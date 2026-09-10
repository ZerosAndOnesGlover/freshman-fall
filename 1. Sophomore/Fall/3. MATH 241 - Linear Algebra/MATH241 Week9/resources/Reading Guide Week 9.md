# MATH 241 · Reading Guide · Week 9
## Strang §4.3, and the last reading before Midterm 2

---

**§4.3 is short and you have already done most of it.** Least squares is Week 8's projection with data attached, so the new content is the *interpretation* and the *numerics* — and the numerics are not in Strang's Chapter 4 at all.

| Chapter | Read? | Why |
|---|---|---|
| **4.3 Least Squares Approximations** | **All of it** | L27 entire |
| **4.3, the "fitting a line" worked example** | **Do it before reading his answer** | The habit, not the arithmetic |
| **§11.2 (or the QR remarks in §4.4)** | **Read** | L28. Strang is briefer than these notes; the table in L28 §4 is not in his book |
| 4.4 revisited | **Skim** | You read it last week; §4.3 gives it a purpose |
| **8.6 / the statistics section** | Read if present | L29's weighted least squares and the MATH 251 connection |
| **Trefethen & Bau, Lecture 11** | **Read this if you read one thing** | Least squares done numerically. **Better than any textbook treatment for L28** |
| **Goodfellow §2.9, §5.1** | Skim | The ML framing: least squares as the first learning algorithm |

---

## §4.3 — the questions to hold

1. **Strang derives the normal equations twice** — once by calculus (differentiate $\lVert b - Ax\rVert^2$) and once by geometry (the error is orthogonal). **Do both.** They are the same equations and the second is the one to remember.
2. **The columns of $A$ hold the basis functions; the unknowns are the coefficients.** Find where he says this. **Which goes in $A$, the data or the parameters?**
3. He fits a line to points. **Do it yourself first**, then compare. Check $A^\mathsf{T}e = 0$ before looking at his answer.
4. **Find the statement that $\hat x$ minimises the error.** Is it proved by calculus or by Pythagoras? *(L27 §3 uses Pythagoras; it is shorter and it generalises.)*
5. He connects least squares to statistics — the Gauss–Markov theorem, or maximum likelihood. **How much does he assume about the errors?** *(MATH 251 next term.)*
6. **Does he warn against the normal equations numerically?** *(He may not, or only briefly. **L28 is where this course diverges from the book**, and the divergence is the week's most useful content.)*

---

## §11.2 / the QR discussion

7. **$\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$.** Find it if he states it. **This one identity is the whole argument of L28.**
8. Substituting $A = QR$ into the normal equations gives $R\hat x = Q^\mathsf{T}b$. **You derived this in PS 8 Q4(d).** Check your derivation against his.
9. **Does he distinguish Gram–Schmidt QR from Householder QR?** L28 §4's table shows they behave completely differently on the same problem, and **most textbooks say "use QR" without saying which.**

---

## Where Trefethen & Bau Earns Its Place

**Lecture 11 of *Numerical Linear Algebra* is the best twelve pages on this topic anywhere**, and it is readable now — it assumes exactly Weeks 8 and 9.

| | |
|---|---|
| The three algorithms compared | normal equations, QR, SVD — **with the same conditioning analysis L28 gives** |
| Why $\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$ | proved properly, via singular values |
| When the normal equations are **acceptable** | he is fairer to them than L28 is; read both |
| The SVD route | **Week 11**, and he explains why it is the most robust and the most expensive |

**Read it after L28 and before the midterm** if you have time; it will make the table in L28 §4 feel inevitable.

---

## Before Midterm 2

**Wednesday of Week 10, 18:00–19:15, SSB 110, covering Weeks 6–9.** One handwritten sheet, one side.

**Weeks 6–9 are one arc, not four topics:**

$$\text{eigenvalues} \to \text{diagonalisation} \to \text{orthogonality} \to \text{least squares}$$

**A gap in Week 6 surfaces as a failure in Week 9**, so revise in order rather than by topic.

**What belongs on the sheet**, roughly by how often it is the thing people cannot recall:

- **The diagonalisability criterion** — geometric $=$ algebraic, **not** "the eigenvalue repeats".
- **$\sum\lambda_i = \operatorname{trace}$ and $\prod\lambda_i = \det$** — two free checks.
- **The normal equations**, and $P = A(A^\mathsf{T}A)^{-1}A^\mathsf{T}$.
- **$\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$**, and $\operatorname{cond}(Q) = 1$.
- **The four-subspace diagram** — still, and now with $b = p + e$ drawn on it.

**What does not belong:** the rotation matrix, the $2\times2$ inverse, the $2\times2$ characteristic polynomial. **All derivable in seconds**, and the space is better spent above.

> **The three verification checks are worth more than any formula on the sheet**, because they are
> what catch errors under time pressure:
>
> | Weeks | Check |
> |---|---|
> | 6–7 | $Av = \lambda v$, and $S\Lambda S^{-1} = A$ |
> | 8–9 | $A^\mathsf{T}e = 0$ |
> | 9 | the line passes through $(\bar x, \bar y)$ |
>
> **Each is exact and takes seconds.** Marks are lost to unverified work far more often than to
> misunderstood theory.

---

## The Habit for This Week

**Ask what the residual is *not* telling you.**

$\lVert e\rVert$ measures how far the data is from your model's reach. **It does not measure whether the model is any good**, and this week gives two proofs of that:

- **More columns always reduce it** (L29 §4), so a smaller residual across different models is guaranteed, not earned.
- **A middle outlier can produce a *larger* residual while doing *less* damage to the fit** than an end outlier (PS 9 Q5(b)), so residual size does not track distortion either.

**The number the arithmetic hands you is real and it answers a narrower question than you want answered.** Getting into the habit of asking which question — this week, on a problem where you can check — is what makes the habit available later, on a problem where you cannot.

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| **Strang, MIT 18.06, Lecture 16** | Projections and least squares |
| **Trefethen & Bau, Lecture 11** | **The best treatment of L28.** Twelve pages |
| **`numpy.linalg.lstsq` docs** | Note which algorithm it uses, and the `rcond` parameter — **that is Week 11** |
| **MATH 251, next term** | Why least squares is the maximum-likelihood estimate, and what "unbiased" means |
| **Week 11** | The SVD: least squares when the columns are *not* independent |

---

*MATH 241 · Week 9 · Reading Guide · © CSE Department*
