# MATH 241 · Recitation 2
## Two Spaces, and Which One Elimination Moves
### Covers Week 2 · sat **Thursday of Week 3**, 15:00–15:50, SSB 108 · **unmarked, attendance required**

---

> **This recitation covers Week 2 and is sat in Week 3.** Recitation *N* covers Week *N* and is sat
> on the Thursday of Week *N+1*.
>
> **PS 2 is due at 17:00 tomorrow.** Come with your attempt.

**What this session is.** Fifty minutes at the board on the two things Week 2 is assessed on: **saying which space a subspace lives in**, and **knowing which of $\mathbf{C}$ and $\mathbf{N}$ elimination preserves.** The numbers below are not PS 2's.

**What to bring:** paper, your PS 2 attempt, one laptop per pair for §4.

---

## 0. Before You Come (10 minutes, at home)

For

$$M = \begin{bmatrix}2 & 4 & 1 & 3\\ 1 & 2 & 0 & 1\\ 3 & 6 & 2 & 5\end{bmatrix}$$

compute $\operatorname{rref}(M)$ and bring it, along with the pivot columns and the rank. **Do not go further** — the session does the rest, and starting from a shared echelon form is what makes fifty minutes enough.

---

## 1. Which $\mathbb{R}^k$? (10 min)

**In pairs, out loud, no writing for the first two minutes.** For the $M$ above:

**(a)** $\mathbf{C}(M)$ is a subspace of which space? $\mathbf{N}(M)$? **Say the two numbers before you look at anything.**

**(b)** What is the largest $\mathbf{C}(M)$ could possibly be? The largest $\mathbf{N}(M)$ could be? Answer from the shape of $M$ alone.

**(c)** Now use your rank. Give the dimension of each, and check they add to something — **which something, and why that one and not the other?** *(rank + nullity $= n$, and $n$ is the number of columns. Students reliably add to $m$.)*

**(d)** $M$ has four columns living in $\mathbb{R}^3$. **Without any computation, how do you know $\mathbf{N}(M) \ne \{0\}$?**

> **The sentence to leave §1 with:** the column space is where $b$ lives and the null space is where
> $x$ lives, and for a rectangular matrix those are different rooms. **Every mark lost on PS 2 Q3(a)
> is this sentence.**

---

## 2. The One That Moves (15 min)

**This is the section. Do not skip to §3 if it runs long.**

**(a)** Write down $\mathbf{C}(M)$ as a span, taken from the columns **of $M$**. Then write down $\mathbf{C}(\operatorname{rref} M)$ as a span, from the columns of the rref.

**(b)** Find the equation of each — one linear condition on $(b_1,b_2,b_3)$ apiece.

**(c)** **Are they the same plane?** Find a vector in one and not the other, and *verify it against both equations.* **Some obvious candidates lie in both** — $(1,2,0)$ does — so a guess is not an answer until it has been checked against each.

**(d)** Now the other space. Compute $\mathbf{N}(M)$ and $\mathbf{N}(\operatorname{rref} M)$. **Are those the same?** They are — say why in one sentence, using the word *invertible*.

**(e)** **The question to argue as a pair.** Row operations preserve one of the two spaces and move the other. **Both spaces are built out of the same nine numbers.** So what exactly is it that a row operation does to a matrix, such that one survives and the other does not?

> *(The answer to reach: a row operation mixes entries **within each column**, so it moves every
> column and therefore the space they span. It does not touch $x$, and the null space is a statement
> about which $x$ kill the matrix — that is, about the **relations among the columns**, which is
> exactly what elimination is designed to expose. Relations survive; positions do not.)*

---

## 3. Complete Solutions at Speed (10 min)

**(a)** $Mx = (3, 1, 5)$. **Before eliminating:** is it solvable? Answer from §2(b) in five seconds. *(There is also a one-line answer visible in the columns. Either is fine; say which you used.)*

**(b)** Solve it completely. One particular solution plus the null space.

**(c)** Your partner will have a different $x_p$ from yours, or should. **Show that your two answers describe the same set** — find the $t, u$ that turn theirs into yours.

**(d)** $Mx = (3, 1, 6)$. Solvable? Which single arithmetic operation settles it?

---

## 4. Ten Minutes With a Machine (10 min)

```bash
python3 resources/spaces.py
```

**(a)** Find the "row operations CHANGE the column space" block. Confirm it says what your §2(c) found, on a different matrix.

**(b)** Find the subspace table at the end. **Two rows fail for opposite reasons** — one is closed under addition but not scaling, the other under scaling but not addition. Identify both, and give the specific vectors. *(This is PS 2 Q1(a) rows 3 and 4.)*

**(c)** The last row says the invertible $3\times3$ matrices are not a subspace, because $I + (-I) = 0$. **Give a second reason** — a condition from L07 §4 that the invertible matrices also fail, independently of that one.

**(d)** *(If you finish early.)* Edit the matrix at the top of the script to your $M$ and re-run. Does the printed rank, nullity and special-solution list match what you did by hand?

---

## 5. Clinic (whatever is left)

**The three that come up every year:**

- **Q2(b), which columns.** If §2 landed this is done. The rref tells you *which positions*; the vectors come from $B$.
- **Q4(d), "is one of us wrong".** §3(c) of this sheet is that question with different numbers. If §3(c) landed, answer Q4(d) from it.
- **Q5(c), $\mathbf{N}(A^\mathsf{T}A) = \mathbf{N}(A)$.** The unstick is one line: *multiply $A^\mathsf{T}Ax = 0$ on the left by $x^\mathsf{T}$ and ask what the resulting scalar is.* Ask for that hint and no more.

> **What not to ask for.** "Is my null space right?" — multiply $A$ by each special solution and see.
> That check is exact and takes a minute.

---

*MATH 241 · Week 2 · Recitation 2 · sat Thursday of Week 3 · unmarked*
