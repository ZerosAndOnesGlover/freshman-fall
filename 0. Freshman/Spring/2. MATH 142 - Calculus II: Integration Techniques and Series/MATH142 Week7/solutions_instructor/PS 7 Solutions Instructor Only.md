# MATH 142 · Calculus II
## Problem Set 7 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Every sum verified symbolically; every verdict corroborated by numerical partial sums.

> **Marking philosophy.** **The test and its hypotheses are the answer.** A correct verdict reached by
> an invalid route scores at most 2 out of 6; a correct route with an arithmetic slip keeps most of
> its marks.
>
> **Zero marks, every time, for "the terms go to zero, so it converges."** A4 exists to make that
> unmistakable.

---

## Part A — Geometric and Telescoping (5 pts each)

### A1 (5) $\;\sum_{n=0}^\infty 3\left(\frac25\right)^n$

First term $3$, ratio $\frac25$ with $|r|<1$:

$$\frac{3}{1-\frac25} = \frac{3}{3/5} = \boxed{5}$$

*Verified.*

*Marking: 1 for checking $|r|<1$, 4 for the value.*

### A2 (5) $\;\sum_{n=2}^\infty\left(-\frac13\right)^n$

**Starts at $n=2$**, so the first term is $\left(-\frac13\right)^2 = \frac19$, and $r=-\frac13$:

$$\frac{1/9}{1+\frac13} = \frac{1/9}{4/3} = \boxed{\frac{1}{12}}$$

*Verified.*

*Marking: **3 of the 5 for handling the starting index.** Using $\frac{1}{1-r}=\frac34$ (as if starting at $n=0$) is the standard error. **Emphasise $\frac{\text{first term}}{1-r}$.***

### A3 (5) $\;\sum_{n=1}^\infty\frac{1}{n(n+3)}$

Partial fractions: $\dfrac{1}{n(n+3)} = \dfrac13\left(\dfrac1n-\dfrac{1}{n+3}\right)$.

**The gap is 3, so three terms survive at each end:**

$$s_N = \frac13\left(1+\frac12+\frac13-\frac{1}{N+1}-\frac{1}{N+2}-\frac{1}{N+3}\right)$$

$$\longrightarrow \frac13\cdot\frac{11}{6} = \boxed{\frac{11}{18}}$$

*Verified.*

*Marking: 2 decomposition, **2 for identifying the three surviving terms**, 1 limit. **A student who kept only one term at each end gets $\frac13$** — a plausible wrong answer, which is why the problem asked for the first and last four terms written out.*

### A4 (5) $\;\sum_{n=1}^\infty\ln\!\left(\frac{n+1}{n}\right)$ — **the trap**

$\ln\frac{n+1}{n} = \ln(n+1)-\ln n$, so the sum telescopes:

$$s_N = \ln(N+1)-\ln1 = \ln(N+1) \longrightarrow \boxed{\infty}$$

**Diverges.**

*Verified: the partial sum to $N=10^6$ is $13.815511558$, exactly $\ln(10^6+1)$.*

**What this shows:** the terms $\ln\frac{n+1}{n} = \ln\left(1+\frac1n\right)\to\ln1 = 0$. **The terms tend to zero and the series diverges** — so the $n$-th Term Test is inconclusive here and proves nothing.

*Marking: 2 for telescoping, 1 for the verdict, **2 for the comment about the $n$-th Term Test.***

> **This is the set's most valuable question.** It is a second harmonic-series-style counterexample,
> and unlike the harmonic series its divergence is completely transparent once telescoped.

---

## Part B — Integral Test and $p$-Series (6 pts each)

### B1 (6) $\;\sum n^{-3/2}$

$p=\frac32>1$, so it **converges** by the $p$-series test.

*(Value: $\zeta(3/2)\approx2.612$ — no elementary closed form, as expected for a non-even $p$.)*

*Marking: 2 for identifying $p$, 4 for the verdict with the criterion stated.*

### B2 (6) $\;\sum\frac{n}{n^2+1}$

**Hypotheses:** $f(x)=\frac{x}{x^2+1}$ is positive on $[1,\infty)$; continuous (denominator never zero); and

$$f'(x) = \frac{(x^2+1)-x(2x)}{(x^2+1)^2} = \frac{1-x^2}{(x^2+1)^2} < 0 \text{ for } x>1$$

so **decreasing** ✓ (all three checked).

$$\int_1^\infty\frac{x\,dx}{x^2+1} = \lim_{T\to\infty}\frac12\ln(x^2+1)\Big|_1^T = \infty$$

**Diverges.**

*Corroborated: partial sums $4.52,\ 9.12,\ 13.72$ at $N=10^2,10^4,10^6$ — increments of $\approx4.6=\ln100$, i.e. logarithmic.*

*Marking: **3 of the 6 for verifying all three hypotheses**, since the question demanded it. 3 for the integral.*

*(Limit comparison with $\frac1n$ also works and is faster — award full marks, but note the question specified the Integral Test.)*

### B3 (6) $\;\sum_{n\ge2}\frac{1}{n(\ln n)^3}$

$u=\ln x$: $\;\int_2^\infty\frac{dx}{x(\ln x)^3} = \int_{\ln2}^\infty\frac{du}{u^3} = \frac{1}{2(\ln2)^2} = 1.04068$ — finite. **Converges.**

*Marking: 2 substitution, 2 evaluation, 2 verdict. **This is the $p$-test in $u$ with $p=3>1$** — students should say so.*

> **A cautionary note on the value, for TAs.** `mpmath`'s `nsum` reports $2.06051618$ for this sum.
> **That is wrong** — and it is the *third* `nsum` failure found while preparing this week (see
> Lecture 3 §5 and D2 below).
>
> The Integral Test settles it. Bracketing the tail of the partial sum at $N=10^6$:
> $$2.065886539 \le S \le 2.065886539$$
> — the two bounds agree to **10 significant figures**, giving $S = \boldsymbol{2.0658865}$.
>
> **Students are not asked for the value**, only the verdict, so this affects no marking. It is
> recorded because a TA who checks against `nsum` will get a different number, and the library is the
> one that is wrong.

### B4 (6) $\;\sum ne^{-n^2}$

$f(x)=xe^{-x^2}$ is positive; $f'(x) = e^{-x^2}(1-2x^2)<0$ for $x\ge1$ ✓ decreasing.

$$\int_1^\infty xe^{-x^2}dx = \left[-\tfrac12e^{-x^2}\right]_1^\infty = \frac{1}{2e}$$

**Converges.**

*Corroborated: the sum is $0.4048814$.*

*Marking: 2 hypotheses, 2 integral (a Week 0 substitution), 2 verdict.*

### B5 (6) — remainder estimate for $\sum n^{-3}$

**(a)** $R_N\le\int_N^\infty x^{-3}dx = \dfrac{1}{2N^2}$. Require $\dfrac{1}{2N^2}<10^{-3}$:

$$N^2>500 \implies N>22.36 \implies \boxed{N=23}$$

**(b)** With $N=23$:

$$\frac{1}{2(24)^2} \le R_{23}\le\frac{1}{2(23)^2},\qquad\text{i.e.}\qquad 8.68\times10^{-4}\le R_{23}\le 9.45\times10^{-4}$$

**(c)** Estimate $S\approx s_{23}+\frac12\left(\frac{1}{2(24)^2}+\frac{1}{2(23)^2}\right)$.

**Why better:** $s_N$ alone ignores the entire remainder, so its error *is* $R_N\approx9\times10^{-4}$. The average sits inside a bracket of width $9.45-8.68 = 0.77\times10^{-4}$, so **its error is at most half that width** — an order of magnitude better, for one extra term.

*Marking: 2 + 2 + 2. **(c) must argue from the width of the bracket**, not merely assert "averages are better".*

---

## Part C — Comparison (6 pts each)

*Standard marking: 2 comparison series, 2 justification (inequality or limit), 2 verdict.*

### C1 (6) $\;\sum\frac{n^2+1}{n^4+3}$ — **converges**

Behaves like $\frac{n^2}{n^4}=\frac1{n^2}$. Limit comparison with $n^{-2}$:

$$L = \lim\frac{n^4+n^2}{n^4+3} = 1 \in(0,\infty)$$

$\sum n^{-2}$ converges, so ours does.

*Corroborated: settles at $0.67242$.*

### C2 (6) $\;\sum_{n\ge2}\frac{1}{n-\ln n}$ — **diverges**

Limit comparison with $\frac1n$:

$$L = \lim\frac{n}{n-\ln n} = \lim\frac{1}{1-\frac{\ln n}{n}} = 1$$

(using $\frac{\ln n}{n}\to0$ from Week 6). $\sum\frac1n$ diverges, so ours does.

*Corroborated: $5.42,\ 10.07,\ 14.68$ — logarithmic growth.*

*(Direct comparison also works: $n-\ln n<n$ so $\frac{1}{n-\ln n}>\frac1n$.)*

### C3 (6) $\;\sum\frac{2+\cos n}{n^2}$ — **converges**

$\cos n\le1$, so $0<\frac{2+\cos n}{n^2}\le\frac{3}{n^2}$, and $\sum\frac{3}{n^2}$ converges.

**Why not the Integral Test:** $f(x)=\frac{2+\cos x}{x^2}$ is **not decreasing** — the numerator oscillates — so the hypothesis fails. **Comparison has no monotonicity requirement.**

*Corroborated: settles at $1.0737$, below $3\cdot\frac{\pi^2}{6}=4.93$ ✓.*

*Marking: **2 of the 6 for the explanation about monotonicity**, which the question asked for.*

### C4 (6) $\;\sum_{n\ge2}\frac{1}{n^{1+1/n}}$ — **diverges**

Limit comparison with $\frac1n$:

$$\frac{a_n}{1/n} = \frac{n}{n^{1+1/n}} = n^{-1/n} = \frac{1}{n^{1/n}}$$

and $n^{1/n}\to1$ (Week 6), so $L=1\in(0,\infty)$. **Since $\sum\frac1n$ diverges, so does ours.**

*Corroborated: $3.41,\ 7.96,\ 12.56$ — logarithmic.*

> **This is the hardest problem on the set.** The exponent $1+\frac1n$ **exceeds 1 for every $n$**, so
> a student may reason "it's a $p$-series with $p>1$, so it converges." **That is wrong**: the
> $p$-series test requires a *fixed* $p$, and here the exponent drifts down to 1. **The extra $\frac1n$
> contributes a factor $n^{-1/n}\to1$, which is not enough to help.**
>
> Expect this error and mark it as a hypothesis failure, not an arithmetic one.

*Marking: 2 for the ratio simplification, 2 for $n^{1/n}\to1$, 2 for the verdict. **A student who answered "converges, $p>1$" scores 0** — but flag it as the instructive error it is.*

### C5 (6) $\;\sum\frac{\arctan n}{n^2}$ — **converges**

$\arctan n<\frac\pi2$ for all $n$, so $0<\frac{\arctan n}{n^2}<\frac{\pi/2}{n^2}$, and $\sum\frac{\pi/2}{n^2}$ converges.

*Corroborated: settles at $0.82188$.*

*Marking: **the key step is bounding $\arctan$ by $\frac\pi2$** — a bounded factor over a convergent $p$-series.*

---

## Part D — Concept (10 pts each)

### D1 (10) — the $n$-th Term Test

**(a)** If $a_n\not\to0$ then $\sum a_n$ diverges.

**(b)** Suppose $\sum a_n$ converges, say $s_N\to S$. Then $s_{N-1}\to S$ as well, so

$$a_N = s_N-s_{N-1}\longrightarrow S-S = 0 \qquad\blacksquare$$

**(c)** The test's conclusion is about the terms, not the sum: **knowing $a_n\to0$ leaves both possibilities open**, and examples of each exist.

- Convergent with $a_n\to0$: $\;\sum\frac{1}{n^2} = \frac{\pi^2}{6}$
- Divergent with $a_n\to0$: $\;\sum\frac1n$, and also A4's $\sum\ln\frac{n+1}{n}$

**(d)** A student checking only the $n$-th Term Test on A4 finds $a_n\to0$, and — if they misread the test as an iff — concludes convergence. **In fact the test is silent**, and they should have gone on to another method. Here **telescoping** settles it: $s_N = \ln(N+1)\to\infty$.

*Marking: 2 + 3 + 3 + 2. **(c) must give two examples**, and (d) must say the test is *silent* rather than that it "fails".*

### D2 (10) — checking a machine

**(a)** $s_{10^6} = 0.937533438812$. *(Verified.)*

**(b)** All terms $\frac{\ln n}{n^2}$ are **non-negative** (for $n\ge1$), so the partial sums are **non-decreasing** and every one is $\le S$. But

$$s_{10^6} = 0.937533\ldots \;>\; 0.936716\ldots = \text{(library's answer)}$$

**A partial sum cannot exceed the total. Therefore the library's answer is wrong** — established using nothing but the definition of a series and the sign of the terms.

**(c)** The Integral Test gives $R_N\le\int_N^\infty\frac{\ln x}{x^2}dx = \frac{\ln N+1}{N}$. At $N=10^6$ that is $1.48\times10^{-5}$, so

$$S \approx 0.937533439 + 0.0000148155 = \boxed{0.9375482543}$$

*(Verified: the true value is $-\zeta'(2) = 0.937548254316$ — the estimate agrees to 11 digits.)*

**(d)** The habit is: **know a property the answer must have, and check it.** Here it was monotonicity of partial sums; earlier in the course it was differentiating an antiderivative (Weeks 0–2), checking a sign (Week 3), and comparing two independent methods (Week 4).

**The link to the earlier CAS failures:** those were *symbolic* — unevaluated integrals, wrong branches, unrecognisable forms. **This one is numerical, and more dangerous, because it returned a plausible number to twelve figures with no warning.** A symbolic failure announces itself; a numerical one does not.

*Marking: 2 + 4 + 2 + 2. **(b) carries the most weight and must not appeal to the known value.** A student who looked up $-\zeta'(2)$ and compared has answered a different, easier question — award 1.*

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Geometric, telescoping, and a trap |
| B (5 × 6) | 30 | Integral Test, hypotheses, remainders |
| C (5 × 6) | 30 | Direct and limit comparison |
| D (2 × 10) | 20 | The $n$-th Term Test; checking a machine |
| **Total** | **100** | |

---

## Diagnostic Notes

| Question | Weakness | Bites in |
|---|---|---|
| **A2** | Ignoring the starting index | Week 9 (power series) |
| **A4 / D1** | Reading the $n$-th Term Test as an iff | Week 8, constantly |
| **C4** | Applying $p$-series with a non-constant exponent | Week 8 (Ratio/Root tests) |
| **C3** | Not checking the Integral Test's monotonicity | Midterm 2 |

**Week 8 introduces four more tests, each with hypotheses.** The habit to establish now is C4's lesson: **a test applies when its hypotheses hold, and "the exponent is bigger than 1" is not the same as "$p>1$ for a fixed $p$."**

---

*MATH 142 · Week 7 · PS 7 Solutions · Instructor Only*
