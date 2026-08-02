# CS 101 · Problem Set 2
## Control Flow: Conditionals and Iteration

**Released:** Friday, Week 2
**Due:** Friday, Week 3 at 11:59 PM
**Submission:** Upload `ps2.py` and `PS 2 Control Flow.md` to the course portal
**Weight:** Part of the 30% Problem Sets grade

---

## Overview

This problem set covers:
- `if / elif / else` decision trees
- `while` loops with loop invariants
- `for` loops with `range`, `enumerate`, and `zip`
- Loop patterns: accumulator, search, reduction
- Debugging: tracing execution by hand
- Combining conditionals and loops

**Structure:**
- Part A: Written — conceptual questions and trace exercises
- Part B: Python implementation problems
- Part C: Challenge problems (ungraded)

---

## Part A: Written Questions (`PS 2 Control Flow.md`)

### A1: Execution Tracing (8 points)

Trace the following code **by hand** — build the complete state table. Do not run it.

```python
n = 156
result = []

while n > 1:
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
    result.append(n)
```

**(a)** Build the state table for the first 10 iterations:

| Iteration | `n` (before body) | `n % 2 == 0` | `n` (after body) | `result` (after append) |
|-----------|------------------|--------------|-----------------|-------------------------|
| 1 | 156 | ? | ? | ? |
| 2 | ? | ? | ? | ? |
| ... | | | | |

**(b)** State the loop invariant precisely. What is guaranteed to be true at the start of every iteration?

**(c)** The loop modifies `result` by appending. After the loop terminates, what mathematical object does `result` represent?

---

### A2: Loop Invariant Proof (8 points)

Consider this function:

```python
def power(base, exp):
    """Compute base ** exp for non-negative integer exp."""
    result = 1
    i = 0
    while i < exp:
        result *= base
        i += 1
    return result
```

**(a)** State the loop invariant precisely. Use the variables `result`, `i`, `base`, and `exp`.

**(b)** Prove the invariant holds **before the first iteration** (initialization).

**(c)** Prove the invariant is **preserved by the body** — if it holds at the start of an iteration, it holds at the end.

**(d)** Show that the invariant **plus the exit condition** implies the function returns the correct value.

**(e)** Why does the loop always terminate? (What decreases toward the exit condition?)

---

### A3: Conditional Logic (6 points)

**(a)** Simplify this condition using De Morgan's Laws. Show your work step by step.

```python
not (x >= 0 and y >= 0 and z >= 0)
```

**(b)** This code is supposed to find the minimum of three values. It has a logical error. Find it, explain why it's wrong with a counterexample, and write the correct version.

```python
def minimum_of_three(a, b, c):
    if a < b:
        if a < c:
            return a
    elif b < c:
        return b
    else:
        return c
```

Counterexample (a specific input where it gives the wrong answer): ___

**(c)** Rewrite the following nested if-else using guard clauses (early returns):

```python
def validate_score(score):
    if score is not None:
        if isinstance(score, (int, float)):
            if 0 <= score <= 100:
                return "valid"
            else:
                return "out of range"
        else:
            return "wrong type"
    else:
        return "missing"
```

---

### A4: `for` vs `while` (4 points)

For each task below, state which loop type (`for` or `while`) is more appropriate and why:

**(a)** Processing each character in a user-supplied string.

**(b)** Reading lines from a file until you find one that starts with "ERROR".

**(c)** Computing the 100th Fibonacci number.

**(d)** Iterating over a dictionary's key-value pairs to build a report.

---

## Part B: Python Implementation (`ps2.py`)

### B1: Number Analysis (12 points)

Write a function `analyze_number(n)` that takes a positive integer and returns a dictionary with these keys:

- `"digits"` — list of digits (most significant first): `analyze_number(1234)["digits"] == [1, 2, 3, 4]`
- `"digit_sum"` — sum of digits: `10`
- `"digit_product"` — product of digits: `24`
- `"is_palindrome"` — True if the digit sequence is a palindrome: `analyze_number(121)["is_palindrome"] == True`
- `"largest_digit"` — the largest single digit: `4`
- `"num_digits"` — count of digits: `4`
- `"digital_root"` — repeatedly sum the digits until a single digit remains: `analyze_number(1234)["digital_root"] == 1` (1234 → 1+2+3+4 = 10 → 1+0 = 1)

Use a `while` loop to extract digits. Do **not** convert to string.

Example:
```python
analyze_number(9875)
# → {
#     "digits": [9, 8, 7, 5],
#     "digit_sum": 29,
#     "digit_product": 2520,
#     "is_palindrome": False,
#     "largest_digit": 9,
#     "num_digits": 4,
#     "digital_root": 2    (29 → 11 → 2)
#   }
```

---

### B2: Sequence Generators (14 points)

Implement each function. Use the specified loop types.

**(a)** `fibonacci_sequence(n)` — return a list of the first `n` Fibonacci numbers.
- F(0)=0, F(1)=1, F(k)=F(k-1)+F(k-2)
- `fibonacci_sequence(8)` → `[0, 1, 1, 2, 3, 5, 8, 13]`
- Use a `for` loop
- State the loop invariant in a comment

**(b)** `geometric_sequence(first, ratio, n)` — return a list of `n` terms.
- `geometric_sequence(2, 3, 5)` → `[2, 6, 18, 54, 162]`
- Use a `for` loop

**(c)** `convergents_of_sqrt2(n)` — the continued fraction approximations of √2.
- The sequence of fractions: 1/1, 3/2, 7/5, 17/12, 41/29, ...
- Each term: if previous numerator=p, denominator=q → next numerator=p+2q, denominator=p+q
- Return a list of `n` `(numerator, denominator)` tuples
- `convergents_of_sqrt2(5)` → `[(1,1), (3,2), (7,5), (17,12), (41,29)]`
- Verify: each fraction approximates √2 ≈ 1.41421...

**(d)** `look_and_say(n)` — generate the first `n` terms of the Look-and-Say sequence.
- 1, 11, 21, 1211, 111221, 312211, ...
- Each term: describe the previous term ("one 1" → "11", "two 1s" → "21", ...)
- Return a list of strings: `['1', '11', '21', '1211', '111221']` for n=5
- Hint: use a `while` loop with a counter tracking runs of identical digits

---

### B3: Pattern Printer (10 points)

Write functions that print ASCII patterns using nested loops. Each function takes an integer `n` as the size parameter.

**(a)** `right_triangle(n)` — prints a right triangle of `*`:
```
*
**
***
****
*****
```

**(b)** `diamond(n)` — prints a diamond (n is the half-height):
```
  *
 ***
*****
 ***
  *
```
(for n=3)

**(c)** `multiplication_table(n)` — prints a formatted multiplication table:
```
    1    2    3    4    5
    2    4    6    8   10
    3    6    9   12   15
    4    8   12   16   20
    5   10   15   20   25
```
Use f-string formatting with field width to align columns.

**(d)** `number_spiral(n)` — print numbers 1..n² in a clockwise spiral pattern.
For n=4:
```
 1  2  3  4
12 13 14  5
11 16 15  6
10  9  8  7
```
This is the hardest pattern. Approach: fill a 2D grid array, then print it. Track direction (right, down, left, up) and turn when you hit a wall or already-filled cell.

---

### B4: String Processing (10 points)

**(a)** `word_frequency(text)` — without using dictionaries (we haven't covered them), find and return the most frequently occurring word in a text string. If there is a tie, return the first one alphabetically.
- Convert to lowercase, split on whitespace
- Use nested loops to count occurrences
- `word_frequency("the cat sat on the mat the cat")` → `"the"`

**(b)** `run_length_encode(s)` — implement run-length encoding.
- Compress consecutive identical characters by counting runs
- `run_length_encode("aaabbbccddddee")` → `"3a3b2c4d2e"`
- `run_length_encode("abcd")` → `"1a1b1c1d"` (or `"abcd"` — your choice, but be consistent)

**(c)** `run_length_decode(s)` — reverse of above.
- `run_length_decode("3a3b2c4d2e")` → `"aaabbbccddddee"`

**(d)** `is_pangram(sentence)` — return True if the sentence contains every letter of the alphabet at least once.
- `is_pangram("The quick brown fox jumps over the lazy dog")` → `True`
- Case-insensitive

---

### B5: Number Theory (12 points)

**(a)** `gcd(a, b)` — compute the greatest common divisor using the Euclidean algorithm.
- Euclidean algorithm: `gcd(a, b) = gcd(b, a % b)` until `b == 0`
- Use a `while` loop (not recursion — we'll do recursion in Week 4)
- Prove correctness with a loop invariant: the invariant is `gcd(a, b)` is preserved
- `gcd(48, 18)` → `6`

**(b)** `lcm(a, b)` — least common multiple.
- `lcm(a, b) = (a * b) // gcd(a, b)`
- One line using your `gcd` function

**(c)** `is_perfect(n)` — True if n equals the sum of its proper divisors.
- Proper divisors of 6: 1, 2, 3 → sum = 6 → perfect!
- `is_perfect(6)` → True, `is_perfect(28)` → True, `is_perfect(12)` → False
- Only check divisors up to `n//2` (no divisor larger than half can divide n)

**(d)** `prime_factorization(n)` — return a list of prime factors (with repetition, sorted).
- `prime_factorization(360)` → `[2, 2, 2, 3, 3, 5]`
- `prime_factorization(13)` → `[13]`
- Use a `while` loop: start with factor=2, divide out completely, increment factor

**(e)** `goldbach(n)` — Goldbach's conjecture: every even integer > 2 is the sum of two primes.
- Given an even integer n > 2, find and return one pair (p, q) where p + q = n and both are prime.
- First write a helper `is_prime(k)` (trial division up to `√k` is sufficient), then search upward from p = 2 for the first p where both `p` and `n - p` are prime.
- `goldbach(28)` → `(5, 23)` or `(11, 17)` or another valid pair

---

### B6: Statistical Analysis (10 points)

Write functions to compute statistics on a list of numbers, using **only loops and conditionals** (no built-in `sum`, `min`, `max`, `sorted`).

**(a)** `stats(data)` — return a dictionary with:
- `"count"`: number of elements
- `"sum"`: total
- `"mean"`: arithmetic mean (float)
- `"min"`: minimum value
- `"max"`: maximum value
- `"range"`: max - min
- `"variance"`: population variance = mean of squared deviations from mean
- `"std_dev"`: square root of variance

**(b)** `median(data)` — return the median of a list.
- You may use Python's built-in `sorted()` here (since we haven't covered sorting yet)
- For even-length lists, return the average of the two middle values

**(c)** `mode(data)` — return the most frequently occurring value.
- If there are multiple modes, return the smallest one
- Use nested loops to count frequencies (no dictionaries)

**(d)** Demonstrate your functions on this dataset:
```python
data = [4, 7, 13, 2, 7, 3, 9, 7, 1, 5, 8, 7, 6, 4, 11]
```
Print a formatted statistics report.

---

### B7: Text Adventure Engine (12 points)

Build the core of a text-based adventure game using a `while True` loop.

The game has:
- A map of rooms (as a list of dictionaries — but since we haven't covered dicts formally, use parallel lists or a simple structure)
- An inventory system
- Basic commands: `go [direction]`, `look`, `take [item]`, `drop [item]`, `inventory`, `help`, `quit`

**Simplification:** use three parallel lists to represent the world:
```python
# Room names, descriptions, and item in each room (or None)
room_names = ["Cave Entrance", "Torch Room", "Treasure Chamber", "Exit"]
room_descs = [
    "You stand at the entrance of a dark cave.",
    "A torch hangs on the wall, casting flickering light.",
    "Gold coins glitter in the dim light.",
    "You see daylight ahead. The exit!"
]
room_items = ["rope", "torch", None, None]  # item in each room, or None

# Connections: room_exits[i] = (north_idx, south_idx, east_idx, west_idx)
# Use -1 for no exit in that direction
room_exits = [
    (-1, -1, 1, -1),   # Cave Entrance: east → Torch Room
    (-1, -1, 2, 0),    # Torch Room: east → Treasure Chamber, west → Cave Entrance
    (-1, -1, 3, 1),    # Treasure Chamber: east → Exit, west → Torch Room
    (-1, -1, -1, 2),   # Exit: west → Treasure Chamber
]
```

**Requirements:**
- `look`: print the current room name, description, and any item present
- `go north/south/east/west`: move to adjacent room or print "No exit that way"
- `take [item]`: pick up item if it's in current room, add to inventory
- `drop [item]`: drop item from inventory into current room
- `inventory`: list carried items
- `help`: list commands
- `quit`: exit the game

**Win condition:** reach the Exit (room 3) while carrying the torch.
**Lose condition:** none (keep playing until quit or win).

Use a `while True` loop for the game loop. Parse commands with `str.split()`. Handle invalid input gracefully.

---

## Grading Rubric

| Problem | Points | Key Criteria |
|---------|--------|--------------|
| A1 Tracing | 8 | Complete table, correct invariant, correct description |
| A2 Invariant proof | 8 | All 5 parts: statement, init, preservation, correctness, termination |
| A3 Conditionals | 6 | De Morgan correct, counterexample valid, guard clauses clean |
| A4 for vs while | 4 | Correct choice with reasoning |
| B1 Number analysis | 12 | All keys correct, uses while loop, no string conversion |
| B2 Sequences | 14 | All four functions correct with invariants for (a) and (c) |
| B3 Patterns | 10 | All patterns correct, formatted properly |
| B4 String processing | 10 | All four functions correct, handles edge cases |
| B5 Number theory | 12 | gcd with invariant proof, all functions correct |
| B6 Statistics | 10 | All statistics correct, no prohibited built-ins |
| B7 Text adventure | 12 | All commands work, win condition correct, input validated |
| **Total** | **106** | |
| Style bonus | up to 5 | Clear names, invariant comments, consistent formatting |

---

## Part C: Challenge Problems (Ungraded)

**C1: Luhn Algorithm**
Credit card numbers are validated using the Luhn algorithm:
1. Double every second digit from the right (positions 2, 4, 6, ...)
2. If the doubled value > 9, subtract 9
3. Sum all digits
4. If the sum is divisible by 10, the number is valid

Implement `luhn_check(card_number_str)` → True/False. Test with real card number patterns (use test numbers — Visa: 4532015112830366, Mastercard: 5425233430109903).

**C2: Conway's Game of Life (one step)**
Given a 2D grid (list of lists of booleans representing alive/dead cells), compute the next generation:
- A live cell with 2 or 3 live neighbors survives
- A dead cell with exactly 3 live neighbors becomes alive
- All other cells die or stay dead

Implement `life_step(grid)` → new_grid. Use a `for` loop over rows and columns, counting neighbors with another pair of loops.

**C3: Roman Numerals**
Implement `to_roman(n)` (integer → Roman numeral string) and `from_roman(s)` (Roman numeral string → integer). Handle 1–3999.

**C4: Anagram Detector**
Without using dictionaries, sets, or sorting: implement `is_anagram(s1, s2)` that returns True if s1 and s2 are anagrams of each other (contain the same characters with the same frequencies). Use only loops and string operations.

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Totals follow the Grading Rubric above (106 + up to 5 style).

### ⚠️ Errata — CORRECTED in the student-facing text above

Both defects **have now been fixed in this document**. Recorded here for the change log.

| Location | Was (wrong) | Now |
|---|---|---|
| B1, `digital_root` bullet | Shipped an unedited authoring artifact — "`7` (for 1234: 1+2+3+4=10, 1+0=1… **wait**: 1234→10→1, so digital root=1)" — showing both a wrong value (`7`) and the author correcting themselves mid-sentence. | Rewritten cleanly; correct value for 1234 is **1**. The code-block example (`9875` → `2`) was already right. |
| B5(e) Goldbach | Said "Use your **sieve** function", but no sieve was ever assigned in PS2 — a dangling requirement students could not satisfy. | Reworded to specify an `is_prime(k)` helper by trial division. A sieve remains perfectly acceptable — accept either. |

Accept work from students holding a pre-correction copy, including any sieve they wrote to satisfy the old B5(e) wording.

---

### Part A — Written (26 points)

**A1 Execution Tracing (8 pts).** Starting `n = 156`:

| Iter | `n` before | `n % 2 == 0` | `n` after | `result` after append |
|---|---|---|---|---|
| 1 | 156 | True | 78 | [78] |
| 2 | 78 | True | 39 | [78, 39] |
| 3 | 39 | False | 118 | [78, 39, 118] |
| 4 | 118 | True | 59 | […, 59] |
| 5 | 59 | False | 178 | […, 178] |
| 6 | 178 | True | 89 | […, 89] |
| 7 | 89 | False | 268 | […, 268] |
| 8 | 268 | True | 134 | […, 134] |
| 9 | 134 | True | 67 | […, 67] |
| 10 | 67 | False | 202 | […, 202] |

**(b)** Invariant: *at the start of every iteration `n` is an integer with `n > 1`, and `result` holds exactly the sequence of values `n` has taken since the start, in order, excluding the initial 156.*
**(c)** `result` is the **Collatz (hailstone) trajectory** of 156, excluding the seed. The full run reaches 1 after **36 steps**, peaking at **304**.

*Grading: 5 pts table (½ per row). 2 pts invariant — must mention both `n > 1` and what `result` accumulates. 1 pt naming Collatz/hailstone.*
*Note: whether the loop terminates for **every** starting `n` is the open Collatz conjecture. Students who observe this deserve style credit; students who claim to have proved termination in general have made an error.*

**A2 Loop Invariant Proof (8 pts).** For `power(base, exp)`:

- **(a) Invariant:** `result == base ** i` and `0 <= i <= exp`.
- **(b) Initialization:** before iteration 1, `result = 1` and `i = 0`; `base ** 0 == 1`. ✓
- **(c) Preservation:** assume `result == base ** i` at the top. The body sets `result' = result * base == base**i * base == base**(i+1)` and `i' = i + 1`, so `result' == base ** i'`. ✓
- **(d) Correctness:** the loop exits when `i < exp` is false, i.e. `i == exp` (it cannot overshoot: `i` rises by exactly 1 and starts ≤ `exp`). Combined with the invariant, `result == base ** exp`. ✓
- **(e) Termination:** `exp - i` is a non-negative integer that strictly decreases by 1 each iteration, so it reaches 0 in finitely many steps.

*Grading: 2 pts (a) — must include the bound on `i`, not just the equation. 1 pt (b). 2 pts (c). 2 pts (d) — must argue `i == exp` exactly. 1 pt (e) naming the decreasing quantity.*
*Common error: stating the invariant as `result == base ** exp`, which is the postcondition, not an invariant — it is false during the loop. Award 0 for (a) in that case.*

**A3 Conditional Logic (6 pts).**

**(a)** `not (x >= 0 and y >= 0 and z >= 0)` → distribute: `not(x>=0) or not(y>=0) or not(z>=0)` → **`x < 0 or y < 0 or z < 0`**.

**(b)** The bug is the mismatched `if`/`elif` nesting: when `a < b` is **true** but `a < c` is **false**, the inner `if` fails and control falls off the end of the function — returning `None` implicitly. The `elif`/`else` belong to the *outer* `if`, so they are unreachable in that path.
- **Counterexample: `minimum_of_three(2, 3, 1)`** → returns `None`; correct answer is `1`.

```python
def minimum_of_three(a, b, c):
    if a <= b and a <= c:
        return a
    if b <= c:
        return b
    return c
```

**(c)** Guard-clause rewrite:

```python
def validate_score(score):
    if score is None:
        return "missing"
    if not isinstance(score, (int, float)):
        return "wrong type"
    if not (0 <= score <= 100):
        return "out of range"
    return "valid"
```

*Grading: 2 pts (a) — full De Morgan working, not just the answer. 2 pts (b) — 1 for identifying the fall-through/`None`, 1 for a **valid** counterexample. Verify their counterexample actually fails; `(1,2,3)` and `(3,2,1)` both work correctly in the buggy version and earn 0. 2 pts (c) — must invert each condition and return early; deduct 1 if any `else` remains.*

**A4 `for` vs `while` (4 pts).** 1 pt each.
- **(a)** `for` — the string is a finite known iterable; iterate `for ch in s`.
- **(b)** `while` — the stopping point is data-dependent and unknown in advance (though `for line in f:` with `break` is also fully acceptable and arguably more Pythonic — accept either **with** the reasoning).
- **(c)** `for` — exactly 100 iterations, a known count.
- **(d)** `for` — iterating a finite collection: `for k, v in d.items()`.

*Grade the reasoning, not the label. The distinction being tested is "known iteration count / known iterable" (→`for`) vs "condition-driven, unknown count" (→`while`).*

---

### Part B — Coding (80 points)

**B1 Number Analysis (12 pts).** Verified: `analyze_number(9875)` → `{'digits': [9,8,7,5], 'digit_sum': 29, 'digit_product': 2520, 'is_palindrome': False, 'largest_digit': 9, 'num_digits': 4, 'digital_root': 2}`.

```python
def analyze_number(n):
    digits, t = [], n
    while t > 0:
        digits.append(t % 10)
        t //= 10
    digits.reverse()                     # extraction yields least-significant first
    if n == 0: digits = [0]              # edge case: the loop never runs
    dsum = 0
    for d in digits: dsum += d
    dprod = 1
    for d in digits: dprod *= d
    largest = digits[0]
    for d in digits:
        if d > largest: largest = d
    dr = n                               # digital root: sum repeatedly until < 10
    while dr >= 10:
        s, t = 0, dr
        while t > 0: s += t % 10; t //= 10
        dr = s
    return {"digits": digits, "digit_sum": dsum, "digit_product": dprod,
            "is_palindrome": digits == digits[::-1], "largest_digit": largest,
            "num_digits": len(digits), "digital_root": dr}
```

*Grading: 2 pts each for digits/digit_sum/digit_product/largest_digit/num_digits/digital_root, minus 2 overall if `str(n)` is used anywhere (the problem forbids string conversion). `is_palindrome` folded into the digits point.*
*Common errors: (a) forgetting `.reverse()` — digits come out backwards, which silently still passes `is_palindrome` and `digit_sum`; check the `digits` key explicitly. (b) `digit_product` initialised to 0 → always 0. (c) `n = 0` infinite/empty edge case.*
*Shortcut worth noting: digital root is `1 + (n-1) % 9` for `n > 0`. Accept it, but only with the loop also present or an explanation — the problem asks for repeated summing.*

**B2 Sequence Generators (14 pts).** All four verified against the spec's examples.

```python
def fibonacci_sequence(n):
    out, a, b = [], 0, 1
    for _ in range(n):
        # invariant: a == F(k), b == F(k+1) where k = len(out)
        out.append(a); a, b = b, a + b
    return out                            # (8) -> [0,1,1,2,3,5,8,13]

def geometric_sequence(first, ratio, n):
    out, term = [], first
    for _ in range(n):
        out.append(term); term *= ratio
    return out                            # (2,3,5) -> [2,6,18,54,162]

def convergents_of_sqrt2(n):
    out, p, q = [], 1, 1
    for _ in range(n):
        # invariant: p/q is the k-th convergent; p**2 - 2*q**2 == ±1
        out.append((p, q)); p, q = p + 2*q, p + q
    return out                            # (5) -> [(1,1),(3,2),(7,5),(17,12),(41,29)]

def look_and_say(n):
    out, cur = [], "1"
    for _ in range(n):
        out.append(cur)
        nxt, i = "", 0
        while i < len(cur):
            j = i
            while j < len(cur) and cur[j] == cur[i]: j += 1
            nxt += str(j - i) + cur[i]
            i = j
        cur = nxt
    return out                            # (5) -> ['1','11','21','1211','111221']
```

Convergents approximate √2 ≈ 1.414214 as `1.0, 1.5, 1.4, 1.416667, 1.413793` — alternating above/below, which is the signature of a continued fraction.

*Grading: 3 pts each for (a),(b),(d); 4 pts for (c) (harder recurrence). Invariant comments required for (a) and (c) — deduct 1 each if absent, per the rubric.*
*Common errors: (a) `fibonacci_sequence(0)` returning `[0]` instead of `[]`, or `(1)` returning `[0,1]`. (d) building the count by scanning the whole string rather than runs, giving `'1211'` → `'111221'` correct but `'111221'` → wrong; check term 6 is `'312211'`.*

**B3 Pattern Printer (10 pts).** All verified.

```python
def right_triangle(n):
    for i in range(1, n+1): print("*" * i)

def diamond(n):                                   # n = half-height
    for i in range(1, n+1):    print(" "*(n-i) + "*"*(2*i-1))
    for i in range(n-1, 0, -1): print(" "*(n-i) + "*"*(2*i-1))

def multiplication_table(n):
    for i in range(1, n+1):
        print("".join(f"{i*j:5d}" for j in range(1, n+1)))

def number_spiral(n):
    g = [[0]*n for _ in range(n)]
    r = c = 0; dr, dc = 0, 1                      # start heading right
    for v in range(1, n*n+1):
        g[r][c] = v
        nr, nc = r+dr, c+dc
        if not (0 <= nr < n and 0 <= nc < n and g[nr][nc] == 0):
            dr, dc = dc, -dr                      # turn clockwise
            nr, nc = r+dr, c+dc
        r, c = nr, nc
    for row in g: print("".join(f"{v:3d}" for v in row))
```

`number_spiral(4)` reproduces the spec's grid exactly.

*Grading: 2 pts each for (a),(b),(c); 4 pts for (d). For (d) award 2 if the grid is filled correctly but printed unaligned.*
*The clockwise turn is `(dr, dc) = (dc, -dr)`. The counter-clockwise version `(-dc, dr)` is the most common wrong turn — it produces a valid-looking but mirrored spiral. Check against the expected grid, not just "looks spiral-ish".*

**B4 String Processing (10 pts).** Verified: `word_frequency(...)` → `"the"`; `run_length_encode("aaabbbccddddee")` → `"3a3b2c4d2e"`; decode round-trips; pangram `True`.

```python
def run_length_encode(s):
    out, i = "", 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]: j += 1
        out += str(j - i) + s[i]
        i = j
    return out

def run_length_decode(s):
    out, i = "", 0
    while i < len(s):
        j = i
        while j < len(s) and s[j].isdigit(): j += 1   # multi-digit runs
        out += s[j] * int(s[i:j])
        i = j + 1
    return out
```

*Grading: 2 pts (a), 3 pts (b), 3 pts (c), 2 pts (d).*
*Critical check on (c): a decoder that steps two characters at a time (`out += s[i+1] * int(s[i]); i += 2`) handles only single-digit counts. On `"12a"` it reads count `1`, char `'2'`, then runs off the end and raises `IndexError` — it does not merely mis-decode, it crashes. Deduct 1. Test with `run_length_encode("a"*12)` → `"12a"` and require a clean round-trip.*
*(a) ties must break alphabetically — test `"b b a a"` → `"a"`.*

**B5 Number Theory (12 pts).** Verified: `gcd(48,18)=6`, `is_perfect(6)=is_perfect(28)=True`, `is_perfect(12)=False`, `prime_factorization(360)=[2,2,2,3,3,5]`, `prime_factorization(13)=[13]`, `goldbach(28)=(5,23)`.

```python
def gcd(a, b):
    while b != 0:            # invariant: gcd(a,b) is unchanged by the swap below
        a, b = b, a % b
    return a

def lcm(a, b): return (a * b) // gcd(a, b)

def prime_factorization(n):
    out, f = [], 2
    while f * f <= n:                 # only trial-divide up to sqrt(n)
        while n % f == 0:
            out.append(f); n //= f
        f += 1
    if n > 1: out.append(n)           # whatever survives is prime
    return out
```

**gcd invariant (required by the rubric):** *`gcd(a, b)` equals the gcd of the original pair at the top of every iteration.* This holds because any common divisor of `a` and `b` also divides `a % b = a − ⌊a/b⌋·b`, and conversely. Termination: `b` strictly decreases and is a non-negative integer.

*Grading: 3 pts (a) including the invariant statement — code alone earns 2. 1 pt (b). 2 pts (c). 3 pts (d). 3 pts (e).*
*Common errors: `prime_factorization` looping `f` to `n` instead of `√n` (correct but O(n) — accept, note inefficiency); forgetting the trailing `if n > 1` so `pf(13)` returns `[]`. For `is_perfect`, `range(1, n//2+1)` is the specified bound; `range(1,n)` also works.*

**B6 Statistical Analysis (10 pts).** On `data = [4,7,13,2,7,3,9,7,1,5,8,7,6,4,11]`:

| Statistic | Value |
|---|---|
| count | 15 |
| sum | 94 |
| mean | 6.2667 |
| min | 1 |
| max | 13 |
| range | 12 |
| variance (population) | 9.9289 |
| std_dev | 3.1510 |
| median | 7 |
| mode | 7 |

*Grading: 6 pts for `stats` (1 per non-trivial field), 2 pts median (must handle even length), 2 pts mode (must break ties toward the smallest).*
*The problem specifies **population** variance (divide by `n`). A student dividing by `n−1` (sample variance) gets 10.6381 — deduct 1 and note the distinction rather than marking it wholly wrong; it is a real and defensible statistic, just not the one specified.*
*Verify no banned built-ins: `sum`, `min`, `max`, `sorted` are prohibited except `sorted` inside `median`, which the problem explicitly allows.*

**B7 Text Adventure Engine (12 pts).** Core loop:

```python
inventory, current = [], 0
DIRS = {"north": 0, "south": 1, "east": 2, "west": 3}

while True:
    raw = input("> ").strip().lower()
    if not raw: continue
    parts = raw.split()
    verb, arg = parts[0], (" ".join(parts[1:]) if len(parts) > 1 else None)

    if verb == "quit":
        print("Goodbye."); break
    elif verb == "help":
        print("go <dir>, look, take <item>, drop <item>, inventory, help, quit")
    elif verb == "look":
        print(room_names[current]); print(room_descs[current])
        if room_items[current]: print(f"You see: {room_items[current]}")
    elif verb == "inventory":
        print("Carrying:", ", ".join(inventory) if inventory else "nothing")
    elif verb == "go":
        if arg not in DIRS:
            print("Go where?")
        else:
            dest = room_exits[current][DIRS[arg]]
            if dest == -1:
                print("No exit that way")
            else:
                current = dest
                print(f"You move {arg} to {room_names[current]}.")
                if current == 3 and "torch" in inventory:
                    print("You escape into daylight. YOU WIN!"); break
    elif verb == "take":
        if arg and room_items[current] == arg:
            inventory.append(arg); room_items[current] = None
            print(f"Taken: {arg}")
        else:
            print("That isn't here.")
    elif verb == "drop":
        if arg in inventory:
            inventory.remove(arg); room_items[current] = arg
            print(f"Dropped: {arg}")
        else:
            print("You aren't carrying that.")
    else:
        print("I don't understand. Try 'help'.")
```

*Grading: 2 pts loop + parsing + graceful unknown-command handling. 1 pt each for look / inventory / help / take / drop (5). 2 pts `go` with the `-1` no-exit check. 3 pts win condition — must require **both** `current == 3` **and** the torch.*
*Common errors: (a) win triggers on reaching room 3 regardless of inventory — this is the single most-missed requirement, deduct all 3; (b) crash on bare `go` with no argument (unhandled `IndexError`) — deduct 1; (c) `drop` overwriting an item already on the floor, silently destroying it — mention, deduct only if it loses the torch and makes the game unwinnable.*

---

### Part C — Challenge (ungraded)

- **C1 Luhn.** Both sample numbers validate. Double every second digit **from the right** (0-indexed from the right: positions 1,3,5…); subtract 9 if >9; total ≡ 0 (mod 10).
- **C2 Life.** Count the 8 neighbours with bounds guards; build a **new** grid — mutating in place corrupts later cells in the same generation, the classic bug.
- **C3 Roman.** Greedy descending value/symbol table including the six subtractive pairs (CM, CD, XC, XL, IX, IV) makes `to_roman` a short loop.
- **C4 Anagram.** Without dict/set/sort: for each of the 26 letters count occurrences in both strings and compare — O(26·n).

---

*CS 101 · Week 2 · Problem Set 2 · Due Friday Week 3 · © CSE Department*
