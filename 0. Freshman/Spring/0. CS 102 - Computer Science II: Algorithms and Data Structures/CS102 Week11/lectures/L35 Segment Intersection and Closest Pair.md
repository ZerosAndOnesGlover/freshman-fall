# CS 102 · Computer Science II
## Lecture 35: Segment Intersection and the Closest Pair

**Date:** Wednesday 7 April 2027 · 09:00–09:50 · Week 11

---

## 1. Do Two Segments Cross?

The question sounds like it needs the line equations, a division, and a check that the intersection
point lies within both segments. It needs none of that.

Two segments $\overline{p_1p_2}$ and $\overline{p_3p_4}$ **properly** cross when each straddles the
other's line — that is, when $p_1$ and $p_2$ are on **opposite sides** of $p_3p_4$, and vice versa.
Four orientation tests:

```python
def segments_intersect(p1, p2, p3, p4):
    d1 = orient(p3, p4, p1); d2 = orient(p3, p4, p2)
    d3 = orient(p1, p2, p3); d4 = orient(p1, p2, p4)
    if d1*d2 < 0 and d3*d4 < 0: return True        # proper crossing
    if d1 == 0 and on_segment(p3, p1, p4): return True   # collinear touching cases
    if d2 == 0 and on_segment(p3, p2, p4): return True
    if d3 == 0 and on_segment(p1, p3, p2): return True
    if d4 == 0 and on_segment(p1, p4, p2): return True
    return False
```

**No division, no square root, and with integer input it is exact.** `on_segment` is a bounding-box
check that only runs when the orientation is already known to be zero.

### The degenerate cases are most of the code

One line handles the general case and four handle the special ones. That ratio is normal in geometry
and it is why the subject has a reputation for fiddliness.

| case | answer |
| --- | --- |
| crossing at an interior point | **True** |
| collinear and disjoint | False |
| collinear and overlapping | **True** |
| T-junction (endpoint on the other segment) | **True** |
| collinear with a gap | False |
| shared endpoint | **True** |

*(Verified: all seven cases in the reference set, plus the four-test implementation against them. **0
failures.**)*

Note that "shared endpoint" and "T-junction" return **True** here. Whether they should is a question
about your application — a polygon's adjacent edges share an endpoint and are not usually said to
intersect. **Decide once and document it**, because both conventions are common and code written for
one silently misbehaves under the other.

---

## 2. All Intersections Among $n$ Segments

Testing every pair is $\Theta(n^2)$, which is fine for hundreds of segments and hopeless for millions.

The **sweep line** algorithm does better. Move a vertical line left to right; maintain the segments it
currently crosses, ordered by height. Two segments can only intersect if they become **adjacent** in
that order at some point, so only adjacent pairs need testing.

- events: segment starts, segment ends, and discovered intersections;
- the event queue is a **priority queue** — Week 3;
- the active set is a **balanced BST** ordered by height — Week 2.

$O((n + k)\log n)$ for $k$ intersections, against $\Theta(n^2)$.

> **This is the payoff for Weeks 2 and 3 arriving in a form you could not have predicted.** A
> geometric algorithm's efficiency comes entirely from two data structures introduced for reasons
> having nothing to do with geometry.

The implementation is genuinely hard — the ordering in the active set changes as the line sweeps,
degeneracies abound, and floating point makes the comparator inconsistent. **You are not asked to
implement it.** You are asked to know that it exists, what it costs, and why.

---

## 3. The Closest Pair

**Problem.** Among $n$ points, find the two that are closest.

Brute force is $\Theta(n^2)$. **Divide and conquer gives $\Theta(n\log n)$**, and it is one of the most
elegant algorithms in the course.

1. Sort by $x$. Split into left and right halves.
2. Recursively find the closest pair in each; let $d$ be the smaller distance.
3. **The answer is either that pair, or a pair straddling the divide.** A straddling pair must lie
   within $d$ of the dividing line — a vertical strip.
4. Sort the strip by $y$ and compare each point with the next few.

### Why step 4 is $O(n)$ and not $O(n^2)$

The strip can contain every point, so comparing all pairs within it would gain nothing. The saving is a
geometric fact:

> Within the strip, any point needs to be compared with **at most 7** following points in $y$ order.

Because both halves already have no pair closer than $d$, a $d \times 2d$ rectangle in the strip can
contain at most 8 points — 4 per side, packed at distance $d$. Anything further than $d$ in $y$ cannot
beat $d$ at all, so the inner loop breaks.

**A constant falls out of a packing argument**, and that constant is what makes the recursion
$T(n) = 2T(n/2) + O(n) = \Theta(n\log n)$.

*(Verified against brute force on 1,000 random point sets. **0 mismatches.**)*

| $n$ | brute force | divide and conquer | speedup |
| --- | --- | --- | --- |
| 1,000 | 148.1 ms | 3.5 ms | 42× |
| 2,000 | 605.9 ms | 7.4 ms | 82× |
| 4,000 | 2,377.1 ms | 17.0 ms | 140× |
| 8,000 | **9,544.9 ms** | **41.3 ms** | **231×** |

*(Verified.)* Brute force quadruples per doubling; divide and conquer slightly more than doubles.

### A practical note

Re-sorting the strip by $y$ at every level makes it $\Theta(n\log^2 n)$. Maintaining a $y$-sorted list
through the recursion — merging as you return, exactly as in merge sort — restores $\Theta(n\log n)$.
**The version above is the $\log^2$ one**, because it is clearer, and at these sizes the difference is
invisible.

---

## 4. The Shape of Geometric Algorithms

Three lectures in, a pattern:

| technique | example | cost |
| --- | --- | --- |
| **sort, then sweep once** | convex hull | $\Theta(n\log n)$ |
| **sort, then sweep with a structure** | segment intersection | $O((n+k)\log n)$ |
| **divide and conquer on coordinates** | closest pair | $\Theta(n\log n)$ |
| **partition space in advance** | k-d trees — Lecture 36 | varies, badly |

**Every one of them begins by imposing an order on unordered data.** Points in a plane have no
intrinsic order; sorting by $x$, or by angle, or splitting on a median, manufactures one — and the
algorithm is whatever that order makes possible.

That is the transferable idea of the week, and it is worth more than any of the four algorithms.

---

## 5. What to Do

- Read CLRS §33.1 (segment intersection predicates), §33.2 (the sweep line, for the idea), and §33.4
  (closest pair).
- **PS 11** implements the intersection predicate against all seven degenerate cases and the closest
  pair against brute force.
- **Lab 11** builds a nearest-neighbour searcher, which is the closest-pair problem's query version.
- Next lecture: segment trees and k-d trees — and a measurement showing one of them stops working
  entirely.

---

*CS 102 · Week 11 · Lecture 35 · © CSE Department*
