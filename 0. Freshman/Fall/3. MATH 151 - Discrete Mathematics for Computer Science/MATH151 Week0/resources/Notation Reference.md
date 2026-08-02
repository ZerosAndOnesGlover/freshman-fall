# MATH 151 — Notation Reference
## Propositional Logic — Week 0

---

## Connective Symbols

| Symbol | Name | Read As | Code Equivalents |
|---|---|---|---|
| ¬p | Negation | "not p" | `!p`, `not p`, `~p` |
| p ∧ q | Conjunction | "p and q" | `p && q`, `p and q` |
| p ∨ q | Disjunction | "p or q" | `p \|\| q`, `p or q` |
| p → q | Conditional | "if p then q", "p implies q" | `!p \|\| q` |
| p ↔ q | Biconditional | "p iff q", "p if and only if q" | `p == q` (for booleans) |
| p ⊕ q | Exclusive OR | "p xor q" | `p ^ q`, `p != q` |

## Derived / Named Connectives

| Name | Formula | Truth: When |
|---|---|---|
| NAND | ¬(p ∧ q) | Not both true |
| NOR | ¬(p ∨ q) | Both false |
| XNOR | p ↔ q | Same truth value |

## Constants

| Symbol | Meaning |
|---|---|
| T (or ⊤ or 1) | Tautological constant (always true) |
| F (or ⊥ or 0) | Contradiction constant (always false) |

## Operator Precedence (High to Low)

```
1. ¬    (unary, right-to-left)
2. ∧    (left-to-right)
3. ∨    (left-to-right)
4. →    (right-to-left)
5. ↔    (left-to-right)
```

## Truth Value Abbreviations

| Written | Meaning |
|---|---|
| T | True |
| F | False |
| 1 | True (especially in hardware/CS contexts) |
| 0 | False |

## Meta-Notation

| Symbol | Meaning |
|---|---|
| φ, ψ, χ | Metavariables standing for arbitrary formulas |
| p, q, r, s | Propositional variables |
| φ ≡ ψ | φ and ψ are logically equivalent |
| ⊨ φ | φ is a tautology (valid) |
| φ ⊨ ψ | ψ follows logically from φ |
| ⊢ φ | φ is provable (in some proof system) |
| := | "is defined as" |

---

## Quick Truth Table Reference

| p | q | ¬p | p∧q | p∨q | p→q | p↔q | p⊕q |
|---|---|-----|-----|-----|-----|-----|-----|
| T | T | F   | T   | T   | T   | T   | F   |
| T | F | F   | F   | T   | F   | F   | T   |
| F | T | T   | F   | T   | T   | F   | T   |
| F | F | T   | F   | F   | T   | T   | F   |

**Memory aid for p→q:** The only way to make a conditional FALSE is to have a TRUE hypothesis and a FALSE conclusion (T→F = F). All other cases are T.

---

## Conditional Relationships

Given p → q:

| Name | Formula | Equiv to p→q? |
|---|---|---|
| Original | p → q | — |
| Converse | q → p | ✗ No |
| Inverse | ¬p → ¬q | ✗ No |
| Contrapositive | ¬q → ¬p | ✓ Yes |

Converse and Inverse ARE equivalent to each other (both equal q → p in effect).

---

## English-to-Logic Patterns

| English | Logic |
|---|---|
| "p and q" | p ∧ q |
| "p but q" | p ∧ q |
| "p or q" (inclusive) | p ∨ q |
| "either p or q but not both" | p ⊕ q |
| "not p" | ¬p |
| "neither p nor q" | ¬p ∧ ¬q |
| "not both p and q" | ¬(p ∧ q) ≡ ¬p ∨ ¬q |
| "if p then q" | p → q |
| "p only if q" | p → q |
| "p if q" | q → p |
| "q whenever p" | p → q |
| "q is necessary for p" | p → q |
| "p is sufficient for q" | p → q |
| "p unless q" | ¬q → p (≡ p ∨ q) |
| "p if and only if q" | p ↔ q |
| "p is necessary and sufficient for q" | p ↔ q |
