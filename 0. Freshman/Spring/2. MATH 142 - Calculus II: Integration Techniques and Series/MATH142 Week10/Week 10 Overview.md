# MATH 142 · Calculus II
## Week 10 · Overview
### Taylor and Maclaurin Series — and **Midterm 2**

---

**Topic:** the climax of the course
**Reading:** Stewart §11.10–11.11 | Apostol Ch. 11 §11.6–11.11
**Assessment this week:** PS 10, Lab 10, **Quiz 10** *(Mon 29 Mar, 11:00 — covers Week 9)*, and **MIDTERM 2**

---

## ⚠ Midterm 2

**Midterm 2 is Wednesday 31 March, 18:00–19:15 (VNC 100).** 75 minutes, covering **Weeks 5–9**, one handwritten sheet (one side), no calculator.

**A full revision guide is in this week's `resources/` folder.** This week's new material (Taylor series) is **not** on it — that is examined on the final.

---

## The Question, Reversed

**Week 9 asked:** given a power series, where does it converge?

**Week 10 asks the question that makes it matter:**

> **Given a function $f$, is there a power series that equals it?**

If $f(x) = \sum c_n(x-a)^n$ near $a$, then differentiating $n$ times and setting $x=a$ kills every term but one, forcing

$$\boxed{c_n = \frac{f^{(n)}(a)}{n!}}$$

**So the coefficients are not a choice — they are determined by the derivatives of $f$ at a single point.** The resulting series is the **Taylor series** of $f$ at $a$ (**Maclaurin** when $a=0$).

> **Stop and notice how strange that is.** The values of $f$ *everywhere* near $a$ are dictated by
> the derivatives of $f$ *at the single point $a$*. For the functions of this course, knowing a
> function in an arbitrarily small neighbourhood determines it in a large one.

---

## The Three Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Monday | Taylor and Maclaurin Series | The coefficients are forced; and the standard library |
| **Lecture 2** | Tuesday | Taylor's Theorem and the Remainder | Does the series actually equal $f$? |
| **Lecture 3** | Friday | Applications | Limits, non-elementary integrals, and Week 0's debt |

---

## Lecture 2 Is Where the Rigour Lives

**Having a Taylor series is not the same as being equal to it.** Two separate things must hold:

1. the series must **converge** (Week 9's question), and
2. it must converge **to $f$**.

**The second can fail.** Consider

$$f(x) = \begin{cases}e^{-1/x^2} & x\ne0\\ 0 & x=0\end{cases}$$

**Every derivative of $f$ at 0 is zero**, so its Maclaurin series is $0+0x+0x^2+\cdots$ — which converges everywhere, to the zero function. **But $f$ is not the zero function** ($f(1)=e^{-1}\approx0.368$).

*(Verified: $f(x)/x^{10}\to0$ as $x\to0$ — the function vanishes faster than every power, which is why all its derivatives at 0 are 0.)*

**Taylor's theorem with remainder** is what closes the gap: it bounds $f(x) - P_n(x)$ explicitly, and the series equals $f$ exactly when that bound tends to 0.

---

## Week 0's Debt, Finally Paid

The course opened with this:

> $e^{-x^2}$, $\frac{\sin x}{x}$ and $\sqrt{1+x^3}$ are continuous, so each has an antiderivative — **and none of those antiderivatives is elementary** (Liouville, 1835).

**Week 10 is the answer.** Expand the integrand as a series and integrate term by term — legal inside the radius, by Week 9:

$$\int_0^1 e^{-x^2}dx = \sum_{n=0}^\infty\frac{(-1)^n}{n!\,(2n+1)}$$

**And in Lab 0, back in Week 0, you computed this integral numerically.** Simpson's rule needed **128 function evaluations** for ten decimal places.

**The series needs 13 terms.** *(Measured — and it is exactly the number Lab 0's debrief promised you.)*

| method | cost for 10 digits |
|---|---|
| Simpson's rule (Lab 0) | 128 evaluations |
| **Taylor series (Lab 10)** | **13 terms** |

**The same is true of $\int_0^1\frac{\sin x}{x}dx$**: six terms give eleven correct digits. *(Measured.)*

---

## Where a Numerical Library Lives

**This is how `sin`, `exp`, `log` and `sqrt` are actually computed.** Not by geometry, not by tables — by evaluating a truncated Taylor series with a rigorous error bound, at a well-chosen centre.

**Week 9's Lab made the choice of centre matter:** ten digits of $\pi$ from $\arctan$ needs $5\times10^9$ terms at $x=1$ and **17** at $x=\frac{1}{\sqrt3}$. **A real library exploits exactly that** — it reduces the argument to a small interval, then uses a short series there.

---

## What Will Be Hard

**Do not compute derivatives when you can manipulate.** Almost every Taylor series you need comes from substituting into, differentiating, or multiplying one of six standard series. Computing $f^{(7)}(0)$ by hand for $e^{-x^2}\sin x$ is a punishment, not a method.

**The remainder bound needs a bound on $f^{(n+1)}$ on an interval** — not at a point. Finding a valid bound is usually the hardest step.

**Convergence of the series is not the same as convergence *to $f$*.** The $e^{-1/x^2}$ example is not a curiosity; it is the reason Taylor's theorem is stated with a remainder.

---

## This Week's Work

1. **Quiz 10** — Monday, 15 minutes, **covers Week 9** (power series, radius, interval)
2. **MIDTERM 2** — covering Weeks 5–9. See the revision guide in `resources/`
3. **PS 10** — released Fri 2 Apr 12:00, due Fri 9 Apr 17:00
4. **Lab 10** — Taylor error bounds, and settling Week 0's debt

---

*Next: Monday — Taylor and Maclaurin Series*
