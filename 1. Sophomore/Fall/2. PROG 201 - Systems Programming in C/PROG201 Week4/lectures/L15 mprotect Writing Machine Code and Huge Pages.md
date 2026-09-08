# PROG 201 · Systems Programming in C
## Week 4 · Lecture 3 of 3
### `mprotect`, Writing Machine Code, and Huge Pages

---

**Reading:** TLPI §50.2 · CS:APP §3.7 (for the calling convention) · `man 2 mprotect`, `man 2 madvise`, `man 7 sigaction` · **Previous:** L14 · **Next:** Lab 4 — write a JIT, on the Monday of Week 5

---

## 1. `mprotect` Changes the Rules on Memory You Already Have

```c
int mprotect(void *addr, size_t len, int prot);
```

`addr` must be page-aligned, `len` is rounded up, and `prot` is the same `PROT_READ`/`PROT_WRITE`/`PROT_EXEC`/`PROT_NONE` set as `mmap`. It splits the underlying region if you protect part of one, which is why a program that `mprotect`s at page granularity in a loop ends up with thousands of lines in `/proc/pid/maps` and a slower kernel.

What makes it interesting is not the call, it is the pairing: **`mprotect` plus a `SIGSEGV` handler lets a program participate in its own page faults.** Every technique in §2 and §3 is that one idea.

---

## 2. A Guard Page

Protect one page `PROT_NONE` after a buffer and an overrun becomes a crash at the moment it happens rather than corruption discovered an hour later. `protect.c`:

```
1. a 4096-byte buffer with a PROT_NONE page after it
   write at offset  4092: fine
   write at offset  4096: Segmentation fault
   write at offset  4100: Segmentation fault
```

The last valid byte works and the first invalid one dies. That is what a debugging allocator does — Electric Fence, and `MALLOC_PERTURB_`'s more sophisticated descendants, and the `ASAN_OPTIONS=detect_stack_use_after_return` machinery you will meet in Week 10.

**It is not free.** Every guarded allocation costs a whole page of address space for the guard, plus a `vm_area_struct` in the kernel, plus a TLB entry's worth of fragmentation. That is why it is a debugging mode and not the default — and also why thread stacks *do* get a guard page by default (glibc puts one below every thread stack), because there the cost is one page per thread and the failure it catches is a silent corruption of another thread's stack.

---

## 3. A Write Barrier

Now the more interesting direction. Mark a region read-only, catch the `SIGSEGV`, note which page was written, make that page writable, and **return from the handler** — the faulting instruction is retried and succeeds.

```c
static void on_segv(int sig, siginfo_t *si, void *ctx)
{
    long p = ((char *) si->si_addr - region) / page;
    mprotect(region + p * page, page, PROT_READ | PROT_WRITE);
    dirty[p] = 1;
}
```

`SA_SIGINFO` gets you `si->si_addr`, **the faulting address** — that is the whole mechanism. `protect.c` again, over 64 pages:

```
2. write barrier over 64 pages
   7 stores to 4 distinct pages -> 4 faults, 4 pages marked dirty
   dirty set: 0 7 31 63
   (the second store to a page is free -- it is already writable)
```

**Seven stores, four faults.** Each page costs one fault the first time it is written and nothing thereafter, because the handler removed the protection that caused it. You have built, in twenty lines, the thing a generational garbage collector calls a write barrier, an incremental checkpointer calls dirty-page tracking, and a distributed shared memory system calls its coherence protocol.

Three warnings, and the first is Week 0's:

- **The handler must be async-signal-safe** (Week 0 L03 §4). `mprotect` is on the list. `printf` is not, and a handler that logs is a handler that deadlocks.
- **Distinguish your faults from real ones.** The handler above checks the address is inside `region` and `_exit`s otherwise. Without that check, a genuine null-pointer bug becomes an infinite fault loop, because returning from a `SIGSEGV` handler that did not fix anything re-executes the same faulting instruction forever.
- **Linux has a better tool now.** `userfaultfd` lets a *thread* handle another thread's faults on a file descriptor, with no signal handler and no async-signal-safety constraint. It is what live migration and CRIU use. `man 2 userfaultfd` — worth knowing the name.

---

## 4. Writing Machine Code

A JIT is `mmap` with `PROT_EXEC` and a byte array. On x86-64 System V (CS:APP §3.7), the first integer argument arrives in `%rdi` and the return value goes in `%rax`, so a function `long f(long x)` returning `x * 3 + 7` is four instructions:

```
48 89 f8              mov  %rdi,%rax
48 69 c0 03 00 00 00  imul $3,%rax,%rax
48 05    07 00 00 00  add  $7,%rax
c3                    ret
```

Seventeen bytes. `jit0.c` writes exactly those into a mapping and calls it:

```
emitted 17 bytes: 48 89 f8 48 69 c0 03 00 00 00 48 05 07 00 00 00 c3
after mprotect(PROT_READ|PROT_EXEC): f(10) = 37   (expected 37)
                                     f(100) = 307  (expected 307)
```

**That is a compiler.** Not a good one, but the difference between it and LLVM is the front end and the optimiser, not the last step. The last step is `memcpy` into a page you are allowed to jump to.

The shape of every JIT:

```c
unsigned char *code = mmap(NULL, len, PROT_READ | PROT_WRITE,
                           MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
size_t n = emit(code, ...);                     /* fill it in            */
mprotect(code, len, PROT_READ | PROT_EXEC);     /* then make it runnable */
long (*f)(long) = (long (*)(long)) code;        /* the cast C dislikes   */
f(10);
```

Two details that are not obvious:

**The function-pointer cast is not strictly conforming C.** Converting `void *` to a function pointer is undefined behaviour in ISO C; POSIX requires it to work, which is why `dlsym` can exist at all (Week 8). Write it as above and move on, but know why the compiler may warn.

**On some architectures you must flush the instruction cache** after writing code — `__builtin___clear_cache(begin, end)` — because the I-cache and D-cache are not coherent. On x86-64 they are, so it is a no-op there, and code that omits it is portable to exactly one architecture. Lab 4 asks you to put it in anyway.

---

## 5. W^X, and Which Way It Fails

**Write-xor-execute** is the rule that a page should never be both writable and executable, because an attacker who can write to a page they can also execute has won (Week 10). `jit0.c` tests all four corners:

| What | Result |
| --- | --- |
| Call a `PROT_READ\|PROT_WRITE` page | **`SIGSEGV`** — the NX bit |
| Call it after `mprotect(PROT_READ\|PROT_EXEC)` | works |
| Write to a `PROT_READ\|PROT_EXEC` page | **`SIGSEGV`** |
| `mmap(PROT_READ\|PROT_WRITE\|PROT_EXEC)` | **allowed**, and it runs |

The first row is the NX (no-execute) bit doing its job, and it is why the buffer-overflow-into-shellcode attack of the 1990s stopped working — which is what created return-oriented programming, and Week 10.

**The fourth row is the one to notice.** Nothing on this machine stops you asking for a page that is writable *and* executable. Linux will refuse it under SELinux policy, under a `pax`/`grsecurity` kernel, or on OpenBSD by default; here it succeeds silently. **So W^X is a discipline you keep, not a rule the system enforces** — and the discipline is exactly the `mmap`-write-`mprotect` sequence in §4. On Apple silicon it *is* enforced, and a JIT must call `pthread_jit_write_protect_np` to flip a thread between writing and executing; code written the lazy way does not port.

---

## 6. Huge Pages

A 4 KiB page means a 512 MiB region needs 131,072 page-table entries, and the TLB holds a few thousand. Walk that region randomly and nearly every access misses the TLB and pays for a page-table walk.

A **huge page** is 2 MiB backed by one PTE, so the same region needs 256 entries. `hugepage.c` fills 512 MiB and then does 20 million random single-byte reads:

```
MADV_NOHUGEPAGE :   42.7 ns per random page touch (AnonHugePages 0 kB)
MADV_HUGEPAGE   :   32.3 ns per random page touch (AnonHugePages 116736 kB)
speedup: 1.32x
```

**1.32×, from changing nothing but the page size.** And read the second column: only **114 MiB of the 512** actually got huge pages, because transparent huge pages need physically contiguous, aligned 2 MiB blocks and this machine's memory was too fragmented to supply more. A quarter of the region promoted bought a third off the access time; a machine with more free memory would do better.

Three things to know:

- **`/sys/kernel/mm/transparent_hugepage/enabled`** is `always`, `madvise` or `never`. It is `madvise` here, so you get huge pages only where you ask — which is why the `MADV_NOHUGEPAGE` row got zero.
- **`always` is not obviously better.** A huge page that is one byte dirty costs 2 MiB of memory and 2 MiB of I/O to write back. Databases routinely turn THP off for exactly this reason.
- **Explicit huge pages** (`hugetlbfs`, `MAP_HUGETLB`) are reserved at boot and never split or swapped. They are what a database or a hypervisor uses when it wants a guarantee rather than a hint.

This is CS:APP's TLB chapter and CS 201 Week 6's page tables, arriving as a number you can measure.

---

## 7. A Mapping Is a Promise the File Can Break

L13 §5 said `read` wins when you cannot afford a `SIGBUS`. This is why. `truncate.c` maps 64 KiB of a 64 KiB file `MAP_SHARED`, then the file is truncated to 4 KiB:

```
1. mapped 64 KiB of a 64 KiB file; byte 60000 reads 'a'
2. the file was truncated to 4096 bytes under us
   reading byte 60000 now: Bus error
   reading byte 100 (still within the file): fine
```

**A read that worked a moment ago now kills the process**, and nothing in the program changed. The mapping is still there; the pages behind the end of the file are not. Week 2 L08 §6 met `SIGBUS` from a forgotten `ftruncate`; this is the same signal from the other direction, and the general rule covers both:

> **`SIGSEGV` means the address is not mapped. `SIGBUS` means it is mapped and there is nothing behind it.**

You cannot prevent another process truncating a file you have mapped. What you can do:

- **`read` instead of `mmap`** for files you do not control. A short `read` is a return value; a short mapping is a signal.
- **Install a `SIGBUS` handler** with `SA_SIGINFO`, and use `si_addr` to decide whether it was your mapping. Painful, and what a database does.
- **Map only what the file has**, re-`fstat` before extending, and accept that the check is racy.

---

## 8. Memory-Mapped I/O

The last thing `mmap` maps is not memory at all. A device's control registers are placed in the physical address space by the bus, and a driver reaches them by mapping those physical addresses — so `*(volatile uint32_t *)(base + 0x18) = 1` becomes a bus transaction to a piece of hardware.

From userspace that is `/dev/mem` (root only, and mostly disabled), or a UIO or VFIO device, and it is how DPDK talks to a network card without the kernel in the path.

Two rules if you ever do it:

- **`volatile` is mandatory.** The compiler must not cache a register read or reorder two writes; a status register can change without your program touching it.
- **`volatile` is not enough.** It stops the *compiler* reordering, not the CPU or the bus. Real drivers use `readl`/`writel`, which carry the necessary barriers.

The reason it is in this lecture is the unification, which is one of Unix's genuinely elegant ideas: **a file, a chunk of anonymous memory, a shared region between processes, and a hardware register are all the same interface.** `mmap` a thing, get a pointer, use it. Week 7's filesystem and Week 11's containers are both built on the same trick.

---

## Summary

- `mprotect` changes permissions on memory you already have, at page granularity, and splits regions when you use it piecemeal.
- **A `PROT_NONE` guard page** turns an overrun into a crash at the point of the bug. glibc puts one below every thread stack.
- **`mprotect` + a `SIGSEGV` handler + `si_addr` is a write barrier**: 7 stores to 4 pages cost 4 faults, and the second store to a page is free. Handlers must be async-signal-safe and must check the address is theirs.
- **A JIT is 17 bytes and an `mprotect`.** Write to a `PROT_WRITE` mapping, flip it to `PROT_EXEC`, cast, call.
- **W^X fails safe in three directions and is not enforced in the fourth**: calling a writable page and writing an executable page both `SIGSEGV`, and `PROT_WRITE|PROT_EXEC` is simply allowed here. Keep the discipline anyway.
- **Huge pages: 42.7 ns → 32.3 ns**, 1.32×, with only 114 MiB of 512 promoted. THP is `madvise`-only on these machines.
- **A mapped file can be truncated under you and reading it then raises `SIGBUS`.** `SIGSEGV` = not mapped; `SIGBUS` = mapped, nothing behind it.
- Device registers are mapped the same way. `volatile` is necessary and not sufficient.

---

## Exercises

1. Put a guard page *before* a buffer as well as after. Which class of bug does each one catch, and which does neither?
2. Extend §3's write barrier to make a copy of a page before letting the write through, then compare the copy with the page at the end. You have written a checkpointer.
3. Remove the address check from `on_segv` and dereference a null pointer. Describe exactly what happens and why it never ends.
4. Extend `jit0.c` to emit `x*a + b` for values read from `argv`. Then emit a loop, and be careful about the encoding of a backward `jmp`.
5. Time a call to the JIT-ed function against the same expression written in C and compiled with `-O2`. Explain the result.
6. Re-run §6 with 64 MiB instead of 512 MiB and then with 2 GiB. Where does the huge-page advantage appear and where does it vanish?
7. Map a file, have another process truncate it, and catch the `SIGBUS` with `SA_SIGINFO`. Print `si_addr` and work out which page it was.
8. `cat /proc/self/maps | wc -l`, then `mprotect` every other page of a 1,000-page mapping and count again. What did you do to the kernel?

---

*PROG 201 · Week 4 · L15 · © CSE Department*
