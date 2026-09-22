# PROG 102 · Problem Set 10 — Solutions and Marking Notes
## A Thread-Safe Bounded Queue

**INSTRUCTOR COPY — not for distribution**

---

## Before Marking

**Reference environment:** g++ 13.3.0, x86-64 Linux, 8 hardware threads.

**Race outcomes are not reproducible.** Mark the *shape* of the result and the reasoning, never the
exact numbers. A student whose `-O2` counter never lost an increment across five runs has an honest
result — and A2(a) is where they should say so.

**Every part requires TSan.** A submission with no TSan output has not done the work regardless of how
good the code is.

---

> **Revised 2026-09-22.** Removed Part A (races at -O0/-O2 and `volatile` — Lecture 31 §3's measurement, which Lab 10 also
> runs) and Part C (the cost of atomics, mutexes and `shared_ptr` sharing — Lecture 33 §2 and L32 §2).
> Old B and D are A and B; re-weighted to keep 100.

## Part A — The Bounded Queue (60)

### A1 (24), A2 (12)

Reference implementation is L33 §3. Required: two condition variables, predicate `wait`, a `done` flag,
`notify_all` in `close()`.

```
produced 60000, consumed 60000, sum 60000  OK
```

TSan-clean.

*Marking B1: 4 correct blocking on both ends, 3 two CVs, 3 predicate form, 2 the shutdown flag, 2
`notify_all`.*
*Marking B2: 5 the test with 3+3, 3 the TSan run.*

**A single condition variable is a 3-point deduction** and worth explaining: a consumer waiting for
"not empty" being woken by a producer's "not full" is a correctness-preserving inefficiency that
becomes a bug the moment someone converts `notify_all` to `notify_one`.

### A3 (12)

- **(a)** Without the flag, consumers block forever on `not_empty`. **The program produces correct
  output and never exits.**
- **(b)** With `notify_one` in `close()`, one consumer wakes and the rest hang. **Same symptom, and it
  depends on the number of consumers**, so it may pass with one.
- **(c)** Without the predicate, a consumer can wake on a stolen notification and proceed on an empty
  queue — typically a crash or garbage from `q.front()`.

*Marking: 2 each. **The "how long did it take you to notice" is not marked but should be read** — the
honest answers are illuminating and (a) is often "I thought it had finished".*

### A4 (12)

**(a)** Two reasons: a `T pop()` cannot signal "closed and empty" except by throwing; and if `T`'s move
throws **after** the element is removed, **the element is lost** — no guarantee is achievable.

**(b)** `if (!q.empty()) q.pop();` — another thread can drain the queue between the two calls. **The
fix is an interface change** because no amount of locking *inside* `empty()` and `pop()` makes the
*pair* atomic: composing two atomic operations does not produce an atomic operation.

*Marking: 3 + 3. **(b)'s "composition is not atomic" is the assessed idea.** "Add a mutex around both"
gets 1 — the caller cannot, because the lock is inside the class.*

---

## Part B — Deadlock (40)

### B1 (12)

Exit **124** under `timeout` — the program hangs.

*Marking: 6. **Require a timeout**; a student who ran it without one and had to kill the terminal
should still get the marks if they report it.*

### B2 (14)

Both fixes complete. `std::scoped_lock` works **even with opposite argument orders**.

*Marking: 3 each.*

### B3 (14)

**(a)** Mutual exclusion, hold-and-wait, no preemption, circular wait. **Consistent ordering breaks
circular wait**; `scoped_lock` also breaks it, by acquiring all-or-nothing rather than incrementally
(so hold-and-wait is arguably what it breaks — **accept either with a good argument**).

**(b)** **TSan does not detect a deadlock that occurs** — the process simply hangs and TSan hangs with
it. It *can* report a lock-order inversion that might deadlock, if it observes both orders. **The limit:
a tool that watches execution cannot report on execution that stopped.**

*Marking: 3 + 3. **(b) must state that the hang defeats the tool.** A student who found TSan's
lock-order-inversion warning has done extra work and should be commended.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 60 |
| B | 40 |
| **Total** | **100** |

---

## What to Watch For

1. **A single condition variable** in A1.
2. **"Add a mutex around both"** in A4(b) — the caller cannot.
3. **No TSan output anywhere.** The set requires it throughout.

---

## Feeding Into Week 11 and the Final

Week 11 explains what students have been passing to `std::thread` all week: a lambda, and specifically
how its captures work. **Lecture 33 §2's `shared_ptr` result is worth revisiting there** — a lambda capturing a
`shared_ptr` **by value**, launched on four threads, is exactly the 57 ns case, and it is the single
most common way real code stumbles into it.

**Week 10's material is on the final**, not on Midterm 2. Say so — several students will assume the
opposite.

---

*PROG 102 · Week 10 · PS 10 Solutions · © CSE Department*
