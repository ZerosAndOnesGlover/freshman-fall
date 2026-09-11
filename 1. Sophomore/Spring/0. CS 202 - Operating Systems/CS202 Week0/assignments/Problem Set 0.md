# CS 202 · Problem Set 0
## Kernel and User Space; the Trap Mechanism

---

**Released:** Week 0, second Wednesday · **Due:** Week 1, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS0_{LastName}_{StudentID}.pdf`, plus your `.c` files in a tarball `PS0_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine and encouraged. The write-up and the code must be
> yours. State at the top: *"I worked on this problem set independently"* or name who you discussed
> which question with.
>
> **Every measured answer requires output from your own machine**, and marks there depend on you
> having run it. State your CPU model (`lscpu | grep 'Model name'`), `uname -r` and `gcc --version`
> at the top. **Your numbers will differ from the lectures' — they must not differ in shape**, and
> where they do, explaining why is worth full marks.
>
> Where a question says **predict first**, write the prediction down before you run anything and
> report both. A wrong prediction honestly reported and explained earns full marks; a right answer
> with no prediction earns half.
>
> Every program you submit compiles clean under `gcc -O2 -Wall -Wextra`.

---

### Q1: What the Mechanisms Are For (15 points)

**(a) [6]** For each mechanism, name **the problem it solves**, and describe **one concrete thing a program could do on MS-DOS**, which had none of them, that it cannot do on Linux:

| Mechanism | Problem it solves | Possible on MS-DOS, not on Linux |
|---|---|---|
| The timer interrupt | | |
| The U/S bit in page-table entries | | |
| The I/O privilege level | | |

**(b) [4]** Classify each as **mechanism** or **policy**, with one sentence of justification: *(i)* saving registers into a trap frame; *(ii)* giving interactive processes a shorter time slice; *(iii)* `vm.overcommit_memory`; *(iv)* the TSS's kernel stack pointer.

**(c) [5]** In a microkernel, a `read` from a file might cross the user/kernel boundary **four times**: application → kernel, kernel → filesystem server, filesystem server → kernel, kernel → application (ignoring the disk driver). Using **your own** measured cost of one crossing from Q3(a), estimate the overhead a microkernel adds to each `read` compared with a monolithic kernel's one round trip. Then use Q3(c)'s table to say **for which workload that overhead would matter, and for which it would not.** A number is required; so is the argument.

---

### Q2: The Wall (20 points)

**(a) [8] Predict first.** For each instruction, predict whether it runs in ring 3 on your machine, and if not, which signal kills the process. Then add each to `privfault.c` and report what happened.

| Instruction | Prediction | Result |
|---|---|---|
| `lgdt` (load a GDT from a 10-byte buffer) | | |
| `sti` | | |
| `int3` | | |
| `ud2` | | |
| `wrmsr` (ECX = `0xC0000082`, `IA32_LSTAR`) | | |
| `pause` | | |
| `int $0x80` with `eax = 20` | | |

**Two of these are not killed, for different reasons.** Say what the two reasons are.

**(b) [6]** `rdtsc` is allowed in ring 3 by default. Give **one reason** a kernel designer would allow it, and **one reason** a sandbox would forbid it. Then reproduce L02 §4's `tsc.c` result on your machine, and **state exactly what the kernel changes, and when, to make it fault for one process and not for others.**

**(c) [6]** Run `grep -c -w umip /proc/cpuinfo` and `grep UMIP /boot/config-$(uname -r)`, and run `sgdt` from ring 3.

- Report all three results.
- If `sgdt` ran and returned an address, is it a user or a kernel address? How do you know?
- **In three sentences:** why does the second command not answer the question the first one does, and what is the only reliable way to know whether a protection is in force?

---

### Q3: What the Door Costs (25 points)

**(a) [8]** Run `syscost.c` on your machine and report its table. Compute:

- the ratio of `syscall(SYS_getppid)` to the function call;
- the ratio of `syscall(SYS_clock_gettime)` to `clock_gettime` through the vDSO.

**Then explain the second ratio.** Both calls return the same time. What does one do that the other does not? Why can the vDSO not be used to make `getppid` equally cheap — or can it? *(Think about what `getppid`'s answer depends on, and when it can change.)*

**(b) [5]** On the reference machine, `syscall(1000)` — a system call that does not exist — cost **572 ns** against **594 ns** for `getppid`. Report your two numbers. **What does their closeness tell you about where the cost of a system call is spent?** Name two things that happen on *every* entry, whatever the call number.

**(c) [7]** Run `readsize.c` on a 16 MiB file with buffers of **1, 16, 4,096 and 65,536 bytes**, and report the number of `read()` calls, the total time and the time per call.

- Explain why the **time per call** stays nearly constant for small buffers and rises for large ones.
- Explain why the **total time** falls by more than three orders of magnitude.
- A program reads a file with `fgetc` in a loop. **Predict** whether its total time will look like your 1-byte row or your 4,096-byte row, and say why. Then measure it.

**(d) [5]** Run `grep . /sys/devices/system/cpu/vulnerabilities/*` and list every line that begins `Mitigation:`. **You cannot tell from `syscost.c` alone how much of your syscall cost each mitigation causes.** Explain why not, and **describe an experiment** that would tell you — what you would change, how, what you would measure, and what access you would need that a student account does not have.

---

### Q4: The Trap by Hand (25 points)

**(a) [10]** Write `nolibc.c`: a program with **no C library at all** — compiled with `-nostdlib -static` — that prints a line with the `write` system call and ends with `exit`, **both made with the `SYSCALL` instruction directly.** Your program provides `_start` itself.

```bash
gcc -O2 -static -nostdlib -fno-stack-protector -o nolibc nolibc.c
strace ./nolibc
```

Submit the source, the `strace` output — which must show **exactly two system calls after the `execve`** — and the size of the binary. Compare that size with a statically linked `printf` version.

**(b) [5]** The `SYSCALL` instruction overwrites two registers. **Name them, say what it stores in each**, and explain why Linux's system-call convention passes the fourth argument in `r10` when the C calling convention passes it in `rcx`.

**(c) [5]** From a **64-bit** program, execute `int $0x80` with `eax = 39`. Report the return value and the line `strace` prints about it. **Explain both** — what system call ran, why that one, and why it returned what it did.

**(d) [5]** `SYSCALL` does not change `RSP`. Describe **a concrete attack** that would work if the kernel's entry code simply pushed the user's registers onto whatever stack `RSP` pointed at. What would a user program set `RSP` to, and what would the kernel's own push then do?

---

### Q5: xv6 (15 points)

Use the xv6-public tree you built in Lab 0.

**(a) [5]** Trace `getpid()` from a user program to `sys_getpid` and back. For each step, give **the file, the function or label, and one sentence** saying what it does. **Mark the exact instruction at which the CPL changes from 3 to 0, and the exact instruction at which it changes back.**

**(b) [5] Predict first.** A user program calls `write(1, (char *)0x80100000, 16)` — a pointer to the start of xv6's kernel. Using `argptr` in `syscall.c`, predict what `write` returns. Then write the program, add it to `UPROGS`, run it, and report. **What would an unprotected kernel have written to the console?**

**(c) [5]** In Lab 0, `int13` was killed with **`trap 13 err 106`**. Write 106 in binary, and split it into the fields of an x86 selector error code: **the index, the IDT bit, and the EXT bit.** What does each field say about what the program tried to do? Then change `int $13` to `int $64` in `int13.c`, rebuild, and explain what happens instead — and why that one is not killed.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | What the mechanisms are for | 15 |
| 2 | The wall | 20 |
| 3 | What the door costs | 25 |
| 4 | The trap by hand | 25 |
| 5 | xv6 | 15 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem set of the term is dropped**, which is there for the week you are ill, not for the week you forgot.

---

*CS 202 · Week 0 · PS 0 · © CSE Department*
