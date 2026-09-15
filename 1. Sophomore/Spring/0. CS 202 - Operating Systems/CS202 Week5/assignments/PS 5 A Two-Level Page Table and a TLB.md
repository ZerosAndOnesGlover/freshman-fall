# CS 202 · Problem Set 5
## A Two-Level Page Table, and a TLB

---

**Released:** Week 5, Wednesday · **Due:** Week 6, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS5_{LastName}_{StudentID}.pdf`, plus your `pt2.c` and any traces you wrote in a tarball `PS5_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine and encouraged. The write-up and the code must be
> yours. State at the top: *"I worked on this problem set independently"* or name who you discussed
> which question with.
>
> **Your `pt2.c` must reproduce every expected output below exactly**, and compile clean under
> `gcc -O2 -Wall -Wextra`.

**Files provided** in `assignments/ps5/`:

| File | Yours to write | Provided |
|---|---|---|
| `pt2.c` | `walk`, `map`, `unmap`, `tlb_invalidate`, `translate` (Q1); `map_big` and the superpage cases (Q5) | simulated physical frames (`palloc`, `pfree`, `entry`), the TLB's storage, and the command driver |
| `traces/*.txt` | — | `basic`, `kernel`, `sparse`, `tlb`, `stale`, `big` |

**The simulator is xv6's page table** (L16 §4) with the hardware's half added. Addresses are 32-bit and split 10/10/12. **The page directory and every page table live in simulated physical frames**: an entry holds a *physical* address, and `entry(pa, i)` gives you entry *i* of the table in the frame at `pa`. The driver's commands are described at the top of `pt2.c`; read them first.

---

### Q1: The Page Table and the TLB (30 points)

Implement the five functions. **To match the expected output, follow these rules exactly:**

- **`walk`** allocates a missing page table with `palloc()` (it comes zeroed) and gives its directory entry `PTE_P | PTE_W | PTE_U`, as xv6 does.
- **`map`** returns −1 if the page is already present. **`unmap`** returns −1 if it was not; otherwise it clears the entry, **invalidates the page in every CPU's TLB** (only the current CPU's when `shootdown` is 0), and **if that page table now has no present entry, frees its frame and clears the directory entry**, returning 1.
- **`translate`** first searches **the current CPU's TLB**. **On a hit**: count it in `hits[cpu]`, set the entry's `used` to `++now`, and use the cached entry. **On a miss**: count it in `misses[cpu]` and walk **without allocating**. If the page is not present, return `NOTPRESENT` **without caching anything**. Otherwise cache the entry — in an invalid slot if there is one, else in place of the slot with the smallest `used` — with `used = ++now`.
- **Then check permissions**, from the entry whether it came from the TLB or the walk: a write to an entry without `PTE_W` is `NOTWRITABLE`; otherwise a user access to an entry without `PTE_U` is `NOTUSER`. Otherwise set `*pa` and return `OK`.

**(a) [20]** Reproduce:

```
$ ./pt2 < traces/basic.txt
map     00400000 -> 00123000
map     00401000 -> 00124000
map     80000000 -> 00001000
map     00401000 -> 00200000  ERROR already mapped
read    00400abc -> 00123abc
uread   00400abc -> 00123abc
uwrite  00400abc    FAULT not writable
uwrite  00401ff0 -> 00124ff0
uread   80000010    FAULT not user
read    80000010 -> 00001010
read    00402000    FAULT not present
read    c0000000    FAULT not present
stats   page-table frames 3 (12 KiB)   cpu 0 TLB 3 hits, 5 misses (37.50% hits)
unmap   00400000
unmap   00401000  (page table freed)
unmap   00401000  ERROR not mapped
read    00401ff0    FAULT not present
stats   page-table frames 2 (8 KiB)   cpu 0 TLB 3 hits, 6 misses (33.33% hits)
```

**(b) [6]** **Which three accesses were TLB hits?** One of them faulted: **why does a faulting access count as a hit**, and why is it correct to check permissions on a hit at all? Why did the last `read` miss, when `00401ff0` had been translated before?

**(c) [4]** Your `translate` does not cache "not present". **Construct a sequence of commands** that would give a wrong answer if it did, and say what the real hardware does instead.

---

### Q2: What the Tables Cost (20 points)

**(a) [8]** `traces/kernel.txt` maps what xv6's `setupkvm` maps into every process (L16 §4's `kmap[]`). **Run it and report the frames.** Derive the number from `memlayout.h` without the simulator, and **reconcile it with L16 §5's measured fork of 1,096 pages.**

**(b) [6]** `traces/sparse.txt` maps one page in every 4 MiB below `KERNBASE`, then unmaps every second one. **Report both `stats` lines and explain each number.** Then answer: for **512 mapped pages**, what are the fewest and the most frames the tables can need? **For what layout does a two-level table need more memory than a flat 4 MiB one**, and by how much at worst?

**(c) [6]** L16 §7 measured x86-64's four-level tables in Linux: **touching 1 GiB added 2,052 kB**, and **64 pages 1 GiB apart added 512 kB**. **Derive both numbers** from the four-level layout, stating which levels needed new pages. **If the 64 pages had been 2 MiB apart instead, how much would they have added?**

---

### Q3: How Well an 8-Entry TLB Does (20 points)

**(a) [8]** Run `traces/tlb.txt`. It maps 1,024 user pages and runs nine access patterns, resetting the counters between them. **Tabulate the pattern and the hit rate.**

**(b) [8]** **Explain every hit rate from the pattern**, with arithmetic where there is some to do. In particular: why is **16 random pages** almost exactly half, and what does **64 random pages** come close to? **Why does column order over the 512 × 512 matrix get no hits at all**, when row order over the same memory gets 99.80%?

**(c) [4]** Change `TLBSIZE` to **64, 256, 511, 512 and 513**, and run the column-order matrix and the 1,024-random-pages pattern with each. **Report the hit rates.** One size is a cliff: **explain exactly why a TLB one entry smaller does so badly**, and relate it to the second-level TLB sizes in L17 §2.

---

### Q4: Stale Translations (15 points)

**(a) [5]** Run `traces/stale.txt` as it is, and with `--no-shootdown`. **Report the last three lines of each.**

**(b) [5]** Without shootdown, **CPU 1's `uwrite` succeeded. Which frame did it write to**, and why is that a serious bug in a real kernel — not merely a wrong number? *(Where might frame `0x5000` be now?)*

**(c) [5]** L17 §6 measured that **Linux sends no shootdown to a CPU where the process is asleep.** Using `flush` — a switch to another address space on a CPU without PCIDs — **write a trace in which CPU 1 has cached the translation, and invalidating only CPU 0 is nevertheless safe.** Run it with `--no-shootdown`, report it, and **state the guarantee the kernel must provide** for CPU 1 when it next runs the process. With PCIDs, the TLB is not flushed on a switch: **what must Linux do instead?**

---

### Q5: Superpages (15 points)

x86 lets a directory entry map **4 MiB directly**: with `PTE_PS` set, the entry's top 10 bits are the start of 4 MiB of frames, and there is no page table. **xv6 uses one** before paging is fully set up: find it in `main.c`.

Implement **`map_big`** — return −1 if the directory entry is already present, otherwise set it to the 4 MiB-aligned `pa | perm | PTE_P | PTE_PS` — and extend the rest:

- **`walk`** returns 0 for an address in a superpage, so **`map`** of a 4 KiB page inside one returns −1.
- **`unmap`** returns **−2** for an address in a superpage.
- **`translate`**, on a miss, treats a superpage's directory entry as the translation and caches it with **`big = 1` and `vpn = va >> 22`**; a TLB entry with `big` set matches any address in its 4 MiB. The physical address keeps the low **22** bits of `va`.

**(a) [8]** **Your program must still reproduce Q1(a) exactly**, and must reproduce:

```
$ ./pt2 < traces/big.txt | grep -v '^mapbig  [8f]'
stats   page-table frames 1 (4 KiB)
read    80123456 -> 00123456
uread   80123456    FAULT not user
map     80400000 -> 00001000  ERROR already mapped
unmap   80400000  ERROR in a superpage
mapbig  10000000 -> 00c00000
mapbig  10123000 -> 01000000  ERROR already mapped
uwrite  103fffff -> 00ffffff
reset
matrix  10000000  512 x 512, column order: 262144 accesses, 0 faults
stats   page-table frames 1 (4 KiB)   cpu 0 TLB 262144 hits, 0 misses (100.00% hits)
```

**(b) [4]** **Explain the two `stats` lines** against Q2(a)'s and Q3's. The column-order matrix got no misses at all: **how many TLB entries did it use?**

**(c) [3]** If superpages remove both the table memory and the TLB misses, **why does xv6 map the kernel with 4 KiB pages once it is running, and why does Linux not give every process 2 MiB pages?** Give two distinct reasons, at least one from L17 §4 or L18 §6.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | The page table and the TLB | 30 |
| 2 | What the tables cost | 20 |
| 3 | How well an 8-entry TLB does | 20 |
| 4 | Stale translations | 15 |
| 5 | Superpages | 15 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem set of the term is dropped.**

---

*CS 202 · Week 5 · PS 5 · © CSE Department*
