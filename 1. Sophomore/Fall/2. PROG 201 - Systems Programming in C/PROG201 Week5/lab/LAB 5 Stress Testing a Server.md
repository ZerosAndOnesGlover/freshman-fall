# PROG 201 · Lab 5
## Stress Testing a Server — Building the Load Generator
### Covers Week 5 · sat **Friday of Week 6, 16:00–17:50**, BH 215 · **unmarked, checked off in the session**

---

> **This lab is on a Friday, and it is the only one that is.** This course's labs are Mondays, and
> the Monday of Week 6 is **Fall Break** — no classes. Lab 5 is made up on the Friday of Week 6 at
> 16:00, after CS 211's lab vacates the building. Nothing else moves;
> [[PROG 201 Scheduling Notes]] §2 records the decision.
>
> **PS 5 is due at 17:00 the same day**, while you are in this room. **Submit before you come.**
> Nothing in the lab needs your problem-set code, and the two overlapping is a fact about the
> calendar rather than a plan.
>
> **Unmarked.** The TA checks your work off in the session.

**What you are building:** the benchmark, not the server.

The curriculum for this lab says "stress test with Apache Benchmark". **`ab` is not installed on these machines** and cannot be added from a student account, so you are going to write it. That is the better exercise: `ab` is four hundred lines of exactly the non-blocking `connect`, `EAGAIN` handling and `epoll` bookkeeping that L18 spent a lecture on, and a benchmark you wrote is a benchmark whose numbers you can defend.

By the end you will have measured five server architectures under three kinds of load and found the two results that matter: **an event-driven server that is exactly as slow as an iterative one**, and **a thread-per-connection server that fails at 7,637 clients without telling anybody.**

---

## 0. Setup (5 minutes)

```bash
mkdir -p "$PROG201/week5/lab5"        # $PROG201 is set in ~/.bashrc -- see Lab 0
cd "$PROG201/week5/lab5"
cp "$ACADEMICS/1. Sophomore/Fall/2. PROG 201 - Systems Programming in C/PROG201 Week5/lab/"{server.c,load.c,hold.c,bench.sh,Makefile} .

make
./server iter 19000 &
curl -s http://127.0.0.1:19000/ ; kill %1
```

**`server.c` is provided complete** and is not the problem set — it returns a fixed string and parses nothing. PS 5's server parses requests, serves files and reports errors; this one exists so that you have something to measure.

Read its five modes before you start: `iter`, `fork`, `thread`, `pool`, `epoll`. Two arguments matter later — the fifth is microseconds of **blocking** work per request and the sixth is microseconds of **CPU** work:

```
./server <mode> <port> <workers> <backlog> <block_us> <spin_us>
```

**Pick a port above 19000 and keep it.** Ports 8080 and 3000 are already in use on these machines, and `bind` failing with `Address already in use` is L16 §5 arriving before you are ready for it.

---

## 1. Part A — The Load Generator (40 min)

`load.c` is an event-driven client: a few threads, each with its own `epoll` set and a fixed number of connection **slots**. A slot walks through three states and then starts another request, so the number of connections in flight stays at your concurrency figure.

```
state 1  connecting   waiting for EPOLLOUT
state 2  writing      sending the request
state 3  reading      until the server closes
```

**TODO 1 — `start_one`.** Claim a request from the budget, make a `SOCK_NONBLOCK` socket, `connect`, and register for `EPOLLOUT`.

The thing to get right is that **`connect` on a non-blocking socket returns −1 with `errno == EINPROGRESS`, and that is success** (L18 §4). Treating it as an error gives you a load generator that reports every request as failed, which at least fails loudly.

**TODO 2 — the connecting state.** The socket became writable, which means the handshake finished — **it does not mean it succeeded.** Ask `SO_ERROR` (L18 §4). A connection refused by the server arrives here, not from `connect`.

**TODO 3 — writing.** 35 bytes, so one `write` will almost always do it. **Write the loop anyway**, tracking `s->sent` — L16 §6, and "almost always" is what makes this bug hard to find later. When it is all out, `EPOLL_CTL_MOD` to `EPOLLIN`.

**TODO 4 — reading.** `read` > 0 is more of the response. **`read` == 0 is the server closing, which for HTTP/1.0 is how a response ends** — so the request succeeded if you got any bytes. Then `finish` the slot and start another in it, keeping `live` correct.

Check it against the iterative server:

```bash
./bench.sh iter 19000 20 2000
```

You want `ok 2000  err 0`. **If `ok` is 0 and `err` is 0, `start_one` is returning 0** and no request ever left. If `err` is 2000, look at TODO 1's `EINPROGRESS`.

Sanity-check the numbers against something you trust:

```bash
time bash -c 'for i in $(seq 200); do curl -s http://127.0.0.1:19000/ >/dev/null; done'
```

`curl` in a loop is a hundred times slower than your generator and it is the check that your generator is talking to the same server.

---

## 2. Part B — Three Workloads (30 min)

**(a) Trivial work.** The server does nothing but reply:

```bash
for m in iter fork thread pool epoll; do ./bench.sh $m 19001 50 20000; done
```

Ours:

| model | req/s |
| --- | --- |
| iterative | 46,810 |
| fork | 15,038 |
| thread | 39,186 |
| pool | 50,687 |
| epoll | 42,985 |

**The iterative server is second fastest.** Q1.

**(b) Blocking work** — 2 ms per request, a call to a database:

```bash
for m in iter fork thread pool epoll; do ./bench.sh $m 19002 50 3000 8 2000; done
```

| model | req/s |
| --- | --- |
| iterative | 434 |
| fork | 13,740 |
| thread | 18,214 |
| pool (8) | 3,469 |
| **epoll** | **434** |

**Two of those numbers are identical and one of them should not be.** Q2 and Q3.

**(c) CPU work** — 500 µs of computation per request:

```bash
for m in iter fork thread pool epoll; do ./bench.sh $m 19003 50 3000 8 0 500; done
```

| model | req/s |
| --- | --- |
| iterative | 1,912 |
| fork | 8,434 |
| thread | 7,004 |
| **pool (8)** | **12,761** |
| epoll | 1,887 |

**The winner changed.** Q4.

Then size the pool for the blocking workload:

```bash
for w in 1 8 32 64 128; do ./bench.sh pool 19004 50 3000 $w 2000; done
```

| workers | 1 | 8 | 32 | 64 | 128 |
| --- | --- | --- | --- | --- | --- |
| req/s | 437 | 3,487 | 14,085 | 14,471 | 18,667 |

---

## 3. Part C — C10K (25 min)

`hold.c` opens connections and keeps them open, watching the server's RSS. It is provided complete.

```bash
./server epoll 19005 8 4096 & SRV=$!
sleep 0.5
./hold 19005 20000 $SRV
kill -9 $SRV
```

Ours:

```
    2000 connections: server RSS 1 MiB
   20000 connections: server RSS 1 MiB
held 20000 connections
server RSS 1416 -> 1416 kB  = 0.0 kB per connection
```

Now the same against `thread`:

```
pthread_create failed after 7637 connections: Resource temporarily unavailable
held 20000 connections
server RSS 1416 -> 64864 kB = 3.2 kB per connection
```

**Read both lines of that output together.** The server stopped making threads at 7,637 and the client still reports twenty thousand connections held. Q5 and Q6 are about what happened to the other twelve thousand clients, and about where the number 7,637 comes from — you measured it three weeks ago.

---

## 4. Part D — Two Protocol Bugs (15 min)

**(a)** Run `nagle`, which is a copy of L18 §5's experiment:

```
  Nagle on (default)        :   38.963 ms per round trip
  TCP_NODELAY               :    0.209 ms per round trip
```

Over loopback. **There is no network.** Q7.

**(b)** After your Part B runs, count the sockets your benchmark left behind:

```bash
ss -tan state time-wait | wc -l
cat /proc/sys/net/ipv4/ip_local_port_range
```

Ours: **11,261 in `TIME_WAIT` after 20,000 requests**, out of **28,232 ephemeral ports**. Q8.

---

## 5. Questions

Answer in the answer sheet. Three or four sentences each unless stated.

**Q1.** In Part B(a) the iterative server beat three of the four concurrent ones. Explain, and then say what that tells you about "Hello, world" benchmarks in general.

**Q2.** The event-driven server managed 434 req/s on the blocking workload — the same as the iterative one. Explain why, in terms of what `epoll` gives you concurrency *over*.

**Q3.** Your event loop must call `getaddrinfo` to resolve a backend hostname. In two sentences: what does that do to the numbers in Q2, and what are the two standard fixes?

**Q4.** In Part B(c) the pool won and thread-per-connection lost, on the same machine and the same concurrency. Explain both, with reference to the number of cores.

**Q5.** Where does 7,637 come from? Name the limit, say where you would read its value, and say why reducing the thread stack size would not help. *(You measured this in Week 3.)*

**Q6.** The clients "held 20000 connections" against a server that had 7,637 threads. Describe, step by step, what happened to client number 10,000 — from `connect` to whatever it eventually saw. Then say what the server *should* do when `pthread_create` fails.

**Q7.** Give the two algorithms that produce the 39 ms in Part D(a), say which side each one runs on, and give the fix you would prefer and why. *(There are two fixes and one of them addresses the cause.)*

**Q8.** Your benchmark left 11,261 sockets in `TIME_WAIT`. **(a)** Why does the *client* accumulate them here and not the server? **(b)** What happens on the third consecutive run, and with which `errno`? **(c)** Name the fix that is a fix, as opposed to the two sysctls that are not.

---

## 6. Checkoff

Show the TA:

- [ ] `./bench.sh iter <port> 20 2000` reporting `ok 2000 err 0`.
- [ ] Your Part B table, all three workloads, and the two identical numbers pointed at.
- [ ] The `thread` server's `pthread_create failed after ...` line, and Q5 answered out loud.
- [ ] Your written answers to **Q2, Q6 and Q8**.

**If you finish early:** add `-k` to your load generator — keep the connection open and send a second request on it, HTTP/1.1 style. Measure the `TIME_WAIT` count and the request rate again. That one change is worth more than every socket option in L18 §6 put together, and it is why HTTP/1.1 exists.

**Take with you:** Week 6's shell is `fork`/`exec`/`waitpid` with a parser, and Week 9 is where you profile something like this properly rather than by timing the whole thing. **Project 2 is a networked multi-threaded server** — it is PS 5 plus this lab's measurements plus Week 3's pool.

---

*PROG 201 · Week 5 · Lab 5 · © CSE Department*
