# MATH 151 · Proof Strategies Reference
## Week 2: Direct, Contrapositive, Contradiction

---

## Strategy Selection Guide

```
Given a claim to prove:
│
├─ Is it of the form P → Q?
│   │
│   ├─ Does P give concrete algebraic form?
│   │   (e.g., "n = 2k", "b = ka", "r = p/q")
│   │   └─ YES → Try DIRECT PROOF first
│   │
│   ├─ Does ¬Q give stronger/more concrete info than P?
│   │   (e.g., P is "n² is even" → ¬Q might be "n is odd" = "n = 2k+1")
│   │   └─ YES → Try CONTRAPOSITIVE
│   │
│   └─ Is the conclusion hard to construct, or does
│       assuming P ∧ ¬Q lead quickly to impossibility?
│       └─ YES → Try CONTRADICTION
│
├─ Is it "X does not exist" or "X is irrational"?
│   └─ Try CONTRADICTION (assume X exists / assume X is rational)
│
├─ Is it "There are infinitely many X"?
│   └─ Try CONTRADICTION (assume finitely many)
│
└─ Is it a biconditional P ↔ Q?
    └─ Prove P → Q AND Q → P separately (two proofs)
```

---

## The Three Techniques at a Glance

### Direct Proof

**What you assume:** P (the hypothesis)

**What you derive:** Q (the conclusion)

**Logical basis:** Modus ponens: P, P→Q ⊢ Q

**Best for:**
- When P gives you explicit form: n = 2k, b = ka, r = p/q
- When Q requires constructing a witness (∃ statement)
- Simple divisibility and parity results

**Template:**
```
Assume P.
By definition, [expand P].
[algebraic steps]
By definition, [Q].  ∎
```

---

### Proof by Contrapositive

**What you assume:** ¬Q

**What you derive:** ¬P

**Logical basis:** P→Q ≡ ¬Q→¬P (logical equivalence)

**Best for:**
- When ¬Q is concrete and ¬P is what you need to show
- Statements "if n² has property X, then n has property X"
- When direct proof requires "taking a square root" or similar non-integer operation

**Template:**
```
We prove the contrapositive: [¬Q → ¬P in words].
Assume ¬Q.
By definition, [expand ¬Q].
[algebraic steps]
By definition, [¬P].
Therefore, by contrapositive, P → Q.  ∎
```

---

### Proof by Contradiction

**What you assume:** ¬C (negation of the claim)

**What you derive:** R ∧ ¬R for some proposition R

**Logical basis:** (¬C → F) → C; equivalently ¬(¬C) ≡ C

**Best for:**
- Irrationality proofs (assume rational, derive contradiction)
- "No solution exists" claims
- "Infinitely many X" (assume finitely many)
- Existence proofs when no constructive witness is available
- Any claim where ¬C immediately gives you two conflicting things

**Template:**
```
Suppose, for contradiction, that ¬C.
[Expand ¬C: if C is P→Q, then assume P ∧ ¬Q.]
[Algebraic steps leading to R.]
[Show ¬R also holds.]
This contradicts [R / our assumption / a known fact].
Therefore C.  ∎
```

---

## Key Theorem Inventory (Week 2)

| Theorem | Technique | Key Move |
|---|---|---|
| Even + Even = Even | Direct | 2j + 2k = 2(j+k) |
| Odd × Odd = Odd | Direct | (2j+1)(2k+1) = 2(2jk+j+k)+1 |
| a\|b, b\|c → a\|c | Direct | b=ja, c=kb → c=(kj)a |
| Sum of rationals is rational | Direct | p/q + m/n = (pn+qm)/(qn) |
| n² even → n even | Contrapositive | n odd → n=2k+1 → n²=2(2k²+2k)+1 odd |
| n² odd → n odd | Contrapositive | n even → n=2k → n²=4k²=2(2k²) even |
| ab odd → a,b both odd | Contrapositive | a or b even → ab even |
| 3\|n² → 3\|n | Contrapositive | Use Division Algorithm: r∈{1,2} → n²≡1 (mod 3) |
| √2 irrational | Contradiction | √2=p/q in lowest terms → p,q both even |
| Infinitely many primes | Contradiction | Finite list → N=p₁…pₙ+1 has prime factor not on list |
| √p irrational (p prime) | Contradiction | Same structure as √2, uses p prime → p\|n² → p\|n |
| log₂ 3 irrational | Contradiction | 2^p = 3^q: left even, right odd |

---

## Divisibility Facts (use freely without proof)

- If a | b and a | c, then a | (mb + nc) for any integers m, n
- If a | b, then a | bc for any integer c
- If a | b and b | c, then a | c (transitivity)
- a | 0 for any integer a
- a | a for any integer a
- If a | b and b | a, then a = ±b
- If p is prime and p | ab, then p | a or p | b (Euclid's Lemma — proved Week 4)

---

## Parity Facts (use freely without proof)

| Combination | Parity of sum | Parity of product |
|---|---|---|
| Even + Even | Even | Even |
| Even + Odd | Odd | Even |
| Odd + Odd | Even | Odd |

**Derived facts:**
- n and n+1 have opposite parity (consecutive integers)
- n(n+1) is always even
- n, n+1, n+2 are consecutive → their sum is divisible by 3
- n² has the same parity as n

---

## The Division Algorithm (cite when needed)

For any integers a and d with d > 0, there exist unique integers q and r with 0 ≤ r < d such that:

**a = dq + r**

q is the quotient, r is the remainder.

Applications in proofs:
- "Every integer is of the form 2k or 2k+1" (d=2, r∈{0,1})
- "Every integer is of the form 3k, 3k+1, or 3k+2" (d=3, r∈{0,1,2})
- "Every integer is of the form 4k, 4k+1, 4k+2, or 4k+3" (d=4)

When proving a claim for "all integers n," you can often case-split using the division algorithm with an appropriate d.
