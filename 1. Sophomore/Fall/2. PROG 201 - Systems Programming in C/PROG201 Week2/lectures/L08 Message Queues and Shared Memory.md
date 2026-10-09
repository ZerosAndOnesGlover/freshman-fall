# PROG 201 · Systems Programming in C
## Week 2 · Lecture 2 of 3
### POSIX Message Queues and Shared Memory

*“Wherever there is modularity there is the potential for misunderstanding: Hiding information implies a need to check communication.”* — Alan Perlis, "Epigrams on Programming" (1982), #20

---

**Reading:** APUE §15.7–15.9 · TLPI Ch. 48, 52, 54 · `man 7 mq_overview`, `man 7 shm_overview`, `man 2 mmap` · **Previous:** L07 · **Next:** L09 — semaphores, and choosing a mechanism

**Coursework:** 📝 **PS 2** released today, due Fri of Week 3 17:00 · 📝 **PS 1** due Fri this week 17:00 · 🔬 **Lab 2** Mon of Week 3 15:00–16:50 · 📊 **Quiz 3** Tue of Week 3

---

## 1. Two Answers to "A Stream Has No Edges"

L07 §7 listed what a pipe cannot do. The top two entries — no boundaries, no addressing — have one answer each, and they sit at opposite ends of a trade-off you will make for the rest of your career:

- **A message queue** puts the boundaries in the kernel. You send a message, the receiver gets *that message*, whole, and never half of it followed by half of the next. The kernel copies it and enforces the edge. **Safe, and it costs a copy and a system call per message.**
- **Shared memory** removes the kernel from the transfer entirely. Two processes map the same physical pages; a store by one is visible to the other with no system call at all. **Fast, and every guarantee is now yours to provide.**

The curriculum's one-line version — "shared memory is the fastest IPC mechanism" — is the standard claim and it is repeated everywhere. **L09 measures it and finds it false for small messages**, by nearly an order of magnitude. Hold the claim loosely until then; this lecture is about what each mechanism *is*.

---

## 2. A Message Queue Has Edges and Priorities

```c
#include <mqueue.h>
struct mq_attr a = { .mq_maxmsg = 10, .mq_msgsize = 64 };
mqd_t q = mq_open("/prog201", O_CREAT | O_RDWR, 0600, &a);
mq_send(q, buf, len, priority);
ssize_t n = mq_receive(q, buf, bufsize, &priority);
```

Four things about that snippet are unlike anything in Week 1.

**The name starts with a slash and contains no others.** `"/prog201"`, not `"/tmp/prog201"`. It is not a path; it is a key in a kernel namespace that happens to be *shown* under `/dev/mqueue`. Link with **`-lrt`**.

**`mqd_t` is not an `int`.** On Linux it happens to be a file descriptor and you can `poll` it, which is useful and non-portable. Compare it against `(mqd_t)-1`, never against `-1` or `NULL`.

**Messages have edges.** From `mq.c`:

```
3. sent 10 bytes, one mq_receive returned 10 -- messages have edges
```

Ten bytes in, ten bytes out, in one call. There is no partial `mq_receive`, no `read_all` loop, no framing protocol. That is the whole point.

**Messages have priorities, and they are absolute.** Send four messages, receive four:

```
2. sent   : routine(1) urgent(9) whenever(0) now(9)
   received: urgent(9) now(9) routine(1) whenever(0)
```

Strictly highest-priority-first, and **FIFO within one priority** — `urgent` came out before `now` because it was sent first. A high-priority sender can starve a low-priority one indefinitely; the kernel will not fix that for you.

### The two-byte trap

```
4. mq_receive into a 2-byte buffer for a 2-byte message -> -1, errno=Message too long
```

The message was two bytes. The buffer was two bytes. It failed.

**`mq_receive`'s buffer must be at least `mq_msgsize`** — the queue's configured maximum — regardless of how long the message actually is. The kernel checks the buffer size before it looks at the message, because it must be able to promise you the message will fit. So the only correct way to size a receive buffer is:

```c
struct mq_attr a;
mq_getattr(q, &a);
char *buf = malloc(a.mq_msgsize);      /* not sizeof your struct */
```

Do that even when you designed the queue, because `mq_open` on an existing queue **ignores your attributes** and gives you the ones it was created with.

---

## 3. The Limits Are Low, and They Are the Design Constraint

`mqlimit.c` tries five geometries as an ordinary user:

```
maxmsg=10    msgsize=8192     -> ok
maxmsg=11    msgsize=8192     -> Invalid argument
maxmsg=10    msgsize=8193     -> Invalid argument
maxmsg=1000  msgsize=64       -> Invalid argument
maxmsg=10    msgsize=1048576  -> Invalid argument
```

Ten messages. Eight kilobytes each. Those are not suggestions:

| Knob | Value here | Where |
| --- | --- | --- |
| `mq_maxmsg` ceiling | **10** | `/proc/sys/fs/mqueue/msg_max` |
| `mq_msgsize` ceiling | **8192** | `/proc/sys/fs/mqueue/msgsize_max` |
| queues per user | 256 | `/proc/sys/fs/mqueue/queues_max` |
| total bytes queued | `ulimit -q` (819200 here) | `RLIMIT_MSGQUEUE` |

A privileged process may exceed the first two; your program will not be one. **So a POSIX message queue on default Linux holds at most 80 KB, in at most ten pieces.** That is a control channel, not a data channel — and notice it is barely larger than one pipe (L07 §2: 64 KB in sixteen pieces).

This is the fact that decides most real designs, and it is nowhere in the textbook chapter. If you find yourself planning to stream a video through a message queue, the kernel will stop you at `mq_open`.

> **System V message queues** (`msgget`/`msgsnd`) are the older API, have different limits, and are still everywhere in old code. They are not on this course's syllabus, and you will meet them; `man 7 svipc` is the twenty minutes that will save you when you do.

---

## 4. An IPC Object Is Not Yours to Forget

`mq.c` deliberately exits without calling `mq_unlink`. Afterwards, from the shell:

```
$ ls -l /dev/mqueue/
-rw------- 1 adebayo-glover adebayo-glover 80 Sep  7 14:56 prog201
$ cat /dev/mqueue/prog201
QSIZE:11         NOTIFY:0     SIGNO:0     NOTIFY_PID:0
```

The queue survived the process, with its eleven bytes of undelivered messages still in it. This is **kernel persistence**, and every POSIX IPC object has it: message queues, shared memory objects, and named semaphores all live until `*_unlink` or reboot.

Consequences you will meet in the lab:

1. **A leaked object outlives your test run**, so the next run gets `EEXIST` from `O_CREAT|O_EXCL`, or worse, silently reattaches to yesterday's data. `shm_unlink` and `mq_unlink` at the *start* of a program you are developing, not only at the end.
2. **The unlink/close split is the same as a file's.** `mq_unlink` removes the name; the queue lives on for whoever still has it open. Exactly `unlink` on a file (L04 §5).
3. **Ten queues per program is nothing.** The 256-per-user limit is reached by a loop that forgets to unlink long before you notice.
4. `/dev/mqueue` and `/dev/shm` are **browsable**. `ls`, `cat`, `rm` all work, and `rm /dev/shm/foo` is `shm_unlink("/foo")`. When a lab machine behaves strangely, look there first.

---

## 5. Shared Memory: `shm_open`, `ftruncate`, `mmap`

Three calls, in that order, always:

```c
int fd = shm_open("/prog201.counter", O_CREAT | O_EXCL | O_RDWR, 0600);
ftruncate(fd, sizeof(struct region));                      /* it is born zero-length */
struct region *r = mmap(NULL, sizeof *r, PROT_READ | PROT_WRITE,
                        MAP_SHARED, fd, 0);
close(fd);                        /* the mapping keeps the object alive */
```

**`shm_open` returns an ordinary file descriptor** for an object in a `tmpfs` mounted at `/dev/shm`. Everything you learned in Week 1 applies to it: `fstat` works, `ftruncate` works, `close` works, and — the line that surprises everyone — **`close` does not unmap.** The mapping holds a reference to the underlying object. Closing the descriptor immediately after `mmap` is the normal idiom, not a bug.

Because it is a `tmpfs` file, it is visible:

```
2. /dev/shm/prog201.demo: size 4096, and cat says: written through a mapping
```

That is `head -c 25 /dev/shm/prog201.demo` reading bytes that another process wrote with `strcpy` into a pointer. **The file and the memory are the same bytes.** Week 4 is a whole week on why.

### `MAP_SHARED` against `MAP_PRIVATE`

The single most important flag in `mmap`, and `maps.c` makes the difference concrete — two anonymous mappings, a child writes 42 to both:

```
1. after the child wrote 42 to both:  MAP_SHARED=42  MAP_PRIVATE=0
```

`MAP_PRIVATE` is **copy-on-write**: the child's store faulted a private copy into existence and the parent's page never changed. That is Week 0 L01's `fork` cost table, and it is what every ordinary `malloc`'d page is. `MAP_SHARED` is the opposite: one physical frame, two page tables, no copy, no fault after the first touch.

**`MAP_SHARED | MAP_ANONYMOUS` is the underrated one.** No name, no `/dev/shm` entry, no cleanup, nothing to leak:

```c
struct region *r = mmap(NULL, sizeof *r, PROT_READ | PROT_WRITE,
                        MAP_SHARED | MAP_ANONYMOUS, -1, 0);
if (fork() == 0) { r->counter++; _exit(0); }     /* the child sees it */
```

It is inherited across `fork` and invisible to anyone else. **If the processes sharing the memory are related, use this** — it removes §4's entire class of bug. Use `shm_open` when they are not related, which is the same distinction as `pipe()` against `mkfifo()`.

---

## 6. The `SIGBUS` Trap

`gotcha.c` does the three calls of §5 with `ftruncate` left out:

```
1. mmap over a 0-byte object succeeded (0x7221b60d8000) -- mmap does not check
   the child then stored one byte: killed by Bus error
```

`mmap` succeeded. It mapped 4,096 bytes of address space over an object with **no** bytes in it, and it did not complain, because `mmap` sets up a mapping and the object's length is not consulted until a page is faulted in.

Then the first store touched a page with no backing, and the kernel raised **`SIGBUS`** — not `SIGSEGV`. Learn the difference, because it is a diagnosis you can make from the crash alone:

| Signal | Means | Typical cause |
| --- | --- | --- |
| `SIGSEGV` | "That address is not mapped, or not mapped like that" | Null pointer, write to `PROT_READ`, past the end of a mapping |
| `SIGBUS` | "That address is mapped, but there is nothing behind it" | **Mapped past the end of the object** — a forgotten `ftruncate`, or a file truncated under you |

A `SIGBUS` in a program that uses `mmap` is almost always a length mismatch. And note the second cause: if another process shrinks the file while you have it mapped, **your process gets `SIGBUS` for something it did not do.**

Two more rules that follow from the same mechanism:

- **`ftruncate` on an existing object is destructive and racy.** The second process to attach should `fstat` and check the size, not `ftruncate` again.
- **Map whole pages.** A mapping is rounded up to a page; bytes between your length and the page end are readable and are not part of the object. Writing there is silently pointless.

---

## 7. What Shared Memory Does Not Give You

You have mapped the same page in two processes. Here is the exact list of what you have and have not bought.

**You have:**
- Zero-copy visibility. A store is visible to the other process without a system call.
- Arbitrary structure. Structs, arrays, a whole hash table if you want one — with pointers replaced by offsets, because the mapping may land at a different address in each process.

**You have not:**

| Missing | What happens without it | Fixed by |
| --- | --- | --- |
| **Mutual exclusion** | `counter++` is load-add-store, and two processes lose updates. **64.7% of them, measured** | L09 §2 — a semaphore |
| **Notification** | Nothing wakes the reader. Polling burns a core; sleeping adds latency | L09 §5 — a semaphore as a signal |
| **Boundaries** | The region is bytes. Where one record ends is your convention | Your header struct |
| **Ordering** | The compiler and the CPU may reorder your stores | `atomic_*`, or the barrier a mutex already contains |
| **Cleanup** | The object outlives everybody (§4) | `shm_unlink`, or `MAP_SHARED|MAP_ANONYMOUS` |
| **Address stability** | The same region is at a different address in each process | Store offsets, never pointers |

Every row is a job the kernel did for you in a pipe and now does not. **That is the trade, stated exactly: you are not buying speed, you are buying the removal of the kernel — and the kernel was doing six useful things.**

L09 puts numbers on the first row and on the claim that this is faster at all.

---

## Summary

- A **message queue** gives you edges and priorities: `mq_receive` returns exactly one message, highest priority first, FIFO within a priority.
- The receive buffer must be **at least `mq_msgsize`**, not the message's length, or `EMSGSIZE`.
- Default unprivileged Linux caps a queue at **10 messages of 8,192 bytes** — 80 KB total. It is a control channel.
- POSIX IPC objects are **kernel-persistent**: they outlive every process until `*_unlink`. `/dev/mqueue` and `/dev/shm` are where the leaks show up.
- **Shared memory is `shm_open` + `ftruncate` + `mmap(MAP_SHARED)`**, and `close` after `mmap` is correct — the mapping holds the reference.
- **`MAP_SHARED|MAP_ANONYMOUS` for related processes.** No name, no leak.
- Mapping past the end of an object gives **`SIGBUS`**, not `SIGSEGV`. It means "mapped, but nothing behind it."
- Shared memory removes the kernel from the transfer, and with it: mutual exclusion, notification, boundaries, ordering, cleanup and address stability.

---

## Exercises

1. `mq_open` an existing queue with attributes different from the ones it was created with. Which set do you get? Prove it with `mq_getattr`.
2. Write a program that creates a message queue and exits without unlinking. Find it from the shell, read its `QSIZE`, and remove it two ways — `rm` and `mq_unlink`.
3. Send messages at priorities 0 and 5 from two processes in a tight loop, and receive slowly. Measure how long a priority-0 message waits. This is starvation; state the condition under which it is unbounded.
4. Map a `shm_open` object twice in the same process at two addresses. Write through one pointer, read through the other. Explain the result in terms of §5.
5. Reproduce the `SIGBUS`, then fix it with `ftruncate`. Now `ftruncate` the object *smaller* from a second process while the first has it mapped, and touch the far end. Which process dies?
6. `MAP_SHARED|MAP_ANONYMOUS`, `fork`, and have the child write. Now do it with `posix_spawn` instead of `fork`. Why does the second one not work, and what is the minimum change that makes it?
7. A struct in shared memory contains a `char *` into the same region. Print it from both processes. Then rewrite it with an offset and print again.

---

*PROG 201 · Week 2 · L08 · © CSE Department*
