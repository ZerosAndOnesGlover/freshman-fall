# CS 202 · Operating Systems
## Week 1 · Lecture 1 of 3
### The Process, and What the Kernel Keeps About It

*“We may compare a man in the process of computing a real number to a machine which is only capable of a finite number of conditions q1, q2, ..., qR which will be called "m-configurations".”* — Alan Turing, "On Computable Numbers" (1936)

---

**Sat:** Monday of Week 1, 09:00–09:50, VNC 101, **after Quiz 1** · **Reading:** OSTEP Ch. 4; Love Ch. 3 · **Next:** L05, states and the context switch

**Coursework:** 📊 **Quiz 1** today · 📝 **PS 1** released Wed this week, due Fri of Week 2 17:00 · 📝 **PS 0** due Fri this week 17:00

---

## 1. A Process Is a Record in a Table

PROG 201 L01 said a process is "a bundle of kernel bookkeeping". **This week you read the bookkeeping.** Every operating system keeps, for each process, one record — traditionally called the **process control block**, or PCB — and a table of them.

**xv6's record is `struct proc`, in `proc.h`, and it is 124 bytes.** Every field:

| Field | Bytes | What it holds | Week |
|---|---:|---|---|
| `uint sz` | 4 | size of the user address space | 5 |
| `pde_t *pgdir` | 4 | **the page table** | 5 |
| `char *kstack` | 4 | the bottom of this process's kernel stack | 1 |
| `enum procstate state` | 4 | `UNUSED`, `EMBRYO`, `SLEEPING`, `RUNNABLE`, `RUNNING`, `ZOMBIE` | **1** |
| `int pid` | 4 | the process ID | 1 |
| `struct proc *parent` | 4 | who to notify on exit | 1 |
| `struct trapframe *tf` | 4 | **the user registers**, saved on the kernel stack at the last trap | **0, 1** |
| `struct context *context` | 4 | **the kernel registers**, saved at the last switch | **1** |
| `void *chan` | 4 | what it is sleeping on, if anything | 3 |
| `int killed` | 4 | a pending kill — xv6 has no other signals | 1 |
| `struct file *ofile[16]` | 64 | the open-file table: sixteen descriptors | 7 |
| `struct inode *cwd` | 4 | the current directory | 7 |
| `char name[16]` | 16 | for debugging | — |

*Sizes on the i386 target: the whole structure, compiled, is 124 bytes, and the field widths sum to it.*

**Two rows are the whole of this week.** `tf` points at the registers the process had in user mode when it last entered the kernel — L03 built that trap frame. `context` points at the registers the *kernel* had, for this process, when it last switched away — L05 builds that. **A process that is not running is nothing but these two saved register sets, a page table, and the rest of this table.**

**The table itself is an array of 64** (`NPROC` in `param.h`), each 124 bytes: **7,936 bytes for every process xv6 can ever have.** A 65th `fork` fails.

---

## 2. Linux's Record Is Eighty Times Larger

Linux's PCB is **`struct task_struct`**. Its size depends on how the kernel was configured, so the only honest way to know it is to ask the compiler that built this kernel.

`tsize.c` is a kernel module that is **compiled against the reference machine's own kernel headers and never loaded** — building a module needs no privilege; loading one does. It declares an array of `sizeof(struct task_struct)` bytes, and the object file's symbol table reports how large the compiler made it:

```
$ make && nm -S tsize.o | grep _size
task_struct_size    9920 bytes
mm_struct_size      1728 bytes
files_struct_size    704 bytes
cred_size            184 bytes
thread_struct_size   184 bytes
```

**9,920 bytes per task, against xv6's 124.** Eighty times larger — and still not the whole story, because the task structure mostly holds *pointers* to other structures:

| xv6 `struct proc` has | Linux `task_struct` points to instead | Size here |
|---|---|---:|
| `pgdir` and `sz` | `struct mm_struct` — the address space, its regions, its page table | 1,728 |
| `ofile[16]` | `struct files_struct` — an expandable descriptor table | 704 |
| *(nothing — xv6 has no users)* | `struct cred` — UIDs, GIDs, capabilities, security labels | 184 |
| `context` | `struct thread_struct`, *inside* `task_struct` — saved stack pointer, segment and debug state | 184 |

**The pointers are the design.** Two tasks that point at *the same* `mm_struct` share an address space; two that point at the same `files_struct` share descriptors. §6 is what Linux calls those tasks.

**The rest of the 9,920 bytes** is everything xv6 does not have: scheduler bookkeeping for several scheduling classes (Week 2), signal state, resource limits and accounting, namespace and control-group membership (PROG 201 Week 11), `seccomp` filters (Week 12), tracing and audit hooks, and more. **Every feature Linux has that xv6 does not is, somewhere, a field in this structure.**

---

## 3. `/proc` Is the Table, Made Readable

xv6 prints its table only on request: press **Ctrl-P** at the console and `procdump` lists every slot in use.

```
1 sleep  init 80103f3d 80104ab9 80105a9d 8010584f
2 sleep  sh 8010407c 801002d2 8010107c 80104d69 80104ab9 80105a9d 8010584f
4 runble spin
6 run    spin
```

**PID, state, name, and — for sleeping processes — the kernel return addresses on the stack**, which say *where* in the kernel it is asleep. Two copies of a CPU-burning `spin` on one CPU: one running, one runnable, waiting its turn.

**Linux makes the table a filesystem.** Every process has a directory `/proc/<pid>/` with **57 entries** on the reference machine, each a view of one part of `task_struct` or what it points to. The four this course uses most:

| File | Shows | Used in |
|---|---|---|
| `status` | human-readable summary: state, IDs, credentials, memory, context-switch counts | this lecture, Lab 1, PS 1 |
| `stat` | the same and more, as one line of numbers for programs | PS 1 |
| `maps` | every region of the address space | L06, Lab 1 |
| `fd/` | a symbolic link per open descriptor | PROG 201 |

**`status`, for a `cat` reading its own:**

```
Name:   cat
State:  R (running)
Pid:    1692262
PPid:   1692258
Uid:    1000    1000    1000    1000
Gid:    1000    1000    1000    1000
VmRSS:      1972 kB
Threads:        1
CapEff: 0000000000000000
CapBnd: 000001ffffffffff
voluntary_ctxt_switches:        1
nonvoluntary_ctxt_switches:     0
```

**`stat` is for programs, and has one trap.** Its fields are space-separated, and field 2 is the command name in parentheses — **which may itself contain spaces and parentheses**, because a program can name itself anything. Parse from the *last* `)`:

| Field | Name | Meaning |
|---:|---|---|
| 1 | `pid` | |
| 2 | `comm` | **`(name)` — do not split this on spaces** |
| 3 | `state` | one letter: L05 §1 |
| 4 | `ppid` | |
| 14, 15 | `utime`, `stime` | CPU time in user and kernel mode, **in clock ticks** — 100 per second here (`getconf CLK_TCK`) |
| 20 | `num_threads` | |
| 22 | `starttime` | when it started, in ticks since boot |

> **Nobody else's secrets, though.** `/proc/1/status` is readable by any user — it is a summary.
> `/proc/1/maps` and `/proc/1/environ` are not: they reveal where a process's code is loaded and
> what is in its environment, and the kernel refuses them to anyone who could not also debug
> that process. Lab 1 finds out exactly which files are which.

---

## 4. How Large the Table Can Grow

| Limit | xv6 | Linux, reference machine | Command |
|---|---:|---:|---|
| Process slots | **64**, fixed at compile time | — no fixed table | `NPROC` in `param.h` |
| Largest PID | — | **4,194,304** | `cat /proc/sys/kernel/pid_max` |
| Threads, system-wide | 64 | **51,142**, set at boot in proportion to RAM | `cat /proc/sys/kernel/threads-max` |
| Processes per user | 64 | **25,571** | `ulimit -u` — `RLIMIT_NPROC` |
| In use right now | — | 351 processes, 1,425 threads (L01 §2) | |

**Linux has no fixed-size table because a table of 51,142 × 9,920 bytes would be half a gigabyte** allocated in advance for tasks that mostly do not exist. Task structures are allocated as tasks are created and freed as they are reaped, and found through hash tables and lists. **Each also needs a kernel stack** — 16 KiB on x86-64 — which is why the thread limit is tied to memory.

**xv6 scans its whole 64-slot array** every time it looks for a process: to schedule, to `wait`, to `kill`. With 64 slots that is fast. **Week 2's scheduler is the first place this stops being true.**

---

## 5. Credentials: Who a Process Is Acting For

The `Uid:` line in `status` has **four** numbers, and they are not a repetition:

| Column | Name | Used for |
|---|---|---|
| 1 | **real** UID | who started the process — who to bill, who may signal it |
| 2 | **effective** UID | **who the kernel treats it as** for permission checks |
| 3 | **saved** set-user-ID | an effective UID it may switch back to |
| 4 | **filesystem** UID | who it is for file access (almost always equal to effective) |

**They differ when a program is *set-user-ID*.** On the reference machine:

```
-rwsr-xr-x root /usr/bin/passwd
-rwsr-xr-x root /usr/bin/sudo
```

The `s` in place of the owner's `x` means: **when this file is `exec`ed, set the effective UID to the file's owner.** So `passwd`, started by user 1000, runs with effective UID **0** — which is what lets it rewrite `/etc/shadow`, a file user 1000 cannot even read. Real UID stays 1000, so the program knows whose password to change.

**This is a lot of power for a program that needs to write one file.** A bug in any set-user-ID-root program is a bug running as root.

### Capabilities: root, in 41 pieces

Linux splits root's privilege into **capabilities**, each a single bit. The bounding set on the reference machine, `CapBnd: 000001ffffffffff`, decodes to **41 of them**:

```
$ capsh --decode=000001ffffffffff
cap_chown, cap_dac_override, cap_dac_read_search, cap_fowner, cap_fsetid, cap_kill,
cap_setgid, cap_setuid, ..., cap_net_raw, ..., cap_sys_module, cap_sys_rawio, ...,
cap_sys_admin, ..., cap_bpf, cap_checkpoint_restore
```

**A normal process's effective set, `CapEff`, is all zeros.** Several of the refusals this course has met are single capabilities: loading a module is `cap_sys_module`; `ioperm` in L02 §4 is `cap_sys_rawio`; `bpftrace` refusing to run (Week 7) is `cap_bpf` and `cap_perfmon`.

**`ping` shows how capabilities are meant to be used.** It needs a raw network socket, which traditionally meant being set-user-ID root. On the reference machine it is not:

```
$ ls -l /usr/bin/ping
-rwxr-xr-x root /usr/bin/ping          ← no s bit
$ getcap /usr/bin/ping
/usr/bin/ping cap_net_raw=ep           ← one capability, attached to the file
```

**A file capability grants exactly one piece of root** — `cap_net_raw`, "effective and permitted" — when the file is executed. And then, measured while `ping` was running, 0.7 seconds after it started:

```
CapPrm: 0000000000000000
CapEff: 0000000000000000
```

**Both zero.** `ping` was *granted* `cap_net_raw` at `exec`, opened its socket, and then **dropped the capability from its permitted set** — which cannot be undone — before sending its first packet. A bug in `ping`'s packet parsing, from then on, runs with no privilege at all.

**That is least privilege applied twice**: grant the smallest piece of power, and hold it for the shortest time. Week 12 is built on it. **xv6 has none of this — it has no users** — which is one of the simplifications worth being uneasy about.

---

## 6. Threads Are Tasks That Share

**Linux has no separate thread object.** A thread is a `task_struct` like any other, created by `clone` with flags that make it **share** the creator's `mm_struct`, `files_struct` and signal handlers instead of copying them. A "process", in Linux's own vocabulary, is a *thread group*.

`/proc/<pid>/status` shows both identities:

- `Pid` is the task's own ID — **different for every thread**.
- `Tgid` is the thread group's ID — **the same for every thread of a process**, and what `getpid()` returns.

**Sharing is cheaper than copying.** `spawn.c` creates and destroys 20,000 of each, pinned, best of five:

| Create and destroy | Cost |
|---|---:|
| `pthread_create` + `pthread_join` | **27.6 µs** |
| `fork` + `_exit` + `waitpid`, small parent | **154.3 µs** |

**5.6× — and the difference is what is not copied.** A new thread needs a `task_struct`, a kernel stack and a user stack. A new process also needs a copy of the page tables, the descriptor table and everything else behind those pointers, and then all of it must be torn down again. PROG 201 L01 §5 measured the page-table part growing at 34 µs per megabyte of parent.

**xv6 has no threads**: every `struct proc` has its own `pgdir`. Adding them would mean separating the fields that belong to an address space from the fields that belong to a flow of control — exactly the split Linux makes with its pointers.

---

## 7. What to Take Away

1. **A process, when not running, is a record**: two saved register sets, a page table, open files and bookkeeping. xv6's is 124 bytes; Linux's is 9,920.
2. **Linux's record points to shared structures**, and the sharing is how threads work.
3. **`/proc/<pid>` is the table as files.** Parse `stat` from the last `)`, and read CPU times in clock ticks.
4. **xv6 has a fixed table of 64; Linux has limits instead** — 4,194,304 PIDs, 51,142 threads, 25,571 per user.
5. **Four UIDs**, and set-user-ID changes the effective one at `exec`. **Capabilities split root into 41 bits**, and `ping` holds one of them for less than a second.
6. **A thread is a task that shares**; creating one cost 27.6 µs against 154.3 µs for a process.

---

## Exercises

1. Pick a thread-heavy program on your machine (`ps -eLf | awk '{print $2}' | uniq -c | sort -n | tail -3`). Compare `/proc/<pid>/status` and `/proc/<pid>/task/<tid>/status` for two of its threads. **Which lines differ?**
2. Write a program whose `argv[0]` is `a) b (c`, using `prctl(PR_SET_NAME, …)`, and read its `/proc/self/stat`. Show that splitting on spaces gets `state` wrong, and that parsing from the last `)` does not.
3. Add `struct signal_struct` and `struct sighand_struct` to `tsize.c`. Which of them does a thread share with its creator, and which is per-thread? *(`man 2 clone`, `CLONE_SIGHAND`.)*
4. Run `sudo -l` — do not type your password, just read the prompt. Then `grep Uid /proc/$(pgrep -n sudo)/status` from another terminal while it waits. **Explain all four numbers.**
5. xv6's `struct proc` has `killed` but no pending-signal mask. Where in xv6 is `killed` checked, and what does that mean for how long a killed process can keep running?

---

*CS 202 · Week 1 · L04 · © CSE Department*
