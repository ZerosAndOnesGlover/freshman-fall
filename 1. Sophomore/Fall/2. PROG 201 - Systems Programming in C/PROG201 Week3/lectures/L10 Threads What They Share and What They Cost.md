# PROG 201 · Systems Programming in C
## Week 3 · Lecture 1 of 3
### Threads: What They Share, and What They Cost

*“If we believe in data structures, we must believe in independent (hence simultaneous) processing. For why else would we collect items within a structure? Why do we tolerate languages that give us the one without the other?”* — Alan Perlis, "Epigrams on Programming" (1982), #68

---

**Reading:** APUE Ch. 11 · TLPI Ch. 29–31 · `man 7 pthreads`, `man 3 pthread_create` · **Previous:** L09 · **Next:** L11 — mutexes and condition variables

**Coursework:** 📊 **Quiz 3** today · 📝 **PS 3** released Wed this week, due Fri of Week 4 17:00 · 📝 **PS 2** due Fri this week 17:00 · 🔬 **Lab 3** Mon of Week 4 15:00–16:50

---

## 1. A Thread Is a Process That Skipped the Copy

Week 0's `fork` gave you a second flow of control by duplicating everything: page tables, descriptor table, signal dispositions, the lot. Week 2 then spent three lectures putting some of it back together, because two processes that need to share need a mechanism — a pipe, a queue, a mapped region.

**A thread is the other end of that trade.** `pthread_create` gives you a second flow of control that shares the address space from the start. Nothing needs to be put back together, because nothing was taken apart.

The price is that **everything is shared by default**, including the things you did not mean to share, and there is no `MAP_PRIVATE` to hide behind. Week 2's shared-memory lecture was about a region you deliberately opted into. This week the region is your whole program.

---

## 2. Exactly What Is Shared

`shared.c` starts one thread and prints the same six things from both:

```
worker: tid=551774  &local=0x748e527fee94  global=2  per_thread=2  fd offset=16  errno=9
main  : tid=551773  &local=0x7ffd976d5754  global=2  per_thread=1  fd offset=16  errno=0

same process: getpid() = 551773 for both threads.
```

Read it line by line:

| Thing | Shared? | Evidence |
| --- | --- | --- |
| The process ID | **one** | `getpid()` is 551773 in both |
| The thread ID | two | `gettid()` is 551773 and 551774 |
| A global variable | **one** | the worker incremented it; main sees `2` |
| A `__thread` variable | two | worker sees `2`, main still sees `1` |
| `errno` | **two** | the worker's failed `close(-1)` set `EBADF`; main's `errno` is still 0 |
| A file descriptor **and its offset** | **one** | main read 16 bytes; the worker's `lseek` reports 16 |
| The stack | two | `0x748e527fee94` against `0x7ffd976d5754` — different regions entirely |

The full list, worth learning as two columns:

**Shared:** the address space (code, globals, heap, and every `malloc`'d block), the descriptor table and the open file descriptions behind it, the current directory, the umask, signal *dispositions*, resource limits, and the process ID.

**Private:** the thread ID, the stack, the register set, `errno`, the signal *mask*, the alternate signal stack, scheduling policy and nice value, and anything declared `__thread`.

**Three of those rows are where the bugs live.**

**`errno` is per-thread, and it has to be.** If it were not, one thread's failed `write` would overwrite another's pending error, and no library function could be trusted. On Linux `errno` is a macro that expands to `(*__errno_location())`, which is thread-local. This is why you must never write `if (errno)` without a preceding failure in *this* thread.

**Signal dispositions are shared; masks are not.** One `sigaction` changes the handler for the whole process. But `pthread_sigmask` changes only the calling thread's mask, and a signal sent to the *process* is delivered to **any one thread that has it unblocked** — an arbitrary one. That is why the standard pattern is: block everything in `main` before creating threads, then have one dedicated thread call `sigwait`. Week 0's L03 machinery all still applies, and it now has to pick a thread.

**The descriptor table is shared, offsets included.** Two threads writing to the same descriptor share an offset exactly as `dup` did in Week 1 L04 — because it *is* the same open file description. Everything you learned about the three tables carries over unchanged.

---

## 3. What a Thread Costs

`cost.c`, 20,000 create-and-join pairs:

```
pthread_create + join        :    29.21 us
fork + waitpid               :   163.64 us   (5.6x)
pthread_create, 64 MiB stack :    53.81 us   (1.8x the default)
default stack size           :     8192 KiB
```

**A thread is 5.6× cheaper than a process** — not a thousand times cheaper, which is what people expect. Week 0 measured `fork` at 0.166 ms for a 1 MB process and found the cost was the page-table copy; a thread skips that copy and still pays for a stack mapping, a kernel task structure, and a scheduler enqueue.

**The default stack is 8 MiB**, which is *virtual* address space, not memory — the pages are faulted in as the thread uses them, so an idle thread costs a page or two of real memory. That is why the 64 MiB stack costs only 1.8× more: `mmap` of a larger region, not more pages touched.

### How many threads can you make?

`maxthreads.c` creates parked threads until `pthread_create` fails, once with the default stack and once with a 64 KiB one:

```
stack   8192 KiB: stopped at 7643 threads, Resource temporarily unavailable
stack     64 KiB: stopped at 7644 threads, Resource temporarily unavailable
```

**The same number.** Shrinking the stack by 128× bought one extra thread.

The usual advice — "reduce the stack size to get more threads" — is about 32-bit address space exhaustion, and it is thirty years out of date on a machine with a 47-bit user address space. The limit here is a **task count**:

| Limit | Value |
| --- | --- |
| `RLIMIT_NPROC` (`ulimit -u`) | 25,571 |
| `/proc/sys/kernel/threads-max` | 51,142 |
| **the cgroup's `pids.max`** | **7,671** |

7,643 created plus the 28 already in this shell's scope is 7,671 exactly. **The binding limit is the cgroup**, which is a Week 11 subject arriving three weeks early, and it is the one nobody checks. When `pthread_create` returns `EAGAIN`, look at `/sys/fs/cgroup/.../pids.max` before you look at anything else.

*(`RLIMIT_NPROC` is 25,571 here — the same number Week 0 L03 measured for `RLIMIT_SIGPENDING`, because both default to the same per-user figure derived from RAM.)*

---

## 4. Creating and Joining

```c
#include <pthread.h>

void *worker(void *arg);

pthread_t t;
int rc = pthread_create(&t, NULL, worker, arg);   /* rc, NOT errno */
if (rc != 0) { fprintf(stderr, "%s\n", strerror(rc)); ... }

void *result;
pthread_join(t, &result);
```

Four things that are unlike every other API in this course:

1. **The pthreads functions return the error number.** They do not set `errno` and they do not return `-1`. `if (pthread_create(...) < 0)` is wrong and will silently never fire. Use `strerror(rc)`, not `perror`.
2. **`arg` and the return value are both `void *`**, so anything larger than a pointer has to be passed by address — and that address must outlive the thread. Passing `&i` from a loop is the classic bug, because every thread gets the same address and reads whatever `i` is *now*.
3. **A joinable thread that is never joined is a leak.** Its stack and descriptor stay until the process exits. Either `pthread_join` it or create it detached (`pthread_attr_setdetachstate`, or `pthread_detach` afterwards).
4. **Returning from `main` calls `exit`, which kills every thread**, wherever it is. `pthread_exit` from `main` instead lets the process live until the last thread finishes. This is a real and common way to lose the tail of a program's work.

### Threads and `fork` do not mix

`fork` in a multi-threaded process duplicates **only the calling thread**. Every other thread simply does not exist in the child — including, and this is the problem, whichever thread was holding the `malloc` lock at the time. The child inherits a locked mutex with no owner, and its next `malloc` deadlocks.

The rule POSIX gives you: **between `fork` and `exec` in a threaded program, call only async-signal-safe functions.** That is Week 0 L03's list, arriving in a new place for the same reason. `pthread_atfork` exists to patch this and is best avoided; if you need to spawn in a threaded program, use `posix_spawn` (Week 0 L01 §5), which does the right thing and is 70× faster besides.

---

## 5. Thread-Local Storage

Three ways to get a variable that is per-thread:

```c
__thread int counter;                  /* GCC, and C11's _Thread_local */
_Thread_local int counter;             /* the standard spelling        */
```

```c
pthread_key_t key;                     /* the portable, older way      */
pthread_key_create(&key, free);        /* with a destructor            */
pthread_setspecific(key, malloc(64));
void *p = pthread_getspecific(key);
```

`_Thread_local` is a storage class: the compiler and linker arrange a per-thread slot, access costs about as much as a global, and there is no destructor. `pthread_key_t` costs a function call per access and gives you a destructor that runs when the thread exits — which is what you want when the value is a heap pointer.

**Thread-local storage is not a fix for a data race.** It is a way to have per-thread state, which is a different thing. If two threads must agree on a value, making it thread-local means they now disagree quietly instead of racing loudly.

---

## 6. What Goes Wrong, and It Goes Wrong Fast

`race.c` is `shm.c` from Week 2 L09 with threads instead of processes: four threads, 200,000 increments each, one shared `long`.

```
mode                    counter     expected       lost      seconds
unguarded                234583       800000      70.7%       0.0006
pthread_mutex            800000       800000       0.0%       0.0529
atomic_fetch_add         800000       800000       0.0%       0.0148
spinlock                 800000       800000       0.0%       0.0390
```

**70.7% of the work vanished** — the same result as Week 2's processes (64.7%), and for exactly the same reason, because it is the same memory. Nothing about threads makes this worse or better; the memory does not know which kind of flow of control is writing to it.

What is new is the **fourth column**. The unguarded version took 0.0006 s and the mutex version took 0.0529 s — the wrong answer is **88 times faster than the right one.** That ratio is the entire reason this bug keeps being written. Nobody removes a lock because they want incorrect results; they remove it because the profiler pointed at it.

`atomic_fetch_add` gets the right answer in 0.0148 s, which is 3.6× faster than the mutex and is the honest answer for a counter. **It is not the answer for anything with two fields**, because atomicity of each field separately is not atomicity of the pair — and that is L11's subject.

---

## Summary

- A thread shares the **address space, descriptors, current directory, signal dispositions and PID**; it has its own **stack, registers, `errno`, signal mask, nice value and TID**.
- `errno` is per-thread by necessity. Signal *dispositions* are shared but *masks* are not, and a process-directed signal goes to an arbitrary thread that has it unblocked.
- `pthread_create`+`join` costs **29 µs** against `fork`+`wait`'s **164 µs** — 5.6×, not a thousand.
- The default stack is **8 MiB of address space**, and shrinking it does not buy you more threads: the ceiling here is the **cgroup's `pids.max` of 7,671**, not memory.
- **Pthreads functions return the error number**; they do not set `errno`.
- Returning from `main` kills every thread. Unjoined joinable threads leak.
- **`fork` in a threaded program keeps only the calling thread**, with everyone else's locks still held. Use `posix_spawn`.
- `_Thread_local` gives per-thread state; it does not fix a race.
- Four threads lost **70.7% of 800,000 increments**, and the broken version was **88× faster** than the correct one. That ratio is why the bug survives.

---

## Exercises

1. Write the loop that passes `&i` to every thread and observe the wrong values. Fix it three ways: a per-thread struct, a cast through `intptr_t`, and a barrier. Which is safe if the thread outlives the loop?
2. Set a `SIGINT` handler, then block `SIGINT` in `main` before creating four threads. Send it. Which thread runs the handler? Now unblock it in one thread only and repeat.
3. Open a file, then have two threads `write` to the same descriptor without a lock. Predict what happens to the offset from Week 1 L04, then check.
4. Create 5,000 threads with a 1 MiB stack and 5,000 with 8 MiB. Compare `VmSize` in `/proc/self/status` and then `VmRSS`. Explain the difference.
5. Find your cgroup's `pids.max`. Lower it with `systemd-run --user -p TasksMax=100` and re-run `maxthreads.c`.
6. Call `fork` from a thread while another thread holds a `malloc` lock (a tight `malloc`/`free` loop will do). Make the child call `malloc`. How long does it hang for?
7. `pthread_join` on an already-joined thread is undefined behaviour, not an error. Write the program that demonstrates why detached threads are the safer default in a long-running server.

---

*PROG 201 · Week 3 · L10 · © CSE Department*
