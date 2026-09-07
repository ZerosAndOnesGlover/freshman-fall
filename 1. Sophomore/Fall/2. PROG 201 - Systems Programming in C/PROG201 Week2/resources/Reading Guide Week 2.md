# PROG 201 · Reading Guide · Week 2
## APUE Chapter 15, and the four `man 7` pages that are better than the book

---

**Week 2 is where APUE shows its age.** Chapter 15 is written around System V IPC — `msgget`, `semget`, `shmget` — which is the API you will *read* in old code and should not *write*. The POSIX interfaces this course teaches (`mq_open`, `sem_open`, `shm_open`) get a fraction of the space, and the Linux-specific limits that decide every real design are not in it at all.

So the reading is split, and the man pages are not optional this week.

| Source | Read? | Why |
|---|---|---|
| **APUE 15.1–15.5** | **All of it** | Pipes, `popen`, coprocesses, FIFOs. Still the best pipe writing there is |
| APUE 15.6–15.8 | **Skim** | System V IPC. Know the shape, know `ipcs`, do not write it |
| **APUE 15.9–15.10** | **Read** | POSIX semaphores and shared memory — short, and it is L08–L09 |
| **TLPI Ch. 44** | **All of it** | Pipes and FIFOs done properly, including §44.7's write-end trick |
| **TLPI Ch. 52** | **Read** | POSIX message queues, with the limits |
| **TLPI Ch. 53–54** | **Read** | POSIX semaphores; POSIX shared memory |
| TLPI Ch. 45–48 | Later | System V. Come back when you meet it |

---

## APUE Chapter 15 — the questions to hold

**§15.2 Pipes**

1. Stevens draws a pipe two ways — one process, and two after a `fork`. Redraw both **with the three tables from L04 §2** underneath. Where is the pipe's buffer in that picture?
2. He says a pipe is half-duplex. Find the paragraph where he mentions full-duplex pipes on some systems, and say why a portable program does not use them.
3. **Why does `popen` return a `FILE *` and not a descriptor?** Then find `pclose` and say what it does that `fclose` does not.

**§15.3 `popen` and `pclose`**

4. Stevens' `popen` implementation keeps an array indexed by descriptor. Say why it must, in one sentence about what `pclose` has to return.
5. `popen("...", "r")` gives you a pipe from a shell. **Name two things that go wrong if the string contains user input.** *(Week 10 spends a whole lecture on this.)*

**§15.5 FIFOs**

6. Stevens gives two uses for FIFOs: shell pipelines that are not linear, and client-server rendezvous. Work through the client-server example and find the place where the server would see a spurious EOF. **How does he avoid it?** Compare with L07 §6.
7. He notes a FIFO write of more than `PIPE_BUF` may interleave. Find that sentence, and then find `PIPE_BUF`'s value in `<limits.h>` on your machine.

**§15.9–15.10 POSIX semaphores and shared memory**

8. Where does Stevens say a `sem_t` must live for two *processes* to share it? Check your answer against L09 §1 before you accept it.
9. He shows `shm_open` + `ftruncate` + `mmap`. **Which of those three can be omitted, and which one causes `SIGBUS` if you skip it?**

---

## The Man Pages for This Week

These four are short, current, and Linux-specific in exactly the ways the book is not. **Read all four.**

| Page | The paragraph that matters |
|---|---|
| **`man 7 pipe`** | "I/O on pipes and FIFOs" — the atomicity rule, `PIPE_BUF`, and the `O_NONBLOCK` variants of it. Also the capacity paragraph and `F_SETPIPE_SZ` |
| **`man 7 fifo`** | The whole thing is one page. The `O_RDONLY`/`O_WRONLY` non-blocking asymmetry and `ENXIO` |
| **`man 7 mq_overview`** | The limits section: `msg_max`, `msgsize_max`, `queues_max`, `RLIMIT_MSGQUEUE`. **This is the page L08 §3 is built from** |
| **`man 7 sem_overview`** | Named against unnamed, and the `sem.` prefix under `/dev/shm` |

**And two more to know exist:** `man 7 shm_overview` (three paragraphs, all useful) and `man 2 mmap` (enormous — read the flags table and the ERRORS section, especially `SIGBUS`).

---

## Where to Go Deeper

| TLPI | Topic |
|---|---|
| §44.6 | Pipe capacity and `F_SETPIPE_SZ`, with the kernel's reasoning |
| §44.7 | The FIFO server's EOF problem and the extra write descriptor. L07 §6 |
| §52.4 | Message queue limits — the table L08 §3 measures |
| §53.4 | Named against unnamed semaphores, and when the distinction bites |
| §54.2–54.5 | POSIX shared memory objects, and the `ftruncate` requirement |
| Ch. 63 | Alternative I/O models. Week 5's reading, and the answer to "how does a server wait on ten pipes at once" |

---

## The Habit for This Week

**Read the limits before you read the API.**

Week 1's habit was to write your prediction down first. This week's is narrower and it will save you a whole design: **before you commit to an IPC mechanism, find the number that caps it.** A pipe is sixteen pages. A message queue is ten messages of eight kilobytes. A semaphore's value is an `unsigned int`. Every one of those is in a man page you can read in four minutes, and every one of them has ended somebody's architecture in week three of a project.

The limits are not footnotes to the interface. **On this subject they are most of the interface.**

---

*PROG 201 · Week 2 · Reading Guide · © CSE Department*
