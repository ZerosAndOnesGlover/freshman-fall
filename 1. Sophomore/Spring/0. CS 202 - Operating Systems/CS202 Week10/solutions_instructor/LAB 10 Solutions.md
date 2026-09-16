# CS 202 · Lab 10 — Solutions and TA Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Session:** Tuesday of Week 11, 15:00–16:50, BH 210. **Unmarked** — checked off in the session.

**Project 1 is due that Friday.** Reserve the last half hour for questions about it; most students will want to talk about the lottery scheduler rather than the hypervisor.

**What the session is actually for.** Students have just written a hypervisor in PS 10 (or are about to). **This lab is where they see what it costs and what it cannot do** — and Part E is the one that changes minds: hardware virtualization barely helps a guest that spends its time in emulated devices.

---

## Timing

| Minutes | Part | TA action |
|---|---|---|
| 0–15 | A | Quick. If `./kvmprobe` fails, check `ls -l /dev/kvm` and group membership |
| 15–35 | B | Editing hand-assembled bytes frightens people; show the byte table on the board |
| 35–60 | **C** | The two exit costs are the week's central number |
| 60–80 | D | Q9's "make the region bigger" is worth doing, not just answering |
| 80–100 | E | Two boot timings and the `unshare` refusal |
| 100–110 | Project 1 questions | |

---

## Answers

Reference machine: i5-8250U, kernel 7.0.0-31, `kvm` and `kvm_intel` loaded, EPT + VPID + unrestricted guest, nested = Y.

### Q1 — the API surface

```
KVM_GET_API_VERSION      12
KVM_GET_VCPU_MMAP_SIZE   12288 bytes
KVM_CAP_NR_VCPUS         8
KVM_CAP_MAX_VCPUS        4096
KVM_CAP_NR_MEMSLOTS      32764
```

**`NR_VCPUS` is the recommended maximum — the host's CPU count (8 here); `MAX_VCPUS` is the hard limit KVM will accept (4096).** Creating more vCPUs than physical CPUs works and simply time-shares them. **[Full marks require that distinction.]**

### Q2 — what a VM is

**A file descriptor.** Therefore: it is **owned by the process** and closed automatically when it exits (no leaked VMs); it can be **passed to another process** over a Unix socket; it obeys the ordinary permission checks on `/dev/kvm`; and `KVM_CREATE_VCPU` on it produces further descriptors. **Accept any two.**

### Q3 — KVM as a character driver

**`/dev/kvm` is a character device with a major and minor number** (Week 9 L28 §1). KVM fills in a **`struct file_operations`**, and the entry that matters is **`.unlocked_ioctl`** — everything in this week's API is an `ioctl`. *(`.mmap` matters too: it is how `kvm_run` becomes shared memory.)*

### Q4 — one exit per character

**The guest's loop does one `out` per byte, and every `out` to an unhandled port is a VM exit that reaches the hypervisor.** 21 characters (20 letters plus the newline) = 21 exits. **A real serial port would behave the same way** — which is why a 16550's FIFO exists.

### Q5 — a guest of your own

**Marking:** any correct message, with the exit count equal to its length. **Printing twice** has two sound answers, and the choice is the lesson:

- **Change the guest**: reset `si` to `0x2000` and jump back once — *more guest code, still one exit per character, 2 × n exits.*
- **Change the host**: after `KVM_EXIT_HLT`, reset `rip` and `rsi` with `KVM_SET_REGS` and re-enter — *no guest change; the hypervisor restarted the guest.*

**The second is what a virtual machine monitor actually is**: the guest's state is data the hypervisor owns and may rewrite. **Give full marks for either with a clear reason; note the second to students who chose the first.**

### Q6 — the cost of leaving

```
100000 port-I/O exits in 0.7880 s = 7880 ns per exit      (7806, 7778 on repeats)
65535 cpuid instructions in 0.0959 s = 1464 ns each       (1422, 1409)
```

**Ratio ≈ 5.5×.** The port-I/O exit **returns from `KVM_RUN` into the hypervisor process**, which reads the shared page, does its work, and re-enters — two extra boundary crossings and a system call each way. **`cpuid` is answered inside KVM**; the hypervisor process never runs.

### Q7 — creating and destroying

```
500 VMs: create 152 us each, destroy 10839 us each
```

**Destruction is ~70× creation.** Tearing down a VM frees its memory slots, its EPT structures and its vCPUs, and **waits for an RCU grace period** so that no CPU can still be walking those structures — milliseconds, by construction. **Accept "it waits for other CPUs to be known to have finished with it".**

### Q8 — the arithmetic

Create 0.15 ms + 1,000 × 7.9 µs = 7.9 ms + destroy 10.8 ms ≈ **18.9 ms**, of which **destruction is 57%** and I/O 42%. **Change first: the teardown** — reuse the VM instead of destroying it (what a pool of pre-created microVMs does), **or** cut the exits with virtio. **Accept either with the arithmetic.**

### Q9 — why the address must be unbacked

```
MMIO exit: write of 1 byte(s) at guest physical 0x80000, data 0x2a
```

**With `GUEST_MEM` = 1 MiB, `0x80000` is inside the region**: the write goes to the hypervisor's `mmap` as plain memory, **no exit occurs**, and the program reports `0 MMIO exits`. **Students should try it** — the reference shipped that bug first, and the corrected version is the lab.

### Q10 — a device that counts

Expected shape:

```c
} else if (run->exit_reason == KVM_EXIT_MMIO) {
    static unsigned long writes;
    if (run->mmio.is_write && run->mmio.phys_addr == 0x80000)
        printf("device: byte 0x%02x (write %lu)\n", run->mmio.data[0], ++writes);
}
```

**How a virtual disk differs:** it has **many registers** (sector, count, command, status) and **completes asynchronously** — the hypervisor must also deliver an **interrupt** to the guest when the transfer is done (`KVM_IRQ_LINE` or the in-kernel irqchip), which this device never does. **[Full marks need the interrupt.]**

### Q11 — the two boot times

```
TCG: 1.20 s, 1.28 s, 1.29 s        KVM: 1.12 s, 1.17 s, 0.92 s
```

**KVM removes the cost of interpreting the guest's instructions; it does not remove exits.** xv6's boot is dominated by **emulated IDE reads and serial writes**, each a userspace exit at ~8 µs. **The guest's own instruction count during boot is small**, so there is little for hardware virtualization to make faster.

### Q12 — the other isolation

```
$ unshare --user --map-root-user id
unshare: write failed /proc/self/uid_map: Operation not permitted
$ cat /proc/sys/kernel/apparmor_restrict_unprivileged_userns
1
$ systemd-run --user --scope -p MemoryMax=128M …
134217728
```

**Cgroups work; unprivileged user namespaces do not** — AppArmor restricts them on Ubuntu 24.04 because they have been a repeated source of privilege escalation.

**A container is a process with its own namespaces (pid, mnt, net, user, uts, ipc) and its own cgroup limits** — nothing more. **What it does not have that the `kvmhost` guest does: its own kernel.** Its system calls go straight to the host kernel at ~659 ns with **no exits at all**.

**Which isolates better:** the VM, **against a kernel bug** — a container escape is one kernel vulnerability away, while a VM escape needs a hypervisor or hardware vulnerability. **The container isolates better against waste**: no second kernel, no double paging, no 11 ms teardown. **Accept any answer that names the shared kernel as the container's weak point.**

---

## Common Problems

| Symptom | Cause | Fix |
|---|---|---|
| `open("/dev/kvm")` fails with `EACCES` | not in the `kvm` group / ACL missing | `ls -l /dev/kvm`, `id`; on BH 210 the ACL grants it |
| `KVM_RUN` fails with `EINVAL` immediately | `rflags` is 0, or `sregs` were zeroed rather than read first | set `rflags = 0x2`; always `KVM_GET_SREGS` first |
| The guest runs away, 100% CPU, no output | guest code at the wrong address, or `rip` not set | check `CODE_ADDR` against the `memcpy` |
| `cpuid` mode never finishes | `cpuid` clobbers `ecx`, which is the loop counter | `push cx` / `pop cx`, and set `rsp` |
| `exits` mode reports 34,464 for 100,000 | 16-bit `cx` in real mode — the count wrapped | count the exits in the **host**, not the guest |
| `-enable-kvm` fails under QEMU | another hypervisor holds the CPU, or nested VMX is off in a VM | `lsmod | grep kvm`; on bare metal it works |

---

*CS 202 · Week 10 · Lab 10 Solutions · Instructor Only*
