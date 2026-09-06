# PROG 201 · Quiz 1
## Administered: Tuesday, Week 1 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 0** — the process model, `fork`/`exec`/`wait`, zombies and orphans, and signals.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room — the point
> is to find out what has not landed while there is still a term left to fix it.
>
> Do not look at the key first. It costs you the only thing the exercise is for.

---

**Q1.** `fork()` returns three different kinds of value. Give all three and say what each means.

&nbsp;

&nbsp;

---

**Q2.** A child calls `_exit(7)` and the parent has not called `wait()` yet. What state is the child in, and name two things the kernel is still holding for it.

&nbsp;

&nbsp;

---

**Q3.** `waitpid` gives you `status == 0x000b`. How did the child end, and what does `WEXITSTATUS(status)` return?

&nbsp;

&nbsp;

---

**Q4.** Five thousand `SIGUSR1` are sent to a process that has them blocked. It then unblocks. How many times does the handler run?

&nbsp;

&nbsp;

---

**Q5.** Name two things a signal handler is allowed to do, and one common call it is not.

&nbsp;

&nbsp;

---

**Q6.** Why is `while (!flag) pause();` wrong, and what replaces it?

&nbsp;

&nbsp;

---

**Q7.** A parent exits before its child. What is the child's `getppid()` afterwards — and what is it on *these* machines?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **`-1`** — the fork failed and there is no child; `errno` is `EAGAIN` (out of processes) or `ENOMEM`. **`0`** — you are in the child. **`> 0`** — you are in the parent, and the value is the child's PID.

*The asymmetry is deliberate: the parent needs the child's PID because it is the only handle it will get; the child can call `getppid()`.*

---

**Q2.** **Zombie** (`Z` in `ps`, `State: Z (zombie)` in `/proc`). Still held: **the PID**, **the exit status**, and the accumulated resource usage. **Not** held: the address space, the file descriptors, the stack — `ps` shows `RSS 0 VSZ 0`.

---

**Q3.** `0x000b` has a zero high byte and 11 in the low bits, so the child was **killed by signal 11, `SIGSEGV`** — `WIFSIGNALED` is true, `WTERMSIG` is 11. **`WEXITSTATUS` returns 0**, which is meaningless here: reading it without checking `WIFEXITED` first reports a crashed child as a clean success.

*(Had the core-dump bit been set it would read `0x008b`.)*

---

**Q4.** **Once.** A pending standard signal is one bit; the other 4,999 found it already set. Measured in L03 §3: 5,000 sent, handler ran once. `SIGRTMIN` would have queued all 5,000 — up to `RLIMIT_SIGPENDING`, past which they are dropped and `kill()` still returns 0.

---

**Q5.** **Allowed:** set a `volatile sig_atomic_t` flag; call an async-signal-safe function (`write`, `waitpid`, `kill`, `_exit`); save and restore `errno`. **Not:** `printf` — nor `malloc`, `free` or `exit`. The list is `man 7 signal-safety`: 192 functions, and none of those four is on it.

---

**Q6.** The signal can arrive **between the test and the `pause()`**. The handler runs, sets the flag, returns — and `pause()` then blocks waiting for a signal that has already been delivered. Replace it with **`sigsuspend`** (block the signal first, and let `sigsuspend` unblock-and-wait atomically), a **self-pipe**, or **`signalfd`**.

---

**Q7.** POSIX: the child is reparented to an **implementation-defined system process**. APUE names `init`, PID 1. **On these machines it is `systemd --user`, PID 257510**, because it sets `PR_SET_CHILD_SUBREAPER` — so `getppid() == 1` is the wrong test for "am I orphaned".

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L01 §2 and L02 §2 |
| **Q3** | **L02 §3** — and redo the table by hand. This is on the Midterm |
| Q4, Q5 | L03 §3 and §4 |
| **Q6** | **L03 §7** — Lab 0's main loop depends on it |
| Q7 | L02 §5 |

**Q3 and Q6 are the ones that recur.** Week 6's shell decodes status words constantly, and every long-running program in this course waits for signals. If either was shaky, fix it this week rather than in Week 8.

---

*PROG 201 · Week 1 · Quiz 1 · covers Week 0 · ungraded*
