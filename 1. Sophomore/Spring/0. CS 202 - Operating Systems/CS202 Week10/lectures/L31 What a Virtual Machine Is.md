# CS 202 · Operating Systems
## Week 10 · Lecture 1 of 3
### What a Virtual Machine Is

*“A man provided with paper, pencil, and rubber, and subject to strict discipline, is in effect a universal machine.”* — Alan Turing, "Intelligent Machinery" (1948)

---

**Sat:** Monday of Week 10, 09:00–09:50, VNC 101, **after Quiz 10** · **Reading:** OSTEP Ch. B (VMM); the KVM API documentation · **Next:** L32, memory and devices

**Coursework:** 📊 **Quiz 10** today · 🔬 **Lab 9** Tue this week 15:00–16:50 · 📝 **PS 10** released Wed this week, due Fri of Week 11 17:00 · 📝 **PS 9** due Fri this week 17:00

---

## 1. The Same Trick, One Level Up

**Week 0 built a wall**: user code runs at a lower privilege, and anything it may not do traps into the kernel. **A virtual machine is that wall applied to a kernel.**

A guest operating system believes it owns the machine. It sets page tables, programs the interrupt controller, talks to disks. **Every one of those is an instruction the hypervisor cannot allow to take effect on the real hardware** — so the hardware is arranged to **trap** them, and the hypervisor emulates what the guest expected to happen.

**That is "trap and emulate", and it is Week 0's design with the roles shifted:**

| | Week 0 | This week |
|---|---|---|
| The protected thing | the kernel | the **hypervisor** |
| The confined thing | a process | **a whole operating system** |
| The boundary | ring 3 → ring 0, by `syscall` and traps | **VMX non-root → VMX root, by *VM exits*** |
| What the confined thing believes | it has the machine's memory | **it has the machine** |

**x86 could not do this properly until 2005.** Some instructions behaved differently in user mode instead of trapping — `popf` silently ignored changes to the interrupt flag — so early VMware rewrote guest code on the fly. **Intel VT-x added a second dimension**: root and non-root operation, each with its own four rings. **A guest kernel runs in ring 0 of non-root mode**, believing it has full privilege, and the instructions that matter cause a **VM exit** into root mode.

```
$ grep -o 'vmx\|ept\|vpid\|unrestricted_guest' /proc/cpuinfo | sort -u
ept
unrestricted_guest
vmx
vpid
```

---

## 2. KVM: The Hypervisor Is a Device

**On Linux, the part that must be in the kernel is a driver** — `kvm` and `kvm_intel`, loaded on this machine — and it exposes the hardware through **`/dev/kvm`** (Week 9's interface, again). **Everything else is an ordinary program.**

The whole API is file descriptors and `ioctl`:

| You have | You call | You get |
|---|---|---|
| `/dev/kvm` | `KVM_CREATE_VM` | **a VM file descriptor** |
| a VM | `KVM_SET_USER_MEMORY_REGION` | the guest's physical memory, which is a `mmap` in your process |
| a VM | `KVM_CREATE_VCPU` | **a vCPU file descriptor** |
| a vCPU | `mmap` | a shared `struct kvm_run` page — **12,288 bytes here** |
| a vCPU | `KVM_SET_SREGS`, `KVM_SET_REGS` | the registers the guest starts with |
| a vCPU | **`KVM_RUN`** | **the guest runs until it exits**; `kvm_run` says why |

```
$ ./kvmprobe
KVM_GET_API_VERSION      12
KVM_GET_VCPU_MMAP_SIZE   12288 bytes
KVM_CAP_NR_VCPUS         8
KVM_CAP_MAX_VCPUS        4096
KVM_CAP_NR_MEMSLOTS      32764
```

**A virtual machine is a file descriptor, its memory is your memory, and running it is a system call that returns when the guest does something you have to deal with.**

---

## 3. A Hypervisor in One Page

`kvmhost.c` is about 120 lines. It maps 64 KiB of memory, writes fifteen bytes of 16-bit code into it, and runs:

```asm
  mov si, 0x2000        ; a string in guest memory
  mov dx, 0x3f8         ; the serial port
next:
  lodsb
  cmp al, 0
  je  done
  out dx, al            ; ← this leaves the guest
  jmp next
done:
  hlt                   ; ← and so does this
```

```
$ ./kvmhost hello
Hello from the guest
guest halted after 21 I/O exits, 0 MMIO exits, 0 other, in 0.0004 s
```

**Twenty-one exits, one per character**, each returning from `KVM_RUN` with `exit_reason == KVM_EXIT_IO` and the byte in the shared page. **The "device" the guest wrote to does not exist**: the hypervisor read the byte and called `putchar`. **That is all device emulation is.**

**What a VM costs to make**, measured by creating and destroying 500 of them:

```
500 VMs: create 152 us each, destroy 10839 us each
```

**Creation is fast; destruction is not.** Tearing a VM down waits for an RCU grace period inside the kernel — about **11 ms** — which is why a machine that starts and stops thousands of short-lived VMs cares about teardown, and why "microVM" projects measure exactly this.

---

## 4. What Makes the Guest Leave

**A VM exit is a trap whose handler is the hypervisor.** The causes divide into three kinds, and the difference is measured in L32 §4:

| Cause | Example | Who handles it |
|---|---|---|
| **The hardware must not let it through** | `cpuid`, writes to control registers, `hlt` | **KVM, inside the kernel** — the guest resumes without your program running |
| **It needs a device that does not exist** | `out` to a port, a load from unmapped memory | **your program**, after `KVM_RUN` returns |
| **The host needs the CPU back** | a timer interrupt, a signal | the host scheduler; `KVM_RUN` returns `EINTR` and you re-enter |

**That last row is a real detail, not a footnote**: `KVM_RUN` can return `-EINTR` at any time, and a hypervisor that treats it as an error stops working the first time a signal arrives. *(Ours did, once.)*

---

## 5. The Guest Runs on the Real CPU

**This is what separates virtualization from emulation.** Between exits, **the guest's instructions execute directly on the processor** at full speed: no interpretation, no translation, no per-instruction cost.

**QEMU can do both**, and xv6 booting shows the difference — or rather, shows how little difference it makes for this guest:

```
TCG (software emulation): 1.20 s, 1.28 s, 1.29 s
KVM (hardware):           1.12 s, 1.17 s, 0.92 s
```

**Barely faster**, because xv6's boot is not computation: it is reading sectors from an emulated IDE disk and printing to an emulated serial port — **thousands of exits**, each costing what L32 §4 measures. **Hardware virtualization makes the guest's own instructions free; it does nothing for the guest's I/O.**

---

## 6. What to Take Away

1. **A virtual machine is Week 0's wall around a whole kernel**: the guest runs in **VMX non-root** mode, and privileged operations cause **VM exits** instead of taking effect.
2. **x86 needed hardware help (2005)** because some privileged instructions failed silently in user mode instead of trapping.
3. **On Linux the hypervisor is a driver plus an ordinary program**: `/dev/kvm`, `ioctl`, and a shared page. **A VM is a file descriptor; its memory is your `mmap`.**
4. **`KVM_RUN` returns when the guest does something you must handle** — and can return `EINTR` for reasons that have nothing to do with the guest.
5. **Making a VM costs ~150–500 µs; destroying one costs ~11 ms**, nearly all of it teardown inside the kernel.
6. **Between exits the guest runs on the real CPU** — which is why a compute-bound guest is nearly native, and why xv6's device-bound boot is not.

---

## Exercises

1. `kvmhost` prints the guest's output with `putchar`. **Which lines of the guest's code know that**, and what would the guest have to change if the hypervisor decided the port were a disk instead?
2. **Why must `KVM_SET_USER_MEMORY_REGION` take a userspace address** rather than a physical one? What does that make possible for the hypervisor?
3. Creating a VM costs 150–500 µs and destroying it 11 ms. **Design a measurement** that shows where the destruction time goes, given that you may not use root.
4. xv6 under KVM was **at best 25% faster** than under emulation. **Name two guests for which the difference would be enormous**, and say what they have in common.
5. `KVM_CAP_NR_VCPUS` is 8 and `KVM_CAP_MAX_VCPUS` is 4096 on this machine. **What is the difference between those two numbers**, and which one limits a guest you start today?

---

*CS 202 · Week 10 · L31 · © CSE Department*
