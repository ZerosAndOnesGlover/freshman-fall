# MATH 241 · Recitation 8
## Projections by Hand
### Covers Week 8 · sat **Thursday of Week 9**, 15:00–15:50, SSB 108 · **unmarked, attendance required**

---

> **This recitation covers Week 8 and is sat in Week 9.**
>
> **PS 8 is due at 17:00 tomorrow.** Come with your attempt.
>
> **Midterm 2 is the Wednesday of Week 10**, covering **Weeks 6–9**. This is the last recitation
> before that material is complete.

**What this session is.** Fifty minutes projecting things and running Gram–Schmidt by hand, because **Week 9 is projection with a story attached** and every difficulty there is a Week 8 difficulty in disguise.

**What to bring:** paper, your PS 8 attempt, one laptop per pair for §4.

---

## 0. Before You Come (10 minutes, at home)

Project $b = (2,3,5)$ onto the line through $a = (1,1,1)$.

**Bring $\hat x$, $p$, $e$, the check that $e \perp a$, and the $3\times3$ projection matrix $P$.**

*(Two of those take one line each. If $P$ took you more than two minutes, look again at L25 §2 — the matrix is $aa^\mathsf{T}$ over a number, and getting those two the right way round is the whole thing.)*

---

## 1. The Drill, and the Order of the Product (10 min)

**In pairs, compare.** Expect $\hat x = 10/3$, $p = \tfrac{10}{3}(1,1,1)$, $e = (-\tfrac43, -\tfrac13, \tfrac53)$.

**(a)** Check $e \perp a$ and confirm you and your partner agree.

**(b)** **The trap.** One of $a^\mathsf{T}a$ and $aa^\mathsf{T}$ is a number and one is a $3\times3$ matrix. **Say which, and what each equals here.** Then write $P$ and check $P^2 = P$.

**(c)** **What is $\operatorname{trace}P$, and why must it be that?** Answer before computing it.

**(d)** Project $(1,1,1)$ itself. **Predict the answer first.** Then project $(1,-1,0)$ and predict that too.

> **Both predictions follow from L25 §5's eigenvalues.** $P$ fixes everything on the line
> ($\lambda = 1$) and kills everything perpendicular to it ($\lambda = 0$). **A projection has no
> other behaviour**, and knowing that saves the arithmetic.

---

## 2. Onto a Plane (15 min)

**This is the session, and it is PS 8 Q2 with different numbers.**

$$A = \begin{bmatrix}1&1\\ 1&0\\ 0&1\end{bmatrix}, \qquad b = (3,0,0)$$

> **Check first that $b$ is genuinely outside $\mathbf{C}(A)$**, or the projection is trivial and the
> exercise is wasted. One dot product against a left-null vector will tell you — finding that vector
> is part (d), so for now just confirm $b$ is not a combination of the two columns.

**(a)** Compute $A^\mathsf{T}A$. **Why is it invertible?** Name the week and the question that proved it.

**(b)** Solve the normal equations $A^\mathsf{T}A\hat x = A^\mathsf{T}b$ for $\hat x$. **Do not form the inverse** — solve the $2\times2$ system.

**(c)** Compute $p = A\hat x$ and $e = b - p$.

**(d)** **Verify $A^\mathsf{T}e = 0$.** Which of the four subspaces does $e$ lie in? **Which two subspaces is $b$ being split between?**

**(e)** Now compute $P = A(A^\mathsf{T}A)^{-1}A^\mathsf{T}$ **once**, and check $Pb$ gives the same $p$.

**(f)** **The question to argue as a pair.** You computed $\hat x$ two ways in this section: by solving a $2\times2$ system, and by forming a $3\times3$ matrix $P$.

**Which would you use for a $1000\times5$ matrix $A$, and why?** *(Count the sizes of the objects involved.)*

> *(The normal equations are a $5\times5$ solve. $P$ is $1000\times1000$ — **a million entries to
> represent a projection onto a 5-dimensional subspace.** Never form $P$ unless you need it as an
> object; and Week 9 will not even form $A^\mathsf{T}A$.)*

---

## 3. Gram–Schmidt, and the Order (10 min)

**(a)** Orthogonalise $a_1 = (1,1,0)$, $a_2 = (1,0,1)$, $a_3 = (0,1,1)$. **Work exactly, clear fractions, and check all three pairwise dot products.**

**(b)** Now do the **same three vectors in reverse order** — $a_3$, $a_2$, $a_1$. **Predict before computing:** will you get the same orthogonal set?

**(c)** **You will not.** Say precisely why, and state what is always true of $q_1$ regardless of the order.

**(d)** **What *is* the same about the two answers?** *(Think about what all three vectors span, and about the subspace spanned by the first two.)*

---

## 4. Ten Minutes With a Machine (10 min)

```bash
python3 resources/orthogonal.py
```

**(a)** Find the four-subspace block. **All ten dot products are zero.** Confirm this is Week 3's table — and note that Week 3 could only *observe* it.

**(b)** Find the projection block. $b = (6,0,0)$ gives $p = (5,2,-1)$ and $e = (1,-2,1)$. **Verify by hand that $e$ is orthogonal to both columns**, and note that $A^\mathsf{T}e = 0$ places it in the left null space.

**(c)** Find the conditioning table at the end: $\operatorname{cond}(S) = 200$, $2\times10^4$, $1.3\times10^8$ for eigenvectors $(1,0)$ and $(1,\varepsilon)$.

**An orthonormal basis gives 1 in every row.** **Say what this has to do with Week 7's complaint about $A = S\Lambda S^{-1}$.**

**(d)** *(If you finish early.)* Find the Gram–Schmidt block producing $(1,1,1)$, $(-1,0,1)$, $(1,-2,1)$. **Those are the constant, linear and quadratic sampled at $x = 1,2,3$, orthogonalised.** Predict what you would get from four points $x = 1,2,3,4$ and check by editing the script.

---

## 5. Clinic (whatever is left)

**PS 8, due tomorrow:**

- **Q2(a), $aa^\mathsf{T}$ against $a^\mathsf{T}a$.** §1(b) is that question.
- **Q4(d), substituting $A = QR$.** The unstick: *substitute, then look for $Q^\mathsf{T}Q$.* Then look for what you can cancel — **and you must justify the cancellation.**
- **Q3(c), the reversed order.** §3 of this sheet is the same question.
- **Q5(d).** Your two sentences must mention Week 7 specifically. A general remark that orthonormal bases are nicer is not an answer.

> **What not to ask for.** "Is my projection right?" — dot the error with each column of $A$. If
> both are zero, it is right. That check is exact and takes thirty seconds.

---

*MATH 241 · Week 8 · Recitation 8 · sat Thursday of Week 9 · unmarked*
