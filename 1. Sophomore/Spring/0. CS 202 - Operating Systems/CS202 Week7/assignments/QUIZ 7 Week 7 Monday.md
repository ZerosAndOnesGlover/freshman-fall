# CS 202 · Quiz 7
## Administered: Monday, Week 7 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 6** — swapping, major faults, page replacement, working sets, thrashing, the OOM killer.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **Lab 6 is tomorrow afternoon and PS 6 is due Friday. Project 1 is assigned this week.**

---

**Q1.** xv6 runs out of memory while a process calls `sbrk`. **What happens to that process, and to the others?** How does Linux differ?

&nbsp;

&nbsp;

---

**Q2.** Give the reference string 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5 to FIFO with **three** frames and then with **four**. **What is surprising, and what is the name for it?** Why can LRU not do the same?

&nbsp;

&nbsp;

---

**Q3.** Exact LRU needs to know the order in which pages were last used. **Why can a kernel not maintain that order**, and what does it use instead?

&nbsp;

&nbsp;

---

**Q4.** A process holds 257 MiB of memory but references only 16 MiB of it each second. **Which number determines whether it thrashes**, and how would you measure the second one from an ordinary account?

&nbsp;

&nbsp;

---

**Q5.** A major fault on the reference machine costs about **90 µs**, an ordinary memory access about **8 ns**. A program makes 10 million memory accesses, of which 0.1% are major faults. **How long does it take, and what fraction of the time is waiting for the disk?**

&nbsp;

&nbsp;

---

**Q6.** `mmap` of 12 GiB is refused on a machine with 7.5 GiB of RAM and 4 GiB of swap, but a thousand mappings of 8 GiB each succeed. **Explain both.**

&nbsp;

&nbsp;

---

**Q7.** Two processes: one holds 4 GiB with `oom_score_adj` 0, the other holds 200 MiB with `oom_score_adj` 500. **Which does the OOM killer choose on a machine with 8 GiB of RAM and no swap?** Show the comparison.

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **`kalloc` fails, `allocuvm` undoes its partial work, and `sbrk` returns −1** — the process is told, and **nothing is killed**; other processes are unaffected. **Linux almost never refuses** (overcommit): it reclaims pages, swapping if it must, and **kills a process** only when reclaim cannot free anything.

---

**Q2.** **Three frames: 9 faults. Four frames: 10** — more memory, more faults. **Belady's anomaly.** LRU cannot show it because it is a **stack algorithm**: with *n* frames it holds the *n* most recently used pages, which is always a subset of what it holds with *n* + 1, so a hit with *n* frames is a hit with *n* + 1.

---

**Q3.** **Most references never reach the kernel** — the TLB and the page table translate them in hardware — so the kernel would have to fault on every access to see it. **It uses the accessed bit** the CPU sets in each page-table entry, sampled by Clock, aging, or Linux's lists.

---

**Q4.** **The working set — 16 MiB — decides**, not the 257 MiB resident. It thrashes when the memory available to it is below the working set. **Measure it by writing `1` to `/proc/<pid>/clear_refs`, waiting the interval, and reading `Referenced` from `/proc/<pid>/smaps_rollup`.**

---

**Q5.** 10,000 major faults × 90 µs = **0.9 s**; the other 9,990,000 accesses × 8 ns = **0.08 s**. **Total ≈ 0.98 s, of which 92% is waiting for the disk** — for one access in a thousand.

---

**Q6.** Overcommit mode 0 **refuses a single request larger than RAM + swap** (11.5 GiB here) as obviously unsatisfiable, **but never compares the sum of all promises against anything.** Memory is only charged when it is touched, so unused promises cost nothing.

---

**Q7.** Score is memory plus adjustment, on this kernel ⅔ × (1000 + adj + 1000 × RSS ÷ total). **First: 4 GiB of 8 GiB = 500‰, adj 0 → ⅔ × 1500 = 1000.** **Second: 200 MiB ≈ 24‰, adj 500 → ⅔ × 1524 = 1016.** **The 200 MiB process is killed** — its adjustment outweighs the other's four gigabytes.

---

### What to Do With Your Score

There is no score. Instead, before Friday:

| If you missed | Reread |
|---|---|
| Q1 | L19 §1–§2 |
| Q2, Q3 | L20 §2–§5 — and run `pagesim` on `belady.txt` |
| Q4 | L21 §1 |
| Q5 | L19 §3 |
| Q6 | L21 §4 |
| Q7 | L21 §5 — **Lab 6 Part E is this** |

---

*CS 202 · Week 7 · Quiz 7 · covers Week 6 · ungraded*
