# CS 201 · Computer Organization & Architecture
## Week 8 · Lecture 3 of 3
### The Application Layer, and the Cost of a Round Trip

---

**Reading:** CS:APP §11.5–11.6 · **Previous:** L26, TCP

---

## 1. The Socket API Is the Boundary

Everything below this line is the kernel's problem. Everything above is yours.

| Call | What it does |
|---|---|
| `socket()` | Create an endpoint. Returns a **file descriptor** |
| `bind()` | Attach a local address and port |
| `listen()` | Mark it as accepting connections |
| `accept()` | Take one connection off the queue — **returns a new fd** |
| `connect()` | Initiate the handshake |
| `send`/`recv` | Move bytes |
| `close()` | Begin the four-way teardown |

**The file descriptor is the whole design.** A socket is an `int`, and `read`, `write`, `poll`, `select` and `epoll` work on it exactly as on a file. **This is Week 6's indirection layer used again**: the kernel maps a small integer to whatever object it likes, and the uniformity is what makes shells, pipes and redirection possible.

**`accept` returning a *new* descriptor is the part people misread.** The listening socket keeps listening; each connection gets its own fd. **A server with 10 000 clients has 10 001 descriptors.**

---

## 2. Connection Setup Is Not Free

```
UDP loopback          connect  11.6 us
TCP loopback          connect 107.1 us
```

*(Measured.)* **Nine times more**, and on loopback there is no network at all — this is the handshake's software cost.

**On a real link it is a full round trip**, which on the measured internet path is 183 ms. **The handshake is not overhead you can tune away; it is a physical property of the distance.**

**UDP's `connect` does not send anything.** It records the peer address locally so later `send` calls need no destination. **There is no handshake because there is no connection** — which is exactly why UDP is what DNS, QUIC and most game protocols use for short exchanges.

---

## 3. Message Size Dominates Everything

Same TCP loopback connection, same code, different message size:

| message | round trip | throughput |
|---:|---:|---:|
| 64 B | 18.6 μs | **6.6 MiB/s** |
| 4 KiB | 21.2 μs | **369.3 MiB/s** |
| 64 KiB | 51.3 μs | **2436.1 MiB/s** |

*(Measured.)*

**A 1024× larger message costs 2.8× the time and delivers 369× the throughput.**

**This is exactly the shape of Week 7's storage curve**, and for exactly the same reason: **a fixed per-operation cost — two system calls, the TCP state machine, socket buffer management, scheduler wakeups — amortised over more bytes.** At 64 bytes you are measuring the software stack; at 64 KiB you are measuring memory bandwidth.

> **The general rule, now seen three times in this course** — Week 4's cache lines, Week 7's storage
> blocks, and here: **when a fixed cost is charged per operation, the operation size is usually the
> most important variable in the system.** Batching is not a micro-optimisation.

---

## 4. HTTP, and Where the Time Goes

HTTP is a text protocol over TCP: a request line, headers, a blank line, an optional body.

```
GET / HTTP/1.1
Host: example.com

```

**The blank line is the framing** — L26 §1's point that TCP preserves no message boundaries, solved by the simplest possible delimiter.

### The measurement

```
dns=0.006908  connect=0.189839  tls=0.402164  ttfb=0.588753  total=0.588931
```

*(Measured, warm DNS cache, on a 187 ms link.)*

| Phase | Elapsed | Cost | ≈ RTTs |
|---|---:|---:|---:|
| DNS *(cached)* | 7 ms | 7 ms | 0 |
| TCP handshake | 190 ms | **183 ms** | 1 |
| TLS handshake | 402 ms | **212 ms** | 1–2 |
| First byte | 589 ms | **187 ms** | 1 |

**Three round trips and the page is done. The server's own processing is invisible inside the last one.**

**Cold DNS is much worse:**

```
dns=3.510149  ...  total=4.233169
```

*(Measured — and `dig` alone reported **1487 ms cold against 3 ms warm**, a 496× difference.)*

**A cache miss on a name lookup cost more than the entire rest of the page load.**

---

## 5. Every Protocol Improvement Is a Round-Trip Removal

Read the table in §4 as a list of targets, and the last twenty years of protocol design falls out:

| Change | Removes |
|---|---|
| **HTTP keep-alive** | The TCP handshake, on every request after the first |
| **HTTP/2 multiplexing** | Head-of-line blocking and per-resource connections |
| **TLS 1.3** | One round trip from the TLS handshake (2 → 1) |
| **TLS session resumption** | The TLS handshake entirely, on reconnect |
| **QUIC** | Combines transport and crypto setup — **0-RTT** for a known server |
| **DNS caching** | 1487 ms → 3 ms *(measured)* |
| **CDNs** | The 187 ms itself — put the bytes 5 ms away |

**Not one of these makes the server faster.** Every one attacks the same term: **how many times does a message have to cross the ocean before the user sees anything.**

> **And the CDN row is the most important.** Every other entry optimises within a fixed distance.
> **A CDN changes the distance**, which is the only way to beat a number set by the speed of light.

---

## 6. Where This Meets the Rest of the Course

**A network server is a systems program**, and every earlier week shows up in it:

| Week | Appears as |
|---|---|
| 4 — caches | Per-connection state must fit in cache, or 10 000 connections thrash |
| 5 — branches | The parser's hot loop, and why protocol parsing is branch-heavy |
| 6 — virtual memory | Socket buffers are pinned kernel pages; `sendfile` avoids copying them to user space |
| 7 — storage | A web server's real bottleneck is usually the disk behind it, not the socket |
| 7 — Little's Law | **Concurrency = throughput × latency**, and at 187 ms you need many connections in flight |

**Little's Law is the one to carry forward.** To sustain 1000 requests per second on a 187 ms link:

$$\text{concurrency} = 1000 \times 0.187 = \mathbf{187 \text{ requests in flight}}$$

**A server handling one request at a time can manage 5 per second on that link, no matter how fast its CPU is.** This is the entire argument for asynchronous I/O, thread pools and event loops — and it is PROG 201's `epoll` material, arriving here with a number attached.

---

## 7. What to Take Away

1. **A socket is a file descriptor**, and that uniformity is the design.
2. **`accept` returns a new fd**; a server with 10 000 clients has 10 001.
3. **TCP `connect` costs 9× UDP's on loopback**, and a full RTT on a real link.
4. **Message size dominates**: 64 B gives 6.6 MiB/s, 64 KiB gives 2436 MiB/s on the same connection.
5. **HTTP framing is a blank line**, because TCP preserves no boundaries.
6. **A 589 ms page load was three round trips**; cold DNS alone cost 1487 ms.
7. **Every protocol improvement removes round trips.** Only a CDN changes the distance.
8. **Little's Law: 1000 req/s at 187 ms needs 187 in flight.**

---

## Exercises

1. Why does `accept` return a new descriptor rather than reusing the listening one?
2. UDP's `connect` sends no packets. What does it actually do, and why is it still worth calling?
3. From §3, compute per-message overhead in microseconds assuming throughput at 64 KiB is bandwidth-limited. How does it compare with a `write()` to a file from Week 7?
4. HTTP delimits headers with a blank line. Give two other framing strategies and one advantage of each.
5. A page loads 40 resources from one origin over a 187 ms link, one connection, no keep-alive. Estimate the load time. Now with keep-alive. Now with HTTP/2 multiplexing.
6. Apply Little's Law: 5000 requests/second, 250 ms latency. How many concurrent requests? What does that imply about a thread-per-request server?
7. DNS was 1487 ms cold and 3 ms warm. Where is the cache, and what would a cold lookup have to do?

---

*Next week: security — and much of it is this week's protocols and Week 3's stack, attacked.*
