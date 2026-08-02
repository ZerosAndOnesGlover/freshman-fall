# MATH 151 — Week 2
## LAB2 Solutions — INSTRUCTOR ONLY

---

## Section 1 — Technique Identification

### 1.1 — If 6|n, then 3|n.
- P: "6|n", Q: "3|n"
- Contrapositive: "If 3∤n, then 6∤n."
- Contradiction assumption: "6|n and 3∤n."
- **Best technique: Direct.** Hypothesis 6|n gives n=6k immediately. Then n=6k=3(2k), so 3|n. One line.

### 1.2 — If 5|n², then 5|n.
- P: "5|n²", Q: "5|n"
- Contrapositive: "If 5∤n, then 5∤n²."
- Contradiction assumption: "5|n² and 5∤n."
- **Best technique: Contrapositive.** Assuming 5∤n gives n=5q+r (r∈{1,2,3,4}) — algebraically concrete. Assuming 5|n² gives n²=5k — harder to use.

### 1.3 — If a+b is odd, then exactly one of a,b is even.
- P: "a+b is odd", Q: "exactly one of a,b is even"
- Contrapositive: "If a and b have the same parity (both even or both odd), then a+b is even."
- Contradiction: "a+b is odd and (a,b both even OR a,b both odd)."
- **Best technique: Contrapositive.** ¬Q (same parity) gives two clean cases; direct from "a+b = odd" is harder to decompose.

### 1.4 — √11 is irrational.
- Not an implication. Claim C: "√11 ∉ ℚ."
- Contradiction assumption: "√11 = p/q in lowest terms."
- **Best technique: Contradiction.** Standard irrationality proof structure.

### 1.5 — If xy > 0, then (x > 0 and y > 0) or (x < 0 and y < 0).
- P: "xy > 0", Q: "both positive or both negative"
- Contrapositive: "If x and y don't have the same sign, then xy ≤ 0."
- **Best technique: Contrapositive.** ¬Q (opposite signs or one is zero) is extremely concrete; from xy>0 alone the algebra is awkward.

### 1.6 — If 4|(n²−1), then n is odd.
- P: "4|(n²−1)", Q: "n is odd"
- Contrapositive: "If n is even, then 4∤(n²−1)."
- **Best technique: Contrapositive.** Assuming n=2k gives n²−1=4k²−1, and 4∤(4k²−1) since 4k²−1 ≡ 3 (mod 4). Very clean.

### 1.7 — No integer n < 10 satisfies n≡2(mod 4) and n≡0(mod 6) except n=6.
- This is not a universal P→Q. It's a claim about finitely many cases.
- **Best technique: Direct exhaustive check**, or Direct proof ruling out cases. Not a typical implication — check all n<10 satisfying one condition and verify the other.

---

## Section 2 — Proofs from Scratch

### Exercise 2.1(a) — 8|(n²−1) when n is odd.

**Proof.** [Direct]
Assume n is odd. Then n = 2k+1 for some k ∈ ℤ.
n² − 1 = (2k+1)² − 1 = 4k² + 4k + 1 − 1 = 4k² + 4k = 4k(k+1).
Since k and k+1 are consecutive integers, one of them is even. So k(k+1) = 2m for some m ∈ ℤ.
Then n²−1 = 4·2m = 8m.
Since m ∈ ℤ, 8|(n²−1). ∎

*Grading note:* Key step is recognizing k(k+1) is even (product of consecutive integers). Award full credit for any correct argument establishing this, including cases (k even / k odd).

### Exercise 2.1(b) — Sum of three consecutive integers divisible by 3.

**Proof.** [Direct]
Let the three consecutive integers be n, n+1, n+2.
Their sum is n + (n+1) + (n+2) = 3n + 3 = 3(n+1).
Since n+1 ∈ ℤ, 3|(3(n+1)). ∎

### Exercise 2.1(c) — If a|b, then a|(b²−b).

**Proof.** [Direct]
Assume a|b. Then b = ka for some k ∈ ℤ.
b² − b = b(b−1) = (ka)(ka−1) = a[k(ka−1)].
Since k(ka−1) ∈ ℤ, a|(b²−b). ∎

### Exercise 2.2(a) — If n²−1 is even, then n is odd.

Contrapositive: if n is even, then n²−1 is odd.

**Proof.** [Contrapositive]
We prove: if n is even, then n²−1 is odd.
Assume n is even. Then n = 2k.
n²−1 = 4k²−1 = 2(2k²−1)+1.
Since 2k²−1 ∈ ℤ, n²−1 is odd.
By contrapositive, if n²−1 is even then n is odd. ∎

### Exercise 2.2(b) — If a²+b² is odd, then a+b is odd.

Contrapositive: if a+b is even, then a²+b² is even.

**Proof.** [Contrapositive]
We prove: if a+b is even, then a²+b² is even.
Assume a+b is even. Then a and b have the same parity.

Case 1: both even. a=2j, b=2k. a²+b²=4j²+4k²=2(2j²+2k²). Even.

Case 2: both odd. a=2j+1, b=2k+1. a²+b²=(4j²+4j+1)+(4k²+4k+1)=4j²+4j+4k²+4k+2=2(2j²+2j+2k²+2k+1). Even.

In both cases a²+b² is even. By contrapositive, the result follows. ∎

### Exercise 2.3(a) — √13 is irrational.

**Proof.** [Contradiction]
Suppose √13 = p/q in lowest terms, gcd(p,q)=1.
Then p² = 13q², so 13|p².
Since 13 is prime and 13|p², we have 13|p.
Write p = 13k: 169k² = 13q², so q² = 13k², so 13|q.
Both 13|p and 13|q contradict gcd(p,q)=1. ∎

### Exercise 2.3(b) — No greatest odd integer.

**Proof.** [Contradiction]
Suppose N is the greatest odd integer.
Consider N+2. Since N is odd, N = 2k+1, so N+2 = 2k+3 = 2(k+1)+1, which is odd.
Moreover N+2 > N.
This contradicts N being the greatest odd integer.
Therefore no greatest odd integer exists. ∎

---

## Section 3 — Proof Critique and Repair

### Flawed Proof 3.1

**Claim:** 4|n² → 4|n.

**Errors:**
1. The step "n = 2√k" takes a square root with no justification that √k is an integer.
2. The step "4|n² and n=2m, hence 4|n" assumes the conclusion — n=2m means 2|n, which does not imply 4|n.
3. The reasoning is circular.

**The claim is FALSE.** Counterexample: n=2. n²=4, and 4|4, but 4∤2.

**Correct statement:** If 4|n², then 2|n (n is even).

**Correct proof (contrapositive):** If n is odd, then 4∤n².
Assume n=2k+1. Then n²=4k²+4k+1=4(k²+k)+1. Since 4(k²+k)+1 ≡ 1 (mod 4), 4∤n². ∎

---

### Flawed Proof 3.2

**Claim:** If n is odd, then n²+n+1 is odd.

**Errors:** None — the proof is CORRECT. n odd → n² odd → n²+n even (odd+odd) → n²+n+1 odd (even+1). Each step is valid.

*Grading note:* This is a "trick" problem — students should recognize a valid proof. Award full marks for "no errors; proof is correct."

---

### Flawed Proof 3.3

**Claim:** If a|b and b|a, then a=b.

**Errors:**
1. "Dividing by b" is only valid when b≠0. The proof doesn't handle b=0.
2. From jk=1 with j,k integers: this gives j=k=1 OR j=k=−1. The proof ignores j=k=−1.
3. If j=k=−1: b=−a, so b≠a in general.

**The claim is FALSE.** Counterexample: a=3, b=−3. 3|(−3) ✓ and (−3)|3 ✓, but 3≠−3.

**Corrected claim:** If a|b and b|a, then a=±b (i.e., |a|=|b|).

**Correct proof:**
Assume a|b and b|a. Then b=ja and a=kb for integers j,k.
If b=0: then a=0 (from a=kb=0), so a=b=0. ✓
If b≠0: substitute to get b=j(kb)=jkb. Since b≠0, jk=1. Since j,k∈ℤ, either j=k=1 (giving b=a) or j=k=−1 (giving b=−a). In both cases, a=±b. ∎

---

### Flawed Proof 3.4

**Claim:** If x²=x, then x=1.

**Errors:**
1. "Dividing both sides by x" is invalid when x=0. Division by zero is undefined.

**The claim is FALSE.** x=0 also satisfies x²=x (0²=0).

**Correct proof:**
Assume x²=x. Then x²−x=0, so x(x−1)=0.
By the zero-product property, x=0 or x−1=0, i.e., x=0 or x=1.
So the solutions are x∈{0,1}. ∎

---

### Flawed Proof 3.5

**Error in the argument "√2+√2=2 so √2 is rational":**

**The error is the false premise "√2 + √2 = √4".**

√2 + √2 = 2√2 ≈ 2.828, whereas √4 = 2. These are not equal, so the step that produces a rational
value is simply wrong.

In general **√a + √b ≠ √(a+b)** — the square root does not distribute over addition. (It *does*
distribute over multiplication: √a·√b = √(ab), which is what makes the error tempting.)

Note the conclusion is false as well as the reasoning: √2 is irrational. But a proof can be invalid
even when its conclusion happens to be true, and vice versa — students should be able to say that
this argument establishes nothing either way.

So the "proof" contains a false premise: "√2+√2=√4" is simply wrong. Even if the conclusion were true (which it isn't — √2 is irrational), this argument doesn't establish it.

---

## Section 4 — Gallery Expected Results

**Gallery 1:** n²+1 not prime for infinitely many n.
Work modulo 5. Observe that for n≡2(mod 5): n²+1≡4+1=5≡0(mod 5). So whenever n≡2(mod 5) and n>2 (so n²+1>5), n²+1 is divisible by 5 but greater than 5, hence composite. There are infinitely many such n (e.g., n=2,7,12,17,...). ∎

**Gallery 2:** p²−1 divisible by 8 for prime p>2.
TRUE. Every prime p>2 is odd. Write p=2k+1.
p²−1=(2k+1)²−1=4k²+4k=4k(k+1).
Since k(k+1) is a product of consecutive integers, one is even: k(k+1)=2m.
So p²−1=8m. ∎

**Gallery 3:** log₂6 irrational.
Suppose log₂6=p/q. Then 2^p=6^q=(2·3)^q=2^q·3^q.
So 2^(p−q)=3^q.
If p>q: left side is a power of 2, right side a power of 3. By FTA, impossible unless both equal 1. But 3^q=1 only if q=0, giving log₂6=0, which means 6=1. Contradiction.
If p<q: 1=2^(q−p)·3^q — but right side ≥2. Contradiction.
If p=q: 1=3^q — impossible for q≥1. ∎
