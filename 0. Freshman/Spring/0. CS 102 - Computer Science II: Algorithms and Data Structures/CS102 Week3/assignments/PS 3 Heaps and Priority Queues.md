# CS 102 · Problem Set 3
## Heaps and Priority Queues

**Released:** Friday 12 February 2027, 10:00 (after L12) · Week 3
**Due:** Friday 19 February 2027, 17:00 · Week 4 — late penalty from 17:01 (syllabus late policy)
**Points:** 100 · counts toward the Problem Sets component (35%, lowest one dropped)
**Expected time:** about 4–5 hours

**Submit:** `ps3.py` (all code, runnable end to end) and `ps3.md` (all written answers, tables, and
proofs). Written answers inside code comments will not be marked.

Height counts **edges**; a leaf has height 0 and the empty tree has height $-1$. All heaps are
**min-heaps**, **0-indexed**, unless a question says otherwise.

## What this problem set uses

Weeks 0–3: the heap property and the 0-indexed array layout, sift-up and sift-down (L10), the linear
build and its proof (L11), and `heapq`, the index map and lazy deletion (L12). The series
$\sum h x^h$ is quoted in L11 §3; you are asked to derive its value at $x = 1/2$ yourself.

**Not needed and not expected:** graphs or Dijkstra's algorithm (Weeks 4–5); heap sort, which is
Lab 3's job. Measuring build swap counts is also out — Lecture 11 §4 has already done it.

---

## Part A — The Array Representation (18 points)

**A1.** *(4)* Write and test the three index functions for a **0-indexed** heap: `left(i)`,
`right(i)`, `parent(i)`.

Then state, in one sentence each:

- (a) the **depth** of index $i$, as a formula;
- (b) the range of indices that are **leaves** in a heap of $n$ elements;
- (c) the **height** of a heap of $n$ elements.

Verify (a) and (b) programmatically for $n = 1 \dots 100$.

---

**A2.** *(10)* Lecture 10 §4 describes a bug: writing `parent(i) = i // 2` — the 1-indexed formula —
in 0-indexed code.

- **(a)** *(2)* Prove that `i // 2 == (i - 1) // 2` holds **exactly** when $i$ is odd, and explain in
  one sentence what that means about which nodes the bug affects.
- **(b)** *(4)* Build a heap by repeated insertion using the **buggy** parent function. By exhaustive
  search over permutations, find **the smallest $n$ for which some insertion order produces an array
  that is not a valid heap.** Report $n$, one witness ordering, and the resulting array. Prove your
  $n$ is minimal by reporting that all permutations of every smaller size pass.
- **(c)** *(2)* Test the buggy build on **increasing** input $0, 1, \dots, n-1$ for
  $n \in \{10, 100, 1000\}$. Report what happens, and explain **why** in one sentence.

> Part (c) is the point of this question. Write your answer to it as though warning a colleague.

---

**A3.** *(4)* Give an array of 7 distinct integers that is a valid min-heap but **not** sorted, and an
array of 7 that is sorted. Then answer: **is every sorted array a valid min-heap?** Prove it or give
a counterexample.

---

## Part B — The Priority Queue (32 points)

Implement a class `MinHeap` with **no use of `heapq`** anywhere in Part B.

**B1.** *(7)* `sift_up(i)` and `sift_down(i)`.

`sift_down` must swap with the **smaller** of the two children. Include in `ps3.md` a three-element
array on which swapping with the *wrong* child leaves the heap property violated, and show the
resulting array.

**B2.** *(8)* `push(x)`, `pop_min()`, `peek()`, `__len__`. `pop_min` on an empty heap must raise
`IndexError`.

**B3.** *(7)* `build(xs)` — the $\Theta(n)$ construction of Lecture 11, **not** repeated insertion.

**B4.** *(5)* `check_heap()`, returning `True` iff the heap property holds at every index. Call it
after every operation in your tests, not just at the end.

**B5.** *(5)* A randomised stress test: at least 300 trials of interleaved `push` and `pop_min`,
comparing your output against `sorted()` on the same multiset, and calling `check_heap()` after every
single operation. Report the number of trials and failures.

> **Do not trust a structure you have not verified.** B5 is what makes Parts C and D worth doing on
> top of your code. This was Lab 0's rule and it has not changed.

---

## Part C — Why the Build Is Linear (26 points)

**C1.** *(5)* In a complete binary tree of $n$ nodes, prove that the number of nodes at height $h$ is
at most $\lceil n / 2^{h+1} \rceil$.

**C2.** *(10)* Using C1, prove that `build` performs $O(n)$ work. Your proof must:

- write the total as a sum over heights;
- evaluate $\sum_{h=0}^{\infty} h/2^{h}$, showing your working — do not merely assert that it is 2;
- state where the $\log n$ factor went.

**C3.** *(5)* The loop `for i in range(n//2 - 1, -1, -1)` runs **backwards**. State the precondition
`sift_down(i)` requires, and explain in two sentences why running forwards violates it. Then
demonstrate it: run a forward version on 500 random arrays and report how many produce an invalid
heap.

**C4.** *(6)* Building by repeated insertion is $\Theta(n\log n)$ in the worst case, and the
$\Theta(n)$ build is $\Theta(n)$. Both call an $O(\log n)$ repair once per element.

**Explain the discrepancy in three sentences or fewer.** A complete answer mentions where the nodes
are.

---

## Part D — `decrease_key` (24 points)

Dijkstra's algorithm needs to lower the priority of an item already in the queue. Both standard
solutions, then a judgement.

**D1.** *(9)* `IndexedPQ`, holding `(priority, key)` pairs with a dict `pos: key -> index` maintained
through every swap. `decrease_key(key, new_priority)` must be $O(\log n)$ and must ignore a new
priority that is not an improvement.

**D2.** *(9)* `LazyPQ` over `heapq`. `decrease_key` pushes a new entry; `pop` discards stale ones.
You may use `heapq` in Part D.

**D3.** *(6)* Cross-check both against a brute-force reference on at least 200 randomised sequences of
pushes with repeated keys. Then answer, in a short paragraph:

- Which would you ship, and why?
- `LazyPQ`'s heap can hold more than one entry per key. Bound its size in terms of the number of
  `decrease_key` calls, and say why Dijkstra's asymptotic running time is unaffected.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 18 | Index arithmetic; the parent bug and why tests miss it |
| B | 32 | A correct, verified priority queue |
| C | 26 | The linear-build proof |
| D | 24 | `decrease_key`, both ways, with a judgement |
| **Total** | **100** | |

Partial credit throughout. **An implementation that passes B5 and a wrong analysis scores better than
a correct analysis of code that does not run.**

---

## A Note on Part A2

A2 asks you to look for an input that makes a wrong program fail, which is the opposite of the usual
exercise.

The buggy parent function passes on increasing input at every size. It passes on decreasing input at
$n = 10$. It fails on 4.3% of random inputs at $n = 10$ and on 98.5% at $n = 100$. **A student who
tested it on sorted data and shipped it would have had every reason to feel confident.**

The habit worth building: when a test passes, ask what class of inputs it actually exercised. Here
the answer is "the ones where the parent function is never consulted," and that is a fact about the
test, not about the code.

---

*CS 102 · Week 3 · Problem Set 3 · © CSE Department*
