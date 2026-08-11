# CS 201 · Computer Organization & Architecture
## Week 10 · Lecture 1 of 3
### Cache Coherence and the MESI Protocol

---

**Reading:** CS:APP §6.6 (revisited), Patterson & Hennessy §5.10 · **Previous:** L30, the security mindset

---

## 1. The Problem Two Cores Create

Week 4 gave every core a private L1 cache, which is what made memory fast. **Multiple cores with private caches create a problem the single-core machine never had.**

```
   Core 0                    Core 1
   ┌────────┐                ┌────────┐
   │ L1: x=5│                │ L1: x=5│      both have cached x
   └────────┘                └────────┘
        └──────────┬───────────┘
              shared L3 / DRAM: x=5
```

Core 0 writes `x = 6`. **Core 1's cached copy still says 5.** If nothing intervenes, Core 1 reads a stale value, and the program is wrong in a way that depends on timing — the worst kind of bug.

**Cache coherence is the guarantee that this cannot happen**: every core sees a single, consistent value for each memory location, as if there were one shared memory. **It is provided by hardware**, transparently, and it is not free — this lecture is about what it costs.

---

## 2. MESI: Four States per Line

The classic coherence protocol gives every cache line one of four states. The name is the four initials:

| State | Meaning | Who else has it |
|---|---|---|
| **M** — Modified | This cache has the only copy, and it is dirty | Nobody |
| **E** — Exclusive | This cache has the only copy, and it is clean | Nobody |
| **S** — Shared | This cache has a clean copy | Others may too |
| **I** — Invalid | This line holds nothing usable | — |

**The rule that does the work: a core may not write a line unless it is in M or E — that is, unless it holds the *only* copy.** To write a Shared line, it must first send an **invalidate** to every other cache holding it, forcing them to I, and only then may it write.

**Reads are cheap; writes to shared data are not.** A read can be satisfied from any core holding the line in S. A write must first make every other copy disappear.

---

## 3. The Write That Costs

Trace `x = 6` when Core 1 also has `x` cached (both in **S**):

1. Core 0 wants to write. Its line is **S** — not writable.
2. Core 0 broadcasts **"invalidate x"** on the interconnect.
3. Core 1 marks its copy **I** and acknowledges.
4. Core 0's line becomes **M**; it writes 6.
5. Core 1 now reads `x` → **miss** → the line is fetched (from Core 0's M copy), and both settle to **S** again.

**Every write to shared data is a broadcast and a set of acknowledgements**, and the latency is that of the inter-core interconnect — far more than an L1 hit. **If two cores write the same line in turn, the line ping-pongs between them**, each write forcing an invalidate and each subsequent read forcing a re-fetch. This is **cache-line bouncing**, and it is the single most important performance pathology of multi-core code.

---

## 4. Measured: One Atomic Counter

Nothing shows this better than a single shared counter. Each thread does `atomic_fetch_add(&shared, 1)`, and the same total number of increments is split across more threads:

| threads | time | throughput |
|---:|---:|---:|
| **1** | 6.23 s | **64.2 M ops/s** |
| 2 | 20.19 s | 19.8 M ops/s |
| 4 | 20.53 s | 19.5 M ops/s |
| 8 | 18.77 s | 21.3 M ops/s |

*(Measured, i5-8250U, `stdatomic` on one shared `long`.)*

**Read the throughput column, and read it twice.** One thread does 64 million increments per second. **Two threads do fewer than 20 million *between them* — the program got three times slower by adding a core.**

**This is negative scaling**, and it is not a subtlety or a measurement artefact. **The single counter's cache line must be in M in exactly one core to be written, so every increment on a different core forces an invalidate-and-transfer of the line.** The threads are not computing in parallel; they are taking turns passing one cache line back and forth across the interconnect, and paying the interconnect latency on every single increment.

> **This is the multi-core version of a lesson the course keeps teaching: the bottleneck is data
> movement, not computation.** The atomic operation itself is a few cycles. The line transfer is
> hundreds. **A shared counter does not scale, full stop** — and the fix is never a faster atomic; it
> is to stop sharing (L32's per-thread counters).

---

## 5. Memory Consistency: a Separate, Harder Problem

Coherence guarantees that all cores agree on the value of *one* location. **It says nothing about the order in which writes to *different* locations become visible.** That is **memory consistency**, and it is where concurrency gets genuinely hard.

Consider two cores:

```
Core 0:  x = 1;  r1 = y;        Core 1:  y = 1;  r2 = x;
```

Intuitively, `r1 == 0 && r2 == 0` should be impossible — one of the writes must happen first. **On x86-64 it can happen anyway**, because each core's *store* can be buffered and made visible to the other core *after* its own later *load*. The hardware reorders your memory operations, within limits the architecture specifies.

**x86-64 is relatively strong** — it is "TSO", total store order, which forbids most reorderings but permits exactly the store-load one above. **ARM and POWER are far weaker** and permit reorderings that would astonish a C programmer. **This is why the same lock-free code can be correct on x86 and broken on ARM.**

**The programmer's tools are the C11 memory model** — `atomic` operations with an ordering (`memory_order_seq_cst` is the safe default; `acquire`/`release` are the expert options) — and **memory fences**, which force ordering where the hardware would not. Week 5's out-of-order execution was one core reordering *its own* instructions invisibly; this is reordering that *other cores can observe*, and it cannot be made invisible without cost.

> **The one rule to carry:** never reason about concurrent code from the source order of memory
> operations across threads. **The hardware does not promise it**, and the memory model is the only
> contract you have. This is CS 211's and PROG 202's material in full; here it is the reason lock-free
> programming is a specialist skill.

---

## 6. What to Take Away

1. **Private caches make multi-core fast and create the coherence problem.**
2. **MESI: a line is Modified, Exclusive, Shared or Invalid**, and only M/E is writable.
3. **Writing a Shared line requires invalidating every other copy** — a broadcast, not a local operation.
4. **A single shared counter scaled *negatively*** — 64 M ops/s on one core, 20 M across two — because its line bounces.
5. **The bottleneck is line movement, not the atomic.** Stop sharing rather than optimising the sharing.
6. **Coherence ≠ consistency.** Coherence is per-location agreement; consistency is cross-location ordering, and x86-64's TSO still permits store-load reordering.
7. **Never trust source order across threads.** The memory model is the only contract.

---

## Exercises

1. Two cores hold `x` in S. Core 0 writes, then Core 1 reads, then Core 1 writes. Give the MESI state of each cache's line after every step.
2. The atomic counter did 64 M ops/s on one thread and ~20 M on two. Explain why aggregate throughput *fell*, in terms of what must be true of the line's MESI state to write it.
3. Why is a *read*-heavy shared workload fine under MESI while a *write*-heavy one is not? Which state lets many cores share cleanly?
4. Give the store-load reordering example. Why can `r1 == 0 && r2 == 0` occur on x86-64 despite coherence?
5. The same lock-free algorithm is correct on x86 and broken on ARM. What property differs, and what would you add to fix the ARM version?
6. A colleague proposes "make the atomic faster" to fix the counter's scaling. Explain why that cannot work and what the actual fix is.

---

*Next: L32 — false sharing, NUMA, and how to write multi-core code that scales.*
