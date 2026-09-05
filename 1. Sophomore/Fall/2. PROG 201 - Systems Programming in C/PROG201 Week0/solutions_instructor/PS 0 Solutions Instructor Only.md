# PROG 201 · Problem Set 0 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for PS 0.** This is the first paper of the course and the first time most of the class has written a system call by hand. **Mark the reasoning, not the polish.** A student who predicts wrongly, runs it, and explains the gap correctly has done exactly what §"Two Habits" asks of them and should get full marks; a student who reports the right number with no evidence of having run anything should not.

**Every measured answer below was produced on the reference machine:** Intel i5-8250U, Ubuntu 24.04, GCC 13.3.0, glibc 2.39, kernel 7.0. Student numbers will differ in magnitude and must not differ in shape.

---

## Q1: Reading `fork()` (20 points)

### (a) [4] Eight processes.

```
                  P0
        ┌─────────┼─────────┐
      fork#1    (P0 cont.)
        │
       P1 ────┐
              │
   after fork#2:  P0 P1 P2 P3
   after fork#3:  P0 P1 P2 P3 P4 P5 P6 P7
```

Each `fork()` doubles the population: 1 → 2 → 4 → **8**.

**Marking:** 2 for the number, 2 for a tree that shows the doubling. A tree with 8 leaves hanging off one root is *wrong* — the children fork too, and that is the point.

### (b) [6] One `x` on a terminal, **eight** through a pipe.

```
$ ./q1b            →  x                        (1)
$ ./q1b | cat      →  x x x x x x x x          (8)
```

`stdout` to a terminal is **line-buffered**: `printf("x\n")` flushes at the newline, before any fork happens, so the buffer is empty when the address space is copied. To a pipe it is **block-buffered** (4096 bytes): the string is still in user-space memory at fork time, gets copied into all eight address spaces, and all eight flush it at `exit`.

**The fix is one line:** `fflush(stdout);` immediately before the first `fork()`. `setvbuf(stdout, NULL, _IONBF, 0)` also works and is worse — it makes every `printf` a system call.

**Marking:** 2 for the two counts, 3 for naming line- vs block-buffering as the mechanism *and* locating the copy at `fork`, 1 for the fix. **Do not accept "the terminal is faster" or "the pipe duplicates output"** — the pipe does nothing; the buffer was duplicated before the pipe ever saw a byte.

### (c) [4] Two lines, in either order.

```
404501: fork returned 404502
404502: fork returned 0
```

**The order is not guaranteed.** Which of the two runs first is entirely up to the scheduler, and on a multi-core machine they may genuinely be simultaneous. Students who ran it twenty times and always saw the parent first should be told that consistency here is a property of *this* scheduler under *this* load, not of the API.

**Marking:** 2 for correct content of both lines (in particular: the child's `fork()` returned 0, and the child's PID equals the parent's printed value), 2 for "not guaranteed" with a reason.

### (d) [6] Two defects.

**Defect 1 — `fork()`'s return value is not checked.** If `fork()` fails it returns `-1`, and `waitpid(-1, &status, 0)` then means *"wait for any child"*. In a program with other children this silently reaps and reports the wrong one; in a program with none it returns `ECHILD` and `log_result` is called with an uninitialised `status`.

**Defect 2 — nothing follows the failed `execv`.** This is the interesting one. If `/usr/bin/helper` does not exist, `execv` returns, the `if` block ends, and **the child falls into the parent's code**: it calls `waitpid`, gets `ECHILD`, calls `log_result`, and returns from `main`. There are now two processes running the parent's logic, and the log gains an entry from a process that was supposed to be a helper.

**Fix:**

```c
pid_t p = fork();
if (p < 0) { perror("fork"); return -1; }
if (p == 0) {
    execv("/usr/bin/helper", argv);
    perror("execv");
    _exit(127);                    /* 127: "command not found", as a shell reports it */
}
```

`_exit`, not `exit` — the child must not run the parent's `atexit` handlers or flush the parent's stdio buffers (see (b)).

**Marking:** 3 each. Award the second only if the student says *the child continues into the parent's code*; "exec might fail" alone is 1. Bonus-worthy but not required: noticing `_exit` vs `exit`.

---

## Q2: The Status Word (18 points)

### (a) [6]

| Raw | How it ended | Value |
|---|---|---|
| `0x0000` | exited normally | `WEXITSTATUS` = 0 |
| `0x0100` | exited normally | `WEXITSTATUS` = 1 |
| `0xff00` | exited normally | `WEXITSTATUS` = 255 |
| `0x0006` | killed by a signal | `WTERMSIG` = 6 (`SIGABRT`), no core |
| `0x0086` | killed by a signal | `WTERMSIG` = 6, **core dumped** (bit 7) |

The layout: **high byte = exit status; low 7 bits = terminating signal; bit 7 = core flag.** A normal exit has a zero low byte, which is what `WIFEXITED` tests.

**Marking:** 1 each for the first four rows, 2 for `0x0086` — the core bit is the one they have to derive rather than recall.

### (b) [4] The child was killed, not exited.

For `status == 0x0006`, `WEXITSTATUS(status)` evaluates `(status >> 8) & 0xff` = **0**. The program prints `child returned 0` — *success* — for a child that died of `SIGABRT`. **A crashed child reported as a clean exit** is the worst failure mode this encoding can produce, and it is one `if` away.

**Marking:** 2 for the scenario, 2 for the specific value 0 and why it is dangerous.

### (c) [4] Eight bits, and the reason is the encoding.

`_exit(256)` = `0x100`; only the low 8 bits reach the parent, and `0x100 & 0xff` = 0. The largest usefully distinguishable status is **255**, because the high byte of the 16-bit status word is all the space there is — the low byte is already spoken for by the signal number and the core flag.

**Marking:** 2 for the truncation, 2 for locating the limit in the layout rather than asserting "it's a byte".

### (d) [4] The shell does the arithmetic.

The kernel hands the shell `0x0009` — `WIFSIGNALED` true, `WTERMSIG` 9. **`$?` is a single byte**, so the shell has to compress "killed by signal 9" and "exited with 9" into one number, and the convention it uses is `128 + signal`. Hence 137. Nothing in the kernel ever computes 137.

The consequence worth stating: `$?` **cannot** distinguish a program that was killed by signal 9 from one that exited with status 137. Your own code can, because it has the whole status word.

**Marking:** 2 for "the shell", 2 for justifying it from the raw value. The consequence is a bonus.

---

## Q3: Zombies, Orphans, and the Process Table (22 points)

### (a) [6]

```
    PID    PPID STAT   RSS    VSZ COMMAND
 402541  402540 Z        0      0 zombies
 402542  402540 Z        0      0 zombies
 402543  402540 Z        0      0 zombies
```

**`RSS` 0 and `VSZ` 0**: the address space is gone — pages freed, mappings torn down, descriptors closed — at `exit`, long before the reap. What is still held is a `task_struct` carrying the PID, the exit status and the accumulated `rusage`, plus the PID's slot in the table.

**Marking:** 2 for the output, 2 for "no address space", 2 for naming what *is* retained. A student who says "the zombie is still using memory" has missed the whole point: award 1.

### (b) [5]

`/proc/<pid>` disappears the moment the reap completes.

The kernel cannot discard the status at `exit` because **the parent may not have asked for it yet**, and the exit status has exactly one legitimate reader. Discarding it would make `wait()` unreliable in precisely the situation it exists for — a parent that was busy when the child finished. The zombie is the state in which the process is dead but its answer is not yet collected.

**Marking:** 3 for the argument, 2 for the `/proc` evidence. Accept any phrasing of "the status must outlive the process because its reader is asynchronous".

### (c) [5] The measured answer here is **not** PID 1.

```
child 402584: ppid after parent exit = 257510
$ ps -o pid,comm= -p 257510        →  257510 systemd
$ tr '\0' ' ' < /proc/257510/cmdline  →  /usr/lib/systemd/systemd --user
```

The mechanism is **`prctl(PR_SET_CHILD_SUBREAPER, 1)`**. A process that sets it collects orphans from anywhere in its own subtree; only when no subreaper exists does the orphan reach `init`. `systemd --user` sets it for the login session.

Students on a machine with no user manager (a container, a minimal VM, WSL without systemd) will legitimately get 1. **Both answers are correct; only an unexamined answer is wrong.**

**Marking:** 2 for reporting and identifying the PID, 3 for the mechanism. Accept "subreaper" without the exact `prctl` spelling.

### (d) [6]

- *N* = **25,571** on the reference machine (`ulimit -u`).
- `fork()` fails with **`EAGAIN`** at that many *live-or-zombie* processes for the UID.
- **Every process owned by that real UID is affected**, not just the server: `RLIMIT_NPROC` is a limit on the number of processes for a **real user ID**, so the user's shell, editor and everything else stop being able to fork too. This is why the classic symptom is "the machine is idle and nothing will start".
- Fixes: **(i)** reap with `waitpid(-1, &st, WNOHANG)` in a loop from a `SIGCHLD` handler — the real fix; **(ii)** `signal(SIGCHLD, SIG_IGN)`, which makes the kernel auto-reap — cheaper, and it costs you **every child's exit status, permanently**; `wait()` afterwards returns `-1`/`ECHILD`.

**Marking:** 1 for *N*, 1 for `EAGAIN`, 2 for the scope of the limit (this is the part students get wrong — they say "the server"), 2 for both fixes with the cost stated.

---

## Q4: Signals Do Not Queue (22 points)

### (a) [8]

| *N* sent | `SIGUSR1` handler runs | `SIGRTMIN` handler runs |
|---:|---:|---:|
| 10 | **1** | 10 |
| 1,000 | **1** | 1,000 |
| 20,000 | **1** | 20,000 |
| *(40,000)* | *1* | ***25,571*** |

**Standard signals carry one pending bit per signal number.** With the signal blocked, the second and every subsequent `kill()` finds the bit already set and does nothing; on unblocking, the handler runs **once**.

**Real-time signals queue**, up to `RLIMIT_SIGPENDING` — 25,571 here (`ulimit -i`). Past that the excess is dropped, **and `kill()` still returns 0 for every one of them**: on the reference machine all 40,000 calls reported success and 14,429 signals never existed.

*(The 40,000 row is not required by the question. Students who found the ceiling on their own deserve the credit under (a)'s "explain any point at which the real-time column stops matching *N*".)*

**Marking:** 3 for the `SIGUSR1` column being 1 everywhere, 3 for the `SIGRTMIN` column tracking *N*, 2 for identifying the ceiling and naming `RLIMIT_SIGPENDING`. A student whose real-time column tops out at their own `ulimit -i` has done the question perfectly regardless of the value.

> **Common wrong result to look for:** a student who forgot to *block* the signal first will see numbers
> like 50% and 76% (the `coalesce.c` figures from L03 §3) rather than 1 and *N*. That is a real
> measurement of a different thing, and it is worth 5 of the 8 if they explain what they measured.

### (b) [4]

`static volatile sig_atomic_t`.

- **`sig_atomic_t`** is the only integer type the standard guarantees can be read and written in one indivisible step with respect to signal delivery — so the main loop can never see a half-written value.
- **`volatile`** forbids the compiler from caching the variable in a register or eliding reloads. Without it, `while (!flag) ;` is legally compiled to `if (!flag) for(;;);` — the compiler can prove nothing in the loop changes `flag`, and a signal handler is invisible to that analysis.

**Neither makes it thread-safe.** `sig_atomic_t` says nothing about other threads (Week 3), and students should be warned off using it as a lock-free counter.

**Marking:** 2 each. The `volatile` mark requires them to say what the compiler would otherwise do.

### (c) [6] Four defects.

```c
void on_sigchld(int sig)
{
    int status;
    pid_t p = waitpid(-1, &status, 0);
    printf("child %d exited with %d\n", p, WEXITSTATUS(status));
}
```

1. **Reaps exactly one child, and blocks while doing it.** `SIGCHLD` does not queue, so one delivery can mean five deaths; the other four become zombies. And with no `WNOHANG`, a spurious delivery blocks the handler — and therefore the whole program — until some child happens to die. *Symptom: zombies under load, and mysterious hangs.*
2. **`printf` is not async-signal-safe.** *Symptom: corrupted output, and — rarely, non-reproducibly — a deadlock in stdio's locks. See L03 §4.*
3. **`errno` is clobbered.** `waitpid` sets `errno` on failure; the interrupted main program then reads an error it never caused. *Symptom: a completely unrelated part of the program reporting a failure that did not happen.*
4. **`WEXITSTATUS` without `WIFEXITED`.** A child killed by a signal reports status 0 — "exited with 0" for a crash (Q2b).

**The rewrite:**

```c
static void on_sigchld(int sig)
{
    (void) sig;
    int saved = errno;
    int st;
    pid_t p;
    while ((p = waitpid(-1, &st, WNOHANG)) > 0)
        child_died = 1;          /* record; let the main loop print */
    errno = saved;
}
```

**Marking:** 1.5 each. Accept a rewrite that sets a flag *or* one that writes with `write(2)`; do not accept one that keeps `printf`.

### (d) [4]

`write` is a thin wrapper around a system call: it has no user-space state, so re-entering it midway is harmless — the kernel serialises. `fwrite` maintains a `FILE` buffer, a position and a lock in **user space**; a handler that re-enters it finds those half-updated, and either corrupts the buffer or deadlocks on a lock the interrupted code already holds.

**Why "usually works" is worse:** it converts a deterministic bug into a probabilistic one. It passes review, passes tests, passes staging, and fails on the one production run where the interruption lands inside the window — with corrupted output rather than a crash, so the failure is discovered long after and far away. L03 §4's `malloc` experiment is the demonstration: 1.49 billion allocations, ~100,000 signals, **no failure at all**, and the code is still undefined behaviour.

**Marking:** 2 for the user-space-state distinction, 2 for the argument about intermittency. Students who merely say "it's on the POSIX list" get 1.

---

## Q5: What the `fork`/`exec` Split Costs and Buys (18 points)

### (a) [6]

| Parent resident | `fork` + `wait` | per MB |
|---:|---:|---:|
| 1 MB | 0.166 ms | — |
| 64 MB | 2.186 ms | 34 µs |
| 256 MB | 8.473 ms | 33 µs |
| 1024 MB | 35.042 ms | 34 µs |

**What is copied is the page tables**, not the pages. A 1 GB mapping needs 262,144 PTEs — 2 MB of page-table memory at 8 bytes each — and every one of them must be walked, copied, and marked read-only in both processes. Copy-on-write eliminates the 1 GB of copying and leaves the 2 MB of bookkeeping, which is why the cost is linear in *how much is mapped* rather than in *how much is touched afterwards*.

**Marking:** 3 for a table with a roughly constant per-MB column (any per-MB value is fine; the *linearity* is the result), 3 for identifying page tables. "The kernel copies the memory" is wrong and costs all three — the previous question in L01 §4 measured zero faults for a reader.

### (b) [6]

| Parent resident | `fork`+`exec` | `posix_spawn` |
|---:|---:|---:|
| 1 MB | 0.654 ms | 0.605 ms |
| 256 MB | 9.249 ms | 0.566 ms |
| 1024 MB | 35.492 ms | 0.504 ms |

The factor passes two at around **64 MB** and reaches **70×** at 1 GB. The saved work is exactly the page-table copy: `posix_spawn` uses `CLONE_VM|CLONE_VFORK` underneath, so the child borrows the parent's address space until `exec` replaces it, and no page tables are duplicated to be thrown away microseconds later.

**Marking:** 3 for the table, 3 for identifying the saved work. Accept any crossing point between 16 MB and 128 MB — it depends on the machine.

### (c) [6] Open question; mark the argument.

A strong answer notices that the four operations are **arbitrary code running in the child's context**, and that a `spawn` API can only support the combinations its designers enumerated. `posix_spawn` proves the point: it has a `file_actions` object (open/close/dup2 only), an `attr` object (process group, signal mask, scheduling), and **no** way to change directory — which is why glibc had to add `posix_spawn_file_actions_addchdir_np`, a non-standard extension, in 2.29. Every gap in such an API becomes a new function.

The `fork`/`exec` design says instead: *here is a window in which you may run any code you like*, and gets unlimited configurability from a primitive with zero configuration parameters.

The cost is what (a) and (b) measured, plus a second one worth credit: **`fork` composes badly with threads.** Only the calling thread survives into the child, so any lock held by another thread at fork time is held forever in the child — which is precisely why `posix_spawn` exists.

For a runtime that must also target Windows, a `spawn`-shaped abstraction is the defensible choice, because Windows has no `fork` and emulating one is expensive and lossy; the answer should acknowledge that this trades configurability for portability, and that the escape hatch is a helper program.

**Marking:** 6 for a coherent argument that engages with configurability *and* cost. 4 if only one side. **Do not reward the "right" conclusion** — there isn't one; reward evidence of having thought about what an API with a hundred flags would look like.

---

## Marking Summary

| Q | Points | The one thing to look for |
|---|---:|---|
| 1 | 20 | The child falling through a failed `exec` into the parent's code |
| 2 | 18 | `WEXITSTATUS` on a killed child prints 0 |
| 3 | 22 | `RLIMIT_NPROC` is per-**user**, not per-process |
| 4 | 22 | The blocked-then-unblocked experiment giving 1, not *N* |
| 5 | 18 | Page tables, not pages |
| | **100** | |

**Expected distribution.** This paper is deliberately gentler than PS 1 onwards: it is the diagnostic. Median around 72–78. **If Q3(d) and Q4(a) are widely missed, spend ten minutes of Week 1's Tuesday lecture on them** — they are load-bearing for Lab 0 and for the Week 6 shell, and every later week assumes them.

---

*PROG 201 · Week 0 · PS 0 Solutions · Instructor Only · © CSE Department*
