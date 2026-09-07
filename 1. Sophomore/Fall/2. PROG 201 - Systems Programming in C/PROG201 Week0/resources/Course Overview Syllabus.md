# PROG 201 · Systems Programming in C
## Course Overview & Week-by-Week Road-map
### Year 2 · Fall · 4 credits (3 lecture + 1 lab)

---

## The Course

**PROG 201 is about the programs that ask the operating system for things.**

PROG 101 taught you C as a language: types, pointers, arrays, the standard library. This course spends thirteen weeks on the other half of the manual — **section 2, the system calls** — and on what the kernel does when you make one. You will write a shell, a concurrent web server, an allocator, a JIT, and a container, each of them a program that cannot be written without asking the kernel for something no library can fake.

By the end you will be able to answer, mechanically: **what happens between `fork()` returning twice and the child's first instruction; why your server stops accepting connections at ten thousand clients; what a file descriptor actually indexes; and why a `printf()` inside a signal handler is a bug even when it works.**

**Prerequisites:** PROG 101, and CS 201 as a co-requisite. CS 201 runs alongside this course and supplies the machine: the address space, the stack, the calling convention. This course supplies the kernel's half of the same picture. Neither re-teaches the other.

---

## Two Habits This Course Is Built Around

**1. The man page is the specification. The machine is the evidence.**

`man 2 fork` is the contract. What your kernel does with it is a fact you can measure, and the two are not always the same thing — POSIX permits latitude that Linux resolves in one particular way, and your program has to survive both.

> **Every number in these notes was produced by a command, and the command is printed next to it.**
> Where the measurement contradicts the textbook, the measurement is shown *and* the textbook's
> claim is kept, because you will meet both. Week 0's L02 has an example: APUE says an orphan is
> adopted by `init`, PID 1. On the lab machines it is adopted by PID 257510.

**2. Every system call can fail, and the failure is the interesting half.**

`fork()` returns `-1` when the process table is full. `read()` returns `-1` with `EINTR` when a signal lands mid-call. `write()` on a socket returns *fewer bytes than you asked it to write* — not as an error, as its normal behaviour. **Code that ignores return values is not shorter than code that checks them; it is a different program, one whose failure mode is silent corruption.**

The habit this course drills: read the RETURN VALUE and ERRORS sections of the man page *before* you write the call, and decide what each listed errno means for your program. Half of them mean "retry", and the half that do not are the ones that matter.

---

## Assessment

| Component | Weight | Rule |
|---|---|---|
| **Problem Sets** | **35%** | PS 0–12, released Wednesday, due the following Friday 17:00. Lowest 1 dropped. |
| **Midterm 1** *(Week 4)* | **12.5%** | 90 minutes, covering **Weeks 0–3**. One handwritten sheet, one side. |
| **Midterm 2** *(Week 8)* | **12.5%** | 90 minutes, covering **Weeks 4–7**. Same format. |
| **Project 1** *(due Week 9)* | **12.5%** | `tsh` — a shell with pipelines, redirection and job control. |
| **Project 2** *(due Week 12)* | **12.5%** | A networked, multi-threaded server. |
| **Final Exam** | **15%** | 150 minutes, comprehensive. Two handwritten pages. |
| **Total** | **100%** | |

**Labs and quizzes carry no weight.** The curriculum's assessment line — *Problem Sets 35%, Projects 25%, Midterms 25%, Final 15%* — sums to 100% without them, and no percentage has been invented to fill the gap. This is the same rule every Year 2 course follows, and the ECE 110 and CS 102 precedent from Year 1.

**They are still required.** The lab is checked off by the TA in the session, and [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second unexcused absence.

**Quizzes** run ten minutes at the start of **Tuesday's** lecture — this course's first lecture of the week — in **Weeks 1–11**. **Quiz *N* covers Week *N−1*.** The answer key is printed in the paper, below the questions.

Both are recorded in [[_PROG 201 Lab and Quiz Record]].

---

## Schedule

| | When | Where |
|---|---|---|
| **Lectures** | Tuesday, Wednesday, Thursday 10:00–10:50 | TH 200 |
| **Lab** | Monday 15:00–16:50 *(mandatory)* | BH 215 |
| **Office hours** | Tuesday 13:00–15:00, Thursday 15:00–16:30 | TH 418 |

### The lab runs a week behind the lectures, because Monday comes first

**Lab *N* covers Week *N* and is sat on the Monday of Week *N+1*.**

This is forced, not chosen. The lectures are Tuesday, Wednesday and Thursday; the lab is **Monday**, which is before all three of them. A lab sat on the Monday of Week *N* would have had **none** of Week *N*'s lectures. So it lags by a week, and the lag is a full one.

| Lab | Covers | Sat on |
|---|---|---|
| **Lab 0** | Week 0 | **Friday of Week 0, 17:00–18:50** — the Friday that closes the ten-day week, after all three lectures. Late because CS 201 and CS 211 hold theirs the same afternoon |
| Lab 1 | Week 1 | Monday of Week 2 |
| Lab *N* | Week *N* | Monday of Week *N+1* |
| **Lab 5** | Week 5 | **Friday of Week 6, 16:00–17:50** — its Monday is Fall Break. See *Deviations* |
| Lab 11 | Week 11 | Monday of Week 12 |
| **Lab 12** | Week 12 | **Demo day**, Monday of the completion period |

**There is no lab session in Week 1.** Lab 0 was sat on the Friday before it, and Lab 1 is waiting for Week 1's lectures to happen.

**Quizzes do not lag.** Quiz *N* is sat at the start of **Tuesday's lecture in Week *N*** and covers **Week *N−1***. Every lab and quiz file states its day *and* its week in the header; the file is authoritative if you are ever unsure.

> **CS 201's lab lags too, and CS 211's does not.** All three courses run this term and they disagree,
> because CS 211's lab is a Friday and has all of its week's teaching behind it. Read each course's
> own header rather than carrying a habit between them.

**Instructor:** Prof. Nadia Petrov · n.petrov@ist.edu · TH 418
**TA:** Aisha Mohammed · amohammed@ist.edu · Mon 17:00–18:00 and Thu 11:00–13:00, BH 215; Fri 16:00–18:00, BH 120

---

## Tools

Everything runs on Linux — **Ubuntu 24.04 LTS in BH 215**, GCC 13.3.0, glibc 2.39, kernel 7.0.

| Tool | For | Preinstalled? |
|---|---|---|
| `gcc` | compiling; `-Wall -Wextra` is not optional in this course | ✅ 13.3.0 |
| `man` | sections 2 and 3, constantly. `man 2 fork`, `man 7 signal-safety` | ✅ |
| `strace` | seeing the system calls a program actually made (Weeks 0–2, 8) | ✅ |
| `gdb` | `set follow-fork-mode child` is the flag you will want in Week 0 | ✅ |
| `valgrind` | `memcheck` from Week 4, `helgrind` for data races in Week 3 | ✅ |
| `perf` | Week 9, and honestly from Week 5 onwards | ✅ |
| `ltrace`, `readelf`, `nm`, `objdump` | Week 8, dynamic linking | ✅ |
| `ab` (apache2-utils) | Week 5, stress-testing your own server | ⚠️ `sudo apt install apache2-utils` |
| `afl++` | Week 10, fuzzing | ⚠️ installed in BH 215 only |

**`strace` is the single most useful tool in this course.** When a program does not do what you expect, `strace -f ./prog` prints every system call it made, in order, with arguments and return values — including the one that returned `-1` and the one you never made.

---

## Textbooks

**Stevens, W.R. & Rago, S. — *Advanced Programming in the UNIX Environment*, 3rd ed. (Addison-Wesley, 2013).**
*Primary text — "APUE". The definitive reference for the POSIX API. Written against a portable Unix rather than against Linux specifically, which is exactly what makes it worth reading: it tells you which of Linux's behaviours you are allowed to rely on.*

**Kerrisk, M. — *The Linux Programming Interface* (No Starch Press, 2010) — "TLPI".**
*Secondary, and the better book when the answer is Linux-specific. 1,500 pages; nobody reads it front to back. Learn to find things in it.*

**Bryant, R. & O'Hallaron, D. — *Computer Systems: A Programmer's Perspective*, 3rd ed.**
*Chapters 8–12 are this course from CS 201's side of the fence. You already own it for CS 201.*

**The man pages.** `man 2 <syscall>` is the first reference for everything in this course, and `man 7 signal-safety`, `man 7 pipe`, `man 7 socket` and `man 7 credentials` are worth reading end to end.

---

## Week by Week

| Week | Topic | The question it answers |
|---|---|---|
| **0** | The Unix Process Model | What is a process, and what does `fork()` actually copy? |
| **1** | File Descriptors and Unix I/O | What is a file descriptor a descriptor *of*? |
| **2** | Pipes, FIFOs and IPC | How do two processes share anything at all? |
| **3** | POSIX Threads | What changes when the sharing is total? |
| **4** | `mmap` and the Virtual Memory API · **MIDTERM 1** | How do you get memory without `malloc`? |
| **5** | Sockets and Concurrent Servers | Why does the server fall over at ten thousand connections? |
| **6** | The Shell — Parsing, Execution, Job Control · **Project 1 assigned** | What is a shell, mechanically? |
| **7** | Filesystems — VFS, Inodes, On-Disk Layout | Where does a file's *name* live? |
| **8** | Dynamic Linking · **MIDTERM 2** | How does `printf` get into your process? |
| **9** | Performance — Profiling in Practice · **Project 1 due** | Which 3% is worth optimising? |
| **10** | Systems Security — Attacks and Mitigations | How is a program exploited when the stack is not executable? |
| **11** | Containers and Virtualization | What is a container, if it is not a machine? |
| **12** | Synthesis — Building a Production Daemon · **Project 2 due** | What separates working code from code that runs unattended? |

---

## What This Course Feeds

**Immediately:** CS 201 runs alongside and the two interlock — its address space is this course's `mmap`, its calling convention is this course's `execve` stack layout, its cache is Week 9's roofline.

**Next term:** **CS 202 (Operating Systems) implements what this course calls.** You will have written a shell that uses `fork`; CS 202 writes the `fork`. CS 212 assumes you can build and debug a multi-process system.

**Later:** CS 302 (Networks) extends Week 5 down the stack. CS 341 (Security) extends Week 10 into exploitation and defence properly. Every systems course after this one assumes you can read a man page and write the call.

---

## Deviations From the Curriculum

Recorded here so a reader meets them without needing `5. Build Records/`:

| What | Why |
|---|---|
| **Lab 5 is sat on the Friday of Week 6, not the Monday** | This course's lab day is Monday and the Monday of Week 6 is Fall Break, so the term has twelve usable Monday slots for thirteen labs. Rather than merge two labs or drop one, Lab 5 is made up on the Friday of Week 6 at 16:00–17:50 in BH 215, after CS 211's Friday lab has vacated the building. The TA's Friday help-desk hours are covered that week too. |
| **The lab machines run Ubuntu 24.04, not the 22.04 the curriculum names** | BH 215 was reimaged with the same build as BH 210 so that CS 201 and PROG 201 share a toolchain. Everything in the curriculum works unchanged; the visible differences are glibc 2.39 rather than 2.35 and GCC 13 rather than 11. **Where a measurement in these notes depends on the glibc version, it says so.** |
| **Labs and quizzes are unweighted** | The curriculum's four components already reach 100%. Required, recorded, unmarked — the Year 2 rule. |
| **Lab 0 is sat at 17:00 on the Friday of Week 0** | Every Year 2 course puts its Week 0 lab on that Friday, and BH 220 (CS 211, 14:00–15:50) and BH 210 (CS 201, 15:00–16:50) already hold the afternoon. 17:00–18:50 is the first window that clashes with neither. It applies to Lab 0 only. The TA's Friday help-desk hours in BH 120 are covered by CS 201's TA that week. |
| **Week 2's lectures contradict the curriculum on shared memory** | The curriculum's Week 2 Core Concept states that "shared memory is the fastest IPC mechanism". Measured on the lab machines, a one-slot shared-memory ring moves bulk data **six times slower than a pipe** at 4 KB per message and makes the same number of system calls; it wins by 2.3× at 64 KB and 5.8× at 256 KB. L09 §5–§6 states the claim, measures it, and gives the condition under which it is true. The claim is not removed — the disagreement is the lesson. |
| **Week 10's ROP work is done in a sandbox with ASLR disabled per-process** | The curriculum sets "build a working ROP chain exploit". It is built against a deliberately vulnerable binary supplied by the course, run under `setarch -R`, and nothing in the assessed work involves a program you did not receive from us. |

---

*PROG 201 · Year 2 Fall · © CSE Department*
