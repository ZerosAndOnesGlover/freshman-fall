# MATH 241 · Quiz 8
## Administered: Monday, Week 8 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 7** — diagonalization, its failure, and complex eigenvalues.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.

---

**Q1.** State $A = S\Lambda S^{-1}$: what is in $S$, what is in $\Lambda$, and what must be true for it to exist?

&nbsp;

&nbsp;

---

**Q2.** $A$ is $3\times3$ with eigenvalues $2, 2, 5$. **What must you check** to decide whether $A$ is diagonalisable?

&nbsp;

&nbsp;

---

**Q3.** You have $A = S\Lambda S^{-1}$. How do you compute $A^{20}$, and why is it cheap?

&nbsp;

&nbsp;

---

**Q4.** A student swaps two diagonal entries of $\Lambda$ but leaves $S$ alone. **Which of trace, determinant, rank and eigenvalues would detect the error?**

&nbsp;

&nbsp;

---

**Q5.** $\begin{bmatrix}5&\varepsilon\\ 0&5\end{bmatrix}$ with $\varepsilon = 10^{-12}$. Is it diagonalisable? Could a computer tell you?

&nbsp;

&nbsp;

---

**Q6.** A real $2\times2$ has $\operatorname{trace} = 2$ and $\det = 5$. **Without finding the eigenvalues**, describe what the matrix does geometrically.

&nbsp;

&nbsp;

---

**Q7.** A Markov matrix has eigenvalues $1$ and $0.6$. What happens to $P^k$, and what governs the rate?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **$S$ has the eigenvectors as its columns; $\Lambda$ has the eigenvalues on its diagonal**, in the same order. **It exists iff $A$ has $n$ linearly independent eigenvectors** — which is what makes $S$ invertible. *(L21 §1.)*

---

**Q2.** **The geometric multiplicity of $\lambda = 2$** — i.e. $\dim\mathbf{N}(A - 2I)$. If it is $2$, $A$ is diagonalisable; if $1$, it is not.

*$\lambda = 5$ needs no check: algebraic multiplicity 1 forces geometric 1. **A repeated eigenvalue is not itself the problem** — L20 §5.*

---

**Q3.** $A^{20} = S\Lambda^{20}S^{-1}$, and $\Lambda^{20} = \operatorname{diag}(\lambda_1^{20},\dots,\lambda_n^{20})$ — **$n$ scalar powers.**

**Cheap because the cost does not grow with the exponent**: two fixed matrix products either way, whether the power is 20 or 20,000. *(L21 §4.)*

---

**Q4.** **None of them.**

The result is $S\Lambda'S^{-1}$ for a diagonal $\Lambda'$ with the same entries, so it is **similar to $A$** — and every similarity invariant therefore agrees. **Trace, determinant, rank, characteristic polynomial and eigenvalues are all identical.**

**The only check is to multiply out $S\Lambda S^{-1}$ and compare with $A$.** *(Second time this term — Week 4's reversed $M$ was the first.)*

---

**Q5.** **Not diagonalisable** — $A - 5I = \begin{bmatrix}0&\varepsilon\\0&0\end{bmatrix}$ has rank 1 for any $\varepsilon \ne 0$, so the eigenspace is one-dimensional against algebraic multiplicity 2.

**A computer could compare $\varepsilon$ with zero** — but a matrix arriving from measurement or from earlier floating-point work carries its own error, so **the distinction is not recoverable in practice.** The property jumps discontinuously at $\varepsilon = 0$, and **no numerical algorithm tests for diagonalisability.** *(L22 §4.)*

---

**Q6.** Discriminant $4 - 20 < 0$, so the eigenvalues are complex. By L23 §2,

$$r = \sqrt{\det} = \sqrt5 \approx 2.24, \qquad \cos\theta = \frac{2}{2\sqrt5} = 0.447 \Rightarrow \theta \approx 63°$$

**It rotates the plane by about $63°$ and scales it by $\sqrt5$.** *(No eigenvector needed.)*

---

**Q7.** **$P^k$ converges**, every column tending to the steady state — the $\lambda = 1$ eigenvector — **from any starting vector.**

**The rate is governed by the second eigenvalue: the error decays as $0.6^k$.** *(L23 §5. This is why PageRank takes about fifty iterations rather than ten thousand.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L21 §1 and §5 |
| Q3 | L21 §4 |
| **Q4** | **L21 §2 and REC 7 §1(b).** **Multiply it out — nothing else works** |
| Q5 | L22 §4 |
| Q6 | L23 §2 |
| Q7 | L23 §5 |

**Q4 is the one that costs marks on the exam.** It is the second appearance of a trap whose defining feature is that **no invariant detects it** — and Weeks 10 and 11 are two more factorisations, so the habit of verifying by multiplication needs to be in place now.

---

*MATH 241 · Week 8 · Quiz 8 · covers Week 7 · ungraded*
