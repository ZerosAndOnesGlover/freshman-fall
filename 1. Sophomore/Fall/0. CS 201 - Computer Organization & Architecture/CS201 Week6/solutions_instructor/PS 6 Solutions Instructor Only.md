# CS 201 · Problem Set 6 — Solutions
## Instructor Only

---

> **Not for distribution.** All measurements from the lab image (i5-8250U, 4 KiB pages, GCC 13.3.0).

---

## Q1 (18) — Translation by Hand

### (a) [4]

| Field | Bits | Width |
|---|---|---|
| PGD | 47–39 | 9 |
| PUD | 38–30 | 9 |
| PMD | 29–21 | 9 |
| PTE | 20–12 | 9 |
| offset | 11–0 | 12 |

$9 + 9 + 9 + 9 + 12 = \mathbf{48}$ ✓

### (b) [4]

`0x00007f3c2a4b1000`:

| | value |
|---|---:|
| **PGD** | **254** (`0x0fe`) |
| **PUD** | **240** (`0x0f0`) |
| **PMD** | **338** (`0x152`) |
| **PTE** | **177** (`0x0b1`) |
| **offset** | **0** |

*(Verified — reconstructing $(254 \ll 39) \,|\, (240 \ll 30) \,|\, (338 \ll 21) \,|\, (177 \ll 12)$ gives `0x7f3c2a4b1000` exactly.)*

> **Award the marks for the shift-and-mask method**, not the arithmetic. A student who shows
> `(va >> 30) & 0x1FF` for PUD and slips a digit keeps 3 of 4.

### (c) [4]

$512 \times 8 = 4096$ bytes $=$ **one page** ✓

**It is a design goal**: the page allocator that hands out data pages can hand out page-table pages with no special case, a table never straddles a page boundary, and the index width falls out as $\log_2(4096/8) = 9$. **The 9-bit index is a consequence of the page size and the entry size, not an independent choice.**

### (d) [3]

**4 KiB pages:** $2^{36}$ entries $\times$ 8 bytes $= 2^{39} = \mathbf{512 \text{ GB}}$ per process.
**2 MiB pages:** $2^{27}$ entries $\times$ 8 bytes $= 2^{30} = \mathbf{1 \text{ GB}}$.

**Still absurd**, which is the point: **huge pages shrink the table but do not make a flat one viable.** The tree is doing the real work; huge pages additionally remove one level and multiply TLB reach.

### (e) [3]

Touching 4 MB $= 1024$ pages, which is at most 1024 PTE-level entries. Since one table covers 512 entries:

| Level | Pages needed |
|---|---|
| PGD | 1 |
| PUD | 1–2 |
| PMD | 1–2 |
| PTE | **2–1024**, depending on scatter |

**Contiguous 4 MB:** roughly **2 PTE tables + 1 each above = ~5 pages ≈ 20 KiB** to map 100 GB of address space.

**The tree wins because the 100 GB that is never touched costs nothing** — untouched subtrees are simply absent.

---

## Q2 (14) — The PTE and Its Bits

### (a) [4] — 0.67 each

| Bit | Purpose |
|---|---|
| **P** | Present in physical memory. 0 ⇒ page fault |
| **R/W** | Writable. 0 ⇒ write faults |
| **U/S** | User-accessible, or supervisor only |
| **A** | Accessed — set by hardware on any reference |
| **D** | Dirty — set by hardware on a write |
| **NX** | No-execute |

### (b) [3]

**A** tells the OS the page has been used since it was last cleared — the input to **Clock/second-chance replacement**. **D** tells it whether an evicted page must be written back or can simply be dropped.

**Minimal because the hardware sets these on every access**, in the critical path of every memory operation. **A counter or timestamp would cost time and bits on the hot path**; one bit each is what can be afforded. Replacement algorithms are shaped around that constraint — which is exactly why Clock exists rather than true LRU.

### (c) [4]

**[2]** Both cases fault identically: the PTE is read-only and a write was attempted. **The hardware cannot distinguish them** — the PTE has no "this is COW" bit.

**[2] The distinction lives in the kernel's own mapping metadata** — the VMA (`vm_area_struct`) describing that region, which records the *logical* permissions. The handler consults it:

- VMA says the region is **read-only** ⇒ a genuine protection violation ⇒ `SIGSEGV`.
- VMA says **writable** but the PTE says read-only ⇒ **copy-on-write** ⇒ copy the frame, mark it writable, resume.

> **This is the marked insight**: the PTE describes what the hardware may do; the VMA describes what
> the program is allowed to do. **COW lives in the gap between them.**

### (d) [3]

The **NX bit** in each page table entry, applied **per page**.

`GNU_STACK` in the ELF header is a *request*; the loader reads it and maps the stack region with or without execute permission, which becomes the NX bit in every PTE covering that region. **One missing directive in one `.asm` file changed the flag for the whole linked binary**, because the linker takes the most permissive setting across all inputs.

---

## Q3 (38) — Build the Simulator

### (a) [12]

Marking:

- **6** — correct four-level walk with sparse allocation; only tables actually needed exist.
- **3** — correct per-level page-table page counts.
- **3** — peak resident frames reported.

> **The common bug is allocating all 512 entries eagerly at every level**, which works and defeats the
> exercise. Check that a trace touching two distant addresses allocates ~8 tables, not 2048.

### (b) [8]

**5** for a working fully associative LRU TLB with correct hit/miss accounting; **3** for the sweep and a *stated* knee.

**Expected shape:** hit rate rises steeply then flattens once the TLB covers the trace's working set in pages. **Require the student to relate the knee to the trace**, not merely to report it.

### (c) [10]

**5** FIFO, **5** Clock. **Clock must use a simulated A bit** — set on access, cleared by the hand as it sweeps, evicting the first entry it finds already clear.

> **Reject any "Clock" implemented with timestamps.** That is LRU wearing a hat, and it misses the
> entire point of §L21 §5: the algorithm is shaped by the hardware providing exactly one bit.

Fault counts should fall monotonically for Clock as `M` rises. **FIFO need not** — see (d).

### (d) [4]

**[2]** Classic reference string:

$$1,2,3,4,1,2,5,1,2,3,4,5$$

*(Verified:)*

| | 3 frames | 4 frames |
|---|---:|---:|
| **FIFO** | **9 faults** | **10 faults** |
| LRU | 10 faults | 8 faults |

**FIFO produces more faults with more frames.** The mechanism: FIFO evicts by arrival order, ignoring use. Adding a frame changes *which* pages are resident in a way that can systematically evict a page just before it is needed again.

**[2] LRU cannot.** It is a **stack algorithm**: the set of pages resident with $n$ frames is always a **subset** of the set resident with $n+1$ frames, for any reference string. So any hit with $n$ frames is a hit with $n+1$, and faults are monotonically non-increasing.

### (e) [4]

**2** for producing both traces and running them; **2** for a specific, correct account of the disagreement.

**Expected disagreement:** the simulator will report a poor TLB hit rate for the random trace and will *overstate* the cost, because it models neither

- **hardware prefetching** (which hides sequential-access latency entirely — Week 4 measured 83× from this), nor
- **the page-table walk being cached** (a TLB miss whose tables are in L1 costs tens of cycles, not a full walk), nor
- **out-of-order overlap** of independent misses.

> **Full marks require naming at least two of those.** "It's just a simulation" scores 1.

---

## Q4 (16) — Demand Paging, Measured

### (a) [4]

```
start                      RSS=  1444 KiB  minor faults=74
after malloc(512 MiB)      RSS=  1580 KiB  minor faults=86
after touching every page  RSS=525864 KiB  minor faults=131157
```

*(Verified.)* $512 \text{ MiB}/4096 = 131\,072$ pages; faults rose by $131\,157 - 86 = \mathbf{131\,071}$. **One per page, to within one.**

### (b) [4]

$1967 - 19 = \mathbf{1948 \text{ ns} \approx 6200 \text{ cycles}}$ at 3.2 GHz. *(Verified; a repeat gave 1887 ns.)*

$$\frac{6200}{438} \approx \mathbf{14 \text{ DRAM accesses}} \qquad \frac{6200}{4} \approx \mathbf{1550 \text{ L1 hits}}$$

### (c) [4]

```
fork() itself took   0.0043 s for a 256 MiB address space
child at birth:      minor faults=14
child after writing: +65536 faults
```

*(Verified.)* $256 \text{ MiB}/4096 = 65\,536$ — **exactly one COW fault per page.**

### (d) [4]

**[2]** At a memcpy bandwidth of roughly 10 GB/s, copying 256 MiB $\approx$ **25–50 ms**, depending on whether it is read+write bandwidth. Accept any measured figure with the method shown.

**[2]** `fork` took **4.3 ms** — an order of magnitude less. **It spent that time duplicating page tables and marking pages read-only, not copying data.** For a 256 MiB region that is ~65 536 PTEs across ~128 PTE-level tables plus the levels above.

---

## Q5 (14) — Translation Is a Separate Cost

### (a) [6]

| stride | pages | ns/access |
|---:|---:|---:|
| 64 B | 8 | **1.24** |
| 256 B | 32 | 4.28 |
| 1 KiB | 128 | 12.68 |
| 4 KiB | 512 | 14.57 |
| 16 KiB | 2048 | 15.77 |
| 64 KiB | 8192 | **27.57** |

*(Verified.)*

### (b) [4]

**[2]** The cache footprint is **32 KiB of lines in every row** — L1-resident throughout, and row 1's 1.24 ns matches Week 4's measured L1 latency of 1.22 ns. **The 22× is entirely address translation**: as the same data spreads across more pages, the TLB can no longer hold the mappings and each access requires an L2 TLB lookup or a page walk.

**[2] L1 dTLB estimate: on the order of 64 entries.** The cost triples between 8 and 32 pages, so the structure is already under pressure at ~32 mappings once the stack, code and page-table pages are counted. **Accept 32–128 with reasoning**; reject a bare number.

### (c) [4]

**[1]** No benefit: ratios **1.00×–1.06×** from 1 MiB to 1 GiB. *(Verified.)*

**[2] Why.** That benchmark places **one pointer per 4 KiB page**, so every access is *both* a TLB miss **and** a cache miss. The ~130 ns of DRAM latency dominates and the translation cost is overlapped with it. **Huge pages fix translation, and translation was not the bottleneck.**

**[1] A benchmark that would show it:** keep the data **cache-resident** while spanning many pages — which is precisely (a)'s design. Repeat (a) with `MADV_HUGEPAGE`: 512 lines across 8192 4 KiB pages become 512 lines across ~16 huge pages, and the TLB holds all of them.

> **This is the week's methodological point, and it is the same one as Week 4 §5.3 and Week 5 §L18
> §3: an intervention only shows up when its bottleneck is the one that binds.** A student who
> reports the null result and explains it correctly has understood the course better than one who
> found a speedup.

---

## Mark Summary

| | |
|---|---:|
| Q1 | 18 |
| Q2 | 14 |
| Q3 | 38 |
| Q4 | 16 |
| Q5 | 14 |
| **Total** | **100** |

**Where the class loses marks, in order:**

1. **Q3(c)** — implementing Clock with timestamps instead of an A bit.
2. **Q2(c)** — looking for the COW distinction in the PTE, where it is not.
3. **Q5(c)** — concluding huge pages are useless rather than misapplied.
4. **Q3(a)** — eager table allocation, which defeats the sparse-tree exercise.
5. **Q3(d)** — asserting LRU is stack-monotone without the subset argument.

---

*CS 201 · Week 6 · PS 6 Solutions · Instructor Only*
