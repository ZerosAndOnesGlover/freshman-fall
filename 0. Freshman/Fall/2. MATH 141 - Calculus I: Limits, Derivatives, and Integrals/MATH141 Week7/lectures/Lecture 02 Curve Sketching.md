# MATH 141 — Calculus I
## Week 7 · Lecture 2 (Tuesday)
### Curve Sketching: The Complete Synthesis

---

**Reading:** Stewart §4.5 | Spivak Ch. 11 (§11.3, applications)

---

## 1. Why Curve Sketching Matters

Up to now, we have studied individual *pieces* of function behavior: domain, limits, continuity, derivatives, concavity. Curve sketching is where every technique from Weeks 1–5 combines into a single, complete picture of a function's global behavior — obtained **without** relying on a graphing calculator or software.

This is not busywork. The ability to predict a function's shape from its formula — before plotting a single point — is the clearest evidence that you understand what the derivative and second derivative actually mean.

---

## 2. The Complete Curve Sketching Checklist

For a function $y = f(x)$:

**A. Domain**
Find all $x$ where $f$ is defined.

**B. Intercepts**
- $y$-intercept: $f(0)$ (if $0$ is in the domain)
- $x$-intercepts: solve $f(x) = 0$ (may not always be solvable by hand — sometimes just note existence via IVT)

**C. Symmetry**
- **Even function** ($f(-x)=f(x)$): symmetric about the $y$-axis
- **Odd function** ($f(-x)=-f(x)$): symmetric about the origin
- **Periodic** ($f(x+p)=f(x)$): repeats — only need to sketch one period

**D. Asymptotes**
- **Vertical asymptotes:** where $f\to\pm\infty$ (usually where denominator $=0$, numerator $\neq0$)
- **Horizontal asymptotes:** $\displaystyle\lim_{x\to\pm\infty}f(x)$
- **Slant (oblique) asymptotes:** when $\deg(\text{numerator}) = \deg(\text{denominator})+1$ in a rational function — find via polynomial division

**E. Intervals of Increase/Decrease**
Find $f'(x)$; determine sign on each interval between critical numbers.

**F. Local Extrema**
Classify each critical number using First or Second Derivative Test.

**G. Concavity and Inflection Points**
Find $f''(x)$; determine sign on each interval; locate inflection points.

**H. Sketch**
Combine all information into a single accurate graph.

---

## 3. Slant Asymptotes — A New Technique

For a rational function $f(x) = \dfrac{P(x)}{Q(x)}$ where $\deg P = \deg Q + 1$, polynomial long division gives:

$$f(x) = (\text{linear function}) + \frac{R(x)}{Q(x)}$$

where the remainder term $\to 0$ as $x\to\pm\infty$. The linear part is the **slant asymptote**.

**Example:** $f(x) = \dfrac{x^2-1}{x}$

Divide: $\dfrac{x^2-1}{x} = x - \dfrac{1}{x}$

As $x\to\pm\infty$, $\dfrac{1}{x}\to0$, so $f(x) \to x$. **Slant asymptote:** $y = x$.

Also: vertical asymptote at $x=0$ (denominator zero, numerator $=-1\neq0$).

---

## 4. Fully Worked Example 1 — Rational Function

$$f(x) = \frac{x^2}{x^2-4}$$

**A. Domain:** $x^2-4\neq0 \implies x\neq\pm2$. Domain: $(-\infty,-2)\cup(-2,2)\cup(2,\infty)$.

**B. Intercepts:** $f(0)=0/(-4)=0$. So $(0,0)$ is both $x$- and $y$-intercept.

**C. Symmetry:** $f(-x) = \dfrac{x^2}{x^2-4} = f(x)$. **Even function** — symmetric about $y$-axis.

**D. Asymptotes:**

*Vertical:* at $x=\pm2$ (denominator zero, numerator nonzero there):
$$\lim_{x\to2^+}f(x) = \frac{4}{0^+} = +\infty \qquad \lim_{x\to2^-}f(x) = \frac{4}{0^-} = -\infty$$

By symmetry, similarly at $x=-2$.

*Horizontal:* $\displaystyle\lim_{x\to\pm\infty}\frac{x^2}{x^2-4} = \lim_{x\to\pm\infty}\frac{1}{1-4/x^2} = 1$. **Horizontal asymptote:** $y=1$.

**E. First derivative:**
$$f'(x) = \frac{2x(x^2-4)-x^2(2x)}{(x^2-4)^2} = \frac{2x^3-8x-2x^3}{(x^2-4)^2} = \frac{-8x}{(x^2-4)^2}$$

Critical number: $x=0$ (numerator zero; note $x=\pm2$ are not in the domain, so not critical numbers — they're excluded points).

Sign: $f'(x)>0$ for $x<0$ (excluding $-2$), $f'(x)<0$ for $x>0$ (excluding $2$).

**Increasing** on $(-\infty,-2)\cup(-2,0)$; **decreasing** on $(0,2)\cup(2,\infty)$.

**F. Local extrema:** $x=0$: sign change $+\to-$: **local maximum**, $f(0)=0$.

**G. Second derivative:**
$$f''(x) = \frac{-8(x^2-4)^2 - (-8x)\cdot2(x^2-4)(2x)}{(x^2-4)^4} = \frac{-8(x^2-4)+32x^2}{(x^2-4)^3} = \frac{24x^2+32}{(x^2-4)^3}$$

Numerator $24x^2+32>0$ always. Sign of $f''$ follows sign of $(x^2-4)^3$, i.e., sign of $(x^2-4)$.

$f''>0$ when $|x|>2$; $f''<0$ when $|x|<2$.

**Concave up** on $(-\infty,-2)\cup(2,\infty)$; **concave down** on $(-2,2)$.

No inflection points (concavity changes only at the excluded points $x=\pm2$, which are not in the domain).

**H. Sketch summary:** Symmetric bowl-shaped curve near $x=0$ (local max at origin), diving to $-\infty$ approaching $x=\pm2$ from inside, jumping to $+\infty$ approaching from outside, then settling toward horizontal asymptote $y=1$ on both far sides.

---

## 5. Fully Worked Example 2 — Exponential Function

$$f(x) = xe^{-x}$$

**A. Domain:** $\mathbb{R}$

**B. Intercepts:** $f(0)=0$. Only $x$-intercept: $x=0$ (since $e^{-x}\neq0$ ever).

**C. Symmetry:** $f(-x)=-xe^{x}\neq\pm f(x)$ in general — no symmetry.

**D. Asymptotes:**

As $x\to\infty$: $f(x)=xe^{-x}\to0$ (exponential decay dominates, per L'Hôpital: $\lim_{x\to\infty}\dfrac{x}{e^x}=0$). **Horizontal asymptote:** $y=0$ as $x\to\infty$.

As $x\to-\infty$: $f(x) = xe^{-x}\to-\infty\cdot\infty = -\infty$. No horizontal asymptote on this side.

**E. First derivative:**
$$f'(x) = e^{-x} + x(-e^{-x}) = e^{-x}(1-x)$$

Critical number: $x=1$ ($e^{-x}$ never zero).

Sign: $e^{-x}>0$ always; sign follows $(1-x)$: positive for $x<1$, negative for $x>1$.

**Increasing** $(-\infty,1)$; **decreasing** $(1,\infty)$.

**F. Local extrema:** $x=1$: $+\to-$: **local maximum**. $f(1)=e^{-1}=1/e\approx0.368$.

**G. Second derivative:**
$$f''(x) = -e^{-x}(1-x)+e^{-x}(-1) = e^{-x}[-(1-x)-1] = e^{-x}(x-2)$$

Critical number: $x=2$.

Sign: $-$ for $x<2$, $+$ for $x>2$.

**Concave down** $(-\infty,2)$; **concave up** $(2,\infty)$. **Inflection point** at $x=2$: $f(2)=2e^{-2}\approx0.271$.

**H. Sketch summary:** Rises from $-\infty$ (steeply, from lower left), crosses through origin, peaks at $(1, 1/e)$, then decreases, has an inflection point at $(2, 2/e^2)$ where it becomes concave up, and flattens toward $y=0$ as $x\to\infty$.

---

## 6. Fully Worked Example 3 — Slant Asymptote Case

$$f(x) = \frac{x^3}{x^2+1}$$

**A. Domain:** $\mathbb{R}$ ($x^2+1$ never zero)

**B. Intercepts:** $f(0)=0$; only $x$-intercept is $x=0$.

**C. Symmetry:** $f(-x) = \dfrac{-x^3}{x^2+1} = -f(x)$. **Odd function** — symmetric about origin.

**D. Asymptotes:** No vertical asymptotes (domain is all of $\mathbb{R}$).

$\deg(\text{num})=3$, $\deg(\text{denom})=2$ — degree difference of 1, so check for slant asymptote via division:

$$\frac{x^3}{x^2+1} = x - \frac{x}{x^2+1}$$

As $x\to\pm\infty$, $\dfrac{x}{x^2+1}\to0$. **Slant asymptote:** $y=x$.

**E. First derivative:**
$$f'(x) = \frac{3x^2(x^2+1)-x^3(2x)}{(x^2+1)^2} = \frac{3x^4+3x^2-2x^4}{(x^2+1)^2} = \frac{x^4+3x^2}{(x^2+1)^2} = \frac{x^2(x^2+3)}{(x^2+1)^2}$$

Numerator: $x^2(x^2+3)\geq0$ always (zero only at $x=0$). So $f'(x)\geq0$ everywhere.

**Increasing on all of $\mathbb{R}$** (with a momentary flat point at $x=0$, but never decreasing).

**F. Local extrema:** None — $f'$ doesn't change sign at $x=0$ (nonnegative on both sides).

**G. Second derivative:** (details omitted for brevity — students should complete)

By symmetry (odd function), expect inflection point at $x=0$ and possibly others symmetric about origin.

**H. Sketch summary:** A monotonically increasing S-shaped curve, symmetric about the origin, approaching the line $y=x$ asymptotically in both directions, with a flat inflection at the origin.

---

## 7. Strategy Notes for Sketching

- **Do algebra first, calculus second.** Simplify the function, factor when possible, before differentiating — this often reveals symmetry or asymptotes immediately.
- **Symmetry cuts your work in half.** If $f$ is even or odd, only analyze $x \geq 0$ and reflect.
- **Watch for excluded points vs. actual asymptotes.** A rational function's domain exclusions might be removable discontinuities (Week 2!) rather than vertical asymptotes — always check whether the numerator also vanishes there.
- **Cross-check with limits at infinity** to make sure your asymptote analysis is consistent with your increasing/decreasing analysis (e.g., if $f$ is increasing and approaching a horizontal asymptote from below, this should be geometrically consistent).

---

## 8. CS Connection — Why This Skill Transfers

The discipline of predicting shape from formula — without plotting — is exactly the skill used in:

- **Complexity analysis:** predicting the *shape* of a runtime function (does it plateau? blow up? have a sweet spot?) from its formula, without running the code
- **Loss landscape visualization:** understanding qualitatively where a loss function has minima, saddle points, and how it behaves at the boundaries of parameter space — the multivariable generalization of everything in this lecture
- **Numerical stability analysis:** knowing where a function's derivative is large (sensitive to input perturbation) vs. small (robust) informs which computations are numerically risky

---

## Lecture 2 Exercises

Perform a complete curve sketching analysis (all 8 steps: domain, intercepts, symmetry, asymptotes, increase/decrease, extrema, concavity, inflection points) for:

1. $f(x) = \dfrac{x}{x^2-1}$

2. $f(x) = x^4 - 4x^3$

3. $f(x) = \dfrac{x^3}{3} - x$

4. $f(x) = xe^{x}$

5. $f(x) = \dfrac{x^2-2x+4}{x-2}$ *(has a slant asymptote — find it)*

6. **(Challenge)** $f(x) = x^{2/3}(x-5)$. Note: this function has a cusp (recall Week 2!). Include this in your analysis of "special points."

---


### Answers

Each answer lists the load-bearing features; a complete solution also shows the sign charts.

**1.** $f(x)=\dfrac{x}{x^2-1}$
Domain $x\neq\pm1$. **Odd** ($f(-x)=-f(x)$). Vertical asymptotes $x=\pm1$; horizontal $y=0$.
$f'=\dfrac{-(x^2+1)}{(x^2-1)^2}<0$ **everywhere** on the domain — decreasing on each of the three
pieces, and therefore **no local extrema at all**.
$f''=\dfrac{2x(x^2+3)}{(x^2-1)^3}$; inflection at $\boxed{(0,0)}$.

> A frequent error: reading "decreasing on $(-\infty,-1)$, $(-1,1)$, $(1,\infty)$" as "decreasing on
> $\mathbb{R}\setminus\{\pm1\}$". It is **not** one decreasing function — values jump across the
> asymptotes.

**2.** $f=x^4-4x^3$. $f'=4x^2(x-3)$; critical $x=0,3$. At $x=0$ the sign of $f'$ does **not** change
(the $x^2$ factor) → no extremum; at $x=3$ it changes $-\to+$ → local **min** $\boxed{(3,-27)}$.
$f''=12x(x-2)$ → inflections at $\boxed{(0,0)}$ and $\boxed{(2,-16)}$. Note $x=0$ is a critical
point *and* an inflection, but not an extremum.

**3.** $f=\tfrac{x^3}{3}-x$. **Odd.** $f'=x^2-1$ → local **max** $\boxed{(-1,\tfrac23)}$, local
**min** $\boxed{(1,-\tfrac23)}$. $f''=2x$ → inflection $\boxed{(0,0)}$.

**4.** $f=xe^x$. Domain $\mathbb{R}$. $f'=(1+x)e^x$ → local **min** at $\boxed{(-1,-e^{-1})}$.
$f''=(2+x)e^x$ → inflection at $\boxed{(-2,-2e^{-2})}$.
As $x\to-\infty$, $f\to0^-$ (horizontal asymptote $y=0$ **on the left only**); as $x\to+\infty$,
$f\to+\infty$. A one-sided asymptote is easy to miss.

**5.** $f=\dfrac{x^2-2x+4}{x-2}$. Long division gives $\boxed{f(x)=x+\dfrac{4}{x-2}}$, so the
**slant asymptote is $y=x$** and there is a vertical asymptote at $x=2$.
$f'=1-\dfrac{4}{(x-2)^2}=0$ at $x=0,4$ → local **max** $(0,-2)$, local **min** $(4,6)$.
$f''=\dfrac{8}{(x-2)^3}$ — no inflection (it never vanishes), concave down for $x<2$, up for $x>2$.

**Find a slant asymptote by division, not by guessing** — it exists exactly when the numerator's
degree exceeds the denominator's by exactly 1.

**6.** $f=x^{2/3}(x-5)=x^{5/3}-5x^{2/3}$.
$$f'=\tfrac53x^{2/3}-\tfrac{10}3x^{-1/3}=\frac{5(x-2)}{3x^{1/3}}$$
Critical numbers: $x=2$ (where $f'=0$) and $\boxed{x=0}$ (where $f'$ is **undefined** but $f=0$).

At $x=0$: $f'\to+\infty$ from the left and $-\infty$ from the right — a **cusp**, and a local
**maximum**. At $x=2$: local **min**, $f(2)=-3\sqrt[3]{4}\approx-4.76$.
$f''=\dfrac{10(x+1)}{9x^{4/3}}$ → inflection at $\boxed{(-1,-6)}$.

The cusp is the whole point: it is an extremum that the Second Derivative Test cannot see and that
solving $f'=0$ alone would never find.

*Next: Wednesday — Applied Optimization: Max/Min Word Problems*
