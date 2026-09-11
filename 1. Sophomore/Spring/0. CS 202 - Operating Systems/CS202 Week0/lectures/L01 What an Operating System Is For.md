# CS 202 · Operating Systems
## Week 0 · Lecture 1 of 3
### What an Operating System Is For

---

**Sat:** first Wednesday of Week 0, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 1–2 · **Next:** L02, the two modes and the wall between them

---

## 1. Three Jobs, One Program

An operating system does three things, and every design decision in this course is a trade between them.

| Job | What it means | The word OSTEP uses | Where this course does it |
|---|---|---|---|
| **Referee** | Many programs want one CPU, one memory, one disk. Somebody has to decide who gets what, and when | *resource management* | Weeks 2, 4, 6 |
| **Illusionist** | Each program is shown a machine it has to itself: its own CPU, its own contiguous memory, named files rather than disk sectors | *virtualization* and *persistence* | Weeks 1, 5, 7, 10 |
| **Guard** | The first two are worthless if a program can ignore them — reach past the referee, or see through the illusion into someone else's memory | *protection* | Weeks 0, 5, 12 |

OSTEP organises the book as **virtualization, concurrency and persistence** — the "three easy pieces". The guard is not a fourth piece; it is the condition under which the other three mean anything, and it is where this week starts.

> **The course in one sentence:** an operating system is the program that makes one machine look
> like many machines, each of them simpler than the real one, **and makes that illusion
> impossible to break from inside.** Weeks 1–11 are the illusion. This week is the "impossible to
> break".

---

## 2. The Illusion, Measured

Everything below was read on the reference machine — an Intel i5-8250U laptop, Ubuntu 24.04.4, kernel 7.0 — in the middle of an ordinary afternoon with a browser and an editor open. The commands are printed beside each number; run them on your own machine now.

| What the programs see | What the machine has | Command |
|---|---|---|
| **1,425 threads**, each of which believes it can run | **8** logical CPUs | `ls -d /proc/[0-9]*/task/* \| wc -l`; `nproc` |
| **351 processes**, each with its own PID and its own memory | one physical memory | `ls -d /proc/[0-9]* \| wc -l` |
| **24,353 GiB** of virtual address space, summed over all processes | **7.5 GiB** of RAM | `ps -eo vsz= \| awk '{s+=$1} END {print s/1048576}'` |
| **27.0 GiB** of memory promised to programs (`Committed_AS`) | a commit limit of **7.8 GiB** | `grep Commit /proc/meminfo` |
| An idle desktop — `top` says **81% idle** | **9,533 context switches** and **6,757 interrupts** every second | two reads of `ctxt` and `intr` in `/proc/stat`, ten seconds apart |

**Read the fourth row twice.** The kernel has promised programs three and a half times more memory than exists, and nothing has gone wrong, because almost none of it has been touched. That is not a bug; it is Week 6's overcommit policy, and it is the reason Week 6 also has an OOM killer.

**And the last row is the one that should surprise you.** "Idle" means that almost none of the 8 CPUs' time is spent running your programs. It does not mean nothing is happening: the kernel is taking an interrupt roughly every 150 microseconds and switching between threads roughly every 105. You never see any of it, and that invisibility is the illusion working.

> **Every row of that table is a week of this course.** Rows 1 and 5 are Weeks 1–3 — the process,
> the context switch, and the scheduler that decides which 8 of 1,425 threads run. Rows 2–4 are
> Weeks 5–6. Week 7 is the question of what happens to a file you wrote before the machine lost
> power, which is the illusion of *persistence* and the only one of the three that has to survive
> the machine being switched off.

---

## 3. What Each Program Is Shown

The illusionist's job is best stated as a table of lies, each of which is told for a good reason.

| The program is shown | The truth | Why the lie is better | Week |
|---|---|---|---|
| **A CPU of its own**, running its instructions in order | a CPU shared with 1,424 other threads, taken away without warning several hundred times a second | nobody has to write code that yields; a bug that loops forever cannot freeze the machine | 1, 2 |
| **A private address space**, starting near zero and contiguous | physical frames scattered anywhere, shared with other processes where it is safe, and sometimes on disk | a program is written once and runs at any address; a pointer bug cannot reach another program | 5, 6 |
| **Files with names**, that grow | numbered blocks on a device that fails, and a cache in RAM that disappears on power loss | nobody writes a block allocator; and the name survives a reboot | 7, 8 |
| **Devices as file descriptors** — `read` and `write` | a thousand different chips with registers, interrupts and timing requirements | `cat` works on a keyboard, a disk and a network socket without knowing which | 9 |
| **A whole machine** | a process on someone else's kernel | one physical server becomes forty rented ones | 10 |
| **One reliable service** | five unreliable machines that disagree | a database that survives losing a data centre | 11 |

**Notice that every lie is an abstraction, and every abstraction has a cost.** Weeks 1–11 each end by measuring what the abstraction costs, because a systems engineer who does not know the price of the illusion will eventually pay it by accident.

---

## 4. History Is a List of Problems, Each Solved by a Mechanism

The textbook history — batch, multiprogramming, timesharing, personal computers, distributed systems — is usually told as a sequence of eras. **It is more useful as a sequence of problems**, because each mechanism was invented to solve one, and each one created the next.

| Era | The problem | The mechanism invented | The problem it created | Here |
|---|---|---|---|---|
| **Batch** (from the mid-1950s; GM-NAA I/O on the IBM 704, 1956) | An expensive machine idles while a human loads the next job | A **resident monitor** that loads jobs one after another | A job can overwrite the monitor. **So: memory protection, and a privileged mode** | **W0** |
| **Multiprogramming** (1960s; the Atlas, 1962; OS/360, 1964) | The CPU idles while a job waits for a tape | Keep several jobs in memory and **switch when one blocks**; **interrupts** tell the OS when I/O finishes | Jobs must be kept out of each other's memory, and someone must choose which runs. **So: address translation and scheduling** | W1, W2, W5 |
| **Timesharing** (CTSS at MIT, 1961; Multics, from 1965; Unix, 1969) | A human at a terminal waits minutes for a result | **A timer interrupt** takes the CPU away every few milliseconds, whether the program yields or not | Code that shares data can now be interrupted mid-update. **So: locks** | W2, W3 |
| **Personal computing** (MS-DOS, 1981) | One user, one machine — so why protect anything? | **Nothing.** MS-DOS ran every program with full control of the hardware | Any program could crash the machine, and malware needed no exploit. **Protection returned** with Windows NT (1993) and Mac OS X (2001) | W0, W12 |
| **Virtualization and the cloud** (VMware from 1999; Xen, 2003; KVM in Linux 2.6.20, 2007) | One physical server per customer is wasteful | **Run whole operating systems as processes**, with hardware support for a mode below the kernel | Isolation is now as strong as the hypervisor — and a CPU flaw can break it. **So: Meltdown and its mitigations (2018)** | W10, W12 |
| **Distributed systems** | One machine fails; a service must not | **Replicate** state across machines and agree on it | Machines disagree, networks partition, and you cannot tell a dead machine from a slow one | W11 |

**The personal-computing row is the one to remember.** An entire industry decided, reasonably, that a single-user machine did not need protection — and then spent the next twenty years putting it back, at great cost, because a machine connected to a network is never single-user. The Week 0 idea is not old; it was unlearned and relearned within living memory.

**The last column is the shape of the whole course.** Nothing in operating systems is solved; each mechanism moves the problem somewhere you can manage it.

---

## 5. Mechanism and Policy

OSTEP draws one distinction early and uses it everywhere, and so does this course.

- **Mechanism** is *how* something is done: saving a thread's registers and loading another's.
- **Policy** is *which* and *when*: which thread runs next, and for how long.

Linux lets you see the separation from a shell. The mechanism of a context switch is compiled into the kernel and you cannot change it. The policy is a set of knobs:

```bash
nice -n 19 ./job           # ask the policy to favour everyone else
chrt --idle 0 ./job        # a different scheduling class entirely
taskset -c 3 ./job         # a placement policy: only CPU 3
```

**The design rule is: put mechanisms in the kernel and keep policies replaceable.** Week 2 writes three scheduling policies against one mechanism, and PS 2 simulates two of Linux's. Week 6 does the same for page replacement. When you meet a kernel feature this term, ask which half it is.

---

## 6. The Kernel Is Not the Operating System

"Operating system" is used loosely for everything that ships on the install medium. **The kernel is precisely the part that runs in the privileged mode** — L02 makes that exact — and everything else is ordinary programs.

| Component on the reference machine | Kernel? | Why |
|---|---|---|
| Linux 7.0 — scheduler, page tables, filesystems, drivers | **Yes** | runs in ring 0 |
| glibc 2.39 — `printf`, `malloc`, the `read()` wrapper | No | a library linked into your process, running with your privileges |
| systemd — starts services, manages sessions | No | PID 1, but an ordinary process: it asks the kernel for everything |
| The shell, `ls`, `gcc` | No | programs |

**xv6 makes the split countable.** The copy you will build in Lab 0 has **6,245 lines of kernel** (`.c`, `.S` and `.h` files that are linked into the kernel image) and **3,144 lines of user programs** — the shell, `ls`, `cat`, and a test suite. Linux's kernel is thousands of times larger, and the split means exactly the same thing.

**Where the line goes is a design choice, and people have fought about it.** A *monolithic* kernel (Linux, xv6) puts the filesystem and drivers inside the privileged boundary: fast, because nothing crosses the boundary to reach them, and dangerous, because a driver bug is a kernel bug. A *microkernel* (MINIX 3, L4, seL4) keeps only address spaces, threads and message passing inside and runs everything else as processes: slower, because a `read` crosses the boundary several times, and robust, because a crashed driver is restarted like any other program. **seL4's kernel is small enough to have been formally proven correct**, which no monolithic kernel is. L03 measures what one crossing costs, and that number is most of this argument.

---

## 7. Why the Course Is Built Around xv6

The curriculum's project is **xv6**, MIT's teaching kernel: a re-implementation of Sixth Edition Unix, small enough to read in full, written for teaching rather than for use.

It has **21 system calls**. The reference machine's Linux headers define **373**, numbered up to 461. xv6 has one scheduler, one filesystem, one kind of lock, and no networking. **Everything it has, it has in the simplest form that works**, and every simplification is a question worth asking: why does Linux need more than this?

> **This course uses the x86 version of xv6**, not the RISC-V version MIT now teaches. The lab
> machines have `gcc -m32` and `qemu-system-i386` and have no RISC-V cross-compiler, and the
> curriculum names x86-64 assembly as the course language. Lab 0 builds it, and the
> [[CS202 Week0/resources/Course Overview Syllabus|syllabus]] records the choice and the one-line
> build fix it needs. **The ideas are identical; the trap entry code is x86 rather than RISC-V, which
> suits a course that follows CS 201.**

---

## 8. What to Take Away

1. **An operating system is a referee, an illusionist and a guard.** The guard is what makes the other two worth anything.
2. **The illusion is enormous and measurable.** 1,425 threads on 8 CPUs; 24,353 GiB of address space on 7.5 GiB of RAM; 9,533 context switches a second on a machine reported as idle.
3. **Every abstraction is a lie told for a reason, and has a price.** This course measures the price.
4. **Each historical mechanism solved one problem and created the next.** Protection was invented, abandoned for personal computers, and put back.
5. **Mechanism in the kernel, policy replaceable.**
6. **The kernel is the part in the privileged mode**, and where that line goes — monolithic or microkernel — is a design decision with a cost you can measure.

---

## Exercises

*(Not assessed. PS 0 is the assessed work; these take a few minutes at a terminal.)*

1. Reproduce §2's table on your own machine. Which row differs most from the reference machine's, and why?
2. `cat /proc/interrupts`. Find the row for the timer (`LOC:` on x86). Roughly how many timer interrupts does each CPU take per second, and how does that compare with `CONFIG_HZ` in `/boot/config-$(uname -r)`? *(They need not agree. Why might they not?)*
3. Pick any process with `ps -eo pid,vsz,rss,comm --sort=-vsz | head`. Why is its `VSZ` so much larger than its `RSS`?
4. Classify each as mechanism or policy: *the TLB*; *the `swappiness` sysctl*; *`fsync`*; *round-robin with a 10 ms quantum*; *copy-on-write*.
5. MS-DOS let every program write to any I/O port. Name one thing a program could do with that which a modern Linux program cannot, and say which mechanism in L02 prevents it.

---

*CS 202 · Week 0 · L01 · © CSE Department*
