# MATH 241 · Linear Algebra
## Week 9 · Lecture 2 of 3 · **Tuesday**
### Least Squares in Practice

---

**Reading:** Strang §4.3 (the QR remarks), §11.2 · **Previous:** L27, least squares · **Next:** L29, what least squares assumes

> **Every number in this lecture is reproduced by `resources/leastsquares.py`.**

---

## 1. The Normal Equations Are Correct and Should Not Be Used

$$A^\mathsf{T}A\hat x = A^\mathsf{T}b$$

**is exact mathematics**, derived twice now, and it is **not** how least squares is computed. **The reason is one identity:**

$$\boxed{\;\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2\;}$$

*(This will be obvious in Week 11: the singular values of $A^\mathsf{T}A$ are the squares of those of $A$, and the condition number is the ratio of largest to smallest. For now, take it and watch what it does.)*

**Squaring a condition number is catastrophic**, because Week 0's L03 §7 said you lose about $\log_{10}\operatorname{cond}$ of your sixteen digits:

| $\operatorname{cond}(A)$ | digits lost solving with $A$ | $\operatorname{cond}(A^\mathsf{T}A)$ | digits lost |
|---:|---:|---:|---:|
| $10^{3}$ | 3 | $10^{6}$ | 6 |
| $10^{6}$ | 6 | $10^{12}$ | 12 |
| $10^{8}$ | 8 | $10^{16}$ | **all of them** |

**A problem you could solve to eight digits becomes one you cannot solve at all** — not because the data is bad, but **because of the algorithm.**

---

## 2. The Standard Counterexample

**Läuchli's matrix**, and it is as small as a counterexample can be:

$$A = \begin{bmatrix}1&1\\ \varepsilon&0\\ 0&\varepsilon\end{bmatrix}$$

**The two columns are obviously independent for every $\varepsilon \ne 0$.** Nothing is wrong with this matrix. But

$$A^\mathsf{T}A = \begin{bmatrix}1+\varepsilon^2 & 1\\ 1 & 1+\varepsilon^2\end{bmatrix}, \qquad \det = 2\varepsilon^2 + \varepsilon^4$$

**and $1 + \varepsilon^2$ rounds to exactly $1$ once $\varepsilon^2 < \varepsilon_{\text{mach}}$**, i.e. once $\varepsilon < 1.49\times10^{-8}$:

| $\varepsilon$ | $1 + \varepsilon^2$ as a `double` | computed $\det$ | $A^\mathsf{T}A$ is |
|---|---|---:|---|
| $10^{-3}$ | $1.0000000099999999$ | $2\times10^{-6}$ | fine |
| $10^{-5}$ | $1.00000000010000$ | $2\times10^{-10}$ | fine |
| $10^{-7}$ | $1.00000000000001$ | $2\times10^{-14}$ | fine |
| $\mathbf{10^{-8}}$ | $\mathbf{1}$ | $\mathbf{0}$ | **SINGULAR** |

**At $\varepsilon = 10^{-8}$, $A^\mathsf{T}A$ is exactly singular in floating point** while $A$ has two independent columns you can see with your eyes. **Forming $A^\mathsf{T}A$ destroyed the problem.**

> **Notice what did *not* go wrong.** The data is exact. The matrix is well within range. There is no
> subtraction of nearly equal quantities anywhere in $A$. **The information was lost in the act of
> computing $A^\mathsf{T}A$**, because $\varepsilon^2$ fell off the bottom of a `double` when added
> to $1$. **This is Week 0's L03 §4 again**, in a new costume.

---

## 3. The Repair: Never Form It

**Week 8's PS 8 Q4(d) derived the alternative**, and it is three lines. Substitute $A = QR$:

$$A^\mathsf{T}A\hat x = A^\mathsf{T}b$$
$$(QR)^\mathsf{T}(QR)\hat x = (QR)^\mathsf{T}b$$
$$R^\mathsf{T}\underbrace{Q^\mathsf{T}Q}_{I}R\hat x = R^\mathsf{T}Q^\mathsf{T}b$$
$$R^\mathsf{T}R\hat x = R^\mathsf{T}Q^\mathsf{T}b$$

**$R$ is invertible** (Week 8's L26 §4 — its diagonal holds the nonzero Gram–Schmidt norms), so $R^\mathsf{T}$ is too, and cancelling gives

$$\boxed{\;R\hat x = Q^\mathsf{T}b\;}$$

**A triangular solve — $n^2$ operations, back substitution, Week 0's L02 §1.**

**And $A^\mathsf{T}A$ never appears.** The condition number is never squared; the whole computation runs at $\operatorname{cond}(A)$, which is the best any method could do.

---

## 4. But *Which* QR

**Here the lecture takes a turn, and the measurement is the reason.**

Week 8's L26 §5 warned that classical and modified Gram–Schmidt are numerically poor when the columns are nearly dependent — **and Läuchli's matrix is exactly that case.** So the natural experiment is three methods, not two:

**All three solving the same least-squares problem, exact answer $\hat x_1 = \hat x_2 = 1/(2+\varepsilon^2)$:**

| $\varepsilon$ | normal equations | Gram–Schmidt QR | **Householder QR** | exact |
|---|---|---|---|---|
| $10^{-3}$ | $0.499999750$ | $0.499999750$ | $0.499999750$ | $0.499999750$ |
| $10^{-5}$ | $0.500000000$ | $0.499999959$ | $0.500000000$ | $0.500000000$ |
| $10^{-7}$ | $0.500000000$ | $\mathbf{0.511501869}$ | $0.500000000$ | $0.500000000$ |
| $10^{-8}$ | **FAILED (singular)** | $\mathbf{1.000000000}$ | $0.500000000$ | $0.500000000$ |
| $10^{-10}$ | **FAILED (singular)** | $\mathbf{1.000000000}$ | $0.500000000$ | $0.500000000$ |

**Three methods. Three different failure points. One survivor.**

**Read the table carefully, because it does not say what you expect.**

- **The normal equations look *fine* until they die.** At $\varepsilon = 10^{-7}$ they give nine correct digits — **and that is luck, not robustness.** $\operatorname{cond}(A^\mathsf{T}A)$ is already $2\times10^{14}$ there; the $2\times2$ system happens to be symmetric and the arithmetic happens to cancel favourably. **At $10^{-8}$ the luck runs out completely.**
- **Gram–Schmidt QR degrades *earlier* than the normal equations** — visibly wrong at $10^{-7}$, useless at $10^{-8}$. **The QR route is not automatically better.**
- **Householder QR is right to nine digits throughout**, including where both others have failed.

> **So "use QR instead of the normal equations" is not adequate advice.** **It matters which QR** —
> and Week 8's L26 §5 said so before the evidence: *Gram–Schmidt is the right thing to understand
> and the wrong thing to run.* **This table is that sentence, measured.**

---

## 5. What Householder Does Differently

**Gram–Schmidt builds $Q$ by subtracting**, and subtraction of nearly equal vectors cancels — the computed $q_j$ drift out of orthogonality, and the drift compounds.

**Householder never subtracts in that way.** It builds $Q$ as a **product of reflections**, each of the form

$$H = I - 2vv^\mathsf{T}, \qquad \lVert v\rVert = 1$$

**Each $H$ is exactly orthogonal by construction** — $H^\mathsf{T}H = I$ holds to machine precision no matter what $v$ is, because it is a formula and not an accumulation. Each reflection is chosen to zero out everything below the diagonal in one column, and **the sign is chosen to avoid cancellation** in forming $v$.

**And $Q$ is never assembled.** The reflections are applied to $A$ and to $b$ as they are computed, so what you store is the $v$'s — $O(mn)$ numbers rather than $m^2$.

> **This is what `numpy.linalg.lstsq`, MATLAB's backslash on a tall matrix, and LAPACK's `dgels` all
> do.** Not because Gram–Schmidt is wrong — it is a correct algorithm — but because **correct is not
> the same as usable**, which is the distinction Week 5's L18 §6 first drew about the determinant and
> which has now appeared five times.

---

## 6. The Practical Rules

| Situation | Do |
|---|---|
| **Least squares, any size** | `numpy.linalg.lstsq`, or `scipy.linalg.lstsq`. **Householder QR underneath** |
| **You want to understand what it did** | Form $A = QR$ by hand on a small case; solve $R\hat x = Q^\mathsf{T}b$ |
| **Normal equations** | For **hand calculation on small problems** and for derivations. **Not in code** |
| **Columns nearly dependent** | The SVD — **Week 11** — which handles rank deficiency as well |
| **Very large and sparse** | Iterative methods (LSQR, conjugate gradient). Neither $A^\mathsf{T}A$ nor $QR$ is formed |
| **Ever** | Do not compute $(A^\mathsf{T}A)^{-1}$. **Week 1's L05 §6 said so, and this is the case it meant** |

> **Two caveats on the table, both honest.**
>
> **The normal equations are not always wrong.** For a well-conditioned $A$ — say
> $\operatorname{cond}(A) < 10^{4}$ — squaring costs you eight digits out of sixteen and leaves
> eight, which is often plenty. **They are also cheaper**: $mn^2/2$ against Householder's $2mn^2$,
> a factor of four. **The objection is that you rarely know $\operatorname{cond}(A)$ in advance**,
> and the failure is silent.
>
> **And Gram–Schmidt is not useless.** *Modified* Gram–Schmidt with **reorthogonalisation** — run
> the subtraction twice — is competitive with Householder and is used where the columns arrive one
> at a time and $Q$ is genuinely needed.

---

## 7. What to Take Away

1. **$\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$**, so forming the normal equations **doubles the digits lost.**
2. **Läuchli's matrix:** two obviously independent columns, and $A^\mathsf{T}A$ **exactly singular in floating point** at $\varepsilon = 10^{-8}$. The information was destroyed by the method.
3. **$A = QR$ turns the normal equations into $R\hat x = Q^\mathsf{T}b$** — a triangular solve, with $A^\mathsf{T}A$ never formed.
4. **But which QR matters.** Gram–Schmidt QR fails *earlier* than the normal equations on this problem; **Householder QR is right throughout.**
5. **The normal equations' good values in the table are luck**, not robustness — $\operatorname{cond}(A^\mathsf{T}A)$ was already $2\times10^{14}$ where they still looked exact.
6. **Householder builds $Q$ from reflections $I - 2vv^\mathsf{T}$**, each exactly orthogonal by construction, and never assembles $Q$.
7. **"Correct" and "usable" are different properties** — the fifth instance this term, after Cramer's rule, the adjugate, the $n!$ determinant and the characteristic polynomial.

---

## Exercises

*(Not assessed.)*

1. Verify by hand that $A^\mathsf{T}A = \begin{bmatrix}1+\varepsilon^2&1\\1&1+\varepsilon^2\end{bmatrix}$ for Läuchli's matrix, and that $\det = 2\varepsilon^2 + \varepsilon^4$.
2. At what $\varepsilon$ does $1 + \varepsilon^2$ round to $1$ in double precision? **Derive it from $\varepsilon_{\text{mach}} = 2^{-52}$** and check against the table.
3. Substitute $A = QR$ into the normal equations and reach $R\hat x = Q^\mathsf{T}b$. **Justify the cancellation of $R^\mathsf{T}$.**
4. $\operatorname{cond}(A) = 10^5$. How many digits do you expect from the normal equations, and from QR? Which would you use, and does the answer change if $\operatorname{cond}(A) = 10^2$?
5. Show that $H = I - 2vv^\mathsf{T}$ with $\lVert v\rVert = 1$ satisfies $H^\mathsf{T} = H$ and $H^2 = I$. **What does that say about $H$ geometrically, and what is $\det H$?**
6. Count the operations: normal equations ($mn^2/2$ to form $A^\mathsf{T}A$, plus $n^3/3$) against Householder ($2mn^2$). At $m = 10^6$, $n = 5$, **which is cheaper and by how much?** Does that change your answer to exercise 4?
7. Run `leastsquares.py` and add $\varepsilon = 10^{-6}$ to the comparison table. **Predict which methods survive before running it.**

---

*MATH 241 · Week 9 · L28 · © CSE Department*
