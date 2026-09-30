---
assessment: Lab 1
course: MATH 151
component: Labs
possible: 100
score: 100
status: graded
started: 2026-09-30
submitted: 2026-09-30
graded: 2026-09-30
source: "LAB 1 Quantifier Workshop.md"
---

# MATH 151 · Lab 1
## Answer Sheet

**Assessment:** `LAB 1 Quantifier Workshop.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Section 1 — Hand Exercises: Evaluation over Finite Domains

#### Exercise 1.1 — Evaluating Quantified Statements

Domain: D = {1, 2, 3, 4, 5, 6}. Evaluate each statement as TRUE or FALSE. If FALSE, exhibit a counterexample; if TRUE, explain why every element satisfies the predicate.

- E(x) = "x is even" = {2, 4, 6}
- O(x) = "x is odd" = {1, 3, 5}
- P(x) = "x is prime" = {2, 3, 5}
- G(x, y) = "x > y"
- D(x, y) = "x divides y"

**Question 1.1(a).** ∀x ∈ D, (E(x) ∨ O(x))

**Answer.** **TRUE.** Check every element:

| x | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| E(x) | F | T | F | T | F | T |
| O(x) | T | F | T | F | T | F |
| E(x) ∨ O(x) | **T** | **T** | **T** | **T** | **T** | **T** |

E and O together cover all of D ({2, 4, 6} ∪ {1, 3, 5} = D), so the disjunction holds for every x.

**Question 1.1(b).** ∃x ∈ D, (P(x) ∧ E(x))

**Answer.** **TRUE.** Witness: x = 2, which is prime (2 ∈ {2, 3, 5}) and even (2 ∈ {2, 4, 6}). It is the only witness, since P ∩ E = {2}.

**Question 1.1(c).** ∃x ∈ D, ∀y ∈ D, G(x, y)

**Answer.** **FALSE.** We need one x that is greater than *every* y in D, and that includes y = x itself. But x > x is never true, so every candidate fails at y = x. For example, the strongest candidate is x = 6, and it fails at y = 6 because 6 > 6 is false.

Negation, which is true: ∀x ∈ D, ∃y ∈ D, x ≤ y (take y = x).

**Question 1.1(d).** ∀x ∈ D, ∃y ∈ D, G(x, y)

**Answer.** **FALSE.** Counterexample: x = 1. We would need some y ∈ D with 1 > y, but the smallest element of D is 1, so there is none. (Every other x from 2 to 6 does have a smaller y, for example y = 1. The statement fails only because of x = 1, but one failure is enough.)

#### Exercise 1.2 — The Quantifier Order Experiment

Domain: D = {1, 2, …, 10}. P(x, y) = "x divides y". Fill in the table for x = 1 to 5, then answer the questions.

**Answer (table).**

|   | y=1 | y=2 | y=3 | y=4 | y=5 | y=6 | y=7 | y=8 | y=9 | y=10 |
|---|---|---|---|---|---|---|---|---|---|---|
| x=1 | T | T | T | T | T | T | T | T | T | T |
| x=2 | F | T | F | T | F | T | F | T | F | T |
| x=3 | F | F | T | F | F | T | F | F | T | F |
| x=4 | F | F | F | T | F | F | F | T | F | F |
| x=5 | F | F | F | F | T | F | F | F | F | T |

**Question 1.2(a).** Is ∀x ∈ D, ∃y ∈ D, P(x, y) true? (For each x, does some y in {1…10} exist that x divides?)

**Answer.** **TRUE.** Every row of the table contains at least one T. In particular, the diagonal entry (y = x) is always T. The same choice works for x = 6 to 10, since every x divides itself (x = 1 · x). So for each x, choose y = x.

**Question 1.2(b).** Is ∃y ∈ D, ∀x ∈ {1,2,3,4,5}, P(x, y) true? (Is there a y divisible by all of 1, 2, 3, 4, 5?)

**Answer.** **FALSE.** This needs a *column* that is all T for x = 1 to 5, and no column is:

- y = 1: fails at x = 2.
- y = 2: fails at x = 3.
- y = 3: fails at x = 2.
- y = 4: fails at x = 3.
- y = 5: fails at x = 2.
- y = 6: fails at x = 4 (and at 5).
- y = 7: fails at x = 2.
- y = 8: fails at x = 3.
- y = 9: fails at x = 2.
- y = 10: fails at x = 3 (and at 4).

A number divisible by 1, 2, 3, 4 and 5 must be a multiple of lcm(1, 2, 3, 4, 5) = 60, and 60 > 10.

**Question 1.2(c).** Are (a) and (b) equivalent? What does your table show about quantifier order?

**Answer.** **No.** (a) is true and (b) is false.
- (a), ∀x ∃y, asks: *does every row contain a T?* The y may be different for each row.
- (b), ∃y ∀x, asks: *is there a single column that is all T?* One y must work for every row at once.

A column of all T's would give a T in every row, so ∃y ∀x ⇒ ∀x ∃y always holds. The converse fails, as this table shows: every row has a T, but the T's are in different columns. Swapping ∀ and ∃ changes the meaning.

#### Exercise 1.3 — Negation Practice

Domain: ℤ. Write the negation of each statement, push ¬ all the way inward, then evaluate both the original and the negation.

**Question 1.3(a).** ∀x, ∃y, (y = x + 1)

**Answer.**
- ¬∀x ∃y (y = x + 1)
- ≡ ∃x ¬∃y (y = x + 1)  — ¬∀ ≡ ∃¬
- ≡ **∃x ∀y (y ≠ x + 1)**  — ¬∃ ≡ ∀¬

**Original: TRUE.** For any integer x, choose y = x + 1, which is an integer.
**Negation: FALSE.** No integer x has the property that x + 1 fails to exist.

**Question 1.3(b).** ∀x, ∀y, (x < y → x² < y²) *(Hint: is the original true? Try x = −3, y = 1.)*

**Answer.**
- ¬∀x ∀y (x < y → x² < y²)
- ≡ ∃x ∃y ¬(x < y → x² < y²)  — ¬∀ ≡ ∃¬, twice
- ≡ ∃x ∃y (x < y ∧ ¬(x² < y²))  — ¬(A → B) ≡ A ∧ ¬B
- ≡ **∃x ∃y (x < y ∧ x² ≥ y²)**  — ¬(a < b) ≡ a ≥ b

**Original: FALSE.** Counterexample: x = −3, y = 1. Then −3 < 1, but x² = 9 and y² = 1, so x² < y² is false. Squaring only preserves order for non-negative numbers.
**Negation: TRUE.** The same pair (x, y) = (−3, 1) is a witness.

#### Exercise 1.4 — Translation Drill

For each, write a precise predicate logic formula AND translate it back into a different English sentence that conveys the same meaning.

**Question 1.4(a).** "For every bug, there exists a developer who can fix it."

**Answer.**
- Domains: b ranges over bugs, d ranges over developers.
- Predicate: F(d, b) = "developer d can fix bug b".
- Formula: **∀b ∃d F(d, b)**
- Back to English: *"There is no bug that no developer can fix."* (This is ¬∃b ∀d ¬F(d, b), which is equivalent.)
- The developer may be different for each bug. ∃d ∀b F(d, b) would instead mean "one developer can fix every bug".

**Question 1.4(b).** "Some feature is requested by every user."

**Answer.**
- Domains: f ranges over features, u ranges over users.
- Predicate: R(u, f) = "user u requests feature f".
- Formula: **∃f ∀u R(u, f)**
- Back to English: *"There is at least one feature that appears on every single user's request list."*
- Here the ∃ comes first, so it is the *same* feature for all users. ∀u ∃f R(u, f) would be the weaker "every user requests something".

**Question 1.4(c).** "No test case passes on an incorrect implementation."

**Answer.**
- Domains: t ranges over test cases, i ranges over implementations.
- Predicates: P(t, i) = "test t passes on implementation i", C(i) = "implementation i is correct".
- Formula: **¬∃t ∃i (¬C(i) ∧ P(t, i))**
- Pushing ¬ inward gives the equivalent form ∀t ∀i (¬C(i) → ¬P(t, i)).
- Back to English: *"Every test case fails on every incorrect implementation."* Equivalently, by the contrapositive P(t, i) → C(i): *"If an implementation passes any test, it is correct."*

### Section 2 — Quantifiers in the Python REPL

Over a finite domain, ∀ is a long `and` and ∃ is a long `or`.

#### Exercise 2.1 — One Quantifier

Domain: D = {1, 2, 3, 4, 5}. For each statement, predict TRUE or FALSE, then type the expression and check.

**Question 2.1(a).** ∀x ∈ D, x² ≥ x

**Answer.** Prediction: **TRUE**, because for x ≥ 1, x² = x · x ≥ 1 · x = x.

```python
>>> 1**2 >= 1 and 2**2 >= 2 and 3**2 >= 3 and 4**2 >= 4 and 5**2 >= 5
True
```

The result matches the prediction.

**Question 2.1(b).** ∃x ∈ D, x² = 9. Write the expression yourself with `or`.

**Answer.** Prediction: **TRUE**, with witness x = 3.

```python
>>> 1**2 == 9 or 2**2 == 9 or 3**2 == 9 or 4**2 == 9 or 5**2 == 9
True
```

The result matches the prediction. `or` short-circuits at the first `True`, so evaluation stops at `3**2 == 9`, which is the witness.

**Question 2.1(c).** ∀x ∈ D, x is odd. Write it with `%`. Python stops evaluating `and` at the first `False`. Which element is the counterexample?

**Answer.** Prediction: **FALSE**, because D contains even numbers.

```python
>>> 1 % 2 == 1 and 2 % 2 == 1 and 3 % 2 == 1 and 4 % 2 == 1 and 5 % 2 == 1
False
```

The counterexample is **x = 2**. `1 % 2 == 1` is `True`, so Python moves on. `2 % 2 == 1` is `0 == 1`, which is `False`, so evaluation stops there and the rest is never checked. 4 is also even, but the short-circuit stops at the *first* counterexample.

#### Exercise 2.2 — Quantifier Order

Domain: {1, 2, 3}. P(x, y) = "x + y = 4".

**Question 2.2(a).** ∀x ∃y P(x, y): for each x there must be some y. That is an `and` of three `or`s. Evaluate it.

**Answer.**

```python
>>> (1+1 == 4 or 1+2 == 4 or 1+3 == 4) and \
... (2+1 == 4 or 2+2 == 4 or 2+3 == 4) and \
... (3+1 == 4 or 3+2 == 4 or 3+3 == 4)
True
```

Each bracket, one per x, contains a true term: x = 1 uses y = 3, x = 2 uses y = 2, and x = 3 uses y = 1.

**Question 2.2(b).** ∃y ∀x P(x, y): write it as an `or` of three `and`s, one for each y, and evaluate it.

**Answer.**

```python
>>> (1+1 == 4 and 2+1 == 4 and 3+1 == 4) or \
... (1+2 == 4 and 2+2 == 4 and 3+2 == 4) or \
... (1+3 == 4 and 2+3 == 4 and 3+3 == 4)
False
```

Each bracket fixes one y (y = 1, then 2, then 3) and asks whether it works for x = 1, 2 and 3. Every bracket is `False`. For a fixed y, only x = 4 − y satisfies x + y = 4, so no y works for all three x.

**Question 2.2(c).** One is `True` and one is `False`. Explain the difference in terms of which quantifier's choice may depend on the other's.

**Answer.**
- In **∀x ∃y**, the ∃ comes second, so the choice of y may **depend on x**. Each x gets its own partner y = 4 − x, and a different y for each x is allowed. So it is `True`.
- In **∃y ∀x**, the ∃ comes first, so y must be chosen **once, before seeing x**, and then work for every x. Since x + y = 4 pins y to 4 − x, no single y works for all three values of x. So it is `False`.

In Python terms, the outer operator is the outer quantifier. `and`-of-`or`s lets each row pick its own true term. `or`-of-`and`s needs one bracket in which every term is true.

#### Exercise 2.3 — De Morgan for Quantifiers

¬∀x P(x) ≡ ∃x ¬P(x). Check it on D = {1, 2, 3} with P(x) = "x² > 1" by evaluating both sides.

**Question 2.3.** Do they agree? Which law from Week 0 (Lecture 02) turns the first expression into the second?

**Answer.**

```python
>>> not (1**2 > 1 and 2**2 > 1 and 3**2 > 1)
True
>>> (not 1**2 > 1) or (not 2**2 > 1) or (not 3**2 > 1)
True
```

**They agree:** both are `True`. The element that makes both sides true is x = 1, since 1² = 1 is not greater than 1. So ∀x P(x) is false and its negation is true.

The law is **De Morgan's law**: ¬(A ∧ B ∧ C) ≡ ¬A ∨ ¬B ∨ ¬C. Over a finite domain, ∀ is an `and` and ∃ is an `or`, so De Morgan for quantifiers is just propositional De Morgan applied to a long conjunction.

### Section 3 — Reflection

**Question 1.** What is the key difference between ∀x ∃y P(x, y) and ∃y ∀x P(x, y)? Give a real-world (non-math) example that illustrates why the order matters.

**Answer.** In ∀x ∃y, the y may **change with x**: each x gets its own y. In ∃y ∀x, there must be **one fixed y** that works for every x at once. The second is strictly stronger. ∃y ∀x implies ∀x ∃y, but not the other way round (see Exercises 1.2 and 2.2).

*Example — locks and keys.* Let L(k, d) = "key k opens door d".
- ∀d ∃k L(k, d): "every door has a key that opens it." This is true in almost any building.
- ∃k ∀d L(k, d): "there is a master key that opens every door." This is a much stronger claim and is often false.

Both statements use the same words and quantifiers, but in a different order, and they have very different truth values.

**Question 2.** A ∀ over a domain with no elements is an `and` with no terms. Why is it sensible to call that TRUE? Relate it to vacuous truth.

**Answer.**
- **Identity element.** `True` is the identity for `and`: A ∧ T ≡ A. Splitting a domain into two parts gives ∀ over (A ∪ B) = (∀ over A) ∧ (∀ over B). If B is empty, this must still equal ∀ over A, which only works if the empty `and` is `True`. (Likewise, the empty `or` is `False`, the identity for `or`.)
- **Vacuous truth.** ∀x ∈ ∅, P(x) means ∀x (x ∈ ∅ → P(x)). The hypothesis x ∈ ∅ is false for every x, so every instance of the conditional is vacuously true, like "if the moon is cheese, then 2 + 2 = 5".
- **No counterexample.** To make a ∀ false you must produce a counterexample, meaning an element where P fails. An empty domain has no elements, so no counterexample can exist. Formally, ¬∀x ∈ ∅ P(x) ≡ ∃x ∈ ∅ ¬P(x), which is an empty `or` and therefore `False`. So the ∀ itself is `True`.

*Example:* "Every student in an empty classroom has passed" is true, because nobody in the room failed.

*Marks: 100 / 100*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | **100 / 100** |
| **Percent** | 100% |
| **Graded** | 2026-09-30 |

**Feedback:**

Every item is correct and every mark is earned. Graded against `LAB 1 Solutions.md`, using
the key's own mapping note for the 2026-09-26 revision: lab 1.1(a)–(d) are key 1.1(a), (c),
(e), (f); lab 1.3(b) is key 1.3(c); lab 1.4(a)–(c) are key 1.4(c)–(e).

| Item | Allocation | Marks |
|---|---|---|
| 1.1(a) | truth table 2 · TRUE with exhaustive-and-exclusive reason 1 | 3 / 3 |
| 1.1(b) | TRUE 1 · witness x = 2 1 · P ∩ E = {2} is the only one 1 | 3 / 3 |
| 1.1(c) | FALSE 1 · defeat via y = x 2 | 3 / 3 |
| 1.1(d) | FALSE 1 · counterexample x = 1 2 | 3 / 3 |
| 1.2 table | five rows × ten columns correct | 5 / 5 |
| 1.2(a) | TRUE 1 · y = x works, extended to x = 6…10 1 | 2 / 2 |
| 1.2(b) | FALSE 1 · all ten columns refuted 1 · lcm = 60 > 10 1 | 3 / 3 |
| 1.2(c) | not equivalent 1 · row/column reading + ∃∀ ⇒ ∀∃ 1 | 2 / 2 |
| 1.3(a) | steps to ∃∀ (y ≠ x+1) 3 · original TRUE / negation FALSE 2 | 5 / 5 |
| 1.3(b) | steps through ¬(A→B) 3 · counterexample and both truth values 3 | 6 / 6 |
| 1.4(a) | domains + predicate 1 · ∀b∃d 1 · equivalent English 2 · ∀∃ vs ∃∀ note 1 | 5 / 5 |
| 1.4(b) | domains + predicate 1 · ∃f∀u 1 · equivalent English 2 · weaker reading 1 | 5 / 5 |
| 1.4(c) | domains + predicates 1 · ¬∃∃(¬C ∧ P) 1 · pushed-inward form 1 · contrapositive + English 2 | 5 / 5 |
| 2.1(a) | prediction + reason 1 · expression 1 · result 1 | 3 / 3 |
| 2.1(b) | prediction + witness 1 · expression 1 · short-circuit noted 1 | 3 / 3 |
| 2.1(c) | prediction 1 · expression 1 · counterexample and short-circuit walkthrough 2 | 4 / 4 |
| 2.2(a) | expression 2 · True 1 · per-x witnesses 1 | 4 / 4 |
| 2.2(b) | expression 2 · False 1 · why every bracket fails 1 | 4 / 4 |
| 2.2(c) | dependency explanation 4 · outer-operator reading 2 | 6 / 6 |
| 2.3 | both sides evaluated 4 · agreement + witness x = 1 3 · De Morgan named and tied to ∀/∃ 4 | 11 / 11 |
| Reflection Q1 | ∀∃ vs ∃∀ distinction 2 · implication direction 2 · non-math example 5 | 9 / 9 |
| Reflection Q2 | identity-element argument 2 · vacuous-truth reading 2 · no-counterexample argument 2 | 6 / 6 |

**How the answers were checked.** The 1.2 table was recomputed from `y % x` for all fifty
cells — no mismatches — and the ten witnesses offered in 1.2(b) were each confirmed to be
genuine failures. lcm(1, 2, 3, 4, 5) = 60 confirms the 1.2(b) argument. All eight Section 2
expressions were executed: 2.1a `True`, 2.1b `True`, 2.1c `False`, 2.2a `True`, 2.2b `False`,
2.3a `True`, 2.3b `True` — every output in the sheet is the real output, and the two 2.3
expressions do agree as claimed. 1.4(c)'s two forms were checked to be the same formula,
since ∀t∀i(¬C(i) → ¬P(t,i)) and ∀t∀i(P(t,i) → C(i)) both reduce to ¬P(t,i) ∨ C(i); this is
the key's own answer for that item, reached by the other direction.

**Work worth noting beyond the rubric.** Three answers go further than the key. 1.2(c) does
not stop at "not equivalent" — it gives the row/column reading and then states the implication
that actually holds, ∃y∀x ⇒ ∀x∃y, together with why the converse fails (the T's sit in
different columns). 1.4(a) and 1.4(b) each volunteer the quantifier-swapped reading, and both
get its strength right: in 1.4(b), ∀u∃f is correctly called the *weaker* "every user requests
something". Section 3 Q1 uses the master-key example, which is the natural non-math
illustration of exactly this distinction.

**Best argument on the sheet.** Reflection Q2 is the strongest single piece of writing. The
key asks only why an empty `and` should be TRUE, and three independent arguments are given:
the identity-element argument (A ∧ T ≡ A forces the empty `and` to be T, and the empty `or`
to be F by the same reasoning), the vacuous-truth reading ∀x ∈ ∅ P(x) ≡ ∀x(x ∈ ∅ → P(x)),
and the formal no-counterexample argument, ¬∀x ∈ ∅ P(x) ≡ ∃x ∈ ∅ ¬P(x) being an empty `or`
and therefore False. The third closes the loop by using the very law the sheet is being tested
on, and the moon-and-cheese analogy is the right one. 2.1(c) is a close second for tracing the
short-circuit explicitly rather than just reporting `False`.

**One presentational note, not charged against the score.** 1.3(a) closes with "No integer x
has the property that x + 1 fails to exist." The negation is ∃x∀y(y ≠ x + 1), whose
falsity means no x has *every* y differing from x + 1 — not that x + 1 fails to exist. The
verdict (original TRUE, negation FALSE) and the witness y = x + 1 are both right, so nothing
turns on it, but the sentence restates the right conclusion for the wrong reason. Worth
rewording: the negation fails because y = x + 1 is a counterexample to "y ≠ x + 1" for every
x. 1.1(c) has the mirror-image habit of a correct proof under the heading "Negation, which is
true", which is accurate there and reads oddly only by contrast.

---
