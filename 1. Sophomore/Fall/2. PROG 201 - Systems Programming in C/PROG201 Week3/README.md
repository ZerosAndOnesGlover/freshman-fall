# PROG 201 · Systems Programming in C
## Week 3: POSIX Threads (pthreads)

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101; CS 201 as co-requisite
**Assessment for this course (overall):** Problem Sets 35%, Projects 25%, Midterms 25%, Final 15%
**This week's deliverables:** PS 3 (due Friday of Week 4) and **Quiz 3** (Tuesday, covers Week 2).
**Lab 2 is sat on the Monday of this week**; **Lab 3 covers this week and is sat on the Monday of Week 4**.

> ### **Midterm 1 is on the Monday of Week 4**, 18:00–19:30, and covers **Weeks 0–3**.
> It is announced this week. **This is the last week of material on it** — and note that Lab 3 is
> sat that same afternoon, 15:00–16:50, ending seventy minutes before the paper starts. Revise
> before the lab, not after it. [[PROG 201 Scheduling Notes]] records why the two land together.

---

### Why This Week Exists

Because the Mars Pathfinder rebooted itself on the surface of Mars, and every lock in its code was correctly taken and correctly released.

Week 2 gave two processes a shared region and a semaphore around it. **A thread is what you get when the sharing is not opt-in**: one address space, one descriptor table, one heap, and several flows of control inside them. Everything Week 2 taught about races applies unchanged — the memory does not know which kind of flow of control is writing to it — and the surface area is now your whole program.

Three ideas, and the third is the one this course exists to teach:

1. **A thread is a process that skipped the copy.** 29 µs against 164 µs, and everything shared except the stack, the registers, `errno` and the signal mask.
2. **A condition variable is the answer to "unlock, then sleep is two operations".** Which is Week 0's `pause()` race, again, in a different vocabulary.
3. **A concurrent program can be provably free of races and still fail.** Correctness and timing are different properties, and priority inversion is where that stops being an abstraction: a half-second critical section became a **hundred-second wait**, with no race anywhere in the program.

---

### Learning Objectives

By the end of Week 3, you should be able to:

1. List what threads share and what they do not, and explain why `errno` has to be in the second list.
2. Say what `pthread_create` costs relative to `fork`, and what the default stack actually consumes.
3. Find the limit that stops you creating more threads — and know that it is usually not memory.
4. Use the pthreads API correctly: error returns rather than `errno`, argument lifetimes, joining or detaching.
5. State why `fork` in a threaded program is dangerous, and what to use instead.
6. Choose between a mutex, a semaphore, a spinlock, an atomic and a reader-writer lock, with the costs.
7. Explain what `pthread_cond_wait` does atomically, and why the loop must be a `while`.
8. Say when `broadcast` is required for **correctness**, not for speed.
9. Build a bounded buffer with a mutex and two condition variables.
10. Explain when a reader-writer lock is a pessimisation, and name two other hazards it carries.
11. **Describe priority inversion, reproduce it, and predict its magnitude from the scheduler's weights.**
12. **Recognise a correctness feature that is silently inert**, and design the experiment that would reveal it.
13. Build a thread pool, size it, and say what its single queue costs.
14. Recognise false sharing.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L10 Threads What They Share and What They Cost]] | The two columns of shared and private, **measured**; thread cost against process cost; why a smaller stack buys no more threads; `fork` in a threaded program; TLS; and the same lost-update race as Week 2, **88× faster wrong than right** |
| [[L11 Mutexes Condition Variables and Reader Writer Locks]] | Mutex against semaphore; the cost of every primitive; what `pthread_cond_wait` does atomically; **7.12% of wakeups found nothing to do**; the one-condition-variable deadlock; when a reader-writer lock loses; the bounded buffer written out |
| [[L12 Priority Inversion Thread Pools and Choosing]] | Pathfinder; **0.49 s → 100.6 s**; `PTHREAD_PRIO_INHERIT` accepted, correct, and inert; the fixes that work; thread pools **45× faster than thread-per-task**; sizing; false sharing; pthreads against C11 threads |
| [[LAB 3 Priority Inversion and Its Fix]] | Reproduce Pathfinder, then fail to fix it. **Monday of Week 4** |
| `lab/inversion.c`, `lab/rtcheck.c`, `lab/Makefile` | The skeleton, and the diagnostic that tells you what the machine will allow |
| [[PS 3 Implement a Thread Pool]] | Build it, shut it down correctly, measure it, and size it. Due **Friday of Week 4** |
| [[PROG201 Week3/assignments/QUIZ 3 Week 3 Tuesday\|QUIZ 3 Week 3 Tuesday]] | Ten minutes, covers **Week 2**, answer key printed |
| [[PROG201 Week3/resources/Reading Guide Week 3\|Reading Guide Week 3]] | APUE Ch. 11–12, and the man pages that cover what the book does not |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A call that returns success has not necessarily done anything.**

Lab 3's four lines are the documented, textbook fix for priority inversion:

```c
pthread_mutexattr_setprotocol(&a, PTHREAD_PRIO_INHERIT);   /* returns 0 */
pthread_mutex_init(&lock, &a);                             /* returns 0 */
```

Both calls succeed. The protocol reads back as `PRIO_INHERIT`. And the measured wait is **100.392 s with it against 100.607 s without** — because priority inheritance boosts a *realtime* priority, `SCHED_OTHER` threads have none, and `RLIMIT_RTPRIO` on these machines is 0 so you cannot get one.

Nothing warns you. No compiler diagnostic, no runtime error, no log line. The only way to know is to **measure the behaviour you were trying to buy** — and the fixes that do work were available all along:

| | H waited |
| --- | --- |
| baseline, no medium threads | 0.49 s |
| **the bug** | **100.6 s** |
| the documented fix, `PRIO_INHERIT` | 100.4 s — **nothing** |
| equal priorities | 1.94 s |
| a hundred short critical sections instead of one long one | ~0.5–0.9 s |

**Hold locks briefly. It is the fix that does not depend on privileges you may not have.**

---

### Assessment Reminder

**Labs and quizzes carry no weight** and are still required. **Quiz 3 is at the start of Tuesday's lecture and covers Week 2**; the answer key is printed in the paper and you mark it yourself before leaving.

> **Two labs touch this week.** **Lab 2** — Week 2's IPC benchmark — is sat on the **Monday of this
> week**. **Lab 3** covers this week and is sat on the **Monday of Week 4**, the same afternoon as
> Midterm 1.

Both are tracked in [[_PROG 201 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 2's shared counter is L10 §6**, with threads instead of processes: 64.7% lost then, 70.7% now, the same three instructions. **Week 2's ring is L11 §7**, with two condition variables where it had two semaphores — and the comparison of the two is the clearest statement of what each primitive is for. **Week 0's `pause()` race is `pthread_cond_wait`'s reason to exist.** **Week 0's `EINTR` rule** applies to `sem_wait` and to every blocking pthreads call. **Week 1's file offsets** are shared between threads because it is the same open file description.

**Sideways:** **CS 201 Week 3 is on the memory hierarchy**, which is L12 §6's false sharing seen from the hardware end: a 64-byte cache line bouncing between four cores is CS 201's coherence protocol doing exactly what it is supposed to.

**Forward:** **Week 4 is `mmap` in its own right.** **Week 5's server is this week's thread pool with sockets in the tasks**, and the C10K problem is the argument that you should not have used threads at all. **Week 6's shell needs `SIGCHLD` in a program with more than one flow of control.** **Project 2 is a networked multi-threaded server**, and PS 3's pool is its core.

---

*PROG 201 · Week 3 · © CSE Department*
