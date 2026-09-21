# CS 101 · Lecture 2
## The Python Environment & Your First Programs

**Week 0 · Lecture 2 of 3**
*"The best way to learn to program is to write programs." — Brian Kernighan*

**Date:** Thursday 24 September 2026 · 09:00–09:50 · Week 0

---

## 0. The Setup Has Meaning

Today we set up your development environment. This is not a chore before the "real" learning begins; understanding your tools is part of being an engineer. You should know what every tool does and why it exists.

---

## 1. The Tool-chain: What Each Tool Is

### Python Interpreter

Python is an **interpreted language**: meaning there is no separate compilation step. When you run `python3 my_program.py`, the Python interpreter reads your source file and executes it line by line.

Under the hood, this is not quite "line by line": Python first **compiles** your source to **bytecode** (`.pyc` files), then the **`CPython` Virtual Machine** executes that bytecode. But this happens transparently.

```
your_code.py  →  [Python Compiler]  →  bytecode (.pyc)  →  [CPython VM]  →  output
```

Compare to C (which you'll learn in PROG 101):
```
your_code.c  →  [Preprocessor]  →  [Compiler]  →  [Linker]  →  executable  →  output
```

Python trades **execution speed** for **development speed**. C runs 10–100× faster; Python code is written 3–5× faster. Neither is universally better; each fits a different use case.

### VS Code

A **text editor** with IDE features. It does not compile or run your code, it helps you **write** it. Features that matter:
- Syntax highlighting (colors help you see structure)
- IntelliSense / autocomplete (speeds up writing, catches typos)
- Integrated terminal (run code without leaving the editor)
- Git integration (version control, covered below)
- Debugging tools (essential from Week 1 onward)

### Git

A **version control system**: a tool that tracks every change you make to your code over time. Think of it as infinite undo with a timestamped history and the ability to have multiple parallel versions ("branches").

Why it matters:
- You can revert to any previous working version
- You can see exactly what changed and when
- Teams can work on the same codebase simultaneously
- Every professional software project uses it

You will use Git for every assignment in this course.

### The Terminal / Command Line

A **text interface** to your operating system. Why use it when `GUIs` exist? Because:
1. It is programmable: you can chain commands, write scripts, automate repetitive tasks
2. Many tools (Git, Python, compilers) are faster and more powerful from the command line
3. Servers have no GUI: if you ever SSH into a server, the terminal is all you have

---

## 2. Essential Terminal Commands

Before touching code, you must navigate your system from the terminal.

```bash
# Navigation
pwd             # Print Working Directory — where am I right now?
ls              # List files in current directory
ls -la          # List all files (including hidden), with details
cd foldername   # Change Directory — move into a folder
cd ..           # Move up one level (to parent directory)
cd ~            # Go to home directory

# File operations
mkdir cs101     # Make a directory called "cs101"
touch file.py   # Create an empty file called "file.py"
cp a.py b.py    # Copy a.py to b.py
mv a.py b.py    # Move (rename) a.py to b.py
rm file.py      # Remove (delete) a file — WARNING: this is permanent, no trash

# Viewing files
cat file.py     # Print entire file to terminal
less file.py    # View file page by page (q to quit)
head -n 5 file.py   # View first 5 lines
tail -n 5 file.py   # View last 5 lines

# Running Python
python3 my_program.py       # Run a Python file
python3 --version           # Check Python version
python3                     # Open the interactive REPL (Ctrl+D or exit() to quit)
```

---

## 3. The REPL: Your Most Important Learning Tool

**REPL** stands for **Read-Eval-Print Loop**:
- **Read**: reads what you type
- **Eval**: evaluates (computes) it
- **Print**: prints the result
- **Loop**: goes back to waiting for more input

Open your terminal and type `python3`. You'll see:
```
Python 3.12.0 (...)
>>> 
```

The `>>>` is the REPL prompt. Try these:

```python
>>> 2 + 2
4
>>> "hello" + " " + "world"
'hello world'
>>> 10 / 3
3.3333333333333335
>>> 10 // 3
3
>>> 10 % 3
1
>>> 2 ** 10
1024
```

**The REPL is your laboratory.** Any time you want to test an idea, check how something works, or experiment, open the REPL. Professional Python programmers use it constantly. Never be afraid to type something and see what happens.

---

## 4. Your First Python Program

Create a file called `hello.py`:

```python
# hello.py
# My first Python program
# CS 101, Week 0

print("Hello, World!")
print("I am learning Computer Science.")
print("Today's date:", "Week 0")
```

Run it: `python3 hello.py`

Expected output:
```
Hello, World!
I am learning Computer Science.
Today's date: Week 0
```

### What is `print()`?

`print()` is a **function** — a reusable unit of code that does something (in this case: displays text to the screen). Functions are called by writing their name followed by parentheses containing **arguments** (inputs).

We will study functions deeply in Week 3. For now, know that `print()` sends output to **standard output** (stdout) — the terminal by default.

---

## 5. Python as a Calculator: Going Deeper

```python
# Arithmetic operators
>>> 17 + 4       # Addition          → 21
>>> 17 - 4       # Subtraction       → 13
>>> 17 * 4       # Multiplication    → 68
>>> 17 / 4       # Division          → 4.25  (always float in Python 3)
>>> 17 // 4      # Floor division    → 4     (integer division, rounds down)
>>> 17 % 4       # Modulo (remainder)→ 1
>>> 2 ** 8       # Exponentiation    → 256

# Order of operations — same as mathematics
>>> 2 + 3 * 4    → 14   (multiplication before addition)
>>> (2 + 3) * 4  → 20   (parentheses override)
```

**The modulo operator `%` is more important than it looks.** It answers the question "what is the remainder when I divide X by Y?" This is used constantly in CS:
- Checking if a number is even: `n % 2 == 0`
- Wrapping around (clock arithmetic): `hour = (hour + 1) % 24`
- Cryptography: `(a * b) % n` is the heart of RSA encryption

---

## 6. Variables: Labels on Objects

```python
x = 42
name = "Alice"
is_enrolled = True
gpa = 3.75
```

In Python, `x = 42` does **not** mean "x is a box containing 42." It means:
1. Create an integer object with value 42 somewhere in memory
2. Attach the label `x` to that object

This distinction matters:

```python
x = [1, 2, 3]   # x labels a list object
y = x            # y labels THE SAME list object (not a copy!)
y.append(4)
print(x)         # → [1, 2, 3, 4]  ← x changed! Because x and y point to the same object
```

We'll explore this deeply when we study data structures. For now: **variables are labels, not boxes.**

**Naming rules:**
- Must start with a letter or underscore (`_`)
- Can contain letters, digits, underscores
- Case-sensitive: `Name` and `name` are different variables
- Cannot use Python keywords: `if`, `else`, `while`, `for`, `def`, etc.

**Naming conventions (follow these):**
```python
# Good — snake_case for variables and functions
student_count = 30
average_grade = 87.5

# Bad — hard to read
studentcount = 30
AverageGrade = 87.5   # Reserved for class names

# Constants — ALL_CAPS by convention
MAX_STUDENTS = 50
PI = 3.14159
```

---

## 7. Comments: Code for Humans

```python
# This is a single-line comment
# The interpreter ignores everything after #

x = 42  # This is an inline comment — useful for brief notes

"""
This is a multi-line string.
When used at the top of a file or function (a "docstring"),
it documents what the file/function does.
It is not technically a comment, but is used like one.
"""

def some_function():
    """This function does nothing yet. This is its docstring."""
    pass
```

**Rule:** Comments should explain **why**, not **what**. The code itself shows what: a well-written comment explains the reasoning behind it.

```python
# Bad comment — just restates the code
x = x + 1  # add 1 to x

# Good comment — explains the reason
x = x + 1  # account for 0-indexing: convert from 1-based user input to 0-based array index
```

---

## 8. Introduction to Git: Version Control

### Why Git?

Imagine working on an essay for 6 hours and then accidentally deleting half of it. Without version control: it's gone. With Git: you restore the last saved version in 5 seconds.

Now imagine 10 people editing the same codebase simultaneously. Without version control: chaos. With Git: each person works independently, and changes are merged systematically.

### Basic Git Workflow

```bash
# 1. Set up once (your identity)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# 2. Create a new repository (once per project)
git init my-cs101-repo
cd my-cs101-repo

# 3. The daily workflow:

# See what has changed since your last save
git status

# Stage a file (prepare it for saving)
git add hello.py
git add .           # Stage ALL changed files

# Commit (save a snapshot with a message)
git commit -m "Add hello world program"

# See the history of commits
git log
git log --oneline   # Compact view
```

**The three areas of Git:**
```
Working Directory  →  git add  →  Staging Area  →  git commit  →  Repository
(files you edit)                  (changes you                    (permanent
                                   plan to save)                   history)
```

**Commit messages: write them well:**
```bash
# Bad
git commit -m "stuff"
git commit -m "fix"

# Good
git commit -m "Add binary search function with O(log n) analysis"
git commit -m "Fix off-by-one error in loop termination condition"
```

---

## 9. Understanding Python's Type System

Python is **dynamically typed**: variables can hold any type, and types are checked at runtime, not before the program runs.

```python
x = 42         # x is an int
x = "hello"    # now x is a str — Python allows this
x = [1, 2, 3]  # now x is a list — Python allows this
```

Compare to C (statically typed):
```c
int x = 42;
x = "hello";   // COMPILER ERROR — x must always be an int
```

**Why does this matter?**
- Dynamic typing: faster to write, easier to experiment with, but bugs can hide until runtime
- Static typing: slower to write, but entire classes of bugs (type errors) are caught before the program runs

This trade-off runs throughout programming language design. We will study it in depth in CS 211 (Programming Languages, Year 2).

**Checking types in Python:**
```python
>>> type(42)
<class 'int'>
>>> type(3.14)
<class 'float'>
>>> type("hello")
<class 'str'>
>>> type(True)
<class 'bool'>
>>> type([1, 2, 3])
<class 'list'>
>>> isinstance(42, int)
True
>>> isinstance(42, str)
False
```

---

## 10. Summary

| Tool               | Purpose                                            |
| ------------------ | -------------------------------------------------- |
| Python Interpreter | Executes Python source code                        |
| VS Code            | Text editor with IDE features                      |
| Terminal           | Text interface to the operating system             |
| Git                | Version control: tracks changes over time          |
| REPL               | Interactive Python environment for experimentation |

| Concept | Key Point |
|---------|-----------|
| Variable | A label pointing to an object in memory |
| Comment | Human-readable explanation; ignored by interpreter |
| Dynamic Typing | Variable types checked at runtime, not compile time |
| Modulo `%` | Remainder after division; extremely widely used |

---

## What's Next

**Lecture 3 (L03):** [[L03 Values Types and Expressions]]
**Lab 0 (Tue):** [[LAB 0 Environment Setup]]


---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** You type the following into the REPL, one line at a time. Write down exactly what the REPL displays after each — remembering that displaying nothing is a legitimate answer.

```python
>>> 3 + 4
>>> x = 3 + 4
>>> x
>>> print(x)
>>> y = print(x)
>>> y
```

**2. (Explain.)** Running `python3 hello.py` and pasting the same file's contents into the REPL can produce different visible output, even though every statement executes identically. Explain the mechanism, and say which of the two is a better model of what your program "really does".

**3. (Build.)** You have made three separate edits to `hello.py` and want each recorded as its own commit, but you have run no git commands at all yet and the directory is not a repository. Write the exact sequence of commands, starting from `cd` into the directory. Then explain what `git add` does that `git commit` does not.

**4. (Stretch.)** §6 describes variables as labels attached to objects rather than boxes containing values. Predict what the following prints, then explain which mental model each line rewards.

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)

c = 10
d = c
d += 1
print(c)
```


### Answers

**1.** `7` — the REPL echoes the value of any expression.

*(nothing)* — assignment is a **statement**, not an expression, so there is no value to echo.

`7` — a bare name is an expression.

`7` — printed by `print`, not echoed.

`7` — `print` still runs and outputs, but its *return* value is `None`, which the REPL suppresses.

*(nothing)* — `y` is `None`, and the REPL deliberately does not echo `None`. This last line is the one that catches people: the value is there, but the REPL hides it. Type `repr(y)` and you will see `'None'` appear.

**2.** The REPL echoes the value of every top-level expression statement; a script discards them silently. So a file containing the bare line `2 + 2` prints nothing when run and prints `4` when pasted. The **script** is the truthful model — the echo is a convenience of the interactive shell, not part of Python's execution semantics. This is why relying on the echo while developing and then wondering why the finished program "stopped printing" is such a common early bug: nothing stopped, the echo was never yours to begin with.

**3.**

```bash
cd path/to/project
git init
git add hello.py
git commit -m "Add greeting"
# ...second edit...
git add hello.py
git commit -m "Handle empty name"
# ...third edit...
git add hello.py
git commit -m "Add usage message"
```

`git add` copies the current contents of the file into the **staging area** (the index) — it selects *what* will go into the next commit. `git commit` takes whatever is staged and writes it to history as an immutable snapshot. The separation is what lets you commit some of your changes and not others. A consequence worth internalising: editing a file *after* `git add` but *before* `git commit` commits the older, staged version, not what is on disk.

**4.** `[1, 2, 3, 4]` then `10`.

Under the box model these look inconsistent — why did changing `b` affect `a` but changing `d` not affect `c`? Under the label model they are the same rule applied twice. `b = a` attaches a second label to one list object; `b.append(4)` **mutates that object**, and `a` labels the same object, so `a` sees it. `d += 1` on an integer cannot mutate it, because integers are immutable — it computes a new object `11` and rebinds only the label `d`. The label `c` is untouched.

The rule is: **mutation is visible through every label; rebinding is visible through one.** Everything confusing about Python's assignment semantics follows from that sentence, and L04 §6 makes it formal.



---

*CS 101 · Week 0 · Lecture 2 · © CSE Department*
