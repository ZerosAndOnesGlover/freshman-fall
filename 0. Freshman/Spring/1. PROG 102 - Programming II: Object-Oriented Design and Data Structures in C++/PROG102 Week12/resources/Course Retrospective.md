# PROG 102 · Course Retrospective
## What This Course Argued, and What to Read Next

---

## The Thesis

The syllabus opened with one sentence:

> **Every abstraction in C++ has a cost. Name it, measure it, then decide whether to pay it.**

Twelve weeks later, here is what that produced.

| Abstraction | Cost, measured |
| --- | --- |
| A member function | **Nothing.** Byte-identical to a free function taking `this` |
| A template instantiation | **Nothing at runtime.** ~416 bytes and ~14 ms of compile time each |
| An iterator | **Nothing.** And a hundred algorithms for forty lines |
| A virtual call | **~2 ns**, and it blocks inlining |
| `unique_ptr` | **Nothing** — and the raw version leaks on a throw |
| `shared_ptr` | ~4 ns single-threaded; **57 ns** under four-thread contention |
| A move | Constant, against $O(n)$ for a copy: **~1 ms vs 0.1 µs** per 1 MB |
| A decorator layer | **0.58 ns** |
| `std::function` | **3.5×** a lambda per call, plus a heap allocation past 16 bytes |
| An exception | **Free** in time when not thrown; 2.7× the code; **1.68 µs** when thrown |
| A mutex | ~3.5× an atomic |
| **A cache miss** | **~138 ns — ninety times an L1 hit** |

**The last row dominates every other row on this list**, and the course arranged itself so that you
would find that out at the end rather than be told it at the start.

---

## The Second Thesis, Which Was Not on the Syllabus

Every week added a clause to the same instruction, and by Week 12 it had become the more valuable half
of the course.

| Week | The lesson |
| --- | --- |
| **0** | Do not believe a claim about C++ you have not seen a compiler make |
| **1** | Advice can be fifteen years out of date. Measure it |
| **2** | A correct measurement can carry a wrong explanation. **Run a control** |
| **3** | A correct theory can answer a different question |
| **4** | Your benchmark may measure something other than what you named it |
| **5** | **The optimizer can delete the thing you are measuring** |
| **6** | A program can be correct, pass every test, trip no sanitizer, and be wrong |
| **9** | A claim about failure is a claim until you have made it fail |
| **10** | A passing run is not evidence; the instrumented run is |
| **11** | **A ratio without a denominator is not an answer** |
| **12** | The rules give you the direction; only the benchmark gives you the crossover |

**Every one of those was learned by getting it wrong**, in materials written by someone who already
knew the trap existed. That is not a confession — it is the point. **The traps are not avoidable by
being careful. They are avoidable by checking.**

---

## What Was Corrected Along the Way

Worth listing, because a course that never revises its own claims is not doing this honestly.

- **Week 3 said the vector/list gap was about the container.** Week 12 showed a `vector` read in random
  order is **as slow as a list**. It was the access order.
- **Week 4 asserted that blocked vectorization dominates virtual-call cost.** Measured: ratio 2.20× at
  `-O2` and 2.23× at `-O3`. The mechanism is real and **did not explain the gap**.
- **Week 8 implied lambdas obsoleted Strategy.** True — and `std::function`, the obvious modern
  spelling, is **slower than the 1994 pattern**.
- **Week 12 expected AoS to beat SoA when all fields are used.** It did not, on this machine. Direction
  confirmed, crossover not.

**Four claims that a textbook would have stated and moved past.** Each survives here in corrected form,
with the measurement that corrected it.

---

## What You Can Do Now

Concretely, and it is more than it feels like:

- **Read a class and say what the compiler generates for it**, and what each generated function does.
- **Write a container** with iterators that work with the standard algorithms — and that the wrong
  algorithms correctly refuse.
- **State which exception guarantee an operation provides**, and produce the evidence.
- **Find a data race** with a tool, and explain why the tool is necessary.
- **Read a profile** and know that the answer is usually allocation or access pattern.
- **Design a benchmark that is not lying to you**, which is rarer than it sounds.

**And the meta-skill:** when someone tells you what code does — a colleague, a book, a blog post, or
you — **you know there is a way to find out, and roughly how long it takes.**

---

## What You Do Not Know Yet

An honest list, because the syllabus promised one:

- **Move semantics in depth** — forwarding references, reference collapsing, `std::forward`. You can
  recognise them; you cannot yet write a perfect-forwarding factory from scratch.
- **The memory model** — acquire/release, relaxed atomics, lock-free data structures. Week 10 used
  `seq_cst` throughout and said so.
- **Template metaprogramming** — SFINAE, `enable_if`, concepts. `if constexpr` covered most of what you
  needed and hid the rest.
- **C++20** — concepts, ranges, coroutines, modules. Week 11 §L36 §4 previewed ranges because they will
  change how you write everything from Week 3.
- **Allocators, and writing one.**
- **Build systems.** You have used `g++` directly all term, which is the right way to learn and the
  wrong way to ship.

---

## What to Read Next

In order.

1. **Meyers, *Effective Modern C++*.** You have read Items 8, 14, 18–25, 31–34. **Read the rest.** It is
   the single best return on time available to you now.
2. **Williams, *C++ Concurrency in Action*.** Week 10 used three chapters of it. The memory-model
   chapters are the natural next step and are genuinely hard.
3. **Sutter, *Exceptional C++*.** Week 9 in much more depth, in a problem-and-solution format that
   suits this material.
4. **Drepper, *What Every Programmer Should Know About Memory*.** Free, long, and the full version of
   Lecture 39.
5. **cppreference, continuously.** You have been using it since Week 3. Keep going.
6. **A large open-source C++ codebase.** Read one. You now have the vocabulary, and Lab 12 gave you the
   practice.

---

## The Last Thing

You started this course by compiling a member function and a free function and comparing the assembly,
to find out whether a claim in a lecture was true.

You are ending it by shuffling an index array to find out whether a claim in **Week 3 of the same
course** was true.

**It was not, quite.** And you have the measurement.

> **That is the whole thing.** C++ is the vehicle and it will change — the language you write in ten
> years will have absorbed half of Weeks 7 and 8 into features, the way C++11 absorbed Strategy. What
> will not change is that software is full of confident claims, most of them well-meant, and that
> **there is almost always a way to go and look.**

Go and look.

---

*PROG 102 · Week 12 · Course Retrospective · © CSE Department*
