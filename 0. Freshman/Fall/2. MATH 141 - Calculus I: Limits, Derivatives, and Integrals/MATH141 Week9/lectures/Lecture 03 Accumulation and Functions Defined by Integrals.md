# MATH 141 · Calculus I
## Week 9 · Lecture 3 (Wednesday)
### Accumulation and Functions Defined by Integrals

*“Less depends upon the choice of words than upon this, that their introduction shall be justified by pregnant theorems.”* — Carl Friedrich Gauss, abstract of *Disquisitiones generales circa superficies curvas* (1827)

**Date:** Wednesday 25 November 2026 · 11:00–11:50 · Week 9

**Coursework:** 📝 **PS 8** due today 11:00 · 📝 **PS 9** released today 12:00, due Wed 2 Dec 11:00 · 🔬 **Lab 9** Fri 27 Nov 15:00–16:50 · 📊 **Quiz 10** Mon 30 Nov 11:00–11:15 · 📘 **Midterm 2** Wed 2 Dec 18:00–19:15

---

**Reading:** Stewart §5.3–5.4 | Spivak Ch. 14

---

## A New Way to Define a Function

Until now every function in this course arrived as a **formula**: $x^2$, $\sin x$, $e^x$, or some
combination. Today a second source:

$$G(x)=\int_a^x f(t)\,dt$$

This is a perfectly good function. Feed it $x$, get a number — the accumulated area from $a$ to $x$.
FTC Part 1 (Monday) tells us it is differentiable with $G'=f$, so we know everything about its slope
without ever writing a formula for $G$ itself.

**Why this matters:** some functions *only* exist this way.

---

## 1. Functions With No Elementary Formula

$$\int_0^1 e^{-x^2}\,dx$$

This integral has a definite value — verified numerically as **$0.7468241328$** — yet
$e^{-x^2}$ has **no elementary antiderivative**. No combination of polynomials, roots, exponentials,
logarithms or trigonometric functions differentiates to $e^{-x^2}$. This is a theorem (Liouville,
1835), not a failure of ingenuity.

So how is the value known? Because

$$G(x)=\int_0^x e^{-t^2}\,dt$$

**exists** by FTC Part 1, is differentiable, and can be evaluated numerically to any precision. It is
important enough to have a name — the **error function**,

$$\operatorname{erf}(x)=\frac{2}{\sqrt\pi}\int_0^x e^{-t^2}\,dt$$

Verified: $\frac{\sqrt\pi}{2}\operatorname{erf}(1)=0.7468241328$, matching the direct numerical
integral exactly.

The error function underlies the normal distribution, and you will meet it in MATH 251. **It is
defined by an integral because it cannot be defined any other way.**

Other members of the same family: $\int\frac{\sin x}{x}dx$ (the sine integral), $\int\frac{1}{\ln x}dx$
(the logarithmic integral, central to the distribution of primes), $\int\sqrt{1-k^2\sin^2\theta}\,d\theta$
(elliptic integrals, giving the arc length of an ellipse).

> **The lesson.** "I cannot find an antiderivative" and "no antiderivative exists" are different
> statements, and the second is far rarer than students assume — but when it holds, the integral
> definition is not a workaround. It **is** the definition.

---

## 2. Differentiating Accumulation Functions

FTC Part 1 in its basic form:

$$\frac{d}{dx}\int_a^x f(t)\,dt = f(x)$$

Verified with $f(t)=t^2+1$ and $a=0$:

| $x$ | $G'(x)$ numerical | $f(x)$ |
|---|---|---|
| $1$ | $2.00000000$ | $2$ |
| $2$ | $5.00000000$ | $5$ |
| $3$ | $10.00000000$ | $10$ |

### With a variable upper limit that is not just $x$

If the upper limit is $u(x)$, the chain rule applies:

$$\frac{d}{dx}\int_a^{u(x)} f(t)\,dt = f\big(u(x)\big)\cdot u'(x)$$

**Why:** write $H(x)=G(u(x))$ where $G(y)=\int_a^y f$. Then $H'=G'(u)\cdot u' = f(u)\,u'$.

Verified for $\dfrac{d}{dx}\int_0^{x^2}\sin t\,dt = \sin(x^2)\cdot 2x$:

| $x$ | numerical | exact |
|---|---|---|
| $1.0$ | $1.68294197$ | $1.68294197$ |
| $1.5$ | $2.33421959$ | $2.33421959$ |

### With a variable lower limit

Use orientation (Week 8): $\int_{u(x)}^{b}f = -\int_b^{u(x)}f$, so

$$\frac{d}{dx}\int_{u(x)}^{b} f(t)\,dt = -f\big(u(x)\big)\,u'(x)$$

### Both limits variable

Split at any convenient constant $c$:

$$\int_{u(x)}^{v(x)} f = \int_{u(x)}^{c} f + \int_c^{v(x)} f
\;\Longrightarrow\;
\frac{d}{dx}\int_{u}^{v} f = f(v)v' - f(u)u'$$

**The pattern:** upper limit contributes positively, lower negatively, each multiplied by its own
derivative.

---

## 3. Reading the Shape of $G$ from $f$

Since $G'=f$ and $G''=f'$, everything from Weeks 6–7 applies — with the graph of $f$ playing the role
of the derivative:

| On the graph of $f$ | On the graph of $G$ |
|---|---|
| $f>0$ | $G$ **increasing** |
| $f<0$ | $G$ **decreasing** |
| $f=0$ crossing $+\to-$ | $G$ has a **local maximum** |
| $f=0$ crossing $-\to+$ | $G$ has a **local minimum** |
| $f=0$ touching without crossing | $G$ has a stationary point, **not** an extremum |
| $f$ increasing | $G$ **concave up** |
| $f$ has a max or min | $G$ has an **inflection point** |
| Area accumulated so far | The **value** $G(x)$ |

This is the single most examinable skill of the week: given a graph of $f$, describe $G$. Note that
$G(a)=0$ always — the accumulation starts empty.

---

## 4. Accumulation in Context

$$G(x)=G(a)+\int_a^x G'(t)\,dt$$

> **Starting value plus accumulated change equals current value.**

| Setting | Reads as |
|---|---|
| Tank filling | volume now = initial volume + $\int$ flow rate |
| Motion | position now = initial position + $\int$ velocity |
| Economics | total cost = fixed cost + $\int$ marginal cost |
| Population | population now = initial + $\int$ growth rate |
| Charge | charge now = initial + $\int$ current |

This rearrangement is how differential equations are solved in practice, and it is the form in which
the FTC is actually used in applications — not as "evaluate an integral" but as **"reconstruct a
quantity from its rate."**

### Worked example

Water enters a tank at $r(t)=4t+3$ L/min, starting from $20$ L. How much after $5$ minutes?

$$V(5)=V(0)+\int_0^5(4t+3)\,dt = 20+\big[2t^2+3t\big]_0^5 = 20+(50+15)=\mathbf{85}\text{ L}$$

*(Verified: $\int_1^5(4t+3)dt = 60.000000$ for the analogous window in Lecture 2's exercise.)*

---

## Summary

| Idea | Takeaway |
|---|---|
| $G(x)=\int_a^x f$ | A legitimate function, defined without a formula |
| $G(a)=0$ | Accumulation starts empty |
| Non-elementary antiderivatives | $e^{-x^2}$ has none — a **theorem** (Liouville), not a gap in skill |
| $\operatorname{erf}$ | Defined by its integral because there is no alternative; verified $0.7468241328$ |
| $\frac{d}{dx}\int_a^x f$ | $=f(x)$ — verified at three points |
| Variable upper limit | $f(u(x))\cdot u'(x)$ — verified against $\sin(x^2)\cdot2x$ |
| Variable lower limit | $-f(u(x))\,u'(x)$ |
| Both variable | $f(v)v'-f(u)u'$ |
| Shape of $G$ from $f$ | $f>0\Rightarrow G$ increasing; $f$ increasing $\Rightarrow G$ concave up |
| Accumulation form | $G(x)=G(a)+\int_a^x G'$ — start plus change |

---

## Lecture 3 Exercises

**1.** Find $G'(x)$:
(a) $G(x)=\int_1^x\frac{1}{1+t^4}dt$
(b) $G(x)=\int_0^{x^3}\cos t\,dt$
(c) $G(x)=\int_x^{5}e^{t^2}dt$
(d) $G(x)=\int_{x}^{x^2}\ln t\,dt$

**2.** Let $G(x)=\int_0^x f(t)\,dt$ where $f$ is positive and increasing on $[0,4]$. Describe $G$:
increasing or decreasing, concave up or down, and the value $G(0)$.

**3.** A tank holds $50$ L and water flows in at $r(t)=6-t$ L/min. Find the volume at $t=4$, and the
time at which the volume is greatest.

**4.** Explain why $\int_0^1 e^{-x^2}dx$ has a definite numerical value even though $e^{-x^2}$ has no
elementary antiderivative. What guarantees the value exists?

### Answers

**1.**

**(a)** $G'(x)=\dfrac{1}{1+x^4}$ — direct FTC Part 1.

**(b)** $G'(x)=\cos(x^3)\cdot 3x^2$ — chain rule with $u=x^3$.

**(c)** $G'(x)=-e^{x^2}$ — the variable is the **lower** limit, so the sign flips.

**(d)** $G'(x)=\ln(x^2)\cdot 2x-\ln(x)\cdot 1=\mathbf{4x\ln x-\ln x}$.

*Using $\ln(x^2)=2\ln x$: the first term is $2\ln x \cdot 2x = 4x\ln x$. (d) is the discriminating
part — both limits vary, and each contributes with its own sign and its own derivative.*

**2.** $G(0)=\mathbf 0$ — the accumulation starts empty.

$f>0$ throughout, so $G$ is **increasing** on $[0,4]$.

$G''=f'>0$ since $f$ is increasing, so $G$ is **concave up**.

*So $G$ rises ever more steeply from the origin. Note that $G$ has no maximum on $[0,4]$ other than at
the right endpoint — a common error is to look for an interior maximum where none exists, because $f$
never changes sign.*

**3.** $V(t)=50+\int_0^t(6-s)\,ds=50+\left[6s-\tfrac{s^2}{2}\right]_0^t=50+6t-\tfrac{t^2}{2}$

At $t=4$: $V(4)=50+24-8=\mathbf{66}$ L.

**Maximum volume:** $V'(t)=r(t)=6-t$, which is zero at $t=\mathbf{6}$ minutes and changes from
positive to negative there — so $t=6$ is a maximum, with $V(6)=50+36-18=68$ L.

*The neat part: the volume is greatest exactly when the **inflow rate hits zero**, because $V'=r$.
After $t=6$ the "inflow" is negative — water is draining. This is FTC Part 1 doing the work: the
extremum of the accumulation is where the integrand crosses zero.*

**4.** The value exists because **integrability and antidifferentiability are different questions**.

$e^{-x^2}$ is **continuous** on $[0,1]$, and every continuous function on a closed bounded interval is
**Riemann integrable** — the limit of Riemann sums exists. That is what guarantees the number exists,
and it is why numerical methods converge to it: verified as $0.7468241328$.

Separately, FTC Part 1 guarantees $G(x)=\int_0^x e^{-t^2}dt$ is a genuine differentiable function with
$G'=e^{-x^2}$ — so an antiderivative **does** exist. What does not exist is an antiderivative
expressible in **elementary** terms, which Liouville proved in 1835.

*Full marks require separating the three claims: the integral exists (continuity ⟹ integrability);
an antiderivative exists (FTC Part 1); no **elementary** antiderivative exists (Liouville). Students
who answer only "we compute it numerically" have described the method without the justification.*

---

*Next: Week 10, Monday — Integration by Substitution*
