# MATH 241 · Reading Guide · Week 12
## Strang's applications, and the reading that closes the course

---

**Nothing this week is new mathematics.** Every application is Weeks 6–11 pointed at a real problem, and the reading is chosen to show you that from outside these notes — **in the words of the people who built the applications.**

**Read lightly and read in order.** PS 11, PS 12 and the final all come before anything here would pay off in marks. **The two papers marked *read* are short and are the best reading of the term.**

| Source | Read? | Why |
|---|---|---|
| **Strang §7.3, Principal Component Analysis** | **Read** | L36 §4. The SVD view, as L36 takes it |
| Strang §4.3 revisited | Skim | L36 §2 — regression was always this |
| **Strang §10.3, Markov Matrices** *(§6.4 in some printings)* | **Re-read** | L37. You read it in Week 7; it means more now |
| **Strang §10.5, Fourier Series: Linear Algebra for Functions** | **Read** | L38 §1–§3. The title is the lecture |
| **Bryan & Leise (2006), *SIAM Review* 48(3)** | **Read — twelve pages** | PageRank from first principles, with the damping argument. Title: `The $25,000,000,000 Eigenvector` |
| **Shlens, *A Tutorial on Principal Component Analysis* (2014)** | **Read** | Free on arXiv. PCA motivated physically, then shown to be the SVD |
| Goodfellow §2.12 | Skim | PCA derived as an optimisation, in CS 331's notation |
| Brin & Page (1998) §2.1 | Skim | The original PageRank definition, with $d = 0.85$ |
| Wallace, *The JPEG Still Picture Compression Standard* (1992) | Optional | L38 §4 at industrial scale |

---

## Strang §7.3 — the questions to hold

1. **Does he centre the data before the SVD?** Find the line. **What goes wrong if you don't** — and does he say?
2. **He computes PCA from the SVD of the data or from the covariance matrix?** Compare with L36 §6's measured negative variance, and **decide whether his choice matters for his examples.** *(It usually doesn't, on examples. It does on data.)*
3. **"Variance explained."** Find his definition. **Is it $\sigma_k^2$ over the sum, or $\sigma_k$ over the sum?** One of those is wrong, and textbooks and software disagree about which they print.
4. He mentions **standardising** columns. **When would you not?** *(L36 §7.)*
5. **Where does Eckart–Young appear**, by name or not? PCA's optimality is that theorem and nothing else.

---

## Markov matrices and Fourier — the questions to hold

6. **Strang proves $\lambda = 1$ is an eigenvalue of a Markov matrix.** Compare with Week 7's L23 §5 proof. **Which is shorter, and which generalises?**
7. **Does he mention damping?** If not, construct the two counterexamples of L37 §5 from his definitions — a cycle and a disconnected web — **and check that his convergence theorem has a hypothesis that excludes them.**
8. **Positive versus non-negative.** Perron–Frobenius has two versions. **Find which one Strang states**, and say which one Google's $G$ satisfies and why that is the reason for damping.
9. In §10.5, **find the sentence that makes a function a vector.** Then find the inner product. **Is it $\int_0^{2\pi}$ or $\int_{-\pi}^{\pi}$?** *(Either works — why?)*
10. **Does he discuss the Gibbs phenomenon?** L38 §3 measured it at $17.9\%$. **Find a claim in his section that is true in the squared-error sense and false pointwise** — or confirm he is careful about which he means.

---

## Where Bryan & Leise Earns Its Place

**Twelve pages, written for exactly your background**, with the title quoted above. **It derives PageRank from the random surfer, hits both of L37 §5's failures, and fixes them with damping** — in the same order this course did, which is reassuring.

> **Its §4 proves the damped matrix has a unique positive steady state**, using a version of
> Perron–Frobenius proved from scratch in a page. **That page is the one piece of PageRank this course
> stated without proof** (L37 §5), and reading it closes the gap.

---

## Where Shlens Earns Its Place

**It starts with a spring, a ball and three cameras**, and asks how to discover that the motion is one-dimensional from six noisy coordinates. **It then derives PCA as a change of basis that diagonalises the covariance matrix** — Week 10's spectral theorem — and only afterwards shows it is the SVD.

> **Its §6, "Discussion", lists PCA's assumptions**: linearity, that large variance means structure,
> and that the principal components are orthogonal. **Compare with L36 §7.** The third assumption is
> the one this course would phrase differently — **orthogonality is not an assumption about the data,
> it is a property of the SVD** — and deciding whether Shlens means the same thing is a good test of
> Weeks 10 and 11.

---

## What Belongs on the Final's Sheet

**The final is Monday Dec 15, 09:00–11:30, two handwritten pages.** Four lines from this week — **it is an applications week, and the sheet space belongs to Weeks 10 and 11**:

1. **PCA**: centre; SVD; directions $V$; variances $\sigma_k^2/(N-1)$; loss $\sum_{j>k}\sigma_j^2$.
2. **PageRank**: $G = \alpha P + \tfrac{1-\alpha}{n}\mathbf{1}\mathbf{1}^\mathsf{T}$, columns of $P$ sum to $1$; rate $\lvert\lambda_2\rvert \le \alpha$.
3. **Fourier**: $a_k = \tfrac1\pi\int f\cos kt$, $b_k = \tfrac1\pi\int f\sin kt$; squared error $\to 0$, overshoot does not.
4. **Three of the four are orthogonal projection; PageRank is Perron–Frobenius.**

**The rest of the sheet** — the FINAL EXAM Revision Guide in this folder says where the marks are, and the Reading Guides for Weeks 10 and 11 each list what belongs from those weeks.

---

## The Habit for This Week

**Ask what a method is optimal *for*.**

**Every application this week was the best possible answer to a precisely stated question** — and every one produced something you might not want:

| Method | Optimal for | And therefore |
|---|---|---|
| degree-19 regression | training squared error | sixteen million on new data |
| PCA | total perpendicular squared distance | ignores which variable you wanted to predict |
| undamped PageRank | being the eigenvector | may not exist uniquely, or be reachable |
| Fourier partial sum | squared error over the interval | $18\%$ wrong at the jump, forever |

> **A method is a theorem plus a question.** The theorem is never the weak point. **Choosing the
> question is**, and that part does not appear in any of the matrices.

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| **MATH 251 (next term)** | Covariance, PCA as statistics, why least squares is maximum likelihood |
| **ECE 211 (next term)** | Fourier as a whole course — L38 §1–§2 for a term |
| **CS 331 (Machine Learning)** | Overfitting properly: validation, regularisation, the bias–variance trade-off |
| **Hastie, Tibshirani & Friedman, *Elements of Statistical Learning*, Ch. 3 and 7** | Regression and model assessment, with L36 §2's table as its opening example |
| **Strang, MIT 18.065** | Linear algebra for data: this week, done as a term |
| **Trefethen & Bau** | For the numerics behind every "computed by" line in L38 §5 |

---

*MATH 241 · Week 12 · Reading Guide · © CSE Department*
