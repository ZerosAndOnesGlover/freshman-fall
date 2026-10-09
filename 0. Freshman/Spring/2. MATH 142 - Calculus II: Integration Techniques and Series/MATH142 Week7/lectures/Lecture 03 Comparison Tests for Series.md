# MATH 142 · Calculus II
## Week 7 · Lecture 3 (Friday)
### Comparison Tests for Series

*“In plausible reasoning the principal thing is to distinguish... a more reasonable guess from a less reasonable guess.”* — George Pólya, *Induction and Analogy in Mathematics* (1954)

**Date:** Friday 12 March 2027 · 11:00–11:50 · Week 7

**Coursework:** 📝 **PS 6** due today 17:00 · 📝 **PS 7** released today 12:00, due Fri 19 Mar 17:00 · 📊 **Quiz 8** Mon 15 Mar 11:00–11:15 · 🔬 **Lab 7** Wed 17 Mar 15:00–16:50

---

**Reading:** Stewart §11.4 | Apostol Ch. 10 §10.13–10.14

---

## 1. Deciding by Resemblance

Most series are neither geometric nor telescoping, and their integrals are no easier than the sums. **Comparison decides them by resemblance to something known.**

**This is Week 3, Lecture 3 with the word "integral" replaced by "series."** The theorems are the same, the strategy is the same, and the errors are the same.

> **Direct Comparison Test.** Suppose $0\le a_n\le b_n$ for all large $n$.
> - If $\sum b_n$ **converges**, so does $\sum a_n$.
> - If $\sum a_n$ **diverges**, so does $\sum b_n$.

**A smaller non-negative series cannot sum to more than a bigger one.**

- **To prove convergence, bound above by a convergent series.**
- **To prove divergence, bound below by a divergent series.**

**Why it works:** the partial sums of $\sum a_n$ increase (terms are non-negative) and are bounded above by $\sum b_n$. **Monotone convergence** — Week 6 — does the rest. *(Every positive-term test in this course is that theorem wearing a different hat.)*

### The two failure modes

**(a) Non-negativity is a hypothesis.** If terms can be negative the partial sums need not increase and the argument collapses. **Week 8 handles sign-changing series.**

**(b) The inequality must point the useful way.** $\frac{1}{n^2}\le\frac1n$ is true, and $\sum\frac1n$ diverges — **which tells you nothing** about $\sum\frac1{n^2}$. Bounding above by a divergent series, or below by a convergent one, is wasted work.

---

## 2. The Benchmarks

Comparison needs a stock of known series. **There are essentially three.**

| Family | Converges when |
|---|---|
| $\displaystyle\sum\frac{1}{n^p}$ | $p>1$ |
| $\displaystyle\sum ar^n$ | $\lvert r\rvert<1$ |
| $\displaystyle\sum\frac{1}{n(\ln n)^p}$ | $p>1$ |

**Nearly every comparison in this course is against one of these**, and the third only for the borderline cases where powers fail — the pair from Lab 3.

---

## 3. Direct Comparison — Examples

### Example 1

$$\sum_{n=1}^\infty\frac{1}{n^2+1}$$

For all $n$: $\;0<\frac{1}{n^2+1}<\frac{1}{n^2}$, and $\sum\frac1{n^2}$ converges ($p=2$). **Converges**, with sum less than $\frac{\pi^2}{6}$.

*(Corroborated: the partial sums settle at $1.07667$, comfortably below $1.64493$.)*

### Example 2

$$\sum_{n=1}^\infty\frac{1}{2^n+1} < \sum_{n=1}^\infty\frac{1}{2^n} = 1$$

**Converges.** *(Corroborated: the sum is $0.76450$, and it has fully settled by $N=100$ — exponential decay.)*

### Example 3 — proving divergence

$$\sum_{n=1}^\infty\frac{1}{\sqrt{n^2+1}}$$

For $n\ge1$: $\sqrt{n^2+1}\le\sqrt{2n^2}=n\sqrt2$, so

$$\frac{1}{\sqrt{n^2+1}} \ge \frac{1}{n\sqrt2}$$

and $\sum\frac{1}{n\sqrt2}$ is a constant times the harmonic series — **divergent**. So ours **diverges.**

*(Corroborated: partial sums $4.81,\ 9.41,\ 14.01$ at $N=10^2,10^4,10^6$ — increments of about $4.6=\ln100$, exactly the logarithmic growth of the harmonic series.)*

### Example 4 — where the Integral Test could not go

$$\sum_{n=1}^\infty\frac{\sin^2n}{n^2}$$

Yesterday the Integral Test **failed its hypotheses** here — $\frac{\sin^2x}{x^2}$ is not decreasing. **Comparison does not care about monotonicity:**

$$0\le\frac{\sin^2n}{n^2}\le\frac{1}{n^2}$$

since $\sin^2\le1$. **Converges.**

*(Corroborated: the partial sums approach $1.0708$, below $\frac{\pi^2}{6}=1.6449$ ✓.)*

**Remarkably, this one has a closed form.** Using $\sin^2n = \frac{1-\cos2n}{2}$ and the Fourier expansion $\sum\frac{\cos nx}{n^2} = \frac{\pi^2}{6}-\frac{\pi x}{2}+\frac{x^2}{4}$ at $x=2$:

$$\sum_{n=1}^\infty\frac{\sin^2n}{n^2} = \frac{\pi-1}{2} = 1.0707963268\ldots$$

*(Verified to 13 digits.)*

**But notice: comparison told us it converges without any of that**, in one line. **The value was a bonus, and an unusual one.**

---

## 4. The Limit Comparison Test

Direct comparison often needs fiddly inequalities. **Limit comparison removes them.**

> **Limit Comparison Test.** If $a_n,b_n>0$ and $\displaystyle L=\lim_{n\to\infty}\frac{a_n}{b_n}$ exists with $0<L<\infty$,
> then $\sum a_n$ and $\sum b_n$ **both converge or both diverge.**

**Two positive series whose ratio settles to a finite nonzero number share a fate.**

### The strategy

> **Keep the dominant term in the numerator and in the denominator; discard everything else; compare
> with what remains.**

This is verbatim Week 3's strategy.

### Example 5

$$\sum_{n=1}^\infty\frac{n+1}{n^3+2}$$

For large $n$ this behaves like $\frac{n}{n^3}=\frac1{n^2}$. With $b_n=\frac1{n^2}$:

$$L = \lim_{n\to\infty}\frac{(n+1)/(n^3+2)}{1/n^2} = \lim_{n\to\infty}\frac{n^3+n^2}{n^3+2} = 1$$

$0<L<\infty$ and $\sum\frac1{n^2}$ converges, so ours **converges.**

*(Corroborated: partial sums settle at $1.42471$.)*

### Example 6 — the direct comparison would fight you

$$\sum_{n=2}^\infty\frac{1}{n-1}$$

Direct: $\frac{1}{n-1}>\frac1n$, and $\sum\frac1n$ diverges — that works. But limit comparison is immediate:

$$L = \lim\frac{1/(n-1)}{1/n} = \lim\frac{n}{n-1} = 1 \implies \textbf{diverges}$$

*(Corroborated: partial sums $5.18,\ 9.79,\ 14.39$ — the harmonic series shifted by one term.)*

### Example 7

$$\sum_{n=2}^\infty\frac{\ln n}{n^2}$$

The $\ln n$ grows, so this is **not** obviously smaller than $\frac{1}{n^2}$ — indeed it is larger for $n\ge3$. **Direct comparison against $\frac1{n^2}$ fails.**

But $\ln n \ll n^{1/2}$ (Week 6's hierarchy), so for large $n$

$$\frac{\ln n}{n^2} \le \frac{n^{1/2}}{n^2} = \frac{1}{n^{3/2}}$$

and $\sum n^{-3/2}$ converges ($p=\frac32>1$). **Converges.**

*(Corroborated: the partial sums approach $0.93755$. The exact value is $-\zeta'(2) = 0.937548254316$.)*

> **The move — trading a logarithm for a small power of $n$ — is worth remembering.** Any $\ln n$ is
> eventually beaten by $n^\varepsilon$ for every $\varepsilon>0$, so a logarithm never changes
> convergence for a $p$-series with $p>1$. It only matters at the boundary $p=1$, which is why
> $\sum\frac{1}{n\ln n}$ is delicate and $\sum\frac{\ln n}{n^2}$ is not.

---

## 5. A Warning About Numerical Libraries

**Two of the examples above expose a real failure in a widely-used numerical library**, and it is worth seeing.

Asked to sum $\sum\frac{\ln n}{n^2}$ to infinity, `mpmath`'s `nsum` returns

$$0.936715596751$$

**This is wrong.** The true value is $-\zeta'(2) = 0.937548254316$ — an error of $8.3\times10^{-4}$, in a routine whose whole purpose is high precision.

**How it was caught, without knowing the answer:** the partial sum to $N=10^6$ is $0.937533$, which is **larger** than the claimed total.

> **For a series of positive terms, no partial sum can exceed the sum.** That single observation
> falsifies the library's answer in one line, using nothing but the definition.

*(The Integral Test then supplies the correct value: adding the tail bound $\frac{\ln N+1}{N}$ to the partial sum gives $0.937548254323$, agreeing with $-\zeta'(2)$ to 11 digits.)*

The same routine gets $\sum\frac{\sin^2 n}{n^2}$ wrong by $7.8\times10^{-5}$, and the same check exposes it.

> **This is the sixth week running that a machine has produced a confident wrong answer**, and the
> first time it was a *numerical* rather than a symbolic one. **The defence has been the same every
> time: know a property the answer must have, and check it.** Here it was monotonicity of partial
> sums — available to anyone who has read the definition of a series.

---

## 6. Strategy: Which Test?

| The series looks like | Try |
|---|---|
| terms do **not** tend to 0 | **$n$-th Term Test** — diverges, done |
| $ar^n$ | **geometric** |
| terms cancel in pairs | **telescoping** (partial fractions first) |
| $\frac{1}{n^p}$ | **$p$-series** |
| a rational function of $n$ | **limit comparison** with $\frac{1}{n^{\deg\text{den}-\deg\text{num}}}$ |
| $f(n)$ with $f$ positive, decreasing, integrable | **Integral Test** — and get an error bound |
| bounded oscillation over a $p$-series | **direct comparison** |
| contains $\ln n$ away from $p=1$ | **comparison**, trading $\ln n$ for $n^\varepsilon$ |
| contains $\ln n$ **at** $p=1$ | **Integral Test** with $u=\ln x$ |

**Check the $n$-th Term Test first. It costs five seconds and finishes the problem outright surprisingly often.**

---

## 7. What To Take From This Lecture

1. **Comparison is Week 3's argument for sums.** Same theorems, same strategy, same errors.
2. **Direct comparison: the inequality direction is everything.**
3. **Limit comparison: keep the dominant terms, discard the rest.**
4. **Non-negativity is a hypothesis**, not a technicality.
5. **Comparison ignores monotonicity**, so it reaches series the Integral Test cannot.
6. **A partial sum of positive terms cannot exceed the total** — an error check that just caught a numerical library.

---

## Looking Ahead

Everything this week required **non-negative terms**. Next week removes that:

$$1-\frac12+\frac13-\frac14+\cdots$$

**converges** — while the same terms with all signs positive give the harmonic series, which does not.

**Week 8 is about what the signs are doing**, and the answer is stranger than it looks: a series like this one can be **rearranged to sum to any number you choose.**

---

*Next: Week 8, Monday — Alternating Series*
