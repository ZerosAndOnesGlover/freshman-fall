# MATH 141 · Calculus I
## Problem Set 0 — INSTRUCTOR SOLUTIONS
### ⚠️ NOT FOR DISTRIBUTION TO STUDENTS ⚠️

---


## Marking Scheme

Point values are printed per problem on the problem set. Within each problem, split the marks:

- **Method (≈60%).** Correct technique named and set up: the right rule or theorem, hypotheses checked where the theorem requires it, and the symbolic work shown before any numerical evaluation.
- **Execution (≈40%).** Correct algebra and simplification, correct final form, and any domain restrictions or constants of integration stated.

A bare answer with no working earns at most the execution marks — and in proof problems ("show that", "prove"), no marks at all, since the reasoning *is* the deliverable.

**Carry-through.** Penalise a given error once. If the student proceeds correctly from their own wrong intermediate value, award the downstream marks in full.

**Equivalent forms.** Accept any algebraically equivalent answer — factored or expanded, and trigonometric identities applied or not — unless the problem explicitly demands a particular form.

### Common errors in this problem set

**1. Ignoring domain restrictions.** The natural domain must exclude zeros of denominators, negatives under even roots, and non-positive arguments of logs. A student who simplifies (x²−1)/(x−1) to x+1 without noting x ≠ 1 has changed the function.

**2. Inventing log and exponent laws.** log(a+b) ≠ log a + log b, and (a+b)ⁿ ≠ aⁿ + bⁿ. These are the two most common false identities; treat either as a method error, not a slip.

**3. Extraneous roots from squaring.** Squaring both sides is not reversible — every candidate must be checked in the *original* equation. A solution set presented without that check is incomplete.

**4. Degrees instead of radians.** All calculus of trig functions assumes radians. sin x ≈ x and (d/dx)sin x = cos x are both false in degrees.

---
*(Revised 2026-09-26: the set was cut to 8 problems and 16 parts. The problems below follow the new numbering.)*

---

## Problem 1 — Domains (12 pts)

**(a)** $f(x) = \dfrac{\sqrt{3-x}}{x^2 - 4}$

Numerator: $3 - x \geq 0 \Rightarrow x \leq 3$  
Denominator: $x^2 - 4 \neq 0 \Rightarrow x \neq \pm 2$

Intersect $(-\infty, 3]$ with $\{x \neq \pm 2\}$:  
$$\boxed{(-\infty, -2) \cup (-2, 2) \cup (2, 3]}$$

**Common student error:** Forgetting $x = -2$ is in $(-\infty, 3]$ and must be excluded. Award 1/2 for correct numerator restriction, 1/2 for correct denominator exclusion, full credit requires both.

---

**(b)** $g(x) = \ln(x^2 - 5x + 6)$

Need $x^2 - 5x + 6 > 0$  
Factor: $(x-2)(x-3) > 0$

Sign chart:
- $(-\infty, 2)$: $(-)(-) = +$ ✅
- $(2, 3)$: $(+)(-) = -$ ❌
- $(3, \infty)$: $(+)(+) = +$ ✅

$$\boxed{(-\infty, 2) \cup (3, \infty)}$$

---

## Problem 2 — $f(x) = \frac{x}{x-1}$ (12 pts)

**(a)** $f(f(x))$

$$f(f(x)) = f\!\left(\frac{x}{x-1}\right) = \frac{\dfrac{x}{x-1}}{\dfrac{x}{x-1}-1} = \frac{\dfrac{x}{x-1}}{\dfrac{x-(x-1)}{x-1}} = \frac{\dfrac{x}{x-1}}{\dfrac{1}{x-1}} = x$$

$$\boxed{f(f(x)) = x}$$

Domain: $x \neq 0$ and $x \neq 1$ (check both applications)

**(b)** Find $f^{-1}(x)$:

$y = \dfrac{x}{x-1}$; solve for $x$: $y(x-1) = x \Rightarrow yx - y = x \Rightarrow x(y-1) = y \Rightarrow x = \dfrac{y}{y-1}$

$$f^{-1}(x) = \frac{x}{x-1}$$

$f$ **is its own inverse** — it's an involution. This is confirmed by part (a): $f(f(x)) = x$ means $f = f^{-1}$.

---

## Problem 3 — Equations (12 pts)

**(a)** $\sqrt{x+5} - \sqrt{x-3} = 2$

Isolate one radical: $\sqrt{x+5} = 2 + \sqrt{x-3}$  
Square: $x + 5 = 4 + 4\sqrt{x-3} + (x-3)$  
$x + 5 = x + 1 + 4\sqrt{x-3}$  
$4 = 4\sqrt{x-3}$  
$\sqrt{x-3} = 1$  
$x - 3 = 1 \Rightarrow x = 4$

Check: $\sqrt{9} - \sqrt{1} = 3 - 1 = 2$ ✅

$$\boxed{x = 4}$$

---

**(b)** $x^4 - 5x^2 + 4 = 0$

Substitute $u = x^2$: $u^2 - 5u + 4 = 0 \Rightarrow (u-1)(u-4) = 0$  
$u = 1 \Rightarrow x^2 = 1 \Rightarrow x = \pm 1$  
$u = 4 \Rightarrow x^2 = 4 \Rightarrow x = \pm 2$

$$\boxed{x = -2, -1, 1, 2}$$

---

## Problem 4 — Inequalities (12 pts)

**(a)** $\dfrac{x^2-1}{x^2-4} \geq 0$

Factor: $\dfrac{(x-1)(x+1)}{(x-2)(x+2)} \geq 0$

Critical points: $x = \pm 1, \pm 2$

Sign chart (left to right: $-\infty, -2, -1, 1, 2, \infty$):

| Interval | $(x-1)$ | $(x+1)$ | $(x-2)$ | $(x+2)$ | Sign |
|----------|---------|---------|---------|---------|------|
| $(-\infty,-2)$ | $-$ | $-$ | $-$ | $-$ | $+$ ✅ |
| $(-2,-1)$ | $-$ | $-$ | $-$ | $+$ | $-$ ❌ |
| $(-1,1)$ | $-$ | $+$ | $-$ | $+$ | $+$ ✅ |
| $(1,2)$ | $+$ | $+$ | $-$ | $+$ | $-$ ❌ |
| $(2,\infty)$ | $+$ | $+$ | $+$ | $+$ | $+$ ✅ |

At $x = \pm 1$: expression $= 0$ ✅. At $x = \pm 2$: undefined ❌.

$$\boxed{(-\infty,-2) \cup [-1,1] \cup (2,\infty)}$$

---

**(b)** $|x^2 - 2x - 3| < 5$

Factor: $|{(x-3)(x+1)}| < 5$

Case 1: $(x-3)(x+1) < 5 \Rightarrow x^2 - 2x - 3 < 5 \Rightarrow x^2 - 2x - 8 < 0 \Rightarrow (x-4)(x+2) < 0 \Rightarrow x \in (-2, 4)$

Case 2: $(x-3)(x+1) > -5 \Rightarrow x^2 - 2x - 3 > -5 \Rightarrow x^2 - 2x + 2 > 0$  
Discriminant: $4 - 8 = -4 < 0$. Always positive. ✅ No restriction.

Intersect: $(-2, 4) \cap \mathbb{R} = (-2, 4)$

$$\boxed{(-2, 4)}$$

---

## Problem 5 — Rationalizing (10 pts)

Multiply numerator and denominator by $\sqrt{x+h}+\sqrt{x}$:

$$= \frac{(x+h)-x}{h(\sqrt{x+h}+\sqrt{x})} = \frac{h}{h(\sqrt{x+h}+\sqrt{x})} = \frac{1}{\sqrt{x+h}+\sqrt{x}}$$

At $h = 0$ the simplified form is $\dfrac{1}{\sqrt{x}+\sqrt{x}} = \dfrac{1}{2\sqrt{x}}$ (Week 3 will show this is the derivative of $\sqrt{x}$)

---

## Problem 6 — Exponential and Logarithmic Equations (12 pts)

**(a)** $e^{2x} - 4e^x + 3 = 0$

Let $u = e^x$: $u^2 - 4u + 3 = 0 \Rightarrow (u-1)(u-3) = 0$  
$u = 1 \Rightarrow e^x = 1 \Rightarrow \boxed{x = 0}$  
$u = 3 \Rightarrow e^x = 3 \Rightarrow \boxed{x = \ln 3}$

**(b)** $\ln(x+1) - \ln(x-1) = 1$

$\ln\!\left(\dfrac{x+1}{x-1}\right) = 1 \Rightarrow \dfrac{x+1}{x-1} = e \Rightarrow x+1 = e(x-1) \Rightarrow x+1 = ex-e$

$x(e-1) = e+1 \Rightarrow x = \dfrac{e+1}{e-1}$

Check: $x = (e+1)/(e-1) \approx 2.16 > 1$, so $x+1 > 0$ and $x-1 > 0$. ✅

$$\boxed{x = \frac{e+1}{e-1}}$$

---

## Problem 7 — Half-Life (12 pts)

**(a)** Half-life 4 hours: $\frac{1}{2}C_0 = C_0 e^{-4k} \Rightarrow e^{-4k} = \frac{1}{2} \Rightarrow k = \dfrac{\ln 2}{4}$

$$\boxed{k = \frac{\ln 2}{4} \approx 0.1733 \text{ hr}^{-1}}$$

**(b)** When $C(t) < 10$: $100e^{-kt} < 10 \Rightarrow e^{-kt} < 0.1 \Rightarrow -kt < \ln(0.1) \Rightarrow t > \dfrac{\ln 10}{k} = \dfrac{4\ln 10}{\ln 2}$

$$t > \frac{4\ln 10}{\ln 2} = 4\log_2 10 \approx 4 \times 3.322 = 13.29 \text{ hours}$$

Exact: $t = \dfrac{4\ln 10}{\ln 2}$; decimal $13.29$ hours.

---

## Problem 8 — Trigonometry (18 pts)

**(a)** $\sin(17\pi/3) = \sin(17\pi/3 - 6\pi) = \sin(17\pi/3 - 18\pi/3) = \sin(-\pi/3) = -\sin(\pi/3) = -\dfrac{\sqrt{3}}{2}$

**(b)** $\cos(\arcsin(3/5))$: If $\theta = \arcsin(3/5)$, then $\sin\theta = 3/5$ with $\theta \in [-\pi/2, \pi/2]$, so $\cos\theta \geq 0$.  
$\cos\theta = \sqrt{1 - 9/25} = \sqrt{16/25} = \dfrac{4}{5}$

**(c)** $\sin(2\theta) = \cos\theta$ on $[0, 2\pi)$

$2\sin\theta\cos\theta = \cos\theta$  
$2\sin\theta\cos\theta - \cos\theta = 0$  
$\cos\theta(2\sin\theta - 1) = 0$

$\cos\theta = 0 \Rightarrow \theta = \pi/2, 3\pi/2$  
$\sin\theta = 1/2 \Rightarrow \theta = \pi/6, 5\pi/6$

$$\boxed{\theta = \pi/6, \pi/2, 5\pi/6, 3\pi/2}$$

---

*MATH 141 · Week 0 · PS 0 Solutions · Instructor Copy · © CSE Department*
