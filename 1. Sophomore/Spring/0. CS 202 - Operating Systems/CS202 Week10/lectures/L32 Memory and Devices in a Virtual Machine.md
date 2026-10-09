# CS 202 · Operating Systems
## Week 10 · Lecture 2 of 3
### Memory and Devices in a Virtual Machine

*“Write a paper promising salvation, make it a 'structured' something or a 'virtual' something, or 'abstract', 'distributed' or 'higher-order' or 'applicative' and you can almost be certain of having started a new cult.”* — Edsger W. Dijkstra, "My hopes of computing science" (EWD709, 1979)

---

**Sat:** Wednesday of Week 10, 09:00–09:50, VNC 101 · **Reading:** the KVM API documentation, `KVM_SET_USER_MEMORY_REGION` and `KVM_EXIT_MMIO`; OSTEP Ch. B · **Next:** L33, what it costs

**Coursework:** 📝 **PS 10** released today, due Fri of Week 11 17:00 · 📝 **PS 9** due Fri this week 17:00 · 📊 **Quiz 11** Mon of Week 11 · 🔬 **Lab 10** Tue of Week 11 15:00–16:50

---

## 1. The Guest's Physical Memory Is Your Virtual Memory

**A guest believes it has physical memory starting at address 0.** The hypervisor gives it one:

```c
void *mem = mmap(0, GUEST_MEM, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
struct kvm_userspace_memory_region region = {
    .slot = 0, .guest_phys_addr = 0, .memory_size = GUEST_MEM,
    .userspace_addr = (unsigned long)mem,
};
ioctl(vmfd, KVM_SET_USER_MEMORY_REGION, &region);
```

**Guest physical address 0 is a byte in an ordinary `mmap` of an ordinary process.** Everything Week 5 and Week 6 said about that mapping still applies: **it is demand-allocated, it can be swapped, it can be shared.** A hypervisor that maps the same file into two guests has given them shared memory; a host that reclaims those pages has swapped a guest's "RAM" to disk.

**The guest has no idea.** Its own page tables map *guest virtual* to *guest physical* — and guest physical is what this mapping translates.

---

## 2. Two Page Tables, One Access

**So every guest memory access needs two translations:**

```
 guest virtual ──(the guest's page tables, which the guest controls)──▶ guest physical
 guest physical ──(the EPT, which the hypervisor controls)────────────▶ host physical
```

**Extended Page Tables (EPT) is the second one, in hardware.** This CPU has it:

```
$ grep -o 'ept\|vpid' /proc/cpuinfo | sort -u
ept
vpid
```

**The cost is in the walk.** A TLB miss in a guest walks **four levels of guest page table**, and *each* of those levels is itself a guest physical address that must go through **four levels of EPT** — up to **24 memory accesses** for one miss, against Week 5's four. **The TLB matters even more inside a VM**, and huge pages (L17 §4) matter at both levels.

**Before EPT (2008), hypervisors kept *shadow page tables***: the hypervisor maintained its own guest-virtual-to-host-physical tables and trapped every guest page-table write to keep them current. **Correct, and enormously expensive** — a guest's `fork` became thousands of exits. **`vpid` tags TLB entries with the VM**, so a VM exit no longer has to flush the TLB — the same idea as Week 5's PCIDs, one level up.

---

## 3. A Device Is Memory That Is Not There

**The guest's driver writes to a device register.** There are two ways it reaches the hypervisor:

**Port I/O** — `out dx, al` — always exits:

```
$ ./kvmhost hello
Hello from the guest
guest halted after 21 I/O exits, …
```

**Memory-mapped I/O** — an ordinary load or store to an address with **no memory slot behind it**. The EPT has no entry, the access faults, and KVM tells the hypervisor exactly what the guest tried:

```
$ ./kvmhost mmio
MMIO exit: write of 1 byte(s) at guest physical 0x80000, data 0x2a
```

**That is the whole mechanism of device emulation**: leave a hole in the guest's physical memory, and every access to it becomes a message to your program — address, size, direction, data. **A virtual disk, a virtual network card and a virtual graphics adapter are all this, with more registers.**

**And a memory slot can be added or removed while the guest runs**, which is how a hypervisor hot-plugs memory, or moves a device's window.

---

## 4. What an Exit Costs

**Not all exits are equal**, and the difference decides how a hypervisor is designed. Measured on the reference machine, with the guest doing nothing but the operation being counted:

| Exit | Handled by | Per exit |
|---|---|---:|
| **`cpuid`** | **KVM, in the kernel** — the hypervisor process never runs | **1,409 – 1,464 ns** |
| **port I/O (`out`)** | **the hypervisor process**, after `KVM_RUN` returns | **7,778 – 7,880 ns** |

**A round trip to userspace costs five and a half times an exit the kernel can answer**, and both are enormous beside the 8 ns of an ordinary memory access (L17 §3). **Everything in hypervisor design follows from that ratio:**

- **Handle what you can in the kernel.** KVM emulates the interrupt controller (`KVM_CAP_IRQCHIP`), the timer, and the instructions that only need register state — so those exits never reach userspace.
- **Batch what you cannot.** `KVM_CAP_COALESCED_MMIO` — value 2 here — lets the guest's repeated writes to a chosen MMIO range accumulate in a ring buffer, delivered on the *next* real exit. **One exit instead of a hundred.**
- **Avoid the exit entirely**, which is §5.

---

## 5. Virtio: Stop Pretending to Be Hardware

**Emulating a real device is absurd in a virtual machine.** The guest's driver writes a sector address one register at a time because that is how an IDE controller works — and each write costs 8 µs of exit.

**Virtio changes the contract**: the guest is told plainly that it is virtualized, and given a **queue in shared memory** instead of a device's registers. The guest writes descriptors into a ring the hypervisor can read directly, and **rings a doorbell — one exit — for a batch of requests.** *(Week 9's block layer already had the queue; virtio simply puts one end of it in the guest.)*

| | Emulated IDE | Virtio |
|---|---|---|
| To submit one request | ~10 port writes = **~80 µs of exits** | descriptors in shared memory + one doorbell = **~8 µs** |
| To submit a hundred | a hundred times that | **still one doorbell**, if they are queued |
| The guest needs | its ordinary driver | **a driver that knows it is a guest** |

**This is why xv6 under KVM was barely faster than under emulation** (L31 §5): xv6's IDE driver does exactly what the first column says, and no amount of hardware virtualization removes those exits. **The fix is not faster virtualization; it is a different device.**

---

## 6. What to Take Away

1. **Guest physical memory is a `mmap` in the hypervisor process** — demand-allocated, swappable, shareable, and invisible to the guest.
2. **EPT translates guest physical to host physical in hardware**, so the guest controls its own page tables; a TLB miss can cost **up to 24 memory accesses**.
3. **Shadow page tables were the software answer** before EPT, and **`vpid` is Week 5's PCID for VMs.**
4. **A device is a hole in guest physical memory**: MMIO exits tell the hypervisor the address, size, direction and data.
5. **Measured: an in-kernel exit costs ~1.4 µs; one that reaches the hypervisor process costs ~7.8 µs** — 5.5× — and that ratio explains in-kernel emulation and coalesced MMIO.
6. **Virtio removes exits instead of making them faster**, by giving the guest a queue in shared memory and one doorbell per batch.

---

## Exercises

1. A guest reads a 4 KiB sector from an emulated IDE disk with ten port writes and one interrupt. **Estimate the cost in exits**, and compare with the 90 µs the real SSD takes (L19 §3).
2. **Why can a hypervisor swap a guest's memory to disk without the guest knowing**, and what does the guest's own swapping then cost? *(Two levels of paging, both trying to evict.)*
3. `KVM_CAP_COALESCED_MMIO` is 2 on this machine. **Describe a device for which coalescing is safe**, and one for which it is not.
4. With EPT, a guest TLB miss can touch 24 lines of page table. **How many does a 2 MiB huge page in the guest save**, and how many if the *host* also uses huge pages for the guest's memory?
5. Virtio needs a driver that knows it is virtualized. **What does that cost an operating system that must also run on real hardware**, and how does Linux handle it?

---

*CS 202 · Week 10 · L32 · © CSE Department*
