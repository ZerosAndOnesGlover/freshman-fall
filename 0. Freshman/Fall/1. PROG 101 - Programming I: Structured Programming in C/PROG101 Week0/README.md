# PROG 101 · Week 0: The C Compilation Model
## Orientation & Tool-chain Setup

---

## Week Overview

Week 0 is orientation week. There are no graded assignments due *this* week — but Lab 0 must be completed, and Problem Set 0 is released at the end of the week (due before Week 1 Lecture 1).

The goal: get your environment working, understand the compilation pipeline deeply, and write your first C programs.

---

## Schedule

| Day       | Event                              | Location      | Duration |
| --------- | ---------------------------------- | ------------- | -------- |
| Tuesday   | Lecture 1: The C Compilation Model | Main Hall 101 | 50 min   |
| Wednesday | Lecture 2: Toolchain, Make, GDB    | Main Hall 101 | 50 min   |
| Thursday  | Lecture 3: Hello World Deep Dive   | Main Hall 101 | 50 min   |
| Monday    | **Lab 0: Environment Setup**       | Lab 204       | 2 hours  |

---

## Files in This Package

```
PROG101_Week0/
├── README.md                          ← You are here
│
├── lectures/
│   ├── Lecture 01 Compilation Model.md    ← The four-stage pipeline
│   ├── Lecture 02 Tool-chain Make GDB.md   ← GCC, Make, GDB, Git
│   └── Lecture 03 Hello World Deep-Dive.md ← C anatomy, printf, scanf
│
├── lab/
│   ├── LAB 0 Environment Setup.md          ← Lab instructions (2 hrs)
│   └── starter/
│       ├── hello.c                        ← Starter: Hello World
│       └── buggy.c                        ← Starter: Buggy program for GDB
│
├── assignments/
│   ├── Problem Set 0.md                   ← PS0 (due Week 1 Tuesday)
│   └── starter/
│       └── broken.c                       ← Starter: broken.c for PS0 P4
│
├── quizzes/
│   └── QUIZ 0.md                          ← Quiz administered Week 1 Tuesday
│
└── resources/
    └── c_quick_reference.md               ← Keep this open always
```

---

## Learning Objectives

After Week 0, you will be able to:

- [ ] Explain the four stages of C compilation and what each produces
- [ ] Distinguish between preprocessor, compiler, assembler, and linker errors
- [ ] Use GCC with essential flags (`-Wall`, `-Wextra`, `-g`, `-std=c11`)
- [ ] Write a Makefile that builds a C program with proper flags
- [ ] Use GDB to set breakpoints, step through code, and inspect variables
- [ ] Use Git to version control your code
- [ ] Read and write a basic C program (Hello World level)
- [ ] Use `printf` with format specifiers correctly
- [ ] Understand declaration vs definition in C

---

## Textbook Reading

Before each lecture:

| Lecture | Reading |
|---------|---------|
| Lecture 1 | K&R §1.1; King Ch. 1 |
| Lecture 2 | K&R §1.2–1.4; CS:APP §1.1–1.5 |
| Lecture 3 | K&R §1.5–1.9; King Ch. 2 |

---

## The Most Important Thing This Week

Learn to ask: *"What is the machine actually doing?"*

When you write `#include <stdio.h>`, what happens? When you type `gcc hello.c`, what happens? When your program crashes, what is the CPU actually doing?

C is the language that forces these questions. That is why we start here.

A programmer who has never thought about these questions can write code. An *engineer* understands the machine they are programming. That is the difference this course is training.

---

## Getting Help

- **Office hours:** Tue/Mon 3-5pm, Room 312
- **Course forum:** Piazza (see course portal for link)
- **Email TAs:** For lab issues — TA emails on course portal
- **Rule for help:** Attempt the problem first. Come to office hours with a specific question and what you've already tried.

---

## A Note on C

C will feel brutal at first. It does not protect you from mistakes. It does not catch errors at the last minute. It gives you exactly what you ask for — no more, no less.

That is not a flaw. That is the point.

Every language you use professionally (Python, Java, Rust, Go, JavaScript, etc.) is built on abstractions that C exposes. When something goes wrong in any of these languages, the engineers who can debug it are the ones who know what's happening underneath. That knowledge comes from C.

You are not just learning a programming language. You are learning how computers work.

*Welcome to PROG 101.*
