# MATH 142 · Calculus II
## Lab 12 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures produced by running the lab in double precision unless stated.

> **Part A is not marked for correctness.** Mark it for a genuine timed attempt and an honest
> self-mark. **A student who scored 2/5 and filled the table accurately gets full marks.** A student
> who scored 5/5 and left the table blank does not.

---

## Part A — Timed Mock Section (30 pts)

**Answers, for the students' own marking — not for grading.**

**A1.** $u=1-x^2$: $\displaystyle\int_0^1x^3\sqrt{1-x^2}\,dx=\frac12\int_0^1(1-u)\sqrt u\,du = \boxed{\dfrac{2}{15}}$
*(Verified.) Odd power of $x$ against $\sqrt{1-x^2}$ — **$u$-substitution, not trig substitution.** Students who reached for $x=\sin\theta$ still get there, slowly.*

**A2.** $\dfrac{x^2+1}{x(x-1)^2}=\dfrac1x+\dfrac{2}{(x-1)^2}$ — **the $\dfrac{B}{x-1}$ term has $B=0$.**

$$\int = \boxed{\ln|x|-\frac{2}{x-1}+C}$$

*(Verified.) **The vanishing middle coefficient is deliberate**: students who omit the $\frac{B}{x-1}$ term from the setup get the right answer for the wrong reason, and should be told so during the self-mark.*

**A3.**
- **(a) Converges** — Ratio Test: $\frac{(n+1)^2}{n^2}\cdot\frac12\to\frac12<1$. *(Sum $=6$.)*
- **(b) Diverges** — Integral Test: $\int_2^\infty\frac{dx}{x\ln x}=[\ln\ln x]_2^\infty=\infty$. *(Verified.)*
- **(c) Conditionally convergent.** AST applies ($b_n=\frac{n}{n^2+1}\downarrow0$; decreasing since $\frac{d}{dn}\frac{n}{n^2+1}=\frac{1-n^2}{(n^2+1)^2}<0$ for $n>1$). **Not absolute:** limit comparison with $\frac1n$ gives ratio $\to1$. *(Verified; the sum is $-0.269610502708$.)*

**A4.** $|3x-1|<1\Rightarrow 0<x<\frac23$, so $R=\frac13$ about $x=\frac13$.
**Both endpoints converge absolutely**, since $\left|\frac{(\pm1)^n}{n^2+1}\right|\le\frac1{n^2}$:

$$\boxed{\left[0,\tfrac23\right]}$$

**A5.** Separable: $(1+y^2)dy=2x\,dx$, so

$$\boxed{y+\frac{y^3}{3}=x^2+\frac43}$$

**Leave it implicit** because solving for $y$ requires the cubic formula. *(Verified: a CAS returns an explicit solution involving $\sqrt[3]{-3x^2+\sqrt{9x^4+24x^2+20}-4}$ — correct, unusable, and exactly the reason the implicit form is the answer.)*

*Marking: **30 for a complete timed attempt with the A6 table filled in.** Deduct only for a missing or obviously insincere self-mark.*

---

## Part B — One Integral, Every Tool (45 pts)

### B1 (10) — the tail bound

On $[T,\infty)$ with $T\ge1$ we have $\frac{x}{T}\ge1$, so

$$\int_T^\infty e^{-x^2}dx \le \int_T^\infty\frac{x}{T}e^{-x^2}dx = \frac{1}{T}\left[-\tfrac12e^{-x^2}\right]_T^\infty = \frac{e^{-T^2}}{2T}$$

| $T$ | true tail | bound $\frac{e^{-T^2}}{2T}$ |
|---:|---|---|
| 1 | $1.39403\times10^{-1}$ | $1.83940\times10^{-1}$ |
| 2 | $4.14553\times10^{-3}$ | $4.57891\times10^{-3}$ |
| 3 | $1.95772\times10^{-5}$ | $2.05683\times10^{-5}$ |
| 4 | $1.36632\times10^{-8}$ | $1.40669\times10^{-8}$ |
| 5 | $1.36254\times10^{-12}$ | $1.38879\times10^{-12}$ |
| **6** | $1.90714\times10^{-17}$ | $\mathbf{1.93294\times10^{-17}}$ |

*(Verified.)* **$T=6$ is the smallest integer with the bound below $10^{-15}$** ($T=5$ gives $1.4\times10^{-12}$).

**The bound is within 3% of the true tail from $T=3$ on** — an unusually good bound, and worth saying so.

*Marking: 5 proof, 3 table, 2 for the choice of $T$. **The proof must produce the factor $x/T$**; a student who writes $e^{-x^2}\le e^{-T^2}$ and integrates gets $\infty$ and has proved nothing.*

### B2 (12) — Simpson

True value: $\int_0^4e^{-x^2}dx = 0.886226911789569$

| $n$ | Simpson | error | ratio |
|---:|---|---|---|
| $4$ | $0.8362142647382531$ | $5.0013\times10^{-2}$ | — |
| $8$ | $0.8861963466352094$ | $3.0565\times10^{-5}$ | $\mathbf{1636.3}$ |
| $16$ | $0.8862269109825432$ | $8.0703\times10^{-10}$ | $\mathbf{37874}$ |
| $32$ | $0.8862269117248652$ | $6.4704\times10^{-11}$ | $12.47$ |
| $64$ | $0.8862269117852432$ | $4.3258\times10^{-12}$ | $14.96$ |
| $128$ | $0.8862269117892941$ | $2.7478\times10^{-13}$ | $15.74$ |
| $256$ | $0.8862269117895524$ | $1.6542\times10^{-14}$ | $16.61$ |

*(Verified.)*

**(a)** **Simpson's rule fits a parabola to each pair of subintervals.** At $n=4$ the step is $h=1$, and $e^{-x^2}$ falls from $1$ to $1.1\times10^{-7}$ across $[0,4]$ — **nothing like a parabola on that scale.** The $O(h^4)$ error term contains $f^{(4)}$, which is large here, so the asymptotic estimate simply does not apply yet. **The huge ratios are the method entering its asymptotic regime, not superconvergence.**

**(b)** **The ratio settles near 16 from $n=32$ onwards.** *(The final $16.61$ overshoots because the error has reached $10^{-14}$, where double-precision rounding is a visible fraction of it.)*

> **Two data points cannot establish an order.** The pair $n=8,16$ would have "proved" order $15$.
> **An order claim needs a run of ratios that stabilise**, and this table is the reason every lab
> this term asked for six rows rather than two.

*Marking: 5 table, 4 for (a), 3 for (b). **Full marks on (b) require the point about two data points.***

### B3 (13) — the series, and the warning

$$e^{-x^2}=\sum_{k\ge0}\frac{(-1)^kx^{2k}}{k!} \;\xrightarrow{\ \int_0^T\ }\; \sum_{k\ge0}\frac{(-1)^kT^{2k+1}}{k!\,(2k+1)}$$

**Term-by-term integration is licensed by Week 9**, since the radius of convergence is infinite.

Summed in double precision **by the recurrence of part (d)**:

| $T$ | series | true | abs error | largest term |
|---:|---|---|---|---|
| $1$ | $0.746824132812427$ | $0.746824132812427$ | $0$ | $1.00$ |
| $2$ | $0.8820813907624221$ | $0.8820813907624216$ | $4.44\times10^{-16}$ | $3.20$ |
| $3$ | $0.8862073482595059$ | $0.8862073482595212$ | $1.53\times10^{-14}$ | $1.90\times10^{2}$ |
| $4$ | $0.8862269117944876$ | $0.8862269117895689$ | $4.92\times10^{-12}$ | $1.14\times10^{5}$ |
| $5$ | $0.8862270157491613$ | $0.8862269254513955$ | $9.03\times10^{-8}$ | $5.85\times10^{8}$ |
| $6$ | $0.8855300658432403$ | $0.8862269254527579$ | $\mathbf{6.97\times10^{-4}}$ | $\mathbf{2.42\times10^{13}}$ |

*(Verified.)*

**(a)** **Error at $T=6$: $6.97\times10^{-4}$** — the answer is wrong in the **third decimal place**.

**(b)** **The largest term is $2.42\times10^{13}$**, against an answer of $0.886$. **Thirteen orders of magnitude of cancellation.** Double precision carries about 16 significant digits, so roughly 13 of them are consumed cancelling — leaving about 3, which is exactly what the error shows.

**(c)** **Catastrophic cancellation.** *(Tuesday's lecture; the $\frac{1-\cos x}{x^2}$ table and the quadratic formula are the same phenomenon.)* **The mathematics is flawless and the convergence is genuine** — the series converges for every $T$, and in exact arithmetic it would give every digit. **The failure is entirely in the arithmetic**, and no amount of adding more terms repairs it.

**(d)** **The two ways of forming the terms disagree.** At $T=6$:

| method | total | error |
|---|---|---|
| $\dfrac{(-1)^kT^{2k+1}}{k!\,(2k+1)}$ directly | $0.8957580220904371$ | $9.53\times10^{-3}$ |
| recurrence $t_k=-t_{k-1}\dfrac{T^2}{k}\cdot\dfrac{2k-1}{2k+1}$ | $0.8855300658432403$ | $6.97\times10^{-4}$ |

*(Verified.)*

> **Two algebraically identical computations of the same convergent series, in the same precision,
> disagree in the second decimal place** — and both are wrong. **Nothing distinguishes them
> mathematically.** The recurrence happens to round better here; that is a fact about floating point,
> not about the series.

**This is the whole content of Tuesday's lecture, arrived at by measurement.**

*Marking: 3 derivation, 4 table, 2 + 2 + 2 for (a)–(c), and **(d) is the point of the part** — award the last 2 within the table mark for actually reporting a disagreement rather than assuming agreement. **A student who reports "both give the same thing" has not run it.***

### B4 (10) — the combined answer

Simpson on $[0,6]$ with $n=256$:

$$0.8862269254527589 \qquad\text{against}\qquad \frac{\sqrt\pi}{2}=0.8862269254527580$$

$$\textbf{Error: } 8.88\times10^{-16}$$

*(Verified — essentially machine precision.)*

**(a)** As above.

**(b)** The required sentence, in substance:

> **The total error is at most the truncation error plus the quadrature error**: B1 proves
> $\int_6^\infty e^{-x^2}dx\le1.93\times10^{-17}$, and B2's stabilised ratio of $16$ establishes the
> Simpson error as $O(h^4)$, extrapolating to below $10^{-14}$ at $n=256$ on $[0,6]$.

**Both pieces are needed.** A student who bounds only the tail has an unbounded quadrature error; one who tabulates only Simpson has ignored an infinite interval.

**(c)**
- **Series:** for **small $T$**, where it is exact to machine precision from a handful of terms and comes with an alternating-series bound *(at $T=1$ the error was exactly zero)*.
- **Quadrature:** for **large $T$**, or whenever the integrand's scale varies enough to cause cancellation in a series. **It is insensitive to the size of $T$** in a way the series is not.

*Marking: 3 + 4 + 3. **(b) must name both sources.***

---

## Part C — The Revision List (25 pts)

**Marked on specificity, not on content.** There is no answer key.

| | Full marks | No marks |
|---|---|---|
| **C1** (10) | *"I do not test endpoints of intervals of convergence."* | *"Week 9."* |
| **C2** (8) | *"I drop the chain rule in FTC problems — check by differentiating the answer back."* | *"Careless mistakes."* |
| **C3** (7) | *"Weeks 2, 4, 9. Ten problems each from the reference sheets, Thursday to Saturday."* | *"Revise harder."* |

**C2 requires an accompanying check for each error.** A named error with no check is half marks.

---

## Marking Summary

| Part | Points |
|---|---|
| A | 30 |
| B1 | 10 |
| B2 | 12 |
| B3 | 13 |
| B4 | 10 |
| C | 25 |
| **Total** | **100** |

---

## Checkoff Checklist

1. Part A attempted **under a timer** and self-marked honestly
2. **B1's proof produces the factor $x/T$**
3. B2(b) says two data points cannot establish an order
4. **B3(b) compares $2.42\times10^{13}$ to $0.886$**
5. **B3(d) reports that the two summation orders disagree**
6. B4(b) names **both** error sources
7. C1–C3 are specific enough to act on

---

## Note for the Debrief

**This is the last lab of the course.** Close it on B3.

> **You have spent twelve weeks proving that things converge.** Today you summed a series that
> converges for every real $T$, whose terms you derived correctly, whose convergence you can prove in
> one line — **and it returned a wrong answer in the third decimal place.**
>
> Then you summed **the same series a second way** and got a different wrong answer.

Then the point:

> **Convergence is a statement about exact arithmetic.** Your machine does not have exact arithmetic,
> and the gap between those two facts is a whole subject you have not met yet.
>
> **What saved you was not a theorem. It was a second method that agreed to fifteen digits.**

Then close the course:

> **Twelve weeks, and two rules survived all of them.**
>
> **The order of convergence decides the practical question** — you measured it on quadrature, on
> products, on series, on iterations, on differential equations, and it decided every one.
>
> **The CAS is a check, not an oracle** — you caught an unevaluated integral, a numerical library
> four digits wrong, a `dsolve` that failed, a sign you had backwards, a quadratic formula off by
> 25%, and today a convergent series off in the third decimal. **Every one of them by a cheap
> independent check.**
>
> **The integrals will fade. That reflex is what you keep.**

---

*MATH 142 · Week 12 · Lab 12 Solutions · Instructor Only*
