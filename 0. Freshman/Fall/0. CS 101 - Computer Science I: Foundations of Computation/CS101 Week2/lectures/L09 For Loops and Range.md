# CS 101 · Lecture 9 (Week 2, Lecture 3)
## Control Flow III: `for` Loops, `range`, and Tracing Execution

**Week 2 · Friday**
*"The for loop is not syntactic sugar — it is a contract between the programmer and the data structure." — David Beazley*

---

## 0. Two Flavors of Iteration

Python has two loop constructs:

- **`while`** — iterate as long as a condition holds; you control when it stops
- **`for`** — iterate over a sequence of values; the sequence controls when it stops

The `for` loop is Python's most-used construct. It is cleaner, less error-prone, and more idiomatic than `while` for any task involving traversal of a known sequence.

---

## 1. The `for` Loop — Anatomy

```python
for variable in iterable:
    body
```

- `iterable` — any object that can produce a sequence of values (list, string, range, tuple, dict, file, ...)
- `variable` — a name that is bound to each successive value from the iterable
- `body` — executed once for each value

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit.upper())
```

Output:
```
APPLE
BANANA
CHERRY
```

**What the for loop does internally:**
1. Ask the iterable for its first value; bind it to `fruit`
2. Execute the body
3. Ask for the next value; bind it to `fruit`
4. Execute the body
5. Repeat until the iterable is exhausted

This is the **iterator protocol** — one of Python's most powerful design patterns. Any object that implements it can be used in a `for` loop. We'll build our own iterators in a later course.

---

## 2. `range()` — The Integer Sequence Generator

`range` produces sequences of integers on demand without storing them in memory.

```python
range(stop)           # 0, 1, 2, ..., stop-1
range(start, stop)    # start, start+1, ..., stop-1
range(start, stop, step)  # start, start+step, start+2*step, ..., < stop
```

```python
# Count from 0 to 4:
for i in range(5):
    print(i)    # 0 1 2 3 4

# Count from 1 to 10:
for i in range(1, 11):
    print(i)    # 1 2 3 4 5 6 7 8 9 10

# Even numbers from 0 to 20:
for i in range(0, 21, 2):
    print(i)    # 0 2 4 6 8 10 12 14 16 18 20

# Count DOWN from 10 to 1:
for i in range(10, 0, -1):
    print(i)    # 10 9 8 7 6 5 4 3 2 1

# Negative step with range:
for i in range(5, -1, -1):
    print(i)    # 5 4 3 2 1 0
```

**`range` is lazy** — it generates values one at a time, not all at once. `range(1_000_000_000)` uses essentially zero memory.

### Why `range(n)` starts at 0

0-based indexing matches how arrays work at the hardware level (memory offset from the start). When you iterate `for i in range(len(lst))`, index `i` directly accesses `lst[i]` — no arithmetic required. This is not arbitrary — it is optimal.

---

## 3. Iterating Over Sequences

The `for` loop works on any sequence:

```python
# Over a string (character by character):
for char in "hello":
    print(char)     # h, e, l, l, o

# Over a list:
numbers = [1, 4, 9, 16, 25]
for n in numbers:
    print(n, "→", n ** 0.5)

# Over a tuple:
for x, y in [(1, 2), (3, 4), (5, 6)]:
    print(f"x={x}, y={y}")   # Tuple unpacking in the loop variable!

# Over a dictionary (iterates over keys by default):
grades = {"Alice": 92, "Bob": 85, "Charlie": 78}
for name in grades:
    print(f"{name}: {grades[name]}")

# Over dict items (key-value pairs):
for name, score in grades.items():
    print(f"{name}: {score}")
```

---

## 4. Essential Loop Utilities

### `enumerate()` — index and value together

When you need both the index and the value:

```python
items = ["alpha", "beta", "gamma"]

# Without enumerate — error-prone:
i = 0
for item in items:
    print(i, item)
    i += 1

# With enumerate — clean and Pythonic:
for i, item in enumerate(items):
    print(i, item)

# Start from 1 instead of 0:
for i, item in enumerate(items, start=1):
    print(f"{i}. {item}")
```

Output:
```
1. alpha
2. beta
3. gamma
```

**Use `enumerate` whenever you need the index.** Never write `i = 0` then `i += 1` inside a `for` loop.

### `zip()` — iterate over multiple sequences simultaneously

```python
names  = ["Alice", "Bob", "Charlie"]
scores = [92, 85, 78]
grades = ["A", "B", "C"]

for name, score, grade in zip(names, scores, grades):
    print(f"{name}: {score} ({grade})")
```

Output:
```
Alice: 92 (A)
Bob: 85 (B)
Charlie: 78 (C)
```

`zip` stops at the shortest sequence. Use `itertools.zip_longest` if you need to handle sequences of different lengths.

### `reversed()` — iterate backwards

```python
for item in reversed(["a", "b", "c"]):
    print(item)    # c, b, a
```

---

## 5. Loop Invariants for `for` Loops

`for` loops have invariants too. The invariant describes what is true at the start of each iteration.

**Example: computing the sum of a list**

```python
numbers = [3, 1, 4, 1, 5, 9]
total = 0   # neutral element for addition

# Invariant: total == sum of numbers[:i]
# (total is the sum of all elements processed so far)
for i, n in enumerate(numbers):
    total += n
    # After this: total == sum of numbers[:i+1]
```

At loop exit: `i == len(numbers) - 1`, invariant gives `total == sum(numbers[:len(numbers)]) == sum(numbers)` ✓

**Example: finding the maximum**

```python
def maximum(lst):
    assert len(lst) > 0, "Cannot find max of empty list"
    current_max = lst[0]
    # Invariant: current_max == max(lst[:i+1])
    for i in range(1, len(lst)):
        if lst[i] > current_max:
            current_max = lst[i]
        # Invariant maintained: current_max is still max of lst[:i+1]
    # At exit: current_max == max(lst[:len(lst)]) == max(lst) ✓
    return current_max
```

---

## 6. `for` vs. `while` — When to Use Each

| Situation | Use |
|-----------|-----|
| Iterating over a known collection | `for` |
| Running a fixed number of times | `for i in range(n)` |
| Continuing until a condition changes | `while condition` |
| User interaction (run until quit) | `while True: ... break` |
| Unknown number of iterations | `while` |
| Numerical methods (converge to answer) | `while error > tolerance` |

**Rule of thumb:** If you know what you're iterating over, use `for`. If you know when to stop but not how many steps it will take, use `while`.

---

## 7. Nested Control Flow — Combining It All

Real programs combine conditionals and loops freely.

### Example: Counting specific elements

```python
def count_evens(numbers):
    """Count how many even numbers are in a list."""
    count = 0
    for n in numbers:
        if n % 2 == 0:   # Conditional inside a for loop
            count += 1
    return count
```

### Example: Finding the first occurrence

```python
def find_first(lst, target):
    """Return the index of the first occurrence of target, or -1."""
    for i, value in enumerate(lst):
        if value == target:
            return i    # Exit function immediately — no need for break
    return -1           # Only reached if target was never found
```

### Example: Building a new list

```python
def squares_of_evens(numbers):
    """Return the squares of all even numbers in the list."""
    result = []
    for n in numbers:
        if n % 2 == 0:
            result.append(n ** 2)
    return result

squares_of_evens([1, 2, 3, 4, 5, 6])   # [4, 16, 36]
```

### Example: Nested loops with early exit

```python
def has_duplicate(lst):
    """Return True if the list contains any duplicate values."""
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):   # Only check pairs where j > i
            if lst[i] == lst[j]:
                return True   # Found a duplicate — exit immediately
    return False   # No duplicates found
```

**Invariant for outer loop:** No duplicate exists in `lst[:i]`.
**Invariant for inner loop:** `lst[i]` is not equal to any element in `lst[i+1:j]`.

---

## 8. The Sieve of Eratosthenes

A beautiful algorithm for finding all primes up to n. Written by Eratosthenes around 240 BC — still one of the most efficient methods for small n.

**Algorithm:**
1. Start with a list of all integers from 2 to n, all marked "prime"
2. Take the first unmarked number p. It's prime. Mark all multiples of p (p², p²+p, ...) as "not prime"
3. Repeat until p² > n
4. All remaining marked numbers are prime

```python
def sieve(n):
    """Return a list of all prime numbers up to and including n."""
    # Initialize: all numbers from 0 to n, assume all prime
    is_prime = [True] * (n + 1)
    is_prime[0] = False   # 0 is not prime
    is_prime[1] = False   # 1 is not prime

    p = 2
    # Loop invariant: all primes < p have been correctly identified;
    # all their multiples >= p² have been marked composite
    while p * p <= n:
        if is_prime[p]:
            # Mark all multiples of p starting from p² as composite
            # (smaller multiples already marked by smaller primes)
            multiple = p * p
            while multiple <= n:
                is_prime[multiple] = False
                multiple += p
        p += 1

    return [i for i in range(n + 1) if is_prime[i]]


primes = sieve(50)
print(primes)
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

This is your first non-trivial algorithm. Notice:
- Nested loops (outer loop over primes, inner loop over multiples)
- A carefully maintained invariant
- Starting from p² (not 2p) — because all smaller multiples were already marked

---

## 9. Comprehensions — A Preview

Python has a shorthand for building lists from loops + conditions: **list comprehensions**.

```python
# Long form:
squares = []
for i in range(10):
    squares.append(i ** 2)

# List comprehension:
squares = [i ** 2 for i in range(10)]

# With a condition:
even_squares = [i ** 2 for i in range(10) if i % 2 == 0]
```

We'll cover these fully in Week 7. For now, know they exist and recognize them when you see them.

---

## 10. Execution Tracing — The Full Skill

By now you should be able to trace any combination of conditionals and loops. Here is the complete process for any non-trivial piece of code:

1. **Find all variables** — list them; note initial values
2. **Identify the loop condition** — when does the loop exit?
3. **Trace iteration by iteration** — maintain a state table
4. **Track any conditional branches** — note which branch was taken each time
5. **Verify the result** — does the final state match what the code intends?

Practice this on every new loop you encounter until it becomes automatic. The students who can trace code reliably make far fewer bugs and fix them far faster.

---

## 11. Summary

| Concept | Key Point |
|---------|-----------|
| `for` loop | Iterates over any iterable; the sequence controls termination |
| `range(start, stop, step)` | Generates integers; lazy (no memory overhead) |
| `enumerate()` | Gives `(index, value)` pairs — use whenever you need the index |
| `zip()` | Iterates multiple sequences in parallel |
| `for` vs `while` | Known sequence → `for`; unknown termination → `while` |
| Loop invariant | Remains true at start of every iteration; proves correctness |
| Nested control | Loops containing conditions containing loops — trace carefully |
| Sieve of Eratosthenes | Classic algorithm: marks composites, leaves primes |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict each.

```python
list(range(10, 0, -3))
len(range(1, 10, 4))
list(range(5, 5))
list(range(0, -3))
list(enumerate("ab", start=1))
list(zip([1, 2, 3], "ab"))
```

**2. (Explain.)** These two loops look equivalent but differ in an important way. Explain what happens in each, and state the rule about modifying a sequence while iterating over it.

```python
# A
xs = [1, 2, 3, 4]
for x in xs:
    if x % 2 == 0:
        xs.remove(x)
print(xs)

# B
xs = [1, 2, 3, 4]
for x in xs[:]:
    if x % 2 == 0:
        xs.remove(x)
print(xs)
```

**3. (Build.)** Implement the Sieve of Eratosthenes for all primes below `n` using `for` loops and a boolean list. Then explain why the inner loop starts at `p * p` rather than `2 * p`.

**4. (Stretch.)** Predict the output, then say how many times the inner body runs for a general `n`.

```python
print([(i, j) for i in range(3) for j in range(i)])
```


### Answers

**1.** `[10, 7, 4, 1]`, `3`, `[]`, `[]`, `[(1, 'a'), (2, 'b')]`, `[(1, 'a'), (2, 'b')]`.

- `range(10, 0, -3)` stops **before** 0, so it yields 10, 7, 4, 1 and then would hit −2, which is past the stop. The endpoint is exclusive in both directions.
- `len(range(1, 10, 4))` is `3` — the values are 1, 5, 9. `range` computes its length arithmetically without generating anything, which is why `len(range(10**18))` is instant.
- `range(5, 5)` and `range(0, -3)` are both **empty**, not errors. A range whose stop is not beyond its start in the direction of travel simply yields nothing — which is what makes `for i in range(len(xs))` safe on an empty list.
- `zip` stops at the **shortest** argument, silently dropping the `3`. That silence is a real source of bugs; pass `strict=True` (Python 3.10+) to raise instead.

**2.** A prints `[1, 3]`… but by accident, and on a different list it would not. B prints `[1, 3]` reliably.

A `for` loop over a list holds an **internal index**, incremented after each pass. When `remove` shortens the list, every later element shifts down one position, but the index does not — so the element that moved into the vacated slot is **skipped**. On `[1, 2, 3, 4]` the damage happens to cancel out; on `[2, 4]` it does not: removing `2` shifts `4` to index 0 while the index moves to 1, the loop ends, and `[4]` survives. Try it.

B iterates over `xs[:]`, a **copy**, so the sequence being walked is never the one being modified. That is the rule: **never mutate a sequence you are iterating over.** Either iterate a copy, or — better — build a new list and rebind: `xs = [x for x in xs if x % 2]`. The comprehension is clearer and does not pay `remove`'s O(n) scan per deletion.

**3.**

```python
def primes_below(n):
    if n <= 2:
        return []
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n ** 0.5) + 1):
        if is_prime[p]:
            for multiple in range(p * p, n, p):
                is_prime[multiple] = False
    return [i for i, prime in enumerate(is_prime) if prime]
```

The inner loop starts at `p * p` because **every composite multiple of `p` below `p²` has already been crossed off**. Such a multiple is `k * p` with `k < p`, so it has a prime factor `q ≤ k < p`, and the pass for `q` — which ran earlier, since the outer loop ascends — already marked it. Starting at `2 * p` is correct but redundant.

The outer loop stops at `√n` for the matching reason: any composite below `n` has a prime factor at most `√n`, so once every prime up to `√n` has had its turn, nothing composite is left unmarked.

Together these bring the running time to O(n log log n), which is close enough to linear that the sieve remains the practical method for generating primes in bulk.

**4.** `[(1, 0), (2, 0), (2, 1)]`.

The clauses read **left to right, outermost first** — `for i` is the outer loop and `for j` the inner, exactly as in the nested-statement form. `i = 0` contributes nothing, because `range(0)` is empty; `i = 1` contributes `j = 0`; `i = 2` contributes `j = 0, 1`.

For general `n`, the inner body runs `0 + 1 + 2 + ... + (n-1) = n(n-1)/2` times — the triangular number, which is **Θ(n²)**. This is the shape of every "all unordered pairs" loop, and recognising it on sight is worth more than the formula: a doubly nested loop whose inner bound depends on the outer index is still quadratic, just with half the constant of a full `n × n` nest. You will prove the closed form by induction in MATH 151 and meet the same sum again bounding insertion sort in L17.



---

## Reading

- **Guttag, Ch. 2.4** — `for` loops and `range`
- **Guttag, Ch. 3** — Numerical programs (applies `while` and `for` to real problems)

---

*CS 101 · Week 2 · Lecture 9 (Fri) · © CSE Department*
