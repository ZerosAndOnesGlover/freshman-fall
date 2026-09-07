# PROG 201 · PS 2 Solutions
## A Producer-Consumer Pipeline, Twice — Instructor Only

---

**Do not distribute.** Q1(c) and Q3 depend on students measuring for themselves.

**Machine these numbers came from:** Linux 7.0.0-30-generic, gcc 13.3.0 (Ubuntu 24.04), `PIPE_BUF` 4,096, four cores. Rates vary 10–20% run to run; the one-slot shared-memory row is the noisiest (165k–228k rec/s across runs). **Mark the ratios and the reasoning, not the digits.**

---

## Reference Solution — `pc.c`

Builds clean under `gcc -Wall -Wextra -O2 -g -std=c11 -o pc pc.c -lrt -lpthread`.

```c
/* PROG 201 -- PS 2 reference solution.
 * A producer-consumer pipeline, once over a pipe and once over shared memory.
 *
 *   ./pc pipe  100000            # 100,000 records through a pipe
 *   ./pc shm   100000 8          # the same through an 8-slot ring
 *   ./pc pipe  100000 -w 4       # four producers (Q1c: atomicity)
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <time.h>
#include <limits.h>
#include <semaphore.h>
#include <sys/mman.h>
#include <sys/wait.h>

#define REC_PAYLOAD 240
#define MAX_SLOTS   64

struct record {
    uint32_t seq;
    uint32_t producer;
    uint32_t sum;                       /* over payload */
    char     payload[REC_PAYLOAD];
};                                      /* 252 bytes -- well under PIPE_BUF */

struct ring {
    sem_t         empty, full;
    unsigned      head, tail;
    struct record slot[MAX_SLOTS];
};

static double now(void)
{
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec / 1e9;
}
static void die(const char *w) { perror(w); exit(1); }

static uint32_t checksum(const char *p, size_t n)
{
    uint32_t h = 2166136261u;
    for (size_t i = 0; i < n; i++) { h ^= (unsigned char) p[i]; h *= 16777619u; }
    return h;
}

static void fill(struct record *r, uint32_t seq, uint32_t who)
{
    r->seq = seq; r->producer = who;
    memset(r->payload, (int)(unsigned char)(who * 37u + seq), REC_PAYLOAD);
    r->sum = checksum(r->payload, REC_PAYLOAD);
}

/* read exactly n bytes or report short */
static ssize_t read_all(int fd, void *buf, size_t n)
{
    size_t got = 0;
    while (got < n) {
        ssize_t k = read(fd, (char *) buf + got, n - got);
        if (k < 0) { if (errno == EINTR) continue; return -1; }
        if (k == 0) return got;
        got += k;
    }
    return got;
}

static void write_all(int fd, const void *buf, size_t n)
{
    size_t sent = 0;
    while (sent < n) {
        ssize_t k = write(fd, (const char *) buf + sent, n - sent);
        if (k < 0) { if (errno == EINTR) continue; die("write"); }
        sent += k;
    }
}

/* ------------------------------------------------------------------ pipe -- */
static void run_pipe(long n, int producers)
{
    int fd[2];
    if (pipe(fd) < 0) die("pipe");

    for (int w = 0; w < producers; w++)
        if (fork() == 0) {
            close(fd[0]);
            struct record r;
            for (long i = 0; i < n; i++) {
                fill(&r, i, w);
                write_all(fd[1], &r, sizeof r);   /* 252 <= PIPE_BUF: atomic */
            }
            _exit(0);
        }
    close(fd[1]);                                  /* the parent's copy, or no EOF */

    long got = 0, bad = 0;
    struct record r;
    double t0 = now();
    for (;;) {
        ssize_t k = read_all(fd[0], &r, sizeof r);
        if (k == 0) break;
        if (k < 0) die("read");
        if ((size_t) k != sizeof r) { bad++; break; }   /* truncated tail */
        if (r.sum != checksum(r.payload, REC_PAYLOAD)) bad++;
        got++;
    }
    double dt = now() - t0;
    close(fd[0]);
    while (wait(NULL) > 0) ;

    printf("pipe   %d producer(s): %ld records, %ld corrupt, %.3f s, %.0f rec/s, %.1f MiB/s\n",
           producers, got, bad, dt, got / dt,
           got * (double) sizeof r / dt / (1024 * 1024));
}

/* ------------------------------------------------------------------- shm -- */
static void run_shm(long n, int slots)
{
    struct ring *g = mmap(NULL, sizeof *g, PROT_READ | PROT_WRITE,
                          MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    if (g == MAP_FAILED) die("mmap");
    if (sem_init(&g->empty, 1, slots) < 0) die("sem_init");
    if (sem_init(&g->full,  1, 0) < 0) die("sem_init");
    g->head = g->tail = 0;

    if (fork() == 0) {                              /* producer */
        struct record r;
        for (long i = 0; i < n; i++) {
            fill(&r, i, 0);
            while (sem_wait(&g->empty) == -1 && errno == EINTR) ;
            g->slot[g->head] = r;
            g->head = (g->head + 1) % slots;
            sem_post(&g->full);
        }
        /* the sentinel: one more record with seq == UINT32_MAX */
        r.seq = UINT32_MAX;
        while (sem_wait(&g->empty) == -1 && errno == EINTR) ;
        g->slot[g->head] = r;
        g->head = (g->head + 1) % slots;
        sem_post(&g->full);
        _exit(0);
    }

    long got = 0, bad = 0;
    double t0 = now();
    for (;;) {
        while (sem_wait(&g->full) == -1 && errno == EINTR) ;
        struct record r = g->slot[g->tail];
        g->tail = (g->tail + 1) % slots;
        sem_post(&g->empty);
        if (r.seq == UINT32_MAX) break;             /* end of stream */
        if (r.sum != checksum(r.payload, REC_PAYLOAD)) bad++;
        got++;
    }
    double dt = now() - t0;
    wait(NULL);

    printf("shm    %2d slots     : %ld records, %ld corrupt, %.3f s, %.0f rec/s, %.1f MiB/s\n",
           slots, got, bad, dt, got / dt,
           got * (double) sizeof(struct record) / dt / (1024 * 1024));
    sem_destroy(&g->empty); sem_destroy(&g->full);
    munmap(g, sizeof *g);
}

int main(int argc, char **argv)
{
    if (argc < 3) { fprintf(stderr, "usage: %s pipe|shm N [slots] [-w P]\n", argv[0]); return 2; }
    long n = atol(argv[2]);
    int slots = 8, producers = 1;
    for (int i = 3; i < argc; i++) {
        if (!strcmp(argv[i], "-w") && i + 1 < argc) producers = atoi(argv[++i]);
        else slots = atoi(argv[i]);
    }
    if (slots < 1 || slots > MAX_SLOTS) { fprintf(stderr, "slots 1..%d\n", MAX_SLOTS); return 2; }

    printf("record is %zu bytes; PIPE_BUF is %d\n", sizeof(struct record), PIPE_BUF);
    if (!strcmp(argv[1], "pipe")) run_pipe(n, producers);
    else if (!strcmp(argv[1], "shm")) run_shm(n, slots);
    else { fprintf(stderr, "pipe or shm\n"); return 2; }
    return 0;
}
```

---

## Q1 — The Pipeline Over a Pipe (30)

**(a) [18]** Marks: `write_all` **[4]**, `read_all` including the partial-record case **[4]**, `EINTR` in both **[2]**, the parent closing its copy of the write end **[3]**, EOF-based termination **[2]**, the four reported figures **[2]**, partial record reported separately with an explanation **[3]**.

The explanation we want for the partial record: **a short read at EOF means a producer died mid-record**, since `write_all` would otherwise have completed it. It is a producer crash, not a pipe problem, and the distinction matters because the two have different fixes.

Deduct for: `if (write(...) < n)` treated as an error; the parent leaving `fd[1]` open and the program hanging; `read` in a loop without a total.

**(b) [6]** **Zero corrupt**, and this is guaranteed, not lucky.

The record is 252 bytes and `PIPE_BUF` is 4,096 (`<limits.h>`, not `<unistd.h>`). POSIX guarantees writes of at most `PIPE_BUF` bytes to a pipe are never interleaved with data from other writers, so each `write` of a whole record either goes in complete or does not begin.

**Full marks require the guarantee, not the observation.** "I ran it and got zero" is [2]. Naming `PIPE_BUF`, the value, and the header is [6].

Measured:

```
record is 252 bytes; PIPE_BUF is 4096
pipe   4 producer(s): 800000 records, 0 corrupt, 0.886 s, 903272 rec/s, 217.1 MiB/s
```

**(c) [6]** The interesting one, and the marks are for the conclusion, not the numbers.

At 8,192 bytes per record with four producers:

| consumer | records | corrupt |
| --- | --- | --- |
| fast (whole record per `read`) | 8,000 | **0** |
| slow, dribbling (997 bytes per `read`, `usleep(200)` between) | 1,200 | **1,192 — 99.3%** |

**The correct answer is (3).** Writes above `PIPE_BUF` *may* interleave, and a test that does not tear proves nothing.

(2) is the tempting answer and it is subtly wrong: a consumer that sleeps but drains a **whole record** at a time tore nothing in 8,000 records, so "falls behind" is not the condition either. The condition involves how the reader drains, which is kernel scheduling detail and not a specification. A student who writes (2) with good reasoning gets [4]; one who writes (3) and explains why their own (2)-shaped observation does not license it gets [6].

**This is the most important question on the paper.** It is the general form of "the absence of a symptom is not evidence", and Week 10 is built on it.

---

## Q2 — The Same Over Shared Memory (30)

**(a) [18]** Marks: region and both semaphores initialised in it **[4]**, correct wait/post pairing **[5]**, `head`/`tail` advanced by the right process only **[3]**, `EINTR` loops **[3]**, `sem_destroy` + `munmap` **[2]**, the "no third semaphore" justification **[1]**.

The justification: with one producer and one consumer, **`head` is written only by the producer and `tail` only by the consumer**, so no two processes ever write the same variable; the two semaphores already prevent the producer from overwriting an unread slot and the consumer from reading an unwritten one.

If the `sem_t`s are outside the region: the parent and child each get their own copy on the first write (copy-on-write, Week 0 L01), so `sem_post` in one is invisible to the other and the program **hangs on the first full ring** — after `slots` records, not immediately. That "works for a bit, then hangs" signature is the thing to be able to recognise.

**(b) [6]** Any working protocol, **[4]**, plus the honest failure analysis, **[2]**.

The sentinel — a record with a reserved `seq`, `UINT32_MAX` in the reference — is the expected answer and it is the right one, because it travels through the same ring and therefore cannot arrive out of order with respect to the data.

The failure analysis we want: **if the producer is `SIGKILL`ed, no sentinel is ever posted and the consumer blocks in `sem_wait(&full)` forever.** A robust version needs something outside the ring — `sem_timedwait` and a check, or a `SIGCHLD` handler in the consumer's parent, or the producer's `wait` status. Award the mark for naming *any* mechanism outside the ring; the point is recognising that in-band termination cannot survive the producer's death.

A count agreed in advance is acceptable and has the same flaw. A flag in the region is worse — it can be set while records are still in the ring, and a student who spots that races with the data deserves the credit.

**(c) [6]** Three marks each.

- `ls /dev/shm` shows **nothing** from this program, because `MAP_SHARED|MAP_ANONYMOUS` has no name — it is inherited across `fork` and freed when the last process unmaps or exits. With `shm_open` there would be a `/dev/shm/<name>` entry, and **it would still be there after a crash**, holding its data, until `shm_unlink` or reboot (L08 §4). Full marks need the crash half.
- `sem_destroy` is only reached by the consumer *after* the sentinel, and the sentinel is the producer's last act before `_exit`, so the producer is not in `sem_wait`. Accept any answer that identifies the ordering argument. **A student who notices that their own code calls `sem_destroy` before `wait(NULL)` and is therefore not actually safe should get full marks and a well done** — the reference solution calls `wait(NULL)` first for exactly this reason.

---

## Q3 — Measure Both, and Account (20)

**(a) [8]** Reference, 200,000 records of 252 bytes:

| Configuration | records/s | MiB/s |
| --- | --- | --- |
| `pipe`, 1 producer | 918,570 | 220.8 |
| `shm`, 1 slot | 227,920 | 54.8 |
| `shm`, 2 slots | 1,122,019 | 269.7 |
| `shm`, 8 slots | 2,424,011 | 582.6 |
| `shm`, 32 slots | 2,772,260 | 666.2 |

**(b) [6]** The arithmetic, and the point is that **one of the two reference numbers is the right one and the other is not**.

- At **1.25 µs** per call (L05): 2.5 µs per record → **400,000 rec/s**. Measured 918,570. The prediction is **2.3× too pessimistic**.
- At **574 ns** per call (L09 §3): 1.15 µs per record → **870,000 rec/s**. Measured 918,570. **Agreement within 6%.**

The 574 ns figure is a bare `getpid()` — syscall entry and exit and nothing else. L05's 1.25 µs was measured on one-byte file I/O, and it therefore includes per-call work the kernel does *for a file* — VFS dispatch, position update, page cache lookup — that a pipe does not do. **A pipe write is close to the cheapest system call there is.**

Marks: the two calculations [3], identifying which matches [2], a sensible account of why they differ [1]. A student who concludes "the pipe's time is essentially all system-call entry and exit" has the intended answer.

**(c) [6]** Blocking handoffs per record:

- **1 slot:** one per record, in both directions — the producer cannot write record *n+1* until the consumer has taken record *n*. At ~3 µs a handoff, that is a ceiling near 300,000 rec/s, and 227,920 is measured. Slower than the pipe, which needs no handoff at all until sixteen pages are full.
- **8 slots:** the producer runs seven records ahead, so most iterations find the semaphore already positive and take the **19.3 ns uncontended path with no system call**. A handoff happens only when the ring actually empties or fills. 2.4 M rec/s.

**The design question [3 of the 6]:** **batch the records.** Write *k* records per `write` and read a page or more per `read`, reassembling in user space — that is what `stdio` does, and it is Week 1 L05 §2's table. At 16 records per call the pipe's syscall cost per record falls by 16×.

The trade-off: **latency**. A partially filled batch sits in the producer's buffer until it fills or the producer flushes, so the last record of a burst can wait indefinitely. This is exactly Nagle's algorithm and `TCP_NODELAY`, which Week 5 meets again. Accept "you now need a flush policy" as the trade-off; that is the same answer.

---

## Q4 — The Deadlock (12)

**This question was built from a measurement that contradicted the standard answer.** Ordering B, written exactly as every textbook warns against, **does not deadlock** in a one-producer-index ring — measured, four configurations, all completed:

```
order A, 2 slots, 2 producers: 40000 consumed
order B, 2 slots, 2 producers: 40000 consumed
order B, 1 slots, 2 producers: 40000 consumed
order B, 1 slots, 4 producers: 80000 consumed
```

Add the consumer's own `sem_wait(&mutex)` and B hangs immediately, while A still completes:

```
CMUTEX order A, 2 slots, 2 producers: 40000 consumed
CMUTEX order B, 2 slots, 2 producers: TIMED OUT
CMUTEX order B, 1 slots, 2 producers: TIMED OUT
```

**(a) [4]** Expected report: **both orderings complete.**

The reason: the consumer never asks for the mutex. So when producer 1 holds the mutex and blocks in `sem_wait(&empty)` on a full ring, the consumer is entirely unobstructed — it takes a record, posts `empty`, and producer 1 wakes and finishes. Producer 2 waits longer than it should, and that is all: **B as written is a serialisation bug, not a deadlock.**

Marks: [2] for reporting the actual result, [2] for identifying that the consumer's independence from the mutex is what saves it. **A student who reports "B deadlocked" has almost certainly not run it** — check their output.

**(b) [4]** With the consumer holding the mutex, B deadlocks. The sequence:

1. The ring is full: `empty` is 0, `full` is `slots`.
2. Producer 1 takes `mutex`, then blocks in `sem_wait(&empty)`.
3. The consumer passes `sem_wait(&full)` — there is data — and then blocks in `sem_wait(&mutex)`.
4. The consumer is the only process that would ever call `sem_post(&empty)`, and it cannot reach that line.
5. Producer 1 is the only holder of `mutex`, and it cannot reach `sem_post(&mutex)` until `empty` is posted.

Permanent, with two processes and no timeout anywhere. Producer 2 joins the queue behind the mutex and changes nothing.

Marks: [2] for the correct result both ways, [2] for a sequence that names step 4 — the cycle only closes because the consumer is the sole source of the resource the mutex-holder is waiting for.

**(c) [2]** Ordering A, consumer mutex in place, 2 × *N* out, zero corrupt. Run it.

**(d) [2]** Any correct general form. Ours: **never block on a resource while holding a lock that the party who would release that resource needs to acquire.** Accept "acquire in a consistent order and do not sleep in a critical section", or a statement of the circular-wait condition.

**On the final note in the paper:** students who report a contradiction *with their configuration stated* should be rewarded, and their configuration should be checked — this key's own numbers are from one four-core machine, and B is a race whose outcome depends on how long the consumer holds the mutex. If a student finds a scheduling in which B(a) does hang, that is a better piece of work than the expected answer, and it does not change (d).

---

## Q5 — Choosing (8)

Two marks each. **The mark is for the justification referring to a number or a stated limit**, not for the mechanism alone — most of these have a defensible second answer.

**(a) Pipe.** Related processes, a linear stream, no framing needed, and the shell has no reason to pay for anything else. A justification citing the sixteen-page buffer or "the crossover is at 64 KB and these records are lines" earns it.

**(b) POSIX message queue.** Unrelated processes (so not a bare `pipe`), discrete sub-1 KB requests (so boundaries are free), priorities needed (so not a FIFO), and a few per minute — well inside the 10 × 8,192 ceiling. **This is the one case where the ceiling is not a problem, and saying so is the justification.**

**(c) Shared memory.** 4 MB per frame is far above the 64 KB crossover; the measured ratio at 256 KB was already 5.75×, and it grows. A ring of a few frames with two semaphores; at 60 fps the handoff cost is 3 µs against a 16.7 ms budget, so synchronisation is free here.

**(d) Shared memory, and the transfer never happens.** The monitor maps the region read-only and reads it in place; nothing is copied and nothing is sent. **This is the case the textbook claim is actually true for**, and a student who says so should be told they have found the point of the week. (A good answer will also notice that reading a 200 MB structure while another process mutates it needs a consistency scheme — a seqlock, double buffering, or a version counter — and that is a legitimate extra credit remark.)

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

---

*PROG 201 · Week 2 · PS 2 Solutions · Instructor Only · © CSE Department*
