# CS 202 · Problem Set 5 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for PS 5.** Q1 and Q5(a) are exact-output: a student who matches has implemented the rules. **The rest is arithmetic about memory and caches**, and the marks are for the arithmetic — a correct number with no derivation earns a third.

**Reference:** `solutions_instructor/pt2 reference (do not distribute).c`. It reproduces every expected output in the handout; the student skeleton compiles with no compiler output. **Every figure below was produced by running the reference** on the reference machine: i5-8250U, Ubuntu 24.04.4, kernel 7.0.0-31.

---

## Q1: The Page Table and the TLB (30 points)

### Reference functions

```c
static uint32_t *walk(uint32_t va, int alloc)
{
    uint32_t *pde = entry(pgdir, PDX(va));
    if (*pde & PTE_PS) return 0;
    if (!(*pde & PTE_P)) {
        if (!alloc) return 0;
        *pde = palloc() | PTE_P | PTE_W | PTE_U;
    }
    return entry(PTE_ADDR(*pde), PTX(va));
}

static int map(uint32_t va, uint32_t pa, uint32_t perm)
{
    uint32_t *pte = walk(va, 1);
    if (!pte || (*pte & PTE_P)) return -1;
    *pte = PTE_ADDR(pa) | perm | PTE_P;
    return 0;
}

static void tlb_invalidate(int c, uint32_t vpn)
{
    for (int i = 0; i < TLBSIZE; i++)
        if (tlb[c][i].valid && !tlb[c][i].big && tlb[c][i].vpn == vpn) tlb[c][i].valid = 0;
}

static int unmap(uint32_t va)
{
    uint32_t *pde = entry(pgdir, PDX(va));
    if (*pde & PTE_PS) return -2;
    uint32_t *pte = walk(va, 0);
    if (!pte || !(*pte & PTE_P)) return -1;
    *pte = 0;
    for (int c = 0; c < NCPU; c++)
        if (shootdown || c == cpu) tlb_invalidate(c, va >> 12);
    uint32_t pt = PTE_ADDR(*pde);
    for (int i = 0; i < 1024; i++)
        if (*entry(pt, i) & PTE_P) return 0;
    pfree(pt);
    *pde = 0;
    return 1;
}
```

`translate` is in the reference file, with its superpage cases (Q5). **The superpage lines are marked; a Q1-only submission omits them and is otherwise identical.**

### (a) [20]

Exact match: **20**. Otherwise, **3 per correct `map`/`unmap` line group, 8 for the translation lines, 3 per `stats` line**, to 20. **A `walk` that allocates when `alloc` is 0** shows up as `read c0000000` producing a table and the first `stats` line reading 4 frames: deduct 5.

### (b) [6]

**The three hits [2]:** `uread 00400abc` and `uwrite 00400abc` (after `read 00400abc` cached page `0x400`), and `read 80000010` (after `uread 80000010` cached page `0x80000`).

**A faulting access that hits [2]:** the TLB answers **what the translation is**, not whether this access is allowed. **The permission bits travel with the cached entry and are checked on every access** — a hit that skipped the check would let a user write through an entry cached by a kernel read. The real MMU does exactly this.

**The last `read` missed [2]** because `unmap 00401000` **invalidated** page `0x401` in the TLB; the walk then found no page table (it had been freed), so the access faulted.

**The first `unmap` freed no table [bonus sentence, no marks]:** page `0x401` was still mapped in the same table.

### (c) [4]

Any sequence in which **an address is translated while unmapped, then mapped, then translated again**:

```
read    00005000        # not present — suppose this were cached
map     00005000 00007000 w
read    00005000        # would still say FAULT not present
```

**Real hardware never caches a failed translation**: a TLB entry is loaded only from a present page-table entry. **After `map`, the kernel need not flush anything**, which is why adding mappings is cheap and removing them (Q4) is not. **[2]** for the sequence, **[2]** for the hardware rule.

---

## Q2: What the Tables Cost (20 points)

### (a) [8]

```
stats   page-table frames 65 (260 KiB)
```

**Derivation [4]:** `KERNBASE` to `KERNBASE + PHYSTOP`: `PHYSTOP` = `0xE000000` = 224 MiB → **56** directory entries, each needing a page table. `DEVSPACE` = `0xFE000000` to 2³² = 32 MiB → **8**. **64 tables + 1 directory = 65.** Note that the kernel-text range starts at a 4 MiB boundary and the I/O space and data are contiguous with it, so no range spills into an extra table.

**Reconciliation [4]** with L16 §5's 1,096: **1,028** user pages copied + **2** user page tables + **65** (directory and kernel tables) + **1** kernel stack. **The simulator's 65 is exactly the part that does not depend on the process.**

### (b) [6]

```
stats   page-table frames 513 (2052 KiB)
stats   page-table frames 257 (1028 KiB)
```

- **513** = 512 page tables (one page per 4 MiB, each in its own table) + 1 directory **[1]**.
- **257**: unmapping every second page left its table empty, so **256 tables were freed [1]**.
- **512 pages, fewest frames [1]: 2** — all 512 in one 4 MiB region, one table. **Most [1]: 513**, one page per table as here.
- **Worse than flat [2]:** a flat table is 1,024 frames (4 MiB). Two levels need more only if **more than 1,023 page tables** exist — **at least one page in 1,024 of the 1,024 directory ranges**, which needs **the whole 4 GiB** used, sparsely. **Worst case 1,025 frames: one page worse.** *(In xv6, where the top half is the kernel, the user half can never do it.)*

### (c) [6]

**Touching 1 GiB → 2,052 kB [2]:** 262,144 pages ÷ 512 entries = **512 PTE pages**; those 512 PTE pages are pointed at by 512 entries in **one PMD page** (each PMD page covers 1 GiB). **513 × 4 KiB = 2,052 KiB.** The PUD and PGD pages already existed.

**64 pages 1 GiB apart → 512 kB [2]:** each page needs its own PTE page **and** its own PMD page, since each gigabyte is covered by a different PMD page. **64 × 2 = 128 pages = 512 KiB.** They all fit under one PUD page (512 GiB each), which already existed.

**64 pages 2 MiB apart [2]:** each needs its own **PTE page** (one PTE page covers 2 MiB), but **all 64 fall under one PMD page**, which is new unless something else is mapped in that gigabyte: **64 + 1 = 65 pages = 260 KiB**. **Measured on the reference machine, three runs: `VmPTE 48 -> 308 kB`, +260 kB.** Accept 256 kB with a stated assumption that the PMD page existed.

---

## Q3: How Well an 8-Entry TLB Does (20 points)

### (a) [8]

| Pattern | Hits | Misses | Hit rate |
|---|---:|---:|---:|
| `seq`, one byte per page | 0 | 1,024 | **0.00%** |
| `seq`, every 16th byte | 261,120 | 1,024 | **99.61%** |
| random among 4 pages | 99,996 | 4 | **100.00%** |
| random among 8 pages | 99,996 | 4 | **100.00%** |
| random among 16 pages | 50,202 | 49,798 | **50.20%** |
| random among 64 pages | 12,693 | 87,307 | **12.69%** |
| random among 1,024 pages | 734 | 99,266 | **0.73%** |
| matrix, row order | 261,632 | 512 | **99.80%** |
| matrix, column order | 0 | 262,144 | **0.00%** |

*(**`reset` zeroes the counters but does not empty the TLB.** The 4-page run started with the last 8 pages of the sequential run cached, so it missed once for each of pages 0–3; the 8-page run started with pages 0–3 still cached, so it missed only for pages 4–7. The driver's `reset` is provided, so every correct submission shows these counts.)* **[1 per row, max 8.]**

### (b) [8]

- **Sequential, one byte per page**: every access is a new page and none is revisited — **no hit is possible [1]**.
- **Every 16th byte**: 256 accesses per page, **the first misses and the other 255 hit**: 255/256 = **99.61% [1]**.
- **4 or 8 random pages**: all fit in the TLB; **only the first access to each misses [1]**.
- **16 random pages [1]**: after warm-up the TLB holds 8 of the 16; a uniformly random page is among them with probability **8/16 = 50%**. LRU does no better than chance on uniform random access, because recency predicts nothing.
- **64 pages [1]**: **8/64 = 12.5%**, measured 12.69%. **1,024 pages**: 8/1,024 = 0.78%, measured 0.73%.
- **Row order [1]**: each row is 512 × 8 bytes = **exactly one page**, so the matrix is 512 pages visited one after another; **512 misses in 262,144 accesses** = 99.80%.
- **Column order [2]**: consecutive accesses are `n × 8` = 4,096 bytes apart — **every access is on the next page**, and a page is revisited only after 511 others. **An 8-entry TLB evicted it long before**: every access misses.

### (c) [4]

Reference, `TLBSIZE` changed and rebuilt:

| `TLBSIZE` | Column-order matrix | 1,024 random pages |
|---:|---:|---:|
| 64 | 0.00% | 6.14% |
| 256 | 0.00% | 24.83% |
| **511** | **0.00%** | 49.76% |
| **512** | **99.80%** | 49.83% |
| 513 | 99.80% | 49.95% |

**[2]** for the table. **The cliff [2]:** column order cycles through the same **512 pages in the same order**. With 512 entries all of them stay cached after the first column. **With 511, the least recently used page is always exactly the next one needed** — each access evicts its successor — so **every access misses**. Random access has no cliff; its hit rate is TLBSIZE/1,024 throughout. **Relating to L17 §2**: a working set just larger than the TLB can behave like no TLB at all if it is accessed in a cycle; this CPU's STLB holds 1,536 entries, so the cliff for 4 KiB pages is at **6 MiB** of cyclically accessed memory.

---

## Q4: Stale Translations (15 points)

### (a) [5]

```
with shootdown:
uread   00001234 -> 00009234
uwrite  00001234 -> 00009234
stats   page-table frames 2 (8 KiB)   cpu 0 TLB 0 hits, 2 misses (0.00% hits)   cpu 1 TLB 1 hits, 2 misses (33.33% hits)

--no-shootdown:
uread   00001234 -> 00005234
uwrite  00001234 -> 00005234
stats   page-table frames 2 (8 KiB)   cpu 0 TLB 0 hits, 2 misses (0.00% hits)   cpu 1 TLB 2 hits, 1 misses (66.67% hits)
```

### (b) [5]

**CPU 1 wrote to frame `0x5000`** — the frame the page was mapped to before `unmap`. **[2]**

**Why it is serious [3]:** after `unmap`, the kernel **frees `0x5000` and may give it to anyone** — another process, a page-cache page of some file, a page table, the kernel's own data. **A stale TLB entry lets this process read and write memory it no longer owns**: an isolation failure, exploitable, and silent. **Accept** any answer that names reuse of the frame.

### (c) [5]

A trace such as:

```
map    00001000 00005000 wu
cpu    1
uread  00001234
flush                                 # CPU 1 switches to another process
cpu    0
unmap  00001000
map    00001000 00009000 wu
cpu    1                              # and later switches back
uread  00001234
stats
```

Reference with `--no-shootdown`:

```
uread   00001234 -> 00009234
stats   page-table frames 2 (8 KiB)   cpu 1 TLB 0 hits, 2 misses (0.00% hits)
```

**[2]** for a trace in which CPU 1 caches, flushes, and then translates correctly.

**The guarantee [2]:** **a CPU that is not running the address space when it changes must not use any translation cached before the change** — its TLB must be flushed, or the entries proven current, **before it next runs the process**. Without PCIDs, switching back loads `CR3` and flushes: free. **With PCIDs [1]**, switching back would keep the old entries, so **Linux records a per-address-space generation number that increments on every flush-requiring change**; a CPU switching in compares the generation it last saw and **flushes that PCID if it is stale**. **Accept** "a counter checked on switch-in" or equivalent.

---

## Q5: Superpages (15 points)

### Reference `map_big`, and the `translate` changes

```c
static int map_big(uint32_t va, uint32_t pa, uint32_t perm)
{
    uint32_t *pde = entry(pgdir, PDX(va));
    if (*pde & PTE_P) return -1;
    *pde = BIG_ADDR(pa) | perm | PTE_P | PTE_PS;
    return 0;
}
```

In `translate`: the TLB match compares `va >> 22` for entries with `big` set; on a miss, a directory entry with `PTE_PS` **is** the translation, cached with `big = 1, vpn = va >> 22`; the physical address is `BIG_ADDR(pte) | (va & 0x3FFFFF)`.

### (a) [8]

**Exact reproduction of both `basic.txt` and `big.txt`: 8.** A submission that breaks `basic.txt` while adding superpages: **at most 4**. **The common bug**: matching a superpage TLB entry with `va >> 12`, which gives `matrix … column` 512 misses (one per 4 KiB page) instead of none — deduct 3.

### (b) [4]

- **1 frame [2]** — just the directory, against Q2(a)'s **65**. The 64 directory entries are the translations; **no page tables exist at all.** This is **why xv6's boot page directory `entrypgdir` uses `PTE_PS`**: it can map the kernel before any allocator exists, with a static array.
- **100% hits [2]** — against Q3's 0.00% for the same access pattern. **The whole 2 MiB matrix lies in one 4 MiB superpage, so it used one TLB entry.** Not even one miss, because **`uwrite 103fffff` before `reset` had already cached that superpage**, and `reset` does not empty the TLB. **Accept "one entry"; the zero needs the `reset` explanation for full marks.**

### (c) [3]

Any two, **at least one tied to L17 §4 or L18 §6 [1.5 each]**:

- **Memory bloat and internal fragmentation**: a 4 KiB allocation commits 4 MiB (or 2 MiB on x86-64). L17 §4.
- **Contiguous frames are scarce**: a superpage needs 1,024 (x86-64 huge page: 512) contiguous free frames; the buddy allocator fragments and **16 of 105 4 MiB blocks did not come back** in L18 §6. xv6's free list has no notion of contiguity at all.
- **Copy-on-write and paging out work per page**: a write to a shared superpage would copy 4 MiB, and evicting one would write 4 MiB; the kernel must split it first.
- **Permissions are per page**: xv6's guard page needs `PTE_U` cleared on one 4 KiB page; text read-only and data writable need different entries.
- **For xv6 specifically**: its kernel mapping sits in every process (Q2(a)), and `kalloc` hands out 4 KiB frames from the same range — a superpage mapping would still work, and xv6 simply chose one mechanism for simplicity. **Accept** this as a reason for xv6 only if the student names simplicity explicitly.

---

*CS 202 · Week 5 · PS 5 Solutions · Instructor Only*
