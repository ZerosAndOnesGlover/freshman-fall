# MATH 151 — Problem Set 12 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

**Total: 100 points**, plus 8 bonus. All values verified computationally.

---

## Part A — Divisibility and Primes

### A1. *(6 pts)*
Given $a\mid b$ and $a\mid c$, write $b=ak_1$ and $c=ak_2$. Then

$$3b-5c = 3ak_1 - 5ak_2 = a(3k_1-5k_2)$$

and $3k_1-5k_2\in\mathbb{Z}$, so $a\mid(3b-5c)$. ∎

**Property used: linearity** — $a\mid b$ and $a\mid c$ imply $a\mid(bx+cy)$ for all integers $x,y$.

*Marking: 4 for the proof, 2 for naming linearity. Producing the explicit witness $3k_1-5k_2$ is the
substance; students who wave at "obviously divisible" get 2.*

---

### A2. *(6 pts)*

| $a$ | $d$ | $q$ | $r$ |
|---|---|---|---|
| $-29$ | 7 | $-5$ | **6** |
| 100 | 13 | 7 | 9 |
| $-7$ | 3 | $-3$ | **2** |

**Why $r\ge0$:** the theorem *defines* $r$ by $0\le r<d$, and that constraint is exactly what makes
$(q,r)$ unique — without it, $-29 = 7(-4)-1$ would be equally valid.

**Difference from C:** C's `%` takes the sign of the dividend, so `-29 % 7` is `-1` and `-7 % 3` is
`-1`. Python's `%` matches the mathematical convention. **Code ported between the two silently
changes behaviour on negative inputs.**

*Marking: 3 for the values, 1 for the uniqueness point, 2 for the C contrast.*

---

### A3. *(6 pts, 2 each)*
$$1764 = 2^2\cdot3^2\cdot7^2 \qquad 5040 = 2^4\cdot3^2\cdot5\cdot7 \qquad 9797 = 97\cdot101$$

*(All verified. $5040=7!$, worth remarking. $9797$ is the discriminator — students who stop trial
division too early call it prime; it needs testing to $\sqrt{9797}\approx99$.)*

---

### A4. *(6 pts)*
$$2\cdot3\cdot5\cdot7\cdot11\cdot13 + 1 = 30030+1 = 30031 = \mathbf{59\times509}$$

**Composite** — verified.

**Why Euclid's proof survives:** the proof never claims $N=\prod p_i+1$ is prime. It claims $N$ has
**some** prime factor, and that this factor cannot be any $p_i$ — because $p_i$ divides
$\prod p_j$, so if it also divided $N$ it would divide $N-\prod p_j = 1$.

Here that new prime is $59$ (and $509$), neither of which is among $\{2,3,5,7,11,13\}$. **The
conclusion — a prime outside the list exists — holds exactly as the proof requires.**

*Marking: 2 for the factorisation, 4 for the explanation. This is the most commonly misremembered
proof in the course; award the 4 only for an argument that identifies what the proof actually
asserts.*

---

## Part B — The Euclidean Algorithm

### B1. *(6 pts)*
$$
\begin{aligned}
1071 &= 2(462) + 147\\
462 &= 3(147) + 21\\
147 &= 7(21) + 0
\end{aligned}
$$
$$\gcd(1071,462) = \mathbf{21}$$

*Marking: 4 for the steps, 2 for the answer. A bare "21" earns 2 — the question demands the steps.*

---

### B2. *(6 pts)*
Back-substituting: $21 = 462 - 3(147)$ and $147 = 1071 - 2(462)$, so

$$21 = 462 - 3\big(1071-2(462)\big) = 7(462) - 3(1071)$$

$$\boxed{x=-3,\quad y=7} \qquad -3(1071)+7(462) = -3213+3234 = 21\ \checkmark$$

*(Verified.)*

---

### B3. *(6 pts)*
$\gcd(252,198)=18$ (trace in the Week 12 reference). Then

$$\operatorname{lcm}(252,198) = \frac{252\times198}{18} = \frac{49896}{18} = 2772$$

$$\gcd\cdot\operatorname{lcm} = 18\times2772 = 49896 = 252\times198\ \checkmark$$

---

### B4. *(6 pts)*
An integer $n$ is written in $\Theta(\log n)$ digits — **that is the input size.**

- **Euclid** costs $O(\log\min(a,b))$ divisions, i.e. **linear in the number of digits** —
  polynomial in the input size.
- **Trial division** costs $\Theta(\sqrt n)$ divisions. Writing $L=\log_{10}n$ for the digit count,
  $\sqrt n = 10^{L/2}$ — **exponential in the input size.**

**Why it matters:** RSA needs both. Key generation and decryption use gcd and modular
exponentiation, both polynomial, so the legitimate parties work in microseconds. Breaking the key
requires factoring, exponential, so the attacker does not. **The entire cryptosystem is this gap.**

A 2048-bit modulus has about 617 digits; trial division would need roughly $10^{308}$ operations.

*Marking: 2 for identifying digit count as the input size, 2 for each cost analysis. Answers saying
"$\sqrt n$ is smaller than $n$ so it's fast" have missed the question entirely — 1 mark.*

---

## Part C — Modular Arithmetic

### C1. *(6 pts)*
$\gcd(11,26)=1$, so the inverse exists. Extended Euclid gives $11(19) = 209 = 8(26)+1$, so

$$11^{-1} \equiv \mathbf{19} \pmod{26}$$

$4^{-1}\bmod6$ **does not exist**: $\gcd(4,6)=2\ne1$.

**Criterion:** $a^{-1}\bmod m$ exists **iff** $\gcd(a,m)=1$.

*Marking: 3 for 19 with verification, 2 for the non-existence, 1 for the criterion.*

---

### C2. *(6 pts)*
$1000 = 2^3\cdot5^3$, so

$$\varphi(1000) = 1000\left(1-\tfrac12\right)\left(1-\tfrac15\right) = 1000\cdot\tfrac12\cdot\tfrac45 = \mathbf{400}$$

*(Verified by counting all 400 integers in $[1,1000]$ coprime to 1000.)*

*Marking: 2 factorisation, 3 formula, 1 arithmetic. Only **distinct** primes enter the product —
using $2^3$ and $5^3$ as separate factors is the standard error.*

---

### C3. *(7 pts)*
Moduli $4, 5, 7$ are pairwise coprime, so a unique solution exists modulo $4\cdot5\cdot7 = 140$.

$$x \equiv \mathbf{17} \pmod{140}$$

**Verification:** $17 = 4(4)+1$ ✓ &nbsp; $17 = 3(5)+2$ ✓ &nbsp; $17 = 2(7)+3$ ✓

*(Confirmed by brute-force search over $0..139$.)*

*Marking: 4 method, 1 answer, 2 verification against all three congruences — which the question
explicitly requires.*

---

### C4. *(7 pts)*
13 is prime and $13\nmid7$, so **Fermat's Little Theorem** gives $7^{12}\equiv1\pmod{13}$.

Since $100 = 8(12) + 4$:

$$7^{100} = \left(7^{12}\right)^{8}\cdot7^{4} \equiv 1^8\cdot7^4 = 7^4 \pmod{13}$$

$7^2 = 49 \equiv 10$, so $7^4 \equiv 10^2 = 100 \equiv \mathbf 9 \pmod{13}$.

*(Verified: $7^{100}\bmod13 = 9$.)*

*Marking: 3 for invoking Fermat, 2 for reducing the exponent mod 12, 2 for the arithmetic. Computing
$7^{100}$ directly earns 2 — correct but not what was asked.*

---

## Part D — RSA

### D1. *(8 pts)*
$$n = 11\times13 = \mathbf{143} \qquad \varphi(n) = 10\times12 = \mathbf{120}$$

$\gcd(7,120)=1$, so $d=7^{-1}\bmod120$ exists. Extended Euclid:

$$120 = 17(7)+1 \quad\Longrightarrow\quad 1 = 120 - 17(7)$$

so $-17(7)\equiv1\pmod{120}$ and $d \equiv -17 \equiv \mathbf{103} \pmod{120}$.

**Check:** $7\times103 = 721 = 6(120)+1$ ✓

*Marking: 2 each for $n$ and $\varphi(n)$, 4 for $d$ with working. The $-17\to103$ normalisation is
where marks are lost.*

---

### D2. *(6 pts)*
**Encrypt:** $c = 9^7 \bmod 143$. By repeated squaring: $9^2=81$, $9^4=81^2=6561\equiv126$,
so $9^7 = 9^4\cdot9^2\cdot9 \equiv 126\cdot81\cdot9 \equiv \mathbf{48}$.

**Decrypt:** $48^{103} \bmod 143 = \mathbf 9$ ✓

*(Both verified.)*

*Marking: 3 each. Students should reduce at every step; anyone who wrote out $9^7 = 4782969$ before
reducing should be warned that the same approach on a real key is impossible.*

---

### D3. *(6 pts)*
Since $ed\equiv1\pmod{\varphi(n)}$, write $ed = 1+k\varphi(n)$ for some integer $k$. Then for $m$
coprime to $n$:

$$(m^e)^d = m^{ed} = m^{1+k\varphi(n)} = m\cdot\left(m^{\varphi(n)}\right)^{k} \equiv m\cdot1^{k} = m \pmod n$$

**The theorem used is Euler's**: $m^{\varphi(n)}\equiv1\pmod n$ whenever $\gcd(m,n)=1$. ∎

*(For the remaining $m$ sharing a factor with $n$, the result still holds via CRT applied mod $p$ and
mod $q$ separately — mention it, but it is not required for full marks.)*

*Marking: 4 for the derivation, 2 for naming Euler's theorem.*

---

### D4. *(6 pts)*
The attacker has $n$ and $e$, and wants $d = e^{-1}\bmod\varphi(n)$. Computing an inverse is easy —
**but it requires $\varphi(n)$**, and $\varphi(n)=(p-1)(q-1)$ requires $p$ and $q$. So the attacker
must **factor $n$**.

**Why believed hard:** the best known classical algorithms (general number field sieve) are
sub-exponential but still infeasible at 2048 bits, and factoring has resisted serious effort since
antiquity.

**Why "believed" and not "proved":** no lower bound has ever been established. Proving factoring
requires super-polynomial time would settle deep open questions in complexity theory. Moreover
**Shor's algorithm factors in polynomial time on a quantum computer**, so the hardness is not
absolute — it is contingent on the machine model.

*Marking: 3 for the chain $d\leftarrow\varphi(n)\leftarrow p,q\leftarrow$ factoring; 3 for the
believed-versus-proved distinction with a reason.*

---

## Bonus Solutions

### Bonus 1. *(4 pts)*
Let $n$ be composite, so $n = ab$ with $1<a\le b<n$. Then $a^2 \le ab = n$, giving $a\le\sqrt n$.
Now $a>1$, so $a$ has a prime divisor $p\le a\le\sqrt n$, and $p\mid a\mid n$. ∎

**Justifying trial division:** if no prime $\le\sqrt n$ divides $n$, then by the contrapositive $n$
is not composite, hence prime. Testing beyond $\sqrt n$ is therefore redundant — any factor above it
has already been found as the partner of one below.

*Marking: 3 for the proof, 1 for the algorithmic consequence.*

---

### Bonus 2. *(4 pts)*
**Verification for $m=8$, $n=9$** (coprime): $\varphi(8)=4$, $\varphi(9)=6$, and $\varphi(72)=24 =
4\times6$ ✓ *(all confirmed by direct count).*

**Proof sketch.** By CRT the map $x \mapsto (x\bmod m,\ x\bmod n)$ is a bijection
$\mathbb{Z}_{mn}\to\mathbb{Z}_m\times\mathbb{Z}_n$. Moreover $\gcd(x,mn)=1$ **iff** $\gcd(x,m)=1$ and
$\gcd(x,n)=1$. So the bijection restricts to a bijection between the units of $\mathbb{Z}_{mn}$ and
the pairs of units, giving $\varphi(mn)=\varphi(m)\varphi(n)$. ∎

*Marking: 1 verification, 3 proof. Full credit requires the CRT bijection; hand-waving at "counting
coprime pairs" earns 2. Note coprimality of $m,n$ is essential — $\varphi(4)\varphi(6)=2\cdot2=4$ but
$\varphi(24)=8$.*

---

*MATH 151 · Week 12 · PS 12 Solutions · Instructor copy — do not distribute*
