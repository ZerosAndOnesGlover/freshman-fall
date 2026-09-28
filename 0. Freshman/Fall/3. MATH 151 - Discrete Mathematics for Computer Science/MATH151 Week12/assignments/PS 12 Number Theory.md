# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 12: Number Theory
### Released: Friday 18 December 2026, 14:00 (after the Friday lecture) | Due: Wednesday 23 December 2026, 17:00 (finals week)

---

**Instructions:**
- Show every step of the Euclidean algorithm; a bare gcd earns no method marks.
- For every modular inverse, state the gcd condition that guarantees it exists.
- Submit as a single PDF.

**Expected time:** about 3 hours. **Scoring:** 100 points total.

> **This is the last problem set of the course.** It is also the most directly useful: everything in
> Part D is running on the machine you submit it from.

---

## Part A — Divisibility and Primes (34 points)

**A1.** *(10 pts)* Prove: if $a\mid b$ and $a\mid c$, then $a\mid(3b-5c)$. State which property of
divisibility you are using.

**A2.** *(12 pts)* Find $q$ and $r$ satisfying the division algorithm for:
(a) $a=-29$, $d=7$ &nbsp;&nbsp; (b) $a=100$, $d=13$ &nbsp;&nbsp; (c) $a=-7$, $d=3$

State why $r$ must be non-negative, and note where this differs from C's `%` operator.

**A3.** *(12 pts)* Compute $2\cdot3\cdot5\cdot7\cdot11\cdot13 + 1$ and factor it. Then explain why
this does **not** damage Euclid's proof that there are infinitely many primes.

---

## Part B — The Euclidean Algorithm (14 points)

**B1.** *(14 pts)* The Euclidean algorithm runs in $O(\log\min(a,b))$ while trial-division
factorisation takes $\Theta(\sqrt n)$. Explain why the first is *polynomial* in the input size and the
second is *exponential*, and why this gap matters for cryptography.

---

## Part C — Modular Arithmetic (38 points)

**C1.** *(12 pts)* Find $7^{-1} \bmod 26$, or show it does not exist. Then determine whether
$4^{-1} \bmod 6$ exists, and state the general criterion.

**C2.** *(12 pts)* Compute $\varphi(1000)$ using the product formula, showing the prime factorisation
you used.

**C3.** *(14 pts)* Compute $7^{100} \bmod 13$ **without** forming $7^{100}$. State which theorem lets
you shortcut the exponent.

---

## Part D — RSA (14 points)

**D1.** *(14 pts)* Prove that RSA decryption inverts encryption, i.e. that $(m^e)^d \equiv m \pmod n$.
Name the theorem you use.

---

## Grading

| Part | Topic | Points |
|---|---|---|
| A | Divisibility and primes | 34 |
| B | The Euclidean algorithm | 14 |
| C | Modular arithmetic | 38 |
| D | RSA | 14 |
| **Total** | | **100** |
