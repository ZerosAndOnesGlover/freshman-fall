# MATH 151 · Week 12
## LAB 12 Solutions — INSTRUCTOR ONLY

All outputs produced by running the lab code.

---

## Section 1 Solutions — By Hand

**1.1** $1071 = 2(462)+147$; $462 = 3(147)+21$; $147 = 7(21)+0$. **$\gcd = 21$**, three steps.

**1.2** $21 = 462-3(147)$ and $147 = 1071-2(462)$, so $21 = 7(462)-3(1071)$: $x=-3$, $y=7$.

**1.3** $11^{-1} \equiv \mathbf{19} \pmod{26}$, since $11\times19 = 209 = 8(26)+1$.

**1.4** $x \equiv \mathbf{17} \pmod{140}$. Uniqueness modulus $4\cdot5\cdot7=140$, valid because the
moduli are pairwise coprime.

---

## Section 2 Solutions — Euclid and Bézout

**2.1** *(4 pts)* Traces match the hand answers: $\gcd(1071,462)=21$ in 3 steps;
$\gcd(252,198)=18$ in 4 steps.

**2.2** *(5 pts)* `egcd(252,198)` → $(18, 4, -5)$, and $4(252)-5(198)=18$ ✓

Students should include a pair with $a<b$ (the algorithm swaps on the first call, costing one extra
step) and a pair with a common factor.

**2.3** *(4 pts)* **Fibonacci is the worst case**, verified:

| $k$ | 5 | 8 | 10 | 15 | 20 |
|---|---|---|---|---|---|
| $\gcd(F_{k+1},F_k)$ steps | 4 | 7 | 9 | 14 | 19 |

**The step count is exactly $k-1$** — linear in $k$, while $F_k$ itself grows like $\varphi^k$. So the
number of divisions is **logarithmic in the size of the inputs**, which is the general bound made
tight.

*This is why Euclid is fast: even its worst case is logarithmic. Students who only observe "it's
still quick" have missed the $k-1$ pattern — push for it.*

**2.4** *(3 pts)* $\gcd\cdot\operatorname{lcm}=ab$ holds on every random pair. Verified for
$(252,198)$: $18\times2772 = 49896 = 252\times198$.

---

## Section 3 Solutions — Modular Arithmetic

**3.1** *(4 pts)*

| Modulus | Invertible elements | Count |
|---|---|---|
| 12 | $\{1,5,7,11\}$ | **4** |
| 13 | $\{1,\ldots,12\}$ | **12** |

**The pattern: the count is $\varphi(m)$.** For prime $m$ every non-zero element is invertible, since
$\gcd(a,p)=1$ for all $0<a<p$ — which is why RSA moduli use primes as their building blocks.

**3.2** *(5 pts)* `phi` and `phi_count` agree for **every** $n\le200$. Notable values:
$\varphi(100)=40$, $\varphi(1000)=400$.

`phi` is $O(\sqrt n)$ because it factors; `phi_count` is $O(n\log n)$. **Both need the
factorisation — which is exactly why $\varphi(n)$ is as hard to obtain as factoring $n$**, and hence
why RSA's private key is safe.

**3.3** *(4 pts)* Euler's theorem verified for **every** $n\le50$ and every $a$ coprime to $n$:
**zero failures**. Fermat confirmed for $p=7,13,17$ — e.g. $a^{16}\equiv1\pmod{17}$ for
$a=1,\ldots,5$.

**3.4** *(5 pts)*

| System | CRT | Brute force |
|---|---|---|
| $x\equiv1(4),\ 2(5),\ 3(7)$ | $17 \pmod{140}$ | 17 ✓ |
| $x\equiv2(3),\ 3(5),\ 2(7)$ | $23 \pmod{105}$ | 23 ✓ |

**3.5** *(3 pts)* Repeated squaring uses $O(\log e)$ multiplications — about **10** for $e=1000$,
against 1000 for the naive loop. More importantly, the naive version applied to RSA-sized exponents
would need $\sim10^{600}$ multiplications; the fast one needs about 2048.

---

## Section 4 Solutions — RSA

**4.1** *(6 pts)*

| $p$ | $q$ | $n$ | $\varphi(n)$ | $e$ | $d$ | $ed \bmod \varphi(n)$ |
|---|---|---|---|---|---|---|
| 11 | 13 | 143 | 120 | 7 | **103** | 1 ✓ |
| 61 | 53 | 3233 | 3120 | 17 | **2753** | 1 ✓ |

**4.2** *(6 pts)* Round-tripping **every** $m$ with $0\le m<n$:

| Key pair | Messages tested | Failures |
|---|---|---|
| $n=143$ | 143 | **0** |
| $n=3233$ | 3233 | **0** |

*Note this includes messages sharing a factor with $n$ (e.g. $m=11$ when $n=143$), which Euler's
theorem alone does not cover — the CRT argument does. Worth mentioning to anyone who asks.*

**4.3** *(4 pts)* With $p=11$, $q=13$, $e=6$: $\varphi(n)=120$ and $\gcd(6,120)=6\ne1$, so no inverse
exists and `mod_inverse` returns **`None`**.

**The requirement is $\gcd(e,\varphi(n))=1$.** Without it there is no $d$, and the scheme has no
decryption function at all. This is why step 2 of key generation is a constraint, not a suggestion.

**4.4** *(4 pts)* `crack(143, 7)` is instant — trial division finds $11$ immediately. For a semiprime
from two 6-digit primes, $\sqrt n \approx 10^6$, so around a million divisions: still under a second.

**Extrapolation:** two 100-digit primes give $n$ with 200 digits, so $\sqrt n \approx 10^{100}$
divisions. At $10^9$ divisions per second that is $10^{91}$ seconds — around $10^{83}$ times the age
of the universe.

*Students who attempt an actual timing extrapolation rather than hand-waving should be credited
generously; the point is to feel the exponential, not to name it.*

---

## Section 5 — Checking Against the Library

All three comparisons agree:

| Yours | Python's | Match |
|---|---|---|
| `my_gcd` | `math.gcd` | ✓ |
| `mod_inverse(a,m)` | `pow(a,-1,m)` | ✓ |
| `mod_pow(b,e,m)` | `pow(b,e,m)` | ✓ |

*One caveat worth flagging: `pow(a,-1,m)` raises `ValueError` when no inverse exists, where
`mod_inverse` returns `None`. Different interface, same mathematics.*

---

## Section 6 — Reflection Model Answers

1. **Same numbers, different difficulty.** Euclid works *with* the numbers as given — each step is a
   single division, and the inputs shrink geometrically, so the cost is logarithmic in their size.
   Factoring must *discover* structure that is not present in the representation; nothing in the
   digits of $n$ points at $p$. Euclid exploits an algebraic identity ($\gcd(a,b)=\gcd(b,a\bmod b)$);
   factoring has no comparable reduction.

2. **If factoring became easy.** RSA would break immediately, along with much of TLS, code signing,
   and older PGP. In practice systems would migrate to problems believed hard for other reasons —
   elliptic curves (though Shor breaks those too), or lattice-based post-quantum schemes. **The
   deeper point: RSA's security was never proved, so this is a live risk rather than a hypothetical
   one**, and it is why NIST has been standardising post-quantum algorithms.

3. **Why not roll your own.** The mathematics is correct and complete, and a production
   implementation would still fail. Textbook RSA is deterministic, so identical plaintexts give
   identical ciphertexts; small messages with small $e$ can be recovered by an ordinary integer
   $e$-th root; and the running time of `mod_pow` leaks bits of $d$ to anyone who can measure
   decryption latency. Real implementations add randomised padding, constant-time arithmetic, and
   careful primality testing. **The theorem is the easy part.**

---

## Checkoff Summary

| Section | Watch for |
|---|---|
| 1 | All four hand exercises correct |
| 2.2 | Bézout verified, including a case with $a<b$ |
| 2.3 | The $k-1$ step pattern identified, not just "it's fast" |
| 3.1 | Count recognised as $\varphi(m)$ |
| 3.3 | Zero Euler failures reported |
| 3.4 | Both systems confirmed by brute force |
| 4.2 | **Zero** round-trip failures on both keys |
| 4.3 | `None` explained as the key-generation constraint |
| 4.4 | Extrapolation attempted with real numbers |
| 5 | All three library comparisons clean |

---

*MATH 151 · Week 12 · Lab 12 Solutions · Instructor copy — do not distribute*
