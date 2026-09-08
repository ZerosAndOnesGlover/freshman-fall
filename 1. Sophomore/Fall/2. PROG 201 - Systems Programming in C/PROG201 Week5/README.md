# PROG 201 · Systems Programming in C
## Week 5: Network Programming — Sockets

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101; CS 201 as co-requisite
**Assessment for this course (overall):** Problem Sets 35%, Projects 25%, Midterms 25%, Final 15%
**This week's deliverables:** PS 5 (due Friday of Week 6) and **Quiz 5** (Tuesday, covers Week 4).
**Lab 4 is sat on the Monday of this week**; **Lab 5 covers this week and is sat on the Friday of Week 6, 16:00–17:50.**

> ### **Lab 5 is on a Friday, and it is the only one that is.**
> The Monday of Week 6 is **Fall Break**. Lab 5 moves to the Friday of Week 6 at 16:00–17:50 in
> BH 215 — and **PS 5 is due at 17:00 that day, while you are in the room.** Submit before the lab.
> [[PROG 201 Scheduling Notes]] records both.

---

### Why This Week Exists

Because "we'll use `epoll`, it handles ten thousand connections" is true, and the server that says it is often exactly as slow as a `for` loop.

Weeks 0–4 built everything a server needs: processes, descriptors, IPC, threads and memory. **This week connects them to another machine, and then asks which of those tools to use** — a question with five plausible answers, three of which are right depending on what a request spends its time doing.

Three ideas:

1. **A socket is a descriptor with two addresses.** Everything from Weeks 1–4 applies to it unchanged, including that a stream has no message boundaries and `write` is allowed to be short.
2. **The architecture only matters when the work is real.** With a trivial response, an iterative server beat three of the four concurrent ones. With 2 ms of blocking work it managed 434 req/s — and so did the event-driven one.
3. **Most of what goes wrong is visible from outside the process.** A full listen queue, eleven thousand `TIME_WAIT`s, a 40 ms round trip on loopback: `ss` shows all three and your program shows none of them.

---

### Learning Objectives

By the end of Week 5, you should be able to:

1. Write a TCP server — `socket`, `bind`, `listen`, `accept` — and a client, without looking them up.
2. Use `getaddrinfo` and loop over its results, and say why the loop matters.
3. Explain what `listen`'s backlog is, what happens past it, and read `ss -ltn`'s two queue columns.
4. Say why every listening socket needs `SO_REUSEADDR`, and what `TIME_WAIT` is protecting.
5. Handle short reads and writes, EOF, and `SIGPIPE`, and distinguish `shutdown` from `close`.
6. Describe five concurrency models and **choose between them from what a request does**, not from a benchmark.
7. **Explain why an event loop is exactly as slow as an iterative server when the handler blocks.**
8. Size a thread pool for blocking work and for CPU work, and get different answers.
9. State the C10K problem and both halves of its answer.
10. Explain why `epoll` is *O(ready)* and `poll` is *O(watched)*, and why `select` cannot be used at all above 1024.
11. Use level- and edge-triggered `epoll` correctly, and say what `EPOLLET` obliges you to do.
12. Handle `EAGAIN` on `read`, `write` and `accept`, and a non-blocking `connect` with `SO_ERROR`.
13. **Recognise a 40 ms latency as a protocol interaction**, and give two fixes.
14. Name the socket options that matter and the two whose defaults bite.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L16 Sockets TCP and the Calls]] | The API; byte order; `getaddrinfo`; **the listen queue holds `backlog+1` and drops the rest silently**; `TIME_WAIT` and `SO_REUSEADDR`, and **11,261 of them after 20,000 requests**; short writes, `SIGPIPE`, `shutdown` |
| [[L17 Five Ways to Serve and the C10K Problem]] | The five models measured on three workloads; **an iterative server that is second fastest**; **`epoll` at 434 req/s, the same as iterative**; pool sizing from 437 to 18,667; **20,000 connections at 0 kB, against 7,637 threads** |
| [[L18 epoll Non-Blocking Sockets and the Options That Matter]] | `poll` 4,827 µs against `epoll` **0.89 µs** at 16,000 fds; why `select` **cannot** be used; level against edge; `EAGAIN` in three places; **Nagle at 186×**; the options worth knowing; `sendfile` at 4,206 MiB/s |
| [[LAB 5 Stress Testing a Server]] | Build the load generator `ab` would have been. **Friday of Week 6** |
| `lab/server.c`, `lab/load.c`, `lab/hold.c`, `lab/nagle.c`, `lab/bench.sh`, `lab/Makefile` | The five-model server (provided), the generator skeleton, and two experiments |
| [[PS 5 A Concurrent HTTP Server]] | A real HTTP/1.0 server: parsing, files, path traversal, two concurrency models, measured. Due **Friday of Week 6** |
| [[PROG201 Week5/assignments/QUIZ 5 Week 5 Tuesday\|QUIZ 5 Week 5 Tuesday]] | Ten minutes, covers **Week 4**, answer key printed |
| [[PROG201 Week5/resources/Reading Guide Week 5\|Reading Guide Week 5]] | APUE Ch. 16, TLPI Ch. 56–63, and **Kegel's C10K page** |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Ask what a request spends its time doing. Then choose.**

| The request mostly… | Winner | req/s | The loser, and why |
| --- | --- | --- | --- |
| does nothing | *anything* | 39k–51k | Even iterative: 46,810 |
| **waits** (2 ms of I/O) | thread-per-connection | **18,214** | **`epoll`: 434** — a blocking handler blocks every connection |
| **computes** (500 µs) | pool sized to cores | **12,761** | `epoll`: 1,887, thread: 7,004 |
| **waits, at 10,000 clients** | event-driven | 20,000 conns, **0 kB each** | threads: **`EAGAIN` at 7,637**, and nobody noticed |

**No row of that table is the same as the row above it**, and the machine, the client and the code were identical throughout. The only thing that changed was what the handler did while it had the connection.

And the thing that makes it dangerous: **the first row is the one everybody benchmarks.**

---

### Assessment Reminder

**Labs and quizzes carry no weight** and are still required. **Quiz 5 is at the start of Tuesday's lecture and covers Week 4**; the answer key is printed in the paper.

> **Two labs touch this week.** **Lab 4** — Week 4's JIT — is sat on the **Monday of this week**.
> **Lab 5** covers this week and is sat on the **Friday of Week 6, 16:00–17:50**, because the Monday
> of Week 6 is Fall Break. It is the only Friday lab of the term.

Both are tracked in [[_PROG 201 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 1 is the substrate** — a socket is a descriptor, `write` is short, EOF is 0, and `write_all` is mandatory. **Week 2's framing problem returns** without `PIPE_BUF` to hide behind. **Week 3's pool is L17's fastest CPU-bound server**, and its 7,643-thread cgroup ceiling is L17 §7's 7,637 connections. **Week 4's `mmap`** is L18 §8's middle row, and `sendfile` is the argument taken one step further.

**Sideways:** **CS 201 Week 5 is on the memory hierarchy and I/O**; the byte-order conversions in L16 §2 are its endianness lecture with a consequence attached.

**Forward:** **Week 6's shell** is `fork`/`exec`/`waitpid` with a parser and job control — the same process machinery, aimed at a terminal instead of a socket. **Week 9 profiles** something like this properly, rather than by timing the whole thing. **Week 11's containers** are what you put a server in. **Project 2 is a networked multi-threaded server**: PS 5's parsing, plus Week 3's pool, plus this week's measurements.

---

*PROG 201 · Week 5 · © CSE Department*
