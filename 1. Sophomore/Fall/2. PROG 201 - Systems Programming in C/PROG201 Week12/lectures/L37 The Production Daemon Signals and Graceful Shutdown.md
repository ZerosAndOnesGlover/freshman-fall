# PROG 201 · Systems Programming in C
## Week 12 · Lecture 1 of 3
### The Production Daemon — Signals and Graceful Shutdown

*“...the right thing might be to eliminate the cost of making a mistake rather than try to guess what's right.”* — Ward Cunningham, "Collective Ownership of Code and Text", Artima interview (2003)

---

**Reading:** TLPI Ch. 20–22 (signals), Ch. 37 (daemons) · `man 7 signal`, `man 7 signal-safety`, `man 2 sigaction`, `man 2 poll` · **Previous:** Week 11 L36 · **Next:** L38 — concurrency and capacity

**Coursework:** 📋 **Project 2** due Fri this week 17:00 · 📝 **PS 11** due Fri this week 17:00 · 🔬 **Lab 12** Mon of the completion period

---

## 1. What "Production" Means

Eleven weeks of this course produced programs that ran, printed the right thing, and exited. This week is about the gap between *ran once, watched by you* and **runs unattended, for months, while you sleep.** A production daemon is not cleverer than your Week 6 server — it is the same server that has been made to survive everything that happens to a long-lived process: signals it did not send itself, clients that vanish mid-reply, load that outstrips it, a `kill` from an operator, a memory budget it must live inside.

The whole week is a single program — a small HTTP server — measured against each of those, and the measurements are the argument. This lecture is the two that arrive as **signals**: the operator's `SIGTERM`, and the client's disconnect that becomes `SIGPIPE`.

**The reference machine** for every number this week: Intel i5-8250U (8 logical CPUs), Linux 7.0.0-30, glibc 2.39, all traffic over loopback. The server is `httpd.c`; the load client is `bench.c` (because `ab` is not installed); the disconnect is `rudeclient.c`. Each figure names the program that produced it.

---

## 2. A Signal Is an Interrupt, Not a Function Call

A signal arrives **between two instructions of whatever the process was doing**, runs a handler, and returns. That asynchrony is the entire difficulty. Three consequences you must design around:

1. **A handler runs in a borrowed context.** It interrupts `main` — possibly in the middle of `malloc`, or `printf`, holding a lock. If the handler calls anything that takes the same lock, or that is not re-entrant, it **deadlocks or corrupts state**. The kernel defines a small list of **async-signal-safe** functions (`man 7 signal-safety`) that a handler may call: `write` is on it; `printf`, `malloc`, `free` are **not**.
2. **A handler must say as little as possible.** The correct handler for "please stop" does not stop anything — it records that a signal came and returns, and the main loop notices. The one variable type safe to touch is `volatile sig_atomic_t`.
3. **Blocking syscalls are interrupted.** A signal delivered while the process sits in `accept` or `poll` makes that call return `-1` with `errno == EINTR`. Code that does not expect `EINTR` treats a delivered signal as a fatal error. Every blocking call in a daemon must handle it — usually `if (errno == EINTR) continue;`.

The classic beginner handler — `void handler(int s){ printf("caught!\n"); cleanup(); exit(0); }` — breaks all three: `printf` is not async-signal-safe, `cleanup` may re-enter a held lock, and it runs teardown from interrupt context. It works in the demo and hangs in production.

---

## 3. The Self-Pipe: Turning a Signal Into a File Descriptor

The idiom that resolves all three problems is the **self-pipe trick**. At startup, create a pipe. The signal handler does exactly one async-signal-safe thing — `write` one byte to the pipe:

```c
static int stop_pipe[2];
static void on_term(int sig){ (void)sig; char c='x'; write(stop_pipe[1], &c, 1); }
```

Then the main loop does not wait on the listening socket alone — it **`poll`s the listening socket *and* the read end of the pipe together**:

```c
struct pollfd pf[2] = { {listen_fd, POLLIN, 0}, {stop_pipe[0], POLLIN, 0} };
for (;;) {
    if (poll(pf, 2, -1) < 0) { if (errno == EINTR) continue; break; }
    if (pf[1].revents & POLLIN) { /* SIGTERM arrived */ break; }   /* leave the loop */
    if (pf[0].revents & POLLIN) { int c = accept(listen_fd, 0, 0); ... }
}
```

Now a signal is just another readable fd. The handler is trivially safe (one `write`); the *response* to the signal happens back in `main`, in normal context, where it may take locks, call `free`, and log freely. This is how real servers turn the asynchronous world of signals into the synchronous world of an event loop — and modern Linux even gives you `signalfd(2)` to skip the pipe. **A signal you handle in the main loop instead of in the handler is a signal you can handle correctly.**

---

## 4. Graceful Shutdown, Measured

When `SIGTERM` arrives (which is what `kill`, `systemctl stop`, and a container runtime's stop send — **not** `SIGKILL`, which cannot be caught), a production daemon does not drop dead. It **drains**: stop accepting new connections, finish the requests already in flight, then exit. An operator who runs `systemctl stop` expects in-flight requests to complete, not to return half a response.

The reference `httpd` does exactly this. On the pipe wakeup it leaves the accept loop, closes the listening socket (new connections now get "connection refused"), sets a `shutting` flag, wakes the worker threads, and `pthread_join`s them so every request already dequeued runs to completion. Then `return 0`. Measured, from `bench` holding 20 connections open when the `SIGTERM` lands:

```
$ ./httpd 39117 4 &          # start
[httpd] pid 1265326 listening on 127.0.0.1:39117, 4 workers
$ kill -TERM %1              # operator asks it to stop
[httpd] SIGTERM: draining
[httpd] drained and exiting 0
$ echo $?
0                            # <- clean exit, in-flight requests completed
```

**Exit 0, and the in-flight responses were delivered.** Contrast the naive design that calls `exit()` inside the handler: it exits from interrupt context, mid-request, and the client holding a connection gets a truncated reply or a reset. Same signal, two designs, and the difference — a clean drain versus a severed connection — is the whole of "graceful."

---

## 5. The SIGPIPE Trap — a Mechanism Present but Not Working

Here is the finding that ties Week 12 to the recurring thread of the whole course. The reference server is **careful**: it checks the return value of every `write`. That is the textbook definition of robust I/O. And yet, with one line missing, the identical careful code is **killed dead** by a client that simply hangs up.

When you `write` to a socket whose peer has closed the connection, the kernel does two things: it will eventually return `-1` with `errno == EPIPE` from `write`, **and** it raises the signal **`SIGPIPE`**, whose default disposition is to **terminate the process**. The signal wins the race: the process dies *before* `write` ever returns the `-1` your careful code was ready to handle. Your error checking is present, and it never runs.

The measured pair, with a client (`rudeclient`/`sigtest_client`) that sends a request then closes, and a server that writes its reply in two parts:

```
=== DEFAULT SIGPIPE disposition ===
[srv] write1 = 17 (ok)                 # first write succeeds, provokes a RST from the peer
[1]+  Broken pipe   ./sigtest_server   # second write -> SIGPIPE -> process KILLED
server exit = 141                      # 141 = 128 + 13 (SIGPIPE)

=== ONE LINE ADDED: signal(SIGPIPE, SIG_IGN) ===
[srv] write1 = 17 (ok)
[srv] write2 = -1 (Broken pipe)        # now write RETURNS -1/EPIPE, as the careful code expected
[srv] SURVIVED both writes
server exit = 0
```

`signal(SIGPIPE, SIG_IGN)` — ignore the signal — is the one line. With it, the kernel skips the terminate-by-signal and lets `write` return `-1`/`EPIPE`, which the existing error check handles: log it, close the connection, move on. In the full `httpd`, a mid-response client disconnect then reads:

```
[worker] client gone (EPIPE), handled
```

and the server serves the next request unbothered — proven by a follow-up `bench` request succeeding against the same still-running pid.

**This is the fifth time the course has met this exact shape** and named it — *a mechanism present is not a mechanism working*:

| Week | Present | Not working |
| --- | --- | --- |
| 3 | `PRIO_INHERIT` set on the mutex | priority inheritance never engaged |
| 8 | the PLT/GOT lazy-binding machinery | bound eagerly, GOT read-only |
| 10 | ASLR enabled system-wide | the non-PIE binary's code not randomised |
| 10 | `endbr64` CET markers in every binary | no CPU support, inert |
| 11 | the user namespace created | its capabilities stripped, `mount` EPERM |
| **12** | **every `write` return value checked** | **SIGPIPE kills the process before `write` returns** |

The lesson is now a law of the course: you cannot read robustness off the presence of the right code. The disconnect happened, the process died, and the only way you learned the error handling never ran was to **make a client hang up and watch.**

---

## Summary

- **Production means unattended.** The daemon is the same server made to survive signals, disconnects, load, and operator commands over months.
- **A signal is an asynchronous interrupt**, not a call: a handler runs in borrowed context, may call only **async-signal-safe** functions (`write` yes, `printf`/`malloc` no), and interrupts blocking syscalls with `EINTR`.
- **The self-pipe trick** turns a signal into a readable fd: the handler `write`s one byte, and the main loop `poll`s that pipe alongside the listening socket, so the *response* to the signal runs in normal context.
- **Graceful shutdown** on `SIGTERM` drains in-flight requests then exits — measured **exit 0** with responses delivered, versus a handler that `exit()`s mid-request and truncates them.
- **The SIGPIPE trap** is the week's "present but not working": careful `write`-return checking is defeated because the kernel raises `SIGPIPE` (default = terminate) before `write` returns `-1`/`EPIPE`. Measured: default → **exit 141** (killed); `signal(SIGPIPE, SIG_IGN)` → `write` returns `EPIPE`, **exit 0**, server survives. The sixth entry in the course's central table.

---

## Exercises

1. Write the "beginner" handler (`printf` + `exit` inside it) and the self-pipe version. Run each under load and describe how they can each go wrong. Which functions in your handler are async-signal-safe?
2. Add `EINTR` handling to a `poll`/`accept` loop, then remove it and send the process a harmless `SIGUSR1` under load. What does the un-handled `EINTR` look like from outside?
3. Reproduce the graceful-shutdown measurement: hold a slow connection open, `kill -TERM`, and confirm the in-flight request completes and the exit code is 0. Then move the teardown into the handler and show the truncated reply.
4. Reproduce the SIGPIPE pair. Explain precisely why the *first* write succeeds and the *second* is the one that triggers `SIGPIPE`/`EPIPE`. (Hint: RST arrives in response to the first.)
5. Why is `SIGKILL` (signal 9) not catchable, and what does that imply about what a daemon can promise on shutdown? What is the operator's contract with `SIGTERM` then `SIGKILL` after a timeout?
6. Replace the self-pipe with `signalfd(2)`. What does it simplify, and what does it still not let you do inside the handler-free model?
7. `MSG_NOSIGNAL` on `send`, and `SO_NOSIGPIPE` where it exists, are alternatives to `signal(SIGPIPE, SIG_IGN)`. Compare them: which is per-call, which per-socket, which process-wide, and when would you prefer each?

---

*PROG 201 · Week 12 · L37 · © CSE Department*
