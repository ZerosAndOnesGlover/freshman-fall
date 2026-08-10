# CS 201 · Computer Organization & Architecture
## Week 7 · Lecture 1 of 3
### The I/O Path — Controllers, Interrupts and DMA

---

**Reading:** CS:APP §6.1.2–6.1.5, §10.1–10.5 · **Previous:** L21, demand paging and COW

---

## 1. Where This Week Sits

Week 6 ended with a cost table that stopped at the minor page fault. **This week supplies the bottom.**

| Event | Cost | Measured |
|---|---:|---|
| L1 cache hit | 4 cycles ≈ 1.2 ns | Week 4 |
| DRAM access | 438 cycles ≈ 137 ns | Week 4 |
| Minor page fault | ~6200 cycles ≈ 1.9 μs | Week 6 |
| **Page-cache hit** | **2.5 μs** | **this week** |
| **SSD 4 KiB read** | **~80–160 μs** | **this week** |
| **`fsync`** | **~3.9 ms** | **this week** |
| HDD seek + rotation | ~5–10 ms | *cited — no spinning disk here* |

**Nine orders of magnitude from the top row to the bottom.** Every design decision in storage follows from that spread.

> **A note on honesty.** The lab machine has an NVMe SSD and **no rotating disk**, so every SSD figure
> in this week is measured and every HDD figure is cited from manufacturer specifications. **Where a
> number is not measured, it says so.**

---

## 2. The Device Is Another Computer

A modern storage device is not a passive lump. **An NVMe SSD has its own multi-core processor, its own DRAM, and firmware larger than early operating systems.** The CPU does not talk to flash; it talks to a controller that talks to flash.

The interface is the same one Week 6 used for memory: **memory-mapped registers.** The controller's control and status registers appear at physical addresses, and the driver reads and writes them with ordinary `mov` instructions. There is no special I/O instruction involved on this path.

```
  CPU  ──── memory bus ────  DRAM
   │
   └──── PCIe ────  NVMe controller ──── flash chips
                     (own CPU + DRAM)
```

**This machine:**

```
$ lsblk -d -o NAME,SIZE,ROTA,TYPE,MODEL
nvme0n1 238.5G    0 disk SAMSUNG MZVLB256HAHQ-000H1
```

*(Verified.* `ROTA 0` *means non-rotational.)*

---

## 3. Three Ways to Wait

The CPU issues a request that will take microseconds or milliseconds. **What does it do meanwhile?**

### Polling

```c
while (!(read_status_register() & READY)) { /* spin */ }
```

**Simple, and it burns a core.** At 3.2 GHz, waiting 100 μs for an SSD spins about **320 000 cycles** doing nothing.

**But it is not always wrong.** When the wait is shorter than the cost of a context switch — a few microseconds — polling wins, because sleeping and waking costs more than the wait. **Modern NVMe drivers poll for very low-latency devices**, which is a reversal of decades of received wisdom, driven entirely by devices getting fast enough to make interrupts the expensive part.

### Interrupts

The device raises a signal when it finishes; the CPU runs other work meanwhile and is diverted into a handler.

**The cost is the diversion itself:** save state, enter the kernel, run the handler, restore, return — and, from Week 6, **the TLB and caches are now polluted with the handler's data.** A few microseconds, which is fine at 10 ms and expensive at 80 μs.

**At very high rates interrupts become pathological.** A device delivering a million completions per second would spend the CPU entirely in interrupt handlers — the **receive livelock** problem. The fix is **interrupt coalescing**: the device batches completions and interrupts once per batch, trading latency for throughput.

### DMA

**Direct Memory Access** is the important one. The controller writes to memory *itself*, without the CPU copying anything.

1. The driver builds a descriptor: source, destination **physical** address, length.
2. It hands the descriptor to the controller and returns.
3. The controller transfers directly to and from DRAM.
4. It raises one interrupt when the whole transfer is done.

**Without DMA the CPU would copy every byte** — at 2 GB/s that is a core fully occupied moving data it is not using.

> **DMA is why Week 6 matters here.** The device knows nothing about page tables; it uses **physical**
> addresses. So the kernel must pin the pages — mark them unswappable — for the duration, translate
> the buffer's virtual address itself, and handle the case where a "contiguous" user buffer is
> scattered across unrelated physical frames. **That last problem is what scatter-gather lists
> solve**, and it exists purely because virtual memory made contiguity a fiction.

---

## 4. The Block Device Abstraction

Underneath, storage devices differ wildly. Above, they all look the same:

> **An array of numbered, fixed-size blocks that can be read or written in any order.**

The block is traditionally 512 bytes and is now usually 4096 to match the page size.

**This abstraction is why a filesystem does not care what it is running on**, and it is imposed by the device: an SSD is internally nothing like an array of blocks — it is pages, erase blocks and a translation layer (L23) — but it presents this interface because forty years of software expects it.

**The abstraction leaks, and knowing where is the whole of L24.** Random access is not the same cost as sequential, even on a device with no moving parts.

---

## 5. The Page Cache

Every read and write passes through the kernel's **page cache** — the same pages Week 6 described, backed by files rather than swap.

**Reads:** check the cache; on a miss, issue I/O and cache the result.
**Writes:** update the cached page, mark it dirty, return. **The data is not on the device yet.**

### What that is worth

Random 4 KiB reads, buffered against `O_DIRECT` (which bypasses the cache entirely):

```
buffered, cached 4K random :   398063 IOPS     2.51 us/op   1554.9 MiB/s
O_DIRECT 4K random (device):     6345 IOPS   157.60 us/op     24.8 MiB/s
page cache is 63x faster
```

*(Measured.)*

**63×, and this is the same idea as every cache in this course** — the memory hierarchy extended one level outward, with DRAM as the fast tier and flash as the slow one.

### And what it costs

**Write-back caching means a successful `write()` guarantees nothing.** If the machine loses power between the call returning and the kernel flushing, the data is gone.

**`fsync()` forces the flush.** Its price:

```
200 x 4K write, no fsync   :  0.0012 s  (   6.0 us/write)
200 x 4K write + fsync each:  0.7753 s  (3876.3 us/write)
fsync costs about 3870 us per call
```

*(Measured.)*

**A 4 KiB write costs 6 μs. Making it durable costs 3.9 ms — 645× more.**

> **This single ratio explains the architecture of every database.** You cannot `fsync` per
> transaction at 645× and remain useful, so systems batch: group commit, write-ahead logs, and
> commit intervals measured in milliseconds. **The "D" in ACID has a price, and this is it.**

---

## 6. What to Take Away

1. **Nine orders of magnitude** from an L1 hit to an `fsync`.
2. **The device is a computer**, reached through memory-mapped registers.
3. **Polling, interrupts, DMA** — and polling is returning, because devices got fast enough that interrupts became the expensive part.
4. **DMA uses physical addresses**, so pages must be pinned and buffers scatter-gathered.
5. **The block device abstraction** hides everything and leaks on access patterns.
6. **The page cache is worth 63×** and is the hierarchy extended outward.
7. **`fsync` costs 3.9 ms against a 6 μs write.** Durability is not free.

---

## Exercises

1. At 3.2 GHz, how many cycles does polling burn waiting 100 μs? How many instructions could have retired?
2. Give the crossover: for what wait time does polling beat an interrupt, if a context switch costs 2 μs? State your assumptions.
3. Why must the kernel pin pages for the duration of a DMA transfer? What would go wrong otherwise — name the Week 6 mechanism.
4. A user buffer of 1 MiB is virtually contiguous. Why might it need a scatter-gather list of 256 entries?
5. `write()` returns success and the power fails. Explain what has and has not happened, and what `fsync` would have changed.
6. A database commits 10 000 transactions per second. Using the measured `fsync` cost, show why one `fsync` per transaction is impossible, and describe the standard workaround.

---

*Next: L23 — what is actually under the block abstraction.*
