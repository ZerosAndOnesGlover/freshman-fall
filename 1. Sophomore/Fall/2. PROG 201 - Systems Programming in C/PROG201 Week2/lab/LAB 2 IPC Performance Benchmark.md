# PROG 201 · Lab 2
## IPC Performance Benchmark — Four Mechanisms, Two Questions
### Covers Week 2 · sat **Monday of Week 3**, 15:00–16:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 2 and is sat in Week 3.** The lab is on Monday and this course's lectures
> are Tuesday to Thursday, so a lab can never be sat in the week it covers — Lab *N* is sat on the
> Monday of Week *N+1*. Every lab file states its own week; the file is authoritative.
>
> **Unmarked.** The TA checks your work off in the session.

**What you are building:** a benchmark that measures a pipe, a FIFO, a POSIX message queue and shared memory, and settles by measurement a claim your textbook makes without one.

The claim, from L08 §1 and from every operating systems book ever written:

> Shared memory is the fastest IPC mechanism.

**Part B will show you it is six times slower than a pipe.** Part C will show you why, and Part D will show you the exact condition under which the claim is true. **Write your prediction down before Part B runs** — Q4 asks what you predicted, and the point of the lab is lost if you fill it in afterwards.

---

## 0. Setup (5 minutes)

```bash
mkdir -p "$PROG201/week2/lab2"        # $PROG201 is set in ~/.bashrc -- see Lab 0
cd "$PROG201/week2/lab2"
cp "$ACADEMICS/1. Sophomore/Fall/2. PROG 201 - Systems Programming in C/PROG201 Week2/lab/"{bench.c,Makefile} .

make
./bench bulk 64 4096
```

You should see the pipe row filled in and the other three showing `--`:

```
bulk: 64 MiB in 4096-byte chunks
mechanism                   seconds        MiB/s
pipe                          0.017       3735.0
FIFO                             --           --
POSIX mq                         --           --
shm + sem, 1 slot                --           --
```

**Read `bulk_pipe` and `rt_pipe` before you write anything.** They are the two worked examples, and every TODO is one of them with a different mechanism in the middle. The `-lrt` in the Makefile is not optional: `mq_*`, `shm_open` and `sem_*` live there.

**One housekeeping target you will need:** `make clean-ipc`. Message queues, shared memory objects and named semaphores are kernel-persistent (L08 §4) — a crashed run leaves its objects behind, and the next run finds them. When something behaves impossibly, run `ls /dev/shm /dev/mqueue` first.

---

## 1. Part A — FIFO and Message Queue (30 min)

**TODO 1 — `bulk_fifo`.** The same transfer through a named pipe.

The whole difference from `bulk_pipe` is that both ends open a path instead of inheriting a descriptor. The trap is L07 §5: **a blocking `open` on a FIFO does not return until the other end opens.** Get the order wrong and the function does not fail, it hangs — so decide, before you type it, which process opens first and why it cannot deadlock.

`unlink` the path *before* `mkfifo` as well as after. A FIFO left by a crashed run gives you `EEXIST` on the next one.

**TODO 2 — `bulk_mq`.** The same transfer as discrete messages.

```c
struct mq_attr a = { .mq_maxmsg = 10, .mq_msgsize = chunk };
mqd_t q = mq_open(MQ_NAME, O_CREAT | O_RDWR, 0600, &a);
if (q == (mqd_t) -1) return -1;              /* NOT if (q < 0) */
```

Two things from L08 §3 will bite you, and both are meant to:

- **`mq_msgsize` cannot exceed 8,192** for an unprivileged process, and `mq_maxmsg` cannot exceed 10. Return `-1` rather than dying when `chunk` is too large — the harness prints `--`, and in Part D that `--` is itself a result.
- **The receive buffer must be at least `mq_msgsize`**, whatever the message length. A buffer sized to the message gets you `EMSGSIZE` and half an hour of confusion.

Check both rows:

```bash
./bench bulk 256 4096
```

Expect the FIFO within about 20% of the pipe, and the message queue a little behind it. **If the FIFO is dramatically slower than the pipe, you are timing the `open` rendezvous** — start the clock after both ends are open, as `bulk_pipe` does.

---

## 2. Part B — Shared Memory, One Slot (30 min)

**Before you write any code, write down a number.** In your answer sheet, complete the sentence:

> I predict shared memory will move 256 MiB in 4 KiB chunks at about ______ MiB/s, which is ______ times the pipe's rate.

Now write it.

**TODO 3 — `bulk_shm`.** `ring_make(1)` gives you a `MAP_SHARED|MAP_ANONYMOUS` region with both semaphores inside it (L09 §1 — this is not optional; a `sem_t` in a local variable gives the parent and the child two unrelated counters).

```
producer                          consumer
--------                          --------
sem_wait(&r->empty);              sem_wait(&r->full);
memcpy(r->data[0], buf, chunk);   memcpy(sink, r->data[0], r->len);
r->len = chunk;                   sem_post(&r->empty);
sem_post(&r->full);
```

**The consumer must really copy the data out.** If you skip the `memcpy`, you are timing an empty loop and your number will be a fiction.

Wrap every `sem_wait` in the retry loop — L09 §3:

```c
while (sem_wait(&r->full) == -1 && errno == EINTR)
    ;
```

**TODO 4 — `rt_shm`.** The round trip: parent `sem_post(&full)` then `sem_wait(&empty)`; child `sem_wait(&full)` then `sem_post(&empty)`. No data moves — the handoff *is* the thing being measured. Use `ring_make(0)` so that **both** semaphores start at zero.

> **Why zero matters.** Start `empty` at 1 and the parent's first `sem_wait` succeeds without the child having done anything, so the parent runs a step ahead and you measure a pipelined half-trip instead of a round trip. The number comes out about 30% too good. This is a real mistake with a plausible-looking result, which is the worst kind.

```bash
./bench bulk 256 4096
./bench trip 100000
```

Now compare the shared-memory row with your prediction. **Do not fix anything.** The number is correct; the claim is what is wrong. Q4 and Q5 are about the gap.

---

## 3. Part C — The Ring Was the Problem (25 min)

**TODO 5 — `bulk_slots`.** `bulk_shm` with the ring indices put back:

```c
r->head = (r->head + 1) % slots;      /* producer only ever writes head */
r->tail = (r->tail + 1) % slots;      /* consumer only ever writes tail */
```

With one producer and one consumer that is all the synchronisation you need — no third semaphore, because no two processes write the same variable. Say why in your answer to Q6.

```bash
./bench slots 256 4096
```

You should get something shaped like this:

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

**Find the knee and note where the curve goes flat.** Compare the flat part with your pipe number from Part A, and with L07 §2's statement about how many buffers a pipe has. Q6.

---

## 4. Part D — Where the Claim Becomes True (20 min)

One command per row, 128 MiB each so it does not take all afternoon:

```bash
for c in 64 512 4096 16384 65536 262144; do ./bench bulk 128 $c; done
```

Build a table of `pipe` against `shm + sem, 1 slot` and the ratio between them. Ours:

| chunk | pipe MiB/s | shm MiB/s | ratio |
| --- | --- | --- | --- |
| 64 B | 79.4 | 8.8 | 0.11× |
| 512 B | 633.9 | 66.9 | 0.11× |
| 4,096 B | 3,648.7 | 670.0 | 0.18× |
| 16,384 B | 3,701.8 | 2,094.0 | 0.57× |
| 65,536 B | 2,887.9 | 6,554.8 | 2.27× |
| 262,144 B | 2,510.3 | 14,431.7 | 5.75× |

Two things to notice and write down:

1. **Where your crossover is** — the chunk size at which the ratio passes 1.0.
2. **What the `POSIX mq` column does at 16,384 and above.** It is not slow. It is gone. That is L08 §3 in the output of your own program.

---

## 5. Questions

Answer in the answer sheet. Three or four sentences each unless stated.

**Q1.** The `bulk_fifo` opens: which process opens first in your code, and what would happen if both opened `O_WRONLY` first? Answer in terms of L07 §5, not by describing what you observed.

**Q2.** `bulk_mq` returns `-1` for `chunk > 8192`. Where does that limit come from, what is the value on this machine, and what would a privileged process have to change to raise it?

**Q3.** Your `mq_receive` buffer is `chunk` bytes. Explain why a buffer sized to the *message* rather than to `mq_msgsize` fails, and quote the `errno`.

**Q4.** What did you predict in Part B, and what did you measure? Give the ratio. Then give the single sentence that best explains the gap.

**Q5.** The round trip through shared memory was only slightly faster than through a pipe — around 8% for us. If shared memory really removes the kernel, why is it not dramatically faster? *(L09 §6. One sentence about what a round trip actually consists of.)*

**Q6.** In Part C, the curve goes flat after about 8 slots. Two parts: **(a)** why does depth stop helping, and **(b)** a pipe has sixteen buffers of its own (L07 §2) — what does that tell you about what you were really comparing in Part B?

**Q7.** From your Part D table, state the rule for when to reach for shared memory over a pipe, as a condition on message size. Then name one situation where the rule says "pipe" and you would still choose shared memory anyway.

---

## 6. Checkoff

Show the TA:

- [ ] `./bench bulk 256 4096` with all four rows filled in.
- [ ] `./bench slots 256 4096`, and say out loud where the knee is and why.
- [ ] Your Part B **prediction**, written before the run, next to the measured number.
- [ ] Your written answers to **Q4, Q5 and Q6**.

**If you finish early:** set `chunk` to 4,097 in Part D and explain the pipe row using L07 §2. Then run `./bench bulk 256 4096` under `strace -c -f` and compare the system-call counts for the pipe and the one-slot ring — the ratio you find there is the whole lab in one number.

**Take with you:** the ring in Part C is Week 3's bounded buffer with threads instead of processes, and Week 5's server hands connections to workers through exactly this structure. PS 2, due Friday of Week 3, is this ring with a real producer and consumer on the ends of it.

---

*PROG 201 · Week 2 · Lab 2 · © CSE Department*
