# PROG 201 · Quiz 10
## Administered: Tuesday, Week 10 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 9** — profiling, the memory hierarchy, the roofline model, and optimising honestly.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **PS 9 is due Friday** — the 5×-by-analysis exercise.

---

**Q1.** A program takes 2.35 s. Every `-O` flag gets it to 2.33; three source changes get it to 0.03. What is the one-sentence lesson, and why is `-O3` sometimes slower than `-O2`?

&nbsp;

&nbsp;

---

**Q2.** `perf` refuses to run on these machines. Why, and what two tools does the course use instead?

&nbsp;

&nbsp;

---

**Q3.** A random pointer chase reports 1.5 ns per access at 8 KiB and 142 ns at 64 MiB. What are those two numbers, and what is the ratio telling you to do?

&nbsp;

&nbsp;

---

**Q4.** Your machine does 13.7 GB/s and 13.5 GFLOP/s. What is the ridge point, and what does a kernel's position relative to it tell you before you write any code?

&nbsp;

&nbsp;

---

**Q5.** Two kernels have identical arithmetic intensity and identical flop counts and differ by 2.9× in speed. The roofline cannot explain it. What is the difference?

&nbsp;

&nbsp;

---

**Q6.** Your bandwidth benchmark reports a kernel achieving 222% of the roofline. What do you conclude, and what is the most likely cause?

&nbsp;

&nbsp;

---

**Q7.** `-O2` emits no SIMD for an integer sum; `-O3` emits ten instructions and runs 4.8× faster in L1. What did `-O3` do, and why will the compiler not do the same for a `float` sum without permission?

&nbsp;

&nbsp;

---
---

# Answer Key

*Mark your own. Be honest — nobody else will see this.*

---

**Q1.** **The compiler cannot fix your algorithm** — flags bought 19%, a hash table bought 60× — and once the algorithm is right the flags stop mattering (0.05 s to 0.04 s). `-O3` can be slower because its extra inlining, unrolling and vectorisation **grow the code**, and bigger code misses the instruction cache; `-O3` is a guess that more speculation pays. *(L28 §1, L30 §2.)*

---

**Q2.** **`kernel.perf_event_paranoid` is 4**, which refuses even a `task-clock` count on your own process (performance counters are a side channel), and lowering it needs root on a shared machine. The course uses **Callgrind** (exact, instruction counts, source-annotated) and a **sampling profiler you write** (`setitimer(ITIMER_PROF)` + a `SA_SIGINFO` handler reading `REG_RIP`). *(L28 §3, §5.)*

---

**Q3.** **L1 latency (~1.5 ns) and DRAM latency (~142 ns)** — a factor of ~95. It is telling you that **where your data sits matters far more than how fast your arithmetic is**: keep the working set in cache, and touch memory in a cache-friendly order. *(L29 §1.)*

---

**Q4.** **Ridge point = 13.5 / 13.7 ≈ 0.98 flops per byte.** A kernel with arithmetic intensity **below** that is memory-bound — no amount of arithmetic cleverness helps, only moving less data; **above** it, possibly compute-bound. The number tells you which half of the problem you are in **before writing a line**. *(L29 §4–§5.)*

---

**Q5.** **Dependency chains.** One kernel is a single chain where each operation waits for the previous one, running at the FMA *latency* (~4 cycles each); the other has several independent chains and runs at the FMA *throughput* (~2 per cycle). Same flops, same bytes — the roofline models neither latency nor instruction-level parallelism. *(L29 §7.)*

---

**Q6.** **A number above the roofline is impossible, so it is a measurement bug** — the roofline is an upper bound. The most likely cause: the **bandwidth ceiling was measured with a dependency chain** (a one-accumulator `s += a[i]`), which measures add latency, not memory, and reads far too low — making everything look like more than 100% of it. *(L29 §8. This course's own first bandwidth number.)*

---

**Q7.** `-O3` **vectorised** the loop — SIMD instructions that add several integers at once, which also split the reduction into independent accumulators, so the `-O3` version lands on the memory ceiling out of cache and runs 4.8× faster in L1. It will not vectorise a `float` reduction without **`-ffast-math`**, because floating-point addition **is not associative** — reordering it into parallel accumulators changes the result, and the compiler will not change your answer without permission. *(L30 §3.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1 | L28 §1, L30 §2 |
| Q2 | L28 §3, §5 |
| Q3, Q4 | L29 §1, §4–§5 — you sat Lab 9 yesterday |
| **Q5, Q6** | **L29 §7–§8** — the two the roofline cannot see |
| Q7 | L30 §3 |

**Q6 is the one that recurs**, and Week 10 opens on the same idea from the other side: this week you will *build* an exploit that reports a shell, and the way you know a mitigation works is that the identical exploit reports a crash instead.

---

*PROG 201 · Week 10 · Quiz 10 · covers Week 9 · ungraded*
