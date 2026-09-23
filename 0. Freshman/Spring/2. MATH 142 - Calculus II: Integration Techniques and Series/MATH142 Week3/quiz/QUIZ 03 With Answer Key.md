# MATH 142 · Calculus II
## Quiz 03 — With Answer Key
### Week 3 · Monday · **Covers Week 2**

---

**Date:** Monday 8 February 2027 · 11:00–11:15 (start of Lecture 1) · Week 3
**Time:** 15 minutes, start of Monday's lecture
**Closed book, no calculator**
**Total: 20 points** (4 points each)

**Covers Week 2:** trigonometric substitution, completing the square, partial fractions.

---

## Questions

**Q1.** Find $\displaystyle\int\frac{dx}{x^2+2x+10}$.

**Q2.** Find $\displaystyle\int\frac{dx}{\sqrt{4-x^2}}$.

**Q3.** Decompose $\dfrac{3x+11}{(x-3)(x+2)}$ into partial fractions, then integrate.

**Q4.** Find $\displaystyle\int\frac{2x+1}{x^2+1}\,dx$.

**Q5.** Find $\displaystyle\int\frac{x^2+1}{x-1}\,dx$.

---
---

# ANSWER KEY

---

**Q1. (4)** Complete the square: $x^2+2x+10 = (x+1)^2+9$. With $u=x+1$:

$$\int\frac{du}{u^2+9} = \frac13\arctan\frac u3 \implies \boxed{\frac13\arctan\frac{x+1}{3}+C}$$

*Marking: 2 for completing the square, 2 for the arctangent. **The leading $\frac13$ is worth 1** and is dropped constantly. Verified symbolically.*

**Q2. (4)** $\boxed{\arcsin\dfrac x2 + C}$

Either from the catalogue directly, or by $x=2\sin\theta$: $\int\frac{2\cos\theta\,d\theta}{2\cos\theta} = \theta = \arcsin\frac x2$.

*Marking: 4. **Accept the catalogue answer without a substitution** — recognising it is the skill. Deduct 1 for $\arcsin x$ (missing the $\frac x2$). Verified symbolically.*

**Q3. (4)** Cover-up: $A = \dfrac{3(3)+11}{3+2} = \dfrac{20}{5} = 4$; $B = \dfrac{3(-2)+11}{-2-3} = \dfrac{5}{-5} = -1$.

$$\frac{3x+11}{(x-3)(x+2)} = \frac{4}{x-3}-\frac{1}{x+2}$$

$$\boxed{\int = 4\ln|x-3| - \ln|x+2| + C}$$

*Marking: 2 for the decomposition, 2 for the integral. Verified: the CAS returns $\frac{4}{x-3}-\frac{1}{x+2}$ and the same antiderivative.*

**Q4. (4)** Split the numerator — the $2x$ is exactly the derivative of $x^2+1$:

$$\int\frac{2x}{x^2+1}dx + \int\frac{dx}{x^2+1} = \boxed{\ln(x^2+1)+\arctan x + C}$$

*Marking: 2 for splitting, 1 for each piece. **No absolute value needed**: $x^2+1>0$. Verified symbolically.*

**Q5. (4)** **Improper fraction — divide first.** $\dfrac{x^2+1}{x-1} = x+1+\dfrac{2}{x-1}$.

$$\boxed{\int = \frac{x^2}{2}+x+2\ln|x-1|+C}$$

*Marking: **2 of the 4 for recognising the need to divide.** A student who attempted a partial fraction decomposition directly gets 0 for method — the degrees make it impossible, and this was Lecture 2 §4. Verified symbolically.*

---

## Marking Summary

| Question | Points | Tests |
|---|---|---|
| Q1 | 4 | Completing the square → arctangent |
| Q2 | 4 | Recognising a catalogue entry |
| Q3 | 4 | Partial fractions, distinct linear |
| Q4 | 4 | Splitting a linear numerator |
| Q5 | 4 | Checking the degrees first |
| **Total** | **20** | |

---

## Note for the Instructor

**Q5 is the diagnostic.** Failing to check whether a fraction is proper was the subject of PS 2's D2, and it recurs this week in a new costume: **failing to check whether an integrand is bounded before applying the Fundamental Theorem.**

Both are the same habit — *verify the hypotheses before applying the method*. If Q5 goes badly, make that connection explicit when introducing improper integrals today, because Lecture 2's $\int_{-1}^{1}\frac{dx}{x^2}=-2$ trap is exactly the same failure.

---

*MATH 142 · Week 3 · Quiz 03 · covers Week 2*
