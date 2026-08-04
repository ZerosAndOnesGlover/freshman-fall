# PROG 102 · Week 12 · Reading Guide
## The Last One

---

## What to Read

| Source | Why |
| --- | --- |
| **Drepper, *What Every Programmer Should Know About Memory*** | Free online. **Lecture 39 is a summary of its first three parts.** |
| **`perf` wiki / `man perf-stat`** | The tool, properly |
| **Meyers, *Effective Modern C++*** Item 30 | Inlining, and why the compiler ignores you |
| **cppreference:** `hardware_destructive_interference_size` | The language's own statement of the cache line |

> **Drepper is 114 pages and worth every one**, but not this week. **Read sections 3.1–3.3** (cache
> operation) now, and the rest when the final is behind you. It is the reference for everything
> Lecture 39 measured.

---

## Guiding Questions

**On memory:**

1. Drepper §3.1 — why is memory organised in **lines** rather than bytes? What would a byte-granular
   cache cost?
2. §3.3 — he measures working-set sweeps like Lecture 39 §2. **Compare his curve with yours.** How
   have the numbers changed since 2007, and how have the *ratios*?
3. What is a **prefetcher**, and why does a sequential access pattern benefit from one while a random
   pattern does not? *(This is Lecture 39 §4's third row.)*
4. Look up **cache associativity**. Construct a stride that would be pathological on an 8-way cache.

**On profiling:**

5. `man perf-stat` — find `cache-misses` and `cache-references`. **What is the ratio called, and what
   is a bad value?**
6. Why does `perf record` need `-g` for call graphs, and what does `--call-graph dwarf` change?

**On the last question:**

7. Meyers Item 30 lists cases where `inline` is ignored. **Which of them apply to a virtual call?**
   *(Week 4 §L14 §6 measured GCC working around one of them.)*

---

## Reproducing This Week's Measurements

**g++ 13.3.0, x86-64 Linux.** These are hardware-dependent — **your cliffs will be at your cache
sizes**, not the reference machine's. Check with `lscpu`.

### L39 §2 — The hierarchy

```
g++ -std=c++17 -O2 -Wall -Wextra hierarchy.cpp -o hier && ./hier
lscpu | grep -i cache
```

**Expect:** a flat region up to your L1 size, then steps at L2 and L3, then a plateau at RAM latency.
Reference: **1.5 ns → 138 ns**.

### L39 §3 — The cache line

```
g++ -std=c++17 -O2 -Wall -Wextra line.cpp -o line && ./line
```

**Expect:** per-touched-element cost roughly doubling up to a 64-byte stride, then flattening.

### L39 §4 — The experiment that corrects Week 3

```
g++ -std=c++17 -O2 -Wall -Wextra vl.cpp -o vl && ./vl
```

**Expect:** vector 4.6–6.9 ms, list 60–72 ms, **vector-in-random-order 58–67 ms**.

**This is the one to run if you run only one.**

### L39 §5 — False sharing

```
g++ -std=c++17 -O2 -Wall -Wextra -pthread false_sharing.cpp -o fs && ./fs
```

**Expect:** padded flat across thread counts; packed degrading to ~14.7× at four threads.

### L39 §6 — AoS vs SoA

```
g++ -std=c++17 -O2 -Wall -Wextra aos_soa.cpp -o as && ./as
```

**Expect:** SoA ahead by ~1.6× on one field, narrowing to ~1.2× on all eight. **Report what you get** —
the crossover is machine-dependent and did not appear here.

### `perf`, if you can

```
cat /proc/sys/kernel/perf_event_paranoid
sudo sysctl kernel.perf_event_paranoid=1
perf stat -e cache-misses,cache-references ./vl
```

**On the reference machine this is 4 and cannot be changed**, so every number above was obtained by
timing. **If you can run `perf`, do** — seeing the miss counts move with the access pattern is worth
the setup.

---

## The Last Word on Method

Twelve weeks of this reading guide have said some version of *go and check*. Here is the summary, and
it is the most useful page in the course.

**The traps, all of which caught these materials:**

| Trap | Where it bit | The fix |
| --- | --- | --- |
| The compiler deletes the loop | W2, W5, W10, W11 | Consume the result; unhoistable inputs |
| Measuring something else | W4 (three attempts) | Control for size, layout, storage |
| Right number, wrong explanation | W2 | Run a control |
| Right theory, wrong question | W3 | Measure what you actually do |
| Warm-up in run 1 | W6 | Discard it, or warm up |
| A single run | W4, W10 | Three minimum; report the spread |
| A ratio with no denominator | W11 | Say what it is a fraction of |
| Asserting the textbook | W4, W12 | The crossover is empirical |

**Notice the pattern.** None of these were caught by care. **All of them were caught by running one
more experiment** — a control, a second optimization level, a different denominator, a swept parameter.

> **The discipline is not "be careful". It is "run the other one".**

---

## After the Exam

The **Course Retrospective** in this folder has the reading list and the honest account of what you do
and do not now know. **Read it after the final**, not before — it is not revision.

---

## This Week

1. **Project 2 due Friday.**
2. **Lab 12** — your demo, and a review of someone else's.
3. **The final exam.** Its guide is in this folder and Section C comes from Project 2.

Good luck. **Go and look.**

---

*PROG 102 · Week 12 · Reading Guide · © CSE Department*
