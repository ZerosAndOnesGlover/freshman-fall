# MATH 241 · Reading Guide · Week 5
## Strang Chapter 5, and the last reading before Midterm 1

---

**Chapter 5 is short and Strang is in a hurry through it**, because the determinant's real job in his book is to produce $\det(A - \lambda I)$ in Chapter 6. **That is this course's view too** — L17 §5 says so explicitly — but it means the chapter rewards a slower reading than its length suggests.

| Chapter | Read? | Why |
|---|---|---|
| **5.1 The Properties of Determinants** | **All of it** | L16. He lists ten properties; ours are three, with the rest derived — **reconcile the two lists** |
| **5.2 Permutations and Cofactors** | **All of it** | L17 §1–§2. The $n!$ formula and the expansion |
| **5.3 Cramer's Rule, Inverses, and Volumes** | **All of it** | L17 §4 and L18. **The volume half is the important half** |
| 6.1 Introduction to Eigenvalues | **Skim the first two pages** | Week 6. Reading them Friday makes Monday easier |
| **Axler Ch. 10.A** | Optional | Determinants defined *from* eigenvalues rather than the reverse. Read it in Week 7, not now |
| **Goodfellow §2.11** | Read | Half a page, the determinant as a volume factor, ML framing |

---

## §5.1 — the questions to hold

1. **Strang's list has ten properties; L16 has three plus derivations.** Go through his ten and mark each as *(defining)* or *(derived)*. You should find his first three are our P1–P3.
2. He says the three defining properties determine the determinant **uniquely**. **Where does he prove it?** *(He mostly does not, and neither do these notes — L16 §2 flags it as a real theorem. Notice the gap rather than assuming you missed something.)*
3. Property: "if a matrix has a zero row, $\det = 0$". Prove it two ways — from linearity, and from the pivot product.
4. **Find his statement that adding a multiple of one row to another leaves $\det$ unchanged.** This is the property that makes elimination usable; L16 §3(c) calls it load-bearing. **Do you agree it is the most important of the ten?**
5. He notes $\det(A^\mathsf{T}) = \det A$ and says every row property is therefore a column property. **List which of his ten you now get for free.**

---

## §5.2

6. The $n!$ formula, with permutation signs. **Write out all six terms for a $3\times3$** and check you recover the diagonal mnemonic.
7. **Then satisfy yourself that the mnemonic fails for $4\times4$.** Count: how many terms should there be, and how many does the diagonal picture produce? *(24 against 8. This error appears every year.)*
8. Cofactors: $C_{ij} = (-1)^{i+j}\det M_{ij}$. **Where does the checkerboard of signs come from?** He derives it; follow the derivation rather than memorising the picture.
9. He observes you may expand along any row or column. **Which would you choose for a matrix with a nearly-empty third column?**
10. **The cost.** Does Strang give the operation count for cofactors against elimination? Compare with L17 §3's table, and with the measured 751× at $n = 8$.

---

## §5.3

11. **Cramer's rule.** Read the statement and the proof. Then read L17 §4's costing. **Strang is fonder of it than these notes are** — decide which view you hold, and be able to defend it.
12. The adjugate formula $A^{-1} = \operatorname{adj}(A)/\det A$. **Check the transpose**: is $\operatorname{adj}$ the cofactor matrix or its transpose? *(PS 5 Q3(a) turns on this.)*
13. **The volume section is the best part of the chapter.** He shows the three defining properties are the properties of area. **Draw his picture for P3** — two parallelograms sharing an edge — and satisfy yourself the areas add.
14. Find where he discusses the **sign** as orientation, and the connection to right- and left-handed frames in $\mathbb{R}^3$.
15. **The Jacobian.** Does he make the connection to change of variables? *(L18 §5 does it explicitly with polar coordinates. If he does not, you now know something the chapter left out.)*

---

## Before Midterm 1

**The paper is Wednesday of Week 6, 18:00–19:15, SSB 110, covering Weeks 0–5.** One handwritten sheet, one side.

**What belongs on the sheet**, in rough order of how often it is the thing people cannot recall:

- **The four-subspace diagram**, with $r$, $n-r$, $r$, $m-r$ and which $\mathbb{R}^k$ each lives in.
- **$[v]_{\text{old}} = M[v]_{\text{new}}$** — the direction of $M$, which no invariant will catch you getting wrong.
- **Which basis comes from $\operatorname{rref}$ and which from $A$**: rows from $\operatorname{rref}$, columns from $A$.
- **$\det(cA) = c^n\det A$**, and the pivot-product formula with its sign rule.
- **The seven equivalent characterisations of invertibility** (L16 §5's table).

**What does not belong on it:** anything you can derive in ten seconds. The rotation matrix, the $2\times2$ inverse, the cofactor sign pattern. **Space spent on those is space not spent on the four items above.**

> **A note on what the exam is actually testing.** Weeks 0–1 are computational and Weeks 2–5 are
> structural, and the structural material is where marks are lost — not because it is harder, but
> because a wrong answer there *looks right*. **A column space computed from $\operatorname{rref}$ is
> a perfectly respectable plane. A reversed $M$ is a perfectly respectable matrix.** Both are wrong,
> and neither announces itself. **The checks that catch them are in L08 §4 and REC 4 §2(f)**; know
> them, and run them.

---

## The Habit for This Week

**Before computing a determinant, look at the matrix for ten seconds.**

Is there a zero row or a repeated row? Is one row an obvious combination of others? Is there a row or column with three zeros in it? Is it triangular already? **Any of those answers the question faster than any algorithm**, and every one of them was a lecture in Week 5.

Ten seconds of looking is worth about three minutes of arithmetic on a typical exam matrix — and unlike the arithmetic, **looking does not have a sign error in it.**

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| **Strang, MIT 18.06, Lectures 18–20** | Properties, cofactors, and Cramer/volume. **Lecture 20 is L18** |
| **3Blue1Brown, *Essence of Linear Algebra*, episode 6** | The determinant as area, animated. Five minutes, and it is L18 §1 |
| **Axler Ch. 10** | Determinants introduced *after* eigenvalues, deliberately. **Read in Week 7**, when the contrast will mean something |
| **Week 6** | Where $\det(A - \lambda I)$ makes L17's symbolic cofactors the right tool after all |

---

*MATH 241 · Week 5 · Reading Guide · © CSE Department*
