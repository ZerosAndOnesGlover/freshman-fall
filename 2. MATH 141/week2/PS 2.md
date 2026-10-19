---
assessment: PS 2
course: MATH 141
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-09
submitted: 2026-10-14
graded: 2026-10-16
source: "Problem Set 2.md"
---

# MATH 141 · PS 2
## Answer Sheet

**Assessment:** `Problem Set 2.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Problem 1 — The Definition  (10 points)

**Your answer:**

$f$ is **continuous at $a$** if and only if all three hold:

1. **(i)** $f(a)$ is defined;
2. **(ii)** $\displaystyle\lim_{x\to a} f(x)$ exists (as a finite real number);
3. **(iii)** $\displaystyle\lim_{x\to a} f(x) = f(a)$.

A function failing each part in turn:

- **(i)** fails: $f(x) = \dfrac1x$ at $a = 0$ — $f(0)$ is undefined.
- **(ii)** fails: $f(x) = \dfrac{|x|}{x}$ at $a = 0$ — the one-sided limits are $-1$ and $+1$, so the limit does not exist.
- **(iii)** fails: $f(x) = x$ for $x \neq 0$ with $f(0) = 5$ — the limit exists and equals $0$, but $f(0) = 5 \neq 0$.

*Marks: 10 / 10*

---

### Problem 2 — Where Is It Continuous?  (12 points)

**Your answer:**

**(a)** $\dfrac{x+1}{x^2-4} = \dfrac{x+1}{(x-2)(x+2)}$. A rational function is continuous wherever its
denominator is nonzero, so $f$ is continuous on $\boxed{(-\infty,-2)\cup(-2,2)\cup(2,\infty)}$;
it is discontinuous (infinite) at $x = \pm2$.

**(b)** $\sqrt{x-3}$ is defined where $x - 3 \ge 0$, i.e. $x \ge 3$, and the square root is continuous on
its domain, so $f$ is continuous on $\boxed{[3,\infty)}$ (right-continuous at $x = 3$).

**(c)** $\dfrac{\sin x}{x}$ is continuous wherever $x \neq 0$, i.e. on
$\boxed{(-\infty,0)\cup(0,\infty)}$; since $\lim_{x\to0}\frac{\sin x}{x} = 1$, the discontinuity at $0$
is **removable** (it can be repaired by defining the value as $1$).

*Marks: 12 / 12*

---

### Problem 3 — Choosing a Value  (10 points)

**Your answer:**

For continuity at $3$ we need $\displaystyle\lim_{x\to3} f(x) = f(3) = k$. Factor the numerator:

$$\frac{x^2-9}{x-3} = \frac{(x-3)(x+3)}{x-3} = x+3 \quad (x \neq 3),$$

so $\displaystyle\lim_{x\to3} f(x) = 3 + 3 = 6$. Hence continuity requires

$$\boxed{k = 6}.$$

*Marks: 10 / 10*

---

### Problem 4 — Classifying Discontinuities  (16 points)

**Your answer:**

| | Function | Point | Type | Reason |
|---|---|---|---|---|
| (a) | $\dfrac{x^2-4}{x-2}$ | $2$ | **Removable** | Cancels to $x+2 \to 4$; limit exists, just undefined at $2$ |
| (b) | $\dfrac{x+2}{x-2}$ | $2$ | **Infinite** | Numerator $\to 4 \neq 0$, denominator $\to 0$, so $f \to \pm\infty$ |
| (c) | $\dfrac{|x|}{x}$ | $0$ | **Jump** | One-sided limits are $-1$ and $+1$ (finite but unequal) |
| (d) | $\cos(1/x)$ | $0$ | **Essential** | Oscillates between $-1$ and $1$ with no one-sided limit |

Parts (a) and (b) are the discriminating pair: both have a denominator vanishing at the point, but the
limit distinguishes them — (a) has a removable factor in the numerator, (b) does not.

*Marks: 16 / 16*

---

### Problem 5 — Finding Every Discontinuity  (12 points)

**Your answer:**

Factor numerator and denominator:

$$f(x) = \frac{x^2-9}{x^2-3x} = \frac{(x-3)(x+3)}{x(x-3)}.$$

The function is undefined where the denominator is zero: $x = 0$ and $x = 3$.

- **At $x = 3$: removable.** The factor $(x-3)$ cancels, leaving $\dfrac{x+3}{x}$; as $x \to 3$ this
  $\to \dfrac{6}{3} = 2$. The limit exists (both sides), so the discontinuity is removable.
- **At $x = 0$: infinite.** After cancellation $f = \dfrac{x+3}{x}$; the numerator $\to 3 \neq 0$ while
  the denominator $\to 0$, so $f \to -\infty$ as $x\to0^-$ and $+\infty$ as $x\to0^+$. Infinite
  discontinuity.

Every discontinuity: $x = 3$ (removable) and $x = 0$ (infinite).

*Marks: 12 / 12*

---

### Problem 6 — The Intermediate Value Theorem  (14 points)

**Your answer:**

**(a)** Let $f(x) = x^3 - x - 2$. It is a polynomial, hence continuous on $[1,2]$. Evaluate at the endpoints:

$$f(1) = 1 - 1 - 2 = -2 < 0, \qquad f(2) = 8 - 2 - 2 = 4 > 0.$$

Since $0$ lies strictly between $f(1)$ and $f(2)$, the **IVT** guarantees a number $c \in (1,2)$ with
$f(c) = 0$ — a root.

**What the IVT tells you:** at least one root exists in $(1,2)$.
**What it does not tell you:** *where* the root is, *how many* roots there are, or how to compute one.
(Uniqueness would need $f' > 0$, which is a Week 6 result.)

**(b)** Let $g(x) = \cos x - x$, continuous on $[0,1]$. Then

$$g(0) = \cos 0 - 0 = 1 > 0, \qquad g(1) = \cos 1 - 1 \approx -0.4597 < 0.$$

Since $g$ changes sign, the IVT gives $c \in (0,1)$ with $g(c) = 0$, i.e. $\cos c = c$. So $\cos x = x$
has a solution in $[0,1]$. (Numerically $c \approx 0.739085$.)

*Marks: 14 / 14*

---

### Problem 7 — Bisection by Hand  (14 points)

**Your answer:**

Run bisection on $f(x) = x^3 - x - 2$ over $[1,2]$ ($f(1) = -2 < 0$, $f(2) = 4 > 0$):

**Step 1.** Midpoint $m = \dfrac{1+2}{2} = 1.500000$. $f(1.5) = 3.375 - 1.5 - 2 = -0.125000 < 0$,
so the root is in $[1.5, 2]$.

**Step 2.** Midpoint $m = \dfrac{1.5+2}{2} = 1.750000$. $f(1.75) = 5.359375 - 1.75 - 2 = +1.609375 > 0$,
so the root is in $[1.5, 1.75]$.

**Step 3.** Midpoint $m = \dfrac{1.5+1.75}{2} = 1.625000$. $f(1.625) = 4.291016 - 1.625 - 2 = +0.666016 > 0$,
so the root is in $[1.5, 1.625]$.

| Step | Bracket | Midpoint | $f(\text{mid})$ |
|---|---|---|---|
| 1 | $[1.000000,\,2.000000]$ | $1.500000$ | $-0.125000$ |
| 2 | $[1.500000,\,2.000000]$ | $1.750000$ | $+1.609375$ |
| 3 | $[1.500000,\,1.750000]$ | $1.625000$ | $+0.666016$ |

**Final bracket:** $\boxed{[1.5,\;1.625]}$ (with the root between $1.5$ and $1.625$).

*Marks: 14 / 14*

---

### Problem 8 — Why It Is Deep  (12 points)

**Your answer:**

The IVT fails over $\mathbb{Q}$. Consider $f(x) = x^2 - 2$, viewed as a function on the **rationals only**,
with domain restricted to $\mathbb{Q}$ and the interval $[1,2] \cap \mathbb{Q}$:

- $f$ is continuous (polynomials are continuous everywhere);
- $f(1) = -1 < 0 < 2 = f(2)$, so the sign change hypothesis holds.

If the IVT held over $\mathbb{Q}$, there would be a **rational** $c \in (1,2)$ with $c^2 - 2 = 0$, i.e.
$c = \sqrt2$. But $\sqrt2$ is irrational — there is **no** such rational $c$. So every hypothesis holds
yet the conclusion fails: the IVT is genuinely false over $\mathbb{Q}$.

What rescues it over $\mathbb{R}$ is **completeness** — the real line has no "gaps". Formally this is the
**least-upper-bound axiom**: every nonempty set of reals bounded above has a least upper bound. It is
completeness that guarantees the real $c$ found by the IVT actually exists. This is why the theorem needs
a proof and not just a picture: the same picture would persuade you the theorem is true over
$\mathbb{Q}$, where it is not.

*Marks: 12 / 12*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-16 |

**Feedback:**
All 8 problems correct and fully justified.

- **P1:** Three-part definition stated exactly; one valid example given for each failing part.
- **P2:** Domains correct for all three, with the right-continuity note at $x=3$ and the removable
  classification for $\sin x/x$.
- **P3:** Limit computed by factoring, $k=6$.
- **P4:** All four classified correctly with reasons; the removable/infinite pair distinguished as the
  rubric intends.
- **P5:** Both discontinuities found and classified (removable at $3$, infinite at $0$).
- **P6:** IVT hypotheses checked (polynomial/continuous, sign change), conclusion stated, and the
  "tells/does not tell" distinction drawn. Part (b) uses $g=\cos x - x$ correctly.
- **P7:** Three bisection steps tabulated with correct brackets, midpoints and $f(\text{mid})$; final
  bracket $[1.5,1.625]$.
- **P8:** Correct counterexample over $\mathbb{Q}$, and the rescue named as completeness / least upper
  bound.

No errors. Full marks.
