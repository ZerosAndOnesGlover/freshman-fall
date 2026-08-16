# MATH 142 · Calculus II
## Week 6 · Lecture 3 (Friday)
### Monotone Convergence, and Sequences That Define Themselves

**Date:** Friday 26 February 2027 · 11:00–11:50 · Week 6

---

**Reading:** Stewart §11.1 | Apostol Ch. 10 §10.5–10.6

---

## 1. Proving Convergence Without Finding the Limit

Every limit so far has been computed: you produced a number. **Today's theorem does something different — it establishes that a limit *exists* without telling you what it is.**

> **Monotone Convergence Theorem.**
> An **increasing** sequence that is **bounded above** converges.
> A **decreasing** sequence that is **bounded below** converges.

**Two finite checks replace an infinite question.**

### Why it is true, and why it is deep

An increasing sequence bounded above has a **least upper bound** $L$ (the supremum). Given $\varepsilon>0$, $L-\varepsilon$ is not an upper bound, so some $a_N>L-\varepsilon$; and since the sequence increases and never exceeds $L$, every later term lies in $(L-\varepsilon,L]$. That is exactly $a_n\to L$. $\blacksquare$

**The theorem rests entirely on the existence of that least upper bound**, which is the **completeness axiom** for $\mathbb R$ — the defining property that distinguishes the reals from the rationals.

> **The rationals fail this theorem.** The sequence
> $$1,\ 1.4,\ 1.41,\ 1.414,\ 1.4142,\ \ldots$$
> is increasing, bounded above by 2, and consists entirely of rational numbers. **Its limit $\sqrt2$
> is not rational.** Inside $\mathbb Q$ this sequence "converges to a hole".
>
> **Monotone convergence is the precise statement that $\mathbb R$ has no holes**, and it is why the
> rest of this course is possible.

### You have used it already

- **Week 3:** the comparison test worked because $F(T)=\int_a^T f$ is increasing in $T$ (as $f\ge0$) and bounded above by the comparison integral. *That was this theorem.*
- **Week 7 onwards:** every convergence test for a series with positive terms is this theorem applied to the partial sums.

---

## 2. Recursive Sequences

A sequence defined by its own previous terms:

$$a_1 = c,\qquad a_{n+1} = g(a_n)$$

**These are what algorithms produce.** Each step applies the same rule to the last answer, which is precisely a loop.

### The two-step method

> **Step 1. Prove the sequence converges** — usually by monotone convergence.
> **Step 2. *Then* find the limit** by solving the **fixed point equation** $L = g(L)$.

**Step 2 is justified by continuity.** If $a_n\to L$ and $g$ is continuous, then

$$L = \lim a_{n+1} = \lim g(a_n) = g\!\left(\lim a_n\right) = g(L)$$

### ⚠ Step 1 is not optional

Consider $a_1=1$, $a_{n+1}=2a_n$. The terms are $1,2,4,8,16,32,\ldots$ — **plainly divergent.**

But the fixed point equation says $L=2L$, hence $L=0$. **A confident, completely wrong answer.**

*(Verified: the terms are $2^{n-1}$ and diverge; the fixed point equation nonetheless returns 0.)*

> **Solving $L=g(L)$ tells you what the limit *would be if it existed*.** It says nothing about
> whether it does. **Marks are lost for this every year** — and it is the same structural error as
> applying the Fundamental Theorem across a singularity in Week 3: *using a theorem whose hypotheses
> were never checked.*

---

## 3. Worked Example — the Nested Radical

$$a_1=\sqrt2,\qquad a_{n+1}=\sqrt{2+a_n}$$

*(This is the sequence $\sqrt2,\ \sqrt{2+\sqrt2},\ \sqrt{2+\sqrt{2+\sqrt2}},\ \ldots$)*

**Step 1a — bounded above by 2, by induction.** True for $a_1=\sqrt2<2$. If $a_n<2$ then

$$a_{n+1}=\sqrt{2+a_n}<\sqrt{2+2}=2 \qquad\checkmark$$

**Step 1b — increasing.** $a_{n+1}>a_n \iff \sqrt{2+a_n}>a_n \iff 2+a_n>a_n^2 \iff a_n^2-a_n-2<0 \iff (a_n-2)(a_n+1)<0$, which holds whenever $0<a_n<2$ — true by Step 1a. $\checkmark$

**Increasing and bounded above $\implies$ converges.**

**Step 2 — the limit.** $L=\sqrt{2+L}$, so $L^2=2+L$, giving $L^2-L-2 = (L-2)(L+1)=0$. Since all terms are positive, $L\ne-1$, so

$$\boxed{L=2}$$

*(Verified: over 40 iterations the sequence is increasing throughout and bounded above by 2, converging to $2.0$. The terms run $1.4142,\ 1.8478,\ 1.9616,\ 1.9904,\ 1.9976,\ldots$, and sympy confirms the fixed point equation has roots $-1$ and $2$.)*

**Note that the discarded root was not spurious algebra — it was a real solution of the fixed point equation, excluded by an argument about the sequence.** Both steps did work.

---

## 4. The Golden Ratio

The Fibonacci numbers $F_1=F_2=1$, $F_{n+1}=F_n+F_{n-1}$ grow without bound. **But the ratios converge.**

Let $r_n = \dfrac{F_{n+1}}{F_n}$. Dividing the recurrence by $F_n$:

$$r_n = \frac{F_n+F_{n-1}}{F_n} = 1 + \frac{1}{r_{n-1}}$$

— a recursive sequence with $g(x)=1+\frac1x$. Its fixed point satisfies

$$L = 1+\frac1L \implies L^2-L-1=0 \implies L = \frac{1\pm\sqrt5}{2}$$

The ratios are positive, so

$$\boxed{L = \varphi = \frac{1+\sqrt5}{2} \approx 1.6180339887}$$

*(Verified: $F_{22}/F_{21} = 1.61803398501735794$, an error of $3.7\times10^{-9}$; sympy confirms the roots $\frac{1\pm\sqrt5}{2}$.)*

**The convergence is not monotone** — the ratios alternate above and below $\varphi$ — so the Monotone Convergence Theorem does not apply directly. *(The standard fix considers the even- and odd-indexed subsequences separately, each of which is monotone.)*

**Worth noting:** $\varphi$ appears in the analysis of the Euclidean algorithm — the worst case for computing $\gcd(a,b)$ is consecutive Fibonacci numbers, which is why the algorithm is $O(\log n)$.

---

## 5. Fixed Points and the Speed of Convergence

**Which fixed points does an iteration actually reach, and how fast?** The answer is a derivative.

Suppose $a_{n+1}=g(a_n)$ with $g(L)=L$. Writing $e_n = a_n - L$ and expanding $g$ near $L$:

$$e_{n+1} = g(a_n)-g(L) \approx g'(L)\,e_n$$

> **The fixed point criterion.**
> - If $|g'(L)|<1$, the iteration **converges** to $L$ (for a good enough start) — the error shrinks by roughly the constant factor $|g'(L)|$ each step. This is **linear convergence.**
> - If $|g'(L)|>1$, the iteration **diverges** from $L$.
> - If $g'(L)=0$, the linear term vanishes and the next term governs: $e_{n+1}\approx\tfrac12g''(L)e_n^2$. **The error squares. This is quadratic convergence.**

### What quadratic convergence means

**The number of correct digits doubles at every step.** For the Babylonian square-root iteration, starting from $a_0=1$:

| step | correct digits |
|---|---|
| 1 | 1 |
| 2 | 2 |
| 3 | 5 |
| 4 | 11 |
| 5 | 24 |
| 6 | **48** |

*(Measured — Lab 6 reproduces this.)*

**Six steps for 48 decimal places.** Compare Lab 1's Wallis product, which needed $8\times10^9$ factors for ten.

**That difference is not cleverness. It is one derivative being zero**, and Lab 6 makes you compute it.

---

## 6. What To Take From This Lecture

1. **Monotone + bounded $\implies$ convergent.** Two finite checks replace an infinite question.
2. **It is the completeness axiom.** The rationals fail it, and $\sqrt2$ is the counterexample.
3. **Recursive sequences: prove convergence first, then solve $L=g(L)$.**
4. **Never skip Step 1.** $a_{n+1}=2a_n$ diverges while its fixed point equation confidently says 0.
5. **$|g'(L)|<1$ gives convergence; $g'(L)=0$ gives quadratic convergence** — digits doubling per step.

---

## Looking Ahead

**Next week the subject is infinite sums**, and the bridge is this:

$$\sum_{n=1}^\infty a_n \;:=\; \lim_{N\to\infty}\underbrace{\big(a_1+a_2+\cdots+a_N\big)}_{s_N}$$

**A series is nothing but a sequence of partial sums.** Every question you can ask about a series is a question about that sequence — so everything this week transfers directly.

**And the first test you meet will be the Integral Test**, which compares a series to an improper integral — bringing Week 3 and Week 6 together into one theorem.

---

*Next: Week 7, Monday — Series and the Geometric Series*
