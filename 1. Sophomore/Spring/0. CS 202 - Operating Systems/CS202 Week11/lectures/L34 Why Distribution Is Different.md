# CS 202 · Operating Systems
## Week 11 · Lecture 1 of 3
### Why Distribution Is Different

*“A distributed system is one in which the failure of a computer you didn't even know existed can render your own computer unusable.”* — Leslie Lamport, email (28 May 1987)

---

**Sat:** Monday of Week 11, 09:00–09:50, VNC 101, **after Quiz 11** · **Reading:** OSTEP Ch. 48; Lamport (1978) · **Next:** L35, agreement

**Coursework:** 📊 **Quiz 11** today · 🔬 **Lab 10** Tue this week 15:00–16:50 · 📝 **PS 11** released Wed this week, due Fri of Week 12 17:00 · 📋 **Project 1** due Fri this week 17:00 · 📝 **PS 10** due Fri this week 17:00

> **Project 1 is due this Friday at 17:00.**

---

## 1. Everything So Far Had One Machine

**Every mechanism in this course has rested on three assumptions**, and all three fail the moment there is a second machine:

| Until now | Across machines |
|---|---|
| **Shared memory**: a lock, a queue, a page table everyone can see | **nothing is shared.** Every fact must be sent, and sending takes time |
| **Failures are total**: the machine is up, or you are not running | **partial failure**: the other machine may be gone, slow, or fine but unreachable — **and you cannot tell which** |
| **One clock**: `rdtsc` orders every event on the machine | **no global clock.** Two machines' clocks disagree, and the disagreement changes |

**This lecture is those three, measured.** The next two are what can be built on top.

---

## 2. What Distance Costs

`netlat.c` measures the same thing — send a byte, get one back — at each level available on one machine, and `ping` supplies the last row:

| Round trip | Cost | Against a function call |
|---|---:|---:|
| a function call | **0.0018 µs** | 1 |
| a system call (`getppid`) | **0.84 µs** | ~470 |
| a pipe, between two processes | **8.5 – 10.5 µs** | ~5,000 |
| **loopback UDP** | **19.1 – 20.3 µs** | ~11,000 |
| **loopback TCP** | **21.4 – 22.5 µs** | ~12,000 |
| **another machine on the internet** (`ping 8.8.8.8`) | **22.6 – 24.5 ms** | **~13,000,000** |

**Loopback never touches a wire** and still costs twenty microseconds — two context switches, two protocol stacks, two copies. **The real network costs a thousand times that**, and nothing in software makes it smaller: it is distance divided by the speed of light in fibre, plus queues.

**So a distributed algorithm is judged by *round trips*, not instructions.** Raft (L35) is designed around "one round trip to a majority", because that is the unit that matters.

---

## 3. "Sent" Is Not "Delivered"

**A successful `write()` to a socket tells you almost nothing.** `delivered.c` connects two processes, stops the reader with `SIGSTOP`, and writes until the kernel refuses:

```
write() reported success for 2643968 bytes the peer never read
and then refused, with the connection still open
```

**Two and a half megabytes "sent" to a process that had stopped reading.** They are in the sender's socket buffer and the receiver's — in RAM on both machines, lost entirely if either crashes.

**This is the general shape of the problem.** Between "I have decided" and "you know it", a message can be:

- **delayed** — arbitrarily, and you cannot distinguish delay from loss;
- **lost** — and TCP's retransmission only pushes the uncertainty into the connection's failure;
- **duplicated** — a retransmission whose acknowledgement was the thing that was lost;
- **delivered, with the acknowledgement lost** — so the sender believes it failed.

**The last is the one that matters most**: *the sender can never know whether a message it did not hear back about was delivered.* **The only defence is to make actions idempotent** — Week 8's replay of a log, one level up — and to identify them, so that a repeat is recognisable.

---

## 4. There Is No Global Clock

**A program can read several clocks, and they measure different things:**

```
CLOCK_REALTIME         resolution 1 ns, now 1789567737.250600213
CLOCK_MONOTONIC        resolution 1 ns, now 33995.747081454
CLOCK_BOOTTIME         resolution 1 ns, now 63640.053830320
```

**`CLOCK_BOOTTIME` is 29,645 seconds ahead of `CLOCK_MONOTONIC` on this machine** — eight hours. That is **how long it spent suspended**: `MONOTONIC` stops while the machine sleeps, `BOOTTIME` does not. **Neither is "the time"**, and `REALTIME` — the one that is — can jump backwards when NTP corrects it.

```
System clock synchronized: yes
NTP service: active
```

**NTP keeps this machine within a few milliseconds of true time**, on a good day, over a network whose round trip is 23 ms. **You cannot do better than half the round-trip uncertainty**, which is why timestamps from two machines cannot be compared to order events a few milliseconds apart.

**So distributed systems order events by *causality*, not by clocks.** Lamport's 1978 answer — a counter per node, carried on every message and raised to the maximum seen — gives "happened before" without any clock at all. **Raft's *term* is exactly such a counter** (L35 §2).

---

## 5. What You Cannot Do

**Two Generals.** Two armies must attack together; messengers can be captured. **No finite exchange of messages makes both sure**: whichever message arrives last, its sender does not know it arrived. **There is no protocol that guarantees agreement over a lossy channel** — only protocols that make disagreement arbitrarily unlikely.

**FLP (1985).** In an asynchronous system — no bound on message delay — **no deterministic protocol can guarantee consensus if even one node may crash**. The proof rests exactly on §1's second row: a silent node is indistinguishable from a slow one.

**What real systems do is choose their impossibility:**

- **Assume a bound on delay** — and use **timeouts** as failure detectors, accepting that a slow node will sometimes be declared dead (L36 §1).
- **Give up determinism** — randomise, so that livelock has probability zero over time. **Raft's randomised election timeouts are exactly this** (L35 §3).

**Every practical consensus protocol does both.**

---

## 6. What to Take Away

1. **Three assumptions fail at once**: no shared memory, partial failure, no global clock.
2. **Measured, distance costs**: 0.84 µs for a system call, 20 µs across loopback, **23 ms to another machine** — a factor of a thousand, and it is physics, not software.
3. **A successful `write` is not delivery**: 2.6 MB "sent" to a stopped reader, still in buffers.
4. **The sender cannot learn whether an unacknowledged message arrived** — so operations must be **idempotent and identifiable**.
5. **Clocks disagree and jump**; `BOOTTIME` and `MONOTONIC` differ by eight hours of suspend on this machine. **Order events by causality** — Lamport's counters, and Raft's terms.
6. **Two Generals and FLP say what is impossible**; real systems buy their way out with **timeouts and randomisation**.

---

## Exercises

1. A service takes 0.5 ms of CPU per request and one round trip to a replica. **Compute its maximum throughput per connection** on loopback and across the internet, using §2's numbers.
2. A client sends "transfer £100", the server does it, and the reply is lost. The client retries. **Describe two designs that prevent a double transfer**, and say what each costs.
3. `CLOCK_MONOTONIC` cannot go backwards but stops during suspend; `CLOCK_BOOTTIME` does not stop; `CLOCK_REALTIME` can jump. **Which would you use for: a 30-second timeout; a certificate's expiry; measuring how long a request took?**
4. **Why does TCP not solve the delivery problem?** Name what it does guarantee, and what it cannot.
5. In Two Generals, suppose messages are lost with probability 0.1 and you may send 10 messages. **What is the chance both sides agree**, and why does no number of messages make it 1?

---

*CS 202 · Week 11 · L34 · © CSE Department*
