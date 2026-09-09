# PROG 201 · Systems Programming in C
## Week 9: Performance — Profiling and Optimization in Practice

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101; CS 201 as co-requisite
**Assessment for this course (overall):** Problem Sets 35%, Projects 25%, Midterms 25%, Final 15%
**This week's deliverables:** **Project 1 due Friday 17:00 (12.5%)**, PS 8 due Friday, PS 9 (released Wednesday, due Friday of Week 10) and **Quiz 9** (Tuesday, covers Week 8).
**Lab 8 is sat on the Monday of this week**; **Lab 9 covers this week and is sat on the Monday of Week 10.**

> ### **Two deadlines on Friday: Project 1 and PS 8**, both at 17:00.
> Project 1 is 12.5% of the course. PS 8 was released last week and is about four hours' work —
> if it is not done, do it before Wednesday. [[PROG 201 Scheduling Notes]] records the collision.

---

### Why This Week Exists

Because there is a program in this week's materials that takes 2.35 seconds, and **every optimisation flag GCC has makes it 19% faster** while **three source changes make it 60 times faster.**

Eight weeks of this course have been measurements. This week is the one where measuring is the subject: how to find out where the time goes, how to know what the machine could do at best, and — the part that takes a lecture on its own — **how to not fool yourself**, which this course has failed at five separate times and recorded each one.

Three ideas:

1. **Measure first, and the order of what works is not the order people try.** Algorithm, then layout, then instruction-level parallelism, then vectorisation, then flags. Most people start at the end.
2. **Your machine has two ceilings and you can measure both in an afternoon** — bandwidth and arithmetic peak — and their ratio tells you, before you write anything, which half of the problem you are in.
3. **A number that is impossible is a fact about your measurement.** Nothing exceeds the roofline; nothing runs in zero seconds; a profiler reporting nothing may be right.

---

### Learning Objectives

By the end of Week 9, you should be able to:

1. State the difference between sampling and instrumentation profiling, with the overheads.
2. Say why `perf` is unavailable here and name three things that are not.
3. Read Callgrind output and find the hot path in it.
4. **Write a sampling profiler** — `setitimer(ITIMER_PROF)`, a `SA_SIGINFO` handler, `REG_RIP` out of the `ucontext`, `dladdr` for names.
5. Say why that profiler cannot name static functions or libc internals.
6. **Measure your machine's memory hierarchy** and identify each level from the steps.
7. Explain the cache line from a stride table, and say where the prefetcher stops helping.
8. Measure memory bandwidth and arithmetic peak, and compute a ridge point.
9. Compute a kernel's arithmetic intensity and place it on a roofline.
10. **Say what the roofline does not model** — dependency chains, prefetching, vectorisation.
11. Rank optimisation techniques by their measured payoff.
12. Say what each `-O` level does, and why `-O3` can be slower than `-O2`.
13. Explain why a float reduction needs `-ffast-math` to vectorise.
14. **Recognise five ways a benchmark lies**, and defend against each.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L28 Measure First and What a Profiler Costs]] | **19% from every compiler flag against 60× from three source changes**; sampling against instrumentation; **`perf` is unavailable and why**; Callgrind's 61.59% in `strcmp`; **writing a sampling profiler in sixty lines**; the two ways it lies to you |
| [[L29 Caches Bandwidth and the Roofline]] | The hierarchy measured — **L1 1.49 ns to DRAM 141.94, a factor of 95**; the cache line from a stride table and where the prefetcher gives up; **13.71 GB/s and 13.50 GFLOP/s, ridge point 0.98**; kernels at 99% and at 18% of their roof; **the bug this lecture was written with** |
| [[L30 Optimising Without Fooling Yourself]] | The ranked list, with measured wins; the `-O` levels, where `-O3` is slower than `-O2`; **`-O2` does not vectorise and `-O3` does — 1.74× out of cache, 4.8× in it**; PGO doing nothing, correctly; **five ways to fool yourself, all of which this course has done** |
| [[LAB 9 Roofline Analysis]] | Measure your machine's two ceilings, then find the bug that puts a kernel above the roof. **Monday of Week 10** |
| `lab/roof.c`, `lab/cache.c`, `lab/sprof.c`, `lab/target.c`, `lab/vecbench.c` | The skeleton and four provided experiments |
| [[PS 9 Make It Five Times Faster]] | Profile a slow program, make it 5× faster **by analysis**, and account for every change. Due **Friday of Week 10** |
| `assignments/ps9/` | `slow.c`, `gen.c`, and `check.sh` — which requires byte-identical output |
| [[PROG201 Week9/assignments/QUIZ 9 Week 9 Tuesday\|QUIZ 9 Week 9 Tuesday]] | Ten minutes, covers **Week 8**, answer key printed |
| [[PROG201 Week9/resources/Reading Guide Week 9\|Reading Guide Week 9]] | CS:APP Ch. 5–6 and **the four-page roofline paper** |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**If a number is impossible, it is your measurement.**

This course has produced five impossible numbers and each one was a bug that a plausible-looking result would have hidden:

| Week | The impossible number | What it actually was |
| --- | --- | --- |
| 4 | `sendfile` and `mmap` reporting the same `ru_maxrss` | a high-water mark, contaminated by running both in one process |
| 4 | a 512 MiB `mmap` taking 0.000 s with **0 page faults** | the compiler deleted the loop |
| 8 | a profiler reporting **2 allocations** for a thousand `malloc`/`free` pairs | `-O2` deleted every one; the binary does not reference `malloc` |
| 9 | a kernel achieving **222% of the roofline** | the bandwidth ceiling was measured with a dependency chain |
| 9 | a one-second program running in **0.00 s** | the compiler hoisted the whole benchmark |

**Four of the five are the compiler removing work, or a dependency chain being mistaken for a resource limit** — and neither announces itself. The defence is not vigilance; it is having a model of what the answer should be, so that a wrong one looks wrong.

That is what the roofline is *for*. Not to predict your performance, but to give you a ceiling that, when you exceed it, tells you that you have made a mistake.

---

### Assessment Reminder

**Project 1 is due Friday at 17:00 and is worth 12.5%.** **PS 8 is due the same day.**

**Labs and quizzes carry no weight** and are still required. **Quiz 9 is at the start of Tuesday's lecture and covers Week 8.**

> **Lab 8** — Week 8's plugin host — is sat on the **Monday of this week**. **Lab 9** covers this
> week and is sat on the **Monday of Week 10**.

Both are tracked in [[_PROG 201 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 0's signals are the sampling profiler** — `SA_SIGINFO`, async-signal-safety, and a handler that must not allocate. **Week 8's `dladdr` and `-rdynamic`** are why the profiler can or cannot name a function. **Week 4's page faults and Week 7's page cache** are the memory side of L29. And **Week 4's 339× allocator** is L28 §1's argument in a different domain: the workload decided the result.

**Sideways:** **CS 201 Week 9 is on performance from the architecture side** — pipelines, superscalar issue, and the latency-against-throughput distinction that L29 §7's dependency chains are made of.

**Forward:** **Week 10 is security**, where the program being analysed is somebody else's and the goal is to find one path rather than the hot one. **Week 12's project** is a system you will have to profile. And Project 2 — a networked, multi-threaded server — is Week 5's measurements plus this week's method.

---

*PROG 201 · Week 9 · © CSE Department*
