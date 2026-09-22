# PROG 102 · Problem Set 11
## Imperative to Functional

**Released:** Friday 9 April 2027, 10:00 · Week 11 (after Thursday's L36)
**Due:** Friday 16 April 2027, 17:00 · Week 12 — late penalty from 17:01
**Points:** 100 · counts toward the Problem Sets component (30%, lowest one dropped)
**Expected time:** about 3–4 hours

## What this problem set uses

Weeks 0–11: the STL algorithms of Lecture 12, and this week — what a lambda is, capture, `mutable`,
`[this]`/`[*this]` and the dangling capture (L34), `std::function` and type erasure (L35),
`constexpr`, `if constexpr`, structured bindings and the ranges preview (L36).

**Not needed and not expected:** testing frameworks and profilers (Week 12). Timing callables and
finding `std::function`'s allocation threshold are Lab 11's job, not this set's.

> **Project 2 is due the same day, and the final exam is Thursday 22 April.** This problem set is short for
> that reason. **Project 2 is worth more; do this one second.**

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**Deliverables:** `lambdas.cpp`, `functional.cpp`, `modern.cpp`, `ANSWERS.md`.
Name collaborators and state any generative-tool use.

---

## Part A — What a Lambda Is (35 pts)

**A1.** *(10)* Write a hand-written functor class and the lambda it corresponds to.

**Confirm they are the same `sizeof`**, that both work with `std::count_if`, and report the type traits
for the lambda: is it a class, copy-constructible, default-constructible?

**A2.** *(10)* **Predict `sizeof`** for six lambdas before measuring:

```
[]           [x]          [x,d]          [&x]          [s]  (std::string)          [&] using two
```

Report **predictions and measurements** in one table. **Explain any you got wrong.**

**A3.** *(6)* Show that `[x]` copies **at creation**: capture, modify the original, call.

Then make it `mutable` and show the lambda's own copy persisting across calls.

**A4.** *(9)* Reproduce the dangling capture: return a lambda from a function capturing a local **by
reference**, and call it.

- **(a)** *(3)* Report the warnings from `-Wall -Wextra -pedantic`.
- **(b)** *(3)* Catch it with AddressSanitizer and paste the report.
- **(c)** *(3)* Do the same with `[this]` inside a class whose object is destroyed first, and fix it
  with `[*this]`.

---

## Part B — Functional Style (32 pts)

**B1.** *(16)* Take **seven** imperative loops — from your Project 1 code, PS 6, or written for this
purpose — and rewrite each with STL algorithms and lambdas.

At least one each of: a **map** (`transform`), a **filter** (`copy_if`/`remove_if`), a **fold**
(`accumulate`), a **search** (`find_if`), and a **partition** or **sort** with a custom comparator.

For each: both versions, and one line on which is clearer.

**B2.** *(8)* Write a function returning a **composed** operation — a lambda that captures and applies
two other callables in sequence.

Demonstrate it. **Say what its type is**, and why you needed `auto` or `std::function` to hold it.

**B3.** *(8)* **Nominate two** of your seven from B1 where the **imperative loop was better**, and
defend each in three sentences.

**Both nominations are required.** Lecture 12 §7 said to prefer algorithms; this is where you say
where that advice stops.

---

## Part C — Modern Features (33 pts)

**C1.** *(9)* Write a `constexpr` function containing a **loop**. Prove it ran at compile time
**two ways**: a `static_assert`, and using the result as a template argument (an `std::array` size).

**C2.** *(9)* Write a function template using `if constexpr` to dispatch over three type categories.

Then **rewrite it with a plain `if`** and paste the error. **Explain what `if constexpr` does that `if`
cannot.**

**C3.** *(7)* Rewrite three loops over a `std::map` using structured bindings. Report before and after.

**C4.** *(8)* Take one algorithm chain from B1 and **write what it would look like with C++20 ranges.**

You cannot compile it. Write it anyway, and say in two sentences what it would save.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 35 | What a lambda is, and the bug the compiler will not catch |
| B | 32 | Functional style — **including where it is wrong** |
| C | 33 | `constexpr`, `if constexpr`, bindings, ranges |
| **Total** | **100** | |

---

## Submission Checklist

1. Clean build; sanitizer-clean except where A4 provokes reports.
2. A2 includes **predictions made before measuring.**
3. B3 nominates **two** loops that should stay loops.
4. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 11 · Problem Set 11 · © CSE Department*
