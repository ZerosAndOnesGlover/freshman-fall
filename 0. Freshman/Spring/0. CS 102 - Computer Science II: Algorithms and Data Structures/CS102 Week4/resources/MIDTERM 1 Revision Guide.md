# CS 102 · MIDTERM 1 — Revision Guide

**Announced:** Week 4 · **Sat:** Monday 1 March 2027, 18:00–19:15 · Week 6 (evening, VNC 100)
**Covers Weeks 0–4** · **Worth 12.5%** of the final grade

**75 minutes.** Closed book. **One handwritten sheet, one side**, of your own notes is permitted. No
calculators — every number on the paper is exact or is a complexity class.

*(Format and weight per the Course Overview Syllabus. Midterms are 25% of the course, split equally
between this paper and Midterm 2 on Monday 29 March, Week 10. The date follows the registry's
ASSESSMENT CALENDAR, which pins Midterm 1 to Week 6.)*

---

## Format

| section | marks | content |
| --- | --- | --- |
| A — short answer | 20 | 8–10 one-or-two-sentence questions across all five weeks |
| B — trace and compute | 25 | Execute algorithms by hand on small inputs |
| C — proof | 25 | Two proofs from the list below |
| D — design and judgement | 30 | Choose a structure for a stated workload and defend it |
| **Total** | **100** | **75 minutes** |

**Section D is where the marks are lost.** It is not a recall question. You will be given a workload —
sizes, operation mix, memory budget — and asked which structure to use and why, and a correct answer
with no justification scores about a third.

---

## What Is Examinable

### Week 0 — Analysis

- Big-O, $\Theta$, $\Omega$ — and the difference, stated precisely.
- Reading a doubling-ratio table: ratio 2 is linear, 4 is quadratic, slightly over 2 is $n\log n$.
- Proof by induction as algorithm verification.
- **Measure before optimising**, and why a benchmark that does not state its machine is not a result.

### Week 1 — Trees and BSTs

- Terminology: root, leaf, height, depth. **Height counts edges; the empty tree is $-1$.** This
  convention is used without exception and the paper assumes it.
- The four traversals, and reconstructing a tree from two of them.
- BST insert, search, delete — all three deletion cases.
- Predecessor and successor.
- Why sorted input produces a height of $n-1$, and why that is worse than an adversarial worst case.

### Week 2 — Balanced BSTs

- The AVL invariant and balance factors.
- Rotations, and **the inorder argument for their correctness** — not a case analysis.
- The four cases, LL/RR/LR/RL, and **why the double-rotation cases cannot be done with one rotation**.
- $N(h) = N(h-1) + N(h-2) + 1 = F(h+3) - 1$, and the bound $h < 1.4404\log_2(n+2) - 1.3277$.
  **Note the $n+2$**; the $n+1$ form circulates widely and is false.
- The five red-black properties and the two-step $h \le 2\log_2(n+1)$ argument.
- The insert/delete asymmetry: insertion rebalances at most once, deletion up to $\Theta(\log n)$
  times.

**Not examinable:** red-black insertion or deletion *code*; B-tree algorithms beyond the fan-out
arithmetic.

### Week 3 — Heaps

- The heap property, and that **a heap is not sorted**.
- 0-indexed index arithmetic, and converting from CLRS's 1-indexed formulas.
- `sift_up`, `sift_down`, and why `sift_down` must take the **smaller** child.
- The $\Theta(n)$ build: the algorithm, why the loop runs backwards, and **the proof**, including
  evaluating $\sum_{h\ge0} h/2^h = 2$.
- Heap sort: $\Theta(n\log n)$ worst case, $O(1)$ space, not stable, not adaptive.
- The priority queue ADT against its implementations.

### Week 4 — Graphs

- Terminology; the handshake lemma; sparse against dense.
- Both representations, their costs, and **when each is right**.
- BFS: the algorithm, the queue-monotonicity invariant, and the shortest-path proof.
- DFS: timestamps, the parenthesis theorem, the four edge types.
- **Back edge $\iff$ cycle**, and that undirected graphs have only tree and back edges.
- Components and bipartiteness.

---

## Proofs You Should Be Able to Reproduce

Section C draws two from this list. Each is a proof done in lecture or set on a problem set.

1. A rotation preserves the inorder sequence. *(L07)*
2. $N(h) = F(h+3) - 1$, by induction. *(L08, PS 2 D1)*
3. The AVL height bound from $N(h)$. *(L08)*
4. A red-black tree with black-height $bh$ has at least $2^{bh} - 1$ internal nodes, hence
   $h \le 2\log_2(n+1)$. *(L09)*
5. **`BUILD-HEAP` is $\Theta(n)$**, including the series evaluation. *(L11, PS 3 C2)*
6. **BFS computes shortest paths**, via queue monotonicity. *(L14, CLRS Thm 20.5)*
7. A directed graph is cyclic iff DFS finds a back edge. *(L15)*
8. In an undirected graph, every edge is a tree edge or a back edge. *(L15)*

**Proofs 5 and 6 are the two most likely to appear.** Both are short, both have a single load-bearing
idea, and both were set on a problem set with full solutions posted.

---

## The Numbers Worth Carrying

You will not be asked to recall measurements. You may be asked what a measurement *implies*, so carry
the shapes rather than the digits.

| fact | shape |
| --- | --- |
| AVL height bound | $\approx 1.44\log_2 n$ — 44% above perfect |
| red-black height bound | $2\log_2 n$ — twice perfect |
| AVL insert vs delete rotations | $\le 2$ against $\Theta(\log n)$ |
| red-black insert vs delete rotations | $\le 2$ against $\le 3$ |
| heap height | exactly $\lfloor\log_2 n\rfloor$ |
| $\Theta(n)$ build, total swaps | $< n$ — precisely $n - s_2(n)$ at most |
| heap sort vs merge sort comparisons | $\approx 2n\log n$ against $\approx n\log n$ |
| BFS/DFS | $\Theta(V+E)$ list, $\Theta(V^2)$ matrix |

---

## The Three Ideas the Course Has Repeated

Every week so far has made the same three points in a different setting. Section D is built on them,
and if you can state each in one sentence with two examples you are ready for it.

**1. The weakest sufficient invariant is the right one.** Size-balance permits 1 tree shape at $n=7$,
AVL permits 17, and only the second can be repaired in $O(1)$. A heap's parent-child ordering is
weaker still, and that is what buys the $\Theta(n)$ build and the pointer-free layout.

**2. Asymptotics do not settle which implementation is faster at your $n$.** `SortedList` beats a
hand-written AVL tree by 16× with worse complexity. `sorted()` beats `heapq.merge` by 2.4×. Heap sort
loses to merge sort by 1.6× despite identical bounds. Each has a specific cause, and "it's the
constant factor" is not an answer.

**3. A bound is a count of operations, not a promise about time.** BFS is $\Theta(V+E)$ and its cost
per edge grows 5× on random graphs and 1.5× on grids across the same size range. `sift_down` doubles
its stride every step. Memory locality is not in the notation.

---

## How to Revise

**Do not reread the lectures.** Work the problem sets again without looking at your solutions — PS 1
through PS 4 are due before the paper — PS 4 on Friday 26 February.

In order of value:

1. **Re-derive proofs 5 and 6 from scratch**, on paper, without notes.
2. **Redraw the four AVL rotation cases from memory.** Most rotation errors are drawing errors.
3. **Hand-trace** an AVL insertion sequence, a `BUILD-HEAP`, and a DFS with timestamps on a 7-vertex
   graph. Section B is exactly this.
4. Reread the "Three Ideas Most Likely to Be Missed" section of each week's README. That is four short
   pages and covers most of Section A.
5. Only then reread lecture material, and only the sections your own attempts showed you needed.

---

## Practical

- **Week 5's lectures and Lecture 19 (the morning of the paper)** are *not* on this paper, even
  though they come before it.
- **Quiz 5** (Monday 22 February) covers Week 4 — the same material as
  Section A of this paper. Treat it as a rehearsal.
- **PS 4 is due Friday 26 February**, before the paper, and all of it is examinable.
- Past papers are on the course page. The two most recent are the best guide to Section D's style;
  earlier ones predate the current graph syllabus.

---

*CS 102 · MIDTERM 1 Revision Guide · © CSE Department*
