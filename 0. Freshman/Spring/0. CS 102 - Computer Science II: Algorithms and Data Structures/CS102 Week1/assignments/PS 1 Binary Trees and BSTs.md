# CS 102 · Problem Set 1
## Binary Trees and Binary Search Trees

**Released:** Friday 29 January 2027, 10:00 (after L06) · Week 1
**Due:** Friday 5 February 2027, 17:00 · Week 2 — late penalty from 17:01 (syllabus late policy)

**Points:** 100 · counts toward the Problem Sets component (35%, lowest one dropped)
**Expected time:** about 4–5 hours

## What this problem set uses

Weeks 0–1 only: loop invariants and induction (L03), tree terminology, the height bounds, the four
traversals and reconstruction (L04), BST search, insert, delete, successor and validation (L05), and
the average-case formulas (L06). Strong induction is also MATH 151.

**Not needed and not expected:** balancing, rotations or AVL trees (Week 2); heaps (Week 3).

> Written proofs must be proofs. A trace of one example is not a proof; see Lecture 03 §4.
> Code must run. Submit `ps1.py` alongside your written work.

---

## Part A — Tree Terminology and Structure (20 pts)

**A1.** *(5)* For a binary tree with $n = 6$ nodes, give the minimum and maximum possible height, and
draw a tree achieving each. **Use the edge-counting convention** (a single node has height 0).

**A2.** *(6)* Prove by induction that a perfect binary tree of height $h$ has exactly $2^{h+1} - 1$
nodes, and that $2^d$ of them are at depth $d$.

**A3.** *(5)* Prove that any binary tree with $n$ nodes has height $h \ge \lceil\log_2(n+1)\rceil - 1$.
*(Hint: use A2 — a tree of height $h$ cannot have more nodes than the perfect tree of height $h$.)*

**A4.** *(4)* A binary tree has 20 leaves and every internal node has exactly 2 children. How many
nodes does it have in total? **Justify** — do not just assert the formula.

---

## Part B — Traversals (20 pts)

**B1.** *(4)* For the tree below, give all four traversals.

```
              10
            /    \
           5      15
          / \       \
         3   7       20
        /     \
       1       9
```

**B2.** *(4)* Implement `preorder`, `inorder`, `postorder` recursively and `level_order` with a
queue. Verify against B1.

**B3.** *(5)* Implement `inorder` **iteratively** with an explicit stack. State its space complexity
and explain when you would prefer it to the recursive version.

**B4.** *(4)* Given preorder `[8, 3, 1, 6, 4, 7, 10, 14, 13]` and inorder
`[1, 3, 4, 6, 7, 8, 10, 13, 14]`, reconstruct the tree. Draw it and give its postorder.

**B5.** *(3)* **Prove** that preorder together with postorder does *not* determine a binary tree, by
exhibiting two distinct trees with identical preorder and identical postorder.

---

## Part C — BST Operations (25 pts)

**C1.** *(4)* Insert `40, 20, 60, 10, 30, 50, 70, 5` into an empty BST. Draw it. Give its height and
its inorder traversal.

**C2.** *(5)* Implement `insert`, `search`, `minimum`, `maximum` iteratively (no recursion). State
the complexity of each in terms of $h$.

**C3.** *(6)* Implement `delete` handling all three cases. Delete `20`, then `60`, then `40` from
your C1 tree, drawing the tree after each. Use the **successor** rule for the two-child case.

**C4.** *(5)* Implement `is_bst(t)` correctly. Then give a **5-node** tree that the naive
parent-child-only check accepts but yours rejects, different from the one in Lecture 05 §1.

**C5.** *(5)* Implement `successor(root, key)` **without parent pointers**. Use L05 §4's two cases:
if the node has a right subtree, take its minimum; otherwise, while searching down from the root for
`key`, remember the last node where you turned **left** — that ancestor is case 2's answer. State its
complexity and explain why it is not $\Theta(1)$ even when the answer is in the same subtree.

---

## Part D — Height and Analysis (20 pts)

**D1.** *(6)* Insert `1..7` in ascending order. What height results? Now find an insertion order of
the same keys giving minimum height. **How many such orders exist?** Justify your count.

**D2.** *(7)* Using $\text{IPL}(n) = 2(n+1)H_n - 4n$, compute the expected average node depth of a
random BST for $n = 31$. Compare with the perfectly balanced 31-node tree. Report the ratio and
comment on how it relates to $2\ln 2$.

**D3.** *(7)* You must support lookup on 10 million records. For each of the following, argue for or
against a plain BST and say what you would use instead where appropriate:
- (a) keys arrive pre-sorted, one at a time, with queries interleaved;
- (b) keys are random 128-bit UUIDs;
- (c) keys arrive pre-sorted but may all be buffered before the structure is built.

---

## Part E — Proof (15 pts)

**E1.** *(8)* Prove that the inorder traversal of a BST yields keys in strictly increasing order.
Use induction on subtree size and state your inductive hypothesis explicitly.

**E2.** *(7)* Prove that Case 3 of BST deletion (two children) never recurses into Case 3.

---

## Grading Summary

| Part | Points | Focus |
|---|---|---|
| A | 20 | Terminology, structural bounds, induction |
| B | 20 | Traversals, reconstruction |
| C | 25 | BST operations, validation |
| D | 20 | Height, average case, engineering judgement |
| E | 15 | Proof |
| **Total** | **100** | |

---

*CS 102 · Week 1 · Problem Set 1 · © CSE Department*
