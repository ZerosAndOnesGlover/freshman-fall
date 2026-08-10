# CS 201 · Computer Organization & Architecture
## Week 6 · Lecture 1 of 3
### Virtual Memory and the Page Table

---

**Reading:** CS:APP §9.1–9.6 · **Previous:** L18, SIMD and Amdahl's Law

---

## 1. The Illusion

Every process believes it owns a private, contiguous 256 TB address space starting at zero-ish and running to $2^{48}$.

**None of that is true.** Physical memory is 8 GB, shared by a hundred processes, and fragmented. **Virtual memory is the machinery that maintains the lie**, and it buys three things at once:

| It provides | Because |
|---|---|
| **Isolation** | A process cannot name an address it has not been given. Not "is not allowed to" — **cannot express** |
| **Relocation** | Every program can be linked to load at the same address, because "the same address" means something different per process |
| **Overcommit** | You can allocate more than exists, because allocation is a promise rather than a delivery (L21) |

**The isolation point is the strongest one.** Week 3 showed there is no bounds check on `ret`. There is no bounds check here either — the protection is that a bad pointer simply has no translation, and the hardware faults.

---

## 2. Pages

Translation is not per byte — that would need a table with $2^{48}$ entries. **Memory is divided into fixed-size pages**, and translation is per page.

```
$ getconf PAGESIZE
4096
```

*(Verified.)* **4 KiB, and the address splits accordingly:**

```
 47                          12 11        0
┌──────────────────────────────┬───────────┐
│      virtual page number     │  offset   │
└──────────────────────────────┴───────────┘
              36 bits              12 bits
```

**The offset is not translated.** Byte 37 of a virtual page is byte 37 of whatever physical frame it maps to. **Only the page number is looked up** — which is why the page size sets the granularity of everything that follows.

> **Compare with Week 4's cache line split.** Same idea, different sizes: a cache splits the address
> into tag/index/offset with a 64-byte block; the MMU splits it into page-number/offset with a 4096-byte
> block. **The bottom 12 bits pass through untouched in both.**

---

## 3. Why the Page Table Is a Tree

A flat table mapping all 36 bits of page number would need $2^{36}$ entries × 8 bytes = **512 GB**, per process. Absurd.

**But address spaces are overwhelmingly empty.** A process uses a few megabytes near the bottom, a stack near the top, and some libraries in between — and nothing at all in the vast gaps. A tree can leave the gaps unrepresented.

**x86-64 uses four levels.** The 36-bit page number splits into four 9-bit indices:

```
 47      39 38      30 29      21 20      12 11        0
┌──────────┬──────────┬──────────┬──────────┬───────────┐
│   PGD    │   PUD    │   PMD    │   PTE    │  offset   │
└──────────┴──────────┴──────────┴──────────┴───────────┘
     9          9          9          9          12
```

**9 bits is not arbitrary.** $2^9 = 512$ entries × 8 bytes each $= 4096$ bytes — **exactly one page.** Every level of the page table is itself a page, so the same allocator manages tables and data.

$$9 + 9 + 9 + 9 + 12 = 48 \text{ bits}$$

**`cr3` holds the physical address of the top-level table**, and it is reloaded on every context switch. That one register is what makes each process's address space private.

---

## 4. What a Walk Costs

To translate one address the hardware reads four tables in sequence — **and each read is itself a memory access.**

$$\text{4 table reads} + \text{1 data access} = \mathbf{5 \text{ memory accesses for one load}}$$

At Week 4's numbers, if the tables are not cached, that is potentially $5 \times 438$ cycles for a single `mov`.

**This would be unusable**, which is why the next lecture exists: the TLB caches translations, and hits are essentially free.

---

## 5. What Is in a Page Table Entry

Each 8-byte entry holds a physical frame number and a set of flags. The ones that matter:

| Bit | Meaning | Used for |
|---|---|---|
| **P** — present | Is this page in physical memory? | 0 ⇒ **page fault** (L21) |
| **R/W** | Writable? | Read-only text; **copy-on-write** |
| **U/S** | User or supervisor only? | The kernel/user boundary |
| **A** — accessed | Set by hardware on any access | **Page replacement** (L21) |
| **D** — dirty | Set by hardware on a write | Whether eviction needs a write-back |
| **NX** | No-execute | **The defence Week 3's Lab 5.1 disabled** |

**The hardware sets A and D; the operating system reads and clears them.** That is the entire interface through which the OS learns which pages are being used — and it is why the replacement algorithms in L21 are shaped the way they are.

**NX is here.** In Week 3 you added a missing `.note.GNU-stack` directive and watched `GNU_STACK` go from `RWE` to `RW`. **This bit is what that changed**, one page at a time.

---

## 6. A Real Address Space

```
$ ./maps
code   (main)      0x58302ed37239
data   (init)      0x58302ed3a010
bss    (uninit)    0x58302ed3a024
heap   (malloc)    0x58305f6d62a0
stack  (local)     0x7ffd32925e94
libc   (printf)    0x7cc6f5c60100
page size          4096
```

and the kernel's own view:

```
58302ed36000-58302ed37000 r--p   ...  /…/maps        <- rodata
58302ed37000-58302ed38000 r-xp   ...  /…/maps        <- code: read + EXECUTE, no write
58302ed3a000-58302ed3b000 rw-p   ...  /…/maps        <- data: read + write, no execute
58305f6d6000-58305f6f7000 rw-p   ...  [heap]
7cc6f5c28000-7cc6f5db0000 r-xp   ...  /usr/lib/…/libc.so.6
7cc6f5eb4000-7cc6f5eb6000 r-xp   ...  [vdso]
```

*(Verified — `/proc/self/maps`.)*

**Four things worth reading off this.**

**Permissions are per region, and no region is both writable and executable.** The code is `r-xp`; the data is `rw-p`. This is NX enforced through the page table — **the W^X property**, and the reason Week 9's attacker cannot simply write shellcode onto the stack and jump to it.

**The same file is mapped several times with different permissions.** libc appears four times because its read-only, executable, relocatable and writable sections need different protections. **One file, several mappings, one physical copy shared by every process using libc.**

**The addresses are randomised.** Run it again and every base moves — ASLR, which exists because Week 3 showed that knowing an address is most of an exploit.

**`[vdso]` is a page the kernel maps into every process** so that calls like `gettimeofday` can run without a mode switch. All those `clock_gettime` calls in Weeks 4 and 5 went there.

---

## 7. Virtual Memory Is Not About Memory

The name is misleading. **Virtual memory is an indirection layer, and once you have one you can do more than pretend RAM is bigger.**

| Use | How the indirection is used |
|---|---|
| **Isolation** | Two processes' identical addresses map to different frames |
| **Sharing** | Two processes' different addresses map to the **same** frame — libc, shared memory |
| **Copy-on-write** | Shared and read-only until someone writes (L21) |
| **Memory-mapped files** | A page's backing store is a file rather than swap |
| **Guard pages** | Deliberately unmapped pages that fault on touch — **Week 3's stack limit** |
| **Overcommit** | Promise address space now, find frames later |

**Every one of these is a program you could not write without the layer.** `fork` would be unusable if it had to copy; shared libraries would need a copy per process; `mmap` would not exist.

---

## 8. What to Take Away

1. **Virtual memory buys isolation, relocation and overcommit** — isolation being the strongest.
2. **4 KiB pages**; the low 12 bits are the offset and pass through untranslated.
3. **Four levels of 9 bits**, because 512 entries × 8 bytes is exactly one page.
4. **A full walk is four extra memory accesses**, which is why the TLB exists.
5. **The PTE's A and D bits are the OS's only window** into what is being used.
6. **NX lives in the PTE.** `r-xp` and `rw-p` in `/proc/self/maps` are W^X in action.
7. **Indirection, not memory.** Sharing, COW, `mmap` and guard pages all come free with the layer.

---

## Exercises

1. Compute the size of a flat page table for a 48-bit address space with 4 KiB pages and 8-byte entries. Then for 2 MiB pages. What does that tell you about why huge pages exist?
2. Verify that a 512-entry table of 8-byte entries is exactly one page, and explain why that is a design goal rather than a coincidence.
3. A process maps 100 GB but touches 4 MB. Roughly how many page-table pages does it need at each of the four levels?
4. Give the four indices and the offset for virtual address `0x00007f3c2a4b1000`. Show the bit split.
5. `/proc/self/maps` shows libc mapped four times. Explain why one mapping with `rwxp` would be both simpler and much worse.
6. `[vdso]` lets `clock_gettime` avoid a system call. What does that save, and why can it not be done for `read`?

---

*Next: L20 — the TLB, and what translation actually costs when it misses.*
