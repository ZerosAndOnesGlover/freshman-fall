# CS 102 — Problem Set 1 Solutions
## INSTRUCTOR ONLY

**Total: 100 points.** All computed answers verified by execution.
**Convention throughout: height counts EDGES.** Single node = height 0, empty tree = height $-1$.

---

## Part A — Terminology and Structure (20 pts)

**A1.** *(4)* $n=6$: **minimum height 2**, **maximum height 5**.

Max: a chain, $h = n-1 = 5$. Min: $h \ge \lceil\log_2 7\rceil - 1 = 3 - 1 = 2$, achieved by a
6-node tree filling levels 0,1 and two nodes at level 2.

*Marking: 2 for values, 2 for trees achieving them.*

**A2.** *(5)* Induction on $h$. **Base** $h=0$: one node $= 2^1-1$ ✓, and $2^0=1$ at depth 0 ✓.
**Step:** a perfect tree of height $h+1$ is a root plus two perfect subtrees of height $h$, giving
$1 + 2(2^{h+1}-1) = 2^{h+2}-1$ ✓. Depth $d+1$ of the whole is depth $d$ of each subtree:
$2\cdot 2^d = 2^{d+1}$ ✓. ∎

**A3.** *(4)* A tree of height $h$ has at most $2^{h+1}-1$ nodes (A2 — the perfect tree maximises).
So $n \le 2^{h+1}-1 \Rightarrow 2^{h+1} \ge n+1 \Rightarrow h \ge \log_2(n+1) - 1$, and since $h$ is
an integer, $h \ge \lceil\log_2(n+1)\rceil - 1$. ∎

**A4.** *(4)* Full = every node has 0 or 2 children. Complete = all levels full except possibly the
last, filled left-to-right. Perfect = full **and** all leaves at the same depth.
**Perfect ⟹ full and complete.** Full ⇏ complete (a full tree can be lopsided). Complete ⇏ full
(a complete tree may have one node with a single left child).

**A5.** *(3)* **39 nodes.** In a full binary tree, internal $=$ leaves $- 1$, so $19$ internal
$+ 20$ leaves $= 39$. *Justification required:* each internal node contributes 2 children; total
non-root nodes $= 2i$; also total $= i + \ell$; so $i + \ell = 2i + 1$, giving $i = \ell - 1$.
**Deduct 1 for asserting $2\ell-1$ without derivation.**

---

## Part B — Traversals (20 pts)

**B1.** *(4)* Verified by execution:

| Traversal | Output |
|---|---|
| Preorder | 10, 5, 3, 1, 7, 9, 15, 20 |
| Inorder | 1, 3, 5, 7, 9, 10, 15, 20 |
| Postorder | 1, 3, 9, 7, 5, 20, 15, 10 |
| Level-order | 10, 5, 15, 3, 7, 20, 1, 9 |

Height 3. Inorder is sorted — the tree is a valid BST.

**B3.** *(5)* Iterative inorder:

```python
def inorder_iter(t):
    out, stack, cur = [], [], t
    while stack or cur:
        while cur:
            stack.append(cur); cur = cur.left
        cur = stack.pop()
        out.append(cur.key)
        cur = cur.right
    return out
```
Space $\Theta(h)$ — same as recursion, but **on the heap rather than the call stack**. Preferred when
$h$ may approach $n$ (Python's default recursion limit of 1000 makes the recursive version crash on a
degenerate tree of 1000 nodes) or when you need to pause/resume the traversal.

**B4.** *(4)* Reconstructed tree — root 8, verified to round-trip both given traversals:

```
            8
          /   \
         3     10
        / \      \
       1   6      14
          / \     /
         4   7   13
```
**Postorder: 1, 4, 7, 6, 3, 13, 14, 10, 8.** *(Verified.)* Height 3. Inorder is sorted, so it is a BST.

**B5.** *(3)* Two distinct trees, both preorder `[5, 3]`, both postorder `[3, 5]`:

```
    5           5
   /             \
  3               3
```
Preorder cannot distinguish them because with one child the (node, left, right) and (node, right,
left) outputs coincide; postorder likewise. **Award full marks for any correct pair.**

---

## Part C — BST Operations (25 pts)

**C1.** *(4)* Inserting `40, 20, 60, 10, 30, 50, 70, 5`:
inorder **5, 10, 20, 30, 40, 50, 60, 70** (sorted ✓), **height 3**. *(Verified.)*

**C3.** *(6)* Delete 20 (two children → successor 30 replaces it); delete 60 (two children →
successor 70); delete 40 (root, two children → successor 50). Final inorder:
**5, 10, 30, 50, 70** — sorted, invariant intact. *Marking: 2 per deletion, requiring a drawing.*

**C4.** *(5)* Correct validator passes bounds down (Lecture 05 §7). Any 5-node counterexample where a
violation is invisible locally, e.g. root 10, left child 5, and 5's right child 12: locally
$5 < 10$ ✓ and $5 < 12$ ✓, but 12 sits in 10's left subtree. **Must differ from the lecture's.**

**C5.** *(5)* Successor without parent pointers: descend from the root, recording the last node
where you went **left**; that node is the successor if the target has no right subtree.
$\Theta(h)$. It is not $\Theta(1)$ even for a same-subtree answer because you must locate the node
first, which itself costs $\Theta(h)$.

---

## Part D — Height and Analysis (20 pts)

**D1.** *(4)* Ascending `1..7` gives **height 6**. Minimum height is 2, and **80 of the $7! = 5040$
insertion orders achieve it** *(verified by exhaustive enumeration)*.

Reasoning for the count: 4 must be inserted first; then each subtree $\{1,2,3\}$ and $\{5,6,7\}$ must
independently be built to height 1 (2 valid orders each: root-first, then either child order — giving
$2\times2$... ) and the two subtrees' insertions may be interleaved arbitrarily:
$\binom{6}{3} = 20$ interleavings $\times\, 2 \times 2 = 80$ ✓.

**Accept the enumeration** as justification; the combinatorial argument earns full marks either way.

**D2.** *(5)* $n=31$: $H_{31} \approx 4.0272$, $\text{IPL} = 2(32)H_{31} - 124 \approx 133.74$, so
expected average depth $\approx \mathbf{4.314}$.

Perfect 31-node tree ($h=4$): average depth $= \frac{0\cdot1 + 1\cdot2 + 2\cdot4 + 3\cdot8 + 4\cdot16}{31} = \frac{98}{31} \approx \mathbf{3.161}$.

**Ratio $\approx 1.365$**, approaching $2\ln 2 \approx 1.386$ from below. *(All verified.)*

**D3.** *(5)* (a) **Against** — degenerate, $\Theta(n)$; online so cannot shuffle; use a balanced BST
(Week 2) or a B-tree. (b) **For** — UUIDs are effectively random, expected height $\approx 2\log_2 n
\approx 46$; a plain BST is fine, though a hash table beats it if range queries are not needed.
(c) **For, with a caveat** — buffer, then build directly from the sorted array by recursive midpoint
selection, giving a perfectly balanced tree in $\Theta(n)$. **Do not insert them one at a time.**

*Marking: award the (c) mark only if they say build-from-sorted rather than shuffle-then-insert.*

**D4.** *(6)* Both correct because $4.311\ln n$ is asymptotic; at $n=1000$ the omitted terms
($-1.953\ln\ln n$ and a negative constant) are a large share of the value. **General lesson:
asymptotic results characterise growth, not magnitude at a given $n$ — validate against measurement
before using one as a numerical prediction.**

---

## Part E — Proof (15 pts)

**E1.** *(5)* Induction on subtree size. **IH:** inorder of any BST of size $< k$ emits its keys in
strictly increasing order. Empty tree: vacuous. For a node $x$ with subtrees $L$, $R$ (each size
$< k$): by IH, inorder($L$) is increasing and all its keys $< x.key$; inorder($R$) is increasing and
all $> x.key$. Concatenation (L, x, R) is therefore strictly increasing. ∎
*Marking: 2 for stating the IH, 2 for using the subtree — not child — property, 1 for strictness.*

**E2.** *(5)* Case 3 replaces $x$'s key with $s = \min(x.\text{right})$ and deletes $s$ from the right
subtree. By definition of minimum, $s$ has **no left child**. A node with no left child falls into
Case 1 (leaf) or Case 2 (right child only). Therefore the recursive call cannot be Case 3, and the
recursion depth from Case 3 is exactly one. ∎

**E3.** *(5)* **False.** Counterexample: the Lecture 05 §1 tree (root 5, left 3, 3's children 2 and
7). Every parent-child triple satisfies the local condition, but $7 > 5$ sits in 5's left subtree, so
inorder gives $2,3,7,5,\ldots$ — not sorted. The condition must hold for **whole subtrees**. ∎
*Students who answer "true" score 0; this is the central misconception of the week.*

---

## Grading Summary

| Part | Points |
|---|---|
| A | 20 |
| B | 20 |
| C | 25 |
| D | 20 |
| E | 15 |
| **Total** | **100** |

---

*CS 102 · Week 1 · PS 1 Solutions · © CSE Department*
