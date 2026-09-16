# CS 202 · Problem Set 10
## A Hypervisor of Your Own

---

**Released:** Week 10, Wednesday · **Due:** Week 11, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS10_{LastName}_{StudentID}.pdf`, plus your `kvmhost.c` in a tarball `PS10_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine and encouraged. The write-up and the code must be
> yours. State at the top: *"I worked on this problem set independently"* or name who you discussed
> which question with.
>
> **`kvmhost.c` must compile clean under `gcc -O2 -Wall -Wextra`.**

**You are writing a hypervisor.** Not a toy model of one — **a real one**, which asks the kernel for a virtual machine, gives it memory and a processor, starts it, and services what it asks for. It is about 120 lines, and most of them are given to you.

**Files provided** in `assignments/ps10/`:

| File | Yours to write | Provided |
|---|---|---|
| `kvmhost.c` | the memory region (Q1a), the vCPU's registers (Q1b), the exit loop (Q1c) | opening `/dev/kvm`, creating the VM and vCPU, mapping `kvm_run`, and **the guests**, hand-assembled |

> **`/dev/kvm` is readable and writable by your account on BH 210** — check with `ls -l /dev/kvm`.
> Nothing in this problem set needs root.

---

### Q1: A Guest That Says Hello (35 points)

**(a) [10]** Give the VM its memory. The provided `mmap` is the guest's RAM; hand it to the VM with **`KVM_SET_USER_MEMORY_REGION`**, at guest physical address 0.

**(b) [10]** Set the vCPU's state: **16-bit real mode** — read the segment registers, set `cs.base` and `cs.selector` to 0, write them back — and the general registers, with `rip` at the code, `rflags` = 0x2, `rcx` = the count, `rsp` = 0x8000.

**(c) [15]** Write the run loop: call **`KVM_RUN`**, then act on `run->exit_reason`:

- **`KVM_EXIT_IO`** — the guest wrote to a port. The byte is at `(char *)run + run->io.data_offset`.
- **`KVM_EXIT_MMIO`** — the guest touched memory you did not map. Report `phys_addr`, `len`, `is_write` and `data[0]`.
- **`KVM_EXIT_HLT`** — the guest halted. Stop.
- **An `ioctl` failure with `errno == EINTR`** is not an error. **Say in your report what it means and what you do.**

Then:

```
$ ./kvmhost hello
Hello from the guest
guest halted after 21 I/O exits, 0 MMIO exits, 0 other, in 0.0004 s
```

---

### Q2: What You Just Built (15 points)

**(a) [5]** The guest wrote to port `0x3f8` and your program printed a character. **Nothing in the machine is a serial port. Explain what the guest believes, what actually happened, and where the byte travelled** — naming the structure it arrived in.

**(b) [5]** The guest's memory is a `mmap` in your process. **Name three things from Weeks 5 and 6 that are therefore true of a guest's "physical" memory**, and say which of them the guest could detect.

**(c) [5]** Your hypervisor never sets a page table for the guest, yet the guest reads its string from address `0x2000`. **Which translation is happening, and which hardware feature performs it?** *(L32 §2.)*

---

### Q3: What an Exit Costs (25 points)

**(a) [10]** Run both measurement modes, at least three times each, pinned to one CPU:

```bash
taskset -c 2 ./kvmhost exits 100000      # each write to the port leaves the guest entirely
taskset -c 2 ./kvmhost cpuid 65535       # each cpuid leaves the guest, but KVM answers it
```

**Report both, with the spread over your runs.**

**(b) [8]** **Explain the ratio.** What does the port-I/O exit do that the `cpuid` exit does not? **Count the boundary crossings** for each, and compare with Week 9's measured cost of an ordinary system call.

**(c) [7]** The `cpuid` guest **must save `cx` around the instruction.** Find out why — run `cpuid` with `eax = 0` on paper — and say what happens to the loop without it. *(This is not hypothetical: the reference hung.)*

---

### Q4: A Device of Your Own (15 points)

**(a) [8]** Run `./kvmhost mmio`. The guest writes one byte to guest physical `0x80000`, which has **no memory behind it**:

```
MMIO exit: write of 1 byte(s) at guest physical 0x80000, data 0x2a
```

**Report it, and explain why the address had to be outside the memory region** — what would have happened if the region had covered it? *(The reference made exactly this mistake first.)*

**(b) [7]** **Design, in writing, a virtual device** at `0x80000`: a one-byte status register and a one-byte data register. Say **what your hypervisor does on a read of each and on a write of each**, and **what the guest's driver would look like**. You need not implement it.

---

### Q5: Emulation Against Virtualization (10 points)

Boot xv6 from Lab 0 under QEMU twice — once as usual, once with `-enable-kvm` — and time each to the `init: starting sh` line.

**(a) [5]** **Report both, three runs each.** *(The reference machine measured 1.20–1.29 s and 0.92–1.17 s.)*

**(b) [5]** **The difference is small. Explain why**, in terms of what xv6 does during boot and what each of the two techniques makes faster. **What would have to change about xv6 for KVM to help a lot?** *(L32 §5.)*

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | A guest that says hello | 35 |
| 2 | What you just built | 15 |
| 3 | What an exit costs | 25 |
| 4 | A device of your own | 15 |
| 5 | Emulation against virtualization | 10 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem set of the term is dropped.**

---

*CS 202 · Week 10 · PS 10 · © CSE Department*
