# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 9.2 (L28) — Solving Linear Recurrences: The Characteristic Equation
### Thursday, Week 9

**Date:** Thursday 22 October 2026 · 13:00–13:50 · Week 9

---

## 1. A Guess That Works

Monday solved recurrences by unrolling. That works, but it is ad hoc. For **linear,
constant-coefficient, homogeneous** recurrences there is a complete method.

The idea: guess $a_n = r^n$ and see what $r$ must be. For

$$a_n = c_1 a_{n-1} + c_2 a_{n-2}$$

substituting $a_n = r^n$ and dividing by $r^{n-2}$ gives the **characteristic equation**

$$r^2 = c_1 r + c_2 \qquad\Longleftrightarrow\qquad r^2 - c_1 r - c_2 = 0$$

**Why the guess is reasonable:** the recurrence says "each term is a fixed combination of the
previous two", and geometric sequences are exactly the sequences whose ratio between consecutive
terms is constant. It is not obvious that *all* solutions are combinations of geometric sequences —
that is the theorem.

> **Theorem.** If the characteristic equation has **distinct** roots $r_1 \neq r_2$, then every
> solution has the form
> $$a_n = A r_1^n + B r_2^n$$
> with $A, B$ determined by the initial conditions.

---

## 2. The Method, Step by Step

1. Write the characteristic equation.
2. Find its roots.
3. Write the general solution.
4. Substitute the initial conditions to get a linear system.
5. Solve for the constants.
6. **Check** against a few iterated values.

Step 6 is not optional. It costs thirty seconds and catches every sign error.

### Worked example — distinct roots

$$a_n = 5a_{n-1}-6a_{n-2},\qquad a_0 = 1,\ a_1 = 4$$

**Characteristic equation:** $r^2 - 5r + 6 = 0$, so $(r-2)(r-3)=0$ and $r = 2, 3$.

**General solution:** $a_n = A\,2^n + B\,3^n$.

**Initial conditions:**
$$n=0:\quad A + B = 1$$
$$n=1:\quad 2A + 3B = 4$$

Subtracting twice the first from the second: $B = 2$, hence $A = -1$.

$$\boxed{a_n = 2\cdot3^n - 2^n}$$

**Check:** iterating the recurrence gives $1, 4, 14, 46, 146, 454, 1394, 4246$; the closed form gives
the same values. *(Verified for $n \le 11$.)*

---

## 3. Repeated Roots

If the characteristic equation has a **double root** $r$, then $A r^n + B r^n$ collapses to a single
constant times $r^n$ — one constant is not enough to satisfy two initial conditions.

> **Theorem.** With a double root $r$, the general solution is
> $$a_n = (A + Bn)\,r^n$$

### Worked example

$$a_n = 6a_{n-1}-9a_{n-2},\qquad a_0 = 1,\ a_1 = 9$$

**Characteristic equation:** $r^2-6r+9 = (r-3)^2 = 0$, so $r = 3$ twice.

**General solution:** $a_n = (A+Bn)3^n$.

$$n=0:\quad A = 1 \qquad n=1:\quad (1+B)\cdot3 = 9 \;\Rightarrow\; B = 2$$

$$\boxed{a_n = (1+2n)\,3^n}$$

**Check:** $1, 9, 45, 189, 729, \ldots$ from both the recurrence and the formula. *(Verified for
$n \le 11$.)*

---

## 4. Fibonacci in Closed Form

$$F_n = F_{n-1}+F_{n-2},\qquad F_0 = 0,\ F_1 = 1$$

**Characteristic equation:** $r^2 - r - 1 = 0$, with roots

$$\varphi = \frac{1+\sqrt5}{2} \approx 1.6180 \qquad \psi = \frac{1-\sqrt5}{2} \approx -0.6180$$

$\varphi$ is the **golden ratio**. Solving $A + B = 0$ and $A\varphi + B\psi = 1$ gives
$A = 1/\sqrt5$, $B = -1/\sqrt5$:

$$\boxed{F_n = \frac{\varphi^n - \psi^n}{\sqrt5}} \qquad \textbf{(Binet's formula)}$$

**Verified:** matches the integer Fibonacci sequence for every $n \le 30$; $F_{30} = 832040$ from
both.

Two things are worth pausing on.

**It is astonishing that this is an integer.** Every $F_n$ is a whole number, yet the formula is
built entirely from irrationals. The irrational parts cancel exactly — a fact you can prove, but
never quite stop finding surprising.

**$|\psi| \approx 0.618 < 1$, so $\psi^n \to 0$.** For $n \geq 1$, $F_n$ is simply the **nearest
integer to $\varphi^n/\sqrt5$**. This is why Fibonacci growth is exponential with base $\varphi$,
and it is where the $\Theta(\varphi^n)$ in Monday's algorithm table came from.

---

## 5. Non-Homogeneous Recurrences

When there is an extra term — $a_n = c_1a_{n-1}+c_2a_{n-2}+f(n)$ — the solution splits:

$$a_n = \underbrace{a_n^{(h)}}_{\text{homogeneous solution}} + \underbrace{a_n^{(p)}}_{\text{particular solution}}$$

Solve the homogeneous part as above, then guess a particular solution matching the shape of $f(n)$:

| $f(n)$ | Try |
|---|---|
| constant | constant $C$ |
| linear in $n$ | $Cn + D$ |
| $d^n$ ($d$ not a root) | $Cd^n$ |
| $d^n$ ($d$ **is** a root) | $Cn\,d^n$ |

**Fit the particular solution first**, then use the initial conditions on the *total*. Reversing the
order is the standard error and produces the wrong constants.

### Worked example

$$a_n = 2a_{n-1}+3,\qquad a_0 = 1$$

Homogeneous: $r = 2$, so $a_n^{(h)} = A\,2^n$. Particular: try $a_n^{(p)} = C$; then
$C = 2C+3$ gives $C = -3$.

$$a_n = A\,2^n - 3, \qquad a_0 = 1 \Rightarrow A - 3 = 1 \Rightarrow A = 4$$

$$\boxed{a_n = 4\cdot2^n - 3}$$

**Check:** $1, 5, 13, 29, 61, \ldots$ from both. *(Verified for $n \le 11$; this is the same answer
Monday obtained by unrolling.)*

---

## 6. Summary

| Case | General solution |
|---|---|
| Distinct roots $r_1 \ne r_2$ | $A r_1^n + B r_2^n$ |
| Double root $r$ | $(A + Bn)r^n$ |
| Non-homogeneous | homogeneous $+$ particular |

| Recurrence | Closed form |
|---|---|
| $a_n = 5a_{n-1}-6a_{n-2}$, $a_0{=}1,a_1{=}4$ | $2\cdot3^n - 2^n$ |
| $a_n = 6a_{n-1}-9a_{n-2}$, $a_0{=}1,a_1{=}9$ | $(1+2n)3^n$ |
| $F_n = F_{n-1}+F_{n-2}$ | $(\varphi^n-\psi^n)/\sqrt5$ |
| $a_n = 2a_{n-1}+3$, $a_0{=}1$ | $4\cdot2^n-3$ |

**Always verify the closed form against three or four iterated values.**

---

## 7. End-of-Lecture Exercises

1. Solve $a_n = 7a_{n-1}-12a_{n-2}$, $a_0 = 2$, $a_1 = 5$.

2. Solve $a_n = 4a_{n-1}-4a_{n-2}$, $a_0 = 1$, $a_1 = 6$. *(Note the repeated root.)*

3. Solve $a_n = a_{n-1}+2a_{n-2}$, $a_0 = 2$, $a_1 = 7$.

4. Use Binet's formula to compute $F_{20}$, and check against iteration.

5. Solve $a_n = 3a_{n-1}+2^n$, $a_0 = 1$. *(Note $2$ is not a root of the characteristic equation.)*

6. **(Stretch.)** Solve $a_n = 4a_{n-1}-4a_{n-2}+2^n$, where $2$ **is** a double root. Explain why the particular guess must be $Cn^2 2^n$ rather than $C2^n$ or $Cn2^n$.

---

## Reading

- **Rosen, 8e §8.2** — Solving linear recurrence relations
- **Epp, 5e §5.8** — Second-order linear homogeneous recurrences
- **Levin, 3e §2.4** — Characteristic roots

*Next: Lecture 9.3 — Generating Functions*
