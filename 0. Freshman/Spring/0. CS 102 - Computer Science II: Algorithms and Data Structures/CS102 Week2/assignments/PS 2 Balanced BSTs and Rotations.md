# CS 102 · Problem Set 2
## Balanced BSTs: AVL Insertion, Rotations, and the Height Bound

**Released:** Friday 5 February 2027, 10:00 (after L09) · Week 2
**Due:** Friday 12 February 2027, 17:00 · Week 3 — late penalty from 17:01 (syllabus late policy)
**Points:** 100 · counts toward the Problem Sets component (35%, lowest one dropped)
**Expected time:** about 4–5 hours

**Submit:** `ps2.py` (Parts A–B) and `ps2.pdf` or `ps2.md` (Parts C–D). Code must run end to end
under `python3 ps2.py` with no arguments.

**Conventions.** Height counts **edges**; the empty tree has height $-1$; a leaf has height $0$.
$\mathrm{bf}(v) = h(v.\text{left}) - h(v.\text{right})$.

## What this problem set uses

Weeks 0–2: the BST from Week 1 (L05, including bounds-passing validation), rotations and the four
cases (L07), AVL insertion, the height bound and deletion (L08), and the red-black and `SortedList`
comparisons (L09). Strong induction is MATH 151.

**Not needed and not expected:** red-black insertion or deletion code (L09 says it is not examined),
heaps (Week 3). **Measuring build heights and rotation counts is Lab 2's job, not this set's.**

---

## Part A — Rotations (20 pts)

Start from the `Node` class in Lecture 08.

**A1.** *(5)* `rotate_right(y)` and `rotate_left(x)`. Each returns the new subtree root and updates
both affected heights **in the correct order**.

**A2.** *(5)* `check_bst(t)` — verify the BST invariant as a **subtree** condition, using the
bounds-passing method from Week 1. Not the child-only test.

**A3.** *(10)* `test_rotation_preserves_order()` — build **at least 500** random BSTs, apply a rotation
at the root in whichever directions are legal, and assert the inorder sequence is unchanged.

> Your test must actually be able to fail. Before submitting, deliberately break `rotate_right` so
> that it moves the **wrong subtree** — for instance `y.left = x.left` in place of `y.left = x.right`
> — confirm the test catches it, then restore. **State in a comment what you broke and what the test
> reported.** Five of the ten points are for this.
>
> Note which breakages this test can and cannot catch. Swapping the two `update_height` calls leaves
> the inorder sequence perfectly correct, so **A3 will not detect it.** That failure needs B3, and
> noticing the gap now is the point of asking.

---

## Part B — AVL Insertion (36 pts)

**B1.** *(5)* `height(t)` and `bf(t)`, both handling `None`. `update_height(t)`.

**B2.** *(16)* `avl_insert(t, key)` — BST insertion followed by rebalancing on the way up, handling
all four cases (LL, RR, LR, RL). Duplicate keys leave the tree unchanged.

**B3.** *(8)* `check_avl(t)` — a single recursive pass returning the height and raising on any of:
BST order violated, a **stored** height that disagrees with the recomputed one, or $|\mathrm{bf}| > 1$.

> The stored-height check is the one that catches the real bugs. A tree can satisfy the BST invariant
> and the balance condition while carrying wrong cached heights, and it will then silently fail to
> rebalance later.

**B4.** *(7)* Stress test: at least 200 trials, each inserting a random number of random keys (allow
duplicates and negatives), calling `check_avl` after **every** insertion and comparing the inorder
sequence against `sorted(set(keys))`.

---

## Part C — The Height Bound (28 pts)

**C1.** *(9)* Let $N(h)$ be the minimum number of nodes in an AVL tree of height $h$. Justify the
recurrence $N(h) = N(h-1) + N(h-2) + 1$ with $N(0)=1$, $N(1)=2$, then **prove by strong induction**
that $N(h) = F(h+3) - 1$, where $F(0)=0$, $F(1)=1$.

**C2.** *(7)* Using $F(k) > \varphi^{k}/\sqrt5 - \tfrac12$, derive an upper bound on $h$ in terms of
$n$. Show your arithmetic; do not quote the boxed result from Lecture 08.

**C3.** *(7)* Lecture 08 warns that the bound is often misquoted with $n+1$ inside the logarithm.
**Find the three smallest $n$ at which the $n+1$ form fails**, and say in one sentence what is
special about those values of $n$.

**C4.** *(5)* An AVL tree has height 10. Give the smallest and largest possible number of nodes.
Justify both.

---

## Part D — Reasoning (16 pts)

Short answers. One paragraph each; the marks are for the argument, not the length.

**D1.** *(4)* Lecture 08 asserts that an insertion triggers **at most one** rebalance event, while a
deletion may trigger one at every level. Explain the difference in terms of what happens to the
*height of the rotated subtree* in each case.

**D2.** *(4)* Both AVL and red-black trees are $\Theta(\log n)$ for all three operations. Give one
workload where you would choose AVL and one where you would choose red-black, and justify each from
the measured data in Lecture 09 — not from the asymptotics, which are identical.

**D3.** *(4)* A colleague proposes a simpler invariant: *at every node, the left and right subtree
**sizes** differ by at most 1.* This does force $h = O(\log n)$. Give a concrete insertion sequence
showing why it is nonetheless a bad choice, and state what it costs.

**D4.** *(4)* `SortedList` has worse asymptotic insertion complexity than an AVL tree and is 16×
faster in the measurement in Lecture 09. Explain the discrepancy, and then state a condition under
which the AVL tree would win.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 20 | Rotations, and a test that can fail |
| B | 36 | AVL insertion, all four cases, verified |
| C | 28 | The height bound, proved |
| D | 16 | Reasoning |
| **Total** | **100** | |

**Late policy:** as per the syllabus.

---

## Advice

**Draw the four cases before you write the four cases.** Almost every failure on this problem set is
a rotation applied to the wrong node or in the wrong direction, and it is much easier to see on paper
than in a debugger.

**Get B3 working before B2 is finished.** A checker you trust turns "it broke somewhere" into "it
broke on this insertion, at this node, with this balance factor." Building the verifier first is a
habit this course will keep rewarding.

**Do not test only with distinct sorted keys.** Sorted input exercises LL and RR and never touches LR
or RL, and a tree that handles only the single-rotation cases will pass a sorted-input test
perfectly.

---

*CS 102 · Week 2 · Problem Set 2 · © CSE Department*
