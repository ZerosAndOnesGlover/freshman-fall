# CS 202 · Operating Systems
## Week 5 · Lecture 3 of 3
### Demand Paging, Copy-on-Write, and Physical Memory

*“... we do not consider it as good engineering practice to consume a resource lavishly just because it happens to be cheap.”* — Niklaus Wirth, *Project Oberon* (2013), §2.3

---

**Sat:** Friday of Week 5, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 23, Linux half; Love Ch. 12 and 15 · **Next:** Week 6, page replacement and swapping

**Coursework:** 📝 **PS 4** due today 17:00 · 📊 **Quiz 6** Mon of Week 6 · 🔬 **Lab 5** Tue of Week 6 15:00–16:50 · 📝 **PS 6** released Wed of Week 6, due Fri of Week 7 17:00

---

## 1. A Gigabyte for Free

L16 §7 mapped a gigabyte and the process's memory did not grow. `faultcost.c` then wrote one byte to each of its 262,144 pages, twice, pinned to one CPU. **Three runs:**

| | Run 1 | Run 2 | Run 3 |
|---|---:|---:|---:|
| `mmap` of 1 GiB: resident memory grows by | 132 kB | 132 kB | 132 kB |
| **first pass**: page faults | 262,147 | 262,147 | 262,147 |
| **first pass: per page** | **1,833 ns** | **1,949 ns** | **1,935 ns** |
| **second pass: per page** | **14.7 ns** | **13.3 ns** | **15.2 ns** |

**`mmap` allocated nothing.** It recorded a region — a **virtual memory area** — and returned. **The first write to each page trapped**, and the kernel allocated a frame, **zeroed it**, installed the entry, and returned to the instruction that faulted, which then ran again and succeeded. **The second pass found every page present and paid 14 ns** — a TLB miss or two and a cache miss.

**Each first touch cost about 130 times as much as each later one.** That is **demand paging**: the kernel does no work for memory until a program proves it will use it. Programs routinely allocate more than they use — stacks, heaps rounded up, arrays sized for the worst case — and **the unused part costs nothing but address space.** (Week 6 asks what happens when programs *do* use it all.)

---

## 2. The Page Fault

**When the MMU cannot translate an access — entry not present, or not writable, or not user — it raises exception 14.** The CPU puts **the faulting address in `CR2`** and pushes an **error code** whose low bits say what happened:

| Bit | Set means |
|---|---|
| 0 | the page **was present** — a protection violation, not a missing page |
| 1 | the access was a **write** |
| 2 | it came from **user mode** |

**What happens next is entirely up to the kernel.** Linux looks the address up among the process's VMAs:

- **In a VMA, and the access is allowed** by the VMA's permissions: a *legitimate* fault. Allocate and zero a frame (anonymous memory), read the page from the page cache (a file), or copy it (copy-on-write, §4). **Return and retry.**
- **In no VMA, or the VMA forbids the access**: deliver **`SIGSEGV`**.

**xv6 has no VMAs and no legitimate faults.** Every user page exists before it is used, so a fault can only be a bug, and `trap` handles exception 14 in its `default:` case. `pgfault.c` is three pages — code and data at `0x0`, the guard page at `0x1000`, the stack at `0x2000` — and writes one byte past its memory, into its guard page, into the kernel, and over its own code:

```
$ pgfault past
size 0x3000; writing to 0x3000
pid 3 pgfault: trap 14 err 6 on cpu 0 eip 0x5d addr 0x3000--kill proc
$ pgfault guard
size 0x3000; writing to 0x1FFF
pid 4 pgfault: trap 14 err 7 on cpu 0 eip 0x5d addr 0x1fff--kill proc
$ pgfault kernel
size 0x3000; writing to 0x80100000
pid 5 pgfault: trap 14 err 7 on cpu 0 eip 0x5d addr 0x80100000--kill proc
$ pgfault text
size 0x3000; writing to 0x0
wrote it
```

**The error codes decode exactly.** Past the end: **6** — a user write to a page **not present**. The guard page and the kernel: **7** — a user write to a page that **is present but forbids it**, because `exec` clears `PTE_U` on the guard page (`clearpteu`) and the kernel's pages never had it. **Same exception, same result, different reasons — and `CR2` names the byte.**

**And the fourth write succeeded.** `allocuvm` maps every page of a program `PTE_W | PTE_U`, code included, so **an xv6 program can overwrite its own instructions**, and so can a buffer overflow in it. Linux maps code read-only and executable, and the same write is a `SIGSEGV`.

*(Our first version of `pgfault` wrote `*p = *p`, and every case "succeeded": the compiler had removed a statement that could not change anything. The fault happens only if the write does.)*

---

## 3. The Zero Page

**Reading memory that was never written must return zeros.** Allocating and zeroing a frame for every such read would be wasteful, so Linux maps **one shared, read-only frame of zeros** instead. `pmlab.c` watches four pages of a fresh mapping through `/proc/self/pagemap` (Lab 5), showing each page as **P** present, **x** mapped by this process only, **d** soft-dirty:

```
       mapped, nothing touched             -.d  -.d  -.d  -.d   faults 0
       read page 0                         P.d  -.d  -.d  -.d   faults 1
       wrote page 0                        Pxd  -.d  -.d  -.d   faults 1
       wrote page 1 (never read)           Pxd  Pxd  -.d  -.d   faults 1
```

**The read faulted and made page 0 present but *not* exclusive** — it is the shared zero page, mapped read-only into this and every other process that has read an untouched page. **The write faulted again**, now a protection fault, and the kernel gave the page a frame of its own. **A page never read costs one fault on its first write; a page read first costs two.**

---

## 4. Copy-on-Write

**`fork` copies the parent's address space** (Week 1). Linux does not copy the memory: it **copies the page tables, marks every writable private page read-only in both**, and shares the frames. **The first write by either process faults, and only then is that one page copied.** `pmlab.c` again, parent then child:

```
parent wrote all four                      Pxd  Pxd  Pxd  Pxd   faults 4
child  after fork                          P.d  P.d  P.d  P.d   faults 0
child  read page 0                         P.d  P.d  P.d  P.d   faults 0
child  wrote page 1                        P.d  Pxd  P.d  P.d   faults 1
```

**After the fork, every page is present in the child and no page is exclusive** — each frame is mapped by two processes. **The child's read is free**; its write faults and gives page 1 a frame of its own. **The parent's page 1 still holds its old value.**

**What copy-on-write saves is measured by `forkcost.c`**: `fork` a parent that has touched 0 to 1 GiB, then have the child write every page. Two runs:

| Parent touched | `fork` | Child writes every page | Faults | per fault |
|---:|---:|---:|---:|---:|
| 0 | 0.091 · 0.087 ms | — | 0 · 1 | — |
| 64 MiB | 2.002 · 1.864 ms | 42.9 · 43.5 ms | 16,384 | 2,617 · 2,654 ns |
| 256 MiB | 6.991 · 5.426 ms | 162.9 · 170.0 ms | 65,536 | 2,486 · 2,594 ns |
| **1 GiB** | **18.9 · 20.9 ms** | **775 · 780 ms** | **262,144** | **2,957 · 2,975 ns** |

- **Forking a 1 GiB process took about 20 ms**: copying 2 MiB of page tables and write-protecting 262,144 entries. **The copying of memory was deferred, not avoided** — a child that wrote every page spent 780 ms doing it, one fault at a time — **but most children call `exec` at once and never write at all**, and they pay only the 20 ms.
- **Each copy-on-write fault cost 2.5–3.0 µs**, against 1.8–1.9 µs for a demand-zero fault (§1): copying 4 KiB costs more than zeroing it.

**xv6 copies everything.** L16 §5's fork took **1,096 pages**, 1,028 of them a byte-for-byte copy of a process that — like `sh` forking to run a command — was about to discard them in `exec`. **Adding copy-on-write to xv6 is part of Project 2.**

---

## 5. xv6 Allocates Eagerly

**`memx` showed the other half: xv6 has no demand paging either.**

```
sbrk(4096): 1 fewer, size 16384
```

**The page was taken from the free list before the program touched it.** `sbrk` calls `growproc`, which calls `allocuvm`, which allocates and zeroes every new page at once — and `exec` does the same for a program's whole image. **In xv6, every page a process has is a page in RAM.** That is what makes its page-fault handler so simple: a fault is always a bug.

| | xv6 | Linux |
|---|---|---|
| `sbrk` / `mmap` of *n* pages | *n* frames allocated and zeroed now | a VMA recorded; nothing allocated |
| first read of an untouched page | cannot happen: it was allocated | the shared zero page, 1 fault |
| first write | cannot fault | a zeroed frame, 1 fault, **~1.9 µs** |
| `fork` of a 4 MiB / 1 GiB process | **1,096 pages copied** / — | page tables copied, **~20 ms for 1 GiB** |
| a write to a shared page after `fork` | cannot happen: nothing is shared | copy one page, **~2.7 µs** |
| a fault outside the process's memory | kill the process | `SIGSEGV` |

---

## 6. Physical Memory: xv6's Free List and Linux's Buddy Allocator

**Every fault above ended with "allocate a frame".** Something has to keep track of which frames are free.

**xv6 keeps a linked list** (`kalloc.c`). Each free page's first bytes hold a pointer to the next; `kalloc` pops one and `kfree` pushes one. **56,790 pages were free** when `memx` started (L16 §5) — 222 MiB. Every allocation is one page, and any page will do, so a list is enough.

**Linux cannot get away with that**, because some allocations need **contiguous** frames: L17 §4's huge pages need 512; device buffers and kernel stacks need several. **The buddy allocator** keeps free blocks of 2⁰, 2¹, … 2¹⁰ pages. A request for 2*ᵏ* pages takes a free block of that order, or **splits** a larger one in half repeatedly; a freed block **merges** with its *buddy* — the other half of the block it was split from — if that is free too. **`/proc/buddyinfo` is readable by anyone**, one column per order. `buddy.c` read it, touched 512 MiB of 4 KiB pages, and unmapped them:

| Normal zone, free blocks of order | 0 (4 KiB) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | **9 (2 MiB)** | **10 (4 MiB)** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| before | 6,223 | 4,518 | 2,021 | 1,009 | 540 | 218 | 59 | 14 | 3 | **136** | **105** |
| 512 MiB touched | 4,015 | 3,937 | 1,805 | 926 | 492 | 195 | 50 | 12 | 2 | **7** | **47** |
| after `munmap` | 5,025 | 4,548 | 2,039 | 1,014 | 542 | 221 | 59 | 14 | 4 | **138** | **89** |

- **Allocating 131,072 single pages consumed large blocks**: 129 of the 2 MiB blocks and 58 of the 4 MiB ones were split up to supply them, while the small orders barely moved.
- **Freeing them merged most back** — order 9 recovered fully — **but not all**: order 10 came back to 89, not 105. **Some freed frames' buddies had been taken by other allocations meanwhile**, so they could not merge. **That is fragmentation**, and it is why L17 §4's huge-page requests sometimes fall back.

**On top of the buddy allocator, the kernel's small objects** — inodes, task structures, network buffers — **come from slab caches** that carve pages into equal-sized objects. `/proc/slabinfo` would show them; **on this machine it is readable only by root.**

---

## 7. Frame Numbers Are Secret

**`/proc/<pid>/pagemap` has one 64-bit entry per virtual page**, and its low 55 bits are **the physical frame number**. On the lab machines they are all zero:

```
$ ./pmwalk
...
present pages with a nonzero frame number: 0
```

**Linux stopped giving frame numbers to unprivileged programs in 2015**, after **Rowhammer**: repeatedly reading rows of DRAM can flip bits in *neighbouring* rows, and an attacker who knows which frames hold their own data can aim at frames holding page tables. **Knowing where your memory is physically became a security risk**, so only a process with `CAP_SYS_ADMIN` sees it. **Every other bit is still there**, and Lab 5 reads them.

**Reading another process's `pagemap` needs permission to inspect it**, and the result follows L13 §5's rules — with one difference:

| Target | `pmwalk PID` |
|---|---|
| a `sleep` this shell started | readable |
| **`pipewire`, same user, not a descendant** | **readable** |
| `init`, pid 1, owned by root | `Permission denied` |

**`ptrace_scope` 1 refused `gdb` attaching to a non-descendant in L13; it did not refuse reading its `pagemap`.** Yama restricts **attaching**; reading `/proc` files is a weaker access mode, allowed to the same user.

---

## 8. What to Take Away

1. **Linux allocates memory when it is first used, not when it is asked for.** A gigabyte mapped cost nothing; **each first touch cost ~1.9 µs and each later one ~14 ns.**
2. **A page fault carries the address (`CR2`) and why (the error code).** Linux resolves it or sends `SIGSEGV`; **xv6 kills the process**, because in xv6 no fault is legitimate.
3. **Reads of untouched memory share one zero page**; the first write takes a frame.
4. **`fork` copies page tables and write-protects**: 20 ms for a 1 GiB process, then ~2.7 µs per page actually written. **xv6 copied 1,028 pages** to do the same job.
5. **xv6 allocates every page eagerly**, which is why its fault handler can be three lines.
6. **Physical frames come from a free list in xv6 and a buddy allocator in Linux**, which can supply contiguous blocks and fragments as allocations interleave: **16 of 105 4 MiB blocks did not come back.**
7. **Frame numbers have been hidden from users since Rowhammer.**

---

## Exercises

1. `faultcost`'s first pass took 262,147 faults for 262,144 pages. **Where might the other three have come from?**
2. A program reads every page of a fresh 1 GiB mapping, then writes every page. **How many faults, and roughly how long**, using §1 and §3?
3. **Predict `pmlab cow`'s parent line** after the child exits: which pages are exclusive, and does the parent's next write to page 1 fault? Then run it.
4. `sh` forks and the child calls `exec`. **With copy-on-write, which of the parent's pages are ever copied?** Why is even that more than zero?
5. A buddy allocator has one free block of order 10 and receives requests for 3 pages, 1 page and 5 pages. **Draw the splits**, and say what is free afterwards.

---

*CS 202 · Week 5 · L18 · © CSE Department*
