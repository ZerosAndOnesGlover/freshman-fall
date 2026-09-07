# PROG 201 · Lab 2 Solutions
## IPC Performance Benchmark — Instructor Only

---

**Do not distribute.** Lab 2 is checked off in the session; the point of the lab is the gap between the prediction in Part B and the measurement, and a student who has seen this file has nothing left to be surprised by.

**Machine these numbers came from:** Linux 7.0.0-30-generic, gcc 13.3.0 (Ubuntu 24.04), page size 4,096, `PIPE_BUF` 4,096, four cores. Bulk figures vary about 10% run to run and round-trip figures about 5%; the orderings are stable across every run we made. **Students on their own hardware will get different numbers and the same shape.** Mark the shape.

---

## 1. The Five TODOs

The skeleton's scaffolding — `now`, `die`, `struct ring`, `ring_make`, `ring_free`, `bulk_pipe`, `rt_pipe`, `row`, `triprow`, `main` — is unchanged. These are the five bodies.

```c
static double bulk_fifo(long bytes, int chunk)
{
    unlink(FIFO_PATH);
    if (mkfifo(FIFO_PATH, 0600) < 0) die("mkfifo");

    if (fork() == 0) {
        int r = open(FIFO_PATH, O_RDONLY);      /* blocks for the writer */
        if (r < 0) _exit(1);
        char *sink = malloc(chunk);
        while (read(r, sink, chunk) > 0)
            ;
        close(r);
        _exit(0);
    }
    int w = open(FIFO_PATH, O_WRONLY);          /* blocks for the reader */
    if (w < 0) die("open fifo");

    char *buf = calloc(chunk, 1);
    double t0 = now();
    for (long sent = 0; sent < bytes; ) {
        ssize_t n = write(w, buf, chunk);
        if (n < 0) die("write");
        sent += n;
    }
    close(w);
    wait(NULL);
    double dt = now() - t0;
    free(buf);
    unlink(FIFO_PATH);
    return dt;
}

static double bulk_mq(long bytes, int chunk)
{
    if (chunk > 8192) return -1;                /* msgsize_max, L08 section 3 */

    mq_unlink(MQ_NAME);
    struct mq_attr a = { .mq_maxmsg = 10, .mq_msgsize = chunk };
    mqd_t q = mq_open(MQ_NAME, O_CREAT | O_RDWR, 0600, &a);
    if (q == (mqd_t) -1) return -1;

    long msgs = bytes / chunk;
    if (fork() == 0) {
        char *sink = malloc(chunk);             /* >= mq_msgsize, not >= len */
        for (long i = 0; i < msgs; i++)
            if (mq_receive(q, sink, chunk, NULL) < 0) _exit(1);
        _exit(0);
    }
    char *buf = calloc(chunk, 1);
    double t0 = now();
    for (long i = 0; i < msgs; i++)
        if (mq_send(q, buf, chunk, 0) < 0) die("mq_send");
    wait(NULL);
    double dt = now() - t0;
    mq_close(q);
    mq_unlink(MQ_NAME);
    free(buf);
    return dt;
}

static double bulk_shm(long bytes, int chunk)
{
    if (chunk > SLOT_SIZE) return -1;
    struct ring *r = ring_make(1);
    long msgs = bytes / chunk;

    if (fork() == 0) {
        char *sink = malloc(chunk);
        for (long i = 0; i < msgs; i++) {
            while (sem_wait(&r->full) == -1 && errno == EINTR)
                ;
            memcpy(sink, r->data[0], r->len);   /* the consumer really copies */
            sem_post(&r->empty);
        }
        _exit(0);
    }
    char *buf = calloc(chunk, 1);
    double t0 = now();
    for (long i = 0; i < msgs; i++) {
        while (sem_wait(&r->empty) == -1 && errno == EINTR)
            ;
        memcpy(r->data[0], buf, chunk);
        r->len = chunk;
        sem_post(&r->full);
    }
    wait(NULL);
    double dt = now() - t0;
    ring_free(r);
    free(buf);
    return dt;
}

static double rt_shm(long trips)
{
    struct ring *r = ring_make(0);      /* both semaphores start at zero */

    if (fork() == 0) {
        for (long i = 0; i < trips; i++) {
            while (sem_wait(&r->full) == -1 && errno == EINTR)
                ;
            sem_post(&r->empty);
        }
        _exit(0);
    }
    double t0 = now();
    for (long i = 0; i < trips; i++) {
        sem_post(&r->full);
        while (sem_wait(&r->empty) == -1 && errno == EINTR)
            ;
    }
    double dt = now() - t0;
    wait(NULL);
    ring_free(r);
    return dt;
}

static double bulk_slots(long bytes, int chunk, int slots)
{
    if (chunk > SLOT_SIZE || slots > MAX_SLOTS) return -1;
    struct ring *r = ring_make(slots);
    long msgs = bytes / chunk;

    if (fork() == 0) {
        char *sink = malloc(chunk);
        for (long i = 0; i < msgs; i++) {
            while (sem_wait(&r->full) == -1 && errno == EINTR)
                ;
            memcpy(sink, r->data[r->tail], chunk);
            r->tail = (r->tail + 1) % slots;    /* only the consumer writes tail */
            sem_post(&r->empty);
        }
        _exit(0);
    }
    char *buf = calloc(chunk, 1);
    double t0 = now();
    for (long i = 0; i < msgs; i++) {
        while (sem_wait(&r->empty) == -1 && errno == EINTR)
            ;
        memcpy(r->data[r->head], buf, chunk);
        r->head = (r->head + 1) % slots;        /* only the producer writes head */
        sem_post(&r->full);
    }
    wait(NULL);
    double dt = now() - t0;
    ring_free(r);
    free(buf);
    return dt;
}```

Builds clean under `gcc -Wall -Wextra -O2 -g -std=c11 -o bench bench.c -lrt -lpthread`.

---

## 2. The Five Places Students Get Stuck

| # | Symptom | Cause | What to say |
| --- | --- | --- | --- |
| 1 | `bulk_fifo` hangs forever, no output | Both ends opened in the same process before the fork, or the parent opens `O_WRONLY` before forking the reader | "Which process opens first, and what is a blocking `open` on a FIFO waiting for?" L07 §5 |
| 2 | `bulk_fifo` is 5× slower than the pipe | The clock started before the rendezvous, so the `open` wait is in the measurement | Point at `bulk_pipe`: `t0 = now()` is after all the setup |
| 3 | `bulk_mq` dies with `EMSGSIZE` | Receive buffer sized to the message, not to `mq_msgsize` | L08 §2. This is the single most common one |
| 4 | `bulk_mq` fails at 16 KB and the student "fixes" it by clamping the chunk | It is not a bug — the limit is real and Part D needs the `--` | "Do not fix it. That gap is a result." |
| 5 | `bulk_shm` is suspiciously fast (> 20,000 MiB/s) | The consumer does not `memcpy` out; the loop measures semaphores only | Ask what the consumer does with the data |

A sixth, rarer and worth catching: a `sem_t` declared as a local in the parent and its address handed to the child. It **appears to work** for a while, because the child's copy-on-write page still has the initialised value in it, and then hangs. If a student's shm run hangs after a few thousand records, look at where the `sem_t` lives.

---

## 3. Reference Measurements

**Part A + B — `./bench bulk 256 4096`**

```
bulk: 256 MiB in 4096-byte chunks
mechanism                   seconds        MiB/s
pipe                          0.070       3680.4
FIFO                          0.088       2924.0
POSIX mq                      0.092       2785.9
shm + sem, 1 slot             0.446        573.8
```

**Part B — `./bench trip 100000`**

```
round trip: 100000 one-byte ping-pongs
mechanism                   seconds      us/trip
pipe                          0.725        7.254
shm + sem                     0.661        6.454
```

Three further runs of the round trip gave 7.20/6.61, 7.26/7.06 and 7.22/6.51. **The shared-memory margin is 8% and is sometimes inside the noise.** A student who reports "no difference" has measured correctly; do not mark them down for it.

**Part C — `./bench slots 256 4096`**

```
slots                       seconds        MiB/s
1                             0.459         557.2
2                             0.261         982.2
4                             0.064        3978.6
8                             0.060        4239.5
16                            0.055        4618.9
32                            0.055        4658.4
64                            0.062        4158.4
```

**Part D — `for c in 64 512 4096 16384 65536 262144; do ./bench bulk 128 $c; done`**

| chunk | pipe | FIFO | mq | shm, 1 slot | shm / pipe |
| --- | --- | --- | --- | --- | --- |
| 64 B | 79.4 | 67.5 | 61.7 | 8.8 | 0.11× |
| 512 B | 633.9 | 527.0 | 444.8 | 66.9 | 0.11× |
| 4,096 B | 3,648.7 | 3,004.6 | 2,663.4 | 670.0 | 0.18× |
| 16,384 B | 3,701.8 | 3,767.1 | **`--`** | 2,094.0 | 0.57× |
| 65,536 B | 2,887.9 | 3,145.5 | **`--`** | 6,554.8 | 2.27× |
| 262,144 B | 2,510.3 | 2,412.8 | **`--`** | 14,431.7 | 5.75× |

All MiB/s. The crossover is between 16 KB and 64 KB.

---

## 4. Answers

**Q1 — the FIFO opens.**

The reader opens first *in the child*, and the parent opens the write end after forking. Either order works **provided the two opens are in different processes**; what cannot work is both in one process, because the first `open` blocks forever waiting for a peer that the process was going to create on its next line.

If both ends opened `O_WRONLY` first, both would block in `open` waiting for a reader that never arrives — `open(O_WRONLY)` on a FIFO does not return until a reader opens (L07 §5). Full marks require the answer to be about the rendezvous rule, not about what they saw.

**Q2 — the 8,192 limit.**

`/proc/sys/fs/mqueue/msgsize_max`, which is **8192** on this machine; the companion `msg_max` is **10**. A process with `CAP_SYS_RESOURCE` may exceed them, or root may raise the `sysctl`s — but note that raising them for everybody is a denial-of-service surface, because queued messages are unswappable kernel memory charged against `RLIMIT_MSGQUEUE`. A good answer mentions the `RLIMIT`; an excellent one notices that the limit exists because the memory is pinned.

**Q3 — the receive buffer.**

`mq_receive` fails with **`EMSGSIZE`** if the buffer is smaller than the queue's `mq_msgsize`, whatever the actual message length, because the kernel validates the buffer before it dequeues anything — it must be able to guarantee the message will fit. The correct idiom is `mq_getattr` then allocate `a.mq_msgsize`, and it is correct even for a queue you created, because `mq_open` on an existing queue ignores the attributes you pass.

**Q4 — the prediction.**

Accept any prediction; the mark is for having written one *before*. Almost everyone predicts shared memory fastest, usually by 2–10×.

Measured: 574 MiB/s against the pipe's 3,680 — **0.16×, so about six times slower.** The sentence we are looking for is some form of: *the one-slot ring forces a blocking handoff every 4 KB, and a handoff costs ~3 µs while the copy it saves costs 118 ns.*

A student who predicted "about the same" and reasoned about handoffs deserves more credit than one who predicted 6× and cannot say why.

**Q5 — the round trip.**

A round trip is **two sleeps and two wakeups whatever it is built on**. Shared memory replaces a `read`/`write` pair with a `sem_wait`/`sem_post` pair, and both block in the kernel through the same scheduler. The only thing removed is the copy of one byte, which is unmeasurable. 8% is the right answer and it is roughly the cost of the two `read`/`write` system calls themselves — 2 × 574 ns against a 7.2 µs trip.

**Q6 — the knee.**

**(a)** Depth stops helping once the ring is deep enough that the producer never finds it full and the consumer never finds it empty. Past that point the two processes overlap completely and the remaining cost is the `memcpy` and the cache traffic between two cores, which no amount of buffering removes. The knee is at 4 slots here and flat from 8.

**(b)** A pipe *is* a sixteen-slot ring (L07 §2). So Part B was not comparing "kernel" against "no kernel" — it was comparing a sixteen-slot buffer against a one-slot one, and the one-slot buffer lost for that reason and not because of the mechanism. **The honest form of the comparison is 16 slots against 16 slots**, which is 4,619 against 3,680 MiB/s: shared memory wins by about 1.2×, and that 1.2× is the one copy it really saved.

This is the answer the lab exists for. A student who gets (b) has understood the week.

**Q7 — the rule.**

From the table: **reach for shared memory when a message is larger than about 64 KB**, because the saving is per byte and the cost is per message, so the ratio is decided by message size alone. Below the crossover a pipe is faster, simpler, and cleans itself up.

For the second half, any defensible answer: a large region both processes *read* and rarely write (the transfer never happens at all — this is the case the textbook claim is actually true for); a structure with internal pointers that a stream would have to serialise; a case where the consumer needs random access; or a case where copying is fine but the extra 64 MB of buffered data is not affordable.

---

## 5. Checkoff

The four boxes are in the lab sheet. In practice:

- **Insist on seeing the written prediction.** If it is not on paper before the run, the checkoff is not complete — offer to let them predict Part C's knee instead and check that.
- **Ask the Q6(b) question out loud** even if they have written it. It is the one that separates "ran the benchmark" from "understood the benchmark".
- The `strace -c -f` extension is worth steering strong students towards, and the result is sharper than it sounds. For 256 MiB in 4 KB chunks:

```
pipe:            65,537 write + 65,538 read           = 131,114 system calls
shm, one slot:  131,778 futex (65,249 of them EAGAIN) = 131,817 system calls
```

  **The same number of system calls.** The mechanism sold as "no system calls" made 703 more than the pipe did. It saved 65,536 copies of 4 KB — about 7.7 ms of `memcpy` — and spent it on futex sleeps that are more expensive than the `read`/`write` pair it replaced. That is the whole lab in one `strace`, and it is worth putting on the board.

---

*PROG 201 · Week 2 · Lab 2 Solutions · Instructor Only · © CSE Department*
