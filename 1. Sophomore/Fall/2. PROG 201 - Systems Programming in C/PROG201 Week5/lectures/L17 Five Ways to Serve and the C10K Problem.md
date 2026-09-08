# PROG 201 · Systems Programming in C
## Week 5 · Lecture 2 of 3
### Five Ways to Serve, and the C10K Problem

---

**Reading:** APUE §16.4–16.5 · TLPI Ch. 60 · Kegel, *The C10K Problem* (1999, updated to 2014) · **Previous:** L16 · **Next:** L18 — `epoll` and non-blocking sockets

---

## 1. Every Server Has the Same Shape

```
accept a connection
    read the request
    do the work
    write the response
    close
```

The only question is **what "do the work" runs on**, and there are five answers. All five are in `server.c`, all five serve the same trivial HTTP response, and the differences between them are the subject of the lecture.

| Model | The connection runs on |
| --- | --- |
| iterative | the accept loop itself |
| fork-per-connection | a fresh process |
| thread-per-connection | a fresh thread |
| thread pool | one of *N* long-lived threads |
| event-driven | the accept loop, interleaved with every other connection |

---

## 2. The Five, in Code

**Iterative** — the whole server:

```c
for (;;) { int c = accept(ls, NULL, NULL); serve(c); }
```

Correct, and it handles exactly one client at a time. Everyone else waits in the listen queue (L16 §4).

**fork-per-connection** — the model Unix was designed around:

```c
int c = accept(ls, NULL, NULL);
if (fork() == 0) { close(ls); serve(c); _exit(0); }
close(c);
```

Two closes and both matter. **The child closes the listening socket** or a restart of the parent finds the port held. **The parent closes the connection** or the descriptor leaks and the client never sees EOF — Week 1 L06 §4's rule, in a new place. And `signal(SIGCHLD, SIG_IGN)` or you accumulate zombies (Week 0 L02).

**thread-per-connection:**

```c
pthread_t t;
pthread_create(&t, NULL, thread_body, (void *)(long) c);
pthread_detach(t);                      /* or the thread leaks (Week 3 L10) */
```

Note the argument is the descriptor passed by value through a `void *`. Passing `&c` is the bug from Week 3 L10's exercises, and here it corrupts a live connection rather than a counter.

**Thread pool** — Week 3's PS 3, with descriptors in the queue instead of function pointers. Bounded, so a load spike queues rather than forking ten thousand things.

**Event-driven** — one thread, non-blocking sockets, `epoll` (L18):

```c
for (;;) {
    int n = epoll_wait(ep, out, 256, -1);
    for (int i = 0; i < n; i++)
        if (out[i].data.fd == ls) accept_all();
        else                      handle(out[i].data.fd);
}
```

---

## 3. Measured: The Trivial Case

`load.c` opens *C* concurrent connections and issues 20,000 requests, each a fresh connection. Concurrency 50, and the server does nothing but reply:

| model | req/s | p50 | p99 |
| --- | --- | --- | --- |
| iterative | 46,810 | 0.94 ms | 3.96 ms |
| fork | 15,038 | 3.07 ms | 5.70 ms |
| thread | 39,186 | 1.16 ms | 2.18 ms |
| **pool (8 workers)** | **50,687** | 0.90 ms | 1.48 ms |
| epoll | 42,985 | 0.99 ms | 1.91 ms |

**The iterative server is second fastest.** Read that again before drawing conclusions from it.

When the work is nothing, concurrency buys nothing, and everything except `fork` is within 30% of everything else. `fork` is three times slower because it is paying 164 µs per connection to build a process (Week 3 L10 §3) in order to do 20 µs of work.

**This table is the reason benchmarks mislead.** A "Hello, world" server measures your accept loop and your kernel, not your architecture. Every architectural difference shows up only when the work is real, which is §4.

---

## 4. Measured: When the Work Blocks

Now each request waits 2 ms — one call to a database, a cache, another service. That is what a real request does. Same client, same concurrency:

| model | req/s | p50 |
| --- | --- | --- |
| iterative | **434** | 111.40 ms |
| fork | 13,740 | 3.34 ms |
| thread | **18,214** | 2.34 ms |
| pool (8 workers) | 3,469 | 13.84 ms |
| **epoll** | **434** | **111.56 ms** |

Three things changed and one of them should stop you.

**The iterative server collapsed to 434 req/s**, which is 1/0.002 and therefore exactly right: one request at a time, each taking 2 ms.

**`fork` and threads went up**, because now there is something to overlap. The 164 µs of `fork` is worth paying to overlap 2 ms of waiting.

**And the event-driven server is at 434 req/s. The same number as the iterative one.**

---

## 5. Why `epoll` Was Not Faster

Because **a blocking call in an event loop blocks every connection.**

`epoll` gives you concurrency over *waiting for I/O it knows about*: sockets you have registered, which it can watch while your thread does something else. It gives you nothing at all over a `usleep`, a synchronous database driver, a `read` of a local file, a DNS lookup through `getaddrinfo`, or a computation. Those all happen **on the event loop's one thread**, and while one of them runs, ten thousand ready connections wait.

This is the single most common way an event-driven server is written wrongly, and the symptom is exactly the table above: the architecture that is supposed to handle ten thousand connections handles one at a time. The rules that follow:

- **Everything in an event loop must be non-blocking**, or handed to a thread pool.
- **`getaddrinfo` blocks.** So does `gethostbyname`, so does any library that opens a file, so does most of `libpq`. An event-driven server needs an asynchronous resolver or a resolver thread.
- **A CPU-bound handler is a blocking handler.** With 500 µs of computation per request instead of 2 ms of waiting, `epoll` managed **1,887 req/s** against the pool's 12,761 — the same failure with a different cause.

**The honest summary of the event-driven model:** it is the best way to wait for many sockets and the worst place to do work. Real servers are hybrids — an event loop for I/O and a pool for anything that blocks — and nginx, Node and Redis are all built that way, with the "single-threaded" claim covering only the loop.

---

## 6. Measured: When the Work Is CPU

Same test, 500 µs of computation per request rather than 2 ms of waiting:

| model | req/s |
| --- | --- |
| iterative | 1,912 |
| fork | 8,434 |
| thread | 7,004 |
| **pool (8 workers)** | **12,761** |
| epoll | 1,887 |

**Now the pool wins**, because CPU-bound work needs exactly as many runnable threads as there are cores, and the pool has that number while thread-per-connection has fifty of them fighting over eight hardware threads. It is Week 3 L12 §5's worker-sizing result arriving with sockets attached.

And the pool's size follows the work. Back on the 2 ms blocking workload:

| pool workers | req/s |
| --- | --- |
| 1 | 437 |
| 8 | 3,487 |
| 32 | 14,085 |
| 64 | 14,471 |
| 128 | 18,667 |

**Eight workers is right for CPU work and catastrophically wrong for blocking work.** Week 3's formula says why: `threads ≈ cores × (1 + wait / service)`, and with 2 ms of wait against microseconds of service the ratio is enormous. A pool sized to `nproc` in a server that talks to a database is the most common capacity bug there is.

---

## 7. The C10K Problem

In 1999 Dan Kegel asked why a machine that could easily hold ten thousand connections' worth of data could not hold ten thousand connections. The answer at the time was that every model above needs a thread or a process per connection, and the per-connection cost was too high.

Measured, on this laptop, with `hold.c` opening connections and never sending anything:

**Event-driven:**

```
    2000 connections: server RSS 1 MiB
   10000 connections: server RSS 1 MiB
   20000 connections: server RSS 1 MiB
held 20000 connections
server RSS 1416 -> 1416 kB  = 0.0 kB per connection
```

**Twenty thousand idle connections, and the server's resident memory did not move.** A connection in an event loop is a descriptor, an epoll registration and whatever state you keep — a few hundred bytes.

**Thread-per-connection:**

```
pthread_create failed after 7637 connections: Resource temporarily unavailable
```

**It stops at 7,637.** And that number should look familiar: Week 3 L10 §3 measured this machine's ceiling at **7,643 threads**, set by the cgroup's `pids.max` of 7,671. The same limit, reached from a completely different direction.

Two details of that failure are worth more than the number:

- **The clients did not notice.** `hold.c` reports "held 20000 connections" because every `connect` succeeded — the kernel completed the handshakes and queued them (L16 §4). The server accepted them and then quietly closed the ones it could not get a thread for. **From outside, the server looked fine and served a third of its clients.**
- **The failure mode is `EAGAIN` from `pthread_create`**, which a server that does not check the return value turns into a segfault or an ignored connection. Week 3 L10 §4: pthreads functions return the error number.

**C10K is solved, and it was solved by `epoll` and by memory getting cheaper.** The modern version is C10M, and the answer to that is to stop going through the kernel per packet at all — which is what DPDK and `io_uring` are about, and which is L18 §7.

---

## 8. Choosing

| Situation | Model | Because |
| --- | --- | --- |
| A tool that serves one client at a time | **iterative** | It is four lines and it is correct |
| Untrusted per-connection code; a crash must not take the server down | **fork** | Isolation. 164 µs is cheap insurance |
| A handful of long-lived connections, each doing blocking work | **thread-per-connection** | Simplest code that overlaps; the ceiling is thousands, not tens |
| Many short requests, work is CPU-bound | **pool sized to cores** | 12,761 against 7,004 |
| Many short requests, work blocks | **pool sized to `cores × (1 + wait/service)`** | 18,667 against 3,487 |
| Ten thousand mostly-idle connections | **event-driven** | 20,000 connections, 0 kB each |
| All of the above at once | **event loop + pool**, and it is what you will actually build | §5 |

**The question to ask first is not "which is fastest".** It is: *what does a request spend its time doing?* Waiting, computing, or nothing — and the tables above give a different winner for each.

---

## Summary

- Every server is `accept`, read, work, write, close. The models differ only in **what the work runs on**.
- With **trivial work**, the iterative server is second fastest and the whole comparison is meaningless. A "Hello, world" benchmark measures your kernel.
- With **2 ms of blocking work**: iterative 434 req/s, threads 18,214, and **`epoll` also 434** — because a blocking call in an event loop blocks every connection.
- **An event loop is the best way to wait and the worst place to work.** Real servers are event loop plus pool.
- With **CPU-bound work**, the pool wins (12,761 against 7,004), sized to the cores.
- Pool size follows the work: for 2 ms of blocking, 8 workers gave 3,487 req/s and 128 gave **18,667**.
- **C10K, measured:** event-driven held **20,000 connections with no measurable memory growth**; thread-per-connection failed at **7,637** with `EAGAIN` — the same cgroup ceiling Week 3 found — and **the clients could not tell.**

---

## Exercises

1. Add `SO_REUSEPORT` and run four copies of the iterative server on one port. Measure the total throughput against one copy. What did the kernel do for you?
2. Instrument the `fork` server to report how long `fork` takes and how long `serve` takes. At what ratio does forking stop being worth it?
3. Set the pool to 1 worker and the event loop to serve the same 2 ms workload. Explain why they give the same number, in one sentence about how many things can be in progress.
4. Make the event-driven server's "work" a non-blocking timer registered with the same `epoll` (see `timerfd_create`). Re-run §4's test. What number do you get now, and why is it a different program?
5. Run the thread server against 10,000 concurrent connections and count how many clients got a response. Then add a check on `pthread_create`'s return value that closes the connection with a 503 instead. Which is better, and for whom?
6. Find the crossover: with how much work per request does `fork` overtake the iterative server?
7. Read Kegel's C10K page. Which of the six approaches it lists have you now measured, and which two does Linux no longer have?

---

*PROG 201 · Week 5 · L17 · © CSE Department*
