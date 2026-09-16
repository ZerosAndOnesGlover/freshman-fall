# CS 202 · Project 2
## xv6: Memory and File System Features

---

**Assigned:** Week 9, Wednesday · **Due:** **Friday of the completion period, 17:00** · **15% of the course**
**Checkpoints:** Part A in the **Week 10 lab**; Part B in the **Week 12 lab** — unmarked, recorded by the TA
**Submit:** a patch against the pinned xv6 (`git diff`), plus a report, `P2_{LastName}_{StudentID}.pdf`

> Collaboration: the kernel code and the report must be yours. **Discussing designs is fine; sharing
> code is not.** State at the top of your report: *"I worked on this project independently"* or name
> who you discussed what with.

---

## What You Are Building

**Three features, in the kernel you have been reading all term**, each fixing something the course has already shown you is missing:

| Part | Feature | The lecture that showed the gap |
|---|---|---|
| **A** | **Lazy allocation**: `sbrk` gives addresses, the page fault gives pages | L18 §5 — xv6 allocates eagerly, Linux does not |
| **B** | **Large files**: a double-indirect block | L22 §3 — xv6's largest file is 71,680 bytes |
| **C** | **Symbolic links**: a file whose contents are a path | L24 §4 — hard links exist; soft links do not |
| **D** | **Measurements and a write-up** | every week of this course |

**Build on your Project 1 tree if you like, or start from a clean pinned xv6** — say which in your report. **If you start from Project 1, watch your system-call numbers**: Project 1 used two, and Part C adds another. *(This is not a hypothetical. See "Two warnings", below.)*

---

## Part A — Lazy Allocation (25 marks)

**`sbrk(n)` currently allocates and zeroes *n* bytes of pages before returning.** Make it move the process's size and allocate nothing; **allocate a page in the page-fault handler**, when the process first touches it.

**Requirements:**

1. **`sys_sbrk`** grows `myproc()->sz` without calling `growproc` for positive *n*. **Negative `sbrk` must still free**, as now.
2. **The fault handler** allocates a zeroed page for a fault that is (a) from user mode, (b) **not present** — check the error code — and (c) at an address **below the process's size** and above the first page. **Anything else must still kill the process**, printing xv6's usual message.
3. **`copyuvm` must skip pages that were never touched**: a `fork` after a lazy `sbrk` must not panic on a missing page-table entry.
4. **`copyout` must work for a lazily allocated page** — a `read()` into fresh memory is the case that catches most implementations.

**Your kernel must still pass `usertests`.**

**Marks:** 10 for `sbrk` and the fault handler; 6 for the checks that keep genuine faults fatal; 5 for `fork`; 4 for `usertests`.

---

## Part B — Large Files (30 marks)

**Add a double-indirect block**, as Unix does: the last address in the inode points at a block of pointers to blocks of pointers.

**Requirements:**

1. `NDIRECT` becomes **11**, and `addrs[]` gains an entry, so that the inode is the same size. **Say in your report why the inode's size must not change.**
2. **`bmap`** resolves block numbers through the new level, allocating both levels on demand.
3. **`itrunc`** frees both levels — **every block, and no block twice.**
4. `FSSIZE` in `param.h` must be large enough to hold a maximal file; say what you chose and why.

**Verify it**: write a file until `write` fails, report the size, **and read every block back**, checking the contents.

**Marks:** 10 for `bmap`; 10 for `itrunc` (a leak here is invisible until the disk fills); 5 for the size arithmetic in your report; 5 for the write-then-read-back test.

---

## Part C — Symbolic Links (25 marks)

**A symbolic link is a file whose contents are a path**, and which `open` follows.

**Requirements:**

1. A new inode type **`T_SYMLINK`**, a new system call **`symlink(target, path)`**, and a new flag **`O_NOFOLLOW`** in `fcntl.h`.
2. **`open` follows a link** to what it names, and follows a chain of links.
3. **`open` with `O_NOFOLLOW` opens the link itself** — reading it then gives the target path.
4. **A loop must not hang the kernel**: follow at most a fixed number of links, then fail. Say what limit you chose.
5. The target need not exist when the link is created. **Say what happens when it does not, and why that is the right answer.**

**Marks:** 8 for the system call; 10 for the follow logic in `open`; 4 for `O_NOFOLLOW`; 3 for loop handling.

---

## Part D — Measurements and Write-Up (20 marks)

**Your report must show that each part works, with numbers rather than assertions.**

**(a) [7]** **Lazy allocation.** Using a way of counting free pages — Week 5's `nfree` patch is in `CS202 Week5/resources/`, or add your own — report the free-page count **before `sbrk`, after `sbrk` of several megabytes, and after touching a few pages.** Then: **how many page faults does touching *n* pages cost**, and what does the first read of an untouched page return?

**(b) [7]** **Large files.** Report **the largest file your kernel can hold**, derived from your constants *and* measured by writing until `write` fails. **Account for every block** of a maximal file: data, indirect, double indirect.

**(c) [3]** **Symbolic links.** Show a link followed, the same link opened with `O_NOFOLLOW`, and a loop refused.

**(d) [3]** **One paragraph on what went wrong.** The bug that took longest, and how you found it. **This is marked**, and an honest paragraph earns full marks.

---

## Two Warnings, From Building the Reference

**These cost the instructor an hour between them; they will cost you longer.**

1. **System-call numbers collide silently.** If your tree already defines `SYS_getpinfo 23` from Project 1 and you add `SYS_symlink 23`, **the kernel will run whichever entry the table holds and your call will return the wrong thing** — not an error. The symptom in the reference was `symlink()` returning **56790**, which was a free-page count from another call. **Check `syscall.h` against `usys.S` whenever you add a call.**
2. **xv6's `Makefile` does not rebuild `usys.o` when `syscall.h` changes.** Your new system call will assemble with the **old** number, and every symptom will point at the kernel. **Run `make clean` after touching `syscall.h`**, always.

---

## What to Hand In

```bash
cd ~/xv6-public
git diff > P2_{LastName}.patch          # every kernel change, including new files (git add -N first)
```

**The TA applies your patch to a clean pinned xv6** with Lab 0's two `Makefile` changes, runs `make clean && make qemu-nox`, then `usertests` and your three test programs. **A patch that does not apply or does not build scores zero for the parts it contains**, so check it the way the TA will:

```bash
git clone https://github.com/mit-pdos/xv6-public.git /tmp/check && cd /tmp/check
git checkout eeb7b415dbcb12cc362d0783e41c3d1f44066b17
sed -i 's/-m32 -Werror/-m32 -Werror -Wno-error=array-bounds -Wno-error=infinite-recursion/' Makefile
sed -i 's/-smp $(CPUS)/-smp $(CPUS),sockets=$(CPUS),cores=1,threads=1/' Makefile
git apply ~/P2_{LastName}.patch && make clean && make qemu-nox
```

**Include your test programs in the patch**, and name them in the report.

---

## Marks

| Part | Topic | Marks |
|---|---|---:|
| A | Lazy allocation | 25 |
| B | Large files | 30 |
| C | Symbolic links | 25 |
| D | Measurements and write-up | 20 |
| | **Total** | **100** *(15% of the course)* |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **There is no dropped project**, and the completion-period deadline is the last one of the term.

---

## Where to Look

| For | Read |
|---|---|
| what a page fault carries, and how xv6 handles one | **L18 §2**; `trap.c`'s `default:` case, `rcr2()` |
| why `copyuvm` must tolerate missing pages | **L18 §4–§5**; `vm.c` |
| the inode's block addresses, and the arithmetic | **L22 §3**; `fs.h`, `bmap` and `itrunc` in `fs.c` |
| how `open` resolves a path | **L22 §5**; `namei`, `sys_open` in `sysfile.c` |
| adding a system call, end to end | **Week 0 L03**; Project 1's Part A |
| counting free pages | `CS202 Week5/resources/nfree.patch` |

---

*CS 202 · Week 9 · Project 2 · © CSE Department*
