# CS 202 Scheduling Notes

What had to be decided before CS 202 could be written, and why each decision went the way it did.
Written 2026-09-11, while building Week 0. **The authority** is
`5. Academic Registry/1. Scheduling/Year2 - Sophomore/CSE_Year2_Sophomore_Curriculum.docx`, and
where the registry's own scheduling files settle a question, they do.

---

## 1. The lab lags a week, and — unlike PROG 201's — every slot exists

[[Year2 - Sophomore/ROOM ASSIGNMENTS|ROOM ASSIGNMENTS]] puts CS 202's lectures on **Mon/Wed/Fri
09:00–09:50 in VNC 101** and its lab on **Tue 15:00–16:50 in BH 210**. A Tuesday lab has only
Monday's lecture behind it, so a lab covering Week *N* cannot be sat in Week *N*.

**Lab *N* covers Week *N* and is sat on the Tuesday of Week *N+1*** — exactly CS 201's shape in the
Fall, for the same reason, in the same room.

**The slots count out without a make-up**, which PROG 201's could not:

| Sitting | Which lab |
|---|---|
| Friday of Week 0 | Lab 0 |
| Tuesdays of Weeks 2–12 (11 Tuesdays) | Labs 1–11 |
| Tuesday of the completion period | Lab 12 (demo day) |

**Spring Break (Mon Mar 16) falls between Weeks 7 and 8**, not inside a teaching week, so it removes
no Tuesday. Thirteen labs, thirteen slots.

**Two labs sit the day after a midterm** — Lab 3 on the Tuesday of Week 4 and Lab 7 on the Tuesday
of Week 8 — because both midterms are Mondays. Lab 7 is also the first week back from Spring Break.
Nothing is moved; the syllabus's lab table names both, and the two lab sheets should be written for
that slot when those weeks are built.

---

## 2. Week 0 has six lecture slots for three lectures, and the registry contradicts itself about which

[[Year2 - Sophomore/ASSESSMENT CALENDAR|ASSESSMENT CALENDAR]]'s Week-0 note says two things that
cannot both be true of Spring:

- *"Classes begin on a Wednesday, and Week 1 … begins the second Monday after."*
- *"Week 0 therefore spans … Jan 12 to Jan 23 in Spring."*

**Jan 12 is a Monday**, and [[ACADEMIC CALENDAR]] lists *"Mon Jan 12 — Spring semester begins
(Week 0)"*. In the Fall the two statements agree (Wed Aug 27 to Fri Sep 5); in the Spring they are
two days apart.

**CS 202's Week 0 lectures are the first Wednesday, first Friday and second Wednesday** — Jan 14,
Jan 16 and Jan 21. This satisfies both readings: it starts on a Wednesday, as the general rule says,
and lies inside Jan 12–23, as the date range says. **Nothing in the registry was edited**; the
contradiction is recorded here for whoever reconciles the Spring calendar.

**Two further reasons the Mondays were not used:**

| Monday | Why not |
|---|---|
| Jan 12 | The semester's opening day. With the Wednesday reading of the rule, no classes meet |
| **Jan 19** | **The third Monday in January — Martin Luther King Jr. Day.** Year 1's calendar records public holidays inside teaching weeks as an *open decision*; Year 2's calendar does not mention this one at all. CS 202 needs only three of its six slots, so it does not have to decide the question, and does not |

**The second Wednesday was chosen over the second Friday for L03** so that PS 0, which covers the
trap mechanism, is released after the lecture that teaches it. That leaves the closing Friday's 09:00
slot unused, directly before Lab 0.

---

## 3. Lab 0 is on Friday morning, and the afternoon is left for PROG 202

Every Year 2 course holds its Week 0 lab on the Friday that closes Week 0. That Friday afternoon
already holds, for every Spring Year 2 student:

| Time | What | Where |
|---|---|---|
| 13:00–14:15 | ECE 211 lecture | MEC 101 |
| 15:00–15:50 | CS 290 seminar | TH 105 |

**Lab 0 is 10:00–11:50 in BH 210.** Friday 10:00–12:00 is free for every Spring Year 2 course — CS 212
lectures Tue/Wed/Thu, PROG 202 Tue/Thu, MATH 251 Mon/Tue/Thu — and it ends before the protected lunch
hour. **BH 210 has no Friday booking in either term**: ROOM ASSIGNMENTS gives it to CS 201's Fall
Tuesday lab and CS 202's Spring Tuesday lab and nothing else.

> **Recorded for PROG 202, not decided for it.** PROG 202 also holds a Week 0 lab on this Friday, and
> a student takes both. With CS 202 in the morning, **16:00–17:50** — after the CS 290 seminar — is
> the first afternoon window that clears everything. PROG 202's own scheduling note should settle it.

---

## 4. PS 0 is released on the second Wednesday, and the registry's date for it is a Friday

The Spring table in ASSESSMENT CALENDAR has *"W0 · Jan 23 · Problem Set 0 released (Wed)"*. **Jan 23 is
a Friday.** The row's own "(Wed)" and the general rule — *released Wednesday of their own week and due
the Friday of the week after* — both say Wednesday.

**PS 0 is released Wednesday Jan 21**, after L03, and due **Friday of Week 1 (Jan 30), 17:00**,
which the calendar's W1 row agrees with. The paper's header says "second Wednesday" rather than a
date, following the registry's instruction to quote week numbers.

---

## 5. The registry names no staff for this course, and nothing was invented

[[Year2 - Sophomore/OFFICE HOURS|OFFICE HOURS]] is titled **"YEAR 2 OFFICE HOURS — FALL"** and lists
the four Fall courses' instructors and TAs. **No Spring course has an entry**, so CS 202 has neither
an instructor nor a TA on record.

MATH 241 met a smaller version of this gap — a named instructor and no TA — and settled it by naming
nobody ([[MATH 241 Scheduling Notes]] §4). **CS 202 follows it.** The syllabus says the staff are not
yet listed and points at the Engineering Help Desk in BH 120, whose hours OFFICE HOURS does give. The
lab solutions refer to "the TA" throughout, which is a role, not a name.

**This is an omission, not a decision.** When Spring staff are assigned, the syllabus's *Schedule*
table is the one place to update.

---

## 6. The curriculum puts Project 2 and the final in Week 12, and the registry does not

The docx's Week 12 assignment list reads *"FINAL EXAM (comprehensive). Project 2 due (a small OS
kernel with scheduling, memory management, and a filesystem). Lab 12: Demo day."*

ASSESSMENT CALENDAR puts **Project 2 due Fri May 1** (the completion period) and the **final on
Wed May 6, 09:00–11:30**. **The registry is authoritative for dates**, and the Registry
Reconciliation already moved CS 202's midterms to the weeks the docx names — so the docx's *weeks*
are honoured where the registry had them wrong, and the registry's *dates* are honoured here, where
the docx is compressing a term's end into one list. Week 12 is built as an ordinary teaching week.

**Three consequences, each recorded in the syllabus's deviations table:**

| Question | Settled as | Why |
|---|---|---|
| When is Project 2 assigned? | **Week 9** | Neither document says. Week 9 is the first week in which all of its material — memory (Weeks 5–6) and filesystems (Weeks 7–8) — has been taught. It gives five weeks to the deadline and overlaps Project 1 by two |
| Is Project 2 a separate kernel? | **No — it extends the student's Project 1 xv6** | The docx calls the whole thing "a semester-long project in which you build … xv6 and extend it". Two independent kernels would contradict that |
| Lab 12 is demo day on Tuesday; Project 2 is due Friday | **The demo shows the kernel as it stands**, and is checked off like any lab | The submission is what is marked. A demo after the deadline would need a slot in finals week, which no lab has |

The gradebook's Project 1 row (*"assigned Week 7, due Week 11"*) and final row (*"150 min"*) already
match the registry.

---

## 7. Which xv6, and the one-line build fix

**The curriculum names xv6 and does not say which.** MIT has maintained two:
[xv6-public](https://github.com/mit-pdos/xv6-public), for 32-bit x86, and xv6-riscv, which replaced it
in MIT's own course in 2019. xv6-public's last commit, **`eeb7b41`**, is titled *"Be more explicit
that we are not maintaining the x86 version anymore."*

**This course uses xv6-public at `eeb7b41`.** Surveyed on the reference machine before anything was
written:

| Needed for | x86 | RISC-V |
|---|---|---|
| compiler | `gcc -m32` ✅ — freestanding compiles and `ld -m elf_i386` links | `riscv64-linux-gnu-gcc`, `riscv64-unknown-elf-gcc` ❌ both absent |
| emulator | `qemu-system-i386` ✅ 8.2.2 | `qemu-system-riscv64` ❌ absent |
| student can install | not needed | **no** — `sudo` requires a password; students have no root on the lab image |

The curriculum's *Language* line is **"C, x86-64 Assembly"**, and the course follows CS 201's x86
year, so the choice is also the better fit on the merits. **xv6-public is 32-bit x86, not x86-64**;
the syllabus says "x86" and does not blur the difference.

### The build fix, established by bisection rather than guessed

xv6-public's `Makefile` compiles with `-Werror`. Under **GCC 13.3.0** the unmodified tree fails:

```
mp.c:25:16: error: array subscript [-2147483648, -2147418114] is outside array bounds
            of 'void[2147483647]' [-Werror=array-bounds=]
```

Demoting only that one warning moved the failure on:

```
sh.c:58:1: error: infinite recursion detected [-Werror=infinite-recursion]
```

**With both demoted, the tree builds, boots and runs its shell**, and every other warning remains an
error. Neither is a real defect, and demoting them changes no generated behaviour. `mp.c` does pointer
arithmetic on a physical address that the compiler cannot know is valid. `sh.c`'s `runcmd` is written
never to return — `user.h` declares `exit` `noreturn`, and every path through `runcmd` ends either in
`exit()` or in a recursive `runcmd` on a smaller sub-command — and GCC 13's analysis reports a
function with no path that returns without recursing as infinite recursion. The recursion is bounded
by the parsed command tree. The fix students apply:

```bash
sed -i 's/-m32 -Werror/-m32 -Werror -Wno-error=array-bounds -Wno-error=infinite-recursion/' Makefile
```

**Tested end to end on a fresh clone**: `make qemu-nox CPUS=2` reaches `init: starting sh`; `ls`,
`echo` and a user program added to `UPROGS` all run. The linker also prints `missing
.note.GNU-stack` and `LOAD segment with RWX permissions` warnings for every user program; these are
warnings from `ld`, not errors, and the lab says to ignore them.

### A second fix, found in Week 1: xv6 was running on one CPU

**Week 0 shipped with only the build fix above, and every xv6 boot in it was on one CPU.** Nobody
would have noticed: `CPUS=2` is xv6's default, the kernel boots, the shell runs. What gave it away,
while building Week 1, was a boot log with `cpu0: starting 0` and no `cpu1` — in Week 0's own
transcripts too, on re-reading them.

**Bisected rather than guessed**, on the reference machine:

| Step | Result |
|---|---|
| Print `ncpu` after `mpinit` — first attempt, in `mpinit` itself | printed nothing: `mpinit` runs before `consoleinit`, so `cprintf` has nowhere to go |
| Print `ncpu` in `main` after `uartinit` | **`ncpu=1` for `CPUS` = 1, 2 and 4** |
| Dump every entry of the MP configuration table the firmware provided | with `-smp 2`: **one `MPPROC` entry**, apicid 0, then buses, one I/O APIC, interrupts |
| Same with `-accel kvm` | one `MPPROC` — not a TCG artefact |
| QEMU monitor, `info hotpluggable-cpus`, plain `-smp 2` | **`socket-id 0, core-id 0` and `socket-id 0, core-id 1`** — two cores, one socket |
| `-smp 2,sockets=2,cores=1,threads=1` | two `MPPROC` entries (apicid 0 and 1), **`ncpu=2`**, `cpu1: starting 1` |
| `-smp 2 -machine pc-i440fx-2.12` | also two entries, `ncpu=2` — an old machine type's default topology is one socket per CPU |

**So: QEMU 8.2's default machine type expands `-smp 2` into two cores of one socket, and the
firmware's legacy MP table then lists one processor.** xv6 reads only that table. The fix asks for
one socket per CPU:

```bash
sed -i 's/-smp $(CPUS)/-smp $(CPUS),sockets=$(CPUS),cores=1,threads=1/' Makefile
```

It changes **two** lines — `QEMUOPTS` and the `qemu-memfs` target — so with both fixes `git diff
--stat` reports three lines. **Verified on a fresh clone**: `cpu1: starting 1` and `cpu0: starting
0` at boot, and three `spin &` processes show **two `run` and one `runble`** under Ctrl-P.

**Week 0 was corrected in the Week 1 commit**: Lab 0 Part D now carries both `sed` lines, its
expected boot output shows `cpu1`, and it tells students to check for it; the Lab 0 solutions gain a
common-problems row; the syllabus's *Which xv6* and deviations row describe both fixes and say the
second was found late. **Lab 1 tells anyone who did Lab 0 before the correction to apply it.**

**The book edition matters.** The current xv6 book is written against the RISC-V code. The syllabus
and reading guide point to the **x86 revision 11**, whose listings match the tree students build.

---

## 8. The tool survey, done once before any week was written

Every week of the docx names a tool, and on a shared lab image some are absent or refuse to run.
**The survey was taken on the reference machine before Week 0 was written**, so that no week promises
something the machine cannot do, and each affected week settles its own substitute when it is built.

| Tool | Week | Found | What it means |
|---|---|---|---|
| `strace` | 0 | ✅ | used as the docx says |
| `gcc -m32`, `qemu-system-i386` | 0, all | ✅ | xv6 and the Lab 0 kernel |
| `chrt`, `nice`, `taskset` | 2 | ✅ | usable; **`SCHED_FIFO` needs `RLIMIT_RTPRIO`**, which PROG 201 found to be 0 — Week 2 must check |
| `gdb` | 4 | ✅ | **`kernel.yama.ptrace_scope` = 1**: gdb can run a program but not attach to an unrelated one. Lab 4 must start the deadlocking program under gdb |
| `valgrind` | 3 | ✅ | |
| `bpftrace` | 7 | ⚠️ **installed; prints `ERROR: bpftrace currently only supports running as the root user.`** | Lab 7 needs a substitute. `kernel.unprivileged_bpf_disabled` is 2 |
| `perf` | — | ⚠️ `perf_event_paranoid` = 4 | not relied on anywhere |
| `mkfs.ext4`, `debugfs` | 7–8 | ✅ | ext4 on an image file, inspected without mounting |
| `zfs`, `zpool`, `btrfs` | 8 | ❌ absent | Lab 8 needs a substitute |
| Kernel headers, `/lib/modules/$(uname -r)/build` | 9 | ✅ present | a module builds; **loading needs `CAP_SYS_MODULE`**. `/boot/vmlinuz-*` is mode 0600, so the host kernel image cannot simply be booted in QEMU either. Week 9 must settle where the module is loaded |
| `/dev/kvm` | 10 | ✅ **opens read-write** from the student account (ACL `+` on the device) | PS 10 and Lab 10 can run as the docx says |
| `etcd`, `etcdctl` | 11 | ❌ absent | network access to GitHub works from the account, so Lab 11 can consider a user-space download |
| `docker`, `podman` | — | ❌ absent | not needed by the docx |
| `busybox`, `cpio` | 9 | ✅ | an initramfs can be built without root |

---

## 9. Every number in Week 0 was measured on the reference machine

**Intel Core i5-8250U** (4 cores, 8 threads; L2 1 MiB, L3 6 MiB), **Ubuntu 24.04.4 LTS, kernel
7.0.0-30, GCC 13.3.0, glibc 2.39, QEMU 8.2.2** — the machine PROG 201 and MATH 241 used, so the
courses' figures are comparable where they overlap. The programs ship in `CS202 Week0/resources/`
with their build lines.

| Claim | Program | Result |
|---|---|---|
| The illusion (L01 §2) | shell one-liners over `/proc` | **351 processes, 1,425 threads, 8 CPUs**; **24,353 GiB VSZ** summed against **7.5 GiB** RAM; `Committed_AS` 27.0 GiB against `CommitLimit` 7.8 GiB; **9,533 context switches/s and 6,757 interrupts/s** with `top` at 81% idle |
| A user program runs in ring 3 | `privfault.c` | `CS = 0x33` |
| Six instructions fault in ring 3 | `privfault.c` | `cli`, `hlt`, `inb`, `outb`, `rdmsr`, `mov %cr3` → `SIGSEGV` |
| `sgdt` leaks a kernel address without UMIP | `privfault.c` | ran; **`0xfffffe530262c000`**; `CONFIG_X86_UMIP=y`; `umip` absent from `/proc/cpuinfo` |
| The kernel can make `rdtsc` fault | `tsc.c` | ran before `prctl(PR_SET_TSC, PR_TSC_SIGSEGV)`; `SIGSEGV` after |
| Kernel addresses read as unmapped | `kread.c` | `0xffffffff81000000`, `0xffff888000000000`, `0x0`, `0x7ffffffff000` → `SEGV_MAPERR` |
| A kernel of our own runs in ring 0 | Lab 0 reference | **`CPL = 0`**; 393 bytes of text; boot to power-off **142–152 ms**; QEMU makes **2,026** system calls to run it |
| xv6 opens one gate | xv6 `trap.c` 23–24, and `int13.c` in xv6 | `int $13` → **`trap 13 err 106`**; `cli` → **`trap 13 err 0`** |
| A system call's cost is the door | `syscost.c` | function 0.30 ns; vDSO 18.5 ns; `getppid` 592–609 ns; **`ENOSYS` 572 ns** |
| Batching | `readsize.c` | 16 MiB: **14.213 s** at 1 byte, **0.0022 s** at 64 KiB |
| Two tables, two doors | `int80.c` | `int $0x80` with `eax=39` → **`-14`** (i386 `mkdir`, `EFAULT`) |
| No libc: two calls | `nolibc.c` | `write`, `exit`; **9,168 bytes** against 785,360 for static `printf` |
| stdio probes its output | `strace` | to `/dev/null`: extra `ioctl(TCGETS)` → `ENOTTY`; to a pipe: none |
| gcc's failures are not errors | `strace -f -c` | **3,051 calls, 902 failed**: 481 `EINVAL` (mostly `readlink`), 401 `ENOENT`, 20 `ENOTTY` |
| xv6 validates pointers | `writek` in xv6 | `write(1, 0x80100000, 16)` → **−1** |
| The open gate with garbage `eax` | `int64` in xv6 | `eax` = 1 → **`fork`**; doubled output and `zombie!` from `init` |
| `fgetc` batches `read` | `strace -c` | **4,098** `read` calls for 16 MiB; **0.047 s** |

**Mitigations are recorded and not apportioned.** `/sys/devices/system/cpu/vulnerabilities` reports PTI,
IBRS (for Spectre v2 and retbleed), buffer clearing (MDS) and others. **L03 states the 590 ns total and
declines to split it**, because splitting it requires rebooting with different kernel parameters, which
a student account cannot do. PS 0 Q3(d) asks students to design that experiment instead.

---

## 10. Errors caught in drafts before anything used them

- **`tsc.c` lost its own output.** The first version printed `rdtsc`'s value in a forked child and
  called `_exit` — into a pipe, so the line sat in stdio's buffer and was discarded. **PROG 201 L01
  §6's bug, in this course's own measurement code**, noticed because the "before" line was missing.
  Fixed with `fflush`, and the Week 0 README names it.
- **A strace count of 17 against 18.** The lecture's listing of a static `hello` (into a pipe) had 17
  lines and the count run (into `/dev/null`) had 18. **The difference is a real call** —
  `ioctl(TCGETS)`, stdio asking whether a character device is a terminal — and it became L03 §3's
  point about traces depending on where output goes, and Lab 0's Q2. The table now states its
  convention.
- **gcc's failures were first described as "looking for files".** Measured: 481 of 902 are
  `EINVAL`, nearly all from `readlink` canonicalising paths; 401 are `ENOENT`. L03 now says so.
- **`SEGV_MAPERR` on kernel addresses was nearly cited as evidence of page-table isolation.** It is
  not: Linux reports a user-mode fault on any kernel-half address as `SEGV_MAPERR` whether or not PTI
  is on. L02 §6 reports the result and cites PTI only from the `vulnerabilities` file.
- **An unmeasured size ratio** — "Linux's kernel is over three thousand times larger" than xv6's —
  was removed from L01 §6.
- **A shortened PID in L03 §5's strace excerpt** was replaced with the real one.
- **The first `nolibc.c`** referenced a function-local static from top-level assembly and failed to
  link (`undefined reference to 'msg.0'`). The PS 0 solutions mention it, because students will hit it.

---

## 11. Presidents Day is Midterm 1, and nobody has decided whether it is a holiday

**Mon Feb 16 — the Monday of Week 4 — is the third Monday in February**, Presidents Day. On it
ASSESSMENT CALENDAR places **CS 202's Midterm 1** (18:00–19:15, VNC 100) and, by the quiz rule,
**Quiz 4** at 09:00. Year 1's calendar flags Presidents Day as an open decision; Year 2's does not
mention it.

**Nothing was moved.** The registry schedules classes and the exam that day, and CS 202 follows the
registry. If the department later observes the holiday, Midterm 1, Quiz 4 and L10 all move together,
and the Week 4 README is the place a student would need to be told.

---

## 12. Every number in Week 1 was measured, and the programs ship with the notes

Same reference machine as §9. Week 1's programs are in `CS202 Week1/resources/`, the xv6 user
programs in `CS202 Week1/lab/`, and PS 1's `worker.c` and `test.pm` in `assignments/ps1/`.

| Claim | Program | Result |
|---|---|---|
| xv6's records are small | `nm -S` on an object compiled against xv6's headers with `-m32` | `struct proc` **124**, `context` **20**, `trapframe` **76**, `cpu` 176 bytes; `NPROC` 64 |
| Linux's are not | `tsize.c`, a module **built against the 7.0.0-30 headers and never loaded** | `task_struct` **9,920**, `mm_struct` 1,728, `files_struct` 704, `cred` 184, `thread_struct` 184 bytes |
| `/proc` per process | `ls /proc/self` | 57 entries |
| Table limits | `/proc/sys/kernel`, `ulimit -u` | `pid_max` 4,194,304; `threads-max` **51,142**; `RLIMIT_NPROC` 25,571; `CLK_TCK` 100 |
| Mode bits on `/proc` do not tell the whole story | `ls -l`, `head`, `cat` on `/proc/1/*` | `status` readable; **`maps` is `-r--r--r--` and still `EACCES`**; `environ` 0400 |
| File capability, then dropped | `getcap`, `/proc/<ping>/status` at 0.7 s | `cap_net_raw=ep` on the file; **`CapPrm` and `CapEff` both 0** while running |
| Threads are cheaper | `spawn.c` | `pthread_create`+`join` **27.6 µs**; `fork`+`_exit`+`waitpid` **154.3 µs**; 5.6× |
| Every state, on purpose | `states.c` | R, S, T, Z, **t** under `ptrace`, **D** for a parent inside `vfork` |
| Almost everything sleeps | `ps -eo stat=` | 261 S, 81 I, **1 R** |
| Voluntary against involuntary | `hog.c`, 5 s on CPU 5 | hog **0 / 4,788**; sleeper **4,748 / 0** |
| One context switch | `ctxsw.c` | baseline pair **1,438 ns**; **2.00 switches per round**; **1,622 ns per switch** on one CPU, **2,139 ns** across two |
| FPU state size | `xsave.c` | XSAVE area **1,088 bytes**; XCR0 `0x1f`; XSAVEOPT, XSAVEC, XSAVES supported |
| Linux's switch frame and FPU policy | the reference machine's `switch_to.h` and `fpu/sched.h` | `inactive_task_frame`: r15–r12, bx, bp, return address; `switch_fpu` **saves eagerly**, restore deferred via `TIF_NEED_FPU_LOAD` |
| ASLR | `layout.c`, three runs and `setarch -R` | every region moves by whole pages; **`0x555555555180`** with `-R`; `randomize_va_space` 2 |
| Address space is not memory | `rss.c` | `VmSize` **+256 MiB** at `mmap`, `VmRSS` unchanged until written, then +64 MiB per quarter |
| xv6's table | Ctrl-P with `spin &` | one CPU: 1 `run`, 1 `runble`; two CPUs (after §7's second fix): **2 `run`, 1 `runble`** |
| xv6 saves no FPU state | `fpu.c` in xv6 | one CPU, two runs: **39,552,364 + 447,636** and **39,786,312 + 213,688**, each pair **= 40,000,000**; two CPUs: 20,000,000 and **19,958,711** |
| `pm` works | `./pm < test.pm` | every job listed from `/proc`, zombies once then reaped, `exited 127` for a missing program, no survivors |

---

## 13. The context-switch measurement, and why its first version was not reported

The first `ctxsw.c` timed the ping-pong and reported **"ns per half round trip" — about 3.0 µs** —
on the assumption that each half round trip is one switch. **Its own counters contradicted it**: the
parent's voluntary-switch count came out at about **100,000 for 200,000 rounds**, where the
assumption predicted 200,000.

**The explanation turned out to be that switches were being counted in one process only, and only
voluntary ones.** Counting **voluntary and involuntary, in both processes** — the child's through
`RUSAGE_CHILDREN` — gave **exactly 2.00 switches per round** in every configuration, split about
half and half on one CPU (the waking task preempts the writer) and all voluntary across two.

**The time was then still not the switch's alone**, so a baseline — the same `write` and `read` in
one process, where nothing blocks — is subtracted. **L05 §5 reports the result as an upper bound**
and says why: a blocking `read` and a waking `write` do work the baseline never does. PS 1 Q3(b) asks
students to find the assumption.

`perf bench sched pipe` **runs without perf events** despite `perf_event_paranoid` = 4, and reports
**2.81 µs per operation**. It is not quoted in the lecture, because what it calls an operation is not
a single switch, and one number with an unclear denominator is worse than none.

---

## 14. The curriculum's lazy-FPU claim, checked against this kernel

The Week 1 Core Concept says FPU/SSE state *"is saved lazily — only when the new process uses
floating-point instructions, signaled by a fault."* **The reference machine's kernel headers say
otherwise.** `arch/x86/include/asm/fpu/sched.h` documents `switch_fpu()` saving the outgoing task's
state at every switch and setting `TIF_NEED_FPU_LOAD`, with the restore deferred to the return to
user space and no fault anywhere.

**L05 §6 teaches the current design and keeps the curriculum's as history**, with the two reasons
it was retired: fast component-wise saving with `XSAVEOPT`, and the 2018 *LazyFP* disclosure.
Recorded as a deviation in the syllabus.

**The claim was checked from the headers rather than from memory** because the headers are on the
machine, and because "Linux does X" in a lecture should mean *this* Linux.

---

## 15. xv6 does not save FPU state, and the first draft of the demonstration got its own expected value wrong

`fpu.c` forks two processes that each add `0.5` twenty million times — **so each should finish at
`x*2 = 20,000,000`**. The first draft printed `(expected 40000000)`.

**On one CPU nobody could see the mistake**, because both processes were wrong anyway and their two
answers summed to 40,000,000 — which is both correct answers combined, and which the draft lecture
described as "the right total". **It surfaced on two CPUs**, where the child printed `final x*2 =
20000000 (expected 40000000)`: a correct answer next to an incorrect expectation.

**Corrected and re-measured, not relabelled.** The message was fixed, `fpu` was re-run twice on one
CPU and once on two, and **every quotation of the old numbers** — in L05 §6, the README, the summary,
Lab 1's solutions and PS 1's — was replaced with the new runs, so that each quoted line is output
the shipped program actually produced.

**The two-CPU run became part of the lesson.** One checkpoint of forty was wrong in the parent
(19,958,711), because a process is not tied to a CPU and the two sometimes shared one across a
switch. L05 §6 and Lab 1's new Q10 say so: **more CPUs made the bug rarer, not absent.**

---

## 16. `worker.c`'s memory mode allocated nothing

PS 1's `worker mem 64` first did `malloc(64 MiB)` followed by `memset(p, 1, n)`, and `pm` listed its
RSS as **1,424 kB**. **GCC at `-O2` had deleted the `memset`** — the buffer is never read, so the
writes are a dead store, and GCC knows `malloc`'s memory is invisible to anyone else.

**Fixed by touching one byte per page and reading one back through a `volatile`**, after which RSS
is **66,952 kB**. The original is now **PS 1 Q2(d)**, which has students put the `memset` back and
explain the RSS — L06 §3's lesson with the compiler as the cause.

---

## 17. PS 1 is not PROG 201's Lab 0 again

The curriculum sets *"Problem Set 1: Implement a user-space process manager."* PROG 201's Lab 0 was
a process **supervisor** — restart on crash, give up on flapping, shut down cleanly — and a student
takes CS 202 having written it.

**PS 1's `pm` is deliberately a different program**: it reads the kernel's table rather than reacting
to signals. There is no `SIGCHLD` handler — reaping in one would make the question's zombie rule
impossible to satisfy — and the marks are for **parsing `/proc/<pid>/stat` from the last `)`**,
knowing a zombie has no `VmRSS`, and reporting a zombie once before reaping it. `pm` is prohibited
from running `ps`.

---

## 18. Errors caught in Week 1 drafts

- **The context-switch figure**, §13.
- **`fpu.c`'s expected value**, §15.
- **`worker.c`'s dead store**, §16.
- **`ncpu` printed from inside `mpinit`**, before the console existed — printed nothing, and briefly
  looked like a hang. Moved to `main`.
- **`tsize.c` failed to compile** because `struct files_struct` is incomplete without
  `<linux/fdtable.h>`.
- **`layout.c` called `getpid` without `<unistd.h>`** — a warning, and in a course that says warnings
  are bugs, a bug.
- **The reading guide's `process-run.py` flags** gave the simulator no process that does I/O, so the
  I/O policy flag it asked students to change did nothing. Replaced with a job list that has one.
- **Two xv6 boots in Week 0's own transcripts** show `cpu0` and no `cpu1`, and were not noticed until
  Week 1 — §7.

---

*Academic Registry · Build Records · © CSE Department*
