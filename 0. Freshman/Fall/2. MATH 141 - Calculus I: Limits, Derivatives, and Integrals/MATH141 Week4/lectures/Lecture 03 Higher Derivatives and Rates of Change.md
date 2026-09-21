# MATH 141 · Calculus I
## Week 4 · Lecture 3 (Wednesday)
### Higher Derivatives and Rates of Change

**Date:** Wednesday 21 October 2026 · 11:00–11:50 · Week 4

---

**Reading:** Stewart §2.7, §3.7 | Spivak Ch. 10

---

## What the Rules Are For

Monday and Tuesday gave the machinery: power, product, quotient, chain. Applied mechanically they
turn any elementary formula into its derivative. This lecture is about what those derivatives
*mean* — and about differentiating repeatedly.

---

## 1. Higher Derivatives

$f'$ is a function (Week 3, Lecture 2), so it can be differentiated again:

$$f'' = (f')', \qquad f''' = (f'')', \qquad f^{(n)} = \big(f^{(n-1)}\big)'$$

Beyond the third, primes become unreadable and we write $f^{(4)}, f^{(5)}, \dots$ — with parentheses,
because $f^4$ would mean the fourth power.

In Leibniz notation:

$$\frac{d^2y}{dx^2}, \qquad \frac{d^3y}{dx^3}, \qquad \frac{d^ny}{dx^n}$$

Verified against numerical differentiation:

| $f$ | at $x$ | $f'$ numerical / exact | $f''$ numerical / exact |
|---|---|---|---|
| $x^5$ | $2$ | $80.000000$ / $80$ | $160.000002$ / $160$ |
| $\sin x$ | $1$ | $0.540302$ / $\cos 1$ | $-0.841471$ / $-\sin 1$ |
| $e^x$ | $1$ | $2.718282$ / $e$ | $2.718282$ / $e$ |
| $\ln x$ | $2$ | $0.500000$ / $\tfrac12$ | $-0.250000$ / $-\tfrac14$ |

*(The tiny error in $f''$ for $x^5$ — $160.000002$ against $160$ — is the second-difference
approximation, not the calculus. Numerical second derivatives amplify rounding error by $1/h^2$,
which is why $h=10^{-4}$ is used rather than $10^{-8}$.)*

### Patterns worth knowing

**Powers terminate.** For $f(x)=x^k$,

$$f^{(n)}(x)=\frac{k!}{(k-n)!}\,x^{\,k-n} \quad (n \le k), \qquad f^{(n)} \equiv 0 \quad (n > k)$$

Verified for $k=5$: the successive derivatives are $5x^4$, $20x^3$, $60x^2$, $120x$, $120$, then
$\mathbf 0$. A degree-$k$ polynomial dies at the $(k+1)$-th derivative — the fact that makes Taylor
polynomials of polynomials exact (Week 12).

**Exponentials are fixed.** $\dfrac{d^n}{dx^n}e^x = e^x$ for every $n$. This is essentially the
*definition* of $e$, and it is why $e^x$ appears in every differential equation you will meet.

**Sine and cosine cycle with period 4.**

$$\sin x \to \cos x \to -\sin x \to -\cos x \to \sin x$$

Verified at $x=0.7$: $+0.6442,\ +0.7648,\ -0.6442,\ -0.7648$ — the values repeat with signs
alternating in pairs. So $\dfrac{d^{n}}{dx^{n}}\sin x$ depends only on $n \bmod 4$.

---

## 2. Motion: Position, Velocity, Acceleration

The classical interpretation, and the one that gives $f''$ its meaning.

If $s(t)$ is position at time $t$:

| Quantity | Meaning | Sign tells you |
|---|---|---|
| $s(t)$ | position | where it is |
| $v(t)=s'(t)$ | **velocity** | direction of travel |
| $a(t)=s''(t)$ | **acceleration** | whether speed is increasing |
| $\lvert v(t)\rvert$ | **speed** | how fast, ignoring direction |

**Velocity and speed are different.** Velocity is signed; speed is its magnitude. An object moving
left at $3$ m/s has velocity $-3$ and speed $3$.

### Worked example

$$s(t)=t^3-6t^2+9t \quad\text{(metres, } t \text{ in seconds)}$$

$$v(t)=3t^2-12t+9=3(t-1)(t-3), \qquad a(t)=6t-12$$

Verified:

| $t$ | $s(t)$ | $v(t)$ | $a(t)$ | |
|---|---|---|---|---|
| $0$ | $0.00$ | $9.00$ | $-12.00$ | moving right, decelerating |
| $1$ | $4.00$ | $0.00$ | $-6.00$ | **turning point** |
| $2$ | $2.00$ | $-3.00$ | $0.00$ | moving left, acceleration changes sign |
| $3$ | $0.00$ | $0.00$ | $6.00$ | **turning point** |
| $4$ | $4.00$ | $9.00$ | $12.00$ | moving right, accelerating |

The object starts at the origin moving right, stops at $t=1$ having reached $s=4$, reverses and
travels left to $s=0$ at $t=3$, then reverses again.

**Displacement versus distance.** Over $[0,4]$:

- **Displacement** $= s(4)-s(0) = 4 - 0 = \mathbf{4}$ m — net change in position.
- **Distance travelled** $= |s(1)-s(0)| + |s(3)-s(1)| + |s(4)-s(3)| = 4 + 4 + 4 = \mathbf{12}$ m.

Verified. They differ because the object reversed direction twice, and you must split the interval
at every point where $v=0$ to compute distance. This distinction returns in Week 9 as the difference
between $\int v\,dt$ and $\int |v|\,dt$.

### Speeding up or slowing down?

The object is **speeding up when $v$ and $a$ have the same sign** and slowing down when they differ.
Not "when $a>0$" — that is a common error.

At $t=2$: $v=-3$ (moving left), $a=0$ turning positive, so shortly after $t=2$ the velocity is
negative and acceleration positive — **slowing down** while still moving left.

---

## 3. Rates of Change in General

The derivative is a **rate of change**, whatever the variables. The units come along for the ride:
if $y$ is in units $U$ and $x$ in units $V$, then $\dfrac{dy}{dx}$ is in $U$ per $V$.

| Context | $f$ | $f'$ means |
|---|---|---|
| Motion | position (m) | velocity (m/s) |
| Biology | population | growth rate (individuals/year) |
| Chemistry | concentration | reaction rate (mol L⁻¹ s⁻¹) |
| Economics | total cost $C(q)$ | **marginal cost** (currency/unit) |
| Thermodynamics | temperature | heating rate (K/s) |
| **CS** | work completed | throughput (items/s) |

### Marginal cost

In economics, **marginal cost** is defined as the cost of producing one more unit,
$C(q+1)-C(q)$ — but is *computed* as $C'(q)$, because the derivative is easier and the difference is
small when $q$ is large.

Verified for $C(q)=0.01q^3-0.6q^2+13q+100$:

| $q$ | $C'(q)$ | $C(q+1)-C(q)$ | difference |
|---|---|---|---|
| $10$ | $4.000$ | $3.710$ | $0.290$ |
| $20$ | $1.000$ | $1.010$ | $0.010$ |
| $30$ | $4.000$ | $4.310$ | $0.310$ |
| $40$ | $13.000$ | $13.610$ | $0.610$ |

The agreement is good but **not exact**, and the error grows with $|C''|$ — the derivative is the
*instantaneous* rate, while the true marginal cost is a difference over a unit step. For a locally
straight cost curve they nearly coincide; for a sharply curving one they do not.

> **This is the linear-approximation idea**, which Week 6 develops properly:
> $C(q+1) \approx C(q) + C'(q)$, with error controlled by $C''$.

---

## Summary

| Idea | Takeaway |
|---|---|
| $f^{(n)}$ | Differentiate $n$ times; write $f^{(4)}$, not $f^4$ |
| $\dfrac{d^n}{dx^n}x^k$ | $\dfrac{k!}{(k-n)!}x^{k-n}$, then $\mathbf 0$ once $n>k$ |
| $\dfrac{d^n}{dx^n}e^x$ | $e^x$ — fixed under differentiation |
| $\dfrac{d^n}{dx^n}\sin x$ | Cycles with **period 4** |
| $s \to v \to a$ | Position, velocity, acceleration |
| Velocity vs speed | Signed vs magnitude |
| **Displacement vs distance** | $4$ m vs $12$ m in the worked example — split at every $v=0$ |
| Speeding up | When $v$ and $a$ share a sign — **not** when $a>0$ |
| Derivative = rate of change | Units are $U$ per $V$ |
| Marginal cost | $C'(q) \approx C(q+1)-C(q)$; error grows with $\lvert C''\rvert$ |

---

## Lecture 3 Exercises

**1.** Find $f'$, $f''$ and $f'''$ for (a) $f(x)=x^4-3x^2+7$ (b) $f(x)=\sin x$ (c) $f(x)=\ln x$.

**2.** For $s(t)=t^3-6t^2+9t$ on $[0,4]$, find (a) when the object is at rest, (b) its displacement,
(c) the total distance travelled.

**3.** A particle has $v(t)=-3$ and $a(t)=+2$ at some instant. Is it speeding up or slowing down?
Explain.

**4.** Find $\dfrac{d^{100}}{dx^{100}}\big[\sin x\big]$ and $\dfrac{d^{7}}{dx^{7}}\big[x^5\big]$.

**5.** For $C(q)=0.01q^3-0.6q^2+13q+100$, compute $C'(20)$ and $C(21)-C(20)$. Explain why they differ
and what controls the size of the discrepancy.

### Answers

**1.**

| | $f'$ | $f''$ | $f'''$ |
|---|---|---|---|
| **(a)** $x^4-3x^2+7$ | $4x^3-6x$ | $12x^2-6$ | $24x$ |
| **(b)** $\sin x$ | $\cos x$ | $-\sin x$ | $-\cos x$ |
| **(c)** $\ln x$ | $x^{-1}$ | $-x^{-2}$ | $2x^{-3}$ |

*(For (c), note the pattern $f^{(n)}=(-1)^{n-1}(n-1)!\,x^{-n}$ for $n\ge1$. Verified at $x=2$:
$f'=0.5$, $f''=-0.25$.)*

**2.** $v(t)=3t^2-12t+9=3(t-1)(t-3)$.

**(a) At rest** when $v=0$: $t=\mathbf{1}$ and $t=\mathbf{3}$ seconds.

**(b) Displacement** $= s(4)-s(0) = 4-0 = \mathbf{4}$ m.

**(c) Distance.** Split at the turning points:

$$|s(1)-s(0)| + |s(3)-s(1)| + |s(4)-s(3)| = |4-0| + |0-4| + |4-0| = 4+4+4 = \mathbf{12}\text{ m}$$

Verified. *The whole point is that (b) and (c) differ: integrating velocity gives displacement, and
you must take absolute values — or split the interval — to get distance.*

**3. Slowing down.**

$v=-3$ and $a=+2$ have **opposite signs**. The acceleration opposes the motion, so the *speed*
$|v|=3$ is decreasing even though the velocity is increasing (from $-3$ toward $0$).

*The common error is answering "speeding up because $a>0$". Acceleration positive means velocity is
increasing; when velocity is negative, increasing it moves it toward zero — which is slowing down.
The correct test is whether $v$ and $a$ share a sign.*

**4.** **$\dfrac{d^{100}}{dx^{100}}\sin x = \sin x$.** The derivatives cycle with period 4, and
$100 \equiv 0 \pmod 4$, so the 100th derivative is the 0th — the function itself.

**$\dfrac{d^{7}}{dx^{7}}x^5 = \mathbf{0}$.** Verified: the derivatives of $x^5$ run
$5x^4, 20x^3, 60x^2, 120x, 120$, and the sixth is already $0$. Since $7 > 5$, so is the seventh.

**5.** $C'(q)=0.03q^2-1.2q+13$, so $C'(20)=0.03(400)-24+13=12-24+13=\mathbf{1.000}$.

$C(21)-C(20)=\mathbf{1.010}$ (verified). They differ by $0.010$.

**Why:** $C'(20)$ is the **instantaneous** rate of change at $q=20$ — the slope of the tangent. The
true marginal cost $C(21)-C(20)$ is the **average** rate over a unit step. They agree only if $C$ is
linear on $[20,21]$.

**What controls the discrepancy:** the second derivative. By the linear approximation,

$$C(q+1) \approx C(q) + C'(q) + \tfrac12 C''(q)$$

so the error is about $\tfrac12 C''(q)$. Here $C''(q)=0.06q-1.2$, giving $C''(20)=0$ — which is why
the agreement at $q=20$ is unusually good ($0.010$). Compare $q=40$, where $C''=1.2$ and the
discrepancy grows to $0.610$, as the verified table shows.

*Full marks require identifying $C''$ as the controlling quantity, not merely saying "they're
approximations".*

---

*Next: Week 5, Monday — Implicit Differentiation*
