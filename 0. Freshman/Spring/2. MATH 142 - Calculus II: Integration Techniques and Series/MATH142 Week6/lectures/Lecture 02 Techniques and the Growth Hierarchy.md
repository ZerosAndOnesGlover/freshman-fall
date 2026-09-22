# MATH 142 · Calculus II
## Week 6 · Lecture 2 (Tuesday)
### Techniques, and the Growth Hierarchy

**Date:** Tuesday 2 March 2027 · 11:00–11:50 · Week 6

---

**Reading:** Stewart §11.1 (continued) | Apostol Ch. 10 §10.4

---

## 1. The Algebra of Limits

If $a_n\to A$ and $b_n\to B$ (both finite), then

$$a_n\pm b_n\to A\pm B,\qquad a_nb_n\to AB,\qquad \frac{a_n}{b_n}\to\frac AB\ (B\neq0),\qquad ca_n\to cA$$

and for continuous $f$: $f(a_n)\to f(A)$.

**All of this is inherited from MATH 141 via the function connection.** It is the last of these — **continuity passes through limits** — that gets used without comment and is worth naming:

$$\lim \ln\left(\frac{n}{n+1}\right) = \ln\left(\lim\frac{n}{n+1}\right) = \ln1 = 0$$

---

## 2. Rational Expressions: Divide by the Dominant Power

$$\lim_{n\to\infty}\frac{2n^2+3}{5n^2-n}$$

Divide top and bottom by $n^2$:

$$= \lim\frac{2+3/n^2}{5-1/n} = \frac{2}{5}$$

*(Verified.)*

**The rule:** for a ratio of polynomials, compare degrees.

| Degrees | Limit |
|---|---|
| top < bottom | $0$ |
| top = bottom | ratio of leading coefficients |
| top > bottom | diverges |

---

## 3. Indeterminate Forms: Pass to the Function

**L'Hôpital's rule does not apply to sequences** — there are no derivatives. **Pass to the function, differentiate, transfer back** (Lecture 1 §4).

### Example 1

$$\lim_{n\to\infty}n^{1/n}$$

An $\infty^0$ form. **Take logarithms first:**

$$\ln a_n = \frac{\ln n}{n}\to0 \implies a_n = e^{\ln a_n}\to e^0 = \boxed{1}$$

*(Verified.)*

**Taking logs is the standard move for $\infty^0$, $0^0$ and $1^\infty$**, and the final step uses continuity of $\exp$.

### Example 2 — the definition of $e$

$$\lim_{n\to\infty}\left(1+\frac1n\right)^n = \boxed{e} \qquad\qquad \lim_{n\to\infty}\left(1+\frac xn\right)^n = \boxed{e^x}$$

*(Both verified: the CAS gives $e$ and $e^3$ for $x=3$.)*

A $1^\infty$ form. Taking logs: $n\ln\left(1+\frac1n\right)$, which is $\infty\cdot0$; rewrite as $\frac{\ln(1+1/n)}{1/n}$ and apply L'Hôpital.

**This limit is the source of continuous compound interest, and it will reappear in Week 10 as the exponential series.**

### Example 3 — a difference of roots

$$\lim_{n\to\infty}\big(\sqrt{n+1}-\sqrt n\big)$$

An $\infty-\infty$ form. **Multiply by the conjugate:**

$$\big(\sqrt{n+1}-\sqrt n\big)\cdot\frac{\sqrt{n+1}+\sqrt n}{\sqrt{n+1}+\sqrt n} = \frac{1}{\sqrt{n+1}+\sqrt n}\to \boxed{0}$$

*(Verified.)*

**Rationalising is the standard move for differences of roots.** L'Hôpital would also work but is far messier.

---

## 4. The Growth Hierarchy

**This is the single most useful table in the second half of the course.** Each function grows strictly faster than everything to its left:

$$\boxed{\ln n \;\ll\; n^p\ (p>0) \;\ll\; a^n\ (a>1) \;\ll\; n! \;\ll\; n^n}$$

where $f\ll g$ means $\dfrac{f(n)}{g(n)}\to0$.

**Consequences you will use constantly:**

$$\frac{\ln n}{n^p}\to0,\qquad \frac{n^p}{a^n}\to0,\qquad \frac{a^n}{n!}\to0,\qquad \frac{n!}{n^n}\to0$$

*(All verified: $\frac{\ln n}{n}\to0$, $\frac{2^n}{n!}\to0$, $\frac{n!}{n^n}\to0$.)*

### The scale of it

At $n=20$:

| | value |
|---|---|
| $\ln n$ | $3.00$ |
| $n^2$ | $400$ |
| $2^n$ | $1.05\times10^{6}$ |
| $n!$ | $2.43\times10^{18}$ |
| $n^n$ | $1.05\times10^{26}$ |

*(Verified.)*

**Twenty-six orders of magnitude across the row**, at a value of $n$ you could count to.

> **This is the same hierarchy you met in CS 101 as the ordering of algorithmic complexity classes** —
> logarithmic, polynomial, exponential, factorial. The reason an $O(n!)$ algorithm is hopeless at
> $n=20$ and an $O(n^2)$ one is trivial **is this table.** It is the same mathematics, and this is
> where it gets proved.

### Why $\frac{a^n}{n!}\to0$

Worth seeing, because it is not a L'Hôpital argument. Fix $a$ and let $m$ be an integer with $m>2a$. For $n>m$,

$$\frac{a^n}{n!} = \underbrace{\frac{a^m}{m!}}_{\text{a fixed number } C}\cdot\underbrace{\frac{a}{m+1}\cdot\frac{a}{m+2}\cdots\frac an}_{\text{each factor} <\frac12}\;<\; C\left(\frac12\right)^{n-m}\to0$$

**Each new factorial factor eventually divides by something bigger than the fixed numerator.** The tail is dominated by a geometric sequence, which we know goes to 0.

---

## 5. Stirling's Approximation

The factorial's growth can be made precise:

$$\boxed{n! \sim \sqrt{2\pi n}\left(\frac ne\right)^n}$$

meaning the ratio tends to 1.

*(Verified: the ratio $n!/\text{Stirling}$ is $1.0168$ at $n=5$, $1.0084$ at $n=10$, $1.0042$ at $n=20$, $1.0017$ at $n=50$ — approaching 1, and roughly halving each time $n$ doubles, consistent with the known correction factor $1+\frac{1}{12n}$.)*

> **The $\sqrt{2\pi}$ in Stirling's formula comes from Wallis' product** — the one you proved in
> **Lab 1**. That is why Lab 1's solutions listed "it is the origin of Stirling's formula" as one of
> the reasons a computationally useless formula still matters. **Here is the payoff.**

**Stirling is used constantly** in probability, statistical mechanics, and the analysis of algorithms — it is how you show that $\log_2(n!) \approx n\log_2 n$, the information-theoretic lower bound for comparison sorting that you met in CS 102.

---

## 6. A Worked Set

| Limit | Method | Value |
|---|---|---|
| $\dfrac{3n^3-n}{7n^3+2n^2}$ | divide by $n^3$ | $\frac37$ |
| $\dfrac{\ln n}{\sqrt n}$ | L'Hôpital on the function | $0$ |
| $n^{1/n}$ | logs | $1$ |
| $\left(1+\frac2n\right)^{3n}$ | logs, or $=\left[\left(1+\frac2n\right)^n\right]^3$ | $e^6$ |
| $\dfrac{\cos n}{n^2}$ | squeeze | $0$ |
| $\dfrac{5^n}{n!}$ | growth hierarchy | $0$ |
| $\dfrac{n!}{n^n}$ | growth hierarchy | $0$ |
| $\sqrt{n^2+n}-n$ | conjugate | $\frac12$ |
| $(-1)^n\frac{n}{n+1}$ | — | **diverges** |

**The last one is worth pausing on.** $\frac{n}{n+1}\to1$, so the terms approach $+1$ and $-1$ alternately and **never settle**. A student who computes $\lim\frac{n}{n+1}=1$ and stops has missed the sign entirely.

---

## 7. What To Take From This Lecture

1. **Divide by the dominant power** for rational expressions.
2. **Pass to the function** for L'Hôpital; **take logarithms** for $1^\infty$, $\infty^0$, $0^0$.
3. **Rationalise** differences of roots.
4. **Learn the growth hierarchy** $\ln n \ll n^p \ll a^n \ll n! \ll n^n$. It is CS 101's complexity ordering, proved.
5. **Stirling:** $n!\sim\sqrt{2\pi n}(n/e)^n$ — and its $\sqrt{2\pi}$ is Lab 1's Wallis product.
6. **Check the sign before declaring convergence.** $(-1)^n a_n$ with $a_n\to L\neq0$ diverges.

---

*Next: Wednesday — Monotone Convergence, and Sequences That Define Themselves*
