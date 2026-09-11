# CS 202 · Operating Systems
## Week 3 · Lecture 3 of 3
### Condition Variables, Semaphores, and the Classic Problems

---

**Sat:** Friday of Week 3, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 30 and 31; xv6 book Ch. 5 on sleep and wakeup · **Next:** Week 4, deadlock — and Midterm 1 on Monday evening

---

## 1. Waiting for a Condition, Not a Lock

A lock answers *"may I touch this data?"*. Threads often need a different answer: **"is there anything to take?"**, **"is there room to put this?"**, **"has my child exited?"**. Holding a lock while looping until the answer is yes blocks everyone who could make it yes; releasing it and re-checking in a loop burns a CPU.

**A condition variable** is a queue of threads waiting for some condition to become true, used together with the lock that protects the data the condition is about:

| Operation | Does, atomically |
|---|---|
| `pthread_cond_wait(cv, m)` | **release `m` and go to sleep on `cv`**; when woken, **re-acquire `m`** before returning |
| `pthread_cond_signal(cv)` | wake one waiter, if any |
| `pthread_cond_broadcast(cv)` | wake all waiters |

**The atomic release-and-sleep is the whole point**, for exactly L11 §3's reason: a thread that released the lock and then slept as two steps could miss a signal sent in between.

**The bounded buffer** — producers put items in, consumers take them out, the buffer has finite room — is the canonical use. The correct version, with a one-slot buffer:

```c
/* producer */                                  /* consumer */
pthread_mutex_lock(&m);                         pthread_mutex_lock(&m);
while (count == 1)                              while (count == 0)
    pthread_cond_wait(&not_full, &m);               pthread_cond_wait(&not_empty, &m);
count = 1;                                      count = 0;
pthread_cond_signal(&not_empty);                pthread_cond_signal(&not_full);
pthread_mutex_unlock(&m);                       pthread_mutex_unlock(&m);
```

**Two details in those ten lines are each the difference between correct and broken**, and `bbuf.c` measures both.

---

## 2. `while`, Not `if`

Change the consumer's `while (count == 0)` to `if`. **One producer, three consumers, 300,000 items**, three runs:

```
if2     consumed 300000 of 300000; woke to an empty buffer 286 times
if2     consumed 300000 of 300000; woke to an empty buffer 372 times
if2     consumed 300000 of 300000; woke to an empty buffer 254 times
```

**Hundreds of times per run, a consumer returned from `pthread_cond_wait` to find the buffer empty.** With `if`, it would then have "taken" an item that did not exist.

**How.** The producer puts an item in and signals `not_empty`, waking consumer C1. **But being woken is not the same as running.** C1 must re-acquire the mutex, and before it does, consumer C2 — which was not waiting at all, just arriving — takes the mutex, sees an item, and takes it. When C1 finally gets the mutex, the item is gone.

**This is *Mesa semantics***, which every mainstream threading system has: a signal means *"the condition was true when I signalled — look again"*, not *"it is true now"*. (*Hoare semantics*, in which the signalled thread runs immediately and the condition is guaranteed, is easy to reason about and costly to implement; nobody ships it.) **POSIX also permits *spurious* wake-ups** — returning from a wait with no signal at all.

> **Rule: always re-test the condition in a `while` loop after waking.** It costs one comparison
> and makes both stolen and spurious wake-ups harmless. With `while`, the same program woke to an
> empty buffer **0 times** in each of three runs.

---

## 3. One Condition Variable for Two Conditions

Now keep `while`, but let producers and consumers **share one condition variable** — producers wait on it when the buffer is full, consumers when it is empty, and everyone signals it:

```
while1  DEADLOCK: no progress for 2 s after 3 of 300000 items consumed (empty takes 0)
while1  DEADLOCK: no progress for 2 s after 10 of 300000 items consumed (empty takes 0)
while1  DEADLOCK: no progress for 2 s after 2 of 300000 items consumed (empty takes 0)
```

**Deadlocked within ten items, all three times** — every thread asleep, the buffer in a state some thread could act on, and no thread awake to act.

**How.** Two consumers are asleep on the shared CV, waiting for an item. The producer adds one, signals, and — the buffer now full — goes to sleep on **the same CV**. Consumer C1 wakes, takes the item, and **signals the CV intending to wake the producer**. **But `signal` wakes one waiter, and the other waiter on that CV is consumer C2.** C2 wakes, finds the buffer empty, and sleeps again. The producer was never woken. Nobody is left awake.

**The fix is the second detail: two condition variables**, one per condition, so that a signal can only wake a thread waiting for the thing that just became true. `pthread_cond_broadcast` on the shared CV also works — every sleeper wakes and re-tests in its `while` — at the cost of waking threads that will immediately sleep again.

---

## 4. xv6's Condition Variable: `sleep` and `wakeup`

xv6 has no `pthread_cond_t`, but it has the same mechanism, in `proc.c`:

```c
void
sleep(void *chan, struct spinlock *lk)
{
  ...
  // Must acquire ptable.lock in order to
  // change p->state and then call sched.
  // Once we hold ptable.lock, we can be
  // guaranteed that we won't miss any wakeup
  // (wakeup runs with ptable.lock locked),
  // so it's okay to release lk.
  if(lk != &ptable.lock){
    acquire(&ptable.lock);
    release(lk);
  }
  p->chan = chan;
  p->state = SLEEPING;
  sched();
  p->chan = 0;
  if(lk != &ptable.lock){
    release(&ptable.lock);
    acquire(lk);
  }
}

void
wakeup1(void *chan)
{
  struct proc *p;
  for(p = ptable.proc; p < &ptable.proc[NPROC]; p++)
    if(p->state == SLEEPING && p->chan == chan)
      p->state = RUNNABLE;
}
```

| pthreads | xv6 |
|---|---|
| condition variable | **a channel** — any address, conventionally the object waited on |
| the mutex passed to `wait` | **`lk`** |
| atomic release-and-sleep | **acquire `ptable.lock`, *then* release `lk`** — `wakeup` needs `ptable.lock` too, so it cannot run in between |
| `signal` or `broadcast` | **`wakeup` wakes every sleeper on the channel** — always a broadcast |

**Because `wakeup` is a broadcast, every caller of `sleep` must loop** — and they do. `wait` loops scanning for a zombie child; `piperead` loops `while(p->nread == p->nwrite && p->writeopen)`; `acquiresleep` (L11 §7) loops `while (lk->locked)`. **§2's rule, in the kernel.**

**The comment in `sleep` is the lost-wakeup problem stated precisely**: a process that checked a condition under `lk`, decided to sleep, released `lk` and was then interrupted before marking itself asleep would miss a `wakeup` sent in that gap. Holding `ptable.lock` across the gap closes it.

---

## 5. Semaphores

**Dijkstra's semaphore** (1960s) is an integer with two operations:

- **`P`** (`sem_wait`): if the value is positive, decrement it; otherwise sleep until it is.
- **`V`** (`sem_post`): increment it, waking a sleeper if there is one.

**A semaphore initialised to 1 is a mutex. Initialised to *n*, it admits *n* holders at once** — a pool of *n* connections, *n* seats at a table. **Initialised to 0, it is a signal that is remembered**: a `V` before anyone waits is not lost, unlike a condition variable's `signal`.

Uncontended, `sem_wait` + `sem_post` cost **19.05 ns** against a mutex's 7.39 (L11 §1): a semaphore must maintain a count that may be read and changed by several threads, not just a flag.

**Semaphores and condition variables can each be built from the other**, and OSTEP Chapter 31 shows that building a condition variable from semaphores is harder than it looks. **In practice**: use a mutex and condition variables when the condition is a predicate over data; use a semaphore when the condition *is* a count.

---

## 6. The Dining Philosophers

Five philosophers sit at a round table with **one fork between each pair**. To eat, a philosopher needs both adjacent forks. **`philo.c`** models each fork as a mutex and each philosopher as a thread that eats as fast as it can, until 200,000 meals have been eaten or nobody has eaten for a second:

| Strategy | Deadlocked | Result |
|---|---:|---|
| **naive**: pick up left, then right | **10 of 10 runs** | after **786–1,157 meals** |
| **ordered**: pick up the lower-numbered fork first | **0 of 10** | 200,000 meals within the first second, every run |
| **seats**: a semaphore lets only four sit at once | **0 of 10** | 200,000 meals within the first second, every run |

**The naive strategy deadlocks every time, and quickly.** If all five pick up their left fork at once, each holds one fork and waits forever for the fork its neighbour holds. With threads racing, "at once" happens within about a thousand meals.

**Both fixes break the cycle, differently.**

- **Ordering** means philosopher 4, whose forks are 4 and 0, picks up **0 first** — reaching across the table in the opposite direction from everyone else. A cycle of waiting would need every philosopher to hold a lower-numbered fork while waiting for a higher one, which philosopher 4 never does.
- **Four seats** means that at most four philosophers compete for five forks, so at least one of them can always get both.

**Week 4 names what both fixes attacked** — the *circular wait* that is one of four conditions every deadlock needs — and adds two more ways out.

---

## 7. Readers and Writers

Many threads read shared data; occasionally one writes. **Reads can safely overlap; writes cannot overlap with anything.** A reader–writer lock allows exactly that — and must decide what happens when a writer arrives while readers hold the lock.

`rw.c` runs **seven readers who never stop reading** — each holds the read lock for about 100 µs, then immediately takes it again — and **one writer who wants the lock every 10 ms**, giving up after one second of waiting:

| glibc rwlock kind | Writer got the lock, in 4 s | Gave up | Median wait | Max wait |
|---|---:|---:|---:|---:|
| **default** | **0 times** | **4 times** | — | — |
| `PTHREAD_RWLOCK_PREFER_WRITER_NONRECURSIVE_NP` | 389 times | 0 | 0.202 ms | 0.946 ms |

**With the default lock, the writer never got in.** glibc's default prefers readers: a new reader may join while the lock is read-held, even with a writer waiting. **Seven overlapping readers meant the lock was never free of readers, so the writer starved** — L10 §3's bounded-waiting property, violated and measured.

**Preferring writers fixes the writer** — a waiting writer blocks new readers, so the current readers drain and the writer gets in within a millisecond — **at the cost of making every reader wait while any writer does.** There is no choice that is free for both; there is only a choice about who waits.

---

## 8. The Sleeping Barber

The curriculum's third classic problem, due to Dijkstra: **a barbershop with one barber, one barber's chair, and *N* waiting chairs.** If there are no customers, the barber sleeps. A customer who arrives to find the barber asleep wakes him; one who finds all waiting chairs full leaves.

It is a bounded buffer whose consumer sleeps, and the standard solution uses two semaphores and a mutex:

```c
sem_t customers;   /* 0: customers waiting to be served  */
sem_t barber;      /* 0: the barber ready to cut          */
pthread_mutex_t m; int waiting = 0;

void barber_loop(void) {                     void customer(void) {
    for (;;) {                                   pthread_mutex_lock(&m);
        sem_wait(&customers);  /* sleep */       if (waiting < CHAIRS) {
        pthread_mutex_lock(&m);                      waiting++;
        waiting--;                                   sem_post(&customers);  /* wake barber */
        sem_post(&barber);                           pthread_mutex_unlock(&m);
        pthread_mutex_unlock(&m);                    sem_wait(&barber);     /* wait for chair */
        cut_hair();                                  get_haircut();
    }                                            } else {
}                                                    pthread_mutex_unlock(&m);  /* leave */
                                                 }
                                             }
```

**The hazard it teaches is the one in §3**: without the mutex around `waiting`, a customer can decide to wait at the same moment the barber decides there is nobody, and each sleeps waiting for the other. **The semaphores remember the posts that a condition variable would lose**, which is why this problem is traditionally solved with them.

---

## 9. Monitors

A **monitor** is a language construct that bundles data with the procedures that use it, **locks automatically on entry to any procedure**, and provides condition variables tied to that lock. Java's `synchronized` methods with `wait` and `notify` are a monitor with Mesa semantics; so are C#'s `lock` and Python's `threading.Condition`.

**C has no monitors** — which is why every piece of C in this lecture pairs a mutex with its condition variables by convention. **Everything a monitor enforces, a C programmer must do by hand**: take the lock before touching the data, pass the right mutex to `wait`, loop after waking, and release the lock on every path out.

---

## 10. What to Take Away

1. **A condition variable atomically releases the mutex and sleeps**, for the same reason `FUTEX_WAIT` compares before sleeping.
2. **Always re-test in `while`.** With `if`, consumers woke to an empty buffer 254–372 times per 300,000 items; with `while`, zero.
3. **One condition per condition variable.** A shared CV deadlocked within 2–10 items — a signal meant for a producer woke a consumer.
4. **xv6's `sleep` and `wakeup` are a condition variable**, `wakeup` always broadcasts, and every `sleep` in xv6 is inside a loop.
5. **A semaphore is a counter that remembers posts**; at 1 it is a mutex, at *n* a pool, at 0 a remembered signal.
6. **Naive philosophers deadlocked 10 runs in 10**; ordering the forks or limiting the seats deadlocked none.
7. **glibc's default reader–writer lock starved a writer completely** — zero acquisitions in four seconds — and preferring writers got it in within a millisecond, at the readers' expense.

---

## Exercises

1. `bbuf.c`'s `if2` mode still consumed every item, because its consumer loops back rather than taking a phantom item. Change it to decrement `count` unconditionally after waking, and run it. What does the program report now?
2. In `while1` mode, replace `pthread_cond_signal` with `pthread_cond_broadcast` everywhere. Measure how many wake-ups return to find nothing to do, and compare the run time with `while2`.
3. xv6's `wakeup1` makes every sleeper on a channel runnable. **Name a place in xv6 where that causes a *thundering herd*** — many processes woken, one able to proceed — and estimate its cost.
4. Implement philosopher strategy **"waiter"**: a single mutex and a condition variable, through which a philosopher picks up both forks at once or waits. Compare its meals per second and its fairness (fewest meals by any philosopher) with `ordered`.
5. `rw.c`'s writer-preferring lock let a writer in within a millisecond. **Construct a workload in which it starves readers**, and measure it.

---

*CS 202 · Week 3 · L12 · © CSE Department*
