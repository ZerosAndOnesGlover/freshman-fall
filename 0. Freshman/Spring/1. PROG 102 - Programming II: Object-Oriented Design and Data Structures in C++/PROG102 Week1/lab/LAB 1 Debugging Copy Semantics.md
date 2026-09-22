# PROG 102 · Lab 1
## Debugging Copy Semantics

**Date:** Monday 1 February 2027 · 15:00–16:50 · Lab section (Week 2) — covers Week 1 (L04–L06)
*2-hour lab · 40 points · in-lab checkoff · part of the Labs component (20%)*
**Deliverable:** `roster.hpp` (repaired), `RESULTS.md`. In-lab checkoff by your TA.

---

## Purpose

You are given `roster.hpp`. **It compiles without a single warning under `-Wall -Wextra -pedantic`,
and it is wrong in four distinct ways.**

That sentence is the lab. Week 0 established that a clean build is not a correct program; this session
makes you feel it. Your tools for the next two hours are AddressSanitizer and reading the code, and
the bugs are arranged so that **fixing one reveals the next** — which is exactly how real debugging
goes.

---

## The Code

```cpp
// roster.hpp -- PROVIDED
#pragma once
#include <cstring>
#include <cstdio>

class Roster {
    char** names;      // array of owned C-strings
    int    count;
    int    cap;
public:
    explicit Roster(int capacity)
        : names(new char*[capacity]), count(0), cap(capacity) {}

    ~Roster() { delete names; }

    void add(const char* n) {
        names[count] = new char[std::strlen(n) + 1];
        std::strcpy(names[count], n);
        ++count;
    }
    const char* at(int i) const { return names[i]; }
    int size() const { return count; }
};
```

**Confirm before you start** that this compiles silently:

```
g++ -std=c++17 -Wall -Wextra -pedantic -c roster_demo.cpp -o /dev/null
```

---

## Part A — Diagnose (14 pts)

Work in order. **Do not fix anything until Part B** — record first.

**A1.** *(3)* Build and run this under `-fsanitize=address`:

```cpp
Roster r(2);
r.add("ada"); r.add("grace");
std::printf("%s %s\n", r.at(0), r.at(1));
```

Report the error. **Name the two functions that disagree**, and state the rule they violate.

**A2.** *(3)* Fix **only** that one bug — a one-word change — and rerun.

A **different** report appears. Quote it, including the byte count and the number of allocations.
**Account for the exact number of bytes.**

**A3.** *(4)* Now add a third name to a roster constructed with capacity 2. Report the error and the
line it names.

**In one sentence, say what the constructor promised and what `add` failed to check.**

**A4.** *(4)* Finally, copy a roster and print the address of element 0 from each:

```cpp
Roster a(2); a.add("ada");
Roster b = a;
std::fprintf(stderr, "a=%p b=%p same=%s\n",
    (void*)a.at(0), (void*)b.at(0), a.at(0)==b.at(0) ? "YES" : "no");
```

Report the addresses, whether they are equal, and the sanitizer's verdict at exit.

**Which two functions are missing?** Name them precisely, with signatures.

---

## Part B — Repair (14 pts)

**B1.** *(4)* Fix the deallocation bug **and** the leak. The destructor must release both the array
**and** every string in it.

**B2.** *(3)* Make `add` grow the roster when it is full, doubling the capacity. Do not use `realloc`.

**B3.** *(7)* Add a **deep-copying** copy constructor and a copy assignment operator.

Write the assignment operator using **copy-swap**: a `noexcept` `swap` member, and
`operator=` taking its parameter **by value**.

Your class must contain **no `this == &other` comparison.**

**Verify all four original faults are gone:** rerun A1, A3 and A4, and additionally run `a = a`. All
four must be sanitizer-clean.

---

## Part C — Count the Copies (8 pts)

**C1.** *(5)* Add counters to `Roster` for constructor, copy constructor, assignment and destructor
calls. Report the counts for each of:

```cpp
Roster a(4); a.add("ada");
Roster b = a;                         // (i)
Roster c(4); c = a;                   // (ii)
void show(Roster r);      show(a);    // (iii)
void show2(const Roster& r); show2(a);// (iv)
```

**C2.** *(3)* Rows (iii) and (iv) differ. **State the difference in copies, and what it would cost** if
`Roster` held ten thousand names instead of one.

---

## Part D — What the Tools Did (4 pts)

**D1.** *(2)* You found four bugs. **How many did `-Wall -Wextra -pedantic` report?**

Now compile the **original** `roster.hpp` with `-Weffc++` and report what it says.

**D2.** *(2)* Answer in two sentences: given D1, **what is a clean `-Wall -Wextra` build actually
evidence of?** Be precise — the answer is not "nothing".

---

## Submission

- `roster.hpp` — repaired, warning-free, sanitizer-clean, no self-assignment guard.
- `RESULTS.md` — every transcript from Part A in order, the Part C table, and D1/D2.
- Your machine, OS and compiler version at the top.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 14 | Diagnosing four distinct faults from sanitizer output |
| B | 14 | Rule of Three via copy-swap, all faults cleared |
| C | 8 | Copy counting, and the cost of pass-by-value |
| D | 4 | What the warning flags did and did not catch |
| **Total** | **40** | |

---

## Reference Transcripts

g++ 13.3.0, x86-64 Linux.

**A1 — as provided:**

```
ERROR: AddressSanitizer: alloc-dealloc-mismatch (operator new [] vs operator delete)
```

**A2 — after `delete` → `delete[]`:**

```
Direct leak of 6 byte(s) in 1 object(s)
Direct leak of 4 byte(s) in 1 object(s)
SUMMARY: AddressSanitizer: 10 byte(s) leaked in 2 allocation(s).
```

10 bytes = `"grace"` (6) + `"ada"` (4), including terminators.

**A3 — third name into capacity 2:**

```
ERROR: AddressSanitizer: heap-buffer-overflow
WRITE of size 8 at 0x...
    in Roster::add(char const*)  roster.hpp:17
```

**A4 — copying:**

```
a=0x502000000030  b=0x502000000030  same=YES
ERROR: AddressSanitizer: attempting double-free
```

---

## What This Lab Is Really Showing

The four bugs are not four unrelated mistakes. **Three of them are the same mistake**, which is that
`Roster` owns something and does not say so:

- the destructor releases the array but not what the array points at;
- there is no copy constructor, so two rosters own one set of strings;
- there is no copy assignment, for the same reason.

**Only the missing bounds check is a separate error**, and it is the one a C programmer would have
caught, because it is the kind of bug PROG 101 trained you to look for.

That is the shape of the transition this course is about. The bugs you are now vulnerable to are not
about arithmetic or pointers — you are already good at those. They are about **ownership**: who is
responsible for releasing a resource, and what happens when that responsibility is silently
duplicated by a function you did not write.

Week 5 removes this whole category by making ownership a property of the *type* — `unique_ptr` cannot
be copied, so the bug becomes a compile error. Until then, the Rule of Three is what stands between
you and this transcript.

---

*PROG 102 · Week 1 · Lab 1 · © CSE Department*
