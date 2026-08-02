# MATH 151 · Logic Laws Reference
## All Standard Propositional Equivalences — Week 0

---

> **How to use this sheet:** Do not read passively. For each law, cover the right side, derive the right side from the left using the truth table or another law, then uncover to check. Mastery requires producing these on demand, not recognizing them when shown.

---

## The Complete Laws of Propositional Logic

### Group 1 — Identity Laws
```
p ∧ T ≡ p
p ∨ F ≡ p
```

### Group 2 — Domination Laws
```
p ∧ F ≡ F
p ∨ T ≡ T
```

### Group 3 — Idempotent Laws
```
p ∧ p ≡ p
p ∨ p ≡ p
```

### Group 4 — Double Negation
```
¬(¬p) ≡ p
```

### Group 5 — Commutativity
```
p ∧ q ≡ q ∧ p
p ∨ q ≡ q ∨ p
```

### Group 6 — Associativity
```
(p ∧ q) ∧ r ≡ p ∧ (q ∧ r)
(p ∨ q) ∨ r ≡ p ∨ (q ∨ r)
```

### Group 7 — Distributivity
```
p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)
p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r)
```

### Group 8 — De Morgan's Laws ⭐
```
¬(p ∧ q) ≡ ¬p ∨ ¬q
¬(p ∨ q) ≡ ¬p ∧ ¬q
```
**Mnemonic:** Negate, flip connective, negate each part.

### Group 9 — Absorption Laws
```
p ∨ (p ∧ q) ≡ p
p ∧ (p ∨ q) ≡ p
```

### Group 10 — Complement Laws (Negation Laws)
```
p ∨ ¬p ≡ T    (Excluded Middle)
p ∧ ¬p ≡ F    (Non-Contradiction)
¬T ≡ F
¬F ≡ T
```

---

## Conditional and Biconditional Laws

### Conditional Elimination
```
p → q ≡ ¬p ∨ q
```

### Contrapositive
```
p → q ≡ ¬q → ¬p
```

### Negation of Conditional ⭐
```
¬(p → q) ≡ p ∧ ¬q
```
(The only counterexample to p → q is p=T, q=F)

### Biconditional Expansion (two forms)
```
p ↔ q ≡ (p → q) ∧ (q → p)
p ↔ q ≡ (p ∧ q) ∨ (¬p ∧ ¬q)
```

### Negation of Biconditional
```
¬(p ↔ q) ≡ p ⊕ q
¬(p ↔ q) ≡ (p ∧ ¬q) ∨ (¬p ∧ q)
```

---

## Named Tautologies (Inference Rules in Disguise)

| Name | Formula |
|---|---|
| **Modus Ponens** | (p ∧ (p → q)) → q |
| **Modus Tollens** | (¬q ∧ (p → q)) → ¬p |
| **Hypothetical Syllogism** | ((p → q) ∧ (q → r)) → (p → r) |
| **Disjunctive Syllogism** | ((p ∨ q) ∧ ¬p) → q |
| **Addition** | p → (p ∨ q) |
| **Simplification** | (p ∧ q) → p |
| **Resolution** | ((p ∨ q) ∧ (¬p ∨ r)) → (q ∨ r) |
| **Exportation** | (p → (q → r)) ≡ ((p ∧ q) → r) |

---

## Substitution and Replacement Principles

If φ ≡ ψ, then any formula containing φ as a subformula remains equivalent when φ is replaced by ψ.

**Example:** To simplify ¬(p ∧ ¬q) → r:
- Note ¬(p ∧ ¬q) ≡ ¬p ∨ q (De Morgan + Double Negation)
- Substitute: (¬p ∨ q) → r
- This is valid by the replacement principle.

---

## Functional Completeness Summary

| Set | Complete? |
|---|---|
| {¬, ∧, ∨} | ✓ Yes |
| {¬, ∧} | ✓ Yes (p∨q ≡ ¬(¬p∧¬q)) |
| {¬, ∨} | ✓ Yes (p∧q ≡ ¬(¬p∨¬q)) |
| {¬, →} | ✓ Yes (p∨q ≡ ¬p→q) |
| {NAND} | ✓ Yes |
| {NOR} | ✓ Yes |
| {∧, ∨} | ✗ No (cannot express ¬) |
| {→} alone | ✗ No |

---

## Common Mistakes — What NOT to Do

| Mistake | Correct Form |
|---|---|
| p → q ≡ q → p | FALSE. Converse ≠ Original |
| ¬(p → q) ≡ ¬p → ¬q | FALSE. ¬(p→q) ≡ p ∧ ¬q |
| p ∨ (q ∧ r) ≡ (p ∨ q) ∧ r | FALSE. Must distribute: (p∨q) ∧ (p∨r) |
| ¬(p ∧ q) ≡ ¬p ∧ ¬q | FALSE. De Morgan: ¬(p∧q) ≡ ¬p ∨ ¬q |
| (p → q) means p causes q | NO. → is material implication only |
| "or" in math is exclusive | NO. ∨ is inclusive; ⊕ is exclusive |
