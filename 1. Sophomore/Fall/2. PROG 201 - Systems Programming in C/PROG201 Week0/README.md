# PROG 201 · Systems Programming in C
## Week 0: The Unix Process Model

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101; CS 201 as co-requisite
**Assessment for this course (overall):** Problem Sets 35%, Projects 25%, Midterms 25%, Final 15%
**This week's deliverables:** Lab 0 and PS 0. **No quiz** — Quiz 1, in Week 1, covers this week.

> **Week 0 is ten days long**, running Aug 27 to Sep 5. It absorbs orientation, add/drop and Labor
> Day, and Week 1 — when graded work begins — opens Sep 8. You get all three lectures and the lab.

---

### Why This Week Exists

Because you can write C, and you cannot yet write a program that starts another program.

**PROG 201 is about the calls that only the kernel can answer.** Over thirteen weeks you will write a shell, a concurrent HTTP server, an allocator, a JIT, a filesystem and a container — six programs that have nothing in common except that none of them can be written in portable C alone.

This week is the foundation all six stand on: **what a process is, how one is made, how one ends, and how one is interrupted.** By Friday you will have written a process supervisor — the thing `systemd` and Kubernetes are elaborations of — and it will be about 200 lines.

It also sets the habit the course is graded on: **when the man page, the textbook and the machine disagree, go and look.** L02 has the first case, and it is not a contrived one.

---

### Learning Objectives

By the end of Week 0, you should be able to:

1. List what the kernel holds per process, and find each item in `/proc`.
2. Use `fork()` correctly, including the `-1` case, and say what the child does and does not inherit.
3. Explain copy-on-write, and predict the page-fault count for a reader and a writer.
4. **Say what `fork()` costs** — that it is linear in the parent's address space — and choose `posix_spawn` when that matters.
5. Explain why a buffered `printf` before a `fork` prints twice, and give the fix.
6. Decode a `wait` status word by hand: exited, signalled, core, and the 8-bit truncation.
7. Write a correct reaping loop, and say why it is a loop.
8. **Say who adopts an orphan on this machine, and why it is not PID 1.**
9. Explain why unreaped children are a denial of service against the whole user, not just the process.
10. Use `sigaction` and justify each flag; write a handler that sets a flag, calls only safe functions, and restores `errno`.
11. **Explain why signals are not a message queue**, with a number attached.
12. Wait for a signal without a race, and say what is wrong with `pause()`.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L01 What a Process Is and What fork Copies]] | `/proc` as the process; `fork`'s two returns; COW measured at 0 and 16,384 faults; **fork at 34 µs/MB and `posix_spawn` 70× faster**; the stdio buffer trap; `exec` |
| [[L02 Waiting Zombies and the Process Table]] | The status word by hand; zombies with RSS 0; `waitpid`/`WNOHANG`; **orphans adopted by PID 257510, not 1**; `RLIMIT_NPROC` as a DoS; groups and sessions; the state machine |
| [[L03 Signals and Async-Signal-Safe Code]] | `sigaction` against `signal`, measured; **5,000 signals delivered once**; 192 safe functions; `printf` corrupting two thirds of its own output; `EINTR`; the `pause()` race |
| [[LAB 0 The Process Supervisor]] | Build a supervisor that restarts crashed children and shuts down cleanly. **Friday of Week 0** |
| `lab/supervisor.c`, `lab/flaky.c`, `lab/Makefile` | The skeleton, the thing to supervise, and the build |
| [[PROG201 Week0/assignments/Problem Set 0\|Problem Set 0]] | Five questions, 100 points, due **Friday of Week 1** |
| [[PROG201 Week0/resources/Course Overview Syllabus\|Course Overview Syllabus]] | **Read this in full in Week 0** — assessment, the lab lag, Fall Break's effect on Lab 5, deviations |
| [[PROG201 Week0/resources/Reading Guide Week 0\|Reading Guide Week 0]] | Which of APUE 1–8 is this week, which is Week 1, and thirteen questions |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A signal is not a message, and a process is not a program.**

Both halves are the same mistake in different clothing: treating a kernel object as if it were the thing you can see. A program is a file; a process is the bundle of state that happens to be running it, and `exec` proves it by swapping the file without disturbing the bundle. A message is data you can count; a signal is **one bit that says something happened at least once** — 5,000 of them, sent while blocked, deliver exactly once.

**Every design decision in the rest of this course follows from that second sentence.** The reaping loop is a loop because of it. The supervisor cannot count crashes from `SIGCHLD` deliveries because of it. Week 6's shell keeps its own job table because of it. And the moment you write a handler that assumes one delivery means one event, you have written a bug that will not appear until the machine is busy.

---

### Assessment Reminder

**Labs and quizzes carry no weight.** The curriculum's assessment line sums to 100% without them, and no percentage has been invented to fill the gap.

They are still required. **The lab is checked off by the TA in the session**, and a second unexcused absence costs a letter grade. **Quiz *N* covers Week *N−1***, runs ten minutes at the start of **Tuesday's** lecture in Weeks 1–11, and prints its own answer key.

> **This course's lab lags a full week, because the lab is on Monday and the lectures are Tuesday
> through Thursday.** Lab *N* covers Week *N* and is sat on the **Monday of Week *N+1***. Lab 0 is
> the exception: it is sat on the **Friday that closes the ten-day Week 0**, at **17:00–18:50** —
> after all three lectures, and after CS 201's and CS 211's Week 0 labs have vacated the afternoon. There is no lab in Week 1. **CS 201 lags too and CS 211 does not** — read each course's
> own header rather than carrying a habit between them.

Both are tracked in [[_PROG 201 Lab and Quiz Record]].

---

### Connections

**Back:** **PROG 101 is assumed and not re-taught** — pointers, arrays, `struct`, and the standard library are vocabulary here. If `char *argv[]` is not immediately obvious to you, revisit PROG 101 Week 6 before Week 1's descriptor tables.

**Sideways:** **CS 201 runs alongside and the two interlock all term.** CS 201's address space is what `fork()` copies the page tables of; its stack is what `execve` builds for the new program; its `/proc/pid/maps` is Week 4's subject. When L01 says "34 µs per megabyte of page tables", CS 201 Week 6 is where you learn what a page table entry is.

**Forward:** **Lab 0's supervisor is Week 6's shell**, minus the parser and the process groups — the `SIGCHLD` handler and the `waitpid`/`WNOHANG` loop transfer line for line into Project 1. L03's `sigsuspend` becomes Week 5's `pselect` and Week 12's shutdown handler. **CS 202 in Spring implements the calls this week makes**: you will write the `fork` whose contract you spent this week reading.

---

*PROG 201 · Week 0 · © CSE Department*
