# PROG 102 · Problem Set 5 — Solutions and Marking Notes
## From Raw Pointers to Smart Pointers

**INSTRUCTOR COPY — not for distribution**

---

## Before Marking

**Reference environment:** g++ 13.3.0, x86-64 Linux. `sizeof` values, allocation counts and warning
counts are exact. Timings are not.

**This set follows Midterm 1.** Expect a bimodal distribution: students who started it after the exam
and students who did not start it at all. Mark generously on Part A, strictly on **C2** and **D4(b)**,
which are the two places a wrong model shows up as a confident wrong answer.

---

## Part A — Rewrite Week 4's Hierarchy (26)

### A1 (8)

`std::vector<std::unique_ptr<Shape>>`, `make_unique` throughout, virtual destructor retained. Output
identical to PS 4 A4 (total area 21.1416), sanitizer-clean.

*Marking: 4 correct rewrite, 2 no `new`/`delete` anywhere, 2 sanitizer-clean transcript.*

### A2 (6)

Removing `virtual`:

```
ERROR: AddressSanitizer: new-delete-type-mismatch
```

**No, `unique_ptr` does not protect you.** It guarantees the `delete` happens; it does not change
*which* destructor that `delete` finds. The rule from L15 §2 is untouched.

*Marking: 3 the transcript, 3 the answer. **Full marks require saying that `unique_ptr` fixes "the
delete happens" and not "the right destructor runs".***

**Worth a note in feedback:** `-Wall -Wextra` gives **zero warnings** here, where a raw `delete`
through a polymorphic base would have warned. A student who noticed that unprompted has read L16 §8
properly and should be commended.

### A3 (6)

| Signature | Promises |
| --- | --- |
| `double total_area(const std::vector<std::unique_ptr<Shape>>&)` | reads the collection, takes nothing |
| `void describe(const Shape&)` | borrows one shape, never null, no ownership |
| `std::unique_ptr<Shape> make_circle(double)` | **gives you ownership**; you must handle it |
| `void absorb(std::unique_ptr<Shape>)` | **takes ownership**; the caller's pointer is null after |

*Marking: 1.5 each. The words "takes" / "gives" / "borrows" are what is being assessed.*

### A4 (6)

```
error: could not convert 'sq' from 'Square' to 'std::unique_ptr<Shape>'
error: could not convert 'sp' from 'std::shared_ptr<Shape>' to 'std::unique_ptr<Shape>'
```

Fix: `void bad(const Shape& s)`.

**The rule: pass ownership by value; pass everything else by reference to the pointee.** A
`const unique_ptr<T>&` parameter demands a specific ownership *representation* while taking no
ownership — it buys nothing and excludes most callers.

*Marking: 3 both errors, 3 the rule. "Because it's more general" is 1 of the 3 — the answer must note
that it takes no ownership anyway.*

---

## Part B — What It Costs (26)

### B1 (6)

```
int*            8
unique_ptr<int> 8
shared_ptr<int> 16
weak_ptr<int>   16
```

Both are 16 because they carry **two** pointers: one to the object, one to the control block. With a
**stateful** deleter, `unique_ptr` grows to hold the deleter.

*Marking: 3 the four values, 2 the control-block explanation, 1 the stateful-deleter result.*

### B2 (8)

`raw(Widget*)` and `uniq(Widget&)` — **byte-identical**.
`bad(const std::unique_ptr<Widget>&)` — one extra `mov rdi, QWORD PTR [rdi]`: an extra load, because
the parameter is a pointer *to* the smart pointer.

*Marking: 4 the identical pair, 4 the extra instruction identified. **A student who reports "identical"
for all three has not compared the third.***

### B3 (6)

| | allocations |
| --- | --- |
| `shared_ptr<W>(new W)` | **2** |
| `make_shared<W>()` | **1** |
| `make_unique<W>()` | **1** |

`make_shared` allocates one block holding the control block and the object together.

*Marking: 3 the counts, 3 the explanation.*

### B4 (6)

| | per operation |
| --- | --- |
| raw pointer | 0.90–1.13 ns |
| `shared_ptr` by reference | 3.19–3.62 ns |
| `shared_ptr` copied | 7.18–8.76 ns |

**The refcount is the copy overhead — about 4 ns** (the difference between rows 2 and 3). The gap
between rows 1 and 2 — roughly 2.4 ns — is **not** the refcount; it is the extra indirection and worse
locality of a 16-byte handle.

*Marking: 3 the three figures, 3 the separation. **The separation is the assessed idea.** A student who
attributes the whole 8 ns to the reference count gets 1 of the 3 — the by-reference row is in their own
table and refutes it.*

---

## Part C — Exception Safety and the Benchmark Trap (18)

### C1 (8)

| | `-O0` | `-O2` |
| --- | --- | --- |
| raw `new`/`delete` | allocs=2 frees=1 **LEAKED** | allocs=2 frees=1 **LEAKED** |
| `make_unique` | balanced | balanced |

*Marking: 8, four per optimization level. **A student reporting the raw version as balanced at `-O2`
has almost certainly written an unconditional throw** — that is C2, and they should be given the marks
for C2 if they explain it.*

### C2 (6) — the assessed question

With an unconditional throw at `-O2`, the raw version reports **balanced**.

**GCC inlined the throwing function, saw that the throw dominated the `delete`, and eliminated the
allocation entirely** — allocation elision is permitted. The benchmark was measuring a program that no
longer allocated anything.

*Marking: 6. **The answer must say the allocation was removed, not that the leak was fixed.** "The
optimizer fixed the bug" scores 0 and is worth correcting directly — it is precisely the wrong
conclusion.*

### C3 (4)

Expected substance:

> **Size:** yes — 8 bytes, identical to a raw pointer.
> **Borrowing:** yes — passing `Widget&` generates byte-identical code to `Widget*`.
> **Owning:** no, not identical — the `unique_ptr` version carries exception-handling landing pads.
> But that is not overhead; it is the release the raw version *fails to perform* when an exception is
> thrown. It is cheaper than free, because the code it replaces was wrong.

*Marking: 4, roughly 1 per distinction plus 1 for the conclusion. An answer of "yes, zero-overhead"
with no qualification gets 1.*

---

## Part D — Cycles and Moves (30)

### D1 (8)

```
use_count a=2 b=2
-- leaving scope --
SUMMARY: AddressSanitizer: 80 byte(s) leaked in 2 allocation(s).
```

**No destructors ran.** With `weak_ptr`: `use_count a=1 b=2`, both destructors run, no leak.

**Reference counting cannot collect cycles**: every object in a cycle is referenced by another member
of the cycle, so no count ever reaches zero, even when the whole group is unreachable from the program.

*Marking: 5 both demonstrations, 3 the explanation. Must say **unreachable but still counted**.*

### D2 (6)

```
before: expired=1 use_count=0
alive : expired=0 use_count=1
lock() -> ok,  use_count now 2
after : expired=1 use_count=0
lock() -> nullptr
```

**`lock()` checks and acquires as one operation.** `expired()` followed by access is a race: the object
can be destroyed between the two calls, and `expired()` returning false is a statement about the past.

*Marking: 4 the lifecycle, 2 the race. Accept a single-threaded framing if they identify the
check-then-use gap.*

### D3 (8)

1 MB buffers, 2,000 operations:

| | per operation |
| --- | --- |
| copy | 941–1036 µs |
| move | 0.055–0.156 µs |

At 16 bytes the ratio collapses toward 1 — a move is a constant few nanoseconds and a copy of 16 bytes
is also a few nanoseconds. **The move's advantage is proportional to the data.**

*Marking: 4 the 1 MB figures **in absolute terms**, 4 the small-buffer comparison and explanation. A
ratio-only answer gets half — the sheet asks for per-operation times explicitly.*

### D4 (8)

**(a) (3)** `a` prints empty, `size()` 0 — **valid but unspecified**. Legal: destroy it, assign to it,
call `size()`. Undefined: `a[0]`, or any operation assuming contents.

**(b) (3)** `return b;` → **zero** moves and zero copies (NRVO constructs in place). `return
std::move(b);` → **one move**, because the `std::move` makes it an rvalue and **disables NRVO**.
`return b;` is correct.

**(c) (2)** Without `noexcept`, `vector` growth **copies**; with it, it moves.

*Marking: 3 + 3 + 2. **(b) is the one to mark strictly** — a student reporting `std::move` as faster or
equal has not counted. The expected counts are 0 and 1.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 26 |
| B | 26 |
| C | 18 |
| D | 30 |
| **Total** | **100** |

---

## What to Watch For

1. **"The optimizer fixed the leak"** (C2). The most important correction in the set.
2. **Attributing the whole `shared_ptr` gap to the refcount** (B4), refuted by their own middle row.
3. **`return std::move(b);` reported as better** (D4b).
4. **Ratio-only answers** to D3.
5. **Not comparing the third signature** in B2.

---

## Feeding Into Week 6

Week 6 builds a templated list and BST with `unique_ptr` nodes, and **assigns Project 1**.

The framing for Monday: this week ended on the **Rule of Zero** — write none of the five, let the
library types do it. **Week 6 is the exception.** A container is exactly the case where you *are* the
resource wrapper, and where the five must be written by hand.

Students who took "Rule of Zero" as an absolute will try to build a linked list out of `std::vector`
and be confused. Say explicitly on Monday: *the Rule of Zero applies to code that uses resources; Week
6 is code that provides them.*

---

*PROG 102 · Week 5 · PS 5 Solutions · © CSE Department*
