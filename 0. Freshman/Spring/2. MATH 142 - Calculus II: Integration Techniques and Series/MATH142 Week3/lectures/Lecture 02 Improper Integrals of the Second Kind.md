# MATH 142 · Calculus II
## Week 3 · Lecture 2 (Tuesday)
### Improper Integrals of the Second Kind — and Singularities That Hide

**Date:** Tuesday 2 February 2027 · 11:00–11:50 · Week 3

---

**Reading:** Stewart §7.8 (continued) | Apostol Ch. 10 §10.8

---

## 1. The Other Way an Integral Can Be Improper

Yesterday the *interval* was infinite. Today the *integrand* is.

$$\int_0^1\frac{dx}{\sqrt x}$$

The interval $[0,1]$ is perfectly ordinary. But $\frac{1}{\sqrt x}\to\infty$ as $x\to0^+$, so the function is **unbounded** — and Week 0's definition required $f$ to be bounded for the Riemann sums to make sense. **Again the symbol has no meaning until we give it one**, and again the answer is a limit:

$$\boxed{\int_a^b f(x)\,dx := \lim_{t\to a^+}\int_t^b f(x)\,dx} \qquad\text{(singularity at the left endpoint)}$$

$$\boxed{\int_a^b f(x)\,dx := \lim_{t\to b^-}\int_a^t f(x)\,dx} \qquad\text{(singularity at the right endpoint)}$$

**Same machinery as yesterday:** step back from the bad point, integrate normally, take a limit.

---

## 2. The Basic Examples

### Example 1 — convergent

$$\int_0^1\frac{dx}{\sqrt x} = \lim_{t\to0^+}\int_t^1 x^{-1/2}dx = \lim_{t\to0^+}\Big[2\sqrt x\Big]_t^1 = \lim_{t\to0^+}\big(2-2\sqrt t\big) = \boxed{2}$$

*Verified symbolically.*

**An infinitely tall region with area 2.** The spike at $x=0$ is thin enough that it contributes nothing in the limit.

### Example 2 — divergent

$$\int_0^1\frac{dx}{x} = \lim_{t\to0^+}\Big[\ln x\Big]_t^1 = \lim_{t\to0^+}\big(-\ln t\big) = \boxed{\infty}$$

*Verified symbolically.*

**The same function, $1/x$, that diverged yesterday at infinity — diverges here at zero too.** It sits exactly on the boundary at both ends, which is what makes it the reference case for everything.

---

## 3. The $p$-Test at a Singularity

$$\boxed{\int_0^1\frac{dx}{x^p} = \begin{cases}\dfrac{1}{1-p} & p<1\quad\text{(converges)}\\[8pt]\infty & p\ge1\quad\text{(diverges)}\end{cases}}$$

*Verified: $p=\tfrac12$ gives 2; $p=0.9$ gives 10; $p=1$, $p=1.1$, $p=2$ all diverge.*

### **The inequality points the opposite way to yesterday's.** This is the single most confused point of the week.

| | Converges when | Because |
|---|---|---|
| $\displaystyle\int_1^\infty\frac{dx}{x^p}$ | $p>1$ | near $\infty$ you need the function to **shrink fast** |
| $\displaystyle\int_0^1\frac{dx}{x^p}$ | $p<1$ | near 0 you need the function to **blow up slowly** |

**A large $p$ helps at infinity and hurts at zero.** Consider $p=2$: $\frac{1}{x^2}$ decays fast at infinity (converges) but explodes violently at 0 (diverges). And $p=\tfrac12$: $\frac{1}{\sqrt x}$ decays too slowly at infinity (diverges) but blows up gently at 0 (converges).

> **Do not memorise two inequalities. Memorise the reason**, and the direction follows every time.
> In both cases **$p=1$ diverges** — $1/x$ is the boundary and is on the wrong side of it at both ends.

### A consequence worth noticing

$$\int_0^\infty\frac{dx}{x^p} \quad\textbf{diverges for every } p$$

because it needs $p>1$ for the tail and $p<1$ for the spike, and no $p$ does both. **Splitting at 1 and testing each half separately is the only correct approach**, and here one half always fails.

---

## 4. More Examples

### Example 3 — an unbounded integrand that converges

$$\int_0^1\ln x\,dx = \lim_{t\to0^+}\Big[x\ln x - x\Big]_t^1 = \lim_{t\to0^+}\big(-1 - t\ln t + t\big) = \boxed{-1}$$

*Verified symbolically.*

**The step $t\ln t\to0$ is the content** — another indeterminate form ($0\cdot\infty$), resolved by L'Hôpital. $\ln x\to-\infty$ at the origin, yet the area is finite and equals $-1$ exactly.

*(The antiderivative $x\ln x - x$ is from Week 1, Lecture 1 — the $dv=dx$ trick.)*

### Example 4 — a singularity at the right endpoint

$$\int_0^9\frac{dx}{\sqrt{9-x}} = \lim_{t\to9^-}\Big[-2\sqrt{9-x}\Big]_0^t = \lim_{t\to9^-}\big(6 - 2\sqrt{9-t}\big) = \boxed{6}$$

*Verified symbolically.*

### Example 5 — an endpoint singularity you may not have noticed

$$\int_0^1\frac{dx}{\sqrt{1-x^2}} = \Big[\arcsin x\Big]_0^1 = \frac\pi2$$

*Verified symbolically.*

**This is improper** — the integrand blows up as $x\to1^-$ — and you have been writing it since Week 0 without comment. It converges, so the casual evaluation gave the right answer. **But it was luck, not method**, and the next example shows what luck looks like when it runs out.

---

## 5. Singularities That Hide — The Trap

### The classic

$$\int_{-1}^{1}\frac{dx}{x^2}$$

Applied thoughtlessly, the Fundamental Theorem gives

$$\left[-\frac1x\right]_{-1}^{1} = (-1) - (1) = -2$$

**This answer is absurd**, and you do not need any theory to see it: the integrand $\frac{1}{x^2}$ is **strictly positive** everywhere it is defined, so its integral cannot possibly be negative.

**What went wrong:** the integrand is unbounded at $x=0$, which is *inside* the interval. FTC Part 2 requires $f$ to be continuous on $[a,b]$, and this $f$ is not even defined at 0. The theorem's hypotheses failed, so its conclusion means nothing.

**Correctly:** split at the singularity and test each side.

$$\int_{-1}^{1}\frac{dx}{x^2} = \int_{-1}^{0}\frac{dx}{x^2}+\int_0^1\frac{dx}{x^2}$$

Each half is $\int_0^1 x^{-p}$ with $p=2\ge1$, so **each half diverges**, and the whole thing diverges.

*Verified symbolically: the CAS returns $\infty$.*

> **The absurd $-2$ is a gift.** The sign was visibly impossible, so the error announced itself. **The
> dangerous cases are the ones where the wrong answer looks plausible** — and there is no way to spot
> those except by checking the integrand for singularities *before* integrating.

### The procedure that prevents it

> **Before evaluating any definite integral, ask: is the integrand defined and bounded on the whole
> closed interval?**
>
> Check **both endpoints** and **every interior point** where a denominator vanishes, a logarithm's
> argument hits zero, or a fractional power has a negative base.
>
> If any point fails, **split there** and treat each piece as improper.

### An interior singularity that converges

$$\int_0^3\frac{dx}{(x-1)^{2/3}}$$

The integrand blows up at $x=1$, inside $[0,3]$. Split:

$$\int_0^1(1-x)^{-2/3}dx + \int_1^3(x-1)^{-2/3}dx$$

*(using the real cube root, so $(x-1)^{2/3} = |x-1|^{2/3}$)*

Each is a $p$-test at a singularity with $p=\tfrac23<1$, so **both converge**:

$$= \Big[-3(1-x)^{1/3}\Big]_0^1 + \Big[3(x-1)^{1/3}\Big]_1^3 = 3 + 3\sqrt[3]{2}$$

$$\boxed{= 3+3\sqrt[3]2 \approx 6.7798}$$

*Verified: symbolic evaluation of the two halves gives $3$ and $3\cdot2^{1/3}$; numerical quadrature over $[0,1,3]$ agrees to 11 significant figures.*

**Note the answer is positive and larger than either half** — as it must be. Splitting was necessary even though the result converged.

> **A CAS warning, again.** Asked for $\int_0^3(x-1)^{-2/3}dx$ directly, a computer algebra system
> returns $3\sqrt[3]2 - 3\sqrt[3]{-1}$ — and it takes $\sqrt[3]{-1}$ to be the *principal* complex
> root $e^{i\pi/3}$, not $-1$. The result is complex and wrong for our purposes. **Splitting by hand
> and using real cube roots gives the right answer.** Third week running: the machine is a check, not
> an oracle.

---

## 6. Both Kinds at Once

An integral can be improper for both reasons:

$$\int_0^\infty\frac{dx}{\sqrt x\,(1+x)}$$

— unbounded integrand at $0$, unbounded interval at $\infty$. **Split at any convenient interior point** and require *both* pieces to converge:

$$= \int_0^1\frac{dx}{\sqrt x(1+x)} + \int_1^\infty\frac{dx}{\sqrt x(1+x)}$$

Near 0 the integrand behaves like $x^{-1/2}$ ($p=\tfrac12<1$ ✓ converges); near $\infty$ it behaves like $x^{-3/2}$ ($p=\tfrac32>1$ ✓ converges). **Both pass, so the integral converges.**

*(That "behaves like" reasoning is not yet rigorous — making it rigorous is tomorrow's lecture.)*

---

## 7. What To Take From This Lecture

1. **An unbounded integrand makes an integral improper**, even on a bounded interval.
2. **Step back from the bad point and take a limit.** Same method as Type I.
3. **$\int_0^1 x^{-p}$ converges $\iff p<1$** — the *opposite* direction from the tail test. Learn the reason, not the inequality.
4. **$p=1$ diverges at both ends.**
5. **Check for singularities before integrating**, including interior ones. FTC Part 2 requires continuity.
6. **Split at every singularity**, and require every piece to converge.

---

*Next: Wednesday — Comparison Tests, and Answering Without Evaluating*
