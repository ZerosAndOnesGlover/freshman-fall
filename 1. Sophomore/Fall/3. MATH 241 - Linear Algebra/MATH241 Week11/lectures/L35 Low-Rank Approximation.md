# MATH 241 · Linear Algebra
## Week 11 · Lecture 3 of 3 · **Friday**
### Low-Rank Approximation

*“It is better to be content with the fraction of a right solution than to beguile ourselves with the whole of a wrong solution.”* — Karl Pearson, *The Grammar of Science* (1892), Introductory

---

**Reading:** Strang §7.1 (image processing) · **Previous:** L34, what the SVD tells you · **Next:** Week 12's L36, PCA

**Coursework:** 📝 **PS 10** due today 17:00 · 📝 **PS 12** released Wed of Week 12, due Fri of Week 12 17:00 · 💬 **Recitation 11** Thu of Week 12 15:00–15:50 · 📕 **Final exam** Mon of finals week 09:00–11:30

> **PS 10 is due at 17:00 today**, alongside **CS 211's Project 1**. **PS 11 was released
> Wednesday** and is due **Friday of Week 12** — with Thanksgiving recess in between, and **PS 12
> due that same Friday.** Plan for it now.
>
> **No classes Nov 24.** Week 12 begins Monday Dec 1, and it is the last teaching week.

---

## 1. The Best Approximation of Lower Rank

**L33 §5 wrote every matrix as a sum of rank-one pieces in decreasing order:**

$$A = \sigma_1u_1v_1^\mathsf{T} + \sigma_2u_2v_2^\mathsf{T} + \cdots + \sigma_ru_rv_r^\mathsf{T}.$$

**The obvious way to approximate $A$ by something simpler is to stop early.** Keep $k$ terms:

$$A_k = \sigma_1u_1v_1^\mathsf{T} + \cdots + \sigma_ku_kv_k^\mathsf{T}.$$

**The theorem is that the obvious thing is optimal**, and there is nothing better to find.

> **Eckart–Young (1936).** Among **all** matrices of rank at most $k$, $A_k$ is the closest to $A$,
> and the error is exactly what was thrown away:
>
> $$\min_{\operatorname{rank}X \le k}\lVert A - X\rVert_2 = \lVert A - A_k\rVert_2 = \sigma_{k+1}, \qquad \min_{\operatorname{rank}X \le k}\lVert A - X\rVert_F = \sqrt{\sigma_{k+1}^2 + \cdots + \sigma_r^2}.$$

**The first statement is L34 §5's claim made precise:** $\sigma_{k+1}$ is the distance from $A$ to the nearest matrix of rank $k$. **A small singular value means a nearby lower-rank matrix**, and that is why thresholding singular values is the right way to decide rank.

*Why it is plausible, not a proof:* $A - A_k = \sum_{j>k}\sigma_ju_jv_j^\mathsf{T}$ is itself in SVD form, so its largest singular value is $\sigma_{k+1}$. **That shows $A_k$ achieves $\sigma_{k+1}$.** That nothing does better needs a dimension argument — any rank-$k$ $X$ has a null space of dimension $n - k$, which must meet the $(k+1)$-dimensional span of $v_1,\dots,v_{k+1}$, and on a unit vector in that intersection $\lVert(A - X)x\rVert = \lVert Ax\rVert \ge \sigma_{k+1}$. **PS 11 Q5 asks for the details.**

---

## 2. Measured

`resources/svd.py` §9 takes an $8\times6$ matrix of random integers, with

$$\sigma = 28.3477,\ \ 20.5879,\ \ 16.048,\ \ 9.965,\ \ 4.3655,\ \ 3.4133,$$

and checks both formulas at every $k$:

| $k$ | $\lVert A - A_k\rVert_2$ | $\sigma_{k+1}$ | $\lVert A - A_k\rVert_F$ | $\sqrt{\sum_{j>k}\sigma_j^2}$ |
|---:|---:|---:|---:|---:|
| $1$ | $20.587861$ | $20.587861$ | $28.485223$ | $28.485223$ |
| $2$ | $16.047980$ | $16.047980$ | $19.686237$ | $19.686237$ |
| $3$ | $9.965048$ | $9.965048$ | $11.402205$ | $11.402205$ |
| $4$ | $4.365518$ | $4.365518$ | $5.541489$ | $5.541489$ |
| $5$ | $3.413261$ | $3.413261$ | $3.413261$ | $3.413261$ |

**Then it tries to beat $A_2$** (error $16.047980$) with other rank-2 matrices:

| Competitor | $\lVert A - X\rVert_2$ |
|---|---:|
| project $A$ onto its two largest columns | $18.671191$ |
| $A_2$ with every factor entry nudged by $1\%$ | $16.048962$ |
| a random rank-2 projection of $A$ | $28.090907$ |
| **the best of $2000$ random rank-2 projections** | **$1.015\times$ the optimum** |

**Nothing gets under $\sigma_3$.** The $1\%$ nudge comes closest and still loses — **the optimum is a genuine minimum, not a flat region.**

---

## 3. Compressing a Picture

**An image is a matrix of pixel intensities**, and a rank-$k$ approximation stores $k$ singular values, $k$ columns of $U$ and $k$ of $V$:

$$\text{storage} = k\,(m + n + 1) \quad\text{instead of}\quad mn.$$

`svd.py` §10 draws a $24\times32$ picture — a bar, a post and a ring, $768$ numbers — whose singular values are

$$14.19,\ \ 6.11,\ \ 4.37,\ \ 2.93,\ \ 1.99,\ \ 1.21,\ \ 0.64,\ \ 0,\ 0,\ \dots$$

**Numerical rank $7$ out of a possible $24$.**

| $k$ | stored | of full | relative error $\lVert A - A_k\rVert_F/\lVert A\rVert_F$ | energy kept |
|---:|---:|---:|---:|---:|
| $1$ | $57$ | $7.4\%$ | $0.5101$ | $73.98\%$ |
| $2$ | $114$ | $14.8\%$ | $0.3509$ | $87.68\%$ |
| $3$ | $171$ | $22.3\%$ | $0.2301$ | $94.71\%$ |
| $4$ | $228$ | $29.7\%$ | $0.1466$ | $97.85\%$ |
| $5$ | $285$ | $37.1\%$ | $0.0830$ | $99.31\%$ |
| $6$ | $342$ | $44.5\%$ | $0.0391$ | $99.85\%$ |
| $7$ | $399$ | $52.0\%$ | $0.0000$ | $100.00\%$ |

*"Energy kept" is $\sum_{j\le k}\sigma_j^2 / \sum_j\sigma_j^2$ — the fraction of $\lVert A\rVert_F^2$ retained.*

**What the approximations look like** (the script's own rendering; darker characters are brighter pixels):

**Rank 1**

```text
                                
                                
  ++@@@@+++++++@@@@####@@@@+++  
  ++@@@@+++++++@@@@####@@@@+++  
  ++@@@@+++++++@@@@####@@@@+++  
  ++@@@@+++++++@@@@####@@@@+++  
  ++@@@@+++++++@@@@####@@@@+++  
  ..----.......::::::::::::...  
  ..----.......::::::::::::...  
  ::++++:::::::-===----===-:::  
  --####-------+*++++++++*+---  
  ::****:::::::=+========+=:::  
  ::****:::::::=+==----==+=:::  
  ::++++:::::::-=--------=-:::  
  ::++++:::::::-=--------=-:::  
  ::++++:::::::-=--------=-:::  
  ::++++:::::::-=--------=-:::  
  ::****:::::::=+==----==+=:::  
  ::****:::::::=+========+=:::  
  --####-------+*++++++++*+---  
  ::++++:::::::-===----===-:::  
  ..----.......::::::::::::...  
                                
                                
```

**Rank 2**

```text
                                
                                
  @@@@@@@@@@@@@#@@@@@@@@@@#@@@  
  @@@@@@@@@@@@@#@@@@@@@@@@#@@@  
  @@@@@@@@@@@@@#@@@@@@@@@@#@@@  
  @@@@@@@@@@@@@#@@@@@@@@@@#@@@  
  @@@@@@@@@@@@@#@@@@@@@@@@#@@@  
    ++++       :=:.    .:=:     
    ++++       :=:.    .:=:     
  ..****.......=+=------=+=...  
  ::@@@@:::::::+#++====++#+:::  
    @@@@       =#=-::::-=#=     
    @@@@       =#=-::::-=#=     
    @@@@       =*-:....:-*=     
    @@@@       =*-:....:-*=     
    @@@@       =*-:....:-*=     
    @@@@       =*-:....:-*=     
    @@@@       =#=-::::-=#=     
    @@@@       =#=-::::-=#=     
  ::@@@@:::::::+#++====++#+:::  
  ..****.......=+=------=+=...  
    ++++       :=:.    .:=:     
                                
                                
```

**Rank 5**

```text
                                
                                
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@  
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@  
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@  
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@  
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@  
    @@@@          .    .        
    @@@@          .    .        
    @@@@        . #@@@@# .      
    @@@@       .@@@@@@@@@@.     
    @@@@        #@*....*@#      
    @@@@       #@*.    .*@#     
    @@@@       @#.      .#@     
    @@@@       @#.      .#@     
    @@@@       @#.      .#@     
    @@@@       @#.      .#@     
    @@@@       #@*.    .*@#     
    @@@@        #@*....*@#      
    @@@@       .@@@@@@@@@@.     
    @@@@        . #@@@@# .      
    @@@@          .    .        
                                
                                
```

**Original**

```text
                                
                                
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@  
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@  
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@  
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@  
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@  
    @@@@                        
    @@@@                        
    @@@@          @@@@@@        
    @@@@        @@@@@@@@@@      
    @@@@        @@@    @@@      
    @@@@       @@@      @@@     
    @@@@       @@        @@     
    @@@@       @@        @@     
    @@@@       @@        @@     
    @@@@       @@        @@     
    @@@@       @@@      @@@     
    @@@@        @@@    @@@      
    @@@@        @@@@@@@@@@      
    @@@@          @@@@@@        
    @@@@                        
                                
                                
```

**Rank 1 is a smear**: one row pattern times one column pattern, so every row is a multiple of every other. **Rank 2 has the bar and the post** and a ghost of the ring. **Rank 5 is nearly the picture**, at $37\%$ of the storage.

### Where the rank comes from

**Each shape on its own** (`svd.py` §10):

| Shape | Numerical rank |
|---|---:|
| the bar | $1$ |
| the post | $1$ |
| bar and post together | $2$ |
| **the ring** | **$5$** |

**$2 + 5 = 7$.** A rectangle aligned with the pixel grid is one row pattern times one column pattern — rank $1$ by definition. **A ring is not a product of a row and a column**, and curves are what low rank is worst at.

> **This is why real image compression is not just a truncated SVD.** JPEG first changes basis to
> cosines on small blocks — **Week 12's Fourier item** — where natural images are nearly sparse,
> and then throws away small coordinates. **Both are the same idea: find the basis in which most
> coordinates are small, and keep the large ones.** The SVD finds the best such basis for one
> matrix; the cosine basis is a fixed one that is good for all photographs at once.

---

## 4. Using It Without Decompressing

**Week 1's L04 measured a speedup of $787\times$** from computing $A(BC)$ instead of $(AB)C$ when $A$ and $B$ were thin factors of a $1000\times1000$ matrix of rank $2$ — and said: *Week 11 explains why any matrix can be approximated this way. Week 1 is why it pays.*

**This is the other half.** If $A \approx A_k = U_k\Sigma_kV_k^\mathsf{T}$, then

$$A_kx = U_k\bigl(\Sigma_k(V_k^\mathsf{T}x)\bigr)$$

costs $k(m + n)$ operations instead of $mn$, **and the $m\times n$ matrix is never formed.**

> **Where this is used, now that you can say why it works:** a recommender stores a users-by-items
> rating matrix as two thin factors and scores a user against a million items without building the
> table; LoRA fine-tunes a large language model by learning a rank-8 correction $U_kV_k^\mathsf{T}$
> to a weight matrix instead of the matrix itself; latent semantic analysis compresses a
> terms-by-documents matrix. **In every case the claim being made is Eckart–Young: that the discarded
> singular values were small.**

---

## 5. Total Least Squares

**Week 9's L29 §6 listed an assumption and deferred its failure to this week:** least squares assumes **all the error is in $b$**, none in $A$. When both coordinates are measured, that is false, and it matters.

`svd.py` §11 generates $40$ points near $y = 2x$ with noise of the same size in **both** coordinates, and fits three ways:

| Method | Slope |
|---|---:|
| regress $y$ on $x$ (Week 9 — vertical distances) | $1.723358$ |
| regress $x$ on $y$, then invert (horizontal distances) | $1.924916$ |
| **total least squares — perpendicular distances** | **$1.877326$** |

**The two ordinary fits disagree by more than $10\%$**, because each one pretends the other coordinate is exact. **Total least squares minimises perpendicular distance, treating both coordinates symmetrically**, and lands between them.

**The SVD computes it in one step.** Centre the points (subtract the centroid), put them in an $N\times2$ matrix $D$, and take its SVD. **The best line through the centroid runs along $v_1$; its normal is $v_2$; and the sum of squared perpendicular distances is $\sigma_2^2$:**

$$\sum_i(\text{perpendicular distance})^2 = 11.458429 = \sigma_2^2.$$

> **That is §1 at rank $1$.** Fitting a line through the centroid is approximating the centred data
> by a rank-one matrix, and Eckart–Young says $v_1$ is the best direction. **Week 12's PCA is exactly
> this in more dimensions** — the best $k$-dimensional subspace through the centroid of a cloud of
> points, found by keeping $k$ singular vectors.

---

## 6. Week 9's Table, Completed

**Week 9's L28 §4 compared methods on Läuchli's matrix** and found that only Householder QR survived. **The SVD survives too** (`svd.py` §12; $b = (1,0,0)$, exact $x_1 = 1/(2 + \varepsilon^2)$):

| $\varepsilon$ | normal equations | Householder QR | **SVD** | exact |
|---:|---|---:|---:|---:|
| $10^{-3}$ | $0.499999750$ | $0.499999750$ | $0.499999750$ | $0.499999750$ |
| $10^{-5}$ | $0.500000000$ | $0.500000000$ | $0.500000000$ | $0.500000000$ |
| $10^{-7}$ | $0.500000000$ | $0.500000000$ | $0.500000000$ | $0.500000000$ |
| $10^{-8}$ | **FAILED** | $0.500000000$ | $0.500000000$ | $0.500000000$ |
| $10^{-10}$ | **FAILED** | $0.500000000$ | $0.500000000$ | $0.500000000$ |

**And the SVD handles the case Householder cannot**: exactly dependent columns, where $R$ has a zero on its diagonal and back substitution divides by it. L34 §4 is that case.

**The cost.** Counting multiply-adds on a random $40\times40$:

| | operations |
|---|---:|
| elimination (Week 0's count) | $\approx 42{,}666$ |
| one-sided Jacobi SVD, as run | $\approx 1{,}829{,}600$ — **$42.9\times$** |

**Jacobi is the simplest SVD to write, not the fastest**; LAPACK's Golub–Kahan algorithm is considerably cheaper (Trefethen & Bau, Lecture 31) and is still a large multiple of elimination. **The most informative factorisation is the most expensive, which is why Week 9 did not start here** — and why `numpy.linalg.lstsq` uses the SVD by default anyway, when robustness matters more than speed.

---

## 7. The Spine of the Course, Complete

**Week 0's syllabus called the course one question asked five times: *when can I replace $A$ by something simpler?*** The five answers are now all on the table:

| Week | Factorisation | Exists when | Middle factor | Outer factors | Used for |
|---|---|---|---|---|---|
| 1 | $A = LU$ | elimination needs no row exchanges (else $PA = LU$) | — | triangular | solving $Ax = b$ |
| 7 | $A = S\Lambda S^{-1}$ | $n$ independent eigenvectors | diagonal | **any** invertible $S$ | powers, dynamics |
| 9 | $A = QR$ | independent columns | — | orthogonal, triangular | least squares |
| 10 | $A = Q\Lambda Q^\mathsf{T}$ | $A$ symmetric | real diagonal | orthogonal | quadratic forms, energy |
| **11** | $A = U\Sigma V^\mathsf{T}$ | **always** | **non-negative diagonal** | **orthogonal, two of them** | rank, norms, pseudoinverse, approximation |

**Read the "exists when" column downwards and the hypotheses fall away**; read the "outer factors" column and they become orthogonal. **Those are the same fact.** Orthogonal factors have condition number $1$, and every factorisation that is safe in floating point is one that uses them.

---

## 8. What to Take Away

1. **$A_k = \sum_{j\le k}\sigma_ju_jv_j^\mathsf{T}$ is the best rank-$k$ approximation**, in both the 2-norm and the Frobenius norm. **Stopping early is optimal.**
2. **The error is what was thrown away:** $\sigma_{k+1}$, or $\sqrt{\sum_{j>k}\sigma_j^2}$.
3. **$\sigma_{k+1}$ is the distance to the nearest rank-$k$ matrix**, which is why a gap in the singular values is a rank.
4. **Compression stores $k(m+n+1)$ numbers.** Straight edges aligned with the grid are cheap; curves are not.
5. **Low rank pays twice**: in storage, and in never forming the product (Week 1's $787\times$).
6. **Total least squares** fits perpendicularly, via the smallest singular vector of the centred data — and is the first appearance of PCA.
7. **The SVD survives everything Week 9's methods failed on, and costs the most.**
8. **Five factorisations, one direction of travel**: fewer hypotheses, more orthogonality.

---

## Exercises

*(Not assessed. PS 11 is the assessed work.)*

1. $A$ has singular values $10, 6, 3, 1$. Give $\lVert A - A_1\rVert_2$, $\lVert A - A_2\rVert_F$, and the energy kept at $k = 2$.
2. **A $1000\times800$ image has singular values that decay like $\sigma_j = 100/j$.** How many terms keep $99\%$ of the energy? How much storage is that, against the full image? *(Estimate the sum by an integral.)*
3. Show that $\lVert A - A_k\rVert_2 = \sigma_{k+1}$ **by writing $A - A_k$ in SVD form.** Which part of Eckart–Young does that prove, and which part does it not?
4. Draw a $5\times5$ image of a plus sign. **What is its rank?** A diagonal line? A filled square rotated by $45°$?
5. Four points $(-1,-2)$, $(0,0)$, $(1,2)$, $(0,1)$. Fit a line by ordinary least squares and by total least squares. **Which point makes them disagree, and why?**
6. **Why does total least squares need the data centred first?** What does the rank-one approximation of *uncentred* data find instead?
7. In §6's table, the normal equations give correct answers at $\varepsilon = 10^{-7}$. **Using L34 §2's table, say why that is luck** — Week 9's word — and what the computed $\sigma_\min(A^\mathsf{T}A)$ there tells you.
8. **Add $QR$ with column pivoting to §7's table.** When does it exist, and what does it offer that plain $QR$ does not? *(Look it up; it is the rank-revealing factorisation that sits between $QR$ and the SVD.)*

---

*MATH 241 · Week 11 · L35 · © CSE Department*
