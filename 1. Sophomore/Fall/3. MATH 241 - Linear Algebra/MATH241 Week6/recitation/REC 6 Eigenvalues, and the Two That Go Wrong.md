# MATH 241 · Recitation 6
## Eigenvalues, and the Two That Go Wrong
### Covers Week 6 · sat **Thursday of Week 7**, 15:00–15:50, SSB 108 · **unmarked, attendance required**

---

> **This recitation covers Week 6 and is sat in Week 7.**
>
> **PS 6 is due at 17:00 tomorrow.** Come with your attempt.
>
> **Midterm 1 papers are returned this week.** If yours revealed a gap in Weeks 2–4, say so in §5 —
> everything from here on is built on them.

**What this session is.** Fifty minutes on the eigenvalue computation and, more importantly, on **the two ways it goes wrong** — no real eigenvalues, and not enough eigenvectors. Week 7 is entirely about the second, so this is the session that decides whether next week makes sense.

**What to bring:** paper, your PS 6 attempt, one laptop per pair for §4.

---

## 0. Before You Come (10 minutes, at home)

For

$$A = \begin{bmatrix}4&1\\ 2&3\end{bmatrix}$$

find the characteristic polynomial **using the $2\times2$ shortcut**, the eigenvalues, and both eigenvectors. **Verify each eigenvector**, and check your eigenvalues against the trace and the determinant.

*(Four numbers of arithmetic if you use the shortcut. If you expanded a determinant, you did it the slow way — L20 §3.)*

---

## 1. The Drill (10 min)

**In pairs, at the board.** Compare your prepared answers. **Expect $\lambda = 2, 5$** with eigenvectors $(-1,2)$ and $(1,1)$.

**(a)** Did you both run the trace and determinant checks? $2 + 5 = 7$ and $2\times5 = 10$. **If your eigenvalues fail either check, you do not need to look for the error — you already know there is one.**

**(b)** Now a $3\times3$, and this one is not a shortcut:

$$B = \begin{bmatrix}2&0&0\\ 1&3&0\\ 4&5&-1\end{bmatrix}$$

**Write down its eigenvalues in five seconds** and say why you may. Then find the eigenvector for $\lambda = 2$.

**(c)** $C$ is $4\times4$ with $\operatorname{trace}C = 10$ and eigenvalues $1, 2, 3, \lambda_4$. **Find $\lambda_4$.** Then, if $\det C = 24$, **check your answer** — and say what you would conclude if the two disagreed.

---

## 2. The Two That Go Wrong (15 min)

**This is the session.** Both are matrices with something missing, and Week 7 is about the second.

### (a) No real eigenvalues (5 min)

$$R = \begin{bmatrix}1&-1\\ 1&1\end{bmatrix}$$

**Find the characteristic polynomial and show it has no real root.** Then find the complex eigenvalues, and **check that their sum is the trace and their product is the determinant.**

**Say, in one sentence, what "no real eigenvalue" means about $R$ as a transformation of the plane.**

### (b) Not enough eigenvectors (10 min)

**Two matrices. Both have a repeated eigenvalue. Only one is defective.**

$$P = \begin{bmatrix}3&0\\ 0&3\end{bmatrix} \qquad\qquad Q = \begin{bmatrix}3&1\\ 0&3\end{bmatrix}$$

**(i)** Show they have the **same characteristic polynomial**. What is it, and what is the repeated eigenvalue?

**(ii)** Find the eigenspace of each. **What is the dimension in each case?**

**(iii)** Give the algebraic and geometric multiplicity of $\lambda = 3$ for each, in a table.

**(iv)** **Which is defective, and which is not?** State the criterion you used — it is not "the eigenvalue repeats", since both do.

**(v)** **The question to argue as a pair.** $P$ and $Q$ have the same characteristic polynomial, the same trace, the same determinant and the same rank. **Are they similar?** Justify — and note this is Week 4's PS 4 Q5(d) with the numbers changed.

> **Get the sentence out loud before moving on:** *a repeated eigenvalue does not make a matrix
> defective; a deficient eigenspace does.* **Every difficulty in Week 7 traces back to this
> distinction**, and the room that leaves without it will find next week arbitrary.

---

## 3. Predicting From Geometry (10 min)

**No matrices until you have predicted.** For each, say the eigenvalues and eigenvectors from the picture:

**(a)** Reflection across the line $y = 3x$.
**(b)** Projection onto the line $y = 3x$.
**(c)** Rotation by $270°$.
**(d)** The map that scales by $5$ in every direction.

**Then:**

**(e)** Which of (a)–(d) has an eigenspace of dimension **2**? What does that say about the transformation?

**(f)** For (b), you can get the eigenvalues **with no geometry and no determinant**, from a single algebraic identity that every projection satisfies. **What is it, and what does it force?**

---

## 4. Ten Minutes With a Machine (10 min)

```bash
python3 resources/eigen.py
```

**(a)** Find the block on the week's $3\times3$. **Confirm the trace and determinant checks** printed there, and note that the eigenvectors are verified by an explicit $Av$ product — the same check the problem set demands of you.

**(b)** Find the table of six predictable transformations. **One is flagged `DEFECTIVE`.** Which, and does it match your §2(b) criterion?

**(c)** Find the rotation block. **The script reports that the trace and determinant identities survive complex eigenvalues.** Verify by hand for $\lambda = \pm i$.

**(d)** *(If you finish early.)* Change the shear's off-diagonal entry from $1$ to $7$ and re-run. **Does it stop being defective?** Predict before you run it, and say what that tells you about how "close" a defective matrix is to a diagonalisable one.

---

## 5. Clinic (whatever is left)

**PS 6, due tomorrow:**

- **Q2(c) against Q2(e).** §2(b) of this sheet is that pair. If §2 landed, this is written.
- **Q4(b), constructing a matrix with geometric multiplicity exactly 2.** The unstick, and nothing more: *start from $4I$ and add a single entry off the diagonal. Then compute the rank of $A - 4I$.*
- **Q5(d).** Two sentences: one about characteristic polynomials being similarity-invariant, one about trace and determinant being the sum and product.

**Midterm 1 papers:** returned this week. **If yours showed a gap in Weeks 2–4, raise it now**, not in Week 10. Prof. Abara is 10:00–11:00 Thursdays in SSB 310, and the Help Desk is BH 120.

> **What not to ask for.** "Is my eigenvector right?" — compute $Av$ and compare with $\lambda v$.
> Exact, thirty seconds, and it is the check the paper explicitly requires.

---

*MATH 241 · Week 6 · Recitation 6 · sat Thursday of Week 7 · unmarked*
