# PROG 102 · Lab 6
## Benchmarking Against `std::list`

**Week 6 · 2-hour lab session · 40 points**
**Deliverable:** `bench.cpp`, `RESULTS.md`. In-lab checkoff.

**Bring your `List<T>` from PS 6.** If it is not working, the first twenty minutes of this session are
for fixing it — tell your TA at the start rather than at the end.

---

## Purpose

You have written a linked list. `std::list` is a linked list. **How close did you get, and where does
the difference come from?**

The honest expected answer is *very close* — both allocate one node per element and chase pointers to
traverse, so there is not much room for either to win. **Where a large gap appears, it is almost always
a design difference rather than a skill difference**, and finding which one is the lab.

Part D then does something none of the previous labs have: **you will make your container lie**, and
measure what the lie costs.

> `-O2` for every timing, **never a sanitizer build**, three runs minimum, machine and compiler at the
> top of `RESULTS.md`.

---

## Part A — The Comparison (14 pts)

**A1.** *(8)* Benchmark `List<int>` against `std::list<int>` at n = 1,000,000 for:

- **build** — `push_back` n elements;
- **traverse** — sum every element;
- **copy** — copy-construct the whole container.

**Three runs each.** Report all nine numbers per container.

**A2.** *(3)* Your **first** run will probably be slower than the rest, for both containers. **Report
it and say why** — then say what you did about it.

**A3.** *(3)* Interpret the comparison in three sentences. **If your list is faster than `std::list` at
anything, treat that as a bug in the benchmark until proven otherwise** and say what you checked.

---

## Part B — Where the Time Goes (12 pts)

**B1.** *(6)* Traversal is the interesting one. Compare three containers at n = 1,000,000:

| | your `List<int>` | `std::list<int>` | `std::vector<int>` |
| --- | --- | --- | --- |

Report all three traversal times.

**B2.** *(6)* The vector will be several times faster than both lists, and the two lists will be close.

**Explain the pattern in four sentences.** Your explanation must account for **both** facts: why the
vector wins by a lot, and why the two lists are nearly identical.

*(Week 3 §L11 §3.1 measured the vector/list gap. Week 12 measures the cause directly. You are expected
to give the mechanism, not the number.)*

---

## Part C — Operations a List Is For (8 pts)

**C1.** *(5)* Implement `splice` if you have not — moving a range of nodes from one list to another by
**relinking**, with no allocation.

Benchmark splicing 100,000 elements between lists against the equivalent on `std::vector`
(erase from one, insert into another).

**Report both**, and the ratio.

**C2.** *(3)* This is the case where a linked list wins decisively. **In two sentences, say why**, and
connect it to Week 3's insertion paradox — specifically, **which half of that paradox this is.**

---

## Part D — Make It Lie (6 pts)

**D1.** *(4)* Change your iterator's `iterator_category` to `random_access_iterator_tag` and implement
`+`, `-`, `<` and `[]` **by looping**. About seven lines.

`std::sort` will now compile on your list. **Run it at n = 1,000, 2,000 and 4,000** and report the
times and whether the output is correctly sorted.

**D2.** *(2)* Report the ratio between successive sizes. **What complexity did you get, and what should
sorting be?**

Then answer in one sentence: **which is worse — an operator that does not exist, or one that exists and
is quadratic?**

---

## Submission

- `bench.cpp` and any headers, so a marker can rerun it.
- `RESULTS.md` — all tables and written answers.
- Machine, OS, compiler version at the top.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 14 | Your container against the real one |
| B | 12 | Why the vector wins and the two lists tie |
| C | 8 | The operation a list is actually for |
| D | 6 | What a dishonest iterator category costs |
| **Total** | **40** | |

---

## Reference Numbers

g++ 13.3.0, x86-64 Linux, `-O2`, n = 1,000,000.

| run | build (ours / std) | traverse (ours / std) | copy (ours / std) |
| --- | --- | --- | --- |
| 1 | 58.7 / 28.6 ms | 3.6 / 2.8 ms | 55.2 / 26.7 ms |
| 2 | 25.6 / 28.7 ms | 5.0 / 4.5 ms | 27.8 / 35.2 ms |
| 3 | 24.6 / 26.3 ms | 4.0 / 3.0 ms | 28.2 / 27.1 ms |

**Runs 2 and 3 are essentially identical between the two containers.** Run 1's `ours 58.7` is allocator
warm-up — the first million allocations in a process pay for growing the heap, and whichever container
runs first absorbs that cost.

**B1 — three-way traversal**, n = 1,000,000 × 10 passes:

| run | your `List` | `std::list` | `std::vector` | list/vector |
| --- | --- | --- | --- | --- |
| 1 | 70.0 ms | 67.0 ms | 7.3 ms | 9.2× |
| 2 | 72.7 ms | 66.6 ms | 9.3 ms | 7.2× |
| 3 | 66.5 ms | 57.2 ms | 5.7 ms | 10.1× |

**The two lists are within about 15% of each other; the vector is 7–10× faster than both.**

**D1 — the lying iterator:**

| n | `std::sort` | correctly sorted? |
| --- | --- | --- |
| 1,000 | 8.58 ms | yes |
| 2,000 | 39.44 ms | yes |
| 4,000 | 194.39 ms | yes |

**About 4.8× per doubling** — $O(n^2 \log n)$. For scale, `std::sort` on 4,000 elements in a
`std::vector` takes well under a millisecond.

---

## What This Lab Is Really Showing

**Part A's result is the encouraging one and the least interesting.** Your list matches `std::list`
because there is nothing clever in either — one allocation per node, pointer chasing to traverse. A
week of work reproduced a standard container's performance, which says more about the problem than
about you.

**Part D is the one to remember.**

Every previous lab has measured a *cost*: what a template instantiation costs, what a virtual call
costs, what a `shared_ptr` copy costs. **Part D measures the cost of a lie** — an interface that
claims a capability it does not have.

And notice the shape of the failure. Nothing crashed. No sanitizer fired. `is_sorted` returned true
every time. **The program was correct and roughly a thousand times too slow**, and there is no tool in
this course that would have told you.

The only thing that would have caught it is the discipline the STL builds in: **declare the category
you can honour, and let the algorithm refuse you.** A compile error you fix in a minute, against a
performance bug you find in production — and the language gave you the compile error for free, if you
were honest with it.

That is why Project 1 marks you for your container *failing* to compile with `std::sort`.

---

*PROG 102 · Week 6 · Lab 6 · © CSE Department*
