# MATH 141 · Calculus I
## Week 6 · Lecture 2 (Tuesday)
### Rolle's Theorem and the Mean Value Theorem

**Date:** Tuesday 3 November 2026 · 11:00–11:50 · Week 6

---

**Reading:** Stewart §4.2 | Spivak Ch. 11 (§11.2)

---

## 1. Rolle's Theorem

> **Theorem (Rolle).** Let $f$ be a function such that:
> 1. $f$ is continuous on $[a,b]$
> 2. $f$ is differentiable on $(a,b)$
> 3. $f(a) = f(b)$
>
> Then there exists at least one $c \in (a,b)$ such that $f'(c) = 0$.

**Geometric meaning:** If a curve starts and ends at the same height, and it's smooth (differentiable) in between, then somewhere it must have a horizontal tangent.

**Proof:**

By the EVT (continuity on $[a,b]$), $f$ attains an absolute max $M$ and absolute min $m$ on $[a,b]$.

**Case 1:** $M = m$. Then $f$ is constant on $[a,b]$, so $f'(x) = 0$ for all $x \in (a,b)$ — any $c$ works.

**Case 2:** $M \neq m$. Since $f(a) = f(b)$, at least one of $M, m$ is attained at an interior point $c \in (a,b)$ (not at both endpoints, since the endpoints have equal value and $M \neq m$ means they can't both be extrema). By Fermat's Theorem, since $f$ is differentiable at $c$ (given) and $c$ is a local extremum, $f'(c) = 0$. $\square$

### Example 1

Verify Rolle's Theorem applies to $f(x) = x^3 - 3x^2 + 2x$ on $[0, 1]$, then find the value(s) of $c$.

**Check hypotheses:** $f$ is a polynomial — continuous and differentiable everywhere. $f(0) = 0$. $f(1) = 1 - 3 + 2 = 0$. So $f(0) = f(1) = 0$. ✓ All hypotheses hold.

**Find $c$:** $f'(x) = 3x^2 - 6x + 2 = 0$

$$x = \frac{6 \pm \sqrt{36-24}}{6} = \frac{6\pm\sqrt{12}}{6} = 1 \pm \frac{\sqrt{3}}{3}$$

$c_1 = 1 - \dfrac{\sqrt{3}}{3} \approx 0.423$ and $c_2 = 1+\dfrac{\sqrt{3}}{3}\approx 1.577$.

Only $c_1 \in (0,1)$. So $c = 1 - \dfrac{\sqrt{3}}{3}$.

### Example 2 — Application: Counting Roots

Show that $f(x) = x^3 + x - 1$ has **exactly one** real root.

**Existence:** $f(0) = -1 < 0$, $f(1) = 1 > 0$. By IVT, there's a root in $(0,1)$.

**Uniqueness (by contradiction using Rolle):** Suppose there were two roots $a < b$ with $f(a) = f(b) = 0$. Since $f$ is a polynomial (continuous and differentiable everywhere), Rolle's Theorem guarantees some $c\in(a,b)$ with $f'(c)=0$.

But $f'(x) = 3x^2 + 1 \geq 1 > 0$ for all $x$ — $f'$ is NEVER zero. Contradiction.

Therefore $f$ cannot have two roots. Combined with existence, $f$ has **exactly one** real root. $\square$

This proof technique — using Rolle's Theorem to show a function cannot have two roots — is extremely powerful and reusable.

---

## 2. The Mean Value Theorem (MVT)

Rolle's Theorem is a special case ($f(a)=f(b)$) of a more general and even more important result.

> **Theorem (MVT).** Let $f$ be a function such that:
> 1. $f$ is continuous on $[a,b]$
> 2. $f$ is differentiable on $(a,b)$
>
> Then there exists at least one $c \in (a,b)$ such that:
> $$f'(c) = \frac{f(b)-f(a)}{b-a}$$

**Geometric meaning:** The slope of the secant line from $(a,f(a))$ to $(b,f(b))$ equals the slope of the tangent line at some interior point $c$. In other words: **somewhere in the interval, the instantaneous rate of change equals the average rate of change.**

**Physical meaning:** If your average speed on a trip was 60 km/h, then at some instant during the trip your speedometer read exactly 60 km/h.

### Proof of MVT (using Rolle's Theorem)

Define an auxiliary function that measures the vertical gap between $f$ and the secant line:

$$g(x) = f(x) - \left[f(a) + \frac{f(b)-f(a)}{b-a}(x-a)\right]$$

$g$ is continuous on $[a,b]$ and differentiable on $(a,b)$ (since $f$ is, and we're subtracting a linear function).

Check: $g(a) = f(a) - f(a) = 0$. $g(b) = f(b) - [f(a) + (f(b)-f(a))] = f(b)-f(b) = 0$.

So $g(a) = g(b) = 0$. By Rolle's Theorem, there exists $c \in (a,b)$ with $g'(c) = 0$.

$$g'(x) = f'(x) - \frac{f(b)-f(a)}{b-a}$$

$$g'(c) = 0 \implies f'(c) = \frac{f(b)-f(a)}{b-a} \quad \square$$

**This proof is a template you should understand deeply:** the MVT is Rolle's Theorem applied to the "tilted" function $g$ that subtracts out the secant line, converting the general case back to the equal-endpoints case.

### Example 3

Verify the MVT for $f(x) = x^3 - x$ on $[0, 2]$ and find the value(s) of $c$.

$f$ is a polynomial: continuous and differentiable everywhere. ✓

$$\frac{f(2)-f(0)}{2-0} = \frac{(8-2)-0}{2} = \frac{6}{2} = 3$$

Find $c$: $f'(x) = 3x^2 - 1 = 3 \implies x^2 = \dfrac{4}{3} \implies x = \pm\dfrac{2}{\sqrt{3}}$

Only $c = \dfrac{2}{\sqrt{3}} \approx 1.155 \in (0,2)$ is valid.

---

## 3. Consequences of the MVT — The Foundation of Curve Sketching

The MVT is not just a curious existence theorem — it is the rigorous foundation for facts you may have used intuitively for years.

### Corollary 1 — Zero derivative implies constant function

> If $f'(x) = 0$ for all $x$ in an interval $I$, then $f$ is constant on $I$.

**Proof:** Take any $x_1 < x_2$ in $I$. By MVT applied to $[x_1, x_2]$: $f'(c) = \dfrac{f(x_2)-f(x_1)}{x_2-x_1}$ for some $c$. Since $f'(c) = 0$, we get $f(x_2) = f(x_1)$. Since this holds for any two points, $f$ is constant. $\square$

### Corollary 2 — Functions with equal derivatives differ by a constant

> If $f'(x) = g'(x)$ for all $x$ in an interval $I$, then $f(x) - g(x) = C$ for some constant $C$.

**Proof:** Let $h(x) = f(x)-g(x)$. Then $h'(x) = f'(x)-g'(x) = 0$ for all $x\in I$. By Corollary 1, $h$ is constant. $\square$

**This corollary is the theoretical foundation of integration!** It tells us that if you know one antiderivative of a function, you know ALL of them (up to a constant) — this is precisely why we write $\int f(x)\,dx = F(x) + C$ starting in Week 8.

### Corollary 3 — Sign of derivative determines monotonicity

> If $f'(x) > 0$ for all $x \in (a,b)$, then $f$ is increasing on $(a,b)$.
> If $f'(x) < 0$ for all $x \in (a,b)$, then $f$ is decreasing on $(a,b)$.

**Proof (increasing case):** Take $x_1 < x_2$ in $(a,b)$. By MVT on $[x_1,x_2]$: $f(x_2)-f(x_1) = f'(c)(x_2-x_1)$ for some $c$. Since $f'(c) > 0$ and $x_2 - x_1 > 0$, we get $f(x_2) - f(x_1) > 0$, i.e., $f(x_2) > f(x_1)$. $\square$

This corollary is the theoretical justification for the **Increasing/Decreasing Test** we use constantly in curve sketching (Week 7) — and it was NOT obvious before now. It required the MVT to prove rigorously.

---

## 4. CS Connection — MVT and Numerical Analysis

**Error bounds in Taylor approximation:** The MVT is the direct ancestor of Taylor's theorem with remainder (Week 12), which gives precise error bounds for polynomial approximations of functions — essential for understanding floating-point computation error and numerical algorithm accuracy.

**Lipschitz continuity:** A function satisfies a Lipschitz condition $|f(x)-f(y)| \leq L|x-y|$ if $|f'(x)| \leq L$ everywhere — a direct MVT consequence. Lipschitz constants bound how much output can change for a given input change, which is central to the analysis of gradient descent convergence rates in optimization and machine learning.

**Monotonic function verification:** Corollary 3 is literally how we verify that a sorting comparator or a monotonic transformation function behaves correctly — if the derivative (or discrete difference) never changes sign, the function is guaranteed monotonic.

---

## Lecture 2 Exercises

1. Verify Rolle's Theorem applies and find all values of $c$:
   - (a) $f(x) = x^2 - 4x + 3$ on $[1,3]$
   - (b) $f(x) = \sin x$ on $[0, \pi]$
   - (c) $f(x) = x^{2/3} - 1$ on $[-1,1]$ — does Rolle's theorem apply? Why or why not?

2. Verify the MVT applies and find all values of $c$:
   - (a) $f(x) = \dfrac{1}{x}$ on $[1,3]$
   - (b) $f(x) = \sqrt{x}$ on $[0,4]$ — check hypotheses carefully at $x=0$

3. **(Root counting via Rolle)** Show that $f(x) = 2x + \cos x$ has exactly one real root.

4. **(Application)** A police officer clocks a car entering a 5 km tunnel at 100 km/h and the same car exiting the tunnel 2 minutes later. What is the minimum speed (in km/h) the car must have reached inside the tunnel? Use the MVT to justify your reasoning rigorously.

5. **(Proof)** Use the MVT to prove: for $x > 0$, $\sin x < x$.
   *(Hint: apply MVT to $f(t) = \sin t$ on $[0, x]$.)*

6. **(Challenge)** Prove that if $f$ is differentiable on $\mathbb{R}$ and $f'(x) \neq 0$ for all $x$, then $f$ is one-to-one (injective). *(Hint: use Rolle's Theorem by contradiction.)*

---


### Answers

**1.** Rolle needs continuity on $[a,b]$, differentiability on $(a,b)$, **and** $f(a)=f(b)$.

**(a)** $f(1)=f(3)=0$ ✓, polynomial ✓. $f'=2x-4=0 \Rightarrow \boxed{c=2}$
**(b)** $\sin0=\sin\pi=0$ ✓. $\cos c=0 \Rightarrow \boxed{c=\pi/2}$
**(c)** $f(-1)=f(1)=0$ ✓ and $f$ is continuous — **but $f'=\tfrac23x^{-1/3}$ does not exist at
$x=0$**, which lies in $(-1,1)$. **Rolle does not apply.** And indeed $f'$ is never zero on the
interval, so the conclusion genuinely fails: the hypothesis is not a technicality.

**2.** MVT needs continuity on $[a,b]$ and differentiability on the **open** $(a,b)$.

**(a)** Average slope $=\dfrac{1/3-1}{2}=-\tfrac13$. Setting $-\tfrac1{c^2}=-\tfrac13$ gives
$\boxed{c=\sqrt3\approx1.732}$, which lies in $(1,3)$ ✓
**(b)** Average slope $=\dfrac{2-0}{4}=\tfrac12$. Setting $\dfrac{1}{2\sqrt c}=\tfrac12$ gives
$\boxed{c=1}$.

Note $\sqrt x$ is **not differentiable at $x=0$** — but the MVT only requires differentiability on
the *open* interval $(0,4)$, and continuity on the closed one. Both hold, so the theorem applies.
The open/closed distinction in the hypotheses is doing real work here.

**3.** $f(x)=2x+\cos x$. **Existence:** $f(-1)=-2+\cos(-1)\approx-1.46<0$ and
$f(0)=1>0$, so the IVT gives a root.

**Uniqueness:** $f'(x)=2-\sin x\geq1>0$ for all $x$, so $f$ is strictly increasing and cannot take
the same value twice. (Equivalently: two roots would force $f'=0$ somewhere between them by Rolle,
contradicting $f'\geq1$.) Hence **exactly one** real root. $\blacksquare$

**IVT gives existence, Rolle gives uniqueness** — the pairing is the technique.

**4.** Average speed $=\dfrac{5\text{ km}}{2\text{ min}}=\dfrac{5}{1/30}=\boxed{150\ \text{km/h}}$.

The position function is continuous and differentiable, so the MVT guarantees an instant at which
the *instantaneous* speed equalled the average — **at least 150 km/h**. The entry reading of
100 km/h is a distractor: it does not matter, because the MVT conclusion depends only on the
endpoints.

This is the mathematical basis of average-speed enforcement, and the argument is airtight in a way
a single radar reading is not.

**5.** Apply the MVT to $f(t)=\sin t$ on $[0,x]$ for $x>0$: there is $c\in(0,x)$ with
$$\frac{\sin x-\sin0}{x-0}=\cos c \quad\Longrightarrow\quad \sin x = x\cos c$$
Since $c>0$, $\cos c<1$, so $\sin x=x\cos c<x$. $\blacksquare$

(For $x\geq\pi/2$ the result is immediate since $\sin x\leq1<\pi/2\leq x$; the MVT argument covers
the delicate small-$x$ case where both sides are close.)

**6.** Suppose $f$ is **not** injective: then $f(a)=f(b)$ for some $a<b$. Since $f$ is
differentiable on $\mathbb{R}$, it is continuous on $[a,b]$ and differentiable on $(a,b)$, so
**Rolle's Theorem** gives some $c\in(a,b)$ with $f'(c)=0$ — contradicting $f'(x)\neq0$ everywhere.

Hence $f$ is injective. $\blacksquare$

A stronger conclusion follows: since $f'$ is a derivative it has the intermediate value property
(Darboux's theorem), so $f'\neq0$ everywhere means $f'$ has **constant sign** — $f$ is strictly
monotonic, not merely injective.

*Next: Wednesday — L'Hôpital's Rule*
