# CS 102 · Computer Science II — Algorithms and Data Structures
## Week 3: Heaps and Priority Queues

**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **PS 3** (released Friday, due Friday of Week 4), Lab 3, **Quiz 3 —
which covers Week 2**.

---

### Why This Week Exists

Week 2 maintained two invariants over the same nodes — order and shape — and paid for it with
rotations, cached heights, and four cases to get right.

This week keeps the shape invariant and **throws most of the order invariant away.** A heap relates
each node only to its two children and says nothing whatever about siblings.

You lose search, which is what a BST was for. In exchange you get a tree that needs **no pointers at
all**, builds in $\Theta(n)$ rather than $\Theta(n\log n)$, sorts in place, and is the right structure
for a problem balanced BSTs handle awkwardly: *repeatedly extract the smallest thing.*

The organising idea is worth stating in advance, because it is the reverse of last week's:

> **A weaker invariant admits more configurations, and admitting more configurations is what makes it
> cheap to restore.** At $n = 8$ there are 210 legal heaps and exactly one sorted array. That freedom
> is what pays for the rigidity of completeness.

### Learning Objectives

By the end of Week 3, you should be able to:

1. State the heap property and explain why it is strictly weaker than the BST invariant — in
   particular, why a heap is **not** sorted.
2. Convert between the 0-indexed and 1-indexed index formulas without introducing the parent bug, and
   explain why that bug survives testing on sorted input.
3. Implement `sift_up` and `sift_down`, and say why `sift_down` must swap with the **smaller** child.
4. Implement the $\Theta(n)$ build and explain why the loop runs backwards.
5. **Prove** the linear bound, including the evaluation of $\sum_{h\ge0} h/2^h$, and say where the
   $\log n$ factor went.
6. Implement heap sort, state its four properties (worst case, space, stability, adaptivity), and
   compare it with merge sort **from measurements**, not from asymptotics.
7. Distinguish the priority queue ADT from the binary heap that implements it, and choose between
   implementations for a stated workload.
8. Implement `decrease_key` both ways — index map and lazy deletion — and defend a choice.
9. Explain why a binary heap makes Dijkstra's algorithm fast on sparse graphs and **not** on dense
   ones.

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L10 The Heap Property and the Array Representation.md` | The two invariants, index arithmetic, sift-up and sift-down |
| `lectures/L11 Building a Heap in Linear Time and Heap Sort.md` | The $\Theta(n)$ build proved and measured; heap sort against merge sort |
| `lectures/L12 Priority Queues and Their Applications.md` | The ADT, `heapq`, `decrease_key`, top-$k$, Dijkstra, scheduling |
| `assignments/PS 3 Heaps and Priority Queues.md` | 100 points, due Friday of Week 4 |
| `assignments/QUIZ 3 Week 3 Monday.md` | 20 points, formative — **covers Week 2** |
| `lab/LAB 3 Heap Sort versus Merge Sort.md` | Reproduce the comparison, then find what the comparison count cannot see |
| `resources/Reading Guide Week 3.md` | CLRS Chapter 6, with the indexing warning to read first |
| `solutions_instructor/` | PS 3 and Lab 3 solutions — instructor only |

### The Three Ideas Most Likely to Be Missed

**1. The linear build is linear because of *where the nodes are*, not because each call is cheap.**
The call at the root still costs $\Theta(\log n)$. The bound holds because the sum
$\sum_h \lceil n/2^{h+1}\rceil\cdot h$ converges. Sift-down is cheap for the many nodes and expensive
for the few; sift-up is the reverse. That one sentence is the whole result, and it is PS 3 C4.

**2. A heap is not a search structure, and the $\Theta(n)$ is structural.** The maximum of a min-heap
can be at any of the $\lceil n/2\rceil$ leaves, so any correct algorithm must inspect all of them. No
cleverness recovers a logarithmic bound. Measured: finding the maximum by pruned depth-first search
visits about 57% of a heap of $10^5$ elements; searching for an absent key visits 100%.

**3. Heap sort's array representation is both why it is elegant and why it is slow.** `sift_down`
doubles its stride at every step, so a large heap is effectively random access. Measured at
$n = 10^6$: heap sort's per-element cost is **3.28×** its $n = 10^3$ value where $n\log n$ predicts
**2.00×**, while merge sort's is 2.17×. The comparison count — flat at a ratio of 1.97 — cannot
explain that, and Lab 3 D1 is where you have to notice it.

### A Note on the Measurements

Every table this week was produced by running code, and the lectures say which machine.

**Swap and comparison counts are deterministic** given the input. If yours differ from the reference,
you have a bug — this is a stronger statement than last week's, because heaps have no tie-breaking
freedom once the input order is fixed. **Timings are not deterministic** and will differ.

One bound is proven rather than observed: the $\Theta(n)$ build performs at most $n - s_2(n)$ swaps,
where $s_2(n)$ counts the 1-bits of $n$. **If your build exceeds it on any input, that is a bug, not
a measurement.**

### Two Things That Are Not What They Look Like

Both are deliberate, and both are graded.

**The obvious worst case is the wrong one.** Decreasing input looks like the adversarial case for the
linear build. It is not — at $n = 10{,}000$ it does 9,992 swaps against an attainable bound of 9,995,
and over $n \le 399$ it misses the bound for 270 of the 399 sizes. It *is* the true worst case for the
insertion build. **The adversarial input for one algorithm is not automatically adversarial for
another**, even when both produce the same structure. (PS 3 D3b.) Compare Week 2, where the extremal
object — the Fibonacci tree — did serve both roles.

**A test that passes can prove nothing.** The 0-indexed parent bug produces a valid heap on increasing
input at every size tested, because an increasing sequence never consults the parent function for a
comparison that matters. It fails on 98.5% of random inputs at $n = 100$. The smallest input that
catches it at all needs **seven** elements. (PS 3 A2.)

### Connections

**Back:** Completeness is **Lecture 07's Candidate 2**, rejected for BSTs because restoring it costs
$\Theta(n)$ — it works here because a heap never has to put a *particular* key in a *particular*
place. The shape-counting argument is the same one that gave 429 BSTs against 17 AVL shapes at
$n = 7$. The contiguity advantage is what let `SortedList` beat a hand-written AVL tree by 16× in
**Lecture 09** — here we get it without giving up the asymptotics. The convergent series is **MATH
151**; the doubling-ratio method is **Lab 0**.

**Forward:** **Week 4** changes subject to graphs, and the link is tighter than it looks: a traversal
is a loop that removes a vertex from a pending collection and adds its neighbours. BFS uses a queue,
DFS a stack, and **Dijkstra uses this week's heap** — one algorithm skeleton, three data structures.
**Week 5** builds Dijkstra properly and needs PS 3 Part E's `decrease_key`. **Week 6**'s Union-Find
has an amortised bound with the same shape as this week's build argument. **Week 9** builds Huffman
codes by repeatedly extracting the two smallest frequencies, which is a priority queue and nothing
else.

---

*CS 102 · Week 3 · © CSE Department*
