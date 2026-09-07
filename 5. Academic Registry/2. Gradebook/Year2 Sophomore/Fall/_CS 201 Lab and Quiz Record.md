# CS 201 · Lab and Quiz Record
## Not part of the course grade

> **This file is deliberately outside the gradebook's weighted components.** CS 201's
> labs and quizzes carry **no weight** — Problem Sets 35, Midterms 25, Final 20 and Projects 20 already sum to 100% without them,
> and [[CS 201]] says so.
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
| Lab 0 | Week 0 | Install NASM and GDB; disassemble a C program | — | |
| Lab 1 | Week 1 | Demonstrate floating-point non-associativity | — | |
| Lab 2 | Week 2 | Read the assembly output of increasingly complex C programs | — | |
| Lab 3 | Week 3 | Trace a function call with GDB; inspect stack frames | — | |
| Lab 4 | Week 4 | Measure cache effects with perf and cachegrind | — | |
| Lab 5 | Week 5 | Vectorize a loop with AVX intrinsics | — | |
| Lab 6 | Week 6 | Observe page faults through /proc/pid/maps | — | |
| Lab 7 | Week 7 | Benchmark disk against SSD access patterns | — | |
| Lab 8 | Week 8 | Capture and analyze packets with Wireshark | — | |
| Lab 9 | Week 9 | Defeat a stack canary with a format string exploit | — | |
| Lab 10 | Week 10 | Implement a parallel reduction in CUDA | — | |
| Lab 11 | Week 11 | Full optimization project: profile, optimize, re-profile | — | |
| Lab 12 | Week 12 | Demo day — the CPU simulator runs real programs | — | |

---

## Quizzes

**Ten minutes at the start of the course's first lecture of the week, Weeks 1–11.** Closed book. Not marked — the answer key is printed in the paper, below the questions.

**Quiz *N* is sat in Week *N* and covers Week *N−1*.** Year 2 numbers its quizzes after the week they are sat in. *(Year 1 was not consistent about this: CS 102 and MATH 142 used the same rule, but ECE 110 numbered its quizzes after the material instead. Check the course before assuming.)*

| Quiz | Sat in | Covers | Topic | Out of | Done |
|---|---|---|---|---|---|
| Quiz 1 | Week 1 | Week 0 | Trace a fetch-decode-execute cycle by hand | — | |
| Quiz 2 | Week 2 | Week 1 | Bit-level manipulation in C; IEEE 754 dissection | — | |
| Quiz 3 | Week 3 | Week 2 | Write five small x86-64 assembly functions | — | |
| Quiz 4 | Week 4 | Week 3 | Recursive Fibonacci in x86-64 assembly | — | |
| Quiz 5 | Week 5 | Week 4 | Matrix transpose optimization — exploit cache locality | — | |
| Quiz 6 | Week 6 | Week 5 | Identify hazards in instruction sequences | — | |
| Quiz 7 | Week 7 | Week 6 | Implement a page table simulator | — | |
| Quiz 8 | Week 8 | Week 7 | Simulate disk I/O scheduling (SSTF, SCAN) | — | |
| Quiz 9 | Week 9 | Week 8 | A simple TCP echo client and server in C | — | |
| Quiz 10 | Week 10 | Week 9 | Exploit a series of intentionally vulnerable programs (sandboxed) | — | |
| Quiz 11 | Week 11 | Week 10 | Parallelize matrix multiplication with OpenMP | — | |

*There is no quiz covering Week 11 or Week 12 — those are examined only on the final.*

---

## Why Unmarked Work Is Worth Doing

The feedback loop that matters here is the one that closes in the next five minutes, not the one that closes when a grade comes back three weeks later. A quiz you mark yourself against the key in the same sitting tells you what has not landed while there is still a term left to fix it. Marking it would add a number and subtract nothing from the misunderstanding.

---

*CS 201 · Lab and Quiz Record · Year 2 Fall*
