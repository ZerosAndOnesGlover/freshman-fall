# PROG 102 · Week 10 · Reading Guide
## Concurrency, and Reproducing the Measurements

---

## What to Read

| Source | Sections | Why |
| --- | --- | --- |
| **Williams, *C++ Concurrency in Action*, 2nd ed.** | **Ch. 1–3** | The standard text. Threads, sharing data, mutexes. |
| **Williams** | **Ch. 4.1** | Condition variables |
| **Williams** | **Ch. 5.1–5.2** | Atomics and the memory model — **read for orientation, not mastery** |
| **cppreference** | `std::thread`, `std::mutex`, `std::condition_variable`, `std::atomic` | Reference |
| **Meyers, *Effective Modern C++*** | **Items 35–37** | `std::thread` vs `std::async`, and why to join |

> **Williams is the book for this topic** and it is much larger than one week of it. **Read Chapters
> 1–3 properly and skim Chapter 5.** Nothing in this course requires the memory-ordering material, and
> attempting it now will cost you more than it returns.

---

## Chapters 1–2 — Threads

**Guiding questions:**

1. §2.1.1 — you must `join()` or `detach()`. **What happens if you do neither, and why did the
   committee choose that behaviour** rather than defaulting to one?
2. §2.2 — Williams introduces `thread_guard`, an RAII wrapper that joins in its destructor.
   **Why is that necessary?** *(Think about an exception between construction and `join()`.)*
3. §2.4 — `hardware_concurrency()`. **What does it return when the implementation cannot tell, and how
   should you handle that?**
4. Williams discusses passing arguments to threads. **What happens to a reference argument, and why is
   `std::ref` needed?**

---

## Chapter 3 — Sharing Data

The chapter that matters most.

**Guiding questions:**

1. §3.1 — Williams defines a race condition and distinguishes it from a **data race**. **State the
   difference.** *(Not every race condition is a data race.)*
2. §3.2.1 — `std::lock_guard`. **Why must you never return a pointer or reference to protected data?**
   Williams has a specific example; find it.
3. §3.2.4 — the deadlock discussion and `std::lock`. **Compare with L32 §3.2's `std::scoped_lock`** —
   what did C++17 add over C++11?
4. §3.2.5 — the lock hierarchy. **When is consistent ordering not enough?**
5. §3.3.1 — `std::once_flag` and `call_once`. **Compare with the function-local static from Week 7
   §L23 §2.1.** Which would you use, and why?

---

## Chapter 4.1 and 5 — Waiting and Atomics

**Guiding questions:**

1. §4.1.1 — Williams' first condition-variable example. **Find where he explains spurious wakeups.**
2. Why does `wait` take the **lock** as an argument? *(What must happen atomically?)*
3. §5.2.3 — `compare_exchange_weak` may fail spuriously. **Why does that exist**, and why is it usually
   used in a loop?
4. §5.3 — the memory model. **Read the introduction and stop.** Note that `seq_cst` is the default and
   that this course requires nothing else.

---

## Reproducing This Week's Measurements

**g++ 13.3.0, x86-64 Linux, 8 hardware threads.** Race outcomes are **not** deterministic — that is
the subject. Run everything several times.

### L31 §3 — The lost update

```
g++ -std=c++17 -O0 -pthread race.cpp -o race0 && ./race0
g++ -std=c++17 -O2 -pthread race.cpp -o race2 && ./race2
```

**Expect:** `-O0` around **1.1M of 4M**; `-O2` mostly **4,000,000** with occasional large losses.
**Run each at least five times** — a single run of the `-O2` version tells you nothing.

### L31 §3.3 — Why

```
g++ -std=c++17 -O2 -S -masm=intel hoist.cpp -o hoist.s
sed -n '/^_Z4bumpi:/,/ret/p' hoist.s
```

**Expect:** one load and one store — the loop collapsed into a single read-modify-write.

### L31 §5.1 — `volatile`

```
g++ -std=c++17 -O2 -pthread vol.cpp -o vol && ./vol
```

**Expect:** ~1.0–1.1M of 4M, **worse than the non-volatile `-O2` version**, and TSan still reporting
races.

### L31 §4 — ThreadSanitizer

```
g++ -std=c++17 -O1 -g -pthread -fsanitize=thread tsan_demo.cpp -o td
setarch $(uname -m) -R ./td        # unsynchronised: data race at line 9
setarch $(uname -m) -R ./td x      # atomic: 0 warnings
```

### L32 §3, §5 — Deadlock and the queue

```
g++ -std=c++17 -O2 -pthread deadlock.cpp -o dl
timeout 5 ./dl          # exit 124 -- deadlocked
timeout 5 ./dl fixed    # completes
g++ -std=c++17 -O2 -pthread pc.cpp -o pc && ./pc
```

### L33 §2 — What sharing costs

```
g++ -std=c++17 -O2 -pthread -c sp_atomic.cpp -o sp.o && g++ -std=c++17 -O2 -pthread sp.o -o sp && ./sp
```

**Expect:** ~5.5 ns single-threaded, ~17 ns once a thread has existed, ~57–62 ns under four-thread
contention.

---

## Why This Week Is Different

Every previous week's measurement was **reproducible**. Run it again, get the same answer within noise.

**This week's are not**, and that is the subject rather than a flaw in the method:

- The `-O2` racing counter gave 4,000,000 twice and 3,000,000 once. **Same binary, same machine, same
  minute.**
- A deadlock may not deadlock, if the timing happens to work out.
- A program that passes a hundred runs can fail on the hundred-and-first, on a busier machine.

**So the discipline changes.** In earlier weeks, one careful measurement with a control was evidence.
Here, **a passing run is not evidence of anything** — and the tool that gives you evidence is
ThreadSanitizer, precisely because it reports races that *did not* manifest.

> **Everywhere else in this course, running the program was the strongest available evidence.
> This week it is the weakest**, and the instrumented run is the strong one.

That inversion is the reason Lab 10's `tracker.cpp` prints a mean of 0.99 while losing two-thirds of
its data. **The output looked right. The tool did not.**

---

## Before Week 11

1. Lectures 31–33 read; **Williams Ch. 1–3.**
2. **Midterm 2 was this week.** PS 10 is due Week 11.
3. **Confirm TSan runs on your machine** if you have not — PS 10 requires it throughout.
4. Week 11 is **lambdas, `std::function`, and modern C++**, and it explains two things this course has
   used without explaining: what you actually pass to `std::thread`, and why Week 8's `std::function`
   benchmark came out as it did.

---

*PROG 102 · Week 10 · Reading Guide · © CSE Department*
