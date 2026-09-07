# PROG 201 · Reading Guide · Week 3
## APUE Chapters 11 and 12, and the parts about time that no book covers

---

**This is the biggest reading week of the term**, and it is also the week before Midterm 1, so the plan below is ordered by what you need first rather than by chapter number.

APUE Chapters 11 and 12 are good on the API and quiet on two things this week measures: **what the primitives cost**, and **what happens when scheduling gets involved**. The second gap is why §3 below sends you to `man 7 sched` rather than to a textbook.

| Source | Read? | Why |
|---|---|---|
| **APUE 11.1–11.6** | **All of it** | Thread creation, termination, synchronisation. L10 and L11 |
| **APUE 11.6.5** | **Read twice** | Mutex attributes, and the one paragraph on priority ceilings and inheritance |
| **APUE 12.1–12.5** | **Read** | Thread limits, attributes, and thread-specific data. L10 §5 |
| APUE 12.8 | **Read** | Threads and `fork`. Four pages, and it is L10 §4's most dangerous rule |
| APUE 12.9 | Skim | Threads and I/O. `pread`/`pwrite`, which Week 1 already gave you |
| **TLPI Ch. 29–30** | **All of it** | The best treatment of thread basics and synchronisation in print |
| TLPI Ch. 31 | Read | Thread safety, TLS, and the `_r` functions |
| TLPI Ch. 33 | Skim | Threads and signals. Come back in Week 5 |
| **TLPI §35.3** | **Read** | Realtime scheduling, which is what L12 §3 turns out to need |

---

## APUE Chapter 11 — the questions to hold

**§11.3 Thread creation**

1. Stevens notes that pthreads functions return the error number rather than setting `errno`. Find the sentence. Then write the two-line error-reporting helper you will use all term — it is not `perror`.
2. The example passes a thread ID by address. **What is the lifetime of the thing you pass to `pthread_create`?** State it as a rule, then find a way to break it in three lines.

**§11.4 Thread termination**

3. Three ways a thread ends: return, `pthread_exit`, cancellation. Give one thing that is true of exactly one of them.
4. What does `pthread_exit` from `main` do that `return` from `main` does not? *(L10 §4. This is worth a mark on the midterm.)*
5. Read the cancellation section. Find "deferred cancellation" and "cancellation point", and then form a view on why almost nobody uses `pthread_cancel`.

**§11.6 Synchronisation**

6. Figure 11.11's incremented reference count. Redraw it as the three-instruction sequence and mark the two places another thread can interleave. *(Week 3 measured 70.7% loss on exactly this.)*
7. Stevens covers `pthread_mutex_timedlock`. Give one situation where a timeout is the right answer and one where it is a way of not fixing the bug.
8. **§11.6.4, reader-writer locks.** He says they are useful when reads are more common than writes. Add the condition his sentence is missing — L11 §6 measured a reader-writer lock at **0.52×** a mutex when it was absent.
9. **§11.6.6, condition variables.** Find where he says the mutex must be held. Then write out, in your own words, the three things `pthread_cond_wait` does and which two of them are atomic with respect to each other.

**§11.6.5 — read this section twice**

10. Find `PTHREAD_PRIO_INHERIT` and `PTHREAD_PRIO_PROTECT`. The book describes what they do. **It does not say what they need in order to do it.** Write down what you think they require, then check against L12 §3 — and note that the gap between the book and the machine is this week's whole lab.

---

## APUE Chapter 12 — the two sections that matter most

**§12.4 Thread-specific data**

11. `pthread_key_create` takes a destructor. When does it run, and what is passed to it? What happens to the value if the destructor is `NULL`?
12. Compare with `__thread` / `_Thread_local`. Which of the two can hold a `malloc`'d pointer without leaking, and why?

**§12.8 Threads and `fork`**

13. Stevens explains that only the calling thread survives in the child. **Work out for yourself which lock is most likely to be held by one of the threads that did not survive**, and why that particular one turns the child into a deadlock rather than a crash.
14. `pthread_atfork` exists to patch this. Read the section, then say why the handlers are difficult to write correctly for a library rather than an application.

---

## The Man Pages for This Week

| Page | The paragraph |
|---|---|
| **`man 7 pthreads`** | The "Thread-safe functions" list and the paragraph on which attributes are per-thread |
| **`man 3 pthread_cond_wait`** | The two paragraphs on spurious wakeups, and the note about signalling with or without the mutex |
| **`man 3 pthread_mutexattr_setprotocol`** | Everything it says about what the protocols require. Read it *before* Lab 3 |
| **`man 7 sched`** | The scheduling policies table, and the "Privileges and resource limits" section — `RLIMIT_RTPRIO` is what Lab 3 turns on |
| `man 3 pthread_rwlockattr_setkind_np` | The three fairness policies, and which one is the default |

**And one command:** `chrt -m` prints the priority ranges your machine supports. Run it before Lab 3 so the lab's Part A is a confirmation rather than a surprise.

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| TLPI §30.1–30.2 | Mutexes and condition variables, with the futex layer visible underneath |
| TLPI §31.3 | One-time initialisation and `pthread_once` |
| TLPI §35.3 | `SCHED_FIFO`, `SCHED_RR`, and the limits that gate them |
| Butenhof, *Programming with POSIX Threads* | Still the best book on the subject. Chapter 3 is the one to read |
| Herlihy & Shavit, *The Art of Multiprocessor Programming* | Where to go when locks stop being enough. Chapter 7 is spin locks done properly |
| **The Mars Pathfinder postmortem** (Glenn Reeves, 1997) | Two pages, freely available, and the best short piece of engineering writing on this course's reading list |

---

## The Habit for This Week

**Check that the thing you enabled is actually on.**

Week 2's habit was to read the limits before the API. This week's is its sharper form: **a call that returns success has not necessarily done anything.** `pthread_mutexattr_setprotocol(PTHREAD_PRIO_INHERIT)` returns 0, the mutex initialises, the protocol reads back correctly, and the behaviour does not change at all — because the thing it boosts does not exist for your threads.

There is no compiler warning for this and no runtime error. The only way to know is to **measure the behaviour you were trying to buy**, which is what Lab 3 makes you do. Carry it forward: every time you turn on a flag for a guarantee, write down the experiment that would fail if the flag were ignored, and run it.

---

*PROG 201 · Week 3 · Reading Guide · © CSE Department*
