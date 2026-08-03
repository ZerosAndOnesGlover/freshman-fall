# CS 102 · Problem Set 11
## Computational Geometry and Spatial Structures

**Released:** Friday, Week 11 · **Due:** Friday, Week 12, 23:59
**100 points · counts toward the Problem Sets component (35% of the final grade)**

**Submit:** `ps11.py` (runnable end to end) and `ps11.md` (written answers and tables).

> **This is the last problem set.** It is due the same day as **PROJECT 2**, in the week of the
> **FINAL EXAM**. Parts A and B are short; Part D is the longest. **Prioritise the project.**
>
> Recall that the lowest problem-set score is dropped. If one thing has to go, this is the cheapest
> one to lose — but read Part D's note before deciding.

---

## Part A — Primitives (20 points)

**Use integer coordinates throughout Parts A–C.** Part D explains why.

**A1.** *(4)* `cross(o, a, b)` and `orient(o, a, b)` returning $-1$, $0$ or $+1$.

**A2.** *(6)* `segments_intersect(p1, p2, p3, p4)` using four orientation tests plus bounding-box
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

**A3.** *(5)* Polygon area from the cross product (the shoelace formula), verified on a square, a
triangle and a non-convex polygon.

State what the **sign** of your result means and how to make it orientation-independent.

**A4.** *(5)* `point_in_polygon(p, poly)` by ray casting.

Report what your implementation does when the point lies **exactly on an edge**, and say why that case
has no universally right answer.

---

## Part B — Convex Hull (22 points)

**B1.** *(8)* `hull(pts)` by Andrew's monotone chain.

Verify against a brute-force hull on at least 500 random **integer** point sets that deliberately
include duplicates and collinear runs. Report mismatches.

**B2.** *(6)* Implement **both** conventions — `cross <= 0` (vertices only) and `cross < 0` (all
boundary points).

Report both hulls for $(0,0), (1,0), (2,0), (3,0), (1,1)$, and give one application that wants each.

**B3.** *(4)* Run the `< 0` version on five **collinear** points. Report exactly what it returns.

Explain the failure, and give the special case needed to fix it.

**B4.** *(4)* Prove the scan is $\Theta(n)$ after sorting.

Your argument must name what is pushed and what is popped, and why the total is linear. **This is the
fifth amortised argument of the course** — name the other four.

---

## Part C — Closest Pair (18 points)

**C1.** *(6)* Brute-force closest pair, and the divide-and-conquer version.

Verify they agree on at least 500 random point sets. Report mismatches.

**C2.** *(6)* Time both for $n \in \{1000, 2000, 4000, 8000\}$. Report the times, the doubling ratios,
and the speedup.

Name the complexity class each doubling ratio indicates.

**C3.** *(6)* The strip step compares each point with only the next few in $y$ order.

- **(a)** *(4)* State the constant, and **justify it** by a packing argument — how many points can a
  $d \times 2d$ rectangle hold if no two are closer than $d$?
- **(b)** *(2)* What would the complexity be without that bound?

---

## Part D — Floating Point (20 points)

**This part is the reason Parts A–C specified integers.**

**D1.** *(6)* Construct collinear triples in `float`: pick $A$, a direction $(dx, dy)$, and two
multiples $t_1 < t_2$ along it, all drawn from `random.uniform`.

Over at least 100,000 such triples, report how many have a **non-zero** cross product.

**D2.** *(6)* For at least 20,000 of the same triples, compare the **sign** of the float cross product
against the sign computed with `fractions.Fraction`.

Report the number of disagreements.

**D3.** *(8)* **Does it change an answer?**

Generate random points, then add points constructed to lie on segments *between* existing points.
Compute the convex hull twice — once in `float`, once with `Fraction` — and compare the **number of
vertices**.

Over at least 1,000 point sets, report how many disagree. Then answer:

- **(a)** *(3)* Why does adding points on segments make this worse?
- **(b)** *(3)* Someone proposes `abs(cross) < 1e-9` as a fix. **Give a concrete reason this is worse
  than doing nothing**, in terms of a property the comparison must have.
- **(c)** *(2)* State the two things you would actually do.

---

## Part E — Spatial Structures (20 points)

**E1.** *(6)* A **segment tree** over an integer array supporting range `min` and point update.

Verify against direct recomputation on at least 300 arrays with at least 30 mixed operations each.

**E2.** *(4)* Time 2,000 range-min queries by `min(a[l:r])` against your segment tree for
$n \in \{10^4, 5\times10^4, 2\times10^5\}$. Report the speedup.

Then state what a **prefix-sum array** does better, and the two things it cannot do at all.

**E3.** *(10)* A **k-d tree** with nearest-neighbour search, instrumented to count nodes visited.

- **(a)** *(4)* Verify against brute force on at least 300 queries in 2-D.
- **(b)** *(6)* For $n = 8192$ and dimensions $\{2, 4, 8, 16, 32\}$, report the **mean nodes visited**,
  that as a percentage of $n$, and the time for both methods.

  State the dimension at which the tree stops paying, and explain **why the pruning test stops
  firing**.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 20 | The cross product, and the degenerate cases |
| B | 22 | Convex hull, both conventions, and the amortised bound |
| C | 18 | Closest pair, and the packing constant |
| D | 20 | Why floating point breaks geometry |
| E | 20 | Segment trees, k-d trees, and the curse of dimensionality |
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

**C2:**

| $n$ | brute force | divide and conquer | speedup |
| --- | --- | --- | --- |
| 1,000 | 148.1 ms | 3.5 ms | 42× |
| 2,000 | 605.9 ms | 7.4 ms | 82× |
| 4,000 | 2,377.1 ms | 17.0 ms | 140× |
| 8,000 | 9,544.9 ms | 41.3 ms | **231×** |

**D1 / D2 / D3:**

| measurement | result |
| --- | --- |
| collinear triples with non-zero cross product | **130,443 of 200,000** (65.2%) |
| float signs differing from exact | **18,190 of 50,000** (36.4%) |
| **point sets whose float hull has a different vertex count** | **573 of 3,000** (**19.1%**) |

**E2:**

| $n$ | `min(a[l:r])` | segment tree | speedup |
| --- | --- | --- | --- |
| 10,000 | 97.5 ms | 4.3 ms | 22× |
| 50,000 | 501.1 ms | 5.6 ms | 90× |
| 200,000 | 2,740.4 ms | 8.3 ms | **332×** |

**E3(b)** — $n = 8192$:

| dim | nodes visited | % of $n$ | brute force | k-d tree |
| --- | --- | --- | --- | --- |
| 2 | 20 | 0.2% | 6.75 ms | 0.02 ms |
| 4 | 62 | 0.8% | 8.73 ms | 0.09 ms |
| 8 | 787 | 9.6% | 13.61 ms | 1.78 ms |
| **16** | **8,071** | **98.5%** | 22.49 ms | **25.06 ms** |
| 32 | 8,192 | 100.0% | 37.72 ms | 42.94 ms |

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
