# MATH 241 · Reading Guide · Week 1
## Strang §2.3–§2.7, and the section that is worth reading twice

---

**Week 1 is the second half of Chapter 2, and it is where the book gets good.** §2.4 is the section that justifies the definition you have been using since school without ever being told why it is that definition, and §2.6 is the one whose title — *"Elimination = Factorization: $A = LU$"* — is the single most useful equals sign in the first half of the course.

| Chapter | Read? | Why |
|---|---|---|
| **2.3 Elimination Using Matrices** | **All of it, now** | You skimmed it in Week 0 because it needed matrix multiplication. It has it now. L06 §3 |
| **2.4 Rules for Matrix Operations** | **All of it, twice** | L04. **The four readings are here**, and Strang gives them in a different order than these notes do |
| **2.5 Inverse Matrices** | **All of it** | L05. His Gauss–Jordan worked example is worth doing alongside ours on a different matrix |
| **2.6 Elimination = Factorization** | **All of it** | L06 §4–§5. Read the last two pages, on cost, especially carefully |
| **2.7 Transposes and Permutations** | **All of it** | L06 §1, §2, §6. Short |
| 3.1 Spaces of Vectors | **Skim the first two pages** | Week 2. Read it Friday evening and Week 2 will start faster |
| **Goodfellow §2.3** | **Read** | Four pages on the inverse, from the machine learning side. Notice what he says about *not* computing it |
| Axler Ch. 3 | Optional | Linear maps done abstractly. It will not help this week and will help enormously in Week 4 |

---

## §2.3 — the questions to hold

1. Strang's $E_{ij}$ and these notes' $E_{ij}$ are the same matrices. **Check the sign convention agrees** — is the multiplier in the matrix $+\ell$ or $-\ell$? Get this straight before §2.6 or $L$ will come out wrong.
2. He introduces the **augmented matrix** as a way of doing $A$ and $b$ at once, and then observes that the same trick with $I$ instead of $b$ gives the inverse. That is one idea used twice; make sure you see it as one.

---

## §2.4 — read this twice

3. **Find all four ways of viewing $AB$.** Strang numbers them; these notes call them readings (i)–(iv). Write down which of his corresponds to which of ours. *(They are not in the same order, and matching them up is the exercise.)*
4. He proves associativity of $ABC$ and calls the proof "the most important" of the section. **Do you agree?** Consider what breaks if it fails.
5. **Block multiplication.** He gives it late in the section and it looks like a footnote. Work out how each of the four readings is a special case of it — the cuts are different in each case.
6. Find his operation count for $AB$. Compare with the $n^3/3$ from Week 0's L03 §2. **Which is larger, and by what factor?** Keep the answer for L05 §6.

---

## §2.5

7. Strang's list of conditions equivalent to invertibility grows through the book; the version in §2.5 is short. **Write it down now, and keep the page.** By Week 5 you will have seven and by Week 11 you will have more.
8. His Gauss–Jordan example is a different matrix from L05 §4's. **Do both.** Two is what makes it a procedure rather than a memory.
9. He observes that $A^{-1}$ of a **tridiagonal** matrix is full. Find that remark. *(L05 §7 measures it: 13 nonzeros in, 25 out.)*
10. **The question he does not ask, and you should:** he shows you how to compute an inverse and then, later in the book, tells you not to. Find both passages and reconcile them in one sentence.

---

## §2.6 — the payoff

11. **Before reading:** take the $3\times3$ you eliminated for PS 0 Q1(a) and write the three multipliers in a lower-triangular array with ones on the diagonal. Then read Strang's derivation and check that he gets your array.
12. He is careful about **why the multipliers land in $L$ without interfering with each other**, and this is the subtle step. Follow it. *(PS 1's Q4 does not test it; L06 §4's parenthetical does, and so does exercise 4 of that lecture.)*
13. **§2.6's cost paragraph is the most practically useful in the chapter.** He gives the cost of factoring and the cost of each subsequent solve. Write both down. They are the answer to PS 0 Q4(a) and PS 1 Q4(b).
14. Find where he says $A = LDU$ with $D$ the pivots pulled out and $U$ having unit diagonal. **What is the point of this variant?** *(Hint: it makes the symmetric case say something. Week 10.)*

---

## §2.7

15. $(AB)^\mathsf{T} = B^\mathsf{T}A^\mathsf{T}$ — Strang proves it by indices. **These notes prove it by shapes first** (L06 §1). Which argument would you reconstruct under exam conditions?
16. He states that $A^\mathsf{T}A$ is symmetric and square for **every** $A$, and immediately says it will "be important later". It is Weeks 9, 10 and 11. **Prove it yourself in one line before reading his.**
17. Permutation matrices: he notes $P^{-1} = P^\mathsf{T}$. **Prove it** rather than accepting it — L06 §6 has the argument, and it is the first orthogonal matrix you will meet.
18. How many $n\times n$ permutation matrices are there? He says. Confirm the reasoning.

---

## The Man Pages of This Week

Numerical linear algebra has documentation and it is worth reading like documentation:

| Read | For |
|---|---|
| `numpy.linalg.solve` docs | Note that it takes a matrix right-hand side, and factors once. This is PS 1 Q5(c) |
| `numpy.linalg.inv` docs | **Read the note telling you not to use it for solving.** Every library has one |
| `scipy.linalg.lu_factor` / `lu_solve` | The two-step form. Note what `lu_factor` returns and that `piv` is $P$ — L06 §6 |
| LAPACK `dgetrf` documentation | One page. `ipiv` is the permutation, stored as $n$ integers rather than $n^2$ zeros and ones |

---

## The Habit for This Week

**Write down which reading you are using.**

When you compute a product, prove something about one, or read a formula containing one, **say which of the four readings you are in** — entries, columns, rows, or outer products. Out loud, or in the margin.

It feels laborious for about a week. Then it stops being conscious, and you will find you have started reaching for the right one automatically: the column reading for anything about solvability, the row reading for anything about elimination, the outer-product reading for anything about approximation. **Week 11's SVD is unreadable without that last reflex**, and this is the week to start building it.

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| **Strang, MIT 18.06, Lectures 3–4** | This week aloud. Lecture 4 is $A = LU$ and is the best fifty minutes on it anywhere |
| **Golub & Van Loan, *Matrix Computations*, Ch. 3** | $LU$ done properly: pivoting strategies, growth factors, blocked algorithms. Reference |
| **Trefethen & Bau, Lectures 20–22** | $LU$ and pivoting with the numerical analysis foregrounded |
| **CS 201 Week 6** | Why blocked matrix multiply is faster than the triple loop, which is L04 §4 from the hardware's side |
| **CS 102, matrix chain multiplication** | You solved L04 §5's bracketing problem in Year 1 by dynamic programming. This is what the $2mnp$ meant |

---

*MATH 241 · Week 1 · Reading Guide · © CSE Department*
