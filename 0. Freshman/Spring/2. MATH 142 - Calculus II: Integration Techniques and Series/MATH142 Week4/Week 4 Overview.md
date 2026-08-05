# MATH 142 · Calculus II
## Week 4 · Overview
### Applications: Volumes of Revolution, Arc Length, Surface Area

---

**Topic:** the slice-approximate-sum-limit pattern, applied three more times
**Reading:** Stewart §6.2–6.3, §8.1–8.2 | Apostol Ch. 2 §2.11–2.13
**Assessment this week:** PS 4, Lab 4, **Quiz 04** *(Monday — covers Week 3)*

---

## One Idea, Three Applications

Week 0, Lecture 3 gave the pattern behind every application of the integral:

> **Slice. Approximate. Sum. Take the limit.**

This week runs it three more times. **There is no new theory** — the whole week is that one pattern applied to three geometric quantities, and the only real work is deciding *how* to slice.

| Quantity | Slice into | Each piece is approximately |
|---|---|---|
| **Volume** (discs/washers) | slabs ⊥ to the axis | a disc or an annulus |
| **Volume** (shells) | slabs ∥ to the axis | a thin cylindrical shell |
| **Arc length** | short pieces of curve | a straight segment |
| **Surface area** | bands of surface | a frustum of a cone |

> **Do not memorise four formulas.** There are perhaps twenty in Chapter 6 of Stewart and one idea.
> A student holding the pattern can rederive any of them in a minute; a student holding the formulas
> is helpless the moment a problem is stated slightly differently — for example, rotating about
> $y=-1$ instead of the $x$-axis.

---

## The Three Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Monday | Volumes by Discs and Washers | Slice perpendicular to the axis |
| **Lecture 2** | Tuesday | Volumes by Cylindrical Shells | Slice parallel to it — and when that is the only sane choice |
| **Lecture 3** | Wednesday | Arc Length and Surface Area | Where closed forms run out |

---

## Where This Week Meets Week 3

Lecture 3 produces integrals like

$$L = \int_a^b\sqrt{1+\big(f'(x)\big)^2}\,dx$$

and the square root of a sum of squares is **almost never** elementary. Three examples:

| Curve | Arc length on the stated interval | |
|---|---|---|
| $y = x^{3/2}$ on $[0,1]$ | $\dfrac{13\sqrt{13}-8}{27} \approx 1.4397$ | elementary |
| $y = x^{2}$ on $[0,1]$ | $\dfrac{\sqrt5}{2}+\dfrac{\operatorname{arcsinh}2}{4}\approx 1.4789$ | elementary, but needs a trig substitution |
| $y = \sin x$ on $[0,\pi]$ | $\approx 3.8202$ | **not elementary** |

*(all verified)*

**The third is an elliptic integral** — the same object that gives the circumference of an ellipse, which is why there is no simple formula for it despite two thousand years of trying. Week 0's opening fact, arriving in a new costume: *most integrals you can write down cannot be evaluated in closed form.*

**And Week 3 supplies the other half.** Lab 4's centrepiece is a solid of revolution with

$$\text{finite volume} \qquad\text{and}\qquad \textbf{infinite surface area}$$

Both facts are improper integrals, and deciding them uses the comparison test you learned last week.

---

## Gabriel's Horn — A Preview

Rotate $y = \dfrac1x$ for $x\ge1$ about the $x$-axis.

$$V = \pi\int_1^\infty\frac{dx}{x^2} = \pi \qquad\qquad S = 2\pi\int_1^\infty\frac1x\sqrt{1+\frac{1}{x^4}}\,dx = \infty$$

*(both verified)*

**The volume converges by the $p$-test with $p=2$; the surface area diverges by comparison with $p=1$.** They differ because the surface integral carries an extra factor that never drops below 1, and $\frac1x$ is on the wrong side of the convergence threshold.

This is the **painter's paradox**: the horn holds exactly $\pi$ cubic units of paint, yet no finite amount of paint will cover its inside surface. Lab 4 asks you to resolve the apparent contradiction — and it does have a resolution.

---

## What Will Be Hard

**Choosing discs or shells.** Both always work in principle. One of them usually produces an integral you can evaluate and the other one you cannot. **The decision costs thirty seconds and saves twenty minutes**, and Lecture 2 gives the rule.

**Rotating about a line that is not an axis.** The radius becomes $|f(x) - c|$ rather than $f(x)$. Most lost marks in this week's material trace to a radius written down without a picture.

**Setting up rather than evaluating.** Several problems this week ask you to *set up* an integral and state whether it can be evaluated in closed form — because after Week 3 you know how to answer that, and because in practice setting up correctly is the part that matters.

---

## This Week's Work

1. **Quiz 04** — Monday, 15 minutes, **covers Week 3** (improper integrals, comparison tests)
2. **PS 4** — released Wednesday, due Wednesday of Week 5
3. **Lab 4** — Gabriel's Horn, and measuring how a polygon converges to a curve

---

## Midterm 1

**Midterm 1 is next week (Week 5) and covers Weeks 0–4** — this week completes its syllabus.

75 minutes, one handwritten sheet, no calculator. A revision guide will be posted with the Week 5 materials, but the useful preparation starts now: **rework PS 0–4 from a blank page**, under time.

---

*Next: Monday — Volumes by Discs and Washers*
