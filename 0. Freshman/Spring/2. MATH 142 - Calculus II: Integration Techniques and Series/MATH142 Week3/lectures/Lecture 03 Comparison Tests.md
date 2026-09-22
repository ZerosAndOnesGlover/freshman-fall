# MATH 142 · Calculus II
## Week 3 · Lecture 3 (Friday)
### Comparison Tests — Answering Without Evaluating

**Date:** Friday 12 February 2027 · 11:00–11:50 · Week 3

---

**Reading:** Stewart §7.8 | Apostol Ch. 10 §10.9

---

## 1. The Situation

$$\int_1^\infty\frac{dx}{\sqrt{x^3+1}}$$

Does it converge? The methods of Monday and Tuesday say: find the antiderivative, then take a limit.

**There is no elementary antiderivative.** (Week 0's opening fact, still binding.) So the limit method has nothing to take a limit of, and we appear to be stuck.

**But we are not**, because the question asked was not "what is the value?" — it was "does it converge?" And that question can be answered without ever finding the value.

> **This is a new mode of reasoning and it is the most important thing in the second half of the
> course.** Everything in Weeks 7–9 is this argument applied to sums.

---

## 2. The Direct Comparison Test

> **Theorem (Direct Comparison).** Suppose $0\le f(x)\le g(x)$ for all $x\ge a$.
>
> - If $\displaystyle\int_a^\infty g$ **converges**, then $\displaystyle\int_a^\infty f$ converges.
> - If $\displaystyle\int_a^\infty f$ **diverges**, then $\displaystyle\int_a^\infty g$ diverges.

**In words: a smaller non-negative function cannot have more area than a bigger one.**

- **To prove convergence, find a bigger function that converges** — an upper bound.
- **To prove divergence, find a smaller function that diverges** — a lower bound.

### Why it is true

$F(T) = \int_a^T f$ is **increasing** in $T$ (since $f\ge0$) and bounded above by $\int_a^\infty g$. **An increasing function bounded above has a limit** — that is the completeness of the real numbers, and it is the entire content of the theorem.

*(In Week 6 this reappears as the Monotone Convergence Theorem for sequences. Same fact, same proof.)*

### The two hypotheses that matter

**(a) Non-negativity is essential.** If $f$ can be negative, $F(T)$ need not be increasing and the argument collapses. All comparison tests in this course require $f\ge0$ near the limit.

**(b) The inequality must point the right way.** Bounding above by a *divergent* function tells you **nothing**: $\frac{1}{x^2}\le\frac1x$, and $\int_1^\infty\frac{dx}x$ diverges, but $\int_1^\infty\frac{dx}{x^2}$ converges perfectly well. **A useless comparison is the most common error on this topic.**

---

## 3. Examples of Direct Comparison

### Example 1 — the motivating integral

$$\int_1^\infty\frac{dx}{\sqrt{x^3+1}}$$

For $x\ge1$: $x^3+1 > x^3$, so $\sqrt{x^3+1}>x^{3/2}$, so

$$0<\frac{1}{\sqrt{x^3+1}}<\frac{1}{x^{3/2}}$$

And $\int_1^\infty x^{-3/2}dx$ converges by the $p$-test ($p=\tfrac32>1$), with value 2. **Therefore our integral converges**, and its value is less than 2.

*Corroborated numerically: the partial integrals at $T = 10^2,10^4,10^6,10^8$ are $1.6948,\ 1.8748,\ 1.8928,\ 1.8946$ — settling near $1.895$, comfortably below the bound of 2.*

**Note what we did and did not learn.** We proved convergence and got an upper bound. We did **not** get the value, and comparison never will.

### Example 2 — exponential

$$\int_1^\infty e^{-x^2}dx$$

For $x\ge1$ we have $x^2\ge x$, so $e^{-x^2}\le e^{-x}$. And $\int_1^\infty e^{-x}dx = e^{-1}$ converges. **Therefore convergent.**

*Corroborated: the partial integral is $0.13940279$ at $T=10^2$ and unchanged through $T=10^8$ — it has fully converged by $x=100$, as an exponential should.*

**The restriction $x\ge1$ matters:** on $(0,1)$ we have $x^2<x$ and the inequality reverses. Comparison only ever needs to hold **eventually** — near the limit — and you should say where.

### Example 3 — proving divergence

$$\int_1^\infty\frac{2+\sin x}{x}\,dx$$

Since $\sin x\ge-1$, the numerator satisfies $2+\sin x\ge1$, so

$$\frac{2+\sin x}{x}\ \ge\ \frac1x\ >0$$

$\int_1^\infty\frac{dx}x$ **diverges**, so by comparison our integral **diverges**.

*Corroborated: partial integrals $9.83,\ 19.03,\ 28.26,\ 37.43$ at $T=10^2,10^4,10^6,10^8$ — growing by about $9.2$ per factor of 100, which is $2\ln(100)$, exactly what an average numerator of 2 predicts.*

**The oscillation is a distraction.** Bounding it away is the whole move.

### Example 4 — a small denominator perturbation

$$\int_1^\infty\frac{dx}{x+e^{2x}}$$

For $x\ge1$, $x+e^{2x}>e^{2x}$, so the integrand is $<e^{-2x}$, whose integral converges. **Convergent.**

*Corroborated: $0.062461999$ at every $T$ from $10^2$ to $10^8$.*

---

## 4. When Direct Comparison Is Awkward

$$\int_1^\infty\frac{dx}{x^2-\tfrac12}$$

Intuitively this behaves like $\frac{1}{x^2}$ and should converge. But $\frac{1}{x^2-\frac12} > \frac{1}{x^2}$ — the inequality points the **wrong way** for proving convergence, and the obvious comparison fails.

You can rescue it (for $x\ge2$, $x^2-\tfrac12>\tfrac12x^2$, so the integrand is $<\tfrac{2}{x^2}$), but the fiddling is unpleasant. **The limit comparison test removes the need for it.**

---

## 5. The Limit Comparison Test

> **Theorem (Limit Comparison).** Suppose $f,g>0$ for large $x$ and
> $$L = \lim_{x\to\infty}\frac{f(x)}{g(x)}$$
> exists.
>
> - If $0<L<\infty$, then $\displaystyle\int_a^\infty f$ and $\displaystyle\int_a^\infty g$ **both converge or both diverge.**
> - If $L=0$ and $\int g$ converges, then $\int f$ converges.
> - If $L=\infty$ and $\int g$ diverges, then $\int f$ diverges.

**In words: two positive functions with a finite nonzero ratio have the same fate.** A constant factor cannot turn a finite area into an infinite one.

**This is much easier to use**, because you only need to identify what $f$ *behaves like*, and you get to ignore constants entirely.

### The strategy

> **Keep the dominant term in the numerator and the dominant term in the denominator, discard
> everything else, and compare with what remains.**

### Example 5

$$\int_1^\infty\frac{x+1}{x^3+x^2+1}\,dx$$

For large $x$ the integrand behaves like $\frac{x}{x^3}=\frac1{x^2}$. Take $g(x)=\frac1{x^2}$:

$$L = \lim_{x\to\infty}\frac{\frac{x+1}{x^3+x^2+1}}{\frac{1}{x^2}} = \lim_{x\to\infty}\frac{x^3+x^2}{x^3+x^2+1} = 1$$

$0<L=1<\infty$, and $\int_1^\infty\frac{dx}{x^2}$ converges. **Therefore convergent.**

*Corroborated: $0.88039,\ 0.89029,\ 0.89039,\ 0.89039$ — settled by $T=10^6$.*

### Example 6 — where the answer is also computable

$$\int_1^\infty\frac{dx}{x^2+x}$$

Limit comparison with $\frac1{x^2}$ gives $L=1$, so it **converges**.

Here we can also get the value, by **partial fractions** (Week 2):

$$\frac{1}{x^2+x} = \frac{1}{x(x+1)} = \frac1x - \frac1{x+1}$$

$$\int_1^T = \Big[\ln x - \ln(x+1)\Big]_1^T = \ln\frac{T}{T+1} - \ln\frac12 \xrightarrow{T\to\infty} 0 + \ln2 = \boxed{\ln 2}$$

*Verified: the partial integrals are $0.68320,\ 0.69305,\ 0.693146,\ 0.6931472$, converging to $\ln 2 = 0.6931472$.*

**Two techniques meeting.** Partial fractions gave a telescoping difference of logarithms whose limit is finite — even though each logarithm separately diverges. This structure returns in Week 7 as a **telescoping series**.

### Example 7 — the awkward one, rescued

$$\int_1^\infty\frac{dx}{x^2-\tfrac12}$$

Limit comparison with $\frac1{x^2}$:

$$L = \lim_{x\to\infty}\frac{x^2}{x^2-\tfrac12} = 1$$

**Converges.** No inequality manipulation at all — this is why the test exists.

---

## 6. Comparison at a Singularity

Both tests work identically for Type II, comparing behaviour **near the singular point** instead of near infinity.

$$\int_0^1\frac{dx}{\sqrt{x}\,\sqrt{1+x}}$$

Near $x=0$ the factor $\sqrt{1+x}\to1$, so the integrand behaves like $x^{-1/2}$. Limit comparison with $g(x)=x^{-1/2}$:

$$L = \lim_{x\to0^+}\frac{1}{\sqrt{1+x}} = 1$$

and $\int_0^1 x^{-1/2}dx = 2$ converges ($p=\tfrac12<1$). **Convergent.**

**Compare against the behaviour at the point that is causing trouble** — that is the only change.

---

## 7. Where Comparison Does Not Help

**(a) It never gives a value.** Comparison answers a yes/no question. If you need the number, you need Monday's method or a numerical one.

**(b) It requires a non-negative integrand.** For sign-changing integrands the increasing-and-bounded argument fails. *(The tool for those is absolute convergence — Week 8.)*

**(c) It requires you to guess the right comparison.** The test verifies a guess; it does not produce one. **Developing the instinct for what a function "behaves like" is the actual skill**, and it comes from doing many.

**(d) In the borderline cases it can be delicate.** $\int_2^\infty\frac{dx}{x\ln x}$ diverges while $\int_2^\infty\frac{dx}{x(\ln x)^2}$ converges — and no power of $x$ separates them, since both are bigger than $x^{-1-\epsilon}$ and smaller than $x^{-1}$. **Comparison against powers cannot decide these**; they must be done directly, by the substitution $u=\ln x$.

---

## 8. What To Take From This Lecture

1. **Comparison decides convergence without evaluating.** A different kind of question, answered a different way.
2. **Direct comparison:** bound above by a convergent, or below by a divergent. **The direction is everything.**
3. **Limit comparison:** if the ratio has a finite nonzero limit, the two share a fate. Much easier in practice.
4. **Strategy: keep the dominant terms, discard the rest.**
5. **Non-negativity is a hypothesis, not a technicality.**
6. **Comparison gives a verdict and a bound, never a value.**

---

## Looking Ahead

This lecture is the hinge of the course.

**Weeks 0–2 were about evaluation** — technique, craft, getting the number. **This week introduced the other question**: does the thing exist at all?

In Week 6 we ask it of sequences, in Week 7 of infinite sums. And the tests there — the Comparison Test, the Limit Comparison Test, and the **Integral Test**, which literally compares a sum to an integral — are the theorems on this page with the word "integral" replaced by "series".

> **The $p$-test you learned Monday becomes the $p$-series test.** $\sum\frac1{n^p}$ converges exactly
> when $p>1$, for exactly the reason $\int_1^\infty\frac{dx}{x^p}$ does. **You have already done the
> hard part.**

Before that, **Week 4** returns to computation — volumes, arc length, surface area — and **Midterm 1 in Week 5** covers Weeks 0–4.

---

*Next: Week 4, Monday — Volumes of Revolution*
