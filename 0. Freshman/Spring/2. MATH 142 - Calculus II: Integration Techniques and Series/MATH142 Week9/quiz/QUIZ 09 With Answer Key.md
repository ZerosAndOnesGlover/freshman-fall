# MATH 142 · Calculus II
## Quiz 09 — With Answer Key
### Week 9 · Monday · **Covers Week 8**

---

**Date:** Monday 22 March 2027 · 11:00–11:15 (start of Lecture 1) · Week 9
**Time:** 15 minutes, start of Monday's lecture
**Closed book, no calculator**
**Total: 20 points** (4 points each)

**Covers Week 8:** alternating series, absolute and conditional convergence, Ratio and Root tests.

---

## Questions

**Q1.** Classify $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{\sqrt n}$ as absolutely convergent, conditionally convergent, or divergent.

**Q2.** Does $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^n n}{n+1}$ converge? Name the test.

**Q3.** Does $\displaystyle\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ converge? Use the Ratio Test.

**Q4.** Classify $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^n}{n^2+1}$.

**Q5.** For $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n^2}$, how many terms guarantee an error below $0.01$?

---
---

# ANSWER KEY

---

**Q1. (4)** $\sum|a_n| = \sum\frac{1}{\sqrt n}$ is a $p$-series with $p=\frac12\le1$: **diverges.**

Alternating Series Test: $b_n=\frac{1}{\sqrt n}$ decreasing ✓, $\to0$ ✓ — **converges.**

$$\boxed{\textbf{Conditionally convergent}}$$

*Marking: 2 for the absolute test, 1 for the AST, **1 for the classification word.** "Converges" alone earns 2 — the question asked for the classification.*

**Q2. (4)** $b_n = \frac{n}{n+1}\to1\neq0$, so $a_n\not\to0$.

**Diverges**, by the **$n$-th Term Test.** *(Verified.)*

*Marking: 2 verdict, **2 for naming the right test.** The Alternating Series Test does not apply here and citing it as the reason earns 1.*

**Q3. (4)**

$$\left|\frac{a_{n+1}}{a_n}\right| = \frac{(n+1)^2}{2^{n+1}}\cdot\frac{2^n}{n^2} = \frac12\left(\frac{n+1}{n}\right)^2\longrightarrow\frac12 < 1$$

**Converges** (absolutely). *(Verified; the sum is exactly 6.)*

*Marking: 3 ratio, 1 verdict.*

**Q4. (4)** $\left|\frac{(-1)^n}{n^2+1}\right| = \frac{1}{n^2+1}<\frac{1}{n^2}$, and $\sum\frac1{n^2}$ converges.

$$\boxed{\textbf{Absolutely convergent}}$$

*Marking: 2 comparison, 2 classification. **The Alternating Series Test is not needed** — noting that absolute convergence is the stronger and quicker conclusion deserves a comment.*

**Q5. (4)** Require $b_{N+1} = \dfrac{1}{(N+1)^2}<0.01$, i.e. $(N+1)^2>100$, i.e. $N+1>10$:

$$\boxed{N=10}$$

*(Verified: $s_{10} = 0.81796$, true value $\frac{\pi^2}{12} = 0.82247$, error $0.0045<0.01$ ✓.)*

*Marking: 2 for the bound, 2 for solving. **A student who wrote $N=9$ (from $(N+1)^2\ge100$) is off by one but has the method** — award 3.*

---

## Marking Summary

| Question | Points | Tests |
|---|---|---|
| Q1 | 4 | Conditional convergence |
| Q2 | 4 | $n$-th Term Test, not AST |
| Q3 | 4 | Ratio Test |
| Q4 | 4 | Absolute convergence by comparison |
| Q5 | 4 | Alternating error bound |
| **Total** | **20** | |

---

## Note for the Instructor

**Q1 and Q4 are the pair**, and the distinction between them is the week's content: same alternating structure, but one absolute series converges and the other does not.

**Today's lecture makes this immediately relevant.** At the endpoints of an interval of convergence, exactly these two situations arise — and a student who cannot tell Q1 from Q4 will not be able to classify an endpoint. **Worth saying so when introducing power series today.**

---

*MATH 142 · Week 9 · Quiz 09 · covers Week 8*
