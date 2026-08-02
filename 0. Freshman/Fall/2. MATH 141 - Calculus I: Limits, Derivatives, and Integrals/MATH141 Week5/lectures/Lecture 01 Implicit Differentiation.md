# MATH 141 — Calculus I
## Week 5 · Lecture 1 (Monday)
### Implicit Differentiation

---

**Reading:** Stewart §3.5 | Spivak Ch. 10 §10.4
**Quiz 05** — this Monday, covers Week 2 (derivative definition and rules)

---

## 1. The Problem with Explicit Functions

Every function we have differentiated so far has been **explicit** — $y$ is isolated on one side:
$$y = f(x) = x^3 - 2x + 1$$

But many important curves are defined **implicitly** — $x$ and $y$ appear together, and $y$ cannot be (easily) isolated:
$$x^2 + y^2 = 25 \qquad x^3 + y^3 = 6xy \qquad \sin(xy) = y^2 - x$$

The circle $x^2 + y^2 = 25$ is not a function (fails vertical line test), but near any point except $(\pm5, 0)$ it looks locally like a function. We want $dy/dx$ at any point on the curve — without solving for $y$.

---

## 2. The Key Idea: $y$ Is a Function of $x$

When we differentiate implicitly, we treat $y$ as an unknown differentiable function of $x$ — call it $y(x)$ — even though we don't know its formula. Then every time we differentiate a term involving $y$, we apply the **chain rule**:

$$\frac{d}{dx}[y^n] = ny^{n-1}\cdot\frac{dy}{dx} \qquad \frac{d}{dx}[\sin y] = \cos y\cdot\frac{dy}{dx} \qquad \frac{d}{dx}[e^y] = e^y\cdot\frac{dy}{dx}$$

The $\frac{dy}{dx}$ factor appears because $y$ is the inner function and $x$ is the variable we differentiate with respect to.

---

## 3. The Method — Four Steps

1. Differentiate both sides of the equation with respect to $x$
2. Every time you differentiate an expression in $y$, multiply by $\frac{dy}{dx}$ (chain rule)
3. Collect all terms with $\frac{dy}{dx}$ on one side
4. Factor out and solve for $\frac{dy}{dx}$

---

## 4. Worked Examples

### Example 1 — The Circle

$$x^2 + y^2 = 25$$

Differentiate both sides with respect to $x$:
$$2x + 2y\frac{dy}{dx} = 0$$

Solve:
$$\frac{dy}{dx} = -\frac{x}{y}$$

**Check:** At the point $(3, 4)$: $\frac{dy}{dx} = -\frac{3}{4}$.

Geometrically: the radius to $(3,4)$ has slope $\frac{4}{3}$. The tangent is perpendicular to the radius, so its slope is $-\frac{3}{4}$. ✓

**Equation of tangent at $(3,4)$:** $y - 4 = -\frac{3}{4}(x-3)$, i.e., $3x + 4y = 25$.

---

### Example 2 — Folium of Descartes

$$x^3 + y^3 = 6xy$$

Differentiate:
$$3x^2 + 3y^2\frac{dy}{dx} = 6y + 6x\frac{dy}{dx}$$

Collect $dy/dx$ terms:
$$3y^2\frac{dy}{dx} - 6x\frac{dy}{dx} = 6y - 3x^2$$

Factor:
$$\frac{dy}{dx}(3y^2 - 6x) = 6y - 3x^2$$

$$\frac{dy}{dx} = \frac{6y - 3x^2}{3y^2 - 6x} = \frac{2y - x^2}{y^2 - 2x}$$

---

### Example 3 — Mixed Expression

$$\sin(xy) = y^2 - x$$

Left side: chain rule, then product rule on $xy$:
$$\cos(xy)\cdot\left(y + x\frac{dy}{dx}\right) = 2y\frac{dy}{dx} - 1$$

Expand:
$$y\cos(xy) + x\cos(xy)\frac{dy}{dx} = 2y\frac{dy}{dx} - 1$$

Collect:
$$x\cos(xy)\frac{dy}{dx} - 2y\frac{dy}{dx} = -1 - y\cos(xy)$$

$$\frac{dy}{dx} = \frac{-1 - y\cos(xy)}{x\cos(xy) - 2y}$$

---

### Example 4 — Second Derivative Implicitly

Find $y''$ given $x^2 + y^2 = r^2$ (circle of radius $r$).

From Example 1: $y' = -x/y$.

Differentiate again using the quotient rule (treating $y$ as a function of $x$):

$$y'' = -\frac{y \cdot 1 - x \cdot y'}{y^2} = -\frac{y - x(-x/y)}{y^2} = -\frac{y + x^2/y}{y^2} = -\frac{y^2 + x^2}{y^3}$$

Since $x^2 + y^2 = r^2$:
$$y'' = -\frac{r^2}{y^3}$$

The second derivative tells us about curvature — this is always negative for the upper semicircle ($y > 0$), confirming it is concave down.

---

## 5. Why This Works — The Chain Rule Foundation

Implicit differentiation is not a new technique. It is the chain rule applied systematically. When we write $x^2 + y^2 = 25$ and differentiate both sides, we are using:

$$\frac{d}{dx}[x^2 + y(x)^2] = \frac{d}{dx}[25]$$

The left side, by the chain rule: $2x + 2y(x)\cdot y'(x)$.

The right side: $0$.

The implicit assumption — that such a function $y(x)$ exists near the point in question — is guaranteed by the **Implicit Function Theorem** (a deep result in multivariable calculus, MATH 241/242). For MATH 141, we assume it holds whenever $dy/dx$ does not blow up.

---

## 6. Derivatives of Inverse Trig Functions via Implicit Differentiation

Implicit differentiation is the tool for differentiating inverse functions. As a preview:

**Deriving $\frac{d}{dx}[\arcsin x]$:**

Let $y = \arcsin x$, so $\sin y = x$ (and $y \in [-\pi/2, \pi/2]$).

Differentiate implicitly:
$$\cos y \cdot \frac{dy}{dx} = 1 \implies \frac{dy}{dx} = \frac{1}{\cos y}$$

From $\sin y = x$: $\cos y = \sqrt{1 - \sin^2 y} = \sqrt{1-x^2}$ (positive since $y \in [-\pi/2, \pi/2]$).

$$\frac{d}{dx}[\arcsin x] = \frac{1}{\sqrt{1-x^2}}$$

We derive all inverse trig derivatives on Wednesday using this method.

---

## 7. Horizontal and Vertical Tangents

Implicit differentiation gives $dy/dx$ as a **quotient**, and that quotient tells you where the
curve's tangent is flat or vertical:

$$\frac{dy}{dx} = \frac{N(x,y)}{D(x,y)} \qquad
\begin{cases}
N = 0,\ D \neq 0 & \Rightarrow \textbf{horizontal tangent}\\
D = 0,\ N \neq 0 & \Rightarrow \textbf{vertical tangent}\\
N = D = 0 & \Rightarrow \textbf{indeterminate — inspect directly}
\end{cases}$$

**Example — the circle $x^2+y^2=25$, where $y' = -x/y$.**

Horizontal tangents need $x = 0$: the points $(0, \pm5)$, the top and bottom of the circle.
Vertical tangents need $y = 0$: the points $(\pm5, 0)$ — exactly the two points excluded in §1,
where the circle fails to look like a function of $x$.

**Example — the folium $x^3+y^3=6xy$, where $y' = \dfrac{2y-x^2}{y^2-2x}$.**

Horizontal tangent: $2y = x^2$ together with the curve equation. Substituting $y = x^2/2$ gives
$x^3 + x^6/8 = 3x^3$, so $x^3(x^3 - 16) = 0$, i.e. $x = 0$ or $x = 16^{1/3} = 2\sqrt[3]{2}$. The
second gives the point $\left(2\sqrt[3]{2},\ 2\sqrt[3]{4}\right)$.

By the symmetry $x \leftrightarrow y$ of the folium, the vertical tangent is the mirror image:
$\left(2\sqrt[3]{4},\ 2\sqrt[3]{2}\right)$.

**The third case is the interesting one.** At the origin the folium gives $N = D = 0$, and the
curve actually crosses itself there — it has *two* tangent lines, $y = 0$ and $x = 0$. A single
number $dy/dx$ cannot describe a self-intersection, and the $0/0$ is the algebra telling you so.
Whenever numerator and denominator vanish together, stop and examine the curve.

---

## 8. Orthogonal Trajectories

Two families of curves are **orthogonal trajectories** if every member of one meets every member
of the other at right angles — that is, the slopes are negative reciprocals at each crossing.
This is the geometry behind electric field lines crossing equipotentials, and streamlines crossing
lines of constant velocity potential.

**Claim.** The family of circles $x^2+y^2=c$ and the family of lines $y = kx$ are orthogonal.

*Proof.* For the circles, implicit differentiation gives $2x + 2yy' = 0$, so $y' = -x/y$.
For the lines, $y = kx$ with $k = y/x$ at any point on the line, so $y' = k = y/x$.

At any intersection point $(x,y)$ with $x,y \neq 0$:

$$\left(-\frac{x}{y}\right)\cdot\left(\frac{y}{x}\right) = -1 \qquad \blacksquare$$

The product of the slopes is $-1$ at *every* crossing, so the families are orthogonal. Note the
argument never solves for the intersection points — implicit differentiation gives the slope as a
function of position, which is exactly what a statement about "every crossing" needs.

---

## 9. Common Errors

**1. Dropping the $dy/dx$ factor.** Writing $\frac{d}{dx}[y^3] = 3y^2$ instead of
$3y^2\frac{dy}{dx}$. This is *the* defining error of the topic — if it appears, the student has
not done implicit differentiation at all, and no partial credit is available for the method.

**2. Forgetting the product rule on mixed terms.** $\frac{d}{dx}[xy] = y + x\frac{dy}{dx}$, not
$\frac{dy}{dx}$ and not $x\frac{dy}{dx}$. Any term containing *both* variables needs the product
rule before the chain rule.

**3. Solving for $y$ first when you shouldn't.** For $x^2+y^2=25$ you *can* write
$y = \pm\sqrt{25-x^2}$ and differentiate — but you must then track two branches and handle the
sign. Implicit differentiation handles both branches at once, and for the folium there is no
solvable form at all.

**4. Substituting the point too early.** Substitute $(a,b)$ only *after* differentiating.
Substituting first turns $y$ into a constant, so $dy/dx$ becomes 0 and the answer is meaningless.

**5. Reporting $dy/dx$ in terms of $x$ alone.** The answer to an implicit problem is normally a
function of **both** $x$ and $y$, and that is correct — it must be, because a single $x$ can
correspond to several points on the curve with different slopes.

---

## 7. CS Connection — Implicit Functions in Computing

**Level sets and implicit surfaces:** Computer graphics and scientific computing frequently define surfaces implicitly — $f(x,y,z) = 0$. Rendering and intersection algorithms require the gradient (multivariable derivative), computed using implicit differentiation principles.

**Newton's method** (MATH 341): Solves $f(x) = 0$ iteratively using $x_{n+1} = x_n - f(x_n)/f'(x_n)$. When $f$ is defined implicitly, $f'$ is found by implicit differentiation.

**Automatic differentiation:** Modern AD systems treat every intermediate computation as an implicit relationship and apply the chain rule forward or backward — exactly the logic of implicit differentiation on computation graphs.

---

## Lecture 1 Exercises

1. Find $dy/dx$ by implicit differentiation:
   - (a) $x^3 + y^3 = 1$
   - (b) $x^2y + xy^3 = 6$ at the point $(1,2)$
   - (c) $e^{x+y} = x^2 + y$
   - (d) $\tan(x+y) = x$

2. Find the equations of both the tangent and normal lines to $x^2 + 4y^2 = 8$ at the point $(2, 1)$.

3. Use implicit differentiation to find $y''$ for $xy + y^2 = 3$.

4. Show that for the curve $y^2 = x^3$ (semicubical parabola), $\frac{dy}{dx} = \frac{3x^2}{2y}$, then find **every** point on the curve where the tangent line is parallel to $y = x + 1$. (Be careful at the origin, and check both branches — the number of such points may not be what you expect.)

5. **(Thinking)** The equation $x^2 - y^2 = 1$ defines a hyperbola. Use implicit differentiation to find $dy/dx$. Then solve explicitly for $y$ (two branches) and differentiate directly. Verify the results agree.

---

### Answers

Attempt each exercise before reading. Every result below was checked numerically.

**1.**
**(a)** $3x^2+3y^2y'=0 \Rightarrow \boxed{y' = -\dfrac{x^2}{y^2}}$

**(b)** Product rule on both terms: $2xy + x^2y' + y^3 + 3xy^2y' = 0$, so
$y'(x^2+3xy^2) = -(2xy+y^3)$ and
$$y' = -\frac{2xy+y^3}{x^2+3xy^2}, \qquad y'(1,2) = -\frac{4+8}{1+12} = \boxed{-\frac{12}{13}}$$

**(c)** $e^{x+y}(1+y') = 2x + y' \Rightarrow y'\left(e^{x+y}-1\right) = 2x - e^{x+y}$, so
$\boxed{y' = \dfrac{2x-e^{x+y}}{e^{x+y}-1}}$

**(d)** $\sec^2(x+y)\,(1+y') = 1 \Rightarrow 1+y' = \cos^2(x+y)$, so
$$y' = \cos^2(x+y) - 1 = \boxed{-\sin^2(x+y)}$$
A pleasing result: the slope depends only on the combination $x+y$, and is never positive.

**2.** $2x+8yy'=0 \Rightarrow y' = -\dfrac{x}{4y}$; at $(2,1)$ the slope is $-\tfrac12$.

- **Tangent:** $y-1=-\tfrac12(x-2)$, i.e. $\boxed{x+2y=4}$
- **Normal:** perpendicular slope $+2$, giving $\boxed{y = 2x-3}$

**3.** $y + xy' + 2yy' = 0 \Rightarrow y' = -\dfrac{y}{x+2y}$. Differentiating that quotient and
substituting $y'$ back:
$$y'' = \boxed{\dfrac{2y(x+y)}{(x+2y)^3}}$$
*(Verified numerically on both branches at $x=1$ and $x=2$.)* The standard error is to leave $y'$
un-substituted in the second derivative — the answer must be in terms of $x$ and $y$ only.

**4.** $2yy' = 3x^2 \Rightarrow y' = \dfrac{3x^2}{2y}$ ✓. Setting $y'=1$ gives $3x^2=2y$;
combined with $y^2=x^3$ this yields $\tfrac94x^4 = x^3$, so $x^3(9x-4)=0$ and $x=0$ or $x=\tfrac49$.

- $x=\tfrac49 \Rightarrow y = \tfrac{3x^2}{2} = \tfrac{8}{27}$. Check: $y^2 = \tfrac{64}{729} = x^3$ ✓,
  slope $=1$ ✓. **The point is $\left(\tfrac49, \tfrac8{27}\right)$.**
- $x=0 \Rightarrow y=0$, where $y' = \tfrac{0}{0}$ is **indeterminate**. The semicubical parabola has a
  **cusp** at the origin with a *vertical* tangent, so this is not a solution.
- On the lower branch $y=-x^{3/2}$ the slope is $-\tfrac32\sqrt{x} \leq 0$ for every $x\geq0$, so it
  never equals $+1$.

**There is exactly ONE such point, not two.** The exercise is phrased to test whether you check
the origin and the second branch rather than stopping at the algebra.

**5.** Implicitly: $2x-2yy'=0 \Rightarrow y' = \dfrac{x}{y}$.

Explicitly, $y = \pm\sqrt{x^2-1}$. Upper branch: $y' = \dfrac{x}{\sqrt{x^2-1}} = \dfrac{x}{y}$ ✓.
Lower branch: $y' = \dfrac{-x}{\sqrt{x^2-1}} = \dfrac{x}{-\sqrt{x^2-1}} = \dfrac{x}{y}$ ✓.

**The single implicit formula $y'=x/y$ covers both branches**, because $y$ carries the sign. That
economy — one formula where the explicit approach needs two cases — is the practical argument for
implicit differentiation.

---

*Next: Tuesday — Derivatives of Logarithmic Functions and Logarithmic Differentiation*
