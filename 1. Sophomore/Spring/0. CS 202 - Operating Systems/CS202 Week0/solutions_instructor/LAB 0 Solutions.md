# CS 202 · Lab 0 — Solutions and TA Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Session:** Friday of Week 0, 10:00–11:50, BH 210. **Unmarked** — checked off in the session.

**What the session is actually for.** Every student arrives able to write C and to call `write`. The three things they have never done, and which this lab exists to make concrete, are:

1. **seeing the system calls** underneath a program they thought was one line (Part A),
2. **being refused by the CPU** rather than by a library or a permission check (Part B),
3. **running code with nothing underneath it** — and noticing that the instruction which killed them in Part B works there (Part C).

**Q6 is the lab.** A student who can say *"the CPU executed `outb` in both; in `privfault` the CPL was 3 so it raised `#GP` instead; the kernel put `privfault` in ring 3 when it `exec`ed it"* has understood Week 0. Everything else is scaffolding for that sentence.

---

## Timing

| Minutes | Part | TA action |
|---|---|---|
| 0–10 | Setup | Walk the room. The failure is always an unquoted `$CS202` — `cp: target 'Sophomore/Spring/0.' is not a directory` |
| 10–30 | A — `strace` | Most finish in 15. Push them to actually do the `diff` for Q2 |
| 30–45 | B — `privfault` | **Insist on written predictions before they run it.** Check at least one student's sheet |
| 45–80 | C — the kernel | The hang at the start alarms people. Say "Ctrl-C" to the room at minute 46 |
| 80–105 | D — xv6 | The clone is the slow step. Start it during Part C if the network is slow |
| 105–110 | Checkoff | |

---

## Reference Solution — `kernel.c`

Tested on the reference machine: Ubuntu 24.04.4, GCC 13.3.0, QEMU 8.2.2. Builds warning-clean with the lab's `Makefile`.

```c
/* kernel.c: CS 202 Lab 0 — reference solution. */

#define COM1        0x3F8
#define DEBUG_EXIT  0xF4
#define VGA_TEXT    0xB8000

void outb(unsigned short port, unsigned char value);
unsigned get_cs(void);

static void serial_putc(char c)
{
    outb(COM1, (unsigned char)c);
}

static void serial_puts(const char *s)
{
    while (*s)
        serial_putc(*s++);
}

static void vga_puts(int row, const char *s)
{
    volatile unsigned short *cell = (volatile unsigned short *)VGA_TEXT + 80 * row;
    while (*s)
        *cell++ = (unsigned short)(0x0F00 | (unsigned char)*s++);   /* white on black */
}

void kmain(void)
{
    serial_puts("Hello from ring 0\n");

    serial_puts("CPL = ");
    serial_putc((char)('0' + (get_cs() & 3)));
    serial_putc('\n');

    vga_puts(0, "Hello from ring 0");     /* stretch: visible with a display */

    outb(DEBUG_EXIT, 0);                  /* QEMU exits with (0 << 1) | 1 = 1 */
}
```

**Output:**

```
--- booting (Ctrl-C quits if your kernel never powers off) ---
Hello from ring 0
CPL = 0
--- QEMU exited with status 1 ---
```

`size hello.elf` reports **393 bytes of text** and 16,384 of BSS (the stack). Boot-to-power-off measured at **142–152 ms** wall clock over five runs, almost all of it QEMU starting up; `strace -f -c` counts **2,026 system calls** made by QEMU to run a kernel that makes none.

---

## Answers

### Q1 — static and dynamic

With output to `/dev/null`, counting every line of `strace -o` including the `execve`: **static 18, dynamic 36**.

**Calls only the dynamic binary makes**, from the reference machine's traces:

| Call | Count | For |
|---|---:|---|
| `access("/etc/ld.so.preload", R_OK)` | 1 | checking for libraries to force-load — `ENOENT` |
| `openat` | 2 | `/etc/ld.so.cache`, then `/lib/x86_64-linux-gnu/libc.so.6` |
| `mmap` | 8 | mapping the cache and libc's segments |
| `pread64` | 2 | reading libc's ELF program headers |
| `read` | 1 | libc's ELF header |
| `close`, `munmap` | 2, 1 | done with the cache and descriptors |

**Any three with a correct purpose.** The static binary makes `readlinkat("/proc/self/exe")` and more `brk` calls instead, which the dynamic one does not; students who notice the *reverse* difference should be praised.

### Q2 — pipe against `/dev/null`

To `/dev/null` there is one extra call, right after `fstat(1, …)`:

```
ioctl(1, TCGETS, …) = -1 ENOTTY (Inappropriate ioctl for device)
```

**stdio is deciding whether `stdout` is a terminal** — line-buffered if so, fully buffered if not. `fstat` shows a pipe is `S_IFIFO`, which cannot be a terminal, so glibc does not ask. `/dev/null` is `S_IFCHR`, and a character device *might* be a terminal, so glibc asks with `TCGETS`, which only a terminal driver implements.

**Accept any answer that connects the extra call to the buffering decision.** Do not accept "because `/dev/null` is special" — it is special only in being a character device, and that is the point.

### Q3 — `ls /`

**`mmap`**, 18 of 75–76 calls on the reference machine. `ls` is dynamically linked against several libraries (`libselinux`, `libc`, `libpcre2`), and each needs several mappings. `close`, `fstat` and `openat` follow. **A student who says `getdents64`** — the call that actually reads the directory — should be told it is made only twice, because one call returns every entry of a small directory at once. That is itself Week 0's lesson: batching.

### Q4 — `privfault`

Reference output:

```
CS = 0x33, so CPL = 3

cli      disable interrupts        -> killed by SIGSEGV
hlt      halt the CPU              -> killed by SIGSEGV
inb      read I/O port 0x3f8       -> killed by SIGSEGV
outb     write I/O port 0x3f8      -> killed by SIGSEGV
rdmsr    read the TSC MSR          -> killed by SIGSEGV
mov cr3  read page-table root      -> killed by SIGSEGV
sgdt     read the GDT register     -> ran, GDT base = 0xfffffe530262c000
rdtsc    read the timestamp        -> ran
cpuid    identify the CPU          -> ran
```

**The usual wrong predictions**, and the kind of rule each involves (L02 §4):

- **`rdmsr` predicted to run** — "it only reads". Kind 1: ring 0 always. Reading MSRs leaks, among other things, the syscall entry address, which defeats KASLR.
- **`cli` predicted `SIGILL`.** Kind 2: IOPL-governed. The instruction is valid; it is disallowed, hence `#GP`, hence `SIGSEGV`.
- **`sgdt` predicted to fault.** Kind 3: allowed unless UMIP. On BH 210, `grep -c -w umip /proc/cpuinfo` is **0**.
- **`rdtsc` predicted to fault.** Kind 3: allowed unless `CR4.TSD`.

**On the `CONFIG_X86_UMIP` sentence:** the config line says the kernel *contains code to use* UMIP; it says nothing about whether the CPU implements it. Only `/proc/cpuinfo` (what the CPU reports) or running `sgdt` (what actually happens) answers the question. **The best answers say that running the instruction is stronger evidence than either file.**

### Q5 — exit status 1

`isa-debug-exit` makes QEMU exit with **`(value << 1) | 1`**, so writing 0 gives 1. **The design reason:** a guest must not be able to make QEMU exit with status 0, because 0 is what QEMU returns when it terminates normally, and automated test harnesses need to tell *"the guest reported success"* from *"QEMU exited for some other reason"*. With the shift, every guest-chosen status is odd. Accept any argument along these lines; the exact rationale is not documented in the lab and the reasoning is what is being checked.

### Q6 — the same `outb`, twice

- **In the kernel**, the CPU checked the CPL, found **0**, and **executed** `outb`: the byte went to the emulated UART and QEMU printed it.
- **In `privfault`**, the CPU checked the CPL, found **3**, and **refused**: it raised `#GP`, entered ring 0 through the kernel's IDT, and Linux sent `SIGSEGV`.

**Who decided that `privfault` runs in ring 3:** the **Linux kernel**, when it loaded the program with `execve` and returned to user mode — the return path loads a code-segment selector whose low two bits are 3. `privfault` did not choose, could not have chosen otherwise, and has no instruction available to change it.

**Do not accept** "the shell decided" or "the user decided". The shell is itself in ring 3 and asked the kernel to `execve`; nobody in ring 3 can place anything in ring 0.

### Q7 — xv6's `ls`

`ls.c` prints **name, type, inode number, size** — `printf(1, "%s %d %d %d\n", fmtname(path), st.type, st.ino, st.size)`. `stat.h` defines `T_DIR 1`, `T_FILE 2`, **`T_DEV 3`**: `console` is a **device file**, inode 19, size 0.

**xv6 has 21 system calls.** PROG 201 calls it does not have — **accept any of**: `waitpid` (only `wait`), `sigaction`/`signal` (no signals at all, only `kill`), `mmap`, `lseek`, `dup2` (only `dup`), `socket`/`accept`, `poll`/`select`/`epoll`, `getppid`. **Signals are the most striking absence**, and worth saying aloud: xv6's `kill` just sets a flag that the victim checks on its next return from the kernel.

### Q8 — `int13`

Reference output inside xv6:

```
$ int13
int13: executing int $13
pid 5 int13: trap 13 err 106 on cpu 0 eip 0x58 addr 0x0--kill proc
$ int13 cli
int13: executing cli
pid 6 int13: trap 13 err 0 on cpu 0 eip 0x5b addr 0x0--kill proc
```

**Printed by `trap()` in `trap.c`, in ring 0**, from its default case for a trap taken from user mode. `int13`'s own `"still running?"` never prints.

**Error 106 = `0x6a` = `0b1101010`**, a selector error code:

| Bits | Field | Value | Meaning |
|---|---|---|---|
| 0 | EXT | 0 | the fault was caused by the program, not an external event |
| 1 | IDT | **1** | the index refers to the **IDT** |
| 2 | TI | 0 | *(meaningful only when IDT = 0)* |
| 15–3 | index | **13** | **IDT entry 13** |

**The program tried to use gate 13; the gate's DPL is 0; the CPU raised `#GP` naming that gate.** For `cli` the error code is 0, because no descriptor was involved.

PIDs and `eip` values will differ slightly between students; the trap number and error codes will not.

---

## Common Problems

| Symptom | Cause | Fix |
|---|---|---|
| `cp: target '…' is not a directory` | unquoted `$CS202` or `$W0` | quote it |
| `gcc: error: unrecognized command-line option '-m32'` — on a laptop | no 32-bit support in the compiler | `sudo apt install gcc-multilib`, or work in BH 210 |
| `make run` prints nothing and never returns | kernel has no power-off yet (TODO 5), or an infinite loop | Ctrl-C |
| Output appears but `make run` still hangs | wrote to the wrong port, or wrote after `kmain` returned | check `DEBUG_EXIT` is `0xF4` and matches the `Makefile` |
| Garbage characters on the serial line | passed the string pointer rather than the character to `outb` | `serial_putc(*s)`, not `serial_putc(s)` |
| `undefined reference to 'strlen'` (or `memset`) | used a libc function; or GCC generated a call to one for a struct copy | write the loop yourself; `-ffreestanding` is already on |
| xv6: `error: array subscript … outside array bounds` in `mp.c` | the GCC 13 patch was not applied | re-run the `sed` from Part D |
| xv6: `Makefile:NNN: *** missing separator` after adding `_int13` | the `sed` was retyped with spaces instead of `\t` | `git checkout Makefile`, re-apply both `sed`s by copy-paste |
| xv6 boots but `int13` is "exec int13 failed" | `_int13` not in `UPROGS`, or `fs.img` not rebuilt | `grep _int13 Makefile`; `make clean && make qemu-nox` |
| Cannot leave xv6 | pressing Ctrl-C, which xv6 ignores | **Ctrl-A then X** |

---

*CS 202 · Week 0 · Lab 0 Solutions · Instructor Only*
