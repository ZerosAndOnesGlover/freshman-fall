# MATH 241 · Reading Guide · Week 0
## Strang Chapters 1 and 2.1–2.3, and the two books you are not reading yet

---

**Week 0 is about sixty pages, and forty of them are Chapter 1**, which you will find easy. Do not skip it on that account — Strang uses Chapter 1 to install a vocabulary that the rest of the book leans on without re-explaining, and the column picture is introduced there rather than in Chapter 2.

| Chapter | Read? | Why |
|---|---|---|
| **1.1 Vectors and Linear Combinations** | **All of it** | This is L01 §4. The whole course is here in miniature |
| **1.2 Lengths and Dot Products** | **Read** | You need the dot product now as notation. **Its geometry is Week 8** — do not chase the projection material yet |
| **1.3 Matrices** | **All of it** | Strang's own transition from combinations to $Ax = b$ |
| **2.1 Vectors and Linear Equations** | **All of it** | The row picture and the column picture side by side. L01 |
| **2.2 The Idea of Elimination** | **All of it, twice** | L02, entire. The most important six pages in the first half of the book |
| 2.3 Elimination Using Matrices | **Skim** | Correct and premature. It says elimination *is* matrix multiplication, which needs Week 1's L04. Come back on the Friday of Week 1 |
| 2.4 – 2.7 | Not yet | Week 1 |
| **9.1 Gaussian Elimination in Practice** | **Read** | L03 §5. Short, and the pivoting rule is stated properly |
| **9.2 Norms and Condition Numbers** | **Read the first three pages** | L03 §7. Stop at the matrix-norm inequalities; you will meet them again in Week 8 with the geometry to make them mean something |
| **Axler Ch. 1** | **Optional, recommended** | Twenty pages, and a completely different temperament. Worth knowing that the other book exists before you need it in Week 3 |
| **Goodfellow Ch. 2.1–2.4** | **Read** | Fifteen pages. Where this is all going, in ML notation. Free at deeplearningbook.org |

---

## Chapter 1 — the questions to hold

**§1.1**

1. Strang asks what the combinations $c\mathbf{u} + d\mathbf{v}$ fill out, for two vectors in $\mathbb{R}^3$. Answer for three cases: $\mathbf{u}, \mathbf{v}$ pointing in different directions; $\mathbf{v} = 2\mathbf{u}$; $\mathbf{v} = \mathbf{0}$. **You have just described the three things a two-column matrix's column space can be** — Week 2's whole subject, three weeks early.
2. He writes "linear combination" perhaps thirty times in this section. Write your own definition, in one sentence, without looking. Keep it; Week 3 will ask you to defend it.

**§1.2**

3. The dot product $\mathbf{u}\cdot\mathbf{v}$ is defined here by a formula and interpreted by an angle. **Which of the two is the definition?** The answer is not obvious and Week 8 argues about it.
4. What does $\mathbf{u}\cdot\mathbf{v} = 0$ mean geometrically? Note the answer; do not pursue it.

**§1.3**

5. Strang writes $A\mathbf{x}$ as a combination of columns *before* he writes it as rows dotted with $\mathbf{x}$, and says explicitly that he is doing so deliberately. **Why?** (L01 §4 gives one reason. He has another, about what generalises.)
6. Find his "difference matrix" example and work out what its inverse does. He is showing you calculus in disguise; identify which operation.

---

## Chapter 2 — the questions that matter

**§2.1**

7. Draw the row picture and the column picture for Strang's $2\times2$ example. Then answer honestly: **which one did you understand faster, and which one do you think you could still draw for $n = 6$?**
8. He gives a $3\times3$ system whose three planes have no common point but do meet in pairs. Sketch it. This is the case people forget on exams.

**§2.2 — read this section twice**

9. Strang's word for the multiplier is $\ell$, and the notes' is the same. In $R_i \leftarrow R_i - \ell_{ik}R_k$, **which index is the row being changed and which is the pivot row?** Get this the right way round now; Week 1's $L$ makes the convention load-bearing.
10. **"Breakdown" and "failure" are different words in this section, and he means different things by them.** Find both, and say which is repaired by a row exchange.
11. He counts the operations at the end. Reproduce the count yourself before reading his — L03 §2 derives it — and check that you agree on the $n^3/3$.
12. He remarks that elimination on a $3\times3$ can be done "in your head, badly". Do the exercise he offers immediately after, on paper, well.

**§2.3 — skim only, and know why**

13. This section's claim is that each elimination step is *multiplication by a matrix* $E_{ik}$. It is true and it is Week 1's L06. **Read the first two pages so the idea is not new when it arrives, and go no further.** You do not yet know why matrix multiplication is defined the way it is, and §2.3 assumes you do.

**§9.1–9.2**

14. Strang's roundoff example is not the one in L03 §4 — he uses a different $\varepsilon$ and a different pair of equations. **Work through his and then ours.** Two instances of one failure is what makes it a pattern rather than a trick.
15. He defines the condition number and immediately says most people never compute it. Both halves are true. **Why is it worth knowing a number you will not compute?**

---

## The Habit for This Week

**Predict the pivots before you eliminate.**

Look at the matrix, guess what the three pivots will be and whether any row exchange will be needed, **write the guess down**, and then run the algorithm. You will be wrong for the first fortnight, and each way of being wrong is informative in a different way: a sign error is arithmetic, a missed row exchange is not looking at column 1, and a wrong count of pivots means you did not see the dependency.

**A prediction you did not write down is a prediction you will remember having got right.**

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| **Strang, MIT 18.06 on OCW** | Lectures 1 and 2 are this week, delivered aloud. He says things at the board that are not in the book — particularly about the column picture |
| **Trefethen & Bau, *Numerical Linear Algebra*, Lectures 20–22** | L03 §4–§7 done properly, including the growth-factor bound partial pivoting does *not* give you |
| **Higham, *Accuracy and Stability of Numerical Algorithms*, Ch. 9** | The definitive treatment. Reference, not reading |
| **CS 201 Week 1** | Running next week, and it is L03 §4's mechanism: IEEE 754, and why floating-point addition is not associative |

---

*MATH 241 · Week 0 · Reading Guide · © CSE Department*
