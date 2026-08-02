# CS 102 — Week 1 Reading Guide
## Binary Trees and Binary Search Trees

**Assigned:** CLRS Chapter 12 (Binary Search Trees), §12.1–12.3. Roughly 20 pages.
**Optional:** CLRS §12.4 (randomly built BSTs); Sedgewick & Wayne §3.2.

---

## Required

### CLRS §12.1 — What is a binary search tree?
The invariant and the inorder-traversal theorem. **Read Theorem 12.1's proof carefully** — it is the
induction that Lecture 05 §2 sketched, done properly, and Problem Set 1 E1 asks you to reproduce it.

> **Guiding question:** CLRS states the invariant as a condition on *subtrees*, not on immediate
> children. Construct a 5-node tree satisfying the child-only condition but not the subtree
> condition. **If you cannot, you have not understood the distinction** — and it is the single most
> common BST bug.

### CLRS §12.2 — Querying a binary search tree
Search, minimum, maximum, successor, predecessor. All $O(h)$.

> **Guiding question:** `TREE-SUCCESSOR` has two cases and the second walks *upward*. Trace it on a
> node with no right child that is the right child of its parent. **How far up can the walk go?**
> What does that say about the complexity?

### CLRS §12.3 — Insertion and deletion
Deletion's three cases, and CLRS's `TRANSPLANT` helper.

> **Guiding question:** CLRS uses the **successor** in the two-child case. Rewrite the case to use the
> predecessor instead. Is the result still a BST? Is it the *same* tree? Problem Set 1 C3 depends on
> your answer.

---

## Optional

### CLRS §12.4 — Randomly built binary search trees
The proof that expected height is $O(\log n)$. **Mathematically demanding** — it uses Jensen's
inequality and exponential height — and it is genuinely optional for this course. Read it if you
enjoyed MATH 151's harder material; Lecture 06 gives you the results without the proof.

### Sedgewick & Wayne §3.2
The same material with excellent diagrams and animations. **If Lecture 05's deletion did not land,
read this before rereading CLRS.**

---

## A Note on the Height Constants

Lecture 06 quoted two different constants and they are easy to confuse:

| Quantity | Asymptotic | In $\log_2$ terms |
| --- | --- | --- |
| Average node **depth** (typical search cost) | $2\ln n - 2.85$ | $\approx 1.386\log_2 n$ |
| Expected **height** (worst search cost) | $4.311\ln n$ | $\approx 2.99\log_2 n$ |

**These answer different questions.** Depth is about the average node; height is about the deepest
one. A structure can have excellent average depth and still have a long thin branch.

The depth formula is exact and matches measurement closely. **The height constant is asymptotic and
converges very slowly** — at $n=1000$ the true mean is around 20, not the 29.8 the formula suggests.
Lab 1 Part D asks you about exactly this.

---

## Before Week 2

- [ ] CLRS §12.1–12.3 read
- [ ] Lab 1 complete
- [ ] Problem Set 1 started — **it is due Friday of Week 2 and Part E takes longer than it looks**
- [ ] You can delete a node with two children on paper without looking anything up

**Week 2 adds a second invariant on top of the BST invariant.** Everything from this week carries
over unchanged, so gaps here will not close by themselves.
