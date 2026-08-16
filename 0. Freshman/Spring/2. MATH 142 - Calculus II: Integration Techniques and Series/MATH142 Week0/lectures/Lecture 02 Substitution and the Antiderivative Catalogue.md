# MATH 142 · Calculus II
## Week 0 · Lecture 2 (Tuesday)
### Substitution and the Antiderivative Catalogue

**Date:** Tuesday 12 January 2027 · 11:00–11:50 · Week 0

---

**Reading:** Stewart §5.5 | Apostol Ch. 5 §5.7

---

## 1. Substitution Is the Chain Rule Backwards

You have exactly **one** integration technique so far, and this is it. Everything in Weeks 1–2 is a variation on it.

The chain rule says $\dfrac{d}{dx}F(g(x)) = F'(g(x))\,g'(x)$. Integrate both sides:

$$\int F'(g(x))\,g'(x)\,dx = F(g(x)) + C$$

Writing $u = g(x)$, so $du = g'(x)\,dx$:

$$\boxed{\int f(g(x))\,g'(x)\,dx = \int f(u)\,du}$$

**The technique is pattern recognition, not algebra.** You are looking for a composite function whose inner function's derivative is also present, up to a constant.

### The one question to ask

> **Is some chunk of this integrand the derivative of some other chunk?**

If yes, the inner chunk is your $u$. If no, substitution will not help and you need Week 1 or Week 2.

---

## 2. Worked Examples — Indefinite

### Example 1 — the archetype

$$\int x e^{x^2}\,dx$$

The composite is $e^{x^2}$, inner function $x^2$, whose derivative is $2x$. We have $x$, which is $2x$ up to the constant $\tfrac12$. Let $u=x^2$, $du=2x\,dx$, so $x\,dx = \tfrac12\,du$:

$$\int x e^{x^2}\,dx = \frac12\int e^u\,du = \frac12 e^u + C = \boxed{\frac{e^{x^2}}{2} + C}$$

*Verified: differentiating $\tfrac12 e^{x^2}$ gives $\tfrac12 e^{x^2}\cdot 2x = xe^{x^2}$. ✓*

### Example 2 — the disguised logarithm

$$\int \tan x\,dx = \int \frac{\sin x}{\cos x}\,dx$$

Let $u=\cos x$, $du = -\sin x\,dx$:

$$= -\int \frac{du}{u} = -\ln|u| + C = \boxed{-\ln|\cos x| + C} \;=\; \ln|\sec x| + C$$

**Whenever the numerator is the derivative of the denominator, the answer is a logarithm.** This pattern — $\int \frac{g'}{g} = \ln|g|$ — is worth memorising as a shape, because partial fractions in Week 2 is entirely an exercise in forcing integrands into it.

### Example 3 — nested logarithm

$$\int \frac{dx}{x\ln x}$$

Let $u=\ln x$, $du = \tfrac{dx}{x}$: the integral becomes $\int\frac{du}{u} = \ln|u|+C = \boxed{\ln|\ln x| + C}$.

*Verified symbolically.*

---

## 3. Definite Integrals: Change the Limits

This is where marks are lost. With $u=g(x)$,

$$\boxed{\int_a^b f(g(x))\,g'(x)\,dx = \int_{g(a)}^{g(b)} f(u)\,du}$$

**The limits are $x$-values on the left and $u$-values on the right.** You have two legitimate options:

1. **Change the limits** (recommended) — then never return to $x$.
2. **Keep the limits in $x$**, find the antiderivative in $u$, substitute back to $x$, *then* evaluate.

What you may **not** do is find an antiderivative in $u$ and evaluate it at the original $x$-limits. That is the single most common error on this topic.

### Example 4

$$\int_0^2 x\sqrt{4-x^2}\,dx$$

Let $u = 4-x^2$, $du = -2x\,dx$, so $x\,dx = -\tfrac12 du$. Limits: $x=0 \Rightarrow u=4$; $x=2 \Rightarrow u=0$.

$$= -\frac12\int_{4}^{0} \sqrt u\,du = \frac12\int_0^4 \sqrt u\,du = \frac12\cdot\left[\frac{2}{3}u^{3/2}\right]_0^4 = \frac13\cdot 8 = \boxed{\frac83}$$

*Verified symbolically: $8/3$.*

Note the limits **reversed** ($4 \to 0$), and flipping them back cancelled the minus sign. Watch for this.

### Example 5

$$\int_0^{\pi/4}\tan x\,dx = \big[-\ln|\cos x|\big]_0^{\pi/4} = -\ln\frac{\sqrt2}{2} + \ln 1 = \ln\sqrt2 = \boxed{\frac{\ln 2}{2}}$$

*Verified symbolically.*

---

## 4. Symmetry: The Free Answer

If $f$ is **odd** ($f(-x)=-f(x)$): $\displaystyle\int_{-a}^{a} f(x)\,dx = 0$.

If $f$ is **even** ($f(-x)=f(x)$): $\displaystyle\int_{-a}^{a} f(x)\,dx = 2\int_0^a f(x)\,dx$.

### Example 6

$$\int_{-2}^{2} x^3\cos x\,dx = 0$$

because $x^3$ is odd, $\cos x$ is even, and odd × even = odd. *Verified symbolically: $0$.*

**Always check symmetry before integrating.** This integral has no elementary-looking route by substitution, and requires integration by parts three times if you attack it directly — or one line if you look at it first. On an exam, that is the difference between finishing and not.

---

## 5. The Catalogue

These are the antiderivatives you are expected to know cold. Anything not on this list must be *derived*.

| $f(x)$ | $\int f(x)\,dx$ | | $f(x)$ | $\int f(x)\,dx$ |
|---|---|---|---|---|
| $x^n,\ n\neq-1$ | $\dfrac{x^{n+1}}{n+1}$ | | $\sec^2 x$ | $\tan x$ |
| $\dfrac1x$ | $\ln\lvert x\rvert$ | | $\csc^2 x$ | $-\cot x$ |
| $e^x$ | $e^x$ | | $\sec x\tan x$ | $\sec x$ |
| $a^x$ | $\dfrac{a^x}{\ln a}$ | | $\csc x\cot x$ | $-\csc x$ |
| $\sin x$ | $-\cos x$ | | $\dfrac{1}{\sqrt{1-x^2}}$ | $\arcsin x$ |
| $\cos x$ | $\sin x$ | | $\dfrac{1}{1+x^2}$ | $\arctan x$ |
| $\tan x$ | $-\ln\lvert\cos x\rvert$ | | $\dfrac{1}{\lvert x\rvert\sqrt{x^2-1}}$ | $\operatorname{arcsec} x$ |
| $\cot x$ | $\ln\lvert\sin x\rvert$ | | $\sinh x$ | $\cosh x$ |
| $\sec x$ | $\ln\lvert\sec x+\tan x\rvert$ | | $\cosh x$ | $\sinh x$ |
| $\csc x$ | $-\ln\lvert\csc x+\cot x\rvert$ | | | |

*(Every entry omits the $+C$.)*

### The $\sec x$ entry deserves a comment

$\int \sec x\,dx = \ln|\sec x + \tan x| + C$ is the one nobody derives on the spot — the standard derivation multiplies by $\frac{\sec x + \tan x}{\sec x+\tan x}$, which is a trick with no motivation other than that it works.

**Here is the useful lesson.** Asked for this integral, a computer algebra system returns

$$\tfrac12\ln(1+\sin x) - \tfrac12\ln(1-\sin x)$$

which looks nothing like the textbook answer. Both are correct — they differ by a constant, and each differentiates to $\sec x$. **Differentiating the textbook form gives exactly $\sec x$**, which settles it in one line.

This is worth internalising now:

> **An antiderivative is not unique in *form*, only up to a constant.** When your answer disagrees with the back of the book, differentiate both. Usually you are both right.

And its corollary, which is the rule from the syllabus:

> **Check by differentiating.** It costs thirty seconds and catches nearly every error you will make in Weeks 0–5.

---

## 6. When Substitution Fails

Substitution handles integrands with a visible inner function and its derivative. It does **nothing** for:

$$\int x e^{x}\,dx \qquad \int \ln x\,dx \qquad \int \frac{dx}{x^2-1} \qquad \int \sqrt{1-x^2}\,dx$$

- The first two need **integration by parts** — Week 1.
- The third needs **partial fractions** — Week 2.
- The fourth needs **trigonometric substitution** — Week 2.

And then there is:

$$\int e^{-x^2}\,dx$$

for which **nothing works, ever**, because no elementary antiderivative exists. Week 10 is the answer to that one.

**Recognising which category an integral falls into is the actual skill of Weeks 1–2**, and it is worth more marks than executing any single technique.

---

## 7. What To Take From This Lecture

1. **Substitution is the chain rule backwards.** Look for an inner function whose derivative is present.
2. **$\int \frac{g'}{g} = \ln|g|$** is the shape behind an enormous number of integrals.
3. **On definite integrals, change the limits** — and if you don't, convert back to $x$ before evaluating.
4. **Check symmetry first.** It is sometimes the whole problem.
5. **Check every antiderivative by differentiating it.**

---

*Next: Wednesday — Area, Average Value, and Net Change*
