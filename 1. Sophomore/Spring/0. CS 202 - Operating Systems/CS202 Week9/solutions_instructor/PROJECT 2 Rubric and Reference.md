# CS 202 · Project 2 — Rubric, Reference and Marking Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Assigned Week 9 Wednesday; Part A shown in the Week 10 lab, Part B in the Week 12 lab; due Friday of the completion period. 15% of the course.**

**The reference** is `project 2 reference (do not distribute).patch` in this folder, with `lazytest.c`, `bigfile.c` and `symtest.c`. **It was verified by applying it to a clean clone of the pinned commit** with Lab 0's two `Makefile` changes, building from clean, and running all three tests.

```bash
git clone https://github.com/mit-pdos/xv6-public.git check && cd check
git checkout eeb7b415dbcb12cc362d0783e41c3d1f44066b17
sed -i 's/-m32 -Werror/-m32 -Werror -Wno-error=array-bounds -Wno-error=infinite-recursion/' Makefile
sed -i 's/-smp $(CPUS)/-smp $(CPUS),sockets=$(CPUS),cores=1,threads=1/' Makefile
git apply STUDENT.patch && make clean && make qemu-nox
```

---

## Reference measurements

**Part A — lazy allocation** (`lazytest`):

```
free 56790 -> 56790 after sbrk(4 MB) (0 pages), -> 56774 after touching 16 pages (16 pages)
reading an untouched page inside the region gives 0
```

**`sbrk(4 MB)` costs nothing; sixteen touched pages cost exactly sixteen**, and an untouched page reads as zero. *(The free-page count comes from Week 5's `nfree` patch, which the handout points students at.)*

**Part B — large files** (`bigfile`, with `FSSIZE` raised to 20,000):

```
wrote 16523 blocks = 8459776 bytes, then write returned -1
read 16523 blocks back correctly
```

**Exactly (11 + 128 + 128 × 128) × 512 = 8,459,776.** A student whose number is 8,460,288 has kept `NDIRECT` at 12 **and grown the inode**, which is a different design — see the marking note below.

**Part C — symbolic links** (`symtest`):

```
open(a, O_CREATE) = 3
symlink(a, b) = 0
open(b, O_NOFOLLOW) = 3
  the link inode: type 4, size 2
  it contains 2 bytes: "a"
open(b) following the link = 3
  read 21 bytes: hello through a link
open of a symlink loop = -1 (should be -1)
```

---

## The reference, in brief

**Part A.** `sys_sbrk` adds to `myproc()->sz` for positive *n* and calls `growproc` only to shrink. `trap.c` gains a `T_PGFLT` case **before** the `default:` one:

```c
    if(curproc != 0 && (tf->cs & 3) == 3 && (tf->err & 1) == 0 && va < curproc->sz && va >= PGSIZE){
      char *mem = kalloc();
      ...
      mappages(curproc->pgdir, (char*)PGROUNDDOWN(va), PGSIZE, V2P(mem), PTE_W|PTE_U)
```

**The three conditions are the marks**: user mode, **not present** (`err & 1` clear — otherwise a protection fault on the guard page would be "fixed" by mapping over it), and inside the process's size. `copyuvm` gains two `continue`s for absent entries, and `mappages` loses its `static`.

**Part B.** `NDIRECT` 11, `addrs[NDIRECT+2]`, a third branch in `bmap`, and a third loop in `itrunc`. **`FSSIZE` 20,000** so that a maximal file fits.

**Part C.** `T_SYMLINK` in `stat.h`, `O_NOFOLLOW` in `fcntl.h`, `sys_symlink` writing the target into the inode's data, and a follow loop in `sys_open` bounded at **10**.

---

## Marking

| Part | Item | Marks | Look for |
|---|---|---:|---|
| **A** | `sbrk` + fault handler | 10 | a page allocated on the fault, not in `sbrk` |
| | the checks | 6 | **`err & 1`** — without it, a guard-page write is silently granted, which is a security bug, not a style point |
| | `fork` | 5 | `copyuvm` skipping absent entries |
| | `usertests` | 4 | run it; it catches `copyout` |
| **B** | `bmap` | 10 | both levels allocated on demand |
| | `itrunc` | 10 | **every block freed once** — check with a write/delete loop and a free-page count |
| | the arithmetic | 5 | 8,459,776, derived |
| | write-and-read-back | 5 | the read-back is what catches a wrong index calculation |
| **C** | `symlink` | 8 | target written into the inode; no requirement that it exist |
| | follow in `open` | 10 | chains followed; inode locks released before `namei` |
| | `O_NOFOLLOW` | 4 | opens the link itself |
| | loop bound | 3 | a limit, not a cycle detector |
| **D** | (a) 7, (b) 7, (c) 3, (d) 3 | 20 | **numbers, not assertions**; (d) is marked and an honest answer earns it |

### Common failures

| Symptom | Cause | Marks |
|---|---|---|
| `usertests` fails in `sbrk` tests; `copyout` returns −1 | the fault handler does not cover kernel access to a lazy page | A: at most 15 |
| a write to the stack guard page succeeds | missing `err & 1` check | A: −6, and say why in feedback |
| `bigfile` reports 8,460,288 bytes | `NDIRECT` left at 12 and the inode grown to `addrs[14]` | **accept with a note**: the inode no longer divides `BSIZE` evenly, so `IPB` changes; if `IPB` was not updated, the file system is corrupt — check `fsck`-like behaviour |
| a maximal file writes but reads back wrong past 71,680 bytes | double-indirect index arithmetic (`bn / NINDIRECT` vs `bn % NINDIRECT`) | B: −8 |
| disk fills after repeated create/delete of large files | `itrunc` not freeing the second level | B: −10 |
| `symlink()` returns a plausible number and no link appears | **system-call number collision** (see below) | not a marking issue — help them find it |
| `open` of a link loop hangs the kernel | no bound | C: −3 |

### The two traps the handout warns about

**Both were hit while building the reference, and both look like kernel bugs:**

1. **A number collision.** This tree already had Week 5's `nfree` at 22; the new `SYS_symlink` was also given 22, and `symlink()` returned **56790** — a free-page count. **Students merging Project 1 (which used 22 and 23) will hit exactly this.**
2. **A stale `usys.o`.** xv6's `Makefile` does not rebuild `usys.S` when `syscall.h` changes, so the stub kept the old number (`mov $0x16` where `$0x17` was expected) **through three edit-build-test rounds**. `objdump -d usys.o | grep -A2 '<symlink>:'` is the fastest check; `make clean` is the fix.

**Tell the Week 10 lab about both**, before the checkpoint.

### A part that is not in this project

**Copy-on-write `fork` was implemented as a candidate Part C and abandoned**: the reference panicked at boot (`init` trapping at `eip 0x1010101`) and the cause was not found within the time available. **It is therefore not asked for**, and no marks anywhere depend on it. If a student implements it anyway as an extension, **mark it generously in D(d)** and ask to see `usertests` pass.

---

*CS 202 · Week 9 · Project 2 Rubric · Instructor Only*
