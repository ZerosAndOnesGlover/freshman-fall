# MATH 142 · Calculus II
## Quiz 10 — With Answer Key
### Week 10 · Monday · **Covers Week 9**

---

**Time:** 15 minutes, start of Monday's lecture
**Closed book, no calculator**
**Total: 20 points** (4 points each)

**Covers Week 9:** power series, radius and interval of convergence, term-by-term operations.

---

## Questions

**Q1.** Find the radius of convergence of $\displaystyle\sum_{n=1}^{\infty}\frac{n\,x^n}{4^n}$.

**Q2.** Find the **interval** of convergence of $\displaystyle\sum_{n=1}^{\infty}\frac{x^n}{n^3}$.

**Q3.** Find the **interval** of convergence of $\displaystyle\sum_{n=1}^{\infty}\frac{(x+2)^n}{n}$.

**Q4.** Find a power series for $\dfrac{1}{1-2x}$ and state its radius.

**Q5.** Find a power series for $\ln(1+x^2)$ and state its radius.

---
---

# ANSWER KEY

---

**Q1. (4)** $\left|\frac{c_{n+1}}{c_n}\right| = \frac{n+1}{4^{n+1}}\cdot\frac{4^n}{n} = \frac14\cdot\frac{n+1}{n}\to\frac14$, so

$$\boxed{R=4}$$

*Marking: 3 ratio, 1 for inverting it. Verified.*

**Q2. (4)** $R=1$, centre 0, open interval $(-1,1)$.

- **$x=1$:** $\sum\frac{1}{n^3}$ — $p$-series, $p=3>1$. **Converges.**
- **$x=-1$:** $\sum\frac{(-1)^n}{n^3}$ — **converges absolutely.**

$$\boxed{[-1,1]}$$

*Marking: 1 radius, 1 per endpoint, 1 for the brackets. Verified.*

**Q3. (4)** $R=1$, **centre $a=-2$**, open interval $|x+2|<1\iff(-3,-1)$.

- **$x=-1$:** $(x+2)^n=1$, giving $\sum\frac1n$. **Diverges.**
- **$x=-3$:** $(x+2)^n=(-1)^n$, giving $\sum\frac{(-1)^n}{n}$. **Converges.**

$$\boxed{[-3,-1)}$$

*Marking: **2 of the 4 for the centre.** Reporting $[-1,1)$ — the interval for the uncentred version — is the standard error. Verified.*

**Q4. (4)** Substituting $2x$ into the geometric series:

$$\frac{1}{1-2x} = \sum_{n=0}^\infty(2x)^n = \sum_{n=0}^\infty 2^nx^n, \qquad |2x|<1 \implies \boxed{R=\tfrac12}$$

*Marking: 2 series, **2 for the radius $\frac12$, not 1.** Substitution shrinks the interval. Verified.*

**Q5. (4)** Substituting $x^2$ into $\ln(1+u) = \sum_{n\ge1}\frac{(-1)^{n+1}u^n}{n}$:

$$\ln(1+x^2) = \sum_{n=1}^\infty\frac{(-1)^{n+1}x^{2n}}{n} = x^2-\frac{x^4}{2}+\frac{x^6}{3}-\cdots$$

Condition $|x^2|<1\iff|x|<1$, so $\boxed{R=1}$.

*Marking: 3 series, 1 radius. Verified.*

---

## Marking Summary

| Question | Points | Tests |
|---|---|---|
| Q1 | 4 | Radius by Ratio Test |
| Q2 | 4 | Interval, both endpoints |
| Q3 | 4 | Interval with a shifted centre |
| Q4 | 4 | Substitution and its effect on $R$ |
| Q5 | 4 | Substitution of $x^2$ |
| **Total** | **20** | |

---

## Note for the Instructor

**Q3 is the diagnostic** — the centre is the thing students lose, and it recurs on Midterm 2 this week.

**Q4 and Q5 set up today's lecture directly:** both are Taylor series obtained without computing a single derivative, which is Lecture 1's main methodological point.

---

*MATH 142 · Week 10 · Quiz 10 · covers Week 9*
