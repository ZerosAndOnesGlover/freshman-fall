# MATH 141 · Problem Set 7 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Revised 2026-09-21 to match the 100-point set; items are numbered as in the new set.*

---


## Marking Scheme

Point values are printed per problem on the problem set. Within each problem, split the marks:

- **Method (≈60%).** Correct technique named and set up: the right rule or theorem, hypotheses checked where the theorem requires it, and the symbolic work shown before any numerical evaluation.
- **Execution (≈40%).** Correct algebra and simplification, correct final form, and any domain restrictions or constants of integration stated.

A bare answer with no working earns at most the execution marks — and in proof problems ("show that", "prove"), no marks at all, since the reasoning *is* the deliverable.

**Carry-through.** Penalise a given error once. If the student proceeds correctly from their own wrong intermediate value, award the downstream marks in full.

**Equivalent forms.** Accept any algebraically equivalent answer — factored or expanded, and trigonometric identities applied or not — unless the problem explicitly demands a particular form.

### Common errors in this problem set

**1. Applying L'Hôpital to a form that is not indeterminate.** Only 0/0 and ∞/∞ qualify directly. Using it on 2/0 or 0/5 produces nonsense; other forms (0·∞, ∞−∞, 1^∞) must be algebraically converted first.

**2. Differentiating the quotient instead of numerator and denominator separately.** L'Hôpital replaces f/g with f′/g′ — it is **not** the quotient rule. This confusion is common and produces a completely different expression.

**3. Not verifying the form still qualifies before reapplying.** Each successive application requires rechecking that the new limit is still indeterminate.

**4. Optimisation without a domain or endpoint check.** A physical optimisation has a feasible domain; the optimum may sit at an endpoint. A single critical point is not automatically the answer, and the student should justify max vs min.

---

## Part A — L'Hôpital Review

**A1.** $0/0$. Apply: $\lim_{x\to0}\dfrac{1-\cos x}{3x^2}$ — still $0/0$. Apply again: $\lim_{x\to0}\dfrac{\sin x}{6x}$ — still $0/0$. Apply again: $\lim_{x\to0}\dfrac{\cos x}{6}=\dfrac16$

**A2.** $y=(1+2x)^{1/x}$; $\ln y=\dfrac{\ln(1+2x)}{x}$, form $0/0$.

L'Hôpital: $\dfrac{2/(1+2x)}{1}\to2$ as $x\to0^+$.

$\lim y=e^2$

---

## Part B — Curve Sketching (Summary Solutions)

**B1.** $f(x)=\dfrac{2x^2}{x^2-1}$

Domain: $x\neq\pm1$. Even function. $y$-int: $(0,0)$. VA at $x=\pm1$. HA: $y=2$.

$f'(x)=\dfrac{4x(x^2-1)-2x^2(2x)}{(x^2-1)^2}=\dfrac{-4x}{(x^2-1)^2}$

Critical: $x=0$. Increasing $(-\infty,-1)\cup(-1,0)$; decreasing $(0,1)\cup(1,\infty)$. Local max at $x=0$, $f(0)=0$.

$f''(x)=\dfrac{-4(x^2-1)^2+4x\cdot2(x^2-1)(2x)}{(x^2-1)^4}=\dfrac{-4(x^2-1)+16x^2}{(x^2-1)^3}=\dfrac{12x^2+4}{(x^2-1)^3}$

Numerator always positive; sign follows $(x^2-1)^3$. Concave up $|x|>1$; concave down $|x|<1$. No inflection points (concavity changes only at excluded points).

**B2.** $f(x)=\dfrac{x^2+1}{x}=x+\dfrac1x$

Domain: $x\neq0$. Odd function. No $y$-intercept. No real $x$-intercepts ($x^2+1=0$ has none). VA at $x=0$. Slant asymptote: $y=x$.

$f'(x)=1-\dfrac1{x^2}$. Critical: $x=\pm1$.

Sign: $+$ for $|x|>1$, $-$ for $0<|x|<1$.

Local max at $x=-1$ ($f=-2$); local min at $x=1$ ($f=2$).

$f''(x)=\dfrac{2}{x^3}$. Concave up $x>0$; concave down $x<0$. No inflection point (not defined at $x=0$).

**B3.** $f(x)=x^2e^{-x}$

Domain: $\mathbb{R}$. No symmetry. $y$-int and $x$-int both at $(0,0)$. HA: $y=0$ as $x\to\infty$; $f\to\infty$ as $x\to-\infty$.

$f'(x)=2xe^{-x}-x^2e^{-x}=xe^{-x}(2-x)$. Critical: $x=0,2$.

Sign: $-$ for $x<0$, $+$ for $0<x<2$, $-$ for $x>2$.

Local min at $x=0$ ($f=0$); local max at $x=2$ ($f=4e^{-2}\approx0.541$).

$f''(x)=e^{-x}(x^2-4x+2)$. Zero at $x=2\pm\sqrt2$. Concave up outside $(2-\sqrt2,2+\sqrt2)$, concave down inside. Inflection points at $x=2\pm\sqrt2$.

---

## Part C — Applied Optimization

**C1.** Square base side $x$, height $h$. $V=x^2h=32000$. Material (open top): $S=x^2+4xh$.

$h=32000/x^2$. $S(x)=x^2+128000/x$.

$S'(x)=2x-128000/x^2=0\implies x^3=64000\implies x=40$ cm.

$h=32000/1600=20$ cm.

$S''(x)=2+256000/x^3>0$ always: confirmed minimum.

**Dimensions: base $40\times40$ cm, height $20$ cm.**

**C2.** Point on ellipse: $(x,y)$ with $x=4\cos\theta$, $y=3\sin\theta$, or directly: rectangle has vertices $(\pm x,\pm y)$ with $y=3\sqrt{1-x^2/16}$.

Area $A=2x\cdot2y=4xy=12x\sqrt{1-x^2/16}$, $x\in(0,4)$.

Maximize $A^2=144x^2(1-x^2/16)=144x^2-9x^4$.

$\dfrac{d}{dx}[A^2]=288x-36x^3=36x(8-x^2)=0\implies x=2\sqrt2$

$y=3\sqrt{1-8/16}=3\sqrt{1/2}=\dfrac{3}{\sqrt2}$

**Dimensions: width $2x=4\sqrt2$, height $2y=3\sqrt2$. Max area $=4xy=4(2\sqrt2)(3/\sqrt2)=24$.**

**C3.** Revenue $R(x)=xp(x)=200x-0.5x^2$. Cost $C(x)=3000+40x$.

Profit $P(x)=R(x)-C(x)=200x-0.5x^2-3000-40x=-0.5x^2+160x-3000$

$P'(x)=-x+160=0\implies x=160$

$P''(x)=-1<0$: confirmed maximum.

$P(160)=-0.5(25600)+160(160)-3000=-12800+25600-3000=9800$

**Production level: 160 units. Maximum profit: \$9800.**

**C4.** Norman window. Let $r$ = radius of the semicircle = half the rectangle's width, and
$h$ = height of the rectangle.

The perimeter is the bottom $(2r)$ + the two vertical sides $(h$ each$)$ + the semicircular arc
$(\pi r)$. The horizontal diameter where the semicircle meets the rectangle is **internal** and is
not part of the perimeter:

$2r+2h+\pi r=10\implies h=\dfrac{10-2r-\pi r}{2}=5-r-\dfrac{\pi r}{2}$

Area $A=2rh+\dfrac12\pi r^2=2r\left(5-r-\dfrac{\pi r}{2}\right)+\dfrac{\pi r^2}{2}=10r-2r^2-\pi r^2+\dfrac{\pi r^2}{2}=10r-2r^2-\dfrac{\pi r^2}{2}$

$A'(r)=10-4r-\pi r=0\implies r=\dfrac{10}{4+\pi}\approx1.40$ m

$h=5-r-\dfrac{\pi r}{2}\approx5-1.40-2.20\approx1.40$ m

$A''(r)=-4-\pi<0$: confirmed maximum.

**Dimensions: $r\approx1.40$ m, $h\approx1.40$ m (rectangle width $2r\approx2.80$ m).**

---

## Part D — Conceptual

**D1.** (a) $f_1'=4x^3$, $f_1''=12x^2$; $f_2'=-4x^3$, $f_2''=-12x^2$; $f_3'=3x^2$, $f_3''=6x$ — all zero at $0$.

(b) $f_1'$ goes $-$ to $+$: **local min**. $f_2'$ goes $+$ to $-$: **local max**. $f_3'=3x^2\ge0$ on both sides, no
sign change: **neither**.

(c) $f''(c)=0$ is consistent with a min, a max, or neither, so the Second Derivative Test is
**inconclusive** there — not evidence that there is no extremum. Fall back to the First Derivative Test.

**D2.** Finding $f'(x)=0$ only identifies **candidates** for extrema (critical numbers) — per Fermat's Theorem, ANY local extremum must occur at a critical number, but not every critical number is necessarily an extremum (recall $f(x)=x^3$ at $x=0$ from Week 6). Verification requires either: the First Derivative Test (checking sign change of $f'$ around the critical number), the Second Derivative Test (checking sign of $f''$ at the critical number), or the Closed Interval Method (comparing against all critical numbers AND endpoints if working on a closed bounded domain).
