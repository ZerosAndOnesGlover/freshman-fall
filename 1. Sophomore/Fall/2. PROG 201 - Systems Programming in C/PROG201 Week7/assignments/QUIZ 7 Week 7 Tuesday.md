# PROG 201 · Quiz 7
## Administered: Tuesday, Week 7 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 6** — the shell, process groups, sessions, the controlling terminal, job control.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.
>
> **PS 6 is due Friday** and **Project 1 is due Week 9.** **Midterm 2 is the Monday of Week 8** and
> covers Weeks 4–7, so everything here is on it.

---

**Q1.** Your shell forks a child to run a command. What has changed about the child's process group, session and controlling terminal? Now the child calls `setpgid(0, 0)`. What changed?

&nbsp;

&nbsp;

---

**Q2.** A shell calls `setpgid` twice for every child — once in the parent, once in the child. Why is one not enough? Say what goes wrong in each direction.

&nbsp;

&nbsp;

---

**Q3.** A background process group tries three things: `read` from the terminal, `write` to it, and `tcsetattr` on it. What happens in each case, and which one depends on a terminal flag?

&nbsp;

&nbsp;

---

**Q4.** Your shell wraps every `tcsetpgrp` in `signal(SIGTTOU, SIG_IGN)` and back. Why? What happens if you leave it out?

&nbsp;

&nbsp;

---

**Q5.** You press Ctrl-Z and your shell stops responding for ever. Both the shell and the job are behaving correctly. What is missing, and what is each process doing?

&nbsp;

&nbsp;

---

**Q6.** Your shell reaps with `waitpid(-1, &st, WNOHANG|WUNTRACED)` and then calls `getpgid(p)` to find which job `p` belonged to. It never works. Why?

&nbsp;

&nbsp;

---

**Q7.** An external command costs about 955 µs through a shell and a builtin costs under 5 µs. Break the 955 µs down as far as you can, and name the two reasons `cd` is a builtin.

&nbsp;

&nbsp;

---
---

# Answer Key

*Mark your own. Be honest — nobody else will see this.*

---

**Q1.** After a plain `fork`: **nothing has changed** — the child inherits the process group, the session and the controlling terminal, so it is in the foreground exactly when the shell is.

After `setpgid(0, 0)`: a **new process group in the same session**, with the pgid equal to the pid, and **the child is now in the background** because the terminal's foreground group is still the shell's. *(L20 §2. `setsid()` would additionally make a new session and lose the terminal entirely — `tcgetpgrp` returns −1.)*

---

**Q2.** **It is a race.** If only the **child** calls it, the parent may `tcsetpgrp` to a group that does not exist yet. If only the **parent** calls it, the child may reach `execvp` first — and `setpgid` on a process that has already `exec`ed fails with `EACCES`, so the program runs in the shell's own group and a Ctrl-C then kills the shell too.

Both call it because **whichever runs first makes it true** and the other's call is a harmless no-op or a harmless failure. *(L20 §3, and APUE §9.4.)*

---

**Q3.** **`read` stops it with `SIGTTIN`** — always. **`write` succeeds** — because `TOSTOP` is clear by default, which is why background output interleaves with your prompt; set `TOSTOP` and it stops with `SIGTTOU`. **`tcsetattr` stops it with `SIGTTOU` regardless of `TOSTOP`**, because changing the terminal's mode changes it for the foreground process too.

So `write` is the one that depends on a flag. *(L20 §4, measured.)*

---

**Q4.** Because **`tcsetpgrp` counts as changing terminal state**, and the shell — at the instant it takes the terminal back from a job — is not the foreground group. So it would send itself `SIGTTOU` and **stop itself**.

Leave it out and the shell freezes the first time a foreground job finishes. `ps -o stat` shows the shell in state **`T`**. It is not a workaround; it is the documented way to use the call. *(L20 §4.)*

---

**Q5.** **`WUNTRACED` is missing** from the `waitpid` call. Without it, `waitpid` reports only *terminations*, and a stop is not a termination.

The job is in state **`T`** — stopped by the `SIGTSTP` the terminal driver sent to the foreground group. The shell is in state **`S`**, blocked in `waitpid` for a process that is never going to exit. **Neither is misbehaving**; the shell simply asked a question that cannot be answered. *(L21 §2.)*

---

**Q6.** Because **`waitpid` returning `p` means `p` has been reaped and no longer exists** — so `getpgid(p)` fails with `ESRCH` and returns −1, the job lookup fails, and the job is never marked done. `jobs` lists it as Running for ever while the process is genuinely gone.

The fix is to record every pid in the job and look up **by pid**. The rule: **after `waitpid` returns, the status is the only thing you still know about that process.** *(L21 §5. Same class as `stat`-then-`open`.)*

---

**Q7.** `fork` + `_exit` + `wait` is **127 µs**; adding `exec /bin/true` takes it to **779 µs**, so `exec` is about 650 µs — the ELF header, the segment mappings, and the dynamic linker. **147 µs of that is the linker**: the same trivial binary costs 679 µs dynamically linked and **532 µs statically**.

`cd` is a builtin for two reasons: **it cannot be anything else** — the working directory is per-process, so a child's `chdir` dies with the child — and it would cost 200× as much if it could. *(L19 §4.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L20 §2–§3 |
| **Q3, Q4** | **L20 §4** — and run `ttyctl` from the Lab 6 folder; it is ten seconds |
| **Q5, Q6** | **L21 §2 and §5** — you sat Lab 6 on Monday; check your own code |
| Q7 | L19 §4 |

**Q5 and Q6 are the ones that recur** — they are two of the five bugs `ps -o pid,pgid,tpgid,stat` will show you, and they are both in Project 1. **Midterm 2 covers Weeks 4–7**, so Q4's `SIGTTOU` and Q6's `ESRCH` are both fair game.

---

*PROG 201 · Week 7 · Quiz 7 · covers Week 6 · ungraded*
