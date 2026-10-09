# MATH 142 · Calculus II
## Week 2 · Lecture 2 (Tuesday)
### Completing the Square, and Making an Integral Fit a Pattern

*“The Simplicity of Figures depend upon the Simplicity of their Genesis and Ideas, and an Æquation is nothing else than a Description (either Geometrical or Mechanical) by which a Figure is generated and rendered more easy to the Conception.”* — Isaac Newton, *Arithmetica Universalis* (1707)

**Date:** Tuesday 2 February 2027 · 11:00–11:50 · Week 2

**Coursework:** 🔬 **Lab 1** Wed 3 Feb 15:00–16:50 · 📝 **PS 1** due Fri 5 Feb 17:00 · 📝 **PS 2** released Fri 5 Feb 12:00, due Fri 12 Feb 17:00 · 📊 **Quiz 3** Mon 8 Feb 11:00–11:15

---

**Reading:** Stewart §7.3 (continued), §7.4 opening | Apostol Ch. 6 §6.14

---

## 1. The Problem

Yesterday's three patterns all had a **bare $x^2$**: $\sqrt{a^2-x^2}$, $\sqrt{a^2+x^2}$, $\sqrt{x^2-a^2}$. Real integrals rarely arrive that way. They look like

$$\int\frac{dx}{x^2+2x+5} \qquad \int\frac{dx}{\sqrt{3-2x-x^2}} \qquad \int\frac{2x+3}{x^2+2x+5}\,dx$$

**None of these fits a pattern as written.** Today's technique is not new mathematics — it is the algebra that makes yesterday's patterns (and the Week 0 catalogue) applicable.

---

## 2. Completing the Square

Any quadratic can be written as a perfect square plus a constant:

$$x^2+bx+c = \left(x+\frac b2\right)^2 + \left(c - \frac{b^2}{4}\right)$$

**Then substitute $u = x + \tfrac b2$**, and the quadratic becomes $u^2 \pm a^2$ — a pattern.

### Example 1 — an arctangent in disguise

$$\int\frac{dx}{x^2+2x+5}$$

Complete the square: $x^2+2x+5 = (x+1)^2 + 4$. Let $u = x+1$, $du=dx$:

$$\int\frac{du}{u^2+4} = \frac12\arctan\frac u2 \implies \boxed{\frac12\arctan\frac{x+1}{2}+C}$$

*Verified symbolically.*

**No trigonometric substitution was needed** — the Week 0 catalogue entry $\int\frac{du}{u^2+a^2} = \frac1a\arctan\frac ua$ finished it. Completing the square was the whole technique.

### Example 2 — an arcsine in disguise

$$\int\frac{dx}{\sqrt{3-2x-x^2}}$$

**Factor out the $-1$ from the $x$ terms first** — this is the step students skip:

$$3-2x-x^2 = 3 - (x^2+2x) = 3 - \big[(x+1)^2 - 1\big] = 4 - (x+1)^2$$

With $u = x+1$:

$$\int\frac{du}{\sqrt{4-u^2}} = \arcsin\frac u2 \implies \boxed{\arcsin\frac{x+1}{2}+C}$$

*Verified symbolically.*

### Example 3 — split the numerator

$$\int\frac{2x+3}{x^2+2x+5}\,dx$$

When the numerator is linear and the denominator quadratic, **split the numerator into (a multiple of the denominator's derivative) plus (a constant)**.

Here $\frac{d}{dx}(x^2+2x+5) = 2x+2$, so write $2x+3 = (2x+2) + 1$:

$$\int\frac{2x+2}{x^2+2x+5}dx + \int\frac{dx}{x^2+2x+5}$$

- The **first** is the $\int\frac{g'}{g} = \ln|g|$ pattern: $\ln(x^2+2x+5)$.
- The **second** is Example 1: $\tfrac12\arctan\tfrac{x+1}{2}$.

$$\boxed{\int\frac{2x+3}{x^2+2x+5}dx = \ln(x^2+2x+5) + \frac12\arctan\frac{x+1}{2}+C}$$

*Verified symbolically.*

*(No absolute value is needed inside the logarithm: $(x+1)^2+4 > 0$ always.)*

> **This splitting move is essential for Lecture 3.** Every irreducible quadratic in a partial
> fraction decomposition ends up exactly here — a logarithm plus an arctangent.

---

## 3. The Decision Procedure for a Quadratic

Given $\int\frac{(\text{linear or constant})}{(\text{quadratic})}\,dx$ or the same under a square root:

1. **Is the numerator a multiple of the denominator's derivative?** → logarithm, done.
2. **If the numerator is linear**, split it: (multiple of $g'$) + (constant). Handle the pieces separately.
3. **For the constant piece, complete the square** and identify:

| After completing the square | Result |
|---|---|
| $\dfrac{1}{u^2+a^2}$ | $\dfrac1a\arctan\dfrac ua$ |
| $\dfrac{1}{\sqrt{a^2-u^2}}$ | $\arcsin\dfrac ua$ |
| $\dfrac{1}{\sqrt{u^2+a^2}}$ | $\ln\big|u+\sqrt{u^2+a^2}\big|$ |
| $\dfrac{1}{\sqrt{u^2-a^2}}$ | $\ln\big|u+\sqrt{u^2-a^2}\big|$ |
| $\dfrac{1}{u^2-a^2}$ | **partial fractions** — Lecture 3 |

*(All verified.)*

**Note the last row.** When the quadratic **factors**, do not complete the square — factor it and use tomorrow's method. Completing the square is for quadratics that *don't* factor over the reals.

### Example 4

$$\int\frac{dx}{x^2+6x+13} = \int\frac{dx}{(x+3)^2+4} = \boxed{\frac12\arctan\frac{x+3}{2}+C}$$

*Verified symbolically.*

---

## 4. Improper Fractions: Divide First

If the numerator's degree is **greater than or equal to** the denominator's, **polynomial long division comes first.** No other technique applies until it does.

$$\int\frac{x^3+x}{x-1}\,dx$$

Dividing: $\dfrac{x^3+x}{x-1} = x^2+x+2+\dfrac{2}{x-1}$. Then

$$\int\left(x^2+x+2+\frac{2}{x-1}\right)dx = \boxed{\frac{x^3}{3}+\frac{x^2}{2}+2x+2\ln|x-1|+C}$$

*Verified symbolically.*

> **This is a precondition for tomorrow.** Partial fraction decomposition **requires** a proper
> fraction — degree of numerator strictly less than degree of denominator. Applying it to an improper
> fraction produces nonsense, and the failure is not obvious. **Check the degrees first, every time.**

---

## 5. A Worked Example Combining Everything

$$\int\frac{\sqrt{x^2-9}}{x}\,dx, \qquad x>3$$

**Note the domain.** Yesterday's warning applies: this integral has different forms on $x>3$ and $x<-3$, and you must say which you are on.

Substitute $x = 3\sec\theta$, $dx = 3\sec\theta\tan\theta\,d\theta$, $\sqrt{x^2-9}=3\tan\theta$ with $\theta\in[0,\tfrac\pi2)$:

$$\int\frac{3\tan\theta}{3\sec\theta}\cdot3\sec\theta\tan\theta\,d\theta = 3\int\tan^2\theta\,d\theta$$

Using $\tan^2 = \sec^2-1$:

$$= 3\int(\sec^2\theta-1)\,d\theta = 3\tan\theta - 3\theta$$

**Back to $x$:** $\tan\theta = \tfrac{\sqrt{x^2-9}}{3}$ and $\sec\theta = \tfrac x3$, so $\theta = \operatorname{arcsec}\tfrac x3 = \arccos\tfrac 3x$.

$$\boxed{\int\frac{\sqrt{x^2-9}}{x}\,dx = \sqrt{x^2-9} - 3\arccos\frac3x + C \qquad (x>3)}$$

*Verified: with the domain declared, symbolic differentiation returns exactly $\frac{\sqrt{x^2-9}}{x}$; numerical differentiation at $x=3.5,\,5,\,9$ agrees to 16 significant figures.*

**Note the identity $\operatorname{arcsec} u = \arccos\frac1u$** — both forms are correct and textbooks differ. If your answer uses $\operatorname{arcsec}$ and the solutions use $\arccos$, you have not made an error.

---

## 6. Rationalizing Substitutions

One more move, for integrands containing an $n$-th root of a linear expression: **substitute the root itself.**

$$\int\frac{dx}{1+\sqrt x}$$

Let $u = \sqrt x$, so $x = u^2$ and $dx = 2u\,du$:

$$\int\frac{2u\,du}{1+u} = 2\int\frac{u}{1+u}\,du = 2\int\left(1 - \frac{1}{1+u}\right)du = 2u - 2\ln|1+u|$$

$$\boxed{= 2\sqrt x - 2\ln(1+\sqrt x)+C}$$

**The step $\frac{u}{1+u} = 1 - \frac1{1+u}$ is division** — §4's rule again, since the degrees are equal.

**Generally:** for $\sqrt[n]{ax+b}$, substitute $u = \sqrt[n]{ax+b}$. The integrand becomes rational, and rational integrands are always doable — which is tomorrow's theorem.

---

## 7. What To Take From This Lecture

1. **Complete the square** to turn any quadratic into $u^2\pm a^2$ and reach a pattern.
2. **Factor out the leading $-1$ first** when the $x^2$ term is negative.
3. **Split a linear numerator** into (a multiple of $g'$) + (constant): logarithm plus arctangent.
4. **If the quadratic factors, do not complete the square** — factor it, and use partial fractions.
5. **Divide first if the fraction is improper.** This is a precondition for tomorrow.
6. **State the domain** on any integral involving $\sqrt{x^2-a^2}$.

---

*Next: Wednesday — Partial Fractions, and a Theorem About Which Integrals Can Be Done*
