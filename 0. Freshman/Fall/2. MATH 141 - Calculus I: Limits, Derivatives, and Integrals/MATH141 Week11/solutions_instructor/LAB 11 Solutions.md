# MATH 141 · Lab 11 Solutions (Instructor)
## Areas, Volumes, and Numerical Checks

All values verified by the Lab 09 midpoint rule at $n=100\,000$. *(Revised 2026-09-26: 2B was removed from
the lab, and the checks use the midpoint rule, since Simpson's rule is never taught.)*

---

## Part 1: The Crossing Trap (5 pts)

**1A** *(1 pt)* — sketch showing the curves meeting at $x=\pi/4$, with $\cos$ above on $[0,\pi/4]$
and $\sin$ above on $[\pi/4,\pi/2]$.

**1B** *(1 pt)* — $\displaystyle\int_0^{\pi/2}(\sin x-\cos x)\,dx = \mathbf{0}$.

Verified: $-0.0000000000$.

**1C** *(3 pts)* — correct area:

$$\int_0^{\pi/4}(\cos x-\sin x)dx+\int_{\pi/4}^{\pi/2}(\sin x-\cos x)dx = 2(\sqrt2-1)\approx\mathbf{0.8284}$$

Verified: $0.8284271247$.

**The required explanation:** the unsplit integral computes the **signed net** difference, not the
area. The region where $\cos>\sin$ contributes negatively and the region where $\sin>\cos$
contributes positively; here they are exactly equal, so they cancel to zero.

*This is the same distinction as displacement versus distance (Weeks 4 and 9): $\int(f-g)$ is signed,
$\int\lvert f-g\rvert$ is area. Students who connect it to that earlier material should be
credited.*

**Marking:** 2 of the 3 for identifying that the first number is a signed net quantity; 1 for the
correct area.

---

## Part 2: Set Up, Evaluate, Verify (7 pts)

**2A** *(3 pts)* $\displaystyle\int_0^1(x^2-x^3)dx=\tfrac13-\tfrac14=\tfrac{1}{12}\approx0.0833$.
Verified $0.0833333333$.

*Watch for $x^3-x^2$, from assuming the higher power is larger. It is not on $(0,1)$.*

**2C** *(4 pts)* $\sqrt x$ is the outer radius on $(0,1)$:

$$V=\pi\int_0^1\big[x-x^2\big]dx=\frac{\pi}{6}\approx\mathbf{0.5236}$$

Verified $0.52359878$.

**The deliberate error:** $\pi\int_0^1(\sqrt x-x)^2dx=\dfrac{\pi}{30}\approx\mathbf{0.1047}$ —
verified — which is **exactly one fifth** of the correct value.

Students should record both and note the factor. The point is that squaring the difference computes
the area of a circle whose radius is the *gap* between the two radii — a geometrically meaningless
quantity — rather than the difference of the two disc areas.

*1 of the 4 marks is for producing the wrong value and identifying the factor.*

---

## Part 3: Two Methods, One Answer (5 pts)

**3A — shells** *(2 pts)*

$$V=2\pi\int_0^2x\cdot x^2dx=2\pi\left[\frac{x^4}{4}\right]_0^2=8\pi$$

**3B — washers in $y$** *(2 pts)*

Outer radius $2$ (the line $x=2$), inner radius $x=\sqrt y$, for $0\le y\le4$:

$$V=\pi\int_0^4\big[4-y\big]dy=\pi\left[4y-\frac{y^2}{2}\right]_0^4=8\pi$$

**Both verified as $25.13274123$ — identical to 8 decimal places.**

**3C** *(1 pt)* — expected answer: the two set-ups are **genuinely different**, using different
slicing directions, different variables of integration, and different geometry. Agreement is
therefore strong evidence both are right; a disagreement would localise an error immediately. It is
the most reliable self-check available for a volume problem, and it costs one extra integral.

*Reject "they should agree because they're the same solid" as circular — the question asks why the
check has value, which is about **independence** of the two computations.*

---

## Part 4: Build Your Own (3 pts)

Base: the region between $y=x$ and $y=x^2$ on $[0,1]$, so the side of each triangle is

$$s(x)=x-x^2$$

An equilateral triangle of side $s$ has area $\dfrac{\sqrt3}{4}s^2$, so

$$V=\frac{\sqrt3}{4}\int_0^1(x-x^2)^2dx=\frac{\sqrt3}{4}\int_0^1\big(x^2-2x^3+x^4\big)dx$$

$$=\frac{\sqrt3}{4}\left(\frac13-\frac12+\frac15\right)=\frac{\sqrt3}{4}\cdot\frac{1}{30}=\mathbf{\frac{\sqrt3}{120}}\approx0.01443$$

Verified: $0.0144337567$, matching $\sqrt3/120$ exactly.

**Marking:** 1 for the correct side length $x-x^2$ (not $x^2-x$, and not a half-width); 1 for the
area formula $\tfrac{\sqrt3}{4}s^2$; 1 for evaluating and verifying.

*The inner integral is $\tfrac{1}{30}$ — a neat check in itself, and worth pointing out.*

---

## Common Submission Problems

| Symptom | Cause | Action |
|---|---|---|
| Part 1 gives $0$ and it is reported as the area | Missed the split entirely | −3; this is the lab's central point |
| 1C says "the areas cancel" only | No mention of *signed* | −1 |
| 2C omits the deliberate error | Skipped the instruction | −1 |
| Part 3 done by one method twice | Not two independent set-ups | −2 |
| Part 4 uses $\tfrac12 s^2$ | Confused with a right triangle | −1 |
| No sketches anywhere | The lab requires them | −2 overall |

---

*MATH 141 · Week 11 · Lab 11 Solutions · Instructor copy — do not distribute*
