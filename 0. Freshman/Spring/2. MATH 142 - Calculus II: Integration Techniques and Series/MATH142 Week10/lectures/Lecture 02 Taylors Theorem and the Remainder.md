# MATH 142 · Calculus II
## Week 10 · Lecture 2 (Tuesday)
### Taylor's Theorem, and Whether the Series Is Really $f$

---

**Reading:** Stewart §11.10 (continued) | Apostol Ch. 11 §11.9–11.11

---

## 1. The Gap

Yesterday: **if** $f$ has a power series at $a$, its coefficients must be $\frac{f^{(n)}(a)}{n!}$.

**That "if" is doing a great deal of work.** Two separate things can fail:

1. **The series may not converge** (Week 9's question — settled by the Ratio Test).
2. **It may converge, but not to $f$.**

**The second failure is the one nobody expects**, so we look at it first.

---

## 2. A Function That Is Not Its Own Taylor Series

$$f(x) = \begin{cases}e^{-1/x^2} & x\ne0\\[4pt] 0 & x=0\end{cases}$$

**$f$ is smooth everywhere** — infinitely differentiable, including at 0.

**And every derivative at 0 is zero.** The reason is that $e^{-1/x^2}$ vanishes faster than every power of $x$:

$$\lim_{x\to0}\frac{e^{-1/x^2}}{x^{k}} = 0 \qquad\text{for every } k$$

*(Verified numerically: $\frac{f(x)}{x^{10}}$ takes the values $18.8,\ 1.4\times10^{-4},\ 3.7\times10^{-34},\ 2.0\times10^{-161}$ at $x=0.5,\ 0.2,\ 0.1,\ 0.05$ — collapsing to zero.)*

**So the Maclaurin series of $f$ is**

$$0+0\cdot x+0\cdot x^2+\cdots = 0$$

**It converges everywhere — to the zero function.** But $f(1)=e^{-1}\approx0.3679\neq0$. *(Verified.)*

> **$f$ agrees with its Taylor series only at the single point $x=0$.**
>
> **This is why Taylor's theorem must be stated with a remainder.** "Compute the coefficients and
> write $\sum$" is not a proof of anything. **You must show the error tends to zero**, and for this
> $f$ it does not.

---

## 3. Taylor's Theorem with Lagrange Remainder

> **Theorem.** If $f$ is $(n+1)$-times differentiable on an interval containing $a$ and $x$, then
>
> $$f(x) = \underbrace{\sum_{k=0}^{n}\frac{f^{(k)}(a)}{k!}(x-a)^k}_{P_n(x)} + R_n(x)$$
>
> where for some $c$ strictly between $a$ and $x$,
>
> $$\boxed{R_n(x) = \frac{f^{(n+1)}(c)}{(n+1)!}(x-a)^{n+1}}$$

**Read the remainder as "the next term, with the derivative evaluated somewhere unknown."** That is exactly what it is.

> **This is the Mean Value Theorem generalised.** At $n=0$ it says $f(x) = f(a)+f'(c)(x-a)$ — the MVT
> from MATH 141. **Taylor's theorem is the MVT for higher derivatives.**

### The consequence that matters

$$f(x) = \sum_{n=0}^\infty\frac{f^{(n)}(a)}{n!}(x-a)^n \iff \lim_{n\to\infty}R_n(x) = 0$$

**A function equals its Taylor series exactly where the remainder vanishes**, and nowhere else.

---

## 4. Using the Bound

**$c$ is unknown**, so in practice you bound $|f^{(n+1)}|$ over the whole interval between $a$ and $x$:

$$\text{If } \left|f^{(n+1)}(t)\right|\le M \text{ for all } t \text{ between } a \text{ and } x, \quad\text{then}\quad \left|R_n(x)\right|\le\frac{M\,|x-a|^{n+1}}{(n+1)!}$$

> **Finding a valid $M$ is usually the hardest step**, and it must be a bound on an *interval*, not a
> value at a point.

### Example 1 — $\sin x$, where $M$ is free

Every derivative of $\sin$ is $\pm\sin$ or $\pm\cos$, so $\left|f^{(n+1)}\right|\le1$ **everywhere**. Take $M=1$:

$$\left|R_n(x)\right|\le\frac{|x|^{n+1}}{(n+1)!}$$

*(Verified — the bound holds in all nine cases tested:)*

| $x$ | $n$ | true error | bound |
|---|---|---|---|
| $0.5$ | 3 | $2.589\times10^{-4}$ | $2.604\times10^{-3}$ |
| $0.5$ | 7 | $5.370\times10^{-9}$ | $9.688\times10^{-8}$ |
| $1.0$ | 3 | $8.138\times10^{-3}$ | $4.167\times10^{-2}$ |
| $1.0$ | 7 | $2.731\times10^{-6}$ | $2.480\times10^{-5}$ |
| $2.0$ | 3 | $2.426\times10^{-1}$ | $6.667\times10^{-1}$ |
| $2.0$ | 7 | $1.361\times10^{-3}$ | $6.349\times10^{-3}$ |

**The bound is honest but loose** — typically 3–10 times the true error. **That is the usual price of a bound valid for every $x$ in the interval.**

### Why $\sin$ equals its series everywhere

$$\left|R_n(x)\right|\le\frac{|x|^{n+1}}{(n+1)!}\longrightarrow0 \qquad\text{for every fixed } x$$

because **factorials beat exponentials** — Week 6's growth hierarchy, $\frac{a^n}{n!}\to0$.

$$\boxed{\sin x = \sum_{n=0}^\infty\frac{(-1)^nx^{2n+1}}{(2n+1)!}\quad\text{for all real } x}$$

**The same argument works for $\cos$ and $e^x$**, giving equality on all of $\mathbb{R}$.

### Example 2 — $e^x$, where $M$ depends on the interval

$f^{(n+1)}(t)=e^t$ is **unbounded** on $\mathbb R$, so there is no single $M$. **But on any fixed interval there is one.** To bound the error on $[0,1]$: $e^t\le e$ there, so

$$\left|R_n(x)\right|\le\frac{e}{(n+1)!} \qquad (0\le x\le1)$$

**Still $\to0$**, so $e^x$ equals its series on $[0,1]$ — and the same argument on $[-A,A]$ for any $A$ gives equality everywhere.

> **The moral: $M$ may depend on the interval, and often must.** Quoting a bound without saying over
> what interval it holds is meaningless.

---

## 5. Two Practical Uses

### (a) How many terms do I need?

**Question:** approximate $\sin(0.5)$ with error below $10^{-10}$.

Solve $\frac{(0.5)^{n+1}}{(n+1)!}<10^{-10}$:

| $n$ | bound | below $10^{-10}$? |
|---|---|---|
| $8$ | $5.38\times10^{-9}$ | no |
| $9$ | $2.69\times10^{-10}$ | **just misses** |
| $10$ | $1.22\times10^{-11}$ | **yes** |

*(Verified.)*

**So $n=10$ is the first degree that suffices.** And since $\sin$ has only odd-power terms, $P_{10}=P_9$ — so this is

$$x-\frac{x^3}{3!}+\frac{x^5}{5!}-\frac{x^7}{7!}+\frac{x^9}{9!}$$

— **five nonzero terms** for ten decimal places.

**This is precisely what a numerical library does** — except it computes the required degree once, at design time, for a fixed argument range.

### (b) Is the truncation good enough here?

**Given $n$, the same inequality bounds the error.** Because the bound is explicit and rigorous, a library can *guarantee* its output to within half a unit in the last place. **No numerical method met so far in this course comes with a guarantee like that.**

---

## 6. Alternating Series: A Shortcut

**When the Taylor series alternates and its terms decrease**, Week 8's estimate applies and is usually **easier and tighter** than the Lagrange bound:

$$\left|R_N\right|\le\ \text{first omitted term}$$

For $\sin(0.5)$, dropping after $\frac{0.5^5}{120}$ leaves an error at most the next term, $\frac{0.5^7}{7!} = 1.5501\times10^{-6}$ — **no derivative bound required at all.**

**And here the bound is nearly exact:** the true error is $1.5447\times10^{-6}$. *(Verified.)* **The alternating estimate is tight to within 0.4%, where the Lagrange bound was loose by a factor of several.**

> **Use the alternating bound when it applies; fall back on Lagrange when it does not.** Lagrange is
> the general theorem; the alternating estimate is the convenient special case.

---

## 7. What To Take From This Lecture

1. **A Taylor series need not equal its function.** $e^{-1/x^2}$ is the standing counterexample.
2. **$f = $ its Taylor series $\iff R_n\to0$.** That is the definition of the question, and the theorem answers it.
3. **Lagrange remainder: $R_n = \frac{f^{(n+1)}(c)}{(n+1)!}(x-a)^{n+1}$** — the next term, evaluated somewhere unknown.
4. **It generalises the Mean Value Theorem.**
5. **Bound $|f^{(n+1)}|$ over the interval**, and say which interval.
6. **$\sin$, $\cos$, $e^x$ equal their series everywhere**, because $\frac{|x|^{n+1}}{(n+1)!}\to0$ — Week 6's hierarchy.
7. **Use the alternating estimate when available.**

---

*Next: Wednesday — Applications, and Week 0's Debt*
