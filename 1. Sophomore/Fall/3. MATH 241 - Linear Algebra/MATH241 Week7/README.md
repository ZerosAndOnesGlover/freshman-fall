# MATH 241 · Linear Algebra
## Week 7: Diagonalization and Complex Eigenvalues

**Credits:** 4 (3 lecture + 1 recitation) · **Prerequisites:** MATH 141
**Assessment for this course (overall):** Problem Sets 35%, Midterms 40%, Final 25%
**This week's deliverables:** PS 7 (released Wednesday, due **Friday of Week 8**) and **Quiz 7** (Monday, covers Week 6). **PS 6 is due at 17:00 this Friday.**
**Recitation 6 is sat this Thursday** — it covers **Week 6**. Recitation 7, covering this week, is sat on the **Thursday of Week 8**.

> **Back to a normal week**, and back to Monday quizzes — last week's Tuesday quiz was the Fall Break
> exception. **Midterm 1 papers are returned this week.**
>
> **This is the densest week in the course.** It assembles Weeks 1 through 6 and introduces almost
> nothing new, which makes it deceptively easy to read and hard to do.

---

### Why This Week Exists

Because Week 4 set out a programme and this is the first row of the table.

$$\text{Given } T\text{, find a basis in which its matrix is as simple as possible.}$$

**Week 6 found the basis** — the eigenvectors are the directions the map does not turn. **Week 7 assembles it**, and the assembly is nothing more than Week 4's change of basis with $M = S$:

$$A = S\Lambda S^{-1}$$

**The proof is one line** — $AS = S\Lambda$, read column by column, which is Week 1's L04 reading (ii) — and **the hypothesis is the whole content.** $S$ must be invertible, which means the eigenvectors must be independent, which means there must be $n$ of them. **Week 6's defective matrices do not have them**, and L22 is what that costs.

**What the factorisation buys is powers.** $A^k = S\Lambda^kS^{-1}$, and $\Lambda^k$ is $n$ scalar powers — **a cost that does not grow with $k$ at all**, against $O(\log k)$ matrix products for repeated squaring. Week 1's L04 §6 promised this and could not deliver it; here it is.

**And that is why the applications are not decoration.** Fibonacci's closed form, a Markov chain's steady state, and the stability of any linear iteration are all the same computation: **raise the eigenvalues to the $k$-th power and see what survives.** L23 §5 closes the loop Week 0 opened — **PageRank is fifty matrix–vector products**, not a linear solve, because the answer wanted is an eigenvector.

---

### Learning Objectives

By the end of Week 7, you should be able to:

1. **State and prove $A = S\Lambda S^{-1}$**, identifying where the independence hypothesis is used.
2. Assemble $S$ and $\Lambda$ in a consistent order, and **verify by multiplying out.**
3. **Say why $S\Lambda S^{-1} = A$ is the only available check** — every similarity invariant is blind to an ordering error.
4. Compute $A^k$ and $A^{-1}$ from the factorisation, and say what each requires of the eigenvalues.
5. **State the diagonalisability criterion** and apply it to a matrix with a repeated eigenvalue.
6. **Prove geometric $\le$ algebraic**, using basis extension and a block determinant.
7. **Explain why defectiveness is not a matter of degree**, and hence why no algorithm tests for it.
8. State what the Jordan form says, **and why nobody computes it.**
9. **Handle complex eigenvalues:** conjugate pairs, and $r = \sqrt{\det}$, $\cos\theta = \operatorname{trace}/(2\sqrt{\det})$.
10. **Use $\lvert\lambda\rvert$ to decide the fate of an iteration**, and define the spectral radius.
11. **Derive a closed form for a linear recurrence**, and say why the golden ratio appears in Fibonacci.
12. **Find a Markov chain's steady state, and say what governs the mixing rate.**

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L21 Diagonalization]] | $A = S\Lambda S^{-1}$, proved in one line from $AS = S\Lambda$; **it is Week 4's change of basis with $M = S$**; assembled on Week 6's matrix; **$A^k$ at a cost that does not grow with $k$**; $e^{At}$; distinct eigenvalues are sufficient and not necessary; **$\Lambda$ as a canonical form** |
| [[L22 When Diagonalization Fails]] | The criterion; **geometric $\le$ algebraic proved** from Weeks 3, 4 and 5; **what is there instead of a missing eigenvector**; the Jordan form stated and its uselessness explained; **defective at $\varepsilon = 10^{-300}$, diagonalisable at $0$, no transition**; the classes that never fail; **differentiation is not diagonalisable** |
| [[L23 Complex Eigenvalues and Powers in Practice]] | Conjugate pairs; **$r$ and $\theta$ from trace and determinant alone**; **$\lvert\lambda\rvert$ decides everything**, measured on three spirals; **Binet's formula as $S\Lambda^kS^{-1}$ read off**; Markov steady states; **the mixing rate is $\lvert\lambda_2\rvert$, and PageRank is fifty iterations** |
| [[REC 7 Assembling S and Lambda]] | Board work on three matrices with three outcomes, and the ordering trap. **Thursday of Week 8** |
| [[PS 7 Diagonalization and Complex Eigenvalues]] | Five questions, 100 points, due **Friday of Week 8** |
| [[MATH241 Week7/assignments/QUIZ 7 Week 7 Monday\|QUIZ 7 Week 7 Monday]] | Ten minutes, covers **Week 6**, answer key printed |
| [[MATH241 Week7/resources/Reading Guide Week 7\|Reading Guide Week 7]] | Strang §6.2 twice and §6.4, **the Jordan form in two pages**, and eleven questions |
| `resources/diagonalize.py` | Every number in L21–L23, reproducible. Fibonacci, a Markov chain, and three spirals |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Multiply it out. Nothing else will catch the error.**

$$S\Lambda S^{-1} \stackrel{?}{=} A$$

Take the correct $S$ and $\Lambda$ for $\begin{bmatrix}1&2\\4&3\end{bmatrix}$ and **swap only the two diagonal entries of $\Lambda$.** You get

$$\begin{bmatrix}3&-2\\ -4&1\end{bmatrix}$$

**which has the same trace, the same determinant, the same rank, the same characteristic polynomial and the same eigenvalues as $A$** — and is not $A$.

**Every similarity invariant is blind to it**, and for a structural reason rather than a coincidence: **the wrong answer is *similar* to the right one.** No quantity preserved by similarity can possibly distinguish them.

> **This is the second time this term.** Week 4's reversed $M$ was the first, with the same structure
> and the same resolution: **compute the thing you claim to have factored, and compare.** Weeks 10
> and 11 are two more factorisations, and the trap does not go away — **so take the habit now.**

---

### Assessment Reminder

**Quizzes and the recitation carry no weight** and are still required. **Quiz 7 is at the start of Monday's lecture and covers Week 6** — back to Monday after the Fall Break exception.

Quizzes are tracked in [[_MATH 241 Quiz Record]].

---

### Connections

**Back:** **This week is Weeks 1–6 assembled.** The proof of $A = S\Lambda S^{-1}$ is **Week 1's L04 reading (ii)**; the factorisation is **Week 4's L15 §4 with $M = S$**; the basis is **Week 6's**; L22's geometric $\le$ algebraic needs **Week 3's basis extension, Week 4's change of basis and Week 5's block determinants**; and $\Lambda$ being a canonical form finishes **PS 4 Q5(d)**, open since Week 4. **Week 1's L04 §6 promised $A^k = S\Lambda^kS^{-1}$** and had to defer it for six weeks.

**Sideways:** **CS 201's Project 1 is assigned this week** (mini-CPU simulator, due Week 9) and PROG 201's Project 1 is due in Week 9 too. **Neither connects to this material**, and Week 7 is dense enough without looking.

**Forward:** **Week 8 is orthogonality**, and it is the answer to L22 §4's problem: when $S$ is nearly singular the factorisation is numerically worthless, and **an orthonormal basis has $\operatorname{cond}(S) = 1$ exactly.** **Week 10 removes the hypothesis entirely for symmetric matrices** — never defective, eigenvectors orthogonal, $S^{-1} = S^\mathsf{T}$ — which is why L22 §6's table has *always* in that row. **Week 11's SVD removes it for every matrix**, by allowing a different basis at each end, which similarity forbids and which Week 4's L14 §1 permitted from the start. **Week 12's PageRank and PCA are both L23 §5**, on matrices of size $10^9$ and on covariance matrices respectively.

---

*MATH 241 · Week 7 · © CSE Department*
