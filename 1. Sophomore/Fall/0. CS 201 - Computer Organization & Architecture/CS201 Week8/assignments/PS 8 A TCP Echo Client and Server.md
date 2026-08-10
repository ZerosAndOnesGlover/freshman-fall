# CS 201 · Problem Set 8
## A TCP Echo Client and Server

---

**Released:** Week 8, Wednesday · **Due:** Week 9, Friday 17:00
**Total: 100 points** · Submit one PDF plus a `.zip` of source, `PS8_{LastName}_{StudentID}.pdf`

> ⚠️ **Project 1 is due the same day.** Q3 here is deliberately modest — a working echo pair is a
> couple of hundred lines. **Do Project 1 first if you are behind on it.**

---

### Q1: Layers and Addressing (18 points)

**(a) [4]** Name the four TCP/IP layers, the unit at each, and one protocol at each.

**(b) [4]** A 1-byte HTTP payload travels over TCP over IP over Ethernet. Give the header bytes added at each layer and the total. Compute the efficiency, and the payload size at which overhead falls below 10%.

**(c) [4]** MAC addresses are flat; IP addresses are hierarchical. **Explain why global routing needs the second**, in terms of what a router would otherwise have to store.

**(d) [3]** For `192.168.137.115/24`: network address, broadcast address, usable host count, and the subnet mask in dotted-quad form.

**(e) [3]** IPv6 has existed since 1998 and adoption took decades. **Name the property of the change that made it slow**, and contrast with a change that would have been fast.

---

### Q2: TCP Mechanics (22 points)

**(a) [4]** Draw the three-way handshake with sequence and acknowledgement numbers. State how many round trips pass before the first byte of application data can be sent.

**(b) [4]** Why are initial sequence numbers randomised? Name the attack, and say what an attacker could do with predictable ones.

**(c) [4]** Closing takes four messages where opening takes three. Explain, then explain **`TIME-WAIT`**: its purpose, its duration, and what goes wrong without it.

**(d) [4]** Two `send` calls of 100 bytes each. **Give three legitimate ways the peer's `recv` calls could observe them**, and state the general property of TCP responsible.

Then name two framing strategies a protocol can use, with one advantage each.

**(e) [6]** Distinguish **flow control** from **congestion control** — what each protects, and the mechanism each uses.

Then: a link has 187 ms RTT and an initial congestion window of 14 KB. Under slow start, how many round trips to reach a 1 MB window, and how long in seconds? **State the consequence for short HTTP responses.**

---

### Q3: Build the Echo Pair (30 points)

Write a TCP echo **server** and **client** in C.

```
./echo_server <port>
./echo_client <host> <port> [--size N] [--count M] [--nodelay]
```

**(a) [12]** **The implementation.**

- The server must handle **at least two sequential clients** without restarting.
- **Framing is required**: send a 4-byte big-endian length prefix, then the payload. **You may not assume one `send` arrives as one `recv`.**
- Both sides must handle **short reads and short writes** — loop until the full message is transferred.
- Clean shutdown on `close`, with no leaked descriptors.

**(b) [6]** **Prove your framing works.** Demonstrate a case where a single logical message is split across multiple `recv` calls, or two messages arrive in one. Show the evidence — a log of the loop's iterations is fine.

> **The easiest way to force this is a large message**, e.g. 1 MiB, where the kernel will
> essentially never deliver it in one `recv`.

**(c) [6]** **Measure it.** Report round-trip time and throughput for message sizes 64 B, 4 KiB and 64 KiB on loopback.

Reference *(verified)*: **18.6 μs / 6.6 MiB/s**, **21.2 μs / 369.3 MiB/s**, **51.3 μs / 2436.1 MiB/s**.

**Explain the shape of the curve**, and say what fixed cost is being amortised.

**(d) [6]** **Add a UDP mode** and compare at 64 B.

Reference *(verified)*: UDP **17.5 μs** against TCP **18.6 μs**; UDP `connect` **11.6 μs** against TCP **107.1 μs**.

**Explain both comparisons** — why the round trips are so close, and why the setup costs are not.

---

### Q4: Make Nagle Deadlock (18 points)

**(a) [4]** Run your echo benchmark with and without `TCP_NODELAY` in the ordinary **send-then-receive** pattern.

Reference *(verified)*: **18.6 μs against 19.1 μs.** **Explain why Nagle has no effect here.**

**(b) [8]** Now change the client to **two small writes then a read** — a 4-byte header and a 16-byte body — with the server reading all 20 bytes before replying. Measure both ways.

Reference *(verified)*: **30.4 μs against 41 068 μs — a factor of 1350.**

**Report your numbers**, and **identify the kernel timer** that 41 ms corresponds to.

> Use ~60 iterations with Nagle on, and unbuffered stdout. At 41 ms each this is slow, and the
> first attempt at this measurement **timed out having printed nothing.**

**(c) [4]** **Trace the deadlock in four steps**, saying at each what each side is waiting for.

**(d) [2]** You measured a 3% difference and a 1350× difference from the same flag, minutes apart. **State the lesson for benchmarking.**

---

### Q5: Where the Time Goes (12 points)

**(a) [4]** Measure your own latency ladder: loopback, LAN gateway, and a public address.

Reference *(verified)*: **0.084 ms**, **2.388 ms**, **186.950 ms**.

Place all three on the course cost ladder and identify **which network hop is faster than an SSD read**.

**(b) [4]** Break down an HTTPS page load with `curl -w`.

Reference *(verified, warm)*: `dns=0.007 connect=0.190 tls=0.402 ttfb=0.589 total=0.589`.

Compute the cost of each phase, express each in round trips against your (a) figure, and state **how much of the total was the server's own work**.

**(c) [4]** DNS was **1487 ms cold and 3 ms warm** *(verified)*.

Explain what a cold lookup must do. Then name **three** protocol or infrastructure changes that remove round trips from (b), and say which one attacks the RTT itself rather than the count.

---

## Marks

| | |
|---|---:|
| Q1 Layers and Addressing | 18 |
| Q2 TCP Mechanics | 22 |
| Q3 Build the Echo Pair | 30 |
| Q4 Make Nagle Deadlock | 18 |
| Q5 Where the Time Goes | 12 |
| **Total** | **100** |

---

*CS 201 · Week 8 · Problem Set 8*
