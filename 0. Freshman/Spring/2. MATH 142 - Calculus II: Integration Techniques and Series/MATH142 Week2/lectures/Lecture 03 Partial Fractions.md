# MATH 142 · Calculus II
## Week 2 · Lecture 3 (Friday)
### Partial Fractions, and a Theorem About Which Integrals Can Be Done

**Date:** Friday 29 January 2027 · 11:00–11:50 · Week 2

---

**Reading:** Stewart §7.4 | Apostol Ch. 6 §6.15

---

## 1. The Claim

Week 0 opened with bad news: $e^{-x^2}$ has no elementary antiderivative, and neither do most functions.

**Today is the good news.** For one large and important class of functions, the answer is *always* yes — and there is an algorithm.

> **Theorem.** Every **rational function** — a quotient $\dfrac{P(x)}{Q(x)}$ of polynomials — has an
> elementary antiderivative, and it is a combination of **polynomials, logarithms, arctangents, and
> rational functions**. Nothing else ever appears.

That is a remarkable statement. It says the entire infinite family of rational functions is *solved*: no cleverness needed, no special functions, no cases where it cannot be done. **Partial fractions is the proof, and it is constructive** — it tells you how to find the answer.

---

## 2. The Idea

You know how to add fractions:

$$\frac{1}{x-1} - \frac{1}{x+1} = \frac{(x+1)-(x-1)}{(x-1)(x+1)} = \frac{2}{x^2-1}$$

**Partial fractions runs this backwards.** Given $\frac{2}{x^2-1}$, which you cannot integrate directly, recover $\frac{1}{x-1}-\frac{1}{x+1}$, which you can — each piece is a logarithm.

$$\int\frac{2\,dx}{x^2-1} = \ln|x-1| - \ln|x+1| + C = \ln\left|\frac{x-1}{x+1}\right| + C$$

**Every hard rational integral becomes a sum of easy ones.**

---

## 3. The Algorithm

### Step 0 — Check the fraction is proper

**If $\deg P \ge \deg Q$, do polynomial long division first.** Partial fraction decomposition is only valid for a proper fraction, and applying it to an improper one silently produces a wrong answer.

*(This was §4 of yesterday's lecture. It is a precondition, not a suggestion.)*

### Step 1 — Factor the denominator completely

Over the reals, every polynomial factors into **linear factors** and **irreducible quadratics** — this is a theorem, and it is why there are exactly four cases below.

### Step 2 — Write the decomposition with unknown constants

| Factor in $Q$ | Contributes |
|---|---|
| distinct linear $(x-r)$ | $\dfrac{A}{x-r}$ |
| repeated linear $(x-r)^k$ | $\dfrac{A_1}{x-r}+\dfrac{A_2}{(x-r)^2}+\cdots+\dfrac{A_k}{(x-r)^k}$ |
| distinct irreducible quadratic $(x^2+bx+c)$ | $\dfrac{Ax+B}{x^2+bx+c}$ |
| repeated irreducible quadratic $(x^2+bx+c)^k$ | $\dfrac{A_1x+B_1}{x^2+bx+c}+\cdots+\dfrac{A_kx+B_k}{(x^2+bx+c)^k}$ |

**Two rules that account for most errors:**
- A **repeated** factor needs a term for **every** power up to $k$, not just the highest.
- An **irreducible quadratic** gets a **linear** numerator $Ax+B$, not a constant.

### Step 3 — Solve for the constants

Two methods, both fine:

- **Cover-up (Heaviside):** for a *distinct linear* factor $(x-r)$, multiply through by it and set $x=r$. Every other term dies, giving the constant instantly.
- **Equate coefficients:** clear denominators and match powers of $x$. Always works; more algebra.

### Step 4 — Integrate each piece

| Piece | Integral |
|---|---|
| $\dfrac{A}{x-r}$ | $A\ln\lvert x-r\rvert$ |
| $\dfrac{A}{(x-r)^k},\ k\ge2$ | $\dfrac{-A}{(k-1)(x-r)^{k-1}}$ |
| $\dfrac{Ax+B}{x^2+bx+c}$ | split the numerator → **logarithm + arctangent** *(yesterday, §2 Example 3)* |

**Notice: logarithms, arctangents, and rational functions. Nothing else.** That is the theorem.

---

## 4. Case 1 — Distinct Linear Factors

$$\int\frac{x+5}{(x+1)(x-2)}\,dx$$

Decompose:

$$\frac{x+5}{(x+1)(x-2)} = \frac{A}{x+1}+\frac{B}{x-2}$$

**By cover-up:**

- $A$: cover $(x+1)$, set $x=-1$: $\;A = \dfrac{-1+5}{-1-2} = \dfrac{4}{-3} = -\dfrac43$
- $B$: cover $(x-2)$, set $x=2$: $\;B = \dfrac{2+5}{2+1} = \dfrac73$

$$\frac{x+5}{(x+1)(x-2)} = -\frac{4}{3(x+1)}+\frac{7}{3(x-2)}$$

*Verified: the CAS decomposition agrees, and recombining returns the original.*

$$\boxed{\int = -\frac43\ln|x+1| + \frac73\ln|x-2| + C}$$

*Verified symbolically.*

> **Always check a decomposition by recombining it.** It takes thirty seconds and catches every
> arithmetic slip. Lab 2 makes you do it mechanically.

---

## 5. Case 2 — Repeated Linear Factors

$$\int\frac{3x+1}{(x-1)^2(x+2)}\,dx$$

The repeated factor needs **both** powers:

$$\frac{3x+1}{(x-1)^2(x+2)} = \frac{A}{x-1}+\frac{B}{(x-1)^2}+\frac{C}{x+2}$$

Cover-up gives the *highest* power of a repeated factor and any distinct factor directly:

- $B$: multiply by $(x-1)^2$, set $x=1$: $\;B = \dfrac{3+1}{1+2} = \dfrac43$
- $C$: cover $(x+2)$, set $x=-2$: $\;C = \dfrac{-6+1}{(-3)^2} = \dfrac{-5}{9}$

$A$ needs another equation — set $x=0$ in the cleared identity, or match the $x^2$ coefficient. Either gives $A = \tfrac59$.

$$\frac{3x+1}{(x-1)^2(x+2)} = \frac{5}{9(x-1)}+\frac{4}{3(x-1)^2}-\frac{5}{9(x+2)}$$

*Verified: the CAS returns exactly this, and it recombines to the original.*

$$\boxed{\int = \frac59\ln|x-1| - \frac{4}{3(x-1)} - \frac59\ln|x+2|+C}$$

*Verified symbolically.*

**Note the middle term is not a logarithm** — $\int\frac{dx}{(x-1)^2}$ is a power, giving $-\frac{1}{x-1}$. This is the "rational function" appearing in the theorem's list, and repeated factors are the only way it arises.

---

## 6. Case 3 — Irreducible Quadratic Factors

$$\int\frac{x^2+1}{(x+1)(x^2+4)}\,dx$$

$x^2+4$ has no real roots, so it is irreducible and gets a **linear** numerator:

$$\frac{x^2+1}{(x+1)(x^2+4)} = \frac{A}{x+1}+\frac{Bx+C}{x^2+4}$$

Cover-up gives $A = \dfrac{(-1)^2+1}{(-1)^2+4} = \dfrac25$. Matching coefficients gives $B = \tfrac35$, $C=-\tfrac35$:

$$= \frac{2}{5(x+1)}+\frac{3(x-1)}{5(x^2+4)}$$

*Verified: the CAS returns exactly this form, and it recombines correctly.*

Now integrate. The second piece **splits**, as in yesterday's §2:

$$\frac35\int\frac{x-1}{x^2+4}dx = \frac35\left[\frac12\int\frac{2x\,dx}{x^2+4} - \int\frac{dx}{x^2+4}\right] = \frac{3}{10}\ln(x^2+4) - \frac{3}{5}\cdot\frac12\arctan\frac x2$$

$$\boxed{\int = \frac25\ln|x+1| + \frac{3}{10}\ln(x^2+4) - \frac{3}{10}\arctan\frac x2 + C}$$

*Verified symbolically.*

**There is the arctangent.** Irreducible quadratics are the only source of one, and every irreducible quadratic produces exactly this pattern: a logarithm from the $x$ part, an arctangent from the constant part.

### Another, in a common disguise

$$\int\frac{2x^2-x+4}{x^3+4x}\,dx$$

**Factor first:** $x^3+4x = x(x^2+4)$ — a linear factor and an irreducible quadratic.

$$\frac{2x^2-x+4}{x(x^2+4)} = \frac1x + \frac{x-1}{x^2+4}$$

*Verified: the CAS returns exactly this.*

$$\boxed{\int = \ln|x| + \frac12\ln(x^2+4) - \frac12\arctan\frac x2 + C}$$

*Verified symbolically.*

---

## 7. Why the Theorem Is True

The argument is now visible:

1. **Division** reduces any rational function to a polynomial plus a proper fraction. Polynomials integrate trivially.
2. **The Fundamental Theorem of Algebra** (over $\mathbb R$) says every denominator factors into linear factors and irreducible quadratics — those are the only possibilities.
3. **Partial fractions** splits the proper fraction into pieces, one per factor.
4. **Each piece is on the short list**: a logarithm, an arctangent, or a power of a linear factor.

Since every step always succeeds, **every rational function has an elementary antiderivative.** $\blacksquare$

### The contrast worth holding onto

| | Rational functions | $e^{-x^2}$, $\tfrac{\sin x}{x}$, $\sqrt{1+x^3}$ |
|---|---|---|
| Elementary antiderivative? | **Always** | **Never** |
| How do you find it? | An algorithm | You cannot |
| Which functions appear? | $\ln$, $\arctan$, rationals | — |

**This is the only large class of functions in the course where integration is completely solved.** It is worth knowing that such a class exists, and worth knowing how small it is.

---

## 8. What To Take From This Lecture

1. **Divide first if the fraction is improper.** Non-negotiable.
2. **Factor the denominator completely**, then write one group of terms per factor.
3. **Repeated factors need every power**; **irreducible quadratics need a linear numerator.**
4. **Cover-up** for distinct linear factors and top powers; coefficients otherwise.
5. **Recombine to check.** Always.
6. **Only three things ever come out:** logarithms, arctangents, and rational functions.

---

## Looking Ahead

The toolkit is now complete: substitution, parts, trigonometric substitution, partial fractions. Everything that *can* be integrated in closed form in this course, you can now attempt.

**Next week we stop asking whether an integral can be evaluated and start asking whether it exists at all.** What is $\int_1^\infty\frac{dx}{x^2}$? The region is infinitely long — and yet the answer is 1. Meanwhile $\int_1^\infty\frac{dx}{x}$ is infinite, although the two regions look almost identical.

**Telling those two apart is Week 3**, and the method — comparison — is a direct ancestor of every convergence test in Weeks 7 and 8.

---

*Next: Week 3, Monday — Improper Integrals*
