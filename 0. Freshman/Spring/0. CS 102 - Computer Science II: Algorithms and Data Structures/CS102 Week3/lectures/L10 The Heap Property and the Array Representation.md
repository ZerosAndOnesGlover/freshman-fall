# CS 102 · Computer Science II
## Lecture 10: The Heap Property and the Array Representation

---

## 1. Throwing an Invariant Away

Week 2 ended with two invariants maintained together over the same nodes — **order** (the BST
property) and **shape** (height balance) — and the cost of keeping both was rotations, cached
heights, and four cases to get right.

This week asks what happens if you keep the shape invariant and **throw most of the order invariant
away**.

The answer is surprising twice over. You lose search, which is what a BST was for. But you gain a
structure that needs **no pointers at all**, builds in $O(n)$ rather than $O(n\log n)$, sorts in
place, and turns out to be the right tool for a problem BSTs handle badly: *repeatedly extract the
smallest thing.*

---

## 2. The Heap Property

A **min-heap** is a binary tree in which, for every node $v$ other than the root,

$$\mathrm{key}(\mathrm{parent}(v)) \le \mathrm{key}(v)$$

A **max-heap** reverses the inequality. Everything in this course is stated for min-heaps, because
that is what a priority queue wants and what Python gives you; a max-heap is the same code with the
comparison flipped.

Compare this to the BST invariant and notice how much weaker it is.

| | BST | heap |
| --- | --- | --- |
| relates | a node to **every** descendant | a node to its **two children** |
| between siblings | left subtree $<$ node $<$ right subtree | **nothing** |
| gives you | the whole sorted order | the minimum, and only the minimum |

**A heap says nothing about siblings.** That single omission is the whole difference. It means the
minimum is at the root — that much is forced — and it means essentially nothing else is determined.

### The heap is not sorted

This is the misconception to kill immediately. The heap property does not sort the array.

```
[1, 2, 3]   is a valid min-heap.
[1, 3, 2]   is also a valid min-heap.
```

*(Verified: both satisfy `a[(i-1)//2] <= a[i]` for all $i \ge 1$.)*

Same three keys, two different arrays, both legal. If a heap sorted its contents there would be one.
The heap gives you the **minimum in $O(1)$** and refuses to commit to anything else.

### How much freedom is that?

Count the arrangements of $n$ distinct keys that form a valid min-heap:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| valid min-heaps | 1 | 1 | 2 | 3 | 8 | 20 | 80 | 210 |
| $n!$ | 1 | 2 | 6 | 24 | 120 | 720 | 5,040 | 40,320 |

*(Verified by exhaustive enumeration of all $n!$ permutations for $n \le 8$, cross-checked against
the recurrence $H(n) = \binom{n-1}{L}\,H(L)\,H(R)$ where $L$ and $R$ are the subtree sizes.)*

At $n = 8$ there are 210 legal heaps and exactly **one** sorted array. Recall the same count from
Lecture 07: at $n=7$ there were 429 BSTs but only 17 AVL-legal shapes. The pattern is consistent —
**a weaker invariant admits more configurations, and admitting more configurations is what makes it
cheap to restore.**

---

## 3. The Second Invariant: Completeness

The heap property alone does not bound the height — a single left-leaning path satisfies it. So a
binary heap adds a shape requirement:

> **A binary heap is a *complete* binary tree**: every level is full except possibly the last, which
> is filled left to right.

This is **Candidate 2 from Lecture 07** — the invariant rejected for BSTs because restoring it after
an insertion could require moving $\Theta(n)$ keys. It works here for exactly the reason it failed
there:

> **A BST must put a particular key in a particular place. A heap does not.**

There is only one legal slot for key 42 in a BST. In a heap, 42 may go anywhere its parent is smaller
— and 210 arrangements at $n=8$ means there is nearly always somewhere to put it. **The freedom we
counted in section 2 is what pays for the rigidity of completeness.** The two invariants are affordable
together only because one is very loose exactly where the other is very tight.

Completeness forces the height immediately. A complete tree on $n$ nodes has height

$$h = \lfloor \log_2 n \rfloor$$

*(Verified for $n = 1 \dots 17$: heights $0,1,1,2,2,2,2,3,3,3,3,3,3,3,3,4,4$.)*

Height counts **edges**, and the empty tree has height $-1$ — the Week 1 convention, unchanged.

This is not "$O(\log n)$ if you are lucky," as with an unbalanced BST, nor "$1.44\log_2 n$ worst
case," as with AVL. **It is exactly the minimum possible height, always, with no rebalancing
machinery whatsoever.** Completeness is free because it is a property of the *shape*, and we will
now choose a representation in which the shape cannot be violated.

---

## 4. The Array Representation

Here is the idea the whole week rests on.

**A complete binary tree has no shape freedom.** Given $n$, there is exactly one complete binary tree.
So the tree carries no information — only the *contents* of the positions do. That means we can
number the positions in level order and store the contents in an array. **The pointers were encoding
a shape we already knew.**

```
            1               index:  0   1   2   3   4   5   6
          /   \             array: [1,  3,  2,  7,  4,  9,  8]
         3     2
        / \   / \           level-order reading of the tree
       7   4 9   8            IS the array, by construction
```

Reading the tree level by level, left to right, gives the array. Reading the array left to right
gives the tree. They are the same object.

### The index arithmetic

For a node at index $i$, counting from **0**:

$$\mathrm{left}(i) = 2i+1, \qquad \mathrm{right}(i) = 2i+2, \qquad \mathrm{parent}(i) = \left\lfloor \frac{i-1}{2} \right\rfloor$$

Counting from **1**, as CLRS does, the same relationships read more cleanly:

$$\mathrm{left}(i) = 2i, \qquad \mathrm{right}(i) = 2i+1, \qquad \mathrm{parent}(i) = \left\lfloor \frac{i}{2} \right\rfloor$$

*(Verified: the two conventions describe the identical tree under the map $i \mapsto i-1$, checked for
all $i < 200$. The round trip $\mathrm{parent}(\mathrm{left}(i)) = \mathrm{parent}(\mathrm{right}(i)) = i$
holds for all $i < 10{,}000$ in the 0-indexed form.)*

> ### The bug this causes, every year
>
> CLRS, most lecture notes, and the description in your course handbook use **1-indexing**. Python
> lists are **0-indexed**. Students transcribe $\lfloor i/2 \rfloor$ into 0-indexed code and get a
> parent function that is wrong.
>
> Here is why it survives testing. Compare `i // 2` against the correct `(i - 1) // 2`:
>
> | $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
> | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
> | `(i-1)//2` (correct) | 0 | 0 | 1 | 1 | 2 | 2 | 3 | 3 | 4 |
> | `i//2` (wrong) | 0 | 1 | 1 | 2 | 2 | 3 | 3 | 4 | 4 |
> | agree? | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ | ✓ |
>
> **It is correct for every odd $i$ and wrong for every even $i$.** *(Verified over $i = 1 \dots 39$:
> 20 agreements, all odd; 19 disagreements, all even.)*
>
> In the 0-indexed layout, **odd indices are left children and even indices are right children**
> (since $2i+1$ is always odd and $2i+2$ always even). So the broken formula handles every left child
> correctly and every right child incorrectly.
>
> Now consider how well it hides. Building a heap by repeated insertion with the wrong parent:
>
> | input | $n=10$ | $n=100$ | $n=1{,}000$ |
> | --- | --- | --- | --- |
> | increasing $0,1,2,\dots$ | **passes** | **passes** | **passes** |
> | decreasing $n,\dots,2,1$ | **passes** | fails | fails |
> | random | fails **4.3%** of the time | fails **98.5%** | fails **100%** |
>
> *(Verified: 50,000 random trials per size at $n \le 100$ and 5,000 at $n = 1000$; the sorted
> cases are deterministic.)*
>
> **Increasing input never catches it.** An increasing sequence is inserted at the end and never
> moves, so the parent function is never consulted for a comparison that matters. That is the first
> test most people write.
>
> The smallest input that exposes the bug at all needs **seven** elements — for example inserting
> $0, 1, 4, 2, 5, 6, 3$, which yields `[0, 1, 4, 2, 5, 6, 3]` where index 6 holds 3 under a parent of
> 4. *(Verified by exhaustive search over all permutations of $n \le 7$: 432 of the 5,040 orderings at
> $n = 7$ fail, and **none** of the orderings at $n \le 6$ do.)*
>
> **PS 3 A2 makes you find that witness yourself**, because the transferable skill is not knowing this
> particular formula — it is knowing that a test which passes tells you nothing until you know what
> inputs could have failed.

### Two more formulas worth having

The **depth** of index $i$ is $\lfloor \log_2 (i+1) \rfloor$ — in Python, `(i+1).bit_length() - 1`.
*(Verified for $i = 0 \dots 14$: depths $0,1,1,2,2,2,2,3,3,3,3,3,3,3,3$.)*

The **leaves** are exactly the indices $\lfloor n/2 \rfloor, \dots, n-1$. There are $\lceil n/2 \rceil$
of them — **half the heap is leaves**, a fact that drives the whole of Lecture 11.

### Why this representation is not merely tidy

Three consequences, and the third is the one that matters in practice.

1. **No pointers.** An `n`-element heap of 8-byte keys occupies $8n$ bytes. A pointer-based binary
   tree needs at least a key plus two pointers per node — $24n$ bytes, and in CPython far more, since
   every node is a separate heap-allocated object with its own header.

2. **The shape invariant cannot be violated.** There is no code that maintains completeness, because
   there is no way to express an incomplete tree in a contiguous array. Appending to the end *is*
   adding a node in the unique legal position. **An invariant you cannot express is an invariant you
   cannot break** — compare the four rotation cases of Week 2, every one of which was a chance to get
   it wrong.

3. **Contiguity.** The array is a single block of memory. Walking a level is a linear scan. Week 2's
   final measurement — `SortedList` beating a hand-written AVL tree by 16× *with worse asymptotic
   complexity* — was the same phenomenon: contiguous memory and no pointer chasing. Here we get it
   without giving up the asymptotics.

Point 3 has a limit, and honesty requires stating it now: `sift_down` walks from index $i$ to $2i+1$
to $4i+3$, so its stride **doubles at every step**. For a heap much larger than the cache, the deep
levels are effectively random access. Lab 3 measures this, and it is why heap sort loses to merge
sort in wall-clock time despite better space behaviour.

---

## 5. The Two Repair Operations

Everything a heap does is built from two procedures. Both restore the heap property after a *single*
violation, by moving one element along one root-to-leaf path.

### Sift-up — for an element that is too small for its position

Used after appending a new element at the end.

```python
def sift_up(a, i):
    while i > 0:
        p = (i - 1) // 2
        if a[i] < a[p]:
            a[i], a[p] = a[p], a[i]
            i = p
        else:
            break                      # parent is smaller: done, and so is everything above
```

The `break` is doing real work. Once `a[i] >= a[p]`, every ancestor is already $\le a[p] \le a[i]$ by
transitivity, so the rest of the path is correct and the loop can stop.

Drop the `break` — walk to the root every time, swapping only when needed — and the code is **still
correct**. It just never stops early. This is the most expensive kind of bug: it has no symptom.

| $n$, random input | comparisons with `break` | without | ratio | $\log_2 n$ |
| --- | --- | --- | --- | --- |
| $1{,}000$ | 2,246 | 7,987 | 3.56 | 9.97 |
| $10{,}000$ | 22,805 | 113,631 | 4.98 | 13.29 |
| $100{,}000$ | 227,856 | 1,468,946 | 6.45 | 16.61 |

*(Verified: 2,000 random trials confirm the variant without `break` always produces a valid heap
containing the right multiset. Counts are means of 3 runs.)*

The ratio grows with $\log n$, which is the signature of an $O(1)$-per-insert operation that has been
made $\Theta(\log n)$. With the early exit, a random insertion rises about 2.3 levels on average
regardless of $n$; without it, every insertion walks its full depth.

Those "without" figures are exactly the **sum of all node depths** — a quantity that returns in
Lecture 11 as the thing the linear-time build avoids paying.

### Sift-down — for an element that is too large for its position

Used after replacing the root. This one has the subtlety.

```python
def sift_down(a, i, n):
    while True:
        l, r, m = 2*i + 1, 2*i + 2, i
        if l < n and a[l] < a[m]: m = l
        if r < n and a[r] < a[m]: m = r
        if m == i:
            return                     # already smaller than both children
        a[i], a[m] = a[m], a[i]
        i = m
```

**You must swap with the *smaller* of the two children.** Swapping with either child that is smaller
than the parent restores that child's relationship and breaks the other one. If `a = [5, 3, 4]` and
you swap 5 with 4, you get `[4, 3, 5]` — and $4 > 3$, so the root is still wrong.

That is the single most common bug in this week's problem set, and it is worth seeing why the fix is
not arbitrary: the new parent must dominate *both* children, so it has to be the minimum of the three.

Both operations touch one node per level, so both are $O(\log n)$ — and the height is
$\lfloor\log_2 n\rfloor$ unconditionally, so that is a worst case, not an average.

### Insert and extract-min

```python
def push(a, x):
    a.append(x)                        # unique legal position for a new node
    sift_up(a, len(a) - 1)

def pop_min(a):
    top = a[0]
    last = a.pop()                     # remove the last leaf
    if a:
        a[0] = last                    # move it to the root...
        sift_down(a, 0, len(a))        # ...and let it fall
    return top
```

`pop_min` looks like a trick and is not. The root must be removed, so something must take its place,
and **the only node whose removal preserves completeness is the last one.** The shape constraint
leaves no choice; the code then repairs the order.

*(Verified: 400 random trials of interleaved `push`, checking the heap property after every single
operation, then draining the heap and comparing against `sorted()`. 0 failures. Same for the $O(n)$
build of Lecture 11: 400 trials, 0 failures.)*

---

## 6. What You Gave Up

Be clear about the cost, because the heap is often reached for when a BST is wanted.

**Search is $O(n)$.** There is no way to find an arbitrary key faster. The heap property lets you
prune a subtree whose root already exceeds your target, but that is all.

*(Verified: locating the maximum of a min-heap by depth-first search with pruning visits, on average
over 20 seeds, **48%** of the heap at $n = 1{,}000$, **59%** at $n = 10^4$, and **57%** at $n = 10^5$.
Searching for a key that is absent visits **100%** of the nodes, at every size.)*

And this is not a weakness of that particular algorithm. **The maximum of a min-heap can be at any
leaf**, and the leaves are $\lceil n/2 \rceil$ of the nodes. Any correct algorithm must be able to
tell those $n/2$ cases apart, so it must inspect all of them. The $\Omega(n)$ is a property of the
structure, not of your code.

| operation | BST (balanced) | binary heap |
| --- | --- | --- |
| find minimum | $O(\log n)$ | $O(1)$ |
| extract minimum | $O(\log n)$ | $O(\log n)$ |
| insert | $O(\log n)$ | $O(\log n)$ |
| **search arbitrary key** | $O(\log n)$ | $\Theta(n)$ |
| **sorted traversal** | $\Theta(n)$ | $\Theta(n \log n)$ |
| build from $n$ items | $\Theta(n\log n)$ | $\Theta(n)$ |
| space per element | key + 2 pointers | **key** |

Read the table as a trade, not a ranking. The heap gives up the two operations that need global order
and, in exchange, wins the three that do not. **If your workload is "insert, and repeatedly remove
the smallest," every column you lost is a column you were not going to read.**

---

## 7. What to Do

- Read CLRS §6.1–6.2. **CLRS is 1-indexed** — reread section 4 before you translate anything.
- **PS 3** is released Friday. Part A is the index arithmetic and the parent-function bug above.
- **Quiz 3 covers Week 2** — rotations, the AVL height bound, the red-black properties. Not heaps.
- Next lecture: building a heap in $\Theta(n)$, and why that does not contradict the
  $\Omega(n\log n)$ sorting bound.

---

*CS 102 · Week 3 · Lecture 10 · © CSE Department*
