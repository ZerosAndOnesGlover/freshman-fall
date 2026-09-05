# PROG 201 · Reading Guide · Week 0
## APUE Chapters 1–8, and what to actually do with them

---

The curriculum sets **"Read: Stevens & Rago Ch. 1–8"** for Week 0. That is about 300 pages, and reading it end to end in a ten-day week is neither possible nor useful. **This guide says which parts are Week 0, which are Week 1, and which are reference material you should know how to find rather than know.**

| Chapter | Now? | Why |
|---|---|---|
| **1. UNIX System Overview** | **Read** | 30 pages, and it is the map of the whole course |
| 2. Standardization and Implementations | *Skim* | Know that POSIX exists and what "implementation-defined" means. Come back when something differs between machines |
| 3. File I/O | **Week 1** | This is Week 1's lecture material. Reading it now is not wasted, but it is not this week |
| 4. Files and Directories | Week 7 | `stat`, permissions, links. Week 7 |
| **5. Standard I/O Library** | **§5.4 only** | Buffering. Twelve pages, and it explains L01 §6 |
| 6. System Data Files | Reference | `/etc/passwd`, `getpwnam`. Look it up when you need it |
| **7. Process Environment** | **Read** | `exit` vs `_exit`, `atexit`, the memory layout, `setjmp` |
| **8. Process Control** | **Read twice** | `fork`, `exec`, `wait`, zombies. **This is Week 0** |

**If you have three hours this week:** Chapter 8, then Chapter 1, then §5.4, then Chapter 7.

---

## Chapter 1 — read for the shape, not the detail

Stevens opens with a whole operating system in thirty pages, and the value is in seeing which pieces exist before you meet any of them properly.

**Questions to hold while reading:**

1. §1.5 says a file descriptor is "a small non-negative integer". *Small* is doing real work in that sentence. Why can it be small — what is it an index into? *(You are answering Week 1's opening question a week early. Write your guess down; you will find out whether it was right on the Tuesday.)*
2. §1.6 introduces the program/process distinction. Give an example of one program and four processes, and one process that runs three programs in sequence.
3. §1.7 lists the error conventions. Which one of `errno`, `perror` and `strerror` is safe to call in a signal handler? *(L03 §4. The answer is not obvious and it is worth checking against `man 7 signal-safety` rather than guessing.)*

---

## Chapter 8 — the chapter this week is built on

Read **§8.1–8.6 closely** (`fork`, `vfork`, `exit`, `wait`, `waitpid`), then **§8.9–8.10** (`exec`, and the seven `exec` functions), then **§8.13** if you have time. §8.11–8.12 (set-user-ID, interpreter files) are Week 7 and Week 10 material.

**Questions:**

4. §8.3, Figure 8.1: run Stevens' `fork` example yourself, once to a terminal and once through a pipe. **You will get different output.** Explain it before you read his explanation.
5. §8.5 gives eight rules for what happens when a parent or child terminates. Reduce them to two sentences: one about the parent dying first, one about the child dying first.
6. §8.6 distinguishes `wait` from `waitpid`. **What can `waitpid` do that `wait` cannot?** Name three things. *(One of them is the whole reason Lab 0 works.)*
7. Stevens says an orphan is inherited by `init`, PID 1. **Test it.** If you get a different number on your machine, do not assume the book is wrong or that you are — find out what the number is. *(L02 §5. This is the most instructive ten minutes in the chapter.)*
8. §8.10, Figure 8.15: the seven `exec` functions differ in three dimensions. Draw the 2×2×2 table and mark which of the eight cells does not exist.

---

## §5.4 — twelve pages that explain a bug you will meet this week

Three buffering modes: fully buffered, line buffered, unbuffered. Which one `stdout` gets **depends on whether it is a terminal**, and is decided the first time you write to it.

9. Why is `stderr` never fully buffered? Give the design reason, not the standard's wording.
10. `setvbuf` lets you choose. Name one situation where forcing `_IONBF` on `stdout` is right, and one where it would be a serious performance mistake.
11. **Connect it to L01 §6:** you now have the mechanism for why `./prog | cat` printed twice. Write the two-sentence version you would give in a code review.

---

## Chapter 7 — environment and termination

Read **§7.3 (`exit`, `_exit`, `_Exit`)**, **§7.6 (environment variables)** and **§7.10 (memory layout)**. §7.11 (`setjmp`/`longjmp`) is worth reading because Week 10 abuses it, but not this week.

12. §7.3: `exit`, `_exit` and `_Exit` differ in what they do on the way out. **Which one must the child call after a failed `exec`, and what breaks if it calls the wrong one?** *(PS 0 Q1(d).)*
13. §7.10's memory layout — text, data, bss, heap, stack — is the same picture CS 201 draws for the address space. Read `/proc/self/maps` and find all five. Which of them does `fork()` mark copy-on-write?

---

## Where to Go Deeper

**Kerrisk, TLPI** — the Linux-specific answers Stevens deliberately does not give:

| TLPI | Topic | When |
|---|---|---|
| Ch. 24–26 | Process creation, termination, monitoring | **This week** — the Linux details behind APUE Ch. 8 |
| Ch. 20–22 | Signals: three chapters, and worth all three | **This week**, for L03 |
| Ch. 27–28 | `exec`, and process creation/execution details | This week |
| Ch. 34 | Process groups, sessions, job control | Week 6 |

**The man pages you should have read by Friday:** `fork(2)`, `execve(2)`, `wait(2)`, `kill(2)`, `sigaction(2)`, `signal(7)`, **`signal-safety(7)`**, `credentials(7)`.

`man 7 signal-safety` is short, is a list, and is the single most consulted page in this course. Read it once now so that you know what is on it; you will look things up in it for the next thirteen weeks.

---

## The One Habit This Guide Is Trying To Build

**When the book and the machine disagree, find out why — do not pick a side.**

Question 7 is the deliberate case. APUE says PID 1; your machine says something else; both statements are true of the systems they describe, and the interesting content is entirely in the gap. That gap is where every hard bug in systems programming lives, and the reflex of going to look rather than assuming is the thing this course is actually teaching.

---

*PROG 201 · Week 0 · Reading Guide · © CSE Department*
