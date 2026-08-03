# CS 102 · Computer Science II
## Lecture 36: Segment Trees and k-d Trees

---

## 1. Two Structures for Range Queries

Both of this lecture's structures answer questions about *regions* rather than individual items — a
range of an array, a region of the plane. Both are built once and queried many times, which is the
same trade as Week 10's suffix arrays.

One of them scales. **The other stops working**, and §5 measures exactly where.

---

## 2. Segment Trees

**Problem.** Given an array, answer `min(a[l:r])` many times, with **updates** interleaved.

| approach | query | update |
| --- | --- | --- |
| recompute `min(a[l:r])` | $\Theta(n)$ | $O(1)$ |
| precompute all $\binom{n}{2}$ ranges | $O(1)$ | $\Theta(n^2)$ |
| **segment tree** | $O(\log n)$ | $O(\log n)$ |

A segment tree is a complete binary tree over the array; each node stores the answer for its range,
each leaf one element. A query decomposes $[l, r)$ into $O(\log n)$ canonical nodes.

```python
class SegTree:
    def __init__(self, a, op=min, ident=float('inf')):
        self.n, self.op, self.ident = len(a), op, ident
        self.size = 1
        while self.size < self.n: self.size *= 2
        self.t = [ident] * (2 * self.size)
        for i, x in enumerate(a): self.t[self.size + i] = x
        for i in range(self.size - 1, 0, -1):
            self.t[i] = op(self.t[2*i], self.t[2*i+1])

    def update(self, i, v):
        i += self.size; self.t[i] = v; i //= 2
        while i: self.t[i] = self.op(self.t[2*i], self.t[2*i+1]); i //= 2

    def query(self, l, r):                      # [l, r)
        res = self.ident; l += self.size; r += self.size
        while l < r:
            if l & 1: res = self.op(res, self.t[l]); l += 1
            if r & 1: r -= 1; res = self.op(res, self.t[r])
            l //= 2; r //= 2
        return res
```

**This is Week 3's array-embedded tree again** — the same $2i$, $2i+1$ index arithmetic, for the same
reason: the shape is fixed, so the pointers carry no information.

*(Verified: 500 trees, 30 mixed queries and updates each, against direct recomputation. **0
mismatches.**)*

| $n$ | 2,000 queries by `min(a[l:r])` | by segment tree | speedup |
| --- | --- | --- | --- |
| 10,000 | 97.5 ms | 4.3 ms | 22× |
| 50,000 | 501.1 ms | 5.6 ms | 90× |
| 200,000 | **2,740.4 ms** | **8.3 ms** | **332×** |

*(Verified.)* Note the segment tree's column barely grows — $O(\log n)$ against $O(n)$.

### What you are actually buying

A **prefix-sum array** answers range *sum* in $O(1)$ with $\Theta(n)$ preprocessing, which is better
than a segment tree. But it needs the operation to be **invertible** — sum minus sum — and it cannot
handle updates without rebuilding.

> **The segment tree's $O(\log n)$ buys two things a prefix array cannot give: updates, and
> non-invertible operations** like `min`, `max` and `gcd`. If you need neither, do not use one.

`op` is a parameter for exactly that reason: any **associative** operation works. Sum, min, max, gcd,
matrix product, "leftmost zero". The structure does not care.

**Lazy propagation** extends it to *range* updates — add 5 to everything in $[l,r)$ — in $O(\log n)$ by
deferring the work. It is the natural next thing to read and it is where segment trees get genuinely
powerful.

---

## 3. k-d Trees

**Problem.** Given $n$ points, find the nearest to a query point, many times.

A **k-d tree** splits space by one coordinate at a time, cycling through the axes: split on $x$ at the
root, on $y$ at depth 1, on $x$ again at depth 2.

```python
def build(pts, depth=0, k=2):
    if not pts: return None
    ax = depth % k
    pts = sorted(pts, key=lambda p: p[ax])
    m = len(pts) // 2
    node = KD(pts[m], ax)
    node.left  = build(pts[:m],   depth+1, k)
    node.right = build(pts[m+1:], depth+1, k)
    return node
```

$\Theta(n\log^2 n)$ to build as written, $\Theta(n\log n)$ with a linear-time median.

### The query, and the line that matters

```python
def nearest(node, q):
    best = [inf, None]
    def go(n):
        if n is None: return
        d = dist2(n.pt, q)
        if d < best[0]: best[0], best[1] = d, n.pt
        diff = q[n.axis] - n.pt[n.axis]
        near, far = (n.left, n.right) if diff < 0 else (n.right, n.left)
        go(near)
        if diff * diff < best[0]:               # <-- the pruning test
            go(far)
    go(node)
    return best
```

Search the side the query is on, then **ask whether the other side could possibly contain something
closer**. If the splitting plane is further away than the best distance so far, the whole subtree is
skipped.

*(Verified against brute force on 500 random 2-D queries. **0 mismatches.**)*

**Everything depends on that pruning test firing.** When it does, the search is $O(\log n)$. When it
does not, the search visits every node — and it is a linear scan with tree overhead on top.

---

## 4. The Curse of Dimensionality

Here is the measurement, and it is the point of the lecture. Same code, same 8,192 points, only the
dimension changing:

| dimensions | nodes visited | as % of $n$ | brute force | k-d tree |
| --- | --- | --- | --- | --- |
| 2 | **20** | **0.2%** | 6.75 ms | **0.02 ms** |
| 4 | 62 | 0.8% | 8.73 ms | 0.09 ms |
| 8 | 787 | 9.6% | 13.61 ms | 1.78 ms |
| 16 | **8,071** | **98.5%** | 22.49 ms | **25.06 ms** |
| 32 | **8,192** | **100.0%** | 37.72 ms | 42.94 ms |

*(Verified. Averages over 200 queries; correctness spot-checked against brute force at every
dimension.)*

**In 2-D the tree visits 20 of 8,192 points and is 337× faster than a linear scan. In 16-D it visits
98.5% of them and is *slower*.** By 32 dimensions it visits every single point and pays for the tree
on top.

### Why

The pruning test asks whether the distance along **one axis** already exceeds the best distance found.
In high dimensions, distance is spread across many coordinates, so any single coordinate's contribution
is a small fraction of the total — and one small quantity almost never exceeds the whole. Nothing gets
pruned.

There is a related fact that makes the whole problem ill-posed: **in high dimensions, the nearest and
farthest points are nearly equidistant.** As $d$ grows, the ratio of the maximum to the minimum
distance from a query point tends to 1 for many distributions. When everything is roughly the same
distance away, "nearest neighbour" stops being a meaningful question, regardless of the data structure.

### What is done instead

- **Approximate nearest neighbour.** Accept a point within $(1+\varepsilon)$ of the true nearest.
  **Locality-sensitive hashing** and **HNSW graphs** are what production vector search uses, and both
  are approximate by design.
- **Reduce the dimension first.** PCA or random projection to 10–50 dimensions, then a k-d tree.
- **Just scan.** At $d = 128$ a brute-force scan with vectorised arithmetic beats every tree, and it
  is simpler and exact.

> **This is the last "correct under an assumption" case in the course, and the most extreme.** A k-d
> tree is correct at every dimension — it returns the true nearest neighbour in all five rows above.
> **What fails is not correctness but the reason for using it**, and no test of correctness would ever
> reveal that.

---

## 5. Choosing a Spatial Structure

| structure | good for | fails when |
| --- | --- | --- |
| **segment tree** | 1-D ranges with updates | you only need sums and never update |
| **Fenwick tree** | prefix sums with updates | the operation is not invertible |
| **k-d tree** | low-dimensional nearest neighbour | $d \gtrsim 10$ |
| **quadtree / octree** | 2-D and 3-D spatial data, non-uniform | high dimensions; deep unbalanced trees |
| **R-tree** | rectangles and spatial databases | high dimensions |
| **LSH / HNSW** | high-dimensional approximate search | you need an exact answer |

**Every row above 10 dimensions says the same thing**, and the honest summary of spatial indexing is
that it is a low-dimensional subject.

---

## 6. Where Week 11 Leaves You

Two structures, one that scales and one whose usefulness evaporates at a threshold you can measure.

**Week 12** is the last week: NP-completeness, and the question of which problems have no efficient
algorithm at all. It is the natural end of this course, because everything up to here has been about
finding a good algorithm and Week 12 is about knowing when to stop looking.

**PROJECT 2 is due Friday of Week 12**, and the **FINAL EXAM** is in Week 12 and is comprehensive.

---

## 7. What to Do

- Segment trees and k-d trees are not in CLRS. **Sedgewick §3.5** covers geometric search; the
  *Competitive Programmer's Handbook* Chapter 9 is the best short treatment of segment trees.
- **PS 11** implements both and reproduces §4's dimension table.
- **Lab 11** builds a nearest-neighbour searcher and finds the dimension where it stops paying.
- **Quiz 11 covers Week 10.**

---

*CS 102 · Week 11 · Lecture 36 · © CSE Department*
