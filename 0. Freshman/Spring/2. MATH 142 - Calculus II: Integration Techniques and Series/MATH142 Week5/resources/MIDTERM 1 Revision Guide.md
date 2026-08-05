# MATH 142 · Calculus II
## Midterm 1 · Revision Guide
### Covering Weeks 0–4

---

## The Exam

| | |
|---|---|
| **When** | Week 5 |
| **Duration** | **75 minutes** |
| **Covers** | **Weeks 0–4** — review, parts, trig integrals, trig substitution, partial fractions, improper integrals, comparison, volumes, arc length, surface area |
| **Not covered** | **Week 5** (parametric and polar). That is examined on Midterm 2. |
| **Weight** | **15%** of the course |
| **Total** | 100 points |
| **Allowed** | **One handwritten sheet, one side.** No calculator. |

**75 minutes for 100 points means roughly 45 seconds per mark.** A 16-point question deserves about 12 minutes. **If you are past 15 minutes on one question, leave it and come back.**

---

## Topic Checklist

Work through this honestly. Tick only what you could do **from a blank page, under time**.

### Week 0 — Review
- [ ] State the definition of $\int_a^b f$ as a limit of Riemann sums
- [ ] State **both** parts of the FTC and say which you are using
- [ ] $\frac{d}{dx}\int_{g(x)}^{h(x)}f = f(h)h' - f(g)g'$ — chain rule and the minus sign
- [ ] Substitution, **changing the limits** on definite integrals
- [ ] Symmetry: odd/even over $[-a,a]$
- [ ] Area between curves; average value; displacement vs distance

### Week 1 — Parts and trigonometric integrals
- [ ] $\int u\,dv = uv-\int v\,du$; LIATE
- [ ] $\int\ln x\,dx$, $\int\arctan x\,dx$ — the $dv=dx$ trick
- [ ] Repeated parts; **tabular integration**
- [ ] The circular case $\int e^{ax}\sin bx\,dx$ — solve algebraically
- [ ] Reduction formulas; $I_n = \frac{n-1}{n}I_{n-2}$ on $[0,\pi/2]$
- [ ] $\int\sin^m\cos^n$: the parity decision table
- [ ] $\int\tan^m\sec^n$: the parity decision table
- [ ] Product-to-sum for different frequencies

### Week 2 — Trigonometric substitution and partial fractions
- [ ] The three patterns and **the range of $\theta$**
- [ ] Reference triangles; changing limits on definite integrals
- [ ] Completing the square; splitting a linear numerator
- [ ] **Divide first** if the fraction is improper
- [ ] All four decomposition cases; recombine to check

### Week 3 — Improper integrals
- [ ] **Write the limit**
- [ ] $\int_1^\infty x^{-p}$ converges iff $p>1$; $\int_0^1 x^{-p}$ converges iff $p<1$
- [ ] **Find interior singularities and split**
- [ ] Direct comparison — **the direction**
- [ ] Limit comparison

### Week 4 — Applications
- [ ] Discs, washers ($R^2-r^2$), shells
- [ ] Radii for **shifted axes**
- [ ] Choosing discs vs shells
- [ ] Arc length $\int\sqrt{1+(f')^2}$
- [ ] Surface area $2\pi\int(\text{radius})\,ds$ — **$ds$, not $dx$**

---

## The Seven Errors That Cost the Most Marks

These are drawn from the diagnostic notes on PS 0–4. **Every one has appeared already.**

1. **Not changing the limits** on a definite substitution, or evaluating a $u$-antiderivative at $x$-limits.
2. **$(R-r)^2$ instead of $R^2-r^2$.**
3. **Not checking whether a fraction is proper** before decomposing. *(PS 2 D2.)*
4. **Not checking the integrand for singularities** before applying the FTC. *(PS 3 D2 — the $-2$.)*
5. **A comparison pointing the wrong way** — bounding above by a divergent function proves nothing.
6. **Using $dx$ where $ds$ is required** in surface area. *(Underestimates the sphere by exactly $\pi/4$.)*
7. **Writing a radius without drawing the region.** *(PS 4 A4.)*

> **Five of these seven are failures to look before computing.** The single most valuable exam habit
> is to spend ten seconds classifying each problem before writing anything.

---

## What To Put on Your Sheet

You have **one side**. Do not waste it on things you know.

**Worth including:**
- The two $p$-tests, with the directions
- The trigonometric substitution table with **ranges of $\theta$** and reference triangles
- The parity decision tables for $\sin^m\cos^n$ and $\tan^m\sec^n$
- Half-angle identities; product-to-sum identities
- $\int\sec x\,dx$ and $\int\sec^3x\,dx$
- The reduction formula and the $I_n$ table
- Volume/arc length/surface formulas
- Any antiderivative you have got wrong twice

**Not worth including:** anything from the Week 0 catalogue you already know cold — that is space you need for the tables.

> **Building the sheet is most of the revision.** Deciding what to include forces you to audit what
> you actually know. **Do not photocopy someone else's.**

---

## Strategy

1. **Read the whole paper first** (2 minutes). Start with what you can do fastest — marks are marks.
2. **Classify before computing.** Improper? Proper fraction? Symmetric? Which technique?
3. **Differentiate every antiderivative** you have time to check.
4. **Look for free consistency checks.** *(Quiz 05: $Q_1+Q_3=\pi$, the cylinder. Week 4: two methods on one solid.)*
5. **Never leave a setup blank.** A correct integral with no evaluation earns most of the setup marks; a blank page earns none.
6. **If a volume comes out negative, or an area does, you have a radius or an orientation backwards.** Say so on the paper even if you cannot fix it — it shows the check was made.

---

## Sample Paper

**75 minutes. 100 points. One side of notes. No calculator.**

*Attempt this under exam conditions before looking at the answers.*

---

**Q1. (18 points)** Evaluate:

**(a)** $\displaystyle\int x^2e^{-x}\,dx$   **(b)** $\displaystyle\int\frac{dx}{x^2+4x+13}$   **(c)** $\displaystyle\int\frac{2x+3}{(x-1)(x+2)}\,dx$

**Q2. (16 points)** Evaluate:

**(a)** $\displaystyle\int_0^{\pi/2}\sin^3x\cos^2x\,dx$   **(b)** $\displaystyle\int\frac{x^2}{\sqrt{9-x^2}}\,dx$

**Q3. (16 points)**

**(a)** Evaluate $\displaystyle\int_1^\infty\frac{dx}{x^{4/3}}$ or show it diverges.
**(b)** Evaluate $\displaystyle\int_0^1\ln x\,dx$ or show it diverges.
**(c)** Determine whether $\displaystyle\int_1^\infty\frac{dx}{\sqrt{x^4+1}}$ converges. **Do not evaluate.**

**Q4. (18 points)** The region bounded by $y=x^2$ and $y=4$ is rotated about:

**(a)** the $x$-axis   **(b)** the $y$-axis

Find both volumes.

**Q5. (16 points)** Find the arc length of $y = \dfrac{x^2}{2}-\dfrac{\ln x}{4}$ on $[1,2]$.

**Q6. (16 points)**

**(a)** State both $p$-tests and explain in one or two sentences why the inequalities point in opposite directions.
**(b)** A student evaluates $\int_{-1}^{1}x^{-2}dx$ as $\left[-\frac1x\right]_{-1}^{1}=-2$. Give a one-line reason this is impossible, name the failed hypothesis, and give the correct verdict.

---
---

# SAMPLE PAPER — ANSWERS

*All verified symbolically.*

**Q1(a)** Tabular integration, or parts twice:

$$\boxed{-(x^2+2x+2)e^{-x}+C}$$

**Q1(b)** Complete the square: $(x+2)^2+9$.

$$\boxed{\frac13\arctan\frac{x+2}{3}+C}$$

**Q1(c)** Cover-up: $A=\frac{2+3}{1+2}=\frac53$ at $x=1$; $B=\frac{-4+3}{-2-1}=\frac13$ at $x=-2$.

$$\boxed{\frac53\ln|x-1|+\frac13\ln|x+2|+C}$$

**Q2(a)** $m=3$ odd: peel one $\sin x$, $u=\cos x$.

$$\int_0^1(1-u^2)u^2du = \frac13-\frac15 = \boxed{\frac{2}{15}}$$

**Q2(b)** $x=3\sin\theta$:

$$\boxed{\frac92\arcsin\frac x3 - \frac{x\sqrt{9-x^2}}{2}+C}$$

**Q3(a)** $p=\frac43>1$, converges: $\dfrac{1}{p-1} = \boxed{3}$.

**Q3(b)** Improper at 0; converges to $\boxed{-1}$ (needs $t\ln t\to0$).

**Q3(c)** **Converges.** $\sqrt{x^4+1}>x^2$, so the integrand is $<x^{-2}$, and $\int_1^\infty x^{-2}$ converges ($p=2>1$).

**Q4(a)** Curves meet at $x=\pm2$. Washer with $R=4$, $r=x^2$:

$$V = \pi\int_{-2}^{2}\big(16-x^4\big)dx = \boxed{\frac{256\pi}{5}}$$

**Q4(b)** Discs in $y$, radius $\sqrt y$, $y\in[0,4]$:

$$V = \pi\int_0^4 y\,dy = \boxed{8\pi}$$

**Q5** $y' = x-\dfrac{1}{4x}$, and

$$1+(y')^2 = x^2+\frac12+\frac{1}{16x^2} = \left(x+\frac{1}{4x}\right)^2$$

*— a perfect square, which is why this curve was chosen.*

$$L = \int_1^2\left(x+\frac{1}{4x}\right)dx = \left[\frac{x^2}{2}+\frac{\ln x}{4}\right]_1^2 = \boxed{\frac32+\frac{\ln2}{4}}\approx 1.673$$

**Q6(a)** $\int_1^\infty x^{-p}$ converges iff $p>1$; $\int_0^1x^{-p}$ converges iff $p<1$. **Near infinity the function must shrink fast** (large $p$ helps); **near a singularity it must blow up slowly** (large $p$ hurts).

**Q6(b)** The integrand is **positive**, so the integral cannot be negative. **FTC Part 2 requires continuity on $[a,b]$**, and the integrand is undefined at $0$. Splitting at $0$, each half is a $p$-test with $p=2\ge1$: **the integral diverges.**

---

## Marking of the Sample Paper

| Q | Points | Where the marks are |
|---|---|---|
| 1 | 18 | 6 each; method must be visible |
| 2 | 16 | 8 each; Q2(b) needs the triangle |
| 3 | 16 | 5+5+6; **the limit notation is worth marks** |
| 4 | 18 | 9 each; the radii carry most of it |
| 5 | 16 | **8 for spotting the perfect square** |
| 6 | 16 | 8+8; (a) wants the *reason*, not the statement |

**A pass on this paper is about 55. A strong performance is 80+.** If you scored below 50 under time, the issue is almost certainly speed on Q1–Q2 — that is fixed by volume practice, not by rereading notes.

---

## The Week Before

- **Rework PS 0–4 from a blank page**, timed. Not reading them — *reworking* them.
- **Build your sheet**, from scratch, yourself.
- **Do the sample paper under exam conditions.**
- **Go to the Math Help Center** with the specific problems you could not do, not with "I'm stuck on integration".

Good luck. **Look before you compute.**

---

*MATH 142 · Midterm 1 Revision Guide · covers Weeks 0–4*
