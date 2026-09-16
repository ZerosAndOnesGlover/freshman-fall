# CS 202 · Reading Guide · Week 10
## Virtualization: OSTEP's VMM Appendix, the KVM API, and Two Papers

---

**The curriculum names no reading for Week 10.** The KVM API document is the week's real text — **read the first three sections before Wednesday**, because PS 10 is written against it.

| Source | Now? | Why |
|---|---|---|
| **OSTEP, Appendix B: "Virtual Machine Monitors"** | **Read** | Trap-and-emulate, the machine/guest/host distinction, why x86 was hard. **L31** |
| **Kernel documentation, `virt/kvm/api.rst`**, §§1–4 | **Read the ioctl list** | `KVM_CREATE_VM`, `KVM_SET_USER_MEMORY_REGION`, `KVM_CREATE_VCPU`, `KVM_RUN`, and the `kvm_run` structure. **L31 §2, PS 10** |
| Intel SDM Vol. 3C, Ch. 23–24 | *Skim the exit-reason list* | What the hardware traps, and what it records. **L31 §4** |
| Adams & Agesen (2006), "A Comparison of Software and Hardware Techniques for x86 Virtualization" | *Read §§1–3* | Why binary translation beat the first hardware support — and the measurements that showed it |
| Barham et al. (2003), "Xen and the Art of Virtualization" | *Optional* | Paravirtualization: changing the guest instead of emulating harder. **L32 §5** |
| Russell (2008), "virtio: Towards a De-Facto Standard for Virtual I/O Devices" | *Read the introduction* | The queue-in-shared-memory design. **L32 §5** |
| `man 7 namespaces`, `man 7 cgroups` | **Before L33** | The other kind of isolation, and the one this machine restricts |

**If you have two hours:** OSTEP Appendix B, then the KVM API's `KVM_RUN` section, then start PS 10 Q1 — the first working guest is about forty lines.

---

## OSTEP Appendix B

1. OSTEP's VMM runs the guest kernel **in user mode** and traps its privileged instructions. **Which of Week 0's mechanisms is it re-using**, and what does it have to keep per guest that the kernel keeps per process?
2. The appendix describes the VMM handling a guest's system call: the guest's trap goes to the VMM first, which passes it to the guest kernel. **Count the boundary crossings** for one guest system call, and compare with the one crossing on real hardware.
3. **Why did x86 need hardware support** when other architectures did not? Name the property a "virtualizable" instruction set must have. *(Popek and Goldberg, 1974.)*

---

## The KVM API

4. `KVM_SET_USER_MEMORY_REGION` takes a **userspace address**. **What does that let the hypervisor do** that a design taking physical addresses could not? Name three things from Weeks 5 and 6 that then apply to a guest's memory automatically.
5. `KVM_RUN` fills in a shared `struct kvm_run`. **Why a shared page rather than returning the data from the `ioctl`?** *(What is the cost of a system call, from Week 9 §L28?)*
6. Find `KVM_EXIT_IO` and `KVM_EXIT_MMIO` in the structure. **What does each tell the hypervisor**, and which fields would a disk emulator need?
7. The API says `KVM_RUN` may return `-EINTR`. **When**, and what must the hypervisor do? *(L31 §4 — our first version got this wrong.)*

---

## The papers

8. Adams & Agesen found **binary translation beating hardware VT-x** on some workloads in 2006. **What was slow about the first hardware support**, and which of this week's measurements is its descendant? *(L32 §4.)*
9. Xen's guests are **modified** to call the hypervisor instead of executing privileged instructions. **What does that buy, and what does it cost** — and which of the two does virtio choose?
10. Virtio puts a queue in shared memory. **Which Week 9 structure does that resemble**, and what is the equivalent of the doorbell there?

---

## Where to Go Deeper

| Source | Topic | When |
|---|---|---|
| Agache et al. (2020), "Firecracker: Lightweight Virtualization for Serverless Applications", *NSDI* | Why VM start-up and teardown times matter, and what they cut to get them down | After L31 §3 |
| Kernel documentation, `admin-guide/mm/ksm.rst` | Sharing identical pages between guests | For L33 §4 |
| `man 8 systemd-nspawn`, `man 1 unshare` | Containers from the command line — and what this machine refuses | **Before Lab 10** |

---

*CS 202 · Week 10 · Reading Guide · © CSE Department*
