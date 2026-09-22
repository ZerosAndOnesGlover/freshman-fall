# PROG 102 · Week 9 · Reading Guide
## Exception Safety, and Reproducing the Measurements

---

## What to Read

| Source | Sections | Why |
| --- | --- | --- |
| **Meyers, *Effective C++*** | **Item 29** | "Strive for exception-safe code." **The best short treatment of the three guarantees.** |
| **Meyers, *Effective C++*** | **Item 8** | Destructors must not throw. Four pages, and the reason is `std::terminate`. |
| **Meyers, *Effective Modern C++*** | **Item 14** | `noexcept` — when it matters and what it buys |
| ***C++ Primer*** | **§5.6, §18.1** | The mechanics: `try`, `catch`, `throw`, the hierarchy |
| **cppreference** | any container operation | **The "Exception safety" clause on every one** |

> **Sutter's *Exceptional C++* is the canonical text** on this material if you want more. Its first
> chapters work through exception-safe container implementation in more detail than any course can.
> Not required, and genuinely excellent.

---

## Meyers Item 29 — The Chapter That Matters

**Guiding questions:**

1. Meyers gives the three guarantees. **Write them from memory first**, then check. Which one did you
   state least precisely?
2. He argues that a function's guarantee is **the weakest of the guarantees of the functions it calls.**
   Why? *(This is why Lab 9 D1 says "weakest observed, not best".)*
3. He presents copy-and-swap as the route to strong. **You wrote that in Week 1.** Re-read L06 §2.3's
   measurement with this week's vocabulary.
4. Meyers notes strong is not always achievable or affordable. **Find his example**, and compare with
   L29 §4.2's `vector::insert`.

---

## Item 8 — Destructors and Exceptions

**Guiding questions:**

1. What happens if a destructor throws **while an exception is already propagating**?
2. Meyers gives two options for a destructor whose cleanup can fail. **What are they, and which does he
   prefer?**
3. Destructors are implicitly `noexcept` since C++11. **Does that make his advice obsolete, or
   enforce it?**

---

## Item 14 — `noexcept`

**Guiding questions:**

1. Meyers says `noexcept` is "part of the interface". **What does that imply about removing it later?**
2. He explains why `vector` growth checks `is_nothrow_move_constructible`. **Restate the argument in
   terms of the strong guarantee.**
3. He warns against marking functions `noexcept` optimistically. **What is the penalty?** *(L30 §1.1
   measures it: exit 134.)*

---

## Reading cppreference for Guarantees

**This is the practical skill of the week.**

Open `std::vector` on cppreference and find, for `push_back`, `insert`, `erase` and `resize`, the
**Exception safety** clause.

**Guiding questions:**

1. Which of the four are strong? Which are basic?
2. `push_back` is strong. **What does the page say happens if the element's move constructor throws
   and is not `noexcept`?**
3. `erase` — what does the page require of the element type, and what does it guarantee?
4. Find one operation whose clause says **"if an exception is thrown, this function has no effect"**.
   That is the strong guarantee stated in the standard's own words.

**Every container page has these clauses**, and most programmers never read them. **They are the
contract**, and after this week you can act on them.

---

## Reproducing This Week's Measurements

**g++ 13.3.0, x86-64 Linux.**

### L28 §2 — Unwinding

```
g++ -std=c++17 -Wall -Wextra -pedantic unwind.cpp -o uw && ./uw
g++ -std=c++17 -g -fsanitize=address unwind.cpp -o uw_asan && ./uw_asan
```

**Expect:** `+ outer + middle + deep` then `- deep - middle - outer`; and a **400-byte leak** from the
raw `new[]` that unwinding did not clean up.

### L28 §5 — What exceptions cost

```
g++ -std=c++17 -O2 -c work.cpp -o work_exc.o
g++ -std=c++17 -O2 -fno-exceptions -DNO_EXC -c work.cpp -o work_no.o
g++ -std=c++17 -O2 same.cpp work_exc.o -o s_exc && ./s_exc
g++ -std=c++17 -O2 same.cpp work_no.o  -o s_no  && ./s_no
size work_exc.o work_no.o
```

**Expect:** times indistinguishable (1.53–1.66 vs 1.49–1.60 ns), and **240 vs 88 bytes** of text.

**Throwing:** about **1.68 µs** per throw.

### L29 §3–4 — The guarantees

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined guarantees.cpp -o gu && ./gu
```

**Expect:** basic goes 2 → **4**; strong goes 2 → **2**; no leaks.

### L30 §1.1 — Lying about `noexcept`

```
g++ -std=c++17 -Wall -Wextra liar.cpp -o liar     # -Wterminate
./liar                                            # exit 134
```

**Expect:** the warning, `terminate called`, and **the `catch (...)` never running.**

---

## A Note on the Testing Framework

The curriculum names **Catch2**. It is not installed on the reference machine, and Lab 9 therefore
ships a **minimal Catch2-compatible header** — verified clean under `-Wall -Wextra -pedantic`, with the
same spellings for `TEST_CASE`, `SECTION`, `REQUIRE`, `CHECK` and `REQUIRE_THROWS_AS`.

**If you have Catch2, use it.** Your `tests.cpp` should compile against either unchanged, and that
compatibility is deliberate — it is also a small demonstration of Week 7's Adapter idea, in that the
fallback exists to make one thing fit another's interface.

**Do not treat the fallback as equivalent to Catch2.** It has no test filtering, no tags, no matchers,
no BDD syntax, and no generators. It is enough for this lab and no more, and that limitation is stated
rather than hidden.

---

## The Habit, in Its Ninth Form

- **W2:** a correct measurement can carry a wrong explanation.
- **W3:** a correct theory can answer a different question.
- **W4:** your benchmark may measure something other than what you named it.
- **W5:** the optimizer can delete the thing you are measuring.
- **W6:** a program can be correct, pass every test, trip no sanitizer, and still be wrong.

**Week 9 adds the one this week is built on:** *a claim about failure behaviour is a claim, until you
have made it fail.*

Everything in Lecture 29 is testable and almost nobody tests it. "This container is exception-safe" is
said constantly and means nothing; **"`insert` provides the basic guarantee, verified by sweeping the
failure point across all seven copies it performs"** is a fact.

And Lab 9 §A2 makes the same point about the tests themselves: **a suite that has never failed is not
evidence of anything.** Break one deliberately, watch it report, and then you know the suite can see.

---

## Before Week 10

1. Lectures 28–30 read; **Meyers Items 8, 14 and 29.**
2. **Project 1 was due Friday.**
3. **PS 9 is the best revision for Midterm 2's Weeks 5–9 content.** Start it early in the week.
4. Week 10 is **concurrency**, and it breaks much of this week: an exception escaping a thread's
   function calls `std::terminate` with no chance to catch it, and `shared_ptr`'s refcount finally
   takes the atomic path Week 5 §L17 §4.1 measured around.
5. **Midterm 2 is Tuesday 30 March** (Week 10), covering **Weeks 5–9**. Its revision guide ships with Week 10's
   materials, but the checklist in Week 4's guide shows you the format.

---

*PROG 102 · Week 9 · Reading Guide · © CSE Department*
