# MATH 141 · Problem Set 7 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

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

## Part A — L'Hôpital's Rule: Basic Forms

**A1(a).** $0/0$. $\lim_{x\to0}\dfrac{3\cos3x}{1}=3$. *(Matches Week 1: $\lim \sin(3x)/x = 3$.)*

**A1(b).** $0/0$. $\lim_{x\to1}\dfrac{1/x}{1}=1$

**A1(c).** $\infty/\infty$. $\lim_{x\to\infty}\dfrac{10x+3}{4x}$ — still $\infty/\infty$, apply again: $\dfrac{10}{4}=\dfrac52$. *(Matches Week 1 algebraic method.)*

**A1(d).** $0/0$. $\lim_{x\to0}\dfrac{e^x+e^{-x}}{\cos x}=\dfrac{1+1}{1}=2$

**A1(e).** $0/0$. $\lim_{x\to\pi/2}\dfrac{-\sin x}{1}=-\sin(\pi/2)=-1$

**A1(f).** $\infty/\infty$. $\lim_{x\to\infty}\dfrac{(1/\ln x)(1/x)}{1/x}=\lim_{x\to\infty}\dfrac{1}{\ln x}=0$

---

**A2(a).** $0/0$. Apply: $\lim_{x\to0}\dfrac{1-\cos x}{3x^2}$ — still $0/0$. Apply again: $\lim_{x\to0}\dfrac{\sin x}{6x}$ — still $0/0$. Apply again: $\lim_{x\to0}\dfrac{\cos x}{6}=\dfrac16$

**A2(b).** $0/0$ (check: $e^0-1-0-0=0$ ✓). Apply: $\lim_{x\to0}\dfrac{e^x-1-x}{3x^2}$ — still $0/0$. Apply: $\lim_{x\to0}\dfrac{e^x-1}{6x}$ — still $0/0$. Apply: $\lim_{x\to0}\dfrac{e^x}{6}=\dfrac16$

**A2(c).** $\infty/\infty$. Apply: $\dfrac{3x^2}{2e^{2x}}$ — still $\infty/\infty$. Apply: $\dfrac{6x}{4e^{2x}}$ — still $\infty/\infty$. Apply: $\dfrac{6}{8e^{2x}}\to0$

---

## Part B — Other Indeterminate Forms

**B1(a).** $\sqrt{x}\ln x=\dfrac{\ln x}{x^{-1/2}}$, form $-\infty/\infty$. L'Hôpital: $\dfrac{1/x}{-\frac12x^{-3/2}}=\dfrac{-2x^{-1/2}}{1}=-2\sqrt{x}\to0$

**B1(b).** $xe^{-x}=\dfrac{x}{e^x}$, form $\infty/\infty$. L'Hôpital: $\dfrac{1}{e^x}\to0$

**B1(c).** $\dfrac1x-\csc x=\dfrac1x-\dfrac1{\sin x}=\dfrac{\sin x-x}{x\sin x}$, form $0/0$.

L'Hôpital: $\dfrac{\cos x-1}{\sin x+x\cos x}$, still $0/0$. Apply again: $\dfrac{-\sin x}{\cos x+\cos x-x\sin x}=\dfrac{-\sin x}{2\cos x-x\sin x}\to\dfrac{0}{2}=0$

**B1(d).** $\dfrac{1}{\ln x}-\dfrac{1}{x-1}=\dfrac{(x-1)-\ln x}{(x-1)\ln x}$, form $0/0$ as $x\to1^+$.

L'Hôpital: $\dfrac{1-1/x}{\ln x+(x-1)/x}$, still $0/0$ at $x=1$. Apply again (or simplify first): numerator $\to\dfrac{x-1}{x}$, so ratio becomes $\dfrac{(x-1)/x}{\ln x+(x-1)/x}$.

Multiply num/denom by $x$: $\dfrac{x-1}{x\ln x+x-1}$, still $0/0$. Apply L'Hôpital again: $\dfrac{1}{\ln x+1+1}=\dfrac{1}{\ln x+2}\to\dfrac12$ as $x\to1$.

---

**B2(a).** $y=(1+2x)^{1/x}$; $\ln y=\dfrac{\ln(1+2x)}{x}$, form $0/0$.

L'Hôpital: $\dfrac{2/(1+2x)}{1}\to2$ as $x\to0^+$.

$\lim y=e^2$

**B2(b).** $y=x^{1/\ln x}$; $\ln y=\dfrac{\ln x}{\ln x}=1$ (constant!). So $\lim y=e^1=e$.

**B2(c).** $y=(\sin x)^x$; $\ln y=x\ln(\sin x)$, form $0\cdot(-\infty)$ as $x\to0^+$.

Rewrite: $\dfrac{\ln(\sin x)}{1/x}$, form $-\infty/\infty$.

L'Hôpital: $\dfrac{\cos x/\sin x}{-1/x^2}=\dfrac{-x^2\cos x}{\sin x}=\dfrac{-x\cos x\cdot x}{\sin x}\to0\cdot1\cdot1=0$ (using $x/\sin x\to1$).

$\lim y=e^0=1$

**B2(d).** $y=\left(1-\dfrac3x\right)^{2x}$; $\ln y=2x\ln\left(1-\dfrac3x\right)$

Rewrite: $\dfrac{2\ln(1-3/x)}{1/x}$, form $0/0$.

L'Hôpital (treat $1/x=t\to0$): $\ln y=\dfrac{2\ln(1-3t)}{t}\to2\cdot\dfrac{-3}{1}=-6$ (using derivative of $\ln(1-3t)$ at $t=0$ is $-3/(1-0)=-3$).

$\lim y=e^{-6}$

---

**B3.** $\dfrac{x+\cos x}{x}$: as $x\to\infty$, this is $\infty/\infty$ technically, but applying L'Hôpital gives $\dfrac{1-\sin x}{1}$, which **oscillates** (does not converge) as $x\to\infty$ since $\sin x$ oscillates. L'Hôpital's Rule requires the limit of $f'/g'$ to EXIST — since it doesn't here, the rule is inapplicable (or rather, it gives no information; it does NOT mean the original limit fails to exist).

**Correct approach:** $\dfrac{x+\cos x}{x}=1+\dfrac{\cos x}{x}$. Since $|\cos x|\leq1$, $\dfrac{\cos x}{x}\to0$ by Squeeze Theorem. So the limit is $1+0=1$.

**Lesson:** L'Hôpital's Rule is a sufficient but not necessary tool — when $f'/g'$ doesn't converge, you must fall back to other techniques (here, the Squeeze Theorem from Week 1).

---

## Part C — Curve Sketching (Summary Solutions)

**C1.** $f(x)=\dfrac{2x^2}{x^2-1}$

Domain: $x\neq\pm1$. Even function. $y$-int: $(0,0)$. VA at $x=\pm1$. HA: $y=2$.

$f'(x)=\dfrac{4x(x^2-1)-2x^2(2x)}{(x^2-1)^2}=\dfrac{-4x}{(x^2-1)^2}$

Critical: $x=0$. Increasing $(-\infty,-1)\cup(-1,0)$; decreasing $(0,1)\cup(1,\infty)$. Local max at $x=0$, $f(0)=0$.

$f''(x)=\dfrac{-4(x^2-1)^2+4x\cdot2(x^2-1)(2x)}{(x^2-1)^4}=\dfrac{-4(x^2-1)+16x^2}{(x^2-1)^3}=\dfrac{12x^2+4}{(x^2-1)^3}$

Numerator always positive; sign follows $(x^2-1)^3$. Concave up $|x|>1$; concave down $|x|<1$. No inflection points (concavity changes only at excluded points).

**C2.** $f(x)=x^4-2x^2+1=(x^2-1)^2$

Domain: $\mathbb{R}$. Even. $y$-int: $(0,1)$. $x$-int: $x=\pm1$ (double roots). No asymptotes (polynomial).

$f'(x)=4x^3-4x=4x(x-1)(x+1)$. Critical: $x=0,\pm1$.

Sign: $-$ on $(-\infty,-1)$, $+$ on $(-1,0)$, $-$ on $(0,1)$, $+$ on $(1,\infty)$.

Local min at $x=\pm1$ ($f=0$); local max at $x=0$ ($f=1$).

$f''(x)=12x^2-4$. Zero at $x=\pm1/\sqrt3$. Concave up $|x|>1/\sqrt3$, concave down $|x|<1/\sqrt3$. Inflection points at $x=\pm1/\sqrt3$, $f(\pm1/\sqrt3)=1/9-2/3+1=4/9$.

**C3.** $f(x)=\dfrac{x^2+1}{x}=x+\dfrac1x$

Domain: $x\neq0$. Odd function. No $y$-intercept. No real $x$-intercepts ($x^2+1=0$ has none). VA at $x=0$. Slant asymptote: $y=x$.

$f'(x)=1-\dfrac1{x^2}$. Critical: $x=\pm1$.

Sign: $+$ for $|x|>1$, $-$ for $0<|x|<1$.

Local max at $x=-1$ ($f=-2$); local min at $x=1$ ($f=2$).

$f''(x)=\dfrac{2}{x^3}$. Concave up $x>0$; concave down $x<0$. No inflection point (not defined at $x=0$).

**C4.** $f(x)=x^2e^{-x}$

Domain: $\mathbb{R}$. No symmetry. $y$-int and $x$-int both at $(0,0)$. HA: $y=0$ as $x\to\infty$; $f\to\infty$ as $x\to-\infty$.

$f'(x)=2xe^{-x}-x^2e^{-x}=xe^{-x}(2-x)$. Critical: $x=0,2$.

Sign: $-$ for $x<0$, $+$ for $0<x<2$, $-$ for $x>2$.

Local min at $x=0$ ($f=0$); local max at $x=2$ ($f=4e^{-2}\approx0.541$).

$f''(x)=e^{-x}(x^2-4x+2)$. Zero at $x=2\pm\sqrt2$. Concave up outside $(2-\sqrt2,2+\sqrt2)$, concave down inside. Inflection points at $x=2\pm\sqrt2$.

**C5.** $f(x)=\ln(x^2+1)$

Domain: $\mathbb{R}$. Even. $y$-int and only intercept: $(0,0)$. No vertical asymptote (never zero inside log). As $x\to\pm\infty$, $f\to\infty$ (no horizontal asymptote, but grows like $2\ln|x|$, slower than linear).

$f'(x)=\dfrac{2x}{x^2+1}$. Critical: $x=0$. Increasing $x>0$, decreasing $x<0$. Local (and absolute) min at $x=0$, $f=0$.

$f''(x)=\dfrac{2(x^2+1)-2x(2x)}{(x^2+1)^2}=\dfrac{2-2x^2}{(x^2+1)^2}$. Zero at $x=\pm1$. Concave up $|x|<1$, concave down $|x|>1$. Inflection points at $x=\pm1$, $f(\pm1)=\ln2$.

---

## Part D — Applied Optimization

**D1.** Square base side $x$, height $h$. $V=x^2h=32000$. Material (open top): $S=x^2+4xh$.

$h=32000/x^2$. $S(x)=x^2+128000/x$.

$S'(x)=2x-128000/x^2=0\implies x^3=64000\implies x=40$ cm.

$h=32000/1600=20$ cm.

$S''(x)=2+256000/x^3>0$ always: confirmed minimum.

**Dimensions: base $40\times40$ cm, height $20$ cm.**

**D2.** Point on ellipse: $(x,y)$ with $x=4\cos\theta$, $y=3\sin\theta$, or directly: rectangle has vertices $(\pm x,\pm y)$ with $y=3\sqrt{1-x^2/16}$.

Area $A=2x\cdot2y=4xy=12x\sqrt{1-x^2/16}$, $x\in(0,4)$.

Maximize $A^2=144x^2(1-x^2/16)=144x^2-9x^4$.

$\dfrac{d}{dx}[A^2]=288x-36x^3=36x(8-x^2)=0\implies x=2\sqrt2$

$y=3\sqrt{1-8/16}=3\sqrt{1/2}=\dfrac{3}{\sqrt2}$

**Dimensions: width $2x=4\sqrt2$, height $2y=3\sqrt2$. Max area $=4xy=4(2\sqrt2)(3/\sqrt2)=24$.**

**D3.** Let $x$= wire for square, $20-x$ for triangle. Square side $=x/4$, area $=x^2/16$. Triangle side $=(20-x)/3$, area $=\dfrac{\sqrt3}{4}\left(\dfrac{20-x}{3}\right)^2$.

$A(x)=\dfrac{x^2}{16}+\dfrac{\sqrt3(20-x)^2}{36}$, $x\in[0,20]$.

$A'(x)=\dfrac{x}{8}-\dfrac{\sqrt3(20-x)}{18}=0$

Solve: $\dfrac{9x}{72}=\dfrac{4\sqrt3(20-x)}{72}\implies9x=4\sqrt3(20-x)\implies9x+4\sqrt3x=80\sqrt3\implies x=\dfrac{80\sqrt3}{9+4\sqrt3}\approx9.34$ m.

$A''(x)=1/8+\sqrt3/18>0$: this critical point is a **minimum**.

**(b) Minimum area:** cut at $x\approx9.34$ m (use Closed Interval Method for the actual value, evaluate $A$ there).

**(a) Maximum area:** since the critical point is a minimum, by Closed Interval Method check endpoints: $A(0)$ (all wire → triangle) vs $A(20)$ (all wire → square). Compare $\dfrac{\sqrt3(20)^2}{36}\approx19.245$ vs $\dfrac{400}{16}=25$. **Maximum: use all wire for the square, $x=20$, giving area 25 m².**

**D4.** Cylinder inscribed in sphere radius $R$: if cylinder height $=2h$, radius $r$, then $r^2+h^2=R^2$ (half-height and radius relate via sphere equation).

$V=\pi r^2(2h)=2\pi r^2h$. Using $r^2=R^2-h^2$: $V(h)=2\pi(R^2-h^2)h=2\pi(R^2h-h^3)$, $h\in(0,R)$.

$V'(h)=2\pi(R^2-3h^2)=0\implies h=R/\sqrt3$

$V''(h)=2\pi(-6h)<0$ for $h>0$: confirmed maximum.

$r^2=R^2-R^2/3=2R^2/3\implies r=R\sqrt{2/3}$

**Dimensions: height $2h=2R/\sqrt3$, radius $r=R\sqrt{2/3}$.**

**D5.** Revenue $R(x)=xp(x)=200x-0.5x^2$. Cost $C(x)=3000+40x$.

Profit $P(x)=R(x)-C(x)=200x-0.5x^2-3000-40x=-0.5x^2+160x-3000$

$P'(x)=-x+160=0\implies x=160$

$P''(x)=-1<0$: confirmed maximum.

$P(160)=-0.5(25600)+160(160)-3000=-12800+25600-3000=9800$

**Production level: 160 units. Maximum profit: \$9800.**

**D6.** Norman window. Let $r$ = radius of the semicircle = half the rectangle's width, and
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

## Part E — Conceptual

**E1.** Conditions: (1) $f,g$ differentiable near $a$ (except possibly at $a$), (2) $g'\neq0$ near $a$, (3) the ORIGINAL limit must be $0/0$ or $\infty/\infty$ form. Example of misuse: $\lim_{x\to0}\dfrac{x+1}{x+2}$ is NOT indeterminate ($=1/2$ directly); blindly applying L'Hôpital gives $\lim \dfrac{1}{1}=1$ — the WRONG answer.

**E2.** L'Hôpital's Rule is proved using Cauchy's Generalized MVT, which states $\dfrac{f(b)-f(a)}{g(b)-g(a)}=\dfrac{f'(c)}{g'(c)}$ for some $c$ between $a,b$. In the $0/0$ case (with $f(a)=g(a)=0$), this reduces to $\dfrac{f(x)}{g(x)}=\dfrac{f'(c)}{g'(c)}$ for $c$ between $a$ and $x$. As $x\to a$, $c\to a$ too (squeezed), giving the L'Hôpital conclusion. Cauchy's MVT itself is proved via an auxiliary function and Rolle's Theorem — exactly the same technique used to prove the ordinary MVT in Week 6.

**E3.** Finding $f'(x)=0$ only identifies **candidates** for extrema (critical numbers) — per Fermat's Theorem, ANY local extremum must occur at a critical number, but not every critical number is necessarily an extremum (recall $f(x)=x^3$ at $x=0$ from Week 6). Verification requires either: the First Derivative Test (checking sign change of $f'$ around the critical number), the Second Derivative Test (checking sign of $f''$ at the critical number), or the Closed Interval Method (comparing against all critical numbers AND endpoints if working on a closed bounded domain).
