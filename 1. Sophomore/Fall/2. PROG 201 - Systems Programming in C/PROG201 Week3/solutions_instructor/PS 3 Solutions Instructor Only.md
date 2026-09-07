# PROG 201 · PS 3 Solutions
## Implement a Thread Pool — Instructor Only

---

**Do not distribute.** Q3, Q4 and Q5(a) are measurements the students must take themselves.

**Machine these numbers came from:** Linux 7.0.0-30-generic, gcc 13.3.0 (Ubuntu 24.04), glibc 2.39, Intel i5-8250U — **4 physical cores, 8 hardware threads**. The core count is load-bearing for Q3(c); a student on a 2-core laptop should find their peak at 2, and that is the correct answer for their machine.

---

## Reference Solution — `pool.c`

Builds clean under `gcc -Wall -Wextra -O2 -g -std=c11 -o pool pool.c -lpthread`.

```c
/* PROG 201 -- PS 3 reference solution: a fixed-size thread pool.
 *
 *   ./pool pool  100000 4 100      # 100,000 tasks, 4 workers, 100 units each
 *   ./pool spawn 100000 4 100      # one thread per task, for comparison
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <time.h>
#include <unistd.h>

/* ------------------------------------------------------------------ pool -- */

typedef void (*task_fn)(void *);

struct task { task_fn fn; void *arg; };

struct pool {
    pthread_mutex_t  lock;
    pthread_cond_t   not_empty;      /* workers wait here for work        */
    pthread_cond_t   not_full;       /* submitters wait here for room     */
    pthread_cond_t   idle;           /* pool_drain waits here             */
    struct task     *ring;
    unsigned         cap, head, tail, count;
    unsigned         busy;           /* workers inside a task             */
    int              shutdown;
    pthread_t       *workers;
    unsigned         nworkers;
};

static void *pool_worker(void *arg)
{
    struct pool *p = arg;
    for (;;) {
        pthread_mutex_lock(&p->lock);
        while (p->count == 0 && !p->shutdown)
            pthread_cond_wait(&p->not_empty, &p->lock);
        if (p->count == 0 && p->shutdown) { pthread_mutex_unlock(&p->lock); break; }

        struct task t = p->ring[p->tail];
        p->tail = (p->tail + 1) % p->cap;
        p->count--;
        p->busy++;
        pthread_cond_signal(&p->not_full);
        pthread_mutex_unlock(&p->lock);

        t.fn(t.arg);                          /* run OUTSIDE the lock */

        pthread_mutex_lock(&p->lock);
        p->busy--;
        if (p->busy == 0 && p->count == 0) pthread_cond_broadcast(&p->idle);
        pthread_mutex_unlock(&p->lock);
    }
    return NULL;
}

static struct pool *pool_create(unsigned nworkers, unsigned cap)
{
    struct pool *p = calloc(1, sizeof *p);
    p->ring = calloc(cap, sizeof *p->ring);
    p->cap = cap;
    p->nworkers = nworkers;
    p->workers = calloc(nworkers, sizeof *p->workers);
    pthread_mutex_init(&p->lock, NULL);
    pthread_cond_init(&p->not_empty, NULL);
    pthread_cond_init(&p->not_full, NULL);
    pthread_cond_init(&p->idle, NULL);
    for (unsigned i = 0; i < nworkers; i++)
        pthread_create(&p->workers[i], NULL, pool_worker, p);
    return p;
}

static void pool_submit(struct pool *p, task_fn fn, void *arg)
{
    pthread_mutex_lock(&p->lock);
    while (p->count == p->cap && !p->shutdown)
        pthread_cond_wait(&p->not_full, &p->lock);
    if (p->shutdown) { pthread_mutex_unlock(&p->lock); return; }
    p->ring[p->head] = (struct task){ fn, arg };
    p->head = (p->head + 1) % p->cap;
    p->count++;
    pthread_cond_signal(&p->not_empty);
    pthread_mutex_unlock(&p->lock);
}

static void pool_drain(struct pool *p)                /* wait for quiet */
{
    pthread_mutex_lock(&p->lock);
    while (p->count > 0 || p->busy > 0)
        pthread_cond_wait(&p->idle, &p->lock);
    pthread_mutex_unlock(&p->lock);
}

static void pool_destroy(struct pool *p)
{
    pthread_mutex_lock(&p->lock);
    p->shutdown = 1;
    pthread_cond_broadcast(&p->not_empty);
    pthread_cond_broadcast(&p->not_full);
    pthread_mutex_unlock(&p->lock);
    for (unsigned i = 0; i < p->nworkers; i++) pthread_join(p->workers[i], NULL);
    pthread_mutex_destroy(&p->lock);
    pthread_cond_destroy(&p->not_empty);
    pthread_cond_destroy(&p->not_full);
    pthread_cond_destroy(&p->idle);
    free(p->ring); free(p->workers); free(p);
}

/* ------------------------------------------------------------------ main -- */
```

The driver (`job`, `main`) is the obvious part and is omitted; the `spawn` mode is `pthread_create` + `pthread_join` per task in a loop.

---

## Q1 — The Pool (32)

**(a) [20]** Marks: two condition variables **[3]**, `while` on both waits **[4]**, **the task called outside the lock [5]**, `pool_submit` blocking rather than growing **[3]**, workers joined and all primitives destroyed **[3]**, pthreads error handling **[2]**.

The five-mark item is the one to look for first. **A pool that calls `t.fn(t.arg)` while holding `p->lock` is serial**, and it is not obvious from reading — the code looks right, the tasks all run, the answers are correct. Q3(c) is designed to catch it: the worker sweep will be flat, and the 8-worker row will be no better than the 1-worker row.

**(b) [8]** The reference tracks `p->busy`, incremented by the worker under the lock **before** it releases the lock to run the task and decremented under the lock afterwards; `pool_drain` waits on a third condition variable, `idle`, for `count == 0 && busy == 0`.

Marks: the extra counter **[3]**, updated under the lock by the worker **[2]**, `pool_drain` testing *both* conditions **[2]**, the re-entrancy answer **[1]**.

The common wrong answer is to wait for `count == 0` only, which returns while four tasks are still running. Ask for a task that sleeps 100 ms and a `pool_drain` immediately after submitting one.

On a task submitting another task: the reference works, because the new task increments `count` under the same lock before `busy` drops. **A student who says "my drain would return early if a task submits from inside a task" and explains why deserves the mark even if they did not fix it** — recognising the hazard is what is being tested.

**(c) [4]** The constraint: **`pool_destroy` must not free the queue or destroy the mutex until every worker has been joined**, because a worker may still be inside `pthread_cond_wait` on a condition variable in that memory. `pthread_cond_destroy` on a condition variable somebody is waiting in is undefined behaviour, not an error.

A submitter blocked in `pool_submit` must be woken: the reference sets `shutdown` and **broadcasts `not_full` as well as `not_empty`**, and `pool_submit` re-checks `shutdown` after waking and returns without queueing. Students who broadcast only `not_empty` have a program that hangs on shutdown under load — worth running with a queue capacity of 2 and eight submitters to expose it.

---

## Q2 — Shutdown (18)

**(a) [8]** Either policy is acceptable with a clear statement of which **[4]**. The reference drains: workers exit only when `count == 0 && shutdown`.

For the other direction: abandon needs the worker's loop condition to become `while (!shutdown && count == 0)` and then `if (shutdown) break;` regardless of `count` — a two-line change, and the interesting part of the answer is that **the queue's remaining `arg` pointers now leak unless the pool knows how to free them**, which is why real pools take a destructor alongside the task function. Award the last marks for noticing the ownership question.

On `pthread_cancel` **[4]**: cancellation only takes effect at a **cancellation point**, so a task in a compute loop with no syscalls is never cancelled — and a task that *is* cancelled is cancelled wherever it happens to be, possibly holding a lock or half-way through a `malloc`. Cleanup handlers exist (`pthread_cleanup_push`) and are effectively impossible to get right through arbitrary user code. **The pool does not own the task's invariants, so it cannot safely interrupt it.** That sentence is the full-mark answer.

**(b) [6]** The loop:

```c
while (p->count == 0 && !p->shutdown)
    pthread_cond_wait(&p->not_empty, &p->lock);
if (p->count == 0 && p->shutdown) break;
```

A single flag test after the wait is not enough for the reason L11 §4 measured: **the wakeup may have been stolen** — another worker took the task — so the predicate must be re-tested under the lock, and the condition being tested is a disjunction of two independent things.

Shutdown must use **`broadcast`**: every worker has to see it, and `signal` wakes one, which exits, and the rest sleep forever. Marks: the loop **[3]**, why not a flag test **[2]**, broadcast and why **[1]**.

**(c) [4]** Any defended behaviour. The reference returns silently, which is defensible but weak; **the best answers return an error or abort**, on the grounds that submitting to a destroyed pool is a bug in the caller and silence hides it. Full marks require the code to actually implement the stated choice — check it.

---

## Q3 — Measure It (20)

**(a) [6]** Reference, 100,000 tasks, 4 workers:

| work per task | thread-per-task | pool | speedup |
| --- | --- | --- | --- |
| 0 units | 35,529 tasks/s | 1,620,449 tasks/s | **45.6×** |
| 100 units | 35,721 tasks/s | 1,271,398 tasks/s | 35.6× |
| 10,000 units | 20,518 tasks/s | 150,009 tasks/s | 7.3× |

**(b) [6]** 35,529 tasks/s is **28.1 µs per task**, against L10 §3's measured 29.21 µs for `pthread_create` + `pthread_join` — **agreement within 4%**. Marks: the conversion **[2]**, the comparison as a percentage **[2]**, the explanation **[2]**.

The explanation: the `spawn` row barely moves from 0 to 100 units because **100 units of work is roughly 16 µs and the thread costs 28 µs**; the task was never the cost. The real number in that row is the thread creation, and the task is noise on top of it.

**(c) [8]** Reference sweeps:

| workers | 10,000 units, tasks/s | 0 units, tasks/s |
| --- | --- | --- |
| 1 | 57,141 | 4,104,725 |
| 2 | 91,682 | 2,372,114 |
| **4** | **166,952** | 1,263,415 |
| 8 | 96,045 | 805,352 |
| 16 | 95,720 | — |

- **The peak is at 4**, which is the number of *physical cores* — not the eight hardware threads. Eight workers is **42% worse** than four. A student whose machine peaks elsewhere should identify their own core count; the mark is for making the connection, not for the number 4.
- **The second sweep has no peak because it is not measuring parallelism.** With no work in a task, the only thing happening is enqueue and dequeue, so the pool is a benchmark of one mutex and two condition variables — and a lock gets slower with every thread added to it. One worker beats eight by 5×.
- **A first sweep that peaks at 1 worker means the task is being run under the queue lock** (Q1(a)). The tell is that adding workers never helps *and* the 1-worker number is no worse than the correct implementation's 1-worker number — the pool is correct, it is just serial.

Marks: two tables **[3]**, the peak identified with its cause **[2]**, the second sweep explained **[2]**, the diagnostic **[1]**.

---

## Q4 — The Condition Variable Questions (16)

**(a) [6]** The expected report is that **nothing goes wrong**, or that it goes wrong rarely and unrepeatably.

**The correct answer is (2).** The `if` version is incorrect and this test does not reliably reach the failure — L11 §4 measured 7.12% of wakeups arriving with the predicate false, so a failure is *available* on every run, but whether it produces a visible symptom depends on what the worker does with a `NULL` task pointer, and a pool whose queue is usually non-empty rarely exercises it.

**Full marks require (2) with the reasoning.** (3) is generous to their own evidence; (1) is the mistake the whole course is trying to prevent, and it is the same mistake as PS 2 Q1(c). **Students who answer (1) here after answering (3) correctly in PS 2 should be shown both papers side by side** — it is the most useful two minutes of feedback available this term.

**(b) [6]** The program **wedges**, exactly as `onecv.c` does in L11 §5: a submitter's "there is room now" wakeup is delivered to another submitter, who finds the queue still full and sleeps again.

The word: **hides**. `broadcast` makes the symptom go away by waking everybody, so the right thread is always among them — but the program still has one condition variable standing for two different predicates, every wakeup is *O(waiters)* instead of *O(1)*, and the next person to add a third predicate will reintroduce the hang. **The bug is the merged condition variable; `broadcast` is a mitigation.** Marks: the observation **[2]**, the wrong-waiter explanation **[2]**, "hides" with a defence **[2]**.

**(c) [4]** The reference signals **with the mutex held**.

The argument for signalling *after* unlocking: the woken thread immediately needs the mutex, and if you still hold it the wakeup is followed by an immediate block — the "hurry up and wait" problem, and the reason the folklore says to unlock first.

The argument for holding it, which is the right one for a bounded queue: **glibc requeues rather than waking** (L11 §5), so the pathology the folklore describes does not occur; and more importantly, releasing the mutex before signalling opens a window in which the queue's state can change again — with several producers and consumers you can signal a condition that is no longer true. **Correctness first; the cost is not real here.** Accept either choice with a real argument; award nothing for "the book says so".

---

## Q5 — Two Bugs With No Bug In Them (14)

**(a) [6]** Reference for the effect in isolation (`falseshare.c`, L12 §6): four threads, four counters, stride varied:

```
  stride      bytes    seconds    vs best
       1          8     0.1255      1.55x
       2         16     0.1253      1.55x
       4         32     0.1193      1.47x
       8         64     0.0809      1.00x
      16        128     0.0814      1.01x
```

In a real pool the effect is smaller and noisier — the queue mutex dominates — so **accept any measurement with the right sign, and accept "no measurable difference" if the student says what else was in the way.** The marks are for the explanation.

The explanation: the counters share a **64-byte cache line**, so an increment by any thread invalidates the line in the other three cores' caches and the line ping-pongs. Nothing is shared logically and everything is shared physically.

`sysconf(_SC_LEVEL1_DCACHE_LINESIZE)` because 64 is not universal — Apple's M-series use 128 for some levels, and a program that hard-codes 64 pads correctly on one machine and not another. Marks: numbers **[2]**, the name and mechanism **[3]**, `sysconf` **[1]**.

**(b) [4]** For I/O-bound tasks the pool should be sized well above the core count, because a worker blocked in `read` is not using a core.

The formula (Little's law, or the "blocking coefficient" form):

```
    threads  =  cores  x  (1 + wait_time / service_time)
```

With 10 ms of wait and, say, 0.1 ms of CPU per task on 4 cores, that is 4 × 101 ≈ 400 workers. **The quantity to measure is the ratio of blocked time to CPU time per task**, which is what `time` gives you as (real − user − sys) / (user + sys). Marks: "more than `nproc`" with a reason **[2]**, a formula **[1]**, naming the measurable ratio **[1]**.

**(c) [4]** Any workload where tasks are short and numerous enough that the single queue's mutex is the limit — which is exactly the 0-unit sweep in Q3(c), where throughput *falls* with every worker.

**Work stealing**: each worker gets its own deque and pushes and pops its own end with no contention at all; a worker that runs dry steals from the *other* end of another worker's deque. The single point of contention becomes a rare one. Marks: a valid workload **[2]**, the two-sentence description **[2]**. Mentioning that this is what Cilk, TBB, Go and Rust's rayon all do is worth saying back to them but is not required.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | The pool | 32 |
| 2 | Shutdown is the hard part | 18 |
| 3 | Measure it | 20 |
| 4 | The condition variable questions | 16 |
| 5 | Two bugs with no bug in them | 14 |
| | **Total** | **100** |

---

*PROG 201 · Week 3 · PS 3 Solutions · Instructor Only · © CSE Department*
