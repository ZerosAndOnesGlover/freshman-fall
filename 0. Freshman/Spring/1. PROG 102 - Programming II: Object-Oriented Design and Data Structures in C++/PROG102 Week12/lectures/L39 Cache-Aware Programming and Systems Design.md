# PROG 102 · Lecture 39
## Cache-Aware Programming and Systems Design

*“...we do not consider it as good engineering practice to consume a resource lavishly just because it happens to be cheap.”* — Niklaus Wirth, *Project Oberon* (2013), §2.3

**Week 12 · Thursday · 50 minutes · The last lecture**
**Reading:** Drepper, *What Every Programmer Should Know About Memory* · **Assumes:** Weeks 3, 6, 10, 11

**Date:** Thursday 15 April 2027 · 10:00–10:50 · Week 12

**Coursework:** 📋 **Project 2** due Fri 16 Apr 17:00 · 📝 **PS 11** due Fri 16 Apr 17:00 · 🔬 **Lab 12** Mon 19 Apr 15:00–16:50 · 📕 **Final exam** Thu 22 Apr 14:00–16:30

---

## 1. The Question From Week 3

**Week 3 §L11 §3.1** measured `std::list` traversing **6.3× slower** than `std::vector` at identical
$O(n)$ complexity. **Week 6** found the same gap — 7–10× — between a student list and a vector. The
explanation given was "memory layout", with a promise that Week 12 would measure it.

**Here is the measurement.**

---

## 2. The Memory Hierarchy

A pointer chase through a random cycle, with the working set growing. **Nothing changes but the size:**

| working set | ns per access | region |
| --- | --- | --- |
| 4 KB | 1.73 | **L1** |
| 16 KB | 1.52 | L1 |
| 32 KB | 1.51 | L1 |
| 64 KB | 2.82 | **L2** |
| 128 KB | 3.53 | L2 |
| 256 KB | 5.16 | L2 |
| 512 KB | 9.35 | **L3** |
| 1 MB | 12.36 | L3 |
| 4 MB | 26.86 | L3 |
| 16 MB | **108.84** | **RAM** |
| 64 MB | **137.60** | RAM |

**The same instruction, ninety times slower**, depending only on where the data is.

**The plateaus and the cliffs are the caches.** L1 ends around 32 KB — 1.51 ns becomes 2.82 the moment
the working set exceeds it. The next step is at a few hundred kilobytes, the next at a few megabytes,
and then you are in main memory paying **more than 100 ns per access.**

> **Measured with `std::chrono` and a loop.** No profiler, no privileges, no hardware counters. **A
> designed benchmark reveals structure a profiler would only have confirmed.**

---

## 3. The Cache Line

Memory does not move a byte at a time. **The unit is a cache line — 64 bytes on x86-64**, and the
language will tell you:

```cpp
std::hardware_destructive_interference_size    // 64
```

Reading one `int` fetches 64 bytes. **Reading the next 15 `int`s is then free.** That is **spatial
locality**, and it is the entire advantage of contiguous storage.

Striding through 64 MB, touching one element every *n* bytes:

| stride | ns per **touched** element |
| --- | --- |
| 4 B | 0.79 |
| 8 B | 0.81 |
| 16 B | 1.18 |
| 32 B | 2.15 |
| **64 B** | **4.04** |
| 128 B | 7.14 |
| 512 B | 8.99 |

**Below 64 bytes, consecutive accesses share a line and the cost per element is tiny.** At 64 bytes and
beyond, every access is its own line and you pay the full price.

**The two localities:**

- **Spatial** — you will soon want data *near* what you just used. Contiguous arrays exploit it.
- **Temporal** — you will soon want the *same* data again. It is still in cache.

---

## 4. The Experiment That Corrects Week 3

Week 3 blamed the container. **That was almost right.**

The same **1,000,000 integers**, traversed three ways:

| | time | vs sequential |
| --- | --- | --- |
| `std::vector`, in order | 4.6–6.9 ms | 1.0× |
| `std::list` | 60.5–71.7 ms | **10–13×** |
| **`std::vector`, in random order** | 57.8–66.7 ms | **8.4–14.5×** |

**The third row is the whole lecture.**

That is a `std::vector` — contiguous, one allocation, perfect layout — read through a shuffled index
array. **It is as slow as the linked list.** Same container, same memory, same data. Only the *order*
differs.

> **It was never about the container.** A `std::vector` is not fast because it is a vector; **it is
> fast because you usually walk it in order.** A `std::list` is not slow because it is a list; **it is
> slow because it makes walking in memory order impossible.**
>
> **The container determines what access patterns are available to you. The access pattern determines
> the speed.**

**This also explains Week 6's result**, where a hand-written list matched `std::list` to within 15%:
both were doing the same thing to memory, and no amount of implementation skill changes that.

---

## 5. False Sharing — and Week 10 Explained

Four threads, each incrementing **its own** counter. Nothing is shared.

```cpp
struct Packed { std::atomic<long> c{0}; };                 // 8 bytes -- 8 per cache line
struct Padded { alignas(64) std::atomic<long> c{0}; };     // 64 bytes -- one per line
```

| threads | packed | padded | ratio |
| --- | --- | --- | --- |
| 1 | 151.5 ms | 107.0 ms | 1.4× |
| 2 | 587.5 ms | 108.1 ms | **5.4×** |
| 4 | **1617.7 ms** | **110.0 ms** | **14.7×** |

**The padded version does not slow down at all** — 107, 108, 110 ms. Perfect scaling.

**The packed version gets 10× worse from one thread to four**, and the counters were never shared. They
merely **sat in the same 64-byte line**, and a cache line is the unit of coherence: when one core writes
it, every other core's copy is invalidated.

**This is false sharing**, and it is the same phenomenon as **Week 10 §L33 §2**, where a `shared_ptr`
copy went from 17 ns to 57 ns under four-thread contention. The reference count is one line, and four
cores were fighting over it.

> **The fix is padding, and the cost is memory.** `alignas(64)` on a per-thread counter turns a 14.7×
> penalty into nothing — at 8× the space. **That trade is almost always worth it for per-thread state,
> and almost never worth it for anything else.**

---

## 6. Data Layout

**Array of structs** — the obvious layout:

```cpp
struct Particle { float x,y,z, vx,vy,vz, mass, charge; };   // 32 bytes
std::vector<Particle> particles;
```

**Struct of arrays** — one array per field:

```cpp
struct { std::vector<float> x, y, z, vx, vy, vz, mass, charge; } particles;
```

Summing **one field of eight** over 4,000,000 particles:

| | time | |
| --- | --- | --- |
| array-of-structs | 8.90–10.37 ms | |
| struct-of-arrays | 5.48–5.88 ms | **1.5–1.8× faster** |

**Because AoS wastes the line.** `sizeof(Particle)` is 32 bytes, so a 64-byte line holds two particles —
and if you only want `x`, you fetched 64 bytes to use 8. **SoA fetches 64 bytes of `x`.**

Summing **all eight fields**:

| | time |
| --- | --- |
| array-of-structs | 13.79–15.87 ms |
| struct-of-arrays | 10.74–14.28 ms |

**SoA's advantage narrows from ~1.6× to ~1.2× — but does not reverse**, on this machine.

> **The textbook says AoS should win when you touch every field.** It did not here, and the honest
> report is: **the direction of the effect is confirmed and the crossover is not.** Eight sequential
> streams still prefetch well; the tie-break would need more fields, a larger struct, or a
> less-predictable pattern.
>
> **Which is a fitting last measurement for this course.** The mechanism is real, the direction is
> right, and the specific claim you were going to repeat did not survive contact with a benchmark.

---

## 7. Practical Rules

From all of the above, in order of how often they matter:

1. **Prefer contiguous storage.** `std::vector` unless you can name a reason.
2. **Walk in memory order.** A sorted traversal of a random index array is §4's third row.
3. **Reduce allocations.** Each one scatters. `reserve` when you know the size.
4. **Keep hot data small and together.** A struct split into hot and cold halves often beats one big
   struct.
5. **Pad per-thread state** to a cache line. Nothing else.
6. **Then measure**, because §6 is what happens when you reason from the rules alone.

---

## 8. Designing a System

The last topic, briefly, because it does not reduce to a measurement.

**A medium-sized system is organised by drawing boundaries.** A good boundary:

- **hides a decision that might change** — the container, the file format, the protocol;
- **is narrow** — few functions, simple types;
- **is testable in isolation** — which is L37's argument, arriving as an architectural one.

**You have been doing this all term.** Week 6's container hid its representation behind an iterator.
Week 7's Facade hid a subsystem. Week 9's contracts *were* the boundaries, written down.

> **The two principles from Week 7 §L22 §3 are the whole of architecture at this scale**: *program to
> interfaces*, so a component can be replaced; and *favour composition*, so the dependency graph stays
> a graph rather than a hierarchy.
>
> **And the honest limit:** nobody can tell you where the boundaries go from a description of the
> problem. You find out by building it, getting it wrong, and moving them — which is why Project 2 asks
> what you would do differently, and why that question is worth 6 marks.

---

## 9. Summary

| Idea | The point |
| --- | --- |
| The hierarchy | **1.5 ns (L1) → 138 ns (RAM)** — about **90×** |
| Measured by timing alone | No profiler, no privileges |
| Cache line = **64 bytes** | `hardware_destructive_interference_size` |
| Spatial locality | Below a 64 B stride, accesses share a line |
| **Week 3's answer was almost right** | It is the **access order**, not the container |
| The proof | A `vector` read in random order is **as slow as a list** |
| **False sharing** | 14.7× at four threads, on counters that are never shared |
| Padding fixes it | 107 → 110 ms across 1–4 threads: flat |
| This is Week 10's `shared_ptr` | The refcount is one line, and four cores fought over it |
| SoA vs AoS | **1.5–1.8×** for one field; narrows to ~1.2× for all eight |
| The textbook crossover | **Did not appear.** Direction confirmed, claim not |
| Architecture | Boundaries hide decisions that might change |

---

## 10. Exercises

**1.** Reproduce §2's hierarchy sweep on your machine. **Identify your L1, L2 and L3 sizes** from where
the cliffs are, and check them against `lscpu`.

**2.** Reproduce §3's stride sweep. **Find your cache line size** from the data alone, then confirm with
`std::hardware_destructive_interference_size`.

**3.** Reproduce §4's three-way traversal. **Report all three.** Then explain in three sentences why the
third row means Week 3's explanation needed correcting.

**4.** Reproduce §5's false sharing at 1, 2, 4 and 8 threads. **Report the ratios**, then connect it to
Week 10's `shared_ptr` measurement in two sentences.

**5.** Build the AoS/SoA comparison. **Find the number of fields at which AoS catches up** on your
machine — or report that it does not, with your data.

**6.** Take the hottest loop in Project 2 and change one thing about its **memory access pattern**.
Measure before and after. **Report both, even if you made it slower.**

**7.** Sketch the architecture of a system with three components, one of which you expect to replace.
**Draw the boundary that makes the replacement cheap**, and say what it costs you elsewhere.

---

## 11. The End

That is the course.

You started in Week 0 by proving that a member function is an ordinary function with a hidden first
argument, by reading the assembly. You are ending by proving that a `std::vector` is not fast because
it is a `std::vector`, by timing a shuffle.

**Both are the same activity**, and it is the one thing this course was actually about: **go and look.**

The `Course Retrospective` in `resources/` says the rest.

---

*PROG 102 · Week 12 · Lecture 39 · © CSE Department*
