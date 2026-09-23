# PROG 102 · Programming II — Object-Oriented Design and Data Structures in C++
## Week 9: Exception Handling and Robust Software

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), CS 101
**Assessment for this course (overall):** Labs 20%, Problem Sets 30%, Midterms 25%, Final 15%, Projects 10%
**This week's deliverables:** PS 9 (released Fri 26 Mar 10:00, due **Fri 2 Apr 17:00**), Lab 9 (**Mon 29 Mar**, 15:00), Quiz 9 (**Tue 23 Mar**, 10:00, covers Week 8) · **PROJECT 1 DUE FRIDAY 26 MAR, 17:00**

---

### Why This Week Exists

You have been writing exception-safe code since Week 1 without being told what that means.

Copy-and-swap (L06 §2.3) gave you the **strong guarantee** — you measured it: after a thrown
`bad_alloc`, the object was untouched, where the four-step version left it use-after-free. RAII
(**Week 5**) is what made that possible. `noexcept` on `swap` and on move constructors (L18 §5) was
load-bearing and the reason was deferred to "Week 9".

**This is Week 9.** The vocabulary arrives, and with it the ability to say precisely what your code
promises when something fails — which is the difference between code that works and code you can
depend on.

**And Lab 8 ended on exactly this.** Your `publish()` had a handler throw, later subscribers were never
notified, and the list was half-pruned. Lecture 29 gives that state a name, and the name is *none of
the three*.

### Learning Objectives

By the end of Week 9, you should be able to:

1. Describe stack unwinding, and demonstrate that destructors run during it.
2. State the **three guarantees** — basic, strong, nothrow — precisely enough to test for them.
3. Determine which guarantee a given function provides, and **write a test that proves it**.
4. Upgrade an operation from basic to strong, and say what that costs.
5. Explain what `noexcept` means, where it is load-bearing, and what happens if you lie.
6. Use the `std::exception` hierarchy and know when to define your own.
7. **Measure** what exceptions cost on the happy path and on the throwing path — and know which
   "zero-cost" claim is true and which is not.
8. Distinguish an **assertion** from an **exception**, and say which a precondition violation deserves.
9. Write a test suite that checks failure behaviour, not just success.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L28 Exceptions and Stack Unwinding]] | `throw`/`catch`, unwinding, the hierarchy, and what it costs |
| [[L29 The Three Guarantees]] | Basic, strong, nothrow — demonstrated and tested |
| [[L30 noexcept Assertions and Contracts]] | `noexcept`, assertions vs exceptions, preconditions |
| [[PS 9 Making a Container Exception-Safe]] | Due Fri 2 Apr 17:00 |
| [[PROG102 Week9/assignments/QUIZ 9 Week 9 Tuesday\|QUIZ 9 Week 9 Tuesday]] | 15 minutes, covers Week 8 |
| [[LAB 9 Testing for Failure]] | A test framework, and tests that check what happens when things break |
| [[PROG102 Week9/resources/Reading Guide Week 9\|Reading Guide Week 9]] | Meyers, the standard's guarantees, and every command |
| [[PROG102 Week9/solutions_instructor/PS 9 Solutions\|PS 9 Solutions]] | Instructor only |
| [[PROG102 Week9/solutions_instructor/LAB 9 Solutions\|LAB 9 Solutions]] | Instructor only |

### The One Thing to Take From This Week

**"Exception-safe" is not a property. It is one of four specific promises, and you have to pick one.**

| Guarantee | Promise |
| --- | --- |
| **Nothrow** | This operation will not throw |
| **Strong** | It succeeds completely, or the state is unchanged |
| **Basic** | It may change the state, but nothing leaks and every invariant holds |
| **None** | Anything may have happened |

The last row is not a joke — it is where most code sits by default, including Lab 8's `publish()` and
including any function that modifies two things in sequence.

**Naming your guarantee is the deliverable.** A container documented as *basic* is more useful than one
described as "exception-safe", because a caller can plan around basic and cannot plan around a
adjective.

### The Measurement That Corrects a Slogan

"C++ exceptions are zero-cost." Measured, on identical source compiled with and without exception
support:

| | with exceptions | `-fno-exceptions` |
| --- | --- | --- |
| **Time**, happy path | 1.53–1.66 ns/call | 1.49–1.60 ns/call |
| **Code size** | **240 bytes** | **88 bytes** |

**Time on the happy path: genuinely free.** Code size: **2.7×**, for the unwind tables.

And when one actually throws: **about 1.68 µs** — roughly a thousand times a normal call.

> **So "zero-cost" means "zero *time* cost when nothing throws".** It is a claim about one of three
> axes, and the slogan drops the qualifier. Exceptions are for the exceptional; use them for failures,
> not for control flow.

### A Note on the Testing Framework

Lab 9 asks for a test suite. **The framework named in the curriculum is Catch2**, and it is the right
thing to learn.

It is **not installed on the reference machine**, so Lab 9 ships a **minimal Catch2-compatible header**
— same spellings for `TEST_CASE`, `SECTION`, `REQUIRE`, `CHECK`, `REQUIRE_THROWS_AS` — verified to
build clean under `-Wall -Wextra -pedantic` and to correctly report failures.

**If you have Catch2, use it**; your tests should compile against either with no changes, and that
compatibility is deliberate.

### Project 1 Is Due Friday

Everything this week applies to it directly — **Part 3.3 asks which guarantee your container provides**,
and after Lecture 29 you will be able to answer properly rather than guessing.

### Connections

**Back:** copy-and-swap (**W1**) was the strong guarantee before you had the name. RAII (**W5**) is the
mechanism. `noexcept` on moves (**W5 §L18 §5**) is explained here. Lab 8's throwing observer is
Lecture 29's opening example.

**Forward:** **Week 10**'s threads make everything harder — an exception in a thread that nobody joins
calls `std::terminate`. **Week 12**'s testing and profiling builds on Lab 9's suite.

---

*PROG 102 · Week 9 · © CSE Department*
