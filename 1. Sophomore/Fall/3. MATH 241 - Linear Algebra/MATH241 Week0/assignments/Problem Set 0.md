# MATH 241 · Problem Set 0
## Linear Systems, Elimination, and What the Algorithm Costs

---

**Released:** Week 0, Wednesday · **Due:** Week 1, **Friday 17:00**
**Total: 100 points** · Submit one PDF, `PS0_{LastName}_{StudentID}.pdf`

> Collaboration on *approaches* is fine and encouraged. **The write-up must be yours**, and that
> includes the arithmetic — copying a worked elimination is both obvious and pointless.
>
> **Show the multipliers.** Every row operation is written as $R_i \leftarrow R_i - \ell R_k$ with
> $\ell$ stated. An answer with no working earns the marks for the answer and none for the method,
> which on this paper is most of them.
>
> **Exact arithmetic throughout Q1–Q3.** Fractions, not decimals. $\tfrac{7}{3}$, never $2.33$.
>
> **Q4 and Q5 are run on a computer**, using `resources/elimination.py` from this week's folder.
> State your Python version and whether you are on your own machine or a lab machine.
>
> **Recitation 0 is the Thursday before this is due**, 15:00–15:50, SSB 108. Arrive with the
> question you are actually stuck on.

---

### Q1: Elimination by Hand (24 points)

For each system: eliminate to row echelon form, **listing every multiplier and every row exchange**, state the pivots, and solve by back substitution. Check each answer by substituting into the *original* equations.

**(a) [8]**

$$\begin{aligned}
x_1 + 2x_2 + 2x_3 &= 3\\
2x_1 + 5x_2 + 7x_3 &= 5\\
3x_1 + 6x_2 + 8x_3 &= 7
\end{aligned}$$

One of the three multipliers is $0$. **Record it anyway**, and say in one sentence what a zero multiplier means about the two rows involved.

**(b) [8]**

$$\begin{aligned}
\phantom{1}x_2 + 2x_3 &= 3\\
x_1 + 3x_2 + \phantom{1}x_3 &= 0\\
2x_1 + 5x_2 + 4x_3 &= 5
\end{aligned}$$

This one cannot start. Say precisely why, fix it, and name which of L02 §2's three operations you used.

**(c) [8]**

$$\begin{aligned}
x_1 + 3x_2 - 2x_3 &= 1\\
2x_1 + \phantom{1}x_2 + 4x_3 &= 7\\
4x_1 + 7x_2 \phantom{{}+ 4x_3} &= d
\end{aligned}$$

Eliminate with $d$ carried as a symbol. **For which single value of $d$ is the system consistent?** For that $d$, give **all** solutions in the form *(one particular solution)* $+\ t\,\cdot$ *(one vector)*. For any other $d$, quote the row of the echelon form that proves there is no solution.

---

### Q2: The Two Pictures (18 points)

Throughout, let

$$B = \begin{bmatrix}1 & 2 & 3\\ 2 & -1 & 1\\ 3 & 1 & 4\end{bmatrix}.$$

**(a) [6]** Draw, on paper, both pictures for the $2\times2$ system $\;x_1 - 2x_2 = -1,\; 3x_1 + 2x_2 = 9$. Label the solution in each. Then state, in one sentence each, **what a solution *is* in each picture** — the two sentences should not be paraphrases of one another.

**(b) [6]** Show that $Bx = (6,2,8)$ has more than one solution by **exhibiting two different linear combinations of the columns of $B$ that both produce $(6,2,8)$**. Neither may be found by elimination: get them by inspection, using a relationship between the columns, and say what that relationship is.

**(c) [6]** Prove that $Bx = (6,2,9)$ has **no** solution, *without eliminating*. 

> *The argument to find:* every column of $B$ satisfies one particular linear relation among its
> three entries. Show that every linear combination of the columns therefore satisfies it too, and
> that $(6,2,9)$ does not. **Three lines, and it proves more than elimination does** — elimination
> shows this one $b$ fails, and your argument describes every $b$ that fails.

---

### Q3: Three Outcomes (16 points)

**(a) [6]** For which values of $c$ and $d$ does

$$\begin{aligned}
x_1 + 2x_2 + 3x_3 &= 1\\
2x_1 + 5x_2 + 8x_3 &= 3\\
3x_1 + 7x_2 + cx_3 &= d
\end{aligned}$$

have (i) exactly one solution, (ii) no solution, (iii) infinitely many? Give the echelon form with $c$ and $d$ carried through, and read all three answers off its last row.

**(b) [5]** Suppose $Az = 0$ for some $z \ne 0$. Prove that for **every** $b$, the system $Ax = b$ has either no solution or infinitely many — never exactly one. *(Two lines. Both directions of the case split are needed.)*

**(c) [5]** Write down a $3\times3$ system whose three planes **meet in pairs but have no common point**, and demonstrate both halves: exhibit a point on each pairwise intersection line, and derive the contradiction that rules out a common point.

---

### Q4: What Elimination Costs (22 points)

Run `resources/elimination.py` from this week's folder. Quote its output where you rely on it.

**(a) [8]** Derive the operation counts $\;\approx n^3/3\;$ for forward elimination and $\;\approx n^2/2\;$ for back substitution, showing the sums. Then answer with numbers:

- You must solve $Ax = b_j$ for **200 different right-hand sides**, with $A$ fixed, $n = 400$. Compare **(i)** running the whole algorithm 200 times, once per $b_j$, against **(ii)** augmenting $A$ with all 200 right-hand sides at once — $[\,A \mid b_1\ \cdots\ b_{200}\,]$ — and eliminating a single time. Count the elimination and the back substitutions in both, give both totals, and give the ratio.
- At what $n$ does elimination on a machine doing $10^{10}$ operations per second take longer than one hour?

**(b) [8]** Reproduce the table in `elimination.py`'s "no pivoting / partial pivoting" section, then **extend it to $\varepsilon = 10^{-13}$ and $\varepsilon = 10^{-14}$.**

- Report the unpivoted $x_1$ at each of the six $\varepsilon$ values.
- **The relative error does not fall monotonically as $\varepsilon$ grows.** Say where it does not, and offer an explanation. *(The $\varepsilon = 10^{-16}$ row in the notes is the hint.)*

**(c) [6]** In your own words, and with the intermediate values printed to check yourself: **why does the unpivoted algorithm return exactly $0.0$ at $\varepsilon = 10^{-17}$?** Name the step at which information is lost, say what quantity is lost, and state what partial pivoting changes so that it is not.

---

### Q5: Nonsingular Is Not the Same as Safe (20 points)

**(a) [8]** Using `elimination.py`, solve $H_n x = b$ for the Hilbert matrices at $n = 4, 6, 8, 10, 12$, with $b$ chosen so the exact answer is $x = (1, 1, \dots, 1)$. Report the exact condition number and the worst error at each $n$.

Then check the rule of thumb *(correct digits $\approx 16 - \log_{10}\operatorname{cond}$)* at every row and report the discrepancy. **Is the rule optimistic or pessimistic? Consistently?**

**(b) [6]** Give a $2\times2$ matrix that is

- **(i)** almost singular by determinant and perfectly conditioned: $\det A = 10^{-8}$ and $\operatorname{cond}_\infty(A) = 1$;
- **(ii)** the other way round: $\det A = 1$ and $\operatorname{cond}_\infty(A) \ge 10^{12}$.

Give both matrices and both computations in full. Then say, in two sentences, what your pair establishes about using $\det A$ to decide whether a solve can be trusted.

**(c) [6]** A colleague solves a $1000 \times 1000$ system, computes the residual $\lVert Ax - b\rVert$, finds it is $10^{-14}$, and concludes the answer is accurate to fourteen digits.

Explain why the conclusion does not follow. Construct a small explicit example — $2\times2$ is enough — of a computed $x$ with a tiny residual and a large error, and give both numbers. **What should the colleague have computed instead?**

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Elimination by hand | 24 |
| 2 | The two pictures | 18 |
| 3 | Three outcomes | 16 |
| 4 | What elimination costs | 22 |
| 5 | Nonsingular is not the same as safe | 20 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*MATH 241 · Week 0 · PS 0 · © CSE Department*
