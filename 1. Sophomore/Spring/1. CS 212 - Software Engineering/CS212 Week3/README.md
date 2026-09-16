# CS 212 · Software Engineering
## Week 3: Architectural Patterns

**Credits:** 3 · **Prerequisites:** PROG 102, CS 101
**Assessment for this course (overall):** Team Project 40%, Individual Assignments 30%, Midterm 15%, Final 15%
**This week's deliverables:** A 2 due Friday 17:00 · **A 3 released Wednesday** · **📊 Quiz 3 Tuesday** (covers Week 2) · **four ADRs and one architecture test, in the repository**

---

### Why This Week Exists

Because Weeks 1 and 2 both stopped at the same unanswered question, and this is where it gets an answer you may not like.

**Where does the invariant live?** Not the user interface — `curl` ignores it. Not the API layer — it cannot see concurrent requests. Not the domain layer — two processes both check, both pass, both insert, **which is precisely `confirm_booking` on 14 October 2024.** Not an in-process lock — you run four workers.

**The answer is the database**, and the objection people raise — *"business rules don't belong in the database"* — confuses two things. **The domain owns the rule; the database owns the guarantee.** Your `confirm()` still catches the integrity error and raises `AlreadyBooked`; your API still turns that into a 409. What changes is that the guarantee now holds against concurrency, against a migration script, and against somebody at a `psql` prompt.

**The general form is the week's most portable sentence: an invariant must be enforced at the narrowest point every path must pass through.**

**And the week's other half is about deciding at all.** A team that never discusses architecture still has one — it is the accumulated residue of six weeks of locally-cheapest decisions, and it is always the same architecture. **That is `roomsvc`. Nobody chose it.** The difference between a decision and an accident costs about ninety minutes and one file, and this week you write four of those files.

---

### Learning Objectives

By the end of Week 3, you should be able to:

1. Define architecture as **the set of decisions that are expensive to reverse**, and apply the test — *what would changing this cost in March?* — to sort a list of your team's arguments into the half worth having.
2. Say why **you have an architecture whether or not you decide one**, and what the undecided one always looks like.
3. **Rank quality attributes with a sacrifice named**, and say why a ranking with no sacrifice is not a ranking.
4. Write an **ADR** with a context containing a number, a decision specific enough to be violated, **negatives**, and the alternatives with why they lost — and explain why an accepted ADR is never edited.
5. **Place an invariant at the narrowest point every path must pass through**, and say why each of the four wider options fails.
6. State Conway's law, and **name the counter-measure**: rotate ownership by feature slice, not by layer, or the domain belongs to nobody.
7. Give layering's **unstated** rule, and **enforce it with a twelve-line test** that a machine runs.
8. Say where layering always leaks — transactions, N+1, validation — and what to do about each.
9. Explain **ports and adapters**: a port is defined by the inside, in the inside's vocabulary; only the driven side needs inversion; **the test fake is a first-class adapter**.
10. Say what hexagonal architecture **actually** buys — fast tests and a readable domain — and why citing database portability makes reviewers stop believing you.
11. Explain why **MVC is a user-interface pattern**, what its core observer relationship is, why HTTP does not have it, and why *"we use MVC"* answers no architectural question.
12. State the **one** thing microservices buy, itemise the bill, and answer the two questions — *what are you buying and who is the customer; what does being wrong about the boundary cost?*

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L10 What Architecture Is and When It Is Decided]] | Architecture as expensive-to-reverse decisions, with `slot`'s list sorted; **the architecture you get by not deciding**; quality attributes and the honest ranking for a term project; **ADRs — immutable, negatives, alternatives, in git**; **where an invariant lives, and the four homes that fail**; Conway's law and the counter-measure |
| [[L11 Layered Hexagonal and MVC]] | Layering's **unstated** rule and the twelve-line test that enforces it; *reads may skip layers, writes may not*; **the three leaks every layered system has**; ports and adapters, with what it buys **measured** — 1 ms against 1.2 s per module — and what it costs; **MVC as a 1979 UI pattern and the Anemic Domain Model**; the modular monolith, and a decision procedure you can run this week |
| [[L12 Microservices and Event-Driven]] | **The one thing microservices buy**; the bill itemised — the lost transaction, sagas whose compensation is not undo, partial failure, seven logs, eight containers, **and refactoring becoming a migration**; when they are right, and why four of the five reasons are not about code; event-driven and the transactional outbox; **the two questions** |
| [[CS212 Week3/project/ADR TEMPLATE\|ADR TEMPLATE]] | Copy into `docs/adr/`. Four rules for the directory, and why you never edit an accepted one |
| [[CS212 Week3/project/PHASE 1 CHECKPOINT\|PHASE 1 CHECKPOINT]] | Three weeks out. Where you should be, **three questions to ask in this week's meeting**, the two most common Week 3 failures, and what to do first if you are behind |
| [[CS212 Week3/assignments/QUIZ 3 Week 3 Tuesday\|QUIZ 3]] | Seven questions on Week 2, ten minutes, with its own answer key |
| [[CS212 Week3/assignments/A 3 Choose and Defend an Architecture\|A 3]] | Five questions, 100 points, due Friday of Week 4. **Two deliverables go in the repository, not the PDF** |
| [[CS212 Week3/resources/Reading Guide Week 3\|Reading Guide Week 3]] | **Cockburn's six pages before any summary of them**; Fowler's article and Fowler's correction to it; and a warning about how unevidenced this week's literature is |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A rule a machine checks is a rule. A rule in a diagram is a hope.**

Twelve lines of `ast` walking your domain package, asserting that nothing in it imports `fastapi`, `sqlalchemy` or `smtplib`, converts an architectural intention into a property of the codebase. It runs on every push. It cannot be forgotten in a hurry, argued away at 23:00 the night before a demo, or quietly abandoned when the fourth person joins.

**Every architecture diagram you have ever seen was true on the day it was drawn.** What makes `roomsvc` what it is not that anyone drew a bad diagram — it is that nothing checked. Six years of locally-reasonable decisions, each one a little cheaper than the alternative, and no mechanism anywhere that said *no*.

**Add the test this week, while your violation count is still zero.** Adding it in Week 9 means fixing thirty violations first, which means it never gets added — and that sentence is the entire mechanism by which architectures decay.

---

### Assessment Reminder

**Quizzes carry no weight. The project carries 40%.** Quiz *N* covers Week *N−1*, ten minutes at the start of **Tuesday's** lecture in Weeks 1–11, with its own key printed. Tracked in [[_CS 212 Quiz Record]].

**Assignments** released Wednesday 17:00, due Friday 17:00 of the week after; **lowest of thirteen dropped.** A 2 is due this Friday; A 3 is released Wednesday.

> **A 3's ADRs and architecture test are Phase 1 artefacts**, so this assignment is three weeks of
> Phase 1 work done early. **ADRs that live only in the PDF cap the paper at 60** — the point of an
> ADR is that it sits next to the code and can be diffed.

---

### Connections

**Back:** **Week 1 asked where an invariant is enforced and deferred it; Week 2 asked what changes together and deferred the structural answer.** This week answers both. **W2 L07 §5's Parnas criterion** is L10's definition of architecture in its 1972 form, and **W2 L08 §5's dependency inversion** is L11's hexagon with the picture removed.

**Sideways:** **CS 202's Week 3 is concurrency and locks** — the same problem this week solves with a constraint, solved there with mutual exclusion in one address space. The two courses are converging on one sentence: **make the check and the act indivisible, at the narrowest point both must pass through.** **MATH 251's Week 3** is the conditional probability that Week 6's mutation scores are interpreted with.

**Forward:** **Week 4** names the patterns that resolve several of this week's conflicts — including the one that fixes the notification-inside-the-transaction bug. **Week 5** writes the concurrency test that proves your placement was right. **Week 6's Phase 1 viva asks what shape you chose and why**, and marks the reasoning rather than the shape. **Week 8** is where the architecture test earns its keep in a pipeline, and **Week 10** is Liskov's substitution rule applied to an API that other people depend on.

---

*CS 212 · Week 3 · © CSE Department*
