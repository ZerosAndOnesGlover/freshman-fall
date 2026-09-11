# CS 202 · Operating Systems
## Week 1 · Lecture 3 of 3
### Address Spaces, and a Process from `fork` to `wait`

---

**Sat:** Friday of Week 1, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 5; xv6 book Ch. 1 and `exec.c` · **Next:** Week 2, scheduling

---

## 1. Every Process Is Shown the Same Map

L04 said the kernel keeps a pointer to each process's page table. **This lecture is what that page table describes**: the address space, the private map of memory every process believes it has to itself.

`layout.c` prints the address of one thing from each region, on the reference machine:

| What | Where it lives | Address (run 1) |
|---|---|---:|
| `main` | **text** — the program's code | `0x5808cd347180` |
| a string literal | **rodata** — read-only data | `0x5808cd3480d2` |
| `int initialised = 42;` | **data** — initialised globals | `0x5808cd34a010` |
| `int uninitialised;` | **bss** — zero-initialised globals | `0x5808cd34a02c` |
| `malloc(64)` | **heap** — grown with `brk` | `0x58090be222a0` |
| `malloc(64 MiB)` | **an anonymous `mmap`** | `0x71cbd3bff010` |
| `printf` | **libc's text**, mapped by the dynamic linker | `0x71cbd7c60100` |
| the vDSO | **kernel-provided code**, L03 §4 | `0x71cbd8017000` |
| a local variable | **stack** | `0x7ffc2a760c2c` |

**Read the column from top to bottom and the addresses rise**: the program at the bottom, then its data, the heap growing upward from just above it, a very large gap, the shared libraries and mappings, and the stack near the top of the user half. This is the picture CS 201 Week 6 drew, and here it is with numbers.

**The largest gap is the point.** Between the heap at `0x5809…` and the mappings at `0x71cb…` there are about **30 TiB of address space with nothing in it.** It costs nothing — no page-table entries, no memory — and it gives the heap and the mappings room to grow towards each other for the life of the process.

`/proc/<pid>/maps` lists every region the kernel is keeping, one per line. Trimmed:

```
55be1c7f4000-55be1c7f5000 r--p 00000000 103:02 3541309   ./layout      ELF header
55be1c7f5000-55be1c7f6000 r-xp 00001000 103:02 3541309   ./layout      text
55be1c7f6000-55be1c7f8000 r--p 00002000 103:02 3541309   ./layout      rodata, relro
55be1c7f8000-55be1c7f9000 rw-p 00003000 103:02 3541309   ./layout      data + bss
55be4fe01000-55be4fe22000 rw-p 00000000 00:00 0          [heap]
7e78f51ff000-7e78f9200000 rw-p 00000000 00:00 0          the 64 MiB malloc
7e78f9200000-7e78f9405000 ...                            /usr/lib/x86_64-linux-gnu/libc.so.6  (5 lines)
7e78f9592000-7e78f9598000 r--p 00000000 00:00 0          [vvar] [vvar_vclock]
7e78f9598000-7e78f959a000 r-xp 00000000 00:00 0          [vdso]
7e78f959a000-7e78f95d4000 ...                            ld-linux-x86-64.so.2  (5 lines)
7ffdb6679000-7ffdb669b000 rw-p 00000000 00:00 0          [stack]
ffffffffff600000-ffffffffff601000 --xp 00000000 00:00 0  [vsyscall]
```

**Each line's permission column is the enforcement.** Text is `r-x` and not `w`: a stray write to your own code is a `SIGSEGV`. Data is `rw-` and not `x`: a buffer overflow cannot simply jump into what it wrote. These are the page-table bits of Week 5, set per region.

---

## 2. The Map Moves Every Time

Run `layout.c` three times:

| What | Run 1 | Run 2 | Run 3 |
|---|---:|---:|---:|
| `main` | `0x5808cd347180` | `0x5f2b88394180` | `0x6335b2e84180` |
| heap | `0x58090be222a0` | `0x5f2b88aee2a0` | `0x6335c3e052a0` |
| `printf` | `0x71cbd7c60100` | `0x794634e60100` | `0x72ada7e60100` |
| stack | `0x7ffc2a760c2c` | `0x7ffda240423c` | `0x7fff5ec4685c` |

**Every region moves between runs, and the low three hex digits never do** — `…180`, `…2a0`, `…100` — because randomisation moves whole pages, and the offset within the page is fixed by the program. This is **address-space layout randomisation**, controlled by `/proc/sys/kernel/randomize_va_space`, which is **2** here: stack, mappings, heap and the program itself are all randomised.

**It can be turned off for one process**, without privilege:

```
$ setarch -R ./layout
main (text)                    0x555555555180
$ setarch -R ./layout
main (text)                    0x555555555180
```

**`0x555555555180`, both times.** That is the kernel's default load address for a position-independent executable, plus `main`'s offset. Debuggers turn randomisation off exactly this way, so that an address you wrote down in the last run still means something.

**Why randomise at all?** An attacker who has found a bug that lets them overwrite a return address needs to know *what address to write*. If `printf` is at a different place on every run, a hard-coded address is wrong almost every time. ASLR does not fix the bug; it makes exploiting it a guess. **Week 12 measures how good the guess is.**

---

## 3. Address Space Is Not Memory

`rss.c` maps 256 MiB and then writes to it a quarter at a time, printing two lines of `/proc/self/status` after each step:

| After | `VmSize` | `VmRSS` |
|---|---:|---:|
| start | 2,692 kB | 1,428 kB |
| **`mmap` 256 MiB** | **264,836 kB** | **1,428 kB** |
| touching ¼ | 264,836 kB | 67,028 kB |
| touching ½ | 264,836 kB | 132,564 kB |
| touching ¾ | 264,836 kB | 198,100 kB |
| touching all | 264,836 kB | 263,636 kB |
| `munmap` | 2,692 kB | 1,492 kB |

**`VmSize` is the address space: it grew by 256 MiB the moment the call returned. `VmRSS` is the memory actually in RAM — the *resident set* — and it did not move at all until the program wrote.** Then it rose by 64 MiB per quarter, exactly as much as was touched.

**This is L01's 24,353 GiB against 7.5 GiB, in one process.** Every page of a fresh mapping is a promise; the kernel keeps it by allocating a frame on the first access, in a page fault. Week 5 is how the translation works and Week 6 is what happens when the promises exceed the RAM.

---

## 4. Where the Map Comes From: `exec`

A process's address space is built by **`exec`**, which throws away whatever was there before and constructs a new one from an ELF file:

1. **Read the ELF program headers.** Each `LOAD` segment says: map this range of the file at this address with these permissions. That is where the four `./layout` lines of `maps` came from.
2. **Set up the heap** as an empty region just above the data, which `brk` will grow.
3. **If the program is dynamically linked, map the dynamic linker** and arrange to start there instead of at `main`. The linker then maps libc — the five `libc.so.6` lines.
4. **Build the stack**: copy `argv` and the environment strings to the top, then an array of pointers to them, then `argc`.
5. **Set the saved user registers** so that the return to user space lands at the entry point with the stack pointer at `argc`.

**xv6 does the same thing in about a hundred lines**, and step 4 is visible in full. From `exec.c`:

```c
// Allocate two pages at the next page boundary.
// Make the first inaccessible.  Use the second as the user stack.
sz = PGROUNDUP(sz);
if((sz = allocuvm(pgdir, sz, sz + 2*PGSIZE)) == 0)
  goto bad;
clearpteu(pgdir, (char*)(sz - 2*PGSIZE));
sp = sz;
```

**xv6's user stack is one page — 4,096 bytes — and the page below it is a guard page** with the user bit cleared. A program that recurses too deeply does not silently scribble over its own data; it touches the guard page and is killed. **Linux's stack grows on demand to 8 MiB** (`ulimit -s`), with its own guard gap below; xv6's never grows.

**The xv6 user address space, bottom to top:**

```
0x00000000   text and data, loaded from the ELF
             guard page    (user bit cleared)
             stack page    (4,096 bytes, grows down from the top)
             heap          (grown by sbrk)
    ...
0x80000000   KERNBASE — the kernel, mapped in every process, user bit clear
```

**The kernel is mapped at `0x80000000` in every xv6 process.** That is the design Linux used until Meltdown (L02 §6), and xv6 has no page-table isolation.

---

## 5. A Process's Whole Life, in xv6

Four functions in `proc.c`, each short enough to read in a sitting. Together they are the life cycle.

### `allocproc` (line 74) — a slot, a PID, and a stack that looks used

`allocproc` finds an `UNUSED` entry in the 64-slot table, marks it `EMBRYO`, gives it a PID, and allocates a 4,096-byte **kernel stack**. Then it does something clever:

```c
sp = p->kstack + KSTACKSIZE;
sp -= sizeof *p->tf;                  // room for a trap frame
p->tf = (struct trapframe*)sp;
sp -= 4;
*(uint*)sp = (uint)trapret;           // a return address into trapret
sp -= sizeof *p->context;
p->context = (struct context*)sp;
memset(p->context, 0, sizeof *p->context);
p->context->eip = (uint)forkret;      // where swtch will "return" to
```

**It builds a kernel stack that looks exactly as if the process had been interrupted and switched away from.** The first time the scheduler switches to it (L05 §3), `swtch` pops the context and returns — into `forkret`, which returns — into `trapret`, which pops the trap frame and `iret`s into user space. **A new process starts running by pretending to resume.** There is no separate "start" path to get wrong.

### `fork` (line 181) — copy the parent, and change one register

```c
np->pgdir = copyuvm(curproc->pgdir, curproc->sz);   // copy every user page
np->sz = curproc->sz;
np->parent = curproc;
*np->tf = *curproc->tf;                             // same saved registers...
np->tf->eax = 0;                                    // ...except the return value
for(i = 0; i < NOFILE; i++)
  if(curproc->ofile[i])
    np->ofile[i] = filedup(curproc->ofile[i]);      // share open files
np->cwd = idup(curproc->cwd);
...
np->state = RUNNABLE;
return pid;                                         // parent's return value
```

**This is why `fork` returns twice.** The child's trap frame is a copy of the parent's, so when the child first reaches user space it resumes at the same instruction — the one after `int $64` — with the same registers. **The one difference is `eax`, which is where the return value lives**: 0 in the child, the child's PID in the parent. PROG 201 L01 §2 described the behaviour; these two lines are the mechanism.

> **xv6's `copyuvm` copies every page.** There is no copy-on-write: a 1 MB xv6 process forking
> copies a megabyte. PROG 201 L01 §4 measured Linux copying **none** for a reader. Adding
> copy-on-write to xv6 is a Project 2 option, and Week 5 is the machinery it needs.

### `exit` (line 228) — give everything back except the entry itself

`exit` closes every open file, releases the current directory, **wakes the parent** (which may be asleep in `wait`), hands any children of its own to `init`, sets its own state to **`ZOMBIE`**, and calls `sched()` — **which never returns**, because nothing will ever switch back to a zombie.

**What a zombie still holds**: its `struct proc` slot, its PID, its kernel stack and its page table. The process is dead but not yet freed, because **it cannot free the kernel stack it is standing on.**

### `wait` (line 273) — the parent does the freeing

`wait` scans the table for a child of the caller in state `ZOMBIE`. If it finds one, it frees the child's kernel stack and page table, clears the slot back to `UNUSED`, and returns the PID. If it has children but none are zombies, it **sleeps**, and `exit` in L05's terms will wake it.

**So the zombie state exists for a mechanical reason, not a philosophical one**: some other process has to free a dead process's last resources, and the parent is waiting for its exit status anyway. PROG 201 L02 measured zombies holding RSS 0; xv6 shows what they do still hold, and who takes it away.

```
               allocproc            fork sets RUNNABLE          scheduler picks it
   UNUSED ───────────────▶ EMBRYO ─────────────────▶ RUNNABLE ─────────────────▶ RUNNING
     ▲                                                  ▲  ▲                         │ │
     │                                     wakeup       │  │    yield (timer)        │ │
     │                                  ┌───────────────┘  └─────────────────────────┘ │
     │                                  │                                              │
     │                               SLEEPING ◀────────── sleep (wait, read, pipe) ────┤
     │                                                                                 │
     └──────────────── parent's wait frees it ─────────── ZOMBIE ◀────── exit ─────────┘
```

---

## 6. Processes Talking: Inter-Process Communication

Each process has its own address space, and **nothing in one can reach the other's memory.** That is the guard from L01 working as intended — and it means two processes that need to cooperate must go through the kernel.

| Mechanism | What the kernel does | Seen in |
|---|---|---|
| **Pipe** | keeps a buffer in kernel memory; `write` copies in, `read` copies out, and each blocks when it must | PROG 201 Weeks 1–2; xv6 `pipe.c` |
| **Signal** | sets a pending bit; delivers it on the target's next return to user space | PROG 201 Week 0 |
| **Shared memory** | maps the same physical frames into two page tables, then gets out of the way | PROG 201 Week 2; Week 5 here |
| **Socket** | a pipe between machines, with a protocol | PROG 201 Week 5 |
| **Exit status** | stores one byte in the zombie until the parent collects it | §5 above |

**xv6 has exactly one of these, the pipe**, and it is small: `pipe.c` keeps a **512-byte** circular buffer (`PIPESIZE`), two counters, and a spinlock. A `write` to a full pipe **sleeps** until a reader makes room; a `read` from an empty one sleeps until a writer arrives — the same `SLEEPING` state and the same `wakeup` as `wait`. **Linux's default pipe holds 65,536 bytes**, in sixteen page-sized slots, as PROG 201 Week 2 measured.

**Every IPC mechanism except shared memory is a copy through the kernel**, so every message pays the door from L03 twice — once to put it in and once to take it out. **Shared memory pays once, to set up, and then not at all** — which is why it can be fastest, and also why PROG 201 Week 2 measured it *losing* to a pipe for small messages, where the coordination it needs cost more than the copies it saved.

---

## 7. What to Take Away

1. **Every process sees the same shape of map**: text, data, bss, heap growing up, a vast gap, mappings, stack growing down.
2. **`/proc/<pid>/maps` is the kernel's list of regions**, and each region's permissions are page-table bits that make writes to code and execution of data fault.
3. **ASLR moves every region by whole pages on every run**; `setarch -R` pins them at `0x555555555180`.
4. **Address space is not memory.** 256 MiB mapped added nothing to RSS until it was written, and then exactly what was written.
5. **`exec` builds the map from an ELF file**; xv6 gives the stack one page and a guard page below it.
6. **xv6's `allocproc` makes a new process look interrupted**, so that starting it is resuming it; `fork` copies the trap frame and changes `eax`; `exit` makes a zombie that cannot free its own stack; `wait` frees it.
7. **Separate address spaces force communication through the kernel**, and every mechanism but shared memory pays the door per message.

---

## Exercises

1. Run `layout.c` under `setarch -R` and without. Then run `cat /proc/self/maps` twice. **Which regions of `cat` move and which do not?** Explain `[vsyscall]`.
2. In xv6, write a program that recurses without limit. Predict what xv6 prints when it dies, then run it. Which line of `trap.c` printed the message, and what is the trap number?
3. `rss.c` touched every page with `memset`. Change it to *read* every page instead, and predict `VmRSS` before you run it. *(PROG 201 L01 §4 has the answer, and Week 5 has the reason.)*
4. In `allocproc`, what would go wrong if the line `p->context->eip = (uint)forkret;` were removed? Trace what `swtch` would do on the first switch to the new process.
5. xv6's `exit` gives its children to `init`. Find the line. What would happen to an orphan's exit status if it did not, and nobody ever called `wait` for it?

---

*CS 202 · Week 1 · L06 · © CSE Department*
