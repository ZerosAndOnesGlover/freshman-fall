# CS 201 · Week 8 · Lab 8
## Observing TCP — Without a Packet Capture

---

**When:** **Tuesday of Week 9**, 15:00–16:50, BH 210 — *after* Week 8's three lectures
**Covers:** Week 8 · **Assessment:** unmarked, checked off by the TA
**You need:** `gcc`, `ss`, `ip`, `ping`, `curl`, `dig`, `strace`.

---

## Before You Start: No Wireshark

The curriculum lists Wireshark. **It is not installed on the lab image, and `tcpdump` is present but unusable:**

```
$ tcpdump -i lo -c 2 -n
tcpdump: lo: You don't have permission to perform this capture on that device
(socket: Operation not permitted)
```

*(Verified.)* Packet capture needs `CAP_NET_RAW`, which needs root.

**So this lab observes TCP from above rather than on the wire**, using three tools you already have:

| Tool | Shows you |
|---|---|
| **`strace`** | The exact system calls, in order, with arguments and timings |
| **`ss`** | Socket state — the TCP state machine, live |
| **your own code** | Timing, which is the thing this course cares about most |

**For this course that is arguably the better view.** CS 201 is about what the *machine* does; `strace` shows the boundary between your program and the kernel, which is exactly where Week 8's abstractions are drawn. **If you have a machine where you are root, run `tcpdump -i lo -n port 54321` alongside Part 3 — it is worth seeing once.**

---

## Part 1 — The Latency Ladder (20 min)

```bash
ping -c 5 -q 127.0.0.1          # loopback
ip route | grep default          # find your gateway
ping -c 5 -q 192.168.137.1       # LAN
ping -c 5 -q 1.1.1.1             # internet
```

Measured on the lab machine:

| target | RTT |
|---|---:|
| `127.0.0.1` | **0.084 ms** |
| LAN gateway | **2.388 ms** |
| `1.1.1.1` | **186.950 ms** |

*(Verified.)*

**Answer:**

1. Place all three on the course's cost ladder alongside L1 (1.2 ns), DRAM (137 ns), an SSD read (157 μs) and `fsync` (3.9 ms). **Which network hop is faster than the SSD?**
2. The internet RTT is 187 ms. Compute how many L1 hits fit in it.
3. Light in fibre travels ~200 000 km/s. **What distance does 187 ms correspond to?** Compare with a plausible physical route and account for the difference.
4. `ip link show` — report the MTU of `lo` and of your network interface. **Why are they different by a factor of 40?**

**✅ CHECKPOINT 1** — your three RTTs and the four answers.

---

## Part 2 — The TCP State Machine, Live (20 min)

```bash
ss -tan | awk 'NR>1{print $1}' | sort | uniq -c | sort -rn
```

On an ordinary idle desktop:

```
     18 ESTAB
      7 TIME-WAIT
      4 LISTEN
      1 LAST-ACK
      1 FIN-WAIT-1
```

*(Verified.)*

**Answer:**

1. What is each state? Draw the part of the state machine connecting `ESTAB`, `FIN-WAIT-1`, `LAST-ACK` and `TIME-WAIT`.
2. **Seven sockets are in `TIME-WAIT` doing nothing.** Why does the state exist, how long does it last, and what breaks without it?
3. `ss -tan` also shows `Recv-Q` and `Send-Q`. Which TCP mechanism do those columns expose?
4. Run `curl -s -o /dev/null https://example.com` and immediately re-run the `ss` count. **What changed?**

**✅ CHECKPOINT 2** — your state counts and the four answers.

---

## Part 3 — Watch the Handshake With `strace` (25 min)

Write a minimal TCP client and server on loopback (or use the PS 8 skeleton), then:

```bash
strace -f -T -e trace=network,close ./server &
strace -T -e trace=network,close ./client
```

**`-T` prints the time spent in each call.** You should see, on the client:

```
socket(AF_INET, SOCK_STREAM, IPPROTO_IP) = 3   <0.000015>
connect(3, {sa_family=AF_INET, ...})     = 0   <0.000107>
sendto(3, "...", 64, 0, NULL, 0)         = 64  <0.000012>
recvfrom(3, "...", 64, 0, NULL, NULL)    = 64  <0.000019>
close(3)                                       <0.000021>
```

**Answer:**

1. **`connect` takes far longer than `send`.** Why? What happened during it that did not happen during `send`?
2. The server's trace shows `socket`, `bind`, `listen`, `accept`. **`accept` returns a different descriptor number than the listening socket.** Why does that matter for a server with 10 000 clients?
3. Repeat with a **UDP** client. Measured on this machine: **UDP `connect` 11.6 μs against TCP's 107.1 μs** *(verified)*. **What does UDP's `connect` actually do?**
4. `strace` shows system calls, not packets. **Name one thing in L26 you cannot see this way** and say what tool you would need.

**✅ CHECKPOINT 3** — both traces and the four answers.

---

## Part 4 — Message Size (20 min)

Build an echo benchmark: send a message, wait for it back, repeat. Same connection, vary the size.

| message | round trip | throughput |
|---:|---:|---:|
| 64 B | 18.6 μs | 6.6 MiB/s |
| 4 KiB | 21.2 μs | 369.3 MiB/s |
| 64 KiB | 51.3 μs | 2436.1 MiB/s |

*(Verified, TCP loopback, `TCP_NODELAY` set.)*

**Answer:**

1. A **1024×** larger message costs **2.8×** the time. What fixed cost is being amortised? Name at least three components of it.
2. **Compare this curve's shape with Week 7's storage table** (4 KiB → 1 MiB gave an 18× throughput rise). What single principle covers both?
3. At 64 KiB, what is the loopback benchmark actually measuring? *(Hint: no packet leaves the machine.)*
4. Also measure UDP at 64 B. Reference *(verified)*: **17.5 μs against TCP's 18.6 μs.** **Why so close, when TCP does so much more?**

**✅ CHECKPOINT 4** — your table and the four answers.

---

## Part 5 — Make Nagle Deadlock (25 min)

The most instructive twenty minutes of the week.

### 5.1 The pattern where Nagle costs nothing

Your Part 4 benchmark is `send` → `recv` → `send` → `recv`. Run it with and without `TCP_NODELAY`.

Reference *(verified)*: **18.6 μs against 19.1 μs — no meaningful difference.**

**Explain why Nagle has nothing to hold back in this pattern.**

### 5.2 The pattern where it costs 1350×

Now write the shape real RPC code has — **two small writes, then wait for a reply**:

```c
send(s, hdr,  4,  0);                 /* write 1: header */
send(s, body, 16, 0);                 /* write 2: body   */
recv(s, reply, 4, MSG_WAITALL);       /* now wait        */
```

and have the server read the **full 20 bytes** before replying:

```c
while ((n = recv(c, b, 20, MSG_WAITALL)) == 20) send(c, b, 4, 0);
```

Run it both ways:

```
TCP_NODELAY (Nagle off)      30.4 us per write-write-read
Nagle ON                  41068.0 us per write-write-read
```

*(Verified.)*

> ⚠️ **Use few iterations with Nagle on** — 60 is plenty. At 41 ms each, 5000 iterations takes over
> three minutes, and **the first attempt at this measurement timed out at two minutes having printed
> nothing.** Also call `setvbuf(stdout, NULL, _IONBF, 0)`, or a timeout will kill the process before
> it flushes.

**Answer:**

1. **41 ms is a suspiciously round number.** What kernel timer is it, and what is it for?
2. Walk the deadlock step by step: which side is waiting for what, at each of the four stages?
3. **Both Nagle and delayed ACK are sensible optimisations in isolation.** State what each is for, then explain why they interact badly.
4. Your Part 5.1 measurement showed a 3% difference and 5.2 showed 1350×, **on the same machine, minutes apart**. What does that tell you about benchmarking a flag rather than a workload?
5. Give one workload where leaving Nagle **on** is correct.

**✅ CHECKPOINT 5** — both measurements and all five answers.

---

## Part 6 — Optional: Where a Page Load Goes

```bash
curl -s -o /dev/null -w "dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer} total=%{time_total}\n" https://example.com
```

Run it twice — **the first run has a cold DNS cache.**

*(Verified: cold `dns=3.510s total=4.233s`; warm `dns=0.007s connect=0.190s tls=0.402s ttfb=0.589s total=0.589s`. And `dig` alone: **1487 ms cold, 3 ms warm** — 496×.)*

**Decompose the warm run into phases and count round trips against your Part 1 internet RTT.** How much of the 589 ms was the server?

---

## Before You Leave

| Task | Command |
|---|---|
| Socket states | `ss -tan`, `ss -tanp` for processes |
| Listening sockets | `ss -tlnp` |
| Syscall trace with timings | `strace -T -e trace=network ./prog` |
| Interface and MTU | `ip -br addr`, `ip link show` |
| Routing | `ip route` |
| Page-load breakdown | `curl -w` with `time_*` variables |
| DNS timing | `dig +stats example.com` |
| Packet capture *(needs root)* | `tcpdump -i lo -n port 54321` |

**The habit:** when a network program is slow, **find out whether you are waiting on the wire, on the kernel, or on a timer.** Part 5's 41 ms was a timer, and no amount of bandwidth would have fixed it.

---

*CS 201 · Week 8 · Lab 8*
