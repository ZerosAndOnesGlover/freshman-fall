# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 12.2 (L37) — Modular Arithmetic, the GCD, and RSA
### Thursday, Week 12

**Date:** Thursday 17 December 2026 · 13:00–13:50 · Week 12

---

## 1. Congruence

> **Definition.** $a \equiv b \pmod m$ means $m \mid (a-b)$.

Equivalently, $a$ and $b$ leave the same remainder on division by $m$.

**This is Week 6's material returning.** Congruence mod $m$ is an **equivalence relation** —
reflexive, symmetric, transitive — and its equivalence classes are the $m$ residue classes
$[0],[1],\ldots,[m-1]$, partitioning $\mathbb{Z}$ exactly as Week 6 promised. The set of classes is
written $\mathbb{Z}_m$.

**Congruences respect arithmetic.** If $a\equiv b$ and $c\equiv d \pmod m$, then

$$a+c\equiv b+d, \qquad a-c\equiv b-d, \qquad ac\equiv bd \pmod m$$

so you may reduce at any point. Computing $7^{100} \bmod 13$ never requires forming $7^{100}$.

> **Division does not work.** $6\equiv 0 \pmod 6$ and $2\cdot3\equiv0$, yet neither $2$ nor $3$ is
> $\equiv0$. Cancelling requires an inverse, and §3 says exactly when one exists.

---

## 2. The Euclidean Algorithm

> $\gcd(a,b) = \gcd(b,\ a \bmod b)$, with $\gcd(a,0)=a$.

**Why:** any common divisor of $a$ and $b$ divides $a-qb = r$ by linearity (Monday), and conversely.
So the pairs $(a,b)$ and $(b,r)$ have identical common divisors.

**Verified trace for $\gcd(252,198)$:**

$$
\begin{aligned}
252 &= 1\cdot198 + 54\\
198 &= 3\cdot54 + 36\\
54 &= 1\cdot36 + 18\\
36 &= 2\cdot18 + 0
\end{aligned}
$$

**$\gcd = 18$** — the last non-zero remainder.

**It is fast.** The remainder at least halves every two steps, so the cost is $O(\log \min(a,b))$ —
*polynomial in the number of digits*, unlike Monday's trial division. This is why cryptography can
compute gcds of 2048-bit numbers instantly while being unable to factor them.

**Also:** $\gcd(a,b)\cdot\operatorname{lcm}(a,b) = ab$. Verified: $\gcd(252,198)=18$,
$\operatorname{lcm}=2772$, and $18\times2772 = 49896 = 252\times198$ ✓

---

## 3. Bézout and Modular Inverses

> **Bézout's identity.** There exist integers $x,y$ with $ax+by=\gcd(a,b)$.

The **extended** Euclidean algorithm produces them by running the trace backwards.

**Verified:** $4\cdot252 + (-5)\cdot198 = 1008 - 990 = 18 = \gcd(252,198)$ ✓

> **Theorem.** $a$ has a multiplicative inverse mod $m$ **iff** $\gcd(a,m)=1$.

**Why:** if $\gcd(a,m)=1$, Bézout gives $ax+my=1$, so $ax\equiv1\pmod m$ and $x$ is the inverse.
Conversely an inverse gives $ax-1=my$, forcing any common divisor of $a$ and $m$ to divide 1.

**Verified inverses:**

| $a$ | $m$ | $a^{-1} \bmod m$ | Check |
|---|---|---|---|
| 3 | 7 | **5** | $15 \equiv 1$ |
| 7 | 26 | **15** | $105 = 4\cdot26+1$ |
| 17 | 3120 | **2753** | $46801 = 15\cdot3120+1$ |
| 4 | 6 | **none** | $\gcd(4,6)=2$ |

**This is the theorem RSA runs on.** The private key is a modular inverse, and it exists precisely
because the public exponent is chosen coprime to $\varphi(n)$.

---

## 4. Fermat and Euler

> **Fermat's Little Theorem.** For prime $p$ and $p\nmid a$: $a^{p-1}\equiv1\pmod p$.

**Verified for $p=17$:** $a^{16}\bmod 17 = 1$ for $a = 1,2,3,4,5$ ✓

> **Euler's theorem.** If $\gcd(a,n)=1$ then $a^{\varphi(n)}\equiv1\pmod n$,

where $\varphi(n)$ counts the integers in $[1,n]$ coprime to $n$:

$$\varphi(n) = n\prod_{p\mid n}\left(1-\frac1p\right)$$

— an **inclusion–exclusion** over the distinct prime divisors, exactly Week 8's technique.

**Verified:** $\varphi(9)=6$, $\varphi(10)=4$, $\varphi(12)=4$, $\varphi(36)=12$,
$\varphi(100)=40$ — the last confirmed by counting all 40 integers below 100 coprime to it.

For distinct primes $p,q$: $\varphi(pq)=(p-1)(q-1)$.

---

## 5. The Chinese Remainder Theorem

> **Theorem.** If $m_1,\ldots,m_k$ are pairwise coprime, the system $x\equiv r_i \pmod{m_i}$ has a
> **unique** solution modulo $M=\prod m_i$.

**Verified example.** $x\equiv2\pmod3$, $x\equiv3\pmod5$, $x\equiv2\pmod7$:

$$x \equiv \mathbf{23} \pmod{105}$$

Brute-force search over $0..104$ finds exactly $23$ ✓

**Uses:** RSA decryption is roughly four times faster done separately mod $p$ and mod $q$ and
recombined; CRT also underlies secret sharing and some error-correcting codes.

---

## 6. RSA

**Key generation.**

1. Choose distinct primes $p, q$; set $n=pq$ and $\varphi(n)=(p-1)(q-1)$.
2. Choose $e$ with $\gcd(e,\varphi(n))=1$.
3. Compute $d = e^{-1} \bmod \varphi(n)$ — the extended Euclidean algorithm of §3.

**Public key** $(n,e)$. **Private key** $d$.

$$\text{encrypt: } c = m^e \bmod n \qquad \text{decrypt: } m = c^d \bmod n$$

**Why it inverts.** $ed\equiv1\pmod{\varphi(n)}$, so $ed = 1+k\varphi(n)$ and

$$c^d = m^{ed} = m^{1+k\varphi(n)} = m\cdot\left(m^{\varphi(n)}\right)^k \equiv m\cdot1^k = m \pmod n$$

by **Euler's theorem**. The entire scheme is §4 applied once.

### Verified worked example

$p=61$, $q=53$ ⟹ $n=3233$, $\varphi(n)=3120$. Take $e=17$; then $d = 17^{-1} \bmod 3120 = 2753$
(check: $17\times2753 = 46801 = 15\times3120+1$ ✓).

| $m$ | $c=m^{17}\bmod 3233$ | $c^{2753}\bmod 3233$ |
|---|---|---|
| 9 | 1972 | **9** ✓ |
| 42 | 2557 | **42** ✓ |
| 100 | 1773 | **100** ✓ |

*(A smaller instance $p=11$, $q=13$, $e=7$, $d=103$ round-trips identically.)*

### Where the security lives

The public key gives away $n$ and $e$. Recovering $d$ needs $\varphi(n)$, which needs $p$ and $q$ —
that is, **factoring $n$**.

Everything the legitimate parties do is polynomial: Euclid is $O(\log n)$, modular exponentiation by
repeated squaring is $O(\log e)$ multiplications. Only the attacker's task is hard.

**And it is hard only as far as we know.** Factoring is not proved difficult, and Shor's algorithm
would break RSA on a sufficiently large quantum computer.

---

## 7. Summary

| | |
|---|---|
| $a\equiv b\pmod m$ | $m\mid(a-b)$; an equivalence relation (Week 6) |
| Arithmetic | $+,-,\times$ respect congruence; **division does not** |
| Euclid | $\gcd(a,b)=\gcd(b,a\bmod b)$; $O(\log\min(a,b))$ |
| $\gcd(252,198)$ | $18$ |
| $\gcd\cdot\operatorname{lcm}$ | $=ab$ |
| Bézout | $ax+by=\gcd(a,b)$; here $4(252)-5(198)=18$ |
| Inverse mod $m$ exists | **iff** $\gcd(a,m)=1$ |
| Fermat | $a^{p-1}\equiv1\pmod p$ |
| Euler | $a^{\varphi(n)}\equiv1\pmod n$; $\varphi(pq)=(p-1)(q-1)$ |
| CRT | Unique solution mod $\prod m_i$; the example gives $23 \bmod 105$ |
| RSA | $d=e^{-1}\bmod\varphi(n)$; correctness **is** Euler's theorem |
| Security | Factoring — believed hard, not proved |

---

## 8. End-of-Lecture Exercises

1. Compute $\gcd(1071, 462)$ by the Euclidean algorithm, showing every step.

2. Find integers $x,y$ with $1071x + 462y = \gcd(1071,462)$.

3. Find $11^{-1} \bmod 26$, or show it does not exist.

4. Compute $\varphi(1000)$ using the product formula.

5. Solve $x\equiv1\pmod4$, $x\equiv2\pmod5$, $x\equiv3\pmod7$.

6. **(Stretch.)** With $p=11$, $q=13$, $e=7$: compute $n$, $\varphi(n)$, and $d$, then encrypt $m=9$ and decrypt it back.

---

## Reading

- **Rosen, 8e §4.1–4.6** — Number theory and cryptography
- **Epp, 5e §8.4** — Modular arithmetic and applications
- **Levin, 3e §3.1** — Number theory

*Next: Lecture 12.3 — Review and the Road Ahead*
