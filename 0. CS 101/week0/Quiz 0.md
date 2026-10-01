---
assessment: Quiz 0
course: CS 101
component: Quizzes
possible: 0
score:
status: ungraded
started: 2026-10-01
submitted: 2026-10-01
source: "QUIZ 0 Orientation Self Assessment.md"
---

# CS 101 · Quiz 0
## Answer Sheet

**Assessment:** `QUIZ 0 Orientation Self Assessment.md`
**Points available:** none — this is an ungraded orientation self-assessment

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Answer

#### Section A: Conceptual Questions

**A1.** In one sentence, define an **algorithm**. What three properties must it have?

An algorithm is a finite sequence of precise, step-by-step instructions that solves every instance of
a problem. It must be:

- **Finite.** It always terminates after a finite number of steps.
- **Unambiguous.** Each step has exactly one meaning, so there is nothing left to interpret.
- **Executable.** Each step can actually be carried out, by a person with pencil and paper or by a
  machine.

**A2.** What is the **Church-Turing Thesis**? What does it imply about your laptop vs. a Turing Machine?

The Church-Turing Thesis says that anything that can be computed by a mechanical, step-by-step
procedure can be computed by a Turing Machine. It is called a *thesis* because "mechanical
procedure" is an informal idea, so it cannot be proved.

What it means for my laptop: it can compute **exactly the same set of functions** as a Turing
Machine, no more and no fewer. The laptop is enormously faster and much easier to program, but it is
not more *powerful* in what it can compute. Any problem a Turing Machine cannot solve, my laptop
cannot solve either.

**A3.** Why is the **Halting Problem** significant? Give the key idea of Turing's proof.

The Halting Problem asks whether there is a program that can take any program P and input I and
decide whether P eventually halts on I. It matters because Turing proved that **no such program can
exist**. It was the first proof that some well-defined problems are *undecidable*, which puts a hard
limit on what computers can do, however fast they get.

**Key idea of the proof (proof by contradiction):** Suppose a program `HALT(P, I)` always answers
correctly. Build a new program `D(P)` that runs `HALT(P, P)` and then **does the opposite**: if
`HALT` says "P halts on itself", `D` loops forever, and if `HALT` says "loops", `D` halts. Now run
`D(D)`. If `D` halts on itself, then by its own construction it loops, and if it loops, it halts.
Both cases are contradictions, so `HALT` cannot exist.

**A4.** What is the difference between a **dynamically-typed** language and a **statically-typed** language? Name one advantage of each.

- **Dynamically typed (Python):** types belong to *values*, and they are checked while the program
  runs. A variable is just a name. `x = 5` and later `x = "five"` is allowed, and a type error such
  as `"a" + 1` only shows up when that line runs.
  **Advantage:** the code is shorter and quicker to write and change, because there are no type
  declarations, so it is good for experimenting and prototyping.
- **Statically typed (C, Java):** every variable has a declared type that the compiler checks
  **before** the program runs, so `int x` can only ever hold an int.
  **Advantage:** a whole class of bugs (type mismatches) is caught at compile time, before the code
  ever runs. The compiler can also produce faster machine code because it knows every type in
  advance.

**A5.** What is a **REPL**, and why is it a useful tool for learning programming?

REPL stands for **Read–Eval–Print Loop**. It *reads* one expression I type, *evaluates* it, *prints*
the result, and *loops* back to wait for the next one. Running `python3` with no file starts it.

It is useful for learning because the feedback is immediate: there is no file to save and no
program to run. I can test a guess ("does `int(3.9)` round?") in seconds, look at types with
`type()`, and build up an idea one expression at a time. In Lab 0, the REPL is how I found out that
`0.1 + 0.2 != 0.3` and that `-10 % 3` is `2`.

#### Section B: Python Types, Predict the Output

**B1.**

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

**Were you right?** Yes. `/` always does true division and returns a float, so the result is 10/3
rounded to the nearest float. That is why the last digit is a 5 rather than 3. `//` is floor
division, 3, and `%` is the remainder, 10 − 3 × 3 = 1.

**B2.**

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

In Python 3, `/` **always** returns a float, even for two ints and even when the division is exact
(`4 / 2` is `2.0`). `//` on two ints stays an int.

**B3.**

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

`bool` is a subtype of `int`, with `True` == 1 and `False` == 0, so arithmetic on them gives
ints: `True + False` = 1 and `True * 10` = 10. `and`, `or` and `not` are normal logic.

**B4.**

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

The first is `False` because of binary floating-point rounding (`0.1 + 0.2` is
`0.30000000000000004`). The other four are falsy values: zero, the empty string, the empty list and
`None` all count as false.

**B5.**

```python
name = "Computer Science"
print(len(name))
print(name[0])
print(name[-1])
print(name[0:8])
print(name.lower())
print("Science" in name)
```

Prediction:

```
16
C
e
Computer
computer science
True
```

Actual:

```
16
C
e
Computer
computer science
True
```

The length is 16: 8 letters + 1 space + 7 letters. Index `-1` counts from the end. The slice `[0:8]`
includes index 0 and stops *before* index 8, giving the 8 characters of `Computer`. `in` checks for
a substring.

#### Section C: Type Conversion, What Happens?

| Expression | Succeeds or Error? | Result (if success) | Type (if success) |
|---|---|---|---|
| `int(3.9)` | Succeeds | `3` (truncates toward zero, does not round) | `int` |
| `int("42")` | Succeeds | `42` | `int` |
| `int("3.9")` | **Error**: `ValueError: invalid literal for int() with base 10: '3.9'` | | |
| `int("hello")` | **Error**: `ValueError: invalid literal for int() with base 10: 'hello'` | | |
| `float(True)` | Succeeds | `1.0` | `float` |
| `str(None)` | Succeeds | `'None'` (the four-character string) | `str` |
| `bool(0.0)` | Succeeds | `False` | `bool` |
| `bool(-1)` | Succeeds | `True` (any non-zero number is truthy) | `bool` |

I checked every row in the Python 3.14.2 REPL.

#### Section D: Git Knowledge

**D1.** What is the difference between `git add` and `git commit`?

`git add` **stages** changes. It copies the current version of a file into the staging area (the
index), which is a draft of the next snapshot, and nothing is saved to history yet. `git commit`
takes everything that is staged and **saves it permanently** as a new snapshot in the history, with
an author, a date and a message. Because these are two steps, I can choose exactly which changes go
into each commit.

**D2.** What command shows you the current state of your repository?

`git status`. It lists the changes that are staged, the changes that are modified but not staged,
and the files that are untracked, and it shows which branch I am on.

**D3.** What does a good commit message look like? Give an example of a bad one and a good one.

A good message has a short subject line (about 50 characters) in the imperative mood ("Add…",
"Fix…"). It says **what** changed, specifically enough that someone reading `git log --oneline`
understands it without opening the diff. If the reason isn't obvious, a blank line follows with a
body explaining **why**.

- **Bad:** `stuff`, or `fixed it`. These don't say what changed or why.
- **Good:** `Add absolute zero conversion to temperature.py`

#### Section E: Big Picture

**E1.** Order these three fields from most theoretical to most practical.

My order (most theoretical → most practical):

```
Computer Science → Software Engineering → Computer Engineering
```

**Justification:** Computer Science asks *what can be computed and how*, and its output is
algorithms and proofs. Software Engineering applies that theory to *building reliable software
systems*. Computer Engineering builds the *physical hardware* (chips, circuits, embedded systems)
that everything runs on, so it is the most hands-on and closest to physical reality.

**E2.** Why do we study Python in CS 101 rather than teaching it as a purely theoretical course?

The ideas in CS 101 (algorithms, correctness, cost) only become real when you run them. A program is
a precise, testable statement of an algorithm: the computer won't accept a vague step, and running
it shows at once whether the idea is right and how fast it is. Python suits this because its syntax
is light and close to pseudocode, so most of my attention goes to the algorithm rather than the
language. Working programs also show things that theory alone hides. In Lab 0, for example,
`0.1 + 0.2 != 0.3` showed me that real machines have limits the mathematics doesn't.

**E3.** What is the **Von Neumann architecture**, and what is its key insight about programs and data?

The Von Neumann architecture is the design almost every computer uses. A **CPU** (with a control
unit and an arithmetic/logic unit) is connected to a **single memory**, and there is input/output.
The CPU repeats the **fetch–decode–execute** cycle: it fetches the next instruction from memory,
decodes it, executes it, and moves on to the next one.

**Key insight:** instructions and data are stored **in the same memory, in the same form**, so a
program is just another kind of data. That is what makes a computer general-purpose. Changing
what the machine does only means loading a different program, with no rewiring. It also means
programs can create, load and run other programs, which is how compilers, interpreters like
`python3` and operating systems work.

*Marks: ___ / 10*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | ___ / 10 |
| **Percent** | ___ |
| **Graded** | ___ |

**Feedback:**

