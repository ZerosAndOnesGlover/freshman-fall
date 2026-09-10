# MATH 241 · Quiz 7
## Administered: Monday, Week 7 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 6** — eigenvalues, eigenvectors, and the characteristic polynomial.

**Instructions:** Closed notes. 10 minutes.

> **Back to Monday.** Last week's Tuesday quiz was the Fall Break exception; Weeks 7–11 are Mondays.
>
> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.

---

**Q1.** Define an eigenvector. Why must $v \ne 0$, and why is $\lambda = 0$ nevertheless allowed?

&nbsp;

&nbsp;

---

**Q2.** Find the eigenvalues of $\begin{bmatrix}5&3\\ 1&3\end{bmatrix}$ **using the $2\times2$ shortcut.**

&nbsp;

&nbsp;

---

**Q3.** $A$ is $3\times3$ with eigenvalues $2, 3, -1$. Give $\operatorname{trace}A$ and $\det A$. Why are these free checks?

&nbsp;

&nbsp;

---

**Q4.** Write down the eigenvalues of $\begin{bmatrix}7&2&9\\ 0&-3&4\\ 0&0&5\end{bmatrix}$, and say why you may.

&nbsp;

&nbsp;

---

**Q5.** Why does a rotation by $90°$ have no real eigenvalues? What are its complex ones, and do trace and determinant still work?

&nbsp;

&nbsp;

---

**Q6.** $-I$ and $\begin{bmatrix}1&1\\ 0&1\end{bmatrix}$ both have a repeated eigenvalue. **Only one is defective.** Which, and what is the criterion?

&nbsp;

&nbsp;

---

**Q7.** Why is cofactor expansion the right tool for $\det(A - \lambda I)$, when Week 5 showed it is $9\times10^{14}$ times too slow at $n = 20$?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** A nonzero $v$ with $Av = \lambda v$.

**$v \ne 0$** because $A0 = \lambda 0$ holds for every $\lambda$ and would make every scalar an eigenvalue. **$\lambda = 0$ is allowed** and means $Av = 0$ for some $v \ne 0$ — that is, $\mathbf{N}(A) \ne \{0\}$, so **$A$ is singular.** *(L19 §1.)*

---

**Q2.** $\operatorname{trace} = 8$, $\det = 15 - 3 = 12$, so

$$\lambda^2 - 8\lambda + 12 = 0 \quad\Longrightarrow\quad \boxed{\lambda = 2,\ 6}$$

*Two numbers read off the matrix. If you expanded a determinant you did it the slow way — L20 §3.*

---

**Q3.** $\operatorname{trace}A = 2 + 3 - 1 = \mathbf{4}$; $\det A = 2 \cdot 3 \cdot (-1) = \mathbf{-6}$.

**Free because** the trace is the diagonal sum — read off, no computation — and $\det A = p(0)$, the constant term of a characteristic polynomial **you have already computed** to get the eigenvalues. *(L20 §2.)*

---

**Q4.** **$\lambda = 7, -3, 5$** — the diagonal entries.

**Because the matrix is triangular**, so $\det(A - \lambda I) = (7-\lambda)(-3-\lambda)(5-\lambda)$, whose roots are the diagonal. *(L19 §5.)*

---

**Q5.** **A rotation by $90°$ leaves no direction unmoved**, so there is nothing for a real eigenvector to be. $p(\lambda) = \lambda^2 + 1$ has no real root.

Over $\mathbb{C}$: $\lambda = \pm i$. **And the identities hold:** $i + (-i) = 0 = \operatorname{trace}$, $i \cdot (-i) = 1 = \det$. *(L19 §6.)*

---

**Q6.** **$\begin{bmatrix}1&1\\0&1\end{bmatrix}$ is defective.**

**The criterion is geometric $<$ algebraic** — the eigenspace dimension is smaller than the root multiplicity. Here $\lambda = 1$ has algebraic 2 and geometric 1. **$-I$ has algebraic 2 and geometric 2** — every vector is an eigenvector — and is diagonal already.

**A repeated eigenvalue is not the problem; a deficient eigenspace is.** *(L20 §5.)*

---

**Q7.** **Because $\det(A - \lambda I)$ has a symbol in it.** Elimination divides by the pivots, and with $\lambda$ present those are expressions like $a_{11} - \lambda$ that **may be zero** — forcing a case split at every step.

**Cofactor expansion only multiplies and adds**, so it produces a polynomial with no cases. *(L17 §5, L19 §3. The $n!$ cost is irrelevant here because $n$ is small and the answer wanted is symbolic.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1 | L19 §1 |
| Q2 | L20 §3 |
| **Q3** | **L20 §2.** Two free checks. **Run them on everything this week** |
| Q4 | L19 §5 |
| Q5 | L19 §6 |
| **Q6** | **L20 §5.** This is today's lecture and all of Week 7 |
| Q7 | L19 §3 |

**Q6 is the one that matters today.** L21 needs $n$ independent eigenvectors, L22 is what happens without them, and a student who thinks "repeated eigenvalue" and "defective" are the same thing will find both lectures arbitrary. **Fix it in the next ten minutes if you have to.**

---

*MATH 241 · Week 7 · Quiz 7 · covers Week 6 · ungraded*
