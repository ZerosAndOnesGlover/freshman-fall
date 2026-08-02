# MATH 141 — Problem Set 3 Solutions
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

**1. Product and quotient rules as products/quotients of derivatives.** (fg)′ ≠ f′g′. This is a definition-level error; award no method marks where it appears.

**2. Omitting the inner derivative in the chain rule.** d/dx[f(g(x))] = f′(g(x))·g′(x). The missing g′(x) is the single most common differentiation error in the course.

**3. Confusing the derivative at a point with the derivative function.** f′(a) is a number; f′(x) is a function. Tangent-line problems need f′ evaluated **at the point of tangency**, not at the x the student happens to be solving for.

**4. Losing the definition when asked for it.** 'From the definition' means the difference quotient limit. Differentiating by rule when the problem demands the definition earns the answer marks only.

---

## Part A — From the Definition

**A1.** $f(x) = 4x^2-3x+1$

$$\frac{f(x+h)-f(x)}{h}=\frac{4(x+h)^2-3(x+h)+1-(4x^2-3x+1)}{h}=\frac{8xh+4h^2-3h}{h}=8x+4h-3$$

$f'(x)=\lim_{h\to0}(8x+4h-3)=8x-3$

---

**A2.** $f(x)=\frac{1}{2x+3}$

$$\frac{f(x+h)-f(x)}{h}=\frac{\frac{1}{2(x+h)+3}-\frac{1}{2x+3}}{h}=\frac{(2x+3)-(2x+2h+3)}{h(2x+2h+3)(2x+3)}=\frac{-2h}{h(2x+2h+3)(2x+3)}$$

$$=\frac{-2}{(2x+2h+3)(2x+3)}\to\frac{-2}{(2x+3)^2}$$

$f'(x)=\dfrac{-2}{(2x+3)^2}$

---

**A3.** $f(x)=\sqrt{x+4}$

$$\frac{\sqrt{x+h+4}-\sqrt{x+4}}{h}\cdot\frac{\sqrt{x+h+4}+\sqrt{x+4}}{\sqrt{x+h+4}+\sqrt{x+4}}=\frac{h}{h(\sqrt{x+h+4}+\sqrt{x+4})}\to\frac{1}{2\sqrt{x+4}}$$

$f'(x)=\dfrac{1}{2\sqrt{x+4}}$

---

**A4(a).** $\displaystyle\frac{f(x+h)-f(x)}{h}=\frac{3x^2h+3xh^2+h^3}{h}=3x^2+3xh+h^2\to3x^2$

So $f'(x)=3x^2$.

**A4(b).** $f(x)=x^3$ (since $(x+h)^3-x^3=3x^2h+3xh^2+h^3$).

---

## Part B — Differentiation Rules

**B1.** $y=7x^6-4x^{3/2}+2x^{-2}-\pi$

$y'=42x^5-6x^{1/2}-4x^{-3}=42x^5-6\sqrt{x}-\dfrac{4}{x^3}$

**B2.** $y=(x^2+3)(x^3-5x+1)$

$y'=2x(x^3-5x+1)+(x^2+3)(3x^2-5)$

$=2x^4-10x^2+2x+3x^4-5x^2+9x^2-15=5x^4-6x^2+2x-15$

*(Verify: expand first: $x^5-5x^3+x^2+3x^3-15x+3=x^5-2x^3+x^2-15x+3$; differentiate: $5x^4-6x^2+2x-15$ ✓)*

**B3.** $y=\dfrac{3x^2-2x+1}{x^2+1}$

$y'=\dfrac{(6x-2)(x^2+1)-(3x^2-2x+1)(2x)}{(x^2+1)^2}=\dfrac{6x^3+6x-2x^2-2-6x^3+4x^2-2x}{(x^2+1)^2}=\dfrac{2x^2+4x-2}{(x^2+1)^2}=\dfrac{2(x^2+2x-1)}{(x^2+1)^2}$

**B4.** $y'=3x^2\sin x+x^3\cos x$

**B5.** $y'=\dfrac{-\sin x(1+\sin x)-\cos x\cdot\cos x}{(1+\sin x)^2}=\dfrac{-\sin x-\sin^2x-\cos^2x}{(1+\sin x)^2}=\dfrac{-\sin x-1}{(1+\sin x)^2}=\dfrac{-1}{1+\sin x}$

**B6.** $y'=6(2x^3-x+4)^5\cdot(6x^2-1)$

**B7.** $y'=\cos(4x^2-1)\cdot8x=8x\cos(4x^2-1)$

**B8.** $y'=e^{3x^2+2x}\cdot(6x+2)=2(3x+1)e^{3x^2+2x}$

**B9.** $y=(\tan x)^{1/2}$; $y'=\frac{1}{2}(\tan x)^{-1/2}\cdot\sec^2x=\dfrac{\sec^2x}{2\sqrt{\tan x}}$

**B10.** $y=[\cos(x^2)]^3$. Layers: outer $u^3$, middle $\cos v$, inner $x^2$.

$y'=3\cos^2(x^2)\cdot(-\sin(x^2))\cdot2x=-6x\sin(x^2)\cos^2(x^2)$

**B11.** $y'=\dfrac{e^x(x^2+1)-e^x\cdot2x}{(x^2+1)^2}=\dfrac{e^x(x^2-2x+1)}{(x^2+1)^2}=\dfrac{e^x(x-1)^2}{(x^2+1)^2}$

**B12.** $y=x^2e^{-x}\sin x$. Apply product rule to $(x^2e^{-x})$ and $\sin x$:

First factor $x^2e^{-x}$: derivative $=2xe^{-x}-x^2e^{-x}=xe^{-x}(2-x)$.

$y'=xe^{-x}(2-x)\sin x+x^2e^{-x}\cos x=xe^{-x}[(2-x)\sin x+x\cos x]$

---

## Part C — Tangent Lines

**C1.** $f(x)=x^3-4x$; $f(2)=8-8=0$ ✓; $f'(x)=3x^2-4$; $f'(2)=8$.

Tangent: $y=8(x-2)=8x-16$.

Normal (slope $=-1/8$): $y=-\frac{1}{8}(x-2)=-\frac{x}{8}+\frac{1}{4}$.

**C2.** $y'=4x^3-4x=0\Rightarrow 4x(x^2-1)=0\Rightarrow x=0,\pm1$.

Points: $(0,0)$, $(1,-1)$, $(-1,-1)$.

**C3.** Tangent at $x=1$: $y=f(1)+f'(1)(x-1)=4+f'(1)(x-1)$.

Passes through $(4,10)$: $10=4+f'(1)(4-1)=4+3f'(1)\Rightarrow f'(1)=2$.

**C4(a).** $f(x)=\sqrt{x}$, $a=9$: $f(9)=3$, $f'(9)=\frac{1}{6}$.

$L(9.04)=3+\frac{1}{6}(0.04)=3+0.00\overline{6}=3.006\overline{6}$.

Exact: $\sqrt{9.04}\approx3.00666$. Error $\approx 0.000004$ ($0.0001\%$).

**C4(b).** $f(x)=x^{10}$, $a=1$: $f(1)=1$, $f'(1)=10$.

$L(1.002)=1+10(0.002)=1.02$.

Exact: $(1.002)^{10}\approx1.02018$. Error $\approx0.00018$ ($0.018\%$).

---

## Part D — Higher Derivatives and Physics

**D1.** $f'=5x^4-30x^2+15$; $f''=20x^3-60x$; $f'''=60x^2-60$; $f^{(4)}=120x$.

**D2.** $y=x\cos x$; $y'=\cos x-x\sin x$; $y''=-\sin x-(\sin x+x\cos x)=-2\sin x-x\cos x$.

**D3.**
(a) $v(t)=3t^2-12t+9=3(t-1)(t-3)$; $a(t)=6t-12=6(t-2)$.

(b) At rest: $v(t)=0\Rightarrow t=1$ or $t=3$.

(c) $v>0$ on $[0,1)\cup(3,\infty)$: moving in positive direction.

(d) $a>0$ when $t>2$: velocity is increasing; if moving backward, slowing down; if moving forward, speeding up.

(e) $s(0)=2$, $s(1)=1-6+9+2=6$, $s(3)=27-54+27+2=2$, $s(4)=64-96+36+2=6$.

Distance $=[s(1)-s(0)]+[s(1)-s(3)]+[s(4)-s(3)]=4+4+4=12$ meters.

**D4.** $y=e^{-x}\sin x$

$y'=-e^{-x}\sin x+e^{-x}\cos x=e^{-x}(\cos x-\sin x)$

Differentiating $y'=e^{-x}(\cos x-\sin x)$ by the product rule:

$y''=-e^{-x}(\cos x-\sin x)+e^{-x}(-\sin x-\cos x)$

$=e^{-x}\left[(-\cos x+\sin x)+(-\sin x-\cos x)\right]=e^{-x}(-2\cos x)=\boxed{-2e^{-x}\cos x}$

Substituting all three into the left-hand side:

$y''+2y'+2y=-2e^{-x}\cos x+2e^{-x}(\cos x-\sin x)+2e^{-x}\sin x$

$=e^{-x}\left(-2\cos x+2\cos x-2\sin x+2\sin x\right)=0$ ✓

So $y=e^{-x}\sin x$ satisfies $y''+2y'+2y=0$, as claimed.

> **Marking note.** The overwhelmingly common error here is $y''=-2e^{-x}\sin x$, obtained by
> mishandling one of the two sign flips in the product rule. It is worth checking explicitly,
> because the *structure* of the student's work looks identical to the correct version — only the
> final trig function differs, and the error then propagates into a non-zero sum. A quick numerical
> spot-check settles it: at $x=1$, $y''=-0.3975$, whereas $-2e^{-1}\sin 1=-0.6191$.

---

## Part E — Chain Rule

**E1(a).** $y=\sin^5(3x)$: outer $u^5$, middle $\sin v$, inner $3x$.

$y'=5\sin^4(3x)\cdot\cos(3x)\cdot3=15\sin^4(3x)\cos(3x)$

**E1(b).** $y=e^{\cos(2x)}$: $y'=e^{\cos(2x)}\cdot(-\sin(2x))\cdot2=-2\sin(2x)e^{\cos(2x)}$

**E1(c).** $y=\left(\frac{x+1}{x-1}\right)^3$: outer $u^3$, inner $\frac{x+1}{x-1}$.

Inner derivative by quotient rule: $\frac{(x-1)-(x+1)}{(x-1)^2}=\frac{-2}{(x-1)^2}$.

$y'=3\left(\frac{x+1}{x-1}\right)^2\cdot\frac{-2}{(x-1)^2}=\frac{-6(x+1)^2}{(x-1)^4}$

**E2(a).** $(f\circ g)'(1)=f'(g(1))\cdot g'(1)=f'(2)\cdot5=4\cdot5=20$

**E2(b).** $(g\circ f)'(2)=g'(f(2))\cdot f'(2)=g'(1)\cdot4=(-3)(4)=-12$

**E2(c).** $\left(\frac{f}{g}\right)'(3)=\frac{f'(3)g(3)-f(3)g'(3)}{[g(3)]^2}=\frac{1\cdot3-2\cdot0}{9}=\frac{3}{9}=\frac{1}{3}$

**E2(d).** $(f\cdot g\circ f)'(1)$: this is $[f(x)\cdot g(f(x))]'$ at $x=1$.

$=(f'(x))(g(f(x)))+(f(x))(g'(f(x))\cdot f'(x))$ at $x=1$

$=f'(1)\cdot g(f(1))+f(1)\cdot g'(f(1))\cdot f'(1)$

$=(-2)\cdot g(3)+(3)\cdot g'(3)\cdot(-2)=(-2)(3)+(3)(0)(-2)=-6$

---

## Part F — Conceptual

**F1.** Correct. Apply product rule twice: $(f\cdot f\cdot f)'=(f\cdot f)'\cdot f+(f\cdot f)\cdot f'=(f'f+ff')\cdot f+f^2\cdot f'=2f'f^2+f^2f'=3f^2f'$.

**F2.** $f'(3)=\lim_{h\to0}\frac{(3+h)^2-9}{h}=\lim_{h\to0}\frac{9+6h+h^2-9}{h}=\lim_{h\to0}(6+h)=6$ ✓

**F3(a).** $|x|$: continuous at 0 ✓. Left deriv $=-1$, right deriv $=+1$, unequal → not differentiable.

**F3(b).** $x|x|$: at $x=0$, $f(0)=0$. $\lim_{h\to0}h|h|/h=\lim_{h\to0}|h|=0$. Differentiable at 0, $f'(0)=0$.

**F3(c).** $f(h)/h=h\sin(1/h)/h=\sin(1/h)$. $\lim_{h\to0}\sin(1/h)$ does not exist. Not differentiable at 0.

---

## Part G — Bonus

**G1.** $(f/g)' = (f\cdot g^{-1})' = f'\cdot g^{-1}+f\cdot(g^{-1})'$.

$(g^{-1})' = \frac{d}{dx}[g(x)^{-1}] = -1\cdot g(x)^{-2}\cdot g'(x) = -g'(x)/g(x)^2$.

So $(f/g)'=f'/g+f\cdot(-g'/g^2)=(f'g-fg')/g^2$. $\square$

**G2(a).** Set $x=y=0$: $f(0)=f(0)f(0)=[f(0)]^2$. So $f(0)(f(0)-1)=0$: either $f(0)=0$ or $f(0)=1$. Since $f(0)=1$ is given, consistent. (If $f(0)=0$, then $f(x)=f(x+0)=f(x)f(0)=0$ for all $x$, contradicting $f'(0)=k$ existing meaningfully.)

**G2(b).** Differentiate $f(x+y)=f(x)f(y)$ with respect to $x$: $f'(x+y)=f'(x)f(y)$. Set $x=0$: $f'(y)=f'(0)f(y)=kf(y)$. $\square$

**G2(c).** $f(x)=e^{kx}$. It satisfies $f(x+y)=e^{k(x+y)}=e^{kx}e^{ky}=f(x)f(y)$, and $f'(x)=ke^{kx}=kf(x)$. With $k=1$: $f(x)=e^x$.
