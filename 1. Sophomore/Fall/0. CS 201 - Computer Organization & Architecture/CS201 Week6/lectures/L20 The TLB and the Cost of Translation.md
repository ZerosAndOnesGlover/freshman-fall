# CS 201 · Computer Organization & Architecture
## Week 6 · Lecture 2 of 3
### The TLB and the Cost of Translation

---

**Reading:** CS:APP §9.6.2–9.6.4 · **Previous:** L19, virtual memory and the page table

---

## 1. A Cache for Translations

L19 left a problem: every memory access needs four table reads first. **The fix is the same one Week 4 used for data — cache the results.**

The **Translation Lookaside Buffer** holds recent virtual-page → physical-frame mappings. It is small, fully or highly associative, and **it is checked in parallel with the L1 cache access**, so a hit costs nothing measurable.

Typical scale on a machine like this one:

| | Entries | Reach at 4 KiB |
|---|---:|---:|
| L1 dTLB | ~64 | **256 KiB** |
| L2 (shared) TLB | ~1536 | **6 MiB** |

**"Reach" is the number that matters: entries × page size.** A 64-entry L1 dTLB covers 256 KiB of address space **no matter how large your caches are.** You can have data sitting in a 32 KiB L1 cache and still miss the TLB on every access to it — because the two structures index different things.

---

## 2. Isolating the Cost

That claim is testable, and the test is the cleanest thing in this week.

**Keep the cache footprint identical and vary only the number of pages it is spread across.**

512 pointers in a random chase — always **512 cache lines = 32 KiB**, which fits this machine's L1d exactly. The only variable is the stride between them, which sets how many pages those 512 lines occupy:

| stride | cache lines | **pages spanned** | ns/access |
|---:|---:|---:|---:|
| 64 B | 512 | **8** | **1.24** |
| 256 B | 512 | 32 | 4.28 |
| 1 KiB | 512 | 128 | 12.68 |
| 4 KiB | 512 | 512 | 14.57 |
| 16 KiB | 512 | 2048 | 15.77 |
| 64 KiB | 512 | **8192** | **27.57** |

*(All measured, `MADV_NOHUGEPAGE` to keep the page size fixed at 4 KiB.)*

**Every row touches the same 32 KiB of cache lines. The data is L1-resident throughout. The access cost still rises 22×.**

**Read the first row against Week 4.** 1.24 ns is the L1 latency Week 4 measured as 1.22 ns — the same number, arrived at independently. At 8 pages, translation is free.

**Then the second row.** 32 pages, and the cost has already tripled. **The L1 dTLB is around 64 entries**, so 32 pages of working set plus the stack, code and page-table pages is enough to start evicting translations. By 128 pages the L1 dTLB is hopeless and every access is going to the L2 TLB or walking the table.

> **This is the lecture's central fact: your data can be entirely in L1 cache and still be slow,
> because translation is a separate lookup with a separate capacity.** Week 4 taught you to count
> cache lines. **You must also count pages.**

---

## 3. Why Huge Pages Exist

The reach problem has an obvious fix: **make the pages bigger.**

x86-64 supports 2 MiB and 1 GiB pages, and a huge page needs no fourth-level table — the PMD entry points straight at a 2 MiB frame. **Same 64 TLB entries, 512× the reach:**

$$64 \times 2\text{ MiB} = 128\text{ MiB} \quad\text{instead of}\quad 64 \times 4\text{ KiB} = 256\text{ KiB}$$

On Linux, transparent huge pages do this automatically:

```
$ cat /sys/kernel/mm/transparent_hugepage/enabled
always [madvise] never
```

*(Verified — this machine is set to `madvise`, so a program must ask via `madvise(p, n, MADV_HUGEPAGE)`.)*

### And a measurement that found nothing

Running the same random pointer chase over 1 MiB to 1 GiB, with and without `MADV_HUGEPAGE`:

| region | 4 KiB pages | huge pages | ratio |
|---:|---:|---:|---:|
| 1 MiB | 14.79 ns | 13.90 ns | 1.06× |
| 16 MiB | 112.93 ns | 112.65 ns | 1.00× |
| 256 MiB | 143.60 ns | 139.81 ns | 1.03× |
| 1 GiB | 162.72 ns | 152.99 ns | 1.06× |

*(Measured.)* **Essentially no benefit at any size.**

**Why, and this is the useful part.** In that benchmark there is one pointer per 4 KiB page, so **every access is both a TLB miss and a cache miss.** The cache miss costs ~130 ns of DRAM latency; the TLB miss is overlapped with it and largely hidden. **Fixing translation does not help when you are waiting for data anyway.**

**The §2 experiment isolates the TLB precisely because it removes the cache misses.** Same principle as Week 4's control at $N = 512$: an intervention only shows up when its bottleneck is the one that binds.

> **Do not conclude that huge pages are useless.** Conclude that they help programs that are
> **TLB-bound and not memory-bound** — large in-memory hash tables, databases with big resident
> working sets, JVM heaps. Those are real and the gains are large. **This benchmark simply was not
> one of them**, and finding that out took one measurement.

---

## 4. What a TLB Miss Costs

A miss is not a fault. The hardware walks the page table itself, in a few tens of cycles if the table pages are in cache — and the page-table pages are ordinary memory, so **they compete for the same cache you are using for data.**

| Event | Cost |
|---|---|
| TLB hit | ~0 — overlapped with the L1 access |
| TLB miss, tables cached | tens of cycles |
| TLB miss, tables not cached | up to 4 DRAM accesses |
| **Page fault** | **~6000 cycles** — L21 measures it |

**Three orders of magnitude across that table.** "Address translation" is not one cost.

---

## 5. Context Switches Are Expensive Here

`cr3` changes on a context switch, so **every translation in the TLB becomes invalid.** A naive design flushes the whole TLB, and the new process starts cold — hundreds of misses before it is running at speed. This is a large part of what makes context switches cost more than the register saving suggests.

**ASIDs** (address space identifiers) tag each entry with its owning process, so entries survive a switch and only the right ones are used. Modern x86-64 calls this PCID.

**On multi-core there is a worse problem.** If one core changes a page table entry, other cores may hold stale copies. There is no hardware coherence for TLBs — so the OS must send an **inter-processor interrupt** to every core that might be affected and wait for each to invalidate. **This is a TLB shootdown**, and it is one of the most expensive operations in a kernel. Week 10 revisits it as the coherence problem it is.

---

## 6. What This Means for Your Code

| Do | Why |
|---|---|
| **Count pages, not just cache lines** | 32 KiB in 8 pages is 1.24 ns; the same 32 KiB in 8192 pages is 27.57 ns |
| Keep hot data contiguous | Fewer pages, fewer translations, and prefetching works |
| Consider huge pages for large working sets | Only if you are **TLB-bound**, not memory-bound |
| Avoid pointer-chasing structures over huge ranges | Worst case for both TLB and cache |
| Do not scatter small allocations | Each `malloc` in a fresh page costs a TLB entry |

**And measure before acting**, because §3 is exactly the case where the obvious fix did nothing.

---

## 7. What to Take Away

1. **The TLB caches translations**; a hit is free, and it is checked in parallel with L1.
2. **Reach = entries × page size.** ~64 entries at 4 KiB is 256 KiB — small.
3. **Same 32 KiB of L1-resident data, 8 pages against 8192 pages: 1.24 ns against 27.57 ns.** Translation is a separate capacity.
4. **Huge pages multiply reach by 512×**, and this machine needs `madvise` to use them.
5. **Huge pages did nothing for a DRAM-bound chase** — because the TLB was not the bottleneck.
6. **A TLB miss costs tens of cycles; a page fault costs thousands.** Different events.
7. **TLB shootdowns are inter-processor interrupts**, and they are expensive.

---

## Exercises

1. Compute TLB reach for 64 entries at 4 KiB, 2 MiB and 1 GiB. Which is enough to cover a 4 GiB in-memory database?
2. In §2, the cost triples between 8 and 32 pages while the cache footprint is unchanged. What does that tell you about the L1 dTLB's capacity? Give a range.
3. The §3 benchmark showed no huge-page benefit. Design a benchmark that **would** show one, and say what you changed and why.
4. A page-table walk reads four tables, and those reads go through the data cache. What happens to your program's cache hit rate when it starts missing the TLB heavily?
5. Explain why TLBs have no hardware coherence protocol when caches do. What would it cost to add one?
6. A process with a 64-entry TLB is context-switched every 1 ms. Estimate the cost of a cold TLB per switch, stating your assumptions, and say what PCIDs save.

---

*Next: L21 — pages that are not there yet, and pages shared until someone writes.*
