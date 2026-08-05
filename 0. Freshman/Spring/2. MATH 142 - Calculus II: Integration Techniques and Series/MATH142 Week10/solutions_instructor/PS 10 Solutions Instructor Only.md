# MATH 142 · Calculus II
## Problem Set 10 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Every series and numerical value verified symbolically.

> **Marking philosophy.** **Reward manipulation, penalise brute force.** A student who computed
> $f^{(8)}(0)$ by eight differentiations in C5 has the right answer by the wrong method and should
> lose 3 of the 6 — the whole point of the week is that the library replaces differentiation.
>
> **Every error bound must name its type and its interval.**

---

## Part A — Building Series (5 pts each)

### A1 (5) $\;e^{3x}$

Substitute $3x$: $\;\displaystyle\sum_{n=0}^\infty\frac{(3x)^n}{n!} = \boxed{\sum_{n=0}^\infty\frac{3^nx^n}{n!}}$, $R=\infty$.

*Verified: $1+3x+\frac{9x^2}{2}+\frac{9x^3}{2}+\cdots$*

### A2 (5) $\;x^2\sin x$

$$x^2\sum_{n\ge0}\frac{(-1)^nx^{2n+1}}{(2n+1)!} = \boxed{\sum_{n=0}^\infty\frac{(-1)^nx^{2n+3}}{(2n+1)!}}, \qquad R=\infty$$

*Verified: $x^3-\frac{x^5}{6}+\frac{x^7}{120}-\cdots$*

### A3 (5) $\;\frac{1}{1+x^3}$

Substitute $-x^3$ into the geometric series:

$$\boxed{\sum_{n=0}^\infty(-1)^nx^{3n}}, \qquad |x^3|<1 \implies R=1$$

*Verified: $1-x^3+x^6-x^9+\cdots$*

### A4 (5) $\;\ln x$ at $a=1$

Write $\ln x = \ln\big(1+(x-1)\big)$ and use the standard series with $u=x-1$:

$$\boxed{\ln x = \sum_{n=1}^\infty\frac{(-1)^{n+1}(x-1)^n}{n} = (x-1)-\frac{(x-1)^2}{2}+\frac{(x-1)^3}{3}-\cdots}$$

$R=1$, so it converges on $(0,2]$.

*Verified.*

*Marking: **4 of the 5 for using the substitution rather than differentiating $\ln x$ repeatedly.** Both give the same answer; only one is a method.*

---

## Part B — Remainders (6 pts each)

### B1 (6) — $P_3$ for $e^x$

**(a)** $P_3(x) = 1+x+\frac{x^2}{2}+\frac{x^3}{6}$

**(b)** $f^{(4)}(t)=e^t$, and on $[0,1]$ we have $e^t\le e$. **So $M=e$ is valid on that interval** (it would not be on $\mathbb R$):

$$|R_3(x)|\le\frac{e\cdot1^4}{4!} = \frac{e}{24} \approx \boxed{0.1133}$$

**(c)** True error at $x=1$: $e - P_3(1) = 2.71828 - 2.66667 = \boxed{0.05162}$.

**The bound is about 2.2 times the true error** — honest and loose, as expected.

*Verified: bound $0.11326$, true error $0.051615$, bound holds ✓.*

*Marking: 1 + **3 for $M=e$ with the interval stated** + 2.*

### B2 (6) — terms for $\cos(0.3)$ to $10^{-8}$

$M=1$ (all derivatives of $\cos$ are bounded by 1), so $|R_n|\le\frac{0.3^{n+1}}{(n+1)!}$:

| $n$ | bound |
|---|---|
| $5$ | $1.01\times10^{-6}$ |
| $6$ | $4.34\times10^{-8}$ |
| $7$ | $\mathbf{1.63\times10^{-9}}$ ✓ |

**$n=7$ is the first degree that suffices.** *(Verified — $n=6$ just misses.)*

Since $\cos$ has only **even** powers, $P_7 = P_6 = 1-\frac{x^2}{2}+\frac{x^4}{24}-\frac{x^6}{720}$:

$$\boxed{\textbf{four nonzero terms}}$$

*Marking: 4 for $n=7$, **2 for converting to the nonzero-term count** (the question asked).*

### B3 (6) — $\sqrt{1.1}$

$$\sqrt{1+x} = 1+\frac x2-\frac{x^2}{8}+\frac{x^3}{16}-\cdots$$

At $x=0.1$: $\;1+0.05-0.00125+0.0000625 = \boxed{1.0488125}$

True: $\sqrt{1.1} = 1.04880885$. **Error $3.65\times10^{-6}$** — five correct significant figures from four terms. *(Verified.)*

### B4 (6) — $\sin(0.2)$

$$\sin(0.2)\approx 0.2-\frac{0.2^3}{6} = 0.2-0.00133333 = 0.19866667$$

**Alternating estimate:** the first omitted term is $\frac{0.2^5}{120} = \boxed{2.667\times10^{-6}}$.

**True error:** $\sin(0.2) = 0.19866933$, so the error is $2.66\times10^{-6}$.

**The bound is tight to about 0.2%** — much better than Lagrange typically manages.

*Marking: 3 estimate, 3 bound with the comparison.*

### B5 (6) — the counterexample

**(a)**

| $x$ | $f(x)$ | $f(x)/x^{10}$ |
|---|---|---|
| $0.5$ | $1.8316\times10^{-2}$ | $18.755$ |
| $0.2$ | $1.3888\times10^{-11}$ | $1.3562\times10^{-4}$ |
| $0.1$ | $3.7201\times10^{-44}$ | $3.7201\times10^{-34}$ |

*(Verified.)*

**(b)** $\dfrac{f(x)}{x^k}\to0$ as $x\to0$, **for every fixed $k$** — $f$ vanishes faster than any power.

**(c)** With every $f^{(n)}(0)=0$, the Maclaurin series is

$$0+0\cdot x+0\cdot x^2+\cdots = 0$$

**It converges for all $x$ (so $R=\infty$), to the zero function.**

**(d)** **No contradiction.** Taylor's theorem does not claim $f$ equals its series; it says

$$f(x) = P_n(x)+R_n(x)$$

Here $P_n\equiv0$, so $R_n(x) = f(x)$ **for every $n$** — and $R_n(x)\not\to0$ for $x\ne0$. **The theorem's conclusion holds exactly; the condition $R_n\to0$ simply fails.**

*Marking: 2 + 1 + 1 + 2. **(d) must identify $R_n(x)=f(x)$** as the reason. "Because the series is wrong" earns 0 — the series is the correct Taylor series; it just does not represent $f$.*

---

## Part C — Applications (6 pts each)

### C1 (6)

$$e^x-1-x-\frac{x^2}{2} = \frac{x^3}{6}+\frac{x^4}{24}+\cdots \implies \frac{\cdots}{x^3} = \frac16+\frac{x}{24}+\cdots\longrightarrow\boxed{\frac16}$$

*Verified.*

### C2 (6) $\;\int_0^{1/2}e^{-x^2}dx$

$$= \sum_{n=0}^\infty\frac{(-1)^n(1/2)^{2n+1}}{n!\,(2n+1)}$$

Four terms: $0.5 - 0.0416667+0.003125-0.000186012 = \boxed{0.46127232}$

**Error bound (alternating):** the next term is $\frac{(1/2)^9}{4!\cdot9} = 9.04\times10^{-6}$.

*(Verified: the true error at four terms is $8.685\times10^{-6}$ — inside the bound ✓.)*

*Marking: 3 series, 2 value, 1 bound.*

### C3 (6) $\;\int_0^1\frac{1-\cos x}{x^2}dx$

$$1-\cos x = \frac{x^2}{2!}-\frac{x^4}{4!}+\cdots \implies \frac{1-\cos x}{x^2} = \frac{1}{2!}-\frac{x^2}{4!}+\frac{x^4}{6!}-\cdots$$

Integrating over $[0,1]$:

$$\boxed{\sum_{n=1}^\infty\frac{(-1)^{n+1}}{(2n)!\,(2n-1)}} = \frac12-\frac{1}{72}+\frac{1}{3600}-\cdots$$

Four terms: $0.48638535$. *(Verified — the true value is $0.48638538$.)*

**Why the series is well behaved at 0:** the integrand's apparent singularity is **removable** — the numerator's lowest power is $x^2$, which cancels the denominator exactly. **The series has constant term $\frac12$ and no pole at all**; the original formula only *appeared* to have one.

*Marking: 3 series, 2 value, **1 for the removable-singularity explanation.***

### C4 (6) $\;\sqrt[3]{1.03}$

$$(1+x)^{1/3} = 1+\frac x3-\frac{x^2}{9}+\frac{5x^3}{81}-\cdots$$

At $x=0.03$: $\;1+0.01-0.0001+0.00000167 = \boxed{1.00990167}$

True: $1.00990163$. **Error $4\times10^{-8}$.** *(Verified.)*

### C5 (6) — $f^{(8)}(0)$ for $f=x^2e^{x^3}$

$$f(x) = x^2\sum_{n\ge0}\frac{x^{3n}}{n!} = \sum_{n=0}^\infty\frac{x^{3n+2}}{n!}$$

**The $x^8$ term needs $3n+2=8$, i.e. $n=2$**, giving $c_8 = \frac{1}{2!} = \frac12$. Then

$$f^{(8)}(0) = 8!\,c_8 = \frac{40320}{2} = \boxed{20160}$$

*Verified: the series is $x^2+x^5+\frac{x^8}{2}+\frac{x^{11}}{6}+\cdots$*

*Marking: 2 series, 2 coefficient, 2 conversion. **A student who differentiated eight times loses 3** — the question said "without differentiating", and the technique is the point.*

---

## Part D — Concept (10 pts each)

### D1 (10)

**(a)** *(Statement as in Lecture 2.)*

**(b)** $f$ equals its Taylor series on an interval **precisely where $R_n(x)\to0$ as $n\to\infty$.**

**(c)** For $f=\sin$, every derivative is $\pm\sin$ or $\pm\cos$, so $\left|f^{(n+1)}\right|\le1$ **everywhere**; take $M=1$:

$$|R_n(x)|\le\frac{|x|^{n+1}}{(n+1)!}$$

For any **fixed** $x$, this $\to0$ because **factorials beat exponentials** — Week 6's growth hierarchy, $\frac{a^n}{n!}\to0$. Hence $R_n\to0$ for every real $x$, and $\sin$ equals its series on all of $\mathbb R$. $\blacksquare$

**(d)** For B5's $f$, the Taylor polynomials are all zero, so $R_n(x) = f(x)-0 = f(x)$, which is **nonzero and constant in $n$** for any $x\ne0$. **$R_n\not\to0$**, so condition (b) fails, and the theorem correctly declines to conclude that $f$ equals its series.

*Marking: 2 + 2 + 4 + 2. **(c) must cite the growth hierarchy**, not merely assert the limit.*

### D2 (10) — Week 0's debt

**(a)** $e^{-x^2} = \sum\frac{(-1)^nx^{2n}}{n!}$ with $R=\infty$; integrating term by term over $[0,1]$:

$$\int_0^1e^{-x^2}dx = \sum_{n=0}^\infty\frac{(-1)^n}{n!}\cdot\frac{1}{2n+1} = \sum_{n=0}^\infty\frac{(-1)^n}{n!(2n+1)}$$

**(b)** Alternating with decreasing terms, so the error is at most the first omitted term $\frac{1}{n!(2n+1)}$. Requiring this $<5\times10^{-11}$:

| terms | error |
|---|---|
| $12$ | $7.79\times10^{-11}$ |
| $\mathbf{13}$ | $\mathbf{5.58\times10^{-12}}$ ✓ |

$$\boxed{13 \text{ terms}}$$

*(Verified.)*

**(c)** Simpson needed **128 function evaluations**; the series needs **13 terms** — roughly a **10-fold** reduction in work, and each term is a single division rather than an exponential evaluation.

**More importantly:** the series carries a **rigorous, a priori error bound** (the next term), whereas Simpson's order was *measured* in Lab 0, not proved. **The series can promise its accuracy before running.**

**(d)** The four theorems:

| Theorem | Week | What it licenses |
|---|---|---|
| **Taylor's theorem** ($R_n\to0$) | 10 | that $e^{-x^2}$ *equals* its series, not merely has one |
| **Term-by-term integration** inside $R$ | 9 | swapping $\int$ and $\sum$ |
| **Rearrangement of absolutely convergent series** | 8 | why that swap is safe |
| **Alternating series estimate** | 8 | the error bound, free |

*Marking: 2 + 2 + 3 + 3. **(d) must name four distinct results with what each licenses.** A vague "by the theory of series" earns 0 of the 3.*

> **This question is the course's closing argument** and is worth reading aloud when returning the
> set. Week 0 asserted an impossibility; Weeks 8–10 built the machinery; the computation is three
> lines and every line has a named justification.

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Building series by manipulation |
| B (5 × 6) | 30 | Both error bounds; the counterexample |
| C (5 × 6) | 30 | Limits, integrals, coefficient extraction |
| D (2 × 10) | 20 | $R_n\to0$; Week 0's debt |
| **Total** | **100** | |

---

## Diagnostic Notes

| Question | Weakness | Bites in |
|---|---|---|
| **A4 / C5** | Differentiating instead of manipulating | The final |
| **B1** | Quoting $M$ without an interval | The final |
| **B5(d) / D1(d)** | Thinking the counterexample breaks the theorem | Conceptually, permanently |
| **D2(d)** | Not tracking which theorem licenses which step | The final's conceptual section |

**Week 11 solves differential equations**, including by power series — where every manipulation from this set is used again, on an unknown function.

---

*MATH 142 · Week 10 · PS 10 Solutions · Instructor Only*
