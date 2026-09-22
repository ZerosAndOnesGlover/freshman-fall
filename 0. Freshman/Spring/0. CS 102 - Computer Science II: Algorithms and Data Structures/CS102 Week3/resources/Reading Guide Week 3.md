# CS 102 · Reading Guide, Week 3
## Heaps and Priority Queues

---

## Required

**CLRS, 4th ed. — Chapter 6, all of it** (Heapsort). Six sections, about 25 pages.

This is the first week whose primary reading is short, self-contained, and entirely on the syllabus.
Chapter 6 is one of the best-constructed chapters in CLRS: it builds one structure, proves one
surprising theorem about it, and derives two applications. **Read all of it.**

Also useful:

- **The `heapq` module documentation** — short, and the "Theory" section at the end is worth reading
  even though it is idiosyncratic.
- **Sedgewick & Wayne §2.4** — priority queues, with the best diagrams of sift-up and sift-down
  anywhere. Their code is 1-indexed with `a[0]` deliberately unused, which is a third convention;
  see the warning below.
- **Skiena §3.5 and §4.3** — the practitioner's view, and a good discussion of when a priority queue
  is the wrong answer.

---

## The Indexing Warning — Read This First

**Three conventions appear in your sources, and they do not agree.**

| source | root at | left child | right child | parent |
| --- | --- | --- | --- | --- |
| CLRS Ch. 6 | index 1 | $2i$ | $2i+1$ | $\lfloor i/2 \rfloor$ |
| Sedgewick | index 1, `a[0]` unused | $2i$ | $2i+1$ | $\lfloor i/2 \rfloor$ |
| **Python `heapq`, and this course** | **index 0** | $2i+1$ | $2i+2$ | $\lfloor (i-1)/2 \rfloor$ |

Every formula in CLRS Chapter 6 is 1-indexed. Every line of code you write for PS 3 is 0-indexed.
**Do not transcribe formulas across that boundary without converting them.**

The specific failure is well documented in Lecture 10 §4: writing `parent(i) = i // 2` in 0-indexed
code produces a function that is correct for every odd index and wrong for every even one, which
means it handles left children and mishandles right children. It **passes on increasing input at
every size tested**, and the smallest input that catches it needs seven elements.

If you read CLRS with a pen, convert as you go and write the 0-indexed form in the margin.

---

## How to Read Chapter 6

**§6.1 (heaps, 3 pages).** The definitions and the index arithmetic. Note that CLRS distinguishes
`heap-size` from `length` — this matters in §6.4, where heap sort shrinks the heap inside an array
that does not shrink. Our `sift_down(a, i, n)` takes `n` as a parameter for the same reason.

**§6.2 (`MAX-HEAPIFY`, 4 pages).** This is our `sift_down`. Read the recurrence
$T(n) \le T(2n/3) + \Theta(1)$ and understand where $2n/3$ comes from — it is the worst-case size of a
child subtree when the last level is half full, and it is the least obvious line in the chapter.

**§6.3 (`BUILD-MAX-HEAP`, 4 pages).** **The most important four pages of the week.** Read the loop
invariant, then read the tighter analysis on the second pass. Figure 6.3 is the proof of Lecture 11
§3 in a picture — the nodes are drawn at the heights they are counted at.

**§6.4 (`HEAPSORT`, 3 pages).** Short. The loop invariant is the thing to retain.

**§6.5 (priority queues, 6 pages).** `HEAP-EXTRACT-MAX`, `HEAP-INCREASE-KEY`, `MAX-HEAP-INSERT`. Note
that CLRS's `HEAP-INCREASE-KEY` assumes you already hold the element's index. **CLRS does not tell
you how to find it**, and that omission is the whole subject of Lecture 12 §3 and PS 3 Part D.

**Problem 6-2 (d-ary heaps)** is worth attempting. It is the natural generalisation, it is a plausible
exam question, and it is the reason B-trees looked familiar last week.

---

## Guiding Questions

Answer these as you read. They are not submitted, and three of them are on the midterm.

1. §6.1: a heap is a complete binary tree, and a complete binary tree on $n$ nodes is **unique**.
   What follows about how much information the pointers in a pointer-based tree were carrying?

2. §6.2: where does $T(n) \le T(2n/3) + \Theta(1)$ come from? Draw the shape that achieves $2n/3$.

3. §6.3: the loose analysis gives $O(n\log n)$ and the tight one gives $O(n)$. **Both are correct
   upper bounds.** What exactly was wrong with the first — was it the number of calls, or the cost
   per call?

4. §6.3 again: the loop runs from $\lfloor n/2 \rfloor$ down to 1. State the precondition of
   `MAX-HEAPIFY(A, i)` and say why the descending order is what establishes it.

5. §6.4: heap sort uses a **max**-heap to produce **ascending** output. Trace $n = 4$ and say why.

6. §6.5: `HEAP-INCREASE-KEY` takes an index $i$. In a real application — Dijkstra — where would that
   index come from? What would it cost to find it if you had not been maintaining it?

7. Compare the heap with Week 2's AVL tree on the six operations in Lecture 12 §1. **Name a workload
   for which the AVL tree is the better choice**, and one for which it is not.

---

## Common Misreadings

**"A heap is a sorted array."** It is not, and this is the misconception that causes the most damage.
`[1, 2, 3]` and `[1, 3, 2]` are both valid min-heaps. A heap constrains parents against children and
says **nothing** about siblings.

**"The heap property gives you binary search."** No. Searching a heap for an arbitrary key is
$\Theta(n)$, and the bound is structural rather than a defect of any particular algorithm: the
maximum of a min-heap may be at any of the $\lceil n/2\rceil$ leaves, so any correct method must
inspect all of them.

**"`BUILD-MAX-HEAP` is $O(n)$ because each call is $O(1)$."** Each call is not $O(1)$; the call at the
root costs $\Theta(\log n)$. The bound is linear because the sum
$\sum_h \lceil n/2^{h+1}\rceil \cdot h$ converges, not because any individual term is small.

**"Heap sort is faster than merge sort because it is in place."** In place is about *space*. Measured
in Lecture 11 §6, heap sort is **1.6× slower** at $n = 10^6$, and the gap grows with $n$. It is
chosen for its worst-case guarantee in $O(1)$ space, not for speed.

**"`heapq._siftup` sifts up."** It sifts **down**. CPython's naming is inverted relative to CLRS and
to this course — see Lecture 12 §2 before reading that source.

---

## If You Have Extra Time

**Fibonacci heaps** (CLRS Chapter 19) achieve $O(1)$ amortised `insert` and `decrease_key`, which
improves Dijkstra's bound to $O(E + V\log V)$. They are also notoriously slow in practice — large
constants, poor locality, and an implementation complexity out of all proportion to the gain. Reading
the first two pages of Chapter 19 is worthwhile; implementing one is not, yet.

**`d`-ary heaps.** Increasing the branching factor makes the tree shallower ($\log_d n$) and
`sift_up` cheaper, at the cost of $d-1$ comparisons per level in `sift_down`. For Dijkstra on a dense
graph, $d = E/V$ is a genuine optimisation. Problem 6-2 works through it, and it is the same
node-size-versus-depth trade you saw with B-trees in Week 2 — with the cache in place of the disk.

---

*CS 102 · Week 3 · Reading Guide · © CSE Department*
