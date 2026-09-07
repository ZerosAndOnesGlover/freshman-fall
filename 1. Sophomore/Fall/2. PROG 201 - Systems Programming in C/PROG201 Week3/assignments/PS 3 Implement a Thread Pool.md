# PROG 201 · Problem Set 3
## Implement a Thread Pool

---

**Released:** Week 3, Wednesday · **Due:** Week 4, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS3_{LastName}_{StudentID}.pdf`, and your code as `PS3_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine. The write-up and the code must be yours.
>
> **Midterm 1 is on the Monday of Week 4** and covers Weeks 0–3. This problem set is due four days
> after it. **Do not leave Q1 until after the midterm** — Q1 is the best revision for the paper
> that exists, and Q3's numbers take an afternoon.
>
> **Q3 is measurement on your own machine.** State your `gcc --version`, `uname -r`,
> `nproc`, and whether you are on BH 215 or your own hardware.
>
> Everything compiles clean under `gcc -Wall -Wextra -O2 -std=c11`. Warnings cost marks.
> Link with `-lpthread`.

---

### The Program

`pool.c`, a fixed-size thread pool with a bounded task queue:

```c
typedef void (*task_fn)(void *);

struct pool *pool_create(unsigned nworkers, unsigned queue_cap);
void         pool_submit(struct pool *p, task_fn fn, void *arg);
void         pool_drain(struct pool *p);      /* block until nothing is queued or running */
void         pool_destroy(struct pool *p);    /* stop the workers and free everything     */
```

Driven by:

```
./pool pool  100000 4 100      # 100,000 tasks, 4 workers, 100 units of work each
./pool spawn 100000 4 100      # one thread per task, for comparison
```

---

### Q1: The Pool (32 points)

**(a) [20]** Implement the four functions above. The queue is L11 §7's bounded buffer with a
`struct task` in each slot: a mutex, a ring, and **two** condition variables — `not_empty` for
workers waiting for work and `not_full` for submitters waiting for room.

Requirements, each of which is a mark:

- **Every wait is a `while` loop**, not an `if`. L11 §4 measured 7.12% of wakeups arriving with nothing to do; you must not assume a wakeup means a task.
- **The task runs outside the lock.** Take the task, release the mutex, *then* call `t.fn(t.arg)`. A pool that runs tasks under its own queue lock has one worker, whatever `nworkers` says — and Q3(c) will show you exactly that number.
- `pool_submit` blocks when the queue is full rather than dropping or growing.
- Workers are `pthread_join`ed in `pool_destroy`, and every mutex and condition variable is destroyed.
- Pthreads calls **return** their error number. No `perror`, no `if (rc < 0)`.

**(b) [8]** `pool_drain` must return when the queue is empty **and** no worker is still inside a
task. An empty queue is not enough — four workers may each be halfway through something.

Say what state you added to track this, which thread updates it, and under which lock. Then say
what your `pool_drain` does if a task submits another task.

**(c) [4]** Give the exact ordering constraint between `pool_destroy` and the workers, in one
sentence, and say what happens if a submitter is blocked in `pool_submit` when `pool_destroy`
is called. Handle that case in your code.

---

### Q2: Shutdown Is the Hard Part (18 points)

**(a) [8]** There are two reasonable shutdown policies:

1. **Drain** — finish everything already queued, then stop.
2. **Abandon** — stop as soon as the current tasks finish; queued tasks are dropped.

Implement one and say which. Then describe, in three or four sentences, what would have to change
in your code to offer the other, and why a pool cannot reasonably offer a third policy — cancel the
task that is currently running. *(`pthread_cancel` exists. Say why you would not use it here; `man
7 pthreads`, "Cancellation points", is the reading.)*

**(b) [6]** Your workers wait on `not_empty`. Shutdown must wake **all** of them, and each must
then distinguish "no work right now" from "no work ever again".

Write out the exact loop condition your worker uses and explain why a single flag test after
`pthread_cond_wait` is not enough. Name which of `signal` and `broadcast` shutdown must use, and
why. *(L11 §5.)*

**(c) [4]** After `pool_destroy` returns, a caller submits another task. What does your
implementation do? Choose a behaviour, defend it in one sentence, and make the code actually do
that rather than whatever it happens to do.

---

### Q3: Measure It (20 points)

**(a) [6]** Fill in this table on your machine, 100,000 tasks and 4 workers:

| work per task | thread-per-task, tasks/s | pool, tasks/s | speedup |
| --- | --- | --- | --- |
| 0 units | | | |
| 100 units | | | |
| 10,000 units | | | |

**(b) [6]** Your `spawn` row for 0 units gives a tasks/second figure. Convert it to microseconds per
task and compare it with L10 §3's measured `pthread_create` + `pthread_join` cost of **29.21 µs**.
State the agreement as a percentage.

Then explain why the `spawn` row **barely changes** between 0 and 100 units of work, and what that
tells you about which of the two numbers in that row is the real one.

**(c) [8]** Sweep the worker count — 1, 2, 4, 8, 16 — at 10,000 units per task, and again at
0 units. You should get two differently-shaped curves. Report both, then answer:

- Where is the peak in the first sweep, and what number on your machine does it correspond to?
- Why does the second sweep have **no peak at all**, and what is that sweep actually measuring?
- If your first sweep peaks at 1 worker, you have the bug from Q1(a). Which one, and how did the number tell you?

---

### Q4: The Condition Variable Questions (16 points)

**(a) [6]** Replace one `while` in your worker with an `if` and run 100,000 tasks. Report what
happens. If nothing happens, run it ten times and report that instead — then say what you have and
have not established, and which of these your evidence supports:

1. The `if` version is correct on this machine.
2. The `if` version is incorrect and this test does not reach the failure.
3. The `if` version is incorrect and this test shows it.

**(b) [6]** Merge `not_empty` and `not_full` into a single condition variable, keep `signal`, set
the queue capacity to 2, and run four submitters against four workers. Report what happens, and
explain it in terms of which thread receives a wakeup meant for a thread waiting on a different
predicate.

Then say whether switching to `broadcast` **fixes** the program or **hides** the bug, and defend
the word you chose.

**(c) [4]** `pthread_cond_signal` may be called with the mutex held or after releasing it. Your
`pool_submit` does one of the two. Say which, and give the argument for the other. *(`man 3
pthread_cond_signal` has both. There is a right answer for a bounded queue and it is not obvious.)*

---

### Q5: Two Bugs With No Bug In Them (14 points)

**(a) [6]** Give each worker a private `long completed` counter in an array indexed by worker
number, with no lock — which is correct, since no two workers touch the same element. Now run the
0-unit sweep at 4 workers and compare against the same program with each counter padded to 64 bytes
(`_Alignas(64)`).

Report both numbers. Name the effect, explain it in terms of what the hardware does with a cache
line, and say why `sysconf(_SC_LEVEL1_DCACHE_LINESIZE)` is better than writing 64.

**(b) [4]** Your pool's tasks are CPU-bound. Suppose instead each task did a blocking `read` from a
socket taking 10 ms. State how you would size the pool now, and why `nproc` is the wrong answer.
Give the formula and name the quantity you would have to measure to use it.

**(c) [4]** In one paragraph: your pool gives you *N* workers sharing one queue. Name one workload
for which that single queue is the bottleneck, and describe — you do not have to implement it — the
standard structural fix. *(The phrase to look up is "work stealing". Two sentences on what it
changes is enough.)*

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

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*PROG 201 · Week 3 · PS 3 · © CSE Department*
