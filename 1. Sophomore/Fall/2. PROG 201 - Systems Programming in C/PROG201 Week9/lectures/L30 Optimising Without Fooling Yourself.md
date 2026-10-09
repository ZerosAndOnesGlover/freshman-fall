# PROG 201 · Systems Programming in C
## Week 9 · Lecture 3 of 3
### Optimising: What Works, What the Compiler Does, and How Not to Fool Yourself

*“The first principle is that you must not fool yourself — and you are the easiest person to fool.”* — Richard Feynman, "Cargo Cult Science", Caltech commencement address (1974)

---

**Reading:** CS:APP Ch. 5 · `man 1 gcc` (the optimisation options) · Gregg, *Systems Performance* Ch. 12 · **Previous:** L29 · **Next:** Lab 9 — roofline analysis, **Monday of Week 10**

**Coursework:** 📋 **Project 1** due Fri this week 17:00 · 📝 **PS 8** due Fri this week 17:00 · 🔬 **Lab 9** Mon of Week 10 15:00–16:50 · 📊 **Quiz 10** Tue of Week 10 · 📝 **PS 10** released Wed of Week 10, due Fri of Week 11 17:00

---

## 1. The Order Things Work In

Ranked by the size of the win, on the program from L28:

| | what | the measured win |
| --- | --- | --- |
| 1 | **A better algorithm** | linear scan → hash table: most of **60×** |
| 2 | **Less data, or a better layout** | stride 16 → stride 1: **5.8×** (L29 §2) |
| 3 | **Instruction-level parallelism** | 1 chain → 4 chains: **2.9×** (L29 §7) |
| 4 | **Vectorisation** | scalar → AVX2 on an L1-resident sum: **4.8×** |
| 5 | **Compiler flags** | `-O0` → `-Ofast` on the unfixed program: **1.19×** |
| 6 | **PGO** | on this program: **1.00×** |

**The list is in that order for almost every program you will ever profile**, and the two ends are the point: the thing at the top is what you can only do by understanding the problem, and the thing at the bottom is what you can do without thinking. People start at the bottom.

Note also that items 3 and 4 are things the *compiler* will do for you if you let it — which is §3 — so the work that is genuinely yours is items 1 and 2.

---

## 2. The Flags, Measured

Same program, same input:

| | slow program | fast program |
| --- | --- | --- |
| `-O0` | 2.78 s | 0.05 s |
| `-O1` | 2.47 s | 0.04 s |
| `-O2` | 2.35 s | 0.04 s |
| `-O3` | 2.38 s | 0.04 s |
| `-Os` | 2.78 s | 0.04 s |
| `-Ofast` | 2.33 s | — |

Three things in that table:

**Nineteen percent from every flag GCC has**, against 60× from three source changes.

**`-O3` is slower than `-O2` here.** It is not a mistake: `-O3` adds aggressive inlining, loop unrolling and vectorisation, all of which grow the code, and bigger code misses the instruction cache more. `-O3` is a *guess* that more speculation will pay, and it is wrong often enough that most distributions build at `-O2`.

**Once the algorithm is right, the flags do not matter.** 0.05 to 0.04 across the whole range.

What each level actually means:

| | |
| --- | --- |
| `-O0` | none. Every variable lives in memory. **Use it for debugging and never for a measurement** |
| `-O1` | the cheap wins — dead code, constant folding, basic register allocation |
| `-O2` | the standard. Inlining within reason, common subexpressions, strength reduction, scheduling |
| `-O3` | `-O2` plus loop unrolling, aggressive inlining, and **vectorisation** |
| `-Os` | `-O2` minus anything that grows the code. For instruction-cache-bound and embedded work |
| `-Ofast` | `-O3` plus `-ffast-math`, which **changes your results** — §4 |
| `-march=native` | use every instruction this CPU has. **The binary will not run elsewhere** |

---

## 3. What the Compiler Does That You Would Otherwise Do By Hand

**Vectorisation is the big one, and it is `-O3`, not `-O2`:**

```c
int sumi(const int *a, long n){ int s = 0; for (long i = 0; i < n; i++) s += a[i]; return s; }
```

| | SIMD instructions emitted | 64 MiB | 16 KiB (in L1) |
| --- | --- | --- | --- |
| `-O2` | **0** | 8.37 GB/s | 9.68 GB/s |
| `-O3` | 10 | **14.53 GB/s** | **46.28 GB/s** |

**1.74× out of cache and 4.8× in it** — and look where the out-of-cache number lands: **14.53 GB/s against L29's measured ceiling of 13.71.** The `-O3` version is at the memory roof; the `-O2` version was not, and the reason is L29 §7 again — a scalar reduction is one dependency chain, and the vectoriser's first act is to split it into several accumulators.

**And the compiler will not do it to floats without permission:**

```
-O3                  SIMD in the float sum: 10
-O3 -ffast-math      SIMD in the float sum: 14
```

Because floating-point addition **is not associative**: `(a+b)+c` and `a+(b+c)` can differ, so splitting a reduction into four accumulators changes the answer. `-ffast-math` says "I do not care", and it is a promise you should make deliberately and per-file, not globally — it also disables NaN and infinity handling, which turns a well-defined program into an undefined one.

**Inlining** is `-O2` and up, and it will restructure your program to the point where a profile no longer matches your source — L28's Callgrind output attributed 31% to `main` for functions that no longer existed.

---

## 4. Profile-Guided Optimisation, and When It Does Nothing

```bash
gcc -O2 -fprofile-generate -o prog prog.c
./prog typical-input                          # produces .gcda
gcc -O2 -fprofile-use -o prog prog.c
```

The compiler now knows which branches are taken, which functions are hot, and which are cold — so it can lay out the hot path contiguously, inline what is actually called, and move cold code out of the way. On branch-heavy programs — interpreters, parsers, compilers themselves — **10–20% is typical**, and Firefox and Chrome both ship PGO builds.

On the program from §2:

| | seconds |
| --- | --- |
| `-O2` | 0.0380 |
| `-O2` + PGO | 0.0380 |

**Nothing at all**, and that is the correct result rather than a failed experiment. The program is bounded by hash lookups and I/O, not by branch prediction or code layout, so there is nothing for PGO to improve. **A technique that works on other people's programs is not a technique that works on yours**, and the only way to find out is the measurement.

Its real cost is operational: you need a **representative** workload, the profile has to be regenerated when the code changes, and a profile from the wrong workload makes things worse.

---

## 5. How To Fool Yourself

This course has now made the same class of mistake five times, in five different weeks, and every one of them was a measurement that reported something impossible.

**The compiler deleted your benchmark.** Week 8: a program with 1,000 `malloc`/`free` pairs, built `-O2`, contained **no reference to `malloc` at all** — the allocations were removed and the profiler correctly reported nothing. This week: a target program for the sampling profiler ran in **0.00 s** because GCC hoisted the whole loop out.

The fix is to make a value escape:

```c
#define KEEP(x) __asm__ volatile("" :: "r,m"(x) : "memory")
```

That is what every benchmarking library calls `DoNotOptimize`, and it says "this value has left the building; you cannot prove nobody reads it".

**You measured latency and called it bandwidth.** L29 §8: a one-accumulator streaming sum reported 6.28 GB/s on a machine that does 13.71, because a dependent reduction is bounded by add latency. **The tell was a kernel reporting 222% of the roof.**

**Your timer is too coarse.** Ten runs of the same 38 ms program through `/usr/bin/time`:

```
0.03 0.03 0.04 0.04 0.03 0.04 0.03 0.03 0.04 0.03
```

Every measurement is right and the resolution is 10 ms, so a real 5% improvement is invisible and a real 30% one might be. **Use `clock_gettime(CLOCK_MONOTONIC)`, and make the thing you are timing take at least a hundred times your timer's resolution.**

**You measured the first run.** Cold page cache, cold branch predictors, an unfaulted heap, and — this term's own Week 4 result — the difference between a cold and a warm file was **0.17 s against 1.58 s**. Warm up, then measure.

**You reported the mean.** Performance distributions are not symmetric: they have a hard floor (the machine cannot go faster) and a long tail (anything can interrupt you). **The minimum of many runs is the most reproducible statistic** for microbenchmarks, and the p99 is what matters for a service. The mean is the one number that is neither.

**Six rules, then:**

1. Make the result escape, or the compiler deletes the work.
2. Time something long enough for your clock.
3. Warm up.
4. Repeat, and report the minimum — and the spread.
5. Change one thing at a time.
6. **If a number is impossible, it is your measurement.** Nothing exceeds the roofline; nothing runs in zero time; a profiler that reports nothing may be right.

---

## 6. The Checklist

When something is slow:

**Before touching the code**
- Is there a workload and a number? Write both down.
- What is the target? "Faster" is not one.

**Find out where the time is**
- Profile it. Callgrind for exactness, a sampler for cheapness (L28).
- Is it CPU, memory, or waiting? `getrusage`'s user against system against elapsed answers it in one line.

**Find out why**
- Compute the arithmetic intensity and put it on the roofline (L29 §5).
- **Memory-bound?** Move less data: layout, types, fusion.
- **Compute-bound but far from the roof?** Dependency chains, then vectorisation.
- **Neither, and the profile is flat?** It is probably not CPU at all — go back to Weeks 1, 5 and 7.

**Fix it**
- Algorithm first. Always.
- One change, one measurement.
- Keep the slow version and check the outputs still match. The 60× in §1 is only a 60× because the output is byte-identical.

**Stop**
- When it meets the target.
- Write down what you changed and what each change bought, because the next person — who is you, in six months — will otherwise undo it.

---

## Summary

- **Ranked by measured win: algorithm (60×), layout (5.8×), ILP (2.9×), vectorisation (4.8×), flags (1.19×), PGO (1.00×).** Most people start at the bottom.
- Every optimisation flag GCC has bought **19%**; three source changes bought **60×**; and once the algorithm was right, the flags bought nothing.
- **`-O3` was slower than `-O2`** — bigger code, more instruction-cache misses. `-O3` is a guess.
- **`-O2` does not vectorise; `-O3` does** — 0 SIMD instructions against 10, and **1.74× out of cache, 4.8× in it**, with the `-O3` version landing exactly on L29's memory ceiling.
- **Floating-point reductions need `-ffast-math`** to vectorise, because FP addition is not associative and the compiler will not change your answer without permission.
- **PGO did nothing here**, which is the correct result for a program that is not branch-bound.
- Five ways to fool yourself, all of which this course has done: **the compiler deleted the benchmark; latency measured as bandwidth; a 10 ms timer on a 38 ms program; a cold first run; the mean.**
- **If a number is impossible, it is your measurement.**

---

## Exercises

1. Build §2's table for a program of your own. Does `-O3` beat `-O2`? If it does not, look at `size` for both.
2. Take a float reduction, compile it `-O3` and `-O3 -ffast-math`, and compare both the assembly and the **answer**. How big is the difference in the result?
3. Write a benchmark without `KEEP`, confirm with `objdump` that the work is gone, then add it. How long did the "before" version claim to take?
4. Time the same function with `/usr/bin/time`, `clock_gettime(CLOCK_MONOTONIC)` and `clock_gettime(CLOCK_PROCESS_CPUTIME_ID)`. When do the three disagree, and which do you want?
5. Run a benchmark 100 times and plot the distribution. Where are the mean, the median and the minimum, and which would you report?
6. Apply PGO to something branch-heavy — a JSON parser, or an interpreter loop. What do you get, and how does it change if you profile with the wrong input?
7. Take the fast program from §1 and try to make it twice as fast again. Write down what you tried and what each attempt bought, **including the ones that bought nothing.**

---

*PROG 201 · Week 9 · L30 · © CSE Department*
