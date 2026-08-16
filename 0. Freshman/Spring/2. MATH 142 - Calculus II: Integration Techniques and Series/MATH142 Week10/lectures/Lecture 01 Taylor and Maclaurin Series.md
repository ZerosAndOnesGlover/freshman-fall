# MATH 142 · Calculus II
## Week 10 · Lecture 1 (Monday)
### Taylor and Maclaurin Series

**Date:** Monday 22 March 2027 · 11:00–11:50 · Week 10

---

**Reading:** Stewart §11.10 | Apostol Ch. 11 §11.6–11.8
**Quiz 10** — this Monday, **covers Week 9** (power series, radius, interval of convergence)
**Midterm 2 this week** — covering Weeks 5–9. See the revision guide in `resources/`.

---

## 1. The Coefficients Are Forced

**Suppose** $f$ has a power series representation near $a$:

$$f(x) = c_0+c_1(x-a)+c_2(x-a)^2+c_3(x-a)^3+\cdots$$

**What must the $c_n$ be?** Differentiate repeatedly — legal inside the radius, by Week 9 — and set $x=a$ each time.

| | | at $x=a$ |
|---|---|---|
| $f(x)$ | $=c_0+c_1(x-a)+\cdots$ | $f(a) = c_0$ |
| $f'(x)$ | $=c_1+2c_2(x-a)+\cdots$ | $f'(a) = c_1$ |
| $f''(x)$ | $=2c_2+6c_3(x-a)+\cdots$ | $f''(a) = 2c_2$ |
| $f'''(x)$ | $=6c_3+\cdots$ | $f'''(a) = 6c_3$ |

**Each differentiation kills the constant term and exposes the next coefficient.** In general $f^{(n)}(a) = n!\,c_n$, so

$$\boxed{c_n = \frac{f^{(n)}(a)}{n!}}$$

> **The coefficients are not chosen — they are determined.** If a power series representation exists
> at all, this is the only one it can be. **Uniqueness comes for free from the derivation.**

### Definition

$$\textbf{Taylor series of } f \textbf{ at } a: \qquad \sum_{n=0}^\infty\frac{f^{(n)}(a)}{n!}(x-a)^n$$

$$\textbf{Maclaurin series}: \qquad a = 0$$

**The truncation at degree $n$ is the Taylor polynomial $P_n$**, and $P_1$ is the tangent line you met in MATH 141. **Taylor's series is the tangent line idea taken to its limit.**

---

## 2. ⚠ Two Things That Can Go Wrong

> **Having a Taylor series is not the same as being equal to it.**

**(a) The series may not converge** anywhere except $x=a$. Week 9's $\sum n!x^n$ has $R=0$.

**(b) It may converge to the wrong thing.** Tomorrow's lecture treats

$$f(x) = \begin{cases}e^{-1/x^2}&x\ne0\\0&x=0\end{cases}$$

whose derivatives at 0 are **all zero**, so its Maclaurin series is identically 0 — **converging everywhere, to a function that is not $f$.**

**So a Taylor series is a candidate, not a guarantee.** Tomorrow's remainder theorem is what turns one into the other.

---

## 3. Deriving the Standard Library

Four series carry almost all the weight. **Derive each once, then never again.**

### $e^x$

Every derivative is $e^x$, so $f^{(n)}(0)=1$:

$$\boxed{e^x = \sum_{n=0}^\infty\frac{x^n}{n!} = 1+x+\frac{x^2}{2!}+\frac{x^3}{3!}+\cdots}\qquad R=\infty$$

*(Verified.)* **$R=\infty$** because $\left|\frac{c_{n+1}}{c_n}\right| = \frac{1}{n+1}\to0$ (Week 9).

### $\sin x$

Derivatives at 0 cycle $0,1,0,-1,0,1,\ldots$, so only odd powers survive:

$$\boxed{\sin x = \sum_{n=0}^\infty\frac{(-1)^nx^{2n+1}}{(2n+1)!} = x-\frac{x^3}{3!}+\frac{x^5}{5!}-\cdots}\qquad R=\infty$$

### $\cos x$

$$\boxed{\cos x = \sum_{n=0}^\infty\frac{(-1)^nx^{2n}}{(2n)!} = 1-\frac{x^2}{2!}+\frac{x^4}{4!}-\cdots}\qquad R=\infty$$

*(Both verified.)*

**Note $\sin$ is odd and its series has only odd powers; $\cos$ is even and has only even powers.** That is not a coincidence — **a function's symmetry is visible in its series**, and it is a free check on your work.

**Also note these have missing terms**, so Week 9's warning applies: find their radius from the terms, not the coefficient formula.

### The binomial series

For any real $k$:

$$\boxed{(1+x)^k = \sum_{n=0}^\infty\binom{k}{n}x^n},\qquad \binom kn = \frac{k(k-1)\cdots(k-n+1)}{n!}, \qquad R=1$$

**When $k$ is a non-negative integer this terminates** and is the ordinary binomial theorem. **For any other $k$ it is an infinite series.**

$$\sqrt{1+x} = 1+\frac x2-\frac{x^2}{8}+\frac{x^3}{16}-\frac{5x^4}{128}+\cdots$$
$$\frac{1}{\sqrt{1+x}} = 1-\frac x2+\frac{3x^2}{8}-\frac{5x^3}{16}+\frac{35x^4}{128}-\cdots$$

*(Both verified.)*

### And from Week 9

$$\frac{1}{1-x} = \sum x^n,\qquad \ln(1+x) = \sum_{n\ge1}\frac{(-1)^{n+1}x^n}{n},\qquad \arctan x = \sum_{n\ge0}\frac{(-1)^nx^{2n+1}}{2n+1}$$

---

## 4. Manipulate, Do Not Differentiate

> **Computing $f^{(n)}(0)$ by hand is almost always the wrong method.** Substitute into, differentiate,
> integrate or multiply a known series instead.

### Example 1 — substitution

$$e^{-x^2} = \sum_{n=0}^\infty\frac{(-x^2)^n}{n!} = \sum_{n=0}^\infty\frac{(-1)^nx^{2n}}{n!} = 1-x^2+\frac{x^4}{2}-\frac{x^6}{6}+\cdots$$

**Radius still $\infty$.**

**Compare the alternative:** computing $\frac{d^{10}}{dx^{10}}e^{-x^2}$ at 0 by hand. **One line against a page.**

### Example 2 — multiplication by a power

$$x\cos x = x\sum\frac{(-1)^nx^{2n}}{(2n)!} = \sum_{n=0}^\infty\frac{(-1)^nx^{2n+1}}{(2n)!}$$

### Example 3 — a product of two series

$$e^x\sin x = \left(1+x+\frac{x^2}{2}+\frac{x^3}{6}+\cdots\right)\left(x-\frac{x^3}{6}+\cdots\right)$$

Collecting by degree: $x + x^2 + \frac{x^3}{3}+0\cdot x^4+\cdots$

**Multiplying series is legal inside the smaller radius**, because both converge absolutely there — Week 8's licence again.

### Example 4 — differentiating a known series

$$\frac{d}{dx}\sin x = \frac{d}{dx}\sum\frac{(-1)^nx^{2n+1}}{(2n+1)!} = \sum\frac{(-1)^n(2n+1)x^{2n}}{(2n+1)!} = \sum\frac{(-1)^nx^{2n}}{(2n)!} = \cos x \ \checkmark$$

**A free consistency check** on both series at once.

---

## 5. Taylor Series at Other Centres

**The centre is a choice**, and it matters enormously in practice.

### Example 5 — $e^x$ at $a=1$

$f^{(n)}(1)=e$ for all $n$, so

$$e^x = \sum_{n=0}^\infty\frac{e}{n!}(x-1)^n = e\left[1+(x-1)+\frac{(x-1)^2}{2!}+\cdots\right]$$

*(Which is just $e^x = e\cdot e^{x-1}$ with the standard series — always look for a shortcut.)*

### Why the centre matters

**A Taylor series converges fastest near its centre.** Week 9's lab measured this: for $\arctan$, ten digits needs $5\times10^9$ terms at $x=1$ but **17** at $x=\frac1{\sqrt3}$.

> **This is how a numerical library works.** To compute $\sin(1000)$ it does **not** evaluate the
> Maclaurin series at 1000 — that would need hundreds of terms and lose catastrophic precision.
> **It reduces the argument modulo $2\pi$ to a small interval, then uses a short series there.**
> **Argument reduction plus a well-centred series is the whole algorithm.**

---

## 6. What To Take From This Lecture

1. **$c_n = \frac{f^{(n)}(a)}{n!}$** — forced, not chosen, and therefore unique.
2. **A Taylor series is a candidate.** It may diverge, or converge to the wrong function.
3. **Learn the library:** $e^x$, $\sin$, $\cos$, the binomial series, plus Week 9's three.
4. **Manipulate rather than differentiate.** Substitution, multiplication, differentiation, integration.
5. **Symmetry shows in the series** — odd functions have odd powers only. Use it as a check.
6. **The centre is a design choice**, and it determines how fast the series is.

---

*Next: Tuesday — Taylor's Theorem, and Whether the Series Is Really $f$*
