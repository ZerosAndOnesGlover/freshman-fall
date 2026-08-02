# CS 101 Week 3 Reading Guide & Resources
## Functions, Scope, and the Call Stack

---

## Required Reading

### Guttag — Introduction to Computation and Programming Using Python

**Chapter 4: Functions, Scoping, and Abstraction**
- §4.1 Functions and Scoping
- §4.2 Specifications
- §4.3 Recursion (preview — we cover this fully in Week 4)
- §4.4 Global Variables
- §4.5 Modules

**What to focus on in Chapter 4:**
- The distinction between parameters and arguments
- How Python decides which namespace to look up a name in (LEGB)
- What a specification (docstring) must contain
- Why `global` should be avoided in favor of return values and parameters

---

## Focused REPL Sessions

### Session A: The Call Stack (20 min)

Open Python Tutor alongside these exercises. Run each example in Python Tutor, step through it completely, then verify your understanding in the REPL.

```python
# 1. How many frames deep does this go?
def f():
    return g()
def g():
    return h()
def h():
    return 42

result = f()
# Step through in Python Tutor: count frames at the deepest point.

# 2. Local variables are truly local:
def set_x():
    x = 999

x = 1
set_x()
print(x)    # Predict: 1 or 999?

# 3. The return value chain:
def double(n):
    return n * 2

def quadruple(n):
    return double(double(n))

def octuple(n):
    return double(quadruple(n))

print(octuple(3))   # Predict without running

# 4. The mutable default trap — confirm it:
def add_item(x, lst=[]):
    lst.append(x)
    return lst

r1 = add_item(1)
r2 = add_item(2)    # Is r2 [2] or [1, 2]?
print(r1 is r2)     # Same object?
print(id(r1), id(r2))
```

### Session B: Scope Edge Cases (15 min)

Predict each output, then verify. If you're wrong, understand why before moving on.

```python
# Case 1: Does a function see the global value at call time or definition time?
x = "original"
def show_x():
    print(x)

show_x()      # "original"
x = "changed"
show_x()      # "original" or "changed"?

# Case 2: Can you read a global list inside a function?
items = [1, 2, 3]
def append_four():
    items.append(4)   # No 'global' needed — why?

append_four()
print(items)

# Case 3: What about assigning to a global?
counter = 0
def increment():
    counter = counter + 1   # What error?

try:
    increment()
except UnboundLocalError as e:
    print(f"Error: {e}")
# Fix it with 'global counter' or by passing counter as argument

# Case 4: Nested functions — closure
def make_greeting(salutation):
    def greet(name):
        return f"{salutation}, {name}!"
    return greet

hello = make_greeting("Hello")
hi    = make_greeting("Hi")
print(hello("Alice"))   # ?
print(hi("Bob"))        # ?
# Note: hello and hi are DIFFERENT functions with DIFFERENT salutations
```

### Session C: Function Design Patterns (15 min)

```python
# Pattern 1: Compose pure functions
import math

def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def midpoint(x1, y1, x2, y2):
    return (x1+x2)/2, (y1+y2)/2

# Use both:
p1 = (0, 0)
p2 = (3, 4)
print(distance(*p1, *p2))     # 5.0
print(midpoint(*p1, *p2))     # (1.5, 2.0)

# Pattern 2: Default None for mutable defaults
def build_list(items, result=None):
    if result is None:
        result = []
    for item in items:
        result.append(item)
    return result

r1 = build_list([1, 2, 3])
r2 = build_list([4, 5, 6])
print(r1)   # [1, 2, 3]
print(r2)   # [4, 5, 6] — separate lists!

# Pattern 3: Higher-order functions
def apply_twice(f, x):
    return f(f(x))

apply_twice(lambda x: x + 1, 5)   # 7
apply_twice(str.upper, "hello")   # Error or "HELLO"? Why?
apply_twice(lambda s: s + "!", "wow")  # "wow!!"

# Pattern 4: Functions returning functions
def make_power(n):
    return lambda x: x ** n

square = make_power(2)
cube   = make_power(3)
print(square(4), cube(3))   # 16, 27
```

---

## Conceptual Exercises (Paper)

Work these without Python. Verify afterward.

**Exercise 1:** Trace the full call stack for this program. Draw each frame.

```python
def sum_to(n):
    if n == 0:
        return 0
    return n + sum_to(n - 1)

result = sum_to(4)
```

At the deepest point: how many frames are on the stack? What is in each frame?

**Exercise 2:** Identify every scope bug in this code:

```python
total = 0
items = []

def process(x):
    total += x           # Bug A
    items.append(x)      # Bug B? Or not?
    result = total / len(items)  # Bug C?
    return result

process(10)
process(20)
```

Which lines raise errors? Which work fine? Explain each using LEGB.

**Exercise 3:** The mutable default trap has a pattern to fix it. Explain why this fix works:

```python
# Broken:
def f(x, lst=[]):
    lst.append(x)
    return lst

# Fixed:
def g(x, lst=None):
    if lst is None:
        lst = []
    lst.append(x)
    return lst
```

Specifically: at what point in execution is `[]` created in the broken version? At what point is it created in the fixed version? What does this tell you about when default values are evaluated?

---

## Key Concepts Map

```
FUNCTIONS
│
├── Definition components
│   ├── Parameters — names in the def
│   ├── Arguments  — values at the call site
│   ├── Body       — indented statements
│   ├── Return     — value sent back; None if absent
│   └── Docstring  — contract: inputs, outputs, examples
│
├── Execution model
│   ├── Call → push new stack frame
│   │         → bind parameters in new frame
│   │         → execute body
│   ├── Return → pop frame → return value to caller
│   └── Stack overflow → too many nested calls
│
├── Scope (LEGB)
│   ├── Local     — names assigned in current function
│   ├── Enclosing — names in enclosing functions (closures)
│   ├── Global    — names at module top level
│   └── Built-in  — print, len, int, range, ...
│
├── Gotchas
│   ├── Mutable default — use None sentinel instead of []/{}/set()
│   ├── global keyword  — needed to ASSIGN to global, not to read
│   ├── UnboundLocalError — assigned in function → treated as local
│   └── Side effect vs return — print() ≠ return; only return composes
│
└── Design principles
    ├── Single responsibility — one function, one thing
    ├── Pure functions       — no side effects; compose freely
    ├── Guard clauses        — early return for invalid cases
    ├── Decomposition        — name sub-computations
    └── Specification        — docstring is a contract
```

---

## Common Mistakes This Week

**Mistake 1: Print instead of return**
```python
def square(x):
    print(x * x)    # WRONG for computation

y = square(5) + 1   # TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
```

**Mistake 2: Mutable default argument**
```python
def add(item, lst=[]):   # WRONG
    lst.append(item)
    return lst

def add(item, lst=None): # Correct
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

**Mistake 3: UnboundLocalError from assigning to a global**
```python
x = 10
def f():
    x += 1      # UnboundLocalError — Python sees assignment, makes x local
    return x

def g():
    global x    # Correct — but usually better to use parameters/return
    x += 1
    return x
```

**Mistake 4: Forgetting that functions are objects**
```python
# No parentheses = the function object itself
# Parentheses = calling the function
print(len)       # <built-in function len>
print(len([]))   # 0

f = print        # f is now the print function
f("hello")       # same as print("hello")
```

**Mistake 5: Modifying a parameter and expecting the caller to see it (for immutables)**
```python
def add_one(x):
    x = x + 1    # creates a new int; does NOT change the caller's variable
    return x

n = 5
add_one(n)
print(n)    # still 5 — integers are immutable

# Contrast with mutables:
def append_one(lst):
    lst.append(1)   # modifies the list in place — caller DOES see this

items = [1, 2, 3]
append_one(items)
print(items)    # [1, 2, 3, 1] — list was modified
```

---

## Week 3 Self-Test

Can you answer all of these without notes?

1. What is the difference between a parameter and an argument?
2. What does a function return if it has no `return` statement?
3. What does LEGB stand for? What does it determine?
4. Why is `def f(x, lst=[])` dangerous? How do you fix it?
5. What is a `global` statement and when do you need it?
6. What is a "pure function"? Give an example of one and of one that isn't.
7. What is a "closure"? Write a 3-line example.
8. What error does `f(x, x, x)` raise if `f` is defined as `def f(a, b)`?
9. Write a `compose(f, g)` function in one line using a lambda.
10. What is the maximum recursion depth in Python by default? What error does exceeding it raise?

---

## Preview: Week 4

Week 4 covers **recursion** in full depth. After this week's recursion preview, you already know the basic idea. Week 4 goes further:

- Mathematical induction as the formal foundation
- Recursion trees and how to draw them
- Tail recursion and why Python doesn't optimize it
- Classic recursive algorithms: Tower of Hanoi, merge sort (preview), binary search
- The three laws of recursion

Before Wednesday, make sure you can implement `factorial` and `gcd` recursively and explain — using the stack — why they terminate.

---

*CS 101 · Week 3 · Reading Guide · © CSE Department*
