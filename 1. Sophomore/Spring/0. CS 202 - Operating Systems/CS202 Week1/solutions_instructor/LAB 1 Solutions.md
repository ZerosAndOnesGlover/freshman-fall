# CS 202 · Lab 1 — Solutions and TA Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Session:** Tuesday of Week 2, 15:00–16:50, BH 210. **Unmarked** — checked off in the session.

**What the session is actually for.** Week 1's lectures stated a dozen facts about the process table. This session makes each of them something the student has *seen*. The three that most students will not believe until they see them, and which the checkoff questions target:

1. **the permission bits on a `/proc` file do not tell you whether you can read it** (Q6),
2. **address space is not memory** (Q3 — and its read-only variant, which surprises everyone),
3. **two xv6 processes share one floating-point register** (Q9).

---

## Timing

| Minutes | Part | TA action |
|---|---|---|
| 0–5 | Setup | Check `$CS202` is set; it is the Lab 0 export |
| 5–25 | A — maps | Students match addresses by eye and give up. Show them `awk` on the hex, or just sort the list |
| 25–40 | B — `rss` | **Insist on the prediction before the run** |
| 40–60 | C — states, hog | `states` takes ~5 s to finish; `hog` 5 s |
| 60–80 | D — PID 1 and `ping` | The `maps` permission denial is the moment of the session. Let them be confused for a minute |
| 80–105 | E — xv6 | The `sed` into `UPROGS` is the usual failure — see Lab 0 solutions |
| 105–110 | Checkoff | |

---

## Answers

### Q1 — the nine addresses

Reference run (`MAPS=1 ./layout`, reference machine; addresses change every run):

| Printed | Line of `maps` it falls in | Perms | Backed by |
|---|---|---|---|
| `main` | `55be1c7f5000-55be1c7f6000` | `r-xp` | `./layout` (text) |
| string literal | `55be1c7f6000-55be1c7f7000` | `r--p` | `./layout` (rodata) |
| initialised global | `55be1c7f8000-55be1c7f9000` | `rw-p` | `./layout` (data) |
| uninitialised global | `55be1c7f8000-55be1c7f9000` | `rw-p` | `./layout` — **bss shares the data page here** |
| `malloc(64)` | `55be4fe01000-55be4fe22000` | `rw-p` | `[heap]` |
| **`malloc(64 MiB)`** | `7e78f51ff000-7e78f9200000` | `rw-p` | **nothing — anonymous mapping** |
| `printf` | `7e78f9228000-7e78f93b0000` | `r-xp` | `libc.so.6` |
| vDSO | `7e78f9598000-7e78f959a000` | `r-xp` | `[vdso]` |
| local variable | `7ffdb6679000-7ffdb669b000` | `rw-p` | `[stack]` |

**The two with no name** — accept either pair a student can defend:

- **The 64 MiB `malloc`**: glibc serves requests above its threshold with `mmap(MAP_ANONYMOUS)`, which has no file and no special name.
- **The uninitialised global** when bss spills past the last file-backed page into an anonymous region — on this binary it did not, so a student who reports bss inside the file-backed `rw-p` page is correct. **Other anonymous lines** in the student's `maps` (glibc's thread-local storage and loader bookkeeping, just below `[vvar]`) are the other acceptable answer.

### Q2 — ASLR

Three normal runs of `main`: `0x5808cd347180`, `0x5f2b88394180`, `0x6335b2e84180`. **The low three hex digits, `180`, never change** — randomisation moves whole pages, and `main`'s offset within its page is fixed by the linker.

Under `setarch -R`: **`0x555555555180`, twice.** `-R` sets the `ADDR_NO_RANDOMIZE` personality flag for that process, disabling ASLR. **A debugger wants it off** so that an address noted in one run — a breakpoint, a watched pointer — still means the same thing in the next; `gdb` does this by default.

### Q3 — `rss`

| After | `VmSize` | `VmRSS` |
|---|---:|---:|
| start | 2,692 kB | 1,428 kB |
| `mmap` 256 MiB | **264,836 kB** | **1,428 kB** |
| touching ¼ … all | 264,836 kB | 67,028 → 263,636 kB |
| `munmap` | 2,692 kB | 1,492 kB |

**The read-only variant** — *predict first*: most students predict RSS rises as with writing. **It does not rise by anything like 256 MiB.** Every read of an untouched anonymous page is satisfied by mapping **the shared zero page** read-only; no new frame is allocated per page. RSS moves by at most a little page-table overhead. The name is **the zero page**; Week 5 has the mechanism, and PROG 201 L01 §4 measured the reader taking 0 faults after a `fork` for the related reason.

*(If a student measures RSS rising for reads, check whether they wrote the loop with `memcmp` or a compiler-visible pattern that GCC turned into a write — or whether transparent huge pages are backing the region. Both are worth ten minutes of conversation.)*

### Q4 — state D

Reference `./states`:

```
what                             pid      state
busy loop                        1491178  R
pause()                          1491179  S
SIGSTOP                          1491180  T
exited, not reaped               1491181  Z
stopped under ptrace             1491182  t
parent waiting in vfork()        1491183  D
this process, reading /proc      1491177  R
```

**The `D` process is a parent suspended inside `vfork()`**, waiting for its child to `exec` or exit. **The child is running in the parent's address space and on the parent's memory** (`man 2 vfork`): the parent must not run — and must not be torn down — while the child is using its memory. If `SIGKILL` destroyed the parent mid-`vfork`, the child would be left executing in a freed address space. So the kernel waits uninterruptibly.

**Accept** "the kernel is waiting for something that must complete and cannot be abandoned half-way" if the student ties it to the shared address space. **Do not accept** "it is waiting for I/O" — that is the classic cause of `D`, but it is not this one.

### Q5 — hog and sleeper

Reference, five seconds on CPU 5:

| | Voluntary | Involuntary |
|---|---:|---:|
| hog | 0 | 4,788 |
| sleeper | 4,748 | 0 |

**Hog**: never blocks, so never switches voluntarily; every switch is a preemption. **Sleeper**: blocks every millisecond, so every switch is voluntary; runs so briefly it is never preempted. **The large numbers are close because most of the hog's preemptions are the sleeper waking up** and being given the CPU.

### Q6 — `/proc/1/maps`

Reference:

```
Name:   systemd
Uid:    0       0       0       0
CapEff: 000001ffffffffff
-r--r--r-- 1 root root 0 ... /proc/1/maps
-r-------- 1 root root 0 ... /proc/1/environ
head: cannot open '/proc/1/maps' for reading: Permission denied
cat: /proc/1/environ: Permission denied
```

**The check is a `ptrace` access-mode check** — `PTRACE_MODE_READ_FSCREDS`, in `man 5 proc`'s words — made **when the file is opened**, not expressed in the mode bits. You may read another process's `maps` only if you could attach a debugger to it: same UID and not more privileged, or `CAP_SYS_PTRACE`. The mode bits say "readable" because `/proc` does not compute per-reader bits.

**Why sensitive:** `maps` gives the **exact load addresses** of the program, its libraries and its stack — which is precisely what ASLR (L06 §2) exists to hide. A user who could read root daemons' `maps` would defeat ASLR for them. **Accept** that answer or "it reveals which files and libraries the process has open"; **require** the point that the permission bits are not the whole check.

### Q7 — `ping`

```
/usr/bin/ping cap_net_raw=ep
CapPrm: 0000000000000000
CapEff: 0000000000000000
```

**Granted `cap_net_raw`; one second later holds nothing.** Between `exec` and the first packet, `ping` opened its socket and **cleared its permitted set**. A capability not in the permitted set can never be raised into the effective set again (without another `exec` of a file that grants it) — so `ping` cannot regain it, even if an attacker takes over its code.

### Q8 — xv6 Ctrl-P

Reference, one CPU, two `spin &`:

```
1 sleep  init 80103f3d 80104ab9 80105a9d 8010584f
2 sleep  sh 8010407c 801002d2 8010107c 80104d69 80104ab9 80105a9d 8010584f
4 runble spin
6 run    spin
```

**One `run`, one `runble`.** Across two listings two seconds apart the *same* PID may be `run` both times — Ctrl-P is handled when the console interrupt arrives, which interrupts whichever `spin` is running, so the listing is biased towards showing that one. Students who see the roles swap are also correct. **There can never be more than one `run` with `CPUS=1`**: one CPU, one running process.

**The hex numbers** are **kernel return addresses on that process's kernel stack** — `procdump` walks the saved frame pointers — showing where in the kernel it is sleeping. Look them up in **`kernel.sym`** or with **`addr2line -e kernel 0x8010407c`**: they resolve to `sleep`, `consoleread`, `fileread`, `sys_read`, `syscall`, `trap` and `alltraps` — the shell asleep in a `read` on the console.

### Q9 — `fpu`

Reference, one CPU, two runs. **Each process should reach `x*2 = 20,000,000`.**

| Run | Parent `x*2` | Child `x*2` | Sum |
|---|---:|---:|---:|
| 1 | 447,636 | 39,552,364 | **40,000,000** |
| 2 | 213,688 | 39,786,312 | **40,000,000** |

Every checkpoint wrong in both processes, both runs. **`x` lived in the x87 register stack**, which is CPU state. **xv6's `swtch` saves four integer registers and nothing of the FPU**, so when the timer switched processes the next one kept adding to the previous one's value. All 40 million half-additions happened, into one register, **so the pair always sums to both correct answers combined.** **The processes share no memory** — the wrong answer is caused by state the kernel did not save.

### Q10 — `fpu` on two CPUs

Reference, `CPUS=2`, one run:

```
child : 0 of 40 checkpoints wrong, final x*2 = 20000000 (expected 20000000)
parent: 1 of 40 checkpoints wrong, final x*2 = 19958711 (expected 20000000)
```

**Not fixed; rarer.** Most of the time the two processes run on different CPUs, and each CPU's x87 holds one process's value, so most checkpoints — and often both final answers — come out right. **Nothing ties a process to a CPU**, so whenever the two share a CPU across a switch, the same corruption happens. Student runs will vary: many will be entirely correct, some will show a checkpoint or two wrong. **Both are the right observation.**

**Why rarer is worse:** a bug that appears every time is found in the first test; a bug that appears once in forty checkpoints, or once in several runs, passes most tests, is dismissed as flaky, and ships. **Accept any answer that makes that point.** The strongest answers add that it will get *worse* again under load — a third FPU-using process on two CPUs guarantees sharing.

---

## Common Problems

| Symptom | Cause | Fix |
|---|---|---|
| `cp: cannot stat '.../CS202 Week1/resources/layout.c'` | `$ACADEMICS` unset in this terminal | `source ~/.bashrc` |
| `layout` prints the maps of `cat`, not itself | wrote `cat /proc/self/maps` in their own version | `self` is whoever opens the file — use the PID |
| `./states` never finishes | killed it early and left a stopped child | `pkill -KILL -f ./states` |
| `ping: socket: Operation not permitted` | on a personal machine without the file capability, or inside a container | skip Q7's measurement; answer from the getcap line |
| xv6: `exec spin failed` | `_spin` not in `UPROGS`, or `fs.img` not rebuilt | `make clean && make qemu-nox CPUS=1` |
| `fpu` prints the right answer, or nearly, in Q9 | booted with two CPUs — that is Q10's experiment, not Q9's | reboot with `CPUS=1` |
| Q10 on "two CPUs" gives the same total corruption as Q9 | the tree lacks Lab 0's second `Makefile` fix, so xv6 is still on one CPU — no `cpu1: starting 1` at boot | apply the second `sed` from Lab 0 Part D and rebuild |
| Ctrl-P does nothing | typed into the host terminal after QEMU exited | it only works at the xv6 prompt |

---

*CS 202 · Week 1 · Lab 1 Solutions · Instructor Only*
