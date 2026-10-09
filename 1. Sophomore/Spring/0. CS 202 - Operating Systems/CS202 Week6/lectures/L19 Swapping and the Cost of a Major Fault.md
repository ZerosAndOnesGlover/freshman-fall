# CS 202 · Operating Systems
## Week 6 · Lecture 1 of 3
### Swapping, and the Cost of a Major Fault

*“Around computers it is difficult to find the correct unit of time to measure progress. Some cathedrals took a century to complete. Can you imagine the grandeur and scope of a program that would take as long?”* — Alan Perlis, "Epigrams on Programming" (1982), #28

---

**Sat:** Monday of Week 6, 09:00–09:50, VNC 101, **after Quiz 6** · **Reading:** OSTEP Ch. 21 · **Next:** L20, choosing a victim

**Coursework:** 📊 **Quiz 6** today · 🔬 **Lab 5** Tue this week 15:00–16:50 · 📝 **PS 6** released Wed this week, due Fri of Week 7 17:00 · 📝 **PS 5** due Fri this week 17:00

---

## 1. What xv6 Does: Refuse

Week 5 left every page in RAM and every allocation eager. **So what happens when there are no free pages?** `memhog` calls `sbrk` until it fails, on a machine with 512 MiB:

```
$ memhog
free pages at start: 56790
allocuvm out of memory
sbrk refused after 56735 pages; free pages now 0
fork returned -1
gave it back: free pages 56735
```

**`kalloc` returned 0, `allocuvm` undid its partial work, and `sbrk` returned −1.** The process was not killed: it was **told**. `fork` then failed the same way — `copyuvm` could not allocate — and the shell, which needed no memory, went on running.

**This is a complete and correct answer to running out of memory**, and it has two costs. **A program that asks for memory it will not use is refused anyway** (Week 5's gigabyte for free is impossible), and **every page a process holds is a page nobody else can have**, however long ago it was last touched.

---

## 2. What Linux Does: Take Pages Back

**Linux gives out memory it does not have** (L21 §4) and then, when it runs short, **takes pages back from processes that are using them** — *reclaim*. What happens to a page's contents depends on where else they exist:

| Page | To reclaim it | To get it back |
|---|---|---|
| **file-backed, clean** — program code, a mapped file | **drop it**; the copy on disk is current | read it from the file |
| **file-backed, dirty** | **write it back** to the file, then drop | read it from the file |
| **anonymous** — heap, stack, `MAP_ANONYMOUS` | **write it to swap**; there is nowhere else | read it from swap |
| **untouched anonymous** | nothing to do; it has no frame (L18 §1) | a zero-filled fault |

**Swap space on the reference machine** is a file, not a partition:

```
$ swapon --show
NAME      TYPE SIZE USED PRIO
/swap.img file   4G   0B   -1
$ cat /proc/sys/vm/swappiness
60
```

**`swappiness` weighs anonymous against file pages**: at 60, the kernel is somewhat more willing to drop file pages than to swap. **`zswap` — a compressed cache in RAM in front of swap — is off here** (`/sys/module/zswap/parameters/enabled` is `N`), so a swapped page really goes to the SSD.

**Week 5's Lab already did this by hand**: `madvise(MADV_PAGEOUT)` reclaimed four pages, and `pagemap` showed them **swapped**, with the contents intact on the way back.

---

## 3. What a Major Fault Costs

**A fault that must read the page from disk is a *major* fault**; one the kernel can satisfy from memory — a zero page, a copy-on-write copy, a page still in the page cache — is a *minor* fault. `getrusage` counts them separately.

`thrash.c` fills 256 MiB, then reads random pages for four seconds, **inside a cgroup whose memory limit is smaller than that** (L21 §2 explains the scope). Two limits, from the reference machine's NVMe swap:

| Limit | Reads in 4 s | Major faults | **Time per major fault** |
|---:|---:|---:|---:|
| 224 MiB | 344,720 | 44,483 | **90 µs** |
| 64 MiB | 58,160 | 43,836 | **91 µs** |

**About 90 µs**, and the same at both limits: the machine is doing one thing — waiting for the SSD, one page at a time. Put beside Week 5's costs:

| Event | Cost | Ratio to a TLB hit |
|---|---:|---:|
| TLB hit and cache hit (L17 §3) | ~8 ns | 1 |
| Minor fault: demand-zero (L18 §1) | 1.9 µs | ~240 |
| Minor fault: copy-on-write (L18 §4) | 2.7 µs | ~340 |
| **Major fault from swap** | **90 µs** | **~11,000** |

**A major fault costs about fifty minor ones, and about eleven thousand ordinary accesses.** That is the whole reason page replacement matters: **the policy's job is to make this event rare** (L20).

---

## 4. Where the Time Goes: Pressure

**The kernel measures how much time its tasks lose waiting for memory** — *pressure stall information*, in `/proc/pressure/memory` and per cgroup. `some` is the share of time at least one task was stalled; `full` the share when every task was.

Measured inside the thrashing scope, over the whole run:

| Limit | memory pressure (`some`/`full`) | I/O pressure (`some`/`full`) |
|---|---|---|
| 224 MiB | 6.1% / 6.1% | **18.2% / 18.2%** |
| 64 MiB | 5.5% / 5.5% | **14.4% / 14.2%** |

**Most of the waiting is counted as I/O pressure, not memory pressure** — the process is blocked on a read from the swap file, and that is what the I/O counter is for. **Memory pressure counts the time spent *reclaiming*** — scanning lists, writing pages out, compacting — rather than the time spent waiting for a page to come back.

**It matters because a userspace daemon acts on these numbers** (L21 §3), and because they are the only numbers a program can read about a slowdown it cannot otherwise see: **the process is not blocked in any system call it made, and `top` shows the CPU idle.**

---

## 5. Who Does the Reclaiming, and When

- **`kswapd`**, a kernel thread per node, wakes when free memory falls below a **low watermark** and reclaims until it reaches a **high** one. **Two watermarks, not one**, so that it does useful batches instead of restarting constantly — and so that allocation can usually proceed while it works.
- **Direct reclaim** happens when an allocation finds no free page and the allocating process must reclaim **in its own context**, before its allocation returns. **That is the stall that memory pressure counts.**
- **A cgroup with a limit reclaims at its own limit**, regardless of how much memory the machine has free. `memory.events` counts it: the 128 MiB-in-64 MiB run of Lab 6 shows `max 269` — the limit was hit 269 times, each time forcing reclaim inside the scope.

**Reclaim chooses victims by the policy in L20.** When it cannot free anything — nothing left that is droppable or swappable — the allocation fails, and **Linux does what xv6 did, except that it kills instead of returning −1** (L21 §5).

---

## 6. What xv6 Would Need

To swap, xv6 would need four things it does not have:

1. **Somewhere to put pages** — a region of the disk, with an allocator for its blocks.
2. **A way to record where a page went.** A page-table entry with `PTE_P` clear is ignored by the CPU, **so its other bits are free for the kernel to use** — exactly what Linux does, and what Lab 5 read out as "swap type and offset".
3. **A fault handler that is not `panic`.** L18 §2's `trap` kills the process; it would have to look the address up, read the page back, install it, and return.
4. **A victim policy** — and the accessed bit to run it on.

**Project 2 asks for the first three, on a small scale.** L20 is the fourth.

---

## 7. What to Take Away

1. **xv6 refuses**: `kalloc` fails, `sbrk` returns −1, `fork` returns −1, and nothing dies. **Simple, and it wastes memory on pages nobody is using.**
2. **Linux reclaims**: clean file pages are dropped, dirty ones written back, **anonymous pages go to swap** — here a 4 GiB file on NVMe, with `swappiness` 60 and `zswap` off.
3. **A major fault cost 90 µs** on this machine — **fifty minor faults, or eleven thousand cache-hit accesses.**
4. **Most of the stall shows up as I/O pressure**; memory pressure counts reclaim work. Both are visible per cgroup, and are the only measure of a slowdown that looks like an idle machine.
5. **`kswapd` reclaims in the background between two watermarks; direct reclaim happens in the allocating process** — and a cgroup reclaims at its own limit.

---

## Exercises

1. `memhog` got 56,735 pages of the 56,790 that were free. **Where did the other 55 go?** *(What does `sbrk` need besides the pages themselves?)*
2. A program maps a 2 GiB file and reads it all on a machine with 1 GiB free. **How many major faults, and how much swap is used?** Why is the answer different from the same program using anonymous memory?
3. Using §3's numbers: a program takes 1 s of CPU and 20,000 major faults. **What is its runtime?** How many faults would keep the slowdown below 10%?
4. **Why is a major fault's cost roughly the same at a 224 MiB limit and at a 64 MiB limit**, when the second is four times shorter of memory?
5. xv6's `sbrk` returns −1 when memory runs out; Linux's `malloc` almost never does. **Name two ways a Linux program can nevertheless find out that memory is short** before something is killed.

---

*CS 202 · Week 6 · L19 · © CSE Department*
