# MATH 142 · Calculus II
## Lab 04 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures below were produced by running the lab.

---

## Part A — The Horn's Volume and Surface (25 pts)

### A1 (8) — volume

$$V = \pi\int_1^\infty\left(\frac1x\right)^2dx = \pi\int_1^\infty\frac{dx}{x^2} = \pi\lim_{T\to\infty}\left(1-\frac1T\right) = \boxed{\pi}$$

**Converges by the $p$-test with $p=2>1$** (Week 3, Lecture 1).

*Verified symbolically: `sympy` returns `pi`.*

*Marking: 3 for the integral, 3 for the limit, **2 for naming the $p$-test with its $p$.***

### A2 (10) — surface area

$$S = 2\pi\int_1^\infty\frac1x\sqrt{1+\left(\frac{-1}{x^2}\right)^2}\,dx = 2\pi\int_1^\infty\frac1x\sqrt{1+\frac1{x^4}}\,dx$$

**Direct comparison.** For all $x\ge1$,

$$\sqrt{1+\frac{1}{x^4}}\ \ge\ \sqrt1 = 1 \implies \frac1x\sqrt{1+\frac1{x^4}}\ \ge\ \frac1x\ >0$$

$\int_1^\infty\frac{dx}{x}$ **diverges** ($p=1$), and we have bounded our integrand **below** by a divergent one — the correct direction for proving divergence. **Therefore $S=\infty$.**

*Verified symbolically: `sympy` returns `oo`.*

*Marking: 3 for the correct surface integral (with $ds$, not $dx$), 4 for the comparison, **3 for stating the direction is correct.** A student who bounds **above** by something divergent has made the standard error and earns 4 of 10 — the inequality is true but proves nothing.*

### A3 (7)

`sympy` returns `pi` and `oo` respectively.

*Marking: 7 for both, reported honestly. **If a student's CAS struggles with the surface integral**, numerical evidence plus the A2 proof is fully acceptable — the proof is the mathematics; the CAS is the check.*

---

## Part B — Truncating the Horn (25 pts)

### B1 (10)

$$V(T) = \pi\int_1^T\frac{dx}{x^2} = \pi\left(1-\frac1T\right)$$

$S(T)$ has **no elementary closed form** — the integrand $\frac1x\sqrt{1+x^{-4}}$ is an algebraic function whose antiderivative involves inverse hyperbolic terms and is not worth writing down. Compute numerically.

| $T$ | $V(T)$ | $S(T)$ |
|---|---|---|
| $10$ | 2.82743 | 15.1774 |
| $10^2$ | 3.11018 | 29.6451 |
| $10^3$ | 3.13845 | 44.1127 |
| $10^4$ | 3.14128 | 58.5802 |
| $10^6$ | 3.14159 | 87.5154 |

*Marking: 5 for $V(T)$ in closed form, 5 for the numerical $S(T)$ table. **Do not penalise a student who found a closed form for $S(T)$** — one exists in terms of $\operatorname{arcsinh}$; it is simply not illuminating.*

### B2 (8)

| $T$ | $S(T)$ | $2\pi\ln T$ | ratio |
|---|---|---|---|
| $10$ | 15.1774 | 14.4676 | 1.04907 |
| $10^2$ | 29.6451 | 28.9351 | 1.02454 |
| $10^3$ | 44.1127 | 43.4027 | 1.01636 |
| $10^4$ | 58.5802 | 57.8703 | 1.01227 |
| $10^6$ | 87.5154 | 86.8054 | 1.00818 |

**The ratio approaches 1.**

**Why that is expected:** the only difference between $S(T)$ and the bound is the factor $\sqrt{1+x^{-4}}$, and $x^{-4}\to0$ very rapidly. By $x=10$ the factor is $\sqrt{1.0001}\approx1.00005$ — indistinguishable from 1. **So almost all of the surface integral's growth comes from the $\frac1x$, i.e. from $\ln T$**, and the excess is a bounded constant contributed almost entirely near $x=1$.

*Marking: 5 for the table, 3 for the explanation. **Full marks require noting that $x^{-4}\to0$ fast**, so the extra factor contributes a bounded amount concentrated near the lower limit.*

### B3 (7)

**(a)** At $T=10^6$, $V = \pi(1-10^{-6}) = 3.14159$ — within $3\times10^{-6}$ of $\pi$. **Visibly converged.**

**(b)** $S(10^6) = 87.5$ — a modest number.

**(c)** **The volume's convergence is numerically obvious; the surface's divergence is not.**

$V(T)$ approaches its limit like $1/T$ — fast, and the digits visibly stabilise. $S(T)$ grows like $2\pi\ln T$, so it looks like a slowly-increasing quantity that could plausibly be settling.

**This is Lab 3's finding exactly**: logarithmic divergence is invisible to computation. A student shown only the $S(T)$ column, with no formula, could not tell it from a convergent sequence.

*Marking: 2 + 2 + 3. **The explicit link to Lab 3 is required for the last 3.***

---

## Part C — The Painter's Paradox (15 pts)

### C1 (8)

**The false step is "no finite amount of paint can cover an infinite area."**

That is true only for a coating of **constant positive thickness**. Covering an area $A$ with a layer of thickness $d$ requires volume $A\times d$, which is infinite when $A$ is — **but nothing requires the coating to have constant thickness.**

Filling the horn with $\pi$ units of liquid does coat the whole interior surface: the layer simply becomes **thinner and thinner** as you go along the horn, tending to zero thickness. **An infinite area coated by a layer of vanishing thickness can have finite volume**, and that is precisely what $V=\pi$ is telling you.

**The two operations are different:**

| Operation | Requires |
|---|---|
| Fill the horn | a **volume** — finite, $=\pi$ |
| Coat with thickness $d>0$ | **area** $\times\,d$ — infinite |

*Marking: 8. **Full marks require identifying constant thickness as the smuggled assumption.** "Because maths and physics are different" earns 2. "Because the horn is infinitely long" earns 2 — true but not the flaw.*

### C2 (7)

**(a)** The horn's radius at $x$ is $\frac1x$, so the radius drops below $d$ when

$$\frac1x < d \iff \boxed{x > \frac1d}$$

**(b)** Beyond that point the horn is **narrower than the paint layer is thick.** A coating of thickness $d$ cannot physically exist there — the layer would have to overlap itself, or the "coating" simply fills the tube completely.

**(c)** So "painting with thickness $d$" is not a well-defined operation on the whole horn at all: past $x=1/d$ it degenerates into "filling". **Filling is bounded by the volume ($\pi$); coating at fixed thickness is bounded by area × $d$ ($\infty$)** — and the two only agree while the tube is wider than the coat.

**Concretely:** with a realistic $d=10^{-4}$ m, the coating description fails beyond $x=10^{4}$ — and the horn continues forever past that.

*Marking: 3 + 2 + 2. **(a) must be $x>1/d$**, and (c) must state that the two operations coincide only where the tube is wider than the layer.*

---

## Part D — Polygon to Curve (25 pts)

**Exact:** $L = \dfrac{\sqrt5}{2}+\dfrac{\operatorname{arcsinh}2}{4} = 1.4789428575445975$

### D1 (8), D2 (7), D3 (5)

| $n$ | $L_n$ | error $L-L_n$ | ratio | $n^2\cdot$err |
|---:|---|---|---:|---|
| 2 | 1.460404813240945 | 1.854e-02 | — | 0.074152 |
| 4 | 1.474280475709316 | 4.662e-03 | 3.976 | 0.074598 |
| 8 | 1.477777985131388 | 1.165e-03 | 4.002 | 0.074552 |
| 16 | 1.478651686954534 | 2.912e-04 | 4.001 | 0.074540 |
| 32 | 1.478870067878563 | 7.279e-05 | 4.000 | 0.074537 |
| 64 | 1.478924660314619 | 1.820e-05 | 4.000 | 0.074536 |
| 128 | 1.478938308248764 | 4.549e-06 | 4.000 | 0.074536 |
| 256 | 1.478941720221367 | 1.137e-06 | 4.000 | 0.074536 |
| 512 | 1.478942573213835 | 2.843e-07 | 4.000 | 0.074536 |

**D2:** ratio $\to 4 = 2^2$, so **order $p=2$** — the same reasoning as Labs 0 and 3 ($\text{ratio}=2^p$).

**D3:** $n^2\times$error $\to \boxed{0.074536}$.

*Marking D1: 8 for the table. D2: 7, of which 4 for $p=2$ and 3 for deriving it from the ratio. D3: 5 for the constant.*

### D4 (5)

**(a)** Every error $L-L_n$ is **positive**, so $L_n < L$: **the polygon always underestimates.**

**(b)** **A straight chord is the shortest path between its two endpoints**, and the arc joining them is a path between the same two points. So each chord is no longer than the arc it replaces, and summing over all $n$ pieces gives $L_n\le L$ — **for every curve and every $n$.**

*(Equality only for a straight line.)*

*Marking: 2 + 3. **The one-line reason must be the shortest-path property**; "because the curve bends" earns 1.*

---

## Part E — Reflection (10 pts)

### E1 (5)

**Lab 4 entry: numerics worked well** — order 2, with the error falling by a factor of 4 per doubling and a clean constant $0.0745/n^2$. Ten-digit accuracy is reachable.

**It most resembles Lab 0**, where numerics also succeeded on a *value* question with a good convergence order.

*Marking: 3 for the entry, 2 for identifying Lab 0. **Accept Lab 1 as the comparison if justified** — a student arguing that order 2 is mediocre next to Simpson's order 4, and that this is a Lab-1-style "works but slowly" case, has read the tables carefully and is right to notice the order is lower.*

### E2 (5)

**Part D could have been done numerically alone. Part A could not.**

Part D asks **"what is this number, and how fast do we approach it?"** — a quantitative question about a finite quantity, which computation answers well.

Part A asks **"is this quantity finite?"** — a statement about a limit over an infinite domain. No table of $S(T)$ values decides it; indeed Part B shows $S(10^6)=87.5$, a perfectly ordinary-looking number for a quantity that is infinite. **Only the comparison argument settles it.**

*Marking: 5. **The distinction required is value-question versus existence-question**, as established in Lab 3. A student who says "Part A involves infinity" earns 2 without that framing.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 25 |
| B | 25 |
| C | 15 |
| D | 25 |
| E | 10 |
| **Total** | **100** |

---

## Checkoff Checklist

1. A1 names the $p$-test **with $p=2$**
2. **A2's comparison points the right way** (bounded *below* by a divergent)
3. B2's ratio $\to1$, explained via $x^{-4}\to0$
4. **B3(c) links to Lab 3's logarithmic invisibility**
5. **C1 identifies constant thickness as the false assumption**
6. C2(a) gives $x>1/d$
7. D2 gives order 2 **from the ratio**
8. **D4(b) uses the shortest-path property**
9. E2 distinguishes value from existence

---

## Note for the Debrief

Two things, and the second matters more:

> **First:** Gabriel's Horn is not a paradox. It is two integrals of the same curve landing on
> opposite sides of the $p=1$ threshold — $\int x^{-2}$ converges, $\int x^{-1}$ does not. **Everything
> strange about it is Week 3, and nothing about it is strange once you know where the threshold is.**

> **Second:** this lab had one half where computation was the right tool and one where it was useless,
> and they sat side by side on the same object. **Part D measured a convergence rate beautifully.
> Part A's question — is the surface finite? — no computation can touch**, and $S(10^6)=87.5$ is
> exactly the sort of reassuring number that would mislead you.
>
> **Knowing which kind of question you are asking is the skill.** That has been the point of all four
> labs.

Then look ahead:

> Next week is **Midterm 1** and parametric curves. And in Week 6 the questions become almost entirely
> of the second kind — from there to the end of the course, "does this converge?" is the question, and
> exact reasoning is the only tool that answers it.

---

*MATH 142 · Week 4 · Lab 04 Solutions · Instructor Only*
