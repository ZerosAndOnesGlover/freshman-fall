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

## Part I — Functions and Domains

### Problem 1 — Domain Solutions

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

**(c)** $h(x) = \sqrt{\dfrac{x+2}{x-1}}$

Need $\dfrac{x+2}{x-1} \geq 0$ AND $x \neq 1$ (denominator)

Critical points: $x = -2$ (numerator zero), $x = 1$ (denom zero)

Sign chart for $\dfrac{x+2}{x-1}$:
- $(-\infty, -2)$: $\dfrac{(-)}{(-)} = +$ ✅
- $(-2, 1)$: $\dfrac{(+)}{(-)} = -$ ❌
- $(1, \infty)$: $\dfrac{(+)}{(+)} = +$ ✅

At $x = -2$: value is $0/(-3) = 0 \geq 0$ ✅ (include)  
At $x = 1$: undefined ❌

$$\boxed{(-\infty, -2] \cup (1, \infty)}$$

---

**(d)** $p(x) = \arcsin(2x - 1)$

Need $-1 \leq 2x-1 \leq 1$  
$0 \leq 2x \leq 2$  
$$\boxed{[0, 1]}$$

---

**(e)** $q(x) = \dfrac{1}{\sqrt{|x| - x}}$

Need $|x| - x > 0$ (strict inequality — denominator cannot be zero)

Case 1: $x \geq 0$: $|x| = x$, so $|x| - x = x - x = 0$. Never $> 0$. No solutions here.  
Case 2: $x < 0$: $|x| = -x$, so $|x| - x = -x - x = -2x > 0$ iff $x < 0$ ✅

$$\boxed{(-\infty, 0)}$$

**Grading note:** This is a tricky problem. Award full credit for correct analysis by cases. Award 3/4 if student gets the correct answer by testing values without full case analysis.

---

### Problem 2 — $f(x) = \frac{x}{x-1}$

**(a)** $f(f(x))$

$$f(f(x)) = f\!\left(\frac{x}{x-1}\right) = \frac{\dfrac{x}{x-1}}{\dfrac{x}{x-1}-1} = \frac{\dfrac{x}{x-1}}{\dfrac{x-(x-1)}{x-1}} = \frac{\dfrac{x}{x-1}}{\dfrac{1}{x-1}} = x$$

$$\boxed{f(f(x)) = x}$$

Domain: $x \neq 0$ and $x \neq 1$ (check both applications)

**(b)** Find $f^{-1}(x)$:

$y = \dfrac{x}{x-1}$; solve for $x$: $y(x-1) = x \Rightarrow yx - y = x \Rightarrow x(y-1) = y \Rightarrow x = \dfrac{y}{y-1}$

$$f^{-1}(x) = \frac{x}{x-1}$$

$f$ **is its own inverse** — it's an involution. This is confirmed by part (a): $f(f(x)) = x$ means $f = f^{-1}$.

**(c)** $f(f(f(x)))$:

$f(f(f(x))) = f(f(f(x))) = f(x)$ (since $f(f(x)) = x$, applying $f$ once more gives $f(x)$).

**Pattern:** four applications are two pairs, each pair giving back $x$: $f^{(4)}(x) = x$; five is one more, $f^{(5)}(x) = f(x)$. In general even counts give $x$, odd counts give $f(x)$. *(Revised 2026-09-21: no induction proof is asked for — induction is not part of MATH 141.)*

---

### Problem 3 — Inverse on Restricted Domain

**(a)** $f(x) = x^2$, domain $[0,\infty)$

$f^{-1}(x) = \sqrt{x}$

Domain of $f^{-1}$: $[0, \infty)$ (= range of $f$)  
Range of $f^{-1}$: $[0, \infty)$ (= domain of $f$)

Verify: $f^{-1}(f(x)) = \sqrt{x^2} = x$ for $x \in [0,\infty)$ ✓ (need $x \geq 0$ or we'd get $|x|$)  
$f(f^{-1}(x)) = (\sqrt{x})^2 = x$ for $x \in [0,\infty)$ ✓

**(b)** $f(x) = x^2$ on $\mathbb{R}$: NOT one-to-one because $f(2) = f(-2) = 4$ — two inputs give the same output. Graphically: horizontal line $y = 4$ intersects the parabola at two points. Algebraically: for any $c > 0$, $x = \sqrt{c}$ and $x = -\sqrt{c}$ both satisfy $f(x) = c$.

---

## Part II — Algebra and Inequalities

### Problem 4 — Equations

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

**(c)** $|2x^2 - 3x| = 2$

Case 1: $2x^2 - 3x = 2 \Rightarrow 2x^2 - 3x - 2 = 0 \Rightarrow (2x+1)(x-2) = 0 \Rightarrow x = -1/2$ or $x = 2$

Case 2: $2x^2 - 3x = -2 \Rightarrow 2x^2 - 3x + 2 = 0$  
Discriminant: $9 - 16 = -7 < 0$. No real solutions.

$$\boxed{x = -\frac{1}{2} \text{ or } x = 2}$$

---

**(d)** $\dfrac{2}{x-1} - \dfrac{3}{x+2} = \dfrac{4}{x^2+x-2}$

Note $x^2 + x - 2 = (x-1)(x+2)$, so:
$$\frac{2(x+2) - 3(x-1)}{(x-1)(x+2)} = \frac{4}{(x-1)(x+2)}$$
$$2x + 4 - 3x + 3 = 4$$
$$-x + 7 = 4$$
$$x = 3$$

Check: $x = 3$ makes neither denominator zero. ✅

$$\boxed{x = 3}$$

---

### Problem 5 — Inequalities

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

**(c)** $\dfrac{x^2-3x}{x^2+x-2} \leq 1$

Move to one side: $\dfrac{x^2-3x}{x^2+x-2} - 1 \leq 0$

$$\frac{x^2-3x - (x^2+x-2)}{x^2+x-2} \leq 0 \Rightarrow \frac{-4x+2}{(x+2)(x-1)} \leq 0 \Rightarrow \frac{-2(2x-1)}{(x+2)(x-1)} \leq 0$$

Equivalently: $\dfrac{2x-1}{(x+2)(x-1)} \geq 0$

Critical points: $x = 1/2, -2, 1$

Sign of $\dfrac{2x-1}{(x+2)(x-1)}$:
| Interval | Sign |
|----------|------|
| $(-\infty,-2)$ | $\frac{(-)}{(-)(-)}) = -$ ❌ |
| $(-2, 1/2)$ | $\frac{(-)}{(+)(-)} = +$ ✅ |
| $(1/2, 1)$ | $\frac{(+)}{(+)(-)} = -$ ❌ |
| $(1, \infty)$ | $\frac{(+)}{(+)(+)} = +$ ✅ |

At $x = 1/2$: value $= 0$ ✅. At $x = -2, 1$: undefined ❌.

$$\boxed{(-2, \tfrac{1}{2}] \cup (1, \infty)}$$

---

### Problem 6 — Algebraic Manipulation

**(a)** $\dfrac{\sqrt{x+h}-\sqrt{x}}{h}$

Multiply numerator and denominator by $\sqrt{x+h}+\sqrt{x}$:

$$= \frac{(x+h)-x}{h(\sqrt{x+h}+\sqrt{x})} = \frac{h}{h(\sqrt{x+h}+\sqrt{x})} = \frac{1}{\sqrt{x+h}+\sqrt{x}}$$

At $h = 0$ the simplified form is $\dfrac{1}{\sqrt{x}+\sqrt{x}} = \dfrac{1}{2\sqrt{x}}$ (Week 3 will show this is the derivative of $\sqrt{x}$)

*This is the derivative of $\sqrt{x}$. Students should note this.*

**(b)** $\dfrac{\frac{1}{(x+h)^2} - \frac{1}{x^2}}{h}$

$$= \frac{\frac{x^2 - (x+h)^2}{x^2(x+h)^2}}{h} = \frac{x^2 - x^2 - 2xh - h^2}{hx^2(x+h)^2} = \frac{-2xh - h^2}{hx^2(x+h)^2}$$
$$= \frac{h(-2x-h)}{hx^2(x+h)^2} = \frac{-2x-h}{x^2(x+h)^2}$$

At $h = 0$ the simplified form is $\dfrac{-2x}{x^4} = \dfrac{-2}{x^3}$

*This is the derivative of $x^{-2}$.*

---

## Part III — Exponentials and Logarithms

### Problem 7 — Equations

**(a)** $e^{2x} - 4e^x + 3 = 0$

Let $u = e^x$: $u^2 - 4u + 3 = 0 \Rightarrow (u-1)(u-3) = 0$  
$u = 1 \Rightarrow e^x = 1 \Rightarrow \boxed{x = 0}$  
$u = 3 \Rightarrow e^x = 3 \Rightarrow \boxed{x = \ln 3}$

**(b)** $\log_3(x+4) - \log_3(x) = 2$

$\log_3\!\left(\dfrac{x+4}{x}\right) = 2 \Rightarrow \dfrac{x+4}{x} = 9 \Rightarrow x + 4 = 9x \Rightarrow 8x = 4 \Rightarrow x = \tfrac{1}{2}$

Check: $x = 1/2 > 0$ ✅. $\log_3(9/2) - \log_3(1/2) = \log_3(9) = 2$ ✅

$$\boxed{x = \frac{1}{2}}$$

**(c)** $3^x \cdot 9^{x-1} = 27^{2x}$

$3^x \cdot 3^{2(x-1)} = 3^{3(2x)}$  
$3^{x + 2x - 2} = 3^{6x}$  
$3x - 2 = 6x$  
$x = -\dfrac{2}{3}$

$$\boxed{x = -\frac{2}{3}}$$

**(d)** $\ln(x+1) - \ln(x-1) = 1$

$\ln\!\left(\dfrac{x+1}{x-1}\right) = 1 \Rightarrow \dfrac{x+1}{x-1} = e \Rightarrow x+1 = e(x-1) \Rightarrow x+1 = ex-e$

$x(e-1) = e+1 \Rightarrow x = \dfrac{e+1}{e-1}$

Check: $x = (e+1)/(e-1) \approx 2.16 > 1$, so $x+1 > 0$ and $x-1 > 0$. ✅

$$\boxed{x = \frac{e+1}{e-1}}$$

---

### Problem 8 — Medication Model

**(a)** Half-life 4 hours: $\frac{1}{2}C_0 = C_0 e^{-4k} \Rightarrow e^{-4k} = \frac{1}{2} \Rightarrow k = \dfrac{\ln 2}{4}$

$$\boxed{k = \frac{\ln 2}{4} \approx 0.1733 \text{ hr}^{-1}}$$

**(b)** When $C(t) < 10$: $100e^{-kt} < 10 \Rightarrow e^{-kt} < 0.1 \Rightarrow -kt < \ln(0.1) \Rightarrow t > \dfrac{\ln 10}{k} = \dfrac{4\ln 10}{\ln 2}$

$$t > \frac{4\ln 10}{\ln 2} = 4\log_2 10 \approx 4 \times 3.322 = 13.29 \text{ hours}$$

**(c)** Therapeutic window: $C(t) \geq 15$:  
$100e^{-kt} \geq 15 \Rightarrow e^{-kt} \geq 0.15 \Rightarrow t \leq \dfrac{-\ln(0.15)}{k} = \dfrac{4\ln(1/0.15)}{\ln 2} = \dfrac{4\ln(20/3)}{\ln 2}$

$\ln(20/3) \approx \ln(6.667) \approx 1.897$

$t \leq \dfrac{4 \times 1.897}{0.6931} \approx \dfrac{7.589}{0.6931} \approx 10.95$ hours

Drug effective for approximately **10.95 hours** (exact: $\dfrac{4\ln(20/3)}{\ln 2}$).

---

### Problem 9 — Change of Base

**(a)** Let $y = \log_a x$. By definition, $a^y = x$.  
Take $\ln$: $y \ln a = \ln x \Rightarrow y = \dfrac{\ln x}{\ln a}$  
Therefore $\log_a x = \dfrac{\ln x}{\ln a}$. ∎

**(b)** $\log_8 32 = \dfrac{\ln 32}{\ln 8} = \dfrac{5\ln 2}{3\ln 2} = \dfrac{5}{3}$

**(c)** $\log_a b \cdot \log_b c \cdot \log_c a = \dfrac{\ln b}{\ln a} \cdot \dfrac{\ln c}{\ln b} \cdot \dfrac{\ln a}{\ln c} = 1$ ∎

---

## Part IV — Trigonometry

### Problem 10 — Exact Values

**(a)** $\cos(7\pi/6) = -\cos(\pi/6) = -\dfrac{\sqrt{3}}{2}$ (third quadrant)

**(b)** $\tan(-3\pi/4) = \tan(-3\pi/4 + \pi) = \tan(\pi/4) = 1$ (tan has period $\pi$)

**(c)** $\sin(17\pi/3) = \sin(17\pi/3 - 6\pi) = \sin(17\pi/3 - 18\pi/3) = \sin(-\pi/3) = -\sin(\pi/3) = -\dfrac{\sqrt{3}}{2}$

**(d)** $\arctan\left(\tan(5\pi/4)\right)$: $\tan(5\pi/4) = \tan(\pi/4) = 1$. Range of $\arctan$ is $(-\pi/2, \pi/2)$, so $\arctan(1) = \pi/4$.  
Answer: $\pi/4$. *(Note: NOT $5\pi/4$, since $5\pi/4 \notin (-\pi/2, \pi/2)$)*

**(e)** $\cos(\arcsin(3/5))$: If $\theta = \arcsin(3/5)$, then $\sin\theta = 3/5$ with $\theta \in [-\pi/2, \pi/2]$, so $\cos\theta \geq 0$.  
$\cos\theta = \sqrt{1 - 9/25} = \sqrt{16/25} = \dfrac{4}{5}$

---

### Problem 11 — Identities

**(a)** LHS: $\dfrac{\tan\theta + \cot\theta}{\sec\theta\csc\theta}$

$$= \frac{\dfrac{\sin\theta}{\cos\theta} + \dfrac{\cos\theta}{\sin\theta}}{\dfrac{1}{\cos\theta} \cdot \dfrac{1}{\sin\theta}} = \frac{\dfrac{\sin^2\theta + \cos^2\theta}{\sin\theta\cos\theta}}{\dfrac{1}{\sin\theta\cos\theta}} = \frac{1}{\sin\theta\cos\theta} \cdot \sin\theta\cos\theta = 1 = \text{RHS}$$ ∎

**(b)** RHS: $2\sin A\sin B$

LHS: $\cos(A-B) - \cos(A+B)$  
$= (\cos A\cos B + \sin A\sin B) - (\cos A\cos B - \sin A\sin B)$  
$= 2\sin A\sin B$ ∎

---

### Problem 12 — Trig Equations

**(a)** $\sin(2\theta) = \cos\theta$ on $[0, 2\pi)$

$2\sin\theta\cos\theta = \cos\theta$  
$2\sin\theta\cos\theta - \cos\theta = 0$  
$\cos\theta(2\sin\theta - 1) = 0$

$\cos\theta = 0 \Rightarrow \theta = \pi/2, 3\pi/2$  
$\sin\theta = 1/2 \Rightarrow \theta = \pi/6, 5\pi/6$

$$\boxed{\theta = \pi/6, \pi/2, 5\pi/6, 3\pi/2}$$

**(b)** $2\cos^2\theta + 3\sin\theta = 3$ on $[0, 2\pi)$

$2(1-\sin^2\theta) + 3\sin\theta = 3$  
$2 - 2\sin^2\theta + 3\sin\theta = 3$  
$2\sin^2\theta - 3\sin\theta + 1 = 0$  
$(2\sin\theta - 1)(\sin\theta - 1) = 0$

$\sin\theta = 1/2 \Rightarrow \theta = \pi/6, 5\pi/6$  
$\sin\theta = 1 \Rightarrow \theta = \pi/2$

$$\boxed{\theta = \pi/6, \pi/2, 5\pi/6}$$

---

