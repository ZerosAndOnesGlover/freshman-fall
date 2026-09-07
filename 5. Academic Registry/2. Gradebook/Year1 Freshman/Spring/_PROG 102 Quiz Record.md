# PROG 102 · Quiz Record
## Not part of the course grade

> **This file is deliberately outside the gradebook's weighted components.** Quizzes carry **0%
> weight** — the curriculum's assessment line (*Labs 20%, Problem Sets 30%, Midterms 25%, Final 15%,
> Projects 10%*) sums to 100% without them.
>
> The leading underscore in the filename keeps this file out of `tools/gpa.py`'s course scan. Do not
> rename it without checking `collect()` in that script.

---

## Why This Is a Separate File

The same reason it is separate in CS 102, and the failure was found there first: the gradebook parser
reads a component's items from its heading until the **next `##` heading containing a percentage**.
An unweighted subheading has none, so its rows are silently absorbed into the component above it.

In CS 102 that quietly attached eleven quiz rows to Project 2. No computed grade changed, because
every row was blank — **it would have** the moment anyone entered a mark.

The schema does support an explicit `## Quizzes — formative, 0% weight` heading, which parses
correctly because the qualifier contains a `%`. **This file exists anyway**, because the vault's
convention is that unweighted records live outside the gradebook, and because a convention that
removes a failure mode is better than one that depends on remembering to write `0%`.

---

## Note the Difference From CS 102

In CS 102, **both** labs and quizzes were unweighted and lived in a record like this one, with labs
under a 10-of-13 completion gate.

**PROG 102 weights labs at 20%.** They are a graded component and they are in [[PROG 102]] with
everything else. Only quizzes are here. There is no lab gate in this course — a missed lab costs you
marks directly, which is a sharper instrument than a gate and needs no separate rule.

---

## Quizzes

**15 minutes at the start of Monday's lecture, Weeks 1–11.** Marked out of 20.

**Quiz *N* covers Week *N−1*** — the convention used in CS 101 and CS 102. A quiz is never a surprise:
it covers the week you have just finished and whose problem set you have already started.

| Quiz | Held | Covers | Topic | Possible | Earned |
|---|---|---|---|---|---|
| Quiz 1 | Week 1 | Week 0 | C to C++: classes and objects | 20 | |
| Quiz 2 | Week 2 | Week 1 | Operator overloading and copy semantics | 20 | |
| Quiz 3 | Week 3 | Week 2 | Templates and generic programming | 20 | |
| Quiz 4 | Week 4 | Week 3 | The Standard Template Library | 20 | |
| Quiz 5 | Week 5 | Week 4 | Inheritance and polymorphism | 20 | |
| Quiz 6 | Week 6 | Week 5 | Memory management and RAII | 20 | |
| Quiz 7 | Week 7 | Week 6 | Linked lists, trees and custom iterators | 20 | |
| Quiz 8 | Week 8 | Week 7 | Creational and structural patterns | 20 | |
| Quiz 9 | Week 9 | Week 8 | Behavioral patterns | 20 | |
| Quiz 10 | Week 10 | Week 9 | Exception handling and exception safety | 20 | |
| Quiz 11 | Week 11 | Week 10 | Concurrency: threads and synchronisation | 20 | |

---

## What Is Never Quizzed

**Week 11 and Week 12 have no quiz covering them.** Quiz 11 is the last one, and it covers Week 10.

This is a consequence of the schedule, not an accident, but it is worth stating plainly because
students infer the opposite: *nothing quizzed means nothing examined.* **Week 11 (lambdas,
`std::function`, `constexpr`, structured bindings) and Week 12 (testing, profiling, cache behaviour)
are both on the comprehensive final**, and Week 12's material is the part of the course that most
directly informs Project 2.

The absence of a quiz in the last fortnight is because the last fortnight is full — Project 2, the
final, and Lab 12's demo all land there.

---

## Why Quizzes Exist At All

C++ is a large language, and the failure mode is not misunderstanding a single idea. It is quietly
never having understood **references** — and finding that out in Week 5, when `unique_ptr` and
`std::move` stop making sense and the reason is three months old.

A 15-minute Monday quiz surfaces that in Week 2, when it costs an office-hour visit instead of a
midterm. **That is the whole design intent**, and it is why the quizzes are marked and returned the
same week rather than being merely collected.

---

*PROG 102 · Quiz Record · © CSE Department*
