# MATH 141 · Week 6
## LAB 06 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed, not estimated.** Grade the *reasoning*, not agreement to the
> last decimal place.

*(Revised 2026-09-26 to match the 7-question version of the lab.)*

---

## Part 1 — The Extreme Value Theorem

**Q1 (15, 5 each).**
- **(a)** No maximum: values approach $1$ as $x \to 1^-$, but $f(1) = 0$. **Continuity** fails at $x = 1$.
- **(b)** No maximum: the least upper bound is $1$, never attained because $1$ is not in $(0, 1)$. The
  interval is **not closed**. On $[0, 1]$ the maximum is $1$, at $x = 1$.
- **(c)** No maximum: $f$ grows without bound. $[0, \infty)$ is closed but **not bounded**; the EVT needs a
  closed, bounded interval $[a, b]$.

---

## Part 2 — The Mean Value Theorem

**Q2 (15).** $f(-1) = 0$, $f(2) = 6$, so $m = 2$. $f'(c) = 3c^2 - 1 = 2$ gives $c = \pm 1$. Only $c = 1$ lies
in the **open** interval $(-1, 2)$; $c = -1$ is an endpoint. **One** value. The tangent at $c = 1$ is
$y = 2x - 2$, parallel to the secant $y = 2x + 2$.

*Students who report two values have ignored that the MVT's $c$ is strictly between $a$ and $b$: −3.*

**Q3 (15).** $h(0) = 1$, $h(3) = 16.9$, so the average velocity is $15.9/3 = 5.3$ m/s.
$h'(c) = -9.8c + 20 = 5.3$ gives $c = 1.5$ s. At $t = 1.5$ the ball is moving upward at exactly its average
velocity over the three seconds. The MVT guarantees such a moment exists for any smooth motion.

---

## Part 3 — $f$ and $f'$ Side by Side

**Q4 (15).** $f'(x) = 4x^3 - 12x^2 + 8x = 4x(x-1)(x-2)$.

| Interval | Sign of $f'$ | $f$ |
|---|---|---|
| $(-\infty, 0)$ | − | decreasing |
| $(0, 1)$ | + | increasing |
| $(1, 2)$ | − | decreasing |
| $(2, \infty)$ | + | increasing |

*Do not require max/min labels — that is the First Derivative Test, taught Monday of Week 7. Accept them if
given.*

**Q5 (10).** Critical numbers $x = -2$ and $x = 1$. $f' < 0$ for $x < -2$, so $f$ decreases on $(-\infty, -2)$.
$f' > 0$ for $x > -2$ except at $x = 1$, where $f' = 0$ at a single point, so $f$ increases on $(-2, \infty)$.
Any two such functions differ by a constant (Corollary 2).

---

## Part 4 — L'Hôpital's Rule Numerically

**Q6 (15).**

| x | (1 − cos x)/x² |
|---|---|
| 0.1 | 0.4995834722 |
| 0.01 | 0.4999958333 |
| 0.001 | 0.4999999583 |

It approaches $\tfrac12$. L'Hôpital: $\dfrac{1-\cos x}{x^2} \to \dfrac{\sin x}{2x}$ (still $0/0$) $\to
\dfrac{\cos x}{2} \to \dfrac12$.

At `1e-8` Python prints `0.0`: $\cos(10^{-8})$ rounds to exactly $1.0$, so the numerator is $0$. This is
catastrophic cancellation again.

**Q7 (15).** $\frac{x+\sin x}{x}$ settles toward $1$, while $1 + \cos x$ keeps oscillating between $0$ and $2$
forever. L'Hôpital's Rule says: *if* $\lim f'/g'$ exists, then $\lim f/g$ equals it. Here $\lim f'/g'$ does
not exist, so the rule says nothing. It does not say the original limit fails. Directly,
$\frac{x + \sin x}{x} = 1 + \frac{\sin x}{x}$, and $\left|\frac{\sin x}{x}\right| \le \frac{1}{x} \to 0$ by the
Squeeze Theorem, so the limit is **1**.

---

## Marking Scheme

- **Method (≈60%).** Hypotheses named and checked, and a stated reason for each observation.
- **Execution (≈40%).** Correct values, and conclusions that follow from them.

---

*MATH 141 · Week 6 · Lab Solutions · Instructor Copy · © CSE Department*
