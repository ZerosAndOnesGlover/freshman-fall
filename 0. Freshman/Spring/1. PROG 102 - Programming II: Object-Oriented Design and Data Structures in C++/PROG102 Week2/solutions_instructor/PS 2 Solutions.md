# PROG 102 · Problem Set 2 — Solutions and Marking Notes
## A Generic `Stack<T>`

**INSTRUCTOR COPY — not for distribution**

---

## Before Marking

**Reference environment:** g++ 13.3.0, x86-64 Linux, `-std=c++17`. Symbol names, `sizeof` values and
error line counts are exact. Timings and addresses are not.

**Calibration:** this is the first problem set where a student can be defeated by the *error messages*
rather than the concepts. A submission with a broken `Stack<T>` and four pages of pasted template
errors is not a student who failed to understand templates — it is usually a student whose Week 1 Rule
of Three was shaky. **Check their PS 1 Part C before concluding otherwise.**

---

> **Revised 2026-09-22.** A2 (template vs hand-written assembly) was removed: Lab 2 Part A does it. A3–A5 are A2–A4. E's third
> error no longer uses `std::sort` on a `std::vector` (Week 3); it compares two `std::pair<P,int>`
> (Week 2). Measured: 6, 5 and 24 lines.

## Part A — Function Templates (20)

### A1 (5)

```
W int    maxof<int>(int, int)          _Z5maxofIiET_S0_S0_
W double maxof<double>(double, double) _Z5maxofIdET_S0_S0_
W long   maxof<long>(long, long)       _Z5maxofIlET_S0_S0_
```

The type argument is **`Ii`**, **`Id`**, **`Il`** — `I...E` delimits the template argument list.

*Marking: 2 the three symbols, 2 identifying the encoding. **Full marks require the `W`** to be present
in what they pasted, whether or not they comment on it — a student who explains that `W` is weak and
connects it to Lecture 03 §4 deserves a note of commendation, not extra marks.*

**A student who pasted nothing** hit the disappearing-symbol trap (their instantiations were inlined
away). That is the intended failure and the fix is explicit instantiation; award 1 if they diagnosed it
in writing.

### A2 (5)

```
error: no matching function for call to 'maxof(int, double)'
```

Three fixes: `maxof<double>(3, 7.5)`; `maxof(3.0, 7.5)`; two template parameters.

*Marking: 1 error, 2 the three fixes, 1 the judgement. **The expected production answer is the explicit
argument** — it is the smallest change and expresses the intent. Accept "make the literals agree" with a
good reason.*

### A3 (5)

`convert<double>(42)` — `Out` explicit, `In` deduced.

Reversed, callers must write `convert<int, double>(42)`, spelling out the parameter the compiler
already knew.

**Rule: non-deducible parameters must come first**, because explicit arguments fill the list left to
right.

*Marking: 2 working code, 2 the rule. The rule must mention ordering, not just "it's more typing".*

### A4 (5)

```
warning: possibly dangling reference to a temporary [-Wdangling-reference]
note: the temporary was destroyed at the end of the full expression 'maxof<int>(3, 7)'
```

```
ERROR: AddressSanitizer: stack-use-after-scope
```

*Marking: 2 compile-time diagnostic, 2 runtime. **`-Wdangling-reference` is new in GCC 13** — a student
on GCC 12 or clang who reports silence **and gives their version** gets full marks for that half. The
ASan report should appear regardless.*

---

## Part B — `Stack<T>` (36)

### B1 (10), B2 (10)

Reference implementation is in `stack_t.hpp`. Key points:

```cpp
template <typename T, int C> Stack<T,C>::Stack(const Stack& o)
    : data(new T[o.cap]), count(o.count), cap(o.cap) {
    for (int i = 0; i < count; ++i) data[i] = o.data[i];   // element-wise, not memcpy
}
template <typename T, int C> void Stack<T,C>::swap(Stack& o) noexcept { ... }
template <typename T, int C> Stack<T,C>& Stack<T,C>::operator=(Stack o) { swap(o); return *this; }
```

*Marking B1: 3 storage and growth, 3 push/pop/top, 2 both exceptions, 2 out-of-class definitions.*
*Marking B2: 4 deep copy constructor, 3 `noexcept` swap covering all members, 3 by-value copy-swap.*

**Grep for `== &`.** A leftover guard is a 3-point deduction and a comment.

**Common fault:** defining members inside the class body. It works, and it sidesteps the syntax B1 is
assessing. Deduct the 2 marks for out-of-class definitions and note that Part C will punish them
anyway.

### B3 (8)

Reference:

```
int:    size=6 cap=8 top=36
deep:   s.size=6 t.size=5
assign: u.size=6 u.top=36
string: size=2 top=grace
double: size=3 cap=4 (started at 2)
empty:  pop from empty stack
```

**Why `std::string` is the case that matters:** it is a `T` with its **own** Rule of Three and its own
heap allocation. It works only because the template made no assumption about `T` beyond
default-constructibility and assignability. An implementation that "works" for `int` and `double` may
be doing something bit-wise that `std::string` will expose.

*Marking: 6 for three types tested with growth and independence, 2 for the `std::string` justification.
**The justification must be about `T` having its own resource management**, not "strings are more
complicated".*

### B4 (8)

**(a) (3)** `Stack<int>` works — `int` is trivially copyable.

**(b) (5)** For `std::string`:

```
warning: 'void* memcpy(...)' writing to an object of type 'class std::__cxx11::basic_string<char>'
         with no trivial copy-assignment; use copy-assignment or copy-initialization instead
         [-Wclass-memaccess]
```

```
before copy: a-long-string-that-will-heap-allocate
after  copy: a-long-string-that-will-heap-allocate
ERROR: AddressSanitizer: attempting double-free
```

**The copy appears to succeed** — both print correctly. `memcpy` duplicated the `std::string` object's
bytes, *including its internal pointer to the heap-allocated characters*. Two `std::string` objects now
own one character buffer. It fails at **destruction**, and it is exactly **Week 1's shallow-copy double
free**, reintroduced inside a template.

*Marking: 3 for (a) plus the warning, 5 for (b). **Full marks require naming it as the Week 1 bug** and
identifying that the duplicated pointer is inside `std::string`, not inside `Stack`. A student who says
only "memcpy is wrong for non-trivial types" gets 3 of the 5 — true, and not an explanation.*

---

## Part C — Instantiation and the Header Rule (18)

### C1 (8)

```
undefined reference to `Stack<int>::Stack(int)'
undefined reference to `Stack<int>::push(int const&)'
undefined reference to `Stack<int>::size() const'
undefined reference to `Stack<int>::~Stack()'
```

`nm -C stack_defs.o` — **empty.**

**Why:** the `.cpp` had the definitions but nobody requesting `Stack<int>`, so nothing was instantiated
and nothing emitted. `main.cpp` had the request but not the definitions, so it emitted calls for the
linker to resolve. **Neither translation unit had both halves.**

*Marking: 3 errors, 2 the empty `nm`, 3 the explanation. **The explanation must identify that both
halves are needed in one translation unit.** "Templates must be in headers" restates the rule without
explaining it — 1 of the 3.*

### C2 (6)

(a) definitions moved to the header — links.
(b) `template class Stack<int>;` in the `.cpp` — links, **8 symbols**.

*Marking: 3 each. Accept any symbol count consistent with their member list; the point is that it went
from zero to non-zero.*

### C3 (4)

**Prefer explicit instantiation when the type list is closed** — e.g. a numeric template used only for
`float` and `double`. Benefits: implementation stays private; users do not recompile when it changes.

**Wrong choice when users need types you did not anticipate** — a general-purpose container. A user
wanting `Stack<char>` gets a link error and **cannot fix it without editing your `.cpp`**.

*Marking: 2 each. Full marks require naming **who is affected** — the library author's build times
versus the user's ability to instantiate.*

---

## Part D — Specialization and Non-Type Parameters (16)

### D1 (6)

```
Traits<double> : generic
Traits<int>    : int (full specialization)
Traits<char*>  : pointer (partial specialization)
Traits<int**>  : pointer (partial specialization -- T = int*)
```

*Marking: 4 implementation, 2 predictions recorded. **`Traits<int**>` is the interesting one** — it
matches `T*` with `T = int*`. A student who predicted "generic" for it and reported the correction has
demonstrated exactly the intended learning; award both prediction marks.*

### D2 (4)

`Stack<double,2>` starts at 2 and grows to 4. `Stack<int>` uses the default.

*Marking: 2 each.*

### D3 (6)

**(a)** `sizeof` = **16, 32, 64** for N = 4, 8, 16 — exactly `N * sizeof(int)`. **`N` is not stored
anywhere in the object; it is part of the type.**

**(b)** `error: could not convert 'b' from 'FixedArray<[...],9>' to 'FixedArray<[...],8>'`

**(c)** `error: the value of 'n' is not usable in a constant expression` — a non-type template argument
must be known at compile time, because it is part of a type, and types are compile-time entities.

*Marking: 2 each. (a)'s "where is N stored" is the assessed half — the answer is **nowhere in the
object**.*

---

## Part E — Reading Template Errors (10)

### E1 (4)

| Error | lines |
| --- | --- |
| plain type error | 6 |
| direct template | 5 |
| through `std::pair`'s `operator<` | 24 |

*Marking: 4. Accept ±20% on the 24; line counts vary with compiler version. **The ordering must hold**:
the direct template error is not longer than the plain one.*

### E2 (6)

**(a)** `stl_pair.h:836:24: error: no match for 'operator<' (operand types are 'const P' and 'const P')`
— line 5 of 24, inside a standard library header (g++ 13.3, re-run 2026-09-22).

**(b)** `required from here` is the **instantiation backtrace** — it records which use caused this
template to be instantiated, and following the chain upward leads from library internals back to the
student's own line.

**(c)** **Depth, not templates.** Error 2 is one level deep and is *shorter* than the non-template
error. Error 3 passes through the library's `operator<` for `pair` and then lists every candidate
`operator<` it tried, and each contributes context lines.

*Marking: 2 each. **(c) is the assessed idea of Part E.** "Templates have bad error messages" scores 0
— the student's own error 2 refutes it, and the question points this out.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 20 |
| B | 36 |
| C | 18 |
| D | 16 |
| E | 10 |
| **Total** | **100** |

---

## What to Watch For

1. **Members defined inside the class body** (B1). Sidesteps the syntax being assessed and will hurt
   them in Week 6.
2. **A leftover `this == &other`** (B2). Grep for it.
3. **"Templates have bad error messages"** in E2(c), contradicted by their own E1 table.
4. **`memcpy` explained as "wrong for non-trivial types"** without identifying the duplicated pointer
   (B4). True but not an explanation.
5. **Nothing pasted in A1.** The disappearing-symbol trap. Worth raising in Monday's lecture, since it
   has now caught students twice — Lecture 01 §2.1 and here.

---

## Feeding Into Week 3

Week 3 opens by comparing `std::vector` with the `Stack<T>` from B1. **Have two or three students'
implementations to hand** — the comparison lands much harder against code the room wrote than against a
slide.

The specific thing to draw out: their `Stack` uses `new T[n]`, which **default-constructs every
element** (L08 §4). `std::vector` does not, and cannot, because it must support types with no default
constructor — which is exactly the error a student hit in D3 if they tried it. That is the opening for
`std::allocator` and for why `vector`'s interface has both `size()` and `capacity()`.

---

*PROG 102 · Week 2 · PS 2 Solutions · © CSE Department*
