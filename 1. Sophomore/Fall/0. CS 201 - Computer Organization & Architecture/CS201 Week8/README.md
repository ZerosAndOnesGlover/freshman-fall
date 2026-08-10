# CS 201 · Computer Organization & Architecture
## Week 8: Computer Networks Fundamentals

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), ECE 110 (digital logic)
**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** PS 8 (due Week 9 Friday), Lab 8 *(sat Tuesday of Week 9)*, and **Quiz 8 on Monday, covering Week 7**.

> ⚠️ **Project 1 is due Week 9, Friday — the same day as PS 8.** PS 8 is deliberately modest for
> that reason. **If you are behind on the simulator, do it first.**

---

### Why This Week Exists

Because the cost ladder has one more rung, and it is the tallest.

Week 7 ended at `fsync` — 3.9 milliseconds. **This week measures an internet round trip at 187 milliseconds**, and a single HTTPS page load at 589. From an L1 hit at 1.2 nanoseconds, that is a factor of about **500 million**, all on the machine in front of you.

**And the reason it is tall is not engineering.** Bandwidth has improved by orders of magnitude in twenty years; transatlantic latency has not improved at all, because the speed of light does not negotiate. **Every protocol development of the last two decades — keep-alive, HTTP/2, TLS 1.3, QUIC, CDNs — is an attack on the same term in the same sum: how many times must a message cross the ocean before the user sees anything.**

The week also contains the clearest example this course has of **two correct optimisations that deadlock against each other**, at a measured cost of 1350×.

---

### Learning Objectives

By the end of Week 8, you should be able to:

1. Name the TCP/IP layers, their units, and one protocol at each.
2. Compute encapsulation overhead and the payload size at which it becomes acceptable.
3. Explain why global routing needs hierarchical addresses.
4. Work with CIDR notation — network, broadcast and host count.
5. Draw the three-way handshake and say how many round trips precede data.
6. Explain `TIME-WAIT` and what breaks without it.
7. **Explain that TCP is a byte stream, and frame a protocol on top of it.**
8. Distinguish flow control from congestion control.
9. Explain slow start and why short connections never reach full speed.
10. **Produce and diagnose the Nagle / delayed-ACK deadlock.**
11. Decompose a page load into round trips and say which optimisation removes which.
12. Apply Little's Law to a networked server.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L25 Layers and the Latency Ladder.md` | The completed ladder, why layers exist, addressing, and where a page load goes |
| `lectures/L26 TCP Reliability Flow and Congestion.md` | Handshake, `TIME-WAIT`, retransmission, windows, AIMD — and Nagle measured twice |
| `lectures/L27 The Application Layer and the Cost of a Round Trip.md` | Sockets, message size, HTTP, and why every improvement removes round trips |
| `assignments/PS 8 A TCP Echo Client and Server.md` | Framing, short reads, a UDP comparison, and the deadlock reproduced |
| `assignments/QUIZ 8 Week 8 Monday.md` | Ten minutes on Week 7. **Unmarked — key in the paper** |
| `lab/LAB 8 Observing TCP.md` | `strace` and `ss` instead of Wireshark, and 25 minutes making Nagle deadlock |
| `resources/Reading Guide Week 8.md` | CS:APP Ch. 11, what it omits, and `man 7 tcp` |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A flag's cost is a property of the workload, not of the flag.**

`TCP_NODELAY`, measured twice on the same machine, minutes apart:

| Pattern | Nagle off | Nagle on | Ratio |
|---|---:|---:|---:|
| `send` → `recv` | 18.6 μs | 19.1 μs | **1.03×** |
| `send` → `send` → `recv` | 30.4 μs | **41 068 μs** | **1350×** |

*(Measured.)*

**41 ms is not a slow network. It is Linux's delayed-ACK timer.** Nagle holds the second small write until the first is acknowledged; the server holds its ACK hoping to piggyback it on a reply it cannot yet send. **Two individually sensible optimisations, each waiting for the other**, broken only by a timer.

**Every RPC library, database driver and game server sets `TCP_NODELAY`** because of this — and you now know why, and know the diagnostic number.

---

### Assessment Reminder

**Labs and quizzes carry no weight**; the four weighted components already total 100%. Both remain required.

**Quiz 8 is Monday**, covering Week 7. **Lab 8 is sat Tuesday of Week 9.**

**A note on tooling.** The curriculum lists Wireshark. **It is not installed, and `tcpdump` cannot capture without root** — so Lab 8 uses `strace`, `ss` and your own timing code instead. For this course that is arguably the better view: `strace` shows the user/kernel boundary that Weeks 6 and 7 were about. **What you cannot see this way — retransmissions, the congestion window, actual segment boundaries — the lab tells you explicitly.**

**The lab network is a tethered Wi-Fi link**, which is why the internet RTT is 187 ms rather than the ~20 ms of a wired campus connection. **Ratios transfer; absolute figures do not.**

---

### Connections

**Back:** **Week 7's Little's Law** returns with a bigger latency — 1000 requests/second at 187 ms needs 187 in flight. **Week 7's message-size curve** reappears exactly: 64 B gives 6.6 MiB/s and 64 KiB gives 2436 MiB/s on the same socket, for the same reason storage blocks behaved that way. **Week 6's file descriptor** is what a socket is.

**Forward:** **Week 9 attacks all of it** — sequence-number prediction, and the fact that a server parsing attacker-controlled input is Week 3's stack with a network in front of it. **Week 11's roofline** needs this week's distinction between waiting on the wire, on the kernel, and on a timer.

**Sideways:** **PROG 201 is writing `epoll` servers this term** — that is the answer to Little's Law here. **CS 302 in Year 3** is this week for a semester, with the derivations.

---

*CS 201 · Week 8 · © CSE Department*
