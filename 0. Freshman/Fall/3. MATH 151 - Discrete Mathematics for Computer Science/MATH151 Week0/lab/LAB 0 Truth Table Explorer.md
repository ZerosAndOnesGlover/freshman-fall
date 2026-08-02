# MATH 151 · Discrete Mathematics for Computer Science
## Lab 0 Truth Table Explorer: Logic by Hand and by Machine
### Wednesday, Week 0 | Duration: 2 hours

---

**Lab Objectives:**
By the end of this lab, you will be able to:
1. Build systematic truth tables for formulas with 2–4 variables
2. Identify equivalences by comparing truth table columns
3. Translate real programming conditions into propositional formulas
4. Write a small Python program to evaluate and classify propositional formulas
5. Recognize logical laws "in the wild" — in code, circuits, and database queries

**Materials needed:** Pencil, graph paper (or ruled paper), laptop with Python 3 installed.

**Grading:** Labs are graded on completion and effort, checked off by TA at end of session. Bring completed work to checkoff.

---

## Section 1 Warm-up: Hand Calculations (30 min)

Work these by hand. Show every intermediate column. Do not use a computer for this section.

### Exercise 1.1. Systematic Column Construction

For a formula with three variables p, q, r, the standard column order is:

```
p: T T T T F F F F
q: T T F F T T F F
r: T F T F T F T F
```

Use this ordering for all 3-variable tables in this lab.

**Task:** Build the complete truth table for each formula, adding all necessary intermediate columns.

**(a)** p ∧ (q ∨ ¬r)

**(b)** (p ∨ q) → (q ∨ r)

**(c)** ¬p ↔ (q ∧ r)

**(d)** (p → q) ∧ (¬r → ¬q)

---

### Exercise 1.2. Equivalence Detection

For each pair of formulas, build their truth tables side by side and determine if they are logically equivalent.

**(a)** Are p → (q → r) and (p ∧ q) → r equivalent?

**(b)** Are (p ∨ q) → r and (p → r) ∧ (q → r) equivalent?

**(c)** Are ¬p ∨ q and p → q equivalent? (You should already know this from lecture — confirm it now.)

For any equivalent pair, identify which law(s) from Lecture 0.3 explain the equivalence.

---

### Exercise 1.3. Tautology Hunting

Which of the following are tautologies? Verify by truth table.

**(a)** (p → q) → (¬q → ¬p)

**(b)** ((p → q) ∧ (q → r)) → (p → r) *(This is the **hypothetical syllogism** — modus ponens chained)*

**(c)** (p ∧ (p → q)) → q *(This is **modus ponens** — the most fundamental inference rule)*

**(d)** ((p ∨ q) ∧ ¬p) → q *(This is **disjunctive syllogism**)*

Write the name and a brief English description of the inference rule each tautology represents.

---

## Section 2 Logic in the Wild (30 min)

### Exercise 2.1. Decoding Code Conditions

Each code snippet contains a boolean condition. Translate it into propositional logic, simplify it using the laws from Lecture 0.3, and describe in plain English what condition causes the branch to execute.

**(a)**
```python
if not (x > 0 and y > 0):
    print("at least one non-positive")
```
Propositional variables: p = "x > 0", q = "y > 0"

**(b)**
```c
if (!connected || (connected && !authenticated)) {
    deny_access();
}
```
Variables: p = "connected", q = "authenticated"

Simplify the condition. The simplified form might surprise you.

**(c)**
```python
# A function's precondition check
if not (isinstance(x, int) and x >= 0 and x < len(arr)):
    raise ValueError("Index out of bounds")
```
Variables: p = "x is an integer", q = "x ≥ 0", r = "x < len(arr)"

**(d)**
```java
if (!(a == b) || !(b == c)) {
    // not all equal
}
```
Variables: p = "a == b", q = "b == c"

Apply De Morgan's to simplify. What is the simplified condition?

---

### Exercise 2.2. Database Queries as Logic

SQL WHERE clauses are propositional formulas. Rewrite each SQL condition in propositional logic, then find a logically equivalent but simpler form.

**(a)**
```sql
WHERE NOT (age >= 18 AND country = 'US')
```

**(b)**
```sql
WHERE (status = 'active' OR status = 'pending') AND NOT (status = 'active' AND verified = false)
```
Variables: p = "status = 'active'", q = "status = 'pending'", r = "verified = false"

Simplify completely. What does the resulting condition mean?

---

### Exercise 2.3. Logic Gates as Connectives

The following is a **logic circuit diagram** represented textually. Trace the output.

```
Inputs: A = 1, B = 0, C = 1

Gate 1: X = A AND B
Gate 2: Y = NOT X
Gate 3: Z = Y OR C
Gate 4: Output = Z AND (NOT C)
```

**(a)** Compute the output value step by step.

**(b)** Write the output as a propositional formula in terms of A, B, C.

**(c)** Simplify the formula using logical laws. What is the simplest equivalent expression?

**(d)** Build the full truth table (8 rows for A, B, C) for the output formula. Under what conditions is the output 1?

---

## Section 3 Python Programming (50 min)

You will build a **truth table generator and formula classifier** in Python. This cements the connection between propositional logic and computation.

### Setup

Create a file called `logic_tools.py`. You will build it incrementally.

---

### Exercise 3.1. Truth Table Generator

```python
from itertools import product

def evaluate_formula(formula_func, variable_names):
    """
    Generates and prints the truth table for a propositional formula.
    
    Args:
        formula_func: A Python function (dict -> bool)
                      Takes a dict mapping variable names to bool values.
        variable_names: List of variable name strings.
    
    Returns:
        list of (assignment_dict, result) tuples
    """
    n = len(variable_names)
    results = []
    
    # Print header
    header = " | ".join(variable_names) + " || Result"
    print(header)
    print("-" * len(header))
    
    # Enumerate all 2^n assignments
    for values in product([True, False], repeat=n):
        assignment = dict(zip(variable_names, values))
        result = formula_func(assignment)
        
        # Format row
        var_cols = " | ".join("T" if assignment[v] else "F" for v in variable_names)
        result_str = "T" if result else "F"
        print(f"{var_cols} || {result_str}")
        
        results.append((assignment, result))
    
    return results
```

**Task:** Copy this function into `logic_tools.py`. Test it by evaluating these formulas:

```python
# Test 1: p AND q
f1 = lambda e: e['p'] and e['q']
evaluate_formula(f1, ['p', 'q'])

# Test 2: p OR (NOT q)
f2 = lambda e: e['p'] or not e['q']
evaluate_formula(f2, ['p', 'q'])

# Test 3: (p AND q) OR (NOT p AND NOT q)  [this is p IFF q]
f3 = lambda e: (e['p'] and e['q']) or (not e['p'] and not e['q'])
evaluate_formula(f3, ['p', 'q'])
```

Verify that Test 3's output matches the truth table for p ↔ q from lecture.

---

### Exercise 3.2. Formula Classifier

```python
def classify_formula(formula_func, variable_names):
    """
    Classifies a propositional formula as tautology, contradiction, or contingency.
    
    Returns: 'tautology', 'contradiction', or 'contingency'
    """
    results = []
    for values in product([True, False], repeat=len(variable_names)):
        assignment = dict(zip(variable_names, values))
        results.append(formula_func(assignment))
    
    if all(results):
        return 'tautology'
    elif not any(results):
        return 'contradiction'
    else:
        return 'contingency'
```

**Task:** Add this to `logic_tools.py`. Use it to classify the following formulas. For each, also predict the classification *before* running the code.

```python
vars2 = ['p', 'q']
vars3 = ['p', 'q', 'r']

# Classify these:
formulas = [
    ("p OR NOT p",           lambda e: e['p'] or not e['p'],                              ['p']),
    ("p AND NOT p",          lambda e: e['p'] and not e['p'],                              ['p']),
    ("(p→q)→((q→r)→(p→r))", lambda e: (not e['p'] or e['q']) and               # messy but correct
                                        (not e['q'] or e['r']) and 
                                        (e['p']) and not e['r'],                            vars3),
    # Actually: the formula (p→q)→((q→r)→(p→r)) 
    # = not(not p or q) or not(not q or r) or not p or r  
    # Let's write it cleanly:
    ("hyp syllogism",        lambda e: not ((not e['p'] or e['q']) and 
                                            (not e['q'] or e['r'])) or 
                                            (not e['p'] or e['r']),                        vars3),
    ("p AND q",              lambda e: e['p'] and e['q'],                                  vars2),
]

for name, f, vs in formulas:
    result = classify_formula(f, vs)
    print(f"{name}: {result}")
```

**Note:** Writing lambdas for complex formulas is awkward. In Exercise 3.3, you will build a better approach.

---

### Exercise 3.3. Equivalence Checker

```python
def are_equivalent(formula1, formula2, variable_names):
    """
    Determines if two propositional formulas are logically equivalent.
    Returns True if they have the same truth table.
    """
    for values in product([True, False], repeat=len(variable_names)):
        assignment = dict(zip(variable_names, values))
        if formula1(assignment) != formula2(assignment):
            return False
    return True
```

**Task:** Add to `logic_tools.py`. Use it to verify:

```python
vars2 = ['p', 'q']
vars3 = ['p', 'q', 'r']

# Verify these equivalences programmatically
tests = [
    # (description, formula1, formula2, variables)
    ("p→q vs ¬p∨q",
     lambda e: not e['p'] or e['q'],
     lambda e: (not e['p']) or e['q'],
     vars2),
    
    ("De Morgan 1: ¬(p∧q) vs ¬p∨¬q",
     lambda e: not (e['p'] and e['q']),
     lambda e: (not e['p']) or (not e['q']),
     vars2),
    
    ("Converse: is p→q equiv to q→p?",
     lambda e: not e['p'] or e['q'],
     lambda e: not e['q'] or e['p'],
     vars2),
    
    ("Exportation: p→(q→r) vs (p∧q)→r",
     lambda e: not e['p'] or (not e['q'] or e['r']),
     lambda e: not (e['p'] and e['q']) or e['r'],
     vars3),
]

for desc, f1, f2, vs in tests:
    result = are_equivalent(f1, f2, vs)
    print(f"{desc}: {'EQUIVALENT' if result else 'NOT EQUIVALENT'}")
```

---

### Exercise 3.4. Counterexample Finder

A useful tool: given two formulas, find an assignment where they differ (a counterexample to their equivalence).

```python
def find_counterexample(formula1, formula2, variable_names):
    """
    If formula1 and formula2 are NOT equivalent, returns an assignment
    dict where they differ. Returns None if they are equivalent.
    """
    for values in product([True, False], repeat=len(variable_names)):
        assignment = dict(zip(variable_names, values))
        if formula1(assignment) != formula2(assignment):
            return assignment
    return None
```

**Task:** Add to `logic_tools.py`. Use it to find a counterexample showing that the converse (q → p) is not equivalent to the original (p → q).

Print the counterexample and explain it in English using the example:
- p = "It is raining"
- q = "The ground is wet"

---

### Exercise 3.5. Bringing It Together

Write a function that takes a formula and:
1. Prints its full truth table
2. Classifies it (tautology / contradiction / contingency)
3. If contingency, reports how many assignments make it true vs false

```python
def analyze_formula(formula_func, variable_names, formula_name="φ"):
    """Complete formula analysis."""
    print(f"\n{'='*50}")
    print(f"Analysis of: {formula_name}")
    print(f"{'='*50}")
    
    results = evaluate_formula(formula_func, variable_names)
    
    classification = classify_formula(formula_func, variable_names)
    print(f"\nClassification: {classification.upper()}")
    
    true_count = sum(1 for _, r in results if r)
    false_count = len(results) - true_count
    
    if classification == 'contingency':
        print(f"True in {true_count}/{len(results)} assignments")
        print(f"False in {false_count}/{len(results)} assignments")
    
    return classification
```

**Test it on:**
```python
analyze_formula(
    lambda e: not (e['p'] and e['q']) == (not e['p'] or not e['q']),
    ['p', 'q'],
    "De Morgan's Law 1 (as biconditional)"
)

analyze_formula(
    lambda e: e['p'] and not e['p'],
    ['p'],
    "p AND NOT p"
)
```

---

## Section 4 Reflection (5 min at end)

Answer these briefly in your lab notebook:

1. What was the most surprising result you observed during this lab?

2. Describe in one sentence how propositional logic and Python's boolean operations relate.

3. The `classify_formula` function requires checking 2ⁿ rows. For n = 32 (32-variable formula), how many rows is that? Is this feasible on a modern computer at 10⁹ operations/second?

---

## Checkoff Criteria

Show your TA:

- [ ] Completed hand truth tables for Section 1 (at minimum 1.1 and 1.2)
- [ ] Section 2.1 with simplified conditions
- [ ] `logic_tools.py` running — demonstrate `analyze_formula` on a tautology and a contradiction
- [ ] Exercise 3.4 counterexample printed and explained

---

*Bring `logic_tools.py` to next lab — we will extend it in Lab 1.*
