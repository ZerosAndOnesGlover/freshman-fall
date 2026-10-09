# PROG 102 · Lecture 35
## `std::function` and Type Erasure

*“Any problem in computer science can be solved with another level of indirection.”* — David Wheeler, as quoted by Butler Lampson in his Turing Award Lecture (1993)

**Week 11 · Wednesday · 50 minutes**
**Reading:** Meyers Item 34; cppreference `std::function` · **Assumes:** L34, Week 8

**Date:** Wednesday 7 April 2027 · 10:00–10:50 · Week 11

**Coursework:** 📝 **PS 10** due Fri 9 Apr 17:00 · 📝 **PS 11** released Fri 9 Apr 10:00, due Fri 16 Apr 17:00 · 🔬 **Lab 11** Mon 12 Apr 15:00–16:50 · 📕 **Final exam** Thu 22 Apr 14:00–16:30

---

## 1. The Problem

Every lambda has a **unique, unnamable type** (L34 §1.2). So:

```cpp
std::vector<???> handlers;                     // what type?
??? make_handler();                            // what return type?
class Button { ??? on_click; };                // what member type?
```

**`auto` does not help** — it deduces one specific type, and you need to hold *several different*
callables in one place.

```cpp
std::function<void()> f;                       // any callable taking nothing, returning void
std::vector<std::function<void(int)>> handlers;
```

**`std::function` is a box that holds any callable with a given signature.** That is the feature, and
this lecture is about what it costs.

---

## 2. How It Works — Type Erasure

`std::function` cannot know at compile time what it holds. So it stores:

- a **pointer to the callable** (or the callable itself, if small — §4);
- a **pointer to a table of operations** — call it, copy it, destroy it — generated for the concrete
  type at the point of assignment.

**That second pointer is the erasure.** The concrete type is used to build the table and then
forgotten; from then on, calling goes through a pointer.

> **You have seen this shape twice.** It is a **vtable** (Week 4 §L14 §3) built by hand for a type
> that has no inheritance relationship, and it is what `qsort`'s function pointer did (Week 3 §L12 §2).
> **The mechanism is the same and so is the consequence: the call cannot be inlined.**

```
sizeof(std::function<int()>) = 32
```

Four words: enough for a small callable, plus the operation table pointer and bookkeeping.

---

## 3. What a Call Costs

The same lambda, called 100,000,000 times, held three ways:

| | ns per call | vs lambda |
| --- | --- | --- |
| **lambda, called directly** | **0.61–0.67** | 1.0× |
| function pointer | 1.50–1.54 | **~2.4×** |
| **`std::function`** | **2.15–2.21** | **~3.5×** |

**The lambda is inlined** — its type is known, its body is visible, and the call disappears entirely.

**The function pointer cannot be inlined** — an indirect call through an address, which is Week 3's
`qsort` result at the level of a single call.

**`std::function` is worse still** because it adds the erasure indirection on top: a call through the
operation table, to a wrapper, which calls the target.

> **This completes Week 8.** There, `std::function` made `std::sort` 1.85× slower than a lambda. Here
> the per-call ratio is 3.5×. **The sort ratio is smaller because the comparison is only part of
> sorting's work** — which is the right way to read both numbers.

---

## 4. The Hidden Allocation

`std::function` has a **small-buffer optimization**: a small enough callable is stored *inside* the
`std::function` object, and anything larger goes on the heap.

Measured, counting allocations while constructing a `std::function` from a lambda capturing *N* bytes:

| capture size | `sizeof(lambda)` | allocations |
| --- | --- | --- |
| 1 | 1 | **0** |
| 8 | 8 | **0** |
| **16** | 16 | **0** |
| **17** | 17 | **1 — heap** |
| 32 | 32 | **1 — heap** |

**The threshold is 16 bytes** on this implementation.

### 4.1 Why That Number Matters

**Two pointers is 16 bytes.** So:

```cpp
[a, b]              // two pointers or two ints -- fits, no allocation
[a, b, c]           // three pointers -- ALLOCATES
[s]                 // a std::string is 32 bytes -- ALLOCATES
[=]                 // captures everything used -- who knows
```

> **Nothing tells you which side of the line you are on.** Not the type system, not a warning, not the
> API. **A `std::function` assigned in a loop, from a lambda capturing a `std::string`, allocates every
> iteration** — and the code looks identical to the version that does not.
>
> **The threshold is implementation-defined.** 16 bytes here; libc++ and MSVC differ. **Do not design
> around the specific number — design around the fact that a boundary exists**, and measure if it
> matters.

---

## 5. When to Use It Anyway

The cost is real and `std::function` is still often correct.

**Use it when you must store callables of *different* types together:**

```cpp
std::vector<std::function<void(const Event&)>> subscribers;    // Week 8's event bus
```

A template parameter cannot express this — each lambda has its own type, and a `vector` needs one.

**Use it when the callable crosses a boundary** the template cannot: a member of a non-template class,
a virtual function's parameter, a separately-compiled library's callback registration.

**Do not use it:**

- **as a parameter type for a function you could template.** `template <class F> void apply(F f)`
  costs nothing; `void apply(std::function<...> f)` costs an erasure and possibly an allocation, on
  every call.
- **in a hot loop**, where §3's 3.5× is being paid per element.
- **as "the modern way to pass a function".** It is not; it is the way to *store* one.

### 5.1 The Rule

> **Template parameter to pass. `std::function` to store.**

That single line covers almost every case, and it is what the standard library itself does —
`std::sort` takes a template parameter; `std::function` exists for the cases `std::sort` does not have.

---

## 6. The Alternatives

| Tool | Holds | Cost | Use |
| --- | --- | --- | --- |
| **template parameter** | one known type | **none** | passing a callable |
| **function pointer** | a free function | one indirect call | C APIs |
| **`std::function`** | any matching callable | erasure + possible allocation | **storing** heterogeneous callables |
| **virtual interface** | a class with state and several methods | one indirect call | a policy object (Week 8 §L26 §3.2) |

**C++20 adds `std::function_ref`-like proposals and `std::move_only_function`**, which address the
copyability requirement that forces `std::function` to be heavier than a non-owning reference needs to
be. Not available to you here; worth knowing the direction.

---

## 7. Summary

| Idea | The point |
| --- | --- |
| The problem | Every lambda has a unique type; you cannot name it in a container |
| Type erasure | A hand-built vtable for unrelated types |
| Same shape as | A virtual call (W4), and `qsort`'s function pointer (W3) |
| `sizeof(std::function<int()>)` | **32** |
| Call cost | lambda **0.61–0.67**, fn ptr **1.50–1.54**, `std::function` **2.15–2.21** ns |
| Ratio | **~3.5×**, and Week 8's 1.85× inside `sort` is the same effect diluted |
| **SBO threshold: 16 bytes** | 17 bytes heap-allocates. Nothing warns you |
| Two pointers fit; three do not | And a `std::string` capture is 32 bytes |
| The threshold is implementation-defined | Design around the boundary existing, not its value |
| **The rule** | **Template parameter to pass; `std::function` to store** |

---

## 8. Exercises

**1.** Reproduce §3: the same lambda called directly, through a function pointer, and through
`std::function`, at least 10⁸ calls, three runs. **Report ns per call for all three.**

**Make sure your loop is not optimized away** — if a version reports 0.00 ns, the compiler deleted it,
and you must make the arguments unhoistable.

**2.** Find your implementation's SBO threshold by instrumenting `operator new` and sweeping the
capture size. **Report the exact byte count at which it starts allocating.**

**3.** Write a lambda capturing a `std::string`. **Predict whether assigning it to a `std::function`
allocates**, then measure. Now capture the string by reference instead and measure again.

**4.** Write a `std::vector<std::function<void()>>` holding five lambdas with different captures.
**Count the total allocations.** Then explain how you would reduce it.

**5.** Take a function `void apply(std::function<int(int)> f)` and rewrite it as
`template <class F> void apply(F f)`. **Measure both** over 10⁷ calls and report the difference.

**6.** Explain, in three sentences, why Week 8's `std::function` was 1.85× the lambda inside
`std::sort` while this lecture measures 3.5× per call. **Both numbers are correct.**

**7.** Give a concrete situation where `std::function` is the only reasonable choice, and one where
using it would be a clear mistake. Be specific.

---

## 9. Next

**Lecture 36** covers the rest of modern C++: `constexpr`, which moves computation to compile time;
`if constexpr`, which chooses a branch at compile time; structured bindings; and a preview of C++20's
ranges — the feature that will change how everything in Week 3 is written.

---

*PROG 102 · Week 11 · Lecture 35 · © CSE Department*
