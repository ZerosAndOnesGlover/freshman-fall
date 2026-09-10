# MATH 241 · Linear Algebra
## Week 9 · Lecture 1 of 3 · **Monday**
### Least Squares

---

**Reading:** Strang §4.3 · **Previous:** Week 8's L26, Gram–Schmidt · **Next:** L28, least squares in practice

> **Quiz 9 is the first ten minutes of this lecture** and covers Week 8.
>
> **Midterm 2 is the Wednesday of Week 10**, covering **Weeks 6–9**. **This week completes the
> examinable material.**
>
> **CS 201's and PROG 201's Project 1 are both due Friday**, at 17:00, alongside PS 8.

---

## 1. The Question Week 2 Refused to Answer

Week 2's L08 §1 established that $Ax = b$ is solvable exactly when $b \in \mathbf{C}(A)$, and Week 3 turned the failure into a checkable condition. **Neither said what to do when the answer is no.**

**And "no" is the normal case.** Whenever you have more data than parameters — $m > n$ — the system is **overdetermined**, $\mathbf{C}(A)$ is a small subspace of $\mathbb{R}^m$, and **almost every $b$ is unreachable.** Measurement error alone guarantees it.

> **So the question changes.** Not *"solve $Ax = b$"*, which is impossible, but
>
> $$\boxed{\;\text{find } \hat x \text{ minimising } \lVert b - A\hat x\rVert\;}$$
>
> **Make the error as small as it can be made.** Week 8 already solved this geometrically: the
> nearest point of $\mathbf{C}(A)$ to $b$ is the projection $p$, so **solve $A\hat x = p$ instead**,
> which *is* solvable because $p \in \mathbf{C}(A)$ by construction.

**Least squares is projection with data attached, and nothing else.**

---

## 2. The Normal Equations, Again

Week 8's L25 §3 derived them for the projection. **The derivation is unchanged**, and worth repeating because the interpretation is new: the error $e = b - A\hat x$ must be orthogonal to $\mathbf{C}(A)$, hence to every column of $A$:

$$A^\mathsf{T}(b - A\hat x) = 0 \quad\Longrightarrow\quad \boxed{\;A^\mathsf{T}A\,\hat x = A^\mathsf{T}b\;}$$

**$n$ equations in $n$ unknowns**, where the original problem had $m$ equations in $n$ unknowns and no solution. **The overdetermined problem has been replaced by a square one that always has a solution** — and has exactly one, when $A$ has independent columns, by **PS 2 Q5(c)**.

> **This is the reduction that makes the subject practical.** $A$ may be $10^6 \times 4$; $A^\mathsf{T}A$
> is $4\times4$. **A million measurements collapse to a four-by-four solve**, and PS 3 Q5(d) worked
> exactly this arithmetic in Week 3 without knowing what it was for.

---

## 3. Fitting a Line

**The canonical application.** Given points $(x_i, y_i)$, find the line $y = c + dx$ fitting them best.

$$\begin{aligned} c + d x_1 &= y_1\\ c + dx_2 &= y_2\\ &\ \vdots \end{aligned} \qquad\Longleftrightarrow\qquad \underbrace{\begin{bmatrix}1 & x_1\\ 1 & x_2\\ \vdots & \vdots\end{bmatrix}}_{A}\begin{bmatrix}c\\ d\end{bmatrix} = \underbrace{\begin{bmatrix}y_1\\ y_2\\ \vdots\end{bmatrix}}_{b}$$

**The unknowns are $c$ and $d$; the data go into $A$ and $b$.** Getting that round the right way is the only conceptual step.

### Worked, on three points

$(1,1)$, $(2,2)$, $(3,2)$ — **not collinear**, so no line passes through all three.

$$A = \begin{bmatrix}1&1\\ 1&2\\ 1&3\end{bmatrix}, \qquad b = \begin{bmatrix}1\\2\\2\end{bmatrix}, \qquad A^\mathsf{T}A = \begin{bmatrix}3&6\\ 6&14\end{bmatrix}, \qquad A^\mathsf{T}b = \begin{bmatrix}5\\ 11\end{bmatrix}$$

Solving: $\;\hat x = \left(\tfrac23,\ \tfrac12\right)$, so

$$\boxed{\;y = \tfrac23 + \tfrac12 x\;}$$

**Fitted values** $p = \left(\tfrac76, \tfrac53, \tfrac{13}{6}\right)$, **residuals** $e = \left(-\tfrac16, \tfrac13, -\tfrac16\right)$, and

$$\lVert e\rVert^2 = \tfrac{1}{36} + \tfrac19 + \tfrac{1}{36} = \tfrac16$$

**Check:** $A^\mathsf{T}e = (0,0)$ ✓ — the residual is orthogonal to both columns, which is what makes this the best line.

> **This $b$ and this $A$ are Week 8's.** L25 §4 projected $(6,0,0)$ onto the same column space, and
> the script projects $(1,2,2)$ onto it. **The projection and the line fit are one computation**, and
> seeing that they are is the point of putting them in consecutive weeks.

### And it really is a minimum

Perturbing the answer makes things worse, every time:

| change | $\lVert e\rVert^2$ |
|---|---|
| none | $\tfrac16 \approx 0.167$ |
| $c + 0.1$ | $\tfrac{59}{300} \approx 0.197$ |
| $d + 0.1$ | $\tfrac{23}{75} \approx 0.307$ |
| $c - 0.1$, $d + 0.05$ | $\tfrac{103}{600} \approx 0.172$ |

**Not a proof, but the proof is Week 8's L25 §1** — Pythagoras, and it shows the minimum is unique.

---

## 4. Why "Least Squares", and What That Chooses

**The quantity minimised is $\lVert e\rVert^2 = \sum e_i^2$** — the sum of the **squares** of the residuals. Hence the name.

**That is a choice, and it is worth knowing it was made.** You could minimise $\sum\lvert e_i\rvert$, or $\max\lvert e_i\rvert$, and both are used. **Squares win for three reasons:**

| | |
|---|---|
| **It is differentiable** | $\sum e_i^2$ is smooth; $\sum\lvert e_i\rvert$ has corners, and $\max$ has more |
| **It gives linear equations** | setting the derivative to zero produces $A^\mathsf{T}A\hat x = A^\mathsf{T}b$ — **linear**, hence solvable in closed form |
| **It is the right answer statistically** | if the errors are independent and normally distributed, least squares is the maximum-likelihood estimate. **MATH 251 next term** |

> **The cost of the choice is L29 §3:** squaring makes a residual of $10$ count **one hundred times**
> a residual of $1$, so a single outlier can drag the whole fit. **The alternatives exist precisely
> because that is sometimes unacceptable** — minimising $\sum\lvert e_i\rvert$ gives *robust*
> regression, at the price of losing the closed form.

---

## 5. The Geometry, Restated

Everything in §2 is one picture, and it is Week 3's four-subspace diagram with $b$ drawn on it.

$$\mathbb{R}^m = \mathbf{C}(A) \oplus \mathbf{N}(A^\mathsf{T}), \qquad b = \underbrace{p}_{\in\ \mathbf{C}(A)} + \underbrace{e}_{\in\ \mathbf{N}(A^\mathsf{T})}$$

| | |
|---|---|
| $p = A\hat x$ | the part of $b$ the model **can** explain |
| $e = b - p$ | the part it **cannot** — orthogonal to everything the model can produce |
| $\lVert e\rVert$ | how badly the model fits |
| $\hat x$ | the coefficients |

**$e \in \mathbf{N}(A^\mathsf{T})$ is the statement that the residual carries no information the model could have used.** If it did, the fit would not be optimal — you could reduce the error further.

> **And this is why $\mathbf{N}(A^\mathsf{T})$, the "least important" of the four subspaces
> (Strang's phrase, quoted in Week 3's reading guide), turns out to matter.** It is where the
> unexplained part of every measurement lives.

---

## 6. What Can Still Go Wrong

**$A$ must have independent columns.** Otherwise $A^\mathsf{T}A$ is singular, there is no unique $\hat x$, and the normal equations have infinitely many solutions. **The projection $p$ still exists and is still unique** — the subspace is fine — but the coefficients producing it are not determined.

**When does that happen in practice?** When two predictors are **redundant**: measuring a length in both metres and feet, or including both "years of education" and "years since starting school". **The model is over-parameterised**, and the fix is to remove a column, not to fight the algebra.

> **Week 11's SVD handles this case properly**, producing the $\hat x$ of smallest norm among all
> minimisers — the *pseudoinverse*. **It is the only method in this course that never fails**, and
> Week 8's L26 §4 table already predicted that.

**And even with independent columns, the computation can be delicate** — which is L28's entire subject, and the reason it is a separate lecture.

---

## 7. What to Take Away

1. **Overdetermined systems are the normal case**, and "no solution" is not an answer. **Minimise $\lVert b - Ax\rVert$ instead.**
2. **Least squares is Week 8's projection with data attached.** Solve $A\hat x = p$, which is solvable by construction.
3. **The normal equations $A^\mathsf{T}A\hat x = A^\mathsf{T}b$** replace $m$ equations with $n$, and have a unique solution when $A$ has independent columns.
4. **Fitting a line: unknowns in $\hat x$, data in $A$ and $b$.** The columns are $1$ and $x$ evaluated at the data points.
5. **Check by $A^\mathsf{T}e = 0$**, always — the same discipline as Week 8.
6. **"Squares" is a choice**, justified by differentiability, linearity and (in MATH 251) maximum likelihood — **and it is what makes outliers loud.**
7. **$b = p + e$ splits the data into what the model explains and what it cannot**, and $e$ lives in the left null space.
8. **Dependent columns break $\hat x$ but not $p$.** Week 11 fixes it.

---

## Exercises

*(Not assessed. PS 9 is the assessed work.)*

1. Fit a line to $(0,1)$, $(1,3)$, $(2,4)$. Give $\hat x$, the fitted values, the residuals and $\lVert e\rVert^2$. **Check $A^\mathsf{T}e = 0$.**
2. Fit a **horizontal** line $y = c$ to the same data. **Show that $\hat c$ is the mean of the $y_i$**, and say why that is not a coincidence.
3. Three points **are** collinear. What are $e$ and $\lVert e\rVert^2$? What is the projection $p$?
4. Show that the least-squares line always passes through $(\bar x, \bar y)$, the centroid of the data. *(Look at the first normal equation.)*
5. $A$ is $100\times3$. What size is $A^\mathsf{T}A$? How many equations does the normal system have, against the original?
6. Fit $y = c + dx$ to $(1,1)$, $(2,2)$, $(3,2)$ by **minimising $\sum e_i^2$ directly** — differentiate with respect to $c$ and $d$ and set both to zero. **Confirm you recover the normal equations.**

---

*MATH 241 · Week 9 · L27 · © CSE Department*
