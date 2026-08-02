# MATH 151 — Discrete Mathematics for Computer Science
## Lab 4 — Set Workshop: Proofs, Venn Diagrams, and Computation
### Wednesday, Week 4 | Duration: 2 hours

---

**Lab Objectives:**
1. Practice element-chasing and algebraic proofs of set identities
2. Use Venn diagrams as an intuition-building (not proof-providing) tool
3. Verify set identities computationally before proving them
4. Compute power sets and Cartesian products programmatically
5. Apply Inclusion-Exclusion to real counting problems

**Materials:** Pencil, paper, laptop with Python 3.

---

## Section 1 — Venn Diagrams as Intuition (Not Proof) (20 min)

Venn diagrams are excellent for building intuition but are **not** a valid proof technique in this course — they don't scale beyond 3 sets and don't handle general/arbitrary sets. Use them to guess identities, then prove with element-chasing or algebra.

### Exercise 1.1

For each pair of expressions, sketch a 3-set Venn diagram (sets $A$, $B$, $C$) and shade the region corresponding to each expression. Determine if the two expressions represent the same region.

**(a)** $A \cap (B \cup C)$ vs. $(A \cap B) \cup (A \cap C)$

**(b)** $A - (B \cap C)$ vs. $(A - B) \cup (A - C)$

**(c)** $(A \cup B) \cap C$ vs. $A \cup (B \cap C)$

For each pair, state whether the shaded regions match. If they match, this suggests (but doesn't prove) an identity — you'll prove the true ones in Section 2.

---

### Exercise 1.2 — Venn Diagram Counting

Draw a 3-circle Venn diagram for sets $A$, $B$, $C$ within universe $U$. Label the 8 regions (including "in none").

Given: $|U|=100$, $|A|=40$, $|B|=35$, $|C|=30$, $|A\cap B|=15$, $|A\cap C|=10$, $|B\cap C|=8$, $|A\cap B\cap C|=3$.

Fill in the count for each of the 8 regions of the Venn diagram (the 7 "inside" regions plus "outside all three").

*(Work from the center outward: fill in $|A\cap B\cap C|$ first, then the pairwise-only regions, then the single-set-only regions, then the outside region.)*

---

## Section 2 — Proof Writing (45 min)

Write complete proofs. For each, state whether you use element-chasing or algebraic proof.

---

### Exercise 2.1

Prove: $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$

(This confirms your Venn diagram observation from Exercise 1.1(a).)

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

### Exercise 2.2

Prove: $A - (B \cap C) = (A - B) \cup (A - C)$

(Confirms Exercise 1.1(b).)

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

### Exercise 2.3

**Disprove** (find a counterexample): $(A \cup B) \cap C = A \cup (B \cap C)$

(This should NOT match in your Venn diagram from 1.1(c) in general — find specific sets that break it.)

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

### Exercise 2.4

Prove: $\overline{A} - \overline{B} = B - A$

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

### Exercise 2.5

Prove: $A \subseteq B \iff A \cup B = B$

*(This is a biconditional — prove both directions.)*

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

## Section 3 — Python: Set Operations and Verification (35 min)

Create `set_tools.py`. Python's built-in `set` type implements exactly the mathematical set abstraction.

### Exercise 3.1 — Basic Operations Verification

```python
def verify_identity(A, B, C, lhs_func, rhs_func, name="identity"):
    """
    Verifies a set identity for specific sets A, B, C.
    lhs_func and rhs_func are functions taking (A,B,C) and returning a set.
    """
    lhs = lhs_func(A, B, C)
    rhs = rhs_func(A, B, C)
    matches = (lhs == rhs)
    print(f"{name}: {'HOLDS' if matches else 'FAILS'}")
    print(f"  LHS = {lhs}")
    print(f"  RHS = {rhs}")
    return matches
```

**Task:** Verify each identity from Exercise 2.1–2.4 using THREE different random-ish sets. If it holds for all three trials, this supports (does not prove) your hand-written proof.

```python
# Test sets — use several different combinations
test_cases = [
    ({1,2,3,4,5}, {3,4,5,6,7}, {5,6,7,8,9}),
    ({1,2}, {2,3}, {3,4}),
    ({1,2,3,4,5,6,7,8}, {2,4,6,8}, {1,3,5,7}),
]

for A, B, C in test_cases:
    verify_identity(A, B, C,
        lambda A,B,C: A & (B | C),
        lambda A,B,C: (A & B) | (A & C),
        "A∩(B∪C) = (A∩B)∪(A∩C)")
```

Run this for all identities from Exercise 2.1, 2.2, 2.4. Report whether all hold.

---

### Exercise 3.2 — Counterexample Search

Write a function that randomly searches for a counterexample to a claimed identity:

```python
import random
import itertools

def find_counterexample(lhs_func, rhs_func, universe, num_trials=1000, subset_size_max=5):
    """
    Randomly generates sets A, B, C from the given universe and checks
    if lhs_func(A,B,C) == rhs_func(A,B,C). Returns first counterexample found.
    """
    universe = list(universe)
    for _ in range(num_trials):
        A = set(random.sample(universe, random.randint(0, min(subset_size_max, len(universe)))))
        B = set(random.sample(universe, random.randint(0, min(subset_size_max, len(universe)))))
        C = set(random.sample(universe, random.randint(0, min(subset_size_max, len(universe)))))
        
        lhs = lhs_func(A, B, C)
        rhs = rhs_func(A, B, C)
        
        if lhs != rhs:
            return (A, B, C, lhs, rhs)
    return None  # no counterexample found in num_trials
```

**Task:** Use this to find a counterexample to the FALSE claim from Exercise 2.3:
$(A \cup B) \cap C = A \cup (B \cap C)$

```python
universe = range(1, 11)
result = find_counterexample(
    lambda A,B,C: (A|B)&C,
    lambda A,B,C: A|(B&C),
    universe
)
if result:
    A,B,C,lhs,rhs = result
    print(f"Counterexample found: A={A}, B={B}, C={C}")
    print(f"LHS = {lhs}, RHS = {rhs}")
else:
    print("No counterexample found — identity may hold (or trials too few)")
```

Compare the counterexample found by the program to the one you found by hand in Exercise 2.3.

---

### Exercise 3.3 — Power Set Generator

```python
def power_set(s):
    """Generate the power set of s as a set of frozensets."""
    s = list(s)
    n = len(s)
    result = set()
    for mask in range(2**n):
        subset = frozenset(s[i] for i in range(n) if (mask >> i) & 1)
        result.add(subset)
    return result

A = {1, 2, 3}
pA = power_set(A)
print(f"P(A) has {len(pA)} elements:")
for s in sorted(pA, key=len):
    print(f"  {set(s)}")
```

**Task:** Run this for $A = \{1,2,3\}$ and verify against your hand computation from PS4 D1. Then run for $A = \{1,2,3,4,5\}$ and verify $|\mathcal{P}(A)| = 32$.

---

### Exercise 3.4 — Cartesian Product and Inclusion-Exclusion

```python
def cartesian_product(A, B):
    return {(a, b) for a in A for b in B}

def inclusion_exclusion_2(A, B):
    """Verify |A∪B| = |A|+|B|-|A∩B|"""
    lhs = len(A | B)
    rhs = len(A) + len(B) - len(A & B)
    return lhs, rhs, lhs == rhs

def inclusion_exclusion_3(A, B, C):
    """Verify |A∪B∪C| formula"""
    lhs = len(A | B | C)
    rhs = len(A)+len(B)+len(C) - len(A&B)-len(A&C)-len(B&C) + len(A&B&C)
    return lhs, rhs, lhs == rhs
```

**Task:**
1. Compute $A \times B$ for $A=\{1,2\}$, $B=\{'x','y','z'\}$. Verify $|A\times B| = |A|\cdot|B|$.
2. Verify inclusion_exclusion_2 and inclusion_exclusion_3 on at least 3 different set triples each.
3. Solve PS4 E2 (multiples of 3 or 5 up to 300) computationally, then compare to your hand calculation.

```python
multiples_of_3 = set(range(3, 301, 3))
multiples_of_5 = set(range(5, 301, 5))
print(f"Divisible by 3 or 5: {len(multiples_of_3 | multiples_of_5)}")
```

---

## Section 4 — Reflection (10 min)

1. Why can't a Venn diagram serve as a rigorous proof for an identity involving 4 or more sets?

2. In Exercise 3.2, the counterexample search is probabilistic — it might miss a counterexample if it exists but is rare. Why does a *single* explicit counterexample (found by hand or by search) suffice to disprove a universal claim, even though *no* number of successful verifications proves a universal claim?

3. Compare `power_set` (bitmask-based) to a recursive definition of power set (e.g., $\mathcal{P}(\{a\}\cup S) = \mathcal{P}(S) \cup \{s\cup\{a\} : s\in\mathcal{P}(S)\}$). Which resembles the inductive proof from Friday's lecture more closely?

---

## Checkoff Criteria

Show your TA:

- [ ] Exercise 1.2: Venn diagram fully labeled with correct region counts (sum should equal 100)
- [ ] Exercise 2.1 and 2.2: complete element-chasing proofs
- [ ] Exercise 2.3: correct counterexample with computation shown
- [ ] Exercise 2.5: both directions of the biconditional proven
- [ ] `set_tools.py` running: demonstrate power_set on a 3-element set and cartesian_product
- [ ] Section 3.2: counterexample found programmatically, matches hand-found counterexample

---

*Bring `set_tools.py` and `predicate_tools.py` to Lab 5 — we build functions and relations on top of these next.*
