# PROG 201 · Systems Programming in C
## Week 0 · Lecture 2 of 3
### Waiting: Zombies, Orphans, and the Process Table

---

**Reading:** APUE §8.5–8.6, §9.2–9.5 · **Previous:** L01, `fork` and `exec` · **Next:** L03, signals

---

## 1. The Question `exit()` Leaves Open

A process ends by calling `_exit(status)` — or by being killed, which the kernel treats as a different ending with a different encoding. Either way, **something has to survive it**: the answer to "how did it go?"

That answer has exactly one reader: the parent. And the parent may not be ready to read it at the moment the child ends. So the kernel keeps the answer, **and to keep the answer it has to keep the process**.

> **This is the whole idea of the zombie, and it is not a bug or an accident.** It is the only design
> that makes `exit status` meaningful at all. The alternative — discard the status when the process
> dies — would mean a parent could never reliably learn how its child finished.

---

## 2. What a Zombie Actually Is

`zshow.c` forks a child that immediately calls `_exit(42)`, then reads the child's `/proc` entry one second later:

```
Name:	zshow
State:	Z (zombie)
Threads:	1
```

**Look at what is missing.** A live process's `status` file carries `VmSize`, `VmRSS`, `VmData`, `VmStk` — a dozen memory lines. A zombie has **none of them**, because it has no address space: the pages, the mappings, the file descriptors, the stack are all gone, freed at `exit`. `ps` agrees:

```
    PID    PPID STAT   RSS    VSZ COMMAND
 402541  402540 Z        0      0 zombie
 402542  402540 Z        0      0 zombie
 402543  402540 Z        0      0 zombie
```

**RSS 0, VSZ 0.** A zombie is not a leaked process; it is a *receipt*. What remains is one `task_struct` holding the PID, the exit status, and the accumulated resource usage — a few hundred bytes of kernel memory, plus the one thing that is genuinely scarce: **the PID itself.**

The moment the parent reaps it, the receipt is destroyed:

```
reaped: exit status 42; /proc/403901 now: gone
```

---

## 3. Reading the Status Word

`wait()` and `waitpid()` hand back a single `int` that is **not** the exit status — it is a packed encoding of *how* the process ended, and you must use the macros to unpack it.

`status.c`, on this machine:

| The child did | Raw `status` | Macros say |
|---|---:|---|
| `_exit(0)` | `0x0000` | `WIFEXITED`, `WEXITSTATUS` = 0 |
| `_exit(3)` | `0x0300` | `WIFEXITED`, `WEXITSTATUS` = 3 |
| **`_exit(256)`** | `0x0000` | `WIFEXITED`, **`WEXITSTATUS` = 0** |
| `_exit(-1)` | `0xff00` | `WIFEXITED`, `WEXITSTATUS` = 255 |
| `raise(SIGKILL)` | `0x0009` | `WIFSIGNALED`, `WTERMSIG` = 9 |
| `raise(SIGSEGV)` | `0x008b` | `WIFSIGNALED`, `WTERMSIG` = 11, **`WCOREDUMP`** |

Three things fall straight out of the encoding:

1. **Only the low 8 bits of the exit status survive.** `_exit(256)` is indistinguishable from success. An exit code is a byte; treat it as one.
2. **Killed is not the same as exited.** `WIFEXITED(status)` is *false* for a process that died on a signal, and code that reads `WEXITSTATUS` without checking `WIFEXITED` first gets a meaningless number. This is the single most common bug in student process code.
3. **`0x008b` is `0x80 | 11`** — bit 7 is the core-dump flag, which is why the shell prints "Segmentation fault (core dumped)".

**The shell flattens all of this into one byte**, which is why `$?` is 137 for a process killed by `SIGKILL`: the convention is **128 + signal number**. That convention is the shell's, not the kernel's. Your own code has the full status word and should use it.

---

## 4. `wait`, `waitpid`, and the Only Two Ways to Reap

```c
pid_t wait(int *status);                              /* any child, blocking */
pid_t waitpid(pid_t pid, int *status, int options);   /* this child, or not blocking */
```

`waitpid`'s first argument selects: `> 0` one child, `-1` any child, `0` any child in my process group, `< -1` any child in process group `-pid`.

The options that matter this term:

| Option | Meaning | Used in |
|---|---|---|
| `WNOHANG` | Return **0 immediately** if no child has exited yet | Lab 0, Week 6 |
| `WUNTRACED` | Also report children *stopped* by a signal | Week 6, job control |
| `WCONTINUED` | Also report children resumed by `SIGCONT` | Week 6 |

**`WNOHANG` is what turns reaping from a blocking operation into a poll**, and it is what makes a `SIGCHLD` handler correct (L03 §6). Without it, a supervisor that wants to reap *whatever has died* while continuing to do its own work has no way to ask.

**When there are no children left**, `wait()` returns `-1` with `errno == ECHILD`. That is a normal, expected answer, not a failure — it is how a reaping loop terminates:

```c
while (waitpid(-1, &st, WNOHANG) > 0)
    ;   /* reap everything that is ready; stop at 0 (none ready) or -1 (none left) */
```

---

## 5. Orphans, and Who Actually Adopts Them

If the parent exits first, the child becomes an **orphan** — and its exit status now has no reader. The kernel reassigns it a parent so that someone will reap it.

**APUE says that parent is `init`, PID 1.** `orphan.c` measures it here:

```
child 402584: ppid at birth = 402583
parent 402583 exiting immediately
child 402584: ppid after parent exit = 257510
```

```
$ ps -o pid,comm= -p 257510
 257510 systemd
$ tr '\0' ' ' < /proc/257510/cmdline
/usr/lib/systemd/systemd --user
```

**PID 257510, not 1.** The orphan was adopted by the *user's* systemd instance, not the system's `init`.

The mechanism is `prctl(PR_SET_CHILD_SUBREAPER, 1)`, a Linux extension. A process that sets it becomes the adoptive parent for any orphan in its subtree, and only if no subreaper exists does the orphan travel all the way to PID 1. `systemd --user` sets it so that a user's stray background processes are reaped by their own session manager instead of accumulating on `init`.

> **This is the first place in the course where the textbook and the machine disagree, and both are
> right.** POSIX guarantees an orphan is reparented to "an implementation-defined system process".
> APUE names the traditional one. Linux with systemd interposes a per-user one. **A program that
> hardcodes `getppid() == 1` as its test for "am I orphaned" is broken on every desktop Linux
> shipped in the last decade** — which is exactly the kind of assumption this course exists to
> knock out of you. Check what you actually need to know instead: compare `getppid()` against the
> PID you recorded at startup.

---

## 6. Why Zombies Are a Denial of Service

A zombie costs a few hundred bytes. That is not the problem. **The problem is that it holds a PID**, and PIDs are a fixed-size resource:

```
$ cat /proc/sys/kernel/pid_max     4194304      # system-wide ceiling
$ ulimit -u                        25571        # RLIMIT_NPROC, per real UID
```

A server that forks a worker per request and never reaps hits `RLIMIT_NPROC` after **25,571 requests** on this machine — at which point `fork()` returns `-1` with `EAGAIN`, and it returns `EAGAIN` **for every other program that user is running too**. The failure is not local to the buggy process; a user's whole session stops being able to start anything.

The classic symptom is a machine that seems fine — no CPU load, no memory pressure, plenty of disk — on which nothing new will start. `ps aux | grep defunct` is the diagnosis, and it is worth doing early rather than late.

**Two fixes, and one of them is not a fix:**

```c
signal(SIGCHLD, SIG_IGN);    /* 1. tell the kernel you will never want the statuses */
```

`autoreap.c` confirms what POSIX promises: with `SIGCHLD` set to `SIG_IGN`, children are reaped automatically at exit and never become zombies. The cost is total — `wait()` then returns `-1`/`ECHILD` and **you can never learn any child's exit status again**. For a daemon that fires and forgets, that is a legitimate trade. For anything that cares whether the work succeeded, it throws away the only channel there is.

```c
while (waitpid(-1, &st, WNOHANG) > 0) ;   /* 2. reap, in a SIGCHLD handler */
```

The second is the real one, and it is what Lab 0 builds. It needs L03's material to be correct, because the handler must be async-signal-safe and must loop — `SIGCHLD` does not queue, so **one delivery can mean any number of dead children**.

> **What is *not* a fix:** calling `wait()` in the main loop whenever you happen to think of it. If
> the main loop is blocked in `accept()` or `read()`, "whenever you think of it" is never, and the
> zombies pile up in exactly the workload — a busy server — where it matters.

---

## 7. The Other Tree: Groups and Sessions

The parent/child tree is not the only structure over processes. There are two more, and Week 6 is built on them.

| Grouping | Made by | What it is for |
|---|---|---|
| **Process group** | `setpgid(pid, pgid)` | The unit that **signals** are delivered to. A shell pipeline is one group |
| **Session** | `setsid()` | A collection of groups with one **controlling terminal**, and one foreground group |

`/proc/<pid>/stat` fields 5 and 6 are the process group and session; `ps -o pid,pgid,sid,tpgid` prints them.

**Why it exists.** When you type Ctrl-C, the terminal driver sends `SIGINT` — not to a process, but to **the foreground process group of the terminal's session**. That is why Ctrl-C kills the whole of `cat file | grep x | wc -l` and not just one of the three. Ctrl-Z sends `SIGTSTP` the same way, and `kill(-pgid, sig)` is how you do it programmatically.

**A session leader that has no controlling terminal is a daemon.** `setsid()` is the call that detaches: it makes the caller a new session leader in a new process group with no terminal, so it cannot be killed by a Ctrl-C in the shell that started it, and cannot be stopped when that shell exits. Week 12 builds a proper daemon; this is the primitive it starts from.

**The whole state machine, then:**

```
                  fork()
                    │
                    ▼
   ┌──────────► R  runnable / running ◄──────────┐
   │                │        ▲                   │ SIGCONT
   │  blocking      │        │ event             │
   │  syscall       ▼        │                   │
   │            S  interruptible sleep           │
   │            D  uninterruptible sleep    T  stopped
   │                │                            ▲
   │                │ _exit() or fatal signal    │ SIGSTOP / SIGTSTP
   │                ▼                            │
   │            Z  zombie ───► reaped ───► gone ─┘
```

Observed directly, with `sleep 30` in the background:

```
running sleep:   S
after SIGSTOP:   T
after SIGCONT:   S
after SIGKILL:   (gone — the shell reaped it)
```

**`D` is the state worth fearing.** An uninterruptible sleep is a process inside a system call that cannot be interrupted — classically an NFS or disk read — and **it cannot be killed, not even by `SIGKILL`**, until the I/O completes or fails. A machine full of `D`-state processes is a machine with a storage problem, and no amount of `kill -9` will help.

---

## 8. What to Take Away

1. **A zombie is a receipt, not a leak.** No address space, no descriptors — a PID and an exit status.
2. **The status word is packed.** Check `WIFEXITED` before `WEXITSTATUS`; only 8 bits survive; `128+n` is the shell's convention, not the kernel's.
3. **`waitpid(-1, &st, WNOHANG)` in a loop** is the reaping idiom, and `ECHILD` is how it ends.
4. **Orphans are adopted by the nearest subreaper**, which on these machines is `systemd --user` at PID 257510 and not `init`. Never test `getppid() == 1`.
5. **Unreaped children exhaust `RLIMIT_NPROC` — 25,571 here — for the whole user**, not just the offending process.
6. **`SIGCHLD` to `SIG_IGN` auto-reaps** at the price of never learning a status again.
7. **Signals go to process groups**, which is why Ctrl-C kills a pipeline, and `setsid()` is how a daemon escapes the terminal.

---

## Exercises

1. Write a program that creates one zombie, then run `ps -o pid,ppid,stat,rss,comm --ppid $(pgrep yourprog)`. Reap it and run the same command again.
2. `_exit(-1)` gives `WEXITSTATUS` 255. What does `_exit(300)` give, and why? Predict before running.
3. Start a process, `kill -STOP` it, and read `/proc/<pid>/stat` field 3. Then `kill -9` it — does it die? Now find a way to produce a `D`-state process. *(Hint: a large read from a slow device; do not use the lab NFS mount.)*
4. In `orphan.c`, replace the test `getppid() == 1` with something that is actually correct on this machine.
5. Read `man 2 wait` and find `WIFCONTINUED`. Which of L02's three groupings does it belong to?

---

*PROG 201 · Week 0 · L02 · © CSE Department*
