# PROG 201 · Systems Programming in C
## Week 12 · Lecture 2 of 3
### Concurrency and Capacity

---

**Reading:** TLPI Ch. 29–30 (threads), Ch. 60 (concurrent servers) · CS:APP §12.3–12.5 · `man 7 pthreads`, `man 2 accept`, `man 3 pthread_cond_wait` · **Previous:** L37 — signals and shutdown · **Next:** L39 — running unattended

---

## 1. The Thread Pool, and Why a Bounded Queue

Week 6's server handled concurrency; this week asks how much, and what happens at the edges. The reference `httpd` uses the standard shape: **one accept loop, a fixed pool of worker threads, and a bounded queue between them.**

```
   accept loop (1 thread)          bounded queue (cap 256)         worker pool (N threads)
   ┌──────────────┐   push   ┌───────────────────────────┐  pop   ┌──────────┐
   │ poll + accept│ ───────▶ │ [fd][fd][fd] ... capacity  │ ─────▶ │ serve(fd)│ × N
   └──────────────┘          └───────────────────────────┘        └──────────┘
                              cond: notempty / notfull
```

Three design choices, each with a reason a naive version gets wrong:

- **A pool, not thread-per-connection.** Spawning a thread per request means an attacker (or a spike) can make you spawn ten thousand threads and exhaust memory — the fork-bomb shape from Week 11, in userspace. A fixed pool caps the concurrency and the memory.
- **A *bounded* queue.** If accept can enqueue without limit, a burst that outruns the workers grows the queue until the process is out of memory — you have moved the fork bomb into the heap. A bounded queue (here 256) means that when it is full, `accept` **blocks** on `pthread_cond_wait(&qnotfull)` — the server stops accepting until a worker frees a slot. That backpressure is a feature: better to leave connections in the kernel's listen backlog (and eventually refuse them) than to accept work you cannot hold.
- **Condition variables, not spinning.** Workers block on `qnotempty`; the acceptor blocks on `qnotfull`. No CPU is burned waiting. `pthread_cond_wait` atomically releases the lock and sleeps, which is the whole reason the pattern is correct — the Week 4 lesson, applied.

---

## 2. Two Scaling Regimes — the Same Server, Opposite Answers

Ask "how many worker threads should the pool have?" and the honest answer is **it depends entirely on what a request does**, and this is measurable. The reference server has two endpoints: `/` returns a fixed string (pure CPU/syscall, microseconds), and `/slow` sleeps 200 ms (models a request that blocks on a database or an upstream). `bench` drives 50 connections; the numbers are stark.

**Regime A — the trivial handler (`GET /`, 10 000 requests):**

| Workers | Throughput |
| --- | --- |
| 1 | 36 152 req/s |
| 2 | 35 943 req/s |
| 4 | 36 377 req/s |
| 8 | 33 752 req/s |
| 16 | 32 455 req/s |

**Adding workers does nothing — and past 8 it *hurts*.** The handler finishes in microseconds, so the bottleneck is not the workers at all; it is the **single accept loop** and the per-connection syscall cost (`accept`, `read`, `write`, `close`) plus loopback connection setup. Throughput is flat at ~36 k because one thread's worth of accept is the ceiling, and adding workers past the core count just adds lock contention on the queue and scheduler churn — hence the decline to 32 k at 16.

**Regime B — the blocking handler (`GET /slow`, 200 ms each):**

| Workers | Throughput | Wall for 40 requests |
| --- | --- | --- |
| 1 | 5 req/s | 8.02 s |
| 2 | 10 req/s | 4.01 s |
| 4 | 20 req/s | 2.01 s |
| 8 | 40 req/s | 1.01 s |

**Perfectly linear — throughput = 5 × workers.** Each request occupies a worker for 200 ms doing nothing but waiting, so N workers serve N requests in parallel: `N / 0.2s = 5N` per second. Here more threads is exactly the right answer, up to the point where you have as many as your peak concurrency.

**One server, two workloads, opposite conclusions.** This is the capstone's version of Week 9's central lesson: **you cannot tune by intuition — you must measure.** "Add threads to go faster" is true for the blocking workload and false-to-harmful for the CPU-bound one. Which regime you are in is a fact you establish with a load test, not a guess you make at the design meeting. (And the trivial-handler ceiling points at the *real* next step for that workload — an event loop with `epoll`, or `SO_REUSEPORT` with multiple accept loops, so the acceptor stops being the bottleneck.)

---

## 3. The p99 Is the Number That Matters

Averages lie about servers. From the trivial-handler run at 4 workers, `bench` reports the distribution, not just the mean:

```
latency mean=2.33ms  p50=1.77ms  p99=11.06ms  max=17.76ms
```

The **mean (2.33 ms)** and **median (1.77 ms)** say the typical request is fast. But the **p99 is 11 ms** — six times the median — and the **max is 17.8 ms**. One request in a hundred is far slower than typical, because it landed when all four workers were busy and waited in the queue, or its thread was descheduled. Users experience the tail: a page that makes 100 requests will, on average, hit that p99 once. **A production SLA is written on the p99 (or p99.9), never the mean**, and a server that reports only its average throughput is hiding exactly the number operators care about. Measuring the tail is why `bench` sorts every latency and reports percentiles rather than just dividing count by time.

---

## 4. Running Unattended Means Not Growing — Measured

A daemon that leaks even a little memory or one file descriptor per request is fine in a demo and dead in a week. Two resources must be **flat over time**, and both are directly observable through `/proc/<pid>/`.

**File descriptors.** Every accepted connection opens an fd; every `serve` must `close` it, on every path including errors. One missed `close` on the error path and the server climbs to its `RLIMIT_NOFILE` and then `accept` fails with `EMFILE` — hours or days in. Measured, watching `/proc/<pid>/fd` across a 10 000-request load:

```
open fds before load:                 6
open fds after 10000 requests:        6
delta:                                0
```

**Zero.** The six are the listening socket, the self-pipe's two ends, and std{in,out,err} — the connection fds are all returned.

**Memory.** A per-request `malloc` without the matching `free`, or an ever-growing cache, shows up as `VmRSS` climbing. Measured across five rounds of 10 000 requests each (50 000 total):

```
round   VmRSS(kB)   open-fds
start      1712        6
1          1728        6
2          1728        6
3          1728        6
4          1728        6
5          1728        6
```

RSS settles at **1728 kB and stays there** — a one-time 16 kB warm-up, then flat. The server's footprint is independent of how many requests it has served, which is the definition of a process that can run for months. **"It doesn't leak" is not a claim you make; it is a line you watch stay flat under sustained load** — the same measure-don't-assert discipline as everywhere else in the course.

---

## Summary

- **Thread pool + bounded queue + condition variables** is the standard concurrent-server shape: a fixed pool caps concurrency (no thread-per-connection fork bomb), a **bounded queue** applies backpressure when accept outruns the workers (no unbounded heap growth), and condvars mean nothing spins.
- **Two scaling regimes, measured on one server:** the trivial `GET /` handler is **flat at ~36 k req/s regardless of worker count** (bottleneck is the single accept loop, not the workers — and 16 workers is *slower* than 4); the blocking `GET /slow` handler scales **linearly, 5 × workers** (5→40 req/s for 1→8). More threads is the right answer only when requests block.
- **Tune by measurement, not intuition** — "add threads" is true in one regime and harmful in the other, and only a load test tells you which you are in. (Week 9's lesson, at the server.)
- **The p99 is the SLA number:** mean 2.33 ms and p50 1.77 ms hide a **p99 of 11 ms** and a max of 17.8 ms; users feel the tail, so report percentiles, not averages.
- **Unattended means flat:** fds measured at **delta 0** across 10 000 requests, RSS **stable at 1728 kB across 50 000** — leak-freedom is a watched line under load, not an assertion.

---

## Exercises

1. Remove the bound on the queue (let it grow) and drive it with a burst far larger than the pool can serve. Watch `VmRSS`. What is the failure mode, and how is it the Week 11 fork bomb in a different place?
2. Reproduce Regime A and Regime B with `httpd` and `bench`/`benchslow`. Plot throughput vs worker count for each. Explain in one sentence each why one is flat and the other linear.
3. At what worker count does Regime A stop improving and start regressing on your machine? Relate it to `nproc`. Why does contention on the single queue lock eventually dominate?
4. `bench` reports mean, p50, p99, max. Construct a latency distribution where the mean is fast but the p99 is unacceptable. Why do user-facing SLAs use p99 or p99.9?
5. Deliberately leak one fd per request (skip a `close` on an error path). How many requests until `accept` fails, given `ulimit -n`? Which errno do you get?
6. The trivial handler is accept-bound. Sketch two fixes — an `epoll` event loop, and `SO_REUSEPORT` with one accept loop per core — and say what each does to the ~36 k ceiling.
7. Why does `pthread_cond_wait` release the mutex atomically as it sleeps, and what race appears if you "check the predicate, unlock, then wait" in three separate steps instead?

---

*PROG 201 · Week 12 · L38 · © CSE Department*
