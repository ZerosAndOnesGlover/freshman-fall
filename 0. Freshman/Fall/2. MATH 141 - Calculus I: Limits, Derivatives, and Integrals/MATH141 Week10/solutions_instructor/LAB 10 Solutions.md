# MATH 141 · Week 10
## LAB 10 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed, not estimated.** Grade the *reasoning*, not agreement to the
> last decimal place.

*(Revised 2026-09-26 to match the 6-question version of the lab.)*

---

## Part 1 — Substitution Pattern Recognition

**Q1 (15).** Every row has its $du$ present up to a constant:

| # | $u$ | $du$ | Antiderivative |
|---|---|---|---|
| 1 | $x^5$ | $5x^4dx$ | $-\tfrac15\cos(x^5)+C$ |
| 2 | $\sqrt x$ | $\frac{dx}{2\sqrt x}$ | $2e^{\sqrt x}+C$ |
| 3 | $\tan x$ | $\sec^2x\,dx$ | $\tfrac16\tan^6x+C$ |
| 4 | $x^3+1$ | $3x^2dx$ | $-\dfrac{1}{12(x^3+1)^4}+C$ |
| 5 | $\sin x$ | $\cos x\,dx$ | $e^{\sin x}+C$ |
| 6 | $\ln x$ | $\frac{dx}{x}$ | $-\dfrac{1}{2(\ln x)^2}+C$ |
| 7 | $\tan x$ | $\sec^2x\,dx$ | $\tfrac23\tan^{3/2}x+C$ |
| 8 | $\arctan x$ | $\frac{dx}{1+x^2}$ | $\tfrac12(\arctan x)^2+C$ |

*Marking: 1 per row (8), plus 3.5 per fully worked integral. Rows 2, 6 and 8 are the ones students most often
miss: the derivative is hidden as a quotient.*

---

## Part 2 — Checking a Substitution

**Q2 (20).** $u = x^2+1$, $du = 2x\,dx$, and the limits become $u = 1$ to $u = 5$:
$$\int_0^2 x(x^2+1)^2dx = \frac12\int_1^5 u^2du = \frac16\big[u^3\big]_1^5 = \frac{124}{6} = \frac{62}{3} \approx 20.6667.$$
`midpoint_rule` with $n = 1000$ gives $20.66664933$, and Desmos gives $20.6666666667$. All three agree to
4 decimal places.

*The commonest error is substituting the $x$-limits $0$ and $2$ into $\frac16u^3$, giving $\frac{8}{6}$. Deduct 6.*

---

## Part 3 — Symmetry

**Q3 (20).** **(a)** $f(-x) = -x^3 + 4x = -f(x)$: **odd**. $\int_{-3}^0 f = -2.25$ and $\int_0^3 f = 2.25$, so
$\int_{-3}^3 f = 0$. An odd function on an interval symmetric about $0$ always integrates to $0$: the two
halves are mirror images with opposite signs.

**(b)** $g(-x) = g(x)$ (even powers only): **even**. $\int_0^{2.5} g = 3.4895833$ and
$\int_{-2.5}^{2.5} g = 6.9791667$, exactly double.

*Asserting the symmetry without checking $f(-x)$ earns no method marks.*

---

## Part 4 — The Tabular Method

**Q4 (10).** $\frac{d}{dx}\left[e^x(x^3-3x^2+6x-6)\right] = e^x(x^3-3x^2+6x-6) + e^x(3x^2-6x+6) = x^3e^x$ ✓

**Q5 (15).**

| Sign | $P$ | $f$ |
|---|---|---|
| + | $x^2$ | $\cos x$ |
| − | $2x$ | $\sin x$ |
| + | $2$ | $-\cos x$ |
| − | $0$ | $-\sin x$ |

$\int x^2\cos x\,dx = x^2\sin x + 2x\cos x - 2\sin x + C$. Differentiating:
$2x\sin x + x^2\cos x + 2\cos x - 2x\sin x - 2\cos x = x^2\cos x$ ✓

**Q6 (20).**

| Sign | $P$ | $f$ |
|---|---|---|
| + | $x^2$ | $e^{-x}$ |
| − | $2x$ | $-e^{-x}$ |
| + | $2$ | $e^{-x}$ |
| − | $0$ | $-e^{-x}$ |

$\int x^2e^{-x}\,dx = -x^2e^{-x} - 2xe^{-x} - 2e^{-x} + C = -e^{-x}(x^2+2x+2) + C$. Differentiating:
$e^{-x}(x^2+2x+2) - e^{-x}(2x+2) = x^2e^{-x}$ ✓

**Why it works.** Row 1 against row 2 is one application of parts with $u = x^2$, $dv = e^{-x}dx$: the diagonal
product $x^2\cdot(-e^{-x})$ is the $uv$ term. The remaining $-\int v\,du = -\int(-e^{-x})(2x)\,dx$ is a new
integral of the same shape, which the next rows handle. Its leading minus sign is why the signs alternate.
The table stops when the polynomial column reaches $0$, because the leftover integral is then $0$.

*Full marks need the $uv$ term identified and the source of the sign alternation.*

---

## Marking Scheme

- **Method (≈60%).** Substitutions and tables set up correctly, symmetry checked, and every antiderivative
  verified by differentiating.
- **Execution (≈40%).** Correct antiderivatives and values.

---

*MATH 141 · Week 10 · Lab Solutions · Instructor Copy · © CSE Department*
