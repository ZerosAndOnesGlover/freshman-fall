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

*Academic Registry · Build Records · Year 2 Sophomore · © CSE Department*
