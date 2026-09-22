# PROG 102 · Lab 5
## Leak Detection with AddressSanitizer

**Date:** Monday 1 March 2027 · 15:00–16:50 · Lab section (Week 6) — covers Week 5 (L16–L18)
*2-hour lab · 40 points · in-lab checkoff · part of the Labs component (20%)*
**Deliverable:** `registry.cpp` (repaired), `RESULTS.md`. In-lab checkoff.

> **Midterm 1 is tomorrow, Tuesday 2 March, 18:00.** This lab is deliberately shorter than Labs 2–4 and is finishable in the
> session. Do not let it collide with your revision.

---

## Purpose

You are given `registry.cpp`. **It compiles clean under `-Wall -Wextra -pedantic` and has five distinct
memory faults.**

Lab 1 had four faults and you fixed them by hand — deep copy constructors, `noexcept` swap, copy-swap
assignment. **This time you will fix them by changing the types**, and the repaired version should have
no `new`, no `delete`, and none of the five special members.

The comparison is the lab. Lab 1's repair was about thirty lines of careful code. This one is about
five.

---

## Part A — Find Them (14 pts)

The faults are ordered so that **fixing one reveals the next.** Work in order and record before you fix.

**A1.** *(3)* Confirm it compiles with no warnings:

```
g++ -std=c++17 -Wall -Wextra -pedantic -c registry.cpp -o /dev/null
```

Then build with `-fsanitize=address` and run. **Report the first error and the line it names.**

**A2.** *(3)* Fix only that fault — a one-line change in `main`. Rerun.

A **different** error appears. Report it, and name the two functions that disagree.

**A3.** *(4)* Fix that one too — again one line. Rerun.

Now you get leaks rather than errors. **Report the total bytes and the number of allocations**, and
account for the byte count: which objects, and which strings inside them?

**A4.** *(4)* Three faults remain and they are all the same kind. Identify each, giving the line and a
one-sentence description:

- one in a destructor;
- one in a member function that removes an element;
- one in a function's **signature**.

**The third is not a missing `delete`.** Say what is actually wrong with it.

---

## Part B — Repair by Retyping (18 pts)

Do not fix these with more `delete` calls. **Fix them by changing what the types say.**

**B1.** *(6)* Make `Session` own its string with a `std::string` instead of `char*`.

**How many of the five special members does `Session` now need?** State the number and the rule.

**B2.** *(6)* Make `Registry` own its sessions with `std::vector<std::unique_ptr<Session>>`, and its
banner with a `std::string`.

`close()` must now actually destroy the session. **Show that it does.**

**B3.** *(6)* Fix `make_orphan`'s signature so the caller cannot fail to handle ownership. Then fix
`find()`.

`find()` is the interesting one: it returns a pointer to something the registry still owns. **What is
the right return type, and why is `unique_ptr` wrong here?**

**The repaired program must contain no `new`, no `delete`, and no user-declared destructor**, and run
clean under `-fsanitize=address,undefined`.

---

## Part C — Compare With Lab 1 (8 pts)

**C1.** *(4)* Count lines. In Lab 1 you repaired `Roster` by writing a deep copy constructor, a
`noexcept` swap and a copy-swap assignment. Here you repaired `Registry` by changing types.

**Report both line counts**, and how many of the five special members each version needed.

**C2.** *(4)* Answer both:

- **(a)** *(2)* The Rule of Zero says to write none of the five. **Which of your two classes obeys it,
  and what made that possible?**
- **(b)** *(2)* Lab 1's `Roster` could have been written this way from the start. **Was Lab 1 therefore
  a waste of time?** Argue your actual view in three sentences.

---

## Submission

- `registry.cpp` — repaired, warning-free, sanitizer-clean, no `new`/`delete`.
- `RESULTS.md` — every transcript from Part A **in order**, plus B and C.
- Machine, OS, compiler version at the top.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 14 | Diagnosing five faults from sanitizer output |
| B | 18 | Repairing by changing ownership types, not by adding `delete` |
| C | 8 | What the Rule of Zero bought, and what Lab 1 was for |
| **Total** | **40** | |

---

## Reference Transcripts

g++ 13.3.0, x86-64 Linux.

**A1 — as provided:**

```
ERROR: AddressSanitizer: heap-use-after-free
    ... in Session::~Session()  registry.cpp:11
```

**A2 — after fixing the double `delete`:**

```
ERROR: AddressSanitizer: alloc-dealloc-mismatch (operator new [] vs operator delete)
```

**A3 — after `delete` → `delete[]`:**

```
Direct leak of 16 byte(s) in 1 object(s)   (x3)
SUMMARY: AddressSanitizer: 65 byte(s) leaked in 6 allocations.
```

**65 = three `Session` objects (16 bytes each) + their strings** — `"ada"` 4, `"grace"` 6,
`"orphan"` 7.

---

## What This Lab Is Really Showing

In **Lab 1** you were given four bugs and you fixed them by writing correct code — a deep copy
constructor, a `noexcept` swap, a copy-swap `operator=`. It worked, it took about thirty lines, and
every one of those lines was a line you could get wrong.

**Here you fixed five bugs by changing three member declarations.**

That is not because you have become a better programmer in four weeks. It is because
`std::string`, `std::vector` and `unique_ptr` are the Lab 1 repair, **written once, by people who got
it right, and reused.** The Rule of Zero is not a style preference — it is the observation that the
careful code has already been written and you should stop rewriting it.

**So why did you do Lab 1 at all?**

Because you now know what those three types are doing. You know `std::string`'s copy constructor
allocates, because you wrote that constructor. You know why `unique_ptr` cannot be copied, because you
watched two owners double-free. You know why `vector`'s move constructor is `noexcept`, because you
know what happens to the strong guarantee if it is not.

**A programmer who is handed the Rule of Zero first learns a rule. A programmer handed it in Week 5
learns a conclusion** — and can tell when it does not apply, which is Week 6's entire assignment.

---

*PROG 102 · Week 5 · Lab 5 · © CSE Department*
