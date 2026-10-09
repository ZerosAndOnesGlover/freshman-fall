# MATH 241 · Linear Algebra
## Week 12 · Lecture 3 of 3 · **Friday**
### Fourier, and the Course in One Table

*“Profound study of nature is the most fertile source of mathematical discoveries.”* — Joseph Fourier, *The Analytical Theory of Heat* (1822), ch. 1

---

**Reading:** Strang §10.5, *Fourier Series: Linear Algebra for Functions* · **Previous:** L37, PageRank · **Next:** the final, Monday Dec 15

**Coursework:** 📝 **PS 11** due today 17:00 · 📝 **PS 12** due today 17:00 · 💬 **Recitation 12** Thu of the completion period 15:00–15:50 · 📕 **Final exam** Mon of finals week 09:00–11:30

> **The last lecture of the course.**
>
> **PS 11 and PS 12 are due at 17:00 today.** **Recitation 12, the final review, is Thursday Dec 11**
> in the completion period. **The final is Monday Dec 15, 09:00–11:30.**

---

## 1. Functions Are Vectors, and They Have a Dot Product

**Week 2's L07 said continuous functions form a vector space** — add two, scale one, and you stay inside — and that *Week 12's Fourier item is a change of basis in a space of functions*. **Week 8's Reading Guide added the missing piece**: a dot product for functions,

$$\langle f, g\rangle = \int_0^{2\pi}f(t)\,g(t)\,dt,$$

**and PS 8 Q3(d) already used one**, orthogonalising $1, x, x^2$ on $[-1,1]$ to get the Legendre polynomials. **Every theorem of Week 8 holds verbatim with this inner product in place of the dot product** — projection, Pythagoras, Gram–Schmidt, orthonormal expansion — because their proofs only used the inner product's rules.

**The family that matters is $1, \cos t, \sin t, \cos 2t, \sin 2t, \dots$, and it is orthogonal:**

$$\int_0^{2\pi}\sin jt\,\sin kt\,dt = \int_0^{2\pi}\cos jt\,\cos kt\,dt = \begin{cases}\pi & j = k \ge 1\\ 0 & j \ne k\end{cases}, \qquad \int_0^{2\pi}\sin jt\,\cos kt\,dt = 0.$$

*(Each is a product-to-sum identity and one integral.)* **And the orthogonality survives sampling.** `resources/applications.py` §7 samples $1, \cos t, \sin t, \dots, \cos 3t, \sin 3t$ at $64$ equally spaced points: the largest dot product between two *different* ones is $6.78\times10^{-15}$ — rounding — and the squared lengths are $64$ for the constant and $32$ for the rest, the discrete versions of $2\pi$ and $\pi$.

---

## 2. Fourier Coefficients Are Projections

**Week 8's L26 §1(c): in an orthonormal basis, coordinates are dot products — *project onto each direction separately and add.*** With an orthogonal (not yet normalised) basis, divide by the squared length:

$$\boxed{\;f \approx \frac{a_0}{2} + \sum_{k\ge1}\bigl(a_k\cos kt + b_k\sin kt\bigr), \qquad a_k = \frac{\langle f, \cos kt\rangle}{\langle\cos kt, \cos kt\rangle} = \frac1\pi\int_0^{2\pi}f\cos kt\,dt, \quad b_k = \frac1\pi\int_0^{2\pi}f\sin kt\,dt\;}$$

**That is the whole of Fourier series, as linear algebra.** No new idea: Week 8's formula, in Week 2's space.

**The square wave** $f = +1$ on $(0,\pi)$, $-1$ on $(\pi, 2\pi)$. Integrating gives $b_k = \dfrac{4}{\pi k}$ for odd $k$ and $0$ otherwise, and all $a_k = 0$. The script computes the same projections numerically from $4096$ samples:

| $k$ | projection, $4096$ samples | exact |
|---:|---:|---:|
| $1$ | $+1.27323967$ | $4/\pi = +1.27323954$ |
| $2$ | $0.00000000$ | $0$ |
| $3$ | $+0.42441356$ | $4/3\pi = +0.42441318$ |
| $5$ | $+0.25464853$ | $4/5\pi = +0.25464791$ |
| $7$ | $+0.18189224$ | $4/7\pi = +0.18189136$ |

---

## 3. Best in the Mean, Not Everywhere

**The partial sum $S_K$ — keep the terms up to $\sin Kt$ — is the orthogonal projection of $f$ onto a finite-dimensional subspace.** So by Week 8 it is the **closest** function in that subspace, in the sense of

$$\lVert f - S_K\rVert^2 = \int_0^{2\pi}\bigl(f - S_K\bigr)^2dt,$$

**and by Pythagoras that squared error is exactly the energy in the discarded coefficients.** It goes to zero. **But look at what else happens** (`applications.py` §8):

| $K$ | largest value of $S_K$ | at $t =$ | $\lVert f - S_K\rVert^2$ |
|---:|---:|---:|---:|
| $1$ | $1.273239545$ | $1.570796$ | $1.190$ |
| $3$ | $1.200421755$ | $0.785398$ | $0.6243$ |
| $9$ | $1.182328209$ | $0.314159$ | $0.2538$ |
| $49$ | $1.179113102$ | $0.062832$ | $0.05092$ |
| $199$ | $1.178988078$ | $0.015708$ | $0.01273$ |
| $999$ | $\mathbf{1.178980078}$ | $0.003142$ | $\mathbf{0.002546}$ |

**The squared error falls like $1/K$. The peak does not fall at all.** It moves toward the jump — the maximum sits at exactly $t = \pi/(K+1)$ — and converges to

$$\frac{2}{\pi}\operatorname{Si}(\pi) = 1.178979744\ldots,$$

**$17.9\%$ above the function's value $1$**, or $8.95\%$ of the jump from $-1$ to $+1$. **This is the Gibbs phenomenon**, and adding terms never removes it.

> **Why it is not a paradox.** Projection minimises **squared error**, and squared error is all it
> controls. A spike of fixed height that gets narrower contributes less and less to the integral, so
> the squared error can go to zero while the spike stays. **Week 9's L27 §4 said "squares" is a
> choice with consequences** — there, that outliers get amplified; **here, that a least-squares
> approximation is allowed to be wrong by $18\%$ at a point.** Same choice, same caveat, in a function
> space.

---

## 4. A Finite Version You Can Compute: the Discrete Cosine Transform

**On a computer, a signal is $N$ samples, and a Fourier-type basis is an $N\times N$ orthogonal matrix.** The one JPEG uses is the **discrete cosine transform**:

$$Q_{ik} = c_k\cos\frac{\pi(2i+1)k}{2N}, \qquad c_0 = \sqrt{1/N},\ c_k = \sqrt{2/N}.$$

**For $N = 8$ the script checks $\max\lvert Q^\mathsf{T}Q - I\rvert = 1.41\times10^{-15}$ — orthonormal.** So coefficients are $c = Q^\mathsf{T}x$, reconstruction is $x = Qc$, and **energy is preserved exactly**: for the smooth signal $(10, 12.75, 15, 16.75, 18, 18.75, 19, 18.75)$, $\sum x_i^2 = 2156.25 = \sum c_k^2$.

**The coefficients are $45.61, -8.05, -3.15, -0.84, -0.71, -0.25, -0.22, -0.06$ — nearly all the energy in the first two.** Compare keeping $k$ numbers in each basis:

| keep | relative error, largest $k$ **DCT coefficients** | relative error, largest $k$ **samples** |
|---:|---:|---:|
| $1$ | $18.789\%$ | $91.246\%$ |
| $2$ | $7.231\%$ | $81.825\%$ |
| $3$ | $\mathbf{2.480\%}$ | $\mathbf{71.168\%}$ |
| $4$ | $1.692\%$ | $59.685\%$ |

**Same signal, same storage, an orthogonal change of basis first, and the error drops from $71\%$ to $2.5\%$.** Smooth signals are nearly sparse in cosines and not at all sparse in samples.

> **This is JPEG**, on $8\times8$ blocks of an image: transform, quantise the small coefficients away,
> store the rest. **Week 11's L35 §3 compressed a picture with its own SVD — the best basis for that
> one matrix. The DCT is a fixed basis that is nearly as good for almost every photograph**, and it
> costs nothing to find. **Both are Week 4's L15 §7 program: find the basis in which most coordinates
> are small, then drop them.**

---

## 5. The Four Applications, Against the Course

| | Regression (L36) | PCA (L36) | PageRank (L37) | Fourier (L38) |
|---|---|---|---|---|
| **The space** | $\mathbb{R}^m$, one coordinate per observation | $\mathbb{R}^p$, one per variable | $\mathbb{R}^n$, one per page | functions on $[0, 2\pi]$ |
| **The matrix** | design matrix $A$ | centred data $D$ | Google matrix $G$ | none needed — an inner product |
| **What is wanted** | nearest point of $\mathbf{C}(A)$ to $b$ | best $k$-dimensional subspace | $Gx = x$ | nearest trigonometric polynomial |
| **The theorem** | projection (Weeks 8–9) | Eckart–Young (Week 11), spectral theorem (Week 10) | Perron–Frobenius; powers (Weeks 6–7) | projection onto an orthogonal family (Week 8) |
| **Orthogonality** | $QR$ or SVD to compute it | $U$, $V$ orthonormal | **none** | sines and cosines |
| **Computed by** | Householder or SVD | SVD of $D$ | power iteration | the integrals, or the DCT/FFT |
| **What goes wrong** | overfitting; forming $A^\mathsf{T}A$ | forming $D^\mathsf{T}D$ | no damping: $\lambda = -1$ or repeated $\lambda = 1$ | Gibbs's $18\%$ |

---

## 6. "All Four Are the Same Theorem" — Checked

**Week 0's syllabus made the claim. Here is the verdict: three of the four are, and the fourth is not.**

**Regression, PCA and Fourier are literally one theorem** — Week 8's L25: *the nearest point of a subspace is the orthogonal projection, and the error is perpendicular to the subspace.*

- **Regression** projects $b$ onto $\mathbf{C}(A)$ in $\mathbb{R}^m$.
- **Fourier** projects $f$ onto the span of $\sin kt$, $\cos kt$ in a space of functions.
- **PCA** chooses the subspace too — Eckart–Young picks the one whose projection loses least — but the loss it measures is still Week 8's perpendicular distance, and $\sigma_{k+1}^2 + \cdots$ is Pythagoras.

**PageRank is not.** L37 §7 listed the differences: $G$ is not symmetric, its eigenvalues are complex, its eigenvectors are not orthogonal, nothing is being approximated, and **no inner product appears anywhere in the problem.** It is Week 6's eigenvector and Week 7's powers, made well-posed by a positivity hypothesis that had to be engineered in.

> **What all four do share is weaker, and more useful: Week 4's L15 §7 program.** *Given the problem,
> find the basis in which it is simple.* **Regression:** an orthonormal basis of $\mathbf{C}(A)$, where
> projecting is dot products. **PCA:** the singular vectors, where the data's shape is diagonal.
> **PageRank:** the eigenvector basis, where $G^k$ is just $\lambda^k$ and everything but $\lambda = 1$
> dies. **Fourier:** sines and cosines, where smooth signals are sparse.
>
> **So the honest version of the syllabus's sentence is: all four are the same *question*.** Three of
> them also have the same answer. **A course that has spent twelve weeks separating "true" from "true
> and usable" should end by separating "the same theorem" from "the same idea"** — and the idea is the
> one Week 4 wrote on the board: *the matrix you were handed is an accident of somebody's basis; find
> the basis that tells the truth.*

---

## 7. The Course, Backwards

**Week 0's syllabus named two habits.** Both came back every week.

**1. Every theorem is an algorithm, and the algorithm is the proof.** Elimination proved the three outcomes (Week 0). Pivots proved rank (Week 3). $AS = S\Lambda$ read column by column proved diagonalisation (Week 7). Gram–Schmidt proved $A = QR$ (Week 8). $u_k = Av_k/\sigma_k$ proved the SVD exists (Week 11).

**2. Exact and floating-point arithmetic are different subjects.** **Seven times, a correct method was not a usable one:**

| Week | Correct | Usable instead |
|---|---|---|
| 5 | Cramer's rule | elimination |
| 5 | the adjugate formula for $A^{-1}$ | elimination |
| 5 | the $n!$-term determinant | the product of pivots |
| 6 | roots of the characteristic polynomial | QR, Jacobi — iterate on the matrix |
| 9 | the normal equations | Householder QR, or the SVD |
| 10 | eigenvalues of a non-symmetric matrix, near a defect | symmetry, when you have it — then it is free |
| 11 | rank as the number of nonzero pivots | the gap in the singular values |

**And this week added the same lesson twice more** — PCA through the covariance matrix is the normal equations again (L36 §6), and the degree-19 fit (L36 §2) is a *correct projection answering the wrong question*, which is the same shape of lesson moved from numerics into statistics.

**The factorisations, in the order you met them** — the spine of the course, from Week 11's L35 §7:

$$A = LU \quad\to\quad A = S\Lambda S^{-1} \quad\to\quad A = QR \quad\to\quad A = Q\Lambda Q^\mathsf{T} \quad\to\quad A = U\Sigma V^\mathsf{T}$$

**Hypotheses fall away from left to right, and the outer factors become orthogonal.** Those are the same fact: orthogonal factors have condition number $1$, and every factorisation that is safe in floating point uses them.

---

## 8. For Monday Week

**The final is comprehensive**: Weeks 0–12, $150$ minutes, two handwritten pages. `resources/FINAL EXAM Revision Guide.md` gives its structure and where the marks are.

**The fastest useful revision is the eleven quiz answer keys**, which between them cover Weeks 0–10 with reasoning written out. **Then the two midterm papers. Then PS 10 and PS 11**, because Weeks 10 and 11 have not yet been examined and the final has to examine them.

**Recitation 12, Thursday Dec 11, is the review.** Bring the topic you would least like to see on the paper.

---

## 9. What to Take Away

1. **Functions are vectors with an inner product $\int fg$**, and Week 8's theorems hold for them without change.
2. **Sines and cosines are orthogonal**, so **Fourier coefficients are projections** — Week 8's L26 §1(c) in a function space.
3. **Partial sums are best in the squared-error sense**, and that error $\to 0$; **the Gibbs overshoot of $17.9\%$ never goes away**, because squared error does not see a narrowing spike.
4. **The DCT is an orthonormal basis of $\mathbb{R}^N$** in which smooth signals are sparse — $2.5\%$ error from $3$ of $8$ numbers, against $71\%$ in the sample basis. **That is JPEG.**
5. **Regression, PCA and Fourier are one theorem — orthogonal projection. PageRank is not.** All four are one *question*: find the basis in which the problem is simple.
6. **Two habits, seven lessons, five factorisations**, and one direction of travel: fewer hypotheses, more orthogonality.

---

## Exercises

*(Not assessed.)*

1. Verify $\int_0^{2\pi}\sin 2t\sin 3t\,dt = 0$ with a product-to-sum identity.
2. Find the Fourier series of $f(t) = t$ on $(-\pi, \pi)$. **Use Pythagoras to show $\sum 1/k^2 = \pi^2/6$.** *(PS 12 Q3.)*
3. **What fraction of the square wave's energy does $\sin t$ alone capture?** *(Its squared length is $2\pi$ over one period.)*
4. The DCT of a **constant** signal: which coefficients are nonzero? Of an alternating signal $(1, -1, 1, -1, \dots)$?
5. **Why does JPEG use blocks of $8\times8$ rather than transforming the whole image at once?** Give one reason from this course and one from outside it.
6. **Argue with §6.** Is there a sense in which PageRank *is* a projection? *(Think about what power iteration does to the component of the error along each eigenvector.)* Does your argument need orthogonality?

---

*MATH 241 · Week 12 · L38 · © CSE Department*
