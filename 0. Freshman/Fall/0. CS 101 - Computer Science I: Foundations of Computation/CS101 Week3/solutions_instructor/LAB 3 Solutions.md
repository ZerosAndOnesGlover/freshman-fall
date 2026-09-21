# CS 101 · Week 3
## LAB 3 Solutions (INSTRUCTOR ONLY)

> Lab sat Tuesday 20 October 2026. **All code below was executed and all stated outputs are real.**

---

## Part 1, Exercise 1.1 — The Fundamental Call Stack

1. **Three frames** while `square(3)` runs.
2. Bottom to top: **`<module>` → `sum_of_squares` → `square`**. The module-level frame is a real
   frame and students routinely forget it; `answer` lives there.
3. **`9` is returned to the point of call** — it becomes the value of the expression `square(a)`,
   which is then bound to `sq_a` in `sum_of_squares`'s frame. It does not "go" to `square`'s frame,
   which is destroyed at that instant.
4. **No.** `x` exists only in `square`'s frame. Each call gets a fresh frame with its own `x`, which
   is precisely why recursion works at all.
5. **`sq_a` and `sq_b` are destroyed** with the frame. Only the returned value survives, bound to
   `answer` in the module frame.

The sentence to extract: **a frame is created per *call*, not per *function*.**

---

## Exercise 1.2 — LEGB

Output:

```
outer
outer
global
```

1. `inner`'s `print(x)` finds no local `x`, so it looks **E**nclosing and finds `outer`'s. The second
   `print` is in `outer` itself, which has a local `x = "outer"`. The third is module level.
2. **Three frames** while `inner()` runs: `<module>` → `outer` → `inner`. A student who answers
   four is counting the `print` call — which genuinely *is* a fourth frame while it executes, but
   `print` is a C builtin and Python Tutor does not show a frame for it. **Accept 3; accept 4 only
   if they name the `print` frame explicitly.**
3. To make `inner` print `"global"`, add **`global x`** inside `inner`. Note `nonlocal x` would
   *not* work — it binds to `outer`'s `x`, which is the value already being printed. Students who
   propose `nonlocal` have the direction confused and should trace it.

---

## Exercise 1.3 — The Mutable Default Trap

1. **`['apple','banana','cherry'] ['apple','banana','cherry'] ['apple','banana','cherry']`** — all
   three names label the **same list object** (`r1 is r2 is r3` is `True`).
2. The default `[]` is created **when the `def` statement executes**, i.e. once at function
   definition time, not at call time.
3. **Exactly once**, for the life of the program. Inspect it with `add_item.__defaults__`, which
   after the three calls shows `(['apple','banana','cherry'],)` — the accumulated list is stored on
   the function object itself.
4. Corrected:

```python
def add_item(item, collection=None):
    if collection is None:
        collection = []
    collection.append(item)
    return collection
```

Use `is None`, **not** `if not collection` — the latter also replaces a caller's deliberately empty
list with a new one, silently discarding their object.

---

## Exercise 1.4 — `UnboundLocalError`

1. Python decides a variable's scope **at compile time, for the entire function body**. Because
   `total` is assigned somewhere in `add_to_total`, `total` is local *throughout* the function —
   including on the right-hand side of the very statement that assigns it. The global is not
   shadowed at that point; it is **invisible from that function entirely**. So `total + n` reads a
   local that has not yet been given a value.

   Exact message: `UnboundLocalError: cannot access local variable 'total' where it is not
   associated with a value`.

2. **Version A:**

```python
total = 0
def add_to_total(n):
    global total
    total = total + n
    return total
```

   **Version B:**

```python
def add_to_total(total, n):
    return total + n
```

3. **Version B is better.** It is a **pure function**: same inputs always give the same output, no
   hidden state, testable with a single `assert`, safe to call from anywhere and in any order, and
   trivially parallelisable. Version A couples the function to one module-level variable, makes the
   result depend on call history, and forces any test to reset the global first. The general rule —
   *push state to the edges, keep the middle pure* — is the design lesson of Week 3.

---

## Exercise 1.5 — Return vs. Print

1. **`TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'`.** `double_print` prints
   `10` and then falls off the end, returning `None`. `None + 1` is a type error. Note the `10`
   **is** printed before the error — the side effect happens, the value does not exist.
2. `double_return(5)` returns `10`, so **`b == 11`**.
3. Because **only a returned value can participate in an expression.** Printing sends characters to
   a stream; it produces no value for the caller. This is the single most common beginner confusion,
   and the diagnostic question is: *could I assign the result to a variable and use it later?*

---

## Part 2 — Scope Bug Hunt (20, 5 each)

| Case | What happens | Why | Fix |
|---|---|---|---|
| 1 `accumulate` | `UnboundLocalError` | `running_total += n` assigns, so `running_total` is local for the whole body (L11 LEGB) | Better: take the total as a parameter and return the new one; or `global running_total` |
| 2 `append_copy` | `original` becomes `[1, 2, 3, 4]` | `lst` and `original` name one list; `append` mutates it | `return lst + [item]` builds a new list |
| 3 `safe_max` | **no bug** | `default=0` is an immutable `int`; a shared default is only dangerous when it is mutable (`[]`) and then mutated | — (the explanation earns the 5) |
| 4 `analyze` | works here, but `len` is now a local `int` | the local name hides the built-in inside `analyze`; any `len(...)` call there would fail with `TypeError: 'int' object is not callable` | rename to `count` |

---

## Part 3 — `text_statistics.py` (35)

Reference implementation (the handout's starter with every `TODO` filled). `run_tests()` passes and
the report prints:

```
Word count:          29
Sentence count:      4
Avg word length:     4.55
Longest word:        vexingly
Shortest word:       my
Is pangram:          True
Reading level:       Elementary
```

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
    return len(_tokenize(text))


def sentence_count(text):
    """
    Return the number of sentences (count of . ! ? characters).

    >>> sentence_count("Hello! How are you? I'm fine.")
    3
    >>> sentence_count("No punctuation here")
    0
    """
    count = 0
    for ch in text:
        if ch in ".!?":
            count += 1
    return count


def average_word_length(text):
    """
    Return the mean number of characters per word.
    Return 0.0 if there are no words.

    >>> average_word_length("cat dog owl")
    3.0
    >>> average_word_length("")
    0.0
    """
    words = _tokenize(text)
    if not words:
        return 0.0
    total = 0
    for w in words:
        total += len(w)
    return total / len(words)


def longest_word(text):
    """
    Return the longest word in text (first one if there's a tie).
    Return "" if text has no words.

    >>> longest_word("the quick brown fox")
    'quick'
    """
    best = ""
    for w in _tokenize(text):
        if len(w) > len(best):
            best = w
    return best


def shortest_word(text):
    """
    Return the shortest word in text (first one if there's a tie).
    Return "" if text has no words.

    >>> shortest_word("the quick brown fox")
    'the'
    """
    words = _tokenize(text)
    if not words:
        return ""
    best = words[0]
    for w in words:
        if len(w) < len(best):
            best = w
    return best


def is_pangram(text):
    """
    Return True if text contains every letter a-z at least once.
    Case-insensitive.

    >>> is_pangram("The quick brown fox jumps over the lazy dog")
    True
    >>> is_pangram("Hello world")
    False
    """
    lowered = text.lower()
    for letter in "abcdefghijklmnopqrstuvwxyz":
        if letter not in lowered:
            return False
    return True


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
    sentences = sentence_count(text)
    if sentences == 0:
        return "Unknown"
    avg = word_count(text) / sentences
    if avg < 10:
        return "Elementary"
    if avg < 15:
        return "Middle"
    if avg < 20:
        return "High School"
    return "College"


def display_report(text):
    """
    Print a formatted analysis report for text.
    This is the ONLY function that may print.
    """
    print("=" * 50)
    print("TEXT ANALYSIS REPORT")
    print("=" * 50)
    print(f"  Word count:          {word_count(text)}")
    print(f"  Sentence count:      {sentence_count(text)}")
    print(f"  Avg word length:     {average_word_length(text):.2f}")
    print(f"  Longest word:        {longest_word(text)}")
    print(f"  Shortest word:       {shortest_word(text)}")
    print(f"  Is pangram:          {is_pangram(text)}")
    print(f"  Reading level:       {reading_level(text)}")
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
    assert average_word_length("cat dog owl") == 3.0
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

    # is_pangram
    assert is_pangram("The quick brown fox jumps over the lazy dog") == True
    assert is_pangram("Hello world") == False
    print("✓ is_pangram")

    # reading_level
    assert reading_level("I am. You are. He is.") == "Elementary"
    print("✓ reading_level")

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

**Checkoff:** every function implemented (4 each for the seven = 28); `display_report` calls the
others rather than recomputing (4); `print(` appears only in `display_report` and `run_tests` (3).
`average_word_length("")` must return `0.0`, not raise `ZeroDivisionError` — the commonest crash.
Punctuation stays attached to words (`"dog."` has length 4); that is acceptable because the spec
splits on whitespace.

---

## Part 4 — Recursion First Look (15)

```python
def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)

def sum_digits(n):
    if n < 10:
        return n
    return n % 10 + sum_digits(n // 10)
```

All handout asserts pass (`power(3, 4) == 81`, `sum_digits(9999) == 36`). `factorial(5)` reaches 7
frames at its deepest (module + 6 calls, `n = 5 … 0`). 8 for `power`, 7 for `sum_digits`.

---

*CS 101 · Week 3 · Lab 3 Solutions · Instructor only*
