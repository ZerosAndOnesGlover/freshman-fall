# PROG 102 · Problem Set 3
## Five Problems With the STL

**Released:** Friday 12 February 2027, 10:00 · Week 3 (after Thursday's L12)
**Due:** Friday 19 February 2027, 17:00 · Week 4 — late penalty from 17:01
**Points:** 100 · counts toward the Problem Sets component (30%, lowest one dropped)
**Expected time:** about 4 hours

## What this problem set uses

Weeks 0–3: iterators and half-open ranges (L10), `vector`, `list`, `map`, `set` and `unordered_map`
(L11), and the algorithms Lecture 12 teaches — `sort`, `stable_sort`, `find`, `count_if`,
`transform`, `accumulate`, `lower_bound`, `binary_search`, `remove`/`remove_if` and `max_element` —
with comparators written as function objects or empty-bracket lambdas (L12 §2.2). Specialization is
Week 2.

**Not needed and not expected:** `nth_element`, `partial_sort`, the set algorithms, `rotate`,
`stable_partition` (none is taught); lambdas with capture (Week 11). Container timing is Lab 3's job.

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**Deliverables:** `problems.cpp` (Part A), `traps.cpp` (Part B),
and `ANSWERS.md`. Name collaborators and state any generative-tool use.

### The Rule for Part A

> **Prefer the algorithms from Lecture 12 to a hand-written loop** wherever one of them fits.

A raw loop is fine where none of Lecture 12's algorithms does the job — A5 is such a case — and you may
always use range-`for` to print. Comparators may be function objects or empty-bracket lambdas.
---

## Part A — Five Problems (60 pts, 12 each)

Each problem: working code, the output for the given input, and **one line naming the containers and
algorithms you used and why.**

Use this input where a sequence of integers is wanted:

```cpp
std::vector<int> v{5,3,8,1,9,2,8,3,7,4};
```

**A1.** *(12)* **Word frequency.** Given a `vector<std::string>`, report each distinct word with its
count, ordered by count descending and then alphabetically. Demonstrate on
`{"the","cat","the","dog","the","cat"}`.

**A2.** *(12)* **Deduplicate, preserving first-occurrence order.** From `v`, produce
`5 3 8 1 9 2 7 4`. *(Note that sorting first would be a different — and wrong — answer.)*

**A3.** *(12)* **Group anagrams.** Given `{"eat","tea","tan","ate","nat","bat"}`, group words that are
anagrams of one another. Report the groups.

**A4.** *(12)* **Statistics.** Report min, max, mean and the sum of squares of `v` in a single pass each.
**Be careful with the mean** — Lecture 12 §4.1.

**A5.** *(12)* **Longest increasing run.** Find the longest run of strictly increasing consecutive
elements in `v`, and report its length and starting index.

---

## Part B — Three Traps (40 pts)

**B1.** *(14)* **`accumulate`'s type.** Sum `{0.5, 0.5, 0.5}` with initial value `0`, then `0.0`.
Report both.

Then sum one million `int`s of one million each with initial value `0`. Report the result, and the
`-fsanitize=undefined` output.

**Why does the sanitizer catch the second and not the first?**

**B2.** *(13)* **`std::remove` does not remove.** Apply it to `{1,2,3,2,4,2,5}` for the value 2.

Report `size()` before and after, and **print the entire vector including the tail.** Then fix it with
the erase-remove idiom.

**In one sentence: why can the algorithm not do this itself?**

**B3.** *(13)* **`vector<bool>`.** Show that `bool& b = vb[0];` fails while `int& i = vi[0];` succeeds,
and report `decltype(vb[0])`.

Then write a function template that works for `std::vector<T>` for every `T` **except** `bool`, and
show it failing.

**In one sentence, state what this says about when to use specialization** — refer to Lecture 09 §2.3.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 60 | Finding the right algorithm and container for five distinct problems |
| B | 40 | Three traps that silently produce wrong answers |
| **Total** | **100** | |

---

## A Note on Loops

**In `ANSWERS.md`, nominate one problem from Part A where you think the raw loop is better than the
algorithm version**, write both, and argue for your choice in three sentences. This is worth **no
marks** and is not optional.
---

## Submission Checklist

1. Clean build, no warnings; sanitizer-clean except where B1–B3 provoke reports.
2. Part A: each problem names its containers and algorithms.
3. Part B: all three traps demonstrated with actual output pasted.
4. The nomination described above.
5. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 3 · Problem Set 3 · © CSE Department*
