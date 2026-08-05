# MATH 142 · Calculus II
## Week 5 · Overview
### Parametric Curves; Polar Coordinates — and **Midterm 1**

---

**Topic:** two ways of describing curves that are not graphs of functions
**Reading:** Stewart §10.1–10.4 | Apostol Ch. 2 §2.14
**Assessment this week:** PS 5, Lab 5, **Quiz 05** *(Monday — covers Week 4)*, and **MIDTERM 1**

---

## ⚠ Midterm 1

**Midterm 1 is this week.** 75 minutes, covering **Weeks 0–4**, one handwritten sheet (one side), no calculator.

**A full revision guide is in this week's `resources/` folder.** Read it now, not the night before — it contains a topic checklist, the seven errors that cost the most marks, and a worked sample paper.

**This week's new material (parametric and polar) is *not* on Midterm 1.** It is examined on Midterm 2.

---

## Why Curves Need a Better Description

Everything so far has been $y=f(x)$: for each $x$, one $y$. That is a serious restriction, and you have already run into it twice.

- **Week 4, PS 4 D2(d):** rotating $y=\sin x$ on $[0,\pi]$ about the $y$-axis was awkward by discs because $\sin$ is not one-to-one there — a horizontal line meets the curve twice.
- **A circle is not a function at all.** $x^2+y^2=1$ needs two half-functions, and they meet badly at $x=\pm1$ where the tangent is vertical and $\tfrac{dy}{dx}$ does not exist.

**Neither of these is a defect of the curve. Both are defects of the description.** This week gives two better ones.

| Description | Idea | Good for |
|---|---|---|
| **Parametric** | $x=x(t)$, $y=y(t)$ — a point moving in time | motion, curves that cross themselves, anything traced |
| **Polar** | $r = f(\theta)$ — distance as a function of direction | circles, spirals, anything with rotational symmetry |

**A circle is horrible as $y=\pm\sqrt{1-x^2}$, easy as $(\cos t,\sin t)$, and trivial as $r=1$.** Choosing the description is most of the work.

---

## The Three Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Monday | Parametric Curves | A curve is a path, not a graph |
| **Lecture 2** | Tuesday | Calculus with Parametric Curves | Slopes, areas, arc lengths — all via the chain rule |
| **Lecture 3** | Wednesday | Polar Coordinates | Area is $\tfrac12\int r^2d\theta$, and why the $\tfrac12$ |

---

## The Week's Best Result

The **cycloid** is the curve traced by a point on the rim of a rolling wheel:

$$x = a(t-\sin t), \qquad y = a(1-\cos t)$$

It looks far worse than a circle or a parabola. **Its arc length over one arch is exactly**

$$L = 8a$$

*(verified)* — no $\pi$, no square roots, no special functions. **Eight times the radius**, exactly.

Meanwhile the **ellipse**, which looks much simpler,

$$x = a\cos t,\qquad y = b\sin t$$

has a perimeter with **no elementary closed form at all** — it is an elliptic integral, the same obstruction you met in Week 4 with $y=\sin x$.

> **The curve that looks harder has the clean answer; the curve that looks easier does not.**
> This is Week 4's C5 lesson again: *appearance is not evidence.* Lab 5 makes you compute both.

The cycloid's arc length comes out cleanly because a half-angle identity collapses the square root:

$$\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2 = 2a^2(1-\cos t) = 4a^2\sin^2\frac t2$$

*(verified)* — and $\sqrt{4a^2\sin^2\tfrac t2} = 2a\sin\tfrac t2$ is elementary. **The same trick makes the cardioid's arc length exactly 8.** *(Also verified.)*

---

## What Will Be Hard

**The $\tfrac12$ in the polar area formula.** $A = \tfrac12\int r^2\,d\theta$ is *not* the same as $\int y\,dx$ with a change of variable — the slices are **circular sectors**, not rectangles, and the $\tfrac12$ comes from the sector's area $\tfrac12r^2\Delta\theta$. Lecture 3 derives it; memorising it without the derivation guarantees you will misapply it.

**Limits of integration in polar.** Finding *which* $\theta$ traces the piece you want is harder than any integral in the problem. A rose curve $r=\cos2\theta$ traces four petals as $\theta$ runs over $[0,2\pi]$, and integrating over the whole range when you wanted one petal gives four times too much — or zero, if the sign flips.

**Vertical tangents.** In parametric form, $\tfrac{dy}{dx} = \tfrac{dy/dt}{dx/dt}$ is undefined where $\tfrac{dx}{dt}=0$. That is not a failure; it is the parametrisation correctly reporting a vertical tangent — the thing $y=f(x)$ could not express.

---

## This Week's Work

1. **Quiz 05** — Monday, 15 minutes, **covers Week 4** (volumes, arc length, surface area)
2. **MIDTERM 1** — covering Weeks 0–4. See the revision guide in `resources/`
3. **PS 5** — released Wednesday, due Wednesday of Week 6
4. **Lab 5** — the cycloid and the ellipse: one has a closed form, one cannot

---

## Looking Ahead

Week 5 closes the first half of the course. **Weeks 0–5 were about evaluation and geometry**; from Week 6 the subject changes entirely.

> **Week 6 begins sequences, and from there to the end the questions are almost all of the form
> "does this converge?"** The syllabus warned you that the difficulty inverts — the computations get
> easier and the reasoning gets much harder. Expect to feel competent this week and lost in two.
> That is the course working as designed.

---

*Next: Monday — Parametric Curves*
