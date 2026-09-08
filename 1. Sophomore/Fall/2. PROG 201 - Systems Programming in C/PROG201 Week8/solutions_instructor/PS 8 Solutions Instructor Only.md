# PROG 201 · PS 8 Solutions
## A `malloc` Profiler with `LD_PRELOAD` — Instructor Only

---

**Do not distribute.** Q4 is three measurements whose answers are the marks.

**Machine these numbers came from:** Linux 7.0.0-30-generic, gcc 13.3.0, glibc 2.39, Ubuntu 24.04.

**On the deadline:** this and Project 1 are both due at 17:00 on the Friday of Week 9. The paper tells students to do this one in Week 8; expect that most will not, and expect Q4 to be the part that suffers. **Mark Q4 generously on reasoning and strictly on evidence** — a student who ran the experiments and got different numbers has done the work.

---

## Reference Solution — `mtrace.c`

The bootstrap arena and the recursion flag are the two pieces students struggle with; everything else is bookkeeping.

```c
/* LD_PRELOAD malloc profiler.  The reference for PS 8. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dlfcn.h>
#include <stdatomic.h>

static void *(*real_malloc)(size_t);
static void  (*real_free)(void *);
static void *(*real_calloc)(size_t, size_t);
static void *(*real_realloc)(void *, size_t);

static atomic_long n_malloc, n_free, n_calloc, n_realloc;
static atomic_long bytes_total, live, peak;
static __thread int inside;                 /* stop recursion through dlsym */

/* dlsym itself calls calloc on the first call, before real_calloc is set.
 * A tiny bootstrap arena breaks that circle. */
static char boot[65536];
static size_t boot_used;
static int is_boot(void *p) { return (char *) p >= boot && (char *) p < boot + sizeof boot; }

static void *boot_alloc(size_t n)
{
    n = (n + 15) & ~(size_t) 15;
    if (boot_used + n > sizeof boot) return NULL;
    void *p = boot + boot_used;
    boot_used += n;
    return p;
}

static void init(void)
{
    static int done;
    if (done) return;
    done = 1;                                /* set BEFORE dlsym, not after */
    real_malloc  = dlsym(RTLD_NEXT, "malloc");
    real_calloc  = dlsym(RTLD_NEXT, "calloc");
    real_realloc = dlsym(RTLD_NEXT, "realloc");
    real_free    = dlsym(RTLD_NEXT, "free");
}

static void bump(long n)
{
    long l = atomic_fetch_add(&live, n) + n;
    long p = atomic_load(&peak);
    while (l > p && !atomic_compare_exchange_weak(&peak, &p, l)) ;
}

void *malloc(size_t n)
{
    if (!real_malloc) { if (inside) return boot_alloc(n); inside = 1; init(); inside = 0; }
    if (!real_malloc) return boot_alloc(n);
    void *p = real_malloc(n);
    if (p) { atomic_fetch_add(&n_malloc, 1);
             atomic_fetch_add(&bytes_total, (long) n); bump((long) n); }
    return p;
}
```

*(The `calloc`, `realloc`, `free` and reporting bodies follow the same shape; the full file is with these notes.)*

Built with `gcc -O2 -fPIC -shared -o mtrace.so mtrace.c -ldl`. **`-ldl` is a no-op on glibc ≥ 2.34** (L25 §6) and should be kept for portability.

---

## Q1 — The Interposer (30)

**(a) [14]** Four functions at [3] each, plus [2] for `dlsym(RTLD_NEXT, ...)` used correctly rather than `dlopen("libc.so.6")`.

`realloc` is where submissions differ. It must: handle `old == NULL` as `malloc`; handle a bootstrap-arena pointer by allocating fresh and copying; and not double-count. A submission that forwards `realloc` without thinking about the arena will crash on the first program that uses it.

**(b) [10]** A working solution **[6]** and the description **[4]**.

Two mechanisms, and a good answer has both:

- **`static __thread int inside`** — per-thread, because two threads can be in `dlsym` at once and a global flag makes one of them take the wrong path.
- **A static arena**, with `free` recognising its blocks by address range and ignoring them, and `realloc` copying out of it.

**The `done = 1` before the `dlsym` calls, not after**, is the subtle one — otherwise a nested call re-enters `init` and recurses anyway. Point it out if it is missing even where the code works.

Arena exhaustion: returning `NULL` is acceptable if stated; the reference's 64 KiB has never been exhausted in testing, and a student who says "I picked a number and never checked" should be asked to add the check.

**(c) [6]** The prediction **[2]**, the actual failure **[4]**.

Expected: a **stack overflow / segfault before `main`**, often with no output at all, because the recursion happens inside the loader before stdio exists. Some students see `Segmentation fault` and nothing else; some see it hang. Both are correct reports.

**Award full marks for an honest "I predicted an infinite loop and got a segfault with no message"** — the point is having done it deliberately.

---

## Q2 — The Report (20)

**(a) [10]** The counts **[3]**, total bytes **[2]**, **peak live [3]**, unfreed count **[2]**.

Peak live requires knowing the size of a freed block. The two reasonable answers:

- **`malloc_usable_size(p)`** — glibc-specific, free, and returns the *usable* size which is ≥ what was asked for, so the peak is a slight over-estimate. Say so.
- **A header before every block**, which means your `malloc` returns `real_malloc(n + 16) + 16` and your `free` subtracts 16. **This changes the allocator's layout**, breaks alignment guarantees if done carelessly, and means any pointer that reaches the real `free` without going through your `malloc` is a crash.

Either is fine with the trade-off stated. The second is what the question means by "changes your allocator's layout".

**(b) [6]** `write(2, ...)` **[4]**, the reason **[2]**.

The reason is **Week 0's**: `printf` is not async-signal-safe and, more immediately here, it **allocates** — so a report printed with `printf` from inside a `malloc` interposer can re-enter the very code it is reporting on. `snprintf` into a stack buffer and one `write` avoids both.

**(c) [4]** `_Atomic` or `atomic_fetch_add` **[3]**, the justification **[1]**.

Why not a mutex: the counters are independent and each update is a single read-modify-write, so an atomic add is one `lock xadd` (Week 3 L11 §2 measured **5.4 ns**) against a mutex's lock/unlock pair — and a mutex inside `malloc` risks deadlocking against a program that allocates from a signal handler.

---

## Q3 — Use It (20)

**(a) [8]** Five programs **[5]**, the table **[1]**, the explanation **[2]**.

Reference, for calibration:

```
python3 -c pass:  malloc 2285  calloc 12  realloc 174  free 2276
                  total 2,742,219 bytes, peak 2,742,219, 21 never freed
```

The most common surprises, all acceptable: how much a "do nothing" interpreter allocates; that `realloc` appears at all; that the unfreed count is not zero (it is not a leak — it is memory the program deliberately keeps until exit); and that `total` equals `peak`, which means nothing was freed before the end.

**(b) [6]** The program **[3]**, the arithmetic matching **[3]**.

**(c) [6]** The filter **[4]**, the use **[2]**. Real profilers filter to keep the output readable and the overhead down; the honest answer is that a program making a million 16-byte allocations produces a report nobody can read.

---

## Q4 — Three Things It Cannot Do (18)

**(a) [6]** Both numbers **[2]**, the explanation **[2]**, **the evidence from the binary [2]**.

Reference: the same source with 1,000 `malloc(128)`/`free` pairs gives

| build | reported |
| --- | --- |
| `-O0` | **1,012 malloc, 1,000 free, 12 never freed** |
| `-O2` | **2 malloc** (both from stdio) |

and the evidence:

```
$ objdump -d leaky | grep -c '<malloc@plt>'      -> 0
$ nm -D --undefined-only leaky | grep -c malloc  -> 0
```

**GCC deleted every allocation** — the standard permits it, since the pointers are unused — so `malloc` is not merely uncalled, **the binary does not reference the symbol at all**.

What it means for any `LD_PRELOAD` tool: **you can only intercept a call that exists in the binary.** A profiler reporting zero allocations may be telling the exact truth about a program that makes none, and there is no way to tell the two cases apart from the profiler's output. The evidence has to come from the binary.

**The `-O2` half is the mark.** A student who ran only `-O0` has not answered the question.

**(b) [6]** The interposer working **[2]**, `date` unaffected **[1]**, the explanation **[3]**.

`date` calls **`clock_gettime`**, not `time`, and `clock_gettime` is resolved through the **vDSO** — a kernel-provided object that is not a file and never enters libc's PLT. So there is nothing to interpose in front of.

Both named: **a different function** and **the vDSO**. One of the two is [4]; both is [6].

**(c) [6]** The report **[2]**, the `LD_DEBUG` confirmation **[1]**, the consequence and the fix **[3]**.

Reference: `true` and `python3` run the destructor; **`ls` and `grep` do not**, and `LD_DEBUG=all` shows the loader printing no `calling fini` lines at all for them.

The consequence: **the tool silently produces no output, with no indication that anything went wrong.** For a measuring tool that is the worst failure mode there is — it is indistinguishable from "the program allocated nothing".

Fixes, any one: write incrementally; interpose `exit`/`_exit` **as well as** the destructor, with a report-once guard; or `atexit` from a constructor. **Note for markers: interposing `_exit` alone does not rescue `ls`** — the reference tried it and it did not help, because a library's internal calls do not go through the PLT. A student who tried it, reported that it failed, and reached for incremental output instead has done better work than one who assumed it would work.

---

## Q5 — What a Real Tool Does (12)

**(a) [4]** The mechanism: **capturing a call stack at every allocation** — by walking frame pointers, by `backtrace()`, or by unwinding DWARF. Expensive because it is tens to hundreds of instructions per allocation instead of two, and because the stacks then have to be stored, de-duplicated and symbolised. Worth it because **totals tell you that you have a problem and stacks tell you where**, which is the difference between a number and an action.

**(b) [4]** Two of: **no bootstrap problem** — the allocator is not interposing on itself; **no PLT dependency**, so it sees allocations from libraries that call their own internal `malloc`, which interposition cannot (a direct consequence of Q4); **access to internal state** — bin occupancy, fragmentation, arena counts — that no interposer can reach; **and it cannot be defeated by static linking**, where there is no dynamic symbol to interpose at all.

**(c) [4]** The problem is the **observer effect**, or **probe effect** — accept either name. Worst on an allocation-intensive workload where allocations are small and frequent: a parser, a JSON or XML library, an interpreter's inner loop, or Week 4's fragmenting allocator benchmark.

What a sampling profiler does: **record only one in *N* allocations** (or take a stack only every *N* bytes allocated, as `heaptrack` and `jemalloc`'s profiler do), so the overhead is bounded and the totals are corrected statistically. Trades exactness for not changing the thing being measured.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | The interposer | 30 |
| 2 | The report | 20 |
| 3 | Use it | 20 |
| 4 | Three things it cannot do | 18 |
| 5 | What a real tool does | 12 |
| | **Total** | **100** |

---

*PROG 201 · Week 8 · PS 8 Solutions · Instructor Only · © CSE Department*
