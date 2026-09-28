# MATH 151 · Discrete Mathematics for Computer Science
## Lab 8 — Advanced Counting Workshop: Pigeonhole and Inclusion–Exclusion
### Wednesday 25 November 2026, 15:00–16:50 · Week 9 | Duration: 2 hours | Covers Week 8 (all three lectures)

---

**Bring:** laptop with Python 3. Work in pairs; both submit.

**Goal:** the two techniques of this week are easy to state and hard to *choose between*. This lab
drills the choice, then makes both concrete by computing.

---

## Section 1 — Pigeonhole Practice (30 min)

For each problem, clearly identify the pigeons and pigeonholes before writing the proof.

### Exercise 1.1

Prove: in any group of 40 people, at least 4 were born on the same day of the week.

**Pigeons:** ___________________ **Pigeonholes:** ___________________

**Proof:**

&nbsp;

&nbsp;

---

### Exercise 1.2

Prove: any subset of $\{1,2,\ldots,50\}$ with 26 or more elements must contain two elements that sum to 51.

**Pigeons:** ___________________ **Pigeonholes:** ___________________

**Proof:**

&nbsp;

&nbsp;

&nbsp;

---

### Exercise 1.3

A programmer writes a hash function mapping strings to one of 1000 buckets. If the program processes 1001 distinct strings, prove a collision must occur. Then explain: does this tell you WHICH strings collide? Why or why not?

&nbsp;

&nbsp;

---

### Exercise 1.4 — Harder

Prove: given any 7 distinct integers, there exist two of them whose sum or difference is divisible by 10.

*Hint:* Consider the remainders mod 10 of the 7 integers. Group the possible remainders $\{0,1,\ldots,9\}$ into pairs $\{r, 10-r\}$ (with $\{0\}$ and $\{5\}$ as singleton groups). How many groups are there? What does landing two integers in the same group tell you?

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

---

## Section 2 — Inclusion–Exclusion Practice (30 min)

### Exercise 2.1

In a survey of 200 developers: 120 use Python, 90 use C, 70 use Rust; 45 use Python and C, 30 use
Python and Rust, 25 use C and Rust; 15 use all three.

**(a)** How many use at least one of the three?

**(b)** How many use none?

**(c)** How many use exactly one?

&nbsp;

&nbsp;

---

### Exercise 2.2

How many integers in $\{1,\ldots,1000\}$ are divisible by 3, 5, or 7? How many by none of them?

State each intersection's divisor explicitly before computing — this is where marks are lost.

&nbsp;

&nbsp;

---

### Exercise 2.3 — The Complement Habit

How many 8-character passwords over the 62-character alphanumeric alphabet contain **at least one
digit**?

Compute it two ways: (i) directly, by summing over the number of digits, and (ii) by complement.
Report how long each took you.

&nbsp;

&nbsp;

---

## Section 3 — Choosing the Tool (20 min)

For each statement, say **only** which technique applies — pigeonhole, inclusion–exclusion, plain
multiplication rule, or derangements — and give a one-sentence justification. **Do not solve them.**

| # | Problem | Tool | Why |
|---|---|---|---|
| 1 | Show that among 13 people, two share a birth month | | |
| 2 | Count integers under 200 divisible by 4 or 6 | | |
| 3 | Count 5-letter strings with no repeated letter | | |
| 4 | Show two of any 5 points in a unit square are close together | | |
| 5 | Count ways to return $n$ hats so nobody gets their own | | |
| 6 | Count passwords with at least one digit and one symbol | | |

*(Section 3 is the section students most often skip and most need.)*

---

## Section 4 — Python: Verify by Brute Force (25 min)

### Exercise 4.1 — Pigeonhole Simulator

```python
import math
import random

def simulate_pigeonhole(n_items, n_containers, trials=10):
    """
    Randomly distributes n_items into n_containers and reports
    the maximum container load, over several trials.
    """
    guaranteed_min = math.ceil(n_items / n_containers)
    print(f"Generalized Pigeonhole guarantees: some container has >= {guaranteed_min} items")
    
    for t in range(trials):
        counts = [0] * n_containers
        for _ in range(n_items):
            counts[random.randint(0, n_containers-1)] += 1
        print(f"  Trial {t+1}: max container load = {max(counts)}")
```

**Task:** Run `simulate_pigeonhole(100, 12)` (the birth-month example) several times. Confirm that the observed maximum is always $\geq \lceil 100/12\rceil = 9$, though it's often higher due to randomness.

---

---

### Exercise 4.2 — Derangements by Enumeration

Use the recursive `permutations(lst)` from CS 101 Lecture 15 (copy it into your file). A permutation `p` of
`[0, 1, …, n−1]` is a **derangement** when no `p[i] == i`.

```python
import math

def is_derangement(p):
    for i in range(len(p)):
        if p[i] == i:
            return False
    return True

def derangements_brute(n):
    count = 0
    for p in permutations(list(range(n))):
        if is_derangement(p):
            count += 1
    return count

def derangements_formula(n):
    total = 0
    for k in range(n + 1):
        total += (-1)**k / math.factorial(k)
    return round(math.factorial(n) * total)
```

**Task:** Tabulate both for $n = 1,\ldots,8$ and confirm they agree. Then compute $D_n/n!$ for each $n$ and observe
what it converges to. State the limit and the $n$ beyond which the ratio is stable to three decimal places.

---

## Section 5 — Reflection (5 min)

1. Section 3 asked you to classify without solving. Which two problems did you find hardest to
   classify, and what feature of the wording misled you?

2. The subset-sum argument in Lecture 26 proves two subsets share a sum but gives no way to find
   them. Describe, in your own words, why an existence proof can be easy while the search is hard.

---

## Checkoff Criteria

- [ ] Section 1: all four pigeonhole proofs with pigeons/pigeonholes explicitly identified
- [ ] Section 2: Exercise 2.1 all three parts; 2.2 with intersection divisors stated
- [ ] Section 2.3: both methods attempted, complement shown to be faster
- [ ] Section 3: all six classified with justification
- [ ] Section 4.2: table matches for all $n \le 8$; limit identified as $1/e$
- [ ] Section 5: both reflection questions answered
