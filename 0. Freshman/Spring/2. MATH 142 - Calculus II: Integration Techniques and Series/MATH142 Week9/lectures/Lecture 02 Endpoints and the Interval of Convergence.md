# MATH 142 · Calculus II
## Week 9 · Lecture 2 (Tuesday)
### Endpoints, and the Interval of Convergence

**Date:** Tuesday 16 March 2027 · 11:00–11:50 · Week 9

---

**Reading:** Stewart §11.8 (continued) | Apostol Ch. 11 §11.4

---

## 1. Where the Ratio Test Stops

Yesterday's formula gives $R$, and with it convergence on $(a-R,a+R)$ and divergence outside $[a-R,a+R]$.

**At the two endpoints $x = a\pm R$, the Ratio Test gives exactly $L=1$** — and Week 8 established what that means:

> **$L=1$ is silence.** The test has finished and told you nothing.

**So the endpoints must be settled separately**, and at each one you have an **ordinary numerical series** — the objects of Weeks 7 and 8. **This lecture is the payoff for three weeks of test-building.**

### The procedure

> 1. **Find $R$** by the Ratio Test.
> 2. **Write the open interval** $(a-R,\,a+R)$ by solving $|x-a|<R$.
> 3. **Substitute $x = a-R$.** Test the resulting numerical series.
> 4. **Substitute $x = a+R$.** Test that one.
> 5. **Report the interval**, with brackets or parentheses as determined.

**Steps 3 and 4 are two separate problems** and may need two different tests. **Neither can be inferred from the other.**

---

## 2. Four Intervals, One Radius

All four combinations occur. Here they are with $R=1$ and centre $0$, so you can see that **only the coefficients differ.**

### (a) Open at both ends: $\sum x^n$

- **$x=1$:** $\sum 1$ — terms do not tend to 0. **Diverges** ($n$-th Term Test).
- **$x=-1$:** $\sum(-1)^n$ — terms do not tend to 0. **Diverges.**

$$\boxed{(-1,1)}$$

### (b) Closed left, open right: $\sum\dfrac{x^n}{n}$

- **$x=1$:** $\sum\frac1n$ — the harmonic series. **Diverges.**
- **$x=-1$:** $\sum\frac{(-1)^n}{n}$ — alternating, $b_n=\frac1n$ decreasing and $\to0$. **Converges** (to $-\ln2$).

$$\boxed{[-1,1)}$$

### (c) Open left, closed right: $\sum\dfrac{(-1)^nx^n}{n}$

- **$x=1$:** $\sum\frac{(-1)^n}{n}$. **Converges** (to $-\ln2$).
- **$x=-1$:** $\sum\frac{(-1)^n(-1)^n}{n} = \sum\frac1n$. **Diverges.**

$$\boxed{(-1,1]}$$

### (d) Closed at both ends: $\sum\dfrac{x^n}{n^2}$

- **$x=1$:** $\sum\frac{1}{n^2}$ — $p$-series, $p=2$. **Converges** (to $\frac{\pi^2}{6}$).
- **$x=-1$:** $\sum\frac{(-1)^n}{n^2}$ — converges **absolutely**. **Converges** (to $-\frac{\pi^2}{12}$).

$$\boxed{[-1,1]}$$

*(All eight endpoint verdicts verified.)*

> **Four series, one radius, four intervals.** The radius is a property of how fast $|c_n|$ grows;
> the endpoints are a much finer question about the coefficients themselves. **Nothing short of a
> direct test will settle them.**

---

## 3. A Shifted Centre

$$\sum_{n=1}^\infty\frac{(x-3)^n}{n\,2^n}$$

**Radius** (yesterday, Example 5/7): $\ell = \frac12$, so $R=2$.

**Open interval:** $|x-3|<2 \iff 1<x<5$.

**Endpoint $x=5$:** substituting, $(x-3)^n = 2^n$, so the series is

$$\sum\frac{2^n}{n2^n} = \sum\frac1n \qquad\textbf{diverges}$$

**Endpoint $x=1$:** $(x-3)^n = (-2)^n$, so

$$\sum\frac{(-2)^n}{n2^n} = \sum\frac{(-1)^n}{n} \qquad\textbf{converges}$$

$$\boxed{\text{Interval of convergence } [1,5)}$$

*(Both verified.)*

> **Notice the mechanics.** Substituting the endpoint makes the $2^n$ cancel exactly — that always
> happens, because the endpoint is where $|x-a|$ equals the radius. **The surviving series is
> governed entirely by the non-geometric part of the coefficient.**

---

## 4. Absolute vs Conditional at the Endpoints

**Inside the radius, convergence is always absolute** (yesterday, §7). **At an endpoint it may be only conditional.**

For $\sum\frac{x^n}{n}$ on $[-1,1)$:

| $x$ | behaviour |
|---|---|
| $\lvert x\rvert<1$ | **absolutely** convergent |
| $x=-1$ | **conditionally** convergent |
| $x=1$ | divergent |

**This matters for Lecture 3.** Term-by-term differentiation and integration are guaranteed **inside** the radius, where convergence is absolute. **At a conditionally convergent endpoint those operations are not automatically valid** — and the fact that they often still work there is a separate theorem (Abel's), not something you may assume.

---

## 5. Common Errors

**(a) Stopping at the radius.** "$R=2$" answers a different question than "find the interval of convergence." **Both endpoints must be tested and the interval reported.**

**(b) Assuming the endpoints match.** They are independent; cases (b) and (c) above differ in exactly one endpoint.

**(c) Forgetting the centre.** For $\sum\frac{(x-3)^n}{n2^n}$ the interval is $[1,5)$, not $[-2,2)$.

**(d) Using the Ratio Test at the endpoint.** It gives $L=1$ there **by construction**. Reaching for it again is circular.

**(e) Divergence by oscillation.** At $x=-1$ in case (a), $\sum(-1)^n$ **diverges** — the partial sums oscillate $-1,0,-1,0,\ldots$ and never settle. **Bounded is not convergent** (Week 6).

---

## 6. A Complete Worked Example

$$\sum_{n=1}^\infty\frac{(-1)^n(x+2)^n}{n\,4^n}$$

**Centre:** $a=-2$.

**Radius:** $\left|\frac{c_{n+1}}{c_n}\right| = \frac{n4^n}{(n+1)4^{n+1}}\to\frac14$, so $R=4$.

**Open interval:** $|x+2|<4 \iff -6<x<2$.

**Endpoint $x=2$:** $(x+2)^n = 4^n$, giving $\sum\frac{(-1)^n4^n}{n4^n} = \sum\frac{(-1)^n}{n}$ — **converges** (conditionally).

**Endpoint $x=-6$:** $(x+2)^n = (-4)^n$, giving

$$\sum\frac{(-1)^n(-4)^n}{n4^n} = \sum\frac{(-1)^n(-1)^n}{n} = \sum\frac1n \qquad\textbf{diverges}$$

$$\boxed{\text{Interval: } (-6,\,2]}$$

> **Note the two $(-1)$ factors combining at $x=-6$.** Sign bookkeeping at endpoints is where most
> marks are lost — **substitute the endpoint value explicitly and simplify**, rather than reasoning
> about signs in your head.

---

## 7. What To Take From This Lecture

1. **The Ratio Test gives $L=1$ at both endpoints, by construction.** It cannot decide them.
2. **Test each endpoint separately**, as an ordinary numerical series, with Weeks 7–8.
3. **All four interval types occur**, and the radius does not determine which.
4. **Solve $|x-a|<R$ explicitly** to get the interval; do not assume it is centred at 0.
5. **Substitute the endpoint and simplify** — the geometric part always cancels.
6. **Inside the radius: absolute. At an endpoint: possibly only conditional.**

---

*Next: Wednesday — Functions as Power Series*
