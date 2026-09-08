# PROG 201 · Problem Set 8
## A `malloc` Profiler with `LD_PRELOAD`

---

**Released:** Week 8, Wednesday · **Due:** Week 9, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS8_{LastName}_{StudentID}.pdf`, and your code as `PS8_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine. The write-up and the code must be yours.
>
> **Project 1 is due at 17:00 on the same day.** Two deadlines, one Friday. This problem set is
> about four hours of work and Project 1 is not — **do this one first, in Week 8**, while the
> lectures are fresh, and leave Week 9 for the shell.
>
> **Q3 and Q4 are measurements on your own machine.** State your `gcc --version`, `uname -r`, and
> your glibc version (`ldd --version`).
>
> Everything compiles clean under `gcc -Wall -Wextra -O2 -std=c11`. Warnings cost marks.

---

### The Tool

`mtrace.so`, a shared library that counts a program's allocations without the program knowing:

```
$ LD_PRELOAD=$PWD/mtrace.so ./someprogram

[mtrace] malloc 2285  calloc 12  realloc 174  free 2276
[mtrace] total allocated 2742219 bytes, peak live 2742219 bytes
[mtrace] 21 allocation(s) never freed
```

---

### Q1: The Interposer (30 points)

**(a) [14]** Replace `malloc`, `calloc`, `realloc` and `free`. Each one finds the real implementation with `dlsym(RTLD_NEXT, ...)`, records what it is about to do, and calls through.

**(b) [10]** **The bootstrap problem, which is the whole difficulty.** `dlsym` may itself allocate, so the first call to your `malloc` calls `dlsym`, which calls your `malloc`, which calls `dlsym`.

Solve it, and describe your solution. The two standard pieces are:

- **a recursion flag** (`__thread`, so it is per-thread), and
- **a small static bootstrap arena** for allocations made before the real functions are known.

If you use an arena, **`free` must recognise its blocks by address and not pass them to the real `free`**, and `realloc` must handle being given one. Say what your arena's size is and what happens if it is exhausted.

**(c) [6]** Write down, before you build it, what you expect to break, then build it **without** the recursion guard and record what actually happens — the message, the signal, and where.

A segfault before `main` is a confusing thing to debug the first time; having done it deliberately once is worth more than being told.

---

### Q2: The Report (20 points)

**(a) [10]** Count and report: calls to each of the four functions; **total bytes allocated**; **peak live bytes**; and how many allocations were never freed.

Peak live needs a running total that goes up on allocate and down on free — which means `free` has to know the size of the block it is freeing. Say how you did that, and what it cost you. *(There are two reasonable answers and one of them changes your allocator's layout.)*

**(b) [6]** Your report must be usable from a program that also writes to stdout and stderr.

Use `write(2, ...)` rather than `printf`, and say why in one sentence — the reason is Week 0's, not this week's.

**(c) [4]** Make the profiler **thread-safe**. Counters shared between threads without synchronisation are Week 3 L10 §6, and that measurement lost 70.7% of its increments.

Say which mechanism you chose and why it is the right one here rather than a mutex.

---

### Q3: Use It (20 points)

**(a) [8]** Run it on **five** programs you did not write. `python3 -c pass`, `git status`, `bash -c true`, a compiler invocation, and one of your own choosing.

Report the table. Then pick the most surprising number and explain it in two or three sentences.

**(b) [6]** Write a program with a **known** allocation profile — *n* allocations of known sizes, *m* of them freed — and check your profiler against it. Show the arithmetic matching.

**Build it `-O0` and say why** in your write-up; Q4(a) is why.

**(c) [6]** Add a `MTRACE_MIN` environment variable: only record allocations of at least that many bytes. Show it changing the output, and say in one sentence what a real profiler uses this kind of filter for.

---

### Q4: Three Things It Cannot Do (18 points)

Each part is something to measure, not to argue about.

**(a) [6]** Take your Q3(b) program with 1,000 `malloc`/`free` pairs and build it `-O2` instead of `-O0`. Run the profiler on both.

Report both numbers. Then explain the `-O2` one — and support it with evidence from the binary, not from the profiler:

```bash
objdump -d prog | grep -c 'malloc@plt'
nm -D --undefined-only prog | grep -c malloc
```

Say what that means for **any** tool built on `LD_PRELOAD`.

**(b) [6]** Write a twelve-line interposer for `time()` and confirm it works on a program of yours. Then run it on `date(1)`.

Report what happens, explain it, and name the two things involved — one is a different function and one is not a library at all.

**(c) [6]** Build the two-line probe with a constructor and a destructor and run it on **at least four** programs, including `/usr/bin/ls` and `/usr/bin/true`.

Report which ran the destructor. Confirm with `LD_DEBUG=all ... | grep "calling fini"`. Then answer the question that matters: **what does this mean for a profiler that prints its report from a destructor, and how would you write one that does not have the problem?**

---

### Q5: What a Real Tool Does (12 points)

**(a) [4]** Your profiler reports totals. `valgrind --tool=massif` and `heaptrack` report **where** the memory went.

Name the mechanism they use to get a call stack at every allocation, and say — in one sentence each — why it is much more expensive than what you did and why it is worth it.

**(b) [4]** `jemalloc` and `tcmalloc` ship their own profilers built **into** the allocator rather than interposing on it.

Give two things that buys them, at least one of which is a direct consequence of Q4.

**(c) [4]** Your interposer changes what it measures: every `malloc` now does more work, and the program's timing changes.

Name this problem, give one allocation-intensive workload where it would matter most, and say what a sampling profiler does about it.

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

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*PROG 201 · Week 8 · PS 8 · © CSE Department*
