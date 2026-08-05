# MATH 142 · Calculus II
## Week 2 · Reference Sheet
### Trigonometric Substitution; Partial Fractions

---

## Trigonometric Substitution

| Expression | Substitute | Identity used | Radical becomes | Range of $\theta$ |
|---|---|---|---|---|
| $\sqrt{a^2-x^2}$ | $x=a\sin\theta$ | $1-\sin^2=\cos^2$ | $a\cos\theta$ | $[-\tfrac\pi2,\tfrac\pi2]$ |
| $\sqrt{a^2+x^2}$ | $x=a\tan\theta$ | $1+\tan^2=\sec^2$ | $a\sec\theta$ | $(-\tfrac\pi2,\tfrac\pi2)$ |
| $\sqrt{x^2-a^2}$ | $x=a\sec\theta$ | $\sec^2-1=\tan^2$ | $a\tan\theta$ | $[0,\tfrac\pi2)\cup[\pi,\tfrac{3\pi}2)$ |

**The range is what lets you drop the absolute value.** State it.

### Reference triangles

| Substitution | Opposite | Adjacent | Hypotenuse |
|---|---|---|---|
| $x=a\sin\theta$ | $x$ | $\sqrt{a^2-x^2}$ | $a$ |
| $x=a\tan\theta$ | $x$ | $a$ | $\sqrt{a^2+x^2}$ |
| $x=a\sec\theta$ | $\sqrt{x^2-a^2}$ | $a$ | $x$ |

### Procedure

1. Identify the pattern
2. Substitute; compute $dx$
3. Simplify the radical (justify dropping $|\cdot|$)
4. Integrate — **it is a Week 1 trigonometric integral**
5. Convert back with the triangle — **or change the limits at step 2 and skip this**

**On definite integrals, change the limits.** Less work, less risk.

### Standard results

| Integral | Answer |
|---|---|
| $\int\sqrt{a^2-x^2}\,dx$ | $\tfrac{a^2}{2}\arcsin\tfrac xa + \tfrac{x\sqrt{a^2-x^2}}{2}$ |
| $\int\dfrac{dx}{(x^2+a^2)^{3/2}}$ | $\dfrac{x}{a^2\sqrt{x^2+a^2}}$ |
| $\int\dfrac{dx}{\sqrt{x^2-a^2}}$ | $\ln\big\lvert x+\sqrt{x^2-a^2}\big\rvert$ |
| $\int\dfrac{dx}{\sqrt{x^2+a^2}}$ | $\ln\big(x+\sqrt{x^2+a^2}\big)$ |
| $\int\dfrac{dx}{x^2\sqrt{x^2+a^2}}$ | $-\dfrac{\sqrt{x^2+a^2}}{a^2x}$ |

*(all omit $+C$; all verified)*

---

## Completing the Square

$$x^2+bx+c = \left(x+\frac b2\right)^2+\left(c-\frac{b^2}{4}\right)$$

**Factor out a leading $-1$ first** if the $x^2$ coefficient is negative.

| After completing the square | Result |
|---|---|
| $\dfrac{1}{u^2+a^2}$ | $\dfrac1a\arctan\dfrac ua$ |
| $\dfrac{1}{\sqrt{a^2-u^2}}$ | $\arcsin\dfrac ua$ |
| $\dfrac{1}{\sqrt{u^2\pm a^2}}$ | $\ln\big\lvert u+\sqrt{u^2\pm a^2}\big\rvert$ |
| $\dfrac{1}{u^2-a^2}$ | **factor it — use partial fractions** |

**If the quadratic factors, don't complete the square.**

### Splitting a linear numerator

Write (numerator) = $k\cdot$(derivative of denominator) + (constant):

$$\int\frac{2x+3}{x^2+2x+5}dx = \underbrace{\int\frac{2x+2}{x^2+2x+5}dx}_{\ln(x^2+2x+5)} + \underbrace{\int\frac{dx}{(x+1)^2+4}}_{\frac12\arctan\frac{x+1}{2}}$$

**Logarithm + arctangent.** Every irreducible quadratic ends here.

---

## Rationalizing Substitutions

For $\sqrt[n]{ax+b}$ in the integrand, substitute $u = \sqrt[n]{ax+b}$ — the integrand becomes **rational**, hence always doable.

$$\int\frac{dx}{1+\sqrt x} \overset{u=\sqrt x}{=} 2\int\frac{u\,du}{1+u} = 2\sqrt x - 2\ln(1+\sqrt x)+C$$

---

## Partial Fractions

### Preconditions

1. **Proper fraction** — if $\deg P\ge\deg Q$, **divide first**. Not optional.
2. **Denominator factored completely** into linear factors and irreducible quadratics.

### The four cases

| Factor in $Q$ | Contributes |
|---|---|
| $(x-r)$ | $\dfrac{A}{x-r}$ |
| $(x-r)^k$ | $\dfrac{A_1}{x-r}+\dfrac{A_2}{(x-r)^2}+\cdots+\dfrac{A_k}{(x-r)^k}$ |
| $(x^2+bx+c)$ irreducible | $\dfrac{Ax+B}{x^2+bx+c}$ |
| $(x^2+bx+c)^k$ | $\dfrac{A_1x+B_1}{x^2+bx+c}+\cdots+\dfrac{A_kx+B_k}{(x^2+bx+c)^k}$ |

**Repeated factors need every power. Irreducible quadratics need a linear numerator.**

### Finding the constants

- **Cover-up (Heaviside)** — for a distinct linear factor $(x-r)$: multiply by it, set $x=r$.
  Also gives the **highest** power of a repeated factor.
- **Equate coefficients** — clear denominators, match powers of $x$. Always works.

### Integrating the pieces

| Piece | Integral |
|---|---|
| $\dfrac{A}{x-r}$ | $A\ln\lvert x-r\rvert$ |
| $\dfrac{A}{(x-r)^k},\ k\ge2$ | $\dfrac{-A}{(k-1)(x-r)^{k-1}}$ |
| $\dfrac{Ax+B}{x^2+bx+c}$ | split → logarithm + arctangent |

### **Always recombine to check.**

---

## The Theorem

> **Every rational function has an elementary antiderivative**, and it is built only from
> **polynomials, logarithms, arctangents, and rational functions.**

**Why:** division handles the improper part; the Fundamental Theorem of Algebra guarantees the factorisation; partial fractions splits it; every piece is on the short list. Each step always succeeds.

| | Rational functions | $e^{-x^2}$, $\frac{\sin x}{x}$, $\sqrt{1+x^3}$ |
|---|---|---|
| Elementary antiderivative? | **Always** | **Never** |
| Method | An algorithm | None exists |

**Where each answer-type comes from:** distinct linear → logarithm; repeated linear → rational function; irreducible quadratic → logarithm **and** arctangent.

---

## The Dalzell Integral (Lab 2)

$$\int_0^1\frac{x^4(1-x)^4}{1+x^2}\,dx = \frac{22}{7}-\pi = 0.00126448926734962\ldots$$

Division gives $\dfrac{x^4(1-x)^4}{1+x^2} = x^6-4x^5+5x^4-4x^2+4-\dfrac{4}{1+x^2}$.

**The integrand is positive on $(0,1)$, so $\frac{22}{7} > \pi$.**

Bounding with $1\le1+x^2\le2$ and $\int_0^1x^4(1-x)^4dx = \frac1{630}$:

$$\frac{1979}{630} \le \pi \le \frac{3959}{1260} \qquad\text{i.e.}\qquad 3.14126984 \le \pi \le 3.14206349$$

*(all verified)*

---

## Two Habits

1. **Differentiate every antiderivative.**
2. **Declare your domain.** $\int\frac{\sqrt{x^2-9}}{x}dx$ and $\int\frac{dx}{(x^2-4)^{3/2}}$ both return multi-branch `Piecewise` expressions from a CAS given no domain, and clean one-line answers given $x>3$ / $x>2$.

---

*MATH 142 · Week 2 · Reference Sheet*
