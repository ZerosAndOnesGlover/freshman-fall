# CS 212 · Software Engineering
## Week 9: Refactoring

**Credits:** 3 · **Prerequisites:** PROG 102, CS 101
**Assessment for this course (overall):** Team Project 40%, Individual Assignments 30%, Midterm 15%, Final 15%
**This week's deliverables:** A 8 due Friday 3 April 17:00 · **A 9 released Wednesday** · **📊 Quiz 9 Tuesday** (covers Week 8)

---

### Why This Week Exists

Because this is where the bug gets removed.

```sql
CREATE UNIQUE INDEX one_confirmed_per_slot
  ON bookings (room, slot)
  WHERE state = 'confirmed';
```

**Twelve insertions, one of them DDL.** Detected 14 October 2024 by two lecturers standing in VNC 101; diagnosed 6 November — **23 days**; shipped 11 March 2025 — **four months.** The engineering work, once somebody was confident, was **an afternoon.**

**The four months were not engineering.** They were 487 lines, eleven tests against ninety-four independent paths, and an author who left in 2023. **Nobody could convince themselves that touching the function was safe** — and every week of this course has been one answer to that sentence.

**Which is also the week's central and least comfortable fact.** Refactoring is safe *because tests tell you when you broke something*, so **`confirm_booking` cannot be refactored safely at all.** Feathers' definition is the honest one — *"legacy code is code without tests"* — and it produces a deadlock: to refactor you need tests, to write tests you need seams, to make seams you must refactor. **The way out is the characterisation test**, which asserts not what the code *should* do but what it *does*, and which is the most useful technique in the week.

---

### Learning Objectives

By the end of Week 9, you should be able to:

1. State Fowler's definition and apply the operational test — **if a test had to change, it was not a refactoring** — and name three things people wrongly call refactoring.
2. Explain why **refactoring requires tests and is therefore often impossible**, and why *"legacy code is code without tests"* is operationally exact.
3. **Write a characterisation test by the procedure**: wrong assertion, read the failure, paste the value, **and comment that it records rather than endorses.**
4. Use **coverage over characterisation tests as a checklist** for what you have not pinned.
5. Wear **one hat at a time**, and say why that makes a red test diagnosable in one step.
6. Refactor **opportunistically** — rule of three, **preparatory** (*make the change easy, then make the easy change*), comprehension, litter-pickup — and say why a refactoring fortnight is usually a mistake.
7. Name the **four cases where refactoring is dangerous**, including the extract-method that moves an `INSERT` out of its critical section.
8. Treat a smell as a **cheap fallible signal**, and run the three steps — notice, ask what it indicates *here*, decide whether now.
9. Identify the **nine smells that account for `roomsvc`**, and say why **Divergent Change is the most serious and invisible to every linter**, and **Speculative Generality the easiest to fix and hardest to agree to.**
10. Show that **Long Function is a symptom**, and apply **Split Phase** — decide, act, announce — so that a notification failure cannot roll back a booking.
11. Plan a **branch by abstraction** in six steps, including the step everybody forgets, and say where teams stall.
12. Describe the **strangler fig** and say why **the data is the hard part** — and why a rewrite throws away every bug you ever fixed.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L28 What Refactoring Is and Is Not]] | The definition, and **the test: if a test had to change, it was not a refactoring**; why refactoring requires tests and so is often impossible; **characterisation tests, by procedure**, with coverage as a checklist; **the two hats**, and how they map to your commits; four triggers, and why a refactoring sprint is usually wrong; **four dangerous cases, including the extract-method that recreates VNC 101** |
| [[L29 The Smell Catalogue Applied]] | A smell as a cheap fallible signal — **the same shape as coverage and linter findings, three weeks running**; **the nine smells that account for `roomsvc`**, with the two that get mis-ranked; **Long Function as a symptom, and Split Phase as the answer**; **the fix — twelve insertions, four months, an afternoon** — and the table of what eight weeks of this course supplied to make the afternoon possible |
| [[L30 Large Refactorings]] | Why the branch-or-one-huge-commit choice is false; **branch by abstraction in six steps**, with the creative step, the stalling step and the step everybody forgets; **the strangler fig, and the data problem stated honestly**; **parallel run** as W6's oracle moved into production; and why a rewrite loses |
| [[CS212 Week9/resources/SMELL CATALOGUE\|SMELL CATALOGUE]] | **Print it.** All twenty-four, the nine that matter here, where each lives in `roomsvc`, and the pre-refactoring checklist |
| [[CS212 Week9/assignments/QUIZ 9 Week 9 Tuesday\|QUIZ 9]] | Seven questions on Week 8, ten minutes, with its own answer key |
| [[CS212 Week9/assignments/A 9 Refactor a Fowler Smell in Real Code\|A 9]] | **On `roomsvc`, not `slot`.** Five questions, 100 points, due Friday 10 April. **Three automatic caps** |
| [[CS212 Week9/resources/Reading Guide Week 9\|Reading Guide Week 9]] | **Type Chapter 1**; why the JavaScript edition does not matter, and the one place the language genuinely does; and why Feathers Ch. 13 pays most this week |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Eight weeks to make an afternoon possible.**

Look at what each week supplied, in order. **Week 1** wrote the invariant down, so there was something to enforce. **Week 2** separated the rule from the email and the VAT, so the change is local. **Week 3** decided where an invariant belongs — the narrowest point every path must pass through. **Week 5** wrote the concurrency test that fails before the fix and passes after. **Week 6** produced the mutant proving the old suite would have shipped it. **Week 7** put a second reader on it, so the author is not alone. **Week 8** made the migration a separate, verified pipeline step. **Week 9** supplied the characterisation tests and Split Phase that make the change safe.

**Eight weeks of apparatus for twelve lines of code.**

**That ratio is not a failure of the course. It is the bill for W0 L01 §4** — roughly 60% of a system's lifetime cost falls after first release, and only about a fifth of that is fixing bugs. **What you are buying, all term, is not correctness. It is the ability to change code you do not fully understand, safely, in an afternoon** — and `roomsvc` is what it costs when nobody bought it.

---

### Assessment Reminder

**Quizzes carry no weight. The project carries 40%.** Quiz *N* covers Week *N−1*, ten minutes at the start of **Tuesday's** lecture in Weeks 1–11, with its own key printed. Tracked in [[_CS 212 Quiz Record]].

**Assignments** released Wednesday 17:00, due Friday 17:00 of the week after; **lowest of thirteen dropped.** A 8 is due this Friday. A 9 is released Wednesday.

> **A 9's three caps all enforce the definition.** **Any of `roomsvc`'s 212 tests failing → 45**,
> because a change that alters behaviour is not a refactoring. **Fewer than three commits → 60**,
> because refactoring is the easiest work in the world to commit incrementally. **An out-of-bounds
> target → 55** — `confirm_booking`'s Split Phase is done for you in L29 §3, the pricing tree was A 2,
> and the `Slot` object was probably A 4. **Find your own.**

---

### Connections

**Back:** **Week 2's question — what changes together? — is what Split Phase splits along**, and the line count falls out as a consequence rather than a target. **W3's placement decision** is what the migration finally implements. **W5's concurrency test** is what makes the fix verifiable, and **W6's mutant** is what proves the old suite would not have. **W8's fast pipeline** is the precondition: a team at eight minutes stops running the suite during a refactoring, which is exactly when it is needed.

**Sideways:** **CS 202's Week 9 is device drivers**, and its Project 2 is assigned this week — worth knowing before you plan A 9's evening. **MATH 251's Midterm 2 is Monday of Week 10**, so this week's Friday is heavier than it looks.

**Forward:** **Week 10 is where "observable behaviour" stops meaning your tests and starts meaning other people's code** — renaming a private method is a refactoring, renaming an API field is a breaking change — and **L26 §7's expand-and-contract returns as a versioning strategy.** **Week 11** measures hotspots properly, which L30 §6 previews in one command, and asks you to prioritise a debt register. **Week 12's retrospective** asks what your refactoring practice changed.

---

*CS 212 · Week 9 · © CSE Department*
