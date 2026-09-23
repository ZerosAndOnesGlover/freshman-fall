# MATH 142 · Calculus II
## Problem Set 12
### Topic: Course-Wide Self-Diagnostic — **UNGRADED**
**Released:** Friday 16 April 2027, 12:00 · Week 12 (after Lecture 3) | **Due:** never — **answers are at the end**

---

> ## ⚠ How to use this
>
> **This set is not collected and carries no marks.** It is a diagnostic: **one problem per week of
> the course**, chosen so that missing it tells you exactly which week to revise.
>
> **Do all thirteen with the answers covered**, in one sitting, without notes. Then check.
> **Then revise only the weeks you missed.** That list is the whole output of this exercise.
>
> **Do not read the answers first.** A problem you have just read the answer to teaches you nothing
> about what you know.

**Time yourself: 90 minutes for all thirteen.** If a problem takes more than seven minutes, stop, mark it, and move on — that is a miss, and the timing is diagnostic too.

---

## The Diagnostic

**Q0 · Week 0 — Foundations.**
$$\frac{d}{dx}\int_0^{x^2}\sin(t^3)\,dt = ?\qquad\text{and}\qquad \int_0^1\frac{x}{1+x^2}\,dx = ?$$

---

**Q1 · Week 1 — Parts and trig integrals.**
$$\int x^2e^x\,dx \qquad\text{and}\qquad \int_0^{\pi/2}\sin^4x\,dx$$

---

**Q2 · Week 2 — Partial fractions and trig substitution.**
$$\int\frac{5x-4}{(x-2)(x+1)}\,dx \qquad\text{and}\qquad \int\frac{dx}{x^2\sqrt{x^2+4}}$$

---

**Q3 · Week 3 — Improper integrals.**
$$\int_1^\infty\frac{dx}{x^2+x}$$
**Evaluate it, and say in one sentence how you would have known it converges without evaluating it.**

---

**Q4 · Week 4 — Applications.**
The region between $y=x$ and $y=x^2$ on $[0,1]$ is rotated about the **$y$-axis**. **Find the volume.**

---

**Q5 · Week 5 — Parametric and polar.**
**(a)** Arc length of $x=t^2,\ y=t^3$ for $0\le t\le1$.
**(b)** Area enclosed by $r=2\cos\theta$.

---

**Q6 · Week 6 — Sequences.**
**(a)** $\displaystyle\lim_{n\to\infty}\left(1+\frac3n\right)^{2n}$
**(b)** $a_{n+1}=\frac12\left(a_n+\frac{6}{a_n}\right)$ with $a_0=2$. **What is the limit, and why must it be the positive one?**

---

**Q7 · Week 7 — Series, first tests.**
$$\sum_{n=2}^{\infty}\frac{1}{n(\ln n)^2}$$
**Converge or diverge? Name the test and carry it out.**

---

**Q8 · Week 8 — Alternating and absolute convergence.**
$$\sum_{n=1}^{\infty}\frac{(-1)^n}{\sqrt n}$$
**Absolutely convergent, conditionally convergent, or divergent? Justify both halves of your answer.**

---

**Q9 · Week 9 — Power series.**
$$\sum_{n=1}^{\infty}\frac{(x-2)^n}{n\,3^n}$$
**Find the radius of convergence and the full interval of convergence, endpoints decided.**

---

**Q10 · Week 10 — Taylor series.**
**Use $P_6$ for $\cos x$ to estimate $\cos(0.5)$, and bound the error *before* comparing with a calculator.**

---

**Q11 · Week 11 — Differential equations.**
$$x^2\frac{dy}{dx}+2xy=\cos x,\qquad y(\pi)=0$$

---

**Q12 · Week 12 — Systems.**
For $x'=y,\ y'=-4x$, **show that $4x^2+y^2$ is constant along every solution**, and say what that implies about the trajectories.

---

---

# Answers

> **Stop here if you have not done all thirteen.**

---

**Q0.** $\dfrac{d}{dx}\displaystyle\int_0^{x^2}\sin(t^3)dt = \boxed{2x\sin(x^6)}$ — FTC **with the chain rule**; the factor $2x$ is the usual casualty.
$\displaystyle\int_0^1\frac{x}{1+x^2}dx = \boxed{\tfrac12\ln2}$ via $u=1+x^2$.

**Q1.** $\displaystyle\int x^2e^xdx = \boxed{(x^2-2x+2)e^x+C}$ — parts twice, or the tabular method.
$\displaystyle\int_0^{\pi/2}\sin^4x\,dx=\boxed{\dfrac{3\pi}{16}}$ — even power, so **half-angle**, not $u$-substitution.

**Q2.** $\dfrac{5x-4}{(x-2)(x+1)}=\dfrac{2}{x-2}+\dfrac{3}{x+1}$, so the integral is $\boxed{2\ln|x-2|+3\ln|x+1|+C}$.
$\displaystyle\int\frac{dx}{x^2\sqrt{x^2+4}}=\boxed{-\dfrac{\sqrt{x^2+4}}{4x}+C}$ — $x=2\tan\theta$. *(Verified by differentiating back.)*

**Q3.** $\dfrac{1}{x^2+x}=\dfrac1x-\dfrac1{x+1}$, giving $\left[\ln\frac{x}{x+1}\right]_1^\infty=\boxed{\ln 2}$.
**Without evaluating:** $0<\frac{1}{x^2+x}<\frac{1}{x^2}$ on $[1,\infty)$, and $\int_1^\infty x^{-2}dx$ converges — **direct comparison.**

**Q4.** **Shells:** $\displaystyle V=2\pi\int_0^1x(x-x^2)\,dx=\boxed{\dfrac{\pi}{6}}$.
*(Washers in $y$ also work and must give the same number — if yours does not, you have the radii the wrong way round, which was Week 4's most common error.)*

**Q5.** **(a)** $\displaystyle\int_0^1\sqrt{4t^2+9t^4}\,dt = \boxed{\dfrac{13\sqrt{13}-8}{27}} \approx 1.43971$.
**(b)** $r=2\cos\theta$ traces the **whole** circle as $\theta$ runs over $[-\pi/2,\pi/2]$; area $=\frac12\int_{-\pi/2}^{\pi/2}4\cos^2\theta\,d\theta=\boxed{\pi}$.
*(It is a circle of radius 1 — if you got $2\pi$ you integrated over $[0,2\pi]$ and traversed it twice.)*

**Q6.** **(a)** $\boxed{e^6}$.
**(b)** The limit satisfies $L=\frac12(L+6/L)$, i.e. $L^2=6$, so $L=\pm\sqrt6$. **Since $a_0=2>0$ and the recursion preserves positivity, $L=\boxed{\sqrt6}$.** *(Verified: the fixed points are exactly $\pm\sqrt6$.)*
**Naming the limit is not the answer — the existence argument is.**

**Q7.** **Converges**, by the **Integral Test** ($f(x)=\frac1{x(\ln x)^2}$ is positive, continuous and decreasing on $[2,\infty)$):
$$\int_2^\infty\frac{dx}{x(\ln x)^2} = \left[\frac{-1}{\ln x}\right]_2^\infty = \frac{1}{\ln2}\approx1.4427 <\infty$$
*(Verified.)* **Note that $\frac1{n\ln n}$ diverges** — the exponent 2 is doing all the work, and this pair is the standard trap.

**Q8.** **Conditionally convergent.**
*Converges:* $b_n=n^{-1/2}$ is positive, decreasing, and $\to0$ — **Alternating Series Test**.
*Not absolutely:* $\sum n^{-1/2}$ is a $p$-series with $p=\frac12\le1$, **divergent**.
*(Both halves are required. Verified numerically: the sum is $-0.604898643422$.)*

**Q9.** Ratio Test gives $\dfrac{|x-2|}{3}<1$, so $\boxed{R=3}$ and the open interval is $(-1,5)$.
**Endpoints:** $x=5$ gives $\sum\frac1n$ — **diverges**; $x=-1$ gives $\sum\frac{(-1)^n}{n}=-\ln2$ — **converges**.
$$\boxed{\text{Interval of convergence } [-1,5)}$$
**A radius without endpoint tests is half an answer.**

**Q10.** $P_6(x)=1-\frac{x^2}{2}+\frac{x^4}{24}-\frac{x^6}{720}$, so $P_6(0.5)=\boxed{0.877582465278}$.
**Bound first:** the series is alternating with decreasing terms at $x=\frac12$, so the error is at most the first omitted term,
$$\frac{(0.5)^8}{8!} = 9.68812\times10^{-8}$$
**Actual error: $9.66126\times10^{-8}$.** *(Verified.)* **The bound is within 0.3% of the truth** — that is what a good bound looks like.

**Q11.** The left side is already $(x^2y)'$, so $x^2y=\sin x+C$; $y(\pi)=0$ gives $C=0$ and
$$\boxed{y=\frac{\sin x}{x^2}}$$
*(Verified by `dsolve` and by substitution.)* **Spotting the product rule saves the integrating-factor computation entirely** — and if you did compute $\mu$, you got $\mu=x^2$ and the same answer.

**Q12.** $\dfrac{d}{dt}(4x^2+y^2)=8xx'+2yy'=8xy+2y(-4x)=0$. *(Verified.)*
**So every trajectory lies on a fixed ellipse $4x^2+y^2=C$** — the trajectories are **closed curves**, hence **every solution is periodic.** *(Indeed $x=\frac{C_1}{2}\sin2t+\frac{C_2}{2}\cos2t$, period $\pi$.)*

---

## What Your Misses Mean

| Missed | Revise | Where |
|---|---|---|
| **Q0** | FTC with the chain rule, $u$-substitution | Week 0 reference sheet |
| **Q1** | Parts, half-angle vs. $u$-sub for trig powers | Week 1 §2–3 |
| **Q2** | Partial-fraction setup, the trig-sub triangle | Week 2 reference sheet |
| **Q3** | Limit definition, comparison test | Week 3 §2, §4 |
| **Q4** | Shells vs. washers, **and the radii** | Week 4 PS 4 A4 |
| **Q5** | Parameter range, $\frac12\int r^2d\theta$ | Week 5 §3–4 |
| **Q6** | Existence *before* the fixed-point equation | Week 6 §4 |
| **Q7** | Integral Test hypotheses; $\frac1{n\ln n}$ vs $\frac1{n(\ln n)^2}$ | Week 7 §3 |
| **Q8** | Both halves of a conditional-convergence claim | Week 8 §2–3 |
| **Q9** | **Endpoint tests** | Week 9 §2 |
| **Q10** | Bounding *before* computing | Week 10 §4 |
| **Q11** | Standard form, product-rule recognition | Week 11 reference sheet |
| **Q12** | Conservation $\Rightarrow$ closed trajectories | Week 12 Lecture 1 |

---

> **If you missed four or fewer, you are in good shape and should revise those four.**
> **If you missed more, revise by week, not by problem** — the misses are clustered, and the cluster
> is what needs the time.
>
> **Lab 12 is the second half of this diagnostic**, taken under exam conditions, on longer problems.

---

*MATH 142 · Problem Set 12 · Ungraded*
