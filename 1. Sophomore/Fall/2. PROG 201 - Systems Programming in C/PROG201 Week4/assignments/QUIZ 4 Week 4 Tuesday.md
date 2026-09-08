# PROG 201 · Quiz 4
## Administered: Tuesday, Week 4 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 3** — threads, mutexes and condition variables, reader-writer locks, priority inversion, thread pools.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.
>
> **Midterm 1 was yesterday evening** and covered Weeks 0–3. This quiz is the same material one
> more time; use it to check what the paper found, before the marks come back.

---

**Q1.** Two threads in one process. Name three things they share and three things they do not.

&nbsp;

&nbsp;

---

**Q2.** A worker thread calls `close(-1)`, which fails. Another thread checks `errno` a moment later and finds 0. Is that a bug? Explain.

&nbsp;

&nbsp;

---

**Q3.** You need 6,000 threads and `pthread_create` returns `EAGAIN` at about 7,600. A colleague suggests reducing the stack size from 8 MiB to 64 KiB. Will it help? Where would you look instead?

&nbsp;

&nbsp;

---

**Q4.** Write the correct shape of a consumer waiting on a condition variable — four lines. Then say what breaks if the `while` is an `if`, and give a number.

&nbsp;

&nbsp;

&nbsp;

---

**Q5.** A bounded buffer uses **one** condition variable for both "not full" and "not empty", with `pthread_cond_signal`. What happens, and why does `broadcast` make the symptom go away without fixing anything?

&nbsp;

&nbsp;

---

**Q6.** A high-priority thread waits 100 seconds for a critical section that takes half a second. Name the phenomenon, and say why raising the waiting thread's priority does not help.

&nbsp;

&nbsp;

---

**Q7.** Your thread pool gets 167,000 tasks/s with 4 workers and 96,000 with 8, on a machine with 4 cores and 8 hardware threads. Explain both numbers.

&nbsp;

&nbsp;

---
---

# Answer Key

*Mark your own. Be honest — nobody else will see this.*

---

**Q1.** **Shared:** the address space (globals, heap, code), the descriptor table and the file offsets behind it, signal *dispositions*, the current directory, the PID. **Private:** the stack, the registers, `errno`, the signal *mask*, the thread ID, the nice value, anything `_Thread_local`. *(L10 §2. Any three of each.)*

---

**Q2.** **Not a bug — `errno` is per-thread**, and it has to be, or one thread's failed call would overwrite another's pending error and no library function could be trusted. On Linux `errno` is a macro expanding to `(*__errno_location())`, which is thread-local. The corollary: never test `errno` without a failing call *in this thread* immediately before. *(L10 §2.)*

---

**Q3.** **It will not help.** Measured: 7,643 threads with 8 MiB stacks and 7,644 with 64 KiB — one extra thread for a 128× reduction. The stack is *address space*, and this machine has 47 bits of it.

Look at the **task count limits**, in this order: the cgroup's `pids.max` (**7,671** here, and the binding one), then `RLIMIT_NPROC` (`ulimit -u`, 25,571), then `/proc/sys/kernel/threads-max`. The advice about stack sizes is about 32-bit address space and is thirty years out of date. *(L10 §3.)*

---

**Q4.**

```c
pthread_mutex_lock(&m);
while (queue_is_empty())            /* while, never if */
    pthread_cond_wait(&cv, &m);
take_one();
pthread_mutex_unlock(&m);
```

With an `if`, the thread proceeds on a false predicate. Measured: **7.12% of wakeups arrived with nothing to do** — stolen wakeups (another consumer took the item first) plus genuinely spurious ones, which POSIX permits. That is more than one in fourteen, not a rounding error. *(L11 §3–§4.)*

---

**Q5.** It **deadlocks**. `signal` wakes exactly one waiter and the implementation neither knows nor cares which predicate that waiter is testing, so a consumer's "there is room now" can be delivered to another consumer, who finds the buffer empty and sleeps again. Measured: the `signal` version wedges; the `broadcast` version completes 80,000 items.

`broadcast` wakes everybody, so the right thread is always among them — but the bug is **one condition variable standing for two predicates**, every wakeup is now *O(waiters)*, and adding a third predicate brings the hang back. Two predicates need two condition variables. *(L11 §5.)*

---

**Q6.** **Priority inversion**: the lock's holder is low priority and a medium-priority thread is preempting it, so the high-priority thread waits behind a thread it outranks, through one it does not. Measured 0.489 s → **100.607 s**.

Raising the waiter's priority does nothing because **it is not runnable** — it is asleep on a futex, taking no part in any scheduling decision. Priority decides who runs among the runnable; the problem is that the thread it is waiting for is not among them. *(L12 §1–§2.)*

---

**Q7.** **4 is the physical core count**, and with CPU-bound tasks that is the peak: four workers keep four cores busy. **8 is the hardware thread count**, and the extra four workers do not get extra execution resources — they add contention for the same cores and for the pool's single queue mutex, so throughput falls 42%.

The general rule: size a pool for CPU-bound work to `sysconf(_SC_NPROCESSORS_ONLN)` and then *measure*, because the useful number is the cores, not the hyperthreads. For I/O-bound work it is higher and must be measured. *(L12 §5.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L10 §2 |
| Q3 | L10 §3 |
| **Q4, Q5** | **L11 §3–§5** — and PS 3 Q4 is these two as code |
| **Q6** | **L12 §1–§3** — you sat Lab 3 yesterday afternoon; check your answers against it |
| Q7 | L12 §5 |

**Q4 and Q5 are the ones that recur.** PS 3's thread pool is a bounded buffer, Week 5's server hands connections to workers through one, and Project 2 is built on it. If either was shaky, fix it before you start the problem set rather than during it.

---

*PROG 201 · Week 4 · Quiz 4 · covers Week 3 · ungraded*
