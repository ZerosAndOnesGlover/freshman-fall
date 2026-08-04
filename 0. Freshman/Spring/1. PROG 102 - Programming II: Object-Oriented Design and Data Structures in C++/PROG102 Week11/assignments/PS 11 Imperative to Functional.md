# PROG 102 · Problem Set 11
## Imperative to Functional

**Week 11 · Released Friday Week 11 · Due Friday Week 12, 17:00 · 100 points**
**Covers:** Lectures 34–36

> **Project 2 is due the same day, and the final exam is that week.** This problem set is short for
> that reason. **Project 2 is worth more; do this one second.**

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**Deliverables:** `lambdas.cpp`, `functional.cpp`, `costs.cpp`, `modern.cpp`, `ANSWERS.md`.
Name collaborators and state any generative-tool use.

---

## Part A — What a Lambda Is (26 pts)

**A1.** *(8)* Write a hand-written functor class and the lambda it corresponds to.

**Confirm they are the same `sizeof`**, that both work with `std::count_if`, and report the type traits
for the lambda: is it a class, copy-constructible, default-constructible?

**A2.** *(8)* **Predict `sizeof`** for six lambdas before measuring:

```
[]           [x]          [x,d]          [&x]          [s]  (std::string)          [&] using two
```

Report **predictions and measurements** in one table. **Explain any you got wrong.**

**A3.** *(4)* Show that `[x]` copies **at creation**: capture, modify the original, call.

Then make it `mutable` and show the lambda's own copy persisting across calls.

**A4.** *(6)* Reproduce the dangling capture: return a lambda from a function capturing a local **by
reference**, and call it.

- **(a)** *(2)* Report the warnings from `-Wall -Wextra -pedantic`.
- **(b)** *(2)* Catch it with AddressSanitizer and paste the report.
- **(c)** *(2)* Do the same with `[this]` inside a class whose object is destroyed first, and fix it
  with `[*this]`.

---

## Part B — Storing Callables (28 pts)

**B1.** *(10)* Measure the same lambda called 10⁸ times, three ways: **directly**, through a
**function pointer**, and through **`std::function`**. Three runs.

**Report ns per call for all three.**

> **If any version reports 0.00 ns, the compiler deleted your loop.** Make the arguments unhoistable
> and re-measure. Say in `ANSWERS.md` what you had to change.

**B2.** *(8)* Find **your** implementation's small-buffer threshold: instrument `operator new` and
sweep the capture size.

**Report the exact byte count at which `std::function` starts allocating**, and `sizeof(std::function
<int()>)`.

**B3.** *(4)* Write a lambda capturing a `std::string`.

**Predict whether assigning it to a `std::function` allocates**, then measure. Then capture the string
**by reference** and measure again. Explain both.

**B4.** *(6)* Week 8 measured `std::function` at **1.85×** a lambda inside `std::sort`. B1 will give you
roughly **3.5×** per bare call.

**Both are correct. Explain the difference in three sentences.**

---

## Part C — Functional Style (26 pts)

**C1.** *(14)* Take **seven** imperative loops — from your Project 1 code, PS 6, or written for this
purpose — and rewrite each with STL algorithms and lambdas.

At least one each of: a **map** (`transform`), a **filter** (`copy_if`/`remove_if`), a **fold**
(`accumulate`), a **search** (`find_if`), and a **partition** or **sort** with a custom comparator.

For each: both versions, and one line on which is clearer.

**C2.** *(6)* Write a function returning a **composed** operation — a lambda that captures and applies
two other callables in sequence.

Demonstrate it. **Say what its type is**, and why you needed `auto` or `std::function` to hold it.

**C3.** *(6)* **Nominate two** of your seven from C1 where the **imperative loop was better**, and
defend each in three sentences.

**Both nominations are required.** Week 3 §L12 §7 said to prefer algorithms; this is where you say
where that advice stops.

---

## Part D — Modern Features (20 pts)

**D1.** *(6)* Write a `constexpr` function containing a **loop**. Prove it ran at compile time
**two ways**: a `static_assert`, and using the result as a template argument (an `std::array` size).

**D2.** *(6)* Write a function template using `if constexpr` to dispatch over three type categories.

Then **rewrite it with a plain `if`** and paste the error. **Explain what `if constexpr` does that `if`
cannot.**

**D3.** *(4)* Rewrite three loops over a `std::map` using structured bindings. Report before and after.

**D4.** *(4)* Take one algorithm chain from C1 and **write what it would look like with C++20 ranges.**

You cannot compile it. Write it anyway, and say in two sentences what it would save.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 26 | What a lambda is, and the bug the compiler will not catch |
| B | 28 | The cost of storing a callable, measured |
| C | 26 | Functional style — **including where it is wrong** |
| D | 20 | `constexpr`, `if constexpr`, bindings, ranges |
| **Total** | **100** | |

---

## Submission Checklist

1. Clean build; sanitizer-clean except where A4 provokes reports.
2. A2 includes **predictions made before measuring.**
3. B1 states what you changed to stop the loop being optimized away.
4. B2 reports **your** threshold, not the lecture's.
5. C3 nominates **two** loops that should stay loops.
6. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 11 · Problem Set 11 · © CSE Department*
