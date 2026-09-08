# PROG 201 · Reading Guide · Week 4
## APUE §14.8 and Chapter 7, and the chapter CS:APP does better than either

---

**This is the week where CS:APP is the better book.** APUE covers `mmap` in nine pages and `malloc` not at all; CS:APP Chapter 9 spends sixty pages on virtual memory and dynamic allocation, with the hardware underneath visible, and §9.9 is the best written account of an allocator there is. **You are also taking CS 201, which is on the memory hierarchy this term** — read Chapter 9 once for both courses.

| Source | Read? | Why |
|---|---|---|
| **CS:APP §9.8–9.9** | **All of it** | Dynamic memory allocation, done properly. §9.9.12 is boundary tags, which is PS 4 Q5 |
| **CS:APP §9.1–9.7** | **Read** | Address translation, page tables, the TLB. This is L13's mechanism |
| **APUE §14.8** | **Read** | `mmap`, `munmap`, `msync`. Short, and it is L13 §2 |
| APUE §7.8 | Read | Memory allocation, and `sbrk`. Ten minutes |
| **TLPI Ch. 49** | **All of it** | The best Linux-specific treatment of `mmap`. `MAP_NORESERVE`, `MAP_POPULATE`, the lot |
| TLPI Ch. 7 | Read | `brk`, `sbrk`, and why `malloc` is a library function |
| TLPI §50.2–50.4 | **Read** | `mprotect`, `mlock`, `madvise` |
| TLPI Ch. 45–48 | Skip | System V shared memory. Week 2 already said why |

---

## CS:APP Chapter 9 — the questions to hold

**§9.9.1–9.9.5 — the requirements**

1. Knuth lists the constraints on an allocator: handle arbitrary request sequences, respond immediately, use only the heap, align blocks, and **never move an allocated block**. Which of those five is the reason C cannot compact its heap, and which is the reason `realloc` may return a different pointer?
2. **Throughput and peak utilisation are in tension.** Write the definition of peak utilisation from the book, then say which of the two your first-fit allocator optimises.

**§9.9.6–9.9.9 — implicit lists**

3. The book stores the size and an allocated bit in one word by exploiting alignment. **How many bits does 16-byte alignment free up, and what else could you put in them?**
4. First fit, next fit, best fit. Bryant gives a one-line summary of each. Predict which is worst for external fragmentation before you read the answer.
5. §9.9.10, splitting: the book splits only when the remainder is at least a minimum block size. **What goes wrong without that rule?** Name the condition, and note that it is why PS 4 Q1(a) asks for a threshold.

**§9.9.12 — boundary tags. This is the section.**

6. Draw a block with a header and a footer. Then write the pointer arithmetic that finds the **previous** block from a given one, and say why it is impossible without the footer.
7. Boundary tags cost a word per block. **For what size of block does that cost exceed 25%?** Then find where the book says how to avoid paying it on allocated blocks.

**§9.9.13–9.9.14 — segregated lists**

8. Simple segregated storage never splits or coalesces. Say what that buys and what it costs, in one sentence each.
9. Where does glibc's `fastbins` sit on the spectrum between §9.9.13 and §9.9.14? *(L14 §3 has the table.)*

---

## APUE and TLPI — the `mmap` questions

10. `MAP_PRIVATE` against `MAP_SHARED` on a **file**. APUE §14.8 states the difference; write down what you expect a store through a `MAP_PRIVATE` file mapping to do to the file, then check against L13 §2. **Most people get this wrong the first time.**
11. `msync` has `MS_SYNC`, `MS_ASYNC` and `MS_INVALIDATE`. What does the third one do, and when would you want it?
12. TLPI §49.4.3 covers `MAP_NORESERVE` and overcommit. What are the three settings of `/proc/sys/vm/overcommit_memory`, and which one makes `mmap` of 4 GiB on a 7 GiB machine fail?
13. TLPI Ch. 49's `mmap`-based IPC section revisits Week 2. Read it as revision and note the one thing it says that L08 did not.

---

## The Man Pages for This Week

| Page | The paragraph |
|---|---|
| **`man 2 mmap`** | The flags table in full, and the NOTES on `MAP_FIXED` being dangerous |
| **`man 2 madvise`** | The difference between `MADV_DONTNEED` and `MADV_FREE`. **Read it before you use either** |
| **`man 5 proc`** | The `/proc/pid/maps` and `/proc/pid/smaps` sections — the field list is the answer to half of L13 |
| `man 3 mallopt` | `M_MMAP_THRESHOLD` and `M_TRIM_THRESHOLD`, both of which PS 4 asks about |
| `man 2 mprotect` | Short. The ERRORS section is the interesting part |

**And one file to read rather than a page:** `/proc/self/maps`, from a program of your own. It is four lines of C and it will teach you more about what a process is than any single page of any book.

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| Wilson, Johnstone, Neely & Boles, *Dynamic Storage Allocation: A Survey and Critical Review* (1995) | The paper that showed most allocator benchmarks were meaningless. **Directly relevant to PS 4 Q3(c)** |
| Berger, Zorn & McKinley, *Reconsidering Custom Memory Allocation* (2002) | Measures custom allocators against a good general one and mostly finds against them |
| Evans, *A Scalable Concurrent malloc(3) Implementation* (2006) | jemalloc's design paper. Arenas and size classes, motivated |
| `man 2 userfaultfd` | Handling your own page faults from another thread. L15 §3's modern replacement |
| Drepper, *What Every Programmer Should Know About Memory* (2007) | Long, and the TLB and huge-page sections are exactly L15 §6 |

---

## The Habit for This Week

**Ask what the number is per.**

Week 2's habit was to read the limits first; Week 3's was to check that what you enabled is on. This one is about reading measurements. Nearly every result this week is a rate with a hidden denominator, and the denominator is where the understanding is:

- `mmap` beat `read` by 25× — **per byte touched**, on a workload that touches one byte per page. Touch every byte and most of it goes away.
- A minor fault costs 1.9 µs — **per fault**, and file mappings get 132 pages per fault while anonymous ones get one.
- A JIT beat an interpreter by 5.5× — **per operation**, and it tied the C compiler, which had already specialised the same code.
- An allocator beat glibc 0.88× and lost 339× — **per workload**, and the workload was the whole result.

When you read a speedup this week, write down what it is divided by before you believe it. Half the numbers change meaning entirely when you do.

---

*PROG 201 · Week 4 · Reading Guide · © CSE Department*
