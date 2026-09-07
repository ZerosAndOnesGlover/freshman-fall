# PROG 201 · Systems Programming in C
## Week 2 · Lecture 1 of 3
### Pipes as a Ring of Pages, and FIFOs

---

**Reading:** APUE §15.1–15.5 · TLPI Ch. 44 · `man 7 pipe`, `man 7 fifo`, `man 3 mkfifo` · **Previous:** L06 · **Next:** L08 — message queues and shared memory

---

## 1. What Week 1 Left Open

L06 used `pipe()` as plumbing: two descriptors, bytes in one end and out the other, and a rule about when EOF arrives. That was enough to build `ls | grep | wc`, and it is not enough to build anything that has to keep working under load.

Three questions Lab 1 did not have to answer, and this week's work does:

1. **How much can a pipe hold?** Lab 1's stages never filled one. A logging daemon fills one every day.
2. **If two processes write to the same pipe, do their records survive?** Sometimes. The rule is exact, it is in `man 7 pipe`, and getting it wrong produces a bug that does not reproduce on your machine.
3. **How do two processes that are not related get a pipe between them?** They cannot — `pipe()` hands you two descriptors and the only way to give one away is inheritance. That is what a **FIFO** is for.

The through-line for the week: **a pipe is a fixed-size buffer in the kernel with a lock around it.** Every property below falls out of that sentence.

---

## 2. A Pipe Holds Sixteen Pages, Not 65,536 Bytes

The number everybody quotes is 64 KB. Measure it and the number is right, but the *unit* is wrong, and the unit is what predicts the surprising case.

`capacity.c` sets `O_NONBLOCK` on the write end and writes fixed-size chunks until `EAGAIN`:

```
   chunk   bytes in   writes efficiency
       1      65536    65536     100.0%
      64      65536     1024     100.0%
    1024      65536       64     100.0%
    2048      65536       32     100.0%
    4095      65520       16     100.0%
    4096      65536       16     100.0%
    4097      45066       11      68.8%
    8192      65536        8     100.0%
   16384      65536        4     100.0%
   65536      65536        1     100.0%
```

Nine rows say 65,536 and one says **45,066**. That row is the lecture.

A Linux pipe is a **ring of sixteen buffers**, each one page (4,096 bytes here — `getconf PAGESIZE`). `F_GETPIPE_SZ` reports 65,536 because 16 × 4,096 = 65,536, but the limit the kernel actually enforces is *sixteen slots*.

A write either lands in the tail slot or gets a new one. `pipe_write()` in `fs/pipe.c` will merge a write into the tail slot only when **the whole write fits in the room left there** — so:

| chunk | what happens | slots for 16 writes |
| --- | --- | --- |
| 64 B | merges 64 at a time until the page is full, then a new slot | 1 slot per 64 writes — packs perfectly |
| 4,095 B | first write leaves 1 byte free; the next 4,095 does not fit in 1 byte, so it takes a new slot | 1 slot per write, **16 bytes wasted** |
| 4,096 B | exactly one slot each | 1 slot per write |
| 4,097 B | one page plus one byte — spills, and the spill poisons the packing | **11 writes and the ring is full** |

The 4,095 row is the quiet one: full marks for efficiency because 65,520 of 65,536 got in, but it used one slot per write. **The ring ran out of slots, not out of bytes.**

**The rule to carry:** a pipe's capacity is sixteen buffers, and a write whose size is not a divisor of the page size wastes some of them. If you are streaming records, make the record size a power of two ≤ 4,096, or batch until you have a page.

You can move the ceiling:

```
default F_GETPIPE_SZ : 65536 bytes
after F_SETPIPE_SZ 1 MiB : granted 1048576, accepted 1048576
F_SETPIPE_SZ 128 KiB     : granted 131072
```

`fcntl(fd, F_SETPIPE_SZ, n)` rounds up to a page and is capped, for an unprivileged process, by `/proc/sys/fs/pipe-max-size` (1 MiB by default). It is a real tool for a real problem — a bursty producer with a reader that stalls — and it is the wrong first reflex, because a bigger buffer converts a fast failure into a slow one.

---

## 3. The Four Ways a Pipe Blocks

| Situation | `read` | `write` |
| --- | --- | --- |
| Buffer empty, a write end is open somewhere | blocks | — |
| Buffer empty, **no** write end open anywhere | returns **0** (EOF) | — |
| Buffer full, a read end is open somewhere | — | blocks until space |
| **No** read end open anywhere | — | **`SIGPIPE`**, or `EPIPE` if you ignore it |

With `O_NONBLOCK` the two "blocks" rows become `EAGAIN` and the other two do not change: **EOF is not an error and a dead reader is not a wait.**

The asymmetry is deliberate. A reader with no writer has learned something final — the stream is over — and gets a value. A writer with no reader has learned something worse — the work it is doing is pointless — and gets a signal, because the correct response is usually to stop, and a return value can be ignored.

L06 stated the EOF rule; it is worth restating in the form that survives a debugging session at 2am:

> **A pipe reports EOF when the last write-end descriptor, in every process, is closed.** A descriptor you forgot to close in a process that is still running holds the pipeline open forever, and `ps -o pid,wchan,cmd` will show the reader parked in `pipe_read`.

---

## 4. `PIPE_BUF`, and the Bug That Does Not Reproduce

Two processes write records into one pipe. Does a reader ever see half of one record followed by half of another?

POSIX's answer is exact:

> Write requests of `{PIPE_BUF}` bytes or less shall not be interleaved with data from other processes doing writes on the same pipe.

`PIPE_BUF` is in `<limits.h>` — **not** `<unistd.h>`, which is where people look — and on Linux it is **4,096**.

`atomic.c` forks four writers, each writing 200 records of one repeated letter, and counts how many records come out uniform. The second column is the same program with a reader that sleeps 200 µs between small reads, so the pipe stays full:

| record size | fast reader | slow reader |
| --- | --- | --- |
| 512 B | 0 torn | **0 torn** |
| 4,096 B | 0 torn | **0 torn** |
| 4,097 B | 10 torn of 800 (1.2%) | **679 torn of 800 (84.9%)** |
| 8,192 B | 0 torn | **792 torn of 800 (99.0%)** |
| 65,536 B | 0 torn | **799 torn of 800 (99.9%)** |

Read the 8,192 row twice.

**With a fast reader, an 8 KB record never tore in 800 attempts.** A test suite would pass. A code review would pass. The record size is twice `PIPE_BUF`, the guarantee does not cover it, and the program is wrong — but nothing on the machine will say so until the reader falls behind in production, at which point 99% of the records are corrupt.

The mechanism is simple once you have §2. A write larger than the space left in the ring is split: the kernel puts in what fits, blocks, and resumes when the reader drains — and any other writer that is waiting gets in between. A write of `PIPE_BUF` or less is never split, because the kernel will not begin it until that much room exists.

**"Slow reader" is not quite the condition, and the difference matters when you try to reproduce this.** A reader that sleeps but then drains a whole record in one `read` does **not** tear anything: 8,000 records of 8 KB from four writers came through clean. Tearing needed a reader that drains in pieces *smaller than a record* — 997 bytes at a time — at which point 1,192 of 1,200 records were corrupt. The plausible reason is that freeing a record's worth of space at once lets the writer at the head of the queue finish its record before anyone else is woken, while dribbling out 997 bytes lets each blocked writer add a fragment in turn. **Do not rely on that detail** — it is one kernel's scheduling, not a guarantee. Rely on the bound, which is a guarantee.

**Three consequences worth memorising:**

1. **`PIPE_BUF` is a promise about the writer's request size, not about the pipe's capacity.** 4,096 is atomic even though 65,536 fit.
2. **`O_NONBLOCK` changes the guarantee.** With `O_NONBLOCK` set, a write of ≤ `PIPE_BUF` either goes in entirely or fails with `EAGAIN` — it is never partial. A write of more than `PIPE_BUF` *may* be partial, and then you have torn your own record with no other writer involved.
3. **The absence of a symptom is not evidence.** This is the general lesson and it outlives pipes. When a guarantee has a stated bound, the test that matters is the one that puts the system past the bound — here, a slow reader.

---

## 5. A FIFO Is a Name, Not a File

`pipe()` has one weakness: the only way to hand somebody the other end is to `fork`. Unrelated processes — a daemon started at boot and a command you type now — have no common ancestor to inherit from.

A **FIFO**, or named pipe, is the same kernel object with a name in the filesystem:

```c
mkfifo("/tmp/prog201.fifo", 0600);        /* creates the name */
int w = open("/tmp/prog201.fifo", O_WRONLY);
```

`fifo.c` demonstrates the four behaviours that catch people:

```
1. mkfifo made a FIFO of size 0
2. open(O_WRONLY|O_NONBLOCK), no reader -> -1, errno=No such device or address
3. open(O_RDONLY|O_NONBLOCK), no writer -> 3, errno=-
   read() on it -> 0, errno=-   (no writer ever attached)
4. blocking open(O_WRONLY) returned after 0.300 s -- it waited for a reader
5. after all that, the FIFO's st_size is still 0 -- no data lives in the name
```

**(1) and (5): the name is not storage.** `ls -l` shows a `p` in the mode field and a size of 0, always. The bytes live in the same sixteen kernel pages a `pipe()` gets; the directory entry is a rendezvous point and nothing else. Delete the FIFO while both ends are open and the conversation continues — you have removed the name, not the pipe. This is `open`-then-`unlink` from L04 §5, and it is the same inode logic.

**(4) `open` on a FIFO is a rendezvous.** A blocking `open(O_WRONLY)` does not return until some process opens the read end, and vice versa. That is unlike every other `open` you have written, and it is why a FIFO-based program can hang in a place where no hang looks possible. The 0.300 s in the output is exactly how late the reader was.

**(2) and (3): the non-blocking cases are asymmetric.** `O_RDONLY|O_NONBLOCK` succeeds immediately with no writer — you get a descriptor that reads EOF. `O_WRONLY|O_NONBLOCK` **fails with `ENXIO`**, because a write end with no reader is useless: the first write would raise `SIGPIPE`. POSIX prefers to tell you now.

That asymmetry gives the standard idiom for a server that must not block on startup:

```c
int r = open(path, O_RDONLY | O_NONBLOCK);      /* always succeeds */
fcntl(r, F_SETFL, fcntl(r, F_GETFL) & ~O_NONBLOCK);   /* now make reads block */
```

Open non-blocking to avoid waiting for the first client, then clear the flag so the read loop is an ordinary blocking one. Note the `F_GETFL`-modify-`F_SETFL` dance — L06 §5's trap, and this is the case that makes you need it.

---

## 6. The FIFO Server's EOF Problem

Here is the bug every first FIFO server has. The server opens the FIFO for reading and loops. Five clients connect one after another, each writing one request and closing.

`fifoeof.c`, without the fix:

```
   server saw: request 0
   server saw: EOF (1)
plain O_RDONLY:            1 of 5 requests read, 1 EOF
```

The server handled one request and shut down, because when client 0 closed its write end **there was no write end open anywhere**, which is the §3 rule, which means EOF. The server cannot tell "no client right now" from "no client ever again" — a stream has no way to say either.

The fix is one line, and it looks like nonsense until you have §3:

```c
int r    = open(path, O_RDONLY);
int keep = open(path, O_WRONLY);     /* never written to.  Never. */
```

```
   server saw: request 0
   server saw: request 1
   server saw: request 2
   server saw: request 3
   server saw: request 4
holding a write end:       5 of 5 requests read, 0 EOF
```

The server holds a write-end descriptor it will never use, purely so that the *last* write end never closes, so `read` never returns 0, so a gap between clients is a **block** rather than an end.

**Be precise about what goes wrong without it, because it is not what it looks like.** EOF on a FIFO is not permanent. `reopen.c` reads, sees EOF, waits, and a new writer turns up:

```
read 6: first
read 0 (EOF)
read 0 (EOF)
read 7: second
```

The same descriptor came back to life. So the server above did not *have* to exit — it chose to, because `n == 0` is what a program written for files means by "finished". A server that loops instead of exiting has the other bug: between clients, `read` returns 0 **immediately, forever**, and the loop is a spin at 100% CPU. Neither behaviour is what you want, and both come from the same place: **a stream has one way to say "no more bytes" and two things to mean by it.**

That is the symptom to recognise. TLPI §44.7 recommends the extra descriptor for exactly this reason; Week 5's sockets can distinguish a closed connection from an idle listener, which is one of several reasons servers are not built on FIFOs.

---

## 7. What a Pipe Cannot Do

Everything in §1–6 is one mechanism seen from different angles, and its limits are as sharp as its guarantees:

| Missing | What it means | Where the term fixes it |
| --- | --- | --- |
| **Boundaries** | The reader gets bytes, not records. Framing is your problem above 4,096 bytes | L08 — message queues have edges |
| **Addressing** | One writer cannot say "this is for you". Everything goes to whoever reads first | L08 — priorities; Week 5 — sockets |
| **Random access** | No `lseek`. It is `ESPIPE` and always will be | L08 — shared memory is memory |
| **A reply** | One direction. Two pipes for a conversation, and now you can deadlock | §6's `keep` trick; Week 5 |
| **Bulk speed without copies** | Every byte is copied user → kernel → user | L09 — measured, and the answer is not what you expect |
| **A way to say "still here"** | EOF means both "done" and "nobody home" | §6 |

None of that makes pipes bad. `ls | grep | wc` needs none of it, which is why the shell has used pipes for fifty years and why Lab 1 was 60 lines. **Reach for something else when you need one of the rows above — and be able to name which row.**

---

## Summary

- A pipe is **sixteen page-sized buffers in a ring**. 65,536 bytes is what that comes to; the enforced limit is the slot count, which is why 4,097-byte writes fill it at 68.8%.
- `F_SETPIPE_SZ` moves the ceiling, up to `/proc/sys/fs/pipe-max-size`.
- `read` on an empty pipe with no writers returns **0**; `write` with no readers raises **`SIGPIPE`**. Asymmetric on purpose.
- **`PIPE_BUF` is 4,096 and it is a bound on your request size.** At or below it, concurrent writes never interleave — measured, 0 torn records in 800. Above it, they interleave **only when the reader falls behind**: 8 KB records were 0% torn with a fast reader and **99.0% torn with a slow one**.
- A **FIFO** is a pipe with a name. The name holds no data, `open` is a rendezvous, `O_RDONLY|O_NONBLOCK` succeeds with no peer and `O_WRONLY|O_NONBLOCK` fails with `ENXIO`.
- A FIFO server must **hold a write-end descriptor open** or the first client's exit ends the server.

---

## Exercises

1. Run `capshape.c` with chunk sizes 2,049 and 3,000. Predict the byte count from §2 before you run it, then explain the result in terms of slots.
2. Raise a pipe to 1 MiB with `F_SETPIPE_SZ` and re-run the 4,097-byte row. Does the 68.8% figure change? Should it?
3. `PIPE_BUF` is 4,096 on Linux and 512 on some other systems. POSIX requires it to be at least 512. Write the one-sentence rule for portable record sizes that follows.
4. Modify `atomic.c` so the four writers use `O_NONBLOCK` and 8 KB records, counting short writes. How many records does it tear *with a fast reader*?
5. Build the §5 idiom — non-blocking `open`, then clear `O_NONBLOCK` — and prove with `strace` that exactly one `fcntl(F_GETFL)` and one `fcntl(F_SETFL)` happen.
6. Write the server from §6 as a loop that does **not** exit on EOF and does **not** hold a write end. Run it with `time` and one client. Where did the CPU go, and which line is spinning?
7. `mkfifo` a path and run `cat < fifo` in one terminal and `ls > fifo` in another. Now do it in the other order. Explain the pause, in the vocabulary of §5.

---

*PROG 201 · Week 2 · L07 · © CSE Department*
