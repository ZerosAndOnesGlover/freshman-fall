# PROG 201 · Systems Programming in C
## Week 6: The Shell — Parsing, Execution, and Job Control

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101; CS 201 as co-requisite
**Assessment for this course (overall):** Problem Sets 35%, Projects 25%, Midterms 25%, Final 15%
**This week's deliverables:** PS 5 (due Friday), PS 6 (released Wednesday, due Friday of Week 7), **Quiz 6** (Tuesday, covers Week 5), and **Project 1 assigned on Friday**.
**Lab 5 is sat on the Friday of this week, 16:00–17:50**; **Lab 6 covers this week and is sat on the Monday of Week 7.**

> ### **Fall Break is the Monday of this week — no classes.**
> The week starts on Tuesday, and three things land on the Friday: **PS 5 is due at 17:00**,
> **Lab 5 is sat 16:00–17:50**, and **Project 1 is assigned**. Submit PS 5 before the lab.
> [[PROG 201 Scheduling Notes]] records why the lab is on a Friday and why the deadline collides.

---

### Why This Week Exists

Because you have written every part of a shell already, and the thing you have not written is the reason Ctrl-C kills `ls | grep | wc` and not `bash`.

Weeks 0–2 gave `fork`, `exec`, `wait`, `dup2` and `pipe`. Lab 1 built `ls | grep | wc` with no shell. **What is left is the structure around them, and one genuinely new idea:** the kernel needs a name for "the processes attached to this terminal right now", and that name is a **process group**.

Three ideas:

1. **A shell is a loop, a parser, and a job table** around calls you already know. `dash` is 15,000 lines and yours will be 400; the difference is quoting, expansion and control flow, none of which is a system call.
2. **Session ⊃ process group ⊃ process**, and a session has at most one *foreground* group. Job control is entirely that sentence.
3. **A shell implements Ctrl-C by not being in the foreground group.** There is no handler and no forwarding — it hands the terminal to a job and steps back.

---

### Learning Objectives

By the end of Week 6, you should be able to:

1. Tokenise a command line on whitespace **and** operators, longest operator first.
2. Write a grammar for pipelines and redirections, and say which part owns which.
3. Reject bad syntax before forking anything.
4. Explain why `cd` **cannot** be an external command, and why `echo` is a builtin anyway.
5. Quantify what running an external command costs, and where the time goes.
6. Execute an *n*-stage pipeline with correct closes, and diagnose a hang from outside the process.
7. Report a pipeline's status, including **128 + signal**.
8. State what `fork`, `setpgid` and `setsid` do to a process's group, session and terminal.
9. **Say why a shell calls `setpgid` in both the parent and the child.**
10. Predict what the terminal does to a background process group for `read`, `write` and `tcsetattr`.
11. Explain why `tcsetpgrp` must be wrapped in `SIGTTOU` being ignored.
12. Use `kill(-pgid, sig)`, and say what the terminal driver does on Ctrl-C.
13. Build a job table and implement `jobs`, `fg` and `bg`.
14. **Use `WUNTRACED` and `WCONTINUED`**, and say what a shell without them does when a job stops.
15. Reap correctly given that `SIGCHLD` does not queue, and say why `getpgid` after `waitpid` fails.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L19 The Read Eval Print Loop]] | The loop; tokenising on operators; the grammar and who owns the redirections; **a builtin at under 5 µs against 955 µs for an external command**, with `fork` only 127 µs of it and **147 µs of it the dynamic linker**; pipelines; `128 + signal` |
| [[L20 Process Groups Sessions and the Terminal]] | Groups, sessions and the controlling terminal, **measured**; `setsid` losing the terminal; the `setpgid` race and why you call it twice; **what the terminal does to a background group — three operations, three different answers**; `kill(-pgid)`; orphaned groups; a shell's startup |
| [[L21 Job Control SIGCHLD and the Job Table]] | The job table; **`WUNTRACED` is what makes Ctrl-Z possible**; reaping in a handler against the loop, and why `SIGCHLD` does not queue; **`getpgid` after `waitpid` returns `ESRCH`**; `fg` hands over the terminal *before* the `SIGCONT` |
| [[LAB 6 Adding Job Control]] | A working shell with the job control removed. **Monday of Week 7** |
| `lab/tsh.c`, `lab/groups.c`, `lab/ttyctl.c`, `lab/groupsig.c`, `lab/Makefile` | The skeleton and L20's three experiments |
| [[PS 6 A Shell Parser and Executor]] | Tokeniser, parser, pipelines, redirections, builtins — **no job control**. Due **Friday of Week 7** |
| [[PROJECT 1 A Unix Shell]] | The complete shell. **Assigned Friday, due Week 9, 12.5%** |
| [[PROG201 Week6/assignments/QUIZ 6 Week 6 Tuesday\|QUIZ 6 Week 6 Tuesday]] | Ten minutes, covers **Week 5**, answer key printed |
| [[PROG201 Week6/resources/Reading Guide Week 6\|Reading Guide Week 6]] | **APUE Ch. 9**, which is the only good treatment of this anywhere |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Look at the process table.**

```
ps -o pid,ppid,pgid,sid,tpgid,stat,wchan,comm -t $(tty | sed 's|/dev/||')
```

Every bug this week produces is visible in that one line of output and invisible in your source:

| Symptom | What the table shows |
| --- | --- |
| `fg` does nothing | **`tpgid` is not the job's `pgid`** |
| Ctrl-C kills only part of a pipeline | **the stages have different `pgid`s** — the `setpgid` race |
| The shell hangs on Ctrl-Z | the child is **`T`**, the shell is **`S`** in `wait` — no `WUNTRACED` |
| A pipeline never finishes | the reader is in **`pipe_read`** — Week 1's missing `close` |
| The shell stopped itself | it is **`T`** and not in the foreground group — `tcsetpgrp` without `SIGTTOU` ignored |

**Five distinct bugs, one command**, and it is the same habit as Week 5's `ss`: the state that explains a process is usually not inside it.

---

### Assessment Reminder

**Labs and quizzes carry no weight** and are still required. **Quiz 6 is at the start of Tuesday's lecture and covers Week 5**; the answer key is printed in the paper.

**Project 1 is worth 12.5%** and is assigned this Friday, due Week 9. PS 6 and Lab 6 are two of its five parts and are yours to reuse in full.

> **Fall Break is the Monday**, so Lab 5 — Week 5's — is sat on the **Friday of this week,
> 16:00–17:50**, the term's only Friday lab. **Lab 6** covers this week and is sat on the **Monday
> of Week 7**, with Mondays resuming from there.

Labs and quizzes are tracked in [[_PROG 201 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 0 is half this week** — `fork`, `exec`, `waitpid`, status words, and `SIGCHLD` not queueing. **Week 1's `dup2` is the redirections and Week 2's `pipe` is the `|`**, closes and all; Lab 1 is L19 §5 with a loop around it. **Week 0 L03's async-signal-safety** decides where a shell may reap.

**Sideways:** **CS 201 Week 6 is the page table**, which is what `fork` copies and `exec` throws away — L19 §4's 127 µs against 779 µs is that distinction with a number on it.

**Forward:** **Week 7's filesystem** is what `cd`, `>` and PATH resolution are actually talking to. **Week 8's dynamic linker** is the 147 µs L19 §4 found between a static and a dynamic binary. **Project 1 is due in Week 9**, and Week 9 is where you would profile it properly.

---

*PROG 201 · Week 6 · © CSE Department*
