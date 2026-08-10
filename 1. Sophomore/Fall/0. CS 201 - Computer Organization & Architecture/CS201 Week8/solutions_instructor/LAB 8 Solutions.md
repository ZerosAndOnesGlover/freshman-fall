# CS 201 · Lab 8 — Solutions and TA Notes
## Instructor Only

---

> **Unmarked.** Five checkpoints plus an optional sixth. All figures measured on the lab image.

---

## Before the Session

**Wireshark is not installed and `tcpdump` cannot capture without root:**

```
tcpdump: lo: You don't have permission to perform this capture on that device
```

*(Verified.)* **Say this at the start**, along with the substitution: `strace` for the syscall boundary, `ss` for the state machine, and the students' own timing code.

**Make the case rather than apologising for it.** For CS 201 the syscall view is closer to the course's subject than a packet trace is — this is a machine-organisation course, and `strace` shows exactly the user/kernel boundary that Weeks 6 and 7 were about. **If any student has a personal machine with root, encourage them to run `tcpdump -i lo -n port 54321` alongside Part 3 and bring the output to the next session.**

**Also flag the network:** the lab link is tethered Wi-Fi (`192.168.137.0/24` is the Windows ICS range), so the internet RTT is **187 ms** where a wired campus link would give ~20 ms. **The ratios are what matter, not the absolute figures.**

---

## Timing

| Part | Budget | Reality |
|---|---|---|
| 1 — latency ladder | 20 min | 15 min |
| 2 — state machine | 20 min | 15 min |
| 3 — `strace` | 25 min | 25 min |
| 4 — message size | 20 min | 20 min |
| 5 — **Nagle deadlock** | 25 min | **Protect this** |

---

## Part 1

| target | RTT |
|---|---:|
| `127.0.0.1` | 0.084 ms |
| gateway | 2.388 ms |
| `1.1.1.1` | 186.950 ms |

*(Verified.)*

**Answers:**

1. **The loopback round trip (84 μs) is faster than an SSD 4 KiB read (157 μs).** Students find this genuinely surprising and it is the point of the exercise.
2. $0.187 / 1.2\times10^{-9} \approx \mathbf{1.6 \times 10^8}$ L1 hits. *(And $1.4\times10^6$ DRAM accesses.)*
3. At 200 000 km/s, 187 ms is **18 700 km one way** — roughly halfway round the Earth, which is not where `1.1.1.1` is. **The gap is queueing, the wireless hop, and the tethered uplink**, not distance. Good answers notice that propagation is only part of latency.
4. **`lo` has MTU 65536; the Wi-Fi interface has 1500.** Loopback never touches a wire, so there is no framing constraint and a larger MTU means fewer trips through the stack. **1500 is Ethernet's historical frame limit.**

**✅ CHECKPOINT 1**

---

## Part 2

```
     18 ESTAB
      7 TIME-WAIT
      4 LISTEN
      1 LAST-ACK
      1 FIN-WAIT-1
```

*(Verified — an idle desktop.)*

**Answers:**

1. `ESTAB` → send FIN → `FIN-WAIT-1` → ... → `TIME-WAIT` on the active closer; the passive closer goes `CLOSE-WAIT` → `LAST-ACK` → `CLOSED`.
2. **`TIME-WAIT` holds the four-tuple for 2×MSL (~60 s on Linux)** so a delayed duplicate from the old connection cannot be accepted by a new connection reusing the same four-tuple. **Without it, stale segments corrupt new streams.** On a busy server these accumulate into tens of thousands, which is what `SO_REUSEADDR` and tuning exist for.
3. **Flow control** — `Recv-Q` is data the application has not read; `Send-Q` is data sent but unacknowledged.
4. A burst of new `ESTAB` then `TIME-WAIT` entries to port 443, one per connection `curl` opened.

**✅ CHECKPOINT 2**

---

## Part 3

**Answers:**

1. **`connect` performs the three-way handshake**; `send` merely copies into a socket buffer and returns. *(Measured: 107.1 μs against ~12 μs.)* On a real link `connect` is a full RTT and `send` is still microseconds.
2. **The listening socket keeps listening.** Each connection needs its own endpoint, so a server with 10 000 clients holds **10 001** descriptors — which is why `ulimit -n` matters and why `epoll` exists.
3. **UDP's `connect` sends nothing** — it records the peer address so later `send` calls need no destination. *(Measured: 11.6 μs against 107.1 μs.)* **There is no handshake because there is no connection.**
4. **Retransmissions, duplicate ACKs, the congestion window, actual segment boundaries** — none are visible from syscalls. **`tcpdump`/Wireshark, or `ss -ti` for some of the connection's internal state**, would be needed.

> `ss -ti` is worth demonstrating even though the lab does not require it — it prints `cwnd`, `rtt`
> and retransmission counts for established sockets, which is the closest thing to seeing congestion
> control without a capture.

**✅ CHECKPOINT 3**

---

## Part 4

| message | round trip | throughput |
|---:|---:|---:|
| 64 B | 18.6 μs | 6.6 MiB/s |
| 4 KiB | 21.2 μs | 369.3 MiB/s |
| 64 KiB | 51.3 μs | 2436.1 MiB/s |

*(Verified.)*

**Answers:**

1. **Two system calls, TCP state-machine processing, socket buffer management, checksums, and the scheduler waking the peer.** At 64 bytes these dominate entirely.
2. **The same principle as Week 7's storage curve:** *when a fixed cost is charged per operation, operation size is usually the most important variable in the system.* **This is the third time the course has hit it** — cache lines, storage blocks, now messages. Say so.
3. **Memory bandwidth and the scheduler.** No packet leaves the machine; at 64 KiB the benchmark is essentially `memcpy` through the kernel plus two context switches.
4. **17.5 μs against 18.6 μs.** On loopback there is no loss, no reordering and no congestion, so **TCP's machinery has nothing to do** — both protocols pay the same syscall and scheduling costs, which dominate.

**✅ CHECKPOINT 4**

---

## Part 5 — the important one

### 5.1

**18.6 μs against 19.1 μs** *(verified)* — nothing. **Nagle only delays a small write when there is already unacknowledged data**, and a strict send-then-receive pattern never creates that state.

### 5.2

**30.4 μs against 41 068 μs — 1350×.** *(Verified.)*

> **Two practical warnings, both learned the hard way when this was first run:**
>
> **Use ~60 iterations with Nagle on.** The first attempt used 5000 and **timed out at two minutes
> having printed nothing at all.**
>
> **Call `setvbuf(stdout, NULL, _IONBF, 0)`.** Output to a pipe is block-buffered, so a killed
> process loses everything it "printed".

**Answers:**

1. **Linux's delayed-ACK timer, ~40 ms.** The receiver holds its ACK hoping to piggyback it on outbound data.
2. Write 1 goes immediately → write 2 held by Nagle (small, and unacked data outstanding) → server has 4 of 20 bytes so sends nothing, and its delayed-ACK timer starts → ~40 ms later the ACK fires, Nagle releases, the server completes and replies.
3. **Nagle** avoids flooding the network with tiny packets; **delayed ACK** avoids sending bare ACKs that could have been piggybacked. **Both reduce packet count; together they each wait for the other**, and only a timer breaks the tie.
4. **A flag's cost is a property of the workload, not of the flag.** 3% and 1350× from the same option on the same machine, minutes apart.
5. **Bulk transfer with many small writes and no interleaved reads** — a logging stream, or a program that writes line by line to a socket it never reads from. There, Nagle's coalescing is a pure win.

> **This is the best twenty minutes in the week.** Two individually sensible optimisations that
> deadlock is a more valuable lesson than the protocol details, and it generalises: students will
> meet the same shape in lock ordering, cache coherence and scheduler interactions.

**✅ CHECKPOINT 5**

---

## Part 6 — optional

*(Verified, warm: `dns=0.007 connect=0.190 tls=0.402 ttfb=0.589 total=0.589`; cold DNS 3.510 s and `dig` 1487 ms against 3 ms.)*

TCP 183 ms, TLS 212 ms, response 187 ms — **three round trips, ~582 of 589 ms.** **The server's own work is invisible.**

---

## What Success Looks Like

1. Place a network hop on the same ladder as a cache miss and an SSD read.
2. Read `ss` output and name the states.
3. Use `strace -T` to see where a network program's time goes.
4. **Explain the Nagle/delayed-ACK deadlock**, having produced it.
5. **Distinguish waiting on the wire, on the kernel, and on a timer.**

Item 5 is the one Week 11 assumes.

---

*CS 201 · Week 8 · Lab 8 Solutions · Instructor Only*
