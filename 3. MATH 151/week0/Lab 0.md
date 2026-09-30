---
assessment: Lab 0
course: MATH 151
component: Labs
possible: 100
score: 100
status: graded
started: 2026-09-30
submitted: 2026-09-30
graded: 2026-09-30
source: "LAB 0 Truth Table Explorer.md"
---

# MATH 151 · Lab 0
## Answer Sheet

**Assessment:** `LAB 0 Truth Table Explorer.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Answer

### Section 1 — Warm-up: Hand Calculations

All 3-variable tables use the standard order: p = TTTTFFFF, q = TTFFTTFF, r = TFTFTFTF.

#### Exercise 1.1 — Systematic Column Construction

**Question 1.1(a).** p ∧ (q ∨ ¬r)

**Answer.**

| p | q | r | ¬r | q ∨ ¬r | p ∧ (q ∨ ¬r) |
|---|---|---|---|---|---|
| T | T | T | F | T | **T** |
| T | T | F | T | T | **T** |
| T | F | T | F | F | **F** |
| T | F | F | T | T | **T** |
| F | T | T | F | T | **F** |
| F | T | F | T | T | **F** |
| F | F | T | F | F | **F** |
| F | F | F | T | T | **F** |

It is true in 3 of the 8 rows, so it is a contingency. The bottom half is all F because p = F makes the ∧ false no matter what the other column says.

**Question 1.1(b).** (p ∨ q) → (q ∨ r)

**Answer.**

| p | q | r | p ∨ q | q ∨ r | (p ∨ q) → (q ∨ r) |
|---|---|---|---|---|---|
| T | T | T | T | T | **T** |
| T | T | F | T | T | **T** |
| T | F | T | T | T | **T** |
| T | F | F | T | F | **F** |
| F | T | T | T | T | **T** |
| F | T | F | T | T | **T** |
| F | F | T | F | T | **T** |
| F | F | F | F | F | **T** |

It is a contingency, false only in the row p = T, q = F, r = F. That is the only row where the hypothesis is true (p makes p ∨ q true) and the conclusion is false (neither q nor r).

#### Exercise 1.2 — Equivalence Detection

**Question 1.2(a).** Are p → (q → r) and (p ∧ q) → r equivalent?

**Answer.** **Yes, equivalent.** The two result columns match in all 8 rows:

| p | q | r | q → r | **p → (q → r)** | p ∧ q | **(p ∧ q) → r** |
|---|---|---|---|---|---|---|
| T | T | T | T | **T** | T | **T** |
| T | T | F | F | **F** | T | **F** |
| T | F | T | T | **T** | F | **T** |
| T | F | F | T | **T** | F | **T** |
| F | T | T | T | **T** | F | **T** |
| F | T | F | F | **T** | F | **T** |
| F | F | T | T | **T** | F | **T** |
| F | F | F | T | **T** | F | **T** |

Law: this is the **Exportation law**. It follows from the other laws:

```
p → (q → r)
≡ ¬p ∨ (¬q ∨ r)        Conditional Elimination (twice)
≡ (¬p ∨ ¬q) ∨ r        Associativity
≡ ¬(p ∧ q) ∨ r         De Morgan's Law
≡ (p ∧ q) → r          Conditional Elimination
```

(In programming this is currying: a function a → (b → c) carries the same information as a function (a, b) → c.)

**Question 1.2(b).** Are (p ∨ q) → r and (p → r) ∧ (q → r) equivalent?

**Answer.** **Yes, equivalent.** The two result columns match in all 8 rows:

| p | q | r | p ∨ q | **(p ∨ q) → r** | p → r | q → r | **(p → r) ∧ (q → r)** |
|---|---|---|---|---|---|---|---|
| T | T | T | T | **T** | T | T | **T** |
| T | T | F | T | **F** | F | F | **F** |
| T | F | T | T | **T** | T | T | **T** |
| T | F | F | T | **F** | F | T | **F** |
| F | T | T | T | **T** | T | T | **T** |
| F | T | F | T | **F** | T | F | **F** |
| F | F | T | F | **T** | T | T | **T** |
| F | F | F | F | **T** | T | T | **T** |

Laws:

```
(p ∨ q) → r
≡ ¬(p ∨ q) ∨ r              Conditional Elimination
≡ (¬p ∧ ¬q) ∨ r             De Morgan's Law
≡ (¬p ∨ r) ∧ (¬q ∨ r)       Distributivity (with Commutativity)
≡ (p → r) ∧ (q → r)         Conditional Elimination (twice)
```

This is **proof by cases**: to show r follows from "p or q", show that r follows from each case separately.

#### Exercise 1.3 — Tautology Hunting

**Question 1.3(a).** (p → q) → (¬q → ¬p)

**Answer.** **Tautology.**

| p | q | p → q | ¬q | ¬p | ¬q → ¬p | (p → q) → (¬q → ¬p) |
|---|---|---|---|---|---|---|
| T | T | T | F | F | T | **T** |
| T | F | F | T | F | F | **T** |
| F | T | T | F | T | T | **T** |
| F | F | T | T | T | T | **T** |

Rule: **Contraposition.** If "p implies q" holds, then "not q implies not p" holds. The columns for p → q and ¬q → ¬p are identical, so the implication between them can never go from T to F. Combined with the fact ¬q, this gives **modus tollens**: from p → q and ¬q, conclude ¬p.

**Question 1.3(b).** (p ∧ (p → q)) → q

**Answer.** **Tautology.**

| p | q | p → q | p ∧ (p → q) | (p ∧ (p → q)) → q |
|---|---|---|---|---|
| T | T | T | T | **T** |
| T | F | F | F | **T** |
| F | T | T | F | **T** |
| F | F | T | F | **T** |

Rule: **Modus ponens.** If p is true and p implies q, then q is true. The hypothesis p ∧ (p → q) is true only in row 1, and q is true there too, so the implication is never T → F.

---

### Section 2 — Logic in the Wild

#### Exercise 2.1 — Decoding Code Conditions

**Question 2.1(a).** `if not (x > 0 and y > 0):` with p = "x > 0", q = "y > 0"

**Answer.**
- Formula: ¬(p ∧ q)
- Simplified: **¬p ∨ ¬q** (De Morgan's Law), i.e. `x <= 0 or y <= 0`.
- English: the branch runs when **x is not positive or y is not positive** (or both). This is exactly what the message "at least one non-positive" says.

**Question 2.1(b).** `if (!connected || (connected && !authenticated))` with p = "connected", q = "authenticated"

**Answer.**
- Formula: ¬p ∨ (p ∧ ¬q)
- Simplification:

```
¬p ∨ (p ∧ ¬q)
≡ (¬p ∨ p) ∧ (¬p ∨ ¬q)      Distributivity
≡ T ∧ (¬p ∨ ¬q)             Complement Law (Excluded Middle), with Commutativity
≡ ¬p ∨ ¬q                   Identity Law
≡ ¬(p ∧ q)                  De Morgan's Law
```

- Simplified condition: **`!connected || !authenticated`**, or equivalently `!(connected && authenticated)`.
- English: **access is denied unless the user is both connected and authenticated.**
- The surprise: the inner `connected &&` check is redundant. The right-hand side of `||` is only evaluated when the left side is false, which means `connected` is already true there. Testing it again adds nothing.

**Question 2.1(c).** `if (!(a == b) || !(b == c))` with p = "a == b", q = "b == c"

**Answer.**
- Formula: ¬p ∨ ¬q
- Simplified: **¬(p ∧ q)** (De Morgan's Law), i.e. `!(a == b && b == c)`. Equivalently, without the outer negation: `a != b || b != c`.
- English: the branch runs when **a, b and c are not all equal**. If a == b and b == c then a == c by transitivity, so p ∧ q means "all three are equal", and the condition is its negation. That matches the comment `// not all equal`.

#### Exercise 2.2 — Logic Gates as Connectives

**Question 2.2(a).** Compute the output for A = 1, B = 0, C = 1.

**Answer.**

| Gate | Expression | Value |
|---|---|---|
| 1 | X = A AND B = 1 ∧ 0 | 0 |
| 2 | Y = NOT X = ¬0 | 1 |
| 3 | Z = Y OR C = 1 ∨ 1 | 1 |
| 4 | Output = Z AND (NOT C) = 1 ∧ ¬1 = 1 ∧ 0 | **0** |

**Output = 0.**

**Question 2.2(b).** Write the output as a propositional formula in A, B, C.

**Answer.** Substitute each gate into the next:

**Output = (¬(A ∧ B) ∨ C) ∧ ¬C**

**Question 2.2(c).** Simplify using logical laws.

**Answer.**

```
(¬(A ∧ B) ∨ C) ∧ ¬C
≡ (¬(A ∧ B) ∧ ¬C) ∨ (C ∧ ¬C)     Distributivity (with Commutativity)
≡ (¬(A ∧ B) ∧ ¬C) ∨ F            Complement Law (Non-Contradiction)
≡ ¬(A ∧ B) ∧ ¬C                  Identity Law
≡ (¬A ∨ ¬B) ∧ ¬C                 De Morgan's Law
```

**Simplest form: ¬(A ∧ B) ∧ ¬C**, equivalently **¬((A ∧ B) ∨ C)** by De Morgan's Law. In gates this is one NAND and one NOT feeding an AND, or a single NOR of (A AND B) with C. The C inside Gate 3 was pointless: Gate 4 forces C = 0 anyway. Check with the inputs from (a): ¬C = ¬1 = 0, so the output is 0, which matches.

---

### Section 3 — Truth Tables in the Python REPL

#### Exercise 3.1 — One Row at a Time

**Answer.** I set p and q to each of the four combinations and evaluated `(not p) or q`:

```python
>>> p = True;  q = True;  (not p) or q
True
>>> p = True;  q = False; (not p) or q
False
>>> p = False; q = True;  (not p) or q
True
>>> p = False; q = False; (not p) or q
True
```

| p | q | `(not p) or q` = p → q |
|---|---|---|
| T | T | T |
| T | F | F |
| F | T | T |
| F | F | T |

This matches the lecture's table for p → q. It is false only when p = T and q = F.

#### Exercise 3.2 — Checking an Equivalence

**Answer.** `(not (p and q)) == ((not p) or (not q))` for each row:

| p | q | result |
|---|---|---|
| True | True | `True` |
| True | False | `True` |
| False | True | `True` |
| False | False | `True` |

All four results are `True`. In Lecture 2's language: the biconditional ¬(p ∧ q) ↔ (¬p ∨ ¬q) is a **tautology** (true in every row), so ¬(p ∧ q) and ¬p ∨ ¬q are **logically equivalent**: ¬(p ∧ q) ≡ ¬p ∨ ¬q. That is De Morgan's Law. Python's `==` on booleans behaves exactly like ↔.

#### Exercise 3.3 — Finding a Counterexample

**Answer.** `((not p) or q) == ((not q) or p)` for each row:

| p | q | p → q | q → p | result |
|---|---|---|---|---|
| True | True | T | T | `True` |
| True | False | F | T | **`False`** |
| False | True | T | F | **`False`** |
| False | False | T | T | `True` |

Two rows give `False`, so p → q is **not** equivalent to its converse q → p. Take the row **p = False, q = True** as the counterexample.

In English, with p = "It is raining" and q = "The ground is wet": suppose it is **not raining, but the ground is wet** (a sprinkler was on). Then "If it is raining, the ground is wet" is still true, because its hypothesis is false, so it cannot be broken. But "If the ground is wet, it is raining" is false: the ground is wet and it is not raining. One statement is true and the other false in the same situation, so they cannot be equivalent. (The row p = True, q = False works the same way in reverse: it is raining but the ground stays dry, for example under a roof. Now the original fails and the converse holds.)

---

### Section 4 — Reflection

**Question 1.** What was the most surprising result?

**Answer.** Exercise 2.1(b). The condition `!connected || (connected && !authenticated)` looks like it handles two separate cases. It collapses to `!connected || !authenticated`, because the second `connected` test can only run when `connected` is already true. Real code often contains redundant checks like this, and the laws find them mechanically. A close second was Exercise 2.2: the output does not depend on Gate 3's C input at all.

**Question 2.** How do propositional logic and Python's boolean operations relate?

**Answer.** Python's `and`, `or` and `not` compute exactly ∧, ∨ and ¬ on `True`/`False`, and `==` on booleans is ↔. So evaluating an expression for one choice of values computes one row of that formula's truth table.

**Question 3.** How long are 2³² and 2⁶⁴ rows at 10⁹ rows per second?

**Answer.**

```python
>>> 2 ** 32
4294967296
>>> 2 ** 32 / 10 ** 9
4.294967296
>>> 2 ** 64
18446744073709551616
>>> 2 ** 64 / 10 ** 9
18446744073.709553
```

- n = 32: about **4.3 seconds**. That is fine.
- n = 64: about **1.84 × 10¹⁰ seconds**, which is roughly **585 years** (18446744073.7 / (3600 · 24 · 365.25) ≈ 584.5).

Adding 32 variables multiplies the work by 2³² ≈ 4.3 billion. Truth tables are therefore only practical for small n. Real tools for large formulas (SAT solvers, working on CNF) avoid listing every row. They do not escape the exponential worst case, since SAT is NP-complete.

*Marks: 100 / 100*

---

## Grading Summary

|             |                          |
| ----------- | ------------------------ |
| **Score**   | **100 / 100**            |
| **Percent** | 100%                     |
| **Graded**  | 2026-09-30               |

**Feedback:**

Full marks. Every table, every simplification and every REPL line in this lab is correct,
and the four checkoff items on the handout are all satisfied. No deductions.

| Section | Marks | |
|---|---|---|
| 1 · Hand Calculations | 35 / 35 | 1.1, 1.2 and 1.3 all built in the mandated column order, with every intermediate column shown. |
| 2 · Logic in the Wild | 30 / 30 | 2.1(a)–(c) simplified and explained in English; 2.2 traced gate by gate, then written as a formula, then simplified. |
| 3 · Python REPL | 25 / 25 | 3.1's four rows match the lecture table; 3.2 gives four `True`; 3.3 finds the counterexample and explains it. |
| 4 · Reflection | 10 / 10 | All three questions answered, the third with the arithmetic carried out. |

**The transcripts are genuine, not reconstructed.** All twelve REPL outputs were re-run
under Python 3 and reproduce exactly — `(not p) or q` over the four rows, the four `True`
from 3.2, the `False, False, True` pattern from 3.3, and the size figures
`4294967296`, `4.294967296`, `18446744073709551616`, `18446744073.709553`. The year figure
in Q3 checks too: 18446744073.71 s ÷ 31 557 600 s/yr = 584.5, so "roughly 585 years" is
right. Separately, all Section 1 columns were recomputed: 1.1(a) TTFTFFFF, 1.1(b) TTTFTTTT
(false only at p = T, q = F, r = F, as stated), 1.2(a) TFTTTTTT on both sides, 1.2(b)
TFTFTFTT on both sides, 1.3(a) TFTT, 1.3(b) TTTT. The simplifications in 2.1(b) and 2.2(c)
were checked in all eight rows and are equivalent to the originals.

**The two results the lab was built to produce both landed.** Exercise 2.1(b) is the one the
handout flags as surprising — `!connected || (connected && !authenticated)` collapses to
`!connected || !authenticated` — and the answer goes further than the simplification: it
explains the redundancy through short-circuit evaluation, that the right operand is only ever
reached when `connected` is already true. That is the real reason, and it is the kind of
observation that transfers to reading other people's code. Reflection Q1 then names this as
the most surprising result of the session, which is the right pick over the gate result in
2.2. 3.3 is handled the way the handout wants, with p = False, q = True as the
counterexample and the sprinkler story making the asymmetry concrete: "not raining, ground
wet" satisfies p → q vacuously while falsifying q → p.

**Two notes, neither charged.** The aside in 1.3(a) is loose — the tautology is
contraposition, and modus tollens needs the two premises (p → q and ¬q), not the tautology
alone, so the sentence compresses two different things. And 1.2(a) and 1.2(b) are given by
law *and* checked by table; the tables are the requirement, the derivations are the bonus.

**On the denominators.** The sheet as generated carries a single `/ 100` line for the whole
lab, since the handout carries no per-exercise point values. The 35 / 30 / 25 / 10 split
above is mine, set from the session's own time budget (30 / 30 / 30 / 5 min); the total is
the 100 recorded in the frontmatter. Separately, the handout grades this lab on completion
and effort at TA checkoff rather than on points, so read this as calibration against the
handout's criteria rather than as credit entering the final grade.

*Graded against `LAB 0 Truth Table Explorer.md`; REPL values re-run, all tables re-derived.*

