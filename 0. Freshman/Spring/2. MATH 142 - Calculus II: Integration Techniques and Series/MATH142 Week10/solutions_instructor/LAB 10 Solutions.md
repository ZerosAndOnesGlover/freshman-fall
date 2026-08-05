# MATH 142 · Calculus II
## Lab 10 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures produced by running the lab.

> **This lab closes a loop opened in Week 0.** Lab 0's debrief promised the students 13 terms; Part C
> delivers exactly 13. **Make sure that connection is drawn explicitly in the debrief** — it is the
> single clearest demonstration that the course was built as one argument.

---

## Part A — Taylor Polynomials and Their Errors (25 pts)

### A1 (10), A2 (8)

For $\sin x$ at $a=0$, with $M=1$ **valid everywhere** (every derivative of $\sin$ is $\pm\sin$ or $\pm\cos$, all bounded by 1):

| $x$ | $n$ | true error | bound $\frac{|x|^{n+1}}{(n+1)!}$ | ratio |
|---|---|---|---|---|
| $0.5$ | $3$ | $2.5887\times10^{-4}$ | $2.6042\times10^{-3}$ | $10.1$ |
| $0.5$ | $5$ | $1.5447\times10^{-6}$ | $2.1701\times10^{-5}$ | $14.0$ |
| $0.5$ | $7$ | $5.3701\times10^{-9}$ | $9.6881\times10^{-8}$ | $18.0$ |
| $1.0$ | $3$ | $8.1377\times10^{-3}$ | $4.1667\times10^{-2}$ | $5.1$ |
| $1.0$ | $5$ | $1.9568\times10^{-4}$ | $1.3889\times10^{-3}$ | $7.1$ |
| $1.0$ | $7$ | $2.7308\times10^{-6}$ | $2.4802\times10^{-5}$ | $9.1$ |
| $2.0$ | $3$ | $2.4263\times10^{-1}$ | $6.6667\times10^{-1}$ | $2.7$ |
| $2.0$ | $5$ | $2.4036\times10^{-2}$ | $8.8889\times10^{-2}$ | $3.7$ |
| $2.0$ | $7$ | $1.3609\times10^{-3}$ | $6.3492\times10^{-3}$ | $5.1$ |

**The bound holds in all nine cases** ✓ *(Verified.)*

*Marking A1: 10. A2: 5 for the bounds, **3 for justifying $M=1$ over all of $\mathbb R$.***

### A3 (7)

**(a)** **Loose** — by a factor of roughly 3 to 18, growing as $x$ shrinks and $n$ grows.

*(The reason: the bound uses the worst case $|f^{(n+1)}(c)|=1$, while the actual $c$ gives something smaller. For an alternating series the true error is close to half the first omitted term, and the Lagrange bound is essentially that whole term with a pessimistic derivative.)*

**(b)** **Because the true error is not knowable in advance.** A library must guarantee accuracy for **every** input in a range, before shipping — it cannot compute the exact error, since that would require the exact answer it is trying to produce. **A bound that is provable and a factor of ten pessimistic is worth infinitely more than an exact error you cannot compute.**

*Marking: 3 + 4. **(b) must identify that the bound is available a priori** and the true error is not.*

---

## Part B — Where the Series Lies (20 pts)

### B1 (8)

| $x$ | $f(x)=e^{-1/x^2}$ | $f(x)/x^{10}$ |
|---|---|---|
| $0.5$ | $1.83156\times10^{-2}$ | $18.755$ |
| $0.2$ | $1.38879\times10^{-11}$ | $1.35624\times10^{-4}$ |
| $0.1$ | $3.72008\times10^{-44}$ | $3.72008\times10^{-34}$ |
| $0.05$ | $1.91517\times10^{-174}$ | $1.96113\times10^{-161}$ |

*(Verified.)*

**The second column collapses to zero** — $f$ vanishes faster than $x^{10}$, and by the same argument faster than any power.

*Marking: 8 for the table with the observation.*

### B2 (6)

$$\text{Maclaurin series of } f = 0+0\cdot x+0\cdot x^2+\cdots = \boldsymbol{0}$$

**Radius $R=\infty$** (the zero series converges everywhere), and **it converges to the zero function.**

### B3 (6)

$f(1) = e^{-1} = 0.367879441$, while the series at $x=1$ gives $0$.

**$f$ agrees with its Taylor series at exactly one point: $x=0$.**

**What this shows:** computing Taylor coefficients and writing $\sum$ proves nothing. **The remainder is not a technicality in the statement of Taylor's theorem — it is the entire content**, because it is the only thing that could establish equality, and here it fails to vanish.

*Marking: 3 + 3. **"At exactly one point" must be stated**, and the conclusion must be about the necessity of the remainder.*

---

## Part C — Collecting Week 0's Debt (35 pts)

### C1 (8)

$$e^{-x^2} = \sum_{n=0}^\infty\frac{(-x^2)^n}{n!} = \sum_{n=0}^\infty\frac{(-1)^nx^{2n}}{n!}, \qquad R=\infty$$

Integrating term by term over $[0,1]$ — legal since $R=\infty$:

$$\int_0^1e^{-x^2}dx = \sum_{n=0}^\infty\frac{(-1)^n}{n!}\int_0^1x^{2n}dx = \boxed{\sum_{n=0}^\infty\frac{(-1)^n}{n!\,(2n+1)}}$$

*Marking: 3 substitution, 3 integration, 2 for noting the radius licenses it.*

### C2 (12)

Target: $\frac{\sqrt\pi}{2}\operatorname{erf}(1) = 0.7468241328124270254$

| terms | partial sum | error |
|---:|---|---|
| $1$ | $1.0$ | $2.532\times10^{-1}$ |
| $2$ | $0.66666666667$ | $8.016\times10^{-2}$ |
| $3$ | $0.76666666667$ | $1.984\times10^{-2}$ |
| $4$ | $0.74285714286$ | $3.967\times10^{-3}$ |
| $5$ | $0.74748677249$ | $6.626\times10^{-4}$ |
| $6$ | $0.74672919673$ | $9.494\times10^{-5}$ |
| $7$ | $0.74683603434$ | $1.190\times10^{-5}$ |
| $8$ | $0.74682280682$ | $1.326\times10^{-6}$ |
| $9$ | $0.74682426574$ | $1.329\times10^{-7}$ |
| $10$ | $0.74682412070$ | $1.211\times10^{-8}$ |
| $11$ | $0.74682413382$ | $1.011\times10^{-9}$ |
| $12$ | $0.74682413273$ | $7.793\times10^{-11}$ |
| $\mathbf{13}$ | $\mathbf{0.746824132818}$ | $\mathbf{5.576\times10^{-12}}$ ✓ |
| $14$ | $0.74682413281$ | $3.722\times10^{-13}$ |
| $15$ | $0.74682413281$ | $2.330\times10^{-14}$ |
| $16$ | $0.74682413281$ | $1.372\times10^{-15}$ |

$$\boxed{N=13 \text{ terms}}$$

*(Verified.)*

*Marking: 12 for the table with $N=13$ identified. **This is the number Lab 0 promised** — say so on the script.*

### C3 (8)

| method | cost for 10 digits |
|---|---|
| Simpson's rule (Lab 0) | **128 function evaluations** |
| Taylor series (Lab 10) | **13 terms** |

**About a tenfold reduction in operations** — and each Simpson evaluation is an $\exp$ call, while each series term is one division and one multiplication. **The real gap is larger than 10.**

**And the qualitative difference matters more:** Lab 0's order-4 behaviour was *measured*; the series' error bound is *proved in advance* by the alternating estimate.

*Marking: 4 table, 4 comment. **Full marks require the a priori/a posteriori distinction**, not just the ratio.*

### C4 (7)

$$\frac{\sin x}{x} = \sum_{n=0}^\infty\frac{(-1)^nx^{2n}}{(2n+1)!} \implies \int_0^1\frac{\sin x}{x}dx = \sum_{n=0}^\infty\frac{(-1)^n}{(2n+1)(2n+1)!}$$

| terms | value | error |
|---|---|---|
| $1$ | $1.0$ | $5.39\times10^{-2}$ |
| $3$ | $0.94611111111$ | $2.80\times10^{-5}$ |
| $5$ | $0.94608307263$ | $2.27\times10^{-9}$ |
| $\mathbf{6}$ | $\mathbf{0.94608307035}$ | $\mathbf{1.23\times10^{-11}}$ |

**Six terms give eleven correct digits.** True value $\mathrm{Si}(1) = 0.946083070367$. *(Verified.)*

**Why the series is fine at $x=0$:** $\sin x$ has lowest term $x$, so $\frac{\sin x}{x}$ has lowest term $1$ — **the singularity is removable**, and the series simply does not have one. **The formula appeared to fail at 0; the function never did.**

*Marking: 3 series, 2 table, **2 for the removable-singularity explanation.***

---

## Part D — Reflection (20 pts)

### D1 (10)

| Step | Theorem | Week |
|---|---|---|
| $e^{-x^2}$ **equals** its Maclaurin series | Taylor's theorem, $R_n\to0$ | **10** |
| swapping $\int$ and $\sum$ | term-by-term integration inside $R$ | **9** |
| why that swap is safe | absolute convergence permits rearrangement | **8** |
| error $\le$ first omitted term | alternating series estimate | **8** |

*Marking: 10 — 2.5 per row. **The Week 8 rearrangement result is the one most often omitted**; students tend to cite only the Week 9 theorem without noticing what it rests on.*

### D2 (10)

**Lab 10 entry: the exact method wins outright — and, uniquely, it can promise its accuracy in advance.**

**What Taylor has that Simpson does not:**

- **Simpson's rule** gave a *measured* order of 4 (Lab 0's ratio column) and an error estimate obtained by comparing against a known answer. **Run on an unknown integral, it offers no certificate.**
- **The Taylor series** carries a **provable a priori bound** — the first omitted term — requiring no knowledge of the answer. You can decide, before computing anything, that 13 terms will suffice.

**That is the difference between a method that works and a method you can ship.** Every other numerical technique in this course was validated by measurement; this one is validated by proof.

*Marking: 10. **Full marks require the a priori guarantee**, not just "the series is faster". A student who says only "13 beats 128" earns 5.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 25 |
| B | 20 |
| C | 35 |
| D | 20 |
| **Total** | **100** |

---

## Checkoff Checklist

1. A2 justifies $M=1$ **over all of $\mathbb R$**
2. **A3(b) says the true error is not available a priori**
3. B1's ratio column collapses
4. **B3 says "exactly one point"**
5. C1 notes $R=\infty$ licenses the integration
6. **C2 identifies $N=13$**
7. C3 gives both the ratio and the a priori distinction
8. C4 explains the removable singularity
9. **D1 names all four theorems, including Week 8's**

---

## Note for the Debrief

**This is the last lab. Close the loop explicitly.**

> **Week 0, Lecture 1.** You were told that $e^{-x^2}$ has an antiderivative — the Fundamental
> Theorem guarantees it — and that **no elementary formula for it exists**. Liouville proved that in
> 1835 and it is not going to change.
>
> **Lab 0, the same week.** You computed $\int_0^1e^{-x^2}dx$ to ten decimal places anyway, with
> Simpson's rule, using 128 function evaluations. The debrief ended with a promise: *in Week 10, 13
> numbers.*
>
> **Today: thirteen numbers.** *(Hold up the table.)*

Then the point that actually matters:

> **The interesting part is not that 13 beats 128.** It is that **you could have known 13 was enough
> before computing anything** — the alternating estimate says so, and it is a theorem.
>
> In Lab 0 you *measured* Simpson's order to be 4. In Lab 3 you found that measurement cannot decide
> convergence at all. In Lab 7 a library returned twelve wrong digits without warning. **Measurement
> has been unreliable all term.**
>
> **What changed in Weeks 8 to 10 is that you can now prove an error bound instead of observing one.**
> That is the whole difference between a calculation and a guarantee — and it is why the theorems
> were worth three weeks.

Then, briefly, forward:

> Week 11 puts all of this to work on differential equations, and Week 12 closes the course.

---

*MATH 142 · Week 10 · Lab 10 Solutions · Instructor Only*
