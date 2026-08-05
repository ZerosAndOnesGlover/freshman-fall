# MATH 142 · Calculus II
## Week 7 · Overview
### Series: Geometric, $p$-Series, Integral and Comparison Tests

---

**Topic:** infinite sums, and the first machinery for deciding whether they mean anything
**Reading:** Stewart §11.2–11.4 | Apostol Ch. 10 §10.10–10.14
**Assessment this week:** PS 7, Lab 7, **Quiz 07** *(Monday — covers Week 6)*

---

## What a Series Is

$$\sum_{n=1}^{\infty}a_n \;:=\; \lim_{N\to\infty}s_N, \qquad\text{where}\qquad s_N = a_1+a_2+\cdots+a_N$$

**A series is nothing but a sequence of partial sums.** Everything from Week 6 applies unchanged — this is a definition, not a new object.

**Adding infinitely many things is not an operation.** You cannot perform it. What you *can* do is add finitely many and take a limit, and that is exactly what the definition says. **Every strange fact about series traces back to this**: the sum is a limit, and limits do not always behave like finite sums.

---

## Two Questions, and Only One Is Usually Answerable

| Question | Status |
|---|---|
| **Does $\sum a_n$ converge?** | Answerable — this week and next build the tools |
| **What does it converge to?** | **Almost never answerable** |

**This asymmetry is the whole shape of the second half.** We can prove $\sum\frac{1}{n^3}$ converges in one line, and nobody knows a closed form for its value. *(It has a name, $\zeta(3)$, and that name is all anyone has.)*

**You met exactly this in Week 3.** Comparison decided whether $\int_1^\infty f$ was finite without evaluating it. This week does the same for sums — and the **Integral Test** makes the parallel a theorem rather than an analogy.

---

## The Three Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Monday | Series, Geometric, Telescoping | The two series we can actually sum |
| **Lecture 2** | Tuesday | The Integral Test and $p$-Series | Week 3, translated — plus error bounds |
| **Lecture 3** | Wednesday | Comparison Tests | Deciding by resemblance |

---

## The Two Series You Can Sum

**Almost every series is unsummable in closed form.** There are two families that are not, and they carry an enormous amount of weight:

**Geometric:**

$$\sum_{n=0}^{\infty}ar^n = \frac{a}{1-r}\qquad (|r|<1)$$

**Telescoping:** where consecutive terms cancel, e.g.

$$\sum_{n=1}^{\infty}\frac{1}{n(n+1)} = \sum_{n=1}^\infty\left(\frac1n-\frac{1}{n+1}\right) = 1$$

*(both verified)*

**The second uses partial fractions from Week 2** — and the cancellation is the discrete cousin of Week 3's $\ln\frac{T-1}{T+1}$, where two divergent pieces combined into a finite limit.

---

## The Harmonic Series

$$\sum_{n=1}^{\infty}\frac1n \;=\; 1+\frac12+\frac13+\frac14+\cdots \;=\;\boldsymbol{\infty}$$

**The terms go to zero and the sum is infinite.** This is the single most important example in the subject, and it is the reason a convergence test is needed at all — you cannot tell by looking.

**And it diverges with almost unbelievable slowness.** Since $H_n\approx\ln n+\gamma$:

| to reach a sum of | you need about |
|---|---|
| $10$ | $12{,}367$ terms |
| $20$ | $2.7\times10^{8}$ terms |
| $50$ | $2.9\times10^{21}$ terms |
| $100$ | $1.5\times10^{43}$ terms |

*(Computed — Lab 7 reproduces these.)*

**No computation will ever see this series diverge.** That is Week 3's Lab lesson again, in a new costume: *a finite computation cannot establish a statement about a limit.*

---

## Convergence Is Not the Same as Being Computable

Even when a series converges, summing it may be hopeless. The **Basel series**

$$\sum_{n=1}^{\infty}\frac{1}{n^2} = \frac{\pi^2}{6} = 1.6449340668\ldots$$

converges — but its partial sums have error almost exactly $\frac1N$, so **ten correct digits would need $10^{10}$ terms.** *(Measured: $N\times\text{error}\to1$.)*

**Lab 7's best result is that this can be fixed almost for free.** The Integral Test provides *two-sided* bounds on the remainder, and simply **averaging them** turns an $O(1/N)$ method into an $O(1/N^3)$ one:

| $N$ | raw error | averaged |
|---|---|---|
| $10$ | $9.5\times10^{-2}$ | $2.9\times10^{-4}$ |
| $10^3$ | $1.0\times10^{-3}$ | $3.3\times10^{-10}$ |

*(Measured.)* **Six orders of magnitude, for one extra line of arithmetic.**

---

## What Will Be Hard

**The $n$-th Term Test only ever proves divergence.** If $a_n\not\to0$, the series diverges. **If $a_n\to0$, it tells you nothing** — the harmonic series is the standing counterexample. Every year, students write "the terms go to zero, so it converges." That is the most common error in the subject.

**Every test has hypotheses.** Comparison needs non-negative terms. The Integral Test needs $f$ positive, continuous *and decreasing*. **Week 6's PS C5 was the warning shot**: a test applied without its hypotheses gives a confident wrong answer.

**Getting an answer is not the goal; justifying it is.** From this week, a correct verdict with no valid argument is worth almost nothing.

---

## This Week's Work

1. **Quiz 07** — Monday, 15 minutes, **covers Week 6** (sequences, monotone convergence, recursion)
2. **PS 7** — released Wednesday, due Wednesday of Week 8
3. **Lab 7** — how slowly the harmonic series diverges, and how to make a convergent series usable

---

*Next: Monday — Series, Geometric and Telescoping*
