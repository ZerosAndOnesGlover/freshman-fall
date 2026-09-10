# MATH 241 · Recitation 4
## One Map, Two Bases
### Covers Week 4 · sat **Thursday of Week 5**, 15:00–15:50, SSB 108 · **unmarked, attendance required**

---

> **This recitation covers Week 4 and is sat in Week 5.**
>
> **PS 4 is due at 17:00 tomorrow.** Come with your attempt.
>
> **CS 201's Midterm 1 is the Monday of this week.** MATH 241's is the Wednesday of **Week 6** —
> two weeks away, covering Weeks 0–5. This session is the last recitation before the material for
> it is complete.

**What this session is.** Fifty minutes on the one skill Week 4 adds: **the same transformation has different matrices, and you choose which.** Building a matrix from images of basis vectors, converting between bases, and getting the direction of $M$ right — which is the error that will otherwise follow you into Weeks 7, 10 and 11.

**What to bring:** paper, your PS 4 attempt, one laptop per pair for §4.

---

## 0. Before You Come (10 minutes, at home)

$T : \mathbb{R}^2 \to \mathbb{R}^2$ is the reflection across the line $y = -x$.

**Find its standard matrix**, by computing $T(e_1)$ and $T(e_2)$ and drawing the picture. Bring both images and the matrix.

*(Draw it. The vector $e_1 = (1,0)$ reflected in the line $y = -x$ — where does it land? If you find yourself reaching for a formula, stop and draw.)*

---

## 1. Build, Don't Recall (10 min)

**In pairs, at the board, no formulas.** For each, compute $T(e_1)$ and $T(e_2)$ and write the matrix:

**(a)** Rotation by $-90°$ (clockwise).
**(b)** Reflection across $y = -x$ — your prepared answer. **Compare with your partner.**
**(c)** $(x,y) \mapsto (x, -y)$ — name it geometrically before you compute.
**(d)** Projection onto the $y$-axis.

**Then:**

**(e)** Compute the product of **(a) and (b)** in both orders. **Are they the same?** Identify each product as a familiar transformation.

**(f)** One of the four matrices above satisfies $A^2 = I$ and one satisfies $A^2 = A$. **Find both and say what each identity means about the transformation.**

---

## 2. The Direction of $M$ (15 min)

**This is the section. Everyone gets this backwards once; do it here rather than on the midterm.**

Let $u_1 = (2,1)$ and $u_2 = (1,1)$.

**(a)** Write $M$ with the new basis vectors as columns. **Compute $M^{-1}$.**

**(b)** Find the coordinates of $v = (5,3)$ in the $u$-basis, **by solving directly** — $c_1u_1 + c_2u_2 = v$.

**(c)** Now check both formulas against your answer:

$$[v]_{\text{old}} = M[v]_{\text{new}} \qquad\text{and}\qquad [v]_{\text{new}} = M^{-1}[v]_{\text{old}}$$

**Which one turns $(c_1,c_2)$ back into $(5,3)$?** Say the sentence out loud: *$M$ takes new coordinates to old.*

**(d)** **The trap.** A classmate says: *"$M$ has the new basis in its columns, so $M$ must convert into the new basis."* **Explain, in one sentence, exactly where that reasoning goes wrong.**

**(e)** Now let $T$ be the map with standard matrix $A = \begin{bmatrix}1&2\\0&3\end{bmatrix}$. Compute $B = M^{-1}AM$.

**(f)** Check your $B$ **without trusting the arithmetic**: compute $T(u_1)$ and $T(u_2)$ directly, express each in the $u$-basis, and confirm those are the columns of $B$. **If they disagree, you have $M$ the wrong way round** — which is exactly the point of the section.

---

## 3. A Basis That Fits the Map (10 min)

$$A = \begin{bmatrix}5&-2\\-2&5\end{bmatrix}$$

**(a)** Compute $A(1,1)$ and $A(1,-1)$. **Each is a multiple of what you started with.** Which multiples?

**(b)** Write $B$, the matrix of this map in the basis $\{(1,1),(1,-1)\}$ — **directly from (a), with no inverse.**

**(c)** Check that $A$ and $B$ have the same trace and the same determinant.

**(d)** **Argue as a pair.** $B$ is diagonal and $A$ is not. **Has the transformation been simplified, or only its description?** Give a physical or geometric statement that is true of the map and visible in $B$ but not in $A$.

**(e)** You found the special basis by being told it. **How would you find it without being told?** You do not have the method yet — **say what you would need to look for.** *(You are describing eigenvectors, and that is Week 6.)*

---

## 4. Ten Minutes With a Machine (10 min)

```bash
python3 resources/transformations.py
```

**(a)** Find the block building each matrix from $T(e_1)$ and $T(e_2)$. **Add your §1 transformations to the `maps` dictionary and re-run.** Do the printed matrices match yours?

**(b)** Find the rotation composition. $R(30)R(60) = R(90)$ to $1.6\times10^{-16}$. **Now check whether $R(30)$ and the reflection across $y = x$ commute.** Predict first.

**(c)** Find the derivative matrix on $\mathbb{P}_3$ and confirm $D^4 = 0$. **Then work out by hand what $D^3$ does to $x^3$**, and check it against the printed matrix.

**(d)** Find the similarity table at the end. **Trace, determinant and rank agree across each pair.** Construct a matrix similar to $\begin{bmatrix}2&0\\0&5\end{bmatrix}$ that is **not** diagonal, and verify all three agree.

---

## 5. Clinic (whatever is left)

**The three that come up every year:**

- **Q4(c), the direction of $M$.** §2 is that question. If §2 landed, refuse to be asked again.
- **Q3(c), $DJ$ against $JD$.** Both products are two minutes of arithmetic. **The question is what the differing entry *means*** — and if you have computed both and seen nothing, look at which basis vector it corresponds to.
- **Q5(d), $I$ and $\begin{bmatrix}1&1\\0&1\end{bmatrix}$.** One line unsticks it: *what is $M^{-1}IM$, for any $M$ at all?*

> **What not to ask for.** "Is my change of basis right?" — §2(f) is the check: compute $T$ on the
> new basis vectors directly and compare with $B$'s columns. Exact, and it takes two minutes.

---

*MATH 241 · Week 4 · Recitation 4 · sat Thursday of Week 5 · unmarked*
