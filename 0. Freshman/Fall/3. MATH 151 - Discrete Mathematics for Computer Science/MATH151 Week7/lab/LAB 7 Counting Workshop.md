# MATH 151 — Discrete Mathematics for Computer Science
## Lab 7 — Counting Workshop: Classification and Computation
### Wednesday, Week 7 | Duration: 2 hours

---

**Lab Objectives:**
1. Practice rapid classification of counting problems into the four scenarios
2. Solve multi-step counting problems by decomposing them correctly
3. Verify counting formulas computationally via brute-force enumeration (for small cases)
4. Build a Python combinatorics toolkit
5. Connect Pascal's Triangle to dynamic programming

**Materials:** Pencil, paper, laptop with Python 3.

---

## Section 1 — Rapid Classification Drill (20 min)

For each scenario, quickly identify: order matters (Y/N)? repetition allowed (Y/N)? Then state which formula applies (don't compute yet).

### Exercise 1.1

**(a)** Choosing 3 flavors of ice cream from 12 for a banana split (each scoop must be different flavor), where the ORDER of scoops on the plate doesn't matter.

**(b)** Choosing 3 flavors of ice cream from 12, where you stack them in a specific order (bottom, middle, top scoop).

**(c)** Rolling a die 5 times and recording the sequence.

**(d)** Choosing a 5-person jury from a pool of 30 (no distinct roles).

**(e)** Assigning each of 5 distinct tasks to one of 3 workers (a worker can get multiple tasks or none).

**(f)** Choosing 4 identical-looking candies from a jar with 6 flavors (you can get multiples of a flavor, only total count of each flavor matters).

**(g)** Ranking your top 3 favorite movies from a list of 10.

---

## Section 2 — Full Worked Problems (45 min)

Solve each completely, showing classification, formula, and arithmetic.

### Exercise 2.1

A pizza place offers 12 toppings. How many pizzas can be made with exactly 4 different toppings?

&nbsp;

&nbsp;

---

### Exercise 2.2

How many ways can a president, vice-president, and secretary be chosen from a club of 20 members (no one holds two positions)?

&nbsp;

&nbsp;

---

### Exercise 2.3

A coin is flipped 10 times. How many outcome sequences have exactly 6 heads?

*(Hint: think of this as choosing WHICH 6 of the 10 flips are heads.)*

&nbsp;

&nbsp;

---

### Exercise 2.4

How many 6-letter strings (from the 26-letter alphabet) contain no repeated letters?

&nbsp;

&nbsp;

---

### Exercise 2.5 — Complementary Counting

How many 4-digit PIN codes (0000 to 9999, leading zeros allowed) have **at least one** digit equal to 0?

&nbsp;

&nbsp;

---

### Exercise 2.6 — Multi-Step

A class has 12 students: 7 CS majors and 5 MATH majors. A team of 4 students is chosen for a project. How many teams have **exactly 2 CS majors and 2 MATH majors**?

&nbsp;

&nbsp;

---

### Exercise 2.7 — Stars and Bars

A vending machine stocks 5 types of candy bars. How many ways can it be restocked with 20 candy bars total (repetition of type allowed, order doesn't matter, machine tracks only counts per type)?

&nbsp;

&nbsp;

---

## Section 3 — Verification via Brute Force (30 min)

For small cases, we can verify counting formulas by literally enumerating all outcomes with Python. This builds trust in the formulas and catches classification errors.

### Exercise 3.1 — Permutations vs Combinations

```python
from itertools import permutations, combinations

items = ['A', 'B', 'C', 'D', 'E']

# Permutations of 3 items from 5
perms = list(permutations(items, 3))
print(f"P(5,3) by formula: {5*4*3}")
print(f"P(5,3) by enumeration: {len(perms)}")

# Combinations of 3 items from 5
combs = list(combinations(items, 3))
print(f"C(5,3) by formula: {5*4*3//(3*2*1)}")
print(f"C(5,3) by enumeration: {len(combs)}")
```

**Task:** Run this and confirm both match. Then print out the first 5 permutations and first 5 combinations to see the structural difference (order preserved vs not).

---

### Exercise 3.2 — Combinations with Repetition

```python
from itertools import combinations_with_replacement

flavors = ['choc', 'van', 'straw']

# Choosing 4 scoops from 3 flavors, repetition allowed, order doesn't matter
selections = list(combinations_with_replacement(flavors, 4))
print(f"Formula C(n+r-1,r) = C(3+4-1,4) = C(6,4): {6*5//2}")
print(f"Enumeration count: {len(selections)}")
for s in selections[:10]:
    print(s)
```

**Task:** Verify the formula matches. This confirms the stars-and-bars derivation from Thursday's lecture.

---

### Exercise 3.3 — Verifying "At Least One" via Complementary Counting

```python
from itertools import product

# 3-digit strings from {0,1,2,3,4}, how many have at least one '0'?
digits = ['0','1','2','3','4']
all_strings = list(product(digits, repeat=3))
total = len(all_strings)

no_zero = [s for s in all_strings if '0' not in s]
at_least_one_zero = total - len(no_zero)

print(f"Total strings: {total}")
print(f"No zero: {len(no_zero)} (should be 4^3 = {4**3})")
print(f"At least one zero: {at_least_one_zero}")

# Direct count for verification
direct_count = len([s for s in all_strings if '0' in s])
print(f"Direct enumeration count: {direct_count}")
print(f"Match: {at_least_one_zero == direct_count}")
```

**Task:** Run and confirm the complementary counting method matches direct enumeration.

---

### Exercise 3.4 — Pascal's Triangle via Dynamic Programming

```python
def pascals_triangle(n_rows):
    triangle = []
    for n in range(n_rows):
        row = [1] * (n+1)
        for r in range(1, n):
            row[r] = triangle[n-1][r-1] + triangle[n-1][r]
        triangle.append(row)
    return triangle

triangle = pascals_triangle(11)
for i, row in enumerate(triangle):
    print(f"n={i}: {row}")

# Verify row sums equal 2^n
for i, row in enumerate(triangle):
    print(f"Row {i} sum: {sum(row)}, 2^{i} = {2**i}, Match: {sum(row)==2**i}")
```

**Task:** Run this and verify all row sums match $2^n$. Then verify the alternating sum of row 10 equals 0:

```python
row10 = triangle[10]
alt_sum = sum((-1)**k * row10[k] for k in range(len(row10)))
print(f"Alternating sum of row 10: {alt_sum}")
```

---

### Exercise 3.5 — Verify the Hockey Stick Identity

```python
from math import comb

def hockey_stick_lhs(n, r):
    return sum(comb(i, r) for i in range(r, n+1))

def hockey_stick_rhs(n, r):
    return comb(n+1, r+1)

for n in range(3, 10):
    for r in range(0, n):
        lhs = hockey_stick_lhs(n, r)
        rhs = hockey_stick_rhs(n, r)
        status = "OK" if lhs == rhs else "MISMATCH"
        print(f"n={n}, r={r}: LHS={lhs}, RHS={rhs} [{status}]")
```

**Task:** Run and confirm all cases show "OK" — this is a computational verification of Friday's Identity 3.

---

## Section 4 — Reflection (5 min)

1. In Exercise 3.3, why is it easier to count "no zero" than "at least one zero" directly? Connect this to the logic/set theory parallel discussed in Monday's lecture (De Morgan's Laws).

2. The brute-force enumeration approach (Exercise 3.1–3.3) works fine for small $n$, but why would it become computationally infeasible for, say, choosing 10 items from 50 with combinations? Compute $\binom{50}{10}$ to see how large it gets.

3. Why does Pascal's Rule (used in the DP table construction, Exercise 3.4) avoid the numerical issues that arise from directly computing large factorials like $50!$?

---

## Checkoff Criteria

Show your TA:

- [ ] Section 1: at least 6 of 7 scenarios correctly classified
- [ ] Section 2: at least 5 of 7 problems solved completely and correctly
- [ ] Exercise 3.1 and 3.2: Python enumeration matching hand formulas
- [ ] Exercise 3.4: Pascal's Triangle DP table generated, row sums verified
- [ ] Exercise 3.5: Hockey Stick Identity verified computationally across all tested cases

---

*This concludes the Python toolkit for the semester's foundational counting material. Week 8 continues with Advanced Counting — the Pigeonhole Principle and Inclusion–Exclusion — which handle the two cases this week's rules cannot: overlapping categories, and questions that ask whether something must exist rather than how many there are.*
