# MATH 241 · Recitation 5 — Solutions and Session Notes
## **INSTRUCTOR ONLY** · Do not distribute

**Session:** Thursday of Week 6, 15:00–15:50, SSB 108 · covers Week 5 · unmarked
**Midterm 1 was the previous evening. PS 5 is due 17:00 the following day.**

---

## Running the Session — read this first

**This session is unlike the others and the sheet is built differently.** The room will arrive having sat an exam fourteen hours earlier, with a problem set due in twenty-six. **Attention will be low and anxiety will not be.**

**The drill sections are deliberately short.** Do not stretch them to fill time. **§4 is the session**, and it has two halves that must happen in the stated order — PS 5 first, because it has a deadline, then the paper.

| | Section | Budget | Note |
|---|---|---|---|
| §1 | The drill | 10 min | Brisk. It is calibration, not teaching |
| §2 | The two traps | 10 min | **Protect (b) and (c)** — both were on the paper |
| §3 | Volume | 10 min | Cut to (a) and (d) if §4 needs room |
| §4 | Clinic | 15–20 min | **The session.** PS 5 first, then the paper |

### The rule about marks

**Do not discuss the mark scheme, and do not confirm individual answers.** Papers are returned in Week 7 and marks are the instructor's. **Work the *method* of a hard question with different numbers** — that is useful and does not pre-empt anything.

**If a student says the whole paper was hard**, that is not a clinic conversation. **Send them to office hours or the Help Desk, by name and time** — Prof. Abara is 10:00–11:00 Thursdays in SSB 310. Weeks 6–11 build on Weeks 2–4 and a real gap will not close on its own.

---

## §1 — The Drill

**(a)** $M = \begin{bmatrix}1&2&0&0\\ 3&1&2&0\\ 0&4&1&3\\ 0&0&2&1\end{bmatrix}$, pivots $1,\ -5,\ \tfrac{13}{5},\ -\tfrac{17}{13}$, **no exchanges**:

$$\det M = 1 \times (-5) \times \tfrac{13}{5} \times \left(-\tfrac{17}{13}\right) = \boxed{17}$$

*The fractions cancel telescopically, which is normal and worth pointing out — students who see $\tfrac{13}{5}$ appear often assume they have erred.*

**(b)** By cofactors along **column 1** (entries $1, 3, 0, 0$): only two minors survive, each $3\times3$. **Genuinely competitive here** — a banded matrix has few nonzeros per row, and each zero deletes a minor.

**The honest comparison:** for this $M$, cofactors along column 1 cost two $3\times3$s ≈ 12 products; elimination costs about the same. **At $n = 4$ with this much sparsity it is a wash.** At $n = 10$, even banded, elimination wins outright.

*Do not overstate the cofactor case. L17 §5 lists sparsity as one of four legitimate uses, and this is an instance, not a reversal.*

**(c)** **$\det = 0$.** Row 3 $= 2\times$row 1 $+$ row 2: $2(1,3,2) + (2,1,4) = (4,7,8)$ ✓ Dependent rows, so L16 §3(e) applies.

**(d)** $\det M = 17$, $M$ is $4\times4$:

| | |
|---|---|
| $\det(M^\mathsf{T})$ | $17$ |
| $\det(M^{-1})$ | $1/17$ |
| $\det(2M)$ | $2^4 \cdot 17 = \mathbf{272}$ |
| $\det(M^2)$ | $289$ |
| $\det(N^{-1}MN)$ | $17$ |

> **Ask the room how many wrote $34$.** $\det(2A) = 2\det A$ is the single most common determinant
> error and it was on yesterday's paper. **Getting them to check what they wrote, now, is worth more
> than the drill.**

---

## §2 — The Two Traps

**(a)** $A = I$, $B = -I$ in $2\times2$: $\det A + \det B = 2$, $\det(A+B) = \det 0 = 0$.

**P3 says: linear in each row *separately*, all other rows held fixed.** Adding two matrices changes **every** row at once, which is outside what P3 licenses. *(A one-row change is linear; an all-rows change is not.)*

**(b) — both breakages**

**1. Perfectly conditioned, trips the check:** $A = 10^{-4}I_2$. Then $\det A = 10^{-8}$, which is under the threshold, and $\operatorname{cond}_\infty(A) = 10^{-4}\cdot 10^{4} = \mathbf{1}$ — the best possible. **Solving with this matrix is exact division by a power of ten.**

**2. Determinant 1, numerically hopeless:** $A = \begin{bmatrix}10^6 & 0\\ 0 & 10^{-6}\end{bmatrix}$. $\det A = 1$, passes the check, and $\operatorname{cond}_\infty(A) = 10^{12}$.

*Both are PS 0 Q5(b). A pair that reproduces them from memory has retained the right thing.*

**(c) — the argument**

The theorem $\det A = 0 \iff$ singular is **exact and has no error term.** The trouble is that **you never compute $\det A$; you compute a floating-point approximation to it**, and the quantity being approximated is not scale-invariant.

**The sentence to reach:** *the criterion is exact, but the number it tests is meaningless at scale — $\det(cA) = c^n\det A$, so a determinant near zero may mean the entries are small rather than the matrix is bad, and a determinant near one guarantees nothing.*

> **Push for the words "scale-invariant".** A pair that gets there has the whole argument; a pair
> saying only "floating point is inaccurate" has not, since the problem persists in exact arithmetic
> — a $1000\times1000$ matrix of entries near $0.1$ has an exactly-computed determinant near
> $10^{-1000}$ and is still perfectly well conditioned.

---

## §3 — Volume

**(a)** $\det\begin{bmatrix}2&1&0\\ 1&3&1\\ 0&1&2\end{bmatrix} = 2(6-1) - 1(2-0) + 0 = 10 - 2 = 8$. **Volume 8.**

**(b)**

| | $\det$ | |
|---|---:|---|
| $\begin{bmatrix}1&7\\0&1\end{bmatrix}$ | $1$ | shear — area preserved |
| $\begin{bmatrix}3&0\\0&3\end{bmatrix}$ | $9$ | uniform scaling — **area $\times 9$, not $\times 3$** |
| $\begin{bmatrix}1&2\\3&6\end{bmatrix}$ | $0$ | columns dependent — the plane collapses to a line |
| $\begin{bmatrix}0&1\\1&0\end{bmatrix}$ | $-1$ | reflection — area preserved, **orientation reversed** |

*The second is worth a beat: $\det(3I_2) = 3^2 = 9$, which is §1(d)'s $\det(2A)$ error in geometric clothing.*

**(c)** The reflection. **The sign records orientation** — an anticlockwise circuit becomes clockwise.

**No rotation can produce it** because the determinant of a rotation by $\theta$ is $\cos^2\theta + \sin^2\theta = 1$ for **every** $\theta$. To reach $-1$ continuously, the determinant would have to pass through $0$ — and a matrix with determinant $0$ is singular, which no rigid motion is. **The two families are separated by a barrier the determinant cannot cross.**

**(d)**

$$\det\begin{bmatrix}\cos\theta & -r\sin\theta\\ \sin\theta & r\cos\theta\end{bmatrix} = r\cos^2\theta + r\sin^2\theta = r$$

**The sentence:** *a change of variables is locally a linear map — its derivative — and a linear map scales area by $\lvert\det\rvert$; so the area element picks up $\lvert\det J\rvert = r$, which is why a polar rectangle far from the origin is bigger than one near it.*

---

## §4 — Clinic

### PS 5 first

**Q3(a), the adjugate.** The unstick, and nothing more: *"is $\operatorname{adj}$ the cofactor matrix, or its transpose?"* Then send them to the verification, which catches it.

**Q3(c), what Cramer's rule is for.** Most will have costed it and stopped. The prompt: *"you have shown it is useless for computing. Look at the shape of the formula — what does it tell you about how $x$ depends on $b$?"* Do **not** say "rational function"; that is the answer.

**Q5's warning.** §2(b) and §2(c). If those landed, say so and move on.

### Then the paper

**Work methods, not answers.** If several students bring the same question, do it once at the board with different numbers.

**Expected clusters, based on what the paper covers:**

| Likely difficulty | Where to point them |
|---|---|
| The four subspaces, dimensions or ambient spaces | Week 3's L12 §3 and REC 3's table |
| Change of basis, direction of $M$ | Week 4's L15 §3, and REC 4 §2(f)'s check |
| $\det(cA)$ | §1(d) above, today |
| Anything from Weeks 0–1 | Almost certainly a symptom, not the cause — send to office hours |

> **Close the session by naming what is next.** Week 6 is eigenvalues, it starts from
> $\det(A - \lambda I) = 0$, and **that determinant is computed symbolically by cofactors** — which
> is why L17 §5 said cofactors were worth a lecture despite being hopeless numerically. **Students
> who found Week 5 pointless should be told, explicitly, that next week is what it was for.**

---

## What to Report Back

| Signal | What it means for Week 6 |
|---|---|
| Several got $\det(2M) = 34$ | It was on the paper. **Recap in L19's first two minutes** |
| §2(c) answered "floating point is inaccurate" | The scale-invariance point has not landed after two attempts. Let it go for now — Week 8's condition-number work revisits it |
| The room was subdued and asked little | Normal the day after an exam. **Report attendance rather than engagement**, and note anyone who did not come |
| Individual students clearly at sea on Weeks 2–4 | **Name them to Prof. Abara.** Week 6 onward is cumulative and this is the last easy moment to intervene |

---

*MATH 241 · Week 5 · Recitation 5 Solutions · © CSE Department*
