# PROG 102 · Problem Set 3
## Ten Problems With the STL

**Week 3 · Released Friday Week 3 · Due Friday Week 4, 17:00 · 100 points**
**Covers:** Lectures 10–12

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**Deliverables:** `problems.cpp` (Part A), `choice.cpp` + measurements (Part B), `traps.cpp` (Part C),
and `ANSWERS.md`. Name collaborators and state any generative-tool use.

### The Rule for Part A

> **No raw loops where a standard algorithm exists.**

You may use range-`for` to *print* results. Everything else — searching, counting, transforming,
partitioning, sorting, accumulating — must go through `<algorithm>` or `<numeric>`.

This constraint is artificial and deliberate. **The point is to make you look for the algorithm**,
because the usual reason people hand-roll a loop is not knowing `std::rotate` or
`std::stable_partition` was already there. Part C asks you to push back on it.

You may of course write your own **lambdas** — those are not loops.

---

## Part A — Ten Problems (60 pts, 6 each)

Each problem: working code, the output for the given input, and **one line naming the containers and
algorithms you used and why.**

Use this input where a sequence of integers is wanted:

```cpp
std::vector<int> v{5,3,8,1,9,2,8,3,7,4};
```

**A1.** *(6)* **Word frequency.** Given a `vector<std::string>`, report each distinct word with its
count, ordered by count descending and then alphabetically. Demonstrate on
`{"the","cat","the","dog","the","cat"}`.

**A2.** *(6)* **Deduplicate, preserving first-occurrence order.** From `v`, produce
`5 3 8 1 9 2 7 4`. *(Note that sorting first would be a different — and wrong — answer.)*

**A3.** *(6)* **The k-th largest**, without fully sorting. Report the 3rd largest of `v`.
**State the complexity of the algorithm you used** and say why it beats sorting.

**A4.** *(6)* **Group anagrams.** Given `{"eat","tea","tan","ate","nat","bat"}`, group words that are
anagrams of one another. Report the groups.

**A5.** *(6)* **Set operations.** Given `{1,2,3,4,5}` and `{4,5,6,7}`, produce their intersection,
union and difference. **State the precondition these algorithms require** — it is easy to violate.

**A6.** *(6)* **Rotate** `v` left by 3 positions, in place.

**A7.** *(6)* **Stable partition**: rearrange `v` so all even values precede all odd ones, **with the
relative order within each group preserved.** Show that `std::partition` gives a different answer, and
report both.

**A8.** *(6)* **Statistics.** Report min, max, mean and the sum of squares of `v` in a single pass each.
**Be careful with the mean** — Lecture 12 §4.1.

**A9.** *(6)* **Longest increasing run.** Find the longest run of strictly increasing consecutive
elements in `v`, and report its length and starting index.

**A10.** *(6)* **Top-N by a custom key.** Given a `vector` of structs with `name` and `score`, report
the three highest scores, ties broken by name. Do not sort the whole container.

---

## Part B — Choosing a Container, With Evidence (20 pts)

**B1.** *(8)* Reproduce Lecture 11 §4 on your machine:

- **(a)** insert N random integers into a `vector` and a `list`, **keeping sorted order**, for at least
  four values of N up to 50,000;
- **(b)** insert 100,000 elements at the **front** of each, where no search is needed.

Report both tables and both ratios.

**B2.** *(6)* `list` insertion is $O(1)$ and `vector` insertion is $O(n)$. Your (a) table shows the
vector winning by a growing factor.

**Explain the contradiction in three sentences.** Then state the general lesson about what a complexity
table does and does not describe.

**B3.** *(6)* Measure `map` against `unordered_map` for insertion and lookup on 200,000 keys, first
with `int` keys and then with `std::string` keys.

Report both. **Does the ratio change between key types?** Give a plausible reason.

---

## Part C — Four Traps (20 pts)

**C1.** *(5)* **`accumulate`'s type.** Sum `{0.5, 0.5, 0.5}` with initial value `0`, then `0.0`.
Report both.

Then sum one million `int`s of one million each with initial value `0`. Report the result, and the
`-fsanitize=undefined` output.

**Why does the sanitizer catch the second and not the first?**

**C2.** *(5)* **`std::remove` does not remove.** Apply it to `{1,2,3,2,4,2,5}` for the value 2.

Report `size()` before and after, and **print the entire vector including the tail.** Then fix it with
the erase-remove idiom.

**In one sentence: why can the algorithm not do this itself?**

**C3.** *(5)* **Iterator invalidation.** Write the `vector` `push_back` invalidation bug and catch it
with AddressSanitizer. Paste the report.

Then `reserve` enough capacity and show it no longer fires. **Is the code now correct? Answer
carefully.**

**C4.** *(5)* **`vector<bool>`.** Show that `bool& b = vb[0];` fails while `int& i = vi[0];` succeeds,
and report `decltype(vb[0])`.

Then write a function template that works for `std::vector<T>` for every `T` **except** `bool`, and
show it failing.

**In one sentence, state what this says about when to use specialization** — refer to Week 2 §L09 §2.3.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 60 | Finding the right algorithm and container for ten distinct problems |
| B | 20 | Measuring container performance and reconciling it with the theory |
| C | 20 | The four traps that silently produce wrong answers |
| **Total** | **100** | |

---

## A Note on the No-Loops Rule

**In `ANSWERS.md`, nominate one problem from Part A where you think the raw loop would have been
better**, write both versions, and argue for the loop in three sentences.

This is worth **no marks** and is not optional. The rule exists to make you learn the library, not
because algorithm calls are always clearer — and a student who finishes Part A without once feeling the
constraint was wrong has probably not looked hard enough at what they wrote.

---

## Submission Checklist

1. Clean build, no warnings; sanitizer-clean except where C1–C4 provoke reports.
2. Part A: no raw loops except for printing; each problem names its containers and algorithms.
3. Part B: at least four values of N, and both directions of the insertion test.
4. Part C: all four traps demonstrated with actual output pasted.
5. The nomination described above.
6. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 3 · Problem Set 3 · © CSE Department*
