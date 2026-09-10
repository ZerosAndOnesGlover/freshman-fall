# MATH 241 · Recitation 3
## Four Subspaces on One Matrix
### Covers Week 3 · sat **Thursday of Week 4**, 15:00–15:50, SSB 108 · **unmarked, attendance required**

---

> **This recitation covers Week 3 and is sat in Week 4.**
>
> **PS 3 is due at 17:00 tomorrow.** Come with your attempt.

**What this session is.** Fifty minutes producing **all four subspaces of one matrix**, with the correct ambient space and dimension for each, and checking the two facts that make them a theorem: the dimensions add up and the pairs are orthogonal. **This is PS 3 Q3 with a different matrix, and it is the single most mechanical thing Week 3 asks of you** — the recitation exists so that you have done it once under supervision.

**What to bring:** paper, your PS 3 attempt, one laptop per pair for §4.

---

## 0. Before You Come (10 minutes, at home)

For

$$M = \begin{bmatrix}1 & 2 & 1 & 4\\ 2 & 4 & 3 & 9\\ 3 & 6 & 4 & 13\end{bmatrix}$$

compute $\operatorname{rref}(M)$ and bring it, with the pivot columns and the rank. **Stop there.**

---

## 1. The Table, Filled In (15 min)

**In pairs, at the board.** Build this table for $M$. **Fill the "lives in" column first, before computing any basis** — it takes five seconds and it is where the marks are.

| Subspace | Lives in | $\dim$ | Basis |
|---|---|---|---|
| $\mathbf{C}(M)$ | | | |
| $\mathbf{N}(M)$ | | | |
| $\mathbf{C}(M^\mathsf{T})$ | | | |
| $\mathbf{N}(M^\mathsf{T})$ | | | |

**As you go, say out loud which recipe each basis uses and why:**

- **$\mathbf{C}(M)$** — pivot columns of **$M$**. *Why not of $\operatorname{rref}(M)$?*
- **$\mathbf{C}(M^\mathsf{T})$** — nonzero rows of **$\operatorname{rref}(M)$**. *Why is that allowed here when the analogous move was forbidden above?*

**$\mathbf{N}(M^\mathsf{T})$ is the one you have not practised.** Transpose $M$ — it becomes $4\times3$ — and run the same special-solution algorithm. *It has dimension $m - r$; work out what that is before you compute it, and use it to check your answer.*

---

## 2. The Two Sums, and the Ten Dot Products (10 min)

**(a)** Check $r + (n-r) = n$ and $r + (m-r) = m$ with your numbers. **Which sum lives in which space?**

**(b)** Compute every dot product between a basis vector of $\mathbf{N}(M)$ and a basis vector of the row space. **How many is that?** Then every one between $\mathbf{N}(M^\mathsf{T})$ and $\mathbf{C}(M)$.

**(c)** They are all zero. **Explain the first family in one sentence**, using the fact that the $i$-th entry of $Mx$ is *(row $i$) $\cdot\ x$*.

**(d)** **The question to argue as a pair.** You have four subspaces, two in $\mathbb{R}^3$ and two in $\mathbb{R}^4$. In each space the two dimensions add to the whole. **Does that, by itself, prove the two subspaces fill the space between them?** Answer carefully.

> *(No. Two lines through the origin in $\mathbb{R}^3$ have dimensions summing to 2, and they fill
> nothing but a plane at best — or a line, if they coincide. **Dimensions adding up is necessary and
> not sufficient; orthogonality is what makes it work**, and that is exactly what Week 8 supplies.
> A pair that gets this has understood why L12 §7 is a preview and not a proof.)*

---

## 3. Solvability Without Elimination (10 min)

**(a)** $\dim\mathbf{N}(M^\mathsf{T})$ tells you how many independent conditions $Mx = b$ imposes on $b$. **How many, and what are they?** Write them as equations in $b_1, b_2, b_3$.

**(b)** Use them — **no elimination** — on $b = (8, 18, 26)$ and $b = (8, 18, 27)$.

**(c)** For the solvable one, give the complete solution. Check $x_p$ against $M$.

**(d)** Your condition from (a) is the equation of a plane in $\mathbb{R}^3$. **Which of the four subspaces is that plane?** Say how you know.

---

## 4. Ten Minutes With a Machine (10 min)

```bash
python3 resources/dimension.py
```

**(a)** The script does all of §1 for the lectures' matrix. **Compare its four bases with yours for $M$** — same shapes, different numbers. Check that the dimension pattern $r,\ n-r,\ r,\ m-r$ holds for both.

**(b)** Find the block showing the left null space is Week 2's plane equation. **Your §3(a) is the same fact for $M$.** Say the sentence out loud: *the coefficients of the solvability condition are a basis for the left null space.*

**(c)** Find the block showing every row of $A$ rebuilt from the rref's rows. **Do the same by hand for your $M$** — three rows, each a combination of two.

**(d)** *(If you finish early.)* Change one entry of the script's matrix so the rank becomes 3. **Which dimensions change, and by how much?** Predict before you run it.

---

## 5. Clinic (whatever is left)

**The three that come up every year:**

- **Q3(b), which recipe.** If §1 landed this is done.
- **Q4(a), how many conditions.** It is $m - r$, and §3(a) is the same question. **Count the zero rows of your rref as a check** — there should be exactly that many.
- **Q5(c), $\operatorname{rank}(AB) \le \min$.** The unstick is one word: **transpose**. You have the first half from PS 2; apply it to $B^\mathsf{T}A^\mathsf{T}$ for the second. Ask for that and no more.

> **What not to ask for.** "Is my left null space right?" — multiply $y^\mathsf{T}M$ and see whether
> you get a row of zeros. Exact, and it takes a minute.

---

*MATH 241 · Week 3 · Recitation 3 · sat Thursday of Week 4 · unmarked*
