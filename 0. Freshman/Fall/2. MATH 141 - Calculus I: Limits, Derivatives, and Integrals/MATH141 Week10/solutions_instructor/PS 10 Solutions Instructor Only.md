# MATH 141 · Problem Set 10 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Revised 2026-09-26 to match the 7-problem, 14-part set; items are numbered as in the new set.*

---

## Marking Scheme

Point values are printed per problem on the problem set. Within each problem, split the marks:

- **Method (≈60%).** Correct technique named and set up: the right rule or theorem, hypotheses checked where the theorem requires it, and the symbolic work shown before any numerical evaluation.
- **Execution (≈40%).** Correct algebra and simplification, correct final form, and any domain restrictions or constants of integration stated.

A bare answer with no working earns at most the execution marks — and in proof problems ("show that", "prove"), no marks at all, since the reasoning *is* the deliverable.

**Carry-through.** Penalise a given error once. If the student proceeds correctly from their own wrong intermediate value, award the downstream marks in full.

**Equivalent forms.** Accept any algebraically equivalent answer — factored or expanded, and trigonometric identities applied or not — unless the problem explicitly demands a particular form.

### Common errors in this problem set

**1. Not changing the limits after u-substitution.** With a definite integral either convert the limits to u, or convert back to x before evaluating. Substituting x-limits into a u-expression is the most common substitution error.

**2. Forgetting du.** The substitution is incomplete until dx is fully expressed in terms of du; a leftover x that cannot be eliminated means the substitution was the wrong choice.

**3. Misapplying symmetry.** ∫_{−a}^{a} f = 0 requires f **odd**; = 2∫₀^a f requires f **even**. Students must state which and why — asserting symmetry without checking f(−x) earns no method marks.

**4. Poor factor choice in integration by parts.** LIATE is a heuristic, not a theorem, but choosing u badly usually yields a harder integral than the original — that is the diagnostic. For the circular cases, the integral must be solved algebraically after it reappears.

---


## Problem 1 — Substitution (18)

**(a)** $u=5x^2+2$, $du=10xdx$. $\int x\sqrt{5x^2+2}dx=\frac1{10}\int\sqrt u\,du=\frac1{10}\cdot\frac{2}3u^{3/2}+C=\frac1{15}(5x^2+2)^{3/2}+C$

**(b)** $u=1+\tan x$, $du=\sec^2x\,dx$. $\int(1+\tan x)^{-3}\sec^2x\,dx=\int u^{-3}du=-\frac{u^{-2}}2+C=-\frac1{2(1+\tan x)^2}+C$

**(c)** $u=1/x$, $du=-\frac1{x^2}dx$. $\int\frac{e^{1/x}}{x^2}dx=-\int e^udu=-e^u+C=-e^{1/x}+C$

---

## Problem 2 — Definite Integrals by Substitution (16)

**(a)** $u=1+\sqrt x$, $du=\frac1{2\sqrt x}dx$, so $\frac{dx}{\sqrt x}=2du$. Limits: $x=1\to u=2$; $x=4\to u=3$.

$\int_2^3\frac{2\,du}u=2[\ln u]_2^3=2(\ln3-\ln2)=2\ln(3/2)$

**(b)** $u=1+\ln x$, limits: $x=1\to u=1$; $x=e\to u=2$.

$\int_1^2\frac{du}u=[\ln u]_1^2=\ln2$

---

## Problem 3 — Symmetry (10)

**(a)** $f(x)=x^5-3x^3+2x$ is odd (all odd powers). $\int_{-4}^4f\,dx=0$

**(b)** $\tan^3x$ is odd ($\tan(-x)=-\tan x$, so $\tan^3(-x)=-\tan^3x$). $\int_{-\pi/4}^{\pi/4}\tan^3x\,dx=0$

---

## Problem 4 — Integration by Parts (18)

**(a)** $u=x,dv=\cos3x\,dx$; $du=dx,v=\frac13\sin3x$

$\int x\cos3x\,dx=\frac{x}3\sin3x-\frac13\int\sin3x\,dx=\frac x3\sin3x+\frac19\cos3x+C$

**(b)** $u=\ln(2x),dv=dx$; $du=\frac1xdx,v=x$

$\int\ln(2x)dx=x\ln(2x)-\int1\,dx=x\ln(2x)-x+C$

**(c)** $u=\arctan(2x),dv=dx$; $du=\frac2{1+4x^2}dx,v=x$

$\int\arctan(2x)dx=x\arctan(2x)-\int\frac{2x}{1+4x^2}dx$

Let $w=1+4x^2,dw=8x\,dx$: $\int\frac{2x}{1+4x^2}dx=\frac14\int\frac{dw}w=\frac14\ln|w|=\frac14\ln(1+4x^2)$

$=x\arctan(2x)-\frac14\ln(1+4x^2)+C$

---

## Problem 5 — Repeated and Circular Parts (16)

**(a)** $\int x^2\sin x\,dx$: $u=x^2,dv=\sin x\,dx$; $du=2x\,dx,v=-\cos x$

$=-x^2\cos x+2\int x\cos x\,dx$

From a Problem 4(a)-style computation: $\int x\cos x\,dx=x\sin x+\cos x$ (standard result)

$=-x^2\cos x+2(x\sin x+\cos x)+C=-x^2\cos x+2x\sin x+2\cos x+C$

**(b)** $I=\int e^{-x}\cos x\,dx$. $u=\cos x,dv=e^{-x}dx$; $du=-\sin x\,dx,v=-e^{-x}$

$I=-e^{-x}\cos x-\int e^{-x}\sin x\,dx$

For the new integral: $u=\sin x,dv=e^{-x}dx$; $du=\cos x\,dx,v=-e^{-x}$

$\int e^{-x}\sin x\,dx=-e^{-x}\sin x+\int e^{-x}\cos x\,dx=-e^{-x}\sin x+I$

$I=-e^{-x}\cos x-[-e^{-x}\sin x+I]=-e^{-x}\cos x+e^{-x}\sin x-I$

$2I=e^{-x}(\sin x-\cos x)\implies I=\frac{e^{-x}(\sin x-\cos x)}2+C$

---

## Problem 6 — Mixed Techniques (10)

$\int x^3e^{x^2}dx$: let $w=x^2$ first, $dw=2x\,dx$, so $x^2\cdot x\,dx=w\cdot\frac{dw}2$

$=\frac12\int we^wdw$

By parts: $u=w,dv=e^wdw$; $=\frac12[we^w-e^w]+C=\frac12e^w(w-1)+C=\frac12e^{x^2}(x^2-1)+C$

---

## Problem 7 — Choosing the Technique (12)

With $u=x,dv=e^{x^2}dx$: finding $v=\int e^{x^2}dx$ is IMPOSSIBLE in elementary terms — $e^{x^2}$ has no elementary antiderivative. Integration by Parts requires being able to find $v$, so this choice fails immediately at step 2 of the method. Correct approach: substitution. Let $w=x^2,dw=2x\,dx$: $\int xe^{x^2}dx=\frac12\int e^wdw=\frac12e^{x^2}+C$.

---

*MATH 141 · Week 10 · Problem Set 10 Solutions · © CSE Department*
