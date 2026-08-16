# CS 102 · Computer Science II
## Lecture 34: Geometric Primitives and the Convex Hull

**Date:** Monday 29 March 2027 · 09:00–09:50 · Week 11

---

## 1. One Operation

Computational geometry looks like it needs trigonometry, angles and distances. Almost none of it does.
**Nearly every algorithm in this week rests on one arithmetic expression:**

$$\mathrm{cross}(O, A, B) = (A_x - O_x)(B_y - O_y) - (A_y - O_y)(B_x - O_x)$$

This is the $z$-component of the 3-D cross product of $\vec{OA}$ and $\vec{OB}$, and its **sign** tells
you the turn direction:

| sign | meaning |
| --- | --- |
| $> 0$ | $B$ is to the **left** of the directed line $O \to A$ — a counter-clockwise turn |
| $< 0$ | $B$ is to the **right** — a clockwise turn |
| $= 0$ | $O$, $A$, $B$ are **collinear** |

Its magnitude is twice the area of triangle $OAB$, which gives polygon area for free.

**No angles, no square roots, no division.** With integer inputs the whole thing is exact integer
arithmetic — a point §4 will make in the strongest possible terms.

```python
def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
```

Everything below is this function called in a loop.

---

## 2. The Convex Hull

> The **convex hull** of a point set is the smallest convex polygon containing every point.

Physically: hammer a nail into every point and stretch a rubber band around them.

It is the most-used structure in the field — it gives the diameter of a point set, bounds collision
volumes, is the first step in many clustering and outlier methods, and reduces "smallest enclosing X"
problems from $n$ points to the hull's vertices, typically far fewer.

### Andrew's monotone chain

The classical algorithm is **Graham scan**, which sorts by polar angle about a pivot. Sorting by angle
requires care with ties and with `atan2`'s precision. **Andrew's monotone chain** avoids all of it by
sorting by coordinate:

```python
def hull(pts):
    P = sorted(set(pts))                        # lexicographic; duplicates removed
    if len(P) <= 2: return P
    def half(P):
        h = []
        for p in P:
            while len(h) >= 2 and cross(h[-2], h[-1], p) <= 0:
                h.pop()                         # h[-1] is not a hull vertex
            h.append(p)
        return h
    lower = half(P)
    upper = half(P[::-1])
    return lower[:-1] + upper[:-1]              # drop the shared endpoints
```

$\Theta(n\log n)$, dominated by the sort; the scan is $\Theta(n)$ because **each point is pushed once
and popped at most once** — the fifth amortised argument of the course, after `BUILD-HEAP`,
union-find, KMP and Kasai.

*(Verified against a brute-force hull on 1,000 random integer point sets, deliberately including many
collinear and duplicate points. **0 mismatches.**)*

---

## 3. The Degenerate Cases Are the Algorithm

A convex hull on random points in general position is easy. **The work is entirely in the degenerate
cases**, and they are not exotic — axis-aligned data, grid coordinates and duplicated points are the
norm, not the exception.

### Collinear points: `<= 0` or `< 0`?

Take $(0,0), (1,0), (2,0), (3,0), (1,1)$ — four points on a line plus one above.

| test | hull returned |
| --- | --- |
| `cross(...) <= 0` | $(0,0), (3,0), (1,1)$ — **3 vertices** |
| `cross(...) < 0` | $(0,0), (1,0), (2,0), (3,0), (1,1)$ — **5 vertices** |

*(Verified.)*

**Both are defensible and they answer different questions.** `<=` returns the *vertices* of the hull;
`<` returns every point *on the boundary*. Rendering a polygon wants the first; testing whether a point
lies on the hull wants the second.

**Neither is a bug, and shipping one when you needed the other is.**

### And the lax version breaks on fully degenerate input

With all points collinear — $(0,0)$ through $(4,0)$:

| test | result |
| --- | --- |
| `<= 0` | $(0,0), (4,0)$ — correct: the hull is a segment |
| `< 0` | $(0,0), (1,0), (2,0), (3,0), (4,0), (3,0), (2,0), (1,0)$ — **every interior point twice** |

*(Verified.)*

The lower and upper chains each retain all five points, and concatenating them duplicates the interior.
**A special case for "all points collinear" is required if you keep boundary points**, and the failure
is silent — you get a polygon with repeated vertices that most downstream code will accept.

---

## 4. Floating Point Will Destroy This

The orientation test is a **sign** test, and a sign test on a value near zero is exactly where floating
point fails. Geometry is the part of this course where that stops being a footnote.

Construct triples that are collinear **by construction** — pick $A$, a direction, and two multiples
along it — and evaluate the cross product in `float`:

| measurement | result |
| --- | --- |
| triples with a **non-zero** cross product | **130,443 of 200,000** — 65.2% |
| float **signs** differing from exact rational arithmetic | **18,190 of 50,000** — 36.4% |

*(Verified against `fractions.Fraction`.)*

**A test for exact collinearity essentially never fires**, and a third of the time the computed sign is
not the true sign.

### It changes the answer

Take random points, then add points constructed to lie *on segments between them* — the situation any
real dataset with shared edges produces. Compute the hull twice: once in `float`, once in exact
rational arithmetic.

> **573 of 3,000 point sets — 19.1% — gave a float hull with a different number of vertices than the
> exact hull.**

*(Verified.)*

**One point set in five produces a wrong convex hull.** Not a slightly different one; a different
polygon.

### What to do about it

1. **Use integers when you can.** Grid data, screen coordinates and fixed-point measurements are exact,
   and the cross product of integers is an integer. **This is the single most effective thing in this
   lecture.** PS 11 uses integer coordinates throughout for exactly this reason.
2. **Use exact predicates when you cannot.** Libraries such as CGAL implement *adaptive* predicates —
   fast floating-point arithmetic first, escalating to exact arithmetic only when the result is too
   close to zero to trust.
3. **Do not "fix" it with an epsilon.** `abs(cross) < 1e-9` makes the predicate non-transitive: three
   points can be pairwise "collinear" and not collinear as a triple. Sorting with an inconsistent
   comparator is undefined behaviour, and the resulting crashes are famously hard to reproduce.

> **This is the only place in the course where the right answer is "use a library".** Convex hull is
> ten lines and correct geometric predicates are a research career. Know what the ten lines do, and
> know why you should not ship them against untrusted float input.

---

## 5. What the Hull Gives You

| problem | via the hull |
| --- | --- |
| **diameter** of a point set | rotating calipers over the hull, $\Theta(h)$ after the hull |
| smallest enclosing rectangle | one hull edge is flush with an optimal rectangle |
| point in convex polygon | binary search on hull vertices, $O(\log h)$ |
| collision detection | convex bounding volumes intersect cheaply |
| linear programming in 2-D | the optimum is at a hull vertex |

The last row is worth stating plainly: **maximising a linear function over a point set means checking
hull vertices only**, which is often a handful out of millions.

---

## 6. What to Do

- Read CLRS §33.1 (segment properties) and §33.3 (convex hull). CLRS gives Graham scan and Jarvis
  march; monotone chain is Problem 33-2 and is what you should implement.
- **PS 11** implements the hull with **integer** coordinates, handles both collinear conventions, and
  reproduces §4's float measurements.
- **Quiz 11 covers Week 10** — string matching. Not this material.
- **PROJECT 2 is due Friday of Week 12.** If Part 1 is not done, this week is the last comfortable
  moment.
- Next lecture: segment intersection and the closest pair.

---

*CS 102 · Week 11 · Lecture 34 · © CSE Department*
