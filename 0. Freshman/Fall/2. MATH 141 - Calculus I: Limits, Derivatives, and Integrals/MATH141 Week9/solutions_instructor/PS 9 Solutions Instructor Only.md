# MATH 141 · Problem Set 9 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-21 out of the student handout, where it had been printed below the questions.*

---
*(Revised 2026-09-26 to match the 8-problem set; items are numbered as in the new set.)*

### Problem 1 — The Statement (6)

If $f$ is **continuous** on $[a,b]$ and $A(x)=\int_a^x f(t)\,dt$, then $A$ is differentiable
on $(a,b)$ and $A'(x)=f(x)$.

*Continuity is the load-bearing hypothesis: for merely integrable $f$, $A$ is continuous but need not
be differentiable at $f$'s jumps.*

### Problem 2 — Differentiating Integrals (18)

(a) $\dfrac{1}{1+x^4}$ (b) $\cos(x^2)\cdot 2x = 2x\cos(x^2)$ (c) $-e^{-x^2}$

*(b) is the chain rule test — $\cos(x^2)$ alone loses the $2x$. (c) tests orientation: the variable
is the **lower** limit, so flip the sign.*
*(6 pts each.)*

### Problem 3 — Reading an Accumulation Function (10)

$A'=f$ by FTC 1.

- $f>0$ on $(0,2)$ ⟹ $A'>0$ ⟹ **$A$ is increasing on $(0,2)$**
- $f<0$ on $(2,4)$ ⟹ $A'<0$ ⟹ **$A$ is decreasing on $(2,4)$**
- $A'(2)=f(2)=0$ with $A'$ changing $+\to-$ ⟹ **$A$ has a maximum at $x=2$** by the first-derivative
  test (Week 7)

*Every claim is a Week 7 statement about $A$, obtained purely from a Week 9 statement about $f$.
That transfer is the content of the problem.*

### Problem 4 — Evaluating Integrals (20)

(a) $\big[x^3-x^2+x\big]_0^2 = 8-4+2=\mathbf 6$
(b) $\big[\tfrac23 x^{3/2}\big]_1^4 = \tfrac{16}{3}-\tfrac23=\mathbf{\tfrac{14}{3}}\approx4.6667$
(c) $\big[\ln x\big]_1^2=\mathbf{\ln 2}\approx0.6931$
(d) $\big[-\cos x\big]_0^{\pi}=1+1=\mathbf 2$

*All four verified numerically: $6.0000000000$, $4.6666666667$, $0.6931471806$, $2.0000000000$.*
*(5 pts each.)*

### Problem 5 — Signed and Geometric Area (10)

$\displaystyle\int_0^{2\pi}\sin x\,dx = \big[-\cos x\big]_0^{2\pi}=-1+1=\mathbf 0$;
$\displaystyle\int_0^{2\pi}\lvert\sin x\rvert\,dx=2\int_0^{\pi}\sin x\,dx=\mathbf 4$.

The first is **net signed area**: the hump on $[0,\pi]$ (area $2$) is exactly cancelled by the trough
on $[\pi,2\pi]$ (area $-2$). The second is **geometric area**, which cannot cancel.

*(Verified: $-2.89\times10^{-16}$ and $4.0000000000$.)*

### Problem 6 — Find the Error (12)

The integrand $\frac{1}{x^2}$ is **not continuous on $[-1,1]$** — it is undefined at $x=0$,
and $\frac{1}{x^2}\to+\infty$ there. FTC 2 requires $F'=f$ on the whole interval, and $-\frac1x$ is
not even defined at $0$, let alone an antiderivative there.

The correct statement is that the integral **diverges**: $\int_0^1 x^{-2}dx=\infty$.

**The warning sign:** $\frac{1}{x^2}>0$ everywhere it is defined, so any legitimate value of the
integral must be **positive**. Producing $-2$ for a strictly positive integrand is impossible, and
that impossibility is detectable without knowing anything about improper integrals. *Full marks
require this reasoning; identifying the discontinuity alone earns 8 of 12.*

### Problem 7 — Filling a Tank (12)

$\displaystyle V(t)=10+\int_0^t 3s^2\,ds = 10 + \big[s^3\big]_0^t=\mathbf{10+t^3}$ litres.

**Check:** $V'(t)=3t^2=r(t)$ ✓, and $V(0)=10$ ✓.

*The initial condition enters as the constant, not through the integral — the integral supplies only
the **change**. This is the single most transferable idea in the section.*

### Problem 8 — What the FTC Really Says (12)

Write $A(x)=\int_a^x f$.

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
explaining it — 5 of 12.*

---

*MATH 141 · Week 9 · Problem Set 9 · © CSE Department*
