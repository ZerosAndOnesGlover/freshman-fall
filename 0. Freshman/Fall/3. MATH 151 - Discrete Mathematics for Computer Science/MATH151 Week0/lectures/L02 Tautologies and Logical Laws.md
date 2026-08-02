# MATH 151: Discrete Mathematics for Computer Science
## Lecture 0.3. Tautologies, Contradictions, Logical Equivalence, and the Laws of Logic
### Friday, Week 0

---

> **Core Question:** How do we classify propositions by their truth behavior, and how do we prove equivalences *without* resorting to truth tables every time?

---

## 1. Classification of Propositions

Once you can build a truth table, you can classify any compound proposition into one of three categories:

### 1.1 Tautology

**Definition.** A proposition is a *tautology* if it is **true under every possible truth-value assignment**.

A tautology is necessarily true — true regardless of what the world is like.

**Examples:**
- p ∨ ¬p — "Either p or not p" (Law of Excluded Middle)
- p → p — "If p, then p"
- (p ∧ q) → p — "If both p and q, then p"

**Truth table for p ∨ ¬p:**

| p | ¬p | p ∨ ¬p |
|---|-----|--------|
| T | F   | **T**  |
| F | T   | **T**  |

All T. Tautology. ∎

**Notation:** We write ⊨ φ (or ⊢ φ) to mean "φ is a tautology" (φ is valid).

**Why do tautologies matter?**
- Tautologies are the theorems of propositional logic — statements provable from logic alone, without any facts about the world.
- In programming, a tautologically true condition is always-true — a sign of a possible bug: `while (true || user_input)` will always loop.
- In circuit design, a circuit implementing a tautology always outputs 1 — you can simplify it to a wire tied to power.

---

### 1.2 Contradiction

**Definition.** A proposition is a *contradiction* (also: *unsatisfiable*) if it is **false under every possible truth-value assignment**.

**Examples:**
- p ∧ ¬p — "p and not p"
- (p → q) ∧ p ∧ ¬q — asserting both a conditional and its violation simultaneously

**Truth table for p ∧ ¬p:**

| p | ¬p | p ∧ ¬p |
|---|-----|--------|
| T | F   | **F**  |
| F | T   | **F**  |

All F. Contradiction. ∎

**Why do contradictions matter?**
- In formal systems: if you can prove a contradiction, you can prove anything (ex falso quodlibet — "from false, anything follows"). This is why consistency is paramount.
- In code: a condition that is always false means dead code — the branch is unreachable.
- In hardware: a contradiction circuit always outputs 0 — simplify to ground.

---

### 1.3 Contingency

**Definition.** A proposition is a *contingency* if it is neither a tautology nor a contradiction — it is **true for some assignments and false for others**.

Most propositions we encounter are contingencies. Their truth value *depends on* (is contingent on) the state of the world.

**Example:** p → q is a contingency (true in rows 1, 3, 4; false in row 2 of the truth table from Lecture 0.2).

---

## 2. Logical Equivalence

**Definition.** Two propositions φ and ψ are *logically equivalent* if they have **identical truth values under every truth-value assignment**. We write φ ≡ ψ.

Equivalently: φ ≡ ψ if and only if φ ↔ ψ is a tautology.

**Method 1: Truth Table Verification**
Build both columns and check they are identical row-by-row.

**Method 2: Law-Based Proof**
Apply known equivalences algebraically, transforming one side into the other.

Method 2 is more powerful — it lets you reason about formulas too large for truth tables. We develop this now.

---

## 3. The Fundamental Laws of Propositional Logic

These are the algebraic laws of propositional logic. Each can be verified by truth table; memorize them and learn to apply them fluently.

### Law Group 1: Identity Laws

| Law | Formula |
|---|---|
| Identity for ∧ | p ∧ T ≡ p |
| Identity for ∨ | p ∨ F ≡ p |

(T and F are the constant true/false propositions.)

### Law Group 2: Domination Laws

| Law | Formula |
|---|---|
| Domination for ∧ | p ∧ F ≡ F |
| Domination for ∨ | p ∨ T ≡ T |

**Connection to code:** `if (condition && false)` → always false. The compiler optimizes this away.

### Law Group 3: Idempotent Laws

| Law | Formula |
|---|---|
| Idempotence of ∧ | p ∧ p ≡ p |
| Idempotence of ∨ | p ∨ p ≡ p |

### Law Group 4: Double Negation

| Law | Formula |
|---|---|
| Double Negation | ¬(¬p) ≡ p |

### Law Group 5: Commutativity

| Law | Formula |
|---|---|
| Commutativity of ∧ | p ∧ q ≡ q ∧ p |
| Commutativity of ∨ | p ∨ q ≡ q ∨ p |

### Law Group 6: Associativity

| Law | Formula |
|---|---|
| Associativity of ∧ | (p ∧ q) ∧ r ≡ p ∧ (q ∧ r) |
| Associativity of ∨ | (p ∨ q) ∨ r ≡ p ∨ (q ∨ r) |

### Law Group 7: Distributivity

| Law | Formula |
|---|---|
| Distributivity of ∧ over ∨ | p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r) |
| Distributivity of ∨ over ∧ | p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r) |

**Important:** Both distributions work — ∧ distributes over ∨, and ∨ distributes over ∧. This is unlike arithmetic where × distributes over + but + does not distribute over ×.

### Law Group 8: De Morgan's Laws ⭐

| Law | Formula |
|---|---|
| De Morgan 1 | ¬(p ∧ q) ≡ ¬p ∨ ¬q |
| De Morgan 2 | ¬(p ∨ q) ≡ ¬p ∧ ¬q |

**Verbal formulation:**
- "Not (p and q)" = "Not p, or not q"
- "Not (p or q)" = "Not p, and not q"

**Mnemonic:** To negate a conjunction/disjunction, negate each part and **flip the connective** (∧ ↔ ∨).

**Verification of De Morgan 1:**

| p | q | p ∧ q | ¬(p ∧ q) | ¬p | ¬q | ¬p ∨ ¬q |
|---|---|-------|---------|-----|-----|---------|
| T | T | T     | **F**   | F   | F   | **F**   |
| T | F | F     | **T**   | F   | T   | **T**   |
| F | T | F     | **T**   | T   | F   | **T**   |
| F | F | F     | **T**   | T   | T   | **T**   |

Columns 4 and 7 are identical. ∎

**De Morgan's Laws are deeply important:**

*In programming:*
```python
# These are logically equivalent:
not (x > 0 and y > 0)
(not x > 0) or (not y > 0)
x <= 0 or y <= 0
```

*In hardware design:* NAND = ¬(p ∧ q) = ¬p ∨ ¬q. NOR = ¬(p ∨ q) = ¬p ∧ ¬q. De Morgan's Laws tell you how NAND and NOR relate to the other gates.

*In database queries:*
```sql
-- These are equivalent:
NOT (age < 18 OR country = 'US')
age >= 18 AND country != 'US'
```

### Law Group 9: Absorption Laws

| Law | Formula |
|---|---|
| Absorption 1 | p ∨ (p ∧ q) ≡ p |
| Absorption 2 | p ∧ (p ∨ q) ≡ p |

**Intuition:** "p, or (p and q)" — if p is true, the whole thing is true. If p is false, (p ∧ q) is also false. So the ∨ with (p ∧ q) adds nothing.

### Law Group 10: Negation Laws

| Law | Formula |
|---|---|
| Excluded Middle | p ∨ ¬p ≡ T |
| Contradiction | p ∧ ¬p ≡ F |

### Conditional Laws

| Law | Formula |
|---|---|
| Conditional Equivalence | p → q ≡ ¬p ∨ q |
| Contrapositive | p → q ≡ ¬q → ¬p |
| Biconditional Expansion | p ↔ q ≡ (p → q) ∧ (q → p) |
| Biconditional Expansion 2 | p ↔ q ≡ (p ∧ q) ∨ (¬p ∧ ¬q) |

---

## 4. Proving Equivalences Algebraically

The power of these laws is that we can prove equivalences by algebraic manipulation — no truth table needed. This scales to formulas with many variables.

**Convention for proof layout:** Show each step on a new line with the law used in brackets.

### Worked Example 1

**Prove:** ¬(p → q) ≡ p ∧ ¬q

```
¬(p → q)
≡ ¬(¬p ∨ q)          [Conditional Equivalence: p→q ≡ ¬p∨q]
≡ ¬(¬p) ∧ ¬q         [De Morgan 2: ¬(A∨B) ≡ ¬A∧¬B]
≡ p ∧ ¬q             [Double Negation: ¬¬p ≡ p]
```

∎

**Reading this result:** The negation of "if p then q" is "p and not q." In other words: the only way to negate a conditional is to assert the hypothesis *and* deny the conclusion. This is the formal basis of proof by counterexample.

### Worked Example 2

**Prove:** p → (q → r) ≡ (p ∧ q) → r

(This is the *exportation* law — very useful in formal proofs.)

```
p → (q → r)
≡ ¬p ∨ (q → r)        [Conditional Equivalence]
≡ ¬p ∨ (¬q ∨ r)       [Conditional Equivalence]
≡ (¬p ∨ ¬q) ∨ r       [Associativity of ∨]
≡ ¬(p ∧ q) ∨ r        [De Morgan 1: ¬A∨¬B ≡ ¬(A∧B)]
≡ (p ∧ q) → r         [Conditional Equivalence]
```

∎

**Implication for CS:** This law is fundamental in functional programming and type theory. In Haskell, the type `a -> b -> c` (a function taking a and returning a function b→c) is isomorphic to the type `(a, b) -> c` (a function taking a pair). Currying is the exportation law.

### Worked Example 3

**Prove:** ¬(p ∨ ¬q) ∨ (¬p ∧ ¬q) ≡ ¬p

```
¬(p ∨ ¬q) ∨ (¬p ∧ ¬q)
≡ (¬p ∧ q) ∨ (¬p ∧ ¬q)      [De Morgan 2 on first term: ¬(p∨¬q) ≡ ¬p∧¬(¬q) ≡ ¬p∧q]
≡ ¬p ∧ (q ∨ ¬q)              [Distributivity of ∧ over ∨, factoring ¬p]
≡ ¬p ∧ T                     [Excluded Middle: q∨¬q ≡ T]
≡ ¬p                         [Identity for ∧]
```

∎

---

## 5. Normal Forms

Any propositional formula can be converted to standard forms that are convenient for automated processing.

### 5.1 Conjunctive Normal Form (CNF)

A formula is in **CNF** if it is a conjunction (AND) of *clauses*, where each clause is a disjunction (OR) of *literals* (variables or their negations).

```
CNF = (l₁ ∨ l₂ ∨ ...) ∧ (l₁' ∨ l₂' ∨ ...) ∧ ...
```

**Example:** (p ∨ ¬q) ∧ (¬p ∨ r ∨ q) ∧ (¬r)

**Why CNF?** SAT solvers — programs that determine if a logical formula is satisfiable — require input in CNF. The famous DPLL algorithm (Davis-Putnam-Logemann-Loveland, 1960) works on CNF. Modern SAT solvers (CDCL — Conflict-Driven Clause Learning) are essential tools in hardware verification, AI planning, and cryptography.

### 5.2 Disjunctive Normal Form (DNF)

A formula is in **DNF** if it is a disjunction (OR) of *minterms*, where each minterm is a conjunction (AND) of literals.

```
DNF = (l₁ ∧ l₂ ∧ ...) ∨ (l₁' ∧ l₂' ∧ ...) ∨ ...
```

**Example:** (p ∧ ¬q) ∨ (¬p ∧ q ∧ r) ∨ (¬p ∧ ¬r)

**Reading DNF from a truth table:** Each row where the formula is true corresponds to one minterm. The minterm includes each variable positively (if it's T in that row) or negated (if it's F). The DNF is the OR of all such minterms.

**Practical consequence:** Every boolean function can be expressed in DNF or CNF. This means every function computable by logic gates has a canonical normal form — this underpins digital circuit design and minimization (Karnaugh maps in ECE 110 are a technique for simplifying DNF/CNF).

---

## 6. Functional Completeness

**Definition.** A set of connectives is *functionally complete* if every boolean function can be expressed using only those connectives.

**{¬, ∧, ∨} is functionally complete** (any formula can be written using just these three).

**{¬, ∧} is functionally complete** (since p ∨ q ≡ ¬(¬p ∧ ¬q) by De Morgan).

**{NAND} alone is functionally complete** (shown in Exercise 4 of Lecture 0.2).

**{NOR} alone is functionally complete** (similar argument).

**Significance for hardware:** You need only one gate type — NAND or NOR — to build any digital circuit. This is why CMOS chips primarily use NAND and NOR gates.

---

## 7. Propositional Logic and Satisfiability

**Definition.** A formula φ is *satisfiable* if there exists at least one truth-value assignment that makes it true.

- Tautologies: satisfiable (every assignment satisfies them)
- Contradictions: **not** satisfiable
- Contingencies: satisfiable (some assignments satisfy them)

**The SAT problem:** Given a CNF formula, is it satisfiable?

SAT was the first problem proven NP-complete (Cook-Levin Theorem, 1971). There is no known polynomial-time algorithm. Yet modern SAT solvers solve instances with millions of variables in seconds through sophisticated heuristics. This is one of the great engineering achievements of the last 30 years.

You will revisit this in CS 102 and again in CS 301, where satisfiability becomes the canonical NP-complete problem.

---

## 8. Week 0 Synthesis — Logic as the Foundation

```
Propositions (atomic units of truth)
    ↓
Connectives (¬, ∧, ∨, →, ↔) build compound propositions
    ↓
Truth Tables mechanically determine truth under all assignments
    ↓
Classification: Tautology / Contradiction / Contingency
    ↓
Equivalence Laws allow algebraic manipulation
    ↓
Normal Forms (CNF/DNF) standardize formulas for computation
    ↓
Applications: circuit design, compiler optimization, SAT solving, formal verification
```

Every proof technique you learn in this course — direct proof, contradiction, contrapositive, induction — has its foundation in propositional logic. When you prove "if n² is odd, then n is odd" by contrapositive ("if n is even, then n² is even"), you are applying p → q ≡ ¬q → ¬p. The logic is the same; only the subject matter changes.

---

## 9. End-of-Lecture Exercises

1. Classify each as tautology, contradiction, or contingency. Justify with a truth table:
   - (a) (p → q) ∨ (q → p)
   - (b) (p ∧ q) ∧ ¬(p ∨ q)
   - (c) p ↔ (p ∧ (p ∨ q))
   - (d) (p → q) ∧ (¬p → q) → q

2. Prove each equivalence using *only* the laws from Section 3 (no truth tables):
   - (a) p → (p → q) ≡ p → q
   - (b) ¬p → (p → q) ≡ T (hint: it is a tautology)
   - (c) (p ∨ q) ∧ ¬p ≡ q ∧ ¬p

3. Convert to CNF:
   - (a) p ↔ q
   - (b) ¬(p ∨ q) ∨ r

4. Convert to DNF using truth table method:
   - (a) p ∧ (q ∨ r) (verify it matches the distributive law result)
   - (b) (p → q) ∧ (q → r)

5. **Deep question:** De Morgan's Laws say ¬(p ∧ q) ≡ ¬p ∨ ¬q. Is there an analogous law for conditionals? That is, what does ¬(p → q) simplify to? (Hint: use the conditional equivalence p → q ≡ ¬p ∨ q, then apply De Morgan.)

6. **Coding exercise:** Write a Python function `is_tautology(formula, n_vars)` that takes a formula as a Python function and the number of variables, and returns True iff the formula is a tautology. Use `itertools.product`. Test it on p ∨ ¬p and p ∧ ¬p.

---

*Week 0 complete. Week 1 begins: Predicate Logic, Quantifiers, and Logical Equivalences with Quantifiers.*
