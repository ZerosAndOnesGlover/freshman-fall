# MATH 142 · Calculus II
## Course Retrospective
### Read this **after** the final exam

---

> **This is not revision.** If the exam has not happened, close it — there is nothing here that will
> earn you a mark, and the revision guide in this folder is where your time should go.
>
> **Afterwards, it is worth twenty minutes.**

---

## 1. What The Course Actually Was

**The catalogue says "integration techniques and series." That is the syllabus, not the subject.**

The subject was this: **you were handed problems whose answers exist and whose formulas do not**, over and over, and taught what to do about it. Every week supplied a new instance.

| Week | The formula that did not exist | What you did instead |
|---|---|---|
| 0 | $\int e^{-x^2}dx$ | Simpson's rule, order 4 |
| 1 | — | the Wallis product, order 1, and useless |
| 2 | — | bounded $\pi$ between two rationals |
| 3 | the boundary between $p=1$ and $p>1$ | proved it, because no computation could find it |
| 4 | $\int\sqrt{1+e^{2x}}\,dx$ *(actually elementary)* | learned that "looks intractable" is not evidence |
| 5 | the ellipse's perimeter | Ramanujan's approximation, error $3.7\times10^{-9}$ |
| 6 | $\sqrt2$ | an iteration from 1700 BC — 48 digits in six steps |
| 7 | $\sum\frac{\ln n}{n^2}$ | Integral-Test bounds, averaged: order $1\to3$ |
| 8 | the sum of a conditionally convergent series | discovered it is not a number at all |
| 9 | the value of a series at its endpoint | tested the endpoints |
| 10 | $\int_0^1e^{-x^2}dx$, again | **13 terms, error $5.6\times10^{-12}$** |
| 11 | $y'=x^2+y^2$ | RK4: $y(1)=0.350231844$ |
| 12 | $\int_0^\infty e^{-x^2}dx$ | quadrature + a proved tail bound: $8.9\times10^{-16}$ |

**Week 0 asked for $\int_0^1e^{-x^2}dx$ and settled for 128 function evaluations from Simpson's rule.** Week 10 returned to it and got more accuracy from **thirteen numbers**, with an error bound proved before the computation started. **That gap is the course.**

---

## 2. The One Number

**Eleven labs. Every one of them ended in a ratio of consecutive errors.**

| method | order | what it bought |
|---|---|---|
| Wallis product | 1 | $8\times10^9$ factors for 10 digits |
| Basel partial sums | 1 | $10^{10}$ terms |
| Euler's method | 1 | $1.4\times10^{10}$ steps |
| Trapezoid, midpoint | 2 | usable |
| Improved Euler | 2 | 2 evaluations per step |
| **Simpson's rule** | **4** | 128 points |
| **RK4** | **4** | 320 steps for 12 digits |
| **Newton / Babylonian** | **quadratic** | 48 digits in six steps |

**Simpson's rule and RK4 were measured eleven weeks apart, on completely unrelated problems, and both gave a ratio of 16.** That is not a coincidence; it is what $p=4$ means.

> **Euler's method and RK4 solve the same equation with the same arithmetic.** RK4 does four times
> the work per step and wins by a factor of two billion.
>
> **Not elegance. Not age. Not cleverness. The exponent $p$ in $\text{error}\approx Ch^p$.**

---

## 3. The Machine Was Wrong Thirteen Times

**Every week of this course documented a computational failure**, and none of them was exotic. They were the default tools, used the obvious way.

| Week | What failed | How it was caught |
|---|---|---|
| 0–5 | integrals returned unevaluated | it said so |
| 2 | *(mine)* $\pi-\frac{355}{113}$ has the sign backwards | positivity of the integrand |
| 3 | the $p$-test boundary is invisible numerically | $p=1.01$ reaches 90% of its value at $T=10^{100}$ |
| 7 | `nsum` gave $0.9367$ for $-\zeta'(2)=0.9375$ | **a partial sum exceeded the reported total** |
| 7 | `nsum` gave $1.07072$ for $\frac{\pi-1}{2}=1.07080$ | same check |
| 7 | `nsum` gave $2.0605$ for $2.0659$ | same check |
| 9 | at $N=200$, $x=0.99,1.00,1.01$ give $4.56,5.88,9.54$ | **no computation can locate a radius** |
| 11 | `dsolve` raised an exception | it said so |
| 12 | the quadratic formula, wrong by **25%** | rationalised numerator agreed to 16 digits |
| 12 | $\frac{1-\cos x}{x^2}$ returned $0.0$ | the identity $2\sin^2(x/2)$ returned $0.5$ |
| 12 | a **convergent** series returned 3 correct digits | quadrature agreed with nothing it said |
| 12 | the *same* series, summed two ways, disagreed in the 2nd decimal | the two runs |
| 12 | two routines gave two different wrong values for $\int_1^\infty\frac{2+\sin x}{x^2}dx$ | a closed form and an oscillation-aware method |

**Not one of these was caught by looking harder at the output.** Every single one was caught by an independent check that cost less than the original computation: a sign, a bound, a partial sum, a substitution, a second method, a refinement.

> **That is the transferable skill.** You will forget the trig substitutions. **You should not forget
> that a number on a screen is a claim, and claims get checked.**

---

## 4. The Three Weeks That Were Actually Hard

**Not the ones with the most algebra.**

**Week 3** was hard because it asked you to distinguish two things that look identical. $\sum\frac1{n^{1.01}}$ converges and $\sum\frac1n$ does not, and **no amount of computation will show you the difference** — at $T=10^6$ the two integrals are $12.9$ and $13.8$. The proof is the only access.

**Week 8** was hard because it broke a rule you had believed since primary school. **A conditionally convergent series can be rearranged to sum to anything you like** — you did it, with 300,000 terms reaching $1$, $\pi$, $0$, and $-2$. **Addition is not commutative in the infinite case**, and there is no way to be told that gently.

**Week 10** was hard because it was easy. Taylor series feel mechanical, and then $e^{-1/x^2}$ arrives: **infinitely differentiable, Maclaurin series identically zero, equal to the function at exactly one point.** Everything you had assumed about "smooth" was a habit, not a theorem.

---

## 5. What You Should Be Able To Do Now

**Not "integrate things." Anyone can be taught to integrate things.**

1. **Look at a problem with no chapter heading and choose a method.**
2. **Prove that something converges** — and know that convergence is not the same as being computable.
3. **Bound an error before computing the quantity**, and recognise a bound that is tight *(PS 12's $9.688\times10^{-8}$ against an actual $9.661\times10^{-8}$)* from one that is useless.
4. **Measure an order of convergence** from a table of errors, and know that two data points cannot establish one.
5. **Check a machine's answer** without recomputing it.

**The fifth is the one that will still be with you in ten years.**

---

## 6. What This Course Did Not Tell You

**In the interest of honesty, here is what was assumed away.**

- **Completeness of $\mathbb R$.** The Monotone Convergence Theorem of Week 6 was stated, not proved. It cannot be proved from anything in this course; it is an axiom about the real numbers.
- **Uniform convergence.** Week 9 differentiated and integrated power series term by term under a licence you were given but not shown. The theorem behind it is the centre of a real analysis course.
- **Exact arithmetic.** Every proof here assumed it. **Week 12 showed you what that assumption costs**, and that is all this course had room for.
- **The Gaussian integral.** $\int_0^\infty e^{-x^2}dx=\frac{\sqrt\pi}{2}$ was quoted and never derived, because the derivation needs a double integral in polar coordinates.

**These are not gaps to worry about. They are the next courses**, and the map is in Wednesday's lecture and this week's reference sheet.

---

## 7. Last Thing

**You spent thirteen weeks in the company of problems that do not have answers in closed form** — which is to say, almost all problems. **The habit that got you through them is worth more than the techniques.**

> **Name the method. Check the hypotheses. Bound the error. Substitute the answer back.**
>
> **And when the machine tells you something, ask how you would know if it were wrong.**

---

*MATH 142 · Calculus II · Course Retrospective*
