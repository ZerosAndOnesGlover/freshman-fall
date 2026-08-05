# MATH 142 · Calculus II
## Week 9 · Lecture 1 (Monday)
### Power Series and the Radius of Convergence

---

**Reading:** Stewart §11.8 | Apostol Ch. 11 §11.1–11.3
**Quiz 09** — this Monday, **covers Week 8** (alternating series, absolute convergence, Ratio and Root tests)

---

## 1. Definition

A **power series centred at $a$** is

$$\sum_{n=0}^\infty c_n(x-a)^n = c_0+c_1(x-a)+c_2(x-a)^2+\cdots$$

The $c_n$ are fixed numbers (the **coefficients**); $x$ is a variable.

**For each fixed value of $x$, this is an ordinary numerical series** — exactly the objects of Weeks 7 and 8. **No new theory is needed to test it.** What is new is that the answer depends on $x$, and we want to know for which $x$ it converges.

**Every power series converges at $x=a$**, where every term after the first vanishes and the sum is $c_0$. **The question is what else.**

---

## 2. The Structure Theorem

> **Theorem.** For a power series $\sum c_n(x-a)^n$, exactly one of these holds:
>
> **(i)** it converges **only at $x=a$**;
> **(ii)** it converges for **every** real $x$;
> **(iii)** there is $R>0$ with convergence for $|x-a|<R$ and divergence for $|x-a|>R$.

$R$ is the **radius of convergence** — with $R=0$ in case (i) and $R=\infty$ in case (ii).

> **The remarkable content is that the convergence set is always an interval centred at $a$.** It is
> never a scattered set, never two pieces, never anything exotic. **A power series converges on a
> disc** (an interval, on the real line), and the only question is its size and whether the ends are
> included.

**At $|x-a| = R$ the theorem says nothing** — and that is not an oversight. Tomorrow's lecture is entirely about those two points.

---

## 3. Finding $R$ With the Ratio Test

Apply the Ratio Test to $a_n = c_n(x-a)^n$:

$$\left|\frac{a_{n+1}}{a_n}\right| = \left|\frac{c_{n+1}}{c_n}\right|\cdot|x-a| \longrightarrow \underbrace{\left(\lim\left|\frac{c_{n+1}}{c_n}\right|\right)}_{=:\ \ell}\cdot|x-a|$$

Convergence requires $\ell\,|x-a|<1$, i.e.

$$\boxed{R = \frac{1}{\ell} = \left(\lim_{n\to\infty}\left|\frac{c_{n+1}}{c_n}\right|\right)^{-1}}$$

with the conventions $R=\infty$ when $\ell=0$, and $R=0$ when $\ell=\infty$.

> **Note where the $|x-a|$ went.** It factors straight out of the ratio, which is exactly why the
> convergence set is an interval — the whole $x$-dependence is a single multiplicative factor.

---

## 4. Worked Examples

### Example 1 — the geometric series

$$\sum_{n=0}^\infty x^n: \qquad \ell = \lim\left|\frac{1}{1}\right| = 1 \implies \boxed{R=1}$$

**Converges for $|x|<1$**, where we already know the sum is $\frac{1}{1-x}$. *(Verified.)*

### Example 2 — same radius, different coefficients

$$\sum_{n=1}^\infty\frac{x^n}{n}: \qquad \ell = \lim\frac{n}{n+1} = 1 \implies \boxed{R=1}$$

$$\sum_{n=1}^\infty\frac{x^n}{n^2}: \qquad \ell = \lim\frac{n^2}{(n+1)^2} = 1 \implies \boxed{R=1}$$

*(Both verified.)*

**All three examples have $R=1$** — yet tomorrow we will see they have **three different intervals**. **The radius does not determine the endpoints.**

### Example 3 — $R=0$

$$\sum_{n=0}^\infty n!\,x^n: \qquad \ell = \lim\frac{(n+1)!}{n!} = \lim(n+1) = \infty \implies \boxed{R=0}$$

*(Verified.)* **Converges only at $x=0$.** The coefficients grow so fast that no nonzero $x$ can tame them.

### Example 4 — $R=\infty$

$$\sum_{n=0}^\infty\frac{x^n}{n!}: \qquad \ell = \lim\frac{n!}{(n+1)!} = \lim\frac{1}{n+1} = 0 \implies \boxed{R=\infty}$$

*(Verified.)* **Converges for every real $x$** — and in Week 10 we will identify its sum as $e^x$.

### Example 5 — a radius that is not 1

$$\sum_{n=1}^\infty\frac{x^n}{n\,2^n}: \qquad \ell = \lim\frac{n\,2^n}{(n+1)2^{n+1}} = \frac12 \implies \boxed{R=2}$$

*(Verified.)*

### Example 6 — an unexpected radius

$$\sum_{n=1}^\infty\frac{n^n}{n!}x^n: \qquad \ell = \lim\frac{(n+1)^{n+1}}{(n+1)!}\cdot\frac{n!}{n^n} = \lim\left(1+\frac1n\right)^n = e$$

$$\implies \boxed{R = \frac1e}$$

*(Verified.)*

**The Week 6 limit $\left(1+\frac1n\right)^n\to e$ producing a radius of convergence** — a nice illustration that the coefficient sequence can be as interesting as the series.

---

## 5. Centres Other Than 0

The whole analysis is about $|x-a|$, so a shifted centre just shifts the interval.

### Example 7

$$\sum_{n=1}^\infty\frac{(x-3)^n}{n\,2^n}$$

Same coefficients as Example 5, so $R=2$ — but now centred at $a=3$:

$$|x-3|<2 \iff 1<x<5$$

**The interval is centred at 3 with radius 2**, so the open interval is $(1,5)$, and the endpoints to check are $x=1$ and $x=5$.

> **A very common error is to report the interval as $(-2,2)$**, forgetting the centre. **Write down
> $|x-a|<R$ first and solve it**, rather than quoting an interval from memory.

---

## 6. Series With Missing Terms

$$\sum_{n=0}^\infty\frac{x^{2n}}{3^n}$$

**The coefficient of $x^{2n+1}$ is zero**, so $\frac{c_{n+1}}{c_n}$ is undefined for the actual coefficient sequence — you cannot apply the boxed formula blindly.

**Apply the Ratio Test to the terms as written**, not to a coefficient sequence:

$$\left|\frac{a_{n+1}}{a_n}\right| = \left|\frac{x^{2n+2}}{3^{n+1}}\cdot\frac{3^n}{x^{2n}}\right| = \frac{x^2}{3}$$

Convergence needs $\frac{x^2}{3}<1$, i.e. $|x|<\sqrt3$:

$$\boxed{R=\sqrt3}$$

> **Rule: apply the Ratio Test to consecutive *nonzero terms*, including the powers of $x$.** The
> coefficient formula is a shortcut valid only when every $c_n$ is nonzero. **Half-power and
> odd-power series are common in Week 10** — $\sin$, $\cos$ and $\arctan$ all have missing terms.

---

## 7. Absolute Convergence Inside the Radius

**A point worth stating explicitly**, because Lecture 3 depends on it entirely.

The Ratio Test's conclusion for $L<1$ is **absolute** convergence. So:

> **For $|x-a|<R$, a power series converges absolutely.**

**By Week 8, that licenses everything**: rearrangement, term-by-term differentiation and integration, multiplication of series. **Inside the radius, a power series behaves like a polynomial.**

**At the endpoints it may converge only conditionally** — as $\sum\frac{(-1)^n}{n}$ does — and there none of those manipulations is guaranteed.

---

## 8. What To Take From This Lecture

1. **A power series converges on an interval centred at $a$** — always.
2. **$R = \left(\lim\left|\frac{c_{n+1}}{c_n}\right|\right)^{-1}$**, with $R=0$ and $R=\infty$ as the extreme cases.
3. **The $|x-a|$ factors out of the ratio**, which is why the set is an interval.
4. **Solve $|x-a|<R$ explicitly** — do not quote an interval centred at 0 for a series centred elsewhere.
5. **For missing terms, run the Ratio Test on the terms themselves.**
6. **Inside $R$ convergence is absolute**, which is the licence for Lecture 3.

---

*Next: Tuesday — Endpoints, and the Interval of Convergence*
