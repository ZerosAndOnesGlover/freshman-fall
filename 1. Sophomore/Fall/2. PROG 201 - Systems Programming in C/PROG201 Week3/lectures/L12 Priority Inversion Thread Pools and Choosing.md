# PROG 201 · Systems Programming in C
## Week 3 · Lecture 3 of 3
### Priority Inversion, Thread Pools, and Choosing

*“In software systems, it is often the early bird that makes the worm.”* — Alan Perlis, "Epigrams on Programming" (1982), #43

---

**Reading:** APUE §11.6.5 · TLPI §35.3 · `man 7 sched`, `man 3 pthread_mutexattr_setprotocol` · **Previous:** L11 · **Next:** Lab 3 — reproduce the inversion, on the Monday of Week 4

**Coursework:** 📝 **PS 2** due Fri this week 17:00 · 🔬 **Lab 3** Mon of Week 4 15:00–16:50 · 📊 **Quiz 4** Tue of Week 4 · 📝 **PS 4** released Wed of Week 4, due Fri of Week 5 17:00

---

## 1. Priority Inversion

Three threads and one mutex.

- **L**, low priority, takes the mutex and starts a long piece of work.
- **H**, high priority, wants the mutex and blocks. This is correct and expected: H waits for L's critical section, and that is the price of sharing.
- **M**, medium priority, wants nothing at all. It just runs.

M preempts L, because M has the higher priority. L, holding the mutex, gets no CPU. H, which outranks M, waits — **behind a thread it outranks, through a thread it does not.** H's wait is now bounded not by the length of L's critical section but by however long M feels like running, which may be forever.

That is priority inversion, and it is not a hypothetical. In July 1997 the **Mars Pathfinder** lander began resetting itself on the Martian surface: a low-priority meteorological task held a mutex on the information bus, a medium-priority communications task preempted it, and the high-priority bus management task missed its deadline. The watchdog rebooted the spacecraft. The fix — enabling priority inheritance on that mutex — was uploaded from Earth to Mars and worked. It is the most famous concurrency bug ever shipped, and the code was correct: every lock was taken, every lock was released, and the system still failed.

**The lesson is the one to carry out of this course:** correctness of a concurrent program is not the same property as its timing behaviour, and a program can be provably free of races and still miss every deadline it has.

---

## 2. It Is Not Subtle

`inversion.c` pins three kinds of thread to **one CPU** and gives L a fixed amount of *work* to do inside the lock — not a fixed amount of time, which is the detail that makes the effect visible. L runs at nice 19; M and H run at nice 0.

```
no burners, L at nice 19, 1 chunk                high waited    0.489 s
3 burners, L at nice 19, 1 chunk                 high waited  100.607 s
```

**A half-second critical section became a hundred-second wait.** Two hundred and six times, on an ordinary desktop with ordinary threads. The baseline is tight across runs — 0.489, 0.495, 0.488 — so the ratio is not an artefact of a noisy denominator.

The arithmetic is exact and worth doing. Linux's CFS gives each thread a share of the CPU proportional to a weight derived from its nice value: nice 0 weighs 1,024 and nice 19 weighs 15. With three nice-0 burners and one nice-19 lock-holder on one CPU, L receives

$$\frac{15}{15 + 3 \times 1024} = 0.49\%$$

of the CPU, so 0.49 s of work takes 0.49 / 0.0049 ≈ **100 s**. The measurement and the scheduler's weight table agree to two significant figures.

**Note what H's priority bought it: nothing.** H is nice 0, the same as the burners, and it spends the entire 100 seconds asleep on a futex. Its priority cannot help it, because it is not competing for the CPU — it is waiting for a lock, and the lock's holder is the one being starved.

---

## 3. The Fix That Does Not Work Here

The textbook answer is **priority inheritance**: while H is blocked on a mutex held by L, L temporarily runs at H's priority, so M cannot preempt it. POSIX exposes it as a mutex attribute:

```c
pthread_mutexattr_t a;
pthread_mutexattr_init(&a);
pthread_mutexattr_setprotocol(&a, PTHREAD_PRIO_INHERIT);
pthread_mutex_init(&lock, &a);
```

Add exactly that to `inversion.c` and measure:

```
3 burners, L at nice 19, 1 chunk                 high waited  100.607 s
3 burners + PRIO_INHERIT, L at nice 19, 1 chunk  high waited  100.392 s
```

**No effect whatsoever.** And nothing failed to tell you so — `rtcheck.c` confirms every call succeeds:

```
pthread_mutexattr_setprotocol(PRIO_INHERIT) -> 0
pthread_mutex_init with PI attr             -> 0
protocol reads back as 1 (PRIO_NONE=0 PRIO_INHERIT=1 PRIO_PROTECT=2)
```

The attribute was set. The mutex was created. The protocol reads back as `PRIO_INHERIT`. And it does nothing, for a reason that is not in the man page's first screen:

> **Priority inheritance boosts a thread's realtime priority. A `SCHED_OTHER` thread has none.**

Linux implements PI in the kernel's `rt_mutex`, which reorders a wait list by realtime priority. A `SCHED_OTHER` thread's nice value is not a realtime priority; there is nothing for the protocol to inherit, so the boost is a no-op. To get a realtime priority you need `SCHED_FIFO` or `SCHED_RR`, and:

```
RLIMIT_RTPRIO: soft=0 hard=0
sched_setscheduler(SCHED_FIFO, 10) -> -1, errno=Operation not permitted
```

**On these machines you cannot.** `RLIMIT_RTPRIO` is 0, so realtime scheduling is refused, so priority inheritance has nothing to work with. *(The machine does grant it to some users — `/etc/security/limits.d/25-pw-rlimits.conf` gives the `pipewire` group `rtprio 95`, because audio has deadlines. The mechanism exists; you are not in the group.)*

**This is the most important thing in the lecture.** A correctness feature that is silently inert is worse than one that is absent, because you will write the four lines, see no error, and believe you are protected. Lab 3 is built around making you check.

---

## 4. The Fixes That Do Work

Three, and all three are available to an unprivileged program. Three runs of each, because two of them are not stable and that is part of the answer:

| configuration | H waited | |
| --- | --- | --- |
| **the bug** — 3 burners, nice 19, 1 chunk | **100.607 s** | |
| the documented fix — `PRIO_INHERIT` | 100.392 s | **1.0×** |
| 3 burners, **nice 0**, 1 chunk | 1.946 / 1.947 / 1.941 s | 52× |
| 3 burners, nice 19, **100 chunks** | 0.534 / 0.487 / 0.899 s | ~170× |
| 3 burners, nice 19, **1000 chunks** | 0.403 / 0.261 / 1.681 s | ~200× |
| 3 burners, nice 0, 100 chunks | 0.012 / 0.012 / 0.015 s | ~7,500× |
| *(no burners at all, for reference)* | 0.489 / 0.495 / 0.488 s | |

**(a) Do not mix priorities around a shared lock.** Putting L at the same nice level as the burners takes the wait from 100 s to 1.94 s, and it is the most *reproducible* row in the table — three runs within 6 ms of each other. The inversion is caused by the priority gap; closing the gap removes it. In practice: a thread that holds a lock a latency-sensitive thread needs must not be deprioritised, however cheap its own work looks.

**(b) Shrink the critical section.** A hundred short critical sections instead of one long one takes the wait to about half a second **without touching a single priority** — back to what it was with no burners at all.

But look at the spread: 0.487 to 0.899 at 100 chunks, and 0.261 to 1.681 at 1,000. **The chunked fix is variable and the equal-priority fix is not**, and the reason is worth understanding rather than averaging away. With a chunked critical section H is no longer waiting for one long hold; it is *racing* for a lock that is free most of the time, and whether it wins on the first gap or the fiftieth is up to the scheduler. The inversion is gone — three orders of magnitude — and what replaces it is ordinary contention with ordinary variance.

Note also that the fastest chunked runs are **below the 0.49 s baseline**, which is not a mistake: H needs the lock once, and with the lock released a thousand times it can get in at a gap instead of waiting out a whole critical section.

**This is still the general fix and the one to reach for.** The bound on H's wait is the *length of the critical section*, not the priorities involved. Priority inheritance bounds the damage; a short critical section prevents it.

**(c) Both.** 0.012 s, and stable. Nothing surprising, but worth having in the table so the two effects can be seen not to conflict.

And the fix that is *not* on this list: making H higher priority. H is already blocked on a futex, not competing for CPU. **You cannot schedule your way out of a lock you are waiting for.**

---

## 5. Thread Pools

L10 measured `pthread_create` + `join` at 29 µs. If a task takes less than that, you spend more time making the worker than doing the work — and this is the normal case for a server, where a "task" is parsing one request.

A **thread pool** creates the workers once and feeds them through a queue. It is L11 §7's bounded buffer with function pointers in the slots. `pool.c`, 100,000 tasks, four workers:

| work per task | thread-per-task | pool | speedup |
| --- | --- | --- | --- |
| 0 units | 35,529 tasks/s | **1,620,449 tasks/s** | **45.6×** |
| 100 units | 35,721 tasks/s | 1,271,398 tasks/s | 35.6× |
| 10,000 units | 20,518 tasks/s | 150,009 tasks/s | 7.3× |

35,529 tasks/s is 28.1 µs per task, which is L10's 29.21 µs measurement arriving from a different direction. **The thread-per-task row barely moves when the task gets 100× more expensive**, because the task was never the cost.

And the ratio falls as the work grows — 45.6× to 7.3× — which is the same shape as Week 2 L09 §6's crossover table, for the same reason: **a fixed per-item overhead amortises.** You have now measured that principle three times in three weeks. It is most of what performance work is.

### How many workers?

The obvious answer is "as many as possible". `pool.c` with 10,000 units of work per task:

| workers | tasks/s |
| --- | --- |
| 1 | 57,141 |
| 2 | 91,682 |
| **4** | **166,952** |
| 8 | 96,045 |
| 16 | 95,720 |

**Four is the peak, and eight is 42% worse than four.** This machine has four physical cores and eight hardware threads; past four, the workers are contending for the same execution resources and for the queue's mutex, and the pool spends its time in `futex` rather than in tasks.

Now the same sweep with **no work per task**, so the only thing being measured is the queue:

| workers | tasks/s |
| --- | --- |
| 1 | 4,104,725 |
| 2 | 2,372,114 |
| 4 | 1,263,415 |
| 8 | 805,352 |

**Throughput falls monotonically.** One worker is five times faster than eight, because with trivial tasks the pool is not a parallelism mechanism, it is a lock benchmark — and a lock gets slower the more threads are hitting it.

Two rules from those two tables:

1. **Size the pool to the cores, not to the tasks.** `sysconf(_SC_NPROCESSORS_ONLN)` for CPU-bound work. For I/O-bound work the right number is higher and has to be measured, because a blocked worker is not using a core.
2. **If the tasks are tiny, do not use a pool.** Batch them until they are not.

---

## 6. False Sharing: A Performance Bug With No Bug In It

Four threads, four counters, **no shared variable, no lock, no race**. `falseshare.c` varies only the distance in memory between the counters:

```
cache line is 64 bytes = 8 longs
  stride      bytes    seconds    vs best
       1          8     0.1255      1.55x
       2         16     0.1253      1.55x
       4         32     0.1193      1.47x
       8         64     0.0809      1.00x
      16        128     0.0814      1.01x
```

The step is at **exactly 64 bytes**, which is the cache line. Below it the four counters share a line; every increment by any thread invalidates the line in the other three cores' caches, and the line ping-pongs between them. Above it each counter has its own line and the threads never speak.

**The program is correct in every configuration and 55% slower in three of them**, for a reason that appears nowhere in the source. This is where CS 201's cache hierarchy and this course meet, and it is the answer to "why is my parallel version not faster".

The fix is padding or `alignas`:

```c
struct counter { _Alignas(64) long value; };     /* C11 */
struct counter counters[THREADS];
```

Find `_SC_LEVEL1_DCACHE_LINESIZE` with `sysconf` rather than assuming 64, and note that **this is exactly the wrong optimisation to make first**: it costs memory, it is invisible in the source, and it matters only for variables that several threads write frequently. Measure, then pad.

---

## 7. Pthreads and C11 Threads

C11 added `<threads.h>`: `thrd_create`, `mtx_lock`, `cnd_wait`, `tss_get`. It is a smaller, cleaner API covering perhaps 80% of what pthreads does.

```
$ ./c11
<threads.h> present
thrd_create/thrd_join work; thread returned 42
```

It works here, on glibc 2.39, and **it works without `-pthread`** — since glibc 2.34 the threading implementation lives in `libc` itself, so the old `-lpthread` is a no-op kept for compatibility. *(The Makefiles in this course still pass it. It costs nothing and it works on older systems.)*

Use pthreads anyway, for this course and for most work:

| | pthreads | C11 threads |
| --- | --- | --- |
| Availability | everywhere POSIX exists | glibc ≥ 2.28; **absent on Windows/MSVC and optional in the standard** |
| Reader-writer locks | yes | **no** |
| Barriers, spinlocks | yes | no |
| Thread attributes (stack size, detach state, affinity) | yes | **no** |
| Priority inheritance | yes (§3) | no |
| Cancellation | yes | no |
| Error reporting | returns the error number | returns `thrd_success` / `thrd_error` — **you cannot tell why** |

`__STDC_NO_THREADS__` exists precisely because an implementation is allowed to skip the whole header. **A C11 threads program is portable to fewer places than a pthreads program**, which is an unusual thing to be able to say about a standard feature, and it is why the ecosystem never moved.

---

## 8. Choosing: Threads or Processes

Week 2 chose between IPC mechanisms. This is the choice one level up, and Weeks 0–3 have now measured everything in the table.

| Consideration | Threads | Processes |
| --- | --- | --- |
| Creation | **29 µs** | 164 µs |
| Sharing | everything, immediately | needs a mechanism (Week 2) |
| Isolation | **none** — one bad pointer takes down all of it | a fault kills one worker |
| A crash | the whole process dies | `waitpid` tells you and you restart it (Lab 0) |
| Debugging | every bug is a timing bug | one flow of control at a time |
| Per-worker memory | a stack, faulted in as used | a full address space, COW |
| Ceiling here | **7,671** (cgroup `pids.max`) | the same limit |
| Different programs | impossible | `exec` |

**The deciding question is almost never performance.** It is: *if one worker corrupts memory, should the others die?* For a browser rendering an untrusted page, the answer is no, and Chrome uses processes. For a web server's request handlers, all running your code over shared state, the answer is that they might as well, and nginx uses both — processes for isolation between workers, and an event loop inside each.

**And the third answer, which Week 5 arrives at: neither.** A single thread with `epoll` handles ten thousand connections with no synchronisation at all, because there is nothing concurrent to synchronise. Most of the difficulty of this week disappears if you can arrange not to need it.

---

## Summary

- **Priority inversion**: a high-priority thread blocked on a lock held by a low-priority thread that a medium-priority thread is preempting. Measured: **0.489 s → 100.607 s, a factor of 206**, and the CFS weight arithmetic predicts it.
- **`PTHREAD_PRIO_INHERIT` initialises without error and does nothing** for `SCHED_OTHER` threads, because there is no realtime priority to inherit — and `RLIMIT_RTPRIO` is 0 here, so you cannot get one.
- The fixes that work: **equalise the priorities** (1.94 s, and stable to 6 ms) and **shrink the critical section** (~0.5 s at 100 chunks, but varying from 0.26 s to 1.7 s, because H now races for the lock instead of waiting for it).
- **A thread pool beats thread-per-task by 45.6× on empty tasks and 7.3× on expensive ones.** The ratio falls as the work grows, because a fixed overhead amortises — the third time this term.
- **Size the pool to the cores**: 4 workers gave 166,952 tasks/s and 8 gave 96,045. With trivial tasks, throughput *falls* with every worker added.
- **False sharing**: four private counters within one 64-byte line ran **1.55× slower** than the same program with them apart. Correct code, invisible cause.
- C11 `<threads.h>` works on glibc 2.39 with no `-pthread`, and is **less portable** than pthreads and missing rwlocks, attributes, barriers and useful errors.
- Threads or processes is a question about **isolation**, not speed.

---

## Exercises

1. Run `inversion.c` with one burner, two, and four. Predict each wait from the CFS weight formula in §2 before you run it.
2. Give H a `pthread_mutex_timedlock` with a 1-second timeout. What should it do when the timeout fires? Write the three options down and argue for one.
3. Reproduce §4(b) with 10, 100 and 1,000 chunks, **five runs each**, and plot the spread rather than the mean. Where does the variance come from, and what does it imply about how short "short enough" is?
4. Add work to `pool.c`'s tasks until the 8-worker row beats the 4-worker row. How much work does it take, and why does that threshold exist?
5. Make the pool's tasks block on a `read` from a pipe instead of burning CPU. Now re-run the worker sweep. Where is the peak, and why is it not 4?
6. Pad `falseshare.c`'s counters with `_Alignas(64)` and confirm the 1.55× disappears. Then find `_SC_LEVEL1_DCACHE_LINESIZE` on your machine and check it is 64.
7. Rewrite `pool.c`'s queue using C11 `<threads.h>`. Which pthreads feature do you miss first?

---

*PROG 201 · Week 3 · L12 · © CSE Department*
