# CS 202 · Operating Systems
## Week 4 · Lecture 2 of 3
### Preventing Deadlock, and Avoiding It with the Banker's Algorithm

---

**Sat:** Wednesday of Week 4, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 32 §32.3; Silberschatz §8.5–8.6 · **Next:** L15, detection, recovery, livelock — and ignoring the problem

---

## 1. Prevention: Make One Condition Impossible

L13 §2's four conditions are all necessary, so **a system in which any one of them can never hold cannot deadlock.** Each can be attacked, and each attack has a price:

| Condition | Break it by | Cost | Seen in |
|---|---|---|---|
| **Mutual exclusion** | not sharing — per-thread data, or lock-free structures | only works when the data can be split, or the structure redesigned | L10 §7's per-thread counters |
| **Hold and wait** | acquire **everything at once**, or hold nothing while waiting | must know every lock needed in advance; less concurrency | PS 3's `waiter` philosophers |
| **No preemption** | if the second lock is busy, **release the first** and retry | wasted work, and **livelock** | L15 §4 measures it |
| **Circular wait** | **a total order**: every thread acquires locks in the same order | every code path must know the order and obey it | L12 §6's ordered philosophers; Lab 4 |

**In practice, operating systems prevent deadlock almost entirely with the last row.** It costs nothing at run time, needs no knowledge of future requests, and fits how code is written: *take the directory lock before the inode lock*, *take the process-table lock before a process's own lock*.

### Circular wait, made impossible

If every thread takes A before B, a thread holding B can never be waiting for A — **so no cycle can pass through the pair.** In general, number the locks and require every thread to acquire them in increasing order; then along any chain of "waiting for a lock held by", the numbers strictly increase, and a chain of strictly increasing numbers cannot return to where it started. PS 3 Q3(b) asked for exactly this proof for the philosophers.

**When there is no natural order**, programs often use the locks' **addresses**: lock whichever mutex has the lower address first. It is a total order that every thread can compute without coordination.

---

## 2. Checking the Order: `lockdep`

A lock order that lives in comments — L13 §7 read xv6's — is broken the first time someone forgets it. **Linux's kernel has a tool that enforces it**: `lockdep` records, for every pair of lock *classes* ever held together, which was taken first, and **reports a possible deadlock the first time any code path takes them in the opposite order** — even if the deadlock never actually happens on that run.

**It is not in the kernel you are running:**

```
$ grep PROVE_LOCKING /boot/config-$(uname -r)
# CONFIG_PROVE_LOCKING is not set
```

`lockdep` costs memory and time on every lock operation, so distributions build it into debug kernels and leave it out of the ones people run. **The kernel you are using prevents deadlock by its developers' discipline, checked on their debug builds**, not by anything it does at run time.

---

## 3. Avoidance: Never Enter a State That Could Deadlock

**Prevention restricts how programs are written. Avoidance restricts what the system grants**, one request at a time. It needs one thing prevention does not: **each process must declare in advance the most it will ever request** of each resource.

With that, the system can classify every state:

- A state is **safe** if there is **some order** in which every process could run to completion — each one, in turn, obtaining its remaining maximum from what is free plus what the earlier processes release when they finish. That order is a **safe sequence**.
- A state that is not safe is **unsafe**. **Unsafe is not deadlocked**: processes might never ask for their full maximum. But in an unsafe state, a deadlock *can* happen, and the system can no longer prevent it.

**Avoidance grants a request only if the state after granting it would still be safe.** Everything else waits.

---

## 4. The Banker's Algorithm

Dijkstra named it for a banker who never lends out cash in a way that could leave him unable to meet every customer's credit line. For *n* processes and *m* resource types:

| Structure | Shape | Holds |
|---|---|---|
| **Available** | *m* | units of each resource free now |
| **Max** | *n* × *m* | each process's declared maximum claim |
| **Allocation** | *n* × *m* | what each process holds now |
| **Need** | *n* × *m* | **Max − Allocation**: what each process may still ask for |

### The safety check

```
Work   ← Available
Finish ← false for every process
repeat
    find a process i with Finish[i] = false and Need[i] ≤ Work     (every component)
    if there is one:
        Work ← Work + Allocation[i]          i runs to completion and releases everything
        Finish[i] ← true
until no such process exists
the state is safe  ⇔  Finish[i] is true for every i
```

### The request algorithm

When process *i* asks for **Request**:

1. If Request > Need[*i*] — **an error**: it exceeded its declared claim.
2. If Request > Available — **wait**: the units are not free.
3. **Pretend to grant it**: Available −= Request; Allocation[*i*] += Request.
4. **Run the safety check.** If the new state is safe, the grant stands. **If not, undo step 3, and process *i* waits.**

### The textbook example, run

Silberschatz's example: five processes, three resource types with 10, 5 and 7 units in total.

| | Allocation | Max | **Need** |
|---|---|---|---|
| P0 | 0 1 0 | 7 5 3 | **7 4 3** |
| P1 | 2 0 0 | 3 2 2 | **1 2 2** |
| P2 | 3 0 2 | 9 0 2 | **6 0 0** |
| P3 | 2 1 1 | 2 2 2 | **0 1 1** |
| P4 | 0 0 2 | 4 3 3 | **4 3 1** |

**Available = (3, 3, 2).** The course's reference implementation, on that state and three requests:

```
state is SAFE; one safe sequence: <P1, P3, P4, P0, P2>
request P1 (1,0,2): GRANTED
  available now (2,3,0)  state is SAFE; one safe sequence: <P1, P3, P4, P0, P2>
request P4 (3,3,0): WAIT: not available
request P0 (0,2,0): DENIED: would be unsafe
```

**Why P0's small request is refused.** Pretend to grant it: Available becomes (2, 1, 0). Now check every Need against Work = (2, 1, 0):

| | Need | Fits in (2, 1, 0)? |
|---|---|---|
| P0 | 7 2 3 | no |
| P1 | 0 2 0 | **no — needs 2 of the second resource, 1 is free** |
| P2 | 6 0 0 | no |
| P3 | 0 1 1 | **no — needs 1 of the third, none is free** |
| P4 | 4 3 1 | no |

**Nobody can finish, so no safe sequence exists.** Two units of the second resource — which P0 does not even need to complete, since it still needs 7 of the first — would leave the system unable to guarantee anyone's completion. **The banker refuses a loan that is small, available and would very likely be repaid**, because he cannot prove that it would be.

*(The book's own safe sequence is ⟨P1, P3, P4, P2, P0⟩. The program scans in index order and finds ⟨P1, P3, P4, P0, P2⟩. **Safe sequences are not unique**; the state is safe if any exists.)*

---

## 5. What the Check Costs

Each pass scans all *n* processes and compares up to *m* resources for each, and there can be *n* passes: **O(*n*² *m*)** per request. Measured with a state built so that every pass finds exactly one process and every comparison scans all *m* resources:

| Processes *n* | *m* = 4 | *m* = 32 |
|---:|---:|---:|
| 100 | 0.018 ms | 0.066 ms |
| 200 | 0.071 ms | 0.257 ms |
| 400 | 0.278 ms | 1.102 ms |
| 800 | 1.093 ms | 4.356 ms |
| 1,600 | 4.615 ms | 17.398 ms |
| 3,200 | **20.590 ms** | **74.690 ms** |

**Doubling *n* multiplies the cost by four**, as *n*² predicts. **Multiplying *m* by eight multiplies it by about 3.6** at *n* = 3,200 — less than eight, because the per-process bookkeeping does not grow with *m*. **At 3,200 processes a single request costs 21–75 ms.** L01 counted 351 processes and 1,425 threads on an idle desktop, each taking locks thousands of times a second.

---

## 6. How Conservative It Is

`banksim.c` generates random workloads — six processes, three resource types with six units each, random maximum claims — in which processes ask for one unit at a time and release everything when their claim is met. **Ten thousand runs, each policy:**

| Policy | Runs deadlocked | Refused although the unit was free |
|---|---:|---:|
| **grant whenever free** | **4,227 of 10,000 — 42.3%** | — |
| **Banker's algorithm** | **0** | **6.5 grants per run** |

**The Banker never deadlocked, and paid for it** by refusing, on average, 6.5 grants per run that were possible at that moment. Some of those refusals prevented deadlocks; others refused requests that would have been fine, because **an unsafe state is not a deadlock** — the algorithm cannot know which future requests will actually arrive.

---

## 7. Why General-Purpose Systems Do Not Use It

| Needs | A general-purpose OS has |
|---|---|
| **every process's maximum claim, declared in advance** | programs that do not know how many locks, files or pages they will want |
| **a fixed set of resource types counted in units** | locks, which are one-of-a-kind, created and destroyed constantly |
| **a fixed set of processes** | 351 processes arriving and leaving |
| **O(*n*²*m*) on every request** | lock operations measured in nanoseconds (L11 §1) |

**Avoidance is used where those assumptions hold** — systems that allocate a small number of large, countable resources to a known set of jobs, and can make a job wait. **A kernel's locks are the opposite case**, which is why kernels prevent deadlock by ordering (§1), and why, for the remaining risk, **L15's answer is often to detect it, or to accept it.**

---

## 8. What to Take Away

1. **Prevention breaks one of the four conditions.** Kernels overwhelmingly break **circular wait**, with a total lock order.
2. **A lock order in a comment is unchecked.** Linux's `lockdep` checks it, and is not built into this kernel.
3. **Avoidance needs maximum claims in advance**, and grants only requests that leave the state **safe**. **Unsafe is not deadlocked.**
4. **The Banker's algorithm** reproduces the textbook: P1's request granted, P4 told to wait, **P0's small request refused as unsafe**.
5. **The safety check is O(*n*²*m*)**: 20.6 ms for 3,200 processes and 4 resources, 74.7 ms with 32.
6. **It is conservative**: random workloads deadlocked 42.3% of the time under naive granting and never under the Banker — at the cost of 6.5 refused-but-free grants per run.
7. **General-purpose kernels do not use avoidance**, because they cannot know claims in advance and cannot afford the check.

---

## Exercises

1. In the textbook state after P1's grant, find **every** safe sequence. How many are there?
2. P3's Need is (0, 1, 1). Could P3 ever be the last process in a safe sequence of the original state? Argue from Work.
3. Modify the safety check to stop as soon as all processes are finished, and to restart the scan from process 0 after each success. Does its worst case change? Its average?
4. Give a state that is unsafe, and a sequence of future requests and releases from it in which **no deadlock ever occurs**.
5. Lock ordering by address is a total order. **Construct a program in which ordering by address still deadlocks** because a lock is freed and a new one allocated at a lower address while a thread holds a third lock.

---

*CS 202 · Week 4 · L14 · © CSE Department*
