# CS 202 · Operating Systems
## Course Overview & Week-by-Week Road-map
### Year 2 · Spring · 4 credits (3 lecture + 1 lab)

---

## The Course

**CS 202 is the other side of the system call.**

PROG 201 spent a term on programs that ask the kernel for things: `fork`, `mmap`, `read`, `accept`. This course spends thirteen weeks inside the kernel that answers — **how it takes the CPU away from one process and gives it to another, how it stops two threads corrupting the same data, how it makes 7.5 GiB of RAM look like terabytes, how it keeps a file intact through a power cut, and how it lets a whole operating system run as a process.**

Most of it you will write. The curriculum's project is **xv6**, MIT's teaching kernel — about six thousand lines of kernel, small enough to read in full — and you will extend it with system calls, a scheduler, and memory and filesystem features across two projects.

By the end you will be able to answer, mechanically: **what the CPU does in the nanoseconds between `syscall` and the kernel's first instruction; why a lock that is correct on one core deadlocks on two; why a program that uses 1% more memory than the machine has can run a thousand times slower; and what exactly `fsync` promised you.**

**Prerequisites:** CS 201 and PROG 201. CS 201 supplied the machine — the address space, the page table, the calling convention, the exception. PROG 201 supplied the interface — every system call this course implements, you have called. Neither is re-taught.

---

## Two Habits This Course Is Built Around

**1. A protection that is switched on is not a protection that works.**

Operating systems are full of mechanisms that are configured, compiled in, or documented, and that do not operate on the machine in front of you — because the CPU lacks a feature, a sysctl is set, or a permission is missing. **Nothing reports the gap.** No call fails and no warning is printed.

> **Every protection claim in these notes was tested by trying to break it, and the command is
> printed next to the result.** Week 0's L02 has the first case: the reference machine's kernel is
> built with `CONFIG_X86_UMIP=y`, the CPU has no UMIP, and an ordinary program read a kernel
> address with one instruction.

**2. Every abstraction has a price, and the price is a number.**

A system call, a context switch, a TLB miss, a page fault, an `fsync`, a VM exit — each is an entry into more privileged code, and each costs something you can measure. **An operating system is a set of answers to the question "how do I give programs this guarantee while paying for it as rarely as possible?"**, and you cannot judge an answer without the number.

The habit this course drills: **when a design decision is justified by performance, find the measurement.** When there is none, make one. When you cannot — because a student account cannot reboot a shared machine, or load a module, or see physical addresses — **say so, and say what the measurement would be.**

---

## Assessment

| Component | Weight | Rule |
|---|---|---|
| **Problem Sets** | **30%** | PS 0–12, released Wednesday, due the following Friday 17:00. **Lowest 1 dropped.** |
| **Midterm 1** *(Week 4, Monday)* | **12.5%** | 18:00–19:15, **VNC 100**, covering **Weeks 0–3**. One handwritten sheet, one side. |
| **Midterm 2** *(Week 8, Monday)* | **12.5%** | 18:00–19:15, **VNC 100**, covering **Weeks 4–7**. Same format. |
| **Project 1** *(assigned Week 7, due Week 11)* | **15%** | **xv6 kernel features** — system calls, a scheduler, and the locks they need. |
| **Project 2** *(assigned Week 9, due completion period)* | **15%** | **A small OS kernel** — xv6 with memory-management and filesystem features added to your Project 1. |
| **Final Exam** | **15%** | Wednesday of finals week, 09:00–11:30, comprehensive. Two handwritten pages. |
| **Total** | **100%** | |

**Labs and quizzes carry no weight.** The curriculum's assessment line — *Problem Sets 30%, Projects 30%, Midterms 25%, Final 15%* — sums to 100% without them, and no percentage has been invented to fill the gap. This is the rule every Year 2 course follows.

**They are still required.** The lab is checked off by the TA in the session, and [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second unexcused absence.

**Quizzes** run ten minutes at the start of **Monday's** lecture — this course's first lecture of the week — in **Weeks 1–11**. **Quiz *N* covers Week *N−1*.** The answer key is printed in the paper, below the questions.

Both are recorded in [[_CS 202 Lab and Quiz Record]].

---

## Schedule

| | When | Where |
|---|---|---|
| **Lectures** | Monday, Wednesday, Friday 09:00–09:50 | VNC 101 |
| **Lab** | Tuesday 15:00–16:50 *(mandatory)* | BH 210 |
| **Midterms** | Monday of Weeks 4 and 8, 18:00–19:15 | VNC 100 |
| **Final** | Wednesday of finals week, 09:00–11:30 | VNC 100, overflow to TH 200 — **check your seat on the portal** |

**Instructor and TA: not yet listed.** The registry's [[Year2 - Sophomore/OFFICE HOURS|OFFICE HOURS]] covers the Fall courses only, and names nobody for CS 202. Nothing has been invented to fill the gap; the course portal carries the staff and their hours once assigned. Until then, the **Engineering Help Desk in BH 120** — Monday–Thursday 10:00–20:00, Friday 10:00–17:00, weekends 12:00–18:00 — is staffed for every Year 1–2 course.

### Week 0 has three lectures in six slots

Week 0 runs ten teaching days, **Jan 12 to Jan 23**, and this course's Monday, Wednesday and Friday give it six lecture slots. **The three lectures are the first Wednesday, the first Friday, and the second Wednesday.** Every lecture file states its day in the header. From Week 1 the pattern is the ordinary Monday, Wednesday, Friday.

### The lab runs a week behind the lectures, because Tuesday comes early

**Lab *N* covers Week *N* and is sat on the Tuesday of Week *N+1*.**

This is forced, not chosen. The lectures are Monday, Wednesday and Friday; the lab is **Tuesday**, which has only Monday's lecture behind it. A lab sat on the Tuesday of Week *N* would be missing two thirds of Week *N*. So it lags by a week.

| Lab | Covers | Sat on |
|---|---|---|
| **Lab 0** | Week 0 | **Friday of Week 0, 10:00–11:50**, BH 210 — the Friday that closes Week 0, after all three lectures |
| Lab 1 | Week 1 | Tuesday of Week 2 |
| Lab *N* | Week *N* | Tuesday of Week *N+1* |
| **Lab 3** | Week 3 | Tuesday of Week 4 — **the day after Midterm 1** |
| **Lab 7** | Week 7 | Tuesday of Week 8 — **the day after Midterm 2**, and the first week back from Spring Break |
| Lab 11 | Week 11 | Tuesday of Week 12 |
| **Lab 12** | Week 12 | **Demo day**, Tuesday of the completion period, 15:00–16:50 |

**There is no lab session in Week 1.** Lab 0 was sat the Friday before, and Lab 1 is waiting for Week 1's lectures to happen.

**Quizzes do not lag.** Quiz *N* is sat at the start of **Monday's lecture in Week *N*** and covers **Week *N−1***. Every lab and quiz file states its day *and* its week in the header; the file is authoritative if you are ever unsure.

> **Spring Break falls between Weeks 7 and 8**, not inside either, so no lecture, lab or quiz moves
> for it. **Problem Set 7 is released before the break and due after it**, and Midterm 2 and Quiz 8
> are both on the Monday you come back. The Week 7 and Week 8 READMEs say so again.

---

## Tools

Everything runs on Linux — **Ubuntu 24.04.4 LTS in BH 210**, kernel 7.0, GCC 13.3.0, glibc 2.39, QEMU 8.2.2. Your coursework goes in the Academic Registry, not your home directory; Lab 0 sets that up.

| Tool | For | On the lab image? |
|---|---|---|
| `gcc`, `gcc -m32`, `ld -m elf_i386` | everything; the `-m32` pair builds xv6 and Lab 0's kernel | ✅ 13.3.0 |
| `qemu-system-i386` | booting xv6 and your own kernels | ✅ 8.2.2 |
| **xv6-public** | the kernel you extend all term — see *Which xv6* | clone it in Lab 0 |
| `strace` | seeing the system calls a program actually made | ✅ |
| `gdb` | debugging xv6 through QEMU's gdb stub, and user programs. **`ptrace_scope` is 1**: gdb can run a program, but cannot attach to one it did not start | ✅ |
| `chrt`, `nice`, `taskset` | Week 2's scheduling policies | ✅ |
| `valgrind` | Week 3's data races (`helgrind`) | ✅ |
| `mkfs.ext4`, `debugfs` | Weeks 7–8 — ext4 on a disk image you own, inspected without mounting | ✅ |
| `/dev/kvm` | Week 10's hypervisor. **Your account can open it** | ✅ |
| Linux kernel headers | Week 9's character-device module | ✅ — see Week 9 for where it is loaded |
| `bpftrace` | Week 7's page-cache tracing | ⚠️ installed, **refuses to run without root** |
| `perf` | occasional | ⚠️ installed; `kernel.perf_event_paranoid` is **4** |
| ZFS, btrfs | Week 8 | ❌ not installed |
| `etcd` | Week 11 | ❌ not installed |

**The ⚠️ and ❌ rows are not oversights to be fixed by `sudo`.** A shared lab image does not give students root, and it should not. Each week whose curriculum entry needs one of them says, in its own README and in *Deviations* below, what it does instead — and, where the difference is itself instructive, **measures the refusal.**

---

## Which xv6

**This course uses [xv6-public](https://github.com/mit-pdos/xv6-public), the 32-bit x86 version, pinned at commit `eeb7b41`.**

MIT moved its own course to a RISC-V port in 2019 and no longer maintains the x86 version. It is used here for three reasons:

1. **The lab image can build and boot it.** `gcc -m32` and `qemu-system-i386` are installed; a RISC-V cross-compiler and `qemu-system-riscv64` are not, and a student account cannot install them.
2. **The curriculum names x86-64 assembly as the course language**, and this course follows CS 201's x86 year. The trap entry, the page tables and the context switch you read in xv6 are x86, like everything CS 201 taught.
3. **The ideas are the same.** Every data structure and algorithm in the RISC-V version has an x86 counterpart in this one.

**Two one-line fixes are needed, both to the `Makefile`.** Lab 0 applies them:

```bash
sed -i 's/-m32 -Werror/-m32 -Werror -Wno-error=array-bounds -Wno-error=infinite-recursion/' Makefile
sed -i 's/-smp $(CPUS)/-smp $(CPUS),sockets=$(CPUS),cores=1,threads=1/' Makefile
```

1. **GCC 13 reports two warnings** in xv6's code that older compilers did not, and xv6 treats every warning as an error. The first line demotes exactly those two and keeps `-Werror` for everything else.
2. **QEMU 8.2 makes `-smp 2` two cores in one socket**, and the firmware's multiprocessor table then lists one processor — so **xv6 boots on one CPU however many you ask for**, and nothing reports it. The second line asks for one socket per CPU, and xv6 then finds them all. **Check for `cpu1: starting 1` at boot.**

**The book to read with it is the matching x86 edition** of *xv6: a simple, Unix-like teaching operating system* (revision 11), not the current RISC-V edition. The chapter structure is similar; the code listings differ.

---

## Textbooks

**Arpaci-Dusseau, R. & Arpaci-Dusseau, A. — *Operating Systems: Three Easy Pieces* — "OSTEP".** Free at ostep.org.
*Primary text. Virtualization, concurrency, persistence, in short chapters with homework you can run. Every week's reading guide says which chapters are that week.*

**Cox, R., Kaashoek, F. & Morris, R. — *xv6: a simple, Unix-like teaching operating system*, x86 revision 11.** Free at pdos.csail.mit.edu.
*The kernel you extend, explained by its authors, with its code. Read the chapter alongside the source files it names.*

**Silberschatz, A., Galvin, P. & Gagne, G. — *Operating System Concepts*, 10th ed. — "the dinosaur book".**
*Comprehensive reference. When OSTEP is brief on a topic — real-time scheduling, the Banker's algorithm — this is where to look.*

**Love, R. — *Linux Kernel Development*, 3rd ed.**
*How Linux implements what OSTEP describes. Written against Linux 2.6.34, so specific function names have moved; the structures have mostly not.*

---

## Week by Week

| Week | Topic | Lab | The question it answers |
|---|---|---|---|
| **0** | What Is an Operating System? | strace; a kernel that prints Hello; xv6 | What makes the kernel different from any other program? |
| **1** | Processes and Process Management | `/proc/<pid>/maps` and `status` | What does the kernel save when it takes the CPU away? |
| **2** | CPU Scheduling | `chrt` and `nice` | Which of 1,425 threads runs next, and who decided? |
| **3** | Synchronization: Locks and Condition Variables · **Midterm 1 announced** | a `futex` lock | How do two threads share one variable safely — and cheaply? |
| **4** | Deadlock · **MIDTERM 1** | reproduce a deadlock; find it with gdb | When can locking go wrong without any bug in any one lock? |
| **5** | Memory Management: Physical and Virtual | `/proc/<pid>/pagemap` | How does an address become a physical frame? |
| **6** | Page Replacement and Swapping | the OOM killer and overcommit | What happens when memory runs out? |
| **7** | File Systems I: Design and Implementation · **Project 1 assigned** | the page cache | Where does a file's data actually live, and when is it safe? |
| — | *Spring Break* | | |
| **8** | File Systems II: Crash Consistency and Modern Designs · **MIDTERM 2** | snapshots and their cost | What survives a crash in the middle of a write? |
| **9** | I/O and Device Drivers · **Project 2 assigned** | a character-device module | How does `read` reach a device the kernel has never heard of? |
| **10** | Virtualization | boot a VM in your own hypervisor | How does an operating system run as a process? |
| **11** | Distributed Systems Concepts · **Project 1 due** | Raft, observed | How do five unreliable machines agree? |
| **12** | OS Security and Course Synthesis | demo day *(completion period)* | What is the smallest set of privileges a program can run with? |
| **Completion** | **Project 2 due** Friday | Lab 12 demo day, Tuesday | |
| **Finals** | **Final Exam**, Wednesday | | |

---

## What This Course Feeds

**Immediately:** **CS 212** assumes you can reason about a multi-process system and its failure modes. **PROG 202** runs alongside — its immutable data structures are Week 3's locking problem avoided by construction.

**Later:** **CS 341 (Security)** starts from Week 0's wall and Week 12's sandbox. **CS 302 (Networks)** extends Week 9's driver model to the network stack and Week 11's partitions to real ones. Every systems course after this one assumes you know what a system call costs and what the kernel does with a page fault.

---

## Deviations From the Curriculum

Recorded here so a reader meets them without needing `5. Build Records/`:

| What | Why |
|---|---|
| **xv6 is the x86 version, not the RISC-V version** | The lab image has `gcc -m32` and `qemu-system-i386` and no RISC-V toolchain, and the curriculum names x86-64 assembly as the course language. See *Which xv6*. Two one-line `Makefile` changes are applied and nothing else in xv6 is modified: the two GCC 13 warnings xv6 fails on are demoted from errors, and QEMU is asked for one socket per CPU, **without which xv6 silently boots on one CPU** under QEMU 8.2. The second fix was found while building Week 1, after Week 0 had shipped with only the first; Lab 0 now carries both. |
| **Labs and quizzes are unweighted** | The curriculum's four components already reach 100%. Required, recorded, unmarked — the Year 2 rule. |
| **Project 2 is due in the completion period, and the final is in finals week** | The curriculum lists "FINAL EXAM" and "Project 2 due" in Week 12's assignment list. The registry's [[Year2 - Sophomore/ASSESSMENT CALENDAR\|ASSESSMENT CALENDAR]] puts Project 2 on the Friday of the completion period and the final on the Wednesday of finals week, and the registry is authoritative for dates. Week 12 is an ordinary teaching week. |
| **Project 2 is assigned in Week 9** | Neither the curriculum nor the registry says when. Week 9 is the first week in which all of Project 2's material — memory (Weeks 5–6) and filesystems (Weeks 7–8) — has been taught, and it gives five weeks to the completion-period deadline, overlapping Project 1 by two. |
| **Lab 12 (demo day) is before Project 2's deadline** | The lab is the Tuesday of the completion period; the deadline is that Friday. Demo day shows the kernel as it stands and is checked off like any lab; the submission is marked, the demo is not. |
| **Week 0's lectures are on the first Wednesday, first Friday and second Wednesday; Lab 0 is Friday morning** | Week 0 has six lecture slots for three lectures. Lab 0 sits on the closing Friday like every Year 2 Week 0 lab, at 10:00–11:50, which is free for every Spring Year 2 student and leaves the afternoon — ECE 211 at 13:00 and CS 290 at 15:00 — untouched. |
| **No instructor or TA is named** | The registry lists Spring staff nowhere. The syllabus says so rather than inventing names; see *Schedule*. |
| **Week 1 teaches that Linux saves FPU state eagerly, not lazily** | The curriculum's Week 1 Core Concept says the FPU/SSE state "is saved lazily — only when the new process uses floating-point instructions, signaled by a fault". That was true of Linux once and is not now. The reference machine's own kernel headers (`arch/x86/include/asm/fpu/sched.h`) show `switch_fpu()` **saving the outgoing task's state at every switch** and deferring only the *restore* to the return to user space, with no fault involved. L05 §6 quotes the header, gives the 1,088-byte XSAVE size, and explains why lazy switching was abandoned — including the 2018 *LazyFP* disclosure. The curriculum's description is kept as history, not deleted. |
| **Week 1 shows that xv6 does not save FPU state at all** | Not a deviation from the curriculum so much as from every textbook's context switch: xv6's `swtch` and trap frame contain no FPU state, so two xv6 processes doing floating point share one x87 register. `fpu.c` measures it — two processes' answers **summing to exactly the right total** — in L05 §6, Lab 1 Q9 and PS 1 Q4, which asks students to design the fix. Nothing in xv6 is changed. |

---

*CS 202 · Year 2 Spring · © CSE Department*
