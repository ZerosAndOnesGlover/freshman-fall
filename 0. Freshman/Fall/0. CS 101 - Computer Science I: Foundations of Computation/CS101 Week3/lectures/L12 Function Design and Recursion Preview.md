# CS 101 Lecture 12 (Week 3, Lecture 3)
## Function Design, Decomposition, and Recursion Preview

**Week 3 · Friday**
*"The art of programming is the art of organizing complexity." — Edsger Dijkstra*

---

## 0. The Goal: Writing Functions That Last

This lecture synthesizes the week by showing you how to design functions — not just how to write them. There is a profound difference: a function that works is a starting point. A function that is correct, clear, composable, and maintainable is engineering.

---

## 1. Function Decomposition — The Core Design Skill

**Decomposition** means breaking a complex problem into smaller sub-problems, each solved by its own function.

**The wrong way — one big function:**
```python
def analyze_text(text):
    # Count words
    words = text.lower().split()
    word_count = len(words)
    # Count sentences
    sentence_count = text.count('.') + text.count('!') + text.count('?')
    # Find most common word (nested loops, 30 more lines...)
    # Compute average word length (10 more lines...)
    # Check if it's a pangram (8 more lines...)
    # ... 70 lines total
    return word_count, sentence_count, ...
```

**The right way — decomposed:**
```python
def tokenize(text):
    """Split text into lowercase words."""
    return text.lower().split()

def count_sentences(text):
    """Count sentences (ends with . ! or ?)."""
    return sum(text.count(p) for p in ".!?")

def average_word_length(words):
    """Compute the mean length of a list of words."""
    if not words:
        return 0.0
    return sum(len(w) for w in words) / len(words)

def most_frequent_word(words):
    """Return the word that appears most often."""
    if not words:
        return None
    unique = list(set(words))
    return max(unique, key=words.count)

def analyze_text(text):
    """Full text analysis — orchestrates the sub-functions."""
    words = tokenize(text)
    return {
        "word_count":      len(words),
        "sentence_count":  count_sentences(text),
        "avg_word_length": average_word_length(words),
        "most_frequent":   most_frequent_word(words),
    }
```

The decomposed version has these advantages:
- Each function is **independently testable**
- Each function has a **single responsibility** (does one thing well)
- `analyze_text` reads almost like English — it's **self-documenting**
- Individual components can be **reused** elsewhere

---

## 2. The Single Responsibility Principle

A function should do **one thing**. If you find yourself writing "and" in a function's docstring, the function probably does too much.

```python
# Violates SRP — does two unrelated things:
def print_and_count_words(text):
    """Print the text and return the word count."""
    print(text)               # side effect: printing
    return len(text.split())  # computation: counting

# Better — separate responsibilities:
def word_count(text):
    """Return the number of words in text."""
    return len(text.split())

def display(text):
    """Print text to stdout."""
    print(text)
```

**The test for SRP:** Can you describe what the function does in one sentence without using "and"? If yes, it probably has a single responsibility.

---

## 3. Pure Functions vs. Functions with Side Effects

A **pure function**:
- Always returns the same output for the same input
- Has no side effects (doesn't modify anything outside itself)

```python
# Pure:
def square(x):
    return x * x

# Pure:
def celsius_to_fahrenheit(c):
    return c * 9/5 + 32

# NOT pure — modifies external state:
def append_and_print(lst, item):
    lst.append(item)    # modifies lst — a side effect
    print(lst)          # prints to screen — a side effect
```

**Why prefer pure functions?**
- **Testable:** same input always gives same output
- **Predictable:** no hidden state changes
- **Composable:** can be combined freely
- **Parallelizable:** no shared state to coordinate

In practice, you need both. The discipline is: **isolate side effects**. Put computation in pure functions; handle I/O and state changes in a small number of clearly-marked places.

---

## 4. Testing Your Functions

Every function you write should have tests. A test is a call that verifies the output matches expectation.

### Simple assertions:

```python
def is_palindrome(s):
    """Return True if s reads the same forwards and backwards."""
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

# Tests:
assert is_palindrome("racecar")     == True
assert is_palindrome("hello")       == False
assert is_palindrome("A man a plan a canal Panama") == True
assert is_palindrome("")            == True   # edge case: empty string
assert is_palindrome("a")           == True   # edge case: single char
print("All is_palindrome tests passed.")
```

### Test-Driven Development (TDD) preview:

Write the tests *first*, then implement. The tests are your specification made executable:

```python
# Step 1: Write tests for gcd() before implementing it
def test_gcd():
    assert gcd(48, 18) == 6
    assert gcd(100, 75) == 25
    assert gcd(7, 13) == 1       # coprime
    assert gcd(0, 5) == 5        # edge case
    assert gcd(5, 0) == 5        # edge case
    assert gcd(12, 12) == 12     # same number
    print("All gcd tests passed.")

# Step 2: Now implement gcd() to make the tests pass
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

test_gcd()
```

This is how professional software is developed. We'll study it formally in Year 2 (CS 212).

---

## 5. Recursion Preview — Functions Calling Themselves

A **recursive function** is one that calls itself. This is not a trick or a special feature — it falls directly out of what we know about function calls and the stack.

```python
def factorial(n):
    """Compute n! recursively."""
    if n == 0:              # base case: stop recursing
        return 1
    return n * factorial(n - 1)   # recursive case: call self with smaller input
```

When `factorial(4)` is called:
```
factorial(4)
  → 4 * factorial(3)
         → 3 * factorial(2)
                → 2 * factorial(1)
                       → 1 * factorial(0)
                              → 1          ← base case, starts returning
                       → 1 * 1 = 1
                → 2 * 1 = 2
         → 3 * 2 = 6
  → 4 * 6 = 24
```

The call stack during this:
```
factorial(4)   ← deepest: 5 frames deep
factorial(3)
factorial(2)
factorial(1)
factorial(0)   ← base case returns first
```

**Every recursive function has:**
1. **Base case(s):** inputs small enough to solve directly (no recursion)
2. **Recursive case:** reduces the problem toward the base case

**The connection to mathematical induction** (from MATH 151):
- Base case ↔ P(0) is true
- Recursive case ↔ if P(k) is true, then P(k+1) is true

When you write a recursive function, you are implementing a mathematical inductive definition. We'll explore this deeply next week.

---

## 6. Designing Recursive Functions — The Three-Step Method

**Step 1: Define the base case(s).**
What is the simplest input? What is the answer for it?

**Step 2: Define the recursive case.**
Assume the function works correctly for *smaller* inputs. Use that assumption to handle the current input.

**Step 3: Trust the recursion.**
Do not trace through the entire recursion in your head. Trust that the recursive call returns the correct result and use it.

```python
# Design: sum of a list recursively
# Step 1: Base case — empty list → sum is 0
# Step 2: Recursive case — sum([first] + rest) = first + sum(rest)
# Step 3: Trust that sum(rest) returns the correct sum of the rest

def recursive_sum(lst):
    if len(lst) == 0:        # base case
        return 0
    return lst[0] + recursive_sum(lst[1:])   # recursive case

recursive_sum([1, 2, 3, 4])   # 10
```

**Trace (brief):** `recursive_sum([1,2,3,4]) = 1 + recursive_sum([2,3,4]) = 1 + (2 + recursive_sum([3,4])) = 1 + 2 + 3 + 4 + 0 = 10` ✓

---

## 7. Helper Functions — Managing Recursive State

Sometimes recursion needs extra parameters that the caller shouldn't know about. Use a **helper function**:

```python
# We want: is_palindrome("racecar")
# But the recursive version needs indices to avoid creating new strings each call

def is_palindrome(s):
    """Public interface — no recursion exposed."""
    return _palindrome_helper(s, 0, len(s) - 1)

def _palindrome_helper(s, lo, hi):
    """Private helper — does the actual recursive work."""
    if lo >= hi:                   # base case: 0 or 1 chars remaining
        return True
    if s[lo] != s[hi]:             # mismatch found
        return False
    return _palindrome_helper(s, lo + 1, hi - 1)  # check inner substring
```

The underscore prefix `_palindrome_helper` is a convention signaling "this is a private implementation detail; don't call it directly."

---

## 8. When to Use Functions vs. Inline Code

**Always use a function when:**
- The code does one identifiable thing that could have a name
- The code is used (or might be used) in more than one place
- The code is complex enough that a name would aid understanding
- You want to test it in isolation

**Don't create a function for:**
- Trivial one-liners that are clearer inline: `total = sum(data)` needs no wrapper
- Code that is used exactly once and is already readable

The goal is not to maximize the number of functions — it is to maximize readability and maintainability.

---

## 9. Keyword Arguments — Calling with Explicit Names

```python
def create_user(name, age, role="student", active=True):
    return {"name": name, "age": age, "role": role, "active": active}

# Positional:
create_user("Alice", 20)

# Keyword — order doesn't matter:
create_user(age=20, name="Alice")

# Mixed — positional must come first:
create_user("Alice", 20, role="staff", active=False)

# All keyword:
create_user(name="Alice", age=20, role="student", active=True)
```

Keyword arguments make call sites **self-documenting**:

```python
# Cryptic:
draw_rectangle(100, 200, 50, 80, True, False)

# Clear:
draw_rectangle(x=100, y=200, width=50, height=80, filled=True, bordered=False)
```

Use keyword arguments whenever positional meaning isn't obvious.

---

## 10. A Complete Design Example: The Mortgage Problem, Done Right

In PS1, you computed mortgage payments analytically for 12 months without loops. Now you have functions and loops — let's build it properly.

```python
"""
mortgage.py
Correctly decomposed mortgage calculator.
Demonstrates: function decomposition, pure functions, composition.
"""

def monthly_rate(annual_rate_percent):
    """Convert annual interest rate (%) to monthly decimal rate."""
    return annual_rate_percent / 12 / 100


def monthly_payment(principal, annual_rate_percent, years):
    """
    Compute the fixed monthly payment for a mortgage.

    Formula: M = P * r(1+r)^n / ((1+r)^n - 1)
    where r = monthly rate, n = total payments.
    """
    r = monthly_rate(annual_rate_percent)
    n = years * 12
    return principal * r * (1 + r)**n / ((1 + r)**n - 1)


def amortize_month(balance, monthly_rate, payment):
    """
    Compute one month of amortization.

    Returns (interest_paid, principal_paid, new_balance).
    """
    interest   = balance * monthly_rate
    principal  = payment - interest
    new_balance = balance - principal
    return interest, principal, max(new_balance, 0.0)   # clamp to 0


def amortization_schedule(principal, annual_rate_percent, years):
    """
    Generate the full amortization schedule as a list of monthly records.

    Each record: {"month": int, "payment": float, "interest": float,
                  "principal": float, "balance": float}
    """
    r       = monthly_rate(annual_rate_percent)
    payment = monthly_payment(principal, annual_rate_percent, years)
    n       = years * 12
    balance = principal
    schedule = []

    for month in range(1, n + 1):
        interest, principal_paid, balance = amortize_month(balance, r, payment)
        schedule.append({
            "month":     month,
            "payment":   payment,
            "interest":  interest,
            "principal": principal_paid,
            "balance":   balance,
        })

    return schedule


def print_schedule_summary(principal, annual_rate_percent, years):
    """Print a full mortgage summary and the first year's schedule."""
    payment  = monthly_payment(principal, annual_rate_percent, years)
    schedule = amortization_schedule(principal, annual_rate_percent, years)
    total_paid     = payment * years * 12
    total_interest = total_paid - principal

    print(f"{'═'*55}")
    print(f"  MORTGAGE SUMMARY")
    print(f"{'═'*55}")
    print(f"  Principal:       ${principal:>12,.2f}")
    print(f"  Annual Rate:     {annual_rate_percent:>11.3f}%")
    print(f"  Term:            {years:>10} years ({years*12} payments)")
    print(f"  Monthly Payment: ${payment:>12,.2f}")
    print(f"  Total Paid:      ${total_paid:>12,.2f}")
    print(f"  Total Interest:  ${total_interest:>12,.2f}")
    print()

    print(f"  {'Mo':>3}  {'Payment':>10}  {'Interest':>10}  {'Principal':>10}  {'Balance':>12}")
    print(f"  {'─'*3}  {'─'*10}  {'─'*10}  {'─'*10}  {'─'*12}")

    for rec in schedule[:12]:   # first year only
        print(f"  {rec['month']:>3}  "
              f"${rec['payment']:>9,.2f}  "
              f"${rec['interest']:>9,.2f}  "
              f"${rec['principal']:>9,.2f}  "
              f"${rec['balance']:>11,.2f}")


if __name__ == "__main__":
    print_schedule_summary(300_000, 6.5, 30)
```

Notice:
- Each function does **one thing** with a clear name
- `amortize_month` is a pure function — same inputs, same outputs, no side effects
- `amortization_schedule` orchestrates — calls pure functions, builds a result
- `print_schedule_summary` handles all display — the only function with side effects
- Testing `amortize_month` in isolation is trivial; testing the monolithic PS1 version was not

---

## 11. Summary

| Concept | Key Point |
|---------|-----------|
| Decomposition | Break complex problems into single-responsibility functions |
| Single Responsibility | One function does one thing; "and" in the description is a warning sign |
| Pure functions | Same input → same output; no side effects; compose freely |
| Test-driven thinking | Write tests before (or alongside) implementation |
| Recursion (preview) | Function calls itself; needs base case and recursive case |
| Helper functions | `_prefixed` functions hide recursive state from callers |
| Keyword arguments | Make call sites self-documenting; `draw(x=100, y=200)` |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Classify each function as pure or impure, and for the impure ones name the specific side effect.

```python
def a(xs):
    return sorted(xs)

def b(xs):
    xs.sort()
    return xs

total = 0
def c(n):
    global total
    total += n
    return total

def d(n):
    print(n)
    return n * 2
```

**2. (Explain.)** This function violates the Single Responsibility Principle. Name every distinct responsibility it holds, then say what specific testing problem that causes.

```python
def process():
    raw = input("Enter numbers: ")
    nums = [int(n) for n in raw.split()]
    avg = sum(nums) / len(nums)
    print(f"Average: {avg:.2f}")
```

**3. (Build.)** Write `is_palindrome(s)` that ignores case, spaces, and punctuation, then write at least five `assert` tests. Say what each test is *for* — a test that duplicates another's reasoning is not worth writing.

**4. (Stretch.)** §5 previews recursion. Using the three-step method from §6, write `count_down(n)` that prints `n` down to 1 then `"Liftoff!"`. Then state what happens for `count_down(-1)` and fix it.


### Answers

**1.** - `a` — **pure.** `sorted` builds a new list; the argument is untouched and the result depends only on the input.
- `b` — **impure.** It mutates the caller's list in place. The caller's variable now points at reordered data whether they wanted that or not. Returning `xs` makes it worse by disguising the mutation as a computation.
- `c` — **impure.** It reads and writes module-level state, so the same argument gives different results on successive calls.
- `d` — **impure.** I/O is a side effect. The return value is a pure function of `n`, but the `print` means calling it twice is not the same as calling it once.

The practical test is: **could I replace a call with its result and change nothing?** For `a` yes; for the others no. Pure functions are the ones you can test with a single `assert`, cache, reorder, and run in parallel without thinking. Impurity is not a sin — a program with no side effects does nothing observable — but it should be deliberate and concentrated, not scattered.

**2.** Four responsibilities: **acquiring** input, **parsing** it, **computing** the average, and **presenting** the result.

The testing problem is concrete: there is no way to test the computation without also driving the I/O. To check that the average of `[1, 2, 3]` is `2.0`, a test must simulate keyboard input and capture stdout — replacing `builtins.input` and redirecting `sys.stdout` — and then parse the printed string back into a number to compare. All of that machinery exists only because the arithmetic is welded to the terminal.

Split it and the tests become trivial:

```python
def parse_numbers(text):
    return [int(n) for n in text.split()]

def mean(nums):
    return sum(nums) / len(nums)

def process():
    nums = parse_numbers(input("Enter numbers: "))
    print(f"Average: {mean(nums):.2f}")
```

Now `assert mean([1, 2, 3]) == 2.0` needs no mocking at all, and `process` — the only part that is still hard to test — contains no logic worth testing. That is the goal: **push impurity to the edges and keep the middle pure.**

**3.**

```python
def is_palindrome(s):
    cleaned = [ch.lower() for ch in s if ch.isalnum()]
    return cleaned == cleaned[::-1]

assert is_palindrome("") is True                       # empty: boundary
assert is_palindrome("a") is True                      # single char: boundary
assert is_palindrome("ab") is False                    # shortest failure
assert is_palindrome("A man, a plan, a canal: Panama")  # the actual feature
assert is_palindrome("!!!") is True                    # all stripped -> empty
assert is_palindrome("abba") is True                   # even length
assert is_palindrome("aba") is True                    # odd length
```

The reasoning behind the selection matters more than the count. **Boundaries** (empty, one element) are where off-by-one errors live. **The shortest failing case** (`"ab"`) proves the function can return `False` at all — a function that always returns `True` passes every positive test. **Even and odd lengths** exercise different midpoint behaviour. **`"!!!"`** probes the interaction between two features (stripping and comparing) rather than either alone, which is where bugs concentrate.

Adding `is_palindrome("racecar")` after all of these adds nothing: it fails for no reason the existing tests do not already cover.

**4.**

```python
def count_down(n):
    if n <= 0:                # base case
        print("Liftoff!")
        return
    print(n)                   # work
    count_down(n - 1)          # smaller problem
```

The three steps: identify the **base case** (nothing left to count), do the **work** for this level, and **recurse on a strictly smaller problem**.

The `-1` question is the point of the exercise. With the base case written as `if n == 0:`, `count_down(-1)` recurses to `-2`, `-3`, … never hitting the base, and dies with `RecursionError: maximum recursion depth exceeded` after about a thousand frames. Written as `n <= 0` — as above — it terminates immediately.

The general lesson: **the base case must catch every value the recursion can reach, not only the value you expect it to stop at.** Testing equality against a single value assumes the parameter marches exactly onto it. Any step that can overshoot — decrementing by 2, dividing, subtracting a computed amount — will sail past an `==` base case. Prefer an inequality, and prove that the parameter strictly decreases toward it.



---

## Reading

- **Guttag, Ch. 4.4** — Functions as Objects
- **Guttag, Ch. 4.5** — Modules (connecting to Friday's PS3)

---

*CS 101 · Week 3 · Lecture 12 (Fri) · © CSE Department*
