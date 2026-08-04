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

## Part A — Races, Measured (24)

### A1 (8)

Reference: `-O0` gives ~1,100,000 of 4,000,000 consistently; `-O2` gives 4,000,000 most runs with
occasional losses of a round million.

*Marking: 8 for ten runs reported. **Accept any distribution** — the point is that they ran it enough
times to see variation.*

### A2 (6)

**(a)** At `-O0` the loss is large and consistent (~72%). At `-O2` the answer is usually **correct**
and occasionally wrong by a whole thread's contribution.

**(b)**

```asm
mov     rdx, QWORD PTR plain[rip]     ; ONE load
lea     rax, 1[rdx+rax]               ; add n
mov     QWORD PTR plain[rip], rax     ; ONE store
```

**The compiler hoisted the counter into a register and collapsed the loop into a single
read-modify-write.** It is **allowed to** because a data race is undefined behaviour — it may assume no
other thread touches `plain`.

*Marking: 3 + 3. **Full marks for (b) require the "because it is UB" step.** "The compiler optimised
it" is 1 of the 3 — the question is why that was legal.*

### A3 (4)

`volatile` at `-O2`: roughly **1.0–1.1M of 4M**, and **TSan still reports races**.

**What `volatile` did:** it suppressed the hoisting, restoring a real million read-modify-writes — so
the loss rate went **back up to the `-O0` level**. It prevents an optimization; it provides no
synchronisation, no atomicity and no ordering between cores.

*Marking: 2 the results, 2 the explanation. **A student who reports `volatile` as an improvement has
misread their own numbers.** It makes the count worse.*

### A4 (6)

**Yes**, TSan reports a race on runs that produced 4,000,000.

**Why that is what you want:** the race exists whether or not it manifested. A tool that only reported
observed corruption would be useless, because the `-O2` version usually does not corrupt — and would
ship.

*Marking: 3 the demonstration, 3 the reasoning.*

---

## Part B — The Bounded Queue (34)

### B1 (14), B2 (8)

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

### B3 (6)

- **(a)** Without the flag, consumers block forever on `not_empty`. **The program produces correct
  output and never exits.**
- **(b)** With `notify_one` in `close()`, one consumer wakes and the rest hang. **Same symptom, and it
  depends on the number of consumers**, so it may pass with one.
- **(c)** Without the predicate, a consumer can wake on a stolen notification and proceed on an empty
  queue — typically a crash or garbage from `q.front()`.

*Marking: 2 each. **The "how long did it take you to notice" is not marked but should be read** — the
honest answers are illuminating and (a) is often "I thought it had finished".*

### B4 (6)

**(a)** Two reasons: a `T pop()` cannot signal "closed and empty" except by throwing; and if `T`'s move
throws **after** the element is removed, **the element is lost** — no guarantee is achievable.

**(b)** `if (!q.empty()) q.pop();` — another thread can drain the queue between the two calls. **The
fix is an interface change** because no amount of locking *inside* `empty()` and `pop()` makes the
*pair* atomic: composing two atomic operations does not produce an atomic operation.

*Marking: 3 + 3. **(b)'s "composition is not atomic" is the assessed idea.** "Add a mutex around both"
gets 1 — the caller cannot, because the lock is inside the class.*

---

## Part C — What Sharing Costs (24)

### C1 (8)

| | result | time |
| --- | --- | --- |
| unsynchronised | ~1.1M (wrong) | 12–16 ms |
| `std::atomic` | 4,000,000 | 69.5–72.1 ms |
| `std::mutex` | 4,000,000 | 240–251 ms |

**The atomic is ~3.5× faster than the mutex.**

*Marking: 6 the three measurements, 2 the comparison.*

### C2 (10)

| | ns per copy |
| --- | --- |
| single-threaded | 5.3–5.9 |
| after a thread has existed | 17.0–17.2 |
| four threads, one control block | 56.6–61.6 |

**The two jumps:**

- **5.9 → 17 ns is not contention.** It is libstdc++ switching from its non-atomic to its atomic
  refcount path, having observed that the program is threaded. The program is effectively
  single-threaded at that point and the cost still tripled.
- **17 → 57 ns is contention** — the control block's cache line ping-ponging between four cores.

*Marking: 6 the three figures, 4 the two explanations. **Full marks require identifying that the first
jump is not contention.** A student who calls both "contention" gets 1 of the 4 — and this is the
question Week 5 §L17 §4.1 was setting up.*

### C3 (6)

Reference, four threads, each with its **own** `shared_ptr` to its **own** object:

| | ns per copy |
| --- | --- |
| shared control block | 64.4–64.8 |
| **separate control blocks** | **4.26–4.32** |
| ratio | **~15×** |

**Note the separate figure is *lower* than the single-threaded 5.3–5.9 ns**, which surprises people and
is correct: each core holds its own control block's cache line exclusively and never gives it up, so
the atomic instruction is uncontended and the four threads run in parallel.

**The atomic path is still in use in both rows.** The entire 15× is contention — specifically, the
shared cache line being transferred between cores on every increment.

*Marking: 3 the measurement, 3 the explanation. **The explanation must distinguish "atomic" from
"contended"** — the same distinction as C2, and here it is the whole effect. A student who notices the
separate case beats single-threaded, and explains it, deserves a commendation.*

---

## Part D — Deadlock (18)

### D1 (6)

Exit **124** under `timeout` — the program hangs.

*Marking: 6. **Require a timeout**; a student who ran it without one and had to kill the terminal
should still get the marks if they report it.*

### D2 (6)

Both fixes complete. `std::scoped_lock` works **even with opposite argument orders**.

*Marking: 3 each.*

### D3 (6)

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
| A | 24 |
| B | 34 |
| C | 24 |
| D | 18 |
| **Total** | **100** |

---

## What to Watch For

1. **"The compiler optimised it"** in A2(b) without the undefined-behaviour step.
2. **Reporting `volatile` as an improvement** (A3), contradicting their own numbers.
3. **A single condition variable** in B1.
4. **"Add a mutex around both"** in B4(b) — the caller cannot.
5. **Calling both C2 jumps "contention"** — the first is not.
6. **No TSan output anywhere.** The set requires it throughout.

---

## Feeding Into Week 11 and the Final

Week 11 explains what students have been passing to `std::thread` all week: a lambda, and specifically
how its captures work. **C2's `shared_ptr` result is worth revisiting there** — a lambda capturing a
`shared_ptr` **by value**, launched on four threads, is exactly the 57 ns case, and it is the single
most common way real code stumbles into it.

**Week 10's material is on the final**, not on Midterm 2. Say so — several students will assume the
opposite.

---

*PROG 102 · Week 10 · PS 10 Solutions · © CSE Department*
