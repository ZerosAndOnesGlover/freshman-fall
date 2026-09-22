# PROG 102 · Lecture 31
## Threads and Races

**Week 10 · Tuesday · 50 minutes**
**Reading:** Williams, *C++ Concurrency in Action*, Ch. 1–2 · **Assumes:** Week 5, Week 9

**Date:** Tuesday 30 March 2027 · 10:00–10:50 · Week 10

---

## 1. Starting a Thread

```cpp
#include <thread>

std::thread t([]{ std::puts("running"); });
t.join();                 // wait for it
```

A `std::thread` runs a callable — usually a lambda (**Week 11**) — on a new OS thread. You must
**`join()`** it (wait) or **`detach()`** it (abandon) before it is destroyed.

**If you do neither, `~thread` calls `std::terminate`.** Not a leak, not a warning: your process dies.
That is deliberate — the language refuses to guess whether you meant to wait.

```cpp
unsigned n = std::thread::hardware_concurrency();      // 8 on the reference machine
```

A hint, not a promise; it can return 0 if the implementation cannot tell.

### 1.1 Exceptions Do Not Cross Threads

```cpp
std::thread t([]{ throw std::runtime_error("boom"); });
t.join();                 // does NOT rethrow. std::terminate was already called.
```

**An exception that escapes a thread's function calls `std::terminate` immediately.** There is no
caller to unwind to — the stack below it belongs to the runtime.

**Everything from Week 9 assumed a caller.** To move an exception between threads you need
`std::promise`/`std::future` or a caught-and-stored `std::exception_ptr`, and you must arrange it
yourself.

> **This is the first thing this week invalidates**, and it is worth stating on day one: your
> carefully exception-safe code protects nothing if the exception is thrown on a thread that has no
> handler.

---

## 2. The Data Race

> **A data race is two threads accessing the same memory, at least one of them writing, with no
> synchronisation between them.**

**In C++ a data race is undefined behaviour.** Not "a wrong answer" — undefined. The compiler is
entitled to assume it does not happen and to optimise accordingly, which §3 shows it doing.

The canonical example:

```cpp
++counter;        // three operations, not one
```

compiles to **load, increment, store**. Two threads interleaving:

| | Thread A | Thread B | `counter` |
| --- | --- | --- | --- |
| 1 | load → 5 | | 5 |
| 2 | | load → 5 | 5 |
| 3 | increment → 6 | | 5 |
| 4 | | increment → 6 | 5 |
| 5 | store 6 | | 6 |
| 6 | | store 6 | **6** |

**Two increments, one result.** A lost update.

---

## 3. Measured — and Why `-O2` Hides It

Four threads, one million `++` each. **Expected 4,000,000.**

### 3.1 At `-O0`

```
run 1  unsynchronised  1139305
run 2  unsynchronised  1137667
run 3  unsynchronised  1115897
```

**About 1.1 million out of 4 million — roughly 72% of increments lost.** The bug is impossible to miss.

### 3.2 At `-O2`

```
run 1  unsynchronised  4000000     <- correct
run 2  unsynchronised  4000000     <- correct
run 3  unsynchronised  3000000
```

**Twice it gave the right answer.** Once it lost exactly one million — a whole thread's contribution.

### 3.3 The Explanation Is in the Assembly

```asm
_Z4bumpi:                              ; for (k=0;k<n;++k) ++plain;
        test    edi, edi
        jle     .L1
        mov     rdx, QWORD PTR plain[rip]     ; ONE load
        lea     eax, -1[rdi]
        lea     rax, 1[rdx+rax]               ; add n
        mov     QWORD PTR plain[rip], rax     ; ONE store
        ret
```

**The million-iteration loop became a single read-modify-write.** The compiler is allowed to do this
precisely *because* a data race is undefined behaviour — it may assume no other thread touches `plain`,
so it can keep the value in a register.

**The race window shrank from a million instruction-triples to one.** So collisions became rare — and
when one happens, it loses an entire thread's million at once.

> **This is the most important thing in the lecture.** The optimizer did not fix your bug. **It changed
> the shape of the failure**, from constant and obvious to rare and catastrophic.
>
> **A concurrency bug that passes testing is not absent.** It is the same bug with a smaller window,
> and the window reopens on a different compiler, a different optimization level, or a busier machine.

---

## 4. ThreadSanitizer

You cannot find these by reading, and you cannot find them reliably by testing. **You find them with a
tool.**

```
g++ -std=c++17 -O1 -g -pthread -fsanitize=thread prog.cpp -o prog
./prog
```

TSan instruments every memory access and tracks which thread touched what, with what synchronisation.
**It reports a race even when the race did not cause a wrong answer on that run** — which is exactly
what you need, given §3.

```
WARNING: ThreadSanitizer: data race (pid=528648)
SUMMARY: ThreadSanitizer: data race tsan_demo.cpp:9 in operator()
```

and on the `std::atomic` version of the same program:

```
race warnings: 0
atomic = 400000
```

### 4.1 Getting It to Run

On some Linux kernels TSan builds and then dies at startup:

```
FATAL: ThreadSanitizer: unexpected memory mapping
```

**This is an address-space-layout problem, not your code.**

```
setarch $(uname -m) -R ./your_program
```

**Verified under `setarch`:** TSan finds the real race and reports **zero** warnings on the atomic
version. Lab 0 asked you to confirm this in Week 0.

### 4.2 What It Costs

TSan slows execution by roughly **5–15×** and uses much more memory. **It is a development tool**, not
something you ship — and, as always, **never time a sanitizer build.**

> **Use it on every concurrent program you write, every time.** A clean TSan run is not proof of
> correctness — it only sees the interleavings that actually occurred — but a dirty one is proof of a
> bug, and it points at the line.

---

## 5. What Counts as Synchronisation

A race requires **unsynchronised** access. These establish synchronisation:

- a **mutex** — Lecture 32;
- **atomic** operations — Lecture 33;
- `join()` — everything the thread did happens-before the join returns;
- thread **creation** — everything before it happens-before the thread starts;
- a **condition variable** wait/notify pair.

**These do not:**

- `volatile` — it prevents certain compiler optimizations and **provides no thread synchronisation
  whatsoever.** This is the most persistent myth in the subject. `volatile` is for
  memory-mapped hardware registers, not for threads.
- a `sleep` — timing is not synchronisation, no matter how long you wait.
- "it's only one byte" — object size is irrelevant; the standard defines races on *memory locations*.
- "reads are safe" — a read racing a write is still a race.

### 5.1 `volatile`, Measured

Because the myth is so durable, here is the counter from §3 declared `volatile`, at `-O2`:

```
volatile counter = 1106642 (expected 4000000)
volatile counter = 1036961 (expected 4000000)
volatile counter = 1085000 (expected 4000000)
```

and under ThreadSanitizer: **2 race warnings.**

**`volatile` made the bug worse, not better.** It suppressed the hoisting from §3.3 — so the loop is a
real million read-modify-writes again — which restores the `-O0` failure rate at `-O2`.

> **That is exactly what it says on the tin and exactly not what people want from it.** `volatile`
> tells the compiler *do not optimize this access away*. It says nothing to the **hardware** about
> cache coherence, nothing about instruction ordering between cores, and nothing about atomicity.
>
> **The load-increment-store is still three operations.** `volatile` guarantees all three happen; it
> does not stop another thread happening in between.

---

## 6. Summary

| Idea | The point |
| --- | --- |
| Neither `join()` nor `detach()` | `std::terminate` |
| An exception escaping a thread | `std::terminate` — **Week 9 assumed a caller** |
| A data race | Two accesses, one a write, no synchronisation. **Undefined behaviour** |
| `++counter` | Load, increment, store — three operations |
| Measured at `-O0` | ~1.1M of 4M — **72% lost** |
| Measured at `-O2` | 4M, 4M, **3M** — usually right, occasionally catastrophic |
| Why | The compiler collapsed the loop to one read-modify-write — **because UB let it** |
| **The optimizer did not fix it** | It shrank the window |
| ThreadSanitizer | Finds races that did not manifest. `setarch $(uname -m) -R` to run it |
| TSan costs 5–15× | Development tool; never time it |
| **`volatile` is not synchronisation** | The most persistent myth in the subject |

---

## 7. Exercises

**1.** Start a thread and neither join nor detach it. **Report what happens** and quote the message.

**2.** Throw from inside a thread's function and try to catch it around the `join()`. **Report what
happens** and explain why in terms of unwinding.

**3.** Reproduce §3: four threads, a million increments each, at `-O0` and `-O2`, **at least five runs
each.** Report every result. **Does yours ever give 4,000,000 at `-O0`?**

**4.** Compile the increment loop and inspect the assembly at both levels. **Paste both** and identify
where the load and store are.

**5.** Run the `-O2` version under ThreadSanitizer. **Does it report a race even on a run that gave the
correct answer?** Explain why that is the useful behaviour.

**6.** Make the counter `volatile` and re-run §3 and the TSan check. **Report both.** Does `volatile`
fix the count? Does TSan still complain?

**7.** Time the same program with and without `-fsanitize=thread`. **Report the slowdown factor.**

---

## 8. Next

**Lecture 32** is the standard fix — mutual exclusion — together with the failure mode it introduces
that races do not have: **deadlock**, where nothing goes wrong and nothing happens at all.

---

*PROG 102 · Week 10 · Lecture 31 · © CSE Department*
