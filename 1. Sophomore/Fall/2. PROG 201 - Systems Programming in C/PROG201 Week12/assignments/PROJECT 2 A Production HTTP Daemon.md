# PROG 201 · Project 2
## `httpd` — A Production HTTP Daemon

---

**Assigned:** Week 10, Friday · **Due:** Week 12, Friday 17:00 (demo at Lab 12, Monday of the completion period)
**Weight: 12.5% of the course** · Submit one PDF, `P2_{LastName}_{StudentID}.pdf`, and your code as `P2_{LastName}.tar.gz`

> **This is the capstone. It is one program, and the marks are weighted toward it running unattended
> rather than toward answering questions about it.**
>
> **You already have the core.** Your Week 5–6 concurrent HTTP server is the starting point, and
> reusing it in full is expected. What this project adds is everything that separates a server you
> watched work once from a **daemon that runs for a month without you**: correct signal handling,
> graceful shutdown, backpressure, a hardened and fuzzed parser, privilege handling, resource
> limits, and — above all — the **measurements** that prove each one works.
>
> **Every claim in your report must name the program that produced the number** (course rule since
> Week 1). "It doesn't leak" is not a sentence; a flat `VmRSS` across 50 000 requests is.
>
> Compiles clean under `gcc -Wall -Wextra -O2 -std=gnu11 -pthread`. Warnings cost marks. The
> provided test harness (`lab/harness/`: `bench`, `rudeclient`) is yours to measure with.

---

### What It Must Do

Serve HTTP/1.0 `GET` over TCP, concurrently, and **survive** everything in Parts 3–5.

```
$ ./httpd 8080 8                 # port, worker count
[httpd] pid 4711 listening on 127.0.0.1:8080, 8 workers
$ curl -s http://127.0.0.1:8080/ ; echo
hello
$ kill -TERM 4711                # an operator asks it to stop
[httpd] SIGTERM: draining
[httpd] drained and exiting 0    # in-flight requests completed; exit 0
```

---

## Part 1 — The Concurrent Core (20 points)

Your Week 5–6 server, working, reused. Marks are for the **shape**, measured.

**[10]** A **thread pool** of N workers and **one accept loop**, not thread-per-connection. State N and why.

**[10]** A **bounded** connection queue with condition variables (`notempty`/`notfull`). Show, by driving a burst larger than the pool can serve, that accept applies **backpressure** (blocks / the kernel backlog fills / connections are refused) instead of the queue growing without limit. Contrast, in one paragraph, with what an unbounded queue does to `VmRSS` under the same burst.

## Part 2 — Signals and Graceful Shutdown (24 points)

**[8] The self-pipe (or `signalfd`).** Your `SIGTERM`/`SIGINT` handler does exactly one async-signal-safe thing; the response happens in the main loop. Show the handler and name every function it calls, and confirm each is on the `signal-safety(7)` list.

**[8] Graceful drain.** On `SIGTERM`: stop accepting, finish in-flight requests, join workers, `exit 0`. **Measure it:** hold a slow connection open with the harness, send `SIGTERM`, and show (a) the in-flight request completed and (b) the exit code is 0. Then show what your *first* (naive, `exit()`-in-handler) version did to that same connection.

**[8] The SIGPIPE pair.** With a client that disconnects mid-response (`rudeclient`, or a two-write handler + a client that closes), show your server **survives** and logs the `EPIPE`. Then remove `signal(SIGPIPE, SIG_IGN)` and show the identical scenario **kills** the process — report the exact exit code and decode it. State which "present but not working" family this belongs to.

## Part 3 — Robustness Under Load (20 points)

**[8] No fd leak.** Watch `/proc/<pid>/fd` (count) across ≥10 000 requests from `bench`. Report before and after; the delta must be 0. If it is not, find the missing `close`.

**[8] No memory leak.** Watch `VmRSS` from `/proc/<pid>/status` across ≥5 rounds of ≥10 000 requests. Report the table; it must be flat (a one-time warm-up is fine). Name what each resident kB is.

**[4] Capacity.** Use `bench` to measure throughput at 1, 2, 4, 8 (and if you can, 16) workers for a **trivial** handler and a **blocking** handler (add a `/slow` endpoint that sleeps). Present both tables and explain, in two sentences, why one is flat and the other scales linearly. Report mean **and p99** latency for one configuration.

## Part 4 — The Hardened Parser (20 points)

**[8] Safe parsing.** Bounded reads, a request-line length cap, no unchecked `Content-Length`, no `gets`-shaped code. Show the code that rejects an over-long request line instead of overflowing.

**[8] Build with the guards on.** `-Wall -Wextra -Werror`, `-fstack-protector-strong`, `-D_FORTIFY_SOURCE=2`, and a sanitizer build target (`-fsanitize=address,undefined`). Show the Makefile and one ASan/UBSan run over your own traffic.

**[4] Fuzz it.** Wrap your parser in `LLVMFuzzerTestOneInput` and fuzz it under `-fsanitize=fuzzer,address` (clang; AFL is not installed). Report how long it ran, how many executions, and either the bug it found (with the reproducer) or that it survived N million iterations clean. Plant one bug and show the fuzzer locating it.

## Part 5 — Running Unattended (16 points)

**[6] Privilege.** Explain, with the measured `bind :80 → EACCES`, why a real web server starts privileged and drops. Write the drop sequence (`setgroups`/`setgid`/`setuid`, correct order) and — the graded part — show the `Groups:` line of `/proc/self/status` with and without `setgroups(0,NULL)`, exhibiting the leftover groups. (You will read/reason this on the lab machines rather than run it as root; say so.)

**[6] Supervision + limits.** Write a `systemd` unit with `Restart=on-failure`, `User=`, `MemoryMax`, `TasksMax`, and `AmbientCapabilities=CAP_NET_BIND_SERVICE`. Explain what each line replaces from a self-daemonizing server, and relate `MemoryMax`/`TasksMax` to your Week 11 measurements.

**[4] Isolation (reflection).** In one paragraph, describe how you would run this daemon inside the Week 11 mini-container (namespaces + seccomp allow-list for the syscalls it actually makes), and what an attacker who fully compromised the parser could and could not then reach.

---

## Report (`P2_*.pdf`)

Structure it by Part. **Every measured figure names its producing command.** A result that is an error code — `EACCES`, exit 141, exit 137, `EAGAIN`, a located ASan crash — is a finding to record and interpret, not a failure to hide: *a measurement that produces something forbidden or impossible is first a fact about the measurement.* Where the lab machine blocks something (binding :80, becoming another user), say so precisely and reason about what would happen where permitted — the same honesty the course modelled all term.

Close with **one page** connecting your daemon to the course: name at least six earlier weeks it draws on, and state which of your Part-2/Part-5 findings is a "present but not working" case and what single measurement revealed it.

## Grading (100 pts)

| Part | Points |
| --- | --- |
| 1 — pool + bounded queue, backpressure shown | 20 |
| 2 — self-pipe, graceful drain measured, SIGPIPE pair measured | 24 |
| 3 — fd delta 0, RSS flat, capacity tables + p99 | 20 |
| 4 — safe parser, guard build, fuzzed (bug found or N-million clean) | 20 |
| 5 — privilege drop + group finding, systemd unit, isolation reflection | 16 |

**Academic integrity.** The daemon is yours, including the Week 5–6 core you reuse. Discussing approaches is fine; sharing code is not. Cite every man page, and cite the reference `httpd` structure only if you were shown it in lab (you were not — the instructor build is not distributed). The harness (`bench`, `rudeclient`) is provided and need not be cited.

---

*PROG 201 · Project 2 · © CSE Department*
