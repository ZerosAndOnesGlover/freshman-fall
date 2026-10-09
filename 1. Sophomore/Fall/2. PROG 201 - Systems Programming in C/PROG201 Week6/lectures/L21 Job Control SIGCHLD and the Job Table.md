# PROG 201 · Systems Programming in C
## Week 6 · Lecture 3 of 3
### Job Control: `SIGCHLD`, the Job Table, and `fg`/`bg`/`jobs`

*“In man-machine symbiosis, it is man who must adjust: The machines can't.”* — Alan Perlis, "Epigrams on Programming" (1982), #99

---

**Reading:** APUE §9.8, §10.7 · CS:APP §8.5.5–8.5.6 · TLPI §34.7 · `man 2 waitpid`, `man 3 tcsetpgrp` · **Previous:** L20 · **Next:** Lab 6 — add job control, **Monday of Week 7**

**Coursework:** 📋 **Project 1** released Fri this week, due Fri of Week 9 17:00 · 📝 **PS 5** due Fri this week 17:00 · 🔬 **Lab 5** Fri this week 16:00–17:50 · 🔬 **Lab 6** Mon of Week 7 15:00–16:50 · 📊 **Quiz 7** Tue of Week 7 · 📝 **PS 7** released Wed of Week 7, due Fri of Week 8 17:00

---

## 1. A Job Is a Process Group With a Name

L20 gave the kernel's structure. A shell adds one thing on top of it: **a number you can type.**

```c
struct job {
    int   id;                     /* what you type after % */
    pid_t pgid;                   /* what the kernel understands */
    int   state;                  /* RUNNING or STOPPED */
    int   nproc;                  /* how many are still alive */
    pid_t pid[MAXSTAGE];          /* every pid -- section 5 */
    int   npid;
    char  cmdline[1024];          /* to print in `jobs` */
};
```

`%1` is a shell-side fiction; `kill(-pgid, ...)` is what actually happens. Everything `jobs`, `fg` and `bg` do is translate between the two.

**The `cmdline` field is why L19 §2 told you to keep a copy of the line.** By the time you have a pgid, the tokeniser has filled the original buffer with NULs.

---

## 2. `waitpid` Has Two Options You Have Not Used

Week 0 used `waitpid` to find out that a child ended. Job control needs to know that a child **stopped** or **continued**, which are not endings:

| Option | Reports | Test |
| --- | --- | --- |
| (none) | the child terminated | `WIFEXITED`, `WIFSIGNALED` |
| **`WUNTRACED`** | the child **stopped** | `WIFSTOPPED`, `WSTOPSIG` |
| **`WCONTINUED`** | the child was **continued** by `SIGCONT` | `WIFCONTINUED` |
| `WNOHANG` | return 0 rather than blocking | — |

**A shell without `WUNTRACED` cannot implement Ctrl-Z.** The child stops, `waitpid` does not return, and the shell hangs waiting for a process that is never going to exit. That is the single most common way a first shell fails, and the symptom — "Ctrl-Z makes my shell freeze" — names the missing flag exactly.

So the shell's `waitpid` is always the same call:

```c
pid_t p = waitpid(-1, &st, WUNTRACED | WCONTINUED | WNOHANG);
```

with `WNOHANG` dropped when it wants to block for a foreground job.

---

## 3. Where to Reap: a Handler, or the Loop

Two designs, and the choice is not obvious.

**In a `SIGCHLD` handler.** The shell learns immediately, which is what you want for a background job that finishes while you are typing. And the handler is subject to every rule from Week 0 L03 §4: async-signal-safe functions only, so **no `printf`** — a handler that reports `[1]+ Done` with `printf` is calling a non-reentrant function from a signal, and Week 0 measured what that does to output (93 of 138 lines damaged).

**In the main loop, before the prompt.** Simple, debuggable, and everything is allowed. The cost is that a job which finishes while you are typing is not reported until you press Enter — **which is exactly what `bash` does**, and why job completions appear with your next prompt rather than mid-line.

The teaching shell reaps in the loop for that reason:

```c
for (;;) {
    reap(0);                       /* WNOHANG: report anything finished */
    print_prompt();
    read_line();
    ...
}
```

**Whichever you choose, `SIGCHLD` is the trap that catches everyone**, and it is Week 0 L03 §2's non-queueing result in a new place: **standard signals do not queue.** Three children exiting while you are inside the handler produce **one** `SIGCHLD`, not three. So a handler that reaps one child loses two, and they become zombies for ever.

```c
static void on_sigchld(int sig)
{
    (void) sig;
    int save = errno;
    while (waitpid(-1, NULL, WNOHANG | WUNTRACED | WCONTINUED) > 0)
        ;                          /* the LOOP is the whole point */
    errno = save;
}
```

**The loop, and saving `errno`.** `waitpid` sets `errno` on failure, and a handler that runs between a failing call and its `errno` check corrupts it — Week 0 L03 §4's rule, and it costs two lines.

---

## 4. Waiting for a Foreground Job

A foreground job ends in one of two ways, and the shell must handle both:

```c
static void wait_foreground(struct job *j)
{
    reap(j->pgid);                          /* blocks until it stops or dies */
    signal(SIGTTOU, SIG_IGN);
    tcsetpgrp(shell_tty, shell_pgid);       /* take the terminal back */
    tcsetattr(shell_tty, TCSADRAIN, &shell_modes);
    signal(SIGTTOU, SIG_DFL);
}
```

Three things happen after the wait and all three are necessary:

- **`tcsetpgrp` back to the shell**, or the shell is typing into a terminal owned by somebody else. Wrapped in `SIG_IGN` for `SIGTTOU` — L20 §4.
- **Restore the terminal modes**, because the job may have left them in a mess. This is why `vi` crashing does not usually leave your shell unusable.
- And the wait itself must accept **stopped** as an ending. `WUNTRACED` again.

---

## 5. A Bug Worth Meeting Deliberately

The obvious way to find which job a reaped process belonged to:

```c
pid_t p = waitpid(-1, &st, ...);
pid_t pg = getpgid(p);              /* <- and here is the bug */
struct job *j = job_by_pgid(pg);
```

**It compiles, it looks right, and it silently does not work.** `waitpid` has just reaped `p`, so `p` no longer exists — `getpgid` returns −1 with `ESRCH`, the lookup fails, and the job is never marked done. The symptom in the reference shell was precise and unhelpful: `kill %1` worked, the process really died, and `jobs` kept listing it as Running for ever.

The fix is to record the pids when you launch the job and look up by pid:

```c
struct job *j = job_by_pid(p);      /* the job remembers its own pids */
pid_t pg = j->pgid;
```

**The general rule: after `waitpid` returns, the only thing you know about that process is its status.** Every other query — its group, its parent, anything in `/proc` — is a question about a process that has ceased to exist. This is the same class as Week 1's `stat`-then-`open`, and it is on the problem set for that reason.

---

## 6. `fg` and `bg`

Both are three or four lines, and the ordering inside them is the lecture:

```c
if (fg) {
    signal(SIGTTOU, SIG_IGN);
    tcsetpgrp(shell_tty, j->pgid);      /* 1. hand over the terminal */
    signal(SIGTTOU, SIG_DFL);
}
j->state = JOB_RUNNING;
kill(-j->pgid, SIGCONT);                /* 2. THEN continue it */
if (fg) wait_foreground(j);             /* 3. and wait */
```

**The terminal is handed over before the `SIGCONT`, not after.** A job that was stopped by `SIGTTIN` will immediately try to read again the moment it continues; if it is not the foreground group at that instant, it stops again and `fg` appears to do nothing.

**`bg` is the same minus the terminal and the wait.** It sends `SIGCONT` and returns to the prompt, and the job runs in the background — where, per L20 §4, it may write but must not read.

**`SIGCONT` is unusual and worth knowing about**: it continues a stopped process *even if it is blocked or ignored*, because a process that could block its own continuation would be unstoppable-and-unstartable. It is the only signal with that property besides `SIGKILL`'s undeliverability rules.

Everything working, from the reference shell driven over a pseudo-terminal:

```
tsh> sleep 20 | cat | cat &
[1] 1093332
tsh> jobs
[1]+  Running                sleep 20 | cat | cat &
tsh> sleep 20 | cat
tsh> ^Cecho still alive
still alive
tsh> kill %1
tsh> jobs
[1]+  Done                   sleep 20 | cat | cat &
```

**A three-stage pipeline is one job**, Ctrl-C killed the foreground one and the shell survived, and `kill %1` reached a group by its shell-side name.

---

## 7. What `bash` Does That This Does Not

| | the teaching shell | `bash` |
| --- | --- | --- |
| Job ids | `%1`, `%2` | also `%+`, `%-`, `%str`, `%?str` |
| Reporting | at the next prompt | the same, and `set -b` makes it immediate |
| `wait` builtin | no | yes, and it is how scripts synchronise |
| `disown` | no | removes a job so `SIGHUP` never reaches it |
| Nested job control | no | `bash -i` inside `bash` manages its own session |
| `jobs -p`, `-l` | no | pids, for scripts |
| Exit with stopped jobs | just exits | warns once, then exits |

**The last row is worth implementing** even in a small shell: exiting with stopped jobs leaves processes stopped in an orphaned group, and L20 §6 says the kernel will `SIGHUP`+`SIGCONT` them — so they die, in a way the user did not ask for and cannot see. One line of warning is the difference between a shell and a toy.

---

## Summary

- A **job is a process group with a shell-side number**; `%1` is a fiction, `kill(-pgid, ...)` is the reality.
- **`WUNTRACED` and `WCONTINUED`** are what make Ctrl-Z possible. A shell without `WUNTRACED` hangs the first time a job stops.
- **Reap in a loop, not once** — `SIGCHLD` does not queue (Week 0 L03 §2), so three exits give one signal.
- A `SIGCHLD` handler must be **async-signal-safe** and must **save and restore `errno`**. Reaping in the main loop instead is legitimate, and is why `bash` reports completions at the next prompt.
- After a foreground job: **`tcsetpgrp` back, restore the terminal modes**, both with `SIGTTOU` ignored.
- **`getpgid` on a just-reaped pid returns `ESRCH`.** Record the pids in the job. The general rule: after `waitpid`, the only thing you still know is the status.
- **`fg` hands over the terminal *before* `SIGCONT`**, or a job stopped by `SIGTTIN` stops again immediately.
- Warn before exiting with stopped jobs — the kernel will `SIGHUP` them.

---

## Exercises

1. Remove `WUNTRACED` from your shell's `waitpid` and press Ctrl-Z. Describe exactly what the shell does and what `ps -o stat` says about both processes.
2. Write the `SIGCHLD` handler with `printf` in it and start twenty background jobs that all finish at once. What does the output look like? *(Week 0 L03 §4 measured this.)*
3. Reap one child per `SIGCHLD` instead of looping. Start ten background `true`s at once and count the zombies with `ps`.
4. Swap the order in `fg` so that `SIGCONT` comes before `tcsetpgrp`, and use it on a job stopped by `SIGTTIN` (`cat &`, then `fg`). What happens, and why is it intermittent?
5. Implement `disown`. Then close the terminal and check the job is still running with `ps -o pid,ppid,stat`. Who is its parent now?
6. Add the "there are stopped jobs" warning on exit. Then exit anyway, and find out what happened to them.
7. Run `jobs` inside `$(...)` in `bash`: `echo $(jobs)`. It prints nothing. Work out why, from L20 §2. *(The answer is one word, and it is about subshells.)*

---

*PROG 201 · Week 6 · L21 · © CSE Department*
