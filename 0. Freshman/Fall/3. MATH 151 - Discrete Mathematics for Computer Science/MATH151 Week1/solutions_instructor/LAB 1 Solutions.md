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

## Section 2 — Quantifiers in the REPL

**2.1.** (a) `True`: x² ≥ x for every positive integer. (b) `1**2 == 9 or 2**2 == 9 or 3**2 == 9 or 4**2 == 9 or 5**2 == 9`
is `True` (x = 3). (c) `1 % 2 == 1 and 2 % 2 == 1 and ...` is `False`; evaluation stops at x = 2, the counterexample.

**2.2.** (a) `True`: x = 1 takes y = 3, x = 2 takes y = 2, x = 3 takes y = 1. (b)
`(1+1 == 4 and 2+1 == 4 and 3+1 == 4) or (1+2 == 4 and 2+2 == 4 and 3+2 == 4) or (1+3 == 4 and 2+3 == 4 and 3+3 == 4)`
is `False`: no single y works for every x. (c) In ∀x ∃y the y may be chosen **after** x, so it may depend on x; in
∃y ∀x one y must be fixed first and work for all x.

**2.3.** Both print `True`. De Morgan's law ¬(A ∧ B ∧ C) ≡ ¬A ∨ ¬B ∨ ¬C (Lecture 02) is exactly ¬∀ ≡ ∃¬ written out.

*(Revised 2026-09-26: Section 2 is now a REPL exercise. The lab no longer asks Exercise 1.1(b), (d), (g), (h),
1.2(d)–(e), 1.3(b), (d), or 1.4(a)–(b); their answers above can be ignored. Lab 1.1(a)–(d) are old (a), (c), (e), (f);
lab 1.3(b) is old (c); lab 1.4(a)–(c) are old (c)–(e).)*

