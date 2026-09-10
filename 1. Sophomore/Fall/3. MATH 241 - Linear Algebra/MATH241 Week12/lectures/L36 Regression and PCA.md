# MATH 241 · Linear Algebra
## Week 12 · Lecture 1 of 3 · **Monday**
### Regression and PCA: Two Ways to Fit

---

**Reading:** Strang §7.3 (PCA) and §4.3 revisited · **Previous:** Week 11's L35, low-rank approximation · **Next:** L37, PageRank

> **The last teaching week. There is no quiz** — Quiz 11 was the last.
>
> **PS 11 and PS 12 are both due Friday at 17:00.** PS 12 is released Wednesday and is short.
> **Recitation 11 is Thursday.** **Recitation 12, the final review, is the Thursday of the
> completion period**, Dec 11.
>
> **The final is Monday Dec 15, 09:00–11:30**, comprehensive, 25% — seating in VNC 100 with overflow
> to TH 200, assignments posted on the portal a week before.

---

## 1. Four Applications, and a Claim to Check

**Week 0's syllabus listed this week as *PCA, PageRank, regression, Fourier* and said: *all four are the same theorem.*** That is a strong claim, and a course that has spent twelve weeks refusing to take claims on trust should not take its own.

**So this week does all four with the tools already built, measures each one, and L38 §6 checks the claim.** It is mostly true. The exception is instructive.

| Lecture | Applications | Tools |
|---|---|---|
| **L36** | regression, PCA | Weeks 8, 9, 11 |
| L37 | PageRank | Weeks 6, 7 |
| L38 | Fourier, and the verdict | Weeks 2, 8 |

Every number is in `resources/applications.py`.

---

## 2. Regression Is Week 9, and Choosing a Model Is Choosing a Subspace

**Week 9's L29 §2 said it: $\mathbf{C}(A)$ is the set of everything the model can produce, and the fit is the projection of the data onto it.** Fitting a polynomial of degree $d$ means projecting onto the $(d+1)$-dimensional space spanned by $1, t, \dots, t^d$ sampled at the data.

**And L29 §4 warned that more columns always fit better.** The subspace grows, so the projection gets closer — guaranteed, whatever the data. **That warning was a theorem about the training data. Here is what it means for new data** (`applications.py` §1): $20$ training points and $400$ test points from $y = \sin 2.5t$ plus noise of standard deviation $0.15$.

| degree | training RMS | test RMS |
|---:|---:|---:|
| $0$ | $0.7978$ | $0.7819$ |
| $1$ | $0.3259$ | $0.3896$ |
| $3$ | $0.0983$ | $0.1947$ |
| $6$ | $0.0917$ | $\mathbf{0.1839}$ |
| $8$ | $0.0728$ | $1.5773$ |
| $10$ | $0.0615$ | $11.6627$ |
| $15$ | $0.0408$ | $1112.69$ |
| $19$ | $\mathbf{0.0000}$ | $\mathbf{16{,}412{,}119}$ |

**Training error falls at every single step** — L29 §4, measured. **Test error falls, flattens near $0.18$ — close to the noise level $0.15$, which no model can beat — and then explodes.** At degree $19$ there are $20$ coefficients for $20$ points: the curve passes through every training point exactly and is off by sixteen million on new ones.

> **This is *overfitting*, and it is not a numerical accident.** The degree-19 fit is the correct
> projection. **It answers the question asked — minimise the training residual — perfectly, and that
> was the wrong question.** CS 331 spends weeks on how to ask a better one; the linear algebra of it
> is this table.

---

## 3. A Better Basis Fixes the Numerics, Not the Model

**Week 9's L29 §4 also said the monomial basis $1, t, t^2, \dots$ is badly conditioned** — Week 0's Hilbert matrix in disguise — and that the fix is an orthogonal family such as the Legendre polynomials. **Both halves are true, and they are about different things:**

| degree | $\operatorname{cond}$, monomials | $\operatorname{cond}$, Legendre | test RMS, monomials | test RMS, Legendre |
|---:|---:|---:|---:|---:|
| $6$ | $1.55\times10^{2}$ | $1.48\times10^{1}$ | $0.183889$ | $0.183889$ |
| $10$ | $1.90\times10^{4}$ | $8.86\times10^{2}$ | $11.662670$ | $11.662670$ |
| $15$ | $1.14\times10^{7}$ | $2.17\times10^{5}$ | $1112.692706$ | $1112.692706$ |
| $19$ | $1.08\times10^{12}$ | $1.03\times10^{10}$ | $16{,}412{,}119.39$ | $16{,}412{,}177.90$ |

**The Legendre basis improves the conditioning by a factor of $10$ to $100$. It changes the test error not at all** — the two agree to eleven digits at degree $15$, and only at degree $19$, where even the Legendre matrix has $\operatorname{cond} = 10^{10}$, does rounding show.

> **Why:** both bases span the same subspace, so they produce the same projection and the same
> curve. **A basis is a way of writing a subspace down; it cannot change which subspace you chose.**
> Conditioning is about computing the answer accurately. Overfitting is about the answer being the
> wrong one. **Keep the two separate** — it is the most common confusion about regression, and this
> table is the cleanest way to see it.

*(Legendre polynomials are orthogonal under $\int_{-1}^{1}$, not on $20$ random points, which is why their conditioning is improved rather than perfect. Week 8's Gram–Schmidt on the actual sample points would give $\operatorname{cond} = 1$.)*

---

## 4. PCA Is the SVD of the Centred Data

**Week 11's L35 §5 fitted a line to points in the plane by minimising perpendicular distance**, using the SVD of the centred data, and said: *Week 12's PCA is exactly this in more dimensions.*

**Principal component analysis.** Given $N$ points in $\mathbb{R}^p$:

1. **Centre them** — subtract the mean, so the rows of $D$ ($N\times p$) average to zero.
2. **Take the SVD** $D = U\Sigma V^\mathsf{T}$.
3. **The columns of $V$ are the principal directions**, in order of importance. **$\sigma_k^2/(N-1)$ is the variance along the $k$-th.**
4. **Keep the first $k$** — Eckart–Young says that is the best $k$-dimensional subspace through the centroid, in the sense of total squared perpendicular distance.

`applications.py` §2: $300$ points scattered near a plane in $\mathbb{R}^3$, with noise $0.4$ in every direction.

| | $\sigma_1$ | $\sigma_2$ | $\sigma_3$ |
|---|---:|---:|---:|
| singular value | $51.61$ | $26.3825$ | $7.1266$ |
| variance explained | $78.10\%$ | $20.41\%$ | $1.49\%$ |
| cumulative | $78.10\%$ | $98.51\%$ | $100\%$ |

**Two directions carry $98.5\%$ of the variation.** The data is, to that accuracy, two-dimensional — and PCA found the plane without being told there was one:

- **the plane's normal is $v_3$**: $(0.80365, -0.34256, -0.48662)$, against the true generating normal $(-0.8, 0.36, 0.48)$ — **$1.09°$ apart**, the sign being irrelevant;
- **the sum of squared distances from the points to the PCA plane is $50.788448$, and $\sigma_3^2 = 50.788448$.** Eckart–Young at rank $2$.

> **The statistical reading, for MATH 251 next term.** $C = D^\mathsf{T}D/(N-1)$ is the **covariance
> matrix** — symmetric positive semidefinite by Week 10's L31 §7 — and $D^\mathsf{T}D = V\Sigma^\mathsf{T}\Sigma V^\mathsf{T}$
> is its spectral decomposition. **So the principal directions are the eigenvectors of the covariance
> matrix** (Week 6's L19 table promised exactly this) and the variances are its eigenvalues. The
> script checks: eigenvalues of $C$ are $8.908319$, $2.327876$, $0.169861$, and
> $\sigma_k^2/299$ gives the same three.

---

## 5. The Regression Plane Is Not the PCA Plane

**Fit the same $300$ points with a plane by regression instead** — $z = c_0 + c_1x + c_2y$, Week 9, minimising vertical distance (§4 of the script):

$$z = 0.03027 + 1.42833\,x - 0.51474\,y.$$

**Its normal is $(-0.78566, 0.28314, 0.55006)$, and the angle between the two planes is $5.0872°$.** Same data, two different best planes:

| | squared **vertical** distances | squared **perpendicular** distances |
|---|---:|---:|
| regression plane | $\mathbf{188.9948}$ | $57.1831$ |
| PCA plane | — | $\mathbf{50.7884}$ |

**Each wins the contest it was built for.** Regression minimises error in $z$ — it singles out one coordinate as the thing to predict and treats the others as exact. PCA minimises error in every direction at once — it treats all coordinates alike.

> **Neither is "the" plane.** They answer different questions. **Use regression when one variable is
> a response and the others are measured without error; use PCA when you want the shape of the data
> and no variable is special.** Week 11's L35 §5 showed the same split in two dimensions, and PS 11
> Q4(c) showed what goes wrong when the choice does not match where the noise really is.

---

## 6. PCA Through the Covariance Matrix Is Week 9's Mistake Again

**Textbooks often compute PCA by forming $C = D^\mathsf{T}D/(N-1)$ and finding its eigenvalues.** Mathematically identical. **Numerically, it is the normal equations** — it forms $D^\mathsf{T}D$, and Week 9's L28 §1 said what that does.

`applications.py` §3 moves the same $300$ points onto the plane to within $10^{-9}$, so the third variance is real and tiny:

| Method | smallest variance |
|---|---:|
| **SVD of $D$** | $\sigma_3^2/(N-1) = 1.0600\times10^{-18}$ |
| **eigenvalues of $D^\mathsf{T}D/(N-1)$** | $\lambda_3 = \mathbf{-9.7476\times10^{-17}}$ |

**The covariance route returns a negative variance**, which is impossible. The true value is about $10^{-18}$ and the largest is about $8.9$, a ratio of $8\times10^{18}$ — **far beyond $1/\varepsilon_\text{mach} = 4.5\times10^{15}$**, so $D^\mathsf{T}D$ cannot represent it. **The SVD of $D$ only needs to resolve $\sigma_3/\sigma_1 \approx 3\times10^{-10}$, which is easy.**

> **It is the same lesson for the third time.** Week 9: don't form $A^\mathsf{T}A$ to solve least
> squares. Week 11: don't form $A^\mathsf{T}A$ to compute an SVD. **Week 12: don't form the
> covariance matrix to do PCA.** `sklearn.decomposition.PCA` takes the SVD of the centred data, and
> this is why.

---

## 7. What PCA Needs From You

**PCA is a projection, and a projection knows nothing about what your coordinates mean.** Three things it cannot do for you:

1. **Units.** Measure one coordinate in metres and another in millimetres, and the second dominates the variance by a factor of $10^6$. **Standardise first** (divide each column by its standard deviation) unless the units are genuinely comparable — and say which you did.
2. **Centring.** Skip it, and the first "principal direction" points at the mean. **Week 11's L35 exercise 6 asked why.**
3. **Nonlinearity.** Points on a circle have no good one-dimensional linear summary, although they are one-dimensional. **PCA finds flat subspaces only.**

---

## 8. What to Take Away

1. **Regression projects onto a model subspace.** Training error falls with every column; **test error does not** — $0.18$ at degree $6$, sixteen million at degree $19$.
2. **A better basis improves conditioning and leaves the fit unchanged.** Numerics and overfitting are different problems.
3. **PCA is the SVD of the centred data**: principal directions are $V$, variances are $\sigma_k^2/(N-1)$, and keeping $k$ is Eckart–Young.
4. **PCA's directions are the covariance matrix's eigenvectors** — Week 10's spectral theorem on a covariance matrix.
5. **Regression and PCA give different planes** — $5.09°$ apart here — because they measure distance differently.
6. **Compute PCA from the data, not the covariance matrix**, or lose the small variances to rounding.
7. **Standardise, centre, and remember it is linear.**

---

## Exercises

*(Not assessed. PS 12 is the assessed work.)*

1. **Why does the test error in §2 level off near $0.18$ rather than falling to $0$?** What would it level off at if the noise were $0.3$?
2. Fit a degree-$3$ polynomial to $4$ points. What is the training residual? **What does that tell you about using training residual to choose a degree?**
3. Four centred points $(6,8)$, $(-6,-8)$, $(-4,3)$, $(4,-3)$. **Find the first principal direction without a computer.** *(PS 12 Q1 does this in full.)*
4. Show that the first principal direction maximises the variance of the projected data, using Week 10's Rayleigh quotient.
5. **When do the regression line and the PCA line coincide?** Give a dataset where they do.
6. A dataset has variances $9$, $4$, $0.01$ along its principal directions. **How much variance does a two-dimensional summary keep?** What is the total squared distance lost, for $N = 101$ points?
7. **Why does centring matter for PCA but not for the singular values of a regression matrix with an intercept column?** *(Think about what the column of ones does.)*

---

*MATH 241 · Week 12 · L36 · © CSE Department*
