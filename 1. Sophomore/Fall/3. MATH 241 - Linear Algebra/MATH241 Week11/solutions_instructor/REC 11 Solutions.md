# MATH 241 · Recitation 11 — TA Notes and Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Thursday of Week 12, 15:00–15:50, SSB 108.**
**PS 11 and PS 12 are both due 17:00 the following day.** This is the first session after Thanksgiving recess.

**Shape of the session.** §0 at home. §1 ten minutes, §2 ten, §3 ten, §4 ten, §5 the rest. **§1 is the session.** If the room cannot do the four steps unaided by minute fifteen, abandon §2(c) and §4 and run §1 again on $K$ from §3 — it is rank one and finishes in three minutes.

> **Expect a cold room.** Ten days away from the material, two problem sets due tomorrow, and the
> final in eleven days. **Start with §0 on the board immediately** — the arithmetic re-engages people
> faster than a recap does.

**Every number below is checked by `svd.py`'s exact routines** — $R = U\Sigma V^\mathsf{T}$ in `Fraction`, and $K^+ = K^\mathsf{T}/225$ by the Penrose condition $KK^+K = K$.

---

## §0 + §1 — The Drill (10 min)

$$R^\mathsf{T}R = \begin{bmatrix}5&12\\-12&-12\end{bmatrix}\begin{bmatrix}5&-12\\12&-12\end{bmatrix} = \begin{bmatrix}169&-204\\-204&288\end{bmatrix}.$$

Trace $457$, determinant $169\cdot288 - 204^2 = 48{,}672 - 41{,}616 = 7{,}056$. **$\lambda^2 - 457\lambda + 7056 = (\lambda - 441)(\lambda - 16)$.**

### (a)

$$\sigma_1 = 21, \qquad \sigma_2 = 4.$$

**Checks:** $21\cdot4 = 84 = \lvert\det R\rvert$ ($\det R = -60 + 144 = 84$) ✓, and $21^2 + 4^2 = 457 = 25 + 144 + 144 + 144$ ✓.

### (b)

$(R^\mathsf{T}R - 441I)v = 0$: $\begin{bmatrix}-272&-204\\-204&-153\end{bmatrix}$, both rows proportional to $(4, 3)$, so $v_1 \perp (4,3)$:

$$v_1 = \tfrac15(3,-4), \qquad v_2 = \tfrac15(4,3).$$

**Signs are a choice.** Accept $\pm$; §1(c) fixes the $u$'s to match whatever was chosen.

### (c)

$$Rv_1 = \tfrac15(15 + 48,\ 36 + 48) = \tfrac15(63, 84) = 21\cdot\tfrac15(3,4) \quad\Longrightarrow\quad u_1 = \tfrac15(3,4)$$
$$Rv_2 = \tfrac15(20 - 36,\ 48 - 36) = \tfrac15(-16, 12) = 4\cdot\tfrac15(-4,3) \quad\Longrightarrow\quad u_2 = \tfrac15(-4,3)$$

$u_1\cdot u_2 = \tfrac1{25}(-12 + 12) = 0$ ✓. **Automatic by L33 §2**: the $u$'s inherit orthonormality from the $v$'s through $R^\mathsf{T}R$ — which is Week 10's spectral theorem.

### (d)

$$R = \underbrace{\tfrac15\begin{bmatrix}3&-4\\4&3\end{bmatrix}}_{U}\begin{bmatrix}21&0\\0&4\end{bmatrix}\underbrace{\tfrac15\begin{bmatrix}3&-4\\4&3\end{bmatrix}}_{V^\mathsf{T}}$$

$(1,1)$ entry: $\tfrac1{25}(3\cdot21\cdot3 + (-4)\cdot4\cdot4) = \tfrac1{25}(189 - 64) = \tfrac{125}{25} = 5$ ✓.

> **Worth pointing out:** $U$ and $V^\mathsf{T}$ are *the same matrix* here. That is a coincidence of
> this example, not a symmetry of $R$ — $R$ is not symmetric. **Ask the room whether it means
> anything.** It doesn't; $V$ itself is the transpose, and it rotates the other way.

---

## §2 — Eigenvalues Are Not Singular Values (10 min)

### (a)

$\lambda^2 + 7\lambda + 84 = 0$, discriminant $49 - 336 = -287$:

$$\lambda = -\tfrac72 \pm \tfrac{\sqrt{287}}{2}\,i \approx -3.5 \pm 8.4705\,i.$$

**Complex.** Week 7's complex eigenvalues — a real matrix with a rotational component.

### (b)

**Singular values are square roots of eigenvalues of $A^\mathsf{T}A$, which is symmetric positive semidefinite, so those eigenvalues are real and $\ge 0$ (Week 10).** A real square root of a non-negative real is real.

### (c)

$\lvert\lambda\rvert^2 = \lambda\bar\lambda = \det R = 84$, so $\lvert\lambda\rvert = \sqrt{84} \approx 9.165$ for **both** — **between $4$ and $21$** ✓.

**Proof** for any square $A$, complex eigenvector allowed: $\lvert\lambda\rvert\,\lVert x\rVert = \lVert Ax\rVert$, and $\sigma_\min\lVert x\rVert \le \lVert Ax\rVert \le \sigma_\max\lVert x\rVert$ (L33 §4, which holds for complex vectors with the same argument). Divide by $\lVert x\rVert$. $\square$

> **This is the one inequality connecting the two lists**, and it is the right thing to leave the
> room with: **eigenvalues live inside the singular-value range, and nothing more precise is true in
> general.** For symmetric matrices they are the singular values up to sign (Week 10's L32 §7).

### (d)

$U = \tfrac15\begin{bmatrix}3&-4\\4&3\end{bmatrix}$ rotates by $\arctan(4/3) = 53.13°$. $V = \tfrac15\begin{bmatrix}3&4\\-4&3\end{bmatrix}$ rotates by $-53.13°$, so $V^\mathsf{T}$ rotates by $+53.13°$. **Read right to left:** turn $53.13°$, stretch by $21$ and $4$, turn another $53.13°$.

*(Script check: `det U = 1`, `det V = 1`, angles $53.1301°$ and $-53.1301°$.)*

---

## §3 — Rank One, and Its Pseudoinverse (10 min)

### (a)

$$K = \begin{bmatrix}2\\1\\-2\end{bmatrix}\begin{bmatrix}4&-3\end{bmatrix}, \qquad \sigma_1 = \lVert(2,1,-2)\rVert\cdot\lVert(4,-3)\rVert = 3\cdot5 = 15,$$
$$u_1 = \tfrac13(2,1,-2), \qquad v_1 = \tfrac15(4,-3), \qquad \sigma_2 = 0.$$

*(Script: $K^\mathsf{T}K = \begin{bmatrix}144&-108\\-108&81\end{bmatrix}$, trace $225 = 15^2$, determinant $0$.)*

### (b)

$A^+ = v\,\sigma^{-1}u^\mathsf{T} = \dfrac{\sigma vu^\mathsf{T}}{\sigma^2} = \dfrac{(\sigma uv^\mathsf{T})^\mathsf{T}}{\sigma^2} = \dfrac{A^\mathsf{T}}{\sigma^2}$.

$$K^+ = \frac{K^\mathsf{T}}{225} = \frac{1}{225}\begin{bmatrix}8&4&-8\\-6&-3&6\end{bmatrix}.$$

### (c)

$$x^+ = K^+b = \tfrac1{225}(8 + 4 - 8,\ -6 - 3 + 6) = \tfrac1{225}(4, -3).$$

$$p = Kx^+ = \begin{bmatrix}2\\1\\-2\end{bmatrix}\cdot\frac{4\cdot4 + (-3)(-3)}{225} = \tfrac{25}{225}(2,1,-2) = \tfrac19(2,1,-2).$$

**Week 8's way:** $p = (b\cdot u_1)u_1 = \tfrac{2 + 1 - 2}{3}\cdot\tfrac13(2,1,-2) = \tfrac19(2,1,-2)$ ✓.

### (d)

$(3,4) \perp (4,-3)$, so $K(3,4) = (2,1,-2)(12 - 12) = 0$: **$(3,4)$ spans $\mathbf{N}(K)$.** $x^+ = \tfrac1{225}(4,-3)$ is a multiple of $v_1$, in the row space, perpendicular to $(3,4)$ — so $\lVert x^+ + t(3,4)\rVert^2 = \lVert x^+\rVert^2 + 25t^2$, **minimised at $t = 0$.** Pythagoras again, as in L34 §4.

---

## §4 — Ten Minutes With a Machine (10 min)

### (a)

**$\sigma_3 = 16.047980$** is the distance from $A$ to the nearest rank-2 matrix — Eckart–Young, L35 §1. **No rank-2 matrix is closer than that, by the theorem**; the table is evidence, not proof. The $1\%$ nudge nearly ties because $A_2$ is a genuine minimum and a small perturbation of a minimum changes the value only to second order.

### (b)

**It should be $\varepsilon^2 = 10^{-14}$ exactly** (to the precision of $\sigma_2(A) = 10^{-7}$). **The third significant digit is wrong** ($1.005$, not $1.000$). $A^\mathsf{T}A$'s entries are $1 + 10^{-14}$, which in double precision is stored with an error of about $10^{-16}$, **a $1\%$ error relative to the $10^{-14}$ being resolved.** $A$ itself stores $\varepsilon = 10^{-7}$ directly and loses nothing.

### (c)

Any of: **rank-deficient least squares** (L34 §4, where Householder divides by zero); **deciding numerical rank** (L34 §5); **low-rank approximation / compression** (L35 §3); **total least squares** (L35 §5); **computing $\lVert A\rVert_2$ or $\operatorname{cond}_2$ exactly** (L34 §2).

---

## §5 — Clinic

**PS 11 Q1.** Push them to $WW^\mathsf{T}$ ($2\times2$), not $W^\mathsf{T}W$ ($3\times3$). **Then $v_k = W^\mathsf{T}u_k/\sigma_k$** — the mirror of §1(c).

**PS 11 Q2.** The first two columns of $V$ span the row space, the third the null space. **Do not confirm answers**; point at L34 §1's table.

**PS 11 Q5(c).** *"A rank-$k$ matrix has a null space of dimension $n - k$. How big is the span of $v_1, \dots, v_{k+1}$? What must two subspaces of those dimensions in $\mathbb{R}^n$ share?"* That hint is enough; do not write the argument.

**PS 11 Q4.** **Do not discuss it.** Q4(a) asks for a prediction before measurement, and the result is surprising enough that hearing it in a clinic removes the question.

> **Flag after the session:** anyone who could not do §1 unaided. **The final has an SVD
> computation on it**, and Recitation 12 next week is the last chance to fix that.

---

*MATH 241 · Week 11 · REC 11 Solutions · © CSE Department*
