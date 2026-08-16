# MATH 142 · Calculus II
## Week 8 · Lecture 1 (Monday)
### Alternating Series

**Date:** Monday 8 March 2027 · 11:00–11:50 · Week 8

---

**Reading:** Stewart §11.5 | Apostol Ch. 10 §10.17
**Quiz 08** — this Monday, **covers Week 7** (series, Integral Test, comparison)

---

## 1. The Series That Should Not Converge

$$\sum_{n=1}^\infty\frac{(-1)^{n+1}}{n} = 1-\frac12+\frac13-\frac14+\cdots$$

**The absolute values give the harmonic series, which diverges.** The terms do not shrink fast enough for any Week 7 test to save it.

**And yet it converges**, to $\ln2 = 0.693147180559945\ldots$ *(verified)*.

**The convergence is caused entirely by cancellation.** Look at the partial sums:

$$s_1 = 1,\quad s_2 = 0.5,\quad s_3 = 0.8\overline{3},\quad s_4 = 0.58\overline{3},\quad s_5 = 0.78\overline{3},\ \ldots$$

They **oscillate**, and the oscillations **shrink**. The odd ones decrease, the even ones increase, and the two sequences squeeze together on the limit.

**That picture is the whole theorem.**

---

## 2. The Alternating Series Test

> **Alternating Series Test (Leibniz).** Consider $\displaystyle\sum_{n=1}^\infty(-1)^{n+1}b_n$ with $b_n>0$. If
>
> **(i)** $b_n$ is **decreasing** ($b_{n+1}\le b_n$, at least eventually), **and**
> **(ii)** $b_n\to0$,
>
> then the series **converges**.

### Both hypotheses are required

**(ii) alone is not enough**, and here is a clean counterexample. Take

$$b_n = \begin{cases}\dfrac1n & n \text{ odd}\\[6pt] \dfrac{1}{n^2} & n \text{ even}\end{cases}$$

Then $b_n\to0$ ✓ — but $b_n$ is **not decreasing**: $b_2 = 0.25 < b_3 = 0.333\ldots$

The alternating series $\sum(-1)^{n+1}b_n$ splits into

$$\underbrace{\left(1+\frac13+\frac15+\cdots\right)}_{\text{odd harmonic — \textbf{diverges}}} \;-\; \underbrace{\left(\frac1{2^2}+\frac1{4^2}+\cdots\right)}_{=\ \frac{\pi^2}{24}\ \text{— converges}}$$

**so it diverges to $+\infty$.**

*(Verified: the partial sums are $1.42$ at $N=10$, $2.53$ at $N=10^2$, $4.83$ at $N=10^4$, $7.13$ at $N=10^6$ — growing steadily, exactly as the odd harmonic series does.)*

**Monotonicity is doing real work, not decoration.**

> **Check (i) explicitly.** Usually by showing $b_{n+1}\le b_n$ directly, or by finding $f'(x)<0$ for
> the corresponding function. **Students routinely verify only $b_n\to0$**, which is checking half a
> theorem.

### Why it works

The even partial sums increase, the odd ones decrease, every even one is below every odd one, and their difference $b_{N+1}\to0$. **Two monotone bounded sequences squeezing together** — Week 6's Monotone Convergence Theorem, used twice. $\blacksquare$

---

## 3. The Error Bound — The Best in the Course

The proof gives something extra, and it is remarkably clean.

> **Alternating Series Estimation.** Under the same hypotheses, with $S$ the sum and $s_N$ the $N$-th
> partial sum:
>
> $$\boxed{\left|S - s_N\right| \;\le\; b_{N+1}}$$
>
> and moreover $S$ lies **between** $s_N$ and $s_{N+1}$.

**The error is at most the first omitted term.**

*(Verified for $\sum\frac{(-1)^{n+1}}{n}$:)*

| $N$ | $s_N$ | $\lvert R_N\rvert$ | $b_{N+1}=\frac{1}{N+1}$ | holds |
|---:|---|---|---|---|
| $1$ | $1.0$ | $0.30685$ | $0.5$ | ✓ |
| $2$ | $0.5$ | $0.19315$ | $0.33333$ | ✓ |
| $5$ | $0.78333$ | $0.09019$ | $0.16667$ | ✓ |
| $10$ | $0.64563$ | $0.04751$ | $0.09091$ | ✓ |
| $20$ | $0.66877$ | $0.02438$ | $0.04762$ | ✓ |

**Compare with Week 7.** There, an error bound required the Integral Test, its three hypotheses, and an improper integral. **Here you read the bound off the next term.**

> **This bound is why Week 10 works.** Taylor series with alternating terms — $\sin$, $\cos$,
> $\arctan$, $\ln(1+x)$ — come with instant, rigorous error control, and that is exactly what a
> numerical library needs.

### The bound is honest, not tight

Notice the bound is roughly **twice** the true error in the table above. That is typical: **the true error is usually about half the first omitted term**, because $S$ sits near the middle of the bracket $[s_N,s_{N+1}]$.

**Averaging consecutive partial sums exploits this** — the same trick as Week 7's averaged remainder bounds, and Lab 8 measures it.

---

## 4. Worked Examples

### Example 1 — the alternating harmonic series

$b_n = \frac1n$: decreasing ✓, tends to 0 ✓. **Converges**, to $\ln2$.

### Example 2

$$\sum_{n=1}^\infty\frac{(-1)^{n+1}}{n^2} = \frac{\pi^2}{12} = 0.822467\ldots$$

*(Verified.)* $b_n=\frac{1}{n^2}$ is decreasing and tends to 0 ✓.

**Note this one also converges absolutely** ($\sum\frac1{n^2}$ converges) — the Alternating Series Test was not needed. That distinction is tomorrow's subject.

### Example 3 — the Leibniz–Gregory series for $\pi$

$$\sum_{n=0}^\infty\frac{(-1)^n}{2n+1} = 1-\frac13+\frac15-\frac17+\cdots = \frac\pi4$$

*(Verified.)*

**A formula for $\pi$ from the odd numbers alone.** But the error bound tells you what it costs: to get $|R_N|\le10^{-6}$ you need $b_{N+1} = \frac{1}{2N+3}\le10^{-6}$, i.e. about **500,000 terms** for six decimal places.

> **Compare Lab 1's Wallis product** ($8\times10^9$ factors for ten digits) and **Lab 6's Babylonian
> iteration** (48 digits in six steps). **Beautiful formulas for $\pi$ are common; fast ones are not.**

### Example 4 — the test does not apply

$$\sum_{n=1}^\infty\frac{(-1)^{n+1}n}{n+1}$$

Here $b_n = \frac{n}{n+1}\to1\neq0$. **Hypothesis (ii) fails.**

**But do not say "the test fails, so we learn nothing."** The terms do not tend to zero, so by the **$n$-th Term Test** (Week 7) the series **diverges** outright.

> **When the Alternating Series Test fails because $b_n\not\to0$, you already have your answer** —
> from a different test. Recognising that saves time and is worth marks.

---

## 5. Where the Signs Matter

Two series with identical magnitudes:

$$\sum\frac{1}{n} = \infty \qquad\qquad \sum\frac{(-1)^{n+1}}{n} = \ln2$$

**Same terms in absolute value. Completely different fates.**

This is the first time in the course that the *arrangement of signs*, rather than the size of the terms, has decided convergence. **Tomorrow shows how much stranger that gets** — for such a series, even the *order* of the terms decides the answer.

---

## 6. What To Take From This Lecture

1. **Alternating Series Test:** $b_n$ **decreasing** and $b_n\to0$. **Two hypotheses — check both.**
2. **It is Monotone Convergence applied twice**, to the even and odd partial sums.
3. **$|R_N|\le b_{N+1}$** — the error is at most the first omitted term. **Free, and the best bound in the course.**
4. **$S$ lies between $s_N$ and $s_{N+1}$**, so the true error is typically about half the bound.
5. **If $b_n\not\to0$, use the $n$-th Term Test** and conclude divergence.
6. **Cancellation, not decay, is what makes these converge** — and that has consequences.

---

*Next: Tuesday — Absolute Convergence, and a Theorem That Should Disturb You*
