# MATH 241 · Linear Algebra
## Week 1 · Lecture 1 of 3 · **Monday**
### Matrix Multiplication, Four Ways

---

**Reading:** Strang §2.4, and §2.3 properly this time · **Previous:** Week 0's L03, cost and conditioning · **Next:** L05, the inverse

> **Quiz 1 is the first ten minutes of this lecture** and covers Week 0. Answer key printed in the
> paper; mark it yourself before you leave.
>
> **Every number in this lecture was computed by `resources/matrices.py`**, which ships with this
> week. Run it.

---

## 1. The Definition, and Why It Looks Arbitrary

If $A$ is $m \times n$ and $B$ is $n \times p$, then $AB$ is $m \times p$ with entries

$$(AB)_{ij} = \sum_{k=1}^{n} a_{ik}b_{kj}.$$

**Row $i$ of $A$, dotted with column $j$ of $B$.** Every student meets this and every student has the same reaction: *why that?* Adding matrices is entrywise; multiplying them is not, and there is an entrywise product — it is called the Hadamard product, it is written $A \circ B$, and outside a few corners of machine learning nobody uses it.

**The answer is that matrix multiplication is not defined at all. It is derived, and only one definition is possible.**

A matrix is a function. $A$ takes a vector in $\mathbb{R}^n$ to a vector in $\mathbb{R}^m$. If $B$ takes $\mathbb{R}^p$ to $\mathbb{R}^n$, then **"first $B$, then $A$" is a function from $\mathbb{R}^p$ to $\mathbb{R}^m$**, and we want $AB$ to *be* that function:

$$(AB)x = A(Bx) \qquad \text{for every } x.$$

Work out what that forces. Column $j$ of any matrix $M$ is $Me_j$, where $e_j$ is the $j$-th standard basis vector. So column $j$ of $AB$ is

$$(AB)e_j = A(Be_j) = A(\text{column } j \text{ of } B) = \sum_k b_{kj}\,a_k$$

using L01's rule that $Av$ is a combination of $A$'s columns with the entries of $v$ as amounts. Reading off row $i$ of that gives $\sum_k a_{ik}b_{kj}$. **The formula, forced, with no choices made.**

> **This is why the shapes have to match.** $AB$ requires $A$'s column count to equal $B$'s row count
> because otherwise "first $B$, then $A$" is not a composition — $B$'s output does not live where
> $A$'s input does. **The shape rule is not bookkeeping; it is the statement that a composition
> exists.**
>
> And it explains the Hadamard product's obscurity: it corresponds to no composition of anything.

---

## 2. Four Ways to Read $AB$, All the Same Number

The formula is one reading. Here are four, and **fluency means switching between them without noticing.** Different proofs and different algorithms want different ones, and using the wrong one is why some results in Weeks 8–11 look like magic.

Let $A$ be $m\times n$ with columns $a_1,\dots,a_n$ and rows $\alpha_1^\mathsf{T},\dots,\alpha_m^\mathsf{T}$; let $B$ be $n\times p$ with columns $b_1,\dots,b_p$ and rows $\beta_1^\mathsf{T},\dots,\beta_n^\mathsf{T}$.

### (i) Entry by entry — dot products

$$(AB)_{ij} = \alpha_i^\mathsf{T} b_j$$

*Use it for:* computing one entry, and for hand arithmetic. **Almost nothing else.**

### (ii) Column by column

$$AB = \bigl[\;Ab_1 \;\big|\; Ab_2 \;\big|\; \cdots \;\big|\; Ab_p\;\bigr]$$

**Each column of $AB$ is $A$ applied to the corresponding column of $B$** — and by L01, each is a combination of $A$'s columns.

*Use it for:* **almost everything.** It is why $AB$'s columns can never leave $A$'s column space, which is the one-line proof of half a dozen results in Weeks 2 and 3. It is how you should read $AA^{-1} = I$ in L05, and it is L05's Gauss–Jordan algorithm in a sentence.

### (iii) Row by row

$$\text{row } i \text{ of } AB \;=\; \alpha_i^\mathsf{T}B \;=\; \sum_k a_{ik}\,\beta_k^\mathsf{T}$$

**Each row of $AB$ is a combination of the rows of $B$.**

*Use it for:* **row operations.** L02's $R_3 \leftarrow R_3 - 3R_2$ *is* left multiplication by a matrix, and this is the reading that makes it obvious. L06 is built on it.

### (iv) Column times row — the outer-product form

$$AB \;=\; \sum_{k=1}^{n} a_k\,\beta_k^\mathsf{T}$$

A column ($n\times1$) times a row ($1\times p$) is a **full $n \times p$ matrix**, of rank one, and $AB$ is a sum of $n$ of them.

*Use it for:* **everything in the second half of the course.** The SVD in Week 11 says every matrix is a sum of rank-one pieces $\sigma_k u_k v_k^\mathsf{T}$ ordered by importance; image compression is keeping the first twenty. **Reading (iv) as fluently as (i) is what makes Week 11 a computation instead of a mystery.** Meet it now.

> **Worth doing once, tonight.** Take $A = \begin{bmatrix}1&2\\3&4\end{bmatrix}$ and
> $B = \begin{bmatrix}5&6\\7&8\end{bmatrix}$ and compute $AB$ **four times**, once by each reading.
> Same $\begin{bmatrix}19&22\\43&50\end{bmatrix}$ each time. Twenty minutes, and it is the best
> twenty minutes you will spend this week.

---

## 3. What Is True, and the One Thing That Is Not

| | Holds? | |
|---|---|---|
| $A(BC) = (AB)C$ | **Yes** | Associative. Both are "do $C$, then $B$, then $A$" |
| $A(B+C) = AB + AC$ | **Yes** | Distributive, on both sides |
| $c(AB) = (cA)B = A(cB)$ | **Yes** | Scalars move freely |
| $AI = IA = A$ | **Yes** | $I$ is the identity function |
| $AB = BA$ | **No** | **Almost never** |
| $AB = 0 \Rightarrow A = 0$ or $B = 0$ | **No** | See below |
| $AB = AC,\ A \ne 0 \Rightarrow B = C$ | **No** | No cancellation. L05 says when there is |

**Associativity is free, because composition of functions is associative** — both sides describe applying $C$, then $B$, then $A$, and there was never a choice about what that means. §5 shows that "free" applies to the *answer* and emphatically not to the *cost*.

### Non-commutativity, in the smallest possible example

$$P = \begin{bmatrix}0&1\\0&0\end{bmatrix}, \qquad Q = \begin{bmatrix}0&0\\1&0\end{bmatrix}$$

$$PQ = \begin{bmatrix}1&0\\0&0\end{bmatrix}, \qquad QP = \begin{bmatrix}0&0\\0&1\end{bmatrix}$$

**Both products are diagonal, and they share no nonzero entry.** This is not a near miss; the two answers have disjoint supports.

**The same pair kills two more plausible rules.**

$$P^2 = \begin{bmatrix}0&0\\0&0\end{bmatrix}$$

**A nonzero matrix whose square is zero** — no nonzero *number* does that, and it is why $AB = 0$ tells you nothing about $A$ and $B$. And cancellation fails too: $P\,Q = P\,(Q + P)$, since $P^2 = 0$, while $Q \ne Q + P$. **From $AB = AC$ with $A \ne 0$ you may conclude nothing at all.**

**Why it is not commutative, in one sentence:** *putting on socks then shoes is not putting on shoes then socks.* Matrices are functions; composition of functions has an order; the order is the content.

> **The consequence that costs marks all term.** $(A+B)^2 = A^2 + AB + BA + B^2$, and **not**
> $A^2 + 2AB + B^2$. Similarly $(AB)^{-1} = B^{-1}A^{-1}$ (L05), and $(AB)^\mathsf{T} = B^\mathsf{T}A^\mathsf{T}$
> (L06) — **the order reverses**, and it reverses for the same reason
> both times: undoing a composition undoes the last step first.

---

## 4. Block Multiplication

Cut $A$ and $B$ into blocks. **If the cuts are compatible — $A$'s column cuts matching $B$'s row cuts — then blocks multiply exactly like entries:**

$$\begin{bmatrix}A_{11} & A_{12}\\ A_{21} & A_{22}\end{bmatrix}
\begin{bmatrix}B_{11} & B_{12}\\ B_{21} & B_{22}\end{bmatrix} =
\begin{bmatrix}A_{11}B_{11} + A_{12}B_{21} & A_{11}B_{12} + A_{12}B_{22}\\
A_{21}B_{11} + A_{22}B_{21} & A_{21}B_{12} + A_{22}B_{22}\end{bmatrix}$$

with the one caution that **the block products must be written in the right order**, since blocks do not commute either.

This is not a curiosity. It is:

- **Readings (ii), (iii) and (iv) as special cases** — cut $B$ into single columns and you have (ii); cut $A$ into single rows, (iii); cut $A$ into columns and $B$ into rows, (iv).
- **How matrix multiplication is actually implemented.** A cache-blocked `dgemm` multiplies $64\times64$ tiles because a tile fits in L1 and the full matrices do not. **CS 201 Week 6 is where that sentence gets its mechanism** — this is one of the two or three places the courses touch directly.
- **How proofs about structured matrices are written.** Weeks 7 and 11 both use it.

---

## 5. What It Costs, and Why the Brackets Are Worth Three Orders of Magnitude

$AB$ with $A$ $m\times n$ and $B$ $n \times p$ has $mp$ entries, each a dot product of length $n$: **$2mnp$ flops**, or $2n^3$ for square $n$.

| $n$ | Multiply $2n^3$ | Eliminate $n^3/3$ | Ratio |
|---:|---:|---:|---:|
| 100 | $2\times10^{6}$ | $3.3\times10^{5}$ | 6 |
| 1,000 | $2\times10^{9}$ | $3.3\times10^{8}$ | 6 |
| 10,000 | $2\times10^{12}$ | $3.3\times10^{11}$ | 6 |

**Multiplying two matrices is six times more expensive than solving a system with one.** That ratio is fixed, and it is the whole argument of L05 §6: if you find yourself computing $A^{-1}$ in order to multiply by it, you have chosen the expensive operation to do the cheap one's job.

### Associativity is free. The parenthesisation is not.

$A(BC)$ and $(AB)C$ give the same answer. They do not give it for the same price. Take $A$ of size $1000\times2$, $B$ of $2\times1000$, $C$ of $1000\times1$:

| | Flops | Largest intermediate |
|---|---:|---|
| $(AB)C$ | $2(1000)(2)(1000) + 2(1000)(1000)(1) = \mathbf{6{,}000{,}000}$ | $AB$ is $1000\times1000$ — **8 MB** |
| $A(BC)$ | $2(2)(1000)(1) + 2(1000)(2)(1) = \mathbf{8{,}000}$ | $BC$ is $2\times1$ — 16 bytes |

**A ratio of 750 to 1, from moving two brackets.** Measured in `matrices.py` on the reference machine:

```
measured: (AB)C 1.048 s   A(BC) 0.001331 s   speedup 787x
the two answers differ by at most 5.68e-14 -- rounding, not disagreement.
```

**787×, and the answers agree to thirteen decimal places.** The gap between 750 and 787 is memory traffic — the left-hand version writes and re-reads eight megabytes that the right-hand version never creates.

> **This is a real technique, not a puzzle.** $A$ and $B$ here are a **low-rank factorisation**: a
> $1000\times1000$ matrix of rank 2, stored as two thin factors. Never forming the product is how
> LoRA fine-tunes a large model by training a rank-8 correction; how a recommender scores a user
> against a million items; how Week 11's compressed image is *used* without being decompressed.
> **Week 11 explains why any matrix can be approximated this way. Week 1 is why it pays.**
>
> Choosing the cheapest bracketing of a chain $A_1A_2\cdots A_k$ is a classic dynamic-programming
> problem — CS 102 solved it in Year 1 as *matrix chain multiplication*, probably without saying
> what the $2mnp$ was. It was this.

### And $2n^3$ is not optimal

Strassen's algorithm multiplies $2\times2$ blocks with **seven** block multiplications instead of eight, and recursing gives $O(n^{\log_2 7}) = O(n^{2.807})$. It is used in practice above $n \approx 1000$. The theoretical record is near $O(n^{2.37})$ and is entirely impractical — the constants are astronomical. **Nobody knows the true exponent**, and whether it is $2$ is a genuinely open problem.

---

## 6. Powers, and the First Reason to Care About Eigenvalues

$A^k$ means $A$ applied $k$ times. Two facts, and the second is a signpost.

**Computing $A^k$ does not need $k$ multiplications.** Square repeatedly: $A^{16} = ((((A^2)^2)^2)^2)$ is four multiplications, not fifteen, and in general $O(\log k)$. *(You have done this before — it is modular exponentiation from CS 101, with matrices in place of integers.)*

**But $O(\log k)$ multiplications is still $O(n^3\log k)$ flops, and there is a better way for large $k$.** If $A$ has $n$ independent eigenvectors then $A = S\Lambda S^{-1}$ with $\Lambda$ diagonal, and

$$A^k = S\Lambda^k S^{-1}$$

— because every $S^{-1}S$ in the middle cancels — and $\Lambda^k$ is **$n$ scalar powers**. That is **Week 7**, and it is the reason Week 6 spends a week on eigenvectors before you have any use for them.

**Where you have already seen it:** Fibonacci. $\begin{bmatrix}F_{k+1}\\F_k\end{bmatrix} = \begin{bmatrix}1&1\\1&0\end{bmatrix}^k\begin{bmatrix}1\\0\end{bmatrix}$, and diagonalising that $2\times2$ produces the closed form with $\varphi = \frac{1+\sqrt5}{2}$ in it. **PageRank is the same computation on a $10^9 \times 10^9$ matrix**, which is why Week 0's L03 said it is not solved by elimination.

---

## 7. What to Take Away

1. **Matrix multiplication is derived, not chosen.** Requiring $(AB)x = A(Bx)$ forces the formula, and forces the shape rule.
2. **Four readings, one number:** entries, columns, rows, and outer products. **The column reading is the default; the outer-product reading is Week 11.**
3. **$AB \ne BA$**, there is no cancellation, and $AB = 0$ does not make either factor zero. $(A+B)^2$ has four terms.
4. **Block multiplication works**, provided the cuts match and you keep the order — and it is how the four readings and every fast implementation are unified.
5. **$2n^3$ against elimination's $n^3/3$: multiplying is six times dearer than solving.** Remember this for L05 §6.
6. **Associativity is free; the bracketing is not.** $750\times$ fewer flops and $787\times$ faster, measured, from one reassociation — and that is the low-rank trick the second half of the course is about.

---

## Exercises

*(Not assessed. PS 1 is the assessed work.)*

1. Compute $\begin{bmatrix}1&2\\3&4\end{bmatrix}\begin{bmatrix}5&6\\7&8\end{bmatrix}$ four times, once by each reading of §2. Confirm all four give $\begin{bmatrix}19&22\\43&50\end{bmatrix}$.
2. Find $2\times2$ matrices with $AB = 0$ but $A \ne 0$ and $B \ne 0$. Now find some with $AB = 0$ and $BA \ne 0$.
3. Prove that if $AB$ and $BA$ are both defined and $A$ is $m\times n$, then $B$ is $n\times m$. When are the two products the same *size*, and does that make them equal?
4. Expand $(A+B)^2$ and $(A+B)(A-B)$ without assuming commutativity. Under what condition does each collapse to the scalar answer?
5. $A$ is $200\times200$, $B$ is $200\times3$, $C$ is $3\times200$. Cost $(AB)C$ and $A(BC)$. Which wins, and by how much? **This time the left bracketing wins**, which is the opposite of §5 — say in one sentence what actually decides it, since it is evidently not "associate to the right".
6. Show that a product of upper-triangular matrices is upper triangular, using reading (iii). Then find the diagonal of the product in terms of the diagonals of the factors.

---

*MATH 241 · Week 1 · L04 · © CSE Department*
