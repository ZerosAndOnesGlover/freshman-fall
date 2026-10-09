# PROG 201 · Systems Programming in C
## Week 0 · Lecture 3 of 3
### Signals: `sigaction`, Masks, and Async-Signal-Safe Code

*“Thinking doesn't guarantee that we won't make mistakes. But not thinking guarantees that we will.”* — Leslie Lamport, as quoted in *Wired* (2013)

---

**Reading:** APUE §10.1–10.15 · **Previous:** L02, waiting · **Next:** Lab 0, the process supervisor

**Coursework:** 📝 **PS 0** released Wed this week, due Fri of Week 1 17:00 · 🔬 **Lab 0** Fri this week 17:00–18:50

---

## 1. A Signal Is an Interruption, Not a Message

When a signal is delivered, the kernel **suspends your program wherever it is**, builds a stack frame for the handler, runs it, and restores the interrupted context. Not between statements — **between instructions**, in the middle of a half-updated data structure if that is where you were.

Everything difficult about signals follows from that one sentence.

```
      normal control flow                     signal arrives
      ───────────────────►  ✂  ───────────────────────────────►  ✂  ──────►
                            │   handler runs on the same stack   │
                            │   (or an altstack, if you set one) │
                            └────────────────────────────────────┘
                              your variables are mid-update here
```

`kill -l` lists **62** signals on this machine: numbers 1–31, the standard ones, and 34–64, the real-time ones. **32 and 33 are missing** because glibc's threading implementation claims them; `SIGRTMIN` is therefore 34, not 32, and hard-coding 32 is a portability bug that appears only under a threaded program.

---

## 2. Never Use `signal()`. Use `sigaction()`.

`signal()` is in the C standard, which is precisely the problem: C says almost nothing about what it does, and two Unix traditions answered differently.

| | System V `signal()` | BSD `signal()` |
|---|---|---|
| Handler after one delivery | **Reset to `SIG_DFL`** | Stays installed |
| Signal blocked during its own handler | No — **it can nest** | Yes |
| Interrupted system call | Fails with `EINTR` | **Restarted** |

**glibc gives you the BSD semantics.** `eintr.c` demonstrates: a `read()` on an empty pipe with `SIGALRM` armed.

```
$ ./eintr sigaction      read() -> -1, errno = 4 (Interrupted system call)
$ ./eintr restart        (no output — read() resumed and blocked forever)
$ ./eintr signal         (no output — same as SA_RESTART)
```

Three installations of the same handler for the same signal: **`sigaction` with no flags gives `EINTR`, `SA_RESTART` resumes the call, and glibc's `signal()` behaves like `SA_RESTART`.** The same source, compiled on a System V-derived Unix, would take the first branch. That is a program whose behaviour depends on the libc it was linked against — and the fix is to stop asking.

```c
struct sigaction sa;
memset(&sa, 0, sizeof sa);          /* zero it: sa_flags and sa_mask must be initialised */
sa.sa_handler = on_sigchld;
sigemptyset(&sa.sa_mask);           /* extra signals blocked during the handler */
sa.sa_flags = SA_RESTART;           /* state your choice explicitly */
if (sigaction(SIGCHLD, &sa, NULL) < 0) die("sigaction");
```

**`sigaction` makes every one of the three rows explicit.** Use it, in this course and after it.

> **`SA_RESTART` is not a free "make `EINTR` go away".** The kernel restarts only some calls;
> `read`/`write` on a slow device, yes — but `select`, `poll`, `epoll_wait`, `nanosleep` and any
> call with a timeout are **never** restarted, because restarting them would silently extend the
> timeout. You still have to handle `EINTR` (§6). `SA_RESTART` reduces where it can appear; it does
> not eliminate it.

---

## 3. Signals Do Not Queue — Measured

A pending standard signal is **one bit**. If a second arrives while the first is still pending, there is no second bit to set, and the second one is gone.

`rtq.c` makes this exact: block the signal, send *N* of them, then unblock and count how many times the handler runs.

| Signal | Sent | Handler ran |
|---|---:|---:|
| `SIGUSR1` (standard) | 5,000 | **1** |
| `SIGRTMIN` (real-time) | 5,000 | 5,000 |
| `SIGRTMIN` | 20,000 | 20,000 |
| `SIGRTMIN` | **40,000** | **25,571** |

**Five thousand signals collapse into one.** Real-time signals do queue — that is their point — but the queue is bounded by `RLIMIT_SIGPENDING`, which is 25,571 here (`ulimit -i`), and past that the excess is dropped. **`kill()` returned 0 for all 40,000 of them.** No error, no indication, 14,429 signals gone.

> **Two limits on this machine happen to share a value.** `ulimit -u` (`RLIMIT_NPROC`, L02 §6) and
> `ulimit -i` (`RLIMIT_SIGPENDING`) are both 25,571 — they are derived from the same kernel default,
> not from each other. Do not read one number as evidence about the other limit.

And with a *running* parent rather than a blocking one, `coalesce.c` sends 100,000 signals while the receiver does ordinary work:

```
SIGUSR1   sent 100000  handled  50085  (50.1%)   ...five runs: 49.7 – 50.1%
SIGRTMIN  sent 100000  handled  76579  (76.6%)   ...five runs: 75.7 – 78.1%
```

**Half of them, reproducibly.** The receiver is inside the handler — during which the signal is blocked — roughly half the time, and every signal that arrives in that window merges with the one already pending.

**The design rule:** a signal means *"at least one of these events happened"*. It never means "one happened", and it certainly never carries a count. **Every signal handler in this course reacts to the fact rather than the number** — which is exactly why the `SIGCHLD` handler in §6 loops with `WNOHANG` instead of reaping once.

---

## 4. Async-Signal-Safety: 192 Functions

A handler can interrupt the main program *inside* a library function. If the handler then calls the same function, it re-enters a routine that is halfway through updating its own state.

POSIX names the functions that are guaranteed to survive this. `man 7 signal-safety` lists them; on this machine the table holds **192 distinct functions**. `write`, `read`, `_exit`, `kill`, `waitpid`, `signal`, `sigaction`, `open`, `close` are on it.

**`printf`, `malloc`, `free` and `exit` are not.**

`reent.c` calls `printf` in a `SIGALRM` handler every 100 µs while the main loop prints 400,000 lines:

```
total lines:      408909
clean A lines:    408771     (main loop)
clean B lines:        45     (handler)
corrupted lines:      93
```

Of the handler's 138 lines, **93 came out damaged — two thirds of them.** Not a crash: lines of the wrong length, spliced fragments, output that no `printf` in the program ever asked for. Silent, and in a real program it corrupts a log file rather than a screen full of A's.

**Now the honest half of the experiment.** `unsafe.c` calls `malloc()` in the handler while the main loop calls `malloc()` at full speed — the textbook deadlock, where the handler tries to take an arena lock the main loop already holds. On this machine it ran **1.49 billion allocations and ~100,000 signals in 20 seconds and never deadlocked**, because glibc 2.39's `tcache` fast path takes no lock at all.

> **That is the lesson, not a failure of the demonstration.** The bug is real, it is undefined
> behaviour, and it is *unreproducible on the fast path* — so it does not show up in your testing,
> it shows up in production, on the run where the allocation happened to miss tcache and go to the
> arena. **"I tried it and it worked" is not evidence about undefined behaviour.** It is evidence
> about one run.

---

## 5. What a Handler Is Allowed to Do

Three things, in practice:

```c
static volatile sig_atomic_t got_sigterm = 0;

static void on_term(int sig)
{
    (void) sig;
    got_sigterm = 1;                    /* 1. set a flag */
}

static void on_chld(int sig)
{
    int saved = errno;                  /* 3. save and restore errno */
    while (waitpid(-1, NULL, WNOHANG) > 0)
        ;                               /* 2. call an async-signal-safe function */
    errno = saved;
}
```

1. **Set a `volatile sig_atomic_t` flag** and let the main loop do the work. `volatile` stops the compiler caching the variable in a register across the loop that reads it; `sig_atomic_t` is the only integer type guaranteed to be read and written in one uninterruptible step. **Neither of them makes it thread-safe** — that is Week 3's problem, and `sig_atomic_t` is not an answer to it.
2. **Call only functions from the list** — in practice `write`, `waitpid`, `kill`, `_exit`.
3. **Save and restore `errno`.** `waitpid` in the handler sets `errno` to `ECHILD` when the children run out; the main program, interrupted mid-way through its own error checking, then reads a value it never caused. This is a genuinely nasty bug: it converts a working program into one that reports failures that did not happen.

**Printing from a handler**, when you must:

```c
static const char msg[] = "caught SIGTERM, shutting down\n";
if (write(STDERR_FILENO, msg, sizeof msg - 1) < 0) { /* nothing useful to do */ }
```

One `write`, no formatting, no buffering. Ugly on purpose.

---

## 6. `EINTR`, and the Retry Wrapper

Any blocking call can return `-1`/`EINTR` when a handler runs during it. **`EINTR` is not an error** — nothing failed, the call was merely cut short — and the correct response is almost always to do it again:

```c
ssize_t r;
do { r = read(fd, buf, n); } while (r < 0 && errno == EINTR);
```

Two places where "just retry" is wrong, and both bite this term:

- **A call with a timeout** — `poll`, `select`, `epoll_wait`, `nanosleep`. Retrying restarts the *full* timeout, so a program signalled every 100 ms waits forever on a 1-second `poll`. Recompute the remaining time, or use `ppoll`/`pselect`.
- **`close()`.** On Linux the descriptor is released *before* `EINTR` is returned, so retrying closes a descriptor that may already have been reopened by another thread. `man 2 close` says it outright: **do not retry `close`**.

---

## 7. The Race That `pause()` Cannot Win

The obvious wait-for-a-signal loop is broken:

```c
while (!got_sigterm)        /* ← if the signal arrives HERE... */
    pause();                /* ← ...this blocks forever */
```

The signal can land between the test and the `pause()`. The flag is set, the handler has already run, and `pause()` is now waiting for a signal that has been and gone. On an idle daemon this hangs until something else happens to arrive — which may be never.

**The fix is to make "unblock and wait" a single atomic operation:**

```c
sigset_t block, orig;
sigemptyset(&block); sigaddset(&block, SIGTERM);
sigprocmask(SIG_BLOCK, &block, &orig);       /* block it first */

while (!got_sigterm)
    sigsuspend(&orig);                        /* atomically unblock + wait */

sigprocmask(SIG_SETMASK, &orig, NULL);
```

`sigsuspend` installs the old mask and blocks in one uninterruptible step, so there is no window. The signal is blocked everywhere else, so if it arrives before the loop, it is *pending* and `sigsuspend` returns immediately.

**Two modern alternatives**, both of which turn a signal into something you can `poll()` alongside your sockets — which is what you will actually want from Week 5 onwards:

- **The self-pipe trick.** The handler does one `write(pipefd[1], "x", 1)`; the main loop selects on the read end. Portable, and `write` is on the safe list.
- **`signalfd(2)`.** Linux-specific: signals are read as structs from a file descriptor, with no handler at all. Cleaner, and unavailable outside Linux.

---

## 8. The Signals You Will Meet This Term

| Signal | Default | Where it comes up |
|---|---|---|
| `SIGCHLD` | **Ignored** | A child stopped or died — L02, Lab 0, Week 6 |
| `SIGINT` / `SIGTSTP` | Terminate / Stop | Ctrl-C and Ctrl-Z, to the **foreground process group** — Week 6 |
| `SIGPIPE` | **Terminate** | Writing to a pipe or socket with no reader — Weeks 2 and 5 |
| `SIGSEGV` / `SIGBUS` | Terminate + core | Week 4, and it is a *useful* signal there |
| `SIGTERM` | Terminate | The polite shutdown request — Week 12 |
| `SIGKILL` / `SIGSTOP` | Terminate / Stop | **Cannot be caught, blocked, or ignored** |
| `SIGALRM` | Terminate | Timeouts, and this lecture's experiments |

**`SIGPIPE` deserves its place on that list now**, because it will kill your Week 5 server on the first client that disconnects early. The default disposition is *terminate the process*, and a server that dies whenever a browser hits Stop is not a server. Either `signal(SIGPIPE, SIG_IGN)` and check `write()` for `EPIPE`, or pass `MSG_NOSIGNAL` to `send()`. It is the most common one-line bug in student network code, and it is one line to prevent.

---

## 9. What to Take Away

1. **A signal interrupts between instructions**, not between statements.
2. **`sigaction`, always.** `signal()`'s semantics depend on the libc, and this machine proves it.
3. **Standard signals do not queue** — 5,000 became 1. Real-time signals queue up to `RLIMIT_SIGPENDING` and then drop silently, with `kill()` still returning 0.
4. **192 functions are async-signal-safe; `printf` and `malloc` are not** — two thirds of the handler's `printf` output came out corrupted, and the `malloc` deadlock did not reproduce in 1.5 billion tries, which is worse.
5. **A handler sets a flag, calls a safe function, and restores `errno`.**
6. **`EINTR` means "do it again"** — except for calls with timeouts and for `close()`.
7. **`pause()` in a test-then-wait loop is a race.** Use `sigsuspend`, a self-pipe, or `signalfd`.

**Lab 0 uses all seven.** A process supervisor is a `SIGCHLD` handler, a `waitpid`/`WNOHANG` loop, a `SIGTERM` flag and a `sigsuspend` main loop — which is the whole of this week, running unattended.

---

## Exercises

1. Install a `SIGINT` handler with `signal()`, press Ctrl-C twice, and explain the result. Repeat with `sigaction` and no flags.
2. Modify `rtq.c` to send `SIGUSR1` and `SIGUSR2` interleaved while both are blocked. How many of each are delivered, and in what order? *(`man 7 signal` explains the ordering.)*
3. Write a handler that calls `printf` and pipe the output to `wc -l`. Vary the timer interval until you can produce a corrupted line, and report the interval you needed.
4. Explain why `write()` is on the async-signal-safe list and `fwrite()` is not.
5. Break the `sigsuspend` loop deliberately: replace it with `pause()` and add a `sleep(1)` between the test and the call. Send `SIGTERM` during the sleep. What happens, and how long does it take to notice?

---

*PROG 201 · Week 0 · L03 · © CSE Department*
