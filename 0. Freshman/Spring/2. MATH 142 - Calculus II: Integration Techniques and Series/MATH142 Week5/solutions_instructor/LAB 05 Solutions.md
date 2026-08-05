# MATH 142 · Calculus II
## Lab 05 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures produced by running the lab at 30-digit precision.

---

## Part A — The Cycloid (25 pts)

### A1 (8) — the half-angle collapse

$$\frac{dx}{dt}=a(1-\cos t),\qquad \frac{dy}{dt}=a\sin t$$

$$\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2 = a^2\big[(1-\cos t)^2+\sin^2t\big] = a^2\big[1-2\cos t+\cos^2t+\sin^2t\big] = a^2(2-2\cos t)$$

**The step:** $1-\cos t = 2\sin^2\frac t2$, hence

$$= 4a^2\sin^2\frac t2 \qquad\textbf{— a perfect square.}$$

*Verified symbolically: the CAS gives $a^2(2-2\cos t)$, and the difference from $4a^2\sin^2\frac t2$ is exactly 0.*

*Marking: 4 for reaching $a^2(2-2\cos t)$, **4 for the half-angle step.** This is the mechanism the whole lab is about.*

### A2 (9) — arc length

Speed $= 2a\left|\sin\frac t2\right| = 2a\sin\frac t2$ on $[0,2\pi]$ (where $\frac t2\in[0,\pi]$, so the sine is non-negative).

$$L = \int_0^{2\pi}2a\sin\frac t2\,dt = 2a\Big[-2\cos\tfrac t2\Big]_0^{2\pi} = 2a\big(2-(-2)\big) = \boxed{8a}$$

*Verified symbolically, and numerically for $a=1$: quadrature gives exactly $8.0$.*

*Marking: 3 for handling the absolute value with a stated reason, 4 for the integral, 2 for the verification. **The absolute value must be addressed** — even though it is harmless here, the astroid (Lecture 2, Example 6) shows what happens when it is not.*

### A3 (8) — area

$$A = \int_0^{2\pi}y\,\frac{dx}{dt}\,dt = a^2\int_0^{2\pi}(1-\cos t)^2dt = a^2\big(2\pi-0+\pi\big) = \boxed{3\pi a^2}$$

*Verified symbolically; numerically $3\pi = 9.42477796077$ for $a=1$.*

**Ratio to the rolling circle** ($\pi a^2$): **exactly 3.**

*Marking: 5 for the area, 3 for the ratio and comment. **$\int_0^{2\pi}\cos^2 = \pi$** is the usual slip.*

---

## Part B — The Ellipse Has No Closed Form (20 pts)

### B1 (8)

$$P = \int_0^{2\pi}\sqrt{a^2\sin^2t+b^2\cos^2t}\,dt$$

`sympy` returns it **unevaluated** — literally `Integral(sqrt(a**2*sin(t)**2 + b**2*cos(t)**2), (t, 0, 2*pi))`.

**What that tells you:** the CAS's integration algorithms — which include a decision procedure for elementary antiderivatives — **failed to find one, and returning the input unevaluated is how it reports that.** It is not a bug or a timeout.

*Marking: 4 for the integral, 4 for the interpretation. **"The computer couldn't do it" earns 1** — the point is that the CAS is reporting a theorem, not admitting defeat.*

### B2 (6)

For $a=2$, $b=1$:

| method | value |
|---|---|
| numerical quadrature | $9.68844822054768$ |
| $4a\,E(e^2)$ via `mp.ellipe` | $9.68844822054768$ |

**Agreement to all 15 figures.**

**What `ellipe` is:** the **complete elliptic integral of the second kind** — which is *defined* as this integral. Naming it does not evaluate it, exactly as `erf` in Lab 0 was a name for $\int e^{-x^2}$. **The library computes it by series or by the arithmetic–geometric mean, not by an antiderivative.**

*Marking: 3 for the two agreeing values, **3 for recognising `ellipe` as a name rather than a solution.** The parallel with `erf` should be drawn; award full marks if it is.*

### B3 (6)

With $a=b$:

$$\sqrt{a^2\sin^2t+a^2\cos^2t} = \sqrt{a^2} = a$$

$$P = \int_0^{2\pi}a\,dt = \boxed{2\pi a}$$ ✓

**Why only this case:** in general the integrand is $\sqrt{b^2+(a^2-b^2)\sin^2t}$ — a genuine quadratic in $\sin t$. **When $a=b$ the coefficient $a^2-b^2$ vanishes**, the expression becomes constant, and the root disappears. For any other pair it does not.

*Marking: 3 for the evaluation, 3 for the explanation. **The explanation must identify the vanishing coefficient**, not merely say "the circle is easier".*

---

## Part C — What People Actually Use (30 pts)

### C1 (12) — the error table

$a=1$; relative errors:

| $b/a$ | exact $P$ | $P_1=\pi(a+b)$ | $P_2=2\pi\sqrt{\frac{a^2+b^2}{2}}$ | $P_3$ (Ramanujan) |
|---|---|---|---|---|
| $1.0$ | 6.283185307 | 0 | 0 | 0 |
| $0.8$ | 5.672333578 | $3.079\times10^{-3}$ | $3.056\times10^{-3}$ | $\mathbf{3.692\times10^{-9}}$ |
| $0.5$ | 4.844224110 | $2.721\times10^{-2}$ | $2.541\times10^{-2}$ | $\mathbf{2.800\times10^{-6}}$ |
| $0.2$ | 4.202008908 | $1.028\times10^{-1}$ | $7.826\times10^{-2}$ | $2.113\times10^{-4}$ |
| $0.1$ | 4.063974180 | $1.497\times10^{-1}$ | $9.869\times10^{-2}$ | $8.419\times10^{-4}$ |
| $0.01$ | 4.001098330 | $2.070\times10^{-1}$ | $1.105\times10^{-1}$ | $3.420\times10^{-3}$ |

*Marking: 12 for a complete table matching these figures.*

*(Note the exact perimeter tends to $4a=4$ as $b\to0$: the ellipse degenerates to a segment of length $2a$ traversed **twice**. Students who spot this deserve a comment.)*

### C2 (8)

**All three are exact at $b=1$** because the ellipse is then a circle of radius 1, whose perimeter is $2\pi$ — and each formula reduces to $2\pi$ when $a=b$. *(Check: $P_1=2\pi$, $P_2=2\pi\sqrt{1}=2\pi$, $P_3=\pi[6-\sqrt{16}]=2\pi$ ✓.)*

**Degradation:** $P_1$ and $P_2$ both deteriorate quickly and are comparable at mild eccentricity, but $P_2$ is roughly twice as good in the flat limit ($11\%$ vs $21\%$). **$P_3$ is better than both everywhere**, by six orders of magnitude at $b/a=0.8$ and still by a factor of 60 at $b/a=0.01$.

**Best at $b/a=0.8$: $P_3$** (by a factor of $10^6$). **Best at $b/a=0.01$: $P_3$** again.

*Marking: 4 for the $a=b$ reduction shown, 4 for the comparison. **The reduction should be verified, not asserted.***

### C3 (10)

**(a)** At $b/a=0.8$: error $3.7\times10^{-9}$ — about **8–9 correct significant figures.**
At $b/a=0.5$: error $2.8\times10^{-6}$ — about **5–6 correct significant figures.**

**(b)** Tolerance $10^{-5}$:

- **$P_3$** stays within $10^{-5}$ down to roughly $b/a\approx0.35$–$0.4$ (it is $2.1\times10^{-4}$ at $b/a=0.2$, already outside). **Good enough for essentially any ellipse that is not extremely flattened.**
- **$P_1$** is $3\times10^{-3}$ even at $b/a=0.8$ — **never good enough**, at any eccentricity below a circle.

**(c)** "Has no closed form" is a statement about **exact symbolic representation**, and it is permanent and absolute. **It says nothing about approximability.** A two-line formula reaches nine significant figures for mild ellipses, which exceeds any engineering requirement and most measurement precision.

**Practically, the non-existence of a closed form is almost irrelevant here.** It matters for *proof* — you cannot derive exact identities from $P_3$ — but not for *computation*.

*Marking: 3 + 4 + 3. **(c) must separate symbolic representability from numerical approximability.** This is the same distinction as Week 0's existence-vs-expressibility, and students who make the link should be told so.*

---

## Part D — Reflection (25 pts)

### D1 (10)

**(a)** For $r=1+\cos\theta$, $r'=-\sin\theta$:

$$r^2+(r')^2 = (1+\cos\theta)^2+\sin^2\theta = 1+2\cos\theta+\cos^2\theta+\sin^2\theta = 2+2\cos\theta$$

**Half-angle:** $2+2\cos\theta = 4\cos^2\frac\theta2$, so the integrand is $2\left|\cos\frac\theta2\right|$ — **the same mechanism as the cycloid.**

$$L = \int_0^{2\pi}2\left|\cos\tfrac\theta2\right|d\theta \overset{u=\theta/2}{=} 4\int_0^\pi|\cos u|\,du = 4\cdot2 = \boxed{8}$$

*Verified: the identity holds exactly; numerical quadrature split at $\theta=\pi$ gives exactly $8.0$. **A CAS asked for this directly returns it unevaluated** — the absolute value defeats it, exactly as in Week 0 with $\int_0^3|t^2-4|dt$.*

**(b)** The ellipse's integrand is

$$\sqrt{a^2\sin^2t+b^2\cos^2t} = \sqrt{b^2+(a^2-b^2)\sin^2t}$$

**A quadratic in $\sin t$ with two independent coefficients.** The cycloid and cardioid cases are one-parameter expressions ($2\pm2\cos$) that a **single half-angle identity** converts into a square. Here there is no identity relating $b^2$ and $a^2-b^2$ — **the expression is a square only in the degenerate case $a=b$.**

*Marking: 6 + 4. **(a) must handle the absolute value**; (b) must identify the two independent coefficients as the obstruction.*

### D2 (8)

**Lab 5 entry: numerics is essential, and excellent.** There is no exact answer to compute, so quadrature (or `ellipe`) *is* the answer — and a two-line closed-form approximation reaches nine figures.

**It most resembles Lab 0**, where numerics succeeded on an integral with no elementary antiderivative. **The difference from Lab 3** is decisive: there, numerics could not answer the question at all; here it answers it completely.

*Marking: 8. Accept any well-argued entry. **The key observation is that this is a value question, not an existence question** — and value questions are where computation wins.*

### D3 (7)

**In common with the labs:** Galileo's weighing was an **empirical measurement of a mathematical quantity** — physical apparatus standing in for computation, producing a number close to the truth.

**What it lacks:** a **proof**. Galileo got "about 3" and could not establish that the ratio was *exactly* 3 rather than $2.98$ or $\pi-0.14$. Roberval's 1634 argument gave the exact value $3\pi a^2$ and with it certainty.

**This is exactly the Lab 2 distinction**: measurement gives evidence, derivation gives proof. Galileo's scales were a 17th-century numerical method, with the same strength and the same limitation.

*Marking: 7. **The answer must name the missing element as proof/exactness.** A student who links it to Lab 2's $\frac{22}{7}>\pi$ argument has understood the whole arc and should be commended.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 25 |
| B | 20 |
| C | 30 |
| D | 25 |
| **Total** | **100** |

---

## Checkoff Checklist

1. **A1 shows the half-angle step explicitly**
2. A2 addresses the absolute value
3. A3 gets the ratio 3
4. **B1 interprets "unevaluated" as a report, not a failure**
5. B2 identifies `ellipe` as a name, like `erf`
6. C1 table matches to the figures shown
7. **C3(c) separates representability from approximability**
8. D1(a) handles $\left|\cos\frac\theta2\right|$
9. **D3 names proof as what Galileo lacked**

---

## Note for the Debrief

> **Two curves, described in the same amount of ink.** The cycloid — no Cartesian equation, unknown
> before the 1600s — has arc length exactly $8a$, four times the diameter of the wheel. The ellipse —
> a conic section, area $\pi ab$, known since Apollonius — has a perimeter no formula will ever
> express.
>
> **The difference is one line of trigonometry.** $2-2\cos t$ is a perfect square; $b^2+(a^2-b^2)\sin^2t$
> is not. That is the entire explanation, and nothing about the curves' appearance predicts it.

Then the practical coda:

> And yet Ramanujan's two-line formula gives the ellipse's perimeter to **nine significant figures**
> for a mild ellipse — a formula he published in 1914 with the note that he had obtained it
> "empirically", and never explained.
>
> **"No closed form" is a permanent fact about symbols. It is very nearly irrelevant to computation.**
> Knowing which of those two you care about, on any given day, is most of applied mathematics.

---

*MATH 142 · Week 5 · Lab 05 Solutions · Instructor Only*
