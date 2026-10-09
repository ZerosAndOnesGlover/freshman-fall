# PROG 201 · Systems Programming in C
## Week 1 · Lecture 2 of 3
### `read`, `write`, and What a System Call Costs

*“A programming language is low level when its programs require attention to the irrelevant.”* — Alan Perlis, "Epigrams on Programming" (1982), #8

---

**Reading:** APUE §3.5–3.9, §5.4 · **Previous:** L04, the three tables · **Next:** L06, `dup2` and non-blocking I/O

**Coursework:** 📝 **PS 1** released today, due Fri of Week 2 17:00 · 📝 **PS 0** due Fri this week 17:00 · 🔬 **Lab 1** Mon of Week 2 15:00–16:50 · 📊 **Quiz 2** Tue of Week 2

---

## 1. Two Calls, and Neither Does What Its Name Suggests

```c
ssize_t read (int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
```

Read this as: *"transfer **up to** `count` bytes, and tell me how many you actually moved."* Both return a `ssize_t` — signed, because `-1` is an answer — and **the returned count is routinely less than `count` with nothing wrong at all**.

| Return | Means |
|---|---|
| `n == count` | The common case, and the one that hides the other rows |
| `0 < n < count` | **A short transfer.** Normal. Not an error |
| `0` from `read` | **End of file** — or, on a pipe, all writers have closed |
| `0` from `write` | You asked for 0 bytes |
| `-1`, `errno == EINTR` | A signal landed mid-call. Retry (W0 L03 §6) |
| `-1`, `errno == EAGAIN` | Non-blocking, nothing available right now (L06 §5) |
| `-1`, other | A real error |

**The single most common bug in student systems code** is `write(fd, buf, n);` with the return value discarded. It works on a file, on a small buffer, on an unloaded machine — and then loses the tail of a message on a socket under load, silently.

**The loop you write instead, and will keep writing all term:**

```c
static ssize_t write_all(int fd, const void *buf, size_t n)
{
    const char *p = buf;
    size_t left = n;
    while (left > 0) {
        ssize_t w = write(fd, p, left);
        if (w < 0) { if (errno == EINTR) continue; return -1; }
        p += w; left -= w;
    }
    return (ssize_t) n;
}
```

Twelve lines. Put it in a header in Week 1 and use it until Week 12.

---

## 2. What a System Call Costs, Measured

A system call is not a function call. It is a mode switch: the CPU changes privilege level, the kernel validates your arguments, does the work, and switches back. **On this machine that is on the order of a microsecond**, and the way to see it is to keep the work constant and vary how many calls you make.

`bufsize.c` copies a 64 MB file with `read`/`write` and nothing else — no stdio, no `mmap`:

| Buffer | Time | Throughput | System calls |
|---:|---:|---:|---:|
| **1 B** | **167.964 s** | 0.4 MB/s | 134,217,728 |
| 16 B | 11.294 s | 5.9 MB/s | 8,388,608 |
| 256 B | 0.854 s | 78.5 MB/s | 524,288 |
| **4 KB** | **0.222 s** | 303.0 MB/s | 32,768 |
| 64 KB | 0.171 s | 393.4 MB/s | 2,048 |
| 1 MB | 0.168 s | 399.0 MB/s | 128 |

**A thousand times slower at one byte at a time**, for identical work and identical data. And then look where it stops mattering: **between 4 KB and 1 MB the whole range is within a factor of 1.3.**

Two conclusions, and the second is the useful one:

1. Per-call overhead dominates until the buffer is big enough to amortise it. 168 s / 134 M calls ≈ **1.25 µs per call**, which is the number to carry around.
2. **4 KB is where the curve flattens** — one page, and not a coincidence: it is the unit the page cache deals in. Beyond it you are optimising something that is no longer the bottleneck. *(This is why `BUFSIZ` is 8192 in glibc, and why `cp` uses 128 KB rather than 16 MB.)*

> **This is the whole reason `stdio` exists.** `printf`, `fputc` and `fread` are a **buffer** — 4096
> bytes by default — sitting on top of `write` and `read`, turning a thousand `putchar` calls into
> one system call. W0 L01 §6's duplicated `hello` was that buffer being copied by `fork`. When you
> use `printf` you are opting into the 4 KB row of this table; when you use `write` you are choosing
> your own row.

---

## 3. Partial Writes Are Not Hypothetical

The clearest place to see one is a pipe, whose capacity is fixed:

```
pipe filled after 65536 bytes (64 KB); next write: errno=11 (EAGAIN)
F_GETPIPE_SZ reports 65536 bytes
```

**A pipe holds 64 KB on this machine.** Write 100 KB into one with no reader draining it and — if the descriptor is blocking — the call *blocks* partway through; if it is non-blocking, it returns having written some prefix, and the rest is your problem. Sockets behave the same way with a send buffer instead of a pipe buffer, which is why Week 5's server is built on `write_all` from the start.

**One guarantee you do get:** a write of `PIPE_BUF` bytes or fewer (4096 on Linux) to a pipe is **atomic** — it is not interleaved with another writer's data. Above `PIPE_BUF`, all bets are off, and two processes logging 8 KB lines through one pipe will produce spliced output. `man 7 pipe` states it exactly; it is worth reading the paragraph.

---

## 4. `lseek`, and the File That Is Bigger Than the Disk

`lseek(fd, offset, whence)` moves the offset in the open file description (L04 §2) and returns the new position. `lseek(fd, 0, SEEK_CUR)` is therefore how you *ask* where you are without moving.

Seeking past the end of a file is legal, and what happens next is a genuinely surprising property of Unix:

```c
int fd = open("sparse.bin", O_WRONLY|O_CREAT|O_TRUNC, 0644);
lseek(fd, 1024L*1024*1024, SEEK_SET);   /* 1 GB past the start */
write(fd, "end", 3);                    /* three bytes */
```

```
  ls -l  says:  1073741827 bytes
  apparent :  1.1G
  on disk  :  4.0K
```

**A 1.1 GB file occupying 4 KB.** The gap is a **hole**: the filesystem records that those blocks are unallocated, `read` returns zeros for them, and no disk is spent until something writes there. This is how VM disk images, core dumps and database files are stored, and it is why `du` and `ls -l` disagree — `ls` reports the size, `du` reports the allocation.

**The practical trap:** copying a sparse file with a naive `read`/`write` loop **fills the holes in**, turning 4 KB into 1.1 GB. `cp --sparse=auto` and `rsync -S` exist for this. Your Lab 1 pipeline will happily do the wrong thing here, and that is worth knowing before you write a backup script.

---

## 5. Atomicity: the Experiment That Loses 95% of Its Data

Four processes, each appending 20,000 lines to the same file. **Every process opens the file itself**, so each has its own open file description and its own offset (L04 §2).

**Version A — the obvious one.** Seek to the end, then write:

```c
lseek(fd, 0, SEEK_END);
write(fd, line, n);
```

**Version B.** Open with `O_APPEND` and just write.

```
--- lseek(END)+write, separate descriptions ---
  noappend.log: 4396          expected: 80000
--- O_APPEND ---
  append.log: 80000           expected: 80000
```

**4,396 lines out of 80,000.** Version A lost 95% of its data, with no error from any system call, on a machine that was not even busy.

**Why.** `lseek` and `write` are two system calls. Between them, another process seeks to the same end-of-file and writes there; both processes then write to the same offset, and the second overwrites the first. The window is microseconds wide and it is hit constantly.

**`O_APPEND` is not a convenience.** It moves the seek *inside* the write, under the inode lock, so "go to the end and write" becomes one indivisible operation. That is the whole difference between the two runs.

> **The general shape, and it is the same shape as `O_CREAT|O_EXCL` in L04 §5:** whenever you find
> yourself doing *check-then-act* or *seek-then-write* across two system calls on shared state, look
> for the flag that fuses them. If there isn't one, you need a lock (Week 3) — and the reason Unix
> has so many single-purpose flags is that a flag is cheaper than a lock.

**Where this bites in practice:** every multi-process log file. It is why `open(..., O_WRONLY|O_APPEND)` is what every logging library does, and why a log with mysteriously missing lines is almost always a program that reopened the file without the flag.

---

## 6. What to Take Away

1. **`read` and `write` transfer *up to* what you asked.** Check the return; write `write_all` once.
2. **A system call costs ~1.25 µs here.** One byte at a time is 1000× slower than 4 KB at a time, for the same work.
3. **The curve flattens at one page.** Past 4 KB you are tuning something that stopped being the bottleneck; `stdio` is exactly this buffer, done for you.
4. **A pipe holds 64 KB**, and writes up to `PIPE_BUF` (4 KB) are atomic. Beyond that, interleaving is legal.
5. **Holes are real.** A 1.1 GB file can occupy 4 KB, and a naive copy destroys that.
6. **`lseek`+`write` from two processes loses 95% of the data. `O_APPEND` loses none.** Two system calls are not one, ever.

---

## Exercises

1. Reproduce the buffer-size table on your own machine. Where does *your* curve flatten, and what is your per-call cost?
2. Run `strace -c ./bufsize in out 1` for a **small** file and read the `write` row. What is the ratio of system time to wall time?
3. Fill a pipe with a blocking write end and no reader. What state does `ps -o stat,wchan` report for the process?
4. Create the sparse file, then copy it with `cp` and with `cat < sparse.bin > copy.bin`. Compare `du` on all three. Explain.
5. Run the `O_APPEND` experiment with 1, 2 and 8 workers. Plot lines-lost against worker count and explain the shape.
6. `write(fd, buf, 0)` returns 0 and is not an error. Find a case where a program that treats `0` as EOF on `write` breaks.

---

*PROG 201 · Week 1 · L05 · © CSE Department*
