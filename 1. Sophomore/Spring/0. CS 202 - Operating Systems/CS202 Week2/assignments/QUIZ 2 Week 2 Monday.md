# CS 202 · Quiz 2
## Administered: Monday, Week 2 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 1** — the process record, states, the context switch, and the address space.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.
>
> Do not look at the key first. It costs you the only thing the exercise is for.

---

**Q1.** Name the two fields of xv6's `struct proc` that hold saved registers, and say which registers each holds.

&nbsp;

&nbsp;

---

**Q2.** A process's `/proc/<pid>/status` shows 0 voluntary and 4,788 involuntary context switches. What kind of process is it, and what took the CPU away from it?

&nbsp;

&nbsp;

---

**Q3.** xv6's `swtch` pushes `ebp`, `ebx`, `esi` and `edi`. Why not `eax`, `ecx` and `edx`?

&nbsp;

&nbsp;

---

**Q4.** A process is in state **D**. What does that mean, and what happens if you send it `SIGKILL`?

&nbsp;

&nbsp;

---

**Q5.** A program `mmap`s 256 MiB and has not touched it yet. What have `VmSize` and `VmRSS` each done?

&nbsp;

&nbsp;

---

**Q6.** In xv6's `fork`, which two lines make the call return twice with different values?

&nbsp;

&nbsp;

---

**Q7.** Two xv6 processes on one CPU each do floating-point arithmetic. What goes wrong, and why?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **`tf`** — the trap frame — holds the **user-mode registers**, saved on entry to the kernel. **`context`** holds the **kernel's callee-saved registers and return address** (`edi`, `esi`, `ebx`, `ebp`, `eip`), saved by `swtch` when the process was switched away from.

---

**Q2.** A **CPU-bound** process — a hog. It never blocks, so it never gives up the CPU voluntarily; **every switch was a preemption**, by the timer or by another task waking and being given the CPU.

---

**Q3.** They are **caller-saved** in the x86 calling convention. `swtch` is an ordinary function call, so **whoever called it has already saved anything it needed from them.** The user's values are safe in the trap frame.

---

**Q4.** **Uninterruptible sleep**: the process is waiting inside the kernel for something that must complete — classically I/O, or a parent inside `vfork`. **`SIGKILL` stays pending** and takes effect only when the wait finishes.

---

**Q5.** **`VmSize` grew by 256 MiB** at once — it is address space. **`VmRSS` did not change**: no page is in RAM until it is touched.

---

**Q6.** **`*np->tf = *curproc->tf;`** — the child gets a copy of the parent's saved user registers, so it resumes at the same instruction — and **`np->tf->eax = 0;`** — the child's return value is 0, while the parent's is the child's PID.

---

**Q7.** Their answers are wrong, and on one CPU the two wrong answers **sum to both right answers together**. **xv6 saves no FPU state on a context switch**, so the x87 register holding each process's running total is shared: the next process continues adding to the previous one's number.

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q6 | L04 §1 and L06 §5 |
| **Q2** | **L05 §2** — Wednesday's MLFQ is built on exactly this distinction |
| Q3 | L05 §3 |
| Q4, Q5 | L05 §1 and L06 §3 |
| **Q7** | **L05 §6** — and PS 1 Q4 |

**Q2 is the one that matters this week.** MLFQ decides a process's priority by watching whether it gives up the CPU or has it taken away — which is Q2 turned into a policy.

---

*CS 202 · Week 2 · Quiz 2 · covers Week 1 · ungraded*
