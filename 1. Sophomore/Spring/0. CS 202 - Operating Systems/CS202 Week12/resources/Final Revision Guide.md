# CS 202 · Final Revision Guide
## One idea and one number, per week

---

**The final is comprehensive, two and a half hours, 100 marks, two handwritten pages permitted.**

**This page is not a summary of the course.** It is an index: **if you can reconstruct the reasoning behind each line, you are prepared; if a line surprises you, go back to that week.** Orders of magnitude are what the paper asks for.

---

| Week | The one idea | The one number |
|---|---|---|
| **0** | **A system call is a trap, not a jump** — the entry point is in a register only ring 0 can write, so the crossing cannot be redirected, and it has a fixed cost regardless of how much work you ask for | **16 MiB read one byte at a time: 14.213 s; at 64 KiB: 0.0022 s — 6,400×** |
| **1** | A process is a table entry; **a context switch saves what the next thread might notice** — and what the kernel forgets to save is a correctness bug, not a performance one | **1,622 ns same CPU, 2,139 ns across CPUs** — and **xv6 does not save the FPU at all** |
| **2** | Scheduling is policy over one mechanism; **"real time" means a deadline you can state, and Linux will only promise what the hardware's wake-up latency allows** | **timer wake-up 144 µs idle, 4 µs busy with slack at 1 ns; deepest C-state exit 890 µs** |
| **3** | A lock is an agreement about a memory location, made possible by one atomic instruction; **the fast path must not enter the kernel** | **uncontended futex 14.8 ns and 0 system calls; a contended shared atomic 29–32 ns** |
| **4** | Deadlock needs four conditions at once, so **breaking any one is enough** — and avoidance requires knowing the future, which is why no OS does it | **the Banker's safety check: 20.590 ms at 3,200 processes** — O(*n*²*m*), and that is why |
| **5** | Translation is a table walk the MMU does on **every** access, so it must be cached; **demand paging and copy-on-write are both "allocate at the fault"** | **page fault 1,833–1,949 ns; COW fault 2,957 ns; TLB gap 17.3 ns at a 2 GiB working set** |
| **6** | Replacement is a guess about the future, and **thrashing is the guess being wrong every time** — the collapse is abrupt because a fault evicts the page about to be used | **21.7M reads/s unrestricted against 14,775/s at 64 MiB — about 1,500×** |
| **7** | A file is an inode and a cache; **the page cache is why storage looks fast, and it is also why nothing you wrote is on the disk yet** | **cold random 4 KiB read 93.9 µs, warm 1.61 µs — 58×; `fsync` of 64 MiB: 41 ms against 15 ms to write it** |
| **8** | Crash consistency is an ordering problem; **write-ahead logging makes the order enforceable, and the barrier is what enforces it** | **36 of 93 crash points left the file system broken without a journal; the journal cost +21% on scattered writes** |
| **9** | Every device is the same three things — **a register interface, an interrupt, and a ring** — and the driver's job is to make them look like a file | **`/dev/null` write 659 ns, `ioctl` 595 ns; 1 MiB reads took 1,969 interrupts against 65,536 for 4 KiB** |
| **10** | A virtual machine is a process whose system calls are **VM exits**; the hypervisor's whole job is to arrange not to exit | **a VM exit: 7,806 ns — nine system calls; hardware virtualisation bought between nothing and 25%** |
| **11** | With two machines there is no shared memory, no common clock, and **failure is indistinguishable from slowness**; agreement is manufactured by counting votes per term | **a round trip to another machine: 22.6–24.5 ms — 13,000,000 function calls** |
| **12** | **Least privilege is the only principle that does not assume your code is correct**; every other defence is a mitigation that leaves the bug in place | **a seccomp filter costs ≈ 50 ns per system call — about 6% — and the cost does not depend on the number of rules** |

---

## The two habits, which are examinable

**1 · A protection that is switched on is not a protection that works.**

> This kernel is built with `CONFIG_X86_UMIP=y`. **The CPU does not implement UMIP.** In Week 12,
> under every protection in the course, `sgdt` still printed a live kernel address from user mode.
> **Nothing anywhere reports the gap.**

**Be able to give one more example from the course** — `perf_event_paranoid = 4`, `unprivileged_bpf_disabled = 2`, restricted user namespaces, a module that builds and will not load — **and to say what the general form of the failure is.**

**2 · Every abstraction has a price, and the price is a number.**

> And the standard failure is **not** an error message. **It is a plausible number from a broken
> harness.** A control that must return zero costs nothing and catches it.

**Be able to describe two of this term's broken harnesses and the check that caught each.** They are listed in **L39 §4**.

---

## What is not on the paper

**xv6 line numbers · system call numbers · BPF opcodes · `struct` member names · anything needing a calculator.**

**If it is in the code and not in the reasoning, it is not on the paper.**

---

*CS 202 · Week 12 · Revision Guide · © CSE Department*
