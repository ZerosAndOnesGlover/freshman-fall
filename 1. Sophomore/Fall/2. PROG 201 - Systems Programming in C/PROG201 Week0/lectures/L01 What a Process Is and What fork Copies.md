# PROG 201 · Systems Programming in C
## Week 0 · Lecture 1 of 3
### What a Process Is, and What `fork()` Copies

---

**Reading:** APUE §1.6, §7.3, §8.1–8.3 · **Next:** L02, waiting and the process table

---

## 1. A Process Is Not a Program

A program is a file. A process is **a bundle of kernel bookkeeping**, and the file is only one entry in it.

Everything below is per-process state the kernel maintains. Every line of it is readable, on this machine, right now:

| What the kernel holds | Where you can read it | Course week |
|---|---|---|
| The address space — which virtual pages exist, and what they map to | `/proc/<pid>/maps` | **W4** |
| The file descriptor table — small integers to open file descriptions | `/proc/<pid>/fd/` | **W1** |
| Signal dispositions, the blocked mask, the pending set | `/proc/<pid>/status`, fields `SigBlk`/`SigPnd` | **W0, L03** |
| Credentials — real and effective UID/GID | `/proc/<pid>/status`, `man 7 credentials` | W7, W11 |
| The current directory and root directory | `/proc/<pid>/cwd`, `/proc/<pid>/root` | W7, W11 |
| Parent PID, process group, session, controlling terminal | `/proc/<pid>/stat` fields 4, 5, 6, 7 | **W0, L02** |
| Resource limits and accounting | `/proc/<pid>/limits`, `getrusage(2)` | W9 |
| The exit status, once it has exited and before it is reaped | *nowhere else — only the process table* | **W0, L02** |

**Try it now.** `ls -l /proc/self/fd` in a shell prints the three descriptors every process starts with, plus the one the `ls` needed to read the directory:

```
lrwx------ 0 -> /dev/pts/3
lrwx------ 1 -> /dev/pts/3
lrwx------ 2 -> /dev/pts/3
lr-x------ 3 -> /proc/1234/fd
```

> **This is the course in one table.** Each row is a week: Week 1 is the second row, Week 3 asks what
> happens when two threads share the first row, Week 4 is the first row directly, Week 11 is what
> happens when you give a process *private copies* of rows 5 and 6.

---

## 2. `fork()` Returns Twice

```c
pid_t p = fork();
if (p < 0)  { perror("fork"); exit(1); }   /* failed: no child exists   */
if (p == 0) { /* child  */ }               /* returned 0 in the child   */
else        { /* parent */ }               /* returned the child's PID  */
```

**One call, two returns, in two different processes.** The child is a copy of the caller, continuing from the same instruction, with the same variables holding the same values, differing in the return value of this one call — and in a small, exactly specified list of other things.

The asymmetry in the return value is not decoration. **The parent needs the child's PID** — it is the only handle it will ever get, and it needs it to wait for it (L02) or signal it (L03). The child does not need the parent's, because it can always ask: `getppid()`.

**Three cases, and the third is real.** `fork()` fails with `EAGAIN` when the system or the user has too many processes — `RLIMIT_NPROC` is 25,571 on the lab machines (`ulimit -u`) — and with `ENOMEM` when the kernel cannot allocate the task structures. A `fork()` whose return value you did not check produces a program in which the parent silently *becomes* the worker it thought it delegated to.

---

## 3. What the Child Gets, and What It Does Not

The child is *almost* a copy. The exceptions are the exam questions, and more importantly they are the bugs.

| Inherited by the child | **Not** inherited |
|---|---|
| The whole address space *(copy-on-write — §4)* | Its own new PID, and a new parent PID |
| Open file descriptors — **sharing the file offset** *(W1)* | **Pending signals** — the child's pending set starts empty |
| Signal handlers and the signal mask | **Timers** — `alarm`, `setitimer`, `timer_create` are cleared |
| Current directory, root directory, umask | Record locks (`fcntl`) held by the parent |
| Environment, resource limits, credentials | Accumulated CPU times — reset to zero |
| Attached shared memory, memory mappings | Semaphore adjustments (`semadj`) |

Measured on this machine (`inherit.c`): the parent blocks `SIGUSR1`, raises it so that it is pending, and arms a five-second alarm before forking.

```
parent: SIGUSR1 pending = 1, alarm remaining = 5
child : SIGUSR1 pending = 0, blocked = 1, alarm remaining = 0
```

**The mask crossed; the pending signal and the timer did not.** The child inherits the *rules* about signals and none of the *outstanding* ones. This is deliberate: a pending signal was aimed at a particular process, and duplicating it would deliver it to a process nobody sent it to.

> **The trap in the left-hand column is the second row.** The child does not get a copy of the file
> offset; it shares the *open file description*, offset included. Two processes writing to an
> inherited descriptor advance one shared cursor. This is what makes `ls > out` work after a fork,
> and it is why Week 1 spends a lecture on the three-table picture.

---

## 4. Copy-on-Write, Measured

The child gets "a copy of the address space" — but copying a gigabyte at every `fork()` would make the call unusable, and no Unix has done it since the 1980s.

Instead: **parent and child share every page, all of them marked read-only.** The first *write* to a page traps into the kernel, which allocates a fresh frame, copies the 4 KB, and marks it writable in the faulting process alone. A page nobody writes is never copied.

`cow.c` forks after touching 64 MB — 16,384 pages — and counts the child's minor faults with `getrusage(2)`:

| Child does | Minor faults | Pages copied |
|---|---:|---:|
| Reads every page | **0** | none |
| Writes one byte in every page | **16,384** | all 16,384 |

Exactly one fault per page, and none at all for the reader. That is copy-on-write with no interpretation required.

**And the isolation is real.** The child sets `buf[0] = 'B'`; after `wait()`, the parent still reads `'A'`. Two processes, one physical page until the moment they disagreed.

---

## 5. So `fork()` Is Cheap? No — It Is O(address space)

Copy-on-write does not copy the pages. **It still copies the page tables**, and those are proportional to how much memory the parent has mapped.

`forkcost.c`, 200 iterations of `fork()` + `_exit()` + `waitpid()`, parent resident size varied:

| Parent resident | `fork()` + `wait()` | Per MB |
|---:|---:|---:|
| 1 MB | 0.166 ms | — |
| 64 MB | 2.186 ms | 34 µs |
| 256 MB | 8.473 ms | 33 µs |
| 1024 MB | **35.042 ms** | 34 µs |

**Linear, at about 34 microseconds per megabyte of parent.** A 1 GB process that forks a child to run `/bin/true` spends 35 milliseconds building page tables it is about to throw away, because `exec()` discards the entire address space it just so carefully arranged to share.

This is the classic production failure: a large, healthy server shells out to a small helper and the *fork*, not the helper, becomes the bottleneck. `spawncost.c` measures the three ways to start `/bin/true`:

| Parent resident | `fork` + `exec` | `vfork` + `exec` | `posix_spawn` |
|---:|---:|---:|---:|
| 1 MB | 0.654 ms | 0.582 ms | 0.605 ms |
| 256 MB | 9.249 ms | 0.539 ms | 0.566 ms |
| 1024 MB | **35.492 ms** | **0.497 ms** | **0.504 ms** |

**At 1 GB, `posix_spawn` is seventy times faster than `fork`+`exec`, and at 1 MB it is no faster at all.** The cost that disappears is exactly the cost of the page tables: `vfork` borrows the parent's address space instead of copying it, and `posix_spawn` is a library routine that uses `CLONE_VFORK`/`CLONE_VM` underneath.

> **`vfork` is a loaded gun and `posix_spawn` is the safe version of the same idea.** In the `vfork`
> child the parent is *suspended* and you are running in its address space: touching any variable,
> returning from the calling function, or calling anything but `_exit` and `exec` is undefined
> behaviour. Use `posix_spawn(3)`, which does the dangerous part correctly and takes file-action
> and signal-mask arguments for the things you would have wanted to do between the fork and the
> exec.

**The rule this course wants:** `fork()` when the child is a copy of the parent that keeps running as one (a server accepting a connection, a shell backgrounding a job). `posix_spawn()` when the child is a *different program*, and the parent is large.

---

## 6. The Buffer Trap, and Why It Is Not a Nit

```c
int main(void) {
    printf("hello\n");          /* no fflush */
    if (fork() == 0) exit(0);   /* child inherits a copy of stdio's buffer */
    wait(0);
    return 0;
}
```

Run it two ways on this machine:

```
$ ./buf                 # to a terminal
hello
$ ./buf | cat           # to a pipe
hello
hello
```

**Same binary, same kernel, one `printf`, two lines.** `stdout` is *line*-buffered on a terminal, so `hello\n` was already flushed before the fork; it is *block*-buffered on a pipe, so the string was still sitting in a 4 KB user-space buffer that `fork()` duplicated along with everything else. Two processes then flushed the same bytes at exit.

Change the child's `exit(0)` to `_exit(0)` and the pipe prints `hello` once — because `_exit` does not run the stdio flush.

**What to take from it.** `printf` is not a system call; it is a library that batches. `fork` copies memory, and stdio's buffer is memory. Any output you have not flushed at the moment you fork will be emitted twice. **`fflush(NULL)` before `fork()`** is the fix, and it is the reason the shell you build in Week 6 will be careful about where it prints.

---

## 7. `exec` — Same Process, Different Program

`fork` makes a process. **`exec` replaces the program running inside one.**

```c
execv("/bin/ls", (char *[]){"ls", "-l", NULL});
perror("execv");        /* reached ONLY if exec failed */
_exit(127);
```

There is no "success" path after `execv`. On success, the calling image is gone — there is no code left to return to. **A line after `exec` that is not error handling is a line you have misunderstood.**

`execpid.c` re-executes itself through `/proc/self/exe`:

```
before exec: pid=403263 ppid=403245
after  exec: pid=403263 ppid=403245  (same pid, new program image)
```

**The PID does not change.** The process is the same kernel object; only its contents were swapped. That is why the shell can `fork` then `exec` and still know which PID to wait for — and it is why `exec` without a preceding `fork` is how a program *becomes* another program, which is exactly what `exec` is for in a shell script.

**What survives `exec`:** PID, PPID, process group, session, controlling terminal, cwd, umask, credentials (modulo set-user-ID), resource limits, **open file descriptors that do not have `FD_CLOEXEC` set**, and the **signal mask**.
**What does not:** the address space in its entirety, all threads but the calling one, memory mappings, **and every signal handler** — a caught signal reverts to `SIG_DFL`, because the function that handled it no longer exists. *Ignored* signals stay ignored.

> **`FD_CLOEXEC` is a security control, not an optimisation.** A descriptor you forget to close leaks
> into every program you exec, including ones you did not write. Week 1 opens files with
> `open(..., O_CLOEXEC)` from the very first example, and Week 6's shell depends on knowing exactly
> which three descriptors survive into the child.

---

## 8. The Six Lines That Are the Rest of Unix

```c
pid_t p = fork();
if (p == 0) { execv(prog, argv); _exit(127); }   /* child : become prog */
int st; waitpid(p, &st, 0);                      /* parent: collect it  */
```

Every shell, every `make`, every CI runner, every container runtime is this, plus the descriptor plumbing of Week 1, plus the job control of Week 6. **The separation of `fork` from `exec` is the design decision the whole system is built on**: because there is a moment between them in which the child exists and the new program does not, the parent can arrange the child's descriptors, signals, credentials and namespaces *using ordinary code in the child*, rather than needing an API with a hundred arguments.

Windows made the other choice — `CreateProcess` takes ten parameters and a struct — and it is instructive to compare which of the two you would rather extend.

---

## 9. What to Take Away

1. **A process is kernel state, most of it readable in `/proc`.** The program is one row of it.
2. **`fork` returns twice**, and the value distinguishes parent from child. Check for `-1`.
3. **The child inherits rules, not outstanding events** — mask yes, pending signals no, timers no.
4. **Copy-on-write is exact:** 0 faults for a reader, one fault per page for a writer.
5. **`fork` is linear in the parent's address space** — 34 µs/MB here — and `posix_spawn` is 70× faster for a 1 GB parent that only wants to run another program.
6. **`fflush(NULL)` before you fork.** Buffers are memory, and memory is copied.
7. **Nothing follows a successful `exec`**, and the PID survives it.

---

## Exercises

*(Not assessed. PS 0 is the assessed work; these are five minutes each at a terminal.)*

1. Run `strace -f ./buf | cat 2>&1 | grep write` and find the two `write(1, "hello\n", 6)` calls. Which PID made each?
2. Predict, then measure, the output of a program that calls `fork()` twice in sequence with no `wait`. How many processes exist? Draw the tree.
3. Add `posix_spawn` to `spawncost.c` for a parent of 4 GB. Does the 34 µs/MB line hold?
4. Read `/proc/self/status` and find `SigBlk`, `SigIgn` and `SigCgt`. They are hexadecimal bitmasks; decode which signals your shell is blocking.
5. `execv` a program that does not exist. What is `errno`, and what does your program print if you did not check?

---

*PROG 201 · Week 0 · L01 · © CSE Department*
