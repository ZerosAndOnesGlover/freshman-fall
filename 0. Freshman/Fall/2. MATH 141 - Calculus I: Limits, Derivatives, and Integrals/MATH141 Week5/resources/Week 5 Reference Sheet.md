# MATH 141 · Calculus I
## Week 5 Reference Sheet
### Implicit Differentiation · Logarithms · Inverse Trig · Related Rates

---

## Implicit Differentiation — The Rule

Whenever a term contains $y$, differentiate it with respect to $x$ and **multiply by $dy/dx$** (chain rule, since $y$ is a function of $x$):

$$\frac{d}{dx}[y^n] = ny^{n-1}\frac{dy}{dx} \qquad \frac{d}{dx}[\sin y] = \cos y\cdot\frac{dy}{dx} \qquad \frac{d}{dx}[e^y] = e^y\frac{dy}{dx}$$

**Procedure:**
1. Differentiate both sides w.r.t. $x$, applying chain rule on every $y$-term
2. Collect all $dy/dx$ terms on one side
3. Factor and solve for $dy/dx$

**Shortcut formula:** For $F(x,y) = 0$:
$$\frac{dy}{dx} = -\frac{\partial F/\partial x}{\partial F/\partial y}$$

---

## Logarithm Derivatives

| Function | Derivative |
|----------|-----------|
| $\ln x$ | $\dfrac{1}{x}$ |
| $\ln\|x\|$ | $\dfrac{1}{x}$ (all $x\neq0$) |
| $\ln(g(x))$ | $\dfrac{g'(x)}{g(x)}$ |
| $\log_a x$ | $\dfrac{1}{x\ln a}$ |
| $\log_a(g(x))$ | $\dfrac{g'(x)}{g(x)\ln a}$ |

**Log laws for simplification before differentiating:**
$$\ln(AB) = \ln A + \ln B \qquad \ln\!\left(\frac{A}{B}\right) = \ln A - \ln B \qquad \ln(A^n) = n\ln A$$

---

## Logarithmic Differentiation — When to Use It

Use when $y = [f(x)]^{g(x)}$ — variable base **and** variable exponent.

**Steps:** Take $\ln$ of both sides → differentiate implicitly → multiply both sides by $y$ → substitute $y$ back.

$$y = u^v \implies \ln y = v\ln u \implies \frac{y'}{y} = v'\ln u + v\cdot\frac{u'}{u} \implies y' = y\!\left(v'\ln u + \frac{vu'}{u}\right)$$

---

## Inverse Trig Derivatives — Complete Table

| Function | Derivative | Domain |
|----------|-----------|--------|
| $\arcsin x$ | $\dfrac{1}{\sqrt{1-x^2}}$ | $(-1,1)$ |
| $\arccos x$ | $\dfrac{-1}{\sqrt{1-x^2}}$ | $(-1,1)$ |
| $\arctan x$ | $\dfrac{1}{1+x^2}$ | $\mathbb{R}$ |
| $\text{arccot}\,x$ | $\dfrac{-1}{1+x^2}$ | $\mathbb{R}$ |
| $\text{arcsec}\,x$ | $\dfrac{1}{|x|\sqrt{x^2-1}}$ | $|x|>1$ |
| $\text{arccsc}\,x$ | $\dfrac{-1}{|x|\sqrt{x^2-1}}$ | $|x|>1$ |

**With chain rule:** $\dfrac{d}{dx}[\arctan(g(x))] = \dfrac{g'(x)}{1+[g(x)]^2}$, etc.

**Key identities** (derivatives sum to zero):
$$\arcsin x + \arccos x = \frac{\pi}{2} \qquad \arctan x + \text{arccot}\,x = \frac{\pi}{2}$$

---

## Related Rates — Problem-Solving Template

**Setup:**
1. Draw a diagram; label all changing quantities as variables
2. State given rate(s) and wanted rate, with signs (negative = decreasing)
3. Write one equation relating the variables using geometry

**Execution:**
4. Differentiate both sides w.r.t. $t$ (chain rule throughout)
5. Substitute given numerical values (ONLY after differentiating)
6. Solve for the unknown rate

> ⚠️ Never substitute values before differentiating.

**Common geometric formulas:**

| Shape | Formula |
|-------|---------|
| Circle | $A = \pi r^2$, $C = 2\pi r$ |
| Sphere | $V = \frac{4}{3}\pi r^3$, $SA = 4\pi r^2$ |
| Cylinder | $V = \pi r^2 h$ |
| Cone | $V = \frac{1}{3}\pi r^2 h$ |
| Right triangle | $a^2 + b^2 = c^2$ |
| Trig ratio | $\tan\theta = \text{opp}/\text{adj}$ |

---

## Full Derivative Table — Weeks 1–3

| Function | Derivative |
|----------|-----------|
| $x^n$ | $nx^{n-1}$ |
| $e^x$ | $e^x$ |
| $a^x$ | $a^x \ln a$ |
| $\ln x$ | $1/x$ |
| $\log_a x$ | $1/(x\ln a)$ |
| $\sin x$ | $\cos x$ |
| $\cos x$ | $-\sin x$ |
| $\tan x$ | $\sec^2 x$ |
| $\sec x$ | $\sec x\tan x$ |
| $\csc x$ | $-\csc x\cot x$ |
| $\cot x$ | $-\csc^2 x$ |
| $\arcsin x$ | $1/\sqrt{1-x^2}$ |
| $\arccos x$ | $-1/\sqrt{1-x^2}$ |
| $\arctan x$ | $1/(1+x^2)$ |

All combined with: constant multiple, sum, product, quotient, and chain rules.

---

## Week 5 Schedule

| Day | Event | Topic |
|-----|-------|-------|
| Monday | **Quiz 05** + Lecture 1 | Implicit differentiation |
| Tuesday | Lecture 2 | Log derivatives, log diff., inverse trig |
| Wednesday | Lecture 3 + **PS 5 released** (12:00) | Related rates |
| Friday | **Lab 05** | Implicit curves, log exploration, related rates simulation |

**Next week:** Extrema, Rolle's Theorem, Mean Value Theorem.
