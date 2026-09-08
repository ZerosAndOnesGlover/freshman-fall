# PROG 201 · Quiz 5
## Administered: Tuesday, Week 5 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 4** — `mmap`, demand paging, where `malloc` gets memory, `mprotect`, JIT compilation, huge pages.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.

---

**Q1.** You `mmap` 4 GiB anonymously on a machine with 2 GiB free, and it succeeds. Then you read every page of the first gibibyte and RSS does not move. Explain both.

&nbsp;

&nbsp;

---

**Q2.** Name the three system calls that set up POSIX shared memory, in order, and say which omission gives `SIGBUS` rather than `SIGSEGV`.

&nbsp;

&nbsp;

---

**Q3.** A minor fault costs about 1.9 µs and a store to a resident page about 19 ns. Where does the 1.9 µs go? Name two things the kernel must do.

&nbsp;

&nbsp;

---

**Q4.** The same cold 256 MiB file took 0.17 s to walk forwards and 1.58 s to walk in random order. What is the mechanism, and which `madvise` call would you use for each walk?

&nbsp;

&nbsp;

---

**Q5.** `malloc(131072)` comes from the heap and `malloc(262144)` comes from its own mapping. Name the knob, give its documented value, and say why the measured boundary was 134,473.

&nbsp;

&nbsp;

---

**Q6.** Your 150-line allocator beats glibc on two workloads and loses by 339× on a third. What is special about the third, and what is the general lesson?

&nbsp;

&nbsp;

---

**Q7.** Write the three steps of a JIT, in order. Then say which of them the machine will let you skip, and why you should not.

&nbsp;

&nbsp;

---
---

# Answer Key

*Mark your own. Be honest — nobody else will see this.*

---

**Q1.** **The `mmap` succeeded because address space is not memory** — the kernel recorded a range and its permissions and allocated nothing. **The reads cost nothing because an untouched anonymous page resolves to the shared zero page**, one physical page of zeroes mapped read-only wherever a fresh anonymous page is read. RSS moves only on the first *write* to each page — copy-on-write, the same mechanism as `fork`. Measured: 4 GiB mapped → RSS 1 MiB; reading 1 GiB → RSS 1 MiB; writing it → **1,025 MiB**. *(L13 §3.)*

---

**Q2.** **`shm_open`, `ftruncate`, `mmap`.** Skipping **`ftruncate`** gives `SIGBUS`: the object is created zero-length, `mmap` does not check the length, and the first touch finds a mapping with nothing behind it. `SIGSEGV` means the address is not mapped; **`SIGBUS` means it is mapped and there is nothing behind it**. *(Week 2 L08 §5–§6; Week 4 L15 §7 is the same signal from a truncated file.)*

---

**Q3.** Any two of: **find a free physical page**; **zero it** (you must not be handed another process's data); **install the page-table entry**; take the mmap lock; account it to the cgroup. The zeroing is the one people forget and it is the reason the fault costs a hundred times a store. *(L13 §4.)*

---

**Q4.** **Readahead.** Walking forward, the kernel detects the pattern and pulls pages in ahead of you, so almost nothing becomes a *major* fault — 65,536 would-be major faults became **2,051 minor and 1 major**. Jumping around defeats the detector and every miss costs a disk read at ~563 µs.

`MADV_SEQUENTIAL` for the forward walk; **`MADV_RANDOM`** for the other, which stops the kernel reading 128 KiB around every access you will never use. *(L13 §4, §6.)*

---

**Q5.** **`M_MMAP_THRESHOLD`**, documented as **128 KiB (131,072)**. The measured boundary was **134,473** because the threshold is compared against the **chunk** size — your request plus a header, rounded — and only after the allocator has failed to satisfy you from the top chunk, which glibc had already grown to 132 KiB. It also **adapts upward at runtime**, to as much as 32 MiB, when it sees large blocks freed. *(L14 §4.)*

---

**Q6.** The third workload allocates 40,000 blocks, frees every other one, and allocates again — so it builds a **free list of 20,000 blocks** and then allocates from it 20,000 times. First fit is *O(n)* per allocation and an address-sorted insert is *O(n)* per free, so it is *O(n²)* with n = 20,000. glibc bins by size and is *O(1)*.

The general lesson: **a measurement that flatters your implementation is a fact about your test.** Same as Week 2's shared-memory result and PS 2's untorn records. *(L14 §7.)*

---

**Q7.** **(1)** `mmap` a page `PROT_READ|PROT_WRITE`; **(2)** write the machine code into it; **(3)** `mprotect` it to `PROT_READ|PROT_EXEC` and call it.

**You can skip step 3 by asking for `PROT_WRITE|PROT_EXEC` in step 1, and this machine allows it.** You should not: W^X is enforced by SELinux, by OpenBSD, and by Apple silicon, so the shortcut does not port — and a code page that stays writable turns any memory-corruption bug in your emitter into arbitrary code execution. *(L15 §4–§5.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| **Q1** | **L13 §3** — and run `rss.c` yourself; it is the clearest thing in the week |
| Q2 | Week 2 L08 §5–§6, and L15 §7 |
| Q3, Q4 | L13 §4 |
| **Q5, Q6** | **L14 §4 and §7** — PS 4 is due Friday and Q6 is its Q3(b) |
| Q7 | L15 §4–§5, and Lab 4 was Monday |

**Q6 is the one that recurs**, and it has now appeared in three different weeks with three different mechanisms. This week it arrives a fourth time: Lab 5's "Hello, world" benchmark makes an iterative server look faster than an event-driven one.

---

*PROG 201 · Week 5 · Quiz 5 · covers Week 4 · ungraded*
