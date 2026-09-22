# CS 102 · Problem Set 11 — Solutions
## Computational Geometry and Spatial Structures

**INSTRUCTOR / TA COPY — not for distribution**

Every number was produced by running code. **Deterministic** figures should match; **machine-dependent**
ones will not.

> **This is the last problem set**, due the same day as Project 2 in final-exam week. The handout told
> students to prioritise the project and reminded them the lowest score is dropped. **Mark
> accordingly** — see the note at the end.

---

> **Revised 2026-09-22.** Removed: A4 (point in polygon by ray casting — never taught), C2 and E2's
> timing, and E3 (the k-d tree dimension sweep — Lab 11 Part C verbatim). C3→C2; E2 is now only the
> prefix-sum question; items re-weighted to keep 100 points.

## Part A — Primitives (19)

### A1 (5), A2 (8) — deterministic

All seven intersection cases must pass:

| case | expected |
| --- | --- |
| proper crossing | True |
| collinear, disjoint | False |
| collinear, overlapping | **True** |
| T-junction | **True** |
| collinear with a gap | False |
| same line, far apart | False |
| shared endpoint | **True** |

*The three collinear cases are where implementations fail. A student whose code returns False for
"collinear, overlapping" has the four orientation tests right and no bounding-box check — the most
common error, and it passes on random input because exact collinearity is rare.*

### A3 (6)

Shoelace: $2A = \sum (x_i y_{i+1} - x_{i+1} y_i)$. The **sign** gives the orientation —
positive for counter-clockwise, negative for clockwise. Take the absolute value for area.

## Part B — Convex Hull (26)

### B1 (9) — deterministic: 0 mismatches

500+ integer point sets with duplicates and collinear runs.

### B2 (7) — deterministic

| convention | hull of $(0,0),(1,0),(2,0),(3,0),(1,1)$ |
| --- | --- |
| `cross <= 0` | $(0,0), (3,0), (1,1)$ |
| `cross < 0` | $(0,0), (1,0), (2,0), (3,0), (1,1)$ |

Applications: `<=` for **rendering or storing the polygon** (you want vertices); `<` for **testing
whether a given point lies on the hull boundary**, or for any downstream code that needs every
collinear boundary point present.

### B3 (5) — deterministic

Five collinear points with `< 0` returns

$$(0,0), (1,0), (2,0), (3,0), (4,0), (3,0), (2,0), (1,0)$$

**Every interior point twice.** The lower and upper chains each retain all five points, and
concatenating them duplicates the interior. Fix: detect the all-collinear case (the hull has zero area)
and return the two extreme points, or de-duplicate.

*The failure is silent — the result is a "polygon" with repeated vertices that most downstream code
accepts. 4 for reporting it exactly and giving a fix; 2 for reporting it without a fix.*

### B4 (5)

Each point is **pushed exactly once** and **popped at most once**, so the total number of stack
operations across the scan is at most $2n$. The `while` loop's iterations are bounded by the total
number of pops, which is bounded by the total number of pushes.

The other four amortised arguments: **`BUILD-HEAP`** (Week 3), **union-find** (Week 6), **KMP's failure
loop** (Week 10), **Kasai's LCP algorithm** (Week 10).

*2 for the argument, 2 for naming at least three of the four. This is the fifth instance and students
should recognise the shape immediately.*

---

## Part C — Closest Pair (16)

### C1 (8) — deterministic: 0 mismatches

### C2 (8)

**(a) (4)** The constant is **7** (or 8 points in the rectangle including the one being processed).

Packing argument: consider a $d \times 2d$ rectangle in the strip, split by the dividing line into two
$d \times d$ squares. Within each square all points come from the same half, and that half has no pair
closer than $d$ — so a $d \times d$ square holds at most **4** points (the corners). Eight points
total, so a point need only be compared with the next 7 in $y$ order.

**(b) (2)** Without the bound, the strip could contain all $n$ points and comparing all pairs within it
would be $\Theta(n^2)$ per level — giving $\Theta(n^2 \log n)$ overall, worse than brute force.

*The packing argument is the mark. Quoting "7" without justification is 1 of 4.*

---

## Part D — Floating Point (21)

### D1 (6), D2 (6) — deterministic to within sampling

| measurement | reference |
| --- | --- |
| constructed-collinear triples with non-zero cross product | **130,443 of 200,000** — 65.2% |
| float signs differing from `Fraction` | **18,190 of 50,000** — 36.4% |

*Accept anything in the same range; these depend on the coordinate distribution. The **shape** —
"most collinear triples are not detected as collinear, and a large minority of signs are wrong" — is
what is being marked.*

### D3 (9) — the assessed question

**573 of 3,000 point sets (19.1%)** gave a float hull with a different vertex count from the exact
hull.

**(a) (3)** Points constructed to lie on segments between others are **exactly collinear in exact
arithmetic and almost never collinear in floating point.** Those are precisely the points whose
inclusion depends on the sign of a near-zero cross product, so each one is a coin flip.

**(b) (3)** An epsilon test destroys **transitivity**: $A,B,C$ can be "collinear" and $B,C,D$
"collinear" without $A,B,D$ being so. Any sort or comparison built on a non-transitive predicate has
**undefined behaviour** — in CPython, `sorted` may produce a garbage order; in C++ `std::sort` can read
out of bounds and crash. **The failure mode changes from a wrong answer to an intermittent crash that
depends on input order**, which is strictly harder to diagnose.

**(c) (2)** Use **integer or fixed-point coordinates** where the data permits; otherwise use **exact or
adaptive predicates** (Shewchuk, CGAL).

*(b) is the graded idea. "It's imprecise" or "eps is hard to choose" scores 1 — the answer must name
transitivity or the resulting undefined behaviour.*

---

## Part E — Segment Trees (18)

### E1 (10) — deterministic: 0 mismatches

### E2 (8)

A prefix-sum array does range **sum** in $O(1)$, better than a segment tree. It **cannot** handle
updates without an $\Theta(n)$ rebuild, and **cannot** handle non-invertible operations such as `min`.

## Marking Summary

| Part | Points |
| --- | --- |
| A | 19 |
| B | 26 |
| C | 16 |
| D | 21 |
| E | 18 |
| **Total** | **100** |

---

## Notes for the Grading Meeting

**1. This set is due Friday 16 April, alongside Project 2, five days before the final.** The handout explicitly told students to
prioritise the project and reminded them the lowest problem-set score is dropped. **Expect a wide
spread and a lower submission rate than usual, and do not read that as a failure of the cohort.**
Check whether a thin submission coincides with a strong project before commenting.

**2. Part D is the intellectual close of the course.** It asks students to establish that code they
proved correct is wrong on realistic input, and D3(b) asks why the reflexive fix is worse than
nothing. Students who get D3(b) have understood something most graduates have not; say so in the
feedback, because it is the last written feedback they will get from this course.

**3. B3's silent failure is worth a comment even when correct.** The duplicated-vertex output is
accepted by almost every downstream consumer, which makes it the single most dangerous bug in the set.

**4. Carried forward.** B4 is the fifth amortised argument (`BUILD-HEAP`, union-find, KMP, Kasai, hull
scan). A student who cannot name three of the previous four has not been connecting weeks, and this is
the last opportunity to say so before the final.

**5. Forward to the final.** The exam is comprehensive. Part D's lesson — a proof is about a model,
and your machine may not implement that model — belongs in the same family as Week 3's cache effects,
Week 5's non-negativity assumption and Week 9's greedy preconditions. **That family is the course's
thesis**, and it is what Section D of the final will test.

---

*CS 102 · Week 11 · PS 11 Solutions · © CSE Department*
