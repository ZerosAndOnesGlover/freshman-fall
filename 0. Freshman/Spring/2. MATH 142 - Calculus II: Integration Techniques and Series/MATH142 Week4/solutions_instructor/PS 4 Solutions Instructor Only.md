# MATH 142 · Calculus II
## Problem Set 4 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Every volume, length and area below was verified symbolically.

> **Marking philosophy.** In this material the **setup is the assessment**. A correct integral with an
> arithmetic slip should keep most of its marks; a wrong radius that happens to integrate to a tidy
> number should keep almost none.
>
> **Award marks for the sketch.** Where a student's radius is wrong, check whether they drew the
> region — almost always they did not, and that is the note to write on the script.

> **A cautionary note for TAs.** While preparing these solutions, **A4 was initially set up wrongly**
> — with the outer radius taken as $2-x^2$ and the inner as $1$, giving $\tfrac{28\pi}{15}$ instead of
> the correct $\tfrac{17\pi}{15}$. The error came from writing radii algebraically without drawing the
> region. **Expect exactly this error on scripts, and expect it to produce a plausible number.**

---

## Part A — Discs and Washers (5 pts each)

### A1 (5) — $y=\sqrt x$ on $[0,4]$ about the $x$-axis

Discs of radius $\sqrt x$:

$$V = \pi\int_0^4\big(\sqrt x\big)^2dx = \pi\int_0^4 x\,dx = \pi\cdot 8 = \boxed{8\pi}$$

*Verified symbolically.*

*Marking: 2 setup, 3 evaluation. Note $(\sqrt x)^2 = x$ — students who leave the root in and integrate $x^{1/2}$ have squared nothing.*

### A2 (5) — between $y=2x$ and $y=x^2$ about the $x$-axis

**Intersections:** $2x=x^2 \implies x=0,2$. On $(0,2)$, checking at $x=1$: $2>1$, so $y=2x$ is **outer**.

$$V = \pi\int_0^2\Big[(2x)^2-(x^2)^2\Big]dx = \pi\int_0^2\big(4x^2-x^4\big)dx = \pi\left(\frac{32}{3}-\frac{32}{5}\right) = \boxed{\frac{64\pi}{15}}$$

*Verified symbolically. $\approx 13.40$.*

*Marking: 1 intersections, 2 correct outer/inner with a check, 2 evaluation. **$(2x-x^2)^2$ is the standard wrong integrand** — deduct 3, since it is the error the lecture named.*

### A3 (5) — $y=\frac1x$ on $[1,3]$ about the $x$-axis

$$V = \pi\int_1^3\frac{dx}{x^2} = \pi\left[-\frac1x\right]_1^3 = \pi\left(1-\frac13\right) = \boxed{\frac{2\pi}{3}}$$

*Verified symbolically.*

*Worth remarking in class: **this is a truncated Gabriel's Horn**, and Lab 4 lets the upper limit go to infinity — where the volume still converges, to $\pi$.*

### A4 (5) — $y=x^2$ on $[0,1]$ about the line $y=2$

**The region is $0\le y\le x^2$, which lies entirely below the axis $y=2$.** Distances to the axis:

- The **farthest** part of the region from $y=2$ is its lower boundary $y=0$: distance $2$. → **$R=2$**
- The **nearest** part is the curve $y=x^2$: distance $2-x^2$. → **$r = 2-x^2$**

$$V = \pi\int_0^1\Big[2^2-\big(2-x^2\big)^2\Big]dx = \pi\int_0^1\big(4x^2-x^4\big)dx = \pi\left(\frac43-\frac15\right) = \boxed{\frac{17\pi}{15}}$$

*Verified symbolically. $\approx 3.560$.*

**Sanity check worth showing students:** rotating the same region about $y=0$ gives only $\tfrac\pi5\approx0.63$. Moving the axis away from the region must *increase* the volume, and $3.56 > 0.63$ ✓.

*Marking: **3 of the 5 are for the two radii**, 2 for evaluation. The common wrong pairs are $(R,r)=(2-x^2,\,1)$ and $(R,r) = (2-x^2,\,2)$; both come from not drawing the region. **Give the sanity check as feedback** — it catches every such error in ten seconds.*

---

## Part B — Cylindrical Shells (6 pts each)

*Standard marking: 2 radius, 2 height, 2 evaluation.*

### B1 (6) — $y=x^3$ on $[0,2]$ about the $y$-axis

$$V = 2\pi\int_0^2 x\cdot x^3\,dx = 2\pi\left[\frac{x^5}{5}\right]_0^2 = 2\pi\cdot\frac{32}{5} = \boxed{\frac{64\pi}{5}}$$

*Verified. $\approx 40.21$.*

### B2 (6) — $y=\sqrt x$ on $[0,4]$ about the $y$-axis

$$V = 2\pi\int_0^4 x\sqrt x\,dx = 2\pi\int_0^4x^{3/2}dx = 2\pi\cdot\frac25\cdot32 = \boxed{\frac{128\pi}{5}}$$

*Verified. $\approx 80.42$.*

### B3 (6) — $y=\cos x$ on $\left[0,\frac\pi2\right]$ about the $y$-axis

$$V = 2\pi\int_0^{\pi/2}x\cos x\,dx = 2\pi\Big[x\sin x+\cos x\Big]_0^{\pi/2} = 2\pi\left(\frac\pi2 - 1\right) = \boxed{\pi^2-2\pi}$$

*Verified symbolically: $\pi(\pi-2)\approx 3.586$.*

*The inner integral is **integration by parts** — Week 1, PS 1 A1. Worth pointing out that this week's geometry keeps producing last week's integrals.*

### B4 (6) — between $y=x$ and $y=x^2$ on $[0,1]$ about the $y$-axis

**Height is (upper) − (lower)** $= x-x^2$:

$$V = 2\pi\int_0^1 x\big(x-x^2\big)dx = 2\pi\left(\frac13-\frac14\right) = \boxed{\frac\pi6}$$

*Verified. $\approx 0.5236$.*

### B5 (6) — $y=x^2$ on $[0,1]$ about $x=3$

The region lies **to the left** of the axis, so the radius is $3-x$:

$$V = 2\pi\int_0^1(3-x)x^2\,dx = 2\pi\left(1-\frac14\right) = \boxed{\frac{3\pi}{2}}$$

*Verified. $\approx 4.712$.*

*Marking: **3 of the 6 for the radius $3-x$ rather than $x-3$.** A negative radius produces a negative volume, which is the built-in warning here — a student reporting $-\tfrac{3\pi}{2}$ has the right idea and should get 4.*

---

## Part C — Arc Length and Surface Area (6 pts each)

### C1 (6) — $y=\tfrac23x^{3/2}$ on $[0,3]$

$y' = x^{1/2}$, so $1+(y')^2 = 1+x$:

$$L = \int_0^3\sqrt{1+x}\,dx = \left[\frac23(1+x)^{3/2}\right]_0^3 = \frac23(8-1) = \boxed{\frac{14}{3}}$$

*Verified symbolically. $\approx 4.667$.*

*The coefficient $\tfrac23$ is chosen precisely so that $(y')^2 = x$ and the root becomes linear. **Say so** — it makes clear that textbook curves are engineered.*

### C2 (6) — $y=\ln(\cos x)$ on $\left[0,\frac\pi4\right]$

$y' = -\tan x$, so $1+(y')^2 = 1+\tan^2x = \sec^2x$ and $\sqrt{\;} = \sec x$ (positive on this interval):

$$L = \int_0^{\pi/4}\sec x\,dx = \Big[\ln|\sec x+\tan x|\Big]_0^{\pi/4} = \ln\big(\sqrt2+1\big) - \ln 1 = \boxed{\ln\big(1+\sqrt2\big)}$$

*Verified symbolically: the CAS form $\tfrac12\ln\frac{1+\frac{\sqrt2}{2}}{1-\frac{\sqrt2}{2}}$ equals $\ln(1+\sqrt2) \approx 0.8814$ — they agree to all digits checked.*

*Marking: 2 for the identity $1+\tan^2=\sec^2$, 2 for $\int\sec$, 2 for evaluation. **This is the Week 1 catalogue entry doing real work** — a nice moment to point at.*

### C3 (6) — $y=x^3$ on $[0,1]$ about the $x$-axis

$y'=3x^2$, so $ds = \sqrt{1+9x^4}\,dx$:

$$S = 2\pi\int_0^1 x^3\sqrt{1+9x^4}\,dx$$

Substitute $u=1+9x^4$, $du=36x^3dx$:

$$= \frac{2\pi}{36}\int_1^{10}\sqrt u\,du = \frac{\pi}{18}\cdot\frac23\Big[u^{3/2}\Big]_1^{10} = \boxed{\frac{\pi\big(10\sqrt{10}-1\big)}{27}}$$

*Verified symbolically. $\approx 3.563$.*

*Marking: 2 for using $ds$ not $dx$, 2 substitution, 2 evaluation. **The $x^3$ in the radius is exactly what makes the substitution work** — without it this integral would be far harder.*

### C4 (6) — $y=2\sqrt x$ on $[1,2]$ about the $x$-axis

$y' = \tfrac{1}{\sqrt x}$, so $\sqrt{1+(y')^2} = \sqrt{1+\tfrac1x}$, and

$$S = 2\pi\int_1^2 2\sqrt x\sqrt{1+\frac1x}\,dx = 4\pi\int_1^2\sqrt{x+1}\,dx = 4\pi\cdot\frac23\Big[(x+1)^{3/2}\Big]_1^2$$

$$= \frac{8\pi}{3}\big(3\sqrt3-2\sqrt2\big) = \boxed{\frac{8\pi\big(3\sqrt3-2\sqrt2\big)}{3}}$$

*Verified symbolically. $\approx 19.836$.*

*Marking: **3 of the 6 for combining the radicals** into $\sqrt{x+1}$ before integrating. Expanding first gives a much worse integral, and students who did should be shown the one-line simplification.*

### C5 (6) — arc length of $y=e^x$ on $[0,1]$

**(a)** $L = \displaystyle\int_0^1\sqrt{1+e^{2x}}\,dx$.

**(b)** **It IS elementary.** Substitute $u=e^x$, $du = u\,dx$:

$$L = \int_1^e\frac{\sqrt{1+u^2}}{u}\,du$$

— a **rational-in-$u$-and-$\sqrt{1+u^2}$** integrand, which yields to the Week 2 trigonometric substitution $u=\tan\theta$. The closed form is

$$L = \sqrt{1+e^{2x}} + \frac12\ln\!\left(\frac{\sqrt{1+e^{2x}}-1}{\sqrt{1+e^{2x}}+1}\right)\Bigg|_0^1 \approx \boxed{2.00350}$$

*Verified: the CAS returns a closed form, and it agrees with numerical quadrature to 15 significant figures ($2.00349711162735$).*

**(c)** The structural difference: after $u=e^x$, the $e^x$ case becomes an **algebraic** integrand — a rational function of $u$ and $\sqrt{1+u^2}$ — and algebraic integrands of that shape are exactly what trigonometric substitution was built for.

For $y=\sin x$ the integrand is $\sqrt{1+\cos^2x}$, and **no substitution removes the trigonometric function from under the root**: you are left with the square root of a quadratic *in $\cos x$*, which is an **elliptic** integral and provably not elementary.

*Marking: 1 + 3 + 2. **Full marks on (b) require actually finding the closed form or clearly identifying the route**; asserting "it is elementary" earns 1 of the 3. **(c) must identify that the substitution makes one algebraic and leaves the other trigonometric.***

> **This problem exists because the expected answer is wrong.** $\sqrt{1+e^{2x}}$ looks at least as
> hopeless as $\sqrt{1+\cos^2x}$, and is not. **Looking intractable is not evidence.** Worth saying
> to the room.

---

## Part D — Concept (10 pts each)

### D1 (10) — one pattern, four formulas

| | Slice | Each piece ≈ | Formula |
|---|---|---|---|
| **(a)** Discs | slabs ⊥ to the axis, thickness $\Delta x$ | a disc of radius $f(x)$, area $\pi f^2$ | $V=\pi\int f^2dx$ |
| **(b)** Shells | strips ∥ to the axis, width $\Delta x$ | a tube: unrolled, $2\pi x\cdot f(x)\cdot\Delta x$ | $V=2\pi\int xf\,dx$ |
| **(c)** Arc length | short arcs over $\Delta x$ | a chord, $\sqrt{(\Delta x)^2+(\Delta y)^2}$ | $L=\int\sqrt{1+(f')^2}\,dx$ |
| **(d)** Surface | bands over $\Delta x$ | a frustum, $2\pi f(x)\cdot\Delta s$ | $S=2\pi\int f\sqrt{1+(f')^2}\,dx$ |

**Why $ds$ and not $dx$ in (d):** the band is a slice of a *cone*, not a cylinder. Its width along the surface is the **slant** length $\Delta s$, which exceeds the horizontal extent $\Delta x$ whenever the curve is not flat.

**What goes wrong with $dx$:** you would get $S=2\pi\int f\,dx$, which **systematically underestimates**, and does so without bound as the curve steepens.

**Test it on the sphere:**

$$2\pi\int_{-r}^{r}\sqrt{r^2-x^2}\,dx = 2\pi\cdot\frac{\pi r^2}{2} = \pi^2r^2 \approx 9.870\,r^2$$

against the true $4\pi r^2\approx 12.566\,r^2$. The ratio is

$$\frac{\pi^2r^2}{4\pi r^2} = \frac\pi4 = 0.7854$$

**— an underestimate of exactly $21.46\%$, and the factor is precisely $\pi/4$.** *(Verified.)*

*A pleasing worked example to put on the board: the wrong method is wrong by a clean constant here, which makes it obvious that the error is structural rather than arithmetic.*

*Marking: 2 per derivation (8), 2 for the $ds$ explanation. **A quoted formula with no derivation earns 1 of its 2.** Full marks on the last part require saying the band is a frustum and that $ds \ge dx$.*

### D2 (10) — two methods, one solid

**(a) Shells:** radius $x$, height $x^2$:

$$V = 2\pi\int_0^2 x\cdot x^2dx = 2\pi\cdot 4 = \boxed{8\pi}$$

**(b) Discs (horizontal slices):** at height $y$, the solid runs from $x=\sqrt y$ to $x=2$, a washer with $R=2$, $r=\sqrt y$, for $y\in[0,4]$:

$$V = \pi\int_0^4\Big[4-y\Big]dy = \pi\big(16-8\big) = \boxed{8\pi}$$

**(c)** They agree. *Verified symbolically: both give $8\pi$.*

**(d)** For $y=\sin x$ on $[0,\pi]$ about the $y$-axis:

**Shells:** $V=2\pi\int_0^\pi x\sin x\,dx = 2\pi^2$ — one line, using a Week 1 integral.

**Discs:** the difficulty is that **$\sin x$ is not one-to-one on $[0,\pi]$.** A horizontal line at height $y\in(0,1)$ meets the curve **twice**, at $x=\arcsin y$ and $x=\pi-\arcsin y$. So the horizontal slice is a *washer* whose two radii are **different branches of the inverse**:

$$V = \pi\int_0^1\Big[(\pi-\arcsin y)^2-(\arcsin y)^2\Big]dy$$

This is evaluable — *verified symbolically to give exactly $2\pi^2$*, confirming the shell answer — but it requires recognising the two branches, expanding, and integrating $\arcsin y$ and $(\arcsin y)^2$.

*Marking: 2 + 3 + 1 + 4. **(d) must name non-injectivity as the cause**, not merely say "discs are harder". A student who writes down the washer integral with both branches has fully understood and should get all 4 even without evaluating it.*

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Discs, washers, shifted axes |
| B (5 × 6) | 30 | Shells, shifted axes |
| C (5 × 6) | 30 | Arc length, surface area, and what is elementary |
| D (2 × 10) | 20 | The pattern; two methods on one solid |
| **Total** | **100** | |

---

## Diagnostic Notes

| Question | Weakness it reveals | Bites in |
|---|---|---|
| **A2 / A4** | $(R-r)^2$, or radii written without a sketch | Midterm 1 |
| **B5** | Radius as $x-c$ regardless of side | Midterm 1 |
| **C3 / C4** | Using $dx$ where $ds$ is required | Midterm 1 |
| **C5** | Assuming "looks hard" means "impossible" | Weeks 9–10 |
| **D2(d)** | Not seeing injectivity as the deciding property | Week 5 (parametric curves) |

**Midterm 1 is next week and covers Weeks 0–4.** The most valuable single instruction for revision: **for every problem, draw it or classify it before computing.** Almost every error above is a computation begun too early.

---

*MATH 142 · Week 4 · PS 4 Solutions · Instructor Only*
