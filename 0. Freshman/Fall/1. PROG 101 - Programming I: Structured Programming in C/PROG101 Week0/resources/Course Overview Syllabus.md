# PROG 101 · Course Overview & Syllabus
## Programming I: Structured Programming in C

---

## Course Information

| | |
|---|---|
| **Credits** | 4 (3 lecture + 1 lab) |
| **Meetings** | Tue/Wed/Thu, 50 minutes each |
| **Lab** | Monday, 2 hours |
| **Language** | C (C99/C11 standard) |
| **Prerequisites** | None (concurrent: CS 101 recommended) |

---

## Course Description

PROG 101 teaches programming in C — a language close enough to the hardware to teach you what a
computer actually does, yet abstract enough to write real programs. C is the language in which Unix,
Linux, the Python interpreter, most databases, and much of the firmware in your devices is written.

Learning C first is a deliberate pedagogical choice: it forces you to confront memory, pointers, and
the machine model directly — knowledge that makes you a better programmer in every language you learn
afterward.

This course takes a **structured programming** approach. Structured programming is not just a style;
it is a methodology for writing programs whose correctness can be reasoned about. Every construct you
learn — sequence, selection, iteration, functions — corresponds to a formal verification technique.

### Why C before Python or Java?

Python hides memory management, types, and the call stack. Java hides pointers and memory. **C hides
nothing.** When you write `int *p = malloc(sizeof(int)); *p = 42; free(p);` you are directly
allocating heap memory, storing a value, and releasing it. No garbage collector. No runtime magic.

---

## Required Textbooks

**1. Kernighan, B. & Ritchie, D. — The C Programming Language, 2nd ed.** *(Prentice Hall, 1988)*
"K&R" — written by the creators of C. Compact, precise, profound. Read every page.

**2. King, K.N. — C Programming: A Modern Approach, 2nd ed.** *(W.W. Norton, 2008)*
Comprehensive and pedagogically excellent. Fills gaps in K&R for modern C.

**3. Bryant, R. & O'Hallaron, D. — Computer Systems: A Programmer's Perspective, 3rd ed.** *(Pearson, 2016)*
"CS:APP" — Chapters 1–3. Explains what C actually compiles to.

**4. Seacord, R. — Effective C** *(No Starch Press, 2020)*
Modern, safety-conscious C. Complements K&R.

---

## Assessment Breakdown

| Component | Weight | Details |
|-----------|--------|---------|
| **Problem Sets (13)** | 35% | PS 0–12, released Friday, due the following Friday at 17:00. Each worth 100 points. **Lowest 1 dropped.** |
| **Lab Sections (12)** | 20% | Lab 1–12, Mondays, 2 hours. Each worth 20 points, graded on completion and correctness with TA checkoff. **Lab 0 is completion-only** and carries no weight. |
| **Midterm Exam 1** (Week 6) | 12.5% | 75 minutes, written. Covers Weeks 0–5. |
| **Midterm Exam 2** (Week 10) | 12.5% | 75 minutes, written. Covers Weeks 6–9. |
| **Final Exam** (Finals week) | 20% | Comprehensive, 150 minutes. |

**Total:** 100%

> **Quizzes carry no direct weight.** The 12 Tuesday quizzes (Quiz 0 in Week 0, then Quiz *N* in
> Week *N+1* covering Week *N*) are **formative**: marked and returned so you and the staff can see
> where you stand, but they do not enter the course grade. Each is 20 points and 10 minutes.

**Grading scale:** this course uses the **university-wide 13-band scale** defined in
[[UNIVERSITY POLICIES]] (Academic Registry) — A+ 97–100, A 93–96, A− 90–92, B+ 87–89, B 83–86,
B− 80–82, C+ 77–79, C 73–76, C− 70–72, D+ 67–69, D 63–66, D− 60–62, F below 60. The registry copy
governs if the two ever differ.

**Credit hours:** 4

---

## The Build Line

Every submission must compile cleanly with:

```
gcc -Wall -Wextra -Werror -pedantic -std=c11 -g
```

and run cleanly under:

```
valgrind --leak-check=full --error-exitcode=1
gcc -fsanitize=address,undefined
```

**Automatic deductions:** any compiler warning (−3 per problem set problem, −2 per lab part); any
Valgrind error or sanitizer report in code that is not deliberately broken (−5 / −3).

This is not pedantry. `-Werror` is how you find out that `i = i++` has no meaning, that your `switch`
falls through by accident, and that you returned the address of a dead stack frame. The flags are
part of the language as this course teaches it.

---

## Weekly Schedule

| Week | Topic | Key Assessments |
|------|-------|----------------|
| 0 | The C Compilation Model | PS 0, Lab 0 *(ungraded)*, Quiz 0 |
| 1 | Types, Variables, and the Memory Model | PS 1, Lab 1 |
| 2 | Operators, Expressions, and Control Flow | PS 2, Lab 2, Quiz 1 |
| 3 | Functions and Structured Programming | PS 3, Lab 3, Quiz 2 |
| 4 | Arrays and Strings | PS 4, Lab 4, Quiz 3 |
| 5 | Pointers I: The Fundamental Abstraction | PS 5, Lab 5, Quiz 4 |
| 6 | Pointers II: Dynamic Memory | **Midterm 1**, PS 6, Lab 6, Quiz 5 |
| 7 | Structures, Unions, and Enumerations | PS 7, Lab 7, Quiz 6 |
| 8 | File I/O and the UNIX File Model | PS 8, Lab 8, Quiz 7 |
| 9 | Recursion in C and Stack Mechanics | PS 9, Lab 9, Quiz 8 |
| 10 | The C Preprocessor and Macros | **Midterm 2**, PS 10, Lab 10, Quiz 9 |
| 11 | The C Standard Library and System Programming Preview | PS 11, Lab 11, Quiz 10 |
| 12 | Software Engineering in C: Style, Testing, Debugging | **Final Exam**, PS 12, Lab 12, Quiz 11 |

---

## Problem Set Policy

- **Released:** Every Friday after lecture
- **Due:** The following Friday at 17:00
- **Late policy:** 20% deduction per day, nothing accepted after 3 days
- **Lowest grade dropped**
- **Format:** C source files + a `Makefile` + a written `answers.md`

## Lab Policy

Labs meet Monday for 2 hours. Check-offs are done by the TA during lab. You must complete at least
70% of each lab to receive credit. If you miss a lab, you may attend another section that week only
with TA approval in advance.

---

## Collaboration Policy

**Problem sets:** discuss approaches freely; all submitted code must be your own. If you cannot
explain a line to a TA, you have not learned it.

**Labs:** collaboration encouraged. Work with a partner if you like; both submit.

**Exams:** no collaboration.

**AI tools:** using AI to generate code you submit as your own is academic dishonesty. You may use AI
to *explain* concepts. In a course whose entire purpose is building a mental model of the machine,
outsourcing the modelling defeats the exercise.

---

## Why This Course Is Designed This Way

You will spend a great deal of Week 5 and Week 6 on pointers, and it will be harder than anything in
CS 101. That is deliberate.

Pointers are not a C quirk to be endured. They are the moment the machine stops being an abstraction:
memory is an array of bytes, a pointer is an index into it, and everything else — arrays, strings,
structs, linked lists, objects in every language you will ever use — is built on that one idea. Once
you have written a dynamic array with `malloc` and `realloc` and watched Valgrind catch your
use-after-free, you understand what a Python list *is*.

The difficulty is the content, not an obstacle in front of it.

---

*PROG 101 · Course Overview & Syllabus · © CSE Department*
