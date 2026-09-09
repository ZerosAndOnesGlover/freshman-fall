# PROG 201 · Reading Guide · Week 9
## CS:APP Chapters 5 and 6, and one four-page paper

---

**This week's reading is two chapters you have already met and one paper that fits on four pages.**

CS:APP Chapter 6 is the memory hierarchy, which CS 201 covered from the hardware side; read it again from the *program's* side, because L29's measurements are its figures with numbers attached. Chapter 5 is optimisation, and it is the best chapter in the book — Bryant and O'Hallaron take one loop through eleven versions and explain every factor of two.

**And Williams, Waterman and Patterson's roofline paper is four pages**, free, and is the whole of Lab 9.

| Source | Read? | Why |
|---|---|---|
| **CS:APP Ch. 5** | **All of it** | Program optimisation, end to end. §5.7–5.9 is L30 §3 |
| **CS:APP Ch. 6** | **§6.2–6.6** | The hierarchy and locality. §6.6 is L29 §1–§2 |
| **Williams et al., *Roofline* (CACM 2009)** | **All four pages** | The model, by the people who made it. Lab 9 |
| Drepper, *What Every Programmer Should Know About Memory* §3, §6 | **Skim §3, read §6** | §6 is "what programmers can do", and it is a checklist |
| Gregg, *Systems Performance* Ch. 1–2, 6 | Read Ch. 2 | Methodology: USE, workload characterisation, drill-down |
| `man 1 valgrind`, `man 1 callgrind_annotate` | Reference | You will use both this week |

---

## CS:APP Chapter 5 — the questions to hold

**§5.1–5.3 What limits performance**

1. The book's first move is to **eliminate the function call from the loop condition**, and it is worth about a factor of two. **Find the same mistake in PS 9's `slow.c`** — it is in `normalise()` and it is the loop's second clause.
2. §5.3's "optimization blockers": memory aliasing and function calls. Write down why `void f(int *a, int *b)` prevents the compiler from keeping `*a` in a register, and then look up what `restrict` promises.

**§5.4–5.6 Removing work**

3. Code motion, common subexpressions, reducing procedure calls. Which of these does `-O2` do for you, and which does it not? *(Try one and read the assembly.)*
4. §5.6's array-access rewrite. Does GCC do it at `-O2`? Check.

**§5.7–5.9 The machine underneath**

5. **Latency and throughput bounds.** The book gives them for an Intel core. Find the FMA numbers for yours, and use them to predict L29 §7's 2.9× before you look at it.
6. §5.9, **loop unrolling with multiple accumulators**. This is the single most important section for this week: it is L29 §7, L29 §8 and L30 §3 all at once. **Work through Figure 5.21's table.**
7. He measures a limit and calls it the "throughput bound". Say in one sentence how that relates to the roofline's horizontal line.

**§5.11–5.13 Reality**

8. §5.11.1: "Do not do it unless you have measured." Compare with L28 §1's 19% against 60×.
9. §5.12, profiling with `gprof`, and §5.13, Amdahl's law. **Apply Amdahl to PS 9**: if `lookup` is 61.59% of the program and you make it free, what is your ceiling? Now check that against the 60× actually achieved and explain the discrepancy. *(It is a good question, and the answer is about what "the rest" was doing.)*

---

## The Roofline Paper — read it once and then use it

10. Figure 1. Redraw it with **your own two numbers** from Lab 9, and put the ridge point on it.
11. The paper lists "ceilings" below the roof — ILP, SIMD, memory affinity. **L29 §7 measures the first two.** Which of the paper's ceilings does your `poly4` result correspond to?
12. §4 gives arithmetic intensities for seven real kernels. Which of them are to the left of your ridge point, and what does that say about what those programs need?
13. The paper is about multicore. Everything in it applies unchanged to one core; say what changes when you add cores, for the two axes separately.

---

## The Man Pages for This Week

| Page | The paragraph |
|---|---|
| **`man 1 valgrind`** | `--tool=callgrind`, `--tool=cachegrind`, `--cache-sim=yes` |
| **`man 2 setitimer`** | `ITIMER_PROF` against `ITIMER_REAL` and `ITIMER_VIRTUAL`. Three timers, three questions |
| **`man 2 sigaction`** | `SA_SIGINFO` and the third handler argument — a `ucontext_t *` |
| `man 3 dladdr` | What it can and cannot find. L28 §6 |
| `man 1 gcc` | "Options That Control Optimization", in full. It is long and it is the reference for L30 §2 |
| `man 2 perf_event_open` | The "perf_event related configuration files" section, and why yours is 4 |

**And two commands worth knowing by heart:** `getconf LEVEL1_DCACHE_LINESIZE` and `lscpu | grep -i cache`. Everything in L29 §1 and §2 is checkable against them in five seconds.

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| Agner Fog, *Optimizing software in C++* and the instruction tables | The latencies and throughputs, per microarchitecture. The reference everyone uses |
| Intel 64 and IA-32 Optimization Reference Manual | Long, official, and Appendix B is the same tables |
| Gregg, *BPF Performance Tools* | What you would use in production if `perf_event_paranoid` were not 4 |
| Curtsinger & Berger, *Coz: Finding Code that Counts* (SOSP 2015) | **Causal profiling** — measures what speeding a line up *would* buy, which is the question a profiler does not answer |
| Mytkowicz et al., *Producing Wrong Data Without Doing Anything Obviously Wrong* (2009) | Measurement bias: link order and environment size change results by more than most optimisations do |

**The Coz and Mytkowicz papers are the two to read** if you read only two. The second is the academic version of L30 §5.

---

## The Habit for This Week

**Write the number down before you look.**

Every previous week's habit was an instrument — `ss`, `ps`, `LD_DEBUG`, `debugfs`. This one is not a tool, it is a discipline, and it is the only one that makes the tools useful:

1. **A workload and a number**, before anything else. "It is slow" cannot be optimised.
2. **A written prediction**, before the profile. PS 9 Q1(a) marks you for having made one, not for being right — because the useful thing is discovering, once, how often you are wrong.
3. **One change, one measurement**, and the failures recorded alongside the successes. A change that bought nothing is data.
4. **A stated stopping condition.** Otherwise optimisation is unbounded, and the last 5% costs more than the first 60×.

**And the corollary, which this course has now needed five times: if a number is impossible, it is your measurement.** Nothing exceeds the roofline. Nothing runs in zero seconds. A profiler that reports no allocations may be telling the exact truth about a binary that makes none.

---

*PROG 201 · Week 9 · Reading Guide · © CSE Department*
