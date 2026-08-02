# CS 101 — Lecture 28 (Week 9, Lecture 1)
## Strings as a Data Structure: Immutability, Encoding, and Cost

---

## 0. Why Strings Get Their Own Week

You have used strings since Week 0. So why return to them in Week 9, after hash tables?

Because until now you have used strings as *values* — things to print and compare. This week treats
them as a **data structure**, with a representation, a cost model, and failure modes. Three facts
drive everything:

1. Strings are **immutable**, so every "modification" allocates.
2. Strings are **sequences of code points**, not bytes — and the difference is where most
   internationalisation bugs live.
3. String operations have **complexities you must know**, because the natural way to build a string
   in a loop is quadratic.

Every one of these has bitten production systems. By the end of the week you will also have the
tool — regular expressions — that makes most text processing a two-line job, along with a clear
sense of when that tool is the wrong one.

---

## 1. Immutability and What It Costs

A Python string cannot be modified. There is no `s[0] = 'H'`:

```python
s = "hello"
s[0] = "H"      # TypeError: 'str' object does not support item assignment
```

Every operation that appears to modify a string in fact **builds a new one**:

```python
s = "abc"
before = id(s)
s += "d"
id(s) == before        # False — s now labels a different object
```

This is the same object model from L04: `+=` on an immutable type cannot mutate, so it computes a
new value and rebinds the name. For a list, `+=` mutates in place and every alias sees the change;
for a string, nothing else can see anything, because the original is untouched.

**Why make strings immutable at all?** Three payoffs:

- **Hashability.** A string can be a dict key precisely because its value can never change, so its
  hash stays valid (L25 §6). Lists are mutable and therefore unhashable.
- **Safe sharing.** A string can be passed anywhere without defensive copying — no caller can
  corrupt it.
- **Interning.** Because two equal strings are interchangeable, the interpreter may store just one
  copy of a repeated literal.

The cost is that building a string incrementally is expensive, which is §2.

---

## 2. The Concatenation Trap

Here is the most common performance bug in beginner Python:

```python
s = ""
for c in source:
    s += c          # looks O(1), is not
```

Each `+=` allocates a new string and copies everything accumulated so far. Over `n` characters that
is `1 + 2 + 3 + … + n = n(n+1)/2` character copies — **Θ(n²)**.

The fix is to collect the pieces and join once:

```python
parts = []
for c in source:
    parts.append(c)     # amortised O(1) each
s = "".join(parts)      # single O(n) pass
```

`str.join` computes the total length first, allocates once, and copies each piece exactly once —
**Θ(n)**.

### A measurement that is easy to get wrong

Time the naive loop directly and you may see only a 4–7× penalty, not a quadratic blow-up:

```
n =  2000: concat   0.225 ms   join 0.056 ms   ratio  4x
n =  8000: concat   0.772 ms   join 0.118 ms   ratio  7x
n = 32000: concat   2.653 ms   join 0.496 ms   ratio  5x
```

That looks linear. **It is a measurement artefact.** CPython contains an optimisation: when the
string being extended has a reference count of 1 — nobody else is looking at it — the interpreter
resizes it in place instead of copying. The naive loop happens to satisfy that condition exactly.

Keep any other reference alive and the optimisation switches off, revealing the real behaviour:

```python
s = ""
keep = []
for c in source:
    s += c
    keep.append(s)      # a live alias defeats the in-place resize
```

```
n =  2000:    1.129 ms
n =  8000:   20.126 ms     (4x the input -> 17.8x the time)
n = 32000:  313.717 ms     (4x the input -> 15.6x the time)
```

Quadrupling `n` multiplies the time by roughly 16 = 4² — textbook Θ(n²).

> **Two lessons, and the second is the more important one.** First: use `join`. Second: **a
> microbenchmark can hide the very behaviour you are trying to measure.** The optimisation here is
> real but fragile — it vanishes the moment the string is stored, returned, or aliased, which is
> exactly what happens in real code. Never rely on an accident of refcounting for your program's
> complexity class.

---

## 3. Strings Are Sequences of Code Points

`len(s)` does **not** return a number of bytes:

| String | `len(str)` | UTF-8 bytes | Encoded |
|---|---|---|---|
| `"hello"` | 5 | 5 | `68 65 6c 6c 6f` |
| `"café"` | 4 | **5** | `63 61 66 c3 a9` |
| `"日本語"` | 3 | **9** | `e6 97 a5 …` |
| `"👋🏽"` | **2** | **8** | `f0 9f 91 8b f0 9f 8f bd` |

A Python `str` is a sequence of **Unicode code points**. Encoding to `bytes` is a separate,
explicit step:

```python
"café".encode("utf-8")          # b'caf\xc3\xa9'  — 5 bytes
b'caf\xc3\xa9'.decode("utf-8")  # 'café'          — 4 code points
```

**UTF-8 is variable-width**: ASCII characters take 1 byte, most European accented letters 2, most
CJK characters 3, and emoji 4. That is why `len(str) != len(bytes)` for anything outside ASCII.

The waving-hand example is worth dwelling on. `"👋🏽"` has `len == 2` because it is *two* code
points — a base emoji plus a skin-tone modifier — that render as one glyph. **Code points are not
characters, and characters are not what users perceive as characters.** A "user-perceived
character" is called a *grapheme cluster*, and Python's standard library does not count them.

### Normalisation

Two strings can look identical and compare unequal:

```python
e1 = "é"        # U+00E9, one precomposed code point
e2 = "é"        # U+0065 U+0301, 'e' + combining acute accent
len(e1), len(e2)     # (1, 2)
e1 == e2             # False
```

The repair is **normalisation**:

```python
import unicodedata
unicodedata.normalize("NFC", e1) == unicodedata.normalize("NFC", e2)   # True
```

**Normalise before comparing or hashing any text that came from outside your program** — user
input, filenames, network data. Skipping it produces the maddening bug where a user swears they
typed the right password and the comparison disagrees.

---

## 4. `str` vs `bytes`

These are different types and Python refuses to mix them:

```python
"a" + b"b"      # TypeError: can only concatenate str (not "bytes") to str
```

That refusal is deliberate. In Python 2 the two were interchangeable, and the result was a
generation of programs that worked on ASCII and corrupted everything else. Python 3 forces you to
say which you mean:

- **`str`** — text. Human-meaningful characters. Use for anything you display, compare, or reason
  about linguistically.
- **`bytes`** — binary. What is actually stored or transmitted. Use for files opened in binary mode,
  network sockets, and cryptographic input.

**The rule: decode at the boundary, work in `str`, encode on the way out.** A program should have a
thin edge that converts and a large interior that never thinks about encoding at all. PROG 101
Week 5 meets the same boundary from the other side, where C gives you nothing but bytes and the
"text" interpretation is entirely yours to impose.

---

## 5. Slicing and the Cost of Every Operation

Slicing produces a **new string** — it copies:

```python
s = "Hello, World"
s[7:]        # 'World'
s[:5]        # 'Hello'
s[::-1]      # 'dlroW ,olleH'  — reversal
s[::2]       # 'Hlo ol'        — every other character
```

| Operation | Complexity | Note |
|---|---|---|
| `s[i]` | Θ(1) | Direct index into the code-point array |
| `len(s)` | Θ(1) | Stored, not counted |
| `s[i:j]` | Θ(j−i) | **Copies** — slicing is not free |
| `s + t` | Θ(len s + len t) | Allocates a new string |
| `"".join(parts)` | Θ(total length) | One allocation, one pass |
| `x in s` | Θ(n·m) worst | Substring search — see L29 |
| `s.replace(a, b)` | Θ(n) | Builds a new string |
| `s.split()` | Θ(n) | Allocates a list plus each piece |

The slicing row is the one people forget. Recursing with `s[1:]` copies the remainder at every
level — the same Θ(n²) trap as list slicing in L15 §6, and the reason index-based recursion exists.

---

## 6. The String Methods Worth Knowing Cold

```python
"a,b,,c".split(",")     # ['a', 'b', '', 'c']   — preserves empty fields
"a b  c".split()        # ['a', 'b', 'c']       — no argument: collapses ALL whitespace
```

**These two behave differently and the difference matters.** `split(sep)` splits on every
occurrence, so consecutive separators produce empty strings — which is what you want for CSV, where
`a,,b` genuinely has an empty middle field. Bare `split()` treats any run of whitespace as one
separator and discards leading/trailing whitespace — which is what you want for prose.

```python
s.find("z")     # -1     — returns a sentinel
s.index("z")    # raises ValueError
```

Use `find` when absence is normal and you will branch on it; use `index` when absence is a bug and
you want it to stop the program. Choosing `find` and then forgetting to check for `-1` produces a
silent off-by-one, because `-1` is a *valid index* in Python and will happily index from the end.

Also worth memorising: `strip`/`lstrip`/`rstrip`, `startswith`/`endswith` (which accept a **tuple**
of options), `lower`/`upper`, `replace`, `count`, and the alignment trio `ljust`/`rjust`/`center`.

> **`casefold`, not `lower`, for case-insensitive comparison.** `lower` handles ASCII; `casefold`
> handles cases like German ß → "ss" that `lower` leaves alone.

---

## 7. CS Connection — Why This Is Not Just Python Trivia

**Immutable strings are a language design choice with system-wide consequences.** Java, C#, and
Python all chose immutability and all provide a separate mutable builder (`StringBuilder`,
`list` + `join`) precisely because the quadratic trap is otherwise unavoidable. C chose mutable
character arrays and pays for it with buffer overflows — PROG 101 Week 2's entire lecture on
`strncpy` exists because C strings have no length and no bounds.

**The encoding boundary is where security bugs live.** Path traversal, SQL injection, and
homograph attacks on domain names all exploit the gap between "these two strings look the same" and
"these two strings *are* the same". Normalisation is not a nicety; it is a validation step.

**And the cost model transfers.** The concat trap is the string instance of a general rule you
already know from L22: **an O(n) operation inside a loop over n items is O(n²)**. You met it with
`list.insert(0, x)`, you meet it here with `+=`, and you will meet it again with file I/O next
week.

---

## 8. Summary

| Idea | Consequence |
|---|---|
| Strings are immutable | Every "edit" allocates; strings are hashable and safe to share |
| `+=` in a loop is Θ(n²) | Build a list, then `"".join(parts)` |
| CPython's in-place resize | Hides the quadratic behaviour in naive benchmarks — do not rely on it |
| `str` is code points, not bytes | `len(str) != len(bytes)` outside ASCII |
| Encoding is explicit | Decode at input, work in `str`, encode at output |
| Equal-looking ≠ equal | Normalise (NFC) before comparing external text |
| Slicing copies | `s[1:]` recursion is Θ(n²) |
| `split(sep)` vs `split()` | Empty fields preserved vs whitespace runs collapsed |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict each value, then check.

```python
len("café")
len("café".encode("utf-8"))
len("👋🏽")
"a,b,,c".split(",")
"a b  c".split()
"hello".find("z")
```

**2. (Explain.)** This benchmark suggests string `+=` is linear, but it is quadratic. Explain the discrepancy and describe how to measure it honestly.

```python
import timeit
timeit.timeit("s=''\nfor c in src: s+=c", setup="src='x'*32000", number=3)
# only ~5x slower than "".join(src)
```

**3. (Build.)** Write `normalise_and_count(words)` that counts word frequencies case-insensitively and correctly for accented text, returning a dict. Explain each of the two normalisation steps.

**4. (Stretch.)** `"é" == "é"` can be `False`. Explain how, give the two code-point sequences, and say what this implies for using user-supplied text as a dict key.

### Answers

**1.** `4`, `5`, `2`, `['a', 'b', '', 'c']`, `['a', 'b', 'c']`, `-1`.

`"café"` is 4 **code points** but 5 **UTF-8 bytes**, because `é` needs two. `"👋🏽"` is 2 code points
— a base emoji plus a skin-tone modifier — that render as a single glyph, so even `len` on the
`str` disagrees with what a user would call "one character".

`split(",")` preserves the empty field between the two commas; bare `split()` collapses whitespace
runs and discards the empties. `find` returns the sentinel `-1` rather than raising.

**2.** CPython optimises `s += c` into an **in-place resize** when `s` has a reference count of 1 —
nothing else refers to it, so extending the existing buffer is safe. The naive benchmark satisfies
that condition exactly, so it measures the optimised path and reports near-linear behaviour.

To measure honestly, defeat the optimisation by keeping a live alias:

```python
s = ""
keep = []
for c in src:
    s += c
    keep.append(s)
```

Measured: 1.13 ms, 20.1 ms, 313.7 ms at n = 2000, 8000, 32000. Quadrupling n multiplies the time by
~16 = 4², confirming **Θ(n²)**.

The deeper point is that the optimisation is **fragile** — storing, returning, or aliasing the
string switches it off, and all three happen constantly in real code. A program whose complexity
class depends on an accident of refcounting is a program that will surprise you.

**3.**

```python
import unicodedata
from collections import Counter

def normalise_and_count(words):
    """Count words case-insensitively and Unicode-correctly."""
    return Counter(
        unicodedata.normalize("NFC", w).casefold()
        for w in words
    )
```

**NFC normalisation** collapses the different code-point sequences that render identically — without
it, `"café"` typed with a combining accent and `"café"` typed precomposed count as two different
words. **`casefold`, not `lower`**, because `casefold` is designed for caseless matching and handles
cases `lower` misses, notably German `ß` → `"ss"`.

Order matters slightly: normalise first, then casefold, since casefolding can itself produce
sequences that benefit from re-normalisation in edge cases.

**4.** The two sequences are:

- `U+00E9` — a single precomposed code point, `len == 1`
- `U+0065 U+0301` — Latin `e` followed by a combining acute accent, `len == 2`

They render identically in every font, and `==` compares code point sequences, so they are
**unequal**. `unicodedata.normalize("NFC", ...)` converts both to the precomposed form and they
compare equal.

**The dict-key implication is serious.** Since `hash` follows `==`, the two spellings hash
differently and land in different buckets. A user who registers with one form and logs in with the
other — trivially possible, since different operating systems and input methods produce different
forms — is not found. The fix is to **normalise at the boundary**, before the text is ever used as
a key, compared, or stored. This is the same "validate at the edge" discipline as L27's advice to
push impurity outward, applied to encoding.

---

## Reading

- **Guttag, Ch. 4** — strings and string methods (primary)
- **Python docs — Unicode HOWTO** — the authoritative treatment of §3 and §4 (strongly recommended)
- **Joel Spolsky, "The Absolute Minimum Every Software Developer Must Know About Unicode"** — the
  classic essay; dated in places but still the best motivation for why §3 matters

---

*CS 101 · Week 9 · Lecture 28 (Wed) · © CSE Department*
