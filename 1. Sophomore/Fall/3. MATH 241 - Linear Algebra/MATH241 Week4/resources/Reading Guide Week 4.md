# MATH 241 · Reading Guide · Week 4
## Strang Chapter 8, and why the book jumps

---

**Strang puts linear transformations in Chapter 8, after eigenvalues and orthogonality.** These notes take them now, in Week 4, and the reason is worth stating: **change of basis is the tool Weeks 7, 10 and 11 all use**, and meeting it for the first time inside a discussion of diagonalisation makes it look like a trick specific to eigenvectors. It is not. It is the general fact, and eigenvectors are one application.

**So this week you read out of order.** Chapter 8 depends on nothing after Chapter 3 except a mention of eigenvalues in §8.3, which is flagged below.

| Chapter | Read? | Why |
|---|---|---|
| **8.1 The Idea of a Linear Transformation** | **All of it** | L13. Strang's examples are more geometric than ours; do both |
| **8.2 The Matrix of a Linear Transformation** | **All of it, twice** | L14, entire. **The most important section in the chapter** |
| **8.3 The Search for a Good Basis** | **Read, and skip the eigenvalue paragraphs** | L15. He forward-references Chapter 6; read around it |
| 8.4, 8.5, 8.6 | Not yet | Graphics and applications. Worth an evening in Week 12 |
| **Axler Ch. 3.A–3.B** | **Read** | Linear maps, null space and range done abstractly. **Better than Strang here** |
| **Goodfellow §2.3** | Skim | The ML view; brief, and the notation differs |

---

## §8.1 — the questions to hold

1. Strang's opening requirement is $T(cv + dw) = cT(v) + dT(w)$; L13 §1 gives two separate conditions. **Show they are equivalent** — one direction needs $d = 0$.
2. He lists transformations that are **not** linear and includes $T(v) = v + v_0$. **Why does a translation matter enough to name?** *(L13 §2's homogeneous-coordinates note; it is the reason 3-D graphics uses $4\times4$.)*
3. Find his examples of $T$ on a space of **functions** or **matrices**. Do at least one in full. **The whole point of Week 3's abstraction was to make these legal.**
4. He defines the range and the kernel — under those names or as *column space* and *nullspace*. **Write down which is which**, and confirm against L13 §3's table.
5. **A linear map is determined by its action on a basis.** Find where he says it. Does he prove it? *(L13 §5's proof is two halves, one using spanning and one using independence — check which of his sentences is doing which job.)*

---

## §8.2 — read this twice

6. **Column $j$ is $T(v_j)$ in the output basis.** This is the whole section. Write the sentence out.
7. Strang is careful to use **two** bases, one for the input space and one for the output. **Where does he take them to be the same, and where does he not?** Most textbook exercises silently use one; Week 11's SVD uses two and needs you to have noticed.
8. He derives the rotation matrix from the images of $e_1$ and $e_2$. **Do it yourself for $-45°$ before reading, then check.** If you had to look up $R_\theta$, that is the habit this section exists to remove.
9. **Composition is multiplication.** Find his statement, then reread Week 1's L04 §1 — where multiplication was *defined* to make this work. **The definition and the theorem are the same fact, three weeks apart.**
10. Does he do differentiation as a matrix? *(He does — find it. Compare his basis and matrix with L14 §4's. If they differ, it will be the basis ordering, which is a good illustration that the matrix is not canonical.)*

---

## §8.3, skipping the eigenvalue paragraphs

11. He writes the change-of-basis relation as $B = M^{-1}AM$ — check that his $M$ and L15 §3's have their **columns** the same way round. *(Textbooks differ. Getting the direction from a book without checking is how the error propagates.)*
12. **Similar matrices.** Find the definition, and the list of what they share. Does he include the trace?
13. He calls the section *the search for a good basis* and lists the candidates. **Write down his list and compare it with L15 §7's table.** The Week 11 row — two different bases, one at each end — is the one to notice.
14. **Skip anything using eigenvalues on a first read.** You will meet it in Weeks 6–7 and the argument does not depend on it.

---

## Where Axler Earns His Place This Week

**Chapter 3 is Axler's best chapter and it is exactly this week.** He treats linear maps as the primary object and matrices as a derived convenience — the opposite emphasis from Strang, and the right one for Week 4.

| Axler | Why bother |
|---|---|
| **3.A** the vector space of linear maps | That $\mathcal{L}(V,W)$ is itself a vector space, and composition is a product. **Strang never says this** |
| **3.B** null space and range | The **Fundamental Theorem of Linear Maps**: $\dim V = \dim\ker T + \dim\operatorname{range} T$. **That is rank–nullity, proved without a single matrix** |
| 3.C the matrix of a map | His §3.C is L14, done carefully, with both bases explicit throughout |

**Read 3.B even if you read nothing else.** Seeing rank–nullity proved with no coordinates anywhere is the clearest evidence that Week 3's theorem was about maps and not about elimination.

---

## The Habit for This Week

**Never write a matrix without saying which basis it is in.**

Up to Week 3 there was one basis and nobody mentioned it. From now on there are two or more in play at once, and **a column of numbers is not an answer until you say what its entries are coordinates in.**

Write it in the margin: *standard*, or *$u$-basis*, or *$\{1,x,x^2\}$*. It takes two words. **The alternative is the characteristic Week 4 error** — computing $M^{-1}AM$ where $MAM^{-1}$ was wanted, getting a perfectly respectable matrix, and having no way to tell.

**The check that catches it costs two minutes:** compute $T$ on each new basis vector directly, convert to the new coordinates, and confirm those are the columns of your $B$. Trace and determinant will *not* catch a reversed $M$ — both matrices are similar to $A$, so every invariant agrees.

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| **Strang, MIT 18.06, Lecture 31** | Linear transformations and change of basis. Late in his ordering; watch it now |
| **Axler Ch. 3** | The whole subject without coordinates |
| **3Blue1Brown, *Essence of Linear Algebra*, episodes 3, 4, 9, 13** | Change of basis animated. **Episode 13 is L15 §7** and is the best five minutes on it anywhere |
| **CS 321 (Graphics)** | L13 §2's homogeneous coordinates, for a whole course |
| **Weeks 7, 10, 11** | Where "find a good basis" acquires three different answers |

---

*MATH 241 · Week 4 · Reading Guide · © CSE Department*
