# MATH 141 — Problem Set 10 Solutions
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

**1. Not changing the limits after u-substitution.** With a definite integral either convert the limits to u, or convert back to x before evaluating. Substituting x-limits into a u-expression is the most common substitution error.

**2. Forgetting du.** The substitution is incomplete until dx is fully expressed in terms of du; a leftover x that cannot be eliminated means the substitution was the wrong choice.

**3. Misapplying symmetry.** ∫_{−a}^{a} f = 0 requires f **odd**; = 2∫₀^a f requires f **even**. Students must state which and why — asserting symmetry without checking f(−x) earns no method marks.

**4. Poor factor choice in integration by parts.** LIATE is a heuristic, not a theorem, but choosing u badly usually yields a harder integral than the original — that is the diagnostic. For the circular cases, the integral must be solved algebraically after it reappears.

---

## Part A — Basic Substitution

**A1.** $u=4x-1$, $du=4dx$. $\int(4x-1)^7dx=\frac14\int u^7du=\frac{u^8}{32}+C=\frac{(4x-1)^8}{32}+C$

**A2.** $u=5x^2+2$, $du=10xdx$. $\int x\sqrt{5x^2+2}dx=\frac1{10}\int\sqrt u\,du=\frac1{10}\cdot\frac{2}3u^{3/2}+C=\frac1{15}(5x^2+2)^{3/2}+C$

**A3.** $u=1+\tan x$, $du=\sec^2x\,dx$. $\int(1+\tan x)^{-3}\sec^2x\,dx=\int u^{-3}du=-\frac{u^{-2}}2+C=-\frac1{2(1+\tan x)^2}+C$

**A4.** $u=\cos x$, $du=-\sin x\,dx$. $\int\cos^4x\sin x\,dx=-\int u^4du=-\frac{u^5}5+C=-\frac{\cos^5x}5+C$

**A5.** $u=1/x$, $du=-\frac1{x^2}dx$. $\int\frac{e^{1/x}}{x^2}dx=-\int e^udu=-e^u+C=-e^{1/x}+C$

**A6.** $u=x^3-2x+5$, $du=(3x^2-2)dx$. $\int\frac{du}u=\ln|u|+C=\ln|x^3-2x+5|+C$

**A7.** $\int\sec x\cdot\frac{\sec x+\tan x}{\sec x+\tan x}dx=\int\frac{\sec^2x+\sec x\tan x}{\sec x+\tan x}dx$

Let $u=\sec x+\tan x$, $du=(\sec x\tan x+\sec^2x)dx$ — exactly the numerator!

$=\int\frac{du}u=\ln|u|+C=\ln|\sec x+\tan x|+C$

**A8.** $u=1-x^2\implies x^2=1-u$, $du=-2x\,dx$. Write $x^3\,dx=x^2\cdot x\,dx=(1-u)\cdot\left(-\frac{du}2\right)$

$\int x^3\sqrt{1-x^2}dx=-\frac12\int(1-u)\sqrt u\,du=-\frac12\int(u^{1/2}-u^{3/2})du$

$=-\frac12\left[\frac23u^{3/2}-\frac25u^{5/2}\right]+C=-\frac13u^{3/2}+\frac15u^{5/2}+C$

$=-\frac13(1-x^2)^{3/2}+\frac15(1-x^2)^{5/2}+C$

---

## Part B — Definite Integrals via Substitution

**B1.** $u=x^2+1$, limits: $x=0\to u=1$; $x=2\to u=5$.

$\frac12\int_1^5u^2du=\frac12\left[\frac{u^3}3\right]_1^5=\frac16(125-1)=\frac{124}6=\frac{62}3$

**B2.** $u=1+\sqrt x$, $du=\frac1{2\sqrt x}dx$, so $\frac{dx}{\sqrt x}=2du$. Limits: $x=1\to u=2$; $x=4\to u=3$.

$\int_2^3\frac{2\,du}u=2[\ln u]_2^3=2(\ln3-\ln2)=2\ln(3/2)$

**B3.** $u=\sin x$, limits: $x=0\to u=0$; $x=\pi/2\to u=1$.

$\int_0^1u^5du=\left[\frac{u^6}6\right]_0^1=\frac16$

**B4.** $u=x^2+1$, limits: $x=0\to u=1$; $x=1\to u=2$.

$\frac12\int_1^2u^{-2}du=\frac12\left[-\frac1u\right]_1^2=\frac12\left(-\frac12+1\right)=\frac14$

**B5.** $u=1+\ln x$, limits: $x=1\to u=1$; $x=e\to u=2$.

$\int_1^2\frac{du}u=[\ln u]_1^2=\ln2$

**B6.** $u=e^x+1$, limits: $x=0\to u=2$; $x=\ln3\to u=4$.

$\int_2^4u^{1/2}du=\left[\frac23u^{3/2}\right]_2^4=\frac23(8-2\sqrt2)=\frac{16}3-\frac{4\sqrt2}3$

---

## Part C — Symmetry

**C1(a).** $f(x)=x^5-3x^3+2x$ is odd (all odd powers). $\int_{-4}^4f\,dx=0$

**C1(b).** $f(x)=\dfrac{x^2\cos x}{1+x^4}$: $f(-x)=\dfrac{x^2\cos x}{1+x^4}=f(x)$ — even.

$\int_{-1}^1f\,dx=2\int_0^1\dfrac{x^2\cos x}{1+x^4}dx$

**C1(c).** $\tan^3x$ is odd ($\tan(-x)=-\tan x$, so $\tan^3(-x)=-\tan^3x$). $\int_{-\pi/4}^{\pi/4}\tan^3x\,dx=0$

---

**C2.** $f(x)=x^6-4x^4+x^2+7$ is even.

$\int_{-2}^2f\,dx=2\int_0^2(x^6-4x^4+x^2+7)dx=2\left[\frac{x^7}7-\frac{4x^5}5+\frac{x^3}3+7x\right]_0^2$

$=2\left[\frac{128}7-\frac{128}5+\frac83+14\right]$

Common denominator 105: $\frac{128}7=\frac{1920}{105}$, $\frac{128}5=\frac{2688}{105}$, $\frac83=\frac{280}{105}$, $14=\frac{1470}{105}$

$=2\left[\frac{1920-2688+280+1470}{105}\right]=2\left[\frac{982}{105}\right]=\frac{1964}{105}$

---

**C3.** Let $I=\int_0^\pi\dfrac{x\sin x}{1+\cos^2x}dx$. Substitute $x\to\pi-x$: $\sin(\pi-x)=\sin x$, $\cos(\pi-x)=-\cos x$, so $\cos^2(\pi-x)=\cos^2x$.

$I=\int_0^\pi\dfrac{(\pi-x)\sin x}{1+\cos^2x}dx=\pi\int_0^\pi\dfrac{\sin x}{1+\cos^2x}dx-I$

$2I=\pi\int_0^\pi\dfrac{\sin x}{1+\cos^2x}dx$

Let $w=\cos x$, $dw=-\sin x\,dx$. Limits: $x=0\to w=1$; $x=\pi\to w=-1$.

$\int_0^\pi\dfrac{\sin x}{1+\cos^2x}dx=\int_{-1}^1\dfrac{dw}{1+w^2}=[\arctan w]_{-1}^1=\dfrac\pi4-\left(-\dfrac\pi4\right)=\dfrac\pi2$

$2I=\pi\cdot\dfrac\pi2=\dfrac{\pi^2}2\implies I=\dfrac{\pi^2}4$

---

## Part D — Integration by Parts (Single)

**D1.** $u=x,dv=\cos3x\,dx$; $du=dx,v=\frac13\sin3x$

$\int x\cos3x\,dx=\frac{x}3\sin3x-\frac13\int\sin3x\,dx=\frac x3\sin3x+\frac19\cos3x+C$

**D2.** $u=x,dv=e^{-2x}dx$; $du=dx,v=-\frac12e^{-2x}$

$\int xe^{-2x}dx=-\frac x2e^{-2x}+\frac12\int e^{-2x}dx=-\frac x2e^{-2x}-\frac14e^{-2x}+C$

**D3.** $u=\ln(2x),dv=dx$; $du=\frac1xdx,v=x$

$\int\ln(2x)dx=x\ln(2x)-\int1\,dx=x\ln(2x)-x+C$

**D4.** $u=\arctan(2x),dv=dx$; $du=\frac2{1+4x^2}dx,v=x$

$\int\arctan(2x)dx=x\arctan(2x)-\int\frac{2x}{1+4x^2}dx$

Let $w=1+4x^2,dw=8x\,dx$: $\int\frac{2x}{1+4x^2}dx=\frac14\int\frac{dw}w=\frac14\ln|w|=\frac14\ln(1+4x^2)$

$=x\arctan(2x)-\frac14\ln(1+4x^2)+C$

**D5.** $u=x,dv=\sec^2x\,dx$; $du=dx,v=\tan x$

$\int x\sec^2x\,dx=x\tan x-\int\tan x\,dx=x\tan x-\ln|\sec x|+C$

**D6.** $u=(\ln x)^2,dv=dx$; $du=\frac{2\ln x}xdx,v=x$

$\int(\ln x)^2dx=x(\ln x)^2-2\int\ln x\,dx=x(\ln x)^2-2(x\ln x-x)+C=x(\ln x)^2-2x\ln x+2x+C$

---

## Part E — Repeated/Circular

**E1.** $\int x^2\sin x\,dx$: $u=x^2,dv=\sin x\,dx$; $du=2x\,dx,v=-\cos x$

$=-x^2\cos x+2\int x\cos x\,dx$

From D1-style computation: $\int x\cos x\,dx=x\sin x+\cos x$ (standard result)

$=-x^2\cos x+2(x\sin x+\cos x)+C=-x^2\cos x+2x\sin x+2\cos x+C$

**E2.** $\int x^2e^{-x}dx$: $u=x^2,dv=e^{-x}dx$; $du=2xdx,v=-e^{-x}$

$=-x^2e^{-x}+2\int xe^{-x}dx$

$\int xe^{-x}dx$: $u=x,dv=e^{-x}dx$; $=-xe^{-x}+\int e^{-x}dx=-xe^{-x}-e^{-x}$

$=-x^2e^{-x}+2(-xe^{-x}-e^{-x})+C=-e^{-x}(x^2+2x+2)+C$

**E3.** $I=\int e^{-x}\cos x\,dx$. $u=\cos x,dv=e^{-x}dx$; $du=-\sin x\,dx,v=-e^{-x}$

$I=-e^{-x}\cos x-\int e^{-x}\sin x\,dx$

For the new integral: $u=\sin x,dv=e^{-x}dx$; $du=\cos x\,dx,v=-e^{-x}$

$\int e^{-x}\sin x\,dx=-e^{-x}\sin x+\int e^{-x}\cos x\,dx=-e^{-x}\sin x+I$

$I=-e^{-x}\cos x-[-e^{-x}\sin x+I]=-e^{-x}\cos x+e^{-x}\sin x-I$

$2I=e^{-x}(\sin x-\cos x)\implies I=\frac{e^{-x}(\sin x-\cos x)}2+C$

**E4.** $I=\int e^{3x}\sin(2x)dx$. $u=\sin2x,dv=e^{3x}dx$; $du=2\cos2x\,dx,v=\frac13e^{3x}$

$I=\frac13e^{3x}\sin2x-\frac23\int e^{3x}\cos2x\,dx$

New integral: $u=\cos2x,dv=e^{3x}dx$; $du=-2\sin2x\,dx,v=\frac13e^{3x}$

$\int e^{3x}\cos2x\,dx=\frac13e^{3x}\cos2x+\frac23\int e^{3x}\sin2x\,dx=\frac13e^{3x}\cos2x+\frac23I$

$I=\frac13e^{3x}\sin2x-\frac23\left[\frac13e^{3x}\cos2x+\frac23I\right]=\frac13e^{3x}\sin2x-\frac29e^{3x}\cos2x-\frac49I$

$I+\frac49I=\frac13e^{3x}\sin2x-\frac29e^{3x}\cos2x$

$\frac{13}9I=\frac{e^{3x}}9(3\sin2x-2\cos2x)$

$I=\frac{e^{3x}(3\sin2x-2\cos2x)}{13}+C$

**E5.** $\int_0^{\pi/2}x\sin x\,dx$: antiderivative (from standard result) $=-x\cos x+\sin x$

$=[-x\cos x+\sin x]_0^{\pi/2}=(0+1)-(0+0)=1$

**E6.** $\int_1^ex^2\ln x\,dx$: $u=\ln x,dv=x^2dx$; $du=\frac1xdx,v=\frac{x^3}3$

$=\left[\frac{x^3}3\ln x\right]_1^e-\int_1^e\frac{x^2}3dx=\left(\frac{e^3}3-0\right)-\frac13\left[\frac{x^3}3\right]_1^e$

$=\frac{e^3}3-\frac19(e^3-1)=\frac{3e^3-e^3+1}9=\frac{2e^3+1}9$

---

## Part F — Mixed Techniques

**F1.** $\int x^3e^{x^2}dx$: let $w=x^2$ first, $dw=2x\,dx$, so $x^2\cdot x\,dx=w\cdot\frac{dw}2$

$=\frac12\int we^wdw$

By parts: $u=w,dv=e^wdw$; $=\frac12[we^w-e^w]+C=\frac12e^w(w-1)+C=\frac12e^{x^2}(x^2-1)+C$

**F2.** $u=\ln x,du=\frac1xdx$. $\int\ln(\ln x)\cdot\frac1xdx$... let $w=\ln x$ first: $\int\ln(w)\,dw=w\ln w-w+C=\ln x\ln(\ln x)-\ln x+C$

**F3.** $f(x)=x^3\sqrt{1-x^2}$: $f(-x)=-x^3\sqrt{1-x^2}=-f(x)$ — **odd**. By symmetry: $\int_{-1}^1f\,dx=0$ immediately, no computation needed.

**F4.** $I=\int\sin(\ln x)dx$. $u=\sin(\ln x),dv=dx$; $du=\frac{\cos(\ln x)}xdx,v=x$

$I=x\sin(\ln x)-\int\cos(\ln x)dx$

New: $u=\cos(\ln x),dv=dx$; $du=-\frac{\sin(\ln x)}xdx,v=x$

$\int\cos(\ln x)dx=x\cos(\ln x)+\int\sin(\ln x)dx=x\cos(\ln x)+I$

$I=x\sin(\ln x)-[x\cos(\ln x)+I]=x\sin(\ln x)-x\cos(\ln x)-I$

$2I=x[\sin(\ln x)-\cos(\ln x)]\implies I=\frac x2[\sin(\ln x)-\cos(\ln x)]+C$

**F5.** $u=\arctan x,dv=x\,dx$; $du=\frac1{1+x^2}dx,v=\frac{x^2}2$

$\int x\arctan x\,dx=\frac{x^2}2\arctan x-\frac12\int\frac{x^2}{1+x^2}dx$

$\frac{x^2}{1+x^2}=1-\frac1{1+x^2}$

$\int\frac{x^2}{1+x^2}dx=x-\arctan x$

$=\frac{x^2}2\arctan x-\frac12(x-\arctan x)+C=\frac{x^2}2\arctan x-\frac x2+\frac12\arctan x+C$

$=\frac{(x^2+1)}2\arctan x-\frac x2+C$

---

## Part G — Conceptual

**G1.** From $\frac{d}{dx}[uv]=u'v+uv'$, integrate both sides: $uv=\int u'v\,dx+\int uv'\,dx=\int v\,du+\int u\,dv$. Rearranging: $\int u\,dv=uv-\int v\,du$.

**G2.** With $u=x,dv=e^{x^2}dx$: finding $v=\int e^{x^2}dx$ is IMPOSSIBLE in elementary terms — $e^{x^2}$ has no elementary antiderivative. Integration by Parts requires being able to find $v$, so this choice fails immediately at step 2 of the method. Correct approach: substitution. Let $w=x^2,dw=2x\,dx$: $\int xe^{x^2}dx=\frac12\int e^wdw=\frac12e^{x^2}+C$.

**G3.** LIATE prioritizes choosing $u$ to be the function that gets SIMPLER when differentiated (logs and inverse trig become algebraic; algebraic functions reduce in degree), while $dv$ should be easy to integrate repeatedly without growing more complex (exponentials and trig functions stay in the same "family" under integration). Counter-example: $\int xe^x\,dx$ with $u=e^x,dv=x\,dx$: $du=e^xdx,v=\frac{x^2}2$. Result: $\frac{x^2}2e^x-\int\frac{x^2}2e^xdx$ — the new integral $\int\frac{x^2}2e^xdx$ is MORE complex (higher power of $x$) than the original, showing this choice makes the problem worse, not better.

**G4 (Bonus).** $u=x^n,dv=e^xdx$; $du=nx^{n-1}dx,v=e^x$.

$\int x^ne^xdx=x^ne^x-n\int x^{n-1}e^xdx \quad\square$

Apply for $n=2$: $\int x^2e^xdx=x^2e^x-2\int xe^xdx$

Apply for $n=1$: $\int xe^xdx=xe^x-1\int e^xdx=xe^x-e^x$

Combine: $\int x^2e^xdx=x^2e^x-2(xe^x-e^x)=x^2e^x-2xe^x+2e^x+C=e^x(x^2-2x+2)+C$ ✓ Matches Wednesday's Example 5.
