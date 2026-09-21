# MATH 151 · Discrete Mathematics for Computer Science
## Week 12 — Number Theory: Divisibility, Primes, Modular Arithmetic; Review

---

### Course Information

| Field | Detail |
|---|---|
| Course | MATH 151: Discrete Mathematics for Computer Science |
| Credits | 3 |
| Semester | Fall, Year 1 |
| Week | 12 of 12 — **final week** |

---

### Week 12 Overview

The course ends where applied mathematics is at its most consequential. Everything this week is
elementary — divisibility, remainders, prime factorisation, ideas mostly settled by Euclid — and
together they secure essentially all encrypted traffic on the internet.

Monday covers **divisibility and primes**: the division algorithm, unique factorisation, and Euclid's
proof that the primes never run out. That proof is widely misremembered as "$p_1\cdots p_k+1$ is
prime", and Monday kills the misremembering with a counterexample you can check by hand.

Thursday is the payoff. The **Euclidean algorithm** computes gcds in $O(\log n)$; its extended form
produces modular inverses; **Euler's theorem** then makes RSA work, and the proof of RSA's correctness
is three lines. You will encrypt and decrypt a number by hand.

**The asymmetry is the whole point.** Multiplying two large primes is instant. Factoring the product
is, as far as anyone knows, infeasible. Everything the legitimate parties do is polynomial; only the
attacker faces an exponential problem. And that gap is *believed*, not proved — nobody has shown
factoring is hard, which is why a proof either way would be among the most consequential results in
the subject.

Friday reviews the whole course and traces where each thread continues.

---

### Week 12 Contents

```
MATH151 Week12/
├── README.md
├── lectures/
│   ├── L36 Divisibility and Primes.md         ← Lecture 36 (Monday 14 Dec)
│   ├── L37 Modular Arithmetic and RSA.md      ← Lecture 37 (Thursday 17 Dec)
│   └── L38 Review and the Road Ahead.md       ← Lecture 38 (Friday 18 Dec)
├── assignments/
│   └── PS 12 Number Theory.md
├── lab/
│   └── LAB 12 Number Theory Workshop.md
├── quiz/
│   └── QUIZ 12 Trees.md
├── resources/
│   ├── Number Theory Reference.md
│   ├── RSA Implementation Toolkit.md
│   └── Final Exam Study Guide.md
└── solutions_instructor/
    ├── LAB 12 Solutions.md
    ├── PS 12 Solutions.md
    └── QUIZ 12 Solutions.md
```

---

### Learning Objectives

By the end of Week 12 you should be able to:

- State the division algorithm and apply it correctly to negative dividends
- Use the linearity property of divisibility in proofs
- State and apply the Fundamental Theorem of Arithmetic, and explain why 1 is not prime
- Reproduce Euclid's proof of the infinitude of primes, and explain why $\prod p_i+1$ need not be prime
- Execute the Euclidean and extended Euclidean algorithms by hand
- Determine when a modular inverse exists and compute it
- Apply Fermat's Little Theorem and Euler's theorem to reduce large exponents
- Solve a system of congruences with the Chinese Remainder Theorem
- Generate RSA keys, encrypt, decrypt, and **prove** the scheme correct
- Explain precisely what an attacker must compute, and why it is believed hard

---

### Schedule at a Glance

| Day | Event | Topic |
|---|---|---|
| Monday 14 Dec, 13:00 | Quiz 12 (15 min) | Covers Week 11: trees, MSTs, traversal |
| Monday 14 Dec, 13:00 | Lecture 36 | Divisibility, the division algorithm, primes, unique factorisation |
| Thursday 17 Dec, 13:00 | Lecture 37 | Congruence, Euclid, Bézout, Fermat, Euler, CRT, RSA |
| Friday 18 Dec, 13:00 | Lecture 38 | Course review and the road ahead |
| Friday 18 Dec, 14:00 | PS 12 released | Due Wednesday 23 Dec, 17:00 (finals week) |
| Wednesday 23 Dec, 15:00 (Week 13) | Lab 12 | Implement RSA from scratch |

---

### Textbook Readings

| Text | Sections |
|---|---|
| Rosen, 8e | §4.1–4.6 (Number theory and cryptography) |
| Epp, 5e | §4.3–4.4 (Divisibility), §8.4 (Modular arithmetic) |
| Levin, 3e | §3.1 (Number theory) |

---

### Key Results

| | |
|---|---|
| $a\mid b$ | $\exists k: b=ak$; **linearity** $a\mid(bx+cy)$ |
| Division algorithm | $0\le r<d$, so $-7\bmod3=2$ |
| Fundamental Theorem | Unique prime factorisation |
| Euclid | Infinitely many primes; $30031=59\times509$ |
| Euclidean algorithm | $O(\log\min(a,b))$; worst case consecutive Fibonacci |
| $\gcd\cdot\operatorname{lcm}$ | $=ab$ |
| Bézout | $ax+by=\gcd(a,b)$ |
| Inverse mod $m$ | Exists **iff** $\gcd(a,m)=1$ |
| Fermat | $a^{p-1}\equiv1\pmod p$ |
| Euler | $a^{\varphi(n)}\equiv1\pmod n$; $\varphi(pq)=(p-1)(q-1)$ |
| CRT | Unique mod $\prod m_i$ |
| RSA correctness | **Is** Euler's theorem |
| RSA security | Factoring — believed hard, **not proved** |

---

### Number Theory in Computer Science

| Concept | Application |
|---|---|
| Modular arithmetic | Hash functions; cyclic buffers; checksums |
| GCD | Reducing fractions; cycle detection; stride calculations |
| Extended Euclid | Modular inverses — the RSA private key |
| Fermat's Little Theorem | Miller–Rabin primality testing |
| Euler's theorem | RSA correctness |
| CRT | Faster RSA decryption; secret sharing; error-correcting codes |
| Prime generation | Key generation, via the Prime Number Theorem's density estimate |
| Factoring hardness | The security assumption under RSA |
| Repeated squaring | Making $m^e \bmod n$ feasible at all |

---

### Connections

**Back:** Week 6's equivalence relations *are* congruence mod $n$ — the residue classes are the
equivalence classes. Week 8's inclusion–exclusion produces Euler's totient formula. Week 3's strong
induction proves the existence half of unique factorisation. Week 2's proof by contradiction is
Euclid's method.

**Forward:** **CS 340** develops cryptography properly — padding, key exchange, digital signatures,
and the attacks that break naive implementations. **CS 301** formalises the complexity classes this
week gestures at.

**Sideways:** the "easy to verify, hard to find" asymmetry underlying RSA is the same shape as Week
8's subset-sum and Week 10's Hamilton problem. By now you should recognise it on sight.

---

*MATH 151 · Week 12 · © CSE Department*

*This concludes the course.*
