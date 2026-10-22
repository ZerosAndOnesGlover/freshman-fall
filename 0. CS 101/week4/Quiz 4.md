---
assessment: Quiz 4
course: CS 101
component: Quizzes
possible: 10
score: 10
status: graded
started: 2026-10-22
submitted: 2026-10-22
graded: 2026-10-22
source: "QUIZ 4 Week 4 Wednesday.md"
---

# CS 101 · Quiz 4
## Answer Sheet

**Assessment:** `QUIZ 4 Week 4 Wednesday.md` (covers Week 3: functions, scope, LEGB, call stack,
mutable defaults)
**Points available:** 10

All outputs verified by running the snippets under Python 3.

---

### Question 1  (2 points)

```python
x = 10
def outer():
    x = 20
    def inner():
        x = 30
        print(x)
    inner()
    print(x)
outer()
print(x)
```

**Output, line by line:**

```
30
20
10
```

`inner` assigns `x = 30` in its own **Local** namespace and prints that. `outer` has its own local
`x = 20`, which `inner` never touches (it never declares `nonlocal`), so after `inner()` returns
`outer` prints `20`. The module-level `x = 10` is untouched by either function and prints last.

---

### Question 2  (2 points)

```python
def append_item(item, lst=[]):
    lst.append(item)
    return lst
print(append_item("a")); print(append_item("b")); print(append_item("c"))
```

**Actual output:**

```
['a']
['a', 'b']
['a', 'b', 'c']
```

**Bug explanation:** The default value `lst=[]` is evaluated **once**, when the `def` statement runs —
not at each call. All three calls therefore share the *same* list object, which accumulates every item.

**Corrected version:**

```python
def append_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

(`None` is the sentinel; the fresh list is created per call. Using `if not lst:` would be wrong because
it would also replace a deliberately passed empty list.)

---

### Question 3  (2 points)

```python
def square(x): return x * x
def sum_squares(a, b): return square(a) + square(b)
result = sum_squares(3, 4)
```

**Deepest point (while `square(3)` is executing): 3 frames.**

Frames, bottom to top:

| Frame | Locals |
|---|---|
| `__main__` | `result` not yet assigned (the call is still being evaluated); module globals include `square`, `sum_squares` |
| `sum_squares` | `a = 3`, `b = 4`; paused at the first `square(a)` call |
| `square` | `x = 3` |

The second call `square(b)` has not begun, so its frame does not exist yet.

---

### Question 4  (2 points)

```python
x = "global"
def f():
    def g():
        print(x)     # (a)
    x = "local_f"
    g()
f()
print(x)             # (b)
```

**(a)** `print(x)` inside `g()` prints **`"local_f"`**, found in the **Enclosing** namespace — the local
scope of `f`. Because `f` assigns `x`, that name is local to `f` (not global), and `g` closes over it.

**(b)** The final `print(x)` prints **`"global"`**, found in the **Global** namespace. `f`'s assignment
created a separate local object and never modified the module-level `x`.

---

### Question 5  (2 points)

```python
compose = lambda f, g: lambda x: f(g(x))

# Verification:
assert compose(lambda x: x**2, lambda x: x + 1)(4) == 25
```

`compose` returns a closure `h` with `h(x) = f(g(x))`. Taking `f(x) = x**2` and `g(x) = x + 1` gives
`h(4) = f(g(4)) = (4 + 1)**2 = 25`.

---

## Grading Summary

| | |
|---|---|
| **Score** | 10 / 10 |
| **Percent** | 100% |
| **Graded** | 2026-10-22 |

**Feedback:**
Full marks. Q1 gives `30, 20, 10` and attributes each correctly under LEGB. Q2 reports the accumulating
output, identifies that the default list is created once at definition time, and the corrected version
uses the `None` sentinel correctly (with the right reason for not using `if not lst`). Q3 counts three
frames and gives the right locals in each, noting that `result` is still unassigned. Q4 gets both
namespaces right — `"local_f"` from Enclosing, `"global"` from Global — including the point that `f`'s
assignment makes `x` local to `f`. Q5's one-line closure is correct and verified to give `25`.
