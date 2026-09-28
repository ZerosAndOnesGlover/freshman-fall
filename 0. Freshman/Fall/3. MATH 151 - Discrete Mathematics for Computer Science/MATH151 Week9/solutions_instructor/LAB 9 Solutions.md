# MATH 151 · Week 9
## LAB 9 Solutions — INSTRUCTOR ONLY

*(Revised 2026-09-28: old Exercise 3.3 (naive vs memoised Fibonacci — CS 101 PS 8 B4 and Lab 4 already measure it) and
reflection Q2 are no longer asked; old 3.4 is 3.3. `series` now uses integers and `//` instead of `Fraction` (never taught in
CS 101); since every denominator starts with 1 the results are identical. Expected answer to the float question: integer
arithmetic is exact, while floats round, which is how Binet's formula fails in 3.2.)*

All numeric results below were produced by running the lab code.

---

## Section 1 Solutions — Modelling

### Exercise 1.1 — No two consecutive 1s
$$a_n = a_{n-1}+a_{n-2},\qquad a_0=1,\ a_1=2$$
Values: $1, 2, 3, 5, 8, 13$. This is $F_{n+2}$.

### Exercise 1.2 — Regions from $n$ lines
$$R_n = R_{n-1}+n,\qquad R_0=1$$
Values: $1, 2, 4, 7, 11, 16$. Closed form $1+\frac{n(n+1)}{2}$.

### Exercise 1.3 — Stairs, 1 or 2 at a time
$$s_n = s_{n-1}+s_{n-2},\qquad s_0=1,\ s_1=1$$
Values: $1, 1, 2, 3, 5, 8$ — Fibonacci again, with a different offset.

*Note that 1.1 and 1.3 have the **same recurrence** and differ only in initial conditions. Draw this
out — it is the lesson of the section.*

### Exercise 1.4 — 3¢ and 5¢ stamps, order matters
$$s_n = s_{n-3}+s_{n-5},\qquad s_0=1,\ s_1=s_2=0,\ s_3=1,\ s_4=0$$
Values $s_0..s_8$: $1, 0, 0, 1, 0, 1, 1, 0, 2$.

*The initial conditions are the whole difficulty. $s_0=1$ counts the empty sequence; without it every
term is zero. Expect this to be the most-missed item in Section 1.*

---

## Section 2 Solutions — By Hand

| Exercise | Closed form | Verified values |
|---|---|---|
| 2.1 $a_n=7a_{n-1}-12a_{n-2}$, $a_0{=}2,a_1{=}5$ | $3\cdot3^n-4^n$ | $2, 5, 11, 17, -13, -295$ |
| 2.2 $a_n=4a_{n-1}-4a_{n-2}$, $a_0{=}1,a_1{=}6$ | $(1+2n)2^n$ | $1, 6, 20, 56, 144, 352$ |
| 2.3 $a_n=3a_{n-1}+2$, $a_0{=}4$ | $5\cdot3^n-1$ | $4, 14, 44, 134, 404, 1214$ |

**2.2 is the repeated-root case** ($r^2-4r+4=(r-2)^2$). **2.1 turns negative at $n=4$** — flag this
in the room, because students assume an arithmetic error.

---

## Section 3 Solutions — Python

### Exercise 3.1 — Verification harness *(6 pts)*

All three Section 2 answers report `OK for n = 0..11`. Students who get a `MISMATCH` have almost
always mis-solved the linear system for $A$ and $B$, not mis-typed the closed form — check their
initial-condition substitution.

### Exercise 3.2 — Binet and floating point

**1.** `binet(n)` agrees with $F_n$ throughout the low range, drifting in the final decimals as $n$ grows.

**2. The first failure is at $n = 71$:**

| | |
|---|---|
| `binet(71)` | $308{,}061{,}521{,}170{,}129.7$ |
| true $F_{71}$ | $308{,}061{,}521{,}170{,}129$ |

`round()` therefore returns $308{,}061{,}521{,}170{,}130$ — off by one.

**What went wrong:** nothing mathematical. $\varphi^{71}$ needs more significant digits than a 64-bit
double provides (about 15–16), so $\varphi^n$ and $\psi^n$ are each stored with a relative error that,
once scaled up to $10^{14}$, exceeds $\tfrac12$. **An exact formula is not an exact computation.**

*This is the single most valuable observation in the lab. Students who write "the formula is wrong"
have missed it — the formula is exact; the arithmetic is not.*

**3.** Dropping $\psi^n$ entirely and rounding $\varphi^n/\sqrt5$ also reproduces $F_n$ — and fails at
exactly the same $n=71$, for the same reason. The failure is float precision, not the approximation.

### Exercise 3.3 — Naive vs memoised Fibonacci

| $n$ | 5 | 10 | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|---|
| calls | 15 | 177 | 1973 | 21891 | 242785 | 2692537 |

**2. The call count satisfies $C_n = C_{n-1}+C_{n-2}+1$** — the same recurrence as the function it is
counting, plus one for the current call. Closed form: $C_n = 2F_{n+1}-1$, **verified for all
$n \le 30$**.

**3.** Memoised: **59 calls** at $n=30$ (one per subproblem, plus the misses), against $2{,}692{,}537$
— a factor of about $45{,}000$.

**4.** Naive is $\Theta(\varphi^n)$; memoised is $\Theta(n)$. The $\varphi$ is exactly Lecture 28's
golden ratio: $C_n = 2F_{n+1}-1$ and $F_n \sim \varphi^n/\sqrt5$, so the call count grows like
$\varphi^n$.

*The point to land: memoisation does not make the algorithm cleverer. It stops it recomputing
subproblems, which is precisely "evaluate the recurrence in a sensible order" — dynamic programming.*

### Exercise 3.4 — Formal division

| Function | Coefficients |
|---|---|
| $1/(1-x)$ | 1, 1, 1, 1, 1, 1, 1, 1 |
| $1/(1-2x)$ | 1, 2, 4, 8, 16, 32, 64, 128 |
| $1/(1-x)^2$ | 1, 2, 3, 4, 5, 6, 7, 8 |
| $x/(1-x-x^2)$ | 0, 1, 1, 2, 3, 5, 8, 13 |
| $(1-x)/(1-5x+6x^2)$ | 1, 4, 14, 46, 146, 454, 1394, 4246 |

All five confirmed.

**Why `Fraction` and not `float`:** the coefficients are exact rationals, and each is computed from
*previous* coefficients — so any rounding error is fed back in and amplified at every subsequent step.
With floats the early coefficients look fine and the later ones silently degrade.

---

## Section 4 Solutions — Generating Functions

### Exercise 4.1 — 1¢, 2¢, 5¢

$$G(x)=\frac{1}{1-x}\cdot\frac{1}{1-x^2}\cdot\frac{1}{1-x^5}$$

Coefficient of $x^{10}$: **10**. The combinations, as (5¢, 2¢, 1¢):

$$(0,0,10),(0,1,8),(0,2,6),(0,3,4),(0,4,2),(0,5,0),(1,0,5),(1,1,3),(1,2,1),(2,0,0)$$

### Exercise 4.2 — At most 3 of each, four types

$(1+x+x^2+x^3)^4$; coefficient of $x^5$ is **40**, confirmed by enumerating all $4^4=256$ selections
and counting those summing to 5.

*The unrestricted count would be $\binom83=56$; the cap removes 16.*

---

## Section 5 — Reflection Model Answers

1. **Closed forms numerically.** An exact formula can be an unreliable computation. Binet is exactly
   correct and unusable in float64 past $n=70$; iteration with integers is slower asymptotically but
   exact at every $n$. Choose the representation, not just the formula.

2. **Recomputation.** $F_5$ is computed once for every occurrence of $F_5$ in the call tree of
   `fib_naive(30)` — in the thousands. Memoisation changes nothing about the recurrence; it changes
   the *order and reuse* of evaluation, turning $\Theta(\varphi^n)$ into $\Theta(n)$.

3. **Which method.** The characteristic equation is faster when the recurrence is linear with
   constant coefficients and you want a closed form. Generating functions handle cases it cannot —
   non-constant coefficients, convolution-style recurrences like Catalan, and counting problems with
   restrictions where the generating function *is* the answer and no closed form is wanted.

---

## Checkoff Summary

| Section | Watch for |
|---|---|
| 1 | Initial conditions, especially 1.4's zeros and $s_0=1$ |
| 2 | 2.2 identified as the repeated-root case; 2.1's negative terms not "corrected" |
| 3.1 | Harness reports OK on all three |
| 3.2 | $n=71$ found; explanation blames precision, not the formula |
| 3.3 | Call recurrence identified; connection to $\varphi$ made |
| 3.4 | All five series; `Fraction` rationale given |
| 4 | Both coefficients verified two ways |

---

*MATH 151 · Week 9 · Lab 9 Solutions · Instructor copy — do not distribute*
