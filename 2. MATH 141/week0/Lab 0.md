---
assessment: Lab 0
course: MATH 141
component: Labs
possible: 100
score: 94
status: graded
started: 2026-09-25
submitted: 2026-09-27
graded: 2026-09-27
source: "LAB 00 Graphical Exploration.md"
---

# MATH 141 · Lab 0

## Answer Sheet

**Assessment:** `LAB 00 Graphical Exploration.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Part 1 — Function Families (Q1–Q5)

**Graph evidence:** _[screenshot or Desmos link for Part 1 — insert here]_

**Your answer:**

#### Activity 1.1: Power Functions

**Q1.** The even powers (y = x² and y = x⁴) are symmetric about the **y-axis**: the left half is the
mirror image of the right half, so f(−x) = f(x). The odd powers (y = x, y = x³ and y = x⁵) are
symmetric about the **origin**: the third quadrant is the mirror image of the first quadrant, so
f(−x) = −f(x).

The reason is the sign of the exponent. A negative number raised to an even power comes out
positive, so f(−x) = f(x); raised to an odd power it comes out negative, the opposite sign, so
f(−x) = −f(x). On the graph, the even powers are U-shaped bowls opening upward that never dip
below the x-axis, while the odd powers are S-shaped curves that pass through the origin and change
sign as x moves through 0.

**Q2.** All five graphs pass through **(0, 0)** and **(1, 1)**.

- At x = 0: for any positive integer n, 0ⁿ = 0, so y = xⁿ gives y = 0. The graph of every power
  function therefore goes through the origin.
- At x = 1: 1ⁿ = 1 for every n, so y = 1. The point (1, 1) is on every one of them.

This is why the five curves are pinched together at those two points in the Desmos window: no
matter how large the exponent grows, the curve is forced through them. (At x = −1 the values
split: the even powers give 1 and the odd powers give −1, which is exactly the symmetry in Q1.)

**Q3.** For 0 < x < 1 the largest of the five is **y = x** (the exponent 1), and the order runs
x > x² > x³ > x⁴ > x⁵. For x > 1 the largest is **y = x⁵**, and the order reverses:
x⁵ > x⁴ > x³ > x² > x.

The order flips at x = 1 because a number strictly between 0 and 1 behaves in the opposite way
from a number greater than 1. If 0 < x < 1, each extra factor of x pulls the product down
(x · x < x since we multiply by something less than 1), so bigger exponents give smaller values. If
x > 1, each extra factor pulls the product up (x · x > x), so bigger exponents give larger values.
At x = 1 neither effect applies: 1ⁿ = 1 for every n, so all five curves meet at the single point
(1, 1) and the ordering is a tie.

#### Activity 1.2: Exponential vs Polynomial Growth

**Q4.** The two curves cross twice in the window. Clicking the intersection points in Desmos gives
approximately **(1.37, 2.59)** and **(9.94, 981.97)**. The first crossing is where x³ overtakes 2ˣ;
the second is where 2ˣ overtakes x³ for good. **Beyond x ≈ 9.94 (and certainly for all x > 10),
2ˣ stays above x³.** The REPL confirms it:

```
>>> 2**9
512
>>> 9**3
729
>>> 2**10
1024
>>> 10**3
1000
```

At x = 9, 2ˣ = 512 is still below 9³ = 729, but at x = 10, 2ˣ = 1024 has overtaken 10³ = 1000 —
so the switch happens between 9 and 10, which brackets the crossing at x ≈ 9.94. Each time x
grows by 1, 2ˣ doubles, while x³ is multiplied by ((x+1)/x)³, a factor of only about 1.33 near
x = 10. Doubling eventually beats a factor of 1.33, and once 2ˣ is ahead it accelerates away.

**Q5.** **√x grows faster than ln x** for large x:

| x | ln(x) | √x |
|---|-------|-----|
| 100 | 4.6052 | 10 |
| 10000 | 9.2103 | 100 |

Multiplying x by 100 took √x up by a factor of 10, but only doubled ln x (4.6052 → 9.2103). The
reason is the type of growth: multiplying x by **e** ≈ 2.72 adds exactly 1 to ln x, no matter how
big x already is, whereas raising x to a fixed power multiplies √x by a constant factor (doubling
√x means quadrupling x). So logarithms grow extraordinarily slowly — the argument has to grow
faster than any fixed power of itself before ln x moves noticeably — and √x, though slow, outruns
them both. This is the first hint of Q4: a constant factor per step (2ˣ doubling) eventually beats
a power of x, because a power of x only grows by a factor that itself shrinks as x gets bigger.

_Marks: 28 / 30_

---

### Part 2 — Transformations (Q6–Q8)

**Graph evidence:** _[screenshot or Desmos link for Part 2 — insert here]_

**Your answer:**

#### Activity 2.1: Sliders

**Q6.** With a = 1 and k = 0, moving h to 2 turns y = x² into y = (x − 2)², and the parabola moves
**2 units to the right**, from vertex (0, 0) to vertex (2, 0). Dragging h from 0 to 2 slides the
whole curve right without changing its shape, because the coefficient of x² is still 1.

Subtracting 2 inside the brackets moves the graph *right* because the x that makes the new
brackets vanish is x = 2: x − 2 = 0 when x = 2. The old vertex sat where the brackets were zero,
i.e. at x = 0; now the brackets are zero at x = 2, so the "bottom of the bowl" — the point where
y = 0 — is at x = 2. Every point of the old curve is dragged along by the same amount, so the
whole parabola lands 2 to the right. (The rule to remember: **inside the brackets, subtracting
shifts right; adding shifts left.** Outside the brackets, as in k, it moves the graph up or down.)

**Q7.** For y = 3(x − 4)² + 1, comparing with y = a(x − h)² + k gives a = 3, h = 4, k = 1, so the
**vertex is (4, 1)**.

The transformations that turn y = x² into y = 3(x − 4)² + 1, in the order I applied them:

1. **Vertical stretch by a factor of 3** (multiply y by 3) — every y-value triples, so the
   parabola becomes 3 times taller and narrower. Set a = 3 in the Desmos slider to check: the
   curve is exactly three times as steep as y = x².
2. **Shift 4 units right** (replace x by x − 4), moving the vertex from (0, 0) to (4, 0).
   Set h = 4 to check.
3. **Shift 1 unit up** (add 1), moving the vertex from (4, 0) to (4, 1). Set k = 1 to check.

#### Activity 2.2: Absolute Value

**Q8.** The parts of y = x² − 4 that lie **on or above the x-axis stay exactly the same**; the part
**below the x-axis is reflected up across it**.

The unchanged parts are the two outer arms, where x² − 4 ≥ 0, that is |x| ≥ 2, i.e. x ≤ −2 and
x ≥ 2. The reflected part is the dip in the middle, between the intercepts x = −2 and x = 2, where
x² − 4 < 0 (for instance at x = 0 the original y = −4).

The reason is the definition of absolute value: |u| = u when u ≥ 0 and |u| = −u when u < 0. So
| x² − 4 | simply throws away the sign of the output — it keeps positive y-values as they are and
flips negative y-values to their mirror images, i.e. it reflects the negative part across y = 0
while leaving the positive part untouched. Graphically the original curve dips to (0, −4) between
its two roots; the absolute-value version folds that dip up to (0, 4), giving a W shape with two
sharp corners (cusps) at the roots x = ±2, where the original curve crosses the x-axis.

_Marks: 23 / 25_

---

### Part 3 — Average Rate of Change and the Approach to Calculus (Q9–Q12)

**Graph evidence:** _[screenshot or Desmos link for Part 3 — insert here]_

**Your answer:**

#### Activity 3.1: Secant Lines for f(x) = x² at x = 1

**Q9.** With f(x) = x², f(1) = 1, and f(1 + h) = (1 + h)². The completed table (values rounded to
four decimal places) is:

| $h$ | $f(1+h)$ | $\dfrac{f(1+h)-f(1)}{h}$ |
|-----|----------|--------------------------|
| $1$ | $4$ | $3.0000$ |
| $0.5$ | $2.25$ | $2.5000$ |
| $0.1$ | $1.21$ | $2.1000$ |
| $0.01$ | $1.0201$ | $2.0100$ |
| $0.001$ | $1.0020$ | $2.0010$ |

The REPL lines I typed, changing h and repeating with the up arrow:

```
>>> h = 1
>>> (1 + h)**2
4.0
>>> ((1 + h)**2 - 1) / h
3.0
>>> h = 0.5
>>> (1 + h)**2
2.25
>>> ((1 + h)**2 - 1) / h
2.5
>>> h = 0.1
>>> (1 + h)**2
1.2100000000000002
>>> ((1 + h)**2 - 1) / h
2.100000000000002
>>> h = 0.01
>>> (1 + h)**2
1.0201
>>> ((1 + h)**2 - 1) / h
2.0100000000000007
>>> h = 0.001
>>> (1 + h)**2
1.0020009999999997
>>> ((1 + h)**2 - 1) / h
2.0009999999996975
```

The trailing `…0000000002` digits are just the computer's rounding, as CS 101 explains: 1.1 cannot
be stored exactly in binary, so (1 + h)² comes out as 1.2100000000000002 instead of 1.21. Rounded
to four decimal places the table is exact.

**Q10.** The slope approaches **2**.

Hand working — expand and simplify until no h is left in the denominator:

$$
\dfrac{(1+h)^2 - 1}{h}
$$

**Step 1.** Expand the square with $(a+b)^2 = a^2 + 2ab + b^2$:

$$
(1+h)^2 = 1^2 + 2(1)(h) + h^2 = 1 + 2h + h^2
$$

**Step 2.** Put everything over the common denominator h:

$$
\dfrac{(1+h)^2 - 1}{h} = \dfrac{1 + 2h + h^2 - 1}{h} = \dfrac{2h + h^2}{h}
$$

**Step 3.** Every term in the numerator contains h, so factor h out:

$$
\dfrac{h(2 + h)}{h}
$$

**Step 4.** Cancel h against h (valid for h ≠ 0); no h is left in the denominator:

$$
2 + h
$$

**Step 5.** Now put h = 0:

$$
2 + 0 = 2
$$

This proves the slope of the secant line tends to **2** as h → 0, exactly the pattern the table
shows: 3, 2.5, 2.1, 2.01, 2.001 — each time h is cut by 10, the slope moves one decimal place
closer to 2.

**Q11.** As h → 0, the second point (1 + h, f(1 + h)) slides along the curve towards (1, f(1)) =
(1, 1) and lands on it, so the secant line becomes the **tangent line** to y = x² at x = 1: the
line of slope 2 through the point (1, 1), i.e. y = 2(x − 1) + 1 = 2x − 1. The chord stops being a
line cutting across the curve and becomes the line that just touches it there, and its slope 2 is
what we will call the derivative of x² at x = 1.

#### Activity 3.2: The Same Idea for g(x) = x³ at x = 2

**Q12.** With g(x) = x³, g(2) = 8, and g(2 + h) = (2 + h)³. The REPL:

```
>>> h = 0.5
>>> (2 + h)**3
15.625
>>> ((2 + h)**3 - 8) / h
15.25
>>> h = 0.1
>>> (2 + h)**3
9.261000000000001
>>> ((2 + h)**3 - 8) / h
12.61000000000001
>>> h = 0.01
>>> (2 + h)**3
8.120600999999997
>>> ((2 + h)**3 - 8) / h
12.060099999999707
```

| $h$ | $g(2+h)$ | $\dfrac{g(2+h)-g(2)}{h}$ |
|-----|----------|--------------------------|
| $0.5$ | $15.625$ | $15.2500$ |
| $0.1$ | $9.2610$ | $12.6100$ |
| $0.01$ | $8.1206$ | $12.0601$ |

The slopes approach **12**.

Hand working — expand (2 + h)³ with $(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3$:

$$
(2+h)^3 = 2^3 + 3(2^2)(h) + 3(2)(h^2) + h^3 = 8 + 12h + 6h^2 + h^3
$$

Subtract g(2) = 8 and divide by h:

$$
\dfrac{(2+h)^3 - 8}{h} = \dfrac{8 + 12h + 6h^2 + h^3 - 8}{h} = \dfrac{12h + 6h^2 + h^3}{h}
$$

Factor h out of the numerator:

$$
\dfrac{h(12 + 6h + h^2)}{h} = 12 + 6h + h^2
$$

No h is left in the denominator, so put h = 0:

$$
12 + 0 + 0 = 12
$$

So the slopes converge on **12**, and the tangent line to y = x³ at x = 2 is y = 12(x − 2) + 8
= 12x − 16. The procedure is identical to Q10 — only the polynomial changed — which is the point
of the lab: the limit of a difference quotient is a mechanical recipe, and Week 1 is devoted to
doing it reliably.

_Marks: 43 / 45_

---

## Grading Summary

|             |                          |
| ----------- | ------------------------ |
| **Score**   | **94 / 100**             |
| **Percent** | 94%                      |
| **Graded**  | 2026-09-27               |

**Feedback:**

All twelve questions are correct, and the reasoning behind them is the strongest part of
this submission. The marking scheme's one named failure mode — reporting what Desmos or
the REPL showed without explaining why — is not committed once in twelve answers. Q1, Q3
and Q8 each state the governing rule and then apply it; Q6 goes further and gives the
mechanism (`x − 2 = 0` happens at `x = 2`) behind the shift. Q5 and Q12 exceed the brief:
Q5 links the logarithm result forward to Q4's doubling argument, and Q12 names the
difference-quotient limit as a mechanical recipe that Week 1 will formalise.

**The written work was verified independently, not against the solutions.** All thirteen
REPL values reproduce exactly under Python 3, floating-point artefacts included
(`1.2100000000000002`, `2.0009999999996975`, `8.120600999999997`), so the transcripts are
genuine rather than reconstructed. Q4's crossings were re-derived by solving
`3·ln x = x·ln 2`: roots 1.3735 and 9.9395, giving y = 2.5909 and 981.9700 — matching the
figures reported here. The hand working for Q7, Q10 and Q12 is correct, and both tangent
lines (2x − 1 and 12x − 16) are right, though only the first is required.

**Deduction — 6 marks, for the three unfilled `Graph evidence:` placeholders** (Parts 1, 2
and 3, 2 marks each). The Lab Report requires one screenshot or Desmos link per part; all
three remain template text. Nothing else on the report checklist is missing: the Q9 table
and both REPL transcripts are complete, and the hand working is present. Attaching the
three graphs would recover the full marks.

**Two notes for the record, not charged against this score.** The Part denominators above
were set to 30/25/45 to match the session's own stated time budget and to sum to the 100 in
the frontmatter; the sheet as generated carried three `/ 100` lines, which would have
recorded 300. Separately, Lab 00 is listed as ungraded orientation in both the lab source
and the Week 0 package README, so this score should be read as calibration against the
instructor solutions rather than as credit entering the final grade.

*Graded against `LAB 00 Solutions.md` (Method ≈60% / Execution ≈40%).*
