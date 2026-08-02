# MATH 141 · Calculus I
## Week 7 · Lecture 1 (Wednesday)
### Derivatives and the Shape of a Graph: Increasing/Decreasing, Concavity, and the First & Second Derivative Tests

---

**Reading:** Stewart §4.3 | Spivak Ch. 11 (§11.3)
**Problem Set 4 released today. Due: Wednesday, Week 7.**

---

## 1. The Increasing/Decreasing Test

From Tuesday's MVT Corollary 3:

> **I/D Test.** If $f'(x) > 0$ on an interval, $f$ is increasing there. If $f'(x) < 0$, $f$ is decreasing there.

**Procedure to find intervals of increase/decrease:**
1. Find $f'(x)$
2. Find critical numbers (where $f'=0$ or undefined)
3. These divide the domain into intervals — use a sign chart (like Week 0's inequality method) to test the sign of $f'$ on each interval

### Example 1

Find intervals of increase/decrease for $f(x) = x^4 - 4x^3$.

$f'(x) = 4x^3 - 12x^2 = 4x^2(x-3)$

Critical numbers: $x = 0$, $x = 3$.

| Interval | $(-\infty, 0)$ | $(0,3)$ | $(3,\infty)$ |
|----------|---------------|---------|--------------|
| Test point | $-1$ | $1$ | $4$ |
| $4x^2$ | $+$ | $+$ | $+$ |
| $(x-3)$ | $-$ | $-$ | $+$ |
| $f'(x)$ | $-$ | $-$ | $+$ |

$f$ is **decreasing** on $(-\infty, 3)$ and **increasing** on $(3, \infty)$.

Note: even though $x=0$ is a critical number, $f'$ doesn't change sign there (negative on both sides) — so $x=0$ is neither a local max nor min.

---

## 2. The First Derivative Test

> **First Derivative Test.** Suppose $c$ is a critical number of a continuous function $f$.
> - If $f'$ changes from positive to negative at $c$: $f$ has a **local maximum** at $c$.
> - If $f'$ changes from negative to positive at $c$: $f$ has a **local minimum** at $c$.
> - If $f'$ does not change sign at $c$: $f$ has **no local extremum** at $c$.

This follows directly from the I/D test: positive-to-negative means the function stops increasing and starts decreasing — a peak.

### Example 2 (continuing Example 1)

From the sign chart above:

- At $x=0$: $f'$ is negative on both sides — **no extremum**.
- At $x=3$: $f'$ changes from negative to positive — **local minimum**. $f(3) = 81 - 108 = -27$.

---

## 3. Concavity — The Second Derivative

Increasing/decreasing describes the direction a curve moves. **Concavity** describes how it curves.

> **Definition.** If the graph of $f$ lies above all its tangent lines on an interval $I$, $f$ is **concave upward** on $I$. If it lies below all its tangent lines, $f$ is **concave downward** on $I$.

**Concavity Test:**

> If $f''(x) > 0$ on an interval, $f$ is concave upward there.
> If $f''(x) < 0$ on an interval, $f$ is concave downward there.

**Why this makes sense:** $f''(x) > 0$ means $f'(x)$ is increasing — the slope is getting steeper (more positive or less negative) as $x$ increases. A curve whose slope is always increasing bends upward, like a bowl (⌣).

**Intuition:** Concave up = "holds water." Concave down = "spills water."

### Inflection Points

> **Definition.** A point $(c, f(c))$ is an **inflection point** if $f$ is continuous there and the concavity changes (from up to down, or down to up).

At an inflection point, $f''(c) = 0$ or $f''(c)$ is undefined — but the converse is not automatic; you must verify concavity actually changes.

### Example 3

Find intervals of concavity and inflection points for $f(x) = x^4 - 4x^3$ (continuing from before).

$f'(x) = 4x^3-12x^2$; $f''(x) = 12x^2 - 24x = 12x(x-2)$

Critical numbers of $f''$: $x = 0$, $x=2$.

| Interval | $(-\infty,0)$ | $(0,2)$ | $(2,\infty)$ |
|----------|--------------|---------|--------------|
| $12x$ | $-$ | $+$ | $+$ |
| $(x-2)$ | $-$ | $-$ | $+$ |
| $f''(x)$ | $+$ | $-$ | $+$ |

Concave up on $(-\infty,0)\cup(2,\infty)$; concave down on $(0,2)$.

**Inflection points:** concavity changes at both $x=0$ and $x=2$.

$f(0) = 0$: inflection point $(0,0)$.
$f(2) = 16-32=-16$: inflection point $(2,-16)$.

---

## 4. The Second Derivative Test

An alternative to the First Derivative Test for classifying critical points:

> **Second Derivative Test.** Suppose $f''$ is continuous near $c$, and $f'(c) = 0$.
> - If $f''(c) > 0$: $f$ has a **local minimum** at $c$.
> - If $f''(c) < 0$: $f$ has a **local maximum** at $c$.
> - If $f''(c) = 0$: **the test is inconclusive** — must use the First Derivative Test instead.

**Intuition:** $f'(c)=0$ means horizontal tangent. $f''(c)>0$ means concave up near $c$ — a horizontal tangent on a concave-up curve is a valley (local min). $f''(c)<0$ means concave down — a horizontal tangent there is a peak (local max).

### Example 4 — When the Second Derivative Test Fails

$f(x) = x^4$. $f'(x) = 4x^3 = 0 \implies x=0$. $f''(x) = 12x^2$, so $f''(0) = 0$ — **inconclusive**.

Use the First Derivative Test instead: $f'(x) = 4x^3$ is negative for $x<0$, positive for $x>0$. Sign change negative→positive: **local minimum** at $x=0$. (In fact, absolute minimum, since $x^4 \geq 0$ always.)

This example shows precisely why the Second Derivative Test has a genuine gap that the First Derivative Test fills.

### Example 5 — Applying the Second Derivative Test

$f(x) = x^3 - 3x^2 - 9x + 5$

$f'(x) = 3x^2-6x-9 = 3(x-3)(x+1)$. Critical numbers: $x=-1, 3$.

$f''(x) = 6x-6$

$f''(-1) = -6-6=-12 < 0$: **local maximum** at $x=-1$. $f(-1) = -1-3+9+5=10$.

$f''(3) = 18-6=12>0$: **local minimum** at $x=3$. $f(3)=27-27-27+5=-22$.

---

## 5. Comprehensive Curve Analysis — Putting It Together

**Full procedure for analyzing $f$:**
1. Find domain
2. Find $f'(x)$; find critical numbers; determine intervals of increase/decrease
3. Apply First (or Second) Derivative Test to classify local extrema
4. Find $f''(x)$; determine intervals of concavity; find inflection points
5. Find any asymptotes (Week 1 techniques)
6. Sketch the graph using all of the above

### Full Example

Analyze $f(x) = 3x^5 - 5x^3$ completely.

**Domain:** $\mathbb{R}$ (polynomial)

**First derivative:** $f'(x) = 15x^4 - 15x^2 = 15x^2(x^2-1) = 15x^2(x-1)(x+1)$

Critical numbers: $x = -1, 0, 1$.

| Interval | $(-\infty,-1)$ | $(-1,0)$ | $(0,1)$ | $(1,\infty)$ |
|----------|---------------|----------|---------|--------------|
| $f'(x)$ sign | $+$ | $-$ | $-$ | $+$ |

Increasing on $(-\infty,-1)\cup(1,\infty)$; decreasing on $(-1,1)$.

**Classify critical points (First Derivative Test):**
- $x=-1$: $+\to-$: **local max**. $f(-1) = -3+5=2$.
- $x=0$: $-\to-$ (no sign change): **not an extremum**.
- $x=1$: $-\to+$: **local min**. $f(1)=3-5=-2$.

**Second derivative:** $f''(x) = 60x^3-30x = 30x(2x^2-1)$

Zero at $x=0, \pm\dfrac{1}{\sqrt2}$.

| Interval | $\left(-\infty,-\frac{1}{\sqrt2}\right)$ | $\left(-\frac1{\sqrt2},0\right)$ | $\left(0,\frac1{\sqrt2}\right)$ | $\left(\frac1{\sqrt2},\infty\right)$ |
|---|---|---|---|---|
| $f''(x)$ sign | $-$ | $+$ | $-$ | $+$ |

Concave down, up, down, up — **three inflection points**: $x=-\dfrac{1}{\sqrt2}, 0, \dfrac{1}{\sqrt2}$.

This function has rich structure: two local extrema and three inflection points, all found systematically from the sign patterns of $f'$ and $f''$.

---

## 6. CS Connection — Convexity in Optimization

**Concave up = convex function** (in optimization terminology). Convex functions are extremely important:

- A convex function has the property that any local minimum is automatically the **global minimum** — this is why convex optimization problems (found throughout machine learning: linear regression, SVM, many neural network loss surfaces under certain conditions) are "easy" to solve reliably.
- Gradient descent is *guaranteed* to converge to the true minimum on a convex function — this is a direct generalization of the concavity theory in this lecture to multiple dimensions.
- Testing $f''(x) \geq 0$ everywhere is exactly how we verify a function is convex — the multivariable analog uses the **Hessian matrix** (a matrix of all second partial derivatives) being positive semi-definite.

Understanding concavity here is the direct foundation for understanding why some ML optimization problems are tractable and others (non-convex, like deep neural network training) are fundamentally harder — they can have many local minima that are not global.

---

## Lecture 3 Exercises

1. Find intervals of increase/decrease and classify all local extrema using the First Derivative Test:
   - (a) $f(x) = 2x^3 + 3x^2 - 12x$
   - (b) $f(x) = x^4 - 8x^2 + 2$
   - (c) $f(x) = \dfrac{x}{x^2+1}$

2. Find intervals of concavity and all inflection points:
   - (a) $f(x) = x^3 - 6x^2 + 9x + 1$
   - (b) $f(x) = xe^{-x}$

3. Use the Second Derivative Test where possible; note where it's inconclusive:
   - (a) $f(x) = x^3 - 3x + 1$
   - (b) $f(x) = x^6$
   - (c) $f(x) = x^4 - 4x^3 + 6x^2$

4. Sketch a function satisfying ALL of the following:
   - $f'(x) > 0$ on $(-\infty, -2)$ and $(1, \infty)$; $f'(x) < 0$ on $(-2, 1)$
   - $f''(x) > 0$ on $(-\infty, -0.5)$; $f''(x) < 0$ on $(-0.5, \infty)$
   - $f(-2) = 5$, $f(1) = -3$

5. **(Proof)** Prove that if $f''(x) > 0$ for all $x$ in an interval $I$, then the graph of $f$ lies above every one of its tangent lines on $I$. *(Hint: fix $a \in I$; define $g(x) = f(x) - [f(a)+f'(a)(x-a)]$ — the vertical gap between curve and tangent line at $a$. Show $g(a)=0$, $g'(a)=0$, and $g''(x)>0$, then use MVT-based reasoning to show $g(x) \geq 0$.)*

6. **(Full analysis)** Perform a complete curve analysis (domain, increase/decrease, extrema, concavity, inflection points) for $f(x) = x^4 - 2x^2$.

---


### Answers

**1.** First Derivative Test — classify by the **sign change** of $f'$.

**(a)** $f'=6x^2+6x-12=6(x+2)(x-1)$. Increasing on $(-\infty,-2)$ and $(1,\infty)$; decreasing on
$(-2,1)$. Local **max** at $\boxed{x=-2}$ ($f=20$), local **min** at $\boxed{x=1}$ ($f=-7$).

**(b)** $f'=4x^3-16x=4x(x-2)(x+2)$. Local **min** at $x=\pm2$ ($f=-14$), local **max** at $x=0$
($f=2$). A symmetric "W".

**(c)** $f'=\dfrac{1-x^2}{(x^2+1)^2}$. Local **min** at $x=-1$ ($f=-\tfrac12$), local **max** at
$x=1$ ($f=\tfrac12$).

**2. (a)** $f''=6x-12=0 \Rightarrow x=2$; concave down on $(-\infty,2)$, up on $(2,\infty)$;
inflection at $\boxed{(2,3)}$.

**(b)** $f=xe^{-x}$, $f'=(1-x)e^{-x}$, $f''=(x-2)e^{-x}$. Concave down on $(-\infty,2)$, up on
$(2,\infty)$; inflection at $\boxed{\left(2,\ 2e^{-2}\right)}$.

**3.** Second Derivative Test: $f'(c)=0$ with $f''(c)>0$ ⇒ min, $f''(c)<0$ ⇒ max, $f''(c)=0$ ⇒
**inconclusive**.

**(a)** $f'=3x^2-3$, critical $x=\pm1$; $f''=6x$. $f''(1)=6>0$ → min; $f''(-1)=-6<0$ → max. ✓
**(b)** $f=x^6$: $f'=6x^5$, critical $x=0$; $f''=30x^4$ and $f''(0)=0$ → **inconclusive**. Fall back
to the sign test: $f'<0$ for $x<0$, $f'>0$ for $x>0$ → **local minimum**.
**(c)** $f=x^4-4x^3+6x^2$: $f'=4x(x^2-3x+3)$. The quadratic has discriminant $9-12=-3<0$, so the
only critical number is $x=0$; $f''=12x^2-24x+12=12(x-1)^2$, and $f''(0)=12>0$ → **local minimum**.
Note $f''(1)=0$ but $x=1$ is *not* an inflection point — $f''\geq0$ never changes sign.

> (b) and (c) together make the point: **$f''=0$ tells you nothing** — neither that an extremum is
> absent (b) nor that an inflection is present (c).

**4.** The description forces: rising to a local **max at $(-2,5)$**, falling to a local **min at
$(1,-3)$**, then rising again; concave **up** left of $x=-0.5$ and concave **down** right of it, so
there is an **inflection point at $x=-0.5$**.

Consistency check worth noting: the max at $x=-2$ sits in the concave-**up** region, which is
unusual but perfectly possible — concavity and the location of extrema are independent pieces of
information.

**5.** Fix $a\in I$ and set $g(x)=f(x)-\left[f(a)+f'(a)(x-a)\right]$, the vertical gap between the
curve and its tangent at $a$. Then
$$g(a)=0,\qquad g'(x)=f'(x)-f'(a),\qquad g'(a)=0,\qquad g''=f''>0$$
Since $g''>0$, $g'$ is **strictly increasing**; as $g'(a)=0$, we get $g'<0$ for $x<a$ and $g'>0$ for
$x>a$. So $g$ is decreasing before $a$ and increasing after, making $x=a$ a **strict global minimum
of $g$ on $I$**, with value $g(a)=0$.

Therefore $g(x)\geq0$ for all $x\in I$, i.e. $f(x)\geq f(a)+f'(a)(x-a)$ — the graph lies **above**
every tangent line, with equality only at the point of tangency. $\blacksquare$

This is the analytic definition of convexity, and it is the inequality behind Newton's method
converging from one side, and behind Jensen's inequality in probability.

*Next week: Curve sketching synthesis, L'Hôpital's Rule, and Optimization Problems (applied max/min)*
