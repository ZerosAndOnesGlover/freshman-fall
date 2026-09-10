# MATH 241 · Problem Set 9
## Least Squares

---

**Released:** Week 9, Wednesday · **Due:** Week 10, **Friday 17:00**
**Total: 100 points** · Submit one PDF, `PS9_{LastName}_{StudentID}.pdf`

> **Exact arithmetic in Q1–Q3.** Q4 is about what floating point does and says so.
>
> **Check every fit** with $A^\mathsf{T}e = 0$. One dot product per column, and it certifies the whole
> computation.
>
> **Midterm 2 is the Wednesday of this paper's due week**, covering **Weeks 6–9**. **Do not leave
> this until after the exam** — most of it is revision for it.
>
> **Recitation 9 is the Thursday before this is due**, 15:00–15:50, SSB 108 — **the day after the
> midterm.**

---

### Q1: Fitting a Line (22 points)

**(a) [8]** Fit $y = c + dx$ to the points $(0,1)$, $(1,2)$, $(2,4)$, $(3,4)$.

Give $A$, $b$, $A^\mathsf{T}A$, $A^\mathsf{T}b$, and $\hat x$. **State the line.**

**(b) [5]** Give the fitted values $p$, the residuals $e$, and $\lVert e\rVert^2$. **Verify $A^\mathsf{T}e = 0$.**

**(c) [4]** Show that the fitted line passes through the centroid $(\bar x, \bar y)$ of the data.

**Prove it in general** from the first normal equation.

**(d) [5]** Fit a **horizontal** line $y = c$ to the same data — so $A$ has a single column of ones.

**Show that $\hat c = \bar y$**, the mean. Then say in one sentence what that makes the mean, in the language of this week.

---

### Q2: Beyond Straight Lines (20 points)

**(a) [8]** Fit $y = c_0 + c_1x + c_2x^2$ to $(-1,4)$, $(0,1)$, $(1,0)$, $(2,1)$.

**Is the fit exact?** Give $\lVert e\rVert^2$ and say what that tells you about $b$ and $\mathbf{C}(A)$.

**(b) [4]** Explain in two sentences why fitting a parabola is **linear** least squares, and give a model in one unknown that is **not**.

**(c) [4]** You fit a degree-3 polynomial to 4 points and get $\lVert e\rVert^2 = 0$. You fit degree 2 and get $\lVert e\rVert^2 = 1.7$.

**Which model is better?** Justify — and say what you would compute to decide properly.

**(d) [4]** Show that adding a column to $A$ can **never increase** $\lVert e\rVert$. *(One sentence, about subspaces.)*

**Why is that a problem rather than a feature?**

---

### Q3: The Geometry (18 points)

**(a) [5]** For your Q1 matrix, give a basis for $\mathbf{C}(A)$ and for $\mathbf{N}(A^\mathsf{T})$, and **verify your residual $e$ lies in the second.**

**(b) [4]** Explain, in the language of the four subspaces, what $p$ and $e$ are and why $b = p + e$ is a splitting of $\mathbb{R}^4$.

**(c) [4]** Prove that $\hat x$ minimises $\lVert b - Ax\rVert$, using Pythagoras. **Where is orthogonality used?**

**(d) [5]** $A$ has **dependent** columns.

- What goes wrong with the normal equations?
- **Does the projection $p$ still exist and is it still unique?** Justify.
- Which week's material handles this case properly?

---

### Q4: Why Not the Normal Equations (24 points)

**(a) [6]** For Läuchli's matrix $A = \begin{bmatrix}1&1\\ \varepsilon&0\\ 0&\varepsilon\end{bmatrix}$, compute $A^\mathsf{T}A$ **by hand** and give $\det(A^\mathsf{T}A)$ exactly.

**At what $\varepsilon$ does $1 + \varepsilon^2$ round to $1$ in double precision?** Derive it from $\varepsilon_{\text{mach}} = 2^{-52}$.

**(b) [5]** $\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$.

Using Week 0's rule of thumb, complete: with $\operatorname{cond}(A) = 10^3$, $10^6$, $10^8$, how many of your sixteen digits survive **solving with $A$**, and how many survive **the normal equations**?

**(c) [6]** Substitute $A = QR$ into $A^\mathsf{T}A\hat x = A^\mathsf{T}b$ and reduce it to $R\hat x = Q^\mathsf{T}b$.

**Justify every cancellation**, in particular why $R^\mathsf{T}$ may be removed.

**(d) [7]** Run `resources/leastsquares.py` and reproduce the three-method table.

- **At $\varepsilon = 10^{-7}$ the normal equations give nine correct digits and Gram–Schmidt QR does not.** Explain both facts.
- **Why is the normal equations' accuracy there described as luck rather than robustness?** Support your answer with $\operatorname{cond}(A^\mathsf{T}A)$ at that $\varepsilon$.
- **What does Householder QR do differently**, and why does it not suffer from either failure?

---

### Q5: What It Assumes (16 points)

**(a) [5]** Five points lie exactly on $y = x$: $(1,1)$ through $(5,5)$. Move $(5,5)$ to $(5,15)$ and refit.

Give the new line and $\lVert e\rVert^2$. **Explain, in terms of the quantity being minimised, why one point out of five can do this.**

**(b) [4]** Now move $(3,3)$ to $(3,13)$ instead, leaving the ends alone. Refit.

**Compare the effect on the slope with (a).** Explain the difference geometrically. *(The answer is more interesting than you may expect.)*

**(c) [3]** Give the weighted normal equations, and say what weights you would use if measurement $i$ has standard deviation $\sigma_i$.

**(d) [4]** Show that $H_{ij} = \displaystyle\int_0^1 x^{i-1}x^{j-1}\,dx = \frac{1}{i+j-1}$ — **Week 0's Hilbert matrix.**

**State in two sentences what Week 0's Hilbert experiment was actually measuring**, and what it implies about fitting high-degree polynomials.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Fitting a line | 22 |
| 2 | Beyond straight lines | 20 |
| 3 | The geometry | 18 |
| 4 | Why not the normal equations | 24 |
| 5 | What it assumes | 16 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*MATH 241 · Week 9 · PS 9 · © CSE Department*
