# CS 202 · Operating Systems
## Week 10: Virtualization

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 201, PROG 201
**Assessment for this course (overall):** Problem Sets 30%, Projects 30%, Midterms 25%, Final 15%
**This week's deliverables:** PS 9 due **Friday**, PS 10 released **Wednesday**, **Quiz 10** at the start of **Monday's** lecture (covers Week 9).
**Lab 9 is sat on the Tuesday of this week; Lab 10 covers this week and is sat on the Tuesday of Week 11.**

> ### **Project 1 is due Friday of next week**, and **Project 2 is due in the completion period.**
> Project 1's Part B — the lottery scheduler — is where the time goes; if it is not running by the
> end of this week, come to the Week 11 lab with the kernel that does not boot.

---

### Why This Week Exists

Because the wall Week 0 built around a process can be built around an entire operating system — and once it is, a machine becomes a file descriptor.

**A hypervisor is Week 0's design with the roles shifted up one level.** The guest kernel runs in its own privileged mode, believing it owns the hardware; the instructions that would actually touch the hardware **trap** to the hypervisor, which emulates what the guest expected. **On Linux the part that must be privileged is a device driver — `/dev/kvm` — and everything else is an ordinary program**: 120 lines create a virtual machine, give it memory, start a processor, and service what it asks for.

**And then you measure it.** An exit KVM answers inside the kernel costs **1.4 µs**; one that reaches your program costs **7.8 µs**. Making a VM costs **150 µs**; destroying one costs **11 ms**. And xv6 boots **barely faster** with hardware virtualization than with pure emulation — because its time goes into emulated device registers, which hardware virtualization does not make cheaper.

---

### Learning Objectives

By the end of Week 10, you should be able to:

1. Explain **trap and emulate**, and why x86 needed hardware support to do it.
2. Describe **VMX root and non-root operation**, and what causes a **VM exit**.
3. Use the **KVM API**: create a VM, give it memory, create a vCPU, run it, and handle its exits.
4. Explain why **guest physical memory is host virtual memory**, and what follows from that.
5. Explain **EPT**, the two levels of translation, and what a guest TLB miss can cost.
6. Explain **device emulation** through port I/O and **MMIO exits**.
7. **Measure the cost of a VM exit**, and distinguish in-kernel from userspace handling.
8. Explain the techniques that **remove exits**: in-kernel devices, coalescing, **virtio**, passthrough.
9. Explain **ballooning, KSM and double paging**, and why one of them is a side channel.
10. Explain **containers** as namespaces plus cgroups, and what they do and do not isolate.
11. Say which boundary — VM or container — belongs where, and why production uses both.
12. Read `/dev/kvm`'s capabilities and say what limits a guest on this machine.

---

### This Week's Materials

| File | Purpose |
|---|---|
| [[L31 What a Virtual Machine Is]] | Trap and emulate; VMX root and non-root; **the KVM API as file descriptors**; a guest that prints through a port in 21 exits; **VM creation 150 µs, destruction 11 ms**; why the guest runs at native speed between exits |
| [[L32 Memory and Devices in a Virtual Machine]] | **Guest physical memory as a `mmap`**; EPT and the 24-access TLB miss; shadow tables and VPID; **an MMIO exit as a device**; **1.4 µs against 7.8 µs**; coalesced MMIO; **virtio, which removes exits rather than shortening them** |
| [[L33 What Virtualization Costs and the Other Kind of Isolation]] | **Cost = exits × cost per exit**; **xv6 booting barely faster under KVM**; ballooning, KSM and double paging; **containers as namespaces plus cgroups**, with the namespace half refused on this machine |
| [[CS202 Week10/assignments/QUIZ 10 Week 10 Monday\|QUIZ 10 Week 10 Monday]] | Ten minutes, covers **Week 9**, answer key printed |
| [[PS 10 A Hypervisor of Your Own]] | Write the hypervisor: memory, registers, the exit loop — then measure exits and design a device. Due **Friday of Week 11** |
| `assignments/ps10/kvmhost.c` | The skeleton: three `TODO`s, with the guests hand-assembled for you |
| [[LAB 10 Boot a Machine You Wrote]] | The API surface; your own guest; the two exit costs; an MMIO device; **TCG against KVM**; and the container mechanisms this machine allows and refuses. **Tuesday of Week 11** |
| `lab/kvmprobe.c`, `lab/vmsplit.c` | What KVM offers; what a VM costs to create and destroy |
| [[CS202 Week10/resources/Reading Guide Week 10\|Reading Guide Week 10]] | OSTEP Appendix B, the KVM API, Adams & Agesen, Xen, virtio |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Virtualization is free until the guest wants something.**

Between exits the guest runs on the real processor at full speed. **Every cost in this week's measurements is a boundary crossing** — 1.4 µs if the kernel can answer, 7.8 µs if your program must, 11 ms to tear the machine down. So every serious optimisation **removes crossings**: emulate the interrupt controller in the kernel, coalesce writes, replace the device with a queue in shared memory, or hand the guest the hardware.

**And the alternative gives up the boundary entirely.** A container has no guest kernel and no exits at all — it shares the host's kernel, which is cheaper in every measurement and worse in exactly one way.

---

### Assessment Reminder

**PS 9 is due Friday at 17:00. PS 10 is released Wednesday.**

**Project 1 is due Friday of Week 11. Project 2 is due Friday of the completion period.**

**Labs and quizzes carry no weight** and are still required. **Quiz 10 is at the start of Monday's lecture and covers Week 9.**

> **Two labs touch this week.** **Lab 9** — devices from both sides — is sat on the **Tuesday of this
> week**. **Lab 10** covers this week and is sat on the **Tuesday of Week 11**.

Both are tracked in [[_CS 202 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 0's trap** is a VM exit one level up. **Week 5's page tables** gain a second level in EPT, and **Week 5's PCIDs** reappear as VPID. **Week 9's device interface** is what `/dev/kvm` is, and what the guest thinks it is talking to. **Week 6's cgroups** are half of what a container is.

**Sideways:** **CS 212** runs its build farm in containers; the trade in L33 §6 is the one that decided it.

**Forward:** **Week 11's replicated services** run on virtual machines that can be stopped, migrated and restarted — and a partition is indistinguishable from a hypervisor pausing a guest. **Week 12** returns to the shared kernel as an attack surface.

---

*CS 202 · Week 10 · © CSE Department*
