# PROG 201 · Systems Programming in C
## Week 3 · Lecture 2 of 3
### Mutexes, Condition Variables, and Reader-Writer Locks

*“In each cycle a so-called "critical section" occurs, critical in the sense that the processes have to be constructed in such a way, that at any moment at most one of the two is engaged in its critical section.”* — Edsger W. Dijkstra, "Cooperating Sequential Processes" (EWD123, 1965)

---

**Reading:** APUE §11.6, §12.4 · TLPI Ch. 30 · `man 3 pthread_cond_wait`, `man 3 pthread_rwlock_rdlock` · **Previous:** L10 · **Next:** L12 — priority inversion and thread pools

**Coursework:** 📝 **PS 3** released today, due Fri of Week 4 17:00 · 📝 **PS 2** due Fri this week 17:00 · 🔬 **Lab 3** Mon of Week 4 15:00–16:50 · 📊 **Quiz 4** Tue of Week 4

---

## 1. A Mutex Is Not a Binary Semaphore

They look identical. Week 2 L09 §1 even said a semaphore initialised to 1 "acts as a mutex". It acts as one; it is not one, and the difference is a word: **ownership**.

| | `sem_t` at 1 | `pthread_mutex_t` |
| --- | --- | --- |
| Who may release it | **anyone** | only the thread that locked it |
| Double unlock | increments to 2 — now two threads can enter | undefined, or `EPERM` with `ERRORCHECK` |
| Recursive lock by the owner | deadlock | deadlock, or a count with `RECURSIVE` |
| Can be used as a signal | **yes** — that is what `full`/`empty` were | no |
| Priority inheritance | no | **yes, in principle** (L12) |

**Use a semaphore to count things and a mutex to protect things.** Week 2's ring used semaphores because `empty` and `full` were counts of slots — one thread posts what another waits for, which a mutex cannot express. This week's bounded buffer uses a mutex plus condition variables because the thing being protected is a data structure, and the thing being waited for is a predicate about it.

---

## 2. What Each Primitive Costs

`primcost.c`, 20 million uncontended iterations of each:

| Operation | Cost |
| --- | --- |
| a plain `++` on a `volatile long` | **1.6 ns** |
| `atomic_fetch_add`, `seq_cst` | 5.4 ns |
| `atomic_fetch_add`, `relaxed` | 5.4 ns |
| **`pthread_mutex_lock` + `unlock`** | **8.2 ns** |
| `pthread_spin_lock` + `unlock` | 8.4 ns |
| `pthread_mutex` with `ERRORCHECK` | 11.3 ns |
| `pthread_rwlock_rdlock` + `unlock` | **18.6 ns** |
| `sem_wait` + `sem_post` | 19.2 ns |
| `pthread_rwlock_wrlock` + `unlock` | 28.5 ns |
| `getpid()` through `syscall()`, for scale | 568.4 ns |

Four things in that table are worth an argument.

**An uncontended mutex costs 8.2 ns and makes no system call.** It is a `lock cmpxchg` on a word, and the kernel is involved only when the word is already taken — the `futex` design from Week 2 L09 §3. `strace` a program whose locks are never contended and you will see nothing. **"We removed the mutex for performance" is almost always a claim about the contended case being wrongly attributed to the uncontended one.**

**A spinlock is not faster.** 8.4 ns against 8.2 ns, uncontended — because the fast path of both is the same atomic instruction. A spinlock's difference is entirely in what it does when it *fails*: burn CPU instead of sleeping. That is a win only when the hold time is shorter than a context switch and you have a core to waste, which in userspace is almost never. It is also the primitive most likely to turn a priority inversion into a livelock (L12).

**A reader-writer lock is 2.3× more expensive to take than a mutex**, in the read case, uncontended. It has more state to maintain: a reader count, a writer flag, and a fairness policy. §6 is about when that pays for itself, and the answer is "later than you think".

**`sem_wait`/`sem_post` at 19.2 ns matches Week 2's 19.3 ns** on the same machine, which is the sanity check that these numbers mean something.

---

## 3. A Condition Variable Is Not a Flag

The problem: a consumer must wait until the buffer is non-empty. It cannot test the predicate without the mutex — the buffer is shared. But it cannot hold the mutex while it sleeps, because the producer needs the mutex to make the predicate true.

```c
pthread_mutex_lock(&m);
while (count == 0)          /* must hold m to read count      */
    ??? sleep ???           /* must NOT hold m while sleeping  */
```

**`pthread_cond_wait` is the operation that resolves that**, and it is the only reason condition variables exist:

```c
pthread_cond_wait(&cv, &m);
```

does three things, and the first two are atomic with respect to each other:

1. release `m`,
2. block on `cv`,
3. and on waking, **re-acquire `m`** before returning.

Because (1) and (2) happen together, a producer cannot slip in between them — it cannot take the mutex, change the predicate, and signal the condition before you were listening. That gap is exactly the `pause()` race from Week 0 L03 §7, and `pthread_cond_wait` is `sigsuspend`'s answer to it, in a different vocabulary. **Both exist because "unlock, then sleep" is two operations and the window between them is where the wakeup gets lost.**

Three rules follow, and none is optional:

- **You must hold the mutex when you call `pthread_cond_wait`.** It is undefined behaviour otherwise, and the function has no way to give the mutex back if it never had it.
- **You must hold the mutex when you change the predicate.** Otherwise the reader's test and your write race.
- **You need not hold it to signal** — but see §5.

---

## 4. The Loop, and the 7% That Proves It

Every textbook says to write

```c
while (!predicate)              /* while, never if */
    pthread_cond_wait(&cv, &m);
```

and explains it with *spurious wakeups*, which sound theoretical enough to ignore. Here is the measurement. `cv.c` runs eight consumers and one producer through 200,000 items and counts the wakeups that returned to find the predicate still false:

```
signal     8 consumers, 200000 items: consumed 200000, woke with nothing to do 15321 (7.12%)
broadcast  8 consumers, 200000 items: consumed 200000, woke with nothing to do 13395 (6.28%)
```

**More than one wakeup in fourteen found nothing to do**, with `pthread_cond_signal`, on an ordinary Linux machine, with no signals being delivered.

Be precise about what those 15,321 wakeups are, because two different things are mixed in and only one of them is what POSIX means by "spurious":

- **A stolen wakeup.** The producer signals; consumer A is woken; consumer B — already awake and just entering the mutex — takes the item first. A wakes, re-acquires the mutex, and the queue is empty. Nothing spurious happened; the wakeup was simply overtaken. **This is the common case and it is unavoidable in any design where `signal` does not hand the resource over.**
- **A genuinely spurious wakeup.** POSIX permits `pthread_cond_wait` to return with no corresponding signal at all, and on Linux `futex` waits can return early — an interrupted system call being the usual cause.

**The `while` loop handles both, an `if` handles neither**, and the distinction matters only when you are explaining the code. What matters when you are writing it is that 7% is not a rounding error: an `if` here would consume from an empty buffer 15,321 times per 200,000 items.

---

## 5. `signal` or `broadcast`

The folklore: `broadcast` causes a thundering herd, so prefer `signal`. Both halves of that are worth checking.

**When `signal` is wrong, it is wrong by deadlock, not by slowness.** `onecv.c` is a bounded buffer with capacity 2, four producers, four consumers, and — the mistake — **one condition variable for both waits**: producers wait on it for "not full", consumers wait on it for "not empty".

```
$ ./onecv          # pthread_cond_signal
(wedged; killed after 25 s)

$ ./onecv b        # pthread_cond_broadcast
broadcast produced 80000, consumed 80000 -- finished
```

`signal` wakes **one** waiter, and the implementation does not know or care which predicate that waiter is testing. A consumer signals "there is room now" and the wakeup goes to another consumer, who finds the buffer empty and goes back to sleep. Everybody waits forever. **The bug is not the signal; the bug is one condition variable for two predicates**, and `broadcast` merely papers over it.

The right fix is two condition variables, `not_empty` and `not_full`, which is what the bounded buffer in §7 has and what Week 2's two semaphores were.

**And the herd is cheaper than advertised.** The same 200,000 items:

| | futex calls | wall clock |
| --- | --- | --- |
| `signal` | 423,342 | 0.250 s |
| `broadcast` | 537,988 | **0.138 s** |

Broadcast made **27% more system calls and finished in 55% of the time.** glibc's `pthread_cond_broadcast` does not simply wake everybody: it moves waiters from the condition variable's queue onto the *mutex's* queue (`FUTEX_REQUEUE`), so they wake one at a time as the mutex is released rather than all at once to fight over it.

**So choose on correctness, not on cost:**

- **`signal`** when every waiter is waiting for the same predicate and exactly one of them can proceed.
- **`broadcast`** when waiters are waiting on different predicates, or when one change can satisfy several of them (a state flag flipping, a shutdown, a barrier releasing).

If you cannot say which case you are in, you are in the second one.

---

## 6. Reader-Writer Locks, and When They Lose

A reader-writer lock allows any number of concurrent readers, or one writer. It sounds strictly better than a mutex for read-heavy data, and §2 already showed it costs 2.3× more to take.

`rw.c` runs *N* threads doing nothing but read-lock, a fixed amount of work, unlock — the same workload under a mutex and under an rwlock:

| work held (iterations) | threads | mutex | rwlock | rwlock speedup |
| --- | --- | --- | --- | --- |
| 0 | 2 | 0.1469 | 0.2851 | **0.52×** |
| 0 | 4 | 0.4512 | 0.7670 | **0.59×** |
| 10 | 2 | 0.0292 | 0.0413 | 0.71× |
| 10 | 8 | 0.2487 | 0.1856 | 1.34× |
| 100 | 2 | 0.0320 | 0.0077 | **4.15×** |
| 100 | 8 | 0.0765 | 0.0286 | 2.67× |
| 1000 | 4 | 0.1916 | 0.0590 | **3.25×** |

**With a trivial critical section the reader-writer lock is nearly twice as slow.** Two threads, no work under the lock, and the "concurrency" it offers is worth less than the extra bookkeeping to get it. The crossover on this machine is somewhere between 10 and 100 iterations of held work.

The rule: **a reader-writer lock pays when readers hold the lock long enough to actually overlap.** Looking up one field in a struct is not that. Walking a tree, formatting a page of output, doing a comparison against every element — that is.

Two more properties to know before you reach for one:

- **Writer starvation is permitted.** POSIX does not require a fairness policy. glibc's default lets a stream of readers hold a writer off indefinitely; `pthread_rwlockattr_setkind_np` with `PTHREAD_RWLOCK_PREFER_WRITER_NONRECURSIVE_NP` changes that, at the cost of read throughput.
- **They are not upgradable.** There is no "I have a read lock, give me a write lock" — it would deadlock two threads that both tried. Unlock, take the write lock, and **re-check everything you read**, because the world changed while you held nothing.

---

## 7. The Bounded Buffer, Written Out

Week 2's ring, with condition variables instead of semaphores. This is the shape PS 3's thread pool is built from:

```c
struct buf {
    pthread_mutex_t lock;
    pthread_cond_t  not_empty, not_full;      /* two.  See section 5 */
    item            slot[CAP];
    unsigned        head, tail, count;
};

void put(struct buf *b, item x)
{
    pthread_mutex_lock(&b->lock);
    while (b->count == CAP)
        pthread_cond_wait(&b->not_full, &b->lock);
    b->slot[b->head] = x;
    b->head = (b->head + 1) % CAP;
    b->count++;
    pthread_cond_signal(&b->not_empty);       /* one consumer can proceed */
    pthread_mutex_unlock(&b->lock);
}

item get(struct buf *b)
{
    pthread_mutex_lock(&b->lock);
    while (b->count == 0)
        pthread_cond_wait(&b->not_empty, &b->lock);
    item x = b->slot[b->tail];
    b->tail = (b->tail + 1) % CAP;
    b->count--;
    pthread_cond_signal(&b->not_full);
    pthread_mutex_unlock(&b->lock);
    return x;
}
```

Compare it with Week 2 L09 §4 line by line. The `sem_wait(&empty)` became `while (count == CAP) cond_wait(&not_full)`; the `sem_post(&full)` became `cond_signal(&not_empty)`. **The semaphore version needed no mutex at all** for one producer and one consumer, because the counts were the synchronisation. This version needs one, because the predicate is a field somebody else can change — but in exchange the predicate can be anything you can write in C, which a semaphore's counter cannot.

**That is the whole trade between the two.** Semaphores are cheaper and less expressive; condition variables let the waiting condition be arbitrary, and charge you a mutex for it.

---

## 8. Deadlock, and the Cheap Way to Catch It

Two mutexes, two threads, opposite orders — the textbook deadlock, and unlike Week 2's semaphore ordering (which turned out not to deadlock at all unless the consumer also took the lock), this one really does:

```c
/* thread A */                     /* thread B */
pthread_mutex_lock(&m1);           pthread_mutex_lock(&m2);
pthread_mutex_lock(&m2);           pthread_mutex_lock(&m1);
```

**Impose a total order on your locks and always take them in it.** Address order works and needs no thought: `if (a < b) { lock(a); lock(b); } else { lock(b); lock(a); }`.

Two tools worth the eight lines it takes to enable them:

- **`PTHREAD_MUTEX_ERRORCHECK`** turns "lock a mutex you already hold" from a silent self-deadlock into `EDEADLK`, and "unlock one you do not hold" into `EPERM`. It costs 11.3 ns against 8.2 (§2) — **38% more on an operation that is 8 ns**, which is nothing. Use it in development.
- **`pthread_mutex_trylock`** returns `EBUSY` instead of blocking, which lets you write a back-off: take the second lock with `trylock`, and if it fails, release the first and start over. Slower and always correct, whatever the order.

And one that costs nothing at all: **`gdb`'s `thread apply all bt`.** A deadlocked program's backtrace names both mutexes and both holders, and the cycle is visible in twenty seconds.

---

## Summary

- A mutex has an **owner**; a semaphore does not. Count with semaphores, protect with mutexes.
- **Uncontended: mutex 8.2 ns, spinlock 8.4 ns, rwlock read 18.6 ns, semaphore 19.2 ns, atomic 5.4 ns.** No system call in any of them.
- `pthread_cond_wait` **atomically releases the mutex and blocks**, then re-acquires on wake. That atomicity is the entire point, and it is the `pause()` race from Week 0 solved again.
- **Always `while`, never `if`** — 7.12% of wakeups found nothing to do, from stolen wakeups and genuinely spurious ones together.
- **One condition variable for two predicates plus `signal` is a deadlock**, measured. Two predicates need two condition variables.
- glibc's `broadcast` **requeues** rather than stampedes: 27% more futex calls and 55% of the wall clock. Choose on correctness.
- A reader-writer lock is **0.52× a mutex** with a trivial critical section and **4.15×** with a long one. It pays only when reads actually overlap. Writers may starve; locks do not upgrade.
- Order your locks. `ERRORCHECK` costs 3 ns and catches self-deadlock.

---

## Exercises

1. Rewrite §7's bounded buffer with one condition variable and `broadcast`. Measure it against the two-variable version at 2, 4 and 8 consumers. Where does the difference come from?
2. Change the `while` in `get` to an `if` and run `cv.c`'s workload. How long before it consumes from an empty buffer, and what does it read?
3. Build the two-mutex deadlock, attach `gdb`, and produce a backtrace that names both mutexes. Then fix it by address ordering and confirm.
4. Measure `pthread_mutex_lock` under contention: 2, 4 and 8 threads locking and unlocking with nothing inside. Plot it against §2's 8.2 ns and explain the shape.
5. Take a read lock and then try to take the write lock in the same thread. What happens, and what does `man 3 pthread_rwlock_wrlock` say about it?
6. Set `PTHREAD_RWLOCK_PREFER_WRITER_NONRECURSIVE_NP` and re-run `rw.c`. Which rows change, and by how much?
7. `pthread_cond_signal` may be called with or without the mutex held. Write both, measure both, and find the argument (it is in `man 3 pthread_cond_signal`) for each.

---

*PROG 201 · Week 3 · L11 · © CSE Department*
