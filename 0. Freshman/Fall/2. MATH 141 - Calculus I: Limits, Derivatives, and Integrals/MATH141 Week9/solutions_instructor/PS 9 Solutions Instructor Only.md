# MATH 141 · Problem Set 9 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-21 out of the student handout, where it had been printed below the questions.*

---

### Part A

**A1.** If $f$ is **continuous** on $[a,b]$ and $A(x)=\int_a^x f(t)\,dt$, then $A$ is differentiable
on $(a,b)$ and $A'(x)=f(x)$.

*Continuity is the load-bearing hypothesis: for merely integrable $f$, $A$ is continuous but need not
be differentiable at $f$'s jumps.*

**A2.** *(3 each)*
(a) $\dfrac{1}{1+x^4}$ (b) $\cos(x^2)\cdot 2x = 2x\cos(x^2)$ (c) $-e^{-x^2}$

*(b) is the chain rule test — $\cos(x^2)$ alone loses the $2x$. (c) tests orientation: the variable
is the **lower** limit, so flip the sign.*

**A3.** $G'(x)=\sin(x^3)\cdot 3x^2-\sin(x^2)\cdot 2x$.

*Verified at $x=1.3$: the formula gives $1.5264599$ and a central difference on the numerically
evaluated $G$ gives $1.5264599$.*

**A4.** $A'=f$ by FTC 1.

- $f>0$ on $(0,2)$ ⟹ $A'>0$ ⟹ **$A$ is increasing on $(0,2)$**
- $f<0$ on $(2,4)$ ⟹ $A'<0$ ⟹ **$A$ is decreasing on $(2,4)$**
- $A'(2)=f(2)=0$ with $A'$ changing $+\to-$ ⟹ **$A$ has a maximum at $x=2$** by the first-derivative
  test (Week 7)

*Every claim is a Week 7 statement about $A$, obtained purely from a Week 9 statement about $f$.
That transfer is the content of the problem.*

### Part B

**B1.** *(3 each)*
(a) $\big[x^3-x^2+x\big]_0^2 = 8-4+2=\mathbf 6$
(b) $\big[\tfrac23 x^{3/2}\big]_1^4 = \tfrac{16}{3}-\tfrac23=\mathbf{\tfrac{14}{3}}\approx4.6667$
(c) $\big[\ln x\big]_1^2=\mathbf{\ln 2}\approx0.6931$
(d) $\big[-\cos x\big]_0^{\pi}=1+1=\mathbf 2$

*All four verified numerically: $6.0000000000$, $4.6666666667$, $0.6931471806$, $2.0000000000$.*

**B2.** $\displaystyle\int_0^{2\pi}\sin x\,dx = \big[-\cos x\big]_0^{2\pi}=-1+1=\mathbf 0$;
$\displaystyle\int_0^{2\pi}\lvert\sin x\rvert\,dx=2\int_0^{\pi}\sin x\,dx=\mathbf 4$.

The first is **net signed area**: the hump on $[0,\pi]$ (area $2$) is exactly cancelled by the trough
on $[\pi,2\pi]$ (area $-2$). The second is **geometric area**, which cannot cancel.

*(Verified: $-2.89\times10^{-16}$ and $4.0000000000$.)*

**B3.** The integrand $\frac{1}{x^2}$ is **not continuous on $[-1,1]$** — it is undefined at $x=0$,
and $\frac{1}{x^2}\to+\infty$ there. FTC 2 requires $F'=f$ on the whole interval, and $-\frac1x$ is
not even defined at $0$, let alone an antiderivative there.

The correct statement is that the integral **diverges**: $\int_0^1 x^{-2}dx=\infty$.

**The warning sign:** $\frac{1}{x^2}>0$ everywhere it is defined, so any legitimate value of the
integral must be **positive**. Producing $-2$ for a strictly positive integrand is impossible, and
that impossibility is detectable without knowing anything about improper integrals. *Full marks
require this reasoning; identifying the discontinuity alone earns 5 of 7.*

### Part C

**C1.** $v(t)=t^2-4$ is negative on $[0,2)$, zero at $2$, positive on $(2,4]$.

**(a) Displacement** $=\displaystyle\int_0^4 (t^2-4)\,dt=\Big[\tfrac{t^3}{3}-4t\Big]_0^4
=\tfrac{64}{3}-16=\mathbf{\tfrac{16}{3}}\approx5.333$ m.

**(b) Total distance.** Split at $t=2$:

$$\int_0^2 (4-t^2)\,dt=\Big[4t-\tfrac{t^3}{3}\Big]_0^2 = 8-\tfrac83=\tfrac{16}{3}$$
$$\int_2^4 (t^2-4)\,dt=\Big[\tfrac{t^3}{3}-4t\Big]_2^4=\tfrac{16}{3}-\left(-\tfrac{16}{3}\right)=\tfrac{32}{3}$$

$$\text{Total} = \frac{16}{3}+\frac{32}{3}=\frac{48}{3}=\mathbf{16}\text{ m}$$

*(Verified: $\int_0^4\lvert v\rvert\,dt = 16.0000000000$, $\int_0^4 v\,dt = 5.3333333333$.)*

**(c)** Displacement is net change in position — motion backwards subtracts. Distance is the length
of the path travelled — every metre counts, whichever way it was walked. They agree only when $v$
never changes sign.

*The coincidence that displacement $\tfrac{16}{3}$ equals the **first piece** $\tfrac{16}{3}$ is
arithmetic, not structure. A student who reports $\tfrac{32}{3}$ as the distance has stopped after
the second piece; a student who reports $\tfrac{16}{3}$ has confused displacement for distance.
Both lose 4 of the 10.*

**C2.** $\displaystyle f_{\text{avg}}=\frac{1}{3}\int_0^3 x^2dx=\frac13\cdot\frac{27}{3}=\mathbf 3$.

MVT for integrals: solve $c^2=3$ on $[0,3]$ ⟹ $c=\sqrt3\approx\mathbf{1.7321}$ (reject $-\sqrt3$,
outside the interval).

*(Verified: average $=3.0000000000$.)*

**C3.** **MVT for integrals.** If $f$ is continuous on $[a,b]$, there exists $c\in[a,b]$ with
$\displaystyle\int_a^b f = f(c)(b-a)$.

**Use in FTC 1's proof:** with $A(x)=\int_a^x f$,

$$\frac{A(x+h)-A(x)}{h}=\frac{1}{h}\int_x^{x+h}f = f(c_h)$$

for some $c_h$ between $x$ and $x+h$. As $h\to0$, $c_h\to x$ is forced by squeezing, and continuity
of $f$ gives $f(c_h)\to f(x)$. Hence $A'(x)=f(x)$. ∎

*This is exactly where continuity is consumed — twice: once for the MVT, once for $f(c_h)\to f(x)$.*

**C4.** $\displaystyle V(t)=10+\int_0^t 3s^2\,ds = 10 + \big[s^3\big]_0^t=\mathbf{10+t^3}$ litres.

**Check:** $V'(t)=3t^2=r(t)$ ✓, and $V(0)=10$ ✓.

*The initial condition enters as the constant, not through the integral — the integral supplies only
the **change**. This is the single most transferable idea in the section.*

### Part D

**D1.** $F$ is well defined because $e^{-t^2}$ is continuous everywhere, so the integral exists for
every $x$. "No elementary formula" is a statement about our notation, not about the function.

What is provable without a formula:

| Property | Reason |
|---|---|
| $F(0)=0$ | Integral over a degenerate interval |
| $F'(x)=e^{-x^2}$ | **FTC 1** |
| $F$ strictly increasing everywhere | $F'=e^{-x^2}>0$ for all $x$ |
| $F$ concave up for $x<0$, down for $x>0$ | $F''=-2xe^{-x^2}$, sign flips at $0$ |
| Inflection at $x=0$ | $F''$ changes sign there |
| $F$ odd | The integrand is even |
| $F(x)\to\tfrac{\sqrt\pi}{2}\approx0.8862$ as $x\to\infty$ | Increasing and bounded |

*(Verified: $F(1)=0.7468241328$, $F(2)=0.8820813908$, $F(3)=0.8862073483$, closing on
$\sqrt\pi/2=0.8862269255$. Numerical differentiation of $F$ at $x=0.5,1,2$ reproduces
$e^{-x^2}$ to nine decimals.)*

This function is $\frac{\sqrt\pi}{2}\operatorname{erf}(x)$ — named, tabulated, and central to
statistics. It has no elementary antiderivative and never needed one.

**Marking:** 1 pt per row, 3 for the opening argument that continuity alone guarantees existence.

**D2.** Write $A(x)=\int_a^x f$.

- **FTC 1:** $A'=f$ — differentiating the accumulation returns the rate.
- **FTC 2:** $\int_a^b F' = F(b)-F(a)$ — accumulating a rate returns the net change.

They are the same claim read in two directions: *accumulate-then-differentiate* and
*differentiate-then-accumulate* are both the identity. FTC 2 follows from FTC 1 in three lines, since
$A$ and $F$ differ by a constant when both are antiderivatives of $f$.

**Why neither is obvious.** The derivative is a **local** limit of difference quotients at one point.
The integral is a **global** limit of sums over an entire interval. Nothing in either definition
mentions the other; they were developed for unrelated problems — tangents and areas — over centuries.
That two limits of such different character invert one another is a theorem with real content, and
it is the reason integration is computable at all. Without it, every definite integral would require
evaluating a limit of sums by hand.

*Full marks need the local-vs-global contrast. "They're inverses" restates the theorem rather than
explaining it — 4 of 10.*

---

*MATH 141 · Week 9 · Problem Set 9 · © CSE Department*
