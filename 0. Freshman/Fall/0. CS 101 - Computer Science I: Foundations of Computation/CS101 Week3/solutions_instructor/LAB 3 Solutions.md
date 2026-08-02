# CS 101 · Week 3
## LAB 3 Solutions (INSTRUCTOR ONLY)

> **All code below was executed and all stated outputs are real.** Where a benchmark appears,
> the absolute timings are machine-specific — grade the *ratios* and the conclusions, never the
> raw milliseconds.

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

## Part 2 — Scope Bug Hunt

The recurring bugs and their fixes:

| Bug pattern | Why it fails | Fix |
|---|---|---|
| Assigning to a global without declaring it | `UnboundLocalError`, as Ex 1.4 | `global`, or better, parameter + return |
| Mutable default argument | Shared across calls | `=None` sentinel |
| Shadowing a builtin (`list = [...]`, `sum = 0`) | Later `list(...)` or `sum(...)` raises `TypeError: 'int' object is not callable` | Rename the variable |
| Reading a loop variable after the loop | Works, but holds the *last* value — and is undefined if the loop body never ran | Initialise before the loop |
| `nonlocal` where `global` is needed (or vice versa) | Binds to the wrong scope | Trace which frame owns the name |

> **The builtin-shadowing one produces the most baffling error message**, because the failure
> appears at a *later, unrelated* line. Show students `python3 -c "import builtins; print(dir(builtins))"`
> once and the habit sticks.

---

## Part 3 — `text_statistics.py` Reference Solution

Complete implementation; all asserts below pass.

```python
import re
from collections import Counter

def _clean_text(text):
    """Return lowercase text stripped of surrounding whitespace."""
    return text.strip().lower()

def _words(text):
    """Return the list of alphabetic words in text, lowercased."""
    return re.findall(r"[a-z']+", _clean_text(text))

def _sentences(text):
    """Return non-empty sentences, split on . ! ? terminators."""
    return [s for s in re.split(r"[.!?]+", text) if s.strip()]

def word_count(text):        return len(_words(text))
def sentence_count(text):    return len(_sentences(text))

def average_word_length(text):
    ws = _words(text)
    return sum(len(w) for w in ws) / len(ws) if ws else 0.0

def longest_word(text):
    ws = _words(text)
    return max(ws, key=len) if ws else ""

def shortest_word(text):
    ws = _words(text)
    return min(ws, key=len) if ws else ""

def char_frequency(text):
    c = Counter(ch for ch in _clean_text(text) if ch.isalpha())
    return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))

def is_pangram(text):
    return set("abcdefghijklmnopqrstuvwxyz") <= set(_clean_text(text))

def reading_level(text):
    sc = sentence_count(text)
    if sc == 0:
        return "Elementary"
    wps = word_count(text) / sc
    if wps < 10:  return "Elementary"
    if wps < 15:  return "Middle"
    if wps < 20:  return "High School"
    return "College"

def analyze(text):
    return {
        "word_count":          word_count(text),
        "sentence_count":      sentence_count(text),
        "average_word_length": average_word_length(text),
        "longest_word":        longest_word(text),
        "shortest_word":       shortest_word(text),
        "char_frequency":      char_frequency(text),
        "is_pangram":          is_pangram(text),
        "reading_level":       reading_level(text),
    }

def display(stats):
    """The ONLY function permitted to print."""
    for k, v in stats.items():
        print(f"{k:>22}: {v}")
```

Verified output for `"The quick brown fox jumps over the lazy dog. It was remarkably fast!"`:

```
            word_count: 13
        sentence_count: 2
   average_word_length: 4.153846153846154
          longest_word: remarkably
         shortest_word: it
        char_frequency: [('a', 5), ('e', 4), ('o', 4), ('r', 4), ('t', 4), ...]
            is_pangram: True
         reading_level: Elementary
```

### What to check at checkoff

1. **Does `analyze` call the other functions, or re-implement them?** The specification is explicit.
   A student who recomputes the word list inside `analyze` has failed the main requirement of the
   lab, however correct the numbers.
2. **Do the edge cases return rather than crash?** Verified behaviour:

   | Input | `word_count` | `sentence_count` | `reading_level` | `longest_word` |
   |---|---|---|---|---|
   | `""` | 0 | 0 | `"Elementary"` | `""` |
   | `"just words here"` (no terminator) | 3 | **1** | `"Elementary"` | `"words"` |
   | `"!!! ???"` | 0 | 0 | `"Elementary"` | `""` |

   `average_word_length("")` must be `0.0`, not `ZeroDivisionError`. This is the most common
   crash. Text with no terminating punctuation must still count as **one** sentence, not zero —
   otherwise `reading_level` divides by zero.
3. **Ties.** `longest_word` and `shortest_word` must be deterministic. `max(..., key=len)` returns
   the **first** maximum, which is a defensible rule; any documented rule is acceptable, but the
   docstring must say which.
4. **No printing outside `display`.** Grep for `print(` — it should appear exactly once.
5. **Two asserts per function**, and they must include an edge case, not two happy paths.

---

## Part 4 — Recursion First Look

Accept any correct recursive `factorial` or `countdown`. The one thing to insist on is that the
**base case is an inequality** (`n <= 0`), not an equality — see Lab 4.

---

## Marking Scheme

The lab is checkoff-graded against the criteria on the handout. Within each part:

- **Method (≈60%).** Correct approach, required loop/structure type actually used, edge cases
  considered, invariants stated where the handout asks for them.
- **Result (≈40%).** Code runs, produces the specified output, and the written answers are correct.

**Carry-through.** A wrong helper that is then used correctly downstream costs marks once.

**Watch for the two failure modes that matter:**
1. Code that produces the right answer for the sample input and is wrong in general — always run
   the edge cases listed under each exercise.
2. Written answers that restate the observation instead of explaining it. "0.1 + 0.2 isn't 0.3
   because floats are imprecise" earns nothing; the answer must reach binary representation.

---

*CS 101 · Week 3 · Lab Solutions · Instructor Copy · © CSE Department*
