# MATH 141 — Calculus I
## Week 3 Reference Sheet
### The Derivative — Definition and Rules

---

## The Definition (Two Forms)

$$f'(a) = \lim_{h\to0}\frac{f(a+h)-f(a)}{h} \qquad \text{or} \qquad f'(a)=\lim_{x\to a}\frac{f(x)-f(a)}{x-a}$$

**Tangent line at $(a, f(a))$:** $\quad y = f(a) + f'(a)(x-a)$

---

## Complete Differentiation Rule Table

| Function | Derivative | Notes |
|----------|-----------|-------|
| $c$ | $0$ | Constant rule |
| $x^n$ | $nx^{n-1}$ | All real $n$ |
| $cf(x)$ | $cf'(x)$ | Constant multiple |
| $f\pm g$ | $f'\pm g'$ | Sum/difference |
| $fg$ | $f'g+fg'$ | Product rule |
| $f/g$ | $(f'g-fg')/g^2$ | Quotient rule |
| $f(g(x))$ | $f'(g(x))\cdot g'(x)$ | **Chain rule** |
| $e^x$ | $e^x$ | |
| $a^x$ | $a^x\ln a$ | |
| $\ln x$ | $1/x$ | (Next week) |
| $\sin x$ | $\cos x$ | |
| $\cos x$ | $-\sin x$ | |
| $\tan x$ | $\sec^2 x$ | |
| $\sec x$ | $\sec x\tan x$ | |
| $\csc x$ | $-\csc x\cot x$ | |
| $\cot x$ | $-\csc^2 x$ | |

---

## Chain Rule — Key Pattern

$$\frac{d}{dx}[f(g(x))] = \underbrace{f'(g(x))}_{\text{outer deriv.}} \cdot \underbrace{g'(x)}_{\text{inner deriv.}}$$

**Leibniz form:** $\dfrac{dy}{dx} = \dfrac{dy}{du}\cdot\dfrac{du}{dx}$

**Most common cases:**

$$\frac{d}{dx}[u^n] = nu^{n-1}u' \qquad \frac{d}{dx}[e^u] = e^u u' \qquad \frac{d}{dx}[\sin u] = \cos u\cdot u'$$

---

## Differentiability — Failure Modes

| Failure type | Example | $f$ continuous? |
|-------------|---------|----------------|
| Corner/kink | $|x|$ at $x=0$ | ✅ Yes |
| Cusp | $x^{2/3}$ at $x=0$ | ✅ Yes |
| Vertical tangent | $x^{1/3}$ at $x=0$ | ✅ Yes |
| Discontinuity | Any jump/removable | ❌ No |

**Key theorem:** Differentiable $\Rightarrow$ Continuous.
**Converse is FALSE:** Continuous $\not\Rightarrow$ Differentiable.

---

## Notation Guide

All of these mean the same thing:

$$f'(x) = y' = \frac{dy}{dx} = \frac{d}{dx}[f(x)] = Df(x)$$

Evaluated at $x = a$:

$$f'(a) = \left.\frac{dy}{dx}\right|_{x=a}$$

---

## Physical Interpretation

| Quantity | Mathematical meaning |
|---------|---------------------|
| $s(t)$ | Position |
| $s'(t) = v(t)$ | Velocity (instantaneous) |
| $v'(t) = s''(t) = a(t)$ | Acceleration |
| $f'(x) > 0$ | $f$ is increasing at $x$ |
| $f'(x) < 0$ | $f$ is decreasing at $x$ |
| $f'(x) = 0$ | $f$ has horizontal tangent at $x$ |
| $f''(x) > 0$ | $f$ is concave up at $x$ |
| $f''(x) < 0$ | $f$ is concave down at $x$ |

---

## Common Errors

| ❌ Wrong | ✅ Right |
|---------|---------|
| $(fg)' = f'g'$ | $(fg)' = f'g+fg'$ |
| $(f/g)' = f'/g'$ | Use quotient rule |
| $\frac{d}{dx}[e^{x^2}] = e^{x^2}$ | $= 2xe^{x^2}$ (chain rule!) |
| $\frac{d}{dx}[\sin(3x)] = \cos(3x)$ | $= 3\cos(3x)$ (chain rule!) |
| $\frac{d}{dx}[(x^2+1)^5] = 5(x^2+1)^4$ | $= 10x(x^2+1)^4$ (chain rule!) |

**The chain rule is the most commonly forgotten rule.** If the argument of a function is anything other than bare $x$, the chain rule applies.

---

## Week 3 Schedule

| Day | Event | Topic |
|-----|-------|-------|
| Monday | **Quiz 03** + Lecture 1 | Derivative definition, difference quotient |
| Tuesday | Lecture 2 | Power, product, quotient rules; trig derivatives |
| Friday | **Lab 03** | Secant→tangent, numerical differentiation, $e$ |
| Wednesday | Lecture 3 + **PS2 released** | Chain rule, exponential derivatives |

**Next week:** Implicit differentiation, logarithmic differentiation, and inverse trig derivatives.
