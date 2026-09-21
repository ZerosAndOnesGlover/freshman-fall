# MATH 141 · Calculus I
## Week 7 · Lecture 3 (Wednesday)
### Applied Optimization: Maximum and Minimum Problems

**Date:** Wednesday 11 November 2026 · 11:00–11:50 · Week 7

---

**Reading:** Stewart §4.7 | Spivak Ch. 11 (applied problems)
**Problem Set 7 released today, 12:00. Due: Wednesday 18 November 2026, 11:00 (Week 8).**

---

## 1. From Theory to Application

Weeks 4–5 built the complete theory of extrema: critical numbers, the Closed Interval Method, the First and Second Derivative Tests. Today we apply this theory to real optimization problems — finding the best possible design, the minimum cost, the maximum area, subject to real-world constraints.

This is arguably the most practically important skill in this course.

---

## 2. General Strategy for Optimization Problems

1. **Understand the problem.** Read carefully. Identify what quantity is to be maximized or minimized (the **objective**), and what relationships (**constraints**) connect the variables.

2. **Draw a diagram** if the problem is geometric. Label all quantities.

3. **Introduce variables and write the objective function** — the quantity to optimize, as a function of one or more variables.

4. **Use the constraint(s) to reduce to a single variable.** If you have two variables related by a constraint equation, solve for one in terms of the other and substitute.

5. **Determine the domain** of the resulting single-variable function — often restricted by physical meaning (lengths must be positive, etc.).

6. **Find critical numbers** by differentiating and setting equal to zero.

7. **Verify it's actually a maximum or minimum** using the First or Second Derivative Test, or the Closed Interval Method if the domain is closed and bounded.

8. **Answer the original question** — with correct units, and re-check that the answer makes physical sense.

---

## 3. Worked Example 1 — The Classic Box Problem

An open-top box is made from a $12\times12$ cm square piece of cardboard by cutting equal squares from each corner and folding up the sides. Find the size of the cut that maximizes the box's volume.

**Step 1–2:** Let $x$ = side length of each cut square. After folding, the box has:
- base side length: $12 - 2x$
- height: $x$

**Step 3 — Objective function:**
$$V(x) = x(12-2x)^2$$

**Step 4:** Already in terms of a single variable $x$ — no additional constraint substitution needed.

**Step 5 — Domain:** We need $x > 0$ and $12-2x > 0$, i.e., $0 < x < 6$.

**Step 6 — Differentiate:**
$$V'(x) = (12-2x)^2 + x\cdot2(12-2x)(-2) = (12-2x)[(12-2x)-4x] = (12-2x)(12-6x)$$

Set $V'(x)=0$: $x=6$ (excluded — endpoint of open domain) or $x=2$.

**Step 7 — Verify maximum:** Use First Derivative Test. For $x$ slightly less than 2: $(12-2x)>0$, $(12-6x)>0$, so $V'>0$. For $x$ slightly more than 2: $(12-2x)>0$, $(12-6x)<0$, so $V'<0$. Sign change $+\to-$: **local max**.

Since $x=2$ is the only critical number in $(0,6)$ and $V\to0$ at both ends of the domain, this local max is the **absolute maximum**.

**Step 8 — Answer:** Cut squares of side $x=2$ cm. Maximum volume: $V(2) = 2(8)^2 = 128\ \text{cm}^3$.

---

## 4. Worked Example 2 — Minimizing Material (Fixed Volume)

A cylindrical can must hold $500\ \text{cm}^3$ of liquid. Find the dimensions that minimize the amount of metal used (surface area).

**Step 1–2:** Let $r$ = radius, $h$ = height.

**Objective:** minimize surface area $S = 2\pi r^2 + 2\pi rh$ (top + bottom + lateral surface).

**Constraint:** $V = \pi r^2 h = 500$

**Step 4 — Eliminate $h$:** From the constraint, $h = \dfrac{500}{\pi r^2}$.

Substitute:
$$S(r) = 2\pi r^2 + 2\pi r\cdot\frac{500}{\pi r^2} = 2\pi r^2 + \frac{1000}{r}$$

**Step 5 — Domain:** $r > 0$.

**Step 6 — Differentiate:**
$$S'(r) = 4\pi r - \frac{1000}{r^2}$$

Set $S'(r)=0$: $4\pi r = \dfrac{1000}{r^2} \implies r^3 = \dfrac{1000}{4\pi} = \dfrac{250}{\pi} \implies r = \sqrt[3]{\dfrac{250}{\pi}} \approx 4.30\ \text{cm}$

**Step 7 — Verify minimum:** Use Second Derivative Test.
$$S''(r) = 4\pi + \frac{2000}{r^3}$$

Since $r>0$, $S''(r) > 0$ always. **Local minimum confirmed.** Since $S(r)\to\infty$ as $r\to0^+$ and as $r\to\infty$, this is also the **absolute minimum** on $(0,\infty)$.

**Step 8 — Answer:** $r \approx 4.30\ \text{cm}$, and $h = \dfrac{500}{\pi r^2} \approx 8.60\ \text{cm}$ (which turns out to equal $2r$ — a well-known result: the optimal can has height equal to its diameter).

---

## 5. Worked Example 3 — Minimum Distance

Find the point on the parabola $y = x^2$ closest to the point $(0, 3)$.

**Step 1–2:** Let $(x, y)$ be a point on the parabola, so $y = x^2$.

**Objective:** minimize distance $D = \sqrt{x^2+(y-3)^2}$. 

**Trick:** minimizing $D$ is equivalent to minimizing $D^2$ (avoids messy square root derivative, and since $D\geq0$, the minimizer is the same).

$$D^2(x) = x^2 + (x^2-3)^2$$

**Step 5 — Domain:** $x \in \mathbb{R}$ (no restriction).

**Step 6 — Differentiate:**
$$\frac{d}{dx}[D^2] = 2x + 2(x^2-3)(2x) = 2x[1+2(x^2-3)] = 2x(2x^2-5)$$

Set equal to zero: $x=0$ or $x^2 = 5/2 \implies x=\pm\sqrt{5/2}$.

**Step 7 — Verify minimum:** Check via sign analysis or Second Derivative Test. At $x = 0$: this gives $y=0$, distance to $(0,3)$ is 3. At $x = \pm\sqrt{5/2}$: $y = 5/2$, distance is $\sqrt{5/2 + (5/2-3)^2} = \sqrt{5/2+1/4} = \sqrt{11/4} \approx 1.658$.

Since $1.658 < 3$, the points $x = \pm\sqrt{5/2}$ give the **minimum** distance; $x=0$ is a local max in the $D^2$ function (or a saddle in this context — verify with the derivative test).

**Step 8 — Answer:** The closest points are $\left(\pm\sqrt{5/2}, 5/2\right)$, at distance $\sqrt{11}/2 \approx 1.658$.

---

## 6. Worked Example 4 — Optimization with a Boundary (Closed Interval Method)

A rectangular field is to be enclosed by a fence and divided into two equal parts by a fence parallel to one side. If $600$ meters of fencing is available, find the dimensions that maximize the total enclosed area.

**Step 1–2:** Let $x$ = width (the side with the dividing fence — three segments of this length), $y$ = length.

**Total fencing:** $3x + 2y = 600$ (three vertical segments of length $x$, two horizontal segments of length $y$).

**Objective:** maximize area $A = xy$.

**Step 4 — Eliminate $y$:** From constraint: $y = \dfrac{600-3x}{2}$.

$$A(x) = x\cdot\frac{600-3x}{2} = 300x - \frac{3x^2}{2}$$

**Step 5 — Domain:** Need $x>0$ and $y>0 \implies 600-3x>0 \implies x<200$. So $x\in(0,200)$.

**Step 6 — Differentiate:**
$$A'(x) = 300 - 3x$$

Set to zero: $x = 100$.

**Step 7 — Verify:** $A''(x) = -3 < 0$ always: **local max**, and since it's the only critical point in the open interval with $A\to0$ at both ends, it's the **absolute maximum**.

**Step 8 — Answer:** $x=100\ \text{m}$, $y = \dfrac{600-300}{2}=150\ \text{m}$. Maximum area: $A = 100(150) = 15{,}000\ \text{m}^2$.

---

## 7. Common Optimization Problem Categories

| Category | Typical objective | Typical constraint |
|----------|-------------------|---------------------|
| Area/Volume maximization | Maximize $A$ or $V$ | Fixed perimeter/surface/material |
| Material/cost minimization | Minimize $S$ or cost function | Fixed volume/capacity |
| Distance minimization | Minimize $D$ (or $D^2$) | Point lies on a curve |
| Revenue/profit maximization | Maximize $R(x)=x\cdot p(x)$ or Profit $=R-C$ | Price-demand relationship |
| Time minimization | Minimize $T = \text{distance}/\text{speed}$ | Path through different media (e.g., Snell's law problems) |

---

## 8. A Note on Verifying Extrema in Applied Problems

In applied problems, you almost always have physical/contextual reasons to expect exactly one critical number corresponds to the answer. Nonetheless, **always verify** using one of:

- **Second Derivative Test** (fastest when $f''$ is easy to compute and nonzero)
- **First Derivative Test** (sign chart around the critical number)
- **Closed Interval Method** (if the domain is naturally closed/bounded — compare against endpoint behavior, keeping in mind endpoints are often *degenerate* cases, e.g., zero volume, which makes physical sense as a minimum, not the maximum you want)

Never simply assume the critical number is the answer without justification — this is one of the most common ways students lose points on optimization problems, even when their setup is entirely correct.

---

## 9. CS Connection — Optimization Is Everywhere in Computing

This lecture is the single-variable prototype for an enormous swath of computer science:

- **Machine learning training** is exactly this process, generalized: minimize a loss function (the "cost" analog) subject to model constraints, by finding where the gradient (multivariable derivative) is zero.
- **Resource allocation and scheduling algorithms** frequently reduce to constrained optimization — e.g., minimizing total wait time subject to a fixed number of servers.
- **Compiler optimization** literally minimizes a cost function (execution time, memory usage) over the space of valid program transformations.
- **Computational geometry** (closest-pair problems, convex hull minimal enclosing shapes) directly generalizes the "minimum distance to a curve" pattern from Example 3.

The exact five-step algorithm you use by hand here — define objective, apply constraint, differentiate, find critical points, verify — is mechanically what optimization libraries (`scipy.optimize`, gradient descent in PyTorch) automate at scale.

---

## Lecture 3 Exercises

1. A farmer has $800$ m of fencing and wants to enclose a rectangular field, then divide it into two equal pens with a fence parallel to one side. Maximize the total enclosed area.

2. Find the dimensions of the rectangle of maximum area that can be inscribed in a semicircle of radius $R$, with one side along the diameter.

3. A cylindrical can (open top) must have volume $1000\ \text{cm}^3$. Find the dimensions minimizing the material used (note: open top means no top surface).

4. Find the point on the line $y = 2x + 3$ closest to the origin. Verify using the fact that the minimum-distance line from a point to a line is perpendicular to the line.

5. A company's profit (in dollars) from selling $x$ units is $P(x) = -0.001x^3 + 3x^2 - 500x - 2000$ for $0 \leq x \leq 2500$. Find the production level that maximizes profit, and state the maximum profit.

6. **(Snell's Law derivation)** A lifeguard at point $A$ on the beach must reach a swimmer at point $B$ in the water as quickly as possible. The lifeguard runs at speed $v_1$ on sand and swims at speed $v_2 < v_1$ in water. Set up the time function as a function of the entry point into the water, differentiate, and show that the optimal path satisfies:
$$\frac{\sin\theta_1}{v_1} = \frac{\sin\theta_2}{v_2}$$
where $\theta_1, \theta_2$ are the angles the sand-path and water-path make with the normal to the shoreline. *(This is exactly Snell's Law of refraction from optics — light "chooses" the path of least time.)*

7. **(Challenge)** A cone-shaped paper cup is to hold a fixed volume $V$. Find the ratio of height to radius that minimizes the amount of paper used (lateral surface area of a cone: $S = \pi r\sqrt{r^2+h^2}$).

---


### Answers

Every solution needs four things: a **diagram**, a **constraint** used to eliminate one variable,
the **domain**, and a **justification** that the critical point is the required extremum.

**1.** Let $x$ be the side perpendicular to the dividing fence and $y$ the other. Fencing:
$3x+2y=800$, so $y=\dfrac{800-3x}{2}$. Area
$$A(x)=x\cdot\frac{800-3x}{2}=400x-\tfrac32x^2, \qquad 0<x<\tfrac{800}{3}$$
$A'=400-3x=0 \Rightarrow x=\tfrac{400}{3}$, $y=200$, and $A''=-3<0$ confirms a maximum.
$$\boxed{A_{\max}=\tfrac{400}{3}\times200=\tfrac{80000}{3}\approx26{,}667\ \text{m}^2}$$

**2.** With the rectangle's corner at $(x,y)$ on $x^2+y^2=R^2$, area $A=2xy=2x\sqrt{R^2-x^2}$.
Maximising $A^2=4x^2(R^2-x^2)$ is easier: its derivative $8x(R^2-2x^2)=0$ gives
$x=\tfrac{R}{\sqrt2}$, hence $y=\tfrac{R}{\sqrt2}$.
$$\boxed{\text{width }R\sqrt2,\ \text{height }\tfrac{R}{\sqrt2},\ A_{\max}=R^2}$$
**Maximising $A^2$ instead of $A$ is legitimate** because $t\mapsto t^2$ is increasing on $t\geq0$ —
a standard device that removes the square root before differentiating.

**3.** Open-top cylinder, $V=\pi r^2h=1000$. Material $S=\pi r^2+2\pi rh$; substituting
$h=\dfrac{1000}{\pi r^2}$:
$$S(r)=\pi r^2+\frac{2000}{r}, \qquad S'=2\pi r-\frac{2000}{r^2}=0 \Rightarrow r^3=\frac{1000}{\pi}$$
$$\boxed{r=\left(\tfrac{1000}{\pi}\right)^{1/3}\approx6.83\ \text{cm}, \quad h=\frac{1000}{\pi r^2}\approx6.83\ \text{cm}}$$
So $h=r$ — the optimal open can is exactly as tall as it is wide. ($S''=2\pi+\tfrac{4000}{r^3}>0$
confirms a minimum.) For a **closed** can the answer is $h=2r$ instead; the difference is the
missing lid.

**4.** Minimise $D^2=x^2+(2x+3)^2=5x^2+12x+9$. Then $\tfrac{d}{dx}D^2=10x+12=0 \Rightarrow
x=-\tfrac65$, $y=2(-\tfrac65)+3=\tfrac35$.
$$\boxed{\left(-\tfrac65,\ \tfrac35\right), \qquad D=\tfrac{3}{\sqrt5}}$$
**Check:** the segment from the origin has slope $\dfrac{3/5}{-6/5}=-\tfrac12$, and the line has
slope $2$. Their product is $-1$ ✓ — perpendicular, as the geometry requires.

**5.** $P'=-0.003x^2+6x-500=0 \Rightarrow 0.003x^2-6x+500=0$, so
$$x=\frac{6\pm\sqrt{36-6}}{0.006}=\frac{6\pm\sqrt{30}}{0.006}$$
The discriminant is $36-4(0.003)(500)=30$, so **both** roots lie inside $[0,2500]$:
$$x=\frac{6\pm\sqrt{30}}{0.006} \quad\Longrightarrow\quad x\approx87.13 \ \text{ and } \ x\approx1912.87$$

Classify with $P''=-0.006x+6$:

| $x$ | $P''$ | Type | $P(x)$ |
|---|---|---|---|
| $0$ (endpoint) | — | — | $-2{,}000$ |
| $87.13$ | $+5.48$ | local **min** | $-23{,}452$ |
| $1912.87$ | $-5.48$ | local **max** | $\mathbf{3{,}019{,}452}$ |
| $2500$ (endpoint) | — | — | $1{,}873{,}000$ |

$$\boxed{x\approx1913\ \text{units},\qquad P_{\max}\approx\$3{,}019{,}452}$$

*(Confirmed by evaluating $P$ on a 5000-point grid across $[0,2500]$.)*

**The lesson is the candidate list, not the location.** A cubic profit function has **two**
critical points, and finding only the smaller one — then reporting it — gives a *local minimum* as
the answer. Note also that the interior maximum beats the right endpoint by over a million dollars,
so stopping at "profit is increasing, take $x=2500$" is equally wrong. Enumerate every critical
point **and** both endpoints, then compare.

**6.** With the shoreline as the $x$-axis, $A=(0,a)$ on sand and $B=(d,-b)$ in water, entry at
$(x,0)$:
$$T(x)=\frac{\sqrt{a^2+x^2}}{v_1}+\frac{\sqrt{b^2+(d-x)^2}}{v_2}$$
$$T'(x)=\frac{x}{v_1\sqrt{a^2+x^2}}-\frac{d-x}{v_2\sqrt{b^2+(d-x)^2}}=0$$
The two fractions are exactly $\dfrac{\sin\theta_1}{v_1}$ and $\dfrac{\sin\theta_2}{v_2}$, where
each $\theta$ is measured from the normal. Hence
$$\boxed{\frac{\sin\theta_1}{v_1}=\frac{\sin\theta_2}{v_2}}$$
which is **Snell's Law**. $T''>0$ throughout, so this is the minimum. Light obeys the same
relation because it too takes the path of least time (Fermat's principle) — the optics is a
corollary of the calculus.

**7.** With $V=\tfrac13\pi r^2h$ fixed, $h=\dfrac{3V}{\pi r^2}$. Minimise
$S^2=\pi^2r^2(r^2+h^2)=\pi^2r^4+\dfrac{9V^2}{r^2}$:
$$\frac{d}{dr}S^2=4\pi^2r^3-\frac{18V^2}{r^3}=0 \Rightarrow r^6=\frac{9V^2}{2\pi^2}$$
Substituting back gives $h^2=2r^2$, hence
$$\boxed{\frac hr=\sqrt2}$$
A pleasingly clean result: the paper-optimal cone has height $\sqrt2$ times its radius, independent
of the volume — as it must be, since the ratio is dimensionless.

*Reading for Week 6: Stewart §5.1 (Areas and Distances — Riemann Sums), beginning of integral calculus.*
*Problem Set 7 due next Wednesday — see assignment file.*
