# CS 201 · Problem Set 8 — Solutions
## Instructor Only

---

> **Not for distribution.** All figures measured on the lab image. **The network path is a tethered
> Wi-Fi link** (`192.168.137.0/24` is the Windows ICS default range), which is why the internet RTT is
> 187 ms rather than the ~20 ms a wired campus connection would give. **Students on other networks
> will see very different absolute numbers and the same ratios.**

---

## Q1 (18) — Layers and Addressing

### (a) [4]

| Layer | Unit | Protocol |
|---|---|---|
| Application | message | HTTP, DNS, SSH |
| Transport | segment | TCP, UDP |
| Network | packet | IP |
| Link | frame | Ethernet, Wi-Fi |

*(Accept a five-layer split with Physical/bit.)*

### (b) [4]

Ethernet 14 + IP 20 + TCP 20 = **54 bytes**.

$$\text{efficiency} = \frac{1}{55} = \mathbf{1.8\%}$$

For overhead below 10%: $\dfrac{54}{p+54} < 0.1 \Rightarrow p > \mathbf{486}$ bytes.

### (c) [4]

**MAC addresses are flat** — 48 bits assigned at manufacture, with no structure to aggregate on. A router would need **one table entry per device on Earth**.

**IP is hierarchical**: a prefix identifies a whole network, so one entry covers millions of hosts. **Route aggregation is what keeps the global table at hundreds of thousands of entries rather than billions**, and CIDR notation is exactly the prefix length.

### (d) [3]

| | |
|---|---|
| Network | `192.168.137.0` |
| Broadcast | `192.168.137.255` |
| Usable hosts | $2^8 - 2 = \mathbf{254}$ |
| Mask | `255.255.255.0` |

### (e) [3]

**IPv6 changed the *interface* of a layer, not its implementation.** Every layer above — sockets, DNS, firewalls, application code that assumed a 32-bit address, printed-address formats, database columns — had to change, and there is no way to do that incrementally when the two address spaces cannot talk to each other directly.

**Contrast:** a change *within* a layer, such as a new TCP congestion-control algorithm (BBR), deploys unilaterally — one endpoint upgrades and everything above is unaffected. **The lesson is Week 0's: an abstraction can be reimplemented freely and respecified only with enormous cost.**

---

## Q2 (22) — TCP Mechanics

### (a) [4]

```
client                          server
   ├───── SYN, seq=x ─────────────▶
   ◀──── SYN-ACK, seq=y, ack=x+1 ──┤
   ├───── ACK, ack=y+1 ───────────▶
```

**One full round trip** before data can be sent. *(The third message may carry data, so it is 1 RTT, not 1.5.)*

### (b) [4]

**Randomised so an off-path attacker cannot guess them.** With predictable ISNs, an attacker who can forge a source address can inject data into — or reset — someone else's connection without ever seeing it. **This is TCP sequence-number prediction**, demonstrated against real systems in the 1990s.

### (c) [4]

**[2]** Each direction is closed independently, so each needs a FIN and an ACK — four messages. A host may still send after receiving a FIN (half-close).

**[2] `TIME-WAIT`** holds the four-tuple for **2×MSL** (typically 60 s on Linux) so that a delayed duplicate from the old connection cannot arrive during a new connection reusing the same four-tuple and be accepted as valid data. **Without it, stale segments could corrupt a new connection's stream.**

### (d) [4]

**[2]** Three of: as two 100-byte reads; as one 200-byte read; as 37 + 163; as 1 byte then 199. **TCP is a byte stream and preserves no message boundaries** — only order and completeness.

**[2] Framing strategies**, any two:

| Strategy | Advantage |
|---|---|
| Length prefix | Constant-time; the receiver knows exactly how much to await |
| Delimiter (e.g. HTTP's blank line) | Human-readable, no length known in advance — good for streaming |
| Fixed-size records | Trivial to parse, no framing bytes at all |

### (e) [6]

**[3] Flow control** protects the **receiver** from being overrun, using the **advertised window** in each ACK. **Congestion control** protects the **network** from being overrun, using the **congestion window**, adjusted by AIMD in response to loss. **Two separate windows; the sender is limited by the smaller.**

**[3] Slow start.** 14 KB doubling per RTT: 14 → 28 → 56 → 112 → 224 → 448 → 896 → 1792 KB, so **7 round trips** to exceed 1 MB, and $7 \times 187\text{ ms} = \mathbf{1.31 \text{ s}}$.

**Consequence:** a short HTTP response finishes long before the window opens — **the transfer spends its entire life in slow start** and never reaches the link's capacity. This is a major argument for connection reuse, and for HTTP/2 multiplexing over a single warmed connection.

---

## Q3 (30) — Build the Echo Pair

### (a) [12]

| | |
|---|---:|
| Works, two sequential clients | 3 |
| **Length-prefixed framing, correct byte order** | 4 |
| **Short-read/short-write loops on both sides** | 4 |
| Clean shutdown, no leaked fds | 1 |

> **The short-read loop is where most submissions fail**, and it usually passes small-message testing
> anyway. **Check the code, not just the output** — a single `recv(fd, buf, n, 0)` without a loop is
> wrong even if it works at 64 bytes. `MSG_WAITALL` is an acceptable alternative **only if the
> student says why it is not a general solution** (it can still return short on signal or error).

### (b) [6]

**4** for a demonstration that a logical message spanned multiple `recv` calls; **2** for evidence rather than assertion.

**The reliable trigger is a 1 MiB message**, where the kernel's socket buffer forces fragmentation. A student who reports "I tried and it never split" at 64 bytes has not tried hard enough — send them back with a bigger message.

### (c) [6]

| message | round trip | throughput |
|---:|---:|---:|
| 64 B | 18.6 μs | 6.6 MiB/s |
| 4 KiB | 21.2 μs | 369.3 MiB/s |
| 64 KiB | 51.3 μs | 2436.1 MiB/s |

*(Verified.)*

**The fixed cost** being amortised: two system calls, TCP state-machine processing, socket buffer management, checksum, and **the scheduler waking the peer process**. At 64 bytes these dominate; at 64 KiB the benchmark is measuring memory bandwidth.

> **Full marks require naming at least three components.** "Overhead" alone is 3 of 6.

### (d) [6]

*(Verified: UDP round trip **17.5 μs** against TCP **18.6 μs**; UDP `connect` **11.6 μs** against TCP **107.1 μs**.)*

**[3] Round trips are close** because on loopback there is no loss, no reordering and no congestion, so **all of TCP's machinery has nothing to do.** The measured time is dominated by system calls and scheduler wakeups, which both protocols pay equally.

**[3] Setup costs are not**, because **TCP's `connect` performs the three-way handshake** — even on loopback that is a full state-machine exchange through the kernel — whereas **UDP's `connect` sends nothing at all**; it merely records the peer address locally so later `send` calls need no destination argument.

---

## Q4 (18) — Make Nagle Deadlock

### (a) [4]

**18.6 μs against 19.1 μs** *(verified)* — no meaningful difference.

**Nagle has nothing to hold back.** Each `send` is immediately followed by a `recv`, so there is never a *second* small write outstanding while the first is unacknowledged. **Nagle only delays a small write when there is already unacknowledged data**, and this pattern never creates that condition.

### (b) [8]

**[4]** **30.4 μs against 41 068 μs — 1350×.** *(Verified.)*

**[4]** **41 ms is Linux's delayed-ACK timer** (~40 ms). The receiver holds its ACK hoping to piggyback it on outbound data; here no outbound data is coming, because the server is still waiting for the rest of the message.

> **Award the [4] only for identifying the timer.** "It's slow because of Nagle" is half the answer —
> Nagle alone would resolve as soon as an ACK arrived. **The 40 ms comes from the other side.**

### (c) [4]

1. **Write 1 (4 B) goes out immediately** — nothing is unacknowledged.
2. **Write 2 (16 B) is held by Nagle** — it is small and write 1 is unacknowledged.
3. **The server has 4 of 20 bytes and does not reply**, so it produces no data to piggyback an ACK on. **Its delayed-ACK timer starts.**
4. **~40 ms later the ACK fires**; Nagle releases write 2; the server's `recv` completes and it replies.

**Each side is waiting for the other**, and only a timer breaks it.

### (d) [2]

**A flag's cost is a property of the workload, not of the flag.** The same option was worth 3% and 1350× on the same machine minutes apart. **Benchmark the access pattern you actually have**, and be suspicious of any performance advice stated without one.

---

## Q5 (12) — Where the Time Goes

### (a) [4]

| target | RTT |
|---|---:|
| loopback | **0.084 ms** |
| LAN gateway | **2.388 ms** |
| `1.1.1.1` | **186.950 ms** |

*(Verified.)*

**The loopback round trip (84 μs) is faster than an SSD 4 KiB read (157 μs)** — the answer expected. Accept the observation that a loopback "network" operation beats local storage.

### (b) [4]

| Phase | Cost | RTTs |
|---|---:|---:|
| DNS (cached) | 7 ms | 0 |
| TCP handshake | **183 ms** | 1 |
| TLS handshake | **212 ms** | 1–2 |
| Server response | **187 ms** | 1 |
| **Total** | **589 ms** | ~3 |

**The server's own work is invisible** — it is somewhere inside the final 187 ms and is small enough not to register. **Essentially 100% of the page load was round trips.**

### (c) [4]

**[1] A cold lookup** must walk the hierarchy: root servers → TLD (`.com`) → the domain's authoritative servers, each a separate round trip, unless a resolver higher up has a cached answer. *(Measured: 1487 ms cold against 3 ms warm — 496×.)*

**[3] Three changes**, any three, with the distinction required:

- **HTTP keep-alive / connection reuse** — removes the TCP handshake on subsequent requests.
- **TLS 1.3 or session resumption** — removes one or both TLS round trips.
- **HTTP/2 or QUIC** — removes per-resource connection setup; QUIC reaches 0-RTT for a known server.
- **DNS caching** — removes the lookup.

**The one that attacks the RTT itself is a CDN.** Every other change reduces the *number* of round trips at a fixed distance; **a CDN changes the distance**, which is the only way to beat a figure set by the speed of light.

---

## Mark Summary

| | |
|---|---:|
| Q1 | 18 |
| Q2 | 22 |
| Q3 | 30 |
| Q4 | 18 |
| Q5 | 12 |
| **Total** | **100** |

**Where the class loses marks, in order:**

1. **Q3(a)** — no short-read loop, hidden by small-message testing.
2. **Q4(b)** — blaming Nagle alone and not identifying the delayed-ACK timer.
3. **Q2(d)** — treating "TCP is a stream" as a slogan without giving concrete split cases.
4. **Q5(c)** — listing optimisations without separating "fewer round trips" from "shorter round trip".
5. **Q2(e)** — conflating flow control with congestion control.

---

*CS 201 · Week 8 · PS 8 Solutions · Instructor Only*
