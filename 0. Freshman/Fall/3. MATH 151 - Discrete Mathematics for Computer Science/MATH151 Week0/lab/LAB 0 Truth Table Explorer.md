# MATH 151 · Discrete Mathematics for Computer Science
## Lab 0 Truth Table Explorer: Logic by Hand and by Machine
### Wednesday 30 September 2026, 15:00–16:50 · Week 1 | Duration: 2 hours | Covers Week 0 (all three lectures)

---

**Lab Objectives:**
By the end of this lab, you will be able to:
1. Build systematic truth tables for formulas with 2–4 variables
2. Identify equivalences by comparing truth table columns
3. Translate real programming conditions into propositional formulas
4. Evaluate propositional formulas in the Python REPL and use it to check an equivalence
5. Recognize logical laws "in the wild" — in code, circuits, and database queries

**Materials needed:** Pencil, graph paper (or ruled paper), laptop with Python 3 installed.

**Grading:** Labs are graded on completion and effort, checked off by TA at end of session. Bring completed work to checkoff.

---

*(Revised 2026-09-26: the Python section used `itertools.product`, `def`, dictionaries, `zip` and lambdas. On
30 September CS 101 has taught only values, types, variables and the boolean operators. It is now a REPL
exercise with `and`, `or`, `not`. Sections 1 and 2 were also cut to fit the two hours.)*

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

---

### Exercise 1.2. Equivalence Detection

For each pair of formulas, build their truth tables side by side and determine if they are logically equivalent.

**(a)** Are p → (q → r) and (p ∧ q) → r equivalent?

**(b)** Are (p ∨ q) → r and (p → r) ∧ (q → r) equivalent?

For any equivalent pair, identify which law(s) from Lecture 2 explain the equivalence.

---

### Exercise 1.3. Tautology Hunting

Which of the following are tautologies? Verify by truth table.

**(a)** (p → q) → (¬q → ¬p)

**(b)** (p ∧ (p → q)) → q *(This is **modus ponens** — the most fundamental inference rule)*

Write the name and a brief English description of the inference rule each tautology represents.

---

## Section 2 Logic in the Wild (30 min)

### Exercise 2.1. Decoding Code Conditions

Each code snippet contains a boolean condition. Translate it into propositional logic, simplify it using the laws from Lecture 2, and describe in plain English what condition causes the branch to execute.

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
```java
if (!(a == b) || !(b == c)) {
    // not all equal
}
```
Variables: p = "a == b", q = "b == c"

Apply De Morgan's to simplify. What is the simplified condition?

---

### Exercise 2.2. Logic Gates as Connectives

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


---

## Section 3 Truth Tables in the Python REPL (30 min)

Python's `and`, `or` and `not` **are** ∧, ∨ and ¬ (CS 101 Lecture 03 §4). That is all the Python this
section needs: no loops, no functions — those come later in CS 101. Open the REPL with `python3`.

Python has no → operator, but you know p → q ≡ ¬p ∨ q, so type `(not p) or q`.

### Exercise 3.1. One Row at a Time

```python
>>> p = True
>>> q = False
>>> (not p) or q
False
```

That is one row of the truth table of p → q. Change `p` and `q` (use the up arrow to recall lines) and
evaluate `(not p) or q` for all four rows. Write the table down and check it against the one from lecture.

### Exercise 3.2. Checking an Equivalence

De Morgan's law says ¬(p ∧ q) ≡ ¬p ∨ ¬q. Two formulas are equivalent exactly when `==` between them is
`True` in **every** row. For each of the four rows, set `p` and `q` and evaluate:

```python
>>> (not (p and q)) == ((not p) or (not q))
```

Record the four results. What does "all four are `True`" tell you, in the language of Lecture 2?

### Exercise 3.3. Finding a Counterexample

Is p → q equivalent to its converse q → p? Evaluate, for each row:

```python
>>> ((not p) or q) == ((not q) or p)
```

Find a row where the result is `False`. That row is a **counterexample** to the equivalence. Explain it in
English with p = "It is raining" and q = "The ground is wet".

---

## Section 4 Reflection (5 min at end)

Answer these briefly in your lab notebook:

1. What was the most surprising result you observed during this lab?

2. Describe in one sentence how propositional logic and Python's boolean operations relate.

3. Checking a formula by truth table takes 2ⁿ rows. For n = 32, type `2 ** 32` into the REPL. At 10⁹ rows per second, how many seconds is that (`2 ** 32 / 10 ** 9`)? And for n = 64?

---

## Checkoff Criteria

Show your TA:

- [ ] Completed hand truth tables for Section 1 (at minimum 1.1 and 1.2)
- [ ] Section 2.1 with simplified conditions
- [ ] Exercise 3.2's four `True` results, and Exercise 3.3's counterexample explained

---

