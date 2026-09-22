# PROG 102 · Lab 6 — Solutions and Checkoff Notes
## Benchmarking Against `std::list`

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**This lab depends on PS 6 working.** Ask at the start who does not have a functioning `List<T>` and
deal with them first — a student debugging their list for ninety minutes gets nothing from the session.

**Have a reference `list.hpp` available** for students whose own is broken. They lose the Part A
comparison's personal meaning but can still do B, C and D, which are where the ideas are.

**Three things to say up front:**

1. **`-O2`, never a sanitizer build, three runs minimum.** Fifth time of asking; it still catches
   people.
2. **The first run of the first container is always slow.** Allocator warm-up. Part A2 asks about it
   deliberately — do not let them "fix" it by deleting the run.
3. **Part C is the point of the lab.** Budget for it: A 35 min, B 30 min, C 35 min.

---

> **Revised 2026-09-22.** Part C (`splice`) was removed: `splice` is never taught in Lectures 19–21. Old Part D is Part C;
> points re-weighted to keep 40.

## Part A — The Comparison (16)

### A1 (10)

Reference, n = 1,000,000:

| run | build (ours / std) | traverse | copy |
| --- | --- | --- | --- |
| 1 | 58.7 / 28.6 ms | 3.6 / 2.8 | 55.2 / 26.7 |
| 2 | 25.6 / 28.7 ms | 5.0 / 4.5 | 27.8 / 35.2 |
| 3 | 24.6 / 26.3 ms | 4.0 / 3.0 | 28.2 / 27.1 |

*Marking: 8 for nine numbers per container with three runs. **Absolute times vary hugely by machine** —
mark that the two containers are close, not the values.*

### A2 (3)

Run 1 is slower for whichever container runs first. **Allocator warm-up**: the first million
allocations in a process force the heap to grow, and that cost lands on whoever goes first.

Acceptable responses: discard the first run, run a warm-up pass before timing, or alternate the order
and report both.

*Marking: 3. **A student who instead concluded "my list is 2× slower than std::list" from run 1 alone**
gets 1, and this is worth discussing with them — it is the same single-run error as Week 4's dispatch
benchmark.*

### A3 (3)

Expected: the two are within noise of each other, because both allocate one node per element and chase
pointers to traverse. **There is very little room for either to be cleverer.**

*Marking: 3. **If a student reports their list as decisively faster, check what they measured** — the
usual causes are a missing `-O2` on the `std::list` build, timing a debug STL, or a list that is not
actually deep-copying in the copy test. A student who investigated and found the cause gets full marks
regardless of the outcome.*

---

## Part B — Where the Time Goes (14)

### B1 (7)

Reference, n = 1,000,000 × 10 passes:

| run | your `List` | `std::list` | `std::vector` | list/vector |
| --- | --- | --- | --- | --- |
| 1 | 70.0 | 67.0 | 7.3 | 9.2× |
| 2 | 72.7 | 66.6 | 9.3 | 7.2× |
| 3 | 66.5 | 57.2 | 5.7 | 10.1× |

*Marking: 6 for all three containers, three runs. Accept 4×–15× for the list/vector ratio.*

### B2 (7) — the assessed question

The answer must account for **both** facts:

> **The vector wins because its elements are contiguous** — one memory fetch brings in many elements,
> and the prefetcher can predict the access pattern. A list's nodes are separate allocations scattered
> across the heap, so each element is an independent trip to memory that cannot be predicted.
>
> **The two lists tie because they are the same design.** Both allocate one node per element and follow
> `next` to traverse. Neither implementation is cleverer than the other; the layout dominates, and they
> have the same layout.

*Marking: 3 for the vector explanation, 3 for the tie. **A student who explains only the vector gap has
answered half the question** — the tie is the more interesting half, because it says the difference is
structural rather than about code quality.*

---

## Part C — Make It Lie (10)

### C1 (6)

| n | `std::sort` | sorted correctly? |
| --- | --- | --- |
| 1,000 | 8.58 ms | yes |
| 2,000 | 39.44 ms | yes |
| 4,000 | 194.39 ms | yes |

*Marking: 4. **The "correctly sorted" column is essential** — a student who did not check it has missed
what makes the result alarming.*

### C2 (4)

About **4.8× per doubling** → $O(n^2 \log n)$. Sorting should be $O(n \log n)$, which would be about
2.2× per doubling.

**Which is worse?** The operator that exists and is quadratic. An absent operator is a compile error
found in a minute; a dishonest one is a performance bug found in production, by a customer, with a
large dataset.

*Marking: 1 the complexity, 1 the judgement. Both halves required.*

---

## Checkoff Checklist

1. `-O2`, three runs, no sanitizer builds timed.
2. A2 identifies allocator warm-up rather than deleting the run.
3. B2 explains **both** the vector gap and the list tie.
4. C1 reports that the lying sort produced **correct** output.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 16 |
| B | 14 |
| C | 10 |
| **Total** | **40** |

---

## Note for the Lab

Close on Part C, and make the contrast with every previous lab explicit.

> **Labs 2 through 5 measured what things cost.** A template instantiation, a virtual call, a
> `shared_ptr` copy. **Today you measured what a lie costs.**

Then the part worth the last five minutes:

> Look at what did *not* happen in Part C. Nothing crashed. No sanitizer fired. Every result was
> correctly sorted. The program was right and about a thousand times too slow — and **not one tool this
> course has given you would have found it.**

That is a genuinely uncomfortable place to leave them, and it should be, because the resolution is not
a better tool:

> The only thing that catches it is declaring a category you can honour and letting the algorithm
> refuse you. **The compile error you spent Part B being annoyed by is the feature.**

If there is time, connect it forward: **Project 1 marks them for their container failing to compile
with `std::sort`**, and Part 5.1 asks them to name two operations they deliberately did not implement.
Both are this lesson, cashed in.

---

*PROG 102 · Week 6 · Lab 6 Solutions · © CSE Department*
