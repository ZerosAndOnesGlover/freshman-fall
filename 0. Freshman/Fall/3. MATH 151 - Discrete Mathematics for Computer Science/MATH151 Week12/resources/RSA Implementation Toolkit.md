# MATH 151 · RSA Implementation Toolkit
## Week 12

Everything below is written from scratch. Compare against Python's built-ins only *after* your own
version works.

---

## Euclid

```python
def my_gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def gcd_trace(a, b):
    steps = []
    while b:
        q, r = divmod(a, b)
        steps.append((a, b, q, r))
        a, b = b, r
    return steps, a
```

*Verified: $\gcd(252,198)=18$ in 4 steps; $\gcd(1071,462)=21$ in 3 steps.*

**Worst case is consecutive Fibonacci numbers** — $\gcd(F_{k+1},F_k)$ takes exactly $k-1$ divisions
(verified for $k=5..20$). Even so, $\gcd(F_{21},F_{20})$ needs only 19 steps on five-digit inputs.

---

## Extended Euclid and Inverses

```python
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y

def mod_inverse(a, m):
    g, x, _ = egcd(a, m)
    return x % m if g == 1 else None
```

`egcd(a, b)` returns $(g, x, y)$ with $ax+by=g$.

*Verified: `egcd(252,198)` → $(18, 4, -5)$ and $4(252)-5(198)=18$ ✓*

*`mod_inverse(17, 3120)` → **2753**; `mod_inverse(4, 6)` → **None**.*

**The `% m` at the end matters** — `egcd` may return a negative $x$, and an inverse should be in
$[0,m)$.

---

## Euler's Totient

```python
def phi(n):
    result, m, p = n, n, 2
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            result -= result // p
        p += 1
    if m > 1:
        result -= result // m
    return result

def phi_count(n):
    return sum(1 for k in range(1, n + 1) if my_gcd(k, n) == 1)
```

*Verified: the two agree for every $n \le 200$. $\varphi(100)=40$, $\varphi(1000)=400$.*

`phi` is $O(\sqrt n)$; `phi_count` is $O(n\log n)$. **Both require the factorisation, which is why
knowing $\varphi(n)$ for a large RSA modulus is as hard as factoring it.**

---

## Fast Modular Exponentiation

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

$O(\log e)$ multiplications instead of $e$. **Never form $m^e$ before reducing** — for RSA-sized
numbers that value has millions of digits.

---

## Chinese Remainder Theorem

```python
from functools import reduce

def crt(residues, moduli):
    M = reduce(lambda x, y: x * y, moduli)
    total = 0
    for r, m in zip(residues, moduli):
        Mi = M // m
        total += r * Mi * mod_inverse(Mi % m, m)
    return total % M, M
```

*Verified: `crt([2,3,2],[3,5,7])` → $(23, 105)$; `crt([1,2,3],[4,5,7])` → $(17, 140)$. Both confirmed
by brute-force search.*

Requires **pairwise coprime** moduli.

---

## RSA

```python
def rsa_keys(p, q, e):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    d = mod_inverse(e, phi_n)
    if d is None:
        raise ValueError("e must be coprime to phi(n)")
    return (n, e), (n, d)

def encrypt(m, pub):
    n, e = pub
    return mod_pow(m, e, n)

def decrypt(c, priv):
    n, d = priv
    return mod_pow(c, d, n)
```

**Verified key pairs:**

| $p$ | $q$ | $n$ | $\varphi(n)$ | $e$ | $d$ | $ed \bmod \varphi(n)$ |
|---|---|---|---|---|---|---|
| 11 | 13 | 143 | 120 | 7 | 103 | 1 ✓ |
| 61 | 53 | 3233 | 3120 | 17 | 2753 | 1 ✓ |

**Round-trip verified for every $m$ with $0 \le m < n$, both key pairs — zero failures.**

**Choosing $e = 6$ with $\varphi(n)=120$ fails**, because $\gcd(6,120)=6\ne1$ and no inverse exists.
`mod_inverse` returns `None` — this is the condition step 2 of key generation exists to enforce.

---

## Breaking It

```python
def crack(n, e):
    for p in range(2, int(n ** 0.5) + 1):
        if n % p == 0:
            q = n // p
            return mod_inverse(e, (p - 1) * (q - 1))
    return None
```

Instant for $n=143$. Slow for a 12-digit semiprime. **Hopeless for 617 digits (2048 bits)** — trial
division is $\Theta(\sqrt n)$, which is exponential in the digit count.

**This is the entire security argument**, and it is empirical: nobody has proved factoring is hard.

---

## Checking Against the Standard Library

| Yours | Python's |
|---|---|
| `my_gcd(a, b)` | `math.gcd(a, b)` |
| `mod_inverse(a, m)` | `pow(a, -1, m)` |
| `mod_pow(b, e, m)` | `pow(b, e, m)` |

If all three agree, you have implemented RSA correctly.

---

## Why "Don't Roll Your Own Crypto"

The mathematics above is correct and complete, and a production implementation would still be
insecure. Textbook RSA leaks information — identical plaintexts give identical ciphertexts, small
messages with small $e$ can be recovered by taking an ordinary $e$-th root, and the timing of
`mod_pow` can reveal bits of $d$ to an attacker measuring how long decryption takes.

Real systems add randomised padding (OAEP), constant-time arithmetic, and careful key generation.
**The failure mode is never the theorem — it is everything around it.**

---

*MATH 151 · Week 12 · Reference · © CSE Department*
