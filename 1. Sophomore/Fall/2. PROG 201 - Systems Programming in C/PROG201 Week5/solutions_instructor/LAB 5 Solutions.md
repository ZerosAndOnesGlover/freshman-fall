# PROG 201 · Lab 5 Solutions
## Stress Testing a Server — Instructor Only

---

**Do not distribute.** Part B's two identical numbers and Part C's 7,637 are the lab, and both are spoiled by reading ahead.

**Machine these numbers came from:** Linux 7.0.0-30-generic, gcc 13.3.0 (Ubuntu 24.04), Intel i5-8250U, **4 physical cores / 8 hardware threads**, `somaxconn` 4,096, `RLIMIT_NOFILE` 1,048,576, ephemeral range 32768–60999. **All traffic is loopback**, which flatters every model equally and removes the network as a variable — say so if a student asks whether the numbers transfer.

> **`ab` is not installed and cannot be.** The curriculum specifies Apache Benchmark; `apache2-utils`
> is not present on the BH 215 image and a student account cannot add it. The lab has students write
> the load generator instead, which exercises L18 §4 properly. Recorded in the syllabus and in
> [[PROG 201 Scheduling Notes]] §11.

---

## 1. The Four TODOs

The scaffolding — `finish`, `worker`'s loop structure, `cmp`, `main`, and all of `server.c`, `hold.c` and `nagle.c` — is provided.

```c
static int start_one(struct slot *s, int ep)
{
    if (atomic_fetch_add(&issued, 1) >= TOTAL) { atomic_fetch_sub(&issued, 1); return 0; }
    int fd = socket(AF_INET, SOCK_STREAM | SOCK_NONBLOCK, 0);
    if (fd < 0) { atomic_fetch_add(&done_err, 1); return 0; }
    struct sockaddr_in a = { .sin_family = AF_INET, .sin_port = htons(PORT),
                             .sin_addr.s_addr = htonl(INADDR_LOOPBACK) };
    s->fd = fd; s->state = 1; s->t0 = now(); s->sent = 0; s->got = 0;
    int rc = connect(fd, (struct sockaddr *) &a, sizeof a);
    if (rc < 0 && errno != EINPROGRESS) { close(fd); s->state = 0; atomic_fetch_add(&done_err,1); return 0; }
    struct epoll_event e = { .events = EPOLLOUT, .data.ptr = s };
    epoll_ctl(ep, EPOLL_CTL_ADD, fd, &e);
    return 1;
}

/* ---- and the three states, inside worker()'s event loop ---- */

            if (s->state == 1) {
                int err = 0; socklen_t l = sizeof err;
                getsockopt(s->fd, SOL_SOCKET, SO_ERROR, &err, &l);
                if (err) { finish(s, ep, 0); live--; if (start_one(s, ep)) live++; continue; }
                s->state = 2;
            }
            if (s->state == 2) {
                ssize_t k = write(s->fd, REQ + s->sent, sizeof REQ - 1 - s->sent);
                if (k < 0) { if (errno != EAGAIN) { finish(s, ep, 0); live--; if (start_one(s,ep)) live++; continue; } }
                else s->sent += k;
                if (s->sent == sizeof REQ - 1) {
                    s->state = 3;
                    struct epoll_event e = { .events = EPOLLIN, .data.ptr = s };
                    epoll_ctl(ep, EPOLL_CTL_MOD, s->fd, &e);
                }
                continue;
            }
            if (s->state == 3) {
                char buf[4096];
                ssize_t k = read(s->fd, buf, sizeof buf);
                if (k > 0) { s->got += k; continue; }
                int ok = (k == 0 && s->got > 0);
                finish(s, ep, ok);
                live--;
                if (start_one(s, ep)) live++;
            }```

Builds clean under `gcc -Wall -Wextra -O2 -g -std=c11 -o load load.c -lpthread`.

---

## 2. Where Students Get Stuck

| # | Symptom | Cause | What to say |
| --- | --- | --- | --- |
| 1 | `ok 0  err 0`, finishes instantly | `start_one` still returns 0 | The skeleton's placeholder. TODO 1 |
| 2 | `err` equals the request count | `EINPROGRESS` treated as a failure | L18 §4. "What does a non-blocking connect return?" |
| 3 | `ok` is right but every latency is ~0 | `s->t0` set after `connect` returns, or never | The clock starts when the request starts |
| 4 | Hangs at the end with `live > 0` | `live` not decremented, or `start_one`'s return value ignored | Have them print `live` each iteration |
| 5 | `ok` far below `TOTAL`, no errors | The budget claimed twice, or `issued` not `atomic` | Four threads share it |
| 6 | Works at conc 20, wedges at conc 500 | Client hit `EADDRNOTAVAIL` — out of ephemeral ports | **This is Q8 arriving early.** Congratulate them |

**Symptom 6 is worth engineering for.** A section that has run several Part B sweeps will start hitting it; `ss -tan state time-wait | wc -l` is the diagnosis and waiting sixty seconds is the cure. Tell the room at the start: *if your generator suddenly reports errors, look at `TIME_WAIT` before you look at your code.*

---

## 3. Reference Measurements

**Part B(a) — trivial work, concurrency 50, 20,000 requests**

| model | req/s | p50 | p99 |
| --- | --- | --- | --- |
| iterative | 46,810 | 0.94 ms | 3.96 ms |
| fork | 15,038 | 3.07 ms | 5.70 ms |
| thread | 39,186 | 1.16 ms | 2.18 ms |
| pool (8) | 50,687 | 0.90 ms | 1.48 ms |
| epoll | 42,985 | 0.99 ms | 1.91 ms |

**Part B(b) — 2 ms of blocking work, concurrency 50, 3,000 requests**

| model | req/s | p50 |
| --- | --- | --- |
| iterative | 434 | 111.40 ms |
| fork | 13,740 | 3.34 ms |
| thread | 18,214 | 2.34 ms |
| pool (8) | 3,469 | 13.84 ms |
| epoll | 434 | 111.56 ms |

**Part B(c) — 500 µs of CPU work**

| model | req/s |
| --- | --- |
| iterative | 1,912 |
| fork | 8,434 |
| thread | 7,004 |
| pool (8) | 12,761 |
| epoll | 1,887 |

**Pool sizing, 2 ms blocking:** 1 → 437, 8 → 3,487, 32 → 14,085, 64 → 14,471, 128 → 18,667 req/s.

**Part C:** epoll held 20,000 connections with RSS 1,416 → 1,416 kB. Thread: `pthread_create failed after 7637 connections: Resource temporarily unavailable`, RSS 1,416 → 64,864 kB.

**Part D:** Nagle 38.963 ms against `TCP_NODELAY` 0.209 ms. `TIME_WAIT` 11,261 after 20,000 requests, against 28,232 ephemeral ports.

Run-to-run variation is 10–20% on throughput and much less on the ratios. **The three numbers that do not vary are 434, 434 and 7,637**, because none of them is a performance figure — they are ceilings.

---

## 4. Answers

**Q1 — the iterative server came second.**

Because the response takes about 20 µs to produce and concurrency buys you nothing when there is nothing to overlap. Everything except `fork` lands within 30% of everything else, and `fork` loses only because it spends 164 µs building a process (Week 3 L10 §3) to do 20 µs of work.

The general lesson: **a "Hello, world" benchmark measures your accept loop and your kernel, not your architecture.** Full marks require the second sentence; the observation alone is [2 of 4].

**Q2 — why `epoll` was not faster.**

`epoll` gives concurrency over **waiting for registered descriptors**. It gives none at all over a blocking call inside the handler, because that call runs on the event loop's single thread — so while it runs, every ready connection waits. 2 ms per request on one thread is 500 req/s, and 434 is that number with overhead.

Look for the phrase "one thread" or equivalent. A student who says "epoll is slow for CPU work" has half of it; ask them what the loop is doing during the `usleep`.

**Q3 — `getaddrinfo` in an event loop.**

It blocks — potentially for seconds on a DNS timeout — so the numbers become Q2's numbers or worse. The two standard fixes: **a resolver thread or pool** that the event loop hands names to, or **an asynchronous resolver** (c-ares, or `getaddrinfo_a`, or the resolver built into the event library). Accept "cache the result" as a partial answer with a note that it does not fix the first lookup.

**Q4 — the pool won the CPU workload.**

CPU-bound work needs exactly as many *runnable* threads as there are cores. The pool has 8 on a machine with 4 physical cores and 8 hardware threads; thread-per-connection has **50**, all runnable, so they context-switch against each other and against the queue, and every switch is scheduler time not spent computing. Iterative and `epoll` are at 1 thread, hence ~1,900 req/s ≈ 1/0.0005.

Full marks need the core count in the answer.

**Q5 — where 7,637 comes from.**

The **cgroup's `pids.max`**, read at `/sys/fs/cgroup/<path>/pids.max` — **7,671** on these machines, of which the shell's scope was already using about 30. Week 3 L10 §3 measured the ceiling at 7,643 threads from the other direction, with `maxthreads.c`.

Reducing the stack size does not help because the stack is **address space, not memory** (Week 4 L13 §3): 8 MiB stacks gave 7,643 threads and 64 KiB stacks gave 7,644. The advice is about 32-bit address exhaustion and is thirty years out of date.

Marks: naming the cgroup [2], where to read it [1], the stack answer with the reason [2].

**Q6 — what happened to client 10,000.**

Step by step: `connect` **succeeded** — the kernel completed the three-way handshake itself and put the connection on the listen queue (L16 §4), with no involvement from the server process. `accept` returned it. `pthread_create` returned `EAGAIN`. The server called `close`, which sent a FIN. The client's next `read` returned **0** — an orderly close with no bytes — which to an HTTP/1.0 client is an empty response, not an error.

**So the client saw a successful connection and a blank page**, and `hold.c`, which never reads, saw nothing wrong at all and reported 20,000 connections held.

What the server should do: **check the return value**, and on failure send a `503 Service Unavailable` with a `Retry-After` before closing, or queue the descriptor for a worker to pick up later. Either is better than a silent close, because a client that is told is a client that can back off. Accept "shed load explicitly" in any form.

This is the best question on the paper. It joins Week 2's untorn records and Week 4's 339×: **the failure that does not announce itself.**

**Q7 — the 39 ms.**

**Nagle's algorithm**, on the **sender**: do not send a small segment while an earlier small segment is unacknowledged. **Delayed ACK**, on the **receiver**: wait up to 40 ms before acknowledging, in case there is data to piggyback on. The sender waits for an ACK that the receiver is deliberately withholding, and the delayed-ACK timer breaks the tie.

Two fixes: **`TCP_NODELAY`** treats the symptom and is what every RPC library and HTTP server does; **writing the message in one call** (or `writev`) removes the cause, because there is never a second small segment. Prefer the second, take the first — a student who says "both, and here is why" has the right answer.

**Q8 — `TIME_WAIT`.**

**(a)** Whichever side **closes first** goes into `TIME_WAIT`, and in HTTP/1.0 with `Connection: close` that is normally the server — but the benchmark's clients are the ones opening a new *ephemeral port* each time, and it is the client's port space that runs out. In our runs the server's listening port is one address and the client burned 11,261 of its 28,232 ports. Accept either framing if it names the four-tuple.

**(b)** `connect` fails with **`EADDRNOTAVAIL`** — no ephemeral port is free.

**(c)** The fix that is a fix: **stop opening a connection per request** — HTTP keep-alive, connection pooling. `net.ipv4.tcp_tw_reuse` and a shorter `tcp_fin_timeout` are the two sysctls that help and trade away the guarantee `TIME_WAIT` exists to provide.

---

## 5. Checkoff

The four boxes are in the lab sheet. In practice:

- **Ask them to point at the two identical numbers** in Part B(b) before they explain them. Recognition first, explanation second.
- **Q6 out loud, always.** The written answer is usually "the server closed it"; the interesting part is that the *client* thought it succeeded.
- The extension — keep-alive in the load generator — is the right forty minutes for a fast pair. Their `TIME_WAIT` count should drop by an order of magnitude and their request rate should rise; both are worth writing on the board.

**Timing.** Setup 5, Part A 40 (it is the bulk), Part B 30, Part C 25, Part D 15. That is 115 against a 110-minute session, so **let Part D go if the room is behind** — it is the one part that is fully covered in L18 and loses least by being read rather than run.

---

*PROG 201 · Week 5 · Lab 5 Solutions · Instructor Only · © CSE Department*
