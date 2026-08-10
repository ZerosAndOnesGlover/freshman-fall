# CS 201 · Quiz 9
## Administered: Monday, Week 9 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 8** — networks, TCP, and the cost of a round trip.

**Instructions:** Closed notes. 10 minutes.

> **Unmarked, no weight.** Key below. Sit it closed-book first.

---

**Q1.** Name the four TCP/IP layers and one protocol at each.

&nbsp;

&nbsp;

---

**Q2.** TCP is a byte stream. Two `send` calls of 100 bytes — give two ways the peer's `recv` might observe them.

&nbsp;

&nbsp;

---

**Q3.** Why does the three-way handshake matter for the latency of a short HTTP request?

&nbsp;

&nbsp;

---

**Q4.** Distinguish flow control from congestion control in one sentence each.

&nbsp;

&nbsp;

---

**Q5.** `TCP_NODELAY` changed one workload by 3% and another by 1350×. The 1350× case measured 41 ms per round trip. What is 41 ms?

&nbsp;

&nbsp;

---

**Q6.** A 64 B message gave 6.6 MiB/s and a 64 KiB message gave 2436 MiB/s on the same socket. Why?

&nbsp;

&nbsp;

---

**Q7.** An HTTPS page load took 589 ms on a 187 ms link. Where did the time go?

&nbsp;

&nbsp;

---

<div style="page-break-after: always;"></div>

---

## Answer Key — Mark Your Own

**Q1.** **Application** (HTTP/DNS/SSH), **Transport** (TCP/UDP), **Network** (IP), **Link** (Ethernet/Wi-Fi). *(Accept a fifth, Physical.)*

---

**Q2.** Any two of: as two 100-byte reads; as one 200-byte read; as 37 + 163; as any other split. **TCP preserves order and completeness, not message boundaries** — so a protocol on top must frame itself (length prefix or delimiter).

---

**Q3.** **The handshake costs one full round trip before any data is sent** — 183 ms on the measured link. A short request's total time is dominated by round trips, so the handshake is a large fraction of it, which is why connection reuse matters so much.

---

**Q4.** **Flow control** stops the sender overrunning the **receiver's buffer** (the advertised window). **Congestion control** stops the sender overrunning the **network** (the congestion window, via AIMD). Different windows, different problems; the sender obeys the smaller.

---

**Q5.** **Linux's delayed-ACK timer (~40 ms).**

Nagle held the second small write until the first was acknowledged; the receiver held its ACK hoping to piggyback it on a reply it could not yet send. Each waited for the other, and the delayed-ACK timer firing is what broke the deadlock. **Two sensible optimisations that deadlock — which is why RPC code sets `TCP_NODELAY`.**

---

**Q6.** **A fixed per-message cost** — two system calls, TCP state-machine work, buffer management, scheduler wakeups — is amortised over more bytes. At 64 B you measure the software stack; at 64 KiB you measure memory bandwidth.

*Same principle as Week 7's storage-block curve and Week 4's cache lines: when a fixed cost is charged per operation, operation size is the dominant variable.*

---

**Q7.** **Almost entirely round trips.** TCP handshake 183 ms + TLS handshake 212 ms + server response 187 ms ≈ three RTTs ≈ 582 of 589 ms. **The server's own processing was invisible inside the last round trip.**

*This is why every protocol improvement removes round trips, and why only a CDN — which changes the distance — beats a number set by the speed of light.*

---

### What to Do With Your Score

| If you missed | Reread |
|---|---|
| Q1, Q2, Q3 | L25 §2–§3, L26 §1–§2 |
| Q4 | L26 §4–§5 |
| **Q5** | **L26 §6 — the measured deadlock** |
| Q6, Q7 | L27 §3 and §4 |

**Q5 is the one to be sure of.** Two correct optimisations that interact badly is a pattern you will meet again in Week 10's cache coherence.

---

*CS 201 · Week 9 · Quiz 9 · covers Week 8 · ungraded*
