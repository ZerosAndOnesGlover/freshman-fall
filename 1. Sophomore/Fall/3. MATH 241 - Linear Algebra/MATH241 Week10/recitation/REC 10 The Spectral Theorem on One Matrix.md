# MATH 241 · Recitation 10
## The Spectral Theorem on One Matrix
### Covers Week 10 · sat **Thursday of Week 11**, 15:00–15:50, SSB 108 · **unmarked, attendance required**

---

> **Midterm 2 papers are returned this week.** Bring yours. **§5 is the post-mortem** and it is the
> last item, deliberately — **the mathematics comes first while everyone can still concentrate.**
>
> **PS 10 is due at 17:00 tomorrow.** Come with your attempt.
>
> **Quiz 11 was Monday and was the last quiz of the term.**

**What this session is.** Fifty minutes on **one** symmetric matrix, taken apart four ways. Every number is a small integer or a clean fraction, and **every claim of Week 10 is checkable on it by hand** — which is the point. The spectral theorem is short enough to state in a sentence and long enough to hide in; doing it once completely is worth reading it three times.

**What to bring:** paper, your PS 10 attempt, your midterm paper, one laptop per pair for §4.

---

## 0. Before You Come (10 minutes, at home)

For

$$A = \begin{bmatrix}9&-4&0\\ -4&7&-4\\ 0&-4&5\end{bmatrix},$$

**verify that $(1,2,2)$, $(2,1,-2)$ and $(2,-2,1)$ are eigenvectors, and find the three eigenvalues.**

**Bring the three products $A u_k$ written out.** *(Three matrix–vector multiplications. No characteristic polynomial, no elimination — you are being handed the eigenvectors precisely so that the session can start at the interesting part.)*

---

## 1. The Drill (10 min)

**In pairs, compare.** Expect $\lambda = 1$, $7$, $13$ in that order.

**(a)** Check $\operatorname{trace}A = 21 = 1 + 7 + 13$ and $\det A = 91 = 1 \times 7 \times 13$. **Which week gave you each of these, and do they hold for non-symmetric matrices too?**

**(b)** Compute the three pairwise dot products of the eigenvectors. **State the theorem that made this a foregone conclusion**, and say exactly where symmetry entered its two-line proof.

**(c)** All three eigenvectors have length $3$. **Is that a theorem or a convenience?** Answer honestly — this matters, because it is why $Q$ is rational here and irrational almost everywhere else.

**(d)** Write $Q$ and $\Lambda$. **Then write $Q^{-1}$, and say how long it took.** *(This is the entire practical content of Week 10 and it should take you four seconds.)*

---

## 2. Four Things at Once (15 min)

Still on the same $A$.

**(a) [spectral]** Verify $Q^\mathsf{T}Q = I$ in exact fractions. **All nine entries.** Then verify $Q\Lambda Q^\mathsf{T} = A$ for the $(1,1)$ and $(1,2)$ entries only, and say why checking two entries of a symmetric product is more than it sounds.

**(b) [projections]** Compute $P_1 = q_1q_1^\mathsf{T}$ as a matrix of ninths. **Verify $P_1^2 = P_1$ and $\operatorname{trace}P_1 = 1$.** Then, *without computing them*, state $\operatorname{trace}(P_1 + P_2 + P_3)$ and $P_1P_2$, with a reason for each.

**(c) [elimination]** Eliminate $A$ by hand and record the pivots. **You should get $9$, $\tfrac{47}{9}$, $\tfrac{91}{47}$.** Check their product against $\det A$, and check each pivot against the ratio of consecutive leading minors $9$, $47$, $91$.

**(d) [positive definite]** **Four different tests are now on your paper.** List which ones, what each says, and note that **you did not run any of them on purpose** — they fell out of work you were doing for other reasons. *(That is the practical lesson: a symmetric matrix tells you whether it is positive definite while you are doing something else with it.)*

---

## 3. The Boundary, and the Trap (10 min)

**(a)** Replace the corner entry $A_{11} = 9$ by a parameter $s$. Compute $\det$ as a function of $s$ and find **exactly** the value at which the matrix stops being positive definite. *(The two smaller leading minors change too — do not assume they are fixed.)*

**(b)** At that critical $s$, **exhibit a nonzero vector $x$ with $x^\mathsf{T}Ax = 0$.** Where does it live, in Week 2's vocabulary? What eigenvalue does it belong to, in Week 6's?

**(c) The trap, and it is on every exam.** $\begin{bmatrix}1&3\\3&1\end{bmatrix}$ has both diagonal entries positive. **Is it positive definite?** Find its eigenvalues and its pivots, then **find an explicit $x$ with $x^\mathsf{T}Ax < 0$.** *(Do not stop at "the eigenvalues say no". The vector is the proof, it takes one guess, and producing it is what an examiner is checking for.)*

**(d)** $\begin{bmatrix}1&2&2\\2&1&2\\2&2&1\end{bmatrix}$ has positive diagonal **and** positive determinant. **Is it positive definite?** *(Compute the three leading minors. Then say which test your colleague in the problem was half-remembering.)*

---

## 4. Ten Minutes With a Machine (10 min)

One laptop per pair. Run `resources/symmetric.py` from the Week 10 folder.

**(a)** Look at **§12's second table**. At $n = 10$, $\varepsilon = 10^{-10}$: a matrix is changed in **one entry** by $10^{-10}$ and every eigenvalue moves from $0$ to magnitude $0.1$. **Say out loud what the amplification factor is.**

**(b)** Look at **§12's first table** immediately above it. **State the contrast in one sentence**, and name the hypothesis that separates the two halves.

**(c)** In **§10**, find $\lambda_\min(H_{12})$. **Now find the sentence in the script that tells you not to believe its digits**, and say what you are entitled to conclude from the number anyway.

> **(c) is the habit the whole term has been building.** A number that is reproducible, correctly
> computed, and untrustworthy in its last twelve digits is a normal object, not a scandal —
> **provided you say so where you print it.**

---

## 5. Midterm Post-Mortem and Clinic (whatever is left)

**Papers are returned this session.**

**Bring:** the question you lost the most marks on, and your PS 10 attempt.

**The TA will:**

- work the **method** of any midterm question, with **different numbers**;
- take PS 10 questions, especially Q2 and Q5(c);
- point you at office hours for anything about **your own** mark.

**The TA will not** discuss the mark scheme or confirm individual answers. **Marks are Prof. Abara's** — office hours Thursdays 10:00–11:00, SSB 310. The Help Desk is BH 120.

> **If the paper revealed a gap in Weeks 6–9, raise it now.** Week 11's SVD is built directly on
> Week 7's diagonalisation and Week 10's spectral theorem, and **the final is comprehensive.**
> Six weeks of accumulated confusion is a bad thing to discover in December.

---

*MATH 241 · Week 10 · REC 10 · unmarked*
