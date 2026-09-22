# PROG 102 · Lab 3
## Profiling STL Containers

**Date:** Monday 15 February 2027 · 15:00–16:50 · Lab section (Week 4) — covers Week 3 (L10–L12)
*2-hour lab · 40 points · in-lab checkoff · part of the Labs component (20%)*
**Deliverable:** `bench/` with your programs, `RESULTS.md`. In-lab checkoff.

---

## Purpose

Every data structures course gives you this table:

| | `vector` | `list` |
| --- | --- | --- |
| insert at a position | $O(n)$ | $O(1)$ |
| random access | $O(1)$ | $O(n)$ |
| traversal | $O(n)$ | $O(n)$ |

**Two of those three rows are misleading in practice, and this lab finds out which.**

You will measure traversal, insertion in both directions, and the associative containers. The results
will contradict the table in one place, confirm it in another, and the difference between the two cases
is the thing worth taking away.

> **Timing discipline:** `-O2` for every measurement, **never a sanitizer build**, three runs minimum,
> and report your machine, OS and compiler at the top of `RESULTS.md`. Part D is the only part that
> uses a sanitizer build, and it is not timed.

---

## Part A — Traversal (10 pts)

**A1.** *(6)* Sum every element of a `vector<int>`, a `deque<int>` and a `list<int>`, each holding
1,000,000 elements, over 20 passes.

Report all three times and the ratio to `vector`.

> **Use the result.** Assign the sum to a `volatile` variable or print it. At `-O2` the compiler will
> otherwise delete the entire loop, and you will measure nothing very quickly.

**A2.** *(4)* All three are $O(n)$. **Explain the spread in three sentences.**

Your explanation should mention memory layout. It does not need to mention cache lines by name — Week
12 measures that directly — but it should say why one contiguous array is different from a million
separate allocations.

---

## Part B — The Insertion Paradox (14 pts)

This is the substance of the lab. Do both halves before drawing any conclusion.

**B1.** *(6)* **Insertion *with* a search.** Insert N random integers into a `vector` and into a
`list`, each time placing the element in its correct position so the container stays sorted.

- For the `vector`, find the position with `std::lower_bound`.
- For the `list`, find it by walking from `begin()` — a list has no random access, so you have no
  choice (L10 §3).

Run for **N = 1,000, 5,000, 20,000, 50,000** and tabulate both times and the ratio.

**B2.** *(4)* **Insertion *without* a search.** Insert 100,000 elements at the **front** of each
container, where the position is already known.

Report both times and the ratio.

**B3.** *(4)* B1 and B2 point in opposite directions. Answer all three:

- **(a)** *(1)* Which container won each, and by roughly what factor?
- **(b)** *(2)* The complexity table says `list` insertion is $O(1)$ and `vector` insertion is $O(n)$.
  **Reconcile that with your B1 result.**
- **(c)** *(1)* State, in one sentence, what the complexity table leaves out.

---

## Part C — Associative Containers (10 pts)

**C1.** *(5)* Insert 200,000 random `int` keys into a `std::map` and a `std::unordered_map`, then look
up every key in a different order from the one you inserted them — reverse order is enough
(`std::shuffle` is not needed and has not been taught).

Report insert and lookup times for both, and the ratios.

**C2.** *(3)* Print the first few keys of each in iteration order, for a small example.

**State what `map` gives you that `unordered_map` does not**, and say whether your lookup measurement
makes that look expensive.

**C3.** *(2)* Build a `std::set` of 100,000 integers. Time `std::find(s.begin(), s.end(), k)` against
`s.find(k)` for a couple of thousand lookups.

Report the ratio. **Why can the generic algorithm not do better?**

---

## Part D — `reserve` and Invalidation (6 pts)

**D1.** *(3)* Time `push_back` of n elements into a `vector` with and without `reserve(n)`, for
n = 10⁵ and 10⁶. Report both speedups.

Separately, count how many times `capacity()` changes over one million `push_back`s, and report the
**growth factor** your standard library uses.

**D2.** *(3)* Take an iterator to `v.begin()`, `push_back` enough to force reallocation, then read
through the iterator. Build with `-fsanitize=address` and paste the report.

Now `reserve` enough capacity up front and show the report disappears.

**Then answer:** *(2 of the 3)* Is the `reserve`d version **correct**, or merely **not currently
failing**? Justify in two sentences.

---

## Submission

- `bench/` — every program, so a marker can rerun them.
- `RESULTS.md` — all tables and written answers.
- **Machine, OS, compiler version at the top.**

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 10 | Traversal, and why $O(n)$ is not one number |
| B | 14 | The insertion paradox, measured both ways |
| C | 10 | Ordered against hashed, and generic against member |
| D | 6 | `reserve`, growth, and invalidation |
| **Total** | **40** | |

---

## Reference Numbers

g++ 13.3.0, x86-64 Linux, `-O2`. **Ratios should be broadly reproducible; absolute times will not be.**

**A1 — traversal**, 1,000,000 ints × 20 passes:

| | time | vs vector |
| --- | --- | --- |
| `vector` | 9.7 ms | 1.0× |
| `deque` | 10.6 ms | 1.1× |
| `list` | **61.2 ms** | **6.3×** |

**B1 — sorted insertion:**

| N | `vector` | `list` | list/vector |
| --- | --- | --- | --- |
| 1,000 | 0.08 ms | 0.41 ms | 5.1× |
| 5,000 | 0.71 ms | 32.5 ms | 45.9× |
| 20,000 | 6.60 ms | 1,038 ms | 157× |
| 50,000 | 45.3 ms | 8,086 ms | **178×** |

**B2 — front insertion, 100,000 elements:**

| `vector` | `list` | vector/list |
| --- | --- | --- |
| 446 ms | 3.5 ms | **128×** |

**C1 — 200,000 int keys:**

| | `map` | `unordered_map` | ratio |
| --- | --- | --- | --- |
| insert | 76.1 ms | 44.5 ms | 1.71× |
| lookup | 98.1 ms | 15.1 ms | **6.50×** |

**C2:** `map` gives `1 2 3 4 5`; `unordered_map` gave `3 2 4 1 5`.

**C3:** `std::find` 2,119 ms against `s.find` 0.3 ms — **about 6,000×**.

**D1:** `reserve` gave 4.59× at 10⁵ and 2.47× at 10⁶. Growth factor **2.0**; one million `push_back`s
caused **21** capacity changes, ending at 1,048,576.

---

## What This Lab Is Really Showing

Part B is the point, and it is not "linked lists are bad".

**Both measurements are correct.** The list's $O(1)$ insertion is real and B2 cashes it in for a 128×
win. B1 loses by 178× because the $O(1)$ insertion is attached to an $O(n)$ search through memory the
cache cannot help with — and in real code, **the search is almost always there.** You rarely happen to
be holding the right position; you usually have to go and find it.

So the complexity table is not wrong. It is **answering a different question** from the one you have.
It describes the insertion in isolation, and your program does a search *and* an insertion, on hardware
where the cost of touching memory varies by a factor of fifty depending on where that memory is.

This is the same shape as Week 2's Lab. There, a correct measurement carried a wrong explanation. Here,
a correct *theory* answers a question adjacent to the one you asked. **In both cases the fix is the
same: get the number for the thing you actually intend to do.**

And it is why the practical advice in Lecture 11 §8 is blunt — **use `vector`, change for a reason you
can name.** Not because linked lists are useless, but because the reasons to prefer one are narrower
than the table makes them look, and you now have the numbers to tell which case you are in.

---

*PROG 102 · Week 3 · Lab 3 · © CSE Department*
