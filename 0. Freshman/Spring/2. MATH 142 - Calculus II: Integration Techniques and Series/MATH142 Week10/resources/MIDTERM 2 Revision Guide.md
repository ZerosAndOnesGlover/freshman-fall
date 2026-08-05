# MATH 142 · Calculus II
## Midterm 2 · Revision Guide
### Covering Weeks 5–9

---

## The Exam

| | |
|---|---|
| **When** | Week 10 |
| **Duration** | **75 minutes** |
| **Covers** | **Weeks 5–9** — parametric and polar, sequences, series and all convergence tests, power series |
| **Not covered** | **Week 10** (Taylor series). That is examined on the final. |
| **Weight** | **15%** of the course |
| **Total** | 100 points |
| **Allowed** | **One handwritten sheet, one side.** No calculator. |

**The character of this exam differs from Midterm 1.** That one was computational — integrate this, find that volume. **This one is about justification.** Most marks are for *naming a test, verifying its hypotheses, and drawing a valid conclusion.* A right answer with an invalid argument scores badly.

---

## Topic Checklist

Tick only what you could do **from a blank page, under time**.

### Week 5 — Parametric and polar
- [ ] $\frac{dy}{dx}=\frac{dy/dt}{dx/dt}$; horizontal/vertical tangents
- [ ] $\frac{d^2y}{dx^2} = \frac{d}{dt}\left(\frac{dy}{dx}\right)\big/\frac{dx}{dt}$ — **not** a ratio of second derivatives
- [ ] Parametric arc length, area, surface area
- [ ] $x=r\cos\theta$, $y=r\sin\theta$; converting by multiplying by $r$
- [ ] **$A=\frac12\int r^2d\theta$** — and where the $\frac12$ comes from
- [ ] $L=\int\sqrt{r^2+(r')^2}\,d\theta$
- [ ] **Finding the range of $\theta$** that traces a curve exactly once

### Week 6 — Sequences
- [ ] Limit techniques: dominant power, logs, conjugates, squeeze
- [ ] **Function limit $\implies$ sequence limit, never the reverse**
- [ ] $r^n$ converges $\iff -1<r\le1$
- [ ] **Growth hierarchy** $\ln n\ll n^p\ll a^n\ll n!\ll n^n$
- [ ] Monotone Convergence Theorem
- [ ] Recursive sequences: **prove convergence, then** solve $L=g(L)$

### Week 7 — Series and the first tests
- [ ] Series = limit of partial sums
- [ ] Geometric $\frac{\text{first term}}{1-r}$; telescoping
- [ ] **$n$-th Term Test proves divergence only**
- [ ] Integral Test — **three hypotheses** — plus the remainder bound
- [ ] $p$-series: converges $\iff p>1$
- [ ] Direct and limit comparison

### Week 8 — Signs
- [ ] Alternating Series Test — **two hypotheses**
- [ ] $|R_N|\le b_{N+1}$
- [ ] Absolute vs conditional; **absolute $\implies$ convergent**
- [ ] Ratio and Root tests; **$L=1$ is silence**
- [ ] Riemann rearrangement (conceptually)

### Week 9 — Power series
- [ ] $R = \left(\lim\left|\frac{c_{n+1}}{c_n}\right|\right)^{-1}$; missing terms need the term ratio
- [ ] **Test both endpoints separately**
- [ ] All four interval types
- [ ] Term-by-term differentiation and integration, and their licence
- [ ] The library: $\frac{1}{1-x}$, $\ln(1+x)$, $\arctan x$

---

## The Eight Errors That Cost the Most Marks

**Every one has already appeared on a problem set or quiz.**

1. **"The terms go to zero, so it converges."** *(PS 7 A4, D1.)* The $n$-th Term Test proves divergence only.
2. **"$L=1$, so it diverges."** *(PS 8 C5, D2.)* $L=1$ is **silence**. $\sum\frac1n$ and $\sum\frac1{n^2}$ both give it.
3. **Checking only one hypothesis of the Alternating Series Test.** *(PS 8 A2.)* $b_n$ must also be **decreasing**.
4. **Reporting a radius when the interval was asked for.** *(PS 9, throughout.)* Both endpoints must be tested.
5. **Losing the centre.** *(PS 9 B2, B3, B5.)* $|x-a|<R$, solved explicitly.
6. **Integrating a polar curve over the wrong range.** *(PS 5 C2.)* One petal is not $[0,2\pi]$.
7. **Solving $L=g(L)$ without proving convergence.** *(PS 6 C5.)* The fixed point equation presupposes a limit exists.
8. **Not classifying convergence as absolute or conditional** when signs are present. *(PS 8 B4.)*

> **Six of these eight are applying a theorem without checking its hypotheses.** That is the single
> theme of Weeks 6–9, and it is what this exam is testing.

---

## What To Put on Your Sheet

**One side.** Do not waste it on things you know.

**Worth including:**
- The **complete decision procedure** for testing a series (Week 8 reference sheet)
- The two $p$-tests and the growth hierarchy
- Polar area and arc length formulas, **with a note about the $\frac12$ and about ranges**
- The standard alternating sums: $\ln2$, $\frac{\pi^2}{12}$, $\frac\pi4$
- The power series library and the four interval types
- Ratio/root limits you keep forgetting: $\left(1+\frac1n\right)^n\to e$, $n^{1/n}\to1$
- Every hypothesis you have failed to check twice

**Not worth including:** anything you can rederive in ten seconds.

---

## Strategy

1. **Read the whole paper (2 minutes).** Convergence questions are often quick; do those first.
2. **For every series, run the decision procedure**, starting with the $n$-th Term Test.
3. **Name every test and verify its hypotheses in writing.** That *is* the answer.
4. **For power series, finish the job**: radius, open interval, both endpoints, final interval.
5. **Never write "converges" alone** where signs are present — say absolutely or conditionally.
6. **If a test is inconclusive, say so and try another.** That is a correct and creditable step.

---

## Sample Paper

**75 minutes. 100 points. One side of notes. No calculator.**

---

**Q1. (18 points)** *(Week 5.)*

**(a)** Find the arc length of $x=t^2$, $y=t^3$ for $t\in[0,2]$.
**(b)** Find the area enclosed by the cardioid $r = 3(1+\sin\theta)$.

**Q2. (16 points)** *(Week 6.)* Evaluate, naming your method:

**(a)** $\displaystyle\lim_{n\to\infty}\frac{2n^3+n}{5n^3-1}$   **(b)** $\displaystyle\lim_{n\to\infty}\left(1+\frac3n\right)^{2n}$   **(c)** $\displaystyle\lim_{n\to\infty}\frac{n!}{2^n\,n!}$

**Q3. (24 points)** *(Weeks 7–8.)* For each, determine convergence, **naming the test and verifying its hypotheses**. Where signs are present, classify as absolute or conditional.

**(a)** $\displaystyle\sum\frac{1}{n^2+3}$   **(b)** $\displaystyle\sum\frac{n}{n^2+1}$   **(c)** $\displaystyle\sum\frac{(-1)^n}{\sqrt{n+1}}$   **(d)** $\displaystyle\sum\frac{3^n}{n!}$

**Q4. (18 points)** *(Week 9.)* Find the **interval of convergence** of

$$\sum_{n=1}^\infty\frac{(x-1)^n}{n\,4^n}$$

**Q5. (12 points)** *(Week 8.)* For $\displaystyle\sum_{n=1}^\infty\frac{(-1)^{n+1}}{n^4}$, how many terms guarantee an error below $10^{-3}$? State the bound you used.

**Q6. (12 points)** *(Concept.)*

**(a)** State the Ratio Test, including the inconclusive case. Give two series, one convergent and one divergent, both with $L=1$.
**(b)** Explain why the Ratio Test can never decide an endpoint of a power series' interval of convergence.

---
---

# SAMPLE PAPER — ANSWERS

*All verified.*

**Q1(a)** Speed $=\sqrt{4t^2+9t^4}=t\sqrt{4+9t^2}$ on $[0,2]$.

$$L = \int_0^2 t\sqrt{4+9t^2}\,dt = \frac{1}{27}\Big[(4+9t^2)^{3/2}\Big]_0^2 = \boxed{\frac{80\sqrt{10}-8}{27}}\approx 9.073$$

**Q1(b)** $A=\frac12\int_0^{2\pi}9(1+\sin\theta)^2d\theta = \frac92(2\pi+0+\pi) = \boxed{\frac{27\pi}{2}}$

**Q2(a)** Divide by $n^3$: $\boxed{\frac25}$.
**Q2(b)** $\left[\left(1+\frac3n\right)^n\right]^2\to\boxed{e^6}$.
**Q2(c)** $\frac{n!}{2^nn!} = \frac{1}{2^n}\to\boxed{0}$ — *geometric, $|r|<1$. (Read the expression carefully; the factorials cancel.)*

**Q3(a)** $\frac{1}{n^2+3}<\frac1{n^2}$; $p$-series $p=2$. **Converges** (direct comparison).
**Q3(b)** Limit comparison with $\frac1n$: $L=1$; $\sum\frac1n$ diverges. **Diverges.**
**Q3(c)** $\sum\frac{1}{\sqrt{n+1}}$ diverges ($p=\frac12$); AST: decreasing ✓, $\to0$ ✓. **Conditionally convergent.**
**Q3(d)** Ratio $=\frac{3}{n+1}\to0<1$. **Converges absolutely.**

**Q4** $\left|\frac{c_{n+1}}{c_n}\right| = \frac{n4^n}{(n+1)4^{n+1}}\to\frac14$, so $R=4$, centre 1, open interval $(-3,5)$.

- $x=5$: $\sum\frac{4^n}{n4^n}=\sum\frac1n$ — **diverges.**
- $x=-3$: $\sum\frac{(-4)^n}{n4^n} = \sum\frac{(-1)^n}{n}$ — **converges.**

$$\boxed{[-3,\,5)}$$

**Q5** Alternating series estimate $|R_N|\le b_{N+1}=\frac{1}{(N+1)^4}$. Need $(N+1)^4>1000$, i.e. $N+1>5.62$, so $N+1=6$:

$$\boxed{N=6 \text{ terms}}$$

*(Check: $s_6 = 0.946768$, true value $\frac78\zeta(4)=0.947033$, error $2.65\times10^{-4}<10^{-3}$ ✓)*

**Q6(a)** *(Statement as in Week 8.)* $\sum\frac1n$ diverges and $\sum\frac1{n^2}$ converges; **both have $L=1$.**

**Q6(b)** For $\sum c_n(x-a)^n$ the ratio is $\left|\frac{c_{n+1}}{c_n}\right|\cdot|x-a|\to\frac{|x-a|}{R}$, which equals **exactly 1** when $|x-a|=R$ — **regardless of the coefficients.** Since $L=1$ is the inconclusive case, the test can never decide an endpoint.

---

## Marking of the Sample Paper

| Q | Points | Where the marks are |
|---|---|---|
| 1 | 18 | 9 each; setup carries most |
| 2 | 16 | 6+6+4; **methods must be named** |
| 3 | 24 | 6 each — **half for the test and its hypotheses** |
| 4 | 18 | 6 radius, 4 per endpoint, 4 final interval |
| 5 | 12 | 6 bound, 6 solving |
| 6 | 12 | 6+6; (b) wants the algebra |

**A pass is about 55; a strong performance is 80+.** If you scored below 50, the cause is almost certainly Q3 — **the decision procedure needs to be automatic**, and that comes from doing thirty of them, not from rereading notes.

---

## The Week Before

- **Rework PS 5–9 from a blank page**, timed.
- **Drill Q3-style problems** until the test choice is instant. This is the highest-value revision available.
- **Build your sheet yourself.**
- **Do the sample paper under exam conditions.**

Good luck. **Name the test, check its hypotheses, then conclude.**

---

*MATH 142 · Midterm 2 Revision Guide · covers Weeks 5–9*
