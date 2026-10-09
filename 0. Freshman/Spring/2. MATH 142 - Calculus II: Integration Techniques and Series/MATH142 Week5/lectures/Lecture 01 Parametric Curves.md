# MATH 142 · Calculus II
## Week 5 · Lecture 1 (Monday)
### Parametric Curves — A Curve Is a Path, Not a Graph

*“What I have given in the second book on the nature and properties of curved lines, and the method of examining them, is, it seems to me, as far beyond the treatment in the ordinary geometry, as the rhetoric of Cicero is beyond the a, b, c of children.”* — René Descartes, letter to Marin Mersenne (1637), on *La Géométrie*

**Date:** Monday 22 February 2027 · 11:00–11:50 · Week 5

**Coursework:** 📊 **Quiz 5** today 11:00–11:15 · 🔬 **Lab 4** Wed 24 Feb 15:00–16:50 · 📝 **PS 4** due Fri 26 Feb 17:00 · 📝 **PS 5** released Fri 26 Feb 12:00, due Fri 5 Mar 17:00 · 📘 **Midterm 1** Wed 3 Mar 18:00–19:15

---

**Reading:** Stewart §10.1 | Apostol Ch. 2 §2.14
**Quiz 05** — this Monday, **covers Week 4** (volumes, arc length, surface area)
**Midterm 1 is Wednesday 3 March, 18:00–19:15** (Week 6) — covering Weeks 0–4. See the revision guide in `resources/`.

---

## 1. The Limitation We Have Been Living With

$y=f(x)$ assigns **one** $y$ to each $x$. Three things it therefore cannot describe:

- **A circle.** $x^2+y^2=1$ requires two half-functions, and at $x=\pm1$ the tangent is vertical, where $\frac{dy}{dx}$ does not exist.
- **A curve that crosses itself.** A figure-eight has two $y$-values at the crossing point — indeed two *tangent directions*.
- **Motion.** "Where is the particle?" is a question about time, and $y=f(x)$ has no time in it. It records the *track* but not the *journey*.

**A parametric description fixes all three at once.**

$$x = x(t),\qquad y = y(t),\qquad t\in[\alpha,\beta]$$

Think of $t$ as **time** and $(x(t),y(t))$ as the position of a moving point. The curve is the **path traced out** — and, crucially, it comes with a *direction of travel* and a *speed*.

---

## 2. Examples

### Example 1 — a line segment

$$x = 1+2t,\qquad y = 3-t,\qquad t\in[0,1]$$

At $t=0$ we are at $(1,3)$; at $t=1$ at $(3,2)$.

**Eliminate the parameter:** $t = \frac{x-1}{2}$, so $y = 3-\frac{x-1}{2}$, i.e. $x+2y = 7$ — a straight line, restricted to the segment between those endpoints.

### Example 2 — the circle

$$x=\cos t,\qquad y=\sin t,\qquad t\in[0,2\pi]$$

Then $x^2+y^2=\cos^2t+\sin^2t=1$. **The Pythagorean identity is what eliminates the parameter**, and this pattern recurs constantly.

**Traversed anticlockwise, starting at $(1,0)$.**

### Example 3 — the ellipse

$$x=a\cos t,\qquad y=b\sin t$$

Then $\left(\frac xa\right)^2+\left(\frac yb\right)^2 = 1$ — the standard ellipse. **The same identity, rescaled.**

### Example 4 — the cycloid

The path of a point on the rim of a wheel of radius $a$ rolling along the ground:

$$x = a(t-\sin t),\qquad y = a(1-\cos t)$$

Here $t$ is the angle the wheel has turned through. One arch corresponds to $t\in[0,2\pi]$.

**This curve cannot reasonably be written as $y=f(x)$** — you would have to invert $x = a(t-\sin t)$ for $t$, which has no closed form. Parametrically it is two lines of elementary functions.

**At $t=0$ and $t=2\pi$ the point touches the ground and the curve has a cusp** — a sharp corner where the tangent is vertical. Tomorrow we will see the calculus report this correctly.

### Example 5 — a curve with a cusp

$$x=t^2,\qquad y=t^3$$

Eliminating: $t = y^{1/3}$, so $x = y^{2/3}$, i.e. $y^2 = x^3$. **This has a cusp at the origin.** The parametrisation passes through smoothly in $t$ while the *curve* has a corner — a distinction $y=f(x)$ cannot make.

### Example 6 — a curve that crosses itself

$$x=t^2-1,\qquad y=t^3-t = t(t^2-1)$$

At $t=-1$ and $t=+1$ **both** give the point $(0,0)$. The curve passes through the origin **twice, in different directions** — an $\alpha$-shaped loop. No function $y=f(x)$ can do this.

---

## 3. Orientation and Speed: The Same Curve, Different Journeys

**A parametrisation carries more information than the curve does.** These all trace the unit circle:

| Parametrisation | $t$ range | What is different |
|---|---|---|
| $(\cos t,\sin t)$ | $[0,2\pi]$ | anticlockwise, once, unit speed |
| $(\cos 2t,\sin 2t)$ | $[0,\pi]$ | anticlockwise, once, **double speed** |
| $(\cos t,-\sin t)$ | $[0,2\pi]$ | **clockwise**, once |
| $(\cos t,\sin t)$ | $[0,4\pi]$ | anticlockwise, **twice** |
| $(\sin t,\cos t)$ | $[0,2\pi]$ | clockwise, starting at $(0,1)$ |

**Same set of points. Five different journeys.**

> **This matters computationally.** Tomorrow's arc length formula integrates *speed over time* — so
> the fourth row would give $4\pi$, not $2\pi$. **It is not wrong; it is the length of a path that
> goes round twice.** Always ask what range of $t$ traces the piece you actually want, exactly once.

---

## 4. Eliminating the Parameter

To identify a parametric curve, remove $t$.

**Method 1 — solve and substitute.** Works when one equation is easily invertible (Examples 1, 5).

**Method 2 — use an identity.** Works for trigonometric parametrisations (Examples 2, 3): isolate $\cos t$ and $\sin t$, then use $\cos^2+\sin^2=1$.

### Example 7

$$x = 2+3\cos t,\qquad y = -1+3\sin t$$

Then $\frac{x-2}{3}=\cos t$ and $\frac{y+1}{3}=\sin t$, so

$$(x-2)^2+(y+1)^2 = 9$$

— a circle of radius 3 centred at $(2,-1)$.

### Two warnings

**(a) Eliminating loses information.** Example 1 gave the line $x+2y=7$, but the parametrisation only traced the *segment* from $(1,3)$ to $(3,2)$. **The Cartesian equation usually describes more of the curve than the parametrisation traces.** Always state the range.

**(b) It is often impossible.** The cycloid cannot be de-parametrised in closed form, and **this is normal.** Do not treat elimination as a required step — it is a tool for *recognising* a curve, not for working with one.

---

## 5. Parametrising a Given Curve

The reverse problem: given a curve, find a parametrisation.

| Curve | A parametrisation |
|---|---|
| $y=f(x)$ on $[a,b]$ | $x=t$, $y=f(t)$, $t\in[a,b]$ |
| circle, centre $(h,k)$, radius $r$ | $x=h+r\cos t$, $y=k+r\sin t$ |
| ellipse $\frac{(x-h)^2}{a^2}+\frac{(y-k)^2}{b^2}=1$ | $x=h+a\cos t$, $y=k+b\sin t$ |
| segment from $P$ to $Q$ | $(x,y) = P + t(Q-P)$, $t\in[0,1]$ |

**Every function graph is trivially a parametric curve** — take $x=t$. So parametric form is strictly more general, which is the point.

**Parametrisations are not unique**, and choosing a convenient one is a real skill. For a circle you would never use $x=t$, $y=\sqrt{1-t^2}$.

---

## 6. Where This Is Used

**Computer graphics** describes every curve and surface parametrically — Bézier curves, the basis of every font you have ever read, are cubic parametric curves. Rendering asks "where is the curve at parameter $t$", never "what is $y$ when $x=3$".

**Physics and robotics** use $t$ as literal time: position, velocity and acceleration are $(x(t),y(t))$ and its derivatives.

**The cycloid itself** is the solution of two famous problems — the **brachistochrone** (the curve of fastest descent under gravity) and the **tautochrone** (the curve on which a bead's time to the bottom is independent of where it starts). Both were solved in the 1690s and both answers are the cycloid.

---

## 7. What To Take From This Lecture

1. **A parametric curve is a path traced by a moving point**, with a direction and a speed.
2. **It can do what $y=f(x)$ cannot:** self-intersections, vertical tangents, cusps, closed curves.
3. **Eliminate the parameter to *recognise* a curve** — with an identity, when trigonometric.
4. **Elimination loses the range and the orientation**, and is often impossible.
5. **The same curve has infinitely many parametrisations.** Which one you use changes the arithmetic, and can change the answer if the range is wrong.

---

*Next: Tuesday — Calculus with Parametric Curves*
