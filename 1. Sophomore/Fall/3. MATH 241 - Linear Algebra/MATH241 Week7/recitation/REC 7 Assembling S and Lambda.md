# MATH 241 · Recitation 7
## Assembling $S$ and $\Lambda$
### Covers Week 7 · sat **Thursday of Week 8**, 15:00–15:50, SSB 108 · **unmarked, attendance required**

---

> **This recitation covers Week 7 and is sat in Week 8.**
>
> **PS 7 is due at 17:00 tomorrow.** Come with your attempt.

**What this session is.** Fifty minutes assembling $A = S\Lambda S^{-1}$ by hand, on **three matrices chosen so that one diagonalises easily, one diagonalises despite a repeated eigenvalue, and one cannot.** Telling the second from the third is the whole skill.

**What to bring:** paper, your PS 7 attempt, one laptop per pair for §4.

---

## 0. Before You Come (10 minutes, at home)

Diagonalise

$$A = \begin{bmatrix}1&2\\ 4&3\end{bmatrix}$$

**Bring $S$, $\Lambda$, $S^{-1}$, and your verification that $S\Lambda S^{-1} = A$.**

*(Use the $2\times2$ shortcut for the eigenvalues. If you expanded a determinant, you did it the slow way.)*

---

## 1. The Drill, and the Order Trap (10 min)

**In pairs, compare your prepared answers.** Expect $\lambda = 5, -1$.

**(a)** Your partner almost certainly ordered the eigenvalues the other way. **Both are correct.** Confirm that both $(S, \Lambda)$ pairs give the same $A$, and state the rule: **the columns of $S$ must be in the same order as the diagonal of $\Lambda$.**

**(b)** Now deliberately break it: keep your $S$ and swap the two diagonal entries of $\Lambda$. **Compute $S\Lambda S^{-1}$.** You will get a matrix — a perfectly respectable one — that is **not $A$.**

**Which of its properties still match $A$'s, and which do not?** *(Check the trace and the determinant.)*

> **This is Week 4's reversed-$M$ trap in new clothes.** The wrong answer is similar to the right
> one, so **trace and determinant cannot detect the error.** The only check is $S\Lambda S^{-1} = A$,
> which is why the problem set demands it.

**(c)** Use your diagonalisation to compute $A^4$, and check one entry by direct multiplication.

---

## 2. Three Matrices, Three Outcomes (15 min)

**This is the session.**

$$P = \begin{bmatrix}5&0\\ 0&5\end{bmatrix} \qquad Q = \begin{bmatrix}5&2\\ 0&5\end{bmatrix} \qquad R = \begin{bmatrix}4&1\\ 2&3\end{bmatrix}$$

**(a)** Find the characteristic polynomial of each. **Two of the three have a repeated eigenvalue.** Which?

**(b)** For each, find every eigenspace and its dimension. **Fill in a table:** matrix, eigenvalue, algebraic multiplicity, geometric multiplicity.

**(c)** **Which are diagonalisable?** For each, say which criterion decided it.

**(d)** For the one that is not, **say what is there instead of the missing eigenvector** — compute $Qe_2$ and describe it in words.

**(e)** **The question to argue as a pair.** $P$ and $Q$ have the same characteristic polynomial, trace, determinant and rank. **One is diagonalisable and one is not.**

Now suppose someone hands you $\begin{bmatrix}5&10^{-9}\\ 0&5\end{bmatrix}$. **Is it diagonalisable?** And **could a computer tell you?**

> *(It is not — geometric multiplicity 1 for any nonzero off-diagonal entry. And no: in floating
> point $10^{-9}$ and $0$ are both perfectly representable, but a matrix arriving from a measurement
> or a previous computation carries error, so **the distinction is not recoverable.** L22 §4.)*

---

## 3. Complex, and What $\lvert\lambda\rvert$ Does (10 min)

$$C = \begin{bmatrix}1&-2\\ 2&1\end{bmatrix}$$

**(a)** Find the complex eigenvalues. Check the sum against the trace and the product against the determinant.

**(b)** **Now get $r$ and $\theta$ from the trace and determinant alone**, using L23 §2, and confirm they match $\lvert\lambda\rvert$ and $\arg\lambda$. **Describe $C$ in one sentence.**

**(c)** Take $x_0 = (1,0)$ and compute $x_1 = Cx_0$, $x_2 = Cx_1$, $x_3 = Cx_2$. **Plot the four points roughly.** What is happening, and what will happen as $k$ grows?

**(d)** **Without any computation:** for which of these does $x_k \to 0$?

$$\begin{bmatrix}0.6&-0.3\\ 0.3&0.6\end{bmatrix} \qquad \begin{bmatrix}1&-2\\ 2&1\end{bmatrix} \qquad \begin{bmatrix}0.5&0\\ 0&1.2\end{bmatrix}$$

*(One number per matrix decides it. Say which number and why — and note that for the middle one you already know the answer from (a).)*

---

## 4. Ten Minutes With a Machine (10 min)

```bash
python3 resources/diagonalize.py
```

**(a)** Find the $A = S\Lambda S^{-1}$ block and confirm the verification prints `True`. **Note that $S$ and $S^{-1}$ are both integer here, and that the script says this is luck.** Why is it usually not?

**(b)** Find the cost comparison. **$\Lambda^{1000}$ is three scalar powers; repeated squaring needs 14 matrix products.** At what $k$ would you bother diagonalising, if the setup costs $O(n^3)$?

**(c)** Find the Markov block. **Every column of $P^k$ converges to $(2/3, 1/3)$.** Confirm that the convergence rate matches $0.7^k$ by comparing the $k = 20$ entries with $0.7^{20}$.

**(d)** *(If you finish early.)* Find the defectiveness table. **Change the off-diagonal entries and re-run.** Confirm §2(e)'s claim that nothing but exactly zero restores diagonalisability.

---

## 5. Clinic (whatever is left)

**PS 7, due tomorrow:**

- **Q1(c).** §2 of this sheet is that question. **A repeated eigenvalue is not the criterion.**
- **Q1(b), the two-dimensional eigenspace.** The unstick: *compute the rank of $A + I$ — you will find it is 1, and rank–nullity gives you the dimension without any elimination.*
- **Q3(c), the two matrices.** One hint: *what is the product of the eigenvalues, and what does that force?* Nothing more.
- **Q4(c), PageRank.** Your paragraph needs three things: which eigenvector, what the iteration is, and **what sets the number of steps.** If you have only the first two, you have not answered it.

> **What not to ask for.** "Is my $S$ right?" — multiply $S\Lambda S^{-1}$ and see. Exact, one
> minute, and §1(b) showed that no other check works.

---

*MATH 241 · Week 7 · Recitation 7 · sat Thursday of Week 8 · unmarked*
