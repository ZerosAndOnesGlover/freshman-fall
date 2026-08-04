# PROG 102 · Programming II — Object-Oriented Design and Data Structures in C++
## Week 10: Concurrency — Threads and Synchronization

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), CS 101
**Assessment for this course (overall):** Labs 20%, Problem Sets 30%, Midterms 25%, Final 15%, Projects 10%
**This week's deliverables:** PS 10, Lab 10, Quiz 10 (Monday, covers Week 9) · **MIDTERM 2 (Weeks 5–9)**

---

### Why This Week Exists

Nine weeks of this course have relied on one assumption you were never told you were making:
**only one thing happens at a time.**

Every invariant, every guarantee, every measurement assumed a single thread. This week removes that
assumption, and a surprising amount of what you know stops being true.

**The exception safety you learned last week is a good example.** The strong guarantee's "commit with a
`noexcept` swap" assumes nobody is reading during the swap. An exception escaping a thread's function
does not unwind to a caller — it calls `std::terminate`. **Week 10 does not extend Week 9; it
invalidates parts of it.**

### The Bug You Cannot Debug By Staring

Concurrency bugs are **timing-dependent**. They appear under load, on particular hardware, in
particular interleavings — and they vanish when you add a print statement.

Measured this week: four threads each incrementing a shared counter one million times, expected
4,000,000.

| Build | Result |
| --- | --- |
| `-O0` | **~1,100,000** — about 72% of increments lost |
| `-O2`, run 1 | 4,000,000 — *correct* |
| `-O2`, run 2 | 4,000,000 — *correct* |
| `-O2`, run 3 | **3,000,000** |

**The same bug, in the same program.** At `-O0` it is glaring. At `-O2` it is usually invisible and
occasionally catastrophic — and Lecture 31 §3 shows why, from the assembly.

**That is what makes this different from every previous week**, and it is why the tool matters more
here than anywhere else in the course.

### Learning Objectives

By the end of Week 10, you should be able to:

1. Start and join threads, and explain what happens if you do neither.
2. Explain a data race precisely, and demonstrate a lost update.
3. **Use ThreadSanitizer** — including getting it to run — and read its output.
4. Protect a critical section with `std::mutex` and `std::lock_guard`, and never with a bare `lock()`.
5. Produce a deadlock, and prevent it with consistent ordering or `std::scoped_lock`.
6. Use a condition variable correctly, including why the predicate form is not optional.
7. Choose between `std::atomic` and a mutex, from measurement.
8. Build a thread-safe bounded queue.
9. Explain why `shared_ptr` costs about **ten times** more under contention than it did in Week 5.

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L31 Threads and Races.md` | `std::thread`, the lost update, and why `-O2` hides it |
| `lectures/L32 Mutexes Deadlock and Condition Variables.md` | Mutual exclusion, deadlock, and waiting properly |
| `lectures/L33 Atomics and Thread-Safe Data Structures.md` | `std::atomic`, the bounded queue, and what sharing costs |
| `assignments/PS 10 A Thread-Safe Bounded Queue.md` | Due Friday of Week 11 |
| `assignments/QUIZ 10 Week 10 Monday.md` | 15 minutes, covers Week 9 |
| `lab/LAB 10 Finding Races with ThreadSanitizer.md` | Five races, found and fixed |
| `resources/MIDTERM 2 Revision Guide.md` | **Weeks 5–9, sat this week** |
| `resources/Reading Guide Week 10.md` | Williams, the memory model, and every command |
| `solutions_instructor/PS 10 Solutions.md` | Instructor only |
| `solutions_instructor/LAB 10 Solutions.md` | Instructor only |

### Before You Start: Make ThreadSanitizer Run

On some Linux kernels TSan **builds fine and dies at startup**:

```
FATAL: ThreadSanitizer: unexpected memory mapping
```

**The fix:**

```
setarch $(uname -m) -R ./your_program
```

**Verified:** under `setarch`, TSan correctly finds a real race and correctly reports **zero** warnings
on properly synchronised code. Lab 0 asked you to check this in Week 0 — **if you did not, do it
now**, before Thursday.

### The Measurement That Pays Off a Five-Week-Old Promise

Week 5 §L17 §4.1 measured a `shared_ptr` copy at about 4 ns, found that libstdc++ chooses between an
atomic and a non-atomic increment **at run time**, and said plainly: *the number is the
single-threaded cost, and Week 10 is where it bites.*

| | ns per copy |
| --- | --- |
| single-threaded | **5.3–5.9** |
| after any thread has existed | **17.0–17.2** |
| four threads sharing one control block | **56.6–61.6** |

**Roughly three times as expensive merely because a thread once ran, and ten times under contention.**
The second figure is the runtime switching paths; the third is the control block's cache line
ping-ponging between cores.

### Midterm 2 Is This Week

**75 minutes, covering Weeks 5–9**, one handwritten sheet, one side. The revision guide is in
`resources/`. **This week's material is not examinable on it.**

### Connections

**Back:** **Week 5**'s atomic refcount, finally measured where it matters. **Week 9**'s guarantees,
several of which do not survive. **Week 8**'s Observer, whose subscriber list is now shared mutable
state.

**Forward:** **Week 11** is lambdas, which is what you pass to a thread. **Week 12**'s cache-aware
programming explains the 10× contention figure properly — false sharing is the same phenomenon.

---

*PROG 102 · Week 10 · © CSE Department*
