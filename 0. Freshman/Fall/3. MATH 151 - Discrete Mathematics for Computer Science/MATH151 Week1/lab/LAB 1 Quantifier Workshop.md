# MATH 151 · Discrete Mathematics for Computer Science
## Lab 1 — Quantifier Workshop: Translation, Evaluation, and Computation
### Wednesday 7 October 2026, 15:00–16:50 · Week 2 | Duration: 2 hours | Covers Week 1 (all three lectures)

---

**Lab Objectives:**
1. Translate English statements into predicate logic and back with precision
2. Evaluate quantified statements over explicit finite domains
3. Correctly negate nested quantified statements
4. Evaluate quantifiers over small domains in the Python REPL, and see the effect of quantifier order

**Materials:** pencil and paper, and the Python REPL.

*(Revised 2026-09-26: the Python section used `def`, `for` loops, lambdas and `all(... for ...)`. On 7 October
CS 101 has reached conditionals, but not loops or functions. It is now a REPL exercise in which ∀ is `and` and ∃ is
`or`. Section 1 was cut from 22 items to 12 to fit the two hours.)*

---

## Section 1 — Hand Exercises: Evaluation over Finite Domains (45 min)

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

**(b)** ∃x ∈ D, (P(x) ∧ E(x))

**(c)** ∃x ∈ D, ∀y ∈ D, G(x, y)

**(d)** ∀x ∈ D, ∃y ∈ D, G(x, y)

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

---

### Exercise 1.3 — Negation Practice

Write the negation of each statement, push ¬ all the way inward, then evaluate both the original and negation:

Domain: ℤ.

**(a)** ∀x, ∃y, (y = x + 1)

**(b)** ∀x, ∀y, (x < y → x² < y²)
*(Hint: is the original true? Try x = −3, y = 1.)*

---

### Exercise 1.4 — Translation Drill

For each, write a precise predicate logic formula AND translate it back into a different English sentence that conveys the same meaning:

**(a)** "For every bug, there exists a developer who can fix it."

**(b)** "Some feature is requested by every user."

**(c)** "No test case passes on an incorrect implementation."

---

## Section 2 — Quantifiers in the Python REPL (40 min)

Over a **finite** domain, a quantifier is just a long `and` or `or`:

- ∀x ∈ {1, 2, 3} P(x) is P(1) ∧ P(2) ∧ P(3), so in Python `P1 and P2 and P3`.
- ∃x ∈ {1, 2, 3} P(x) is P(1) ∨ P(2) ∨ P(3), so in Python `P1 or P2 or P3`.

That needs only the operators and comparisons from CS 101 Weeks 0–1. Loops, which would let the computer
write the long expression for you, come in CS 101 Week 2.

### Exercise 2.1 — One Quantifier

Domain D = {1, 2, 3, 4, 5}. For each statement, predict TRUE or FALSE, then type the expression and check.

**(a)** ∀x ∈ D, x² ≥ x:

```python
>>> 1**2 >= 1 and 2**2 >= 2 and 3**2 >= 3 and 4**2 >= 4 and 5**2 >= 5
```

**(b)** ∃x ∈ D, x² = 9. Write the expression yourself with `or`.

**(c)** ∀x ∈ D, x is odd. Write it with `%`. Python stops evaluating `and` at the first `False` (short-circuit,
CS 101 Lecture 05 §4). Which element is the counterexample?

### Exercise 2.2 — Quantifier Order

Domain {1, 2, 3}, and P(x, y) = "x + y = 4".

**(a)** ∀x ∃y P(x, y): for **each** x there must be **some** y. That is an `and` of three `or`s:

```python
>>> (1+1 == 4 or 1+2 == 4 or 1+3 == 4) and \
... (2+1 == 4 or 2+2 == 4 or 2+3 == 4) and \
... (3+1 == 4 or 3+2 == 4 or 3+3 == 4)
```

**(b)** ∃y ∀x P(x, y): write it as an `or` of three `and`s, one for each y, and evaluate it.

**(c)** One is `True` and one is `False`. Explain the difference in terms of which quantifier's choice may
depend on the other's.

### Exercise 2.3 — De Morgan for Quantifiers

¬∀x P(x) ≡ ∃x ¬P(x). Check it on D = {1, 2, 3} with P(x) = "x² > 1" by evaluating both sides:

```python
>>> not (1**2 > 1 and 2**2 > 1 and 3**2 > 1)
>>> (not 1**2 > 1) or (not 2**2 > 1) or (not 3**2 > 1)
```

Do they agree? Which law from Week 0 (Lecture 02) turns the first expression into the second?

---

## Section 3 — Reflection (10 min)

Answer in your lab notebook:

1. What is the key difference between ∀x ∃y P(x,y) and ∃y ∀x P(x,y)? Give a real-world (non-math) example that illustrates why the order matters.

2. A ∀ over a domain with **no** elements is an `and` with no terms. Why is it sensible to call that TRUE? Relate it to vacuous truth.

---

## Checkoff Criteria

Show your TA:

- [ ] Exercise 1.1: all four statements evaluated with justification
- [ ] Exercise 1.2: division table filled, questions (a)–(c) answered
- [ ] Exercise 1.3: both negations correctly simplified
- [ ] Exercise 2.2: both expressions evaluated and the difference explained
- [ ] Exercise 2.3: both sides evaluated
- [ ] Reflection question 1 answered

---

