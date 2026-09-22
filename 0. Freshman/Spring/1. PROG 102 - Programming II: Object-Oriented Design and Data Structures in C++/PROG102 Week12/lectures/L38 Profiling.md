# PROG 102 · Lecture 38
## Profiling

**Week 12 · Wednesday · 50 minutes**
**Reading:** `perf` documentation; Meyers Item 30 (inlining) · **Assumes:** every measurement week

**Date:** Wednesday 14 April 2027 · 10:00–10:50 · Week 12

---

## 1. The Rule

> **Measure before you optimise. Then measure again.**

You have been told this all semester and now it has a name and a tool.

**The reason is empirical:** programmers are consistently wrong about where time goes. The loop you are
staring at is where you *expect* the cost; the profile is where it *is*. Every measurement in this
course that surprised you — Week 3's insertion paradox, Week 4's three attempts, Week 8's
`std::function`, Week 11's self-deleting benchmark — was an instance of that gap.

**Amdahl's law** puts a bound on the argument:

> If a part takes fraction $p$ of the runtime, making it infinitely fast speeds the program by at most
> $1/(1-p)$.

**Optimising something that takes 5% of the time cannot gain you more than 5%**, however brilliant the
optimisation. Which is why you find the 60% first.

---

## 2. Two Kinds of Profiler

| | How | Cost | Distortion |
| --- | --- | --- | --- |
| **Sampling** (`perf`) | interrupts periodically, records where you are | ~1–5% | low |
| **Instrumenting** (`gprof`, Callgrind) | counts every call | 2–50× | **high** |

**Prefer sampling.** An instrumenting profiler changes the thing it measures: it makes small functions
disproportionately expensive, which can invert your ranking. Callgrind is superb for **counts** —
cache misses, instructions — and misleading for **time**.

---

## 3. Using `perf`

```
g++ -std=c++17 -O2 -g prog.cpp -o prog        # -O2 AND -g: optimised, with symbols

perf stat ./prog                               # summary counters
perf stat -e cache-misses,cache-references,instructions,cycles ./prog
perf record -g ./prog && perf report           # where the time goes, with call graphs
```

**`-O2 -g` together** is the combination people get wrong. Profile the optimised build — a `-O0` profile
tells you about a program you will never ship — and keep `-g` so the report names functions rather than
addresses.

### 3.1 Permissions

`perf` needs kernel access to hardware counters:

```
cat /proc/sys/kernel/perf_event_paranoid
sudo sysctl kernel.perf_event_paranoid=1
```

**Values of 2 or more restrict the counters** you need. **On the reference machine this is 4 and cannot
be changed**, which is why every number in Lecture 39 was obtained by timing instead.

> **That constraint turned out to be instructive.** Lecture 39's entire memory hierarchy — L1 through
> RAM, the cache line size, false sharing — was measured with `std::chrono` and a loop.
>
> **A profiler tells you *where* the time goes. A designed benchmark tells you *why*.** You need both,
> and only one of them requires permission.

---

## 4. Reading a Profile

```
  38.42%  prog  [.] Tree<int>::contains
  21.07%  prog  [.] operator new
  14.83%  libc  [.] _int_malloc
   9.12%  prog  [.] List<int>::push_back
```

**Three things to look for, in order:**

**Is the top entry what you expected?** If `contains` dominates and you thought insertion did, stop and
find out why before changing anything.

**Is allocation in the top five?** `operator new` and `_int_malloc` at 36% combined says the problem is
**how often you allocate**, not what you do afterwards. That is a design fix — `reserve`, fewer
temporaries, a different container — and it is usually the largest single win available.

**Is anything there that should not be?** A `memcpy` you did not write means something is copying;
`std::function`'s wrapper (Week 11) means an erased call in a hot path.

### 4.1 Self Time and Total Time

**Self** is time in the function itself; **total** includes what it called. A function with 2% self and
70% total is not slow — **something it calls is**, and `perf report -g` shows you which.

---

## 5. The Order of Operations

When a program is too slow:

1. **Measure.** Establish the baseline. Without it you cannot tell whether you helped.
2. **Profile.** Find where the time is.
3. **Ask about the algorithm first.** $O(n^2) \to O(n \log n)$ beats every micro-optimisation, and
   Week 3's containers are usually where that lives.
4. **Then ask about memory.** Allocation count and access pattern — Lecture 39.
5. **Then micro-optimise.** Rarely worth it, and the compiler is better at it than you.
6. **Measure again**, and keep the number.

> **Steps 3 and 4 are where the wins are, and step 5 is where the time is spent.** That inversion is
> the single most common failure in performance work.

### 5.1 And Know When to Stop

**A program that is fast enough is finished.** Optimisation costs readability, and readability is what
you will need next year. **Have a target before you start**, and stop when you meet it.

---

## 6. Benchmarking Honestly

This course has spent twelve weeks on this and it is worth collecting:

| Trap | Week | Fix |
| --- | --- | --- |
| The compiler deletes the loop | 2, 5, 10, **11** | Consume the result; make inputs unhoistable |
| Measuring something other than what you named | **4** | Control for size, layout, storage |
| Right measurement, wrong explanation | **2** | Run a control |
| Right theory, wrong question | **3** | Measure the operation you actually perform |
| First run is slowest | **6** | Warm up, or discard it |
| A single run | **4, 10** | Three minimum; report the spread |
| A ratio with no denominator | **11** | Say what it is a fraction of |
| Timing a sanitizer build | every lab | Never |

**Every one of those produced a wrong answer in this course**, in materials written by someone who knew
the trap existed. **That is the point of the list.**

---

## 7. Summary

| Idea | The point |
| --- | --- |
| Measure before optimising | Programmers are consistently wrong about where time goes |
| **Amdahl's law** | 5% of the runtime bounds your gain at 5% |
| Sampling vs instrumenting | Prefer sampling; instrumenting distorts what it measures |
| `-O2 -g` | Optimised build, with symbols |
| `perf_event_paranoid` | Needs to be ≤1; **4 on the reference machine** |
| A profiler says **where**; a benchmark says **why** | Only one needs permission |
| Allocation in the top five | A design problem, and usually the biggest win |
| Self vs total time | 2% self, 70% total means look at the callees |
| Order | measure → profile → **algorithm** → **memory** → micro → measure |
| Know when to stop | Fast enough is finished |

---

## 8. Exercises

**1.** Check your `perf_event_paranoid`. **If it is above 1, report what `perf stat` refuses to do.**
Then do exercise 3 by timing instead.

**2.** Profile your Project 2 test suite with `perf record -g`. **Report the top five entries.** Was the
top one what you expected?

**3.** Find the allocation count in one Project 2 operation, either from `perf` or by instrumenting
`operator new`. **Then reduce it** and measure the improvement.

**4.** Take a function taking 5% of your runtime and make it **twice** as fast. **Measure the whole
program's improvement** and compare with Amdahl's bound.

**5.** Profile the same program at `-O0` and `-O2`. **Report both top-five lists.** How much would the
`-O0` profile have misled you?

**6.** Build a benchmark that falls into one of §6's traps **on purpose**, then fix it. Report both
numbers.

**7.** Take the slowest operation in Project 2 and write down, **before profiling**, where you think
the time goes. Then profile. **Report both, including how wrong you were.**

---

## 9. Next

**Lecture 39** is the last of this course. It measures the memory hierarchy directly and settles a
question that has been open since **Week 3** — and the answer turns out not to be the one Week 3 gave
you.

---

*PROG 102 · Week 12 · Lecture 38 · © CSE Department*
