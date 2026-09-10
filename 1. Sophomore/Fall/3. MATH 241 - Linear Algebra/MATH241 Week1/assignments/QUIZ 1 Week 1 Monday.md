# MATH 241 · Quiz 1
## Administered: Monday, Week 1 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 0** — linear systems, the two pictures, Gaussian elimination, cost and conditioning.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room — the point
> is to find out what has not landed while there is still a term left to fix it.
>
> Do not look at the key first. It costs you the only thing the exercise is for.

---

**Q1.** How many solutions can a system of linear equations have? List every possibility, and say in one sentence why the list is that short.

&nbsp;

&nbsp;

---

**Q2.** Write $Ax$ as a combination of the columns of $A$, for $A = \begin{bmatrix}1&3\\2&-1\end{bmatrix}$ and $x = (4, 1)$. Give the resulting vector.

&nbsp;

&nbsp;

---

**Q3.** Elimination reaches a $0$ in the pivot position. Name the **two** things this can mean, and give the single test that distinguishes them.

&nbsp;

&nbsp;

---

**Q4.** Elimination costs about $n^3/3$. Back substitution costs about $n^2/2$. At $n = 1000$, what fraction of the total is the back substitution — roughly?

&nbsp;

&nbsp;

---

**Q5.** Solve $\;\varepsilon x_1 + x_2 = 1,\; x_1 + x_2 = 2\;$ with $\varepsilon = 10^{-17}$, in double precision, taking the pivots in the order given. What does the algorithm return for $x_1$, and what is the true answer?

&nbsp;

&nbsp;

---

**Q6.** State the partial-pivoting rule in one sentence, and say what bound it guarantees.

&nbsp;

&nbsp;

---

**Q7.** A matrix has $\det A = 10^{-40}$. Is solving $Ax = b$ with it going to be numerically difficult? Justify your answer.

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **None, exactly one, or infinitely many.** Never two, never seventeen. Because if $x$ and $y$ are distinct solutions then so is $x + t(y-x)$ for every real $t$ — two solutions generate a whole line of them. *(L01 §5. The finiteness you know from $x^2 = 4$ is a non-linear phenomenon.)*

---

**Q2.** $4\begin{bmatrix}1\\2\end{bmatrix} + 1\begin{bmatrix}3\\-1\end{bmatrix} = \begin{bmatrix}7\\7\end{bmatrix}$.

*The entries of $x$ are the **amounts** of each column. If you computed it as two dot products you got the right number by the reading this course is trying to displace — L01 §4.*

---

**Q3.** **(i) A row exchange is needed** — there is a nonzero below it in that column, and swapping fixes it. Nothing is wrong with the matrix. **(ii) The matrix is singular** — the whole column below is zero, so there is no pivot here at all.

**The test: look down the column, below the pivot row. Is there a nonzero?** That is the only thing you have to check.

---

**Q4.** $n^3/3 = 3.3\times10^{8}$ and $n^2/2 = 5\times10^{5}$, so back substitution is about **$0.15\%$** — roughly one part in seven hundred. **Reaching triangular form is essentially all of the work**, which is why Week 1 keeps the factorisation.

---

**Q5.** It returns **$x_1 = 0.0$**. The true answer is $x_1 = 1/(1-\varepsilon)$, which is **$1$** to every digit a `double` holds.

*The multiplier is $10^{17}$, so $1 - 10^{17}$ and $2 - 10^{17}$ both round to $-10^{17}$; then $x_2 = 1$ exactly, $1 - x_2 = 0$ exactly, and $x_1 = 0/\varepsilon = 0$. **A 100% error with no warning.** L03 §4.*

---

**Q6.** **At each column, swap the row with the largest absolute value in that column into the pivot position.** It guarantees every multiplier satisfies $\lvert\ell_{ik}\rvert \le 1$, so no step can amplify.

*It does **not** guarantee accuracy — it bounds the multipliers, not the answer, and Wilkinson matrices still grow by $2^{n-1}$ under it.*

---

**Q7.** **You cannot tell, and the determinant is the wrong thing to look at.** $\det(cA) = c^n\det A$, so a tiny determinant may mean nothing but small entries — $10^{-4}I_{2}$ has $\det = 10^{-8}$ and is perfectly conditioned. **Compute $\operatorname{cond}(A) = \lVert A\rVert\lVert A^{-1}\rVert$ instead**, which is scale-invariant. *(L03 §6–§7. $\det H_{10} = 2.2\times10^{-53}$ and the difficulty is real; $\det(10^6 I_2)$ is enormous and there is none.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1 | L01 §5 — and redo the two-line proof from memory |
| **Q2** | **L01 §4.** This is the habit the whole course rests on. **Fix it this week** |
| **Q3** | **L02 §6** — the two cases are on the midterm every year |
| Q4 | L03 §2 |
| Q5, Q6 | L03 §4–§5 |
| Q7 | L03 §6–§7 |

**Q2 and Q3 are the ones that recur.** Q2 because Weeks 2 and 3 are entirely about the column space and you cannot see it through dot products; Q3 because "singular" is a property of the matrix and "needs a swap" is a property of the row order, and every exam question about rank turns on the difference. **If either was shaky, fix it before Week 2 rather than before the midterm.**

---

*MATH 241 · Week 1 · Quiz 1 · covers Week 0 · ungraded*
