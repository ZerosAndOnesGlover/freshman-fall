# CS 102 · Problem Set 11
## Computational Geometry and Spatial Structures

**Released:** Friday 9 April 2027, 10:00 (after L36) · Week 11
**Due:** Friday 16 April 2027, 17:00 · Week 12 — late penalty from 17:01 (syllabus late policy)
**Points:** 100 · counts toward the Problem Sets component (35%, lowest one dropped)
**Expected time:** about 4 hours

**Submit:** `ps11.py` (runnable end to end) and `ps11.md` (written answers and tables).

## What this problem set uses

Week 11: the cross product, orientation, segment intersection and the shoelace area (L34–L35), the
monotone-chain hull and its degenerate cases, floating point and `fractions.Fraction` (L34), the
closest pair and its packing constant (L35), and segment trees (L36). Amortised arguments from Weeks
3, 6 and 10 are named in B4.

**Not needed and not expected:** point-in-polygon tests (never taught), timing, and the k-d tree
curse-of-dimensionality measurement — that is Lab 11's job.

> **This is the last problem set.** It is due the same day as **PROJECT 2** (Friday 16 April); the
> final exam follows on Wednesday 21 April. Parts A and B are short; Part D is the longest.
> **Prioritise the project.**
>
> Recall that the lowest problem-set score is dropped. If one thing has to go, this is the cheapest
> one to lose — but read Part D's note before deciding.

---

## Part A — Primitives (19 points)

**Use integer coordinates throughout Parts A–C.** Part D explains why.

**A1.** *(5)* `cross(o, a, b)` and `orient(o, a, b)` returning $-1$, $0$ or $+1$.

**A2.** *(8)* `segments_intersect(p1, p2, p3, p4)` using four orientation tests plus bounding-box
checks for the collinear cases.

Verify it against **all seven** of these, reporting expected and actual:

| case | expected |
| --- | --- |
| proper crossing | True |
| collinear, disjoint | False |
| collinear, overlapping | True |
| T-junction | True |
| collinear with a gap | False |
| same line, far apart | False |
| shared endpoint | True |

**A3.** *(6)* Polygon area from the cross product (the shoelace formula), verified on a square, a
triangle and a non-convex polygon.

State what the **sign** of your result means and how to make it orientation-independent.

---

## Part B — Convex Hull (26 points)

**B1.** *(9)* `hull(pts)` by Andrew's monotone chain.

Verify against a brute-force hull on at least 500 random **integer** point sets that deliberately
include duplicates and collinear runs. Report mismatches.

**B2.** *(7)* Implement **both** conventions — `cross <= 0` (vertices only) and `cross < 0` (all
boundary points).

Report both hulls for $(0,0), (1,0), (2,0), (3,0), (1,1)$, and give one application that wants each.

**B3.** *(5)* Run the `< 0` version on five **collinear** points. Report exactly what it returns.

Explain the failure, and give the special case needed to fix it.

**B4.** *(5)* Prove the scan is $\Theta(n)$ after sorting.

Your argument must name what is pushed and what is popped, and why the total is linear. **This is the
fifth amortised argument of the course** — name the other four.

---

## Part C — Closest Pair (16 points)

**C1.** *(8)* Brute-force closest pair, and the divide-and-conquer version.

Verify they agree on at least 500 random point sets. Report mismatches.

**C2.** *(8)* The strip step compares each point with only the next few in $y$ order.

- **(a)** *(5)* State the constant, and **justify it** by a packing argument — how many points can a
  $d \times 2d$ rectangle hold if no two are closer than $d$?
- **(b)** *(3)* What would the complexity be without that bound?

---

## Part D — Floating Point (21 points)

**This part is the reason Parts A–C specified integers.**

**D1.** *(6)* Construct collinear triples in `float`: pick $A$, a direction $(dx, dy)$, and two
multiples $t_1 < t_2$ along it, all drawn from `random.uniform`.

Over at least 100,000 such triples, report how many have a **non-zero** cross product.

**D2.** *(6)* For at least 20,000 of the same triples, compare the **sign** of the float cross product
against the sign computed with `fractions.Fraction`.

Report the number of disagreements.

**D3.** *(9)* **Does it change an answer?**

Generate random points, then add points constructed to lie on segments *between* existing points.
Compute the convex hull twice — once in `float`, once with `Fraction` — and compare the **number of
vertices**.

Over at least 1,000 point sets, report how many disagree. Then answer:

- **(a)** *(4)* Why does adding points on segments make this worse?
- **(b)** *(3)* Someone proposes `abs(cross) < 1e-9` as a fix. **Give a concrete reason this is worse
  than doing nothing**, in terms of a property the comparison must have.
- **(c)** *(2)* State the two things you would actually do.

---

## Part E — Segment Trees (18 points)

**E1.** *(10)* A **segment tree** over an integer array supporting range `min` and point update.

Verify against direct recomputation on at least 300 arrays with at least 30 mixed operations each.

---

**E2.** *(8)* A **prefix-sum array** answers range *sums* too. State what it does better than your
segment tree, and the two things it cannot do at all (Lecture 36 §2).

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 19 | The cross product, and the degenerate cases |
| B | 26 | Convex hull, both conventions, and the amortised bound |
| C | 16 | Closest pair, and the packing constant |
| D | 21 | Why floating point breaks geometry |
| E | 18 | Segment trees against prefix sums |
| **Total** | **100** | |

---

## Reference Numbers

Python 3.14, x86-64 Linux. **Counts are deterministic; timings are not.**

**B2** — points $(0,0), (1,0), (2,0), (3,0), (1,1)$:

| convention | hull |
| --- | --- |
| `cross <= 0` | $(0,0), (3,0), (1,1)$ — 3 vertices |
| `cross < 0` | $(0,0), (1,0), (2,0), (3,0), (1,1)$ — 5 points |

**B3** — five collinear points $(0,0) \dots (4,0)$ with `< 0`:

$$(0,0), (1,0), (2,0), (3,0), (4,0), (3,0), (2,0), (1,0)$$

**Every interior point appears twice.**

**D1 / D2 / D3:**

| measurement | result |
| --- | --- |
| collinear triples with non-zero cross product | **130,443 of 200,000** (65.2%) |
| float signs differing from exact | **18,190 of 50,000** (36.4%) |
| **point sets whose float hull has a different vertex count** | **573 of 3,000** (**19.1%**) |

**All verification mismatch counts should be 0.**

---

## A Note on Part D

Every other problem set this term has asked you to make something work. **Part D asks you to establish
that something you already wrote does not**, on input it will certainly meet.

The convex hull in Part B is correct. Give it floating-point coordinates with points lying on segments
— which is what any dataset with shared boundaries produces — and **19% of the time it returns a
polygon with the wrong number of vertices.** Not a rounding error in the coordinates; a different
polygon.

**D3(b) is the graded idea.** An epsilon comparison is the reflexive fix and it makes things worse,
because it destroys **transitivity**: three points can be pairwise "collinear" without being collinear
as a triple, and a sort using an inconsistent comparator has undefined behaviour. The result is not a
slightly wrong hull; it is an intermittent crash that depends on the input order.

This is the last thing this course has to say about correctness, and it is the least comfortable:
**an algorithm can be proved correct and still be wrong on your machine**, because the proof was about
the real numbers and your machine does not have those.

---

*CS 102 · Week 11 · Problem Set 11 · © CSE Department*
