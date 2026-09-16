# CS 202 · Reading Guide · Week 9
## I/O and Device Drivers: OSTEP 36–37, xv6's Drivers, and the Module That Will Not Load

---

**The curriculum names no reading for Week 9.** **Read OSTEP 36 before Wednesday** — it is the whole shape of the week — and **read xv6's `console.c` and `ide.c`**, which are the two drivers you will extend.

> **This week also assigns Project 2**, due in the completion period, and **Project 1 is due in two
> weeks.** The reading below is short for that reason.

| Source | Now? | Why |
|---|---|---|
| **OSTEP 36. I/O Devices** | **Read** | The canonical device: status, command and data registers; polling against interrupts; DMA; the device driver as an abstraction layer. **L28, L29** |
| OSTEP 37. Hard Disk Drives | *Skim §37.1–§37.4* | Where the block layer's scheduling ideas come from — even on an SSD that has no seek. **L29 §5** |
| **xv6 book (x86, rev. 11), Ch. 3 §3.5–§3.6 and Ch. 4** | **Read, with `trap.c`, `console.c`, `uart.c` open** | Interrupts, and the console driver you extend in PS 9. **L28 §4, L29 §2** |
| xv6 book, Ch. 6's `ide.c` section | *Read* | A block driver: a queue, an interrupt handler, and `sleep`/`wakeup`. **L29 §3** |
| **Corbet, Rubini & Kroah-Hartman, *Linux Device Drivers*, 3rd ed., Ch. 1–3** | **Read Ch. 3** | `file_operations`, `register_chrdev`, `copy_to_user` — free online. **L30** |
| Love, Ch. 7 "Interrupts and Interrupt Handlers" | *Reference* | Top halves, bottom halves, and why a handler may not sleep | 
| `man 4 null`, `man 2 ioctl`, `man 5 proc` under `/proc/interrupts` | **Before Lab 9** | The files and calls the lab reads |

**If you have two hours:** OSTEP 36, then LDD3 Chapter 3, then xv6's `console.c` from `consoleread` to `consoleintr`.

---

## OSTEP 36 — devices

1. OSTEP's canonical protocol polls a status register, writes a command, then polls again. **Where does the CPU time go**, and at what device speed does polling beat interrupts? *(L29 §4 measures the modern version of this question.)*
2. **Why does a slow device favour interrupts and a fast one favour polling?** Give the threshold in terms of the interrupt cost and the device's service time.
3. §36.5 introduces **DMA**. **What exactly does the CPU no longer do**, and what must it still do for every transfer?
4. §36.6 distinguishes **port-mapped** from **memory-mapped** I/O. Find one of each in xv6 — `uart.c` uses one, `lapic.c` the other — and say how you can tell from the code.
5. OSTEP's driver abstraction ends with "the file system is written to a generic block interface". **In xv6, name the structure that is that interface** (L28 §4), and the two function pointers it holds.

---

## xv6's drivers

6. `consoleread` calls `sleep(&input.r, &cons.lock)` while the buffer is empty, and `consoleintr` calls `wakeup(&input.r)`. **Which Week 3 pattern is this**, and what would break if `consoleintr` tried to take a sleeping lock instead?
7. **An interrupt handler in xv6 may not sleep.** Find the reason in `trap.c`: **whose stack and whose process context is the handler running on?**
8. `ide.c` keeps a queue of buffers and starts the disk for the head of the queue only. **What wakes the process that was waiting for a block**, and how does it know its block arrived rather than someone else's?
9. `uartintr` reads one character per interrupt. **At 115,200 baud, how many interrupts per second is that**, and what does the same calculation give for an NVMe disk at 1.6 GB/s in 4 KiB blocks? *(L29 §4 measured the real number.)*

---

## LDD3 Chapter 3 — the Linux module

10. A Linux character driver fills in a `struct file_operations`. **List the four entries that correspond to `open`, `read`, `write`, `close`**, and say what xv6's `devsw` has instead.
11. **Why can a driver not simply dereference the pointer a user passed to `write`?** Name the two functions that do it properly, and the two distinct things that can go wrong without them. *(Week 5 L18 §2 met one of them.)*
12. LDD3 says a module may not use floating point or the C library. **Give the reason for each** — one is about saved state (Week 1 L05 §6), the other about what is linked into the kernel.
13. `register_chrdev` returns a major number. **What does `mknod` then do**, and what is the equivalent step in xv6's PS 9 device?

---

## Where to Go Deeper

| Source | Topic | When |
|---|---|---|
| Kernel documentation, `block/blk-mq.rst` (online) | Multi-queue block layer — this machine has five hardware queues | For L29 §5 |
| **Love**, Ch. 17 "Devices and Modules" | The device model, `sysfs`, and how `/dev` is populated | For L30 |
| `man 8 lsmod`, `man 8 insmod`, `man 7 capabilities` (`CAP_SYS_MODULE`) | Why Lab 9's module will not load | **Before Lab 9** |
| Kernel documentation, `admin-guide/sysrq.rst` | What a driver bug looks like from the outside | *Optional* |

---

*CS 202 · Week 9 · Reading Guide · © CSE Department*
