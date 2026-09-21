# MATH 151 · Week 2
## PS2 Solutions — INSTRUCTOR ONLY

---

## Part A — Direct Proof

### A1.

**(a)** If n is odd, then n+1 is even.

**Proof.** Assume n is odd. By definition, n = 2k+1 for some k ∈ ℤ.
Then n+1 = 2k+1+1 = 2k+2 = 2(k+1).
Since k+1 is an integer, n+1 is even. ∎

**(b)** If m is even and n is odd, then m+n is odd.

**Proof.** Assume m is even and n is odd. Then m = 2j and n = 2k+1 for some j,k ∈ ℤ.
Then m+n = 2j + 2k+1 = 2(j+k)+1.
Since j+k ∈ ℤ, m+n is odd. ∎

**(c)** If a|b and a|c, then a|(3b−2c).

**Proof.** Assume a|b and a|c. Then b = ja and c = ka for some j,k ∈ ℤ.
Then 3b−2c = 3(ja)−2(ka) = (3j−2k)a.
Since 3j−2k ∈ ℤ, a|(3b−2c). ∎

**(d)** Product of two rationals is rational.

**Proof.** Let r = p/q and s = m/n with p,q,m,n ∈ ℤ, q≠0, n≠0.
Then rs = (p/q)(m/n) = pm/(qn).
Since pm ∈ ℤ, qn ∈ ℤ, and qn ≠ 0, rs is rational. ∎

**(e)** If n = 4k+1, then n² = 8m+1 for some m ∈ ℤ.

**Proof.** Assume n = 4k+1.
n² = (4k+1)² = 16k²+8k+1 = 8(2k²+k)+1.
Let m = 2k²+k ∈ ℤ. Then n² = 8m+1. ∎

**(f)** n²+n is even for any integer n.

**Proof.** Note n²+n = n(n+1). We consider two cases.

Case 1: n is even. Then n = 2k, so n(n+1) = 2k(n+1) = 2[k(n+1)]. Even.

Case 2: n is odd. Then n+1 is even (n+1 = 2k+1+1 = 2(k+1)). So n(n+1) = n·2(k+1) = 2[n(k+1)]. Even.

In both cases, n²+n is even. ∎

**(g)** If a|b, then a²|b².

**Proof.** Assume a|b. Then b = ka for some k ∈ ℤ.
b² = (ka)² = k²a².
Since k² ∈ ℤ, a²|b². ∎

---

### A2. Flawed proof identification and correction.

**Error in the flawed proof:** The "proof" ends with: "4|n² and n=2m, hence 4|n." This is the conclusion being assumed, not derived. Having n=2m means 2|n, not 4|n. The jump from "n=2m" to "4|n" is unjustified.

**The claim is FALSE.** Counterexample: n = 2. n² = 4 = 4·1, so 4|n². But n = 2, and 4 ∤ 2.

**Correct statement and proof:**

**Corrected Claim:** If n² is divisible by 4, then n is even (i.e., 2|n).

**Proof.** Contrapositive: if n is odd, then n² is not divisible by 4.
Assume n is odd. Then n = 2k+1 for some k ∈ ℤ.
n² = (2k+1)² = 4k²+4k+1 = 4(k²+k)+1.
Since 4(k²+k)+1 leaves remainder 1 when divided by 4, 4 ∤ n². ∎

*Grading: 2 pts for identifying the specific error. 2 pts for correct disproof (counterexample n=2) and correct restated/proved claim.*

---

## Part B — Proof by Contrapositive

### B1.

**(a)** If n² is odd, then n is odd.

Contrapositive: if n is even, then n² is even.

**Proof.** We prove the contrapositive: if n is even, then n² is even.
Assume n is even. Then n = 2k for some k ∈ ℤ.
n² = (2k)² = 4k² = 2(2k²).
Since 2k² ∈ ℤ, n² is even.
By contrapositive, if n² is odd then n is odd. ∎

**(b)** If ab is even, then a is even or b is even.

Contrapositive: if a is odd and b is odd, then ab is odd.

**Proof.** We prove the contrapositive: if a and b are both odd, then ab is odd.
Assume a = 2j+1 and b = 2k+1 for j,k ∈ ℤ.
ab = (2j+1)(2k+1) = 4jk+2j+2k+1 = 2(2jk+j+k)+1.
Since 2jk+j+k ∈ ℤ, ab is odd.
By contrapositive, the original holds. ∎

**(c)** If x+y is irrational, then x is irrational or y is irrational.

Contrapositive: if x and y are both rational, then x+y is rational.

**Proof.** We prove the contrapositive: if x and y are rational, then x+y is rational.
Let x = p/q and y = m/n with q,n ≠ 0.
x+y = (pn+qm)/(qn), where pn+qm ∈ ℤ and qn ≠ 0.
So x+y is rational. By contrapositive, the original holds. ∎

**(d)** If 3 ∤ n, then 9 ∤ n².

Contrapositive: if 9 | n², then 3 | n.

Actually the correct contrapositive of "3∤n → 9∤n²" is "9|n² → 3|n."

**Proof.** We prove the contrapositive: if 9|n², then 3|n.

If 9|n², then 3|n² (since 9|n² means n²=9k, so n²=3(3k), meaning 3|n²).
By Example 5 of Lecture 7 (if 3|n² then 3|n), we conclude 3|n.
By contrapositive, the original holds. ∎

Alternative direct approach for contrapositive:

Assume 3∤n. By division algorithm, n=3q+r with r∈{1,2}.

Case r=1: n²=(3q+1)²=9q²+6q+1=9(q²+⌊6q/9⌋)+... more cleanly: 9q²+6q+1. Then n²=9q²+6q+1. Is 9|n²? We need 9|(9q²+6q+1), i.e., 9|(6q+1). For this to hold for all q... it doesn't always. For example q=0: 9|1 is false. So 9∤n². ✓

Case r=2: n²=(3q+2)²=9q²+12q+4=9(q²+1)+12q+4-9=9(q²+1)+(12q-5)... cleaner: 9q²+12q+4. 9q²+12q+4 mod 9 = 0+3q+4 mod 9 = (3q+4) mod 9. For 9|(3q+4) we need 3q≡5(mod 9), i.e., q≡... this is never 0 mod 9. So 9∤n².

In both cases 9∤n². ∎ (Graders: accept any correct case analysis.)

---

### B2. Technique selection justifications.

**(a)** n³ even → n even. **Contrapositive.** Reason: assuming n³ is even gives n³=2k, but extracting cube root algebraically is messy. The contrapositive (n odd → n³ odd) is clean: n=2k+1 → n³=(2k+1)³, expand and group.

**(b)** 5|n → 5|n². **Direct.** Reason: hypothesis 5|n gives n=5k immediately. Then n²=25k²=5(5k²). Very clean direct proof.

**(c)** a odd and b odd → a+b even. **Direct.** Reason: both hypotheses give explicit form (a=2j+1, b=2k+1), and computing a+b=2(j+k+1) is immediate.

**(d)** x² < x → x < 1. **Contrapositive.** Reason: contrapositive is x≥1 → x²≥x. If x≥1, then x²=x·x≥1·x=x (since x≥1). Clean algebra. Direct proof from x²<x is harder — dividing by x requires checking x>0 separately.

---

## Part C — Proof by Contradiction

### C1.

**(a)** √7 is irrational.

**Proof.** Suppose √7 = p/q in lowest terms (gcd(p,q)=1). Then p²=7q².
So 7|p². Since 7 is prime and 7|p², we have 7|p (Euclid's lemma for primes).
Write p=7k. Then 49k²=7q², so q²=7k². Thus 7|q², so 7|q.
Both 7|p and 7|q contradict gcd(p,q)=1. ∎

**(b)** √(2/3) is irrational.

**Proof.** Suppose √(2/3) = p/q with gcd(p,q)=1.
Then 2/3 = p²/q², so 2q² = 3p².
Thus 2|3p². Since gcd(2,3)=1, we have 2|p², hence 2|p.
Write p=2k: 2q²=3(4k²)=12k², so q²=6k².
Then 2|q², so 2|q.
Both 2|p and 2|q contradict gcd(p,q)=1. ∎

**(c)** log₃ 5 is irrational.

**Proof.** Suppose log₃ 5 = p/q with q>0, gcd(p,q)=1.
Then 3^(p/q) = 5, so 3^p = 5^q.
The left side: 3^p is divisible by 3 but not by 5.
The right side: 5^q is divisible by 5 but not by 3.
But 3^p = 5^q. By unique prime factorization (Fundamental Theorem of Arithmetic), the prime factorizations of both sides must be identical. The left side has only 3 as a prime factor; the right side has only 5. These are different primes, so this is impossible unless both sides equal 1 — but 3^p ≥ 3 and 5^q ≥ 5 for p,q ≥ 1.
(If p=0: 1 = 5^q, impossible for q≥1. If p<0: 3^p < 1 < 5^q, impossible.)
Contradiction. ∎

**(d)** No rational r has r²=6.

**Proof.** Suppose r=p/q ∈ ℚ with r²=6 and gcd(p,q)=1.
Then p²=6q²=2·3·q².
So 2|p², hence 2|p. Write p=2k: 4k²=6q², so 2k²=3q².
Thus 2|3q². Since gcd(2,3)=1, 2|q², so 2|q.
Both 2|p and 2|q contradict gcd(p,q)=1. ∎

**(e)** If 5|n², then 5|n.

**Technique choice:** Contrapositive is cleaner here.

**Proof (contrapositive).** We prove: if 5∤n, then 5∤n².
Assume 5∤n. By division algorithm, n=5q+r with r∈{1,2,3,4}.

Case r=1: n²=(5q+1)²=25q²+10q+1=5(5q²+2q)+1. So n²≡1(mod 5), thus 5∤n².
Case r=2: n²=(5q+2)²=25q²+20q+4=5(5q²+4q)+4. n²≡4(mod 5), 5∤n².
Case r=3: n²=(5q+3)²=25q²+30q+9=5(5q²+6q+1)+4. n²≡4(mod 5), 5∤n².
Case r=4: n²=(5q+4)²=25q²+40q+16=5(5q²+8q+3)+1. n²≡1(mod 5), 5∤n².

In all cases, 5∤n². By contrapositive, the result follows. ∎

---

### C2. Infinitely many primes of the form 4k+3.

**Proof.** Suppose for contradiction that there are finitely many primes of the form 4k+3: list them as p₁, p₂, …, pₙ.

Consider N = 4p₁p₂…pₙ − 1.

Note: N = 4(p₁p₂…pₙ) − 1 = 4(p₁p₂…pₙ - 1) + 3. So N is of the form 4m+3 (with m = p₁p₂…pₙ − 1).

Since N > 1, N has at least one prime factor. The key observation: if all prime factors of N were of the form 4k+1, then N itself would be of the form 4k+1 (since the product of numbers ≡1 mod 4 is ≡1 mod 4). But N ≡ 3 (mod 4), so N must have at least one prime factor q of the form 4k+3.

This prime q cannot be any of p₁, …, pₙ: for each pᵢ, we have pᵢ | (4p₁…pₙ), so pᵢ | (N − 4p₁…pₙ) = −1, meaning pᵢ | 1. Impossible since pᵢ ≥ 3.

So q is a prime of the form 4k+3 not in our list. Contradiction. ∎

*Grading note: This is significantly harder than C1. Give 4 pts for a complete correct proof. Give 2 pts for a proof that correctly identifies N and explains why N must have a 4k+3 factor, even if the exclusion from the list is not cleanly argued.*

---

### C3. Flaw in the √4 "proof."

**The flaw:** The step "Since k² = q², thus q = ±k, and gcd(p,q) = gcd(2k,k) = k" is incorrect reasoning, AND the proof doesn't actually reach a contradiction for ALL cases.

Specifically: from p = 2k and q² = k², we get q = ±k (since q is a positive integer, q = k). Then p = 2k and q = k, so gcd(p,q) = gcd(2k,k) = k. For gcd(p,q) = 1 (our assumption), we need k = 1. When k = 1: p = 2, q = 1. Then √4 = p/q = 2/1 = 2, which IS an integer (and hence rational). 

So the proof fails because it only shows a contradiction when k > 1. When k = 1, there is no contradiction — and indeed √4 = 2 = 2/1 IS rational. The "proof" breaks down because k = 1 is a valid solution.

**Why the √2 proof doesn't have this problem:** In the √2 proof, after finding that both p and q are even, we can write p = 2j and q = 2m and substitute back to get √2 = 2j/2m = j/m, which is in lower terms — triggering an infinite descent argument (every pair leads to a smaller pair). For √2, there is no "bottoming out" at a valid rational representation; the descent never terminates. For √4, the descent terminates at p=2, q=1, which is a valid representation.

The essential issue: the irrationality proof relies on the fact that √n has no finite representation as p/q. For √4 = 2, such a representation exists, so the argument cannot reach a true contradiction.

---

## Part D — Mixed

### D1. n(n+1)(n+2) divisible by 6.

**Technique:** Direct proof with cases (mod 3) + parity argument.

**Proof.** We show 2 | n(n+1)(n+2) and 3 | n(n+1)(n+2) separately, then since gcd(2,3)=1, their product 6 divides n(n+1)(n+2).

**2 | n(n+1)(n+2):** Among any two consecutive integers, one is even. In particular n and n+1 are consecutive, so one of them is even. Thus 2 | n(n+1), and hence 2 | n(n+1)(n+2).

**3 | n(n+1)(n+2):** By the division algorithm, n ≡ 0, 1, or 2 (mod 3).
- If n ≡ 0 (mod 3): 3|n, so 3|n(n+1)(n+2).
- If n ≡ 1 (mod 3): n+2 ≡ 0 (mod 3), so 3|(n+2), hence 3|n(n+1)(n+2).
- If n ≡ 2 (mod 3): n+1 ≡ 0 (mod 3), so 3|(n+1), hence 3|n(n+1)(n+2).

In all cases 3 | n(n+1)(n+2). Since 2 and 3 both divide n(n+1)(n+2) and gcd(2,3)=1, we have 6 | n(n+1)(n+2). ∎

**Technique justification:** Direct proof is most natural — the hypothesis is empty (the claim is about all n) and the structure invites case analysis.

---

### D2. n is odd ↔ n² is odd. (Both directions.)

**(→) If n is odd, then n² is odd. [Direct proof.]*

**Proof.** Assume n is odd. Then n = 2k+1 for some k ∈ ℤ.
n² = (2k+1)² = 4k²+4k+1 = 2(2k²+2k)+1.
Since 2k²+2k ∈ ℤ, n² is odd. ∎

**(←) If n² is odd, then n is odd. [Contrapositive.]*

**Proof.** We prove the contrapositive: if n is even, then n² is even.
Assume n is even. Then n = 2k for some k ∈ ℤ.
n² = 4k² = 2(2k²). Since 2k² ∈ ℤ, n² is even.
By contrapositive, if n² is odd then n is odd. ∎

---

### D3.

**(a)** Every contrapositive proof is a contradiction proof:

To prove P→Q by contrapositive, we assume ¬Q and derive ¬P.

In contradiction terms: we assume P ∧ ¬Q. We then derive ¬P (as in the contrapositive proof). But we assumed P. So we have P ∧ ¬P — a contradiction. The contradiction IS the simultaneous truth of P (assumed) and ¬P (derived).

**(b)** Can every contradiction proof be converted to contrapositive?

Not always cleanly. Contradiction proofs that are NOT implications — e.g., "√2 is irrational," "there are infinitely many primes" — are not of the form P→Q, so the contrapositive (¬Q→¬P) doesn't apply.

For proofs of implications P→Q: if the contradiction proof derives ¬P from P ∧ ¬Q, then yes — the derivation of ¬P from ¬Q is exactly a contrapositive proof (discarding the unused P assumption). But if the contradiction uses BOTH P and ¬Q to derive the contradiction (neither alone being the explicit contradiction), then converting to contrapositive may not be clean.

Example where contradiction is essential: "√2 is irrational" — there is no natural implication P→Q here to take the contrapositive of.

---

### D4. Euclid's Lemma: if a|bc and gcd(a,b)=1, then a|c.

**Proof.** Assume a|bc and gcd(a,b)=1.

By Bézout's Identity (given), there exist integers x, y such that ax + by = 1.

Multiplying both sides by c:
acx + bcy = c.

Now a | acx (since acx = a(cx)).
Since a | bc, we have a | bcy (since bcy = (bc)y).

Therefore a | (acx + bcy) = c. ∎

**Why each hypothesis is necessary:**

- If we drop gcd(a,b)=1: counterexample a=4, b=2, c=3. a|bc (4|6? No, 4∤6). Bad example. Try: a=4, b=2, c=6. bc=12, 4|12 ✓. But 4∤6. So gcd(4,2)=2≠1 and the conclusion fails.

- If we drop a|bc: trivially, a need not divide c. E.g., a=3, b=1, c=5. gcd(3,1)=1, 3∤5.

Both hypotheses are essential.

---

### D5.

**(a)** If a|(b+c), then a|b or a|c. **FALSE.**
Counterexample: a=3, b=1, c=2. a|(b+c) since 3|3 ✓. But 3∤1 and 3∤2. ✗

**(b)** If a|bc, then a|b or a|c. **FALSE.**
Counterexample: a=4, b=6, c=2. a|bc: 4|12 ✓. But 4∤6 and 4∤2. ✗

**(c)** If p is prime and p|ab, then p|a or p|b. **TRUE.** This is Euclid's Lemma for primes.

**Proof.** Suppose p|ab and p∤a. We show p|b.
Since p is prime and p∤a, gcd(p,a)=1 (the only positive divisors of p are 1 and p; since p∤a, their gcd isn't p, so it's 1).
By Euclid's Lemma (D4): since p|ab and gcd(p,a)=1, we have p|b. ∎

**The contrast between (b) and (c):** The key is that primality of a gives gcd(a,b)=1 whenever a∤b, which is the hypothesis needed for Euclid's Lemma. For composite a (like 4), gcd(4,6)=2≠1, so the lemma doesn't apply.
