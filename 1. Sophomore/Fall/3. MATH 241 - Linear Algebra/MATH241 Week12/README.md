# MATH 241 · Linear Algebra
## Week 12: Applications — Regression, PCA, PageRank, Fourier · Final Review

**Credits:** 4 (3 lecture + 1 recitation) · **Prerequisites:** MATH 141
**Assessment for this course (overall):** Problem Sets 35%, Midterms 40%, Final 25%
**This week's deliverables:** **PS 11 and PS 12 both due Friday 17:00**. PS 12 is released Wednesday and is short. **No quiz** — Quiz 11 was the last.
**Recitation 11 is sat this Thursday** — it covers **Week 11**. **Recitation 12**, the final review, is sat on the **Thursday of the completion period, Dec 11**.

> ## The last teaching week.
>
> **Friday Dec 5 is the heaviest afternoon of the term**: PS 11 and PS 12 here, the same two in every
> other course, and **Project 2 in CS 201, PROG 201 and CS 211**. None of it can move. **PS 12 is
> written to take an evening**, and the Problem Sets component drops your lowest mark.
>
> **The final is Monday Dec 15, 09:00–11:30**, VNC 100 with overflow to TH 200 — comprehensive,
> 100 marks, 25%. **It is the first final of the exam week.** See
> [[MATH241 Week12/resources/FINAL EXAM Revision Guide|FINAL EXAM Revision Guide]].

---

### Why This Week Exists

Because Week 0's syllabus made a promise on the first day — *a JPEG is a change of basis, PageRank is an eigenvector, least squares is a projection* — and a sentence like that should be cashed out, not repeated.

**Nothing this week is new mathematics.** Every application is Weeks 6–11 aimed at a problem someone actually has:

- **Regression** is Week 9's projection — and L36 measures what Week 9 could only warn about: **training error falls at every degree, while error on new data falls to $0.18$ and then rises to sixteen million.**
- **PCA** is Week 11's SVD of centred data — found a plane to within $1.09°$, and **computing it through the covariance matrix instead returned a negative variance.**
- **PageRank** is Week 6's eigenvector found by Week 7's powers — **exact on six pages, and converging at exactly the rate its second eigenvalue predicts.**
- **Fourier** is Week 8's orthonormal expansion in Week 2's space of functions — **with a squared error that goes to zero and an $18\%$ overshoot that never does.**

**And the syllabus said *all four are the same theorem.*** L38 §6 checks that claim rather than repeating it — **and finds it true of three.**

---

### Learning Objectives

By the end of Week 12, you should be able to:

1. **Explain overfitting** as a correct projection answering the wrong question, and distinguish it from ill-conditioning.
2. **Carry out PCA** by hand on centred data: directions, variance explained, and lost variance $= \sigma_{k+1}^2 + \cdots$.
3. **Say why the regression line and the principal line differ**, and which distance each minimises.
4. **Explain why PCA should be computed from the data, not the covariance matrix.**
5. **Set up PageRank**: the Markov matrix, dangling pages, and the damped matrix $G$.
6. **Predict power iteration's convergence** from $\lvert\lambda_2\rvert$, and explain the two failures damping prevents.
7. **Compute Fourier coefficients as projections**, and state what the partial sums do and do not converge to.
8. **Explain why a cosine basis compresses smooth signals**, and connect it to JPEG.
9. **Say which of the four applications is an orthogonal projection, and which is not.**
10. **Reconstruct the course's spine** — five factorisations, seven correct-but-unusable methods — from memory.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L36 Regression and PCA]] | **Training error against test error, measured**; a better basis fixes numerics, not overfitting; **PCA is the SVD of centred data**; **the regression plane is not the PCA plane**; the covariance route's negative variance |
| [[L37 PageRank]] | The recursive definition as an eigenvector; dangling pages and damping; **six pages, exactly**; **power iteration against $\lvert\lambda_2\rvert^k$**; **the cycle and the split web**; Perron–Frobenius; $6.7\times10^{14}$ times cheaper than elimination |
| [[L38 Fourier, and the Course in One Table]] | Functions as vectors; **coefficients as projections**; **Gibbs's $17.9\%$ that never goes**; the DCT and JPEG; **the four applications in one table**; **"the same theorem", checked**; the course backwards |
| [[REC 12 Final Review]] | **Week 10's matrix through all twelve weeks**; which tool for which problem; seven lessons with their numbers. **Thursday Dec 11** |
| [[PS 12 Synthesis]] | PCA, PageRank and Fourier **by hand**. Short. Due **Friday** |
| [[MATH241 Week12/assignments/FINAL EXAM\|FINAL EXAM]] | **Monday Dec 15, 09:00–11:30.** Eight questions, 100 marks |
| [[MATH241 Week12/resources/FINAL EXAM Revision Guide\|FINAL EXAM Revision Guide]] | The paper's structure, what is examinable, and what to put on your two pages |
| [[MATH241 Week12/resources/Reading Guide Week 12\|Reading Guide Week 12]] | Strang's applications, **Bryan & Leise on PageRank**, **Shlens on PCA** |
| `resources/applications.py` | Every number in L36–L38, reproducible |
| `solutions_instructor/` | Instructor only — including `final_check.py`, which asserts every number in the final's mark scheme |

---

### The One Thing to Take From This Week

**"All four are the same theorem" is true of three of them.**

| | Regression | PCA | Fourier | **PageRank** |
|---|---|---|---|---|
| **The theorem** | orthogonal projection | orthogonal projection, onto the best subspace | orthogonal projection, in a function space | **Perron–Frobenius** |
| **Orthogonality** | yes | yes | yes | **none** |
| **What made it work** | independent columns, or the SVD | nothing extra | nothing extra | **damping, engineered in** |

**Regression, PCA and Fourier are Week 8's L25, word for word**: the nearest point of a subspace is the projection, and the error is perpendicular. **PageRank is not** — its matrix is not symmetric, its eigenvalues are complex, no inner product appears anywhere, and it only has a unique answer because damping forces every entry positive.

> **What all four share is weaker and more useful — Week 4's L15 §7:** *find the basis in which the
> problem is simple.* **The same question, answered four ways, three of them by the same theorem.** A
> course that spent twelve weeks separating *true* from *true and usable* should end by separating
> *the same theorem* from *the same idea*, and L38 §6 does.

---

### Assessment Reminder

**No quiz this week.** Recitations 11 and 12 remain required.

**PS 11 and PS 12 are due Friday at 17:00.** The Problem Sets component (35%) drops your lowest of PS 0–12.

**The final is Monday Dec 15, 09:00–11:30, 25%** — the [[MATH241 Week12/resources/FINAL EXAM Revision Guide|Revision Guide]] gives its sections and weighting. **Two handwritten pages, no devices.** Prof. Abara's office hours in the completion period: **Monday Dec 8, 13:00–15:00** and **Thursday Dec 11, 10:00–11:00**, SSB 310.

Quizzes are tracked in [[_MATH 241 Quiz Record]].

---

### Connections

**Back:** **Every earlier week is used.** Week 0's L03 promised PageRank is not elimination; L37 §6 measures the gap at $6.7\times10^{14}$. Week 2's L07 said functions are vectors; L38 §1 gives them a dot product. **Week 6's L19 table** asked *what are the principal components?* and *what is PageRank?* — L36 §4 and L37 §3. **Week 7's L23 §5** gave the rate $\lvert\lambda_2\rvert$; L37 §4 measures it. **Week 8's L26 §1(c)** said Fourier series are *project onto each direction and add*; L38 §2 does it. **Week 9's L29 §4** warned that more columns always fit better; L36 §2 shows what that costs. **Week 10's spectral theorem** is PCA on a covariance matrix. **Week 11's Eckart–Young** is why PCA keeps the top singular vectors, and its L35 §5 total least squares is PCA in two dimensions.

**Sideways:** **CS 201, PROG 201 and CS 211 all have Project 2 due Friday**, and the completion period (Dec 8–12) is their demo week. **MATH 241 has no project** — use that week for revision, because this final is first.

**Forward:** **MATH 251** (Spring) is covariance, PCA and least squares as statistics. **ECE 211** (Spring) is Fourier for a term. **CS 331** assumes all twelve weeks and re-derives none of them — **and its first week is L36 §2's table.**

---

*MATH 241 · Week 12 · © CSE Department*
