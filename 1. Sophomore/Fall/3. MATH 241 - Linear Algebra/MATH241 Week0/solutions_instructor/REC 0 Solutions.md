# MATH 241 · Recitation 0 — Solutions and Session Notes
## **INSTRUCTOR ONLY** · Do not distribute

**Session:** Thursday of Week 1, 15:00–15:50, SSB 108 · covers Week 0 · unmarked
**PS 0 is due 17:00 the following day**, which is why the session sits here.

---

## Running the Session

**Fifty minutes, and §2 and §3 are the ones that matter.** If time runs short, cut §1 to five minutes and drop §4(d) — do **not** cut §3, which is the only place in Week 0 where students are made to think in the column picture under supervision, and it is the direct preparation for Q2(c).

| | Section | Budget | If it overruns |
|---|---|---|---|
| §1 | Multiplier discipline | 10 min | Cut to 5. It is a warm-up, not a lesson |
| §2 | The mid-elimination zero | 15 min | **Protect this.** It is the single most common Week 0 error |
| §3 | Reading the columns | 10 min | **Protect this.** It is Q2(c) and it is Week 2 |
| §4 | The machine | 10 min | Demo from the front instead of in pairs |
| §5 | Clinic | 5 min | Take it to the Help Desk |

**Board discipline.** Make them write multipliers *before* the operation, not after. The habit is the entire content of §1 and it pays off for the rest of the term.

**Do not answer a "check my Q1" question.** Redirect to substitution every time, out loud, so the room hears the redirect. By Recitation 2 they stop asking.

---

## §0 / §1 — The Prepared Problem

$$\left[\begin{array}{ccc|c} 2 & 4 & -2 & 2\\ 4 & 9 & -3 & 8\\ -2 & -3 & 7 & 10\end{array}\right]
\xrightarrow[\;\ell_{31}=-1\;]{\;\ell_{21}=2\;}
\left[\begin{array}{ccc|c} 2 & 4 & -2 & 2\\ 0 & 1 & 1 & 4\\ 0 & 1 & 5 & 12\end{array}\right]
\xrightarrow{\;\ell_{32}=1\;}
\left[\begin{array}{ccc|c} 2 & 4 & -2 & 2\\ 0 & 1 & 1 & 4\\ 0 & 0 & 4 & 8\end{array}\right]$$

**Multipliers $2, -1, 1$. Pivots $2, 1, 4$.** Back substitution: $x_3 = 2$, $x_2 = 4 - 2 = 2$, $2x_1 + 8 - 4 = 2 \Rightarrow x_1 = -1$.

$$x = (-1, 2, 2)$$

Substitution check: $-2 + 8 - 4 = 2$ ✓ · $-4 + 18 - 6 = 8$ ✓ · $2 - 6 + 14 = 10$ ✓

> **The error to expect:** $\ell_{31} = -1$ handled as $R_3 \leftarrow R_3 - R_1$, giving
> $[\,0\ \ -7\ \ 9 \mid 8\,]$. The room will contain both versions and the pairs will find it
> themselves, which is the point of pairing. **Let them find it.** Do not announce the answer at the
> start of §1.

---

## §2 — The Zero That Is Not at the Top

$$\left[\begin{array}{ccc|c} 1 & 2 & 3 & 6\\ 2 & 4 & 7 & 13\\ 3 & 5 & 3 & 11\end{array}\right]
\xrightarrow[\;\ell_{31}=3\;]{\;\ell_{21}=2\;}
\left[\begin{array}{ccc|c} 1 & 2 & 3 & 6\\ 0 & 0 & 1 & 1\\ 0 & -1 & -6 & -7\end{array}\right]$$

**(a) The fixable kind — L02 §6 Case A.** The test is *"is there a nonzero below it in this column?"*, and row 3 has $-1$. **That is the only thing you have to look at.** Nothing about the size of the matrix, the other entries, or how the zero arose is relevant to the decision.

*Push on this at the board.* Students want to reason about why the zero appeared. The algorithm does not care, and asking them to state the one-line test is what makes the two cases separable in their heads.

**(b)** Swap $R_2 \leftrightarrow R_3$:

$$\left[\begin{array}{ccc|c} 1 & 2 & 3 & 6\\ 0 & -1 & -6 & -7\\ 0 & 0 & 1 & 1\end{array}\right]$$

Already triangular — no further elimination needed. **Pivots $1, -1, 1$: three of them, so the matrix is nonsingular.** $x_3 = 1$, $-x_2 - 6 = -7 \Rightarrow x_2 = 1$, $x_1 + 2 + 3 = 6 \Rightarrow x_1 = 1$. So $x = (1,1,1)$, which checks against all three originals immediately.

**(c) Where the zero came from.** Row 2's first two entries, $[\,2\ \ 4\,]$, are exactly twice row 1's $[\,1\ \ 2\,]$. **Subtracting $2R_1$ therefore annihilates both**, not just the one it was aimed at. The third entries differ ($7 \ne 6$), which is why the row did not vanish entirely.

*The phrasing to insist on:* the zero is a fact about **rows 1 and 2 of the original matrix**, and it was there before any arithmetic was done. Students who say "because $4 - 4 = 0$" have described the arithmetic, not the cause.

**(d) With row 3 replaced by $[\,2\ \ 4\ \ 9\,]$.**

$$\left[\begin{array}{ccc} 1 & 2 & 3\\ 2 & 4 & 7\\ 2 & 4 & 9\end{array}\right]
\xrightarrow[\;\ell_{31}=2\;]{\;\ell_{21}=2\;}
\left[\begin{array}{ccc} 1 & 2 & 3\\ 0 & 0 & 1\\ 0 & 0 & 3\end{array}\right]$$

**Now column 2 is entirely zero below the pivot row, and there is nothing to swap in. Case B: singular.** Column 2 has **no pivot**; elimination moves on to column 3, gets a pivot there, and finishes with **two pivots for three unknowns**.

**The sentence without elimination in it:**

| | The matrix is like this |
|---|---|
| **(a)–(c), fixable** | Nothing is wrong with it. Its rows happened to be in an order the algorithm could not start column 2 from |
| **(d), singular** | **Column 2 is twice column 1** — $(2,4,4) = 2(1,2,2)$ — so the columns only reach a plane, and one unknown is redundant |

> **This is the whole §2 payoff and it is worth the last three minutes.** A row exchange is a fact
> about the *presentation*; a missing pivot is a fact about the *matrix*. Elimination distinguishes
> them and nothing simpler does. Students who leave with that sentence will not confuse the two
> cases on the midterm.

---

## §3 — Reading the Columns

$$C = \begin{bmatrix}1 & 2 & 1\\ 3 & 6 & 0\\ 2 & 4 & 5\end{bmatrix}, \qquad c_1 = \begin{bmatrix}1\\3\\2\end{bmatrix},\; c_2 = \begin{bmatrix}2\\6\\4\end{bmatrix},\; c_3 = \begin{bmatrix}1\\0\\5\end{bmatrix}$$

**(a)** $c_2 = 2c_1$. Visible at a glance; if a pair is computing, stop them.

**(b)** Every $Cx = x_1c_1 + x_2c_2 + x_3c_3 = (x_1 + 2x_2)c_1 + x_3c_3$, so **the reachable $b$ are exactly the combinations of $c_1$ and $c_3$: a plane through the origin in $\mathbb{R}^3$**, spanned by $(1,3,2)$ and $(1,0,5)$.

**(c)** Find $(\alpha,\beta,\gamma)$ with $\alpha c_1 + \dots$ — that is, a vector orthogonal to both spanning columns:

$$\alpha + 3\beta + 2\gamma = 0 \quad\text{and}\quad \alpha + 0 + 5\gamma = 0$$

From the second, $\alpha = -5\gamma$; substituting, $-5\gamma + 3\beta + 2\gamma = 0 \Rightarrow \beta = \gamma$. Take $\gamma = 1$:

$$\boxed{-5b_1 + b_2 + b_3 = 0}$$

Verify on all three columns: $c_1: -5 + 3 + 2 = 0$ ✓ · $c_2: -10 + 6 + 4 = 0$ ✓ · $c_3: -5 + 0 + 5 = 0$ ✓

*(Any nonzero multiple of $(-5,1,1)$ is correct. Some pairs will find $(5,-1,-1)$; accept it.)*

**(d)**

| $b$ | $-5b_1 + b_2 + b_3$ | Solvable? |
|---|---:|---|
| $(1,3,2)$ | $0$ | **Yes** — it is $c_1$ |
| $(1,1,1)$ | $-3$ | **No** |
| $(0,0,0)$ | $0$ | **Yes**, trivially: $x = 0$ |
| $(3,9,6)$ | $0$ | **Yes** — it is $3c_1$ |

**(e)** For $b = (1,3,2)$: $x = (1,0,0)$ reaches it, and so does $x = (-1,1,0)$, since $-c_1 + c_2 = -c_1 + 2c_1 = c_1$ ✓. *(The general solution is $(1,0,0) + t(-2,1,0)$ — the direction vector encodes $c_2 = 2c_1$, which is a preview of Week 2's null space and is worth naming aloud if the room is quick.)*

> **The closing remark to make out loud.** Elimination answers "is *this* $b$ reachable?" one $b$ at
> a time and costs $n^3/3$. The equation in (c) answers it **for every $b$ at once** and cost
> nothing. Week 2 calls the plane the **column space** and the equation a constraint from the **left
> null space**. They have now met both objects before the vocabulary, which is the right order.

---

## §4 — The Machine

**(a)** Room prediction is usually "something huge" or "an error". **The answer is `0.0`**, which is the outcome nobody guesses, and the surprise is the pedagogy. Let them predict out loud before anyone scrolls.

**(b)** Adding $10^{-13}$ and $10^{-14}$:

| $\varepsilon$ | Unpivoted $x_1$ | Relative error |
|---|---|---:|
| $10^{-13}$ | $1.000310945187266$ | $3.11\times10^{-4}$ |
| $10^{-14}$ | $0.99920072216264089$ | $7.99\times10^{-4}$ |

There is no threshold — the error degrades smoothly and then collapses. **The useful outcome of the exercise is that each pair has to choose a tolerance and defend it**, which is what an error bound is. Any answer between $10^{-13}$ and $10^{-15}$ is defensible; "when it stops being wrong" is not, and is the answer to argue with.

**(c)** $4.1\times10^{16} \times 2.2\times10^{-16} \approx 9$.

That product is **the relative error bound**: $\operatorname{cond}(A)\cdot\varepsilon_{\text{mach}}$ bounds how far the computed answer can be from the true one, relative to the true one. **A bound of $9$ permits an answer nine times the size of the right one** — it guarantees nothing whatever, not even the sign. Once the product reaches $1$, the number of digits you are promised is zero.

*The follow-up worth asking if the room is with you:* the measured error at $n=12$ was $6\times10^{-3}$, far better than the bound of $9$. **Why is that not reassuring?** Because it is luck for this particular $b$; nothing about the computation entitles you to it, and a different $b$ on the same matrix can attain the bound.

**(d)** Scaling $H_{10}$ by $10$:

| | Before | After | Changed? |
|---|---|---|---|
| $\det$ | $2.16\times10^{-53}$ | $\times 10^{10} = 2.16\times10^{-43}$ | **Yes**, by ten orders of magnitude |
| $\operatorname{cond}_\infty$ | $3.54\times10^{13}$ | $3.54\times10^{13}$ | **No** |
| Accuracy of the solve | 3 digits | 3 digits | **No** |

$\det(cA) = c^n\det A$, whereas the $c$ in $\lVert cA\rVert$ cancels the $1/c$ in $\lVert(cA)^{-1}\rVert$. **The determinant depends on your choice of units and the condition number does not, which settles which of the two is measuring the difficulty of the problem.** This is PS 0 Q5(b) in disguise; if a pair gets here, they have done that question.

---

## §5 — Clinic Notes

**Q1(c), carrying $d$.** The instruction that unsticks people: *treat $d$ as if it were the number 7, and do not simplify it away.* The echelon form's last row is $[\,0\ 0\ 0 \mid d-9\,]$ and everything follows from reading it.

**Q2(c).** If §3 landed, say so explicitly: *"you did this twenty minutes ago with $C$; do it with $B$."* Do not re-derive it — the transfer is the exercise.

**Q5(c).** The one-line unstick: *residual asks whether your $x$ nearly satisfies the equations; error asks whether it is near the answer. Draw two number lines.* Do **not** give them the $2\times2$ example; constructing it is where the marks are.

> **Do not solve any part of PS 0 at the board.** The numbers in this sheet were chosen to be
> different from the paper's for that reason. If a clinic question can only be answered by working
> a PS 0 part, answer the *method* question underneath it and send them to office hours — Prof.
> Abara is available 10:00–11:00 tomorrow morning, before the 17:00 deadline.

---

## What to Report Back

Note for the Week 1 lecture on Friday which of these the room struggled with:

| Signal | What it means for Week 1 |
|---|---|
| §2(a) answered with reasoning about *why* the zero appeared | The two-case test has not landed. Re-state it in one line before L06's $PA = LU$ |
| §3(c) needed heavy prompting | The column picture is still not the default. **L04 §2 should slow down** |
| §4(c) got the arithmetic but not the meaning | Fine for now. Week 8 has the geometry that makes it stick |

---

*MATH 241 · Week 0 · Recitation 0 Solutions · © CSE Department*
