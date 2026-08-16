# CS 101 · Lecture 11 (Week 3, Lecture 2)
## Scope, Namespaces, and the Call Stack

**Week 3 · Thursday**
*"The call stack is one of the most important data structures you will ever understand." — CS 101*

**Date:** Thursday 10 September 2026 · 09:00–09:50 · Week 3

---

## 0. The Question This Lecture Answers

When you write `x = 5` in one function and then `x = 10` in another, why don't they interfere? When a function calls another function, where do its variables go? When that function returns, how does Python know where to continue executing?

The answer is the **call stack** — the data structure that manages every function call in your program. Understanding it transforms function calls from magic into mechanism.

---

## 1. Namespaces — Where Names Live

A **namespace** is a mapping from names to objects — essentially, a dictionary that Python searches when you use a name.

```python
x = 10          # binds 'x' in the module (global) namespace

def foo():
    y = 20      # binds 'y' in foo's local namespace
    print(x)    # looks up 'x': not in local → check global → found: 10
    print(y)    # looks up 'y': found in local: 20

foo()
print(y)        # NameError: 'y' not in global namespace
```

Every Python program has multiple namespaces active simultaneously:
- **Built-in namespace**: `print`, `len`, `int`, `range`, ... — always available
- **Global (module) namespace**: names defined at the top level of a file
- **Local namespace**: names defined inside a currently-executing function

---

## 2. The LEGB Rule — Python's Name Resolution Order

When Python encounters a name, it searches namespaces in this exact order:

```
L → Local      (inside the current function)
E → Enclosing  (inside any enclosing functions — for nested functions)
G → Global     (the module's top-level namespace)
B → Built-in   (Python's built-in names: print, len, etc.)
```

First match wins. If the name is not found in any namespace: `NameError`.

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        # x = "local"   # If this line existed, 'local' wins
        print(x)        # No local x → check enclosing → finds "enclosing"

    inner()

outer()   # prints "enclosing"
print(x)  # prints "global" — global namespace unchanged
```

```python
# Built-in shadowing — don't do this:
len = 42            # shadows the built-in len()
print(len("hello")) # TypeError: 'int' object is not callable
del len             # restore it
print(len("hello")) # 5 — built-in restored
```

---

## 3. The Call Stack — The Full Mechanical Picture

The **call stack** (also called the **execution stack** or **runtime stack**) is a stack data structure that Python maintains to track function calls.

Each time a function is called, Python **pushes** a new **stack frame** onto the stack. Each frame contains:
- The function's **local variables** (its namespace)
- The **return address** — where to continue executing after the function returns
- A reference to the **calling frame** (the frame below it on the stack)

When a function returns, its frame is **popped** off the stack, and execution resumes in the frame below.

### Concrete example — tracing the stack

```python
def add(a, b):
    result = a + b
    return result

def compute(x):
    doubled = add(x, x)
    tripled = add(x, doubled)
    return tripled

y = compute(5)
```

The stack evolves like this:

```
Step 1: Call compute(5)
┌─────────────────────┐
│ compute             │ ← top of stack (active frame)
│   x = 5            │
│   [executing]      │
├─────────────────────┤
│ __main__ (global)  │ ← bottom frame
│   y = ???          │
└─────────────────────┘

Step 2: compute calls add(5, 5)
┌─────────────────────┐
│ add                 │ ← top of stack
│   a = 5, b = 5     │
│   result = ???     │
├─────────────────────┤
│ compute             │
│   x = 5            │
│   doubled = ???    │
├─────────────────────┤
│ __main__            │
│   y = ???          │
└─────────────────────┘

Step 3: add(5,5) executes: result = 10; returns 10
        add's frame is popped; compute resumes
┌─────────────────────┐
│ compute             │ ← top of stack again
│   x = 5            │
│   doubled = 10     │ ← return value stored
│   [executing]      │
├─────────────────────┤
│ __main__            │
│   y = ???          │
└─────────────────────┘

Step 4: compute calls add(5, 10)
┌─────────────────────┐
│ add                 │
│   a = 5, b = 10    │
│   result = ???     │
├─────────────────────┤
│ compute             │
│   x = 5            │
│   doubled = 10     │
│   tripled = ???    │
├─────────────────────┤
│ __main__            │
│   y = ???          │
└─────────────────────┘

Step 5: add returns 15; compute returns 15; y = 15
┌─────────────────────┐
│ __main__            │ ← only frame remaining
│   y = 15           │
└─────────────────────┘
```

**The critical insight:** Every function call gets its own frame with its own namespace. `result` in `add` is completely separate from any variable named `result` in `compute` or in `__main__`. They live in different frames on the stack.

---

## 4. Viewing the Call Stack with `traceback`

Python shows you the call stack whenever an exception propagates up through multiple calls:

```python
def c():
    return 1 / 0

def b():
    return c()

def a():
    return b()

a()
```

```
Traceback (most recent call last):
  File "example.py", line 10, in <module>
    a()
  File "example.py", line 8, in a
    return b()
  File "example.py", line 5, in b
    return c()
  File "example.py", line 2, in c
    return 1 / 0
ZeroDivisionError: division by zero
```

Read this from **bottom to top**: the error occurred in `c`, which was called by `b`, called by `a`, called at the module level. This is the call stack at the moment of the exception — Python prints it so you know exactly how execution reached the error.

---

## 5. Variable Scope — The Precise Rules

### Local scope

Variables assigned inside a function are **local** — they exist only during that function call:

```python
def foo():
    x = 10    # local to foo
    return x

foo()
print(x)      # NameError: 'x' is not defined in global scope
```

### Accessing (not modifying) global variables

A function can **read** a global variable without any special declaration:

```python
PI = 3.14159    # global

def circle_area(r):
    return PI * r * r    # reads PI from global scope — fine
```

### Modifying global variables — the `global` keyword

To **assign** to a global variable inside a function, you must declare it with `global`:

```python
count = 0    # global

def increment():
    global count    # declares: 'count' refers to the global variable
    count += 1      # modifies the global

increment()
increment()
print(count)    # 2
```

Without `global count`, `count += 1` would create a **new local variable** `count` — it would not modify the global. This is a common source of bugs:

```python
count = 0

def increment_broken():
    count += 1    # UnboundLocalError! Python sees 'count' is assigned,
                  # so it's local — but it's read before being assigned

increment_broken()    # UnboundLocalError: local variable 'count' referenced before assignment
```

**Advice:** Avoid `global` in production code. It creates invisible coupling between a function and its environment. Return values and parameters are almost always the right approach.

### The `nonlocal` keyword (enclosing scope)

For nested functions, `nonlocal` modifies a variable in the enclosing (not global) scope:

```python
def make_counter():
    count = 0                 # enclosing scope variable
    def increment():
        nonlocal count        # refers to 'count' in make_counter's scope
        count += 1
        return count
    return increment          # return the function itself (more on this later)

counter = make_counter()
print(counter())   # 1
print(counter())   # 2
print(counter())   # 3
```

This pattern — a function carrying state from its enclosing scope — is called a **closure**. It's one of the most powerful concepts in programming. We'll explore closures deeply in Week 9 (decorators and functional programming).

---

## 6. Default Parameter Values

Functions can have parameters with default values — making those arguments optional:

```python
def greet(name, greeting="Hello", punctuation="!"):
    return f"{greeting}, {name}{punctuation}"

greet("Alice")                         # "Hello, Alice!"
greet("Bob", greeting="Hi")            # "Hi, Bob!"
greet("Charlie", punctuation=".")      # "Hello, Charlie."
greet("Diana", "Hey", "?")            # "Hey, Diana?"
```

Parameters with defaults must come **after** parameters without defaults.

### ⚠️ The Mutable Default Trap — One of Python's Most Notorious Bugs

**Never use a mutable object (list, dict, set) as a default value:**

```python
# WRONG — this is a famous Python gotcha:
def append_to(item, lst=[]):    # lst=[] is evaluated ONCE at definition time
    lst.append(item)
    return lst

print(append_to(1))    # [1]   — seems fine
print(append_to(2))    # [1, 2] — WRONG! Same list object reused!
print(append_to(3))    # [1, 2, 3] — the default list is accumulating
```

**Why:** Default values are evaluated when the `def` statement runs, not when the function is called. The same list object is reused across all calls.

**The correct pattern:**

```python
# CORRECT — use None as sentinel, create new list inside:
def append_to(item, lst=None):
    if lst is None:
        lst = []    # create a NEW list each time
    lst.append(item)
    return lst

print(append_to(1))    # [1]
print(append_to(2))    # [2]  — fresh list
print(append_to(3))    # [3]  — fresh list
```

Memorize this pattern. You will encounter this bug in real codebases.

---

## 7. `*args` and `**kwargs` — Variable-Length Arguments

### `*args` — arbitrary positional arguments

```python
def sum_all(*args):
    """Accept any number of positional arguments."""
    total = 0
    for n in args:      # args is a tuple
        total += n
    return total

sum_all(1, 2, 3)         # 6
sum_all(1, 2, 3, 4, 5)  # 15
sum_all()                # 0
```

### `**kwargs` — arbitrary keyword arguments

```python
def describe(**kwargs):
    """Accept any number of keyword arguments."""
    for key, value in kwargs.items():   # kwargs is a dict
        print(f"  {key}: {value}")

describe(name="Alice", age=20, major="CS")
# name: Alice
# age: 20
# major: CS
```

### Combined usage

```python
def flexible(required, *args, **kwargs):
    print(f"required: {required}")
    print(f"extra positional: {args}")
    print(f"keyword args: {kwargs}")

flexible("hello", 1, 2, 3, color="red", size=10)
# required: hello
# extra positional: (1, 2, 3)
# keyword args: {'color': 'red', 'size': 10}
```

The `*args`/`**kwargs` pattern is used throughout Python's standard library. Understanding it lets you read and write any Python API.

---

## 8. Stack Overflow — When the Stack Runs Out

The call stack has a finite size. If functions call each other too deeply, the stack fills up:

```python
def infinite_descent(n):
    return infinite_descent(n - 1)   # calls itself forever

infinite_descent(1000)
# RecursionError: maximum recursion depth exceeded
```

Python's default recursion limit is 1000 frames (configurable but rarely worth changing). We'll revisit this in Week 4 (recursion) — understanding the stack is the key to understanding why recursion limits exist.

---

## 9. Lambda Functions — Anonymous One-Liners

```python
# Regular function:
def square(x):
    return x * x

# Equivalent lambda:
square = lambda x: x * x

# Inline usage (most common):
numbers = [3, 1, 4, 1, 5, 9]
numbers.sort(key=lambda x: -x)    # sort descending
print(numbers)    # [9, 5, 4, 3, 1, 1]
```

`lambda` creates an anonymous function — a function without a `def` name. It is limited to a single expression (no statements, no multiple lines). Use lambdas for short inline functions; for anything complex, use `def`.

---

## 10. Summary

| Concept | Key Point |
|---------|-----------|
| Namespace | A mapping from names to objects; Python searches them in LEGB order |
| LEGB rule | Local → Enclosing → Global → Built-in; first match wins |
| Stack frame | Created on each function call; holds local variables and return address |
| Call stack | Stack of frames; grows on call, shrinks on return |
| Local scope | Variables assigned in a function are local; invisible outside |
| `global` | Required to assign to a global variable inside a function |
| `nonlocal` | Required to assign to an enclosing (not global) variable |
| Mutable default trap | Never use `[]`, `{}`, or `set()` as default values; use `None` |
| `*args` / `**kwargs` | Accept arbitrary positional / keyword arguments |
| Lambda | Anonymous single-expression function; use for short inline callables |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Apply the LEGB rule to predict each output.

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        return x
    return inner()

print(outer())

def broken():
    print(y)
    y = 1

y = "global y"
broken()
```

**2. (Explain.)** Run this and explain the result. It is one of the best-known traps in Python.

```python
def add(item, bucket=[]):
    bucket.append(item)
    return bucket

print(add(1))
print(add(2))
print(add(3))
```

**3. (Build.)** Write a function `make_counter()` that returns a function; each call to the returned function yields the next integer starting from 0. You will need `nonlocal` — explain what goes wrong without it.

**4. (Stretch.)** Predict both outputs and explain the difference.

```python
fs = [lambda: i for i in range(3)]
print([f() for f in fs])

gs = [lambda i=i: i for i in range(3)]
print([g() for g in gs])
```


### Answers

**1.** `enclosing`, then **`UnboundLocalError: cannot access local variable 'y' where it is not associated with a value`**.

The first is straightforward LEGB: `inner` has no local `x`, so it looks to the **E**nclosing scope, finds `outer`'s `x`, and stops before reaching the global.

The second is the one that surprises people, because there *is* a global `y` and the `print` comes *before* the assignment. It fails anyway. Python decides a variable's scope at **compile time, for the whole function body**: because `y` is assigned somewhere in `broken`, `y` is local throughout `broken` — including on the line above the assignment. The global is not shadowed at that line, it is **invisible from that function entirely**.

This is why the fix is `global y` (or, in a nested function, `nonlocal y`) rather than reordering the lines. Reordering makes the error go away but changes what the code means.

**2.** `[1]`, `[1, 2]`, `[1, 2, 3]` — the list is **shared across all calls**.

A default value is evaluated **once, when the `def` statement executes**, not once per call. That single list object is stored on the function itself (inspect it with `add.__defaults__`) and handed to every call that omits the argument. Because lists are mutable, `append` modifies the one shared object and the next caller sees the leftovers.

The fix is the standard idiom:

```python
def add(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

Now a fresh list is built on each call that needs one. Use `is None` rather than `if not bucket`, so that a caller who deliberately passes an empty list gets their list back rather than a new one.

The rule generalises: **never use a mutable object as a default** — no `[]`, `{}`, `set()`, or object instance. Immutable defaults (`0`, `""`, `None`, tuples) are safe precisely because there is nothing to mutate.

**3.**

```python
def make_counter():
    n = -1
    def next_value():
        nonlocal n
        n += 1
        return n
    return next_value

c = make_counter()
print(c(), c(), c())   # 0 1 2
d = make_counter()
print(d())             # 0 — independent state
```

Without `nonlocal`, the line `n += 1` is an assignment to `n`, so Python marks `n` as **local to `next_value`**. Reading it on the right-hand side of `+=` then fails with `UnboundLocalError` — the same mechanism as the previous exercise. `nonlocal n` declares that `n` refers to the binding in the nearest enclosing function scope, so the assignment rebinds *that* name.

Note what this gives you: `c` and `d` each capture their own `n`. The inner function plus the environment it captured is a **closure**, and it is a full substitute for a small object with one field and one method. That equivalence — closures and objects are two encodings of the same thing — is a recurring idea; PROG 101 Week 3 reaches it from the other side, building dispatch tables out of function pointers because C has no closures.

**4.** `[2, 2, 2]` then `[0, 1, 2]`.

The first is **late binding**. Each lambda captures the *variable* `i`, not its value at creation time. By the time any of them is called, the comprehension has finished and `i` holds its final value `2`, so all three see `2`. The closure captured a reference to a cell, and the cell's contents changed.

The second forces **early binding** by using a default argument. Defaults are evaluated at `def` (or `lambda`) time, so `i=i` snapshots the current value into each function's own default. This is the standard workaround, and it is why you sometimes see the otherwise-baffling `lambda x=x: ...` in real code.

The cleaner alternative is a factory that gives each closure its own scope:

```python
fs = [(lambda v: (lambda: v))(i) for i in range(3)]   # or use functools.partial
```

This bites hardest when registering callbacks in a loop — every button ends up doing what the last one was supposed to do. Recognise the symptom and you will find the cause fast.



---

## Reading

- **Guttag, Ch. 4.2–4.3** — Specifications and Scoping (primary)
- **Python Tutor:** Visualize every example in this lecture — the stack visualization is exactly what we described

---

*CS 101 · Week 3 · Lecture 11 (Thu) · © CSE Department*
