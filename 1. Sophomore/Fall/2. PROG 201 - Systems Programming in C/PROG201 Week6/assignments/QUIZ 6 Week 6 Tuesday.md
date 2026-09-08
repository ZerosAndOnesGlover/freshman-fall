# PROG 201 · Quiz 6
## Administered: Tuesday, Week 6 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 5** — sockets, TCP, concurrent server architectures, the C10K problem, `epoll`, socket options.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.
>
> **Fall Break was yesterday**, so this is the week's first session. **PS 5 is due Friday at 17:00
> and Lab 5 is sat 16:00–17:50 that day** — submit before you come.

---

**Q1.** Give the four calls a TCP server makes, in order, and say which one returns a descriptor you can read from.

&nbsp;

&nbsp;

---

**Q2.** You call `listen(fd, 4)` and never call `accept`. Five clients connect instantly and the sixth hangs for two seconds and gives up. Explain both halves.

&nbsp;

&nbsp;

---

**Q3.** A server restarts and `bind` fails with `Address already in use`, though nothing is listening. What is holding the address, why does it exist, and what is the one-line fix?

&nbsp;

&nbsp;

---

**Q4.** With 2 ms of blocking work per request, an iterative server managed 434 req/s and an `epoll` server managed 434 req/s. Explain.

&nbsp;

&nbsp;

---

**Q5.** Thread-per-connection stopped at 7,637 connections with `EAGAIN`, and the clients did not notice. Give the limit, and describe what client number 10,000 actually experienced.

&nbsp;

&nbsp;

---

**Q6.** At 16,000 descriptors, one `poll` call costs 4,827 µs and one `epoll_wait` costs 0.89 µs. Give the reason, in terms of what each interface makes the kernel do.

&nbsp;

&nbsp;

---

**Q7.** A request/response exchange over **loopback** takes 39 ms per round trip. Name the two algorithms, and give the fix that addresses the cause rather than the symptom.

&nbsp;

&nbsp;

---
---

# Answer Key

*Mark your own. Be honest — nobody else will see this.*

---

**Q1.** **`socket`, `bind`, `listen`, `accept`.** **`accept`** returns the readable descriptor — a *new* one, for one connection. The listening socket is not readable or writable and stays open for the next `accept`; treating it as the connection is the classic first bug. *(L16 §2.)*

---

**Q2.** **The queue holds `backlog + 1`** — Linux's documented off-by-one — so five connections completed. Measured: `listen(4)` → 5, `listen(16)` → 17.

The sixth **hung rather than being refused** because the kernel **drops the SYN silently** when the accept queue is full. No RST is sent, so the client gets no `ECONNREFUSED`; its TCP retransmits after 1 s, 2 s, 4 s. **A full listen queue presents as latency, not as an error.** *(L16 §4.)*

---

**Q3.** A **`TIME_WAIT`** connection on that address — whichever side closed first waits 2×MSL (60 s on Linux) so that a delayed duplicate packet cannot be delivered to a new connection reusing the same four-tuple. It is a correctness mechanism.

The fix: **`setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one)`** before `bind`. Set it on every listening socket you write; there is no case where you want the alternative. *(L16 §5.)*

---

**Q4.** **A blocking call in an event loop blocks every connection on it.** `epoll` gives concurrency over *waiting for registered descriptors*, not over anything the handler does — and the handler runs on the loop's single thread. 2 ms per request on one thread is 500 req/s; 434 is that with overhead.

The consequences: everything in an event loop must be non-blocking or handed to a pool, **`getaddrinfo` blocks**, and a CPU-bound handler is a blocking handler (the same test with 500 µs of computation gave 1,887 req/s). *(L17 §5.)*

---

**Q5.** The **cgroup's `pids.max`** — 7,671 on these machines, which Week 3 measured from the other direction as a 7,643-thread ceiling. Not memory: threads cost 3.2 kB each here, and shrinking the stack buys nothing.

Client 10,000: **`connect` succeeded** — the kernel completed the handshake itself and queued the connection. The server `accept`ed it, `pthread_create` returned `EAGAIN`, and the server called `close`, sending a FIN. The client's `read` returned **0**, which to an HTTP/1.0 client is an empty response rather than an error. **It saw a successful connection and a blank page.** *(L17 §7.)*

---

**Q6.** **`select` and `poll` are stateless**: you hand the kernel the whole descriptor set on every call and it walks all of it — *O(watched)*, and no implementation can avoid it.

**`epoll` is stateful**: `epoll_ctl` registers a descriptor once and the kernel attaches a callback, so `epoll_wait` returns a ready list that was built as events arrived — *O(ready)*. Hence 0.89 µs at 16,000 descriptors and 0.72 µs at ten. **This is the answer to C10K.** *(L18 §1.)*

---

**Q7.** **Nagle's algorithm** on the sender (do not send a small segment while an earlier one is unacknowledged) and **delayed ACK** on the receiver (wait up to 40 ms in case there is data to piggyback on). Each waits for the other; the delayed-ACK timer breaks the tie.

`TCP_NODELAY` treats the symptom and is what every HTTP server and RPC library does. **The fix that addresses the cause is to send the message in one call** — build header and body in one buffer, or use `writev` — so there is never a second small segment. *(L18 §5.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L16 §2 and §4 |
| **Q3** | **L16 §5** — and PS 5 needs it on the first line of your server |
| **Q4, Q5** | **L17 §5 and §7** — these are the week, and Lab 5 measures them on Friday |
| Q6 | L18 §1 |
| Q7 | L18 §5 |

**Q4 is the one that recurs**, and it is this term's fourth appearance of the same shape: a measurement that looks fine (Week 2's untorn records), an implementation that flatters itself (Week 4's 339×), a benchmark that measures the wrong thing (Lab 5's "Hello, world"), and now an architecture that is only fast on the workload nobody has.

---

*PROG 201 · Week 6 · Quiz 6 · covers Week 5 · ungraded*
