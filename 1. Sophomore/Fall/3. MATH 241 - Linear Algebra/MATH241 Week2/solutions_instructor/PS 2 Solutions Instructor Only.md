# MATH 241 · Problem Set 2 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Everything on this paper is exact arithmetic**; `resources/spaces.py` reproduces the $B$ computations if a script needs checking.

**What this paper is testing.** Q1 is the definitional grind and should be near-full marks. **Q2(e) and Q3(d) are the conceptual core** — that elimination preserves the null space and moves the column space is the one Week 2 idea that students carry away wrong, and it reappears in Week 3 as "row rank = column rank" and in Week 9 as a bug in their least-squares code. Q4(d) tests whether they know what the answer to a linear system *is*. Q5(c) is the hardest thing on the paper and it is Week 9's foundation.

**Common failure modes:** (1) asserting a subspace rather than testing it; (2) putting $\mathbf{C}(B)$ and $\mathbf{N}(B)$ in the same space; (3) Q2(b) answered with the pivot columns **of the rref**; (4) Q4(d) answered "yes, one of us is wrong".

---

## Q1: Subspaces (20 points)

### (a) [10] — 2 each

**1. $\{x - 2y + z = 0\}$ — YES.**
$0$: $0 - 0 + 0 = 0$ ✓. Sums: if $u, v$ satisfy it then $(u_1+v_1) - 2(u_2+v_2) + (u_3+v_3) = 0 + 0 = 0$ ✓. Scaling: $c u_1 - 2cu_2 + cu_3 = c\cdot 0 = 0$ ✓. **A plane through the origin.**

**2. $\{x - 2y + z = 5\}$ — NO.** $0 - 0 + 0 = 0 \ne 5$, so **$0$ is not in it**; condition 1 fails. *(A plane not through the origin. It is a translate of row 1's plane, which is exactly L09 §7's picture.)*

**3. $\{xyz = 0\}$ — NO.** $(1,1,0)$ and $(0,0,1)$ are both in it, and $(1,1,0) + (0,0,1) = (1,1,1)$ has $xyz = 1 \ne 0$. **Closure under addition fails.** *(It contains $0$ and is closed under scaling — two conditions out of three, which is why all three are checked.)*

**4. $\{x \le y \le z\}$ — NO.** $(1,2,3)$ is in it; $(-1)(1,2,3) = (-1,-2,-3)$ needs $-1 \le -2$, false. **Closure under scaling fails.** *(Contains $0$ and is closed under addition. The other two-out-of-three.)*

**5. Symmetric $2\times2$ — YES.** $0^\mathsf{T} = 0$ ✓; $(A+B)^\mathsf{T} = A^\mathsf{T}+B^\mathsf{T} = A+B$ ✓; $(cA)^\mathsf{T} = cA^\mathsf{T} = cA$ ✓. **All three from Week 1's L06 §1 rules.**

*Marking: 2 each — 1 for the verdict, 1 for the work. **A "no" without specific vectors earns 1 of 2.** Rows 3 and 4 are the ones to read carefully; a student who names the failing condition for each has understood why the test has three parts.*

### (b) [4]

$$A = \begin{bmatrix}1&0\\0&0\end{bmatrix}, \quad B = \begin{bmatrix}0&0\\0&1\end{bmatrix}, \qquad \det A = \det B = 0, \qquad A + B = I,\ \det I = 1$$

**Closure under addition fails.** *(Any pair of complementary rank-one matrices works.)*

*Marking: 3 for the example, 1 for naming the condition.*

### (c) [6]

**$U \cap W$ is a subspace.** $0 \in U$ and $0 \in W$, so $0 \in U \cap W$. If $u, v \in U \cap W$ then $u+v \in U$ (as $U$ is a subspace) and $u+v \in W$, so $u+v \in U\cap W$; likewise $cu$. $\square$

**Union failing.** $U = x$-axis, $W = y$-axis in $\mathbb{R}^2$. $(1,0) \in U$ and $(0,1) \in W$, both in $U \cup W$, but $(1,0)+(0,1) = (1,1)$ is on neither axis. **Addition fails.**

**The only circumstance: $U \subseteq W$ or $W \subseteq U$** (then the union is the larger one, which is a subspace).

*Proof of "only".* Suppose neither contains the other, so there are $u \in U\setminus W$ and $w \in W \setminus U$. If $U \cup W$ were a subspace it would contain $u + w$. Say $u + w \in U$; then $w = (u+w) - u \in U$, a contradiction. Say instead $u+w \in W$; then $u = (u+w) - w \in W$, also a contradiction. So $U \cup W$ is not a subspace. $\square$

*Marking: 2 for the intersection, 1 for the union counterexample, 3 for the "only" proof. **The proof by contradiction is the hard part and most scripts will assert the condition without proving it is necessary — award 1 of the 3 for a correct statement alone.***

---

## Q2: The Column Space (22 points)

### (a) [4]

$$B = \begin{bmatrix}1&2&0&3\\ 2&4&1&8\\ 1&2&1&5\end{bmatrix} \xrightarrow[\;\ell_{31}=1\;]{\;\ell_{21}=2\;} \begin{bmatrix}1&2&0&3\\ 0&0&1&2\\ 0&0&1&2\end{bmatrix} \xrightarrow{\;\ell_{32}=1\;} \begin{bmatrix}1&2&0&3\\ 0&0&1&2\\ 0&0&0&0\end{bmatrix}$$

Already reduced (pivots are $1$, and column 3 is clear above). **Pivot columns 1 and 3; free columns 2 and 4; rank $r = 2$.**

### (b) [5]

$$\mathbf{C}(B) = \operatorname{span}\left\{\begin{bmatrix}1\\2\\1\end{bmatrix}, \begin{bmatrix}0\\1\\1\end{bmatrix}\right\} \subseteq \mathbb{R}^3$$

**Columns 1 and 3 of $B$** — the pivot positions. **A plane through the origin in $\mathbb{R}^3$**, since two independent vectors span a 2-dimensional subspace.

*Marking: 3 for the right two columns, 1 for $\mathbb{R}^3$, 1 for "plane through the origin". **Deduct 3 for taking the pivot columns of the rref** — $(1,0,0)$ and $(0,1,0)$ — which is L08 §4's trap and gives a different plane.*

### (c) [5]

Need $\alpha b_1 + \beta b_2 + \gamma b_3 = 0$ on both spanning columns:

$$(1,2,1): \ \alpha + 2\beta + \gamma = 0 \qquad (0,1,1): \ \beta + \gamma = 0$$

From the second, $\beta = -\gamma$; then $\alpha - 2\gamma + \gamma = 0$, so $\alpha = \gamma$. Take $\gamma = 1$:

$$\boxed{\;b_1 - b_2 + b_3 = 0\;}$$

| column | $b_1 - b_2 + b_3$ | |
|---|---|---|
| $(1,2,1)$ | $1 - 2 + 1$ | $0$ ✓ |
| $(2,4,2)$ | $2 - 4 + 2$ | $0$ ✓ |
| $(0,1,1)$ | $0 - 1 + 1$ | $0$ ✓ |
| $(3,8,5)$ | $3 - 8 + 5$ | $0$ ✓ |

*Marking: 3 for the equation, 2 for checking all four. **The two unused columns are the point of the check** — they are the ones that could have failed.*

### (d) [4] — 1 each

| $b$ | $b_1 - b_2 + b_3$ | In $\mathbf{C}(B)$? |
|---|---:|---|
| $(6,15,9)$ | $0$ | **yes** |
| $(6,15,10)$ | $1$ | **no** |
| $(0,0,0)$ | $0$ | **yes** — every subspace contains $0$ |
| $(1,3,2)$ | $0$ | **yes** |

### (e) [4]

$$\operatorname{rref}(B) = \begin{bmatrix}1&2&0&3\\0&0&1&2\\0&0&0&0\end{bmatrix}, \quad \text{columns } (1,0,0),\ (2,0,0),\ (0,1,0),\ (3,2,0)$$

Every one has third entry $0$, so

$$\mathbf{C}(\operatorname{rref} B) = \{b : b_3 = 0\} \qquad\text{against}\qquad \mathbf{C}(B) = \{b : b_1 - b_2 + b_3 = 0\}$$

**A separating vector, either direction:**

| $v$ | in $\mathbf{C}(B)$? | in $\mathbf{C}(\operatorname{rref}B)$? |
|---|---|---|
| $(1,0,0)$ | **no** — $1 - 0 + 0 = 1$ | **yes** — $b_3 = 0$ |
| $(0,1,1)$ | **yes** — $0 - 1 + 1 = 0$ | **no** — $b_3 = 1$ |

> **Watch for $(1,1,0)$**, which is the natural first guess and lies in **both** ($1-1+0 = 0$ and
> $b_3 = 0$). A script offering it has not checked. Award the mark only where the separating vector
> is verified against both equations.

**What elimination preserves: the dependencies among the columns** — equivalently the null space — **not the space the columns span.**

*Marking: 2 for the two equations, 1 for a correct separating vector, 1 for the preservation sentence. **Accept a separating vector in either direction; require that they verify it, since $(1,1,0)$ lies in both and is the natural first guess.***

---

## Q3: The Null Space (22 points)

### (a) [8]

From $\operatorname{rref}(B)$: $\;x_1 + 2x_2 + 3x_4 = 0$ and $x_3 + 2x_4 = 0$. Free: $x_2, x_4$.

**$s_2$** ($x_2=1, x_4=0$): $x_3 = 0$, $x_1 = -2$. $\;s_2 = (-2, 1, 0, 0)$
**$s_4$** ($x_4=1, x_2=0$): $x_3 = -2$, $x_1 = -3$. $\;s_4 = (-3, 0, -2, 1)$

**Verified against $B$:**

$$Bs_2 = -2(1,2,1) + (2,4,2) = (0,0,0)\ ✓$$
$$Bs_4 = -3(1,2,1) - 2(0,1,1) + (3,8,5) = (-3,-6,-3) + (0,-2,-2) + (3,8,5) = (0,0,0)\ ✓$$

$$\mathbf{N}(B) = \{\,t(-2,1,0,0) + u(-3,0,-2,1)\,\} \subseteq \mathbb{R}^4, \qquad \dim = 2$$

*Marking: 5 for the two special solutions, 2 for verification against $B$, 1 for $\mathbb{R}^4$ and dimension 2. **$\mathbb{R}^4$ is the mark students lose** — many write $\mathbb{R}^3$ by carrying over from Q2.*

### (b) [5]

$s_2 = (-2,1,0,0)$ says $-2b_1 + b_2 = 0$, i.e. $\;\boxed{b_2 = 2b_1}$: $\;2(1,2,1) = (2,4,2)$ ✓

$s_4 = (-3,0,-2,1)$ says $-3b_1 - 2b_3 + b_4 = 0$, i.e. $\;\boxed{b_4 = 3b_1 + 2b_3}$: $\;3(1,2,1) + 2(0,1,1) = (3,6,3)+(0,2,2) = (3,8,5)$ ✓

*Marking: 2 per dependency, 1 for both verifications. **The point to make on the script: the null space is the complete list of column dependencies.***

### (c) [4]

**$B$:** rank $2$ + nullity $2 = 4 = n$ ✓

**$B'$ is $4\times5$**, so $m = 4$, $n = 5$. Eliminating gives

$$\operatorname{rref}(B') = \begin{bmatrix}1&2&0&1&1\\ 0&0&1&2&1\\ 0&0&0&0&0\\ 0&0&0&0&0\end{bmatrix}, \qquad r = 2$$

**Nullity $= n - r = 5 - 2 = 3$**, by counting free columns — no special solutions needed.

*Marking: 1 for $B$, 3 for $B'$. **Full marks require the nullity obtained by subtraction**, as instructed; a student who computes all three special solutions has answered a different question and gets 2 of the 3.*

### (d) [5]

Each row operation is left multiplication by an invertible matrix (Week 1's L06 §3), so $\operatorname{rref}(A) = EA$ for some invertible $E$.

**($\subseteq$)** If $Ax = 0$ then $EAx = E0 = 0$, so $x \in \mathbf{N}(EA)$.
**($\supseteq$)** If $EAx = 0$ then, multiplying by $E^{-1}$, $Ax = E^{-1}0 = 0$. $\square$

**Why it fails for the column space:** the argument moves $x$, and $x$ is untouched by row operations — but $\mathbf{C}$ is a statement about the *columns*, and $EA$ has different columns from $A$ ($Ea_j$ rather than $a_j$). **There is no reason for $\operatorname{span}\{Ea_j\}$ to equal $\operatorname{span}\{a_j\}$, and Q2(e) shows it does not.**

*Marking: 3 for both directions (1 if only one), 2 for the column-space contrast. **The invertibility of $E$ is the whole proof; a script that omits it has shown only $\subseteq$.***

---

## Q4: The Complete Solution (20 points)

### (a) [8]

$$[\,B \mid b\,] = \left[\begin{array}{cccc|c}1&2&0&3&6\\ 2&4&1&8&15\\ 1&2&1&5&9\end{array}\right] \longrightarrow \left[\begin{array}{cccc|c}1&2&0&3&6\\ 0&0&1&2&3\\ 0&0&0&0&0\end{array}\right]$$

**Particular solution**, free variables zero: $x_1 = 6$, $x_3 = 3$.

$$x_p = (6, 0, 3, 0), \qquad Bx_p = 6(1,2,1) + 3(0,1,1) = (6,12,6)+(0,3,3) = (6,15,9)\ ✓$$

$$\boxed{\;x = \begin{bmatrix}6\\0\\3\\0\end{bmatrix} + t\begin{bmatrix}-2\\1\\0\\0\end{bmatrix} + u\begin{bmatrix}-3\\0\\-2\\1\end{bmatrix}\;}$$

*Marking: 3 for $x_p$, 2 for the check against $B$, 3 for the complete set. **A "solution" consisting only of $x_p$ scores 3** — the question said completely.*

### (b) [4]

Need $x_p + ts_2 + us_4 = (1,1,1,1)$. The second coordinate gives $t = 1$ immediately; the fourth gives $u = 1$. Check the rest:

$$(6,0,3,0) + (-2,1,0,0) + (-3,0,-2,1) = (1, 1, 1, 1)\ ✓$$

$$t = u = 1$$

*Marking: 2 for the coefficients, 2 for the verification. Reading them off the free coordinates rather than solving a system is the intended route; do not require it.*

### (c) [4]

$$\left[\begin{array}{cccc|c}1&2&0&3&6\\ 0&0&1&2&3\\ 0&0&0&0&\mathbf{1}\end{array}\right]$$

**The last row reads $0 = 1$: no solution.**

**Q2(c)–(d) predicted it:** $b_1 - b_2 + b_3 = 6 - 15 + 10 = 1 \ne 0$, so $(6,15,10) \notin \mathbf{C}(B)$ — established before any elimination.

*Marking: 2 for the row, 2 for the reference back to the plane equation.*

### (d) [4]

**No — neither is wrong.** $x_p$ is not unique: **any** solution serves, and the recipe "set the free variables to zero" is a convention for making the arithmetic easy, not a property of the answer. Two different $x_p$ differ by an element of $\mathbf{N}(B)$, which the $t$ and $u$ then absorb.

**What is uniquely determined: the solution *set*** — equivalently, the pair (any one particular solution, the subspace $\mathbf{N}(B)$). Their classmate's $x_p$ is in the set above, and the set above is in theirs.

*Marking: 2 for "no", 2 for identifying the solution set as the invariant. **A student who says "yes, one is wrong" has not understood L09 §6 and should be told so explicitly** — this is the most common wrong answer on the paper and it indicates the whole section has been read as a recipe.*

---

## Q5: Structure (16 points)

### (a) [4]

Every column of $AB$ is $A b_j$ (PS 1 Q1(c)), and $Ab_j \in \mathbf{C}(A)$ by definition. $\mathbf{C}(AB)$ is spanned by those columns, and $\mathbf{C}(A)$ is a subspace containing all of them, so it contains their span. $\square$

**Strict:** $A = I_2$, $B = \begin{bmatrix}1&0\\0&0\end{bmatrix}$. Then $\mathbf{C}(AB)$ is the $x$-axis and $\mathbf{C}(A) = \mathbb{R}^2$.

### (b) [4]

If $Ax = 0$ then $(BA)x = B(Ax) = B0 = 0$. $\square$

**Strict:** $A = \begin{bmatrix}1&0\\0&1\end{bmatrix}$, $B = \begin{bmatrix}0&0\\0&0\end{bmatrix}$. Then $\mathbf{N}(A) = \{0\}$ and $\mathbf{N}(BA) = \mathbb{R}^2$.

*Marking (a) and (b): 2 for each proof, 2 for each example.*

### (c) [8]

**($\subseteq$ in the direction $\mathbf{N}(A) \subseteq \mathbf{N}(A^\mathsf{T}A)$)** — this is (b) with $B = A^\mathsf{T}$.

**($\supseteq$)** Suppose $A^\mathsf{T}Ax = 0$. Multiply on the left by $x^\mathsf{T}$:

$$0 = x^\mathsf{T}(A^\mathsf{T}Ax) = (x^\mathsf{T}A^\mathsf{T})(Ax) = (Ax)^\mathsf{T}(Ax) = \lVert Ax\rVert^2$$

using $(Ax)^\mathsf{T} = x^\mathsf{T}A^\mathsf{T}$ — Week 1's L06 §1. **A norm is zero only for the zero vector**, so $Ax = 0$ and $x \in \mathbf{N}(A)$. $\square$

> **This is where "real" is used.** Over $\mathbb{C}$ the statement needs $A^*A$ with the conjugate
> transpose, because $x^\mathsf{T}x$ can vanish for nonzero complex $x$. Worth a marginal note to
> anyone who asks.

**The application.** $A$ is $10^6\times3$ of rank 3. Then $A^\mathsf{T}A$ is $\mathbf{3\times3}$ — small, whatever $m$ is. Rank 3 means $\mathbf{N}(A) = \{0\}$ (L09 §5, full column rank), so by the theorem $\mathbf{N}(A^\mathsf{T}A) = \{0\}$; a square matrix with trivial null space is **invertible** (Week 1's L05 §2, characterisation 3).

**So the normal equations $A^\mathsf{T}A\hat x = A^\mathsf{T}b$ have a unique solution** — a $3\times3$ solve standing in for a million-row problem. *(Which is Week 9, and is why Week 1 bothered to prove $A^\mathsf{T}A$ symmetric.)*

*Marking: 2 for citing (b), 4 for the $\lVert Ax\rVert^2$ argument, 2 for the application. **The step students miss is $x^\mathsf{T}A^\mathsf{T}Ax = \lVert Ax\rVert^2$** — many get to $x^\mathsf{T}A^\mathsf{T}Ax = 0$ and stop, not seeing that it says something. Award 2 of the 4 for reaching that line.*

---

## Grade Distribution Expected

| Band | Score | Description |
|---|---|---|
| Strong | 88–100 | Q1(c)'s "only" proof, Q2(e) with a verified separating vector, Q5(c) complete |
| Solid | 72–87 | Q2–Q4 correct; Q5(c) reaching $\lVert Ax\rVert^2$ but not concluding |
| Passing | 55–71 | Q2 and Q3 mechanically right; conceptual parts thin |
| Concerning | < 55 | **Q2(b) answered from the rref, or Q4(d) answered "yes".** Both say the student is applying recipes without a picture of what a subspace is. Week 3 is entirely conceptual and will be worse. Help Desk before Week 4 |

---

*MATH 241 · Week 2 · PS 2 Solutions · © CSE Department*
