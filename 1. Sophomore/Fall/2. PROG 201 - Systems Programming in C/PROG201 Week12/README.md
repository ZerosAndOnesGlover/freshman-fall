# PROG 201 · Systems Programming in C
## Week 12: Synthesis — Building a Production Daemon

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101; CS 201 as co-requisite
**Assessment for this course (overall):** Problem Sets 35%, Projects 25%, Midterms 25%, Final 15%
**This week's deliverable:** **Project 2** — a production HTTP daemon — **due Friday 17:00** (demo at Lab 12, Monday of the completion period). **No quiz** (Weeks 11–12 are examined on the final).
**Lab 11 is sat on the Monday of this week; Lab 12 (demo day + code review) is sat on the Monday of the completion period.**

> ### **This is the capstone. One program, and every claim about it is measured.**
> The week takes your Week 5–6 concurrent server and makes it a **daemon that runs unattended**:
> correct signals, graceful shutdown, backpressure, a hardened and fuzzed parser, privilege
> handling, resource limits — and the measurements that prove each works. `ab` is not installed, so
> the course ships its own load client (`bench`) and disconnect tool (`rudeclient`) as the Lab 12
> harness. Every number this week was produced on the reference machine by a named program.

---

### Why This Week Exists

Because eleven weeks produced programs that ran, printed the right thing, and exited — watched by you. Nothing yet had to survive a `kill` from an operator, a client that hangs up mid-reply, a burst that outruns it, or a memory budget, for months, unattended. The gap between *ran once* and *runs unattended* is where real systems live and where this course ends.

The whole week is one small HTTP server, measured against each hazard, and the measurements are the argument. The thesis: **the difference between working code and production code is not cleverness — it is the measurement you take after you think you are done.**

Three ideas:

1. **A signal is an asynchronous interrupt**, so the daemon turns signals into fds (the self-pipe) and responds in the main loop — draining on `SIGTERM`, ignoring `SIGPIPE`.
2. **Capacity is measured, never assumed** — the same server is flat across worker counts for a trivial handler and linear for a blocking one; only a load test says which regime you are in.
3. **Running unattended means not growing and not lying** — flat fds and RSS under sustained load, and a privilege drop you *verify* rather than assume.

---

### Learning Objectives

By the end of Week 12, you should be able to:

1. Explain why a signal handler may call only async-signal-safe functions, and name which common ones are not.
2. Implement the **self-pipe trick** (or `signalfd`) and respond to signals in the main loop.
3. Implement **graceful shutdown** — drain in-flight work on `SIGTERM`, exit 0.
4. Explain and fix the **SIGPIPE trap**, and decode the exit code of a process killed by it.
5. Build a **thread pool + bounded queue** and explain the backpressure a bound provides.
6. **Measure** throughput and p99 latency, and distinguish an accept-bound from a worker-bound workload.
7. **Measure** fd and memory stability under sustained load and locate a leak.
8. Harden a parser (bounded reads, guard build) and **fuzz** it under ASan.
9. Explain the privilege-drop sequence and the `setgroups` trap; verify a drop via `/proc/self/status`.
10. Write a `systemd` unit with restart, privilege, and cgroup resource controls.
11. Compose the whole course — parser (W10), isolation and cgroups (W11), sockets and signals (W5–6) — into one defended service.
12. State the course's law — *a mechanism present is not a mechanism working* — across all seven of its appearances, each with its revealing measurement.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L37 The Production Daemon Signals and Graceful Shutdown]] | Signals as async interrupts; async-signal-safety; the **self-pipe trick**; **graceful drain on SIGTERM measured to exit 0**; the **SIGPIPE pair** — careful `write`-checking defeated because the signal fires first (**exit 141**), one `SIG_IGN` line fixing it (**EPIPE, exit 0**) — the sixth "present but not working" |
| [[L38 Concurrency and Capacity]] | Thread pool + **bounded queue** + condvars; **two scaling regimes measured** — trivial handler **flat ~36k req/s** (accept-bound, 16 workers *slower* than 4), blocking handler **linear 5×workers**; **p99 (11ms) is the SLA number, not the mean (2.3ms)**; **fd delta 0** and **RSS flat at 1728 kB across 50k requests** |
| [[L39 Running Unattended and the Synthesis]] | **`bind :80 → EACCES`** and the start-privileged-then-drop pattern; **`setuid` without `setgroups` keeps root's groups** (seventh "present but not working", read from `/proc/self/status`); `systemd` supervision with **`MemoryMax`/`TasksMax` (Week 11 cgroups)** and `AmbientCapabilities`; the fuzzed parser (Week 10); and the course-wide synthesis |
| [[LAB 12 Demo Day and Code Review]] | Demo your daemon against the harness (drain, rude client, no-leak, the SIGPIPE negative control), then **review a peer's daemon** against a production checklist. **Monday of the completion period** |
| `lab/harness/` | `bench.c` (load client, reports p99), `rudeclient.c` (mid-response disconnect), Makefile, README — provided, warning-clean |
| [[PROJECT 2 A Production HTTP Daemon]] | The capstone: turn your Week 5–6 server into a production daemon and **measure** every property. **Due Friday of Week 12** |
| `assignments/p2/` | Starter scaffold (`httpd.c` with TODOs, builds clean under `-Werror`) and a production+sanitizer Makefile |
| [[PROG201 Week12/resources/Reading Guide Week 12\|Reading Guide Week 12]] | `signal-safety(7)` (read twice), `setuid`+`setgroups` together, `systemd.service`, the self-pipe trick |
| `solutions_instructor/` | Instructor only — marking notes and the reference daemon |

*There is no Quiz 12 — Weeks 11 and 12 are examined on the final.*

---

### The One Thing to Take From This Week

**The difference between working code and code that runs unattended is the measurement you take after you think you are done.**

| Property | Naive design | Production design | Measured pair |
| --- | --- | --- | --- |
| **Shutdown** | `exit()` in the handler | drain, then exit | truncated reply → **clean exit 0** |
| **Client disconnect** | check `write()` return | *also* ignore SIGPIPE | **exit 141 (killed)** → **exit 0 (EPIPE handled)** |
| **Burst** | unbounded queue | bounded, backpressure | RSS runaway → bounded |
| **Capacity** | "add threads" | measure the regime | flat ~36k (trivial) vs linear 5×N (blocking) |
| **Leaks** | assert "it's fine" | watch under load | fd **delta 0**, RSS **flat 1728 kB / 50k reqs** |
| **Privilege drop** | trust `getuid()` | read `/proc/self/status` | `Groups:` still root's → **empty** |

**The SIGPIPE row and the privilege-drop row are the sixth and seventh times the course has met the same shape** — a mechanism *present* that is not *working*: `PRIO_INHERIT` (W3), lazy binding (W8), ASLR-without-PIE and inert CET (W10), the stripped user namespace (W11), and now these two. In every case the code was there and looked right, and the only thing that told the truth was a measurement taken *after* the code was written: hold a connection and hang up, or read the group list. **That habit — distrust your own success until you have measured it — is what the course was for.**

---

### Assessment Reminder

**Labs and the demo carry no weight** and are required. **Project 2 is due Friday 17:00 and is 12.5% of the course.** There is **no quiz** this week.

> **Lab 11** is sat on the **Monday of this week**. **Lab 12** — demo day and peer code review — is
> sat on the **Monday of the completion period**. The **final exam** is comprehensive (150 minutes,
> two handwritten pages) and covers all twelve weeks, including 11 and 12.

Tracked in [[_PROG 201 Lab and Quiz Record]].

---

### Connections

**Back — this is where they all converge:** **Weeks 0–2** (processes, fds, redirection) are the fd discipline measured flat; **Weeks 3–4** (threads, sync, VM) are the pool, condvars and RSS; **Weeks 5–6** (sockets, concurrent server, the shell's signals) are the daemon's core and its signal handling; **Week 7** (filesystems) is what it serves; **Weeks 8–9** (linking, performance) are the build and the measure-don't-guess method; **Week 10** (security) is the hardened, fuzzed parser; **Week 11** (containers) is the isolation and cgroup budget it runs inside.

**Sideways:** **CS 201** on privilege levels and the user/kernel boundary is the hardware under §1's privileged-port and §2's capability model.

**Forward:** CS 302 (Networks) takes the socket down the stack; CS 341 (Security) takes the parser hardening into full exploitation and defence. Every systems course after this assumes you can write the daemon *and* measure that it works.

---

*PROG 201 · Week 12 · © CSE Department · end of the course*
