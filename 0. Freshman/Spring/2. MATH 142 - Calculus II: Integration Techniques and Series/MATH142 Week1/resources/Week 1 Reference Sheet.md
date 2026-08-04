# MATH 142 · Calculus II
## Week 1 · Reference Sheet
### Integration by Parts; Trigonometric Integrals

---

## Integration by Parts

$$\int u\,dv = uv - \int v\,du \qquad\qquad \int_a^b u\,dv = \Big[uv\Big]_a^b - \int_a^b v\,du$$

From the product rule, integrated. **Trades one integral for another** — worthwhile only if the new one is easier.

### Choosing $u$ — LIATE

**L**ogarithmic → **I**nverse trig → **A**lgebraic → **T**rigonometric → **E**xponential

**Earlier in the list becomes $u$.** Choose $u$ to simplify on differentiation; $dv$ must be integrable.

*A heuristic, not a theorem.*

### Standard results

| Integral | Answer |
|---|---|
| $\int xe^x\,dx$ | $(x-1)e^x$ |
| $\int \ln x\,dx$ | $x\ln x - x$ |
| $\int x\sin x\,dx$ | $-x\cos x + \sin x$ |
| $\int x\cos x\,dx$ | $x\sin x + \cos x$ |
| $\int \arctan x\,dx$ | $x\arctan x - \tfrac12\ln(1+x^2)$ |
| $\int \arcsin x\,dx$ | $x\arcsin x + \sqrt{1-x^2}$ |
| $\int x^2e^x\,dx$ | $(x^2-2x+2)e^x$ |
| $\int e^x\sin x\,dx$ | $\tfrac12 e^x(\sin x - \cos x)$ |
| $\int e^x\cos x\,dx$ | $\tfrac12 e^x(\sin x + \cos x)$ |

*(all omit $+C$; all verified by differentiation)*

### Three patterns

1. **Lone $\ln x$, $\arctan x$, $\arcsin x$** → take $dv = dx$.
2. **Polynomial of degree $n$** → $n$ applications; use **tabular integration**.
3. **The integral returns** → treat as an algebraic equation and solve for it. **Keep the same type of $u$ at every application.**

---

## Reduction Formulas

$$\int\sin^n x\,dx = -\frac{\sin^{n-1}x\cos x}{n} + \frac{n-1}{n}\int\sin^{n-2}x\,dx$$

$$\int\cos^n x\,dx = \frac{\cos^{n-1}x\sin x}{n} + \frac{n-1}{n}\int\cos^{n-2}x\,dx$$

**On $[0,\pi/2]$ the boundary term vanishes:**

$$I_n = \int_0^{\pi/2}\sin^n x\,dx = \frac{n-1}{n}I_{n-2}, \qquad I_0 = \frac\pi2,\ \ I_1 = 1$$

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $I_n$ | $\tfrac\pi2$ | $1$ | $\tfrac\pi4$ | $\tfrac23$ | $\tfrac{3\pi}{16}$ | $\tfrac8{15}$ | $\tfrac{5\pi}{32}$ | $\tfrac{16}{35}$ | $\tfrac{35\pi}{256}$ |

**Even $n$ → multiple of $\pi$; odd $n$ → rational.** The parity decides which base case the recursion lands on.

---

## Trigonometric Integrals

### $\int\sin^m x\cos^n x\,dx$

| $m$ | $n$ | Method |
|---|---|---|
| any | **odd** | peel one $\cos x$ for $du$; use $\cos^2=1-\sin^2$; $u=\sin x$ |
| **odd** | any | peel one $\sin x$ for $du$; use $\sin^2=1-\cos^2$; $u=\cos x$ |
| **even** | **even** | half-angle identities, or reduction formula |

$$\sin^2x = \frac{1-\cos2x}{2} \qquad \cos^2x = \frac{1+\cos2x}{2} \qquad \sin x\cos x = \frac{\sin 2x}{2}$$

### $\int\tan^m x\sec^n x\,dx$

| $m$ | $n$ | Method |
|---|---|---|
| any | **even** | peel $\sec^2x$ for $du$; use $\sec^2=1+\tan^2$; $u=\tan x$ |
| **odd** | any | peel $\sec x\tan x$ for $du$; use $\tan^2=\sec^2-1$; $u=\sec x$ |

$$\int\sec x\,dx = \ln|\sec x+\tan x| \qquad \int\sec^3x\,dx = \frac{\sec x\tan x + \ln|\sec x+\tan x|}{2}$$

### Different frequencies — product-to-sum

$$\sin A\sin B = \tfrac12\big[\cos(A-B)-\cos(A+B)\big]$$
$$\cos A\cos B = \tfrac12\big[\cos(A-B)+\cos(A+B)\big]$$
$$\sin A\cos B = \tfrac12\big[\sin(A-B)+\sin(A+B)\big]$$

---

## Orthogonality

For positive integers $m,n$:

$$\int_0^{2\pi}\sin mx\,\sin nx\,dx = \int_0^{2\pi}\cos mx\,\cos nx\,dx = \begin{cases}0 & m\neq n\\ \pi & m=n\end{cases}$$

$$\int_0^{2\pi}\sin mx\,\cos nx\,dx = 0 \quad\text{always}$$

**Consequence — the Fourier coefficient.** If $f(x) = \sum_k a_k\sin kx$ then

$$a_j = \frac1\pi\int_0^{2\pi}f(x)\sin(jx)\,dx$$

The integral annihilates every frequency but the one you multiplied by. *This is why Fourier analysis works.*

---

## Wallis' Product (Lab 1)

$$\frac\pi2 = \prod_{k=1}^{\infty}\frac{(2k)(2k)}{(2k-1)(2k+1)} = \frac21\cdot\frac23\cdot\frac43\cdot\frac45\cdot\frac65\cdot\frac67\cdots$$

with $W_n = \dfrac{\pi}{2}\cdot\dfrac{I_{2n+1}}{I_{2n}}$ and $I_{2n}/I_{2n+1}\to1$.

**Converges at order 1**: error $\approx \dfrac{\pi/8}{n}$. *(Measured — doubling $n$ merely halves the error; 10 decimal places would need about $8\times10^9$ factors.)*

---

## Strategy: Which Technique?

| Integrand | Try |
|---|---|
| inner function and its derivative | substitution |
| catalogue entry | write it down |
| (polynomial) × (exp or trig) | parts, $u$ = polynomial |
| lone $\ln$, $\arctan$, $\arcsin$ | parts, $dv=dx$ |
| (polynomial) × $\ln x$ | parts, $u=\ln x$ |
| $e^{ax}\sin bx$, $e^{ax}\cos bx$ | parts twice, then solve |
| powers of $\sin$/$\cos$ | parity table |
| powers of $\tan$/$\sec$ | parity table |
| $\sin mx\cos nx$ etc. | product-to-sum |
| high power of one trig function | reduction formula |

**Ask "which kind is this?" before computing anything.** Recognition is worth more marks than execution.

---

## Two Habits

1. **Differentiate every antiderivative.** Sign errors in parts are constant and each takes ten seconds to catch.
2. **The CAS is a check, not an oracle.** It returns $\int\sec^3x\,dx$ in a form unrecognisable against the boxed one above — both correct, differing by a constant.

---

*MATH 142 · Week 1 · Reference Sheet*
