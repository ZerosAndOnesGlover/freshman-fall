# MATH 142 · Calculus II
## Week 1 · Lecture 2 (Tuesday)
### Repeated Parts, Reduction Formulas, and the Integral That Comes Back

**Date:** Tuesday 26 January 2027 · 11:00–11:50 · Week 1

---

**Reading:** Stewart §7.1 (continued) | Apostol Ch. 5 §5.9

---

## 1. Applying Parts More Than Once

Yesterday every example terminated after one application. When $u$ is a polynomial of degree $n$, it takes $n$ differentiations to reach a constant — so **parts must be applied $n$ times**.

### Example 1 — $\int x^2 e^x\,dx$

**First application:** $u = x^2$, $dv = e^x dx$, so $du = 2x\,dx$, $v = e^x$:

$$\int x^2 e^x dx = x^2 e^x - \int 2x e^x\,dx = x^2 e^x - 2\int x e^x\,dx$$

**Second application:** we did $\int xe^x dx = (x-1)e^x$ yesterday. So

$$\int x^2 e^x dx = x^2 e^x - 2(x-1)e^x + C = \boxed{(x^2 - 2x + 2)e^x + C}$$

*Verified symbolically.*

**Check:** $\frac{d}{dx}\big[(x^2-2x+2)e^x\big] = (2x-2)e^x + (x^2-2x+2)e^x = x^2 e^x$ ✓

**Keep $u$ the same type at each step.** Having chosen the polynomial as $u$, choose the polynomial again. Switching mid-problem undoes the previous step and returns you to the start — a real and common way to waste ten minutes.

---

## 2. Tabular Integration

For (polynomial) × (something easily integrated repeatedly), there is a bookkeeping device that makes repeated parts almost mechanical.

**Build two columns:** differentiate $u$ down to zero on the left; integrate $dv$ repeatedly on the right. Then multiply along the diagonals, **alternating signs**.

### Example 2 — $\int x^3 e^{2x}\,dx$

| sign | $u$ and derivatives | $dv$ and integrals |
|:---:|---|---|
| $+$ | $x^3$ | $e^{2x}$ |
| $-$ | $3x^2$ | $\tfrac12 e^{2x}$ |
| $+$ | $6x$ | $\tfrac14 e^{2x}$ |
| $-$ | $6$ | $\tfrac18 e^{2x}$ |
| | $0$ | $\tfrac1{16}e^{2x}$ |

Multiply each left entry by the right entry **one row down**, with the signs shown:

$$= x^3\cdot\tfrac12 e^{2x} \;-\; 3x^2\cdot\tfrac14 e^{2x} \;+\; 6x\cdot\tfrac18 e^{2x} \;-\; 6\cdot\tfrac1{16}e^{2x} + C$$

$$= \left(\frac{x^3}{2} - \frac{3x^2}{4} + \frac{3x}{4} - \frac38\right)e^{2x} + C = \boxed{\frac{(4x^3-6x^2+6x-3)e^{2x}}{8} + C}$$

*Verified symbolically.*

**This would have been four applications of the formula.** The table is the same computation with the bookkeeping made visible, and it is much harder to lose a sign in.

**It only works when the left column terminates** — i.e. when $u$ is a polynomial. For $\int e^x \sin x\,dx$ neither column ever ends, which is §3.

---

## 3. The Integral That Comes Back

$$\int e^x\sin x\,dx$$

LIATE says take $u = \sin x$ (**T** before **E**). Then $du = \cos x\,dx$, $v = e^x$:

$$I = \int e^x\sin x\,dx = e^x\sin x - \int e^x\cos x\,dx$$

Apply parts again to the new integral, **keeping the trigonometric factor as $u$**: $u = \cos x$, $dv = e^x dx$:

$$\int e^x\cos x\,dx = e^x\cos x + \int e^x\sin x\,dx = e^x\cos x + I$$

Substituting back:

$$I = e^x\sin x - \big(e^x\cos x + I\big) = e^x\sin x - e^x\cos x - I$$

**The original integral has reappeared.** No further application will help — a third would just cycle again.

**But this is now an algebraic equation in $I$.** Solve it:

$$2I = e^x(\sin x - \cos x) \implies \boxed{I = \frac{e^x(\sin x - \cos x)}{2} + C}$$

*Verified symbolically.*

**Check:** $\frac{d}{dx}\left[\frac{e^x(\sin x-\cos x)}{2}\right] = \frac{e^x(\sin x - \cos x) + e^x(\cos x + \sin x)}{2} = \frac{2e^x\sin x}{2} = e^x\sin x$ ✓

### Two things to notice

**(a) You must be consistent.** If on the second application you switch and take $u = e^x$, the two steps undo each other and you get the vacuous identity $I = I$. **Same type of $u$ both times.**

**(b) The constant.** Solving the equation gives one $C$ at the end, not one per application. Writing $+C$ at intermediate stages and then dividing by 2 will produce a $C/2$, which is still an arbitrary constant — harmless, but a common source of confusion.

### The companion

By the identical argument,

$$\int e^x\cos x\,dx = \frac{e^x(\sin x + \cos x)}{2} + C$$

*Verified symbolically.* **Only the sign differs.** Both are worth knowing; both appear whenever a damped oscillation is integrated, which in engineering is constantly.

---

## 4. Reduction Formulas

Sometimes you cannot finish the job but you can **make the problem smaller**. A reduction formula expresses an integral with exponent $n$ in terms of the same integral with a smaller exponent — a recurrence, in the CS sense.

### Deriving the formula for $\int\sin^n x\,dx$

Split off one factor of $\sin x$:

$$\int\sin^n x\,dx = \int \underbrace{\sin^{n-1}x}_{u}\cdot\underbrace{\sin x\,dx}_{dv}$$

Then $du = (n-1)\sin^{n-2}x\cos x\,dx$ and $v = -\cos x$:

$$\int\sin^n x\,dx = -\sin^{n-1}x\cos x + (n-1)\int\sin^{n-2}x\cos^2 x\,dx$$

Now use $\cos^2 x = 1 - \sin^2 x$:

$$= -\sin^{n-1}x\cos x + (n-1)\int\sin^{n-2}x\,dx - (n-1)\int\sin^n x\,dx$$

**The original integral is back again** — the same situation as §3, and the same escape. Move it to the left:

$$n\int\sin^n x\,dx = -\sin^{n-1}x\cos x + (n-1)\int\sin^{n-2}x\,dx$$

$$\boxed{\int\sin^n x\,dx = -\frac{\sin^{n-1}x\cos x}{n} + \frac{n-1}{n}\int\sin^{n-2}x\,dx}$$

*Verified symbolically for $n = 2,3,4,5$: in each case the two sides differ by zero.*

**Read it as a recurrence.** Each application drops the exponent by 2, so you recurse down to a base case: $\int\sin^0x\,dx = x$ or $\int\sin^1 x\,dx = -\cos x$, depending on parity.

> **This is exactly a recursive algorithm** — a recurrence relation with two base cases, reducing $n$ by 2 each call, terminating in $\lceil n/2\rceil$ steps. Lab 1 asks you to implement it.

---

## 5. The Definite Case: A Beautiful Simplification

Evaluate the reduction formula between $0$ and $\tfrac\pi2$ and something excellent happens. Write

$$I_n = \int_0^{\pi/2}\sin^n x\,dx$$

The boundary term is $\left[-\frac{\sin^{n-1}x\cos x}{n}\right]_0^{\pi/2}$. At $x = \tfrac\pi2$, $\cos x = 0$; at $x=0$, $\sin x = 0$ (for $n\ge2$). **The boundary term vanishes at both ends**, leaving

$$\boxed{I_n = \frac{n-1}{n}\,I_{n-2}}, \qquad I_0 = \frac\pi2,\quad I_1 = 1$$

*Verified symbolically for $n=2,\ldots,8$: every case matches exactly.*

### The values

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $I_n$ | $\dfrac\pi2$ | $1$ | $\dfrac\pi4$ | $\dfrac23$ | $\dfrac{3\pi}{16}$ | $\dfrac8{15}$ | $\dfrac{5\pi}{32}$ | $\dfrac{16}{35}$ | $\dfrac{35\pi}{256}$ |

*All computed and verified.*

**Notice the pattern: even $n$ gives a multiple of $\pi$, odd $n$ gives a rational number.** The parity of $n$ determines which base case the recursion lands on, and $\pi$ enters only through $I_0$.

That observation has a remarkable consequence. Since $I_n$ is decreasing in $n$, squeezing $I_{2n}$ between its odd neighbours and taking $n\to\infty$ yields **Wallis' product**:

$$\frac{\pi}{2} = \frac{2}{1}\cdot\frac{2}{3}\cdot\frac{4}{3}\cdot\frac{4}{5}\cdot\frac{6}{5}\cdot\frac{6}{7}\cdots$$

a formula for $\pi$ found by John Wallis in **1656** — before calculus existed — using nothing but this recursion. **Lab 1 computes it, and measures how badly it converges.**

---

## 6. What To Take From This Lecture

1. **A polynomial of degree $n$ needs $n$ applications of parts.** Keep $u$ the same type throughout.
2. **Tabular integration** is repeated parts with the bookkeeping made visible. Use it whenever the left column terminates.
3. **When the original integral reappears, solve for it algebraically.** This is not a failure of the method; it is the method.
4. **A reduction formula is a recurrence relation**, with base cases and a termination argument.
5. **On $[0,\pi/2]$ the boundary term vanishes**, giving the clean recursion $I_n = \frac{n-1}{n}I_{n-2}$.

---

*Next: Wednesday — Trigonometric Integrals, and the Identity Behind Fourier Analysis*
