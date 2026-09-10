# MATH 241 · Reading Guide · Week 8
## Strang Chapter 4, and the structure Week 2 withheld

---

**Chapter 4 is where Strang's book turns from algebra to geometry**, and it is the chapter most students find easiest — because the pictures are finally allowed. **Do not mistake that for it being unimportant:** Weeks 9, 10, 11 and 12 all rest on it, and it is the answer to the conditioning complaint Week 7 ended on.

| Chapter | Read? | Why |
|---|---|---|
| **4.1 Orthogonality of the Four Subspaces** | **All of it** | L24. You skimmed two pages of this in Week 3; read it properly |
| **4.2 Projections** | **All of it, twice** | L25 entire. **The most reused section in the second half** |
| **4.4 Orthonormal Bases and Gram–Schmidt** | **All of it** | L26 |
| 4.3 Least Squares | **Do not read yet** | **Week 9.** It will be much better after this week has settled |
| **Strang §4.2, the "trace of a projection" remark** | Find it | PS 8 Q2(d) |
| **Axler Ch. 6.A–6.B** | **Read 6.A** | Inner products done abstractly — the right framing for Week 12 |
| **Goodfellow §2.6–2.7** | Skim | Norms and orthogonality in ML notation |

---

## §4.1 — the questions to hold

1. Strang defines orthogonal subspaces and immediately warns about the floor and the wall. **Reconstruct why they are not orthogonal** before reading his explanation.
2. **The one-line proof that $\mathbf{N}(A) \perp \mathbf{C}(A^\mathsf{T})$.** Find it. It is *"$Ax = 0$ says $x$ is perpendicular to every row"*, and it is worth noticing how little it needs.
3. He introduces **orthogonal complements** and writes $\mathbf{N}(A) = \mathbf{C}(A^\mathsf{T})^\perp$. **What does the word *complement* add** beyond orthogonality? *(Week 3's REC 3 §2(d) is exactly this trap: dimensions adding up is not enough.)*
4. Find where he states that every $x$ splits uniquely as $w + w^\perp$. **This is L25's projection before projections are defined** — notice that the splitting comes first and the formula second.
5. **Does he prove the converse of the solvability condition?** *(That $b \perp \mathbf{N}(A^\mathsf{T})$ implies $Ax = b$ is solvable. Week 3's L12 §5 owed it and L24 §4 pays it.)*

---

## §4.2 — read this twice

6. **The projection onto a line.** He writes $p = \dfrac{a^\mathsf{T}b}{a^\mathsf{T}a}a$ and then $P = \dfrac{aa^\mathsf{T}}{a^\mathsf{T}a}$. **Confirm for yourself which of $a^\mathsf{T}a$ and $aa^\mathsf{T}$ is a number and which is a matrix**, and what rank the matrix has.
7. **The key idea, stated once:** the error is orthogonal to the subspace. Everything in the section follows from it. **Find the sentence where he says so.**
8. He derives $A^\mathsf{T}A\hat x = A^\mathsf{T}b$. **Where does he use that $A$ has independent columns?** *(For $A^\mathsf{T}A$ to be invertible — and you proved that in PS 2 Q5(c), Week 2.)*
9. $P^2 = P$ and $P^\mathsf{T} = P$. **Prove both algebraically before reading his**, and give the geometric reason for each.
10. **What are the eigenvalues of a projection matrix?** He may not say. Work it out from §5's geometry — and then check $\operatorname{trace}P = \dim W$ falls out.
11. He notes the degenerate cases $P = I$ and $P = 0$. **Which subspaces do they project onto?**

---

## §4.4

12. **Orthonormal is orthogonal *and* unit length.** Strang writes $Q^\mathsf{T}Q = I$. **Why is $QQ^\mathsf{T} = I$ only true for square $Q$?** *(Try a $3\times2$ $Q$ and compute both.)*
13. **The three things that become free:** the inverse, coordinates, the projection matrix. Find all three in his text and write them out.
14. **Gram–Schmidt.** Do his example before reading the answer. Then do it **in the reverse order** and compare — PS 8 Q3(c).
15. He gives $A = QR$ and notes $R$ is upper triangular. **Why upper?** Answer from the construction, not from the picture.
16. **Does he mention that classical Gram–Schmidt is numerically poor?** *(He may mention modified Gram–Schmidt in passing. L26 §5 says what production code actually does, which is Householder reflections.)*

---

## Where Axler Earns His Place This Week

**Axler §6.A defines an *inner product space*** — a vector space with a $\langle\cdot,\cdot\rangle$ satisfying four axioms — and derives length, angle, Cauchy–Schwarz and orthogonality from those alone.

**Why bother, when Strang's dot product is concrete and works?** Because **the abstraction is what lets Week 12 happen.** PS 8 Q3(d) orthogonalises $1, x, x^2$ using $\int_{-1}^{1}fg\,dx$ in place of the dot product, and gets the Legendre polynomials. **That integral is an inner product**, every theorem of this week applies to it verbatim, and Fourier series are the orthonormal-basis expansion of L26 §1(c) in a space of functions.

**Read 6.A before Week 12 and this will feel inevitable rather than magical.**

---

## The Habit for This Week

**Check the error, not the answer.**

You have projected $b$ onto a subspace and got $p$. **Do not check $p$. Check $e = b - p$:**

$$e^\mathsf{T}a_j = 0 \quad\text{for every column } a_j \qquad\text{equivalently}\qquad A^\mathsf{T}e = 0$$

**One dot product per column, exact, and it certifies the entire computation** — the normal equations, the inverse, the arithmetic, all of it. If $e$ is orthogonal to the subspace and $p = b - e$ lies in it, then $p$ **is** the projection, by the uniqueness in L24 §4.

**This is the third instance of the same discipline this term.** Week 4: multiply out $M^{-1}AM$ and compare. Week 7: multiply out $S\Lambda S^{-1}$ and compare. **Week 8: dot the error with the columns.** In each case the check costs seconds, is exact, and catches errors that no plausibility inspection would.

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| **Strang, MIT 18.06, Lectures 14–17** | Orthogonality, projections, least squares, Gram–Schmidt. **Lecture 15 is L25** |
| **Trefethen & Bau, Lectures 7–8** | QR and Gram–Schmidt with the numerics foregrounded. **Lecture 8 is L26 §5 in full** |
| **Axler Ch. 6** | Inner product spaces, and orthogonal projection without coordinates |
| **Week 9** | Least squares: this week's projection, with data attached |
| **Week 12** | Fourier as an orthonormal expansion — L26 §1(c) on functions |

---

*MATH 241 · Week 8 · Reading Guide · © CSE Department*
