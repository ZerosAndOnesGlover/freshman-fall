# CS 101 · Lab 2
## Debugging with Print-Tracing, PDB, and Loop Invariants

**Tuesday of Week 3 · Lab Section** — sat after this week's Wed–Fri lectures, and covers Week 2.
*Duration: 2 hours · Graded on completion (TA checkoff)*

---

## Objectives

By the end of this lab, you will:
- [ ] Trace loop execution by hand with full state tables
- [ ] Identify and state loop invariants for given loops
- [ ] Use `print()` strategically to debug loops
- [ ] Use Python's `pdb` debugger to step through code
- [ ] Fix 5 buggy programs using systematic debugging
- [ ] Implement the Collatz sequence and the Sieve of Eratosthenes

---

## Setup

```bash
cd ~/cs101
mkdir week2 && cd week2
```

---

## Part 1: Manual Execution Tracing (30 minutes)

**Before touching code:** work through these by hand on paper. Tracing mentally without committing to paper is how bugs hide.

### Exercise 1.1: Trace this loop completely

```python
x = 100
result = 0
count = 0

while x > 1:
    if x % 2 == 0:
        x = x // 2
    else:
        x = 3 * x + 1
    result += x
    count += 1
```

Build the complete state table:

| Iteration | `x` (start) | `x % 2 == 0?` | `x` (end) | `result` | `count` |
|-----------|------------|--------------|-----------|----------|---------|
| 0 (init) | 100 | — | — | 0 | 0 |
| 1 | 100 | ? | ? | ? | ? |
| 2 | ? | ? | ? | ? | ? |
| ... | | | | | |

**Do the first 8 iterations by hand. Then answer:**
1. What does this code compute?
2. State the loop invariant precisely (what is true at the start of each iteration?).
3. What is the final value of `result` after the loop completes?

### Exercise 1.2: Find the bug by tracing

This code is supposed to compute the factorial of `n` (n! = 1 × 2 × 3 × ... × n). It has a bug.

```python
n = 5
result = 0      # Bug hint: is this the right starting value?
i = 1

while i <= n:
    result *= i
    i += 1

print(result)   # Should print 120, but doesn't
```

1. Trace the first 3 iterations and find the bug.
2. What does the loop invariant tell you about the correct initialization?
3. Fix the bug and verify by tracing the corrected version.

### Exercise 1.3: Trace nested loops

```python
total = 0
i = 1
while i <= 4:
    j = 1
    while j <= i:
        total += j
        j += 1
    i += 1
print(total)
```

Build a full trace table. (Hint: use two rows of columns — one for the outer loop, one for the inner.)

What pattern do you see in what's being computed?

---

## Part 2: Debugging Techniques (30 minutes)

### Technique 1: Strategic Print Debugging

The most fundamental debugging technique: insert `print()` statements to inspect state.

**Bad print debugging:**
```python
print(x)              # What is x? Which iteration? Useless.
print("here")         # Confirms execution reached this line, nothing more.
```

**Good print debugging:**
```python
print(f"[iter {i}] x={x}, result={result}, condition={x > 0}")
# Gives you: the iteration number, all relevant variables, and the condition
```

Create `debug_exercise.py` with this buggy code. Use print debugging to find each bug.

```python
# debug_exercise.py
# Five buggy functions. Use print debugging to find and fix each bug.
# After fixing, remove the debug prints and verify the correct output.

def bug_1():
    """Should return the sum of all odd numbers from 1 to 99."""
    total = 0
    for i in range(1, 100, 2):
        total = i          # BUG: this is not accumulation!
    return total
    # Expected: 2500


def bug_2():
    """Should return True if n is prime, False otherwise."""
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, n):   # BUG: this range is too large (inefficient but not wrong)
                                 # The real bug is elsewhere — find it!
            if n % i == 0:
                return True      # BUG: this return value is wrong!
        return False
    
    # Test:
    assert is_prime(2) == True
    assert is_prime(7) == True
    assert is_prime(9) == False
    assert is_prime(1) == False
    return "is_prime tests passed"


def bug_3():
    """Should count how many times 'a' appears in a string."""
    s = "banana"
    count = 0
    for char in s:
        if char == 'a':
            count + 1   # BUG: augmented assignment not used!
    return count
    # Expected: 3


def bug_4():
    """Should return the largest value in a non-empty list."""
    def find_max(lst):
        current_max = 0   # BUG: what if all values are negative?
        for val in lst:
            if val > current_max:
                current_max = val
        return current_max
    
    assert find_max([3, 1, 4, 1, 5, 9]) == 9
    assert find_max([-1, -5, -3]) == -1   # This will fail!
    return "find_max tests passed"


def bug_5():
    """Should reverse a string without using [::-1]."""
    def reverse_string(s):
        result = ""
        i = len(s)        # BUG: off-by-one error
        while i >= 0:
            result += s[i]
            i -= 1
        return result
    
    assert reverse_string("hello") == "olleh"
    assert reverse_string("a") == "a"
    assert reverse_string("") == ""
    return "reverse_string tests passed"


# Run each bug function:
# (Comment/uncomment to test one at a time)
print(bug_1())
print(bug_2())
print(bug_3())
print(bug_4())
print(bug_5())
```

**For each bug:**
1. Add strategic print statements inside the function to inspect state
2. Identify the exact line that is wrong
3. Explain WHY it is wrong (what was the programmer's intent vs. what the code does)
4. Fix it
5. Verify with print that it now produces the correct result
6. Remove the debug prints

### Technique 2: Python Debugger (PDB)

PDB is Python's built-in interactive debugger. It lets you pause execution, inspect variables, and step through code line by line.

**Method 1: Insert a breakpoint in code**
```python
import pdb

def my_function(x):
    result = 0
    for i in range(x):
        pdb.set_trace()    # Execution pauses here
        result += i
    return result
```

**Method 2: Run from command line with PDB**
```bash
python3 -m pdb my_program.py
```

**Method 3: `breakpoint()` built-in (Python 3.7+)**
```python
def my_function(x):
    result = 0
    for i in range(x):
        breakpoint()    # Cleaner than pdb.set_trace()
        result += i
    return result
```

**Essential PDB commands:**

| Command | Shortcut | What it does |
|---------|----------|-------------|
| `next` | `n` | Execute the next line (don't step into functions) |
| `step` | `s` | Execute next line (step INTO function calls) |
| `continue` | `c` | Continue until next breakpoint |
| `print expr` | `p expr` | Print the value of an expression |
| `list` | `l` | Show surrounding source code |
| `where` | `w` | Show call stack |
| `quit` | `q` | Exit the debugger |
| `help` | `h` | Show help |

**PDB exercise:**

Create `pdb_exercise.py`:

```python
# pdb_exercise.py
# Use PDB to trace through this Newton's method implementation
# and understand each step.

def sqrt_newton(x, tolerance=1e-10):
    """Compute sqrt(x) using Newton-Raphson iteration."""
    if x < 0:
        raise ValueError("Cannot take sqrt of negative number")
    if x == 0:
        return 0
    
    guess = x / 2.0
    iterations = 0
    
    while abs(guess**2 - x) > tolerance:
        breakpoint()    # <- PDB will pause here each iteration
        old_guess = guess
        guess = (guess + x / guess) / 2.0
        iterations += 1
    
    return guess, iterations

result, iters = sqrt_newton(2.0)
print(f"sqrt(2) ≈ {result}")
print(f"Actual: {2**0.5}")
print(f"Error: {abs(result - 2**0.5):.2e}")
print(f"Iterations: {iters}")
```

Run with `python3 pdb_exercise.py`. At each breakpoint, use `p guess`, `p old_guess`, `p abs(guess**2 - 2.0)` to watch the convergence. Notice how the error roughly squares each iteration (quadratic convergence).

**Questions to answer in a comment block at the top of the file:**
1. After how many iterations does the error drop below 1e-6?
2. After how many iterations below 1e-10?
3. How does the error change between iterations — is the convergence linear or faster?

---

## Part 3: Loop Implementation Challenges (30 minutes)

Create `loops.py`. Implement each function with the specified loop type.

```python
# loops.py
# CS 101 — Week 2, Lab 2
# Loop implementation exercises

# ─── Exercise 3.1: Collatz Sequence ───────────────────────────────────────────

def collatz_length(n):
    """
    Return the number of steps for the Collatz sequence starting at n to reach 1.
    
    Rules: if n is even → n = n // 2
           if n is odd  → n = 3*n + 1
    
    Example: collatz_length(6) → 8
    Sequence: 6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1 (8 steps)
    
    Use a while loop.
    """
    # TODO: implement
    pass


def max_collatz_length(limit):
    """
    Find the starting number in [1, limit] that produces the longest Collatz sequence.
    
    Returns (starting_number, length).
    
    Example: max_collatz_length(20) → (18, 20)
    (18 produces the longest sequence for starting numbers 1-20)
    
    Use nested loops: outer for loop over 1..limit, inner while loop for Collatz.
    """
    # TODO: implement
    pass


# ─── Exercise 3.2: Prime Sieve ────────────────────────────────────────────────

def sieve_of_eratosthenes(n):
    """
    Return a list of all prime numbers up to and including n.
    
    Algorithm:
    1. Create a boolean list is_prime[0..n], initialized to True
    2. Set is_prime[0] = is_prime[1] = False
    3. For each p from 2 to sqrt(n):
         if is_prime[p]:
             mark is_prime[p*p], is_prime[p*p + p], ... as False
    4. Return all i where is_prime[i] is True
    
    Hint: use while p*p <= n for the outer loop condition.
    
    Examples:
        sieve_of_eratosthenes(10)  → [2, 3, 5, 7]
        sieve_of_eratosthenes(30)  → [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        sieve_of_eratosthenes(1)   → []
    """
    # TODO: implement
    pass


def prime_gaps(n):
    """
    Return a list of gaps between consecutive primes up to n.
    
    Example: prime_gaps(30) → [1, 2, 2, 4, 2, 4, 2, 4, 6]
    (gaps between 2,3,5,7,11,13,17,19,23,29)
    
    Use sieve_of_eratosthenes(), then compute gaps with a for loop.
    """
    # TODO: implement
    pass


# ─── Exercise 3.3: FizzBuzz Extended ─────────────────────────────────────────

def fizzbuzz_range(start, end, rules=None):
    """
    Generalized FizzBuzz for any range and any set of rules.
    
    rules: list of (divisor, word) tuples, e.g. [(3,"Fizz"), (5,"Buzz"), (7,"Bazz")]
    If rules is None, use the standard [(3,"Fizz"), (5,"Buzz")].
    
    For each n in [start, end] (inclusive):
        - Concatenate words for all divisors that divide n (in rule order)
        - If no divisors match, use str(n)
    
    Return a list of strings.
    
    Examples:
        fizzbuzz_range(1, 15) → ["1","2","Fizz","4","Buzz","Fizz","7","8",
                                  "Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]
        fizzbuzz_range(1, 21, [(3,"Fizz"),(5,"Buzz"),(7,"Bazz")]) → 
            ["1","2","Fizz","4","Buzz","Fizz","Bazz","8","Fizz","Buzz",
             "11","Fizz","13","Bazz","FizzBuzz","16","17","Fizz","19",
             "Buzz","FizzBazz"]
    """
    if rules is None:
        rules = [(3, "Fizz"), (5, "Buzz")]
    # TODO: implement
    pass


# ─── Exercise 3.4: Digital Root ───────────────────────────────────────────────

def digital_root(n):
    """
    Repeatedly sum the digits of n until the result is a single digit.
    
    This is called the digital root.
    
    Examples:
        digital_root(493)  → 7  (4+9+3=16, 1+6=7)
        digital_root(942)  → 6  (9+4+2=15, 1+5=6)
        digital_root(7)    → 7  (already single digit)
        digital_root(0)    → 0
    
    Use nested while loops: outer loop until single digit, inner loop sums digits.
    
    Invariant for outer loop: n > 0 (or n == 0 as a special case)
    State the invariant in a comment inside your implementation.
    """
    # TODO: implement
    pass


# ─── Exercise 3.5: Caesar Cipher ──────────────────────────────────────────────

def caesar_encrypt(text, shift):
    """
    Apply a Caesar cipher to text with the given shift.
    
    Rules:
    - Shift only alphabetic characters (a-z, A-Z)
    - Preserve case: 'A' shifted by 3 → 'D', 'z' shifted by 3 → 'c'
    - Wrap around: 'Y' shifted by 3 → 'B', 'z' shifted by 3 → 'c'
    - Leave non-alphabetic characters unchanged (spaces, punctuation, digits)
    - Handle negative shifts (shift of -3 is the same as shift of 23)
    
    Hint: use ord() to get the ASCII code, chr() to convert back.
    For uppercase: new_char = chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
    
    Examples:
        caesar_encrypt("Hello, World!", 3)  → "Khoor, Zruog!"
        caesar_encrypt("abc", 1)            → "bcd"
        caesar_encrypt("xyz", 3)            → "abc"
        caesar_encrypt("ABC", -3)           → "XYZ"
    """
    # TODO: implement using a for loop over characters
    pass


def caesar_decrypt(text, shift):
    """Decrypt a Caesar cipher. One line using caesar_encrypt."""
    # TODO: one line — use caesar_encrypt with a negative shift
    pass


# ─── Tests ────────────────────────────────────────────────────────────────────

def run_tests():
    """Run all tests. Any failure will raise AssertionError with a message."""
    
    # Test collatz_length
    assert collatz_length(1)  == 0,  f"collatz(1) should be 0, got {collatz_length(1)}"
    assert collatz_length(6)  == 8,  f"collatz(6) should be 8, got {collatz_length(6)}"
    assert collatz_length(27) == 111, f"collatz(27) should be 111, got {collatz_length(27)}"
    print("✓ collatz_length")
    
    # Test max_collatz_length
    n, length = max_collatz_length(20)
    assert n == 18 and length == 20, f"max_collatz(20) should be (18,20), got ({n},{length})"
    print("✓ max_collatz_length")
    
    # Test sieve
    assert sieve_of_eratosthenes(10) == [2, 3, 5, 7]
    assert sieve_of_eratosthenes(1)  == []
    assert sieve_of_eratosthenes(2)  == [2]
    assert len(sieve_of_eratosthenes(100)) == 25  # There are 25 primes ≤ 100
    print("✓ sieve_of_eratosthenes")
    
    # Test prime_gaps
    assert prime_gaps(10) == [1, 2, 2]  # gaps: 2→3=1, 3→5=2, 5→7=2
    print("✓ prime_gaps")
    
    # Test fizzbuzz
    result = fizzbuzz_range(1, 15)
    assert result[0]  == "1",        f"fizzbuzz[0] should be '1'"
    assert result[2]  == "Fizz",     f"fizzbuzz[2] should be 'Fizz'"
    assert result[4]  == "Buzz",     f"fizzbuzz[4] should be 'Buzz'"
    assert result[14] == "FizzBuzz", f"fizzbuzz[14] should be 'FizzBuzz'"
    print("✓ fizzbuzz_range")
    
    # Test digital_root
    assert digital_root(493) == 7
    assert digital_root(0)   == 0
    assert digital_root(7)   == 7
    assert digital_root(999) == 9  # 9+9+9=27, 2+7=9
    print("✓ digital_root")
    
    # Test caesar
    assert caesar_encrypt("Hello, World!", 3) == "Khoor, Zruog!"
    assert caesar_encrypt("xyz", 3)           == "abc"
    assert caesar_encrypt("ABC", -3)          == "XYZ"
    assert caesar_decrypt(caesar_encrypt("Secret message!", 13), 13) == "Secret message!"
    print("✓ caesar_encrypt / decrypt")
    
    print("\n🎉 All tests passed!")


if __name__ == "__main__":
    run_tests()
```

---

## Part 4: Loop Invariant Documentation (15 minutes)

For **three** of your implementations above, add a detailed invariant comment block using this template:

```python
def your_function(args):
    """Docstring."""
    
    # === Loop Invariant ===
    # At the start of each iteration:
    #   [state the invariant precisely]
    #
    # Initialization establishes invariant because:
    #   [explain why the initial values satisfy the invariant]
    #
    # Body preserves invariant because:
    #   [explain why each case in the body keeps the invariant true]
    #
    # Termination: [explain why the loop always terminates]
    #
    # Correctness: [how invariant + exit condition proves the function is correct]
    # =====================
    
    # ... implementation ...
```

This is not just an academic exercise — this is how professional code is documented in safety-critical systems, compilers, and operating system kernels.

---

## Part 5: Commit and Reflection (15 minutes)

```bash
cd ~/cs101/week2
git add .
git commit -m "Week 2 Lab: debugging, loop invariants, Collatz, Sieve, Caesar cipher"
git push
```

### Reflection — add to `LAB 2 Debugging and Loops.md`:

**Q1.** You fixed 5 bugs using print debugging. Which of these categories did each bug fall into?
- Wrong initialization
- Wrong condition (off-by-one, wrong operator)
- Wrong update
- Wrong return value
- Wrong accumulation operation

**Q2.** You stated loop invariants for 3 of your implementations. For one of them: prove that the invariant is maintained. That is, show that if the invariant is true at the start of an iteration, it is still true at the end.

**Q3.** The Newton-Raphson square root converges *quadratically*: the number of correct digits roughly doubles each iteration. But a linear search for the root (try 0.5, 1.0, 1.5, ...) converges linearly: the number of correct digits increases by a fixed amount each iteration. Why does this difference matter for large problems? What does it mean in terms of iteration count needed for 10 decimal places of accuracy?

**Q4.** When debugging `bug_4()`, the issue was initializing `current_max = 0` instead of `current_max = lst[0]`. Connect this to the concept of a loop invariant: what invariant was being violated by the wrong initialization?

---

## TA Checkoff Criteria

Show your TA:
- [ ] Exercise 1.1 state table (at least 8 rows) — done on paper
- [ ] All 5 bugs in `debug_exercise.py` fixed and explained
- [ ] `loops.py` with all 5 functions passing `run_tests()`
- [ ] 3 loop invariant comment blocks in `loops.py`
- [ ] PDB exercise completed with convergence questions answered

---

## Bonus Challenges

**Bonus 1 — Longest Collatz chain under 1,000,000:**
Which starting number under one million produces the longest Collatz sequence? (This is Project Euler problem #14.) Warning: this will take a few seconds to compute naively. Can you make it faster with memoization (saving results you've already computed)?

**Bonus 2 — Prime number theorem:**
The prime number theorem states that the number of primes ≤ n is approximately n/ln(n). Use your sieve to verify this for n = 100, 1000, 10000, 100000. How good is the approximation?

**Bonus 3 — Vigenère cipher:**
The Vigenère cipher uses a keyword instead of a fixed shift. Each letter of the plaintext is shifted by the corresponding letter of the keyword (cycling). Implement `vigenere_encrypt(text, key)` and `vigenere_decrypt(text, key)`.

---

*CS 101 · Week 2 · Lab 2 · © CSE Department*
