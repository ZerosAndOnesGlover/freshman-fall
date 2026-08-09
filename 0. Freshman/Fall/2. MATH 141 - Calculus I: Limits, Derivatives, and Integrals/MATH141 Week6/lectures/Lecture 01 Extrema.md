# MATH 141 · Calculus I
## Week 6 · Lecture 1 (Monday)
### Maximum and Minimum Values: Extrema, Critical Points, and the Extreme Value Theorem

---

**Reading:** Stewart §4.1 | Spivak Ch. 11 (§11.1)
**Quiz 06** — this Monday, covers Week 5 (implicit differentiation, logs, inverse trig, related rates)

---

## 1. Why We Care About Extrema

One of the most practically important applications of calculus is **optimization** — finding the best (maximum or minimum) value of a quantity. Engineers minimize cost and material usage; scientists maximize efficiency; machine learning minimizes loss functions. All of this rests on a rigorous theory of extrema, which we build this week.

---

## 2. Absolute vs Local Extrema — Precise Definitions

> **Definition.** $f$ has an **absolute maximum** at $c$ if $f(c) \geq f(x)$ for all $x$ in the domain of $f$. The value $f(c)$ is called the **absolute maximum value**.
>
> $f$ has an **absolute minimum** at $c$ if $f(c) \leq f(x)$ for all $x$ in the domain. Similarly for absolute minimum value.
>
> Together: **absolute extrema** (also called **global extrema**).

> **Definition.** $f$ has a **local maximum** at $c$ if $f(c) \geq f(x)$ for all $x$ **near** $c$ (i.e., in some open interval containing $c$).
>
> $f$ has a **local minimum** at $c$ if $f(c) \leq f(x)$ for all $x$ near $c$.

**Key distinction:** Local extrema are about behavior *near* a point; absolute extrema are about behavior over the *entire domain*. Every absolute extremum that occurs in the interior of the domain is also a local extremum, but not every local extremum is absolute.

**Example:** For $f(x) = x^3 - 3x$ on $[-3, 3]$:
- Local max at $x = -1$: $f(-1) = 2$
- Local min at $x = 1$: $f(1) = -2$
- Absolute max at $x = 3$: $f(3) = 18$ (endpoint, not a local max in the interior sense)
- Absolute min at $x = -3$: $f(-3) = -18$

---

## 3. The Extreme Value Theorem (EVT)

> **Theorem (EVT).** If $f$ is continuous on a closed interval $[a,b]$, then $f$ attains both an absolute maximum and an absolute minimum value on $[a,b]$.

**Why both hypotheses matter:**

**Continuity is essential.** Consider $f(x) = \begin{cases} x & 0 \leq x < 1 \\ 0 & x = 1 \end{cases}$ on $[0,1]$. This is discontinuous at $x=1$ and has no maximum — values get arbitrarily close to 1 but never reach it (since $f(1)=0$, not 1).

**Closed interval is essential.** Consider $f(x) = x$ on $(0,1)$ (open interval). $f$ is continuous but has no maximum or minimum — the interval has no endpoints to attain them.

**Bounded interval is essential.** Consider $f(x) = x$ on $[0, \infty)$. Continuous, closed at one end, but unbounded — no maximum exists.

The EVT is a **pure existence theorem**: it guarantees that extrema exist, but says nothing about how to find them. That's the job of the next section.

---

## 4. Critical Numbers — Where Extrema Can Occur

> **Definition.** A **critical number** of $f$ is a number $c$ in the domain of $f$ such that either $f'(c) = 0$ or $f'(c)$ does not exist.

**Fermat's Theorem.** If $f$ has a local maximum or minimum at $c$, and $f'(c)$ exists, then $f'(c) = 0$.

**Proof sketch:** Suppose $f$ has a local max at $c$ and $f'(c)$ exists. For small $h > 0$:
$$\frac{f(c+h)-f(c)}{h} \leq 0 \implies \lim_{h\to0^+}\frac{f(c+h)-f(c)}{h} \leq 0$$

For small $h < 0$:
$$\frac{f(c+h)-f(c)}{h} \geq 0 \implies \lim_{h\to0^-}\frac{f(c+h)-f(c)}{h} \geq 0$$

Since $f'(c)$ exists, both one-sided limits equal $f'(c)$. So $f'(c) \leq 0$ and $f'(c) \geq 0$, forcing $f'(c) = 0$. $\square$

> ⚠️ **The converse is FALSE.** $f'(c) = 0$ does NOT imply a local extremum at $c$. Classic counterexample: $f(x) = x^3$ has $f'(0) = 0$, but $x=0$ is neither a local max nor min — it's an **inflection point** (saddle behavior).

**Why we need "or $f'(c)$ does not exist":** Consider $f(x) = |x|$. It has a local (and absolute) minimum at $x=0$, but $f'(0)$ does not exist (corner). Fermat's theorem doesn't apply directly, but the extremum still occurs at a critical number — this is why the critical number definition includes both cases.

---

## 5. The Closed Interval Method — Finding Absolute Extrema

To find the absolute maximum and minimum of a **continuous** function $f$ on a **closed interval** $[a,b]$:

1. Find all critical numbers of $f$ in the open interval $(a,b)$
2. Evaluate $f$ at each critical number
3. Evaluate $f$ at the two endpoints $a$ and $b$
4. The largest value from steps 2–3 is the absolute maximum; the smallest is the absolute minimum

**Why this works:** By the EVT, absolute extrema exist. If an extremum occurs at an interior point, by Fermat's theorem that point must be a critical number. If it occurs at an endpoint, it's automatically included in step 3. There is nowhere else an extremum could hide.

### Example 1

Find the absolute max/min of $f(x) = x^3 - 3x^2 + 1$ on $[-1, 4]$.

**Step 1 — Critical numbers:** $f'(x) = 3x^2 - 6x = 3x(x-2)$.

$f'(x) = 0 \implies x = 0$ or $x = 2$. Both are in $(-1,4)$. ($f'$ is defined everywhere, so no other critical numbers.)

**Step 2 — Evaluate at critical numbers:**
$f(0) = 1$
$f(2) = 8 - 12 + 1 = -3$

**Step 3 — Evaluate at endpoints:**
$f(-1) = -1 - 3 + 1 = -3$
$f(4) = 64 - 48 + 1 = 17$

**Step 4 — Compare:** $\{1, -3, -3, 17\}$.

**Absolute maximum:** $17$ at $x=4$.
**Absolute minimum:** $-3$, attained at BOTH $x=2$ and $x=-1$.

### Example 2 — Non-differentiable critical point

Find the absolute max/min of $f(x) = x^{2/3}$ on $[-1, 8]$.

$f'(x) = \dfrac{2}{3}x^{-1/3} = \dfrac{2}{3\sqrt[3]{x}}$

$f'(x)$ is never zero (numerator is constant $2/3 \neq 0$), but $f'(0)$ is undefined. Critical number: $x = 0$.

**Evaluate:**
$f(-1) = 1$
$f(0) = 0$
$f(8) = 4$

**Absolute maximum:** $4$ at $x=8$. **Absolute minimum:** $0$ at $x=0$.

---

## 6. Optimization on Unbounded or Open Intervals

The closed interval method requires $[a,b]$. For open or unbounded intervals, the EVT doesn't guarantee extrema exist. You must analyze behavior directly (often using the First or Second Derivative Test — Week 5) or examine limits at the boundary/infinity.

**Example:** $f(x) = \dfrac{1}{x^2+1}$ on $(-\infty, \infty)$.

$f'(x) = \dfrac{-2x}{(x^2+1)^2} = 0 \implies x = 0$.

$f(0) = 1$. As $x \to \pm\infty$, $f(x) \to 0^+$. Since $f(0)=1 > f(x)$ for all other $x$, this IS the absolute maximum (even without a closed interval, because we can verify it directly). There is no absolute minimum (infimum $0$ is never attained).

---

## 7. CS Connection — Optimization Everywhere

Extrema-finding is the mathematical core of nearly every optimization problem in computer science:

**Machine learning:** Training a model = minimizing a loss function $L(\theta)$ over parameters $\theta$. Critical points ($\nabla L = 0$) are candidates for minima — exactly Fermat's theorem generalized to multiple variables.

**Algorithm design:** Many algorithms (e.g., convex optimization solvers, gradient descent) rely on the guarantee that a continuous function on a closed, bounded (compact) set attains its extrema — a multivariable generalization of the EVT.

**Resource allocation:** Constrained optimization (Lagrange multipliers, in multivariable calculus) finds the best allocation of limited resources — literally "closed interval method" generalized to higher dimensions.

**Why local ≠ global matters in ML:** Neural network loss landscapes have many local minima ($f'=0$ points that aren't the true global minimum). This is exactly the warning from Fermat's theorem's converse failing — gradient descent can get stuck at a critical point that isn't the best possible value.

---

## Lecture 1 Exercises

1. Find all critical numbers of:
   - (a) $f(x) = 2x^3 - 3x^2 - 12x + 5$
   - (b) $g(x) = \dfrac{x}{x^2+1}$
   - (c) $h(x) = x^{4/5}(x-4)^2$
   - (d) $k(x) = |x^2 - 4|$

2. Use the Closed Interval Method to find the absolute max and min:
   - (a) $f(x) = x^4 - 2x^2 + 3$ on $[-2, 2]$
   - (b) $f(x) = x + \dfrac{1}{x}$ on $[0.5, 4]$
   - (c) $f(x) = 2\cos x + \sin(2x)$ on $[0, \pi/2]$

3. Give an example of a function on $[0,1]$ that is discontinuous at exactly one point and has no absolute maximum. Sketch it.

4. **(Fermat's Theorem converse)** Verify that $f(x) = x^3$ has $f'(0) = 0$ but that $x=0$ is neither a local max nor min. Explain using the sign of $f'(x)$ near $x=0$.

5. **(Synthesis)** A continuous function $f$ on $[0, 10]$ satisfies $f(0) = 3$, $f(10) = 3$, and has exactly one critical number at $x = 5$ where $f(5) = 8$. What can you conclude about the absolute max and min of $f$ on $[0,10]$? Is more information needed?

---


### Answers

**1.** Critical numbers are where $f'=0$ **or** $f'$ is undefined *while $f$ is defined*.

**(a)** $f'=6x^2-6x-12=6(x-2)(x+1)$ → $\boxed{x=-1,\ 2}$
**(b)** $g'=\dfrac{1-x^2}{(x^2+1)^2}$ → $\boxed{x=\pm1}$
**(c)** $h'=\dfrac{(x-4)(14x-16)}{5\,x^{1/5}}$ → $\boxed{x=0,\ \tfrac87,\ 4}$. Note $x=0$ counts:
$h'$ is **undefined** there but $h(0)=0$ exists.
**(d)** $k=|x^2-4|$ → $\boxed{x=0,\ \pm2}$. The points $\pm2$ are **corners** (derivative undefined);
$x=0$ is where the inside parabola turns.

> (c) and (d) are the point of the exercise: **critical numbers include points where $f'$ fails to
> exist.** Solving $f'=0$ alone misses corners and cusps.

**2.** Closed Interval Method — evaluate at critical numbers **and both endpoints**.

**(a)** Critical $x=0,\pm1$. Values: $f(\pm2)=11$, $f(\pm1)=2$, $f(0)=3$.
Max $\boxed{11}$ at $x=\pm2$; min $\boxed{2}$ at $x=\pm1$.

**(b)** $f'=1-\tfrac1{x^2}=0 \Rightarrow x=1$. Values: $f(0.5)=2.5$, $f(1)=2$, $f(4)=4.25$.
Max $\boxed{4.25}$ at $x=4$; min $\boxed{2}$ at $x=1$.

**(c)** $f'=-2\sin x+2\cos2x=2(1-\sin x-2\sin^2x)$; with $s=\sin x$, $(2s-1)(s+1)=0$ gives
$s=\tfrac12$, i.e. $x=\pi/6$. Values: $f(0)=2$, $f(\pi/6)=\tfrac{3\sqrt3}{2}\approx2.598$,
$f(\pi/2)=0$.
Max $\boxed{\tfrac{3\sqrt3}{2}}$ at $x=\pi/6$; min $\boxed{0}$ at $x=\pi/2$.
*(Confirmed by scanning 200 points across the interval.)*

**3.** For example
$$f(x)=\begin{cases}x & 0\leq x<1\\ 0 & x=1\end{cases}$$
It is discontinuous only at $x=1$. The supremum is $1$ but it is **never attained** — values
approach 1 without reaching it. This is exactly the EVT's continuity hypothesis failing.

**4.** $f(x)=x^3$: $f'(x)=3x^2$, so $f'(0)=0$ ✓. But $f'(x)=3x^2>0$ for **all** $x\neq0$ — the
derivative does not change sign, so $f$ is increasing on both sides and $x=0$ is neither a max nor
a min (it is a horizontal inflection).

**Fermat's Theorem is one-directional:** an interior extremum forces $f'=0$, but $f'=0$ does not
force an extremum. This is precisely why the First Derivative *sign* Test exists.

**5.** $f$ is continuous on a closed bounded interval, so the EVT guarantees both extrema exist. The
only candidates are the critical number and the endpoints: $f(0)=3$, $f(5)=8$, $f(10)=3$.

**Absolute max $=\boxed{8}$ at $x=5$; absolute min $=\boxed{3}$, attained at both $x=0$ and $x=10$.**

**No further information is needed** — the candidate list is complete. That completeness is what
makes the Closed Interval Method a *method* rather than a search: with continuity on $[a,b]$, the
extrema can only occur at critical numbers or endpoints, and here all three have been evaluated.

*Next: Tuesday — Rolle's Theorem and the Mean Value Theorem*
