# PROG 201 · Problem Set 1 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**All measurements below are from the reference machine:** Intel i5-8250U, Ubuntu 24.04.4, GCC 13.3.0, glibc 2.39, kernel 7.0. Students' magnitudes will differ; the *shapes* must not.

**What this paper is testing.** Q1 is the first real program of the term and is worth marking generously on structure. Q2 and Q4 are the conceptual core — the three tables, and the difference between one system call and two — and a student who has those two right will survive Week 6. Q3 is calibration. Q5 is a discussion.

---

## Q1: Implement Redirection (28 points)

### Reference solution

```c
/* redirect.c — PS 1 Q1 reference solution.
 *
 *   ./redirect wc -l '<' /etc/services
 *   ./redirect ls /nope '>' both.txt '2>&1'
 *
 * Redirections may appear anywhere and are applied left to right, which is what
 * makes '> f 2>&1' and '2>&1 > f' different.
 */
#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

struct redir { int fd; int flags; const char *path; int dupfrom; };  /* dupfrom >= 0 => 2>&1 */

static void die(const char *what, const char *arg)
{
    fprintf(stderr, "redirect: %s%s%s: %s\n", what, arg ? " " : "", arg ? arg : "", strerror(errno));
    _exit(1);
}

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: %s cmd [args] [< in] [> out] [>> out] [2> err] [2>&1]\n", argv[0]); return 2; }

    char **cmd = calloc(argc + 1, sizeof *cmd);
    struct redir r[16];
    int nc = 0, nr = 0;

    for (int i = 1; i < argc; i++) {
        const char *a = argv[i];
        int need_path = 1, fd, flags, dupfrom = -1;

        if      (!strcmp(a, "<"))    { fd = 0; flags = O_RDONLY; }
        else if (!strcmp(a, ">"))    { fd = 1; flags = O_WRONLY|O_CREAT|O_TRUNC;  }
        else if (!strcmp(a, ">>"))   { fd = 1; flags = O_WRONLY|O_CREAT|O_APPEND; }
        else if (!strcmp(a, "2>"))   { fd = 2; flags = O_WRONLY|O_CREAT|O_TRUNC;  }
        else if (!strcmp(a, "2>&1")) { fd = 2; flags = 0; dupfrom = 1; need_path = 0; }
        else { cmd[nc++] = argv[i]; continue; }

        if (nr == 16) { fprintf(stderr, "redirect: too many redirections\n"); return 2; }
        if (need_path) {
            if (i + 1 >= argc) { fprintf(stderr, "redirect: %s needs a filename\n", a); return 2; }
            r[nr++] = (struct redir){ fd, flags, argv[++i], -1 };
        } else {
            r[nr++] = (struct redir){ fd, 0, NULL, dupfrom };
        }
    }
    if (nc == 0) { fprintf(stderr, "redirect: no command\n"); return 2; }

    fflush(NULL);
    pid_t p = fork();
    if (p < 0) { perror("fork"); return 1; }

    if (p == 0) {
        for (int i = 0; i < nr; i++) {              /* left to right: order is the semantics */
            if (r[i].dupfrom >= 0) {
                if (dup2(r[i].dupfrom, r[i].fd) < 0) die("dup2", NULL);
            } else {
                int fd = open(r[i].path, r[i].flags, 0644);
                if (fd < 0) die(r[i].path, NULL);
                if (dup2(fd, r[i].fd) < 0) die("dup2", r[i].path);
                close(fd);                           /* the spare must not leak into the command */
            }
        }
        execvp(cmd[0], cmd);
        die(cmd[0], NULL);
    }

    int st;
    while (waitpid(p, &st, 0) < 0)
        if (errno != EINTR) { perror("waitpid"); return 1; }
    return WIFEXITED(st) ? WEXITSTATUS(st) : 128 + WTERMSIG(st);
}
```

**Verified output:**

```
$ ./redirect wc -l '<' /etc/services      →  361      (shell agrees: 361)
$ ./redirect echo one '>' o.txt ; ./redirect echo two '>>' o.txt ; cat o.txt
one
two
$ ./redirect ls /nope '2>' e.txt ; echo $?  →  2       (ls's own exit status)
$ ./redirect ls /nope '>' both.txt '2>&1' ; cat both.txt
ls: cannot access '/nope': No such file or directory
$ ./redirect ls /nope '2>&1' '>' b2.txt      →  error on the TERMINAL, b2.txt empty
$ ./redirect sh -c 'kill -9 $$' ; echo $?    →  137
```

### Marking

| Part | Points | Look for |
|---|---:|---|
| (a) parsing anywhere in argv | 4 | Redirection tokens removed from the exec'd `argv`. A solution that only handles trailing redirections gets 2 |
| (a) `<`, `>`, `>>`, `2>` | 6 | `>>` must use **`O_APPEND`**, not `lseek(SEEK_END)`. Deduct 2 for the `lseek` version even though it "works" — Q4 is about exactly why |
| (a) error handling | 3 | Filename **and** `strerror(errno)`, exit 1, no exec |
| (a) exit status | 3 | `WIFEXITED` checked; `128 + WTERMSIG` for the signal case |
| (b) `2>&1` and ordering | 6 | Both orders demonstrated with real output, explained as "dup2 copies where 1 points *now*" |
| (c) descriptors at exec | 6 | The `close(fd)` after each `dup2`. A student who lists it as deliberate has not understood; it is a leak |

**The common wrong answer to (c)** is "0, 1, 2 and the file". The file descriptor from `open` must be closed after the `dup2` — the command already has it as 0, 1 or 2, and leaving the spare open leaks a writable descriptor into a program that did not ask for one (Q5a is the same bug with consequences).

**Also acceptable and worth noting aloud:** a solution that does the `open` in the *parent* before forking, so that a missing input file is reported before a process is created. That is what `bash` does, and it is better than the reference. Award the marks and say so.

---

## Q2: The Three Tables (18 points)

### (a) [8] Measured, all four:

| | Contents | Size |
|---|---|---:|
| **A** — `dup` | `11112222` | 8 |
| **B** — second `open` | `2222` | **4** |
| **C** — across `fork` | `111122223333` | 12 |
| **D** — both `O_APPEND` | `11112222` | 8 |

- **A**: `dup` shares the open file description, so the second write starts at offset 4.
- **B**: two descriptions, two offsets. `b` starts at 0 and **overwrites** `1111`. The file is 4 bytes long: half the data written is gone, with no error.
- **C**: `fork` shares the description exactly as `dup` does. The child's write advances the parent's offset — which is why `>` works across forks.
- **D**: `O_APPEND` moves the seek inside the write, so **the explicit `lseek(b, 0, SEEK_SET)` is discarded**. This is the row students get wrong; many predict `2222` overwriting.

**Marking:** 2 each. Full marks require the *explanation*, not just the string. **B and D are the discriminating rows.**

### (b) [4] The diagram for B

Two fd-table entries → **two** open file descriptions (offsets 4 and 0) → **one** inode. Deduct 2 for a diagram with one open file description; that is answer A.

### (c) [6]

- **If the offset lived in the descriptor:** `dup` and `fork` would give independent offsets, and shell redirection would break — `(echo a; echo b) > f` would have both children writing at 0, and `f` would hold `b`. Every `>` involving a fork would silently lose data.
- **If the offset lived in the inode:** two unrelated programs reading the same file would move *each other's* position. `grep x /etc/passwd` running twice at once would each read half the file. Concurrent readers would be impossible without locking.

**Marking:** 3 each. Accept any concrete consequence; reward examples over restatements.

---

## Q3: What a System Call Costs (20 points)

### (a) [10] Reference table, 64 MB:

| Buffer | Time | Throughput | Syscalls |
|---:|---:|---:|---:|
| 1 B | 167.964 s | 0.4 MB/s | 134,217,728 |
| 16 B | 11.294 s | 5.9 MB/s | 8,388,608 |
| 256 B | 0.854 s | 78.5 MB/s | 524,288 |
| 4 KB | 0.222 s | 303.0 MB/s | 32,768 |
| 64 KB | 0.171 s | 393.4 MB/s | 2,048 |
| 1 MB | 0.168 s | 399.0 MB/s | 128 |

Per-call cost from the 1-byte row: 167.964 s / 134,217,728 ≈ **1.25 µs**. The curve flattens at **4 KB**, one page.

**Marking:** 6 for a complete table with a ~1000× span, 2 for the per-call derivation, 2 for identifying the flattening point. **A student whose 1-byte row is missing because "it took too long" should be given the marks if they say so and extrapolate** — that is the correct engineering response, and it is also the correct answer to the question.

### (b) [5] Under `strace -c`, system time dominates and total wall time rises by an order of magnitude, because `strace` adds two context switches per call. **The point to draw out:** `strace -c` is for *counting* calls, never for timing them. A student who reports a slowdown and concludes the syscalls got slower has misread their tool.

### (c) [5] `cp` does not read the data into user space at all:

```
$ strace -c -f cp in.bin out1.bin
 96.08  0.045216  22608  2  copy_file_range
```

**Two `copy_file_range` calls for 64 MB.** The copy happens inside the kernel — on a filesystem that supports it, possibly with no data movement at all (reflinks). `cat > out` is the 4 KB loop with an extra process. Accept `sendfile`, `copy_file_range` or `mmap` as the answer depending on the coreutils build; require them to have run `strace`.

---

## Q4: Two System Calls Are Not One (20 points)

### (a) [10] Reference, 4 workers × 20,000 lines:

```
lseek(END)+write : 4,396 lines survived of 80,000        (985,330 of 2,960,000 bytes)
O_APPEND         : 80,000 lines survived of 80,000       (2,960,000 bytes — exact)
```

**Loss at *N* = 1 is zero**, because there is no second process to interleave between the `lseek` and the `write`. Loss rises steeply with *N* and then saturates — with more writers, almost every write lands on an offset another worker is also about to use.

**Marking:** 5 for both columns at several *N*, 3 for explaining the window between the two calls, 2 for the *N* = 1 answer. **A student who reports no loss at any *N* has almost certainly made the workers share one descriptor** — that is part (b), and they should be told to look at which process called `open`.

### (b) [4] With one inherited descriptor there is **no loss at any *N***: one open file description, one offset, and `write` advances it atomically. The `lseek` is redundant rather than dangerous.

**This is the pair of results that makes the point.** Same code, same flag, opposite outcome, and the only difference is *where `open` was called*. Marking: 4, of which 2 for the correct prediction stated in advance.

### (c) [6] Two of:

| Pattern | The fused version | The race without it |
|---|---|---|
| `stat` then `open` to create | **`O_CREAT\|O_EXCL`** | Two processes both find the file absent and both create it; one wins, silently |
| `lseek(SEEK_END)` then `write` | **`O_APPEND`** | (a) — 95% data loss |
| `open` then `fcntl(FD_CLOEXEC)` | **`O_CLOEXEC`** | A fork between them leaks the descriptor into an exec'd child |
| `F_GETFL` then `F_SETFL` | *(no fused form — this one genuinely needs care)* | Another process changes flags in between |
| `dup` after `close(1)` | **`dup2`** | A signal handler or thread opens something and takes descriptor 1 |

**Marking:** 3 each for two of the first four rows, with the race stated. The last row is worth a bonus mention — it is L04 §1's old idiom.

---

## Q5: A Descriptor Is a Capability (14 points)

### (a) [6]

The descriptor onto `/etc/shadow` survives `exec` because it was not marked `FD_CLOEXEC`. `less` inherits it as, say, descriptor 3; the user types `!sh`, and the subshell inherits it again; `cat <&3` prints the file. **No permission check occurs, because the check happened at `open()` time in a process that was root.** A descriptor is not a name — it is an already-granted, already-checked right to the object.

**Fix:** `O_CLOEXEC` on the `open`.

**Marking:** 3 for "the check happened at open time", 3 for the fix. A student who says "less shouldn't allow subshells" has answered a different question: 1.

### (b) [4] `F_SETFL` **replaces** the status flags on the open file description, which is shared by every descriptor produced by `dup` or `fork` from that one — including in other processes, if the descriptor came from your shell. Setting `O_NONBLOCK` alone clears `O_APPEND`, and the shell's log file starts being overwritten from position 0.

Correct form: `int fl = fcntl(fd, F_GETFL); fcntl(fd, F_SETFL, fl | O_NONBLOCK);`

### (c) [4] Open question. A strong answer notes that closed-by-default would make Lab 1 impossible in its current shape — the pipe descriptors *must* survive `exec`, so the shell would need an explicit "keep this one" call between `fork` and `exec`, which is precisely what `posix_spawn`'s `file_actions` is. It would also have prevented an entire class of container escapes. The honest summary: **the default is wrong for security and right for the shell**, and modern practice (`O_CLOEXEC` everywhere, opt into inheritance) is the industry quietly reversing it one flag at a time.

**Marking:** 4 for an argument that engages both sides. Do not reward a conclusion.

---

## Marking Summary

| Q | Points | The one thing to look for |
|---|---:|---|
| 1 | 28 | `close()` after `dup2`, and `O_APPEND` for `>>` |
| 2 | 18 | Row B losing half the data; row D discarding the `lseek` |
| 3 | 20 | ~1.25 µs per call, flattening at one page |
| 4 | 20 | Same code, opposite result, depending on who called `open` |
| 5 | 14 | "The check happened at open time" |
| | **100** | |

**Expected median 68–74** — lower than PS 0, mostly on Q1's descriptor hygiene. **If Q2(a) row D is widely missed, spend five minutes on it in Week 2's Tuesday lecture**: `O_APPEND` overriding an explicit seek is the mechanism the whole logging world depends on, and Week 12's daemon assumes it.

---

*PROG 201 · Week 1 · PS 1 Solutions · Instructor Only · © CSE Department*
