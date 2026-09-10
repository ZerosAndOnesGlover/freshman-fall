# MATH 241 · Recitation 9 — Solutions and Session Notes
## **INSTRUCTOR ONLY** · Do not distribute

**Session:** Thursday of Week 10, 15:00–15:50, SSB 108 · covers Week 9 · unmarked
**Midterm 2 was the previous evening. PS 9 is due 17:00 the following day.**

---

## Running the Session

**This is Recitation 5's situation repeated** — exam yesterday, deadline tomorrow — and the sheet has the same shape: short drill, long two-part clinic, **problem set before post-mortem.** See REC 5's notes; the rules about marks are identical and are worth rereading.

| | Section | Budget | Note |
|---|---|---|---|
| §1 | The drill | 10 min | Calibration only |
| §2 | Why not the normal equations | 15 min | **Protect (e)** |
| §3 | What it assumes | 10 min | **Protect (b)–(c)** — the prediction must be made first |
| §4 | Clinic | 15–20 min | PS 9 first, then the paper |

**Do not discuss marks or confirm answers.** Papers return in Week 12.

---

## §0 / §1 — The Drill

$(1,2)$, $(2,3)$, $(3,5)$: $A^\mathsf{T}A = \begin{bmatrix}3&6\\6&14\end{bmatrix}$, $A^\mathsf{T}b = \begin{bmatrix}10\\23\end{bmatrix}$.

Solving $3c + 6d = 10$ and $6c + 14d = 23$: doubling the first gives $6c + 12d = 20$, so $2d = 3$ and $d = \tfrac32$; then $3c = 10 - 9 = 1$, so $c = \tfrac13$.

$$\hat x = \left(\tfrac13,\ \tfrac32\right) \quad\Longrightarrow\quad y = \tfrac13 + \tfrac32 x$$

$$p = \left(\tfrac{11}{6},\ \tfrac{10}{3},\ \tfrac{29}{6}\right), \qquad e = \left(\tfrac16,\ -\tfrac13,\ \tfrac16\right), \qquad \lVert e\rVert^2 = \tfrac16$$

**(b)** $\sum e_i = 0$ is the **first** equation of $A^\mathsf{T}e = 0$ (the column of ones); $\sum x_ie_i = 0$ is the **second** (the column of $x$'s). **Both free, both exact.**

Here: $\tfrac16 - \tfrac13 + \tfrac16 = 0$ ✓ and $1(\tfrac16) + 2(-\tfrac13) + 3(\tfrac16) = \tfrac16 - \tfrac23 + \tfrac12 = 0$ ✓

**(c)** $\bar x = 2$, $\bar y = \tfrac{10}{3}$, and the line at $x = 2$ gives $\tfrac13 + 3 = \tfrac{10}{3}$ ✓

> **The centroid check is the one to insist on**, because it catches an error the residual checks
> can miss. A pair who has mis-solved the $2\times2$ system will often still produce a residual that
> looks plausible; **the line failing to pass through $(\bar x, \bar y)$ is unambiguous.** Ask the
> room to run it on their own answer before comparing with anyone else's.

**(d)** Adding 7 to every $y_i$ **raises $c$ by 7 and leaves $d$ unchanged** — the data is translated vertically, so the best line translates with it. *(From the normal equations: $A^\mathsf{T}b$ gains $(7m,\ 7\sum x_i)$, which is $7\times$ the first column of $A^\mathsf{T}A$.)*

---

## §2 — Why Not the Normal Equations

**(a)** $A^\mathsf{T}A = \begin{bmatrix}1+\varepsilon^2&1\\1&1+\varepsilon^2\end{bmatrix}$.

**The columns of $A$ are independent because neither is a multiple of the other** — the second entries are $\varepsilon$ and $0$. Five seconds, no computation.

**(b)** $\det = (1+\varepsilon^2)^2 - 1 = 2\varepsilon^2 + \varepsilon^4$.

**Computed as zero once $1 + \varepsilon^2$ rounds to $1$**, i.e. $\varepsilon^2 < 2^{-52}$, i.e. $\varepsilon < 2^{-26} = 1.49\times10^{-8}$.

**(c)** **The information was lost in the addition $1 + \varepsilon^2$**, inside the formation of $A^\mathsf{T}A$. Nothing was wrong with $A$; **the method discarded the small quantity by adding it to a large one.** *(Week 0's L03 §4 in a new costume — insist on the connection.)*

**(d)** $\operatorname{cond}(A) = 10^6$ → about **10 digits** survive. $\operatorname{cond}(A^\mathsf{T}A) = 10^{12}$ → about **4**.

**(e) — the argument**

**The normal equations at $10^{-7}$:** $1 + \varepsilon^2$ is still distinguishable from 1, so the determinant is nonzero, and this particular symmetric $2\times2$ cancels favourably. **Nine correct digits.**

**Gram–Schmidt at $10^{-7}$:** the columns are nearly parallel, so $a_2 - (q_1^\mathsf{T}a_2)q_1$ is a small vector computed as a difference of large nearly-equal ones. **Catastrophic cancellation**, the computed $q_2$ drifts out of orthogonality, and the answer is wrong in the second decimal place.

**Can you rely on the normal equations there? No.** $\operatorname{cond}(A^\mathsf{T}A) \approx 2\times10^{14}$: **the problem as posed to the solver has about two reliable digits.** Nine came out right by luck, and one step later — at $\varepsilon = 10^{-8}$ — the luck fails completely and the matrix goes exactly singular.

> **The sentence to leave with:** *"use QR instead of the normal equations" is not adequate advice;
> it matters which QR.* **Week 8's L26 §5 said Gram–Schmidt is the right thing to understand and the
> wrong thing to run, and this table is that claim measured.**

---

## §3 — What It Assumes

**(a)** $(5,5) \to (5,15)$: $\;y = -4 + 3x$, $\lVert e\rVert^2 = 40$. **Slope tripled.**

**(b)–(c)** $(3,3) \to (3,13)$: $\;y = 2 + x$, $\lVert e\rVert^2 = 80$.

**The slope is unchanged. The residual is twice as large.**

**Both facts from the centroid theorem.** The line must pass through $(\bar x, \bar y)$. Here $x = 3$ **is** $\bar x$, so moving that point changes $\bar y$ and **nothing else about the geometry** — the line rises without tilting. **A point at the centre of the $x$-range has no leverage on the slope; a point at the end has the most.**

**And the residual is larger** because the fit could not accommodate the outlier at all: with the end point it tilted to meet it partway, reducing the squared error; with the middle point tilting does not help, so the full displacement stays in the residual.

**(d)** **What would measure the distortion:** compare the *fitted coefficients* with and without the point — or compute each point's **leverage** $P_{ii}$, the diagonal of the projection matrix. *(Accept "refit without it and see"; that is exactly what Cook's distance formalises.)*

> **This is the section that surprises people, and the surprise is the pedagogy.** Most pairs will
> predict that the middle outlier tilts the line more, because it produces a bigger residual.
> **Insist that they write the prediction down before computing.**

---

## §4 — Clinic Notes

**Q2(c).** §3, and the general point: a zero residual from $n = m$ is arithmetic, not evidence.

**Q4(d).** **Three explanations, and check they have all three.** Most will explain the normal-equations failure and stop.

**Q5(b).** §3(b)–(c).

**Q5(d).** *"Compute the integral first — it is two lines. Then ask what matrix you have just built."*

### Returned papers

**Week 12.** Do not discuss marks. Work methods with different numbers.

**Say clearly:** **Weeks 10 and 11 are the hardest of the course**, they assume Weeks 6–9 throughout, and **this is the last comfortable moment to close a gap.** Names to Prof. Abara this week if anyone is clearly adrift.

---

## What to Report Back

| Signal | What it means for Week 10 |
|---|---|
| §1(c) skipped or hand-waved | **They are not running the centroid check.** Say so in L30's first two minutes |
| §2(e) answered "the normal equations are just better here" | The luck-versus-robustness distinction has not landed. It is a likely final question |
| §3(b) predicted correctly | Rare and worth noting — they have understood leverage without being taught it |
| Students adrift on Weeks 6–7 | **Names to Prof. Abara.** Week 10 is the spectral theorem and assumes all of it |

---

*MATH 241 · Week 9 · Recitation 9 Solutions · © CSE Department*
