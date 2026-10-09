# CS 201 · Computer Organization & Architecture
## Week 8 · Lecture 2 of 3
### TCP — Reliability, Flow, and Congestion

*“TCP implementations will follow a general principle of robustness: be conservative in what you do, be liberal in what you accept from others.”* — Jon Postel, RFC 793, *Transmission Control Protocol* (1981), §2.10

---

**Reading:** CS:APP §11.4 · **Previous:** L25, layers and the latency ladder

**Coursework:** 📝 **PS 8** released today, due Fri of Week 9 17:00 · 📝 **PS 7** due Fri this week 17:00 · 📊 **Quiz 9** Mon of Week 9 · 🔬 **Lab 8** Tue of Week 9 15:00–16:50 · 📘 **Midterm 2** Mon of Week 10 18:00–19:15

---

## 1. What IP Gives You, and What It Does Not

**IP promises to try.** A packet may be dropped, duplicated, reordered, or corrupted. There is no acknowledgement, no retransmission, and no ordering.

**This is deliberate.** Every router along the path is stateless with respect to your connection, which is what lets the network scale and survive failures — the "end-to-end principle": put the intelligence at the edges, keep the middle dumb and fast.

**So reliability has to be built on top, at the endpoints.** That is TCP.

| | TCP | UDP |
|---|---|---|
| Delivery | reliable, retransmitted | best effort |
| Ordering | in order | none |
| Connection | three-way handshake | none |
| Boundaries | **byte stream** — none preserved | datagram — preserved |
| Flow control | yes | no |
| Congestion control | **yes** | no |
| Header | 20 bytes | 8 bytes |

**"Byte stream, no boundaries" is the one people get wrong.** Two `send` calls of 100 bytes may arrive as one 200-byte `recv`, or as 37 and 163. **TCP guarantees the bytes and their order, not your framing.** Every protocol on top of TCP therefore has to delimit its own messages — a length prefix, or a terminator like HTTP's blank line. **PS 8 makes you handle this.**

---

## 2. The Three-Way Handshake

```
client                          server
   │                               │
   ├───── SYN, seq=x ─────────────▶│
   │◀──── SYN-ACK, seq=y, ack=x+1 ─┤
   ├───── ACK, ack=y+1 ───────────▶│
   │                               │
```

**One round trip before any data moves.** That is the 183 ms in L25 §5's page load, and it is why connection reuse matters so much.

**The sequence numbers are the point**, not a formality. They are randomised at connection setup — if they were predictable, an off-path attacker could inject data into someone else's connection. **Sequence-number prediction was a real attack**, and randomising the initial value is the fix.

**Closing takes four messages** (FIN, ACK, FIN, ACK) because each direction is shut down independently. The closer then waits in **`TIME-WAIT`** for twice the maximum segment lifetime, so that a delayed duplicate from the old connection cannot be mistaken for data on a new one reusing the same four-tuple.

**You can see all of this on a running machine:**

```
$ ss -tan | awk 'NR>1{print $1}' | sort | uniq -c | sort -rn
     18 ESTAB
      7 TIME-WAIT
      4 LISTEN
      1 LAST-ACK
      1 FIN-WAIT-1
```

*(Measured — an ordinary desktop.)* **Seven sockets sitting in `TIME-WAIT` doing nothing but waiting.** On a busy server this becomes a resource problem, and `SO_REUSEADDR` exists because of it.

---

## 3. Reliability: Sequence Numbers and Retransmission

Every byte is numbered. The receiver acknowledges the highest contiguous byte received. **If an ACK does not arrive in time, the sender retransmits.**

**"In time" is the hard part.** The timeout must exceed the round-trip time — but the RTT varies from 18 μs on loopback to 187 ms across the Atlantic, and changes minute to minute. **So TCP measures it continuously**, keeping a smoothed estimate and a variance, and sets the retransmission timeout well above both. Too short and it floods the network with needless duplicates; too long and it stalls after a loss.

**Fast retransmit** short-circuits the timer: three duplicate ACKs for the same sequence number mean a segment is missing while later ones are arriving, so the sender resends immediately rather than waiting.

---

## 4. Flow Control: Do Not Overrun the Receiver

Every ACK carries a **window** — how many more bytes the receiver has buffer space for. The sender may not exceed it. **If the application stops reading, the window shrinks to zero and the sender stops.**

**This is backpressure**, and it is why a slow client cannot exhaust a fast server's memory. `ss` shows it directly as `Recv-Q` and `Send-Q`.

**Flow control is about the receiver. Congestion control is about the network.** They are separate mechanisms solving separate problems, and conflating them is the most common misunderstanding of TCP.

---

## 5. Congestion Control: Do Not Overrun the Network

Nothing tells a sender how much capacity the path has. **TCP discovers it by increasing its rate until packets are lost, then backing off.** Loss is the signal.

| Phase | Behaviour |
|---|---|
| **Slow start** | Window **doubles** every RTT — exponential, despite the name |
| **Congestion avoidance** | After a threshold, window grows by **one segment per RTT** — linear |
| **Loss (triple duplicate ACK)** | Halve the window, continue — "fast recovery" |
| **Loss (timeout)** | Window back to 1. **Something is badly wrong** |

**This is AIMD — additive increase, multiplicative decrease** — and it provably converges to a fair share between competing flows.

**Slow start is why short connections never reach full speed.** The window starts at ~10 segments (~14 KB) and doubles per RTT. On a 187 ms link, reaching a 1 MB window takes about 7 round trips — **1.3 seconds** — and most HTTP responses finish long before that. **The transfer spends its whole life in slow start**, which is another reason connection reuse matters: an established connection has already paid.

> **Loss as a congestion signal was a 1980s design decision and it has aged imperfectly.** On wireless
> links, loss often means interference rather than congestion, and halving the window is exactly
> wrong. Modern algorithms like **BBR** model bandwidth and RTT directly instead of waiting for loss.

---

## 6. Nagle's Algorithm: Measured, Twice

**The problem Nagle solves:** a program sending one byte at a time produces 41-byte packets carrying 1 byte of data. **Nagle's rule: if there is unacknowledged data outstanding, buffer small writes until it is acknowledged or a full segment accumulates.**

### Where it costs nothing

A strict request-response loop — one `send`, one `recv` — on loopback:

```
TCP loopback, NODELAY    64 B round-trip  18.6 us
TCP loopback, Nagle on   64 B round-trip  19.1 us
```

*(Measured.)* **Essentially no difference**, because there is never a *second* small write waiting: every send is immediately followed by a receive, so nothing is ever held back.

### Where it costs 1350×

Now the pattern real RPC code writes — a header, then a body, then wait for the reply:

```c
send(s, hdr,  4, 0);        /* write 1 */
send(s, body, 16, 0);       /* write 2 */
recv(s, reply, 4, MSG_WAITALL);
```

```
TCP_NODELAY (Nagle off)      30.4 us per write-write-read
Nagle ON                  41068.0 us per write-write-read
```

*(Measured.)* **41 milliseconds per round trip. A 1350× penalty.**

**And the number 41 ms is the diagnosis.** It is Linux's **delayed-ACK timer**, and the deadlock runs like this:

1. Write 1 goes out immediately — nothing is unacknowledged yet.
2. Write 2 is small **and** there is unacknowledged data, so **Nagle holds it**.
3. The server has 4 bytes but is waiting for the whole 20-byte message, so it **does not reply**.
4. The server's **delayed ACK** waits ~40 ms hoping to piggyback the ACK on a response that never comes.
5. The ACK finally fires; Nagle releases write 2; the server completes and replies.

**Two optimisations, each individually sensible, that deadlock against each other.**

> **This is why every RPC library, database driver and game server sets `TCP_NODELAY`.** It is also a
> perfect example of why you measure: the same flag showed a 3% difference in one access pattern and
> a 1350× difference in another, **on the same machine, minutes apart.**

---

## 7. What to Take Away

1. **IP is best-effort by design**; reliability belongs at the endpoints.
2. **TCP is a byte stream with no message boundaries.** Your protocol must frame itself.
3. **The handshake costs one RTT** before any data — 183 ms on the measured link.
4. **`TIME-WAIT` exists so old duplicates cannot corrupt a new connection**, and there were 7 on an idle desktop.
5. **Flow control protects the receiver; congestion control protects the network.** Different mechanisms.
6. **Slow start means short connections never reach full speed.**
7. **Nagle cost 3% in one pattern and 1350% × 13 in another.** Measure the pattern you actually have.

---

## Exercises

1. Two `send` calls of 100 bytes each. List three different ways the receiver's `recv` calls could legitimately observe them.
2. Why are initial sequence numbers randomised? Name the attack that motivated it.
3. Why does closing take four messages when opening takes three?
4. A server has 30 000 sockets in `TIME-WAIT`. Explain the cause, the risk, and one mitigation.
5. A link has 187 ms RTT and the initial window is 14 KB. How many round trips to reach a 1 MB window under slow start? How long is that in seconds?
6. Explain the Nagle/delayed-ACK deadlock in your own words, and say why 41 ms is the diagnostic number.
7. Give a workload where leaving Nagle **on** is the right choice, and justify it.

---

*Next: L27 — the application layer, and what a round trip really costs.*
