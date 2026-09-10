# MATH 241 · Quiz 5
## Administered: Monday, Week 5 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 4** — linear transformations, their matrices, and change of basis.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then mark it yourself before you leave.
>
> **Midterm 1 is a week on Wednesday** and covers Weeks 0–5. Treat this paper as a diagnostic.

---

**Q1.** State the two conditions for $T$ to be linear. Which one-line test catches most non-examples immediately?

&nbsp;

&nbsp;

---

**Q2.** Is $T(v) = v + b$ linear, for a fixed $b \ne 0$? What do graphics APIs do about it?

&nbsp;

&nbsp;

---

**Q3.** $T$ rotates $\mathbb{R}^2$ by $180°$. Write its standard matrix by computing $T(e_1)$ and $T(e_2)$.

&nbsp;

&nbsp;

---

**Q4.** $\ker T$ and the range of $T$ are two subspaces you already know under other names. Which?

&nbsp;

&nbsp;

---

**Q5.** $M$ has the new basis vectors as its columns. Does $M$ convert old coordinates to new, or new to old?

&nbsp;

&nbsp;

---

**Q6.** $A$ and $B = M^{-1}AM$ describe the same map. Name three quantities they must share.

&nbsp;

&nbsp;

---

**Q7.** $D$ is differentiation on $\mathbb{P}_3$. Why is $D$ not invertible, and what everyday piece of notation is that fact responsible for?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** $T(v+u) = Tv + Tu$ and $T(cv) = cTv$.

**The test: $T(0) = 0$.** One substitution, and it disposes of every affine map and most other impostors. *(L13 §1.)*

---

**Q2.** **Not linear** — $T(0) = b \ne 0$.

Graphics APIs embed $\mathbb{R}^3$ as the plane $w = 1$ in $\mathbb{R}^4$, where $\begin{bmatrix}A&b\\0&1\end{bmatrix}$ **is** linear and reproduces $T$. **That is the whole reason 3-D pipelines use $4\times4$ matrices.** *(L13 §2.)*

---

**Q3.** $T(e_1) = (-1,0)$ and $T(e_2) = (0,-1)$, so

$$A = \begin{bmatrix}-1&0\\ 0&-1\end{bmatrix} = -I$$

*Derived in five seconds. A student who reached for $R_\theta$ and substituted $\theta = \pi$ got the right answer the slow way — L14 §2.*

---

**Q4.** $\ker T = \mathbf{N}(A)$, the **null space**. Range $= \mathbf{C}(A)$, the **column space**.

*Week 4 introduced no new computation — only new names for Weeks 2–3's objects. (L13 §3.)*

---

**Q5.** **New to old.** $[v]_{\text{old}} = M[v]_{\text{new}}$.

*$M$'s columns are the new basis vectors **written in old coordinates**, so multiplying by $M$ assembles $v$ out of them and delivers an old-coordinate answer. **Building out of the new basis is not converting into it.** (L15 §3 — and this is the error the recitation exists to catch.)*

---

**Q6.** **Rank, trace, determinant.** *(Also, from Week 6, the eigenvalues — which subsume the other two.)* Individual entries are **not** shared. *(L15 §6.)*

---

**Q7.** $\ker D$ is the **constants**, which is not $\{0\}$, so $D$ is not injective — it destroys one dimension of information. *(It is also not surjective: nothing differentiates to a cubic within $\mathbb{P}_3$.)*

**That kernel is the $+\,C$** on every antiderivative: two functions have the same derivative exactly when they differ by an element of $\ker D$. *(L13 §4.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L13 §1–§2 |
| **Q3** | **L14 §2** — derive, do not recall |
| Q4 | L13 §3 |
| **Q5** | **L15 §3.** Reversing $M$ is undetectable by trace or determinant. **Fix it before the midterm** |
| Q6 | L15 §6 |
| Q7 | L13 §4 |

**Q5 is the one that matters.** A reversed $M$ produces a matrix that is *similar to the right answer*, so it has the same trace, determinant and rank — **no invariant will ever catch it.** The only check is computing $T$ on the new basis vectors directly and comparing with $B$'s columns.

---

*MATH 241 · Week 5 · Quiz 5 · covers Week 4 · ungraded*
