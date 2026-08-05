# MATH 142 · Calculus II
## Problem Set 2 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Every antiderivative below was verified by symbolic differentiation.

> **Marking philosophy.** This set is the heaviest computation of the course. **Mark the method.** A
> student with the right substitution, the right range, and an arithmetic slip in line four
> understands this material; a student with a correct answer and no visible reasoning may not.
>
> **Award full credit for correct alternative forms.** $\operatorname{arcsec}\frac x3$ and
> $\arccos\frac3x$ are equal; $\ln|x+\sqrt{x^2-a^2}|$ and $\operatorname{arcosh}\frac xa$ differ by a
> constant. If it differentiates to the integrand, it is right.

---

## Part A — Trigonometric Substitution (5 pts each)

### A1 (5) — $\int\sqrt{4-x^2}\,dx$

Pattern $\sqrt{a^2-x^2}$, $a=2$: $x = 2\sin\theta$, $dx=2\cos\theta\,d\theta$, $\theta\in[-\tfrac\pi2,\tfrac\pi2]$ so $\sqrt{4-x^2}=2\cos\theta$.

$$\int 2\cos\theta\cdot2\cos\theta\,d\theta = 4\int\cos^2\theta\,d\theta = 4\left(\frac\theta2+\frac{\sin\theta\cos\theta}{2}\right) = 2\theta + 2\sin\theta\cos\theta$$

Triangle: $\sin\theta=\tfrac x2$, $\cos\theta = \tfrac{\sqrt{4-x^2}}{2}$.

$$\boxed{= 2\arcsin\frac x2 + \frac{x\sqrt{4-x^2}}{2}+C}$$

*Verified.*

*Marking: 1 substitution, 1 range stated, 2 integration, 1 conversion back. **The range must appear** — it is what licenses $\sqrt{4\cos^2\theta}=2\cos\theta$ without absolute value.*

### A2 (5) — $\int\frac{dx}{x^2\sqrt{x^2+9}}$, $x>0$

Pattern $\sqrt{a^2+x^2}$, $a=3$: $x=3\tan\theta$, $dx=3\sec^2\theta\,d\theta$, $\sqrt{x^2+9}=3\sec\theta$.

$$\int\frac{3\sec^2\theta\,d\theta}{9\tan^2\theta\cdot3\sec\theta} = \frac19\int\frac{\sec\theta}{\tan^2\theta}d\theta = \frac19\int\frac{\cos\theta}{\sin^2\theta}d\theta$$

With $w=\sin\theta$: $=\frac19\int w^{-2}dw = -\frac{1}{9\sin\theta}$.

Triangle: $\sin\theta = \tfrac{x}{\sqrt{x^2+9}}$.

$$\boxed{= -\frac{\sqrt{x^2+9}}{9x}+C}$$

*Verified by differentiation.*

*Marking: 2 substitution, 2 the $\frac{\sec}{\tan^2}\to\frac{\cos}{\sin^2}$ simplification, 1 conversion. **The rewrite into sines and cosines is the step students miss** — they try to force a $\tan$/$\sec$ parity case that does not apply.*

### A3 (5) — $\int\frac{dx}{(x^2-4)^{3/2}}$, $x>2$

$x=2\sec\theta$, $dx = 2\sec\theta\tan\theta\,d\theta$; on $x>2$ take $\theta\in[0,\tfrac\pi2)$, where $\tan\theta\ge0$, **so $\sqrt{x^2-4} = 2\tan\theta$ without an absolute value** — this is where $x>2$ is used.

$$(x^2-4)^{3/2} = 8\tan^3\theta \implies \int\frac{2\sec\theta\tan\theta}{8\tan^3\theta}d\theta = \frac14\int\frac{\sec\theta}{\tan^2\theta}d\theta = \frac14\int\frac{\cos\theta}{\sin^2\theta}d\theta = -\frac{1}{4\sin\theta}$$

Triangle: $\sin\theta = \tfrac{\sqrt{x^2-4}}{x}$.

$$\boxed{= -\frac{x}{4\sqrt{x^2-4}}+C}$$

*Verified: differentiating gives $\frac{1}{(x^2-4)^{3/2}}$ exactly.*

*Marking: 1 substitution, **2 for stating explicitly where $x>2$ is used** (the problem asked), 2 execution.*

> **Worth showing the class.** Asked for this with no domain, a CAS returns a two-branch `Piecewise`
> with an imaginary unit in the second branch. Told $x>2$, it returns the boxed answer. **The domain
> is part of the problem, not decoration.**

### A4 (5) — $\int_0^1\frac{dx}{(1+x^2)^{3/2}}$

$x=\tan\theta$, $dx=\sec^2\theta\,d\theta$. **Limits:** $x=0\Rightarrow\theta=0$; $x=1\Rightarrow\theta=\tfrac\pi4$.

$$\int_0^{\pi/4}\frac{\sec^2\theta}{\sec^3\theta}d\theta = \int_0^{\pi/4}\cos\theta\,d\theta = \Big[\sin\theta\Big]_0^{\pi/4} = \boxed{\frac{\sqrt2}{2}}\approx 0.7071$$

*Verified symbolically.*

*Marking: 2 for changing the limits, 3 for the rest. **A student who converted back to $x$ and then evaluated earns full marks** but should be told the limit change was two lines shorter — the problem asked for it.*

---

## Part B — Completing the Square and Rationalizing (6 pts each)

### B1 (6) — $\int\frac{dx}{x^2+4x+8}$

$x^2+4x+8 = (x+2)^2+4$. With $u=x+2$:

$$\int\frac{du}{u^2+4} = \frac12\arctan\frac u2 \implies \boxed{\frac12\arctan\frac{x+2}{2}+C}$$

*Verified.*

*Marking: 3 completing the square, 3 the arctangent with the correct $\tfrac12$. **The leading $\tfrac1a$ is dropped constantly** — it is worth 2 of the 6.*

### B2 (6) — $\int\frac{dx}{\sqrt{8+2x-x^2}}$

**Factor the $-1$ out of the $x$ terms first:**

$$8+2x-x^2 = 8-(x^2-2x) = 8-\big[(x-1)^2-1\big] = 9-(x-1)^2$$

With $u=x-1$:

$$\int\frac{du}{\sqrt{9-u^2}} = \arcsin\frac u3 \implies \boxed{\arcsin\frac{x-1}{3}+C}$$

*Verified.*

*Marking: **3 of the 6 for handling the sign correctly.** The common wrong path gives $(x+1)^2$ or a $\sqrt{u^2-9}$, and everything downstream is then wrong. Show the $8-(x^2-2x)$ grouping explicitly when returning the set.*

### B3 (6) — $\int\frac{3x-1}{x^2-2x+5}\,dx$

$\frac{d}{dx}(x^2-2x+5) = 2x-2$. Write $3x-1 = \tfrac32(2x-2)+2$:

$$= \frac32\int\frac{2x-2}{x^2-2x+5}dx + 2\int\frac{dx}{(x-1)^2+4}$$

$$= \frac32\ln(x^2-2x+5) + 2\cdot\frac12\arctan\frac{x-1}{2}$$

$$\boxed{= \frac32\ln(x^2-2x+5)+\arctan\frac{x-1}{2}+C}$$

*Verified symbolically.*

*Marking: 3 for the split with correct coefficients, 3 for the two integrals. **The $\tfrac32$ and the leftover $2$ are the difficulty**; check their arithmetic: $\tfrac32(2x-2) = 3x-3$, and $-1-(-3) = 2$ ✓.*

### B4 (6) — $\int\frac{x^3+2x}{x+1}\,dx$

**Improper — divide first.** $\dfrac{x^3+2x}{x+1} = x^2-x+3-\dfrac{3}{x+1}$.

$$\boxed{= \frac{x^3}{3}-\frac{x^2}{2}+3x-3\ln|x+1|+C}$$

*Verified.*

*Marking: **3 for recognising the fraction is improper and dividing**, 3 for the integration. A student who attempted partial fractions without dividing should be pointed at D2 — it is the same error.*

### B5 (6) — $\int\frac{\sqrt x}{1+x}\,dx$

$u=\sqrt x$, $x=u^2$, $dx=2u\,du$:

$$\int\frac{u}{1+u^2}\cdot2u\,du = 2\int\frac{u^2}{1+u^2}du = 2\int\left(1-\frac{1}{1+u^2}\right)du = 2u - 2\arctan u$$

$$\boxed{= 2\sqrt x - 2\arctan\sqrt x + C}$$

*Verified.*

**Why not a logarithm:** after substituting, the denominator is $1+u^2$ — an **irreducible quadratic**, which yields an arctangent. A logarithm would require the denominator to factor (or the numerator to be its derivative), and $1+u^2$ does neither over the reals.

*Marking: 2 substitution, 2 the division step $\frac{u^2}{1+u^2}=1-\frac1{1+u^2}$, **2 for the explanation.** The explanation must reference irreducibility; "because it's arctan" earns 0 of those 2.*

---

## Part C — Partial Fractions (6 pts each)

*Marking throughout: **1 of the 6 is for verifying the decomposition by recombining**, which the instructions required.*

### C1 (6) — $\int\frac{5x-3}{(x-1)(x+3)}\,dx$

Cover-up: $A = \frac{5(1)-3}{1+3} = \frac12$ ; $B = \frac{5(-3)-3}{-3-1} = \frac{-18}{-4} = \frac92$.

$$\frac{5x-3}{(x-1)(x+3)} = \frac{1}{2(x-1)}+\frac{9}{2(x+3)}$$

*Verified: recombines to the original.*

$$\boxed{\int = \frac12\ln|x-1| + \frac92\ln|x+3| + C}$$

*Verified.*

### C2 (6) — $\int\frac{dx}{x^3-x}$

**Factor completely:** $x^3-x = x(x-1)(x+1)$ — three distinct linear factors.

$$\frac{1}{x(x-1)(x+1)} = -\frac1x + \frac{1}{2(x-1)}+\frac{1}{2(x+1)}$$

*Verified: the CAS returns exactly this, and it recombines.*

$$\boxed{\int = -\ln|x| + \frac12\ln|x-1| + \frac12\ln|x+1| + C}$$

*(equivalently $\tfrac12\ln\left|\tfrac{x^2-1}{x^2}\right|$)*

*Verified.*

*Marking: **2 for factoring out the $x$.** Students who write $x^3-x = (x-1)(x^2+x)$ and stop have not factored completely, and their decomposition will not close.*

### C3 (6) — $\int\frac{x^2+2x+3}{(x-1)(x+1)^2}\,dx$

Repeated factor needs both powers:

$$= \frac{A}{x-1}+\frac{B}{x+1}+\frac{C}{(x+1)^2}$$

Cover-up: $A = \frac{1+2+3}{(1+1)^2} = \frac{6}{4}=\frac32$ ; $C = \frac{1-2+3}{-1-1} = \frac{2}{-2} = -1$. Then $B = -\frac12$.

$$= \frac{3}{2(x-1)} - \frac{1}{2(x+1)} - \frac{1}{(x+1)^2}$$

*Verified: matches the CAS decomposition and recombines.*

$$\boxed{\int = \frac32\ln|x-1| - \frac12\ln|x+1| + \frac{1}{x+1} + C}$$

*Verified.*

*Marking: 2 for the correct three-term shape, 2 for the constants, 1 for the non-logarithmic middle term, 1 for the check. **The $+\frac1{x+1}$ sign** trips people: $\int(x+1)^{-2}dx = -(x+1)^{-1}$, and the coefficient is $-1$, so the result is $+\frac1{x+1}$.*

### C4 (6) — $\int\frac{4x}{(x+1)(x^2+1)}\,dx$

$x^2+1$ is irreducible → linear numerator:

$$\frac{4x}{(x+1)(x^2+1)} = \frac{-2}{x+1}+\frac{2x+2}{x^2+1}$$

*Verified: the CAS gives $\frac{2(x+1)}{x^2+1} - \frac{2}{x+1}$, the same thing.*

$$\int = -2\ln|x+1| + \int\frac{2x}{x^2+1}dx + \int\frac{2}{x^2+1}dx$$

$$\boxed{= -2\ln|x+1| + \ln(x^2+1) + 2\arctan x + C}$$

*Verified.*

*Marking: 2 for the linear numerator, 2 for splitting it, 1 for the arctangent, 1 for the check. **Using a constant numerator over $x^2+1$ is the standard error** and makes the system unsolvable — if a student reports "no solution", this is why, and it is worth 2 marks of partial credit for noticing the inconsistency.*

### C5 (6) — $\int\frac{x^3+4}{x^2+4}\,dx$

**Improper — divide first:** $\dfrac{x^3+4}{x^2+4} = x + \dfrac{-4x+4}{x^2+4}$.

$$\int = \int x\,dx - 4\int\frac{x}{x^2+4}dx + 4\int\frac{dx}{x^2+4}$$

$$\boxed{= \frac{x^2}{2} - 2\ln(x^2+4) + 2\arctan\frac x2 + C}$$

*Verified.*

*Marking: **3 for dividing first.** This is the problem D2 dissects; a student who decomposed directly should get 0 for method here and can recover the marks in D2 by diagnosing it.*

---

## Part D — Concept (10 pts each)

### D1 (10) — the theorem

**The four steps, and what each needs:**

1. **Polynomial division** reduces $\frac PQ$ to (polynomial) + (proper fraction). *If this failed, the decomposition in step 3 would be invalid — see D2.* Polynomials integrate trivially.
2. **Factorisation over $\mathbb R$**: every real polynomial factors into linear factors and irreducible quadratics. *This is a consequence of the Fundamental Theorem of Algebra plus the fact that complex roots of real polynomials come in conjugate pairs.* If cubics could be irreducible, there would be a case with no known antiderivative.
3. **Partial fraction decomposition** splits the proper fraction into one group of terms per factor. *This always has a solution — the linear system is guaranteed non-singular.*
4. **Each piece is integrable in closed form**: $\frac{A}{x-r}$, $\frac{A}{(x-r)^k}$, $\frac{Ax+B}{x^2+bx+c}$ are all on the catalogue.

**Since every step always succeeds, the antiderivative always exists.**

**What can appear, and why:**

| Answer type | Comes from |
|---|---|
| Polynomial | the division step (improper fractions only) |
| Logarithm | distinct linear factors, **and** the $x$-part of an irreducible quadratic |
| Rational function | **repeated** linear factors, powers $\ge2$ |
| Arctangent | the **constant part** of an irreducible quadratic |

*Marking: 6 for the four steps (1.5 each, with the "what would fail" comment), 4 for the answer-type table. **Step 2 is the one most often omitted** — students recite the algorithm without noticing it rests on a theorem about factorisation. Award the mark only if the factorisation guarantee is mentioned.*

### D2 (10) — the student's error

**(a)** The student **omitted Step 0: they did not check that the fraction is proper.** Here $\deg(x^3+4) = 3 > 2 = \deg(x^2+4)$, so the fraction is **improper** and must be divided before any decomposition is written.

**(b)** The contradiction $0=1$ is not a sign that the integral is impossible — it is the algebra **correctly reporting that no such decomposition exists.** The form $\frac{Ax+B}{x^2+4}$ describes only *proper* fractions: as $x\to\infty$ it tends to 0, whereas the original tends to $\infty$ like $x$. **No choice of $A,B$ can fix a mismatch in growth rate**, and the inconsistent equation is exactly that fact expressed in coefficients.

**(c)** Dividing: $\dfrac{x^3+4}{x^2+4} = x+\dfrac{4-4x}{x^2+4}$, giving

$$\frac{x^2}{2}-2\ln(x^2+4)+2\arctan\frac x2 + C$$

*(as in C5)*

**(d)** By the theorem in D1, **every** rational function has an elementary antiderivative. $\frac{x^3+4}{x^2+4}$ is a rational function, so "cannot be done" was never available as a conclusion — the only possibility was that the method had been misapplied.

*Marking: 3 + 3 + 2 + 2. **(b) is the discriminating part.** Full marks require the student to see the contradiction as informative rather than as failure — ideally with the growth-rate argument. "Because they didn't divide" repeats (a) and earns 1 of the 3.*

*(d) is a one-sentence answer but an important habit: **when a general theorem guarantees a result, a contradiction in your working locates an error in the working**, not a counterexample to the theorem.*

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | The three patterns; ranges; converting back |
| B (5 × 6) | 30 | Completing the square; splitting; division; rationalizing |
| C (5 × 6) | 30 | All four decomposition cases |
| D (2 × 10) | 20 | The theorem, and a diagnostic error |
| **Total** | **100** | |

---

## Diagnostic Notes

| Question | Weakness it reveals | Bites in |
|---|---|---|
| **A3** | Not stating the domain / range | Week 3, where improper integrals live or die on limits |
| **B2** | Sign handling when completing the square | Midterm 1 |
| **B4 / C5 / D2** | Not checking whether a fraction is proper | Anywhere a rational function appears |
| **C4** | Constant numerator over an irreducible quadratic | Week 11 (partial fractions in ODEs) |

**Midterm 1 covers Weeks 0–4 and is two weeks away.** Parts A–C of this set are a fair sample of its computational half; students who found them slow rather than hard need volume practice, not more theory.

---

*MATH 142 · Week 2 · PS 2 Solutions · Instructor Only*
