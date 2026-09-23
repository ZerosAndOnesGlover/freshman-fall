# MATH 142 · Calculus II
## Quiz 00 — Diagnostic
### Week 0 · Ungraded · Answer key included

**Date:** Monday 18 January 2027 · 11:00–11:25, before Lecture 1 · Week 0

---

**Time:** 25 minutes, closed book, no calculator
**Weight:** **none.** This quiz does not enter the gradebook.

---

## What This Is For

This is the checklist from the Week 0 Overview, turned into questions. Its purpose is to tell you **now** what you would otherwise find out at Midterm 1.

**Take it under real conditions** — 25 minutes, nothing open, no calculator — then mark it against the key. A score is meaningless; *which* questions you missed is not.

> **Do not read the answer key first.** A diagnostic you have already seen the answers to diagnoses nothing.

---

## Questions

**Q1.** State the definition of $\displaystyle\int_a^b f(x)\,dx$ as a limit of Riemann sums. Define every symbol you use.

**Q2.** Evaluate $\displaystyle\int_0^1 (3x^2-2x)\,dx$.

**Q3.** Find $\displaystyle\frac{d}{dx}\int_0^x \sin(t^2)\,dt$.

**Q4.** Find $\displaystyle\frac{d}{dx}\int_0^{x^2}\sin(t^2)\,dt$.

**Q5.** Find $\displaystyle\int \frac{x}{1+x^2}\,dx$.

**Q6.** Evaluate $\displaystyle\int_0^{\pi/2}\sin x\cos x\,dx$.

**Q7.** Evaluate $\displaystyle\int_{-3}^{3}\frac{x^7}{1+x^4}\,dx$.

**Q8.** Find the area of the region between $y=\sqrt x$ and $y=x^2$ on $[0,1]$.

**Q9.** Find the average value of $f(x)=x^3$ on $[0,2]$.

**Q10.** A particle has velocity $v(t)=2t-6$ m/s for $0\le t\le5$. Find (a) the displacement and (b) the total distance travelled.

---
---

# ANSWER KEY

**Stop here if you have not done the quiz.**

---

**Q1.** Partition $[a,b]$ into $n$ subintervals of width $\Delta x = \frac{b-a}{n}$, with sample point $x_i^*$ in the $i$-th subinterval. Then

$$\int_a^b f(x)\,dx = \lim_{n\to\infty}\sum_{i=1}^n f(x_i^*)\,\Delta x$$

provided the limit exists and is independent of the choice of the $x_i^*$.

*Full credit requires: the partition, $\Delta x$, the sample points, the sum, and the limit. **"$F(b)-F(a)$" is not the definition** — it is FTC Part 2.*

**Q2.** $\big[x^3 - x^2\big]_0^1 = (1-1) - 0 = \boxed{0}$

*The answer being zero is not a mistake. The signed area cancels.*

**Q3.** $\boxed{\sin(x^2)}$ — FTC Part 1, directly.

**Q4.** $\boxed{2x\sin(x^4)}$ — FTC Part 1 **plus the chain rule**, since the upper limit is $x^2$:
$\frac{d}{dx}F(x^2) = F'(x^2)\cdot 2x = \sin\big((x^2)^2\big)\cdot 2x$.

*If you wrote $\sin(x^4)$ without the $2x$, that is the single most common error on this topic. Verified numerically at $x=0.9$ and $x=1.5$ to 14 significant figures.*

**Q5.** $u=1+x^2$, $du=2x\,dx$: $\;\frac12\int\frac{du}{u} = \boxed{\tfrac12\ln(1+x^2)+C}$

*No absolute value is needed: $1+x^2>0$ always. Writing $\ln|1+x^2|$ is not wrong, just redundant.*

**Q6.** $u=\sin x$, $du=\cos x\,dx$; limits $0\to1$: $\;\int_0^1 u\,du = \boxed{\tfrac12}$

*Equally valid: $\sin x\cos x = \tfrac12\sin 2x$, giving $\big[-\tfrac14\cos 2x\big]_0^{\pi/2} = \tfrac14+\tfrac14=\tfrac12$.*

**Q7.** $\boxed{0}$ — the integrand is **odd** ($x^7$ odd, $1+x^4$ even) and the interval is symmetric about $0$.

*Anyone who tried to find an antiderivative here has lost the marks to time, not to error. **Check symmetry first.***

**Q8.** On $(0,1)$, $\sqrt x > x^2$. So

$$A = \int_0^1\big(\sqrt x - x^2\big)dx = \left[\tfrac23 x^{3/2} - \tfrac13 x^3\right]_0^1 = \tfrac23-\tfrac13 = \boxed{\tfrac13}$$

**Q9.** $\displaystyle f_{\text{avg}} = \frac{1}{2}\int_0^2 x^3\,dx = \frac12\left[\frac{x^4}{4}\right]_0^2 = \frac12\cdot 4 = \boxed{2}$

**Q10.** $v(t)=2t-6$ is zero at $t=3$, negative on $[0,3)$, positive on $(3,5]$.

- **(a) Displacement:** $\displaystyle\int_0^5(2t-6)\,dt = \big[t^2-6t\big]_0^5 = 25-30 = \boxed{-5\text{ m}}$
- **(b) Distance:** split at $t=3$:
$$\int_0^3(6-2t)\,dt + \int_3^5(2t-6)\,dt = 9 + 4 = \boxed{13\text{ m}}$$

*Getting $-5$ for both means you did not split at the sign change.*

---

## How to Read Your Result

| If you missed… | Then before Week 1 you should… |
|---|---|
| **Q1** | Reread Lecture 1 §1. Week 3 will be incoherent without it. |
| **Q3, Q4** | Reread Lecture 1 §3. This appears on every exam in this course. |
| **Q5, Q6** | Drill substitution — Lecture 2 and PS 0 Part B. This is the prerequisite for Weeks 1–2. |
| **Q7** | Add "check symmetry" to your first pass on every integral. |
| **Q8, Q9, Q10** | Reread Lecture 3. Week 4 is these ideas with harder geometry. |
| **Q10(b) only** | You know the material; you are not splitting at sign changes. Cheap marks to recover. |

**Missing three or more:** go to the Math Help Center this week. Not in Week 3 — this week. The material does not get lighter, and Week 1 assumes all of this.

---

*MATH 142 · Week 0 · Diagnostic Quiz · ungraded*
