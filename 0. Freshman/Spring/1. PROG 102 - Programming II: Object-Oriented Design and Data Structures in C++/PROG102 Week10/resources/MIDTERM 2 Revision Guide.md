# PROG 102 · Midterm 2 · Revision Guide
## Weeks 5–9

**Sat Tuesday 30 March 2027, 18:00–19:30 (Week 10, VNC 100) · a 75-minute paper · 12.5% of the course grade**
**Closed book, closed device. One handwritten sheet of A4, one side only.**

---

## What Is Examinable

**Lectures 16–30, Problem Sets 5–9, and Labs 5–9.** Plus **Project 1**, in the sense that the design
decisions it required are fair game.

**Week 10's material is not examinable.** Threads, mutexes and atomics are on the final, not on this
paper.

### The Shape of the Paper

Identical to Midterm 1:

| Section | Marks | What it asks |
| --- | --- | --- |
| **A — Short answer** | 30 | 10 questions, 3 marks each |
| **B — Code reading** | 30 | What does this do, what is wrong with it, what does the compiler say |
| **C — Code writing** | 25 | Write a class or an operation correctly, on paper |
| **D — Explain a measurement** | 15 | A table of numbers; what it shows and what it does not |
| **Total** | **100** | |

**Section D again.** Midterm 1's Section D was the most under-prepared part of the paper. It is 15
marks for explaining numbers you have already produced.

---

## The Ten Things Most Likely to Appear

1. **`unique_ptr` vs `shared_ptr` vs `weak_ptr`** — which, when, and what each costs. *(L16, L17)*
2. **Why `unique_ptr` is "cheaper than free"** — the raw version leaks on an exception. *(L16 §5.3)*
3. **The reference cycle**, and how `weak_ptr` breaks it. *(L17 §5–6)*
4. **`std::move` is a cast** and moves nothing; the moved-from state. *(L18 §4)*
5. **Rule of Five vs Rule of Zero**, and when Zero does not apply. *(L18 §7, L19 §4)*
6. **The sentinel node**, and why it removes three cases. *(L19 §3)*
7. **Iterator categories** — declaring one you cannot honour. *(L20 §5)*
8. **The three exception guarantees**, and determining one by testing. *(L29)*
9. **`noexcept`** — where it is load-bearing and what a lie costs. *(L30 §1)*
10. **Assertion vs exception**, and the `operator[]`/`at()` split. *(L30 §2, §3.1)*

---

## Week-by-Week Checklist

### Week 5 — RAII and Smart Pointers

- [ ] RAII in one sentence; the destructor is the mechanism
- [ ] `unique_ptr` = exclusive ownership; not copyable, and why that is the design
- [ ] `sizeof`: `unique_ptr` **8**, `shared_ptr` **16**, `weak_ptr` **16**
- [ ] Passing the **pointee** generates byte-identical code to a raw pointer
- [ ] `const unique_ptr<T>&` is **the wrong parameter type** — and why
- [ ] The ownership case differs by **exception landing pads** — not overhead
- [ ] Raw `new`/`delete` **leaks on a throw**: `allocs=2 frees=1`, at `-O0` and `-O2`
- [ ] The benchmark trap: an unconditional throw let `-O2` **delete the allocation**
- [ ] `make_shared` = **1** allocation; `shared_ptr(new W)` = **2**
- [ ] `shared_ptr` copy ≈ **4 ns**; by reference is already ~3.5× a raw pointer
- [ ] The refcount path is chosen **at run time** — that figure is single-threaded
- [ ] **Cycles leak**: 80 bytes, 2 allocations, **no destructors ran**
- [ ] `weak_ptr::lock()` is the only safe access; `expired()`-then-use is a race
- [ ] `std::move` is a **cast**; moved-from is *valid but unspecified* (except `unique_ptr`: null)
- [ ] `return std::move(x)` is **wrong** — `-Wpessimizing-move`
- [ ] Without `noexcept`, `vector` growth **copies**
- [ ] **Rule of Zero** — and RAII does **not** fix Week 4's virtual destructor rule

### Week 6 — Implementing Containers

- [ ] The **sentinel**: four insertion cases become one; `end()` is a real node
- [ ] `prev`/`next` are raw pointers because they are **structure, not ownership**
- [ ] Rule of **Five** here, because you are the resource wrapper
- [ ] A move must leave a **valid empty list**, not a wreck
- [ ] Invalidation is a **consequence** of where elements live
- [ ] The five `iterator_traits` typedefs; the category is a **tag type**
- [ ] `template <bool Const>`; the `iterator` → `const_iterator` converting constructor
- [ ] **`std::sort` refusing your iterator is the pass condition**
- [ ] Lying about the category: sorts **correctly**, at $O(n^2 \log n)$ — 8.6 / 39.4 / 194.4 ms
- [ ] BST with `unique_ptr` children needs **zero** of the five
- [ ] Height in **edges**; empty = **−1**; sorted input gives height $n-1$
- [ ] **The recursive destructor**: fine at 500,000, **segfaults at 1,000,000**

### Week 7 — Creational and Structural Patterns

- [ ] The two principles: composition over inheritance; program to interfaces
- [ ] A pattern solves **change**; name the change it makes easy
- [ ] Meyers' Singleton; thread-safe by language guarantee; `__cxa_guard_acquire`
- [ ] Why Singleton is usually the wrong answer
- [ ] Factory Method; a type-switch **at a boundary** is acceptable
- [ ] Abstract Factory: adding a family is free, adding a **product** is expensive
- [ ] Builder: more than ~4 parameters, or any `bool`
- [ ] Adapter can **restrict** as well as translate (`std::stack`)
- [ ] Decorator: $2^n$ vs $n$ — **10 features: 1024 vs 10** — at **~0.58 ns per layer**
- [ ] Composite; Facade

### Week 8 — Behavioural Patterns

- [ ] Observer; the naive version gives `stack-use-after-scope`
- [ ] `weak_ptr` observers skip and prune; **no `detach`**; the count is stale
- [ ] Five things Observer does **not** solve
- [ ] Strategy; the Open/Closed Principle
- [ ] **Four ways to pass a comparison**: virtual 166, **`std::function` 296**, lambda 160, default 150 ms
- [ ] `std::function` is slowest — **type erasure blocks inlining**, as with `qsort` in Week 3
- [ ] Command; **undo is what justifies it**; 20 lines/4 types vs 8 lines/2 types
- [ ] Template Method; the Hollywood Principle; prefer Strategy
- [ ] State; behaviour localised, **transitions distributed**
- [ ] What C++11 obsoleted — **and what it did not**

### Week 9 — Exception Safety

- [ ] Unwinding destroys **objects, not allocations** — a raw `new[]` leaked 400 bytes
- [ ] Catch by `const&`; catching by value **slices**
- [ ] `throw;` not `throw e;`
- [ ] `logic_error` vs `runtime_error`
- [ ] **Time on the happy path is free** (1.53–1.66 vs 1.49–1.60 ns)
- [ ] **Code size is not**: **240 vs 88 bytes**
- [ ] A throw costs **~1.68 µs**, ~1000× a call
- [ ] The **four** states: nothrow, strong, basic, **none**
- [ ] Basic: 2 → **4**. Strong: 2 → **2**
- [ ] The strong recipe: risky work on a copy, commit with a `noexcept` swap
- [ ] **Copy-and-swap was the strong guarantee all along**
- [ ] Strong costs a copy — why `vector::insert` is only basic
- [ ] Determining a guarantee by **sweeping the failure point**
- [ ] The guarantee is the **weakest observed**, not the best
- [ ] Lying about `noexcept`: `-Wterminate`, then `std::terminate` — **the `catch` does not run**
- [ ] Assertion vs exception: *could a correct caller trigger this?*

---

## Section D: The Measurements

**Do not memorise the numbers. Memorise what each demonstrates and what it does not.**

| Measurement | Shows | The trap |
| --- | --- | --- |
| raw `new` leaks on throw, `unique_ptr` does not | RAII is correctness, not tidiness | The `-O2` unconditional-throw case **deleted the allocation** |
| `make_shared` 1 alloc vs 2 | A real saving | It keeps the block alive until the last `weak_ptr` |
| `shared_ptr` copy ≈ 4 ns | Sharing is not free | **Single-threaded only** — the path is chosen at run time |
| cycle: 80 bytes, no destructors | Counting cannot collect cycles | Not a `shared_ptr` bug; a property of refcounting |
| lying iterator: 8.6 → 194.4 ms | A dishonest category is $O(n^2\log n)$ | **It sorted correctly every time** |
| 500k fine, 1M segfault | Recursion depth from input data | Not a leak — **no sanitizer diagnoses it** |
| Decorator $2^n$ vs $n$, 0.58 ns/layer | The trade is one-sided | At n=3 the class count barely improves |
| `std::function` 296 vs lambda 160 ms | Type erasure blocks inlining | **Same lambda**, different container |
| exceptions: free in time, 240 vs 88 bytes | "Zero-cost" is about **time** | A first attempt compared two different APIs |
| basic 2→4, strong 2→2 | The guarantees are testable | The guarantee is the **weakest** across all failure points |

**A good Section D answer states what the number is evidence for and names one thing it is not.**

---

## How to Build the Sheet

One side of A4, handwritten. **Making it is most of the revision.**

Worth the space:

- The **five special members** and when each is suppressed
- The **preference order**: value → `unique_ptr` → reference → `shared_ptr` → `weak_ptr`
- The **five `iterator_traits` typedefs** and the four categories
- The **three guarantees** in one line each, plus the strong recipe
- `sizeof` facts: `unique_ptr` 8, `shared_ptr` 16, first virtual +8, empty class 1
- Where `noexcept` is load-bearing

Not worth it: exact benchmark figures (Section D supplies the table), and anything you can derive.

---

## Practice Strategy

**Now:** work the lecture exercises you skipped. They are the paper's source material.

**One week out:** re-run **one** measurement from each of Labs 5, 6 and 9 without looking at your notes.
If you cannot reproduce it, you cannot explain it.

**Three days out:** write the sheet. Then a timed 75 minutes on Weeks 5–6, which is the half people
forget while revising the patterns.

**The night before:** stop.

---

## Practicalities

- **75 minutes**, written to be finishable in 65.
- **Section C is marked on ideas, not syntax.** A missing semicolon costs nothing; a missing `virtual`
  on a destructor, or a missing `noexcept` on a swap in a strong-guarantee operation, costs plenty.
- **Show working in Section D.** Reasoning with an arithmetic slip earns most of the marks; a bare
  number earns few.
- Any arrangement you need — extra time, a separate room — is set up by emailing the instructor,
  **without giving a reason.** Do it now, not in exam week.

---

*PROG 102 · Week 10 · Midterm 2 Revision Guide · © CSE Department*
