# CS 101 · Week 2 Control Flow: Conditionals and Iteration

---

## Contents

```
CS101_Week2/
│
├── README.md                                  ← You are here
│
├── lectures/
│   ├── L07 Conditionals.md                    ← Wed: if/elif/else, decision trees,
│   │                                               guard clauses, De Morgan's Laws
│   ├── L08 While Loops.md                     ← Thu: while loops, loop invariants,
│   │                                               accumulator/search/reduction patterns
│   └── L09 For Loops and Range.md             ← Fri: for loops, range, enumerate,
│                                                   zip, Sieve of Eratosthenes
│
├── lab/
│   ├── LAB 2 Debugging and Loops.md            ← Tue of W3: print debugging, PDB,
│   │                                               Collatz, Sieve, Caesar cipher
│   └── loops_starter.py                       ← Lab starter code with TODOs + test suite
│
├── assignments/
│   ├── QUIZ 2 Week 2 Wednesday.md                  ← In-class quiz (covers Week 1)
│   ├── PS 2 Control Flow.md                    ← Problem Set 2 (due Friday Week 3)
│   └── ps2_starter.py                         ← PS2 starter code with full test suite
│
├── resources/
│   └── Reading Guide Week 2.md                 ← Reading, REPL sessions, common mistakes,
│                                                  loop invariant deep dive
│
└── solutions_instructor/
    └── LAB 2 Solutions.md                      ← Expected answers and marking notes
```

---

## Week 2 at a Glance

**Theme:** Making decisions and repeating actions — the two control structures that, combined with sequence, can express any computation (Böhm-Jacopini theorem).

| Day | Event | Topic |
|-----|-------|-------|
| Wed | Lecture 7 + Quiz 2 | Conditionals: `if/elif/else`, decision trees, guard clauses |
| Thu | Lecture 8 | `while` loops, loop invariants, accumulator/search/reduction patterns |
| Fri | Lecture 9 + PS2 released | `for` loops, `range`, `enumerate`, `zip`, Sieve of Eratosthenes |
| Tue (W3) | Lab 2 (graded) | Debugging with print + PDB, Collatz, Caesar cipher |

---

## Your To-Do List

### Before Wednesday
- [ ] Read Guttag Ch. 2.2 (branching programs)
- [ ] Review your Week 1 answers — Quiz 2 covers Week 1 material

### Wednesday
- [ ] Quiz 2 (10 min — covers types, expressions, Week 1)
- [ ] Notes for L07

### Before Thursday
- [ ] REPL Session A from Reading Guide (conditionals)
- [ ] Read Guttag Ch. 2.3 (while loops)

### Thursday
- [ ] Notes for L08
- [ ] REPL Session B (while loop tracing)

### Tuesday Lab, Week 3 (Required, Graded)
- [ ] Complete all 5 buggy functions in `debug_exercise.py`
- [ ] Implement all 5 functions in `loops_starter.py` (all tests pass)
- [ ] Write loop invariants for 3 functions
- [ ] Complete PDB exercise with convergence analysis
- [ ] TA checkoff

### Friday
- [ ] Notes for L09
- [ ] REPL Session C (for loop patterns)
- [ ] PS2 released — read all parts this weekend

### Weekend
- [ ] Start PS2 — complete B1, B2, B3 before next Tuesday
- [ ] Read Guttag Ch. 3.1–3.3 (numerical programs)

---

## The Central Ideas of Week 2

**1. The Böhm-Jacopini theorem (1966):**
Any computable function can be expressed using only:
- Sequence (do A then B)
- Selection (if condition then A else B)
- Iteration (while condition do A)

You will never need `goto`. This week you have all three.

**2. The if/elif/else chain is a decision tree.**
Only one branch executes. Tests run in order. More specific conditions must come first.

**3. Every correct loop has three components:**
- Initialization: establishes the starting state
- Condition: determines when to continue
- Update: makes progress toward termination

Forgetting the update → infinite loop.

**4. Loop invariants prove correctness.**
A loop invariant is true before the loop, after every iteration, and (combined with the exit condition) proves the function is correct. This is not academic — it's how you *know* your code is right.

**5. `for` loops are for known sequences; `while` for unknown termination.**
`for i in range(n)`: runs exactly n times.
`while condition`: runs until condition becomes False.

**6. The accumulator pattern:**
```python
result = neutral_element   # 0 for sum, 1 for product, [] for lists
for item in collection:
    result = combine(result, item)
```
The invariant: `result` holds the combined value of all items processed so far.

---

## Algorithms Introduced This Week

| Algorithm | What it does | Loop type | Key invariant |
|-----------|-------------|-----------|---------------|
| Digit extraction | Extracts digits via `n % 10`, `n //= 10` | `while n > 0` | Remaining digits are the not-yet-processed prefix |
| Collatz sequence | Apply 3n+1 or n/2 until reaching 1 | `while n != 1` | n > 0 always |
| Euclidean GCD | `a, b = b, a % b` until b = 0 | `while b != 0` | gcd(a,b) is preserved |
| Sieve of Eratosthenes | Mark composites, leave primes | Nested `while` | All composites ≤ p² are marked after processing p |
| Prime factorization | Divide out factors from 2 upward | Nested `while` | n's remaining prime factors are all ≥ current factor |
| Caesar cipher | Shift each letter by k mod 26 | `for char in text` | Characters before index i are already shifted |

---

## Quick Self-Check

Without looking at notes, answer these:

1. What does `for i in range(5, 0, -1)` produce?
2. What does `enumerate(["a","b","c"], start=1)` produce when iterated?
3. What is the neutral element for: (a) addition, (b) multiplication, (c) string concatenation?
4. In the sieve of Eratosthenes, why start marking at `p*p` instead of `2*p`?
5. What is `zip([1,2,3], ["a","b"])` — does it error or truncate?
6. State the loop invariant for `gcd(a, b)`.
7. Write the condition for "n is odd and greater than 100" as a single expression.
8. What does `break` do inside a `while True` loop?

*(Answers: `[5,4,3,2,1]`; `(1,'a'),(2,'b'),(3,'c')`; `0`, `1`, `""`; all smaller multiples already marked by smaller primes; truncates to shorter; `gcd(a,b)==gcd(orig_a,orig_b)`; `n % 2 != 0 and n > 100`; exits the loop immediately)*

---

*CS 101 · Week 2 · © CSE Department*
