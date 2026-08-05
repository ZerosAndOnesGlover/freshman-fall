# MATH 142 · Calculus II
## Week 8 · Reference Sheet
### Alternating Series; Absolute Convergence; Ratio and Root Tests

---

## Alternating Series Test (Leibniz)

For $\displaystyle\sum(-1)^{n+1}b_n$ with $b_n>0$:

> **(i)** $b_n$ **decreasing** (eventually) **and** **(ii)** $b_n\to0$ $\implies$ **converges**

**Both hypotheses are required.** With $b_n=\frac1n$ ($n$ odd), $\frac1{n^2}$ ($n$ even), the terms tend to 0 but are not monotone, and the series **diverges** — it splits into the divergent odd harmonic minus a convergent piece. *(Verified: partial sums $1.42,\ 2.53,\ 4.83,\ 7.13$ at $N=10,10^2,10^4,10^6$.)*

**If $b_n\not\to0$, use the $n$-th Term Test** and conclude divergence.

### The error bound — the best in the course

$$\boxed{\left|S-s_N\right|\le b_{N+1}}, \qquad\text{and } S \text{ lies between } s_N \text{ and } s_{N+1}$$

**The error is at most the first omitted term.** Free — no integral, no hypotheses beyond the test's own.

**It is loose by a factor of about 2**: the true error tends to **half** the bound, because $S$ sits near the middle of the bracket. *(Measured for the alternating harmonic series.)*

**Averaging consecutive partial sums exploits this:**

$$\widetilde S_N = \frac{s_N+s_{N+1}}{2} \implies \text{order } 2 \text{ instead of } 1$$

| $N$ | raw error | averaged |
|---|---|---|
| $100$ | $4.98\times10^{-3}$ | $2.45\times10^{-5}$ |
| $400$ | $1.25\times10^{-3}$ | $1.55\times10^{-6}$ |

*(measured — ratio 4 per doubling)*

---

## Standard Alternating Sums

| Series | Value |
|---|---|
| $\sum\frac{(-1)^{n+1}}{n}$ | $\ln2 = 0.693147$ |
| $\sum\frac{(-1)^{n+1}}{n^2}$ | $\frac{\pi^2}{12} = 0.822467$ |
| $\sum_{n\ge0}\frac{(-1)^n}{2n+1}$ | $\frac\pi4$ |
| $\sum\frac{(-1)^{n+1}}{n^3}$ | $\frac34\zeta(3) = 0.901543$ |

*(all verified)*

**The Leibniz–Gregory series for $\pi$ needs ~500,000 terms for six decimals.** Beautiful formulas for $\pi$ are common; fast ones are not.

---

## Absolute and Conditional Convergence

| | |
|---|---|
| **Absolutely convergent** | $\sum\lvert a_n\rvert$ converges |
| **Conditionally convergent** | $\sum a_n$ converges, $\sum\lvert a_n\rvert$ diverges |

> **Absolute convergence $\implies$ convergence.** *(Proof: $0\le a_n+\lvert a_n\rvert\le2\lvert a_n\rvert$, then comparison.)*

**The converse is false** — $\sum\frac{(-1)^{n+1}}{n}$ is the standing example.

### The procedure

1. **Test $\sum\lvert a_n\rvert$ first** — this unlocks every Week 7 test.
2. Converges → **absolutely convergent**, done.
3. Diverges → try the **Alternating Series Test**.
4. Converges → **conditionally convergent**.

**Absolute convergence handles irregular signs**: $\sum\frac{\sin n}{n^2}$ has no alternating structure, but $\left|\frac{\sin n}{n^2}\right|\le\frac1{n^2}$ settles it.

---

## The Riemann Rearrangement Theorem

> **A conditionally convergent series can be rearranged to converge to any $T\in\mathbb R$**, or to $\pm\infty$.

**Why it is possible:** for a conditionally convergent series, the positive terms alone sum to $+\infty$ and the negative terms alone to $-\infty$. The finite value comes from the *ordering* resolving $\infty-\infty$.

**The greedy algorithm:** add positives until you exceed $T$; add negatives until you drop below; repeat. Each stage terminates (each half diverges), and the overshoot is at most the last term used, which $\to0$.

**Measured on the alternating harmonic series, 300,000 terms:**

| target | achieved |
|---|---|
| $1$ | $0.999999871$ |
| $\pi$ | $3.14155$ |
| $0$ | $-1.04\times10^{-6}$ |
| $-2$ | $-1.99978$ |

**In natural order those same terms give $\ln2$.**

> **A series is a limit of partial sums, not an addition.** Reordering produces a different sequence
> of partial sums, which may have a different limit. **Absolutely convergent series are immune** —
> every rearrangement gives the same sum — and that is what licenses term-by-term manipulation in
> Week 10.

*Riemann proved this in 1853; it was published only in 1866–67, after his death.*

---

## The Ratio Test

$$L=\lim_{n\to\infty}\left|\frac{a_{n+1}}{a_n}\right|$$

| $L$ | Conclusion |
|---|---|
| $<1$ | **converges absolutely** |
| $>1$ or $\infty$ | **diverges** |
| $=1$ | **no conclusion** |

**A geometric comparison.** $L>1$ gives divergence via the $n$-th Term Test, so it is a real conclusion.

## The Root Test

$$L = \lim_{n\to\infty}\sqrt[n]{\lvert a_n\rvert}$$

**Same trichotomy.** Prefer it when the whole term is an $n$-th power.

> **$n$-th powers → Root. Factorials → Ratio.**
> They fail together, and **neither can see a $p$-series** — every $p$-series gives $L=1$.

### Worked limits

| Series | test | $L$ | verdict |
|---|---|---|---|
| $\frac{n^2}{2^n}$ | ratio | $\frac12$ | converges |
| $\frac{(-3)^n}{n!}$ | ratio | $0$ | absolutely |
| $\frac{n!}{2^nn^2}$ | ratio | $\infty$ | diverges |
| $\frac{(2n)!}{(n!)^2}$ | ratio | $4$ | diverges |
| $\frac{(n!)^2}{(2n)!}$ | ratio | $\frac14$ | converges |
| $\frac{n^n}{n!}$ | ratio | $e$ | diverges |
| $\frac{n!}{n^n}$ | ratio | $\frac1e$ | **converges** |
| $\left(\frac{n}{2n+1}\right)^n$ | root | $\frac12$ | converges |
| $\frac{1}{(\ln n)^n}$ | root | $0$ | converges |
| $\frac1{n^p}$ | either | $1$ | **inconclusive** |

*(all verified)*

### ⚠ $L=1$ is silence, not divergence

$\sum\frac1n$ and $\sum\frac1{n^2}$ **both give $L=1$** and have opposite fates.

**An instructive failure:** for $\sum\frac{(1+1/n)^{n^2}}{e^n}$ the Root Test gives $L=1$ — but $a_n\to e^{-1/2}\neq0$, so the **$n$-th Term Test** gives divergence at once. *(Verified.)*

*Do not confuse $\lim a_n$ with $\lim\sqrt[n]{a_n}$: here they are $e^{-1/2}$ and $1$.*

---

## The Complete Decision Procedure

| Step | Check | Action |
|---|---|---|
| 1 | $a_n\to0$? | **No** → diverges, done |
| 2 | geometric / telescoping? | sum exactly |
| 3 | $p$-series? | $p>1$ converges |
| 4 | factorials / $n$-th powers? | Ratio / Root |
| 5 | positive, rational-ish? | limit comparison |
| 6 | positive, decreasing, integrable? | Integral Test **+ error bound** |
| 7 | mixed signs? | test $\sum\lvert a_n\rvert$ first, then Alternating |

**Step 1 costs five seconds and finishes many problems.**

---

*MATH 142 · Week 8 · Reference Sheet*
