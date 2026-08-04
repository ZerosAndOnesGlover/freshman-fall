# MATH 142 · Calculus II
## Quiz 01 — With Answer Key
### Week 1 · Monday · **Covers Week 0**

---

**Time:** 15 minutes, start of Monday's lecture
**Closed book, no calculator**
**Total: 20 points** (4 points each)

**Covers Week 0:** the Fundamental Theorem, substitution, and applications of the integral.

---

## Questions

**Q1.** Find $\displaystyle\frac{d}{dx}\int_1^{x^2}\cos(t^3)\,dt$.

**Q2.** Find $\displaystyle\int x^2 e^{x^3}\,dx$.

**Q3.** Evaluate $\displaystyle\int_{-4}^{4}\frac{x^3}{1+x^2}\,dx$.

**Q4.** Find the area of the region bounded by $y = 4-x^2$ and the $x$-axis.

**Q5.** Find the average value of $f(x)=e^x$ on $[0,\ln 2]$.

---
---

# ANSWER KEY

---

**Q1. (4)** $\boxed{2x\cos(x^6)}$

FTC Part 1 with the chain rule: with $F(u)=\int_1^u\cos(t^3)dt$ we have $F'(u)=\cos(u^3)$, and the integral is $F(x^2)$, so the derivative is $\cos((x^2)^3)\cdot 2x$.

*Marking: 2 for $\cos(x^6)$, **2 for the factor $2x$**. Writing $\cos(x^5)$ or $\cos(x^8)$ for $(x^2)^3$ loses 1.*

*Verified numerically at $x=1.2$ and $x=1.9$ to 14 significant figures.*

**Q2. (4)** $u = x^3$, $du = 3x^2dx$:

$$\frac13\int e^u du = \boxed{\frac{e^{x^3}}{3}+C}$$

*Marking: 1 for the substitution, 2 for the answer, **1 for the $+C$**. Verified symbolically.*

**Q3. (4)** $\boxed{0}$

The integrand is **odd** — $x^3$ is odd and $1+x^2$ is even — and the interval $[-4,4]$ is symmetric about the origin.

*Marking: 4 for the symmetry argument. **A student who attempted polynomial division and ran out of time gets 1** for a correct start. The instruction all Week 0 was to check symmetry first; this question is that instruction, examined.*

*Verified symbolically: exactly 0.*

**Q4. (4)** The parabola meets $y=0$ at $x = \pm 2$, and $4-x^2 \ge 0$ between them:

$$A = \int_{-2}^{2}(4-x^2)\,dx = 2\int_0^2 (4-x^2)dx = 2\left[4x - \frac{x^3}{3}\right]_0^2 = 2\left(8-\frac83\right) = \boxed{\frac{32}{3}}$$

*Marking: 1 for the limits $\pm2$, 3 for the value. Using symmetry is not required but is faster. Verified symbolically.*

**Q5. (4)**

$$f_{\text{avg}} = \frac{1}{\ln 2 - 0}\int_0^{\ln 2}e^x\,dx = \frac{\big[e^x\big]_0^{\ln 2}}{\ln 2} = \frac{2-1}{\ln 2} = \boxed{\frac{1}{\ln 2}}\approx 1.4427$$

*Marking: 1 for the $\frac{1}{b-a}$ factor, 2 for the integral, 1 for simplifying $e^{\ln 2}=2$. **Omitting the $\frac{1}{b-a}$ is the standard error** and caps the answer at 2.*

*Verified symbolically: $1/\ln 2$.*

---

## Marking Summary

| Question | Points | Tests |
|---|---|---|
| Q1 | 4 | FTC Part 1 with a chain rule |
| Q2 | 4 | Substitution |
| Q3 | 4 | Symmetry |
| Q4 | 4 | Area, finding your own limits |
| Q5 | 4 | Average value |
| **Total** | **20** | |

---

## Note for the Instructor

**Q1 and Q3 are the diagnostic pair.**

- Missing the $2x$ in **Q1** is the error that recurs on every exam in this course. If more than a quarter of the class drops it, spend five minutes on it before Lecture 2.
- Attempting **Q3** by brute force rather than by symmetry indicates a student who is executing rather than reading. Worth a general comment to the room: the first pass over any integral is a *look*, not a computation.

---

*MATH 142 · Week 1 · Quiz 01 · covers Week 0*
