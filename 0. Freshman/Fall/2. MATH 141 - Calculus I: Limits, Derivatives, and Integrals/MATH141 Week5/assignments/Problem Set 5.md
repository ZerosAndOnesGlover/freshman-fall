# MATH 141 · Calculus I
## Problem Set 5
### Topic: Implicit Differentiation, Logarithms, Inverse Trig, Related Rates
**Released:** Wednesday, Week 5 | **Due:** Wednesday, Week 4 (start of class)

---

## Part A — Implicit Differentiation (4 pts each)

**A1.** Find $dy/dx$ by implicit differentiation. Do not solve for $y$ first.

- (a) $x^4 + y^4 = 16$
- (b) $\sqrt{x} + \sqrt{y} = 4$
- (c) $ye^x + xe^y = 1$
- (d) $\ln(x+y) = x^2 + y$
- (e) $\cos(x-y) = x\sin y$

**A2.** Find $y'$ and $y''$ for $x^2 - xy + y^2 = 3$.

**A3.** Find all points on the curve $x^2 + 2xy - y^2 + x = 5$ where the tangent line is horizontal.

**A4.** The curve $2(x^2+y^2)^2 = 25(x^2-y^2)$ is called a **lemniscate of Bernoulli**.

- (a) Find $dy/dx$ by implicit differentiation.
- (b) Find the equations of the tangent lines at the points $(\pm3, 1)$. Verify both points lie on the curve.

---

## Part B — Logarithmic Derivatives (3 pts each)

**B1.** Differentiate:

- (a) $y = \ln(x^4 + 3x^2 - 1)$
- (b) $y = \ln\!\left(\dfrac{x^2+1}{x^2-1}\right)$ — simplify using log laws first
- (c) $y = \ln|\tan x + \sec x|$
- (d) $y = x^2\ln(3x)$
- (e) $y = \ln(\ln x)$
- (f) $y = \log_5(x^3+1)$

**B2.** Use logarithmic differentiation to find $y'$:

- (a) $y = x^{\tan x}$
- (b) $y = (\ln x)^x$
- (c) $y = (x^2+1)^{3x}$
- (d) $y = \dfrac{x^{3/2}(2x-1)^4}{\sqrt{x^2+1}}$ — use logs to simplify the product/quotient

---

## Part C — Inverse Trigonometric Derivatives (3 pts each)

**C1.** Differentiate:

- (a) $y = \arctan(4x^3)$
- (b) $y = \arcsin\!\left(\dfrac{x}{3}\right)$
- (c) $y = x\arctan x - \dfrac{1}{2}\ln(1+x^2)$
- (d) $y = \arctan\!\left(\dfrac{1}{x}\right)$
- (e) $y = \arcsin(\cos x)$

**C2.** Show that $\dfrac{d}{dx}[\arctan x] + \dfrac{d}{dx}[\text{arccot}\, x] = 0$, then explain geometrically why $\arctan x + \text{arccot}\, x = \dfrac{\pi}{2}$ for all $x$.

**C3.** Find $f'(x)$ for $f(x) = \arcsin\!\left(\dfrac{2x}{1+x^2}\right)$.

Simplify your answer completely. *(Hint: try $x = \tan\theta$ substitution, or differentiate directly and simplify with trig identities.)*

---

## Part D — Related Rates (6 pts each)

For each problem: draw a diagram, label variables, identify given and wanted rates, write the geometric equation, differentiate with respect to time, substitute, and solve.

**D1.** A spherical snowball melts so that its volume decreases at $1\ \text{cm}^3/\text{min}$. How fast is the radius decreasing when $r = 5\ \text{cm}$? How fast is the surface area decreasing at that moment?

**D2.** A ladder $13\ \text{m}$ long rests against a vertical wall. The bottom slides away from the wall at $2\ \text{m/s}$.

- (a) How fast is the top descending when the bottom is $5\ \text{m}$ from the wall?
- (b) How fast is the angle between the ladder and the ground decreasing at the same moment?

**D3.** A water trough is $10\ \text{m}$ long. Its cross-section is an isoceles triangle with width $2\ \text{m}$ at the top and depth $1\ \text{m}$. Water is poured in at $0.5\ \text{m}^3/\text{min}$. How fast is the water level rising when the depth is $0.3\ \text{m}$?

*(Hint: cross-sectional area of water $= \frac{1}{2}\cdot\text{width}\cdot\text{depth}$. Find width as a function of depth by similar triangles.)*

**D4.** Two people start walking from the same point. Person A walks east at $4\ \text{km/h}$, Person B walks north at $3\ \text{km/h}$. How fast is the distance between them increasing after $30\ \text{minutes}$?

**D5.** A spotlight on the ground shines on a wall $12\ \text{m}$ away. A person $2\ \text{m}$ tall walks away from the spotlight toward the wall at $1.5\ \text{m/s}$. When the person is $4\ \text{m}$ from the wall:

- (a) How fast is the length of their shadow on the wall changing?
- (b) Is the shadow getting longer or shorter? Explain physically why this makes sense.

**D6.** *(Challenging)* A boat is pulled toward a dock by a rope through a ring on the dock at height $3\ \text{m}$ above water level. The rope is pulled in at $1\ \text{m/s}$. How fast is the boat approaching the dock when $5\ \text{m}$ of rope remains between the ring and the boat?

---

## Part E — Mixed Differentiation (4 pts each)

Differentiate. These require selecting and combining the right techniques.

**E1.** $y = \arctan\!\left(\dfrac{\sqrt{x}-1}{\sqrt{x}+1}\right)$

**E2.** $y = (\arcsin x)^2$

**E3.** $y = e^{\arctan x}\sqrt{1+x^2}$

**E4.** $y = \ln\!\left(\dfrac{1+\sin x}{1-\sin x}\right)$

**E5.** $y = x^{x^2}$ — use logarithmic differentiation

---

## Part F — Conceptual (5 pts each)

**F1.** Explain in your own words why you cannot substitute numerical values for variables before differentiating in a related rates problem. Construct a specific counterexample showing what goes wrong if you do.

**F2.** For the curve defined implicitly by $F(x, y) = 0$, implicit differentiation gives:
$$\frac{dy}{dx} = -\frac{F_x}{F_y}$$

where $F_x = \partial F/\partial x$ (treat $y$ constant) and $F_y = \partial F/\partial y$ (treat $x$ constant).

Verify this formula for:
- (a) $F(x,y) = x^2 + y^2 - 25$ (the circle from Lecture 1)
- (b) $F(x,y) = x^3 + y^3 - 6xy$ (the Folium of Descartes)

**F3.** A student differentiates $y = x^x$ as follows: "Since $y = x^x$, by the power rule $y' = x\cdot x^{x-1} = x^x$." Find the error. What is the correct derivative, and why does the power rule fail here?

---

## Grading Summary

| Part | Points | Focus |
|------|--------|-------|
| A (6 × 4) | 24 | Implicit differentiation |
| B (10 × 3) | 30 | Logarithmic techniques |
| C (5 × 3) | 15 | Inverse trig derivatives |
| D (6 × 6) | 36 | Related rates |
| E (5 × 4) | 20 | Mixed techniques |
| F (3 × 5) | 15 | Conceptual understanding |
| **Total** | **140** | |
