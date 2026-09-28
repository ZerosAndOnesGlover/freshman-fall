# MATH 151 · Problem Set 9 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

**Total: 100 points.** Every closed form below was verified against iteration.

---

> *Revised 2026-09-28: cut from 17 problems to 8 problems with 11 parts. New → old: A1 = A4, 12 · B1 = B1, 12 · B2 = B2, 12 · C1 = C3, 12 · C2 = C5, 16 · D1 = D1, 8 · D2 = D2, 16 · D3 = D5, 12. The point values in the headings and marking lines below are the old ones; scale each marking line in proportion.*
>
> *Why items were dropped:*
> - *A1, A2 and A3 are Lab 9 Exercises 1.1, 1.4 and 1.2.*
> - *B3, C1 and C2 are Lab 9 Exercises 2.3, 2.1 and 2.2.*
> - *C4 is Lab 9 Exercise 3.2.*
> - *D3 and D4 are Lab 9 Exercises 4.1 and 4.2.*


## Part A — Modelling with Recurrences

### A1. *(6 pts)* No two consecutive 1s

A valid string of length $n$ either ends in `0` (preceded by any valid string of length $n-1$) or
ends in `01` — i.e. ends in `1`, which forces a `0` before it, preceded by any valid string of length
$n-2$.

$$a_n = a_{n-1}+a_{n-2},\qquad a_0=1,\ a_1=2$$

**Values:** $1, 2, 3, 5, 8, 13$ — the **Fibonacci numbers**, shifted: $a_n = F_{n+2}$.

*Marking: 3 for the recurrence, 2 for correct initial conditions, 1 for identifying Fibonacci.
$a_0=1$ (the empty string) is the one students get wrong; accept $a_1=2, a_2=3$ as the base instead.*

---

### A2. *(6 pts)* 3¢ and 5¢ stamps, order matters

A sequence totalling $n$ ends with either a 3¢ or a 5¢ stamp:

$$s_n = s_{n-3}+s_{n-5},\qquad s_0=1,\ s_1=s_2=0,\ s_3=1,\ s_4=0$$

**Values $s_0..s_8$:** $1, 0, 0, 1, 0, 1, 1, 0, 2$

*(Verified by direct computation. $s_8 = 2$: the sequences $3{+}5$ and $5{+}3$ — distinct because
order matters.)*

*Marking: 3 for the recurrence, 3 for the initial conditions. **The initial conditions are the whole
difficulty here** — several are zero, and $s_0=1$ (the empty sequence) is essential or everything
collapses to 0. A student with the right recurrence and $s_0=0$ gets 3.*

---

### A3. *(6 pts)* Regions from $n$ lines

The $n$-th line crosses the previous $n-1$ lines in $n-1$ distinct points, which cut it into $n$
segments; each segment splits one existing region in two.

$$R_n = R_{n-1}+n,\qquad R_0=1$$

Unrolling: $R_n = 1 + (1+2+\cdots+n) = 1 + \dfrac{n(n+1)}{2}$.

**Verified:** $1, 2, 4, 7, 11, 16, 22, 29$ from both recurrence and formula.

*Marking: 3 for the recurrence with justification, 3 for the closed form. The justification — why the
$n$-th line adds exactly $n$ regions — is the mathematical content; a bare recurrence gets 1.*

---

### A4. *(6 pts, 1.5 each)*

| | Order | Linear? | Constant coeff? | Homogeneous? |
|---|---|---|---|---|
| (a) $a_n=3a_{n-1}-a_{n-3}$ | 3 | yes | yes | yes |
| (b) $a_n=n\,a_{n-1}$ | 1 | yes | **no** | yes |
| (c) $a_n=a_{n-1}^2$ | 1 | **no** | — | — |
| (d) $a_n=a_{n-1}+a_{n-2}+n^2$ | 2 | yes | yes | **no** |

*(a) is order 3 despite $a_{n-2}$ being absent — order is the largest lag, not the number of terms.*

---

## Part B — Solving by Iteration

### B1. *(5 pts)* $a_n=a_{n-1}+n$, $a_0=0$

$$a_n = 0 + 1 + 2 + \cdots + n = \frac{n(n+1)}{2}$$

the **triangular numbers**: $0, 1, 3, 6, 10, 15, 21, 28$ *(verified)*.

**Induction.** Base $a_0=0=\frac{0\cdot1}{2}$ ✓. Step: assuming $a_{n-1}=\frac{(n-1)n}{2}$,
$$a_n = \frac{(n-1)n}{2}+n = \frac{n^2-n+2n}{2} = \frac{n(n+1)}{2}\ \checkmark$$

*Marking: 2 unrolling, 1 closed form, 2 induction. The induction is required by the question.*

---

### B2. *(5 pts)* $T_n=2T_{n-1}+1$, $T_0=1$

$$T_n = 2^{n+1}-1$$

**Verified:** $1, 3, 7, 15, 31, 63, 127, 255$.

**Why it differs from Hanoi's $2^n-1$:** the recurrence is identical; only the initial condition moved.
Unrolling gives $T_n = 2^nT_0 + (2^n-1)$, so $T_0=0$ yields $2^n-1$ and $T_0=1$ yields
$2^n+2^n-1 = 2^{n+1}-1$. **The recurrence fixes the shape of the solution; the initial condition
selects which member of that family you get.**

*Marking: 3 for the closed form, 2 for the explanation. That explanation is the point of the problem.*

---

### B3. *(6 pts)* $a_n=3a_{n-1}+2$, $a_0=4$

**By iteration:** $a_n = 3^n\cdot4 + 2(3^{n-1}+\cdots+1) = 4\cdot3^n + 2\cdot\frac{3^n-1}{2} = 5\cdot3^n-1$.

**By characteristic equation:** homogeneous root $r=3$ gives $A3^n$; particular constant $C$ satisfies
$C=3C+2$, so $C=-1$. Then $a_0=4$ gives $A-1=4$, $A=5$.

$$\boxed{a_n = 5\cdot3^n-1}$$

**Verified:** $4, 14, 44, 134, 404, 1214, 3644, 10934$ from both.

*Marking: 3 per method. Both must reach the same answer; a student getting different results and not
noticing loses 2 more.*

---

## Part C — The Characteristic Equation

### C1. *(6 pts)* $a_n=7a_{n-1}-12a_{n-2}$, $a_0=2$, $a_1=5$

$r^2-7r+12=(r-3)(r-4)=0$, so $r=3,4$ and $a_n=A3^n+B4^n$.

$A+B=2$, $3A+4B=5$ ⟹ $B=-1$, $A=3$.

$$\boxed{a_n = 3\cdot3^n-4^n}$$

**Verified:** $2, 5, 11, 17, -13, -295, -1909, -9823$.

> **Note the sequence goes negative from $n=4$.** Positive coefficients do not guarantee positive
> terms — the $-4^n$ eventually dominates. Students who "correct" their arithmetic because the
> numbers look wrong should be told to check by iteration instead.

---

### C2. *(6 pts)* $a_n=4a_{n-1}-4a_{n-2}$, $a_0=1$, $a_1=6$

$r^2-4r+4=(r-2)^2=0$ — a **double root** $r=2$, so the repeated-root case applies and the solution is
$(A+Bn)2^n$, not $A2^n+B2^n$ (which has only one free constant and cannot meet two conditions).

$A=1$; $(1+B)2=6$ ⟹ $B=2$.

$$\boxed{a_n=(1+2n)2^n}$$

**Verified:** $1, 6, 20, 56, 144, 352, 832, 1920$.

*Marking: 2 for identifying the repeated root, 2 for the $(A+Bn)r^n$ form, 2 for the constants. The
question explicitly asks which case applies — no marks for the form without naming it.*

---

### C3. *(6 pts)* $a_n=a_{n-1}+2a_{n-2}$, $a_0=2$, $a_1=7$

$r^2-r-2=(r-2)(r+1)=0$, so $r=2,-1$.

$A+B=2$, $2A-B=7$ ⟹ $A=3$, $B=-1$.

$$\boxed{a_n=3\cdot2^n-(-1)^n}$$

**Verified:** $2, 7, 11, 25, 47, 97, 191, 385$.

---

### C4. *(6 pts)* $F_{20}$ by Binet

$$F_{20}=\frac{\varphi^{20}-\psi^{20}}{\sqrt5} = \mathbf{6765}$$

*(Computed: $6765.000000000005$ in double precision — see the note below.)*

**Why $F_n$ is the nearest integer to $\varphi^n/\sqrt5$:** $|\psi| = \frac{\sqrt5-1}{2} \approx 0.618 < 1$,
so $|\psi^n|$ shrinks geometrically and $\left|\psi^n/\sqrt5\right| < \tfrac12$ for all $n \ge 1$.
Dropping it therefore moves the value by less than half, and rounding recovers $F_n$ exactly.

*Marking: 3 for the value, 3 for the argument — which must quantify "less than a half", not merely
say "$\psi^n$ is small".*

*Worth mentioning in review: in float64 this **fails from $n=71$**, where the formula gives
$308{,}061{,}521{,}170{,}129.7$ against the true $308{,}061{,}521{,}170{,}129$. Exact mathematics,
inexact arithmetic.*

---

### C5. *(6 pts)* $a_n=3a_{n-1}+2^n$, $a_0=1$

Homogeneous root $r=3$ ⟹ $A3^n$. Since $2$ **is not** a root of $r-3=0$, the guess $C2^n$ is
legitimate — it does not duplicate a homogeneous solution, so it can supply a genuinely new degree of
freedom.

$C2^n = 3C2^{n-1}+2^n$ ⟹ $2C = 3C+2$ ⟹ $C=-2$. Then $a_0=1$ gives $A-2=1$, $A=3$.

$$\boxed{a_n=3\cdot3^n-2\cdot2^n}$$

**Verified:** $1, 5, 19, 65, 211, 665, 2059, 6305$.

*Marking: 4 for the solution, 2 for the legitimacy explanation. Had $2$ been a root, $C2^n$ would
satisfy the homogeneous equation and give $0=2^n$ — the reason the rule says multiply by $n$.*

---

## Part D — Generating Functions

### D1. *(5 pts)* $\dfrac{1}{1-3x}$

Coefficients $1, 3, 9, 27, 81, 243$ — the sequence $a_n = 3^n$ *(verified by formal division)*.

---

### D2. *(6 pts)* GF for $a_n=a_{n-1}+2a_{n-2}$, $a_0=2$, $a_1=7$

Multiply by $x^n$, sum from $n\ge2$:

$$G(x)-2-7x = x\big(G(x)-2\big)+2x^2G(x)$$
$$G(x)\left(1-x-2x^2\right) = 2+5x$$
$$\boxed{G(x)=\frac{2+5x}{1-x-2x^2}}$$

**Verified:** coefficients $2, 7, 11, 25, 47, 97, 191, 385$ — matching C3 (new C1) exactly.

*Marking: 4 for the derivation, 2 for the coefficient check. The commonest error is dropping the
$-2$ inside $x(G(x)-2)$ — the shifted sum starts at $n=2$, so $a_0$ must be removed.*

---

### D3. *(7 pts)* Coins of 1¢, 2¢, 5¢

$$G(x)=\frac{1}{1-x}\cdot\frac{1}{1-x^2}\cdot\frac{1}{1-x^5}$$

Coefficient of $x^{10}$: **10**.

**The ten combinations** (as counts of 5¢, 2¢, 1¢):

$$(0,0,10),(0,1,8),(0,2,6),(0,3,4),(0,4,2),(0,5,0),(1,0,5),(1,1,3),(1,2,1),(2,0,0)$$

*Marking: 3 for the generating function, 2 for the coefficient, 2 for a complete listing. A listing
with 9 or 11 entries indicates a missed or duplicated case — the systematic order above prevents it.*

---

### D4. *(6 pts)* At most 3 of each of four types

$$G(x)=\left(1+x+x^2+x^3\right)^4$$

Coefficient of $x^5$: **40** *(verified by brute-force enumeration over all $4^4$ selections)*.

*Marking: 3 for the generating function, 3 for the coefficient. Answering $\binom{8}{3}=56$ — the
unrestricted count — earns 1: it ignores the "at most 3" cap, which excludes the 16 selections using
4 or 5 of one type.*

---

### D5. *(6 pts)* Formal power series

A **formal** power series is an algebraic object whose defining data is its sequence of coefficients.
$x$ is an indeterminate, never a number; the series is never evaluated.

**Why convergence is irrelevant:** every operation used — addition, multiplication, formal division,
shifting — is *defined coefficient-wise* and produces each output coefficient from finitely many
input coefficients. No limit is ever taken, so there is nothing to converge. This is why
$\frac{1}{1-x}$ is legitimate despite the series diverging for every $|x|\ge1$.

**A legitimate operation:** multiplication, defined by
$\left(\sum a_nx^n\right)\left(\sum b_nx^n\right)=\sum_n\left(\sum_{k=0}^n a_kb_{n-k}\right)x^n$,
where each coefficient is a **finite** sum.

*(Also acceptable: formal differentiation, or division by a series with non-zero constant term.)*

*Marking: 3 for the definition, 3 for the finiteness argument. "We just don't care about convergence"
earns 1 — the question asks why we are entitled not to.*

---

*MATH 151 · Week 9 · PS 9 Solutions · Instructor copy — do not distribute*
