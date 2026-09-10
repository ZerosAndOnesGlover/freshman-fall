# MATH 241 · Linear Algebra
## Week 9: Least Squares

**Credits:** 4 (3 lecture + 1 recitation) · **Prerequisites:** MATH 141
**Assessment for this course (overall):** Problem Sets 35%, Midterms 40%, Final 25%
**This week's deliverables:** PS 9 (released Wednesday, due **Friday of Week 10**) and **Quiz 9** (Monday, covers Week 8). **PS 8 is due at 17:00 this Friday.**
**Recitation 8 is sat this Thursday** — it covers **Week 8**. Recitation 9, covering this week, is sat on the **Thursday of Week 10** — the day after the midterm.

> **This week completes Midterm 2's material.** The paper is **Wednesday of Week 10, 18:00–19:15,
> SSB 110**, covering **Weeks 6–9**.
>
> **CS 201's and PROG 201's Project 1 are both due Friday at 17:00**, alongside PS 8. **A heavy
> Friday** — three deadlines in one afternoon, none of which this course can move.

---

### Why This Week Exists

Because Week 2 said $Ax = b$ has no solution when $b \notin \mathbf{C}(A)$, and stopped.

**That is the normal situation.** Whenever you have more measurements than parameters, $\mathbf{C}(A)$ is a small subspace of $\mathbb{R}^m$ and almost every $b$ is unreachable — **measurement error alone guarantees it.** "No solution" is a true statement and a useless one.

**Week 8 supplied the answer without naming it:** the nearest reachable point is the projection $p$, so solve $A\hat x = p$ instead. **Least squares is projection with data attached**, and L27 is that sentence made arithmetic.

**But the interesting half of the week is L28**, and it is where this course parts company with the textbook. The normal equations $A^\mathsf{T}A\hat x = A^\mathsf{T}b$ are **exact mathematics and the wrong algorithm**, because

$$\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$$

**doubles the digits you lose.** On Läuchli's matrix — two columns you can see are independent — $A^\mathsf{T}A$ goes **exactly singular in floating point** at $\varepsilon = 10^{-8}$. Nothing is wrong with the data; **the method threw the information away.**

**And the repair is not simply "use QR".** Measured against each other, **Gram–Schmidt QR fails *earlier* than the normal equations on that problem**, and only **Householder QR** survives. Week 8's L26 §5 predicted exactly this and this week measures it.

---

### Learning Objectives

By the end of Week 9, you should be able to:

1. **State the least-squares problem** and say why "no solution" is the normal case.
2. **Derive the normal equations** from orthogonality of the residual.
3. **Fit a line**, putting the parameters in $\hat x$ and the data in $A$ and $b$.
4. **Check every fit with $A^\mathsf{T}e = 0$**, and with the centroid.
5. **Prove $\hat x$ minimises $\lVert b - Ax\rVert$** by Pythagoras.
6. **Say why "squares"**, and what that choice costs.
7. **State $\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$** and convert it into digits lost.
8. **Explain Läuchli's matrix** — where the information was destroyed, and at what $\varepsilon$.
9. **Reduce the normal equations to $R\hat x = Q^\mathsf{T}b$**, justifying every cancellation.
10. **Say why "use QR" is inadequate advice**, and what Householder does differently.
11. **Fit anything linear in the parameters**, and give a model that is not.
12. **Explain why a smaller residual is not evidence of a better model**, and why an outlier's damage does not track its residual.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L27 Least Squares]] | The question Week 2 refused; **the normal equations, and $m$ equations becoming $n$**; fitting a line worked exactly; **why "squares" is a choice**; the geometry as $b = p + e$; what dependent columns break and what they do not |
| [[L28 Least Squares in Practice]] | **$\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$**; **Läuchli's matrix going exactly singular**; the reduction to $R\hat x = Q^\mathsf{T}b$; **three methods, three failure points, one survivor**; what Householder does differently; **when the normal equations are acceptable after all** |
| [[L29 What Least Squares Assumes]] | **Linear in the parameters, not in $x$**; fitting as projection onto a space of functions; **one outlier moving everything**; **more columns always fit better, which is the problem**; **Week 0's Hilbert matrix revealed as polynomial fitting**; weighted least squares |
| [[REC 9 Fitting, the Day After the Midterm]] | Short drill, long clinic — PS 9 before post-mortem. **Thursday of Week 10** |
| [[PS 9 Least Squares]] | Five questions, 100 points, due **Friday of Week 10** |
| [[MATH241 Week9/assignments/QUIZ 9 Week 9 Monday\|QUIZ 9 Week 9 Monday]] | Ten minutes, covers **Week 8**, answer key printed |
| [[MATH241 Week9/resources/Reading Guide Week 9\|Reading Guide Week 9]] | Strang §4.3, **Trefethen & Bau Lecture 11**, and what belongs on the midterm sheet |
| `resources/leastsquares.py` | Every number in L27–L29, reproducible. **Three least-squares methods compared, including a Householder QR** |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**"Use QR instead of the normal equations" is not adequate advice. It matters which QR.**

Three methods, one problem, exact answer $\hat x_1 = 1/(2+\varepsilon^2)$:

| $\varepsilon$ | normal equations | Gram–Schmidt QR | **Householder QR** | exact |
|---|---|---|---|---|
| $10^{-5}$ | $0.500000000$ | $0.499999959$ | $0.500000000$ | $0.500000000$ |
| $10^{-7}$ | $0.500000000$ | $\mathbf{0.511501869}$ | $0.500000000$ | $0.500000000$ |
| $10^{-8}$ | **FAILED** | $\mathbf{1.000000000}$ | $0.500000000$ | $0.500000000$ |

**Read it carefully, because it does not say what the slogan says.**

- **The normal equations look exact until they die** — and their nine correct digits at $\varepsilon = 10^{-7}$ are **luck, not robustness.** $\operatorname{cond}(A^\mathsf{T}A)$ is already $2\times10^{14}$ there; the problem as posed has about two reliable digits, and one step later the matrix is exactly singular.
- **Gram–Schmidt QR is wrong *before* the normal equations are** — because the columns are nearly parallel and the subtraction cancels catastrophically. **Week 8's L26 §5 said so before the evidence existed.**
- **Only Householder survives**, because it builds $Q$ from reflections that are exactly orthogonal by construction rather than by accumulation.

> **This is the fifth time this term that "correct" and "usable" have come apart** — after Cramer's
> rule, the adjugate formula, the $n!$ determinant and the characteristic polynomial. **By now it
> should be a reflex to ask the second question**, and this week is where the reflex is worth the
> most, because the failing method is the one every textbook derives.

---

### Assessment Reminder

**Quizzes and the recitation carry no weight** and are still required. **Quiz 9 is at the start of Monday's lecture and covers Week 8.**

> **Recitation 9 falls the day after Midterm 2 and the day before PS 9 is due** — the same shape as
> Recitation 5, and the sheet is built for it: short drill, long two-part clinic.

Quizzes are tracked in [[_MATH 241 Quiz Record]].

---

### Connections

**Back:** **Week 2's L08 §1 posed the question and refused it.** **Week 8's L25 is the whole of L27** — the projection, the normal equations, the orthogonality of the residual — with data attached. **PS 2 Q5(c)** proved $A^\mathsf{T}A$ invertible in Week 2 for exactly this moment. **PS 8 Q4(d)** derived $R\hat x = Q^\mathsf{T}b$ before this week needed it. **Week 8's L26 §5** predicted Gram–Schmidt's failure. **Week 0's L03 §6–§7** supplied the rule of thumb that converts a condition number into digits — **and Week 0's Hilbert matrix turns out to have been polynomial fitting all along**, since $H_{ij} = \int_0^1 x^{i+j-2}dx$ is the Gram matrix of $1, x, x^2, \dots$

**Sideways:** **CS 201's and PROG 201's Project 1 are both due Friday.** Scheduling, not content — but it is a three-deadline afternoon and worth planning around.

**Forward:** **Week 10 is symmetric matrices**, and $A^\mathsf{T}A$ — the matrix at the centre of this week — is symmetric for every $A$ (Week 1's L06 §2). **Its eigenvalues and eigenvectors are what Week 11 calls the singular values and singular vectors**, so this week's central object is next week's subject. **Week 11's SVD handles the case this week cannot** — dependent columns, where $\hat x$ is not unique — via the pseudoinverse, and gives the third and most robust least-squares algorithm. **Week 12's PCA is least squares in disguise**, fitting a subspace rather than a function.

---

*MATH 241 · Week 9 · © CSE Department*
