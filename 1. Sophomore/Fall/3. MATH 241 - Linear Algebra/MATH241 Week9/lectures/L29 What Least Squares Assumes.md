# MATH 241 · Linear Algebra
## Week 9 · Lecture 3 of 3 · **Friday**
### What Least Squares Assumes

*“Far better an approximate answer to the right question, which is often vague, than an exact answer to the wrong question, which can always be made precise.”* — John Tukey, "The Future of Data Analysis", *Annals of Mathematical Statistics* 33(1) (1962)

---

**Reading:** Strang §4.3 (the applications), §8.6 · **Previous:** L28, least squares in practice · **Next:** Week 10, symmetric matrices

**Coursework:** 📝 **PS 8** due today 17:00 · 📊 **Quiz 10** Mon of Week 10 · 📝 **PS 10** released Wed of Week 10, due Fri of Week 11 17:00 · 💬 **Recitation 9** Thu of Week 10 15:00–15:50

> **PS 8 is due at 17:00 today**, alongside CS 201's and PROG 201's Project 1. **PS 9 was released
> Wednesday and is due the Friday of Week 10.**
>
> **Midterm 2 is next Wednesday**, 18:00–19:15, SSB 110, covering **Weeks 6–9**. **This lecture
> completes the examinable material.**

---

## 1. "Linear" Means Linear in the Unknowns

**The most useful thing to understand about least squares is how much it covers**, and the answer surprises people.

$$y = c_0 + c_1x + c_2x^2$$

is a **parabola** — plainly not a straight line — and fitting it is **linear least squares**, because the unknowns $c_0, c_1, c_2$ appear linearly. **The model may be as curved as you like in $x$; what matters is that it is linear in the parameters.**

$$A = \begin{bmatrix}1 & x_1 & x_1^2\\ 1 & x_2 & x_2^2\\ \vdots\end{bmatrix}$$

**The columns are the basis functions evaluated at the data points**, and nothing else changes — same normal equations, same QR, same everything.

### Worked

Data $(0,1)$, $(1,3)$, $(2,7)$, $(3,13)$. Fitting $y = c_0 + c_1x + c_2x^2$:

$$\hat x = (1, 1, 1) \quad\Longrightarrow\quad y = 1 + x + x^2, \qquad \lVert e\rVert^2 = 0$$

**An exact fit** — the four points happen to lie on that parabola, so $b \in \mathbf{C}(A)$ and the residual is zero. **Least squares handles that case without special-casing it**, which is worth noticing: the projection of a point already in the subspace is itself.

### What else is covered

| Model | Columns of $A$ |
|---|---|
| $c_0 + c_1x$ | $1$, $x$ |
| polynomial of degree $d$ | $1, x, \dots, x^d$ |
| $c_1\sin x + c_2\cos x$ | $\sin x$, $\cos x$ |
| $c_0 + c_1x_1 + c_2x_2 + \dots$ *(several predictors)* | one column per predictor |
| $c_1e^{-x} + c_2e^{-2x}$ | $e^{-x}$, $e^{-2x}$ |

**And what is not:** $y = c_0e^{c_1x}$ — the unknown $c_1$ is inside the exponential. **That is *nonlinear* least squares**, needs iteration, and has no closed form. *(Though taking logs turns this particular one into a linear fit, at the cost of changing which errors you are minimising — a trade worth knowing about.)*

---

## 2. Fitting Is Projection Onto a Space of Functions

**Week 8's L26 §3 orthogonalised $1$, $x$, $x^2$ sampled at three points** and produced the discrete Legendre vectors. **That was this computation**, seen from the other side.

**Choosing a model is choosing a subspace.** $\mathbf{C}(A)$ is the set of all functions your model can produce, sampled at the data points, and **the fit is the projection of the data onto it.** More basis functions means a bigger subspace, a smaller residual, and — §4 — not necessarily a better model.

> **This is the thread to Week 12.** Replace the data points by a whole interval and the dot product
> by $\int fg$, and the same projection produces **Fourier coefficients**: the best approximation to
> a function by a combination of sines and cosines. **PS 8 Q3(d) already did the polynomial version
> on $[-1,1]$**, getting $1$, $x$, $x^2 - \tfrac13$.

---

## 3. One Outlier Moves Everything

**Five points exactly on $y = x$.** Fit a line, then move **one** of them:

| data | fitted line | $\lVert e\rVert^2$ |
|---|---|---|
| unchanged | $y = 0 + 1\,x$ | $0$ |
| $(5,5) \to (5,7)$ | $y = -\tfrac45 + \tfrac75\,x$ | $\tfrac85$ |
| $(5,5) \to (5,15)$ | $y = -4 + 3\,x$ | $40$ |

**Moving one point out of five by 10 changes the slope from 1 to 3.** The other four points are still exactly on $y = x$, and the fitted line no longer goes near any of them.

**This is not a defect in the arithmetic.** It is the direct consequence of L27 §4's choice: **minimising $\sum e_i^2$ means a residual of $10$ counts one hundred times a residual of $1$.** A single far-away point can outvote the rest of the data, because its squared error dominates the sum.

> **Three responses, and choosing between them is a modelling decision rather than a mathematical
> one.**
>
> **Remove the outlier** — if you have grounds to believe it is an error. Requires judgement and is
> easy to abuse.
> **Change the norm.** Minimising $\sum\lvert e_i\rvert$ gives **robust regression**: far less
> sensitive, no closed form, solved by linear programming.
> **Weight the points.** Minimise $\sum w_ie_i^2$, giving suspect measurements less say — which is
> §5.

---

## 4. More Columns Always Fit Better, and That Is the Problem

**Adding a basis function can only reduce $\lVert e\rVert$**, because it enlarges $\mathbf{C}(A)$ and the projection onto a larger subspace is at least as close. **With $n = m$ independent columns the residual is exactly zero** — a polynomial of degree $m-1$ passes through all $m$ points.

**So "the residual got smaller" is never evidence that a model is better.** It is guaranteed.

**And the fit gets worse in the way that matters.** A degree-9 polynomial through 10 noisy points oscillates violently between them; it reproduces the data exactly and predicts nothing. **This is *overfitting*, and it is a whole subject** — CS 331's, mostly.

> **The linear-algebra symptom is conditioning.** The Vandermonde matrix
> $$A = \begin{bmatrix}1 & x_1 & x_1^2 & \cdots\\ 1 & x_2 & x_2^2 & \cdots\\ \vdots\end{bmatrix}$$
> becomes **spectacularly ill-conditioned** as the degree rises — its columns $1, x, x^2, \dots$ are
> nearly parallel on any short interval, because $x^7$ and $x^8$ look almost identical there.
>
> **Which is exactly Week 0's Hilbert matrix**, and not by analogy: $H_{ij} = 1/(i+j-1)$ **is**
> $\int_0^1 x^{i-1}x^{j-1}dx$, the Gram matrix of $1, x, x^2, \dots$ under the function inner
> product. **$\operatorname{cond}(H_{12}) = 4\times10^{16}$**, and Week 0's L03 §6 measured two
> correct digits out of sixteen. **That was polynomial fitting all along**, six weeks before least
> squares existed.
>
> **The fix is an orthogonal basis** — Legendre polynomials instead of $1, x, x^2$ — which is
> Week 8's Gram–Schmidt, and it is why orthogonal polynomial families exist at all.

---

## 5. Weighted Least Squares, in One Line

**If some measurements are more reliable than others**, say so. Minimise

$$\sum_i w_i e_i^2 \qquad\text{instead of}\qquad \sum_i e_i^2$$

which is ordinary least squares applied to $WA$ and $Wb$, where $W = \operatorname{diag}(\sqrt{w_i})$:

$$\boxed{\;A^\mathsf{T}W^2A\,\hat x = A^\mathsf{T}W^2b\;}$$

**No new theory** — scale the rows and run the same algorithm. **The right weights are $w_i = 1/\sigma_i^2$**, the inverse variances, which is a statistical statement and is **MATH 251's**.

---

## 6. What It Assumes, Collected

**Least squares is a tool with a specification, and it is worth reading it once:**

| Assumption | If violated |
|---|---|
| The model is **linear in the parameters** | Different subject: nonlinear least squares, iterative |
| The columns are **independent** | $\hat x$ not unique. $p$ still is. **Week 11's pseudoinverse** |
| **All errors are in $b$**, none in $A$ | Total least squares is a different problem, and also Week 11 |
| Errors are **comparable in size** | Weight them — §5 |
| Errors are **not wildly outlying** | §3. Change the norm |
| You want to **minimise squared error** | Sometimes you do not |

> **None of these is a mathematical requirement.** The algebra runs regardless and returns a number
> every time. **They are the conditions under which the number means what you think it means** — and
> the reason this lecture exists is that the arithmetic will never tell you one has failed.

---

## 7. What to Take Away

1. **"Linear" refers to the parameters, not the model.** Polynomials, sinusoids and exponential sums are all linear least squares; $c_0e^{c_1x}$ is not.
2. **Choosing a model is choosing a subspace**, and the fit is the projection onto it — **the same computation as Week 8's Gram–Schmidt, from the other side.**
3. **One outlier can dominate**, because squaring makes a residual of 10 count 100 times one of 1. That is L27 §4's choice, not a law.
4. **More columns always reduce the residual**, so a smaller residual is never evidence of a better model. **Overfitting is the failure**, and the linear-algebra symptom is a Vandermonde matrix going ill-conditioned.
5. **Week 0's Hilbert matrix was polynomial fitting** — $H_{ij} = \int_0^1x^{i+j-2}dx$ — and its $\operatorname{cond} = 4\times10^{16}$ was this problem, six weeks early.
6. **Weighted least squares is row scaling**, and the right weights are inverse variances.
7. **The algebra always returns an answer.** Whether it means anything depends on assumptions the arithmetic cannot check.

---

## Exercises

*(Not assessed. PS 9 is due Friday of Week 10 — the week of Midterm 2.)*

1. Fit $y = c_0 + c_1x + c_2x^2$ to $(-1,2)$, $(0,1)$, $(1,2)$, $(2,5)$. **Is the fit exact?**
2. Fit $y = c_1\sin x + c_2\cos x$ to three data points of your choosing. **Write down $A$ and say what its columns are.**
3. Take the five points on $y = x$ from §3 and move $(3,3)$ to $(3,8)$ instead. **Does a middle outlier move the slope as much as an end one?** Explain geometrically.
4. Show that fitting a degree-$(m-1)$ polynomial to $m$ points gives $\lVert e\rVert = 0$. **What is $\mathbf{C}(A)$ in that case?**
5. Compute $\int_0^1 x^{i-1}x^{j-1}dx$ and confirm it is $H_{ij} = 1/(i+j-1)$. **State in one sentence what Week 0's Hilbert experiment was really measuring.**
6. Derive the weighted normal equations $A^\mathsf{T}W^2A\hat x = A^\mathsf{T}W^2b$ by applying ordinary least squares to $WA$ and $Wb$.
7. **You fit a model and the residual is exactly zero.** Give two very different explanations, and say what you would compute next to tell them apart.

---

*MATH 241 · Week 9 · L29 · © CSE Department*
