# CS 201 · Computer Organization & Architecture
## Week 4 · Lecture 2 of 3
### Cache Organisation — Lines, Sets and Ways

*“The programmer's primary weapon in the never-ending battle against slow system is to change the intramodular structure. Our first response should be to reorganize the modules' data structures.”* — Fred Brooks, *The Mythical Man-Month* (1975), ch. 9

---

**Reading:** CS:APP §6.4 · **Previous:** L13, the hierarchy measured

**Coursework:** 📝 **PS 4** released today, due Fri of Week 5 17:00 · 📝 **PS 3** due Fri this week 17:00 · 📊 **Quiz 5** Mon of Week 5 · 📘 **Midterm 1** Mon of Week 5 18:00–19:15 · 🔬 **Lab 4** Tue of Week 5 15:00–16:50

---

## 1. Three Numbers Describe Any Cache

$$\text{capacity} = S \times E \times B$$

| Symbol | Meaning | On this machine's L1d |
|---|---|---|
| $B$ | **block** (line) size in bytes | 64 |
| $E$ | **ways** — lines per set | 8 |
| $S$ | **sets** | 64 |

$$64 \times 8 \times 64 = 32\,768 = 32\text{ KiB} \quad\checkmark$$

*(Verified against `lscpu -C`.)* And the other two levels:

$$\text{L2: } 1024 \times 4 \times 64 = 256\text{ KiB} \quad\checkmark \qquad \text{L3: } 8192 \times 12 \times 64 = 6\text{ MiB} \quad\checkmark$$

**Everything else about a cache is a consequence of those three numbers.**

---

## 2. How an Address Is Split

A physical address is cut into three fields — **and the cache never sees them as anything else:**

```
 63                    …                    6 5        0
┌──────────────────────┬────────────────────┬───────────┐
│         tag          │    set index       │  offset   │
└──────────────────────┴────────────────────┴───────────┘
```

| Field | Bits | Purpose |
|---|---|---|
| **offset** | $\log_2 B = 6$ | which byte within the line |
| **set index** | $\log_2 S = 6$ | **which set the line must go in** |
| **tag** | the rest | identifies which line is present |

**The set index is not a hint. It is arithmetic.** Address $A$ can only ever live in set $\lfloor A/64 \rfloor \bmod 64$. If that set is full, something in it is evicted — **even if the other 63 sets are empty.**

**Lookup:** index the set, compare the tag against all $E$ ways in parallel, and on a match use the offset. All $E$ comparators run at once, which is why high associativity costs power and latency.

---

## 3. Direct-Mapped, Set-Associative, Fully Associative

They are the same design at three values of $E$.

| $E$ | Name | Trade |
|---|---|---|
| 1 | **Direct-mapped** | One comparator, fastest lookup. Two hot addresses mapping to the same set thrash forever |
| 2–16 | **Set-associative** | What every real cache is. This machine: 8-way L1, 4-way L2, 12-way L3 |
| $S=1$, all lines one set | **Fully associative** | No conflicts ever, but $E$ comparators — only practical for tiny caches like the TLB |

**Direct-mapped caches fail spectacularly on a specific pattern.** Two arrays whose addresses differ by exactly the cache size map to the same set at every index, so alternating between them misses every time — with 99% of the cache sitting empty. Associativity is what makes that merely bad instead of catastrophic.

---

## 4. The Three Kinds of Miss

Diagnosis matters, because each has a different fix.

| Miss | Cause | Fix |
|---|---|---|
| **Compulsory** *(cold)* | First-ever reference to the line | **None** — you must fetch it once. Prefetching can only hide it |
| **Capacity** | The working set exceeds the cache | Make the working set smaller — **blocking** (L15) |
| **Conflict** | Too many hot lines map to one set | Change the addresses: **padding**, or a different stride |

**Distinguishing capacity from conflict is the useful skill.** If your data fits comfortably in the cache and you are still missing, the misses are conflict misses, and the fix is layout rather than algorithm.

---

## 5. Conflict Misses Are a Power-of-Two Problem

The set index is $\lfloor A/64 \rfloor \bmod 64$. **Any stride that is a multiple of $S \times B = 64 \times 64 = 4096$ bytes hits the same set every time.**

That is why **powers of two are dangerous array dimensions**. A `double` matrix with a row length of 512 has rows exactly $512 \times 8 = 4096$ bytes apart — so `m[0][j]`, `m[1][j]`, `m[2][j]` … all map to the **same L1 set**. With 8 ways, the ninth row evicts the first.

**The fix is to break the alignment**, usually by padding the row length by one element:

```c
double m[512][513];    /* rows are 4104 bytes apart, not 4096 */
```

**This is the standard reason production numerical libraries pad their leading dimensions**, and it is worth recognising in code you did not write.

### But check that conflict is your problem first

Padding fixes **conflict** misses. It does nothing for the other two kinds, and it is easy to reach for it when the problem is elsewhere.

Traversing `double m[512][512]` by column — the textbook conflict scenario, stride exactly 4096 — and then padding to `[512][513]`:

| | D1 miss rate | LLd miss rate | wall clock |
|---|---:|---:|---:|
| `[512][512]` | 95.0% | 0.6% | 0.1324 s |
| `[512][513]` | 93.7% | 0.6% | 0.1347 s |

*(Measured.)* **The miss rate barely moved, and the padded version was marginally *slower*.**

**Why.** The set conflict is real, but it is not what costs the time. Column traversal takes **one useful `double` from every 64-byte line** — a 1-in-8 spatial-locality waste that no amount of re-mapping repairs. And with the whole 2 MiB array resident in the 6 MiB L3, those misses are ~41-cycle L3 hits, not 438-cycle DRAM trips: `LLd` is 0.6%.

> **The general rule this illustrates is the week's real subject.** Padding, blocking and layout
> changes each address a *different* kind of miss. **Diagnose which level is missing, and why, before
> choosing the intervention** — otherwise you will apply a correct technique to the wrong problem and
> measure nothing, which is exactly what happened here.
>
> L13's exercise 5 asked whether padding 4096 to 4097 would help the column-major loop. **The answer
> is no, and now you have the measurement.**

---

## 6. Writes Are the Complicated Half

Reads have one policy. Writes have two decisions.

**On a write hit — when to propagate:**

| Policy | Behaviour | Trade |
|---|---|---|
| **Write-through** | Update cache and next level immediately | Simple, always consistent, high traffic |
| **Write-back** | Update cache, mark the line **dirty**, write out on eviction | Far less traffic — repeated writes coalesce. Needs a dirty bit |

**On a write miss — whether to fetch first:**

| Policy | Behaviour |
|---|---|
| **Write-allocate** | Fetch the line, then write into it |
| **No-write-allocate** | Write straight through, do not disturb the cache |

**Essentially all modern caches are write-back with write-allocate**, because both bets pay off under temporal locality: a line you just wrote is likely to be written again.

**The counter-intuitive consequence of write-allocate:** writing to memory you never read still **reads** it first. Initialising a large array costs a full read of it. That is why `memset` of a very large buffer can be limited by *read* bandwidth, and why non-temporal store instructions (`movnt*`) exist — they bypass the cache precisely to avoid this.

---

## 7. The Programmer's View

You cannot control the cache. You control four things that determine how it behaves:

1. **How much data is live at once** — the working set, against $S \times E \times B$.
2. **In what order you touch it** — sequential uses all of every line; strided discards most of it.
3. **How it is laid out** — array of structs against struct of arrays; padding.
4. **How often you come back** — whether a line is still resident on reuse.

**Nothing in this list is visible in your algorithm's complexity.** Two $O(n^2)$ loops differ by 30× (L13 §6). Big-O counts operations; the cache counts lines.

---

## 8. What to Take Away

1. **$S \times E \times B$ = capacity.** This machine: $64 \times 8 \times 64$ = 32 KiB L1d, verified.
2. **The set index is arithmetic, not a hint** — an address has exactly one set it may occupy.
3. **Direct-mapped, set-associative, fully associative** are one design at three values of $E$.
4. **Compulsory, capacity, conflict** — different causes, different fixes.
5. **Power-of-two strides cause conflict misses**; pad the leading dimension.
6. **Write-back + write-allocate**, so writing an array reads it first.
7. **Complexity counts operations; the cache counts lines.**

---

## Exercises

1. Verify the L2 and L3 geometries from `lscpu -C` the way §1 verifies L1d.
2. Give the set index and tag for address `0x7fff8a3c40` in this machine's L1d. Show the bit split.
3. A direct-mapped 32 KiB cache with 64-byte lines. Two `float` arrays of 8192 elements each, allocated back to back. Adding them elementwise, what is the hit rate, and why?
4. Now make it 8-way with the same capacity. What changes, and what does not?
5. A `double A[512][512]` is traversed by column. Compute the byte stride between successive accesses, show that they collide in L1, and say how many rows can be live before eviction begins.
6. Explain why `memset` on a 100 MiB buffer might be limited by memory **read** bandwidth. Which policy causes this, and what instruction avoids it?

---

*Next: L15 — turning all of this into a 3× speedup on a real kernel.*
