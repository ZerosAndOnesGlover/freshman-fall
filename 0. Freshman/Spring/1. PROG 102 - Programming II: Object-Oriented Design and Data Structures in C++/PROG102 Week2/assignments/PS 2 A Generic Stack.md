# PROG 102 · Problem Set 2
## A Generic `Stack<T>`

**Released:** Friday 5 February 2027, 10:00 · Week 2 (after Thursday's L09)
**Due:** Friday 12 February 2027, 17:00 · Week 3 — late penalty from 17:01
**Points:** 100 · counts toward the Problem Sets component (30%, lowest one dropped)
**Expected time:** about 4–5 hours

## What this problem set uses

Weeks 0–2: the Rule of Three and copy-swap (Week 1), throwing an exception (L04 §4.2), function
templates and deduction (L07), class templates, the header rule, non-type parameters and `std::pair`
(L08), instantiation, specialization and reading template errors (L09). `std::string` is used only
as an element type, as the lectures use it.

**Not needed and not expected:** `std::vector`, `std::sort` or any other STL container or algorithm
(Week 3), move semantics (Week 5). Comparing template and hand-written assembly is Lab 2's job.

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**No warnings**, except where a part explicitly asks you to provoke one.

**Deliverables:** `stack.hpp`, `stack_test.cpp`, `traits.cpp`, `errors.md`, and `ANSWERS.md`.
Name collaborators and state any generative-tool use at the top of `ANSWERS.md`.

**You may not use `std::vector`, `std::array`, `std::stack` or `std::string`'s dynamic behaviour as a
substitute for your own storage.** You may use `std::string` as an *element type* — indeed Part B
requires it.

---

## Part A — Function Templates (20 pts)

**A1.** *(5)* Write `template <typename T> T maxof(T a, T b)`.

Instantiate it explicitly for `int`, `double` and `long`. Run `nm` on the object file and paste the
three mangled symbols. **For each, identify the substring encoding the type argument.**

**A2.** *(5)* Call `maxof(3, 7.5)` and paste the error.

Then fix it **three** ways. In one sentence, say which you would use in production and why.

**A3.** *(5)* Write `template <typename Out, typename In> Out convert(In value)`.

Call it as `convert<double>(42)`. Then **swap the two template parameters** in the declaration and show
what the call site must become. **State the rule this demonstrates about parameter ordering.**

**A4.** *(5)* Write the `const T&` version of `maxof` that returns `const T&`, and demonstrate the
dangling reference.

Report **both** what the compiler says at build time and what AddressSanitizer says at run time.
*(If your compiler is silent at build time, say so and give its version — this diagnostic is recent.)*

---

## Part B — `Stack<T>` (36 pts)

**B1.** *(10)* A class template `Stack<T>` with private `T* data; int count; int cap;` and:

```
Stack()            push(const T&)     pop()  -> T
size() const       top() const -> const T&   capacity() const
empty() const
```

`pop` and `top` must `throw std::underflow_error` (from `<stdexcept>`, as in Lecture 04 §4.2) when empty. `push` must grow the storage by doubling
when full.

**Define the members outside the class body**, using the `template <typename T> ... Stack<T>::` form.

**B2.** *(10)* The full Rule of Three: copy constructor, `noexcept` `swap`, and copy assignment written
as **copy-swap**.

**No `this == &other` comparison anywhere.**

**B3.** *(8)* Test it with **three** element types: `int`, `std::string`, and a small `struct` of your
own with its own Rule of Three.

For each: force at least one growth, make a copy, modify the copy, and show the original is unchanged.
**All sanitizer-clean.**

**The `std::string` case is the one that matters** — say in one line why in `ANSWERS.md`.

**B4.** *(8)* In your copy constructor, replace the element-copy loop with `std::memcpy`.

- **(a)** *(3)* Show `Stack<int>` still works.
- **(b)** *(5)* Show what happens for `Stack<std::string>`. Paste the compiler warning **and** the
  sanitizer report.

**Then explain**: the copy appears to succeed and prints the right string. Where does it actually fail,
and which Week 1 bug is this?

---

## Part C — Instantiation and the Header Rule (18 pts)

**C1.** *(8)* Split your `Stack<T>` into `stack_decl.hpp` (declarations only) and `stack_defs.cpp`
(definitions), and try to build a program that uses `Stack<int>`.

Paste the linker errors **and** the output of `nm stack_defs.o`.

**Explain in two sentences why `stack_defs.o` contains what it contains.**

**C2.** *(6)* Fix it **two** ways:

- **(a)** *(3)* Move the definitions into the header.
- **(b)** *(3)* Keep them in the `.cpp` and add explicit instantiation.

Show `nm` output after (b), and state how many symbols appeared.

**C3.** *(4)* Give one concrete situation where you would prefer (b), and one where (b) would be the
wrong choice. Be specific about who is affected.

---

## Part D — Specialization and Non-Type Parameters (16 pts)

**D1.** *(6)* Write `Traits<T>` with:

- a generic version reporting `"generic"`;
- a **full specialization** for `int`;
- a **partial specialization** for `T*`.

**Predict the output** for `Traits<double>`, `Traits<int>`, `Traits<char*>` and `Traits<int**>` before
running. Report predictions and results.

**D2.** *(4)* Add a non-type parameter to your stack: `template <typename T, int InitialCap = 4>`.

Show `Stack<double, 2>` starting at capacity 2 and growing. Show that `Stack<int>` still works with no
second argument.

**D3.** *(6)* Write `FixedArray<T, N>` holding `T data[N]`.

- **(a)** *(2)* Report `sizeof` for `N` = 4, 8, 16. **Where is `N` stored?**
- **(b)** *(2)* Write a function taking `FixedArray<int,8>` and pass it a `FixedArray<int,9>`. Paste
  the error.
- **(c)** *(2)* Try `int n = 8; FixedArray<int, n> a;`. Paste the error and explain in one sentence.

---

## Part E — Reading Template Errors (10 pts)

**E1.** *(4)* Produce three errors and record the **line count** of each:

1. an ordinary non-template type error;
2. a direct template error — your `maxof` on a type with no `operator>`;
3. comparing two `std::pair<P, int>` with `<`, where `P` has no `operator<` (`std::pair` is Lecture 08 §6).

Put the counts in a table in `errors.md`. (Lecture 09 §5 measured an error through `std::sort`; you are
doing the same with the one library template you have met.)

**E2.** *(6)* For error 3:

- **(a)** *(2)* Quote the **one line** that actually identifies the problem, and say how far down it is.
- **(b)** *(2)* Quote a `required from here` line and say what it is telling you.
- **(c)** *(2)* Error 2 is *shorter* than error 1 on the reference machine. **What does that tell you
  about why error 3 is long?** The answer is not "templates".

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 20 | Function templates, deduction, and zero-cost verified |
| B | 36 | A correct generic container with the Rule of Three |
| C | 18 | Why template definitions live in headers |
| D | 16 | Specialization and non-type parameters |
| E | 10 | Reading a 78-line error message |
| **Total** | **100** | |

**Where the marks actually are:** B is the implementation and it is worth the most. But **A2, B4, C1
and E are 30 points for running things and reporting what happened** — and B4 and E are the two that
students who skip come to regret in Week 6, when a broken templated iterator produces exactly these
errors.

---

## Submission Checklist

1. Clean build, no warnings except B4(b) and Part E.
2. Sanitizer-clean except where B4(b) provokes a report.
3. No `this == &other` anywhere in `Stack`.
4. Part B tested with **three** element types, one of them `std::string`.
5. Part D includes predictions made before running.
6. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 2 · Problem Set 2 · © CSE Department*
