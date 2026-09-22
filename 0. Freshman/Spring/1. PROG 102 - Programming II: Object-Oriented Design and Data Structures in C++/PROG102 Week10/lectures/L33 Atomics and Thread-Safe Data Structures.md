# PROG 102 · Lecture 33
## Atomics and Thread-Safe Data Structures

**Week 10 · Thursday · 50 minutes**
**Reading:** Williams Ch. 5, Ch. 6.1–6.2 · **Assumes:** L31, L32, Week 5

**Date:** Thursday 1 April 2027 · 10:00–10:50 · Week 10

---

## 1. `std::atomic`

```cpp
std::atomic<long> counter{0};
++counter;                     // one indivisible operation
```

**An atomic operation cannot be interrupted partway.** The load-increment-store of L31 §2 becomes a
single `lock`-prefixed instruction the hardware executes as a unit.

Measured, four threads × one million increments:

| | result | time |
| --- | --- | --- |
| unsynchronised | ~1,100,000 | 12–16 ms |
| **`std::atomic`** | **4,000,000** | **69.5–72.1 ms** |
| `std::mutex` | 4,000,000 | 240–251 ms |

**Correct, and about 3.5× cheaper than the mutex.**

### 1.1 What Atomics Can Do

```cpp
std::atomic<int> a{0};
a.store(5);  a.load();
a.fetch_add(3);           // ++, +=
a.exchange(7);            // set and return the old value
int expected = 7;
a.compare_exchange_strong(expected, 9);    // set to 9 only if it is still 7
```

**`compare_exchange` is the primitive everything else is built on.** It is how you implement a
lock-free update:

```cpp
int old = a.load();
while (!a.compare_exchange_weak(old, f(old))) { }   // retry if someone changed it
```

### 1.2 What They Cannot Do

**An atomic protects one variable. It does not protect an invariant across two.**

```cpp
std::atomic<int> size{0};
std::atomic<int> capacity{10};
// another thread can observe size > capacity between these two updates
```

**Both variables are atomic and the pair is racy.** If two values must agree, you need a mutex — there
is no way to make two atomics into one transaction.

**Nor is `std::atomic<T>` lock-free for every `T`.** For large types the library falls back to an
internal lock:

```cpp
std::atomic<BigStruct> b;
b.is_lock_free();          // may be false
```

> **Rule from L32 §2, restated: an atomic protects a variable; a mutex protects an invariant.** The
> question is not "which is faster" but "how many things must be consistent".

### 1.3 Memory Ordering — A Signpost

Every atomic operation takes an optional ordering:

```cpp
a.store(1, std::memory_order_release);
a.load(std::memory_order_acquire);
```

The default, `memory_order_seq_cst`, is the strongest and the slowest, and **it is what you should
use.** Relaxed orderings are faster and are where experts write bugs that appear only on ARM.

**This course does not require you to use anything but the default.** Know that the parameter exists,
know that the default is sequentially consistent, and treat weaker orderings as a specialism.

---

## 2. What Sharing Actually Costs

**Week 5 §L17 §4.1** measured a `shared_ptr` copy at about 4 ns, discovered that libstdc++ chooses
between an atomic and a non-atomic increment **at run time**, and said: *that is the single-threaded
cost, and Week 10 is where it bites.*

Measured now, 5,000,000 copies:

| | ns per copy | vs single-threaded |
| --- | --- | --- |
| single-threaded | **5.3–5.9** | 1.0× |
| after any thread has existed | **17.0–17.2** | **~3×** |
| four threads sharing one control block | **56.6–61.6** | **~10×** |

**Three separate effects, and they are worth separating.**

**5.9 → 17 ns** is the runtime switching from the non-atomic to the atomic path. The program is still
effectively single-threaded — one `std::thread` was created and joined — and the cost tripled.
**libstdc++ decides once and never goes back.**

**17 → 57 ns** is **contention**. Four cores are incrementing the same reference count, and that
counter lives in one cache line. Every increment must take exclusive ownership of that line, so the
line ping-pongs between cores.

> **The object being pointed at is not shared in any meaningful sense — nobody writes to it.** The
> *reference count* is shared, and that is enough to serialise four cores.
>
> **This is the deepest reason `shared_ptr` is not a safe default** (L17 §7), and it is stronger than
> the Week 5 argument. Not "it costs 4 ns" but: **passing `shared_ptr` by value in a hot path on
> several threads turns an uncontended program into a contended one, through a counter you never
> think about.**
>
> **Pass `const shared_ptr&` or a reference to the pointee.** Week 12 explains the cache mechanism
> directly; this is **false sharing**, and it is the same phenomenon.

---

## 3. A Thread-Safe Bounded Queue

The producer-consumer structure from L32 §5, and PS 10's deliverable:

```cpp
template <typename T>
class BoundedQueue {
    std::queue<T> q;
    std::size_t   cap;
    mutable std::mutex m;
    std::condition_variable not_full, not_empty;
    bool done = false;
public:
    explicit BoundedQueue(std::size_t c) : cap(c) {}

    void push(T v) {
        std::unique_lock<std::mutex> lk(m);
        not_full.wait(lk, [&]{ return q.size() < cap; });
        q.push(std::move(v));
        lk.unlock(); not_empty.notify_one();
    }
    bool pop(T& out) {
        std::unique_lock<std::mutex> lk(m);
        not_empty.wait(lk, [&]{ return !q.empty() || done; });
        if (q.empty()) return false;
        out = std::move(q.front()); q.pop();
        lk.unlock(); not_full.notify_one();
        return true;
    }
    void close() {
        { std::lock_guard<std::mutex> g(m); done = true; }
        not_empty.notify_all();
    }
};
```

```
produced 60000, consumed 60000, sum 60000  OK   (3 producers, 3 consumers, three runs)
```

### 3.1 Why the Interface Looks Like That

**`bool pop(T& out)` rather than `T pop()`.** A `T pop()` cannot signal "the queue is closed and empty"
except by throwing, and it has a worse problem: if `T`'s move constructor throws *after* the element
has been removed, **the element is lost** — the queue no longer has it and the caller never got it.
**That is Week 9's strong guarantee, unachievable in a `T pop()` signature.**

**No `empty()` or `size()` — or if there is, they are useless.** By the time the caller sees the answer,
another thread may have changed it. **A thread-safe container cannot have a meaningful `empty()`**,
which is why `if (!q.empty()) q.pop();` is a race even when both operations are individually
thread-safe.

> **This is the deepest lesson of the week about interfaces.** Making each operation thread-safe does
> **not** make the class thread-safe. Composition of atomic operations is not atomic, and the fix is
> to design operations that do the whole job — `pop` that waits and returns a status, rather than
> `empty` followed by `pop`.

---

## 4. What Week 9 Loses

Worth stating explicitly, because it is easy to assume the guarantees carry over.

- **An exception escaping a thread calls `std::terminate`** (L31 §1.1). There is no caller.
- **The strong guarantee's commit-by-swap assumes nobody is reading during the swap.** With a mutex
  held it still works; without one it does not.
- **`noexcept` is more load-bearing**, since there is nowhere for a throw to go.
- **A destructor running while another thread holds a reference** is a lifetime bug no guarantee
  addresses — which is what `shared_ptr` exists for, at the cost measured in §2.

**To move an exception between threads you must do it explicitly** — `std::promise`/`std::future`, or
catching and storing a `std::exception_ptr` and rethrowing it in the joining thread.

---

## 5. Summary

| Idea | The point |
| --- | --- |
| `std::atomic` | Indivisible. **4,000,000 correct, 69.5–72.1 ms** |
| vs mutex | ~3.5× cheaper |
| `compare_exchange` | The primitive under lock-free algorithms |
| **Two atomics are not a transaction** | An atomic protects a variable; a mutex protects an invariant |
| Memory ordering | Default `seq_cst`; weaker orderings are a specialism |
| `shared_ptr` single-threaded | **5.3–5.9 ns** |
| after a thread exists | **17.0–17.2 ns** — the runtime switched paths, permanently |
| four threads contending | **56.6–61.6 ns** — the control block's cache line ping-pongs |
| `bool pop(T&)` | A `T pop()` cannot be strongly exception-safe |
| **No meaningful `empty()`** | Thread-safe operations do not compose into a thread-safe class |
| Week 9 partially invalidated | No caller to unwind to |

---

## 6. Exercises

**1.** Reproduce §1's table: unsynchronised, atomic and mutex. Report results and times.

**2.** Implement a lock-free counter with `compare_exchange_weak`. Compare its time with
`fetch_add`. **Which is faster, and why might that surprise you?**

**3.** Write two `std::atomic<int>`s that must satisfy `size <= capacity`. **Construct a program where
another thread observes the invariant violated**, and confirm TSan is silent about it.

**Then explain why TSan's silence is correct.**

**4.** Reproduce §2's three `shared_ptr` measurements. **Report all three**, and say which of the two
jumps is the runtime switching paths and which is contention.

**5.** Take the four-thread case and give each thread its **own** `shared_ptr` to its **own** object.
**Report the per-copy time** and explain the difference.

**6.** Implement the bounded queue and test it with 3 producers and 3 consumers over at least 50,000
items. Run it under ThreadSanitizer.

**7.** Add `bool empty() const` to your queue. **Write a program using `if (!q.empty()) q.pop();` that
fails**, and run it under TSan. Then explain why the fix is an interface change rather than more
locking.

---

## 7. Next

**Week 11** is lambdas, `std::function`, and modern C++ — including a proper explanation of Week 8's
`std::function` benchmark. It is also where the callable you pass to `std::thread` gets explained
properly.

**Midterm 2 was this week.** Week 11's material is on the final.

---

*PROG 102 · Week 10 · Lecture 33 · © CSE Department*
