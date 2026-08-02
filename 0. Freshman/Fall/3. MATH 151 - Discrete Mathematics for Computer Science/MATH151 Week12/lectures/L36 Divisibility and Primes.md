# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 12.1 (L36) — Divisibility and Primes
### Monday, Week 12

---

## 1. Divisibility

> **Definition.** For integers $a, b$ with $a \ne 0$, we say $a \mid b$ ("$a$ divides $b$") if there
> exists an integer $k$ with $b = ak$.

Note what this does *not* say: nothing about fractions, nothing about remainders. It is a purely
existential statement, which is why divisibility proofs are almost always "produce the $k$".

**Basic properties.** For all integers $a,b,c$:

| | |
|---|---|
| $a\mid b$ and $b\mid c$ ⟹ $a\mid c$ | transitivity |
| $a\mid b$ and $a\mid c$ ⟹ $a\mid(bx+cy)$ for all $x,y$ | **linearity** |
| $a\mid b$ and $b\mid a$ ⟹ $a=\pm b$ | |
| $a \mid 0$ for every $a\ne0$ | |

**The linearity property is the workhorse.** Almost every proof this week uses it, usually in the
form "if $d$ divides two things, it divides any integer combination of them".

**Proof of linearity.** $b=ak_1$ and $c=ak_2$ give $bx+cy = a(k_1x+k_2y)$, and $k_1x+k_2y$ is an
integer. ∎

---

## 2. The Division Algorithm

> **Theorem.** For any integer $a$ and any $d>0$, there exist **unique** integers $q$ and $r$ with
> $$a = dq + r, \qquad 0 \le r < d$$

$q$ is the quotient, $r$ the remainder. The constraint $0\le r<d$ is what makes them unique.

**Careful with negatives.** $-7 = 3(-3) + 2$, so $-7 \bmod 3 = 2$ — *not* $-1$. The remainder is
always non-negative under this definition. Python's `%` agrees; C's `%` does not, which is a
recurring source of bugs.

---

## 3. Primes

> **Definition.** An integer $p>1$ is **prime** if its only positive divisors are $1$ and $p$.
> Otherwise it is **composite**.

$1$ is neither — a convention, but a load-bearing one, as §4 explains.

### The Fundamental Theorem of Arithmetic

> **Theorem.** Every integer $n>1$ factors into primes, **uniquely** up to order.

**Verified:**

| $n$ | Factorisation |
|---|---|
| 360 | $2^3\cdot3^2\cdot5$ |
| 1001 | $7\cdot11\cdot13$ |
| 1024 | $2^{10}$ |
| 2310 | $2\cdot3\cdot5\cdot7\cdot11$ |
| 97 | $97$ (prime) |

**This is why $1$ is not prime.** If it were, $6 = 2\cdot3 = 1\cdot2\cdot3 = 1^2\cdot2\cdot3$ would
have infinitely many factorisations and uniqueness would fail. Excluding $1$ is what buys the
theorem.

**Existence** is strong induction (Week 3): either $n$ is prime, or $n=ab$ with both factors smaller,
and both factor by hypothesis. **Uniqueness** is harder and needs Euclid's lemma — that $p \mid ab$
implies $p\mid a$ or $p\mid b$.

---

## 4. There Are Infinitely Many Primes

> **Theorem (Euclid).** There are infinitely many primes.

**Proof.** Suppose the primes were exactly $p_1,\ldots,p_k$. Let $N = p_1p_2\cdots p_k + 1$.

$N>1$, so it has a prime divisor $p$. If $p$ were one of the $p_i$, then $p$ divides both
$p_1\cdots p_k$ and $N$, hence divides their difference $N - p_1\cdots p_k = 1$ — impossible.

So $p$ is a prime not on the list, contradicting completeness. ∎

### A misreading worth destroying

Students often remember this as "$p_1\cdots p_k+1$ is prime". **It is not.** Verified:

| Primes used | $N = \prod p_i + 1$ | Factorisation |
|---|---|---|
| 2 | 3 | prime |
| 2, 3 | 7 | prime |
| 2, 3, 5 | 31 | prime |
| 2, 3, 5, 7 | 211 | prime |
| 2, 3, 5, 7, 11 | 2311 | prime |
| 2, 3, 5, 7, 11, 13 | **30031** | $\mathbf{59 \times 509}$ |

At the sixth step $N$ is composite — and the proof does not care. It only needs $N$ to have *some*
prime factor outside the list, and $59$ obliges. **The argument is about the existence of a new
prime, not about $N$ itself.**

---

## 5. Finding Primes

### Trial division

To test whether $n$ is prime, try divisors up to $\sqrt n$. If $n=ab$ with $a\le b$, then
$a\le\sqrt n$ — so a factor above $\sqrt n$ always has a partner below it.

Cost $\Theta(\sqrt n)$, which sounds cheap and is not: $n$ has $\log_{10} n$ digits, so this is
**exponential in the input size**. Testing a 2048-bit number this way is hopeless.

### The Sieve of Eratosthenes

Mark multiples of each prime up to $\sqrt n$; whatever survives is prime.

**Verified:** there are **25 primes below 100** — $2, 3, 5, 7, 11, \ldots, 83, 89, 97$.

Cost $\Theta(n\log\log n)$, efficient for finding *all* primes up to $n$, useless for testing a
single huge one.

### The distribution of primes

> **Prime Number Theorem.** $\pi(n) \sim \dfrac{n}{\ln n}$.

Primes thin out but never stop. Near $10^{300}$ roughly one number in $690$ is prime, which is why
generating a random 1024-bit prime by guess-and-test is practical — and RSA depends on exactly that.

---

## 6. Why Cryptography Lives Here

Two facts, in tension:

- **Multiplying primes is easy.** Two 1024-bit primes multiply in microseconds.
- **Factoring the product is hard.** No known classical algorithm factors a 2048-bit semiprime in
  reasonable time.

This asymmetry is the whole basis of RSA, which Wednesday builds. **It is not a theorem** — nobody has
proved factoring is hard, only that no one has managed it. Shor's algorithm factors in polynomial
time *on a quantum computer*, which is why post-quantum cryptography is an active field.

**The security of most internet traffic rests on a problem we believe is hard and cannot prove is.**

---

## 7. Summary

| | |
|---|---|
| $a\mid b$ | $\exists k: b=ak$ |
| Linearity | $a\mid b, a\mid c \Rightarrow a\mid(bx+cy)$ |
| Division algorithm | $a=dq+r$, $0\le r<d$, unique |
| $-7 \bmod 3$ | $= 2$, not $-1$ |
| Prime | $p>1$ with no divisors but $1$ and $p$ |
| Fundamental Theorem | Unique prime factorisation |
| Why $1$ isn't prime | Uniqueness would fail |
| Euclid | Infinitely many primes |
| $\prod p_i + 1$ | Need **not** be prime — $30031 = 59\times509$ |
| Trial division | $\Theta(\sqrt n)$ — exponential in the digit count |
| Sieve | 25 primes below 100 |
| RSA rests on | Factoring being hard — believed, unproved |

---

## 8. End-of-Lecture Exercises

1. Prove: if $a\mid b$ and $a\mid c$ then $a\mid(3b-5c)$.

2. Find $q$ and $r$ for $a=-29$, $d=7$, with $0\le r<7$.

3. Factor 1764, 5040, and 9797 into primes.

4. How many primes are there below 50? List them.

5. Compute $2\cdot3\cdot5\cdot7\cdot11\cdot13\cdot17 + 1$ and determine whether it is prime.

6. **(Stretch.)** Prove that if $n$ is composite then it has a prime factor $\le\sqrt n$, and explain why this justifies stopping trial division there.

---

## Reading

- **Rosen, 8e §4.1, §4.3** — Divisibility, primes, greatest common divisors
- **Epp, 5e §4.3–4.4** — Divisibility and the division algorithm
- **Levin, 3e §3.1** — Number theory basics

*Next: Lecture 12.2 — Modular Arithmetic, the GCD, and RSA*
