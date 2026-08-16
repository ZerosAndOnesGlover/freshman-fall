# PROG 102 · Lecture 32
## Mutexes, Deadlock, and Condition Variables

**Week 10 · Wednesday · 50 minutes**
**Reading:** Williams Ch. 3–4 · **Assumes:** L31, Week 5 (RAII)

**Date:** Wednesday 24 March 2027 · 10:00–10:50 · Week 10

---

## 1. Mutual Exclusion

A **mutex** ensures that only one thread at a time is inside a **critical section**.

```cpp
std::mutex m;
int counter = 0;

{
    std::lock_guard<std::mutex> g(m);      // locks
    ++counter;                              // critical section
}                                           // unlocks -- always
```

**Never call `m.lock()` and `m.unlock()` yourself.** An early return, a `break`, or an exception
between them leaves the mutex locked forever, and every other thread blocks on it permanently.

`std::lock_guard` is **RAII** (Week 5) applied to a lock: acquire in the constructor, release in the
destructor. **Unwinding releases it** (L28 §2), which is exactly the property you need.

| Type | Use |
| --- | --- |
| `std::lock_guard` | Simple scoped locking. **The default.** |
| `std::unique_lock` | When you must unlock early, or hand it to a condition variable |
| `std::scoped_lock` | **Two or more mutexes at once** — §3.2 |

---

## 2. It Works, and It Costs

From L31 §3, four threads × one million increments:

| | result | time |
| --- | --- | --- |
| unsynchronised (`-O0`) | ~1,100,000 | 12–16 ms |
| **`std::atomic`** | **4,000,000** | **69.5–72.1 ms** |
| **`std::mutex`** | **4,000,000** | **240–251 ms** |

**Both are correct. The mutex is about 3.5× the atomic**, and both are far slower than the broken
version — which is the honest shape of this trade: **correctness costs, and the wrong answer is always
available cheaply.**

The mutex is more expensive because locking and unlocking is a function call each way, with a kernel
futex wait under contention. **The atomic is a single `lock`-prefixed instruction.**

> **Use an atomic when the critical section is one variable and one operation.** Use a mutex when it is
> anything more — two variables that must agree, a container, an invariant spanning several fields.
> **A mutex protects an invariant; an atomic protects a variable.**

---

## 3. Deadlock

Mutexes introduce a failure mode races do not have. **Nothing goes wrong, and nothing happens.**

```cpp
// Thread 1                      // Thread 2
lock(a);                         lock(b);
lock(b);   // waits for T2       lock(a);   // waits for T1
```

Each holds what the other needs. Measured, with 1,000 iterations and a one-microsecond delay between
the two locks:

```
INCONSISTENT ordering
exit=124        (timed out after 5s -- deadlocked)
```

**The program did not crash. It stopped**, and no sanitizer fires — TSan can detect *lock-order
inversions* that might deadlock, but a deadlocked process simply hangs.

### 3.1 The Four Conditions

Deadlock requires all four (Coffman's conditions):

1. **Mutual exclusion** — a resource is held exclusively.
2. **Hold and wait** — a thread holds one and waits for another.
3. **No preemption** — the resource cannot be taken away.
4. **Circular wait** — a cycle in the "waits for" graph.

**Break any one and deadlock becomes impossible.** In practice you break the fourth.

### 3.2 The Fixes

**Consistent lock ordering.** If every thread locks `a` before `b`, no cycle can form. **This is the
standard answer** and it costs nothing — but it requires a global convention, which is hard to maintain
in a large codebase.

**`std::scoped_lock`** — locks several mutexes with a deadlock-avoidance algorithm:

```cpp
std::scoped_lock lk(a, b);        // in one thread
std::scoped_lock lk(b, a);        // in another -- STILL SAFE
```

Verified: with the argument order **deliberately opposite** in the two threads, the program completes.

```
consistent (std::scoped_lock) ordering
completed
exit=0
```

> **`std::scoped_lock` is the answer whenever you need two mutexes.** It is one line, it is safe
> regardless of argument order, and it removes the need for a global convention. C++11 spells it
> `std::lock`; C++17 gave it a proper RAII wrapper.

**Other approaches:** a lock hierarchy (never acquire a lower-level lock while holding a higher-level
one), or `try_lock` with backoff. Both are for when the above are not enough.

### 3.3 Livelock

Threads that are running, responding to each other, and making no progress — two people stepping aside
in a corridor, repeatedly. **Rarer than deadlock, harder to detect** (the CPU is busy, so nothing looks
stuck), and usually caused by naive retry-on-failure loops with no randomised backoff.

---

## 4. Condition Variables

A mutex protects data. **A condition variable lets a thread wait for the data to become interesting.**

The problem: a consumer must wait until the queue is non-empty. Spinning on `while (q.empty()) {}`
burns a whole core, and sleeping in a loop is arbitrary and slow.

```cpp
std::mutex m;
std::condition_variable not_empty;
std::queue<int> q;

// consumer
std::unique_lock<std::mutex> lk(m);
not_empty.wait(lk, [&]{ return !q.empty(); });      // atomically unlocks and sleeps
int v = q.front(); q.pop();

// producer
{ std::lock_guard<std::mutex> g(m); q.push(42); }
not_empty.notify_one();
```

**`wait` unlocks the mutex, sleeps, and relocks it on waking — atomically.** That atomicity is the
whole reason condition variables exist; doing it by hand has a window in which the notification is
lost.

### 4.1 Always Use the Predicate Form

```cpp
cv.wait(lk, [&]{ return !q.empty(); });     // correct
cv.wait(lk);                                // almost always wrong
```

**Two reasons, and both are real:**

**Spurious wakeups.** `wait` may return without any notification, and the standard permits it. Without
a predicate you proceed on a queue that is still empty.

**Stolen wakeups.** `notify_one` wakes one waiter; between its waking and its relocking the mutex,
another thread may take the item. The predicate is re-checked after relocking, so the waiter goes back
to sleep.

**The predicate form is exactly `while (!pred()) wait(lk);`**, and writing that loop yourself is
correct too. What is not correct is checking once.

### 4.2 `notify_one` or `notify_all`

- **`notify_one`** when any single waiter can handle the event — a queue with interchangeable
  consumers. Cheaper.
- **`notify_all`** when waiters are waiting on *different* conditions, or when the state change might
  satisfy several — and always for a shutdown flag, where every waiter must wake.

> **A shutdown that uses `notify_one` is a hang waiting to happen.** Lecture 33's bounded queue uses
> `notify_all` in `close()` for exactly this reason.

---

## 5. Putting It Together

```cpp
template <typename T>
class BoundedQueue {
    std::queue<T> q;
    std::size_t   cap;
    mutable std::mutex m;
    std::condition_variable not_full, not_empty;
    bool done = false;
public:
    void push(T v) {
        std::unique_lock<std::mutex> lk(m);
        not_full.wait(lk, [&]{ return q.size() < cap; });
        q.push(std::move(v));
        lk.unlock();                       // unlock BEFORE notifying
        not_empty.notify_one();
    }
    bool pop(T& out) {
        std::unique_lock<std::mutex> lk(m);
        not_empty.wait(lk, [&]{ return !q.empty() || done; });
        if (q.empty()) return false;       // closed and drained
        out = std::move(q.front()); q.pop();
        lk.unlock();
        not_full.notify_one();
        return true;
    }
    void close() {
        { std::lock_guard<std::mutex> g(m); done = true; }
        not_empty.notify_all();            // ALL -- every consumer must wake
    }
};
```

Verified with 3 producers, 3 consumers, 20,000 items each:

```
produced 60000, consumed 60000, sum 60000  OK
produced 60000, consumed 60000, sum 60000  OK
produced 60000, consumed 60000, sum 60000  OK
```

**Three details that are easy to get wrong:**

- **Two condition variables**, not one. A consumer waiting for "not empty" should not be woken by a
  producer's "not full".
- **Unlock before notifying.** Otherwise the woken thread immediately blocks on the mutex you still
  hold. Correct either way; this is faster.
- **`done` plus `notify_all`.** Without a shutdown flag, consumers wait forever on a queue nobody will
  fill. **This is the most common bug in student implementations** and it presents as a program that
  produces correct output and never exits.

---

## 6. Summary

| Idea | The point |
| --- | --- |
| `std::lock_guard` | RAII for locks. **Never `lock()`/`unlock()` by hand** |
| Mutex vs atomic, measured | 240–251 ms vs 69.5–72.1 ms — **~3.5×** |
| Which to use | **A mutex protects an invariant; an atomic protects a variable** |
| Deadlock | Verified: **exit 124**, timed out. Nothing crashes; nothing happens |
| Four conditions | Break circular wait |
| `std::scoped_lock` | Safe **even with opposite argument order** — verified |
| Livelock | Running, responsive, no progress |
| `cv.wait(lk, pred)` | **Always** the predicate form — spurious and stolen wakeups |
| `notify_all` for shutdown | `notify_one` leaves consumers asleep forever |
| The bounded queue | Two CVs, unlock before notify, a `done` flag |

---

## 7. Exercises

**1.** Take L31's racing counter and fix it with `std::lock_guard`. Confirm 4,000,000 and confirm TSan
is silent. **Report the time** and compare with the atomic version.

**2.** Replace the `lock_guard` with manual `lock()`/`unlock()` and add an early `return` between them.
**What happens to the other threads?**

**3.** Reproduce the deadlock in §3, with a timeout. **Report the exit code.** Then fix it two ways —
consistent ordering and `std::scoped_lock` — and show both completing.

**4.** With `std::scoped_lock`, deliberately pass the mutexes in **opposite orders** in the two threads.
**Does it still work?** Explain why.

**5.** Write a consumer using `cv.wait(lk)` without a predicate. **Construct a case where it proceeds on
an empty queue.** *(A stolen wakeup is easier to force than a spurious one — use three consumers.)*

**6.** Implement the bounded queue from §5. Test it with 3 producers and 3 consumers. **Then remove the
`done` flag** and report what happens at shutdown.

**7.** Change `close()` from `notify_all` to `notify_one` with three consumers. **What happens, and how
long does it take you to notice?**

---

## 8. Next

**Lecture 33** covers `std::atomic` properly — what it can and cannot do — and returns to a promise
made in **Week 5**: `shared_ptr`'s reference count was measured at about 4 ns and described as "the
single-threaded cost". This week it is ten times that.

---

*PROG 102 · Week 10 · Lecture 32 · © CSE Department*
