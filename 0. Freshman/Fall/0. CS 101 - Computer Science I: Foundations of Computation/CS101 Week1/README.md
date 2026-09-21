# CS 101 · Week 1 Data, Types, Variables, and Expressions

---

## Contents

```
CS101_Week1/
│
├── README.md                                 ← You are here
│
├── lectures/
│   ├── L04 Data Types Variables.md           ← Wed: Python object model, mutability,
│   │                                              int/float/str/None deep dive
│   ├── L05 Expressions and Operators.md      ← Thu: Evaluation model, precedence,
│   │                                              short-circuit, bitwise operators
│   └── L06 Type System and REPL.md           ← Fri: Strong/dynamic typing,
│                                                  conversions, math module, REPL workflow
│
├── lab/
│   ├── LAB 1 Type Exploration.md              ← Tue 6 Oct (W2): Python Tutor, predictions,
│   │                                              f-string formatting, converter
│   ├── starter_converter.py                  ← Lab starter — fill in the conversions
│   └── [type_experiments.py, precedence_test.py, etc. — you create these]
│
├── assignments/
│   ├── QUIZ 1 Week 1 Wednesday.md                 ← In-class quiz (10 min, covers Week 0)
│   ├── PS 1 Data Types and Expressions.md     ← Problem Set 1 (due Fri 9 Oct, 17:00)
│   └── ps1_starter.py                        ← PS1 starter code with TODOs
│
├── resources/
│   └── Reading Guide Week 1.md                ← Reading, REPL sessions, videos, mistakes
│
└── solutions_instructor/
    └── LAB 1 Solutions.md                     ← Expected answers and marking notes
```

---

## Week 1 at a Glance

**Theme:** Data, the raw material of all computation. What it is, how Python organizes it, and how to compute with it.

| Day | Event | Topic |
|-----|-------|-------|
| Wed 30 Sep | Lecture 4 + Quiz 1 | Python object model, types deep dive, mutable vs immutable |
| Thu 1 Oct | Lecture 5 | Expressions, evaluation model, operator precedence, bitwise |
| Fri 2 Oct | Lecture 6 + PS1 released | Type system, conversions, `math`, REPL as thinking tool |
| Tue 6 Oct (W2) | Lab 1 (graded) | Python Tutor, predict-then-run, formatting, converter |

---

## Your To-Do List

### Before Wednesday
- [ ] Complete Lab 0 if not already done
- [ ] Read the Week 1 Reading Guide
- [ ] Watch "Python Names and Values" (Ned Batchelder, PyCon 2015) — 25 min

### Wednesday
- [ ] Quiz 1 (first 10 minutes of lecture, covers Week 0 material)
- [ ] Take notes during L04

### Before Thursday
- [ ] Reread L04 notes
- [ ] REPL Session A from the Reading Guide (mutability exploration)

### Thursday
- [ ] Take notes during L05
- [ ] Try the REPL Session B (short-circuit evaluation)

### Tuesday 6 October Lab, Week 2 (Required)
- [ ] Complete all parts of LAB1
- [ ] Finish `converter.py` from `starter_converter.py`
- [ ] Get TA checkoff

### Friday
- [ ] Take notes during L06
- [ ] PS1 is released — read all parts tonight
- [ ] Begin Part A (written questions) over the weekend

### Weekend
- [ ] Start PS1 — at minimum complete Part A and B1, B2
- [ ] Watch "Floating Point Numbers" (Computerphile) — explains PS1 written Q4

---

## The Core Ideas of Week 1

**1. Everything in Python is an object.**
Every value has identity (`id()`), type (`type()`), and value. Variables are labels (references) to objects, not containers.

**2. Mutable vs. immutable is the single most important distinction in Python.**
`int`, `float`, `str`, `bool`, `tuple`, `None` = immutable (cannot change after creation).
`list`, `dict`, `set` = mutable (can change in place).
When you assign `y = x` for a mutable object, `y` and `x` refer to the **same** object.

**3. Python is dynamically typed but strongly typed.**
- Dynamically typed: variables can hold any type at any time; type checking is at runtime
- Strongly typed: Python refuses silent conversion between unrelated types

**4. Operator precedence follows strict rules.**
`**` (right-assoc) > `*//%` > `+-` > comparisons > `not` > `and` > `or`
When in doubt: use parentheses.

**5. Short-circuit evaluation returns operands, not just booleans.**
`x and y` returns `x` if x is falsy, else returns `y`.
`x or y` returns `x` if x is truthy, else returns `y`.

**6. Float arithmetic is approximate.**
`0.1 + 0.2 != 0.3`. Use `math.isclose()` for float comparisons.

**7. `int()` truncates, `round()` uses banker's rounding.**
`int(3.9) = 3`, `int(-3.9) = -3`. `round(2.5) = 2`, `round(3.5) = 4`.

---

## Quick Self-Test

Can you answer these without looking at your notes?

1. What is the result of `2 ** 3 ** 2`? Why?
2. What is the result of `0 or "" or [] or 42`?
3. What does `int(-7.9)` return? Why?
4. Why is `0.1 + 0.2 == 0.3` False?
5. You write `a = [1,2,3]; b = a; b.append(4)`. What does `print(a)` output?
6. What is the difference between `str(x)` and `repr(x)` for a string `x`?
7. What does `"hello"[::-1]` return?
8. What does `bool([False])` return? Why?

*(Answers: 512, 42, -3, floating-point imprecision, [1,2,3,4], repr adds quotes, "olleh", True — non-empty list is truthy regardless of contents)*

---

*CS 101 · Week 1 · © CSE Department*
