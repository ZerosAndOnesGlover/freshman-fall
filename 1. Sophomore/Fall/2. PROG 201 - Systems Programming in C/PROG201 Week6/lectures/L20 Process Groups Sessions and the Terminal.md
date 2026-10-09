# PROG 201 · Systems Programming in C
## Week 6 · Lecture 2 of 3
### Process Groups, Sessions, and the Controlling Terminal

*“I've seen [visual] editors like that, but I don't feel a need for them. I don't want to see the state of the file when I'm editing.”* — Ken Thompson, as summarized in Peter Salus, *A Quarter Century of UNIX* (1994)

---

**Reading:** APUE Ch. 9 · TLPI Ch. 34 · `man 2 setpgid`, `man 2 setsid`, `man 3 tcsetpgrp`, `man 7 credentials` · **Previous:** L19 · **Next:** L21 — job control

**Coursework:** 📝 **PS 6** released today, due Fri of Week 7 17:00 · 📋 **Project 1** released Fri this week, due Fri of Week 9 17:00 · 📝 **PS 5** due Fri this week 17:00 · 🔬 **Lab 5** Fri this week 16:00–17:50 · 🔬 **Lab 6** Mon of Week 7 15:00–16:50 · 📊 **Quiz 7** Tue of Week 7

---

## 1. The Problem Ctrl-C Poses

You type `ls -l /usr | grep bin | wc -l` and press Ctrl-C. **Three processes must die and your shell must not.** The kernel has to know which processes those are, and it cannot ask the shell — the shell is blocked in `waitpid` and the keypress arrives in a driver.

So the kernel needs a name for "the processes that are currently attached to this terminal", and it needs it to be a *set*, not a pid. That is what a **process group** is, and Week 0 L02 §5 mentioned them in passing. This lecture is what they are for.

Three levels, each a set of the one below:

```
session          one login, one controlling terminal
 ├─ process group   one job:  ls | grep | wc
 │   ├─ process        ls
 │   ├─ process        grep
 │   └─ process        wc
 └─ process group   another job: sleep 100 &
     └─ process        sleep
```

**A session has at most one *foreground* process group.** Everything else in it is background. That single fact is the whole of job control.

---

## 2. What `fork`, `setpgid` and `setsid` Actually Do

`groups.c` prints its identity in four situations. Every column is `getpid`, `getppid`, `getpgrp`, `getsid`, and `tcgetpgrp("/dev/tty")` — the terminal's idea of which group is in front:

```
the shell's child      pid=1092347 ppid=1092345 pgid=1092347 sid=1092347 tcpgrp=1092347  <- foreground
  fork, nothing else   pid=1092348 ppid=1092347 pgid=1092347 sid=1092347 tcpgrp=1092347  <- foreground
  after setpgid(0,0)   pid=1092349 ppid=1092347 pgid=1092349 sid=1092347 tcpgrp=1092347
  after setsid()       pid=1092350 ppid=1092347 pgid=1092350 sid=1092350 tcpgrp=-1
  pipeline stage 0     pid=1092351 ppid=1092347 pgid=1092351 sid=1092347 tcpgrp=1092347
  pipeline stage 1     pid=1092352 ppid=1092347 pgid=1092351 sid=1092347 tcpgrp=1092347
```

Read it row by row:

**`fork` changes nothing.** The child is in its parent's process group and session, and is therefore in the foreground exactly when its parent is. This is why a plain `fork` in a program you write inherits Ctrl-C for free — and why a shell that does nothing else cannot separate a background job from itself.

**`setpgid(0, 0)` makes a new process group in the same session.** The pgid becomes the pid: **the process is now a group leader**. And notice what happened to the last column — `tcpgrp` is still the parent's group, so this process is now in the **background**. §4 is what that costs it.

**`setsid()` makes a new session, a new group, and — the column nobody expects — `tcgetpgrp` returns −1.** A new session has **no controlling terminal at all**. This is exactly how a daemon detaches: `fork`, `setsid`, and it can never again be killed by a Ctrl-C or hung up on when the terminal closes. It is also why `setsid` fails with `EPERM` if you are already a group leader — a session leader must be a group leader of a *new* group, and the kernel refuses to move a leader.

**A pipeline is one group.** Stages 0 and 1 have different pids and the same pgid, and that pgid is stage 0's pid. **The first process of a pipeline becomes the group leader and every later stage joins it.** That is the whole of how `ls | grep | wc` becomes a thing Ctrl-C can address.

---

## 3. Setting the Group Is a Race, and You Fix It by Doing It Twice

The shell wants the child in a new group. Two candidates:

```c
pid_t k = fork();
if (k == 0) { setpgid(0, 0); execvp(...); }   /* the child does it */
```
```c
pid_t k = fork();
if (k > 0)  { setpgid(k, k); }                /* the parent does it */
```

**Both are wrong on their own, and the reason is a race.** If only the child does it, the parent may call `tcsetpgrp(tty, k)` before the child has run at all — and `tcsetpgrp` on a group that does not exist yet fails. If only the parent does it, the child may reach `execvp` and run before the parent's `setpgid` lands, so the program starts in the wrong group and a Ctrl-C in that window goes to the wrong place.

**The fix is to do it in both**, which is what every real shell does:

```c
pid_t k = fork();
if (k == 0) { setpgid(0, pgid); ... execvp(...); }
setpgid(k, pgid);                       /* and again, in the parent */
```

One of the two calls succeeds and the other is a harmless no-op, and by the time both processes are past that line the group definitely exists. **The parent must tolerate `EACCES`** — `setpgid` on a child that has already `exec`ed is refused — so do not check the return value into an error path. It is one of the very few places in Unix where the correct code is "call it twice and ignore one failure", and it is in APUE §9.4 for exactly this reason.

---

## 4. What the Terminal Does to a Background Group

A terminal has one foreground process group, and it enforces it. `ttyctl.c` runs three operations in a group that is *not* the foreground one:

```
TOSTOP is clear by default

a process group that is NOT the foreground one:
  read() from the terminal                   STOPPED by Stopped (tty input)
  (background wrote this)
  write() to the terminal                    exited 0
  tcsetattr() on the terminal                STOPPED by Stopped (tty output)

now with TOSTOP set:
  write() to the terminal                    STOPPED by Stopped (tty output)
```

**Three different answers to what looks like one question**, and the asymmetry is deliberate:

**Reading is always forbidden.** A background process that reads the terminal gets **`SIGTTIN`** and stops, because two processes competing for your keystrokes is not a thing anyone can use. This is why `cat &` stops immediately, and the shell reports `[1]+ Stopped`.

**Writing is allowed by default.** A background process that writes gets through — which is why a background job's output interleaves with your prompt, messily, and why nobody has fixed that in fifty years. `TOSTOP` is the terminal flag that changes it, and with it set, writing gets **`SIGTTOU`** and stops too. It is off by default because most people would rather have the mess than have every background job stop.

**Changing terminal settings is always forbidden.** `tcsetattr` from a background group gets `SIGTTOU` **regardless of `TOSTOP`**, because a background process changing the terminal's mode out from under the foreground one is unambiguously wrong.

**And `tcsetpgrp` is in that last category** — which produces the strangest line in any shell:

```c
signal(SIGTTOU, SIG_IGN);
tcsetpgrp(shell_tty, pgid);       /* hand the terminal to the job */
signal(SIGTTOU, SIG_DFL);
```

**A shell taking the terminal back from a job it just stopped is, at that instant, a background process changing terminal state — so it would stop itself.** Ignoring `SIGTTOU` around every `tcsetpgrp` is not a workaround; it is the documented way to use the call.

---

## 5. Signalling a Group

```c
kill(pid,   SIGINT);    /* one process           */
kill(-pgid, SIGINT);    /* every process in that group */
kill(0,     SIGINT);    /* every process in MY group -- including me */
```

`groupsig.c` makes three processes in one group and one in another:

```
group A = 1092545 (3 processes), group B = 1092548 (1 process)

kill(1092546, SIGINT)   -- one process by pid:
  A[0] pid 1092545: still running
  A[1] pid 1092546: Interrupt
  A[2] pid 1092547: still running

kill(-1092545, SIGINT)  -- the whole group (note the minus):
  A[0] pid 1092545: Interrupt
  A[1] pid 1092546: already reaped
  A[2] pid 1092547: Interrupt
  B    pid 1092548: still running   <- a different group, untouched
```

**The minus sign is the entire difference**, and it is the single most useful piece of syntax in this lecture. `kill -TERM -1234` from the command line means the same thing, which is why `kill -9 -$$` is a thing people type and why they should be careful with it.

**Ctrl-C is `kill(-foreground_pgid, SIGINT)`, sent by the terminal driver.** Ctrl-Z is the same with `SIGTSTP`, Ctrl-\ with `SIGQUIT`. The characters are configurable (`stty intr`, `susp`, `quit`), the mechanism is not, and **the shell does nothing at all** — it has ignored those signals for itself and the kernel delivers them to whichever group `tcsetpgrp` last named.

That is the design worth stopping on. **A shell implements Ctrl-C by not being in the foreground group.** There is no handler, no forwarding, no bookkeeping. It puts the job in front and steps back.

---

## 6. Orphaned Process Groups

A process group is **orphaned** when no member has a parent in a *different* group of the same session — that is, when the shell that was managing it has gone.

POSIX requires that if such a group contains a stopped process, **every process in it is sent `SIGHUP` followed by `SIGCONT`**. Otherwise you would have processes stopped forever with nothing left that could continue them.

Two consequences you meet in practice:

- **Closing a terminal `SIGHUP`s the session leader**, the shell hangs up its jobs, and they die. `nohup` and `disown` are the two ways out — `nohup` ignores the signal, `disown` removes the job from the shell's table so it is never signalled.
- **A background job whose shell exits keeps running** if it is not stopped, gets reparented to `init`/`systemd` (Week 0 L02 §5's measurement), and its process group becomes orphaned but harmless.

`setsid` in a daemon is the deliberate version of all of this: no controlling terminal, so no `SIGHUP`, so nothing to survive.

---

## 7. The Shell's Own Startup

Before a shell can manage anyone, it has to establish itself. The sequence, and every line is defensive:

```c
while (tcgetpgrp(tty) != (shell_pgid = getpgrp()))
    kill(-shell_pgid, SIGTTIN);            /* not in front yet: stop and wait */

signal(SIGINT,  SIG_IGN);                  /* the shell must survive Ctrl-C  */
signal(SIGQUIT, SIG_IGN);
signal(SIGTSTP, SIG_IGN);                  /* ...and Ctrl-Z                  */
signal(SIGTTIN, SIG_IGN);
signal(SIGTTOU, SIG_IGN);

shell_pgid = getpid();
if (getpgrp() != shell_pgid)               /* may already be a leader        */
    setpgid(shell_pgid, shell_pgid);
tcsetpgrp(tty, shell_pgid);                /* claim the terminal             */
tcgetattr(tty, &shell_modes);              /* remember how it was            */
```

**The loop at the top is not paranoia.** A shell started in the background — from another shell, or by a test harness — must not start reading the terminal, so it stops itself with `SIGTTIN` until somebody foregrounds it. That is the same mechanism as §4, used deliberately on itself.

**The `getpgrp() != shell_pgid` check is load-bearing too**, and it was found by testing rather than by reading: a shell launched under a pseudo-terminal is already a session leader, and `setpgid` on a session leader fails with `EPERM`. A shell that checks the return value and exits will not run under `script`, under `pty.fork()`, or as a login shell.

**Saving the terminal modes matters** because a job may leave the terminal in a strange state — `vi` exits badly, and your shell restores it. It is why `reset` exists for the cases where the shell did not.

---

## Summary

- **Session ⊃ process group ⊃ process.** A session has at most one **foreground** process group; everything else is background.
- **`fork` inherits the group and session.** `setpgid(0,0)` makes a new group in the same session — and puts you in the background. **`setsid()` makes a new session and loses the controlling terminal entirely** (`tcgetpgrp` = −1), which is how a daemon detaches.
- **A pipeline is one process group**, led by its first stage.
- **Call `setpgid` in both the parent and the child.** It is a race otherwise, and one of the two calls is always a harmless failure.
- The terminal's rules for a background group: **`read` always stops you (`SIGTTIN`); `write` does not, unless `TOSTOP`; `tcsetattr` always does (`SIGTTOU`)**.
- **`tcsetpgrp` counts as changing terminal state**, so a shell must ignore `SIGTTOU` around it or stop itself.
- **`kill(-pgid, sig)` signals a group.** Ctrl-C is the terminal driver doing exactly that to the foreground group; **the shell implements Ctrl-C by not being in that group.**
- An **orphaned** process group with a stopped member is sent `SIGHUP` + `SIGCONT` by the kernel.
- A shell's startup **waits to be foregrounded, ignores five signals, takes its own group, claims the terminal and saves its modes** — and must tolerate already being a session leader.

---

## Exercises

1. Run `cat &` in `bash`. What happens, and which signal? Now run `echo hello &` and explain why that one works.
2. `stty tostop`, then run a chatty command in the background. Undo it with `stty -tostop`. Which of §4's rows did you just change?
3. Write the daemon four-liner — `fork`, `setsid`, `fork` again, `chdir("/")` — and explain what the **second** `fork` is for. *(It is about §2's last sentence.)*
4. From one terminal, find the pgid of a pipeline running in another, and `kill -STOP` the whole group. Then continue it. What did the other terminal show?
5. Delete the parent's `setpgid` from `tsh.c` and run `sleep 5` a hundred times in a loop, checking `getpgid` each time. How often does the race bite?
6. Remove the `signal(SIGTTOU, SIG_IGN)` from around `tcsetpgrp`. What does the shell do the first time a job stops, and how would you diagnose it from `ps` alone?
7. Start a shell in the background (`./tsh &`) and watch it stop itself. Which line of §7 did that, and what does `ps -o stat` show?

---

*PROG 201 · Week 6 · L20 · © CSE Department*
