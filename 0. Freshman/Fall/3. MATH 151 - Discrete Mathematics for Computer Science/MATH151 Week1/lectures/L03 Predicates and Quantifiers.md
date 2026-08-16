# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 1.1 (L03) — Predicates, Domains, and Quantifiers
### Monday, Week 1

**Date:** Monday 24 August 2026 · 13:00–13:50 · Week 1

---

> **Core Question:** How do we make precise mathematical statements about *all* objects in a collection, or about the *existence* of an object with some property?

---

## 1. The Limitation of Propositional Logic

Consider the argument:

1. Every integer divisible by 4 is divisible by 2.
2. 12 is divisible by 4.
3. Therefore, 12 is divisible by 2.

This argument is obviously valid. But propositional logic cannot capture *why* it is valid. If we assign:
- p = "Every integer divisible by 4 is divisible by 2"
- q = "12 is divisible by 4"
- r = "12 is divisible by 2"

Then the argument is p ∧ q → r, which is not a tautology in propositional logic — the truth of r does not follow from p ∧ q by propositional rules alone.

The problem: propositional logic treats p, q, r as atomic and cannot see *inside* them. It cannot exploit the logical structure of "every," "divisible by," or the relationship between 4, 2, and 12.

Predicate logic opens up these statements and gives us the tools to reason inside them.

---

## 2. Predicates

**Definition.** A *predicate* (also: *propositional function*) is a statement containing one or more variables that becomes a proposition when those variables are assigned specific values.

We write P(x), Q(x, y), R(x, y, z), etc.

**Examples:**

| Predicate | Notation | P(3) | P(−2) | P(0) |
|---|---|---|---|---|
| "x is positive" | P(x) | T | F | F |
| "x is even" | E(x) | F | T | T |
| "x² > x" | Q(x) | **T** (9 > 3) | T (4 > −2) | F (0 > 0 is false) |

Q(x) = "x² > x" repays a closer look, because its truth set is not what most people first guess:

- Q(3): 9 > 3 → **T**
- Q(−2): 4 > −2 → **T**
- Q(0): 0 > 0 → **F**
- Q(1): 1 > 1 → **F**
- Q(0.5): 0.25 > 0.5 → **F**

Over the reals, **Q(x) is false exactly on the closed interval [0, 1] and true everywhere else.**
Squaring only makes a number bigger when it is outside [0,1] — between 0 and 1 it makes it smaller,
and at the endpoints it changes nothing. Students who assume "squaring makes things bigger" get
three of these five wrong.

**Multi-variable predicates:**

| Predicate | Notation | Example |
|---|---|---|
| "x divides y" | D(x, y) | D(3, 12) = T, D(5, 12) = F |
| "x + y = z" | S(x, y, z) | S(2, 3, 5) = T, S(2, 3, 6) = F |
| "x is between a and b" | B(x, a, b) | B(5, 1, 10) = T |

**Key point:** A predicate by itself is neither true nor false — it is a *function* from objects to truth values. It becomes a proposition only when:
1. Every variable is replaced by a specific value, OR
2. Every variable is bound by a quantifier (defined below).

---

## 3. The Domain of Discourse

**Definition.** The *domain of discourse* (also: *universe of discourse*, *domain*) is the set of all objects that variables range over.

The domain is a critical part of the specification. The same predicate can have very different truth behavior over different domains.

**Example:** P(x) = "x² ≥ 0"
- Over ℝ (real numbers): TRUE for all x — P is always true
- Over ℂ (complex numbers): FALSE for some x — e.g., x = i gives i² = −1 < 0

**Example:** E(x) = "x is even"
- Over ℤ (integers): meaningful, true for {…, −4, −2, 0, 2, 4, …}
- Over ℝ: the concept of "even" doesn't apply to non-integers

**Convention:** If the domain is not stated, assume it is clear from context — but in formal work, *always specify the domain*.

**Common domains in this course:**
| Symbol | Domain |
|---|---|
| ℕ | Natural numbers {0, 1, 2, 3, …} (some texts start at 1) |
| ℤ | Integers {…, −2, −1, 0, 1, 2, …} |
| ℤ⁺ | Positive integers {1, 2, 3, …} |
| ℚ | Rational numbers |
| ℝ | Real numbers |
| ℂ | Complex numbers |

---

## 4. Universal Quantification — ∀

**Definition.** The *universal quantification* of P(x) over domain D, written **∀x P(x)** (read: "for all x, P(x)"), is the proposition that asserts P(x) is true for *every* element x in the domain D.

∀x P(x) is **true** if and only if P(a) is true for every element a in D.
∀x P(x) is **false** if and only if there exists at least one element a in D for which P(a) is false.

**Notation variants:** ∀x P(x), ∀x: P(x), (∀x)P(x), ∀x ∈ D, P(x)

### Examples

**Domain: ℤ (integers)**

| Statement | Truth Value | Reason |
|---|---|---|
| ∀x (x + 1 > x) | T | Adding 1 always increases an integer |
| ∀x (x² ≥ 0) | T | Squares of real integers are non-negative |
| ∀x (x² > 0) | F | Counterexample: x = 0 gives 0² = 0, not > 0 |
| ∀x (x is even) | F | Counterexample: x = 1 |
| ∀x (x + 0 = x) | T | Identity property of addition |

### Counterexamples

To prove ∀x P(x) is **false**, it suffices to exhibit one value a in the domain for which P(a) is false. This is called a **counterexample**.

**Example:** Disprove ∀x ∈ ℤ, x² > x.
- Counterexample: x = 0. Then x² = 0 and x = 0, so x² = x, not x² > x. ✗

**Example:** Disprove ∀x ∈ ℤ, x² ≠ x.
- Counterexample: x = 1. Then x² = 1 = x. ✗ (Also x = 0 works.)

**Why one counterexample suffices:** ∀x P(x) claims P is true for ALL x. One failure breaks the claim. This is asymmetric — one counterexample disproves a universal, but you cannot prove a universal with any finite number of examples (unless the domain is finite).

### Connection to Conjunction

Over a **finite** domain D = {a₁, a₂, …, aₙ}:

∀x P(x) ≡ P(a₁) ∧ P(a₂) ∧ … ∧ P(aₙ)

The universal quantifier is a *generalized conjunction* — AND over all elements of the domain.

Over an **infinite** domain, this conjunction is infinite — we cannot write it out, which is why we need the ∀ notation.

---

## 5. Existential Quantification — ∃

**Definition.** The *existential quantification* of P(x) over domain D, written **∃x P(x)** (read: "there exists an x such that P(x)"), is the proposition that asserts P(x) is true for *at least one* element x in D.

∃x P(x) is **true** if and only if there exists at least one element a in D for which P(a) is true.
∃x P(x) is **false** if and only if P(a) is false for every element a in D.

**Notation variants:** ∃x P(x), ∃x: P(x), ∃x ∈ D, P(x)

### Examples

**Domain: ℤ**

| Statement | Truth Value | Reason |
|---|---|---|
| ∃x (x² = 4) | T | Witness: x = 2 (or x = −2) |
| ∃x (x + 1 = x) | F | No integer satisfies this |
| ∃x (x < 0) | T | Witness: x = −1 |
| ∃x (x² < 0) | F | No real integer has negative square |
| ∃x (x is prime ∧ x is even) | T | Witness: x = 2 |

### Witnesses

To prove ∃x P(x) is **true**, exhibit one specific value a for which P(a) is true. This value is called a **witness** (or **example**).

**Example:** Prove ∃x ∈ ℤ, x² = 2x.
- Witness: x = 0. Then 0² = 0 = 2(0). ✓ (x = 2 also works: 4 = 4.)

**Example:** Prove ∃x ∈ ℤ, (x > 100) ∧ (x is prime).
- Witness: x = 101 (which is prime — verify: not divisible by 2, 3, 5, 7; √101 < 11). ✓

### Connection to Disjunction

Over a **finite** domain D = {a₁, a₂, …, aₙ}:

∃x P(x) ≡ P(a₁) ∨ P(a₂) ∨ … ∨ P(aₙ)

The existential quantifier is a *generalized disjunction* — OR over all elements.

---

## 6. Uniqueness Quantification — ∃!

**Definition.** **∃! x P(x)** (read: "there exists a unique x such that P(x)") asserts that P(x) is true for *exactly one* element of the domain.

∃! x P(x) ≡ ∃x (P(x) ∧ ∀y (P(y) → y = x))

(There exists an x satisfying P, and every other thing satisfying P is equal to x.)

**Examples:**
- ∃! x ∈ ℝ, x² = 0 — TRUE (only x = 0)
- ∃! x ∈ ℝ, x² = 1 — FALSE (both x = 1 and x = −1 satisfy this)
- ∃! x ∈ ℝ, x + 3 = 7 — TRUE (only x = 4)

**In CS:** Uniqueness quantification appears in database theory ("there is exactly one record with this primary key") and in function definitions ("for each input there is exactly one output").

---

## 7. Free and Bound Variables

**Definition.** In a formula, an occurrence of variable x is **bound** if it is within the scope of a quantifier ∀x or ∃x. Otherwise, it is **free**.

A formula with no free variables is a **closed formula** (a proposition — it has a definite truth value).
A formula with free variables is an **open formula** (a predicate — truth value depends on the free variables).

**Examples:**
- ∀x P(x, y) — x is bound, y is **free**. This is still a predicate in y.
- ∃x (x > y) — x is bound, y is free.
- ∀x ∃y (x + y = 0) — both x and y are bound. This is a proposition (T over ℤ).
- P(x) ∧ ∀x Q(x) — the x in P(x) is free; the x in Q(x) is bound. **Two different x's!**

**Warning:** Reusing the same variable name for both free and bound occurrences in one formula is legal but extremely confusing. In clean mathematical writing, rename the bound variable: P(x) ∧ ∀y Q(y).

---

## 8. Translating Between English and Predicate Logic

This is the most practically important skill of the week. It requires care — English is ambiguous, predicate logic is not.

### General Strategy
1. Identify the domain.
2. Define any predicates you need.
3. Identify the quantifier structure ("every," "some," "no," "at least one," "exactly one").
4. Write the formula.
5. Read it back in English to verify it says what you intended.

### Worked Examples

**Example 1:** "Every student in this class has studied calculus."

Domain: all people. Let S(x) = "x is a student in this class", C(x) = "x has studied calculus."

∀x (S(x) → C(x))

*Note:* With a universal quantifier over all people, the condition S(x) acts as a *filter* — we use → to say "for those x that are students, C(x) holds." A common error is ∀x (S(x) ∧ C(x)), which would mean "everyone is both a student in this class AND has studied calculus" — a much stronger claim.

**Universal statements over a restricted domain use →, not ∧.**

**Example 2:** "Some student in this class has not studied calculus."

∃x (S(x) ∧ ¬C(x))

*Note:* With an existential quantifier, the condition S(x) acts as a *conjunction* — we want an x that is both a student AND lacks calculus. A common error is ∃x (S(x) → ¬C(x)), which is true whenever there exists someone who is NOT a student (since F→anything = T). That's almost always true and not what we mean.

**Existential statements over a restricted domain use ∧, not →.**

This asymmetry — ∀ pairs with →, ∃ pairs with ∧ — is the single most common source of errors in predicate logic translation. Memorize it.

**Example 3:** "No integer is both even and odd."

Domain: ℤ. E(x) = "x is even", O(x) = "x is odd."

∀x ¬(E(x) ∧ O(x))

Equivalently: ∀x (E(x) → ¬O(x))

**Example 4:** "There is a largest prime" (we claim this is false).

Domain: ℤ⁺. P(x) = "x is prime."

∃x (P(x) ∧ ∀y (P(y) → y ≤ x))

This reads: there exists a prime x such that every prime y satisfies y ≤ x. This is FALSE — there is no largest prime (Euclid's theorem).

**Example 5:** "Every program that terminates produces correct output."

Domain: all programs. T(x) = "x terminates", C(x) = "x produces correct output."

∀x (T(x) → C(x))

---

## 9. CS Connection: Quantifiers as Loops

Over a finite domain {a₁, …, aₙ}, evaluating ∀x P(x) and ∃x P(x) corresponds directly to loops:

```python
# ∀x P(x): check P for every element
def forall(domain, predicate):
    for x in domain:
        if not predicate(x):
            return False    # found a counterexample
    return True

# ∃x P(x): find one element satisfying P
def exists(domain, predicate):
    for x in domain:
        if predicate(x):
            return True     # found a witness
    return False
```

This is not just an analogy — it is the precise computational meaning of quantifiers over finite domains. In databases:
- `SELECT * FROM users WHERE age > 18` implements ∃ (find elements satisfying a predicate)
- `SELECT COUNT(*) FROM users WHERE age > 18 = (SELECT COUNT(*) FROM users)` checks ∀

---

## 10. Summary

| Concept | Symbol | Meaning | True When | False When |
|---|---|---|---|---|
| Universal | ∀x P(x) | "For all x, P(x)" | P(a) true for every a | P(a) false for some a |
| Existential | ∃x P(x) | "There exists x with P(x)" | P(a) true for some a | P(a) false for every a |
| Uniqueness | ∃! x P(x) | "Exactly one x with P(x)" | P(a) true for exactly one a | 0 or ≥2 satisfy P |

**Translation rules:**
- ∀ with restricted domain → use **→**
- ∃ with restricted domain → use **∧**

---

## 11. End-of-Lecture Exercises

Domain for all problems: ℤ (integers) unless stated.

1. Let P(x) = "x² < 10". Find all x ∈ {−4, −3, −2, −1, 0, 1, 2, 3, 4} for which P(x) is true.

2. Determine the truth value of each. If false, give a counterexample; if true, explain why:
   - (a) ∀x ∈ ℤ, x² ≥ 0
   - (b) ∀x ∈ ℤ, x² > 0
   - (c) ∃x ∈ ℤ, x² = 2
   - (d) ∃x ∈ ℤ, x² = x
   - (e) ∀x ∈ ℤ⁺, ∃y ∈ ℤ⁺, y > x

3. Define predicates and translate into predicate logic. State your domain:
   - (a) "Not every real number has a square root that is real."
   - (b) "Some program runs forever."
   - (c) "Every even integer greater than 2 is the sum of two primes." (Goldbach's Conjecture)
   - (d) "There is no largest integer."

4. Translate into English. Domain: ℝ.
   - (a) ∀x (x² ≥ 0)
   - (b) ∃x (x³ = x)
   - (c) ∀x (x > 0 → ∃y (y² = x))

5. Identify all free and bound variables:
   - (a) ∀x (P(x) → Q(x, y))
   - (b) ∃x P(x) ∧ Q(x)
   - (c) ∀x ∃y (x + y = z)

---

*Next: Lecture 1.2 — Negating Quantified Statements, Quantifier Equivalence Laws*
