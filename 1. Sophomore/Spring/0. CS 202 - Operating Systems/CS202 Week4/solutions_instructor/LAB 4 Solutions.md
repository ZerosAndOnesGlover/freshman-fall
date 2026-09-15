# CS 202 · Lab 4 — Solutions and TA Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Session:** Tuesday of Week 5, 15:00–16:50, BH 210. **Unmarked** — checked off in the session.

**What the session is actually for.** Students have read about the four conditions and the resource-allocation graph. They have never **reconstructed a graph from evidence**. Q2 is the lab: a table filled from `/proc`, with addresses matched to locks and owners to threads, and a cycle drawn from that table alone. **Do not accept a graph drawn from reading the source** — ask the student to point at the line of output each edge came from.

**Midterm 1 marks may be back this week.** Keep the session on the lab.

---

## Timing

| Minutes | Part | TA action |
|---|---|---|
| 0–5 | Setup | Check `~/.gdbinit` — without the debuginfod line, `gdb` stops to ask a question |
| 5–20 | A | Forty runs take ~80 s: the watchdog waits a second each time. Tell them to start it and read B meanwhile |
| 20–45 | B | **The address matching is where students stall.** Do one row on the board |
| 45–70 | C | The `ptrace_scope` refusal surprises everyone. Let it |
| 70–90 | D | The watchdog rewrite is ten lines; offer the structure if someone is stuck after ten minutes |
| 90–110 | Checkoff | `pgrep -x abba` must be empty before they leave |

---

## Answers

All reference figures from the reference machine: i5-8250U, Ubuntu 24.04.4, kernel **7.0.0-31** (Week 4's measurements were retaken after a kernel update; Weeks 0–3 used 7.0.0-30).

### Q1 — rounds before deadlock

| Work | Twenty runs | Median |
|---|---|---:|
| 0 | 400 274 336 32 **0** 687 424 433 216 658 143 531 507 523 110 331 357 30 437 959 | **≈ 378** |
| 1,000 | 18 631 **0** 15 13 2 16 **0** 4 2 1 4 16 12 16 7 11 12 4 1 | **≈ 9** |

**Longer work while holding the first lock widens the window** in which the other thread can take *its* first lock — so the moment when each holds one and wants the other arrives sooner. **0 rounds** means both threads took their first lock before either completed a single round: thread one got A, thread two got B, before either reached its second `lock`.

**Accept** any medians of the same shape — hundreds against ones or tens.

### Q2 — the table

Reference run:

```
  task 10561: state R, wchan 0                syscall 0 0x4 0x640f69b8d710 0x400 ...
  task 10562: state S, wchan futex_do_wait    syscall 202 0x640f5d48f080 0x80 0x2 ...
  task 10563: state S, wchan futex_do_wait    syscall 202 0x640f5d48f040 0x80 0x2 ...
  &A = 0x640f5d48f040, &B = 0x640f5d48f080
  A is owned by TID 10562, B by TID 10563
```

| Task | State | System call | Futex address | Lock | Owns |
|---|---|---|---|---|---|
| 10562 | S | 202, `futex` | `0x640f5d48f080` | **B** | **A** |
| 10563 | S | 202, `futex` | `0x640f5d48f040` | **A** | **B** |

**Wait-for graph: 10562 → 10563 → 10562.** (10562 waits for B, owned by 10563; 10563 waits for A, owned by 10562.)

**The three arguments:**

- `0x640f5d48f080` — **the address of the futex word**, which for a glibc mutex is the start of the `pthread_mutex_t`, so it equals `&B`.
- `0x80` — **the operation**: `FUTEX_WAIT` (0) with `FUTEX_PRIVATE_FLAG` (128) — the futex is private to this process.
- `0x2` — **the expected value**: sleep only if the word still equals 2, **L11 §3's "locked, and someone may be waiting"**.

**Marking cue:** a student who identifies the lock by source line rather than by address has not done the question.

### Q3 — the running thread

**It is the main thread, running the watchdog**: at that instant it is inside `read` (syscall **0**) on file descriptor **4** — reading its own `/proc/self/task/.../syscall` file in order to print the line. It is not part of the deadlock because **it never takes A or B**; it only sleeps a second at a time and reads the counter.

### Q4 — from outside

Reference outside view gives the same two tasks in `S`, `futex_do_wait`, syscall 202 on the two addresses. **What it cannot tell you: which thread owns which lock.** The owners came from glibc's `__data.__owner` field, **read from the process's own memory** — not something `/proc` exposes. From outside you can see that two threads wait on two addresses, and must *infer* the ownership — or use a debugger.

### Q5 — `gdb -p`

```
Could not attach to process.  If your uid matches the uid of the target
process, check the setting of /proc/sys/kernel/yama/ptrace_scope, or try
again as the root user.  For more details, see /etc/sysctl.d/10-ptrace.conf
ptrace: Inappropriate ioctl for device.
1
```

**`ptrace_scope` = 1 permits tracing only descendants.** Without it, any program a user runs — including a compromised one — could attach to every other process of that user and **read its memory**: a browser's session cookies, a password manager's vault. **The shell that runs `gdb -p` is not an ancestor of `abba`**, so the kernel refuses even though the UIDs match.

### Q6 — `gdb`

Reference:

```
  2    Thread 0x7ffff7bff6c0 (LWP 10822) "abba" futex_wait (... futex_word=0x555555558080 <B>)
  3    Thread 0x7ffff73fe6c0 (LWP 10823) "abba" futex_wait (... futex_word=0x555555558040 <A>)
Thread 3: #4 0x000055555555549a in two (arg=0x0) at abba.c:46
Thread 2: #4 0x000055555555541d in one (arg=0x0) at abba.c:32
$1 = 10822        (A's owner)
$2 = 10823        (B's owner)
```

| LWP | Blocked in | Waiting for | Owns |
|---|---|---|---|
| 10822 | `one`, `abba.c:32` | **B** | **A** |
| 10823 | `two`, `abba.c:46` | **A** | **B** |

**Cycle: LWP 10822 holds A, waits for B → B is held by LWP 10823, which waits for A → A is held by 10822.**

**The fix:** in `two`, change the first `pthread_mutex_lock(&B)` to `pthread_mutex_lock(&A)` **and** the second to `pthread_mutex_lock(&B)` — i.e. acquire in the same order as `one`. *(Swapping the unlocks is not required for correctness, but symmetric code is easier to check.)* **Students who say "line 46" have found the blocked call, not the cause** — the ordering is set by *both* lock calls in `two`.

### Q7 — fixed

Reference, 30 seconds each:

```
no deadlock in 30 s: 199254198 rounds; slowest second 5403919 rounds       (work 0)
no deadlock in 30 s: 10787201 rounds; slowest second 355390 rounds        (work 1000)
```

**The change removes circular wait.** **Thirty seconds is not a proof** — Part A's deadlocks came within a few hundred rounds, which is strong evidence, but a test only samples interleavings. **The proof:** every thread acquires A before B. A cycle would need some thread holding B while waiting for A. No thread ever requests A while holding B. So no cycle of waits can exist, and without circular wait there is no deadlock.

### Q8 — `errchk`

```
default mutex, locked twice by one thread:        ETIMEDOUT (after waiting 1 s)
error-checking mutex, locked twice by one thread: EDEADLK (at once)
robust mutex, owner exited while holding it:      EOWNERDEAD
  after pthread_mutex_consistent and unlock, lock returns 0
```

**Neither would have caught `abba`.** An error-checking mutex detects a thread relocking **a mutex it already owns** — it needs only its own owner field. A robust mutex detects **an owner that has died**. `abba`'s cycle needs to know that **the owner of B is itself waiting for A** — information about *another* mutex and *another* thread's wait, which no single mutex records. **That is a graph, and L15 §1's detector is what builds it.**

---

## Common Problems

| Symptom | Cause | Fix |
|---|---|---|
| `gdb` stops with *"Enable debuginfod for this session? (y or [n])"* | no `~/.gdbinit` line | the setup `echo`, or answer `n` |
| Backtraces show `??` instead of `one`/`two` | built with `-O2` or without `-g` | rebuild with `-O0 -g` |
| `print A.__data.__owner` → *"No symbol A in current context"* | stopped in a libc frame with the wrong scope | `frame 4` first, or `print 'abba.c'::A` |
| Ctrl-C in `gdb` does nothing | pressed before the program started | `run 0` first |
| Fixed program still reports a deadlock | watchdog unchanged: it now "detects" nothing because it breaks on the first slow second of a *loaded* machine | report only a second with **zero** progress |
| `abba` processes left behind | Part B's `wait` run not killed | `pkill -x abba` |

---

*CS 202 · Week 4 · Lab 4 Solutions · Instructor Only*
