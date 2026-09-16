# CS 202 · Operating Systems
## Week 11: Distributed Systems Concepts

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 201, PROG 201
**Assessment for this course (overall):** Problem Sets 30%, Projects 30%, Midterms 25%, Final 15%
**This week's deliverables:** **Project 1 due Friday, 17:00 (15%)**, PS 10 due **Friday**, PS 11 released **Wednesday**, **Quiz 11** at the start of **Monday's** lecture (covers Week 10) — **the last quiz of the term**.
**Lab 10 is sat on the Tuesday of this week; Lab 11 covers this week and is sat on the Tuesday of Week 12.**

> ### **Project 1 is due this Friday at 17:00.**
> The lottery scheduler, `settickets`, `getpinfo`, the locking write-up and the measurements.
> **Bring a kernel that does not boot to Tuesday's lab** — that is what the session is for.
> **Project 2 is due in the completion period**, and its Part B checkpoint is the Week 12 lab.

---

### Why This Week Exists

Because every mechanism in this course has assumed one machine, and three of its assumptions fail the moment there are two.

**There is no shared memory**, so a lock cannot be taken — agreement has to be manufactured by counting votes. **Failures are partial**: a machine that does not answer may be dead, or busy, or perfectly fine behind a broken switch, **and nothing can tell you which**. **There is no clock**: this laptop's own `CLOCK_BOOTTIME` and `CLOCK_MONOTONIC` differ by eight hours of suspend, and two machines' wall clocks differ by however much NTP has not yet fixed.

**And distance is expensive.** A function call costs 1.8 ns, a system call 0.84 µs, a loopback round trip 20 µs — and a round trip to another machine **23 milliseconds**, thirteen million times the function call. **That number, not instruction count, is what a distributed algorithm is designed around.**

**So this week builds the one thing that makes the rest possible**: a protocol that lets five machines agree on who is in charge, and keeps agreeing while messages are lost, delayed and cut in half.

---

### Learning Objectives

By the end of Week 11, you should be able to:

1. Name the three assumptions that fail across machines, and give a measurement of each.
2. **Quote the latency ladder** from a function call to a network round trip, and use it to bound throughput.
3. Explain why a successful `write()` is not a delivery, and what follows for retries.
4. Explain why **idempotence** is the only defence against an unacknowledged message.
5. Distinguish `CLOCK_REALTIME`, `MONOTONIC` and `BOOTTIME`, and choose correctly among them.
6. State **Two Generals** and **FLP**, and say how real protocols escape them.
7. Explain **terms** as a logical clock, and the rule that makes staleness detectable.
8. Explain **Raft's leader election**: timeouts, one vote per term, majorities, heartbeats.
9. **Prove** that two leaders cannot share a term.
10. **Measure** the cost of a leader failure, and split it into detection and election.
11. Explain **split brain**, why Raft permits it, and what it prevents instead.
12. Explain what a partition forces a system to choose, and what real systems choose.

---

### This Week's Materials

| File | Purpose |
|---|---|
| [[L34 Why Distribution Is Different]] | The three broken assumptions; **the latency ladder, 1.8 ns to 23 ms**; **2.6 MB "sent" to a stopped reader**; `BOOTTIME` eight hours ahead of `MONOTONIC`; Two Generals and FLP, and the two ways out |
| [[L35 Agreement Rafts Leader Election]] | The replicated log; **terms as a logical clock**; the election, one vote per term, majorities; **a crashed leader costing 232 ticks, 219 of them waiting**; why 2*f* + 1 |
| [[L36 Partitions Timeouts and What Real Systems Do]] | **Split brain measured — two leaders for 756 ticks**, and why only one could commit; **loss from 0 to 80%**, and the knee; the timeout as the whole design; etcd, ZooKeeper, Consul; what a partition forces you to choose |
| [[CS202 Week11/assignments/QUIZ 11 Week 11 Monday\|QUIZ 11 Week 11 Monday]] | Ten minutes, covers **Week 10**, answer key printed — **the last quiz** |
| [[PS 11 Raft Leader Election]] | Implement the election, then break it: crash the leader, lose 40% of messages, partition the cluster. Due **Friday of Week 12** |
| `assignments/ps11/raftsim.c` | The simulator: five `TODO`s, with the network, the schedule and **the safety check** provided |
| [[LAB 11 Raft Observed]] | The latency ladder; `write` without delivery; three clocks; **and Raft crashed, partitioned and starved of messages**. **Tuesday of Week 12** |
| `lab/netlat.c`, `lab/delivered.c`, `lab/clocks.c` | The three measurements that make "distributed" concrete |
| [[CS202 Week11/resources/Reading Guide Week 11\|Reading Guide Week 11]] | OSTEP 48, the Raft paper, Lamport, FLP, CAP, and the Jepsen reports |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A lock works because every thread can see the same word of memory. Across machines there is no such word.**

So agreement is manufactured, every time, by **counting votes from a majority** — and the whole of Raft's safety is that two majorities of the same set must overlap. **Everything else is timing**: a timeout to notice that the leader is gone, randomisation so that the replacements do not collide, and heartbeats to stop the timers of everyone who should stay quiet.

**And the timeout is the design.** Measured here: of the 232 ticks a cluster spent without a leader after one crashed, **219 were spent waiting to notice.** Make it shorter and you depose healthy leaders under load; make it longer and every failure costs seconds.

---

### Assessment Reminder

**Project 1 is due Friday at 17:00 — 15% of the course.** **PS 10 is due Friday; PS 11 is released Wednesday.**

**Project 2 is due Friday of the completion period.**

**Labs and quizzes carry no weight** and are still required. **Quiz 11 is Monday and covers Week 10; it is the last quiz** — Weeks 11 and 12 are examined only on the final.

> **Two labs touch this week.** **Lab 10** — your own hypervisor — is sat on the **Tuesday of this
> week**. **Lab 11** covers this week and is sat on the **Tuesday of Week 12**.

Both are tracked in [[_CS 202 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 8's journal** is this week's replicated log, and its idempotent replay is why a repeated message is safe. **Week 4's timeouts** are the same failure detector. **Week 3's locks** are what cannot be used here. **Week 10's virtual machines** are what these replicas usually run on — and a paused guest is indistinguishable from a partition.

**Sideways:** **MATH 251**'s probability is behind the loss sweep: why 20% loss is invisible and 60% is fatal.

**Forward:** **Week 12** asks what an attacker does with a system whose parts must trust each other's messages, and finishes the course.

---

*CS 202 · Week 11 · © CSE Department*
