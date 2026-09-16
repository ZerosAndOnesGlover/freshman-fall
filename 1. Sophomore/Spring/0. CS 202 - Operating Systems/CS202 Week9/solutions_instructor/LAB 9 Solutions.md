# CS 202 · Lab 9 — Solutions and TA Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Session:** Tuesday of Week 10, 15:00–16:50, BH 210. **Unmarked** — checked off in the session.

**What the session is actually for.** Students have now written a driver (PS 9) and read about interrupts (L29). **This lab is where the numbers arrive**: what a device call costs when the device does nothing, how many interrupts the same 256 MiB costs at two request sizes, and what three deliberate bugs do to a working driver.

**Part D is the best twenty minutes of the week** — students break their own driver three ways and watch each failure. **Do not let them skip it to finish PS 9.**

---

## Timing

| Minutes | Part | TA action |
|---|---|---|
| 0–20 | A | The build takes a minute; `insmod` fails instantly. Discuss why while it builds |
| 20–45 | B | Straightforward; the interesting part is Q6 |
| 45–70 | C | `dd` with `iflag=direct` is the whole trick; check nobody forgets it |
| 70–95 | **D** | **Three rebuilds.** Each is one line changed; keep them moving |
| 95–110 | Checkoff | |

---

## Answers

Reference machine: i5-8250U, kernel 7.0.0-31, NVMe SSD, GCC 13.3.0.

### Q1 — the size of a module

```
$ ls -la cs202ring.ko
330976 cs202ring.ko
$ size cs202ring.ko
   text    data     bss     dec     hex filename
   1604    1328       4    2936     b78 cs202ring.ko
```

**1,604 bytes of code in a 330 KB file. [2]**

**The rest [3]:** an ELF **relocatable** object, not an executable — it carries **symbol tables and relocations** for every kernel symbol it calls, **`.modinfo`** (the strings `modinfo` prints), the **`__versions`/BTF and debug sections** the kernel build adds, and the module-loader metadata. **`objdump -h` shows them**; a `strip --strip-debug` removes most of the bulk and the module still loads.

*(A student who says "debug symbols" earns the marks; the point is that the code is tiny and the metadata is not.)*

### Q2 — the refusal

```
insmod: ERROR: could not insert module cs202ring.ko: Operation not permitted
```

**`CAP_SYS_MODULE` [2].** **What a module could do [2]:** run in kernel mode with no restrictions — read every process's memory, hook every system call, disable `ptrace_scope`, turn off the OOM killer, hide itself from `lsmod`. **There is no smaller privilege: a loaded module *is* the kernel.**

**What you can still do [1]:** build it, read its metadata (`modinfo`, `size`, `objdump`), and list what is loaded (`lsmod`, `/proc/modules`). **Accept any two.**

### Q3 — `vermagic`

**A string recording the kernel version, SMP setting, preemption model and compiler ABI the module was built against. [2]**

**If it does not match, the load is rejected** — the module is refused rather than run. **[1]**

**Why 7.0.0-31 and -30 differ [2]:** a module is **linked against the kernel's internal symbols and structure layouts**, which are not a stable interface: a field added to `struct file` or a changed inline function silently breaks a module built for a different build. **Linux deliberately has no stable in-kernel ABI**, which is why distributions rebuild every module for every kernel.

### Q4 — what a device call costs

| | 4 bytes | 4 KiB |
|---|---:|---:|
| `/dev/null` (write) | **659 ns** | 684 ns |
| `/dev/zero` (read) | 687 ns | 882 ns |
| `/dev/urandom` (read) | 946 ns | **12,689 ns** |
| a cached file (read) | 819 ns | 1,064 ns |
| `ioctl` (`ENOTTY`) | **595 ns** | |
| `poll`, ready | 673 ns | |

**`/dev/null`'s 659 ns is [4]:** the `syscall` instruction and `sysret`; **two `CR3` switches for page-table isolation** (Week 5 L17 §5) — the reason a call costs hundreds of nanoseconds on this machine rather than tens; the file-descriptor table lookup and reference count; and **the indirect call through `file_operations`**, which is the only part the driver author writes.

**Against `getppid` at ~590 ns (Week 0):** the extra ~70 ns is the descriptor lookup and the dispatch. **Accept any answer that identifies the system call as the dominant term.**

### Q5 — per-byte work

**`/dev/zero`: (882 − 687) / 4,092 ≈ 0.05 ns per byte** — `memset`. **`/dev/urandom`: (12,689 − 946) / 4,092 ≈ 2.9 ns per byte** — generating randomness, roughly sixty times dearer. **[3]**

**Which benefits from `mmap` [2]: `/dev/zero`** — its whole cost is the call, and mapping it removes the call entirely (`mmap` of `/dev/zero` is how anonymous memory used to be requested). **`/dev/urandom` cannot benefit**: its cost is real computation that must happen per byte however it is reached.

### Q6 — the `ioctl` line

**`ioctl` returning `ENOTTY` is the cheapest line (595 ns) and does nothing at all**: it enters the kernel, looks up the descriptor, calls the driver, and returns an error. **So ~600 ns is the floor for *any* interaction with a device** — every other line's excess is the device's own work, and nothing in the table is dominated by the driver's dispatch. **[3]**

### Q7 — interrupts, two ways

| Request size | Interrupts | Requests | Per request | Elapsed |
|---|---:|---:|---:|---:|
| **1 MiB** | **1,969** | 256 | **7.7** | 0.136 s |
| **4 KiB** | **65,536** | 65,536 | **1.00** | 1.115 s |

**Same 256 MiB; 33 times the interrupts and 8 times the time. [4]**

### Q8 — where 7.7 comes from

```
$ cat /sys/block/nvme0n1/queue/max_sectors_kb
128
```

**The block layer splits every request at 128 KiB**, so a 1 MiB read becomes **eight** commands, each completing with one interrupt: **8 × 256 = 2,048 expected, 1,969 measured** — slightly fewer because the driver coalesces completions that arrive together (one interrupt can reap several finished commands from the queue). **[4, and give full marks for 8 with the `max_sectors_kb` reasoning even without the coalescing remark.]**

### Q9 — `none`, and eight queues

```
scheduler: [none] mq-deadline        hardware queues: 8        nr_requests: 1023
```

**Why `none` [3]:** the scheduler's historic job was **reordering to minimise seeks** (OSTEP 37). **This device has no seek**, serves many commands at once from a 1,023-deep queue, and reorders internally — so software reordering adds latency and CPU and buys nothing. `mq-deadline` remains available for workloads that need fairness or read-priority guarantees.

**One queue per CPU [2]:** submission takes **no shared lock** — two CPUs issuing I/O do not contend — which is what let Linux scale past a few hundred thousand IOPS. **Completion interrupts are also steered per queue**, which is why `/proc/interrupts` shows the disk's interrupts landing on one CPU per queue.

### Q10 — the blocking read

```
$ ringtest 300
parent: reading (this blocks until the child writes)
parent: read 300 bytes of 300; the last byte was 'n', which is byte 299
```

**The child sleeps 20 ticks before opening the device**, so for those ticks the parent was **inside `ringread`, asleep on `&ring.r`** — it had already printed its line and could be nowhere else. **The two lines that put it there [3]:** the `while(ring.r == ring.w)` loop and the `sleep(&ring.r, &ring.lock)` inside it.

### Q11 — three deliberate bugs

| Change | What happens | What it is |
|---|---|---|
| **remove `wakeup(&ring.r)`** | `ringtest` **hangs forever**; the shell does not return; the machine is idle | **A lost wake-up** (Week 3 L12 §2) — and from `top`'s point of view, Week 4 L15 §3's invisible deadlock: everything asleep, nothing wrong |
| **`if` instead of `while`** | usually works; **occasionally returns 0 bytes or reads garbage** when the reader wakes and another reader or a partial write has changed the state | **Mesa semantics** (L12 §2): being woken is not being right |
| **return `n` instead of the count** | `ringtest` reports **more bytes than were written**, and the extra bytes are **whatever was in the user's buffer** | **The worst of the three** |

**Why the third is worst [3]:** the first two **fail loudly or intermittently in the driver's own test**; the third **succeeds**. Every program that trusts the return value — which is every program — silently processes uninitialised memory, and on Linux the same bug leaks kernel data to user space. **A driver that lies about how much it did is worse than one that hangs.**

---

## Common Problems

| Symptom | Cause | Fix |
|---|---|---|
| `make` in `linux/` fails with `Syntax error: "("` | the path contains parentheses — the vault's own path does | build from a copy in `$CS202/week9/lab9`, as the handout says |
| `insmod` says "Invalid module format" instead of "Operation not permitted" | built against a different kernel | `uname -r` against `modinfo`'s `vermagic` |
| Interrupt counts identical for both `dd` runs | forgot `iflag=direct`; the second read came from the page cache | re-run with it, and check `Cached` in `/proc/meminfo` |
| Interrupt delta is negative or huge | another process is doing I/O | run the two `dd`s back to back and take the difference across each |
| `ringtest` prints nothing and the shell hangs | the driver never wakes the reader — Q11's first bug, arrived at accidentally | Ctrl-A X, then look at `ringwrite` |

---

*CS 202 · Week 9 · Lab 9 Solutions · Instructor Only*
