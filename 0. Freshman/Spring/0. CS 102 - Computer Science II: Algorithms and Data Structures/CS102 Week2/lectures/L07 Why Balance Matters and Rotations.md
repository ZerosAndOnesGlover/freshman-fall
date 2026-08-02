# CS 102 · Computer Science II
## Lecture 07: Why Balance Matters, and the Rotation

---

## 1. Where Week 1 Left Us

Every BST operation costs $\Theta(h)$. Nothing in the BST invariant constrains $h$.

Insert $0, 1, 2, \dots, n-1$ in that order and every key goes to the right of everything before it.
The result is a linked list of height $n-1$. Measured, on the machine these notes were prepared on:

| $n$ | height of BST built from sorted input | height of a perfect tree on $n$ nodes |
| --- | --- | --- |
| $1{,}000$ | $999$ | $9$ |
| $10{,}000$ | $9{,}999$ | $13$ |
| $100{,}000$ | $99{,}999$ | $16$ |

The consequence is not academic. Building the $n = 16{,}000$ tree took **7.24 seconds** against
**0.14 s** for a balanced tree; running 2,000 random successful searches on the $n = 8{,}000$ tree
took **0.195 s** against **0.0011 s** — a factor of **170**.

**The input that triggers this is the most natural input there is.** A database export, a log file, a
list of IDs assigned in order. This is a structure whose failure mode is *tidy data*.

This week fixes it, and the fix is one idea: **add a second invariant, about shape, and find an
$O(1)$ operation that repairs it.**

---

## 2. What Should "Balanced" Mean?

We need a property that (a) forces $h = O(\log n)$ and (b) can be restored cheaply after an update.
Those two requirements pull against each other, and the interesting part is where the compromise
lands.

### Candidate 1 — perfect

*Every level is full.* This forces $h = \lceil\log_2(n+1)\rceil - 1$, the best possible. But it is
only achievable when $n = 2^{k}-1$, so it cannot be an invariant of a structure that accepts
arbitrary insertions.

### Candidate 2 — complete

*Every level full except possibly the last, filled left to right.* Achievable at every $n$, and still
$h = \lfloor\log_2 n\rfloor$. **This is the invariant a heap uses** — Week 3 — and it works there
because a heap never has to put a *particular* key in a *particular* place. A BST does. Restoring
completeness after a BST insertion can require moving $\Theta(n)$ keys.

### Candidate 3 — size-balanced

*At every node, $\big|\,|L| - |R|\,\big| \le 1$*, where $|L|$ and $|R|$ are subtree **sizes**. This
forces $h = O(\log n)$, but it is nearly as rigid as completeness. Count the shapes each candidate
invariant permits on $n$ nodes:

| $n$ | size-balanced shapes | height-balanced (AVL) shapes | all BST shapes |
| --- | --- | --- | --- |
| 7 | **1** | 17 | 429 |
| 10 | 32 | 60 | 16,796 |
| 12 | 32 | 184 | 208,012 |

At $n = 7$ there is **exactly one** legal size-balanced tree. A structure with essentially no freedom
of shape cannot absorb an insertion locally, and the consequence is measurable: inserting a new
minimum key into a size-balanced tree of 255 nodes changes the left-subtree size of **253 of them**.
That is $\Theta(n)$ per insertion — worse than the sorted array we were trying to beat.

### Candidate 4 — height-balanced

*At every node, $\big|\,h(L) - h(R)\,\big| \le 1$*, where $h$ is **height**.

This is the AVL invariant, and it is the one that works. It is weaker than the first three — an
AVL tree can be visibly lopsided — but it is **weak enough to be repairable in $O(1)$** and still
strong enough to force $h = O(\log n)$. Lecture 08 proves both halves.

> **The general lesson, and it recurs all term:** the useful invariant is rarely the strongest one.
> It is the weakest one that still buys the guarantee you need, because weaker invariants are cheaper
> to maintain.

---

## 3. The Rotation

A rotation is a local rearrangement of two nodes and three subtrees. It changes the shape of a tree
and **leaves its inorder sequence unchanged**, which is exactly the same statement as: it preserves
the BST invariant.

### Right rotation

```
      y                            x
     / \                          / \
    x   C     right-rotate(y)    A   y
   / \       ───────────────►       / \
  A   B      ◄───────────────      B   C
                left-rotate(x)
```

Read off the inorder sequence of each side:

- Left: $A$, then $x$, then $B$, then $y$, then $C$.
- Right: $A$, then $x$, then $B$, then $y$, then $C$.

**Identical.** That is the whole proof, and it is worth pausing on: the rotation is correct not
because of a case analysis but because both pictures are two drawings of the same ordered sequence.

```python
def rotate_right(y):
    x = y.left
    y.left = x.right       # B moves from x's right to y's left
    x.right = y
    update_height(y)       # y first — it is now x's child
    update_height(x)
    return x               # the new subtree root

def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    update_height(x)       # x first
    update_height(y)
    return y
```

**The order of the two height updates matters.** $y$ becomes a child of $x$, so $y$'s height must be
recomputed before $x$'s is computed from it. Reversing these two lines produces a tree whose stored
heights are wrong, whose balance factors are therefore wrong, and which then fails to rebalance —
without ever violating the BST invariant, so ordinary tests pass. It is the hardest bug in this
week's problem set to find by inspection.

Each rotation touches a fixed number of pointers, so it is $O(1)$ regardless of subtree sizes. $A$,
$B$, $C$ are never examined — only re-parented.

*(Verified: 2,000 random BSTs, each rotated at the root in both directions, inorder sequence compared
before and after. 0 mismatches.)*

---

## 4. The Four Cases

Let $z$ be the **lowest** node whose balance factor $\mathrm{bf}(z) = h(L) - h(R)$ has left the range
$\{-1, 0, +1\}$ after an insertion. Everything below $z$ is still balanced. There are four shapes,
named for the two steps of the path from $z$ toward the inserted key.

| Case | $\mathrm{bf}(z)$ | $\mathrm{bf}$ of that child | Fix |
| --- | --- | --- | --- |
| **LL** | $+2$ | $\ge 0$ | `rotate_right(z)` |
| **RR** | $-2$ | $\le 0$ | `rotate_left(z)` |
| **LR** | $+2$ | $< 0$ | `rotate_left(z.left)`, then `rotate_right(z)` |
| **RL** | $-2$ | $> 0$ | `rotate_right(z.right)`, then `rotate_left(z)` |

LL and RR are mirror images; so are LR and RL. **There are really only two cases**, and if you learn
LL and LR you can derive the others by exchanging every `left` and `right`.

### Why LR genuinely needs two rotations

This is the step students most often try to shortcut, so here it is concretely. Insert $30, 10, 20$:

```
    30              30
   /               /
  10      →       10        bf(30) = +2,  bf(10) = -1   ← left-right
                    \
                     20
```

Apply a single right rotation at $30$ and see what happens:

```
   10
     \
      30
     /
    20
```

The new root has $\mathrm{bf} = -2$. **We have moved the violation, not repaired it** — the tree is
exactly as unbalanced as before, mirrored.

*(Verified: single `rotate_right` on this tree yields a root with balance factor $-2$.)*

The reason is structural. A single right rotation at $z$ promotes $z$'s left child and hands $z$ that
child's **right** subtree. In the LL case the offending subtree is the child's *left* one, which the
rotation lifts. In the LR case it is the child's *right* one — the one the rotation pushes back down.
The first rotation exists to convert LR into LL, and only then does the second rotation work.

Applying both to $30, 10, 20$ gives root $20$ with children $10$ and $30$ — balanced, and the correct
BST.

---

## 5. What a Rotation Cannot Do

Two limits, both worth stating before you start implementing.

**A rotation changes the height of the subtree it is applied to by at most 1.** *(Verified
exhaustively over all distinct BST shapes on up to 8 nodes: the maximum change is exactly 1.)* It is
a local repair, so it cannot turn a degenerate tree into a balanced one in a single step — an AVL
tree built from the sorted keys $0 \dots 99{,}999$ performs **99,983 rotations** along the way, one
for very nearly every insertion. That is why the invariant is maintained on *every* insertion rather
than repaired in bulk afterwards.

**A rotation cannot fix anything if you do not know where to apply it.** The whole algorithm is: find
the lowest violation, classify it into one of four cases, apply the corresponding rotation. Lecture
08 shows that after an *insertion* this happens at most once. After a *deletion* it can happen at
every level, and the difference between those two facts is the most surprising result of the week.

---

## 6. What to Do

- Read CLRS §13.1–13.2 (rotations) — the red-black chapter, but the rotation code is universal.
- Redraw all four cases from memory tonight, without notes. Most rotation bugs are drawing errors.
- **Lab 2** measures the BST-versus-AVL gap that section 1 quoted, on your own machine.

---

*CS 102 · Week 2 · Lecture 07 · © CSE Department*
