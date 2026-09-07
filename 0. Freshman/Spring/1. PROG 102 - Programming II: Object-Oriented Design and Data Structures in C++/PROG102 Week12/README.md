# PROG 102 · Programming II — Object-Oriented Design and Data Structures in C++
## Week 12: Software Engineering — Testing, Profiling, and Systems Design

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), CS 101
**Assessment for this course (overall):** Labs 20%, Problem Sets 30%, Midterms 25%, Final 15%, Projects 10%
**This week:** Lab 12 (your Project 2 demo) · **PROJECT 2 DUE** · **FINAL EXAM**
**No problem set and no quiz this week.**

---

### Why This Week Exists

To answer a question the course has been deferring since **Week 3**.

You measured `std::list` traversing **6.3× slower** than `std::vector` at identical $O(n)$ complexity,
and were told the reason was "memory layout" and that Week 12 would measure it. In **Week 6** your own
list matched `std::list` and both lost to `vector` by 7–10×. In **Week 10** a `shared_ptr` copy went
from 5.9 ns to 57 ns under four-thread contention, and the explanation was deferred again.

**All three are the same phenomenon**, and this week measures it directly.

The week also covers what to do with the rest of your life as a programmer: how to test, how to find
out where the time actually goes, and how to arrange a system larger than one file.

### The Measurement the Course Has Been Building To

**The memory hierarchy, measured by timing alone:**

| working set | ns per access |
| --- | --- |
| 4–32 KB (L1) | **1.5–1.7** |
| 64–256 KB (L2) | 2.8–5.2 |
| 512 KB–4 MB (L3) | 9.4–26.9 |
| 16–64 MB (RAM) | **109–138** |

**About ninety times**, from the fastest to the slowest, with no change in the number of operations.

### And the Experiment That Settles It

Week 3 blamed the container. **That was almost right and not quite.** The same 1,000,000 integers,
traversed three ways:

| | time | vs sequential |
| --- | --- | --- |
| `std::vector`, in order | 4.6–6.9 ms | 1.0× |
| `std::list` | 60.5–71.7 ms | **10–13×** |
| **`std::vector`, in random order** | 57.8–66.7 ms | **8.4–14.5×** |

**The contiguous vector, accessed out of order, is as slow as the linked list.** Same allocation, same
data, same container — only the access pattern differs.

> **It was never about the container. It is about the order in which you touch memory**, and a linked
> list is simply a data structure that makes a bad order unavoidable.

### Learning Objectives

By the end of Week 12, you should be able to:

1. Write unit tests that check failure as well as success, and explain TDD's actual claim.
2. Profile a program and find where the time goes — **rather than where you assumed it went.**
3. Describe the memory hierarchy with measured numbers.
4. Explain cache lines, spatial and temporal locality.
5. **Demonstrate that access order, not container type, causes the vector/list gap.**
6. Recognise and fix **false sharing** — and connect it to Week 10's `shared_ptr` figure.
7. Choose a data layout (array-of-structs against struct-of-arrays) for a given access pattern.
8. Sketch the architecture of a medium-sized system and defend the boundaries.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L37 Testing and Test-Driven Development]] | Unit tests, TDD, what coverage does and does not tell you |
| [[L38 Profiling]] | `perf`, sampling vs instrumentation, and finding the real hot spot |
| [[L39 Cache-Aware Programming and Systems Design]] | **The memory hierarchy, measured** — and how to arrange a system |
| [[LAB 12 Project Demo and Code Review]] | Present Project 2; review someone else's |
| [[PROG102 Week12/resources/FINAL EXAM Revision Guide\|FINAL EXAM Revision Guide]] | **Comprehensive, Weeks 0–12** |
| [[PROG102 Week12/resources/Course Retrospective\|Course Retrospective]] | What this course argued, and what to read next |
| [[PROG102 Week12/resources/Reading Guide Week 12\|Reading Guide Week 12]] | And every command to reproduce this week |
| [[PROG102 Week12/solutions_instructor/LAB 12 Solutions\|LAB 12 Solutions]] | Instructor only |

### A Note on `perf`

Lecture 38 uses `perf`, and on many Linux systems it needs a one-time permission change:

```
cat /proc/sys/kernel/perf_event_paranoid      # if this is 2 or more, counters are restricted
sudo sysctl kernel.perf_event_paranoid=1
```

**On the reference machine this setting is 4 and cannot be changed**, so every measurement in Lecture
39 was obtained by **timing alone**, which needs no privileges and no tools.

**That is deliberate and worth noticing:** the entire memory hierarchy above was measured with
`std::chrono` and a loop. **You do not need a profiler to see the hierarchy — you need a benchmark
designed to reveal it.**

### Everything Is Due This Week

- **Project 2** — Friday.
- **Lab 12** — your demo and a code review of someone else's project.
- **The final exam** — comprehensive, 180 minutes, two handwritten sheets.

**The revision guide is in `resources/` and you should read it now.**

---

*PROG 102 · Week 12 · © CSE Department*
