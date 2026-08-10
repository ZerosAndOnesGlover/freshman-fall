# CS 201 · Week 4 · Reading Guide
## CS:APP Chapter 6 — The Memory Hierarchy

---

**Set reading:** Bryant & O'Hallaron, **§6.1–6.6**. This is the most directly useful chapter in the book for working programmers.
**Also:** Ulrich Drepper, *What Every Programmer Should Know About Memory* (2007) — **§3.1–3.3**.

---

## Why This Chapter Repays the Time

Chapter 3 taught you to read what the compiler produced. **Chapter 6 is about the half of performance the compiler cannot help with**, because it depends on your data and your access order, neither of which the compiler can change without knowing your intent.

**§6.6 is the payoff.** Read the earlier sections as setup for it.

---

## Section by Section

| § | Topic | What to take from it |
|---|---|---|
| **6.1.1** | RAM: SRAM vs DRAM | Why one is fast and small and the other slow and large. Six transistors against one |
| **6.1.2–6.1.4** | Disks | Skim now; **Week 7** does storage properly |
| **6.1.5** | Solid state disks | Same — Week 7 |
| **6.1.6** | **The widening gap** | Figure 6.16. The whole justification for the chapter |
| **6.2** | Locality | Temporal and spatial. The book's stride-1 discussion is L13 §4 |
| **6.3** | The memory hierarchy | The general principle, independent of the specific levels |
| **6.4.1** | Generic cache organisation | **$S$, $E$, $B$ and the address split.** The core of L14 |
| **6.4.2** | Direct-mapped caches | Work the example fully. Conflict misses are clearest here |
| **6.4.3** | Set-associative caches | What real caches are |
| **6.4.4** | Fully associative | Rare, but it is how the TLB works — Week 6 |
| **6.4.5** | Writes | Write-back, write-allocate. **Read it; it is the half people skip** |
| **6.4.6** | Anatomy of a real hierarchy | Compare with your own `lscpu -C` |
| **6.4.7** | Performance impact | Miss rate, hit time, miss penalty |
| **6.5** | Writing cache-friendly code | Short and concrete |
| **6.6** | **Putting it together** | The memory mountain, and the transpose/blocking examples. **The point of the chapter** |

---

## Questions to Read Against

**On §6.1.6 and §6.2**

1. Figure 6.16 plots the CPU–memory gap over time. What is the gap now, and what does §6.1.6 predict about closing it?
2. Give a code example with excellent temporal locality and poor spatial locality, and one with the reverse.
3. §6.2 says stride-1 is the best pattern. **At what array size does that stop being the whole story?** *(Consider what the prefetcher can and cannot do.)*

**On §6.4 — the core**

4. State $S$, $E$, $B$ for your own L1d from `lscpu -C`, then verify the capacity.
5. Work the book's direct-mapped example by hand before reading the answer. Then redo it 2-way and say which misses disappear.
6. Derive the byte stride that maps every access to the same set. What array dimension in `double`s produces it?
7. **Why is the set index taken from the *middle* bits of the address rather than the high bits?** *(What would go wrong if consecutive lines all landed in the same set?)*

**On §6.4.5 — writes**

8. Write-back plus write-allocate is near-universal. Give the locality argument for each half.
9. **Why does writing to an array you never read still read it?** What instruction avoids this, and when is it worth using?

**On §6.5–6.6**

10. The book's memory mountain has ridges along both axes. What does each axis control, and which ridge corresponds to the pointer chase in Lab 4?
11. Work through the book's blocked matrix multiply. **How many arrays are live in the inner loop, and how does that change the tile-size calculation compared with transpose?**
12. §6.6 reports speedups from blocking. **Under what conditions does the book say it will not help?** Lab 4 Part 5.3 measures exactly that case.

> **Question 7 is the one worth real thought**, and it is examinable. The answer explains why the
> hierarchy works at all for sequential access.

---

## Reading Against the Machine

```bash
# 1. Your own geometry
lscpu -C

# 2. Build the memory mountain yourself — this is Lab 4 Part 2
#    Pointer chase over working sets from 4 KiB to 32 MiB.
#    Predict where the cliffs will be BEFORE you run it.

# 3. The book's claims about miss rates, checked
valgrind --tool=cachegrind --cache-sim=yes ./yourprog
```

**Item 2 before Tuesday** makes the lab twice as valuable — you will spend the session interpreting rather than typing.

**One caution about cachegrind, which the book does not mention:** it *simulates* a cache and models **no prefetching, no TLB and no out-of-order execution.** It is deterministic and reproducible, which is why this course uses it — but where it disagrees with the stopwatch, **the stopwatch is right.** Lab 4 Part 5 is built on exactly that disagreement.

---

## Terminology You Should Own by Week 5

| | | |
|---|---|---|
| SRAM / DRAM | cache line / block | $S$, $E$, $B$ |
| tag / set index / offset | direct-mapped | set-associative |
| fully associative | hit rate / miss rate | miss penalty |
| compulsory / cold miss | capacity miss | conflict miss |
| temporal locality | spatial locality | stride |
| write-back / write-through | write-allocate | dirty bit |
| eviction | LRU | prefetching |
| blocking / tiling | working set | AoS / SoA |

---

## If You Want More

**Drepper, *What Every Programmer Should Know About Memory*** (2007, ~114 pages). §3 is the best treatment of cache behaviour written for programmers. **Dated in its specifics** — the numbers are from 2007 hardware — **and completely sound in its reasoning.** Read §3.1–3.3 now; §6 is a catalogue of optimisation techniques worth having seen before Week 11.

**Igor Ostrovsky, *Gallery of Processor Cache Effects*** — seven short experiments, each a few lines of code with a surprising graph. An hour well spent, and several of them are Lab 4 in miniature.

**`cg_annotate`** annotates cachegrind output **per source line**, so you can see which line is missing:

```bash
valgrind --tool=cachegrind --cachegrind-out-file=cg.out ./prog
cg_annotate cg.out
```

Not needed for the lab, and the first tool you will want in Week 11.

---

*CS 201 · Week 4 · Reading Guide*
