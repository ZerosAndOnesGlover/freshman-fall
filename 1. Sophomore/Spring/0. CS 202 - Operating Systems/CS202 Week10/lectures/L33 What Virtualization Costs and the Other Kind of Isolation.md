# CS 202 · Operating Systems
## Week 10 · Lecture 3 of 3
### What Virtualization Costs — and the Other Kind of Isolation

---

**Sat:** Friday of Week 10, 09:00–09:50, VNC 101 · **Reading:** `man 7 namespaces`, `man 7 cgroups`; the virtio paper · **Next:** Week 11, distributed systems

---

## 1. The Cost Model Is One Line

**Between exits, a guest runs at native speed.** So:

> **the cost of virtualization = (exits per second) × (cost per exit)**

and both terms are things a hypervisor's designer controls. Measured on the reference machine (L32 §4):

| Exit | Per exit |
|---|---:|
| handled by KVM **in the kernel** (`cpuid`) | **1.4 µs** |
| handled by the **hypervisor process** (port I/O) | **7.8 µs** |

**A guest that computes exits almost never and runs at full speed. A guest that talks to devices exits constantly and pays 8 µs each time.** Everything else in this lecture follows.

---

## 2. Measured: The Guest That Does Not Compute

```
xv6 boot, TCG (software emulation): 1.20 s, 1.28 s, 1.29 s
xv6 boot, KVM (hardware):           1.12 s, 1.17 s, 0.92 s
```

**Hardware virtualization bought between nothing and 25%.** xv6's boot reads sectors from an emulated IDE controller a register at a time and prints through an emulated serial port — **thousands of userspace exits**, and those cost the same whether the guest's own instructions are emulated or native.

**The lesson generalises.** A database in a VM pays for its I/O; a compiler in a VM pays for almost nothing. **Ask what fraction of a workload's time is spent in device registers before asking how fast the hypervisor is.**

---

## 3. Making Exits Rarer

**Four techniques, in increasing order of how much they change:**

| Technique | What it does | Cost |
|---|---|---|
| **In-kernel emulation** (`KVM_CAP_IRQCHIP`) | the interrupt controller and timer are emulated inside KVM | the exit still happens — **1.4 µs instead of 7.8** |
| **Coalesced MMIO** (`KVM_CAP_COALESCED_MMIO` = 2 here) | repeated writes to a chosen range accumulate in a ring, delivered at the next real exit | only safe for write-only registers with no side effects |
| **Virtio** (L32 §5) | replace the device with a queue in shared memory: **one doorbell per batch** | the guest needs a driver that knows it is virtualized |
| **Device passthrough** (VT-d/IOMMU) | give the guest the real device; the IOMMU keeps its DMA inside its own memory | the device belongs to one guest, and migration becomes hard |

**Each step removes exits rather than making them cheaper** — which is the only move that scales.

---

## 4. Memory, Across Several Guests

**A guest's "physical" memory is host virtual memory** (L32 §1), so Weeks 5 and 6 apply to it — and produce two problems of their own:

- **Double paging.** The host may swap out a page the guest thinks is resident; the guest, under its own memory pressure, may then choose that page to evict — **reading it from host swap in order to write it to guest swap.**
- **The guest never gives memory back.** A guest that has touched its memory keeps it; the host cannot tell what is free inside. **Ballooning** fixes this with a driver in the guest that allocates pages and tells the host they are free.
- **Identical pages across guests** — ten VMs running the same distribution — can be merged. **KSM is enabled on this machine** (`/sys/kernel/mm/ksm/run` is 1): the kernel scans for identical pages and merges them copy-on-write. **It also turns memory contents into a timing side channel**, which is why it is off by default in multi-tenant settings.

**And a guest can itself be a hypervisor**: `/sys/module/kvm_intel/parameters/nested` is **`Y`** here. **Each level multiplies the exits** that reach the bottom.

---

## 5. The Other Kind of Isolation

**A virtual machine isolates by giving each guest its own kernel. A container isolates by giving each group of processes its own *view* of one kernel.**

The mechanisms are two Linux features this course has already met:

- **Namespaces** — a process's view of a kind of global name. This shell is in eight:

```
$ ls -l /proc/self/ns/
mnt  net  pid  time  user  uts  ipc  cgroup
```

  **A container is a process whose `pid`, `mnt`, `net` and `user` namespaces differ from yours** — it sees its own process table, its own root filesystem, its own network interfaces, and its own idea of who is root.

- **Cgroups** — Week 6's memory limits, and the same for CPU and process count. On this machine the user is delegated `cpu memory pids`, which is exactly what Lab 6's scopes used.

**There is no guest kernel, so there are no VM exits at all**: a system call in a container is Week 9's 659 ns, not 8 µs. **The price is that every container shares one kernel** — a kernel bug is everyone's bug, which is Week 12's subject.

**And on these machines you cannot build one from scratch:**

```
$ unshare --user --map-root-user id
unshare: write failed /proc/self/uid_map: Operation not permitted
```

**Unprivileged user namespaces are restricted by AppArmor here** (`kernel.apparmor_restrict_unprivileged_userns` is 1), because they have been a rich source of privilege-escalation bugs — a container mechanism whose own attack surface was too large. **The cgroup half works; the namespace half does not.**

---

## 6. Choosing

| | Virtual machine | Container |
|---|---|---|
| Isolation boundary | **the hardware's**, enforced by VT-x and EPT | **the kernel's system-call interface** |
| Guest kernel | its own | **shared with the host** |
| A system call costs | ~0.7 µs (native) — but device I/O costs exits | **~0.7 µs, and nothing else** |
| Start-up | ~150 µs to create, **~11 ms to destroy** (L31 §3), plus booting a kernel | a `fork` and an `exec` |
| Memory | a whole kernel per guest; ballooning and KSM to share | one kernel, shared page cache |
| Runs a different OS | **yes** | no — the kernel is the host's |
| A kernel bug | contained to one guest, usually | **affects every container** |

**Which is why production systems use both**: containers inside virtual machines, with the VM boundary between tenants and the container boundary between services of one tenant.

---

## 7. What to Take Away

1. **Cost = exits × cost per exit.** Measured: **1.4 µs** in the kernel, **7.8 µs** out to the hypervisor.
2. **xv6 booted barely faster under KVM than under emulation**, because its time is in emulated device registers, not in its own instructions.
3. **Every optimisation removes exits** rather than making them cheaper: in-kernel devices, coalescing, virtio, passthrough.
4. **A guest's memory is the host's virtual memory**, which brings double paging, ballooning and KSM — and KSM brings a side channel.
5. **Containers isolate views of one kernel** with namespaces and cgroups: **no exits at all**, and no second kernel — but a shared one.
6. **This machine allows the cgroup half and refuses the namespace half**, because unprivileged user namespaces were themselves a security problem.

---

## Exercises

1. A workload spends 5% of its instructions on I/O, each I/O costing ten port writes. **Estimate its slowdown in a VM with emulated devices, and with virtio.**
2. **Why does coalesced MMIO need the hypervisor's permission per range**, rather than being applied to all MMIO?
3. Double paging: **construct the sequence** in which a guest page is read from host swap only to be written to guest swap, and say which layer should have known better.
4. KSM merges identical pages across guests. **Describe the measurement an attacker in one guest makes** to learn what is running in another.
5. A team wants to run ten services from the same company on one machine, and also to run one customer's untrusted code. **Which boundary goes where, and why?**

---

*CS 202 · Week 10 · L33 · © CSE Department*
