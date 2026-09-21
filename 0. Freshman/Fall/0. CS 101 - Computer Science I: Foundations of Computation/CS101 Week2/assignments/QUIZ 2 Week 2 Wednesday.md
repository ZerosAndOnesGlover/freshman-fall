# CS 101 · Quiz 2
## Week 2, Wednesday: In-Class Assessment

**Date:** Wednesday 7 October 2026 · 09:00–09:10 (start of L07) · Week 2
**Duration:** 10 minutes (first 10 minutes of Wednesday lecture)
**Format:** Written — closed book, closed notes
**Covers:** Week 1 material: types, expressions, operators, type conversions

---

### Question 1 (2 points)

What is the output? If it raises an error, name the error type.

```python
x = 10
y = 3
print(f"{x / y:.1f}")
print(f"{x // y}  {x % y}")
print(x * y == x ** 2 - x)
```

Line 3: _______________
Line 4: _______________
Line 5: _______________

---

### Question 2 (2 points)

What does each expression evaluate to? Give the **exact value and type**.

```python
(a)  int(3.9) + int(-3.9)     →  value: ___  type: ___

(b)  "ab" * 3 == "ababab"     →  value: ___  type: ___
```

---

### Question 3 (2 points)

What is printed?

```python
a = [1, 2, 3]
b = a
b.append(4)
a = a + [5]
print(len(b))
print(len(a))
```

`len(b)` = ___
`len(a)` = ___

Explain in one sentence why `a` and `b` have different lengths at the end:

---

### Question 4 (2 points)

What does this expression evaluate to? Show your reasoning.

```python
0 or "" or [] or "hello" or 42
```

Result: _______________

Why (explain short-circuit evaluation in one sentence): _______________

---

### Question 5 (2 points)

Write a single Python expression (not a statement — no `=`, no `if` statement) that evaluates to `True` if and only if integer `n` is divisible by both 3 and 7 but not by 5.

Expression: _______________

---

**Total: 10 points**

---

## Answer Key (Instructor Copy)

**Q1:**
- Line 3: `3.3`  (10/3 = 3.333..., formatted to 1 decimal place)
- Line 4: `3  1` (floor division 3, remainder 1)
- Line 5: `False` — `10*3=30`, `10**2-10=100-10=90`. `30 == 90` is False

**Q2:**
- (a) `int(3.9) + int(-3.9)` = `3 + (-3)` = `0`, type `int`
  (both truncate toward zero)
- (b) `"ab" * 3 == "ababab"` → `"ababab" == "ababab"` → `True`, type `bool`

**Q3:**
- `len(b)` = `4`
- `len(a)` = `5`
- Explanation: `b.append(4)` mutates the original list (b and a pointed to the same object). Then `a = a + [5]` creates a NEW list and rebinds `a` to it, so `a` and `b` now point to different objects.

**Q4:**
- Result: `"hello"`
- `or` short-circuits: evaluates operands left to right, returns the first truthy value.
- `0` is falsy → skip; `""` is falsy → skip; `[]` is falsy → skip; `"hello"` is truthy → return `"hello"` (never evaluates `42`)

**Q5:**
```python
n % 3 == 0 and n % 7 == 0 and n % 5 != 0
```
Or equivalently: `n % 21 == 0 and n % 5 != 0`

---

*CS 101 · Week 2 · Quiz 2 · © CSE Department*
