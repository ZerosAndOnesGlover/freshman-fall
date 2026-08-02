# MATH 151 Quantifier Rules Reference
## Week 1: Predicate Logic and Quantifiers

---

## Quantifier Definitions

| Quantifier | Symbol | True When | False When | Prove True By | Disprove By |
|---|---|---|---|---|---|
| Universal | ∀x P(x) | P(a) holds for every a in domain | P(a) fails for some a | Prove P(x) for arbitrary x | Exhibit one counterexample |
| Existential | ∃x P(x) | P(a) holds for some a in domain | P(a) fails for every a | Exhibit one witness | Prove P(x) false for all x |
| Unique | ∃! x P(x) | Exactly one a satisfies P | Zero or ≥2 satisfy P | Exhibit witness; prove uniqueness | Show 0 or ≥2 witnesses |

---

## Negation Rules (De Morgan for Quantifiers)

| Original | Negation | Note |
|---|---|---|
| ∀x P(x) | ∃x ¬P(x) | Flip ∀→∃, negate predicate |
| ∃x P(x) | ∀x ¬P(x) | Flip ∃→∀, negate predicate |
| ∀x ∀y P(x,y) | ∃x ∃y ¬P(x,y) | Flip each quantifier |
| ∀x ∃y P(x,y) | ∃x ∀y ¬P(x,y) | Flip each quantifier |
| ∃x ∀y P(x,y) | ∀x ∃y ¬P(x,y) | Flip each quantifier |
| ∃x ∃y P(x,y) | ∀x ∀y ¬P(x,y) | Flip each quantifier |

**General rule:** Push ¬ inward through quantifiers, flipping each one (∀↔∃), until ¬ reaches the predicate, then negate the predicate using propositional laws.

**Final answers must never contain ¬∀ or ¬∃.**

---

## Bounded Quantifiers

| Form | Equivalent Expansion |
|---|---|
| ∀x ∈ S, P(x) | ∀x (x ∈ S → P(x)) |
| ∃x ∈ S, P(x) | ∃x (x ∈ S ∧ P(x)) |
| Negate ∀x ∈ S, P(x) | ∃x ∈ S, ¬P(x) — S stays the same |
| Negate ∃x ∈ S, P(x) | ∀x ∈ S, ¬P(x) — S stays the same |

---

## Translation Patterns (Critical)

| English | Logic | Common Error |
|---|---|---|
| "Every A is B" | ∀x (A(x) → B(x)) | Using ∧ instead of → |
| "Some A is B" | ∃x (A(x) ∧ B(x)) | Using → instead of ∧ |
| "No A is B" | ∀x (A(x) → ¬B(x)) or ¬∃x(A(x)∧B(x)) | |
| "Not every A is B" | ∃x (A(x) ∧ ¬B(x)) | |
| "At least one A is B" | ∃x (A(x) ∧ B(x)) | |
| "All and only A's are B's" | ∀x (A(x) ↔ B(x)) | |

**The critical asymmetry:**
- Universal + restricted domain → **→** (implication)
- Existential + restricted domain → **∧** (conjunction)

*Why:* ∀x ∈ S, P(x) = ∀x (x∈S → P(x)) expands with →. ∃x ∈ S, P(x) = ∃x (x∈S ∧ P(x)) expands with ∧.

---

## Quantifier Order — The Key Asymmetry

| Statement | Meaning | Strength |
|---|---|---|
| ∃y ∀x P(x,y) | One y works for ALL x simultaneously | Stronger |
| ∀x ∃y P(x,y) | For each x, SOME y works (may differ per x) | Weaker |

**Implication:** ∃y ∀x P(x,y) → ∀x ∃y P(x,y) always holds.
**Non-implication:** ∀x ∃y P(x,y) does NOT imply ∃y ∀x P(x,y) in general.

**Canonical example over ℤ with P(x,y) = "y > x":**
- ∀x ∃y (y > x): TRUE — for any x, take y = x+1
- ∃y ∀x (y > x): FALSE — no single integer exceeds all integers

---

## Quantifier–Connective Interactions

| Law | Status | Notes |
|---|---|---|
| ∀x(P∧Q) ≡ (∀xP)∧(∀xQ) | ✓ TRUE | ∀ distributes over ∧ |
| ∃x(P∨Q) ≡ (∃xP)∨(∃xQ) | ✓ TRUE | ∃ distributes over ∨ |
| ∀x(P∨Q) ≡ (∀xP)∨(∀xQ) | ✗ FALSE | Counterexample: P="even", Q="odd" |
| ∃x(P∧Q) ≡ (∃xP)∧(∃xQ) | ✗ FALSE | Right side doesn't guarantee same x |

---

## Common Domains

| Symbol | Set |
|---|---|
| ℕ | {0, 1, 2, 3, …} (natural numbers) |
| ℤ | {…, −2, −1, 0, 1, 2, …} (integers) |
| ℤ⁺ | {1, 2, 3, …} (positive integers) |
| ℚ | Rational numbers (fractions p/q, q≠0) |
| ℝ | Real numbers |
| ℂ | Complex numbers |

---

## Named Quantified Definitions (to recognize on sight)

| Definition | Formal Statement |
|---|---|
| f injective | ∀x₁ ∀x₂ (f(x₁)=f(x₂) → x₁=x₂) |
| f surjective onto B | ∀y∈B, ∃x∈A, f(x)=y |
| Sequence bounded above | ∃M∈ℝ, ∀n∈ℕ, aₙ ≤ M |
| Sequence bounded | ∃M∈ℝ, ∀n∈ℕ, |aₙ| ≤ M |
| Limit lim f(x)=L as x→a | ∀ε>0, ∃δ>0, ∀x (0<|x−a|<δ → |f(x)−L|<ε) |
| f uniformly continuous | ∀ε>0, ∃δ>0, ∀x ∀y (|x−y|<δ → |f(x)−f(y)|<ε) |
| x and y are coprime | ∀d∈ℤ⁺, (D(d,x) ∧ D(d,y) → d=1) |

---

## Free vs Bound Variables

| Term | Meaning |
|---|---|
| Bound variable | Appears within scope of a quantifier ∀x or ∃x |
| Free variable | Not within scope of any quantifier for that variable |
| Closed formula | No free variables — has a definite truth value |
| Open formula | Has free variables — truth depends on variable assignment |

**Rule:** In ∀x ∃y P(x, y, z): x and y are bound, z is free. The whole formula is a predicate in z.
