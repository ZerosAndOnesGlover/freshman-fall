# PROG 102 · Week 1 · Reading Guide
## *C++ Primer* Chapters 13–14, and Reproducing the Measurements

---

## What to Read

| Source | Sections | Why |
| --- | --- | --- |
| ***C++ Primer*** | **§13.1–13.3** | Copy control. The core reading of the week. |
| ***C++ Primer*** | **Ch. 14** | Operator overloading. Read §14.1–14.5, §14.8. |
| **Meyers, *Effective C++*** | **Item 11** | "Handle assignment to self in `operator=`". Four pages, and the best short treatment of §7 of Lecture 05. |
| **cppreference** | *copy elision*, *rule of three* | For §6 of Lecture 06, which is newer than all three books |

> ***C++ Primer* is from 2012 and describes the C++11 rules.** For Week 1 that matters in exactly one
> place: **§13.1.1 on copy elision is out of date.** It describes elision as an optimization the
> compiler is permitted to perform. Since C++17, part of it is mandatory and part is not — Lecture 06
> §6 measures the difference. **Trust the lecture over the book here**, and check cppreference if you
> want the standard's own wording.

---

## §13.1 — Copy, Assign, Destroy

The chapter that matters. Read it slowly.

**Guiding questions:**

1. §13.1.1 — the book says the copy constructor's first parameter "must be a reference". **Why?**
   Answer without looking: what would happen if it took its parameter by value?
2. §13.1.2 — copy assignment. The book's version does **not** have a self-assignment guard in its first
   presentation. Find where it addresses this, and compare its treatment with Lecture 05 §7.
3. §13.1.3 — destructors. The book states that the destructor body runs *before* the members are
   destroyed. **Does that ordering matter for a class holding a raw pointer? For one holding a
   `std::vector`?**
4. §13.1.4 — the Rule of Three. The book calls it "the rule of three/five". **What does the class need
   to have for the rule to apply at all?**

---

## §13.2 — Copy Control and Resource Management

**Guiding questions:**

1. The book distinguishes classes that behave like **values** from those that behave like **pointers**.
   Which is `Roster` from Lab 1 meant to be, and which is it *as provided*?
2. §13.2.1 gives a `HasPtr` value-like class. **Compare its `operator=` to Lecture 06's copy-swap.**
   Which one needs a self-assignment guard, and why does the other not?
3. The book's reference-counted `HasPtr` in §13.2.2 is a preview of `std::shared_ptr` (Week 5). Read
   it, and note how much code it takes. That is the code `shared_ptr` replaces.

---

## §13.3 — Swap

Short and directly relevant.

**Guiding questions:**

1. Why does the book say to write `swap` as a **friend** or free function rather than only a member?
   *(The answer involves `std::swap` and argument-dependent lookup, and matters more in Week 3.)*
2. The book uses `using std::swap;` followed by an unqualified `swap(a, b)`. **What does this idiom
   achieve** that `std::swap(a, b)` does not?
3. Lecture 06 marks `swap` `noexcept` and the book does not emphasise this. **Why does the exception
   guarantee depend on it?**

---

## Chapter 14 — Operator Overloading

Read §14.1–14.5 and §14.8. **Skip §14.9 (overloading, conversions and operators) for now** — it is
about implicit conversion operators and is a Week 4 concern.

**Guiding questions:**

1. §14.1 — the book gives guidance on which operators to overload and which to leave alone. **Compare
   its advice with Lecture 04 §9.** Do they agree?
2. §14.2 — the book explains why `operator<<` must be a non-member. **Write down the reason before you
   read it**, then check.
3. §14.3 — equality. The book insists `==` and `!=` should always be defined together, each in terms of
   the other. Why is defining only `==` a problem in C++17? *(In C++20 it is not — `!=` is generated.)*
4. §14.5 — subscript. The book's `operator[]` pair returns `std::string&` and `const std::string&`.
   **Why is the return type of the `const` version not `std::string`?**
5. §14.8 — function-call operator. Note what the book calls a "function object". Lecture 04 §5 calls it
   a functor. Same thing. **Week 11 will show it is also what a lambda is.**

---

## Reproducing This Week's Measurements

All figures from **g++ 13.3.0, x86-64 Linux**. Copy counts and allocation counts are **exact and
should match**; addresses will not.

### L04 §2.1 — Member operators break symmetry

```
g++ -std=c++17 -fsyntax-only sym.cpp
```

**Expect:** `error: no match for 'operator*' (operand types are 'double' and 'V')`.

### L04 §3 — `operator<<` as a member

```
g++ -std=c++17 -Wall -Wextra shift2.cpp -o shift2 && ./shift2
```

**Expect:** `v << std::cout` compiles and prints `1`. This is the point — it is not broken, it is
backwards.

### L05 §7 — Self-assignment, traced

```
g++ -std=c++17 -Wall -Wextra -g -fsanitize=address trace.cpp -o trace && ./trace
```

**Expect:** `this == &o`, the old pointer freed, `o.d` equal to the *new* pointer, six bytes of `0xbe`,
and no NUL terminator.

> **`0xbe` is AddressSanitizer's fill pattern for freshly allocated memory.** Without `-fsanitize=address`
> you will see different garbage, and on a different allocator you may see zeros — which would make the
> bug *invisible*. That is worth thinking about.

### L05 §9 — What the warning flags catch

```
g++ -std=c++17 -Wall -Wextra -pedantic -c dep.cpp -o /dev/null      # silence
g++ -std=c++17 -Wall -Wextra -Wdeprecated-copy-dtor -c dep.cpp -o /dev/null
g++ -std=c++17 -Weffc++ -c dep.cpp -o /dev/null
```

**Expect:** nothing, then a deprecation warning, then the three-line `-Weffc++` report.

### L06 §2.3 — Exception safety

```
g++ -std=c++17 -Wall -Wextra -g -fsanitize=address excsafe.cpp -o excsafe
./excsafe        # four-step:  heap-use-after-free
./excsafe x      # copy-swap:  a="hello", untouched
```

### L06 §4 — What copy-swap costs

```
g++ -std=c++17 -O2 -Wno-mismatched-new-delete allocs.cpp -o allocs && ./allocs
```

**Expect:** 1000 / 0 / 1000 allocations for four-step / reusing / copy-swap. Identical at `-O0`.

### L06 §5–6 — Copy counting and elision

```
for cfg in "-std=c++11 -O0" "-std=c++11 -O0 -fno-elide-constructors" \
           "-std=c++17 -O0" "-std=c++17 -O0 -fno-elide-constructors" "-std=c++17 -O2"; do
    g++ $cfg count1.cpp -o c1 && ./c1
done
```

**Expect:** `V3 c = a + b;` shows 0 copies everywhere **except** C++11 with elision disabled, where it
shows 2.

---

## The Habit, Restated

Week 0's reading guide said: **do not believe a claim about C++ that you have not seen a compiler
make.** Week 1 gives you the sharpest example of why.

Every textbook and every tutorial will tell you that returning a large object by value is expensive
and you should avoid it. **Measure it.** In C++17 the answer is zero copies, guaranteed by the
standard, and the advice you have been given is fifteen years out of date.

The same is true in the other direction. Copy-swap is presented everywhere as *the* way to write
assignment, with its cost rarely mentioned. Lecture 06 §4 measures it: **a thousand allocations where
a reusing version does none.** That does not make copy-swap wrong — it makes it a choice, and you
cannot make a choice you did not know you had.

---

## Before Week 2

1. Lectures 04–06 read.
2. *C++ Primer* §13.1–13.3 worked through.
3. **PS 1 Parts A and B started.** Part D's measurements take minutes; the writing takes longer.
4. Lab 1's `Roster` repaired — Week 2 turns it into `Roster<T>`, and a broken `Roster` becomes a
   broken template, which is considerably harder to debug.

---

*PROG 102 · Week 1 · Reading Guide · © CSE Department*
