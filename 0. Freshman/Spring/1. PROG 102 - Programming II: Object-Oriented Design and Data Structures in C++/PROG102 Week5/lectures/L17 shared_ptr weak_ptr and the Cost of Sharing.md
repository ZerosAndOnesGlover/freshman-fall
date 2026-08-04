# PROG 102 · Lecture 17
## `shared_ptr`, `weak_ptr`, and the Cost of Sharing

**Week 5 · Wednesday · 50 minutes**
**Reading:** *C++ Primer* §12.1.1, §12.1.4–12.1.6 · **Reference:** Meyers Items 19–21
**Assumes:** L16

---

## 1. When One Owner Is Not Enough

`unique_ptr` covers most cases. It cannot cover this one:

> Several parts of the program need the object, they finish with it at unpredictable times, and it
> should be destroyed when the **last** of them is done.

A cache handing out entries. Nodes in a graph reachable by several paths. An observer registry. There
is no single owner to attach the lifetime to.

**`std::shared_ptr` counts owners and destroys the object when the count reaches zero.**

```cpp
auto a = std::make_shared<Widget>(1, 2);
auto b = a;                          // both own it; use_count() == 2
```

---

## 2. The Control Block

A `shared_ptr` is **two** pointers:

```
sizeof(std::shared_ptr<int>) = 16      (a raw pointer is 8)
sizeof(std::weak_ptr<int>)   = 16
```

One points at the object. The other points at a **control block** holding:

- the **strong count** — how many `shared_ptr`s;
- the **weak count** — how many `weak_ptr`s;
- the deleter and allocator.

The object is destroyed when the strong count hits 0. **The control block itself survives until the
weak count also hits 0**, because the `weak_ptr`s still need somewhere to look to discover the object
is gone.

---

## 3. `make_shared` Halves the Allocations

```cpp
auto p = std::shared_ptr<W>(new W{1});     // object, then control block
auto q = std::make_shared<W>(W{1});        // one block holding both
```

Measured with an instrumented `operator new`:

| Expression | allocations |
| --- | --- |
| `std::shared_ptr<W>(new W)` | **2** |
| `std::make_shared<W>()` | **1** |
| `std::make_unique<W>()` | **1** |

`make_shared` allocates one block big enough for the control block *and* the object. Half the
allocations, and the two end up adjacent in memory, which helps the cache.

> **The one case to avoid `make_shared`:** it keeps the whole block alive until the last `weak_ptr`
> dies, because the object's storage is inside the control block's allocation. For a large object with
> long-lived `weak_ptr`s watching it, `shared_ptr<W>(new W)` releases the object's memory sooner.
>
> That is a genuine trade-off and a rare one. **Default to `make_shared`.**

---

## 4. What Copying Costs

Copying a `shared_ptr` increments the count; destroying one decrements it. Measured over 5,000,000
distinct objects, three runs:

| | per operation |
| --- | --- |
| raw pointer | 0.90–1.13 ns |
| `shared_ptr` by **reference** | 3.19–3.62 ns |
| `shared_ptr` **by value** (a copy) | 7.18–8.76 ns |
| **the copy itself** | **≈3.9–5.1 ns** |

Two separate costs are visible, and it is worth separating them.

**The copy costs about 4 ns** — the increment, the later decrement, and the fact that the compiler
cannot hoist the operation out of a loop because it has side effects.

**Even without copying, `shared_ptr` is ~3.5× a raw pointer** (3.3 ns against 0.9 ns) in this loop.
That is not the refcount; it is the extra indirection and the worse locality of a 16-byte handle.

### 4.1 Is the Count Atomic?

The count must be thread-safe, so the increment should be a `lock`-prefixed instruction. Looking at the
assembly, libstdc++ emits **both**:

```asm
.L17:
        lock add   DWORD PTR 8[rdi], 1        ; atomic path
...
        add        DWORD PTR 8[rdi], 1        ; plain path
```

and chooses between them **at run time**, by checking whether the program has actually started any
threads. Compiling with `-pthread` does not change the generated code — the decision is not made at
compile time.

Measured, copy overhead with and without `-pthread`: **4.17 ns and 4.01 ns** — indistinguishable,
because neither program started a thread and both took the cheap path.

> **So the number above is the *single-threaded* cost.** In a genuinely multithreaded program the
> atomic path is taken and it is more expensive — and worse, a hot refcount becomes a contended cache
> line between cores. **Week 10 is where this stops being a footnote.**
>
> This is also a good example of a measurement that is correct and narrower than it looks. "A
> `shared_ptr` copy costs 4 ns" is true of the program I ran, and I did not run the one where it
> matters.

---

## 5. The Cycle

Reference counting has one failure mode, and it is not subtle once you see it.

```cpp
struct Node { std::shared_ptr<Node> other; int id; ~Node(); };

auto a = std::make_shared<Node>();
auto b = std::make_shared<Node>();
a->other = b;
b->other = a;          // cycle
```

Measured on leaving the scope:

```
  use_count a=2 b=2
  -- leaving scope --
SUMMARY: AddressSanitizer: 80 byte(s) leaked in 2 allocation(s).
```

**No destructor ran at all.** When `a` and `b` go out of scope each count drops from 2 to 1 — and each
object is still held by the other. Nothing reaches zero, nothing is destroyed, and the objects are
unreachable from the program.

**That is a leak in a garbage-free language, produced entirely by "safe" pointers.** Reference counting
cannot collect cycles; this is its known and permanent limitation, and it is why languages with real
garbage collectors use tracing rather than counting.

---

## 6. `weak_ptr`

A `weak_ptr` **observes without owning**. It does not affect the strong count.

```cpp
struct Node {
    std::shared_ptr<Node> next;    // owns
    std::weak_ptr<Node>   back;    // observes
};
a->next = b;
b->back = a;                       // no longer a cycle
```

```
  use_count a=1 b=2
  -- leaving scope --
  ~NodeW(1)
  ~NodeW(2)
```

**Both destroyed, no leak.** `a`'s count is 1 because `b->back` does not count.

### 6.1 Using One

You cannot dereference a `weak_ptr` — the object may already be gone. You must `lock()` it, which
returns a `shared_ptr` that is null if the object has expired:

```cpp
if (auto locked = obs.lock()) {
    locked->use();        // guaranteed alive inside this block
}
```

Measured through an object's lifetime:

```
before: expired=1 use_count=0
alive : expired=0 use_count=1
lock()  -> ok, v=42, use_count now 2       <- lock() temporarily adds an owner
-- leaving scope --
after : expired=1 use_count=0
lock()  -> nullptr (object is gone)
```

**`lock()` is the only safe way**, and the reason is the two-line gap between checking and using:
`if (!obs.expired()) obs.lock()->use();` is a race in threaded code, because the object can die between
the two calls. `lock()` does the check and the acquisition as one operation.

### 6.2 Where to Put the `weak_ptr`

**In a parent/child tree: parent owns children with `shared_ptr`, children point back with
`weak_ptr`.** The rule generalises: *the direction that represents ownership gets the `shared_ptr`;
the back-reference gets the `weak_ptr`.*

If you cannot say which direction owns, that is a design problem the pointers cannot fix.

---

## 7. Choosing

In order of preference:

1. **A value member or a stack object.** No pointer at all. Most objects do not need one.
2. **`unique_ptr`** — one owner. **This should be the overwhelming majority of your heap objects.**
3. **A reference or raw pointer** — borrowing, no ownership. Fine as a *parameter* or a short-lived
   local; never store one whose lifetime you cannot reason about.
4. **`shared_ptr`** — genuinely several owners with no single lifetime.
5. **`weak_ptr`** — a back-reference or an observer, to break a cycle.

> **`shared_ptr` is not the safe default.** It is heavier, it can leak through cycles, its thread-safe
> count costs more in the case you care about, and — worst — **it makes lifetime unanalysable.** With
> `unique_ptr` you can point at the owner. With `shared_ptr` everywhere, the answer to "when is this
> destroyed?" is "when the last of an unknown number of holders lets go", which is a question you
> cannot answer by reading the code.
>
> **Reach for `shared_ptr` when you can name the several owners.** If you are reaching for it because
> you are not sure who owns the object, the pointer is not the problem.

---

## 8. Summary

| Idea | The point |
| --- | --- |
| `shared_ptr` | Reference-counted shared ownership; **16 bytes** |
| The control block | Strong count, weak count, deleter |
| `make_shared` | **1 allocation** instead of 2 |
| Copy cost | ≈**4 ns**; and `shared_ptr` is ~3.5× a raw pointer even without copying |
| The count is atomic — **conditionally** | Both paths emitted, chosen at run time by whether threads exist |
| The measured cost is single-threaded | Week 10 is where the atomic path bites |
| **Cycles leak** | 80 bytes, 2 allocations, **no destructors ran** |
| `weak_ptr` | Observes without owning; breaks the cycle |
| `lock()` | The only safe access; `expired()` then use is a race |
| Preference order | value → `unique_ptr` → reference → `shared_ptr` → `weak_ptr` |

---

## 9. Exercises

**1.** Report `sizeof` for `unique_ptr`, `shared_ptr` and `weak_ptr`. **Explain why two of them are
16.**

**2.** Instrument `operator new` and count allocations for `shared_ptr<W>(new W)`, `make_shared<W>()`
and `make_unique<W>()`. Report all three.

**3.** Reproduce §4's table. Report the raw, by-reference and by-value figures. **Which part of the gap
is the refcount, and which part is not?**

**4.** Find the `lock`-prefixed instruction in your compiler's `shared_ptr` copy. Then compile with and
without `-pthread` and compare the assembly. **Report whether it changed, and say what that implies
about when the atomic is used.**

**5.** Build the two-node cycle. Report `use_count()` for both, whether the destructors run, and the
sanitizer's leak figure. Then fix it with `weak_ptr` and show the destructors running.

**6.** Write a tree where each node holds `shared_ptr` children and a `weak_ptr` parent. Add a method
`depth()` that walks to the root via the parent link. **What must it do at each step?**

**7.** A colleague proposes using `shared_ptr` for every heap object "so we never have to think about
lifetimes". Give three specific objections, at least one of which is not about performance.

---

## 10. Next

**Lecture 18** explains the thing `unique_ptr` needed and this lecture kept using: **move semantics.**
You cannot copy a `unique_ptr`, and yet `return std::make_unique<W>()` works and
`v.push_back(std::move(p))` works. That is because ownership can be *transferred*, and C++11 added the
machinery to say so.

---

*PROG 102 · Week 5 · Lecture 17 · © CSE Department*
