# PROG 201 · Systems Programming in C
## Week 4 · Lecture 2 of 3
### Where Memory Comes From: `brk`, `mmap`, and `malloc`

---

**Reading:** APUE §7.8 · TLPI Ch. 7 · CS:APP §9.9 · `man 2 brk`, `man 3 mallopt`, `man 3 mallinfo2` · **Previous:** L13 · **Next:** L15 — `mprotect` and JIT

---

## 1. There Is No Heap

There is a line in `/proc/self/maps` labelled `[heap]`, and it is a convenience, not a thing:

```
5a132cfbc000-5a132cfdd000 rw-p 00000000 00:00 0          [heap]
```

It is an anonymous `MAP_PRIVATE` region like any other. The kernel labels it `[heap]` because it is the region grown by `brk`, and that is the whole of what makes it the heap.

**`malloc` is a library function, not a system call.** The kernel has no idea your program has a `malloc`; it hands out pages, and everything else — sizes, alignment, reuse, `free` — happens in userspace, in `libc`, in code you could have written yourself. That is what PS 4 asks you to do, and the point of doing it is that after this week `malloc` stops being magic.

Two system calls stand behind it.

---

## 2. `brk` and `sbrk`: One Number

```c
int   brk(void *addr);      /* set the program break to addr    */
void *sbrk(intptr_t incr);  /* move it by incr; return the OLD value */
```

The **program break** is the end of the process's data segment. Raising it makes the region between the old and new break valid, zero-filled, anonymous memory. Lowering it throws it away. That is the entire interface — **one number, moved up and down** — and it dates from a time when a process had one contiguous data area.

It is enough to write an allocator (`sbrk(n)` for more, and never give it back), and it has two crippling limitations:

- **It is one-dimensional.** You can only return memory from the *end*. Free a 100 MiB block in the middle and the break cannot move past it, so the memory stays yours forever.
- **There is one of it.** Two threads calling `sbrk` concurrently race on the same number, and a library that uses `sbrk` fights the `malloc` in the same process.

`sbrk` is not even a system call any more — glibc implements it on top of `brk` — and `man 2 brk` says plainly that it is not specified by POSIX. **Use `mmap` in new code.** `brk` survives because glibc's `malloc` still uses it for the main arena, where "return memory from the end only" is exactly what a stack-like allocation pattern wants.

---

## 3. What `malloc` Actually Does

glibc's allocator (ptmalloc, descended from Doug Lea's) keeps a **chunk** header before every block: size, plus flag bits, plus — when the chunk is free — links into a free list. Free chunks are sorted into **bins**:

| Bin | Holds | Policy |
| --- | --- | --- |
| `fastbins` | small chunks, ≤ 128 bytes | LIFO, not coalesced — speed over tidiness |
| `tcache` | per-**thread** cache, 64 chunks per size | no lock at all; glibc ≥ 2.26 |
| `smallbins` | exact-size lists up to 1,008 bytes | FIFO, coalesced |
| `largebins` | size ranges above that | best fit within the bin |
| the top chunk | the space at the end of the arena | grown with `brk` |

**`tcache` is why Week 0's `malloc`-in-a-signal-handler experiment did not deadlock.** L03 §4 measured 1.49 billion allocations under ~100,000 signals with no hang, because the fast path takes no lock. It is also why "malloc is not async-signal-safe" remains true: the fast path is not the only path.

An **arena** is a heap with a lock. The main arena is grown with `brk`; additional arenas — created when threads contend — are `mmap`ed. This is why a heavily threaded program's `/proc/pid/maps` has several large anonymous regions that are not `[heap]`.

---

## 4. The Threshold, Measured

Above some size, `malloc` stops carving up its arena and asks the kernel for a mapping of its own. `one.c` allocates once per process, so nothing is reused, and reports where the pointer landed:

```
     size  came from
       16  brk
     4096  brk
    65536  brk
   131072  brk
   131073  brk
   262144  mmap
  1048576  mmap
```

Bisecting the boundary exactly:

```
largest brk allocation:   134472
smallest mmap allocation: 134473
```

**The documented threshold is 128 KiB — 131,072 — and the measured switch is at 134,473.** The 3,401-byte difference is the point: the threshold is compared against the **chunk** size (your request plus a header, rounded up) and only after the allocator has failed to satisfy you from the top chunk, which glibc had already grown to 132 KiB. `M_MMAP_THRESHOLD` is a threshold on the allocator's internal decision, not a promise about your argument.

And it **moves**. glibc raises the threshold dynamically when it sees a large block freed, up to 32 MiB, on the theory that a program which allocated 1 MiB once will do it again and should not pay for a fresh mapping each time. `mallopt(M_MMAP_THRESHOLD, n)` pins it and disables the adaptation.

`strace` on eight allocations:

```
brk(0x5b6e298ba000)   = ...        <- three brk calls
brk(0x5b6e298db000)   = ...
brk(0x5b6e298bb000)   = ...
mmap(NULL, 1052672,  ...)          <- the 1 MiB malloc
munmap(0x7c6526cff000, 1052672)    <- and its free
mmap(NULL, 16781312, ...)          <- the 16 MiB malloc
munmap(0x7c6525dff000, 16781312)
```

**Three system calls for the six small allocations, and one each for the two large ones.** That asymmetry is the reason for the threshold: a large block returned to the arena would fragment it and could never be given back to the system, while a large block with its own mapping is returned to the kernel by `free` immediately — which is also why a program that allocates and frees 1 MiB in a loop can be slower than one that allocates 1 KiB, and why `M_MMAP_THRESHOLD` exists as a knob.

---

## 5. Building One

The design PS 4 asks for, and the smallest thing that deserves to be called an allocator:

```c
struct header {
    uint32_t magic;      /* catch a bad free early                    */
    uint32_t mapped;     /* 1 => this block has a mapping of its own  */
    size_t   size;       /* payload bytes                             */
    struct header *next; /* free-list link; only meaningful when free */
    size_t   pad;        /* keep the payload 16-aligned               */
};
```

Four decisions, each with a real alternative:

**Where the metadata lives.** In a header immediately before the payload, so `free(p)` finds it with `(struct header *) p - 1` and no lookup. The alternative is a side table, which costs a search but leaves the payload untouched — this is what a debugging allocator does, and it is why ASan can tell you about a heap overflow that a header-based allocator would simply not survive.

**Alignment.** `malloc` must return memory suitable for any type, which on x86-64 means **16 bytes** (`alignof(max_align_t)`). Get this wrong and SSE loads fault. Making the header a multiple of 16 makes the payload aligned for free.

**How you find a block.** First fit is what fits in a lecture: walk the free list, take the first block big enough, split it if the remainder is worth having. Best fit wastes less and costs a full walk. Segregated lists by size class are what real allocators do, and they are why glibc has bins.

**When you give memory back.** Small allocations come out of a 1 MiB arena that is never returned; large ones get their own mapping and `free` calls `munmap` at once. That mirrors glibc, and §4 is why.

---

## 6. Coalescing, and Why the List Is Sorted

Split without merging and every `free` makes the heap permanently more granular: a hundred allocations of 64 bytes, all freed, leave a hundred 64-byte holes and no room for a 128-byte request. **Coalescing is not an optimisation; it is what makes `free` mean anything.**

Merging two adjacent free blocks needs you to know they are adjacent, which is why the reference keeps the free list **sorted by address**:

```c
static void insert_free(struct header *h)
{
    struct header *prev = NULL, *cur = free_list;
    while (cur && cur < h) { prev = cur; cur = cur->next; }
    h->next = cur;
    if (prev) prev->next = h; else free_list = h;

    if (h->next && (char *) h->next == (char *) (h + 1) + h->size) {
        h->size += sizeof *h + h->next->size;      /* merge forward  */
        h->next  = h->next->next;
    }
    if (prev && (char *) h == (char *) (prev + 1) + prev->size) {
        prev->size += sizeof *h + h->size;         /* merge backward */
        prev->next  = h->next;
    }
}
```

**The sort is what makes those two `if`s possible**, and it is also what makes the function *O(n)*. Real allocators avoid the walk with **boundary tags**: a footer at the end of every block repeating its size, so the block before you can be found by arithmetic rather than by searching. That is Knuth's trick from 1973, it is in CS:APP §9.9, and it is Q5 on the problem set.

---

## 7. Where a Simple Allocator Dies

The reference allocator is 150 lines. Measured against glibc, 200,000 allocations of 16–528 bytes:

| workload | mine | glibc | ratio |
| --- | --- | --- | --- |
| allocate all, then free all | 0.0443 s | 0.0505 s | **0.88×** |
| allocate, free half as you go | 0.0094 s | 0.0197 s | **0.48×** |
| **allocate 40,000, free every other one, allocate again** | **1.6375 s** | **0.0048 s** | **339×** |

**It beats glibc on two workloads and loses by a factor of three hundred and thirty-nine on the third.**

Nothing is wrong with the first two numbers. On a workload where the free list stays short, a 150-line first-fit allocator really is faster than ptmalloc, because ptmalloc is doing bookkeeping — bins, arenas, thread caches — that this workload never benefits from.

The third workload builds a free list of **20,000 blocks** and then allocates from it 20,000 times. Every allocation walks the list; every `free` walks it again to find the insertion point. That is *O(n²)*, and 339× is what *O(n²)* looks like when *n* is twenty thousand. glibc has bins, so the same workload is *O(1)* per operation.

**The lesson is about benchmarks, not about allocators.** It is easy to write an allocator that beats glibc, and the difficulty is entirely in choosing the workload. Every allocator is fast on some distribution of sizes and lifetimes and terrible on another, which is why programs with unusual allocation patterns — a compiler, a game engine, a web server — routinely ship their own, and why *general-purpose* allocators are so much harder than they look.

This is Week 2's shared-memory result in a new place. **A number that flatters your implementation is a fact about your test.**

---

## 8. Fragmentation

Two kinds, and only one of them is visible in a profiler:

**Internal fragmentation** is the space inside a block you were given but cannot use: rounding to 16 bytes, the header, the size class you were rounded up to. It is bounded and predictable — ask for 17 bytes from the reference and 32 bytes of payload plus a 32-byte header are spent, so **65% of that allocation is overhead.** For small objects the header is often bigger than the object, which is why real allocators use size classes with the metadata *outside* the block.

**External fragmentation** is free memory you cannot use because it is in the wrong-sized pieces. §7's third workload is the pathological case, and it has no general solution in C — you cannot move a block, because somebody holds a pointer to it. Garbage-collected languages compact the heap precisely because they *can* move things; C's guarantee that `p` stays valid until you `free` it is exactly what forbids it.

The number to know: `mallinfo2()` reports `uordblks` (bytes in use) and `fordblks` (bytes free but held), and the ratio between the second and what the process has taken from the kernel is your fragmentation. A long-running program whose RSS grows while its live data does not is fragmenting, not leaking, and the two need entirely different fixes.

---

## Summary

- **There is no heap** — `[heap]` is the anonymous region grown by `brk`, and `malloc` is a library function the kernel knows nothing about.
- `brk`/`sbrk` move **one number**, so memory can only be returned from the end. Use `mmap`.
- glibc keeps chunk headers and sorts free chunks into **fastbins, tcache, smallbins and largebins**; `tcache` is the lock-free fast path Week 0 measured.
- The `mmap` threshold is documented as 128 KiB and **measured at 134,473 bytes**, because it applies to the chunk after the top chunk has failed — and it adapts upward at runtime.
- An allocator needs: a header, **16-byte alignment**, a fit policy, and a rule for returning memory.
- **Coalescing is what makes `free` mean anything**, and an address-sorted free list is the cheap way to do it — at *O(n)*. Boundary tags are the real answer.
- A 150-line allocator beat glibc **0.88×** and **0.48×** on two workloads and lost **339×** on a fragmenting one. The difficulty in allocators is choosing the workload, not writing the code.
- **Internal** fragmentation is overhead inside blocks; **external** is free memory in useless pieces, and C cannot compact.

---

## Exercises

1. Write the two-line program that prints `sbrk(0)` before and after `malloc(1)`. Then run it under `strace` and explain why the break moved by more than one byte.
2. `mallopt(M_MMAP_THRESHOLD, 4096)` and re-run §4's bisection. Where is the boundary now, and why is it still not 4,096?
3. Allocate 1 MiB, free it, and allocate 1 MiB again, with `strace`. How many `mmap` calls do you see, and what does that tell you about the dynamic threshold?
4. Implement `my_realloc` that grows in place when the next block is free. Measure it against a version that always copies, on a `realloc`-heavy workload.
5. Add boundary tags to the reference allocator and re-run §7's third workload. How much of the 339× survives?
6. `mallinfo2()` before and after §7's third workload. What are `uordblks` and `fordblks`, and what is the ratio?
7. Ask for 17 bytes a million times and never free. Compare the process's RSS with 17 million bytes. Where did the rest go?

---

*PROG 201 · Week 4 · L14 · © CSE Department*
