# PROG 102 · Lab 11
## Profiling Lambda Overhead

**Week 11 · 2-hour lab session · 40 points**
**Deliverable:** `bench.cpp`, `RESULTS.md`. In-lab checkoff.

> **Project 2 is due next Friday and the final is that week.** This lab is short and its results feed
> directly into Project 2 Part 3.3.

---

## Purpose

Week 8 measured `std::function` as the slowest of four ways to pass a comparison to `std::sort` and
attributed it to type erasure. **This lab measures the mechanism directly**, at the level of a single
call, and finds a second cost that benchmark could not see.

You will also meet — for the fourth time this course — a benchmark that reports **zero** because the
compiler deleted it. **By now you should expect that**, and Part A is built so that you have to handle
it.

> `-O2` for every timing, three runs minimum, machine and compiler at the top of `RESULTS.md`.

---

## Part A — Three Ways to Call (14 pts)

**A1.** *(5)* Call the same trivial lambda 10⁸ times, three ways: **directly**, through a **function
pointer**, and through a **`std::function`**.

**Your first attempt will report 0.00 ns for at least two of them.**

- **(a)** *(2)* Report that result and say which versions vanished.
- **(b)** *(3)* Explain why the `std::function` version survived when the others did not.

**A2.** *(6)* Fix it so all three are measured. **Make the arguments unhoistable** — index into a data
array, use the loop counter, or both.

Report **ns per call** for all three, three runs each. State what you changed.

**A3.** *(3)* Compute the ratios against the direct lambda.

**Explain why the function pointer sits between the other two**, in two sentences.

---

## Part B — The Hidden Allocation (12 pts)

**B1.** *(6)* Instrument `operator new` to count allocations. Then construct a `std::function` from
lambdas capturing 1, 8, 16, 17, 24 and 32 bytes.

**Report the exact capture size at which allocation begins**, and `sizeof(std::function<int()>)`.

**B2.** *(3)* Capture a `std::string` by value and report whether it allocates. Then capture it **by
reference** and report again.

**Explain the difference in one sentence** — and say what the by-reference version risks.

**B3.** *(3)* Build a `std::vector<std::function<void()>>` with five lambdas of varying capture size.

**Report the total allocations**, and describe one change that would reduce it.

---

## Part C — Does It Matter? (10 pts)

**C1.** *(6)* Take a realistic operation — sorting 10⁶ elements, or applying a transform — and run it
with the comparator/operation passed **as a template parameter** and **as a `std::function`.**

Report both times and the ratio.

**C2.** *(4)* Your A3 ratio (per bare call) and your C1 ratio (inside real work) **will differ
substantially.**

- **(a)** *(2)* Report both.
- **(b)** *(2)* **Both are correct.** Explain, and say which one you would quote to a colleague asking
  "is `std::function` slow?"

---

## Part D — The Rule (4 pts)

**D1.** *(2)* From your own numbers, state in one sentence when `std::function` is the wrong choice.

**D2.** *(2)* Give a concrete case from **your Project 1 or Project 2 code** where `std::function` is
the **right** choice, and say what a template parameter could not do there.

---

## Submission

- `bench.cpp` and any headers.
- `RESULTS.md` — all tables, the A1 failure, and every written answer.
- Machine, OS, compiler version at the top.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 14 | Three call mechanisms, including the benchmark that deleted itself |
| B | 12 | The small-buffer threshold, found rather than looked up |
| C | 10 | The same question at two scales, both answered |
| D | 4 | The rule, from your own data |
| **Total** | **40** | |

---

## Reference Numbers

g++ 13.3.0, x86-64 Linux, `-O2`.

**A1 — the first attempt**, constant arguments:

```
lambda    0.0 ms (0.000 ns) | std::function  441.1 ms (2.206 ns) | fn ptr    0.0 ms (0.000 ns)
```

**A2 — with unhoistable arguments**, 10⁸ calls:

| run | lambda | function pointer | `std::function` |
| --- | --- | --- | --- |
| 1 | 0.667 ns | 1.507 ns | 2.205 ns |
| 2 | 0.610 ns | 1.499 ns | 2.153 ns |
| 3 | 0.606 ns | 1.539 ns | 2.209 ns |

**Ratios:** function pointer ≈ **2.4×**, `std::function` ≈ **3.5×**.

**B1:**

```
sizeof(std::function<int()>) = 32

capture   1 bytes -> allocations 0
capture   8 bytes -> allocations 0
capture  16 bytes -> allocations 0
capture  17 bytes -> allocations 1   <- HEAP
capture  32 bytes -> allocations 1   <- HEAP
```

**Threshold: 16 bytes.**

**For comparison — Week 8, inside `std::sort` on 2,000,000 ints:** lambda 160 ms, `std::function`
296 ms — **1.85×**, not 3.5×.

---

## What This Lab Is Really Showing

**Part C2 is the point, and it is a lesson about quoting numbers.**

You will measure `std::function` at about **3.5× a lambda per call**, and at about **1.85×** inside a
real sort. Both are correct measurements of the same thing at different scales, and **which one you
quote changes what your colleague does.**

Say "3.5×" and they will rewrite working code to avoid `std::function`. Say "1.85% of your sort time"
— because the comparison is a small part of sorting — and they will leave it alone. **The honest answer
is the one that includes the denominator**: 3.5× *of the call*, which is 1.85× *of the sort*, which may
be 0.1% *of the program*.

That is this course's argument in its final form. Week 2 asked what a measurement was *of*. Week 4
asked what your benchmark was *measuring*. **Week 11 asks what fraction of the thing you actually care
about it represents** — and a ratio with no denominator is not an answer.

**And Part A is the fourth time a benchmark has deleted itself.** Week 2's template instantiation,
Week 5's leaked allocation, Week 10's hoisted counter, and now this. By now the reflex should be
automatic: **a suspiciously good number means check the assembly, not celebrate.**

---

*PROG 102 · Week 11 · Lab 11 · © CSE Department*
