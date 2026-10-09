# MATH 241 · Linear Algebra
## Week 12 · Lecture 2 of 3 · **Tuesday**
### PageRank: An Eigenvector Too Large to Factor

*“We came up with the notion that not all web pages are created equal. People are – but not web pages.”* — Sergey Brin, guest lecture at UC Berkeley (2005)

---

**Reading:** Strang's Markov matrices section (§6.4 or §10.3, depending on printing), revisited · **Previous:** L36, regression and PCA · **Next:** L38, Fourier and the course in one table

**Coursework:** 📝 **PS 12** released Wed this week, due Fri this week 17:00 · 💬 **Recitation 11** Thu this week 15:00–15:50 · 📝 **PS 11** due Fri this week 17:00 · 📕 **Final exam** Mon of finals week 09:00–11:30

> **PS 11 and PS 12 are due Friday.** PS 12 is released tomorrow. **Recitation 11 is Thursday.**
>
> **Week 0's L03 §2 made a promise on the second day of term**: *PageRank is not solved by
> elimination, because $n^3/3$ at $n = 10^9$ is ten million years.* Week 7's L23 §5 named the method.
> **Today it is carried out, on a web small enough to check exactly.**

---

## 1. The Question

**Which pages matter?** Counting links is easy to game — make a thousand pages that link to yours. **PageRank's answer is recursive: a page matters if pages that matter link to it.**

That sounds circular, and it is — **it is an eigenvector equation.** Let $x_i$ be page $i$'s importance, and suppose page $j$, with $d_j$ outgoing links, passes $x_j/d_j$ to each page it links to. Then

$$x_i = \sum_{j \to i}\frac{x_j}{d_j}, \qquad\text{i.e.}\qquad x = Px,$$

where $P_{ij} = 1/d_j$ if $j$ links to $i$. **$P$ is a Markov matrix** — non-negative, each column summing to $1$ — **and PageRank is its $\lambda = 1$ eigenvector.** Week 7's L23 §5 proved $\lambda = 1$ is always there.

> **The random surfer.** Equivalently: someone clicks links at random forever. $x_i$ is the fraction
> of time they spend on page $i$. **Week 7's steady state, with pages as states.**

---

## 2. Six Pages, and Two Repairs

$$0 \to 1, 2 \qquad 1 \to 2 \qquad 2 \to 0 \qquad 3 \to 2, 4 \qquad 4 \to 3, 5 \qquad 5 \to \text{(nothing)}$$

**Two things are wrong with $P$ as defined, and both are real features of the web.**

**(a) Page 5 is *dangling*** — it links nowhere, so its column is all zeros and $P$ is not Markov. **Repair:** a surfer on a dead end jumps to a page chosen uniformly. Column 5 becomes $\tfrac16(1,1,1,1,1,1)$.

**(b) The surfer can get trapped.** Pages $0$, $1$, $2$ link only among themselves: once in, never out. §5 shows what that does. **Repair — damping:** at each step, with probability $\alpha$ follow a link, and with probability $1 - \alpha$ jump to a uniformly random page:

$$\boxed{\;G = \alpha P + \frac{1-\alpha}{n}\mathbf{1}\mathbf{1}^\mathsf{T}, \qquad \alpha = 0.85\;}$$

**$G$ is still Markov** — each column is a mixture of two columns that sum to $1$ — **and every entry is now positive.** $\alpha = 0.85$ is the value in Brin and Page's paper.

---

## 3. The Exact Answer

**For six pages, solve $(G - I)x = 0$ with $\sum x_i = 1$ exactly** (`applications.py` §5, in `Fraction`, with $\alpha = \tfrac{17}{20}$):

| page | PageRank | |
|---:|---:|---:|
| $0$ | $\tfrac{29447}{91988}$ | $0.320118$ |
| $1$ | $\tfrac{31133}{183976}$ | $0.169223$ |
| $\mathbf{2}$ | $\tfrac{62107}{183976}$ | $\mathbf{0.337582}$ |
| $3$ | $\tfrac{3}{52}$ | $0.057692$ |
| $4$ | $\tfrac{3}{52}$ | $0.057692$ |
| $5$ | $\tfrac{3}{52}$ | $0.057692$ |

**$Gx = x$ exactly, the entries sum to exactly $1$, and every column of $G$ sums to exactly $1$** — all checked in rational arithmetic.

**Read it.** Page $2$ wins: three pages link to it. **Page $0$ is a close second with only one incoming link — but that link is from page $2$**, the most important page, which gives page $0$ its whole share. **That is the recursion working.** Page $1$ gets half of page $0$'s vote. Pages $3$, $4$, $5$ receive nothing from the $\{0,1,2\}$ cluster and live on teleports and each other.

---

## 4. What Google Actually Computes: Powers

**Nobody solves $(G - I)x = 0$ at $n = 10^9$.** The method is Week 7's: **multiply any starting vector by $G$, repeatedly.**

$$x^{(k+1)} = Gx^{(k)}, \qquad x^{(0)} = \tfrac1n\mathbf{1}.$$

**Week 7's L23 §5 said the error shrinks like $\lvert\lambda_2\rvert^k$.** So find $\lambda_2$. The script computes $G$'s characteristic polynomial **exactly** (Faddeev–LeVerrier in `Fraction`) and then its roots:

| eigenvalue | $\lvert\lambda\rvert$ |
|---|---:|
| $1$ | $1$ |
| $-0.425 \pm 0.425\,i$ | $\mathbf{0.601041}$ |
| $0.566667$ | $0.566667$ |
| $-0.425$ | $0.425$ |
| $0$ | $0$ |

*(Largest $\lvert p(\lambda)\rvert$ at the computed roots: $3.1\times10^{-17}$.)*

**And the iteration, measured in float:**

| $k$ | $\lVert x^{(k)} - x\rVert_1$ | $\lvert\lambda_2\rvert^k$ |
|---:|---:|---:|
| $1$ | $3.705\times10^{-1}$ | $6.010\times10^{-1}$ |
| $10$ | $2.938\times10^{-3}$ | $6.152\times10^{-3}$ |
| $20$ | $9.584\times10^{-6}$ | $3.785\times10^{-5}$ |
| $40$ | $2.813\times10^{-10}$ | $1.433\times10^{-9}$ |
| $60$ | $8.313\times10^{-15}$ | $5.423\times10^{-14}$ |

**Average reduction per step from $k = 10$ to $60$: $0.5875$**, against $\lvert\lambda_2\rvert = 0.6010$. **The error tracks $\lvert\lambda_2\rvert^k$ to within a constant, for sixty steps, down to rounding.**

> **Why the step-by-step ratio wobbles.** $\lambda_2$ is a **complex pair**, so the error does not
> shrink by the same factor each step — it **spirals in**, rotating as it decays. **Week 7's L23 §3
> said $\lvert\lambda\rvert$ decides everything and the argument of $\lambda$ decides the
> rotation**, and this is that, on a web.

---

## 5. Why the Damping Is There

**Remove it and the method can fail in two different ways**, both Week 6 and Week 7 phenomena (`applications.py` §6).

**(a) It never settles.** A two-page cycle, $0 \to 1 \to 0$, has $P = \begin{bmatrix}0&1\\1&0\end{bmatrix}$ with eigenvalues $1$ and $\mathbf{-1}$. Starting from $(1, 0)$, the iteration gives $(0,1), (1,0), (0,1), \dots$ forever. **$\lvert\lambda_2\rvert = 1$, so nothing decays.**

**(b) The answer is not unique.** Two separate cycles, $\{0,1\}$ and $\{2,3\}$. **Three different starting vectors are all fixed points**:

$$\left(\tfrac12, \tfrac12, 0, 0\right), \qquad \left(0, 0, \tfrac12, \tfrac12\right), \qquad \left(\tfrac14, \tfrac14, \tfrac14, \tfrac14\right).$$

**$\lambda = 1$ has a two-dimensional eigenspace** — Week 6's geometric multiplicity — and "the" ranking depends on where the surfer started. **The question has no answer.**

**(c) With damping $0.85$**, the same split web has the **unique** PageRank $\left(\tfrac14, \tfrac14, \tfrac14, \tfrac14\right)$ and eigenvalue moduli $1, 0.85, 0.85, 0.85$.

> **The theorem that makes it work.** Damping makes every entry of $G$ positive. **Perron–Frobenius:**
> a matrix with all entries positive has a largest eigenvalue that is **simple**, with an eigenvector
> whose entries are all **positive**, and every other eigenvalue is strictly smaller in modulus. For a
> Markov matrix that largest eigenvalue is $1$. **A further result (Haveliwala and Kamvar, 2003)
> sharpens it for Google's $G$: $\lvert\lambda_2\rvert \le \alpha$**, whatever the web — attained in
> (c), where the web splits, and comfortably beaten in §4, where $\lvert\lambda_2\rvert = 0.601$.
>
> **So $\alpha$ is a dial.** Closer to $1$ follows the links more faithfully and converges more
> slowly; $0.85^{50} \approx 3\times10^{-4}$ is why Week 7 quoted about fifty iterations.

---

## 6. What It Costs

At web scale — $n = 10^9$ pages, about ten links per page:

| Method | Operations |
|---|---:|
| **elimination**, $n^3/3$ (Week 0) | $3.3\times10^{26}$ |
| **fifty power iterations**, each touching every link once | $5.0\times10^{11}$ |
| ratio | $\mathbf{6.7\times10^{14}}$ |

**And $G$ is never formed.** It is dense — every entry positive — but $Gx = \alpha Px + \tfrac{1-\alpha}{n}(\mathbf{1}^\mathsf{T}x)\mathbf{1}$, and $\mathbf{1}^\mathsf{T}x = 1$ for a probability vector. **So each step is one sparse multiplication by $P$ plus adding a constant.** Week 1's L04 lesson — never form what you can apply — at the largest scale in the course.

> **Week 0's promise, kept.** L03 §2: *ten million years.* Week 6's L19: *it is solved by repeatedly
> multiplying by $A$.* Week 7's L23: *the rate is $\lvert\lambda_2\rvert$.* **Today: an exact answer on
> six pages, a measured rate that matches the eigenvalue, and the reason the method needs damping at
> all.**

---

## 7. What PageRank Is Not

**Hold this for Friday.** PCA and regression were **projections onto orthonormal bases** — Week 8, with Week 10 and 11 supplying the bases. **PageRank is different in three visible ways:**

- **$G$ is not symmetric**, so Week 10 does not apply: its eigenvalues are complex (§4) and its eigenvectors are not orthogonal.
- **It is not a projection.** Nothing is being approximated; an exact eigenvector is wanted.
- **It is computed by iteration**, and the iteration is only well-posed because of a hypothesis — positivity — that had to be engineered in.

**L38 §6 uses this when it checks the syllabus's claim that all four applications are the same theorem.**

---

## 8. What to Take Away

1. **PageRank is the $\lambda = 1$ eigenvector of a Markov matrix**: a page matters if pages that matter link to it.
2. **Two repairs:** dangling pages jump uniformly; **damping** $G = \alpha P + \tfrac{1-\alpha}{n}\mathbf{1}\mathbf{1}^\mathsf{T}$ makes every entry positive.
3. **On six pages it can be found exactly** — and page $0$ ranks second on a single link, because of whose link it is.
4. **Power iteration converges like $\lvert\lambda_2\rvert^k$** — measured $0.5875$ per step against $\lvert\lambda_2\rvert = 0.601$ — and **spirals** when $\lambda_2$ is complex.
5. **Without damping it can oscillate forever ($\lambda = -1$) or have no unique answer (a repeated $\lambda = 1$).**
6. **Perron–Frobenius** makes the answer unique and positive; **$\lvert\lambda_2\rvert \le \alpha$** bounds the work.
7. **Fifty sparse products instead of $3\times10^{26}$ operations**, and $G$ is never formed.

---

## Exercises

*(Not assessed. PS 12 is the assessed work.)*

1. Three pages: $0 \to 1$, $1 \to 0, 2$, $2 \to 0$. **Write $P$. Find its PageRank without damping.** *(PS 12 Q2 adds damping.)*
2. **Show that $G = \alpha P + \tfrac{1-\alpha}{n}\mathbf{1}\mathbf{1}^\mathsf{T}$ is a Markov matrix** whenever $P$ is.
3. In §3, **why do pages $3$, $4$ and $5$ get exactly the same PageRank?** *(Write out the equations for those three rows.)*
4. For the two-cycle $\begin{bmatrix}0&1\\1&0\end{bmatrix}$ with damping $\alpha$, find the eigenvalues of $G$. **For which $\alpha$ does power iteration converge?**
5. **Why is $\mathbf{1}^\mathsf{T}x^{(k)} = 1$ at every step** if it is at step $0$? Why does that let you avoid forming $G$?
6. A web of $10^9$ pages with $\alpha = 0.85$. **How many iterations bring the error below $10^{-8}$** in the worst case the bound allows?
7. **Is PageRank a similarity invariant?** If you renumber the pages — $G \mapsto \Pi G\Pi^\mathsf{T}$ for a permutation $\Pi$ — what happens to $x$?

---

*MATH 241 · Week 12 · L37 · © CSE Department*
