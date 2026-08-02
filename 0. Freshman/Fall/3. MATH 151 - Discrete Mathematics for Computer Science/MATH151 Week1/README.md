# MATH 151 · Discrete Mathematics for Computer Science
## Week 1 — Predicate Logic, Quantifiers, and Logical Equivalences

---

### Course Information

| Field | Detail |
|---|---|
| Course | MATH 151: Discrete Mathematics for Computer Science |
| Credits | 3 |
| Semester | Fall, Year 1 |
| Week | 1 of 12 |

---

### Week 1 Overview

Week 0 gave you propositional logic — a language for combining *atomic* true/false statements. But propositional logic cannot express most mathematical claims. "Every even integer greater than 2 is the sum of two primes" is not just a single proposition — it is a statement *about all* integers satisfying a property. "There exists a prime between n and 2n" asserts the *existence* of something. Propositional logic has no machinery for this.

Week 1 introduces **predicate logic** (also called first-order logic), which adds:
- **Predicates** — properties that objects can have or fail to have
- **Quantifiers** — ∀ ("for all") and ∃ ("there exists") — which turn predicates into propositions
- **Domains of discourse** — the universe of objects we are talking about

This is the language in which virtually all of mathematics is written.

**You will leave Week 1 able to:**
- Define predicates and evaluate them over a domain
- Write ∀ and ∃ statements and determine their truth values
- Negate quantified statements correctly (the most critical skill)
- Translate complex English mathematical claims into predicate logic
- Prove or disprove universally and existentially quantified statements
- Recognize nested quantifiers and understand why order matters

---

### Week 1 Contents

```
MATH151_Week1/
├── README.md
│
├── lectures/
│   ├── L03 Predicates and Quantifiers.md        ← Lecture 4 (Monday)
│   ├── L04 Negation and Equivalences.md         ← Lecture 5 (Thursday)
│   └── L05 Nested Quantifiers.md                ← Lecture 6 (Friday)
│
├── assignments/
│   └── PS 1 Predicate Logic.md
│
├── lab/
│   └── LAB 1 Quantifier Workshop.md
│
├── quiz/
│   ├── QUIZ 1 Propositional Logic.md             ← Administered Monday (covers Week 0)
│   └── QUIZ 2 Preview.md
│
├── resources/
│   ├── quantifier_rules_reference.md
│   └── translation_patterns.md
│
└── solutions_instructor/
    ├── QUIZ 1 Solutions.md
    ├── PS 1 Solutions.md
    └── LAB 1 Solutions.md
```

---

### Schedule at a Glance

| Day | Event | Topic |
|---|---|---|
| Monday | Quiz 1 (15 min) | Covers all of Week 0 propositional logic |
| Monday | Lecture 4 | Predicates, domains, quantifiers ∀ and ∃ |
| Thursday | Lecture 5 | Negating quantified statements, logical equivalences with quantifiers |
| Wednesday | Lab 1 | Quantifier translation workshop + Python predicate evaluator |
| Friday | Lecture 6 | Nested quantifiers, order matters, bounded quantifiers |
| Friday | PS 1 Released | Due Week 2 Friday |

---

### Textbook Readings

| Text | Sections |
|---|---|
| Rosen, 8e | §1.4, §1.5 |
| Epp, 5e | §3.1, §3.2, §3.3 |
| Levin, 3e | §0.2 (continued) |

---

### The Leap from Propositional to Predicate Logic

| | Propositional Logic | Predicate Logic |
|---|---|---|
| Basic unit | Proposition (fixed T/F) | Predicate (T/F depends on input) |
| Variables | Propositional (p, q, r) | Object variables (x, y, n) |
| Combining | ¬ ∧ ∨ → ↔ | Same connectives + ∀ ∃ |
| Can express | "It is raining AND cold" | "Every integer has a successor" |
| Cannot express | "All x satisfy P(x)" | — |

The addition of quantifiers makes predicate logic **vastly more expressive** — and also makes negation significantly more subtle.
