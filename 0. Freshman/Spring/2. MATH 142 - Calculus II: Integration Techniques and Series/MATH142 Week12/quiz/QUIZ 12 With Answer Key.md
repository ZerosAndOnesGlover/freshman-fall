# MATH 142 · Calculus II
## Quiz 12 — With Answer Key
### Week 12 · Monday · **Covers Week 11**

---

**Time:** 15 minutes, start of Monday's lecture
**Closed book, no calculator**
**Total: 20 points** (4 points each)

**Covers Week 11:** separable equations, first-order linear equations, models, equilibria.

**The last quiz of the course.**

---

## Questions

**Q1.** Solve $\dfrac{dy}{dx}=x^2y^2$. **State any solution your method loses.**

**Q2.** Solve $\dfrac{dy}{dx}+3y=6$ with $y(0)=1$.

**Q3.** Solve $x\dfrac{dy}{dx}-y=x^2$.

**Q4.** A population satisfies $\dfrac{dP}{dt}=\tfrac12P\left(1-\dfrac{P}{100}\right)$ with $P(0)=10$. **Write $P(t)$ and give $\lim_{t\to\infty}P(t)$.**

**Q5.** For $\dfrac{dy}{dx}=y(y-1)(y-3)$, **find the equilibrium solutions and classify each as stable or unstable — without solving the equation.**

---
---

# ANSWER KEY

---

**Q1. (4)** Separable: $\dfrac{dy}{y^2}=x^2dx$, so $-\dfrac1y=\dfrac{x^3}{3}+C$ and

$$\boxed{y=\frac{-3}{x^3+C'}}$$

**Lost solution: $y\equiv0$**, killed by dividing by $y^2$.

*(Verified.) Marking: 3 for the solution, **1 for $y\equiv0$** — this mark is the point of the question. **Do not award it for a vague remark about "the trivial case"**; the student must name $y\equiv0$ as a solution.*

**Q2. (4)** Already in standard form with $P=3$, so $\mu=e^{3x}$ and $(e^{3x}y)'=6e^{3x}$, giving $y=2+Ce^{-3x}$. Then $y(0)=1\Rightarrow C=-1$:

$$\boxed{y=2-e^{-3x}}$$

*(Verified.) Marking: 3 general, 1 initial condition. **Separation also works here** ($\frac{dy}{6-3y}=dx$) and earns full marks.*

**Q3. (4)** **Standard form first** — divide by $x$:

$$\frac{dy}{dx}-\frac{1}{x}y = x, \qquad \mu=e^{-\int dx/x}=\frac1x$$

Then $\left(\dfrac yx\right)'=1$, so $\dfrac yx=x+C$ and

$$\boxed{y=x^2+Cx}$$

*(Verified.) Marking: 1 standard form, 2 $\mu$, 1 answer. **Reading $P=-1$ off the undivided equation is the standard error** and caps the question at 1.*

**Q4. (4)** Logistic with $k=\tfrac12$, $M=100$, $A=\dfrac{M-P_0}{P_0}=9$:

$$\boxed{P(t)=\frac{100}{1+9e^{-t/2}}}, \qquad \lim_{t\to\infty}P(t)=\boxed{100}$$

*(Verified: substituting into the equation gives residual exactly $0$, and $P(0)=10$.)*

*Marking: 3 solution, 1 limit. **Award the limit mark even if the solution is wrong**, provided the student reads it off the equation ($P=M$ is the stable equilibrium) rather than from a broken formula.*

**Q5. (4)** Set $y'=0$: **equilibria $y=0,\ 1,\ 3$.**

**Sign of $y'$ between them** *(verified at sample points)*:

| interval | sample | $y'$ | motion |
|---|---|---|---|
| $y<0$ | $-1$ | $-8$ | down, away from $0$ |
| $0<y<1$ | $0.5$ | $+0.625$ | up, toward $1$ |
| $1<y<3$ | $2$ | $-2$ | down, toward $1$ |
| $y>3$ | $4$ | $+12$ | up, away from $3$ |

$$\boxed{y=0\ \text{unstable},\qquad y=1\ \textbf{stable},\qquad y=3\ \text{unstable}}$$

*(Confirmed by the derivative test: $f'(y)=3y^2-8y+3$ gives $f'(0)=3>0$, $f'(1)=-2<0$, $f'(3)=6>0$.)*

*Marking: 2 for the three equilibria, 2 for the classification **with the sign evidence.** A bare list of "stable/unstable" with no signs or derivative values earns 1 of the 2.*

---

## Notes for the Grader

- **Q1's lost solution and Q3's standard form are the two marks that separate the class.** Both were flagged repeatedly in Week 11 and both are on the reference sheet.
- **Every answer here can be checked by substitution in under thirty seconds.** Students who ran out of time should be reminded that the check is faster than the solve.
- **This is the last quiz.** Return it before the final, and use the debrief to point at the revision guide.

---

*MATH 142 · Quiz 12 · Week 12*
