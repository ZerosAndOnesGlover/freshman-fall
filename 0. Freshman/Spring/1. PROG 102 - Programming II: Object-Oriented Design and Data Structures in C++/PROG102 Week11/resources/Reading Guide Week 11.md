# PROG 102 · Week 11 · Reading Guide
## Lambdas, and Reproducing the Measurements

---

## What to Read

| Source | Sections | Why |
| --- | --- | --- |
| **Meyers, *Effective Modern C++*** | **Items 31–34** | Lambdas. **The best treatment available.** |
| **Meyers** | **Items 23–30** | Move semantics and forwarding, properly |
| ***C++ Primer*** | **§10.3, §14.8, §16.2.6** | Lambdas, function objects, forwarding |
| **cppreference** | `std::function`, *lambda expression*, `constexpr` | Reference |

> **Meyers Item 31 — "Avoid default capture modes" — is the four pages that matter most this week.**
> It is Lecture 34 §2.2 and §3 in the author's own words, and his examples of `[=]` capturing `this`
> without appearing to are worth reading before you write another callback.

---

## Items 31–34

**Item 31 — avoid default capture modes.**

1. Meyers shows `[&]` producing a dangling reference. **Compare with L34 §3.** Does he mention that no
   compiler warns?
2. He shows `[=]` capturing `this` **without `this` appearing in the capture list**. **Why is that
   surprising**, and what does it mean for a lambda stored in a member?
3. What is his recommended alternative for capturing a member? *(C++14 init-capture, or C++17
   `[*this]`.)*

**Item 32 — use init capture to move objects into closures.**

4. Why can `[x]` not move? What does `[x = std::move(x)]` do that `[x]` cannot?
5. Give a case where moving into a closure genuinely matters. *(A `unique_ptr` captured by a lambda
   handed to a thread — **Week 10**.)*

**Item 33 — `decltype` on `auto&&` parameters.** Skim. It is about perfect-forwarding generic lambdas
and you are not required to write them.

**Item 34 — prefer lambdas to `std::bind`.**

6. `std::bind` predates lambdas. **Find two of Meyers' reasons to prefer a lambda.**
7. He notes `std::bind` is harder for compilers to inline. **Connect that to Lecture 35 §3's
   measurement.**

---

## `constexpr` and Modern Features

8. cppreference on `constexpr`: **what may a `constexpr` function not do**, in C++17?
9. Look up `consteval` (C++20). **What does it add that `constexpr` does not guarantee?** *(L36 §1.1.)*
10. Look up `if constexpr`. **Why must the untaken branch still be syntactically valid**, even though
    it is not compiled?

---

## Reproducing This Week's Measurements

**g++ 13.3.0, x86-64 Linux.** `sizeof` values and the SBO threshold are exact; timings are not.

### L34 §1 — A lambda is a class

```
g++ -std=c++17 -Wall -Wextra lambda_is_class.cpp -o lic && ./lic
```

**Expect:** hand-written functor and `[x]` lambda both **4** bytes; empty lambda **1**; `[&x]` **8**;
`[s]` with a `std::string` **32**.

### L34 §3 — The dangling capture

```
g++ -std=c++17 -Wall -Wextra -c dangle.cpp -o /dev/null      # NO warning
g++ -std=c++17 -O1 -g -fsanitize=address dangle.cpp -o dg && ./dg
```

**Expect:** silence from the compiler, `stack-use-after-return` from ASan. And with `[this]`:
`heap-use-after-free`, fixed by `[*this]`.

### L35 §3 — What a call costs

```
g++ -std=c++17 -O2 -Wall -Wextra callcost2.cpp -o cc2 && ./cc2
```

**Expect:** lambda **0.61–0.67 ns**, function pointer **1.50–1.54 ns**, `std::function`
**2.15–2.21 ns**.

> **Your first attempt will report 0.00 ns** for the lambda and the function pointer, because the
> compiler will hoist a call with constant arguments out of the loop. **That is Lab 11 Part A1** and
> you are expected to hit it.

### L35 §4 — The small-buffer threshold

```
g++ -std=c++17 -O2 -Wall -Wextra sbo17.cpp -o sbo17 && ./sbo17
```

**Expect:** `sizeof(std::function<int()>)` = 32, and allocation beginning at **17 bytes** of capture.

### L36 §1–3 — Modern features

```
g++ -std=c++17 -Wall -Wextra -pedantic modern.cpp -o mod && ./mod
```

**Expect:** `static_assert`s holding for `factorial(10)` and `fib(30)`; `std::array<int,
factorial(5)/24>` with 5 elements; `if constexpr` dispatching correctly.

---

## The Habit, in Its Final Form Before the Last Week

The instruction has been sharpened every week:

- **W2:** a correct measurement can carry a wrong explanation.
- **W3:** a correct theory can answer a different question.
- **W4:** your benchmark may measure something other than what you named it.
- **W5:** the optimizer can delete the thing you are measuring.
- **W6:** a program can be correct, pass every test, trip no sanitizer, and still be wrong.
- **W9:** a claim about failure is a claim until you have made it fail.
- **W10:** a passing run is not evidence; the instrumented run is.

**Week 11 adds the one about communication:** *a ratio without a denominator is not an answer.*

`std::function` is **3.5×** a lambda per call, **1.85×** inside a sort, and quite possibly **0.1%** of
your program. **All three are the same measurement**, and which one you quote determines whether a
colleague rewrites working code.

> **The number is not the finding. The number plus what it is a fraction of is the finding.**

That is worth carrying past this course, because it is the difference between a benchmark that informs
a decision and one that wins an argument.

---

## Before Week 12

1. Lectures 34–36 read; **Meyers Items 31–32** especially.
2. **Project 2 is assigned and due Week 12.** It is mostly Project 1 improved — start by fixing what
   Project 1's feedback said.
3. PS 11 is short. **Project 2 is worth more.**
4. Week 12 is the last: testing, profiling with `perf`, cache-aware programming, and system design. It
   measures the memory hierarchy directly and settles the argument that has been running since Week 3
   — **why a `vector` beats a `list` at the same complexity.**
5. **The final exam is in Week 12, and Lab 12 is your Project 2 demo.**

---

*PROG 102 · Week 11 · Reading Guide · © CSE Department*
