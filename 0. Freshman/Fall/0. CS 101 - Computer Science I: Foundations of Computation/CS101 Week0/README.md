	# CS 101: Week 0: Orientation
## What is Computer Science?

---

## Contents of This Package

```
CS101_Week0/
│
├── README.md                           ← You are here
│
├── lectures/
│   ├── L01 What Is Computer Science.md     ← Wed: CS as a discipline, Turing, history
│   ├── L02 Python Environment and REPL.md  ← Thu: Tools, terminal, REPL, Git intro
│   └── L03 Values Types and Expressions.md ← Fri: Python types, operators, expressions
│
├── lab/
│   ├── LAB 0 Environment Setup.md          ← Tue lab instructions (2 hours)
│   ├── starter_hello.py                   ← Lab starter code — hello world
│   ├── starter_temperature.py             ← Lab starter code — temperature converter
│   ├── starter_calculator.py              ← Lab starter code — calculator
│   └── turing_machine_simulator.py        ← Bonus: TM simulator in Python
│
├── assignments/
│   └── QUIZ 0 Orientation Self Assessment.md ← Ungraded self-check quiz
│
└── resources/
    ├── Course Overview Syllabus.md         ← Full course info, grading, policies
    ├── Reading Guide Week 0.md              ← What to read, where to find it
    └── Python Quick Reference.md           ← Cheat sheet: types, operators, Git, terminal
```

---

## Week 0 at a Glance

**Theme:** Orientation (building the mental model before writing serious code).

| Day | Event     | What Happens                                         |     |
| --- | --------- | ---------------------------------------------------- | --- |
| Wed | Lecture 1 | What is CS? Algorithms, Turing, history, Von Neumann |     |
| Thu | Lecture 2 | Python, tools, terminal, REPL, Git setup             |     |
| Fri | Lecture 3 | Values, types, expressions, operators                |     |
| Tue | Lab 0     | Environment setup, first programs, Git repo          |     |

**No Problem Set this week.** (PS1 releases Friday of Week 1.)
**No Quiz this week.** (Quiz 1 is Wednesday of Week 2.)
**Ungraded self-assessment quiz** in `assignments/` — do this over the weekend.

---

## Your To-Do List for Week 0

### Before Wednesday's Lecture
- [ ] Read the Course Overview (`resources/Course Overview Syllabus.md`)
- [ ] Attempt to install Python 3, VS Code, and Git

### After Wednesday's Lecture
- [ ] Read L01 notes
- [ ] Watch: "Turing Machines Explained" on Computerphile (YouTube)

### After Thursday's Lecture
- [ ] Read L02 notes
- [ ] Complete at least the Python and Git installation steps
- [ ] Try the terminal commands in L02

### Tuesday Lab (Required)
- [ ] Bring laptop with Python, VS Code, Git installed (or ask for help)
- [ ] Complete all of LAB 0 Environment Setup.md
- [ ] Get checked off by TA before leaving

### After Friday's Lecture
- [ ] Read L03 notes
- [ ] Complete the self-assessment quiz (`assignments/QUIZ 0 Orientation Self Assessment.md`)
- [ ] Read Guttag Chapter 1
- [ ] Spend 30 minutes in the Python REPL experimenting

### Weekend
- [ ] Read `resources/Reading Guide Week 0.md` and follow the links
- [ ] Try `turing_machine_simulator.py` (bonus — highly recommended)
- [ ] Make sure your Git repo has all your lab files committed

---

## Core Ideas of Week 0

After this week, you should understand:

**1. What CS actually is**
Not programming. The *science of computation* — what can be computed, how efficiently, and with what certainty.

**2. The Turing Machine**
A simple model (infinite tape + read/write head + state machine) that defines all of computation. Your laptop is one. So is your phone. So is your brain (arguably).

**3. The Church-Turing Thesis**
Anything that can be computed by any mechanical process can be computed by a Turing Machine. This unifies all notions of computation.

**4. The Halting Problem**
There exist well-defined problems that no algorithm can solve — provably, forever, regardless of computing power. This is one of the most surprising results in all of mathematics.

**5. Variables as labels**
In Python, `x = 42` attaches the label `x` to the object `42`. Variables are not boxes; they are names.

**6. Types define legal operations**
You cannot add a string to an integer without explicit conversion. This is not arbitrary — it prevents logical errors.

**7. Git as an engineering practice**
Version control is not optional in professional software development. Start using it now, for everything.

---

## The Big Picture

You are beginning a four-year journey that will take you from these foundations to designing full operating systems, building compilers, training machine learning models, and creating distributed systems that serve millions of users.

Every concept in Year 1 is a seed. The harvest comes in Years 2, 3, and 4. The students who succeed are the ones who understand Year 1 deeply — not the ones who race through it.

**Take it seriously. Ask questions. Use the REPL. Commit your code.**

---

*CS 101 · Week 0 · Orientation Package · © CSE Department*
