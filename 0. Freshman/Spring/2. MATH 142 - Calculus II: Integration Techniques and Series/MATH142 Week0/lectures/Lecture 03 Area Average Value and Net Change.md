# MATH 142 · Calculus II
## Week 0 · Lecture 3 (Wednesday)
### Area, Average Value, and Net Change

---

**Reading:** Stewart §6.1, §6.5, §5.4 | Apostol Ch. 2 §2.1–2.6

---

## 1. The Pattern Behind Every Application

Every application of the integral in this course — areas this week, volumes and arc length in Week 4, work, mass, probability — is the same four-step move:

> **Slice. Approximate. Sum. Take the limit.**

1. **Slice** the quantity into $n$ pieces indexed by a variable.
2. **Approximate** each piece by something you can compute — usually a rectangle, later a disc or a straight segment. The approximation must have error that vanishes faster than the piece shrinks.
3. **Sum** the approximations. This is a Riemann sum.
4. **Take the limit** as the slices thin. The sum becomes an integral.

**Learn the pattern, not the formulas.** There are perhaps twenty formulas in Chapter 6 of Stewart and one idea. Students who memorise the formulas cannot handle a problem stated slightly differently; students who hold the pattern can rederive any of them in a minute.

The whole of Week 4 is this pattern applied three more times.

---

## 2. Area Between Curves

If $f(x)\ge g(x)$ on $[a,b]$, the area between them is

$$\boxed{A = \int_a^b \big[f(x)-g(x)\big]\,dx}$$

**Deriving it via the pattern:** slice vertically at $x$, width $\Delta x$. The strip is approximately a rectangle of height $f(x)-g(x)$ and width $\Delta x$, so area $\approx [f(x)-g(x)]\Delta x$. Sum and take the limit.

### The two things that go wrong

**(a) Getting top and bottom backwards.** The integrand is *(upper) − (lower)*, always. If your answer is negative, you have them swapped — area is never negative.

**(b) The curves crossing inside the interval.** If $f-g$ changes sign, a single integral gives the *net* signed area, not the geometric area. You must find the crossings and split:

$$A = \int_a^c |f-g| = \int_a^{c_1}(f-g) + \int_{c_1}^{b}(g-f)$$

**Always sketch, or at least solve $f=g$ to find the crossings.** This is the same additivity property from Lecture 1, doing real work.

### Example 1

Area between $y=x$ and $y=x^2$ from $x=0$ to $x=1$.

On $(0,1)$ we have $x > x^2$, so $y=x$ is on top:

$$A = \int_0^1 (x - x^2)\,dx = \left[\frac{x^2}{2}-\frac{x^3}{3}\right]_0^1 = \frac12-\frac13 = \boxed{\frac16}$$

*Verified symbolically: $1/6$.*

### Example 2 — find the limits yourself

Area enclosed between $y=x^2$ and $y=8-x^2$.

No interval is given: the curves themselves bound the region. Set them equal:

$$x^2 = 8-x^2 \implies 2x^2 = 8 \implies x = \pm 2$$

On $(-2,2)$, $8-x^2$ is on top (check at $x=0$: $8 > 0$ ✓):

$$A = \int_{-2}^{2}\big[(8-x^2)-x^2\big]dx = \int_{-2}^2 (8-2x^2)\,dx$$

The integrand is even, so this is $2\int_0^2(8-2x^2)dx = 2\left[8x-\frac{2x^3}{3}\right]_0^2 = 2\left(16-\frac{16}{3}\right) = 2\cdot\frac{32}{3} = \boxed{\frac{64}{3}}$

*Verified symbolically: $64/3$.*

### Slicing horizontally

Sometimes $x$ as a function of $y$ is simpler. The region between $x=p(y)$ (right) and $x=q(y)$ (left) for $y\in[c,d]$ has area

$$A = \int_c^d \big[p(y)-q(y)\big]\,dy$$

**Choose the direction that avoids splitting.** A region bounded by $y^2=x$ and $y=x-2$ needs two integrals in $x$ and one in $y$ — the horizontal slice is strictly less work.

---

## 3. Average Value of a Function

The average of finitely many numbers is their sum over their count. A function on $[a,b]$ has infinitely many values, so we take the limit of averages of samples:

$$\frac{f(x_1)+\cdots+f(x_n)}{n} = \frac1n\sum f(x_i) = \frac{1}{b-a}\sum f(x_i)\,\Delta x \quad\text{using } \Delta x = \frac{b-a}{n}$$

Letting $n\to\infty$, the sum becomes an integral:

$$\boxed{f_{\text{avg}} = \frac{1}{b-a}\int_a^b f(x)\,dx}$$

**Geometrically:** $f_{\text{avg}}$ is the height of the rectangle over $[a,b]$ with the same area as the region under $f$.

### Example 3

Average value of $f(x)=x^2$ on $[0,3]$:

$$f_{\text{avg}} = \frac{1}{3}\int_0^3 x^2\,dx = \frac13\cdot\left[\frac{x^3}{3}\right]_0^3 = \frac13\cdot 9 = \boxed{3}$$

*Verified symbolically: $3$.*

Sanity check: $f$ ranges from $0$ to $9$ on this interval, and $3$ lies between them. It is below the midpoint $4.5$ because $x^2$ spends more of the interval small — correct for a convex increasing function.

### Example 4

Average value of $\sin x$ on $[0,\pi]$:

$$\frac{1}{\pi}\int_0^\pi \sin x\,dx = \frac{2}{\pi} \approx 0.6366$$

*Verified symbolically: $2/\pi$.*

This number is worth remembering — **it is the average rectified value of a sine wave**, and it appears throughout signal processing and electrical engineering.

### The Mean Value Theorem for Integrals

If $f$ is continuous on $[a,b]$, there exists $c\in[a,b]$ with

$$f(c) = f_{\text{avg}} = \frac{1}{b-a}\int_a^b f(x)\,dx$$

**A continuous function actually attains its average.** This follows from the Intermediate Value Theorem: $f_{\text{avg}}$ lies between $\min f$ and $\max f$, so $f$ takes that value somewhere.

For Example 3: solve $c^2 = 3$, giving $c = \pm\sqrt3$; only $c=\sqrt3\approx 1.732$ lies in $[0,3]$. *Verified: the solutions are $\pm\sqrt3$, and exactly one is in range.*

**Continuity is essential.** A step function that is $0$ on $[0,1)$ and $1$ on $[1,2]$ has average $\tfrac12$ and never takes the value $\tfrac12$.

---

## 4. Net Change, and Why $\int v \neq$ Distance

FTC Part 2, read as a sentence about rates:

$$\int_a^b F'(x)\,dx = F(b)-F(a)$$

> **The integral of a rate of change is the total change.**

This is the most useful sentence in applied calculus. If $v(t)$ is velocity, $\int_{t_1}^{t_2} v\,dt$ is the **change in position** — the displacement. If $c(t)$ is a marginal cost, its integral is total cost. If $f(t)$ is a flow rate, its integral is the volume delivered.

### The distinction that gets examined

- **Displacement** $= \displaystyle\int_{t_1}^{t_2} v(t)\,dt$ — signed; backwards motion cancels forwards motion.
- **Distance travelled** $= \displaystyle\int_{t_1}^{t_2} |v(t)|\,dt$ — unsigned; every metre counts.

### Example 5

A particle has velocity $v(t)=t^2-4$ (m/s) for $0\le t\le 3$.

**Displacement:**

$$\int_0^3 (t^2-4)\,dt = \left[\frac{t^3}{3}-4t\right]_0^3 = (9-12) - 0 = \boxed{-3\text{ m}}$$

The particle ends up 3 m *behind* where it started.

**Distance:** $v(t)=0$ at $t=2$, and $v<0$ on $[0,2)$, $v>0$ on $(2,3]$. Split there:

$$\int_0^3 |v|\,dt = \int_0^2 (4-t^2)\,dt + \int_2^3 (t^2-4)\,dt = \frac{16}{3} + \frac{7}{3} = \boxed{\frac{23}{3}\text{ m}} \approx 7.667\text{ m}$$

*Verified: each piece computed exactly, total $23/3$; confirmed by high-precision quadrature to 20 digits.*

**A note on method.** A computer algebra system asked directly for $\int_0^3 |t^2-4|\,dt$ returned the expression **unevaluated** — it would not resolve the absolute value on its own. Splitting at the sign change by hand gave the exact answer immediately.

> This is the same lesson as yesterday's $\sec x$: **the machine is a check on your work, not a substitute for it.** It is very good at the steps you already know how to set up, and it fails in ways that look like an answer. In this course you will use one regularly — and you will always be able to say why its output is right.

---

## 5. What To Take From This Lecture

1. **Slice, approximate, sum, take the limit.** Every application is this. Week 4 is this three more times.
2. **Area is (upper) − (lower)**, and you must find where they cross.
3. **Average value is the integral divided by the width**, and a continuous function attains it.
4. **The integral of a rate is the total change.** Signed for displacement, absolute for distance.
5. **Split at sign changes yourself.** Neither you nor the machine should integrate across one.

---

## Looking Ahead

Every integral in this lecture was elementary — you could find each antiderivative from the Lecture 2 catalogue. That will stop being true on Monday.

**Week 1 begins with $\int x e^x\,dx$**, which has an elementary answer that substitution cannot reach, and the technique that reaches it — integration by parts — is the product rule run backwards, exactly as substitution was the chain rule run backwards.

---

*Next: Week 1, Monday — Integration by Parts*
