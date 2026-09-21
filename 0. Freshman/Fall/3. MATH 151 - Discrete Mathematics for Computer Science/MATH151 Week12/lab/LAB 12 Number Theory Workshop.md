# MATH 151 · Discrete Mathematics for Computer Science
## Lab 12 — Number Theory Workshop: Euclid to RSA
### Wednesday 23 December 2026, 15:00–16:50 · Week 13 (finals week) | Duration: 2 hours | Covers Week 12 (all three lectures)

---

**Bring:** laptop with Python 3. Work in pairs; both submit. No external libraries — in particular,
**do not** use `pow(a, -1, m)` or `math.gcd` until Section 5, where you check your own work against
them.

**The point of this lab:** by the end you will have implemented, from nothing, every component of the
cryptosystem protecting the connection you submit it over.

---

## Section 1 — By Hand (20 min)

### Exercise 1.1
Run the Euclidean algorithm on $\gcd(1071,462)$, writing each division step.

### Exercise 1.2
Work the extended algorithm backwards to find $x,y$ with $1071x+462y=\gcd$.

### Exercise 1.3
Find $11^{-1}\bmod 26$ by hand using your answer to 1.2's method.

### Exercise 1.4
Solve $x\equiv1\pmod4$, $x\equiv2\pmod5$, $x\equiv3\pmod7$ by hand. State the modulus of uniqueness.

---

## Section 2 — Euclid and Bézout (30 min)

**2.1** *(4 pts)* Implement `my_gcd(a, b)` iteratively, and `gcd_trace(a, b)` returning the list of
$(a, b, q, r)$ steps. Print the trace for $(1071,462)$ and $(252,198)$ and check both against your
hand answers.

**2.2** *(5 pts)* Implement the extended algorithm:

```python
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y
```

Verify $ax+by=g$ for at least six pairs, including one where $a<b$ and one with a common factor.

**2.3** *(4 pts)* Count the number of division steps for $\gcd(F_{k+1}, F_k)$ using Fibonacci numbers
$k=5,\ldots,20$. **Fibonacci pairs are the worst case for Euclid** — tabulate the step count against
$k$ and describe the relationship.

**2.4** *(3 pts)* Verify $\gcd(a,b)\cdot\operatorname{lcm}(a,b)=ab$ for ten random pairs.

---

## Section 3 — Modular Arithmetic (30 min)

**3.1** *(4 pts)* Implement `mod_inverse(a, m)` using `egcd`, returning `None` when the inverse does
not exist. Build the full table of invertible elements mod 12 and mod 13. **How many are there in
each case, and what is the pattern?**

**3.2** *(5 pts)* Implement `phi(n)` by the product formula, and `phi_count(n)` by brute-force
counting. Verify they agree for all $n \le 200$.

**3.3** *(4 pts)* Verify **Euler's theorem** $a^{\varphi(n)}\equiv1\pmod n$ for every $n \le 50$ and
every $a$ coprime to $n$. Report any failures. Then check **Fermat's** special case for
$p = 7, 13, 17$.

**3.4** *(5 pts)* Implement `crt(residues, moduli)` for pairwise coprime moduli. Test on the
Section 1.4 system, and on $x\equiv2\pmod3$, $x\equiv3\pmod5$, $x\equiv2\pmod7$. Verify each answer
by brute-force search.

**3.5** *(3 pts)* Implement fast modular exponentiation by repeated squaring:

```python
def mod_pow(base, exp, m):
    result = 1
    base %= m
    while exp > 0:
        if exp & 1:
            result = result * base % m
        base = base * base % m
        exp >>= 1
    return result
```

Compare its multiplication count with the naive loop for $2^{1000} \bmod 10^9{+}7$.

---

## Section 4 — RSA (30 min)

**4.1** *(6 pts)* Implement key generation:

```python
def rsa_keys(p, q, e):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    d = mod_inverse(e, phi_n)
    return (n, e), (n, d)
```

Generate keys for $p=11, q=13, e=7$ and for $p=61, q=53, e=17$. Report $n$, $\varphi(n)$, and $d$ for
each, and verify $ed \equiv 1 \pmod{\varphi(n)}$.

**4.2** *(6 pts)* Implement `encrypt` and `decrypt` with `mod_pow`. For each key pair, round-trip
**every** message $m$ with $0 \le m < n$. Report the number of failures. *(It should be zero.)*

**4.3** *(4 pts)* Choose $e = 6$ with $p=11, q=13$. What does `mod_inverse` return, and why? State
the condition on $e$ that key generation requires.

**4.4** *(4 pts)* Write `crack(n, e)` that factors $n$ by trial division and recovers $d$. Time it
for $n = 143$, then for a semiprime built from two 6-digit primes. **Extrapolate: how long for two
100-digit primes?**

---

## Section 5 — Checking Your Work (10 min)

Now compare against Python's built-ins:

- `math.gcd(a, b)` against `my_gcd`
- `pow(a, -1, m)` against `mod_inverse`
- `pow(base, exp, m)` against `mod_pow`

Report any discrepancies. **If there are none, you have implemented RSA correctly from scratch.**

---

## Section 6 — Reflection (10 min)

1. Section 2.3 showed Fibonacci pairs are Euclid's worst case, and it is still fast. Section 4.4
   showed factoring is not. Both operate on the same numbers — what makes one easy and the other hard?

2. RSA's correctness is Euler's theorem, proved in the 1760s. Its security rests on factoring being
   hard, which is **not** proved. What would change if someone found a polynomial factoring
   algorithm tomorrow?

3. You implemented every piece of RSA in under 60 lines. Why, then, is "don't roll your own crypto"
   standard advice?

---

## Checkoff Criteria

Show your TA:

- [ ] Section 1: all four hand exercises
- [ ] 2.2: Bézout verified for six pairs
- [ ] 2.3: Fibonacci step-count table with the relationship described
- [ ] 3.1: invertible-element tables for mod 12 and mod 13, pattern identified
- [ ] 3.2: `phi` and `phi_count` agreeing for all $n\le200$
- [ ] 3.3: Euler verified with zero failures
- [ ] 3.4: CRT correct on both systems, brute-force confirmed
- [ ] 4.2: **zero** round-trip failures for both key pairs
- [ ] 4.3: `None` explained
- [ ] 4.4: extrapolation attempted
- [ ] Section 5: all three comparisons clean
