# CS 101 · Lecture 10 (Week 3, Lecture 1)
## Functions, Parameters, Return Values, and Encapsulation

**Week 3 · Wednesday**
*"A function is not just a named block of code — it is a contract between the caller and the implementation." — Barbara Liskov*

**Date:** Wednesday 9 September 2026 · 09:00–09:50 · Week 3

---

## 0. Why Functions? The Deep Answer

Before Week 3, every program you wrote was a flat sequence of statements. This works fine for 20 lines. It fails catastrophically at 200, 2,000, or 200,000 lines — for three reasons:

**1. Repetition.** If you need to compute a mortgage payment in six places, you write the formula six times. When the formula is wrong (and it will be), you fix it in six places — and miss at least one.

**2. Cognitive overload.** The human working memory holds roughly 7 items. A 200-line flat program requires you to hold all 200 lines in your head simultaneously to understand any part of it.

**3. No testability.** You cannot test a computation that is buried in line 47 of a flat script. You can only test the whole program.

Functions solve all three problems by introducing **abstraction**: a name that hides a computation. Once you name a computation, you can:
- Call it from anywhere without repeating its implementation
- Understand a program by understanding its names, not its internals
- Test each computation in isolation

This is not a convenience feature — it is the foundational engineering technique for managing complexity.

---

## 1. Anatomy of a Function

```python
def function_name(parameter_1, parameter_2):
    """
    Docstring: describes what the function does, its parameters, and its return value.
    This is read by help(), IDEs, and documentation generators.
    """
    # body: statements that compute the result
    result = parameter_1 + parameter_2
    return result     # the value handed back to the caller
```

Every component has a precise role:

| Component | Role |
|-----------|------|
| `def` | Keyword that starts a function definition |
| `function_name` | The name you use to call it; follows variable naming rules |
| `(parameter_1, parameter_2)` | Placeholders for the values the caller will supply |
| Docstring | Human-readable contract describing the function |
| Body | The computation — indented 4 spaces |
| `return` | Sends a value back to the caller; exits the function |

---

## 2. The Mechanics: What Actually Happens When You Call a Function

```python
def square(x):
    result = x * x
    return result

y = square(5)
print(y)    # 25
```

Step by step — this is what Python actually does:

1. **Evaluate the argument:** `5` evaluates to `5`
2. **Create a new stack frame:** a new namespace is created for this call
3. **Bind the parameter:** in the new frame, `x` is bound to `5`
4. **Execute the body:** `result = 5 * 5 = 25`
5. **Return:** the value `25` is handed back to the caller, the frame is destroyed
6. **Bind the result:** in the caller's frame, `y` is bound to `25`

The key phrase: **the stack frame is created and destroyed for each call.** Parameters and local variables exist only while the function runs.

We'll visualize this in detail when we study the call stack in Lecture 11.

---

## 3. Parameters vs. Arguments — The Precise Distinction

These terms are often used interchangeably, but they mean different things:

- **Parameter**: the name in the function definition — `x` in `def square(x)`
- **Argument**: the value supplied in a call — `5` in `square(5)`

```python
def add(a, b):      # a, b are PARAMETERS
    return a + b

result = add(3, 4)  # 3, 4 are ARGUMENTS
```

This distinction matters when reading error messages. Python says:
```
TypeError: add() takes 2 positional arguments but 3 were given
```
The word "arguments" here refers to the call site.

---

## 4. Return Values — The Complete Picture

### 4.1 Every function returns something

A function without an explicit `return` statement returns `None`:

```python
def greet(name):
    print(f"Hello, {name}!")    # side effect: prints to screen
    # no return statement

result = greet("Alice")
print(result)    # None — greet() returned nothing
```

`print()` and `return` are fundamentally different:
- `print()` is a **side effect** — it affects the external world (the screen)
- `return` sends a value **back to the caller** — it is part of the computation

A function that only prints cannot be composed with other functions. A function that returns a value can be used anywhere an expression is expected.

```python
# Can compose return values:
total = add(square(3), square(4))   # add(9, 16) = 25

# Cannot compose print — it returns None:
total = add(print(3), print(4))     # add(None, None) → TypeError
```

### 4.2 Multiple return values via tuple unpacking

Python functions can return multiple values by returning a tuple:

```python
def min_max(lst):
    """Return (minimum, maximum) of a non-empty list."""
    current_min = lst[0]
    current_max = lst[0]
    for x in lst[1:]:
        if x < current_min:
            current_min = x
        if x > current_max:
            current_max = x
    return current_min, current_max    # returns a tuple

lo, hi = min_max([3, 1, 4, 1, 5, 9, 2, 6])
print(f"min={lo}, max={hi}")   # min=1, max=9
```

The `return a, b` syntax is equivalent to `return (a, b)`. The tuple is unpacked at the call site by `lo, hi = ...`.

### 4.3 Early return — using return as a guard

`return` immediately exits the function. This enables the guard clause pattern:

```python
def safe_divide(a, b):
    if b == 0:
        return None    # Early return for invalid input
    return a / b       # Normal case — only reached if b != 0
```

This is cleaner than nesting everything inside an `if b != 0:` block.

---

## 5. How Functions Achieve Encapsulation

**Encapsulation** means hiding the implementation details behind a name. The caller knows *what* the function does; they don't need to know *how*.

```python
def is_prime(n):
    """Return True if n is a prime number, False otherwise."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True
```

When you call `is_prime(17)`, you think "is 17 prime?" — not "check divisibility by 3, 5, 7, ... up to √17." The complexity is **encapsulated** behind the name `is_prime`.

This is why good function names are so important. `is_prime(n)` communicates intent. `check_div(n)` does not. `f(n)` communicates nothing at all.

---

## 6. Function Composition — Building Complexity From Simplicity

The real power of functions is **composition**: using functions to build other functions.

```python
def celsius_to_kelvin(c):
    return c + 273.15

def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9

def fahrenheit_to_kelvin(f):
    return celsius_to_kelvin(fahrenheit_to_celsius(f))
```

`fahrenheit_to_kelvin` is defined entirely in terms of the other two functions. It doesn't repeat any logic — it **composes** existing abstractions.

This is how large software is built: small, well-tested functions composed into larger functions composed into modules composed into systems.

```python
# Building a statistics library from simple components:
def mean(data):
    return sum(data) / len(data)

def variance(data):
    m = mean(data)
    return mean([(x - m)**2 for x in data])

def std_dev(data):
    return variance(data) ** 0.5

def z_score(x, data):
    return (x - mean(data)) / std_dev(data)
```

Each function is simple, testable, and understandable in isolation. Together they form a complete statistical toolkit.

---

## 7. Specifications — The Contract Model

Before writing any function, write its specification. A specification answers:

1. **What are the inputs?** (types, constraints, valid range)
2. **What does the function return?** (type, meaning)
3. **What are the preconditions?** (what must be true when the function is called)
4. **What are the postconditions?** (what is guaranteed to be true when it returns)

```python
def binary_search(lst, target):
    """
    Search for target in a sorted list using binary search.

    Preconditions:
        - lst is sorted in ascending order (caller's responsibility)
        - lst contains no duplicate values

    Args:
        lst    (list): a sorted list of comparable elements
        target:        the value to search for

    Returns:
        int: the index of target in lst, or -1 if not found

    Examples:
        binary_search([1, 3, 5, 7, 9], 5)  → 2
        binary_search([1, 3, 5, 7, 9], 4)  → -1
        binary_search([], 5)                → -1

    Time complexity: O(log n)
    """
    lo, hi = 0, len(lst) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

The docstring **is** the specification. It is a contract between the function and its callers. If the caller respects the preconditions, the function guarantees the postconditions.

---

## 8. `assert` — Enforcing Preconditions

`assert` checks that a condition is true; if not, it raises `AssertionError`:

```python
def factorial(n):
    """Return n! for non-negative integer n."""
    assert isinstance(n, int) and n >= 0, f"n must be a non-negative int, got {n}"
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

factorial(5)    # 120
factorial(-1)   # AssertionError: n must be a non-negative int, got -1
factorial(2.5)  # AssertionError: n must be a non-negative int, got 2.5
```

`assert` is for **preconditions** — things that must be true for the function to work correctly, that the *caller* is responsible for ensuring. It is not for error handling of user input (use `try/except` for that — Week 10).

---

## 9. First-Class Functions — Functions as Values

In Python, functions are **first-class objects** — they can be assigned to variables, passed as arguments, and returned from other functions.

```python
def double(x):
    return x * 2

def triple(x):
    return x * 3

# Functions can be assigned to variables:
f = double
print(f(5))    # 10

# Functions can be passed as arguments:
def apply(func, value):
    return func(value)

print(apply(double, 5))   # 10
print(apply(triple, 5))   # 15

# Functions can be stored in data structures:
operations = [double, triple, abs]
for op in operations:
    print(op(-4))    # -8, -12, 4
```

This is a deep feature — we'll explore it fully in later weeks. For now: understand that `double` (without parentheses) is the function object itself, while `double(5)` is a call that evaluates to `10`.

---

## 10. A Complete Example: Building a Mini Math Library

```python
"""
mathlib.py
A small mathematical library demonstrating function design principles.
"""

def clamp(value, lo, hi):
    """
    Restrict value to the interval [lo, hi].

    clamp(5, 0, 10)   → 5
    clamp(-3, 0, 10)  → 0
    clamp(15, 0, 10)  → 10
    """
    assert lo <= hi, f"lo={lo} must be <= hi={hi}"
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value


def lerp(a, b, t):
    """
    Linear interpolation between a and b by fraction t.
    t=0 → a, t=1 → b, t=0.5 → midpoint.

    lerp(0, 100, 0.25)  → 25.0
    lerp(10, 20, 0.5)   → 15.0
    """
    assert 0.0 <= t <= 1.0, f"t={t} must be in [0, 1]"
    return a + (b - a) * t


def normalize(value, old_min, old_max, new_min=0.0, new_max=1.0):
    """
    Map value from [old_min, old_max] to [new_min, new_max].

    normalize(75, 0, 100)         → 0.75
    normalize(75, 0, 100, 0, 10)  → 7.5
    """
    assert old_min != old_max, "old_min and old_max must be different"
    t = (value - old_min) / (old_max - old_min)
    return lerp(new_min, new_max, t)


def sign(x):
    """
    Return -1 if x < 0, 0 if x == 0, 1 if x > 0.
    """
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


def is_between(value, lo, hi, inclusive=True):
    """
    Return True if value is between lo and hi.
    If inclusive=True (default), the endpoints are included.
    """
    if inclusive:
        return lo <= value <= hi
    else:
        return lo < value < hi


# Demonstration:
if __name__ == "__main__":
    print(clamp(5, 0, 10))          # 5
    print(clamp(-3, 0, 10))         # 0
    print(lerp(0, 100, 0.25))       # 25.0
    print(normalize(75, 0, 100))    # 0.75
    print(sign(-42))                # -1
    print(is_between(5, 1, 10))     # True
    print(is_between(5, 1, 5, inclusive=False))  # False
```

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Why functions? | Eliminate repetition, manage complexity, enable testing |
| Parameters vs arguments | Parameters are names in the definition; arguments are values at the call |
| Return value | The value handed back to the caller; every function returns something (None if implicit) |
| Encapsulation | The caller knows *what*, not *how* |
| Function composition | Build complex behavior from simple, tested components |
| Specification | A contract: preconditions the caller must satisfy; postconditions the function guarantees |
| `assert` | Enforces preconditions; fails loudly if violated |
| First-class functions | Functions are objects; can be assigned, passed, and returned |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict what each call returns.

```python
def a(): pass
def b(): return
def c(): return 1, 2
def d(xs):
    for x in xs:
        if x < 0:
            return x

print(a(), b(), c())
print(d([1, 2, 3]), d([1, -2, 3]))
```

**2. (Explain.)** §3 distinguishes parameters from arguments. Using the function below, name every parameter, and for each call say which arguments are positional and which are keyword — and why the last call is an error.

```python
def f(a, b=2, *args, c, **kwargs): ...

f(1, c=3)
f(1, 5, 7, 9, c=3, d=4)
f(1, 2, 3)
```

**3. (Build.)** Write `mean(xs)` with a specification in the docstring and an `assert` enforcing its precondition. Then explain why `assert` is the wrong tool for validating data that came from a user.

**4. (Stretch.)** §9 introduces first-class functions. Predict the output, and explain what makes the last line work.

```python
def twice(f, x):
    return f(f(x))

def inc(n):
    return n + 1

print(twice(inc, 5))
print(twice(len, "hello"))
print(twice(twice, ...))
```


### Answers

**1.** `None None (1, 2)` then `None -2`.

All four illustrate one rule: **a function that reaches the end of its body without executing a `return` returns `None`.** `a` has no `return` at all; `b` has a bare `return`, which is `return None` written shorter; `d([1, 2, 3])` finds no negative and falls off the end.

`c` shows that `return 1, 2` returns a **single tuple**, not two values — Python has no multiple return. `x, y = c()` works because the tuple is then unpacked by the assignment.

`d` is the one that matters in practice. A function whose "not found" path is an accidental fall-off is a bug waiting to happen, because `None` will travel silently until something tries to do arithmetic on it, and the traceback will point at that distant line rather than at `d`. Make the failure path explicit: `return None` on purpose, or raise.

**2.** Parameters: `a` (positional-or-keyword, required), `b` (positional-or-keyword, default `2`), `*args` (collects extra positionals), `c` (**keyword-only**, required), `**kwargs` (collects extra keywords).

- `f(1, c=3)` — `1` is a positional argument binding `a`; `c=3` is a keyword argument. `b` takes its default, `args` is `()`, `kwargs` is `{}`.
- `f(1, 5, 7, 9, c=3, d=4)` — positionals `1, 5` bind `a, b`; `7, 9` overflow into `args`; `c=3` is keyword; `d=4` overflows into `kwargs` as `{'d': 4}`.
- `f(1, 2, 3)` — **`TypeError: f() missing 1 required keyword-only argument: 'c'`**. Everything after `*args` is keyword-only and can never be filled positionally, so the `3` goes into `args` and `c` is left unbound.

The distinction to keep: a **parameter** is a name in the `def`; an **argument** is a value at the call site. Making `c` keyword-only is a deliberate API choice — it forces callers to name the value, which is what you want for flags and options that would otherwise appear as an unexplained bare `True`.

**3.**

```python
def mean(xs):
    """Return the arithmetic mean of xs.

    Pre:  xs is a non-empty sequence of numbers.
    Post: returns sum(xs) / len(xs) as a float.
    """
    assert len(xs) > 0, "mean() requires a non-empty sequence"
    return sum(xs) / len(xs)
```

`assert` is for **checking your own reasoning**, not for validating input. Two reasons it is wrong for user data:

1. **`assert` can be compiled out.** Running Python with `-O` removes every `assert` statement entirely. Validation that vanishes under an optimisation flag is not validation. This is the decisive argument.
2. **`AssertionError` is the wrong signal.** It tells a caller that the *program* has a bug, not that *they* passed something bad. A caller can reasonably catch `ValueError` and re-prompt; catching `AssertionError` to handle bad input is a code smell.

So: `assert` for invariants you believe are already guaranteed (a preconditon a *programmer* must satisfy), and an explicit `if ...: raise ValueError(...)` for anything that crossed a trust boundary.

**4.** `7`, then a `TypeError`, then a question worth thinking about.

`twice(inc, 5)` is `inc(inc(5))` = `7`.

`twice(len, "hello")` computes `len("hello")` = `5`, then `len(5)` — and integers have no length, so it raises `TypeError: object of type 'int' has no len()`. The lesson: passing a function as a value is easy, but `twice` implicitly requires `f`'s **return type to match its own parameter type**. Nothing in Python checks that; the error surfaces one call too late. A type annotation `def twice(f: Callable[[T], T], x: T) -> T` states the constraint, and a checker like `mypy` would catch this statically.

The third line is deliberately incomplete. `twice(twice, ...)` would need a value that is itself a `(function, value)` pair, since `twice` takes two arguments — so it does not typecheck. But `twice` *can* be composed if you curry it, and that is the door into functional programming: functions that take and return functions are just values, and the only thing that limits what you can build is whether the types line up.



---

## Reading

- **Guttag, Ch. 4** — Functions, Scoping, and Abstraction (primary — read all of it)

---

*CS 101 · Week 3 · Lecture 10 (Wed) · © CSE Department*
