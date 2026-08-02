# MATH 141 — Calculus I
## Week 8 · Lecture 3 (Wednesday)
### Properties of the Definite Integral

---

**Reading:** Stewart §5.2 | Spivak Ch. 13

---

## Why Properties Before Technique

Monday built Riemann sums; Tuesday defined

$$\int_a^b f(x)\,dx=\lim_{n\to\infty}\sum_{i=1}^{n}f(x_i^*)\,\Delta x$$

That definition is unusable for computation — Week 9's Fundamental Theorem fixes that. But before the
FTC arrives, the properties below let you evaluate, bound and manipulate integrals **without ever
computing a limit**, and several of them are the only tool available when no antiderivative exists.

Each follows from the corresponding property of finite sums, since the integral is a limit of sums.

---

## 1. Linearity

$$\int_a^b\big[c_1f(x)+c_2g(x)\big]dx=c_1\int_a^b f(x)\,dx+c_2\int_a^b g(x)\,dx$$

Verified on $[0,2]$ with $f=x^2$, $g=\sin x$:

| Quantity | Value |
|---|---|
| $\int_0^2 x^2\,dx$ | $2.6666666667$ *(exact $\tfrac83$)* |
| $\int_0^2 \sin x\,dx$ | $1.4161468365$ *(exact $1-\cos 2$)* |
| $\int_0^2 (3f-2g)\,dx$ | $5.1677063269$ |
| $3I_f - 2I_g$ | $5.1677063269$ ✓ |

**Why it holds:** a Riemann sum of $c_1f+c_2g$ splits termwise, and limits respect finite sums.

**What it does not permit.** There is no product rule for integrals:

$$\int fg \ne \left(\int f\right)\left(\int g\right)$$

Check on $[0,1]$ with $f=g=x$: $\int_0^1 x^2 = \tfrac13$, but $\left(\int_0^1 x\right)^2=\tfrac14$.
Week 10's integration by parts exists precisely because products are hard.

---

## 2. Additivity Over Intervals

$$\int_a^b f = \int_a^c f + \int_c^b f$$

Verified: $\int_0^2 x^2 = 2.6666666667$, while $\int_0^1 + \int_1^2 = 0.3333333333 + 2.3333333333 =
2.6666666667$ ✓

**This holds for any $c$, including $c$ outside $[a,b]$** — once the orientation convention below is
adopted. It is the property that lets you handle piecewise-defined integrands: split at each break
point and integrate each piece.

---

## 3. Orientation

Two conventions, both forced by consistency:

$$\int_b^a f = -\int_a^b f, \qquad \int_a^a f = 0$$

Verified: $\int_2^0 x^2 = -2.6666666667$ and $\int_1^1 x^2 = 0$.

These are *definitions*, not theorems — but they are the only definitions that keep additivity true
when $c$ lies outside $[a,b]$. The minus sign is why "area" and "integral" are not synonyms: an
integral is a **signed** quantity, sensitive to direction of travel as well as to the sign of $f$.

---

## 4. Comparison and Bounds

> **If $f(x)\le g(x)$ on $[a,b]$, then $\displaystyle\int_a^b f \le \int_a^b g$.**

Two consequences do most of the work.

**Crude bounds.** If $m \le f(x) \le M$ on $[a,b]$, then

$$m(b-a) \;\le\; \int_a^b f \;\le\; M(b-a)$$

Verified for $x^2$ on $[0,2]$, where $m=0$ and $M=4$:

$$0 \le 2.666667 \le 8 \quad\checkmark$$

The bounds are loose, but they cost nothing and require no antiderivative — which matters when none
exists in closed form.

**The triangle inequality for integrals.**

$$\left|\int_a^b f\right| \le \int_a^b |f|$$

Verified on $[0,2\pi]$:

| | Value |
|---|---|
| $\int_0^{2\pi}\sin x\,dx$ | $-3.13\times10^{-16}$ — i.e. **$0$** |
| $\int_0^{2\pi}\lvert\sin x\rvert\,dx$ | $4.0000000000$ |

$|0| \le 4$, and dramatically so. The first integral cancels because the sine's positive and negative
humps are equal; the second measures **total** area regardless of sign.

**This is the displacement-versus-distance distinction from Week 4**, in integral form: $\int v\,dt$
gives displacement, $\int|v|\,dt$ gives distance travelled.

---

## 5. Symmetry

For $f$ integrable on $[-a,a]$:

| $f$ | Result |
|---|---|
| **Odd** — $f(-x)=-f(x)$ | $\displaystyle\int_{-a}^{a}f = 0$ |
| **Even** — $f(-x)=f(x)$ | $\displaystyle\int_{-a}^{a}f = 2\int_0^a f$ |

Verified on $[-2,2]$:

- $x^3$ (odd): $1.63\times10^{-15}$ — **exactly $0$** to machine precision.
- $x^2$ (even): $5.3333333333$, and $2\int_0^2 x^2 = 5.3333333333$ ✓

**Check symmetry before doing any work.** Recognising that $\int_{-1}^{1}x^3e^{x^2}\,dx=0$ takes a
second; evaluating it takes considerably longer and is unnecessary. This is the single highest-value
habit in this lecture.

*(Take care: the integrand must be odd **and** the interval symmetric about $0$. $\int_0^2 x^3 \ne 0$.)*

---

## 6. Average Value and the Mean Value Theorem for Integrals

> **Definition.** The **average value** of $f$ on $[a,b]$ is
> $$f_{\text{avg}}=\frac{1}{b-a}\int_a^b f(x)\,dx$$

This is the continuous analogue of an arithmetic mean: a Riemann sum divided by $n$ is exactly the
mean of $n$ samples, and the limit replaces the sum with an integral.

Verified for $x^2$ on $[0,2]$: $f_{\text{avg}} = \tfrac12(2.6666667) = 1.3333333333$, exactly
$\tfrac43$.

> **MVT for Integrals.** If $f$ is continuous on $[a,b]$, there exists $c\in(a,b)$ with
> $$f(c)=f_{\text{avg}}, \qquad\text{equivalently}\qquad \int_a^b f = f(c)(b-a)$$

**A continuous function attains its own average.** Verified: solving $c^2 = \tfrac43$ gives
$c = \sqrt{4/3} = 1.1547005384$, which lies in $(0,2)$ ✓

**The proof is the IVT** (Week 2). By the bounds in §4, $m \le f_{\text{avg}} \le M$; since $f$
attains $m$ and $M$ and is continuous, the IVT gives a point where it takes the intermediate value
$f_{\text{avg}}$.

**Continuity is essential.** A step function jumping between $0$ and $1$ has average $\tfrac12$ and
never takes that value — the same reason the IVT needs continuity.

---

## 7. Riemann Sums as Estimates

Before the FTC, sums are the only way to get a number. Verified for $\int_0^1 x^2\,dx = \tfrac13$:

| $n$ | left | **midpoint** | right |
|---|---|---|---|
| $10$ | $0.28500000$ | $0.33250000$ | $0.38500000$ |
| $100$ | $0.32835000$ | $0.33332500$ | $0.33835000$ |
| $1000$ | $0.33283350$ | $0.33333325$ | $0.33383350$ |
| $10\,000$ | $0.33328334$ | $0.33333333$ | $0.33338334$ |

Two things to read off:

**Left and right bracket the answer** for a monotone integrand — left underestimates for increasing
$f$, right overestimates. That gives a free error bound: the true value lies between them.

**The midpoint rule is far better.** At $n=100$ it already has 4 correct decimals, where left and
right have 2. Left and right converge like $O(1/n)$; the midpoint rule is $O(1/n^2)$ — verified,
since going from $n=100$ to $n=1000$ improves the midpoint error by roughly $100\times$ and the
endpoint errors by only $10\times$.

---

## Summary

| Property | Statement |
|---|---|
| Linearity | $\int(c_1f+c_2g)=c_1\int f+c_2\int g$ — verified |
| **No product rule** | $\int fg \ne (\int f)(\int g)$ — $\tfrac13$ vs $\tfrac14$ on $[0,1]$ |
| Additivity | $\int_a^b=\int_a^c+\int_c^b$ |
| Orientation | $\int_b^a=-\int_a^b$; $\int_a^a=0$ |
| Comparison | $f\le g \Rightarrow \int f\le\int g$ |
| Crude bounds | $m(b-a)\le\int f\le M(b-a)$ — verified $0\le2.67\le8$ |
| Triangle inequality | $\lvert\int f\rvert\le\int\lvert f\rvert$ — verified $0$ vs $4$ |
| **Odd on $[-a,a]$** | $\int = 0$ — check this first |
| **Even on $[-a,a]$** | $\int = 2\int_0^a$ |
| Average value | $\frac{1}{b-a}\int_a^b f$ |
| MVT for integrals | Continuous $f$ **attains** its average; proved by the IVT |
| Midpoint rule | $O(1/n^2)$ against $O(1/n)$ for left/right |

---

## Lecture 3 Exercises

**1.** Given $\int_0^3 f = 7$ and $\int_0^3 g = -2$, evaluate:
(a) $\int_0^3(2f+5g)$ (b) $\int_3^0 f$ (c) $\int_0^3(f-g)$

**2.** Evaluate without computing an antiderivative:
(a) $\int_{-4}^{4}x^5\,dx$ (b) $\int_{-1}^{1}x^2\cos x\,dx$ in terms of $\int_0^1 x^2\cos x\,dx$
(c) $\int_{-\pi}^{\pi}x^3\sin^2 x\,dx$

**3.** Given $\int_0^5 f = 12$ and $\int_0^2 f = 5$, find $\int_2^5 f$.

**4.** Use crude bounds to show $2 \le \int_1^3\sqrt{1+x^2}\,dx \le 2\sqrt{10}$.

**5.** Find the average value of $f(x)=x^2$ on $[0,2]$ and the point $c$ guaranteed by the MVT for
integrals. Then explain why the theorem fails for a step function.

### Answers

**1.** By linearity and orientation:

(a) $2(7)+5(-2)=14-10=\mathbf{4}$
(b) $-\int_0^3 f = \mathbf{-7}$
(c) $7-(-2)=\mathbf{9}$

**2.**

**(a) $\mathbf 0$.** $x^5$ is odd and $[-4,4]$ is symmetric about $0$. *(Verified in the analogous
case $\int_{-2}^2 x^3 = 1.63\times10^{-15}$, i.e. zero.)*

**(b) $\mathbf{2\int_0^1 x^2\cos x\,dx}$.** The product of two even functions ($x^2$ and $\cos x$) is
even, and the interval is symmetric.

**(c) $\mathbf 0$.** $x^3$ is odd, $\sin^2 x$ is even, and odd × even = **odd**. The interval
$[-\pi,\pi]$ is symmetric, so the integral vanishes.

*(c) is the discriminating part — students must track the parity through the product rather than
looking only at the leading factor.*

**3.** By additivity, $\int_0^5 f = \int_0^2 f + \int_2^5 f$, so

$$\int_2^5 f = 12 - 5 = \mathbf{7}$$

**4.** On $[1,3]$, $\sqrt{1+x^2}$ is increasing, so

$$m=\sqrt{1+1}=\sqrt2, \qquad M=\sqrt{1+9}=\sqrt{10}$$

With $b-a=2$:

$$\sqrt2\cdot 2 \le \int_1^3\sqrt{1+x^2}\,dx \le \sqrt{10}\cdot 2$$

Since $2\sqrt2 \approx 2.828 > 2$, the stated lower bound of $2$ follows *a fortiori*. The bounds are
$[2.828,\ 6.325]$; the true value is about $4.16$.

*Note this integrand has an antiderivative involving $\sinh^{-1}$, well beyond this course — which is
exactly the situation where crude bounds earn their keep.*

**5.** $f_{\text{avg}}=\dfrac{1}{2-0}\int_0^2 x^2\,dx = \dfrac{1}{2}\cdot\dfrac83 = \mathbf{\dfrac43}$
*(verified: $1.3333333333$)*.

The MVT guarantees $c\in(0,2)$ with $f(c)=\tfrac43$, i.e. $c^2=\tfrac43$, giving

$$c=\sqrt{4/3}=\mathbf{1.1547005384} \in (0,2) \ \checkmark$$

**Why it fails for a step function.** Take

$$f(x)=\begin{cases}0,& 0\le x<1\\ 1,& 1\le x\le 2\end{cases}$$

Then $\int_0^2 f = 1$ and $f_{\text{avg}}=\tfrac12$. But $f$ takes only the values $0$ and $1$ — it
**never equals $\tfrac12$**, so no such $c$ exists.

The theorem's proof runs through the **IVT**, which requires continuity. This step function has a
jump discontinuity at $x=1$ and skips the value $\tfrac12$ entirely — precisely the failure mode from
Week 2, Lecture 3.

---

*Next: Week 9, Monday — The Fundamental Theorem of Calculus, Part 1*
