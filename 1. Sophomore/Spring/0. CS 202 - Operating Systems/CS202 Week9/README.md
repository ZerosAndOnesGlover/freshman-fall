# CS 202 · Operating Systems
## Week 9: I/O and Device Drivers

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 201, PROG 201
**Assessment for this course (overall):** Problem Sets 30%, Projects 30%, Midterms 25%, Final 15%
**This week's deliverables:** PS 8 due **Friday**, PS 9 released **Wednesday**, **Project 2 assigned Wednesday** (15%, due **Friday of the completion period**), **Quiz 9** at the start of **Monday's** lecture (covers Week 8).
**Lab 8 is sat on the Tuesday of this week; Lab 9 covers this week and is sat on the Tuesday of Week 10.**

> ### Two projects are now running at once.
> **Project 1 is due Friday of Week 11** — two weeks away, and its Week 9 checkpoint is **this week's
> lab session**: show the TA that `settickets` and `getpinfo` work. **Project 2 is assigned this
> Wednesday** and is due in the completion period. They overlap deliberately; Project 2's first part
> is short.

---

### Why This Week Exists

Because every `read()` in this course has ended somewhere, and this week is that somewhere.

**One system call reaches a file, a pipe, a terminal and a disk**, and the kernel makes that true with a table of function pointers per open file — nine lines in xv6, a page in Linux. **A driver is the code behind one of those tables**, and writing one means giving up the C library, floating point, a large stack, and the right to sleep when an interrupt is running.

**The measurements this week are about overhead.** Reaching a device that does *nothing* costs **659 ns** on this machine — the system call, not the driver. Reading 256 MiB in 4 KiB pieces costs **65,536 interrupts and 1.1 seconds**; the same bytes in 1 MiB pieces cost **1,969 interrupts and 0.14 seconds**. **The device is not the bottleneck; the way you ask it is.**

**And one thing you cannot do:** load a kernel module. It builds — 330 KB of `.ko` from a page of code — and `insmod` refuses it, because a module *is* the kernel. **So the driver you write and run is in xv6**, where the kernel is yours.

---

### Learning Objectives

By the end of Week 9, you should be able to:

1. Explain how one system call reaches many devices, and name the structure that makes it possible in **xv6** and in **Linux**.
2. Explain what a **device file** is, and what `mknod`'s major and minor numbers do.
3. **Measure the cost of a device call** and separate dispatch from the device's own work.
4. Distinguish **character** from **block** devices, and say which the page cache and block layer serve.
5. **Copy safely across the user boundary**, and describe what happens when a driver does not.
6. Explain **polling, interrupts and DMA**, and say which suits which device.
7. **Count the interrupts an I/O costs**, and explain the effect of request size and `max_sectors_kb`.
8. Explain the **multi-queue block layer** and why its default scheduler is `none`.
9. Explain why an **interrupt handler may not sleep**, and what top and bottom halves are for.
10. Write a **character driver** that blocks and wakes correctly, in xv6.
11. Build a **Linux kernel module**, read its metadata, and explain why it will not load here.
12. Name the constraints kernel code runs under, and the six bugs a first driver has.

---

### This Week's Materials

| File | Purpose |
|---|---|
| [[L28 One Interface for Every Device]] | `devsw` and `file_operations`; device files as a name and two numbers; **dispatch measured at 659 ns with a driver that does nothing**; `/dev/urandom` at 2.9 ns per byte; character against block; copying across the boundary |
| [[L29 Interrupts DMA and the Block Layer]] | Polling, interrupts, DMA; **1,969 interrupts for 256 MiB in 1 MiB reads against 65,536 in 4 KiB reads**; `max_sectors_kb` explaining the first; **eight hardware queues, scheduler `none`**; why a handler may not sleep |
| [[L30 Writing a Driver and the Module That Will Not Load]] | A module built — **330 KB from six lines** — and refused by `insmod`; what the kernel takes away; the shape of a character driver in both kernels; **the six bugs a first driver has**, five of them Week 3's |
| [[CS202 Week9/assignments/QUIZ 9 Week 9 Monday\|QUIZ 9 Week 9 Monday]] | Ten minutes, covers **Week 8**, answer key printed |
| [[PS 9 A Character Device Twice]] | The same ring-buffer device in Linux (build only) and in xv6 (running). Due **Friday of Week 10** |
| `assignments/ps9/` | `ring.c` and `linux/cs202ring.c` with `TODO`s, `ringtest.c`, and the module `Makefile` |
| [[PROJECT 2 xv6 Memory and File System Features]] | **Assigned this week, due Friday of the completion period, 15%.** Lazy allocation, large files, symbolic links, and the measurements that show they work |
| [[LAB 9 Devices From Both Sides]] | The module that will not load; device-call costs; counting interrupts; **and three deliberate bugs in your own driver**. **Tuesday of Week 10** |
| `lab/devcost.c` | The same call to four devices, timed |
| [[CS202 Week9/resources/Reading Guide Week 9\|Reading Guide Week 9]] | OSTEP 36–37, xv6's `console.c` and `ide.c`, LDD3 Chapter 3 |
| `solutions_instructor/` | Instructor only — including the xv6 device reference and Project 2's patch |

---

### The One Thing to Take From This Week

**A driver is concurrent code reachable through `open`.**

Its interface is a table of functions; its correctness is Week 3's — block when there is nothing to do, wake whoever is waiting, never sleep where you may not, never trust a pointer from user space. **Five of the six bugs a first driver has are bugs you have already met**, and the sixth — returning a count you did not produce — is the one that fails silently.

**And the cost of using a device is mostly not the device.** 659 ns to call a driver that does nothing; 65,536 interrupts for data that 1,969 could have carried. **Interfaces, not hardware, decide most of what I/O costs.**

---

### Assessment Reminder

**PS 8 is due Friday at 17:00. PS 9 is released Wednesday.**

**Project 2 is assigned Wednesday: 15%, due Friday of the completion period.** **Project 1 is due Friday of Week 11, and its checkpoint is this week's lab session.**

**Labs and quizzes carry no weight** and are still required. **Quiz 9 is at the start of Monday's lecture and covers Week 8.**

> **Two labs touch this week.** **Lab 8** — snapshots and crashes — is sat on the **Tuesday of this
> week**. **Lab 9** covers this week and is sat on the **Tuesday of Week 10**.

Both are tracked in [[_CS 202 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 0's system call** is the 659 ns every device call starts with, page-table isolation included. **Week 3's `sleep`/`wakeup`** is the body of every blocking driver. **Week 7's buffer cache** sits between the file system and the disk driver, and **Week 8's flush** is a command this layer issues.

**Sideways:** **PROG 201**'s `read`/`write` wrappers are the user side of the same interface; **CS 212** will meet the same dispatch table as an object-oriented pattern.

**Forward:** **Week 10** turns the whole machine into a device: a hypervisor is a driver for a CPU. **Week 11's replicated log** is carried by network devices whose drivers work exactly like this week's. **Project 2** extends the kernel this week's driver lives in.

---

*CS 202 · Week 9 · © CSE Department*
