# MATH 142 · Calculus II
## Week 8 · Lecture 2 (Tuesday)
### Absolute Convergence, and a Theorem That Should Disturb You

**Date:** Tuesday 16 March 2027 · 11:00–11:50 · Week 8

---

**Reading:** Stewart §11.6 | Apostol Ch. 10 §10.18–10.20

---

## 1. Two Kinds of Convergence

> **Definition.** $\sum a_n$ converges **absolutely** if $\sum|a_n|$ converges.
> It converges **conditionally** if $\sum a_n$ converges but $\sum|a_n|$ does not.

Three examples, which exhaust the possibilities:

| Series | $\sum a_n$ | $\sum\lvert a_n\rvert$ | Verdict |
|---|---|---|---|
| $\sum\dfrac{(-1)^{n+1}}{n^2}$ | converges to $\frac{\pi^2}{12}$ | converges to $\frac{\pi^2}{6}$ | **absolutely convergent** |
| $\sum\dfrac{(-1)^{n+1}}{n}$ | converges to $\ln2$ | **diverges** | **conditionally convergent** |
| $\sum\dfrac{1}{n}$ | diverges | diverges | **divergent** |

*(all verified)*

---

## 2. Absolute Convergence Implies Convergence

> **Theorem.** If $\sum|a_n|$ converges, then $\sum a_n$ converges.

**Proof.** For every $n$,

$$0 \;\le\; a_n+|a_n| \;\le\; 2|a_n|$$

so by **direct comparison** (Week 7), $\sum(a_n+|a_n|)$ converges — note its terms are non-negative, so Week 7's tests apply. Then

$$\sum a_n = \sum\big(a_n+|a_n|\big) - \sum|a_n|$$

is a difference of two convergent series, hence convergent. $\blacksquare$

> **This is why the theorem matters practically.** It lets you apply **every Week 7 test** — all of
> which needed non-negative terms — to a series with arbitrary signs, simply by testing $\sum|a_n|$
> first. **If the absolute series converges, you are done, and you never think about the signs.**

**The converse is false**: $\sum\frac{(-1)^{n+1}}{n}$ converges and $\sum\frac1n$ does not. **That gap is what "conditional" names.**

---

## 3. The Practical Procedure

> **Given a series with mixed signs:**
>
> 1. **Test $\sum|a_n|$ first**, with any Week 7 method.
> 2. If it converges — **done, absolutely convergent.**
> 3. If it diverges — the original may still converge. **Now** try the Alternating Series Test (if applicable).
> 4. If that gives convergence, the series is **conditionally convergent**.

**Step 1 is the efficient move**, because Week 7's tests are stronger and more numerous than Week 8's.

### Example 1

$$\sum_{n=1}^\infty\frac{\sin n}{n^2}$$

The signs are irregular — no alternating structure at all. But

$$\left|\frac{\sin n}{n^2}\right|\le\frac{1}{n^2}$$

and $\sum\frac1{n^2}$ converges, so **the series converges absolutely.**

> **Notice what just happened.** A series whose sign pattern is essentially unpredictable was settled
> by ignoring the signs entirely. **Absolute convergence is the tool for series with no usable
> structure.**

### Example 2

$$\sum_{n=1}^\infty\frac{(-1)^{n+1}}{\sqrt n}$$

$\sum\frac{1}{\sqrt n}$ is a $p$-series with $p=\frac12\le1$: **diverges.** So not absolutely convergent.

Alternating Series Test: $b_n=\frac{1}{\sqrt n}$ is decreasing ✓ and $\to0$ ✓. **Converges conditionally.**

---

## 4. Why "Conditional" Is the Right Word

**A conditionally convergent series converges only because of cancellation**, and its positive and negative parts are *separately* infinite.

Write $P$ for the sum of the positive terms and $N$ for the sum of the negative ones. For the alternating harmonic series:

$$P = 1+\frac13+\frac15+\cdots = \infty, \qquad N = -\left(\frac12+\frac14+\frac16+\cdots\right) = -\infty$$

**Both halves diverge.** The finite answer $\ln2$ comes from the *interleaving* — from $\infty-\infty$ being resolved by the particular order in which the terms arrive.

> **And an $\infty-\infty$ resolved by an ordering can be re-resolved by a different ordering.** That
> observation is the whole of the next section.

---

## 5. The Riemann Rearrangement Theorem

> **Theorem (Riemann).** Let $\sum a_n$ converge **conditionally**. Then for any target
> $T\in\mathbb{R}$ — or $T=+\infty$, or $T=-\infty$ — there is a rearrangement of the terms whose sum
> is exactly $T$.

*Riemann proved this in **1853**, in the Habilitationsschrift he presented that December — *Ueber die Darstellbarkeit einer Function durch eine trigonometrische Reihe*. **It was not published until 1866–67, after his death.** Like Oresme's proof from Week 7, one of the subject's decisive arguments sat unread for over a decade.*

**The same terms. Reordered. Any sum you name.**

### The construction, which is simple enough to run

To reach a target $T$:

1. **Add positive terms**, in order, until the running total first exceeds $T$.
2. **Add negative terms**, in order, until it first drops below $T$.
3. **Repeat forever.**

**Why it works:** the positives alone diverge to $+\infty$, so step 1 always terminates; the negatives alone diverge to $-\infty$, so step 2 always does too. And every time you cross $T$, you overshoot by **at most the size of the last term used** — which tends to 0. **So the partial sums are trapped in a shrinking interval around $T$.**

### It really works

Applying this to the alternating harmonic series, with 300,000 terms:

| target | achieved |
|---|---|
| $\ln 2 = 0.693147$ | $0.693146$ |
| $1$ | $0.999999871$ |
| $\pi$ | $3.14155$ |
| $0$ | $-1.04\times10^{-6}$ |
| $-2$ | $-1.99978$ |

*(Measured — Lab 8 makes you reproduce this.)*

**And in their natural order, those very same terms sum to $\ln2$.**

### What has actually gone wrong

**Nothing.** Addition of finitely many numbers is commutative, and that fact is not in dispute.

**But an infinite series is not an addition.** It is

$$\lim_{N\to\infty}s_N$$

and **rearranging the terms produces a different sequence $\{s_N\}$** — one that may perfectly well have a different limit, or none.

> **Every strange fact about series comes back to the definition.** The symbol $\sum$ looks like
> addition and inherits none of its guarantees automatically. **The guarantees have to be earned, and
> absolute convergence is what earns them.**

### The good news

> **An absolutely convergent series may be rearranged freely**, and every rearrangement has the same
> sum.

**This is the practical payoff of the whole lecture.** When you want to reorder terms, split a series in two, multiply two series together, or interchange a sum with an integral or another sum — **absolute convergence is the hypothesis that licenses it.** Conditional convergence licenses none of it.

**In Week 10 you will differentiate and integrate power series term by term.** That is legitimate because power series converge absolutely inside their radius of convergence — a fact established next week.

---

## 6. What To Take From This Lecture

1. **Absolute:** $\sum|a_n|$ converges. **Conditional:** $\sum a_n$ converges but $\sum|a_n|$ does not.
2. **Absolute convergence implies convergence**, by comparison on $a_n+|a_n|$.
3. **Test $\sum|a_n|$ first** — it lets you use all of Week 7 and ignore the signs.
4. **Conditional convergence means $P=+\infty$ and $N=-\infty$**, resolved by the ordering.
5. **Riemann: a conditionally convergent series can be rearranged to any sum whatsoever.**
6. **Absolute convergence is what licenses rearrangement**, and every other manipulation you will want to perform.

---

*Next: Wednesday — The Ratio and Root Tests*
