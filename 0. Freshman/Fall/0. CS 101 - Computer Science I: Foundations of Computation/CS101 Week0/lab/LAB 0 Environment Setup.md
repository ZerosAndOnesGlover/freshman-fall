# CS 101 · Lab 0
## Environment Setup & First Programs

**Date:** Tuesday 29 September 2026 · 15:00–16:50 · Lab Section (Week 1) — covers Week 0. Like every CS 101 lab, it
sits on the Tuesday after the week it covers (moved from Friday of Week 0, which is MATH 141's lab slot).
*Duration: 2 hours · Graded — 100 points via in-lab TA checkoff, part of the Labs component (10%)*

---

## Objectives

By the end of this lab, you will have:
- [ ] Python 3.10+ installed and working
- [ ] VS Code installed with the Python extension
- [ ] Git installed and configured
- [ ] A GitHub account connected to your repository
- [ ] Your first Python program committed and pushed
- [ ] Successfully experimented with the REPL
- [ ] Completed 3 warm-up exercises

If you get stuck on any step, raise your hand. The TA will help. Everyone hits installation problems, it is normal and expected.

---

## Part 1: Installation Verification (15 minutes)

Open a terminal and verify each tool:

### 1.1 Python

```bash
python3 --version
```

Expected output: `Python 3.10.x` or higher.

If you see `Python 2.7.x` or an error:
- **macOS:** Install via [python.org](https://python.org/downloads) or `brew install python3`
- **Windows:** Install via [python.org](https://python.org/downloads) — **check "Add to PATH"**
- **Linux (Ubuntu/Debian):** `sudo apt-get install python3 python3-pip`

### 1.2 VS Code

```bash
code --version
```

Expected output: A version number like `1.85.0`.

Install the Python extension:
1. Open VS Code
2. Press `Ctrl+Shift+X` (or `Cmd+Shift+X` on Mac)
3. Search "Python"
4. Install the extension by Microsoft

### 1.3 Git

```bash
git --version
```

Expected output: `git version 2.x.x`.

Configure your identity (do this once):
```bash
git config --global user.name "Your Full Name"
git config --global user.email "your.email@university.edu"
```

### 1.4 Verify the Terminal Works in VS Code

1. Open VS Code
2. Press `` Ctrl+` `` (backtick) to open the integrated terminal
3. Run `python3 --version` in the VS Code terminal
4. You should see the same output as before

---

## Part 2: Git Repository Setup (20 minutes)

### 2.1 Create Your Freshman Fall Repository

Your coursework does not live in your home directory. It lives in the Academic Registry, next to
the answer sheets. **All six Freshman Fall courses share one repository**, rooted at:

```
5. Academic Registry/4. Submissions/Year1 Freshman/Fall/
```

Each course is a folder inside it (`0. CS 101/`, `1. PROG 101/`, …). That is a long path with
spaces in it, so give it names once. Add this to `~/.bashrc` (the registry's
[[4. Submissions/README|README]] has the full block):

```bash
export ACADEMICS=~/"Documents/1. Academics/0. Computer Science and Engineering (B.Sc)"
export FALL1="$ACADEMICS/5. Academic Registry/4. Submissions/Year1 Freshman/Fall"
export CS101="$FALL1/0. CS 101"
```

Then open a new terminal and make the **Fall folder** a repository — once, for all six courses:

```bash
cd "$FALL1"
git init          # skip this if another course's lab already did it
ls -la            # You should see a .git folder
mkdir -p "$CS101"
```

**Quote `"$FALL1"` and `"$CS101"` every time.** The paths contain spaces; unquoted, `cd` gets
several arguments and fails.

This repository is deliberately kept out of the vault's git repo. You can run `git` commands from
inside any course folder — Git finds the repository in the parent folder automatically.

### 2.2 Create a README

Create a file called `README.md` in `"$FALL1"` with this content:

```markdown
# Freshman Fall — Coursework

**Student:** Your Name Here
**Year:** Freshman
**Institution:** [Your University]

## Course Overview

This repository contains my assignments, labs and projects for all six Freshman Fall courses.

## Structure

- `0. CS 101/` — Computer Science I (one `weekN/` folder per week)
- `1. PROG 101/` — Programming I in C
- ... (one folder per course)
```

### 2.3 Your First Commit

```bash
cd "$FALL1"
git add README.md
git status       # See what's staged
git commit -m "Initial commit: Add README for CS 101"
git log          # See your commit history
```

### 2.4 Connect to GitHub (if using GitHub)

1. Go to [github.com](https://github.com) and create an account if you don't have one
2. Create a new repository called `freshman-fall` (make it private)
3. Follow GitHub's instructions to connect your local repo:

```bash
git remote add origin https://github.com/yourusername/freshman-fall.git
git branch -M main
git push -u origin main
```

---

## Part 3: Your First Python Programs (30 minutes)

Create a folder for this week's work:
```bash
cd "$CS101"
mkdir -p week0
cd week0
```

### Exercise 3.1: Hello, World!

Create `hello.py`:

```python
# hello.py
# CS 101, Week 0, Lab 0
# Your Name, Date

print("Hello, World!")
print("My name is [Your Name].")
print("I am beginning my study of Computer Science.")
```

Run it: `python3 hello.py`

Commit it:
```bash
git add hello.py
git commit -m "Week 0 Lab: Add hello world program"
```

### Exercise 3.2: The REPL — Type Exploration

Open the Python REPL (`python3`) and run each of these. **Write down what you observe** in the space provided.

```python
# Types and their behavior
type(42)
type(3.14)
type(True)
type("hello")
type(None)

# Integer arithmetic
2 ** 32
2 ** 64
2 ** 100           # Notice anything about the size?
10 // 3
10 % 3
-10 % 3            # This might surprise you — think about why

# Float behavior
0.1 + 0.2          # Notice anything?
0.1 + 0.2 == 0.3   # What do you expect?
round(0.1 + 0.2, 10)

# String operations
"hello" + " " + "world"
"ha" * 5
len("computer science")
"Computer Science".lower()
"Computer Science".upper()
"Computer Science".replace("Computer", "Data")
"one,two,three".split(",")

# Type conversion
int(3.9)           # Truncates or rounds?
int("42")
int("3.9")         # What happens here?
float("3.14")
str(2 ** 10)
bool(0)
bool([])
bool([1, 2, 3])
```

**REPL Observations Log** (fill this out):

| Expression | Result | Why (your explanation) |
|---|---|---|
| `0.1 + 0.2` | | |
| `0.1 + 0.2 == 0.3` | | |
| `-10 % 3` | | |
| `int(3.9)` | | |
| `int("3.9")` | | |
| `bool([])` | | |

### Exercise 3.3: Temperature Converter

Create `temperature.py`:

```python
# temperature.py
# Temperature converter: Celsius ↔ Fahrenheit ↔ Kelvin
# CS 101, Week 0, Lab 0

# --- Formulas ---
# F = (C × 9/5) + 32
# C = (F - 32) × 5/9
# K = C + 273.15

print("=== Temperature Converter ===\n")

# Convert 100°C (boiling point of water)
celsius = 100.0
fahrenheit = (celsius * 9/5) + 32
kelvin = celsius + 273.15

print(f"Boiling point of water:")
print(f"  {celsius}°C = {fahrenheit:.2f}°F = {kelvin:.2f}K")

# Convert -40 (the point where Celsius and Fahrenheit are equal)
celsius = -40.0
fahrenheit = (celsius * 9/5) + 32
kelvin = celsius + 273.15

print(f"\n-40 degrees:")
print(f"  {celsius}°C = {fahrenheit:.2f}°F = {kelvin:.2f}K")

# Convert 98.6°F (normal human body temperature)
fahrenheit = 98.6
celsius = (fahrenheit - 32) * 5/9
kelvin = celsius + 273.15

print(f"\nHuman body temperature:")
print(f"  {fahrenheit}°F = {celsius:.2f}°C = {kelvin:.2f}K")

# CHALLENGE: Add absolute zero (-273.15°C)
# Your code here:
```

**Task:** Add the code to also print absolute zero (-273.15°C) in all three units.

### Exercise 3.4: Personal Calculator (Challenge)

Create `calculator.py`:

```python
# calculator.py
# A simple interactive calculator
# CS 101, Week 0, Lab 0

print("=== Simple Calculator ===")
print("Enter two numbers and I'll compute several things.\n")

# Get input
a = float(input("Enter first number: "))
b = float(input("Enter second number: "))

# Compute and display results
print(f"\nResults for {a} and {b}:")
print(f"  Sum:          {a} + {b} = {a + b}")
print(f"  Difference:   {a} - {b} = {a - b}")
print(f"  Product:      {a} × {b} = {a * b}")

# Division: handle division by zero
if b != 0:
    print(f"  Quotient:     {a} / {b} = {a / b:.6f}")
    print(f"  Floor div:    {a} // {b} = {a // b}")
    print(f"  Remainder:    {a} % {b} = {a % b}")
else:
    print("  Division by zero is undefined.")

print(f"  Power:        {a} ** {b} = {a ** b}")
```

**Task:** Run this with several inputs:
- `a=17, b=5`; what are the floor division and remainder results?
- `a=0, b=5`; what happens?
- `a=5, b=0`; does it handle this gracefully?
- `a=-7, b=3`; does modulo behave as you expect?

---

## Part 4: Commit Everything (10 minutes)

```bash
# From the $CS101/week0 directory
git add .
git status    # Make sure all files are staged
git commit -m "Week 0 Lab: Complete environment setup and exercises"
git push      # Push to GitHub (if configured)
git log --oneline   # See your commit history
```

---

## Part 5: Reflection Questions (15 minutes)

Answer these in a file called `reflection.md` in your `week0` folder:

**1. Type System**
Python's `int` type has no maximum value. C's `int` (32-bit) has a maximum of 2,147,483,647. Name one situation where Python's unlimited integers are necessary. Name one situation where C's fixed-size integers are preferable.

**2. Float Imprecision**
You observed that `0.1 + 0.2 != 0.3` in Python. Why does this happen? (Hint: think about binary representation.) What would be the consequence if financial software used regular floats for dollar amounts?

**3. Modulo Surprises**
You tested `-10 % 3`. The result in Python is `2`, not `-1` (which is what you might get in C or Java). Python's modulo result always has the same sign as the divisor. Why might this behavior be useful for computing things like "which day of the week is it N days after a given day"?

**4. Git**
Why is it better to make many small commits ("Add temperature conversion formula", "Handle division by zero") rather than one large commit ("Complete lab 0")?

---

## Lab Completion Checklist

Before leaving:
- [ ] Python 3.10+ installed: `python3 --version`
- [ ] VS Code installed with Python extension
- [ ] Git installed and configured with your name and email
- [ ] `hello.py` created and running
- [ ] REPL Observations Log filled out
- [ ] `temperature.py` completed (including absolute zero)
- [ ] `calculator.py` run with multiple inputs
- [ ] `reflection.md` written
- [ ] All files committed to Git
- [ ] TA has checked you off

---

## Additional Resources

- **Python Documentation:** https://docs.python.org/3/
- **Git Reference:** https://git-scm.com/doc
- **VS Code Python Tutorial:** https://code.visualstudio.com/docs/python/python-tutorial
- **Python Tutor (visualize code execution):** https://pythontutor.com

---

*CS 101 · Week 0 · Lab 0 · © CSE Department*
