# MATH 241 · Quiz 10
## Administered: Monday, Week 10 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 9** — least squares, the normal equations, and what fitting assumes.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **Midterm 2 is this Wednesday**, covering **Weeks 6–9**. **This is the last diagnostic before the
> paper**, and Week 9 is the part of it you have had least time with. **Take it seriously and read
> the key today, not on Wednesday afternoon.**

---

**Q1.** Why is "$Ax = b$ has no solution" the **normal** situation rather than an unlucky one? Answer with $m$, $n$ and one sentence.

&nbsp;

&nbsp;

---

**Q2.** Derive $A^\mathsf{T}A\hat x = A^\mathsf{T}b$ from one sentence about the residual $e = b - A\hat x$.

&nbsp;

&nbsp;

---

**Q3.** Fit $y = c + dx$ to $(-1,1)$, $(0,2)$, $(1,4)$. Give $A$, $A^\mathsf{T}A$, $\hat x$, the residual $e$, and **check $A^\mathsf{T}e = 0$**.

&nbsp;

&nbsp;

&nbsp;

---

**Q4.** State the identity that makes the normal equations the wrong algorithm, and convert it into a statement about **digits**.

&nbsp;

&nbsp;

---

**Q5.** On Läuchli's matrix at $\varepsilon = 10^{-8}$, $A^\mathsf{T}A$ is **exactly singular in floating point**, although $A$ visibly has independent columns. **Name the single arithmetic operation that destroyed the information.**

&nbsp;

&nbsp;

---

**Q6.** "Use QR instead of the normal equations." **Why is that not adequate advice?** Name the two QRs and say which survives.

&nbsp;

&nbsp;

---

**Q7.** Adding a column to $A$ can never increase $\lVert e\rVert$. **Why not** — and why is that a problem rather than a feature?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** With $m$ measurements and $n$ parameters and $m > n$, $\mathbf{C}(A)$ is an $n$-dimensional subspace sitting inside $\mathbb{R}^m$. **Almost every $b$ in $\mathbb{R}^m$ is outside it**, and measurement error alone puts $b$ outside. **Solvability is the accident; unsolvability is the default.** *(L27 §1.)*

---

**Q2.** **The residual must be orthogonal to $\mathbf{C}(A)$**, hence to every column of $A$:

$$A^\mathsf{T}(b - A\hat x) = 0 \quad\Longrightarrow\quad A^\mathsf{T}A\hat x = A^\mathsf{T}b.$$

*(L27 §2. It is Week 8's L25 §3 with data attached.)*

---

**Q3.**

$$A = \begin{bmatrix}1&-1\\1&0\\1&1\end{bmatrix}, \quad A^\mathsf{T}A = \begin{bmatrix}3&0\\0&2\end{bmatrix}, \quad A^\mathsf{T}b = \begin{bmatrix}7\\3\end{bmatrix} \quad\Longrightarrow\quad \hat x = \begin{bmatrix}c\\d\end{bmatrix} = \begin{bmatrix}\tfrac73\\[2pt]\tfrac32\end{bmatrix}.$$

Fitted values $\left(\tfrac56, \tfrac73, \tfrac{23}{6}\right)$, so

$$e = \left(\tfrac16,\ -\tfrac13,\ \tfrac16\right), \qquad A^\mathsf{T}e = \left(\tfrac16 - \tfrac13 + \tfrac16,\ -\tfrac16 + 0 + \tfrac16\right) = (0,0)\ ✓$$

and $\lVert e\rVert^2 = \tfrac1{36} + \tfrac19 + \tfrac1{36} = \tfrac16$.

> **$A^\mathsf{T}A$ came out diagonal because $\bar x = 0$** — the $x$ values were centred. **That is
> worth doing on purpose**, and it is the cheapest conditioning improvement in the subject.
>
> **Centroid check:** $\bar x = 0$, $\bar y = \tfrac73$, and the line at $x = 0$ gives $c = \tfrac73$ ✓

---

**Q4.** $\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$.

**In digits:** forming $A^\mathsf{T}A$ **doubles the number of digits you lose.** If $A$ costs you six digits, the normal equations cost you twelve — from sixteen. *(L28 §1, using Week 0's L03 §7 rule of thumb.)*

---

**Q5.** **The addition $1 + \varepsilon^2$.** With $\varepsilon = 10^{-8}$, $\varepsilon^2 = 10^{-16}$ is below the spacing of doubles near $1$ ($2^{-52} \approx 2.2\times10^{-16}$), so $1 + \varepsilon^2$ **rounds to exactly $1$** and both entries of $A^\mathsf{T}A$ become identical. **The matrix goes exactly singular** while $A$ itself is unharmed. *(L28 §2.)*

---

**Q6.** **Because it matters which QR.**

| method | $\varepsilon = 10^{-7}$ | $\varepsilon = 10^{-8}$ |
|---|---|---|
| normal equations | $0.500000000$ | **FAILED** |
| **Gram–Schmidt QR** | $\mathbf{0.511501869}$ | $\mathbf{1.000000000}$ |
| **Householder QR** | $0.500000000$ | $0.500000000$ |

**Gram–Schmidt fails *earlier* than the normal equations** on this problem, because the columns are nearly parallel and the subtraction cancels catastrophically — **Week 8's L26 §5 predicted exactly this.** **Only Householder survives**, because its $Q$ is a product of reflections that are orthogonal by construction rather than by accumulation. *(L28 §4.)*

---

**Q7.** **The old fit is still available** — set the new coefficient to zero — so the minimum over the larger set of options cannot be worse. Equivalently, the new $\mathbf{C}(A)$ **contains** the old one, and projecting onto a bigger subspace cannot land further from $b$.

**Which is why a smaller residual is not evidence of a better model.** Take $n = m$ columns and the residual is zero, with a model that has learned the noise and predicts nothing. *(L29 §4.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread — **before Wednesday** |
|---|---|
| Q1, Q2 | L27 §1–§2. **Two marks of definition on any least-squares exam question** |
| **Q3** | **L27 §3.** **The single most likely computation on Midterm 2's Week 9 question** |
| Q4, Q5 | L28 §1–§2 |
| Q6 | L28 §4 |
| Q7 | L29 §4 |

> **On the midterm, Weeks 6–9 are equally weighted and Week 9 is the one you have practised least.**
> **Q3 is the arithmetic to be fluent at**, and the $A^\mathsf{T}e = 0$ check is free marks and free
> reassurance.
>
> **Today's lecture (L30) is not on the paper.** If you are choosing between attending and revising,
> attend — the notes will not close the loop from Week 7 for you as quickly as forty minutes will.

---

*MATH 241 · Week 10 · Quiz 10 · covers Week 9 · ungraded*
