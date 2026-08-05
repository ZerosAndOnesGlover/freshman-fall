# MATH 142 · Calculus II
## Week 8 · Overview
### Alternating Series; Absolute Convergence; Ratio and Root Tests

---

**Topic:** what the signs are doing — and the strangest theorem in the course
**Reading:** Stewart §11.5–11.7 | Apostol Ch. 10 §10.17–10.21
**Assessment this week:** PS 8, Lab 8, **Quiz 08** *(Monday — covers Week 7)*

---

## Removing the Non-Negativity Hypothesis

Every test in Week 7 required $a_n\ge0$. That was not a technicality — the partial sums had to be **increasing** for monotone convergence to apply.

**This week the terms may change sign**, and the situation changes completely.

$$1-\frac12+\frac13-\frac14+\frac15-\cdots \;=\;\ln 2$$

**converges.** Take the same terms with all signs made positive and you get the harmonic series, which **diverges.**

> **So the signs are not a detail. They are doing the work.** The series converges because of
> cancellation, not because the terms shrink fast enough — and a series that converges only for that
> reason turns out to be a far stranger object than one that converges outright.

---

## The Three Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Monday | Alternating Series | A test with **two** hypotheses, and the best error bound in the course |
| **Lecture 2** | Tuesday | Absolute vs Conditional Convergence | Two kinds of convergence, and why the difference matters |
| **Lecture 3** | Wednesday | The Ratio and Root Tests | Geometric comparison, automated |

---

## The Best Error Bound You Will Meet

For an alternating series satisfying the test's hypotheses:

$$\left|R_N\right| \;\le\; b_{N+1}$$

**The error is no bigger than the first term you left out.** No integral, no estimation, no work — you read the bound straight off the next term.

*(Verified for the alternating harmonic series at $N=1,2,5,10,20$: the bound holds every time.)*

Compare Week 7, where getting an error bound required the Integral Test and its hypotheses. **This one is free**, and Week 10 will lean on it heavily for Taylor series.

---

## The Theorem That Should Disturb You

> **Riemann Rearrangement Theorem.** If $\sum a_n$ converges **conditionally**, then for **any** real
> number $T$ — or $+\infty$, or $-\infty$ — the terms can be rearranged so that the new series
> converges to $T$.

**The same terms. A different order. Any sum you like.**

Lab 8 makes you do it. Rearranging the alternating harmonic series with a simple greedy rule gives, after 300,000 terms:

| target | achieved |
|---|---|
| $1$ | $0.999999871$ |
| $\pi$ | $3.14155$ |
| $0$ | $-1.0\times10^{-6}$ |
| $-2$ | $-1.99978$ |

*(Measured.)* **And in their natural order those very same terms sum to $\ln2 = 0.693147$.**

> **Addition is commutative. Infinite addition is not** — because infinite addition is not addition.
> It is a limit, and rearranging the terms changes the sequence of partial sums into a different
> sequence, which may have a different limit. **Every strange fact about series comes back to the
> definition.**
>
> **Absolutely convergent series are immune.** That is the practical reason the distinction matters.

---

## Two Tests That Do Most of the Work

**Ratio Test:** compute $L=\lim\left|\dfrac{a_{n+1}}{a_n}\right|$. Then $L<1$ converges, $L>1$ diverges, $L=1$ **tells you nothing.**

**Root Test:** the same with $L=\lim|a_n|^{1/n}$.

**Both are comparisons with a geometric series** — they ask "by what factor do the terms shrink?" and compare that factor with 1. **You have met this idea three times already:** Week 3's $p$-test, Week 6's fixed-point criterion $|g'(L)|<1$, and Week 7's geometric series.

### The $L=1$ case is not a formality

$$\sum\frac1n \quad\text{and}\quad \sum\frac{1}{n^2}$$

**both have ratio limit exactly 1** *(verified)* — and one diverges while the other converges. **When $L=1$ the test has genuinely finished and told you nothing**, and you must use Week 7's methods instead.

**This matters enormously in Week 9**, where the Ratio Test finds the radius of convergence of a power series but is always inconclusive at the endpoints — which is precisely why endpoints have to be checked separately.

---

## What Will Be Hard

**The Alternating Series Test has two hypotheses**, and $b_n\to0$ is only one of them. **$b_n$ must also be decreasing**, and students routinely skip checking it.

**"Diverges" from the Ratio Test is a real conclusion; "$L=1$" is not.** Writing "the Ratio Test gives 1, so it diverges" is a serious error.

**Conditional convergence is a fragile property.** You may not rearrange, you may not regroup freely, and you may not manipulate such a series as if it were a finite sum. **Absolute convergence is what licenses all the algebra you want to do.**

---

## This Week's Work

1. **Quiz 08** — Monday, 15 minutes, **covers Week 7** (series, Integral Test, comparison)
2. **PS 8** — released Wednesday, due Wednesday of Week 9
3. **Lab 8** — the Leibniz error bound, and rearranging a series to sum to $\pi$

---

## Looking Ahead

**Week 9 puts a variable into a series:**

$$\sum_{n=0}^\infty c_n x^n$$

Such a thing converges for some $x$ and not others, and the Ratio Test from this week is exactly the tool that finds the boundary. **Then Week 10 shows that nearly every function you know is one of these** — which is how a computer evaluates $\sin$, $\exp$ and $\log$, and how $\int e^{-x^2}dx$ finally becomes computable.

---

*Next: Monday — Alternating Series*
