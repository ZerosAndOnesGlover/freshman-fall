# CS 102 · Reading Guide, Week 11
## Computational Geometry and Spatial Structures

---

## Required

**The CLRS 4th edition has no computational geometry chapter** (its Chapter 33 is machine learning).
The sections below are **Chapter 33 of the CLRS 3rd edition**, §33.1–33.4, about 25 pages. With only
the 4th edition, read de Berg et al. §1.1 (convex hulls) and §2.1 (segment intersection), Kleinberg &
Tardos §5.4 (closest pair), and the *Competitive Programmer's Handbook* Ch. 29–30 instead.

- §33.1 line-segment properties — **the section that matters**
- §33.2 determining whether any pair of segments intersects (the sweep line)
- §33.3 convex hull
- §33.4 finding the closest pair of points

**Segment trees and k-d trees are not in CLRS.** Use:

- **de Berg et al. §5.2** — kd-trees;
- **Competitive Programmer's Handbook (Laaksonen), Ch. 9** — the clearest short treatment of segment
  trees anywhere, and free;
- **de Berg, Cheong, van Kreveld & Overmars, *Computational Geometry***, Ch. 1–5 — the standard
  reference, and unusually readable.

> **PROJECT 2 is due Friday 16 April** and the **FINAL EXAM** is Wednesday 21 April. If reading must be cut,
> read §33.1 properly and skim the rest.

---

## Read §33.1 First and Slowly

Chapter 33's first section defines the cross product and the orientation test, and **every other
algorithm in the chapter is that test in a loop.** Convex hull, segment intersection, point-in-polygon
and polygon area are all the same three-line predicate applied differently.

If you take one thing from this week, take this:

> The **sign** of $(A-O) \times (B-O)$ says whether $B$ is left of, right of, or on the directed line
> $O \to A$.

No angles, no trigonometry, no division, and — with integer inputs — **exact**.

CLRS is also unusually careful here about the degenerate cases: collinear points, shared endpoints,
zero-length segments. **Read those paragraphs rather than skipping to the algorithm.** In geometry the
degenerate cases are most of the code and essentially all of the bugs.

---

## How to Read It

**§33.1 (7 pages).** The cross product, orientation, and segment intersection with all its special
cases. The most valuable seven pages of the chapter.

**§33.2 (8 pages).** The sweep-line algorithm for detecting whether *any* two segments intersect. Read
for the **idea** — events in a priority queue, an active set in a balanced BST — not to implement it.
Note which two data structures it needs and where they came from.

**§33.3 (7 pages).** Graham scan and Jarvis march. **Andrew's monotone chain** — what the lectures use
and what you should implement — is Problem 33-2. It avoids angular sorting entirely and is shorter.

**§33.4 (5 pages).** Closest pair. The content is the argument that only a constant number of points
need be compared in the strip; make sure you can reproduce the packing argument, not just quote the
constant.

---

## Guiding Questions

Three of these are on the final.

1. §33.1: state what the sign of the cross product means geometrically. Then give **three** different
   problems it solves without any further machinery.

2. §33.1: segment intersection needs four orientation tests plus bounding-box checks. What exactly do
   the bounding-box checks handle that the orientation tests cannot?

3. §33.3: in the monotone-chain scan, prove the total work after sorting is $\Theta(n)$. What is pushed
   and what is popped?

4. Changing `cross(...) <= 0` to `< 0` changes which points the hull contains. Describe both results
   and name an application wanting each.

5. §33.4: why is a **constant** number of comparisons enough in the strip? Give the packing argument,
   and say what the algorithm would cost without it.

6. §33.2: the sweep line needs a priority queue and a balanced BST. Which weeks introduced them, and
   for what unrelated purposes?

7. A k-d tree prunes by comparing one coordinate against the current best distance. Explain why that
   test almost never fires in 32 dimensions.

---

## Common Misreadings

**"Geometry needs trigonometry."** Almost none of it does. Angles, `atan2` and square roots introduce
floating point where integers would have been exact. **If you find yourself computing an angle, ask
whether a cross product would do** — it usually would.

**"Degenerate cases are edge cases you handle at the end."** They are most of the code and all of the
bugs. Collinear points, shared endpoints, duplicated points and axis-aligned input are the *normal*
case for real data — grids, screen coordinates, and anything snapped to a resolution.

**"The convex hull algorithm is ten lines, so it is easy."** The ten lines are easy. Getting the right
answer on collinear input, on duplicated points, on fewer than three points, and in floating point is
not. Measured: with points lying on segments between other points, a float hull has a **different
number of vertices** from the exact hull on **19.1%** of random point sets.

**"An epsilon fixes floating-point geometry."** It makes it worse. `abs(cross) < eps` is not
transitive — three points can be pairwise "collinear" without being collinear as a triple — and a sort
with an inconsistent comparator has undefined behaviour. The symptom is an intermittent crash that
depends on input order, which is far harder to diagnose than a wrong polygon.

**"A k-d tree makes nearest-neighbour search fast."** In two dimensions, by a factor of 337. In
sixteen it visits **98.5%** of the data and is **slower than a linear scan**, while remaining perfectly
correct. Spatial indexing is a low-dimensional subject.

**"Segment trees are for range sums."** A prefix-sum array does range sums better — $O(1)$ per query.
A segment tree buys **updates** and **non-invertible operations** (min, max, gcd). If you need neither,
you are paying $O(\log n)$ for nothing.

---

## If You Have Extra Time

**Exact geometric predicates.** Shewchuk's adaptive-precision arithmetic evaluates orientation tests
using floating point first and escalating only when the answer is too close to zero to trust — exact
results at nearly floating-point speed. It is the foundation of CGAL and of most serious geometry
software, and the paper is readable.

**Rotating calipers.** Once you have a convex hull, the diameter of a point set, the width, the
smallest enclosing rectangle and the maximum distance between two convex polygons all fall out in
$\Theta(h)$ by walking two pointers around the hull. It is the best return on a hull you will find.

**Lazy propagation in segment trees.** Extends point updates to **range** updates in $O(\log n)$ by
deferring work down the tree. It is where segment trees become genuinely powerful, and it is the single
most useful extension in this lecture.

**Fenwick trees (binary indexed trees).** A segment tree's smaller, faster cousin for invertible
operations — one array, a dozen lines, and a beautiful bit trick. It cannot do `min`, which is exactly
the trade Lecture 36 §2 describes.

**Locality-sensitive hashing and HNSW.** What actually powers high-dimensional similarity search — the
retrieval half of every modern embedding-based system. Both are approximate by design, for the reason
Lecture 36 §4 measures.

---

*CS 102 · Week 11 · Reading Guide · © CSE Department*
