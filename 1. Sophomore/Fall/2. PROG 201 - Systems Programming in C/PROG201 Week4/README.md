# PROG 201 · Systems Programming in C
## Week 4: Memory-Mapped Files and the Virtual Memory API

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101; CS 201 as co-requisite
**Assessment for this course (overall):** Problem Sets 35%, Projects 25%, Midterms 25%, Final 15%
**This week's deliverables:** **Midterm 1** (Monday, 18:00–19:30, Weeks 0–3, 12.5%), PS 4 (due Friday of Week 5) and **Quiz 4** (Tuesday, covers Week 3).
**Lab 3 is sat on the Monday of this week**; **Lab 4 covers this week and is sat on the Monday of Week 5**.

> ### **Midterm 1 is the Monday of this week**, 18:00–19:30, covering **Weeks 0–3** — 12.5% of the course.
> Lab 3 is sat that same afternoon and ends at 16:50. Nothing in Week 4 is on the paper. Marked
> scripts come back in Tuesday's lecture, before Quiz 4.

---

### Why This Week Exists

Because `malloc` is not a system call, `[heap]` is not a thing, and a compiler is `mmap` plus seventeen bytes.

Weeks 0–3 built processes, descriptors, IPC and threads on top of memory that simply existed. **This week is where the memory comes from** — and the answer turns out to be one system call that also explains how programs are loaded, how files are read without copying, how a debugger catches an overrun, and how a JIT works.

Three ideas:

1. **Address space is free and memory is not.** Mapping 4 GiB costs nothing; reading a gigabyte of it costs nothing; *writing* it costs a gigabyte. The difference is one shared page of zeroes and the copy-on-write machinery from Week 0.
2. **`malloc` is a library function**, and after PS 4 it stops being magic. It is a header, an alignment rule, a fit policy and a merge rule — roughly 150 lines, which will beat glibc on two workloads and lose by **339×** on a third.
3. **The last step of a compiler is `memcpy` into a page you are allowed to jump to.** Lab 4 is 51 bytes of x86-64 and an `mprotect`.

---

### Learning Objectives

By the end of Week 4, you should be able to:

1. Read `/proc/pid/maps` and say what each line is and who made it.
2. Choose correctly among the four combinations of `MAP_PRIVATE`/`MAP_SHARED` and file-backed/anonymous.
3. **Explain why `MAP_PRIVATE` writes to a file never reach the file**, and predict it before testing.
4. Distinguish `VmSize`, `VmRSS` and `Pss`, and say which to quote.
5. Explain demand paging, the shared zero page, and what `MADV_DONTNEED` destroys.
6. Quantify a minor fault, a major fault and a store to a resident page, and say why file mappings fault in batches.
7. Say when `mmap` beats `read` and when it does not, with a reason that is not "`mmap` is faster".
8. Describe what `brk` does and why it is not enough.
9. Describe glibc's chunks, bins and `tcache`, and explain the `mmap` threshold and why it moves.
10. **Write an allocator**: header, alignment, first fit, splitting, coalescing, large-block mappings.
11. Explain internal and external fragmentation, and why C cannot compact.
12. Use `mprotect` with a `SIGSEGV` handler to build a guard page and a write barrier.
13. **Generate and execute machine code at runtime**, and state the W^X discipline and where it is not enforced.
14. Say what huge pages buy, and what they cost.
15. Distinguish `SIGSEGV` from `SIGBUS` and name a cause of each.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L13 mmap and What a Mapping Costs]] | Every region is an `mmap`; the four combinations; **4 GiB mapped for 1 MiB of RSS**; the shared zero page; minor 1.9 µs against major 563 µs; file mappings fault **132 pages at a time**; `mmap` against `read`, both directions |
| [[L14 Where Memory Comes From brk mmap and malloc]] | There is no heap; `brk`'s one number; chunks, bins and `tcache`; **the threshold measured at 134,473 not 131,072**; building an allocator; coalescing; **339× on the wrong workload**; fragmentation |
| [[L15 mprotect Writing Machine Code and Huge Pages]] | Guard pages; **a write barrier in twenty lines**; a JIT in 17 bytes; the four corners of W^X and the one that is not enforced; huge pages at **1.32×**; `SIGBUS` from a truncated file; device registers |
| [[LAB 4 Writing a JIT]] | Emit x86-64, make it runnable, call it, and measure it. **Monday of Week 5** |
| `lab/jit.c`, `lab/Makefile` | The skeleton — it already generates and calls machine code |
| [[PS 4 An Allocator Built on mmap]] | Write `malloc`. Then break it, measure it, and account for the fragmentation. Due **Friday of Week 5** |
| [[PROG201 Week4/assignments/QUIZ 4 Week 4 Tuesday\|QUIZ 4 Week 4 Tuesday]] | Ten minutes, covers **Week 3**, answer key printed |
| [[PROG201 Week4/resources/Reading Guide Week 4\|Reading Guide Week 4]] | **CS:APP Ch. 9 is the book this week**, plus TLPI Ch. 49 and the man pages |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Ask what the number is per.**

Every headline this week is a ratio with a denominator that changes what it means:

| The number | What it is per | What happens when you change that |
| --- | --- | --- |
| `mmap` beat `read` **25×** | per byte *touched*, one per page | touch every byte and most of it vanishes |
| a minor fault is **1.9 µs** | per fault | file mappings get 132 pages per fault, anonymous get 1 |
| readahead: **0.17 s vs 1.58 s** | per access *order* | same file, same bytes, 8.5× apart |
| a JIT beat an interpreter **5.5×** | per operation dispatched | against the C compiler it ties |
| an allocator beat glibc **0.88×** | per workload | on the next workload it loses **339×** |

**The 339× is the one to carry.** A 150-line allocator really is faster than glibc on two of three workloads, and catastrophically worse on the third — and nothing about the code changed between them. It is Week 2's shared-memory result and PS 2's untorn records arriving a third time: **a measurement that flatters your implementation is a fact about your test.**

---

### Assessment Reminder

**Midterm 1 is Monday, 18:00–19:30, and is worth 12.5%.** It covers **Weeks 0–3** and nothing from this week.

**Labs and quizzes carry no weight** and are still required. **Quiz 4 is at the start of Tuesday's lecture and covers Week 3**; the answer key is printed in the paper.

> **Two labs touch this week.** **Lab 3** — Week 3's priority inversion — is sat on the **Monday of
> this week**, ending seventy minutes before the midterm. **Lab 4** covers this week and is sat on
> the **Monday of Week 5**.

Both are tracked in [[_PROG 201 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 0's copy-on-write is L13 §3**, and this time you can watch RSS move. **Week 2 L08's `SIGBUS`** — a forgotten `ftruncate` — is L15 §7 from the other direction, a file truncated under a live mapping. **Week 0 L03's async-signal-safety** governs L15 §3's fault handler. **Week 3's `tcache`** is why `malloc` in a signal handler did not deadlock, and L14 §3 says why.

**Sideways:** **CS 201 Week 4 is the memory hierarchy and CS 201 Week 6 is the page table** — this week is the same machinery from the system-call side. L15 §6's huge pages are CS 201's TLB, measured.

**Forward:** **Week 5's server** uses `mmap` to send files without copying (`sendfile` is the same idea taken further). **Week 7's filesystem** is the page cache these mappings sit on. **Week 8's dynamic linker** makes most of the `mmap` calls in `/proc/self/maps`, and its GOT patching is Lab 4's backpatching problem. **Week 10's ROP** is the fourth corner of L15 §5, used against you.

---

*PROG 201 · Week 4 · © CSE Department*
