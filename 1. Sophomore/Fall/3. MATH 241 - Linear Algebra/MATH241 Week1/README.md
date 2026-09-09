# MATH 241 · Linear Algebra
## Week 1: Matrices — Operations, Transpose, Inverse

**Credits:** 4 (3 lecture + 1 recitation) · **Prerequisites:** MATH 141
**Assessment for this course (overall):** Problem Sets 35%, Midterms 40%, Final 25%
**This week's deliverables:** PS 1 (released Wednesday, due **Friday of Week 2**) and **Quiz 1** (Monday, covers Week 0). **PS 0 is due at 17:00 this Friday.**
**Recitation 0 is sat this Thursday** — it covers **Week 0**, and Recitation 1, covering this week, is sat on the **Thursday of Week 2**.

---

### Why This Week Exists

Because Week 0 treated $A$ as a *table you do things to*, and it is not. **It is a function, and this week is about the algebra of functions.**

Three questions, and the third is the one that pays:

1. **Why is matrix multiplication defined that way?** Not by convention. Requiring $(AB)x = A(Bx)$ — that $AB$ should *be* the composite function — forces the formula and the shape rule, with no choices left over.
2. **What is $A^{-1}$, and when does it exist?** Elimination already answered the second half in Week 0: when there are $n$ pivots. The lecture that matters is the one about **why you should almost never compute it**, which has three separate arguments and a table of measurements behind each.
3. **What was elimination actually doing?** It was factoring. **$A = LU$**, and $L$ is the multipliers you were told in Week 0 to write in the margin — no arithmetic required to build it. From there, a second right-hand side costs $0.6\%$ of the first.

By Friday you will have met **the first of the course's five factorisations** and will know why the other four exist.

---

### Learning Objectives

By the end of Week 1, you should be able to:

1. **Derive** the matrix multiplication formula from the requirement $(AB)x = A(Bx)$, and derive the shape rule with it.
2. Compute a product by all four readings — entries, columns, rows, outer products — and choose the right one for a given argument.
3. **Prove that every column of $AB$ is a combination of the columns of $A$**, in two lines, using the column reading.
4. Expand $(A+B)^2$ correctly, and state the exact condition under which it collapses.
5. Give matrices with $AB = 0$, $A \ne 0$, $B \ne 0$, and say what that costs the cancellation law.
6. Multiply in blocks, and see the four readings as special cases of one rule.
7. **Cost a matrix product at $2mnp$**, and choose the bracketing of a chain that minimises it.
8. Compute $A^{-1}$ by Gauss–Jordan, and state six conditions equivalent to invertibility.
9. **Give three independent arguments against computing an inverse to solve a system** — cost, accuracy, and sparsity — with a number attached to each.
10. Use $(AB)^{-1} = B^{-1}A^{-1}$ and $(AB)^\mathsf{T} = B^\mathsf{T}A^\mathsf{T}$, and reconstruct why both reverse.
11. **Prove $A^\mathsf{T}A$ is symmetric for any $A$**, in one line, and say where it reappears.
12. **Factor $A = LU$ by transcribing the multipliers**, solve with it by forward then back substitution, and produce $P$ when a row exchange is needed.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L04 Matrix Multiplication Four Ways]] | The definition **derived**, not stated; four readings of one product; $AB \ne BA$ in the smallest example; blocks; **$2n^3$ against elimination's $n^3/3$**; **$750\times$ fewer flops and $787\times$ faster from moving two brackets** |
| [[L05 The Inverse Gauss-Jordan and Why Not To Compute One]] | Uniqueness in one line; six equivalent conditions; Gauss–Jordan worked; the reversal rule; **six times the work, $2$–$91\times$ worse accuracy, and a tridiagonal matrix whose inverse has no zeros at all** |
| [[L06 Transposes Permutations and A = LU]] | $(Ax)\cdot y = x\cdot(A^\mathsf{T}y)$ as the real definition; **$A^\mathsf{T}A$ symmetric always**; elimination as matrix multiplication; **$A = LU$ with $L$ transcribed, not computed**; $PA = LU$; **$P^{-1} = P^\mathsf{T}$, your first orthogonal matrix** |
| [[REC 1 Building L and Never Inverting]] | Board work on the four readings and on where $P$ acts. **Thursday of Week 2** |
| [[PS 1 Matrices Inverses and the LU Factorization]] | Five questions, 100 points, due **Friday of Week 2** |
| [[MATH241 Week1/assignments/QUIZ 1 Week 1 Monday\|QUIZ 1 Week 1 Monday]] | Ten minutes, covers **Week 0**, answer key printed |
| [[MATH241 Week1/resources/Reading Guide Week 1\|Reading Guide Week 1]] | Strang §2.3–2.7, which section to read twice, and eighteen questions |
| `resources/matrices.py` | Every number in L04–L06, reproducible. Pure Python, no dependencies |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**$L$ is not computed. It is transcribed.**

Week 0 told you to write the multipliers in the margin and did not say why. The why is that those three numbers, dropped into a lower-triangular array with ones on the diagonal, **are a matrix satisfying $A = LU$** — and the elimination you already performed is the entire derivation. Nothing is calculated.

**Everything else this week is a consequence of taking that seriously.**

- $A^{-1}$ is $2n^3$; $LU$ is $n^3/3$; both cost $2n^2$ per solve afterwards. **So the inverse's extra work buys nothing at all**, and the six-times figure is the whole of L05 §6.
- $L$ and $U$ for our running matrix hold **6 nonzero integers**. $A^{-1}$ holds **9 fractions with denominator 24**. For the tridiagonal $K$, $L$ and $U$ keep the band and $K^{-1}$ has **not one zero entry** — at $n = 10^6$ that is 32 megabytes against 8 terabytes.
- And the factorisation generalises where the inverse does not. **$A = LU$ is the first of five**: $QR$, $S\Lambda S^{-1}$, $Q\Lambda Q^\mathsf{T}$, $U\Sigma V^\mathsf{T}$ are Weeks 7 through 11, every one the same move — **replace $A$ by factors you can solve with instantly.**

---

### Assessment Reminder

**Quizzes and the recitation carry no weight** and are still required. **Quiz 1 is at the start of Monday's lecture and covers Week 0**; the answer key is printed in the paper and you mark it yourself before leaving.

> **The recitation this week covers Week 0, not this week.** Recitation 0 is sat **this Thursday**,
> the day before PS 0 is due; **Recitation 1 covers Week 1 and is sat on the Thursday of Week 2**,
> the day before PS 1 is due. The lag is a full week from here on, because this course's Thursday
> session falls before its Friday lecture.

Quizzes are tracked in [[_MATH 241 Quiz Record]].

---

### Connections

**Back:** **Week 0's discarded arithmetic is this week's $L$.** The multipliers $2, -1, 3$ from L02 §4 are $L$'s subdiagonal; the transformed right-hand side $(1, 12, 12)$ from the same section is $L^{-1}b$, and L06 §5 recovers it by forward substitution. **Week 0's L03 §2 cost count is what makes L05 §6's argument bite** — without $n^3/3$ against $2n^3$ there is no case against inverting, only a preference.

**Sideways:** **CS 201 Week 2 is caches and the memory hierarchy**, and L04 §5's measured $787\times$ against a predicted $750\times$ is exactly the gap that course explains — the missing $5\%$ is eight megabytes of intermediate that does not fit in L2. **CS 201 Week 6's blocked matrix multiply is L04 §4's block rule with a cache attached.** The two courses have not been this close since Week 0 and will not be again this term.

**Forward:** **Week 2 is L04 §2's column reading taken seriously.** "Every column of $AB$ is a combination of the columns of $A$" becomes the column space; PS 1 Q1(c) is Week 3's $\operatorname{rank}(AB) \le \operatorname{rank}A$ with the vocabulary removed. **Week 5's determinant is the product of $U$'s pivots**, times $-1$ per row exchange — which is why $\det$ costs $n^3/3$ and not $n!$. **Week 8's projections are L05's exercise 6**, the matrices with $A^2 = A$. **Weeks 9, 10 and 11 all run through $A^\mathsf{T}A$**, whose symmetry L06 §2 proves in one line and whose consequences take three weeks. And **$P^{-1} = P^\mathsf{T}$ is the trivial case of the property that makes the second half of the course work**: Week 9 prefers $QR$ because $\operatorname{cond}(Q) = 1$, and that is this fact.

---

*MATH 241 · Week 1 · © CSE Department*
