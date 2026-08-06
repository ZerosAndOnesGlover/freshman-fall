# MATH 142 · Calculus II
## Quiz 11 — With Answer Key
### Week 11 · Monday · **Covers Week 10**

---

**Time:** 15 minutes, start of Monday's lecture
**Closed book, no calculator**
**Total: 20 points** (4 points each)

**Covers Week 10:** Taylor and Maclaurin series, remainders, applications.

---

## Questions

**Q1.** Find the Maclaurin series for $e^{-2x}$ and state its radius.

**Q2.** Find the Maclaurin series for $x\cos(x^2)$.

**Q3.** Evaluate $\displaystyle\lim_{x\to0}\frac{1-\cos x}{x^2}$ **using series.**

**Q4.** Estimate $\sin(0.1)$ using terms up to $x^3$, and bound the error.

**Q5.** Write a series for $\displaystyle\int_0^{0.3}e^{-x^2}dx$ and evaluate it to three terms.

---
---

# ANSWER KEY

---

**Q1. (4)** Substituting $-2x$ into $e^u=\sum\frac{u^n}{n!}$:

$$\boxed{e^{-2x} = \sum_{n=0}^\infty\frac{(-2)^nx^n}{n!} = 1-2x+2x^2-\frac{4x^3}{3}+\cdots}, \qquad R=\infty$$

*Marking: 3 series, 1 radius. Verified.*

**Q2. (4)** $\cos u = \sum\frac{(-1)^nu^{2n}}{(2n)!}$ with $u=x^2$, then multiply by $x$:

$$\boxed{x\cos(x^2) = \sum_{n=0}^\infty\frac{(-1)^nx^{4n+1}}{(2n)!} = x-\frac{x^5}{2}+\frac{x^9}{24}-\cdots}$$

*Marking: 4. **Verified** — note the exponents $4n+1$, which students often get wrong.*

**Q3. (4)** $1-\cos x = \frac{x^2}{2}-\frac{x^4}{24}+\cdots$, so

$$\frac{1-\cos x}{x^2} = \frac12-\frac{x^2}{24}+\cdots \longrightarrow\boxed{\frac12}$$

*Marking: 2 series, 2 limit. **The question said "using series"** — a L'Hôpital solution earns 2. Verified.*

**Q4. (4)**

$$\sin(0.1)\approx 0.1-\frac{0.1^3}{6} = \boxed{0.09983333}$$

**Alternating estimate:** the error is at most the first omitted term, $\dfrac{0.1^5}{120} = 8.33\times10^{-8}$.

*(True error: $8.331\times10^{-8}$ — the bound is tight to 0.02%.)*

*Marking: 2 estimate, 2 bound. **Naming the bound as the alternating estimate is required.** Verified.*

**Q5. (4)** $e^{-x^2}=\sum\frac{(-1)^nx^{2n}}{n!}$, so

$$\int_0^{0.3}e^{-x^2}dx = \sum_{n=0}^\infty\frac{(-1)^n(0.3)^{2n+1}}{n!(2n+1)}$$

Three terms: $0.3-0.009+0.000243 = \boxed{0.291243}$

*(True value $0.2912379$ — error $5\times10^{-6}$, within the next term $\frac{0.3^7}{6\cdot7}=5.2\times10^{-6}$ ✓)*

*Marking: 2 series, 2 evaluation. Verified.*

---

## Marking Summary

| Question | Points | Tests |
|---|---|---|
| Q1 | 4 | Substitution into $e^x$ |
| Q2 | 4 | Composition and multiplication |
| Q3 | 4 | Limits by series |
| Q4 | 4 | Alternating error bound |
| Q5 | 4 | Term-by-term integration |
| **Total** | **20** | |

---

## Note for the Instructor

**Q5 is the miniature of Week 10's whole argument** — an integrand with no elementary antiderivative, handled in three lines with a free error bound.

**This is the last quiz of the course.** Worth saying so, and worth noting that the final is comprehensive: Week 0's Riemann sums through this week's differential equations.

---

*MATH 142 · Week 11 · Quiz 11 · covers Week 10*
