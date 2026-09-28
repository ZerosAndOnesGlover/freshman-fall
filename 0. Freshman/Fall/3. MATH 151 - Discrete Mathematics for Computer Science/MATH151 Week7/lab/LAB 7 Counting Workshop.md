# MATH 151 · Discrete Mathematics for Computer Science
## Lab 7 — Counting Workshop: Classification and Computation
### Wednesday 18 November 2026, 15:00–16:50 · Week 8 | Duration: 2 hours | Covers Week 7 (all three lectures)

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

## Section 2 — Full Worked Problems (40 min)

Solve each completely, showing classification, formula, and arithmetic.

### Exercise 2.1

A pizza place offers 12 toppings. How many pizzas can be made with exactly 4 different toppings?

&nbsp;

&nbsp;

---

### Exercise 2.2

A coin is flipped 10 times. How many outcome sequences have exactly 6 heads?

*(Hint: think of this as choosing WHICH 6 of the 10 flips are heads.)*

&nbsp;

&nbsp;

---

### Exercise 2.3 — Complementary Counting

How many 4-digit PIN codes (0000 to 9999, leading zeros allowed) have **at least one** digit equal to 0?

&nbsp;

&nbsp;

---

### Exercise 2.4 — Stars and Bars

A vending machine stocks 5 types of candy bars. How many ways can it be restocked with 20 candy bars total (repetition of type allowed, order doesn't matter, machine tracks only counts per type)?

&nbsp;

&nbsp;

---

## Section 3 — Verification via Brute Force (40 min)

Counting formulas can be checked by **listing** every case with nested loops and counting them (CS 101 Week 2).

### Exercise 3.1 — Permutations vs Combinations

```python
import math

ordered = 0
unordered = 0
for a in range(1, 6):
    for b in range(1, 6):
        for c in range(1, 6):
            if a != b and b != c and a != c:
                ordered += 1          # an ordered choice of 3 distinct items
            if a < b < c:
                unordered += 1        # each 3-element subset, counted once
print("P(5,3):", ordered, "formula", 5 * 4 * 3)
print("C(5,3):", unordered, "formula", math.comb(5, 3))
```

**Task:** Run it. Why does the condition `a < b < c` count each subset exactly once, and by what factor does
`ordered` exceed `unordered`?

### Exercise 3.2 — "At Least One" via Complementary Counting

How many 3-digit strings over {0, 1, 2, 3, 4} contain at least one 0? Count them directly with three nested loops
(digits `a`, `b`, `c` in `range(5)`, and the test `a == 0 or b == 0 or c == 0`), and compare with the complement
count 5³ − 4³.

### Exercise 3.3 — Pascal's Triangle via Dynamic Programming

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
alt_sum = 0
for k in range(len(row10)):
    alt_sum += (-1)**k * row10[k]
print(f"Alternating sum of row 10: {alt_sum}")
```

---

### Exercise 3.4 — Verify the Hockey Stick Identity

```python
from math import comb

def hockey_stick_lhs(n, r):
    total = 0
    for i in range(r, n + 1):
        total += comb(i, r)
    return total

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

1. In Exercise 3.2, why is it easier to count "no zero" than "at least one zero" directly? Connect this to the logic/set theory parallel discussed in Monday's lecture (De Morgan's Laws).

2. The brute-force enumeration approach (Exercises 3.1–3.2) works fine for small $n$, but why would it become computationally infeasible for, say, choosing 10 items from 50 with combinations? Compute $\binom{50}{10}$ to see how large it gets.

3. Why does Pascal's Rule (used in the DP table construction, Exercise 3.3) avoid the numerical issues that arise from directly computing large factorials like $50!$?

---

## Checkoff Criteria

Show your TA:

- [ ] Section 1: at least 6 of 7 scenarios correctly classified
- [ ] Section 2: all four problems solved completely and correctly
- [ ] Exercises 3.1 and 3.2: loop counts matching the formulas
- [ ] Exercise 3.3: Pascal's Triangle generated, row sums verified
- [ ] Exercise 3.4: Hockey Stick Identity verified across all tested cases

---

*This concludes the Python toolkit for the semester's foundational counting material. Week 8 continues with Advanced Counting — the Pigeonhole Principle and Inclusion–Exclusion — which handle the two cases this week's rules cannot: overlapping categories, and questions that ask whether something must exist rather than how many there are.*
