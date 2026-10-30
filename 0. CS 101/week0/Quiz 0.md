---
assessment: Quiz 0
course: CS 101
component: Quizzes
possible: 0
score:
status: ungraded
started: 2026-10-30
submitted: 2026-10-30
source: "QUIZ 0 Orientation Self Assessment.md"
---

# CS 101 · Quiz 0
## Answer Sheet

**Assessment:** `QUIZ 0 Orientation Self Assessment.md`
**Points available:** none — this is an ungraded orientation self-assessment

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

## Section A: Conceptual Questions

### A1

**Your answer:**

An **algorithm** is a finite, unambiguous, executable sequence of instructions that takes input and
produces a defined output for every instance of a class of problems. The six properties (L01 §4) are:

- **Finite** — it terminates after a finite number of steps.
- **Unambiguous** — every step has exactly one interpretation.
- **Executable** — every step can actually be carried out.
- **Input** — it accepts valid input data.
- **Output** — it produces a defined result.
- **Class of problems** — it works for all valid inputs, not just the examples.

---

### A2

**Your answer:**

The **Church–Turing Thesis** states that any computation that can be carried out by a mechanical,
step-by-step process can also be carried out by a Turing Machine. It is a thesis rather than a
theorem, because "mechanical process" is an informal notion that cannot be proved about.

It implies that my laptop and a Turing Machine can compute **exactly the same set of functions**:
the laptop can simulate a Turing Machine for as long as its memory lasts, and a Turing Machine can simulate the laptop. The laptop is vastly faster and easier to program, but it is not more
*powerful*. Any problem no Turing Machine can solve, my laptop cannot solve either.

---

### A3

**Your answer:**

The **Halting Problem** asks whether a program can take any program P and input I and decide, in
finite time, whether P eventually halts on I. It is significant because Turing proved that **no such
program can exist**: it was the first proof that a well-defined problem is *undecidable*, which puts
a hard limit on what any computer can do, however fast it becomes.

**Key idea of the proof (contradiction):** suppose a program `HALT(P, I)` always answers correctly.
Build `D(P)` that calls `HALT(P, P)` and then does the opposite — if `HALT` says "halts", `D` loops
forever; if `HALT` says "loops", `D` halts. Now ask what `D(D)` does. If it halts, `HALT(D, D)` said
it loops; if it loops, `HALT` said it halts. Either way `HALT` was wrong, so `HALT` cannot exist.

---

### A4

**Your answer:**

A **dynamically-typed** language such as Python attaches types to *values* and checks them while the program runs. A variable is only a name, so `x = 5` followed by `x = "five"` is allowed, and a type error such as `"a" + 1` appears only when that line executes. **Advantage:** code is shorter and
faster to write and change, which suits experimenting and prototyping.

A **statically-typed** language such as C or Java gives every variable a declared type that the
compiler checks **before** the program runs, so `int x` can only ever hold an int. **Advantage:** a
whole class of type-mismatch bugs is caught at compile time, before the code runs, and the compiler can generate faster machine code because it knows every type in advance.

---

### A5

**Your answer:**

A **REPL** is a **Read–Eval–Print Loop**: it *reads* one expression, *evaluates* it, *prints* the
result, and *loops* back for the next one. Running `python3` with no file starts it.

It is useful for learning because feedback is immediate — there is no file to save and no program to run. I can test a guess in seconds, inspect values with `type()`, and build an idea one expression at a time. In Lab 0 the REPL is how I discovered that `0.1 + 0.2 != 0.3`, that `-10 % 3` is `2`, and
that `int("3.9")` raises `ValueError`.

---

## Section B: Python Types — Predict the Output

### B1

**Your answer:**

```python
x = 10
y = 3
print(x / y)
print(x // y)
print(x % y)
```

Prediction:

```
3.3333333333333335
3
1
```

Actual output:

```
3.3333333333333335
3
1
```

**Was I right?** Yes. `/` always performs true division and returns a float, so `10 / 3` is the nearest float to 3.333…, which prints as `3.3333333333333335`. `//` floors to `3`, and `%` gives the
remainder `10 - 3 × 3 = 1`.

---

### B2

**Your answer:**

```python
print(type(5))
print(type(5.0))
print(type(5 / 2))
print(type(5 // 2))
```

Prediction:

```
<class 'int'>
<class 'float'>
<class 'float'>
<class 'int'>
```

Actual:

```
<class 'int'>
<class 'float'>
<class 'float'>
<class 'int'>
```

`/` **always** returns a float in Python 3, even when the division is exact (`4 / 2` is `2.0`), while
`//` on two ints stays an int.

---

### B3

**Your answer:**

```python
a = True
b = False
print(a + b)
print(a * 10)
print(a and b)
print(a or b)
print(not a)
```

Prediction:

```
1
10
False
True
False
```

Actual:

```
1
10
False
True
False
```

`bool` is a subtype of `int`, with `True == 1` and `False == 0`, so arithmetic on booleans produces `int`s: `True + False` is `1` and `True * 10` is `10`. `and`, `or` and `not` behave as ordinary logic.

---

### B4

**Your answer:**

```python
print(0.1 + 0.2 == 0.3)
print(bool(0))
print(bool(""))
print(bool([]))
print(bool(None))
```

Prediction:

```
False
False
False
False
False
```

Actual:

```
False
False
False
False
False
```

The first is `False` because of binary floating-point rounding: `0.1 + 0.2` is `0.30000000000000004`, a different float from the one nearest `0.3`. The other four are the falsy
values: zero, the empty string, the empty list and `None`.

---

### B5

**Your answer:**

```python
name = "Computer Science"
print(len(name))
print(name[0])
print(name[-1])
print(name[0:8])
print(name.lower())
print(name[9:])
```

Prediction:

```
16
C
e
Computer
computer science
Science
```

Actual:

```
16
C
e
Computer
computer science
Science
```

The length is 16: 8 letters + 1 space + 7 letters. `name[-1]` counts from the end. The slice `[0:8]`
includes index 0 and stops **before** index 8, giving `Computer`. Index 8 is the space, so `[9:]`
starts at `S` and gives `Science`.

---

## Section C: Type Conversion — What Happens?

### C1

**Your answer:**

| Expression | Succeeds or Error? | Result (if success) | Type (if success) |
|---|---|---|---|
| `int(3.9)` | Succeeds | `3` (truncates toward zero, does not round) | `int` |
| `int("42")` | Succeeds | `42` | `int` |
| `int("3.9")` | **Error:** `ValueError: invalid literal for int() with base 10: '3.9'` | — | — |
| `int("hello")` | **Error:** `ValueError: invalid literal for int() with base 10: 'hello'` | — | — |
| `float(True)` | Succeeds | `1.0` | `float` |
| `str(None)` | Succeeds | `'None'` (the four-character string) | `str` |
| `bool(0.0)` | Succeeds | `False` | `bool` |
| `bool(-1)` | Succeeds | `True` (any non-zero number is truthy) | `bool` |

I checked every row in the Python 3.14.2 REPL. Note that `int("3.9")` fails because converting a
string is parsing, not numeric truncation; `int(float("3.9"))` succeeds and gives `3`.

---

### C2

**Your answer:**

`int("42")` **succeeds** → `42`, type `int`. The text is a valid base-10 integer literal.

---

### C3

**Your answer:**

`int("3.9")` **raises** `ValueError: invalid literal for int() with base 10: '3.9'`. Converting a string is parsing, and `"3.9"` is not an integer literal. `int(float("3.9"))` succeeds and gives `3`.

---

### C4

**Your answer:**

`int("hello")` **raises** `ValueError: invalid literal for int() with base 10: 'hello'`. The text is not a number at all.

---

### C5

**Your answer:**

`float(True)` **succeeds** → `1.0`, type `float`. `bool` is a subtype of `int`, so `True` converts as
`1`.

---

### C6

**Your answer:**

`str(None)` **succeeds** → `'None'`, type `str`. This is the four-character string, not the value
`None`.

---

### C7

**Your answer:**

`bool(0.0)` **succeeds** → `False`, type `bool`. Zero is falsy whatever its numeric type.

---

### C8

**Your answer:**

`bool(-1)` **succeeds** → `True`, type `bool`. Any non-zero number, negative or positive, is truthy.

---

## Section D: Git Knowledge

### D1

**Your answer:**

`git add` **stages** changes: it copies the current version of a file into the staging area (the
index), which is a draft of the next snapshot, but nothing is saved to history yet. `git commit`
takes everything staged and **saves it permanently** as a new snapshot in the history, with an
author, a date and a message. Keeping the two steps separate lets me choose exactly which changes go into each commit.

---

### D2

**Your answer:**

`git status`. It shows the staged changes, the modified-but-unstaged changes, the untracked files, and the current branch.

---

### D3

**Your answer:**

A good commit message has a short subject line (about 50 characters) in the imperative mood ("Add…", "Fix…"). It says **what** changed specifically enough to understand from `git log --oneline` alone; if the reason is not obvious, a blank line and a body explain **why**.

- **Bad:** `stuff` or `fixed it` — neither says what changed or why.
- **Good:** `Add absolute zero conversion to temperature.py`

---

## Section E: Big Picture

### E1

**Your answer:**

Order (most theoretical → most practical):

```
Computer Science → Software Engineering → Computer Engineering
```

Computer Science asks *what can be computed and how*, and its output is algorithms and proofs.
Software Engineering applies that theory to building reliable software systems. Computer Engineering builds the physical hardware — chips, circuits and embedded systems — that everything runs on, so it is the most hands-on and closest to physical reality.

---

### E2

**Your answer:**

The ideas of CS 101 — algorithms, correctness and cost — only become concrete when they are run. A program is a precise, testable statement of an algorithm: the computer will not accept a vague step, and running it shows immediately whether the idea is right and how fast it is. Python suits this because its syntax is light and close to `pseudocode`, so most attention goes to the algorithm rather than the language. Working programs also reveal things theory alone hides: in Lab 0, for example, `0.1 + 0.2 != 0.3` showed that real machines have limits the mathematics does not.

---

### E3

**Your answer:**

The **Von Neumann architecture** is the design almost every computer uses: a **CPU** (control unit and arithmetic/logic unit) connected to a **single memory**, with input/output. The CPU repeats the **fetch–decode–execute** cycle — fetch the next instruction from memory, decode it, execute it, then
move on.

**Key insight:** instructions and data are stored **in the same memory, in the same form**, so a program is just another kind of data. That is what makes a computer general-purpose: changing what the machine does only means loading a different program, with no rewiring. It also means programs
can create, load and run other programs, which is how compilers, interpreters such as `python3`, and operating systems work.

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | ___ / 10 |
| **Percent** | ___ |
| **Graded** | ___ |

**Feedback:**
