# MATH 142 · Calculus II
## Week 9 · Lecture 3 (Wednesday)
### Functions as Power Series

---

**Reading:** Stewart §11.9 | Apostol Ch. 11 §11.5

---

## 1. Reading the Geometric Series Backwards

$$\sum_{n=0}^\infty x^n = \frac{1}{1-x}\qquad (|x|<1)$$

**Until now we read this left to right: a series, and here is its sum.** Read it right to left and it says something new:

> **The function $\dfrac{1}{1-x}$ *is* a power series on $(-1,1)$.**

**That is a representation of a function by an infinite polynomial**, and this lecture builds a small library of them from this single identity — using nothing but substitution, multiplication, differentiation and integration.

---

## 2. Why the Operations Are Legal

> **Theorem.** Let $f(x)=\sum c_n(x-a)^n$ have radius $R>0$. Then on $(a-R,a+R)$ the function $f$ is
> differentiable (hence continuous), and
>
> $$f'(x) = \sum_{n\ge1} nc_n(x-a)^{n-1}, \qquad \int f(x)\,dx = C+\sum_{n\ge0}\frac{c_n(x-a)^{n+1}}{n+1}$$
>
> **Both new series have the same radius $R$.**

**This is a genuinely strong statement.** Differentiating an infinite sum term by term is an interchange of two limits, and interchanging limits is exactly the sort of thing that usually fails.

> **What makes it work is absolute convergence.** Yesterday's §4: inside the radius, a power series
> converges absolutely — and Week 8 established that absolute convergence is the licence for
> rearranging and recombining terms. **The three weeks lock together here.**

**The radius is preserved, but the endpoints may change** — differentiating tends to lose them, integrating tends to gain them. Endpoints must be rechecked every time.

---

## 3. Building a Library

### Substitution

Replace $x$ by anything, provided you track the condition.

$$\frac{1}{1+x} = \frac{1}{1-(-x)} = \sum_{n=0}^\infty(-x)^n = \sum_{n=0}^\infty(-1)^nx^n \qquad(|x|<1)$$

$$\frac{1}{1+x^2} = \sum_{n=0}^\infty(-1)^nx^{2n}\qquad (|x^2|<1 \iff |x|<1)$$

$$\frac{1}{1-2x} = \sum_{n=0}^\infty 2^nx^n \qquad(|2x|<1\iff |x|<\tfrac12)$$

*(All verified.)*

> **Track the condition, not just the algebra.** The third has radius $\frac12$, not 1 — substituting
> $2x$ shrinks the interval.

### Multiplication by a power

$$\frac{x^3}{1-x} = x^3\sum_{n\ge0}x^n = \sum_{n\ge0}x^{n+3} \qquad(|x|<1)$$

**Radius unchanged.**

### Differentiation

$$\frac{d}{dx}\frac{1}{1-x} = \frac{1}{(1-x)^2} = \sum_{n\ge1}nx^{n-1} = 1+2x+3x^2+4x^3+\cdots$$

Multiplying by $x$:

$$\boxed{\sum_{n=1}^\infty nx^n = \frac{x}{(1-x)^2}}\qquad(|x|<1)$$

*(Verified — and a CAS confirms it with the side condition $-1<x<1$ attached, which is the radius doing its work.)*

**A closed form for a series that is not geometric**, obtained by differentiating one that is.

### Integration — the two important ones

**Integrating $\frac{1}{1+t}$ from 0 to $x$:**

$$\ln(1+x) = \int_0^x\frac{dt}{1+t} = \int_0^x\sum_{n\ge0}(-1)^nt^n\,dt = \sum_{n=0}^\infty\frac{(-1)^nx^{n+1}}{n+1}$$

$$\boxed{\ln(1+x) = x-\frac{x^2}{2}+\frac{x^3}{3}-\frac{x^4}{4}+\cdots = \sum_{n=1}^\infty\frac{(-1)^{n+1}x^n}{n}}$$

**Integrating $\frac{1}{1+t^2}$:**

$$\arctan x = \int_0^x\frac{dt}{1+t^2} = \sum_{n=0}^\infty\frac{(-1)^nx^{2n+1}}{2n+1}$$

$$\boxed{\arctan x = x-\frac{x^3}{3}+\frac{x^5}{5}-\frac{x^7}{7}+\cdots}$$

*(Both verified against the CAS's own expansions.)*

---

## 4. The Endpoints Change

Both new series have radius 1, but **integration gained an endpoint.**

$\frac{1}{1+x} = \sum(-1)^nx^n$ has interval $(-1,1)$ — divergent at both ends, since the terms do not tend to 0.

**After integrating**, $\ln(1+x) = \sum\frac{(-1)^{n+1}x^n}{n}$:

- **$x=1$:** $\sum\frac{(-1)^{n+1}}{n}$ — **converges** to $\ln2$.
- **$x=-1$:** $\sum\frac{(-1)^{n+1}(-1)^n}{n} = -\sum\frac1n$ — **diverges.** *(Verified: $-\infty$.)*

$$\text{Interval } (-1,1]$$

**The extra factor of $\frac1n$ from integrating was exactly enough to rescue one endpoint.**

> **This is why the endpoints must be rechecked after every operation.** They are not inherited.

---

## 5. Two Famous Consequences

**Setting $x=1$ in each boxed formula** — legitimate because each converges there:

$$\ln 2 = 1-\frac12+\frac13-\frac14+\cdots \qquad\qquad \frac\pi4 = 1-\frac13+\frac15-\frac17+\cdots$$

*(Both verified.)*

> **These are the two series from Week 8, and now you know where they come from.** They were not
> curiosities — they are $\ln(1+x)$ and $\arctan x$ evaluated at the edge of their intervals.

**And now their slowness is explained.** At $x=1$ you are sitting **exactly on the boundary of convergence**, where the geometric decay that makes a power series fast has entirely disappeared. **The terms only decay like $\frac1n$.**

**Inside the radius it is a different story.** To compute $\ln2$ instead as $-\ln(1-x)$ at $x=\frac12$:

| $x$ | terms for 10 digits |
|---|---|
| $0.5$ | $29$ |
| $0.9$ | $190$ |
| $0.99$ | $1{,}988$ |
| $0.999$ | $19{,}974$ |
| $1.0$ | **never** |

*(Measured.)*

**Twenty-nine terms at $x=\frac12$ against half a million at $x=1$.** **Where you evaluate a power series matters enormously**, and Week 10 makes systematic use of that.

---

## 6. Using the Library

Once you have a few series, new ones come from manipulation rather than from scratch.

### Example — a series for $\dfrac{x}{(1-2x)^2}$

Start from $\frac{1}{1-2x} = \sum2^nx^n$ ($|x|<\frac12$). Differentiate:

$$\frac{2}{(1-2x)^2} = \sum_{n\ge1}n2^nx^{n-1} \implies \frac{x}{(1-2x)^2} = \frac{x}{2}\sum_{n\ge1}n2^nx^{n-1} = \sum_{n\ge1}n2^{n-1}x^{n}$$

**Radius still $\frac12$.**

### Example — integrating something with no elementary antiderivative

$$\int\frac{\ln(1+x)}{x}\,dx = \int\sum_{n\ge1}\frac{(-1)^{n+1}x^{n-1}}{n}\,dx = \sum_{n=1}^\infty\frac{(-1)^{n+1}x^n}{n^2}+C$$

**The integrand has no elementary antiderivative**, yet the series representation integrates in one line.

> **This is the technique that finally answers Week 0.** $\int e^{-x^2}dx$ has no elementary
> antiderivative — but expand $e^{-x^2}$ as a power series and integrate term by term, and you get a
> perfectly good series for it. **Week 10 does exactly that.**

---

## 7. What To Take From This Lecture

1. **$\frac{1}{1-x} = \sum x^n$ read backwards is a function represented by a series.**
2. **Term-by-term differentiation and integration are valid inside the radius**, and the radius is preserved.
3. **They are valid because convergence is absolute there** — Week 8's licence.
4. **Endpoints are not preserved.** Recheck them after every operation.
5. **Substitution changes the radius**; track the condition.
6. **Where you evaluate matters:** 29 terms at $x=\frac12$ against never at $x=1$.

---

## Looking Ahead

This week has been about series that **happen** to add up to familiar functions. **Week 10 reverses the question:**

> Given a function $f$, can we *construct* a power series that equals it — and how do we know?

The construction is **Taylor's formula**, $c_n = \frac{f^{(n)}(a)}{n!}$, and the guarantee is **Taylor's theorem with remainder**, which bounds the error of a truncation.

**That is the climax of the course**, and it is how every numerical library evaluates every transcendental function you have ever called.

---

*Next: Week 10, Monday — Taylor and Maclaurin Series*
