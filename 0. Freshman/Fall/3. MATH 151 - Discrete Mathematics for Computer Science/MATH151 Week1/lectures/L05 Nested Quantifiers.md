# MATH 151 — Discrete Mathematics for Computer Science
## Lecture 1.3 (L05) — Nested Quantifiers
### Friday, Week 1

---

> **Core Question:** What happens when we quantify over multiple variables simultaneously, and why does the *order* of quantifiers fundamentally change the meaning of a statement?

---

## 1. Motivation

The statements we have written so far involved a single quantified variable. But most interesting mathematical claims involve relationships between multiple variables:

- "For every integer x, there exists an integer y greater than x." (∀x ∃y)
- "There exists an integer y that is greater than every integer x." (∃y ∀x)

These two statements look similar but have drastically different meanings — one is true, one is absurd. Understanding this distinction is the heart of this lecture.

---

## 2. Nested Quantifiers — Definition

A **nested quantifier** expression has two or more quantifiers, each binding a different variable.

**General form:** Q₁x Q₂y P(x, y)

where Q₁ and Q₂ are each either ∀ or ∃.

The variables are bound from *outside in*: Q₁ binds x in the entire expression Q₂y P(x, y); Q₂ binds y in P(x, y).

**Reading procedure:** Read left to right, treating each quantifier as a new layer:

∀x ∃y P(x, y) reads as:
"For every x [fix any x], there exists some y [possibly depending on x] such that P(x, y)."

The key phrase: "possibly depending on x." The witness y in ∃y may be chosen *after seeing x*, and may be different for different choices of x.

---

## 3. The Four Combinations — ℤ as Domain

Let the domain be ℤ throughout. Let P(x, y) = "x < y" for illustration.

### Case 1: ∀x ∀y P(x, y) — "Every x is less than every y"

For all integers x and y, x < y.

**FALSE.** Counterexample: x = 5, y = 3. Then 5 < 3 is false.

### Case 2: ∀x ∃y P(x, y) — "For every x, some y is greater"

For every integer x, there exists an integer y with x < y.

**TRUE.** Given any x, take y = x + 1. Then x < x + 1. ✓

Note: y depends on x — we choose y *after* seeing x. Different x values lead to different witnesses y.

### Case 3: ∃x ∀y P(x, y) — "Some x is less than every y"

There exists an integer x that is less than every integer y.

**FALSE.** Any candidate x would need to satisfy x < y for all y, including y = x − 1. But x < x − 1 is false for all x ∈ ℤ. No smallest integer exists.

### Case 4: ∃x ∃y P(x, y) — "Some x is less than some y"

There exist integers x and y with x < y.

**TRUE.** Witness: x = 0, y = 1. Then 0 < 1. ✓

---

## 4. Order Matters — The Critical Asymmetry

The most important fact about nested quantifiers:

**∀x ∃y P(x, y) and ∃y ∀x P(x, y) are NOT logically equivalent in general.**

| Statement | Meaning | Relative Strength |
|---|---|---|
| ∀x ∃y P(x, y) | For each x, we can find a (possibly different) y | Weaker |
| ∃y ∀x P(x, y) | There is a single y that works for all x simultaneously | Stronger |

**∃y ∀x P(x, y) → ∀x ∃y P(x, y)** always holds (a single y that works for all x certainly works for each individual x).

**∀x ∃y P(x, y) → ∃y ∀x P(x, y)** does NOT hold in general — having a (potentially different) y for each x does not mean one y works for all x.

**Mathematical analogy:**
- ∀x ∃y (y = x + 1): For every integer, I can find a successor. TRUE. The successor depends on x.
- ∃y ∀x (y = x + 1): There is one integer that is the successor of every integer. FALSE — no single number is the successor of all integers.

---

## 5. Loop Interpretation of Nested Quantifiers

The loop analogy from Lecture 1.1 extends naturally to nested quantifiers:

```python
# ∀x ∀y P(x, y)
def forall_forall(domain, P):
    for x in domain:
        for y in domain:
            if not P(x, y):
                return False   # found counterexample (x, y)
    return True

# ∀x ∃y P(x, y)
def forall_exists(domain, P):
    for x in domain:
        found = False
        for y in domain:
            if P(x, y):
                found = True
                break          # found witness y for this x
        if not found:
            return False       # no witness for this x
    return True

# ∃x ∀y P(x, y)
def exists_forall(domain, P):
    for x in domain:
        works_for_all = True
        for y in domain:
            if not P(x, y):
                works_for_all = False
                break
        if works_for_all:
            return True        # x works for all y
    return False

# ∃x ∃y P(x, y)
def exists_exists(domain, P):
    for x in domain:
        for y in domain:
            if P(x, y):
                return True    # found witness pair (x, y)
    return False
```

The loop structure makes the quantifier order concrete: in `forall_exists`, the inner loop (finding y) runs fresh for each x — the witness y can depend on x. In `exists_forall`, we look for a single x that passes the inner ∀y check.

---

## 6. Negating Nested Quantifiers

Apply the negation rules repeatedly, pushing ¬ inward one quantifier at a time.

**Rule:** ¬ passes through each quantifier, flipping it (∀↔∃), until it reaches the predicate, which it then negates.

### Example 1

Negate: ∀x ∃y (x + y = 0)

Step 1: ¬(∀x ∃y (x + y = 0))
Step 2: ≡ ∃x ¬(∃y (x + y = 0))   [flip ∀ to ∃]
Step 3: ≡ ∃x ∀y ¬(x + y = 0)      [flip ∃ to ∀]
Step 4: ≡ ∃x ∀y (x + y ≠ 0)       [negate predicate]

**Reading:** "There exists an integer x such that for every integer y, x + y ≠ 0."

Original is TRUE (over ℤ: given x, take y = −x). So negation is FALSE.

### Example 2

Negate: ∃ε > 0, ∀δ > 0, ∃x (|x − a| < δ ∧ |f(x) − L| ≥ ε)

(This is the negation of the ε-δ definition of a limit — we'll return to it.)

Step 1: ¬(∃ε > 0, ...)
≡ ∀ε > 0, ¬(∀δ > 0, ...)
≡ ∀ε > 0, ∃δ > 0, ¬(∃x (...))
≡ ∀ε > 0, ∃δ > 0, ∀x, ¬(|x − a| < δ ∧ |f(x) − L| ≥ ε)
≡ ∀ε > 0, ∃δ > 0, ∀x, (|x − a| ≥ δ ∨ |f(x) − L| < ε)
≡ ∀ε > 0, ∃δ > 0, ∀x, (|x − a| < δ → |f(x) − L| < ε)

This is exactly the ε-δ definition of lim_{x→a} f(x) = L. The negation of "L is NOT the limit" is "L IS the limit." The quantifier structure of calculus limits is predicate logic in action.

### Example 3 — Proof Obligations

Negate: ∀x ∈ ℝ, ∀y ∈ ℝ, (x < y → ∃z ∈ ℝ, x < z < y)

(This says: between any two reals, there is a real — TRUE, take z = (x+y)/2.)

¬(∀x ∀y (x < y → ∃z, x < z < y))
≡ ∃x ∃y ¬(x < y → ∃z, x < z < y)
≡ ∃x ∃y (x < y ∧ ¬∃z, x < z < y)
≡ ∃x ∃y (x < y ∧ ∀z, ¬(x < z < y))
≡ ∃x ∃y (x < y ∧ ∀z, (z ≤ x ∨ z ≥ y))

**Reading:** "There exist reals x and y with x < y such that no real z lies strictly between them." This is the negation, and it is FALSE over ℝ (but TRUE over ℤ — e.g., there is no integer strictly between 0 and 1).

---

## 7. Quantifier Alternation and Complexity

The *quantifier alternation* pattern of a statement — how ∀ and ∃ alternate — determines its logical complexity and, in computability theory, its position in the arithmetical hierarchy.

| Pattern | Complexity | Typical Meaning |
|---|---|---|
| ∀x P(x) | Π₁ | Universal claim — falsified by one counterexample |
| ∃x P(x) | Σ₁ | Existential claim — verified by one witness |
| ∀x ∃y P(x, y) | Π₂ | "For every input, some output satisfies P" |
| ∃x ∀y P(x, y) | Σ₂ | "Some fixed x satisfies P for all y" |
| ∀x ∃y ∀z P(x, y, z) | Π₃ | Three alternations |

More alternations = harder to verify or falsify. A Π₂ statement (∀∃) cannot be verified by finite computation in general — you must check infinitely many x values, each requiring finding a witness y. This connects to the complexity classes studied in CS 301.

---

## 8. Common Mathematical Definitions as Nested Quantifiers

Many core mathematical definitions are nested quantified statements. Recognizing the quantifier structure clarifies what must be proved or disproved.

### Injectivity (one-to-one)

f: A → B is **injective** iff:
∀x₁ ∈ A, ∀x₂ ∈ A, (f(x₁) = f(x₂) → x₁ = x₂)

Equivalently (contrapositive of the inner implication):
∀x₁ ∈ A, ∀x₂ ∈ A, (x₁ ≠ x₂ → f(x₁) ≠ f(x₂))

To **prove** f is injective: assume f(x₁) = f(x₂) for arbitrary x₁, x₂, then derive x₁ = x₂.
To **disprove**: find specific x₁ ≠ x₂ with f(x₁) = f(x₂).

### Surjectivity (onto)

f: A → B is **surjective** iff:
∀y ∈ B, ∃x ∈ A, f(x) = y

To **prove**: given arbitrary y ∈ B, construct a specific x ∈ A with f(x) = y.
To **disprove**: find a specific y ∈ B with no preimage — prove ∃y ∈ B, ∀x ∈ A, f(x) ≠ y.

### Limit Definition

lim_{x→a} f(x) = L iff:
∀ε > 0, ∃δ > 0, ∀x ∈ ℝ, (0 < |x − a| < δ → |f(x) − L| < ε)

Three quantifiers, two alternations (∀∃∀). Proving a limit requires: given any ε (arbitrary positive real), *constructing* a δ that works (the witness), then verifying it works for *every* x in the δ-neighborhood.

### Uniform Continuity vs Pointwise Continuity

**Pointwise continuous** at every point:
∀x ∈ ℝ, ∀ε > 0, ∃δ > 0, ∀y ∈ ℝ, (|x − y| < δ → |f(x) − f(y)| < ε)

**Uniformly continuous:**
∀ε > 0, ∃δ > 0, ∀x ∈ ℝ, ∀y ∈ ℝ, (|x − y| < δ → |f(x) − f(y)| < ε)

The difference: in pointwise continuity, δ may depend on x (it is chosen after x is fixed). In uniform continuity, δ must work for all x simultaneously (it is chosen before x is fixed). This is exactly the ∀∃ vs ∃∀ distinction — the quantifiers are in a different order.

Every uniformly continuous function is continuous, but not vice versa. The logical reason: ∃δ ∀x is stronger than ∀x ∃δ.

---

## 9. Translation Workshop — Complex Statements

**Statement 1:** "Every sorting algorithm that is comparison-based requires Ω(n log n) comparisons in the worst case."

Domain: sorting algorithms.
C(a) = "a is comparison-based", T(a, n) = "a requires at least n log n comparisons in worst case."

∀a (C(a) → ∀n ∈ ℤ⁺, T(a, n))

**Statement 2:** "There exists a hash function such that for every input, the output is uniformly distributed."

Domain: hash functions and inputs.
H(h, x, y) = "hash function h maps input x to output y."

∃h ∀x ∀y₁ ∀y₂ (output_probability(h, x, y₁) = output_probability(h, x, y₂))

(Simplified — formally requires probability theory, but the quantifier structure is ∃∀∀∀.)

**Statement 3:** "The Collatz conjecture" — for every positive integer n, repeated application of the Collatz function eventually reaches 1.

Let C(n, k) = "applying the Collatz function k times to n yields 1."

∀n ∈ ℤ⁺, ∃k ∈ ℕ, C(n, k)

This is a ∀∃ statement. It has been verified computationally for all n up to approximately 2⁶⁸, but remains unproved in general.

---

## 10. Week 1 Synthesis

Predicate logic extends propositional logic by adding:

```
Predicates P(x), P(x,y), ...
    — properties of objects, true or false depending on input
    
Domains D
    — the universe of objects variables range over

Universal quantifier ∀x P(x)
    — P holds for every element of D
    — generalized conjunction
    — disproved by one counterexample

Existential quantifier ∃x P(x)
    — P holds for some element of D
    — generalized disjunction
    — proved by one witness

Negation rules
    — ¬∀x P(x) ≡ ∃x ¬P(x)
    — ¬∃x P(x) ≡ ∀x ¬P(x)

Nesting
    — ∀x ∃y ≠ ∃y ∀x in general
    — order of quantifiers is semantically critical
```

---

## 11. End-of-Lecture Exercises

Domain: ℤ unless stated.

1. Determine truth values. If false, give explicit counterexample(s):
   - (a) ∀x ∃y (y = x²)
   - (b) ∃x ∀y (y = x²)
   - (c) ∀x ∀y ∃z (z = x + y)
   - (d) ∃x ∃y (x² + y² = 0)
   - (e) ∀x ∃y (x · y = 1) over ℚ \ {0}
   - (f) ∀x ∃y (x · y = 1) over ℤ

2. Write the negation of each, pushing ¬ all the way inward. Simplify:
   - (a) ∀x ∀y (x² + y² > 0)
   - (b) ∃x ∀y (x ≤ y)
   - (c) ∀x ∃y ∀z (P(x, y) → Q(y, z))

3. Give predicate logic formulas for each. State the domain and any predicate definitions:
   - (a) "Every function has at most one output for each input." (Definition of function)
   - (b) "The sequence {aₙ} is bounded above." (∃M such that all terms ≤ M)
   - (c) "The sequence {aₙ} converges to L." (ε-N definition)
   - (d) "Two integers are coprime." (Their only common divisor is 1)

4. Consider f(x) = x² over domain ℝ. Determine:
   - (a) Is f injective? Write the injective definition as a quantified statement, evaluate it, and give a counterexample if false.
   - (b) Is f surjective onto ℝ? Write the surjective definition, evaluate, and find a y with no preimage if false.
   - (c) Is f surjective onto [0, ∞)? Re-evaluate.

5. **Deep question:** Show that these two statements are NOT equivalent by finding a domain and predicate P(x, y) where one is true and the other is false:
   - ∀x ∃y P(x, y)
   - ∃y ∀x P(x, y)

---

*Week 1 complete. Week 2: Proof Techniques — Direct Proof, Proof by Contradiction, Proof by Contrapositive.*
