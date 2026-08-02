# CS 101 · Week 5: Searching and Sorting Algorithms

---

## Contents

```
CS101_Week5/
│
├── README.md                                    ← You are here
│
├── lectures/
│   ├── L16 Searching Algorithms.md              ← Wed: linear vs binary search,
│   │                                                 loop invariant proof, off-by-one traps,
│   │                                                 bisect variants, binary search on the answer
│   ├── L17 Elementary Sorting.md                ← Thu: selection/insertion/bubble sort,
│   │                                                 loop invariants, stability, key parameter,
│   │                                                 empirical comparison/swap counting
│   └── L18 Merge Sort and Quicksort.md          ← Fri: merge sort recurrence + tree proof,
│                                                      quicksort + worst case, Timsort,
│                                                      Ω(n log n) decision-tree lower bound
│
├── lab/
│   ├── LAB 5 Sorting Benchmarks.md               ← Tue: implement + instrument all 5 sorts,
│   │                                                 benchmark 10→100,000, plot log-log,
│   │                                                 verify best-case & stability empirically
│   └── sorting_algorithms_starter.py            ← Lab starter — 5 algorithms + verify_all()
│
├── assignments/
│   ├── QUIZ 5 Week 5 Wednesday.md                    ← In-class quiz (covers Week 4)
│   ├── PS 5 Searching and Sorting.md             ← Problem Set 5 (due Friday Week 6)
│   └── ps5_starter.py                           ← Full scaffold: 4 sections, search + sort +
│                                                      empirical analysis + event scheduling
│
└── resources/
    └── Reading Guide Week 5.md                   ← 3 experimentation sessions, algorithm
                                                      summary table, 5 mistakes, self-test,
                                                      Midterm 1 prep notes
```

---

## Week 5 at a Glance

**Theme:** Algorithms, for real — the same problem (searching, sorting) solved multiple ways, with dramatically different efficiency. This week converts the recursion and complexity intuition from Week 4 into concrete, comparable, benchmarkable algorithms.

| Day | Event | Topic |
|-----|-------|-------|
| Wed | Lecture 16 + Quiz 5 | Linear vs binary search; invariant proofs; binary search on the answer |
| Thu | Lecture 17 | Selection, insertion, bubble sort; stability; O(n²) at scale |
| Fri | Lecture 18 + PS5 released | Merge sort, quicksort, Timsort; Ω(n log n) lower bound |
| Tue | Lab 5 (graded) | Implement, instrument, benchmark, and plot all 5 sorting algorithms |

**⚠️ Midterm 1 is next week** (Week 6), covering everything from Week 0 through Week 5.

---

## Your To-Do List

### Before Wednesday
- [ ] Reread Guttag Ch. 3.4 (bisection search) with fresh eyes post-recursion
- [ ] Review Week 4 — Quiz 5 covers recursion, base cases, memoization

### Wednesday
- [ ] Quiz 5 (10 min — covers Week 4)
- [ ] Notes for L16

### Before Thursday
- [ ] REPL Session A from Reading Guide (feel the O(n) vs O(log n) gap firsthand)
- [ ] Read the sorting chapter in Guttag (or equivalent)

### Thursday
- [ ] Notes for L17
- [ ] REPL Session B (watch selection sort degrade vs merge sort)

### Tuesday Lab (Required, Graded)
- [ ] Implement all 5 instrumented sorting algorithms
- [ ] Run the full benchmark (n=10 to 100,000) and generate all 3 plots
- [ ] Verify best-case behavior and stability empirically
- [ ] TA checkoff

### Friday
- [ ] Notes for L18
- [ ] REPL Session C (Stirling's approximation — feel why Ω(n log n) is real)
- [ ] PS5 released — read completely tonight

### Weekend
- [ ] Start PS5 — at minimum A1–A4 (written) and B1 (search variants)
- [ ] **Begin Midterm 1 review** — Weeks 0 through 5

---

## The Central Ideas of Week 5

**1. Structure enables efficiency.**
Sorting imposes global order on data; binary search exploits that order to eliminate half the search space per comparison. This is the deepest idea of the week: precomputation (sorting) buys faster subsequent operations (searching).

**2. The same asymptotic class can hide very different constants.**
Insertion sort and bubble sort are both O(n²), but insertion sort's best case (already-sorted data) is O(n) — a property that makes it genuinely useful in hybrid systems like Timsort.

**3. Divide-and-conquer breaks the O(n²) barrier.**
Merge sort's recurrence T(n) = 2T(n/2) + O(n) solves to O(n log n) — provably better than any O(n²) approach at scale. The recursion-tree method (from Week 4) is exactly how you derive this.

**4. Stability is a concrete, checkable property — not an abstraction.**
A stable sort preserves the relative order of equal elements. This directly enables multi-key sorting: sort by the least significant key first, then by increasingly significant keys.

**5. Ω(n log n) is a provable lower bound for comparison sorts.**
The decision-tree argument (n! possible orderings require log₂(n!) ≈ n log n comparisons in the worst case) proves that merge sort, quicksort (average case), and Timsort are asymptotically optimal — not just "good," but as good as any comparison sort can be.

**6. Real systems use hybrid, empirically-tuned algorithms.**
Timsort exploits real-world data's natural runs. C++'s introsort switches strategies based on recursion depth. Always prefer your language's built-in sort in production code.

---

## Quick Self-Check

Without notes:

1. What precondition must hold before you can binary search a list?
2. State binary search's loop invariant.
3. Why is selection sort's number of comparisons always exactly n(n-1)/2?
4. What makes insertion sort O(n) on already-sorted data?
5. What is bubble sort's early-exit optimization?
6. Solve the recurrence T(n) = 2T(n/2) + O(n) using a recursion tree.
7. Why is quicksort's worst case O(n²), and how do real implementations avoid it?
8. What does "stable" mean for a sorting algorithm? Name one stable and one unstable algorithm from this week.
9. What is Timsort, and why does it beat pure merge sort in practice on real data?
10. What is the Ω(n log n) lower bound, and what argument proves it?

*(Answers: 1. sorted data. 2. if target is present, it's in lst[lo..hi]. 3. the inner loop structure doesn't depend on values, only positions. 4. no shifting is ever needed. 5. skip remaining passes if a full pass makes zero swaps. 6. O(n) work per level × log₂n levels = O(n log n). 7. degenerate pivot (already-sorted + first-element pivot); randomized/median-of-three pivot mitigates. 8. equal elements keep relative order; merge sort stable, quicksort/selection sort not. 9. Python's hybrid sort exploiting natural runs + insertion sort for small/sorted runs. 10. n! orderings require log₂(n!)≈n log n comparisons; decision-tree depth argument.)*

---

## Algorithms and Patterns Introduced This Week

| Algorithm | Complexity | Key Idea |
|-----------|-----------|----------|
| Linear search | O(n) | Check every element; no precondition |
| Binary search | O(log n) | Halve the search space; requires sorted data |
| Binary search on the answer | O(log(range)) | Applies to any monotonic predicate, not just arrays |
| Selection sort | O(n²) | Find min of remainder, swap to front |
| Insertion sort | O(n) best, O(n²) worst | Insert into sorted prefix; great for nearly-sorted data |
| Bubble sort | O(n) best, O(n²) worst | Swap adjacent pairs; early-exit optimization |
| Merge sort | O(n log n) | Divide, recursively sort, merge; stable |
| Quicksort | O(n log n) avg, O(n²) worst | Partition around pivot; fast in practice, unstable |
| Timsort | O(n) best, O(n log n) worst | Hybrid: exploits real-world data's natural order |

---

*CS 101 · Week 5 · © CSE Department*
