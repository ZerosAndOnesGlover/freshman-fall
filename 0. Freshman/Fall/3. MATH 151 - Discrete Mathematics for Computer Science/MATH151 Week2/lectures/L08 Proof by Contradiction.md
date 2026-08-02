# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 2.3 (L08) — Proof by Contradiction
### Friday, Week 2

---

> **Core Question:** How do we prove something is true by showing that assuming it is false leads to an impossible situation?

---

## 1. The Logical Basis

**Proof by contradiction** (also called *reductio ad absurdum*) rests on the tautology:

**(¬P → F) → P**

If assuming ¬P leads to a contradiction (a false statement, denoted F), then ¬P must be false, meaning P must be true.

Equivalently, in classical logic: **¬(¬P) ≡ P** (double negation).

More generally, to prove P → Q by contradiction:
- Assume P ∧ ¬Q (the hypothesis holds but the conclusion fails)
- Derive a contradiction — a statement of the form R ∧ ¬R
- Conclude: P ∧ ¬Q is impossible, so P → Q must hold

---

## 2. The Structure of a Contradiction Proof

1. State "Proof by contradiction."
2. **Assume the negation** of what you want to prove.
3. Derive consequences by valid steps.
4. Arrive at a **contradiction** — an explicit statement that is false (typically A ∧ ¬A, or an arithmetic impossibility).
5. State: "This is a contradiction. Therefore our assumption was false, and [the original claim] holds." ∎

---

## 3. Worked Examples

### Example 1: √2 Is Irrational

**Theorem.** √2 is irrational.

This is one of the oldest and most beautiful proofs in mathematics, attributed to the ancient Greeks (possibly Hippasus of Metapontum, ca. 450 BC). It allegedly shocked the Pythagoreans, who believed all quantities were commensurable (rational).

**Proof.**
Suppose, for contradiction, that √2 is rational.

Then there exist integers p and q with q ≠ 0 such that √2 = p/q.

We may assume this fraction is in **lowest terms** — meaning gcd(p, q) = 1, so p and q share no common factor. (Every rational number can be written in lowest terms.)

Squaring both sides:
$$2 = \frac{p^2}{q^2}$$
$$p^2 = 2q^2$$

This means p² is even (it equals 2q², which is divisible by 2).

By the theorem proved in Lecture 2.2 (if n² is even then n is even), p is even.

Since p is even, p = 2k for some integer k.

Substituting:
$$(2k)^2 = 2q^2$$
$$4k^2 = 2q^2$$
$$q^2 = 2k^2$$

This means q² is even, which (by the same theorem) means q is even.

But now both p and q are even — contradicting our assumption that p/q is in lowest terms (since gcd(p,q) ≥ 2).

**Contradiction.** Our assumption that √2 is rational must be false.

Therefore, √2 is irrational. ∎

**Why does this proof work?** The key move is the "lowest terms" assumption — by assuming the fraction is fully reduced, we set up a situation where the argument must eventually force both p and q to share a common factor. This is a contradiction of "lowest terms." The proof is self-undermining.

**Connection to infinite regress:** An equivalent way to see why this works: if √2 = p/q in lowest terms, we derived that both p = 2k and q is even, so √2 = 2k/q, which further reduces... and this reduction process never terminates for an irrational number.

---

### Example 2: There Are Infinitely Many Primes

**Theorem.** There are infinitely many prime numbers.

This is Euclid's proof (*Elements*, Book IX, Proposition 20), written around 300 BC. It remains one of the finest proofs ever written.

**Proof.**
Suppose, for contradiction, that there are finitely many primes.

List them all: p₁, p₂, p₃, …, pₙ.

Consider the number:
$$N = p_1 \cdot p_2 \cdot p_3 \cdots p_n + 1$$

N is greater than 1, so N has at least one prime factor. Call it p.

Since p₁, p₂, …, pₙ is our complete list of all primes, p must equal pᵢ for some i.

But then pᵢ | N and pᵢ | (p₁ · p₂ · … · pₙ).

Therefore pᵢ | (N − p₁ · p₂ · … · pₙ) = 1.

But no prime divides 1 (since all primes are ≥ 2 and 1/p < 1 for any prime p).

**Contradiction.** Our assumption that the list p₁, …, pₙ contains all primes must be false.

Therefore there are infinitely many primes. ∎

**Common Misconception:** Students often think the proof claims "p₁p₂…pₙ + 1 is prime." It does NOT. For example, 2 · 3 · 5 · 7 · 11 · 13 + 1 = 30031 = 59 × 509, which is composite. The proof only uses the fact that N has SOME prime factor — which is guaranteed — and that this prime factor cannot be on our list.

---

### Example 3: √3 Is Irrational

**Theorem.** √3 is irrational.

**Proof.**
Suppose, for contradiction, that √3 is rational.

Then √3 = p/q in lowest terms, so p² = 3q².

Thus 3 | p².

By the result from Lecture 2.2 Example 5 (if 3 | n², then 3 | n), we have 3 | p.

So p = 3k for some integer k.

Substituting: (3k)² = 3q², so 9k² = 3q², so q² = 3k².

Thus 3 | q², which means 3 | q.

Both p and q are divisible by 3, contradicting gcd(p,q) = 1.

Therefore √3 is irrational. ∎

---

### Example 4: No Rational Solution to x² = 2 (Algebraic Version)

**Theorem.** The equation x² = 2 has no rational solution.

(This is equivalent to Example 1, stated differently.)

**Proof.**
Suppose x = p/q ∈ ℚ satisfies x² = 2, with gcd(p,q) = 1.

Then (p/q)² = 2, so p² = 2q².

The rest follows as in Example 1. ∎

---

### Example 5: Contradiction Proving a Concrete Uniqueness

**Theorem.** The equation 3x + 4y = 1 has no solution where both x and y are positive integers.

**Proof.**
Suppose for contradiction that x, y ∈ ℤ⁺ satisfy 3x + 4y = 1.

Since x ≥ 1 and y ≥ 1:
$$3x + 4y \geq 3(1) + 4(1) = 7 > 1$$

But we assumed 3x + 4y = 1. This contradicts 3x + 4y ≥ 7 > 1.

**Contradiction.** No positive integer solution exists. ∎

---

### Example 6: Log₂ 3 Is Irrational

**Theorem.** log₂ 3 is irrational.

**Proof.**
Suppose log₂ 3 = p/q for integers p, q with q > 0 and gcd(p,q) = 1.

By definition of logarithm: 2^(p/q) = 3.

Raising both sides to the q-th power: 2^p = 3^q.

The left side is a power of 2, so it is even.
The right side is a power of 3, which is odd (since 3^q is odd for all q).

An even number cannot equal an odd number.

**Contradiction.** Therefore log₂ 3 is irrational. ∎

**Note:** This argument uses the Fundamental Theorem of Arithmetic (unique prime factorization) — the left side has only 2 as a prime factor, while the right side has only 3.

---

## 4. Contradiction vs Contrapositive — Relationship

Proof by contrapositive is actually a special case of proof by contradiction:

To prove P → Q by contradiction, assume P ∧ ¬Q and derive contradiction.
To prove P → Q by contrapositive, assume ¬Q and derive ¬P.

If you assume ¬Q and derive ¬P, then P and ¬P together give the contradiction P ∧ ¬P.

So the contrapositive proof IS a contradiction proof — just a structured version where the contradiction is always "P ∧ ¬P" with ¬P derived directly.

**Preference:** When possible, prefer contrapositive — it is more direct and the structure is cleaner. Use full contradiction when:
- The claim is not an implication (e.g., "√2 is irrational" is not naturally P → Q)
- The contradiction arises from a source other than the negation of P
- You are proving a "no solution exists" result

---

## 5. Proving Existence by Contradiction

Contradiction is also used to prove that something exists, by showing that its non-existence leads to absurdity.

**Example:** "Between any two distinct rationals, there is another rational."

(Proved constructively — take the average. But for non-constructive existence proofs, contradiction is essential.)

**Non-constructive existence:** In some advanced mathematics, we can prove something exists without exhibiting it — only by showing its non-existence is contradictory. This is valid in classical logic but rejected by *constructive* mathematics (where a proof of existence must produce a witness).

For this course, we use classical logic.

---

## 6. The Infinite Descent Technique

A related method, used by Fermat, is **infinite descent**:

1. Assume the statement is false.
2. Show that if it fails for some value n, it fails for a smaller value n' < n.
3. This process can continue indefinitely — giving an infinite decreasing sequence of positive integers.
4. But the positive integers are well-ordered (no infinite decreasing sequence exists).
5. **Contradiction.**

This is essentially induction in disguise. We will revisit it in Week 3.

---

## 7. Summary — All Three Techniques

| Technique | Assume | Derive | Conclude |
|---|---|---|---|
| **Direct** | P | Q step by step | P → Q |
| **Contrapositive** | ¬Q | ¬P step by step | P → Q (via contrapositive) |
| **Contradiction** | ¬(P→Q) = P ∧ ¬Q | R ∧ ¬R (any contradiction) | P → Q |

**The universal principle:** In each case, you are establishing that a certain assumption leads to a true statement (direct), an equivalent statement (contrapositive), or an impossible statement (contradiction). All three are valid.

---

## 8. End-of-Lecture Exercises

1. Prove each by contradiction:
   - (a) √5 is irrational.
   - (b) √6 is irrational. *(Hint: If √6 = p/q, then p² = 6q² = 2 · 3 · q². Use Euclid's lemma or the approach from Example 3 twice.)*
   - (c) log₂ 5 is irrational.
   - (d) There is no greatest even integer.

2. Prove by contradiction: If n² is odd, then n is odd.
   Then compare your proof to the contrapositive proof of the same statement. Which do you prefer and why?

3. **Euclid's proof, analyzed:**
   - (a) In Example 2, why can't we simply say "N = p₁p₂…pₙ + 1 is prime, and it's not in our list, contradiction"?
   - (b) Compute N for the list {2, 3, 5}. Is N prime? For the list {2, 3, 5, 7}?
   - (c) The proof shows any *finite* list of primes is incomplete. Can you construct an infinite list of primes directly from Euclid's argument? What would that look like?

4. Prove: There is no integer n such that n ≡ 1 (mod 4) and n ≡ 3 (mod 4) simultaneously.
   *(You may use: n ≡ r (mod m) means m | (n − r).)*

5. **Open-ended:** The proof that √2 is irrational uses the fact that 2 is prime (specifically, that 2 | p² implies 2 | p). Which step of the proof would fail if we replaced 2 with 4 (attempting to show √4 is irrational)? Why does the proof correctly *fail* for √4?

---

*Week 2 complete. Week 3: Proof by Mathematical Induction — weak and strong.*
