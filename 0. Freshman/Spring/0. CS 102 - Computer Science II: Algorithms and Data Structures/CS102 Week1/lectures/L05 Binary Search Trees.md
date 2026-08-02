# CS 102 · Computer Science II
## Lecture 05: Binary Search Trees

---

## 1. The BST Invariant

A **binary search tree** is a binary tree satisfying, at every node $x$:

> **BST invariant.** Every key in the left subtree of $x$ is **less than** $x.\text{key}$, and every
> key in the right subtree is **greater than** $x.\text{key}$.

Two details students get wrong, both of which produce code that works on small examples and fails on
larger ones.

**It is a whole-subtree condition, not a parent–child condition.** Checking only that
`left.key < x.key < right.key` is not enough. This tree passes that weaker check at every node and is
**not** a BST:

```
        5
       / \
      3   8
     / \
    2   7          <-- 7 > 5, but it is in 5's LEFT subtree
```

The local test at node 3 sees $2 < 3 < 7$ and is satisfied. The violation is only visible from node 5.

**Duplicates are excluded by this statement.** Real implementations either forbid them, or store a
count per node, or adopt a consistent tie-breaking rule. We forbid them, which keeps the invariant
and the proofs clean.

---

## 2. Why the Invariant Buys Search

**The inorder traversal of a BST yields its keys in sorted order.** That single fact is the reason
BSTs exist, and it follows directly from the invariant by induction on the subtree.

*Proof sketch.* For an empty tree the claim is vacuous. For a node $x$, inorder emits (left subtree,
then $x$, then right subtree). By the inductive hypothesis the left output is the sorted left keys —
all less than $x.\text{key}$ — and the right output is the sorted right keys, all greater. Their
concatenation is therefore sorted. ∎

Search follows the same logic **without** producing the whole order:

```python
def search(t, key):
    while t is not None:
        if   key == t.key: return t
        elif key <  t.key: t = t.left
        else:              t = t.right
    return None
```

> **Loop invariant.** At the top of each iteration, if `key` is in the original tree, it is in the
> subtree rooted at `t`.

**Initialisation:** `t` is the root; the whole tree. **Maintenance:** if `key < t.key`, the invariant
guarantees every key in `t`'s right subtree exceeds `t.key`, hence exceeds `key`, so `key` cannot be
there — descending left is safe. Symmetrically for the other branch. **Termination:** each step
descends one level, so the loop ends within $h+1$ iterations; it exits either at a match or at
`None`, which by the invariant means the key was absent. ∎

**This is binary search, with pointers instead of index arithmetic** — and the identical structure of
the two proofs is not a coincidence.

---

## 3. Insertion

Search for the key; when you fall off the tree, that empty slot is exactly where the key belongs.

```python
def insert(t, key):
    if t is None:
        return Node(key)
    if   key < t.key: t.left  = insert(t.left, key)
    elif key > t.key: t.right = insert(t.right, key)
    # key == t.key: already present, no duplicates
    return t
```

**Insertion never restructures the tree.** A new key always becomes a leaf. That is what makes
insertion $\Theta(h)$ — and also what allows the tree to degenerate, since the shape is entirely
determined by insertion order.

---

## 4. Minimum, Maximum, Predecessor, Successor

**Minimum** is the leftmost node; **maximum** the rightmost.

```python
def minimum(t):
    while t.left is not None:
        t = t.left
    return t
```

**Successor** of $x$ — the next key in sorted order — has two cases, and the second is the one people
forget:

1. **If $x$ has a right subtree**, the successor is the minimum of that subtree.
2. **Otherwise**, walk up until you come from a *left* child; that ancestor is the successor. If no
   such ancestor exists, $x$ is the maximum and has no successor.

```python
def successor(x):                      # requires parent pointers
    if x.right is not None:
        return minimum(x.right)
    p = x.parent
    while p is not None and x is p.right:
        x, p = p, p.parent
    return p
```

Case 2 is best understood through the inorder traversal: you finish a subtree and return to the
ancestor whose visit was deferred while that subtree was processed.

Both run in $\Theta(h)$.

---

## 5. Deletion

Deletion is the only genuinely awkward BST operation, because removing an internal node leaves a hole
that must be filled without breaking the invariant. **Three cases.**

**Case 1 — the node is a leaf.** Remove it.

**Case 2 — the node has one child.** Splice the child into its place. The invariant survives because
the subtree keeps its entire key range.

**Case 3 — the node has two children.** You cannot simply remove it; both subtrees need a parent.
**Replace its key with its inorder successor's key, then delete the successor from the right
subtree.**

The successor is the minimum of the right subtree, so it has **no left child** — meaning its own
deletion is Case 1 or Case 2, and the recursion terminates immediately. It never recurses into
Case 3 again.

```python
def delete(t, key):
    if t is None:
        return None
    if   key < t.key: t.left  = delete(t.left, key)
    elif key > t.key: t.right = delete(t.right, key)
    else:
        if t.left  is None: return t.right      # cases 1 and 2
        if t.right is None: return t.left       # cases 1 and 2
        s = minimum(t.right)                    # case 3
        t.key = s.key
        t.right = delete(t.right, s.key)
    return t
```

**Why the successor works:** it is the smallest key greater than everything in the left subtree and
smaller than everything else in the right subtree — precisely the key range the hole requires. The
predecessor (maximum of the left subtree) works equally well and by the same argument.

> **A known asymmetry.** Always choosing the successor biases the tree over many deletions, tending
> to make left subtrees deeper. Alternating between successor and predecessor mitigates it. This is
> a real effect, though it is not why BSTs degenerate — that is Lecture 06's subject.

---

## 6. Complexity — All of It Is $\Theta(h)$

| Operation | Time |
| --- | --- |
| `search`, `insert`, `delete` | $\Theta(h)$ |
| `minimum`, `maximum` | $\Theta(h)$ |
| `predecessor`, `successor` | $\Theta(h)$ |
| `inorder` (all keys sorted) | $\Theta(n)$ |

**Every interesting operation is $\Theta(h)$, and nothing so far controls $h$.** From Lecture 04,
$h$ ranges from $\lceil\log_2(n+1)\rceil - 1$ to $n - 1$.

That is the entire tension of this week, and it is not hypothetical:

**Inserting sorted data produces a degenerate tree.** Insert `1, 2, 3, 4, 5` into an empty BST and
every key goes to the right of the last — a linked list of height 4, with $\Theta(n)$ search.

**And sorted input is not a rare adversarial case.** It is what you get from a database export, a log
file, a sorted CSV, or any upstream process that happened to order its output. **The most natural
input is the worst one**, which is a genuinely bad property for a data structure to have and is why
Week 2 exists.

---

## 7. Validating a BST

A recurring exercise, and the naive answer is wrong.

**Wrong** — only checks parent against children:

```python
def is_bst_wrong(t):
    if t is None: return True
    if t.left  and t.left.key  >= t.key: return False
    if t.right and t.right.key <= t.key: return False
    return is_bst_wrong(t.left) and is_bst_wrong(t.right)
```

This returns `True` for the counterexample in §1.

**Right** — pass down the permitted range:

```python
def is_bst(t, lo=None, hi=None):
    if t is None: return True
    if lo is not None and t.key <= lo: return False
    if hi is not None and t.key >= hi: return False
    return is_bst(t.left, lo, t.key) and is_bst(t.right, t.key, hi)
```

Each node inherits a bound from every ancestor, which is exactly what makes it a whole-subtree
condition. **An equally valid alternative:** produce the inorder traversal and check it is strictly
increasing — $\Theta(n)$ either way, and arguably clearer.

---

## 8. Exercises

**1.** Insert `50, 30, 70, 20, 40, 60, 80` into an empty BST. Draw it. Give all four traversals.
Which is sorted?

**2.** Insert the same seven keys in **ascending** order. What is the height now? What is the cost of
searching for `80`?

**3.** Delete `50` from your tree in exercise 1, using the successor rule. Draw the result and verify
the invariant holds.

**4.** Prove that Case 3 of deletion never recurses into Case 3.

**5.** Give a 5-node tree that `is_bst_wrong` accepts but `is_bst` rejects, different from §1's.

**6.** How many distinct BSTs contain the keys $\{1,2,3\}$? Generalise to $n$ keys — the answer is
the $n$-th **Catalan number**, $C_n = \frac{1}{n+1}\binom{2n}{n}$. Verify for $n=3$.

---

*CS 102 · Week 1 · Lecture 05 · © CSE Department*
