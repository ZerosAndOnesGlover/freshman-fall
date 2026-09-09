# MATH 241 · Recitation 1
## Building $L$, and Never Inverting
### Covers Week 1 · sat **Thursday of Week 2**, 15:00–15:50, SSB 108 · **unmarked, attendance required**

---

> **This recitation covers Week 1 and is sat in Week 2.** Recitation *N* covers Week *N* and is sat
> on the Thursday of Week *N+1*, because this course's Thursday session falls before its Friday
> lecture. From here on it is every Thursday.
>
> **PS 1 is due at 17:00 tomorrow.** Come with your attempt.

**What this session is.** Fifty minutes at the board on the two things Week 1 is actually assessed on: **reading a product four ways**, and **producing $L$ without computing anything**. The numbers below are not PS 1's.

**What to bring:** paper, your PS 1 attempt, one laptop per pair for §3.

---

## 0. Before You Come (10 minutes, at home)

Factor this as $F = LU$ by elimination. Bring $L$, $U$, and the three multipliers.

$$F = \begin{bmatrix}2 & 1 & 0\\ 4 & 5 & 3\\ -2 & 5 & 10\end{bmatrix}$$

**Then, before you check anything:** multiply your $L$ and $U$ back together. If you do not get $F$, you have a sign error in $L$, and finding it yourself is worth more than the ten minutes it costs.

---

## 1. Four Readings, Out Loud (10 min)

$$A = \begin{bmatrix}2 & -1\\ 1 & 3\end{bmatrix}, \qquad B = \begin{bmatrix}1 & 0 & 4\\ 2 & 5 & -1\end{bmatrix}$$

**In pairs. One of you computes $AB$ by reading (ii), columns; the other by reading (iii), rows. Neither of you may use the entry formula.** Compare. Then both of you do reading (iv), outer products, together.

**Three questions to answer at the board before moving on:**

**(a)** Reading (iv) writes $AB$ as a sum of how many matrices here, and what size is each? What is the **rank** of each one? *(You do not have the definition of rank yet. Say what is obviously special about a matrix built as one column times one row.)*

**(b)** Does $BA$ exist? If so, what size? If not, why not — in terms of composition of functions rather than in terms of index bookkeeping.

**(c)** Reading (ii) says every column of $AB$ is a combination of the columns of $A$. **$A$ has two columns and $AB$ has three.** Is that a contradiction? Answer carefully; it is PS 1 Q1(c) and it is Week 2's first lecture.

---

## 2. $L$ Is Not Computed (15 min)

### (a) The transcription (5 min)

Check your prepared $F$ against your partner's:

| | Expect |
|---|---|
| Multipliers | $\ell_{21} = 2$, $\ell_{31} = -1$, $\ell_{32} = 2$ |
| $U$ | $\begin{bmatrix}2&1&0\\0&3&3\\0&0&4\end{bmatrix}$ |
| $L$ | $\begin{bmatrix}1&0&0\\2&1&0\\-1&2&1\end{bmatrix}$ |

**Say out loud, as a pair: nothing was calculated to build $L$.** The three numbers were already on your page. If you found yourself multiplying anything to get $L$, stop and find out what you did instead.

### (b) The one that needs a swap in the middle (10 min)

$$G = \begin{bmatrix}1 & 2 & 3\\ 2 & 4 & 1\\ 3 & 5 & 2\end{bmatrix}$$

**Eliminate column 1 only**, then stop.

**(i)** What is the $(2,2)$ entry now? Which of Week 0's two cases is it, and what is the test?

**(ii)** Fix it and finish. Give the pivots.

**(iii)** **Here is the part everyone gets wrong.** You want $P$ with $PG = LU$. You discovered the swap *in the middle* of the elimination — but $P$ multiplies the **original** $G$.

Write down your $P$, form $PG$, and **eliminate $PG$ from scratch.** Does it go through without a swap? What are $L$ and $U$?

**(iv)** Compare the $U$ you got in (ii) with the $U$ you got in (iii). Are they the same? Should they be? **And are the multipliers the same?**

> **The thing to leave with.** Discovering a swap is a fact about the elimination; $P$ is a fact
> about the original matrix. **LAPACK does exactly what you did in (iii)** — it records the row
> interchanges as it goes, in an integer vector called `ipiv`, and the factorisation it returns is
> of the permuted matrix. It does not re-run anything, because it does not have to; but the
> factorisation it hands you factors $PA$, not $A$, and **forgetting that is the most common bug in
> code that calls `lu_factor` directly.**

---

## 3. Ten Minutes With a Machine (10 min)

One laptop per pair:

```bash
python3 resources/matrices.py
```

**(a)** Find the section comparing solving $Hx = b$ against forming $H^{-1}$ and multiplying. **Inverting is worse at every $n$. By how much, at each?**

Now the real question: **the penalty is $20\times$ at $n=6$, $2\times$ at $n=10$, and $91\times$ at $n=12$.** It does not increase with $n$. **Is that reassuring or alarming?** Argue it as a pair.

**(b)** Find the tridiagonal $K$ and its inverse. Count the zeros in each. Then read the table at the bottom of that section: at $n = 10^4$, $K$ has $29{,}998$ nonzeros and $K^{-1}$ has $10^8$.

**At 8 bytes per entry, how much memory is $K^{-1}$ for $n = 10^6$?** Compare with $L$ and $U$, which keep the band. **This is the argument that actually stops people inverting**, more than the flop count does.

**(c)** *(If you finish early.)* Find the $(AB)C$ / $A(BC)$ timing. The flop ratio is $750$ and the measured speedup is around $787$. **The measurement beats the prediction.** What is the flop count not counting?

---

## 4. Clinic (whatever is left)

**The three that come up every year:**

- **PS 1 Q1(c).** If §1(c) landed, this is done. If it did not, ask now.
- **PS 1 Q4(c), the $P$.** §2(b)(iii) of this sheet is the same question with different numbers. **Do not ask for the answer; ask which step you are not able to justify.**
- **PS 1 Q5(b), the rule.** You have the two costs. The question is what single sentence predicts both, and "associate to the right" is not it — check your candidate rule against part (a) before you write it down.

> **What not to ask for.** "Is my $L$ right?" — multiply $LU$ and see. That check is exact, takes
> ninety seconds, and is more reliable than anyone's eye.

---

*MATH 241 · Week 1 · Recitation 1 · sat Thursday of Week 2 · unmarked*
