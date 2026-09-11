# CS 202 · Problem Set 3
## A Mutex from Compare-and-Swap, and Five Philosophers

---

**Released:** Week 3, Wednesday · **Due:** Week 4, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS3_{LastName}_{StudentID}.pdf`, plus your three `.c` files in a tarball `PS3_{LastName}.tar.gz`

> **Midterm 1 is on the Monday of Week 4**, between this problem set's release and its deadline,
> and covers Weeks 0–3. **Q1, Q2 and Q5 are good revision for it**; Q3 and Q4 can wait until after.
>
> Collaboration: discussing approaches is fine and encouraged. The write-up and the code must be
> yours. State at the top: *"I worked on this problem set independently"* or name who you discussed
> which question with.
>
> **Every measured answer requires output from your own machine.** State your CPU model, core count,
> `uname -r` and `gcc --version` at the top. Where a question says **predict first**, write the
> prediction down before running anything, and report both.
>
> Every file you submit compiles clean under `gcc -O2 -Wall -Wextra -pthread`.

**Files provided** in `assignments/ps3/`. Each has a working harness and `TODO`s for you:

| File | Yours to write | Provided |
|---|---|---|
| `casmutex.c` | `cas_mutex_lock`, `cas_mutex_unlock` | the benchmark; `pthread` and `broken` locks for comparison |
| `philo3.c` | `pick_up` and `put_down` for `ordered`, `seats` and `waiter` | `naive`; the harness, which counts each philosopher's meals and detects deadlock |
| `rwpref.c` | `my_rdlock`, `my_rdunlock`, `my_wrlock_until`, `my_wrunlock` | the harness: seven readers, one writer, glibc's lock for comparison |

---

### Q1: A Mutex from Compare-and-Swap (30 points)

Implement `cas_mutex_lock` and `cas_mutex_unlock` in `casmutex.c`. **You may not use futexes, `pthread_mutex`, or any lock from glibc.** Your lock must:

- acquire with **compare-and-swap** (`atomic_compare_exchange_weak` or `_strong`), and **test the value before attempting the swap** (L11 §5);
- **spin with `pause` for at most `SPIN_LIMIT` attempts, then call `sched_yield()` between further attempts** — unless the global `yielding` is 0, in which case it spins forever (this is how the harness's `spin` mode compares);
- release with a single atomic store.

**(a) [10]** Your implementation, and a sentence each on why it has **mutual exclusion** and why it has **progress**. *(Bounded waiting is (d).)*

**(b) [12] Predict first**, then run all four, and tabulate `mine`, `spin` and `pthread` in each:

```bash
taskset -c 3   ./casmutex uncontended mine 20000000        # and pthread
taskset -c 2-5 ./casmutex contended mine 4 4000000         # and spin, pthread
taskset -c 2   ./casmutex contended mine 4 400000 2000     # and spin, pthread
taskset -c 2-5 ./casmutex contended mine 8 400000 2000     # and spin, pthread
```

**(c) [5]** For each of the last three rows, **say which lock won and why**, in terms of whether the lock holder was running while others waited. **In the one-CPU row, explain what `sched_yield()` changes** — which thread does the scheduler run instead of the spinner, and why that makes the lock released sooner?

**(d) [3]** Your lock does not have **bounded waiting**. Describe a sequence of events in which one thread waits forever while others keep acquiring it. Does `pthread_mutex` guarantee bounded waiting? *(`man 3 pthread_mutex_lock` does not promise it; say what that means.)*

---

### Q2: A Lock That Is Not Atomic (10 points)

`casmutex.c`'s `broken` lock is:

```c
static void broken_lock(broken_mutex *m)   { while (m->held) sched_yield(); m->held = 1; }
static void broken_unlock(broken_mutex *m) { m->held = 0; }
```

**(a) [3] Predict first**, then run it three times with a timeout, and report what happens:

```bash
for i in 1 2 3; do timeout 20 ./casmutex contended broken 4 40000; echo "exit $?"; done
```

**It does not print a wrong counter.** Find out why: `objdump -d --no-show-raw-insn casmutex` and read `work()` — `broken_lock` has been inlined into it. **Find the loop that calls `sched_yield`, and say what it no longer does.**

**(b) [3]** The compiler was allowed to do that. **Explain why**, using two facts: what the C standard says about a *data race* on an ordinary variable, and what the compiler can prove about who can change `bm` — a `static` variable whose address never leaves the file — during a call to `sched_yield`.

**(c) [2]** Now declare the field `volatile int held` and rebuild. Run it three times and report the counters. **Give the interleaving**, instruction by instruction, in which two threads are both inside the critical section.

**(d) [2]** Replace the test and the set with a single compare-and-swap on an atomic. **Which of L10 §3's three properties does that fix, and which does it not?** Does it also remove the problem in (a), and why?

---

### Q3: Five Philosophers, Measured (30 points)

Implement `ordered`, `seats` and `waiter` in `philo3.c`'s `pick_up` and `put_down`:

| Strategy | Rule |
|---|---|
| `ordered` | pick up the lower-numbered of the two forks first |
| `seats` | a semaphore initialised to 4 must be acquired before touching any fork |
| `waiter` | one mutex and one condition variable: pick up **both** forks at once when both are free, or wait; on putting down, wake the others |

**(a) [9]** Run each of the four strategies three times for 3 seconds (`./philo3 <strategy> 3`) and tabulate: whether it deadlocked, meals per second, and the harness's **fairness ratio** — fewest meals by any philosopher divided by the most.

**(b) [6]** **Prove that `ordered` cannot deadlock.** Your proof should not depend on timing: suppose all five philosophers are blocked, and derive a contradiction from the order in which forks are acquired.

**(c) [6]** **Which strategy is fairest, and which is least fair?** Use the per-philosopher counts the harness prints, not just the ratio. **Explain the least fair one from its rule** — which philosophers eat least, and what do those philosophers have in common that the others do not? *(For `ordered`, list each philosopher's first fork.)*

**(d) [6]** `seats` breaks deadlock differently from `ordered`. **Which of the conditions for deadlock does each break?** *(OSTEP Ch. 32 lists four; Week 4 teaches them. You may read ahead.)*

**(e) [3]** Which strategy would you choose for a real server where a "philosopher" is a request needing two database rows, and why? One paragraph.

---

### Q4: A Writer-Preferring Reader–Writer Lock (20 points)

L12 §7 showed glibc's default reader–writer lock starving a writer completely. Implement `my_rwlock` in `rwpref.c` with **one mutex and two condition variables**, so that **a waiting writer prevents new readers from entering**.

**(a) [8]** Your implementation. **`my_wrlock_until` gives up at a deadline** — make sure that a writer who gives up does not leave readers blocked behind a writer who is no longer waiting.

**(b) [6]** Run `./rwpref glibc`, `./rwpref glibc-writer` and `./rwpref mine` twice each. Tabulate the writer's acquisitions and median wait **and the number of reads the readers completed**. How does your lock compare with glibc's writer-preferring kind?

**(c) [6]** **Your lock can starve readers.** Describe the workload that does it. Then describe a *fair* policy — neither readers nor writers can starve — in two or three sentences, and say what it costs.

---

### Q5: Locks in xv6 (10 points)

**(a) [4]** xv6's `acquire` calls `pushcli()` **before** the `xchg` loop. Describe exactly what could go wrong on a single CPU if it called `pushcli()` **after** acquiring the lock instead.

**(b) [6]** L11 §7 removed the lock from xv6's page allocator. `kalloc` is:

```c
r = kmem.freelist;
if(r)
  kmem.freelist = r->next;
return (char*)r;
```

**Give an interleaving on two CPUs in which both return the same page.** Then explain the other two symptoms L11 reported — **`sbrk` failing as if memory were exhausted**, and **`panic: remap`** — each in two sentences.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | A mutex from compare-and-swap | 30 |
| 2 | A lock that is not atomic | 10 |
| 3 | Five philosophers, measured | 30 |
| 4 | A writer-preferring reader–writer lock | 20 |
| 5 | Locks in xv6 | 10 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem set of the term is dropped.**

---

*CS 202 · Week 3 · PS 3 · © CSE Department*
