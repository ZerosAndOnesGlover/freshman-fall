# MATH 142 · Calculus II
## Quiz 02 — With Answer Key
### Week 2 · Monday · **Covers Week 1**

---

**Time:** 15 minutes, start of Monday's lecture
**Closed book, no calculator**
**Total: 20 points** (4 points each)

**Covers Week 1:** integration by parts, reduction formulas, trigonometric integrals.

---

## Questions

**Q1.** Find $\displaystyle\int x e^{2x}\,dx$.

**Q2.** Evaluate $\displaystyle\int_0^1 x e^{-x}\,dx$.

**Q3.** Find $\displaystyle\int\sin^3x\cos^4x\,dx$.

**Q4.** Evaluate $\displaystyle\int_0^{\pi/2}\sin^4x\,dx$ using the reduction formula $I_n = \frac{n-1}{n}I_{n-2}$, with $I_0=\frac\pi2$.

**Q5.** Find $\displaystyle\int\sin5x\,\sin2x\,dx$.

---
---

# ANSWER KEY

---

**Q1. (4)** Parts with $u=x$, $dv=e^{2x}dx$; $du=dx$, $v=\tfrac12e^{2x}$:

$$= \frac{xe^{2x}}{2} - \frac12\int e^{2x}dx = \frac{xe^{2x}}{2}-\frac{e^{2x}}{4} = \boxed{\frac{(2x-1)e^{2x}}{4}+C}$$

*Marking: 1 for the choice of $u$, 2 for execution, 1 for $+C$. **The $v=\tfrac12e^{2x}$ is where the marks go** — students who write $v=e^{2x}$ lose 2. Verified symbolically.*

**Q2. (4)** $u=x$, $dv=e^{-x}dx$; $v=-e^{-x}$:

$$= \Big[-xe^{-x}\Big]_0^1 + \int_0^1 e^{-x}dx = -e^{-1} + \Big[-e^{-x}\Big]_0^1 = -e^{-1} + (1 - e^{-1})$$

$$= \boxed{1 - \frac2e}\approx 0.2642$$

*Marking: 2 for the bracket at both limits, 2 for the rest. **Two minus signs compound here** ($v$ is negative and the formula subtracts). Verified symbolically.*

**Q3. (4)** $m=3$ is **odd** → peel one $\sin x$, convert with $\sin^2=1-\cos^2$, substitute $u=\cos x$ (so $du = -\sin x\,dx$):

$$\int(1-\cos^2x)\cos^4x\,\sin x\,dx = -\int(1-u^2)u^4\,du = -\int(u^4-u^6)du$$

$$= -\frac{u^5}{5}+\frac{u^7}{7} = \boxed{-\frac{\cos^5x}{5}+\frac{\cos^7x}{7}+C}$$

*Marking: 1 for naming the case, 3 for execution. **The minus sign from $du$ is the trap.** Verified symbolically.*

**Q4. (4)**

$$I_4 = \frac34 I_2 = \frac34\cdot\frac12 I_0 = \frac38\cdot\frac\pi2 = \boxed{\frac{3\pi}{16}}\approx 0.5890$$

*Marking: 4 for the recursion shown. Deduct 1 for the answer with no working — the question said to use the formula. Verified symbolically.*

**Q5. (4)** Product-to-sum: $\sin A\sin B = \tfrac12[\cos(A-B)-\cos(A+B)]$ with $A=5x$, $B=2x$:

$$\int\tfrac12\big[\cos3x - \cos7x\big]dx = \frac12\left(\frac{\sin3x}{3}-\frac{\sin7x}{7}\right) = \boxed{\frac{\sin3x}{6}-\frac{\sin7x}{14}+C}$$

*Marking: 2 for the identity, 2 for the integration. Verified symbolically — the CAS returns exactly this.*

---

## Marking Summary

| Question | Points | Tests |
|---|---|---|
| Q1 | 4 | Parts, single application |
| Q2 | 4 | Definite parts, evaluating $[uv]$ |
| Q3 | 4 | The odd-power case |
| Q4 | 4 | The reduction formula |
| Q5 | 4 | Product-to-sum |
| **Total** | **20** | |

---

## Note for the Instructor

**Q3 is the one that matters for this week.** Trigonometric substitution — starting today — produces exactly this kind of integral as its output. A student who cannot finish Q3 will complete a substitution correctly and then be unable to evaluate what it produced.

If Q3 scores poorly across the room, put one worked odd-power example on the board before beginning Lecture 1, and point at the connection explicitly.

---

*MATH 142 · Week 2 · Quiz 02 · covers Week 1*
