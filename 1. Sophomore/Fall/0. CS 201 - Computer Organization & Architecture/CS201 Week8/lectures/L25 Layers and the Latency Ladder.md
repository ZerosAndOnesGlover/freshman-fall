# CS 201 · Computer Organization & Architecture
## Week 8 · Lecture 1 of 3
### Layers, and the Latency Ladder Completed

*“Never underestimate the bandwidth of a station wagon full of tapes hurtling down the highway.”* — Andrew S. Tanenbaum, *Computer Networks*, 3rd ed. (1996), paraphrasing Warren Jackson

---

**Reading:** CS:APP §11.1–11.3 · **Previous:** L24, storage performance

**Coursework:** 📊 **Quiz 8** today · 🔬 **Lab 7** Tue this week 15:00–16:50 · 📝 **PS 8** released Wed this week, due Fri of Week 9 17:00 · 📝 **PS 7** due Fri this week 17:00

---

## 1. The Ladder, Finished

Seven weeks of measurement, on one machine, in one table:

| Event | Time | Measured in |
|---|---:|---|
| L1 cache hit | 1.2 ns | Week 4 |
| DRAM access | 137 ns | Week 4 |
| Minor page fault | 1.9 μs | Week 6 |
| Page-cache hit | 2.5 μs | Week 7 |
| **TCP loopback round trip** | **18.6 μs** | **this week** |
| SSD 4 KiB read | ~157 μs | Week 7 |
| **LAN round trip** | **2.4 ms** | **this week** |
| `fsync` | 3.9 ms | Week 7 |
| **Internet round trip** | **187 ms** | **this week** |
| **One HTTPS page load** | **589 ms** | **this week** |

*(All measured on the lab machine.)*

**From 1.2 nanoseconds to 589 milliseconds is a factor of about 500 million.**

**Read the ladder for where the network sits.** A loopback round trip is *faster* than reading from the SSD. A LAN round trip is comparable to an `fsync`. **And an internet round trip is 187 ms — roughly 600 million cycles**, during which the processor could have executed more instructions than there are in most programs.

> **This is the week's frame.** Networking is not primarily about protocols. It is about the fact
> that **the speed of light is 300 000 km/s and does not negotiate.** London to New York and back is
> 11 000 km, which is 37 ms in fibre at best. **Every design decision above follows from being unable
> to fix that.**

---

## 2. Why Layers

The problem: many kinds of physical medium, many kinds of application, and you cannot write $m \times n$ pieces of software.

**The solution is the same one Week 0 gave for the whole machine — a stack of abstractions, each using the one below and hiding it from the one above.**

| TCP/IP layer | Job | Unit | Example |
|---|---|---|---|
| **Application** | What the bytes *mean* | message | HTTP, DNS, SSH |
| **Transport** | Process-to-process delivery | segment | **TCP**, UDP |
| **Network** | Host-to-host across networks | packet | **IP** |
| **Link** | Node-to-node on one medium | frame | Ethernet, Wi-Fi |
| **Physical** | Bits onto a wire | bit | copper, fibre, radio |

**The OSI model has seven layers** and is the one you will be asked about in interviews. Its session and presentation layers never corresponded to anything real in the TCP/IP stack, which is why practice uses four or five.

**The key property is encapsulation.** Each layer wraps the layer above in its own header:

```
[ Ethernet header [ IP header [ TCP header [ HTTP request ] ] ] ]
        14 B          20 B        20 B         your data
```

**54 bytes of headers before your data starts.** For a 1-byte payload that is 98% overhead — which is exactly why L26's Nagle algorithm exists, and why measuring throughput in "messages per second" without stating the message size is meaningless.

---

## 3. Addressing at Each Layer

Three different names for the same machine, at three layers, and each exists because the layer below cannot do the job.

| Layer | Address | Scope | Example |
|---|---|---|---|
| Link | **MAC** | one physical segment | `1c:ae:bf:fd:86:83` |
| Network | **IP** | globally routable | `192.168.137.115` |
| Transport | **port** | one process on one host | `54321` |

**MAC addresses are flat** — 48 bits, assigned at manufacture, with no structure to route on. Fine for a single Ethernet segment where you can broadcast; hopeless globally, because a router would need a table with every device on Earth.

**IP addresses are hierarchical**, which is the whole point. `192.168.137.0/24` means "the first 24 bits identify the network" — so a router stores one entry for a whole block rather than one per host. **CIDR notation is that prefix length**, and route aggregation is what keeps the global routing table at hundreds of thousands of entries instead of billions.

**Ports identify the process.** The kernel demultiplexes an arriving segment to a socket using the **four-tuple** — source IP, source port, destination IP, destination port. Two browser tabs to the same server differ only in source port.

**IPv6** exists because 32 bits is 4.3 billion addresses and the world has more devices than that. 128 bits is $3.4\times10^{38}$. **Adoption took thirty years** because every layer above had to be touched, which is what happens when an abstraction's *interface* changes rather than its implementation.

---

## 4. The Layers Have Costs, and They Are Measurable

The latency ladder in §1 is a tour of the layers:

**Loopback — 18.6 μs.** No wire at all; the packet never leaves the kernel. **This is the cost of the software stack alone** — two system calls, the TCP state machine, checksums, socket buffers, and the scheduler waking the peer. **A round trip that touches no hardware still costs 60 000 cycles.**

**LAN — 2.4 ms** to the local gateway over Wi-Fi. Add a physical medium with contention, and it is 130× loopback.

**Internet — 187 ms** to a public resolver. Add propagation delay and a dozen routers.

> **Notice what does *not* appear in that progression: bandwidth.** Every figure above is
> **latency**, and latency is the thing you cannot buy your way out of. You can lay more fibre; you
> cannot make it shorter. **Bandwidth has improved by orders of magnitude in twenty years and
> transatlantic latency has not improved at all.**

---

## 5. What Actually Happens When You Load a Page

`curl https://example.com`, with the DNS cache warm:

```
dns=0.006908s  connect=0.189839s  tls=0.402164s  ttfb=0.588753s  total=0.588931s
```

*(Measured.)* Decomposed:

| Phase | Time | Round trips |
|---|---:|---|
| DNS lookup *(cached)* | 7 ms | 0 — local |
| **TCP handshake** | **183 ms** | **1 RTT** |
| **TLS handshake** | **212 ms** | **1–2 RTT** |
| **Server response** | **187 ms** | **1 RTT** |
| **Total** | **589 ms** | |

**The link's round-trip time is 187 ms. The page took 589 ms. Essentially all of it is round trips.**

**The server's own work is invisible** — somewhere inside that last 187 ms is the time it took to generate the response, and it is small enough not to matter.

**And DNS cold is worse.** The same measurement with an empty cache:

```
dns=3.510149s  ...  total=4.233169s
```

*(Measured — and `dig` reported 1487 ms cold against 3 ms warm, a 496× difference.)*

> **This is why every network optimisation is about eliminating round trips**, not about making the
> server faster. Connection reuse, HTTP/2 multiplexing, TLS 1.3's one-RTT handshake, QUIC's zero-RTT
> resumption, DNS caching, CDNs putting the content 5 ms away instead of 187 — **all of them are
> attacks on the same term in the same sum.**

---

## 6. What to Take Away

1. **1.2 ns to 589 ms** — the full ladder, on one machine.
2. **A loopback round trip is 18.6 μs**, faster than the SSD; an internet round trip is 187 ms.
3. **Layers exist so you do not write $m \times n$ implementations**, and encapsulation costs 54 bytes of header.
4. **MAC is flat, IP is hierarchical, ports identify processes.** Hierarchy is what makes routing possible.
5. **Latency is the thing you cannot buy.** Bandwidth improved by orders of magnitude; transatlantic RTT did not.
6. **A 589 ms page load contained ~582 ms of round trips.** Optimisation means removing round trips.

---

## Exercises

1. From §1, how many L1 hits fit in one internet round trip? How many DRAM accesses?
2. London to New York is ~5500 km. Compute the theoretical minimum RTT in fibre (light travels at ~2/3 $c$ in glass). Compare with the 187 ms measured here and explain the gap.
3. A 1-byte payload carries 54 bytes of headers. Compute the efficiency. At what payload size does overhead fall below 10%?
4. Why can MAC addresses not be used for global routing? What property does IP have that they lack?
5. `192.168.137.115/24` — give the network address, the broadcast address and the number of usable hosts.
6. From §5, identify which phases could be eliminated by (a) connection reuse, (b) a CDN, (c) TLS 1.3. Estimate the saving for each.

---

*Next: L26 — how TCP turns an unreliable network into a reliable stream, and what that costs.*
