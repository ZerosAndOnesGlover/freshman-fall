# MATH 142 · Calculus II
## Problem Set 8 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Every limit and value verified symbolically; every verdict corroborated numerically.

> **Marking philosophy.** Two things carry the marks this week:
> **(1) both hypotheses of the Alternating Series Test**, and
> **(2) classifying convergence as absolute or conditional.**
>
> A student who writes "converges by AST" having checked only $b_n\to0$ has done half the work and
> should get half the marks. **"Converges" without the absolute/conditional classification is
> incomplete** wherever signs are present.

---

## Part A — Alternating Series (5 pts each)

### A1 (5) $\;\sum_{n\ge1}\frac{(-1)^{n+1}}{2n+1}$

$b_n = \frac{1}{2n+1}$.

- **Decreasing:** $2n+3>2n+1$ so $b_{n+1}<b_n$ ✓
- **$\to0$:** $\frac{1}{2n+1}\to0$ ✓

**Converges** by the Alternating Series Test.

*(Value: $1-\frac\pi4 = 0.2146$ — this is the Leibniz–Gregory series with its first term removed. Verified.)*

*Marking: **2 for each hypothesis explicitly checked**, 1 for the verdict.*

### A2 (5) $\;\sum_{n\ge1}\frac{(-1)^n n}{n^2+1}$

$b_n = \frac{n}{n^2+1}$.

- **$\to0$:** degree of denominator exceeds numerator ✓
- **Decreasing:** let $f(x)=\frac{x}{x^2+1}$; then

$$f'(x) = \frac{(x^2+1)-x(2x)}{(x^2+1)^2} = \frac{1-x^2}{(x^2+1)^2} < 0 \text{ for } x>1 \ \checkmark$$

*(Verified: $f'(2) = -\frac{3}{25}<0$; and $b_1,b_2,b_3 = \frac12,\frac25,\frac{3}{10}$ is decreasing.)*

**Converges.**

*Marking: 2 for $b_n\to0$, **3 for a genuine monotonicity argument.** "It looks decreasing" earns 1. The derivative route is cleanest and worth pointing out.*

### A3 (5) — error bound for $\sum\frac{(-1)^{n+1}}{n^3}$

**(a)** Require $b_{N+1} = \dfrac{1}{(N+1)^3}<10^{-3}$, i.e. $(N+1)^3>1000$, i.e. $N+1>10$:

$$\boxed{N=10}$$

**(b)** Since $S$ lies between consecutive partial sums, $S\in[s_{10},s_{11}]$ — and as the next term $+\frac{1}{11^3}$ is positive, $s_{10}<S<s_{11}$.

*(Verified: $s_{10} = 0.901116476$, true $S = \frac34\zeta(3) = 0.901542677$, error $4.26\times10^{-4}<10^{-3}$ ✓.)*

*Marking: 3 + 2. **Note the bound is honest but loose** — the true error is about $\frac{4}{10}$ of the bound, consistent with the "half the bound" behaviour in Lab 8.*

### A4 (5) $\;\sum_{n\ge1}\frac{(-1)^n n}{2n+1}$

$b_n = \frac{n}{2n+1}\to\frac12 \neq 0$. **Hypothesis (ii) fails**, so the Alternating Series Test does not apply.

**But this is not "no information":** since $a_n = \frac{(-1)^nn}{2n+1}$ does not tend to 0, the **$n$-th Term Test** gives

$$\boxed{\textbf{diverges}}$$

*Marking: 2 for identifying the failed hypothesis, **3 for supplying the correct verdict with the right test.** A student who stopped at "AST does not apply" earns 2 — the question explicitly asked for the verdict.*

> **This is the week's most common structural error**, and it mirrors Week 7's "$L=1$, so it
> diverges": **a test that does not apply is silent, but another test may still speak.**

---

## Part B — Absolute or Conditional? (6 pts each)

*Standard marking: 3 for the test on $\sum|a_n|$, 2 for the follow-up, 1 for the correct classification word.*

### B1 (6) $\;\sum\frac{(-1)^n}{n^{4/3}}$

$\sum\left|a_n\right| = \sum\frac{1}{n^{4/3}}$ is a $p$-series with $p=\frac43>1$: **converges.**

$$\boxed{\textbf{Absolutely convergent}}$$

*The Alternating Series Test is not needed and should not be used — absolute convergence is the stronger statement.*

### B2 (6) $\;\sum\frac{(-1)^n}{\ln(n+1)}$

$\sum\frac{1}{\ln(n+1)}$: since $\ln(n+1)<n$ for $n\ge1$, we have $\frac{1}{\ln(n+1)}>\frac1n$, and $\sum\frac1n$ diverges. **So the absolute series diverges.**

*(Verified: at $n=1000$, $\frac{1}{\ln1001} = 0.1447 \gg 0.001 = \frac1n$.)*

Alternating Series Test: $b_n = \frac{1}{\ln(n+1)}$ is decreasing ✓ (as $\ln$ increases) and $\to0$ ✓.

$$\boxed{\textbf{Conditionally convergent}}$$

### B3 (6) $\;\sum\frac{\cos n}{n^2}$

**The signs are irregular — no alternating structure.** The tool is absolute convergence:

$$\left|\frac{\cos n}{n^2}\right|\le\frac{1}{n^2}$$

and $\sum\frac1{n^2}$ converges, so by **direct comparison** the absolute series converges.

$$\boxed{\textbf{Absolutely convergent}}$$

*Marking: **2 of the 6 for recognising that no alternating test applies** and that absolute convergence is the only available route. This is the question's point.*

### B4 (6) $\;\sum\frac{(-1)^n n}{n^2+1}$

$\sum\frac{n}{n^2+1}$: limit comparison with $\frac1n$ gives $L=1$, and $\sum\frac1n$ diverges. **Absolute series diverges.**

A2 established that the alternating series **converges**. Hence

$$\boxed{\textbf{Conditionally convergent}}$$

**What A2 did not establish:** A2 proved *convergence* only. It said nothing about whether the convergence was absolute — and it is not. **The classification requires the extra test on $\sum|a_n|$.**

*Marking: 4 for the classification, **2 for the comparison with A2**, which the question asked for.*

### B5 (6) $\;\sum_{n\ge2}\frac{(-1)^n}{n\ln n}$

$\sum\frac{1}{n\ln n}$ **diverges** by the Integral Test ($u=\ln x$; Week 7, Lecture 2, Example 2).

Alternating Series Test: $b_n = \frac{1}{n\ln n}$ decreasing ✓, $\to0$ ✓.

$$\boxed{\textbf{Conditionally convergent}}$$

---

## Part C — Ratio and Root (6 pts each)

### C1 (6) $\;\sum\frac{n!}{3^n}$

$$\frac{a_{n+1}}{a_n} = \frac{(n+1)!}{3^{n+1}}\cdot\frac{3^n}{n!} = \frac{n+1}{3}\longrightarrow\infty$$

$L=\infty>1$: **diverges.** *(Verified.)*

*Marking: 4 ratio, 2 verdict. **Factorial beats exponential** — Week 6's hierarchy, now deciding a sum.*

### C2 (6) $\;\sum\frac{(n!)^2}{(2n)!}$

$$\frac{a_{n+1}}{a_n} = \frac{((n+1)!)^2}{(2n+2)!}\cdot\frac{(2n)!}{(n!)^2} = \frac{(n+1)^2}{(2n+2)(2n+1)} = \frac{n+1}{2(2n+1)}\longrightarrow\frac14$$

$L=\frac14<1$: **converges absolutely.** *(Verified.)*

*Marking: **4 for the factorial cancellation**, which is the skill. 2 verdict.*

### C3 (6) $\;\sum\frac{(-3)^n2^n}{n!}$

**Simplify first:** $(-3)^n2^n = (-6)^n$, so the series is $\sum\frac{(-6)^n}{n!}$.

$$\left|\frac{a_{n+1}}{a_n}\right| = \frac{6}{n+1}\longrightarrow 0$$

$L=0<1$: **converges absolutely.** *(Verified.)*

*(Value: $e^{-6}-1$ starting from $n=1$. Verified — though not required.)*

*Marking: 2 for combining the powers, 2 ratio, 2 for stating **absolutely** (the question asked).*

### C4 (6) $\;\sum\left(\frac{n}{n+1}\right)^{n^2}$

**Root Test**, since the term is an $n$-th power:

$$\sqrt[n]{a_n} = \left(\frac{n}{n+1}\right)^{n} = \frac{1}{\left(1+\frac1n\right)^n}\longrightarrow\frac1e < 1$$

**Converges.** *(Verified: the root limit is $e^{-1}$.)*

*Marking: 2 for choosing the Root Test, **2 for the Week 6 limit $\left(1+\frac1n\right)^n\to e$**, 2 verdict.*

### C5 (6) $\;\sum\frac{n^2}{n^3+1}$

**(a)** $\dfrac{a_{n+1}}{a_n} = \dfrac{(n+1)^2}{(n+1)^3+1}\cdot\dfrac{n^3+1}{n^2}\longrightarrow 1$. **$L=1$ — inconclusive.** *(Verified.)*

**(b)** Limit comparison with $\frac1n$:

$$L = \lim\frac{n^2/(n^3+1)}{1/n} = \lim\frac{n^3}{n^3+1} = 1\in(0,\infty)$$

$\sum\frac1n$ diverges, so **the series diverges.**

*Marking: 2 for (a) with "inconclusive" stated, 4 for (b) naming limit comparison. **A student who wrote "$L=1$ so diverges" in (a) and got the right final answer still loses the 2** — the reasoning is exactly the error the question tests.*

---

## Part D — Concept (10 pts each)

### D1 (10) — rearrangement

**(a)** Absolute: $\sum|a_n|$ converges. Conditional: $\sum a_n$ converges but $\sum|a_n|$ does not.

**(b)** $0\le a_n+|a_n|\le2|a_n|$. Since $\sum2|a_n|$ converges, direct comparison (valid — terms non-negative) gives convergence of $\sum(a_n+|a_n|)$. Then $\sum a_n = \sum(a_n+|a_n|)-\sum|a_n|$ is a difference of convergent series. $\blacksquare$

**(c)** Positives: $1+\frac13+\frac15+\cdots$. Comparing with $\frac{1}{2n}$, this is half the harmonic series — **diverges.** Negatives: $-\left(\frac12+\frac14+\cdots\right)$ — likewise **diverges** to $-\infty$.

**So the value $\ln2$ arises from an $\infty-\infty$ resolved by the particular interleaving.** Change the interleaving and you re-resolve it differently.

**(d)** *(Statement as in the lecture.)* **Algorithm:** add positives until the running total exceeds $T$; add negatives until it drops below $T$; repeat.

**Each stage terminates** because the positive terms alone diverge to $+\infty$ (so you must eventually cross above $T$) and the negative terms alone to $-\infty$ (so you must eventually cross below).

**(e)** For an absolutely convergent series the positive and negative parts **each converge**, so there is no $\infty-\infty$ to re-resolve. **Every rearrangement gives the same sum.**

*Marking: 1 + 3 + 3 + 2 + 1. **(c) and (d) carry the weight.** (d)'s termination argument must invoke the divergence of each half — that is exactly the hypothesis "conditionally convergent" being used.*

### D2 (10) — hypotheses and silence

**(a)** $\dfrac{n}{n+1}\to1$ and $\dfrac{n^2}{(n+1)^2}\to1$. **Both give $L=1$**, yet $\sum\frac1n$ diverges and $\sum\frac1{n^2}$ converges. **So $L=1$ carries no information whatsoever.** *(Verified.)*

**(b)** For $a_n = n^{-p}$,

$$\frac{a_{n+1}}{a_n} = \left(\frac{n}{n+1}\right)^{p}\longrightarrow1 \quad\text{for every } p$$

**The Ratio Test cannot see polynomial behaviour at all** — polynomial decay is too slow to register as a geometric ratio. **It is a tool for factorials and exponentials**, where the ratio has a genuine limit away from 1.

**(c)** The student has treated a **silent** test as a **negative** one. $L=1$ means the test has finished without a conclusion; it does not mean divergence. **Another test must be used.**

**(d)** $\sqrt[n]{a_n} = \dfrac{\left(1+\frac1n\right)^n}{e}\to\dfrac ee = 1$ — **inconclusive.** *(Verified.)*

But $a_n\to e^{-1/2} = 0.6065\neq0$ *(verified numerically: $0.6256$, $0.6085$, $0.60655$ at $n=10,10^2,10^4$)*, so the **$n$-th Term Test** gives **divergence** immediately.

*Marking: 2 + 3 + 2 + 3. **(b) must explain *why* polynomial series always give 1**, not merely assert it. In (d), watch for students confusing $\lim a_n$ with $\lim\sqrt[n]{a_n}$ — they are $e^{-1/2}$ and $1$, and only the second is the Root Test.*

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | AST, both hypotheses; error bound |
| B (5 × 6) | 30 | Absolute vs conditional |
| C (5 × 6) | 30 | Ratio and Root, including inconclusive |
| D (2 × 10) | 20 | Rearrangement; the meaning of $L=1$ |
| **Total** | **100** | |

---

## Diagnostic Notes

| Question | Weakness | Bites in |
|---|---|---|
| **A2** | Not proving monotonicity | Midterm 2 |
| **A4 / C5 / D2(c)** | Treating a silent test as a negative one | Week 9, at every endpoint |
| **B4** | Stopping at "converges" without classifying | Week 9 (interval of convergence) |
| **D1(e)** | Not seeing absolute convergence as a *licence* | Week 10 (term-by-term operations) |

**Week 9 applies the Ratio Test to power series**, where it gives the radius of convergence — and where **$L=1$ occurs at exactly the two endpoints**, which must then be settled by hand with Weeks 7–8 tests. **A student who does not understand that $L=1$ is silence will not be able to find an interval of convergence.**

---

*MATH 142 · Week 8 · PS 8 Solutions · Instructor Only*
