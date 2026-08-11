# CS 201 · Midterm 2 — Solutions and Mark Scheme
## Instructor Only

---

> **Not for distribution before the paper is returned.** All quoted measurements are from the
> Weeks 5–9 lectures and labs. **Method over answer**: a correct approach with an arithmetic slip
> keeps most marks; a bare number on a "show your working" question keeps none.

---

## Q1 — Pipelining and Parallelism (20)

### (a) [4]

**[2]** **Latency** is the time for one instruction end-to-end; **throughput** is instructions completed per unit time. **[2]** Pipelining improves **throughput only** — each instruction still traverses all stages, but one completes per cycle once the pipeline is full.

### (b) [4]

- (1)→(2): **RAW** on `rax` — a load-use hazard, and a **true dependency**.
- (2)→(3): **WAR** on... no — (3) writes `rbx`, which (1) read. (1)→(3) is **WAR** on `rbx`.

**RAW is the true dependency; WAR/WAW are naming artefacts removed by register renaming.**

> Accept identification of the RAW as the one that matters; award the [2] for "renaming removes WAR/WAW,
> cannot remove RAW".

### (c) [4]

The single chain is **latency-bound** — each `addsd` must complete before the next begins. Four independent chains are **throughput-bound** — the out-of-order engine issues them across multiple units in parallel. Hence 4.00× on identical arithmetic.

### (d) [4]

At 16 KiB/array the three arrays fit in L1/L2 and the **vector units are the limit** (4.51×). At 16 MiB they total 48 MiB against a 6 MiB L3, so the loop is **memory-bandwidth-bound** and wider arithmetic does nothing (1.07×). **One resource binds at a time; SIMD helps only when compute is it.**

### (e) [4]

$$S = \frac{1}{(1-0.4) + \frac{0.4}{5}} = \frac{1}{0.6 + 0.08} = \frac{1}{0.68} = \mathbf{1.47\times}$$

> Full marks require the formula and the substitution. A bare "1.47" with no working keeps 1.

---

## Q2 — Virtual Memory (20)

### (a) [4]

A page is 4096 B and a PTE is 8 B, so a table holds $4096/8 = 512$ entries, and $\log_2 512 = \mathbf{9}$. **The index width is a consequence of page size and entry size**, and makes every table exactly one page.

### (b) [4]

**Five.** Four page-table levels (PGD, PUD, PMD, PTE) plus the data access itself.

### (c) [4]

**Only the number of pages the data is spread across.** The 32 KiB stayed L1-resident throughout; the 22× rise is **address translation** — 8 pages fit the TLB, 8192 do not, so nearly every access needs an L2-TLB lookup or a page walk. **The TLB is the structure responsible**, and its reach is a separate capacity from cache size.

### (d) [4]

**`malloc` is a promise, not a delivery** — the kernel recorded a mapping and committed almost no physical memory. **Pages become resident on first touch**, one minor fault each *(measured: 131 071 faults for 131 072 pages)*.

### (e) [4]

**Copy-on-write**, implemented by the **R/W (writable) bit**. After `fork`, all pages are shared read-only in both processes; the first write to each traps, the kernel copies that one page and marks it writable. $256\text{ MiB}/4096 = 65\,536$ pages, one fault each.

---

## Q3 — Storage (20)

### (a) [4]

**Seek + rotational latency + transfer.** For 4 KiB, transfer is **~0.2%** of the total (≈0.03 ms of ~13 ms); seek dominates. **Implication: large blocks are nearly free**, so filesystems, read-ahead and B-trees all use large transfers to amortise the seek.

### (b) [4]

**A page can only be programmed after erase, and erase operates on a whole block.** Page 4–16 KiB (read/program); erase block 1–4 MiB (erase). **The FTL writes new data to an already-erased page elsewhere and remaps**, rather than rewriting the block in place.

### (c) [4]

**Per-request software overhead** — syscall, block layer, NVMe submission/completion — a fixed cost per request that dominates at 4 KiB and is amortised at 1 MiB. **If the device were the limit, the curve would be flat.**

### (d) [4]

**Whether the data was already in DRAM.** Buffered hits the page cache; `O_DIRECT` bypasses it and reaches the device. Same 4 KiB read, 63× apart.

### (e) [4]

Budget at 10 000 tps is **100 μs/transaction**; one `fsync` is **3876 μs** — **~39× the budget**, capping the system near 256 tps. **The technique is group commit**: many transactions share one `fsync`, trading a few ms of latency for throughput.

> Require the arithmetic (budget vs cost) for full marks, not just "batch them".

---

## Q4 — Networks (20)

### (a) [4]

**Application** (HTTP), **Transport** (TCP), **Network** (IP), **Link** (Ethernet). Overhead: 20 + 20 + 14 = **54 bytes** for a 1-byte payload.

### (b) [4]

Any two: two 100-byte reads; one 200-byte read; 37 + 163; etc. **TCP preserves order and completeness, not message boundaries**, so a protocol must frame itself (length prefix or delimiter).

### (c) [4]

**41 ms is Linux's delayed-ACK timer.** **Nagle** held the second small write until the first was acknowledged; the receiver's **delayed ACK** held the acknowledgement hoping to piggyback it on a reply it could not yet send. Each waited for the other.

> "Nagle made it slow" alone is 2 of 4 — the 41 ms is the delayed-ACK timer on the *other* side.

### (d) [4]

TCP handshake ~183 ms + TLS ~212 ms + response ~187 ms ≈ **three round trips ≈ 582 of 589 ms**. **The server's own processing was invisible** inside the final round trip.

### (e) [4]

**Concurrency = throughput × latency** = $1000 \times 0.187 = \mathbf{187}$ requests in flight. **A one-at-a-time server manages ~5 requests/second** on this link regardless of CPU speed — hence async I/O / thread pools / `epoll`.

---

## Q5 — Security (20)

### (a) [4]

`buf` at `rbp-0x10`: 16 (buf) + 8 (saved rbp) = **24 bytes** to the return address. Frame drawn: buf `[rbp-0x10..-1]`, saved rbp `[rbp..+7]`, return addr `[rbp+8]`.

### (b) [4]

Any two: **it is thread-local storage, unreachable through a stack overflow**; **it is randomised per process**, so an attacker cannot predict it; **a normal local would itself be overwritten** by the same overflow. The attacker cannot reproduce a value they cannot read.

### (c) [4]

**Code reuse — ret2libc / ROP.** NX stops *new* code from executing; it does not stop jumping to code that is *already* executable. **libc's ~6000 `ret` instructions are gadget terminators**, and the set is large enough to be Turing-complete, so the attacker builds the computation from existing fragments.

### (d) [4]

`count * size` **overflows** for large `count`, wrapping to a small value; `malloc` returns a tiny buffer the caller then overflows — a **heap overflow**. **Fix:** `calloc(count, size)` or `__builtin_mul_overflow`, which detect the overflow and refuse.

### (e) [4]

**`endbr64` being present proves only that CET was *compiled in*, not that the hardware *enforces* it.** Check the CPU (`grep -E 'shstk|ibt' /proc/cpuinfo`), the kernel, and the process's opt-in. **On this machine's 2017 CPU there is no `shstk`, so the shadow stack is not enforced despite the landing pads.**

> The "compiled in ≠ enforced" distinction is the marked point; award full only if it is explicit.

---

## Mark Summary and Expected Distribution

| | | Expected mean |
|---|---:|---:|
| Q1 Pipelining/Parallelism | 20 | ~13 |
| Q2 Virtual Memory | 20 | ~13 |
| Q3 Storage | 20 | ~14 |
| Q4 Networks | 20 | ~12 |
| Q5 Security | 20 | ~13 |
| **Total** | **100** | **~65** |

**Where marks will be lost, in order:**

1. **Q4(c)** — blaming Nagle without naming the delayed-ACK timer.
2. **Q2(c)** — attributing the 22× to cache rather than TLB, or vice versa.
3. **Q1(e) / Q3(e) / Q4(e)** — the three calculations, done without the formula shown.
4. **Q5(e)** — saying CET is active because `endbr64` is present.
5. **Q3(c)** — attributing the 18× to the device rather than per-request overhead.

Items 1 and 5 are the same error in two topics — **attributing a measured effect to the wrong cause** — and are worth naming when the paper is returned, since Week 11 is entirely about correct attribution.

---

*CS 201 · Midterm 2 Solutions · Instructor Only*
