# CS 202 · Quiz 11
## Administered: Monday, Week 11 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 10** — virtualization: the KVM API, memory and devices, exits, and containers.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **Project 1 is due this Friday at 17:00.** PS 10 is due Friday too; **Lab 10 is tomorrow.**
>
> **This is the last quiz of the term.**

---

**Q1.** A guest executes `out dx, al`. **Describe what happens**, from the instruction to the byte appearing on the hypervisor's screen.

&nbsp;

&nbsp;

---

**Q2.** Guest physical address 0 is a byte in the hypervisor's `mmap`. **Name two consequences** from Weeks 5 and 6, and one the guest could detect.

&nbsp;

&nbsp;

---

**Q3.** Measured: an exit KVM handles itself costs **1.4 µs**; one that reaches the hypervisor process costs **7.8 µs**. **Explain the difference**, and name one technique that exploits it.

&nbsp;

&nbsp;

---

**Q4.** A guest writes to guest physical `0x80000`. **Under what condition is that an MMIO exit**, and what does the hypervisor receive?

&nbsp;

&nbsp;

---

**Q5.** xv6 booted in about 1.25 s under software emulation and about 1.05 s under KVM. **Why so little difference**, and what kind of guest would show a large one?

&nbsp;

&nbsp;

---

**Q6.** Creating a VM costs about **150 µs**; destroying one costs about **11 ms**. **What is the kernel doing for those 11 ms**, and which workload cares?

&nbsp;

&nbsp;

---

**Q7.** **What is a container, in terms of two Linux mechanisms?** Name what it does *not* have that a virtual machine does, and the one way that makes it worse.

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** The instruction causes a **VM exit**: the CPU leaves VMX non-root mode, KVM sees an I/O exit it cannot serve, **`KVM_RUN` returns** to the hypervisor process, which finds `exit_reason == KVM_EXIT_IO` and the byte at `(char *)run + run->io.data_offset` in the **shared `kvm_run` page**, and prints it. **Nothing in the machine is a serial port.**

---

**Q2.** Any two: it is **demand-allocated** (untouched guest pages cost nothing); **the host can swap it**; it can be **shared or deduplicated** (KSM); it obeys the host's **cgroup limits**. **The guest can detect host swapping by timing** — a stall it cannot account for, which is the double-paging problem.

---

**Q3.** The cheap exit is **handled inside KVM**, so the hypervisor process never runs: two boundary crossings. The dear one **returns from `KVM_RUN`** and re-enters: two more crossings plus a system call each way. **Techniques: in-kernel device emulation (`KVM_CAP_IRQCHIP`), coalesced MMIO, or virtio**, which removes exits altogether.

---

**Q4.** **Only if no memory slot covers that address.** With memory mapped there, the write is an ordinary store and there is no exit. If unbacked, the hypervisor receives `phys_addr`, `len`, `is_write` and the **data** — everything a device needs.

---

**Q5.** **KVM makes the guest's own instructions native; it does not remove exits.** xv6's boot is emulated IDE and serial registers — thousands of userspace exits at ~8 µs each, which cost the same either way. **A compute-bound guest** — a compiler, a database query — would show a large difference.

---

**Q6.** **Tearing down the VM's memory slots, EPT structures and vCPUs, and waiting for an RCU grace period** so no CPU can still be walking them. **Workloads that start and stop many short-lived VMs care** — serverless platforms, per-request sandboxes — which is why they pool pre-created VMs.

---

**Q7.** **Namespaces** (its own view of pids, mounts, network, users) **plus cgroups** (its share of memory, CPU and processes). **It does not have its own kernel**: its system calls go straight to the host's at ~0.7 µs with no exits. **That is why it is worse in one way — a kernel bug is everyone's bug.**

---

### What to Do With Your Score

There is no score. Instead, before Friday:

| If you missed | Reread |
|---|---|
| Q1, Q4 | L31 §3, L32 §3 |
| Q2 | L32 §1 |
| **Q3, Q5** | **L32 §4 and L33 §2 — PS 10 Q3 is this** |
| Q6 | L31 §3 |
| Q7 | L33 §5 |

---

*CS 202 · Week 11 · Quiz 11 · covers Week 10 · ungraded · the last quiz of the term*
