# CS 102 · Problem Set 2
## Balanced BSTs: AVL Insertion, Rotations, and the Height Bound

**Released:** Friday of Week 2 · **Due:** Friday of Week 3, start of lecture
**100 points** · Contributes to the Problem Sets component (35% of the course grade)

**Submit:** `ps2.py` (Parts A–C) and `ps2.pdf` or `ps2.md` (Parts D–E). Code must run end to end
under `python3 ps2.py` with no arguments.

**Conventions.** Height counts **edges**; the empty tree has height $-1$; a leaf has height $0$.
$\mathrm{bf}(v) = h(v.\text{left}) - h(v.\text{right})$.

---

## Part A — Rotations (16 pts)

Start from the `Node` class in Lecture 08.

**A1.** *(4)* `rotate_right(y)` and `rotate_left(x)`. Each returns the new subtree root and updates
both affected heights **in the correct order**.

**A2.** *(4)* `check_bst(t)` — verify the BST invariant as a **subtree** condition, using the
bounds-passing method from Week 1. Not the child-only test.

**A3.** *(8)* `test_rotation_preserves_order()` — build **at least 500** random BSTs, apply a rotation
at the root in whichever directions are legal, and assert the inorder sequence is unchanged.

> Your test must actually be able to fail. Before submitting, deliberately break `rotate_right` so
> that it moves the **wrong subtree** — for instance `y.left = x.left` in place of `y.left = x.right`
> — confirm the test catches it, then restore. **State in a comment what you broke and what the test
> reported.** Four of the eight points are for this.
>
> Note which breakages this test can and cannot catch. Swapping the two `update_height` calls leaves
> the inorder sequence perfectly correct, so **A3 will not detect it.** That failure needs B3, and
> noticing the gap now is the point of asking.

---

## Part B — AVL Insertion (30 pts)

**B1.** *(4)* `height(t)` and `bf(t)`, both handling `None`. `update_height(t)`.

**B2.** *(14)* `avl_insert(t, key)` — BST insertion followed by rebalancing on the way up, handling
all four cases (LL, RR, LR, RL). Duplicate keys leave the tree unchanged.

**B3.** *(6)* `check_avl(t)` — a single recursive pass returning the height and raising on any of:
BST order violated, a **stored** height that disagrees with the recomputed one, or $|\mathrm{bf}| > 1$.

> The stored-height check is the one that catches the real bugs. A tree can satisfy the BST invariant
> and the balance condition while carrying wrong cached heights, and it will then silently fail to
> rebalance later.

**B4.** *(6)* Stress test: at least 200 trials, each inserting a random number of random keys (allow
duplicates and negatives), calling `check_avl` after **every** insertion and comparing the inorder
sequence against `sorted(set(keys))`.

---

## Part C — Measuring (18 pts)

**C1.** *(6)* Build an AVL tree from the sorted keys $0 \dots n-1$ for
$n \in \{1000, 10000, 100000\}$ and tabulate its height against $\lceil\log_2(n+1)\rceil - 1$.

Build a **plain BST** from the same keys for $n \in \{1000, 10000\}$ only, and add its height to the
table.

> **Do not attempt the plain BST at $n = 100{,}000$.** Building it is $\Theta(n^2)$ — about
> $5\times10^9$ pointer steps, and **307 seconds** on the reference machine. Instead, **state its height
> without building it and justify the claim in one sentence.** Being blocked by the quadratic cost is
> the intended experience; note in your write-up roughly how long you estimate it would take, and how
> you got the estimate.

**C2.** *(6)* Count rotations. Report total single-rotations performed while building each AVL tree
above, and separately the **maximum performed by any one insertion**.

**C3.** *(6)* Do the same for **random** input at all three sizes, averaged over 5 seeds. Report BST
height, AVL height, and total rotations. The plain BST *is* feasible here at $n = 100{,}000$ — say
why, in one sentence.

Report all three tables in your write-up. **Your numbers will differ from the lectures' in the timing
columns and should not differ in the height or rotation columns** — heights and rotation counts are
deterministic given the input. If yours differ, something is wrong; say so.

---

## Part D — The Height Bound (24 pts)

**D1.** *(8)* Let $N(h)$ be the minimum number of nodes in an AVL tree of height $h$. Justify the
recurrence $N(h) = N(h-1) + N(h-2) + 1$ with $N(0)=1$, $N(1)=2$, then **prove by strong induction**
that $N(h) = F(h+3) - 1$, where $F(0)=0$, $F(1)=1$.

**D2.** *(6)* Using $F(k) > \varphi^{k}/\sqrt5 - \tfrac12$, derive an upper bound on $h$ in terms of
$n$. Show your arithmetic; do not quote the boxed result from Lecture 08.

**D3.** *(6)* Lecture 08 warns that the bound is often misquoted with $n+1$ inside the logarithm.
**Find the three smallest $n$ at which the $n+1$ form fails**, and say in one sentence what is
special about those values of $n$.

**D4.** *(4)* An AVL tree has height 10. Give the smallest and largest possible number of nodes.
Justify both.

---

## Part E — Reasoning (12 pts)

Short answers. One paragraph each; the marks are for the argument, not the length.

**E1.** *(3)* Lecture 08 asserts that an insertion triggers **at most one** rebalance event, while a
deletion may trigger one at every level. Explain the difference in terms of what happens to the
*height of the rotated subtree* in each case.

**E2.** *(3)* Both AVL and red-black trees are $\Theta(\log n)$ for all three operations. Give one
workload where you would choose AVL and one where you would choose red-black, and justify each from
the measured data in Lecture 09 — not from the asymptotics, which are identical.

**E3.** *(3)* A colleague proposes a simpler invariant: *at every node, the left and right subtree
**sizes** differ by at most 1.* This does force $h = O(\log n)$. Give a concrete insertion sequence
showing why it is nonetheless a bad choice, and state what it costs.

**E4.** *(3)* `SortedList` has worse asymptotic insertion complexity than an AVL tree and is 16×
faster in the measurement in Lecture 09. Explain the discrepancy, and then state a condition under
which the AVL tree would win.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 16 | Rotations, and a test that can fail |
| B | 30 | AVL insertion, all four cases, verified |
| C | 18 | Measurement |
| D | 24 | The height bound, proved |
| E | 12 | Reasoning |
| **Total** | **100** | |

**Late policy:** as per the syllabus — 10% per day, up to three days.

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
