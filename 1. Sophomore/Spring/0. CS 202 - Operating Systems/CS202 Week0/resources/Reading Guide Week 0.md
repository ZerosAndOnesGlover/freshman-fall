# CS 202 · Reading Guide · Week 0
## OSTEP Chapters 1–6, and what to actually do with them

---

The curriculum sets **"Read: OSTEP Ch. 1–6"** for Week 0. That is about seventy pages, three of them dialogues, and **two of the six chapters are really Week 1's.** This guide says which is which.

| Chapter | Now? | Why |
|---|---|---|
| **1. A Dialogue on the Book** | *Skim* | Two pages. It explains the title, and the title is the course's structure |
| **2. Introduction to Operating Systems** | **Read** | The whole book in twenty pages: virtualization, concurrency, persistence, and a history. **This is L01** |
| 3. A Dialogue on Virtualization | *Skim* | A peach, and why sharing one is hard |
| 4. The Abstraction: The Process | **Week 1** | The process, its states, its data structures. Reading it now is not wasted; it is next Monday's lecture |
| 5. Interlude: Process API | *Skim* | `fork`, `exec`, `wait` — **PROG 201 Week 0 covered this in more depth.** Read it to see how OSTEP says what you already know |
| **6. Mechanism: Limited Direct Execution** | **Read twice** | Restricted operations, the trap table, and taking the CPU back. **This is L02 and L03** |

**If you have three hours this week:** Chapter 6, then Chapter 2, then Chapter 6 again, then the xv6 book (below).

---

## Chapter 2 — read for the three pieces

OSTEP's Chapter 2 runs four small C programs — one that uses the CPU, one that uses memory, one with two threads, one that writes a file — and uses each to motivate one part of the book. **Run them.** They are in the book's GitHub repository, and each takes a minute.

**Questions to hold while reading:**

1. The `cpu.c` example runs four copies at once on a machine the book says has one CPU, and all four appear to make progress. **What is the illusion, and what mechanism produces it?** Name the week of this course that builds that mechanism.
2. The `mem.c` example prints the same address from two processes, each storing a different value there. How can both be true? *(CS 201 Week 6 already told you. Say it in one sentence.)*
3. The `threads.c` example with a large loop count prints the wrong total. **Why is the answer different on every run?** *(Week 3. Write your guess down now.)*
4. §2.6 lists the design goals of an OS. **Which of them does L01's "guard" correspond to, and which ones conflict with it?** Give one pair that pulls in opposite directions and say why.
5. §2.7's history stops earlier than L01 §4's table. Which row of L01's table does OSTEP not have, and what does that row add to the argument?

---

## Chapter 6 — the chapter this week is built on

Read **§6.1–6.2** closely — direct execution, and the problem of restricted operations. That is **L02 and L03**. Then read **§6.3**, switching between processes — **that is Week 1**, but it depends on §6.2, and reading them together is the point of the chapter. §6.4 is a two-paragraph preview of Week 3.

**Questions:**

6. §6.2 introduces the **trap table**. Match OSTEP's description, step by step, to the xv6 code in L02 §7 and L03 §6: what is xv6's trap table called, which function fills it in, and when does that function run?
7. OSTEP's timeline figure shows two moments when the kernel runs *before* any user program: **at boot**, and **on each trap**. What does the kernel do in the first that makes the second safe? *(L03 §2 names three MSRs. Why must those be written at boot and not on each call?)*
8. §6.2 says the user program must not be able to specify the address it jumps to in the kernel, only a system-call number. **Explain what could go wrong otherwise**, using a concrete function in xv6's `sysfile.c` that a program would like to jump into the middle of.
9. §6.3 describes the **cooperative** approach to taking back the CPU, and rejects it. Which row of L01 §4's history table ran a real operating system on the cooperative approach, and what happened?
10. OSTEP's aside on measurement quotes figures for a system call and a context switch from the 1990s. **Compare them with L03 §4's 590 ns.** Is today's machine faster by the factor you would expect from thirty years of CPU speed-ups? If not, L03 §4 has the reason.

**Do the homework.** Chapter 6's homework asks you to measure the cost of a system call with a zero-byte `read`. **Do it, and compare with `syscost.c`.** Your number and the lecture's should have the same shape; if they differ by more than a factor of two, find out why before the Lab.

---

## The xv6 book — Chapter 0, and one part of Chapter 3

Use the **x86 edition, revision 11** — see the syllabus's *Which xv6*. The current RISC-V edition's code does not match the kernel you are building.

**Chapter 0, "Operating system interfaces"**, is a tour of xv6's system calls from the user's side: processes, file descriptors, pipes, the file system. **You know all of it from PROG 201.** Read it quickly and notice how few calls xv6 needs for a working shell.

11. Chapter 0 lists xv6's system calls in a table. Count them. **Which PROG 201 call you used every week does xv6 not have?** What would your Week 5 server have needed instead?

**Chapter 3, "Traps, interrupts, and drivers"** — read **only the sections on x86 protection and on system calls** this week. Leave interrupts and drivers for Week 9.

12. The book says the `int` instruction does a long list of things — changing stacks, pushing registers, loading `%cs` and `%eip` from the IDT entry. **Which of those steps does `SYSCALL`, in L03 §2, leave to the kernel's software instead?** Why might the designers of x86-64 have preferred that?
13. The book explains why the kernel's stack must be different from the user's. Give the concrete failure, in xv6, if `int $64` did not switch stacks and a user program set `%esp` to 0 before making a system call.

---

## Where to Go Deeper

| Source | Topic | When |
|---|---|---|
| **Silberschatz**, Ch. 1–2 | OS structure, dual-mode operation, system-call categories | **This week** — broader and more encyclopaedic than OSTEP |
| **Love**, Ch. 5 | System calls in Linux: numbers, handlers, `copy_from_user` | **This week**, for L03 |
| **Love**, Ch. 1–2 | Linux's history and building a kernel | Browse |
| **Intel SDM**, Vol. 3A, Ch. 5 and 6 | Protection, privilege levels, interrupt and exception handling | Reference for L02 |
| **Intel SDM**, Vol. 2B, `SYSCALL` | The instruction's exact definition | Reference for L03 §2 — it is one page, and worth reading once |

**The man pages you should have read by Friday:** `syscall(2)`, `syscalls(2)`, `vdso(7)`, `prctl(2)` (for `PR_SET_TSC`), `strace(1)`.

`man 2 syscall` has a table of every architecture's calling convention — which register holds the number, which hold the arguments, which instruction makes the call. **Find x86-64 and i386 in it**, and you have L03 §5 in two rows.

---

## The One Habit This Guide Is Trying To Build

**When the book gives a number, measure it on your own machine before you believe it.**

Question 10 is the deliberate case. OSTEP's figures were true of the machines they were measured on; L03's are true of this one; yours will be different again. **None of them is wrong.** The skill is knowing that a performance number is a fact about a machine, a kernel version and a configuration, and never about "system calls" in general — and that the configuration includes security mitigations that did not exist when most textbooks were written.

---

*CS 202 · Week 0 · Reading Guide · © CSE Department*
