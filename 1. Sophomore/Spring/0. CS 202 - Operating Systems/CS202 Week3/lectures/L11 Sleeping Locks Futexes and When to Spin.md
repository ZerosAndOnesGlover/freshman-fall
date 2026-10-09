# CS 202 · Operating Systems
## Week 3 · Lecture 2 of 3
### Sleeping Locks, Futexes, and When to Spin

*“We postulate, that inspecting the present value of such a common variable and assigning a new value to such a common variable are to be regarded as indivisible, non-interfering actions.”* — Edsger W. Dijkstra, "Cooperating Sequential Processes" (EWD123, 1965)

---

**Sat:** Wednesday of Week 3, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 28 §28.11–28.15; Drepper, "Futexes Are Tricky" §1–§6 · **Next:** L12, condition variables, semaphores and the classic problems

**Coursework:** 📝 **PS 3** released today, due Fri of Week 4 17:00 · 📝 **PS 2** due Fri this week 17:00 · 📊 **Quiz 4** Mon of Week 4 · 📘 **Midterm 1** Mon of Week 4 18:00–19:15 · 🔬 **Lab 3** Tue of Week 4 15:00–16:50

---

## 1. What a Lock Costs When Nobody Competes

Most locks, most of the time, are **uncontended**: one thread takes it, does its work, and releases it before anyone else arrives. **So the first number that matters is the cost of a lock that nobody else wants.** `lockcost.c`, one thread, pinned, fifty million lock–increment–unlock rounds, best of five:

| Lock | ns per round |
|---|---:|
| no lock | 1.61 |
| `atomic_fetch_add` — one `lock xadd` | 5.41 |
| **`pthread_mutex_lock`** | **7.39** |
| `pthread_spin_lock` | 8.36 |
| futex mutex — §3's | 10.67 |
| test-and-set spinlock — L10 §6's | 10.68 |
| compare-and-swap spinlock | 12.68 |
| `sem_wait` / `sem_post` | 19.05 |

**Every one of them is under 20 ns**, and glibc's mutex is the cheapest lock in the table. **A system call costs 590 ns** (L03 §4). So whatever these locks do when uncontended, **none of them enters the kernel** — and that can be checked directly:

```
$ strace -f -c ./uncont          # 50,000,000 pthread_mutex lock/unlock pairs
100.00    0.000440          12        34         1 total
```

**34 system calls for the whole program** — loading it, mapping libc, writing its one line of output — **and not one `futex`.** Fifty million lock operations happened entirely in ring 3.

---

## 2. Why Not Always Spin?

L10's spinlock is simple and, uncontended, cheap. **Its problem appears when the thread holding the lock is not running** — because it was preempted, or is waiting for I/O. Then every waiting thread spins, burning its CPU, until the holder is scheduled again: **possibly a whole slice, 3 ms, per waiter.**

**The alternative is to sleep**: if the lock is taken, ask the kernel to deschedule you until it is released. That needs the kernel, and the simplest version of it costs a system call on every release — whether or not anyone is waiting:

```c
void lock(void)   { while (atomic_exchange(&v, 1) != 0) futex_wait(&v, 1); }
void unlock(void) { atomic_store(&v, 0); futex_wake(&v, 1); }     /* always */
```

| Two-state lock, always wakes | ns per round | `futex` calls per million rounds |
|---|---:|---:|
| **uncontended** | **638.6** | **1,000,000** |

**Forty-three times the cost of glibc's mutex**, and exactly one system call per unlock — which is what 638 ns is: 590 ns of door and a little work. **A sleeping lock that always tells the kernel is a lock nobody would use.** The trick is knowing *when* the kernel needs to be told.

---

## 3. The Futex

A **futex** — *fast userspace mutex*, added to Linux in 2002–2003 — is not a lock. It is a system call that gives user space two operations on **an ordinary integer in user memory**:

| Operation | Meaning |
|---|---|
| `FUTEX_WAIT(addr, val)` | **if `*addr` still equals `val`**, put me to sleep on `addr`; otherwise return at once |
| `FUTEX_WAKE(addr, n)` | wake up to *n* threads sleeping on `addr` |

**The comparison in `FUTEX_WAIT` is done inside the kernel, atomically with going to sleep.** That is the entire design. It closes the gap in which a thread decides to sleep because the lock is taken, and the lock is released — with a wake-up sent to nobody — before it actually sleeps:

```
$ ./futexlab eagain
FUTEX_WAIT expecting 7 on a value of 5 returned -1, errno EAGAIN: no sleep at all
```

**The value had already changed, so the kernel refused to sleep.** A thread that loses that race simply loops and looks again.

### Drepper's three-state mutex

Ulrich Drepper's paper *Futexes Are Tricky* presents two broken futex mutexes before a correct one. The correct one uses **three values** for the integer:

| Value | Means |
|---|---|
| **0** | unlocked |
| **1** | locked, **and nobody is waiting** |
| **2** | locked, **and somebody may be waiting** |

```c
void futex_acquire(futex_lock *l)
{
    int c = 0;
    if (atomic_compare_exchange_strong(&l->v, &c, 1)) return;   /* 0 → 1: done, no syscall */
    if (c != 2) c = atomic_exchange(&l->v, 2);                  /* mark "someone may wait"  */
    while (c != 0) {
        sys_futex(&l->v, FUTEX_WAIT_PRIVATE, 2);                /* sleep only if still 2    */
        c = atomic_exchange(&l->v, 2);
    }
}

void futex_release(futex_lock *l)
{
    if (atomic_exchange(&l->v, 0) == 2)                         /* was anyone marked?       */
        sys_futex(&l->v, FUTEX_WAKE_PRIVATE, 1);                /* only then, wake one      */
}
```

**The uncontended path is one compare-and-swap to lock and one exchange to unlock** — no system call. **The kernel is entered only when a thread must sleep (the value is 2) and only when a release finds the value was 2.** A woken thread sets the value back to 2 rather than 1, because it cannot know whether other threads are still asleep — occasionally causing an unnecessary wake, never a missed one.

| | Two-state, always wakes | **Three-state** |
|---|---:|---:|
| **uncontended**: ns per round | 638.6 | **14.8** |
| **uncontended**: `futex` calls per million | 1,000,000 | **0** |
| **4 threads contending**: ns per round | 300.2 | **100.3** |
| **4 threads contending**: `futex` calls in 2 million rounds | 2,000,255 | **7,095** |

**Under contention, the three-state lock entered the kernel in 0.35% of its rounds.** Of those 7,095 calls, 2,450 returned an error — almost all `EAGAIN`, the value having changed before the thread could sleep, which is §3's comparison doing its job.

---

## 4. A Lock That Is Almost Right

Here is a natural attempt to avoid the always-wake cost with only two states: **count the waiters in an ordinary variable, and only wake if the count is positive.**

```c
void lock(void)
{
    while (atomic_exchange(&v, 1) != 0) {
        waiters++;                     /* a plain int */
        futex_wait(&v, 1);
        waiters--;
    }
}
void unlock(void) { atomic_store(&v, 0); if (waiters > 0) futex_wake(&v, 1); }
```

`futexlab contended buggy2`, four threads, four million rounds, ten trials:

```
buggy2   HUNG: counter stuck at 1001615 of 4000000 for 2 s, lock value 0, waiters 0
buggy2   HUNG: counter stuck at 1004621 of 4000000 for 2 s, lock value 0, waiters 0
buggy2   HUNG: counter stuck at 1001245 of 4000000 for 2 s, lock value 0, waiters 0
    ... 10 of 10 trials hung
```

**Every trial hung, with the lock free and the waiter count reading zero — and threads asleep forever.** `waiters++` is L10 §1's race: three instructions, updated by several threads with no protection. **Increments are lost, the count drifts below the true number of sleepers, and an unlock that reads 0 skips the wake-up a sleeping thread was depending on.** Once every thread still running has finished its share, the sleepers remain, and nothing will ever wake them.

> **The information that decides whether to wake must live in the same atomic word as the lock.**
> That is what Drepper's value 2 is. Every version of this bug — and there are many in the
> literature — puts the "is anyone waiting?" answer somewhere the lock's atomic operations
> cannot see.

---

## 5. Under Contention

Twenty million increments behind one lock, split among 1, 2, 4 and 8 threads with no pinning:

| ns per increment | 1 | 2 | 4 | 8 |
|---|---:|---:|---:|---:|
| test-and-set spinlock | 14.9 | 65.0 | 167.6 | **263.8** |
| **test-and-*test*-and-set** | 16.7 | 50.7 | 114.3 | **121.6** |
| compare-and-swap spinlock | 15.1 | 70.9 | 160.5 | 247.1 |
| `pthread_spin_lock` | 8.6 | 21.8 | 37.7 | **54.9** |
| futex mutex, three-state | 14.9 | 37.2 | 40.8 | 77.0 |
| `pthread_mutex_lock` | 19.5 | 60.7 | 63.2 | 148.4 |

*(Two runs of the first table differ by a few percent; figures here are from the run that added TTAS and per-thread counters.)*

**Two things to read off it.**

**Test-and-set costs more the more threads wait, and the reason is a write.** A failing `xchg` still *writes* 1 into a lock that is already 1, and — as L10 §7 found for the atomic counter — every write drags the lock's cache line to the writing CPU. Eight spinning threads make the line bounce continuously. **Test-and-test-and-set** reads first and only writes when the lock looks free:

```c
if (atomic_load(&l->v) == 0 && atomic_exchange(&l->v, 1) == 0) return;
```

**At 8 threads that one read halved the cost**, from 263.8 to 121.6 ns. glibc's spinlock does better still — by more than a factor of two — and finding out why is Exercise 4.

**And no lock scales.** The best contended figure, 37.7 ns at 4 threads, is still worse than the *unprotected* single-threaded increment's 1.6 ns by a factor of twenty. **Contended locks serialise; the lesson of L10 §7 stands.**

---

## 6. When to Spin, and When to Sleep

Give the critical section real work — a loop of 2,000 iterations, roughly a few microseconds — and run four threads, **first all on one CPU, then on four**:

| µs per increment, 400,000 in total | 4 threads on **1** CPU | 4 threads on **4** CPUs |
|---|---:|---:|
| test-and-test-and-set spinlock | **8.25** | **3.21** |
| `pthread_spin_lock` | **8.06** | **3.19** |
| futex mutex, three-state | 3.15 | 3.93 |
| `pthread_mutex_lock` | 3.24 | 4.13 |

**On one CPU, spinning costs two and a half times as much.** Whenever the holder is preempted mid-section, every waiter spins through a whole slice for a lock that cannot be released until the holder runs again — on this same CPU, which the spinners are occupying.

**On four CPUs, spinning wins by about 20%.** The holder is running on another CPU and will release within microseconds, so a short spin avoids two system calls and a context switch for the waiter.

**The rule both columns teach:** *spin only while the holder is running on another CPU and will finish soon; otherwise sleep.* Real systems implement exactly that:

- **glibc's `PTHREAD_MUTEX_ADAPTIVE_NP`** spins for a bounded number of iterations before falling back to the futex.
- **The Linux kernel's `mutex`** spins *optimistically* — but only while it can see the owner is currently running on some CPU.
- **Kernel spinlocks** are used only for sections so short, or in contexts so constrained — an interrupt handler cannot sleep — that sleeping is either pointless or impossible.

---

## 7. Locks in xv6

**xv6 has two kinds, for exactly §6's two cases.**

**Spinlocks** (`spinlock.c`, L10 §6) protect short sections: the process table, the free-page list, the console. Interrupts are off while one is held, so a holder cannot be preempted on its own CPU — **which is what makes spinning acceptable in xv6**: a holder is always running, on some CPU, and will release soon.

**Sleeplocks** (`sleeplock.c`) protect sections that may block — above all the disk buffer cache, where a buffer is held across a disk read that takes milliseconds:

```c
void
acquiresleep(struct sleeplock *lk)
{
  acquire(&lk->lk);
  while (lk->locked) {
    sleep(lk, &lk->lk);
  }
  lk->locked = 1;
  lk->pid = myproc()->pid;
  release(&lk->lk);
}
```

**A sleeplock is a flag protected by a spinlock, plus `sleep`** — L12 §4's condition variable. Spinning for the duration of a disk read would waste milliseconds of CPU; sleeping costs a context switch and nothing else.

**One xv6 lock breaks an otherwise universal rule.** `sched()` must be called holding `ptable.lock`, and `swtch` then runs a *different* process — **which releases the lock**, in `scheduler()` or, for a brand-new process, in `forkret()`. A lock acquired by one process and released by another is normally a bug; here it is what keeps another CPU from picking up the half-switched process. The xv6 book's Chapter 5 calls it out, and so should you when you change the scheduler in Project 1.

**xv6's kernel has 42 call sites of `acquire`.** Every one of them is protecting something L10 §1's race could corrupt — and one of them can be removed to see what.

### Taking the lock out of xv6's page allocator

`kalloc.c` keeps free physical pages in a linked list, protected by `kmem.lock`. **Change one line so the lock is never used**, boot xv6 on two CPUs, and run `allocstress`: four processes that each grow their memory by eight pages, fill every byte with their own letter, check it, and give the pages back, a thousand times.

| Kernel | Run | Result |
|---|---|---|
| **with the lock** | 1 | all four children: **1,000 iterations clean** |
| **without** | 1 | `child 0: CORRUPTION at iteration 12, byte 12288: found 66, wrote 65` — **then two children's `sbrk` failed**, one at iteration 48 |
| **without** | 2 | **`panic: remap`** — the whole kernel |

**Found 66, wrote 65**: child 0 wrote `'A'` into a page and read back `'B'` — **child 1's letter, in child 0's memory.** Two CPUs had popped the same page off the free list at the same instant — L10 §1's load, add, store, on a linked list — and **handed one physical page to two processes.** The failed `sbrk` calls are the list corrupted further, looking empty. **The panic is the same race landing on a page-table page**: the kernel found a mapping already present where it had just allocated a fresh page, and stopped.

**One missing lock, and in the space of two runs: a privacy breach between processes, a false out-of-memory, and a crashed kernel.** None of the three looked like a locking bug.

---

## 8. What to Take Away

1. **Uncontended locks cost 7–19 ns and make no system calls**: 50 million `pthread_mutex` pairs, zero `futex` calls.
2. **A sleeping lock that always wakes costs 639 ns** — a system call per unlock.
3. **A futex is a conditional sleep on a user integer**; `FUTEX_WAIT` refuses to sleep if the value has changed, which closes the lost-wakeup gap.
4. **Drepper's three states — free, locked, contended — cost 14.8 ns uncontended with no system calls**, and entered the kernel in 0.35% of contended rounds.
5. **The "is anyone waiting?" answer must live in the lock's atomic word.** A waiter count kept beside it hung ten runs in ten.
6. **Test-and-test-and-set halves a spinlock's contended cost** by not writing to a held lock.
7. **Spin only while the holder runs elsewhere.** Four threads on one CPU: spinning 8.1–8.3 µs, sleeping 3.1–3.2. On four CPUs: spinning 3.2, sleeping 3.9–4.1.
8. **xv6 spins for short sections with interrupts off, and sleeps across I/O.**

---

## Exercises

1. Modify the three-state lock so that a woken thread sets the value to 1 instead of 2. Construct the interleaving in which a sleeping thread is never woken, then run it under `futexlab`'s watchdog.
2. `lockcost` shows `sem_wait`/`sem_post` at 19.05 ns, over twice a mutex. A semaphore is a counter, not a flag. What does it have to do, uncontended, that a mutex does not?
3. Run `contend mutex 4 4000000` under `strace -f -c` and count `futex` calls. Compare with the three-state lock's. **glibc makes more; suggest two reasons.**
4. **Find out why glibc's `pthread_spin_lock` beats test-and-test-and-set by a factor of two at eight threads.** Disassemble it with `objdump -d /lib/x86_64-linux-gnu/libc.so.6` and read the loop.
5. In xv6, `bread` returns a buffer locked with a sleeplock. Why would a spinlock be *incorrect* there, not merely slow? *(What does `acquire` do to interrupts, and what does a disk read wait for?)*

---

*CS 202 · Week 3 · L11 · © CSE Department*
