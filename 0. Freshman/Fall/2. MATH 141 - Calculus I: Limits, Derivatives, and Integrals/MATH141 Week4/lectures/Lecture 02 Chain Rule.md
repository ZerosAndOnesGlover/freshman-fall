# MATH 141 · Calculus I
## Week 4 · Lecture 2 (Tuesday)
### The Chain Rule: Differentiating Composite Functions

**Date:** Tuesday 15 September 2026 · 11:00–11:50 · Week 4

---

**Reading:** Stewart §3.4 | Spivak Ch. 10 (§10.3)
**Problem Set 2 released today. Due: Wednesday, Week 3.**

---

## 1. The Problem with Composite Functions

The power, product, and quotient rules handle functions built from $+, -, \times, \div$. But what about:

$$y = \sin(x^2) \qquad y = \sqrt{x^3+1} \qquad y = (3x^2-5)^{10}$$

Each is a **composite function** — a function applied to a function. The chain rule handles exactly this case.

---

## 2. The Chain Rule

> **Theorem.** If $g$ is differentiable at $x$ and $f$ is differentiable at $g(x)$, then the composite $h(x) = f(g(x))$ is differentiable at $x$ and:
>
> $$h'(x) = f'(g(x))\cdot g'(x)$$

**In Leibniz notation:** if $y = f(u)$ and $u = g(x)$, then:

$$\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}$$

This reads like a fraction cancellation — $du$ "cancels." It's not literally a fraction, but the notation is deliberately designed to suggest this. It is one of Leibniz's great insights.

**In words:** "Derivative of the outside (evaluated at the inside), times derivative of the inside."

---

## 3. Proof of the Chain Rule

The naive proof attempt fails: write

$$\frac{h(x+k)-h(x)}{k} = \frac{f(g(x+k))-f(g(x))}{k} = \frac{f(g(x+k))-f(g(x))}{g(x+k)-g(x)}\cdot\frac{g(x+k)-g(x)}{k}$$

and take limits. The problem: $g(x+k)-g(x)$ might equal zero for some values of $k$ near 0, making the division invalid. The rigorous proof (using a clever reformulation of differentiability) is in Spivak Ch. 10. The essential idea is correct:

$$\frac{dy}{dx} = \lim_{k\to0}\frac{f(g(x+k))-f(g(x))}{k} = \left[\lim_{\Delta u\to0}\frac{f(u+\Delta u)-f(u)}{\Delta u}\right]\cdot\left[\lim_{k\to0}\frac{g(x+k)-g(x)}{k}\right] = f'(u)\cdot g'(x)$$

where $u = g(x)$ and $\Delta u = g(x+k)-g(x) \to 0$ as $k\to 0$. $\square$

---

## 4. Applying the Chain Rule — Systematic Method

**Step 1:** Identify the outer function $f$ and inner function $g$.
**Step 2:** Differentiate the outer function, leaving the inner function untouched.
**Step 3:** Multiply by the derivative of the inner function.

### Example 1 — Power of a function

$$y = (x^3 + 2x)^5$$

- Outer: $f(u) = u^5$, so $f'(u) = 5u^4$
- Inner: $g(x) = x^3+2x$, so $g'(x) = 3x^2+2$

$$\frac{dy}{dx} = 5(x^3+2x)^4 \cdot (3x^2+2)$$

### Example 2 — Trig of a function

$$y = \sin(x^2)$$

- Outer: $\sin(u)$, derivative $\cos(u)$
- Inner: $u = x^2$, derivative $2x$

$$\frac{dy}{dx} = \cos(x^2)\cdot 2x = 2x\cos(x^2)$$

Compare: $(\sin x)' = \cos x$. The $x^2$ inside changes everything.

### Example 3 — Square root of a function

$$y = \sqrt{3x^2-5} = (3x^2-5)^{1/2}$$

$$\frac{dy}{dx} = \frac{1}{2}(3x^2-5)^{-1/2}\cdot 6x = \frac{6x}{2\sqrt{3x^2-5}} = \frac{3x}{\sqrt{3x^2-5}}$$

### Example 4 — Chain rule within chain rule (nested)

$$y = \sin^3(x^2) = [\sin(x^2)]^3$$

Three layers: $y = u^3$, $u = \sin(v)$, $v = x^2$.

$$\frac{dy}{dx} = 3u^2 \cdot \cos(v) \cdot 2x = 3\sin^2(x^2)\cdot\cos(x^2)\cdot 2x = 6x\sin^2(x^2)\cos(x^2)$$

**General pattern for $[\sin(g(x))]^n$:**
$$\frac{d}{dx}[\sin^n(g(x))] = n\sin^{n-1}(g(x))\cdot\cos(g(x))\cdot g'(x)$$

---

## 5. The Generalized Power Rule

The most common chain rule application — power of a function:

$$\frac{d}{dx}[u^n] = nu^{n-1}\cdot\frac{du}{dx}$$

where $u = g(x)$ is any differentiable function. This is the power rule with the chain rule built in.

**Examples:**

$$\frac{d}{dx}(x^2+1)^{10} = 10(x^2+1)^9\cdot 2x = 20x(x^2+1)^9$$

$$\frac{d}{dx}\frac{1}{(3x+1)^4} = \frac{d}{dx}(3x+1)^{-4} = -4(3x+1)^{-5}\cdot 3 = \frac{-12}{(3x+1)^5}$$

---

## 6. Chain Rule + Product/Quotient Rules Together

Real functions require multiple rules simultaneously. Always identify the outermost structure first.

**Example:**

$$y = x^2\sin(x^3)$$

Outermost structure: a **product** of $x^2$ and $\sin(x^3)$. Use the product rule, then chain rule on $\sin(x^3)$:

$$\frac{dy}{dx} = 2x\cdot\sin(x^3) + x^2\cdot\cos(x^3)\cdot 3x^2 = 2x\sin(x^3) + 3x^4\cos(x^3)$$

**Example:**

$$y = \frac{\sin(2x)}{x^2+1}$$

Outermost: **quotient**. Apply quotient rule, then chain rule on $\sin(2x)$:

$$\frac{dy}{dx} = \frac{2\cos(2x)\cdot(x^2+1) - \sin(2x)\cdot 2x}{(x^2+1)^2}$$

---

## 7. Derivatives of Exponential Functions

**The natural exponential $e^x$:**

The number $e \approx 2.71828...$ is defined precisely so that:

$$\frac{d}{dx}[e^x] = e^x$$

The exponential function is its own derivative. This is the defining property of $e$, and it is the most important single fact about exponentials in calculus.

**With the chain rule:**
$$\frac{d}{dx}[e^{g(x)}] = e^{g(x)}\cdot g'(x)$$

**Examples:**
$$\frac{d}{dx}[e^{3x}] = 3e^{3x}$$
$$\frac{d}{dx}[e^{x^2}] = 2xe^{x^2}$$
$$\frac{d}{dx}[e^{\sin x}] = e^{\sin x}\cos x$$

**General base $a^x$:**
$$\frac{d}{dx}[a^x] = a^x\ln a$$

(Proved by writing $a^x = e^{x\ln a}$ and applying chain rule.)

---

## 8. Why the Chain Rule Is the Most Important Rule

The chain rule is not just one rule among several — it is the rule that makes all the others composable. Every function you will ever differentiate (outside of bare polynomials) requires the chain rule at some level.

**In ML and optimization:** The chain rule is **backpropagation**. A neural network is a composition of functions (layers). Backpropagation computes $\frac{\partial \text{Loss}}{\partial w}$ for every weight $w$ by applying the chain rule repeatedly backward through the composition. Concretely:

$$\frac{d\text{Loss}}{dw_1} = \frac{d\text{Loss}}{d\text{out}} \cdot \frac{d\text{out}}{d\text{hidden}} \cdot \frac{d\text{hidden}}{dw_1}$$

This is the chain rule. Automatic differentiation frameworks (PyTorch, JAX) are chain rule engines operating on computation graphs. Understanding the chain rule mathematically is the prerequisite to understanding how any gradient-based learning works.

---

## 9. Table of Derivative Rules — Complete So Far

| Function | Derivative | Notes |
|----------|-----------|-------|
| $c$ | $0$ | |
| $x^n$ | $nx^{n-1}$ | All real $n$ |
| $e^x$ | $e^x$ | |
| $a^x$ | $a^x\ln a$ | |
| $\sin x$ | $\cos x$ | |
| $\cos x$ | $-\sin x$ | |
| $\tan x$ | $\sec^2 x$ | |
| $\sec x$ | $\sec x\tan x$ | |
| $\csc x$ | $-\csc x\cot x$ | |
| $\cot x$ | $-\csc^2 x$ | |
| $[g(x)]^n$ | $n[g(x)]^{n-1}\cdot g'(x)$ | Chain + Power |
| $e^{g(x)}$ | $e^{g(x)}\cdot g'(x)$ | Chain + Exp |
| $\sin(g(x))$ | $\cos(g(x))\cdot g'(x)$ | Chain + Sin |
| $f(g(x))$ | $f'(g(x))\cdot g'(x)$ | General chain |

---

## 10. Common Errors

**1. Omitting the inner derivative.** $\frac{d}{dx}f(g(x)) = f'(g(x))\cdot\boldsymbol{g'(x)}$. The
missing $g'(x)$ is the single most common differentiation error in the entire course. Symptom:
$\frac{d}{dx}\sin(3x)$ reported as $\cos(3x)$ instead of $3\cos(3x)$.

**2. Differentiating the inner function in place.** $\frac{d}{dx}(x^2+1)^5$ is
$5(x^2+1)^4\cdot 2x$, **not** $5(2x)^4$. The outer function is evaluated *at the original inner
function*, unchanged.

**3. Losing count of the layers.** For $\sin^4(\cos(x^2))$ there are four: the fourth power, the
sine, the cosine, and $x^2$. Write them down before differentiating — the derivative is the product
of one factor per layer, so a missing factor means a missed layer.

**4. Chain rule *and* product rule.** $xe^{-x^2}$ needs both: product rule at the top level, chain
rule inside the exponential. Students who apply only one get a plausible-looking wrong answer.

**5. $\frac{d}{dx}e^{u} = e^{u}u'$, not $e^{u}$.** And $\frac{d}{dx}e^{x^2} = 2xe^{x^2}$, not
$x^2e^{x^2-1}$ — the power rule does not apply to a *constant* base.

---

## Lecture 3 Exercises

1. Differentiate using the chain rule:
   - (a) $y = (5x^3 - x)^7$
   - (b) $y = \cos(3x^2 + 1)$
   - (c) $y = e^{x^2 - 2x}$
   - (d) $y = \sqrt[3]{\sin x} = (\sin x)^{1/3}$
   - (e) $y = \sin^4(\cos(x^2))$ — identify all three layers before differentiating

2. Find $dy/dx$ for $y = xe^{-x^2}$.

3. Find the equation of the tangent line to $y = \sin(2x)$ at $x = \pi/4$.

4. **(Proof)** Derive $\dfrac{d}{dx}[\cos x] = -\sin x$ using the definition and the identity $\cos(x+h) = \cos x\cos h - \sin x\sin h$. Use the two special trig limits.

5. **(Application)** A population grows according to $P(t) = 1000e^{0.03t}$, where $t$ is years.
   - (a) Find $P'(t)$ — the instantaneous growth rate.
   - (b) How fast is the population growing at $t = 0$? At $t = 10$?
   - (c) Show that $P'(t) = 0.03\cdot P(t)$ — the growth rate is proportional to the current population. This is the defining equation of exponential growth.

6. **(Chain rule mechanics)** If $f(3) = 5$, $f'(3) = 2$, $g(x) = f(x^2 - 1)$, find $g'(2)$.

---

### Answers

All verified numerically (using **relative** error — several of these have magnitudes near $10^7$,
where an absolute-error check is meaningless).

**1.**
**(a)** $\boxed{7(5x^3-x)^6(15x^2-1)}$ &nbsp;&nbsp;
**(b)** $\boxed{-6x\sin(3x^2+1)}$ &nbsp;&nbsp;
**(c)** $\boxed{(2x-2)e^{x^2-2x}}$

**(d)** $\boxed{\tfrac13(\sin x)^{-2/3}\cos x = \dfrac{\cos x}{3\sqrt[3]{\sin^2 x}}}$

**(e)** Four layers — $u^4$, $\sin$, $\cos$, $x^2$ — so four factors:
$$\boxed{-8x\sin^3(\cos(x^2))\cdot\cos(\cos(x^2))\cdot\sin(x^2)}$$

**2.** Product rule with the chain rule inside:
$$\frac{d}{dx}\left[xe^{-x^2}\right]=e^{-x^2}+x\left(-2xe^{-x^2}\right)=\boxed{e^{-x^2}(1-2x^2)}$$

**3.** $y=\sin(2x)$, $y'=2\cos(2x)$. At $x=\pi/4$: $y=\sin(\pi/2)=1$ and
$y'=2\cos(\pi/2)=\boxed{0}$.

The tangent is the **horizontal** line $\boxed{y=1}$ — the curve is at its maximum there. A student
who reports a sloped line has evaluated $\cos$ in degrees or mis-substituted.

**4.** From the definition, using $\cos(x+h)=\cos x\cos h-\sin x\sin h$:
$$\frac{\cos(x+h)-\cos x}{h}=\cos x\cdot\frac{\cos h-1}{h}-\sin x\cdot\frac{\sin h}{h}$$
The two special limits give $\dfrac{\cos h-1}{h}\to0$ and $\dfrac{\sin h}{h}\to1$, so the whole
expression tends to $\cos x\cdot 0-\sin x\cdot 1=\boxed{-\sin x}$.

**5.** $P(t)=1000e^{0.03t}$.
- **(a)** $\boxed{P'(t)=30e^{0.03t}}$
- **(b)** $P'(0)=\boxed{30}$ people/year; $P'(10)=30e^{0.3}\approx\boxed{40.5}$ people/year
- **(c)** $P'(t)=30e^{0.03t}=0.03\left(1000e^{0.03t}\right)=\boxed{0.03\,P(t)}$ ✓

This is the differential equation $P'=kP$, whose *only* solutions are $P(0)e^{kt}$. Exponential
growth is not a curve that happens to fit — it is the unique consequence of "growth rate
proportional to current size", and the same equation governs radioactive decay ($k<0$), compound
interest, and unbounded population models.

**6.** $g(x)=f(x^2-1)$, so $g'(x)=f'(x^2-1)\cdot 2x$. At $x=2$: the inner value is
$2^2-1=3$, so
$$g'(2)=f'(3)\cdot 2(2)=2\cdot4=\boxed{8}$$
Note $f(3)=5$ is **not needed** — a deliberate distractor. The chain rule uses $f'$ at the inner
value, never $f$ itself.

---

*Reading for Week 3: Stewart §3.5 (implicit differentiation), §3.6 (derivatives of logarithms)*
*Problem Set 2 due next Wednesday — see assignment file.*
