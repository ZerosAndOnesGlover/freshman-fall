# MATH 151: Discrete Mathematics for Computer Science
## Problem Set 12: Number Theory
### Released: Friday, Week 12 | Due: Wednesday of Finals Week (11:59 PM)

---

**Instructions:**
- Show every step of the Euclidean algorithm; a bare gcd earns no method marks.
- For every modular inverse, state the gcd condition that guarantees it exists.
- Submit as a single PDF.

**Scoring:** 100 points total, plus an optional 8-point bonus.

> **This is the last problem set of the course.** It is also the most directly useful: everything in
> Part D is running on the machine you submit it from.

---

## Part A — Divisibility and Primes (24 points)

**A1.** *(6 pts)* Prove: if $a\mid b$ and $a\mid c$, then $a\mid(3b-5c)$. State which property of
divisibility you are using.

**A2.** *(6 pts)* Find $q$ and $r$ satisfying the division algorithm for:
(a) $a=-29$, $d=7$ &nbsp;&nbsp; (b) $a=100$, $d=13$ &nbsp;&nbsp; (c) $a=-7$, $d=3$

State why $r$ must be non-negative, and note where this differs from C's `%` operator.

**A3.** *(6 pts)* Factor $1764$, $5040$, and $9797$ into primes.

**A4.** *(6 pts)* Compute $2\cdot3\cdot5\cdot7\cdot11\cdot13 + 1$ and factor it. Then explain why
this does **not** damage Euclid's proof that there are infinitely many primes.

---

## Part B — The Euclidean Algorithm (24 points)

**B1.** *(6 pts)* Compute $\gcd(1071, 462)$, showing every division step.

**B2.** *(6 pts)* Find integers $x, y$ with $1071x + 462y = \gcd(1071,462)$.

**B3.** *(6 pts)* Verify $\gcd(a,b)\cdot\operatorname{lcm}(a,b)=ab$ for $a=252$, $b=198$.

**B4.** *(6 pts)* The Euclidean algorithm runs in $O(\log\min(a,b))$ while trial-division
factorisation takes $\Theta(\sqrt n)$. Explain why the first is *polynomial* in the input size and the
second is *exponential*, and why this gap matters for cryptography.

---

## Part C — Modular Arithmetic (26 points)

**C1.** *(6 pts)* Find $11^{-1} \bmod 26$, or show it does not exist. Then determine whether
$4^{-1} \bmod 6$ exists, and state the general criterion.

**C2.** *(6 pts)* Compute $\varphi(1000)$ using the product formula, showing the prime factorisation
you used.

**C3.** *(7 pts)* Solve the system $x\equiv1\pmod4$, $x\equiv2\pmod5$, $x\equiv3\pmod7$. State the
modulus of the unique solution and verify your answer against all three congruences.

**C4.** *(7 pts)* Compute $7^{100} \bmod 13$ **without** forming $7^{100}$. State which theorem lets
you shortcut the exponent.

---

## Part D — RSA (26 points)

**D1.** *(8 pts)* With $p=11$, $q=13$, $e=7$: compute $n$, $\varphi(n)$, and $d$. Show the extended
Euclidean working for $d$.

**D2.** *(6 pts)* Using your key, encrypt $m=9$ and decrypt the result. Show both modular
exponentiations.

**D3.** *(6 pts)* Prove that RSA decryption inverts encryption, i.e. that $(m^e)^d \equiv m \pmod n$.
Name the theorem you use.

**D4.** *(6 pts)* An attacker knows $n$ and $e$. Explain precisely what they must compute to recover
$d$, why that is believed hard, and why "believed" rather than "proved".

---

## Bonus (8 points — optional)

**Bonus 1.** *(4 pts)* Prove that if $n$ is composite, it has a prime factor $\le\sqrt n$. Explain how
this justifies stopping trial division at $\sqrt n$.

**Bonus 2.** *(4 pts)* Show that $\varphi$ is multiplicative for coprime arguments:
$\gcd(m,n)=1 \implies \varphi(mn)=\varphi(m)\varphi(n)$. Verify for $m=8$, $n=9$.

---

## Grading

| Part | Topic | Points |
|---|---|---|
| A | Divisibility and primes | 24 |
| B | The Euclidean algorithm | 24 |
| C | Modular arithmetic | 26 |
| D | RSA | 26 |
| **Total** | | **100** |
