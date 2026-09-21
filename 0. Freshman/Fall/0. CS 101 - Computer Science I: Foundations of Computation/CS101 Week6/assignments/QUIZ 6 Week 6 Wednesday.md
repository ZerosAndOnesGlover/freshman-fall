# CS 101 · Quiz 6
## Week 6, Wednesday — In-Class Assessment

**Date:** Wednesday 4 November 2026 · 09:00–09:10 (start of L19) · Week 6
**Duration:** 10 minutes (first 10 minutes of Wednesday lecture)
**Format:** Written — closed book, closed notes
**Covers:** Week 5 material: linear/binary search, elementary sorting, merge sort/quicksort, stability

---

### Question 1 (2 points)

What precondition does binary search require that linear search does not? What happens if you binary search unsorted data (does it always fail, or can it silently give a wrong answer)?

---

### Question 2 (2 points)

For each sorting algorithm, state its worst-case time complexity and whether it is stable (Y/N).

| Algorithm | Worst case | Stable? |
|-----------|-----------|---------|
| Selection sort | | |
| Insertion sort | | |
| Merge sort | | |
| Quicksort | | |

---

### Question 3 (2 points)

Insertion sort has a best-case time complexity of O(n), much better than its worst case of O(n²). What specific property of the input data triggers this best case? Explain in one sentence why the algorithm behaves this way on such input.

---

### Question 4 (2 points)

Write the recurrence relation for merge sort's time complexity (in terms of T(n)). Then state the final complexity class this recurrence solves to.

Recurrence: T(n) = ___________

Solution: O(___________)

---

### Question 5 (2 points)

A classmate claims: "Quicksort is O(n log n), full stop — that's just what it is." Correct this statement precisely: what IS quicksort's worst-case complexity, when does it occur, and what practical technique reduces the chance of hitting it?

---

**Total: 10 points**

---

## Answer Key (Instructor Copy)

**Q1:** Binary search requires the data to be **sorted**. If you binary search unsorted data, it does NOT reliably fail — it can silently return a wrong answer (either missing a target that's present, or matching a value at the wrong position) because the algorithm's logic for discarding half the search space depends entirely on the sortedness assumption. This is a dangerous silent failure mode, not a loud error.

**Q2:**
| Algorithm | Worst case | Stable? |
|-----------|-----------|---------|
| Selection sort | O(n²) | No |
| Insertion sort | O(n²) | Yes |
| Merge sort | O(n log n) | Yes |
| Quicksort | O(n²) | No |

**Q3:** Already-sorted (or nearly-sorted) input. When the data is already sorted, the inner `while` condition (`lst[j] > key`) is immediately False for every element, so no shifting ever occurs — the algorithm just scans through once, giving O(n).

**Q4:**
Recurrence: `T(n) = 2T(n/2) + O(n)`
Solution: `O(n log n)`

**Q5:** Quicksort's **average-case** complexity is O(n log n), but its **worst-case** complexity is O(n²). The worst case occurs with a poor pivot choice combined with adversarial input (e.g., always choosing the first element as pivot on already-sorted or reverse-sorted data), causing maximally unbalanced partitions. Using a **randomized pivot** (or median-of-three) makes the worst case exponentially unlikely in practice.

---

*CS 101 · Week 6 · Quiz 6 · © CSE Department*
