# PROG 201 Scheduling Notes

What had to be decided before PROG 201 could be written, and why each decision went the way it did.
Written 2026-09-05, while building Week 0. **The authority** is
`5. Academic Registry/1. Scheduling/Year2 - Sophomore/CSE_Year2_Sophomore_Curriculum.docx`, and
where the registry's own scheduling files settle a question, they do.

---

## 1. The lab has to lag a full week, and unlike CS 201 it had no choice

[[Year2 - Sophomore/ROOM ASSIGNMENTS|ROOM ASSIGNMENTS]] puts PROG 201's lectures on **Tue/Wed/Thu 10:00** and its lab on **Mon
15:00–16:50**. The lab is therefore before every one of that week's lectures, and a lab covering
Week *N* cannot be sat in Week *N*.

**Lab *N* covers Week *N* and is sat on the Monday of Week *N+1***, which is the same shape CS 201
uses for the same reason (its lab is a Tuesday and its lectures Mon/Wed/Fri) and the opposite of
CS 211, whose Friday lab has all of its week's teaching behind it. All three are stated in each
course's own syllabus and in every lab file's header, because a student takes all three at once.

---

## 2. Thirteen labs, twelve Monday slots

Counting the sittings the term actually has:

| Sitting | Which lab |
|---|---|
| Friday of Week 0 | Lab 0 |
| Mondays of Weeks 2–12 (11 Mondays) | Labs 1–11 |
| Monday of the completion period | Lab 12 (demo day) |

That is thirteen — **except that the Monday of Week 6 is Fall Break**, and [[ACADEMIC CALENDAR]]
says no classes. Ten usable Mondays, thirteen labs, one short. The Monday of Week 1 cannot absorb it:
Lab 0 was sat the Friday before, and Lab 1 is still waiting for Week 1's lectures to happen.

**Resolved with a make-up rather than a merge.** Lab 5 — which would have been sat on the Monday of
Week 6 — moves to the **Friday of Week 6, 16:00–17:50, BH 215**. Nothing else moves.

The alternatives, and why not:

| Option | Why not |
|---|---|
| Sit it on the Tuesday of Week 6 instead | CS 201's lab holds Tue 15:00–16:50 and the students are in it |
| Wednesday of Week 6 | Free, but that evening is MATH 241's Midterm 1 |
| Thursday of Week 6 | MATH 241's recitation is Thu 15:00–15:50 |
| Merge Lab 5 into Lab 6 | Lab 6 is job control, which is a full session on its own, and Lab 5 needs the machines for a stress test |
| Drop a lab | The registry lists thirteen and the curriculum assigns each of them work |

**BH 215 has no other Fall booking** — [[Year2 - Sophomore/ROOM ASSIGNMENTS|ROOM ASSIGNMENTS]] gives it to PROG 201's Monday lab and
nothing else that term — so the Friday slot is available. CS 211's lab vacates BH 220 at 15:50, and
16:00 clears it.

---

## 3. The Week 0 lab is at 17:00, which is late, and there is nowhere earlier

[[Year2 - Sophomore/ASSESSMENT CALENDAR|ASSESSMENT CALENDAR]] puts **every** Year 2 course's Week 0 lab on the Friday that closes the
ten-day Week 0. On that one afternoon:

| Course | Time | Room |
|---|---|---|
| CS 211 Lab 0 | 14:00–15:50 | BH 220 |
| CS 201 Lab 0 | 15:00–16:50 | BH 210 |
| **PROG 201 Lab 0** | **17:00–18:50** | **BH 215** |

17:00 is the first start time that clears both. It applies to Lab 0 only.

> **Worth recording, and not fixed here: CS 201's and CS 211's Week 0 labs already overlap each
> other**, 15:00–15:50, and a Year 2 student is enrolled in both. That was true before PROG 201 was
> written and it is not PROG 201's to resolve — but whichever of the two moves, PROG 201's 17:00
> start could then move earlier, and this note is where to look when it does.

---

## 4. PS 0 is due in Week 1, not Week 0

[[Year2 - Sophomore/ASSESSMENT CALENDAR|ASSESSMENT CALENDAR]] §"W0" makes CS 201's PS 0 the exception — due the Friday of Week 0, because
CS 201's Week 0 is ten days long — and says every other problem set is released Wednesday of its own
week and due the Friday of the week after. **PROG 201 follows the general rule**: PS 0 released
Wednesday of Week 0, due Friday of Week 1. The paper says so in its header.

---

## 5. The lab machines are on 24.04, not the 22.04 the curriculum names

The curriculum's PROG 201 entry says *OS: Linux (Ubuntu 22.04)*. BH 215 runs **Ubuntu 24.04.4 LTS,
GCC 13.3.0, glibc 2.39, kernel 7.0** — the same image as BH 210, so that CS 201 and PROG 201 share
a toolchain in a term where they are taught side by side.

Nothing in the curriculum's thirteen weeks needs 22.04, but **two of Week 0's measurements are
version-dependent and are labelled in the notes where they appear**:

- the `malloc`-in-a-signal-handler deadlock does not reproduce, because glibc 2.39's `tcache` fast
  path takes no lock (L03 §4 — and the lecture makes the non-reproduction the point);
- orphans are adopted by `systemd --user`, not by PID 1 (L02 §5), which is a property of the session
  manager rather than of glibc, but is equally a thing APUE does not describe.

Recorded as a deviation in [[PROG201 Week0/resources/Course Overview Syllabus|Course Overview Syllabus]] so that a reader
meets it without coming here.

---

## 6. Every number in Week 0 was measured on the reference machine

Intel Core i5-8250U, Ubuntu 24.04.4, GCC 13.3.0, glibc 2.39, kernel 7.0.0-30 — the same machine the
CS 201 Week 0 figures were taken on, so the two courses' numbers are comparable where they overlap.

The measurements the lectures depend on, and the programs that produced them:

| Claim | Program | Result |
|---|---|---|
| COW copies nothing for a reader | `cow.c` | 0 minor faults reading 16,384 pages; 16,384 writing them |
| `fork` is linear in the parent | `forkcost.c` | 0.166 ms at 1 MB → 35.042 ms at 1 GB; ~34 µs/MB |
| `posix_spawn` avoids the page tables | `spawncost.c` | 70× faster than `fork`+`exec` at 1 GB, no faster at 1 MB |
| stdio buffers are copied by `fork` | `buf.c` | one `x` on a pty, eight through a pipe |
| Standard signals do not queue | `rtq.c` | 5,000 `SIGUSR1` sent while blocked → handler ran **once** |
| Real-time signals queue, then drop silently | `rtq.c` | 40,000 sent → 25,571 delivered = `RLIMIT_SIGPENDING`, with `kill()` returning 0 every time |
| `printf` in a handler corrupts | `reent.c` | 93 of the handler's 138 lines damaged |
| `malloc` in a handler does not fail | `unsafe.c` | 1.49 billion allocations, ~100,000 signals, no deadlock |
| Orphans are not adopted by PID 1 | `orphan.c` | adopted by 257510, `/usr/lib/systemd/systemd --user` |
| The mask survives `fork` and `exec` | Lab 0 | child `SigBlk` = `0x14002` (SIGINT, SIGTERM, SIGCHLD) until the fix |

**The last row is Lab 0's Part C**, and it was found the way the students will find it: the
reference solution shut down by SIGKILLing a child that should have died on SIGTERM.

---

## 7. Every number in Week 2 was measured too, and three of them contradict the curriculum

Same machine as §6. Week 2's programs, and what each one settled:

| Claim | Program | Result |
|---|---|---|
| A pipe holds sixteen *slots*, not 65,536 bytes | `capshape.c` | 4,096-byte writes fill it 100%; **4,097-byte writes fill it to 68.8%** (45,066 bytes in 11 writes) |
| `F_SETPIPE_SZ` moves the ceiling | `capacity.c` | 1 MiB granted; capped by `/proc/sys/fs/pipe-max-size` |
| `PIPE_BUF` bounds the request, not the pipe | `atomic.c` | 4 writers, 800 records: **0 torn at 4,096 B, 679 torn at 4,097 B** with a slow reader |
| Above `PIPE_BUF` a fast reader hides the bug | `atomic.c`, `pcbig.c` | 8 KB records: **0 torn of 8,000** with a fast reader, **1,192 torn of 1,200** with a dribbling one |
| FIFO `open` is a rendezvous, and asymmetric | `fifo.c` | `O_WRONLY\|O_NONBLOCK` → `ENXIO`; `O_RDONLY\|O_NONBLOCK` → a descriptor that reads EOF |
| A FIFO server needs a held write end | `fifoeof.c` | 1 of 5 requests without it, 5 of 5 with it |
| FIFO EOF is not sticky | `reopen.c` | the same read descriptor revives when a new writer opens |
| Message queues have edges and priorities | `mq.c` | `urgent(9) now(9) routine(1) whenever(0)` — priority first, FIFO within |
| The receive buffer must be ≥ `mq_msgsize` | `mq.c` | 2-byte message into a 2-byte buffer → `EMSGSIZE` |
| **Unprivileged mq limits are 10 × 8,192** | `mqlimit.c` | maxmsg 11 → `EINVAL`; msgsize 8,193 → `EINVAL` |
| IPC objects outlive the process | `mq.c` | `/dev/mqueue/prog201` still held `QSIZE:11` after exit |
| `MAP_SHARED` vs `MAP_PRIVATE` | `maps.c` | child writes 42: shared reads 42, private reads 0 |
| Mapping past the end gives `SIGBUS` | `gotcha.c` | no `ftruncate` → child killed by **Bus error**, not a segfault |
| An unguarded shared counter | `shm.c` | **282,666 of 800,000** increments survived (64.7% lost); with `sem_wait`, 800,000 |
| Uncontended semaphores are not system calls | `maps.c` | **19.3 ns** per `sem_wait`+`sem_post` pair |
| Reference costs for the arithmetic | `maps.c` | `getpid()` **574.2 ns**; `memcpy` of 4,096 B **117.8 ns** |
| The benchmark | `bench.c` (Lab 2) | pipe 3,680 MiB/s, FIFO 2,924, mq 2,786, **shm one slot 574** |
| Ring depth is the fix | `bench.c` | 1 slot 557 MiB/s → 4 slots 3,979 → flat at ~4,600 from 8 |
| The crossover is message size | `bench.c` | shm/pipe **0.11× at 64 B, 0.57× at 16 KB, 2.27× at 64 KB, 5.75× at 256 KB** |
| Shared memory makes no fewer system calls | `strace -c -f` | pipe **131,114**; one-slot ring **131,817**, nearly all `futex` |
| Ordering B is not always a deadlock | `dead.c` | completes with an independent consumer; **hangs the moment the consumer takes the mutex** |

### The three that contradict something

1. **"Shared memory is the fastest IPC mechanism."** The curriculum's own Week 2 Core Concept says
   so, and the syllabus repeats it. Measured, a one-slot shared-memory ring is **six times slower
   than a pipe** at 4 KB and the same number of system calls. L09 §5–§6 keeps the claim, states it,
   and then takes it apart; the syllabus's deviations table records that the lecture disagrees with
   the curriculum text. **The claim is true above ~64 KB per message and false below it**, and that
   is the form the course teaches.

2. **"`SA_RESTART` does not restart `sem_wait`."** Widely repeated. On glibc 2.39 it plainly does —
   `gotcha.c` returns `EINTR` with `sa_flags = 0` and **hangs forever** with `SA_RESTART`. L09 §3
   reports both and still requires the retry loop, because the loop is correct either way.

3. **"Ordering B deadlocks."** Every textbook says a producer that takes the mutex before waiting
   for a slot deadlocks. With a consumer that touches only `tail`, it does not — four
   configurations, all completed. It deadlocks as soon as the consumer needs the mutex too. PS 2 Q4
   was rewritten around the measurement, and the lesson is better than the one it replaced: **the
   bad ordering is not reliably fatal, which is why it ships.**

### One gap, recorded rather than fixed

**Week 1 has no table here.** Its figures are stated in L04–L06 with their outputs quoted, and two
of its programs are named in the lectures (`offsets.c` in L04, `bufsize.c` in L05), but the others —
the `O_APPEND` race that lost 4,396 of 80,000 lines, the `writev` comparison, the `FD_CLOEXEC`
demonstration — were not written down with their program names when Week 1 was built. Anyone
reproducing Week 1 will have to rewrite them from the lecture text, which is possible but is work
that should not have been necessary. **Weeks 3 onward get their table in this file as they are
built.**

---

## 8. Week 3 could not be built as the curriculum specifies, and the reason is worth the whole lab

The curriculum sets **"Lab 3: Demonstrate priority inversion and its fix (priority inheritance)."**
The first half works and is spectacular. **The second half cannot be done on these machines**, and
finding out why turned out to be better material than the lab that was asked for.

`RLIMIT_RTPRIO` is **0, soft and hard**, so `sched_setscheduler(SCHED_FIFO)` returns `EPERM`.
Linux implements priority inheritance in `rt_mutex`, which reorders waiters by *realtime* priority;
a `SCHED_OTHER` thread has none, so the protocol has nothing to boost. Measured:

| configuration | H waited |
|---|---|
| baseline, no medium threads | 0.489 / 0.495 / 0.488 s |
| **3 burners, L at nice 19** | **100.607 s** |
| the same, with `PTHREAD_PRIO_INHERIT` | 100.392 s — **no effect** |

And nothing reports a failure: `pthread_mutexattr_setprotocol` returns 0, `pthread_mutex_init`
returns 0, and `pthread_mutexattr_getprotocol` reads back `PRIO_INHERIT`.

**The lab was rebuilt around that** rather than around a demonstration that cannot happen. Students
run a diagnostic first (`rtcheck.c`), predict from it, apply the documented fix, watch it do
nothing, and then apply the two fixes that do work — equal priorities and short critical sections.
The syllabus records the deviation. *(`/etc/security/limits.d/25-pw-rlimits.conf` grants the
`pipewire` group `rtprio 95`, so the mechanism is present and configured for somebody. Granting it
to students was rejected: an unprivileged `SCHED_FIFO` thread that spins wedges a core, and BH 215
is a shared room.)*

### Lab 3 and Midterm 1 are on the same day

[[Year2 - Sophomore/ASSESSMENT CALENDAR|ASSESSMENT CALENDAR]]'s week map puts **Week 4 at Sep 29**, and the midterm row reads
`W4 | Sep 29 | PROG 201 | Midterm 1 | 18:00–19:30 · Weeks 0–3`. [[ACADEMIC CALENDAR]] agrees:
"Mon Sep 29 — PROG 201 Midterm 1". PROG 201's lab is Monday 15:00–16:50 and Lab *N* is sat in
Week *N+1*, so **Lab 3 ends at 16:50 and the paper covering its material starts seventy minutes
later.**

Not resolved here, because nothing is obviously wrong: Lab 3 is the last teaching on Weeks 0–3 and
sitting it three hours before the paper is arguably good. **It is recorded so that whoever
timetables Year 3 sees the pattern**, and because the same shape recurs — CS 211's Midterm 1 is the
Tuesday of Week 4, the afternoon of CS 201's lab. Both the lab sheet and the Week 3 README say so
plainly, so a student is not surprised by it.

*(A first pass at this wrote "Midterm 1 is this Thursday" in the lab sheet, which was wrong twice
over: the registry's model puts it on the Monday, and course material is supposed to quote week
numbers rather than weekdays — §5's rule. Corrected.)*

---

## 9. Every number in Week 3 was measured on the reference machine

Same machine as §6 and §7 — and this week the machine's shape matters to the results, so: **Intel
i5-8250U, 4 physical cores, 8 hardware threads**, cgroup `pids.max` 7,671, `RLIMIT_NPROC` 25,571.

| Claim | Program | Result |
|---|---|---|
| What threads share and what they do not | `shared.c` | one `global`, two `__thread`, **two `errno`**, one file offset, one PID, two TIDs |
| A thread is cheaper than a process, but not by much | `cost.c` | `pthread_create`+`join` **29.21 µs** against `fork`+`wait` **163.64 µs** — 5.6× |
| A bigger stack is address space, not memory | `cost.c` | 64 MiB stack costs 1.8× the default's 29 µs; default stack is 8,192 KiB |
| **A smaller stack does not buy more threads** | `maxthreads.c` | **7,643** threads at 8 MiB, **7,644** at 64 KiB — the limit is the cgroup's `pids.max` of 7,671 |
| The lost-update race, with threads | `race.c` | **70.7% of 800,000** increments lost; Week 2's processes lost 64.7% |
| Wrong is faster than right | `race.c` | unguarded 0.0006 s, mutex 0.0529 s — **88×** |
| What each primitive costs, uncontended | `primcost.c` | plain `++` 1.6 ns · atomic 5.4 · **mutex 8.2** · spin 8.4 · errorcheck 11.3 · rwlock rd 18.6 · sem 19.2 · rwlock wr 28.5 · `getpid()` 568.4 |
| **Wakeups that find nothing to do are common** | `cv.c` | **7.12%** with `signal`, 6.28% with `broadcast`, 8 consumers / 200,000 items |
| glibc's broadcast requeues rather than stampedes | `cv.c` + `strace` | broadcast: 537,988 futex calls in 0.138 s; signal: 423,342 in 0.250 s |
| **One condition variable, two predicates, `signal`** | `onecv.c` | **wedges**; `broadcast` completes 80,000 items |
| A reader-writer lock can be a pessimisation | `rw.c` | **0.52×** a mutex at 2 threads with an empty critical section; **4.15×** with 100 units of work |
| Priority inversion | `inversion.c` | **0.489 s → 100.607 s**, and CFS weights predict 100.6 |
| **`PTHREAD_PRIO_INHERIT` is inert here** | `inversion.c`, `rtcheck.c` | 100.392 s with it; every call returns success |
| The fixes that work | `inversion.c` | nice 0: **1.946/1.947/1.941 s**. 100 chunks: 0.534/0.487/0.899 s. Both: 0.012 s |
| A thread pool against thread-per-task | `pool.c` | **45.6×** at 0 units, 35.6× at 100, 7.3× at 10,000 |
| Pool size follows the cores, not the tasks | `pool.c` | 1→57k, 2→92k, **4→167k**, 8→96k, 16→96k tasks/s |
| A pool with trivial tasks is a lock benchmark | `pool.c` | 1 worker 4.10 M/s falling monotonically to 805 k/s at 8 |
| False sharing | `falseshare.c` | **1.55×** slower below 64 bytes of stride; the step is exactly at the cache line |
| C11 threads are present and less useful | `c11.c` | `<threads.h>` works, and **without `-pthread`** — glibc ≥ 2.34 |

### The three that contradict something

1. **"Reduce the thread stack size to fit more threads."** Standard advice, and it bought exactly
   one extra thread out of 7,643. It is advice about 32-bit address space exhaustion and it is
   thirty years out of date on this machine. The binding limit is the **cgroup**, which nobody
   checks and which Week 11 will explain.

2. **"`broadcast` causes a thundering herd, so prefer `signal`."** glibc's `pthread_cond_broadcast`
   requeues waiters onto the mutex, so broadcast made 27% *more* futex calls and finished in 55% of
   the wall clock. The reason to prefer `signal` is not cost; and there is a case — one condition
   variable serving two predicates — where `signal` **deadlocks** and only `broadcast` survives.
   L11 §5 keeps the rule and replaces its justification.

3. **"Priority inheritance fixes priority inversion."** True, and inapplicable, and silently so.
   This is §8, and it is the deviation recorded in the syllabus.

### A methodological note worth keeping

**`inversion.c`'s critical section had to be a fixed amount of *work*, not a fixed amount of time.**
A first version used `while (elapsed < 0.5)`, and the inversion barely registered — 0.544 s against
a 0.500 s baseline — because starving a thread that loops until the clock says stop changes nothing
about when the clock says stop. With a fixed iteration count the same experiment gives 100.6 s.
The skeleton's `work()` carries a comment saying so, because a student who "simplifies" it back to
a sleep will measure nothing and have no way to know why.

---

## 10. Every number in Week 4 was measured on the reference machine

Same machine as §6, §7 and §9. Two of its properties matter to the results and are recorded here so
a reader knows why their own numbers differ: **7 GiB of RAM with about 2 GiB free**, and
**`/sys/kernel/mm/transparent_hugepage/enabled` set to `madvise`** rather than `always`.

| Claim | Program | Result |
|---|---|---|
| Address space is free | `rss.c` | 4 GiB mapped: `VmSize` 4,098 MiB, **`VmRSS` 1 MiB** |
| Reading untouched anonymous memory is free | `rss.c` | reading 1 GiB of it left RSS at **1 MiB** — the shared zero page |
| Writing is what costs | `rss.c` | writing the same GiB took RSS to **1,025 MiB** |
| **`MADV_DONTNEED` destroys data** | `rss.c` | RSS back to 1 MiB and the first byte reads 0 |
| A minor fault against a store | `faultcost.c` | **1,880 ns** against **18.7 ns** — about 100× |
| A major fault | `faultcost.c` | **563 µs**, from a random walk over a cold file |
| **Readahead decides everything** | `faultcost.c` | same cold 256 MiB: **0.174 s sequential, 1.575 s random** |
| File mappings fault in batches | `faultcount.c` | **132 pages per fault** file-backed; **exactly 1** anonymous |
| `mmap` against `read` | `readvsmap.c` | 0.181 s (4 KiB reads) / 0.057 s (1 MiB reads) / **0.007 s** (mmap) / 0.001 s (`MAP_POPULATE`) |
| `MAP_PRIVATE` writes do not reach the file | `sharedmap.c` | `read()` still returns what the `MAP_SHARED` mapping wrote |
| Writing a file, two ways | `sharedmap.c` | `pwrite`+`fsync` **747 MiB/s**; `MAP_SHARED`+`msync` **948 MiB/s** |
| **The `mmap` threshold is not 128 KiB** | `one.c` | largest `brk` allocation **134,472**, smallest `mmap` **134,473** |
| `malloc` calls the kernel rarely | `where.c` + `strace` | **3 `brk` calls for 6 small allocations**; one `mmap`/`munmap` pair each for 1 MiB and 16 MiB |
| A guard page | `protect.c` | offset 4,092 fine, 4,096 `SIGSEGV` |
| A write barrier | `protect.c` | **7 stores to 4 pages → 4 faults**; the second store to a page is free |
| A JIT is 17 bytes | `jit0.c` | `48 89 f8 48 69 c0 03 …`, `f(10) = 37` |
| **W^X is not enforced here** | `jit0.c` | calling a `W` page and writing an `X` page both `SIGSEGV`; **`PROT_WRITE\|PROT_EXEC` is allowed** |
| Huge pages | `hugepage.c` | **42.7 → 32.3 ns** per random touch, 1.32×, with only **114 MiB of 512** promoted |
| `SIGBUS` from under a live mapping | `truncate.c` | truncate the file and the same read that worked is a **Bus error** |
| An allocator against glibc | `mymalloc.c`, `mtest.c` | **0.88×**, **0.48×**, and **339×** on a fragmenting workload |
| A JIT against an interpreter | Lab 4's `jit.c` | JIT 2.08–2.22 ns, C loop 2.08–2.09 ns (**a tie**), bytecode VM 11.38–11.63 ns (**5.5×**) |

### The three that contradict something

1. **"`malloc` switches to `mmap` at 128 KiB."** Documented, and the measured boundary is
   **134,473** — 3,401 bytes higher — because the threshold applies to the *chunk* after the top
   chunk has failed, and glibc had already grown the arena to 132 KiB. It also **moves at runtime**:
   glibc raises it, up to 32 MiB, when it sees large blocks freed. L14 §4 states the documented
   number, the measured one, and the reason they differ.

2. **"Reduce the stack size / mapping size to save memory."** `rss.c` shows the mapping is not the
   cost — 4 GiB of address space cost 1 MiB of RSS, and reading a gigabyte of it cost nothing at
   all. This is Week 3's thread-stack finding (§9) with the mechanism made visible, and the two are
   cross-referenced in both lectures.

3. **"A JIT is faster than compiled code."** Measured, the JIT **tied** `gcc -O2` and beat the
   bytecode VM by 5.5×. The tie is not a defect in the emitter: the coefficients are `const` at
   file scope, so gcc had already specialised `horner` exactly as the JIT does. Lab 4 Q6 is built
   on this, and the lab extension — coefficients from `argv` — is the case where the compiler
   genuinely cannot know.

### One thing the curriculum lists that cannot be done as written

The Week 4 syllabus includes **"memory-mapped I/O for device registers"** and **"writing to and
reading from specific virtual addresses that the hardware monitors"**. On BH 215 that needs
`/dev/mem` (root, and disabled by `CONFIG_STRICT_DEVMEM` on this kernel) or a VFIO/UIO binding to a
real device, neither of which is available to a student account or appropriate on a shared machine.

**L15 §8 covers it as a reading rather than an exercise** — the physical-address mapping, why
`volatile` is necessary and why it is not sufficient, and where `readl`/`writel` come in. The
practical work in that lecture is `mprotect` and the JIT, which exercise the same API. Recorded in
the syllabus as a deviation.

### A methodological note, and it caught three programs

**Every timing loop this week had to have its result printed.** Three of the measurement programs
first reported `0.000 s` — `readvsmap.c`, `falseshare.c` in Week 3, and `faultcost.c`'s random walk
— because the accumulator was never used afterwards and gcc deleted the loop. The first version of
`readvsmap.c` also reported **0 minor faults for a 512 MiB mapping**, which should have been the
tell rather than the timing.

The rule the build now follows: **a benchmark that reports an impossible number is reporting that
it did not run.** Print the checksum, and check the fault count against the page count before
believing the seconds.

---

## 11. Lab 5's tool is not installed, so the lab builds it

The curriculum sets **"Lab 5: Stress test the HTTP server with Apache Benchmark (ab)."** `ab` ships
in `apache2-utils`, which is **not on the BH 215 image**, and a student account cannot install it.
`wrk` and `siege` are absent too; `curl` and `ss` are present.

**Rebuilt as "write the load generator".** Students implement an event-driven benchmark client —
non-blocking `connect` with `EINPROGRESS`, `SO_ERROR` after `EPOLLOUT`, `EAGAIN` on both sides, and
a slot-per-connection state machine — which is precisely L18 §4, and which `ab` would have hidden.
The server is provided complete so the lab measures rather than builds; PS 5's server is a
different program (it parses requests and serves files).

This is a better lab than the one specified, and it is worth saying why rather than only that it is
different: **a benchmark you did not write is a benchmark whose numbers you cannot defend**, and
three of this week's results — the two 434s, the 7,637, and the 11,261 `TIME_WAIT`s — are results
about the *measurement* as much as about the servers.

Recorded in the syllabus. If `apache2-utils` is ever added to the image, the lab does not need to
change: comparing your generator against `ab` becomes the natural extension.

### Lab 5 and PS 5 collide, and this one is worth flagging

Lab 5 is the term's only Friday lab (§2 — the Monday of Week 6 is Fall Break), sat **16:00–17:50 on
the Friday of Week 6**. [[Year2 - Sophomore/ASSESSMENT CALENDAR|ASSESSMENT CALENDAR]] puts **PS 5 due at 17:00 that Friday**, so the
deadline falls while the students are in the lab.

**Not resolved here**, on the same grounds as §8's midterm collision: nothing is obviously wrong,
the two pieces of work are independent, and moving either has costs. Both the lab sheet and PS 5
say plainly "submit before you come to the lab". **The cheap fix, if anyone wants one, is to move
PS 5's deadline to 23:59 that day** — it costs nothing, since no marking begins that evening, and
it removes the only case this term where a deadline lands inside a scheduled session.

This is the second Week-*N* collision found by building the material rather than by reading the
calendar (§8 was the first). Worth checking Weeks 6–12 for a third before Year 3 is timetabled.

---

## 12. Every number in Week 5 was measured on the reference machine

Same machine as §6, §7, §9 and §10. **All traffic is loopback**, which removes the network as a
variable and flatters every model equally; the orderings transfer and the absolute rates do not.
Relevant settings: `somaxconn` 4,096, `RLIMIT_NOFILE` 1,048,576, ephemeral range 32768–60999
(28,232 ports), `tcp_fin_timeout` 60.

| Claim | Program | Result |
|---|---|---|
| The listen queue holds `backlog+1` | `backlog.c` | `listen(4)` → **5** immediate; `listen(16)` → **17** |
| Past the queue, SYNs are dropped, not refused | `backlog.c` | the rest hang for 2 s and time out; no `ECONNREFUSED` |
| `TIME_WAIT` holds the address | `reuse.c` | rebind fails `EADDRINUSE` without `SO_REUSEADDR`, succeeds with it |
| **`TIME_WAIT` at scale** | `ss` after a run | **11,261** after 20,000 requests, against 28,232 ephemeral ports |
| Trivial work: the architecture does not matter | `server.c`, `load.c` | iter **46,810**, fork 15,038, thread 39,186, pool 50,687, epoll 42,985 req/s |
| **A blocking handler blocks an event loop** | same | 2 ms of work: iter **434**, thread 18,214, pool(8) 3,469, **epoll 434** |
| CPU work wants a pool sized to cores | same | 500 µs: pool(8) **12,761**, thread 7,004, epoll 1,887 |
| Pool size follows the work | same | 2 ms blocking: 1→437, 8→3,487, 32→14,085, 64→14,471, **128→18,667** |
| **C10K, the event-driven side** | `hold.c` | **20,000 connections, RSS 1,416 → 1,416 kB** |
| **C10K, the thread side** | `hold.c` | `pthread_create` failed after **7,637** with `EAGAIN`; RSS → 64,864 kB |
| `poll` is O(watched), `epoll` is O(ready) | `readiness.c` | 16,000 fds: poll **4,827 µs**, epoll **0.89 µs**; at 10 fds epoll is 0.72 µs |
| **`select` cannot be used above 1024** | `readiness.c` | glibc aborts: *"bit out of range 0 - FD_SETSIZE on fd_set"* |
| Nagle plus delayed ACK | `nagle.c` | **38.963 ms** per round trip against **0.209 ms** with `TCP_NODELAY` — 186× |
| A peer that stops reading | `slowreader.c` | **2,625,024 bytes (2.50 MiB)** absorbed, then `EAGAIN` forever |
| Copies cost | `zerocopy.c` | `read`+`write` 2,444 MiB/s · `mmap`+`write` 3,043 · **`sendfile` 4,456** |
| **And `sendfile` is also the smallest** | `zerocopy.c` | `ru_maxrss` 1,768 kB · **132,716 kB** · 1,640 kB |
| Path traversal is stopped by resolving | `httpd.c` | `..`, `%2e%2e` and a symlink to `/etc/passwd` all → 404 |

### The three worth arguing with

1. **"Use `epoll`, it scales."** True of *waiting* and false of *working*. An event loop with a 2 ms
   blocking call in the handler served **434 requests per second — the same as a `for` loop.**
   L17 §5 is built on it, and it is the week's headline.

2. **"Thread-per-connection does not scale."** True, and the reason is not what people say. It is
   not memory — 3.2 kB per connection — it is the **task-count ceiling**, and this machine's is the
   cgroup `pids.max` that Week 3 §9 already measured at 7,643. The two numbers, 7,643 and 7,637,
   were reached three weeks apart by completely different programs.

3. **"Benchmark it and pick the fastest."** With a trivial response the **iterative server came
   second of five**. Every architectural difference in this week appears only when the handler does
   something, and the "Hello, world" case — the one everybody publishes — is the one case where the
   answer is "it does not matter".

### A measurement that was contaminated, and how it showed

`zerocopy.c` first reported `ru_maxrss` of **132,908 kB for all three methods**, including
`sendfile`, which never brings the file into the process. `ru_maxrss` is a **high-water mark for the
life of the process**, so running all three in one process reports the largest of them three times.
Re-run one per process, the numbers are 1,768 / 132,716 / 1,640 kB and the point of `sendfile`
becomes visible.

**PS 5 Q4(c) now requires separate processes and says why**, and the solutions award credit to a
student who makes the mistake, notices the number is impossible, and re-runs. It is the same
lesson as Week 4's deleted timing loops: *a benchmark that reports an impossible number is
reporting that it did not measure what you think.*

---

## 13. PS 6 and Project 1 are the same program, so the build split them

The curriculum lists, in the same week:

- **"Problem Set 6: Implement a shell (tsh) with pipelines, I/O redirection, background jobs."**
- **"Project 1 assigned"** — which [[Year2 - Sophomore/ASSESSMENT CALENDAR|ASSESSMENT CALENDAR]] names as *Unix shell (tsh)*, due W9, worth 12.5%.

**That is one deliverable asked for twice**, three weeks apart, and setting both as written would have students submit the same program in Week 7 and again in Week 9.

**Resolved by splitting it along the seam the material already has:**

| | Scope | Due |
|---|---|---|
| **PS 6** | tokeniser, parser, *n*-stage pipelines, four redirections, `&`, builtins. **Job control explicitly out of scope** | Friday of Week 7 |
| **Lab 6** | the job table, `jobs`/`fg`/`bg`, `WUNTRACED`, `tcsetpgrp` — on a provided skeleton | Monday of Week 7 |
| **Project 1** | the complete shell: PS 6 + Lab 6 + robustness + a test suite + a write-up | Friday of Week 9 |

PS 6 tells students to write it so Project 1 can build on it; Project 1 says reusing their own PS 6 and Lab 6 **in full** is expected and is what those pieces were for. The PS 6 solutions tell markers **not to award marks for job control appearing early** — a student who spent that week on `fg` has usually done the parser thinly.

This preserves the curriculum's totals (PS 6 is still a problem set, Project 1 is still 12.5%) and its topics, and removes the duplication. **The alternative — making PS 6 something other than a shell — was rejected** because the curriculum's Week 6 has no second topic and the shell is what the lectures build toward.

---

## 14. Every number in Week 6 was measured on the reference machine

Same machine as §6, §7, §9, §10 and §12. **Everything in this week needs a controlling terminal**;
the session runs non-interactively, so the job-control experiments were driven through a
pseudo-terminal (`script -qc`, and Python's `pty.fork()` for the scripted ones). A pty behaves
identically to BH 215's terminals for every property this week uses.

| Claim | Program | Result |
|---|---|---|
| `fork` inherits the group and session | `groups.c` | child pgid = sid = parent's; still foreground |
| `setpgid(0,0)` leaves the foreground | `groups.c` | new pgid, same sid, `tcgetpgrp` is now somebody else's |
| **`setsid()` loses the controlling terminal** | `groups.c` | new pgid **and** sid, and **`tcgetpgrp` returns −1** |
| A pipeline is one group | `groups.c` | two stages, different pids, **pgid = stage 0's pid** |
| **A background group may not read** | `ttyctl.c` | `read` → **stopped by `SIGTTIN`** |
| ...may write, by default | `ttyctl.c` | `write` → **exited 0**; with `TOSTOP` set → stopped by `SIGTTOU` |
| ...and may never change terminal settings | `ttyctl.c` | `tcsetattr` → **stopped by `SIGTTOU`, regardless of `TOSTOP`** |
| The minus sign is the difference | `groupsig.c` | `kill(pid)` hit 1 of 3; `kill(-pgid)` hit all 3 and left another group alone |
| **A builtin against an external command** | `tsh` | 2,000 builtins in **under 10 ms**; 2,000 `/bin/true` in **1.91 s** — 955 µs each |
| Where the 955 µs goes | `cmdcost.c` | `fork`+`_exit`+`wait` **127.1 µs**; +`exec /bin/true` **779.2 µs**; `/bin/sh -c` **919.2 µs** |
| **The dynamic linker's share** | `cmdcost.c` | trivial binary **dynamic 679.3 µs**, **static 532.4 µs** — 147 µs, 22% |
| Job control, end to end | `tsh` over a pty | Ctrl-Z reports `Stopped`; `bg` resumes; a 3-stage pipeline is one job; Ctrl-C kills the job and the shell survives |

### The bug the reference shell had, kept as the lab's set piece

The obvious way to attribute a reaped process to a job is

```c
pid_t p = waitpid(-1, &st, ...);
struct job *j = job_by_pgid(getpgid(p));      /* <- wrong */
```

and it **silently does not work**: `waitpid` has just reaped `p`, so `getpgid(p)` fails with
`ESRCH`. The symptom in the reference was exact and unhelpful — `kill %1` genuinely killed the
process and `jobs` listed it as Running for ever.

The fix is to record every pid in the job and look up by pid. **Lab 6 keeps the trap**: the skeleton
provides `job_by_pid` as the stub to implement and the lab sheet says only that it is "by PID and
not by pgid — L21 §5 says why, or find out for yourself". It is Q4, and the solutions tell TAs to
let students reach it rather than warning them.

It is the same class as Week 1's `lseek`-then-`write` and PS 5's `stat`-then-`open`: **a question
about a thing that changed between the asking and the using.**

### Two other findings worth recording

**A shell must tolerate already being a session leader.** `setpgid` fails with `EPERM` on a session
leader, and a shell started under `script` or `pty.fork()` already is one. The reference exited with
`setpgid: Operation not permitted` the first time it was driven over a pty; the fix is a
`getpgrp() != shell_pgid` guard. **Project 1's marking notes make this a test**, because it is
exactly the failure a student who only ever ran their shell by hand will have.

**`WUNTRACED`'s absence is a hang, not an error.** The Lab 6 skeleton deliberately ships without it,
and the first thing the lab does is press Ctrl-Z and watch the shell stop responding — with both
processes behaving correctly and nothing to see in the shell's own output. `ps -o stat` showing `T`
and `S` is the whole diagnosis, which is why the week's habit is the process table.

---

## 15. The lab/midterm collision is systematic, not accidental

§8 recorded that **Lab 3 and Midterm 1** fall on the same Monday. §11 recorded that **Lab 5 and PS 5's
deadline** fall on the same Friday. Building Week 7 produced the third:

| | Lab | Midterm |
|---|---|---|
| Monday of Week 4 | **Lab 3**, 15:00–16:50 | **Midterm 1**, 18:00–19:30 (Weeks 0–3) |
| Monday of Week 8 | **Lab 7**, 15:00–16:50 | **Midterm 2**, 18:00–19:30 (Weeks 4–7) |

**This is not a coincidence and it will recur every year.** PROG 201's lab is on a Monday
([[Year2 - Sophomore/ROOM ASSIGNMENTS|ROOM ASSIGNMENTS]]) and both its midterms are on Mondays ([[Year2 - Sophomore/ASSESSMENT CALENDAR|ASSESSMENT CALENDAR]]), so **every
midterm collides with a lab**, and it is always the lab covering the last week the paper examines.

Still not resolved here, for the reason §8 gave: the lab is the last teaching on the paper's
material and sitting it three hours before is arguably good. But **it should be a timetabling
decision rather than an accident**, and the pattern is now stated once rather than being
rediscovered per week. Three cheap fixes, in increasing cost:

| Option | Cost |
|---|---|
| Move both midterms to the **Tuesday** evening | CS 211's Midterm 1 is already Tuesday of Week 4; two papers in one evening |
| Move both midterms to the **Wednesday** evening | MATH 241's Midterm 1 is Wednesday of Week 6, but not Weeks 4 or 8 — **this one is free** |
| Move the lab in those two weeks | Breaks the "labs are Mondays" rule the whole course is built on |

**The Wednesday option is available in both weeks** and costs nothing that the calendar shows.
Recorded for whoever timetables Year 3; the Week 4, 7 and 8 material all says plainly that the two
land together, so no student is surprised by it in the meantime.

---

## 16. Every number in Week 7 was measured on the reference machine

Same machine as §6, §7, §9, §10, §12 and §14. Root filesystem is **ext4 on NVMe, mounted
`noatime`**, which matters for two of these. **Nothing this week needed root**: `mke2fs`, `debugfs`,
`dumpe2fs`, `e2fsck` and `tune2fs` all operate on an ordinary file, and only `mount(8)` does not —
so the whole of Lab 7 runs from a student account, which is what made the lab possible at all.

| Claim | Program | Result |
|---|---|---|
| One API over many filesystems | `vfs.c` | six `f_type`s from one `statfs`; **`proc` and `sysfs` report 0 blocks** |
| **`st_size` is a lie on `procfs`** | `vfs.c` | `/proc/self/stat`: `st_size` 0, and `read` returns 40 bytes |
| Two names, one inode | `links.c` | `a.txt` and `b.txt` share inode 3539906, `links 2` |
| Removing a name is not deleting a file | `links.c` | hard link survives with `links 1`; the symlink **dangles** |
| Blocks are freed on the **last close**, not the last unlink | `links.c` | readable through the descriptor; `/proc/self/fd/3 -> ... (deleted)` |
| Link restrictions | `links.c` | hard link to a directory → **`EPERM`**; symlink → allowed |
| **A short symlink lives in the inode** | `debugfs` | 14-byte target: `Blockcount: 0`, `Fast link dest`. 75-byte target: 1 block |
| **ext2's indirect blocks** | `debugfs` on an ext2 image | 5,000,000 B: `12 direct + IND + DIND + 19 IND`; 4,883 data + **21 pointer blocks** |
| 256 pointers per 1 KiB block | `debugfs` | each `(IND)` covers exactly 256 blocks; max file **16 GiB** at 1 KiB blocks |
| **ext4's extents** | `debugfs` | the same file in **2 records, 0 pointer blocks**; a 200,000 B file in **one** |
| Filesystem overhead | `dumpe2fs` | 7,451 of 65,536 blocks — **11%** on 64 MiB, mostly the inode table |
| Backup superblocks | `dumpe2fs` | 8193, 24577, 40961, 57345 |
| **Recovery from a backup** | `dd` + `e2fsck` | primary zeroed → "Bad magic number"; `e2fsck -fy -b 8193` → every file back |
| **The journal is a file** | `debugfs`, `tune2fs` | inode 8, 4,194,304 B; `-O ^has_journal` reclaims exactly 4,096 blocks = **6.2%** |
| `fsck` finds a link-count error | `e2fsck` | "Inode 13 ref count is 1, should be 2" — **pass 4**; rc=**4** with `-fn`, rc=**1** with `-fy` |
| **`fsck` does not check data** | `dd` + `e2fsck` | 1 KiB of a file replaced with noise → **clean, rc=0** |
| **One directory block destroys every name** | `dd` + `e2fsck` | root dir block corrupted → clean filesystem, **every file in `lost+found` as `#11`…`#17`** |
| **Durability costs 154×** | `durable.c` | 41,980 rec/s buffered against **255** with `fsync` per record |
| `fdatasync` only wins when the size does not change | `durable2.c` | appending: 3.67 vs 3.91 ms. **In place: 1.26 vs 4.11 ms — 3.3×** |
| The directory `fsync` doubles a safe write | `durable2.c` | 4.17 ms → **8.05 ms** |

### The two that make the lab

**Corrupting 1,024 bytes of a file's data leaves `e2fsck` reporting a clean filesystem** (rc=0), because
data integrity is not one of the invariants a filesystem check verifies — ext4 checksums its
metadata (`metadata_csum`) and nothing else. **Corrupting 1,024 bytes of the root directory** loses
every name in the filesystem while every file survives intact: `e2fsck -fy` salvages the directory,
finds seven unreferenced inodes, and files them in `lost+found` as `#11` through `#17`, with
`#15` being all 5,000,000 bytes of `huge.bin`.

The pair is the lab's argument: **`fsck` restores the filesystem, not your data**, and in the second
case the names were unrecoverable *in principle* — an inode does not contain a name, so once the
directory block is gone there is nowhere else to look.

### A note on `verify.sh`

The provided checker verifies **sizes and structure, not contents**, so it passes the data-block
corruption. That is deliberate and the solutions tell TAs to reward a student who notices — adding
a checksum check is the extension. It is the same shape as Week 4's contaminated `ru_maxrss` and
Week 5's "Hello, world" benchmark: **a check that passes is a fact about the check.**

---

## 17. Every number in Week 8 was measured on the reference machine

Same machine as §6, §7, §9, §10, §12, §14 and §16. **Two properties of this system are load-bearing
this week and would change the results elsewhere**: it is **glibc 2.39**, and Ubuntu builds
everything with **`-Wl,-z,relro,-z,now`**.

| Claim | Program | Result |
|---|---|---|
| Static against dynamic, size | `hello.c` | **785,232 bytes** static, **16,056** dynamic — 49× |
| Static against dynamic, startup | `startup.c` | static 503/571/750 µs, dynamic 852/881/948 µs over three paired runs |
| A binary names its own loader | `readelf -l` | `INTERP` → `/lib64/ld-linux-x86-64.so.2` |
| **`linux-vdso.so.1` is not a file** | `ldd` | mapped by the kernel; no such path exists |
| A cross-library call is an indirect jump | `objdump -d -j .plt.sec` | `greet@plt: jmp *0x2f3e(%rip)` through a GOT slot |
| **The lazy GOT slot points at its own PLT stub** | `readelf -x .got.plt` | slots contain **`0x1030`** and **`0x1040`** — the PLT entries themselves |
| **Lazy binding is OFF by default here** | `readelf -d` | `FLAGS: BIND_NOW`, `FLAGS_1: NOW PIE` |
| Lazy resolves at first call | `LD_DEBUG=bindings` | `greet` binds between the first and second call; `farewell` only when called |
| `BIND_NOW` resolves before `main` | `LD_DEBUG=bindings` | both bindings precede the program's first output |
| **`-fPIC` costs one extra load** | `objdump -d` | PIC: `mov (%rip),%rax` then `mov (%rax),%eax`. Non-PIC: one `mov` |
| A non-PIC object cannot be shared | `ld` | `relocation R_X86_64_PC32 ... can not be used when making a shared object` |
| **glibc 2.34 merged the small libraries** | `ls` | no `libdl.so`, `libpthread.so` or `librt.so` at all |
| Interposition works | `faketime.so` | `time()` returns 1000000000; `LD_DEBUG` shows the bind going to `faketime.so` |
| **...and does nothing to `date`** | `faketime.so` | `date` prints the real time — it calls `clock_gettime` via the vDSO |
| **`-O2` deletes the allocations** | `mtrace.so` | `-O0`: **1,012 malloc, 1,000 free**. `-O2`: **2** — and `nm -D` shows the binary does not reference `malloc` at all |
| A real program's profile | `mtrace.so` | `python3 -c pass`: 2,285 malloc, 12 calloc, 174 realloc, 2.74 MB, 21 unfreed |
| **`ld.so` runs no destructors for some programs** | `probe.so`, `LD_DEBUG=all` | fini runs for `true` and `python3`; **none at all for `ls` and `grep`** |
| One libc holds several versions of a symbol | `nm -D --with-symbol-versions` | `memcpy@GLIBC_2.2.5` **and** `memcpy@@GLIBC_2.14`; 41 version definitions |
| Constructor and destructor order | `order.c` | ctor: `b`, `a`, preload, main. dtor: exact reverse |
| A plugin can export exactly one symbol | `nm -D` | `-fvisibility=hidden` + one `visibility("default")` → 1 line |
| `dlopen` cost | `host.c` | 2 plugins in **0.211 ms** |

### The one that contradicts the curriculum

**The Week 8 Core Concept describes lazy binding as how dynamic linking works** — the PLT stub, the
first call, the resolver patching the GOT. That mechanism is real and is in the lecture, **and it is
not what happens on these machines**: every binary is built `-z relro -z now`, so all symbols bind
before `main` and the GOT is then made read-only.

The lecture teaches both, in that order, and says why the default changed: **a writable GOT is what
a GOT-overwrite attack needs**, which is Week 10's subject. Lab 8 has students build the same
program twice — once with `-z lazy -z norelro` — so they see the mechanism in the bytes and then see
that their own binaries do not use it. Recorded in the syllabus.

### Two findings that became PS 8's Q4

**`-O2` deleted every allocation.** A test program with 1,000 `malloc`/`free` pairs contains **no
reference to `malloc` at all** after optimisation — not merely no calls, but no undefined symbol.
The profiler correctly reported almost nothing, and nothing in its output could distinguish that
from a program that genuinely allocates nothing.

**`ld.so` runs no fini functions for `ls` or `grep`.** A `LD_PRELOAD` tool reporting from
`__attribute__((destructor))` therefore prints nothing for them, silently. **Interposing `_exit`
does not rescue it** — tried, and it does not, because a library's internal calls do not go through
the PLT. The remedy the solutions ask for is incremental output.

Both are the term's recurring shape — *a measurement that produces nothing is a fact about the
measurement* — and Quiz 8's closing note counts this as its fifth appearance, after Week 2's untorn
records, Week 4's 339×, Week 5's "Hello, world" benchmark and Week 7's clean `fsck`.

### And a third scheduling collision

**PS 8 and Project 1 are both due at 17:00 on the Friday of Week 9.** PS 8 is released in Week 8 and
is roughly four hours of work; Project 1 is three weeks of it. Both papers say so, and PS 8 tells
students to do it in Week 8 and leave Week 9 for the shell.

Not resolved, and unlike §15's lab/midterm pattern this one is a genuine choice rather than a
structural consequence: the problem-set rhythm is "released Wednesday of week *N*, due Friday of
week *N+1*", and Project 1's due date comes from the curriculum. **The cheap fix is to release PS 8
a week earlier or make it the term's dropped problem set by design.** Recorded for Year 3.

---

## 18. `perf` does not work on these machines, and the week is better for it

The curriculum's Week 9 is built on **`perf`**: "CPU profiling with perf: call graphs, hot paths",
and the Core Concept describes a sampling profiler in terms of it. On BH 215:

```
$ perf stat -e task-clock ./prog
perf_event_paranoid setting is 4:
```

**`kernel.perf_event_paranoid` is 4**, which refuses everything — not merely kernel profiling but a
`task-clock` count on the caller's own process. Ubuntu ships it that way because performance
counters are a demonstrated side channel, and lowering it needs root on a shared machine.

**Three things that need no privileges were used instead**, and between them they cover the
curriculum's topics:

| | covers |
|---|---|
| **Callgrind** (`valgrind --tool=callgrind`) | exact call graphs and hot paths, with source annotation |
| **Cachegrind** (`--cache-sim=yes`) | the curriculum's "cache profiling with valgrind cachegrind", unchanged |
| **A sampling profiler the students write** | the sampling half, from the mechanism up |

**The third is the improvement.** `setitimer(ITIMER_PROF)` plus a `SA_SIGINFO` handler that reads
`REG_RIP` out of the `ucontext` is a sampling profiler in about sixty lines, and building one
teaches what `perf` hides: why sampling is statistical (five runs of one program gave `slow` between
**62.31% and 76.12%**), why the handler must be async-signal-safe (Week 0 L03), and why it cannot
name a static function without `-rdynamic` — **1 dynamic symbol against 14**, measured, which is
Week 8's visibility lecture arriving as a tooling failure.

Its honest limit is recorded too: profiling the PS 9 program, the hand-written sampler attributes
**74.88% to "libc.so.6"** where Callgrind says `__strcmp_avx2`, because glibc resolves `strcmp`
through an IFUNC to a symbol `dladdr` cannot see. **Both profiles are in the solutions**, and
comparing them is PS 9 Q1(c).

Recorded in the syllabus. If `perf_event_paranoid` is ever lowered on the lab image, nothing needs
to change — running `perf` alongside becomes the natural extension.

---

## 19. Every number in Week 9 was measured on the reference machine

Same machine as §6, §7, §9, §10, §12, §14, §16 and §17: **Intel i5-8250U, 4 cores / 8 threads,
32 KiB L1d, 256 KiB L2, 6 MiB L3**, gcc 13.3.0, Linux 7.0.0-30. The cache sizes matter to half of
these.

| Claim | Program | Result |
|---|---|---|
| **Flags against algorithm** | `slow.c` | every `-O` level spans **2.78 → 2.33 s (19%)**; three source changes give **2.31 → 0.03 s (77×)** |
| Once the algorithm is right, flags stop mattering | `fast.c` | `-O0` 0.05 s, `-O3` 0.04 s |
| **`-O3` can be slower than `-O2`** | `slow.c` | 2.38 s against 2.35 s |
| Callgrind names the hot path exactly | `callgrind_annotate` | **61.59% `__strcmp_avx2`**, 31.32% inlined into `main` |
| Cachegrind's miss rate is derivable | `--cache-sim=yes` | **D1 miss rate 6.2%** on a sequential `int` scan = **1/16** |
| **A sampling profiler in sixty lines works** | `sprof.c` | 78.50% / 20.00% / 1.50% across three functions of known cost |
| Sampling is statistical | `sprof.c` | five runs: `slow` **62.31%–76.12%**, `quick` **1.00%–7.04%** |
| It cannot name static functions | `sprof.c` | without `-rdynamic`: **100% attributed to the executable**; 1 dynamic symbol against 14 |
| It cannot name libc's IFUNC internals | `sprof.c` | **74.88% "libc.so.6"** where Callgrind says `__strcmp_avx2` |
| **The hierarchy** | `cache.c` | L1 **1.49 ns**, L2 3.13, L3 11.84, DRAM **141.94** — a factor of **95**, steps on the documented sizes |
| **The cache line, and the prefetcher** | `cache.c` | stride 1 **1.09 ns**, stride 16 (64 B) **6.33**, and **flat at 14.5 from stride 32 (128 B)** |
| **The two ceilings** | `roof.c` | **13.71 GB/s** and **13.50 GFLOP/s**, ridge point **0.98 flops/byte** |
| A memory-bound kernel at its roof | `roof.c` | `axpy` **99%** |
| A compute-bound kernel far from it | `roof.c` | `poly(deg 16)` **18%** |
| **Dependency chains, which the roofline cannot model** | `roof.c` | same AI, same flops: **2.47 against 7.14 GFLOP/s — 2.9×** |
| **`-O2` does not vectorise; `-O3` does** | `vecbench.c` | 0 SIMD instructions against 10; **8.37 → 14.53 GB/s** (64 MiB) and **9.68 → 46.28** (16 KiB) |
| Float reductions need permission | `gcc -S` | `-O3` 10 SIMD instructions in the float sum, `-O3 -ffast-math` **14** |
| **PGO doing nothing, correctly** | `fast.c` | 0.0380 s with and without |
| The timer is too coarse | `/usr/bin/time` | ten runs of a 30 ms program: `0.03 0.03 0.04 0.04 0.03 …` |
| **The staged breakdown** | `st1/st2/st3.c` | hash table **23×**; `normalise` +10%; score bucketing **3× of what remained** |

### The bug this week was written with, kept as the lab

The first version of `roof.c` measured memory bandwidth as

```c
for (size_t i = 0; i < n; i++) s += a[i];
```

and reported **6.28 GB/s** — after which the kernel table showed `axpy` achieving **222% of the
roof**, which cannot happen. A single-accumulator reduction is a **dependency chain** bounded by
floating-point add latency, not by memory; with eight accumulators the same loop reads **13.71
GB/s** and every kernel falls below 100%.

**Lab 9 is built on it.** TODO 1 tells students to write the obvious loop first, note the number,
and then find the row above 100%. The same mistake then appears deliberately as a kernel — `sum
(1 acc)` at 45% — and again in L30 §3, where it turns out to be exactly what `-O2` was doing wrong
in the vectorisation comparison. **Three appearances of one idea, and the first one was an
accident.**

### Amdahl, in the direction people forget

The staged measurements show `compute_scores` as **0.055 s of 2.351 — 2.3%, correctly ignored** in
the first profile, and then as **a third of the remaining runtime** once the hash table is in. The
solutions ask markers to reward a student who re-profiled and noticed; most re-profile and do not
remark on it.

### And the running count

Quiz 9's closing note makes this the term's **sixth** instance of *a measurement that produces
nothing, or something impossible, is a fact about the measurement*: Week 2's untorn records, Week
4's 339× allocator and deleted timing loops, Week 5's "Hello, world" benchmark, Week 7's clean
`fsck` on a corrupted file, Week 8's profiler reporting two allocations, and now Week 9's 222% of a
roofline. **The Week 9 README tabulates all five of the numeric ones**, because by this point in
the course the pattern is worth naming rather than rediscovering.

---

## 20. Week 10 needed four tool substitutions, and the sandbox is real

Week 10 is exploitation and defence. Four of the tools the curriculum names are not on the BH 215
image and a student account cannot add them, and one hardware feature the lecture discusses is
absent from the CPUs. All are handled the way the rest of the course handles missing tools — build
or substitute, and record it.

| Curriculum names | On the machine | Substitute |
|---|---|---|
| **ROPgadget** / ropper | neither installed | a **40-line gadget finder** (`gadget.py`), byte-scan for sequences ending in `ret` |
| **checksec** | not installed | a **10-line `checksec.sh`** reading `readelf`/`objdump` |
| **AFL** | not installed | **libFuzzer** (`clang -fsanitize=fuzzer`), coverage-guided, same idea |
| **Intel CET** shadow stack | **CPU has no `shstk`/`ibt`** | discussed and measured as *present-but-inert* |

**The sandbox is `setarch -R` and course-supplied binaries.** `setarch -R` sets
`ADDR_NO_RANDOMIZE` for a single process — measured, the stack sits at a fixed `0x7fffffffd340`
every run under it and randomises without it — and **the machine-wide `randomize_va_space` (which is
2) is never touched**. The targets are compiled with protections removed on purpose. The syllabus,
the lab and PS 10 all state the bounds, and PS 10's last mark-bearing part is turning every defence
back on.

---

## 21. Every result in Week 10 was measured on the reference machine

Same machine as the earlier weeks: Intel i5-8250U, gcc 13.3.0, glibc 2.39, clang, Linux 7.0.0-30,
`randomize_va_space` 2. **The target is non-PIE, so its addresses are deterministic** — `unlock`
0x4011f6, `pop rdi ; ret` 0x40125a, bare `ret` 0x40125c — which is what lets the lab and PS run
without a per-build address hunt.

| Claim | How | Result |
|---|---|---|
| Overflow reaches the return address | marker + gdb | offset **72** (64-byte buf + 8-byte saved rbp) |
| **The stack canary catches the exploit** | `vuln_canary` | `*** stack smashing detected ***`, **exit 134** |
| **NX turns shellcode into a fault** | shellcode on a `RW` stack | **SIGSEGV, exit 139** |
| shellcode would run on an exec stack | `-z execstack` | the `RW`→`RWE` bit is the only difference |
| **A 3-gadget ROP chain spawns a shell** | `exploit.py` | `[unlock] correct key`, then `uid=1000` in the shell |
| `system` needs 16-byte alignment | drop the align gadget | crash **inside `system` on a `movaps`** |
| **A CET-compiled libc has almost no clean gadgets** | byte scan of static libc | **zero** `pop rdi ; ret` (`5f c3`) sites; the target ships its own |
| **ASLR without PIE leaves the chain working** | run `vuln` with ASLR on | still `[unlock] correct key` |
| **PIE + ASLR breaks it** | `vuln_pie` | SIGSEGV; hardcoded 0x4011f6 is not where `unlock` is |
| ASLR is on/off per process | `setarch -R ./leak` | fixed `0x7fffffffd340`; randomises without `-R` |
| **`%p` leaks the stack** | `./fmt '%p %p …'` | live addresses, and the input string as `0x7025207025207025` |
| **`%n` is a write primitive** | `./fmt 'AAAAAAAA%7$n'` | SIGSEGV writing through the controlled slot |
| **Heap bugs are silent without a sanitizer** | `heap_plain` | use-after-free **rc=5**, double-free **rc=0** — both clean |
| ASan catches them | `-fsanitize=address` | heap-use-after-free and double-free, both sites named |
| **CFI catches a type-confused call** | clang `-fsanitize=cfi` | *"control flow integrity check for type 'int (int, int)' failed"*, names `evil` |
| **CET markers are present but inert** | `objdump`, `/proc/cpuinfo` | **24 `endbr64`** in `vuln`; **no `shstk`/`ibt`** — nothing enforces them |
| **libFuzzer finds a planted bug** | `-fsanitize=fuzzer,address` | heap-buffer-overflow at **`parser.c:28`**, 13-byte reproducer, ~10 execs with a seeded corpus |

### Two "present but not working" findings, and a pattern completed

Two of this week's measurements are the same shape as Week 3's `PRIO_INHERIT` (accepted, inert) and
Week 8's lazy binding (documented, switched off):

- **ASLR is on and does nothing to a non-PIE binary's code** — the exploit runs with randomisation
  fully enabled, because only the stack, heap and libraries moved and the chain uses none of them.
- **The compiler emits CET `endbr64` markers into every binary, and the CPU cannot enforce them** —
  so the shadow stack that would stop the ROP chain is compiled-for and absent.

Both are in the README's "one thing to take from this week" table, because the course now has a
named recurring lesson — **a mechanism being present is not the same as it working** — appearing in
Weeks 3, 8 and 10, and it is the whole justification for the week's teach-by-watching-it-fail method.

### On teaching exploitation, for the record

The department teaches this because it is bounded and defensive: a binary the course wrote, a
sandbox the student controls, and a stated purpose that PS 10 closes on by turning the mitigations
back on. The build followed the syllabus's existing deviation (recorded in the Course Overview since
Week 0) and added the ethics note to PS 10 itself. Nothing here is a technique against a system the
student was not given, and the material says so in the lab, the problem set and the reading guide.

---

## 22. Week 11 tool substitutions and the userns-restriction deviation

Week 11 (Containers and Virtualization) has the largest tool gap of the course, and it is turned
into the subject rather than papered over.

| Curriculum tool | On the machine? | Substitution / handling |
|---|---|---|
| `docker` | **absent** | Build the container from primitives — `clone` + namespaces in C (`minic.c`). Docker is those primitives plus cgroups plus OverlayFS; the week teaches the parts. |
| `podman`, `runc`, `lxc` | **absent** | Same — no rootless runtime available; the C mini-container is the artifact. |
| `newuidmap`/`newgidmap` (setuid map helpers) | **absent** | Maps are written directly to `/proc/<pid>/uid_map` from the parent (which is allowed for a single-id `"0 <uid> 1"` map without the setuid helper). This is why `unshare --map-root-user` fails but the C container works. |
| `fuse-overlayfs` | **absent** | OverlayFS is described and measured-to-EPERM; the unprivileged overlay mount needs this helper or real root, neither present. |
| `unshare(1)`, `nsenter`, `lsns`, `capsh`, `systemd-run --user` | **present** | Used for demonstration and for the cgroup limits (`systemd-run --user --scope -p MemoryMax/TasksMax`). |

**The central deviation — `apparmor_restrict_unprivileged_userns` = 1.** On this Ubuntu 24.04
machine the kernel is configured (via an AppArmor mediation) to permit an unprivileged user
namespace to be *created* but to strip its capabilities, so `CAP_SYS_ADMIN`-gated operations inside
it — `mount`, `sethostname`, `pivot_root`, an overlay mount — return **EPERM even to uid 0 in the
namespace**. Measured directly: `cat /proc/sys/kernel/apparmor_restrict_unprivileged_userns` → `1`.

The consequence is pedagogically clean and is treated as the week's headline finding rather than a
defect: **namespace creation works and the kernel-enforced isolation is genuine** (the child is
PID 1; its network namespace has only `lo`), **while the userspace setup that would complete the
illusion does not** (no private `/proc`, no hostname). This is the **fifth "a mechanism present is
not a mechanism working"** entry — joining Week 3 `PRIO_INHERIT`, Week 8 lazy binding, and Week 10's
ASLR-without-PIE and inert CET — and is stated as *a namespace created is not a capability granted*
in L34 §5, the README table, the Reading Guide (Q14), and Quiz 11's closing note. On a machine with
the restriction off, run as real root, or with the setuid map helpers installed, `minic` performs
`mount`/`sethostname` too; the material says so and PS 11 grades the EPERM as the correct result,
not a failure. The syllabus deviations table (Course Overview) carries the matching Week 11 row.

---

## 23. Every result in Week 11 was measured on the reference machine

Same machine as the earlier weeks: Intel i5-8250U, gcc 13.3.0 / `cc`, glibc 2.39, Linux 7.0.0-30,
cgroup v2, `apparmor_restrict_unprivileged_userns` = 1. Startup and OOM figures vary a little run to
run; the categorical results (PID 1, only `lo`, mount EPERM, identical kernel, exit 137) are
invariant on this configuration. Each figure names the program that produced it, per the course rule.

| Claim | How (program) | Result |
|---|---|---|
| A user namespace can be created unprivileged | `try_clone` (`CLONE_NEWUSER`) | **OK** |
| Individual namespaces alone fail unprivileged | `probe` (`CLONE_NEWPID` alone, etc.) | **EPERM** for PID/NET/NS/UTS standalone |
| **`CLONE_NEWUSER` carries the other five in one call** | `minic` (6 flags) | **OK** — the container clones |
| **The child is PID 1** | `minic sh -c 'echo $$'` | self-PID **1**; host PID (via `pgrep`) e.g. **1251803** |
| **The network namespace is isolated** | `netns` / `minic ip -o link show` | **only `lo`, DOWN** vs host's 3 (`lo`, `enp0s31f6`, `wlp61s0`) |
| **The kernel is shared** | `minic uname -r` vs host | **identical**, `7.0.0-30-generic` |
| uid 0 inside maps to real uid outside | `minic id -u` | **0** inside; files created owned by uid 1000 on host |
| **`sethostname` is refused to namespace-root** | `minic` | **EPERM** ("Operation not permitted") |
| **`mount` is refused to namespace-root** | `minic` (private `/proc`) | **EACCES/EPERM** ("Permission denied") |
| the reason | `cat /proc/sys/.../apparmor_restrict_unprivileged_userns` | **1** |
| **cgroup memory/pids are delegated to the user** | `cat .../user@1000.service/cgroup.controllers` | **`memory pids`** |
| **A memory cap OOM-kills, cgroup-local** | `systemd-run --user --scope -p MemoryMax=100M -p MemorySwapMax=0 ./hog` | killed ~**90 MiB**, **exit 137** (128+SIGKILL); host untouched |
| **`pids.max` stops a fork bomb** | fork loop under `-p TasksMax=20` | 21st `fork` → **EAGAIN** |
| **Container startup is ~1 ms** | `cost` | fork **139.2 µs**, clone **119.4 µs**, clone+6ns **1001.5 µs** |
| **seccomp narrows the syscall surface unprivileged** | `sec` | `write` allowed; `getpid` → **-1, EPERM**; no root, after `PR_SET_NO_NEW_PRIVS` |
| overlay mount needs root/helper | `ovl` (in userns) / `mount -t overlay` | **EPERM** / "must be superuser to use mount" |

### The one finding that shapes the whole week

Read the PID-1 / only-`lo` rows against the `sethostname`/`mount` EPERM rows: the isolation that is a
**property of the namespace's existence** is enforced by the kernel and works; the isolation that
requires **performing a privileged operation** does not, because the AppArmor restriction gives the
container a capability-less root. The mini-container is therefore a genuine, runnable artifact whose
behaviour on *this* image (PID/net isolated, mount/hostname refused) is exactly documented — the
honest state, measured, with the "run it elsewhere and the rest works" caveat recorded here and in
the student materials.

---

*Academic Registry · Build Records · Year 2 Sophomore · © CSE Department*
