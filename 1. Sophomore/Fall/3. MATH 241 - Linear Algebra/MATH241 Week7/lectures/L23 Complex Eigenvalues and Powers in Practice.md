# MATH 241 · Linear Algebra
## Week 7 · Lecture 3 of 3 · **Friday**
### Complex Eigenvalues, and Powers in Practice

*“Every kind of science, if it has only reached a certain degree of maturity, automatically becomes a part of mathematics.”* — David Hilbert, "Axiomatic Thought" (1918)

---

**Reading:** Strang §6.2 (the complex examples), §6.4 opening, §10.3 · **Previous:** L22, when it fails · **Next:** Week 8, orthogonality

**Coursework:** 📝 **PS 6** due today 17:00 · 📊 **Quiz 8** Mon of Week 8 · 📝 **PS 8** released Wed of Week 8, due Fri of Week 9 17:00 · 💬 **Recitation 7** Thu of Week 8 15:00–15:50

> **PS 6 is due at 17:00 today.** PS 7 was released Wednesday and is due the Friday of Week 8.

---

## 1. Complex Eigenvalues Are Normal, Not Pathological

Week 6's L19 §6 met a rotation with no real eigenvalues and called it correct. **This lecture takes it seriously**, because complex eigenvalues are what you get from **anything that oscillates** — and most things oscillate.

**For a real matrix, complex eigenvalues come in conjugate pairs.** $p(\lambda)$ has real coefficients, so $p(\bar\lambda) = \overline{p(\lambda)}$, and a root $\lambda$ forces $\bar\lambda$ to be one too. **The eigenvectors conjugate along with them:** $Av = \lambda v$ gives $A\bar v = \bar\lambda\bar v$, since $\bar A = A$.

$$R = \begin{bmatrix}0&-1\\ 1&0\end{bmatrix}: \qquad \lambda = \pm i, \qquad v = (1, \mp i)$$

**And L20 §2's identities hold unchanged:** $i + (-i) = 0 = \operatorname{trace}R$ and $i(-i) = 1 = \det R$. **Two real numbers, computed from a pair of complex ones** — which is possible precisely because the pair is conjugate.

> **A real matrix with complex eigenvalues is not diagonalisable over $\mathbb{R}$** — there is no
> real eigenvector to put in $S$ — **and it is diagonalisable over $\mathbb{C}$.** So "diagonalisable"
> depends on which field you are working over, and from here on the field is $\mathbb{C}$ unless
> stated otherwise. **L22's defective matrices are defective over $\mathbb{C}$ too**, and that is a
> genuinely different failure.

---

## 2. The Real Form: Rotation and Scaling

You can avoid complex arithmetic. **A real $2\times2$ with eigenvalues $re^{\pm i\theta}$ is similar, over $\mathbb{R}$, to**

$$r\begin{bmatrix}\cos\theta & -\sin\theta\\ \sin\theta & \cos\theta\end{bmatrix}$$

**a rotation by $\theta$ scaled by $r$.** This is as close to diagonal as $\mathbb{R}$ permits, and it says exactly what the transformation does.

**Read off the two numbers from the trace and determinant, without finding an eigenvector:**

$$\lambda\bar\lambda = r^2 = \det A \qquad\qquad \lambda + \bar\lambda = 2r\cos\theta = \operatorname{trace}A$$

$$\boxed{\;r = \sqrt{\det A}, \qquad \cos\theta = \frac{\operatorname{trace}A}{2\sqrt{\det A}}\;}$$

**Worked:** $B = \begin{bmatrix}1&-1\\1&1\end{bmatrix}$ has $\operatorname{trace} = 2$, $\det = 2$, so $r = \sqrt2$ and $\cos\theta = 2/(2\sqrt2) = 1/\sqrt2$, giving $\theta = 45°$. **$B$ rotates by $45°$ and scales by $\sqrt2$** — and indeed $\lambda = 1 \pm i = \sqrt2\,e^{\pm i\pi/4}$.

> **This is the shape underneath every damped oscillation.** $r$ is the growth or decay per step;
> $\theta$ is the frequency. **ECE 211 next term is that sentence for a whole course**, and the
> reason $e^{i\omega t}$ appears everywhere in signals is that it is an eigenvector of
> differentiation.

---

## 3. $\lvert\lambda\rvert$ Decides Everything

For iteration $x_{k+1} = Ax_k$ — that is, $x_k = A^kx_0$ — **the modulus of the eigenvalues is the whole story.**

$$A^k = S\Lambda^kS^{-1} \quad\Longrightarrow\quad \Lambda^k = \operatorname{diag}(\lambda_1^k, \dots, \lambda_n^k)$$

**and $\lambda^k$ does one of three things.** Writing $\lambda = re^{i\theta}$: $\lambda^k = r^ke^{ik\theta}$, so the **angle spins** and the **modulus decides the fate**.

| | Behaviour |
|---|---|
| $\lvert\lambda\rvert < 1$ | $\lambda^k \to 0$ |
| $\lvert\lambda\rvert = 1$ | bounded, never settling — rotates forever |
| $\lvert\lambda\rvert > 1$ | $\lvert\lambda^k\rvert \to \infty$ |

**Measured, on a rotation by $30°$ scaled three ways:**

| | $\lambda$ | $\lvert\lambda\rvert$ | Orbit |
|---|---|---:|---|
| rotate $30°$ | $0.866 \pm 0.500i$ | $1.000$ | a **circle** |
| $\times 1.1$ | $0.953 \pm 0.550i$ | $1.100$ | **spirals out** |
| $\times 0.9$ | $0.779 \pm 0.450i$ | $0.900$ | **spirals in** |

**After 24 steps at $r = 1.1$ a point is $9.85$ times further out; at $r = 0.9$ it is $0.080$ times as far.** The angle is doing the same thing in all three cases; only the modulus differs.

> **So the stability criterion for any linear iteration is one inequality:**
> $$\boxed{\;A^k \to 0 \iff \lvert\lambda_i\rvert < 1 \text{ for every } i\;}$$
> **The largest $\lvert\lambda\rvert$ is called the *spectral radius*.** It is what "will this
> converge" means, in numerical linear algebra, control theory and the analysis of every iterative
> method you will meet.
>
> *(For a defective matrix the same criterion holds, with a polynomial factor in $k$ that does not
> change the conclusion — L22's Jordan blocks contribute $k^j\lambda^k$, and $r < 1$ still wins.)*

---

## 4. Fibonacci, in Closed Form

$$\begin{bmatrix}F_{k+1}\\ F_k\end{bmatrix} = \begin{bmatrix}1&1\\ 1&0\end{bmatrix}\begin{bmatrix}F_k\\ F_{k-1}\end{bmatrix} \qquad\Longrightarrow\qquad \begin{bmatrix}F_{k+1}\\ F_k\end{bmatrix} = F^k\begin{bmatrix}1\\ 0\end{bmatrix}$$

**Week 1's L04 §6 wrote this down and could not do anything with it.** Now: $\operatorname{trace}F = 1$, $\det F = -1$, so

$$\lambda^2 - \lambda - 1 = 0 \qquad\Longrightarrow\qquad \lambda = \frac{1 \pm \sqrt5}{2}$$

$$\varphi = 1.6180339887\ldots \qquad\qquad \psi = \frac{1-\sqrt5}{2} = -0.6180339887\ldots$$

**Distinct, so diagonalisable, so $F^k = S\Lambda^kS^{-1}$**, and reading off the bottom entry gives

$$\boxed{\;F_k = \frac{\varphi^k - \psi^k}{\sqrt5}\;}$$

**Binet's formula.** Verified exactly:

| $k$ | $F_k$ | $(\varphi^k - \psi^k)/\sqrt5$ | $\varphi^k/\sqrt5$ |
|---:|---:|---:|---:|
| 5 | $5$ | $5.000000$ | $4.959675$ |
| 10 | $55$ | $55.000000$ | $55.003636$ |
| 20 | $6765$ | $6765.000000$ | $6765.000030$ |
| 30 | $832040$ | $832040.000000$ | $832040.000000$ |

**Two things to notice.** The formula is **exact** — a ratio of irrationals producing an integer every time. And since $\lvert\psi\rvert < 1$, **$\psi^k$ dies**, so $F_k \approx \varphi^k/\sqrt5$: the last column converges to the third from above.

> **The golden ratio appears in the Fibonacci sequence because it is an eigenvalue.** Not by
> numerology — $\varphi$ is a root of $\lambda^2 = \lambda + 1$, which is the recurrence written as a
> characteristic equation. **Every linear recurrence has a closed form obtained exactly this way**,
> and the closed form is $\sum c_i\lambda_i^k$ over the eigenvalues.

---

## 5. Markov Chains, and Why They Settle

$$P = \begin{bmatrix}0.9 & 0.2\\ 0.1 & 0.8\end{bmatrix}$$

**A *Markov matrix*: entries $\ge 0$, and each column sums to $1$.** It moves probability around — column $j$ says where the population in state $j$ goes next.

**$\lambda = 1$ is always an eigenvalue of such a matrix.** *Why:* the columns summing to $1$ says $(1,1,\dots,1)P = (1,1,\dots,1)$, so $(1,\dots,1)$ is an eigenvector of $P^\mathsf{T}$ with $\lambda = 1$ — and **$P$ and $P^\mathsf{T}$ share eigenvalues** (Week 6's PS 6 Q5(b)). **No computation required.**

Here: $\operatorname{trace} = 1.7$, $\det = 0.70$, so $\lambda = 1$ and $\lambda = 0.7$.

**The steady state is the $\lambda = 1$ eigenvector:** $(P - I)v = 0$ gives $v = (2,1)$, normalised $(\tfrac23, \tfrac13)$.

**And now the powers, measured:**

| $k$ | $P^k$ |
|---:|---|
| 1 | $\begin{bmatrix}0.900&0.200\\ 0.100&0.800\end{bmatrix}$ |
| 5 | $\begin{bmatrix}0.723&0.555\\ 0.277&0.445\end{bmatrix}$ |
| 20 | $\begin{bmatrix}0.6669&0.6661\\ 0.3331&0.3339\end{bmatrix}$ |
| 60 | $\begin{bmatrix}0.66667&0.66667\\ 0.33333&0.33333\end{bmatrix}$ |

**Every column converges to $(\tfrac23,\tfrac13)$** — the steady state, **regardless of where you started.**

### The rate is the second eigenvalue

$\Lambda^k = \operatorname{diag}(1^k, 0.7^k) = \operatorname{diag}(1, 0.7^k)$. **The $1$ stays and everything else decays**, at the rate of the second-largest $\lvert\lambda\rvert$:

$$0.7^5 = 0.168, \qquad 0.7^{20} = 7.98\times10^{-4}, \qquad 0.7^{60} = 5.08\times10^{-10}$$

$$\boxed{\;\text{"how fast does it mix" } = \text{ a question about } \lvert\lambda_2\rvert\;}$$

> **This is PageRank.** The web graph's transition matrix has $\lambda_1 = 1$ with the PageRank
> vector as its eigenvector, and repeatedly multiplying **any** starting vector by it converges to
> that eigenvector at rate $\lvert\lambda_2\rvert^k$. **Google's original paper reports about fifty
> iterations** — which is $\lvert\lambda_2\rvert \approx 0.85$ and $0.85^{50} \approx 3\times10^{-4}$.
>
> **And this closes a loop from Week 0.** L03 §2 said PageRank cannot be solved by elimination:
> $n^3/3$ at $n = 10^9$ is ten million years. **It is solved by fifty matrix–vector products**, each
> $O(\text{nonzeros})$, because the answer wanted is an eigenvector and not a solve. **Week 0
> promised the explanation would be here.**

---

## 6. What to Take Away

1. **Complex eigenvalues are normal**, and for a real matrix they come in **conjugate pairs**, with conjugate eigenvectors. Trace and determinant stay real.
2. **Diagonalisable over $\mathbb{C}$ is not the same as over $\mathbb{R}$.** A rotation is the first; it is not the second.
3. **A real $2\times2$ with complex eigenvalues is a rotation by $\theta$ scaled by $r$**, with $r = \sqrt{\det A}$ and $\cos\theta = \operatorname{trace}A/(2\sqrt{\det A})$ — **no eigenvector needed.**
4. **$\lvert\lambda\rvert$ decides everything** for iteration: $<1$ decays, $=1$ persists, $>1$ blows up. The largest is the **spectral radius**, and $A^k \to 0 \iff$ all $\lvert\lambda_i\rvert < 1$.
5. **Binet's formula is $F^k = S\Lambda^kS^{-1}$ read off**, and **the golden ratio is in the Fibonacci sequence because it is an eigenvalue.** Every linear recurrence works this way.
6. **A Markov matrix always has $\lambda = 1$**, its eigenvector is the steady state, and every column of $P^k$ converges to it from any start.
7. **The mixing rate is $\lvert\lambda_2\rvert$** — and **PageRank is fifty matrix–vector products**, which is why Week 0 said it is not a linear solve.

---

## Exercises

*(Not assessed. PS 7 is due Friday of Week 8.)*

1. $A = \begin{bmatrix}2&-3\\ 3&2\end{bmatrix}$. Find the complex eigenvalues, then **use §2 to give $r$ and $\theta$ without them** and check the two agree.
2. For which real $c$ does $\begin{bmatrix}0&1\\ -1&c\end{bmatrix}$ have complex eigenvalues? For which does the iteration $x_{k+1} = Ax_k$ converge to $0$?
3. Write the recurrence $a_{k+1} = 5a_k - 6a_{k-1}$ as a matrix power, find the eigenvalues, and give a closed form for $a_k$ with $a_0 = 0$, $a_1 = 1$. **Check it at $k = 4$.**
4. $P = \begin{bmatrix}0.8&0.3\\ 0.2&0.7\end{bmatrix}$. Find the steady state and the second eigenvalue. **How many steps until $P^k$ is within $10^{-6}$ of its limit?**
5. Prove that a Markov matrix has $\lambda = 1$, using the column sums and Week 6's fact about $A$ and $A^\mathsf{T}$.
6. $A$ is $3\times3$ with eigenvalues $1, 0.5, -0.5$. Describe $A^k$ as $k \to \infty$. **What if the eigenvalues were $1, 0.5, -1$?**
7. **Why does a Markov matrix never have an eigenvalue with $\lvert\lambda\rvert > 1$?** *(Think about what $P^k$ does to a probability vector, and what would happen if some $\lvert\lambda\rvert$ exceeded 1.)*

---

*MATH 241 · Week 7 · L23 · © CSE Department*
