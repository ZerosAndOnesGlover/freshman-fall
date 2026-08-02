# MATH 141 — Quiz 12
## Administered: start of Week 12, Monday
### Covers: Week 11 — applications of integration

**Duration:** 15 minutes · Closed book · **20 points**

---

## Section A — Short Answer (2 pts each)

**A1.** Write the integral for the area between $y=f(x)$ and $y=g(x)$ on $[a,b]$, stating any
condition required.

**A2.** Find the area between $y=x$ and $y=x^2$ on $[0,1]$.

**A3.** State the disk-method formula for revolving $y=f(x)$ about the $x$-axis.

**A4.** State the washer formula, and the most common error in applying it.

**A5.** State the shell formula and say when you would prefer it to washers.

---

## Section B — Longer (5 pts each)

**B1.** Find the area between $y=\sin x$ and $y=\cos x$ on $[0,\pi/2]$. Show the split and explain
why it is required.

**B2.** The region under $y=x^2$ on $[0,2]$ is revolved about the $y$-axis. Find the volume by
shells, then verify it by washers in $y$.

---

**Total: 20 points**

---

## Answer Key (Instructor Copy)

**A1.** $A=\displaystyle\int_a^b\big[f(x)-g(x)\big]dx$, **provided $f\ge g$ throughout $[a,b]$**.
Otherwise split at every crossing, or integrate $\lvert f-g\rvert$.

*1 pt for the integral, 1 for the condition. The condition is the mark most often lost.*

**A2.** $\displaystyle\int_0^1(x-x^2)dx=\tfrac12-\tfrac13=\mathbf{\tfrac16}$ *(verified $0.1666666667$)*.

**A3.** $V=\pi\displaystyle\int_a^b\big[f(x)\big]^2dx$.

**A4.** $V=\pi\displaystyle\int\big[R_{\text{out}}^2-R_{\text{in}}^2\big]dx$.

**The common error:** writing $\pi\int(R_o-R_i)^2dx$ — squaring the difference instead of
differencing the squares. Verified to be wrong by a factor of **5** in the standard $\sqrt x$-vs-$x$
example ($\pi/30$ instead of $\pi/6$).

**A5.** $V=2\pi\displaystyle\int_a^b x\,f(x)\,dx$.

**Prefer shells** when revolving about the **$y$-axis** with the region given as $y=f(x)$ — shells
slice parallel to the axis and need no inversion to $x=g(y)$.

**B1.** The curves cross at $x=\pi/4$.

$$A=\int_0^{\pi/4}(\cos x-\sin x)dx+\int_{\pi/4}^{\pi/2}(\sin x-\cos x)dx=\mathbf{2(\sqrt2-1)}\approx0.8284$$

*(Verified $0.8284271247$.)*

**Why the split is required:** a single integral of $\sin x-\cos x$ over $[0,\pi/2]$ gives **exactly
0** — verified — because the two equal regions cancel. The unsplit integral computes a *signed net*
quantity, not an area.

*Marking: 2 for the crossing point, 2 for the two correct integrals, 1 for the explanation. A
student who answers $0$ has made the exact error the question tests.*

**B2. Shells:** $V=2\pi\displaystyle\int_0^2x\cdot x^2dx=2\pi\left[\tfrac{x^4}{4}\right]_0^2=\mathbf{8\pi}$

**Washers in $y$:** outer radius $2$, inner radius $\sqrt y$, $0\le y\le4$:

$$V=\pi\int_0^4\big[4-y\big]dy=\pi\left[4y-\tfrac{y^2}{2}\right]_0^4=\mathbf{8\pi}$$

Both verified as $25.13274123$.

*Marking: 3 for shells, 2 for the washer verification. The agreement of two independent set-ups is
the strongest available check, and students should be told so.*

---

*MATH 141 · Week 12 · Quiz 12 · © CSE Department*
