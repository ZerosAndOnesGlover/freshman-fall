# CS 202 · Operating Systems
## Week 3: Synchronization — Locks and Condition Variables

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 201, PROG 201
**Assessment for this course (overall):** Problem Sets 30%, Projects 30%, Midterms 25%, Final 15%
**This week's deliverables:** PS 2 due **Friday**, PS 3 released **Wednesday**, **Quiz 3** at the start of **Monday's** lecture (covers Week 2).
**Lab 2 is sat on the Tuesday of this week**; **Lab 3 covers this week and is sat on the Tuesday of Week 4.**

> ### **Midterm 1 is announced this week, and sat next Monday.**
> **Monday of Week 4, 18:00–19:15, VNC 100** — 75 minutes, **12.5%** of the course, covering
> **Weeks 0–3**: this week included. One handwritten sheet, one side. The revision guide is in the
> Week 4 folder. **Lab 3 is the next afternoon**, and Quiz 4 is the same Monday morning.

---

### Why This Week Exists

Because Week 1's context switch can happen between any two instructions, and `counter++` is three.

**Two threads incrementing one variable lost half of their increments** on the reference machine. Nothing crashed and nothing was reported. On one CPU a third were still lost. With a thousand increments, none were — so every quick test passes. **That is the problem this week solves, and the reason every kernel has locks on nearly every piece of shared data.**

The solutions are built up from the hardware. **An atomic instruction** makes a spinlock; **a futex** makes a lock that sleeps without paying for a system call when nobody is waiting; **condition variables** let a thread wait for something to become true; **semaphores** count. Each has a failure that looks correct on the page — a lock that hangs ten times in ten, a buffer that deadlocks after two items, a writer that never gets in — **and every one of them is measured here, so that you know not just that it can happen, but how soon.**

---

### Learning Objectives

By the end of Week 3, you should be able to:

1. **Show that `counter++` is not atomic** from its disassembly, and explain why one CPU still loses updates.
2. State the three properties a lock must provide, and **why disabling interrupts is not a lock**.
3. Name x86's atomic instructions — **`xchg`, `lock cmpxchg`, `lock xadd`** — and build a spinlock from test-and-set.
4. **Explain why xv6's `acquire` disables interrupts**, with the one-CPU deadlock it prevents.
5. Explain **why a shared atomic counter got slower from one thread to two**, and what per-thread counters avoid.
6. **Measure a lock's uncontended cost and system calls**, and say why a sleeping lock must not always wake.
7. **Explain `FUTEX_WAIT`'s comparison** and the lost wake-up it prevents; write Drepper's three-state mutex.
8. **Find the bug in a lock that keeps its waiter count outside the atomic word.**
9. Say **why test-and-test-and-set beats test-and-set**, and **when to spin and when to sleep**, with measurements.
10. Use condition variables correctly — **`while`, not `if`; one condition per CV** — and explain the failure of each mistake.
11. **Map xv6's `sleep` and `wakeup` onto condition variables**, and say why every `sleep` is in a loop.
12. Use semaphores; solve the **dining philosophers**, the **readers–writers** and the **sleeping barber** problems, and **say which condition each fix breaks**.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L10 Races and the Hardware That Makes Locks Possible]] | **Two threads lose 49.9%**, one CPU loses 37%, a thousand increments lose nothing; `cli` is not a lock; `xchg`, `lock cmpxchg`, `lock xadd`; a spinlock; **xv6's `pushcli`**; **per-thread counters at 0.3 ns against a shared atomic at 31** |
| [[L11 Sleeping Locks Futexes and When to Spin]] | **50 million uncontended mutex operations, zero `futex` calls**; always-wake at 639 ns; **Drepper's mutex at 14.8 ns**, 0.35% of contended rounds in the kernel; **a lock that hung 10 runs in 10**; TTAS halves TAS; **spin on four CPUs, sleep on one**; **xv6 without its allocator lock: corruption and `panic: remap`** |
| [[L12 Condition Variables Semaphores and the Classic Problems]] | **`if` woke to an empty buffer 254–372 times**; **one CV deadlocked within 10 items**; xv6's `sleep`/`wakeup`; semaphores; **naive philosophers deadlock 10 in 10**, two fixes deadlock 0; **glibc's default rwlock gave a writer zero acquisitions in 4 s**; the sleeping barber; monitors |
| [[CS202 Week3/assignments/QUIZ 3 Week 3 Monday\|QUIZ 3 Week 3 Monday]] | Ten minutes, covers **Week 2**, answer key printed |
| [[PS 3 A Mutex from Compare-and-Swap and Five Philosophers]] | A spin-then-yield mutex, a lock that is not atomic, four philosophers' strategies measured for fairness, a writer-preferring rwlock, and xv6's allocator. Due **Friday of Week 4** |
| `assignments/ps3/` | `casmutex.c`, `philo3.c`, `rwpref.c` — harnesses with `TODO`s |
| [[LAB 3 A Futex Lock]] | Always-wake, three-state, and a lock that hangs. **Tuesday of Week 4**, the day after Midterm 1 |
| `lab/flock.c` | The futex lock skeleton |
| [[CS202 Week3/resources/Reading Guide Week 3\|Reading Guide Week 3]] | OSTEP 26 and 28–31, the xv6 book on locking, and Drepper's paper |
| `resources/*.c`, `resources/locks.h`, `resources/allocstress.c` | Every program whose output appears in the lectures, including the xv6 allocator stress test |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A concurrency bug is a fact about timing, and a test is a sample of timings.**

Every broken program this week looked correct and passed some run. `race.c` with a thousand increments. `buggy2`'s lock, which works until thread counts drift. The one-CV buffer, which processed two items before stopping. The naive philosophers, who ate a thousand meals first. **None of those bugs was rare in the sense that matters** — each struck within seconds — and each was invisible to a test that ran briefly or once.

**The defence is not more testing. It is an argument**: what property does this lock give, what interleaving would break it, and what atomic operation rules that interleaving out? Drepper's value 2, the `while` loop, the lower-numbered fork first — **each is a one-line answer to a specific interleaving**, and the measurements are how you learn to believe that the interleaving is real.

---

### Assessment Reminder

**PS 2 is due Friday at 17:00. PS 3 is released Wednesday.**

**Midterm 1: Monday of Week 4, 18:00–19:15, VNC 100, Weeks 0–3, 12.5%.** One handwritten sheet, one side.

**Labs and quizzes carry no weight** and are still required. **Quiz 3 is at the start of Monday's lecture and covers Week 2.**

> **Two labs touch this week.** **Lab 2** — Week 2's scheduling — is sat on the **Tuesday of this
> week**. **Lab 3** covers this week and is sat on the **Tuesday of Week 4**, the afternoon after
> Midterm 1.

Both are tracked in [[_CS 202 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 0's `cli`** is L10 §4's non-solution, and **Week 0's system-call cost** is why L11's always-wake lock is unusable. **Week 1's context switch** is what makes preemption between `load` and `store` possible, and **Week 2's 3 ms slice** is how much work one lost update erases. **PROG 201 Week 3** used `pthread` locks from the outside; this week is their inside.

**Sideways:** **CS 201 Week 10's false sharing** is L10 §7's atomic counter getting slower with more threads. **PROG 202's immutable data** is the approach that avoids needing most of these locks at all.

**Forward:** **Week 4 is deadlock** — the four conditions, the Banker's algorithm, and a deadlock found in gdb — and every example uses this week's locks. **Week 5's TLB shootdown** is a lock problem across CPUs. **Project 1's scheduler must take `ptable.lock` correctly**, and L11 §7's lock held across `swtch` is the one you are most likely to get wrong.

---

*CS 202 · Week 3 · © CSE Department*
