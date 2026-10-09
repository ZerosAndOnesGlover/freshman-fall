# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 4 (L04) — Negating Quantified Statements and Logical Equivalences
### Thursday, Week 1

*“The two eyes of exact science are mathematics and logic: the mathematical sect puts out the logical eye, the logical sect puts out the mathematical eye; each believing that it can see better with one eye than with two.”* — Augustus De Morgan, as quoted in Florian Cajori, *A History of Mathematics* (1894)

**Date:** Thursday 1 October 2026 · 13:00–13:50 · Week 1

**Reading:** Rosen, 8e §1.4 · Epp, 5e §3.2 · Levin, 3e §0.2 *(details at the end of the lecture)*

**Coursework:** 📝 **PS 0** due Fri 2 Oct 17:00 · 📝 **PS 1** released Fri 2 Oct 14:00, due Fri 9 Oct 17:00 · 📊 **Quiz 2** Mon 5 Oct 13:00–13:15 · 🔬 **Lab 1** Wed 7 Oct 15:00–16:50

---

> **Core Question:** What does it mean to negate a quantified statement, and what algebraic laws govern predicate logic?

---

## 1. Why Negation of Quantifiers Matters

Negation is one of the most frequently needed operations in mathematical proofs. When you attempt to prove a statement by contradiction, you assume its negation. When you try to disprove a claim, you prove its negation. When you debug a program specification, you examine what the negation of a contract looks like.

Getting negation of quantified statements wrong is one of the most common errors in mathematical writing. This lecture fixes that permanently.

---

## 2. De Morgan's Laws for Quantifiers

Recall De Morgan's Laws for propositional logic:
- ¬(P ∧ Q) ≡ ¬P ∨ ¬Q
- ¬(P ∨ Q) ≡ ¬P ∧ ¬Q

Since ∀ is a generalized ∧ and ∃ is a generalized ∨, there are analogous laws for quantifiers.

---

### Law 1: Negation of a Universal

**¬(∀x P(x)) ≡ ∃x ¬P(x)**

*Reading:* "Not every x satisfies P" means "there exists some x that does not satisfy P."

**Proof of equivalence:**

∀x P(x) is false ↔ P(a) is false for some a in the domain
                  ↔ ¬P(a) is true for some a in the domain
                  ↔ ∃x ¬P(x) is true

So ¬(∀x P(x)) is true precisely when ∃x ¬P(x) is true. ∎

**Example:**
- Statement: ∀x ∈ ℤ, x² > 0 — "Every integer has positive square"
- Negation: ∃x ∈ ℤ, x² ≤ 0 — "Some integer has non-positive square"
- The negation is true (witness: x = 0, since 0² = 0 ≤ 0).
- Therefore the original statement is false.

---

### Law 2: Negation of an Existential

**¬(∃x P(x)) ≡ ∀x ¬P(x)**

*Reading:* "There is no x satisfying P" means "every x fails to satisfy P."

**Proof of equivalence:**

∃x P(x) is false ↔ P(a) is false for every a in the domain
                  ↔ ¬P(a) is true for every a in the domain
                  ↔ ∀x ¬P(x) is true ∎

**Example:**
- Statement: ∃x ∈ ℤ, x² < 0 — "Some integer has negative square"
- Negation: ∀x ∈ ℤ, x² ≥ 0 — "Every integer has non-negative square"
- The negation is true (squares of real integers are always ≥ 0).
- Therefore the original statement is false.

---

### The Pattern

| Original | Negation | Rule |
|---|---|---|
| ∀x P(x) | ∃x ¬P(x) | Flip quantifier, negate predicate |
| ∃x P(x) | ∀x ¬P(x) | Flip quantifier, negate predicate |

**Mnemonic:** To negate a quantified statement, *flip the quantifier* (∀↔∃) and *negate the predicate*.

---

## 3. Pushing Negations Inward — Worked Examples

When negating complex quantified statements, push the negation sign as far inward as possible, flipping quantifiers as you go.

### Example 1

Negate: ∀x ∈ ℝ, (x > 0 → ∃y ∈ ℝ, y² = x)

**Step 1:** Apply Law 1 — flip ∀ to ∃, negate the body:
¬(∀x ∈ ℝ, (x > 0 → ∃y ∈ ℝ, y² = x))
≡ ∃x ∈ ℝ, ¬(x > 0 → ∃y ∈ ℝ, y² = x)

**Step 2:** Negate the conditional — recall ¬(P → Q) ≡ P ∧ ¬Q:
≡ ∃x ∈ ℝ, (x > 0 ∧ ¬∃y ∈ ℝ, y² = x)

**Step 3:** Apply Law 2 — flip ∃ to ∀, negate the predicate:
≡ ∃x ∈ ℝ, (x > 0 ∧ ∀y ∈ ℝ, y² ≠ x)

**Reading:** "There exists a positive real number x such that no real number y satisfies y² = x."

This is the negation of "every positive real has a real square root." The negation says "some positive real has no real square root." (Over ℝ, the negation is FALSE — every positive real does have a square root. So the original is TRUE.)

### Example 2

Negate: ∃x ∈ ℤ, (x is prime ∧ x is even)

¬(∃x ∈ ℤ, (P(x) ∧ E(x)))
≡ ∀x ∈ ℤ, ¬(P(x) ∧ E(x))     [Law 2]
≡ ∀x ∈ ℤ, (¬P(x) ∨ ¬E(x))    [De Morgan for ∧]
≡ ∀x ∈ ℤ, (P(x) → ¬E(x))     [Conditional Equivalence]

**Reading:** "Every prime integer is odd." (The original claims there exists an even prime — which is true, namely 2. So the negation is false.)

### Example 3

Negate the claim: "Every CS student has taken at least one math course."

Domain: students. C(x) = "x is a CS student", M(x) = "x has taken at least one math course."

Original: ∀x (C(x) → M(x))
Negation: ∃x ¬(C(x) → M(x))
        ≡ ∃x (C(x) ∧ ¬M(x))

**Reading:** "There exists a CS student who has taken no math course." Exactly right — to disprove "every CS student took math," you find one CS student who hasn't.

---

## 4. Logical Equivalences Involving Quantifiers

These are the algebraic laws for predicate logic. They hold for any predicate P(x), Q(x) over any domain.

### 4.1 Distribution Laws

| Law | Formula |
|---|---|
| ∀ distributes over ∧ | ∀x (P(x) ∧ Q(x)) ≡ (∀x P(x)) ∧ (∀x Q(x)) |
| ∃ distributes over ∨ | ∃x (P(x) ∨ Q(x)) ≡ (∃x P(x)) ∨ (∃x Q(x)) |

**Warning — the following do NOT hold in general:**

| Invalid | Counterexample |
|---|---|
| ∀x (P(x) ∨ Q(x)) ≢ (∀x P(x)) ∨ (∀x Q(x)) | P(x) = "x is even", Q(x) = "x is odd": left side true (every integer is even or odd), right side false (not all integers are even, not all are odd) |
| ∃x (P(x) ∧ Q(x)) ≢ (∃x P(x)) ∧ (∃x Q(x)) | Right implies left but not vice versa — could have x₁ satisfying P and different x₂ satisfying Q |

### 4.2 Scope Extension Laws

When a variable does not appear free in one part of a formula:

| Law | Condition | Formula |
|---|---|---|
| ∀ scope extension | x not free in Q | ∀x (P(x) ∧ Q) ≡ (∀x P(x)) ∧ Q |
| ∀ scope extension | x not free in Q | ∀x (P(x) ∨ Q) ≡ (∀x P(x)) ∨ Q |
| ∃ scope extension | x not free in Q | ∃x (P(x) ∧ Q) ≡ (∃x P(x)) ∧ Q |
| ∃ scope extension | x not free in Q | ∃x (P(x) ∨ Q) ≡ (∃x P(x)) ∨ Q |

**Intuition:** If Q doesn't involve x, pulling it outside the quantifier changes nothing — Q is either always true or always false regardless of x.

### 4.3 Vacuous Quantification

Over an empty domain ∅:
- ∀x P(x) is **vacuously TRUE** — there are no elements to violate it
- ∃x P(x) is **FALSE** — there are no elements to serve as witnesses

**This matters in CS:** A loop over an empty list that checks "for all elements, property P" returns true. A loop that looks for "some element satisfying P" returns false.

```python
all(P(x) for x in [])   # True  — vacuous universal
any(P(x) for x in [])   # False — failed existential
```

---

## 5. Counterexamples and Witnesses: Formal Proof Obligations

| Claim Type | To Prove TRUE | To Prove FALSE |
|---|---|---|
| ∀x P(x) | Prove P(x) for arbitrary x (no assumptions about x) | Give one counterexample a where P(a) is false |
| ∃x P(x) | Give one witness a where P(a) is true | Prove P(x) is false for every x |
| ¬∀x P(x) | Give one counterexample (same as proving ∃x ¬P(x)) | Prove P(x) for all x |
| ¬∃x P(x) | Prove P(x) false for all x (same as proving ∀x ¬P(x)) | Give one witness |

This table clarifies what is required at every step of an argument. When proving ∀x P(x), you must prove P(x) for an **arbitrary** x — one you know nothing about beyond what the domain tells you. If your proof relies on x being even, or positive, or prime, then you have only proven P for those special x, not for all x.

---

## 6. Bounded Quantifiers

In mathematics and CS, we frequently restrict quantifiers to a subset of the domain. This is done with bounded quantifier notation:

| Notation | Equivalent Form |
|---|---|
| ∀x ∈ S, P(x) | ∀x (x ∈ S → P(x)) |
| ∃x ∈ S, P(x) | ∃x (x ∈ S ∧ P(x)) |

The earlier rule reappears: bounded ∀ uses →, bounded ∃ uses ∧.

**Negation of bounded quantifiers:**

| Statement | Negation |
|---|---|
| ∀x ∈ S, P(x) | ∃x ∈ S, ¬P(x) |
| ∃x ∈ S, P(x) | ∀x ∈ S, ¬P(x) |

The bound S stays the same — only the quantifier flips and the predicate is negated.

**Example:** Negate "Every prime greater than 2 is odd":
- Original: ∀x ∈ ℤ, (x > 2 ∧ P(x)) → O(x)
  Or with bounded notation: ∀x ∈ {primes > 2}, O(x)
- Negation: ∃x ∈ {primes > 2}, ¬O(x) = ∃x ∈ ℤ, (x > 2 ∧ P(x) ∧ ¬O(x))
- Reading: "There exists a prime greater than 2 that is not odd" (i.e., is even).
- This is FALSE — 2 is the only even prime, and 2 is not > 2.

---

## 7. Translating "No," "None," "Nothing"

Statements with "no" or "none" appear frequently. The pattern:

| English | Logic |
|---|---|
| "No x satisfies P" | ¬∃x P(x) ≡ ∀x ¬P(x) |
| "No student passed" | ∀x (S(x) → ¬P(x)) |
| "Nothing is both A and B" | ∀x ¬(A(x) ∧ B(x)) ≡ ∀x (A(x) → ¬B(x)) |

**Example:** "No integer is both prime and negative."

∀x ∈ ℤ, ¬(Prime(x) ∧ x < 0)
≡ ∀x ∈ ℤ, (Prime(x) → x ≥ 0)

This is TRUE — all primes are positive by definition.

---

## 8. "At Least," "At Most," "Exactly" — Counting Quantifiers

| Phrase | Logic |
|---|---|
| "At least one" | ∃x P(x) |
| "At least two" | ∃x ∃y (x ≠ y ∧ P(x) ∧ P(y)) |
| "At most one" | ∀x ∀y (P(x) ∧ P(y) → x = y) |
| "Exactly one" | ∃! x P(x) |

These arise constantly in specifications. "A function maps each input to exactly one output" uses exactly-one: ∀x ∃! y, f(x) = y.

---

## 9. Worked Translation Examples: CS Specifications

**Example 1:** Precondition of binary search.

"The array arr is sorted in non-decreasing order."

Let A(i) = arr[i]. Domain: valid indices {0, 1, …, n−1}.

∀i ∀j ((0 ≤ i < j ≤ n−1) → A(i) ≤ A(j))

Or with bounded quantifiers:
∀i ∈ {0,…,n−2}, A(i) ≤ A(i+1)

(The second form works because ≤ is transitive — adjacent comparisons suffice.)

**Example 2:** "The function f has no memory leaks."

"Every block of memory allocated is eventually freed."

Let Alloc(b, t) = "block b is allocated at time t", Free(b, t) = "block b is freed at time t".

∀b ∀t (Alloc(b, t) → ∃t' (t' > t ∧ Free(b, t')))

**Example 3:** "There is a deadlock in the system."

"There exist two processes, each waiting for a resource held by the other."

∃p ∃q (p ≠ q ∧ Waits(p, resource_held_by(q)) ∧ Waits(q, resource_held_by(p)))

**Example 4:** "The sorting algorithm is correct."

∀arr (IsSorted(Sort(arr)) ∧ IsPermutation(Sort(arr), arr))

(Output is sorted AND is a permutation of the input — both conditions are necessary.)

---

## 10. Summary

| Rule | Formula |
|---|---|
| Negate ∀ | ¬(∀x P(x)) ≡ ∃x ¬P(x) |
| Negate ∃ | ¬(∃x P(x)) ≡ ∀x ¬P(x) |
| ∀ distributes over ∧ | ∀x(P∧Q) ≡ (∀xP)∧(∀xQ) |
| ∃ distributes over ∨ | ∃x(P∨Q) ≡ (∃xP)∨(∃xQ) |
| Bounded ∀ | ∀x∈S, P(x) ≡ ∀x(x∈S → P(x)) |
| Bounded ∃ | ∃x∈S, P(x) ≡ ∃x(x∈S ∧ P(x)) |

**The single most important rule to internalize:**

> To negate a quantified statement: flip every quantifier (∀↔∃) as you push the negation inward, and negate the innermost predicate.

---

## 11. End-of-Lecture Exercises

1. Negate each statement, simplify fully, and state whether the original or its negation is true:
   - (a) ∀x ∈ ℤ, x² ≥ x
   - (b) ∃x ∈ ℝ, x² = −1
   - (c) ∀x ∈ ℤ⁺, ∃y ∈ ℤ⁺, y > x
   - (d) ∃x ∈ ℝ, ∀y ∈ ℝ, x ≤ y

2. Which distribution laws hold? For those that fail, give a counterexample:
   - (a) ∀x (P(x) ∧ Q(x)) ≡ (∀x P(x)) ∧ (∀x Q(x))
   - (b) ∀x (P(x) ∨ Q(x)) ≡ (∀x P(x)) ∨ (∀x Q(x))
   - (c) ∃x (P(x) ∧ Q(x)) ≡ (∃x P(x)) ∧ (∃x Q(x))
   - (d) ∃x (P(x) ∨ Q(x)) ≡ (∃x P(x)) ∨ (∃x Q(x))

3. Negate the following program specifications:
   - (a) "Every function in the codebase has at least one unit test."
   - (b) "No two users share the same email address."
   - (c) "If a transaction commits, then all its writes are durable."

4. Translate into predicate logic, then negate:
   - (a) "Every positive real number has a real square root."
   - (b) "There is a rational number between any two distinct real numbers."

5. Express "at most two integers satisfy P(x)" in predicate logic without using ∃!.

---

## Reading

- **Rosen, 8e §1.4** — Negating quantified expressions; logical equivalences with quantifiers
- **Epp, 5e §3.2** — Predicates and quantified statements II
- **Levin, 3e §0.2** — Mathematical statements

*Next: Lecture 5 — Nested Quantifiers: When Order Matters*
