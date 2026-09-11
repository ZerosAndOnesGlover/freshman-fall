# CS 202 · Problem Set 3 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for PS 3.** This problem set straddles Midterm 1, and the concurrency in it is the kind where **a program can pass a test and be wrong**. Mark **arguments** as heavily as measurements: a mutual-exclusion claim must name the atomic step it depends on; a fairness claim must use per-philosopher counts; a deadlock-freedom claim must be a proof, not "I ran it ten times".

**Reference programs**: `solutions_instructor/casmutex reference`, `philo3 reference` and `rwpref reference (do not distribute).c`. The student skeletons in `assignments/ps3/` are the same files with the student's functions replaced by `TODO`s; all compile warning-clean.

**Every figure below is from the reference machine**: Intel i5-8250U (4 cores, 8 threads), Ubuntu 24.04.4, kernel 7.0, GCC 13.3.0. Student numbers will differ in magnitude; **the ordering of the locks in each row of Q1(b), and the shape of Q3's fairness results, should not.**

---

## Q1: A Mutex from Compare-and-Swap (30 points)

### (a) [10]

```c
#define SPIN_LIMIT 100

void cas_mutex_lock(cas_mutex *m)
{
    for (int spins = 0;; spins++) {
        int expected = 0;
        if (atomic_load_explicit(&m->held, memory_order_relaxed) == 0
            && atomic_compare_exchange_weak(&m->held, &expected, 1))
            return;
        if (spins < SPIN_LIMIT || !yielding)
            __asm__("pause");
        else
            sched_yield();
    }
}

void cas_mutex_unlock(cas_mutex *m)
{
    atomic_store(&m->held, 0);
}
```

- **Mutual exclusion**: a thread returns from `cas_mutex_lock` only after a compare-and-swap that changed `held` from 0 to 1. **The CAS is atomic, so of all threads that attempt it while `held` is 0, exactly one succeeds**; the value is then 1 until that thread's unlock stores 0. **The test before the CAS is only an optimisation** — its result can be stale — and correctness does not depend on it.
- **Progress**: if `held` is 0 and threads are trying, **some thread's CAS succeeds** — a CAS fails only because the value changed, which means another thread's succeeded. (A weak CAS may fail spuriously; the loop retries, and spurious failures do not persist.)

**Marking:** 6 for a correct lock meeting the specification, 2 + 2 for the arguments. **Deduct 4** if the CAS's `expected` is not reset inside the loop — after one failure it holds 1, and every later CAS "succeeds" by swapping 1 for 1 while another thread holds the lock.

### (b) [12]

| Row | `mine` | `spin` | `pthread` |
|---|---:|---:|---:|
| uncontended, 20M, CPU 3 | **16.4 ns** | — | 19.7 ns |
| 4 threads, CPUs 2–5, 4M, no critical-section work | 121.7 ns | 128.8 ns | **57.6 ns** |
| **4 threads, CPU 2 only**, 400k, section of 2,000 | **3,204.6 ns** | **8,110.5 ns** | 3,176.7 ns |
| **8 threads, CPUs 2–5**, 400k, section of 2,000 | **3,177.2 ns** | 5,954.1 ns | 3,969.0 ns |

*(This harness dispatches every lock call through a `switch`, so its uncontended `pthread` figure is higher than L11 §1's dedicated 7.39 ns loop. Compare locks within a row, not across programs.)*

**Prediction marks** go to any prediction honestly recorded and compared.

### (c) [5]

- **4 threads on 4 CPUs, tiny section: `pthread` wins, by half.** The lock is held for a few nanoseconds, the holder is always running, and glibc's mutex takes its fast path almost every time. `mine` and `spin` perform nearly the same because **`mine` almost never reaches `SPIN_LIMIT`** — the lock frees within a few pauses — and both lose to glibc on cache-line traffic from repeated CAS attempts. **Yielding never comes into it.**
- **4 threads on 1 CPU: `mine` ≈ `pthread`; `spin` is 2.5× worse.** When a holder is preempted mid-section, **it is not running**, and a spinner burns its whole slice waiting on a CPU the holder needs. **`sched_yield()` gives the CPU back to the scheduler, which runs another runnable thread — eventually the holder — so the lock is released without waiting out the spinner's slice.** That is the same effect glibc's sleeping lock gets, by a different route.
- **8 threads on 4 CPUs: `mine` wins.** More threads than CPUs means holders are regularly preempted, so pure spinning wastes slices (5.95 µs). **`pthread` puts waiters to sleep and wakes them with `futex` calls and context switches**, which on a section this length costs more than a brief spin followed by a yield (3.97 against 3.18 µs).

**Marking:** 1 for the first row, 2 each for the others. **Full marks in the one-CPU row require saying *which* thread runs instead of the spinner** (the holder, eventually) and **why that shortens the wait.**

### (d) [3]

**No bounded waiting.** Thread A's CAS can fail every time: each time the lock is released, some other thread — which happened to test and CAS a few nanoseconds earlier, or was simply running while A was yielding — takes it. **Nothing records that A has been waiting longest.** A thread that yields is particularly likely to lose, since it is not even running when the lock frees.

**`pthread_mutex_lock` does not guarantee bounded waiting either**: POSIX specifies no ordering among waiters, and glibc's default mutex lets a running thread "barge" in ahead of a woken sleeper. **In practice this is chosen deliberately** — FIFO handoff forces a context switch on every release — and it means starvation under contention is possible, merely unusual.

---

## Q2: A Lock That Is Not Atomic (10 points)

### (a) [3]

```
(timeout after 20 s, three runs)  exit 124
```

**It hangs.** At `-O2`, `broken_lock` inlined into `work()` looks like this:

```asm
1612:  mov    0x2a70(%rip),%edx        # 4088 <bm>     load held ONCE
161a:  je     16c3 <work+0xf3>                         if 0, go and set it to 1
1620:  call   1110 <sched_yield@plt>                   otherwise...
1625:  jmp    1620 <work+0x50>                         ...yield, forever
```

**The loop calls `sched_yield` and jumps straight back to the call — it never re-reads `held`.** A thread that sees the lock held **once** yields forever. With four threads, one of them almost immediately sees another holding it, and the program stops making progress.

**Marking:** 1 for reporting the hang, 2 for finding the loop and saying it does not reload `held`.

### (b) [3]

- **A data race on a non-atomic object is undefined behaviour** in C11. The compiler may assume the program has none — that is, **that no other thread modifies `bm.held` concurrently.**
- **`bm` is `static` and its address never leaves the translation unit**, so no function in another file — `sched_yield` included — can hold a pointer to it. **Under single-threaded semantics, `held` cannot change across the call.** The compiler therefore evaluates `m->held` once and hoists the test out of the loop.

**The lesson worth saying aloud in feedback:** a race is not merely "a wrong answer sometimes". **It licenses the compiler to transform the program into one that does something else entirely.**

**Marking:** 1½ + 1½.

### (c) [2]

With `volatile int held` (reference; `-O0` gives the same shape):

| Run | `-O2`, `volatile` | `-O0` |
|---|---:|---:|
| 1 | 30,688 of 40,000 | 33,834 |
| 2 | 26,142 | 30,912 |
| 3 | 28,992 | 38,081 |

**Wrong by 5–35%, and no hang.** The interleaving:

| Thread A | Thread B | `held` |
|---|---|---|
| `mov held → eax` (0) | | 0 |
| | `mov held → eax` (0) | 0 |
| `movl $1 → held` | | 1 |
| | `movl $1 → held` | 1 |
| **inside** | **inside** | |

**Both tested before either set.** The loop's `sched_yield` changes nothing about that.

**Marking:** 1 for the counters, 1 for an interleaving with two loads before either store.

### (d) [2]

**A single compare-and-swap on an atomic fixes mutual exclusion** — test and set become one atomic step — **and does not fix bounded waiting** (Q1(d)). **It also removes (a)'s problem**: an `_Atomic` object, or any access through `<stdatomic.h>`, is not a data race by definition, and the compiler must re-read it on every iteration. **Progress** was already present in the broken lock whenever it did not hang; accept an answer that says CAS "restores" it, with that reasoning.

---

## Q3: Five Philosophers, Measured (30 points)

### (a) [9]

Reference, three runs each, 3 s:

| Strategy | Deadlocked | Meals per second | Fewest / most | Ratio | Per philosopher (run 1) |
|---|---|---:|---:|---:|---|
| `naive` | **3 of 3** — after 6, 240, 135 meals | — | — | — | — |
| `ordered` | 0 | 20,627 · 20,523 · 19,709 | 9,330 / 14,503 | **0.64 · 0.57 · 0.56** | 10,178 · 13,587 · 14,282 · 14,503 · **9,330** |
| `seats` | 0 | 17,502 · 18,670 · 18,972 | 10,446 / 10,591 | **0.99 · 1.00 · 1.00** | 10,500 · 10,591 · 10,446 · 10,488 · 10,482 |
| `waiter` | 0 | 20,172 · 20,071 · 20,330 | 12,061 / 12,143 | **0.99 · 1.00 · 1.00** | 12,087 · 12,131 · 12,061 · 12,143 · 12,095 |

### (b) [6] `ordered` cannot deadlock

Suppose all five philosophers are blocked. **Each blocked philosopher holds its lower-numbered fork and is waiting for its higher-numbered one** — it acquires them in that order, and it cannot be waiting for its first fork while holding nothing, or that fork would be free for someone.

Take any blocked philosopher *p*<sub>1</sub>, holding fork *f*<sub>1</sub> and waiting for fork *g*<sub>1</sub> > *f*<sub>1</sub>. Fork *g*<sub>1</sub> is held by some philosopher *p*<sub>2</sub>. Since *p*<sub>2</sub> holds *g*<sub>1</sub> and is blocked, **either *g*<sub>1</sub> is *p*<sub>2</sub>'s lower fork**, and *p*<sub>2</sub> waits for a fork *g*<sub>2</sub> > *g*<sub>1</sub> — **or it is *p*<sub>2</sub>'s higher fork, in which case *p*<sub>2</sub> holds both and is not blocked** — a contradiction. So *g*<sub>2</sub> > *g*<sub>1</sub> > *f*<sub>1</sub>. Continuing, **every step in the chain of "waits for a fork held by" strictly increases the fork number.** With only five forks the chain must eventually revisit a philosopher, requiring some fork number to exceed itself. **Contradiction: not all can be blocked.**

**Marking:** full marks for any proof whose key step is "each wait is for a strictly higher-numbered fork, so the waits-for relation cannot cycle". **Zero** for "I ran it and it never deadlocked".

### (c) [6]

**Fairest: `waiter` and `seats`**, both with fewest/most at 0.99–1.00. **Least fair: `ordered`**, at 0.56–0.64.

**The first forks under `ordered`:** philosopher 0 → fork 0; 1 → 1; 2 → 2; 3 → 3; **4 → fork 0** (its forks are 4 and 0, and 0 is lower). **Philosophers 0 and 4 both start by competing for fork 0**, while every other philosopher's first fork is contested by nobody else as a *first* fork. **The two sharing a first fork eat least** — philosopher 4 the fewest in every run (8,233–9,330), philosopher 0 next — and philosopher 3, whose second fork (4) is rarely wanted because philosopher 4 is so often stuck waiting for fork 0, eats most (14,503–14,939).

**`waiter` is fair here** because it hands both forks atomically and broadcasts on every release, so every waiting philosopher re-checks, and with symmetric think and eat times no pair can consistently lock out a neighbour. **A student who argues that `waiter` *can* starve a philosopher** — two neighbours alternating so that both of philosopher *i*'s forks are never free at once — **is correct in principle and should get credit for it**, but must report that it did not happen in their measurement.

### (d) [6]

The four conditions (OSTEP Ch. 32): **mutual exclusion, hold-and-wait, no preemption, circular wait.**

- **`ordered` breaks circular wait** — (b)'s proof is exactly that no cycle can form.
- **`seats` also breaks circular wait**, differently: a cycle of waiting around the table needs all five philosophers each holding one fork, and at most four are ever seated. **Hold-and-wait still happens**; the cycle cannot close.
- *(For comparison, `waiter` breaks **hold-and-wait**: nobody ever holds one fork while waiting for another.)*

**Marking:** 3 + 3. Accept "`seats` prevents the circular-wait condition from being satisfiable" in any wording.

### (e) [3]

**Resource ordering** — acquire rows in a fixed order, such as by primary key — is what databases and file systems actually do: no global bottleneck, no counting semaphore to size, and deadlock-freedom by construction. **`waiter`** serialises every acquisition through one lock, which becomes the bottleneck at scale. **Accept `waiter` for a small system** if the student names the bottleneck; accept `seats` if they say how *N* would be chosen.

---

## Q4: A Writer-Preferring Reader–Writer Lock (20 points)

### (a) [8]

```c
static void my_rdlock(my_rwlock *l)
{
    pthread_mutex_lock(&l->m);
    while (l->writer || l->waiting_writers > 0)
        pthread_cond_wait(&l->readers_ok, &l->m);
    l->readers++;
    pthread_mutex_unlock(&l->m);
}

static void my_rdunlock(my_rwlock *l)
{
    pthread_mutex_lock(&l->m);
    if (--l->readers == 0)
        pthread_cond_signal(&l->writer_ok);
    pthread_mutex_unlock(&l->m);
}

static int my_wrlock_until(my_rwlock *l, const struct timespec *deadline)
{
    int rc = 0;
    pthread_mutex_lock(&l->m);
    l->waiting_writers++;
    while ((l->writer || l->readers > 0) && rc == 0)
        rc = pthread_cond_timedwait(&l->writer_ok, &l->m, deadline);
    l->waiting_writers--;
    if (rc == 0)
        l->writer = 1;
    else if (l->waiting_writers == 0)
        pthread_cond_broadcast(&l->readers_ok);
    pthread_mutex_unlock(&l->m);
    return rc == 0 ? 0 : -1;
}

static void my_wrunlock(my_rwlock *l)
{
    pthread_mutex_lock(&l->m);
    l->writer = 0;
    if (l->waiting_writers > 0)
        pthread_cond_signal(&l->writer_ok);
    else
        pthread_cond_broadcast(&l->readers_ok);
    pthread_mutex_unlock(&l->m);
}
```

**The give-up branch is the question's trap.** A writer that times out has been holding readers back through `waiting_writers`. **If it simply decrements and leaves, readers already asleep on `readers_ok` stay asleep** until some unrelated event wakes them. Broadcasting when no other writer is waiting releases them.

**Marking:** 2 per function. **Deduct 3** for a missing give-up broadcast; **deduct 2** for `if` instead of `while` in either wait.

### (b) [6]

| Lock | Writer acquisitions | Gave up | Median wait | Max wait | Reads completed |
|---|---:|---:|---:|---:|---:|
| `glibc` (default) | **0 · 0** | 4 · 4 | — | — | **171,912 · 170,748** |
| `glibc-writer` | 390 · 390 | 0 | 0.192 · 0.196 ms | 0.317 · 0.315 ms | 166,380 · 165,792 |
| **`mine`** | 390 · 389 | 0 | 0.191 · 0.194 ms | 0.342 · 0.837 ms | 165,665 · 165,372 |

**`mine` matches glibc's writer-preferring kind** to within run-to-run noise on the median. **Preferring writers cost the readers about 3%** of their throughput (≈171,000 reads against ≈166,000), because every writer arrival makes new readers wait until it has finished.

### (c) [6]

**Readers starve if writers arrive faster than they finish** — for example, writers with no pause between attempts, or many writers. `waiting_writers` is then never 0 when a reader checks, so **no reader is ever admitted.**

**A fair policy**, in outline: **admit in arrival order, in batches** — when a writer releases, admit *all readers that were waiting at that moment* (but not readers who arrive afterwards) before the next writer; when those readers finish, admit the next writer. **Neither side can starve**, since each waiting party is served within one batch of the other kind. **Cost**: more state (a queue, or a generation counter), somewhat longer writer waits than pure writer preference, and more wake-ups.

**Marking:** 3 for the starvation workload, 3 for a policy that actually bounds both waits with its cost stated.

---

## Q5: Locks in xv6 (10 points)

### (a) [4]

If `acquire` disabled interrupts **after** obtaining the lock, there would be an instant **with the lock held and interrupts still on**. A timer or device interrupt arriving then, on the same CPU, runs a handler that may try to `acquire` **the same lock** — the tick counter's, or the console's. **The holder is the code the interrupt suspended, on this CPU, and cannot run until the handler returns; the handler spins forever.** One CPU, one thread of control, deadlocked. **Disabling interrupts first closes that window.** *(`holding()` would not catch it either — it would see this CPU holding the lock and panic, which is at least visible.)*

**Marking:** 4 for the interrupt-handler-on-same-CPU scenario. 2 for "interrupts could arrive" without the same-lock deadlock.

### (b) [6]

**Two CPUs returning the same page:**

| CPU 0 | CPU 1 |
|---|---|
| `r = kmem.freelist;` → page P | |
| | `r = kmem.freelist;` → **page P** |
| `kmem.freelist = r->next;` → Q | |
| | `kmem.freelist = r->next;` → Q |
| returns P | **returns P** |

**Both processes receive P.** Each writes its letter into it; one reads back the other's. That is `allocstress`'s `found 66, wrote 65`.

**`sbrk` failing:** `kfree` pushes (`r->next = freelist; freelist = r`) and `kalloc` pops, and **a push interleaved with a pop can overwrite `freelist` with a stale pointer** — dropping the freed page, and every page linked after it, from the list. **Enough lost links and the list is empty while most of memory is free**, so `kalloc` returns 0 and `sbrk` fails as if memory were exhausted.

**`panic: remap`:** a page handed out twice may be used **as a page-table page** by one allocation while also being handed to a process as ordinary memory, or allocated as a page table twice. When `mappages` then installs a mapping, **it finds the page-table entry already marked present** — written by the other user of the same page — and xv6 panics rather than silently overwrite a mapping.

**Marking:** 3 for a correct two-CPU interleaving, 1½ each for the two symptoms. **Accept** any mechanism for `sbrk` failure that loses free-list links, and any for `remap` in which one physical page ends up in two roles.

---

*CS 202 · Week 3 · PS 3 Solutions · Instructor Only*
