# MATH 241 · Recitation 5
## Determinants, the Day After the Midterm
### Covers Week 5 · sat **Thursday of Week 6**, 15:00–15:50, SSB 108 · **unmarked, attendance required**

---

> **This session sits in an awkward place and the sheet is built for it.**
>
> **Midterm 1 was yesterday** (Wednesday, 18:00–19:15, SSB 110, Weeks 0–5). **PS 5 is due at 17:00
> tomorrow.** So this is simultaneously the Week 5 recitation, a post-mortem, and the last clinic
> before a deadline.
>
> **The drill in §1–§3 is short for that reason**, and §4 is longer than usual. Come with your PS 5
> attempt **and** with whatever you could not do yesterday.

---

## 0. Before You Come (10 minutes, at home)

Compute $\det M$ **by elimination**, listing the pivots and counting exchanges:

$$M = \begin{bmatrix}1&2&0&0\\ 3&1&2&0\\ 0&4&1&3\\ 0&0&2&1\end{bmatrix}$$

*(It is banded — lots of zeros — so there is a temptation to expand by cofactors. **Do it by elimination anyway**; §1 compares the two.)*

**Also bring:** one question from yesterday's paper you are unsure you got right. Not the hardest one — **the one you cannot tell about.**

---

## 1. The Drill (10 min)

**In pairs, at the board.**

**(a)** Compare your prepared answers. **Expect $\det M = 17$.** If you and your partner differ, find the first pivot you disagree on rather than restarting.

**(b)** Now compute the same determinant by **cofactor expansion**, choosing your row or column deliberately. **Which was less work here?** Banded matrices are the case where cofactors are competitive — say why.

**(c)** Without computing, give the determinant of

$$\begin{bmatrix}1&3&2\\ 2&1&4\\ 4&7&8\end{bmatrix}$$

*(Look at the rows. One is a combination of the other two — find it.)*

**(d)** $\det M = 17$. **Write down, in one line each:** $\det(M^\mathsf{T})$, $\det(M^{-1})$, $\det(2M)$, $\det(M^2)$, $\det(N^{-1}MN)$.

> **$\det(2M)$ is the one people get wrong under time pressure.** $M$ is $4\times4$, so it is $2^4$,
> not $2$. **If that came up on yesterday's paper, check what you wrote.**

---

## 2. The Two Traps (10 min)

**(a)** A classmate says: *"$\det(A + B) = \det A + \det B$, because the determinant is linear."*

**Give the two-second counterexample**, then state precisely what P3 does claim. **Why is "linear in each row separately" not the same as "linear"?**

**(b)** A second classmate writes, in code:

```python
if abs(det(A)) < 1e-10:
    raise ValueError("matrix is singular")
```

**Break this in two different ways:**

1. A matrix that is **perfectly conditioned** and trips the check.
2. A matrix with **determinant 1** that is numerically hopeless.

*(You built both in PS 0 Q5(b). Two minutes if you remember them, five if you rebuild them.)*

**(c)** **The question to argue as a pair.** $\det A = 0$ **exactly** characterises singularity — it is a theorem, proved in L16 §5, with no approximation anywhere. **So why is it a bad test?** Answer in one sentence that distinguishes *exact mathematics* from *floating-point computation*.

---

## 3. Volume, Quickly (10 min)

**(a)** Find the volume of the parallelepiped with edges $(2,1,0)$, $(1,3,1)$, $(0,1,2)$.

**(b)** For each, give the determinant and say in one phrase what happens to area:

$$\begin{bmatrix}1&7\\0&1\end{bmatrix} \qquad \begin{bmatrix}3&0\\0&3\end{bmatrix} \qquad \begin{bmatrix}1&2\\3&6\end{bmatrix} \qquad \begin{bmatrix}0&1\\1&0\end{bmatrix}$$

**(c)** One of those four has a **negative** determinant. What does the sign mean, and why can no rotation ever produce it? *(Think about what would have to happen to the determinant along the way.)*

**(d)** **The payoff.** Compute the Jacobian of $x = r\cos\theta$, $y = r\sin\theta$ and get $r$. **State the sentence that connects this to MATH 142's $dA = r\,dr\,d\theta$.**

---

## 4. Clinic — PS 5, and Yesterday's Paper (15+ min)

**This is the long section this week.** Two things happen in it, in this order.

### First: PS 5, due tomorrow at 17:00

**The three that come up every year:**

- **Q3(a), the adjugate.** $\operatorname{adj}C$ is the **transpose** of the cofactor matrix. Forgetting the transpose gives a matrix that fails the $C\cdot\operatorname{adj}C = (\det C)I$ check — **which is why the question asks you to run it.**
- **Q3(c), "what is Cramer's rule for".** You will have costed it and found it hopeless. **The question is what remains valuable once you know that.** Look at the *form* of the answer, not the arithmetic.
- **Q5's closing warning.** §2(b) of this sheet is the same question. If §2 landed, this is written.

### Second: yesterday's paper

**Bring the question you could not call.** Not for a mark — the paper is marked already — but because **the same material is on the final**, and the gap between "I think I got it" and "I know I got it" is the thing worth closing while it is fresh.

> **What the TA will and will not do.** Will: work the *method* of a question you found hard, using
> different numbers. Will not: confirm whether your particular answer was right, or discuss the
> mark scheme. **Marks are Prof. Abara's** and the paper is returned in Week 7.
>
> **If you found the whole paper hard**, the useful conversation is not about the paper. Go to
> office hours — Thursday 10:00–11:00, SSB 310, which is this morning — or the Help Desk. **Weeks
> 6–11 are cumulative on Weeks 2–4**, and a gap there does not close by itself.

---

*MATH 241 · Week 5 · Recitation 5 · sat Thursday of Week 6 · unmarked*
