# CS 102 · Computer Science II
## Lecture 09: Red-Black Trees, B-Trees, and What Practice Actually Uses

**Date:** Friday 5 February 2027 · 09:00–09:50 · Week 2

---

## 1. A Second Way to Balance

AVL trees give a strong guarantee — height under $1.4404\log_2(n+2)$ — and pay for it with a
deletion that may rotate at every level.

**Red-black trees make the opposite trade.** They allow a taller tree in exchange for a cheaper
repair. Both are $\Theta(\log n)$; they differ in the constants, and the choice between them is an
engineering decision rather than a mathematical one.

The mechanism is unusual and worth stating plainly before the rules: a red-black tree does not
measure or store heights at all. **It stores one bit per node** — a colour — and four rules about
colours turn out to constrain the height.

---

## 2. The Five Properties

Every node is either **red** or **black**. Treat the empty subtrees as real black nodes — call them
`NIL` — which removes a great many special cases from the code.

1. Every node is red or black.
2. **The root is black.**
3. **Every `NIL` leaf is black.**
4. **A red node's children are both black.** (Equivalently: no two reds in a row on any path.)
5. **For every node, all paths from it down to `NIL` contain the same number of black nodes.**

Properties 4 and 5 are the load-bearing ones. Define the **black-height** $bh(v)$ as the number of
black nodes on any path from $v$ down to a `NIL`, not counting $v$ itself. Property 5 says this is
well defined.

### Why these five force $h = O(\log n)$

Two steps.

**Step 1 — a subtree rooted at $v$ contains at least $2^{bh(v)} - 1$ internal nodes.** By induction
on height. If $v$ is `NIL` then $bh(v) = 0$ and it has $2^0 - 1 = 0$ internal nodes. Otherwise each
child has black-height $bh(v)$ or $bh(v)-1$, so by the inductive hypothesis each contributes at least
$2^{bh(v)-1} - 1$, and $2\big(2^{bh(v)-1} - 1\big) + 1 = 2^{bh(v)} - 1$.

**Step 2 — at least half the nodes on any root-to-leaf path are black.** This is property 4: reds
cannot be adjacent, and property 2 makes the top one black. So $bh(\text{root}) \ge h/2$, where $h$
counts edges.

Combining, $n \ge 2^{h/2} - 1$, hence

$$\boxed{\,h \le 2\log_2(n+1)\,}$$

**A red-black tree is at most twice the height of a perfect tree** — against 1.44× for AVL.

*(Verified: a CLRS-style red-black insert was implemented and stress-tested — 400 random trials
checking all five properties, BST order, and set semantics after every insertion. The bound was never
violated; the worst ratio $h/\log_2(n+1)$ observed was **1.806**, on sorted input at $n = 100{,}000$.)*

The 1.806 is worth noticing. The AVL bound of 1.44 is approached only along a thin family of
Fibonacci-shaped trees; the red-black bound of 2 gets genuinely close on ordinary sorted input.
**The weaker guarantee is weak in practice, not only on paper.**

---

## 3. AVL Against Red-Black, Measured

Two implementations, same machine, same keys.

### Sorted input $0, 1, \dots, n-1$

| $n$ | AVL height | RB height | perfect | AVL rotations | RB rotations |
| --- | --- | --- | --- | --- | --- |
| $1{,}000$ | 9 | 16 | 9 | 990 | 983 |
| $10{,}000$ | 13 | 23 | 13 | 9,986 | 9,976 |
| $100{,}000$ | 16 | 30 | 16 | 99,983 | 99,969 |

### Random input, mean of 5 runs

| $n$ | BST height | AVL height | RB height | AVL rotations | RB rotations |
| --- | --- | --- | --- | --- | --- |
| $1{,}000$ | 20.0 | 11.0 | 11.2 | 698 | 580 |
| $10{,}000$ | 29.8 | 15.0 | 15.6 | 6,987 | 5,783 |
| $100{,}000$ | 39.8 | 19.0 | 19.0 | 69,742 | 58,222 |

Read these carefully, because the second table contradicts something you will hear.

**On sorted input the red-black tree is nearly twice as tall** — 30 against 16 — and it does
**essentially the same number of rotations** (99,969 against 99,983). The usual summary, *"red-black
trees rebalance less,"* **is simply false for this input.**

**On random input the heights are almost identical** — 19.0 versus 19.0 at $n = 10^5$ — and the
red-black tree does about **17% fewer rotations**. That is where the folklore comes from, and 17% is
a much smaller number than the folklore implies.

> **The real advantage is not in this table.** It is in *deletion*, which these measurements do not
> exercise: red-black deletion needs at most **three** rotations in the worst case, where AVL
> deletion needs $\Theta(\log n)$. That is the property a library implementer is buying, and it is
> why you should be suspicious of a benchmark — including this one — that reports only insertions.

*(Verified: CLRS red-black deletion implemented and stress-tested alongside insertion — 400 random
trials, plus full insert-then-delete-everything sweeps at $n = 2{,}000$ and $n = 20{,}000$ on both
sorted and random keys, checking all five properties after every operation. **Maximum rotations
observed: 2 for any insertion, 3 for any deletion**, at every size. Compare AVL deletion, which
reached 9 rotations for a single deletion on a tree of only 10,945 nodes.)*

---

## 4. Why Libraries Choose Red-Black

The constant-bounded rebalancing on both insert and delete, plus one bit of metadata per node instead
of an integer height, is enough to have made red-black the default in most standard libraries.

On the machine these notes were prepared on, `/usr/include/c++/13/bits/stl_tree.h` opens with the
comment `// Red-black tree class, designed for use in implementing STL`, and `stl_map.h` defines
`std::map` in terms of `_Rb_tree`. Java's `TreeMap` and the Linux kernel's `rbtree.h` do the same.

AVL trees remain the better choice when reads dominate writes, because the shorter tree wins every
lookup. **Neither is "better."** They are different points on the same trade-off, and being able to
say which you want, and why, is the thing being examined.

---

## 5. B-Trees: When the Cost Model Changes

Everything so far assumed one cost model — following a pointer is cheap and uniform. On disk that is
false by five orders of magnitude, and the right data structure changes completely.

A B-tree of order $b$ has up to $b-1$ keys and $b$ children per node, all leaves at the same depth.
The height is $\Theta(\log_b n)$, and $b$ is chosen so that **one node is exactly one disk page.**

The arithmetic, for a 4 KiB page with 8-byte keys and 8-byte child pointers:

$$\left\lfloor \frac{4096 - 8}{8 + 8} \right\rfloor = 255 \text{ keys, so } 256 \text{ children per node.}$$

| keys $n$ | levels, $b = 256$ | levels, AVL |
| --- | --- | --- |
| $10^6$ | **3** | 27 |
| $10^9$ | **4** | 41 |
| $10^{12}$ | **5** | 56 |

**Four disk reads to find one key among a billion.** An AVL tree with the same keys on disk would
need 41, and at roughly 0.1 ms per random read on a spinning disk that is the difference between
0.4 ms and 4 ms — a factor of ten, from nothing but choosing the node size to match the hardware.

With 16-byte keys the fan-out drops to 171 and $10^9$ keys need 5 levels rather than 4. **The
structure is tuned to the page, not to the key count**, which is why database index pages are sized
the way they are.

This is the first time this course has changed the cost model, and it will not be the last. **An
algorithm is only optimal with respect to a model**, and one of the most common real-world mistakes
is optimising against a model that does not describe the machine.

---

## 6. What Python Actually Gives You

Python has no balanced BST in its standard library, which surprises people arriving from C++ or Java.
`dict` and `set` are hash tables — expected $O(1)$, but **unordered**, so they cannot answer "what is
the smallest key above $x$?"

The usual answer is `sortedcontainers`, whose `SortedList` supports ordered insertion, ordered
iteration, `bisect_left`, and indexing by rank.

**It is not a tree.** Inspecting version 2.4.0 directly:

```
>>> s = SortedList(range(100000))
>>> type(s._lists), type(s._lists[0]), len(s._lists), s._load
(<class 'list'>, <class 'list'>, 100, 1000)
```

It is a **list of lists** — sublists of about 1,000 elements each (the `_load` parameter), so
$n/1000$ of them, with a separate index over the sublist *lengths* to make rank queries logarithmic.
Insertion does a binary search to find the sublist and then a memory move within it, which is
asymptotically worse than $O(\log n)$.

That index is itself worth a look. Its docstring describes it as *"binary trees in a dense array
notation similar to a binary heap"* — each row is the pairwise sums of the row below, concatenated
into one flat list. **You are three days from building exactly that structure**, from the other
direction, in Week 3.

And yet:

| operation, $n = 100{,}000$ sorted insertions | time |
| --- | --- |
| `SortedList.add` | **0.068 s** |
| hand-written AVL insert (pure Python) | 1.089 s |

**Sixteen times faster, with the worse asymptotic complexity.** The reason is that its inner loop is
a `list` slice assignment — a `memmove` in C over contiguous memory — while the AVL tree executes
Python-level function calls and chases pointers into scattered objects. Moving 1,000 contiguous
machine words costs less than 17 interpreted comparisons.

Three conclusions, and the third is the one to keep:

1. **Asymptotics do not settle which implementation is faster at a given $n$.** They settle which one
   wins *eventually*, and eventually may be past every size you care about.
2. **The constant factor here is a property of the language, not the algorithm.** In C the comparison
   would come out differently.
3. **You still need to understand the tree.** You cannot evaluate whether `SortedList` is the right
   tool — or read its index structure, or predict where its performance falls apart — without the
   material of this week. *Knowing the structure is what lets you decline to implement it.*

---

## 7. Where This Leaves Week 2

You now have the guarantee Week 1 was missing: **$\Theta(\log n)$ worst case for search, insert, and
delete**, with no assumption whatsoever about input order.

Two invariants, maintained together, over the same nodes — order and shape. **Week 3 keeps the shape
invariant and throws the order invariant away.** A heap is a complete binary tree with only a
parent-child ordering, and the surprise is how much you can still do with that much less structure —
including making it an array with no pointers at all.

---

## 8. What to Do

- Read CLRS §13.3–13.4 (red-black insertion and deletion) and §18.1 (B-tree definition).
- **PS 2** is due Friday. **Lab 2** reproduces section 3's sorted-input comparison on your machine.
- You are **not** examined on red-black insertion code. You are examined on the five properties, the
  $2\log_2(n+1)$ argument, and the AVL/red-black trade-off.

---

*CS 102 · Week 2 · Lecture 09 · © CSE Department*
