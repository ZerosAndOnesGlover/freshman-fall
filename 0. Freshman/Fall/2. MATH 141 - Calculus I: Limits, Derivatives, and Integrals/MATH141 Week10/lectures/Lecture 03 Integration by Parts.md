# MATH 141 · Calculus I
## Week 10 · Lecture 3 (Wednesday)
### Integration by Parts

---

**Reading:** Stewart §7.1 | Spivak Ch. 19 (Integration Techniques)
**Problem Set 10 released today. Due: Wednesday, Week 8.**

---

## 1. Motivation — When Substitution Fails

Consider $\displaystyle\int x\cos x\,dx$ or $\displaystyle\int \ln x\,dx$ or $\displaystyle\int xe^x\,dx$.

None of these fit the substitution pattern $f(g(x))g'(x)$ — there's no clean "inside function whose derivative appears elsewhere." We need a fundamentally different technique, and — just as the Substitution Rule was the Chain Rule read backward — **Integration by Parts is the Product Rule read backward.**

---

## 2. Deriving the Integration by Parts Formula

Recall the Product Rule:
$$\frac{d}{dx}[u(x)v(x)] = u'(x)v(x)+u(x)v'(x)$$

Integrate both sides with respect to $x$:

$$u(x)v(x) = \int u'(x)v(x)\,dx + \int u(x)v'(x)\,dx$$

Rearrange:

$$\int u(x)v'(x)\,dx = u(x)v(x) - \int u'(x)v(x)\,dx$$

**Using differential notation** ($du=u'(x)dx$, $dv=v'(x)dx$):

> **Integration by Parts Formula:**
> $$\int u\,dv = uv - \int v\,du$$

**In words:** to integrate a product, differentiate one factor ($u$) and integrate the other ($dv$), then subtract the integral of the new product $v\,du$.

---

## 3. The Method — Step by Step

1. **Identify $u$ and $dv$** in the integrand (the integrand should be expressible as $u\cdot dv$)
2. **Compute $du$** (differentiate $u$) and **compute $v$** (integrate $dv$ — you only need ONE antiderivative, so omit "+C" at this stage)
3. **Apply the formula:** $\displaystyle\int u\,dv = uv - \int v\,du$
4. **Evaluate the new integral** $\displaystyle\int v\,du$ — hopefully simpler than the original

**The entire skill of this technique is choosing $u$ and $dv$ wisely.**

---

## 4. The LIATE Heuristic for Choosing $u$

A helpful (not universal, but very reliable) mnemonic for choosing which factor should be $u$:

$$\textbf{L-I-A-T-E}$$

| Priority | Type | Examples |
|----------|------|----------|
| 1 (highest) | **L**ogarithmic | $\ln x$, $\log_a x$ |
| 2 | **I**nverse trig | $\arcsin x$, $\arctan x$ |
| 3 | **A**lgebraic | $x^n$, polynomials |
| 4 | **T**rigonometric | $\sin x$, $\cos x$ |
| 5 (lowest) | **E**xponential | $e^x$, $a^x$ |

**Choose $u$ to be whichever function type appears earliest (highest priority) in this list.** The remaining factor (with its $dx$) becomes $dv$.

**Why this works, intuitively:** logarithms and inverse trig functions don't simplify when integrated (they often get MORE complex), but they simplify beautifully when *differentiated*. Exponentials and trig functions are the opposite — easy to integrate repeatedly, and don't change character when integrated. So we differentiate the "hard to integrate, easy to differentiate" factor, and integrate the "easy either way" factor.

---

## 5. Worked Examples

### Example 1 — Algebraic × Trigonometric

$$\int x\cos x\,dx$$

By LIATE: Algebraic beats Trigonometric, so $u=x$ (Algebraic), $dv=\cos x\,dx$ (Trigonometric).

$$u=x \quad dv=\cos x\,dx$$
$$du=dx \quad v=\sin x$$

$$\int x\cos x\,dx = x\sin x - \int\sin x\,dx = x\sin x-(-\cos x)+C = x\sin x+\cos x+C$$

**Verify by differentiating:** $\dfrac{d}{dx}[x\sin x+\cos x] = \sin x+x\cos x-\sin x = x\cos x$ ✓

### Example 2 — Algebraic × Exponential

$$\int xe^x\,dx$$

By LIATE: Algebraic beats Exponential, so $u=x$, $dv=e^x\,dx$.

$$u=x \quad dv=e^x\,dx$$
$$du=dx \quad v=e^x$$

$$\int xe^x\,dx = xe^x-\int e^x\,dx = xe^x-e^x+C = e^x(x-1)+C$$

### Example 3 — Logarithmic Alone (the "trick" $dv=dx$)

$$\int \ln x\,dx$$

There's only one factor! Treat the integral as $\displaystyle\int(\ln x)\cdot1\,dx$, so $u=\ln x$ (Logarithmic — highest priority), $dv=dx$.

$$u=\ln x \quad dv=dx$$
$$du=\frac1x dx \quad v=x$$

$$\int\ln x\,dx = x\ln x-\int x\cdot\frac1x\,dx = x\ln x-\int1\,dx = x\ln x-x+C$$

**This "single-factor" trick works for all inverse functions** — $\arcsin x$, $\arctan x$, etc. — since they too have no elementary antiderivative on their own, but their derivatives are simple algebraic expressions.

### Example 4 — Inverse Trig

$$\int \arctan x\,dx$$

$u=\arctan x$, $dv=dx$.

$$du=\frac{1}{1+x^2}dx \quad v=x$$

$$\int\arctan x\,dx = x\arctan x-\int\frac{x}{1+x^2}\,dx$$

The remaining integral requires substitution ($w=1+x^2$, $dw=2x\,dx$):

$$\int\frac{x}{1+x^2}\,dx = \frac12\ln(1+x^2)+C$$

$$\int\arctan x\,dx = x\arctan x-\frac12\ln(1+x^2)+C$$

*(This confirms the result derived by a different method in Week 3's Problem Set, Problem C1(c) — a nice consistency check across techniques.)*

---

## 6. Repeated Integration by Parts

Some integrals require applying the technique **more than once**.

### Example 5

$$\int x^2e^x\,dx$$

$u=x^2$, $dv=e^x\,dx$. $du=2x\,dx$, $v=e^x$.

$$= x^2e^x-\int 2xe^x\,dx = x^2e^x-2\int xe^x\,dx$$

The remaining integral $\displaystyle\int xe^x\,dx$ was solved in Example 2: $xe^x-e^x+C$.

$$\int x^2e^x\,dx = x^2e^x-2(xe^x-e^x)+C = x^2e^x-2xe^x+2e^x+C = e^x(x^2-2x+2)+C$$

**Pattern:** integrating $x^ne^x$ requires $n$ applications of Integration by Parts, each time reducing the power of $x$ by 1. This is the origin of the **tabular method** (a shortcut organizing repeated integration by parts, covered in the lab).

---

## 7. The "Circular" Case — Solving for the Integral Algebraically

Some integrals, after two applications of Integration by Parts, return to a multiple of the **original** integral. Instead of an infinite loop, this lets us solve algebraically.

### Example 6

$$I = \int e^x\sin x\,dx$$

$u=\sin x$, $dv=e^x\,dx$. $du=\cos x\,dx$, $v=e^x$.

$$I = e^x\sin x-\int e^x\cos x\,dx$$

Apply Integration by Parts again to $\displaystyle\int e^x\cos x\,dx$: $u=\cos x$, $dv=e^x\,dx$. $du=-\sin x\,dx$, $v=e^x$.

$$\int e^x\cos x\,dx = e^x\cos x+\int e^x\sin x\,dx = e^x\cos x+I$$

Substitute back:

$$I = e^x\sin x - [e^x\cos x+I] = e^x\sin x-e^x\cos x-I$$

$$2I = e^x\sin x-e^x\cos x$$

$$I = \frac{e^x(\sin x-\cos x)}{2}+C$$

**This "solve for $I$" technique** is a genuinely elegant piece of algebra layered on top of the calculus — recognizing when an integral reappears and using that structure rather than integrating forever.

---

## 8. Integration by Parts for Definite Integrals

$$\int_a^b u\,dv = \Big[uv\Big]_a^b - \int_a^b v\,du$$

### Example 7

$$\int_0^1 xe^{-x}\,dx$$

$u=x$, $dv=e^{-x}dx$. $du=dx$, $v=-e^{-x}$.

$$= \Big[-xe^{-x}\Big]_0^1 - \int_0^1(-e^{-x})\,dx = \Big[-xe^{-x}\Big]_0^1+\int_0^1e^{-x}\,dx$$

$$= [-e^{-1}-0]+\Big[-e^{-x}\Big]_0^1 = -e^{-1}+[-e^{-1}-(-1)] = -e^{-1}-e^{-1}+1 = 1-\frac2e$$

---

## 9. CS Connection — Integration by Parts and Summation by Parts

Integration by Parts has a direct **discrete analog** called **summation by parts** (Abel's summation), which is the discrete-math cousin of this calculus technique:

$$\sum_{i=1}^n a_i(b_{i+1}-b_i) = [a_nb_{n+1}-a_1b_1] - \sum_{i=1}^{n-1}b_{i+1}(a_{i+1}-a_i)$$

This identity is used in:
- **Proving convergence of series** in numerical analysis (Abel's test, Dirichlet's test)
- **Analyzing algorithms** involving cumulative sums and differences (a technique sometimes needed in competitive programming and algorithm analysis for telescoping sums)
- **Signal processing**, where discrete integration-by-parts-like manipulations simplify convolution and correlation computations

The core idea — trade the derivative/difference from one factor onto the other, at the cost of a boundary term — is a recurring pattern anywhere continuous or discrete accumulation interacts with products of sequences or functions.

---

## Lecture 3 Exercises

1. Use Integration by Parts (with LIATE to guide your choice of $u$):
   - (a) $\displaystyle\int x\sin(2x)\,dx$
   - (b) $\displaystyle\int x^2\ln x\,dx$
   - (c) $\displaystyle\int \arcsin x\,dx$
   - (d) $\displaystyle\int x\sec^2x\,dx$

2. Use repeated Integration by Parts:
   - (a) $\displaystyle\int x^2\cos x\,dx$
   - (b) $\displaystyle\int x^3e^x\,dx$ *(requires three applications — look for the pattern)*

3. Use the "solve for $I$" technique:
   - (a) $\displaystyle\int e^{2x}\cos(3x)\,dx$
   - (b) $\displaystyle\int \sec^3x\,dx$ *(Hint: write $\sec^3x=\sec x\cdot\sec^2x$; after applying by parts once, use the identity $\tan^2x=\sec^2x-1$ to reveal the original integral.)*

4. Evaluate the definite integral $\displaystyle\int_1^e x\ln x\,dx$.

5. **(Synthesis)** Evaluate $\displaystyle\int x^2e^{3x}\,dx$ using repeated Integration by Parts. Then verify your answer by differentiating.

6. **(Challenge)** Derive a general reduction formula for $\displaystyle\int x^ne^x\,dx$ in terms of $\displaystyle\int x^{n-1}e^x\,dx$, using one application of Integration by Parts. Use it to quickly re-derive the result from Example 5.

---


### Answers

**1.** LIATE picks $u$: **L**og, **I**nverse trig, **A**lgebraic, **T**rig, **E**xponential.

**(a)** $u=x$, $dv=\sin2x\,dx$: $\boxed{-\tfrac{x\cos2x}{2}+\tfrac{\sin2x}{4}+C}$
**(b)** $u=\ln x$ (L beats A): $\boxed{\tfrac{x^3\ln x}{3}-\tfrac{x^3}{9}+C}$
**(c)** $u=\arcsin x$, $dv=dx$: $\boxed{x\arcsin x+\sqrt{1-x^2}+C}$
**(d)** $u=x$, $dv=\sec^2x\,dx$: $\boxed{x\tan x+\ln|\cos x|+C}$

(c) is the pattern for every inverse function: take $dv=dx$, so that differentiating $u$ removes the
inverse entirely.

**2. (a)** Two applications: $\boxed{x^2\sin x+2x\cos x-2\sin x+C}$
**(b)** Three applications: $\boxed{e^x\left(x^3-3x^2+6x-6\right)+C}$

The pattern in (b) — alternating signs with falling factorial coefficients — is exactly what the
**tabular method** (Lab 10 Part 4) automates.

**3. (a)** Two applications return the original integral. With
$I=\displaystyle\int e^{2x}\cos3x\,dx$, one obtains $I=\tfrac{e^{2x}(2\cos3x+3\sin3x)}{4}-\tfrac94I$,
so $\tfrac{13}{4}I=\ldots$ and
$$\boxed{I=\frac{e^{2x}\left(2\cos3x+3\sin3x\right)}{13}+C}$$
The denominator 13 is $2^2+3^2$ — always the sum of the squares of the two rate constants.

**(b)** With $u=\sec x$, $dv=\sec^2x\,dx$ and $\tan^2x=\sec^2x-1$:
$$\int\sec^3x\,dx=\sec x\tan x-\int\sec^3x\,dx+\int\sec x\,dx$$
$$\boxed{\int\sec^3x\,dx=\tfrac12\left(\sec x\tan x+\ln|\sec x+\tan x|\right)+C}$$
Note it needs $\int\sec x\,dx$, which came from W3 L02 Exercise 1(b).

**4.** $u=\ln x$, $dv=x\,dx$:
$$\int_1^ex\ln x\,dx=\left[\frac{x^2\ln x}{2}-\frac{x^2}{4}\right]_1^e
=\left(\frac{e^2}{2}-\frac{e^2}{4}\right)-\left(0-\frac14\right)=\boxed{\frac{e^2+1}{4}\approx2.0973}$$
*(Numerically confirmed.)*

**5.** Two applications with $u=x^2$ then $u=x$:
$$\boxed{\int x^2e^{3x}\,dx=e^{3x}\left(\frac{x^2}{3}-\frac{2x}{9}+\frac{2}{27}\right)+C}$$

**Verification by differentiation** (the point of the exercise):
$$\frac{d}{dx}\left[e^{3x}\left(\tfrac{x^2}{3}-\tfrac{2x}{9}+\tfrac{2}{27}\right)\right]
=e^{3x}\left[3\left(\tfrac{x^2}{3}-\tfrac{2x}{9}+\tfrac{2}{27}\right)+\left(\tfrac{2x}{3}-\tfrac29\right)\right]$$
$$=e^{3x}\left[x^2-\tfrac{2x}{3}+\tfrac29+\tfrac{2x}{3}-\tfrac29\right]=x^2e^{3x} \ \checkmark$$

**Always differentiate your antiderivative.** It is a complete check, it takes seconds, and unlike
the integration it cannot go subtly wrong — which makes it the single most valuable habit in
integral calculus.

*Reading for Week 8: Stewart §7.2–7.3 (Trigonometric Integrals and Trigonometric Substitution)*
*Problem Set 10 due next Wednesday — see assignment file.*
