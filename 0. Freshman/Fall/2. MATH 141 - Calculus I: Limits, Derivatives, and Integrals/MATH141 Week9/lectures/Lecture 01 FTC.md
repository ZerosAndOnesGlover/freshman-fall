# MATH 141 · Calculus I
## Week 9 · Lecture 1 (Monday)
### The Fundamental Theorem of Calculus

**Date:** Monday 23 November 2026 · 11:00–11:50 · Week 9

---

**Reading:** Stewart §5.3 | Spivak Ch. 14 (The Fundamental Theorem)
**Problem Set 8 is due Wednesday 25 November 2026, 11:00.**

---

## 1. The Most Important Theorem in Calculus

Everything in this course has been building toward this moment. We have two seemingly unrelated concepts:

- **Differentiation:** instantaneous rate of change, built from tangent lines
- **Integration:** accumulated total, built from Riemann sums of areas

The Fundamental Theorem of Calculus (FTC) reveals that these are **inverse operations** — as intimately connected as addition and subtraction, or multiplication and division. This single fact converts integration from a painful limit-of-Riemann-sums computation (Monday's lecture) into a simple two-step algebraic procedure.

---

## 2. FTC Part 1 — The Derivative of an Accumulation Function

Define the **accumulation function**:
$$g(x) = \int_a^x f(t)\,dt$$

This function outputs, for each $x$, the signed area accumulated from $a$ up to $x$. (Note: we use $t$ as the integration variable to avoid confusing it with the variable $x$ in the function's argument.)

> **Theorem (FTC Part 1).** If $f$ is continuous on $[a,b]$, then the function $g(x) = \displaystyle\int_a^x f(t)\,dt$ is differentiable on $(a,b)$, and:
> $$g'(x) = f(x)$$

**In words: the derivative of the accumulation function is the original function.** Integration and differentiation undo each other.

### Proof Sketch

$$g'(x) = \lim_{h\to0}\frac{g(x+h)-g(x)}{h} = \lim_{h\to0}\frac{1}{h}\left[\int_a^{x+h}f(t)\,dt - \int_a^x f(t)\,dt\right]$$

By interval additivity (Tuesday's lecture): $\displaystyle\int_a^{x+h}f(t)\,dt - \int_a^x f(t)\,dt = \int_x^{x+h}f(t)\,dt$.

So:
$$g'(x) = \lim_{h\to0}\frac{1}{h}\int_x^{x+h}f(t)\,dt$$

By the Mean Value Theorem for Integrals (Tuesday), $\displaystyle\int_x^{x+h}f(t)\,dt = f(c)\cdot h$ for some $c$ between $x$ and $x+h$.

$$g'(x) = \lim_{h\to0}\frac{f(c)\cdot h}{h} = \lim_{h\to0}f(c)$$

As $h\to0$, $c\to x$ (squeezed between $x$ and $x+h$). Since $f$ is continuous:

$$g'(x) = \lim_{c\to x}f(c) = f(x) \quad\square$$

**This proof uses nearly every major theorem from Weeks 1–6**: interval additivity of integrals, the Mean Value Theorem for Integrals, the Squeeze principle, and continuity. It is the payoff of the entire course so far.

### Example 1 — Direct Application of FTC Part 1

Find $\dfrac{d}{dx}\displaystyle\int_2^x t^3\,dt$.

By FTC Part 1: $\dfrac{d}{dx}\displaystyle\int_2^x t^3\,dt = x^3$ — immediately, no computation of the integral required.

### Example 2 — With the Chain Rule

Find $\dfrac{d}{dx}\displaystyle\int_1^{x^2} \sin(t)\,dt$.

Let $u=x^2$. By FTC Part 1 combined with the chain rule:

$$\frac{d}{dx}\int_1^{x^2}\sin(t)\,dt = \sin(x^2)\cdot\frac{d}{dx}[x^2] = 2x\sin(x^2)$$

### Example 3 — Variable Lower Limit

Find $\dfrac{d}{dx}\displaystyle\int_x^5 \cos(t^2)\,dt$.

Reverse the limits: $\displaystyle\int_x^5\cos(t^2)\,dt = -\int_5^x\cos(t^2)\,dt$.

By FTC Part 1: $\dfrac{d}{dx}\left[-\displaystyle\int_5^x\cos(t^2)\,dt\right] = -\cos(x^2)$

### Example 4 — Both Limits Variable

Find $\dfrac{d}{dx}\displaystyle\int_{x}^{x^3} e^{t^2}\,dt$.

Split at a convenient constant, say $0$:

$$\int_x^{x^3}e^{t^2}\,dt = \int_x^0 e^{t^2}\,dt + \int_0^{x^3}e^{t^2}\,dt = -\int_0^x e^{t^2}\,dt + \int_0^{x^3}e^{t^2}\,dt$$

Differentiate each piece:

$$\frac{d}{dx}\left[-\int_0^xe^{t^2}\,dt\right] = -e^{x^2}$$

$$\frac{d}{dx}\left[\int_0^{x^3}e^{t^2}\,dt\right] = e^{(x^3)^2}\cdot3x^2 = 3x^2e^{x^6}$$

$$\frac{d}{dx}\int_x^{x^3}e^{t^2}\,dt = 3x^2e^{x^6} - e^{x^2}$$

---

## 3. Antiderivatives — Formalizing the Inverse Operation

> **Definition.** $F$ is an **antiderivative** of $f$ on an interval $I$ if $F'(x) = f(x)$ for all $x \in I$.

**Recall from Week 4 (MVT Corollary 2):** if $F$ and $G$ are both antiderivatives of $f$ on an interval, then $F(x) - G(x) = C$ for some constant $C$. This means: **antiderivatives are unique up to an additive constant.**

We write the **general antiderivative** (also called the **indefinite integral**):

$$\int f(x)\,dx = F(x) + C$$

where $F$ is any particular antiderivative. (We will build a complete toolkit of antiderivative formulas next week.)

---

## 4. FTC Part 2 — The Evaluation Theorem

This is the version of the FTC used for actually **computing** definite integrals — and it is the reason five weeks spent building differentiation rules will now pay enormous dividends in integration.

> **Theorem (FTC Part 2).** If $f$ is continuous on $[a,b]$, and $F$ is ANY antiderivative of $f$ (i.e., $F'=f$), then:
> $$\int_a^b f(x)\,dx = F(b) - F(a)$$

**Notation:** we write $F(b)-F(a)$ as $\Big[F(x)\Big]_a^b$ or $F(x)\Big|_a^b$.

### Proof (using FTC Part 1)

Let $g(x) = \displaystyle\int_a^x f(t)\,dt$. By FTC Part 1, $g'(x) = f(x)$ — so $g$ IS an antiderivative of $f$.

Since $F$ is also an antiderivative of $f$, by MVT Corollary 2 (Week 4): $F(x) = g(x) + C$ for some constant $C$.

Evaluate at $x=a$: $F(a) = g(a) + C = \displaystyle\int_a^a f(t)\,dt + C = 0+C = C$. So $C = F(a)$.

Evaluate at $x=b$: $F(b) = g(b)+C = \displaystyle\int_a^b f(t)\,dt + F(a)$

$$\implies \int_a^b f(t)\,dt = F(b)-F(a) \quad\square$$

**This proof shows FTC Part 2 is a direct consequence of FTC Part 1 plus the MVT Corollary from Week 4.** The entire semester's machinery converges here.

---

## 5. Computing Definite Integrals — Finally, an Easy Method!

Compare: computing $\displaystyle\int_0^1 x^2\,dx$ via Riemann sums (Monday) required summation formulas and a limit computation. Via FTC Part 2:

An antiderivative of $x^2$ is $F(x) = \dfrac{x^3}{3}$ (check: $F'(x)=x^2$ ✓).

$$\int_0^1 x^2\,dx = F(1)-F(0) = \frac13 - 0 = \frac13$$

**Exactly matching Monday's laborious computation — obtained in one line.**

### Example 5

$$\int_1^4 \sqrt{x}\,dx = \int_1^4 x^{1/2}\,dx$$

Antiderivative: $F(x) = \dfrac{x^{3/2}}{3/2} = \dfrac23x^{3/2}$ (using the reverse power rule: raise the power by 1, divide by the new power).

$$= \frac23x^{3/2}\Big|_1^4 = \frac23(8) - \frac23(1) = \frac{16}{3}-\frac23 = \frac{14}{3}$$

### Example 6

$$\int_0^{\pi/2}\cos x\,dx$$

Antiderivative of $\cos x$ is $\sin x$ (since $\frac{d}{dx}[\sin x]=\cos x$).

$$= \sin x\Big|_0^{\pi/2} = \sin(\pi/2)-\sin(0) = 1-0=1$$

### Example 7

$$\int_1^e \frac1x\,dx$$

Antiderivative of $1/x$ is $\ln x$ (Week 3!).

$$=\ln x\Big|_1^e = \ln e - \ln 1 = 1-0=1$$

### Example 8 — Verifying the Midpoint Approximation from Tuesday

Recall Tuesday's Example 5 estimated $\displaystyle\int_1^2\frac1x\,dx \approx 0.6912$ using $M_4$. Now compute exactly:

$$\int_1^2\frac1x\,dx = \ln x\Big|_1^2 = \ln2-\ln1 = \ln2 \approx 0.6931$$

The midpoint approximation was accurate to within $0.002$ using just 4 rectangles — a testament to how quickly Riemann sums converge for smooth functions.

---

## 6. Building an Antiderivative Table (Reversing Week 2–3's Derivative Rules)

Every derivative rule from Weeks 2–3 gives us an antiderivative rule, read backward:

| $f(x)$ | $\int f(x)\,dx$ |
|--------|-----------------|
| $x^n$ ($n\neq-1$) | $\dfrac{x^{n+1}}{n+1}+C$ |
| $\dfrac1x$ | $\ln|x|+C$ |
| $e^x$ | $e^x+C$ |
| $\sin x$ | $-\cos x+C$ |
| $\cos x$ | $\sin x+C$ |
| $\sec^2x$ | $\tan x+C$ |
| $\sec x\tan x$ | $\sec x+C$ |
| $\dfrac{1}{\sqrt{1-x^2}}$ | $\arcsin x+C$ |
| $\dfrac{1}{1+x^2}$ | $\arctan x+C$ |

We will substantially expand this table next week with integration techniques (substitution, integration by parts).

---

## 7. CS Connection — Why the FTC Changed Computing Forever

Before the FTC (proven independently by Newton and Leibniz in the 1600s), computing any area required a bespoke geometric or limiting argument — exactly the laborious process of Monday's lecture, redone from scratch for every new function. The FTC converts this into an **algorithm**: find an antiderivative, evaluate at two points, subtract.

**This is precisely the difference between brute-force computation and algorithmic efficiency** that defines computer science. Just as a good algorithm replaces an exponential-time brute-force search with a polynomial-time method exploiting structure, the FTC replaces an intractable-by-hand Riemann sum limit with an $O(1)$-style lookup (find the antiderivative) plus two evaluations.

**Symbolic computation systems** (Mathematica, SymPy, Wolfram Alpha) implement exactly this table-lookup-plus-evaluation strategy at massive scale, using pattern-matching against thousands of known antiderivative forms combined with the integration techniques we study next week (substitution, parts) — essentially automating the "find $F$" step of FTC Part 2.

**When no elementary antiderivative exists** (e.g., $\int e^{-x^2}dx$, essential in probability/statistics), computers fall back to numerical Riemann-sum-based methods (Simpson's Rule, adaptive quadrature) — directly generalizing Monday's lecture. Understanding both the exact (FTC) and approximate (Riemann sum) methods, and knowing when each applies, is essential for any computational scientist.

---

## Lecture 3 Exercises

1. Use FTC Part 1 to find $g'(x)$:
   - (a) $g(x) = \displaystyle\int_0^x (t^2+1)\,dt$
   - (b) $g(x) = \displaystyle\int_3^x \sqrt{1+t^3}\,dt$
   - (c) $g(x) = \displaystyle\int_0^{x^2} \sin(t)\,dt$
   - (d) $g(x) = \displaystyle\int_{\cos x}^{5} e^{t^2}\,dt$

2. Use FTC Part 2 to evaluate:
   - (a) $\displaystyle\int_{-1}^2 (3x^2-2x+1)\,dx$
   - (b) $\displaystyle\int_1^4 \frac{1}{\sqrt x}\,dx$
   - (c) $\displaystyle\int_0^{\pi/4}\sec^2x\,dx$
   - (d) $\displaystyle\int_1^2 \left(x^3 - \frac1{x^2}\right)dx$
   - (e) $\displaystyle\int_0^1 e^x\,dx$

3. Find the derivative of $h(x) = \displaystyle\int_{x^2}^{x^3} \ln(1+t^2)\,dt$. *(Split the integral at a constant, e.g., 0, then differentiate each piece.)*

4. Verify FTC Part 2 for $f(x) = x^2$ on $[0,1]$ by comparing your answer to the exact Riemann sum limit computed in Monday's lecture (Section 6).

5. **(Conceptual)** A student is confused: "FTC Part 1 says the derivative of an integral is the original function. FTC Part 2 says the integral equals an antiderivative evaluated at the endpoints. Aren't these the same statement?" Explain precisely how the two parts differ and how Part 2 is proven USING Part 1 (refer to the proof in Section 4).

6. **(Challenge)** Find $\dfrac{d^2}{dx^2}\displaystyle\int_0^x (x-t)f(t)\,dt$ where $f$ is continuous. *(Hint: first expand $(x-t)f(t) = xf(t) - tf(t)$ and split the integral; note that $x$ can be pulled outside the first integral since it doesn't depend on $t$. Then apply FTC Part 1 twice.)*

---


### Answers

**1.** FTC Part 1, with the chain rule where the upper limit is not simply $x$.

**(a)** $\boxed{x^2+1}$ &nbsp;&nbsp; **(b)** $\boxed{\sqrt{1+x^3}}$ — the constant lower limit 3 is
irrelevant to the derivative.
**(c)** $\boxed{\sin(x^2)\cdot2x}$ &nbsp;&nbsp;
**(d)** The variable is the **lower** limit, so flip the sign first:
$\displaystyle\int_{\cos x}^{5}=-\int_{5}^{\cos x}$, giving
$\boxed{e^{\cos^2x}\sin x}$.

**2. (a)** $\left[x^3-x^2+x\right]_{-1}^{2}=6-(-3)=\boxed{9}$
**(b)** $\left[2\sqrt x\right]_1^4=4-2=\boxed{2}$
**(c)** $\left[\tan x\right]_0^{\pi/4}=\boxed{1}$
**(d)** $\left[\tfrac{x^4}{4}+\tfrac1x\right]_1^2=\left(4+\tfrac12\right)-\left(\tfrac14+1\right)=\boxed{\tfrac{13}{4}}$
**(e)** $\left[e^x\right]_0^1=\boxed{e-1\approx1.718}$

*(All five confirmed by numerical integration.)*

**3.** Split at 0 to make each piece a standard FTC Part 1 form:
$$h(x)=\int_{x^2}^{0}\ln(1+t^2)\,dt+\int_{0}^{x^3}\ln(1+t^2)\,dt$$
$$h'(x)=\boxed{3x^2\ln\!\left(1+x^6\right)-2x\ln\!\left(1+x^4\right)}$$
Each limit contributes its own chain-rule factor, and the **lower** limit contributes with a minus
sign. The splitting point is arbitrary — any constant works and cancels out.

**4.** FTC Part 2 gives $\displaystyle\int_0^1x^2\,dx=\left[\tfrac{x^3}{3}\right]_0^1=\tfrac13$,
matching the Riemann-sum limit computed on Monday. ✓

The agreement is the theorem's content: a **limit of sums** and a **difference of antiderivative
values** are two computations with no evident reason to coincide, and the FTC is the statement that
they always do.

**5.** They are different statements about inverse operations.

- **Part 1** says differentiation *undoes* integration:
  $\dfrac{d}{dx}\displaystyle\int_a^xf(t)\,dt=f(x)$. It asserts that an antiderivative **exists**
  for every continuous $f$ — a genuine existence theorem.
- **Part 2** says integration is *evaluated by* any antiderivative:
  $\displaystyle\int_a^bf=F(b)-F(a)$. This is a computational tool.

**Part 2 is proved using Part 1.** Define $G(x)=\int_a^xf$; Part 1 gives $G'=f$, so $G$ is *an*
antiderivative. If $F$ is any other, then $(F-G)'=0$, so by the MVT $F-G$ is **constant**. Hence
$$F(b)-F(a)=G(b)-G(a)=\int_a^bf-0=\int_a^bf$$

Note where the MVT enters — "zero derivative implies constant" is not obvious and is exactly what
the MVT supplies. The two parts are not the same statement; one manufactures antiderivatives, the
other spends them.

*Reading for Week 7: Stewart §5.4–5.5 (Indefinite Integrals, the Substitution Rule)*
*Problem Set 9 is released Wednesday after Lecture 3.*
