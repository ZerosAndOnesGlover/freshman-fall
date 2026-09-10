# MATH 241 · Problem Set 9 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Exact in Q1–Q3 and Q5**; Q4 is floating point and says so. `resources/leastsquares.py` reproduces everything.

**What this paper is testing.** Q1 and Q2 are the mechanical core and are Midterm-2 material. **Q4(d) is the best question on the paper** — it asks the student to explain a table in which the *wrong* method looks right and the recommended one looks wrong, which cannot be answered by recall. **Q5(b) is the paper's surprise**: the middle outlier does more damage to the residual and none at all to the slope.

**Common failure modes:** (1) Q2(c) answering "degree 3, the residual is zero"; (2) Q4(d) explaining only the normal-equations column; (3) Q5(b) predicted rather than computed, and predicted wrong; (4) Q3(d) claiming $p$ is also non-unique.

---

## Q1: Fitting a Line (22 points)

### (a) [8]

$$A = \begin{bmatrix}1&0\\1&1\\1&2\\1&3\end{bmatrix}, \quad b = \begin{bmatrix}1\\2\\4\\4\end{bmatrix}, \quad A^\mathsf{T}A = \begin{bmatrix}4&6\\6&14\end{bmatrix}, \quad A^\mathsf{T}b = \begin{bmatrix}11\\22\end{bmatrix}$$

Solving: $4c + 6d = 11$, $6c + 14d = 22$. Multiply the first by $3$ and the second by $2$: $12c + 18d = 33$, $12c + 28d = 44$; subtract to get $10d = 11$, so $d = \tfrac{11}{10}$, then $c = \tfrac{11}{10}$.

$$\boxed{\;y = \tfrac{11}{10} + \tfrac{11}{10}\,x\;}$$

### (b) [5]

$$p = \left(\tfrac{11}{10},\ \tfrac{11}{5},\ \tfrac{33}{10},\ \tfrac{22}{5}\right), \qquad e = \left(-\tfrac{1}{10},\ -\tfrac15,\ \tfrac{7}{10},\ -\tfrac25\right), \qquad \lVert e\rVert^2 = \tfrac{7}{10}$$

$$A^\mathsf{T}e = \left(\textstyle\sum e_i,\ \sum x_ie_i\right) = (0,\ 0)\ ✓$$

### (c) [4]

**The first normal equation is $\sum(y_i - c - dx_i) = 0$**, i.e. $\sum e_i = 0$, which rearranges to

$$\sum y_i = mc + d\sum x_i \quad\Longrightarrow\quad \bar y = c + d\bar x.$$

**So $(\bar x, \bar y)$ satisfies the fitted line, always.** ✓ Here $\bar x = \tfrac32$, $\bar y = \tfrac{11}{4}$, and $\tfrac{11}{10} + \tfrac{11}{10}\cdot\tfrac32 = \tfrac{11}{4}$ ✓

*Marking: 2 for the check, 2 for the general proof. **The general proof is the question**; verifying on the data alone gets 2.*

### (d) [5]

With $A = (1,1,1,1)^\mathsf{T}$: $A^\mathsf{T}A = 4$, $A^\mathsf{T}b = \sum y_i = 11$, so $\hat c = \tfrac{11}{4} = \bar y$ ✓

**In this week's language: the mean is the projection of the data onto the space of constant vectors** — the single number that best approximates the data in the least-squares sense. **The mean is a least-squares fit**, which is not a metaphor.

*Marking: 3 for the computation, 2 for the interpretation. **The interpretation is the point** and most scripts will stop at the arithmetic.*

---

## Q2: Beyond Straight Lines (20 points)

### (a) [8]

$$y = 1 - 2x + x^2 = (x-1)^2, \qquad \lVert e\rVert^2 = \mathbf{0}$$

**The fit is exact.** The four points lie on that parabola, so $b \in \mathbf{C}(A)$ and the projection of $b$ is $b$ itself.

*Check: $x = -1 \to 4$ ✓, $0 \to 1$ ✓, $1 \to 0$ ✓, $2 \to 1$ ✓*

### (b) [4]

**Linear because the unknowns $c_0, c_1, c_2$ appear linearly** — the model is $c_0\cdot 1 + c_1\cdot x + c_2\cdot x^2$, a linear combination of three fixed functions. **The curvature is in the basis functions, not in the parameters**, and least squares never looks at $x$ except to build the columns.

**Not linear:** $y = c_0e^{c_1x}$ — the unknown $c_1$ sits inside the exponential. *(Accept $y = \sin(c_1x)$, $y = c_0/(x + c_1)$, etc.)*

### (c) [4]

**Neither, on this evidence — and "degree 3" is the wrong answer.**

**A degree-3 polynomial through 4 points always has $\lVert e\rVert^2 = 0$**, because $A$ is then $4\times4$ with independent columns, so $\mathbf{C}(A) = \mathbb{R}^4$ and every $b$ is reachable. **The zero residual is guaranteed by the arithmetic and carries no information about the model.**

**What to compute instead:** the fit's performance on **data not used to fit it** — hold out points, or cross-validate. *(Accept: an information criterion, a residual plot, or new measurements.)*

*Marking: 2 for rejecting the degree-3 conclusion with the right reason, 2 for proposing out-of-sample evaluation. **A script answering "degree 3, it fits perfectly" earns 0** and should be told plainly that this is the central error of the lecture.*

### (d) [4]

**Adding a column enlarges $\mathbf{C}(A)$**, and the projection onto a larger subspace is at least as close to $b$ — so $\lVert e\rVert$ cannot increase.

**Why that is a problem:** it means **$\lVert e\rVert$ can never be used to compare models of different sizes.** A smaller residual is guaranteed by adding parameters, so it is not evidence of anything. **Taken to the limit you get an exact fit that predicts nothing — overfitting.**

---

## Q3: The Geometry (18 points)

### (a) [5]

$\mathbf{C}(A) = \operatorname{span}\{(1,1,1,1),\ (0,1,2,3)\}$, a plane in $\mathbb{R}^4$.

$\mathbf{N}(A^\mathsf{T})$ has dimension $4 - 2 = 2$; solving $A^\mathsf{T}y = 0$ (i.e. $\sum y_i = 0$ and $\sum x_iy_i = 0$) gives a basis such as

$$(1,-2,1,0), \qquad (0,1,-2,1)$$

**And $e = \left(-\tfrac{1}{10},-\tfrac15,\tfrac{7}{10},-\tfrac25\right)$ satisfies both:** $\sum e_i = 0$ ✓ and $\sum x_ie_i = 0$ ✓, which is exactly $A^\mathsf{T}e = 0$.

*Accept any valid basis. Marking: 2 for $\mathbf{C}(A)$, 2 for $\mathbf{N}(A^\mathsf{T})$, 1 for the verification.*

### (b) [4]

$$\mathbb{R}^4 = \mathbf{C}(A) \oplus \mathbf{N}(A^\mathsf{T})$$

**$p$ is the part of the data the model can produce**; **$e$ is the part it cannot**, and $e$ is orthogonal to everything the model could ever output. **The splitting is unique** (Week 8's L24 §4), which is why the best fit is unique.

### (c) [4]

For any $x$, write $b - Ax = (b - A\hat x) + (A\hat x - Ax) = e + A(\hat x - x)$. The second term is in $\mathbf{C}(A)$ and $e \perp \mathbf{C}(A)$, so by Pythagoras

$$\lVert b - Ax\rVert^2 = \lVert e\rVert^2 + \lVert A(\hat x - x)\rVert^2 \ \ge\ \lVert e\rVert^2$$

with equality iff $A(\hat x - x) = 0$. $\square$

**Orthogonality is used to kill the cross term** — that is the whole of the proof.

### (d) [5]

- **The normal equations become singular**: $A^\mathsf{T}A$ is not invertible, so $\hat x$ is not unique — there are infinitely many minimisers.
- **$p$ still exists and is still unique.** The projection depends only on the **subspace** $\mathbf{C}(A)$, which is perfectly well defined; only the *coefficients* expressing $p$ in terms of dependent columns are ambiguous.
- **Week 11**, via the pseudoinverse — which selects the minimiser of smallest norm.

*Marking: 2, 2, 1. **A script claiming $p$ is also non-unique has confused the subspace with the basis** and should be corrected explicitly.*

---

## Q4: Why Not the Normal Equations (24 points)

### (a) [6]

$$A^\mathsf{T}A = \begin{bmatrix}1+\varepsilon^2 & 1\\ 1 & 1+\varepsilon^2\end{bmatrix}, \qquad \det = (1+\varepsilon^2)^2 - 1 = 2\varepsilon^2 + \varepsilon^4$$

**$1 + \varepsilon^2$ rounds to $1$ when $\varepsilon^2 < \varepsilon_{\text{mach}} = 2^{-52}$**, i.e.

$$\varepsilon < 2^{-26} = 1.49\times10^{-8}$$

*(Matches the table: fine at $10^{-7}$, singular at $10^{-8}$.)*

### (b) [5]

Digits surviving $\approx 16 - \log_{10}\operatorname{cond}$:

| $\operatorname{cond}(A)$ | solving with $A$ | $\operatorname{cond}(A^\mathsf{T}A)$ | normal equations |
|---:|---:|---:|---:|
| $10^{3}$ | 13 | $10^{6}$ | 10 |
| $10^{6}$ | 10 | $10^{12}$ | 4 |
| $10^{8}$ | 8 | $10^{16}$ | **0** |

**Squaring the condition number doubles the digits lost.**

### (c) [6]

$$(QR)^\mathsf{T}(QR)\hat x = (QR)^\mathsf{T}b \;\Rightarrow\; R^\mathsf{T}\underbrace{Q^\mathsf{T}Q}_{I}R\hat x = R^\mathsf{T}Q^\mathsf{T}b \;\Rightarrow\; R^\mathsf{T}R\hat x = R^\mathsf{T}Q^\mathsf{T}b$$

**$R$ is invertible** — its diagonal holds the Gram–Schmidt norms $\lVert w_j\rVert$, all nonzero because the columns of $A$ are independent (Week 8's L26 §4). **Hence $R^\mathsf{T}$ is invertible**, and multiplying both sides by $(R^\mathsf{T})^{-1}$ gives

$$\boxed{\;R\hat x = Q^\mathsf{T}b\;}$$

*Marking: 4 for the algebra, 2 for justifying the $R^\mathsf{T}$ cancellation via invertibility. **A script that "cancels $R^\mathsf{T}$ from both sides" without saying why gets 4.***

### (d) [7]

**The normal equations at $\varepsilon = 10^{-7}$.** $1 + \varepsilon^2 = 1.00000000000001$ is still distinguishable from $1$, so $\det = 2\times10^{-14}$ is computed nonzero, and for this **symmetric $2\times2$** the arithmetic happens to cancel favourably — nine correct digits.

**Gram–Schmidt QR at $\varepsilon = 10^{-7}$.** The two columns $(1,\varepsilon,0)$ and $(1,0,\varepsilon)$ are **nearly parallel**, so the subtraction $a_2 - (q_1^\mathsf{T}a_2)q_1$ cancels catastrophically: the result is a small vector computed as a difference of large nearly equal ones, and the computed $q_2$ is badly non-orthogonal to $q_1$. **Week 8's L26 §5 predicted exactly this**, and here it is measured.

**Why the normal equations' accuracy is luck.** $\operatorname{cond}(A) \approx \sqrt2/\varepsilon = 1.4\times10^{7}$, so $\operatorname{cond}(A^\mathsf{T}A) \approx 2\times10^{14}$ — **the problem as posed to the solver has at most two reliable digits.** Nine correct digits from a system that ill-conditioned is a coincidence of this particular $2\times2$'s structure, and **the coincidence fails completely one step later**, at $\varepsilon = 10^{-8}$, where $A^\mathsf{T}A$ goes exactly singular.

**Householder.** Builds $Q$ as a product of reflections $H = I - 2vv^\mathsf{T}$, each **exactly orthogonal by construction** rather than by accumulation, with the sign of $v$ chosen to avoid cancellation. **Nothing is subtracted in the vulnerable way**, $A^\mathsf{T}A$ is never formed, and the whole computation runs at $\operatorname{cond}(A)$ rather than its square. **Right to nine digits at every $\varepsilon$ in the table.**

*Marking: 2 + 2 + 3. **The third part — luck rather than robustness — is what separates a strong script.** A student who explains only why the normal equations eventually fail, without addressing why they look good first, has answered half the question.*

---

## Q5: What It Assumes (16 points)

### (a) [5]

$(1,1)$ … $(4,4)$, $(5,15)$:

$$\boxed{\;y = -4 + 3x\;}, \qquad \lVert e\rVert^2 = 40$$

**The slope has tripled**, and the other four points are still exactly on $y = x$.

**Why:** least squares minimises $\sum e_i^2$, so **a residual of 10 costs 100 while a residual of 1 costs 1.** The fit will accept substantial error at four points to reduce the error at the fifth, because that one is being charged quadratically.

### (b) [4]

$(1,1)$, $(2,2)$, $(3,13)$, $(4,4)$, $(5,5)$:

$$\boxed{\;y = 2 + 1\,x\;}, \qquad \lVert e\rVert^2 = 80$$

**The slope is unchanged at exactly 1** — only the intercept moved, from 0 to 2. **And the residual is twice as large as in (a).**

**The geometry: leverage.** $x = 3$ is exactly $\bar x$, the mean of the $x$-values. By Q1(c) the line must pass through $(\bar x, \bar y)$, and moving a point at $\bar x$ **moves $\bar y$ and nothing else** — it shifts the line up without tilting it. **A point at the centre has no leverage on the slope; a point at the end has the most.**

> **Worth stating on the script:** the more damaging outlier for the *fit* produced the *smaller*
> residual. **$\lVert e\rVert$ does not measure how much an outlier distorted the model.**

*Marking: 2 for the line and residual, 2 for the leverage explanation. **Most scripts will predict the slope changes and be wrong** — the paper warned them the answer is more interesting than expected.*

### (c) [3]

$$A^\mathsf{T}W^2A\,\hat x = A^\mathsf{T}W^2b, \qquad W = \operatorname{diag}(\sqrt{w_i})$$

**Weights $w_i = 1/\sigma_i^2$** — inverse variances, so noisier measurements count less. *(MATH 251 proves this is the maximum-likelihood choice.)*

### (d) [4]

$$\int_0^1 x^{i-1}x^{j-1}dx = \int_0^1 x^{i+j-2}dx = \left[\frac{x^{i+j-1}}{i+j-1}\right]_0^1 = \frac{1}{i+j-1} = H_{ij} \qquad\square$$

**What Week 0 was measuring.** $H$ is the **Gram matrix of $1, x, x^2, \dots$** under the inner product $\int_0^1fg$ — that is, $A^\mathsf{T}A$ for polynomial fitting. **So Week 0's Hilbert experiment was measuring the conditioning of polynomial least squares**, six weeks before least squares was defined.

**The implication:** fitting high-degree polynomials in the basis $1, x, x^2, \dots$ is **catastrophically ill-conditioned** — $\operatorname{cond}(H_{12}) = 4\times10^{16}$, two correct digits out of sixteen. **Use an orthogonal basis instead** (Legendre), which is Week 8's Gram–Schmidt and is why those families exist.

*Marking: 2 for the integral, 2 for the two sentences. **The connection back to Week 0 is the question**; a script that computes the integral and stops gets 2.*

---

## Grade Distribution Expected

| Band | Score | Description |
|---|---|---|
| Strong | 88–100 | Q2(c) rejecting the zero residual, Q4(d) all three parts, Q5(b)'s leverage explanation |
| Solid | 72–87 | Q1–Q3 correct; Q4 computed; Q5(b) computed but not explained |
| Passing | 55–71 | Fits computed and verified with $A^\mathsf{T}e = 0$ |
| Concerning | < 55 | **Q2(c) answered "degree 3".** It is the central misconception of the week and it is on the midterm |

---

*MATH 241 · Week 9 · PS 9 Solutions · © CSE Department*
