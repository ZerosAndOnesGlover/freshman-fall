# PROG 201 · Systems Programming in C
## Week 9 · Lecture 1 of 3
### Measure First, and What a Profiler Costs

---

**Reading:** CS:APP §5.14 · *Systems Performance* (Gregg) Ch. 1–2 · `man 1 valgrind`, `man 2 setitimer`, `man 3 dladdr` · **Previous:** L27 · **Next:** L29 — caches, bandwidth and the roofline

---

## 1. The Number That Makes the Argument

Here is a program that reads 400,000 words and counts them. It is correct. It takes **2.35 seconds**.

Now, two ways to make it faster.

**Try every optimisation setting the compiler has:**

| | seconds |
| --- | --- |
| `-O0` | 2.78 |
| `-O1` | 2.47 |
| `-O2` | 2.35 |
| `-O3` | 2.38 |
| `-Os` | 2.78 |
| `-Ofast` | 2.33 |

**Nineteen percent, across everything GCC offers**, and `-O3` is slower than `-O2`.

**Or profile it, find that 61.59% of the instructions are inside `strcmp`, and replace a linear scan with a hash table:**

| | seconds |
| --- | --- |
| the original | 2.351 |
| after three changes | **0.039** |

**Sixty times**, with byte-identical output.

That is the whole of Week 9 in one comparison, and it is why the first lecture is about measuring rather than about optimising. **The compiler cannot fix your algorithm**, and — the part people find harder — once your algorithm is right, the compiler flags stop mattering at all:

| the *fast* program | seconds |
| --- | --- |
| `-O0` | 0.05 |
| `-O2` | 0.04 |
| `-O3` | 0.04 |

---

## 2. The Two Kinds of Profiler

| | **Sampling** | **Instrumentation** |
| --- | --- | --- |
| How | interrupt the program periodically, record where it was | insert counting code at every function or line |
| Overhead | **~1%**, and tunable | 2× to 100× |
| Accuracy | statistical — needs enough samples | exact counts |
| Sees | whatever was running, including libraries and the kernel | only what was instrumented |
| Distorts | almost nothing | small functions, badly |
| Examples | `perf`, VTune, `gprof`'s timer half | Callgrind, `gcov`, `gprof`'s call-count half |

**Choose sampling to find out where the time goes, and instrumentation to find out exactly what happened.** They answer different questions, and this course uses both — because the standard sampling tool is unavailable, which is §3.

---

## 3. `perf` Does Not Work Here, and That Is Worth Knowing

The obvious first command is `perf`, and on these machines it fails:

```
$ perf stat -e task-clock ./prog
perf_event_paranoid setting is 4:
  -1: Allow use of (almost) all events by all users
>= 0: Disallow raw and ftrace function tracepoint access
>= 1: Disallow CPU event access
>= 2: Disallow kernel profiling
```

**`kernel.perf_event_paranoid` is 4**, which refuses everything — not just kernel profiling, but a `task-clock` count on your own process. Ubuntu ships it that way because performance counters have repeatedly been a side-channel: they can measure another process's behaviour precisely enough to extract keys.

Lowering it needs root, and on a shared machine it is a real decision rather than a formality. So this course does what you will have to do on any locked-down production host:

| | what it needs |
| --- | --- |
| `perf` | `perf_event_paranoid ≤ 2`, i.e. root or a policy change |
| **Callgrind** | **nothing** — it simulates the CPU in software |
| **`gprof`** | **nothing** — `-pg` and the process's own timer |
| **A sampling profiler you wrote** | **nothing** — `setitimer` and a signal handler |

**The third row is the interesting one**, and it is §5.

---

## 4. Callgrind: Exact, Slow, and Available

```
$ valgrind --tool=callgrind --callgrind-out-file=cg.out ./slow words.txt
$ callgrind_annotate cg.out
```

```
3,984,355,595 (100.0%)  PROGRAM TOTALS

  Ir                      file:function
  2,453,885,767 (61.59%)  strcmp-avx2.S:__strcmp_avx2 [libc.so.6]
  1,247,789,129 (31.32%)  slow.c:main [./slow]
    227,382,882 ( 5.71%)  ???:0x0000000000109190
     30,305,117 ( 0.76%)  vfscanf-internal.c:__vfscanf_internal [libc.so.6]
```

**61.59% of every instruction executed was inside `strcmp`**, and it says so with no ambiguity, naming the file and the exact glibc variant. It also annotates your source line by line.

Three things to know about it:

**It counts instructions, not time.** `Ir` is instruction reads. A cache miss and a register move count the same, so a memory-bound program will look flatter than it is — which is what `--cache-sim=yes` and L29 are for.

**It runs the program on a simulated CPU**, typically **20–100× slower**. Use a smaller input. That is not a limitation to apologise for: exact counts on a tenth of the data usually answer the question.

**It is deterministic.** Run it twice and get identical numbers, which makes before-and-after comparisons trivial and is something no sampling profiler can offer.

---

## 5. Write the Sampling Profiler

A sampling profiler is about sixty lines, needs no privileges, and building one is the fastest way to stop thinking of profilers as magic.

**The mechanism**: ask the kernel to interrupt you every *n* microseconds of CPU time, and in the handler, look at where you were interrupted.

```c
static void on_prof(int sig, siginfo_t *si, void *uc)
{
    ucontext_t *c = uc;
    void *ip = (void *) c->uc_mcontext.gregs[REG_RIP];   /* x86-64 */
    if (nsamp < MAXSAMP) samples[nsamp++] = ip;
}

void sprof_start(long usec)
{
    struct sigaction sa = {0};
    sa.sa_sigaction = on_prof;
    sa.sa_flags = SA_SIGINFO | SA_RESTART;
    sigaction(SIGPROF, &sa, NULL);
    struct itimerval it = { { 0, usec }, { 0, usec } };
    setitimer(ITIMER_PROF, &it, NULL);
}
```

**`ITIMER_PROF` counts CPU time, not wall time**, and delivers `SIGPROF` — so a program that blocks on I/O is not sampled while it waits, which is what you want when you are looking for CPU. (`ITIMER_REAL`/`SIGALRM` samples wall time and would.)

**The third argument to a `SA_SIGINFO` handler is a `ucontext_t *`**, and it holds the entire interrupted register set — including the instruction pointer. That is the sample.

Then `dladdr` turns an address into a function name (Week 8), and counting gives you a profile:

```
[sprof] 200 samples
[sprof] samples percent  function
[sprof]     157   78.50%  slow
[sprof]      40   20.00%  medium
[sprof]       3    1.50%  quick
```

**Three rules the handler must obey**, and all three are Week 0 L03:

- **Async-signal-safe only.** Recording into a preallocated array is fine; `malloc` and `printf` are not — and a `malloc` profiler that samples inside `malloc` will deadlock.
- **Save and restore `errno`** if you call anything that can set it.
- **The buffer is finite.** Count what you drop rather than growing it in a handler.

---

## 6. Two Ways Your Own Profiler Will Lie to You

**It cannot name a static function.** `dladdr` reads the **dynamic** symbol table, and a `static` function is not in it. Without `-rdynamic` the whole profile collapses:

```
$ ./target_nord
[sprof]     200  100.00%  ./target_nord        <- no function names at all

$ nm -D --defined-only target_nord | wc -l     ->  1
$ nm -D --defined-only target      | wc -l     -> 14
```

**`-rdynamic` puts your symbols in the dynamic table** and the profile becomes readable. This is Week 8 §7's visibility argument arriving as a tooling failure — and it is why real profilers read `.symtab` from the file, or the DWARF, rather than asking the loader.

**It will not name libc's internals either.** Profiling the slow program from §1 with the same profiler gives:

```
[sprof]    1955   74.88%  /lib/x86_64-linux-gnu/libc.so.6
[sprof]     465   17.81%  main
```

**Seventy-five percent "somewhere in libc"** — which we know from Callgrind is `__strcmp_avx2`, but `dladdr` cannot say so, because glibc resolves `strcmp` through an IFUNC to a variant whose symbol is not where `dladdr` looks.

**So the honest summary of a hand-built sampler**: it tells you which of *your* functions is hot, cheaply, on any machine, and it will point at a library without telling you why. That is often enough to know what to do next, and when it is not, Callgrind is.

---

## 7. The Method

1. **Have a workload and a number.** "It is slow" is not a starting point; "this input takes 2.35 s" is.
2. **Measure before you look at the code.** Every guess you make before profiling is a guess you will defend afterwards.
3. **Find the top item, and only the top item.** 61.59% in `strcmp` makes everything else irrelevant until it is fixed.
4. **Ask why it is hot before making it faster.** `strcmp` was not slow; it was being called 2.4 billion times, and the fix is to call it less.
5. **Change one thing. Measure again.** The profile moves, and the new top item is rarely the old second place.
6. **Stop when it is fast enough**, and write down what you did and what it bought.

Step 4 is the one people skip. **The profiler tells you *where*; it never tells you *why***, and the answer to "why" is what decides whether you write a hash table or a SIMD intrinsic.

---

## Summary

- **A profiler beat every compiler flag by 60× to 19%** on the same program. The compiler cannot fix your algorithm, and once the algorithm is right the flags stop mattering.
- **Sampling** costs ~1% and is statistical; **instrumentation** is exact and costs 2×–100×. They answer different questions.
- **`perf` is unavailable here** — `perf_event_paranoid` is 4, and lowering it needs root. Callgrind, `gprof` and a profiler you write need nothing.
- **Callgrind** is deterministic, names everything, annotates your source, counts **instructions rather than time**, and runs 20–100× slow.
- **A sampling profiler is `setitimer(ITIMER_PROF)` plus a `SA_SIGINFO` handler that reads `REG_RIP` out of the `ucontext`.** The handler must be async-signal-safe.
- **It cannot name static functions without `-rdynamic`** — measured, 1 dynamic symbol against 14 — and it cannot name libc's IFUNC-resolved internals at all.
- The method: a workload and a number; measure first; fix the top item; **ask why it is hot**; measure again.

---

## Exercises

1. Run `perf stat true` on your own machine. If it works, what is your `perf_event_paranoid`? If it does not, read `man 2 perf_event_open`'s "perf_event related configuration files".
2. Profile the same program with Callgrind and with your sampling profiler. Where do they disagree, and which one is wrong?
3. Set the sampling interval to 10 ms, 1 ms and 100 µs on a one-second program. Plot samples against interval, and say where the overhead starts to show.
4. Sample a program that spends most of its time blocked on `read`. Compare `ITIMER_PROF` and `ITIMER_REAL`. Which one do you want, and when would you want the other?
5. Add `-rdynamic` to a program with static functions and diff the profile. Then make one function non-static and see it appear.
6. Callgrind a program twice with the same input. Are the numbers identical? Now do the same with your sampler.
7. Write the profiler's handler with `printf` in it and run it on a program that allocates in a loop. Describe the failure precisely.

---

*PROG 201 · Week 9 · L28 · © CSE Department*
