# PROG 102 · Lecture 06
## The Copy-Swap Idiom, and Counting Copies

*“One man's constant is another man's variable.”* — Alan Perlis, "Epigrams on Programming" (1982), #1

**Week 1 · Thursday · 50 minutes**
**Reading:** *C++ Primer* §13.3 · **Reference:** Meyers, *Effective C++* Item 11
**Assumes:** L05 (Rule of Three, self-assignment)

**Date:** Thursday 28 January 2027 · 10:00–10:50 · Week 1

**Coursework:** 📝 **PS 0** due Fri 29 Jan 17:00 · 📝 **PS 1** released Fri 29 Jan 10:00, due Fri 5 Feb 17:00 · 🔬 **Lab 1** Mon 1 Feb 15:00–16:50 · 📊 **Quiz 2** Tue 2 Feb 10:00–10:15

---

## 1. Where We Left Off

Lecture 05's copy assignment operator is correct and has two flaws:

```cpp
CharBuffer& operator=(const CharBuffer& o) {
    if (this == &o) return *this;       // a check the common path pays for
    delete[] data;                      // released BEFORE the risky part
    size = o.size;
    data = new char[size];              // if this throws, the object is destroyed
    std::memcpy(data, o.data, size);
    return *this;
}
```

The second flaw is the serious one, and this is what it costs. To force an allocation to fail, the
test program replaces the global `operator new[]` — the function every `new T[n]` calls — with one
that throws when a flag is set. This is the harness; copy it as it is (Problem Set 1 does):

```cpp
#include <cstdlib>
#include <new>

static bool fail_next_new = false;           // set to true: the next new[] throws
void* operator new[](std::size_t n) {
    if (fail_next_new) { fail_next_new = false; throw std::bad_alloc(); }
    if (void* p = std::malloc(n ? n : 1)) return p;
    throw std::bad_alloc();
}
void operator delete[](void* p) noexcept { std::free(p); }
void operator delete[](void* p, std::size_t) noexcept { std::free(p); }
```

Then `fail_next_new = true; try { a = b; } catch (const std::bad_alloc&) { … }` (Lecture 04 §4.2).
Forcing the allocation to fail:

```
FourStep before: a="hello"
  bad_alloc caught
ERROR: AddressSanitizer: heap-use-after-free on address 0x502000000010
```

**After a failed assignment, `a` is not merely wrong — it is destroyed.** Its buffer is freed and its
`data` pointer dangles. Reading it is a use-after-free, and when `a` eventually goes out of scope its
destructor will `delete[]` the same block a second time.

The assignment *threw*, which is fine and expected. What is not fine is that it took the target down
with it.

---

## 2. The Idiom

```cpp
class CharBuffer {
    int   size;
    char* data;
public:
    // ... constructor, copy constructor, destructor as before ...

    void swap(CharBuffer& o) noexcept {
        std::swap(size, o.size);
        std::swap(data, o.data);
    }

    CharBuffer& operator=(CharBuffer o) {   // NOTE: by value
        swap(o);
        return *this;
    }
};
```

Three lines, and both flaws are gone.

### 2.1 How It Works

The parameter is taken **by value**, so the copy happens *before* the function body runs — performed by
the copy constructor you already wrote:

1. `o` is constructed as a copy of the right-hand side. **If this throws, the body never runs and
   `*this` has not been touched.**
2. `swap` exchanges the guts of `*this` and `o`. This is three pointer/integer swaps — **it cannot
   throw.**
3. `o` goes out of scope at the closing brace, and its destructor releases **the old buffer**, which it
   now holds.

The destructor that cleans up your previous state is one you already wrote and did not have to think
about. That is L02's destruction order doing the work.

### 2.2 Self-Assignment Is Free

```cpp
a = a;
```

The parameter is a *copy* of `a`. The body swaps `*this` with that copy — harmless — and destroys the
copy. There is no aliasing, so **no guard is needed**:

```
Naive    -> AddressSanitizer: heap-buffer-overflow
Guarded  -> "hello"
CopySwap -> "hello"
```

Correct with no `if (this == &o)` anywhere in the class.

### 2.3 Exception Safety Is Free

The same forced-failure test, on the copy-swap version:

```
CopySwap before: a="hello"
  bad_alloc caught
CopySwap after : a="hello"
```

**The exception propagated and `a` is untouched.** This is the **strong exception guarantee**:
the operation either succeeds completely, or has no effect. Week 9 names the three guarantees and
explains why this one is the target for data structure operations.

You get it here because of *ordering*: everything that can fail happens before anything is modified.
That is the whole trick, and it generalises far beyond assignment.

---

## 3. Writing `swap` Correctly

```cpp
void swap(CharBuffer& o) noexcept {
    std::swap(size, o.size);
    std::swap(data, o.data);
}
```

- **Swap members, never whole objects.** `std::swap(*this, o)` calls `operator=`, which calls `swap`,
  forever.
- **Mark it `noexcept`.** Swapping built-ins and pointers cannot throw, and the guarantee in §2.3
  depends on that. Week 9 explains why `noexcept` on `swap` is load-bearing rather than decorative.
- **Swap every member.** A forgotten member is a corruption bug that appears only after an assignment,
  which is a miserable thing to track down.

---

## 4. What It Costs

Copy-swap is not free, and the honest comparison matters.

**1,000 assignments between two objects of the same size**, counting heap allocations:

| Assignment operator | allocations | frees |
| --- | --- | --- |
| Four-step with guard | **1000** | 1000 |
| Buffer-reusing | **0** | 0 |
| **Copy-swap** | **1000** | 1000 |

*(Identical at `-O0` and `-O2`, so this is not an optimizer artefact.)*

The buffer-reusing version notices the existing allocation is big enough and just copies into it:

```cpp
if (o.n <= cap) { n = o.n; std::memcpy(d, o.d, n); return *this; }
```

**Zero allocations.** For a container assigned repeatedly in a loop, that is a real and sometimes large
win — and it is why `std::vector::operator=` does exactly this rather than copy-swap.

> **So which do you write?**
>
> **Copy-swap, unless you have measured that assignment is hot.** It is three lines, it cannot get
> self-assignment wrong, it gives the strong guarantee for free, and it reuses the copy constructor so
> there is only one place where copying is implemented.
>
> The reusing version is longer, needs its own self-assignment guard, needs a separate capacity member,
> and gives only the **basic** guarantee — if the reallocation path throws, the object is damaged.
>
> **Buy the allocation back only when a profiler tells you to.** This is the course's thesis in its
> smallest form: name the cost, measure it, then decide.

---

## 5. Counting Copies

Lab 1 asks you to count copies. Here is the instrument: a class that counts every special member call.

```cpp
struct V3 {
    double x, y, z;
    V3(double a=0,double b=0,double c=0):x(a),y(b),z(c){ ++C.ctor; }
    V3(const V3& o):x(o.x),y(o.y),z(o.z){ ++C.copy; }
    V3& operator=(const V3& o){ x=o.x;y=o.y;z=o.z; ++C.assign; return *this; }
    ~V3(){ ++C.dtor; }
};
V3 operator+(const V3& a, const V3& b){ return V3(a.x+b.x, a.y+b.y, a.z+b.z); }
```

Measured, `-std=c++17 -O2`:

| Expression | ctor | copy | assign | dtor |
| --- | --- | --- | --- | --- |
| `V3 a(1,2,3), b(4,5,6);` | 2 | 0 | 0 | 0 |
| `V3 c = a + b;` | 1 | **0** | 0 | 0 |
| `c = a + b;` *(c already exists)* | 1 | 0 | 1 | 1 |
| `dot(V3 a, V3 b)` — **by value** | 0 | **2** | 0 | 2 |
| `dot(const V3& a, const V3& b)` | 0 | **0** | 0 | 0 |
| `V3 s = a + b + c;` | 2 | **0** | 0 | 1 |

Two results deserve attention.

### 5.1 Pass by `const&`, Measured

Passing two `V3`s by value costs **two copy constructions and two destructions** per call. By `const&`
it costs **nothing**.

That is the entire justification for L00 §5.3's rule, and now it is a number rather than an assertion.
For `V3` a copy is 24 bytes and cheap; for a `std::string` or a container it is a heap allocation, per
call, in every loop.

### 5.2 `V3 c = a + b;` Performs Zero Copies

`operator+` returns by value. There is a temporary. Yet **copy is 0**.

This is not the optimizer being clever.

---

## 6. Guaranteed Copy Elision

Here is `V3 c = a + b;` across five compiler configurations:

| Configuration | copies |
| --- | --- |
| `-std=c++11 -O0` | 0 |
| `-std=c++11 -O0 -fno-elide-constructors` | **2** |
| `-std=c++17 -O0` | 0 |
| `-std=c++17 -O0 -fno-elide-constructors` | **0** |
| `-std=c++17 -O2` | 0 |

Read row 2 against row 4. `-fno-elide-constructors` is a flag whose sole purpose is to disable copy
elision. **In C++11 it produces two copies. In C++17 it changes nothing.**

The reason is a change in what the standard *says*, not in what the compiler *does*:

- **Before C++17**, `a + b` created a temporary object, and `c` was copy-constructed from it. The
  compiler was *permitted* to skip that copy. The copy constructor still had to exist and be
  accessible, and a compiler was free not to elide.
- **From C++17**, `a + b` is a **prvalue** — not an object, but a *recipe for initialising one*. When
  you write `V3 c = a + b;`, that recipe initialises `c` directly. **There is no temporary and no copy
  to elide.**

> **This is why the flag has no effect.** You cannot disable an optimization that is not an
> optimization. C++17 made it a rule about the meaning of the language.

**The practical consequence:** returning a large object by value is not the performance mistake C
programmers expect it to be. This is correct and costs nothing:

```cpp
Matrix multiply(const Matrix& a, const Matrix& b) {
    Matrix result(a.rows(), b.cols());
    // ...
    return result;
}
```

### 6.1 Named Returns Are a Different Case

Returning a **named** local is *not* covered by the guarantee. It is a separate, older optimization
called **NRVO** (named return value optimization), which is permitted but not required:

```cpp
V3 named()   { V3 local(1,2,3); return local; }   // NRVO: permitted
V3 prvalue() { return V3(1,2,3); }                // guaranteed elision
```

Measured:

| Configuration | `named()` | `prvalue()` |
| --- | --- | --- |
| `-std=c++17 -O0` | 0 copies | 0 copies |
| `-std=c++17 -O2` | 0 copies | 0 copies |
| `-std=c++17 -O0 -fno-elide-constructors` | **1 copy** | **0 copies** |

**The last row is the whole distinction in one line.** The flag disables NRVO, because NRVO is an
optimization the compiler may decline. It does not touch the prvalue case, because there is no
optimization there to disable.

In practice every compiler performs NRVO at `-O2`, so returning a named local is fine. But it is a
*quality-of-implementation* promise rather than a guarantee, and Week 5's move semantics is the
backstop for when it does not apply.

Row 6 of §5's table shows the same thing compounding: `a + b + c` creates two intermediate results and
copies **none** of them.

---

## 7. Where This Is Going

The Rule of Three is the C++98 answer. C++11 added two more special members:

```cpp
CharBuffer(CharBuffer&& o) noexcept;              // move constructor
CharBuffer& operator=(CharBuffer&& o) noexcept;   // move assignment
```

making it the **Rule of Five**. A move *steals* the buffer from a temporary instead of copying it —
because a temporary is about to be destroyed and will not miss it.

There is also the **Rule of Zero**, which is the one to aim for: if your class holds `std::string`,
`std::vector` and `std::unique_ptr` members rather than raw pointers, **it needs none of the five**.
The members handle their own copying and destruction, and the compiler-generated versions are correct.

Both arrive in **Week 5**. The reason for meeting the Rule of Three first is that you cannot understand
why `unique_ptr` is designed the way it is until you have written the code it replaces.

> **A note on copy-swap and moves.** Once moves exist, `operator=(CharBuffer o)` taking by value
> handles *both* copy and move assignment in one function — the parameter is copy-constructed from an
> lvalue and move-constructed from an rvalue. This is a genuine advantage of the idiom and one reason
> it survived into modern C++.

---

## 8. Summary

| Idea | The point |
| --- | --- |
| Copy-swap | Take by value, swap, return. Three lines |
| Self-assignment | Safe with no guard — the parameter is already a copy |
| Strong exception guarantee | Verified: after a thrown `bad_alloc`, `a` is still `"hello"` |
| The four-step version | Verified: after the same failure, `a` is **use-after-free** |
| `swap` must be `noexcept` | The guarantee depends on it |
| The cost | 1000 assignments = 1000 allocations; a reusing version does 0 |
| Which to write | Copy-swap, until a profiler says otherwise |
| Pass by `const&` | 2 copies per call becomes 0 — measured |
| `V3 c = a + b;` | **Zero** copies |
| Guaranteed copy elision | `-fno-elide-constructors` gives 2 copies in C++11 and 0 in C++17 |
| Rule of Five / Rule of Zero | Week 5 |

---

## 9. Exercises

**1.** Add copy-swap to your Week 0 `CharBuffer`. Verify `a = a` works and that the class contains no
`this == &o` comparison.

**2.** Reproduce §2.3: replace `operator new[]` so it throws on demand, and show that your copy-swap
version leaves the target unchanged. Then swap in the four-step operator and show that it does not.
**Paste both transcripts.**

**3.** Build the counting harness from §5 and reproduce the six-row table. Then predict, *before
running*, the counts for:

```cpp
V3 f() { V3 local(1,2,3); return local; }     // a named local
V3 d = f();
```

**Were you right? Which of §6's two cases is this?**

**4.** Run `V3 c = a + b;` under all five configurations in §6 and reproduce the table. **Explain in
two sentences why row 4 differs from row 2.**

**5.** Implement the buffer-reusing `operator=` and reproduce the allocation counts in §4. Then force
its reallocation path to throw and show that the object is damaged. **Which exception guarantee does it
offer?**

**6.** `swap` is marked `noexcept`. Remove it and explain what could go wrong — you may need Week 9 to
answer this fully, so give your best attempt now and revisit it then.

**7.** A class has a `std::vector<int>` member and nothing else. **How many of the five special members
should you write?** Justify from §7.

---

## 10. Next

**Week 2** is templates: how to write `CharBuffer` once and get `Buffer<int>`, `Buffer<double>` and
`Buffer<std::string>` from it. The Rule of Three does not change; it just has to be written generically.

Then **Week 3** shows you that the standard library already did all of this, and `std::vector` is what
you have been building badly for three weeks — which is the right moment to meet it, because you will
know exactly what it is doing for you.

---

*PROG 102 · Week 1 · Lecture 06 · © CSE Department*
