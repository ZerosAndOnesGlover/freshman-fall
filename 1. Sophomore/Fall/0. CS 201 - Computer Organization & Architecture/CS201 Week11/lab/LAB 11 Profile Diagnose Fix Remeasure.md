# CS 201 · Week 11 · Lab 11
## Profile, Diagnose, Fix, Re-measure

---

**When:** **Tuesday of Week 12**, 15:00–16:50, BH 210 — *after* Week 11's three lectures
**Covers:** Week 11 · **Assessment:** unmarked, checked off by the TA
**You need:** `gcc`, `gprof` (`-pg`), `valgrind` (callgrind, cachegrind). No privileges required.

> **This is the capstone lab.** It runs the full method — measure, profile, diagnose, bound, fix,
> re-measure — on one program, and it is the shape of the optimisation project half of Project 2.
> Do not skip a step; the steps are the point.

---

## Before You Start: Why Not `perf`

`perf` is the tool professionals reach for, and it is what the curriculum names. **On this machine it needs privileges it does not have** (`perf_event_paranoid = 4`, Week 4). So this lab uses **gprof** (sampling + call counts, via `-pg`) and **callgrind/cachegrind** (exact, unprivileged, via valgrind).

**The method is identical; only the instrument changes.** Where `perf` would be better — low overhead, hardware counters, production profiling — the notes say so.

---

## Part 1 — Measure the Whole Thing (10 min)

```c
/* prog.c — a program that spends its time somewhere surprising */
double cheap(double x)     { return x * 1.0001; }
double expensive(double x) { double s=0; for(int i=0;i<50;i++) s+=sqrt(x+i); return s; }
int main(void) {
    double t=0;
    for (long i=0;i<2000000;i++) { t+=cheap(i); t+=cheap(i+1); t+=expensive(i); }
    printf("%.1f\n", t);
    return 0;
}
```

```bash
gcc -O2 -o prog prog.c -lm
time ./prog
```

**Before profiling, predict:** `cheap` is called twice as often as `expensive`. **Which do you think dominates?** Write it down — the point is to be wrong on paper.

**✅ CHECKPOINT 1** — the runtime and your (unprofiled) guess.

---

## Part 2 — Profile to Find the Hotspot (20 min)

```bash
gcc -O2 -pg -o prog_prof prog.c -lm
./prog_prof                      # produces gmon.out
gprof -b prog_prof gmon.out | head
```

**You will see `100.00 ... main` and nothing else** — because `-O2` inlined `cheap` and `expensive` away. **This is the profiling trap from L34.** Fix it:

```bash
gcc -O2 -pg -fno-inline -o prog_prof prog.c -lm
./prog_prof && gprof -b prog_prof gmon.out | head
```

Now:

```
  %   cumulative   self              self
 time   seconds   seconds    calls  ns/call  name
 94.44      0.17     0.17  2000000    85.00   expensive
  5.56      0.18     0.01                     main
  0.00      0.18     0.00  4000000     0.00   cheap
```

*(Verified.)*

**Answer:**

1. **Was your Part 1 guess right?** `expensive` is 94%, `cheap` is 0% despite twice the calls. What quantity actually determined the profile?
2. Why did the `-O2` build attribute everything to `main`? What did `-fno-inline` cost you in realism?
3. Run it under callgrind too: `valgrind --tool=callgrind ./prog_prof`, then `callgrind_annotate`. **You should see `mcount`/`__mcount_internal` near 20% of the profile.** What is that, and what does it say about instrumenting profilers?

**✅ CHECKPOINT 2** — the profile, and your three answers.

---

## Part 3 — Bound the Payoff With Amdahl (10 min)

`expensive` is 94% of runtime. **Before touching it, compute the ceiling:**

1. If you made `expensive` *infinitely* fast, what is the maximum overall speedup? *(Reference: 16.7×.)*
2. If you only made it 2× faster, what is the overall speedup? *(Reference: 1.89×.)*
3. `cheap` is 0%. What is the maximum speedup from optimising `cheap`?

**This is the step that decides whether the work is worth doing.** State, from the numbers, whether `expensive` is worth attacking and whether `cheap` ever is.

**✅ CHECKPOINT 3** — the three Amdahl figures and your decision.

---

## Part 4 — The Real Optimisation: A Memory-Bound Kernel (35 min)

Now the substantial one. A 1024×1024 `double` matrix multiply, which is **memory-bound** and where the roofline earns its keep.

```c
/* mm.c — naive ijk vs cache-friendly ikj */
static double A[N][N], B[N][N], C[N][N];
void mm_ijk(void){ for(i) for(j){ double s=0; for(k) s+=A[i][k]*B[k][j]; C[i][j]=s; } }
void mm_ikj(void){ for(i){ zero C[i]; for(k){ double a=A[i][k]; for(j) C[i][j]+=a*B[k][j]; } } }
```

### 4.1 Measure both

```bash
gcc -O2 -o mm mm.c
./mm
```

*(Verified: naive `ijk` 5.52 s; `ikj` 0.74 s — **7.45×**, identical result.)*

### 4.2 Diagnose with cachegrind

```bash
valgrind --tool=cachegrind --cache-sim=yes --cachegrind-out-file=/dev/null ./mm 0   # ijk
valgrind --tool=cachegrind --cache-sim=yes --cachegrind-out-file=/dev/null ./mm 1   # ikj
```

*(Verified:)*

| | D1 miss rate | LLd miss rate |
|---|---:|---:|
| naive `ijk` | 50.1% | **50.1%** |
| `ikj` | 8.3% | **8.3%** |

**Answer:**

1. The naive version has LLd rate = D1 rate = 50%. **What does that equality tell you** (recall Week 4's transpose)?
2. `ijk` strides down a column of B; `ikj` streams rows. Compute how many useful doubles come out of each 64-byte line in each case, and connect it to the 50%→8% drop.
3. This is a **memory-bound** kernel. On the roofline, which roof is it under, and does the fix reduce flops or bytes moved?

### 4.3 The optimisation ladder

Measure the naive version across flags, then the best combination:

| Version | Time | vs `-O0` |
|---|---:|---:|
| naive `-O0` | 16.12 s | 1.0× |
| naive `-O2` | 5.27 s | 3.1× |
| naive `-O3` | 4.14 s | 3.9× |
| naive `-O3 -march=native` | 2.82 s | 5.7× |
| **`ikj` `-O3 -march=native`** | **0.58 s** | **27.8×** |

*(Verified.)*

**Answer:**

4. Compiler flags gave 5.7× with no source change; the layout change gave ~5× more on top. **Why do they multiply rather than overlap?**
5. **What is the right order** — flags first or layout first — and why?

**✅ CHECKPOINT 4** — both timings, the cachegrind rates, and five answers.

---

## Part 5 — A Benchmark That Lies (15 min)

Reproduce one failure from L36 and explain it.

```c
/* This "sums a big loop" — time it at -O0 and -O2 */
long n = 100000000; long s = 0;
double t0 = now();
for (long i = 0; i < n; i++) s += i;
double t1 = now();
printf("%ld in %.4f s\n", s, t1 - t0);
```

```bash
gcc -O0 -o slow bench.c && ./slow
gcc -O2 -o fast bench.c && ./fast          # reports 0.0000 s
```

*(Verified — `-O2` folds the loop to a constant, Week 0.)*

**Answer:**

1. The `-O2` version reports 0.0000 s. Disassemble `main` and find the constant. **What happened to the loop?**
2. Fix the benchmark so the loop survives `-O2`. Show the disassembly proving it. Name what your fix prevented.
3. **State the checklist question this failure violates** (L36 §6), and one other question from that checklist you would always ask.

**✅ CHECKPOINT 5** — the constant-folded `main`, your fix, and the checklist answers.

---

## Before You Leave

| Task | Command |
|---|---|
| Whole-program time | `time ./prog` |
| Sampling profile + call counts | `gcc -pg -fno-inline …` → `gprof -b prog gmon.out` |
| Exact profile (slow) | `valgrind --tool=callgrind …` → `callgrind_annotate` |
| Diagnose memory behaviour | `valgrind --tool=cachegrind --cache-sim=yes …` |
| Per-source-line miss counts | `cg_annotate cachegrind.out.PID` |
| Real hardware counters *(needs root)* | `perf stat -d ./prog`, `perf record`/`report` |

**The method, one line:** **measure → profile → diagnose → bound → fix → re-measure**, and never skip diagnose or bound. **That loop is the whole of performance engineering, and it is half of Project 2.**

---

*CS 201 · Week 11 · Lab 11*
