# MATH 151 · Week 1
## PS1 Solutions — INSTRUCTOR ONLY

---

## Part A Solutions

### A1.
P(x) = x² − 5x + 6 = 0 = (x−2)(x−3) = 0, so P(x) is true iff x = 2 or x = 3.

**(a)** From {0,1,2,3,4,6}: P(2) = T, P(3) = T. All others: F. **Answer: {2, 3}**

**(b)** ∀x ∈ {0,1,2,3,4,6}, P(x): **FALSE**. Counterexample: x = 0, P(0) = 0−0+6 = 6 ≠ 0.

**(c)** ∃x ∈ {0,1,2,3,4,6}, P(x): **TRUE**. Witness: x = 2 (P(2) = 4−10+6 = 0 ✓).

---

### A2. D(x,y) = "x divides y", domain ℤ⁺

**(a)** D(3,12): Does 3 | 12? 12 = 4×3. **TRUE.**

**(b)** D(5,13): Does 5 | 13? 13 = 2×5 + 3. Remainder 3 ≠ 0. **FALSE.**

**(c)** D(1,n) for any n ∈ ℤ⁺: n = n×1 always. **TRUE** for all n.

**(d)** D(n,0): is 0 = k·n for some k? The answer turns entirely on the quantifier's domain, and
this is the point of the part.

- Under the **standard** definition of divisibility, k ranges over **ℤ**, so k = 0 gives 0 = 0·n and
  **n | 0 for every n**. → **TRUE.**
- If the problem's stated domain restricts k to **ℤ⁺**, then k ≥ 1 forces k·n ≥ n > 0 ≠ 0. → **FALSE.**

**Accept either answer with a coherent justification that names which convention is in use.** Award
no marks for an unjustified TRUE or FALSE. Worth raising in discussion: this is why definitions
specify their domains, and why "n | 0" surprises students who have only seen positive divisors.

**(e)** D(n,n): n = 1×n always. **TRUE** for all n ∈ ℤ⁺.

**(f)** D(n,1) for n > 1: Does n | 1? We need 1 = k·n for some positive integer k. Since n > 1 and k ≥ 1, k·n ≥ n > 1. Impossible. **FALSE.**

---

### A3. Free and bound variables

**(a)** ∀x (P(x, y) ∧ Q(y, z)):
- x: **bound** (quantified by ∀x)
- y: **free** (appears in P(x,y) and Q(y,z), not quantified)
- z: **free**

**(b)** ∃x P(x) ∧ ∀x Q(x):
- First x (in ∃x P(x)): **bound** by ∃
- Second x (in ∀x Q(x)): **bound** by ∀
- These are two *different* x's despite same name. Recommend renaming to ∃x P(x) ∧ ∀y Q(y).

**(c)** ∀x ∃y (R(x, y) → S(y, z)) ∧ T(x):
- x in R(x,y): bound by ∀x
- y in R(x,y), S(y,z): bound by ∃y
- z in S(y,z): **free**
- x in T(x): **free** — T(x) is outside the scope of ∀x (the ∀x scopes over ∃y(R→S), not the entire conjunction, assuming standard left-binding)

*Note for graders:* Depending on how the scope of ∀x is read — whether it covers the entire formula or just ∃y(R→S) — the x in T(x) may be bound or free. If students write it as ∀x [∃y (R(x, y) → S(y, z)) ∧ T(x)], then x in T(x) is bound. Accept either interpretation with consistent justification.

**(d)** ∃x (∀y P(x, y)) ∧ ∃y Q(x, y):
- x in ∃x(...): bound in first conjunct
- y in ∀y P(x,y): bound
- x in Q(x,y): **free** (outside scope of ∃x)
- y in ∃y Q(x,y): bound by that ∃y
- Q(x,y) contains a free x and a bound y.

---

## Part B Solutions

### B1. (Domain: ℤ unless stated)

**(a)** ∀x, x+1 > x: **TRUE.** For any integer x, adding 1 gives a strictly larger integer.

**(b)** ∀x, x² ≥ 0: **TRUE** over ℤ (and ℝ). The square of any real number is non-negative.

**(c)** ∀x, x² > x: **FALSE.** Counterexample: x = 0 (0 > 0 is false). Also x = 1: 1 > 1 is false.

**(d)** ∃x, x² = x: **TRUE.** Witness: x = 0 (0² = 0 ✓). Also x = 1.

**(e)** ∃x ∈ ℝ, x² = 2: **TRUE.** Witness: x = √2 ∈ ℝ.

**(f)** ∃x ∈ ℤ, x² = 2: **FALSE.** √2 is irrational, so no integer squares to 2. (If n² = 2, then n = √2 ∉ ℤ.)

**(g)** ∀x ∈ ℚ, ∃y ∈ ℚ, y > x: **TRUE.** Given any rational x, take y = x + 1 ∈ ℚ, and y > x.

**(h)** ∀x ∈ ℝ, x = 0 ∨ x > 0 ∨ x < 0: **TRUE.** This is the trichotomy of real numbers — every real is zero, positive, or negative. (Tautological given the ordering of ℝ.)

---

### B2. Translations

**(a)** "Some prime number is even."
Domain: ℤ⁺. P(x) = "x is prime", E(x) = "x is even."
**∃x (P(x) ∧ E(x)).** [True — witness: x = 2]

**(b)** "Not every real number is rational."
Domain: ℝ. Q(x) = "x is rational."
**¬∀x Q(x)** equiv. **∃x ¬Q(x).** [True — witness: x = √2]

**(c)** "Every algorithm either terminates or runs forever."
Domain: algorithms. T(a) = "a terminates", F(a) = "a runs forever" = ¬T(a).
**∀a (T(a) ∨ ¬T(a)).** This is a tautology — every algorithm either terminates or it doesn't. The formula is vacuously true regardless of the algorithms. (It's propositional tautology p ∨ ¬p applied universally.)

**(d)** "There is a real number that is not the square of any real number."
Domain: ℝ.
**∃x ∈ ℝ, ∀y ∈ ℝ, y² ≠ x.** [True — witness: x = −1, since no real squares to a negative.]

**(e)** "Every input to the function produces an output."
Domain: inputs, outputs. f = the function.
**∀x ∃y, f(x) = y.** (This is essentially the definition of total function.)

**(f)** "No integer is both positive and negative."
Domain: ℤ. Pos(x) = "x > 0", Neg(x) = "x < 0."
**∀x ¬(Pos(x) ∧ Neg(x))** equiv. **∀x (Pos(x) → ¬Neg(x)).**

---

### B3. Translations from logic to English (Domain: ℝ, P(x) = "x is rational")

**(a)** ∀x (x > 0 → ∃y, y² = x): "Every positive real number has a (real) square root." TRUE.

**(b)** ∃x ∀y (x ≤ y): "There exists a real number that is less than or equal to every real number" — i.e., a minimum real number. FALSE over ℝ (ℝ has no minimum).

**(c)** ∀x ∀y (x < y → ∃z, x < z < y): "Between any two distinct real numbers, there exists a real number." TRUE (take z = (x+y)/2).

**(d)** ∀x (P(x) → ∀y (P(y) → P(x+y))): "For any two rational numbers, their sum is rational." TRUE (ℚ is closed under addition).

**(e)** ∃x ¬P(x): "There exists an irrational real number." TRUE (e.g., √2).

**(f)** ¬∀x P(x): "Not every real number is rational." TRUE (same meaning as (e)).

**(e) and (f) equivalence:** ¬∀x P(x) ≡ ∃x ¬P(x) by De Morgan for quantifiers. So yes, they are equivalent — and both are true.

---

## Part C Solutions

### C1. Negations

**(a)** ∀x, x² ≥ 0
Negation: **∃x, x² < 0.** Original: TRUE (over ℤ/ℝ). Negation: FALSE.

**(b)** ∃x, x + x = x (i.e., 2x = x, i.e., x = 0)
Negation: **∀x, x + x ≠ x.** Original: TRUE (witness x=0). Negation: FALSE.

**(c)** ∀x ∈ ℤ, ∃y ∈ ℤ, x + y = 0
Negation: **∃x ∈ ℤ, ∀y ∈ ℤ, x + y ≠ 0.** Original: TRUE (given x, take y = −x). Negation: FALSE.

**(d)** ∃x ∈ ℝ, ∀y ∈ ℝ, x · y = y
Note: x · y = y iff x = 1 (for y ≠ 0). x = 1 satisfies ∀y, 1·y = y. Original: TRUE (witness x=1).
Negation: **∀x ∈ ℝ, ∃y ∈ ℝ, x · y ≠ y.** FALSE (x=1 is a counterexample to the negation).

**(e)** ∀x (E(x) → ∃k, x = 2k)
Negation: **∃x (E(x) ∧ ∀k, x ≠ 2k).**
Reading: "Some even number is not equal to 2k for any integer k." This is the definition of being even! So the original is the definition of even numbers, which is TRUE by definition. Negation: FALSE.

---

### C2. English → Logic → Negate → English

**(a)** "Every student who passes the midterm passes the course."
Let S(x)="x is a student", M(x)="x passes midterm", C(x)="x passes course."
Formula: ∀x (S(x) ∧ M(x) → C(x))
Negation: ∃x (S(x) ∧ M(x) ∧ ¬C(x))
English: "There is a student who passes the midterm but does not pass the course."

**(b)** "Some program can solve every instance of the halting problem."
Let P(x)="x is a program", H(i)="i is an instance of halting problem", Solves(x,i)="x solves i."
Formula: ∃x (P(x) ∧ ∀i (H(i) → Solves(x,i)))
Negation: ∀x (P(x) → ∃i (H(i) ∧ ¬Solves(x,i)))
English: "Every program fails to solve at least one instance of the halting problem." (This is actually TRUE — the halting problem is undecidable.)

**(c)** "No two distinct real numbers have the same absolute value."
Domain: ℝ. Formula: ∀x ∀y (x ≠ y → |x| ≠ |y|)
Negation: ∃x ∃y (x ≠ y ∧ |x| = |y|)
English: "There exist two distinct real numbers with the same absolute value." (TRUE — e.g., 3 and −3.)
So the original is FALSE (and indeed, x and −x have the same absolute value for x ≠ 0).

---

### C3. Error identification

**(a)** Statement: ∀x P(x). Proposed negation: ∀x ¬P(x).
**Error:** The quantifier was not flipped. The negation of ∀ is ∃, not ∀.
**Correct negation:** ∃x ¬P(x).

(Note: ∀x ¬P(x) is the statement that P holds for NO x — much stronger than merely "not all x satisfy P.")

**(b)** Statement: ∃x (P(x) ∧ Q(x)). Proposed negation: ∀x (¬P(x) ∧ ¬Q(x)).
**Error:** ∧ was not flipped to ∨ when De Morgan's Law was applied inside.
**Correct negation:** ∀x (¬P(x) ∨ ¬Q(x)) [De Morgan: ¬(P∧Q) ≡ ¬P∨¬Q].

**(c)** Statement: ∀x (P(x) → Q(x)). Proposed negation: ∃x (P(x) → ¬Q(x)).
**Error:** The predicate was negated incorrectly. The negation of P→Q is P∧¬Q (not P→¬Q).
**Correct negation:** ∃x (P(x) ∧ ¬Q(x)).

---

## Part D Solutions

### D1. Truth values over ℤ

**(a)** ∀x ∃y (y > x): **TRUE.** Given x, take y = x+1.

**(b)** ∃y ∀x (y > x): **FALSE.** Any candidate y would need to exceed every integer, including y−1. Impossible.

**(c)** ∀x ∀y (x < y → ∃z, x < z < y): **FALSE** over ℤ. Counterexample: x=0, y=1. No integer z satisfies 0 < z < 1.
(This is TRUE over ℝ — illustrates how domain matters.)

**(d)** ∀x ∃y (x + y = 0): **TRUE.** Given x, take y = −x ∈ ℤ.

**(e)** ∃x ∀y (x + y = 0): **FALSE.** Any fixed x would need x + y = 0 for all y, requiring y = −x always — but y varies. No single x satisfies this for all y.

**(f)** ∀x ∀y ∃z (z = x + y): **TRUE.** Given any x, y ∈ ℤ, take z = x+y ∈ ℤ (integers are closed under addition).

**(g)** ∃x ∃y (x² + y² = 5): **TRUE.** Witness: x=1, y=2. 1+4=5 ✓. (Also x=2,y=1 and negatives.)

**(h)** ∀x ∃y (x · y = 1) over ℤ: **FALSE.** Counterexample: x=2. We need 2y=1, so y=1/2 ∉ ℤ.

**(i)** ∀x ∃y (x · y = 1) over ℚ\{0}: **TRUE.** Given any non-zero rational x = p/q, take y = q/p ∈ ℚ\{0}. Then xy = 1.

**(j)** ∃x ∀y ∀z (x = y + z): **FALSE.** A single x would need to equal y+z for all pairs (y,z), which is impossible since y+z takes all integer values.

---

### D2. Negations of nested statements

**(a)** ∀x ∀y (x + y = y + x)
Negation: **∃x ∃y (x + y ≠ y + x)**
Original: TRUE (commutativity of addition in ℤ). Negation: FALSE.

**(b)** ∃x ∀y (x ≤ y)
Negation: **∀x ∃y (x > y)** [flip ∃→∀, flip ∀→∃, negate ≤ to >]
Original: FALSE (no smallest integer). Negation: TRUE (for any x, take y = x−1).

**(c)** ∀x ∃y ∀z (z > y → z > x)
Negation: **∃x ∀y ∃z (z > y ∧ z ≤ x)**

Work:
¬(∀x ∃y ∀z (z>y→z>x))
≡ ∃x ¬(∃y ∀z (z>y→z>x))
≡ ∃x ∀y ¬(∀z (z>y→z>x))
≡ ∃x ∀y ∃z ¬(z>y→z>x)
≡ ∃x ∀y ∃z (z>y ∧ z≤x)

Original: TRUE over ℤ — given x, take y = x. Then ∀z, z>x→z>x (trivially true).
Negation: FALSE.

**(d)** ∃x ∃y (x² + y² < 0)
Negation: **∀x ∀y (x² + y² ≥ 0)**
Original: FALSE (sum of squares ≥ 0 always over ℤ). Negation: TRUE.

---

### D3. Definitions

**(a) Function definition:**
∀x∈A, ∃!y∈B, f(x)=y

Expanded form of ∃!:
∀x∈A, (∃y∈B, f(x)=y) ∧ (∀y₁∈B ∀y₂∈B, (f(x)=y₁ ∧ f(x)=y₂) → y₁=y₂)

**(b) f(x) = 2x, injectivity:**
∀x₁∈ℤ ∀x₂∈ℤ, (f(x₁)=f(x₂) → x₁=x₂)
= ∀x₁ ∀x₂, (2x₁=2x₂ → x₁=x₂)

Proof: Assume 2x₁ = 2x₂. Dividing both sides by 2: x₁ = x₂. ✓ So f is injective.

**(c) f(x) = 2x, surjectivity onto ℤ:**
∀y∈ℤ, ∃x∈ℤ, 2x=y

Counterexample: y=1. We need 2x=1, so x=1/2 ∉ ℤ. So f is NOT surjective onto ℤ.
(f is surjective onto the even integers, but not onto all of ℤ.)

**(d) Sequence {aₙ} = (−1)ⁿ bounded:**
Definition: ∃M∈ℝ, ∀n∈ℕ, |aₙ| ≤ M.
Take M = 1. Then |aₙ| = |(−1)ⁿ| = 1 ≤ 1 for all n. ✓ Bounded.

**(e) Density of ℚ in ℝ:**
Formal: ∀x∈ℝ ∀y∈ℝ, (x < y → ∃q∈ℚ, x < q < y)
Negation: ∃x∈ℝ ∃y∈ℝ, (x < y ∧ ∀q∈ℚ, ¬(x < q < y))
         = ∃x∈ℝ ∃y∈ℝ, (x < y ∧ ∀q∈ℚ, q≤x ∨ q≥y)
English: "There exist two distinct real numbers with no rational number strictly between them."

---

## Part E Solutions

### E1. Program properties

**(a)** Type safety:
Domain: programs, runtime states.
T(p) = "p is well-typed", E(p,s) = "p encounters a type error at runtime state s."
**∀p (T(p) → ∀s ¬E(p,s))**
Or: **∀p ∀s (T(p) ∧ reachable(p,s) → ¬E(p,s))**

**(b)** Memory safety:
Let A(addr,t) = "address addr was allocated at or before time t and not yet freed."
Access(p,addr,t) = "program p accesses address addr at time t."
**∀t ∀addr (Access(p,addr,t) → A(addr,t))**

**(c)** Termination:
Domain: inputs, execution steps.
Valid(x) = "x is a valid input", Halts(p,x,n) = "p halts on x within n steps."
**∀x (Valid(x) → ∃n∈ℕ, Halts(p,x,n))**

---

### E2. Big-O

Given: f(n) = O(g(n)) iff ∃C∈ℝ⁺ ∃n₀∈ℕ ∀n∈ℕ (n≥n₀ → f(n)≤C·g(n))

**(a)** Negation (f(n) ≠ O(g(n))):
¬(∃C>0 ∃n₀∈ℕ ∀n∈ℕ (n≥n₀ → f(n)≤C·g(n)))
≡ **∀C>0 ∀n₀∈ℕ ∃n∈ℕ (n≥n₀ ∧ f(n) > C·g(n))**

**(b)** English: "For every positive constant C and every threshold n₀, there exists some n ≥ n₀ where f(n) exceeds C·g(n)." In other words: f grows faster than any constant multiple of g — no matter how large a constant you pick, f eventually exceeds it.

**(c)** Pattern: ∃∃∀ — two existentials followed by one universal. This is a Σ₂ statement (though in the negation it becomes ∀∀∃, which is Π₂).

---

### E3. Load balancer specs

**(a)**
- Spec A: ∀r ∃s, s processes r. "For every request, some server processes it."
- Spec B: ∃s ∀r, s processes r. "There is a single server that processes every request."

**(b)** Spec B is stronger (∃∀ implies ∀∃ but not vice versa). Spec A is weaker.

**(c)** A load balancer satisfies **Spec A** — each request is routed to some server, but not necessarily the same one. Different requests may go to different servers.

**(d)** A single server handling all requests satisfies **both Spec A and Spec B**. The single server is the witness for ∃s in Spec B, and it works for every request r.

---

## Bonus Solutions

### Bonus 1

**(a)** Continuity at a: ∀ε>0 ∃δ>0 ∀x (|x−a|<δ → |f(x)−f(a)|<ε)
Uniform continuity: ∀ε>0 ∃δ>0 ∀x ∀y (|x−y|<δ → |f(x)−f(y)|<ε)

Difference: In continuity, the ∀x for the center point a is *outside* ∃δ. In uniform continuity, both ∀x and ∀y (the two points being compared) come *after* ∃δ. So for continuity, δ may depend on both ε and the center point a. For uniform continuity, δ depends only on ε.

**(b)** Uniform continuity → pointwise continuity at every a:
Given ε>0, uniform continuity supplies δ that works for ALL x,y. In particular, fixing x=a and letting y be the variable, we have: ∀y (|a−y|<δ → |f(a)−f(y)|<ε). This is exactly pointwise continuity at a. ✓

**(c)** Negation of uniform continuity:
∃ε>0 ∀δ>0 ∃x ∃y (|x−y|<δ ∧ |f(x)−f(y)|≥ε)
English: "There exists some ε>0 such that for any δ>0, no matter how small, we can find two points within δ of each other whose function values are at least ε apart."
Informally: the function can be made to oscillate by at least ε over arbitrarily small intervals. Example: f(x) = sin(1/x) near x=0.

### Bonus 2

**(a)** ∀x ∃y (x≠y ∧ F(x,y)) — everyone has a friend (distinct from themselves)

**(b)** ∃x ∀y (x≠y → F(x,y)) — someone is friends with everyone else

**(c)** ∀x ¬F(x,x) — no one is friends with themselves

**(d)** ∀x ∀y (F(x,y) → F(y,x)) — friendship is symmetric

**(e)** With (c) and (d): ¬(b) = ∀x ∃y (x≠y ∧ ¬F(x,y)).
Using (d), F(x,y)↔F(y,x), so ¬F(x,y)↔¬F(y,x).
The negation says: "Everyone has someone they are not friends with (other than themselves)." With symmetry this means: "Everyone has some non-friend." This cannot be further simplified to a dramatically shorter form, but it can be stated as: "No person is friends with every other person at the party."
