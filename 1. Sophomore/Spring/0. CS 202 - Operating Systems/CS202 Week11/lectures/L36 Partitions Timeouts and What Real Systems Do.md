# CS 202 · Operating Systems
## Week 11 · Lecture 3 of 3
### Partitions, Timeouts, and What Real Systems Do

*“Thinking doesn't guarantee that we won't make mistakes. But not thinking guarantees that we will.”* — Leslie Lamport, as quoted in *Wired* (2013)

---

**Sat:** Friday of Week 11, 09:00–09:50, VNC 101 · **Reading:** Ongaro & Ousterhout §§6–8; Gilbert & Lynch on CAP · **Next:** Week 12, security and synthesis

**Coursework:** 📋 **Project 1** due today 17:00 · 📝 **PS 10** due today 17:00 · 🔬 **Lab 11** Tue of Week 12 15:00–16:50 · 📝 **PS 12** released Wed of Week 12, due Fri of the completion period 17:00 · 📕 **Final exam** Wed of finals week 09:00–11:30

> **Project 1 is due today at 17:00.**

---

## 1. Split Brain, Measured

**Partition a five-node cluster so that two nodes are on one side and three on the other**, at tick 300, and heal it at 1200:

```
$ ./raftsim -n 5 -seed 3 -ticks 2000 -partition 300:3 -heal 1200
t= 174  node 0 times out and stands for election in term 1
t= 189  node 0 wins term 1 with 3 of 5 votes
t= 300  the network partitions: mask 0x3
t= 486  node 2 times out and stands for election in term 2
t= 491  node 2 wins term 2 with 3 of 5 votes
t=1200  the partition heals
t=1247  node 0 steps down: it saw term 2 while in term 1
```

**Between t=491 and t=1247 there were two leaders**, node 0 in term 1 and node 2 in term 2, **each certain it was the leader** — and neither able to detect the other. **That is split brain, and Raft does not prevent it.**

**What Raft prevents is *both of them committing*.** Node 0 is on the minority side: it can reach one other node, and **an entry needs three of five to commit**. So the old leader can accept requests and never finish any of them, while the majority side makes progress. **When the partition heals, the first message from term 2 deposes node 0**, 47 ticks later.

**The practical reading:** a leader is not something a node *is*; it is something a node **can prove by talking to a majority**, and a leader that cannot reach a majority is already deposed even if nobody has told it.

---

## 2. What Loss Does to Availability

**Raft's failure detector is a timeout**, so a lossy network looks exactly like a failing leader. Five nodes, 5,000 ticks, averaged over five seeds:

| Message loss | Elections started | Leaders elected | **Time without a leader** |
|---:|---:|---:|---:|
| 0% | 1.2 | 1.0 | **3.9%** |
| 10% | 1.8 | 1.2 | 3.9% |
| 20% | 4.0 | 2.8 | 4.8% |
| **40%** | 19.8 | 5.4 | **22.9%** |
| 60% | 54.8 | 4.6 | 60.3% |
| **80%** | **85.6** | **0.4** | **97.7%** |

**Up to 20% loss the cluster barely notices**: heartbeats are frequent, and a lost one costs nothing unless several in a row are lost. **Past 40% it degrades fast**, and at 80% it is **effectively dead** — 85 elections in 5,000 ticks, almost none of which produced a leader, because a candidate needs its requests *and* the replies to survive.

**The shape matters more than the numbers.** The system does not fail gradually: **it works, then it thrashes.** The thrashing is elections, and each election makes the network busier.

---

## 3. The Timeout Is the Whole Design

**There is no way to distinguish a crashed node from a slow one** (L34 §5), so every practical system picks a timeout and lives with both failure modes:

| Timeout too short | Timeout too long |
|---|---|
| a slow leader is deposed unnecessarily | a dead leader is not replaced for that long |
| **elections during load spikes**, exactly when the system is busiest | **outages measured in seconds** |
| measured: at 40% loss, 19.8 elections in 5,000 ticks | measured: a crashed leader cost 232 ticks, 219 of them waiting |

**Real systems expose it and mean it**: etcd's default election timeout is 1,000 ms with 100 ms heartbeats, and its documentation warns that increasing it across a wide-area link is the difference between a working cluster and one that elects constantly.

**And the same trade appeared twice already in this course**: Week 4's hung-task detector waits 120 seconds before declaring a task stuck, and Week 6's `systemd-oomd` waits 20 seconds of sustained pressure. **A failure detector is always a timeout, and the number is always a guess about the tail.**

---

## 4. What Real Systems Are

| System | Algorithm | Used for |
|---|---|---|
| **etcd** | **Raft** | Kubernetes' entire state; leader election, locks, configuration, service discovery |
| **ZooKeeper** | Zab (similar structure, different history) | the same, in the Hadoop/Kafka world |
| **Consul** | Raft | service discovery and health checking |
| **PostgreSQL, MySQL** replication | a leader and followers, **without** automatic consensus by default | durability and read scaling; the failover decision is usually external |

**None of them is installed on these machines:**

```
$ which etcd etcdctl zookeeper-server consul
$
```

**So Lab 11 observes Raft in the simulator instead**, which has one advantage over etcd for teaching: **you can partition it, drop 40% of its messages, and crash its leader on demand** — and read every message it sent.

**What such a service is actually used for is worth stating plainly:** almost nobody writes a consensus protocol. They run three or five copies of one of these and use it as **the one place in the system that can make a decision** — who is the primary, who holds the lock, what the configuration is. **Everything else is built on top and is allowed to be inconsistent.**

---

## 5. The Choice a Partition Forces

**When the network splits, a replicated service can be consistent or available, not both** — which is what CAP says, formally (Gilbert & Lynch, 2002) and narrowly: *during a partition*, a system that answers on both sides can return different answers, and one that refuses on one side is unavailable there.

**Raft chooses consistency.** The minority side refuses writes — measured in §1, node 0 could commit nothing — and its clients see timeouts. **A Dynamo-style store chooses availability**: both sides accept writes, and the divergence is reconciled later, by version vectors and application-specific merges.

**Neither is right; they are different products.** Configuration data, locks and leadership are worthless if two answers exist — so etcd refuses. A shopping cart is worthless if it rejects an "add to cart" — so it accepts, and merges.

**And outside a partition, both can be fast and correct**, which is why the real engineering question is not CAP but **how often you are partitioned and what you do for those seconds.**

---

## 6. Where This Course Already Did This

**Nothing in this week is new; it is the course's own mechanisms across a network:**

| Here | Earlier |
|---|---|
| the **replicated log** | **Week 8's journal**: write it down, then apply it |
| **idempotent replay** after a crash | Week 8 §2: installing a logged block twice writes the same bytes |
| **commit** = a majority has it | Week 8: commit = the header reached the disk |
| **terms** as a logical clock | Week 4's lock ordering: a total order imposed to make reasoning possible |
| **timeouts as failure detection** | Week 4's hung-task detector; Week 6's `systemd-oomd` |
| **quorum instead of a lock** | Week 3's mutex, which needs shared memory and cannot cross a network |

**The last row is the one to remember.** A lock works because every thread can see the same word of memory. **Across machines there is no such word**, so agreement must be manufactured — by counting votes, every time.

---

## 7. What to Take Away

1. **Split brain happens**: two leaders in different terms existed for 756 ticks in the measured run. **Raft prevents both from committing**, not both from existing.
2. **A leader is a node that can reach a majority** — one that cannot is already deposed, and learns it 47 ticks after the partition heals.
3. **Loss degrades the cluster abruptly**: unnoticed to 20%, thrashing at 40%, **97.7% leaderless at 80%.**
4. **The timeout is the design.** Too short elects constantly under load; too long turns a crash into a long outage — measured, 219 of 232 leaderless ticks were waiting.
5. **Real systems are etcd, ZooKeeper and Consul**, used as the one place in a system that can decide; none is installed here, so the simulator stands in — and can be partitioned on demand.
6. **A partition forces a choice**: Raft refuses on the minority side; a Dynamo-style store accepts everywhere and reconciles.
7. **It is all the course's own material at a distance**: logs, idempotent replay, commit points, logical order, and timeouts instead of locks.

---

## Exercises

1. In §1's run, node 0 accepted a client request at t=600. **Trace what the client sees**, and say when — if ever — it learns the outcome.
2. Using §2's table, **at what loss rate would you say the cluster is "down"**, and defend the threshold you chose in terms of what a client experiences.
3. A five-node cluster is split 2 | 2 | 1 by two simultaneous partitions. **What happens?** How long does it last, and what would three nodes have done?
4. etcd uses a 1,000 ms election timeout and 100 ms heartbeats. **Translate the simulator's ticks into those units** and say what §4's crashed-leader outage becomes in seconds.
5. **Name two services in a system you use** that must be linearizable and two that must not be, and say what each would cost if the choice were reversed.

---

*CS 202 · Week 11 · L36 · © CSE Department*
