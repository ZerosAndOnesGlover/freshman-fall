# CS 101 · Week 3: Functions, Scope, and the Call Stack

---

## Contents

```
CS101_Week3/
│
├── README.md                                    ← You are here
│
├── lectures/
│   ├── L10 Functions and Encapsulation.md       ← Wed: why functions, anatomy,
│   │                                                 parameters vs arguments, return,
│   │                                                 encapsulation, composition,
│   │                                                 specifications, assert, first-class
│   ├── L11 Scope and Call Stack.md              ← Thu: namespaces, LEGB rule,
│   │                                                 call stack mechanics, frame diagrams,
│   │                                                 global/nonlocal, defaults, *args/**kwargs
│   └── L12 Function Design and Recursion Preview.md     ← Fri: decomposition, SRP, pure functions,
│                                                      testing, recursion preview, helpers,
│                                                      keyword args, mortgage refactor
│
├── lab/
│   ├── LAB 3 Stack Frames and Functions.md       ← Tue 20 Oct (W4): Python Tutor visualization,
│   │                                                 scope bug hunt, text analysis library,
│   │                                                 recursion intro
│   └── starter_text_statistics.py               ← Lab starter with TODOs + full test suite
│
├── assignments/
│   ├── QUIZ 3 Week 3 Wednesday.md                    ← In-class quiz (covers Week 2)
│   ├── PS 3 Functions and Scope.md               ← Problem Set 3 (due Fri 23 Oct, 17:00)
│   └── ps3_starter.py                           ← Scaffold: signatures and docstring TODOs
│
├── resources/
│   └── Reading Guide Week 3.md                   ← 3 REPL sessions, concept map,
│                                                     mistake list, self-test, Week 4 preview
│
└── solutions_instructor/
    └── LAB 3 Solutions.md                        ← Expected answers and marking notes
```

---

## Week 3 at a Glance

**Theme:** Functions are the most important abstraction in programming. This week teaches not just how to write them, but how to *design* them — and what Python does with them mechanically at the level of the call stack.

| Day | Event | Topic |
|-----|-------|-------|
| Wed 14 Oct | Lecture 10 + Quiz 3 | Why functions; anatomy; return vs print; composition; specifications |
| Thu 15 Oct | Lecture 11 | Namespaces; LEGB; call stack; frames; global; mutable default trap; `*args`/`**kwargs` |
| Fri 16 Oct | Lecture 12 + PS3 released | Function design; SRP; pure functions; testing; recursion preview |
| Tue 20 Oct (W4) | Lab 3 (graded) | Python Tutor stack frames, scope bugs, text statistics, recursion first look |

---

## Your To-Do List

### Before Wednesday
- [ ] Read Guttag Ch. 4.1 (functions and scoping)
- [ ] Review your Week 2 answers — Quiz 3 covers Week 2 material
- [ ] Watch "Python Names and Values" (Ned Batchelder) if you haven't already

### Wednesday
- [ ] Quiz 3 (10 min — covers Week 2 control flow)
- [ ] Notes for L10

### Before Thursday
- [ ] REPL Session A from Reading Guide (call stack)
- [ ] Read Guttag Ch. 4.2 (specifications)
- [ ] Visualize at least 3 function calls in Python Tutor

### Thursday
- [ ] Notes for L11
- [ ] REPL Session B (scope edge cases)

### Tuesday 20 October Lab, Week 4 (Required, Graded)
- [ ] Python Tutor exercises 1.1–1.5 with written answers
- [ ] All 4 scope cases explained; the 3 bugs fixed
- [ ] `text_statistics.py` — all functions implemented, all tests passing
- [ ] `recursion_intro.py` — `power` and `sum_digits` implemented
- [ ] TA checkoff

### Friday
- [ ] Notes for L12
- [ ] REPL Session C (function design patterns)
- [ ] Read PS3 completely tonight

### Weekend
- [ ] Start PS3 — at minimum B1 (math library) and B5 (recursion)
- [ ] Read Guttag Ch. 4.3 (recursion preview)
- [ ] Visualize `factorial(5)` in Python Tutor — count the frames

---

## The Central Ideas of Week 3

**1. A function is a named abstraction.**
The caller knows *what* it does. The implementation knows *how*. This separation is the foundation of managing complexity at scale.

**2. Every function call creates a stack frame.**
The frame holds local variables and the return address. It is pushed on call and popped on return. This is why local variables don't leak between functions — they live in separate frames.

**3. Python resolves names using LEGB.**
Local → Enclosing → Global → Built-in. First match wins. If not found anywhere: `NameError`.

**4. The mutable default argument trap is one of Python's most notorious bugs.**
`def f(x, lst=[])` evaluates `[]` once at definition time. Use `def f(x, lst=None): if lst is None: lst = []` instead.

**5. `return` sends a value back. `print` is a side effect.**
Only functions that `return` values can be composed in expressions. Functions that only `print` return `None` — you cannot use them to build larger computations.

**6. Pure functions — no side effects, same output for same input — compose freely.**
They are independently testable, predictable, and parallelizable. Isolate side effects in a small number of clearly-marked functions.

**7. Decompose into single-responsibility functions.**
If your docstring says "and", the function probably does too much.

**8. Recursion is function calls — all the way down.**
A recursive function calls itself. The call stack grows with each call and unwinds as base cases return. We'll make this rigorous in Week 4.

---

## Quick Self-Check

Without notes:

1. A function definition has no `return` statement. What does it return when called?
2. What is the difference between a parameter and an argument?
3. You write `x = 5` inside a function. Does this change the global `x`? Why or why not?
4. What does `global x` do inside a function?
5. Why is `def f(lst=[])` dangerous? Write the correct version.
6. You call `result = print("hello")`. What is `result`?
7. What does LEGB stand for?
8. At what point during execution is a default parameter value evaluated?
9. Write a `compose(f, g)` function: `compose(f, g)(x)` should return `f(g(x))`.
10. `factorial(5)` calls `factorial(4)` which calls `factorial(3)` ... which calls `factorial(0)`. How many stack frames are on the stack at the deepest point?

*(Answers: None, names vs values at call site, no (new local x), declares assignment refers to global, evaluated once at def time so all calls share it, None, Local/Enclosing/Global/Built-in, at def statement execution, `lambda x: f(g(x))`, 6 frames)*

---

## Algorithms and Patterns Introduced This Week

| Pattern | Description | Example |
|---------|-------------|---------|
| Accumulator function | Pure function that builds result from inputs | `sum_of_squares(lst)` |
| Guard clause | Early return for invalid inputs | `if n < 0: return None` |
| Composition chain | Each function calls the simpler one below | `normalize → lerp → clamp` |
| Function factory | Function that returns a function (closure) | `make_counter()` |
| Helper function | `_prefixed` function that supports a public function | `_tokenize()` |
| Memoization | Cache results to avoid recomputation | `memoize(func)` |
| Recursive base+step | Base case stops recursion; recursive case reduces | `factorial(n) = n * factorial(n-1)` |

---

*CS 101 · Week 3 · © CSE Department*
