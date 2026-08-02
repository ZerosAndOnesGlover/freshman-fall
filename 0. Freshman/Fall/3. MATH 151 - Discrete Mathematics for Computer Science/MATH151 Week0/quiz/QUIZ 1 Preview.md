# MATH 151 · Discrete Mathematics for Computer Science
## Quiz 1 Scope Preview
### Quiz administered: Monday, Week 1 (first 15 minutes of lecture)

---

**Format:** 4–5 short problems. No notes. No calculator. 15 minutes.

**Coverage:** Weeks 0 and 1 material:
- Week 0: Propositional logic (propositions, connectives, truth tables, tautologies, equivalence laws)
- Week 1: Predicate logic and quantifiers (covered next week)

---

## What You Must Know Cold for Week 0 Material

### 1. Connective Definitions (from memory)

You must be able to immediately write the 4-row truth table for:
- ¬p
- p ∧ q
- p ∨ q
- p → q (including explaining why F → anything is T)
- p ↔ q

No partial credit for incorrect conditional rows.

### 2. Operator Precedence

Given a formula without explicit parentheses, correctly parse it:
- ¬ binds tightest
- Then ∧
- Then ∨
- Then →
- Then ↔

**Example:** ¬p ∨ q → r ∧ ¬s should parse as (¬p ∨ q) → (r ∧ ¬s)

### 3. Truth Table Construction

Build a truth table for a 2- or 3-variable formula in the time available (< 5 minutes). This requires:
- Knowing the 2ⁿ row count
- Correct systematic column filling
- Correct evaluation of each row

### 4. Classification

Given a completed truth table, classify the formula as tautology, contradiction, or contingency.

### 5. The Laws (must apply, not just recognize)

You will be given one or two algebraic equivalence proofs to complete. Know these cold:
- Double Negation
- De Morgan's Laws (both)
- Distributivity (both directions — ∧ over ∨, and ∨ over ∧)
- Conditional Equivalence: p → q ≡ ¬p ∨ q
- Contrapositive: p → q ≡ ¬q → ¬p
- Absorption Laws
- Identity and Domination Laws

### 6. Translation

Translate English ↔ logical formulas. Know these patterns:
- "p only if q" = p → q
- "p unless q" = ¬q → p (equivalently p ∨ q)
- "neither p nor q" = ¬p ∧ ¬q
- "p is necessary for q" = q → p
- "p is sufficient for q" = p → q

---

## Sample Quiz Problems (Representative, not actual quiz)

**Problem 1.** (3 pts) Write the truth table for: (p ∧ ¬q) → r

**Problem 2.** (3 pts) Prove using logical laws (no truth table): ¬(p → q) ≡ p ∧ ¬q

**Problem 3.** (3 pts) Translate: "The function terminates if and only if the input is finite and memory does not overflow."

Variables: p = "function terminates", q = "input is finite", r = "memory overflows"

**Problem 4.** (3 pts) Is (p → q) ∨ (q → r) a tautology, contradiction, or contingency? Justify.

**Problem 5.** (3 pts) Apply De Morgan's Law to simplify: ¬(¬p ∧ (q ∨ ¬r))

---

## Study Recommendations

1. **Do not just read — write.** Practice building truth tables by hand until you can do a 3-variable table in under 3 minutes.

2. **Flashcards for the laws.** Write each law on one side; the name on the other. Drill until instantaneous.

3. **Practice algebraic proofs.** Take any formula, convert it to CNF step by step. Then convert back. Fluency requires repetition.

4. **Work PS0 completely.** The problem set is the best quiz preparation.

5. **Focus on the conditional.** Most errors on quizzes and exams involve incorrect handling of p → q, especially the vacuous truth rows.

---

## After the Quiz

The remaining class time on Week 2 Monday will cover **Predicate Logic and Quantifiers** (Week 1 material, Lecture 1.0). Bring your course reader.
