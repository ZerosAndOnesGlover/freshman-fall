# PROG 102 · Problem Set 8
## Observer and Strategy

**Released:** Friday 19 March 2027, 10:00 · Week 8 (after Thursday's L27)
**Due:** Friday 26 March 2027, 17:00 · Week 9 — late penalty from 17:01
**Points:** 100 · counts toward the Problem Sets component (30%, lowest one dropped)
**Expected time:** about 3–4 hours — kept short because Project 1 is due the same day

## What this problem set uses

Weeks 0–8: `shared_ptr`/`weak_ptr` (Week 5), throwing (L04 §4.2), and this week — Observer and its
`weak_ptr` form (L25), lambdas with capture and `std::function` as far as Lecture 25 §4's box takes
them, Strategy, Command and Template Method (L26), State, MVC and the "obsoleted" argument (L27).

**Not needed and not expected:** exception guarantees (Week 9), how `std::function` works inside
(Week 11). Timing the four Strategy forms is Lecture 26 §3's measurement, not repeated here.

> **Project 1 is due the same day as this problem set.** That is deliberate — this set is short, and
> **Project 1 is worth more.** Do this one second.

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**Deliverables:** `observer.cpp`, `strategy.cpp`, `command.cpp`, `ANSWERS.md`.
Name collaborators and state any generative-tool use.

---

## Part A — Observer (32 pts)

**A1.** *(6)* Implement the naive Observer: a subject holding `std::vector<Observer*>`, and at least
two concrete observers.

Then **break it**: register an observer that goes out of scope before the subject notifies.

**Paste the sanitizer report** and name the line and the function.

**A2.** *(10)* Rewrite it with `std::weak_ptr<Observer>`.

Requirements: dead observers are **skipped**, and the list is **pruned** during notification. Nobody
calls `detach`.

Demonstrate: two observers, one dies, notification happens. **Report the registered count before the
death, after the death, and after the next notification.**

**A3.** *(6)* The count after the death and before the next notification is **stale**.

- **(a)** *(3)* Explain why in two sentences.
- **(b)** *(3)* Write a `live_count()` that is accurate, and give a situation where the difference
  matters.

**A4.** *(10)* Break it three more ways. For each: demonstrate, report what happens, and **do not fix
it**.

- **(a)** *(4)* **Re-entrancy** — an observer that attaches another observer from inside `notify`.
  Run under `-fsanitize=address`.
- **(b)** *(3)* **An observer that throws** from `notify`. Report which observers were notified and
  which were not.
- **(c)** *(3)* **Ordering** — construct a case where the result depends on registration order.

*(Week 9 fixes (b). The others are yours to think about.)*

---

## Part B — Strategy (16 pts)

**B1.** *(8)* Implement Strategy the classic way: an interface with at least three concrete
comparison strategies, used to sort a vector.

Add a fourth strategy. **Report the lines changed and the call sites touched.**

**B2.** *(8)* Lecture 26 §3 measured `std::function` as the slowest of four ways to pass a comparison.
Give a concrete situation where it is nevertheless the **right** choice.

Be specific about what a template parameter could not do there. **A vague answer about flexibility
earns half.**

---

## Part C — Command (30 pts)

**C1.** *(10)* Implement Command 1994-style — an interface, a concrete command class per action, and a
history with `run` and `undo` — for a text buffer supporting **append** and **erase**.

**C2.** *(10)* Implement the same behaviour with lambdas and `std::function`, with no `Command`
interface and no per-action classes.

**Report non-blank line counts and type counts for both.** They must produce identical output.

**C3.** *(10)* Answer both:

- **(a)** *(5)* Add **redo** to both versions. Which was easier, and what did each need?
- **(b)** *(5)* Give a concrete case where the **1994 version is better.** Lecture 27 §3.4 names the
  category; you supply a specific example.

---

## Part D — The Argument (22 pts)

`ANSWERS.md`. Marked as writing.

**D1.** *(8)* Lecture 27 §3.1 claims: *a design pattern is a workaround for something the language
cannot say.*

**Argue for it in four sentences, using one pattern from this week as evidence.**

**D2.** *(8)* Now argue **against** it. Find a pattern from Weeks 7–8 that would still be needed in a
language with every feature you can think of, and defend it in four sentences.

**Both halves are marked on the quality of the argument, not the position.**

**D3.** *(6)* Pick one pattern from Weeks 7–8 and name a plausible **future** language feature that
could absorb it. One paragraph.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 32 | Observer, and the four things it does not solve |
| B | 16 | Strategy, and when `std::function` is right |
| C | 30 | Command, both eras, counted |
| D | 22 | Arguing both sides of the week's claim |
| **Total** | **100** | |

---

## Submission Checklist

1. Clean build; sanitizer-clean except where A1 and A4 deliberately provoke reports.
2. A2's version contains **no `detach`** and no observer that knows its subject.
3. C2 reports line and type counts for both versions.
4. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 8 · Problem Set 8 · © CSE Department*
