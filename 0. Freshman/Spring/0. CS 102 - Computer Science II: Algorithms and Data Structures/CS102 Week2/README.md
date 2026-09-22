# CS 102 · Computer Science II — Algorithms and Data Structures
## Week 2: Balanced BSTs — AVL Trees and Red-Black Trees

**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **PS 2** (released Fri 5 Feb 10:00, due **Fri 12 Feb 17:00**), Lab 2 (**Tue 9 Feb**, 15:00), **Quiz 2** (Mon 1 Feb, 09:00) — which covers Week 1.

---

### Why This Week Exists

Week 1 ended on an unresolved problem: every BST operation costs $\Theta(h)$, and nothing in the BST
invariant constrains $h$. Sorted input — the most ordinary input there is — produces a tree of height
$n-1$.

This week resolves it, and the resolution is a single idea: **add a second invariant, about shape,
and find an $O(1)$ operation that repairs it.** The second invariant is height-balance; the operation
is the rotation. Everything else follows.

The result is a genuine guarantee rather than an expectation. **41 comparisons, worst case, on a
billion keys**, with no assumption whatsoever about the order the keys arrived in.

### Learning Objectives

By the end of Week 2, you should be able to:

1. Explain why sorted input is the BST's worst case and why that matters more than an adversarial one.
2. Evaluate a candidate balance invariant on two axes — does it force $h = O(\log n)$, and can it be
   restored cheaply — and say why the *weakest* sufficient invariant is the right one.
3. Perform left and right rotations, and prove correctness by the inorder argument rather than by
   case analysis.
4. Classify an imbalance into LL, RR, LR, or RL, and explain **why the double-rotation cases cannot
   be fixed with one rotation**.
5. Implement AVL insertion with cached heights, and say why the two `update_height` calls are ordered
   as they are.
6. Derive $N(h) = N(h-1)+N(h-2)+1 = F(h+3)-1$ and the bound $h < 1.4404\log_2(n+2) - 1.3277$.
7. State the five red-black properties and reproduce the two-step argument for $h \le 2\log_2(n+1)$.
8. Choose between AVL and red-black for a stated workload, **citing measurements rather than
   asymptotics** — the asymptotics are identical.
9. Explain what changes about the cost model on disk, and why B-trees follow from it.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L07 Why Balance Matters and Rotations]] | Candidate invariants, the rotation, the four cases |
| [[L08 AVL Trees Insertion Height and Deletion]] | Insertion, the height bound proved, the insert/delete asymmetry |
| [[L09 Red-Black Trees B-Trees and What Practice Uses]] | Five properties, AVL vs RB measured, B-trees, `SortedList` |
| [[PS 2 Balanced BSTs and Rotations]] | 100 points, due Fri 12 Feb 17:00 |
| [[CS102 Week2/assignments/QUIZ 2 Week 2 Monday\|QUIZ 2 Week 2 Monday]] | 20 points, formative — **covers Week 1** |
| [[LAB 2 BST versus AVL on Sorted Input]] | Reproduce the gap, then find where balancing stops paying |
| [[CS102 Week2/resources/Reading Guide Week 2\|Reading Guide Week 2]] | CLRS §13.1–13.4 and §18.1, with guiding questions |
| `solutions_instructor/` | PS 2 and Lab 2 solutions — instructor only |

### The Three Ideas Most Likely to Be Missed

**1. Insertion and deletion are not symmetric.** An insertion triggers at most one rebalance, because
the rotation gives back exactly the level the insertion added. A deletion's rotation can *lower* the
subtree, creating a fresh violation above it — so the repair propagates. Measured: 9 rotations for a
single deletion on a tree of 10,945 nodes. This is PS 2 D1 and it is on the midterm.

**2. The height bound's constant is routinely misquoted.** The bound is
$1.4404\log_2(n{+}2) - 1.3277$. The $n{+}1$ version circulates widely and **is false** — it fails at
$n = 2, 7, 20, 54, \dots$, which are precisely the sizes where the worst case occurs. PS 2 C3 makes
you find them.

**3. "Red-black trees rotate less than AVL trees" is only half true.** On sorted insertions the two
are within 0.02% of each other, and the red-black tree is nearly twice as tall. The real advantage is
in *deletion* — at most 3 rotations against $\Theta(\log n)$ — which insert-only benchmarks, including
the one in Lecture 09, do not show.

### A Note on the Measurements

Every table in this week's material was produced by running code, and the lectures say which machine.
**Two columns are deterministic and two are not.** Heights and rotation counts depend only on the
input sequence — if yours differ from the reference, you have a bug. Timings depend on your machine
and will differ; if yours are *better* than the reference, suspect a bug rather than a fast laptop.

### Connections

**Back:** The BST invariant from **Week 1** is carried over untouched — an AVL tree is a BST with one
extra condition, and every search you wrote last week runs on it unmodified. The Fibonacci numbers
and strong induction are **MATH 151**. The doubling-ratio method for reading a timing table is
**Lab 0**.

**Forward:** **Week 3**'s heap keeps a shape invariant and discards the ordering one, and the payoff
is a tree with no pointers at all — `SortedList`'s internal index, which you meet in Lecture 09, is
that idea arriving three days early. **Week 5** uses a heap-backed priority queue for Dijkstra.
**Week 8**'s optimal BSTs return to this week's structures and ask a different question: not how to
keep a tree balanced, but how to shape it around a known access distribution — for which balance
turns out to be the *wrong* objective.

---

*CS 102 · Week 2 · © CSE Department*
