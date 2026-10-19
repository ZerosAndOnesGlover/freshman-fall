---
assessment: Quiz 1
course: CS 101
component: Quizzes
possible: 10
score: 10
status: graded
started: 2026-09-30
submitted: 2026-09-30
graded: 2026-09-30
source: "QUIZ 1 Week 1 Wednesday.md"
---

# CS 101 · Quiz 1
## Answer Sheet

**Assessment:** `QUIZ 1 Week 1 Wednesday.md`
**Points available:** 10

---

**Q1 (2 pts). Circle the falsy values.**

```
0        1        ""        "False"        []        [0]        None        False        0.0
```

**Falsy:** `0`, `""`, `[]`, `None`, `False`, `0.0`.
**Not falsy:** `1`, `"False"` (a non-empty string is truthy whatever it contains), `[0]` (a non-empty
list is truthy whatever it contains).

*Marks: 2 / 2*

---

**Q2 (2 pts).** `x = "5"; y = 3`

- **Line 3** `print(x * y)` → `555` — string repetition: `"5" * 3 = "555"`.
- **Line 4** `print(x + y)` → **`TypeError: can only concatenate str (not "int") to str`** —
  `+` between `str` and `int` is not defined.

*Marks: 2 / 2*

---

**Q3 (2 pts).**

- (a) `2 ** 3 ** 2` = `2 ** (3 ** 2)` = `2 ** 9` = **`512`** (`**` is right-associative).
- (b) `10 // 3 + 10 % 3` = `3 + 1` = **`4`**.

*Marks: 2 / 2*

---

**Q4 (2 pts). Complete the blanks.**

A **Turing Machine** consists of an infinite **tape**, a read/write **head**, and a finite set of
**states**.

The **Halting Problem** is the question of whether, given any program P and input I, P will **halt**
(terminate). Turing proved this is **undecidable**.

*Marks: 2 / 2*

---

**Q5 (2 pts).** `==` vs `is`.

`==` tests **value equality**: do the two objects have the same value? `is` tests **identity**: do the
two names refer to the *same* object?

Concrete example: use `is` when checking for `None` — write `if x is None:` rather than `x == None`,
because there is only ever one `None` object, so identity is the correct and idiomatic test.

*Marks: 2 / 2*

---

## Grading Summary

| | |
|---|---|
| **Score** | 10 / 10 |
| **Percent** | 100% |
| **Graded** | 2026-09-30 |

**Feedback:**
All correct per the answer key. Q1 lists exactly the six falsy values and correctly keeps `"False"`
and `[0]` as truthy. Q2 gives `555` and names `TypeError` with the concatenation message. Q3 respects
`**` right-associativity and integer precedence. Q4 completes the machine and Halting-Problem blanks.
Q5 distinguishes value equality from identity and gives the canonical `x is None` example.
