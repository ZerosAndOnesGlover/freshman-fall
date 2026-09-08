# PROG 201 · Problem Set 4
## An Allocator Built on `mmap`

---

**Released:** Week 4, Wednesday · **Due:** Week 5, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS4_{LastName}_{StudentID}.pdf`, and your code as `PS4_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine. The write-up and the code must be yours.
>
> **Q3 is measurement on your own machine.** State your `gcc --version`, `uname -r`, `getconf
> PAGESIZE`, and whether you are on BH 215 or your own hardware.
>
> **You are replacing `malloc`, so you cannot use `malloc`.** No `calloc`, no `strdup`, no
> `getline`, and be careful with `printf`, which allocates on its first call — call it once before
> you start measuring. `mmap`, `munmap` and `mprotect` are your only sources of memory.
>
> Everything compiles clean under `gcc -Wall -Wextra -O2 -std=c11`. Warnings cost marks.

---

### The Interface

```c
void *my_malloc(size_t n);
void  my_free(void *p);
void *my_realloc(void *p, size_t n);
void  my_stats(void);          /* to stderr: mappings held, free list length, bytes free */
```

Two sources of memory, as in L14 §5:

- **Small requests** come out of an arena you take from the kernel a megabyte at a time and never give back.
- **Requests of 128 KiB or more** get an `mmap` of their own, and `my_free` `munmap`s it immediately.

---

### Q1: The Allocator (30 points)

**(a) [20]** Implement `my_malloc` and `my_free` with a header before each block and a single free list.

Requirements, each of which is a mark:

- **A header before the payload**, so `my_free(p)` finds it at `(struct header *) p - 1` with no search. Include a magic number and check it — an unrecognised pointer must be a diagnosed abort, not silent corruption.
- **The payload is 16-byte aligned.** Say in one sentence where 16 comes from, and prove it: assert `((uintptr_t) p & 15) == 0` for a thousand allocations of random sizes.
- **First fit, with splitting.** Split only when the remainder can hold a header plus something useful; say what threshold you chose.
- **Coalescing on free**, forward and backward. L14 §6 keeps the free list sorted by address to make this two comparisons; you may do that or use boundary tags (Q5), but you must merge.
- **Large blocks get their own mapping** and are `munmap`ed by `my_free`.

**(b) [6]** `my_realloc`. Growing in place when the block that follows is free is worth doing and worth explaining; if you copy every time, say so and say what it costs.

**(c) [4]** `my_stats`, and then the two numbers that make it useful: **bytes you have taken from the kernel** and **bytes currently handed out to the caller**. Print both after each workload in Q3. The ratio between them is Q4.

---

### Q2: Make It Fail Properly (18 points)

**(a) [6]** Write a test that checks, for a thousand random allocations of random sizes:

- every pointer is 16-aligned,
- no two live allocations overlap,
- data written into a block survives every other allocation and free,
- `my_free(NULL)` is a no-op and `my_malloc(0)` does something you can defend.

Report which of those your first implementation failed. **If it passed all four first time, say so and say what you think that means** — an untested allocator that passes on the first run is more often an untested test.

**(b) [6]** Add a **guard mode**, compiled in with `-DGUARD`: every allocation gets its own mapping with a `PROT_NONE` page immediately after it, positioned so the payload ends exactly at the page boundary (L15 §2).

Demonstrate that it turns a one-byte overrun into an immediate `SIGSEGV`. Then say why this is a debugging mode and not the default — your answer must include a number, from `/proc/self/status` or `wc -l /proc/self/maps`.

**(c) [6]** Three errors a real allocator has to survive. For each, say what yours does and what it *should* do:

- `my_free` on a pointer that was never allocated,
- `my_free` twice on the same pointer,
- writing 8 bytes past the end of a block and then calling `my_free` on the **next** block.

The third is the interesting one. Say why the header design in L14 §5 makes it undetectable, and name one thing a real allocator does about it.

---

### Q3: Measure It (22 points)

**(a) [10]** Three workloads, yours against `glibc`, 200,000 operations each:

| workload | mine | glibc | ratio |
| --- | --- | --- | --- |
| allocate all, then free all | | | |
| allocate, free half as you go | | | |
| allocate 40,000, free every other, allocate 40,000 more | | | |

**(b) [6]** One of your three ratios will be much worse than the others — for us the third was **339×**. Report yours and explain it in terms of the complexity of your `my_malloc` and `my_free` on that workload. Give the *O* and say what *n* is.

If instead you beat glibc on all three, your third workload is not fragmenting the heap. Say why not, and fix it.

**(c) [6]** You will probably **beat** glibc on at least one workload. Explain how a 150-line allocator can beat one that thousands of people have worked on, in terms of what ptmalloc is doing that your workload never benefits from.

Then answer the question that matters: **given (b) and (c), what would you have to know about a program before claiming your allocator is better for it?**

---

### Q4: Fragmentation (16 points)

**(a) [6]** After each of Q3's workloads, report **bytes taken from the kernel** against **bytes live**. Define your fragmentation as the ratio, state it for all three, and say which of the two kinds in L14 §8 each one is showing.

**(b) [6]** Ask for 17 bytes, a million times, and never free. Compare your process's `VmRSS` with 17,000,000.

Where did the difference go? Break it down: alignment, header, and anything else. Then say what a real allocator does for small objects that avoids most of it, and why it costs something else.

**(c) [4]** A long-running server's RSS grows steadily while the amount of live data does not. It is not leaking. In three or four sentences: what is happening, how would you confirm it with `mallinfo2` or `/proc/pid/smaps_rollup`, and what are the two structural fixes? *(Neither is "call `free` more".)*

---

### Q5: Do It Properly (14 points)

**(a) [8]** Your free list is walked on both allocate and free. Implement **one** of these and measure the effect on Q3's third workload:

- **Boundary tags** — a footer repeating the size at the end of every block, so the previous block can be found by arithmetic and coalescing needs no search. (CS:APP §9.9.12; Knuth, 1973.)
- **Segregated free lists** — one list per size class, so the search is bounded.

Report the before and after for the third workload, and say how much of your penalty survived.

**(b) [6]** In a paragraph each:

- A `tcache`-style **per-thread** cache would make your allocator faster in a threaded program. Say what it caches and why no lock is needed, and name the correctness problem it creates that a single global free list does not have.
- Your allocator never returns the small-object arena to the kernel. Describe what it would take to, and say why glibc mostly does not either. *(`M_TRIM_THRESHOLD` is the word to look up.)*

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

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*PROG 201 · Week 4 · PS 4 · © CSE Department*
