# PROG 201 · Systems Programming in C
## Week 1 · Lecture 1 of 3
### File Descriptors and the Three Tables

*“I think the major good idea in Unix was its clean and simple interface: open, close, read, and write.”* — Ken Thompson, "Unix and Beyond: An Interview with Ken Thompson", *IEEE Computer* (1999)

---

**Reading:** APUE §3.1–3.4, §3.10–3.12 · **Previous:** W0 L03, signals · **Next:** L05, what `read` and `write` cost

**Coursework:** 📊 **Quiz 1** today · 📝 **PS 1** released Wed this week, due Fri of Week 2 17:00 · 📝 **PS 0** due Fri this week 17:00 · 🔬 **Lab 1** Mon of Week 2 15:00–16:50

> **Quiz 1 is at the start of today's lecture.** Ten minutes, covering **Week 0**. The answer key is
> printed in the paper.

---

## 1. The Smallest Interesting Integer in Unix

```c
int fd = open("/etc/hostname", O_RDONLY);
```

`fd` is **3**. Not a pointer, not a handle, not a cookie — the number three. Run it again in a new process and it is three again.

```
$ ls -l /proc/self/fd
lrwx------ 0 -> /dev/pts/1
lrwx------ 1 -> /dev/pts/1
lrwx------ 2 -> /dev/pts/1
lr-x------ 3 -> /proc/415516/fd
```

**A file descriptor is an index into a per-process array.** 0, 1 and 2 are already taken — stdin, stdout, stderr, which your shell opened before it exec'd you — so the first one you get is 3.

**The allocation rule is exactly one sentence, and it is load-bearing:** `open`, `dup`, `pipe`, `socket` and `accept` all return **the lowest-numbered descriptor not currently in use**. That is not an implementation detail; it is specified by POSIX, and the oldest redirection idiom in Unix depends on it:

```c
close(STDIN_FILENO);            /* descriptor 0 is now free      */
open("input.txt", O_RDONLY);    /* ...so this returns 0          */
```

`dup2` (L06) is the modern way to do that, because the version above is a race in a threaded program and silently opens the wrong descriptor if `close` fails. But you will read the idiom in old code, and now you know why it works.

**How many can you have?** `ulimit -n` on this machine is **1,048,576** — a modern default; on older systems it is often 1,024, which is the number the Week 5 C10K discussion assumes you will run into. `RLIMIT_NOFILE` is per-process, and it is the reason a leaked descriptor eventually becomes `EMFILE` and a server that stops accepting connections.

---

## 2. Three Tables, Not One

The descriptor is an index into the first of **three** kernel structures, and almost every confusing thing about Unix I/O is a consequence of the second one existing.

```
  process A                    system-wide                     per-file
  ┌──────────────┐             ┌────────────────────┐          ┌──────────────┐
  │ fd table     │             │ open file          │          │ inode        │
  │              │             │ description        │          │              │
  │ 0 ──────────►│────────────►│  offset            │─────────►│ size         │
  │ 1 ──────────►│──┐          │  status flags      │    ┌────►│ permissions  │
  │ 2 ──────────►│  │          │  (O_APPEND, ...)   │    │     │ timestamps   │
  │ 3 ──────────►│──┼─────────►│  refcount          │────┘     │ block ptrs   │
  └──────────────┘  │          └────────────────────┘          └──────────────┘
                    │          ┌────────────────────┐              ▲
  process B         └─────────►│ another open file  │──────────────┘
  ┌──────────────┐             │ description        │
  │ 3 ──────────►│────────────►│  its OWN offset    │
  └──────────────┘             └────────────────────┘
```

| Table | One per | Holds |
|---|---|---|
| **File descriptor table** | process | the small integers, and `FD_CLOEXEC` for each |
| **Open file description** | `open()` call | **the file offset**, the status flags, a reference count |
| **Inode** | file | size, permissions, timestamps, where the data lives |

**The offset lives in the middle table.** It is not a property of the descriptor and it is not a property of the file. Two descriptors may share one offset or have two, depending entirely on *how they came to exist*, and that is the single most useful thing in this lecture.

| How you got the second descriptor | Same open file description? | Shared offset? |
|---|---|---|
| `dup()` / `dup2()` | **yes** | **yes** |
| inherited across `fork()` | **yes** | **yes** |
| a second `open()` of the same path | no | no |
| passed over a Unix socket (Week 2) | **yes** | **yes** |

---

## 3. The Demonstration

`offsets.c` opens the same file three ways: `a` with `open`, `b` = `dup(a)`, `c` with a second `open`.

```
after open: a=3 b=4 c=5
write 4 on a  ->  off(a)=4 off(b)=4 off(c)=0
write 4 on b  ->  off(a)=8 off(b)=8 off(c)=0
write 4 on c  ->  off(a)=8 off(b)=8 off(c)=4
```

**Writing on `a` moved `b`'s offset and not `c`'s.** `a` and `b` are two indices into one open file description; `c` is a second description onto the same inode.

The file ends up holding:

```
CCCCBBBB
```

`AAAA` was written at offset 0 and then **overwritten by `CCCC`**, because `c` began at 0 and knew nothing about the other two. `BBBB` landed at offset 4 because `b` shared `a`'s advanced offset. Eight bytes of file from twelve bytes of writes, and no error anywhere.

**This is not a contrived hazard.** It is exactly what happens when two processes both open a log file and write to it, and it is why `O_APPEND` exists (L05 §5).

---

## 4. `fork()` Inherits Descriptors — and the Offset With Them

The second half of `offsets.c`:

```c
int d = open("forked.txt", O_RDWR|O_CREAT|O_TRUNC, 0644);
write(d, "parent1", 7);
if (fork() == 0) { write(d, "child!", 6); _exit(0); }
wait(0);
write(d, "parent2", 7);
```

```
forked.txt = parent1child!parent2
```

**Nothing was overwritten.** The child's write advanced an offset the parent shares, so the parent's second write went to byte 13 without either process coordinating. Contrast §3, where two separate `open()`s clobbered each other.

**This is the mechanism that makes shell redirection work.** When you type `(echo a; echo b) > f`, the shell opens `f` once, forks twice, and both children write through the same open file description — so their output concatenates instead of overwriting. The alternative design, where each child has its own offset, would make `>` useless for anything that forks.

> **W0 L01 §3 listed "open file descriptors, sharing the file offset" in the inherited column.** This
> is the payoff of that row. It is also the first of several places this term where "the child gets
> a copy" is *false*: the child gets a copy of the **fd table**, and the entries in the copy point at
> **the same** open file descriptions.

---

## 5. `open()`, and the Flags That Matter

```c
int fd = open(path, flags, mode);
```

**Exactly one** of `O_RDONLY`, `O_WRONLY`, `O_RDWR`, OR-ed with any of:

| Flag | Effect | Note |
|---|---|---|
| `O_CREAT` | Create if absent | **`mode` is required** and is only consulted on creation |
| `O_EXCL` | With `O_CREAT`, fail if it exists | The only atomic "create it if I am first" there is |
| `O_TRUNC` | Truncate to zero length | What `>` does |
| `O_APPEND` | Every write goes to the end, atomically | L05 §5 |
| `O_NONBLOCK` | Never block | L06 §5 |
| `O_CLOEXEC` | Close automatically on `exec` | **Use it by default.** L06 §4 |

**`mode` is not the resulting permissions.** The file gets `mode & ~umask`, and `umask` is inherited from your shell — typically `022`, so `open(..., 0666)` produces a file with mode `0644`. Students discover this when a file they created `0666` refuses to be group-writable, and the answer is never in their code.

**`O_CREAT|O_EXCL` is the whole reason lock files work.** `if (!exists(path)) create(path)` is two system calls with a race between them; `open(path, O_CREAT|O_EXCL, 0600)` is one call that either creates the file or returns `EEXIST`, with no window. **Any time you find yourself testing for existence and then acting, look for the flag that does both at once** — this pattern recurs in Weeks 2, 7 and 11.

---

## 6. `close()`, and Why Its Return Value Is Not Decoration

```c
if (close(fd) < 0) { /* this is not impossible */ }
```

`close` can fail with `EIO`: on some filesystems the error from a write that was buffered in the kernel is not reported until the descriptor is closed. Ignoring it means losing the only notification you will get that the data did not reach the disk. *(`fsync` before `close` is the belt-and-braces version, and Week 7 goes into when you actually need it.)*

**Do not retry a failed `close`.** As W0 L03 §6 said: on Linux the descriptor is released before the error is returned, so a retry closes whatever has since taken that number.

**Descriptor leaks are the failure mode to fear**, because they are silent until they are fatal. A server that leaks one descriptor per request works perfectly for hours and then fails every accept with `EMFILE`. `ls -l /proc/<pid>/fd | wc -l` over time is the diagnosis, and Week 9's tooling automates it.

---

## 7. What to Take Away

1. **A descriptor is an index into a per-process array**, and the kernel always hands you the lowest free one.
2. **Three tables:** descriptor → open file description → inode. **The offset is in the middle one.**
3. `dup` and `fork` share an open file description; a second `open` creates a new one. **Same file, different answer.**
4. `parent1child!parent2` — inherited descriptors share an offset, and that is what makes `>` work across forks.
5. **`open`'s `mode` is masked by `umask`.** `O_CREAT|O_EXCL` is the atomic create.
6. **Check `close`.** Do not retry it. Watch `/proc/<pid>/fd` when a long-running program starts misbehaving.

---

## Exercises

1. Predict the contents of `shared.txt` in `offsets.c` before running it. Then change `dup(a)` to a third `open()` and predict again.
2. Write a program that opens a file and prints its own `/proc/self/fd` listing. Now open it twice more and explain the three numbers.
3. `open("f", O_CREAT|O_WRONLY, 0777)` on this machine produces a file with what permissions? Check `umask`, predict, then run.
4. Two processes each `open()` the same log file and write 10,000 lines. Predict the resulting line count, then measure it. *(You are pre-running L05 §5's experiment; keep your number.)*
5. Read `man 2 open` and find `O_TMPFILE`. What problem does it solve that `O_CREAT|O_EXCL` plus `unlink` does not?

---

*PROG 201 · Week 1 · L04 · © CSE Department*
