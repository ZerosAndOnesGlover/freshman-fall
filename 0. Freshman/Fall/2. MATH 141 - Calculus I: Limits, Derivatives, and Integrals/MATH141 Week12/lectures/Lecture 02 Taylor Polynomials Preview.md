# MATH 141 · Calculus I
## Week 12 · Lecture 2 (Tuesday)
### Taylor Polynomials: A Preview

**Date:** Tuesday 15 December 2026 · 11:00–11:50 · Week 12

---

**Reading:** Stewart §11.10 (skim) | Spivak Ch. 20

---

## The Question

Your calculator computes $e^{0.7}$, $\sin(1.2)$, $\ln(3)$. **How?**

It cannot use the definitions — $e^x$ as a limit, $\sin x$ from a triangle — because a processor
does only addition and multiplication. So it must be evaluating a **polynomial**, and the polynomial
must be very close to the real function.

Constructing that polynomial is what this lecture is about. It is also where MATH 142 begins, so
this is a genuine preview rather than a coda.

---

## 1. The Idea: Match Derivatives

You have already built the simplest case. The **tangent line** at $a$,

$$L(x)=f(a)+f'(a)(x-a)$$

is the unique line agreeing with $f$ in **value and slope** at $a$. It is a degree-1 approximation.

Why stop at slope? Match the second derivative too, and the third, and so on. A polynomial of degree
$n$ has $n+1$ coefficients, so it can match $n+1$ conditions:

$$T_n(a)=f(a),\quad T_n'(a)=f'(a),\quad \dots,\quad T_n^{(n)}(a)=f^{(n)}(a)$$

> **Definition.** The **Taylor polynomial** of degree $n$ for $f$ about $a$ is
> $$T_n(x)=\sum_{k=0}^{n}\frac{f^{(k)}(a)}{k!}(x-a)^k$$
> $$=f(a)+f'(a)(x-a)+\frac{f''(a)}{2!}(x-a)^2+\cdots+\frac{f^{(n)}(a)}{n!}(x-a)^n$$
>
> When $a=0$ it is called a **Maclaurin polynomial**.

**Where the $k!$ comes from.** Differentiating $(x-a)^k$ exactly $k$ times gives $k!$, so dividing by
$k!$ makes the $k$-th derivative of that term equal $f^{(k)}(a)$ — exactly as required. Nothing
mysterious: it is Week 4's higher-derivative pattern, used backwards.

---

## 2. The Standard Examples

### $e^x$ about $0$

Every derivative of $e^x$ is $e^x$, so $f^{(k)}(0)=1$ for all $k$:

$$T_n(x)=1+x+\frac{x^2}{2!}+\frac{x^3}{3!}+\cdots+\frac{x^n}{n!}$$

Evaluated at $x=1$, this should approach $e=2.718281828459$. Verified:

| $n$ | $T_n(1)$ | error |
|---|---|---|
| $1$ | $2.000000000000$ | $7.18\times10^{-1}$ |
| $2$ | $2.500000000000$ | $2.18\times10^{-1}$ |
| $3$ | $2.666666666667$ | $5.16\times10^{-2}$ |
| $4$ | $2.708333333333$ | $9.95\times10^{-3}$ |
| $5$ | $2.716666666667$ | $1.62\times10^{-3}$ |
| $8$ | $2.718278769841$ | $3.06\times10^{-6}$ |
| $10$ | $2.718281801146$ | $2.73\times10^{-8}$ |

Ten terms give eight correct digits — and the terms are only additions, multiplications and
divisions by integers.

### $\sin x$ about $0$

The derivatives cycle $\sin\to\cos\to-\sin\to-\cos$ (Week 4), so at $0$ they are $0,1,0,-1,\dots$ —
**every even derivative vanishes**. Only odd powers survive:

$$T_n(x)=x-\frac{x^3}{3!}+\frac{x^5}{5!}-\frac{x^7}{7!}+\cdots$$

Verified at $x=0.5$, where $\sin(0.5)=0.479425538604$:

| $n$ | $T_n(0.5)$ | error |
|---|---|---|
| $1$ | $0.500000000000$ | $2.06\times10^{-2}$ |
| $3$ | $0.479166666667$ | $2.59\times10^{-4}$ |
| $5$ | $0.479427083333$ | $1.54\times10^{-6}$ |
| $7$ | $0.479425533234$ | $5.37\times10^{-9}$ |

**$T_1(x)=x$ is the small-angle approximation** $\sin x\approx x$ from physics — now revealed as
simply the first Taylor polynomial, with a quantifiable error.

---

## 3. Accuracy Depends on Distance from the Centre

A Taylor polynomial is built at **one point**, and it degrades as you move away. Verified for $e^x$:

| $x$ | $T_2$ error | $T_4$ error | $T_6$ error |
|---|---|---|---|
| $0.5$ | $2.37\times10^{-2}$ | $2.84\times10^{-4}$ | $1.65\times10^{-6}$ |
| $1.0$ | $2.18\times10^{-1}$ | $9.95\times10^{-3}$ | $2.26\times10^{-4}$ |
| $2.0$ | $2.39$ | $3.89\times10^{-1}$ | $3.35\times10^{-2}$ |
| $3.0$ | $11.6$ | $3.71$ | $6.73\times10^{-1}$ |

Reading **across**: more terms always help. Reading **down**: the same polynomial gets steadily worse
further from $0$.

**The practical consequence.** A library computing $e^x$ does not use one polynomial for all $x$. It
reduces the argument to a small range — writing $e^x = 2^k\cdot e^r$ with $r$ small — and uses a
polynomial only there. **Argument reduction is why a handful of terms suffices.**

---

## 4. The Error Term

The pattern above is not accidental.

> **Taylor's Theorem (Lagrange form).** If $f$ is $(n+1)$-times differentiable, then for some $c$
> between $a$ and $x$,
> $$f(x)-T_n(x)=\frac{f^{(n+1)}(c)}{(n+1)!}(x-a)^{n+1}$$

Two things to read from it:

**The error is $O\big((x-a)^{n+1}\big)$** — halving the distance from the centre cuts the error of
$T_n$ by a factor of $2^{n+1}$.

**The unknown $c$ is exactly the MVT's $c$.** Indeed $n=0$ gives $f(x)-f(a)=f'(c)(x-a)$ — the Mean
Value Theorem itself. **Taylor's theorem is the MVT generalised to higher order**, which is why
Week 6 keeps reappearing.

### Verifying the error order

For the linearisation of $\sqrt x$ at $a=4$, the error should be $O(\Delta x^2)$ with constant
$\approx\frac{\lvert f''(4)\rvert}{2}=\frac{1}{8\cdot4^{3/2}}=0.015625$. Verified:

| $\Delta x$ | error | error / $\Delta x^2$ |
|---|---|---|
| $0.1$ | $1.543\times10^{-4}$ | $0.01543$ |
| $0.2$ | $6.098\times10^{-4}$ | $0.01525$ |
| $0.4$ | $2.382\times10^{-3}$ | $0.01489$ |
| $0.8$ | $9.110\times10^{-3}$ | $0.01423$ |

The ratio is nearly constant and tends to $0.015625$ as $\Delta x\to0$ — exactly as predicted.

---

## 5. Polynomials Are Their Own Taylor Polynomials

If $f$ is a polynomial of degree $d$, then $f^{(k)}\equiv0$ for $k>d$ (Week 4), so $T_d=f$ **exactly**
— no error, at any $x$, about any centre.

Verified for $p(x)=2x^3-5x+1$ with $T_3$ centred at $a=1$:

| $x$ | $p(x)$ | $T_3(x)$ |
|---|---|---|
| $0$ | $1.000$ | $1.000$ |
| $1$ | $-2.000$ | $-2.000$ |
| $2$ | $7.000$ | $7.000$ |
| $5$ | $226.000$ | $226.000$ |
| $-3$ | $-38.000$ | $-38.000$ |

Exact everywhere, including far from the centre. Taylor expansion of a polynomial is just
**rewriting it in powers of $(x-a)$** — a change of basis, not an approximation.

---

## 6. What Comes Next

Letting $n\to\infty$ gives the **Taylor series**

$$f(x)=\sum_{k=0}^{\infty}\frac{f^{(k)}(a)}{k!}(x-a)^k$$

and immediately raises questions this course cannot answer: does the series converge? for which $x$?
does it converge to $f$? *(For $e^x$, $\sin x$ and $\cos x$: yes, everywhere. For others the radius
of convergence is finite, and there are functions whose Taylor series converges to the wrong thing.)*

Those are the subject of **MATH 142**.

---

## Summary

| Idea | Takeaway |
|---|---|
| $T_n$ matches $f$'s first $n$ derivatives at $a$ | The tangent line is $T_1$ |
| Formula | $T_n(x)=\sum_{k=0}^{n}\dfrac{f^{(k)}(a)}{k!}(x-a)^k$ |
| Why $k!$ | Differentiating $(x-a)^k$ $k$ times gives $k!$ |
| $e^x$ about $0$ | $\sum x^k/k!$ — verified $T_{10}(1)$ accurate to $2.7\times10^{-8}$ |
| $\sin x$ about $0$ | Odd powers only; $T_1=x$ is the small-angle approximation |
| Accuracy | Degrades with distance from the centre — verified across $x=0.5$ to $3$ |
| Argument reduction | Why libraries need only a few terms |
| Error term | $\dfrac{f^{(n+1)}(c)}{(n+1)!}(x-a)^{n+1}$ — verified $O(\Delta x^2)$ for $n=1$ |
| Taylor generalises the MVT | $n=0$ **is** the MVT |
| Polynomials | $T_d=f$ exactly — a change of basis |

---

## Lecture 2 Exercises

**1.** Find $T_3$ for $f(x)=e^x$ about $a=0$, and use it to estimate $e^{0.2}$.

**2.** Find $T_2$ for $f(x)=\sqrt x$ about $a=4$, and estimate $\sqrt{4.4}$.

**3.** Explain why the Maclaurin polynomial for $\cos x$ has only even powers.

**4.** Find $T_2$ for $f(x)=2x^3-5x+1$ about $a=1$. Is it equal to $f$? Why or why not?

**5.** The error of $T_1$ for $\sqrt x$ at $a=4$ behaves like $C(\Delta x)^2$. Predict $C$ from
Taylor's theorem and compare with the measured $0.01543$ at $\Delta x=0.1$.

### Answers

**1.** $T_3(x)=1+x+\dfrac{x^2}{2}+\dfrac{x^3}{6}$.

At $x=0.2$: $1+0.2+0.02+0.0013\overline{3}=\mathbf{1.221333\overline{3}}$.

True $e^{0.2}=1.221402758$; error $\approx6.9\times10^{-5}$.

**2.** $f(4)=2$, $f'(x)=\tfrac{1}{2\sqrt x}$ so $f'(4)=\tfrac14$, and
$f''(x)=-\tfrac{1}{4}x^{-3/2}$ so $f''(4)=-\tfrac{1}{32}$.

$$T_2(x)=2+\frac14(x-4)-\frac{1}{64}(x-4)^2$$

At $x=4.4$: $2+0.1-\frac{0.16}{64}=2+0.1-0.0025=\mathbf{2.0975}$.

True $\sqrt{4.4}=2.097617696$; error $\approx1.2\times10^{-4}$.

*(The linearisation alone gives $2.1$, with error $2.4\times10^{-3}$ — the quadratic term improves it
twentyfold.)*

**3.** $\cos x$ is an **even** function, and its derivatives at $0$ alternate
$1,0,-1,0,1,\dots$ — every **odd** derivative vanishes because it is $\pm\sin 0=0$.

Since $T_n$'s coefficients are $f^{(k)}(0)/k!$, all odd-power coefficients are zero:

$$T_n(x)=1-\frac{x^2}{2!}+\frac{x^4}{4!}-\cdots$$

*The general principle: an even function has only even powers, an odd function only odd powers.
$\sin x$ is odd and gets only odd powers, as verified in §2.*

**4.** $p(1)=-2$, $p'(x)=6x^2-5$ so $p'(1)=1$, $p''(x)=12x$ so $p''(1)=12$:

$$T_2(x)=-2+1(x-1)+\frac{12}{2}(x-1)^2=-2+(x-1)+6(x-1)^2$$

**No, $T_2\ne p$.** The degree is too low: $p$ is cubic, and $T_2$ can match only up to the second
derivative. The missing term is $\dfrac{p'''(1)}{3!}(x-1)^3=\dfrac{12}{6}(x-1)^3=2(x-1)^3$.

Adding it gives $T_3$, which **is** exactly $p$ — verified at $x=0,1,2,5,-3$, agreeing to every
digit.

*The rule: $T_n=f$ exactly when $f$ is a polynomial of degree $\le n$. Degree $d$ needs $n\ge d$.*

**5.** By Taylor's theorem with $n=1$, the error is
$\dfrac{f''(c)}{2!}(\Delta x)^2$ for some $c$ near $4$. So

$$C\approx\frac{\lvert f''(4)\rvert}{2}=\frac{1}{2}\cdot\frac{1}{4\cdot4^{3/2}}=\frac{1}{2\cdot32}=\mathbf{0.015625}$$

The measured ratio at $\Delta x=0.1$ is $0.01543$ — agreeing to about 1%. The remaining gap is
because $c$ lies strictly between $4$ and $4.1$, where $\lvert f''\rvert$ is slightly smaller than at
$4$. Verified: the ratio rises toward $0.015625$ as $\Delta x$ shrinks ($0.01423 \to 0.01489 \to
0.01525 \to 0.01543$).

*Full marks require both the prediction and the explanation of why the measured value is slightly
below it.*

---

*Next: Wednesday — Final Exam Preparation and the Road Ahead*
