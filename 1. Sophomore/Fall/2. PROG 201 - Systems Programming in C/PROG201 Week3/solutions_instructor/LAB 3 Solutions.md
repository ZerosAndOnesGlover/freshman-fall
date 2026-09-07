# PROG 201 · Lab 3 Solutions
## Priority Inversion, and Its Fix — Instructor Only

---

**Do not distribute.** The lab turns on the students discovering for themselves that `PTHREAD_PRIO_INHERIT` does nothing; a student who has read this has nothing left to find.

**Machine these numbers came from:** Linux 7.0.0-30-generic, gcc 13.3.0 (Ubuntu 24.04), glibc 2.39, Intel i5-8250U, **`RLIMIT_RTPRIO` 0/0**. Every figure below is from a run with nothing else on the machine; the chunked rows are noticeably noisier than the others and that is Q6.

> **The lab is sat 15:00–16:50 on the Monday of Week 4 and Midterm 1 is at 18:00 the same day.**
> That is the registry's calendar, not an error in the lab sheet. In practice: keep to time, and
> do not let the checkoff queue run past 16:50.

---

## 1. The Four TODOs

The scaffolding — `now`, `pin`, `work`, the calibration line, `main`'s argument parsing — is unchanged from the skeleton.

```c
static void *low(void *arg)
{
    (void) arg;
    pin();
    setpriority(PRIO_PROCESS, 0, low_nice);
    for (int c = 0; c < chunks; c++) {
        pthread_mutex_lock(&lock);
        low_has_lock = 1;
        work(WORK_UNITS / chunks);
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

static void *high(void *arg)
{
    double *out = arg;
    pin();
    setpriority(PRIO_PROCESS, 0, 0);
    while (!low_has_lock) sched_yield();     /* let L get there first */
    double t0 = now();
    pthread_mutex_lock(&lock);
    *out = now() - t0;
    pthread_mutex_unlock(&lock);
    return NULL;
}

static void *medium(void *arg)
{
    (void) arg;
    pin();
    setpriority(PRIO_PROCESS, 0, 0);
    while (!stop) { volatile unsigned long x = 0; for (int i = 0; i < 100000; i++) x++; }
    return NULL;
}

/* in main(), replacing TODO 4 */
    if (pi) {
        int rc = pthread_mutexattr_setprotocol(&a, PTHREAD_PRIO_INHERIT);
        if (rc) fprintf(stderr, "setprotocol: %s\n", strerror(rc));
    }```

Builds clean under `gcc -Wall -Wextra -O2 -g -std=c11 -o inversion inversion.c -lpthread`.

---

## 2. Where Students Get Stuck

| # | Symptom | Cause | What to say |
| --- | --- | --- | --- |
| 1 | Baseline reports a wait of ~0.000 s | H reached the mutex before L did | "Whose lock are you timing? What guarantees L got there first?" — the `low_has_lock` spin |
| 2 | Part C shows no inversion, wait ≈ baseline | `work()` rewritten as a `sleep` or a wall-clock loop | The header comment says this. Starving a *timed* loop changes nothing |
| 3 | Part C shows no inversion, threads scattered | `pin()` dropped, or called from `main` instead of each thread | Eight cpus, three burners: nobody starves. Affinity is per-thread |
| 4 | Everything is fast and the burners never stop | `stop` not `volatile`, so the burner loop is optimised into `while(1)` | Real bug, real lesson — worth two minutes on the board |
| 5 | `./inversion m chunks=100` seems to hang | It is not hung. Wall clock is ~100 s in **every** `m` run — L still has to finish | The reported wait is H's, not the program's |
| 6 | H's wait is negative or `-1.000` | `high` did not write through `arg` | It is a `double *`, not a return value |

**Symptom 5 costs more lab time than everything else combined.** Say it at the start: every `m` run takes about a hundred seconds no matter what the answer turns out to be.

---

## 3. Reference Measurements

**Part A — `./rtcheck`**

```
RLIMIT_RTPRIO: soft=0 hard=0
RLIMIT_NICE  : soft=0 hard=0
sched_setscheduler(SCHED_FIFO, 10) -> -1, errno=Operation not permitted
pthread_mutexattr_setprotocol(PRIO_INHERIT) -> 0
pthread_mutex_init with that attribute      -> 0
protocol reads back as 1 (NONE=0 INHERIT=1 PROTECT=2)
```

**Parts B, C, D**

| configuration | H waited |
| --- | --- |
| no burners (baseline) | 0.489 / 0.495 / 0.488 s |
| **3 burners, nice 19, 1 chunk** | **100.607 s** |
| 3 burners + `PRIO_INHERIT` | 100.392 s |
| 3 burners, nice 0, 1 chunk | 1.946 / 1.947 / 1.941 s |
| 3 burners, nice 19, 100 chunks | 0.534 / 0.487 / 0.899 s |
| 3 burners, nice 19, 1000 chunks | 0.403 / 0.261 / 1.681 s |
| 3 burners, nice 0, 100 chunks | 0.012 / 0.012 / 0.015 s |

Calibration is 0.484–0.541 s across runs.

**A note on the chunked rows.** An earlier set taken while other work was on the machine gave 1.676 s at 100 chunks and **13.647 s** at 1,000 — the same binary, the same arguments. The chunked configuration is sensitive to what else is running in a way the others are not, for the reason in Q6. **Do not treat a student's outlying chunked number as a mistake**; ask what else was on their machine, and treat the question as answered if they can say.

---

## 4. Answers

**Q1 — what a lock promises.**

**A lock promises that you will get it after the current holder releases it — nothing about when that is.** H is entitled to complain that L's critical section is long; it is not entitled to complain that it waited for it. Part B's 0.49 s is the honest price of sharing, and everything Part C adds on top is the bug.

Full marks for any phrasing that separates *the length of the critical section* (a property of the program) from *the wait* (a property of the schedule). [Marked in the session — accept it spoken.]

**Q2 — the arithmetic.**

Ours: calibration ≈ 0.49 s, Part C 100.607 s, **ratio 206×**.

CFS weights: nice 0 → 1,024, nice 19 → 15. L's share on one cpu is 15/(15 + 3×1024) = 0.00487, so 0.49/0.00487 ≈ **100.6 s**. The prediction and the measurement agree to two significant figures, which is better than this kind of arithmetic usually manages and is worth pointing out.

Common cause of disagreement: a laptop on battery with a low `energy_performance_preference`, or a browser on cpu 0. Ask what `top` said.

**Q3 — why raising H's priority does not help.**

**H is not runnable.** It is blocked on a futex inside `pthread_mutex_lock`, so it is not competing for the cpu at all and its priority never enters a scheduling decision. Priority determines who runs among the *runnable*; H's problem is that the thread it is waiting for is not among them.

This is the most commonly half-answered question of the six. "Because H is waiting" is [1]; naming *runnable* is the mark.

**Q4 — why `PRIO_INHERIT` did nothing.**

Priority inheritance boosts the lock holder's **realtime priority**, using the kernel's `rt_mutex` machinery, which orders waiters by realtime priority. A `SCHED_OTHER` thread has **no realtime priority** — its nice value is not one — so there is nothing to inherit and the boost is a no-op.

And it cannot be fixed here: Part A shows `RLIMIT_RTPRIO` is **0/0**, so `sched_setscheduler(SCHED_FIFO)` returns `EPERM` and the threads cannot be given a realtime priority in the first place.

Full marks require **both halves**: what PI boosts, and why this program has none of it. A student who says only "you need `SCHED_FIFO`" has half of it and should be asked the other half out loud.

*(For the curious: `/etc/security/limits.d/25-pw-rlimits.conf` on these machines gives the `pipewire` group `rtprio 95`, because audio has deadlines. The mechanism is present and configured for somebody; students are not in that group. If a student asks to be added, the answer is no, and the reason — an unprivileged `SCHED_FIFO` thread in a spin loop wedges a core — is a better lesson than the demonstration would have been.)*

**Q5 — faster than the baseline.**

**H needs the lock exactly once.** In the baseline it arrives while L holds the lock for the whole 0.49 s, so it waits out the entire critical section. With 1,000 chunks the lock is free between every pair of chunks, and H takes it at whichever gap it is next scheduled into — which is on average much sooner than the end.

The lesson is that *contention is about the distribution of hold times, not their sum*. L does the same total work in both cases.

**Q6 — where the variance comes from.**

**In the equal-priority fix H is waiting; in the chunked fix H is racing.** With one long critical section, H's wait is determined by how fast L can finish — a quantity the scheduler fixes deterministically from the weights, hence 1.946/1.947/1.941. With a thousand short ones, H's wait depends on which gap it happens to be scheduled into against three burners, which is a lottery, hence 0.261 to 1.681.

The second half — which would you want with a deadline — should get: **the reproducible one**. A worst case of 1.947 s that you can compute beats an average of 0.7 s with an unknown tail, because a deadline is a statement about the tail. Accept the opposite answer if it is defended by "and I would then bound the tail by *also* shortening the critical section", which is the row that gives 0.012 s.

**This is the best question on the paper.** It is the difference between throughput thinking and latency thinking, and Week 5's server is the same argument again.

**Q7 — the spinlock.**

On a single cpu, H spins holding the cpu, so L — which needs that cpu to finish its critical section and release the lock — never runs. H spins until its timeslice ends, and with L at nice 19 against three nice-0 burners it may be a very long time. Nothing is blocked in the kernel's sense and no progress is made: this is a **livelock**, and it is strictly worse than the mutex version, which at least lets L run.

Accept "spin-then-block would help" as an extra remark; `pthread_mutex` with `PTHREAD_MUTEX_ADAPTIVE_NP` already does that.

**Q8 — Part A as a prediction.**

Part A said `RLIMIT_RTPRIO` is 0 and `SCHED_FIFO` is refused. **Since priority inheritance acts on realtime priorities, a machine that refuses realtime priorities cannot deliver priority inheritance** — so the Part D result was predictable before a line of Part C was written, and the four lines that returned 0 were never evidence of anything.

One sentence, and the point of the whole lab. Students who wrote a real prediction in Part A should be told so.

---

## 5. Checkoff

The four boxes are in the lab sheet. In practice:

- **Ask Q3 and Q4 out loud** even where they are written. Q3 separates students who have understood "runnable" from students who have memorised "priority".
- **Look at their Part A notes.** If they wrote nothing down, that is the finding — say so, kindly, and point at Q8.
- The extension (find the shortest critical section that still shows a visible inversion) is a good use of a fast student's last twenty minutes, and their number is worth collecting: across the section it makes a distribution, and the spread in it is Q6 again.

**Timing.** Setup and Part A, 15 minutes. Part B, 25. Part C is one 100-second run and 20 minutes of arithmetic. Part D is four runs, two of them 100 seconds — **start them and discuss while they run**. That leaves 15 minutes for checkoff, and the room must be clear by 16:50 because the midterm is at 18:00.

---

*PROG 201 · Week 3 · Lab 3 Solutions · Instructor Only · © CSE Department*
