# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 1. Truth Tables: Systematic Evaluation of Compound Propositions
### Thursday, Week 0

*“That logic, as a science, is susceptible of very wide applications is admitted; but it is equally certain that its ultimate forms and processes are mathematical.”* — George Boole, *An Investigation of the Laws of Thought* (1854)

**Date:** Thursday 24 September 2026 · 13:00–13:50 · Week 0

**Reading:** Rosen, 8e §1.1 · Epp, 5e §2.1–2.2 · Levin, 3e §3.1 *(details at the end of the lecture)*

**Coursework:** 📝 **PS 0** released Fri 25 Sep 14:00, due Fri 2 Oct 17:00 · 📊 **Quiz 1** Mon 28 Sep 13:00–13:15 · 🔬 **Lab 0** Wed 30 Sep 15:00–16:50

---

> **Core Question:** Given a compound proposition of arbitrary complexity, how do we *mechanically* determine its truth under every possible assignment of truth values?


---

## 1. The Truth Table Method

A truth table is a systematic enumeration of all possible truth-value assignments to propositional variables, together with the resulting truth value of the compound proposition.

**Why complete enumeration?**
A proposition with n variables has **2ⁿ** possible truth-value assignments. For 2 variables, that's 4 rows. For 3 variables, 8 rows. For 10 variables, 1024 rows. For 100 variables, SAT solvers are computing!

Truth tables are:
- Finite (for finite n)
- Mechanical (no insight required, pure computation)
- Complete (no case is missed)

They are the *brute-force* approach to logical analysis.

---

## 2. Construction Procedure

**Algorithm for building a truth table:**

1. **List all variables.** Count n variables → you have 2ⁿ rows.

2. **Fill variable columns.** For the rightmost variable, alternate T/F. For the next, alternate in pairs (TT/FF). For the next, in quadruples. Pattern: variable k (from right, starting at 0) alternates in blocks of 2ᵏ.

   For n=3 (variables p, q, r):
   ```
   p: T T T T F F F F    (blocks of 4)
   q: T T F F T T F F    (blocks of 2)
   r: T F T F T F T F    (blocks of 1)
   ```

3. **Add intermediate columns** for each subformula, working from innermost to outermost. Evaluate each row using the operator definitions.

4. **The final column** is the truth value of the full formula.

---

## 3. Worked Examples

### Example 1: ¬p ∧ q

Two variables → 4 rows.

| p | q | ¬p | ¬p ∧ q |
|---|---|----|--------|
| T | T | F  | **F**  |
| T | F | F  | **F**  |
| F | T | T  | **T**  |
| F | F | T  | **F**  |

**Reading the table:** ¬p ∧ q is true in exactly one scenario: when p is false and q is true.

---

### Example 2: (p ∨ q) → ¬r

Three variables → 8 rows.

| p | q | r | p ∨ q | ¬r | (p ∨ q) → ¬r |
|---|---|---|-------|-----|--------------|
| T | T | T | T     | F   | **F**        |
| T | T | F | T     | T   | **T**        |
| T | F | T | T     | F   | **F**        |
| T | F | F | T     | T   | **T**        |
| F | T | T | T     | F   | **F**        |
| F | T | F | T     | T   | **T**        |
| F | F | T | F     | F   | **T**        |
| F | F | F | F     | T   | **T**        |

**Reading the table:** The formula is false exactly when (p ∨ q) is true and r is true. That is, when at least one of p, q is true, but r is also true.

---

### Example 3: p → (q → p)

| p   | q   | q → p | p → (q → p) |
| --- | --- | ----- | ----------- |
| T   | T   | T     | **T**       |
| T   | F   | T     | **T**       |
| F   | T   | F     | **T**       |
| F   | F   | T     | **T**       |

Every row is T. This formula is always true, a **tautology**. (We explore tautologies in Lecture 2.)

---

## 4. The Conditional: Deeper Analysis

The conditional p → q consistently confuses students because its truth table differs from intuition. Let us examine it from three angles.

### Angle 1: The Promise Interpretation (Lecture 0 Review)

The conditional is a promise: "If p, I guarantee q." The only way to *break* the promise is to have p true but q false. This gives us the truth table from Lecture 0.

### Angle 2: The Logical Equivalence

**Claim:** p → q ≡ ¬p ∨ q (they have the same truth table).

| p | q | p → q | ¬p | ¬p ∨ q |
|---|---|-------|-----|--------|
| T | T | T     | F   | **T**  |
| T | F | F     | F   | **F**  |
| F | T | T     | T   | **T**  |
| F | F | T     | T   | **T**  |

The final columns are identical. Therefore p → q and ¬p ∨ q always have the same truth value, they are **logically equivalent**.

**Implication:** Every conditional can be rewritten as a disjunction. This is not just a curiosity, it is the basis of *clausal normal form* used in SAT solvers and automated theorem provers.

### Angle 3: The Contrapositive

**Claim:** p → q ≡ ¬q → ¬p (the contrapositive).

| p | q | p → q | ¬q | ¬p | ¬q → ¬p |
|---|---|-------|-----|-----|---------|
| T | T | T     | F   | F   | **T**   |
| T | F | F     | T   | F   | **F**   |
| F | T | T     | F   | T   | **T**   |
| F | F | T     | T   | T   | **T**   |

Again, identical final columns. The contrapositive is logically equivalent to the original conditional.

**Why this matters in proofs:** Sometimes it is easier to prove ¬q → ¬p than p → q directly. We will use this technique extensively in Week 2.

---

## 5. Converse and Inverse: Two Common Mistakes

Given p → q:

| Name | Formula | Equivalent to p → q? |
|---|---|---|
| **Original** | p → q | — |
| **Converse** | q → p | ✗ **Not equivalent** |
| **Inverse** | ¬p → ¬q | ✗ **Not equivalent** |
| **Contrapositive** | ¬q → ¬p | ✓ **Equivalent** |

**Verification — Converse q → p:**

| p | q | p → q | q → p |
|---|---|-------|-------|
| T | T | T     | T     |
| T | F | F     | T     |
| F | T | T     | F     |
| F | F | T     | T     |

Columns 3 and 4 differ in rows 2 and 3. **Not equivalent.**

**The classic error:** Concluding that p → q implies q → p. 

Example: "If it rains, the ground is wet" does NOT mean "If the ground is wet, it rained." (The ground could be wet from a sprinkler.)

**Programming context:**
```
"If a function is pure, it has no side effects."
```
The converse: "If a function has no side effects, it is pure", is not necessarily true (it could still depend on global state for *reading*, which some definitions permit).

---

## 6. The Biconditional: Unpacked

**p ↔ q is equivalent to (p → q) ∧ (q → p).**

Proof by truth table:

| p | q | p → q | q → p | (p → q) ∧ (q → p) | p ↔ q |
|---|---|-------|-------|-------------------|-------|
| T | T | T     | T     | **T**             | T     |
| T | F | F     | T     | **F**             | F     |
| F | T | T     | F     | **F**             | F     |
| F | F | T     | T     | **T**             | T     |

The last two columns are identical. ∎

**p ↔ q is also equivalent to (p ∧ q) ∨ (¬p ∧ ¬q).**

This reads: "p and q are both true, or both are false." Verify this with a truth table as an exercise.


| p   | q   | p ∧ q | ¬p  | ¬q  | ¬p ∧ ¬q | (p ∧ q) ∨ (¬p ∧ ¬q) | p ↔ q |
| --- | --- | ----- | --- | --- | ------- | ------------------- | ----- |
| T   | T   | T     | F   | F   | F       | T                   | T     |
| T   | F   | F     | F   | T   | F       | F                   | F     |
| F   | T   | F     | T   | F   | F       | F                   | F     |
| F   | F   | F     | T   | T   | T       | T                   | T     |


---

## 7. Exclusive OR (XOR): ⊕

For completeness:

**Definition.** p ⊕ q ("p exclusive-or q") is true when exactly one of p, q is true.

| p | q | p ⊕ q |
|---|---|-------|
| T | T | F     |
| T | F | T     |
| F | T | T     |
| F | F | F     |

**Relationship to ↔:** p ⊕ q ≡ ¬(p ↔ q). XOR and biconditional are logical opposites.

**In hardware:** The XOR gate is fundamental in adder circuits. The sum bit of a half-adder is p ⊕ q; the carry bit is p ∧ q. When you implement addition in hardware (ECE 110), you are using XOR at the bit level.

**In cryptography:** XOR is the basis of one-time pad encryption. Encrypting message M with key K: `ciphertext` = M ⊕ K. `Decrypting`: M = `ciphertext` ⊕ K (since (M ⊕ K) ⊕ K = M ⊕ (K ⊕ K) = M ⊕ 0 = M). You will need to verify these algebraic identities, they follow from logical laws.

---

## 8. Reading Compound Formulas: Worked Decomposition

**Task:** Compute the truth value of (¬p ∧ q) ↔ (r → ¬q) when p = T, q = F, r = T.

Work from inner to outer:

```
Step 1: ¬p = ¬T = F
Step 2: ¬q = ¬F = T
Step 3: ¬p ∧ q = F ∧ F = F
Step 4: r → ¬q = T → T = T
Step 5: (¬p ∧ q) ↔ (r → ¬q) = F ↔ T = F
```

Answer: **F**

*Discipline:* Always resolve negations first, then work outward using precedence.

---

## 9. Truth Tables in Software: A Note

A truth table for n variables can be computed programmatically. In Python:

```python
from itertools import product

def truth_table(formula, variables):
    """
    formula: a function (dict -> bool) 
    variables: list of variable names
    """
    print(" | ".join(variables) + " | result")
    print("-" * (4 * (len(variables) + 1)))
    for assignment in product([True, False], repeat=len(variables)):
        env = dict(zip(variables, assignment))
        result = formula(env)
        row = " | ".join("T" if env[v] else "F" for v in variables)
        print(f"{row} | {'T' if result else 'F'}")

# Example: (p OR q) AND (NOT r)
truth_table(
    lambda e: (e['p'] or e['q']) and not e['r'],
    ['p', 'q', 'r']
)
```

This is not just a convenience, writing a truth table evaluator teaches you that logic is **computation**. The connectives are functions from truth values to truth values. Propositional logic is, in a precise sense, the theory of boolean functions.

---

## 10. Summary

| Concept | Key Fact |
|---|---|
| n variables | 2ⁿ rows in truth table |
| Conditional p → q | False only when p=T, q=F |
| p → q equivalence | p → q ≡ ¬p ∨ q |
| Contrapositive | p → q ≡ ¬q → ¬p (equivalent) |
| Converse/Inverse | q → p, ¬p → ¬q (NOT equivalent to original) |
| Biconditional | p ↔ q ≡ (p → q) ∧ (q → p) |
| XOR | p ⊕ q ≡ ¬(p ↔ q) |

---

## 11. End-of-Lecture Exercises

1. Build the complete truth table for each formula:
   - (a) (p → q) ∧ (¬p → r)
   - (b) (p ∧ ¬q) ∨ (¬p ∧ q) — What well-known connective does this equal?
   - (c) ¬(p ∨ q) ↔ (¬p ∧ ¬q) — What do you notice?
   - (d) (p → q) → ((q → r) → (p → r))

2. Given p = F, q = T, r = F, evaluate without a full truth table:
   - (a) (p ∧ q) → (r ∨ ¬p)
   - (b) ¬(p ↔ q) ∨ r
   - (c) (¬p → q) ∧ (q → ¬r)

3. Show that p → q and its inverse ¬p → ¬q have the **same** truth table as each other (even though neither is equivalent to the original).

4. The **NAND** connective (p NAND q) is defined as ¬(p ∧ q). Show that:
   - (a) ¬p ≡ p NAND p
   - (b) p ∧ q ≡ (p NAND q) NAND (p NAND q)
   - (c) p ∨ q ≡ (p NAND p) NAND (q NAND q)
   
   This shows NAND is **functionally complete** — all other connectives can be expressed with NAND alone. In hardware, this is why NAND gates are the universal building block of digital circuits.

5. A function f: {T,F}ⁿ → {T,F} is a **boolean function**. How many distinct boolean functions of 1 variable exist? Of 2 variables? Of n variables? (Hint: think about how many possible truth tables there are.)

---

## Reading

- **Rosen, 8e §1.1** — Truth tables of compound propositions
- **Epp, 5e §2.1–2.2** — Truth tables; conditional statements
- **Levin, 3e §3.1** — Propositional logic

*Next: Lecture 2 — [[L02 Tautologies and Logical Laws]]*
