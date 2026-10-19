---
assessment: Quiz 2
course: CS 101
component: Quizzes
possible: 10
score: 10
status: graded
started: 2026-10-07
submitted: 2026-10-07
graded: 2026-10-07
source: "QUIZ 2 Week 2 Wednesday.md"
---

# CS 101 · Quiz 2
## Answer Sheet

**Assessment:** `QUIZ 2 Week 2 Wednesday.md`
**Points available:** 10

---

**Q1 (2 pts).** `x = 10; y = 3`

- **Line 3** `print(f"{x / y:.1f}")` → `3.3` (10/3 = 3.333…, formatted to 1 decimal).
- **Line 4** `print(f"{x // y}  {x % y}")` → `3  1` (floor division 3, remainder 1).
- **Line 5** `print(x * y == x ** 2 - x)` → `False` (`10*3 = 30`, `10**2 - 10 = 90`, and `30 == 90` is False).

*Marks: 2 / 2*

---

**Q2 (2 pts). Exact value and type.**

- (a) `int(3.9) + int(-3.9)` = `3 + (-3)` = **`0`**, type **`int`**. (`int()` truncates toward zero.)
- (b) `"ab" * 3 == "ababab"` → `"ababab" == "ababab"` → **`True`**, type **`bool`**.

*Marks: 2 / 2*

---

**Q3 (2 pts).**

```python
a = [1, 2, 3]
b = a
b.append(4)
a = a + [5]
print(len(b))
print(len(a))
```

- `len(b)` = **`4`**
- `len(a)` = **`5`**

**Why they differ:** `b.append(4)` **mutated** the one list that both `a` and `b` name, so `b` became
`[1, 2, 3, 4]`. Then `a = a + [5]` built a **new** list and **rebound** `a` to it (`[1, 2, 3, 4, 5]`),
leaving `b` pointing at the old list. Mutation is visible through every label; rebinding is visible
through one.

*Marks: 2 / 2*

---

**Q4 (2 pts).** `0 or "" or [] or "hello" or 42`

**Result:** `"hello"`.

`or` evaluates its operands left to right and returns the **first truthy** one (short-circuit).
`0`, `""` and `[]` are all falsy, so evaluation passes them and stops at `"hello"`; `42` is never
evaluated.

*Marks: 2 / 2*

---

**Q5 (2 pts).** A single expression that is `True` iff `n` is divisible by both 3 and 7 but not by 5:

```python
n % 3 == 0 and n % 7 == 0 and n % 5 != 0
```

(Equivalently, `n % 21 == 0 and n % 5 != 0`.)

*Marks: 2 / 2*

---

## Grading Summary

| | |
|---|---|
| **Score** | 10 / 10 |
| **Percent** | 100% |
| **Graded** | 2026-10-07 |

**Feedback:**
All correct per the answer key. Q1's three outputs are right, including `False` for the comparison.
Q2 gives the exact values and types. Q3 gets both lengths and explains mutation vs rebinding — the key
distinction. Q4 returns `"hello"` and explains short-circuiting. Q5 is a valid single expression
(the `% 21` form is also accepted).
