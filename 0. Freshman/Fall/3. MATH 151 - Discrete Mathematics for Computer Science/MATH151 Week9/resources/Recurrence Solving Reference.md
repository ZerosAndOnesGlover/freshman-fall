# MATH 151 — Recurrence Solving Reference
## Week 9: Recurrence Relations

---

## Anatomy

$$a_n = c_1a_{n-1} + c_2a_{n-2} + f(n), \qquad a_0 = \ldots,\ a_1 = \ldots$$

**A recurrence without initial conditions describes infinitely many sequences.** Always state them.

| Term | Meaning |
|---|---|
| **Order** | How many previous terms appear |
| **Linear** | The $a_i$ appear to the first power, never multiplied together |
| **Constant coefficients** | The $c_i$ do not depend on $n$ |
| **Homogeneous** | $f(n) = 0$ |

| Example | Classification |
|---|---|
| $a_n = 5a_{n-1}-6a_{n-2}$ | linear, order 2, constant, homogeneous |
| $a_n = 2a_{n-1}+3$ | linear, order 1, constant, **non**-homogeneous |
| $a_n = n\,a_{n-1}$ | linear, **not** constant-coefficient |
| $a_n = a_{n-1}^2$ | **not** linear |

---

## Method 1 — Iteration (Unrolling)

Expand until the pattern appears, then **prove by induction**. Unrolling reveals; induction
establishes.

$$T_n = 2T_{n-1}+1,\ T_0=0 \;\Longrightarrow\; T_n = 2^n-1$$

---

## Method 2 — The Characteristic Equation

For **linear, constant-coefficient, homogeneous** recurrences of order 2:

$$a_n = c_1a_{n-1}+c_2a_{n-2} \quad\longrightarrow\quad r^2 - c_1r - c_2 = 0$$

| Roots | General solution |
|---|---|
| Distinct $r_1 \ne r_2$ | $A r_1^n + B r_2^n$ |
| Double root $r$ | $(A + Bn)\,r^n$ |

Then substitute the initial conditions and solve for $A, B$.

### Non-homogeneous

$$a_n = \underbrace{a_n^{(h)}}_{\text{solve homogeneous}} + \underbrace{a_n^{(p)}}_{\text{guess by shape of } f(n)}$$

| $f(n)$ | Try |
|---|---|
| constant | $C$ |
| linear | $Cn+D$ |
| $d^n$, $d$ not a root | $Cd^n$ |
| $d^n$, $d$ a simple root | $Cnd^n$ |
| $d^n$, $d$ a double root | $Cn^2d^n$ |

**Fit the particular solution first, then apply initial conditions to the total.** Reversing this is
the standard error.

---

## Worked Results — All Verified Against Iteration

| Recurrence | Initial | Closed form | First values |
|---|---|---|---|
| $T_n = 2T_{n-1}+1$ | $T_0=0$ | $2^n-1$ | 0, 1, 3, 7, 15 |
| $T_n = 2T_{n-1}+1$ | $T_0=1$ | $2^{n+1}-1$ | 1, 3, 7, 15, 31 |
| $a_n = 5a_{n-1}-6a_{n-2}$ | 1, 4 | $2\cdot3^n-2^n$ | 1, 4, 14, 46, 146 |
| $a_n = 6a_{n-1}-9a_{n-2}$ | 1, 9 | $(1+2n)3^n$ | 1, 9, 45, 189, 729 |
| $a_n = 7a_{n-1}-12a_{n-2}$ | 2, 5 | $3\cdot3^n-4^n$ | 2, 5, 11, 17, −13 |
| $a_n = 4a_{n-1}-4a_{n-2}$ | 1, 6 | $(1+2n)2^n$ | 1, 6, 20, 56, 144 |
| $a_n = a_{n-1}+2a_{n-2}$ | 2, 7 | $3\cdot2^n-(-1)^n$ | 2, 7, 11, 25, 47 |
| $a_n = 2a_{n-1}+3$ | $a_0=1$ | $4\cdot2^n-3$ | 1, 5, 13, 29, 61 |
| $a_n = 3a_{n-1}+2$ | $a_0=4$ | $5\cdot3^n-1$ | 4, 14, 44, 134, 404 |
| $a_n = 3a_{n-1}+2^n$ | $a_0=1$ | $3\cdot3^n-2\cdot2^n$ | 1, 5, 19, 65, 211 |
| $a_n = a_{n-1}+n$ | $a_0=0$ | $n(n+1)/2$ | 0, 1, 3, 6, 10 |
| $R_n = R_{n-1}+n$ | $R_0=1$ | $1+n(n+1)/2$ | 1, 2, 4, 7, 11 |

> Note the $7a_{n-1}-12a_{n-2}$ row **goes negative**. A recurrence with positive coefficients can
> still produce negative terms once the initial conditions put the larger root's coefficient
> negative. Do not use "the numbers look wrong" as a check — use iteration.

---

## Fibonacci

$$F_n = F_{n-1}+F_{n-2},\quad F_0=0,\ F_1=1$$

Characteristic roots $\varphi = \frac{1+\sqrt5}{2} \approx 1.6180$ and
$\psi = \frac{1-\sqrt5}{2} \approx -0.6180$.

$$F_n = \frac{\varphi^n-\psi^n}{\sqrt5} \qquad\textbf{(Binet)}$$

Since $|\psi|<1$, **$F_n$ is the nearest integer to $\varphi^n/\sqrt5$ for $n\ge1$.**

> **A numerical warning, verified.** Evaluated in 64-bit floating point, `round(binet(n))` first
> disagrees with $F_n$ at **$n = 71$**, where it gives $308{,}061{,}521{,}170{,}129.7$ against the
> true $308{,}061{,}521{,}170{,}129$. The formula is exact; double precision is not. An exact formula
> is not automatically a safe computation.

$F_0..F_{10} = 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55$.

---

## Recurrences in Algorithms

| Algorithm | Recurrence | Solution |
|---|---|---|
| Linear search | $T_n = T_{n-1}+1$ | $\Theta(n)$ |
| Binary search | $T_n = T_{n/2}+1$ | $\Theta(\log n)$ |
| Merge sort | $T_n = 2T_{n/2}+n$ | $\Theta(n\log n)$ |
| Naive Fibonacci | $T_n = T_{n-1}+T_{n-2}+1$ | $\Theta(\varphi^n)$ |
| Tower of Hanoi | $T_n = 2T_{n-1}+1$ | $2^n-1$ |

**Naive Fibonacci call counts, verified:**

| $n$ | 5 | 10 | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|---|
| calls | 15 | 177 | 1973 | 21891 | 242785 | 2692537 |

The count itself satisfies $C_n = 2F_{n+1}-1$ — verified for all $n \le 30$. Memoisation reduces it
to $\Theta(n)$.

---

## Common Errors

| ❌ | ✅ |
|---|---|
| Omitting initial conditions | A recurrence alone defines nothing |
| Using $Ar^n+Br^n$ for a double root | It collapses to one constant — use $(A+Bn)r^n$ |
| Applying initial conditions before adding the particular solution | Fit the particular first |
| Trusting a closed form unchecked | Verify against three iterated values, always |
| Assuming positive coefficients give positive terms | See the $7a_{n-1}-12a_{n-2}$ row |
| Treating Binet as safe in floating point | It fails from $n=71$ |

---

*MATH 151 · Week 9 · Reference · © CSE Department*
