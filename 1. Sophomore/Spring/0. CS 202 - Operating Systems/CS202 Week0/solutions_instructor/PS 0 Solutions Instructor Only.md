# CS 202 · Problem Set 0 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for PS 0.** This is the first paper of the course. **Mark the reasoning and the evidence, not the polish.** A student who predicted wrongly, ran it, and explained the gap has done exactly what the syllabus's first habit asks and gets full marks for that part; a student who reports the lecture's numbers with no sign of having run anything does not.

**Every measured answer below was produced on the reference machine:** Intel i5-8250U, Ubuntu 24.04.4, kernel 7.0, GCC 13.3.0, glibc 2.39. **Student numbers will differ in magnitude and must not differ in shape.** In particular, a student on a newer CPU with fewer mitigations may measure a system call at 100–200 ns. That is correct, and the ratios in Q3 change accordingly.

---

## Q1: What the Mechanisms Are For (15 points)

### (a) [6]

| Mechanism | Problem it solves | Possible on MS-DOS, not on Linux |
|---|---|---|
| **Timer interrupt** | A program that never yields would keep the CPU forever; the OS needs to take the CPU back **without the program's cooperation** | `cli` followed by an infinite loop freezes the whole machine; or simply never returning to DOS |
| **U/S bit** | Programs must not read or write the kernel's memory, or each other's | Overwrite the interrupt vector table to hook every keyboard or disk interrupt — the standard technique of DOS viruses and "terminate and stay resident" programs |
| **I/O privilege level** | Only the kernel's drivers may touch device registers | Write sectors to the disk directly through the controller's ports, bypassing the filesystem — including the boot sector |

**Marking:** 1 per cell. **Accept any correct concrete example.** Reject "crash the computer" without saying how — the point is the mechanism.

### (b) [4]

- *(i)* **Mechanism** — how a trap is handled, not which process benefits.
- *(ii)* **Policy** — a choice about who gets the CPU, replaceable without changing how switching works.
- *(iii)* **Policy** — the kernel's rule about how much memory to promise; the page-fault mechanism underneath is unchanged by it.
- *(iv)* **Mechanism** — part of how the CPU finds a stack on entry to ring 0.

**Marking:** 1 each, only with a justification. *(iii)* is sometimes argued as mechanism ("it's a sysctl, it changes what the kernel does"); accept it if the student argues that the setting selects between mechanisms, not merely that it is configurable.

### (c) [5]

**Reference numbers:** one round trip into the kernel and back ≈ **590 ns**.

The four crossings in the question are **two entries and two exits** — two round trips — plus two switches of address space (application → server → application), which a monolithic `read` does not do. So the added cost is **at least one extra round trip, ≈ 590 ns per `read`**, and more once the address-space switches are counted. **A student who takes "four crossings" as four times 590 ns (≈ 2.4 µs total, ≈ 1.8 µs added) is also acceptable** if they say what they are counting.

**Where it matters**, from L03 §4's table:

- **1-byte reads**: 16,777,217 calls. An extra ≈ 590 ns each adds **≈ 9.9 s** to a 14.2 s run — roughly **70% slower**.
- **64 KiB reads**: 257 calls. The same overhead adds **≈ 0.15 ms** to 2.2 ms — about **7%**.

**The argument the marks are for:** the microkernel's overhead is **per call**, so it matters in proportion to the number of calls, not the amount of work. **Batching, which Linux programs already do for other reasons, is what makes microkernels viable.** 2 for a defensible number, 3 for the workload argument.

---

## Q2: The Wall (20 points)

### (a) [8]

Reference results, from ring 3:

| Instruction | Result |
|---|---|
| `lgdt` | **SIGSEGV** — ring 0 only |
| `sti` | **SIGSEGV** — IOPL-governed, like `cli` |
| `int3` | **SIGTRAP** — a breakpoint exception, delivered as a signal. This is how debuggers work |
| `ud2` | **SIGILL** — `#UD`, invalid opcode, by design |
| `wrmsr` to `IA32_LSTAR` | **SIGSEGV** — ring 0 only |
| `pause` | **ran** |
| `int $0x80`, `eax = 20` | **ran** — returned the PID |

**The two not killed, for different reasons:**

1. **`pause` is not privileged at all.** It is a hint to the CPU that the program is in a spin loop, and does nothing a program should be prevented from doing.
2. **`int $0x80` is a door.** It is an interrupt through an IDT gate **whose DPL is 3** — the kernel opened it deliberately as the legacy system-call entry. `eax = 20` is `getpid` in the i386 table.

**Marking:** 4 for the table (partial credit for predictions honestly wrong and then reported correctly), 4 for the two reasons. **The key discrimination is between "not privileged" and "privileged but permitted through a gate"**; a student who says both are "allowed" without distinguishing gets 2 of the 4.

### (b) [6]

- **Allow:** `rdtsc` gives a high-resolution timestamp with **no system call**, which profilers, databases and runtimes use millions of times a second. Forcing a trap would cost ~590 ns per timestamp here — L03 §4.
- **Forbid:** **timing side channels.** Cache-timing attacks — including the Spectre family — need a precise clock to tell a cache hit from a miss. A sandbox that denies untrusted code a fine-grained clock makes those attacks much harder.

**What the kernel changes, and when:** `prctl(PR_SET_TSC, PR_TSC_SIGSEGV)` marks **the calling thread** as not allowed `rdtsc`. **On every context switch into that thread, the kernel sets the `TSD` bit in `CR4`**, and on switching to a thread without the mark, clears it. The CPU then faults any ring-3 `rdtsc` while the bit is set. **The key is that `CR4` is per-CPU hardware state and the setting is per-thread, so the kernel reconciles them at every switch.**

**Marking:** 2 + 2 + 2. The last 2 require "`CR4.TSD`" (or "a control-register bit") **and** "on context switch".

### (c) [6]

Reference: `umip` count **0**; `CONFIG_X86_UMIP=y`; `sgdt` **ran** and returned **`0xfffffe530262c000`**.

**Kernel address**: it is in the upper, canonical half of the 48-bit address space — at or above `0xffff800000000000` — which on Linux x86-64 is the kernel's half. Student values will differ; any `0xffff…` value is a kernel address.

**The three sentences:** the config line records that the kernel was **built with code to use** UMIP; `/proc/cpuinfo` records whether **the CPU has** the feature; the two are independent, and only the second — or better, **executing the instruction and observing the result** — tells you whether the protection is in force on this machine.

**Marking:** 2 for results, 1 for kernel address with reason, 3 for the argument. **Full marks require saying that trying the instruction is the reliable test.** A student whose CPU *does* have UMIP will see `sgdt` fault (or, on some kernels, be emulated with a dummy value) — that is a correct result, and the argument is the same.

---

## Q3: What the Door Costs (25 points)

### (a) [8]

Reference table (two runs, ns per call):

```
function call (noinline)                          0.30
clock_gettime  (vDSO, no trap)                   18.52
getppid()      (glibc wrapper)                  591.57 – 608.75
syscall(SYS_getppid)                            593.75 – 600.90
syscall(SYS_clock_gettime) (forced trap)        634.86 – 645.95
read(-1, ...)  (fails with EBADF)               589.02 – 597.02
syscall(1000)  (no such call: ENOSYS)           571.60 – 572.09
```

- `syscall(SYS_getppid)` / function ≈ **2,000×**.
- `syscall(SYS_clock_gettime)` / vDSO ≈ **34×**.

**The second ratio:** the vDSO function reads the time from **kernel-maintained pages mapped read-only into the process** and computes the result **in ring 3**. The trapping version enters ring 0 to do the same arithmetic. **The work is identical; the door is the difference.**

**Could `getppid` go in the vDSO?** Only if the kernel published each process's parent PID in a per-process page and **updated it whenever the parent changes** — which happens when the parent exits and the process is re-parented (PROG 201 L02). It is possible in principle, and an unattractive trade for a call nobody makes in a hot loop. **A student who notes that glibc once cached `getpid` in user space and removed the cache (glibc 2.25) because it went stale across `clone` deserves credit** — it is exactly this problem.

**Marking:** 3 for the table with machine details stated, 2 for the ratios, 3 for the explanation. **Any argued answer to the `getppid` question** — yes with the update cost, or no because of it — earns the last mark.

### (b) [5]

Reference: **572 ns** for `ENOSYS` against **594 ns** for `getppid`. **At least 90% of a cheap system call's cost is the entry and exit, not the call.**

**On every entry and exit, whatever the number** — accept any two:

- the **`SYSCALL`/`SYSRET` transitions** themselves, and the stack switch;
- **saving and restoring registers** into `pt_regs`;
- **PTI's page-table switch** (`CR3` write) on entry and exit;
- **IBRS's MSR write** on entry and exit (retbleed / Spectre v2 mitigation);
- **clearing CPU buffers** before returning to user space (MDS mitigation);
- the bounds check on the syscall number itself.

**Marking:** 2 for the numbers and the conclusion, 3 for two correct per-entry costs. **Do not accept** "the kernel has to look up the function" as a significant cost — it is one array index.

### (c) [7]

Reference (16 MiB file, page cache warm):

| Buffer | `read()` calls | Total | Per call |
|---:|---:|---:|---:|
| 1 | 16,777,217 | 14.213 s | 847 ns |
| 16 | 1,048,577 | 0.873 s | 832 ns |
| 4,096 | 4,097 | 0.0057 s | 1,390 ns |
| 65,536 | 257 | 0.0022 s | 8,648 ns |

- **Per call flat, then rising:** for small buffers the cost of a call is the door, which does not depend on the buffer. For large buffers the kernel spends time **copying bytes** from the page cache into the user buffer, and that is proportional to the buffer size.
- **Total falls by more than three orders of magnitude** because total ≈ *calls × (door + copy)*: shrinking the number of calls by 65,536× removes almost all of the door cost, while the copy cost — the same 16 MiB either way — is small by comparison.
- **`fgetc` — predict, then measure.** Reference: **0.047 s, with 4,098 `read` calls** (from `strace -c`). **Its number of `read` calls matches the 4,096-byte row**, because stdio reads 4 KiB at a time into its own buffer. **Its total time is ≈ 8× the 4,096-byte row**, because `fgetc` is itself a function call per byte that takes and releases the `FILE`'s lock. **A student who predicts "like the 1-byte row" and measures otherwise, and explains the stdio buffer, gets full marks.** A student who notices the 8× and attributes it to per-byte locking (or tries `getc_unlocked`) deserves a comment of praise.

**Marking:** 2 for the table, 2 + 1 for the two explanations, 2 for `fgetc` with a measurement.

### (d) [5]

Reference `Mitigation:` lines: `meltdown` (PTI), `spectre_v1`, `spectre_v2` (IBRS; IBPB/STIBP conditional; RSB filling), `retbleed` (IBRS), `mds`, `mmio_stale_data` (clear CPU buffers), `spec_store_bypass` (via `prctl`), `srbds` (microcode), `l1tf` (PTE inversion), `itlb_multihit` (KVM), `vmscape` (IBPB before exit to userspace).

**Why not from `syscost.c` alone:** it measures the **sum** of every entry and exit cost on this configuration. Every mitigation is active in every measurement, so there is **no variation to attribute** — one number, many causes.

**The experiment:** boot the same kernel repeatedly, each time **disabling one mitigation** with its kernel command-line parameter (`nopti`, `retbleed=off`, `spectre_v2=off`, `mds=off`, …, or `mitigations=off` for all), run `syscost.c` under identical conditions (pinned CPU, same load, several runs, best-of), and **compare each against the all-on baseline.** Mitigations can interact, so a careful version also measures all-off and turns them on one at a time.

**Access needed:** **root, to change the boot parameters, and the ability to reboot the machine** — neither of which a student has on a shared lab image. **A student who proposes doing it inside a VM (Week 10) should be told it is a reasonable idea with a catch**: a guest's syscall cost includes virtualization effects, so the absolute numbers would not transfer, though differences between guest configurations might.

**Marking:** 1 for the list, 2 for why not, 2 for an experiment that changes one thing at a time and names the access required.

---

## Q4: The Trap by Hand (25 points)

### (a) [10]

Reference:

```c
/* nolibc.c: a program with no C library at all, and two system calls made by hand. */
__asm__(
    ".section .rodata\n"
    "msg:    .ascii \"hello, with no libc\\n\"\n"
    "        .set len, . - msg\n"
    ".text\n"
    ".globl _start\n"
    "_start:\n"
    "        mov  $1, %eax\n"          /* write(2) */
    "        mov  $1, %edi\n"
    "        lea  msg(%rip), %rsi\n"
    "        mov  $len, %edx\n"
    "        syscall\n"
    "        mov  $60, %eax\n"         /* exit(2)  */
    "        xor  %edi, %edi\n"
    "        syscall\n");
```

```
$ strace ./nolibc
execve("./nolibc", ["./nolibc"], 0x7ffc13599f70 /* 89 vars */) = 0
write(1, "hello, with no libc\n", 20)   = 20
exit(0)                                 = ?
+++ exited with 0 +++
```

**Size: 9,168 bytes**, against **785,360** for a statically linked `printf` version — 86× smaller.

**A version in C with a static function wrapping `syscall` via inline assembly is equally acceptable.** The requirements are `-nostdlib`, `_start` provided, `SYSCALL` used directly, and exactly two calls after `execve`.

**Common error, worth a comment rather than a deduction:** a static `const char msg[]` referenced from a top-level `__asm__` block fails to link (`undefined reference to 'msg.0'`), because the compiler gives function-local statics a mangled name. Students hit exactly this on the reference machine's first attempt too.

**Marking:** 5 for a working program, 3 for the trace showing exactly two calls, 2 for the size comparison. **Deduct 3 if the program returns from `_start`** — there is no caller to return to, and it will crash (`SIGSEGV`) after printing, which `strace` shows.

### (b) [5]

- **`RCX ← RIP`** of the next instruction — the return address.
- **`R11 ← RFLAGS`** — the user's flags, restored by `SYSRET`.

**`r10` instead of `rcx`:** `SYSCALL` has **already overwritten `rcx`** by the time the kernel could look at it, so the fourth argument cannot travel there. The system-call ABI therefore moves the fourth argument to `r10`, and glibc's `syscall()` wrapper shuffles it from `rcx` (where C put it) into `r10` before `SYSCALL`.

**Marking:** 1 + 1 for the registers, 3 for `r10` with the reason.

### (c) [5]

Reference: **returned `-14`**, and `strace` prints `[ Process PID=… runs in 32 bit mode. ]` (then `… runs in 64 bit mode.` when the program returns to the 64-bit path).

**Explanation:** `int $0x80` enters through the **legacy i386 entry**, which dispatches on the **i386 system-call table**. In that table **39 is `mkdir`**, not `getpid`. `mkdir` took its path pointer from `ebx`, which held whatever the program happened to leave there — not a valid user pointer — so the kernel's `copy_from_user` check failed and it returned **`-EFAULT`** (14). `strace` notices the change of ABI and reports it.

**Marking:** 1 for the value, 1 for the strace line, 3 for "i386 table", "39 is `mkdir`", and "`EFAULT` because the pointer argument was garbage". A student who says "it called `getpid` but failed" gets 1 of the 3.

### (d) [5]

**The attack:** before `SYSCALL`, a user program sets `RSP` to **a kernel address** — for example, just above the kernel's own credentials structure, or the system-call table. If the entry code pushed registers onto "the stack" it found in `RSP`, **the kernel would write user-controlled values** (the saved registers, which the attacker chose) **into kernel memory at an attacker-chosen address.** That is an arbitrary kernel write, and an arbitrary kernel write is a privilege escalation: overwrite your process's UID with 0, or a function pointer with an address of your choosing.

**Equally acceptable:** set `RSP` to an unmapped address, so the kernel's first push page-faults **in ring 0 on its own entry path** — a crash of the whole machine from an unprivileged program.

**Worth a bonus remark if a student finds it:** this class of bug is real. **CVE-2012-0217** was a `SYSRET` return-path flaw on Intel CPUs in several operating systems, in which the CPU could raise a fault in ring 0 while still using a user-supplied stack pointer.

**Marking:** 2 for "point `RSP` at kernel memory", 3 for what the push then does and why it is an escalation (or a crash, argued).

---

## Q5: xv6 (15 points)

### (a) [5]

| Step | File | Function or label | What it does |
|---|---|---|---|
| 1 | `usys.S` | `getpid` (from `SYSCALL(getpid)`) | `movl $SYS_getpid, %eax` (11); **`int $T_SYSCALL`** |
| 2 | — | *the CPU* | **CPL 3 → 0 at `int $64`.** Switches to the kernel stack from the TSS; pushes `ss`, `esp`, `eflags`, `cs`, `eip`; jumps to IDT entry 64 |
| 3 | `vectors.S` | `vector64` | pushes a fake error code 0 and the trap number 64; `jmp alltraps` |
| 4 | `trapasm.S` | `alltraps` | pushes segment and general registers — completing `struct trapframe` — loads kernel data segments, `call trap` |
| 5 | `trap.c` | `trap` | `tf->trapno == T_SYSCALL`: stores `tf`, calls `syscall()` |
| 6 | `syscall.c` | `syscall` | reads `eax`, bounds-checks it, calls `syscalls[11]`, **stores the result in `tf->eax`** |
| 7 | `sysproc.c` | `sys_getpid` | `return myproc()->pid;` |
| 8 | `trapasm.S` | `trapret` | pops the trap frame; **`iret` — CPL 0 → 3**, popping a `cs` with RPL 3 |
| 9 | `usys.S` | `getpid` | `ret` to the caller, with the PID in `eax` |

**Marking:** 3 for a complete, ordered path with files; **2 for correctly naming `int $T_SYSCALL` and `iret` as the two CPL changes.** Deduct 1 if the student says `ret` in `usys.S` returns to ring 3 — by then it is already in ring 3.

### (b) [5]

**Prediction:** `argptr` rejects the pointer because `0x80100000 >= curproc->sz` — a user process's size is a few tens of kilobytes — so `sys_write` returns **−1** without touching the buffer.

**Reference result**, from a test program on the reference machine:

```
$ writek

writek: write returned -1
```

**An unprotected kernel would have written the first 16 bytes of its own image** at `KERNLINK` (`0x80100000`) to the console. In xv6 those bytes begin with **the Multiboot header from `entry.S`** — the magic `0x1BADB002`, stored little-endian as `02 b0 ad 1b` — followed by the flags and checksum: mostly unprintable garbage on a terminal, and **a kernel memory disclosure** in principle.

**Marking:** 2 for the prediction with `argptr`'s check named, 1 for the measured result, 2 for what would have leaked. A student who says "the kernel's code" without identifying the Multiboot header gets full marks; identifying it is a bonus remark.

### (c) [5]

**106 = `0b0000000001101010`**:

| Field | Bits | Value | Meaning |
|---|---|---|---|
| **EXT** | 0 | 0 | caused by the program, not an external event |
| **IDT** | 1 | 1 | the index refers to an **IDT** entry |
| **TI** | 2 | 0 | ignored when IDT = 1 |
| **Index** | 15–3 | 13 | **IDT entry 13** |

**What it says:** the program executed `int` naming **gate 13**; gate 13's DPL is 0 (`trap.c` line 23); the CPU refused the transfer and raised `#GP` **about gate 13**.

**With `int $64` instead — reference result:**

```
$ int64
int13: executing int $64
int13: still running?
int13: still run$ ning?
zombie!
```

**It is not killed, because gate 64 is the one with DPL 3 — it is a system call.** The system call made is whatever number happened to be in `eax`. On the reference machine that was **1**, `SYS_fork`: the last thing `printf` did was a `write` of one character, which returned 1 into `eax`. **The program forked.** Both copies printed `still running?` — interleaved, which is why the line is torn — and the parent exited without waiting. The orphaned child was re-parented to `init`, and `init`'s loop printed `zombie!` when it reaped a process that was not the shell.

**Marking:** 2 for decoding with correct fields, 1 for what it means, 2 for the `int $64` behaviour. **Full marks for the last part do not require identifying `fork`** — "it is a system call through the open gate, with whatever was in `eax`, so it is not killed" earns both marks. A student who works out `fork` from the doubled line and `zombie!` deserves a comment, because that is Week 1's material deduced from Week 0's.

---

*CS 202 · Week 0 · PS 0 Solutions · Instructor Only*
