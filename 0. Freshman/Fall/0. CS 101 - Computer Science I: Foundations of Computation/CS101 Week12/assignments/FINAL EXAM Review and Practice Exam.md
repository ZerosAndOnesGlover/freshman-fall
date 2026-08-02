# CS 101: Final Exam
## Review Guide and Practice Exam

**Exam:** Week 12, during the scheduled examination period
**Duration:** 3 hours · **Format:** Written, closed book. One double-sided A4 sheet of handwritten notes permitted.
**Covers:** Weeks 1–11 — the entire course
**Weight:** 25% of final grade

---

## Part I: Review Guide

### How the Exam Is Weighted

| Area                                        | Weeks | ~Share | Notes                                  |
| ------------------------------------------- | ----- | ------ | -------------------------------------- |
| Foundations: types, control flow, functions | 1–3   | 15%    | Assumed throughout; rarely asked alone |
| Recursion                                   | 4     | 10%    | Base cases, call stack, recomputation  |
| Searching and sorting                       | 5     | 15%    | Including which to choose and why      |
| Complexity analysis                         | 6     | 20%    | The single heaviest topic              |
| Data structures                             | 7–8   | 20%    | Lists/stacks/queues; hash tables       |
| Strings and regex                           | 9     | 10%    | Encoding boundary; greedy vs lazy      |
| Files and exceptions                        | 10    | 10%    | Modes, atomicity, clause ordering      |
| Computability                               | 11    | 10%    | Definitions and one reduction          |

*(Shares are approximate and overlap — a single question often spans Weeks 6, 7, and 8 at once.)*

### The Nine Things Most Likely to Cost You Marks

These are the errors that recur every year.

1. **Confusing "always halts" with "answers correctly"** — a decider must do both. This is the whole
   decidable/recognisable distinction.
2. **Reducing in the wrong direction** — you must build a HALT-solver *from* the new problem's
   solver, never the reverse.
3. **Quoting Big-O without stating the case** — "quicksort is O(n log n)" is incomplete; average, not
   worst.
4. **Saying "O(1) lookup" without conditions** — average case, good hash, bounded load factor.
5. **Forgetting that `open(path, "w")` truncates at open**, before any write.
6. **Ordering `except` clauses general-before-specific** — the specific clause becomes unreachable.
7. **Conflating code points, bytes, and grapheme clusters.**
8. **Claiming a regex can match nested structure.** It cannot, and Week 11 tells you it is a theorem.
9. **Giving a complexity without saying what n counts.** "O(n)" in a nested-collection problem is
   meaningless until you say whether n is rows, cells, or characters.

### Facts Worth Memorising

| | |
|---|---|
| Selection sort comparisons | exactly n(n−1)/2, on **every** input |
| Bubble/insertion swaps | exactly the number of **inversions** |
| Bubble/insertion best case | Θ(n) on sorted input |
| Merge sort | Θ(n log n) always; Θ(n) extra space; stable |
| Quicksort | Θ(n log n) average, **Θ(n²) worst**, in-place, not stable |
| Binary search | ⌊log₂ n⌋ + 1 comparisons worst case (7 at n=100, 20 at n=10⁶) |
| Naive fib(n) calls | 2·fib(n+1) − 1 — that is 21,891 calls for n = 20 |
| `list.insert(0, x)` | Θ(n) |
| dict/set lookup | Θ(1) average, Θ(n) worst |
| dict insert | Θ(1) **amortised** — resize is Θ(n) and geometrically rare |
| `s += c` in a loop | Θ(n²) total copies: n(n+1)/2 |
| HALT | undecidable, but **recognisable** |

---

## Part II: Practice Exam

**Attempt this under exam conditions before looking at the answers.** Three hours, no notes beyond
one sheet. The real exam is the same shape and length.

**Total: 100 points**

---

### Section A: Short Answer (30 points, 2 points each)

**A1.** State whether `0.1 + 0.2 == 0.3` evaluates to `True` or `False`, and explain in one sentence.

**A2.** `len("café")` is 4 but `len("café".encode("utf-8"))` is 5. Explain. State `len("👋🏽")`.

**A3.** What does this print, and why?

```python
def add(x, acc=[]):
    acc.append(x)
    return acc
print(add(1), add(2), add(3))
```

**A4.** State the worst-case number of comparisons binary search performs on a sorted array of
1,000,000 elements.

**A5.** Give the exact number of comparisons selection sort performs on a reversed array of 32
elements, and state how that number changes if the array is already sorted.

**A6.** Naive recursive `fib(20)` makes how many calls? Give the formula.

**A7.** Why is dict insertion described as O(1) *amortised* rather than O(1)?

**A8.** A hash table with 16 buckets holds 6 keys, all in one bucket. State the load factor and
explain why it does not describe the problem.

**A9.** State what `re.findall(r"<.+>", "<a><b>")` returns and give the one-character fix to get both
tags.

**A10.** Which of `re.match`, `re.search`, `re.fullmatch` must be used to *validate* a field, and
why?

**A11.** A file contains `EXISTING`. State its contents after `open(path, "w")` followed immediately
by `close()`.

**A12.** Name two of the four requirements for a crash-safe atomic write, with the failure each
prevents.

**A13.** Give one exception class caught by `except BaseException:` but not `except Exception:`, and
say why the distinction matters.

**A14.** Define **decidable** and **recognisable**, making the difference explicit.

**A15.** State Rice's theorem, defining both of its qualifying adjectives.

---

### Section B: Analysis (25 points)

**B1 (8 points).** For each, give the tightest complexity in terms of n = `len(data)`, and state what
dominates.

```python
def a(data):                      # (a)
    out = []
    for x in data:
        if x not in out:
            out.append(x)
    return out

def b(data):                      # (b)
    seen = set()
    return [x for x in data if not (x in seen or seen.add(x))]

def c(data):                      # (c)
    s = ""
    for x in data:
        s += str(x)
    return s

def d(data):                      # (d)
    return sorted(set(data))
```

**B2 (7 points).** A student benchmarks (c) above and finds it takes only ~5× longer than
`"".join(...)` rather than the predicted quadratic blow-up. Explain what CPython is doing, and state
the condition under which the optimisation applies.

**B3 (10 points).** You must repeatedly answer "how many records have score > k?" for varying k, over
a fixed dataset of n records.

(a) Give the complexity of the naive approach. *(2)*
(b) Propose a preprocessing step and state its one-off cost. *(3)*
(c) State the per-query cost after preprocessing. *(3)*
(d) State the break-even number of queries at which preprocessing pays for itself, in terms of n. *(2)*

---

### Section C — Implementation (20 points)

**C1 (10 points).** Write a function `top_k(counts, k)` that returns the k highest-valued items from
a dict of `{item: count}`, as a list of `(item, count)` sorted descending by count.

State the complexity of your solution, and state a different complexity you could achieve with a
different structure and when it would be worth it.

**C2 (10 points).** Write `safe_load(path)` that reads a JSON file and returns a dict, meeting all of:

- missing file → return `{}`
- empty file → return `{}`
- malformed JSON → raise a `ConfigError` naming the file
- JSON that parses but is not a dict → raise a `ConfigError` naming the file
- the encoding is specified explicitly

Define `ConfigError`. Do not use `os.path.exists`.

---

### Section D: Computability (25 points)

**D1 (5 points).** Give the formal 7-tuple definition of a Turing machine and say what δ does.

**D2 (8 points).** Prove that HALT is undecidable. Give the construction and argue **both** cases.

**D3 (7 points).** Prove that **PRINTS-42** = { ⟨M, w⟩ : M ever prints `42` when run on w } is
undecidable, by reduction from HALT. State the assumption, give the construction, argue both
directions, conclude.

**D4 (5 points).** Your manager asks for a tool that flags every submitted program that will infinite
loop, with no false positives. Explain why it cannot be built, and propose something that can — naming
which of sound/complete/total you gave up.

---

## Part III: Answer Key

> **Instructor copy.** Distribute after the practice attempt, not before.

### Section A

**A1.** **`False`.** `0.1` and `0.2` have no exact binary representation, so the sum is
`0.30000000000000004`, not `0.3`. *(Verified.)*

**A2.** A `str` is a sequence of **Unicode code points**; UTF-8 is **variable-width** and `é` needs
two bytes. `len("👋🏽")` is **2** — a base emoji (U+1F44B) plus a skin-tone modifier (U+1F3FD), two
code points rendering as one grapheme.

**A3.** Prints `[1, 2, 3] [1, 2, 3] [1, 2, 3]`. The default `[]` is evaluated **once, at function
definition**, so all three calls append to the same list. (Also: Python evaluates all three arguments
before printing, so even the first shows the final state.)

**A4.** ⌊log₂ 1000000⌋ + 1 = **20**.

**A5.** **496** comparisons — n(n−1)/2 = 32·31/2. It **does not change**: selection sort's comparison
count is completely input-independent, because it scans the whole unsorted remainder every pass
regardless of what it finds. *(Verified on random, sorted, and reversed inputs.)*

**A6.** **21,891** calls. The formula is **2·fib(n+1) − 1**; fib(21) = 10,946, so 2·10946 − 1 = 21,891.
*(Verified by instrumented count.)*

**A7.** Because **resizing (rehashing)** occurs occasionally and costs **Θ(n)** for that one
insertion. Because the table doubles, resizes are geometrically rare, so n insertions total O(n) and
the per-operation average is O(1). It is a worst-case guarantee over a *sequence*, not a
probabilistic average.

**A8.** Load factor = **6/16 = 0.375**. It does not describe the problem because load factor measures
**occupancy, not uniformity** — 15 buckets are empty while one holds a 6-long chain, so lookups
degrade to Θ(n) despite a healthy-looking ratio.

**A9.** Returns **`['<a><b>']`** — one match. `.+` is **greedy**: it consumes to the end, then
backtracks only to the **last** `>`. Fix: **`<.+?>`** — the `?` makes it lazy, giving
`['<a>', '<b>']`. *(Verified.)*

**A10.** **`fullmatch`**, because validation means the *entire* string must conform. `search` would
accept any string merely *containing* a match — `search(r"\d{4}", "12345")` matches `1234`, wrongly
accepting `"12345"` as a 4-digit PIN. *(Verified.)*

**A11.** **Empty.** `"w"` truncates the file **at open**, before any write occurs. *(Verified.)*

**A12.** Any two:

| Requirement | Prevents |
|---|---|
| Temp file in the **same directory** | `os.replace` is only atomic within a filesystem |
| **`fsync`** before rename | Power loss leaving an empty or partial file |
| **`os.replace`** not `os.rename` | Failure on Windows when the destination exists |
| Cleanup under **`except BaseException`** | Ctrl-C leaving an orphaned temp file |

**A13.** **`KeyboardInterrupt`** (also `SystemExit`, `GeneratorExit`). These sit outside `Exception`
deliberately so ordinary error handling does not swallow them — catching `Exception` must not make
your program un-interruptible. *(Verified: `issubclass(KeyboardInterrupt, Exception)` is `False`.)*

**A14.** **Decidable** — a TM exists that, on **every** input, **halts** and answers correctly.
**Recognisable** — a TM exists that accepts every string in L, but on strings not in L may reject *or
run forever*. The difference is the **halting guarantee on no-instances**.

**A15.** Every **non-trivial**, **semantic** property of programs is undecidable. *Semantic* = about
the program's input/output behaviour, not its text. *Non-trivial* = true of some programs and false of
others.

---

### Section B

**B1** *(2 points each)*

| | Complexity | What dominates |
|---|---|---|
| **(a)** | **Θ(n²)** | `x not in out` is a linear scan of a list, performed n times |
| **(b)** | **Θ(n)** average | Set membership and insertion are Θ(1) average |
| **(c)** | **Θ(n²)** | String immutability: each `+=` copies the whole accumulated string; n(n+1)/2 copies total |
| **(d)** | **Θ(n log n)** | `set()` is Θ(n), `sorted` is Θ(n log n) and dominates |

*Marking:* (b) must say **average** — adversarial hash collisions make it Θ(n²). Deduct 1 otherwise.

**B2** *(7 points)* CPython **resizes the string in place** when its reference count is **1** — that
is, when nothing else refers to it, so growing it cannot be observed by any other name. The naive
loop happens to satisfy this, since `s` is the only reference.

**The condition is the refcount.** Bind the intermediate result elsewhere (`prev = s`) and the
optimisation disappears, restoring the quadratic behaviour.

*Two further marks for either:* it is a CPython implementation detail, not a language guarantee (PyPy
and others differ); or, the asymptotic claim is still correct — this changes the constant, not the
growth class.

*Do not accept* "the interpreter caches strings" or "string interning."

**B3** *(10 points)*

**(a)** *(2)* **Θ(n) per query** — scan all records and count.

**(b)** *(3)* **Sort the scores once**, at a one-off cost of **Θ(n log n)**. *(Accept: build a sorted
array of scores, or a prefix-count structure over a bounded score range at Θ(n).)*

**(c)** *(3)* **Θ(log n) per query** — binary search for the first score > k; the answer is the
number of elements from there to the end, available by index arithmetic in Θ(1).

**(d)** *(2)* Preprocessing pays off when `n log n + q log n < q · n`, i.e. roughly when
**q > log n**. For n = 10⁶ that is about 20 queries — so preprocessing wins almost immediately.

*Marking:* full marks for (d) require the comparison of totals, not just "when q is large."

---

### Section C

**C1** *(10 points)*

```python
def top_k(counts, k):
    """Return the k highest-valued items as (item, count), descending."""
    return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:k]
```

**Complexity: Θ(m log m)** where m is the number of distinct items — the sort dominates.

**The alternative:** a **min-heap of size k** (`heapq.nlargest`) gives **Θ(m log k)**. Since k is
typically a small constant while m may be enormous, this is effectively Θ(m).

**When it is worth it:** when **k ≪ m**. At m = 500,000 distinct words and k = 10, the heap avoids
sorting half a million items to read ten. At m = 50 it is not worth the added complexity — the sort
is clearer and the difference unmeasurable.

*Marking:* 5 for a correct function, 2 for the correct complexity **with m defined**, 3 for the
alternative **plus the condition**. An answer that names the heap without saying when it wins gets 1
of those 3 — the judgement is the point.

**C2** *(10 points)*

```python
import json
from pathlib import Path


class ConfigError(Exception):
    """Raised when a config file exists but cannot be used."""


def safe_load(path):
    try:
        text = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}

    if not text.strip():
        return {}

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ConfigError(f"{path}: malformed JSON ({exc})") from exc

    if not isinstance(data, dict):
        raise ConfigError(f"{path}: expected an object, got {type(data).__name__}")

    return data
```

*Marking, 2 points each:* missing file returns `{}` via **EAFP** (no `os.path.exists` — that would be
TOCTOU); empty file handled *before* parsing; `JSONDecodeError` converted to `ConfigError`; the
`isinstance` shape check (a bare `json.loads("42")` succeeds and returns an int); `encoding="utf-8"`
stated explicitly.

*Award a bonus mark* for `raise ... from exc`, which preserves the original traceback.

*Common failure:* handling the missing file with a pre-check. It is both TOCTOU-prone and explicitly
forbidden by the question.

---

### Section D

**D1** *(5 points)* **(Q, Σ, Γ, δ, q₀, q_accept, q_reject)** — states; input alphabet; tape alphabet
(⊇ Σ, includes the blank); transition function; start state; two halting states.

**δ: Q × Γ → Q × Γ × {L, R}** — given the current state and the symbol under the head, it specifies
the next state, the symbol to write, and which way to move. **δ is the machine**; everything else is
bookkeeping. *(2 of the 5 marks are for δ.)*

**D2** *(8 points)* Assume `halts(f, x)` exists, always halting and always correct. Define:

```python
def paradox(f):
    if halts(f, f):
        while True: pass
    else:
        return
```

Run `paradox(paradox)`:

- **If it halts** — then `halts(paradox, paradox)` returned `True`, so the `while True` branch was
  taken and it **does not halt**. Contradiction.
- **If it does not halt** — then `halts(paradox, paradox)` returned `False`, so `return` executed and
  it **halts**. Contradiction.

The cases are exhaustive; the only assumption was `halts`. Therefore `halts` does not exist. ∎

*Marking:* 3 construction, 2 per case, 1 conclusion. **Both cases are required** — one case alone
caps at 4/8.

**D3** *(7 points)* Assume `prints_42(f, x)` decides PRINTS-42. Construct:

```python
def halts(f, x):
    def wrapper(_):
        f(x)              # if this never returns, we never reach the print
        print("42")       # reached ONLY if f(x) halted
    return prints_42(wrapper, None)
```

- **If f(x) halts** — control reaches the print, `wrapper` prints `42`, `prints_42` returns `True`,
  `halts` returns `True`. ✅
- **If f(x) loops forever** — the print is never reached, `wrapper` never prints `42`, `prints_42`
  returns `False`, `halts` returns `False`. ✅

`halts` would then be correct on every input, contradicting D2. Therefore `prints_42` does not
exist. ∎

*Marking:* 1 assumption, 3 construction, 2 for **both** directions, 1 conclusion. A reduction in the
**wrong direction** (using `halts` to decide PRINTS-42) earns **at most 1** — it proves nothing.

**D4** *(5 points)* The request is for a decider that is **total** (answers on every submission),
**sound** (never flags a terminating program) and **complete** (flags every looping one). That is
exactly a decider for the complement of HALT, which D2 rules out. It is not a hard problem; it is a
nonexistent one. *(3 marks.)*

**Buildable alternative** *(2 marks — any one, with the dropped property named):*

- **A timeout** — run each submission for N seconds and flag whatever is still running. Total and
  complete; **drops soundness** (slow-but-correct programs get flagged).
- **A conservative static analyser** — prove termination where structure allows, and answer
  `loops` / `terminates` / **`don't know`**. Sound and complete on what it answers; **drops totality**.

*Full marks require naming which property was sacrificed.* "Use a timeout" alone is worth 1.

---

## Final Advice

**Show your reasoning.** Most of these questions award more for the argument than the answer. A
correct complexity with no justification earns partial credit; a wrong complexity with sound
reasoning often earns more.

**Say which case you mean.** Best, average, worst — for every complexity claim, every time.

**In Section D, argue both directions.** It is the single most common way marks are lost on the
final, and it is entirely avoidable.

Good luck.

---

*CS 101 · Week 12 · Final Exam Review · © CSE Department*
