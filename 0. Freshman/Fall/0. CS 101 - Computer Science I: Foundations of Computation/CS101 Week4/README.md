# CS 101 Week 4 Recursion: Thinking in Self-Reference

---

## Contents

```
CS101_Week4/
│
├── README.md                                    ← You are here
│
├── lectures/
│   ├── L13 Recursion Fundamentals.md            ← Wed: three laws, induction connection,
│   │                                                 recursion trees, Fibonacci, list/string
│   │                                                 recursion, Tower of Hanoi, binary search,
│   │                                                 tail recursion, recursion limit
│   ├── L14 Recursive Algorithms.md              ← Thu: counting calls via trees, merge sort,
│   │                                                 recursive descent parsing, binary trees,
│   │                                                 iterative conversion, mutual recursion
│   └── L15 Recursion Mastery.md                 ← Fri: stack depth mechanics, tail calls +
│                                                      trampoline, five design patterns
│                                                      (linear/binary/D&C/tree/backtracking),
│                                                      power set walkthrough, anti-patterns
│
├── lab/
│   ├── LAB 4 Recursion Trees.md                  ← Tue: hand-drawn recursion trees,
│   │                                                 6 recursive implementations,
│   │                                                 slicing anti-pattern fix, N-Queens
│   └── recursion_lab_starter.py                 ← Lab starter with TODOs + full test suite
│
├── assignments/
│   ├── QUIZ 4 Week 4 Wednesday.md                    ← In-class quiz (covers Week 3)
│   ├── PS 4 Recursion.md                         ← Problem Set 4 (due Friday Week 5)
│   └── ps4_starter.py                           ← Full scaffold: 6 sections, 30+ functions
│
└── resources/
    └── Reading Guide Week 4.md                   ← 3 REPL sessions, algorithm comparison
                                                      tables, 6 mistakes, 10-question self-test
```

---

## Week 4 at a Glance

**Theme:** Recursion — the mathematical idea of self-reference, made rigorous and practical. This is the pivot week where computational thinking becomes provably correct thinking.

| Day | Event | Topic |
|-----|-------|-------|
| Wed | Lecture 13 + Quiz 4 | Three laws; induction; recursion trees; Fibonacci; Hanoi; binary search |
| Thu | Lecture 14 | Counting calls; merge sort; recursive descent parsing; trees; iteration conversion |
| Fri | Lecture 15 + PS4 released | Stack depth; tail recursion; 5 design patterns; power set; anti-patterns |
| Tue | Lab 4 (graded) | Recursion tree drawing; 6 implementations; slicing fix; N-Queens backtracking |

---

## Your To-Do List

### Before Wednesday
- [ ] Read Guttag Ch. 4.3 (recursion)
- [ ] Review Week 3 — Quiz 4 covers functions, scope, call stack

### Wednesday
- [ ] Quiz 4 (10 min — covers Week 3)
- [ ] Notes for L13

### Before Thursday
- [ ] REPL Session A from Reading Guide (recursion vs. the stack)
- [ ] Visualize `fib(4)` in Python Tutor — watch overlapping subproblems appear

### Thursday
- [ ] Notes for L14
- [ ] REPL Session B (memoization transformation — measure the speedup yourself)

### Tuesday Lab (Required, Graded)
- [ ] Draw all 4 recursion trees by hand (Part 1)
- [ ] Implement all 6 functions in `recursion_lab.py` with correctness comments
- [ ] Fix the slicing anti-pattern (`slicing_fix.py`)
- [ ] Implement and run the N-Queens solver
- [ ] TA checkoff

### Friday
- [ ] Notes for L15
- [ ] REPL Session C (design practice — sum_digits, count_occ, is_sorted)
- [ ] PS4 released — read completely tonight

### Weekend
- [ ] Start PS4 — at minimum A1–A3 (written) and B1 (list operations)
- [ ] Read Guttag Ch. 3.4 (bisection search)

---

## The Central Ideas of Week 4

**1. Recursion is mathematical induction, implemented.**
Base case ↔ P(0). Recursive case ↔ "if P(k), then P(k+1)." When you write a recursive function correctly, you have implicitly written an inductive proof.

**2. The three laws are non-negotiable.**
Base case. Progress toward the base case. Self-call. Violate any one and the function is wrong (or infinite).

**3. Recursion trees make complexity visible.**
Draw the tree; count the nodes. Linear recursion → O(n) nodes. Binary recursion → O(2^n) nodes. Halving recursion → O(log n) depth, O(n) total work.

**4. Naïve Fibonacci is the canonical warning about overlapping subproblems.**
`fib(n-1) + fib(n-2)` recomputes the same values exponentially many times. Memoization — caching results — turns O(2^n) into O(n). This is your first taste of dynamic programming.

**5. Merge sort is divide-and-conquer, done right.**
Split, recursively sort each half, merge. O(n log n) — optimal for comparison-based sorting.

**6. Binary search is recursion on a shrinking search space.**
Each call eliminates half the remaining possibilities. O(log n) — extraordinarily fast even for huge inputs.

**7. Python does not optimize tail calls.**
Every recursive call — tail position or not — consumes a stack frame. Deep recursion (> 1000 frames) raises `RecursionError`. Convert to iteration with an explicit stack when needed.

**8. Five patterns cover almost all recursive algorithms:**
Linear decrease, binary decrease (beware exponential blowup), divide-and-conquer, tree recursion, and backtracking (choose-explore-unchoose).

---

## Quick Self-Check

Without notes:

1. State the three laws of recursion.
2. Why is `fib(n) = fib(n-1) + fib(n-2)` (naive) exponential?
3. What fixes it, and what's the resulting time complexity?
4. What is the recursion tree depth for merge sort on n elements?
5. Why is `lst[1:]` inside a recursive call dangerous for performance?
6. What is the "choose-explore-unchoose" pattern used for?
7. Does Python optimize tail-recursive calls? What's the practical consequence?
8. What is `sys.getrecursionlimit()` by default?
9. In `fast_power`, why does squaring halve the number of multiplications needed?
10. Give one example each of a problem better solved recursively and one better solved iteratively.

*(Answers: 1. base case, progress, self-call. 2. two calls per level, recomputing shared subproblems. 3. memoization; O(n). 4. log₂n. 5. slicing is O(n), so total work becomes O(n²). 6. backtracking — try, recurse, undo on failure. 7. No; deep tail recursion still overflows the stack. 8. 1000. 9. b^n = (b^(n/2))², so exponent halves each call instead of decreasing by 1. 10. tree traversal (recursive) vs. summing a list (iterative).)*

---

## Algorithms and Patterns Introduced This Week

| Algorithm/Pattern | Complexity | Key Idea |
|-------------------|-----------|----------|
| Factorial (recursive) | O(n) | Linear decrease; textbook base+step |
| Naïve Fibonacci | O(2^n) | Binary decrease; overlapping subproblems |
| Memoized Fibonacci | O(n) | Cache to eliminate recomputation |
| Merge sort | O(n log n) | Divide, recursively sort, combine |
| Binary search | O(log n) | Halve the search space each call |
| Fast power | O(log n) | Square to halve the exponent |
| Tree operations | O(n) | One call per child; base case on None |
| Tower of Hanoi | O(2^n) moves | Move n-1, move 1, move n-1 — provably optimal |
| Permutations | O(n!) | Choose-explore-unchoose over all positions |
| N-Queens | O(n!) worst case | Backtracking with pruning via `is_safe` |
| Power set | O(2^n) | Include or exclude each element |

---

*CS 101 · Week 4 · © CSE Department*
