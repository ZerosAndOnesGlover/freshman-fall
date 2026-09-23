# MATH 142 · Calculus II
## Lab 02: Partial Fractions, and a Proof that $\tfrac{22}{7} > \pi$
### Week 2 Lab Session

**Date:** Wednesday 10 February 2027 · 15:00–16:50 · Lab section (Week 3) — covers Week 2 (Lectures 1–3)

---

**Duration:** 2 hours
**Format:** Individual or pairs (pairs submit separate reports)
**Graded on:** completion + correctness — **100 points**
**Tools required:** Python 3 with `sympy` (`pip install sympy`) and `fractions`

> **SymPy — every call the MATH 142 labs use, in one place.** No course has taught SymPy, so this box
> is the whole of what you need; nothing else from the library is expected, in this lab or later ones.
>
> ```python
> import sympy as sp
> x, n, t = sp.symbols('x n t')          # symbols to build expressions with: (x**2 + 1)/(x - 1)
> sp.apart(e, x)                          # partial fractions (Week 2)
> sp.together(e);  sp.simplify(e)         # recombine over one denominator; simplify
> sp.div(p, q, x)                         # polynomial division -> (quotient, remainder)
> sp.diff(F, x)                           # derivative
> sp.integrate(f, x)                      # antiderivative
> sp.integrate(f, (x, a, b))              # definite integral; use sp.oo for infinity
> sp.limit(e, n, sp.oo)                   # a limit
> sp.series(sp.atan(x), x, 0, 10)         # Maclaurin expansion up to (not including) x**10
> sp.sin, sp.cos, sp.exp, sp.log, sp.sqrt, sp.pi, sp.E   # use these, not math's, inside expressions
> ```
>
> **SymPy checks your hand working; it never replaces it.** Every lab asks for the hand derivation first.

---

## Overview

Lecture 3 proved that **every rational function has an elementary antiderivative**, by an algorithm. This lab uses that algorithm to prove something specific and surprising:

$$\int_0^1\frac{x^4(1-x)^4}{1+x^2}\,dx \;=\; \frac{22}{7}-\pi$$

The integrand is a rational function, so the theorem guarantees the integral can be evaluated exactly — and it comes out as a rational number minus $\pi$.

**And now the point.** On the open interval $(0,1)$ the integrand is **strictly positive**: $x^4>0$, $(1-x)^4>0$, $1+x^2>0$. A positive function has a positive integral. Therefore

$$\frac{22}{7}-\pi > 0 \implies \boxed{\frac{22}{7} > \pi}$$

The approximation you were given in school is **not** equal to $\pi$, and it errs on the high side. The proof is one Week 2 integral.

Bounding the same integral will then give you $\pi$ to three decimal places — from a polynomial division.

---

## Part A — The Machinery (25 pts)

**A1 (10 pts).** Write a function that takes a rational function and returns its partial fraction decomposition, then **verifies** the decomposition by recombining it.

```python
import sympy as sp
x = sp.symbols('x')

def decompose_and_check(expr):
    """Return (decomposition, ok) where ok is True iff it recombines to expr."""
    d = sp.apart(expr, x)
    ok = sp.simplify(sp.together(d) - expr) == 0
    return d, ok
```

Run it on all four cases from Lecture 3 and confirm each recombines:

| | Expression | Case |
|---|---|---|
| (i) | $\dfrac{x+5}{(x+1)(x-2)}$ | distinct linear |
| (ii) | $\dfrac{3x+1}{(x-1)^2(x+2)}$ | repeated linear |
| (iii) | $\dfrac{x^2+1}{(x+1)(x^2+4)}$ | irreducible quadratic |
| (iv) | $\dfrac{2x^2-x+4}{x^3+4x}$ | needs factoring first |

**Report the decomposition and the check for each.**

**A2 (8 pts).** Now try your function on $\dfrac{x^3+4}{x^2+4}$ — an **improper** fraction.

Report exactly what `sp.apart` returns. Does it still recombine correctly? Explain what `apart` did with the improper part, and why the answer is not of the form "constants over factors".

**A3 (7 pts).** Write a function that, given a rational function, returns its antiderivative and **verifies it by differentiation**:

```python
def integrate_and_check(expr):
    F = sp.integrate(expr, x)
    return F, sp.simplify(sp.diff(F, x) - expr) == 0
```

Run it on all five expressions above. Report which verify.

*This is the "check by differentiating" rule of the course, automated.*

---

## Part B — The Integral (25 pts)

**B1 (8 pts).** Expand $x^4(1-x)^4$ as a polynomial. Report the result.

**B2 (10 pts).** Divide it by $1+x^2$. Report the **quotient** and the **remainder**, and confirm that

$$\frac{x^4(1-x)^4}{1+x^2} = (\text{quotient}) + \frac{(\text{remainder})}{1+x^2}$$

*Use `sp.div(numerator, 1 + x**2, x)`, then verify the identity symbolically.*

**B3 (7 pts).** Integrate the right-hand side **term by term** from 0 to 1, giving each term's value as an exact fraction (and the last as a multiple of $\pi$). Sum them.

Confirm the total is exactly $\dfrac{22}{7}-\pi$, and report its decimal value to 15 significant figures.

---

## Part C — The Bounds (25 pts)

Knowing $\frac{22}{7}-\pi$ exactly is only useful if you can bound it. On $[0,1]$:

$$1 \;\le\; 1+x^2 \;\le\; 2$$

**C1 (8 pts).** Deduce that

$$\frac{1}{2}\int_0^1 x^4(1-x)^4\,dx \;\le\; \int_0^1\frac{x^4(1-x)^4}{1+x^2}\,dx \;\le\; \int_0^1 x^4(1-x)^4\,dx$$

State which property of the integral you used. *(It is from Week 0.)*

**C2 (7 pts).** Evaluate $\displaystyle\int_0^1 x^4(1-x)^4\,dx$ exactly. Report it as a fraction.

**C3 (10 pts).** Combine C1 and C2 with $\int = \frac{22}{7}-\pi$ to produce **explicit rational bounds on $\pi$**:

$$\underline{\phantom{XXXX}} \;\le\; \pi \;\le\; \underline{\phantom{XXXX}}$$

Report both as exact fractions **and** as decimals to 15 places. Then:

- (a) Verify the true value of $\pi$ lies inside.
- (b) How many decimal places of $\pi$ does this pin down?
- (c) How wide is the interval?

---

## Part D — Doing Better (15 pts)

The same trick works with a better-chosen integrand.

**D1 (9 pts).** Evaluate, exactly,

$$\int_0^1\frac{x^8(1-x)^8\big(25+816x^2\big)}{3164\,(1+x^2)}\,dx$$

**You should get a rational number minus $\pi$** (or $\pi$ minus a rational — report which way round it comes out, and be careful, because the direction is the whole content of the next part).

**D2 (6 pts).** The rational number appearing should be $\frac{355}{113}$ — a famous approximation to $\pi$, accurate to six decimal places.

- (a) From the **sign** of your integral, state whether $\frac{355}{113}$ is greater or less than $\pi$. Justify from the positivity of the integrand, not from a decimal comparison.
- (b) Report the value of the integral to 15 significant figures, and compare with the error $\left|\pi - \frac{355}{113}\right|$.

---

## Part E — Reflection (10 pts)

**E1 (5 pts).** In Lab 0 you computed $\int_0^1e^{-x^2}dx$ **numerically** to 10 decimal places. In this lab you computed an integral **exactly**, and the exact answer proved an inequality.

Explain what an exact evaluation gave you here that a numerical one could not. *(Consider: could you have proved $\frac{22}{7}>\pi$ by computing the integral numerically? What would that argument be missing?)*

**E2 (5 pts).** The theorem in Lecture 3 says every rational function has an elementary antiderivative. This lab is an instance.

In two or three sentences, say why the theorem matters *practically* — what does it let you do, or stop worrying about, that you could not for a general integrand?

---

## What to Submit

1. Your decomposition/verification functions and their output on all five expressions (Part A)
2. The expansion, division, and term-by-term integration (Part B)
3. Your bounds on $\pi$, exact and decimal, with the verification (Part C)
4. The $\frac{355}{113}$ result and the sign argument (Part D)
5. Parts E1 and E2

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A | 25 | Decomposition, verification, the improper case |
| B | 25 | Division and exact term-by-term integration |
| C | 25 | Bounding, and rational bounds on $\pi$ |
| D | 15 | The $\frac{355}{113}$ companion and the sign argument |
| E | 10 | Exact versus numerical |
| **Total** | **100** | |

---

## A Note on the Source

The integral in Part B is due to **Donald Percy Dalzell** (1898–1988), a British electrical engineer, who published it as "On 22/7" in the *Journal of the London Mathematical Society* in **1944**, and derived it again in the Cambridge student journal *Eureka* in 1971 — the version most often cited.

Evaluating it was **the first problem on the 1968 Putnam Competition**.

Every step of it is Week 2 material.

---

*An exact technique proved an inequality that no amount of numerical computation could establish. That is what Part E is about.*
