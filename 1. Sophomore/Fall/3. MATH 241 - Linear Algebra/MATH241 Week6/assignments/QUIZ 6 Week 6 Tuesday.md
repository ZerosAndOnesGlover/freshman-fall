# MATH 241 · Quiz 6
## Administered: **Tuesday**, Week 6 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 5** — determinants.

**Instructions:** Closed notes. 10 minutes.

> **This is the only quiz in the term that is not a Monday.** Week 6's Monday is **Fall Break**, so
> the quiz moves to the start of the week's first lecture, which is the Tuesday. Weeks 7–11 revert
> to Monday.
>
> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **Midterm 1 is tomorrow evening**, 18:00–19:15, SSB 110, covering Weeks 0–5. **Sit this paper as a
> last diagnostic** — everything on it is examinable tomorrow.

---

**Q1.** State the three defining properties of the determinant.

&nbsp;

&nbsp;

---

**Q2.** $A$ is $3\times3$ with $\det A = 5$. Find $\det(2A)$ and $\det(A^{-1})$.

&nbsp;

&nbsp;

---

**Q3.** How do you compute a determinant by elimination? State the rule including the sign.

&nbsp;

&nbsp;

---

**Q4.** Cofactor expansion costs $n!$; elimination costs $n^3/3$. Given that, **why is cofactor expansion taught at all?**

&nbsp;

&nbsp;

---

**Q5.** What does $\lvert\det A\rvert$ measure geometrically? What does the **sign** mean?

&nbsp;

&nbsp;

---

**Q6.** Prove $\det(M^{-1}AM) = \det A$ in one line.

&nbsp;

&nbsp;

---

**Q7.** A well-conditioned $1000\times1000$ matrix has every entry near $0.1$. A colleague tests invertibility with `if det(A) != 0:`. What goes wrong, and what should they compute?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** $\det I = 1$; **exchanging two rows reverses the sign**; **linear in each row separately**, the other rows fixed. *(L16 §2.)*

---

**Q2.** $\det(2A) = 2^3 \cdot 5 = \mathbf{40}$ — a factor of 2 **per row**, and there are three. $\det(A^{-1}) = \mathbf{1/5}$.

*If you wrote $10$, that is the single most common determinant error and it is on tomorrow's paper. **P3 is linearity in one row at a time.***

---

**Q3.** **Eliminate; the determinant is the product of the pivots, times $-1$ once per row exchange.**

$$\det A = (-1)^{\#\text{exchanges}} \, p_1p_2\cdots p_n$$

*Valid because adding a multiple of one row to another leaves $\det$ unchanged (L16 §3(c)) — that property is what makes the whole method legal.*

---

**Q4.** **Because it handles symbolic entries and elimination does not.** Elimination divides by pivots; with a symbol in the matrix that means dividing by expressions that might be zero, forcing a case split at every step. **Cofactors only multiply and add.**

**And $\det(A - \lambda I)$ is exactly such a determinant** — which is this week's lecture and the reason Week 5 happened. *(L17 §5. Also: small $n$, and rows with many zeros.)*

---

**Q5.** $\lvert\det A\rvert$ is the factor by which $A$ **scales volume** (area, in $\mathbb{R}^2$).

**The sign is orientation:** positive preserves it, negative reverses it — an anticlockwise circuit becomes clockwise, or a right-handed frame becomes left-handed. *(L18 §1–§2.)*

---

**Q6.**

$$\det(M^{-1}AM) = \det(M^{-1})\det(A)\det(M) = \frac{1}{\det M}\det(A)\det(M) = \det A$$

*Using the product rule and $\det(M^{-1}) = 1/\det M$. **This is the theorem Week 4 assumed.** (L18 §4.)*

---

**Q7.** The determinant is roughly $(0.1)^{1000} = 10^{-1000}$, which **underflows a `double` to exactly $0.0$** — so the test reports a perfectly good matrix as singular.

**The cause:** $\det(cA) = c^n\det A$, so the determinant is **not scale-invariant** and is dominated by the size of the entries rather than by invertibility.

**Compute $\operatorname{cond}(A) = \lVert A\rVert\lVert A^{-1}\rVert$ instead**, which is scale-invariant. *(L18 §6, and Week 0's L03 §7.)*

---

### What to Do With Your Score

There is no score — and the exam is tomorrow, so use this as triage.

| If you missed | Reread **tonight** |
|---|---|
| Q1, Q3 | L16 §2 and §4 |
| **Q2** | **L16 §2.** $\det(cA) = c^n\det A$. **Put it on your cheat sheet** |
| Q4 | L17 §5 |
| Q5 | L18 §1–§2 |
| Q6 | L18 §4 |
| **Q7** | **L18 §6.** The exact-criterion / bad-test distinction is the week's main idea |

**Q2 and Q7 are the two most likely to appear tomorrow**, and they are the two people get wrong under time pressure. **Neither requires any computation** — both are one fact, correctly recalled.

---

*MATH 241 · Week 6 · Quiz 6 · covers Week 5 · sat Tuesday · ungraded*
