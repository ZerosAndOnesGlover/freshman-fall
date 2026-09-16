# CS 202 · Problem Set 10 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for PS 10.** Q1 is binary — the guest prints or it does not — and is worth a third of the marks for that reason. **The other two thirds are for explaining a machine the student has just built**, which is where a copied solution fails.

**Reference:** `kvmhost reference (do not distribute).c`, complete. Both it and the student skeleton compile with no compiler output. All figures from the reference machine (i5-8250U, kernel 7.0.0-31, `kvm_intel` with EPT, unrestricted guest and nested support).

---

## Q1: A Guest That Says Hello (35 points)

### (a) [10]

```c
struct kvm_userspace_memory_region region = {
    .slot = 0, .guest_phys_addr = 0, .memory_size = GUEST_MEM,
    .userspace_addr = (unsigned long)mem,
};
if (ioctl(vmfd, KVM_SET_USER_MEMORY_REGION, &region) < 0) { perror(...); return 1; }
```

**Common failures:** a `memory_size` that is not a multiple of the page size (`EINVAL`); forgetting `MAP_SHARED` on the `mmap` (works, but the guest's writes are then invisible to a second mapping — worth a note, not a deduction).

### (b) [10]

```c
struct kvm_sregs sregs;
ioctl(vcpufd, KVM_GET_SREGS, &sregs);
sregs.cs.base = 0;
sregs.cs.selector = 0;
ioctl(vcpufd, KVM_SET_SREGS, &sregs);

struct kvm_regs regs = { .rip = CODE_ADDR, .rflags = 0x2, .rax = 'A', .rcx = count, .rsp = 0x8000 };
ioctl(vcpufd, KVM_SET_REGS, &regs);
```

**`rflags` must have bit 1 set** — a zero `rflags` is not a legal x86 state and `KVM_RUN` fails with `EINVAL`. **Deduct 3** for a submission that discovers this and hard-codes something else without saying why.

**Reading `sregs` before modifying it** matters: the rest of the segment state (`ds`, `es`, `ss`, the descriptor cache) comes from KVM's reset state, and a zeroed `kvm_sregs` will not run.

### (c) [15]

The loop, with the three exit reasons and the `EINTR` retry:

```c
    if (ioctl(vcpufd, KVM_RUN, 0) < 0) {
        if (errno == EINTR) continue;
        perror("KVM_RUN"); return 1;
    }
```

**`EINTR` [5 of the 15]:** `KVM_RUN` returns it when a signal arrives while the guest is running — a timer, a `SIGWINCH`, anything. **It says nothing about the guest**, and the hypervisor must simply re-enter. **A submission that treats it as fatal works until it does not**, which is exactly what happened to the reference.

**Expected output:**

```
Hello from the guest
guest halted after 21 I/O exits, 0 MMIO exits, 0 other, in 0.0004 s
```

---

## Q2: What You Just Built (15 points)

### (a) [5]

**The guest believes** it wrote a byte to a 16550 UART at port `0x3f8`. **What happened:** the `out` instruction caused a **VM exit** with `exit_reason == KVM_EXIT_IO`; KVM filled in `run->io` (direction, size, port, count) and put the byte in the shared `kvm_run` page at `run->io.data_offset`; `KVM_RUN` returned; **the hypervisor read the byte out of that page and called `putchar`.** **The byte travelled: guest register → VMCS/exit handling → the shared page → the host's stdout.**

### (b) [5]

Any three of: **it is demand-allocated** (a guest page costs nothing until touched — L18); **it can be swapped by the host** (L19), unknown to the guest; **it can be shared or deduplicated** (KSM — L33 §4); **it is subject to the host's cgroup limits** (L21); **`fork` of the hypervisor would make it copy-on-write.**

**Which the guest could detect: the timing** — a page the host has swapped costs the guest a 90 µs stall it cannot account for. **This is the "double paging" problem**, and it is the reason hypervisors prefer ballooning to host swapping.

### (c) [5]

**The guest has no page tables at all — it is in real mode**, so guest virtual = guest physical. **The translation that happens is guest physical → host physical**, performed by **EPT** (`ept` in `/proc/cpuinfo`), from the memory region installed in (a). **Accept "the second-level page tables KVM built from my memory slot".**

---

## Q3: What an Exit Costs (25 points)

### (a) [10]

```
100000 port-I/O exits in 0.7880 s = 7880 ns per exit
100000 port-I/O exits in 0.7806 s = 7806 ns per exit
100000 port-I/O exits in 0.7778 s = 7778 ns per exit
65535 cpuid instructions in 0.0959 s = 1464 ns each, in one KVM_RUN
65535 cpuid instructions in 0.0932 s = 1422 ns each
65535 cpuid instructions in 0.0923 s = 1409 ns each
```

**[5 per mode, with a spread.]** Students' absolute numbers will vary with CPU and mitigations; **the ratio should be 4–7×.**

### (b) [8]

**Ratio ≈ 5.5×.**

| | `cpuid` | port I/O |
|---|---|---|
| guest → VMX root | ✔ | ✔ |
| KVM handles it | ✔ | ✘ — KVM cannot know what a port means |
| **return to the hypervisor process** | ✘ | **✔ — `KVM_RUN` returns** |
| hypervisor runs, then re-enters | ✘ | **✔** |

**Boundary crossings: two for `cpuid`** (in and out of non-root), **four for port I/O** (plus the `ioctl` return and re-entry, which is a system call each way). **Against Week 9's ~659 ns system call**, a userspace exit is about twelve system calls' worth.

### (c) [7]

**`cpuid` with `eax = 0` returns the vendor string in `ebx`, `edx` and `ecx`** — `ecx` receives `"ntel"`. **In 16-bit real mode `loop` counts with `cx`**, so the counter is overwritten with part of the vendor string on every iteration and the loop does not terminate. **The fix is `push cx` / `pop cx` around it** (and a valid `rsp`). **[4 for the clobber, 3 for the consequence.]** *(The reference hung exactly here; a student who reports the same hang and diagnoses it earns full marks.)*

---

## Q4: A Device of Your Own (15 points)

### (a) [8]

```
MMIO exit: write of 1 byte(s) at guest physical 0x80000, data 0x2a
guest halted after 0 I/O exits, 1 MMIO exits, 0 other, in 0.0002 s
```

**With a 1 MiB region [4]:** `0x80000` is **inside** it, so the write lands in the hypervisor's `mmap` as ordinary memory, **no exit happens at all**, and the guest sees nothing unusual. *(The reference's first version made this mistake and reported "0 MMIO exits" — the fix was to shrink the region to 64 KiB.)* **MMIO works precisely because the address is not backed.**

### (b) [7]

A reasonable design, marked on coherence:

| Access | Hypervisor does |
|---|---|
| read of `0x80000` (status) | return 1 if the host has a byte queued, else 0 |
| read of `0x80001` (data) | return the next queued byte, and pop it |
| write of `0x80001` (data) | append the byte to the host's output |
| write of `0x80000` (status) | ignore, or use as a reset |

**The guest's driver** polls the status register, then reads or writes data — **exactly Week 9's canonical device** (L29 §1), which is the point: the student has just built the thing the driver talks to. **Full marks for naming what `run->mmio.data` must be filled in with on a read, and that `is_write` distinguishes the cases.**

---

## Q5: Emulation Against Virtualization (10 points)

### (a) [5]

```
TCG: 1.20 s, 1.28 s, 1.29 s        KVM: 1.12 s, 1.17 s, 0.92 s
```

### (b) [5]

**xv6's boot is not computation.** It reads the kernel and the file system from an **emulated IDE controller**, a register at a time, and prints to an **emulated serial port** — **thousands of userspace exits at ~8 µs each** (Q3), and those cost the same under KVM as under TCG. **What KVM makes free is the guest's own instruction stream**, of which xv6 executes relatively little during boot.

**What would change it [2 of the 5]:** a guest that computes (a compiler, a database query) — or **a guest using virtio**, where a batch of block requests costs one doorbell instead of ten port writes each (L32 §5). **Accept either.**

---

*CS 202 · Week 10 · PS 10 Solutions · Instructor Only*
