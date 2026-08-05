# MATH 142 · Calculus II
## Week 8 · Lecture 3 (Wednesday)
### The Ratio and Root Tests

---

**Reading:** Stewart §11.6 | Apostol Ch. 10 §10.21

---

## 1. Comparing With a Geometric Series, Automatically

A geometric series $\sum ar^n$ converges exactly when $|r|<1$, and $r$ is **the factor by which each term is multiplied to get the next.**

**The Ratio Test asks the same question of an arbitrary series:** by what factor do the terms shrink, eventually?

> **Ratio Test.** Let $L=\displaystyle\lim_{n\to\infty}\left|\frac{a_{n+1}}{a_n}\right|$ (if it exists).
>
> - $L<1$ $\implies$ $\sum a_n$ converges **absolutely**
> - $L>1$ (or $L=\infty$) $\implies$ $\sum a_n$ **diverges**
> - $L=1$ $\implies$ **no conclusion**

**Why:** if $L<1$, pick $r$ with $L<r<1$. Eventually $|a_{n+1}|\le r|a_n|$, so from that point the terms are dominated by a geometric series with ratio $r<1$ — **direct comparison** finishes it. If $L>1$ the terms grow, so $a_n\not\to0$ and the **$n$-th Term Test** gives divergence.

> **Notice the two conclusions are asymmetric.** $L<1$ gives **absolute** convergence — a strong
> conclusion, licensing everything from Lecture 2. $L>1$ gives divergence via the $n$-th Term Test,
> which is why it is genuinely conclusive and not merely "the comparison failed".

---

## 2. The $L=1$ Case Is Not a Formality

$$\sum\frac1n \qquad\text{and}\qquad \sum\frac{1}{n^2}$$

**Both have ratio limit exactly 1** *(verified)*:

$$\frac{n}{n+1}\to1 \qquad\qquad \frac{n^2}{(n+1)^2}\to1$$

**One diverges and one converges.** So when $L=1$ the test has finished and supplied **no information whatsoever** — you must use Week 7.

> **Writing "$L=1$, so the series diverges" is a serious error** and appears every year. The test is
> *silent*, not negative. **The same discipline as the $n$-th Term Test in Week 7.**

**More generally, the Ratio Test always gives $L=1$ on a $p$-series** — for every $p$. **It cannot see polynomial behaviour at all.** It is a tool for factorials and exponentials, where terms shrink geometrically or faster.

---

## 3. What the Ratio Test Is Good At

**Factorials and $n$-th powers**, because they simplify beautifully in a ratio.

| Series | $L$ | Verdict |
|---|---|---|
| $\sum\dfrac{n^2}{2^n}$ | $\frac12$ | converges |
| $\sum\dfrac{(-3)^n}{n!}$ | $0$ | converges absolutely |
| $\sum\dfrac{n!}{2^nn^2}$ | $\infty$ | diverges |
| $\sum\dfrac{(2n)!}{(n!)^2}$ | $4$ | diverges |
| $\sum\dfrac{n^n}{n!}$ | $e$ | diverges |
| $\sum\dfrac{n!}{n^n}$ | $\frac1e$ | **converges** |
| $\sum\dfrac{1}{n^3}$ | $1$ | **inconclusive** |

*(all verified)*

### Example 1 — the archetype

$$\sum\frac{n^2}{2^n}: \qquad \left|\frac{a_{n+1}}{a_n}\right| = \frac{(n+1)^2}{2^{n+1}}\cdot\frac{2^n}{n^2} = \frac12\left(\frac{n+1}{n}\right)^2 \to \frac12 < 1$$

**Converges absolutely.**

### Example 2 — the two factorial cousins

$$\sum\frac{n^n}{n!}: \quad \frac{a_{n+1}}{a_n} = \frac{(n+1)^{n+1}}{(n+1)!}\cdot\frac{n!}{n^n} = \left(1+\frac1n\right)^n\to e>1 \implies \textbf{diverges}$$

$$\sum\frac{n!}{n^n}: \quad \frac{a_{n+1}}{a_n} = \left(\frac{n}{n+1}\right)^n\to\frac1e<1 \implies \textbf{converges}$$

*(Both verified.)*

> **These two settle a question left open in Week 6.** There we showed $\frac{n!}{n^n}\to0$ but said
> nothing about the *sum*. **The Ratio Test now gives it in one line** — and the limits $e$ and $\frac1e$
> come straight from $\left(1+\frac1n\right)^n\to e$.

---

## 4. The Root Test

> **Root Test.** Let $L=\displaystyle\lim_{n\to\infty}\sqrt[n]{|a_n|}$.
>
> - $L<1$ $\implies$ converges **absolutely**
> - $L>1$ $\implies$ **diverges**
> - $L=1$ $\implies$ **no conclusion**

**Same trichotomy, same geometric reasoning** — if $|a_n|^{1/n}\le r<1$ eventually, then $|a_n|\le r^n$ and comparison finishes it.

### When to prefer it

**Use the Root Test when the whole term is an $n$-th power.** The root then cancels the exponent and the limit is immediate.

| Series | $L$ | Verdict |
|---|---|---|
| $\sum\left(\dfrac{n}{2n+1}\right)^n$ | $\frac12$ | converges |
| $\sum\dfrac{1}{(\ln n)^n}$ | $0$ | converges |

*(both verified)*

$$\sqrt[n]{\left(\frac{n}{2n+1}\right)^n} = \frac{n}{2n+1}\to\frac12 \qquad\qquad \sqrt[n]{\frac{1}{(\ln n)^n}} = \frac{1}{\ln n}\to0$$

**One line each.** The Ratio Test would be far messier on both.

### The two tests are close relatives

Whenever the ratio limit exists, the root limit exists and equals it. **The Root Test is strictly stronger** — it sometimes works when the ratio limit fails to exist — but in practice you choose by convenience:

> **$n$-th powers → Root Test. Factorials → Ratio Test.**

**They fail together**: if one gives $L=1$, so does the other. **Neither can see a $p$-series.**

---

## 5. An Instructive Failure

$$\sum_{n=1}^\infty\frac{\left(1+\frac1n\right)^{n^2}}{e^n}$$

The whole term is an $n$-th power, so try the Root Test:

$$\sqrt[n]{a_n} = \frac{\left(1+\frac1n\right)^{n}}{e} \longrightarrow \frac ee = 1$$

**$L=1$ — inconclusive.** *(Verified.)*

**But the series is not hard.** Look at the terms themselves:

$$a_n \longrightarrow e^{-1/2} = 0.6065\ldots \neq 0$$

*(Verified: $a_n$ is $0.6256$ at $n=10$, $0.60854$ at $n=100$, $0.60655$ at $n=10^4$, settling at $e^{-1/2}$.)*

**So the $n$-th Term Test gives divergence immediately.**

> **Two lessons.**
> **(1)** An inconclusive Ratio or Root Test means *try something else*, and the something else is
> often the cheapest test of all.
> **(2)** **Check the $n$-th Term Test first.** It costs five seconds and would have finished this
> problem before the Root Test was even attempted.

*(A caution from preparing this example: it is easy to confuse $\lim a_n$ with $\lim\sqrt[n]{a_n}$. They are $e^{-1/2}$ and $1$ here — **different questions with different answers**, and only the second is the Root Test.)*

---

## 6. Strategy: The Complete Decision Procedure

You now have every test this course will teach. **In order of what to try:**

| Step | Check | If it applies |
|---|---|---|
| **1** | Does $a_n\to0$? | **No** → diverges, done |
| **2** | Geometric or telescoping? | sum it exactly |
| **3** | $p$-series? | $p>1$ converges |
| **4** | Factorials or $n$-th powers? | **Ratio** or **Root** Test |
| **5** | Positive terms, rational-ish? | **limit comparison** with a $p$-series |
| **6** | Positive, decreasing, integrable? | **Integral Test** (plus an error bound) |
| **7** | Mixed signs? | test $\sum\lvert a_n\rvert$ first, then **Alternating Series** |

**Step 1 is free and finishes a surprising number of problems.** Step 7 is the order to work in when signs are present, because absolute convergence is the stronger conclusion.

---

## 7. What To Take From This Lecture

1. **Ratio Test:** $L=\lim\left|\frac{a_{n+1}}{a_n}\right|$; $L<1$ **absolutely** convergent, $L>1$ divergent, $L=1$ **silent**.
2. **Root Test:** the same with $\sqrt[n]{|a_n|}$; prefer it for $n$-th powers.
3. **Both are geometric comparisons** — the third time this idea has appeared, after Week 3's $p$-test and Week 6's $|g'(L)|<1$.
4. **$L=1$ is genuinely inconclusive:** $\sum\frac1n$ and $\sum\frac1{n^2}$ both give it.
5. **Neither test can see a $p$-series.** They are for factorials and exponentials.
6. **When a test is inconclusive, try the cheapest one you have not used.**

---

## Looking Ahead

**Next week we put a variable into the series:**

$$\sum_{n=0}^\infty c_nx^n$$

For each fixed $x$ this is an ordinary series, and **the Ratio Test decides it** — giving a **radius of convergence** $R$ such that the series converges for $|x|<R$ and diverges for $|x|>R$.

**And at $|x|=R$ the Ratio Test gives exactly $L=1$** — which is precisely why the endpoints have to be examined separately, by hand, with the tests of Weeks 7 and 8.

> **Today's "inconclusive" case is next week's main event.**

---

*Next: Week 9, Monday — Power Series*
