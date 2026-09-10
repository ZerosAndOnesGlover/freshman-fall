# MATH 241 · Reading Guide · Week 6
## Strang §6.1, and a two-lecture week

---

**Week 6 has two lectures instead of three** — Fall Break took the Monday — so the reading carries more of the load than usual. **§6.1 is long and repays it**; read it in two sittings rather than one.

| Chapter | Read? | Why |
|---|---|---|
| **6.1 Introduction to Eigenvalues** | **All of it, twice** | L19 and L20 together. **Strang's best section** |
| 6.2 Diagonalizing a Matrix | **Skim the first three pages** | Week 7. Reading them this weekend makes Monday much easier |
| **5.1, the paragraph on $\det(A - \lambda I)$** | **Re-read** | You read it last week without knowing what it was for |
| **Axler Ch. 5.A** | **Read** | Eigenvalues **without determinants**, which is a genuinely different approach — see below |
| **Goodfellow §2.7** | Read | Eigendecomposition in ML notation, two pages |

---

## §6.1 — the questions to hold

1. Strang opens with $Ax = \lambda x$ and immediately asks what is special about $x$. **Write your own one-sentence answer before reading his.**
2. He derives $\det(A - \lambda I) = 0$ from the requirement that $A - \lambda I$ be singular. **Check you can reconstruct that chain**: eigenvector exists $\Rightarrow$ nontrivial null space $\Rightarrow$ singular $\Rightarrow$ zero determinant. Four steps, each from a different week.
3. **Find where he says the eigenvalues of a triangular matrix are on the diagonal.** Why is this immediate?
4. His examples include a projection and a reflection. **Predict the eigenvalues from the geometry before reading the arithmetic** — L19 §5's habit.
5. Strang uses $\det(A - \lambda I)$; some books use $\det(\lambda I - A)$. **Which does he use, and what would change?** *(Only the overall sign, for odd $n$. But check before comparing coefficients with any other source.)*
6. **Find the trace and determinant identities.** He states them early and uses them constantly as checks. **Adopt the habit this week, not later.**
7. He discusses a rotation with complex eigenvalues. **Does he treat this as a defect or as normal?** *(Normal — and Week 7 agrees. Anything that oscillates has complex eigenvalues.)*
8. **The hardest thing in the section is the distinction between the two multiplicities.** Find where he introduces it. Does he use the words *algebraic* and *geometric*? *(He may say "repeated eigenvalue" and "missing eigenvector" instead. **The idea matters; the vocabulary is ours.**)*

---

## §6.2, first three pages only

9. He states that $n$ independent eigenvectors give $A = S\Lambda S^{-1}$. **This is Week 4's L15 §7 first row**, and the change of basis is the one you already know. Read far enough to see the shape and stop.
10. **Find the condition for diagonalisability** and check it against L20 §5's definition of *defective*. They should be the same statement.

---

## Where Axler Earns His Place This Week

**Axler's Chapter 5 develops eigenvalues with no determinants at all**, and he argues at length that this is the right way round — his book is called *Linear Algebra Done Right* largely on the strength of that choice.

| Axler | Why bother |
|---|---|
| **5.A** invariant subspaces and eigenvalues | Defines an eigenvalue as a $\lambda$ making $T - \lambda I$ **not injective** — no determinant anywhere |
| **5.A**, existence over $\mathbb{C}$ | Proves every operator on a complex space has an eigenvalue, **without the fundamental theorem of algebra**. Elegant, and short |

**Read 5.A after L20, not before.** The determinant route is the one you need for computation and for this course's exams; Axler's is the one that explains why eigenvalues exist at all. **Meeting the computational version first and the conceptual one second is the right order** — the reverse leaves you unable to find an eigenvalue.

> **And it puts Week 5 in perspective.** Axler gets to eigenvalues in Chapter 5 having never defined
> a determinant; he introduces determinants in Chapter 10, *from* the eigenvalues. **Two coherent
> orderings of the same subject.** This course takes Strang's because it is the computational one,
> and the reading guide flags the alternative so that you know it is a choice.

---

## The Habit for This Week

**Run the trace and determinant checks. Every time. Without exception.**

You have computed eigenvalues $\lambda_1, \dots, \lambda_n$. **Add them: is the sum the trace? Multiply them: is the product the determinant?**

- The trace is the diagonal sum — **read off, no computation.**
- The determinant is $p(0)$, the constant term of a polynomial **you have already computed.**

**So both checks are free**, they are independent of each other, and between them they catch nearly every arithmetic error a $2\times2$ or $3\times3$ admits. **There is no other place in this course where two free, independent checks are available**, and students who do not use them lose marks to errors they could have found in five seconds.

**Then check each eigenvector too**, with one $Av$ product. **Three checks, under a minute, and the computation is certified.**

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| **Strang, MIT 18.06, Lecture 21** | Eigenvalues and eigenvectors. His examples differ from the notes' — do both |
| **3Blue1Brown, *Essence of Linear Algebra*, episode 14** | Eigenvectors animated, including **why a rotation has none**. Ten minutes, and it is L19 §5–§6 |
| **Axler Ch. 5.A** | The determinant-free development |
| **Week 7** | Diagonalisation: what the two multiplicities were for |
| **Week 12** | PageRank and PCA, both of which are the dominant eigenvector of something |

---

*MATH 241 · Week 6 · Reading Guide · © CSE Department*
