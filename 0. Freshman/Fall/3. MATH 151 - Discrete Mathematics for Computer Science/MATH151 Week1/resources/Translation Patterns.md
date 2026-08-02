# MATH 151 · Translation Patterns Reference
## English ↔ Predicate Logic: Week 1

---

## The Core Asymmetry (Memorize First)

```
∀ (for all) + restricted domain  →  use IMPLICATION (→)
∃ (there exists) + restricted domain  →  use CONJUNCTION (∧)
```

This is not arbitrary. It follows from the expansions:
- ∀x ∈ S, P(x)  expands to  ∀x (x ∈ S → P(x))
- ∃x ∈ S, P(x)  expands to  ∃x (x ∈ S ∧ P(x))

**Why the error is so common:** In English, "every student passed" and "some student passed" both feel like they should use AND. But in logic, the universal "every student passed" does NOT claim that everyone is a student — it only makes a claim about those who ARE students. The implication → does exactly this: it fires (makes a claim) only when x ∈ S.

---

## Pattern Table — Single Quantifier

| English Phrasing | Domain Setup | Formula |
|---|---|---|
| "Every P is Q" | x is a P | ∀x (P(x) → Q(x)) |
| "All P's are Q's" | x is a P | ∀x (P(x) → Q(x)) |
| "Each P is Q" | x is a P | ∀x (P(x) → Q(x)) |
| "Any P is Q" | x is a P | ∀x (P(x) → Q(x)) |
| "P's are always Q" | x is a P | ∀x (P(x) → Q(x)) |
| "Some P is Q" | x is a P | ∃x (P(x) ∧ Q(x)) |
| "There is a P that is Q" | x is a P | ∃x (P(x) ∧ Q(x)) |
| "At least one P is Q" | x is a P | ∃x (P(x) ∧ Q(x)) |
| "No P is Q" | x is a P | ∀x (P(x) → ¬Q(x)) |
| "No P is Q" (equiv.) | | ¬∃x (P(x) ∧ Q(x)) |
| "Not every P is Q" | x is a P | ∃x (P(x) ∧ ¬Q(x)) |
| "Some P is not Q" | x is a P | ∃x (P(x) ∧ ¬Q(x)) |

---

## Quantifier–English Correspondence

| English word/phrase | Quantifier |
|---|---|
| every, all, any, each, for all | ∀ |
| some, there exists, at least one, there is | ∃ |
| no, none, nothing, nobody, never | ¬∃ or ∀¬ |
| exactly one, a unique, one and only one | ∃! |
| not every, not all | ¬∀ or ∃¬ |

---

## Negation Translations

| Positive English | Logical Form | Negated Form | Negative English |
|---|---|---|---|
| "Every P is Q" | ∀x(P→Q) | ∃x(P∧¬Q) | "Some P is not Q" |
| "Some P is Q" | ∃x(P∧Q) | ∀x(P→¬Q) | "No P is Q" |
| "No P is Q" | ∀x(P→¬Q) | ∃x(P∧Q) | "Some P is Q" |
| "Not every P is Q" | ∃x(P∧¬Q) | ∀x(P→Q) | "Every P is Q" |

---

## Nested Quantifier Patterns

| English | Formula | Notes |
|---|---|---|
| "For every x, some y satisfies R(x,y)" | ∀x ∃y R(x,y) | y may depend on x |
| "There is a y that works for every x" | ∃y ∀x R(x,y) | single y, independent of x |
| "Every x and every y satisfy R(x,y)" | ∀x ∀y R(x,y) | all pairs |
| "Some x and some y satisfy R(x,y)" | ∃x ∃y R(x,y) | some pair exists |
| "Every x has some y and some z with R(x,y,z)" | ∀x ∃y ∃z R(x,y,z) | |

---

## Worked Translation Examples

### Example Set 1 — Number Theory

| Statement | Predicates | Domain | Formula |
|---|---|---|---|
| "Every integer has a successor" | — | ℤ | ∀x ∃y (y = x + 1) |
| "Every positive integer has a prime factor" | Prime(p) | ℤ⁺ | ∀n ∃p (Prime(p) ∧ D(p, n)) |
| "There is no largest integer" | — | ℤ | ¬∃x ∀y (x ≥ y) equiv. ∀x ∃y (y > x) |
| "Between any two rationals there is a rational" | R(x)="x is rational" | ℚ | ∀x ∀y (x < y → ∃z (R(z) ∧ x < z < y)) |
| "Every even integer > 2 is a sum of two primes" (Goldbach) | E(x), P(x) | ℤ⁺ | ∀x ((E(x) ∧ x > 2) → ∃p ∃q (P(p) ∧ P(q) ∧ x = p+q)) |

### Example Set 2 — Function Properties

| Property | Domain | Formula |
|---|---|---|
| f is a function (well-defined) | A, B | ∀x∈A ∃!y∈B, f(x)=y |
| f is injective | A | ∀x₁∈A ∀x₂∈A (f(x₁)=f(x₂) → x₁=x₂) |
| f is surjective onto B | B, A | ∀y∈B ∃x∈A, f(x)=y |
| f is bijective | A, B | (injective) ∧ (surjective) |
| f is non-decreasing | ℝ | ∀x ∀y (x ≤ y → f(x) ≤ f(y)) |

### Example Set 3 — CS and Software

| Statement | Predicates | Domain | Formula |
|---|---|---|---|
| "Every input produces exactly one output" | — | inputs, outputs | ∀x ∃!y, f(x)=y |
| "No two users share a username" | U(x)="x is a user", Same(x,y)="same username" | users | ∀x ∀y (x≠y → ¬Same(x,y)) |
| "Every allocated block is eventually freed" | Alloc(b,t), Free(b,t) | blocks, times | ∀b ∀t (Alloc(b,t) → ∃t'(t'>t ∧ Free(b,t'))) |
| "The sort is stable" | Eq(a,b), Before(i,j) | array elements | ∀i ∀j (i<j ∧ Eq(arr[i],arr[j]) → Before(pos(i),pos(j))) |
| "f is O(g)" | — | ℕ | ∃C>0 ∃n₀∈ℕ ∀n≥n₀, f(n) ≤ C·g(n) |

---

## Warning: Ambiguous English Phrases

Some English phrases are genuinely ambiguous — predicate logic forces you to resolve the ambiguity.

| Ambiguous | Interpretation 1 | Interpretation 2 |
|---|---|---|
| "A student answered every question" | ∃s ∀q A(s,q) — one student got all | ∀q ∃s A(s,q) — every question was answered by some student |
| "Every professor failed some student" | ∀p ∃s F(p,s) — each prof failed someone | ∃s ∀p F(p,s) — some student failed every prof |
| "All that glitters is not gold" | ∀x (G(x) → ¬Gold(x)) — nothing glittery is gold | ¬∀x (G(x) → Gold(x)) — not everything glittery is gold |

When translating, ask: "What exactly is being claimed about every/some/no x?"
