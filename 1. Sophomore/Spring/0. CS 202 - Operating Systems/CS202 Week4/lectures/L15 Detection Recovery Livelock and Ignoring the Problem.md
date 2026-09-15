# CS 202 · Operating Systems
## Week 4 · Lecture 3 of 3
### Detection, Recovery, Livelock — and Ignoring the Problem

---

**Sat:** Friday of Week 4, 09:00–09:50, VNC 101 · **Reading:** Silberschatz §8.7–8.8; OSTEP Ch. 32 §32.3 on livelock · **Next:** Week 5, memory management

---

## 1. Detection: Let It Happen, Then Find It

Prevention constrains how code is written; avoidance needs claims no program can state. **The third option is to grant requests freely and look for deadlocks afterwards.**

**With one instance of each resource** — every mutex — detection is L13 §3's observation: **build the wait-for graph and look for a cycle.** A depth-first search finds one in time linear in the number of threads and edges. L13 built that graph by hand from `/proc` and from `gdb`.

**With several instances**, a cycle is not proof (L13 §3). The detection algorithm is the Banker's safety check with one substitution: **use each process's current *request*, not its maximum remaining *need***.

```
Work ← Available
Finish[i] ← true if process i holds nothing, else false
repeat
    find i with Finish[i] = false and Request[i] ≤ Work
    if found: Work ← Work + Allocation[i];  Finish[i] ← true
until none found
the processes with Finish[i] = false are deadlocked
```

**The two differences from the safety check, and why:**

| | Banker's safety check | Detection |
|---|---|---|
| Compares against | **Need** = Max − Allocation: everything it *might* ask for | **Request**: what it *is* asking for now |
| A process holding nothing | treated like any other | **finished from the start** — it cannot be part of a cycle |
| Answers | *could* this deadlock, in the worst case? | **has** this deadlocked, right now? |

**The optimism is deliberate.** Detection assumes a process whose current request can be met will finish and release everything. If it later asks for more and blocks, the next run of the detector will see it.

### The textbook example, run

Silberschatz's detection example: five processes, resources with 7, 2 and 6 units, **Available = (0, 0, 0)**.

| | Allocation | Request |
|---|---|---|
| P0 | 0 1 0 | 0 0 0 |
| P1 | 2 0 0 | 2 0 2 |
| P2 | 3 0 3 | 0 0 0 |
| P3 | 2 1 1 | 1 0 0 |
| P4 | 0 0 2 | 0 0 2 |

```
$ ./detect < textbook_detect.txt
no deadlock; the processes can finish in the order <P0, P2, P3, P4, P1>
```

**Nothing is free, and yet nothing is deadlocked**: P0 and P2 are waiting for nothing, will finish, and release enough for the rest. Now let **P2 ask for one more unit of the third resource** — Request becomes (0, 0, 1):

```
$ ./detect < textbook_detect_more.txt
DEADLOCKED: P1 P2 P3 P4
```

**One extra unit requested, and four processes are deadlocked.** P0 still finishes, but releases only (0, 1, 0), and none of the other four requests fits in that.

---

## 2. When to Look, and What to Do

**How often to run the detector** is a trade:

| Run it | Cost | Benefit |
|---|---|---|
| on every request that has to wait | a detection pass per blocked request | the deadlock is found the moment it forms, and the request that closed the cycle is known |
| periodically, or when utilisation drops | little | a deadlock may sit for a while; many processes may be involved by then |

**Recovery** means breaking the cycle, and every method loses something:

- **Kill a process** in the cycle — one at a time, rerunning detection, or all of them. **Its work is lost**; choose the victim by how much it has done, how much it holds, or how cheaply it restarts.
- **Preempt a resource** — take it from its holder and give it to someone else. **The holder must be rolled back** to a state before it held the resource, which is only possible if something recorded that state.

**Databases are the system that does this routinely.** Transactions lock rows, lock orders cannot be imposed across arbitrary queries, and **a transaction can be rolled back by design**. So a database manager checks for a cycle among waiting transactions — PostgreSQL does it after a transaction has waited for a configurable second — and **aborts one**, reporting a deadlock to the client, which retries. **Recovery is cheap exactly where rollback already exists.**

---

## 3. What Linux Does About a User-Space Deadlock: Nothing

**L13's `abba` threads would sleep forever.** Nothing in the kernel noticed them, and nothing will.

Linux does have a **hung-task detector**, and it is switched on:

```
$ grep DETECT_HUNG_TASK /boot/config-$(uname -r)
CONFIG_DETECT_HUNG_TASK=y
$ cat /proc/sys/kernel/hung_task_timeout_secs
120
```

**It reports tasks stuck in uninterruptible sleep — state `D` — for more than 120 seconds**, because a task stuck in `D` usually means a kernel or driver problem. **`abba`'s threads are in state `S`**, interruptible sleep in a futex wait (L13 §4), which is what every idle program looks like. **A user-space deadlock is indistinguishable, to the kernel, from a program waiting for something that has not happened yet.**

**This is the ostrich algorithm**, named for the bird that — in the story — buries its head: **ignore deadlocks, and restart the program when a person notices.** It is what every general-purpose OS does for user programs, and for good reason: deadlocks are rare relative to the cost of preventing them for everyone; detection needs information about locks that user-space libraries keep to themselves; and a human deciding to restart a hung program is usually the right recovery.

---

## 4. Livelock, Measured

L14 §1's third row — **break "no preemption" by releasing and retrying** — avoids deadlock and creates a different failure. `livelock.c` has two threads that each need locks A and B, taking them in opposite orders but **never waiting for the second**: take the first, *try* the second, and if it is busy, release the first and start again.

| Retry strategy | Two CPUs: rounds per second | failed attempts per round | One CPU: rounds per second | failed attempts per round |
|---|---:|---:|---:|---:|
| **polite** — retry at once | **128,579** | **32.21** | **50,322** | **53.92** |
| `sched_yield()` before retrying | 981,142 | 0.54 | 1,404,338 | 0.00 |
| **random sleep, 0–99 µs** | **1,310,491** | 0.01 | 1,314,593 | 0.01 |
| *ordered* — both take A then B, blocking | 867,137 | 0 | 1,424,131 | 0 |

**The polite threads never deadlocked, and did roughly a tenth of the useful work** — on two CPUs, 32 attempts failed for every one that succeeded. Both threads are **running**, both CPUs are busy, and **most of what they do is taking a lock, failing to get the second, and giving the first back** — in step with each other, so that each one's retry collides with the other's. **That is livelock**: activity without progress. It is worse on one CPU, where each thread's failures happen while the other has been preempted holding its first lock.

**Two fixes, both breaking the symmetry:**

- **Random back-off.** A thread that fails waits a random interval before trying again, so the two stop colliding. **On two CPUs it did better than ordered blocking** — 1.31 million rounds per second against 0.87 million — because a thread that sleeps briefly avoids both the collision and the futex sleep-and-wake that blocking needs. **This is Ethernet's answer to collisions**, and for the same reason.
- **Ordering.** No trying, no failing: the deadlock is prevented, so there is nothing to back off from. It is the simplest correct answer and, on one CPU, the fastest.

**`sched_yield()` helps a lot on one CPU and less on two**, because on one CPU yielding lets the other thread run to completion and release its lock, while on two the other thread is already running.

---

## 5. Three Failures, One Table

| | Deadlock | Livelock | Starvation |
|---|---|---|---|
| **Threads are** | asleep | running | mostly running; one is not |
| **CPU** | idle | busy | busy |
| **Progress** | none | little or none | everyone but the victim |
| **`/proc` state** | `S`, `wchan` in futex | `R` | `R` / `S` mixed |
| **Measured this term** | `abba`: every run | polite retry: 32 failures per success | L12 §7's writer: 0 acquisitions in 4 s |
| **Cure** | order, avoid, or detect and recover | randomise, or order | fairness |

---

## 6. Help from the Library: Mutexes That Notice

POSIX mutexes have types, and two of them turn a silent hang into an error the program can see. `errchk.c`:

```
default mutex, locked twice by one thread:        ETIMEDOUT (after waiting 1 s)
error-checking mutex, locked twice by one thread: EDEADLK (at once)
robust mutex, owner exited while holding it:      EOWNERDEAD
  after pthread_mutex_consistent and unlock, lock returns 0
```

| Type | Problem it catches | What happens |
|---|---|---|
| default | none | **a thread that locks a mutex it already holds sleeps forever** — here, until a 1 s timeout |
| **`PTHREAD_MUTEX_ERRORCHECK`** | **self-deadlock** | the second `lock` returns **`EDEADLK`** immediately |
| **`PTHREAD_MUTEX_ROBUST`** | **the holder died** | the next `lock` returns **`EOWNERDEAD`**; the new holder must repair the protected data and call `pthread_mutex_consistent` |

**Neither detects a cycle between two threads.** Error-checking catches the one-thread case — **exactly what xv6's `acquire` panics on** (L13 §7) — and robust mutexes catch a holder that can never release. **Both are cheap because each needs only information the mutex already has**: its own owner. A two-lock cycle needs information about other locks, which no single mutex holds.

---

## 7. What to Take Away

1. **Detection with single-instance resources is a cycle search** in the wait-for graph.
2. **With several instances, run the safety check on current requests**: the textbook state is not deadlocked with nothing available, and **one extra unit requested by P2 deadlocks four processes.**
3. **Recovery kills or rolls back**, and is cheap only where rollback already exists — which is why databases detect deadlocks and kernels do not.
4. **Linux ignores user-space deadlocks.** Its hung-task detector watches only state `D`, and deadlocked threads sleep in `S`.
5. **Release-and-retry trades deadlock for livelock**: polite retry did a tenth of the work, with 32 failures per success. **Random back-off fixed it**, and beat blocking on two CPUs.
6. **Error-checking and robust mutexes detect the cases a single mutex can see** — a thread relocking, a holder that died — and no more.

---

## Exercises

1. Draw the resource-allocation graph for `textbook_detect_more.txt`. Does it contain a cycle? Does every process in the cycle appear in the detector's output?
2. The detector marks processes holding nothing as finished before scanning. **Construct a state in which omitting that step reports a process as deadlocked that is not.**
3. In `livelock.c`, replace the random sleep with a **fixed** 50 µs sleep. Predict the result, then measure it. Why does randomness matter?
4. Exponential back-off doubles the maximum random delay after each consecutive failure. What does it buy over a fixed range, and what does it cost when contention is light?
5. Would an error-checking mutex have caught `abba.c`'s deadlock? Would a robust one? For each, say exactly what information it would need that it does not have.

---

*CS 202 · Week 4 · L15 · © CSE Department*
