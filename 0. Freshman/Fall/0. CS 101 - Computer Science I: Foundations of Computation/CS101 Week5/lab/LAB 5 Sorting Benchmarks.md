# CS 101 · Lab 5
## Counting the Work Sorting Algorithms Do

**Date:** Tuesday 3 November 2026 · 15:00–16:50 · Lab Section (Week 6) — covers Week 5 (L16–L18)
*Duration: 2 hours · 100 points via TA checkoff, part of the Labs component (10%)*

---

## Objectives

By the end of this lab, you will:
- [ ] Implement selection, insertion, bubble and merge sort so each reports its comparisons and swaps (L17 §7)
- [ ] Measure how the counts grow as `n` doubles, on sorted, reversed and random input
- [ ] Explain best and worst cases from the numbers, not from memory
- [ ] Show on paper why selection sort is not stable

**Tools used:** Weeks 0–5 only — functions, loops, lists, tuples, `random.randint` (as in L17 §7).
You count operations instead of timing them: counts are exact, repeatable, and need no extra modules.

---

## Setup

```bash
mkdir -p "$CS101/week5"
cd "$CS101/week5"
```

Copy `sorting_counts_starter.py` from this week's `lab/` folder to `"$CS101/week5"`, renamed `sorting_counts.py`.

---

## Part 1: Four Sorts That Count (35 minutes) — 30 points

Each function returns `(sorted_copy, comparisons, swaps)` and must not change its argument.

| Function | Notes |
|---|---|
| `selection_sort(lst)` | count a swap only when `smallest != i` |
| `insertion_sort(lst)` | swap-based: move `a[j]` left while `a[j-1] > a[j]`; stop at the first comparison that fails |
| `bubble_sort(lst)` | with the early exit from L17 §3: stop after a pass with no swaps |
| `merge_sort(lst)` | count one comparison per `left[i] <= right[j]` test; add the counts from both halves; swaps are 0 |

The starter's `__main__` block checks all four against `sorted()` on seven edge cases (empty, one
element, duplicates, sorted, reversed) and on 100 random lists. All must pass.

---

## Part 2: How the Counts Grow (35 minutes) — 35 points

Once Part 1 passes, the starter goes on to Part 2, which prints comparisons for `n` = 100, 200, 400, 800 on sorted, reversed
and random input. Copy the table into `lab5_notes.md` and answer:

1. Which counts are **exactly** the same on every input? Give the formula in `n`.
2. For insertion and bubble sort on **sorted** input, what is the count? Why so small?
3. When `n` doubles, by what factor does each column grow? Which grow by about 4, which by a little more than 2?
4. Merge sort on **sorted** input still does about `(n/2) log₂ n` comparisons. Why doesn't it get the free ride insertion sort gets?

---

## Part 3: Swaps (15 minutes) — 15 points

Part 3 of the starter prints swaps for the three quadratic sorts on reversed input with `n = 100`.

1. Record the three numbers. Selection sort's is surprisingly small — explain exactly why it is `n/2`
   on reversed input (trace `[4, 3, 2, 1]` by hand).
2. L17 §1 says selection sort is the right choice when swaps are expensive. Use your numbers to explain.

---

## Part 4: Stability on Paper (15 minutes) — 20 points

Records are `(grade, name)`; sort by **grade only**:

```
[(2, "Ann"), (2, "Bob"), (1, "Cal")]
```

1. Trace **selection sort** by hand. Show the list after each pass. Are Ann and Bob still in order?
2. Trace **insertion sort** the same way. Are they?
3. Using L17's stability discussion, state the property of each algorithm's swaps that decides the answer.

---

## Part 5: Commit and Reflection

```bash
cd "$CS101/week5"
git add .
git commit -m "CS 101 Lab 5: comparison and swap counts for four sorts"
git push
```

In `lab5_notes.md`: **Q1.** For random input, estimate from your table the `n` at which merge sort
does 10× fewer comparisons than insertion sort. **Q2.** Why does counting comparisons tell you more
about an algorithm than one stopwatch timing does? Name one thing a count misses.

---

## TA Checkoff Criteria

| Part | Points | Show your TA |
|---|---|---|
| 1 | 30 | All four sorts pass the starter's checks (7.5 each) |
| 2 | 35 | Table recorded; four questions answered from the numbers |
| 3 | 15 | Swap counts recorded; selection sort's `n/2` explained |
| 4 | 20 | Both traces and the stability rule |
| **Total** | **100** | Reflection answered and work committed (required) |

---

*CS 101 · Week 5 · Lab 5 · Tuesday 3 November 2026 · © CSE Department*
