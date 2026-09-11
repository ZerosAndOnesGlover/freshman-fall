# CS 202 · Quiz 1
## Administered: Monday, Week 1 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 0** — what an operating system is, kernel and user mode, privileged instructions, and system calls.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room — the point
> is to find out what has not landed while there is still a term left to fix it.
>
> Do not look at the key first. It costs you the only thing the exercise is for.

---

**Q1.** Where does an x86 CPU keep the current privilege level, and what value does it have in an ordinary Linux program?

&nbsp;

&nbsp;

---

**Q2.** A program running in ring 3 executes `cli`. Name the exception the CPU raises, and the signal Linux delivers.

&nbsp;

&nbsp;

---

**Q3.** `rdtsc` normally runs in ring 3. Name the mechanism that can make it fault for one process only.

&nbsp;

&nbsp;

---

**Q4.** List three things the `SYSCALL` instruction does, and one important thing it does **not** do.

&nbsp;

&nbsp;

---

**Q5.** On the reference machine a system call that does not exist cost 572 ns, and `getppid` cost 594 ns. What does that tell you?

&nbsp;

&nbsp;

---

**Q6.** Why is `clock_gettime` about thirty times cheaper than `getppid`, when both are system calls in the manual?

&nbsp;

&nbsp;

---

**Q7.** In xv6, all 256 IDT gates but one have DPL 0. Which one does not, and why does that one gate matter?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** In the **low two bits of the `CS` register**. In a Linux user program `CS` is `0x33`, so the CPL is **3**. The kernel runs at CPL 0.

---

**Q2.** **`#GP`, general protection (vector 13)**, and Linux delivers **`SIGSEGV`**.

*Not `SIGILL`: `cli` is a valid instruction that is disallowed at this privilege level. `SIGILL` is for `#UD`, an opcode that does not exist, like `ud2`.*

---

**Q3.** The **`TSD` bit in `CR4`**, set by the kernel when it switches to that process. A program asks for it with **`prctl(PR_SET_TSC, PR_TSC_SIGSEGV)`**.

---

**Q4.** Any three of: saves the return address into **`RCX`**; saves `RFLAGS` into **`R11`**; clears the `RFLAGS` bits in `IA32_FMASK` (**interrupts off**); loads the kernel code segment (**CPL → 0**); jumps to the address in **`IA32_LSTAR`**.

**It does not switch the stack** — `RSP` still holds the user's value, which is why the kernel's entry code must load its own stack before it pushes anything.

---

**Q5.** **Almost all the cost of a cheap system call is the crossing itself** — entry, register saving, page-table switch and mitigations, and the exit — **not the work the call does.** `ENOSYS` does no work and still pays for the door.

---

**Q6.** `clock_gettime` goes through the **vDSO**: code and data the kernel maps into every process, so the time is read **in ring 3 with no trap**. `getppid` has no vDSO version and enters the kernel. Measured: **18.5 ns** against **~590 ns**.

---

**Q7.** **Vector 64, `T_SYSCALL`**, with DPL 3. It is **xv6's entire system-call interface** — the only way a user program may deliberately enter the kernel. Using any other gate with `int` is a `#GP`: `int $13` was killed with `trap 13 err 106`.

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L02 §2–§3 |
| Q3 | L02 §4 |
| **Q4** | **L03 §2** — and draw the before-and-after register table. This is on the Midterm |
| Q5, Q6 | L03 §4 |
| **Q7** | **L02 §7** — Wednesday's lecture assumes it |

**Q4 and Q7 are the ones that recur.** Wednesday's context switch saves registers for the same reason `SYSCALL` does, and every xv6 system call you add in Project 1 goes through gate 64. If either was shaky, fix it this week.

---

*CS 202 · Week 1 · Quiz 1 · covers Week 0 · ungraded*
