# CS 201 · Lab 6 — Solutions and TA Notes
## Instructor Only

---

> **Unmarked.** Four checkpoints. All figures measured on the lab image.

---

## Timing

| Part | Budget | Reality |
|---|---|---|
| 1 — address space | 20 min | 15 min |
| 2 — demand paging | 25 min | 25 min |
| 3 — copy-on-write | 25 min | 25 min. **Warn about the buffering trap first** |
| 4 — TLB isolation | 30 min | **Protect this.** The best measurement of the week |

---

## Part 1

**Answers:**

1. Code in `r-xp`, data and bss in `rw-p`, heap in `[heap]` `rw-p`, stack in `[stack]` `rw-p`, `printf` in libc's `r-xp` mapping.
2. **No region is both `w` and `x`.** This is **W^X**, enforced by the NX bit. **Week 3's Lab Part 5.1** disabled it for a whole binary by omitting `.note.GNU-stack`, turning `GNU_STACK` from `RW` to `RWE`.
3. **Different sections need different protections** — read-only data, executable code, relocations, writable data — so the file is mapped four times with four permission sets. **One physical copy, shared by every process using libc.**
4. **The base addresses change every run; the relative layout and the permissions do not.** That is **ASLR**.
5. **`[vdso]`** is a kernel-provided page of code mapped into every process so that a few calls — notably `clock_gettime` and `gettimeofday` — run **without a mode switch**. Every timing loop in Weeks 4 and 5 went through it.

> Q2 is the one to dwell on. Students have *seen* NX as an ELF flag; this is the first time they see
> it as a property of mapped regions.

**✅ CHECKPOINT 1**

---

## Part 2

```
start                      RSS=  1444 KiB  minor faults=74
after malloc(512 MiB)      RSS=  1580 KiB  minor faults=86
after touching every page  RSS=525864 KiB  minor faults=131157
```

*(Verified.)* **`malloc` of 512 MiB cost 136 KiB.** Let the room react before explaining.

### 2.1

$512 \text{ MiB}/4096 = 131\,072$ pages against $131\,157 - 86 = 131\,071$ faults. **One per page.**

### 2.2

$1967 - 19 = \mathbf{1948}$ ns $\approx$ **6200 cycles**. *(Verified; repeat gave 1887 ns.)*

Against Week 4's ladder: **~14 DRAM accesses, ~1550 L1 hits.** For a fault that touches no disk whatsoever.

### 2.3

Trap to the kernel; find the VMA covering the address; check permissions; allocate a physical frame; **zero it**; install the PTE; return and retry the instruction.

**The zeroing is the security-mandated step.** Without it, a fresh page would hand the process whatever the previous owner left in that frame — passwords, keys, other users' data. **Isolation costs 4096 bytes of stores per fault**, and that is a large part of the 6200 cycles.

**✅ CHECKPOINT 2**

---

## Part 3

> **Announce the buffering trap before they start.** Without `setvbuf(stdout, NULL, _IONBF, 0)`, the
> child inherits the parent's stdio buffer and `_exit` skips the flush — **the child's output
> vanishes entirely.** This happened on the first run of this experiment and cost ten minutes.

```
parent before fork:  RSS=263596 KiB
child at birth:      RSS=263068 KiB  minor faults=14
child after writing: RSS=263260 KiB  minor faults=65566 (+65536)
fork() itself took   0.0043 s for a 256 MiB address space
```

*(Verified.)*

**Answers:**

1. At ~10 GB/s, copying 256 MiB would take **25–50 ms**. `fork` took **4.3 ms** — an order of magnitude less. It spent that time **duplicating page tables and marking pages read-only**, not copying data.
2. The child **has** 256 MiB of address space; it **owns** essentially none of it. Every page is shared with the parent and marked read-only in both.
3. **Each write hit a read-only PTE and faulted.** The kernel then consulted the VMA, saw the region was logically writable, copied that one frame, marked it writable, and resumed. **65 536 pages, 65 536 faults.**
4. **The R/W bit.** Clearing it on shared pages is the entire mechanism.
5. **Almost none.** `exec` replaces the address space, so all that deferred copying is never performed. **That is the design's justification** — the common case does no work at all.

**✅ CHECKPOINT 3**

---

## Part 4 — the important one

| stride | pages | ns/access |
|---:|---:|---:|
| 64 B | **8** | **1.24** |
| 256 B | 32 | 4.28 |
| 1 KiB | 128 | 12.68 |
| 4 KiB | 512 | 14.57 |
| 16 KiB | 2048 | 15.77 |
| 64 KiB | **8192** | **27.57** |

*(Verified.)*

**Put the constant on the board before the numbers: 512 pointers, 512 cache lines, 32 KiB, L1-resident in every row.**

**Answers:**

1. Row 1's **1.24 ns matches Week 4's L1 latency of 1.22 ns** — measured independently, two weeks apart. The 22× at the bottom is **pure address translation**: the same L1-resident data spread across 8192 pages exceeds the TLB by orders of magnitude.
2. Tripling between 8 and 32 pages puts the **L1 dTLB at roughly 64 entries**. Accept 32–128 with reasoning.
3. **Reach = entries × page size.** $64 \times 4\text{ KiB} = 256$ KiB; $64 \times 2\text{ MiB} = 128$ MiB.
4. **Count pages as well as cache lines.** Week 4 said data must fit in cache; this says it must *also* be reachable by the TLB, and those are different capacities.

### 4.1 — the null result

Huge pages gave **1.00×–1.06×** across 1 MiB to 1 GiB. *(Verified.)*

**Because that benchmark has one pointer per 4 KiB page, so every access is a cache miss too.** The ~130 ns DRAM latency dominates and hides translation. **Huge pages fix translation; translation was not the bottleneck.**

**A benchmark that would show it:** §4's design — cache-resident data spanning many pages. With `MADV_HUGEPAGE`, 512 lines over 8192 4 KiB pages becomes 512 lines over ~16 huge pages, and the TLB holds them all.

> **This is the third time the course has made this point** — Week 4 §5.3's control, Week 5's AVX
> sweep, and now this. **Say so explicitly.** The pattern is the transferable lesson: *an intervention
> only shows up when its bottleneck is the one that binds*, and a null result tells you which
> bottleneck you actually had.

**✅ CHECKPOINT 4**

---

## What Success Looks Like

1. Read `/proc/PID/maps` and identify every region and its permissions.
2. Distinguish virtual size from resident size, and explain why `malloc` is nearly free.
3. Explain COW from the fault counts, not from a diagram.
4. **Say that cache residency and TLB reach are separate capacities**, having measured both.

Item 4 is what Week 7 and Week 11 both build on.

---

*CS 201 · Week 6 · Lab 6 Solutions · Instructor Only*
