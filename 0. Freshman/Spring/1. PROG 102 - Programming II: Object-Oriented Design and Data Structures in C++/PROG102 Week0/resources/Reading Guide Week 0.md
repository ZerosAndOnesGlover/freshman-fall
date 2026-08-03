# PROG 102 · Week 0 · Reading Guide
## *C++ Primer* Chapters 1–2, and How to Check Everything Yourself

---

## How to Read a C++ Book

You have four books on the reading list and you will not read four books. Here is the division of
labour for Week 0:

| Book | This week | How |
| --- | --- | --- |
| **Lippman, *C++ Primer*** | Ch. 1, §2.3–2.5, §7.1–7.3 | **Work through it.** This is the one you read. |
| **Stroustrup, *The C++ Programming Language*** | §16.2 if curious | **Look things up.** Do not read it linearly. |
| **Meyers, *Effective Modern C++*** | Not yet | From Week 5, when the items will make sense |
| **Gang of Four, *Design Patterns*** | Not yet | Weeks 7–8 |

**Also keep [cppreference.com](https://en.cppreference.com) open.** It is more accurate and far more
current than any of the four, and learning to read its notation is a genuine course objective. When a
book and cppreference disagree, cppreference is right.

> **A warning about *C++ Primer*.** It is excellent and it is from **2012**, three standards ago. Where
> it and the lectures disagree about modern practice, the lectures win. Specific places this bites in
> Week 0: it will show you `NULL` where you should write `nullptr`, and it predates the `= default`
> and `= delete` idioms being routine.

---

## Chapter 1 — Getting Started

Skim this. You can already program; you are here for the notation.

**Read properly:** §1.2 on `std::cout` and `std::endl`, and §1.4.2 on the `for` loop over a container.

**Guiding questions:**

1. What does `std::endl` do that `"\n"` does not, and when do you actually want it?
2. `std::cin >> x` — what happens if the input is not a number? *(The book is thin on this. It matters
   in Week 9.)*
3. Why does `#include <iostream>` use angle brackets, and when would you use quotes?

---

## Chapter 2 — Variables and Basic Types

The chapter that matters this week. Three sections deserve real attention.

### §2.3 — Compound Types (references and pointers)

**This is the most important reading of Week 0.** References have no C equivalent, and Lectures 02 and
03 assume them completely.

**Guiding questions:**

1. After `int x = 5; int& r = x;`, what is `&r`? **Verify your answer by printing it.**
2. Can a reference be reseated to refer to a different object? What syntax would you try, and what
   does it actually do?
3. Why must a reference be initialized when a pointer need not be?
4. When is `T&` the right parameter type, and when is `const T&`? *(Answer: `const T&` far more often.
   Lecture 00 §5.3.)*

### §2.4 — `const`

Read this twice. `const` in C++ does considerably more than in C, and Week 0's Lecture 03 depends on
it.

**Guiding questions:**

1. What is the difference between `const int* p`, `int* const p`, and `const int* const p`?
2. Why does a `const` reference bind to a temporary when a non-`const` reference does not?
3. The book covers `const` on *objects*. Lecture 03 covers `const` on *member functions*. **What is
   the connection?** *(Hint: the type of `this`.)*

### §2.5 — Dealing with Types

`auto` and `decltype`. Read §2.5.2 on `auto` carefully; skim `decltype`, which you need only to
recognise.

**Guiding question:** in `auto x = expr;`, is `x` ever a reference? *(This has a surprising answer and
Week 5 depends on it.)*

---

## §7.1–7.3 — Defining Classes

Read alongside Lectures 01–03 rather than before them.

**Guiding questions:**

1. §7.1.2 — the book introduces `this`. **Does it say what `this` costs?** Lecture 01 answers this by
   compiling to assembly; compare the two treatments.
2. §7.1.4 — constructors. What is the difference between the *initializer list* and assignment in the
   body, and when is it not a matter of preference?
3. §7.2 — access control. The book says `private` "prevents access". **After Lecture 03 §1.2, is that
   phrasing precise enough?**
4. §7.3.2 — `mutable`. What is the example the book gives, and does it meet Lecture 03's standard for
   legitimate use?

---

## Reproducing Every Measurement in This Week's Lectures

**Every number in Lectures 00–03 was produced by running something.** None of it is quoted from
memory, and you should be able to reproduce all of it. Here is how.

All lecture measurements used **g++ 13.3.0, x86-64 Linux, `-std=c++17`**. Your numbers for `sizeof`
and the assembly should match exactly. The garbage values in L02 §4.1 will not, and the guide below
says why.

### L01 §2 — Member and free functions compile identically

```
g++ -std=c++17 -O1 -S -masm=intel this_ptr.cpp -o this_ptr.s
sed -n '/^_ZN7Counter3addEi:/,/ret/p' this_ptr.s
sed -n '/^_Z8add_freeP7Counteri:/,/ret/p' this_ptr.s
```

**Expect:** identical bodies, both `add DWORD PTR [rdi], esi`.

**If the member function is missing**, you defined it inside the class body — see L01 §2.1. That is
the intended trap.

### L01 §3 — Objects do not grow when you add member functions

```
g++ -std=c++17 -Wall -Wextra sizes.cpp -o sizes && ./sizes
```

**Expect:** 16, 16, 1, 1. These are exact and machine-independent on any 64-bit platform.

### L01 §4 — Mangling

```
g++ -std=c++17 -c mangle.cpp -o mangle.o
nm mangle.o                 # raw
nm -C mangle.o              # demangled
echo '_ZNK3app6Widget4drawEdd' | c++filt
```

**Expect:** `_ZNK...` for the `const` overload, and `plain_c_function` unmangled under `extern "C"`.

### L02 §4.1 — The declaration-order bug

```
g++ -std=c++17 -Wall -Wextra -c realbug.cpp -o /dev/null    # read the warnings
g++ -std=c++17 -g realbug.cpp -o rb0 && ./rb0               # -O0
g++ -std=c++17 -O2  realbug.cpp -o rb2 && ./rb2             # -O2
```

**Expect:** `-Wreorder` **and** `-Wuninitialized`, and an allocation wildly larger than the four
integers requested.

> **Your numbers will differ from the lecture's, and that is the correct result.** The lecture reports
> 99,539,950 integers at `-O0` and 1,600,677,166 at `-O2`. Those are whatever bytes happened to be in
> that stack slot on that run of that binary. **Reading uninitialized memory has no defined value, so a
> reproducible number would be the surprising outcome.** What must reproduce is that the number is
> large and wrong.

### L02 §5.2 — Heap objects and leaks

```
g++ -std=c++17 -g leak2.cpp -o leak2 && ./leak2
valgrind --leak-check=full ./leak2
```

**Expect:** `dtor heap` never printed, and `definitely lost: 8 bytes in 1 blocks`.

### L03 §1.2 — `private` is compile-time only

```
g++ -std=c++17 -fsyntax-only err1.cpp        # the error
g++ -std=c++17 -Wall -Wextra wk0.cpp -o wk0 && ./wk0    # the memcpy read
```

**Expect:** an error for naming the member, and `4200` printed for reading its bytes.

### L03 §4 — `inline` is a linkage rule

```
g++ -std=c++17 -c a.cpp -o a.o && g++ -std=c++17 -c b.cpp -o b.o && g++ a.o b.o -o prog
nm a.o | grep square
```

**Expect:** `multiple definition` without `inline`; links with it; symbol type `T` → `W`.

---

## A Habit Worth Forming Now

**Do not believe a claim about C++ that you have not seen a compiler make.**

This applies to the lectures. Every measurement above is reproducible in under a minute, and the
commands are given so that you can check rather than trust. If one of them does not reproduce on your
machine, that is worth raising — either the lecture is wrong or your setup differs in a way that is
itself interesting.

It applies far more to the internet. C++ has an unusually large volume of confident, outdated advice
attached to it: `inline` described as a speed hint (L03 §4.3), `NULL` instead of `nullptr`, and
`std::endl` everywhere. Much of it was correct in 1998.

**The compiler on your machine is the authority on what your compiler does.** `-S`, `nm`, `c++filt`
and `sizeof` are how you ask it.

---

## Before Week 1

1. Lectures 00–03 read, **in that order**.
2. *C++ Primer* §2.3 worked through — references specifically.
3. Your toolchain confirmed by Lab 0 Part A.
4. **PS 0 Part E attempted.** Week 1's first lecture opens on exactly that double-free, and it lands
   much harder if you have watched it happen to your own code.

---

*PROG 102 · Week 0 · Reading Guide · © CSE Department*
