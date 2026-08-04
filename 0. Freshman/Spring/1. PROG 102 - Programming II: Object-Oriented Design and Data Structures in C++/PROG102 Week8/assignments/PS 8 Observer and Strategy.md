# PROG 102 · Problem Set 8
## Observer and Strategy

**Week 8 · Released Friday Week 8 · Due Friday Week 9, 17:00 · 100 points**
**Covers:** Lectures 25–27

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

## Part B — Strategy, Measured (30 pts)

**B1.** *(6)* Implement Strategy the classic way: an interface with at least three concrete
comparison strategies, used to sort a vector.

Add a fourth strategy. **Report the lines changed and the call sites touched.**

**B2.** *(12)* Sort **2,000,000** integers four ways, three runs each:

1. classic Strategy (virtual call);
2. `std::function`;
3. a lambda passed as a template parameter;
4. default `operator<`.

**Write down your predicted ranking before running.** Report the prediction, the times, and whether all
four produced identical output.

**B3.** *(6)* One of those four is much slower than most people expect.

- **(a)** *(3)* Which, and by what factor against the lambda?
- **(b)** *(3)* Explain the mechanism. **Then find Week 3's `qsort` vs `std::sort` figure and state
  both ratios.** Are they close, and why would you expect them to be?

**B4.** *(6)* Give a concrete situation where `std::function` is the **right** choice despite B2.

Be specific about what a template parameter could not do there. **A vague answer about flexibility
earns half.**

---

## Part C — Command (22 pts)

**C1.** *(8)* Implement Command 1994-style — an interface, a concrete command class per action, and a
history with `run` and `undo` — for a text buffer supporting **append** and **erase**.

**C2.** *(8)* Implement the same behaviour with lambdas and `std::function`, with no `Command`
interface and no per-action classes.

**Report non-blank line counts and type counts for both.** They must produce identical output.

**C3.** *(6)* Answer both:

- **(a)** *(3)* Add **redo** to both versions. Which was easier, and what did each need?
- **(b)** *(3)* Give a concrete case where the **1994 version is better.** Lecture 27 §3.4 names the
  category; you supply a specific example.

---

## Part D — The Argument (16 pts)

`ANSWERS.md`. Marked as writing.

**D1.** *(6)* Lecture 27 §3.1 claims: *a design pattern is a workaround for something the language
cannot say.*

**Argue for it in four sentences, using one pattern from this week as evidence.**

**D2.** *(6)* Now argue **against** it. Find a pattern from Weeks 7–8 that would still be needed in a
language with every feature you can think of, and defend it in four sentences.

**Both halves are marked on the quality of the argument, not the position.**

**D3.** *(4)* Pick one pattern from Weeks 7–8 and name a plausible **future** language feature that
could absorb it. One paragraph.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 32 | Observer, and the four things it does not solve |
| B | 30 | Four strategies measured, and the surprising one explained |
| C | 22 | Command, both eras, counted |
| D | 16 | Arguing both sides of the week's claim |
| **Total** | **100** | |

---

## Submission Checklist

1. Clean build; sanitizer-clean except where A1 and A4 deliberately provoke reports.
2. A2's version contains **no `detach`** and no observer that knows its subject.
3. B2 includes your **prediction, recorded before running.**
4. B3 quotes **both** ratios — this week's and Week 3's.
5. C2 reports line and type counts for both versions.
6. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 8 · Problem Set 8 · © CSE Department*
