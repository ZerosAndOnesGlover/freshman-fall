# PROG 201 · Systems Programming in C
## Week 2 · Lecture 3 of 3
### Semaphores, and Choosing a Mechanism

---

**Reading:** APUE §15.8, §15.10 · TLPI Ch. 53 · `man 7 sem_overview`, `man 3 sem_wait` · **Previous:** L08 · **Next:** Lab 2 — benchmark all four, on the Monday of Week 3

---

## 1. A Semaphore Is a Counter With a Waiting Room

```c
sem_wait(&s);     /* if s > 0, s--.  Otherwise sleep until it is > 0, then s-- */
sem_post(&s);     /* s++, and wake one sleeper if there is one */
```

That is the entire interface, and both operations are **atomic**: no other process can see the counter between the test and the decrement. That is the one thing you cannot write yourself in C, and it is the only reason the primitive exists.

Two ways to read the same counter, and you will use both this week:

- **A permit count.** Initialise to *N* and the semaphore admits *N* holders at once. *N* = 1 is a **mutex**; *N* = 8 is a connection pool.
- **A count of things that have happened.** Initialise to 0 and `sem_post` means "one more item is ready", `sem_wait` means "wait for one". This is a **signal**, not a lock, and it is what makes §5's ring work.

The producer-consumer pattern uses one of each, which is why students who only ever think "semaphore = mutex" find it baffling.

### Where the counter lives

| Kind | Created by | Lives in | Shared between |
| --- | --- | --- | --- |
| **Unnamed, `pshared = 0`** | `sem_init(&s, 0, n)` | Ordinary memory | Threads of one process |
| **Unnamed, `pshared = 1`** | `sem_init(&s, 1, n)` | **Shared memory you provide** | Any process that maps it |
| **Named** | `sem_open("/name", ...)` | `/dev/shm/sem.name` | Any process that knows the name |

The middle row is the one Week 2 uses, and its requirement is absolute: **the `sem_t` must itself be in the shared region.** Put it in a local variable, pass its address to a child, and you have two unrelated counters and a program that "works" until it does not.

```c
struct region { sem_t lock; long counter; };     /* the semaphore is inside */
```

Named semaphores are kernel-persistent like everything else in L08 §4:

```
2. sem_open created /dev/shm/sem.prog201.sem (32 bytes, mode 600)
```

Note the `sem.` prefix the library adds, and that a `sem_t` is 32 bytes of ordinary shared memory. There is nothing magic in it — the magic is in the atomic instruction the library uses on it.

---

## 2. What It Costs Not to Have One

`shm.c` maps a shared `long`, forks four processes, and has each add 1 to it 200,000 times. Eight hundred thousand increments; the counter should read 800,000:

```
unguarded:   counter = 282666, expected 800000  (517334 updates lost, 64.7%)
unguarded:   counter = 241292, expected 800000  (558708 updates lost, 69.8%)
sem_wait:    counter = 800000, expected 800000  (0 updates lost, 0.0%)
```

**Two thirds of the work vanished**, and the amount that vanishes changes every run.

`counter++` compiles to load, add, store. Two processes load 41, both add, both store 42, and one increment is gone. Nothing detects it. There is no error, no signal, no log line — the number is simply wrong, and it is wrong by a different amount each time, which is exactly the property that makes this class of bug expensive.

Notice how *large* the loss is. People expect a race to be rare — "a narrow window", "one in a million". Here it is the common case, because four processes on four cores are executing the same three instructions on the same cache line as fast as they can. **A window is only narrow relative to how often you aim at it.**

The fix is two lines and it is exact:

```c
sem_wait(&r->lock);
r->counter++;
sem_post(&r->lock);
```

Zero lost, every run. What that costs is §3.

---

## 3. The Uncontended Case Is Nearly Free; the Contended Case Is a System Call

From `maps.c`, ten million uncontended pairs, and two reference points:

| Operation | Cost |
| --- | --- |
| `sem_wait` + `sem_post`, uncontended | **19.3 ns** |
| `memcpy` of 4,096 bytes | **117.8 ns** |
| `getpid()` through `syscall()` | **574.2 ns** |
| A blocking semaphore handoff between two processes | **≈ 3.3 µs** (from §5's 6.6 µs round trip) |

19.3 ns is about sixty cycles, and there is **no system call in it**. glibc implements `sem_wait` as an atomic decrement in user space; it only enters the kernel — via `futex` — when the counter is already zero and it has to sleep. `strace` a lock that is never contended and you will see nothing at all, which is the correct and initially alarming result.

**So the cost of a lock is not the lock. It is the sleeping.** The gap between 19.3 ns and 3.3 µs is a factor of a hundred and seventy, and which side of it you land on is decided by your design, not by your choice of primitive. That is the whole reason for §6's tables.

### `sem_wait` and `EINTR` — and the folklore is wrong

`gotcha.c` blocks in `sem_wait` and takes a `SIGUSR1` with a handler installed:

```
$ ./gotcha                    # handler installed with sa_flags = 0
3. sem_wait returned -1, errno=Interrupted system call   (handler flags: none)

$ RESTART=1 ./gotcha          # handler installed with SA_RESTART
(hangs)
```

`sem_wait` **is** interruptible, and `SA_RESTART` **does** restart it — glibc restarts the underlying `futex` wait. You will read in more than one place that `SA_RESTART` has no effect on `sem_wait`; on this machine, with this glibc, it plainly does.

Do not rely on either behaviour. Write the loop:

```c
while (sem_wait(&s) == -1 && errno == EINTR)
    ;
```

This is Week 0 L03 §5's rule arriving in new clothes, and the same reasoning applies: `SA_RESTART` covers *some* calls on *some* systems, so a program that is correct everywhere handles `EINTR` itself. `sem_timedwait` has the same requirement plus `ETIMEDOUT`.

---

## 4. Producer and Consumer, Written Out

The pattern the rest of the course reuses. Two semaphores and a ring:

```c
struct ring {
    sem_t empty, full;               /* both in the shared region */
    unsigned head, tail;
    char data[SLOTS][SLOT_SIZE];
};

sem_init(&r->empty, 1, SLOTS);       /* SLOTS free slots to start */
sem_init(&r->full,  1, 0);           /* nothing to consume yet    */
```

```c
/* producer */                          /* consumer */
sem_wait(&r->empty);                    sem_wait(&r->full);
memcpy(r->data[r->head], src, n);       memcpy(dst, r->data[r->tail], n);
r->head = (r->head + 1) % SLOTS;        r->tail = (r->tail + 1) % SLOTS;
sem_post(&r->full);                     sem_post(&r->empty);
```

Read the symmetry: **each side waits on the resource it consumes and posts the resource it produces.** The producer consumes free slots and produces full ones. Nothing else is needed for one producer and one consumer — `head` is touched only by the producer and `tail` only by the consumer, so no third semaphore is required.

**With more than one producer you need one.** Two producers both read `head`, both write the same slot, and you are back in §2. Add a `sem_t mutex` around the index update — and now the ordering matters:

```c
sem_wait(&r->empty);      /* CORRECT: get a slot, then get the lock */
sem_wait(&r->mutex);
...
```
```c
sem_wait(&r->mutex);      /* WRONG: holds the lock while waiting for a slot */
sem_wait(&r->empty);
...
```

Every textbook calls the second one a deadlock. **Run it and it completes.** Two producers, a ring of two, 40,000 records: both orderings finish.

It completes because *this* consumer never asks for the mutex. It only touches `tail`, so when a producer is blocked on `empty` holding the mutex, the consumer is unobstructed — it takes a record, posts `empty`, and the producer wakes. The wrong ordering costs you concurrency between the producers and nothing else.

Now give the consumer a reason to take the mutex — a shared record count, a high-water mark, anything the producers also touch — and the same code hangs on the first full ring:

1. Producer 1 holds `mutex` and blocks on `empty`.
2. The consumer blocks on `mutex`.
3. The consumer is the **only** source of `sem_post(&empty)`, and it cannot reach that line.

**Never block on a resource while holding a lock that the party who would release that resource needs to acquire.** That is the rule, and note what the experiment adds to it: **the bad ordering is not always a deadlock, which is precisely why it survives code review and ships.** It is PS 2's Q4.

---

## 5. The Benchmark

Now the claim from L08 §1, measured. This is Lab 2's own program, `bench.c`: it moves 256 MiB between a parent and a child in 4,096-byte chunks, and separately does 100,000 one-byte round trips.

**Bulk transfer — 256 MiB in 4 KiB chunks**

| Mechanism | Seconds | MiB/s |
| --- | --- | --- |
| pipe | 0.070 | **3,680** |
| FIFO | 0.088 | 2,924 |
| POSIX mq | 0.092 | 2,786 |
| shm + semaphores, **one slot** | 0.446 | **574** |

**Round trip — 100,000 one-byte ping-pongs**

| Mechanism | Seconds | µs per trip |
| --- | --- | --- |
| pipe | 0.720 | 7.20 |
| shm + semaphores | 0.661 | **6.61** |

Three runs each; bulk varies about 10% run to run, the round trip about 5%. The orderings are stable.

Two results, and both are the opposite of what you were told.

**The fastest IPC mechanism came last in bulk, by six times.** A pipe moved data six times faster than the mechanism every textbook calls the fastest.

**And on latency it barely won at all** — 8%, which is close to the run-to-run noise. If shared memory's advantage were "no kernel", a round trip should have been dramatically cheaper, and it was not.

Before reading on, work out why both of those happened. Everything you need is in L07 §2 and §3 of this lecture.

---

## 6. Why, and What It Actually Means

Take the round trip first, because it is the simpler one.

**A blocking `sem_wait` is a `futex` sleep, and a blocking `read` on an empty pipe is a kernel sleep too.** Both wake the peer through the scheduler; both pay a context switch. Shared memory removed the *copy* of one byte — 118 ns for a whole page (§3), so a fraction of a nanosecond for one byte — and left the expensive half exactly where it was. **8% is the right answer.** A round trip is two sleeps whatever you build it on.

Now the bulk result, which has three causes.

**Cause one: a pipe already has a sixteen-slot ring.** L07 §2. The writer can put sixteen pages in before it must wait, so producer and consumer overlap and neither sleeps very often. The one-slot ring forces a **lockstep handoff**: every 4 KB, the producer sleeps, the consumer wakes, the consumer sleeps, the producer wakes. Two sleeps at ~3 µs per 4 KB, against a copy that costs 118 ns.

So deepen the ring and change nothing else — `./bench slots 256 4096`:

```
slots                       seconds        MiB/s
1                             0.459         557.2
2                             0.261         982.2
4                             0.064        3978.6
8                             0.060        4239.5
16                            0.055        4618.9
32                            0.055        4658.4
64                            0.062        4158.4
```

**Four slots is a seven-fold improvement over one, and gets you past the pipe.** The curve is flat from 8 slots on, because by then the two processes overlap fully and what is left is the `memcpy` and the cache traffic. The remaining margin over the pipe — about 1.2× — is the one copy shared memory really did save.

**Cause two: there were never fewer system calls.** Count them — `strace -c -f`, 256 MiB in 4 KB chunks:

```
pipe:            65,537 write + 65,538 read           = 131,114 system calls
shm, one slot:  131,778 futex (65,249 of them EAGAIN) = 131,817 system calls
```

**The same number.** The mechanism sold as "no system calls" made 703 more of them than the pipe did. It removed 65,536 copies of a page — about 7.7 ms of `memcpy` at §3's rate — and spent the saving on futex sleeps that cost more than the `read`/`write` pair they replaced.

The "no system call" claim is true of the *uncontended* semaphore (§3, 19.3 ns, and `strace` shows nothing). A one-slot ring is contended on every single operation, so the fast path is never taken.

**Cause three: the saving is per byte and the cost is per message.** So the ratio must move with message size, and it does. Same program, one slot, 128 MiB each:

| chunk | pipe MiB/s | shm MiB/s | shm / pipe |
| --- | --- | --- | --- |
| 64 B | 79.4 | 8.8 | **0.11×** |
| 512 B | 633.9 | 66.9 | 0.11× |
| 4,096 B | 3,648.7 | 670.0 | 0.18× |
| 16,384 B | 3,701.8 | 2,094.0 | 0.57× |
| 65,536 B | 2,887.9 | 6,554.8 | **2.27×** |
| 262,144 B | 2,510.3 | 14,431.7 | **5.75×** |

The crossover is between 16 KB and 64 KB. Below it you are paying two context switches to save one copy of something too small to be worth copying. Above it the pipe is capped by its own 64 KB buffer — a 256 KB write blocks three times on the way through — while shared memory is not.

**Also read the `POSIX mq` row of that sweep in Lab 2's output: it is `--` from 16 KB up**, because `mq_msgsize` cannot exceed 8,192 (L08 §3). The mechanism does not get slower at large messages; it becomes unavailable.

**The sentence to keep:**

> Shared memory does not make IPC fast. It removes the kernel from the *transfer*, and the kernel was never the expensive part — the **wakeup** was. You win when the message is large enough that one copy costs more than two context switches, and not before.

And the honest reading of the textbook claim: it is true for the case it is usually said about — a large region both processes work in, synchronising rarely — and false as a general statement about moving messages between them.

---

## 7. Choosing

| Need | Reach for | Because |
| --- | --- | --- |
| A stage in a pipeline, related processes | **pipe** | Free, no cleanup, 16-page buffer already built in |
| The same, unrelated processes | **FIFO** | A name is all a pipe was missing (L07 §5) |
| Discrete requests with priorities, low rate | **POSIX mq** | Boundaries and ordering for free — but 10 × 8 KB is the ceiling (L08 §3) |
| Large records, high rate, related or not | **shm + semaphores** | Above ~64 KB per message it is the only one that scales |
| A big structure both sides read and rarely write | **shm** | The transfer never happens at all — that is the real win |
| Notification only, no data | **`kill` / `signalfd` / an empty pipe write** | Week 0 L03, and Week 5's self-pipe |
| Two machines | **sockets** | Week 5. None of the above crosses a network |

And three rules that are worth more than the table:

1. **Start with a pipe.** It is the cheapest thing to write, it has no cleanup, its buffer is already 64 KB, and it is fast enough for almost everything. Move only when you have measured a reason.
2. **If you reach for shared memory, batch.** A one-slot ring is the slowest thing on this page. Depth is free; wakeups are not.
3. **Measure on your machine.** Every number in this lecture is from one Linux 7.0 box with one glibc. The *orderings* will hold; the crossover point will move.

---

## Summary

- A semaphore is an atomic counter with a waiting room: a **permit count** (initialise to *N*) or a **signal** (initialise to 0).
- For processes the `sem_t` must live **inside the shared region**, with `pshared = 1`.
- An unguarded shared counter lost **64.7% of 800,000 increments**. With `sem_wait`, zero, every run.
- Uncontended `sem_wait`+`sem_post` costs **19.3 ns and no system call**; a contended handoff costs **~2 µs**. The factor of a hundred between them is your design, not your primitive.
- `sem_wait` returns **`EINTR`** — and on this glibc `SA_RESTART` really does restart it, contrary to the usual advice. Write the retry loop anyway.
- Producer-consumer: **wait on what you consume, post what you produce.** With multiple producers, take the slot before the mutex. The other order **completes** when the consumer needs no lock and **deadlocks** the moment it does — measured both ways.
- Measured: a pipe moved bulk data **6× faster** than a one-slot shared-memory ring, and shared memory won the round trip by only **8%** — because a round trip is two sleeps whatever you build it on.
- **Deepening the ring to four slots is a 7× gain** and is what gets shared memory past the pipe at 4 KB. The rest is message size: **0.11× at 64 B, 2.3× at 64 KB, 5.8× at 256 KB.**
- `strace` counted **131,114 system calls for the pipe and 131,817 for the one-slot ring** — the same number. The "no system calls" claim describes the *uncontended* semaphore, and a one-slot ring is contended every time.
- What shared memory removes is the copy. The cost was the **wakeup**.

---

## Exercises

1. In `shm.c`, replace `counter++` with `__atomic_fetch_add(&r->counter, 1, __ATOMIC_SEQ_CST)` and drop the semaphore. Is the count right? Time it against the semaphore version and explain the difference.
2. Initialise `empty` to `SLOTS + 1` by mistake. What is the first symptom, and how many messages does it take to appear?
3. Build the §4 deadlock: two producers, a ring of two, and a consumer that takes the mutex. Attach `gdb` to all three and show, from the backtraces alone, which semaphore each is parked on. Then remove the consumer's mutex and show that the same producer code now completes.
4. Reproduce the §6 chunk sweep with the ring at 8 slots instead of 1. Where does the crossover move to, and why does it move in that direction?
5. `sem_getvalue` on a contended semaphore may return a negative number on some systems and 0 on Linux. Check yours, then say why the value is nearly useless for making a decision.
6. Time `sem_wait`/`sem_post` uncontended against `pthread_mutex_lock`/`unlock` uncontended. Explain the result with reference to what each one does when it does *not* have to sleep.
7. A named semaphore is left over from a crashed run, with value 0. Every subsequent run hangs. Find it, and write the two-line program that repairs it. Then say what a robust program should have done instead.

---

*PROG 201 · Week 2 · L09 · © CSE Department*
