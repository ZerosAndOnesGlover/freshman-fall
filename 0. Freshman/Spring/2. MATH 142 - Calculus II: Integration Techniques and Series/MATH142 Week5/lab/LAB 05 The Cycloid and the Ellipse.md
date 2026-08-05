# MATH 142 · Calculus II
## Lab 05: The Cycloid and the Ellipse
### Week 5 Lab Session

---

**Duration:** 2 hours
**Format:** Individual or pairs (pairs submit separate reports)
**Graded on:** completion + correctness — **100 points**
**Tools required:** Python 3 with `sympy` and `mpmath`

---

## Overview

Two curves, described parametrically in almost the same amount of ink:

$$\textbf{Cycloid: } x=a(t-\sin t),\ y=a(1-\cos t) \qquad\qquad \textbf{Ellipse: } x=a\cos t,\ y=b\sin t$$

**One has an arc length of exactly $8a$. The other's perimeter cannot be written in closed form at all.**

The cycloid is the stranger object — it cannot even be expressed as $y=f(x)$, and it was unknown before the 17th century. The ellipse is a conic section, studied since Apollonius around 200 BC, whose area is simply $\pi ab$.

**The tractable one is the one that looks harder.** This lab makes you verify both facts, and then confront the practical question that follows: if there is no formula for the ellipse's perimeter, **what do people actually use?**

---

## Part A — The Cycloid (25 pts)

**A1 (8 pts).** Compute $\left(\dfrac{dx}{dt}\right)^2+\left(\dfrac{dy}{dt}\right)^2$ and simplify it to a perfect square using a half-angle identity. Show the step.

**A2 (9 pts).** Hence find the arc length of one arch ($t\in[0,2\pi]$) **by hand**, then verify with `sympy`.

Confirm numerically for $a=1$ that your answer is exactly $8$.

**A3 (8 pts).** Find the area under one arch by hand, and verify symbolically.

State the ratio of this area to the area of the rolling circle, and comment on how simple it is.

---

## Part B — The Ellipse Has No Closed Form (20 pts)

**B1 (8 pts).** Write down the integral for the perimeter of $x=a\cos t$, $y=b\sin t$.

Ask `sympy` to evaluate it symbolically with $a\ne b$. **Report exactly what it returns**, and say what that tells you.

**B2 (6 pts).** For $a=2$, $b=1$, compute the perimeter by numerical quadrature to 15 significant figures.

Then compute it using `mpmath`'s complete elliptic integral `mp.ellipe`, via

$$P = 4a\,E(e^2), \qquad e^2 = 1-\frac{b^2}{a^2}$$

**Confirm the two agree**, and explain what `ellipe` actually is. *(It is not "the answer" — it is a name for the integral, exactly as `erf` was in Lab 0.)*

**B3 (6 pts).** Set $a=b$ in the perimeter integral and evaluate it by hand. You should get $2\pi a$.

Explain why the integral becomes elementary **only** in this case, referring to what happens to $\sqrt{a^2\sin^2t+b^2\cos^2t}$.

---

## Part C — What People Actually Use (30 pts)

Since there is no formula, engineers use approximations. Three of them:

$$P_1 = \pi(a+b) \qquad P_2 = 2\pi\sqrt{\frac{a^2+b^2}{2}} \qquad P_3 = \pi\left[3(a+b)-\sqrt{(3a+b)(a+3b)}\right]$$

The third is **Ramanujan's approximation**, published in *Modular Equations and Approximations to $\pi$* (Quarterly Journal of Mathematics, **1914**) — where it appears in the paper's final sentence, described only as "obtained empirically". **Ramanujan never explained how he found it.**

**C1 (12 pts).** Fix $a=1$. For $b = 1,\ 0.8,\ 0.5,\ 0.2,\ 0.1,\ 0.01$, tabulate the exact perimeter and the **relative error** of each of $P_1,P_2,P_3$.

**C2 (8 pts).** All three are exact at $b=1$. Why?

Then describe how each degrades as the ellipse flattens. Which is best at $b/a=0.8$? Which at $b/a=0.01$?

**C3 (10 pts).** Report the relative error of Ramanujan's formula at $b/a=0.8$ and at $b/a=0.5$.

- (a) How many correct significant figures does it give in each case?
- (b) A machining tolerance of one part in $10^5$ is typical. Over what range of $b/a$ is $P_3$ good enough? What about $P_1$?
- (c) Comment: the exact answer does not exist in closed form, yet a two-line formula is accurate to nine figures for mild ellipses. **What does this say about the practical importance of "has no closed form"?**

---

## Part D — Reflection (25 pts)

**D1 (10 pts).** The cycloid's arc length worked out because a half-angle identity turned $2a^2(1-\cos t)$ into a perfect square $4a^2\sin^2\frac t2$.

- (a) Show that the **cardioid** $r=1+\cos\theta$ has the same structure, and hence that its perimeter is exactly $8$.
- (b) Explain why the ellipse's integrand $\sqrt{a^2\sin^2t+b^2\cos^2t}$ admits no such collapse when $a\ne b$. What is structurally different?

**D2 (8 pts).** Across five labs the relationship between exact and numerical methods has varied:

| Lab | Verdict |
|---|---|
| 0 | numerics won |
| 1 | numerics worked, $6\times10^7$ times too slowly |
| 2 | numerics gave the value, not the proof |
| 3 | numerics could not answer at all |
| 4 | numerics excellent on one half, useless on the other |
| **5** | **?** |

Fill in the entry for this lab, and justify it in two or three sentences.

**D3 (7 pts).** The cycloid was studied by Galileo (who tried to find its area **by weighing metal cut-outs** and got about 3, but could not prove it), and its area was proved to be $3\pi a^2$ by Roberval in 1634. Wren found the arc length in 1658.

In two or three sentences: what does Galileo's method have in common with the numerical methods in these labs, and what does it lack?

---

## What to Submit

1. The half-angle simplification, arc length and area of the cycloid (Part A)
2. `sympy`'s response to the ellipse perimeter, and the two numerical routes (Part B)
3. The approximation error table and your answers to C2 and C3 (Part C)
4. The cardioid computation and your reflections (Part D)

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A | 25 | The cycloid, by hand and verified |
| B | 20 | Establishing there is no closed form |
| C | 30 | What is used instead, and how good it is |
| D | 25 | Why one collapses and one does not; reflection |
| **Total** | **100** | |

---

*The ellipse has no formula for its perimeter and never will. It also has an approximation good to nine figures. Both facts are true, and only one of them matters to somebody building something.*
