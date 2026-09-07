# PROG 201 · Problem Set 2
## A Producer-Consumer Pipeline, Twice

---

**Released:** Week 2, Wednesday · **Due:** Week 3, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS2_{LastName}_{StudentID}.pdf`, and your code as `PS2_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine. The write-up and the code must be yours.
>
> **Q1 and Q2 are one program**, `pc.c`, which builds the same pipeline over two different
> mechanisms. Write Q1 first and get it correct before starting Q2 — Q3 compares them and needs
> both.
>
> **Q1(c) and Q3 are measurements on your own machine.** State your `gcc --version`, `uname -r`,
> and whether you are on BH 215 or your own hardware. Report what you measured, including when it
> disagrees with this paper.
>
> Everything compiles clean under `gcc -Wall -Wextra -O2 -std=c11`. Warnings cost marks.
> Link with `-lrt -lpthread`.

---

### The Program

One producer generates *N* fixed-size records; one consumer verifies every one of them and reports the rate. A record carries its own integrity check:

```c
#define REC_PAYLOAD 240

struct record {
    uint32_t seq;             /* 0, 1, 2, ... */
    uint32_t producer;        /* which producer wrote it */
    uint32_t sum;             /* checksum over payload   */
    char     payload[REC_PAYLOAD];
};                            /* 252 bytes */
```

Fill the payload with a byte derived from **both** `producer` and `seq` — `(unsigned char)(producer * 37 + seq)` will do. **Do not** derive it from `seq` alone: with several producers writing identical payloads, two half-records spliced together are still self-consistent and your corruption check silently passes. *(This is not hypothetical. It is the first version of the reference solution.)*

Usage:

```
./pc pipe 200000            # 200,000 records through a pipe
./pc shm  200000 8          # the same through an 8-slot shared-memory ring
./pc pipe 200000 -w 4       # four concurrent producers
```

---

### Q1: The Pipeline Over a Pipe (30 points)

**(a) [18]** Implement `run_pipe`. One `pipe`, one forked producer per `-w`, the consumer in the parent.

Requirements, each of which is a mark:

- **`write_all` and `read_all`.** A `write` may be short and a `read` may return a partial record; neither is an error. Both loops must also handle `EINTR` (Week 0 L03 §5).
- **The parent closes its copy of the write end** before reading, or the consumer never sees EOF (L07 §3).
- The consumer detects the end of the stream by **EOF**, and reports the record count, the corruption count, elapsed seconds and records/second.
- A read that returns a **partial record at EOF** is a distinct failure from a checksum mismatch. Report it separately and say, in one sentence, what it would mean.

**(b) [6]** Run with `-w 4`. Report the corruption count.

Then explain, referring to the number 4,096 and to `<limits.h>`, why you were entitled to expect that result **before** running it. Your answer must name the guarantee, not describe the observation.

**(c) [6]** Now break it. Raise `REC_PAYLOAD` so that a record is **8,192 bytes**, and slow the consumer down — sleep between reads, and read in pieces *smaller than one record*.

Report the corruption count for both consumers: the fast one and the dribbling one. You should find a large difference. Explain it in terms of L07 §4, and state clearly which of the following your data supports:

1. Writes larger than `PIPE_BUF` always interleave.
2. Writes larger than `PIPE_BUF` interleave when the reader falls behind.
3. Writes larger than `PIPE_BUF` **may** interleave, and nothing about your test proves they will not.

*(One of these is the correct engineering conclusion. It is not the one your measurement most directly suggests.)*

---

### Q2: The Same Pipeline Over Shared Memory (30 points)

**(a) [18]** Implement `run_shm` with a ring of `slots` records in a `MAP_SHARED|MAP_ANONYMOUS` region, and two semaphores:

```c
sem_init(&g->empty, 1, slots);      /* slots free    */
sem_init(&g->full,  1, 0);          /* none ready    */
```

Requirements:

- **Both `sem_t`s live inside the shared region** (L09 §1). Say in one sentence what breaks if they do not, and how you would notice.
- Producer: wait `empty`, write slot, advance `head`, post `full`. Consumer: the mirror image. **No third semaphore** for one producer and one consumer — justify that in one sentence.
- Every `sem_wait` in a retry loop on `EINTR` (L09 §3).
- `sem_destroy` and `munmap` on the way out.

**(b) [6]** A pipe ends with EOF. A shared-memory ring has no such thing — the consumer waiting on `full` cannot tell "nothing yet" from "nothing ever again", which is L07 §6's problem in a new place.

Implement a termination protocol and **justify your choice**. A sentinel record with a reserved `seq` is the obvious one; a count agreed in advance and a flag in the region are two others. Say what yours does if the producer is killed with `SIGKILL` halfway through, and what a robust version would need.

**(c) [6]** Two cleanup questions, with evidence:

- Your region is `MAP_SHARED|MAP_ANONYMOUS`. Show what `ls /dev/shm` contains after a run, and explain why. Then say what would be there if you had used `shm_open`, and what would still be there after a crash.
- `sem_destroy` on a semaphore another process is blocked in is undefined behaviour. Explain how your termination protocol guarantees nobody is blocked when you call it.

---

### Q3: Measure Both, and Account for the Difference (20 points)

**(a) [8]** Produce this table on your machine, 200,000 records each:

| Configuration | records/s | MiB/s |
| --- | --- | --- |
| `pipe`, 1 producer | | |
| `shm`, 1 slot | | |
| `shm`, 2 slots | | |
| `shm`, 8 slots | | |
| `shm`, 32 slots | | |

**(b) [6]** The pipe moves one 252-byte record per `write` and one per `read`: **two system calls per record.** Week 1 L05 measured a system call at about 1.25 µs, and Week 2 L09 measured `getpid()` at 574 ns.

Compute the records/second that two system calls per record predicts, and compare it with your measured pipe row. State the agreement as a percentage. If it agrees, say what that tells you about where the pipe's time goes; if it does not, say what else is in the budget.

**(c) [6]** Your 1-slot shared-memory row is probably **slower** than the pipe, and your 8-slot row faster. Explain both, in terms of the number of blocking handoffs per record in each case.

Then answer the design question this raises: **the pipe is losing to two system calls per record. What single change to `run_pipe` — no shared memory involved — would remove most of that cost?** You do not have to implement it, but say what the trade-off is.

---

### Q4: The Deadlock You Will Actually Write (12 points)

With **two or more producers**, the ring needs a mutex around the `head` update, because two producers must not claim the same slot. Here are the two orderings:

```c
/* A */                          /* B */
sem_wait(&g->empty);             sem_wait(&g->mutex);
sem_wait(&g->mutex);             sem_wait(&g->empty);
... write slot, advance head ... ... write slot, advance head ...
sem_post(&g->mutex);             sem_post(&g->mutex);
sem_post(&g->full);              sem_post(&g->full);
```

B holds a lock across a blocking wait, which is the classic recipe for deadlock, and every textbook says so.

**(a) [4]** Implement both, with two producers and a ring of two, and run each one. **Report what actually happens.**

One of them will not do what you were told to expect. Explain why not — specifically, say which process is able to make progress and why the lock it does not hold is the reason.

**(b) [4]** Now change one thing: make the **consumer** take the mutex too, around its own index update. (It has to, in any design where the consumer maintains something the producers also touch — a record count, a high-water mark, a free list.)

Re-run both orderings. Report the result, and for the one that now hangs, give the exact sequence of events that makes it permanent: how many processes, what each is waiting on, and which post can never happen.

**(c) [2]** Keep the correct ordering and demonstrate it: two producers, 2 × *N* records out, zero corrupt, with the consumer's mutex in place.

**(d) [2]** State the general rule your answer to (b) is an instance of, in one sentence, in a form that would apply to a lock and a database transaction as readily as to these two semaphores.

*(If your program in (a) hangs where this paper says it should not, or runs where it says it should hang, report that. Say what your configuration was. A measurement that contradicts the paper is worth more than one that agrees with it, provided you can say what you ran.)*

---

### Q5: Choosing (8 points)

Four systems. For each, name the mechanism from Week 2 you would use and give **one sentence** of justification that refers to a measured number or a stated limit from this week — not to a general impression.

**(a) [2]** A shell running `find | xargs grep | sort`.

**(b) [2]** A daemon that accepts jobs from `/usr/bin` tools run by users who log in at unpredictable times, at a rate of a few per minute, where a job is under 1 KB and urgent jobs must jump the queue.

**(c) [2]** A video pipeline moving 4 MB frames between two processes at 60 frames per second.

**(d) [2]** A monitoring process that must read a 200 MB table maintained by another process, on demand, without disturbing it.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | The pipeline over a pipe | 30 |
| 2 | The same over shared memory | 30 |
| 3 | Measure both, and account for the difference | 20 |
| 4 | The deadlock you will actually write | 12 |
| 5 | Choosing | 8 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*PROG 201 · Week 2 · PS 2 · © CSE Department*
