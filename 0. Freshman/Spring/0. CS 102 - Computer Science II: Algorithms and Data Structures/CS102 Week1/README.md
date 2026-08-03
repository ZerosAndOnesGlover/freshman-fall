# CS 102 · Computer Science II — Algorithms and Data Structures
## Week 1: Binary Trees and Binary Search Trees

**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **PS 1** (released Friday, due Friday of Week 2), Lab 1, **Quiz 1 —
which covers Week 0**.

---

### Why This Week Exists

Every structure in CS 101 was linear, and linear structures force a choice you cannot escape: a
sorted array searches in $\Theta(\log n)$ but inserts in $\Theta(n)$; a linked list inserts in
$\Theta(1)$ but searches in $\Theta(n)$.

**Trees get both** — and the price is maintaining an invariant. That trade, *an invariant maintained
cheaply on every update buys a guarantee on every query*, is the recurring theme of Weeks 1–3 and is
worth naming now.

The week ends on a problem rather than a resolution. A BST's operations all cost $\Theta(h)$, and
nothing in the structure controls $h$: **sorted input produces a degenerate tree of height $n-1$**,
and sorted input is not adversarial, it is what a database export looks like. Week 2 fixes it.

### Learning Objectives

By the end of Week 1, you should be able to:

1. Use tree terminology precisely — **depth counts up to the root, height counts down to a leaf** — under the edge-counting convention.
2. Prove that a perfect binary tree of height $h$ has $2^{h+1}-1$ nodes, and derive $h \ge \lceil\log_2(n+1)\rceil - 1$.
3. Implement all four traversals and say what each is for; explain why postorder is the deletion order.
4. Reconstruct a tree from inorder + preorder, and prove preorder + postorder is insufficient.
5. State the BST invariant as a **subtree** condition and give a tree that satisfies the child-only condition but is not a BST.
6. Implement search, insert, and all three cases of delete, and prove the two-child case never recurses into itself.
7. Explain why every BST operation is $\Theta(h)$, and why that is both the structure's strength and its weakness.
8. Distinguish expected **depth** ($\approx 1.386\log_2 n$) from expected **height** ($\approx 2.99\log_2 n$), and explain why an asymptotic constant can be a poor predictor at practical $n$.

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L04 Trees and Traversals.md` | Terminology, shapes, height bounds, four traversals, reconstruction |
| `lectures/L05 Binary Search Trees.md` | The invariant, search/insert/delete, successor, validation |
| `lectures/L06 BST Height Average and Worst Case.md` | Why sorted input is the worst case; average-case results; what would fix it |
| `assignments/PS 1 Binary Trees and BSTs.md` | 100 points, due Friday of Week 2 |
| `assignments/QUIZ 1 Week 1 Monday.md` | 20 points, formative — **covers Week 0** |
| `lab/LAB 1 Visualising Tree Traversals.md` | Build a renderer, instrument the traversals, measure heights |
| `resources/Reading Guide Week 1.md` | CLRS §12.1–12.3 with guiding questions |
| `solutions_instructor/` | PS 1 and Lab 1 solutions — instructor only |

### The Two Ideas Most Likely to Be Missed

**1. The BST invariant is about subtrees, not children.** Checking only
`left.key < key < right.key` accepts trees that are not BSTs. This is the single most common bug of
the week, it is the subject of PS 1 E3, and it appears again in the midterm.

**2. Sorted input is the worst case.** Not a contrived adversarial sequence — the most natural input
there is. A structure whose failure mode is triggered by *tidy* data fails in production on real
data while passing tests on synthetic data.

### Connections

**Back:** Lecture 03's loop invariants are used directly to prove BST search correct — the proof is
structurally identical to binary search's, which is not a coincidence. MATH 151's induction is
assumed throughout Part E of the problem set.

**Forward:** **Week 2** keeps the BST invariant exactly as it is and adds a second invariant about
*shape*, plus the rotation that repairs it — everything from this week carries over unchanged, so
gaps here will not close by themselves. **Week 3**'s heap is a different tree invariant answering a
different question. **Week 4**'s BFS is the level-order traversal of this week, generalised from
trees to graphs.

---

*CS 102 · Week 1 · © CSE Department*
