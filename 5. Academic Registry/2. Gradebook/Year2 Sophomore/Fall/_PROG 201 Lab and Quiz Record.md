# PROG 201 · Lab and Quiz Record
## Not part of the course grade

> **This file is deliberately outside the gradebook's weighted components.** PROG 201's
> labs and quizzes carry **no weight** — Problem Sets 35, Projects 25, Midterms 25 and Final 15 already sum to 100% without them,
> and [[PROG 201]] says so.
>
> The leading underscore in the filename keeps this file out of `tools/gpa.py`'s course scan. Do not
> rename it without checking `collect()` in that script.

---

## Why This Is a Separate File

The gradebook parser reads a component's items from its heading until the **next `##` heading
containing a percentage**. An unweighted subheading has none, so its rows are silently absorbed into
the component above it. The failure was found in CS 102 in Year 1, where eleven quiz rows quietly
attached themselves to Project 2. Year 2 avoids it the same way Year 1 settled on: the unweighted
work lives here, and the gradebook has no table for it at all.

**The `Out of` column reads `—`, not a number.** That is load-bearing. `tools/make_answer_sheets.py`
reads it, and a non-numeric entry is what makes a sheet say `Marks: ___ / —` rather than inventing a
total the paper never claimed. Writing `0` would mean the same thing to a reader and the wrong thing
to the tool.

Use the **Done** column as a tick. The point of the record is that you can see, in one place, which
weeks you actually did the work.

---


## Labs

**Thirteen labs, Weeks 0–12, in the scheduled session.** Mandatory. The TA checks the work off during or just after the session; nothing is marked out of anything.

> **Attendance is the enforcement.** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] reduces the final course grade > by one letter after a second unexcused lab absence. That rule, not a mark, is why the > lab is not optional.

| Lab | Week | Topic | Out of | Done |
|---|---|---|---|---|
| Lab 0 | Week 0 | Write a process supervisor that restarts crashed children | — | |
| Lab 1 | Week 1 | Build a pipeline: ls | grep | wc, in C | — | |
| Lab 2 | Week 2 | IPC performance benchmark | — | |
| Lab 3 | Week 3 | Demonstrate priority inversion and its fix | — | |
| Lab 4 | Week 4 | Write a JIT that generates and executes machine code | — | |
| Lab 5 | Week 5 | Stress-test the HTTP server with Apache Benchmark | — | |
| Lab 6 | Week 6 | Add job control (fg, bg, jobs) to the shell | — | |
| Lab 7 | Week 7 | Corrupt and recover an ext4 filesystem | — | |
| Lab 8 | Week 8 | Implement a plugin system with dlopen | — | |
| Lab 9 | Week 9 | Roofline model analysis of a computation | — | |
| Lab 10 | Week 10 | Fuzz a provided program with AFL and find bugs | — | |
| Lab 11 | Week 11 | Run a program in an isolated container | — | |
| Lab 12 | Week 12 | Final demo and code review | — | |

---

## Quizzes

**Ten minutes at the start of the course's first lecture of the week, Weeks 1–11.** Closed book. Not marked — the answer key is printed in the paper, below the questions.

**Quiz *N* is sat in Week *N* and covers Week *N−1*.** Year 2 numbers its quizzes after the week they are sat in. *(Year 1 was not consistent about this: CS 102 and MATH 142 used the same rule, but ECE 110 numbered its quizzes after the material instead. Check the course before assuming.)*

| Quiz | Sat in | Covers | Topic | Out of | Done |
|---|---|---|---|---|---|
| Quiz 1 | Week 1 | Week 0 | The Unix process model: fork, exec, wait, zombies | — | |
| Quiz 2 | Week 2 | Week 1 | Implement I/O redirection (pipe and redirect operators) | — | |
| Quiz 3 | Week 3 | Week 2 | A producer-consumer pipeline using pipes and shared memory | — | |
| Quiz 4 | Week 4 | Week 3 | Implement a thread pool | — | |
| Quiz 5 | Week 5 | Week 4 | Implement a basic malloc/free using mmap | — | |
| Quiz 6 | Week 6 | Week 5 | Build a concurrent HTTP/1.0 server | — | |
| Quiz 7 | Week 7 | Week 6 | Implement a shell (tsh) with pipelines, redirection, background jobs | — | |
| Quiz 8 | Week 8 | Week 7 | Implement a simple file system in C over a disk image | — | |
| Quiz 9 | Week 9 | Week 8 | Use LD_PRELOAD to intercept malloc() for profiling | — | |
| Quiz 10 | Week 10 | Week 9 | Optimize a provided slow program — 5× by analysis, not guessing | — | |
| Quiz 11 | Week 11 | Week 10 | Build a working ROP chain exploit (sandboxed) | — | |

*There is no quiz covering Week 11 or Week 12 — those are examined only on the final.*

---

## Why Unmarked Work Is Worth Doing

The feedback loop that matters here is the one that closes in the next five minutes, not the one that closes when a grade comes back three weeks later. A quiz you mark yourself against the key in the same sitting tells you what has not landed while there is still a term left to fix it. Marking it would add a number and subtract nothing from the misunderstanding.

---

*PROG 201 · Lab and Quiz Record · Year 2 Fall*
