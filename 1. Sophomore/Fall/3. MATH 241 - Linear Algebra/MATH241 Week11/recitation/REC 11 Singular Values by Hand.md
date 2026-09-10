# MATH 241 · Recitation 11
## Singular Values by Hand
### Covers Week 11 · sat **Thursday of Week 12**, 15:00–15:50, SSB 108 · **unmarked, attendance required**

---

> **This recitation covers Week 11 and is sat in Week 12**, after Thanksgiving recess.
>
> **PS 11 and PS 12 are both due at 17:00 tomorrow.** Bring PS 11; PS 12 is short and is final
> preparation.
>
> **Recitation 12, next Thursday in the completion period, is the final review.** This is the last
> recitation with new mathematics in it.

**What this session is.** Fifty minutes computing SVDs on paper, on matrices small enough to finish. **Week 11 is the week most students understand in lectures and cannot do on an exam**, because the construction has four steps and it is easy to lose the thread after two. The cure is doing it three times.

**What to bring:** paper, your PS 11 attempt, one laptop per pair for §4.

---

## 0. Before You Come (10 minutes, at home)

For

$$R = \begin{bmatrix}5&-12\\ 12&-12\end{bmatrix},$$

**compute $R^\mathsf{T}R$ and its two eigenvalues.**

*(They are perfect squares. If yours are not, recheck the off-diagonal entry of $R^\mathsf{T}R$ — it is the dot product of the two columns of $R$, and the sign is where people slip.)*

---

## 1. The Drill: Four Steps (10 min)

**In pairs, compare.** Expect $R^\mathsf{T}R = \begin{bmatrix}169&-204\\-204&288\end{bmatrix}$ with eigenvalues $441$ and $16$.

**(a) [step 1]** $\sigma_1 = \ ?$ and $\sigma_2 = \ ?$ **Check two ways**: $\sigma_1\sigma_2 = \lvert\det R\rvert$, and $\sigma_1^2 + \sigma_2^2$ equals the sum of the squares of all four entries.

**(b) [step 2]** Find unit eigenvectors $v_1, v_2$ of $R^\mathsf{T}R$. **They have entries in fifths.**

**(c) [step 3]** Compute $u_k = Rv_k/\sigma_k$. **Check $u_1\perp u_2$** — and say which week's theorem made that automatic.

**(d) [step 4]** Write $R = U\Sigma V^\mathsf{T}$ and **multiply it back out** for the $(1,1)$ entry only.

> **The trap in step 3.** Students compute $u_k$ as an eigenvector of $RR^\mathsf{T}$ *independently*
> and get the sign wrong half the time. **$u_k = Rv_k/\sigma_k$ fixes the sign for you**, and an
> independent eigenvector does not. On an exam, derive $U$ from $V$.

---

## 2. Eigenvalues Are Not Singular Values (10 min)

**(a)** Find the eigenvalues of $R$. *(Trace $-7$, determinant $84$.)* **What kind of numbers are they, and which week told you to expect that?**

**(b)** $R$ has **complex** eigenvalues and **real, positive** singular values $21$ and $4$. **Say in one sentence why a singular value can never be complex**, using L33 §2.

**(c)** Compute $\lvert\lambda\rvert$ for each eigenvalue. **Where does it sit relative to $\sigma_2 = 4$ and $\sigma_1 = 21$?** Then prove that $\sigma_\min \le \lvert\lambda\rvert \le \sigma_\max$ for **every** eigenvalue of **every** square matrix. *(Take $Ax = \lambda x$ and compare $\lVert Ax\rVert$ with what L33 §4 says $A$ can do to a unit vector.)*

**(d)** $\det U = \det V = +1$ here. **So $R$ is a rotation, a stretch, and a rotation.** By how many degrees does each rotation turn? *(Read the angles off $U$ and $V$ — each is a $(3,4,5)$ triangle.)*

---

## 3. Rank One, and Its Pseudoinverse (10 min)

$$K = \begin{bmatrix}8&-6\\ 4&-3\\ -8&6\end{bmatrix}$$

**(a)** Write $K$ as a column times a row. **Read off $\sigma_1$, $u_1$ and $v_1$ without computing $K^\mathsf{T}K$.** What is $\sigma_2$?

**(b)** For a rank-one matrix $A = \sigma uv^\mathsf{T}$, show that $A^+ = A^\mathsf{T}/\sigma^2$. **Then write $K^+$.**

**(c)** Solve $Kx \approx b$ in the least-squares sense for $b = (1,1,1)$, **taking the shortest solution**. Give $x^+$, the projection $p = Kx^+$, and check that $p$ is the projection of $b$ onto the line through $u_1$ **computed the Week 8 way**.

**(d)** **Every $x = x^+ + t\,(3,4)$ fits equally well.** Why $(3,4)$? And why is $t = 0$ the shortest?

---

## 4. Ten Minutes With a Machine (10 min)

One laptop per pair. Run `resources/svd.py` from the Week 11 folder.

**(a)** In **§9**, the competitor that comes closest to beating $A_2$ is **$A_2$ itself with its factors nudged by $1\%$**, and it still loses — $16.048962$ against $16.047980$. **Say why no competitor can get below $16.047980$**, naming the singular value.

**(b)** In **§5's Läuchli table**, at $\varepsilon = 10^{-7}$ the computed $\sigma_\min(A^\mathsf{T}A)$ is $1.005\times10^{-14}$. **What should it be, and which digit is wrong?** Why does the error appear in $A^\mathsf{T}A$ and not in $A$?

**(c)** In **§12**, the SVD costs $42.9\times$ elimination as run. **Name one situation where you would pay that anyway**, from this week's lectures.

> **Do not open PS 11 Q4 on the machine in this session.** It asks you to predict before you
> measure, and the prediction is the marks.

---

## 5. Clinic (whatever is left)

**Bring:** the PS 11 question you are stuck on.

**Priorities, in order:**

1. **PS 11 Q1** — the four steps on a wide matrix. **Do it through $WW^\mathsf{T}$**, the smaller product.
2. **PS 11 Q2** — the four subspaces from the SVD. §3 of this sheet is the rank-one version.
3. **PS 11 Q5(c)** — the Eckart–Young dimension argument. Trefethen & Bau Lecture 5 is allowed.

> **Next Thursday is Recitation 12, the final review**, in the completion period. **Bring the one
> topic from Weeks 0–11 that you would least like to see on the paper.** The final is Monday Dec 15,
> 09:00–11:30.

---

*MATH 241 · Week 11 · REC 11 · unmarked*
