# MATH 151 · Number Theory Reference
## Week 12

---

## Divisibility

> $a \mid b$ means $\exists k \in \mathbb{Z}: b = ak$.

| Property | |
|---|---|
| Transitivity | $a\mid b$, $b\mid c$ ⟹ $a\mid c$ |
| **Linearity** | $a\mid b$, $a\mid c$ ⟹ $a\mid(bx+cy)$ for all integers $x,y$ |
| Antisymmetry | $a\mid b$, $b\mid a$ ⟹ $a=\pm b$ |

**Linearity is the workhorse** — nearly every proof this week reduces to it.

### Division algorithm

$$a = dq + r,\qquad 0 \le r < d \quad\text{(unique)}$$

| $a$ | $d$ | $q$ | $r$ |
|---|---|---|---|
| $-29$ | 7 | $-5$ | **6** |
| 100 | 13 | 7 | 9 |
| $-7$ | 3 | $-3$ | **2** |

> **The remainder is never negative.** $-7 \bmod 3 = 2$, not $-1$. Python's `%` agrees; **C's does
> not** — `-7 % 3` is `-1` in C. A recurring source of bugs.

---

## Primes

> $p>1$ is prime if its only positive divisors are $1$ and $p$.

**Fundamental Theorem of Arithmetic:** every $n>1$ factors into primes uniquely up to order.

| $n$ | Factorisation |
|---|---|
| 360 | $2^3\cdot3^2\cdot5$ |
| 1001 | $7\cdot11\cdot13$ |
| 1024 | $2^{10}$ |
| 1764 | $2^2\cdot3^2\cdot7^2$ |
| 5040 | $2^4\cdot3^2\cdot5\cdot7$ |
| 9797 | $97\cdot101$ |
| 2310 | $2\cdot3\cdot5\cdot7\cdot11$ |

**$1$ is not prime** — otherwise uniqueness fails ($6 = 2\cdot3 = 1\cdot2\cdot3 = \ldots$).

### Euclid: infinitely many primes

Given $p_1,\ldots,p_k$, the number $N = \prod p_i + 1$ has a prime factor not among them.

> **$N$ itself need not be prime.** Verified:

| Primes used | $N$ | Factorisation |
|---|---|---|
| 2, 3, 5, 7, 11 | 2311 | prime |
| 2, 3, 5, 7, 11, 13 | **30031** | $59 \times 509$ |
| 2, 3, 5, 7, 11, 13, 17 | **510511** | $19\times97\times277$ |

The proof only needs a *new* prime factor, and $59$ supplies one.

### Finding primes

- **Trial division** to $\sqrt n$: $\Theta(\sqrt n)$ — **exponential in the digit count**
- **Sieve of Eratosthenes**: $\Theta(n\log\log n)$ for all primes up to $n$. There are **25 primes
  below 100** and **15 below 50**
- **Prime Number Theorem:** $\pi(n)\sim n/\ln n$

---

## The Euclidean Algorithm

$$\gcd(a,b)=\gcd(b,\ a\bmod b),\qquad \gcd(a,0)=a$$

**Verified trace, $\gcd(252,198)$:**

$$252 = 1(198)+54 \quad 198 = 3(54)+36 \quad 54 = 1(36)+18 \quad 36 = 2(18)+0$$

$\gcd = \mathbf{18}$ — the last non-zero remainder.

**$\gcd(1071,462)$:** $1071=2(462)+147$, $462=3(147)+21$, $147=7(21)+0$ ⟹ $\gcd=\mathbf{21}$.

**Cost $O(\log\min(a,b))$** — polynomial in the digit count. The worst case is consecutive
**Fibonacci** numbers: verified, $\gcd(F_{k+1},F_k)$ takes exactly $k-1$ steps.

$$\gcd(a,b)\cdot\operatorname{lcm}(a,b)=ab$$

*Verified: $\gcd(252,198)=18$, $\operatorname{lcm}=2772$, $18\cdot2772=49896=252\cdot198$.*

---

## Bézout and Inverses

> **Bézout:** $\exists x,y$ with $ax+by=\gcd(a,b)$.

*Verified: $4(252)-5(198)=18$; $-3(1071)+7(462)=21$.*

> **$a^{-1} \bmod m$ exists iff $\gcd(a,m)=1$.**

| $a$ | $m$ | $a^{-1}$ |
|---|---|---|
| 3 | 7 | 5 |
| 7 | 26 | 15 |
| 11 | 26 | 19 |
| 17 | 3120 | 2753 |
| 4 | 6 | **none** |
| 6 | 120 | **none** |

*Invertible elements mod 12: $\{1,5,7,11\}$ — four of them, $=\varphi(12)$. Mod 13: all twelve,
$=\varphi(13)$.*

---

## Congruence

> $a\equiv b\pmod m$ ⟺ $m\mid(a-b)$.

An **equivalence relation** (Week 6) partitioning $\mathbb{Z}$ into $m$ residue classes.

$+$, $-$, $\times$ respect congruence — **division does not**. Cancelling requires an inverse.

### Fermat and Euler

$$a^{p-1}\equiv1\pmod p \quad (p \text{ prime},\ p\nmid a) \qquad a^{\varphi(n)}\equiv1\pmod n \quad (\gcd(a,n)=1)$$

$$\varphi(n)=n\prod_{p\mid n}\left(1-\frac1p\right) \qquad \varphi(pq)=(p-1)(q-1)$$

| $n$ | 9 | 10 | 12 | 36 | 100 | 1000 |
|---|---|---|---|---|---|---|
| $\varphi(n)$ | 6 | 4 | 4 | 12 | 40 | **400** |

*All verified by brute-force counting.*

**Use:** $7^{100}\bmod13$. Fermat gives $7^{12}\equiv1$, and $100 = 8(12)+4$, so
$7^{100}\equiv7^{4}\equiv\mathbf 9 \pmod{13}$ — verified.

---

## Chinese Remainder Theorem

> Pairwise coprime moduli ⟹ a **unique** solution mod $M=\prod m_i$.

| System | Solution |
|---|---|
| $x\equiv2(3)$, $x\equiv3(5)$, $x\equiv2(7)$ | $x\equiv \mathbf{23} \pmod{105}$ |
| $x\equiv1(4)$, $x\equiv2(5)$, $x\equiv3(7)$ | $x\equiv \mathbf{17} \pmod{140}$ |

*Both confirmed by brute-force search.*

---

## RSA

1. Primes $p,q$; $n=pq$; $\varphi(n)=(p-1)(q-1)$
2. $e$ with $\gcd(e,\varphi(n))=1$
3. $d=e^{-1}\bmod\varphi(n)$

$$c=m^e\bmod n \qquad m=c^d\bmod n$$

**Correctness is Euler's theorem:** $ed=1+k\varphi(n)$, so
$c^d=m^{1+k\varphi(n)}=m(m^{\varphi(n)})^k\equiv m$.

**Verified worked examples:**

| $p$ | $q$ | $n$ | $\varphi(n)$ | $e$ | $d$ | $m$ | $c$ | decrypted |
|---|---|---|---|---|---|---|---|---|
| 11 | 13 | 143 | 120 | 7 | 103 | 9 | 48 | **9** ✓ |
| 61 | 53 | 3233 | 3120 | 17 | 2753 | 9 | 1972 | **9** ✓ |
| 61 | 53 | 3233 | 3120 | 17 | 2753 | 42 | 2557 | **42** ✓ |

**Security:** recovering $d$ from $(n,e)$ requires $\varphi(n)$, hence $p$ and $q$, hence **factoring
$n$**. Believed hard; **not proved**. Shor's algorithm breaks it on a quantum computer.

---

## Common Errors

| ❌ | ✅ |
|---|---|
| $-7\bmod3=-1$ | $=2$; the remainder is non-negative |
| $\prod p_i+1$ is always prime | $30031=59\times509$ |
| Cancelling in a congruence | Needs an inverse; requires $\gcd=1$ |
| Assuming every $a$ has an inverse mod $m$ | Only when $\gcd(a,m)=1$ |
| $\varphi(n)=n-1$ for all $n$ | Only for **prime** $n$ |
| Computing $m^e$ then reducing | Reduce at every step — use repeated squaring |
| "Factoring is proved hard" | It is **believed** hard |

---

*MATH 151 · Week 12 · Reference · © CSE Department*
