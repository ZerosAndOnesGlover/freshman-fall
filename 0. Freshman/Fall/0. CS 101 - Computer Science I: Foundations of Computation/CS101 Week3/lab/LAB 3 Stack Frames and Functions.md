# CS 101 · Lab 3
## Stack Frame Visualization and Function Design

**Tuesday of Week 4 · Lab Section** — sat after this week's Wed–Fri lectures, and covers Week 3.
*Duration: 2 hours · Graded on completion (TA checkoff)*

---

## Objectives

By the end of this lab, you will:
- [ ] Visualize stack frames using Python Tutor for at least 5 programs
- [ ] Explain precisely what happens to variables when a function is called and returns
- [ ] Identify and fix scope-related bugs
- [ ] Apply the mutable default argument trap and fix it
- [ ] Design a decomposed multi-function program from scratch
- [ ] Write tests alongside every function you implement

---

## Setup

```bash
cd ~/cs101
mkdir week3 && cd week3
```

Open Python Tutor: **https://pythontutor.com/python-3.html**

Keep it open in a browser tab throughout the lab. Every exercise says "Python Tutor" — use it for that one.

---

## Part 1: Stack Frame Visualization (35 minutes)

For each exercise: paste the code into Python Tutor, step through it **completely**, then answer the questions in `LAB 3 Stack Frames and Functions.md`.

### Exercise 1.1: The Fundamental Call Stack

```python
def square(x):
    result = x * x
    return result

def sum_of_squares(a, b):
    sq_a = square(a)
    sq_b = square(b)
    return sq_a + sq_b

answer = sum_of_squares(3, 4)
print(answer)
```

Step through every line in Python Tutor. At the moment `square(3)` is executing, count the frames on the stack.

**Answer in `LAB 3 Stack Frames and Functions.md`:**
1. How many stack frames exist when `square(3)` is running?
2. What are they, from bottom to top?
3. When `square(3)` returns, where does the value `9` go?
4. Does `x` in `square(3)` interfere with anything in `sum_of_squares`?
5. After `sum_of_squares` returns, what happens to `sq_a` and `sq_b`?

### Exercise 1.2: The LEGB Rule in Action

```python
x = "global"

def outer():
    x = "outer"

    def inner():
        print(x)   # Which x?

    inner()
    print(x)       # Which x?

outer()
print(x)           # Which x?
```

Before running: **predict each `print` output.** Then step through Python Tutor.

**Answer:**
1. What does each `print` output and why?
2. At the moment `inner()` is executing, how many frames are on the stack?
3. Modify the code so `inner()` prints `"global"` instead of `"outer"`. What changes?

### Exercise 1.3: The Mutable Default Trap

```python
def add_item(item, collection=[]):
    collection.append(item)
    return collection

r1 = add_item("apple")
r2 = add_item("banana")
r3 = add_item("cherry")
print(r1, r2, r3)
```

Step through in Python Tutor. Watch what happens to the default list object across calls.

**Answer:**
1. What is printed? Why?
2. At what point in execution is the default `[]` created?
3. How many times is the default `[]` created total?
4. Rewrite `add_item` correctly (using `None` as default). Paste the corrected version.

### Exercise 1.4: Global vs. Local

```python
total = 0

def add_to_total(n):
    total = total + n   # Is this the global total or a new local?
    return total

add_to_total(5)
```

**Before running:** predict what happens.

Then run it and observe the `UnboundLocalError`.

**Answer:**
1. Why does `UnboundLocalError` occur here? Explain precisely using what you know about how Python determines scope.
2. Write two corrected versions:
   - Version A: use `global total`
   - Version B: remove the global, take `total` as a parameter and return the new total
3. Which version is better design and why?

### Exercise 1.5: Return Values vs. Print

```python
def double_print(x):
    print(x * 2)

def double_return(x):
    return x * 2

# Attempt to use both in a computation:
a = double_print(5) + 1    # What happens?
b = double_return(5) + 1   # What happens?
```

**Answer:**
1. What error occurs on the `double_print` line? Explain why.
2. What does `double_return` return? What is the value of `b`?
3. Why can `double_return` be used in expressions but `double_print` cannot?

---

## Part 2: Scope Bug Hunt (20 minutes)

Create `scope_bugs.py`. Each function has a scope-related bug. Find it, explain it, and fix it.

```python
# scope_bugs.py
# CS 101 — Week 3, Lab 3
# Scope bug hunt: find, explain, and fix each bug.

# ─── Bug 1 ────────────────────────────────────────────────────────────────────
# This should accumulate a running total across calls.
running_total = 0

def accumulate(n):
    running_total += n    # Bug: what kind of error does this cause?
    return running_total

# accumulate(5)   # Uncomment to test
# accumulate(3)


# ─── Bug 2 ────────────────────────────────────────────────────────────────────
# This should return a list with the item appended, WITHOUT modifying the input.
def append_copy(lst, item):
    lst.append(item)     # Bug: what is wrong with this?
    return lst

original = [1, 2, 3]
new_list = append_copy(original, 4)
# After this call, original should still be [1, 2, 3].
# Is it?


# ─── Bug 3 ────────────────────────────────────────────────────────────────────
# This factory is supposed to create different multiplier functions.
def make_multipliers():
    multipliers = []
    for factor in [1, 2, 3, 4, 5]:
        multipliers.append(lambda x: x * factor)   # Bug: closure trap!
    return multipliers

fns = make_multipliers()
# fns[0](10) should be 10, fns[1](10) should be 20, etc.
# Are they? Run it and see. Explain why.


# ─── Bug 4 ────────────────────────────────────────────────────────────────────
# This should return the maximum of a list, defaulting to 0 for empty lists.
def safe_max(lst, default=0):
    if lst == []:
        return default
    max_val = lst[0]
    for x in lst:
        if x > max_val:
            max_val = x
    return max_val

# This seems fine. But what's the subtle bug with the default parameter?
# Hint: try calling safe_max() with no arguments after calling safe_max([1,2,3]).
# (Trick question — there ISN'T a bug here. Explain WHY not. What makes
#  default=0 safe but default=[] would be dangerous?)


# ─── Bug 5 ────────────────────────────────────────────────────────────────────
# This should shadow the built-in len correctly. What's wrong?
def analyze(data):
    len = 0                      # Bug: this shadows the built-in!
    for item in data:
        len += 1
    average = sum(data) / len    # Does this work?
    return len, average

# analyze([1, 2, 3, 4, 5])
```

**For each bug:**
1. What is the exact error (or wrong behavior)?
2. Why does it happen? (Reference the LEGB rule or mutability as appropriate)
3. Write the corrected version

---

## Part 3: Function Design Workshop (35 minutes)

Design and implement a complete, well-decomposed program. This is the main exercise.

Create `text_statistics.py`.

### Specification

Write a **text analysis library** with the following public interface:

```python
analyze(text)           → dict with all statistics below
word_count(text)        → int
sentence_count(text)    → int
average_word_length(text) → float
longest_word(text)      → str
shortest_word(text)     → str
char_frequency(text)    → list of (char, count) tuples, sorted by count desc
is_pangram(text)        → bool
reading_level(text)     → str  # "Elementary", "Middle", "High School", or "College"
```

**Reading level heuristic** (Flesch-Kincaid simplified):
- average words per sentence < 10 → "Elementary"
- average words per sentence < 15 → "Middle"
- average words per sentence < 20 → "High School"
- otherwise → "College"

### Requirements

1. **Each function must:**
   - Have a complete docstring (what it does, args, returns, example)
   - Be independently testable
   - Have at least 2 `assert` tests below its definition

2. **`analyze(text)` must:**
   - Call all other functions (not re-implement their logic)
   - Return a dictionary with keys matching the function names

3. **No function may:**
   - Print anything (all output goes through a separate `display` function)
   - Modify its arguments

4. **Helper functions:**
   - Any shared logic must go in a helper (prefix with `_`)
   - Helpers must also have docstrings

### Starter structure:

```python
#!/usr/bin/env python3
"""
text_statistics.py
CS 101 — Week 3, Lab 3

Text analysis library demonstrating function decomposition.

Student: ____________________________
Date: ______________________________
"""


def _clean_text(text):
    """
    Return lowercase text stripped of leading/trailing whitespace.
    Internal helper used by multiple functions.

    >>> _clean_text("  Hello World!  ")
    'hello world!'
    """
    return text.strip().lower()


def _tokenize(text):
    """
    Split text into a list of words (lowercase, whitespace-split).

    >>> _tokenize("The quick brown fox")
    ['the', 'quick', 'brown', 'fox']
    """
    return _clean_text(text).split()


def word_count(text):
    """
    Return the number of words in text.

    >>> word_count("Hello world")
    2
    >>> word_count("")
    0
    """
    # TODO
    pass


def sentence_count(text):
    """
    Return the number of sentences (count of . ! ? characters).

    >>> sentence_count("Hello! How are you? I'm fine.")
    3
    >>> sentence_count("No punctuation here")
    0
    """
    # TODO
    pass


def average_word_length(text):
    """
    Return the mean number of characters per word.
    Return 0.0 if there are no words.

    >>> average_word_length("cat dog bird")
    3.0
    >>> average_word_length("")
    0.0
    """
    # TODO
    pass


def longest_word(text):
    """
    Return the longest word in text (first one if there's a tie).
    Return "" if text has no words.

    >>> longest_word("the quick brown fox")
    'quick'
    """
    # TODO
    pass


def shortest_word(text):
    """
    Return the shortest word in text (first one if there's a tie).
    Return "" if text has no words.

    >>> shortest_word("the quick brown fox")
    'the'
    """
    # TODO
    pass


def char_frequency(text):
    """
    Return a list of (char, count) tuples for all alphabetic characters,
    sorted by count descending, then alphabetically for ties.
    Text is case-insensitive.

    >>> char_frequency("aabbc")
    [('a', 2), ('b', 2), ('c', 1)]

    Hint: use nested loops — no dictionaries allowed.
    """
    # TODO
    pass


def is_pangram(text):
    """
    Return True if text contains every letter a-z at least once.
    Case-insensitive.

    >>> is_pangram("The quick brown fox jumps over the lazy dog")
    True
    >>> is_pangram("Hello world")
    False
    """
    # TODO
    pass


def reading_level(text):
    """
    Estimate reading level based on average words per sentence.

    Heuristic:
        avg_words_per_sentence < 10  → "Elementary"
        avg_words_per_sentence < 15  → "Middle"
        avg_words_per_sentence < 20  → "High School"
        otherwise                    → "College"

    If there are no sentences (no .!?), return "Unknown".

    >>> reading_level("I am. You are. He is.")
    'Elementary'
    """
    # TODO
    pass


def analyze(text):
    """
    Run all analyses on text and return a dictionary.

    Keys: word_count, sentence_count, average_word_length,
          longest_word, shortest_word, char_frequency,
          is_pangram, reading_level

    This function must CALL the other functions — not reimplement them.
    """
    # TODO
    pass


def display_report(text):
    """
    Print a formatted analysis report for text.
    This is the ONLY function that may print.
    """
    results = analyze(text)

    print("=" * 50)
    print("TEXT ANALYSIS REPORT")
    print("=" * 50)
    print(f"  Word count:          {results['word_count']}")
    print(f"  Sentence count:      {results['sentence_count']}")
    print(f"  Avg word length:     {results['average_word_length']:.2f}")
    print(f"  Longest word:        {results['longest_word']}")
    print(f"  Shortest word:       {results['shortest_word']}")
    print(f"  Is pangram:          {results['is_pangram']}")
    print(f"  Reading level:       {results['reading_level']}")
    print()
    print("  Top 5 most frequent characters:")
    for char, count in results['char_frequency'][:5]:
        bar = "█" * count
        print(f"    '{char}': {bar} ({count})")
    print("=" * 50)


def run_tests():
    """Run all assertion tests."""

    # word_count
    assert word_count("hello world") == 2
    assert word_count("") == 0
    assert word_count("  spaces  ") == 1
    print("✓ word_count")

    # sentence_count
    assert sentence_count("Hello! How are you? I'm fine.") == 3
    assert sentence_count("No punctuation") == 0
    print("✓ sentence_count")

    # average_word_length
    assert average_word_length("cat dog bird") == 3.0
    assert average_word_length("") == 0.0
    print("✓ average_word_length")

    # longest_word
    assert longest_word("the quick brown fox") == "quick"
    assert longest_word("") == ""
    print("✓ longest_word")

    # shortest_word
    assert shortest_word("the quick brown fox") == "the"
    assert shortest_word("") == ""
    print("✓ shortest_word")

    # char_frequency
    freq = char_frequency("aabbc")
    assert freq[0][1] >= freq[1][1]   # sorted descending by count
    print("✓ char_frequency")

    # is_pangram
    assert is_pangram("The quick brown fox jumps over the lazy dog") == True
    assert is_pangram("Hello world") == False
    print("✓ is_pangram")

    # reading_level
    assert reading_level("I am. You are. He is.") == "Elementary"
    print("✓ reading_level")

    # analyze
    results = analyze("The quick brown fox jumps over the lazy dog.")
    assert "word_count" in results
    assert results["is_pangram"] == True
    print("✓ analyze")

    print("\n🎉 All tests passed!")


if __name__ == "__main__":
    run_tests()

    sample = """
    The quick brown fox jumps over the lazy dog.
    Pack my box with five dozen liquor jugs.
    How vexingly quick daft zebras jump!
    The five boxing wizards jump quickly.
    """
    display_report(sample)
```

---

## Part 4: Recursion First Look (10 minutes)

Create `recursion_intro.py`. These are simple recursive functions — focus on understanding the stack, not on efficiency.

```python
# recursion_intro.py
# CS 101 — Week 3, Lab 3
# First recursive functions. Visualize each one in Python Tutor.

def factorial(n):
    """
    Return n! using recursion.
    Base case: factorial(0) = 1
    Recursive case: factorial(n) = n * factorial(n-1)
    """
    assert n >= 0 and isinstance(n, int)
    if n == 0:
        return 1
    return n * factorial(n - 1)


def count_down(n):
    """
    Print n, n-1, n-2, ..., 1, 0 using recursion.
    Base case: count_down(0) prints 0 and stops.
    Recursive case: print n, then count_down(n-1).
    """
    print(n)
    if n > 0:
        count_down(n - 1)


def power(base, exp):
    """
    Compute base**exp using recursion (exp is a non-negative integer).
    Base case: power(base, 0) = 1
    Recursive case: power(base, exp) = base * power(base, exp - 1)
    """
    # TODO: implement
    pass


def sum_digits(n):
    """
    Return the sum of digits of non-negative integer n using recursion.
    Base case: single digit → return n
    Recursive case: last digit (n%10) + sum_digits(n//10)

    sum_digits(1234) → 10
    """
    # TODO: implement
    pass


# Tests:
assert factorial(0) == 1
assert factorial(5) == 120
assert factorial(10) == 3628800
print("✓ factorial")

assert power(2, 0)  == 1
assert power(2, 10) == 1024
assert power(3, 4)  == 81
print("✓ power")

assert sum_digits(0)    == 0
assert sum_digits(9)    == 9
assert sum_digits(1234) == 10
assert sum_digits(9999) == 36
print("✓ sum_digits")

print("\nVisualize in Python Tutor:")
print("  factorial(5) — count how deep the stack gets")
print("  sum_digits(123) — trace how the result is assembled")
```

**Python Tutor task:** Visualize `factorial(5)`. At the deepest point, how many frames are on the stack? What is the maximum `n` value where `factorial(n)` wouldn't hit Python's recursion limit?

---

## Part 5: Commit (10 minutes)

```bash
cd ~/cs101/week3
git add .
git commit -m "Week 3 Lab: scope bugs, stack frames, text analysis library, recursion intro"
git push
```

### Reflection in `LAB 3 Stack Frames and Functions.md`:

**Q1.** In Exercise 1.3 (mutable default trap), the bug occurs because the default `[]` is evaluated once at function definition time. Why does Python work this way? (Hint: think about what `def` actually does — it's a statement that creates a function object. When is that statement executed?)

**Q2.** In Exercise 1.4, you wrote two corrected versions of `add_to_total` — one using `global`, one using a parameter. For what kind of situation might the `global` version actually be appropriate? For what kind of situation is the parameter version strictly better?

**Q3.** In the `text_statistics.py` design, `display_report` is the only function that prints. Why is this a good design principle? What would be harder if every function printed its own output?

**Q4.** You implemented `factorial` recursively and previously implemented it with a `while` loop. Both are correct. What is one situation where the recursive version is *preferable*? What is one situation where the iterative version is preferable?

---

## TA Checkoff Criteria

Show your TA:
- [ ] Python Tutor answers for Exercises 1.1–1.5 in `LAB 3 Stack Frames and Functions.md`
- [ ] All 5 bugs in `scope_bugs.py` identified, explained, and fixed
- [ ] `text_statistics.py` with all functions implemented and all tests passing
- [ ] `recursion_intro.py` with `power` and `sum_digits` implemented and tests passing
- [ ] Git log showing commits

---

## Bonus Challenges

**Bonus 1:** Add a `compare_texts(text1, text2)` function to `text_statistics.py` that prints a side-by-side comparison of two texts' statistics.

**Bonus 2:** Implement `flatten(lst)` recursively — given a list that may contain nested lists, return a flat list of all elements: `flatten([1,[2,[3,4]],5]) → [1,2,3,4,5]`.

**Bonus 3:** Implement the Tower of Hanoi recursively: `hanoi(n, from_peg, to_peg, via_peg)` prints the sequence of moves to transfer n disks from `from_peg` to `to_peg` using `via_peg` as auxiliary. The algorithm is 3 lines of code. Visualize `hanoi(3, 'A', 'C', 'B')` in Python Tutor.

---

*CS 101 · Week 3 · Lab 3 · © CSE Department*
