# CS 101 · Week 0 Orientation Quiz
## (Ungraded: Self-Assessment)

**Purpose:** This quiz helps you check your understanding of Week 0 concepts.
It is not graded. Answer honestly, your score tells you where to review before Lecture 1.

**Time:** 20 minutes
**Instructions:** Answer without looking at notes first. Then check your answers.

---

## Section A: Conceptual Questions (Short Answer)

**A1.** In one sentence, define an **algorithm**. What three properties must it have?

```
Your answer:
```

**A2.** What is the **Church-Turing Thesis**? What does it imply about your laptop vs. a Turing Machine?

```
Your answer:
```

**A3.** Why is the **Halting Problem** significant? Give the key idea of Turing's proof (not the full proof — just the idea).

```
Your answer:
```

**A4.** What is the difference between a **dynamically-typed** language (like Python) and a **statically-typed** language (like C or Java)? Name one advantage of each.

```
Your answer:
```

**A5.** What is a **REPL**, and why is it a useful tool for learning programming?

```
Your answer:
```

---

## Section B: Python Types: Predict the Output

For each code snippet, **predict the output** before running it. Then run it in the REPL and check.

**B1.**
```python
x = 10
y = 3
print(x / y)
print(x // y)
print(x % y)
```
Your prediction:
```

```
Actual output (run it):
```

```
Were you right? If not, explain why:
```

```

**B2.**
```python
print(type(5))
print(type(5.0))
print(type(5 / 2))
print(type(5 // 2))
```
Your prediction:
```

```
Actual:
```

```

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
Your prediction:
```

```
Actual:
```

```

**B4.**
```python
print(0.1 + 0.2 == 0.3)
print(bool(0))
print(bool(""))
print(bool([]))
print(bool(None))
```
Your prediction:
```

```
Actual:
```

```

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
Your prediction:
```

```
Actual:
```

```

---

## Section C: Type Conversion, What Happens?

For each line, state whether it succeeds or raises an error. If it succeeds, give the result and type.

| Expression | Succeeds or Error? | Result (if success) | Type (if success) |
|---|---|---|---|
| `int(3.9)` | | | |
| `int("42")` | | | |
| `int("3.9")` | | | |
| `int("hello")` | | | |
| `float(True)` | | | |
| `str(None)` | | | |
| `bool(0.0)` | | | |
| `bool(-1)` | | | |

-------------- | ------------------ | ------------------- | ----------------- |
| `int(3.9)`     | Succeeds           | 3                   | int               |
| `int("42")`    | Suceeds            | 42                  | int               |
| `int("3.9")`   | Error              |                     |                   |
| `int("hello")` | Error              |                     |                   |
| `float(True)`  | Succeds            | 1.0                 | float             |
| `str(None)`    | Succeeds           | 'None'              | string            |
| `bool(0.0)`    | Suceeds            | False               | boolean           |
| `bool(-1)`     | Suceeds            | True                | boolean           |

---

## Section D: Git Knowledge

**D1.** What is the difference between `git add` and `git commit`?

```
Your answer:
```

**D2.** What command shows you the current state of your repository (what's changed, what's staged)?

```
Your answer:
```

**D3.** What does a good commit message look like? Give an example of a bad one and a good one.

```
Bad:
Good:
```

---

## Section E: Big Picture

**E1.** Order these three fields from most theoretical to most practical:
`[ ] Computer Engineering  [ ] Computer Science  [ ] Software Engineering`

Your order (most theoretical → most practical):
```

```
Justify your ordering in one sentence:
```

```

**E2.** Why do we study Python in CS 101 rather than teaching it as a purely theoretical course with no programming?

```
Your answer:
```

**E3.** What is the **Von Neumann architecture**, and what is its key insight about programs and data?

```
Your answer:
```

---

## Answer Key

*(Check your answers after completing the quiz)*

**A1.** An algorithm is a finite, unambiguous, executable sequence of instructions that solves a class of problems. The three properties: finite (terminates), unambiguous (each step has one interpretation), executable (can be carried out).

**A2.** The Church-Turing Thesis states that any computation that can be performed by any mechanical process can be performed by a Turing Machine. Implication: your laptop is computationally equivalent to a Turing Machine — it can compute exactly the same set of functions (just faster with more memory).

**A3.** The Halting Problem (can we determine if any program halts on any input?) is significant because Turing proved it **undecidable** — no algorithm can solve it for all programs. Proof idea: assume HALT(P, I) exists, construct program D that runs HALT(D, D) and does the opposite — a contradiction.

**A4.** Dynamically typed: types checked at runtime; code is more flexible, faster to write. Statically typed: types checked at compile time; type errors caught before running, better performance. Advantage of dynamic: faster iteration. Advantage of static: entire class of bugs caught early.

**A5.** REPL = Read-Eval-Print Loop. It reads an expression, evaluates it, prints the result, and loops. Useful for experimentation, quick testing of ideas, and learning — you get immediate feedback.

**B1.** `3.3333...`, `3`, `1`
**B2.** `<class 'int'>`, `<class 'float'>`, `<class 'float'>` (division always returns float in Python 3), `<class 'int'>`
**B3.** `1`, `10`, `False`, `True`, `False`
**B4.** `False`, `False`, `False`, `False`, `False` — all falsy values
**B5.** `16`, `C`, `e`, `Computer`, `computer science`, `True`

**C1.** `int(3.9)` → succeeds → 3 (int) — truncates toward zero, not rounds
**C2.** `int("42")` → succeeds → 42 (int)
**C3.** `int("3.9")` → **ValueError** — must convert to float first
**C4.** `int("hello")` → **ValueError**
**C5.** `float(True)` → succeeds → 1.0 (float)
**C6.** `str(None)` → succeeds → `'None'` (str) — the string "None"
**C7.** `bool(0.0)` → succeeds → False (bool)
**C8.** `bool(-1)` → succeeds → True — any non-zero number is `truthy`

**D1.** `git add` stages changes (prepares them for a commit). `git commit` permanently saves the staged changes to history with a message.
**D2.** `git status`
**D3.** Bad: `"fix"`, `"stuff"`, `"aaa"`. Good: `"Add temperature conversion formula"`, `"Fix off-by-one error in loop termination"`

**E1.** Computer Science → Software Engineering → Computer Engineering is the usual answer (L01 §3). Accept a defended alternative.
**E2.** The course's ideas (algorithms, cost, correctness) only become concrete when you run them: a program is a precise, testable statement of an algorithm, and Python keeps syntax out of the way.
**E3.** One memory holds **both the program's instructions and its data**; the CPU fetches, decodes and executes instructions one at a time (L01 §8). Key insight: a program is just data, so programs can load and run other programs.

---

## Score Interpretation

- **18–20 correct:** Excellent foundation. You'll move quickly through Week 1.
- **14–17 correct:** Good start. Review the concepts you missed before Lecture 1.
- **10–13 correct:** Re-read Lectures 1–3 before next class. Focus on sections you found confusing.
- **Under 10:** Spend extra time in office hours this week. The early material is the most important.

---

*CS 101 · Week 0 · Orientation Quiz (Ungraded) · © CSE Department*
