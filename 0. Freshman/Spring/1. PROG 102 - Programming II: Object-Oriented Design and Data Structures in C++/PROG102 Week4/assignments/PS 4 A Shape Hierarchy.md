# PROG 102 · Problem Set 4
## A Shape Hierarchy

**Week 4 · Released Friday Week 4 · Due Friday Week 5, 17:00 · 100 points**
**Covers:** Lectures 13–15

> **Midterm 1 is in Week 5**, covering Weeks 0–4. This problem set is due the same week. **Start it
> early** — the revision guide assumes you have done Parts A and D.

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**Deliverables:** `shapes.hpp`, `shapes.cpp`, `traps.cpp`, `bench.cpp`, `ANSWERS.md`.
Name collaborators and state any generative-tool use.

---

## Part A — The Hierarchy (34 pts)

**A1.** *(10)* An abstract base `Shape` with:

- a `std::string` label, settable at construction, readable via a `const` accessor;
- **pure virtual** `area()`, `perimeter()`, `kind()` and `draw(std::ostream&) const`;
- a **virtual destructor**.

Then `Circle`, `Rectangle` and `Triangle`, each overriding all four with `override`.

Constructors must reject invalid geometry by throwing `std::invalid_argument` — non-positive
dimensions, and for `Triangle` a violation of the triangle inequality.

**A2.** *(6)* A free `operator<<(std::ostream&, const Shape&)` that delegates to `draw`.

**In `ANSWERS.md`, say why `draw` is virtual and `operator<<` is not**, in two sentences. This is the
single most important design question in Part A.

**A3.** *(10)* A `main` holding `std::vector<std::unique_ptr<Shape>>` with at least one of each shape.
Print each with its area and perimeter, then report the total area and the largest shape, **using STL
algorithms** (Week 3), not raw loops.

Show a rejected construction.

**A4.** *(8)* Verify against these exact values, at four decimal places:

| Shape | area | perimeter |
| --- | --- | --- |
| `Circle(r=1)` | 3.1416 | 6.2832 |
| `Rectangle(3×4)` | 12.0000 | 14.0000 |
| `Triangle(3,4,5)` | 6.0000 | 12.0000 |
| **total area** | **21.1416** | |

**Everything must be sanitizer-clean.** Paste the transcript.

---

## Part B — The vtable (16 pts)

**B1.** *(6)* Report `sizeof` for: a shape-like class with no virtual functions; the same with one
virtual function; the same with ten; and one of your derived classes.

**Explain the pattern in two sentences**, and say what the first virtual function cost you.

**B2.** *(6)* Under GDB, use `info vtbl` on a `Circle` and a `Rectangle`. Paste both.

**Confirm that slot 0 holds the same *function name* in both**, and say why the slot index is the same.

**B3.** *(4)* Swap the declaration order of two virtual functions **in the base**, rebuild, and dump
the vtables again. **Report what moved.**

---

## Part C — The Three Traps (26 pts)

**C1.** *(10)* **The virtual destructor.** Build two hierarchies whose derived classes allocate in the
constructor and free in the destructor — one with a virtual base destructor, one without.

`new` a derived object, `delete` through a base pointer, for each. Report:

- which destructors ran;
- what AddressSanitizer says;
- **whether `-Wall -Wextra` warned.**

Then, *(4 of the 10)*: **determine exactly when the warning fires.** Try a base **with** a virtual
function and a base with **none**, and report both. Explain the difference in one sentence.

**C2.** *(8)* **Slicing.** Demonstrate it three ways: a by-value parameter, assignment to a base-typed
variable, and `std::vector<Base>`.

Report the wrong output for each. Then make the base abstract and report **which of the three now fail
to compile** — and which still compiles.

**C3.** *(8)* **Downcasting.** Take a `D2*` held as a `B*`. `static_cast` it to `D1*` and read a
member. Report the value and **explain where that number came from.**

Then `dynamic_cast` the same pointer and report the result.

Finally, write a three-way `dynamic_cast` chain over your shapes, rewrite it as a virtual function, and
**count the lines each version needs when you add a fourth shape.**

---

## Part D — What Dispatch Costs (24 pts)

**D1.** *(12)* Measure the cost of virtual dispatch — **and get it right, which takes three attempts.**

Report all three, with times and ratios:

- **(a)** *(3)* `std::vector<std::unique_ptr<Shape>>` against a `std::vector` of a non-virtual class.
- **(b)** *(4)* Both stored **contiguously by value**, dispatching through a base reference.
- **(c)** *(5)* The same, with the non-virtual type **padded to the same `sizeof`** as the virtual one.

**For each, state what it was measuring.** (a) and (b) are not wrong measurements — they are
measurements of something else, and saying what is the point of this question.

Report **at least five runs** of (c) and quote the mean.

**D2.** *(6)* Compile a virtual call at `-O2 -S` and look for a `cmp`/`jne` guard before an inlined
body.

**Did your compiler devirtualize?** Now add a second class derived from `Shape` **in the same file**
and recompile. Report whether the guard survived.

**D3.** *(6)* Measure `dynamic_cast` against a plain virtual call over at least 10⁶ objects. Report the
ratio.

Then answer: **your D1(c) ratio was around 2×. Is virtual dispatch expensive?** Answer in three
sentences, using absolute numbers rather than ratios.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 34 | A correct abstract hierarchy with virtual destructor and validation |
| B | 16 | The vtable, observed rather than described |
| C | 26 | The three traps, each demonstrated |
| D | 24 | Measuring dispatch, including two wrong measurements |
| **Total** | **100** | |

**Where the marks actually are:** D1 is 12 points for producing three numbers, two of which are
"wrong". That is deliberate — the skill being assessed is knowing *what your benchmark measured*, and
it is the skill Lab 2 introduced and Lab 3 sharpened.

---

## Submission Checklist

1. Clean build; sanitizer-clean except where C1 and C3 provoke reports.
2. Every override marked `override`.
3. A4's numbers match to four decimal places.
4. C1 includes the **both-cases** investigation of when the warning fires.
5. D1 reports all three attempts with an interpretation of each.
6. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 4 · Problem Set 4 · © CSE Department*
