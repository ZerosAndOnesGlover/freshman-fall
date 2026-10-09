# CS 202 · Operating Systems
## Week 0 · Lecture 3 of 3
### System Calls: the Trap, What It Costs, and What the Numbers Mean

*“I think the major good idea in Unix was its clean and simple interface: open, close, read, and write.”* — Ken Thompson, "Unix and Beyond: An Interview with Ken Thompson" (1999)

---

**Sat:** second Wednesday of Week 0, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 6 in full; xv6 book Ch. 3 on system calls · **Next:** Week 1, the process

**Coursework:** 📝 **PS 0** released Wed this week, due Fri of Week 1 17:00 · 🔬 **Lab 0** Fri this week 10:00–11:50

---

## 1. A System Call Is a Function Call That Changes Privilege

L02 built a wall and said it has three doors. **This lecture is the one a program opens on purpose.**

A program that wants something only the kernel can do — open a file, send a packet, create a process — has to transfer control into ring 0. Whatever mechanism does that must meet four requirements, and each one rules out something simpler:

| Requirement | Rules out |
|---|---|
| **1. Change the CPL from 3 to 0** | an ordinary `call` — it cannot change privilege |
| **2. Land only where the kernel chose** | a `call` to a kernel address — the program would pick the entry point, and could jump into the middle of a permission check |
| **3. Not trust anything the program controls** — including its stack pointer | using the program's stack for the kernel's first instructions |
| **4. Come back** to the instruction after the call, in ring 3 | a one-way jump |

**x86-64 meets all four with one instruction, `SYSCALL`**, and one instruction back, `SYSRET`. xv6, which is 32-bit, uses the older route — an `int` through the one open IDT gate from L02 §7. Both are here, because they are the same idea in different clothing.

---

## 2. What `SYSCALL` Does, Atomically

The kernel prepares for system calls **once, at boot**, by writing three model-specific registers — the `wrmsr` that ring 3 is forbidden (L02 §4):

| MSR | Holds |
|---|---|
| `IA32_LSTAR` | **the address of the kernel's system-call entry point** |
| `IA32_STAR` | the kernel's and the user's code-segment selectors |
| `IA32_FMASK` | which `RFLAGS` bits to clear on entry — including **IF**, so interrupts are off for the first instructions |

**Now a program executes `SYSCALL`, and the CPU does all of this as one instruction:**

1. `RCX ← RIP` — the address of the next instruction, so the kernel knows where to return.
2. `R11 ← RFLAGS` — the user's flags.
3. `RFLAGS ← RFLAGS & ~IA32_FMASK` — interrupts off.
4. `CS ← ` the kernel selector from `IA32_STAR`; **the CPL is now 0.**
5. `RIP ← IA32_LSTAR` — **the kernel's entry point, which the program did not choose.**

**Notice what it does not do: it does not change `RSP`.** The kernel's first instructions run on the user's stack pointer, which the user controls completely — it could point at kernel memory, or at nothing. So Linux's entry code, `entry_SYSCALL_64`, does almost nothing before it has swapped to its own per-CPU data (`swapgs`), saved the user's `RSP`, switched to the kernel's page tables (PTI, L02 §6), and loaded a kernel stack. **Only then does it push the registers and call C.**

```
user:    mov $39, %eax     ; getpid
         syscall           ; ── ring 3 → ring 0 ──────────────────────────┐
                                                                         │
kernel:  entry_SYSCALL_64  ; swapgs, save user RSP, switch CR3 and stack │
         push registers    ; build struct pt_regs                        │
         do_syscall_64     ; sys_call_table[39]  →  sys_getpid           │
         restore registers                                               │
         sysret            ; RIP ← RCX, RFLAGS ← R11, ring 0 → ring 3 ───┘
user:    ; %rax now holds the PID
```

**The calling convention follows from step 1.** Linux passes system-call arguments in `rdi, rsi, rdx, r10, r8, r9` — and **`r10`, not `rcx`**, is fourth, because `SYSCALL` has just overwritten `rcx` with the return address. The C calling convention's fourth register is `rcx`; the system-call convention cannot use it. That one-register difference is why `syscall(2)` in glibc has to shuffle arguments.

**The return value comes back in `rax`.** A value from −4095 to −1 means an error: glibc negates it into `errno` and returns −1.

---

## 3. Watching Them: `strace`

`strace` stops a program at every system call and prints it. On the reference machine, a statically linked `printf("hello\n")`, with its output going into a pipe:

```
execve("./hello_static", ["./hello_static"], ...)       = 0
brk(NULL)                                               = 0x21b13000
brk(0x21b13d00)                                         = 0x21b13d00
arch_prctl(ARCH_SET_FS, 0x21b13380)                     = 0
set_tid_address(0x21b13650)                             = 1479460
set_robust_list(0x21b13660, 24)                         = 0
rseq(0x21b13ca0, 0x20, 0, 0x53053053)                   = 0
prlimit64(0, RLIMIT_STACK, NULL, {...})                 = 0
readlinkat(AT_FDCWD, "/proc/self/exe", ..., 4096)       = 167
getrandom("\x2f\x0b\x04\xc8\xb0\xd9\x94\x09", 8, ...)   = 8
brk(NULL)                                               = 0x21b13d00
brk(0x21b34d00)                                         = 0x21b34d00
brk(0x21b35000)                                         = 0x21b35000
mprotect(0x4a5000, 20480, PROT_READ)                    = 0
fstat(1, {st_mode=S_IFIFO|0600, ...})                   = 0
write(1, "hello\n", 6)                                  = 6
exit_group(0)                                           = ?
```

**Seventeen lines to print one line — and one of them is the line.** The first, `execve`, is the call that turned the process into this program. Everything between it and the `write` is the C runtime setting up a process: the heap (`brk`), thread-local storage (`arch_prctl`), the random canary for stack protection (`getrandom`), making the relocated data read-only (`mprotect`). The `fstat` on descriptor 1 is stdio finding out what its output is before it decides how to buffer (PROG 201 L01 §6).

**Send the output to `/dev/null` instead and there is an eighteenth line**, just after the `fstat`:

```
fstat(1, {st_mode=S_IFCHR|0666, st_rdev=makedev(0x1, 0x3), ...}) = 0
ioctl(1, TCGETS, 0x7ffd...)             = -1 ENOTTY (Inappropriate ioctl for device)
```

A pipe cannot be a terminal, so stdio does not ask. `/dev/null` is a character device, and a character device might be one, so stdio asks — with an `ioctl` that only a terminal answers — and is told no. **The program's system calls depend on where its output goes**, which is a small thing to know and a large thing to have forgotten when two traces refuse to match.

Counted with output to `/dev/null`, every line of `strace -o` output including the `execve`:

| Program | Lines of `strace` |
|---|---:|
| a program with **no C library at all** — `write` then `exit`, by hand (PS 0 Q4) | **3** — the `execve` and two calls |
| `hello`, statically linked | 18 |
| `hello`, dynamically linked | 36 |
| `/usr/bin/true` | 30 |
| `ls /` | 76 |
| `gcc -O2 hello.c` — the driver, the compiler, the assembler and the linker, with `strace -f -c` | **3,051 calls**, of which 902 failed |

**The dynamic `hello` doubles the static one** — the extra calls are the dynamic linker opening, mapping and protecting `libc.so.6`, which is PROG 201 Week 8. **And the 902 failures in `gcc` are not errors.** 481 are `EINVAL`, nearly all from `readlink` — the driver canonicalising paths by asking of each one *"is this a symbolic link?"* and being told *"no, it is an ordinary file"*. 401 are `ENOENT`: looking for a header, a library or a program in each place it might be, and trying the next place.

> **Never time anything under `strace`.** It stops the traced program twice per system call and
> switches to `strace` and back. Use it to see *what* happened, and use a clock without it to see
> *how long*.

---

## 4. What the Crossing Costs

`syscost.c` runs each operation millions of times, pinned to one CPU, and keeps the best of seven runs. On the reference machine:

| Operation | ns per call | vs a function call |
|---|---:|---:|
| a function call (`noinline`) | **0.30** | 1× |
| `clock_gettime` through the **vDSO** | **18.5** | 62× |
| `getppid()` | 592–609 | ~2,000× |
| `syscall(SYS_getppid)` | 594–601 | ~2,000× |
| `syscall(SYS_clock_gettime)` — the same clock, forced through a real trap | 635–646 | ~2,100× |
| `read(-1, …)` — fails immediately with `EBADF` | 589–597 | ~2,000× |
| **`syscall(1000)` — there is no such system call** | **572** | ~1,900× |

*Ranges are two separate runs.*

**Read the last row against the rest.** A system call that does not exist — the kernel checks the number, finds nothing, and returns `-ENOSYS` — costs **572 ns**. A system call that does real work costs 590–650. **So on this machine at least 90% of the price of a cheap system call is the door, not the room behind it.**

### Why the door is this expensive here

OSTEP's measurement aside says a modern system call is sub-microsecond, and 590 ns is. But it is not *cheap*, and the reason is in L02 §6: this CPU is one of those Meltdown and Spectre affected, and every entry and exit now does extra work.

```
$ grep . /sys/devices/system/cpu/vulnerabilities/{meltdown,spectre_v2,retbleed,mds}
meltdown:   Mitigation: PTI
spectre_v2: Mitigation: IBRS; IBPB: conditional; STIBP: conditional; RSB filling; ...
retbleed:   Mitigation: IBRS
mds:        Mitigation: Clear CPU buffers; SMT vulnerable
```

**Each line is work on the path in §2.** *PTI* switches page tables on every entry and exit. *IBRS* writes an MSR to restrict indirect-branch speculation. *Clear CPU buffers* scrubs microarchitectural state before returning to user space.

**This lecture does not split the 590 ns among them, because it cannot.** Mitigations are chosen at boot, with kernel command-line parameters, and a student account can neither change them nor reboot a shared machine. A number that cannot be measured here is not stated here. **PS 0 Q3(d) asks you what experiment would.**

### The vDSO: the system call that is not one

`clock_gettime` at **18.5 ns** is thirty times cheaper than the trap version of the same call, and it gives the same answer. It never enters ring 0.

```
$ grep -E 'vdso|vvar' /proc/self/maps
7af5a1279000-7af5a127d000 r--p  [vvar]
7af5a127d000-7af5a127f000 r--p  [vvar_vclock]
7af5a127f000-7af5a1281000 r-xp  [vdso]
```

**The kernel maps a small shared library, the vDSO, into every process**, together with read-only pages of kernel data that it keeps up to date — the current time among them. glibc's `clock_gettime` calls the vDSO's function, which reads those pages in ring 3. **Nothing privileged happens, so no door is needed.** It works only for calls that merely *read* something the kernel is willing to publish, which is why there are only a handful of vDSO functions.

### What the cost does to a program

`readsize.c` reads the same 16 MiB file, already in the page cache, with different buffer sizes:

| Buffer | `read()` calls | Total time | Per call |
|---:|---:|---:|---:|
| 1 byte | 16,777,217 | **14.213 s** | 847 ns |
| 16 bytes | 1,048,577 | 0.873 s | 832 ns |
| 512 bytes | 32,769 | 0.028 s | 862 ns |
| 4 KiB | 4,097 | 0.0057 s | 1,390 ns |
| 64 KiB | 257 | **0.0022 s** | 8,648 ns |
| 1 MiB | 17 | 0.0027 s | 158,291 ns |

**Same bytes, same file, same kernel: 14.2 seconds or 2.2 milliseconds.** Up to about 512 bytes the per-call cost is flat — it is the door — so total time is simply proportional to the number of calls. Past that, copying the bytes starts to dominate each call, and at 1 MiB total time rises slightly: the calls fell from 257 to 17 and the time did not follow them down, because by then **the cost is the copy, not the door.**

**This is why buffered I/O exists.** `fgetc` does not call `read` once per byte; stdio reads 4 KiB at a time and hands you bytes from its own buffer, in ring 3. **Every layer of batching in a system — stdio, the page cache, `io_uring`, network packet coalescing — is a way of paying for the door fewer times.**

---

## 5. The Numbers Are the Interface

A system call is identified by **a number in `rax`**, and the number is the contract. On the reference machine:

| Call | x86-64 number (`SYSCALL`) | i386 number (`int $0x80`) |
|---|---:|---:|
| `getpid` | **39** | 20 |
| `getppid` | 110 | 64 |
| `mkdir` | 83 | **39** |

**Linux keeps two tables**, one per door, and they disagree. `int80.c` makes the same request three ways from a 64-bit program:

```
getpid()                   = 1482869
syscall, rax=39            = 1482869
int $0x80, eax=20          = 1482869
int $0x80, eax=39          = -14
```

**The last line is not `getpid`.** `int $0x80` selects the i386 table, where 39 is `mkdir` — and `mkdir` was handed whatever garbage was in `ebx` as a path, which is not a valid pointer, so it returned `-14`, **`-EFAULT`**. `strace` noticed the door change and said so, on its own standard error:

```
[ Process PID=1479484 runs in 32 bit mode. ]
[ Process PID=1479484 runs in 64 bit mode. ]
```

**Numbers are never reused.** Once a number ships, some binary somewhere depends on it, so Linux adds calls at the end and never renumbers. The reference machine's headers define **373** x86-64 system calls, numbered up to **461**; the gaps are calls that were removed, or reserved and never implemented. **xv6 has 21**, numbered 1 to 21 in `syscall.h`.

---

## 6. xv6's Version, End to End

xv6 is 32-bit and uses a software interrupt rather than `SYSCALL`, but every requirement from §1 is met in the same way. **Follow `getpid` from a user program to the kernel and back:**

**1. The user stub** — `usys.S`, generated for every call by one macro:

```asm
#define SYSCALL(name) \
  .globl name; \
  name: \
    movl $SYS_ ## name, %eax; \
    int $T_SYSCALL; \
    ret
```

`getpid()` in user code is `movl $11, %eax; int $64; ret`. **The `int $64` is the door**: the only IDT gate with DPL 3 (L02 §7).

**2. The CPU**, on `int $64` from ring 3: switches to ring 0, loads the kernel stack for this process from the task-state segment, pushes the user's `SS`, `ESP`, `EFLAGS`, `CS` and `EIP` onto it, and jumps to the handler address in IDT entry 64. **Requirements 1–3, in hardware.**

**3. The vector** — `vectors.S`, line 318:

```asm
vector64:
  pushl $0          # fake error code, so every trap frame has the same shape
  pushl $64         # trap number
  jmp alltraps
```

**4. `alltraps`** — `trapasm.S` — pushes the segment registers and all general-purpose registers, which completes a `struct trapframe` on the kernel stack, loads the kernel's data segments, and calls `trap(tf)`.

**5. `trap()`** — `trap.c`, line 39 — sees `tf->trapno == T_SYSCALL` and calls `syscall()`:

```c
num = curproc->tf->eax;
if(num > 0 && num < NELEM(syscalls) && syscalls[num]) {
  curproc->tf->eax = syscalls[num]();
} else {
  cprintf("%d %s: unknown sys call %d\n", curproc->pid, curproc->name, num);
  curproc->tf->eax = -1;
}
```

**The number is checked before it is used as an index.** Without that bounds check, `eax` would be a user-chosen index into a table of function pointers — requirement 2, broken in C after the hardware met it.

**6. `sys_getpid`** — `sysproc.c` — is `return myproc()->pid;`. **Its return value is written into the saved `eax` in the trap frame**, not into the register, because the register is about to be overwritten when the trap frame is popped.

**7. Back:** `trap` returns to `trapret`, which pops the trap frame and executes `iret`, which pops `EIP`, `CS`, `EFLAGS`, `ESP` and `SS` — **and the CPL in the popped `CS` is 3.** The user program resumes at the `ret` in its stub, with the PID in `eax`.

| Step | Linux x86-64 | xv6 |
|---|---|---|
| Door | `SYSCALL` | `int $64` |
| Entry address chosen by | `IA32_LSTAR`, written at boot | IDT entry 64, written at boot |
| Stack switch | done in software by the entry code | done by the CPU, from the TSS |
| Saved registers | `struct pt_regs` | `struct trapframe` |
| Dispatch | `sys_call_table[rax]` | `syscalls[eax]` |
| Return | `SYSRET` (or `IRET`) | `IRET` |

---

## 7. What the Kernel Must Never Trust

A system call's arguments come from the program, and **every pointer among them could point anywhere** — at kernel memory, at an unmapped page, at another argument that is being changed by a second thread.

xv6 checks each one against the process's size before touching it. From `syscall.c`:

```c
int
argptr(int n, char **pp, int size)
{
  ...
  if(size < 0 || (uint)i >= curproc->sz || (uint)i+size > curproc->sz)
    return -1;
  *pp = (char*)i;
  return 0;
}
```

**A pointer is accepted only if the whole buffer lies below `sz`**, the top of the process's user memory. A program that passes a kernel address to `write` gets `-1` back instead of having the kernel copy its own memory out to a file.

**Linux does the same with `copy_from_user` and `copy_to_user`**, which check the address range and survive a fault if the page turns out to be unmapped. **The `-EFAULT` in §5 was this check working**: `mkdir` was handed a pointer that was not in the process's memory, and refused it.

> **The subtle half is time.** Checking a pointer and then reading through it is two steps, and in
> between another thread in the same process can change the memory. A kernel that reads a
> user-supplied length, checks it, and reads it again for the copy has a *time-of-check to
> time-of-use* bug. **The rule is to copy arguments into the kernel once, and check the copy.**
> Week 3 has the vocabulary for why; Week 12 has the attacks.

---

## 8. What to Take Away

1. **A system call must change the CPL, land where the kernel chose, not trust the user's state, and return.** One instruction does the first, second and fourth; the kernel's entry code does the third.
2. **`SYSCALL` saves `RIP` in `RCX` and `RFLAGS` in `R11`**, and loads `RIP` from an MSR the kernel wrote at boot. It does not switch stacks — which is why the fourth argument is in `r10`.
3. **`strace` shows the interface**: 17 lines for a static `hello` into a pipe, 3 with no libc, 3,051 calls for `gcc` — and the count changes with where the output goes.
4. **The door costs about 590 ns here, and a call that does nothing costs 572.** The vDSO avoids it entirely at 18.5 ns, for the calls that only read.
5. **Batching is how systems pay for the door less often**: a 16 MiB file read a byte at a time took 14.2 s; in 64 KiB buffers, 2.2 ms.
6. **The number is the interface, and it depends on the door**: 39 is `getpid` through `SYSCALL` and `mkdir` through `int $0x80`.
7. **Every argument is hostile until checked, and checked once.**

---

## Exercises

1. `strace -f -c make` in the xv6 directory. Which system call is made most often, and why that one?
2. Run `syscost.c` on your own machine, then `grep . /sys/devices/system/cpu/vulnerabilities/*`. Is your syscall cheaper or dearer than 590 ns? Is your list of mitigations shorter or longer?
3. Modify `readsize.c` to use `fgetc` instead of `read`, one byte at a time. Predict the total time before you run it, from the table in §4.
4. In xv6, call a system call number that does not exist — write a user program that executes `movl $99, %eax; int $64`. What does the console print, and which line of `syscall()` printed it?
5. In xv6's `argptr`, the check is `(uint)i >= curproc->sz || (uint)i+size > curproc->sz`. Why is the first comparison needed at all, when the second one looks stronger? *(Think about what `i + size` does when `i` is close to 2³².)*

---

*CS 202 · Week 0 · L03 · © CSE Department*
