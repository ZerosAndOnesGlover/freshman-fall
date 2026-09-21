# MATH 141 · Problem Set 5 Solutions
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

**1. Forgetting dy/dx when differentiating y-terms implicitly.** Every y is a function of x, so d/dx(y³) = 3y²·(dy/dx). Dropping the factor is the defining error of implicit differentiation.

**2. Substituting numbers before differentiating in related rates.** Values that vary must stay symbolic until after d/dt is applied. Substituting a changing quantity early turns it into a constant and forces its rate to zero.

**3. Not identifying which rates are given and which is wanted.** Require an explicit list (dV/dt known, dr/dt wanted) plus the equation relating the variables, before any differentiation. Most wrong answers here are wrong at that stage.

**4. Mishandling inverse-trig derivatives.** d/dx arcsin x = 1/√(1−x²) — the domain restriction |x| < 1 matters, and the sign distinguishes arccos from arcsin.

---

## Part A — Implicit Differentiation

**A1(a).** $x^4+y^4=16$

$4x^3+4y^3y'=0 \implies y'=-\dfrac{x^3}{y^3}$

**A1(b).** $\sqrt{x}+\sqrt{y}=4$

$\dfrac{1}{2\sqrt{x}}+\dfrac{1}{2\sqrt{y}}y'=0 \implies y'=-\dfrac{\sqrt{y}}{\sqrt{x}}=-\sqrt{\dfrac{y}{x}}$

**A1(c).** $ye^x+xe^y=1$

$y'e^x+ye^x+e^y+xe^yy'=0$

$y'(e^x+xe^y)=-ye^x-e^y$

$y'=\dfrac{-ye^x-e^y}{e^x+xe^y}$

**A1(d).** $\cos(x-y)=x\sin y$

$-\sin(x-y)(1-y')=\sin y+x\cos y\cdot y'$

$-\sin(x-y)+\sin(x-y)y'=\sin y+x\cos y\cdot y'$

$y'[\sin(x-y)-x\cos y]=\sin y+\sin(x-y)$

$y'=\dfrac{\sin y+\sin(x-y)}{\sin(x-y)-x\cos y}$

---

**A2.** $x^2-xy+y^2=3$

$2x-y-xy'+2yy'=0$

$y'(2y-x)=y-2x$

$y'=\dfrac{y-2x}{2y-x}$

For $y''$: differentiate $y'(2y-x)=y-2x$ w.r.t. $x$:

$y''(2y-x)+y'(2y'-1)=y'-2$

$y''=\dfrac{y'-2-y'(2y'-1)}{2y-x}=\dfrac{y'-2-2y'^2+y'}{2y-x}=\dfrac{2y'-2-2y'^2}{2y-x}$

Substitute $y'=\dfrac{y-2x}{2y-x}$ and put everything over $(2y-x)^2$. The numerator collapses to
$-6(x^2-xy+y^2)$, which is $-18$ by the original equation:

$y''=-\dfrac{18}{(2y-x)^3}$

*(Checked with SymPy. The old key left this unfinished.)*

---

**A3.** $x^2+2xy-y^2+x=5$

$2x+2y+2xy'-2yy'+1=0$

$y'(2x-2y)=-(2x+2y+1)$

$y'=\dfrac{-(2x+2y+1)}{2(x-y)}$

Horizontal tangent: $y'=0 \implies 2x+2y+1=0 \implies y=-x-\tfrac{1}{2}$.

Substitute into curve: $x^2+2x(-x-\tfrac{1}{2})-(-x-\tfrac{1}{2})^2+x=5$

$x^2-2x^2-x-x^2-x-\tfrac{1}{4}+x=5$

$-2x^2-x-\tfrac{1}{4}=5$

$-2x^2-x-\tfrac{21}{4}=0 \implies 8x^2+4x+21=0$

Discriminant: $16-672<0$. No real solutions — no horizontal tangents on this curve.

---

## Part B — Logarithmic Derivatives

**B1(a).** $y'=\dfrac{4x^3+6x}{x^4+3x^2-1}$

**B1(b).** $\ln\!\left(\dfrac{x^2+1}{x^2-1}\right)=\ln(x^2+1)-\ln(x^2-1)$

$y'=\dfrac{2x}{x^2+1}-\dfrac{2x}{x^2-1}=2x\cdot\dfrac{(x^2-1)-(x^2+1)}{(x^2+1)(x^2-1)}=\dfrac{-4x}{x^4-1}$

**B1(c).** $y'=2x\ln(3x)+x^2\cdot\dfrac{1}{x}=2x\ln(3x)+x$

**B1(d).** $y'=\dfrac{1}{\ln x}\cdot\dfrac{1}{x}=\dfrac{1}{x\ln x}$

**B1(e).** $y'=\dfrac{3x^2}{(x^3+1)\ln 5}$

**B2(a).** $\ln y=\tan x\ln x$

$\dfrac{y'}{y}=\sec^2x\ln x+\dfrac{\tan x}{x}$

$y'=x^{\tan x}\!\left(\sec^2x\ln x+\dfrac{\tan x}{x}\right)$

**B2(b).** $\ln y=\tfrac{3}{2}\ln x+4\ln(2x-1)-\tfrac{1}{2}\ln(x^2+1)$

$\dfrac{y'}{y}=\dfrac{3}{2x}+\dfrac{8}{2x-1}-\dfrac{x}{x^2+1}$

$y'=\dfrac{x^{3/2}(2x-1)^4}{\sqrt{x^2+1}}\!\left(\dfrac{3}{2x}+\dfrac{8}{2x-1}-\dfrac{x}{x^2+1}\right)$

---

## Part C — Inverse Trig

**C1(a).** $y'=\dfrac{12x^2}{1+16x^6}$

**C1(b).** $y'=\dfrac{1/3}{\sqrt{1-(x/3)^2}}=\dfrac{1}{\sqrt{9-x^2}}$

**C1(c).** $y'=\arctan x+\dfrac{x}{1+x^2}-\dfrac{2x}{2(1+x^2)}=\arctan x+\dfrac{x}{1+x^2}-\dfrac{x}{1+x^2}=\arctan x$

*This is a well-known antiderivative identity: $\int\arctan x\,dx = x\arctan x-\tfrac{1}{2}\ln(1+x^2)+C$.*

**C1(d).** $y=\arctan(x^{-1})$; $y'=\dfrac{-x^{-2}}{1+x^{-2}}=\dfrac{-1/x^2}{(x^2+1)/x^2}=\dfrac{-1}{x^2+1}$

*Note: $\arctan(1/x)+\arctan x=\pi/2$ for $x>0$, consistent with $(\arctan x)'=1/(1+x^2)$ and $(\arctan(1/x))'=-1/(1+x^2)$.*

**C2.** $(\arctan x)'=\dfrac{1}{1+x^2}$, $(\text{arccot}\,x)'=\dfrac{-1}{1+x^2}$. Sum $=0$.

Since their derivatives sum to zero, $\arctan x+\text{arccot}\,x=C$ (constant). At $x=1$: $\arctan 1+\text{arccot}\,1=\pi/4+\pi/4=\pi/2$. So $C=\pi/2$.

---

## Part D — Related Rates

**D1.** $V=\tfrac{4}{3}\pi r^3$, $\dfrac{dV}{dt}=-1$.

$\dfrac{dV}{dt}=4\pi r^2\dfrac{dr}{dt} \implies \dfrac{dr}{dt}=\dfrac{-1}{4\pi(25)}=\dfrac{-1}{100\pi}$ cm/min.

$SA=4\pi r^2$, $\dfrac{d(SA)}{dt}=8\pi r\dfrac{dr}{dt}=8\pi(5)\cdot\dfrac{-1}{100\pi}=\dfrac{-2}{5}$ cm²/min.

**D2(a).** $x^2+y^2=169$. At $x=5$: $y=12$.

$2x\dfrac{dx}{dt}+2y\dfrac{dy}{dt}=0 \implies \dfrac{dy}{dt}=-\dfrac{x}{y}\cdot\dfrac{dx}{dt}=-\dfrac{5}{12}(2)=-\dfrac{5}{6}$ m/s.

**D2(b).** $\cos\theta=x/13$, so $-\sin\theta\dfrac{d\theta}{dt}=\dfrac{1}{13}\dfrac{dx}{dt}$.

At $x=5$: $\sin\theta=12/13$.

$-\dfrac{12}{13}\dfrac{d\theta}{dt}=\dfrac{2}{13} \implies \dfrac{d\theta}{dt}=-\dfrac{1}{6}$ rad/s.

**D3.** Cross-section: isosceles triangle. By similar triangles, width $w=2h$ (since $w/h=2/1$).

Cross-sectional area: $A_{cs}=\tfrac{1}{2}(2h)(h)=h^2$.

Volume: $V=A_{cs}\cdot L=10h^2$.

$\dfrac{dV}{dt}=20h\dfrac{dh}{dt} \implies 0.5=20(0.3)\dfrac{dh}{dt}=6\dfrac{dh}{dt}$

$\dfrac{dh}{dt}=\dfrac{0.5}{6}=\dfrac{1}{12}\approx0.0833$ m/min.

**D4.** At $t=0.5$ h: $x=4(0.5)=2$ km (east), $y=3(0.5)=1.5$ km (north).

$D^2=x^2+y^2$; $D=\sqrt{4+2.25}=\sqrt{6.25}=2.5$ km.

$2D\dfrac{dD}{dt}=2x\dfrac{dx}{dt}+2y\dfrac{dy}{dt}=2(2)(4)+2(1.5)(3)=16+9=25$

$\dfrac{dD}{dt}=\dfrac{25}{2(2.5)}=5$ km/h.

---

## Part E — Mixed

**E1.** $y'=2\arcsin x\cdot\dfrac{1}{\sqrt{1-x^2}}=\dfrac{2\arcsin x}{\sqrt{1-x^2}}$

**E2.** $y=e^{\arctan x}(1+x^2)^{1/2}$

$y'=e^{\arctan x}\cdot\dfrac{1}{1+x^2}\cdot(1+x^2)^{1/2}+e^{\arctan x}\cdot\dfrac{1}{2}(1+x^2)^{-1/2}\cdot2x$

Simplifying each term, and using $\dfrac{\sqrt{1+x^2}}{1+x^2}=\dfrac{1}{\sqrt{1+x^2}}$:

$=e^{\arctan x}\!\left[\dfrac{\sqrt{1+x^2}}{1+x^2}+\dfrac{x}{\sqrt{1+x^2}}\right]=e^{\arctan x}\!\left[\dfrac{1}{\sqrt{1+x^2}}+\dfrac{x}{\sqrt{1+x^2}}\right]=\dfrac{e^{\arctan x}(1+x)}{\sqrt{1+x^2}}$

**E3.** $\ln y=x^2\ln x$

$\dfrac{y'}{y}=2x\ln x+x$

$y'=x^{x^2}(2x\ln x+x)=x^{x^2+1}(2\ln x+1)$

---

## Part F — Conceptual

**F1.** If you substitute $x=6$, $y=8$ into $x^2+y^2=100$ before differentiating, you get $100=100$, which differentiates to $0=0$ — a useless identity. The variables must remain variable during differentiation because we need to track how they change relative to each other. Specific numerical values are a single snapshot; the derivative captures the rate of change as we move through that snapshot.

**F2.** The power rule $(x^n)'=nx^{n-1}$ requires $n$ to be a **constant**. In $y=x^x$, the exponent is $x$ — a variable. The student treated a variable exponent as a constant, which is invalid. The power rule and exponential rule each handle only one special case; $x^x$ is neither. Logarithmic differentiation gives the correct $y'=x^x(\ln x+1)$.
