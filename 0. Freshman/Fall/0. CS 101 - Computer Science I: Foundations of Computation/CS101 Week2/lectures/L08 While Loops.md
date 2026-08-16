# CS 101 · Lecture 8 (Week 2, Lecture 2)
## Control Flow II: `while` Loops and Loop Invariants

**Week 2 · Thursday**
*"To iterate is human, to recurse divine." — L. Peter Deutsch*
*(We'll cover recursion in Week 4. For now, let's be human.)*

**Date:** Thursday 3 September 2026 · 09:00–09:50 · Week 2

---

## 0. The Problem with No Loops

In Problem Set 1, you computed 12 months of a mortgage schedule by writing 12 essentially identical blocks of code. That was deliberate — to show you exactly why loops are necessary.

Consider: how would you write a program to print the first 1,000 prime numbers without loops? You can't. Or rather, you'd need 1,000 manually written lines. Repetition is the essence of computation, and loops are how we express it.

---

## 1. The `while` Loop: Structure and Mechanics

### Basic syntax:

```python
while condition:
    body
```

Execution model:
1. Evaluate `condition`
2. If `False` → exit the loop, continue with the next statement
3. If `True` → execute `body`
4. Go back to step 1

```python
# Count from 1 to 5:
i = 1                  # Initialization
while i <= 5:          # Condition
    print(i)           # Body
    i = i + 1          # Update — CRITICAL! Without this, infinite loop
```

Output:
```
1
2
3
4
5
```

**The three parts of every correct `while` loop:**
1. **Initialization**: set up variables before the loop
2. **Condition**: determines when the loop continues
3. **Update**: changes state so the condition eventually becomes False

If you forget the update, you get an **infinite loop** — the loop runs forever. Press `Ctrl+C` to interrupt.

---

## 2. Tracing Loop Execution

**The most important skill for understanding loops:** trace through them by hand, step by step, tracking variable values.

```python
# Find the sum of digits of a positive integer
n = 1234
digit_sum = 0

while n > 0:
    digit = n % 10      # Last digit
    digit_sum += digit  # Add it to sum
    n = n // 10         # Remove last digit
```

Let's trace this:

| Iteration | `n` (before) | `digit` | `digit_sum` (after) | `n` (after) |
|-----------|-------------|---------|---------------------|-------------|
| Start | 1234 | — | 0 | — |
| 1 | 1234 | 4 | 4 | 123 |
| 2 | 123 | 3 | 7 | 12 |
| 3 | 12 | 2 | 9 | 1 |
| 4 | 1 | 1 | 10 | 0 |
| Exit | 0 | — | 10 | — |

After the loop: `digit_sum = 10`. Check: `1+2+3+4 = 10` ✓

**Practice this.** Tracing loops by hand — building the table row by row — is the fundamental debugging technique for iteration.

---

## 3. Loop Invariants: The Formal Proof Method

A **loop invariant** is a predicate (a logical statement) that is:
- **True before the loop starts** (initialization establishes it)
- **True after every iteration** (loop body preserves it)
- **Combined with the exit condition, proves correctness**

Think of a loop invariant as a mathematical promise the loop makes about its variables at every checkpoint.

### Example: Digit Sum

For the digit sum loop above, the invariant is:

> `digit_sum + sum_of_digits(original_n) == sum_of_digits(1234)`
> 
> i.e., `digit_sum` holds the sum of the digits we've removed from n so far.

- **Before the loop:** `digit_sum = 0`, `n = 1234`. Sum of digits removed = 0. Invariant holds: `0 + 10 = 10` ✓
- **After iteration 1:** `digit_sum = 4`, `n = 123`. Sum of digits remaining in n = 6. `4 + 6 = 10` ✓
- **After iteration 2:** `digit_sum = 7`, `n = 12`. Sum remaining = 3. `7 + 3 = 10` ✓
- **Exit condition:** `n == 0` → sum of digits remaining = 0
- **Invariant + exit:** `digit_sum + 0 = 10` → `digit_sum = 10` ✓

**This is a proof that the loop is correct.** Not a test, not an empirical check — a mathematical proof.

---

## 4. Common Loop Patterns

### Pattern 1: Counting up and down

```python
# Count up:
i = 0
while i < n:
    process(i)
    i += 1

# Count down:
i = n - 1
while i >= 0:
    process(i)
    i -= 1
```

### Pattern 2: Accumulator

An **accumulator** starts at a neutral value and collects results:

```python
# Sum of 1 to n:
total = 0           # Neutral value for addition
i = 1
while i <= n:
    total += i      # Accumulate
    i += 1

# Product of 1 to n (n!):
product = 1         # Neutral value for multiplication
i = 1
while i <= n:
    product *= i    # Accumulate
    i += 1
```

**Invariant for the sum loop:** `total == 1 + 2 + ... + (i-1)`

After loop exit (`i == n+1`): `total == 1 + 2 + ... + n` ✓

### Pattern 3: Search

```python
# Find first index where condition holds:
i = 0
while i < len(lst) and not condition(lst[i]):
    i += 1

if i < len(lst):
    print(f"Found at index {i}")
else:
    print("Not found")
```

**Note:** The condition `i < len(lst)` comes first in `and` — this is **short-circuit protection**. If `i` reaches `len(lst)`, we don't evaluate `lst[i]` (which would be an `IndexError`).

**Invariant:** `condition(lst[j])` is False for all `j < i`.

### Pattern 4: Reduction (consuming input)

```python
# Process a number digit by digit until it's exhausted:
while n > 0:
    process(n % 10)   # Work on last digit
    n //= 10          # Remove last digit
```

### Pattern 5: Converge to answer (numerical methods)

```python
# Newton-Raphson: approximate square root of x
# Iteration: guess = (guess + x/guess) / 2
x = 2.0
guess = x / 2
epsilon = 1e-10   # Tolerance

while abs(guess**2 - x) > epsilon:
    guess = (guess + x / guess) / 2.0

print(f"sqrt({x}) ≈ {guess}")   # 1.4142135623730951
```

**Invariant:** The error `|guess² - x|` decreases with each iteration (quadratic convergence — the number of correct decimal digits roughly doubles each step).

---

## 5. `break` and `continue`

### `break`: exit the loop immediately

```python
# Search for a value, stop when found:
target = 7
i = 0
while i < len(lst):
    if lst[i] == target:
        break       # Found it — stop searching
    i += 1

if i < len(lst):
    print(f"Found {target} at index {i}")
else:
    print(f"{target} not found")
```

### `continue`: skip the rest of this iteration

```python
# Print only even numbers, skip odds:
i = 0
while i < 20:
    i += 1
    if i % 2 != 0:
        continue    # Skip to next iteration
    print(i)
```

### `else` clause on while: rarely needed but worth knowing

```python
# Else runs if the loop finished WITHOUT a break:
while condition:
    if found:
        break
else:
    print("Loop completed without finding anything")
```

This is mostly used in search loops to distinguish "found" from "exhausted".

**Advice:** Use `break` and `continue` sparingly. They make loops harder to reason about. If you find yourself needing many `break` statements, consider restructuring your logic.

---

## 6. Infinite Loops: When and How

An intentional infinite loop uses `while True:` and relies on `break` to exit:

```python
# Interactive loop — runs until user says to stop:
while True:
    command = input("Enter command (or 'quit'): ").strip().lower()
    if command == "quit":
        print("Goodbye!")
        break
    elif command == "help":
        print("Available commands: help, status, quit")
    else:
        execute(command)
```

This is cleaner than trying to manage a boolean flag:

```python
# Worse version — uses a flag:
running = True
while running:
    command = input("> ")
    if command == "quit":
        running = False  # convoluted; still runs the rest of the loop body!
    ...
```

The `while True: ... break` pattern is idiomatic for "run until the user says stop."

---

## 7. Nested Loops

Loops can contain other loops. Each iteration of the outer loop runs the entire inner loop.

```python
# Multiplication table:
row = 1
while row <= 5:
    col = 1
    while col <= 5:
        print(f"{row * col:4}", end="")  # end="" prevents newline
        col += 1
    print()   # newline after each row
    row += 1
```

Output:
```
   1   2   3   4   5
   2   4   6   8  10
   3   6   9  12  15
   4   8  12  16  20
   5  10  15  20  25
```

**Performance alert:** Nested loops multiply iteration counts. If the outer loop runs N times and the inner loop runs M times, the body executes N×M times total. For N=M=1000, that's 1,000,000 iterations. We'll analyze this formally in Week 6 (Big-O).

---

## 8. Loop Design Process

When writing a loop, ask these questions in order:

1. **What changes each iteration?** (These are the loop variables)
2. **What is the stopping condition?** (When should the loop exit?)
3. **What invariant holds?** (What is true at the start of every iteration?)
4. **Does initialization establish the invariant?**
5. **Does the body preserve the invariant?**
6. **Does the loop terminate?** (Does the update make progress toward the exit condition?)

If you can answer all six, your loop is correct.

---

## 9. Complete Example: Collatz Sequence

The **Collatz conjecture** (unsolved since 1937): Start with any positive integer n. Repeatedly apply:
- If n is even: n → n/2
- If n is odd: n → 3n + 1

The conjecture states this always reaches 1. No counterexample has been found, but no proof exists either.

```python
def collatz(n):
    """
    Compute and print the Collatz sequence starting at n.
    Returns the number of steps taken to reach 1.
    """
    steps = 0
    print(n, end=" ")

    # Loop invariant: n > 0 (preserved because:
    #   - even case: n/2 > 0 if n > 0
    #   - odd case: 3n+1 > 0 if n > 0)
    # Termination: unproven in general, but observed empirically
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        print(n, end=" ")
        steps += 1

    print()
    return steps


# Test:
steps = collatz(27)
print(f"\nReached 1 in {steps} steps")
# 27 takes 111 steps and reaches 9232 before coming back down
```

This loop has an invariant (n > 0) but we cannot prove termination in general. This connects back to the Halting Problem — there may be no algorithm that can determine whether a given Collatz sequence halts.

---

## 10. Summary

| Concept | Key Point |
|---------|-----------|
| `while` structure | Init → Test → Body → Update → repeat |
| Three components | Initialization, condition, update — all three required |
| Tracing | Build a table of variable values at each iteration |
| Loop invariant | True before, during (after each iteration), and at exit |
| Accumulator pattern | Neutral start value; collect results incrementally |
| `break` / `continue` | Exit immediately / skip to next iteration |
| `while True:` | Intentional infinite loop; use `break` to exit |
| Nested loops | Outer N × Inner M = N×M total body executions |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Trace this loop and give the final values of `i` and `total`.

```python
i, total = 0, 0
while i < 5:
    i += 1
    if i == 3:
        continue
    if i == 5:
        break
    total += i
print(i, total)
```

**2. (Explain.)** State the loop invariant for this function and use it to argue that the function is correct. Your argument needs all three parts: initialisation, maintenance, and termination.

```python
def total(xs):
    s, i = 0, 0
    while i < len(xs):
        s += xs[i]
        i += 1
    return s
```

**3. (Build.)** Write a `while` loop that computes the integer square root of `n` — the largest `i` with `i * i <= n` — without using `**`, `math.sqrt`, or floats. State its invariant and its complexity.

**4. (Stretch.)** The Collatz sequence sends `n` to `n // 2` when even and `3 * n + 1` when odd, stopping at 1. Write the loop, and report how many steps `n = 27` takes. Then explain why you cannot write a loop invariant that proves this function terminates for all inputs.


### Answers

**1.** `5 7`.

| Pass | `i` after `i += 1` | Action | `total` |
|---|---|---|---|
| 1 | 1 | falls through | 1 |
| 2 | 2 | falls through | 3 |
| 3 | 3 | `continue` — skips the add | 3 |
| 4 | 4 | falls through | 7 |
| 5 | 5 | `break` — exits before the add | 7 |

Two things to notice. `continue` jumps to the **condition test**, not out of the loop — and because the increment happens *before* the `continue` here, the loop still progresses. Had `i += 1` been at the bottom of the body, the `continue` would have skipped it and produced an infinite loop; that is the classic `continue` bug. And `break` exits immediately, so `i` retains the value it had at that moment (`5`) rather than any value the condition would have produced.

**2.** **Invariant:** at the top of each iteration, `s == sum(xs[0:i])`.

*Initialisation.* Before the first test, `s = 0` and `i = 0`. `xs[0:0]` is empty and its sum is `0`, so the invariant holds.

*Maintenance.* Assume `s == sum(xs[0:i])` at the top of an iteration and that `i < len(xs)`, so `xs[i]` exists. The body sets `s` to `sum(xs[0:i]) + xs[i]`, which is `sum(xs[0:i+1])`, then sets `i` to `i+1`. So at the top of the next iteration `s == sum(xs[0:i])` again with the new `i`.

*Termination.* `i` strictly increases by 1 each pass and `len(xs)` is fixed, so the loop runs exactly `len(xs)` times and exits with `i == len(xs)`. Combining that with the invariant gives `s == sum(xs[0:len(xs)])`, which is the sum of the whole list — what the function claims to return. ∎

The pattern is always the same: the invariant alone is not a proof, and neither is termination alone. **Invariant + exit condition ⇒ postcondition** is where the correctness actually comes from.

**3.**

```python
def isqrt(n):
    i = 0
    while (i + 1) * (i + 1) <= n:
        i += 1
    return i
```

*Invariant:* at the top of each iteration, `i * i <= n`. *Termination:* `i` increases each pass and is bounded by `n`, so the loop ends; at exit `(i+1)**2 > n`, which with the invariant gives exactly the largest such `i`.

The complexity is **O(√n)** iterations — which for a 64-bit `n` is up to about 3 billion passes, far too slow. Binary searching the answer over `[0, n]` gives **O(log n)**, and is a direct application of the "binary search on the answer" idea from L16:

```python
def isqrt(n):
    lo, hi = 0, n + 1          # invariant: lo*lo <= n < hi*hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid
    return lo
```

Avoiding floats is not fussiness: `int(math.sqrt(n))` is *wrong* for some large `n`, because the double cannot represent the value exactly and may round just above or below the true root. Python provides `math.isqrt` for exactly this reason.

**4.**

```python
def collatz_steps(n):
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps
```

`collatz_steps(27)` is **111** — the sequence climbs as high as 9232 before descending, which is why 27 is the standard demonstration that "the numbers get smaller" is not an argument here.

Termination proofs need a **variant**: a quantity that is bounded below and strictly decreases every iteration. In the previous exercises `len(xs) - i` served that role. For Collatz no such quantity is known. `n` itself is not one — the odd step *increases* it. Nobody has found any variant, and nobody has found a counterexample either: the **Collatz conjecture**, that this terminates for every positive integer, has been open since 1937 and verified by computer past 2⁶⁸ without proof.

The honest summary is that you can prove a loop terminates when you can exhibit a variant, and the absence of one is not evidence of non-termination — it is the boundary of what is currently known.



---

## Reading

- **Guttag, Ch. 2.3** — `while` Loops (primary)
- **Guttag, Ch. 3.2–3.3** — Loop examples (exhaustive enumeration, approximation)

---

*CS 101 · Week 2 · Lecture 8 (Thu) · © CSE Department*
