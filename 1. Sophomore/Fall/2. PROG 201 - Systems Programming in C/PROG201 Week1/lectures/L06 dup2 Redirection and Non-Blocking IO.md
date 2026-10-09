# PROG 201 · Systems Programming in C
## Week 1 · Lecture 3 of 3
### `dup2`, Redirection, and Non-Blocking I/O

*“In Unix, one tries to design programs to operate not specifically with each other, but with programs as yet unthought of.”* — Doug McIlroy, as quoted in Eric S. Raymond, *The Art of Unix Programming* (2003)

---

**Reading:** APUE §3.12, §14.6, §14.7 · TLPI Ch. 5, §63.5 · **Previous:** L05 · **Next:** Lab 1 — build `ls | grep | wc` in C

**Coursework:** 📝 **PS 0** due Fri this week 17:00 · 🔬 **Lab 1** Mon of Week 2 15:00–16:50 · 📊 **Quiz 2** Tue of Week 2 · 📝 **PS 2** released Wed of Week 2, due Fri of Week 3 17:00

---

## 1. `dup` and `dup2` Copy the Index, Not the File

```c
int new = dup(old);            /* lowest free descriptor, same open file description */
int r   = dup2(old, want);     /* make `want` a copy of `old`, closing `want` first  */
```

Both make a **new entry in the descriptor table pointing at the same open file description** (L04 §2). Same offset, same status flags, same everything except the number — which is the entire point, because the number is what a program you did not write is going to use.

`dup2` differs from `dup` in two ways that matter:

- **You choose the number.** That is what makes redirection possible: a child's stdout must be descriptor **1** specifically, because `execvp` is about to run a program that writes to 1 without asking.
- **It closes the target first, atomically.** `close(1); dup(fd);` is the same thing with a race in the middle — if a signal handler or another thread opens something between the two calls, you have redirected the wrong descriptor. **`dup2` cannot be interrupted between the close and the copy.**

If `old == want`, `dup2` does nothing and returns `want` — deliberately, so that `dup2(fd, 1)` is safe even when `fd` is already 1.

---

## 2. Redirection, Written Out

`ls > listing.txt`, with no shell involved:

```c
if (fork() == 0) {
    int fd = open("listing.txt", O_WRONLY|O_CREAT|O_TRUNC, 0644);
    dup2(fd, STDOUT_FILENO);     /* descriptor 1 now refers to the file */
    close(fd);                   /* the extra descriptor has done its job */
    execlp("ls", "ls", "-1", "/etc/hosts", "/etc/hostname", (char *) 0);
    _exit(127);
}
wait(0);
```

```
  listing.txt now holds:
    /etc/hostname
    /etc/hosts
```

**`ls` was not modified, recompiled, or told anything.** It writes to descriptor 1 as it always does; the shell rearranged what descriptor 1 *means* in the moment between `fork` and `exec`. **That window is why Unix separates the two calls** (W0 L01 §8), and this is the payoff of the design.

**Three details that are not decoration:**

- **`close(fd)` after the `dup2`.** The file now has two descriptors pointing at it; leaving the spare open leaks it into the exec'd program and, for a pipe, prevents EOF (§3).
- **The order is `open`, `dup2`, `exec`.** Do the `open` before the `fork` if the parent needs to detect failure; do it after if the parent must not hold the descriptor.
- **`O_TRUNC` is what makes `>` clobber** and `O_APPEND` is what makes `>>` not. The difference between the two shell operators is one flag.

### The `2>&1` ordering trap

```
$ ls /nope > f 2>&1      # f holds: ls: cannot access '/nope': ...
$ ls /nope 2>&1 > f      # f is EMPTY; the error goes to the terminal
```

Both were run on this machine. **The second is not a typo, and it is not a shell quirk — it is `dup2` semantics.** Redirections are applied left to right:

- `> f 2>&1` — first descriptor 1 becomes the file, *then* descriptor 2 is made a copy of descriptor 1, which is now the file. Both go to the file.
- `2>&1 > f` — first descriptor 2 is made a copy of descriptor 1, **which is still the terminal**, and *then* descriptor 1 is changed to the file. Descriptor 2 keeps pointing at the terminal.

`2>&1` copies **where descriptor 1 points right now**. It does not create a lasting link between 1 and 2. Once you can see the `dup2` calls the shell is making, the rule stops being something you memorise.

---

## 3. Pipes: One Buffer, Two Descriptors, and a Rule About EOF

```c
int fd[2];
pipe(fd);        /* fd[0] = read end, fd[1] = write end */
```

A pipe is a 64 KB kernel buffer (L05 §3) with a descriptor at each end. `fork` after `pipe`, close the ends you do not need, and two processes have a byte stream.

**The EOF rule is the one students lose an afternoon to:**

> `read` on a pipe returns 0 — end of file — **only when every descriptor open on the write end has
> been closed**, in every process.

Forget one and the reader waits forever. Reproduced deliberately, with the parent's copy of the write end left open:

```
$ timeout 5 ./pipeline_bug ls -1 /etc : wc -l
(nothing)                       rc=124 — killed by the timeout
$ ps -o pid,stat,wchan:20,comm -C wc
    PID STAT WCHAN                COMMAND
 415630 S    anon_pipe_read       wc
```

**`wc` is parked in `anon_pipe_read`**, waiting for an EOF that a *different* process is preventing by holding a descriptor it never uses. `wchan` naming the exact kernel function it is blocked in is the fastest diagnosis there is, and it is worth remembering that `ps -o wchan` exists.

**And the mirror image:** writing to a pipe whose read end is closed raises **`SIGPIPE`**, whose default action is to kill your process. Ignore the signal and `write` returns `-1` with `EPIPE` instead. `head` works by closing its input, so `producer | head -1` kills the producer — which is the intended behaviour, and is why a server that writes to disconnected clients must handle `SIGPIPE` (W0 L03 §8) rather than discover it in production.

---

## 4. `FD_CLOEXEC`: What Leaks Into the Program You Just Started

```c
int plain  = open("/etc/hostname", O_RDONLY);
int onexec = open("/etc/hostname", O_RDONLY|O_CLOEXEC);
execv("/proc/self/exe", ...);
```

```
before exec: plain fd=3, O_CLOEXEC fd=4
after exec, the new program's own /proc/self/fd:
  fd 3 -> /etc/hostname
  fd 4 -> /proc/415481/fd        <- the `ls` that printed this, not our file
```

**Descriptor 3 survived into the new program; descriptor 4 was closed by the kernel** — and the
number 4 was then handed straight back out to the next thing that opened something, which is the
lowest-free-descriptor rule of L04 §1 doing its job. Everything else — PID, cwd, mask — survived too (W0 L01 §7); the descriptor table is the part you control per entry.

**Why this is a security control and not tidiness.** A privileged program that opens `/etc/shadow`, then execs a helper, has handed that helper a readable descriptor onto `/etc/shadow` — no permission check applies, because the check happened at `open` time in a process that was allowed. Container runtimes have been escaped through exactly this: a leaked descriptor onto a host directory is a path out of the namespace (Week 11).

**Use `O_CLOEXEC` at every `open`, and `SOCK_CLOEXEC` at every `socket`, unless you specifically intend the descriptor to be inherited.** The `fcntl(fd, F_SETFD, FD_CLOEXEC)` form exists for descriptors you did not open yourself, and it is a second system call plus a race in a threaded program — which is why the flags were added to `open`, `socket`, `pipe2`, `accept4` and `dup3`.

**In Lab 1 you want the opposite**, deliberately: the pipe descriptors must survive into the exec'd stage. That is the case where inheritance is the mechanism rather than the leak, and being able to say which case you are in is the skill.

---

## 5. Non-Blocking I/O and `EAGAIN`

```c
int flags = fcntl(fd, F_GETFL);
fcntl(fd, F_SETFL, flags | O_NONBLOCK);      /* get, modify, set — never just set */
```

With `O_NONBLOCK`, a call that would have waited returns `-1` with **`EAGAIN`** instead:

```
pipe filled after 65536 bytes; next write: errno=11 (EAGAIN)
```

**`EAGAIN` is not an error.** It means *"not now"* — nothing failed, nothing was lost, and the correct response is to do something else and come back. `EWOULDBLOCK` is the same value on Linux; POSIX permits them to differ, so portable code checks both.

**The trap** is the read-modify-write above. `fcntl(fd, F_SETFL, O_NONBLOCK)` — without the `F_GETFL` — clears `O_APPEND` and every other status flag on that open file description, **including for every other process sharing it** (L04 §2). It is a one-line way to break a log file you do not own.

**Non-blocking on its own is a busy-wait**, and a busy-wait is the thing W0's Lab 0 forbade. What makes it useful is being told *when* to come back — `select`, `poll`, `epoll` — which is Week 5, and which is also where you find out that non-blocking sockets are how one thread serves ten thousand clients.

---

## 6. `readv`/`writev`: Fewer Calls for the Same Bytes

An HTTP response is a status line, some headers, and a body — three buffers that are not adjacent in memory. Three `write` calls, or one `writev`:

```c
struct iovec v[3] = { {status, ns}, {headers, nh}, {body, nb} };
writev(fd, v, 3);
```

100,000 responses to `/dev/null`, measured:

| | Time | System calls |
|---|---:|---:|
| three `write`s | 0.32 s | 300,000 |
| one `writev` | **0.10 s** | **100,000** |

**3.2× faster, for the same bytes**, and the reason is L05 §2's 1.25 µs. The alternative — `memcpy` the three pieces into one buffer and issue one `write` — costs a copy of the whole body, which for a large response is worse than the two calls you saved.

**`writev` is also atomic with respect to other writers**, in the same sense a single `write` is. For a log line assembled from several pieces, that is the difference between one line and three interleaved fragments.

---

## 7. What to Take Away

1. **`dup2` copies the descriptor, not the file**, closes the target atomically, and lets you choose the number — which is why redirection is possible at all.
2. **Redirection is `open`, `dup2`, `close`, `exec`**, in the window between `fork` and `exec`.
3. **`2>&1` copies where 1 points at that moment.** Order matters, and the mechanism explains the rule.
4. **A pipe reports EOF only when every write-end descriptor everywhere is closed.** `ps -o wchan` names the function a stuck process is blocked in.
5. **`O_CLOEXEC` by default.** A leaked descriptor is a leaked capability, not a leaked integer.
6. **`EAGAIN` means "not now".** Never set flags without `F_GETFL` first.
7. **`writev` is 3.2× faster than three `write`s** and atomic in the same way one write is.

**Lab 1 is all seven at once:** `pipe`, `fork`, `dup2`, close the right descriptors, `execvp`, and reap. Ninety lines, and it is the machine underneath every shell command you have ever typed.

---

## Exercises

1. Write the four `dup2` calls a shell makes for `cmd < in > out 2>> err`. Which order do they have to be in, and why does one of them need `O_APPEND`?
2. Run `strace -f -e trace=dup2,openat,pipe2 bash -c 'ls | wc -l > n.txt'` and map every line to something in this lecture.
3. In `pipeline.c`, delete one `close()` and predict which stage hangs before running it. Confirm with `ps -o wchan`.
4. Set `O_NONBLOCK` on a pipe's read end with `fcntl(fd, F_SETFL, O_NONBLOCK)`. Now check `F_GETFL` on the *write* end in another process. What did you break?
5. Measure `writev` against `write` for two buffers of 8 bytes and for two of 8 MB. Explain why the ratio is not the same.
6. `dup2(fd, fd)` — what does it return, and what does it do to `FD_CLOEXEC` on `fd`? *(`man 2 dup` is explicit, and the answer surprises people.)*

---

*PROG 201 · Week 1 · L06 · © CSE Department*
