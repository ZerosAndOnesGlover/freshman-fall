# MATH 141 · Calculus I
## Week 9 · Lecture 2 (Tuesday)
### The Fundamental Theorem, Part 2 — Evaluation

**Date:** Tuesday 24 November 2026 · 11:00–11:50 · Week 9

---

**Reading:** Stewart §5.3 | Spivak Ch. 14

---

## The Theorem That Makes Integration Possible

Monday proved **FTC Part 1**: the accumulation function
$G(x)=\int_a^x f(t)\,dt$ is an antiderivative of $f$, so **differentiation and integration are
inverse operations**.

Today's consequence is what you will actually use for the rest of your life.

> **FTC Part 2.** If $f$ is continuous on $[a,b]$ and $F$ is **any** antiderivative of $f$, then
> $$\int_a^b f(x)\,dx = F(b)-F(a)$$

Before this, computing $\int_0^3 x^2\,dx$ meant evaluating $\lim_{n\to\infty}\sum \left(\frac{3i}{n}\right)^2\frac3n$
— a genuine effort. Now it is $\frac{3^3}{3}-0 = 9$, in one line.

**Notation:** $\big[F(x)\big]_a^b$ or $F(x)\Big|_a^b$ both mean $F(b)-F(a)$.

---

## 1. Why It Follows from Part 1

Part 1 gives one antiderivative: $G(x)=\int_a^x f(t)\,dt$, with $G'=f$.

Let $F$ be **any** other antiderivative. Then $(F-G)'=f-f=0$, so by the Mean Value Theorem (Week 6)
$F-G$ is **constant**: $F(x)=G(x)+C$.

Now evaluate at both endpoints:

$$F(b)-F(a)=\big[G(b)+C\big]-\big[G(a)+C\big]=G(b)-G(a)=\int_a^b f - 0 = \int_a^b f \quad\blacksquare$$

**The constant cancels** — which is exactly why "any antiderivative" works and why the $+C$ that
matters so much for indefinite integrals is irrelevant here.

Note the proof uses the MVT. That is why Week 6 sits where it does.

---

## 2. Evaluation in Practice

Verified against numerical integration:

| Integral | $F(x)$ | $F(b)-F(a)$ | Numerical |
|---|---|---|---|
| $\int_0^3 x^2\,dx$ | $\tfrac{x^3}{3}$ | $9$ | $9.0000000000$ |
| $\int_0^\pi \sin x\,dx$ | $-\cos x$ | $2$ | $2.0000000000$ |
| $\int_0^2 e^x\,dx$ | $e^x$ | $e^2-1$ | $6.3890560989$ |
| $\int_1^e \frac1x\,dx$ | $\ln x$ | $1$ | $1.0000000000$ |
| $\int_0^{\pi/4}\sec^2x\,dx$ | $\tan x$ | $1$ | $1.0000000000$ |

Every one agrees to ten decimal places.

### The basic antiderivatives

| $f(x)$ | $F(x)$ |
|---|---|
| $x^n$, $n\ne-1$ | $\dfrac{x^{n+1}}{n+1}$ |
| $\dfrac1x$ | $\ln\lvert x\rvert$ |
| $e^x$ | $e^x$ |
| $\sin x$ | $-\cos x$ |
| $\cos x$ | $\sin x$ |
| $\sec^2 x$ | $\tan x$ |

Read the differentiation table (Week 4) backwards. **Every antiderivative you know is a derivative
you already knew.**

### Two traps

**The $n=-1$ exception.** $\int x^{-1}dx = \ln|x|$, not $\frac{x^0}{0}$. The power rule genuinely
fails there, and the absolute value matters because $1/x$ is defined for negative $x$ too.

**Discontinuity inside the interval invalidates the theorem.** Consider

$$\int_{-1}^{1}\frac{1}{x^2}\,dx \overset{?}{=} \left[-\frac1x\right]_{-1}^{1} = -1-1 = -2$$

That is **wrong**, and visibly so: $1/x^2 > 0$ everywhere, so the integral cannot be negative. The
FTC requires $f$ **continuous on $[a,b]$**, and $1/x^2$ has an infinite discontinuity at $0$. The
integral is in fact divergent.

**Always check the integrand is continuous on the whole interval before applying the FTC.** A
negative answer to an obviously positive integral is the usual symptom.

---

## 3. Net Change

Rewriting Part 2 with $F' = f$:

$$\int_a^b F'(x)\,dx = F(b)-F(a)$$

> **The integral of a rate of change is the net change.**

This is the single most useful reading of the theorem, and it reunites the whole course:

| $F$ | $F'$ | $\int_a^b F'$ |
|---|---|---|
| Position | velocity | **displacement** |
| Velocity | acceleration | change in velocity |
| Volume | flow rate | net volume added |
| Total cost | marginal cost | cost of units $a$ to $b$ |
| Population | growth rate | net population change |

### Displacement versus distance, resolved

Week 4 distinguished these by splitting at turning points. The FTC gives a cleaner statement:

$$\text{displacement}=\int_a^b v(t)\,dt, \qquad \text{distance}=\int_a^b \lvert v(t)\rvert\,dt$$

Verified with $v(t)=3t^2-12t+9$ on $[0,4]$, whose position is $s(t)=t^3-6t^2+9t$:

| | Value |
|---|---|
| $\int_0^4 v\,dt$ | $4.000000$ |
| $s(4)-s(0)$ | $4.000000$ ✓ |
| $\int_0^4 \lvert v\rvert\,dt$ | $12.000000$ |
| Hand check $\lvert s(1)-s(0)\rvert+\lvert s(3)-s(1)\rvert+\lvert s(4)-s(3)\rvert$ | $12.000000$ ✓ |

The absolute value is doing exactly what splitting-at-turning-points did in Week 4 — and it needs no
case analysis.

---

## 4. Average Value, Revisited

Week 8 defined $f_{\text{avg}}=\frac{1}{b-a}\int_a^b f$ but could not compute it. Now:

$$f_{\text{avg}}=\frac{F(b)-F(a)}{b-a}$$

which is the **average rate of change of $F$** — the slope of the secant.

Verified for $f(x)=x^2$ on $[0,2]$: $f_{\text{avg}}=\frac{1}{2}\cdot\frac83=1.3333333333$ ✓

> **Notice what this says.** The MVT for integrals asserts $f$ attains its average; the MVT for
> derivatives asserts $F'$ attains the secant slope of $F$. With $F'=f$ these are **the same
> statement**. Weeks 6 and 8 were proving the same theorem in two languages, and the FTC is the
> dictionary.

---

## Summary

| Idea | Takeaway |
|---|---|
| **FTC Part 2** | $\int_a^b f = F(b)-F(a)$ for **any** antiderivative $F$ |
| Why any $F$ works | Antiderivatives differ by a constant, which cancels |
| Proof needs | FTC Part 1 **and** the MVT (Week 6) |
| Notation | $\big[F(x)\big]_a^b$ |
| Antiderivative table | The Week 4 derivative table, read backwards |
| $\int x^{-1}$ | $\ln\lvert x\rvert$ — the power rule fails at $n=-1$ |
| **Continuity required** | $\int_{-1}^1 x^{-2}$ "$=-2$" is nonsense; check the interval first |
| **Net change** | $\int_a^b F' = F(b)-F(a)$ — the integral of a rate is the net change |
| Displacement | $\int v\,dt$ — verified $4$ |
| Distance | $\int\lvert v\rvert\,dt$ — verified $12$ |
| Average value | $\dfrac{F(b)-F(a)}{b-a}$, the secant slope of $F$ |

---

## Lecture 2 Exercises

**1.** Evaluate: (a) $\int_1^4\sqrt x\,dx$ (b) $\int_0^{\pi/2}\cos x\,dx$ (c) $\int_1^2\frac{3}{x}dx$
(d) $\int_{-1}^{1}(x^3+x)\,dx$

**2.** A student computes $\int_{-2}^{2}\frac{1}{x^2}dx=\left[-\frac1x\right]_{-2}^{2}=-1$. Identify
the error and state what is actually true.

**3.** Water flows into a tank at $r(t)=4t+3$ litres/minute. How much enters between $t=1$ and
$t=5$ minutes?

**4.** For $v(t)=t^2-4$ m/s on $[0,4]$, find the displacement and the total distance travelled.

**5.** Find the average value of $f(x)=\sin x$ on $[0,\pi]$, and the $c$ guaranteed by the MVT for
integrals.

### Answers

**1.**

**(a)** $\int_1^4 x^{1/2}dx=\left[\tfrac23x^{3/2}\right]_1^4=\tfrac23(8)-\tfrac23(1)=\mathbf{\tfrac{14}{3}}\approx4.6667$

**(b)** $\big[\sin x\big]_0^{\pi/2}=1-0=\mathbf 1$

**(c)** $3\big[\ln x\big]_1^2=3\ln 2 \approx \mathbf{2.0794}$

**(d)** $\mathbf 0$ — by symmetry, $x^3+x$ is **odd** on a symmetric interval (Week 8). Evaluating
directly also gives $\left[\tfrac{x^4}{4}+\tfrac{x^2}{2}\right]_{-1}^{1}=\tfrac34-\tfrac34=0$, but
the symmetry argument is faster and should be the first thought.

**2.** The error is applying the FTC to an integrand that is **not continuous on the interval**.
$\frac{1}{x^2}$ has an infinite discontinuity at $x=0 \in [-2,2]$, so the hypothesis fails and the
computation is meaningless.

**The tell:** $\frac{1}{x^2}>0$ everywhere it is defined, so any correct value must be **positive**.
A negative answer signals the error immediately.

**What is actually true:** the integral **diverges**. Splitting at the singularity,
$\int_0^2 x^{-2}dx=\lim_{\epsilon\to0^+}\left[-\tfrac1x\right]_\epsilon^2=\lim(\tfrac1\epsilon-\tfrac12)=+\infty$.

*This is the most important cautionary example of the week — check continuity before evaluating.*

**3.** By net change, the volume added is

$$\int_1^5(4t+3)\,dt=\big[2t^2+3t\big]_1^5=(50+15)-(2+3)=65-5=\mathbf{60}\text{ litres}$$

**4.** $v(t)=t^2-4=(t-2)(t+2)$, which is **negative** on $[0,2)$ and positive on $(2,4]$ — a genuine
sign change at $t=2$.

**Displacement:**
$$\int_0^4(t^2-4)dt=\left[\tfrac{t^3}{3}-4t\right]_0^4=\tfrac{64}{3}-16=\mathbf{\tfrac{16}{3}}\approx5.333\text{ m}$$

**Distance:** split at $t=2$, where $v$ changes sign.

*On $[0,2]$*, $v<0$, so the contribution is $\int_0^2(4-t^2)\,dt$:

$$\left[4t-\tfrac{t^3}{3}\right]_0^2 = 8-\tfrac83 = \tfrac{16}{3}$$

*On $[2,4]$*, $v>0$:

$$\left[\tfrac{t^3}{3}-4t\right]_2^4 = \left(\tfrac{64}{3}-16\right)-\left(\tfrac83-8\right)
= \tfrac{16}{3}+\tfrac{16}{3}=\tfrac{32}{3}$$

**Total distance** $=\dfrac{16}{3}+\dfrac{32}{3}=\dfrac{48}{3}=\mathbf{16}\text{ m}$.

*(Verified numerically: $\int_0^4\lvert v\rvert\,dt = 16.00000000$.)*

Note the two pieces are **not** equal — $\tfrac{16}{3}$ against $\tfrac{32}{3}$ — because the interval
lengths are equal but $|v|$ grows on the second. Adding them, not mistaking one for the total, is
where this problem is usually lost.

*The splitting is unavoidable here because $v$ genuinely changes sign — unlike Week 4's
$4t(t-3)^2$, where the double root meant no split was needed.*

**5.** $f_{\text{avg}}=\dfrac{1}{\pi}\int_0^\pi\sin x\,dx=\dfrac{1}{\pi}\big[-\cos x\big]_0^\pi
=\dfrac{1}{\pi}(1+1)=\mathbf{\dfrac{2}{\pi}}\approx0.6366$

*(Verified numerically: $\int_0^\pi \sin x\,dx = 2.0000000000$.)*

The MVT for integrals guarantees $c\in(0,\pi)$ with $\sin c=\tfrac2\pi$:

$$c=\arcsin\!\left(\tfrac2\pi\right)\approx\mathbf{0.6901}$$

*By symmetry $c=\pi-0.6901\approx2.4515$ works too — the theorem promises **at least one** such
point, not a unique one.*

---

*Next: Wednesday — Net Change, Accumulation, and Functions Defined by Integrals*
