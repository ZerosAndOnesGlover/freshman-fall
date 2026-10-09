# CS 202 · Operating Systems
## Week 0 · Lecture 2 of 3
### Two Modes, and the Wall Between Them

*“Wherever there is modularity there is the potential for misunderstanding: Hiding information implies a need to check communication.”* — Alan Perlis, "Epigrams on Programming" (1982), #20

---

**Sat:** first Friday of Week 0, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 6 §6.1–6.2 · **Next:** L03, system calls and the trap

**Coursework:** 📝 **PS 0** released Wed this week, due Fri of Week 1 17:00 · 🔬 **Lab 0** Fri this week 10:00–11:50

---

## 1. The Problem the Wall Solves

L01 ended with the guard. Here is why the guard cannot be software alone.

The fastest way to run a program is to **let it run directly on the CPU** — no interpreter, no checking of each instruction. OSTEP calls this *direct execution*, and every general-purpose OS does it. But while your program's instructions are executing, **the kernel is not running.** It cannot inspect the next instruction, because it is not executing anything.

So consider what a program running directly on an x86 CPU could do if nothing stopped it:

| Instruction | Effect if a user program could run it |
|---|---|
| `cli` | Disable interrupts. The timer can no longer take the CPU back, so **the scheduler never runs again** |
| `hlt` | Stop the CPU until the next interrupt |
| `out` to the disk controller's ports | Write any sector of the disk, underneath every filesystem permission |
| `mov %rax, %cr3` | **Load a different page table** — see and write any process's memory, including the kernel's |
| `wrmsr` to `IA32_LSTAR` | Replace the address the CPU jumps to on every system call (L03) |

**Any one of these ends protection.** And no amount of checking in the kernel helps, because the kernel is not running when the instruction executes. **The check has to be in the CPU.**

OSTEP's name for the solution is **limited direct execution**: run the program directly, but in a mode in which the CPU itself refuses those instructions, and arrange that the only ways back into the kernel are ones the kernel chose in advance.

---

## 2. Where the Mode Lives

On x86 the CPU's current privilege level — the **CPL** — is the **low two bits of the code segment register, `CS`**. Four levels exist, called *rings* 0 to 3. Linux and xv6 use only two: **ring 0 for the kernel, ring 3 for everything else.**

You can read `CS` from an ordinary program; reading it is not privileged. From `privfault.c` on the reference machine:

```
CS = 0x33, so CPL = 3
```

And from the kernel you will build in Lab 0, which runs with nothing underneath it:

```
Hello from ring 0
CPL = 0
```

**Same register, same instruction to read it, different machine state.** Nothing in either program *chose* its ring. The user program is in ring 3 because the kernel put it there before jumping to it; the Lab 0 kernel is in ring 0 because that is where the CPU starts.

> **Other architectures name the same idea differently.** RISC-V has U-mode, S-mode and M-mode;
> ARMv8 has exception levels EL0 (applications) to EL3 (firmware). Everyone has at least the two
> levels this lecture needs, and most have a third above the kernel — which is Week 10's
> hypervisor.

---

## 3. What Ring 3 May Not Do — Measured

`privfault.c` forks one child per instruction, executes that one instruction in the child, and reports what happened. Run on the reference machine, ring 3:

| Instruction | What it would do | Result in ring 3 |
|---|---|---|
| `cli` | disable interrupts | **killed by SIGSEGV** |
| `hlt` | halt the CPU | **killed by SIGSEGV** |
| `inb (%dx)`, port `0x3f8` | read the serial port | **killed by SIGSEGV** |
| `outb (%dx)`, port `0x3f8` | write the serial port — *the exact instruction the Lab 0 kernel uses to print* | **killed by SIGSEGV** |
| `rdmsr`, MSR `0x10` | read a model-specific register | **killed by SIGSEGV** |
| `mov %cr3, %rax` | read the page-table root | **killed by SIGSEGV** |
| `sgdt` | read the GDT register | **ran** — and returned `0xfffffe530262c000` |
| `rdtsc` | read the timestamp counter | **ran** |
| `cpuid` | identify the CPU | **ran** |

**What actually happened, step by step, for `cli`:**

1. The CPU decodes `cli`, sees CPL 3, and **refuses to execute it**. It raises exception 13, *general protection* (`#GP`).
2. An exception is a forced entry into ring 0. The CPU looks up vector 13 in the **interrupt descriptor table**, which the kernel filled in at boot, switches to ring 0 and to a kernel stack, and jumps to the kernel's handler.
3. Linux's handler sees that the fault came from user mode and **sends the process `SIGSEGV`**. The default action for `SIGSEGV` is to terminate.

**The CPU enforced the rule, and the kernel chose the consequence.** A different kernel could emulate the instruction, log it, or kill the whole process group; the refusal itself is not negotiable.

> **Why SIGSEGV and not SIGILL?** The instruction is perfectly legal; the CPU knows exactly what
> `cli` means. It is *disallowed*, which the CPU reports as a protection fault — and Linux maps
> protection faults to `SIGSEGV`. An opcode that does not exist raises a different exception
> (`#UD`, invalid opcode), which Linux maps to `SIGILL`.

---

## 4. Three Kinds of Rule — and the Kernel Sets Two of Them

The table in §3 is not one rule. It is three, and the difference matters.

| Kind | Instructions | Who decides |
|---|---|---|
| **Ring 0 only, always** | `hlt`, `mov` to or from `%cr0`/`%cr3`/`%cr4`, `rdmsr`/`wrmsr`, `lgdt`/`lidt` | **The CPU.** No kernel setting lets ring 3 run these |
| **Ring 0 unless the kernel grants it** | `in`, `out`, `cli`, `sti` | The **I/O privilege level** in `RFLAGS` and the per-task I/O permission bitmap, both set by the kernel. Linux gives every process IOPL 0 |
| **Allowed unless the kernel forbids it** | `rdtsc`, `sgdt`/`sidt` | Control-register bits the kernel sets: `CR4.TSD` makes `rdtsc` fault, `CR4.UMIP` makes `sgdt` fault |

**The middle row is how X servers once drove graphics cards from user space**: a privileged process called `iopl(3)` and was then allowed to touch ports directly. Linux still offers `ioperm(2)` to processes with `CAP_SYS_RAWIO`, and since Linux 5.5 no longer lets even those processes disable interrupts.

**The bottom row you can test yourself, without any privilege.** Linux exposes `CR4.TSD` per process through `prctl(2)`. `tsc.c`, on the reference machine:

```
PR_GET_TSC = PR_TSC_ENABLE
  before: rdtsc = 72823018231802
prctl(PR_SET_TSC, PR_TSC_SIGSEGV) = 0
  after : killed by signal 11
```

**One system call later, an instruction that was allowed is a protection fault.** The kernel flips the bit in `CR4` whenever it switches to this process, and flips it back when it switches away.

**Why would anyone want this?** `rdtsc` is a nanosecond-resolution clock that needs no system call, and a precise clock is exactly what a timing side-channel attack needs. Sandboxes turn it off for the code they distrust. You will meet this again in Week 12.

---

## 5. A Mechanism Compiled In Is Not a Mechanism Working

Look at `sgdt` again. It stores the address of the kernel's **global descriptor table** — a kernel data structure — into user memory. On the reference machine it ran, and returned **`0xfffffe530262c000`**: a kernel address, obtained by an ordinary program without a system call.

This is known, and there is a fix. Intel's **UMIP** (*User-Mode Instruction Prevention*) is a `CR4` bit that makes `sgdt`, `sidt`, `sldt`, `smsw` and `str` fault in ring 3. The reference machine's kernel was built with it:

```
$ grep UMIP /boot/config-$(uname -r)
CONFIG_X86_UMIP=y
$ grep -c -w umip /proc/cpuinfo
0
```

**The kernel supports UMIP. The CPU does not have it.** The i5-8250U predates the feature, so the bit the kernel would set does not exist, and the instruction runs.

> **Hold on to this pattern — you will see it all term.** The configuration says a protection is
> on; the machine does not do it. Nothing reports the gap: no warning, no error, no failed call.
> **The only way to know whether a protection is working is to try to break it and see whether it
> stops you.** That is what `privfault.c` does, and it is the method of Week 12.

**Whether that address is worth anything** to an attacker depends on how much else the kernel randomises and hides — `/proc/kallsyms` on the same machine prints every symbol at address `0000000000000000` to an unprivileged user, because `kernel.kptr_restrict` is 1. That is Week 12's subject. The point here is narrower: **a user program learned something about ring 0 that nobody decided it should.**

---

## 6. Memory Is the Other Half of the Wall

Refusing instructions is not enough. A user program that could simply *read* the kernel's memory, or *write* it, would not need `cli`.

`kread.c` tries to read one byte at each of four addresses:

| Address | What lives there | Result |
|---|---|---|
| `0xffffffff81000000` | where x86-64 kernels traditionally load their text | **SIGSEGV**, `SEGV_MAPERR` |
| `0xffff888000000000` | the start of the kernel's direct map of physical memory | **SIGSEGV**, `SEGV_MAPERR` |
| `0x0` | nothing — a NULL pointer | **SIGSEGV**, `SEGV_MAPERR` |
| `0x7ffffffff000` | the top page of the user half | **SIGSEGV**, `SEGV_MAPERR` |

**To a user program, the kernel's half of the address space is indistinguishable from a NULL pointer.** That is the point.

The mechanism is a bit in every page-table entry, **U/S — user/supervisor**. A page whose entry has U/S clear can be touched only in ring 0; the CPU checks the bit on every access, as part of the translation CS 201 Week 6 described. Week 5 walks the page table and finds the bit.

**The wall runs in both directions.** The reference machine's CPU flags include `smep` and `smap`:

- **SMEP** — *Supervisor Mode Execution Prevention* — makes the CPU refuse to **execute** a user page while in ring 0.
- **SMAP** — *Supervisor Mode Access Prevention* — makes it refuse to **read or write** a user page in ring 0, except inside a window the kernel opens deliberately.

Both exist because a kernel bug that jumps to, or dereferences, a user-controlled pointer is the most common way to turn a kernel bug into a privilege escalation. **The wall protects the kernel from user programs, and also from its own mistakes.**

> **And the wall has been breached.** In 2018 *Meltdown* showed that on many Intel CPUs a user
> program could read kernel memory **speculatively** — the CPU raised the fault, but only after
> briefly executing the read, and the value left traces in the cache. The page-table bit was
> correct; the CPU's speculation ignored it. **Linux's fix was to stop mapping the kernel into user
> page tables at all** while user code runs — *page-table isolation*. On the reference machine,
> `cat /sys/devices/system/cpu/vulnerabilities/meltdown` says `Mitigation: PTI`. L03 measures what
> that costs.

---

## 7. The Wall Has Doors, and the Kernel Chose Where

A wall with no doors is a crash. The CPU enters ring 0 in exactly three ways, and **the kernel decides the destination of every one of them in advance**, by filling in the interrupt descriptor table at boot:

| Door | Caused by | Asked for? | Example |
|---|---|---|---|
| **Interrupt** | a device — the timer, the disk, the network card | No | the 6,757 per second in L01 §2 |
| **Exception** | the instruction just executed — a fault | No | §3's `#GP`; a page fault (Week 5) |
| **System call** | the program, deliberately | **Yes** | L03 |

**Each IDT entry — each *gate* — carries its own privilege level, its DPL.** A program in ring 3 may use the `int n` instruction to jump through a gate only if that gate's DPL is 3. **This is what stops a user program from simply calling the page-fault handler.**

**xv6 shows the rule in two lines** (`trap.c`, lines 23–24):

```c
for(i = 0; i < 256; i++)
    SETGATE(idt[i], 0, SEG_KCODE<<3, vectors[i], 0);            /* DPL 0: kernel only */
SETGATE(idt[T_SYSCALL], 1, SEG_KCODE<<3, vectors[T_SYSCALL], DPL_USER);
```

**All 256 gates are closed to ring 3, and then one is opened: vector 64, `T_SYSCALL`.** That single open gate is xv6's entire system-call interface.

**Measured inside xv6.** A user program that executes `int $13` — trying to jump straight into the general-protection handler — and then one that executes `cli`:

```
$ int13
int13: executing int $13
pid 5 int13: trap 13 err 106 on cpu 0 eip 0x58 addr 0x0--kill proc
$ int13 cli
int13: executing cli
pid 6 int13: trap 13 err 0 on cpu 0 eip 0x5b addr 0x0--kill proc
```

**Both are killed with trap 13, and the error codes say why.** For `cli`, error 0: the instruction itself was refused. For `int $13`, **error 106**, which is `0x6a` = `(13 << 3) | 2` — the CPU's way of saying *"the fault concerns IDT entry 13"*. The program asked to use gate 13, the gate's DPL is 0, and the CPU raised a `#GP` about the gate instead of taking it. Neither message came from `int13`; both were printed by xv6's `trap()`, in ring 0.

---

## 8. What to Take Away

1. **Direct execution is fast and the kernel is not running while it happens**, so the protection check must be in the CPU.
2. **The mode is the CPL, the low two bits of `CS`**: 3 for user programs (`CS = 0x33`), 0 for the kernel.
3. **A privileged instruction in ring 3 is a `#GP`**, which Linux turns into `SIGSEGV`. The CPU refuses; the kernel chooses the consequence.
4. **Some rules are fixed in the CPU and some are set by the kernel** — `prctl(PR_SET_TSC)` turned `rdtsc` into a fault with one call.
5. **A protection that is configured is not necessarily working.** UMIP is compiled in and the CPU lacks it, and `sgdt` returned a kernel address.
6. **Memory is protected by the U/S bit**, and SMEP and SMAP protect the kernel from its own bugs. Meltdown broke the bit speculatively, and PTI is the fix.
7. **There are three doors into ring 0** — interrupts, exceptions and system calls — and **the kernel chose every destination at boot**. xv6 opens exactly one gate to ring 3.

---

## Exercises

1. Run `privfault.c`. Then add `ud2` (the defined-to-be-invalid instruction) and `int3` to the table. Predict the signal for each before you run it.
2. Add `wrmsr` to `privfault.c`. Why would it be **catastrophic** rather than merely bad if ring 3 could execute it, when `rdmsr` is only bad? *(L03 §2 names one MSR that makes the answer obvious.)*
3. Read `/proc/cpuinfo` on your own machine. Does it have `umip`? If so, run `privfault.c` and report what `sgdt` does now.
4. In xv6's `trap.c`, change `DPL_USER` to `0` on line 24 and rebuild. Predict what happens when `init` makes its first system call, then boot it and see. *(Restore the line afterwards.)*
5. `kread.c` got `SEGV_MAPERR` for the kernel's address and for NULL. What would you expect to see instead if the page existed but the U/S bit forbade access? Find the constant in `man 2 sigaction`.

---

*CS 202 · Week 0 · L02 · © CSE Department*
