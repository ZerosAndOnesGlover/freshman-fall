# MATH 151 · Discrete Mathematics for Computer Science
## Lab 1 — Quantifier Workshop: Translation, Evaluation, and Computation
### Wednesday 7 October 2026, 15:00–16:50 · Week 2 | Duration: 2 hours | Covers Week 1 (all three lectures)

---

**Lab Objectives:**
1. Translate English statements into predicate logic and back with precision
2. Evaluate quantified statements over explicit finite domains
3. Correctly negate nested quantified statements
4. Extend the Python logic toolkit from Lab 0 to handle predicates and quantifiers
5. Discover the effect of quantifier order computationally

**Materials:** Lab 0's `logic_tools.py`, a text editor, Python 3.

---

## Section 1 — Hand Exercises: Evaluation over Finite Domains (35 min)

For all problems in this section, work by hand. Show every step.

### Exercise 1.1 — Evaluating Quantified Statements

**Domain:** D = {1, 2, 3, 4, 5, 6}

Evaluate each statement as TRUE or FALSE. If FALSE, exhibit a counterexample; if TRUE, explain why every element satisfies the predicate.

Let:
- E(x) = "x is even" = {2, 4, 6}
- O(x) = "x is odd" = {1, 3, 5}
- P(x) = "x is prime" = {2, 3, 5}
- G(x, y) = "x > y"
- D(x, y) = "x divides y"

**(a)** ∀x ∈ D, (E(x) ∨ O(x))

**(b)** ∀x ∈ D, (E(x) ∧ O(x))

**(c)** ∃x ∈ D, (P(x) ∧ E(x))

**(d)** ∀x ∈ D, (P(x) → O(x))

**(e)** ∃x ∈ D, ∀y ∈ D, G(x, y)

**(f)** ∀x ∈ D, ∃y ∈ D, G(x, y)

**(g)** ∀x ∈ D, ∀y ∈ D, (D(x, y) → D(x, y + x))

**(h)** ∃x ∈ D, ∃y ∈ D, (x ≠ y ∧ x² = y)

---

### Exercise 1.2 — The Quantifier Order Experiment

Domain: D = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}. Predicate: P(x, y) = "x divides y."

Fill in the following table. For each (x, y) pair, mark T if x divides y, F otherwise. Use this to answer the quantified questions below.

|   | y=1 | y=2 | y=3 | y=4 | y=5 | y=6 | y=7 | y=8 | y=9 | y=10 |
|---|---|---|---|---|---|---|---|---|---|---|
| x=1 | | | | | | | | | | |
| x=2 | | | | | | | | | | |
| x=3 | | | | | | | | | | |
| x=4 | | | | | | | | | | |
| x=5 | | | | | | | | | | |

(Fill only x = 1 through 5 — enough rows for the questions below.)

Using your table:

**(a)** Is ∀x ∈ D, ∃y ∈ D, P(x, y) true? (For each x, does some y in {1…10} exist that x divides?)

**(b)** Is ∃y ∈ D, ∀x ∈ {1,2,3,4,5}, P(x, y) true? (Is there a y divisible by all of 1, 2, 3, 4, 5?)

**(c)** Are (a) and (b) equivalent? What does your table show about quantifier order?

**(d)** Identify the witness for (a) for each x. Does the witness y depend on x?

**(e)** If (b) is true, identify the witness y. Is this the same y for every x, or different?

---

### Exercise 1.3 — Negation Practice

Write the negation of each statement, push ¬ all the way inward, then evaluate both the original and negation:

Domain: ℤ.

**(a)** ∀x, ∃y, (y = x + 1)

**(b)** ∃x, ∀y, (x · y = y)

**(c)** ∀x, ∀y, (x < y → x² < y²)
*(Hint: is the original true? Try x = −3, y = 1.)*

**(d)** ∃x, ∃y, (x² + y² = 3)

---

### Exercise 1.4 — Translation Drill

For each, write a precise predicate logic formula AND translate it back into a different English sentence that conveys the same meaning:

**(a)** "Every email address belongs to at most one user account."

**(b)** "There exists a password that no user has chosen."

**(c)** "For every bug, there exists a developer who can fix it."

**(d)** "Some feature is requested by every user."

**(e)** "No test case passes on an incorrect implementation."

---

## Section 2 — Python: Predicate Evaluator (55 min)

You will extend `logic_tools.py` with predicate and quantifier evaluation. Create a new file `predicate_tools.py` that imports from `logic_tools.py`.

### Exercise 2.1 — Quantifier Functions

```python
def forall(domain, predicate):
    """
    Evaluates ∀x ∈ domain, predicate(x).
    Returns (bool, counterexample_or_None).
    If True, counterexample is None.
    If False, counterexample is the first x where predicate(x) is False.
    """
    for x in domain:
        if not predicate(x):
            return False, x
    return True, None


def exists(domain, predicate):
    """
    Evaluates ∃x ∈ domain, predicate(x).
    Returns (bool, witness_or_None).
    If True, witness is the first x where predicate(x) is True.
    If False, witness is None.
    """
    for x in domain:
        if predicate(x):
            return True, x
    return False, None


def forall_verbose(domain, predicate, pred_name="P"):
    """Evaluates ∀x P(x) and prints a summary."""
    result, counterex = forall(domain, predicate)
    if result:
        print(f"∀x {pred_name}(x): TRUE over domain of size {len(list(domain))}")
    else:
        print(f"∀x {pred_name}(x): FALSE. Counterexample: x = {counterex}")
    return result


def exists_verbose(domain, predicate, pred_name="P"):
    """Evaluates ∃x P(x) and prints a summary."""
    result, witness = exists(domain, predicate)
    if result:
        print(f"∃x {pred_name}(x): TRUE. Witness: x = {witness}")
    else:
        print(f"∃x {pred_name}(x): FALSE. No witness found in domain.")
    return result
```

**Task:** Add these to `predicate_tools.py`. Test on these examples:

```python
domain = range(-10, 11)  # integers -10 to 10

# Test 1: ∀x, x² ≥ 0
forall_verbose(domain, lambda x: x**2 >= 0, "x²≥0")

# Test 2: ∀x, x² > 0
forall_verbose(domain, lambda x: x**2 > 0, "x²>0")

# Test 3: ∃x, x² = 4
exists_verbose(domain, lambda x: x**2 == 4, "x²=4")

# Test 4: ∃x, x² = 3
exists_verbose(domain, lambda x: x**2 == 3, "x²=3")
```

---

### Exercise 2.2 — Nested Quantifiers

```python
def forall_forall(domain1, domain2, predicate):
    """∀x ∈ domain1, ∀y ∈ domain2, P(x, y)."""
    for x in domain1:
        for y in domain2:
            if not predicate(x, y):
                return False, (x, y)   # counterexample pair
    return True, None


def forall_exists(domain1, domain2, predicate):
    """∀x ∈ domain1, ∃y ∈ domain2, P(x, y)."""
    for x in domain1:
        found = False
        for y in domain2:
            if predicate(x, y):
                found = True
                break
        if not found:
            return False, x   # x with no witness
    return True, None


def exists_forall(domain1, domain2, predicate):
    """∃x ∈ domain1, ∀y ∈ domain2, P(x, y)."""
    for x in domain1:
        if all(predicate(x, y) for y in domain2):
            return True, x    # the witness x
    return False, None


def exists_exists(domain1, domain2, predicate):
    """∃x ∈ domain1, ∃y ∈ domain2, P(x, y)."""
    for x in domain1:
        for y in domain2:
            if predicate(x, y):
                return True, (x, y)
    return False, None
```

**Task:** Add to `predicate_tools.py`. Use domain = range(1, 11) (integers 1–10) to verify your hand answers from Exercise 1.2:

```python
D = list(range(1, 11))

def divides(x, y):
    return y % x == 0

# Test the four quantifier combinations with P(x,y) = "x divides y"
print("∀x ∀y D(x,y):", forall_forall(D, D, divides))
print("∀x ∃y D(x,y):", forall_exists(D, D, divides))
print("∃x ∀y D(x,y):", exists_forall(D, D, divides))
print("∃x ∃y D(x,y):", exists_exists(D, D, divides))
```

For each result, explain in one sentence what the output reveals about divisibility.

---

### Exercise 2.3 — Quantifier Order Demonstrator

Write a function that, given a predicate P(x, y), evaluates all four combinations (∀∀, ∀∃, ∃∀, ∃∃) and prints a comparison:

```python
def quantifier_comparison(domain1, domain2, predicate, pred_name="P(x,y)"):
    """
    Compares all four quantifier combinations for a 2-variable predicate.
    """
    print(f"\nQuantifier analysis for: {pred_name}")
    print(f"Domain: {list(domain1)[:5]}... (size {len(list(domain1))})")
    print("-" * 50)
    
    results = {
        "∀x ∀y": forall_forall(domain1, domain2, predicate),
        "∀x ∃y": forall_exists(domain1, domain2, predicate),
        "∃x ∀y": exists_forall(domain1, domain2, predicate),
        "∃x ∃y": exists_exists(domain1, domain2, predicate),
    }
    
    for quantifier, (truth, evidence) in results.items():
        status = "TRUE" if truth else "FALSE"
        evidence_str = f"  (evidence: {evidence})" if evidence is not None else ""
        print(f"  {quantifier} {pred_name}: {status}{evidence_str}")
    
    print()
    # Check the expected implication: (∃x∀y) should imply (∀x∃y)
    if results["∃x ∀y"][0] and not results["∀x ∃y"][0]:
        print("  WARNING: ∃∀ is True but ∀∃ is False — this should be impossible!")
    elif results["∃x ∀y"][0]:
        print("  Note: ∃x∀y is True, which implies ∀x∃y is also True (as expected).")
```

**Task:** Run this on three different predicates and interpret the output:

```python
D = list(range(1, 8))

# Predicate 1: x < y
quantifier_comparison(D, D, lambda x, y: x < y, "x < y")

# Predicate 2: x + y == 7
quantifier_comparison(D, D, lambda x, y: x + y == 7, "x+y=7")

# Predicate 3: x * y == x
quantifier_comparison(D, D, lambda x, y: x * y == x, "x*y=x")
```

For each predicate, write 2–3 sentences interpreting the pattern of True/False results.

---

### Exercise 2.4 — Negation Verifier

Write a function that verifies De Morgan's Laws for quantifiers computationally:

```python
def verify_quantifier_negation(domain, predicate, pred_name="P"):
    """
    Verifies:
    1. ¬(∀x P(x)) ≡ ∃x ¬P(x)
    2. ¬(∃x P(x)) ≡ ∀x ¬P(x)
    """
    neg_pred = lambda x: not predicate(x)
    
    # Check Law 1: ¬(∀x P(x)) ≡ ∃x ¬P(x)
    forall_result, _ = forall(domain, predicate)
    exists_neg_result, witness = exists(domain, neg_pred)
    
    law1_holds = (not forall_result) == exists_neg_result
    
    # Check Law 2: ¬(∃x P(x)) ≡ ∀x ¬P(x)
    exists_result, _ = exists(domain, predicate)
    forall_neg_result, _ = forall(domain, neg_pred)
    
    law2_holds = (not exists_result) == forall_neg_result
    
    print(f"\nNegation verification for {pred_name}:")
    print(f"  ∀x P(x) = {forall_result}")
    print(f"  ∃x ¬P(x) = {exists_neg_result}")
    print(f"  Law 1 [¬∀ ≡ ∃¬]: {'HOLDS' if law1_holds else 'FAILS'}")
    print(f"  ∃x P(x) = {exists_result}")
    print(f"  ∀x ¬P(x) = {forall_neg_result}")
    print(f"  Law 2 [¬∃ ≡ ∀¬]: {'HOLDS' if law2_holds else 'FAILS'}")
    
    return law1_holds and law2_holds
```

**Task:** Run on 5 different predicates over domain = range(-5, 6). All should verify that both laws hold. If any fail, there is a bug in the implementation.

```python
D = list(range(-5, 6))

predicates = [
    (lambda x: x > 0, "x > 0"),
    (lambda x: x**2 < 10, "x² < 10"),
    (lambda x: x % 2 == 0, "x is even"),
    (lambda x: x == 0, "x = 0"),
    (lambda x: True, "always True"),
]

for pred, name in predicates:
    verify_quantifier_negation(D, pred, name)
```

---

### Exercise 2.5 — Combining with Lab 0 Tools

Recall from Lab 0 that ∀ is a generalized ∧ and ∃ is a generalized ∨. Verify this computationally:

```python
from functools import reduce

def forall_as_and(domain, predicate):
    """Computes ∀x P(x) by reducing with AND."""
    return reduce(lambda acc, x: acc and predicate(x), domain, True)

def exists_as_or(domain, predicate):
    """Computes ∃x P(x) by reducing with OR."""
    return reduce(lambda acc, x: acc or predicate(x), domain, False)

# Verify these match forall() and exists() from Exercise 2.1
D = list(range(1, 8))
pred = lambda x: x**2 < 20

result_forall, _ = forall(D, pred)
result_forall_and = forall_as_and(D, pred)
result_exists, _ = exists(D, pred)
result_exists_or = exists_as_or(D, pred)

print(f"forall matches forall_as_and: {result_forall == result_forall_and}")
print(f"exists matches exists_as_or:  {result_exists == result_exists_or}")
```

**Extension:** What happens with an empty domain `D = []`? What do `forall_as_and` and `exists_as_or` return? Do these match the expected vacuous truth values?

---

## Section 3 — Reflection (10 min)

Answer in your lab notebook:

1. What is the key difference between ∀x ∃y P(x,y) and ∃y ∀x P(x,y)? Give a real-world (non-math) example that illustrates why the order matters.

2. In Exercise 2.3, for the predicate "x + y = 7" over {1,…,7}: ∀x ∃y was true but ∃x ∀y was false. Explain in your own words why.

3. The function `forall_as_and` with an empty domain returns `True`. Is this a bug or a feature? Relate to the concept of vacuous truth.

---

## Checkoff Criteria

Show your TA:

- [ ] Exercise 1.1: at least 6 of 8 statements evaluated correctly with justification
- [ ] Exercise 1.2: division table filled, questions (a)–(e) answered
- [ ] Exercise 1.3: at least 3 of 4 negations correctly simplified
- [ ] `predicate_tools.py` running: demonstrate `quantifier_comparison` on one predicate
- [ ] Exercise 2.4: all five negation verifications passing
- [ ] Reflection question 1 answered

---

*Save `predicate_tools.py` — it will be extended in Lab 2.*
