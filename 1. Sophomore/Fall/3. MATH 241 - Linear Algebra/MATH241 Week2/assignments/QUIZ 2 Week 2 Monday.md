# MATH 241 · Quiz 2
## Administered: Monday, Week 2 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 1** — matrix multiplication, the inverse, transposes, and $A = LU$.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.
>
> Do not look at the key first. It costs you the only thing the exercise is for.

---

**Q1.** Matrix multiplication is defined by $(AB)_{ij} = \sum_k a_{ik}b_{kj}$. What requirement forces that formula, rather than the entrywise product?

&nbsp;

&nbsp;

---

**Q2.** Compute $AB$ for $A = \begin{bmatrix}1&2\\0&3\end{bmatrix}$, $B = \begin{bmatrix}4&1\\2&5\end{bmatrix}$ — **by columns**, showing each column of $AB$ as a combination of the columns of $A$.

&nbsp;

&nbsp;

---

**Q3.** Expand $(A+B)^2$. Under exactly what condition does it equal $A^2 + 2AB + B^2$?

&nbsp;

&nbsp;

---

**Q4.** You have factored $A = LU$ for a $1000\times1000$ matrix. A new right-hand side $b$ arrives. Roughly how many operations to solve $Ax = b$ — and how many if you had not kept the factors?

&nbsp;

&nbsp;

---

**Q5.** $A$ is $1000\times2$, $B$ is $2\times1000$, $C$ is $1000\times1$. Which is cheaper, $(AB)C$ or $A(BC)$, and roughly by what factor?

&nbsp;

&nbsp;

---

**Q6.** Give **two** reasons not to compute $A^{-1}$ in order to solve $Ax = b$.

&nbsp;

&nbsp;

---

**Q7.** In $A = LU$, where do the entries of $L$ come from? And what changes when a row exchange is needed?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** That $AB$ should **be the composite function** — $(AB)x = A(Bx)$ for every $x$. Working out what that forces gives the formula, and forces the shape rule too: $A$'s column count must equal $B$'s row count, or "first $B$, then $A$" is not a composition at all. *(L04 §1. The entrywise Hadamard product corresponds to no composition of anything, which is why nobody uses it.)*

---

**Q2.** $AB = \begin{bmatrix}8&11\\6&15\end{bmatrix}$, and by columns:

$$Ab_1 = 4\begin{bmatrix}1\\0\end{bmatrix} + 2\begin{bmatrix}2\\3\end{bmatrix} = \begin{bmatrix}8\\6\end{bmatrix}, \qquad Ab_2 = 1\begin{bmatrix}1\\0\end{bmatrix} + 5\begin{bmatrix}2\\3\end{bmatrix} = \begin{bmatrix}11\\15\end{bmatrix}$$

*If you computed four dot products you got the right number by the reading this course is trying to displace. **This week's L08 is built on the column reading** — the answer to "which $b$ are reachable" is unreadable through dot products.*

---

**Q3.** $(A+B)^2 = A^2 + AB + BA + B^2$. It equals $A^2 + 2AB + B^2$ **if and only if $AB = BA$** — the two sides differ by exactly $AB - BA$. *(L04 §3. "If and only if", not "if": commuting is the precise condition.)*

---

**Q4.** **About $2n^2 = 2\times10^6$** — a forward substitution through $L$ and a back substitution through $U$, each $n^2$.

Without the factors: **$n^3/3 \approx 3.3\times10^8$**, a fresh elimination. **A factor of about 170.** *(L06 §5.)*

---

**Q5.** **$A(BC)$**, by about **750×** — $8{,}000$ flops against $6{,}000{,}000$ — and it never forms the $1000\times1000$, 8 MB intermediate that $(AB)C$ does. Measured at 787×. *(L04 §5. The rule is: form the intermediate with the fewest entries — **not** "associate to the right", which gets Week 1's other example backwards.)*

---

**Q6.** Any two of:

- **Cost.** Gauss–Jordan is $\approx 2n^3$ against $LU$'s $n^3/3$ — six times the work — and both then cost $2n^2$ per solve, so the extra buys nothing.
- **Accuracy.** Measured worse at every $n$ on Hilbert systems, by an unpredictable factor of 2 to 91.
- **Sparsity.** The inverse of a sparse matrix is dense: the tridiagonal $K$ has 13 nonzeros and $K^{-1}$ has 25, and at $n = 10^6$ that is 8 terabytes against 32 megabytes of band.

*(L05 §6–§7. The third is the one that stops people in practice.)*

---

**Q7.** **$L$'s entries are the multipliers, transcribed** — $\ell_{ik}$ goes in position $(i,k)$, with ones on the diagonal. **Nothing is computed**; they were already on the page from the elimination.

With a row exchange, $A = LU$ fails and you get **$PA = LU$** instead: the permutation is applied to the *original* matrix, and $P^{-1} = P^\mathsf{T}$. *(L06 §4, §6.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1 | L04 §1 |
| **Q2** | **L04 §2, reading (ii)** — and redo it before Tuesday. **This week depends on it** |
| Q3 | L04 §3 |
| Q4, Q5 | L06 §5 and L04 §5 |
| Q6 | L05 §6–§7 |
| **Q7** | **L06 §4** — $L$ is transcription. If you calculated something, find out what |

**Q2 is the one that matters this week.** L08 defines the column space as the span of the columns and asks which $b$ it reaches; a student still reading $Ax$ as a stack of dot products will find Weeks 2 and 3 opaque and will not be able to say why. **Fix it now, not before the midterm.**

---

*MATH 241 · Week 2 · Quiz 2 · covers Week 1 · ungraded*
