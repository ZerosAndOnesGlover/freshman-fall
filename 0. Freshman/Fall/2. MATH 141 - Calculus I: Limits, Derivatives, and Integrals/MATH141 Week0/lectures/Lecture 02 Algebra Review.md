# MATH 141 · Calculus I
## Week 0 · Lecture 2 of 4
### Algebra Review: Equations, Inequalities & the Coordinate Plane

**Date:** Wednesday 19 August 2026 · 11:00–11:50 · Week 0

---

**Course:** MATH 141: Calculus I  
**Reading:** Stewart §1.1–1.3 | Spivak Ch. 1

---

## Why Algebra Is the Calculus Bottleneck

Here is a fact that surprises many students: most errors on calculus exams are not calculus errors — they are algebra errors. The derivative of $\sin(x^2)$ is straightforward once you know the chain rule. The error happens when simplifying the result. This lecture is a targeted review of the algebra skills that calculus will demand constantly.

We will not review everything — only what calculus actually uses heavily. Master this material and you remove the most common source of lost points.

---

## 1. The Real Number Line and Intervals

The real numbers $\mathbb{R}$ are ordered: for any two distinct reals $a$ and $b$, either $a < b$ or $a > b$.

### Interval Notation (Review)

You met this in [[Lecture 00 The Language of Mathematics]] §4. Before reading the table, recall it yourself: which
bracket **includes** its endpoint, and why can $\infty$ never take one?

| Notation | Meaning | Graph |
|----------|---------|-------|
| $(a, b)$ | $a < x < b$ (open) | Excludes endpoints |
| $[a, b]$ | $a \leq x \leq b$ (closed) | Includes endpoints |
| $[a, b)$ | $a \leq x < b$ (half-open) | Includes $a$, excludes $b$ |
| $(a, \infty)$ | $x > a$ | Unbounded right |
| $(-\infty, b]$ | $x \leq b$ | Unbounded left |
| $(-\infty, \infty)$ | All reals $\mathbb{R}$ | — |

From here on, every solution set in this course is written this way. If the table above
was not immediate, reread [[Lecture 00 The Language of Mathematics]] §4–5 before continuing — the sign-chart
work in §3 below is unreadable without it.

### Absolute Value

$$|x| = \begin{cases} x & \text{if } x \geq 0 \\ -x & \text{if } x < 0 \end{cases}$$

Geometrically, $|x|$ is the **distance** from $x$ to $0$ on the number line.  
More generally, $|a - b|$ is the **distance** between $a$ and $b$.

**Key properties:**
$$|ab| = |a||b| \qquad \left|\frac{a}{b}\right| = \frac{|a|}{|b|} \qquad |a+b| \leq |a| + |b| \text{ (Triangle Inequality)}$$

The **Triangle Inequality** — $|a + b| \leq |a| + |b|$ — is one of the most important inequalities in analysis. It will appear in every $\varepsilon$-$\delta$ proof in this course.

**Absolute value equations and inequalities:**

| Equation / Inequality | Equivalent Form |           |                               |
| --------------------- | --------------- | --------- | ----------------------------- |
| $                     | x               | = c$      | $x = c$ or $x = -c$           |
| $                     | x               | < c$      | $-c < x < c$                  |
| $                     | x               | > c$      | $x > c$ or $x < -c$           |
| $                     | x - a           | < \delta$ | $a - \delta < x < a + \delta$ |

The last form, $|x - a| < \delta$ describing a neighborhood of $a$, is the exact language of limits. Learn to read it fluently.

---

## 2. Solving Equations

### 2.1 Linear Equations

Standard form: $ax + b = 0$. Solve by isolating $x$:
$$x = -\frac{b}{a} \quad (a \neq 0)$$

### 2.2 Quadratic Equations

$ax^2 + bx + c = 0$

**Three methods:**

**Factoring** (when obvious):  
$x^2 - 5x + 6 = (x-2)(x-3) = 0 \Rightarrow x = 2$ or $x = 3$

**Completing the square:**  
$x^2 + bx = x^2 + bx + \left(\frac{b}{2}\right)^2 - \left(\frac{b}{2}\right)^2 = \left(x + \frac{b}{2}\right)^2 - \frac{b^2}{4}$

This technique is essential for putting conic sections in standard form and for integration later.

**Quadratic formula** (always works):
$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

The **discriminant** $\Delta = b^2 - 4ac$ tells you:
- $\Delta > 0$: two distinct real roots
- $\Delta = 0$: one repeated real root
- $\Delta < 0$: no real roots (complex roots)

### 2.3 Polynomial Equations

**Factor Theorem:** $(x - r)$ is a factor of $P(x)$ if and only if $P(r) = 0$.

**Rational Root Theorem:** If $P(x) = a_n x^n + \cdots + a_0$ has rational root $p/q$ (in lowest terms), then $p \mid a_0$ and $q \mid a_n$.

**Useful factoring identities to memorize:**
$$a^2 - b^2 = (a-b)(a+b)$$
$$a^3 - b^3 = (a-b)(a^2 + ab + b^2)$$
$$a^3 + b^3 = (a+b)(a^2 - ab + b^2)$$
$$a^n - b^n = (a-b)(a^{n-1} + a^{n-2}b + \cdots + b^{n-1})$$

### 2.4 Equations Involving Radicals

**Strategy:** Isolate the radical, then raise both sides to the appropriate power.

**Critical:** After squaring, always check for extraneous solutions.

**Example:**  
$\sqrt{2x + 3} = x - 1$  
Square: $2x + 3 = (x-1)^2 = x^2 - 2x + 1$  
Collect on one side: $x^2 - 2x + 1 - 2x - 3 = 0 \Rightarrow x^2 - 4x - 2 = 0$  
Quadratic formula: $x = \frac{4 \pm \sqrt{16+8}}{2} = \frac{4 \pm \sqrt{24}}{2} = 2 \pm \sqrt{6}$

Check $x = 2 + \sqrt{6} \approx 4.45$: LHS $= \sqrt{7 + 2\sqrt{6}} > 0$, RHS $= 1 + \sqrt{6} > 0$. ✅  
Check $x = 2 - \sqrt{6} \approx -0.45$: RHS $= 1 - \sqrt{6} < 0$, but LHS $\geq 0$. ❌ Extraneous.

### 2.5 Equations with Exponentials and Logarithms

**Key rules:**

**Exponential:**
$$a^x = a^y \iff x = y \quad (a > 0, a \neq 1)$$
$$a^{x+y} = a^x \cdot a^y \qquad (a^x)^y = a^{xy} \qquad a^{-x} = \frac{1}{a^x}$$

**Logarithmic:**
$$\log_a(xy) = \log_a x + \log_a y$$
$$\log_a\left(\frac{x}{y}\right) = \log_a x - \log_a y$$
$$\log_a(x^r) = r \log_a x$$
$$\log_a x = \frac{\ln x}{\ln a} \quad \text{(change of base)}$$

**Example:** Solve $3^{2x-1} = 5$  
Take $\ln$: $(2x-1)\ln 3 = \ln 5$  
$x = \frac{1}{2}\left(\frac{\ln 5}{\ln 3} + 1\right) = \frac{\ln 5 + \ln 3}{2\ln 3} = \frac{\ln 15}{2 \ln 3}$

---

## 3. Solving Inequalities

Inequalities require more care than equations because multiplying by a negative number **reverses the inequality sign**.

### 3.1 Linear Inequalities

Solve like equations, but flip the sign when multiplying/dividing by a negative.

$-3x + 2 > 8 \Rightarrow -3x > 6 \Rightarrow x < -2$

### 3.2 Polynomial Inequalities

**The Sign Chart Method:**

To solve $f(x) > 0$ (or $< 0$):

1. Find all real zeros of $f(x)$
2. Plot them on a number line — they divide $\mathbb{R}$ into intervals
3. Test one value in each interval
4. Determine the sign of $f$ in each interval
5. Select intervals matching your inequality

**Example:** Solve $x^2 - x - 6 > 0$

Factor: $(x-3)(x+2) > 0$  
Zeros: $x = -2$ and $x = 3$

| Interval | Test point | $(x-3)$ | $(x+2)$ | Product |
|----------|------------|---------|---------|---------|
| $(-\infty,-2)$ | $x=-3$ | $-$ | $-$ | $+$ ✅ |
| $(-2, 3)$ | $x=0$ | $-$ | $+$ | $-$ ❌ |
| $(3, \infty)$ | $x=4$ | $+$ | $+$ | $+$ ✅ |

Solution: $(-\infty, -2) \cup (3, \infty)$

### 3.3 Rational Inequalities

**Never cross-multiply without checking the sign of the denominator.** Instead, move everything to one side and use a sign chart.

**Example:** Solve $\dfrac{x+1}{x-2} \leq 3$

Move all terms left:
$$\frac{x+1}{x-2} - 3 \leq 0 \Rightarrow \frac{x+1 - 3(x-2)}{x-2} \leq 0 \Rightarrow \frac{-2x+7}{x-2} \leq 0$$

Critical points: $x = 7/2$ (numerator zero) and $x = 2$ (denominator zero, excluded)

| Interval | Sign of $-2x+7$ | Sign of $x-2$ | Sign of quotient |
|----------|----------------|---------------|-----------------|
| $(-\infty, 2)$ | $+$ | $-$ | $-$ ✅ |
| $(2, 7/2)$ | $+$ | $+$ | $+$ ❌ |
| $(7/2, \infty)$ | $-$ | $+$ | $-$ ✅ |

At $x = 7/2$: quotient $= 0$, which satisfies $\leq 0$. ✅  
At $x = 2$: undefined. ❌

Solution: $(-\infty, 2) \cup [7/2, \infty)$

### 3.4 Absolute Value Inequalities

Remember: $|f(x)| < c \iff -c < f(x) < c$

**Example:** Solve $|2x - 5| < 7$  
$-7 < 2x - 5 < 7$  
$-2 < 2x < 12$  
$-1 < x < 6$

Solution: $(-1, 6)$

---

## 4. The Coordinate Plane

### 4.1 Distance Formula

Distance between $(x_1, y_1)$ and $(x_2, y_2)$:
$$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

This is the Pythagorean theorem. Every time you compute a distance in $\mathbb{R}^n$, you are applying a generalization of this formula.

### 4.2 Midpoint Formula

Midpoint of the segment from $(x_1, y_1)$ to $(x_2, y_2)$:
$$M = \left(\frac{x_1+x_2}{2}, \frac{y_1+y_2}{2}\right)$$

### 4.3 Lines

**Slope** of line through $(x_1, y_1)$ and $(x_2, y_2)$:
$$m = \frac{y_2 - y_1}{x_2 - x_1} = \frac{\Delta y}{\Delta x} = \frac{\text{rise}}{\text{run}}$$

Slope is the *constant rate of change* of $y$ with respect to $x$. Calculus generalizes this to **instantaneous** rate of change via derivatives.

**Forms of a line equation:**

| Form | Equation | Use case |
|------|----------|----------|
| Slope-intercept | $y = mx + b$ | Given slope and $y$-intercept |
| Point-slope | $y - y_1 = m(x - x_1)$ | Given slope and one point |
| Standard | $ax + by = c$ | General form |
| Vertical | $x = a$ | Undefined slope |

**Parallel lines:** Same slope, different $y$-intercept: $m_1 = m_2$  
**Perpendicular lines:** Slopes are negative reciprocals: $m_1 \cdot m_2 = -1$

### 4.4 Circles

A circle with center $(h, k)$ and radius $r$:
$$(x-h)^2 + (y-k)^2 = r^2$$

**Example:** Find center and radius of $x^2 + y^2 - 6x + 4y - 3 = 0$

Complete the square in $x$ and $y$:
$$(x^2 - 6x + 9) + (y^2 + 4y + 4) = 3 + 9 + 4 = 16$$
$$(x-3)^2 + (y+2)^2 = 16$$

Center: $(3, -2)$, Radius: $4$

---

## 5. Algebraic Manipulation Techniques for Calculus

These specific techniques appear repeatedly in calculus computations.

### 5.1 Rationalizing

Used to simplify expressions involving radicals, especially in limit computations.

**Multiply by conjugate:**
$$\frac{\sqrt{x+h} - \sqrt{x}}{h} \cdot \frac{\sqrt{x+h} + \sqrt{x}}{\sqrt{x+h}+\sqrt{x}} = \frac{(x+h) - x}{h(\sqrt{x+h}+\sqrt{x})} = \frac{1}{\sqrt{x+h}+\sqrt{x}}$$

This manipulation is exactly how we compute the derivative of $\sqrt{x}$ from the definition.

### 5.2 Partial Fraction Decomposition (Preview)

For integration later:
$$\frac{2x+1}{(x-1)(x+2)} = \frac{A}{x-1} + \frac{B}{x+2}$$

Multiply both sides by $(x-1)(x+2)$:  
$2x + 1 = A(x+2) + B(x-1)$

Set $x = 1$: $3 = 3A \Rightarrow A = 1$  
Set $x = -2$: $-3 = -3B \Rightarrow B = 1$

So $\dfrac{2x+1}{(x-1)(x+2)} = \dfrac{1}{x-1} + \dfrac{1}{x+2}$

### 5.3 Simplifying Complex Fractions

$$\frac{\dfrac{1}{x+h} - \dfrac{1}{x}}{h} = \frac{\dfrac{x - (x+h)}{x(x+h)}}{h} = \frac{-h}{hx(x+h)} = \frac{-1}{x(x+h)}$$

This is the derivative of $1/x$ from the definition.

### 5.4 Long Division of Polynomials

When degree of numerator $\geq$ degree of denominator:

$$\frac{x^3 + 2x - 1}{x - 1} = x^2 + x + 3 + \frac{2}{x-1}$$

Verify: $(x-1)(x^2+x+3) + 2 = x^3+x^2+3x - x^2-x-3+2 = x^3 + 2x - 1$ ✅

---

## 6. Common Algebraic Errors to Eliminate

Here are the mistakes that calculus courses see most frequently. Study them. Eliminate them.

**Error 1:** $\sqrt{a^2 + b^2} = a + b$  
**Correct:** $\sqrt{a^2 + b^2} \neq a + b$ in general. $\sqrt{9 + 16} = 5 \neq 3 + 4 = 7$.

**Error 2:** $(a+b)^2 = a^2 + b^2$  
**Correct:** $(a+b)^2 = a^2 + 2ab + b^2$. The $2ab$ term is never missing.

**Error 3:** $\dfrac{a + b}{a} = b$  
**Correct:** $\dfrac{a+b}{a} = 1 + \dfrac{b}{a}$. You can only cancel common *factors*, not additive terms.

**Error 4:** $\ln(a + b) = \ln a + \ln b$  
**Correct:** $\ln(ab) = \ln a + \ln b$. The log of a *product* splits, not the log of a *sum*.

**Error 5:** $\dfrac{d}{dx}[f(x)g(x)] = f'(x)g'(x)$  
**Correct:** This is wrong (product rule is different). Flagged here so you know to watch for it in Week 4, when the product rule arrives.

---

## 7. Trigonometry Deep Dive: What Calculus Actually Needs

### The Unit Circle

The unit circle ($r = 1$, centered at origin) defines:
$$\cos\theta = x\text{-coordinate}, \qquad \sin\theta = y\text{-coordinate}$$

at the point on the circle at angle $\theta$ from the positive $x$-axis (measured counterclockwise).

**Exact values you must know:**

| $\theta$ | $0$ | $\pi/6$ | $\pi/4$ | $\pi/3$ | $\pi/2$ | $\pi$ | $3\pi/2$ | $2\pi$ |
|---------|-----|---------|---------|---------|---------|-------|----------|-------|
| $\sin\theta$ | $0$ | $1/2$ | $\frac{\sqrt{2}}{2}$ | $\frac{\sqrt{3}}{2}$ | $1$ | $0$ | $-1$ | $0$ |
| $\cos\theta$ | $1$ | $\frac{\sqrt{3}}{2}$ | $\frac{\sqrt{2}}{2}$ | $1/2$ | $0$ | $-1$ | $0$ | $1$ |
| $\tan\theta$ | $0$ | $\frac{1}{\sqrt{3}}$ | $1$ | $\sqrt{3}$ | undef | $0$ | undef | $0$ |

**Memory trick for $\sin$:** $0, \frac{\sqrt{1}}{2}, \frac{\sqrt{2}}{2}, \frac{\sqrt{3}}{2}, \frac{\sqrt{4}}{2}$ — the numerators go $0, 1, 2, 3, 4$ under the root.

### Essential Identities for Calculus

$$\sin^2\theta + \cos^2\theta = 1$$
$$\tan^2\theta + 1 = \sec^2\theta \quad \text{(from dividing by } \cos^2\theta\text{)}$$
$$1 + \cot^2\theta = \csc^2\theta \quad \text{(from dividing by } \sin^2\theta\text{)}$$

**Half-angle formulas** (essential for integration):
$$\sin^2\theta = \frac{1 - \cos 2\theta}{2} \qquad \cos^2\theta = \frac{1 + \cos 2\theta}{2}$$

**Product-to-sum formulas** (for advanced integration):
$$\sin A \cos B = \frac{1}{2}[\sin(A+B) + \sin(A-B)]$$

### Inverse Trig Functions

Since $\sin$, $\cos$, $\tan$ are not one-to-one on all of $\mathbb{R}$, their inverses are defined on restricted domains:

| Function | Domain of Inverse | Range of Inverse |
|----------|------------------|-----------------|
| $\arcsin x$ | $[-1, 1]$ | $[-\pi/2, \pi/2]$ |
| $\arccos x$ | $[-1, 1]$ | $[0, \pi]$ |
| $\arctan x$ | $\mathbb{R}$ | $(-\pi/2, \pi/2)$ |

$\arctan$ appears constantly in integration (Week 9+). Note that $\lim_{x\to\infty}\arctan x = \pi/2$ and $\lim_{x\to-\infty}\arctan x = -\pi/2$.

---

## 8. Summary Checklist

Before Lecture 3, you should be able to, without hesitation, do the following:

- [ ] Solve polynomial, rational, radical, exponential, and logarithmic equations
- [ ] Solve linear, polynomial, rational, and absolute value inequalities
- [ ] Write interval notation for any solution set
- [ ] Apply the sign chart method for polynomial/rational inequalities
- [ ] Simplify complex fractions by finding common denominators
- [ ] Rationalize numerators/denominators involving radicals
- [ ] Recite exact trig values at multiples of $\pi/6$ and $\pi/4$
- [ ] Apply all Pythagorean and angle-sum identities
- [ ] Use the half-angle formulas
- [ ] Find domains using all restriction types simultaneously

---

## Lecture 2 Exercises

1. Solve: $\dfrac{3}{x-1} - \dfrac{2}{x+1} = \dfrac{1}{x^2-1}$

2. Solve the inequality: $\dfrac{x^2 - 3x}{x+2} > 0$

3. Find all solutions to $|3x - 2| \geq 5$.

4. Simplify: $\dfrac{\dfrac{1}{x+h} - \dfrac{1}{x}}{h}$ and find its value as $h \to 0$ (informally — we make this precise next week).

5. Prove the identity: $\dfrac{\sin\theta}{1-\cos\theta} = \dfrac{1+\cos\theta}{\sin\theta}$

6. Given $\sin\theta = 3/5$ and $\theta$ is in Quadrant II, find $\cos\theta$, $\tan\theta$, $\sec\theta$, $\csc\theta$, $\cot\theta$.

7. Solve: $2\cos^2 x - \cos x - 1 = 0$ for $x \in [0, 2\pi)$.

8. **(Challenge)** Prove the triangle inequality: $|a+b| \leq |a| + |b|$ for all $a, b \in \mathbb{R}$.  

*Hint: Consider cases based on signs, or use $|x|^2 = x^2$.*

---


### Answers

**1.** Multiplying by $(x-1)(x+1)$: $3(x+1)-2(x-1)=1 \Rightarrow x+5=1 \Rightarrow \boxed{x=-4}$.
Not an excluded value ✓; both sides evaluate to $\tfrac1{15}$.

**2.** $\dfrac{x(x-3)}{x+2}>0$ with critical points $-2,0,3$. Test values give
$-18,\ +4,\ -\tfrac23,\ +\tfrac23$, so the solution is $\boxed{(-2,0)\cup(3,\infty)}$.
$x=-2$ is excluded as undefined; $x=0,3$ are excluded because the inequality is **strict**.

**3.** $3x-2\geq5$ **or** $3x-2\leq-5$, giving $\boxed{x\leq-1\ \text{ or }\ x\geq\tfrac73}$.
A $\geq$ absolute-value inequality yields a *union of two rays*; a $\leq$ one yields a single
interval. Swapping those is the standard error.

**4.** $\dfrac1h\left[\dfrac{1}{x+h}-\dfrac1x\right]=\dfrac{-h}{h\,x(x+h)}=\dfrac{-1}{x(x+h)}
\longrightarrow\boxed{-\dfrac{1}{x^2}}$

You have just computed the derivative of $1/x$ — before the word exists. Week 2 §3 does it again
with the limit made precise.

**5.** Cross-multiplying reduces the claim to $\sin^2\theta=(1-\cos\theta)(1+\cos\theta)=1-\cos^2\theta$,
the Pythagorean identity ✓. Valid where $\sin\theta\neq0$ and $\cos\theta\neq1$.

**6.** In QII, $\cos\theta<0$, so $\cos\theta=\boxed{-\tfrac45}$ and
$$\tan\theta=-\tfrac34,\qquad \sec\theta=-\tfrac54,\qquad \csc\theta=\tfrac53,\qquad \cot\theta=-\tfrac43$$
Only $\sin$ and $\csc$ are positive in QII — the signs come from the quadrant, not the algebra.

**7.** With $c=\cos x$: $2c^2-c-1=(2c+1)(c-1)=0$, so $c=1$ or $c=-\tfrac12$. On $[0,2\pi)$:
$$\boxed{x=0,\ \tfrac{2\pi}{3},\ \tfrac{4\pi}{3}}$$
All three verified to satisfy the equation to machine precision. Forgetting that $\cos x=-\tfrac12$
has **two** solutions in $[0,2\pi)$ is the usual omission.

**8.** Since $|t|^2=t^2$ for real $t$, and $ab\leq|ab|=|a||b|$:
$$|a+b|^2=(a+b)^2=a^2+2ab+b^2\leq|a|^2+2|a||b|+|b|^2=\left(|a|+|b|\right)^2$$
Both sides are non-negative, so taking square roots preserves the inequality. $\blacksquare$

Equality holds exactly when $ab=|ab|$ — when $a$ and $b$ share a sign, or one is zero.

*Next lecture: Lecture 3 — Exponentials, Logarithms, and Parametric Preview*  
*Reading: Stewart §1.4–1.5*
