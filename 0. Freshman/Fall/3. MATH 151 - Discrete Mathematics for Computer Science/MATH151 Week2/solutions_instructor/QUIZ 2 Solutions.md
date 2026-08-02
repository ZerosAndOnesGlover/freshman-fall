# MATH 151 — Week 2
## Quiz 2 Solutions — INSTRUCTOR ONLY

---

### Problem 1 — Truth Values (4 pts, 1 pt each)

Domain: ℤ⁺. E(x) = "x is even", P(x) = "x is prime."

**(a)** ∀x (P(x) → E(x)): **FALSE.**
Counterexample: x = 3. P(3) = T (3 is prime), E(3) = F (3 is odd). So P(3)→E(3) = T→F = F.

**(b)** ∃x (P(x) ∧ E(x)): **TRUE.**
Witness: x = 2. P(2) = T (2 is prime), E(2) = T (2 is even). ✓

**(c)** ∀x (E(x) → ¬P(x)): **FALSE.**
This says "every even number is not prime." Counterexample: x = 2. E(2) = T, ¬P(2) = F. So E(2)→¬P(2) = T→F = F.

**(d)** ∃x ∀y (x ≤ y): **FALSE.**
This asserts a smallest positive integer. ℤ⁺ has a smallest element (1), so: x = 1. Is 1 ≤ y for all y ∈ ℤ⁺? Yes, since y ≥ 1 for all y ∈ ℤ⁺. **TRUE.**

*(Grading correction: (d) is TRUE over ℤ⁺ because 1 is the minimum. Common instructor error to mark FALSE — verify domain is ℤ⁺ not ℤ. Over ℤ the answer would be FALSE.)*

**(d) over ℤ⁺: TRUE.** Witness: x = 1. For all y ∈ ℤ⁺, y ≥ 1. ✓

---

### Problem 2 — Negations (6 pts, 2 pts each)

**(a)** ∀x ∃y (x + y = 0)

Negation:
¬(∀x ∃y (x+y=0))
≡ ∃x ¬(∃y (x+y=0))
≡ ∃x ∀y (x+y≠0)
≡ **∃x ∀y (x + y ≠ 0)**

Reading: "There exists an integer x such that x + y ≠ 0 for every integer y."
Original is TRUE (witness y = −x). Negation is FALSE.

**(b)** ∃x ∀y (x · y = y)

Negation:
¬(∃x ∀y (xy=y))
≡ ∀x ¬(∀y (xy=y))
≡ ∀x ∃y (xy≠y)
≡ **∀x ∃y (x · y ≠ y)**

Reading: "For every integer x, there exists an integer y such that xy ≠ y."
Original is TRUE (witness x = 1: 1·y = y for all y). Negation is FALSE.

**(c)** ∀x ∀y (x < y → ∃z, x < z < y)

Negation:
¬(∀x ∀y (x<y → ∃z, x<z<y))
≡ ∃x ∃y ¬(x<y → ∃z, x<z<y)
≡ ∃x ∃y (x<y ∧ ¬∃z, x<z<y)
≡ **∃x ∃y (x < y ∧ ∀z, ¬(x < z < y))**
≡ ∃x ∃y (x < y ∧ ∀z (z ≤ x ∨ z ≥ y))

Reading: "There exist integers x and y with x < y such that no integer z satisfies x < z < y."
Over ℤ, original is FALSE (counterexample: x=0, y=1, no z with 0<z<1). Negation TRUE.

*Grading: 1 pt for correct quantifier flipping, 1 pt for correct predicate negation. Deduct 1 pt if ¬∀ or ¬∃ remains in answer.*

---

### Problem 3 — Translations (4 pts, 2 pts each)

**(a)** "Every function that terminates produces a correct output."

Domain: functions. T(f) = "f terminates", C(f) = "f produces correct output."

**∀f (T(f) → C(f))**

*Grading: 1 pt for correct universal with implication. 1 pt for correct predicate definitions. Deduct 1 pt for ∀f (T(f) ∧ C(f)) — wrong connective.*

**(b)** "There is no largest prime number."

As ∀∃ statement: "For every prime p, there exists a prime q greater than p."

Domain: ℤ⁺. P(x) = "x is prime."

**∀p (P(p) → ∃q (P(q) ∧ q > p))**

Alternative: ¬∃p (P(p) ∧ ∀q (P(q) → q ≤ p))

*Grading: 2 pts for correct ∀∃ form. Accept equivalent correct formulations. Deduct 1 pt if the formula doesn't enforce that q is prime.*

---

### Problem 4 — Nested Quantifiers (6 pts)

**(a)** (2 pts) Are ∀x∃y P(x,y) and ∃y∀x P(x,y) equivalent?

**NO.** Counterexample: domain ℤ, P(x,y) = "y > x."
- ∀x ∃y (y > x): TRUE — given any x, take y = x+1.
- ∃y ∀x (y > x): FALSE — no fixed integer exceeds every integer.

*Grading: 1 pt for correct answer (No). 1 pt for valid specific counterexample with domain and predicate.*

**(b)** P(x,y) = "x is a factor of y", domain ℤ⁺.

**(i)** ∀x ∃y P(x,y): **TRUE.**
For every x ∈ ℤ⁺, take y = x. Then x | x. ✓ (Or take y = 2x, etc.)

**(ii)** ∃y ∀x P(x,y): **FALSE.**
We need one y divisible by every positive integer. No such y exists in ℤ⁺ (any y has only finitely many divisors, but ℤ⁺ is infinite).
Explicit: y=1 fails (2∤1). y=2 fails (3∤2). No finite y works.

**(iii)** ∃x ∀y P(x,y): **TRUE.**
Witness: x = 1. Then 1 | y for every y ∈ ℤ⁺ (since y = y·1). ✓

**(iv)** ∀x ∀y P(x,y): **FALSE.**
Counterexample: x = 2, y = 3. 2 does not divide 3.

*Grading: 1 pt each (4 pts total) for correct truth value with brief justification. For TRUE, a witness suffices. For FALSE, a specific counterexample is required.*

---

### Grade Distribution (typical)

| Score | Interpretation |
|---|---|
| 18–20 | Mastered predicate logic |
| 14–17 | Solid; review negation and nested quantifier order |
| 10–13 | Review quantifier rules; redo Lab 1 exercises |
| < 10 | Schedule office hours immediately |
