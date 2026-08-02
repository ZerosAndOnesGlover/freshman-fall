# MATH 151 · Week 1
## LAB1 Solutions — INSTRUCTOR ONLY

---

## Section 1 Solutions

### Exercise 1.1 — Evaluating over D = {1,2,3,4,5,6}

E = {2,4,6}, O = {1,3,5}, P = {2,3,5}

**(a)** ∀x ∈ D, (E(x) ∨ O(x)): **TRUE.**
Every integer in {1,…,6} is either even or odd. These are exhaustive and mutually exclusive.

**(b)** ∀x ∈ D, (E(x) ∧ O(x)): **FALSE.**
Counterexample: x=1. E(1)=F, so E(1)∧O(1)=F∧T=F.

**(c)** ∃x ∈ D, (P(x) ∧ E(x)): **TRUE.**
Witness: x=2. P(2)=T (2 is prime), E(2)=T (2 is even). ✓

**(d)** ∀x ∈ D, (P(x) → O(x)): **FALSE.**
Counterexample: **x = 2**. P(2) = T (2 is prime) but O(2) = F (2 is even), so the implication
P(2) → O(2) = T → F = **F**, and a single false instance defeats a universal claim.

*Note:* 2 is the only even prime, so it is the sole counterexample in D — which is exactly why
"all primes are odd" is such a durable student error. Require the counterexample to be named; an
answer of "FALSE" with no witness earns no marks.

*(Note for graders: if students say TRUE, they forgot that 2 is an even prime.)*

**(e)** ∃x ∈ D, ∀y ∈ D, G(x,y) (x > y for all y in D): **FALSE.**
Any x would need to be > every element of D including itself and elements larger than it. No such x exists.
Explicit check: x=6 is largest. Is 6 > 6? No.

**(f)** ∀x ∈ D, ∃y ∈ D, G(x,y) (for each x, some y in D with x > y): **FALSE.**
Counterexample: x=1. Is there y ∈ {1,2,3,4,5,6} with 1 > y? No — 1 is the smallest.
*(Note: would be TRUE if the domain were {1,…,6} and we needed y ≠ x, but not here.)*

**(g)** ∀x ∈ D, ∀y ∈ D, (D(x,y) → D(x, y+x)):
If x | y then x | (y+x)?
Proof: if y = kx, then y+x = kx+x = (k+1)x, so x | (y+x). **TRUE.**

**(h)** ∃x ∈ D, ∃y ∈ D, (x≠y ∧ x²=y):
Need x²=y where x,y ∈ {1,…,6} and x≠y.
x=1: 1²=1=y, but x=y=1. ✗
x=2: 2²=4. y=4 ∈ D, x≠y. ✓ **TRUE.** Witness: (x,y) = (2,4).

---

### Exercise 1.2 — Divisibility table (x divides y)

|   | y=1 | y=2 | y=3 | y=4 | y=5 | y=6 | y=7 | y=8 | y=9 | y=10 |
|---|---|---|---|---|---|---|---|---|---|---|
| x=1 | T | T | T | T | T | T | T | T | T | T |
| x=2 | F | T | F | T | F | T | F | T | F | T |
| x=3 | F | F | T | F | F | T | F | F | T | F |
| x=4 | F | F | F | T | F | F | F | T | F | F |
| x=5 | F | F | F | F | T | F | F | F | F | T |

**(a)** ∀x ∈ D, ∃y ∈ D, P(x,y) (for each x, some y in {1..10} that x divides):
- x=1: y=1 ✓; x=2: y=2 ✓; x=3: y=3 ✓; x=4: y=4 ✓; x=5: y=5 ✓
**TRUE.** Each x divides itself (and x ≤ 10, so x ∈ D).

**(b)** ∃y ∈ D, ∀x ∈ {1,2,3,4,5}, P(x,y) (some y divisible by all of 1,2,3,4,5):
LCM(1,2,3,4,5) = 60. But 60 > 10. Scan columns: no column has all T for x=1..5.
- y=6: D(3,6)=T, D(2,6)=T, but D(4,6)=F, D(5,6)=F. ✗
- y=10: D(2,10)=T, D(5,10)=T, but D(3,10)=F, D(4,10)=F. ✗
**FALSE.** No y ∈ {1..10} is divisible by all of {1,2,3,4,5}.

**(c)** Not equivalent. (a) is TRUE, (b) is FALSE. This demonstrates ∀∃ ≠ ∃∀.

**(d)** Witnesses for (a): for x=1, any y works (take y=1); for x=2, take y=2; for x=3, take y=3; for x=4, take y=4; for x=5, take y=5. Yes, the witness y depends on x — specifically y=x works (x divides x).

**(e)** (b) is FALSE, so there is no witness. If it were TRUE, the witness y would be the same for every x simultaneously — one fixed column with all T for rows 1–5.

---

### Exercise 1.3 — Negation Practice (Domain: ℤ)

**(a)** ∀x, ∃y, (y = x + 1)
Negation: ∃x, ∀y, (y ≠ x + 1)
Original: **TRUE** (given x, take y = x+1). Negation: **FALSE.**

**(b)** ∃x, ∀y, (x · y = y) — i.e., x is the multiplicative identity
Negation: ∀x, ∃y, (x · y ≠ y)
Original: **TRUE** (witness: x=1, since 1·y=y for all y). Negation: **FALSE.**

**(c)** ∀x, ∀y, (x < y → x² < y²)
Negation: ∃x, ∃y, (x < y ∧ x² ≥ y²)
Original: **FALSE.** Counterexample: x=−3, y=1. −3 < 1, but (−3)²=9 ≥ 1²=1. ✗
Negation: **TRUE.** Witness: (x,y) = (−3, 1).

**(d)** ∃x, ∃y, (x² + y² = 3)
Negation: ∀x, ∀y, (x² + y² ≠ 3)
Over ℤ: x²+y²=3 requires e.g. x=1,y=? → 1+y²=3 → y²=2 → y=√2∉ℤ. x=0: y²=3→no. No integer solution. Original: **FALSE.** Negation: **TRUE.**

---

### Exercise 1.4 — Translation

**(a)** "Every email address belongs to at most one user account."
Domain: email addresses, user accounts. B(e,u) = "email e belongs to account u."
∀e ∀u₁ ∀u₂ ((B(e,u₁) ∧ B(e,u₂)) → u₁=u₂)
Alternative English: "If two accounts share an email address, they are the same account."

**(b)** "There exists a password that no user has chosen."
Domain: passwords, users. C(u,p) = "user u has chosen password p."
∃p ∀u ¬C(u,p)
Alternative English: "Some password has been chosen by nobody."

**(c)** "For every bug, there exists a developer who can fix it."
Domain: bugs, developers. Fix(d,b) = "developer d can fix bug b."
∀b ∃d Fix(d,b)
Alternative English: "No bug is beyond all developers' ability to fix."

**(d)** "Some feature is requested by every user."
Domain: features, users. R(u,f) = "user u requests feature f."
∃f ∀u R(u,f)
Alternative English: "There is a universally requested feature."

**(e)** "No test case passes on an incorrect implementation."
Domain: test cases, implementations. Pass(t,i) = "test t passes on implementation i", Correct(i) = "i is correct."
∀t ∀i (Pass(t,i) → Correct(i))
Equivalently: ∀t ∀i (¬Correct(i) → ¬Pass(t,i))
Alternative English: "Every test that passes on any implementation, that implementation is correct."

---

## Section 2 — Python Expected Outputs

### Exercise 2.1

```
∀x x²≥0: TRUE over domain of size 21
∀x x²>0: FALSE. Counterexample: x = 0
∃x x²=4: TRUE. Witness: x = -2   (or 2, depending on iteration order)
∃x x²=3: FALSE. No witness found in domain.
```

### Exercise 2.2 — Divisibility over D = range(1,11)

```
∀x ∀y D(x,y): FALSE  (evidence: first (x,y) where x doesn't divide y, e.g., (2,1))
∀x ∃y D(x,y): TRUE   (each x divides itself)
∃x ∀y D(x,y): TRUE   (evidence: x=1, since 1 divides everything)
∃x ∃y D(x,y): TRUE   (evidence: e.g., (1,1))
```

Interpretations:
- ∀x ∀y: Not every integer divides every other. (2 does not divide 1.)
- ∀x ∃y: Every integer divides at least one element of {1..10} — namely itself.
- ∃x ∀y: x=1 divides every integer. 1 is the universal divisor.
- ∃x ∃y: Trivially, some divisibility holds (1|1).

### Exercise 2.3 — Quantifier comparison

**P(x,y) = "x < y" over D = {1..7}:**
- ∀x ∀y: FALSE (e.g., x=3, y=2: 3<2 false)
- ∀x ∃y: **FALSE**. The natural choice y = x+1 works for every x **except x = 7**, where no
  y ∈ {1..7} satisfies 7 < y. Counterexample: **x = 7**. (The statement would be true over an
  unbounded domain such as ℕ — the failure is caused by D having a largest element.)
- ∃x ∀y: FALSE (no x smaller than all y in D including itself)
- ∃x ∃y: TRUE (e.g., x=1, y=2)

**P(x,y) = "x + y = 7" over D = {1..7}:**
- ∀x ∀y: FALSE (1+1=2≠7)
- ∀x ∃y: TRUE for x∈{1..6} (y=7−x∈D). But x=7: need y=0∉D. **FALSE.**
- ∃x ∀y: FALSE (no fixed x makes x+y=7 for all y)
- ∃x ∃y: TRUE (x=3, y=4)

**P(x,y) = "x*y = x" over D = {1..7}:**
x*y=x iff x(y−1)=0 iff x=0 (not in D) or y=1.
- ∀x ∀y: FALSE (x=2, y=2: 4≠2)
- ∀x ∃y: TRUE — for every x, take y=1: x·1=x ✓. **TRUE.**
- ∃x ∀y: FALSE — would need x·y=x for all y, i.e., x=0 for all y≠1. Not possible with x∈{1..7}.
- ∃x ∃y: TRUE (x=3, y=1)

Pattern: ∃∀ being False while ∀∃ is True confirms the expected implication holds in the correct direction only.

### Exercise 2.4 — Negation verifier

All 5 predicates should produce:
```
Law 1 [¬∀ ≡ ∃¬]: HOLDS
Law 2 [¬∃ ≡ ∀¬]: HOLDS
```
If any FAIL, there is a bug in the forall/exists implementation.

### Exercise 2.5 — Empty domain

`forall_as_and([], pred)` returns `True` (vacuous universal — the reduce starts with True and never updates it).
`exists_as_or([], pred)` returns `False` (no witness exists — reduce starts with False and never updates it).

These match the expected vacuous truth values:
- ∀x∈∅, P(x) = TRUE (vacuously)
- ∃x∈∅, P(x) = FALSE (no witness possible)

This is a feature, not a bug. Python's `all([])` and `any([])` exhibit the same behavior for the same mathematical reason.
