# PROG 201 · PS 4 Solutions
## An Allocator Built on `mmap` — Instructor Only

---

**Do not distribute.** Q3 and Q4 depend on students measuring their own allocator, and Q3(b)'s pathological ratio is the point of the problem set.

**Machine these numbers came from:** Linux 7.0.0-30-generic, gcc 13.3.0 (Ubuntu 24.04), glibc 2.39, page size 4,096. Timings vary 10–20% run to run; **the third workload's ratio does not** — it is three orders of magnitude and no amount of noise touches it.

---

## Reference Solution — `mymalloc.c`

Builds clean under `gcc -Wall -Wextra -O2 -g -std=c11 -c mymalloc.c`.

```c
/* PROG 201 -- PS 4 reference solution: an allocator built on mmap.
 *
 * One free list, first fit, split on allocate, coalesce on free.
 * Allocations above BIG get a mapping of their own and give it straight back.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stddef.h>
#include <unistd.h>
#include <sys/mman.h>

#define ALIGN     16
#define ARENA     (1L << 20)          /* grow the heap a MiB at a time */
#define BIG       (128L * 1024)       /* above this, one mapping each   */
#define MAGIC     0x4d414c4cu

struct header {                        /* 32 bytes, 16-aligned payload */
    uint32_t magic;
    uint32_t mapped;                   /* 1 => this block is its own mmap */
    size_t   size;                     /* payload bytes, not counting this */
    struct header *next;               /* free list link, only when free   */
    size_t   pad;
};

static struct header *free_list;
static size_t total_mapped, n_mmap, n_munmap;

static size_t roundup(size_t n, size_t a) { return (n + a - 1) & ~(a - 1); }

static void *map(size_t bytes)
{
    void *p = mmap(NULL, bytes, PROT_READ | PROT_WRITE,
                   MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (p == MAP_FAILED) return NULL;
    total_mapped += bytes; n_mmap++;
    return p;
}

/* Keep the free list sorted by address, so coalescing is a check on the two
 * neighbours.  Sorted insert is O(n); a real allocator uses size classes and
 * boundary tags, which is Q5. */
static void insert_free(struct header *h)
{
    struct header *prev = NULL, *cur = free_list;
    while (cur && cur < h) { prev = cur; cur = cur->next; }
    h->next = cur;
    if (prev) prev->next = h; else free_list = h;

    /* coalesce forward: is the next free block exactly where this one ends? */
    if (h->next && (char *) h->next == (char *) (h + 1) + h->size) {
        h->size += sizeof *h + h->next->size;
        h->next  = h->next->next;
    }
    /* coalesce backward */
    if (prev && (char *) h == (char *) (prev + 1) + prev->size) {
        prev->size += sizeof *h + h->size;
        prev->next  = h->next;
    }
}

void *my_malloc(size_t n)
{
    if (n == 0) return NULL;
    n = roundup(n, ALIGN);

    if (n >= BIG) {                                   /* its own mapping */
        size_t bytes = roundup(n + sizeof(struct header), 4096);
        struct header *h = map(bytes);
        if (!h) return NULL;
        h->magic = MAGIC; h->mapped = 1;
        h->size = bytes - sizeof *h;
        return h + 1;
    }

    struct header **pp = &free_list;
    for (; *pp; pp = &(*pp)->next) {
        struct header *h = *pp;
        if (h->size < n) continue;
        if (h->size >= n + sizeof *h + ALIGN) {       /* split */
            struct header *rest = (struct header *) ((char *) (h + 1) + n);
            rest->magic = MAGIC; rest->mapped = 0;
            rest->size = h->size - n - sizeof *h;
            rest->next = h->next;
            *pp = rest;
            h->size = n;
        } else {
            *pp = h->next;
        }
        h->magic = MAGIC; h->mapped = 0;
        return h + 1;
    }

    size_t bytes = roundup(n + sizeof(struct header), ARENA);
    struct header *h = map(bytes);
    if (!h) return NULL;
    h->magic = MAGIC; h->mapped = 0;
    h->size = bytes - sizeof *h;
    insert_free(h);
    return my_malloc(n);                              /* now it will fit */
}

void my_free(void *p)
{
    if (!p) return;
    struct header *h = (struct header *) p - 1;
    if (h->magic != MAGIC) { fprintf(stderr, "my_free: bad pointer %p\n", p); abort(); }
    if (h->mapped) {
        size_t bytes = h->size + sizeof *h;
        munmap(h, bytes); n_munmap++; total_mapped -= bytes;
        return;
    }
    insert_free(h);
}

void *my_realloc(void *p, size_t n)
{
    if (!p) return my_malloc(n);
    struct header *h = (struct header *) p - 1;
    if (h->magic != MAGIC) abort();
    if (h->size >= n) return p;
    void *q = my_malloc(n);
    if (!q) return NULL;
    memcpy(q, p, h->size);
    my_free(p);
    return q;
}

void my_stats(void)
{
    size_t free_bytes = 0, blocks = 0;
    for (struct header *h = free_list; h; h = h->next) { free_bytes += h->size; blocks++; }
    fprintf(stderr, "mapped %zu KiB in %zu mmaps (%zu munmaps); free list: %zu blocks, %zu KiB\n",
            total_mapped / 1024, n_mmap, n_munmap, blocks, free_bytes / 1024);
}
```

---

## Q1 — The Allocator (30)

**(a) [20]** Marks: header with a magic and a checked `my_free` **[4]**, 16-byte alignment with the assertion **[4]**, first fit with a defended split threshold **[4]**, **coalescing both directions [5]**, large blocks with their own mapping and `munmap` on free **[3]**.

The five-mark item is coalescing, and it is the one most often half-done: forward merging is easy and backward merging is what the address-sorted list is *for*. A submission that merges forward only will pass every functional test and fail Q3(a) row 3 by an even wider margin than the reference — worth pointing out to them, because it turns a design mistake into a visible number.

**Where 16 comes from:** `alignof(max_align_t)` on x86-64, which is the alignment of `long double`; SSE loads (`movaps`) fault on a misaligned address, so it is not a performance nicety. Accept "the widest scalar type the ABI has".

Deduct for: a header that is not a multiple of 16 (the payload then is not aligned even if the arena is); `my_free` that trusts the pointer; splitting with no minimum remainder, which manufactures unusable slivers.

**(b) [6]** Copying every time is acceptable **[3]** with the cost stated. Growing in place when the following block is free is **[6]** — and the detail to check is that they verify the *next* block is free **and adjacent**, not merely that the free list contains something big enough.

Note for discussion: `realloc(p, n)` where `n` is smaller should not shrink-and-copy; the standard permits returning `p` unchanged, and the reference does.

**(c) [4]** Both numbers, printed. The common error is reporting the free-list total as "free memory" without also reporting what was taken from the kernel — the ratio is the whole of Q4(a) and needs both.

---

## Q2 — Make It Fail Properly (18)

**(a) [6]** Four checks **[4]**, and the honest report **[2]**.

The overlap check is the one that catches real bugs: keep the live pointers and sizes in an array and verify no two ranges intersect. A splitting bug that hands out the same 16 bytes twice passes every other test.

**"It passed all four first time"** — accept it, and probe: ask them to deliberately break `insert_free`'s forward merge and confirm the tests still pass. If they do, the tests are weak and the student has learned the intended thing. Award the marks either way if the report is honest.

**(b) [6]** Guard mode **[3]**, the demonstration **[1]**, the reason with a number **[2]**.

The positioning detail is the mark: the payload must **end** at the page boundary, so `mmap` two pages, `mprotect` the second `PROT_NONE`, and return `page_end - n` rounded down to 16. A student who puts the payload at the start of the page catches nothing — the overrun runs into the rest of the page first.

The number: every allocation costs at least two pages of address space and **one `vm_area_struct` in the kernel**. `wc -l /proc/self/maps` after a thousand guarded allocations is in the thousands, against a handful normally; `VmSize` grows by 8 MiB per thousand 16-byte allocations. Kernel VMA lookup is a red-black tree, so a program with 100,000 VMAs makes every subsequent fault slower.

**(c) [6]** Two marks each.

- **Never allocated:** the magic check catches most of it and cannot catch all — a pointer into the middle of a live block may have a plausible magic before it. The reference aborts. Real allocators either abort (glibc's "invalid pointer") or, in a debug build, check the pointer is within a known arena.
- **Double free:** the reference **does not catch it** — the block goes onto the free list twice and the list becomes cyclic, so the next `my_malloc` may hand out the same block to two callers. Students who noticed deserve credit; the fix is a flag bit in the header set on free and cleared on allocate, which is what glibc's tcache double-free check does.
- **Overrun into the next block's header, then free that block:** **undetectable by design.** The header is inline, so the overrun is a legal write as far as the allocator can tell, and by the time `my_free` reads the corrupted size the damage is done. This is the case for **out-of-line metadata**: a debugging allocator keeps headers in a side table so a payload overrun cannot reach them, which is exactly what ASan does and why it costs 2–3× to run.

Full marks on the third require naming the design property, not just "it crashes".

---

## Q3 — Measure It (22)

**(a) [10]** Reference, 200,000 operations:

| workload | mine | glibc | ratio |
| --- | --- | --- | --- |
| allocate all, then free all | 0.0443 s | 0.0505 s | **0.88×** |
| allocate, free half as you go | 0.0094 s | 0.0197 s | **0.48×** |
| allocate 40,000, free every other, allocate 40,000 more | **1.6375 s** | 0.0048 s | **339×** |

**(b) [6]** The third. `my_malloc` is *O(n)* in the free list and `my_free` is *O(n)* to find the insertion point, and **n is 20,000** — the blocks freed by the every-other pass. 40,000 operations against a 20,000-long list is *O(n²)*, and 339× is what that looks like. glibc bins by size, so both operations are *O(1)*.

Marks: identifying the workload **[2]**, the complexity of both operations **[2]**, naming *n* **[2]**. "It's the free list" without *n* is [3].

**If they beat glibc on all three:** the usual cause is that their third workload frees in an order that coalesces everything back into one block, so the list never grows. Ask them to print the free-list length; if it is 1, the workload is not fragmenting.

**(c) [6]** ptmalloc maintains fastbins, tcache, smallbins, largebins, arena locking and a dynamic `mmap` threshold — **bookkeeping that pays off across many workloads and costs on every single one.** A first-fit list with no locking and no size classes does less work per operation, so on a workload where the list stays short it wins, and it wins honestly.

The question that matters: **you would have to know the distribution of allocation sizes and, more importantly, of lifetimes** — because lifetime is what determines whether the free list stays short or fragments. Accept any answer naming both size and lifetime distributions; excellent answers add that you would need the *sequence*, not just the distributions, since interleaving is what fragments.

This is Wilson et al. (1995)'s conclusion and it is worth saying the paper's name out loud when returning the marks.

---

## Q4 — Fragmentation (16)

**(a) [6]** Reference `my_stats` after the three workloads: 61,440 KiB taken from the kernel across 61 mappings, with the free list holding 61,439 KiB at the end — i.e. **essentially everything is free and none of it has been returned**, because the small-object arena never is (Q5(b)).

Marks: the ratio for all three **[3]**, and correctly identifying **external** fragmentation in workload 3 and **internal** in workload 1 **[3]**.

**(b) [6]** 17 bytes rounds to 32 (16-byte alignment) plus a 32-byte header = **64 bytes for a 17-byte object**. A million of them is 64 MB of RSS against 17 MB requested: **73% overhead**, and the header is bigger than the object.

What real allocators do: **size classes with the metadata outside the block** — a page (or "slab", or "run") is dedicated to one size class, and the class is recoverable from the page's address, so a 17-byte object costs 24 or 32 bytes total and no per-object header at all. What it costs: a page can only hold one size, so a program using one 17-byte object and one 33-byte object pays for two pages. That is the trade jemalloc, tcmalloc and the Linux slab allocator all make.

Marks: the arithmetic **[2]**, alignment and header identified separately **[2]**, size classes with the cost **[2]**.

**(c) [4]** **External fragmentation**, not a leak: live data is constant while the allocator holds memory it cannot use in usefully sized pieces.

Confirm with `mallinfo2()` — `uordblks` (in use) roughly constant while `arena` + `hblkhd` grows — or `/proc/pid/smaps_rollup`, where `Rss` climbs while the program's own accounting of live objects does not.

The two structural fixes: **(1) size-class or pool allocation**, so blocks of a class are only ever reused for that class and holes cannot be the wrong size; **(2) arena-per-phase / region allocation**, where a whole arena is freed at once when a request or a phase ends, which is what a compiler pass or a request-scoped web server does. Accept "switch to jemalloc" as a third with a shrug — it is what people actually do and it is a different allocator's fragmentation, not none.

---

## Q5 — Do It Properly (14)

**(a) [8]** Either structure, implemented and measured.

**Boundary tags** remove the search from `my_free` — the previous block's footer is at `(char *)h - sizeof(size_t)` — so `free` becomes *O(1)*. `malloc` is still *O(n)* over the free list, so the reference's third workload improves by roughly half and stays quadratic. Expect students to report something between 2× and 5× better and still catastrophic; **that is the correct result and they should say so.**

**Segregated lists** fix `malloc` instead, and with enough classes the third workload comes back to within a small multiple of glibc. A student who does both has fixed it properly.

Marks: implementation **[5]**, before/after on the third workload **[2]**, an honest statement of how much survived **[1]**. **Do not require the penalty to disappear** — the honest report is the mark.

**(b) [6]** Three each.

- **`tcache`:** caches recently freed chunks **per size class, per thread**, so `free` pushes and `malloc` pops with no lock, because the cache is reachable only from one thread — it is `_Thread_local` (Week 3 L10 §5). The correctness problem it creates: **memory migrates between threads.** A block allocated by thread A and freed by thread B lands in B's cache and never returns to A, so a producer/consumer pair can grow memory without bound. Real allocators bound the cache and flush it. Accept also "double-free detection gets harder", which is a real CVE-generating property of tcache.
- **Returning the arena:** you would have to track whether an entire mapping's worth of contiguous space is free and `munmap` exactly that mapping, which a single free list spanning several mappings cannot easily tell you — hence per-mapping accounting. glibc mostly does not because the top-of-heap `brk` arena can only be trimmed from the end (`M_TRIM_THRESHOLD`, 128 KiB by default), and because giving pages back means faulting them in again later at 1.9 µs each (L13 §4). **Holding freed memory is usually the right decision**, which is why RSS is a poor proxy for a leak.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | The allocator | 30 |
| 2 | Make it fail properly | 18 |
| 3 | Measure it | 22 |
| 4 | Fragmentation | 16 |
| 5 | Do it properly | 14 |
| | **Total** | **100** |

---

*PROG 201 · Week 4 · PS 4 Solutions · Instructor Only · © CSE Department*
