# CS 101 · Week 9: Strings and Regular Expressions

---

## Contents

```
CS101_Week9/
│
├── README.md                                    ← You are here
│
├── lectures/
│   ├── L28 Strings as a Data Structure.md       ← Wed: immutability, the Θ(n²) concat trap and
│   │                                                 the benchmark that hides it, code points vs
│   │                                                 bytes, normalisation, str/bytes boundary
│   ├── L29 String Algorithms and Text           ← Thu: naive search Θ(n·m), why the built-in is
│   │   Processing.md                                2000x faster, tokenising, why split breaks on
│   │                                                 quoted CSV, palindromes, the anagram trap
│   └── L30 Regular Expressions.md               ← Fri: the regex language, match/search/fullmatch,
│                                                     groups, greedy vs lazy, ReDoS, and the
│                                                     regular-vs-context-free boundary
│
├── lab/
│   ├── LAB 9 Text Processing and Regex.md       ← Tue: measure the concat trap and defeat the
│   │                                                 refcount optimisation, instrument naive
│   │                                                 search, build a log parser, demonstrate ReDoS
│   └── text_lab_starter.py                      ← Lab starter — benchmarks + ReDoS harness ready
│                                                     to run, search/regex parts as TODOs
│
├── assignments/
│   ├── QUIZ 9 Week 9 Wednesday.md               ← In-class quiz (covers Week 8)
│   ├── PS 9 Strings and Regular Expressions.md  ← Problem Set 9 (due Friday Week 10)
│   └── ps9_starter.py                           ← Scaffold with a 16-test self-check suite
│
├── resources/
│   └── Reading Guide Week 9.md                  ← 3 REPL sessions, cost model + regex reference
│                                                     cards, 10-question self-test
│
└── solutions_instructor/
    └── LAB 9 Solutions.md                       ← Verified timings, expected answers, marking notes
```

---

## Week 9 at a Glance

**Theme:** Text is the most common data type in computing, and the one with the most hidden edges.
This week gives you a cost model for strings, the algorithms that operate on them, and a
declarative pattern language — plus a clear account of where each stops working.

| Day | Event | Topic |
|-----|-------|-------|
| Wed | Lecture 28 + Quiz 9 | Immutability, the concatenation trap, encoding and normalisation |
| Thu | Lecture 29 | Substring search cost, tokenising, transformation patterns |
| Fri | Lecture 30 + PS9 released | Regular expressions, greedy vs lazy, ReDoS, the regex boundary |
| Tue | Lab 9 (graded) | Measure everything above yourself |

**📌 Project 1 (Data Analysis Tool) is due this Friday.** See Week 7's `PROJECT 1` file.

---

## Your To-Do List

### Before Wednesday
- [ ] Review Week 8 — Quiz 9 covers hash tables, load factor, dict/set patterns
- [ ] **Finish Project 1** — it is due Friday

### Wednesday
- [ ] Quiz 9 (10 min — covers Week 8)
- [ ] Notes for L28
- [ ] REPL Session A (the encoding boundary)

### Before Thursday
- [ ] Read the Python **Unicode HOWTO** completely
- [ ] REPL Session B (catch the concatenation trap honestly)

### Thursday
- [ ] Notes for L29
- [ ] Read the **Regular Expression HOWTO** before Friday

### Friday
- [ ] Notes for L30
- [ ] REPL Session C (regex reflexes)
- [ ] **Submit Project 1**
- [ ] PS9 released — read it completely

### Tuesday Lab (Required, Graded)
- [ ] Both concatenation benchmarks; identify the quadratic ratio
- [ ] `naive_search` agreeing with `str.find`; confirm the (n−k)(k+1) formula
- [ ] Log parser with named groups that skips malformed lines
- [ ] Find an input the `search`-based validator wrongly accepts
- [ ] ReDoS timings and explanation
- [ ] TA checkoff

### Weekend
- [ ] Start PS9 — at minimum A1–A2 (written) and B1–B3 (code)

---

## The Central Ideas of Week 9

**1. Strings are immutable, so every edit allocates.**
Building one with `+=` in a loop copies everything accumulated so far each time — Θ(n²). Collect
pieces in a list and `"".join` once for Θ(n).

**2. A benchmark can hide the behaviour it is measuring.**
CPython resizes a string in place when nothing else references it, which makes the naive loop look
linear. Keep a live alias and the true Θ(n²) appears: 1.1 ms → 20 ms → 314 ms as n quadruples
twice. **When a measurement contradicts the theory, check the measurement first.**

**3. `str` is code points; `bytes` is bytes.**
`len("café")` is 4 but its UTF-8 encoding is 5 bytes, and `len("👋🏽")` is 2 because it is a base
emoji plus a modifier. Decode at input, work in `str`, encode at output.

**4. Equal-looking is not equal.**
`"é"` has two different code-point spellings. Without NFC normalisation they compare unequal and
hash differently — so a user can register under one and fail to log in with the other.

**5. Naive substring search is Θ(n·m); the built-in is O(n+m).**
Measured: 1.6 million comparisons at n=32,000, and `str.find` is about 2000× faster. Fast
algorithms all share one idea — **a failed match tells you something**, so do not throw it away.

**6. Regex is a language for shapes, with two hard limits.**
It cannot parse anything that nests (regular vs context-free — a theorem, proved in CS 301), and a
badly written pattern can be exponential. `^(a+)+$` took 983 ms on 24 characters; `^a+$` handles
100,000 in 1.2 ms.

**7. Validation means `fullmatch`.**
`search` asks whether the pattern appears *somewhere*, which accepts
`"drop table; 1234"` as a 4-digit PIN. This is a real bypass class, not a technicality.

---

## Quick Self-Check

Without notes:

1. Why is `s += c` in a loop Θ(n²), and why might a benchmark not show it?
2. What is `len("👋🏽")`? Why?
3. Give the two code-point sequences for `é` and the call that reconciles them.
4. `re.match` vs `re.search` vs `re.fullmatch` — which validates, and why the other two do not.
5. Why does `re.findall(r"<.+>", "<a><b>")` return one match? Give the fix.
6. Worst case for naive search, and the input that triggers it.
7. Give a CSV line that `line.split(",")` parses wrongly.
8. Why is `^(a+)+$` exponential but `^a+$` linear?
9. State the language-class reason regex cannot parse HTML.
10. Name two problems where regex is tempting but wrong.

*(Answers: 1. each `+=` copies everything accumulated, n(n+1)/2 copies total; CPython resizes in
place when the refcount is 1, which the naive loop satisfies. 2. 2 — base emoji + skin-tone
modifier. 3. `U+00E9` vs `U+0065 U+0301`; `unicodedata.normalize("NFC", …)`. 4. start / anywhere /
whole string — **fullmatch**, because the others accept strings merely *containing* the pattern.
5. `.+` is greedy and backtracks to the last `>`; use `<.+?>`. 6. Θ(n·m), from a needle that almost
matches everywhere such as `"aaa…ab"` against `"aaaa…a"`. 7. `'name,"Smith, John",42'`. 8. the
nested quantifier makes the parse ambiguous, so failing requires trying exponentially many
partitions. 9. regex describes regular languages; HTML is context-free, and regular languages
cannot count unbounded nesting. 10. parsing HTML/JSON/any nested format; CSV with quoted fields.)*

---

## Techniques Introduced This Week

| Technique | Complexity | Key Idea |
|---|---|---|
| Accumulator + `join` | Θ(n) | Replaces the Θ(n²) `+=` loop |
| NFC normalisation | Θ(n) | Makes equal-looking text actually equal |
| Naive substring search | Θ(n·m) worst | Every alignment, restarting from scratch |
| Two-way search (built-in) | O(n+m) | Reuses what the failed match revealed |
| Named-group extraction | Θ(n) | One pattern replaces a hand-written parser |
| `fullmatch` validation | Θ(n) | Whole-string match, not containment |
| Lazy quantifiers `+?` | — | Fix for "the match swallowed too much" |
| `csv` for delimited data | Θ(n) | Handles quoting that `split` cannot |

---

*CS 101 · Week 9 · © CSE Department*
