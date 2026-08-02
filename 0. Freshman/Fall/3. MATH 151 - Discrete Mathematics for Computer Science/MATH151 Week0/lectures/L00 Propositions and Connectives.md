# MATH 151 Discrete Mathematics for Computer Science
## Lecture 0.1. Propositions and Logical Connectives
### Monday, Week 0

---

> **Core Question:** What is a *precise* statement, and how do we build complex precise statements from simple ones?

---

## 0. Why Logic?

Mathematics is built on proofs. Proofs are built on logic. Before you can prove anything, that an algorithm is correct, that a data structure maintains its invariant, that a program terminates; you need a language for making and combining claims with surgical precision.

Natural language fails us. Consider:

> "You can pass if you study or you are lucky."

Does this mean:
- (a) You can pass if you study. Separately, you can pass if you are lucky.
- (b) You need both, to study *and* to be lucky, in order to pass.
- (c) Something else?

Ambiguity is tolerable in conversation. It is catastrophic in mathematics and engineering. This week we build a **formal language**, propositional logic, that eliminates ambiguity.

---

## 1. Propositions

**Definition (Proposition).** A *proposition* is a declarative sentence that is either **true** or **false**, but not both.

The truth value of a proposition is either **T** (true) or **F** (false). (Some texts use 1/0 or ⊤/⊥.)

### Examples of Propositions

| Statement                                                    | Proposition?                                              | Truth Value                            |
| ------------------------------------------------------------ | --------------------------------------------------------- | -------------------------------------- |
| "2 + 2 = 4"                                                  | ✓ Yes                                                     | T                                      |
| "The integer 7 is even"                                      | ✓ Yes                                                     | F                                      |
| "Every even integer greater than 2 is the sum of two primes" | ✓ Yes                                                     | Unknown (Goldbach's Conjecture: open!) |
| "What time is it?"                                           | ✗ No (question)                                           | —                                      |
| "Close the door."                                            | ✗ No (command)                                            | —                                      |
| "x + 1 = 5"                                                  | ✗ No (depends on x, a *predicate*, not yet a proposition) | —                                      |
| "This statement is false."                                   | ✗ No (paradox, the Liar's Paradox)                        | —                                      |

> **Important:** A proposition must have a definite truth value, even if *we* don't know it. Goldbach's Conjecture is a proposition; "x + 1 = 5" is not (it becomes a proposition when x is specified).

---

## 2. Propositional Variables

We use lowercase letters, typically **p, q, r, s**, as **propositional variables**: placeholders for propositions.

```
p := "It is raining."
q := "I carry an umbrella."
r := "The ground is wet."
```

This notation `:=` means "is defined as."

The truth value of p is determined by the actual state of the world. In abstract logic, we consider all possible truth-value assignments.

---

## 3. Logical Connectives

Given propositions p and q, we build **compound propositions** using **logical connectives**. There are five fundamental connectives.

---

### 3.1 Negation ("NOT" ¬)

**Definition.** The *negation* of proposition p, written **¬p** (also written ~p or !p in code), is true when p is false, and false when p is true.

**Truth Table:**

| p | ¬p |
|---|---|
| T | F |
| F | T |

**Examples:**
- p = "It is raining." → ¬p = "It is **not** raining."
- p = "7 is even." → ¬p = "7 is **not** even." (equivalently, "7 is odd.")

**In code:** `!p` in C/Java/Python, `not p` in Python, `~p` in boolean contexts.

**Deep Note:** Double negation: ¬(¬p) ≡ p. Negating twice returns to the original. This seems obvious, but it fails in *constructive* (intuitionistic) logic, which matters in formal verification and some functional programming type theories. For this course, we work in classical logic where ¬(¬p) ≡ p always holds.

---

### 3.2 Conjunction ("AND" ∧)

**Definition.** The *conjunction* of p and q, written **p ∧ q**, is true if and only if **both** p and q are true.

**Truth Table:**

| p | q | p ∧ q |
|---|---|---|
| T | T | **T** |
| T | F | F |
| F | T | F |
| F | F | F |

**Examples:**
- "It is raining **and** I carry an umbrella." → True only when both are true.
- In Python: `p and q` short-circuits: if p is False, q is never evaluated.

**Key Property:** Conjunction is *demanding*, all conditions must hold.

**In hardware (ECE 110):** The AND gate computes p ∧ q.

---

### 3.3 Disjunction ("OR" ∨)

**Definition.** The *disjunction* of p and q, written **p ∨ q**, is true if **at least one** of p and q is true.

**Truth Table:**

| p | q | p ∨ q |
|---|---|---|
| T | T | **T** |
| T | F | **T** |
| F | T | **T** |
| F | F | F |

**Examples:**
- "I will study **or** I will fail." → This is true even if you both study *and* fail (unlikely but logically consistent).
- In Python: `p or q` short-circuits: if p is True, q is never evaluated.

**Warning: Inclusive vs. Exclusive OR:**
The mathematical ∨ is **inclusive OR**: "p or q (or both)."

Everyday English "or" is often **exclusive OR**: "Tea or coffee?" (not both). We denote exclusive OR by **p ⊕ q** (also written XOR). We study this separately.

**In hardware (ECE 110):** The OR gate computes p ∨ q. The XOR gate computes p ⊕ q.

---

### 3.4 Conditional ("IF...THEN" →)

**Definition.** The *conditional* (also: *implication*) **p → q** is false **only** when p is true and q is false. In all other cases, it is true.

**Truth Table:**

| p | q | p → q |
|---|---|---|
| T | T | **T** |
| T | F | **F** |
| F | T | **T** |
| F | F | **T** |

Here:
- **p** is the *hypothesis* (also: antecedent, premise)
- **q** is the *conclusion* (also: consequent)

**Reading p → q:**
- "If p, then q."
- "p implies q."
- "p only if q." (p can be true only when q is true)
- "q if p."
- "q whenever p."
- "p is sufficient for q."
- "q is necessary for p."

**The controversial rows:** When p is false (rows 3 and 4), the conditional is **vacuously true**.

**Why?** Consider a contract: "If you score above 90, you get an A."
- You score 95 and get an A: contract honored. (T, T → T) ✓
- You score 95 but get a B: contract *violated*. (T, F → F) ✗
- You score 75 and get an A: contract not violated — the contract said nothing about scores ≤ 90. (F, T → T) ✓
- You score 75 and get a B: contract not violated — it didn't promise anything here. (F, F → T) ✓

The conditional makes a promise only when the hypothesis is true. When the hypothesis is false, the promise is vacuous, and vacuous promises are not lies.

**Programming analogy:**
```python
# This function's contract: "if x > 0, return x"
# If x = -5, the function has no obligation — it may do anything
def f(x):
    if x > 0:
        return x
    # When x <= 0, the contract is silent
```

---

### 3.5 Biconditional ("IF AND ONLY IF" ↔)

**Definition.** The *biconditional* **p ↔ q** is true when p and q have the **same truth value**.

**Truth Table:**

| p   | q   | p ↔ q |
| --- | --- | ----- |
| T   | T   | **T** |
| T   | F   | F     |
| F   | T   | F     |
| F   | F   | **T** |

**Reading p ↔ q:**
- "p if and only if q." (abbreviated "p iff q")
- "p is necessary and sufficient for q."
- "p exactly when q."

**Relationship to →:** Note that p ↔ q ≡ (p → q) ∧ (q → p). A biconditional is the conjunction of both directions. (We will prove this next lecture using truth tables.)

**In mathematics:** Biconditionals are extremely common, nearly every definition in mathematics is an "iff" statement.
- "An integer `n` is even **if and only if** there exists an integer `k` such that `n = 2k`." (In other words, "Being even is **exactly equivalent** to being twice an integer.", or in division terms, "An integer is even **if and only if** it is divisible by 2.")
- "A function `f` is bijective **if and only if** it is injective and surjective."

---

## 4. Operator Precedence

When we write ¬p ∧ q → r ∨ s ↔ t, how do we parse it? By convention:

| Priority | Operator | Notes |
|---|---|---|
| 1 (highest) | ¬ | Negation binds tightest — it applies to the immediately adjacent proposition |
| 2 | ∧ | Conjunction (AND) |
| 3 | ∨ | Disjunction (OR) |
| 4 | → | Conditional (right-associative) |
| 5 (lowest) | ↔ | Biconditional |

**Right-associativity of →:** p → q → r means p → (q → r), not (p → q) → r.

**Examples:**

```
¬p ∧ q         means  (¬p) ∧ q           [¬ before ∧]
p ∧ q ∨ r      means  (p ∧ q) ∨ r        [∧ before ∨]
p → q ∧ r      means  p → (q ∧ r)        [∧ before →]
¬p ∨ q → r    means  (¬p ∨ q) → r       [¬,∨ before →]
```

**Advice:** When in doubt, parenthesize. Clarity beats cleverness.

---

## 5. Translating Between English and Logic

This is a skill that requires practice. Some patterns:

| English | Logic |
|---|---|
| "p and q" | p ∧ q |
| "p but q" | p ∧ q (same logical meaning) |
| "neither p nor q" | ¬p ∧ ¬q (equivalently ¬(p ∨ q)) |
| "p unless q" | ¬q → p (equivalently p ∨ q) |
| "p only if q" | p → q |
| "p if q" | q → p |
| "p iff q" | p ↔ q |
| "not both p and q" | ¬(p ∧ q) |

**Worked Example:**

Statement: "You will fail the exam if and only if you neither study nor attend lecture."

Let:
- p = "You fail the exam."
- q = "You study."
- r = "You attend lecture."

Translation:
- "neither study nor attend lecture" = ¬q ∧ ¬r
- "fail iff neither..." = p ↔ (¬q ∧ ¬r)

---

## 6. The Connection to Code

Every `if` statement in every programming language is a conditional proposition. Every boolean expression you write is a propositional formula.

```python
# Python
if (x > 0) and (not flag or y < 10):
    do_something()
```

In logical notation: Let p = "x > 0", q = "flag", r = "y < 10".

The condition is: p ∧ (¬q ∨ r)

Understanding the truth table of this formula tells you exactly under which combinations of p, q, r the branch is taken, no ambiguity, no surprises.

**Short-circuit evaluation:** Python and C/C++ evaluate `and`/`&&` and `or`/`||` lazily:
- `p and q`: if p is F, q is never evaluated. (Safe: `if ptr != NULL and ptr->val > 0`)
- `p or q`: if p is T, q is never evaluated.

This matters for correctness when q has side effects or could cause an error.

---

## 7. Summary

| Connective | Symbol | True When |
|---|---|---|
| Negation | ¬p | p is F |
| Conjunction | p ∧ q | Both T |
| Disjunction | p ∨ q | At least one T |
| Conditional | p → q | Not (p=T and q=F) |
| Biconditional | p ↔ q | Same truth value |

**Precedence (high to low):** ¬ > ∧ > ∨ > → > ↔

---

## 8. End-of-Lecture Exercises

Work these before Thursday's lecture:

1. Determine whether each sentence is a proposition. If so, state its truth value:
   - (a) "The sum of two odd integers is even." --- A proposition (T)
   - (b) "Did you finish the homework?" Not a proposition
   - (c) "n² + 1 is prime."  A proposition ()
   - (d) "There exists a greatest prime number." A proposition (T)

2. Let p = "The program terminates", q = "The input is valid", r = "Memory is available." Translate each into logical notation:
   - (a) "The program terminates if the input is valid and memory is available." (p ->q V r)
   - (b) "The program terminates only if memory is available."
   - (c) "If the program does not terminate, then either the input is invalid or memory is unavailable."
   - (d) "The program terminates if and only if both the input is valid and memory is available."

1. Write the truth table for: ¬p ∧ (q ∨ r)

| p   | q   | r   | ¬p  | (q ∨ r) | ¬p ∧ (q ∨ r) |
| --- | --- | --- | --- | ------- | ------------ |
| T   | T   | T   | F   | T       | F            |
| T   | T   | F   | F   | T       | F            |
| F   | F   | T   | T   | T       | T            |
| F   | F   | F   | T   | F       | F            |



3. Determine the truth value of each proposition (take p = T, q = F, r = T):
   - (a) (p ∧ q) → r
   - (b) ¬p ∨ (q → r)
   - (c) (p ↔ r) ∧ ¬q
   - (d) ¬(p ∧ ¬q) → (r ∨ q)

---

*Next: Lecture 0.2 — [[L01 Truth Tables]]*
