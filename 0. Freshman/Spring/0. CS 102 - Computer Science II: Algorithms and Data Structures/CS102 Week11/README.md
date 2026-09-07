# CS 102 · Computer Science II — Algorithms and Data Structures
## Week 11: Computational Geometry and Advanced Data Structures

**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **PS 11** (released Friday, due Friday of Week 12 — **the last problem
set**), Lab 11, **Quiz 11 — which covers Week 10** and is the last quiz.
**PROJECT 2 is due Friday of Week 12.** The **FINAL EXAM** is in Week 12 and is comprehensive.

---

### Why This Week Exists

Computational geometry looks like it needs trigonometry. It does not. **Nearly everything this week
rests on one expression:**

$$\mathrm{cross}(O, A, B) = (A_x - O_x)(B_y - O_y) - (A_y - O_y)(B_x - O_x)$$

Its sign says whether $B$ is left of, right of, or on the directed line $O \to A$. No angles, no
division, no square roots — and with integer inputs it is **exact**. Convex hull, segment
intersection, polygon area and point-in-polygon are all that one predicate in a loop.

The week's second half is spatial structures — segment trees and k-d trees — and it ends with the most
extreme "correct but useless" result in the course.

### Learning Objectives

By the end of Week 11, you should be able to:

1. Use the cross product for orientation, area, and segment intersection, and say why no
   trigonometry is needed.
2. Handle the degenerate cases — collinear, duplicate, shared-endpoint — and recognise that they are
   most of the code.
3. Implement the convex hull by monotone chain, **choose between the two collinear conventions**, and
   prove the scan linear.
4. Implement the closest pair in $\Theta(n\log n)$ and **justify the packing constant**.
5. State what the sweep-line algorithm costs and which two data structures it needs.
6. Explain why floating point breaks geometric predicates, and why an epsilon makes it worse.
7. Implement a segment tree, and say what a prefix-sum array does better and what it cannot do.
8. Implement a k-d tree, and **identify the dimension at which it stops being worth using**.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L34 Geometric Primitives and Convex Hull]] | The cross product, monotone chain, degeneracies, and float robustness |
| [[L35 Segment Intersection and Closest Pair]] | Four orientation tests, the sweep line, and the packing argument |
| [[L36 Segment Trees and k-d Trees]] | Range queries, and the curse of dimensionality measured |
| [[PS 11 Computational Geometry]] | 100 points, due Friday of Week 12 — the last problem set |
| [[CS102 Week11/assignments/QUIZ 11 Week 11 Monday\|QUIZ 11 Week 11 Monday]] | 20 points, formative — **covers Week 10** |
| [[LAB 11 A 2D Nearest-Neighbour Searcher]] | Build it, measure it, and find where it stops paying |
| [[CS102 Week11/resources/Reading Guide Week 11\|Reading Guide Week 11]] | CLRS Ch. 33, plus what CLRS omits |
| `solutions_instructor/` | PS 11 and Lab 11 solutions — instructor only |

### The Three Ideas Most Likely to Be Missed

**1. The degenerate cases are the algorithm.** A convex hull on points in general position is ten
lines. Changing `cross(...) <= 0` to `< 0` changes whether collinear boundary points are returned —
**both are defensible and they answer different questions.** And the `<` version on fully collinear
input returns every interior point **twice**, silently producing a polygon with repeated vertices that
most downstream code accepts.

**2. Floating point does not merely lose precision here — it changes the answer.** Over 200,000
constructed-collinear triples, **65.2%** have a non-zero cross product, and **36.4%** of computed signs
disagree with exact rational arithmetic. The consequence: with points lying on segments between other
points, **19.1% of point sets give a float hull with a different number of vertices than the exact
hull.** Not a rounding error — a different polygon.

**3. A k-d tree stops being useful long before it stops being correct.** At $n = 8192$:

| dimensions | nodes visited | brute force | k-d tree |
| --- | --- | --- | --- |
| 2 | 20 (0.2%) | 6.75 ms | **0.02 ms** — 337× faster |
| 8 | 787 (9.6%) | 13.61 ms | 1.78 ms |
| **16** | **8,071 (98.5%)** | 22.49 ms | **25.06 ms — slower** |
| 32 | 8,192 (100%) | 37.72 ms | 42.94 ms |

**The tree returns the true nearest neighbour at every dimension.** No correctness test would ever
detect that it has stopped being worth using.

### A Warning About the Obvious Fix

Faced with §2, the reflexive response is `abs(cross) < 1e-9`. **This is worse than doing nothing.**

An epsilon comparison is not **transitive**: three points can be pairwise "collinear" without being
collinear as a triple. A sort built on a non-transitive comparator has undefined behaviour — in C++ it
can read out of bounds and crash. **The failure mode changes from a wrong polygon to an intermittent
crash that depends on input order**, which is far harder to diagnose.

The two things that actually work: **use integers where the data permits**, and **use exact or
adaptive predicates** (Shewchuk, CGAL) where it does not. This is the one place in the course where
the right answer is "use a library".

### A Note on the Measurements

**Counts are deterministic** — hull outputs on integer input, node-visit counts, and every verification
total. The float measurements in Part D are sampling estimates and will vary by a percentage point.

**Timings are not**, and the k-d tree table's *ratios* matter more than its milliseconds: the
progression from 0.2% to 98.5% of nodes visited is the result, and it reproduces on any machine.

### Connections

**Back:** The hull scan's linearity is the **fifth** amortised argument of the course, after **Week 3**'s
`BUILD-HEAP`, **Week 6**'s union-find, and **Week 10**'s KMP and Kasai. The sweep line needs **Week 3**'s
priority queue and **Week 2**'s balanced BST, for reasons having nothing to do with geometry. Segment
trees are **Week 3**'s array-embedded tree with the same $2i, 2i+1$ arithmetic. Lab 11's $k$-nearest
uses **Week 3**'s bounded heap. The closest pair is **Week 0**'s divide and conquer.

**Forward:** **Week 12** is the last week — NP-completeness, and knowing when to stop looking for a
better algorithm. It is the natural end: this week's k-d tree fails for a reason you can measure and
work around; Week 12's problems fail for a reason nobody knows how to fix. **PROJECT 2** and **PS 11**
are both due Friday of Week 12, and the **FINAL EXAM** is comprehensive.

---

*CS 102 · Week 11 · © CSE Department*
