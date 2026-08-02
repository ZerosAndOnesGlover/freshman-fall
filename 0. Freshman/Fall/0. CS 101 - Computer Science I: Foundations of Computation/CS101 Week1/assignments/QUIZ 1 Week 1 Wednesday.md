# CS 101 Quiz 1
## Week 1, Wednesday: In-Class Assessment

**Duration:** 10 minutes (first 10 minutes of Wednesday lecture)
**Format:** Written: closed book, closed notes
**Weight:** Part of lab/quiz participation grade

---

> This quiz covers Week 0 material: CS as a discipline, Turing Machines,
> computation, Python types, variables, and expressions.
> It is designed to take 5–7 minutes. If you studied, it is easy.

---

### Question 1 (2 points)

Circle all values below that are **falsy** in Python:

```
0        1        ""        "False"        []        [0]        None        False        0.0
```

---

### Question 2 (2 points)

What is the output of the following code? If it raises an error, name the error type.

```python
x = "5"
y = 3
print(x * y)
print(x + y)
```

Line 3 output: "555"

Line 4 output or error: TypeError

---

### Question 3 (2 points)

What is the value of each expression?

```python
(a)  2 ** 3 ** 2     = 512

(b)  10 // 3 + 10 % 3  = 4
```

---

### Question 4 (2 points)

Complete the blanks:

A **Turing Machine** consists of an infinite tape, a read/write head, and a finite set of instructions with transition states.

The **Halting Problem** is the question of whether, given any program P and input I, P will halt. Turing proved this is undecidable (decidable / undecidable).

---

### Question 5 (2 points)

What is the difference between `==` and `is` in Python?

== compares values while is checks if the values are from the same object.

Write a specific, concrete example of when you should use `is` instead of `==`:

We use `is` when we want to check if two objects are the same.

---

**Total: 10 points**

---

## Answer Key (Instructor Copy)

**Q1:** Falsy values: `0`, `""`, `[]`, `None`, `False`, `0.0`
Not falsy: `1`, `"False"` (non-empty string), `[0]` (non-empty list)

**Q2:**
- Line 3: `555` — string repetition: `"5" * 3 = "555"`
- Line 4: `TypeError: can only concatenate str (not "int") to str`

**Q3:**
- (a) `2 ** 3 ** 2` = `2 ** 9` = `512` (right-associative)
- (b) `10 // 3 + 10 % 3` = `3 + 1` = `4`

**Q4:**
Turing Machine: tape, head, states
Halting Problem: halt (terminate), undecidable

**Q5:**
`==` tests value equality: do two objects have the same value?
`is` tests identity: are two variables pointing to the same object?
Use `is` for: `x is None` (checking for None — correct idiom since there is only one None object)

---

*CS 101 · Week 1 · Quiz 1 · © CSE Department*
