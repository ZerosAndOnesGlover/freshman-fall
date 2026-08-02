# MATH 151 · Week 0
## PS 0 Solutions: INSTRUCTOR ONLY
### Do not distribute to students

---

## Part A Solutions

### A1.
(a) "Every prime greater than 2 is odd." — **Proposition, TRUE.** Proof: any even number > 2 is divisible by 2, hence composite, so not prime.

(b) "This problem set is difficult or easy." — **Proposition, TRUE** (vacuously — it must be one or the other; this is p ∨ ¬p in disguise). Could also argue it is ambiguous English — accept either "proposition" or "not a proposition with justification."

(c) "x² − 4 = 0" — **Not a proposition** (open formula with free variable x; truth depends on x). Becomes a proposition when x is specified.

(d) "There are infinitely many prime numbers." — **Proposition, TRUE.** (Euclid's theorem: assume finitely many primes p₁,...,pₙ; then p₁p₂...pₙ + 1 is divisible by none of them, contradiction.)

(e) "The program in Listing A halts on all inputs." — **Proposition** (it is either true or false, even though we may not be able to determine which — undecidability is not the same as not being a proposition). Truth value: unknown without Listing A.

(f) "Prove that 1 + 1 = 2." — **Not a proposition** (a command/imperative sentence).

---

### A2.

(a) "The user can log in iff the network is connected and the server is running."
Formula: **s ↔ (p ∧ q)**
Negation: ¬(s ↔ (p ∧ q)) ≡ (s ∧ ¬(p ∧ q)) ∨ (¬s ∧ (p ∧ q))
           ≡ (s ∧ (¬p ∨ ¬q)) ∨ (¬s ∧ p ∧ q)  [De Morgan on inner]

(b) "If network connected and server running, then database reachable and user can log in."
Formula: **(p ∧ q) → (r ∧ s)**
Negation: ¬((p ∧ q) → (r ∧ s)) ≡ (p ∧ q) ∧ ¬(r ∧ s) ≡ p ∧ q ∧ (¬r ∨ ¬s)

(c) "User cannot log in unless network is connected."
"Unless": ¬p → ¬s (if network not connected, user cannot log in)
Equivalently by contrapositive: s → p
Formula: **¬p → ¬s** (or equivalently **s → p**)
Negation: ¬(s → p) ≡ s ∧ ¬p

(d) "Not the case that server is running and database is unreachable."
Formula: **¬(q ∧ ¬r)**
Negation: ¬¬(q ∧ ¬r) ≡ q ∧ ¬r  [Double Negation]

---

### A3. (Assignment: p=T, q=T, r=F, s=F)

(a) (p ∧ q) → s
English: "If the network is connected and server is running, then the user can log in."
Evaluation: (T ∧ T) → F = T → F = **F**

(b) ¬r → ¬s
English: "If the database is not reachable, then the user cannot log in." (contrapositive of s→r)
Evaluation: ¬F → ¬F = T → T = **T**

(c) (p ↔ q) ∧ (r ↔ s)
English: "The network is connected iff the server is running, and the database is reachable iff the user can log in."
Evaluation: (T↔T) ∧ (F↔F) = T ∧ T = **T**

---

## Part B Solutions

### B1. Truth Tables

**(a) (p → q) ∧ (q → p)**

| p | q | p→q | q→p | (p→q)∧(q→p) |
|---|---|-----|-----|-------------|
| T | T | T   | T   | T           |
| T | F | F   | T   | F           |
| F | T | T   | F   | F           |
| F | F | T   | T   | T           |

This equals p ↔ q. **Contingency.**

**(b) ¬p ∨ (p ∧ q)**

| p | q | ¬p | p∧q | ¬p∨(p∧q) |
|---|---|----|-----|----------|
| T | T | F  | T   | T        |
| T | F | F  | F   | F        |
| F | T | T  | F   | T        |
| F | F | T  | F   | T        |

**Contingency.** (True except when p=T, q=F)

**(c) (p ∨ q) → (p ∧ q)**

| p | q | p∨q | p∧q | (p∨q)→(p∧q) |
|---|---|-----|-----|-------------|
| T | T | T   | T   | T           |
| T | F | T   | F   | F           |
| F | T | T   | F   | F           |
| F | F | F   | F   | T           |

**Contingency.** (This is actually equivalent to p ↔ q — see B2.)

**(d) (p → q) → ((p → ¬q) → ¬p)**

| p | q | ¬q | p→q | p→¬q | (p→¬q)→¬p | (p→q)→((p→¬q)→¬p) |
|---|---|----|-----|------|-----------|-------------------|
| T | T | F  | T   | F    | T         | T                 |
| T | F | T  | F   | T    | F         | T                 |
| F | T | F  | T   | T    | T         | T                 |
| F | F | T  | T   | T    | T         | T                 |

**Tautology.** (This is modus tollens in disguise: if p→q and p→¬q, then ¬p.)

---

### B2.

(a) B1(d) is a tautology. B1(a), B1(b), B1(c) are contingencies. None are contradictions.

(b) B1(a) is equivalent to **p ↔ q** (biconditional).

(c) B1(b): ¬p ∨ (p ∧ q)
Prove ≡ ¬p ∨ q:

Truth-table verification (all four rows):

| p | q | ¬p∨(p∧q) | ¬p∨q |
|---|---|---|---|
| T | T | F∨T = **T** | F∨T = **T** |
| T | F | F∨F = **F** | F∨F = **F** |
| F | T | T∨F = **T** | T∨T = **T** |
| F | F | T∨F = **T** | T∨F = **T** |

The columns agree in every row, so the equivalence holds. Algebraically:
¬p ∨ (p ∧ q) ≡ (¬p ∨ p) ∧ (¬p ∨ q)  [Distributivity]
             ≡ T ∧ (¬p ∨ q)           [Excluded Middle]
             ≡ ¬p ∨ q                  [Identity]
             ≡ p → q                   [Conditional Equivalence]

So B1(b) ≡ **p → q**. Algebraic proof complete.

---

### B3. (p=T, q=F, r=T, s=F)

(a) (p ∧ ¬q) → (r ∨ s)
= (T ∧ ¬F) → (T ∨ F)
= (T ∧ T) → T
= T → T = **T**

(b) ¬(p ↔ r) ∨ (q ∧ ¬s)
= ¬(T ↔ T) ∨ (F ∧ ¬F)
= ¬T ∨ (F ∧ T)
= F ∨ F = **F**

(c) ((p → q) → r) ∧ (¬s ∨ q)
= ((T → F) → T) ∧ (¬F ∨ F)
= (F → T) ∧ (T ∨ F)
= T ∧ T = **T**

---

### B4.

(a) 2⁵ = **32 rows**

(b) Tautology: true in **32** rows. Contradiction: true in **0** rows.

(c) **Contingency.** A formula true in exactly 1 row is a contingency (it is satisfiable but not a tautology).

Example: p₁ ∧ p₂ ∧ p₃ ∧ p₄ ∧ p₅ — true only when all five variables are true.

---

## Part C Solutions

### C1.

**(a)** "If divisible by 4, then divisible by 2." (p → q)
- Converse: "If divisible by 2, then divisible by 4." (q → p) — **NOT equivalent**
- Inverse: "If not divisible by 4, then not divisible by 2." (¬p → ¬q) — **NOT equivalent**
- Contrapositive: "If not divisible by 2, then not divisible by 4." (¬q → ¬p) — **Equivalent**

**(b)** p → q (O(n log n) → efficient)
- Converse: q → p — not equivalent
- Inverse: ¬p → ¬q — not equivalent
- Contrapositive: ¬q → ¬p — equivalent

**(c)** p → (q ∧ r)
- Converse: (q ∧ r) → p
- Inverse: ¬p → ¬(q ∧ r) ≡ ¬p → (¬q ∨ ¬r)
- Contrapositive: ¬(q ∧ r) → ¬p ≡ (¬q ∨ ¬r) → ¬p — **Equivalent**

**(d)** ¬p → ¬(q ∨ r)
- Contrapositive: (q ∨ r) → p — **Equivalent**
- Converse: ¬(q ∨ r) → ¬p ≡ (¬q ∧ ¬r) → ¬p
- Inverse: p → (q ∨ r)

---

### C2.

(a) p = "2 is odd" = F. The statement "If F, then moon is cheese" is **vacuously true** (F→anything = T).

(b) p = "score 100 on every PS" = F (scored 80 on PS0). The conditional is **vacuously true** — not violated.

(c) x = 3: p = "x>100" = F. Vacuously true. x = 200: p=T, q = "x>50" = T. **T→T = T** (substantively true).

---

### C3.

(a) (p → q) ∨ (q → p):
= (¬p ∨ q) ∨ (¬q ∨ p)
= (¬p ∨ p) ∨ (q ∨ ¬q)
= T ∨ T = T ✓

This is a tautology. The "paradox": in everyday reasoning, "p implies q" means there's a causal or logical connection. But material implication is defined purely by truth values. When p=F or q=T, the conditional is true regardless of any connection. So for any p and q, at least one of "p implies q" or "q implies p" is materially true — even for completely unrelated p and q. This is a feature (for formal logic) but seems wrong colloquially.

(b) p → (q → p) ≡ ¬p ∨ (¬q ∨ p) = (¬p ∨ p) ∨ ¬q = T ∨ ¬q = T. ✓

"Paradox": A true proposition is implied by anything. If p is true, then "if q then p" is true — even if q and p are totally unrelated. Again: material implication is not causal.

(c) The material conditional is the right choice because: (1) it makes implication computable from truth values alone, with no need to evaluate "relevance" or "causality"; (2) it is consistent — it never produces contradictions; (3) it makes all classical inference rules (modus ponens, contrapositive, etc.) valid, which is what we need for mathematical proof. The "paradoxes" are an artifact of applying a formal tool to informal reasoning — not a defect in the formal tool.

---

## Part D Solutions

### D1.

**(a)** (p ∧ q) ∨ (p ∧ ¬q)
≡ p ∧ (q ∨ ¬q)    [Distributivity: factor p]
≡ p ∧ T             [Excluded Middle]
≡ p                  [Identity] ∎

**(b)** (p → q) ∧ (p → ¬q)
≡ (¬p ∨ q) ∧ (¬p ∨ ¬q)   [Conditional Equivalence × 2]
≡ ¬p ∨ (q ∧ ¬q)            [Distributivity: factor ¬p]
≡ ¬p ∨ F                    [Non-Contradiction]
≡ ¬p                         [Identity] ∎

**(c)** ¬(p ↔ q)
≡ ¬((p → q) ∧ (q → p))                         [Biconditional Expansion]
≡ ¬(p → q) ∨ ¬(q → p)                           [De Morgan]
≡ (p ∧ ¬q) ∨ (q ∧ ¬p)                           [Negation of Conditional × 2]
≡ (p ∧ ¬q) ∨ (¬p ∧ q)                           [Commutativity of second term] ∎

**(d)** (p ∨ q) ∧ (¬p ∨ r) → (q ∨ r)
≡ ¬((p ∨ q) ∧ (¬p ∨ r)) ∨ (q ∨ r)              [Conditional Equivalence]
≡ (¬(p ∨ q) ∨ ¬(¬p ∨ r)) ∨ (q ∨ r)             [De Morgan]
≡ ((¬p ∧ ¬q) ∨ (p ∧ ¬r)) ∨ (q ∨ r)             [De Morgan × 2]

Distribute and simplify:
= (¬p ∧ ¬q) ∨ (p ∧ ¬r) ∨ q ∨ r

Case analysis suffices here for a truth-table-free proof:
- If p=T: (p∧¬r)∨r = ¬r∨r = T ✓
- If p=F: (¬p∧¬q)∨q = ¬q∨q = T ✓

So the formula ≡ T. ∎ (Alternatively: build truth table — all 8 rows are T.)

---

### D2. Converting to CNF

**(a)** p → q
≡ ¬p ∨ q    [Conditional Equivalence]

This is already CNF (one clause: (¬p ∨ q)). **CNF: (¬p ∨ q)**

**(b)** p ↔ q
≡ (p → q) ∧ (q → p)              [Biconditional Expansion]
≡ (¬p ∨ q) ∧ (¬q ∨ p)           [Conditional Equivalence × 2]

**CNF: (¬p ∨ q) ∧ (¬q ∨ p)**  ✓ (Two clauses.)

**(c)** ¬(p ∨ ¬q) → r
≡ ¬¬(p ∨ ¬q) ∨ r         [Conditional Equivalence]
≡ (p ∨ ¬q) ∨ r           [Double Negation]
≡ p ∨ ¬q ∨ r             [Associativity]

**CNF: (p ∨ ¬q ∨ r)**  ✓ (Single clause.)

---

### D3. Converting to DNF

**(a)** p ∧ (q ∨ ¬r)

Truth table (rows where formula is T):
| p | q | r | p∧(q∨¬r) |
|---|---|---|----------|
| T | T | T | T∧(T∨F)=T |
| T | T | F | T∧(T∨T)=T |
| T | F | T | T∧(F∨F)=F |
| T | F | F | T∧(F∨T)=T |
| F | * | * | F∧(*)=F   |

True rows: (T,T,T), (T,T,F), (T,F,F)

Minterms:
- (T,T,T): p ∧ q ∧ r
- (T,T,F): p ∧ q ∧ ¬r
- (T,F,F): p ∧ ¬q ∧ ¬r

**DNF:** (p ∧ q ∧ r) ∨ (p ∧ q ∧ ¬r) ∨ (p ∧ ¬q ∧ ¬r)

Verify vs distributive law result:
p ∧ (q ∨ ¬r) ≡ (p∧q) ∨ (p∧¬r)
= (p∧q∧(r∨¬r)) ∨ (p∧¬r∧(q∨¬q))
= (p∧q∧r) ∨ (p∧q∧¬r) ∨ (p∧¬r∧q) ∨ (p∧¬r∧¬q)

Eliminate duplicate (p∧q∧¬r): matches ✓

**(b)** p ↔ q:
True rows: (T,T) and (F,F)
Minterms: (p∧q) and (¬p∧¬q)
**DNF:** (p ∧ q) ∨ (¬p ∧ ¬q) ✓ (matches Biconditional Expansion 2 from laws)

---

### D4.

**(a)** p ∧ q using {¬, ∨}:
By De Morgan: ¬(¬p ∨ ¬q) ≡ p ∧ q. ✓

**(b)** p ∨ q using {¬, →}:
p ∨ q ≡ ¬p → q  [since p→q ≡ ¬p∨q, so ¬p→q ≡ ¬¬p∨q ≡ p∨q] ✓

**(c)** {∧, ∨} cannot express ¬: Every formula using only ∧ and ∨, when all variables are T, evaluates to T. But ¬p evaluates to F when p=T. So negation is outside the expressible set.

More formally: any formula built from ∧ and ∨ with all-true inputs gives all-true outputs. Negation takes a true input to false — impossible with these connectives alone.

---

## Bonus Solutions

**(a)** p | q = ¬(p∧q): truth table matches NAND. ✓

**(b)** 
- ¬p = p | p  (since ¬(p∧p) = ¬p) ✓
- p ∧ q = (p|q)|(p|q)  [since ¬(¬(p∧q)) = p∧q and using (a)] ✓
- p ∨ q = (p|p)|(q|q)  [this is (¬p)|(¬q) = ¬(¬p ∧ ¬q) = p∨q, by De Morgan] ✓

**(c)** NOR: p↓q = ¬(p∨q)
- ¬p = p ↓ p  (since ¬(p∨p) = ¬p) ✓
- p ∨ q = (p↓q)↓(p↓q)  (double NOR = double negation of OR = OR) ✓
- p ∧ q = (p↓p)↓(q↓q) = ¬p↓¬q = ¬(¬p∨¬q) = p∧q by De Morgan ✓

**(d)** Using one gate type simplifies manufacturing: a chip fab can optimize a single cell design to the maximum. Cost per gate drops. You also need only one type of spare part. The tradeoff: circuits may require more gates to implement the same function compared to a mixed-gate design. For example, a 2-input AND requires 2 NAND gates (one to NAND, one to negate the NAND output), vs a single AND gate. This extra gate count means more area and potentially more power consumption — the practical cost of universality.
