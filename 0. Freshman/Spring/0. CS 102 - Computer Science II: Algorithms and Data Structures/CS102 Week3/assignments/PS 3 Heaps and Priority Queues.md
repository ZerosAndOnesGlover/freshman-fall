# CS 102 · Problem Set 3
## Heaps and Priority Queues

**Released:** Friday, Week 3 · **Due:** Friday, Week 4, 23:59
**100 points · counts toward the Problem Sets component (35% of the final grade)**

**Submit:** `ps3.py` (all code, runnable end to end) and `ps3.md` (all written answers, tables, and
proofs). Written answers inside code comments will not be marked.

Height counts **edges**; a leaf has height 0 and the empty tree has height $-1$. All heaps are
**min-heaps**, **0-indexed**, unless a question says otherwise.

---

## Part A — The Array Representation (16 points)

**A1.** *(4)* Write and test the three index functions for a **0-indexed** heap: `left(i)`,
`right(i)`, `parent(i)`.

Then state, in one sentence each:

- (a) the **depth** of index $i$, as a formula;
- (b) the range of indices that are **leaves** in a heap of $n$ elements;
- (c) the **height** of a heap of $n$ elements.

Verify (a) and (b) programmatically for $n = 1 \dots 100$.

---

**A2.** *(8)* Lecture 10 §4 describes a bug: writing `parent(i) = i // 2` — the 1-indexed formula —
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

## Part B — The Priority Queue (30 points)

Implement a class `MinHeap` with **no use of `heapq`** anywhere in Part B.

**B1.** *(6)* `sift_up(i)` and `sift_down(i)`.

`sift_down` must swap with the **smaller** of the two children. Include in `ps3.md` a three-element
array on which swapping with the *wrong* child leaves the heap property violated, and show the
resulting array.

**B2.** *(8)* `push(x)`, `pop_min()`, `peek()`, `__len__`. `pop_min` on an empty heap must raise
`IndexError`.

**B3.** *(6)* `build(xs)` — the $\Theta(n)$ construction of Lecture 11, **not** repeated insertion.

**B4.** *(6)* `check_heap()`, returning `True` iff the heap property holds at every index. Call it
after every operation in your tests, not just at the end.

**B5.** *(4)* A randomised stress test: at least 300 trials of interleaved `push` and `pop_min`,
comparing your output against `sorted()` on the same multiset, and calling `check_heap()` after every
single operation. Report the number of trials and failures.

> **Do not measure a structure you have not verified.** B5 exists so that Part D's numbers mean
> something. This was Lab 0's rule and it has not changed.

---

## Part C — Why the Build Is Linear (20 points)

**C1.** *(4)* In a complete binary tree of $n$ nodes, prove that the number of nodes at height $h$ is
at most $\lceil n / 2^{h+1} \rceil$.

**C2.** *(8)* Using C1, prove that `build` performs $O(n)$ work. Your proof must:

- write the total as a sum over heights;
- evaluate $\sum_{h=0}^{\infty} h/2^{h}$, showing your working — do not merely assert that it is 2;
- state where the $\log n$ factor went.

**C3.** *(4)* The loop `for i in range(n//2 - 1, -1, -1)` runs **backwards**. State the precondition
`sift_down(i)` requires, and explain in two sentences why running forwards violates it. Then
demonstrate it: run a forward version on 500 random arrays and report how many produce an invalid
heap.

**C4.** *(4)* Building by repeated insertion is $\Theta(n\log n)$ in the worst case, and the
$\Theta(n)$ build is $\Theta(n)$. Both call an $O(\log n)$ repair once per element.

**Explain the discrepancy in three sentences or fewer.** A complete answer mentions where the nodes
are.

---

## Part D — Measuring the Build (16 points)

**D1.** *(6)* Instrument `build` and your insertion-based build with a **swap counter**. For
$n \in \{1000, 10000, 100000\}$, tabulate the swaps performed by each on

- random input (mean of 5 seeds), and
- decreasing input $n, n-1, \dots, 1$.

**D2.** *(4)* Add a column for $n - s_2(n)$, where $s_2(n)$ is the number of 1-bits in $n$ (in Python,
`bin(n).count('1')`). Compare it to your **decreasing-input** build column and comment on what you see.

**D3.** *(6)* Answer both, citing your own numbers:

- **(a)** On random input, the ratio between the two builds is roughly **constant** in $n$; on
  decreasing input it **grows**. Explain why. What is the average number of levels a random key rises
  during an insertion, and why does that not depend on $n$?
- **(b)** Is decreasing input the **worst case** for the $\Theta(n)$ build? Check your D1 numbers
  against your D2 bound before answering. If it is not, say what that implies about testing
  worst-case performance.

> **(b) is worth reading twice.** The obvious adversarial input for one algorithm is not
> automatically the adversarial input for another, even when both build the same structure.

---

## Part E — `decrease_key` (18 points)

Dijkstra's algorithm needs to lower the priority of an item already in the queue. Both standard
solutions, then a judgement.

**E1.** *(7)* `IndexedPQ`, holding `(priority, key)` pairs with a dict `pos: key -> index` maintained
through every swap. `decrease_key(key, new_priority)` must be $O(\log n)$ and must ignore a new
priority that is not an improvement.

**E2.** *(7)* `LazyPQ` over `heapq`. `decrease_key` pushes a new entry; `pop` discards stale ones.
You may use `heapq` in Part E.

**E3.** *(4)* Cross-check both against a brute-force reference on at least 200 randomised sequences of
pushes with repeated keys. Then answer, in a short paragraph:

- Which would you ship, and why?
- `LazyPQ`'s heap can hold more than one entry per key. Bound its size in terms of the number of
  `decrease_key` calls, and say why Dijkstra's asymptotic running time is unaffected.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 16 | Index arithmetic; the parent bug and why tests miss it |
| B | 30 | A correct, verified priority queue |
| C | 20 | The linear-build proof |
| D | 16 | Measurement, and reading it honestly |
| E | 18 | `decrease_key`, both ways, with a judgement |
| **Total** | **100** | |

Partial credit throughout. **An implementation that passes B5 and a wrong analysis scores better than
a correct analysis of code that does not run.**

---

## Reference Numbers

From the machine these notes were prepared on (Python 3.14, x86-64 Linux). **Swap counts are
deterministic given the input** — yours should match. Timings, if you take any, will not.

Build swaps, **decreasing** input:

| $n$ | $\Theta(n)$ build | insertion build | $n - s_2(n)$ |
| --- | --- | --- | --- |
| 1,000 | 992 | 7,987 | 994 |
| 10,000 | 9,992 | 113,631 | 9,995 |
| 100,000 | 99,990 | 1,468,946 | 99,994 |

Build swaps, **random** input, seed 0 (single seed, so you can check one run exactly):

| $n$ | $\Theta(n)$ build | insertion build |
| --- | --- | --- |
| 1,000 | 780 | 1,342 |
| 10,000 | 7,456 | 12,688 |
| 100,000 | 74,294 | 128,207 |

Generated with `random.seed(0)` then `[random.random() for _ in range(n)]`.

**If your $\Theta(n)$ build exceeds $n - s_2(n)$ on any input, you have a bug** — that is a proven
upper bound, not an observation.

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
