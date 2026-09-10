# MATH 241 · Recitation 10 — TA Notes and Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Thursday of Week 11, 15:00–15:50, SSB 108.**
**Midterm 2 papers are returned this session. PS 10 is due 17:00 the following day.**

**Shape of the session.** §0 is done at home. §1 ten minutes, §2 fifteen, §3 ten, §4 ten, §5 whatever is left. **Run §1–§4 to time and protect §5** — but note the ordering is deliberate: **the mathematics comes first, while attention is available.** Handing back papers at minute zero costs the session.

**How to hand the papers back.** At the **start of §5**, face down, without comment. Not at the start of the hour.

> **This is the same instruction as REC 6, and for the same reason.** A room that has just seen its
> marks does not do linear algebra. **Recitation 5 and Recitation 9 sat the day *before* marks
> existed; this one sits the day they arrive**, and it is the only recitation of the term where the
> ordering of the sheet is doing pastoral work rather than pedagogical work.

**One matrix, four ways.** Everything in §1–§3 is the same $A$. **Do not substitute your own matrix** — this one is constructed so that $Q$ is rational and every check closes exactly, and an improvised replacement will produce irrational eigenvectors and lose the session.

---

## §0 + §1 — The Drill (10 min)

$$A = \begin{bmatrix}9&-4&0\\ -4&7&-4\\ 0&-4&5\end{bmatrix}$$

$$Au_1 = A(1,2,2) = (9 - 8 + 0,\ -4 + 14 - 8,\ 0 - 8 + 10) = (1,2,2) \Rightarrow \lambda_1 = 1$$
$$Au_2 = A(2,1,-2) = (18 - 4 + 0,\ -8 + 7 + 8,\ 0 - 4 - 10) = (14,7,-14) \Rightarrow \lambda_2 = 7$$
$$Au_3 = A(2,-2,1) = (18 + 8 + 0,\ -8 - 14 - 4,\ 0 + 8 + 5) = (26,-26,13) \Rightarrow \lambda_3 = 13$$

### (a)

$\operatorname{trace}A = 9 + 7 + 5 = 21 = 1 + 7 + 13$ ✓ and $\det A = 91 = 1\times7\times13$ ✓.

**Both are Week 6 (L20 §2) and both hold for every square matrix**, symmetric or not — they are consequences of the characteristic polynomial's coefficients, and nothing about symmetry is used. **Say this out loud**; students routinely file trace and determinant under "symmetric matrix facts" this week.

### (b)

$u_1\cdot u_2 = 2 + 2 - 4 = 0$; $u_1\cdot u_3 = 2 - 4 + 2 = 0$; $u_2\cdot u_3 = 4 - 2 - 2 = 0$.

**L30 §3.** Symmetry enters at exactly one step:

$$\lambda(x\cdot y) = (Ax)^\mathsf{T}y = x^\mathsf{T}\underbrace{A^\mathsf{T}}_{= A}y = x^\mathsf{T}Ay = \mu(x\cdot y).$$

**Make someone point at the substitution.** The whole week is that one equality used in different places.

### (c)

**A convenience, and a constructed one.** $A$ was built backwards from three integer vectors that happen to be mutually perpendicular with equal length $3$, so that $Q$ has rational entries.

> **This is worth being honest about.** In general the eigenvectors of a symmetric integer matrix
> have irrational entries and $Q$ is irrational — try $\begin{bmatrix}2&1\\1&3\end{bmatrix}$, whose
> eigenvalues are $\tfrac{5\pm\sqrt5}{2}$. **The theorem is exact; the arithmetic is usually not**,
> and a session built on a lucky matrix should say that it is.

### (d)

$$Q = \frac13\begin{bmatrix}1&2&2\\ 2&1&-2\\ 2&-2&1\end{bmatrix}, \qquad \Lambda = \operatorname{diag}(1,7,13), \qquad Q^{-1} = Q^\mathsf{T}.$$

**Four seconds.** *(If anyone starts eliminating, stop them and ask what $Q^\mathsf{T}Q$ is. That is the entire practical content of the week.)*

---

## §2 — Four Things at Once (15 min)

### (a)

$Q^\mathsf{T}Q = I$: the diagonal entries are $\tfrac19(1+4+4) = 1$ three times, and the off-diagonals are (b)'s dot products over $9$.

**Why two entries of $Q\Lambda Q^\mathsf{T}$ is more than it sounds:** the product $Q\Lambda Q^\mathsf{T}$ is **symmetric by construction** — $(Q\Lambda Q^\mathsf{T})^\mathsf{T} = Q\Lambda Q^\mathsf{T}$ — so checking $(1,2)$ also checks $(2,1)$. **Six of the nine entries are determined by three.** *(Entry $(1,1)$: $\tfrac19(1\cdot1 + 7\cdot4 + 13\cdot4) = \tfrac19(1 + 28 + 52) = \tfrac{81}{9} = 9$ ✓. Entry $(1,2)$: $\tfrac19(1\cdot2 + 7\cdot2 + 13\cdot(-4)) = \tfrac19(2 + 14 - 52) = -4$ ✓.)*

### (b)

$$P_1 = q_1q_1^\mathsf{T} = \frac19\begin{bmatrix}1&2&2\\ 2&4&4\\ 2&4&4\end{bmatrix}, \qquad P_1^2 = P_1\ ✓, \qquad \operatorname{trace}P_1 = \tfrac19(1 + 4 + 4) = 1\ ✓$$

**Without computing:** $\operatorname{trace}(P_1 + P_2 + P_3) = \operatorname{trace}I = 3$, because the three projections sum to the identity (L30 §5) — **and the three traces are $1$ each, so they are counting out the three dimensions of $\mathbb{R}^3$ one line at a time.**

$P_1P_2 = 0$, because $P_1P_2 = q_1(q_1^\mathsf{T}q_2)q_2^\mathsf{T}$ and the middle factor is the scalar $q_1\cdot q_2 = 0$.

> **That one-line argument is the item to get on the board.** Students who verify $P_1P_2 = 0$ by
> multiplying out nine entries have the right answer and the wrong habit; the scalar in the middle
> is the reason, and it is why *perpendicular* is the operative word in "sum of perpendicular
> projections".

### (c)

Eliminating: $R_2 \leftarrow R_2 + \tfrac49R_1$ gives $(0, \tfrac{47}{9}, -4)$; then $R_3 \leftarrow R_3 + \tfrac{36}{47}R_2$ gives $(0, 0, \tfrac{91}{47})$.

$$\text{pivots } 9,\ \tfrac{47}{9},\ \tfrac{91}{47}, \qquad \text{product } = 91 = \det A\ ✓$$

**Leading minors $9$, $47$, $91$**, and each pivot is the ratio of consecutive minors: $\tfrac{47}{9}$, $\tfrac{91}{47}$, with the first being $\tfrac91$. ✓

### (d)

**Four tests are now on the paper without any of them having been run on purpose:**

| Test | The evidence already produced | Verdict |
|---|---|---|
| eigenvalues $> 0$ | $1$, $7$, $13$ from §0 | ✓ |
| pivots $> 0$ | $9$, $\tfrac{47}{9}$, $\tfrac{91}{47}$ from (c) | ✓ |
| leading minors $> 0$ | $9$, $47$, $91$ from (c) | ✓ |
| $A = R^\mathsf{T}R$ | Cholesky exists, since the pivots are positive | ✓ |

**The practical lesson, and the reason for the ordering of this section:** you rarely *set out* to test positive definiteness. **You eliminate for some other reason and the pivots tell you**, or you diagonalise for some other reason and the eigenvalues tell you. **The test is a by-product.**

---

## §3 — The Boundary, and the Trap (10 min)

### (a)

$$A(s) = \begin{bmatrix}s&-4&0\\ -4&7&-4\\ 0&-4&5\end{bmatrix}, \qquad D_1 = s,\quad D_2 = 7s - 16,\quad D_3 = 19s - 80.$$

**All three depend on $s$** — the sheet warns about this and students still assume $D_1$ and $D_2$ are fixed. The three thresholds are $s > 0$, $s > \tfrac{16}{7} \approx 2.286$, $s > \tfrac{80}{19} \approx 4.211$, and the **binding** one is the last:

$$\boxed{\;A(s) \text{ is positive definite} \iff s > \tfrac{80}{19}\;}$$

*(At $s = 9$, $D = (9, 47, 91)$ ✓, comfortably inside.)*

### (b)

At $s = \tfrac{80}{19}$ the pivots are $\tfrac{80}{19}$, $\tfrac{16}{5}$, $\mathbf{0}$, and

$$x = (19, 20, 16) \quad\Longrightarrow\quad A\!\left(\tfrac{80}{19}\right)x = 0 \quad\Longrightarrow\quad x^\mathsf{T}Ax = 0.$$

*(Check: $\tfrac{80}{19}\cdot19 - 4\cdot20 = 80 - 80 = 0$; $-4\cdot19 + 7\cdot20 - 4\cdot16 = -76 + 140 - 64 = 0$; $-4\cdot20 + 5\cdot16 = 0$.)*

**Week 2: $x \in \mathbf{N}(A)$. Week 6: $x$ is an eigenvector for $\lambda = 0$.** The two are the same statement, and this is the cleanest place all term to say so.

### (c)

$$\begin{bmatrix}1&3\\3&1\end{bmatrix}: \quad \lambda = 4,\ -2; \qquad \text{pivots } 1,\ -8; \qquad x = (1,-1) \Rightarrow x^\mathsf{T}Ax = 1 - 6 + 1 = \mathbf{-4}.$$

**Insist on the vector.** "The eigenvalues say no" is a correct answer to a question that was not asked; the exhibited $x$ is the proof, and finding it takes one guess — **the eigenvector for the negative eigenvalue is $(1,-1)$**, and it is always the place to look.

### (d)

$$C = \begin{bmatrix}1&2&2\\ 2&1&2\\ 2&2&1\end{bmatrix}: \qquad D_1 = 1,\quad D_2 = \mathbf{-3},\quad D_3 = 5.$$

**Not positive definite** — eigenvalues $5, -1, -1$, since $C = 2J - I$ and $J$ has eigenvalues $3, 0, 0$.

**The half-remembered test is test 4**, which requires **all** leading principal minors positive. **Positive diagonal and positive determinant is not it**, and here the determinant is positive precisely because there are *two* negative eigenvalues.

> **The follow-up question, if the room is quick:** can this happen in $2\times2$? **No** — there
> $D_1 = a_{11}$ and $D_2 = \det$ are the only two minors, so positive diagonal plus positive
> determinant *is* the test. **The counterexample needs three dimensions**, and that is why the
> mnemonic survives: it is true in the case everyone checks it on.

---

## §4 — Ten Minutes With a Machine (10 min)

### (a)

**$10^{9}$.** A perturbation of $10^{-10}$ in one entry; every eigenvalue moves from $0$ to magnitude $10^{-1}$.

**Make someone say the number out loud.** It is the week's headline and it does not land when read silently.

### (b)

**"A symmetric matrix's eigenvalues move by at most the size of the perturbation; a non-symmetric matrix's can move by a billion times more."**

**The hypothesis is symmetry, and nothing else.** The two matrices in §12 are the same size and the perturbations are the same size.

**If asked why:** at $\varepsilon = 0$ the shift matrix is a single Jordan block — Week 7's worst case, $n$ copies of the eigenvalue $0$ and **one** eigenvector. **Defectiveness and eigenvalue sensitivity are the same phenomenon**, and L30 excludes both with one hypothesis.

### (c)

$\lambda_\min(H_{12}) = 9.953\times10^{-17}$, and the script's own §10 says:

> *"lambda_min for H_12 is about 1e-17, which is smaller than the rounding error in the stored
> entries of H_12 itself. That figure is at the noise floor and its digits are not to be trusted —
> only its order of magnitude, which the exactly-computed cond_inf column corroborates."*

**What you are entitled to conclude:** the order of magnitude, hence $\operatorname{cond}_2(H_{12}) \sim 10^{16}$, hence about **two correct digits** in any solve — which is exactly what Week 0's L03 §6 measured empirically before any of this vocabulary existed.

> **This is the habit, and it is worth naming as such in the room.** The number is reproducible,
> correctly computed, and untrustworthy in most of its digits. **All three at once, and saying so
> where you print it is the whole discipline.** PS 10 Q4(b) pushes it one step further, to
> $n = 14$, where the computed $\lambda_\min$ comes out **negative** for a provably positive
> definite matrix. **Do not spoil that** — it is the best question on the problem set.

---

## §5 — Post-Mortem (whatever is left)

**Papers face down, start of this section.**

**Do:**

- work the **method** of any midterm question with **different numbers**;
- take PS 10 questions — **Q2 and Q5(c) are the ones that will come**;
- send anyone with a question about their own mark to Prof. Abara, Thursdays 10:00–11:00, SSB 310.

**Do not:**

- discuss the mark scheme;
- confirm or deny individual answers;
- compare marks across the room, or let the room do it.

**If the room is quiet and demoralised**, do the last ten minutes on §3(c) again with a $3\times3$. **Working something they can definitely do is the right end to this session.**

> **Flag to the instructor after the session:** anyone whose paper showed a Week 7 gap.
> **Week 11's SVD is Week 7's diagonalisation plus Week 10's theorem**, and a Week 7 gap is now
> compounding weekly with a comprehensive final on Dec 15.

---

*MATH 241 · Week 10 · REC 10 Solutions · © CSE Department*
