# MATH 241 · Linear Algebra
## Week 7 · Lecture 2 of 3 · **Tuesday**
### When Diagonalization Fails

*“The way I have taken seems not to lead to the goal, but much rather to make the truth of geometry doubtful.”* — Carl Friedrich Gauss, letter to Farkas Bolyai (1799)

---

**Reading:** Strang §6.2 (the "not diagonalizable" discussion), §8.3 · **Previous:** L21, diagonalisation · **Next:** L23, complex eigenvalues

**Coursework:** 📝 **PS 7** released Wed this week, due Fri of Week 8 17:00 · 💬 **Recitation 6** Thu this week 15:00–15:50 · 📝 **PS 6** due Fri this week 17:00 · 📊 **Quiz 8** Mon of Week 8

---

## 1. The Hypothesis Was Not Decoration

L21 needed **$n$ independent eigenvectors** to make $S$ invertible. **Some matrices do not have them**, and this lecture is what to do about it.

$$S = \begin{bmatrix}3&1\\ 0&3\end{bmatrix}: \qquad p(\lambda) = (3-\lambda)^2, \qquad \mathbf{N}(S - 3I) = \operatorname{span}\{(1,0)\}$$

**One eigenvector for a $2\times2$.** There is no invertible $S$ with $S^{-1}AS$ diagonal, and no amount of cleverness produces one — **it is a fact about the matrix, not about your method.**

**Week 6's vocabulary, restated as the criterion:**

$$\boxed{\;A \text{ diagonalisable} \iff \text{geometric} = \text{algebraic for every eigenvalue} \iff \sum_\lambda \dim\mathbf{N}(A - \lambda I) = n\;}$$

**A matrix failing this is *defective*.**

---

## 2. Why Geometric Cannot Exceed Algebraic

Week 6's L20 §5 asserted $1 \le \text{geometric} \le \text{algebraic}$ and deferred the upper bound. **Here it is**, and the argument is L21's construction run partway.

> **Claim.** If $\dim\mathbf{N}(A - \lambda I) = g$, then $\lambda$ is a root of $p$ of multiplicity
> at least $g$.
>
> *Sketch.* Take a basis $s_1,\dots,s_g$ of the eigenspace and extend it to a basis of
> $\mathbb{R}^n$ (Week 3 — every independent list extends). With $M$ the matrix of that basis,
> $$M^{-1}AM = \begin{bmatrix}\lambda I_g & B\\ 0 & C\end{bmatrix}$$
> because $A$ sends each of the first $g$ basis vectors to $\lambda$ times itself. Taking
> determinants of the block form (Week 5),
> $$p(\mu) = \det(A - \mu I) = (\lambda - \mu)^g \det(C - \mu I),$$
> so $(\lambda - \mu)^g$ divides $p$ and the algebraic multiplicity is at least $g$. $\square$

**The lower bound is easier:** $\lambda$ a root of $p$ makes $A - \lambda I$ singular, so its null space is at least a line, so $g \ge 1$.

> **Note what the proof used:** Week 3's basis extension, Week 4's change of basis, Week 5's
> determinant of a block matrix. **Everything in Week 7 is assembled from earlier weeks**, which is
> why it is the densest week in the course and why nothing new is being introduced.

---

## 3. Where the Missing Eigenvectors Went

**The instructive question is not "why did it fail" but "what is there instead".**

For $S = \begin{bmatrix}3&1\\0&3\end{bmatrix}$, look at what $S$ does to the basis $e_1, e_2$:

$$Se_1 = 3e_1 \qquad\qquad Se_2 = e_1 + 3e_2$$

**$e_1$ is an eigenvector. $e_2$ is not — it is sent to $3e_2$ *plus a bit of $e_1$*.** That extra term is exactly what the diagonal form cannot express: a diagonal matrix scales each basis vector independently, with **no coupling**, and here there is coupling that no change of basis removes.

**The best available form keeps the coupling and makes it minimal:**

$$\begin{bmatrix}\lambda & 1\\ 0 & \lambda\end{bmatrix}$$

**a *Jordan block*.** And the general theorem, stated and not proved:

> **Jordan form.** Every square complex matrix is similar to a block-diagonal matrix whose blocks
> are Jordan blocks — $\lambda$ on the diagonal, $1$ just above it, zeros elsewhere. It is unique up
> to the order of the blocks.

**A matrix is diagonalisable exactly when every Jordan block is $1\times1$.** So the Jordan form is the canonical form that L21 §6 could only give for the diagonalisable case, and it completes the classification of similarity.

> **Why this course states it and stops.** The Jordan form is a beautiful theorem and a **numerically
> useless** one, for the reason in §4: the block structure is not stable under perturbation, so it
> cannot be computed reliably in floating point. **No production library computes it.** You should
> know it exists, know what it says, and know why nobody uses it — which is a more useful thing to
> carry than the construction.

---

## 4. Defectiveness Is Not a Matter of Degree

**This is the section that changes how you think about the whole topic.**

$$\begin{bmatrix}3&\varepsilon\\ 0&3\end{bmatrix}$$

| $\varepsilon$ | geometric multiplicity of $\lambda = 3$ | |
|---|---:|---|
| $1000$ | $1$ | defective |
| $7$ | $1$ | defective |
| $1$ | $1$ | defective |
| $10^{-300}$ | $1$ | defective |
| **$0$** | $\mathbf{2}$ | **diagonalisable** |

**Defective for every nonzero $\varepsilon$, however small, and diagonalisable at exactly zero.** There is **no continuous transition** — the property jumps.

**Three consequences, and they are the practical content of the lecture:**

**(a) "Nearly diagonalisable" is not a meaningful phrase.** The matrix at $\varepsilon = 10^{-300}$ is as defective as the one at $\varepsilon = 1000$.

**(b) No numerical algorithm tests for defectiveness.** In floating point you cannot distinguish $\varepsilon = 0$ from $\varepsilon = 10^{-300}$, so the question *is this matrix diagonalisable* is **not answerable by a computation**. Real software does not ask it.

**(c) So the eigenvector computation is ill-conditioned near a defective matrix**, even though the eigen*values* are fine. **This is why Week 0's condition-number theme returns**: $\varepsilon = 10^{-8}$ gives two eigenvectors that are almost parallel, so $S$ is nearly singular, so $S^{-1}$ is enormous and $A = S\Lambda S^{-1}$ is a numerically worthless factorisation even though it exists.

> **The professional answer is to avoid the question**, and the next four weeks are how:
>
> - **Week 8:** orthonormal bases, where $S^{-1} = S^\mathsf{T}$ and $\operatorname{cond}(S) = 1$.
> - **Week 10:** symmetric matrices are **never** defective, and their eigenvectors are orthogonal.
> - **Week 11:** the SVD exists for **every** matrix, with orthonormal bases at both ends.
>
> **Each removes a hypothesis rather than working harder to satisfy it**, which is the pattern
> Week 4's L15 §7 table was predicting.

---

## 5. The Cases That Do Not Fail

**Defectiveness is rare and there are large classes where it cannot happen.** Worth knowing, so that you stop checking:

| $A$ | Diagonalisable? | Why |
|---|---|---|
| $n$ distinct eigenvalues | **always** | L20 §6 |
| **symmetric** ($A^\mathsf{T} = A$) | **always**, with orthogonal eigenvectors | **Week 10** |
| orthogonal ($Q^\mathsf{T}Q = I$) | always, over $\mathbb{C}$ | Week 8 |
| a projection ($P^2 = P$) | always | exercise 6 of L21 |
| triangular with distinct diagonal | always | the diagonal is the spectrum |
| triangular with a repeated diagonal | **often not** | $\begin{bmatrix}3&1\\0&3\end{bmatrix}$ |
| **nilpotent** ($N^k = 0$, $N \ne 0$) | **never** | all eigenvalues $0$, so $\Lambda = 0$, so $A = 0$ |

**The nilpotent row is worth a sentence.** Week 6's L20 §4 showed every eigenvalue of a nilpotent matrix is zero. If such an $A$ were diagonalisable then $\Lambda = 0$ and $A = S0S^{-1} = 0$. **So a nonzero nilpotent matrix is always defective** — and Week 4's differentiation operator $D$ on $\mathbb{P}_3$, with $D^4 = 0$, is an example. **Differentiation is not diagonalisable.**

*(Which is a real fact about calculus, not an artefact: there is no basis of polynomials in which differentiation acts by independent scaling. The eigenvectors of $D$ are only the constants.)*

---

## 6. The Full Picture of Canonical Forms

**Where Week 7 leaves the classification of matrices up to similarity:**

| Class | Canonical form | Exists |
|---|---|---|
| Diagonalisable | $\Lambda$, diagonal | when geometric $=$ algebraic throughout |
| **Every** complex matrix | **Jordan form** | always — §3 |
| Symmetric real | $\Lambda$ with **orthogonal** $S$ | always — Week 10 |
| **Every** matrix, any shape | **$U\Sigma V^\mathsf{T}$** | always — Week 11 |

**Read the "exists" column downwards.** Diagonalisation is the natural thing and it can fail. The Jordan form never fails and is unusable. **Weeks 10 and 11 get unconditional existence *and* numerical reliability, by restricting the matrices or by allowing two different bases.**

> **The last row is the one to look forward to.** The SVD is not a similarity — it uses a different
> basis at the input and the output, which similarity forbids — and **that extra freedom is exactly
> what buys unconditional existence.** Week 4's L14 §1 permitted two bases from the start, and
> nothing until Week 11 needed it.

---

## 7. What to Take Away

1. **Diagonalisable $\iff$ geometric $=$ algebraic for every eigenvalue** $\iff$ the eigenspace dimensions sum to $n$.
2. **Geometric $\le$ algebraic**, proved by block-triangularising in a basis extending the eigenspace — Weeks 3, 4 and 5 combined.
3. **What is there instead of a missing eigenvector is coupling**: $Se_2 = e_1 + 3e_2$. The Jordan block $\begin{bmatrix}\lambda&1\\0&\lambda\end{bmatrix}$ is the minimal form of it.
4. **The Jordan form always exists and nobody computes it**, because the block structure is not stable under perturbation.
5. **Defectiveness is not a matter of degree** — defective at $\varepsilon = 10^{-300}$, diagonalisable at $0$, with no transition. **So no algorithm tests for it.**
6. **Near a defective matrix, $S$ is nearly singular and $A = S\Lambda S^{-1}$ is numerically worthless** even though it exists.
7. **Distinct eigenvalues, symmetric, orthogonal and projections never fail. Nonzero nilpotent matrices always do** — including differentiation.
8. **Weeks 10 and 11 remove the hypothesis rather than satisfying it**, which is the pattern.

---

## Exercises

*(Not assessed.)*

1. For $\begin{bmatrix}5&1\\0&5\end{bmatrix}$: give both multiplicities of $\lambda = 5$ and show it is defective. **What is its Jordan form?**
2. Give a $3\times3$ matrix with eigenvalues $2,2,2$ that is (a) diagonalisable, (b) defective with a two-dimensional eigenspace, (c) defective with a one-dimensional eigenspace.
3. Show that a nonzero nilpotent matrix is never diagonalisable, in two lines. Then verify directly that $\begin{bmatrix}0&1\\0&0\end{bmatrix}$ has only one eigenvector.
4. $A$ is $4\times4$ with $p(\lambda) = (\lambda-1)^2(\lambda-2)^2$. **List every possible pair of geometric multiplicities**, and say which pairs make $A$ diagonalisable.
5. Compute the eigenvectors of $\begin{bmatrix}3&1\\0&3.0001\end{bmatrix}$ and find the angle between them. **Then estimate $\operatorname{cond}(S)$**, and say what that does to $A = S\Lambda S^{-1}$ as a numerical object. *(This is §4(c) with numbers.)*
6. Week 4's $D$ on $\mathbb{P}_3$ has $D^4 = 0$. Find all its eigenvectors and confirm it is defective. **What is the largest Jordan block?**
7. **True or false:** if $A$ and $B$ have the same characteristic polynomial and both are diagonalisable, they are similar. What if only one is?

---

*MATH 241 · Week 7 · L22 · © CSE Department*
