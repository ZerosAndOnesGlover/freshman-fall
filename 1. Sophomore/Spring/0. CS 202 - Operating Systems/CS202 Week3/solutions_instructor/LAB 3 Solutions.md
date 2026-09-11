# CS 202 · Lab 3 — Solutions and TA Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Session:** Tuesday of Week 4, 15:00–16:50, BH 210 — **the afternoon after Midterm 1.** **Unmarked** — checked off in the session.

**Read the room.** Half the class slept badly and some of them think the paper went wrong. **Do not discuss the midterm** — marks come back later, and a post-mortem in a lab helps nobody. Get them building in the first ten minutes; the futex lock is satisfying enough to change the mood.

**What the session is for.** Q2 is the idea: **`FUTEX_WAIT` compares before it sleeps**, and every correct futex lock depends on it. Q4 is the craft: three states, and why the woken thread writes 2. Q5 is the warning: a lock that looks like a sensible optimisation and hangs every time.

The reference solution is `solutions_instructor/flock reference (do not distribute).c`. **Do not project it before the 90-minute mark.**

---

## Timing

| Minutes | Part | TA action |
|---|---|---|
| 0–5 | Setup | `./flock eagain` should print EAGAIN — if it hangs, their `flock.c` is not the provided one |
| 5–20 | A — glibc | Quick. Make them compute the percentage |
| 20–30 | B — `FUTEX_WAIT` | Insist on the written lost-wake-up sequence before moving on |
| 30–55 | C — `always2` | The common bug is waiting expecting 0 instead of 1 — hangs immediately |
| 55–85 | D — `drepper3` | **Checkpoint.** Students who set 1 after waking will pass most runs; ask Q4's first bullet before signing off |
| 85–105 | E — `buggy2` | Let them predict first. Almost everyone predicts it works |
| 105–110 | Checkoff | |

---

## Reference `lock` and `unlock`

```c
static void lock(void)
{
    if (kind == 2) {                                        /* drepper3 */
        int c = 0;
        if (atomic_compare_exchange_strong(&v, &c, 1)) return;
        if (c != 2) c = atomic_exchange(&v, 2);
        while (c != 0) { fwait(2); c = atomic_exchange(&v, 2); }
        return;
    }
    /* buggy2 omitted -- provided */
    while (atomic_exchange(&v, 1) != 0)                     /* always2 */
        fwait(1);
}

static void unlock(void)
{
    if (kind == 2) { if (atomic_exchange(&v, 0) == 2) fwake(1); return; }
    atomic_store(&v, 0);                                    /* always2 */
    fwake(1);
}
```

---

## Answers

All figures from the reference machine: i5-8250U, Ubuntu 24.04.4, kernel 7.0.

### Q1 — glibc's mutex

```
mutex, 1 thread(s), 4M: 1 futex calls, 0 errors
mutex, 4 thread(s), 4M: 28393 futex calls, 10542 errors
```

**Uncontended: one `futex` call in four million lock–unlock pairs** — and that one is not the mutex at all: `contend` creates its worker thread and `pthread_join`s it, and **`pthread_join` waits on a futex** for the thread to exit. **The mutex itself made none.**

**Four threads: 28,393 calls in 8,000,000 lock and unlock operations — about 0.35%.** A run-to-run variation of ±20% is normal (an earlier reference run gave 33,426). **What it tells you:** glibc's mutex spends essentially all of its time in user space even under heavy contention, and **enters the kernel only when a thread genuinely has to sleep or be woken**. About a third of the calls return an error — `EAGAIN`, the value having changed before the sleep — which is Q2's comparison working.

**Accept** any percentage computed against either 4 million or 8 million operations, if the student says which.

### Q2 — `FUTEX_WAIT`

```
FUTEX_WAIT expecting 7 on a value of 5 returned -1, errno EAGAIN: no sleep at all
```

**The lost wake-up without the comparison:**

1. Thread T reads the lock word: 1, held. **T decides to sleep.**
2. Before T calls into the kernel, the holder H releases: stores 0 and calls `FUTEX_WAKE`. **Nobody is asleep on the address yet, so the wake is discarded.**
3. T now calls `FUTEX_WAIT` and **sleeps — on a lock that is free, having missed the only wake-up that was ever going to come.** If no other thread takes and releases the lock, T sleeps forever.

**With the comparison**, step 3's `FUTEX_WAIT` sees 0, not the expected 1, returns `EAGAIN` at once, and T loops and takes the lock. **The check and the sleep are atomic inside the kernel** — the futex hash bucket lock is held across both — which is the entire reason futexes work.

**Marking cue:** a student who says "the kernel checks the value" without the sequence has not answered. Require the three steps.

### Q3 — `always2`

| | ns per round | `futex` calls |
|---|---:|---:|
| uncontended, 5M rounds, pinned | **638.6** | **1,000,000 per million rounds** |
| 4 threads contending, 2M rounds | 300.2 | 2,000,255 |

**638 ns ≈ one system call** — L03 §4 measured 590 ns for the crossing — **plus the lock's few nanoseconds of work.** Every unlock calls `FUTEX_WAKE` whether or not anyone is waiting, so an uncontended program pays a system call per round. **Correct: yes. Usable: no** — forty times glibc's mutex for the common case.

**Why contended is *cheaper* per round than uncontended** (students often ask): with four threads on several CPUs, the rounds overlap in time; the figure is wall-clock time divided by all rounds. Each individual unlock still pays its system call.

### Q4 — `drepper3`

| | `always2` | **`drepper3`** |
|---|---:|---:|
| uncontended ns | 638.6 | **14.8** |
| uncontended `futex` calls per million | 1,000,000 | **0** |
| contended ns (4 threads) | 300.2 | **100.3** |
| contended `futex` calls (2M rounds) | 2,000,255 | **7,095** (2,450 errors) |

**Why a woken thread writes 2, not 1.** Suppose three threads: H holds the lock; A and B are both asleep (value 2). H unlocks: value 0, wakes **one** thread — A. **If A takes the lock by writing 1**, the value no longer records that B is asleep. When A unlocks, it exchanges 0 and sees **1**, so it **does not wake anyone** — and B sleeps forever. **Writing 2 costs at most one unnecessary wake-up** (when nobody else was actually waiting) and never loses one.

**The errors** are `EAGAIN`: a thread read 2, but by the time `FUTEX_WAIT` compared, another thread had changed the value. **Harmless** — the thread loops and reads again — and a sign the comparison is doing its job.

**Checkpoint:** `drepper3` uncontended with **0** `futex` calls and a correct counter.

### Q5 — `buggy2`

Reference, five runs:

```
buggy2   HUNG: counter stuck at 1001615 of 4000000 for 2 s, lock value 0, waiters 0
buggy2   HUNG: counter stuck at 1004621 of 4000000 for 2 s, lock value 0, waiters 0
buggy2   HUNG: counter stuck at 1001245 of 4000000 for 2 s, lock value 0, waiters 0
    ... ten of ten reference runs hung
```

**Lock value 0: nobody holds it. Waiters 0: the unlock path believes nobody is waiting. And the counter stopped: threads are asleep in `FUTEX_WAIT`.**

**How it happens.** `waiters++` and `waiters--` are **L10 §1's race** — load, add, store — executed by several threads at once with no protection. **Updates are lost, and the count drifts below the true number of sleeping threads**, eventually to 0 while threads sleep. An `unlock` that reads `waiters == 0` skips `FUTEX_WAKE`. **The sleeper's `FUTEX_WAIT` had compared against 1 and gone to sleep legitimately** — the lock *was* held when it slept — so the comparison does not save it this time. **When the other threads finish their share and exit, no unlock ever happens again**, and the sleepers stay asleep. *(The counter stalling just past 1,000,000 — one thread's quota — is typical: it hangs once the threads still making progress run out.)*

**What Drepper's lock does with that information:** it **keeps "someone may be waiting" inside the atomic lock word itself, as the value 2**, so every lock and unlock that reads or changes it does so atomically with the lock state.

---

## Common Problems

| Symptom | Cause | Fix |
|---|---|---|
| `always2` hangs at once | `fwait(0)` — waiting "if the value is 0", i.e. if the lock is free | wait expecting **1** |
| `drepper3` uncontended makes 1M `futex` calls | `unlock` wakes unconditionally | wake only if the exchange returned **2** |
| `drepper3` occasionally hangs under contention | woken thread writes 1 instead of 2 | Q4's first bullet |
| Counter wrong with `drepper3` | fast path uses `atomic_store(&v, 1)` instead of compare-and-swap | the fast path must be a CAS from 0 |
| `strace -c` shows no `futex` line | not `-f`: the calls are in the worker threads | `strace -f -c` |

---

*CS 202 · Week 3 · Lab 3 Solutions · Instructor Only*
