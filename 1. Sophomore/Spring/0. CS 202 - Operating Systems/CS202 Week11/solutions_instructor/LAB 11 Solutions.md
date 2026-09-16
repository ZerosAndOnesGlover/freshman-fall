# CS 202 · Lab 11 — Solutions and TA Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Session:** Tuesday of Week 12, 15:00–16:50, BH 210. **Unmarked** — checked off in the session.

**This is the last ordinary lab; Lab 12 is demo day.** Project 2 is due in the completion period, so **expect questions about the double-indirect block** — and leave time for them.

**What the session is actually for.** Parts A–C are three measurements that make "distributed" concrete before any algorithm appears: distance costs a thousand times more than a system call, a successful `write` is not a delivery, and the machine's own clocks disagree by eight hours. **Part D is then the algorithm surviving what those facts do to it.**

---

## Timing

| Minutes | Part | TA action |
|---|---|---|
| 0–20 | A | `ping` needs the campus network; if it is down, use any host that answers |
| 20–35 | B | Instant; the discussion is the point |
| 35–50 | C | The `BOOTTIME` gap surprises everyone |
| 50–95 | **D** | **The lab.** The loss sweep takes a few minutes; start it and discuss while it runs |
| 95–105 | E | |
| 105–110 | Checkoff and Project 2 questions | |

---

## Answers

Reference machine: i5-8250U, kernel 7.0.0-31, Wi-Fi, NTP active.

### Q1 — the ladder

| Round trip | Measured | × a function call |
|---|---:|---:|
| function call | 0.0018 µs | 1 |
| system call (`getppid`) | 0.84 µs | ~470 |
| pipe, two processes | 8.5 – 10.5 µs | ~5,000 |
| loopback UDP | 19.1 – 20.3 µs | ~11,000 |
| loopback TCP | 21.4 – 22.5 µs | ~12,000 |
| **`ping 8.8.8.8`** | **22.6 – 24.5 ms** | **~13,000,000** |

**The largest jump is the last one — three orders of magnitude** — and it is the only one that is physics rather than software.

### Q2 — where loopback's 20 µs goes

**Four things:** two **system calls** (0.84 µs each); two **context switches** (~3 µs each, Week 5 L17 §5); the **protocol stack** twice — TCP/IP headers, checksums, socket buffers; and two **copies** between user and kernel memory. **Accept any four; the point is that no wire is involved.**

### Q3 — throughput

**Loopback:** 0.5 ms + 0.02 ms ≈ 0.52 ms per request → **~1,920 requests/s per connection.**
**Internet:** 0.5 ms + 23 ms ≈ 23.5 ms → **~43 requests/s per connection.**

**The round trip dominates by 46 to 1.** **What to change: stop waiting** — pipeline requests, batch them, or replicate the data so the consultation is local. **Adding CPU does nothing.**

### Q4 — 2.6 MB in flight

```
write() reported success for 2643968 bytes the peer never read
```

**They are in the sender's socket send buffer and the receiver's receive buffer** — **RAM on both machines.** If the sender crashes now, **everything not yet read is gone**, and the receiver has no way to ask for it. **[The two buffers are the marks.]**

### Q5 — the same failure on a network

**A receiver that has stopped reading, a network that has partitioned, and a receiver that crashed all look identical to the sender**: writes succeed until the buffers fill, then block or fail. **The sender cannot distinguish slow from dead** — L34 §5 — which is why the only available answer is a **timeout**, and why every protocol above this needs acknowledgements of its own.

### Q6 — the clocks

```
CLOCK_MONOTONIC  33995.7    CLOCK_BOOTTIME  63640.1
```

**A difference of 29,645 s ≈ 8.2 hours: the time the laptop spent suspended.** `MONOTONIC` stops during suspend; `BOOTTIME` counts it. **Neither is wall-clock time**, and `REALTIME` may jump when NTP corrects it.

### Q7 — which clock

| For | Use | Why not the others |
|---|---|---|
| a 30-second request timeout | **`CLOCK_MONOTONIC`** | `REALTIME` can jump backwards and hang the timeout; `BOOTTIME` would count a suspend as elapsed |
| a certificate's expiry | **`CLOCK_REALTIME`** | it is a statement about wall-clock time; the others have no relation to dates |
| how long a function took | **`CLOCK_MONOTONIC`** (or `MONOTONIC_RAW` to avoid NTP slewing) | `REALTIME` can be adjusted mid-measurement |

### Q8 — the quiet run

**Elected at t=170.** **The 170 leaderless ticks are start-up**: 158 waiting for the first timeout to expire and 12 running the election. **There is no leader when a cluster starts, and nothing can be done about the first timeout.**

### Q9 — the crash

**Leaderless from t=500 to t=732 — 232 ticks: 219 waiting, 13 electing.**

**With timeouts halved to [75, 150):** the outage falls to roughly **120 ticks** — the wait halves, the election does not change. **What gets worse:** spurious elections. With heartbeats every 50 ticks and delays up to 11, a couple of unlucky heartbeats now exceed the shortest timeouts, and the cluster deposes a healthy leader. **Students who rebuild and see extra elections in the log have the answer in front of them.**

### Q10 — the partition

**Two leaders from t=491 to t=1247 — 756 ticks.** Node 0 (term 1) could talk to node 1 only: **it could accept requests and commit none.** Node 2 (term 2) had three of five and could commit. **The heal deposed node 0** — the first message carrying term 2 made it a follower, 47 ticks later.

### Q11 — the knee

| Loss | Elections | Leaders | Leaderless |
|---:|---:|---:|---:|
| 0% | 1.2 | 1.0 | 3.9% |
| 20% | 4.0 | 2.8 | 4.8% |
| 40% | 19.8 | 5.4 | 22.9% |
| 60% | 54.8 | 4.6 | 60.3% |
| 80% | 85.6 | 0.4 | 97.7% |

**The knee is between 20% and 40%.** **Elections rise and leaders fall** because winning needs a request *and* a reply to survive for a majority: at 80% loss almost no candidate collects two replies, so candidates stand repeatedly and fail — **and each failed election adds traffic.** **The cluster is busy doing nothing.**

### Q12 — the invariant

**No violations in 150 runs** (50 seeds × 3 loss rates), and none in the partition runs either.

**What is checked:** that **no two nodes ever become leader in the same term.** **No amount of loss or partitioning can break it** because it follows from counting, not from timing: a win needs votes from more than half the nodes, each node votes at most once per term, and two such sets must overlap. **Loss and partitions can prevent elections from succeeding; they cannot create extra votes.**

### Q13 — the tool that is not here

```
$ which etcd etcdctl zookeeper-server consul
$
```

**What etcd would have shown:** a **real** cluster's view of itself — `etcdctl endpoint status` prints each member's ID, term, revision and whether it is the leader; `etcdctl watch` shows log entries being replicated and committed, which the simulator has no log to show.

**What you can do here that you could not do to production etcd:** **drop 40% of its messages, partition it on command, crash its leader at a chosen instant, and read every message it sent** — with a seed that makes the run repeatable. **Accept any one of each.**

---

*CS 202 · Week 11 · Lab 11 Solutions · Instructor Only*
