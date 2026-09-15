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

## 19. Every number in Week 2 was measured or simulated, and the programs ship with the notes

Same reference machine as §9. Linux measurements in `CS202 Week2/resources/`; the simulator skeleton
and workloads in `assignments/ps2/`; the reference simulator in `solutions_instructor/`.

| Claim | Program | Result |
|---|---|---|
| The convoy and SJF | `schedsim` on `convoy.txt` | FCFS **110.0** / SJF **50.0** ms average turnaround |
| Non-preemptive SJF with arrivals | `late.txt` | SJF = FCFS = **103.3**; SRTF **50.0** |
| The quantum sweep | `rr:Q` on `convoy.txt` | q = 1: 59.7 ms, response 1.0, **30 switches**; q = 10: **56.7**; q = 100: **110.0** (= FCFS) |
| Interactive against batch | `mixed.txt` | editor wait per keystroke: FCFS **10.0**, RR10 **1.3**, RR50 **8.5**, MLFQ **0.4**, fair **0.3** ms |
| Gaming | `gamer.txt` | naive rule: gamer **241**, honest **400**; final rule: honest **263**, gamer **415** |
| Starvation | `starve.txt`, naive rules | no boost: long job **900** (waiting 800); boost 100: **422** |
| xv6's quantum | `ticks.c` in xv6, timed from the host | **100.1 ticks per second** |
| `nice` divides a CPU by the weight table | `share.c` | nice 1 **44.4%** (table 44.5), 5 **24.6** (24.7), 10 **9.5** (9.7), 19 **1.3** (1.4); `SCHED_IDLE` **0.3** (0.3); `SCHED_BATCH` 50.0 |
| This kernel is EEVDF | reference machine's `include/linux/sched.h`; `/proc/self/sched` | `sched_entity` has `deadline`, `min_vruntime`, `vlag`, `vprot`, `slice`; `se.slice` **2,800,000 ns**; `SCHED_EXT` = 7 and `CONFIG_SCHED_CLASS_EXT=y` |
| The slice does not shrink | `slice.c` | run length **3.00 ms** for 2, 3 and 4 hogs; time off CPU 3.00 / 6.00 / 9.00 ms; `CONFIG_HZ=1000` |
| Autogroup inert | `share.c` with `setsid`; `/proc/self/cgroup`; `cgroup.subtree_control` walk | nice 19 in its own session **1.3%**; `cpu` enabled down to `user@1000.service`, not below `app.slice` |
| A cgroup weight overrides `nice` | `systemd-run --user --scope -p CPUWeight=100` | `app.slice` gains `cpu` while the scope lives; **nice-19 hog 57.8–58%**; controller removed afterwards |
| Refusals | `chrt`, `nice`, `ulimit` | `SCHED_FIFO`, `SCHED_RR`, `SCHED_DEADLINE`: `EPERM`; `RLIMIT_RTPRIO` 0; `RLIMIT_NICE` 0; nice −5 denied |
| Real-time cap | `/proc/sys/kernel` | `sched_rt_runtime_us` 950,000 of 1,000,000; `sched_rr_timeslice_ms` 100 |
| Rate-monotonic and EDF | `rtsim.c` | `1/4 2/6 3/12` (U 0.833 > bound 0.780): **RM no misses**; `2/5 4/7` (U 0.971): **RM misses at t = 7**, EDF none |
| Latency | `lat.c` | busy CPU median **54 µs** → **4 µs** with slack at 1 ns; idle CPU **144 µs** → **93 µs**; `timerslack_ns` 50,000 |
| Idle states | `/sys/devices/system/cpu/cpu7/cpuidle` | `intel_idle`, `menu` governor; exit latency C1 2 µs … C6 85 µs, C8 200 µs, C10 **890 µs** |

**The latency maxima of 2–4 ms are reported and not explained.** They occur a few times in 3,000 with
and without competition; their cause needs kernel tracing (`bpftrace`, `perf`), neither of which an
account can run here (§8). L09 §6 says so rather than guessing.

---

## 20. The curriculum names CFS; this kernel runs EEVDF

The Week 2 Core Concept describes CFS as always running *"the process with the least CPU time … in
O(log n) with a red-black tree"*. **CFS's weights, `vruntime` and red-black tree are all still in the
kernel, and L08 teaches them.** What changed in Linux 6.6 is the *selection*: eligibility by lag,
then earliest virtual deadline.

**Checked from the reference machine's own headers and `/proc`, not from memory**, for the same reason
as §14. The evidence that matters in a lecture is the evidence a student can reproduce: one `sed` of
`sched.h` and one `cat` of `/proc/self/sched`. **Recorded as a syllabus deviation.**

**The measurement that makes it concrete is `slice.c`**: a slice that stayed at 3.00 ms with two,
three or four hogs, where the course's own fair model — dividing a latency target — shrinks it. PS 2
Q5 is built on the disagreement.

---

## 21. Autogroup is on and does nothing, and a CPU weight changes more than one group

**Found by prediction.** `share.c` was written expecting autogroup to split two hogs in different
sessions 50/50, and **measured 1.3%**. Reading `/proc/self/cgroup` and walking `cgroup.subtree_control`
up the tree showed the `cpu` controller enabled from the root down to `user@1000.service` — so
`app.slice` is a CPU group and every desktop process is below it. **Autogroups apply only to tasks in
the root CPU group.**

**The next measurement was initially misread.** A `systemd-run --user --scope -p CPUWeight=100` test
gave the nice-19 hog **58%**, and a second run without the property gave **1%**. The difference is
that **requesting a CPU weight makes systemd enable the `cpu` controller in `app.slice`** for the life
of the scope. **Confirmed by reading `app.slice`'s `cgroup.subtree_control` before (`memory pids`),
during (`cpu memory pids`) and after (`memory pids`)** — in two separate runs, one of them Lab 2's own
procedure.

**Lab 2 Part C teaches both halves.** Its solutions note that student paths in BH 210 may differ — an
SSH login ends in a `session-N.scope` — and that a student whose task *is* in the root CPU group will
see autogroup work, which is the better answer.

---

## 22. `schedsim` had two modelling bugs, and its own output found both

**MLFQ demotion was skipped whenever a job blocked.** Step 6 checked the allotment only if the job was
still running after its millisecond — so a job that blocked on the millisecond it exhausted its
allotment was never demoted, and **a job blocking after every millisecond could never be demoted at
all.** It surfaced as `starve.txt` showing the long job starving under the *final* rules, which the
rules are designed to prevent. **The allotment is now charged before the blocking check**, and the
student skeleton's `TODO` says why.

**The fair policy had no wake-up preemption**, and on `mixed.txt` produced output **identical to
`rr:10`**, line for line. That was the clue: with two equal weights the fair slice is exactly 10 ms,
so without some other trigger the policies coincide. Wake-up preemption was added; the editor's wait
fell from 1.3 to 0.3 ms. **PS 2 Q2(b) has students remove it and find the same coincidence.**

**The skeleton was checked against the reference after both fixes**: FCFS, SJF, SRTF and round robin
produce byte-identical output on `convoy`, `late` and `mixed` (compared with `md5sum`).

---

## 23. Two PS 2 questions were wrong until the reference was run on them

**Q3(a) asked "at what allotment does the gamer start to win".** Run for *A* = 5 to 1000 under the final
rules, **the gamer never wins**: the honest job's lead shrinks from 172 ms to 32 ms and never
reverses. Reworded to ask whether it ever wins and why the gap narrows.

**Q2(c) asked students to remove sleeper placement and explain the change on `mixed.txt`.** There is
none: the editor never sleeps long enough to fall below the floor. A workload was designed to show the
effect — `burst.txt`, a job computing 100 ms and sleeping 200 — where the batch job's finish moves
from **811 to 900 ms** without the floor. The question now asks for both workloads and why one
changes. **Its first draft named the two jobs `batch` and `burst`**, which share a first letter and
made the timeline unreadable; the napping job is now `nap`.

**Every expected-output line in PS 2** was pasted from a reference run, not typed.

---

## 24. The first Lab 2 reference transcript measured one process twice

Running Lab 2 as a script to produce reference answers, **Part A reported the same PID on both lines**:
the first `hog` had been started in the background before the working directory was entered, `taskset`
failed with `No such file or directory`, and `pgrep -n` then found the second hog both times. **A slip
in the reference run, not in the handout** — re-run correctly, the shares are 44.4 / 24.7 / 9.7 / 1.4%.

**It became a common-problems row** in the Lab 2 solutions, because students running the same commands
out of order will get the same symptom, and `cpushare.sh` printing the PIDs is what makes it visible.

---

## 25. Every number in Week 3 was measured, and the programs ship with the notes

Same reference machine as §9. Programs in `CS202 Week3/resources/`; the futex lock skeleton in `lab/`;
the PS 3 skeletons in `assignments/ps3/`; references in `solutions_instructor/`.

| Claim | Program | Result |
|---|---|---|
| A race loses updates | `race.c`, 10M per thread | 2 threads **49.9%** lost, 4: 73.9%, 8: 68.8%; on one CPU **37.4 / 64.9 / 77.9%**; 1,000 per thread: **0 lost**; 100,000: 44.1% |
| Uncontended lock costs | `lockcost.c`, CPU 3, 50M | none 1.61; atomic 5.41; TAS 10.68; CAS 12.68; futex (three-state) 10.67; `pthread_spin` 8.36; **`pthread_mutex` 7.39**; `sem` 19.05 ns |
| An uncontended mutex never enters the kernel | `uncont.c` under `strace -f -c` | **34 system calls for the whole program, none `futex`**, for 50M lock/unlock pairs |
| Sharing without locks | `contend.c` | per-thread padded counters **1.5 → 0.3 ns** at 8 threads; shared atomic **7.4 → 29–32 ns** |
| TAS against TTAS | `contend.c`, 20M | TAS 14.9 / 65.0 / 167.6 / **263.8**; TTAS 16.7 / 50.7 / 114.3 / **121.6**; `pthread_spin` 8.6 / 21.8 / 37.7 / **54.9** ns |
| When to spin | `contend.c`, section of 2,000 iterations | 4 threads, 1 CPU: TTAS **8.25**, spin 8.06, futex 3.15, mutex 3.24 µs; 4 CPUs: TTAS **3.21**, spin 3.19, futex 3.93, mutex 4.13 µs |
| `FUTEX_WAIT` compares first | `futexlab eagain` | expected 7 on 5 → **−1, `EAGAIN`** |
| Always-wake against three-state | `futexlab` | uncontended **638.6 ns, 1M calls per 1M ops** against **14.8 ns, 0 calls**; 4 threads 300.2 ns and 2,000,255 calls against **100.3 ns and 7,095** |
| A waiter count outside the lock word | `futexlab buggy2` | **hung 10 of 10**, counter stuck near 1,001,000 of 4,000,000, lock 0, waiters 0 |
| glibc's mutex, contended | `contend mutex 4 4000000` under `strace -f -c` | 28,393–33,426 `futex` calls; 1 call with one thread (from `pthread_join`) |
| CVs: `if` against `while` | `bbuf.c`, 300,000 items, 3 consumers | `if`: **254–372** wake-ups to an empty buffer; `while`, two CVs: **0** |
| One CV for two conditions | `bbuf.c while1` | **deadlocked after 2, 3 and 10 items** |
| Dining philosophers | `philo.c` | naive **10 of 10 deadlocked** after 786–1,157 meals; ordered and seats 0 of 10 |
| Philosophers' fairness | `philo3` reference, 3 s | ordered ratio **0.56–0.64**, philosopher 4 fewest; seats and waiter **0.99–1.00** |
| Writer starvation | `rw.c`, `rwpref` reference | glibc default **0 writer acquisitions in 4 s**; prefer-writer 389–390, median 0.19–0.20 ms; readers lose ≈3% |
| xv6 without its allocator lock | `allocstress` in xv6, `CPUS=2` | **`CORRUPTION … found 66, wrote 65`**, two `sbrk` failures; second run **`panic: remap`**; locked kernel **1,000 iterations clean** ×4 |
| The spin-then-yield CAS mutex | `casmutex` reference | 4 threads 1 CPU: **3.20 µs** against spin 8.11, `pthread` 3.18; 8 threads 4 CPUs: **3.18** against 5.95 and 3.97 |
| A non-atomic lock at `-O2` | `casmutex broken` | **hangs** (timeout at 400k and 40k); disassembly shows `held` loaded once and `call sched_yield; jmp` back to the call |
| The same lock, `volatile` or `-O0` | `casmutex` variants | no hang; counters **26,142–38,081 of 40,000** |

---

## 26. The allocator-lock experiment needed a program designed to show it

**The first attempt ran `usertests` on an xv6 without `kmem.lock`**, next to a locked kernel, for 70 s
each. **Both were cut off by the timeout in the middle of `usertests`**, and the window included a full
rebuild. The locked kernel's `trap 14` lines were `usertests`' deliberate faults, not failures.
**Nothing could be concluded.**

**`allocstress.c` was written to make the failure visible if it happens and impossible to miss.** Four
processes grow by eight pages, fill every byte with their own letter, verify, and shrink, 1,000 times.
**The letters are `'A'`+*k*, chosen to avoid 0 (a fresh page from `allocuvm`) and 1 (the junk `kfree`
writes)**, so a mismatch can only mean another process's data. Both kernels were built before timing
started.

**Results were unambiguous in two runs** (§25). L11 §7 reports all three outcomes — corruption, false
out-of-memory, panic — because each is a different face of the same race.

---

## 27. PS 3's non-atomic lock hangs, and the compiler is why

PS 3 Q2 was drafted expecting the `broken` lock — `while (m->held) sched_yield(); m->held = 1;` — to
**print a wrong counter**. **The reference run never finished**: it timed out at 4,000,000, 400,000 and
40,000 operations.

**The disassembly of `work()` at `-O2`** shows the load of `bm` once, then `call sched_yield` and a
`jmp` straight back to the call. **GCC hoisted the test out of the loop.** It may: a data race on a
non-atomic object is undefined behaviour, and `bm` is `static` with an address that never escapes the
file, so under single-threaded semantics `sched_yield` cannot change it.

**Confirmed both ways**: at `-O0`, and at `-O2` with `volatile int held`, the program terminates with
the expected wrong counter (26,142–38,081 of 40,000). **One thread, and two threads with 4,000
operations, completed correctly** — the hang needs a thread to observe the lock held at least once.

**Q2 was rewritten around the finding** — predict, observe the hang, find the loop, explain the
compiler's licence, then make it `volatile` and find the lost-update interleaving. **It is a better
question than the one drafted**: "a race is undefined behaviour" is usually taught as a sentence, and
here it is a hang with a disassembly.

---

## 28. PS 3's fairness hint pointed at the wrong strategy

Q3(c)'s draft hint asked *"what happens to philosopher 1 if philosophers 0 and 2 alternate eating?"* —
expecting `waiter` to be the unfair strategy. **Measured, `waiter` was the fairest (0.99–1.00) and
`ordered` the least fair (0.56–0.64)**, with philosopher 4 — whose first fork is 0, shared with
philosopher 0 — eating fewest in every run.

**The hint now asks students to list each philosopher's first fork under `ordered`.** The solutions
still credit a student who argues `waiter` can starve in principle, provided they report that it did
not in their measurement.

---

## 29. Output lost to `_exit`, for the third time

`bbuf.c` and `philo.c` first reported **nothing** — every line was in stdio's buffer when `_exit` ran
from a watchdog, with output going to a pipe. **Week 0's `tsc.c` (§10) had the same bug.** Each program
now calls `fflush(stdout)` before `_exit`. `philo.c`'s deadlock counts survived the first run only
because the script also checked the exit status.

**Worth recording as a pattern, not three accidents**: every program in this course that measures a
concurrency failure needs to exit from a thread that is not stuck, and `_exit` is the natural call.
Later weeks' watchdogs should be written with the flush in from the start.

---

## 30. Week 4 was measured twice, on two kernels, and only the second set is quoted

**The build paused on 2026-09-11 with Week 4's measurements taken and no Week 4 file written.** The
session scratchpad did not survive the pause, and **the reference machine's kernel was updated from
7.0.0-30 to 7.0.0-31** in the meantime. **Every Week 4 measurement was retaken on 2026-09-15**, from
programs rewritten to the same design, and **only the retaken figures appear in the course.** Week 4's
Lab 4 solutions say which kernel; Weeks 0–3 remain on 7.0.0-30.

**Two of the lost first-run figures would have been wrong had they been used**: the first `banksim`
(§32) and a first Banker's scaling test that failed every comparison at the first resource, so that
*m* had no effect. The retaken versions fix both.

---

## 31. Every number in Week 4 was measured, and the programs ship with the notes

Kernel 7.0.0-31; otherwise the reference machine of §9. Programs in `CS202 Week4/lab/` and
`resources/`; Banker, detection and simulation references in `solutions_instructor/`, because PS 4
asks students to write them.

| Claim | Program | Result |
|---|---|---|
| ABBA deadlocks | `abba.c`, 20 runs each | no work: **400 274 336 32 0 687 … 959**, median ≈ 378; work 1,000: **18 631 0 15 … 1**, median ≈ 9 |
| The cycle from `/proc` | `abba.c`'s watchdog | two tasks in `S`, `wchan futex_do_wait`, **syscall 202 on `&B` and `&A`, op 0x80, value 2**; owners cross |
| The cycle from `gdb` | `gdb -batch` with `SIGTRAP` | LWP 10822 in `one` at `abba.c:32` on `<B>`; LWP 10823 in `two` at `abba.c:46` on `<A>`; owners 10822 and 10823 |
| No attaching | `gdb -p` | **"Could not attach to process"**; `ptrace_scope` 1 |
| Ordering removes it | `abba` with both threads A then B | **no stall in 30 s: 199,254,198 rounds** (slowest second 5,403,919); work 1,000: 10,787,201 |
| Mutex types | `errchk.c` | default relock `ETIMEDOUT` after 1 s; error-checking **`EDEADLK`**; robust **`EOWNERDEAD`**, then 0 after `pthread_mutex_consistent` |
| `lockdep` absent | `/boot/config-7.0.0-31-generic` | `# CONFIG_PROVE_LOCKING is not set`; `CONFIG_DETECT_HUNG_TASK=y`, timeout 120 s |
| Banker, textbook | `banker` reference | SAFE ⟨P1, P3, P4, P0, P2⟩; P1 (1,0,2) **GRANTED**; P4 (3,3,0) **WAIT**; P0 (0,2,0) **DENIED** |
| Safety-check cost | `bankbench.c` | *m* = 4: 0.018 → **20.590 ms** for *n* = 100 → 3,200; *m* = 32: 0.066 → **74.690 ms** |
| Conservativeness | `banksim` reference, 10,000 runs | `UNITS` 6: naive **42.3%** deadlocked, Banker **0**, 6.5 refusals per run; `UNITS` 4 / 9 / 12: 24.5% / 33.5% / 67.0% |
| Detection, textbook | `detect` reference | no deadlock ⟨P0, P2, P3, P4, P1⟩; with P2 requesting one more C: **P1 P2 P3 P4** |
| The "holding nothing" rule | `detect` with and without it | P3 holding nothing and waiting: **P0 P1** with the rule, **P0 P1 P3** without |
| Livelock | `livelock.c` | polite **128,579/s, 32.21 failures per round** (2 CPUs), 50,322/s and 53.92 (1 CPU); back-off 1.31M/s; ordered 0.87M / 1.42M |
| Fixed and exponential back-off | PS 4 Q5 reference | fixed 50 µs **1.29M/s, 0.01**; expo 1.28M/s on 2 CPUs, **1.41M/s on 1** |
| xv6 double acquire | `sys_uptime` with two `acquire`s | **`lapicid 0: panic: acquire`**; `addr2line`: `acquire ← sys_uptime ← syscall ← trap ← alltraps` |
| Midterm 1 | `midterm1_check.sh` | FCFS 15.25 / 8.75; SRTF 13.0 / 4.25; RR-4 18.25 / 4.5; RM set *U* 0.85, *R*₃ = 8, no misses; **every assertion passes** |

---

## 32. The first random simulation of the Banker was wrong

**The first `banksim` drew one random request and, when the Banker refused it, retried a new random
draw** — counting every retry as a refusal, sometimes retrying the same unsafe request many times, and
bailing out after a step limit that it then counted as a deadlock. **Its figures (32.7% naive
deadlocks, 2.1 refusals per run) were never used.**

**The rewrite enumerates every grant possible at each step, filters out the unsafe ones under the
Banker, and chooses among the rest**, so a refusal is counted once per step and a run under the Banker
can only end by finishing. **L14 §6 quotes the rewrite.**

**Its rates are not monotonic in the supply** — 24.5%, 42.3%, 33.5%, 67.0% for 4, 6, 9 and 12 units —
because the claim range `UNITS/2` rounds down and zero claims become rarer as supply grows. **PS 4 Q3(b)
was drafted asking students to explain why both columns "fall"**, and was rewritten to ask them to
describe the trend and explain it from the claim distribution, before release.

---

## 33. PS 4's first states did not exercise what they were written to

**`ps4_state.txt`'s first version** produced GRANTED, WAIT, WAIT and ERROR — **no DENIED**, the one
outcome that distinguishes the Banker from a simple availability check. **`ps4_detect_b.txt`'s first
version** was meant to be deadlocked and was not. Both were redesigned by hand and then confirmed with
the reference programs: the new Banker state produces **all four outcomes** (GRANTED twice), and the
detection pair differs in one request and is **deadlock-free and deadlocked (P0 P1)**.

**The second design also gave Q2(c) its best example**: a process holding nothing, waiting on a
deadlocked holder, reported deadlocked only by a detector that drops the "holding nothing" rule.

---

## 34. The "fixed" ABBA check reported a deadlock while both threads were running

The first program written to show that lock ordering prevents the deadlock **printed `DEADLOCK after
59,870,831 rounds`**, with both worker threads in state `R` and neither lock owned. **The watchdog's
end-of-run test was wrong**, not the fix. The rewrite reports a deadlock only for a **whole second
with zero progress**, runs for 30 seconds, and prints the slowest second's round count.

**It is now a Lab 4 common-problems row**, because students rewriting the watchdog in Part D will make
the same mistake.

---

## 35. A fixed back-off did not collide, and the question expected it to

PS 4 Q5(b) was drafted to ask *"explain why `fixed` behaves as it does, in terms of what happens when
both threads fail at the same moment"* — expecting a fixed 50 µs sleep to reproduce the collisions.
**Measured, `fixed` was as good as random back-off** (1.29M rounds per second, 0.01 failures per
round). **A 50 µs sleep is not 50 µs**: timer slack and wake-up latency — L09 §6's own measurements —
randomise it by tens of microseconds. **The question now asks students to predict, observe, and explain
from L09**, and to say what would make `fixed` collide.

---

## 36. Midterm 1: marks, content, and the script that checks it

**100 marks in 75 minutes**, five questions of 20. The gradebook records *Possible 100* and *75 min*;
MATH 241's final followed its gradebook in the same way (§6 of its notes), and CS 211's
one-mark-per-minute convention was not adopted. Recorded as a syllabus deviation.

**Every number in the mark scheme is produced by `midterm1_check.sh`**, which builds the Week 2 reference
simulator and `rtsim` from the vault and asserts the rest. **The paper's scheduling question was chosen
so that SRTF's preemption at *t* = 1 changes the schedule**, and its real-time set so that the
Liu–Layland bound is inconclusive and response-time analysis decides.

**No Week 4 material appears on the paper.** Q5 is a synthesis question on a new xv6 system call whose
four parts between them draw on all of Weeks 0–3 — the timer interrupt and a lock, the user pointer,
system-call cost, and gaming a scheduler — and do not depend on one another, so a student stuck on one
part can still answer the others.

**Presidents Day** (§11) falls on the midterm's Monday; the Week 4 README says so and that the calendar
schedules the paper as normal.

---

## 37. Lab 4 cannot attach `gdb` to a running process

The curriculum's *"detect it with gdb"* reads naturally as attaching to a hung program. **On the lab
image `ptrace_scope` is 1**, measured refusing `gdb -p` on the student's own process. **Lab 4 measures the
refusal, starts the program under `gdb` instead, and teaches diagnosis from `/proc`** — which works where
no debugger can attach — as its central part. Recorded as a syllabus deviation.

---

## 38. Every number in Week 5 was measured, and the programs ship with the notes

Kernel 7.0.0-31; otherwise the reference machine of §9, with a 4 GiB swap file and transparent huge
pages set to `madvise`. Programs in `CS202 Week5/resources/` and `lab/`; the PS 5 reference in
`solutions_instructor/`. xv6 measurements use `resources/nfree.patch` — **one added system call,
`nfree()`, counting the kernel's free list** — on the Lab 0 build.

| Claim | Program | Result |
|---|---|---|
| ASLR | `aspace.c`, two runs | `main` at `0x56890e4a20c0` and `0x629a5e82a0c0`; stack `0x7ffd4461f8e4` → PGD 255, PUD 501, PMD 35, PTE 31, offset 2276 |
| Top of user space | `aspace.c` | `MAP_FIXED_NOREPLACE` at 2⁴⁷ and at 2⁴⁷ − 4096 both fail; a hint at 2⁵⁶ returns `0x7089ae420000` |
| Five levels built, four run | `/boot/config-7.0.0-31-generic`, `/proc/cpuinfo` | `CONFIG_PGTABLE_LEVELS=5`; no `la57` flag |
| xv6's fork, every page | `memx.c` | sbrk(4096) **1**; sbrk(4 MB) **1,025**; fork **1,096** = 1,028 + 2 + 65 + 1; the patch applied to a clean tree reproduced it |
| Kernel mapping | PS 5 `kernel.txt` | **65 frames**, matching the fork's decomposition |
| Linux tables | `faultcost.c` | 1 GiB mapped: `VmPTE` unchanged at 44 kB; touched: **2,096 kB**; 64 pages 1 GiB apart: **+512 kB**; 2 MiB apart: **+260 kB** |
| This CPU's TLBs | `tlbinfo.c` | leaf 2 bytes `63 03 76 ff b5 f0 c3`: 64 + 32 L1 data entries, **1,536 STLB** |
| TLB miss cost | `tlbcost.c`, median of 3 | gap between 4 KiB and 2 MiB pages **1.6 ns at 4 MiB, 17.3 ns at 2 GiB** (50.02 against 32.69 ns); +18 ns in both at 16 MiB from L3 |
| THP | `/proc/vmstat` | `thp_fault_alloc 961`, `thp_fault_fallback 72` since boot; 1.63–1.78 GiB of a 2 GiB request backed |
| PCID | `switchcost.c`, three runs | threads 2,984–3,107 ns per switch; processes 3,116–3,190 ns: **1–4%** more |
| Meltdown | `/sys/devices/system/cpu/vulnerabilities/meltdown` | `Mitigation: PTI` |
| Shootdowns | `shootdown.c`, two runs | single 5,897 / 5,900 ns; **busy second thread 6,570 / 7,093 ns with 199,977 / 196,079 interrupts**; sleeping 6,089 / 6,598 ns with 41 / 939 |
| First touch | `faultcost.c`, three runs | **1,833 / 1,949 / 1,935 ns per fault**; second pass 14.7 / 13.3 / 15.2 ns per page |
| Zero page, COW, soft-dirty, pageout | `pmlab.c`, three runs each | fault columns identical every run; outputs quoted in L18 §3–§4 and Lab 5 Solutions |
| COW cost | `forkcost.c`, two runs | fork of 1 GiB **18.9 / 20.9 ms**; child writes 775 / 780 ms, **2,957 / 2,975 ns per fault** |
| xv6 faults | `pgfault.c` | past the end **err 6**; guard and kernel **err 7**; **a write over `main` succeeds** |
| Buddy allocator | `buddy.c` | 512 MiB touched: order 9 **136 → 7**, order 10 **105 → 47**; after `munmap` 138 and **89** |
| Pageout read-back | `pmlab` with majors weighted 1,000 | `faults 1`, three runs: **minor** — the swap cache |
| Hidden frames | `pmwalk.c` | 0 nonzero frame numbers; swap type and offset 0; pid 1 `Permission denied`; `pipewire` (same user, not a descendant) readable |
| `calloc` of 100 MiB | a Lab 5 check program | read **25,600 faults, RSS +0**; write 25,600 faults, **RSS +102,400 kB** |
| TLB-size cliff | PS 5 reference, `TLBSIZE` 64–513 | column-order matrix **0.00% at 511, 99.80% at 512** |

---

## 39. Four Week 5 programs measured nothing on their first run, and one lecture was drafted before its run

**Recorded together, because they are the same mistake**: a measurement written without asking
what the compiler or the kernel would do with it.

- **`pmprobe`'s "read" of an untouched page showed not present.** At `-O2` the read into an unused
  local was deleted. **`volatile` fixed it**, and the corrected run found the zero page (L18 §3).
- **`tlbcost` first printed `0.00 ns` for every working set**: its sum was never used, so the whole
  read loop was deleted. **The next version printed times but a zero checksum**, because every page
  was filled with `(char)i` for `i` a multiple of 4,096 — always 0. **Only the third version is
  quoted.**
- **`pgfault` first computed its "guard" address one page too low**, inside the program's own code,
  and the write succeeded. **Its second version wrote `*p = *p`** and every case "succeeded", because
  the compiler removed the self-assignment. **The third version writes `1`.**
- **L18 §2's xv6 transcript was first written from what the run was expected to print, before the
  run.** The run then disagreed in `eip` and in the guard case, and **the section was replaced with
  the measured output**, adding the fourth case — xv6's writable text — that the correct run
  revealed. **No lecture text is to be drafted ahead of its measurement again**; this is the rule
  §22 already stated for questions.

---

## 40. `pmlab`'s fault counts were counting the wrong pages

The first `pmlab` reported fault counts between steps. They included **faults on pages it was not
watching**: the first call into a libc function whose code page this process had not yet mapped;
printing; **after `fork`, the parent's and child's own stack and `.bss` pages, which `fork` had made
copy-on-write**; and after `clear_refs`, **every page of the process**, since clearing soft-dirty
write-protects them all. One step showed `faults +-151`: the child's counter starts at zero.

**The fix measures each operation alone** and takes the unrelated faults — writing the `sink`
variable — before measuring. **Lab 5 Q8 has students delete one of those lines** and explain the
fault that appears, because the pollution is itself the best demonstration that `fork`
write-protects everything.

---

## 41. PS 5's first `kernel.txt` guessed where xv6's data segment starts

The trace was first written with the data segment at `0x8010b000`. **`nm kernel` on the Week 5 build
puts `data` at `0x80108000`.** The frame count was 65 either way — the ranges are contiguous — but
the page counts in the trace were wrong, and were corrected.

**The PS 5 reference was then extended with superpages (Q5)** after the traces had been run; all
five earlier traces were rerun against the old binary and produced **byte-identical output** before
the new question was written.

**Q3(c)'s cliff was found by running, not predicted**: the question first asked for 64, 256 and 512
entries; the run at 511 showed that a TLB one entry smaller than a cyclic working set gets no hits
at all, and the question now includes 511 and 513.

---

## 42. The xv6 patch first included the Makefile

`nfree.patch` was first generated with `git diff` over the whole tree, **which included Lab 0's two
Makefile changes and the `_memx` line**, and failed to apply to a tree where Lab 0's changes already
existed. **The shipped patch covers only the seven kernel and library files**; `_memx` and `_pgfault`
are added with the same `sed` as every other xv6 program in the course. It was applied to a fresh
clone with Lab 0's changes and reproduced `memx`'s numbers exactly.

---

## 43. Claims the Week 5 drafts made without a measurement, and what replaced them

- **"Copying the gigabyte at fork would take longer than 780 ms"** (L18 §4) was never measured; it was
  replaced with what was: the copy is deferred, and a child that writes every page pays 780 ms.
- **"The stack sits more than 128 TiB above zero"**: `0x7ffd…` is just below 2⁴⁷. "Nearly".
- **L16 §5 counted the page directory twice**, once in the process's 12 KiB and once in the kernel's
  260 KiB. Now 8 KiB and 256 KiB, with the directory separate.
- **Lab 5 Q12 was drafted expecting a major fault** on reading back a paged-out page. Measured, it is
  minor — the swap cache still held the frame — and the question now asks which, and why.
- **The sleeping-thread shootdown rounds were 3–12% slower than single-threaded, with no
  interrupts.** No explanation was verified, and L17 §6 says so rather than offering one.

---

## 44. Every number in Week 6 was measured, and the programs ship with the notes

Kernel 7.0.0-31, reference machine of §9, **4 GiB swap file on NVMe**, `swappiness` 60, `zswap` off,
transparent huge pages `madvise`, `systemd 255` with `systemd-oomd` active. Programs in
`CS202 Week6/resources/`, `lab/` and `assignments/ps6/`; the simulator reference in
`solutions_instructor/`.

| Claim | Program | Result |
|---|---|---|
| xv6 refuses | `memhog.c` (needs Week 5's `nfree.patch`) | `allocuvm out of memory`; **sbrk refused after 56,735 pages**; `fork` −1; shell survives; pages returned |
| Major fault cost | `thrash.c` in a scope | 224 MiB limit: 344,720 reads, 44,483 major faults in 4 s; 64 MiB: 58,160 reads, 43,836 — **≈ 90 µs either way** |
| Pressure | `thrash.c` reading its cgroup's `memory.pressure` and `io.pressure` | memory **5.5–6.1%**, io **14.2–18.2%** |
| Thrashing curve | `thrash.c`, 256 MiB, 4 s | unlimited **21.7M reads/s**; 256 MiB **1.23M**; 224 MiB 76,276; 192 MiB 42,178; 128 MiB 22,724; **64 MiB 14,775** |
| Locality beats capacity | `thrash.c … hot` | at the 64 MiB limit **166,745 reads/s against 14,775 — 11×** |
| Working set | `wss.c` | 257 MiB resident; **Referenced 65,652 kB after reading 64 MiB, 16,436 kB after writing 16 MiB** |
| Textbook string | `pagesim` | 3 frames: **FIFO 15, LRU 12, Clock 14, OPT 9** — matches Silberschatz §10.4 |
| Belady's anomaly | `pagesim` on `belady.txt` | FIFO **9 → 10**, **Clock 9 → 10**; LRU 10 → 8; OPT 7 → 6 |
| Locality curve | `gentrace 1000 50 90 10 10000 1` | at 60 frames FIFO 27,747, LRU 16,518, Clock 19,906, OPT 8,933 |
| Aging | `pagesim -t` at 60 frames | tick 1 **77,321**; 8: 52,250 / 23,150; 100: 33,205 / **14,460**; 1,000: **80,799** / 16,381; 10,000: 88,561 / 16,518 |
| Real traces | `valgrind --tool=lackey` + `lackey2pages.c` | `sort -n` 2,000 numbers: 2,121,880 accesses → **1,031,795 references, 387 pages**; `ls /usr/bin`: 7,118,108 → 2,390,544, 302 pages |
| Clock against LRU | `pagesim` on those traces | within **10% from 32 frames up** on both |
| Overcommit | `overcommit.c` | single mapping **11 GiB ok, 12 GiB refused** (RAM+swap 11.5 GiB); `MAP_NORESERVE` always ok; **8,000 GiB accepted in 8 GiB pieces**, `Committed_AS` 7.8 TiB |
| `RLIMIT_AS` | `overcommit.c limit` | 256 MiB → **252** 1 MiB allocations; 1 GiB → 1,017 |
| Badness | `oomscore.c` | **⅔ point per point of adj; 6.7 points per 1% of RAM+swap**; adj floor **100** (`user@.service` `OOMScoreAdjust=100`) |
| Who dies | `/proc/*/oom_score` | Chrome renderers, **adj 300, scores 875–888**; kernel threads 0 |
| A kill | `hog` in a 64 MiB scope | killed at **48 MiB**, status **137**, `max 41 oom 1 oom_kill 1`, peak exactly 64 MiB; with 32 MiB swap, 80 MiB; with swap unlimited, 128 MiB in 0.12 s |
| `OOMPolicy` | the same scope without `-p OOMPolicy=continue` | the scope's shell is **`SIGTERM`ed**; `systemd-run` exits 143 |

---

## 45. PS 6's aging policy, as first specified, was worse than FIFO

The aging policy was written from the textbook rule — 8-bit counter per frame, shifted at each tick,
**a newly loaded page's counter starting at 0** — and measured at 60 frames on the locality trace it
took **80,799 faults at tick 1,000 against FIFO's 27,747.** The cause is in the rule: between ticks
every newly loaded page has counter 0, so **each fault evicts a page fetched moments earlier.**

**The fix is one comparison** — rank by the reference bit first, then the counter — and it brings the
same policy to 16,381. **Both are shipped**: `aging` is the textbook rule and `aging2` the fix, and
**PS 6 Q5 asks students to explain the collapse rather than presenting the fix as given.** The
lecture (L20 §5) describes aging and points at Q5 instead of spoiling it.

**A second measured surprise stayed in the question**: at tick 100, `aging2` beats *exact LRU*
(14,460 against 16,518), because the trace mixes a working set with uniform noise and aging counts
frequency as well as recency. **Q5(c) asks for that explanation.**

---

## 46. Week 6's experiments can kill the session, and the lab says so

`systemd-oomd` is **active** and monitors `user@1000.service` at a **50% memory-pressure limit over
20 s**; the memory controller is delegated to the user, so `systemd-run --user --scope -p MemoryMax=`
works without root. **Every out-of-memory and thrashing experiment in Week 6 runs inside such a
scope, and every run is seconds long.** An unconfined `hog` would have the kernel reclaim from the
whole machine, and `oomd` would then kill the student's desktop.

**Two mechanisms were found by running, not by reading**:

- **systemd's default `OOMPolicy=stop` terminates the rest of the unit** after the kernel kills one
  process in it — so the first scope experiments printed nothing but "Terminated". The lab passes
  `-p OOMPolicy=continue` and **Q7 makes the default the lesson.**
- **`memory.pressure` stays low while a process thrashes** (5.5–6.1%), because it counts reclaim
  work; the waiting shows up in **`io.pressure` (14–18%)**. L19 §4 states both, rather than the
  textbook claim that memory pressure measures thrashing.

---

## 47. The OOM score's scale is not explained, and the notes say so

`oom_score` was measured as **⅔ × (1000 + adj + 1000 × RSS ÷ (RAM + swap))** — the two slopes are
exact to three digits over four points each. **Why a process holding nothing scores 733 rather than
0 was not established**, and L21 §5 says so in one sentence rather than inventing a mechanism. **What
the killer compares is the ordering**, and the ordering is by memory held, adjusted — which is what
the lecture and Lab 6 Q8 teach.

**The curriculum's own description of badness** — "inversely proportional to niceness and runtime" —
is Linux's **pre-2.6.36** heuristic, removed in 2010. Recorded as a syllabus deviation, with the old
rule kept as history.

---

## 48. Two Week 6 mistakes worth not repeating

- **A 200,000-line `sort` traced under valgrind wrote a 10.35 GB log**, and was still writing when it
  was noticed. **`valgrind --tool=lackey` costs about 15 bytes per memory access**; PS 6 tells
  students to trace something small, and the reference trace is `sort -n` of **2,000** numbers
  (114 MB of log, 6.2 MB of page references). **No trace is shipped in the vault** — the converter
  and the instructions are, because even the small one is megabytes.
- **`pkill -f "valgrind --tool=lackey"` killed the shell that ran it**, because the pattern matched
  that shell's own command line; the valgrind survived, kept writing to a log that had already been
  unlinked, and was only stopped later by PID. **Match by process name, or check the PID first.**

---

*Academic Registry · Build Records · © CSE Department*
