# MATH 141 · Problem Set 2 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-21 out of the student handout, where it had been printed below the questions.*

*(Revised 2026-09-26: the set was cut to 8 problems. The solutions below follow the new numbering.)*

---

### Problem 1 — The Definition (10)

(i) $f(a)$ is defined; (ii) $\lim_{x\to a}f(x)$ exists; (iii) they are equal. *(4 pts)*

Failures: (i) $\frac1x$ at $0$; (ii) $\frac{\lvert x\rvert}{x}$ at $0$; (iii) $f(x)=x$ for $x\ne0$
with $f(0)=5$. *(2 pts each)*

### Problem 2 — Where Is It Continuous? (12)

(a) All $x\ne\pm2$. (b) $[3,\infty)$ — right-continuous at $3$. (c) All $x\ne0$; the
discontinuity at $0$ is **removable**, with limit $1$.

### Problem 3 — Choosing a Value (10)

$\dfrac{(x-3)(x+3)}{x-3}=x+3\to6$, so $k=\mathbf 6$.

### Problem 4 — Classifying Discontinuities (16, 4 each)

| | Type | Reason |
|---|---|---|
| (a) | **Removable** | Cancels to $x+2\to4$ |
| (b) | **Infinite** | Numerator $\to4\ne0$ |
| (c) | **Jump** | One-sided limits $-1$ and $+1$ |
| (d) | **Essential** | Oscillates between $\pm1$ |

*(a) and (b) are the discriminating pair — both have a vanishing denominator.*

### Problem 5 — Finding Every Discontinuity (12)

$\dfrac{(x-3)(x+3)}{x(x-3)}$. **At $3$: removable** (limit $2$). **At $0$: infinite**.

*Verified: $f\to2$ from both sides at $3$; $f\to\mp\infty$ at $0$.*

### Problem 6 — The Intermediate Value Theorem (14)

**(a)** $f(1)=-2<0<4=f(2)$; $f$ is a polynomial, hence continuous. By the IVT a root exists in
$(1,2)$.

**Does tell you:** at least one root exists.
**Does not:** where it is, how many there are, or how to find one.

*(The actual root is $1.521379706805$; uniqueness needs $f'>0$, which is Week 6.)*

**(b)** $g(x)=\cos x-x$ is continuous; $g(0)=1>0$ and $g(1)=\cos 1-1\approx-0.4597<0$. IVT gives a
solution in $(0,1)$.

*(Verified: $c\approx0.739085133$.)*

### Problem 7 — Bisection by Hand (14)

Verified trace:

| Step | Bracket | Midpoint | $f(\text{mid})$ |
|---|---|---|---|
| 1 | $[1.000000,2.000000]$ | $1.500000$ | $-0.125000$ |
| 2 | $[1.500000,2.000000]$ | $1.750000$ | $+1.609375$ |
| 3 | $[1.500000,1.750000]$ | $1.625000$ | $+0.666016$ |

Final bracket: $[1.5, 1.625]$. *(4 pts per step, 2 for the final bracket.)*

### Problem 8 — Why It Is Deep (12)

Take $f(x)=x^2-2$ on $[1,2]$ over $\mathbb{Q}$ only. $f$ is continuous, $f(1)=-1<0<2=f(2)$,
yet no **rational** $c$ has $c^2=2$ — $\sqrt2$ is irrational.

So the conclusion fails while every hypothesis holds. What rescues it over $\mathbb{R}$ is
**completeness** — the reals have no gaps, formalised by the least-upper-bound axiom.

*This is why the IVT needs a proof rather than a picture: the picture is equally convincing over
$\mathbb{Q}$, where the theorem is false. Full marks require naming completeness.*

---

*MATH 141 · Week 2 · Problem Set 2 · © CSE Department*
