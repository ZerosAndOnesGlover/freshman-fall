# MATH 241 · Problem Set 12
## Synthesis: PCA, PageRank and Fourier by Hand

---

**Released:** Week 12, Wednesday · **Due:** Week 12, **Friday 17:00** *(last teaching week)*
**Total: 100 points** · Submit one PDF, `PS12_{LastName}_{StudentID}.pdf`

> **This is deliberately short.** PS 11 is due the same afternoon, the final is ten days later, and
> the Problem Sets component **drops your lowest mark**. **Everything here is by hand, on numbers
> chosen to come out exactly**, and three of the four questions are the kind of computation the final
> asks for. **No computer is needed.**
>
> **Collaboration on approaches is fine; the write-up must be yours.**

---

### Q1: PCA and Regression on Four Points (30 points)

The points $(6, 8)$, $(-6, -8)$, $(-4, 3)$, $(4, -3)$ are the rows of a $4\times2$ matrix $D$.

**(a) [4]** Check that the points are centred. Compute $D^\mathsf{T}D$.

**(b) [8]** Show that $(3,4)$ and $(-4,3)$ are eigenvectors of $D^\mathsf{T}D$ and find the eigenvalues. **Give the two principal directions, the two singular values of $D$, and the fraction of the total variance each direction explains.**

**(c) [8]** Compute each point's **score** — its coordinate along the first principal direction — and its distance from the first principal line. **Check that the sum of squared distances equals $\sigma_2^2$**, and say which theorem made that inevitable.

**(d) [10]** Now fit $y = mx$ by **ordinary least squares** (the points are centred, so no intercept is needed).

- Give $m$ exactly, and compare with the slope of the first principal line.
- **Which points pull the two lines apart, and why do they affect one method more than the other?**
- Compute the sum of squared **vertical** distances and the sum of squared **perpendicular** distances for **both** lines, and **state which line wins each contest.**

---

### Q2: PageRank on Three Pages (30 points)

Links: $0 \to 1$, $\quad 1 \to 0$ and $1 \to 2$, $\quad 2 \to 0$.

**(a) [6]** Write the Markov matrix $P$. **Find the PageRank without damping** — the $\lambda = 1$ eigenvector with entries summing to $1$ — exactly.

**(b) [8]** Show that the characteristic polynomial of $P$ is $\lambda^3 - \tfrac12\lambda - \tfrac12$ *(monic convention)*, factor out $\lambda - 1$, and find the other two eigenvalues. **Does power iteration converge for this $P$? At what rate, and how does the error behave step to step?**

**(c) [10]** Now damp with $\alpha = \tfrac45$: $G = \tfrac45P + \tfrac1{15}\mathbf{1}\mathbf{1}^\mathsf{T}$.

- **Prove** that if $\mathbf{1}^\mathsf{T}w = 0$ then $Gw = \tfrac45Pw$. Deduce that **every eigenvalue of $G$ other than $1$ is $\tfrac45$ times an eigenvalue of $P$.** *(You may assume the eigenvectors of $P$ for $\lambda \ne 1$ have entries summing to zero — prove it for a bonus mark.)*
- Give the eigenvalues of $G$ and $\lvert\lambda_2(G)\rvert$.
- **Find the PageRank of $G$ exactly.**

**(d) [6]** **Without damping, pages $0$ and $1$ tie. With damping they do not.** Say which page moves ahead, and explain why in terms of the links — not the arithmetic.

---

### Q3: Fourier, and a Famous Sum (25 points)

Let $f(t) = t$ on $(-\pi, \pi)$, with $\langle f, g\rangle = \int_{-\pi}^{\pi}fg\,dt$.

**(a) [4]** **Without integrating**, show that every cosine coefficient $a_k$ is zero.

**(b) [8]** Show $b_k = \dfrac{\langle f, \sin kt\rangle}{\langle\sin kt, \sin kt\rangle} = \dfrac{2(-1)^{k+1}}{k}$. *(Integrate by parts once.)*

**(c) [8]** **Pythagoras in a function space.** Because $\sin t, \sin 2t, \dots$ are orthogonal and complete for odd functions,

$$\lVert f\rVert^2 = \sum_k b_k^2\,\lVert\sin kt\rVert^2.$$

Compute both sides, and **deduce $\displaystyle\sum_{k=1}^\infty\frac{1}{k^2} = \frac{\pi^2}{6}$.**

**(d) [5]** What fraction of $\lVert f\rVert^2$ is captured by the first **one**, **three** and **ten** terms? Give each as an exact expression and as a percentage to two decimal places.

---

### Q4: The Course in One Table (15 points)

**(a) [8]** For each of **regression, PCA, PageRank and Fourier**, write one line each giving: the matrix (or space) involved; the object computed; the week whose theorem guarantees it exists; and whether orthogonality is used.

**(b) [4]** **Which one of the four is not an orthogonal projection?** Name the hypothesis it needed instead, and where that hypothesis came from.

**(c) [3]** L36 §6 and Week 9's L28 make the same numerical point about two different computations. **State the point in one sentence** and name both computations.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | PCA and regression on four points | 30 |
| 2 | PageRank on three pages | 30 |
| 3 | Fourier, and a famous sum | 25 |
| 4 | The course in one table | 15 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*MATH 241 · Week 12 · PS 12 · © CSE Department*
