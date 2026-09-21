# CS 101 · Quiz 4
## Week 4, Wednesday — In-Class Assessment

**Date:** Wednesday 21 October 2026 · 09:00–09:10 (start of L13) · Week 4
**Duration:** 10 minutes (first 10 minutes of Wednesday lecture)
**Format:** Written — closed book, closed notes
**Covers:** Week 3 material: functions, scope, LEGB, call stack, mutable defaults

---

### Question 1 (2 points)

What is the output? If it raises an error, name the error type and explain why.

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

Line by line output:

---

### Question 2 (2 points)

This function has a famous Python bug. What is it, what is the actual output of the three calls, and write the corrected version.

```python
def append_item(item, lst=[]):
    lst.append(item)
    return lst

print(append_item("a"))
print(append_item("b"))
print(append_item("c"))
```

Actual output:

Bug explanation:

Corrected version:
```python


```

---

### Question 3 (2 points)

How many stack frames are on the call stack at the deepest point of this execution? List them from bottom to top, with the value of all local variables in each frame.

```python
def square(x):
    return x * x

def sum_squares(a, b):
    return square(a) + square(b)

result = sum_squares(3, 4)
```

Deepest point (when `square(3)` is executing):

Frames (bottom → top):

---

### Question 4 (2 points)

What does each expression evaluate to? Give the value and explain which namespace Python finds it in.

```python
x = "global"

def f():
    def g():
        print(x)    # (a) which x?
    x = "local_f"
    g()

f()
print(x)            # (b) which x?
```

(a) `print(x)` inside `g()` prints: ___ found in ___ namespace
(b) final `print(x)` prints: ___ found in ___ namespace

---

### Question 5 (2 points)

Write a one-line Python function `compose(f, g)` that returns a new function `h` such that `h(x) = f(g(x))`.

Then write one line showing that `compose(lambda x: x**2, lambda x: x+1)(4)` equals `25`.

```python
compose = 

# Verification:

```

---

**Total: 10 points**

---

## Answer Key (Instructor Copy)

**Q1:**
```
30      ← inner()'s local x
20      ← outer()'s local x (not modified by inner)
10      ← global x (not modified by either function)
```
LEGB: `inner` finds `x=30` in Local. `outer` finds `x=20` in its own Local. Global `x=10` unchanged.

**Q2:**
Actual output:
```
['a']
['a', 'b']
['a', 'b', 'c']
```
Bug: `lst=[]` is evaluated **once** at function definition time, not at each call. All calls share the same list object.

Corrected:
```python
def append_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

**Q3:** When `square(3)` is executing, there are **3 frames** on the stack:
```
Bottom: __main__ — result = ???
Middle: sum_squares — a=3, b=4 (paused at first square call)
Top:    square — x=3
```

**Q4:**
(a) prints `"local_f"` — found in **Enclosing** (outer function `f`'s) namespace.
(b) prints `"global"` — found in **Global** namespace. `f`'s local `x` does not affect the global.

**Q5:**
```python
compose = lambda f, g: lambda x: f(g(x))

# Verification:
assert compose(lambda x: x**2, lambda x: x+1)(4) == 25
# (4+1)**2 = 5**2 = 25
```

---

*CS 101 · Week 4 · Quiz 4 · © CSE Department*
