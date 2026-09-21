# MATH 141 · Lab 02 Solutions (Instructor)
## Continuity, Discontinuity, and Bisection

All figures verified by computation.

---

## Part 1: Seeing the Four Types (6 pts)

**1A — removable.** $\dfrac{x^2-1}{x-1}$ at $x=1$:

| $x$ | $f(x)$ | | $x$ | $f(x)$ |
|---|---|---|---|---|
| $0.9$ | $1.900000$ | | $1.001$ | $2.001000$ |
| $0.99$ | $1.990000$ | | $1.01$ | $2.010000$ |
| $0.999$ | $1.999000$ | | $1.1$ | $2.100000$ |

Limit $2$; $f(1)$ undefined. **Part (i)** of the definition fails.

**1B — infinite.** $\pm10^4$ at $x=\pm10^{-4}$; $\pm10^8$ at $\pm10^{-8}$. Limits $+\infty$ and
$-\infty$. **Part (ii)** fails.

**1C — jump.** $f(-10^{-6})=-0.000001$, $f(+10^{-6})=+1.000001$. One-sided limits $0$ and $1$.
**Part (ii)** fails.

**1D — essential.** At $x=\dfrac{1}{k\pi/2}$:

| $x$ | $\sin(1/x)$ |
|---|---|
| $0.6366197724$ | $+1$ |
| $0.2122065908$ | $-1$ |
| $0.1273239545$ | $+1$ |
| $0.0909456818$ | $-1$ |
| $0.0707355303$ | $+1$ |
| $0.0578745248$ | $-1$ |

**Exactly alternating $\pm1$**, with the points crowding toward $0$. No one-sided limit exists —
**part (ii)** fails, but for a different reason than 1B or 1C: the values do not settle *and* do not
diverge.

*Marking: 1 pt for the table, 0.5 for the correct classification, each part. The 1D table must show
the alternation; students who sample at arbitrary points see noise and conclude nothing.*

---

## Part 2: Repairing a Discontinuity (4 pts)

**2A.** Values approach $12$ from both sides ($11.940100$ at $x=1.99$, $12.006001$ at $x=2.001$).

**2B.** $\dfrac{x^3-8}{x-2}=\dfrac{(x-2)(x^2+2x+4)}{x-2}=x^2+2x+4$, which at $x=2$ gives
$4+4+4=\mathbf{12}$ ✓

**2C.**
$$\tilde f(x)=\begin{cases}\dfrac{x^3-8}{x-2},& x\ne2\\[4pt] 12,& x=2\end{cases}$$

**2D — the marking point.** A limit as $x\to2$ is computed over values with $0<\lvert x-2\rvert$ —
the definition **explicitly excludes** $x=2$. Since $x\ne2$ throughout, dividing by $x-2$ is dividing
by a nonzero quantity and is valid.

The cancelled expression $x^2+2x+4$ agrees with $f$ at every point where the limit "looks", so their
limits coincide. That $x^2+2x+4$ is *also* defined at $2$ is a bonus — it is what makes the
extension continuous.

*Students who say "we cancel because $x\ne2$" without connecting it to the $0<\lvert x-a\rvert$ in
the definition get 0.5 of the 1.*

---

## Part 3: Bisection (7 pts)

**3A/3B — verified trace** on $x^3-x-2$ over $[1,2]$:

| Step | Bracket | Midpoint | $f(\text{mid})$ |
|---|---|---|---|
| 1 | $[1.000000,2.000000]$ | $1.500000$ | $-0.125000$ |
| 2 | $[1.500000,2.000000]$ | $1.750000$ | $+1.609375$ |
| 3 | $[1.500000,1.750000]$ | $1.625000$ | $+0.666016$ |
| 4 | $[1.500000,1.625000]$ | $1.562500$ | $+0.252197$ |
| 5 | $[1.500000,1.562500]$ | $1.531250$ | $+0.059113$ |
| 6 | $[1.500000,1.531250]$ | $1.515625$ | $-0.034054$ |
| 7 | $[1.515625,1.531250]$ | $1.523438$ | $+0.012250$ |
| 8 | $[1.515625,1.523438]$ | $1.519531$ | $-0.010971$ |

**3C.** Root $=\mathbf{1.521379706805}$, with $f(\text{root})=1.33\times10^{-15}$.

**3D.** Predicted versus actual step counts:

| $\varepsilon$ | $\lceil\log_2(1/\varepsilon)\rceil$ |
|---|---|
| $10^{-4}$ | $14$ |
| $10^{-6}$ | $20$ |
| $10^{-10}$ | $34$ |

*Students whose code uses `while (b-a) > eps` should get exactly these. A common off-by-one comes
from testing `>=` instead of `>`; accept either with a note.*

---

## Part 4: The IVT Over the Rationals (3 pts)

**4A.** By hand, the midpoints are $\tfrac32,\tfrac54,\tfrac{11}{8},\tfrac{23}{16},\dots$ —
**every one rational**, with denominators doubling.

**4B — the expected explanation.**

Every midpoint bisection produces is rational, and the brackets shrink without bound toward a point
where $f$ changes sign. But that point is $\sqrt2$, which is **not rational** — so within
$\mathbb{Q}$ the process converges to nothing. There is a "hole" exactly where the root should be.

Over $\mathbb{R}$ the nested brackets **do** converge to a point, because the reals are **complete**:
every nested sequence of closed intervals with shrinking width contains a real number. That
completeness is precisely what the IVT's proof requires, and precisely what $\mathbb{Q}$ lacks.

*Full marks require the word **completeness** (or an accurate description of it). "Because $\sqrt2$
isn't rational" alone is the observation, not the explanation — award 1 of 2.*

---

## Common Submission Problems

| Symptom | Cause | Action |
|---|---|---|
| 1D sampled at arbitrary $x$ | Missed the instruction | −1; the alternation is only visible at the specified points |
| 2D says only "$x\ne2$" | No link to the definition | −0.5 |
| 3D off by one | `>=` vs `>` in the loop | No deduction if noted |
| 4B stops at "$\sqrt2$ is irrational" | Observation, not explanation | −1 |

---

*MATH 141 · Week 2 · Lab 02 Solutions · Instructor copy — do not distribute*
