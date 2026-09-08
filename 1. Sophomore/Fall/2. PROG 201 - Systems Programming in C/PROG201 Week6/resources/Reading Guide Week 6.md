# PROG 201 · Reading Guide · Week 6
## APUE Chapter 9, which is the only good chapter about this anywhere

---

**Week 6 has one essential reading and it is APUE Chapter 9.** Process relationships — groups, sessions, controlling terminals, orphaned process groups — are documented in `man` pages that assume you already understand them, and in textbooks that mention them in passing. Stevens wrote thirty pages that explain *why*, and nobody has improved on it.

**CS:APP §8.4–8.5 is the other one**, and it is where the `tsh` you are building comes from: the shell lab in that book is this project's ancestor, and its treatment of the `SIGCHLD` race is the clearest short version there is.

| Source | Read? | Why |
|---|---|---|
| **APUE Ch. 9** | **All of it** | Process groups, sessions, controlling terminals. This is L20 |
| **APUE §8.10** | **Read** | `system()`, and why writing it correctly is harder than it looks |
| **CS:APP §8.4–8.5** | **All of it** | Process control and signals, with the shell as the running example |
| **TLPI Ch. 34** | **All of it** | The Linux specifics, and the best account of orphaned process groups |
| TLPI Ch. 27 | Read | `exec`, and what survives it |
| TLPI §62.1–62.3 | Skim | Terminals. Enough to know `tcgetattr` exists and what `raw` means |
| **CS:APP shell lab handout** | **Optional but recommended** | Freely available; the same problem, differently staged |

---

## APUE Chapter 9 — the questions to hold

**§9.2 Process groups**

1. `getpgrp()` and `getpgid(pid)`. When would you use the second, and what does it return for a process that has just been reaped? *(L21 §5. There is a measurement.)*
2. Stevens says `setpgid` can only be used on the caller or one of its children, and only before the child `exec`s. **Work out from that pair of restrictions why a shell calls it twice**, and check against L20 §3.

**§9.5 Sessions**

3. `setsid` fails if the caller is already a process group leader. Why? Then write the two-line explanation of why a daemon forks *before* calling it.
4. A session leader that opens a terminal acquires it as a controlling terminal. Find the flag that prevents this, and say why a daemon wants it.

**§9.6 Controlling terminal**

5. `/dev/tty` is not a device; it is a name for "whatever my controlling terminal is". What does opening it do in a process that has none? *(`groups.c` prints the answer as −1 in a different column.)*
6. Stevens explains why the terminal generates signals for the **foreground** group only. Write down what a background process gets for `read`, `write` and `tcsetattr`, then check against `ttyctl`'s output. **One of the three will surprise you.**

**§9.8 Job control**

7. He lists what a shell must do for job control. Tick off which of them your Lab 6 shell does.
8. Find the paragraph on `SIGTTOU` and `tcsetpgrp`. It is three sentences and it explains the strangest lines in any shell.

**§9.10 Orphaned process groups**

9. Work through Figure 9.11. Then say what happens to `sleep 100` if you `exit` a shell while it is *stopped*, and what happens if it is *running*. They differ. *(L20 §6.)*

---

## CS:APP §8.5 — the signals chapter

10. §8.5.5's "safe" functions and §8.5.6's three rules for handlers. **Compare rule 2 with the reaping loop in L21 §3** — they are the same statement.
11. CS:APP shows a shell that loses `SIGCHLD`s. Reproduce the bug in your own before you read the fix.
12. §8.5.7, "Synchronizing flows to avoid nasty concurrency bugs", is about a race between adding a job to the table and reaping it. **Does your shell have that race?** Work it out from where your `reap` is called, not by testing.

---

## The Man Pages for This Week

| Page | The paragraph |
|---|---|
| **`man 2 setpgid`** | The restrictions — who may call it on whom, and until when. Both matter |
| **`man 2 waitpid`** | `WUNTRACED`, `WCONTINUED`, and the status macros in full |
| **`man 3 tcsetpgrp`** | Short, and every sentence is load-bearing. Read the `SIGTTOU` note twice |
| **`man 7 credentials`** | Process groups and sessions, defined precisely, in one page |
| `man 1 stty` | `tostop`, `intr`, `susp`. The terminal's side of L20 §4 |
| `man 3 glob` | For Project 1's globbing extension, if you take it |

**And two commands to live in this week:** `ps -o pid,ppid,pgid,sid,tpgid,stat,comm` shows every relationship in L20 at once, and `ps -o stat` alone tells you `T` (stopped), `S` (sleeping), `R`, `Z` and — the useful one — `+` for "in the foreground group".

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| `dash` source, `jobs.c` | 1,500 lines, and it is exactly what you are writing. The most readable real shell |
| `bash` source, `jobs.c` | 4,000 lines, and the difference is the whole of §7 in L21 |
| POSIX.1-2017, "Shell Command Language" | The grammar, formally. Section 2.10 is the yacc |
| Kernighan & Pike, *The Unix Programming Environment*, Ch. 3 | 1984, and still the best account of what a shell is *for* |
| Ritchie, *A Stream Input-Output System* (1984) | Where the terminal handling came from |

---

## The Habit for This Week

**Look at the process table.**

Week 5's habit was to look at the sockets. This one is its sibling and it is the single most useful debugging move in the whole course:

```
ps -o pid,ppid,pgid,sid,tpgid,stat,wchan,comm -t $(tty | sed 's|/dev/||')
```

Every bug in this week is visible there and invisible in your source:

- a job that will not come back to the foreground: **`tpgid` is not its `pgid`**;
- a pipeline that will not die on Ctrl-C: **its stages have different `pgid`s** — the `setpgid` race;
- a shell that hangs on Ctrl-Z: the child is **`T`** and the shell is **`S`** in `wait`;
- a pipeline that never finishes: the reader is in **`pipe_read`**, which is Week 1's missing `close`;
- a shell that stopped itself: **it is `T` and it is not in the foreground group** — a `tcsetpgrp` without `SIGTTOU` ignored.

**Five distinct bugs, one command.** Learn the column order once and you will use it for the rest of your career.

---

*PROG 201 · Week 6 · Reading Guide · © CSE Department*
