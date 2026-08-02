# CS 101 Week 2 Reading Guide & Resources
## Control Flow: Conditionals and Iteration

---

## Required Reading

### Guttag — Introduction to Computation and Programming Using Python

**Chapter 2.2 — Branching Programs**
- The `if` statement: syntax and semantics
- Nested conditionals
- The role of indentation

**Chapter 2.3 — While Loops**
- `while` loop syntax and execution model
- Termination and infinite loops
- The decrementing function (termination argument)

**Chapter 2.4 — For Loops and Range**
- `for` loop over sequences
- `range()` in depth
- `break` and `continue`

**Chapter 3.1–3.3 — Numerical Programs**
- Exhaustive enumeration (using loops to search)
- Bisection search (connecting loops to algorithms)
- Newton-Raphson approximation

### What to Focus On

After reading, you should be able to answer:

1. What is the execution order of an `if/elif/else` chain?
2. Given a `while` loop, can you identify when it will terminate? When might it not?
3. What is the difference between `for i in range(5)` and `for i in range(1, 6)`?
4. What is `enumerate()` and why is it better than maintaining a counter manually?
5. What is a loop invariant and why does it matter?

---

## Focused REPL Sessions

### Session A: Understanding Conditionals (15 min)

Work through each one — **predict first, then verify**:

```python
# Short-circuit in conditions
x = None
if x is not None and x > 0:   # Safe — why?
    print("positive")
else:
    print("not positive or None")

# What if we wrote it differently?
if x > 0 and x is not None:   # Is this safe? Test with x = None
    print("positive")

# Chained comparisons
x = 5
print(1 < x < 10)        # True
print(1 < x < 4)         # False
print(x == 5 == x)       # True
print(10 > x > 0)        # True — same as (10 > x) and (x > 0)

# Truthiness in conditions
for val in [0, 1, -1, "", "a", [], [0], None, False, True]:
    if val:
        print(f"{repr(val):>12} → truthy branch")
    else:
        print(f"{repr(val):>12} → falsy branch")
```

### Session B: Tracing While Loops (20 min)

Trace each loop by building the state table before running:

```python
# Loop 1: What does this compute?
n = 12
count = 0
while n > 1:
    if n % 2 == 0:
        n //= 2
    else:
        n = 3*n + 1
    count += 1
print(count)   # Predict before running

# Loop 2: What condition does this check?
n = 49
i = 2
while i * i <= n:
    if n % i == 0:
        print(f"{n} is divisible by {i}")
        break
    i += 1
else:
    print(f"{n} is prime")

# Loop 3: What does this build?
n = 12345
digits = []
while n > 0:
    digits.append(n % 10)
    n //= 10
print(digits)
```

After running: write one sentence for each loop explaining what it computes and why.

### Session C: For Loop Patterns (15 min)

```python
# enumerate
words = ["apple", "banana", "cherry"]
for i, word in enumerate(words):
    print(f"  {i}: {word}")

# zip — what happens when lists have different lengths?
a = [1, 2, 3, 4]
b = ["a", "b", "c"]
for x, y in zip(a, b):   # What happens to the 4?
    print(x, y)

# Accumulator patterns
# Sum of squares of even numbers from 1 to 20:
total = 0
for n in range(1, 21):
    if n % 2 == 0:
        total += n ** 2
print(total)

# Building a string:
vowels = ""
for char in "Hello World":
    if char.lower() in "aeiou":
        vowels += char
print(vowels)

# Nested loop — predict the output count before running:
count = 0
for i in range(5):
    for j in range(i):
        count += 1
print(count)   # What is this counting geometrically?
```

---

## Conceptual Exercises (Paper and Pencil)

Work these without Python. Then verify.

**Exercise 1:** What is the loop invariant for this function?

```python
def count_divisors(n):
    count = 0
    for i in range(1, n + 1):
        if n % i == 0:
            count += 1
    return count
```

State it as: "At the start of iteration i, `count` equals ..."

**Exercise 2:** This loop is supposed to find the first index in `lst` where the value exceeds `threshold`. Find the bug by thinking carefully, not by running it.

```python
def first_above(lst, threshold):
    for i in range(len(lst)):
        if lst[i] > threshold:
            i = i    # bug is somewhere around here
    return i
```

What happens if no element exceeds the threshold? What happens if the first element exceeds it?

**Exercise 3:** Predict the output of this nested loop without running it:

```python
for i in range(1, 4):
    line = ""
    for j in range(1, i + 1):
        line += f"{i*j:3}"
    print(line)
```

---

## Deep Dive: Why Loop Invariants Matter

Loop invariants are not just a theoretical tool — they are how professional engineers reason about correctness in safety-critical systems.

**The seL4 microkernel** (used in defense and aviation systems) has every loop formally verified with invariants using the Isabelle/HOL proof assistant. When a loop is proven correct via its invariant, you have a mathematical guarantee — not just "I tested it and it seemed fine."

**Binary search** — which we'll study in Week 5 — has an invariant that is subtle enough that Jon Bentley famously found that most programmers who claimed to know binary search had bugs in their implementation. The invariant: "if the target is in the array, it must be in `lst[lo:hi+1]`." The classic off-by-one bugs violate this invariant.

For now, practice identifying invariants on the loops you write. Ask yourself after writing every loop: *what is true at the start of every iteration?*

---

## Key Algorithms Introduced This Week

### Euclidean Algorithm (for GCD)

```
gcd(a, b):
    while b ≠ 0:
        a, b = b, a mod b
    return a
```

**Invariant:** `gcd(a, b)` is preserved by the operation `(a,b) → (b, a mod b)`.
**Termination:** `b` strictly decreases each iteration (since `a mod b < b`).
**History:** Described in Euclid's *Elements*, c. 300 BC — one of the oldest algorithms known.

### Sieve of Eratosthenes

**Invariant:** After processing prime `p`, all composite numbers with a prime factor ≤ `p` have been marked.
**Why start at `p²`?** All smaller multiples of `p` have a prime factor < `p` and were already marked.
**Complexity:** O(n log log n) — nearly linear. One of the most efficient algorithms for finding primes up to n.

### Newton-Raphson Method

**Invariant:** The error `|guess² - x|` is positive and (empirically) decreasing.
**Convergence:** Quadratic — the number of correct digits roughly doubles each iteration.
**History:** Isaac Newton (1669), Joseph Raphson (1690). Still the dominant root-finding method in scientific computing.

---

## Common Mistakes This Week

**Mistake 1: Forgetting to update the loop variable**
```python
i = 0
while i < 10:
    print(i)
    # Forgot i += 1 → infinite loop!
```

**Mistake 2: Off-by-one in range**
```python
# "Print 1 to 10":
for i in range(10):     # WRONG: prints 0 to 9
    print(i)
for i in range(1, 11):  # Correct: prints 1 to 10
    print(i)
```

**Mistake 3: Modifying a list while iterating over it**
```python
lst = [1, 2, 3, 4, 5]
for x in lst:
    if x % 2 == 0:
        lst.remove(x)   # WRONG: skips elements!
# Fix: iterate over a copy, or build a new list
lst = [x for x in lst if x % 2 != 0]
```

**Mistake 4: Using `=` in a condition**
```python
while n = 0:   # SyntaxError in Python (intentional)
while n == 0:  # Correct
```

**Mistake 5: Wrong initialization for accumulator**
```python
# Product loop — wrong:
product = 0       # 0 * anything = 0!
for x in lst:
    product *= x
# Fix:
product = 1       # 1 is the neutral element for multiplication
```

**Mistake 6: Condition that's always True / never True**
```python
x = 5
while x > 0 or x < 10:   # This is always True for all x!
    ...
# Did you mean: while 0 < x < 10?
```

---

## Week 2 Self-Test

Can you answer these without notes?

1. What are the three required components of a `while` loop?
2. What is a loop invariant? Give an example.
3. Why does `for i in range(len(lst))` give you indices, while `for x in lst` gives you values?
4. What does `enumerate()` return? Give an example.
5. Write the FizzBuzz output for 13, 14, 15 without running it.
6. What is the Euclidean algorithm? What is its loop invariant?
7. In the sieve of Eratosthenes, why do we start marking at p² (not 2p)?
8. What is the loop invariant for computing the sum of a list?

---

## Preview: Week 3

Week 3 covers **functions, scope, and the call stack** — the most important week of the first half of the course. After Week 3, everything you write will be organized into functions.

Before next Wednesday, think about:
- What is a function, at a fundamental level?
- When you call a function, where do its variables live?
- What does it mean for a function to "return" a value?

---

*CS 101 · Week 2 · Reading Guide · © CSE Department*
