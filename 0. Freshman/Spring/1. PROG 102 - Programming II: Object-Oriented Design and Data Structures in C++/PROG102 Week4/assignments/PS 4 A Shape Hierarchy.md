# PROG 102 · Problem Set 4
## A Shape Hierarchy

**Released:** Friday 19 February 2027, 10:00 · Week 4 (after Thursday's L15)
**Due:** Friday 26 February 2027, 17:00 · Week 5 — late penalty from 17:01
**Points:** 100 · counts toward the Problem Sets component (30%, lowest one dropped)
**Expected time:** about 4–5 hours

## What this problem set uses

Weeks 0–4: the STL of Week 3, throwing an exception (L04 §4.2), inheritance, `override` (L13), virtual
functions, the vtable, devirtualization (L14), abstract classes, virtual destructors, slicing and the
casts (L15).

**Not needed and not expected:** `unique_ptr` (Week 5 — hold your shapes as `Shape*` and `delete` them),
exceptions beyond throwing one (Week 9). Dumping vtables in GDB is Lab 4's job.

> **Midterm 1 is Tuesday 2 March 2027, 18:00–19:30** (Week 6), covering Weeks 0–4. **Start this set
> early** — the revision guide assumes you have done Parts A and C.

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**Deliverables:** `shapes.hpp`, `shapes.cpp`, `traps.cpp`, `bench.cpp`, `ANSWERS.md`.
Name collaborators and state any generative-tool use.

---

## Part A — The Hierarchy (36 pts)

**A1.** *(12)* An abstract base `Shape` with:

- a `std::string` label, settable at construction, readable via a `const` accessor;
- **pure virtual** `area()`, `perimeter()`, `kind()` and `draw(std::ostream&) const`;
- a **virtual destructor**.

Then `Circle`, `Rectangle` and `Triangle`, each overriding all four with `override`.

Constructors must reject invalid geometry by throwing `std::invalid_argument` — non-positive
dimensions, and for `Triangle` a violation of the triangle inequality.

**A2.** *(6)* A free `operator<<(std::ostream&, const Shape&)` that delegates to `draw`.

**In `ANSWERS.md`, say why `draw` is virtual and `operator<<` is not**, in two sentences. This is the
single most important design question in Part A.

**A3.** *(10)* A `main` holding `std::vector<Shape*>` with at least one of each shape, created with
`new` and **deleted at the end** (Week 5 replaces this with `unique_ptr`).
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

**Everything must be sanitizer-clean — including no leaks.** Paste the transcript.

---

## Part B — The vtable's Size (8 pts)

**B1.** *(8)* Report `sizeof` for: a shape-like class with no virtual functions; the same with one
virtual function; the same with ten; and one of your derived classes.

**Explain the pattern in two sentences**, and say what the first virtual function cost you.

---

## Part C — The Three Traps (32 pts)

**C1.** *(12)* **The virtual destructor.** Build two hierarchies whose derived classes allocate in the
constructor and free in the destructor — one with a virtual base destructor, one without.

`new` a derived object, `delete` through a base pointer, for each. Report:

- which destructors ran;
- what AddressSanitizer says;
- **whether `-Wall -Wextra` warned.**

Then, *(5 of the 12)*: **determine exactly when the warning fires.** Try a base **with** a virtual
function and a base with **none**, and report both. Explain the difference in one sentence.

**C2.** *(10)* **Slicing.** Demonstrate it three ways: a by-value parameter, assignment to a base-typed
variable, and `std::vector<Base>`.

Report the wrong output for each. Then make the base abstract and report **which of the three now fail
to compile** — and which still compiles.

**C3.** *(10)* **Downcasting.** Take a `D2*` held as a `B*`. `static_cast` it to `D1*` and read a
member. Report the value and **explain where that number came from.**

Then `dynamic_cast` the same pointer and report the result.

Finally, write a three-way `dynamic_cast` chain over your shapes, rewrite it as a virtual function, and
**count the lines each version needs when you add a fourth shape.**

---

## Part D — What Dispatch Costs (24 pts)

**D1.** *(12)* Compile a virtual call at `-O2 -S` and look for a `cmp`/`jne` guard before an inlined
body.

**Did your compiler devirtualize?** Now add a second class derived from `Shape` **in the same file**
and recompile. Report whether the guard survived.

**D2.** *(12)* Measure `dynamic_cast` against a plain virtual call over at least 10⁶ objects. Report the
ratio.

Then answer: **Lecture 14 §5 measured a virtual call at around 2× a direct one. Is virtual dispatch
expensive?** Answer in three
sentences, using absolute numbers rather than ratios.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 36 | An abstract hierarchy, `override`, and `operator<<` delegating to a virtual |
| B | 8 | What the vptr costs in space |
| C | 32 | The virtual destructor, slicing, and downcasting |
| D | 24 | Devirtualization and the price of `dynamic_cast` |
| **Total** | **100** | |

**Where the marks actually are:** D2's last question is the one to spend time on — a ratio is not a
cost until you know what it is a ratio of.

---

## Submission Checklist

1. Clean build; sanitizer-clean except where C1 and C3 provoke reports.
2. Every override marked `override`.
3. A4's numbers match to four decimal places.
4. C1 includes the **both-cases** investigation of when the warning fires.
5. A3 frees every shape; the transcript shows no leak.
6. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 4 · Problem Set 4 · © CSE Department*
