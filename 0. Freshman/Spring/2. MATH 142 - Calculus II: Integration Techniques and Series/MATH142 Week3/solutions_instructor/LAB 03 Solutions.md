# MATH 142 · Calculus II
## Lab 03 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures below were produced by running the lab with `mpmath` at 30 digits.

> **This lab has no measurement noise.** $F(T,p)$ is a closed form, so every number is exact to the
> precision requested. **Students should match these digits.** A mismatch means an implementation
> error, not machine variation — unlike Labs 0 and 1.

---

## Part A — Derive and Verify (20 pts)

### A1 (8) — the derivation

For $p\neq1$:

$$\int_1^T x^{-p}dx = \left[\frac{x^{1-p}}{1-p}\right]_1^T = \frac{T^{1-p}-1}{1-p} = \frac{1-T^{1-p}}{p-1}$$

For $p=1$:

$$\int_1^T\frac{dx}{x} = \Big[\ln x\Big]_1^T = \ln T$$

*Marking: 4 each. **The two forms of the $p\neq1$ answer are the same** — deduct nothing for either.*

### A2 (6) — verification

| | value | exact |
|---|---|---|
| $F(T,2)\to$ | $1$ | $\frac{1}{2-1}=1$ ✓ |
| $F(T,\tfrac32)\to$ | $2$ | $\frac{1}{1.5-1}=2$ ✓ |
| $F(10^6,1)$ | $13.8155105579$ | $6\ln10 = 13.8155105579$ ✓ |

*Marking: 2 each.*

### A3 (6) — the limits, stated in advance

| $p$ | $\lim_{T\to\infty}F(T,p)$ |
|---|---|
| $0.5$ | $\infty$ (diverges) |
| $0.99$ | $\infty$ (diverges) |
| $1$ | $\infty$ (diverges) |
| $1.01$ | $\mathbf{100}$ (converges) |
| $1.5$ | $2$ (converges) |
| $2$ | $1$ (converges) |

*Marking: 1 each. **The instruction to do this before computing the table is not decorative** — a student who computes first will read the table and conclude the wrong thing, which is the lab's entire demonstration. If a report shows the limits derived after the table, note it.*

*$\frac{1}{p-1}$ at $p=1.01$ is $\frac{1}{0.01}=100$ — the source of the whole effect.*

---

## Part B — The Table (25 pts)

### B1 (18) and B2 (7)

$$F(T,p)=\int_1^T x^{-p}\,dx$$

| $T$ | $p=0.5$ | $p=0.99$ | $p=1$ | $p=1.01$ | $p=1.5$ | $p=2$ |
|---|---|---|---|---|---|---|
| $10$ | 4.32456 | 2.32930 | 2.30259 | 2.27628 | 1.36754 | 0.9 |
| $10^2$ | 18.0 | 4.71285 | 4.60517 | 4.50074 | 1.8 | 0.99 |
| $10^3$ | 61.2456 | 7.15193 | 6.90776 | 6.67457 | 1.93675 | 0.999 |
| $10^4$ | 198.0 | 9.64782 | 9.21034 | 8.79892 | 1.98 | 0.9999 |
| $10^6$ | 1998.0 | 14.8154 | 13.8155 | 12.9036 | 1.998 | 0.999999 |
| $10^{10}$ | 199998.0 | 25.8925 | 23.0259 | 20.5672 | 1.99998 | 1.0 |
| $10^{20}$ | $2.0\times10^{10}$ | 58.4893 | 46.0517 | 36.9043 | 2.0 | 1.0 |
| $10^{50}$ | $2.0\times10^{25}$ | 216.228 | 115.129 | 68.3772 | 2.0 | 1.0 |
| $10^{100}$ | $2.0\times10^{50}$ | 900.0 | 230.259 | **90.0** | 2.0 | 1.0 |
| **limit** | **div** | **div** | **div** | **100** | **2** | **1** |

*Marking B1: 18 for a complete correct table. B2: 7 for correct convergence marking **derived from A3, not from the appearance of the numbers.***

---

## Part C — What the Table Shows (30 pts)

### C1 (10)

At $T=10^6$:

| $p$ | value | fate |
|---|---|---|
| $0.99$ | $14.82$ | diverges |
| $1$ | $13.82$ | diverges |
| $1.01$ | $12.90$ | **converges to 100** |

**(a)** Largest is $p=0.99$; **smallest is $p=1.01$.**

**(b)** **Only $p=1.01$ converges** — and it is the smallest of the three.

**(c)** The reasoning fails because **the three columns are not "the same"; they are at different stages of completely different journeys.** Specifically:

- $p=1.01$ at $12.90$ has covered $12.9\%$ of the distance to its limit of $100$ — it is *early*, not *settled*.
- $p=1$ at $13.82$ is $\ln(10^6)$ and will grow without bound, but so slowly that it will never *look* like it.

**The numbers agree only because a convergent sequence early in its approach and a divergent one growing logarithmically are numerically indistinguishable.** Nothing about the values distinguishes "slowly approaching 100" from "slowly approaching infinity", and no larger $T$ within reach changes that.

*Marking: 2 + 2 + 6. **(c) is the lab.** Full marks require identifying that $p=1.01$ is early in its approach rather than settled. "They're different because the $p$-test says so" earns 2 — true, but it does not explain why the numbers mislead.*

### C2 (8)

**(a)** $\dfrac{12.9036}{100} = \mathbf{12.9\%}$ of its limit at $T=10^6$.

**(b)** Require $F(T,1.01) = 90$:

$$\frac{1-T^{-0.01}}{0.01} = 90 \implies 1-T^{-0.01} = 0.9 \implies T^{-0.01}=0.1$$

$$\implies -0.01\log_{10}T = -1 \implies \log_{10}T = 100 \implies \boxed{T = 10^{100}}$$

*Verified: $F(10^{100},1.01) = 90.0$ exactly.*

**(c)** $10^{100}$ is a **googol** — larger than the number of atoms in the observable universe (about $10^{80}$) by twenty orders of magnitude. **It is not reachable by any computation, now or ever.** And it only gets to 90%.

*Marking: 2 + 4 + 2. **The algebra in (b) must be shown**; quoting $10^{100}$ from the lab sheet earns 1 of the 4.*

### C3 (6)

$F(T,2) = 1-\frac1T$, so $90\%$ of its limit of 1 requires $1-\frac1T = 0.9$, i.e. $\boxed{T=10}$.

*Verified: $F(10,2)=0.9$ exactly.*

**$T=10$ against $T=10^{100}$ — and both integrals converge.**

**The difference:** the rate of approach is governed by $T^{1-p}$, and $1-p$ is $-1$ for $p=2$ but only $-0.01$ for $p=1.01$. **How close $p$ sits to the threshold controls everything.** Convergence is a yes/no fact; the *speed* of convergence is a separate matter entirely, and it degenerates without limit as $p\to1^+$.

*Marking: 3 for $T=10$, 3 for the explanation. **Full marks require identifying $1-p$ as the controlling exponent**, not merely "$p=2$ converges faster".*

### C4 (6)

| $p$ | growth of $F(T,p)$ | at $10^2$ | at $10^6$ | at $10^{20}$ | at $10^{100}$ |
|---|---|---|---|---|---|
| $0.5$ | $2\sqrt T - 2$ — **power** | 18.0 | 1998 | $2\times10^{10}$ | $2\times10^{50}$ |
| $1$ | $\ln T$ — **logarithmic** | 4.61 | 13.82 | 46.05 | 230.26 |

**$p=0.5$ is obviously divergent**: the values explode, and no one would mistake $2\times10^{50}$ for a limit.

**$p=1$ is invisibly divergent**: $\ln T$ grows so slowly that after a googol it has reached only 230. Every finite computation shows a modest, slowly-increasing number — exactly what a slowly-converging sequence also shows.

> **Divergence is not the same as blowing up.** A quantity can increase forever and still look, at
> every scale you can inspect, like it is settling down.

*Marking: 4 for the two growth forms identified from the formula, 2 for the contrast. **Both forms must come from the closed form**, not be guessed from the numbers.*

---

## Part D — A Pair Powers Cannot Separate (15 pts)

### D1 (5) — the proofs

Both use $u=\ln x$, $du=\frac{dx}{x}$; when $x=2$, $u=\ln2$.

$$\int_2^\infty\frac{dx}{x\ln x} = \int_{\ln2}^{\infty}\frac{du}{u} = \infty \qquad\textbf{diverges}$$

$$\int_2^\infty\frac{dx}{x(\ln x)^2} = \int_{\ln2}^{\infty}\frac{du}{u^2} = \frac{1}{\ln2} \qquad\textbf{converges}$$

**Both reduce to the $p$-test in $u$**, with $p=1$ and $p=2$ respectively.

*Verified symbolically: $\infty$ and $\frac{1}{\ln 2} = 1.4427$.*

*Marking: 2 + 3. **The substitution turning both into the $p$-test is the insight** — this is why $\ln$ is the natural next scale after powers.*

### D2 (6) — numerically

Exact partial integrals: $\int_2^T\frac{dx}{x\ln x} = \ln\ln T - \ln\ln 2$ and $\int_2^T\frac{dx}{x(\ln x)^2} = \frac{1}{\ln2}-\frac{1}{\ln T}$.

| $T$ | divergent one | convergent one |
|---|---|---|
| $10^2$ | 1.8937 | 1.2255 |
| $10^6$ | 2.9923 | 1.3703 |
| $10^{20}$ | 4.1963 | 1.4210 |
| $10^{100}$ | **5.8057** | **1.43835** |

Limit of the convergent one: $\frac{1}{\ln2} = 1.442695$.

**At $T=10^{100}$:** the convergent one is $1.43835$, still $0.3\%$ short of its limit. The divergent one has reached only $5.81$ — and it **diverges like $\ln\ln T$**, the slowest divergence in ordinary mathematics.

*Marking: 4 for the table, 2 for the commentary. **The striking fact is that the divergent integral is at 5.81 after a googol**; make sure they notice it.*

### D3 (4)

Write $f(x)=\frac{1}{x\ln x}$. For any $q$:

- **$q=1$:** $\frac{f(x)}{1/x} = \frac{1}{\ln x}\to0$. The limit is 0, so limit comparison with $\frac1x$ is inconclusive in the useful direction — $L=0$ only helps if the comparison **converges**, and $\int\frac{dx}x$ diverges.
- **$q=1+\epsilon$ for any $\epsilon>0$:** $\frac{f(x)}{x^{-1-\epsilon}} = \frac{x^{\epsilon}}{\ln x}\to\infty$. So $f$ is eventually **larger** than a convergent comparison — again no conclusion.

**So $\frac{1}{x\ln x}$ sits strictly between $x^{-1}$ and $x^{-1-\epsilon}$ for every $\epsilon>0$**: smaller than the divergent benchmark, larger than every convergent one. No power can decide it.

The same holds for $\frac{1}{x(\ln x)^2}$ — and since one converges and the other diverges while **both** occupy that same gap, no power-based test could possibly separate them.

*Marking: 4. **The key observation is that the two functions occupy the same gap yet have different fates**, which proves no power test suffices. Award 2 for computing the two limits without drawing that conclusion.*

---

## Part E — Reflection (10 pts)

### E1 (5)

The missing entry: **numerics cannot determine the answer at all, at any $T$.**

| Lab | How badly numerics loses |
|---|---|
| **0** | Not at all — numerics *won*. 10 digits from 128 points. |
| **2** | Numerics gives the value but **cannot prove the inequality** — it gives evidence, not proof. |
| **1** | Numerics works but costs $8\times10^9$ against 128 — a factor of $6\times10^7$. |
| **3** | **Numerics fails outright.** No finite $T$ decides it. |

**Ranking (worst last): 0, 1, 2, 3** — or with 1 and 2 interchanged, since Lab 1 is a quantitative loss and Lab 2 a qualitative one; **accept either order for those two if justified.**

*Marking: 3 for the entry, 2 for a justified ranking. **Lab 3 must be last** — it is the only one where numerics cannot succeed at any cost. Deduct 2 if Lab 0 is not identified as a case where numerics won; the course is not arguing that numerical methods are bad.*

### E2 (5)

**The question changed from "what is the value?" to "does the limit exist?"**

A finite computation can estimate a value to any accuracy you are willing to pay for — that is Lab 0, and it works.

But **convergence is a statement about a limit, i.e. about the entire infinite tail**, and no finite amount of the tail constrains the rest of it. Any finite table is consistent with both convergence and divergence: the $T=10^6$ row of Part B contains a convergent column and two divergent ones that are numerically indistinguishable.

**A finite computation cannot establish an infinitary statement.** The $p$-test can, because it argues about the limit directly rather than sampling it.

*Marking: 5. **The essential idea is that convergence is a property of the whole tail**, which no finite prefix determines. "Because the numbers are too close together" earns 2 — that is the symptom, not the reason.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 20 |
| B | 25 |
| C | 30 |
| D | 15 |
| E | 10 |
| **Total** | **100** |

---

## Checkoff Checklist

1. **A3 limits stated before the table was computed**
2. Table matches to the digits shown (no machine variation excuse)
3. **C1(c) identifies $p=1.01$ as early in its approach, not settled**
4. C2(b) shows the algebra reaching $T=10^{100}$
5. **C3 identifies $1-p$ as the controlling exponent**
6. C4 gives both growth forms from the closed form
7. D3 shows both functions occupy the same gap between powers
8. **E2 says convergence is a statement about the whole tail**

---

## Note for the Debrief

This is the fourth lab and the arc closes here. Put the four side by side:

> **Lab 0:** numerics won — ten digits from 128 points.
> **Lab 1:** numerics worked, sixty million times more expensively than it needed to.
> **Lab 2:** numerics gave the number but could not give the proof.
> **Lab 3:** numerics cannot answer the question at all.

Then the point:

> Nothing here says computation is bad — **Lab 0 is a genuine success and you will use those methods
> for the rest of your career.** What changed across the four labs is **the question**. "What is this
> number?" is a question a computer answers well. **"Does this limit exist?" is not.**
>
> At $T$ equal to a googol, $\int_1^T x^{-1.01}dx$ has reached 90 of its eventual 100, and
> $\int_1^T x^{-1}dx$ has reached 230 on its way to infinity. **You cannot tell these apart by
> looking, and neither can any machine that will ever be built.** One line of exact reasoning tells
> them apart immediately.

Then point forward:

> **Every question in the second half of this course is of the second kind.** Does this series
> converge? What is its radius of convergence? Does this approximation improve without bound? Starting
> in Week 6, the exact methods are the only methods.

---

*MATH 142 · Week 3 · Lab 03 Solutions · Instructor Only*
