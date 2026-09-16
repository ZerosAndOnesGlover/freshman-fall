# CS 202 · Operating Systems
## Week 12 · Lecture 3 of 3
### What This Course Was About

---

**Sat:** Friday of Week 12, 09:00–09:50, VNC 101 · **Reading:** none — re-read your own measurements · **Next:** the final, Wednesday of finals week, 09:00–11:30, VNC 100

---

## §1 · One Mechanism, Six Times

**Thirteen weeks looked like six subjects.** They were one, applied to six resources. Every time this course protected or shared something, it built the same three pieces:

> **An interposition point** the hardware cannot be talked out of · **a table** that says what the
> abstraction maps to · **a cache** of that table, because consulting it every time is too slow.

| Week | Resource | Interposition point | Table | Cache |
|---|---|---|---|---|
| **0–1** | the CPU's privilege | `syscall` → an MSR only ring 0 can write | the system call table | — |
| **1–3** | the CPU's time | the timer interrupt | the run queue | the per-CPU run queue |
| **5–6** | memory | the MMU, on **every** load and store | the page table | **the TLB** |
| **7–8** | storage | `read`/`write` and the block layer | the inode and its block pointers | **the page cache** |
| **9** | devices | the interrupt and the ring buffer | the driver's `file_operations` | the ring itself |
| **10** | the whole machine | the **VM exit** | the EPT, and the VMCS | the EPT's own TLB |
| **11** | agreement | the election timeout | the term, and who voted | the leader |
| **12** | authority | the reference monitor | the mode bits, the filter, the capability set | — |

**Read the rows and the same four sentences keep appearing:**

**The interposition point must be unavoidable, which means it must be hardware.** A check a program can skip is not a check. The MMU checks the U/S bit on every access because it is silicon; `syscall` cannot be redirected because the MSR is privileged; the VM exit fires because the CPU is in guest mode. **Week 12's whole difficulty is that the one mechanism which is *not* hardware — the eighteen setuid binaries — is where the bugs are.**

**The table is always too slow to consult.** So there is a cache, and the cache introduces the same three problems every time: **what is in it** (the working set, Week 6), **when it lies** (staleness — a stale TLB entry after a page-table write, a stale page-cache page after a write, a stale leader after a partition), and **who invalidates it** (`invlpg` and the TLB shootdown IPI, `fsync`, the term number).

**Every one of them was measured, and the cache was worth between 5× and 58×.** A TLB hit against a miss: **17.3 ns** saved per access at 2 GiB. A warm page-cache read against a cold one: **1.61 µs against 93.9 µs, 58×**.

**And every one of them fails the same way**: the cache is correct until something changes it behind your back, and the mechanism that tells you is the expensive part. **That is the whole course in one sentence.**

---

## §2 · The Price List

**Habit 2 said: when a design is justified by performance, find the measurement.** Here is every price this course paid, on the reference machine, from this term's own programs. **Learn the orders of magnitude, not the digits.**

| What | Cost | Where |
|---|---|---|
| A function call | **1.8 ns** | L34 |
| An uncontended lock (futex fast path) | **14.8 ns**, 0 system calls | L11 |
| A contended atomic, 8 threads | **29–32 ns** | L10 |
| **A seccomp filter, per system call** | **≈ +50 ns** | **L38 §4** |
| A TLB miss, 2 GiB working set | **17.3 ns** | L17 §3 |
| An `ioctl` to a character device | **595 ns** | L28 |
| A write to `/dev/null` | **659 ns** | L28 |
| **A system call** | **≈ 840 ns** | L03, L34 |
| A page fault, first touch | **1,833–1,949 ns** | L18 |
| A context switch, same CPU | **1,622 ns** | L05 §5 |
| A context switch, across CPUs | **2,139 ns** | L05 §5 |
| A copy-on-write fault | **2,957 ns** | L18 |
| **A VM exit** | **7,806 ns** | L33 |
| A pipe round trip | **8.5–10.5 µs** | L34 |
| A loopback round trip (UDP / TCP) | **19–22 µs** | L34 |
| `pthread_create` + `join` | **27.6 µs** | L04 |
| A cold random 4 KiB read, NVMe | **93.9 µs** | L23 |
| `fork` + `exit` + `wait` | **154 µs** | L04 |
| A timer wake-up, idle CPU | **144 µs** *(4 µs busy, with slack at 1 ns)* | L09 |
| Deepest C-state exit (C10) | **890 µs** | L09 |
| `fsync` of 64 MiB | **41 ms** *(the write itself: 15 ms)* | L23 |
| **A round trip to another machine** | **22.6–24.5 ms** | L34 |

**The ratios are what you actually use:**

- **A system call is 470 function calls.** That is why `read()` of one byte at a time took **14.2 s** for 16 MiB and 64 KiB reads took **0.0022 s** — **6,400×**, all of it system call overhead. **Batch.**
- **A page fault is two system calls.** Lazy allocation is therefore free if the pages are never touched and a 2× tax if they all are — which is Project 2 Part A, and why `sbrk` of 4 MB costing zero pages is the whole point.
- **A VM exit is nine system calls, or nearly five context switches.** That is why virtio exists, why Week 10's guest ran 100,000 exits to make the number visible, and why a hypervisor's job description is "arrange not to exit".
- **A network round trip is 13,000,000 function calls.** No amount of local optimisation matters next to one avoidable round trip. **This is why distributed algorithms are counted in round trips and nothing else.**
- **And a seccomp filter is 6% of a system call** — which is what a security mechanism costs when it is designed well, and the reason there is no excuse for not using it.

---

## §3 · Habit 1, Revisited: The Protection That Is Switched On

**Week 0's L02 made a claim that sounded like a trick: this machine's kernel is built with `CONFIG_X86_UMIP=y`, the CPU does not implement UMIP, and therefore an ordinary program can read a kernel address with one instruction.**

**Twelve weeks later, under every protection in L37 and L38 — PTI, IBRS, ASLR, `kptr_restrict`, AppArmor, Yama, a disabled `perf`, a disabled unprivileged BPF — here is that instruction again:**

```bash
grep -c CONFIG_X86_UMIP=y /boot/config-7.0.0-31-generic     # 1
./sgdt
sgdt from user mode succeeded: GDT base 0xfffffe397b808000 limit 127
```

**It still works.** And the address it printed is a **live kernel address**, from the same machine where:

```bash
grep -m1 ' T ' /proc/kallsyms
0000000000000000 srso_alias_untrain_ret       # kptr_restrict = 1: every symbol zeroed
```

**The kernel carefully zeroes every address in `/proc/kallsyms` to deny an attacker the kernel's layout, and then a single unprivileged instruction hands one over.** Neither mechanism is broken. `kptr_restrict` does exactly what it says; `CONFIG_X86_UMIP` does exactly what it says **on a CPU that has UMIP**, which this one does not. **The gap is between the configuration and the silicon, and nothing anywhere reports it.**

**That was Habit 1, and it recurred in every week of this course:**

| Week | Configured, documented or assumed | What the machine actually did |
|---|---|---|
| 0 | `CONFIG_X86_UMIP=y` | **the CPU has no UMIP; `sgdt` leaks a kernel address** |
| 1 | xv6 saves FPU state | **it does not save it at all** |
| 6 | `perf` for page-fault tracing | **`perf_event_paranoid = 4`: unusable for this account** |
| 7 | `bpftrace` for the page cache | **`unprivileged_bpf_disabled = 2`: refused** |
| 9 | a module that builds is a module that loads | **built clean, refused to load — unsigned, and the account cannot** |
| 10 | containers, to contrast with VMs | **`apparmor_restrict_unprivileged_userns = 1`: `unshare` refused** |
| 11 | etcd, to watch Raft | **not installed, and not installable by a student account** |
| 12 | every CPU flaw is mitigated | **`gather_data_sampling: Vulnerable`** — alone in a directory of `Mitigation:` lines |

**Eight weeks, eight gaps, and every one of them was found by trying the thing rather than reading the setting.** That is the habit. It is not cynicism about documentation — the documentation was accurate every time. **It is that "enabled" and "effective" are different words**, and only one of them is measurable.

---

## §4 · Habit 2, Revisited: The Measurements This Course Got Wrong

**The price list in §2 is trustworthy because a great many earlier versions of it were not.** These are this term's own failures, and they are on the final's syllabus in the sense that **the reasoning they teach is examinable**:

| The number we got | Why it was wrong | How it was caught |
|---|---|---|
| A TLB cost of **zero** | `-O2` deleted the loop; then the checksum was always 0 because the fill wrote `(char)i` at page granularity | the result was *too clean* |
| A page-fault test that faulted **nothing** | `*p = *p` is a no-op the compiler removes | fault count did not move |
| A guard-page write that **succeeded** | the address was one page low — it wrote into the text segment | the "failure" did not fail |
| Page-fault counts **polluted** | libc's first call, printing, and COW of the stack after `fork` all fault | per-step measurement and pre-touching |
| An aging policy **worse than FIFO** (80,799 against 27,747) | the policy as specified was genuinely worse at long ticks | shipped both, and made it PS 6 Q5 |
| A crash sweep reporting **zero crash points** | `|| true` swallowed the exit status; and the range swept was never reached; and the checker was too weak to see orphaned inodes | three separate fixes |
| `symlink()` returning **56790** | a duplicate system call number, then a **stale `usys.o`** the Makefile never rebuilt | `objdump -d usys.o` |
| A hypervisor reporting **34,464 of 100,000** exits | 16-bit `cx` truncation in the guest | the host counted instead |
| A page-cache read **not 58× faster** | the "cold" pass was never actually cold | reading the file first |
| A seccomp filter that made system calls **faster** | CPU frequency ramp, not the filter | **a control that measured the baseline twice** |
| A canary demo where **both builds** printed the same message | it was `_FORTIFY_SOURCE` firing in both; the canary never ran | reading the *exact* message |
| A timing attack that "worked" | it recovered **one byte of eight**, and only after interleaving and discarding the retraining batch | counting the bytes |

**One pattern runs through all of them, and it is the single most useful thing in this course:**

> **The standard failure is not an error message. It is a plausible number from a broken harness.**

**A wrong number that looks wrong costs you ten minutes.** A wrong number that looks *right* goes into a report, a design document, and a decision. **The defences are cheap and they are all on that table**: check the thing you measured is the thing you named; run a control that must return zero; look at the generated code when the compiler is involved; be suspicious of results that are too clean; and **check what was actually built.**

---

## §5 · What the Final Asks

**Wednesday of finals week, 09:00–11:30. Two and a half hours, 100 marks, 15%, comprehensive. Two handwritten pages, both sides.** Seat allocations on the portal — VNC 100 with overflow to TH 200.

**It is comprehensive in the way this course has been comprehensive**: not thirteen disconnected topics, but the table in §1 asked from several directions. **Roughly:**

- **Mechanism.** Given a mechanism from any week, say where the interposition point is, what the table holds, what caches it and what invalidates the cache.
- **Arithmetic.** Banker's algorithm, page-replacement traces, block-address arithmetic in an inode, quorum sizes. **All of it by hand; all of it seen before.**
- **Numbers.** The orders of magnitude in §2, and the ratios between them — and what a design decision should be when the ratio is 6,400×.
- **Judgment.** A described system, a claimed property, and the question *what would you measure to find out if it is true?*
- **The two habits.** A configuration that says one thing and a machine that does another; or a measurement that produced a plausible number and an explanation of what is wrong with the harness.

**What is not on it:** anything requiring a calculator, xv6 line numbers, system call numbers, BPF opcodes, or the spelling of a `struct` member. **If it is in the code and not in the reasoning, it is not on the paper.**

**The revision guide in `resources/` lists, per week, the one idea and the one number.** It is short on purpose.

---

## §6 · What Comes Next

**You have written parts of a kernel and measured the rest.** Three honest directions:

**Read a real one.** xv6 is 6,000 lines and you have read most of it. Linux's `kernel/sched/fair.c` is 13,000 lines on its own and repays a week — you now know what a run queue is for, which is the hard part. **`Documentation/` in the Linux tree is written by the people who wrote the code.**

**Read the papers this course compressed.** *The UNIX Time-Sharing System* (Ritchie & Thompson, 1974) is eleven pages and contains most of Weeks 7–9. *End-to-End Arguments in System Design* is the best twelve pages in the field. Raft's paper is readable in an evening; so is *A Case for Redundant Arrays of Inexpensive Disks*. **Saltzer & Schroeder** is 1975 and is still what Week 12 was about.

**And keep the habit.** The mechanisms in this course will be replaced — io_uring is already eating the system call table, persistent memory breaks the storage hierarchy, and confidential computing moves the hypervisor out of the TCB. **What will not be replaced is that every abstraction has a price, that the price is a number, and that the number is measurable on the machine in front of you.**

**That was the course.**

---

### What You Should Be Able to Do

1. **Give the interposition point, table and cache** for any mechanism in the course, and name what invalidates the cache.
2. **Quote the price list to an order of magnitude**, and use the ratios to justify a design decision.
3. **Explain the UMIP result**, and generalise it: why "configured" and "effective" are different claims.
4. **Describe three of this term's broken harnesses** and the check that would have caught each.
5. **Say what you would measure** to test a claimed property of a system you have not seen.

---

*CS 202 · Week 12 · L39 · © CSE Department*
