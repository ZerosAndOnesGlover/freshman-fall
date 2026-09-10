# MATH 241 · Recitation 7 — Solutions and Session Notes
## **INSTRUCTOR ONLY** · Do not distribute

**Session:** Thursday of Week 8, 15:00–15:50, SSB 108 · covers Week 7 · unmarked
**PS 7 is due 17:00 the following day.**

---

## Running the Session

**§2 is the session**, and §1(b) is the five minutes that stops the commonest silent error. Week 7 is the densest week in the course and the room will be tired; **do not try to cover everything.**

| | Section | Budget | If it overruns |
|---|---|---|---|
| §1 | The drill and the order trap | 10 min | **Keep (b).** Cut (c) |
| §2 | Three matrices, three outcomes | 15 min | **Protect. Cut §3 or §4** |
| §3 | Complex and $\lvert\lambda\rvert$ | 10 min | Keep (a), (b), (d) |
| §4 | The machine | 10 min | Drop |
| §5 | Clinic | 5 min | Never drop |

---

## §0 / §1 — The Drill and the Order Trap

$A = \begin{bmatrix}1&2\\4&3\end{bmatrix}$: trace $4$, determinant $3 - 8 = -5$, so $\lambda^2 - 4\lambda - 5 = 0$ and $\boxed{\lambda = 5, -1}$.

Eigenvectors: $(1,2)$ for $\lambda = 5$; $(1,-1)$ for $\lambda = -1$.

$$S = \begin{bmatrix}1&1\\ 2&-1\end{bmatrix}, \quad \Lambda = \begin{bmatrix}5&0\\ 0&-1\end{bmatrix}, \quad S^{-1} = \begin{bmatrix}\tfrac13&\tfrac13\\ \tfrac23&-\tfrac13\end{bmatrix}, \quad S\Lambda S^{-1} = A\ ✓$$

**(a)** Both orderings work provided the columns of $S$ match the diagonal of $\Lambda$. **Have a pair with the other ordering write theirs next to the first** — two different $S$, two different $\Lambda$, same $A$.

**(b) — the five minutes that matter**

Keeping $S$ and swapping only $\Lambda$'s diagonal gives

$$S\begin{bmatrix}-1&0\\0&5\end{bmatrix}S^{-1} = \begin{bmatrix}3&-2\\ -4&1\end{bmatrix}$$

**trace $4$, determinant $-5$ — identical to $A$'s.**

> **So the two most familiar checks are both blind to this error**, and for a structural reason: the
> wrong matrix is *similar* to the right one, so **every** similarity invariant agrees. Trace,
> determinant, rank, characteristic polynomial, eigenvalues — all identical, all useless.
>
> **This is exactly Week 4's reversed-$M$ situation** (REC 4 §2), and the resolution is the same:
> the only check is to multiply out and compare with $A$. **Say so, and connect the two explicitly**
> — a student who sees this is the second instance will generalise the habit.

**(c)** $A^4 = \begin{bmatrix}209&208\\ 416&417\end{bmatrix}$, via $\Lambda^4 = \operatorname{diag}(625, 1)$.

---

## §2 — Three Matrices, Three Outcomes

$$P = \begin{bmatrix}5&0\\ 0&5\end{bmatrix} \qquad Q = \begin{bmatrix}5&2\\ 0&5\end{bmatrix} \qquad R = \begin{bmatrix}4&1\\ 2&3\end{bmatrix}$$

**(a)** $P$ and $Q$ both give $(5-\lambda)^2$ — **repeated.** $R$ gives $\lambda^2 - 7\lambda + 10 = (\lambda-2)(\lambda-5)$ — **distinct.**

**(b)**

| | $\lambda$ | algebraic | geometric | eigenspace |
|---|---|---:|---:|---|
| $P$ | $5$ | $2$ | $2$ | all of $\mathbb{R}^2$ |
| $Q$ | $5$ | $2$ | $\mathbf{1}$ | $\operatorname{span}\{(1,0)\}$ |
| $R$ | $2$ | $1$ | $1$ | $\operatorname{span}\{(1,-2)\}$ |
| $R$ | $5$ | $1$ | $1$ | $\operatorname{span}\{(1,1)\}$ |

**(c)**

- **$P$: yes** — geometric $=$ algebraic. *(It is already diagonal.)*
- **$Q$: no** — geometric $1 <$ algebraic $2$.
- **$R$: yes** — **two distinct eigenvalues**, so L20 §6 gives independence with no eigenspace check needed.

*Three different reasons for three outcomes. Make the room state which criterion applies to each.*

**(d)** $Qe_2 = (2, 5) = 2e_1 + 5e_2$.

**$e_2$ is sent to $5$ times itself *plus a bit of $e_1$*** — the coupling that no change of basis removes. A diagonal matrix scales each basis vector independently; here one basis vector leaks into another, and the Jordan block $\begin{bmatrix}5&1\\0&5\end{bmatrix}$ is the minimal form of that leak. *(L22 §3.)*

**(e) — the argument**

$\begin{bmatrix}5&10^{-9}\\0&5\end{bmatrix}$ is **defective**: $A - 5I = \begin{bmatrix}0&10^{-9}\\0&0\end{bmatrix}$ has rank 1, so the eigenspace is one-dimensional. **Any nonzero off-diagonal entry does this.**

**Could a computer tell you? No, in the sense that matters.** The value $10^{-9}$ is perfectly representable, so a computer can compare it with zero — **but a matrix arriving from a measurement, or from a previous floating-point computation, carries error of its own.** You cannot distinguish "the entry is exactly $0$" from "the entry is $10^{-17}$ and rounded". **So the question is not decidable for any matrix you did not write down by hand**, and production software does not ask it.

> **Push for the second half.** Many pairs will say "yes, just check if it is zero", which is right
> about the literal float and wrong about the situation. **The follow-up: where did this matrix come
> from?**

---

## §3 — Complex, and What $\lvert\lambda\rvert$ Does

**(a)** $C = \begin{bmatrix}1&-2\\2&1\end{bmatrix}$: trace $2$, determinant $1 + 4 = 5$.

$$\lambda^2 - 2\lambda + 5 = 0 \quad\Longrightarrow\quad \lambda = 1 \pm 2i$$

$(1+2i) + (1-2i) = 2$ ✓ · $(1+2i)(1-2i) = 1 + 4 = 5$ ✓

**(b)** $r = \sqrt{5} = 2.2361$; $\cos\theta = 2/(2\sqrt5) = 0.4472$, so $\theta = 63.4°$.

And $\lvert 1+2i\rvert = \sqrt5$ ✓, $\arg(1+2i) = \arctan 2 = 63.4°$ ✓

**$C$ rotates by about $63°$ and scales by $\sqrt5 \approx 2.24$.**

**(c)** From $x_0 = (1,0)$:

| $k$ | $x_k$ | $\lVert x_k\rVert$ |
|---:|---|---:|
| 0 | $(1,0)$ | $1$ |
| 1 | $(1,2)$ | $2.236$ |
| 2 | $(-3,4)$ | $5.000$ |
| 3 | $(-11,-2)$ | $11.180$ |

**Spiralling outwards**, turning about $63°$ each step and multiplying the radius by $\sqrt5$ every time — $\lVert x_k\rVert = (\sqrt5)^k$ exactly. **It goes to infinity.**

**(d)** One number each: **the spectral radius.**

| | $\lvert\lambda\rvert$ | $x_k \to 0$? |
|---|---|---|
| $\begin{bmatrix}0.6&-0.3\\0.3&0.6\end{bmatrix}$ | $\sqrt{\det} = \sqrt{0.45} = 0.671$ | **yes** |
| $\begin{bmatrix}1&-2\\2&1\end{bmatrix}$ | $\sqrt5 = 2.236$ | no |
| $\begin{bmatrix}0.5&0\\0&1.2\end{bmatrix}$ | $1.2$ | no |

**For the first two the determinant gives it immediately** — complex conjugate pair, so $\lvert\lambda\rvert^2 = \det$. The third is diagonal, so read it off. **No characteristic polynomial needed for any of them.**

---

## §4 — The Machine

**(a)** Verification prints `True`, and $\det S = 1$. **Usually not integer** because the eigenvectors solve $(A - \lambda I)v = 0$ with $\lambda$ a root of a polynomial — typically irrational, so the eigenvector entries are too. **Integer eigenvectors need integer eigenvalues *and* luck.**

**(b)** Diagonalising costs $O(n^3)$ once, then $O(1)$ in $k$. Repeated squaring costs $O(n^3\log k)$. **They cross at small $k$ — around $\log k \approx$ a few** — so in practice **diagonalise whenever you need more than a handful of powers**, provided the matrix is diagonalisable and $S$ is well conditioned. *(That last proviso is L22 §4 and is the real constraint.)*

**(c)** At $k = 20$ the entries are $0.666933$ and $0.666135$, differing from $2/3$ by about $2.7\times10^{-4}$ and $5.3\times10^{-4}$. And $0.7^{20} = 7.98\times10^{-4}$. **Same order of magnitude** ✓ — the error is $O(\lvert\lambda_2\rvert^k)$.

**(d)** Nothing but exactly zero restores it. **The table in the script already shows $\varepsilon = 1, 7, 1000$ all defective**, and any value a pair tries will be too.

---

## §5 — Clinic

**Q1(c).** §2. Refuse to re-derive; ask which of the three §2 matrices Q1's resembles.

**Q1(b).** *"What is the rank of $A + I$?"* and stop. They should see it is 1, and rank–nullity does the rest.

**Q3(c).** *"What is the product of the eigenvalues?"* Nothing more.

**Q4(c).** Check they have all three elements. **A paragraph naming the eigenvector and the iteration but not $\lvert\lambda_2\rvert$ is two-thirds of an answer**, and the missing third is the one that explains why fifty iterations suffice.

---

## What to Report Back

| Signal | What it means for Week 8 |
|---|---|
| §1(b) surprised the room | Good. It is the second instance of the same trap and they should now generalise it |
| §2(c) needed prompting on which criterion applies | **The three cases have not separated.** Week 10 assumes them; flag it |
| §2(e) answered "yes, check if it is zero" | Expected. The follow-up question is the teaching moment, not the correction |
| §3(d) done without characteristic polynomials | Excellent — that is the fluency Week 8 wants |

---

*MATH 241 · Week 7 · Recitation 7 Solutions · © CSE Department*
