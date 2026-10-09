# CS 201 · Computer Organization & Architecture
## Week 11 · Lecture 1 of 3
### Measure First — Profiling and Amdahl in Practice

*“The real problem is that programmers have spent far too much time worrying about efficiency in the wrong places and at the wrong times; premature optimization is the root of all evil (or at least most of it) in programming.”* — Donald Knuth, "Computer Programming as an Art", Turing Award Lecture (1974)

---

**Reading:** CS:APP §5.1–5.4 · **Previous:** L33, the GPU

**Coursework:** 📊 **Quiz 11** today · 🔬 **Lab 10** Tue this week 15:00–16:50 · 📝 **PS 11** released Wed this week, due Fri of Week 12 17:00 · 📝 **PS 10** due Fri this week 17:00

---

## 1. The Whole Course Was Building to This

Eleven weeks of measurement have a method behind them, and this is the week it becomes explicit:

> **Measure. Find the bottleneck. Fix the bottleneck. Measure again.**

Every previous week gave you a piece: Week 4 said count cache misses, Week 5 said find the dependency chain, Week 7 said ask "device or cache?", Week 10 said look for the bouncing line. **Performance engineering is the discipline that ties them together, and its first law is that you are wrong about where the time goes.**

**Knuth's line, in full, because it is always quoted wrong:**

> *"We should forget about small efficiencies, say about 97% of the time: premature optimization is
> the root of all evil. Yet we should not pass up our opportunities in that critical 3%."*

The famous half is a warning against optimising by guesswork. **The forgotten half is the point of this week: there *is* a critical 3%, and the job is to find it and optimise it — with measurement, not intuition.**

---

## 2. You Do Not Know Where the Time Goes

A program that spends its time somewhere surprising:

```c
double cheap(double x)     { return x * 1.0001; }
double expensive(double x) { double s=0; for(int i=0;i<50;i++) s+=sqrt(x+i); return s; }

for (long i = 0; i < 2000000; i++) {
    t += cheap(i); t += cheap(i+1);   /* called twice as often */
    t += expensive(i);                 /* called once */
}
```

**`cheap` is called twice as often as `expensive`.** Intuition, counting call sites, might blame it. **The profiler does not guess:**

```
$ gprof -b prog gmon.out
  %   cumulative   self              self
 time   seconds   seconds    calls  ns/call  name
 94.44      0.17     0.17  2000000    85.00   expensive
  5.56      0.18     0.01                     main
  0.00      0.18     0.00  4000000     0.00   cheap
```

*(Measured.)*

**`expensive` is 94% of the runtime; `cheap`, despite twice the calls, is 0%.** The call count is a red herring — what matters is time per call times calls, and only measurement gives you that. **Optimising `cheap` to nothing would save 0%.**

---

## 3. Two Kinds of Profiler

**Sampling profilers** interrupt the program periodically and record where it is. `perf`, and gprof's timing, work this way.

- **Cheap** — a few percent overhead, so you can profile production.
- **Statistical** — accurate for hot functions, noisy for rare ones.
- **Sees the whole program**, including libraries and the kernel.

**Instrumenting profilers** insert counting code at every function entry and exit. `gprof`'s call counts, and `callgrind`, work this way.

- **Exact** — every call counted.
- **Slow** — callgrind runs a program 20–50× slower.
- **Perturbs what it measures** — the instrumentation itself takes time.

**You can see the perturbation directly.** Running the profiled binary under callgrind, the profiling machinery *itself* appears in the profile:

```
1,030,000,000 (74.4%)  expensive
  156,000,000 (11.3%)  __mcount_internal      <- gprof's own counting code
  126,000,000 ( 9.1%)  mcount                 <- more of it
```

*(Measured.)* **Twenty percent of the "work" is the profiler.** This is Week 0's lesson yet again — *the tool changes what it measures* — and it is why a sampling profiler, which barely perturbs, is the right default, and callgrind is for when you need exact counts and can tolerate the distortion.

> **On this machine `perf` needs privileges it does not have** (`perf_event_paranoid`, Week 4). So this
> week uses **gprof** (compile with `-pg`) and **callgrind** (unprivileged), and notes where `perf`
> would be the better tool. The *method* is identical; only the instrument changes.

---

## 4. The `-O2` Trap in Profiling

gprof needs function boundaries to attribute time — and `-O2` **inlines** functions, erasing those boundaries. Profile the optimised build and:

```
100.00      0.18     0.18                     main
```

*(Measured — `-O2`, everything inlined into `main`.)* **The profiler says 100% of the time is in `main` and tells you nothing**, because `cheap` and `expensive` no longer exist as separate functions.

**The fix is `-O2 -fno-inline` for profiling** — optimised code, but with the boundaries preserved so the profiler can see them. **Profile something close to what ships, not the debug build** (which would mislead you about what is hot), **but keep the structure the profiler needs.** This tension — realistic optimisation versus observable structure — is why profiling is a skill and not a button.

---

## 5. Amdahl Tells You What Is Worth Doing

Once the profile names the hotspot, Amdahl's Law (Week 5) tells you the *ceiling* on fixing it — before you spend a day trying.

$$S = \frac{1}{(1-p) + \dfrac{p}{s}}$$

**`expensive` is 94% of runtime.** If you made it *infinitely* fast:

$$S_{\max} = \frac{1}{1 - 0.94} = \mathbf{16.7\times}$$

**And if you only halved it** ($s = 2$):

$$S = \frac{1}{0.06 + \frac{0.94}{2}} = \frac{1}{0.53} = \mathbf{1.89\times}$$

**Read those two numbers together.** Even perfect elimination of the hotspot caps you at 16.7×; a realistic 2× on it gives 1.89×. **Amdahl converts a profile into a budget:** it tells you the best case *before* you invest, so you can decide whether the hotspot is worth attacking or whether the 6% "rest" has become the new ceiling.

**The corollary drives the whole method:** after each fix, **the bottleneck moves.** Optimise the 94% hotspot away and the 6% is now 100% of a much smaller runtime — so you re-profile, find the *new* hotspot, and repeat. **Performance engineering is iterative because Amdahl guarantees the target moves every time you hit it.**

---

## 6. The Method, Stated

| Step | Tool | Question |
|---|---|---|
| 1. **Measure** the whole thing | stopwatch, `time` | Is it even slow? Where, roughly? |
| 2. **Profile** to find the hotspot | gprof, `perf`, callgrind | *Which function* is the time in? |
| 3. **Diagnose** the hotspot | cachegrind, disassembly | *Why* is it slow — compute, memory, branches? |
| 4. **Bound** the payoff | Amdahl | Is fixing it worth it? |
| 5. **Fix**, then **re-measure** | — | Did it work? Where is the time *now*? |

**Steps 3 and 4 are the ones beginners skip**, and they are what separate engineering from thrashing. **Diagnosing tells you *what kind* of fix (L35's roofline); bounding tells you *whether* to bother.** The next lecture is step 3.

---

## 7. What to Take Away

1. **Measure first.** You are wrong about where the time goes — `expensive` was 94%, `cheap` 0%, despite twice the calls.
2. **Knuth's full quote endorses the critical 3%.** The warning is against *guessing*, not against optimising.
3. **Sampling profilers are cheap and statistical; instrumenting ones are exact and slow** — and the instrumentation shows up in its own profile (20% here).
4. **`-O2` inlines away the boundaries** a profiler needs; profile with `-O2 -fno-inline`.
5. **Amdahl converts a profile into a budget** — a 94% hotspot caps you at 16.7× even if you delete it.
6. **The bottleneck moves after every fix**, so the method iterates.

---

## Exercises

1. `expensive` is 94% and called 2M times; `cheap` is 0% and called 4M times. Explain why the call count misled, and what quantity actually determines the profile.
2. A profile shows a function at 30%. Give the maximum overall speedup from optimising it, and the speedup if you make it 3× faster.
3. Why does profiling a `-O2` build often attribute everything to `main`? What flag fixes it, and what does that flag cost in realism?
4. Callgrind showed `__mcount_internal` at 11% of the profile. What is that, and what does its presence tell you about instrumenting profilers?
5. You optimise a 94% hotspot down to nothing. The program is now dominated by a function that was 4%. What has changed, and what do you do next?
6. When would you accept callgrind's 20–50× slowdown over a sampling profiler's few percent?

---

*Next: L35 — the roofline model, and diagnosing *why* the hotspot is slow.*
