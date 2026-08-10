# CS 201 · Week 6 · Lab 6
## Observing Page Faults Through `/proc`

---

**When:** **Tuesday of Week 7**, 15:00–16:50, BH 210 — *after* Week 6's three lectures
**Covers:** Week 6 · **Assessment:** unmarked, checked off by the TA
**You need:** `gcc`, `/proc`, `getconf`. No privileges required.

---

## What This Lab Is For

Virtual memory is the most invisible thing in the course — no instruction mentions it and no disassembly shows it. **`/proc` is where it becomes visible**, and this lab is two hours of looking.

You will read your own address space, watch memory that does not exist become real one page at a time, count copy-on-write faults, and isolate the TLB from the cache.

---

## Part 1 — Read Your Own Address Space (20 min)

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int global_init = 42;
int global_bss;
int main(void) {
    int stack_var = 1;
    int *heap = malloc(1024);
    printf("code   (main)      %p\n", (void*)main);
    printf("data   (init)      %p\n", (void*)&global_init);
    printf("bss    (uninit)    %p\n", (void*)&global_bss);
    printf("heap   (malloc)    %p\n", (void*)heap);
    printf("stack  (local)     %p\n", (void*)&stack_var);
    printf("libc   (printf)    %p\n", (void*)printf);
    printf("page size          %ld\n", sysconf(_SC_PAGESIZE));
    fflush(stdout);
    char cmd[64]; snprintf(cmd, sizeof cmd, "cat /proc/%d/maps", getpid());
    system(cmd);
    return 0;
}
```

Expected shape *(verified — your addresses will differ)*:

```
58302ed37000-58302ed38000 r-xp   ...  /…/maps          <- your code
58302ed3a000-58302ed3b000 rw-p   ...  /…/maps          <- your data
58305f6d6000-58305f6f7000 rw-p   ...  [heap]
7cc6f5c28000-7cc6f5db0000 r-xp   ...  /usr/lib/…/libc.so.6
7cc6f5eb4000-7cc6f5eb6000 r-xp   ...  [vdso]
...                              ...  [stack]
```

**Answer:**

1. Find the region containing each of the six printed addresses. Give the permissions of each.
2. **Is any region both writable and executable?** Say what that property is called and which Week 3 lab disabled it for a whole binary.
3. libc appears **four times**. Why not once?
4. Run the program three times. **What changes, and what stays the same?** Name the mechanism.
5. `[vdso]` is mapped by the kernel into every process. What is it for? *(You have called into it repeatedly in Weeks 4 and 5.)*

**✅ CHECKPOINT 1** — the maps output and your five answers.

---

## Part 2 — Memory That Does Not Exist Yet (25 min)

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>
#define MB (1024L*1024)
static long rss_kb(void) {
    FILE *f = fopen("/proc/self/statm", "r"); long sz, res;
    if (fscanf(f, "%ld %ld", &sz, &res) != 2) res = 0;
    fclose(f); return res * 4;
}
static long minflt(void) {
    struct rusage r; getrusage(RUSAGE_SELF, &r); return r.ru_minflt;
}
int main(void) {
    printf("start                      RSS=%6ld KiB  minor faults=%ld\n", rss_kb(), minflt());
    char *p = malloc(512*MB);
    printf("after malloc(512 MiB)      RSS=%6ld KiB  minor faults=%ld\n", rss_kb(), minflt());
    for (long i = 0; i < 512*MB; i += 4096) p[i] = 1;
    printf("after touching every page  RSS=%6ld KiB  minor faults=%ld\n", rss_kb(), minflt());
    return 0;
}
```

```
start                      RSS=  1444 KiB  minor faults=74
after malloc(512 MiB)      RSS=  1580 KiB  minor faults=86
after touching every page  RSS=525864 KiB  minor faults=131157
```

*(Verified.)*

**`malloc` of half a gigabyte cost 136 KiB.**

### 2.1 Check the arithmetic

$512 \text{ MiB} / 4096 = ?$ Compare with the increase in minor faults. **They should agree to within one.**

### 2.2 Time a single fault

Touch every page, then touch them all again:

```
first touch  (page fault each): 0.2578 s over 131072 pages = 1967 ns/page
second touch (already mapped) : 0.0025 s over 131072 pages =   19 ns/page
```

*(Verified.)*

**Subtract.** You have just measured the cost of a minor page fault. Convert to cycles using your Week 5 clock. **Compare with Week 4's DRAM latency of 438 cycles — how many DRAM accesses is one fault worth?**

### 2.3 The kernel is doing real work

List what the kernel must do on a minor fault for a fresh anonymous page. **One of the steps is unavoidable for security reasons — which, and what would leak without it?**

**✅ CHECKPOINT 2** — the three lines, the page arithmetic, and your per-fault cost in cycles.

---

## Part 3 — Copy-on-Write (25 min)

```c
long SZ = 256*MB;
char *p = malloc(SZ); memset(p, 1, SZ);          /* fully resident */
printf("parent before fork:  RSS=%ld KiB\n", rss_kb());
double t0 = now(); pid_t pid = fork(); double t1 = now();
if (pid == 0) {
    printf("child at birth:      RSS=%ld KiB  minor faults=%ld\n", rss_kb(), minflt());
    long f0 = minflt();
    for (long i = 0; i < SZ; i += 4096) p[i] = 2;
    printf("child after writing: RSS=%ld KiB  minor faults=%ld (+%ld)\n",
           rss_kb(), minflt(), minflt() - f0);
    _exit(0);
}
wait(NULL);
printf("fork() itself took   %.4f s for a %ld MiB address space\n", t1-t0, SZ/MB);
```

> **Call `setvbuf(stdout, NULL, _IONBF, 0)` first.** The child inherits the parent's stdio buffer and
> `_exit` does not flush it — without this you will lose the child's output entirely. *(That is
> exactly what happened the first time this was run.)*

```
parent before fork:  RSS=263596 KiB
child at birth:      RSS=263068 KiB  minor faults=14
child after writing: RSS=263260 KiB  minor faults=65566 (+65536)
fork() itself took   0.0043 s for a 256 MiB address space
256 MiB / 4096 = 65536 pages
```

*(Verified.)*

**Answer:**

1. `fork` of a fully resident 256 MiB process took 4.3 ms. **Roughly how long would copying 256 MiB take?** Estimate from Week 4's bandwidth, and say what `fork` actually spent its time on.
2. The child was born having taken **14** faults. What does it have, and what does it own?
3. **+65 536 faults** for **65 536 pages**. What made each of those faults happen, given that the child only wrote to memory it already "had"?
4. What single PTE bit makes the whole mechanism work?
5. `fork` is usually followed by `exec`. **How many pages get copied in that case, and why is that the design's whole justification?**

**✅ CHECKPOINT 3** — the four lines and your five answers.

---

## Part 4 — Isolating the TLB From the Cache (30 min)

The best measurement of the week. **Keep the cache footprint constant and vary only the page count.**

512 pointers in a random chase — always 512 cache lines = **32 KiB, which fits L1d exactly**. Change only the stride between them:

| stride | cache lines | pages spanned | ns/access |
|---:|---:|---:|---:|
| 64 B | 512 | **8** | **1.24** |
| 256 B | 512 | 32 | 4.28 |
| 1 KiB | 512 | 128 | 12.68 |
| 4 KiB | 512 | 512 | 14.57 |
| 16 KiB | 512 | 2048 | 15.77 |
| 64 KiB | 512 | **8192** | **27.57** |

*(Verified. Use `madvise(p, n, MADV_NOHUGEPAGE)` so the page size stays 4 KiB.)*

**Answer:**

1. **The data is in L1 cache in every row.** Compare row 1 with Week 4's measured L1 latency. Then explain the 22× at the bottom.
2. Between 8 and 32 pages the cost **triples**. From that, estimate the L1 dTLB's capacity in entries.
3. Define **TLB reach**. Compute it for 64 entries at 4 KiB and at 2 MiB.
4. State the general rule this experiment establishes, in one sentence, as an addition to Week 4's advice about counting cache lines.

### 4.1 A fix that did nothing

The same random chase over 1 MiB to 1 GiB, with and without `MADV_HUGEPAGE`:

| region | 4 KiB | huge | ratio |
|---:|---:|---:|---:|
| 1 MiB | 14.79 ns | 13.90 ns | 1.06× |
| 16 MiB | 112.93 ns | 112.65 ns | 1.00× |
| 1 GiB | 162.72 ns | 152.99 ns | 1.06× |

*(Verified — essentially no benefit.)*

**Explain why huge pages helped nothing here**, given that §4's experiment shows translation costing 22×. Your answer must say what that benchmark is bound by.

Then: **design a benchmark that would show a huge-page benefit.** State what you would change.

> Check whether your machine will even use them:
> ```bash
> cat /sys/kernel/mm/transparent_hugepage/enabled
> ```
> `always [madvise] never` means a program must ask.

**✅ CHECKPOINT 4** — your stride table, the four answers, and your explanation of the null result.

---

## Before You Leave

| Task | Command |
|---|---|
| Address space map | `cat /proc/self/maps` |
| Resident vs virtual size | `cat /proc/self/statm` *(fields: size, resident, …, in pages)* |
| Fault counts | `getrusage(RUSAGE_SELF, &r)` → `ru_minflt`, `ru_majflt` |
| Fault counts, externally | `/usr/bin/time -v ./prog` |
| Page size | `getconf PAGESIZE` |
| Huge page policy | `cat /sys/kernel/mm/transparent_hugepage/enabled` |
| Per-page detail | `/proc/PID/smaps` |

**The habit:** when a program's memory behaviour is confusing, `/proc` already knows. **Resident size, virtual size and fault counts answer most questions before you write any instrumentation.**

---

*CS 201 · Week 6 · Lab 6*
