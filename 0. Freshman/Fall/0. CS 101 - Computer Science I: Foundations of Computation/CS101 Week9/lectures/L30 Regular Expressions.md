# CS 101 · Lecture 30 (Week 9, Lecture 3)
## Regular Expressions: A Language for Patterns

*“I define UNIX as 30 definitions of regular expressions living under one roof.”* — Donald Knuth, *Digital Typography* (1999), ch. 33

**Date:** Friday 27 November 2026 · 09:00–09:50 · Week 9

**Reading:** Python docs — Regular Expression HOWTO · Python docs — `re` module reference · Friedl, *Mastering Regular Expressions*, Ch. 4–6 *(details at the end of the lecture)*

**Coursework:** 📋 **Project 1** due today 17:00 · 📝 **PS 8** due today 17:00 · 📝 **PS 9** released today 10:00, due Fri 4 Dec 17:00 · 📘 **Midterm 2** Mon 30 Nov 18:00–19:15 · 🔬 **Lab 9** Tue 1 Dec 15:00–16:50 · 📊 **Quiz 10** Wed 2 Dec 09:00–09:10

---

## 0. Why a Second Language Inside Python

Yesterday's tools handle *fixed* patterns: `"error" in line`, `line.split(",")`. But most real text
questions are about **shapes**, not literals:

- Does this line start with a date?
- Extract every email address.
- Split on commas *or* semicolons, with optional spaces.
- Is this string a valid identifier?

Writing each as hand-rolled character loops is tedious and error-prone. A **regular expression** is
a tiny declarative language for describing such shapes, and Python's `re` module compiles them into
a matching engine.

Regex is genuinely powerful and genuinely dangerous — it has a class of performance failure that
can take down a server, and a well-known boundary beyond which it is simply the wrong tool. Both
are in this lecture.

---

## 1. The Core Language

| Pattern | Meaning | Example match |
|---|---|---|
| `.` | any character except newline | `a.c` → `abc`, `a7c` |
| `\d` `\w` `\s` | digit, word char, whitespace | `\d\d` → `42` |
| `\D` `\W` `\S` | the negations | |
| `[aeiou]` | any one listed character | |
| `[^0-9]` | any one character **not** listed | |
| `*` `+` `?` | 0+, 1+, 0-or-1 repetitions | `ab+` → `ab`, `abbb` |
| `{n}` `{n,m}` | exactly n / between n and m | `\d{4}` → `2026` |
| `^` `$` | start / end of string | `^\w+` |
| `\b` | word boundary | `\bcat\b` |
| `|` | alternation (or) | `cat|dog` |
| `( )` | group and capture | |
| `(?: )` | group without capturing | |

Verified behaviour:

```python
re.findall(r"\d+", "abc 123 def 45")        # ['123', '45']
re.findall(r"[aeiou]", "sequoia")           # ['e', 'u', 'o', 'i', 'a']
re.findall(r"cat|dog", "a cat and a dog")   # ['cat', 'dog']
re.findall(r"^\w+", "one two")              # ['one']
re.findall(r"\w+$", "one two")              # ['two']
```

### Raw strings are not optional

**Always write regex patterns as `r"..."`.** Regex uses backslashes heavily, and so does Python's
string literal syntax. Without the `r`, `"\d"` is Python trying to interpret `\d` as an escape
sequence, and `"\b"` becomes an actual backspace character rather than a word boundary.

This is not a stylistic preference — it is a source of bugs that produce *silently wrong matches*
rather than errors. (I hit exactly this while preparing these notes: writing `r'\\s+'` instead of
`r'\s+'` produced a pattern matching a literal backslash followed by `s`, and `re.sub` cheerfully
did nothing.)

---

## 2. The Four Functions You Need

```python
re.search(pattern, text)     # first match ANYWHERE -> Match or None
re.match(pattern, text)      # match anchored at the START -> Match or None
re.fullmatch(pattern, text)  # must match the ENTIRE string -> Match or None
re.findall(pattern, text)    # every match -> list of strings (or tuples if groups)
```

The distinction is the most common source of confusion:

```python
re.match(r"world", "hello world")       # None     — not at the start
re.search(r"world", "hello world")      # <Match span=(6, 11)>
re.fullmatch(r"\w+", "hello")           # <Match span=(0, 5)>
re.fullmatch(r"\w+", "hello world")     # None     — space is not \w
```

> **For validation, use `fullmatch`.** Using `search` to validate is a classic security bug: 
> `re.search(r"\d{4}", user_input)` accepts `"drop table; 1234"` because it only asks whether a
> four-digit run appears *somewhere*.

Two more that do the heavy lifting:

```python
re.sub(r"\s+", " ", "a   b \t c")       # 'a b c'    — collapse whitespace
re.split(r"[,;]\s*", "a, b; c")         # ['a', 'b', 'c']  — split on either delimiter
```

`re.split` is the answer to "split on commas *or* semicolons, with optional following spaces" — a
question `str.split` cannot express at all.

---

## 3. Groups: Extracting, Not Just Matching

Parentheses **capture** the matched text for retrieval:

```python
m = re.search(r"(\w+)@(\w+)\.com", "mail bob@example.com now")
m.group(0)    # 'bob@example.com'   — the whole match
m.group(1)    # 'bob'
m.group(2)    # 'example'
m.span()      # (5, 20)
```

Group 0 is always the entire match; groups 1, 2, … are the parenthesised parts, numbered by opening
parenthesis.

**Named groups** are far more maintainable once you have more than two:

```python
m = re.search(r"(?P<user>\w+)@(?P<host>[\w.]+)", "x bob@ex.com")
m.groupdict()      # {'user': 'bob', 'host': 'ex.com'}
```

A full worked example — parsing a log line:

```python
log = "2026-07-26 11:02:33 ERROR disk full"
m = re.match(r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\s+(\w+)\s+(.*)", log)
m.groups()
# ('2026', '07', '26', '11', '02', '33', 'ERROR', 'disk full')
```

Eight fields in one line. The equivalent hand-written parser is thirty lines and will get the
variable-width message field wrong.

**Backreferences** let a pattern refer to what it already matched — `\1` means "the same text group
1 matched":

```python
re.findall(r"\b(\w+) \1\b", "the the quick brown fox fox")
# ['the', 'fox']        — finds accidentally doubled words
```

---

## 4. Greedy vs Lazy — The Quantifier Trap

By default quantifiers are **greedy**: they match as much as possible.

```python
re.findall(r"<.+>", "<a><b>")     # ['<a><b>']   — ONE match spanning everything
re.findall(r"<.+?>", "<a><b>")    # ['<a>', '<b>']  — two matches
```

`.+` consumes to the end of the string, then backtracks just far enough to find a `>`. Since the
*last* `>` works, greedy matching swallows both tags. Adding `?` makes the quantifier **lazy** —
match as few characters as possible while still allowing the overall match.

```python
re.findall(r"a+", "aaa")     # ['aaa']            — greedy
re.findall(r"a+?", "aaa")    # ['a', 'a', 'a']    — lazy
```

**Whenever a pattern matches "too much", suspect greediness first.** It is the single most common
regex bug, and the fix is usually one `?`.

---

## 5. Catastrophic Backtracking — How a Regex Becomes an Outage

Some patterns take **exponential** time on inputs that fail to match. Consider `^(a+)+$` — a
repeated group whose contents are themselves repeatable — tested against a string of `a`s followed
by one `!`:

| Input | Time |
|---|---|
| 18 a's + `!` | 15.9 ms |
| 20 a's + `!` | 60.7 ms |
| 22 a's + `!` | 246.8 ms |
| 24 a's + `!` | **983.5 ms** |

Every two extra characters roughly **quadruples** the time — that is 2ⁿ. Extrapolate: 40 characters
would take over a year.

Meanwhile the equivalent-but-unambiguous pattern is instant:

```
^a+$ on 100,000 a's + '!'  ->  1.2 ms
```

**The cause is ambiguity.** For `^(a+)+$`, the string `"aaaa"` can be divided among the groups in
exponentially many ways — `(aaaa)`, `(aaa)(a)`, `(aa)(aa)`, `(a)(a)(a)(a)`, and so on. When the
final `$` fails because of the `!`, the engine dutifully backtracks and tries **every one** of those
divisions before concluding failure. `^a+$` admits exactly one way to match, so there is nothing to
backtrack through.

This is **ReDoS** — regular expression denial of service. An attacker who can supply input to a
vulnerable pattern can consume a CPU core indefinitely with a short string. It has caused real
outages, including a well-known Cloudflare incident in 2019.

**How to avoid it:**

- Be suspicious of **nested quantifiers** — `(a+)+`, `(a*)*`, `(a|aa)+`. These are the signature.
- Prefer specific character classes to `.` — `[^"]*` instead of `.*` inside a quoted region.
- Anchor patterns so failure is detected early.
- Never run a user-supplied regex against a large input.

Python's `re` uses a backtracking engine, so it is vulnerable. The `regex` package (third-party) and
Go's RE2 use automaton-based engines with guaranteed linear time — at the cost of dropping
backreferences, which cannot be expressed without backtracking.

---

## 6. When Regex Is the Wrong Tool

Consider stripping HTML tags:

```python
re.sub(r"<.*?>", "", '<a href="x">link</a>')
# 'link'      — works
```

Now an attribute containing `>`:

```python
re.sub(r"<.*?>", "", '<a href="a>b">link</a>')
# 'b">link'   — WRONG
```

The lazy `.*?` stops at the first `>`, which is inside the quoted attribute value. Patch that and
you will fail on the next case; patch again and fail on comments, or CDATA, or unclosed tags.

**The boundary is precise and worth stating properly.** Regular expressions describe **regular
languages**, which by definition cannot count arbitrarily deep nesting. HTML, JSON, and programming
languages are **context-free** — they permit unbounded nesting — so no regular expression can parse
them. This is not a limitation of Python's implementation; it is a theorem, and you will prove it
in **CS 301**. Week 11 of this course takes the first step toward that machinery.

| Use regex for | Use something else for |
|---|---|
| Validating a fixed-shape field | Nested or recursive structure |
| Extracting from a known line format | HTML → an HTML parser |
| Splitting on a set of delimiters | JSON → `json` |
| Find-and-replace with patterns | CSV → `csv` |
| Tokenising for a hand-written parser | Full parsing → a parser generator |

> **The one-line test:** if the format can nest inside itself, regex cannot parse it.

---

## 7. Practical Discipline

**Compile patterns used repeatedly.** `re.compile` does the parsing work once:

```python
DATE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
for line in lines:
    m = DATE.match(line)        # no recompilation per iteration
```

(`re` caches recent patterns internally, so this matters less than it once did — but it also
*documents* the pattern as a named constant, which is the larger benefit.)

**Use verbose mode for anything non-trivial:**

```python
EMAIL = re.compile(r"""
    [\w.+-]+        # local part
    @
    [\w-]+          # domain
    \.[\w.]+        # TLD (possibly multi-level)
""", re.VERBOSE)
```

`re.VERBOSE` ignores whitespace and allows comments. A regex you cannot read is a regex you cannot
maintain, and the write-only reputation of regular expressions comes almost entirely from patterns
that were never formatted.

Verified against that pattern with `fullmatch`:

| Input | Valid |
|---|---|
| `bob@example.com` | ✓ |
| `a@b.co` | ✓ |
| `not-an-email` | ✗ |
| `@x.com` | ✗ |

> **A warning about email.** This pattern is fine for a form field. It is **not** a correct
> implementation of the email address specification, which is genuinely baroque — the RFC-compliant
> regex is thousands of characters and still does not tell you whether the address exists. For real
> validation, check the shape loosely and then send a confirmation message. That is what every
> serious system does.

---

## 8. Summary

| Idea | Takeaway |
|---|---|
| Regex is a language for shapes | Declarative alternative to character loops |
| Always use raw strings | `r"\d"`, never `"\d"` |
| `match` / `search` / `fullmatch` | Anchored at start / anywhere / entire string |
| Validate with `fullmatch` | `search` accepts anything *containing* the pattern |
| Groups extract | Numbered, or named with `(?P<name>...)` |
| Greedy by default | Add `?` when a match swallows too much |
| Nested quantifiers → ReDoS | `(a+)+$` is exponential; 24 characters took 983 ms |
| Regex cannot parse nesting | Regular vs context-free — a theorem, proved in CS 301 |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict each result.

```python
re.findall(r"<.+>",  "<a><b>")
re.findall(r"<.+?>", "<a><b>")
re.match(r"world", "hello world")
re.findall(r"\d+", "a1b22c333")
re.split(r"[,;]\s*", "a, b; c")
```

**2. (Explain.)** A colleague validates a 4-digit PIN with `re.search(r"\d{4}", pin)`. Give two inputs it wrongly accepts and state the one-word fix.

**3. (Build.)** Write a function that extracts every `(hour, minute, level, message)` tuple from log lines of the form `2026-07-26 11:02:33 ERROR disk full`, skipping malformed lines. Use a named-group pattern in verbose mode.

**4. (Stretch.)** `^(a+)+$` takes 983 ms on 24 characters while `^a+$` handles 100,000 in 1.2 ms. Explain the mechanism, name the attack, and give two structural rules for avoiding it.

### Answers

**1.** `['<a><b>']`, `['<a>', '<b>']`, `None`, `['1', '22', '333']`, `['a', 'b', 'c']`.

The first two are the greedy/lazy contrast: `.+` runs to the end and backtracks to the *last* `>`,
producing one match spanning both tags; `.+?` stops at the *first* `>`, producing two.

`re.match` returns `None` because it anchors at position 0 and the text starts with `hello`. Use
`re.search` to find it anywhere.

**2.** It wrongly accepts anything *containing* four consecutive digits:

- `"12345"` — five digits; `search` finds a 4-digit run inside it
- `"drop table; 1234"` — arbitrary text with a valid-looking PIN buried in it

Also `"1234abcd"`, `"abc1234"`, and so on. The one-word fix is **`fullmatch`**:

```python
re.fullmatch(r"\d{4}", pin)
```

Equivalently, anchor the pattern: `re.match(r"\d{4}$", pin)`. Note `re.match(r"\d{4}", pin)` alone
is *still* wrong — it anchors only the start, so `"1234abcd"` passes.

This is a real security bug class, not a curiosity: using a containment test where an equality test
was intended is how validation gets bypassed.

**3.**

```python
import re

LOG = re.compile(r"""
    ^\d{4}-\d{2}-\d{2}          # date (matched, not captured)
    \s+
    (?P<hour>\d{2}):(?P<minute>\d{2}):\d{2}
    \s+
    (?P<level>[A-Z]+)
    \s+
    (?P<message>.+)$
""", re.VERBOSE)

def parse_log(lines):
    """Yield (hour, minute, level, message) for each well-formed line."""
    for line in lines:
        m = LOG.match(line)
        if m:                                  # skip malformed lines
            yield (m["hour"], m["minute"], m["level"], m["message"])
```

Three deliberate choices. **`^` and `$`** ensure the whole line has the expected shape rather than
merely containing it. **`.+` for the message** is safe here because it is the last element and
anchored by `$` — there is nothing after it to backtrack against. And **checking `if m:`** rather
than assuming a match is what makes malformed lines skip instead of raising `AttributeError` on
`None` — the single most common regex runtime error.

**4.** The mechanism is **ambiguity causing exponential backtracking**. In `^(a+)+$`, a run of `n`
a's can be partitioned among the repetitions of the outer group in exponentially many ways —
`(aaaa)`, `(aaa)(a)`, `(aa)(aa)`, `(a)(a)(a)(a)`, … When the trailing `!` makes `$` fail, the
backtracking engine tries **every partition** before it can report failure. Measured, the time
roughly quadruples per two added characters — 15.9 ms → 60.7 → 246.8 → 983.5 for 18 → 24
characters, i.e. Θ(2ⁿ).

`^a+$` admits exactly one way to match a given string, so there is nothing to backtrack through and
it is linear — 100,000 characters in 1.2 ms.

The attack is **ReDoS** (regular expression denial of service). A few dozen characters of input can
pin a CPU core indefinitely, which is why it appears in real outage postmortems.

Two structural rules:

1. **Never nest quantifiers over overlapping alternatives** — `(a+)+`, `(a*)*`, `(x|xx)+`. If two
   different parses of the same text are possible, the engine may have to try both.
2. **Make patterns as specific as possible, and anchor them.** `[^"]*` instead of `.*` inside
   quotes gives the engine no choice about where to stop; anchoring lets failure be detected without
   re-scanning.

A third, when it applies: use a **non-backtracking engine** (RE2, or Python's third-party `regex`
module in its POSIX mode) where linear time is guaranteed — accepting that backreferences become
unavailable, since they are precisely the feature that requires backtracking.

---

## Reading

- **Python docs — Regular Expression HOWTO** — the best introduction available; read it fully
- **Python docs — `re` module reference** — for the full syntax table
- **Friedl, *Mastering Regular Expressions*, Ch. 4–6** — optional, and the definitive treatment of
  the backtracking behaviour behind §5

---

*CS 101 · Week 9 · Lecture 30 (Fri) · © CSE Department*
