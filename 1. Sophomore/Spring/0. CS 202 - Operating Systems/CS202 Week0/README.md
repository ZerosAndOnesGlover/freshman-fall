# CS 202 · Operating Systems
## Week 0: What Is an Operating System?

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 201, PROG 201
**Assessment for this course (overall):** Problem Sets 30%, Projects 30%, Midterms 25%, Final 15%
**This week's deliverables:** Lab 0 and PS 0. **No quiz** — Quiz 1, in Week 1, covers this week.

> **Week 0 is ten teaching days long**, running Jan 12 to Jan 23. It absorbs registration and
> add/drop, and Week 1 — when graded work begins — opens Jan 26. You get all three lectures and
> the lab: **Wednesday, Friday, and the following Wednesday**, with **Lab 0 on the closing Friday
> morning**.

---

### Why This Week Exists

Because PROG 201 taught you to ask the kernel for things, and you have never seen the kernel say no.

**CS 202 is the other side of every system call you made last term.** Over thirteen weeks you will write the pieces that PROG 201 called: a scheduler, a lock, a page table, a filesystem, a journal, a driver, a hypervisor. Most of them go into **xv6**, a teaching kernel small enough to read in full, which you build and boot for the first time on Friday.

This week is the foundation under all of them: **what makes the kernel different from any other program.** Not that it is bigger or cleverer — that the **CPU itself** will refuse to let any other program do what the kernel does. By Friday you will have written a kernel of your own, about forty lines of C, that runs with nothing underneath it and prints *Hello*.

It also sets the habit the course is graded on: **a protection that is switched on is not the same as a protection that works.** L02 has the first case, and it is on the machine in front of you.

---

### Learning Objectives

By the end of Week 0, you should be able to:

1. State the three jobs of an operating system, and say which one the other two depend on.
2. **Measure the illusion** on a running machine: threads against CPUs, address space against RAM, context switches on an idle desktop.
3. Tell the history of operating systems as problems and the mechanisms that solved them, and say which problem each mechanism created.
4. Distinguish mechanism from policy, and the kernel from the operating system.
5. Explain why protection must be enforced by the CPU and not by the kernel.
6. **Read the CPL from `CS`**, and say what it is in a user program and in a kernel.
7. Predict which instructions fault in ring 3, **and which of those rules the kernel itself sets** — and demonstrate one with `prctl`.
8. Explain what the U/S bit, SMEP and SMAP each prevent, and what Meltdown did to the first.
9. **List what the `SYSCALL` instruction does and does not do**, and explain the `r10` in the system-call convention.
10. Use `strace` to see the system calls a program makes, and say why not to time anything under it.
11. **Say what a system call costs on your machine**, why a nonexistent one costs almost as much, and what the vDSO avoids.
12. Trace a system call through xv6 from the user stub to `sys_getpid` and back, naming every file.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L01 What an Operating System Is For]] | Referee, illusionist, guard; **1,425 threads on 8 CPUs, 24,353 GiB of address space on 7.5 GiB**; history as problems; mechanism and policy; kernel against OS; why xv6 |
| [[L02 Two Modes and the Wall Between Them]] | Limited direct execution; **`CS = 0x33`**; six instructions that kill a ring-3 program; **`rdtsc` made to fault with one `prctl`**; UMIP compiled in and absent; the U/S bit, SMEP, SMAP, Meltdown; **xv6's one open gate** |
| [[L03 System Calls and the Trap]] | `SYSCALL` step by step; `strace`; **590 ns per crossing, 572 for a call that does not exist, 18.5 through the vDSO**; 14.2 s against 2.2 ms for one file; two syscall tables; xv6's `getpid` end to end |
| [[LAB 0 A Kernel That Prints Hello]] | `strace`, ring 3's refusals, a kernel of your own, and xv6 built and booted. **Friday of Week 0, morning** |
| `lab/Makefile`, `lab/boot.S`, `lab/kernel.c`, `lab/link.ld`, `lab/int13.c` | The kernel skeleton, and one xv6 user program |
| [[CS202 Week0/assignments/Problem Set 0\|Problem Set 0]] | Five questions, 100 points, due **Friday of Week 1** |
| [[CS202 Week0/resources/Course Overview Syllabus\|Course Overview Syllabus]] | **Read this in full in Week 0** — assessment, the lab lag, the two projects, which xv6, deviations |
| [[CS202 Week0/resources/Reading Guide Week 0\|Reading Guide Week 0]] | Which of OSTEP 1–6 is this week, and which is Week 1 |
| `resources/*.c` | Every program whose output appears in the lectures, with its build line |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**The kernel is not special because of what it is. It is special because of where the CPU lets it run.**

Your Lab 0 kernel and `privfault.c` both execute `outb`. In one, a character appears on the serial port. In the other, the process is killed. **The instruction, the bytes and the port are identical; the only difference is two bits in `CS`.** Everything an operating system guarantees — that a program cannot freeze the machine, read another program's memory, or write the disk behind the filesystem's back — comes down to the CPU checking those bits on every instruction, and to the kernel being the only code that ever runs with them clear.

**And every entry into that code has a price.** 590 nanoseconds is nothing once and fourteen seconds sixteen million times. **Weeks 1–12 are thirteen answers to the same question — how do you get the kernel's protection while crossing into it as rarely as possible?** — and you will recognise the question in every one of them.

---

### Assessment Reminder

**Labs and quizzes carry no weight.** The curriculum's assessment line sums to 100% without them, and no percentage has been invented to fill the gap.

They are still required. **The lab is checked off by the TA in the session**, and a second unexcused absence costs a letter grade. **Quiz *N* covers Week *N−1***, runs ten minutes at the start of **Monday's** lecture in Weeks 1–11, and prints its own answer key.

> **This course's lab lags a week, because the lab is on Tuesday and the lectures are Monday,
> Wednesday and Friday.** Lab *N* covers Week *N* and is sat on the **Tuesday of Week *N+1***.
> Lab 0 is the exception: it is sat on the **Friday that closes Week 0, 10:00–11:50 in BH 210**,
> after all three lectures. **There is no lab in Week 1.**

Both are tracked in [[_CS 202 Lab and Quiz Record]].

---

### Connections

**Back:** **CS 201 is assumed and not re-taught.** Its Week 6 page tables are L02 §6's U/S bit; its x86-64 calling convention is L03 §2's reason for `r10`; its exceptions are L02 §3's `#GP`. **PROG 201 is assumed too** — every system call in PS 0 is one you made last term, and the stdio-before-`fork` bug from its L01 §6 turned up in this week's own measurement code.

**Sideways:** **PROG 202, CS 212, MATH 251, ECE 211 and CS 290 run alongside.** MATH 251's Week 0 — sample spaces and events — is the start of the tool Week 2 uses to reason about scheduling, and Week 11 uses to reason about failure.

**Forward:** **Week 1 is the process** — what the kernel saves when it takes the CPU away, which is the register list from L03 §2 used for a different purpose. **Lab 0's xv6 is where Project 1 happens in Week 7**, so build it cleanly now. **Week 10's hypervisor boots Lab 0's kernel**, with you as the machine instead of QEMU. **Week 12's `seccomp`** is a filter on the syscall numbers from L03 §5.

---

*CS 202 · Week 0 · © CSE Department*
