# MATH 241 · Reading Guide · Week 7
## Strang §6.2, and the densest week in the course

---

**Week 7 assembles Weeks 1 through 6 and adds almost nothing new.** $A = S\Lambda S^{-1}$ is Week 4's change of basis with Week 6's basis; the proof is Week 1's column reading; the failure analysis needs Week 3's basis extension and Week 5's block determinants. **So the reading is short and the connections are the work.**

| Chapter | Read? | Why |
|---|---|---|
| **6.2 Diagonalizing a Matrix** | **All of it, twice** | L21 and L22. **The central section of the second half of the book** |
| **6.2, the Fibonacci example** | **Read carefully** | L23 §4. Strang does it at length and well |
| **6.4 Markov Matrices** *(or §10.3 in some printings)* | **Read** | L23 §5, and the PageRank connection |
| 6.2, complex examples | **Read** | L23 §1–§2 |
| **8.3 The Search for a Good Basis** | **Re-read** | You read it in Week 4 and skipped the eigenvalue paragraphs. **Read those now** |
| Jordan form appendix | **Skim, do not study** | L22 §3 — know it exists and why nobody computes it |
| **Axler Ch. 5.B–5.C** | Optional | Diagonalisability without determinants; good, and not needed for the exam |

---

## §6.2 — the questions to hold

1. **Strang's proof of $A = S\Lambda S^{-1}$ is the $AS = S\Lambda$ argument.** Reconstruct it before reading, using Week 1's L04 reading (ii). **Which side does $\Lambda$ multiply on, and why does that matter?**
2. He is careful that $S$ must be invertible. **Which earlier week supplies "independent columns $\Rightarrow$ invertible"?**
3. **Find his statement of the diagonalisability criterion.** Does he phrase it in terms of the two multiplicities, or in terms of counting independent eigenvectors? *(Both are correct and the second is easier to apply.)*
4. **The powers.** He derives $A^k = S\Lambda^kS^{-1}$ and uses it immediately. **Compare his cost discussion with L21 §4's table.**
5. He gives examples of matrices that are **not** diagonalisable. **For each, identify the eigenvalue whose eigenspace is deficient**, and check the algebraic multiplicity.
6. **Find where he says "diagonalisable" and "invertible" are unrelated.** Construct all four combinations: diagonalisable and invertible, diagonalisable and singular, non-diagonalisable and invertible, non-diagonalisable and singular. *(All four exist. This is a good five minutes.)*
7. **The Fibonacci example.** Work it yourself before reading his, and confirm you get Binet's formula. **Why is $\varphi$ an eigenvalue rather than a coincidence?**

---

## §6.4 / §10.3 — Markov matrices

8. **Why is $\lambda = 1$ always an eigenvalue?** Strang gives the column-sum argument. Reconstruct it, and say which Week 6 fact about $A$ and $A^\mathsf{T}$ it needs.
9. He shows every other eigenvalue satisfies $\lvert\lambda\rvert \le 1$. **Read the argument** — it is a good one and it is why Markov chains settle rather than blow up.
10. **Find the steady state.** Is it unique? *(It is, under a connectivity hypothesis he may or may not state. Notice whether he does.)*
11. **The rate of convergence.** Does he connect it to $\lvert\lambda_2\rvert$? *(L23 §5 does, and it is the practically important part — it is why PageRank takes about fifty iterations rather than ten thousand.)*

---

## The Jordan Form: Read Two Pages and Stop

**L22 §3 states it; Strang has an appendix.** What to take:

- **Every complex matrix is similar to a block-diagonal matrix of Jordan blocks.** It always exists and it is unique up to block order.
- **A matrix is diagonalisable exactly when every block is $1\times1$.**
- **Nobody computes it**, because the block structure is not stable under perturbation — L22 §4.

**Do not study the construction.** It is not examinable, it is not used again in this course, and the time is better spent on Week 8's orthogonality, which is used constantly from here to the end.

---

## The Habit for This Week

**Multiply it out.**

$$S\Lambda S^{-1} \stackrel{?}{=} A$$

**One matrix product, and it certifies the entire computation** — the eigenvalues, every eigenvector, the ordering, and the inverse.

**Nothing else will.** REC 7 §1(b) shows that swapping two of $\Lambda$'s diagonal entries while keeping $S$ produces a matrix with **the same trace, the same determinant, the same rank and the same eigenvalues** as $A$ — and it is not $A$. **Every similarity invariant is blind to the error**, for the structural reason that the wrong answer is similar to the right one.

**This is the second time this term the same trap has appeared.** Week 4's reversed $M$ was the first, and the resolution was identical: compute the thing you claim to have factored, and compare. **If you have taken the habit from Week 4, this week costs you nothing. If you have not, take it now** — Weeks 10 and 11 are two more factorisations and the trap does not go away.

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| **Strang, MIT 18.06, Lectures 22 and 24** | Diagonalisation and powers; then Markov matrices. **Lecture 22 is L21 almost exactly** |
| **3Blue1Brown, *Essence of Linear Algebra*, episode 14 (second half)** | Eigenbasis and diagonalisation, animated |
| **Brin & Page, *The Anatomy of a Large-Scale Hypertextual Web Search Engine* (1998)** | PageRank's original paper. **Readable now** — §2.1 is L23 §5 |
| **Axler Ch. 5.B–5.C, Ch. 8** | Diagonalisability, then generalised eigenvectors and the Jordan form done properly |
| **Weeks 10 and 11** | Where the hypothesis is removed rather than checked |

---

*MATH 241 · Week 7 · Reading Guide · © CSE Department*
