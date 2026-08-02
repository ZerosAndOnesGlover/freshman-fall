# MATH 151 · Week 0
## LAB 0 Solutions: INSTRUCTOR ONLY
### Do not distribute to students

---

## Section 1 Solutions

### Exercise 1.1

**(a)** p ∧ (q ∨ ¬r)

| p | q | r | ¬r | q∨¬r | p∧(q∨¬r) |
|---|---|---|----|------|----------|
| T | T | T | F  | T    | **T**    |
| T | T | F | T  | T    | **T**    |
| T | F | T | F  | F    | **F**    |
| T | F | F | T  | T    | **T**    |
| F | T | T | F  | T    | **F**    |
| F | T | F | T  | T    | **F**    |
| F | F | T | F  | F    | **F**    |
| F | F | F | T  | T    | **F**    |

True in rows 1,2,4. False in 3,5,6,7,8.

**(b)** (p ∨ q) → (q ∨ r)

| p | q | r | p∨q | q∨r | (p∨q)→(q∨r) |
|---|---|---|-----|-----|-------------|
| T | T | T | T   | T   | **T**       |
| T | T | F | T   | T   | **T**       |
| T | F | T | T   | T   | **T**       |
| T | F | F | T   | F   | **F**       |
| F | T | T | T   | T   | **T**       |
| F | T | F | T   | T   | **T**       |
| F | F | T | F   | T   | **T**       |
| F | F | F | F   | F   | **T**       |

Only row 4 (p=T, q=F, r=F) is false. Contingency.

**(c)** ¬p ↔ (q ∧ r)

| p | q | r | ¬p | q∧r | ¬p↔(q∧r) |
|---|---|---|----|-----|---------|
| T | T | T | F  | T   | **F**   |
| T | T | F | F  | F   | **T**   |
| T | F | T | F  | F   | **T**   |
| T | F | F | F  | F   | **T**   |
| F | T | T | T  | T   | **T**   |
| F | T | F | T  | F   | **F**   |
| F | F | T | T  | F   | **F**   |
| F | F | F | T  | F   | **F**   |

**(d)** (p → q) ∧ (¬r → ¬q)

Note: ¬r → ¬q is the inverse of q → r, which equals the contrapositive of r → q... actually ¬r→¬q ≡ q→r (contrapositive). So this is (p→q) ∧ (q→r).

| p | q | r | p→q | ¬r | ¬q | ¬r→¬q | (p→q)∧(¬r→¬q) |
|---|---|---|-----|----|----|-------|----------------|
| T | T | T | T   | F  | F  | T     | **T**          |
| T | T | F | T   | T  | F  | F     | **F**          |
| T | F | T | F   | F  | T  | T     | **F**          |
| T | F | F | F   | T  | T  | T     | **F**          |
| F | T | T | T   | F  | F  | T     | **T**          |
| F | T | F | T   | T  | F  | F     | **F**          |
| F | F | T | T   | F  | T  | T     | **T**          |
| F | F | F | T   | T  | T  | T     | **T**          |

---

### Exercise 1.2

**(a)** p→(q→r) vs (p∧q)→r

| p | q | r | q→r | p→(q→r) | p∧q | (p∧q)→r |
|---|---|---|-----|---------|-----|---------|
| T | T | T | T   | T       | T   | T       |
| T | T | F | F   | F       | T   | F       |
| T | F | T | T   | T       | F   | T       |
| T | F | F | T   | T       | F   | T       |
| F | T | T | T   | T       | F   | T       |
| F | T | F | F   | T       | F   | T       |
| F | F | T | T   | T       | F   | T       |
| F | F | F | T   | T       | F   | T       |

Columns 5 and 7 are identical. **EQUIVALENT.** This is the Exportation Law.

**(b)** (p∨q)→r vs (p→r)∧(q→r)

| p | q | r | p∨q | (p∨q)→r | p→r | q→r | (p→r)∧(q→r) |
|---|---|---|-----|---------|-----|-----|-------------|
| T | T | T | T   | T       | T   | T   | T           |
| T | T | F | T   | F       | F   | F   | F           |
| T | F | T | T   | T       | T   | T   | T           |
| T | F | F | T   | F       | F   | T   | F           |
| F | T | T | T   | T       | T   | T   | T           |
| F | T | F | T   | F       | T   | F   | F           |
| F | F | T | F   | T       | T   | T   | T           |
| F | F | F | F   | T       | T   | T   | T           |

Columns 5 and 8 are identical. **EQUIVALENT.**

Law: this is distributivity of → over ∨ on the left: (p∨q)→r ≡ (p→r)∧(q→r). Very useful in proofs.

**(c)** ¬p∨q vs p→q: EQUIVALENT by Conditional Equivalence law. Confirmed by matching truth tables.

---

### Exercise 1.3

**(a)** (p→q)→(¬q→¬p) — Contrapositive law as a tautology.

All rows T. **TAUTOLOGY.** This is the **Law of Contrapositive**: asserts that p→q and its contrapositive are equivalent.

**(b)** ((p→q)∧(q→r))→(p→r) — All rows T. **TAUTOLOGY.**

**Hypothetical Syllogism**: if p implies q and q implies r, then p implies r. This is transitivity of implication. Direct analog of: if A⊂B and B⊂C then A⊂C.

**(c)** (p∧(p→q))→q — All rows T. **TAUTOLOGY.**

**Modus Ponens**: the most fundamental rule of inference. "p is true, and p implies q; therefore q." Every proof that uses "therefore" is using modus ponens.

**(d)** ((p∨q)∧¬p)→q — All rows T. **TAUTOLOGY.**

**Disjunctive Syllogism**: "Either p or q; not p; therefore q." Used constantly in case analysis proofs: "The value is positive, negative, or zero. It's not negative (shown). It's not zero (shown). Therefore it's positive."

---

## Section 2 Solutions

### Exercise 2.1

**(a)** `not (x > 0 and y > 0)`
= ¬(p ∧ q)
≡ ¬p ∨ ¬q   [De Morgan]
= "x ≤ 0 or y ≤ 0"

The branch executes when at least one of x, y is non-positive. The code comment "at least one non-positive" is correct.

**(b)** `!connected || (connected && !authenticated)`
= ¬p ∨ (p ∧ ¬q)
≡ (¬p ∨ p) ∧ (¬p ∨ ¬q)   [Distributivity]
≡ T ∧ (¬p ∨ ¬q)            [Excluded Middle]
≡ ¬p ∨ ¬q                   [Identity]
≡ ¬(p ∧ q)                  [De Morgan]
= "not (connected and authenticated)"

**The simplified condition:** `!(connected && authenticated)` — deny access if the user is not both connected AND authenticated. The original code has redundancy that the laws reveal.

**(c)** `not (isinstance(x, int) and x >= 0 and x < len(arr))`
= ¬(p ∧ q ∧ r)
≡ ¬p ∨ ¬q ∨ ¬r   [De Morgan, extended]
= "x is not an integer, OR x < 0, OR x ≥ len(arr)"

Raise the error if any one condition fails. This is correct index validation.

**(d)** `!(a == b) || !(b == c)`
= ¬p ∨ ¬q
≡ ¬(p ∧ q)   [De Morgan]
= "NOT (a==b AND b==c)"
= "NOT all three are equal"

So the branch executes when a, b, c are NOT all equal. The comment "not all equal" is correct. Simplified: `!(a == b && b == c)`.

---

### Exercise 2.2

**(a)** `NOT (age >= 18 AND country = 'US')`
= ¬(p ∧ q)  where p="age≥18", q="country='US'"
≡ ¬p ∨ ¬q   [De Morgan]
= "age < 18 OR country ≠ 'US'"

**(b)** `(status='active' OR status='pending') AND NOT (status='active' AND verified=false)`
= (p ∨ q) ∧ ¬(p ∧ r)  where p="active", q="pending", r="verified=false"
≡ (p ∨ q) ∧ (¬p ∨ ¬r)   [De Morgan]
≡ (p ∧ ¬r) ∨ (q ∧ ¬p) ∨ (q ∧ ¬r)   [Distribute — or use case analysis]

Simpler: case analysis:
- If p (active): need ¬r, i.e., verified=true → "active AND verified"
- If q (pending): ¬p is true (can't be both active and pending), so condition becomes q ∧ (¬p∨¬r) = q ∧ T = q → just "pending"

Result: `(status='active' AND verified=true) OR status='pending'`

This makes intuitive sense: active users must be verified; pending users are allowed regardless of verification.

---

### Exercise 2.3

**(a)** Step-by-step with A=1, B=0, C=1:
- Gate 1: X = A AND B = 1 AND 0 = **0**
- Gate 2: Y = NOT X = NOT 0 = **1**
- Gate 3: Z = Y OR C = 1 OR 1 = **1**
- Gate 4: Output = Z AND (NOT C) = 1 AND (NOT 1) = 1 AND 0 = **0**

Output = **0**

**(b)** Formula: ((¬(A∧B)) ∨ C) ∧ ¬C

**(c)** Simplify:
((¬(A∧B)) ∨ C) ∧ ¬C
≡ (¬(A∧B) ∧ ¬C) ∨ (C ∧ ¬C)   [Distributivity]
≡ (¬(A∧B) ∧ ¬C) ∨ F            [Non-Contradiction]
≡ ¬(A∧B) ∧ ¬C                   [Identity]
≡ ¬((A∧B) ∨ C)                  [De Morgan]

Simplest form: **¬((A∧B) ∨ C)** — output is 1 only when neither (A and B) nor C is true.

**(d)** Output = 1 when: NOT(A=1,B=1) AND C=0 → only when C=0 and not both A,B are 1.

True rows: (0,0,0), (0,1,0), (1,0,0). That's 3 of 8 rows.

---

## Section 3: Python Expected Outputs

### Exercise 3.1. Expected output for Test 3 (p ↔ q):

```
p | q || Result
-----------
T | T || T
T | F || F
F | T || F
F | F || T
```

Matches p↔q truth table. ✓

### Exercise 3.2. Expected classifications:

```
p OR NOT p:     tautology
p AND NOT p:    contradiction
hyp syllogism:  tautology
p AND q:        contingency
```

### Exercise 3.3. Expected equivalence results:

```
p→q vs ¬p∨q:          EQUIVALENT
De Morgan 1:            EQUIVALENT
Converse: is p→q equiv to q→p?: NOT EQUIVALENT
Exportation:            EQUIVALENT
```

### Exercise 3.4. Counterexample for converse:

Expected output: `{'p': True, 'q': False}` (or `{'p': False, 'q': True}`)

English explanation: Let p = "It is raining", q = "The ground is wet."
Assignment p=True, q=False: "It is raining" (TRUE) but "The ground is wet" (FALSE).
- p→q evaluates to: T→F = **False**
- q→p evaluates to: F→T = **True**

They differ. This is a case where rain exists but the ground is (somehow) dry — the original conditional is violated, but the converse is vacuously satisfied (wet ground isn't needed to make q→p true when q is false).

### Exercise 3.5. Expected output for De Morgan test:

```
==================================================
Analysis of: De Morgan's Law 1 (as biconditional)
==================================================
p | q || Result
-----------
T | T || T
T | F || T
F | T || T
F | F || T

Classification: TAUTOLOGY
```

For `p AND NOT p`:
```
Classification: CONTRADICTION
True in 0/2 assignments
False in 2/2 assignments
```

---

## Section 4: Reflection Model Answers

**1.** Most surprising result: typically students are surprised by Exercise 2.1(b) — that the redundant-looking condition simplifies to just `¬(p∧q)`. The redundancy is invisible without the algebraic tools.

**2.** Python's boolean operations (and, or, not) implement exactly the logical connectives ∧, ∨, ¬ over the values True/False. The truth tables are identical. The only difference: Python uses short-circuit evaluation (lazy), while the logical truth tables evaluate both operands.

**3.** 2³² = 4,294,967,296 rows ≈ 4 billion. At 10⁹ operations/second, this takes approximately 4 seconds. For n=64: 2⁶⁴ ≈ 1.8 × 10¹⁹ operations — at 10⁹ ops/sec, that's ~585 years. This is why SAT is NP-complete and why brute-force truth table enumeration is not a viable algorithm for large formulas.
