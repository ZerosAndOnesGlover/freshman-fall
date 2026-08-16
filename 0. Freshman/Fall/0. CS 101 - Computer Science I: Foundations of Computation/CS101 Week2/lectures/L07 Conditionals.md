# CS 101 · Lecture 7 (Week 2, Lecture 1)
## Control Flow I: Conditionals and Boolean Decision Trees

**Week 2 · Wednesday**
*"The most important control structure in any programming language is the conditional — it is where the program makes a decision." — Donald Knuth*

**Date:** Wednesday 2 September 2026 · 09:00–09:50 · Week 2

---

## 0. Why Control Flow?

Every program we have written so far executes from top to bottom, line by line, with no choices and no repetition. This is called **sequential execution** — and it is severely limited.

Real computation requires:
- **Selection** — do one thing or another based on a condition (`if/elif/else`)
- **Iteration** — repeat something until a condition changes (`while`, `for`)

These two ideas, combined with sequential execution, are sufficient to express any computable function. This is the **Böhm-Jacopini theorem** (1966): any algorithm can be written using only sequence, selection, and iteration. You will never need `goto`.

This week we implement both. Today: selection.

---

## 1. The `if` Statement: Structure and Mechanics

### Basic syntax:

```python
if condition:
    body
```

The `condition` is any expression that evaluates to a boolean (or is truthy/falsy). The `body` is one or more statements, **indented** by exactly 4 spaces.

```python
x = 42

if x > 0:
    print("x is positive")
    print("It is greater than zero")
```

**Indentation is not style — it is syntax.** Python uses indentation to define blocks. This is unlike C, Java, and most other languages that use `{}`. Inconsistent indentation causes `IndentationError`.

### The full if-elif-else structure:

```python
if condition_1:
    # executed if condition_1 is True
    body_1
elif condition_2:
    # executed if condition_1 is False AND condition_2 is True
    body_2
elif condition_3:
    # executed if conditions 1 and 2 are False AND condition_3 is True
    body_3
else:
    # executed if ALL conditions above are False
    fallback_body
```

**Key rules:**
- `elif` and `else` are optional
- You can have as many `elif` branches as needed
- Only **one** branch executes — the first one whose condition is True
- Once a branch executes, all remaining branches are skipped

---

## 2. How Python Evaluates Conditions

Any expression can be a condition. Python converts it to bool automatically using the **truthiness rules** from Week 1:

```python
# All of these are valid conditions:
if x:              # True if x is truthy (non-zero, non-empty, not None)
if x > 0:          # Comparison expression
if x == y:         # Equality test
if "key" in d:     # Membership test
if x is None:      # Identity test
if not flag:       # Negated condition
```

### Tracing execution: the decision tree model

Think of `if/elif/else` as a **decision tree**. At each node, you test a condition. If True, you take that branch and stop. If False, you move to the next node.

```
          ┌─────────────────┐
          │  score >= 90?   │
          └────────┬────────┘
           True ◄──┤──► False
           │                │
      print("A")   ┌────────┴────────┐
                   │  score >= 80?   │
                   └────────┬────────┘
                    True ◄──┤──► False
                    │                │
               print("B")    ┌───────┴───────┐
                             │  score >= 70? │
                             └───────┬───────┘
                              True ◄─┤─► False
                              │              │
                         print("C")     print("F")
```

In Python:

```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"
```

**Why this works correctly:** Because conditions are tested in order and only one branch runs, `score >= 80` is only reached if `score < 90`. So you don't need to write `80 <= score < 90` — the structure of the if-chain handles it.

---

## 3. The Deep Why: What Does "Condition" Actually Mean?

A condition in an `if` statement is evaluated by Python through these precise steps:

1. Evaluate the expression to produce an object
2. Call `bool()` on that object
3. If `True`: execute the block. If `False`: skip it.

This means **any** expression can be a condition:

```python
items = [1, 2, 3]

if items:           # bool([1,2,3]) = True — list is non-empty
    print("list has items")

if not items:       # bool([]) = False, so not [] = True
    print("list is empty")
    
name = ""
if name:            # bool("") = False — empty string
    print(f"Hello, {name}")
else:
    print("No name provided")
```

This pattern — using the truthiness of a container to check if it's non-empty — is idiomatic Python. It's cleaner than `if len(items) > 0:`.

---

## 4. Common Conditional Patterns

### 4.1 Guard clauses (fail fast)

Instead of deeply nested conditions, return (or raise) early:

```python
# Nested — hard to read:
def process(x):
    if x is not None:
        if x > 0:
            if x < 1000:
                result = x * 2
                return result

# Guard clauses — each condition eliminates an invalid case:
def process(x):
    if x is None:
        return None       # guard: reject None
    if x <= 0:
        return None       # guard: reject non-positive
    if x >= 1000:
        return None       # guard: reject too large
    return x * 2          # main logic — only reached if all guards pass
```

Guard clauses make the **happy path** (valid input, normal case) the main flow of the function.

### 4.2 Conditional expression (ternary)

For simple two-way choices in an expression context:

```python
# If-else statement:
if x >= 0:
    abs_x = x
else:
    abs_x = -x

# Conditional expression — one line:
abs_x = x if x >= 0 else -x
```

Use the conditional expression when the logic is simple enough to read in one line. If you have to think about it, use the full if-else.

### 4.3 Nested conditions

Sometimes conditions must nest:

```python
def classify_point(x, y):
    """Classify a 2D point's location."""
    if x == 0 and y == 0:
        return "origin"
    elif x == 0:
        return "y-axis"
    elif y == 0:
        return "x-axis"
    elif x > 0 and y > 0:
        return "quadrant I"
    elif x < 0 and y > 0:
        return "quadrant II"
    elif x < 0 and y < 0:
        return "quadrant III"
    else:
        return "quadrant IV"
```

Notice: the `x == 0 and y == 0` case must come **first** — otherwise the `x == 0` branch would catch it. Order matters.

---

## 5. Loop Invariants: The Mathematical Heart of Loops

Before we cover loops (Thursday), we need this idea: **loop invariants**.

A loop invariant is a logical statement that:
1. Is **true before the loop begins**
2. Is **true after every iteration**
3. Combined with the loop's exit condition, **proves the loop is correct**

This might sound abstract, but every correct loop has a loop invariant — even if you've never thought about it explicitly. Learning to identify invariants transforms you from someone who writes loops that *seem* to work into someone who *proves* loops are correct.

**Example — finding the maximum of a list:**

```python
def find_max(lst):
    """Return the maximum value in a non-empty list."""
    current_max = lst[0]
    # Loop invariant: current_max == max(lst[0..i-1])
    # i.e., current_max is the maximum of all elements seen so far
    for i in range(1, len(lst)):
        if lst[i] > current_max:
            current_max = lst[i]
        # After this iteration: current_max == max(lst[0..i])
        # Invariant maintained!
    # At loop exit: i == len(lst)-1
    # Invariant + exit condition: current_max == max(lst[0..len(lst)-1])
    # = max of entire list ✓
    return current_max
```

We'll use loop invariants every week from now on. Mark this concept — it recurs in Week 4 (recursion), Week 5 (sorting), Week 6 (Big-O), and every algorithms course you'll ever take.

---

## 6. Debugging Conditionals

### The most common bugs in conditionals:

**Bug 1: `=` instead of `==`**
```python
if x = 5:    # SyntaxError in Python (good — Python catches this!)
if x == 5:   # Correct
```

Python intentionally makes assignment a statement (not an expression) to prevent this bug. In C, `if (x = 5)` is valid and almost always a bug.

**Bug 2: Wrong operator for edge cases**
```python
# Intends: "at least 18"
if age > 18:    # BUG: excludes exactly 18!
if age >= 18:   # Correct
```

**Bug 3: Forgetting that `and`/`or` short-circuit with operand types**
```python
result = x or default_value
# If x is 0 (which is valid!), result = default_value — wrong!
# Better:
result = x if x is not None else default_value
```

**Bug 4: Chained comparisons with non-transitive operators**
```python
# This works correctly:
0 < x < 10       # True if 0 < x AND x < 10

# This does NOT mean what you think in most languages:
a < b > c        # True if (a < b) AND (b > c) — Python chains this correctly
                 # but it reads confusingly. Use explicit parentheses.
```

### Debugging technique: trace execution manually

For any conditional you're unsure about, substitute specific values and trace through:

```python
# Testing the grade function with score = 75:
score = 75
# Line 1: score >= 90? → 75 >= 90? → False → skip
# Line 2: score >= 80? → 75 >= 80? → False → skip
# Line 3: score >= 70? → 75 >= 70? → True → grade = "C", exit chain
grade = "C"  ✓
```

---

## 7. A Complete Example: Fizzbuzz

FizzBuzz is a classic programming exercise:
- For multiples of 3: print "Fizz"
- For multiples of 5: print "Buzz"
- For multiples of both 3 and 5: print "FizzBuzz"
- Otherwise: print the number

```python
def fizzbuzz(n):
    """Return the FizzBuzz string for a given integer n."""
    if n % 15 == 0:      # Must check 15 FIRST (divisible by both)
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)
```

**Why does order matter here?** If we checked `n % 3 == 0` first, n=15 would return "Fizz" and never reach the FizzBuzz case. The most specific case must come first.

**Alternative approach — build the answer string:**
```python
def fizzbuzz_v2(n):
    result = ""
    if n % 3 == 0:
        result += "Fizz"
    if n % 5 == 0:
        result += "Buzz"
    return result if result else str(n)
```

This version uses independent `if` checks (not `elif`) and builds the answer. It's slightly more elegant because `"Fizz"` and `"Buzz"` are not repeated, and adding multiples of 7 → "Bazz" would require only one new `if` block.

---

## 8. Boolean Algebra and De Morgan's Laws

Boolean conditions follow mathematical laws. These are useful when simplifying complex conditions.

**De Morgan's Laws:**
```
not (A and B)  ≡  (not A) or (not B)
not (A or B)   ≡  (not A) and (not B)
```

In Python:
```python
# These are equivalent:
not (x > 0 and y > 0)
(x <= 0) or (y <= 0)

# These are equivalent:
not (x == 0 or y == 0)
(x != 0) and (y != 0)
```

Use De Morgan's to simplify conditions that feel awkward:

```python
# Awkward:
if not (user is None or not user.is_active):
    ...

# After De Morgan:
if user is not None and user.is_active:
    ...
```

---

## 9. The `match` Statement (Python 3.10+)

Python 3.10 introduced structural pattern matching — a more powerful form of multi-way selection:

```python
command = input("Enter command: ")

match command:
    case "quit" | "exit":
        print("Goodbye!")
    case "help":
        print("Available commands: quit, help, start")
    case "start":
        print("Starting...")
    case _:                  # Default case (like else)
        print(f"Unknown command: {command}")
```

The `_` wildcard matches anything. `|` separates multiple patterns for one case.

`match` also supports **structural matching** (matching against data structures):

```python
point = (1, 0)

match point:
    case (0, 0):
        print("Origin")
    case (x, 0):
        print(f"On x-axis at {x}")
    case (0, y):
        print(f"On y-axis at {y}")
    case (x, y):
        print(f"At ({x}, {y})")
```

This is elegant but new — we'll use `if/elif/else` as the primary tool and introduce `match` where it genuinely simplifies.

---

## 10. Summary

| Concept | Key Point |
|---------|-----------|
| Sequential execution | Default: top to bottom, line by line |
| `if/elif/else` | Tests conditions in order; exactly one branch runs |
| Truthiness as condition | Any expression; Python calls `bool()` automatically |
| Guard clauses | Return early to eliminate invalid cases; keeps main logic clean |
| Conditional expression | `val_if_true if condition else val_if_false` — for simple cases |
| Loop invariant | A property true before, during, and after a loop — proves correctness |
| De Morgan's Laws | `not (A and B) = (not A) or (not B)` and vice versa |
| Order matters | In `if/elif` chains, more specific conditions must come first |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict each value.

```python
bool([])
bool([0])
bool("0")
bool("")
bool(" ")
1 < 2 < 3
1 < 2 > 0
3 > 2 == True
```

**2. (Explain.)** Apply De Morgan's laws to rewrite `not (a and not b)` with the negation pushed all the way inward, then explain what makes such a rewrite worth doing in real code.

**3. (Build.)** Write a function `classify(n)` that returns `"negative"`, `"zero"`, `"small"` (1–9), or `"large"` (10+). Then write it a second time as a single chain with no `elif`, and say which version you would ship.

**4. (Stretch.)** Both of these guard against dividing by zero. One is correct and one has a latent bug. Identify which, and give an input that distinguishes them.

```python
# A
if d != 0 and n / d > 1:
    ...

# B
if n / d > 1 and d != 0:
    ...
```


### Answers

**1.** `False`, `True`, `True`, `False`, `True`, `True`, `True`, `False`.

The three that catch people:
- `bool([0])` is `True`. A container is truthy when it is **non-empty**; the truthiness of its contents is never consulted. A one-element list holding a falsey value is still a one-element list.
- `bool("0")` is `True` and `bool(" ")` is `True`. Any string of length ≥ 1 is truthy, including `"0"`, `"False"`, and a single space. Only `""` is falsey. This is why `if input("Continue? "):` is almost always a bug — every answer is truthy, including `"no"`.
- `3 > 2 == True` is `False`. Comparisons **chain**: this means `(3 > 2) and (2 == True)`, and `2 == True` is `False` since `True` is `1`. It does *not* mean `(3 > 2) == True`. Chaining is why `1 < 2 > 0` is legal at all — it reads as `1 < 2 and 2 > 0`.

**2.** `not (a and not b)` ⟶ `(not a) or (not not b)` ⟶ `not a or b`.

The rewrite is worth doing because **negations of compound conditions are hard to read and easy to get wrong**, and the commonest bug in the area is distributing a `not` without flipping the connective — writing `not a and not b` for `not (a or b)`, which is a different condition. Pushing negations inward until each one touches a single atom removes the opportunity.

There is a second reason: the rewritten form often reveals what the condition actually means. `not a or b` is the truth table of **implication** — it is exactly "a implies b". A guard written as `not (logged_in and not verified)` is opaque; the same guard written `not logged_in or verified` reads as "if they are logged in, they must be verified", which is the business rule. You will formalise this equivalence in MATH 151.

**3.**

```python
def classify(n):
    if n < 0:
        return "negative"
    elif n == 0:
        return "zero"
    elif n < 10:
        return "small"
    else:
        return "large"
```

Because every branch `return`s, the `elif`s are redundant and plain `if`s behave identically. But **ship the `elif` version**. The `elif` chain declares in the syntax that the cases are mutually exclusive and that exactly one will fire; a sequence of bare `if`s makes the reader verify that by checking every branch really does return. When someone later adds logging before a `return`, the `elif` version stays correct and the bare-`if` version silently starts falling through.

Note also that the ordering carries logic: `n < 10` is only reached when `n` is already known to be positive, so it does not need to be written `0 < n < 10`. That implicit narrowing is the reason to keep the chain in this order, and the reason reordering branches is more dangerous than it looks.

**4.** **A is correct; B is broken.** Any input with `d == 0` distinguishes them — say `n = 5, d = 0`.

In A, `and` short-circuits: `d != 0` is `False`, so `n / d` is never evaluated and the guard works. In B the division is evaluated **first**, raising `ZeroDivisionError` before the guard that was supposed to prevent it ever runs. The check is in the expression but has no effect, which is worse than not being there — it looks defended.

The general rule: in a short-circuiting `and`, **the guard must precede what it guards**. The same applies to `or` with a negated guard (`d == 0 or n / d > 1`), to `xs and xs[0]`, and to any `x is not None and x.field` test. Ordering operands of `and`/`or` is not a style choice in these cases; it is the correctness condition.



---

## Reading

- **Guttag, Ch. 2.2** — Branching Programs (conditionals)
- **Guttag, Ch. 2.3** — `while` Loops (preview for Thursday)

---

*CS 101 · Week 2 · Lecture 7 (Wed) · © CSE Department*
