# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 9.1 (L27) — Recurrence Relations: Modelling and Iteration
### Monday, Week 9

**Date:** Monday 23 November 2026 · 13:00–13:50 · Week 9

---

## 1. Definition by Self-Reference

A **recurrence relation** defines each term of a sequence using earlier terms.

$$a_n = 2a_{n-1} + 3, \qquad a_0 = 1$$

Two parts, both essential: the **recurrence** and the **initial conditions**. Without initial
conditions the relation describes infinitely many sequences; without the recurrence you have a single
number.

**Week 3's induction is the same shape seen from the other side.** Induction proves a property by
reducing $n$ to $n-1$; a recurrence *defines* a value by reducing $n$ to $n-1$. Recursion in code is
the third face of the same idea — which is why this week is the mathematical foundation for
recursive algorithm analysis in CS 102.

---

## 2. Modelling With Recurrences

The skill worth having is not solving recurrences — it is **writing them down** from a problem
statement.

### Tower of Hanoi

Move $n$ discs from one peg to another, never placing a larger disc on a smaller one.

To move $n$ discs: move the top $n-1$ to the spare peg, move the largest disc, move the $n-1$ back.

$$T_n = 2T_{n-1} + 1, \qquad T_0 = 0$$

### Fibonacci — rabbit pairs, or anything else

$$F_n = F_{n-1} + F_{n-2}, \qquad F_0 = 0,\ F_1 = 1$$

### Bit strings with no two consecutive zeros

Let $b_n$ count length-$n$ strings over $\{0,1\}$ with no `00`. A valid string either ends in 1
(preceded by any valid string of length $n-1$) or ends in `10` (preceded by any valid string of
length $n-2$):

$$b_n = b_{n-1} + b_{n-2}, \qquad b_1 = 2,\ b_2 = 3$$

Same recurrence as Fibonacci, different initial conditions — so $b_n = F_{n+2}$. **The recurrence
captures the structure; the initial conditions locate you within it.**

### Compound interest

$$A_n = 1.05\,A_{n-1}, \qquad A_0 = P$$

---

## 3. Solving by Iteration (Unrolling)

The most direct method: expand until the pattern is visible, then prove it by induction.

### Tower of Hanoi, unrolled

$$
\begin{aligned}
T_n &= 2T_{n-1}+1\\
&= 2(2T_{n-2}+1)+1 = 4T_{n-2}+2+1\\
&= 4(2T_{n-3}+1)+3 = 8T_{n-3}+4+2+1\\
&\ \ \vdots\\
&= 2^k T_{n-k} + (2^{k-1}+\cdots+2+1)
\end{aligned}
$$

Setting $k=n$ and using $T_0 = 0$:

$$T_n = 2^n \cdot 0 + (2^{n-1}+\cdots+1) = \mathbf{2^n - 1}$$

**Verified:** iterating the recurrence to $n=14$ agrees with $2^n-1$ at every step; $T_{10} = 1023$.

**This must still be proved by induction** — unrolling shows the pattern, it does not establish it.
The induction is routine: $T_{n} = 2(2^{n-1}-1)+1 = 2^n - 1$ ✓

**The interpretation matters.** $2^n - 1$ moves means 64 discs take $2^{64}-1 \approx 1.8\times10^{19}$
moves. At one move per second that is longer than the age of the universe. A recurrence with a
doubling factor is not merely "slow" — it is a wall.

### A non-homogeneous example

$$a_n = 2a_{n-1}+3,\quad a_0 = 1 \;\Longrightarrow\; a_n = 4\cdot2^n - 3$$

**Verified** against iteration for $n \le 11$: $1, 5, 13, 29, 61, \ldots$ ✓

---

## 4. Where Recurrences Come From in Computing

| Algorithm | Recurrence | Solution |
|---|---|---|
| Linear search | $T_n = T_{n-1} + 1$ | $\Theta(n)$ |
| Binary search | $T_n = T_{n/2} + 1$ | $\Theta(\log n)$ |
| Merge sort | $T_n = 2T_{n/2} + n$ | $\Theta(n\log n)$ |
| Naive Fibonacci | $T_n = T_{n-1}+T_{n-2}+1$ | $\Theta(\varphi^n)$ |
| Tower of Hanoi | $T_n = 2T_{n-1}+1$ | $2^n - 1$ |

**The naive Fibonacci row is the one to stare at.** Computing $F_n$ by direct recursion costs
*exponential* time, because the same subproblems are recomputed astronomically often — $F_{30}$
requires **2,692,537** calls to produce the answer $832040$. Storing intermediate results
(memoisation) collapses it to $\Theta(n)$. CS 102 calls this dynamic programming; it is nothing more
than *evaluating a recurrence in the right order*.

---

## 5. Degree, Order, and Vocabulary

| Term | Meaning |
|---|---|
| **Order** | How many previous terms appear: $a_n = a_{n-1}+a_{n-2}$ has order 2 |
| **Linear** | Terms appear to the first power, not multiplied together |
| **Constant coefficients** | The multipliers do not depend on $n$ |
| **Homogeneous** | No term free of the $a_i$ — no "$+3$", no "$+n^2$" |

$$a_n = 5a_{n-1}-6a_{n-2} \quad\text{— linear, order 2, constant coefficients, homogeneous}$$
$$a_n = 2a_{n-1}+3 \quad\text{— linear, order 1, constant coefficients, \textbf{non}-homogeneous}$$
$$a_n = a_{n-1}\cdot a_{n-2} \quad\text{— \textbf{not} linear}$$
$$a_n = n\,a_{n-1} \quad\text{— linear but \textbf{not} constant-coefficient}$$

Wednesday's method solves exactly the first kind — **linear, constant-coefficient, homogeneous** —
and extends with effort to the second. The last two need other tools.

---

## 6. Summary

| Idea | Statement |
|---|---|
| A recurrence needs both | the relation **and** initial conditions |
| Modelling | decompose by what happens at the last step |
| Same recurrence, different start | $b_n = F_{n+2}$ for no-`00` bit strings |
| Iteration | unroll, spot the pattern, **then prove by induction** |
| Hanoi | $T_n = 2^n - 1$ |
| $a_n = 2a_{n-1}+3$, $a_0=1$ | $a_n = 4\cdot 2^n - 3$ |
| Classification | order, linear, constant-coefficient, homogeneous |
| Naive Fibonacci | exponential — the case for memoisation |

---

## 7. End-of-Lecture Exercises

1. Write a recurrence for the number of length-$n$ bit strings with **no two consecutive 1s**. State the initial conditions and compute the first six values.

2. Solve $a_n = 3a_{n-1}$, $a_0 = 5$, by iteration.

3. Solve $a_n = a_{n-1} + n$, $a_0 = 0$, by iteration. *(You should recognise the answer.)*

4. A country issues stamps worth 3¢ and 5¢. Write a recurrence for the number of ways to make $n$ cents where **order matters**, and compute the first eight values.

5. Unroll $T_n = 2T_{n-1} + 1$ with $T_0 = 1$ instead of $0$. How does the closed form change?

6. **(Stretch.)** The derangement numbers satisfy $D_n = (n-1)(D_{n-1}+D_{n-2})$. Verify this against the Week 8 table for $n \le 6$, and explain combinatorially where the factor $(n-1)$ comes from.

---

## Reading

- **Rosen, 8e §8.1** — Applications of recurrence relations
- **Epp, 5e §5.6** — Recursive definitions and sequences
- **Levin, 3e §2.4** — Solving recurrence relations

*Next: Lecture 9.2 — Solving Linear Recurrences with the Characteristic Equation*
