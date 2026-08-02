# CS 101 — Week 9 Reading Guide & Resources
## Strings, Text Processing, and Regular Expressions

---

## Required Reading

### Guttag — *Introduction to Computation and Programming Using Python*
- **Ch. 4** — strings and string methods. Review rather than new material; skim for anything you
  have not used.

### Python Documentation (primary source this week)
- **Unicode HOWTO** — the authoritative treatment of §3–§4 of Lecture 28. Read it fully; it is
  short and it is the reference you will return to for years.
- **Regular Expression HOWTO** — the best regex introduction available anywhere. Read completely
  before Friday's lecture if you can.
- **`re` module reference** — for the full syntax table.
- **`csv` module** — read the introduction and the dialect discussion.

### Optional but recommended
- **Joel Spolsky, "The Absolute Minimum Every Software Developer Must Know About Unicode"** —
  dated in places, still the best motivation for why encoding matters.
- **CLRS Ch. 32.1** — the naive string-matching algorithm and its analysis. §32.4 covers KMP for
  the ambitious.
- **Friedl, *Mastering Regular Expressions*, Ch. 4–6** — the definitive treatment of backtracking.

---

## Focused REPL / Experimentation Sessions

### Session A: Feeling the encoding boundary (15 min)

```python
for s in ("hello", "café", "日本語", "👋🏽"):
    b = s.encode("utf-8")
    print(f"{s!r:10} len(str)={len(s)}  len(bytes)={len(b)}  {b.hex(' ')}")

# Why does the emoji have len 2?
list("👋🏽")            # two code points: base + skin-tone modifier

# Two strings that look identical:
e1, e2 = "é", "é"       # precomposed vs e + combining accent
len(e1), len(e2), e1 == e2

import unicodedata
unicodedata.normalize("NFC", e1) == unicodedata.normalize("NFC", e2)
```

**Question to answer for yourself:** if a user types their name into a form on macOS and later logs
in from Windows, could `username in users` fail even though they typed the same thing? What would
prevent it?

### Session B: Catching the concatenation trap (15 min)

```python
import timeit
# The misleading version:
timeit.timeit("s=''\nfor c in src: s+=c", setup="src='x'*32000", number=3)

# The honest version — a live alias defeats CPython's in-place resize:
timeit.timeit("""
s=''
keep=[]
for c in src:
    s += c
    keep.append(s)
""", setup="src='x'*32000", number=1)
```

Run both at n = 2000, 8000, 32000. **The second should quadruple-and-then-some as n quadruples.**
If it does not, your alias is not keeping the string alive.

### Session C: Regex reflexes (20 min)

Predict each before running. Note every one you get wrong.

```python
import re
re.findall(r"<.+>",  "<a><b>")           # greedy
re.findall(r"<.+?>", "<a><b>")           # lazy
re.match(r"world",  "hello world")
re.search(r"world", "hello world")
re.fullmatch(r"\w+", "hello world")
re.split(r"[,;]\s*", "a, b; c")
re.sub(r"\s+", " ", "a   b \t c")
re.findall(r"\b(\w+) \1\b", "the the quick fox fox")

# Named groups — much more readable past two captures:
re.search(r"(?P<user>\w+)@(?P<host>[\w.]+)", "x bob@ex.com").groupdict()
```

Then break something on purpose:

```python
re.sub(r"<.*?>", "", '<a href="a>b">link</a>')     # why is this wrong?
```

### Session D: The three limits of regex (15 min)

Regex fails in three *independent* ways. Reproduce each:

```python
import re, time

# 1. PERFORMANCE — exponential backtracking
bad = re.compile(r"^(a+)+$")
t0 = time.perf_counter(); bad.search("a"*24 + "!")
print("ReDoS:", (time.perf_counter()-t0)*1000, "ms")

# 2. LANGUAGE CLASS — cannot count nesting
re.sub(r"<.*?>", "", '<a href="a>b">link</a>')     # 'b">link'  — wrong

# 3. SEMANTIC CONTEXT — the characters don't carry the answer
re.split(r"(?<=[.!?])\s+", "Dr. Smith went home. He slept.")
# ['Dr.', 'Smith went home.', 'He slept.']         — three, should be two
```

**Be able to state which fix applies to which.** Rewriting the pattern fixes (1). Using a parser
fixes (2). Nothing in the regex family fixes (3) — it needs a model of the language.

---

---

## Quick Reference Card

### String cost model

| Operation | Complexity |
|---|---|
| `s[i]`, `len(s)` | Θ(1) |
| `s[i:j]` | Θ(j−i) — **copies** |
| `s + t` | Θ(len s + len t) |
| `"".join(parts)` | Θ(total) — **use this** |
| `s += c` in a loop | **Θ(n²)** |
| `x in s` | Θ(n+m) via `str.find` |

### Regex functions

| Function | Anchoring | Returns |
|---|---|---|
| `re.match` | start | Match / None |
| `re.search` | anywhere | Match / None |
| `re.fullmatch` | entire string | Match / None ← **use for validation** |
| `re.findall` | all matches | list |
| `re.sub` | all matches | new string |
| `re.split` | on matches | list |

### Regex syntax survival kit

```
.  \d \w \s      any / digit / word / whitespace
[abc]  [^abc]    one of / not one of
*  +  ?          0+, 1+, 0-or-1        (add ? for LAZY)
{n}  {n,m}       exact / range
^  $  \b         start / end / word boundary
|                alternation
( )  (?: )       capture / group-without-capture
(?P<name> )      named capture
\1               backreference
re.VERBOSE       whitespace + comments allowed in the pattern
```

**Always use raw strings:** `r"\d+"`, never `"\d+"`.

---

## Self-Test

Without notes:

1. Why is `s += c` in a loop quadratic, and why might a benchmark hide that?
2. What is `len("👋🏽")`, and why?
3. Give two code-point sequences that render as `é`. What repairs the comparison?
4. State the difference between `re.match`, `re.search`, and `re.fullmatch`. Which validates?
5. `re.findall(r"<.+>", "<a><b>")` returns one match. Why, and what is the fix?
6. What is the worst-case complexity of naive substring search, and what input triggers it?
7. Why does `"a,b".split(",")` differ from `"a b".split()` in how it treats repeats?
8. Give an input for which `line.split(",")` parses a CSV line incorrectly.
9. What makes `^(a+)+$` exponential and `^a+$` linear?
10. State the language-class reason regex cannot parse HTML.

*(Answers: 1. each `+=` copies everything so far, n(n+1)/2 copies; CPython resizes in place when
refcount is 1, which the naive loop satisfies. 2. **2** — a base emoji plus a skin-tone modifier.
3. `U+00E9` and `U+0065 U+0301`; `unicodedata.normalize("NFC", ...)`. 4. anchored at start /
anywhere / entire string; **fullmatch** validates. 5. `.+` is greedy and backtracks to the last `>`;
add `?` for `<.+?>`. 6. Θ(n·m), triggered by a needle that almost matches everywhere, e.g. `"aaa…ab"`
in `"aaaa…a"`. 7. `split(sep)` preserves empty fields between consecutive separators; bare `split()`
treats any whitespace run as one separator. 8. `'name,"Smith, John",42'` — the quoted comma. 9. the
nested quantifier makes the parse ambiguous, so failure requires trying exponentially many
partitions; `^a+$` admits one parse. 10. regex describes **regular** languages, HTML is
**context-free**; regular languages cannot count unbounded nesting.)*

---

## Looking Ahead

**📌 Project 1 is due this Friday.** Submit before starting PS9.

**Week 10** turns to files, I/O, and error handling — where the accumulator pattern from this week
reappears (the mistake becomes opening a file inside the loop), and where the encoding boundary of
Lecture 28 §4 becomes a decision you make on every `open()` call. **Midterm 2** is also in Week 10,
covering Weeks 6–9.

---

*CS 101 · Week 9 · © CSE Department*
