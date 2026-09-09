# MATH 241 · Recitation 0
## Elimination at the Board
### Covers Week 0 · sat **Thursday of Week 1**, 15:00–15:50, SSB 108 · **unmarked, attendance required**

---

> **This recitation covers Week 0 and is sat in Week 1.** The recitation is Thursday and this
> course's lectures are Monday, Tuesday and **Friday**, so a session can never cover the week it
> sits in — Recitation *N* covers Week *N* and is sat on the Thursday of Week *N+1*. **There was no
> recitation in Week 0.** Every recitation file states its own week; the file is authoritative.
>
> **PS 0 is due at 17:00 tomorrow.** That is not an accident of the timetable — the lag was chosen
> to put this session the afternoon before the deadline. **Come with your partial attempt**, not
> with a blank page.
>
> **Unmarked, and attendance is required** — [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]]
> costs a letter grade after a second unexcused absence. Nothing is handed in.

**What this session is.** Fifty minutes at the board, in pairs, on the four things that go wrong in Week 0. It is **not** a lecture and it is **not** a walkthrough of PS 0 — the numbers below are deliberately different from the ones on the paper, and they exercise the same four skills.

**What to bring:** paper, your attempt at PS 0, and a laptop between every two people for §4.

---

## 0. Before You Come (10 minutes, at home)

Eliminate this by hand and bring the result. **The session starts with it and does not wait.**

$$\begin{aligned}
2x_1 + 4x_2 - 2x_3 &= \phantom{1}2\\
4x_1 + 9x_2 - 3x_3 &= \phantom{1}8\\
-2x_1 - 3x_2 + 7x_3 &= 10
\end{aligned}$$

Write down: the three multipliers, the three pivots, and $x$. If you cannot finish it, bring how far you got — **the place you stopped is more useful to the session than a finished answer.**

---

## 1. Warm-Up: The Multiplier Discipline (10 min)

**At the board, in pairs.** One of you eliminates, the other writes only the multipliers, out loud, before each operation. Then swap.

**Check against each other**, not against a solution:

| | Expect |
|---|---|
| Multipliers | $\ell_{21} = 2$, $\ell_{31} = -1$, $\ell_{32} = 1$ |
| Pivots | $2,\ 1,\ 4$ |
| Solution | $x = (-1, 2, 2)$ |

**Two things to notice out loud before moving on:**

1. **$\ell_{31} = -1$ is negative**, so the operation is $R_3 \leftarrow R_3 + R_1$. Say the words "minus minus one" once and you will stop dropping the sign.
2. The solution has $x_1 = -1$. **Substitute it back into the original first equation now** — not into your echelon form. Sixty per cent of the errors in this room are caught by that one substitution and by nothing else.

> **If your pair disagrees, do not re-derive.** Find the *first* row where your two echelon forms
> differ and look only at that one operation. Disagreements are almost always a single multiplier,
> and hunting from the top is much faster than starting again.

---

## 2. The Zero That Is Not at the Top (15 min)

Everyone expects a zero in the $(1,1)$ position. **Almost nobody expects one to appear in the middle**, and this is where Week 0's marks are lost.

$$\begin{bmatrix}1 & 2 & 3\\ 2 & 4 & 7\\ 3 & 5 & 3\end{bmatrix}, \qquad b = \begin{bmatrix}6\\13\\11\end{bmatrix}$$

**Do the first column.** You should get

$$\left[\begin{array}{ccc|c} 1 & 2 & 3 & 6\\ 0 & 0 & 1 & 1\\ 0 & -1 & -6 & -7\end{array}\right]$$

**Now stop and answer, at the board, before doing anything else:**

**(a)** The $(2,2)$ entry is $0$. **Which of L02 §6's two cases is this** — the fixable kind or the singular kind? *How do you know*, and what is the one thing you had to look at to decide?

**(b)** Fix it and finish. What are the pivots?

**(c)** The original matrix has a zero nowhere in it. **Where did the zero come from?** Answer in terms of rows 1 and 2 of the *original* matrix, not in terms of the arithmetic you just did.

**(d)** **The question worth the fifteen minutes.** Suppose row 3 had been $[\,2\ \ 4\ \ 9\,]$ instead of $[\,3\ \ 5\ \ 3\,]$. Redo the first column. What happens now, and which of the two cases is it? Say what the *matrix* is like in each case, in a sentence that does not mention elimination.

---

## 3. Reading the Columns (10 min)

$$C = \begin{bmatrix}1 & 2 & 1\\ 3 & 6 & 0\\ 2 & 4 & 5\end{bmatrix}$$

**No elimination in this section. Pens down on the algorithm.**

**(a)** Find the relationship between the columns of $C$ by looking at them. *(It is visible in under five seconds. If you are computing, you are doing the wrong thing.)*

**(b)** $Cx = b$ is solvable for some $b$ and not for others. **Describe the set of solvable $b$ geometrically**, in one sentence, using the word *plane*.

**(c)** Find a single linear equation $\alpha b_1 + \beta b_2 + \gamma b_3 = 0$ that every solvable $b$ satisfies. Verify it on all three columns of $C$ — each column is trivially solvable, so each must satisfy it.

**(d)** Use your equation to decide, **without eliminating**, whether each of these is solvable: $(1,3,2)$, $(1,1,1)$, $(0,0,0)$, $(3,9,6)$.

**(e)** For one solvable $b$ of your choice, give **two different** $x$ that reach it.

> **The point of this section**, and it is worth saying at the board: elimination answers "is *this*
> $b$ reachable" one $b$ at a time. **The equation you found in (c) answers it for all $b$ at once,
> and it took no arithmetic.** Week 2 gives that equation and that plane their proper names.

---

## 4. Fifteen Minutes With a Machine (10 min)

One laptop per pair. `cd` to this week's folder and run:

```bash
python3 resources/elimination.py
```

**(a)** Find the "no pivoting / partial pivoting" table. **Predict, before scrolling, what the unpivoted answer will be at $\varepsilon = 10^{-17}$.** Most of the room predicts something large. Then look.

**(b)** Edit the tuple of $\varepsilon$ values and add $10^{-14}$ and $10^{-13}$. Where does the unpivoted column become acceptable? **Say what "acceptable" meant when you decided** — you have just done, informally, what an error bound does formally.

**(c)** Find the Hilbert table. `cond` at $n = 12$ is $4.1\times10^{16}$. Machine epsilon is $2.2\times10^{-16}$. **Multiply them.** What have you just computed, and why does a product of $1$ or more mean the end of the road?

**(d)** *(If you finish early.)* $\det H_{10} \approx 2.2\times10^{-53}$, which is small. Multiply $H_{10}$ by $10$ and ask what happens to (i) its determinant and (ii) its condition number. Which of the two changed, and what does that tell you about which one to trust?

---

## 5. Clinic (whatever is left)

Bring the question you are actually stuck on in PS 0.

**The three that come up every year**, so ask if any of them is yours:

- **Q1(c) with $d$ carried as a symbol.** People eliminate the numbers and then try to put $d$ back. Carry it from the first row operation and it is no harder than a number.
- **Q2(c) "without eliminating".** The intended argument is §3(c) of this sheet. If §3 landed, Q2(c) is three lines.
- **Q5(c) residual against error.** They are not the same measurement and the question is built on the gap. If that sentence is not yet obvious, ask now rather than at 16:55 tomorrow.

> **What not to ask for.** "Can you check my Q1?" is not a recitation question — substitute your
> answer into the original equations and you have checked it yourself, in thirty seconds, more
> reliably than anyone can by eye. **Ask about the step you could not take**, not about the answer
> you already have.

---

*MATH 241 · Week 0 · Recitation 0 · sat Thursday of Week 1 · unmarked*
