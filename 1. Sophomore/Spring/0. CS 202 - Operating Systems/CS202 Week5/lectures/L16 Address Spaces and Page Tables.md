# CS 202 · Operating Systems
## Week 5 · Lecture 1 of 3
### Address Spaces and Page Tables

---

**Sat:** Monday of Week 5, 09:00–09:50, VNC 101, **after Quiz 5** · **Reading:** OSTEP Ch. 13, 18, 20; xv6 book Ch. 2 · **Next:** L17, the TLB

---

## 1. Every Process Gets the Same Addresses — Almost

`aspace.c` prints where three things live. **Run twice**:

| | First run | Second run |
|---|---|---|
| `main` | `0x56890e4a20c0` | `0x629a5e82a0c0` |
| a `malloc` block | `0x56893b9e62a0` | `0x629a7d5222a0` |
| a local variable | `0x7ffd4461f8e4` | `0x7ffe3a0340f4` |

**The addresses differ between runs, and within each run they are enormous** — the stack sits nearly 128 TiB above zero, in a machine with 7.7 GiB of memory. Neither fact is possible if a program's addresses are places in RAM.

**They are not.** Every address a program uses is **virtual**: the CPU translates each one, on every access, to a **physical** address, using tables the kernel controls. That one indirection buys three things at once:

- **Isolation.** A process can name only memory its tables map. Another process's memory has no virtual address in it.
- **Relocation.** The program is linked as if it owned the whole space; the kernel puts its pages wherever there is free memory. **The randomisation above — ASLR — is the kernel choosing different virtual placements each run**, so that an attacker cannot know where code is.
- **Sparseness.** A process can use a few pages near zero, a few near 128 TiB, and nothing between, and pay only for what it uses.

**This week is how the translation is done (L16), how it is made fast (L17), and how the kernel uses it to avoid doing work until it must (L18).**

---

## 2. Before Paging: Base and Bounds, and Segments

**The simplest translation is one register pair**: *physical = base + virtual*, and a fault if *virtual ≥ bounds*. It gives isolation and relocation, costs one addition, and is how early time-sharing systems worked.

**It fails at sparseness.** The whole range from 0 to the top of the stack must be one contiguous block of physical memory, including the unused middle. **Segmentation** gives each region — code, heap, stack — its own base and bounds, which removes the hole but leaves **external fragmentation**: variable-sized segments come and go, and free memory ends up in pieces too small to use.

**x86-64 still has segment registers** — Week 0's current privilege level lives in `CS` — but every segment's base is 0 and its limit is everything. **Translation is done entirely by paging.**

---

## 3. Pages and Frames

**Paging cuts both spaces into fixed-size pieces**: virtual **pages** and physical **frames**, 4 KiB each on x86. An address splits into a **page number** and an **offset**:

```
  32-bit virtual address
  +--------------------------------+------------+
  |    virtual page number (20)    | offset (12)|
  +--------------------------------+------------+
                  |                       |
          page table lookup               | unchanged
                  v                       v
  +--------------------------------+------------+
  |   physical frame number (20)   | offset (12)|
  +--------------------------------+------------+
```

**The offset passes through unchanged**; only the page number is translated. Because every piece is the same size, **any free frame fits any page** — no external fragmentation at all. The price is **internal** fragmentation (the unused tail of a process's last page) and **a table to hold the translations**.

**A page-table entry holds the frame number and permission bits.** On x86:

| Bit | Name | Meaning when set |
|---|---|---|
| 0 | `P` | **present** — the entry is valid; otherwise any access faults |
| 1 | `W` | **writable** — otherwise a write faults |
| 2 | `U` | **user** — otherwise an access from ring 3 faults |
| 5 | `A` | accessed — **set by the CPU** on any use |
| 6 | `D` | dirty — **set by the CPU** on a write |
| 12–31 | | the frame number |

**The CPU checks P, W and U on every access, and sets A and D itself.** The kernel reads A and D to learn what a process has been doing — Week 6's page replacement depends on them.

---

## 4. xv6's Two-Level Page Table

**A flat table for 32-bit addresses needs 2²⁰ entries of 4 bytes: 4 MiB per process**, almost all of it describing addresses the process never uses. **x86's answer in 32-bit mode is two levels.** The top 10 bits index a **page directory**; its entry points to a **page table**, indexed by the next 10; its entry gives the frame. From xv6's `mmu.h`:

```c
// A virtual address 'la' has a three-part structure as follows:
// +--------10------+-------10-------+---------12----------+
// | Page Directory |   Page Table   | Offset within Page  |
// |      Index     |      Index     |                     |
// +----------------+----------------+---------------------+
#define PDX(va)         (((uint)(va) >> PDXSHIFT) & 0x3FF)
#define PTX(va)         (((uint)(va) >> PTXSHIFT) & 0x3FF)
#define PTXSHIFT        12      // offset of PTX in a linear address
#define PDXSHIFT        22      // offset of PDX in a linear address
```

**Each directory entry covers 4 MiB.** A directory entry that is not present means *nothing in these 4 MiB is mapped* — and no page table exists for them. **That is where the saving comes from.**

**The kernel's walk**, `walkpgdir` in `vm.c`, is what the CPU does in hardware, written in C:

```c
static pte_t *
walkpgdir(pde_t *pgdir, const void *va, int alloc)
{
  pde_t *pde;
  pte_t *pgtab;

  pde = &pgdir[PDX(va)];
  if(*pde & PTE_P){
    pgtab = (pte_t*)P2V(PTE_ADDR(*pde));
  } else {
    if(!alloc || (pgtab = (pte_t*)kalloc()) == 0)
      return 0;
    // Make sure all those PTE_P bits are zero.
    memset(pgtab, 0, PGSIZE);
    *pde = V2P(pgtab) | PTE_P | PTE_W | PTE_U;
  }
  return &pgtab[PTX(va)];
}
```

Three details matter:

1. **Directory entries hold physical addresses** (`V2P`), because the CPU reads them without translation. **The kernel must convert back** (`P2V`) to read a table itself — it can do that because **xv6 maps all physical memory at `KERNBASE` = `0x80000000`**, so physical address *p* is virtual address *p* + `0x80000000`.
2. **A new table is zeroed**, so every entry starts not present.
3. **`mappages`** calls `walkpgdir(…, 1)` for each page and fills in the entry — **panicking with `remap` if one is already present**. You met that panic in L10 when two processes were given one page.

**Every process's directory has two halves.** Below `KERNBASE`, the process's own pages. From `KERNBASE` up, **the whole kernel** — `setupkvm` maps it into every new directory, so that a trap into the kernel needs no change of tables:

```c
static struct kmap { … } kmap[] = {
 { (void*)KERNBASE, 0,             EXTMEM,    PTE_W}, // I/O space
 { (void*)KERNLINK, V2P(KERNLINK), V2P(data), 0},     // kern text+rodata
 { (void*)data,     V2P(data),     PHYSTOP,   PTE_W}, // kern data+memory
 { (void*)DEVSPACE, DEVSPACE,      0,         PTE_W}, // more devices
};
```

**None of the kernel's entries has `PTE_U`**, so a user program that names a kernel address faults — Week 0's wall, enforced one entry at a time.

---

## 5. What the Tables Cost, in xv6

**To count, we added one system call to xv6**: `nfree()` returns the number of pages on the kernel's free list (`resources/nfree.patch`). `memx` grows itself and forks:

```
$ memx
size 12288, free pages at start: 56790
sbrk(4096): 1 fewer, size 16384
sbrk(4 MB) more: 1025 fewer, size 4210688
in child after fork: 1096 fewer than parent before fork
after child exits: 55764 (parent had 55764)
```

**`sbrk(4 MB)` took 1,025 pages**: 1,024 for the memory, and **one page table**, because the process's size crossed from its first 4 MiB into its second. **The fork took 1,096**, and every one can be accounted for:

| Pages | For |
|---:|---|
| **1,028** | the child's copy of the parent's memory: 4,210,688 bytes ÷ 4,096 |
| 2 | page tables for the user half: the first and second 4 MiB |
| 1 | the page directory |
| **64** | **page tables for the kernel half**: 224 MiB of `KERNBASE`…`PHYSTOP` is 56 directory entries; 32 MiB of `DEVSPACE` is 8 more |
| 1 | the child's kernel stack |
| **1,096** | |

**The process's own two page tables cost 8 KiB. The kernel's 64 cost 256 KiB — in every process.** For a small program that is most of its memory. **Linux avoids it** by sharing the kernel's lower-level tables among all processes: each process's top-level table points at the same kernel tables. xv6 builds them afresh each time, for simplicity. **PS 5 Q2 has you reproduce the 65 from `kmap[]` with your own page table.**

**The flat alternative** would be 4 MiB of table per process whatever it used — **a thousand pages, for a program that needed four.** Two levels cost at most one page more than flat, when every 4 MiB region is in use, and far less otherwise.

---

## 6. x86-64: Four Levels, 48 Bits

**With 64-bit addresses a two-level table cannot work.** Each level's table must fit in a page; with 8-byte entries a page holds **512** entries, so each level resolves **9 bits**. x86-64 uses four levels, which with the 12-bit offset gives **48-bit virtual addresses — 256 TiB**:

```
 63      48 47    39 38    30 29    21 20    12 11         0
+----------+--------+--------+--------+--------+------------+
| sign ext.|  PGD   |  PUD   |  PMD   |  PTE   |   offset   |
+----------+--------+--------+--------+--------+------------+
     16        9        9        9        9         12
```

*(Linux's names; Intel calls them PML4, PDPT, PD and PT.)* **L16 §1's stack address, split** by `aspace.c`:

```
0x7ffd4461f8e4 → PGD 255  PUD 501  PMD 35  PTE 31  offset 2276
```

**Bits 63–48 must copy bit 47** — a *canonical* address — or the CPU faults. That splits the space into two halves with a 16-exabyte hole between: **user space from 0 to `0x00007fffffffffff`, the kernel from `0xffff800000000000` up.** The stack's PGD index is **255, the last of the lower half**: Linux puts the stack at the top of user space.

**Measured**, the top of user space is one page lower still:

```
MAP_FIXED at 2^47-4096 -> 0xffffffffffffffff     (MAP_FAILED)
mmap hint 2^56 -> 0x7089ae420000                 (ignored)
```

**The last user page is never mapped** — a guard between user and kernel halves. **The hint above 2⁴⁷ was ignored** because this machine has only four levels. **The kernel was built for five** — `CONFIG_PGTABLE_LEVELS=5` in `/boot/config-7.0.0-31-generic` — which would give 57-bit addresses, **but the CPU lacks the `la57` flag** in `/proc/cpuinfo`, so the kernel folds the fifth level away at boot. **One kernel image supports both.**

**And one page of the kernel half is visible to every process:**

```
ffffffffff600000-ffffffffff601000 --xp 00000000 00:00 0      [vsyscall]
```

**Four levels make a TLB miss cost four memory reads** before the one the program wanted. L17 measures what that does.

---

## 7. Linux's Tables, Measured

`/proc/<pid>/status` reports **`VmPTE`: the memory in this process's page tables.** `faultcost.c`:

```
before mmap:        VmRSS   1460 kB  VmPTE   44 kB
after 1 GiB mmap:   VmRSS   1592 kB  VmPTE   44 kB  VmSize 1051272 kB
after touching:     VmRSS 1050236 kB  VmPTE 2096 kB
64 pages, 1 GiB apart:              VmPTE 44 -> 556 kB
```

- **Mapping a gigabyte costs no table memory at all.** `mmap` records a region; no entries exist until pages are used (L18).
- **Touching all 262,144 pages added 2,052 kB of tables**: 513 pages — **512 PTE pages** at 512 entries each, and **one PMD page** to point at them.
- **Sixty-four pages, one per gigabyte, added 512 kB**: 128 pages — **for each page, one PTE page and one PMD page**, since no two share either. **64 pages of data, 256 KiB, cost twice their own size in tables.**

**That last is the multi-level table's weakness**: it saves memory for dense regions and sparse gaps, and **wastes it on addresses scattered one per region**. Real programs are mostly dense, which is why the design works.

---

## 8. What to Take Away

1. **Every address a program uses is virtual**, translated by the CPU on every access through tables the kernel owns. That gives **isolation, relocation and sparse address spaces** at once.
2. **Paging splits addresses into page number and offset**; any frame fits any page. **The entry's P, W and U bits are checked by the CPU on every access**; A and D are set by it.
3. **xv6 uses x86's two levels, 10 + 10 + 12.** `walkpgdir` is the hardware's walk in C, and allocates a zeroed table on demand.
4. **Every xv6 process maps the whole kernel**, at a cost measured exactly: **65 of the 1,096 pages** a fork of a 4 MiB process took.
5. **x86-64 uses four levels, 9 + 9 + 9 + 9 + 12, for 48-bit canonical addresses.** User space stops one page below 2⁴⁷; this kernel can do five levels, and this CPU cannot.
6. **Table memory follows use, not size**: a gigabyte mapped costs nothing, touched costs 2 MiB, and 64 scattered pages cost 512 KiB.

---

## Exercises

1. Split `0x00401ff0` into xv6's directory index, table index and offset. Then split `0x7ffe3a0340f4` into x86-64's five fields.
2. **What is the largest amount of page-table memory an xv6 process can need** for its user half, and for what address-space layout?
3. xv6's `walkpgdir` gives directory entries `PTE_W | PTE_U` even for kernel addresses. **Construct the access that would be wrongly allowed if the page-table entry were equally generous**, and say why it is not.
4. The fork in §5 took 1,096 pages. **Predict the number for a process of size 12,288 bytes** — the size `memx` had at start. What fraction is the kernel mapping?
5. A 4-level table for a process that touches **one page in every 2 MiB** across 1 GiB. How much table memory, and how does that compare with the pages themselves?

---

*CS 202 · Week 5 · L16 · © CSE Department*
