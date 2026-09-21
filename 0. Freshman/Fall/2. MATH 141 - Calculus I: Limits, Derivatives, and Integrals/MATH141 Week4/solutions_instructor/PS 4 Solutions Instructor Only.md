# MATH 141 · Problem Set 4 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-21 out of the student handout, where it had been printed below the questions.*

---

*Every derivative below was verified numerically by central difference; agreement to 8 decimal places.*

### Part A

| | $f'(x)$ | Rule | Check at $x$ |
|---|---|---|---|
| **A1** | $6x(x^3-2x)+(3x^2+1)(3x^2-2)$ | Product | $x=2$: $178.00000000$ |
| **A2** | $\dfrac{2(x^2+3)-(2x+1)(2x)}{(x^2+3)^2}=\dfrac{-2x^2-2x+6}{(x^2+3)^2}$ | Quotient | $x=1$: $0.12500000$ |
| **A3** | $2x\cos(x^2)$ | Chain | $x=1.5$: $-1.88452087$ |
| **A4** | $10x(x^2+1)^4$ | Chain + power | $x=1$: $160.00000000$ |
| **A5** | $3e^{3x}$ | Chain | $x=0.5$: $13.44506721$ |
| **A6** | $\dfrac{x}{\sqrt{x^2+1}}$ | Chain + power | $x=2$: $0.89442719$ |
| **A7** | $\dfrac{\cos x}{2\sqrt{1+\sin x}}$ | Chain + power | $x=0.8$: $0.26582133$ |
| **A8** | $\dfrac{1}{(x^2+1)^{3/2}}$ | Quotient + chain | $x=1.2$: $0.26237066$ |

**A8 is the discriminating one.** The quotient rule gives

$$\frac{\sqrt{x^2+1}-x\cdot\frac{x}{\sqrt{x^2+1}}}{x^2+1}
=\frac{(x^2+1)-x^2}{(x^2+1)^{3/2}}=\frac{1}{(x^2+1)^{3/2}}$$

and the simplification is worth 2 of the 5 — students who stop at the unsimplified form have done the
calculus but not the algebra.

*Marking: 3 pts for a correct derivative, 2 for naming the rule(s) and showing the step.*

### Part B

**B1.** $f'=4x^3-6x$, $f''=12x^2-6$, $f'''=24x$, $f^{(4)}=24$, $f^{(5)}=\mathbf 0$.

*A degree-4 polynomial dies at the 5th derivative.*

**B2.** $\dfrac{d^{50}}{dx^{50}}\cos x$: the derivatives cycle with **period 4**, and
$50 \equiv 2 \pmod 4$. Two derivatives from $\cos x$ gives $-\cos x$. **Answer: $-\cos x$.**

$\dfrac{d^{9}}{dx^{9}}x^6 = \mathbf 0$, since $9 > 6$ and $\frac{d^n}{dx^n}x^k=0$ once $n>k$.

*3 pts each, plus 1 for stating the governing pattern rather than grinding out nine derivatives.*

**B3.** With $y=e^{-x}\sin x$:

$$y'=-e^{-x}\sin x+e^{-x}\cos x=e^{-x}(\cos x-\sin x)$$
$$y''=-e^{-x}(\cos x-\sin x)+e^{-x}(-\sin x-\cos x)=e^{-x}(-2\cos x)$$

Then

$$y''+2y'+2y=e^{-x}\big[-2\cos x+2(\cos x-\sin x)+2\sin x\big]=e^{-x}\cdot 0=0 \quad\blacksquare$$

*Marking: 3 for $y'$, 3 for $y''$, 1 for the cancellation. The product rule is needed twice.*

### Part C

**C1.** $v(t)=4t^3-24t^2+36t=\mathbf{4t(t-3)^2}$; $a(t)=12t^2-48t+36=\mathbf{12(t-1)(t-3)}$.

**C2.** $v=0$ at $t=\mathbf{0}$ and $t=\mathbf{3}$. Note $t=3$ is a **double root**.

**C3.** Displacement $=s(4)-s(0)=32-0=\mathbf{32}$ m. *(Verified.)*

**C4.** Distance $=\mathbf{32}$ m — **equal** to the displacement.

**The justification is the marking point.** Although $v(3)=0$, the factor $(t-3)^2$ is a *squared*
term, so $v$ **touches zero without changing sign**. Verified: $v\ge0$ throughout $[0,4]$. The
particle never reverses, so it never retraces ground and distance equals displacement.

*Contrast the Wednesday lecture's example, where $v=3(t-1)(t-3)$ had simple roots, the sign did
change, and distance ($12$ m) exceeded displacement ($4$ m). A student who splits at $t=3$ and adds
absolute values still gets $32$ — award full marks, but note the reasoning shortcut.*

**C5.** At $t=2$: $v(2)=4(2)(1)^2=+8$ and $a(2)=12(1)(-1)=-12$.

**Opposite signs ⟹ slowing down.** The particle is moving forward while decelerating.

*Reject "slowing down because $a<0$" without the comparison — the sign of $a$ alone does not decide.*

### Part D

**D1.** $C'(q)=0.03q^2-1.2q+13$, so $C'(30)=27-36+13=\mathbf{4.000}$.

$C(31)-C(30)=\mathbf{4.310}$ (verified). Difference: $0.310$.

**Why:** $C'(30)$ is the *instantaneous* rate — the tangent slope. The true marginal cost is the
*average* rate over a unit step. They coincide only where $C$ is locally linear.

**What controls it:** the second derivative. From $C(q+1)\approx C(q)+C'(q)+\tfrac12C''(q)$, the error
is about $\tfrac12C''(q)$. Here $C''(q)=0.06q-1.2$, so $\tfrac12C''(30)=0.300$ — against a measured
discrepancy of $0.310$. Verified across $q=10,20,30,40$: errors $-0.290, +0.010, +0.310, +0.610$
against $\tfrac12C''$ of $-0.300, 0.000, +0.300, +0.600$.

*Full marks require naming $C''$. "They're approximations" scores 3 of 8.*

**D2.** Take $f(x)=g(x)=x$ at any point, say $x=3$.

- $(fg)(x)=x^2$, so $(fg)'(3)=2(3)=\mathbf 6$.
- $f'(3)g'(3)=1\cdot1=\mathbf 1$.

$6 \ne 1$, so the claim is false.

**Correct rule:** $(fg)'=f'g+fg'$. Check: $1\cdot3+3\cdot1=6$. ✓

*Any concrete counterexample earns full credit; a general argument without numbers earns 4 of 7,
since the question asks specifically for one.*

---

*MATH 141 · Week 4 · Problem Set 4 · © CSE Department*
