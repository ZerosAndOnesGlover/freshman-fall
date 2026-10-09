# CS 212 · Software Engineering
## Week 3 · Lecture 1 of 3
### What Architecture Is, and When It Is Decided

*“The essence of a software entity is a construct of interlocking concepts: data sets, relationships among data items, algorithms, and invocations of functions.”* — Fred Brooks, "No Silver Bullet" (1986)

---

**Sat:** Tuesday of Week 3, 10:00–10:50, TH 200 · **⚠️ Quiz 3 in the first ten minutes** — covers Week 2 · **Reading:** Sommerville Ch. 6 §6.1–6.2 · **Next:** L11, layered and hexagonal

**Coursework:** 📊 **Quiz 3** today · 📝 **Assignment 3** released Wed this week 17:00, due Fri of Week 4 17:00 · 📝 **Assignment 2** due Fri this week 17:00

---

## 1. The Definition That Is Actually Useful

There are many definitions. The one worth carrying:

> **Architecture is the set of decisions that are expensive to reverse.**
> — Fowler, after Booch: *"the shared understanding… the decisions you wish you could get right
> early because they are perceived as hard to change"*

**The definition is operational**, which is what makes it better than "the high-level structure of a system". It gives you a test you can apply to any decision in front of you:

> **If we were wrong about this, what would it cost to change in March?**

An answer measured in hours is not architecture; it is a detail, and you should stop discussing it and go and write it. An answer measured in weeks is architecture, **and it deserves a written record of why** — which is §5.

**Apply it to `slot` right now:**

| Decision | Cost of reversal in March | Architecture? |
|---|---|---|
| Whether `Slot` is a fixed 50-minute value or an interval | **Schema, every query, the unique index, the domain model** | **Yes** |
| Whether a booking belongs to a person or a course | **Every foreign key and most queries** | **Yes** |
| Whether the domain imports SQLAlchemy | **Every test and every file in the domain** | **Yes** |
| Which HTTP framework | A week of mechanical work | Borderline |
| Whether the week view is a table or a grid of divs | An afternoon | **No — stop arguing about it** |
| Function and variable names | Minutes, with a refactoring tool | **No** |

**Most of what teams argue about in Week 3 is in the bottom half of that table.** The skill is noticing which half you are in.

---

## 2. Architecture Is Decided Whether or Not You Decide It

**The most important sentence in this lecture.**

A team that never discusses architecture still has one. It is the accumulated consequence of the first six weeks of decisions made under time pressure by whoever happened to be typing — and it is almost always the same architecture: **everything in the route handlers, SQL wherever it was convenient, business rules distributed across the layer that happened to need them.**

**That is `roomsvc`.** Nobody chose it. There is no document, no diagram, no ADR. The architecture is *"whatever `confirm_booking` does"*, and it emerged from five people over six years each making the locally cheapest decision.

> **Gall's law, and it is worth keeping:** *a complex system that works is invariably found to have
> evolved from a simple system that worked.* **This is true and it is not a licence.** `roomsvc`
> evolved from a simple system that worked, and it arrived where it is because **nobody ever spent
> an hour writing down which decisions were load-bearing.** Evolution needs a direction.

**The practical consequence for your team:** you will make these decisions in the next fortnight whether you talk about them or not. **The only choice is whether they are decisions or accidents**, and the difference costs about ninety minutes and one file per decision.

---

## 3. Quality Attributes Are What Architecture Trades Between

Architecture is not chosen for correctness — any architecture can be correct. **It is chosen to favour some qualities over others**, and the qualities conflict.

| Quality | What it asks | What it costs |
|---|---|---|
| **Modifiability** | Can a change be made in one place? | Indirection; more files; slower to read |
| **Testability** | Can a part be exercised alone, fast? | Seams, abstractions, dependency inversion |
| **Performance** | Latency, throughput | **Almost always fights modifiability** — layers cost hops, abstraction costs allocation |
| **Availability** | Does it stay up when a part fails? | Redundancy, retries, and a great deal of complexity |
| **Scalability** | Does it survive 100× load? | Statelessness, partitioning, and giving up transactions |
| **Security** | Can the boundary be trusted? | Choke points, which are exactly what "flexible" architectures lack |
| **Deployability** | How often, and how safely, can you ship? | Automation, and a Week 8 pipeline |

**Name yours, in order, before you choose a shape.** For `slot`, the honest ranking for a five-person term project is roughly: **testability → modifiability → deployability → security → performance → availability → scalability.** Your users number in the dozens, your data in the thousands of rows, and your marks come from engineering quality rather than throughput.

> **A team that ranks scalability first will build the wrong system and be marked down for it**,
> and this happens most years. The viva question is: *what in your requirements made scalability
> matter?* **There is no honest answer available**, because the department has 34 rooms.

---

## 4. The Shapes, Briefly

Detail in L11 and L12; the map first.

| Shape | One sentence | Favours | Costs |
|---|---|---|---|
| **Layered** | Each layer may call the one below | Modifiability, comprehensibility | Hops; and layers leak under pressure |
| **Hexagonal / ports-and-adapters** | The domain is in the middle and knows nothing outside it | **Testability**, modifiability | Ceremony; a mapping layer people resent |
| **MVC** | Separate presentation, logic and data for a *user interface* | UI modifiability | Says nothing about the rest, and is constantly over-claimed |
| **Modular monolith** | One deployable, strong internal module boundaries | Deployability, simplicity, testability | Boundaries are only as strong as your discipline |
| **Microservices** | Many independently deployable services | Independent deployment, team autonomy | **Distributed systems problems, all of them** |
| **Event-driven** | Components communicate by publishing facts | Decoupling in time, extensibility | You lose the ability to follow the control flow by reading |

**For `slot`, the defensible answers are the middle two**, and a team choosing either can argue it well. **A team choosing microservices will be asked what it bought**, and the syllabus warns them (§7.5).

---

## 5. Architecture Decision Records

Nygard (2011), *"Documenting Architecture Decisions"* — the whole idea is one page, and it is the most useful process artefact in this course.

**The problem it solves:** in March somebody asks *"why is the domain layer not allowed to import SQLAlchemy?"* and the four people who agreed it in January remember four different reasons. **Meanwhile the one person who disagreed has left the team, and the argument against — which was good — is gone entirely.**

**An ADR is a short markdown file, in the repository, numbered, immutable.**

```markdown
# 0003. The domain layer does not import the ORM

Date: 2026-02-11
Status: accepted

## Context

Our test suite currently needs a Postgres container, which takes 9 s to start
and 1.2 s per test module. We expect ~200 tests by May. We also want to be
able to state the booking rules in one file that a non-author can read.

## Decision

`slot.domain` imports nothing from `sqlalchemy`, `fastapi`, or any client
library. Persistence is reached through a `BookingRepo` protocol defined in
the domain and implemented in `slot.infra`.

## Consequences

+ Domain tests run with no container: 0.8 ms per test measured on the spike.
+ The booking rules are readable in one file.
− One more indirection: answering "what SQL runs when we confirm?" now needs
  two files.
− A mapping between ORM rows and domain objects, which is ~40 lines of tedium
  and a place for bugs.
− We accept that we will NOT get database portability from this, and that is
  not why we are doing it.

## Alternatives considered

- **Domain objects are ORM models.** Simpler, one fewer layer, and the one
  the team's previous project used. Rejected because every domain test then
  needs a database, and we measured that at 1.2 s per module.
- **Repository over an in-memory fake only in tests.** Same benefit, but the
  fake drifts from the real one; we have seen this.
```

**Four things make it work, and every one of them is regularly dropped:**

1. **Immutable.** You never edit an accepted ADR. You write a new one that **supersedes** it, and mark the old one `superseded by 0011`. **The record of having changed your mind is the most valuable part** — Week 11 and the final report both ask for it.
2. **Consequences include the negatives.** An ADR with only upsides is marketing. The minus lines above are what makes it useful in March.
3. **Alternatives considered, with why they lost.** This is the part that answers the March question, and the part teams skip.
4. **In the repository, in git, next to the code.** Not in a wiki nobody has access to, and not in a document that cannot be diffed.

> **Phase 1 requires at least four ADRs.** Not because four is a magic number, but because a team
> that has made fewer than four expensive-to-reverse decisions by Week 6 has not started.
> **Write them as you decide, not the night before** — an ADR reconstructed from memory loses
> exactly the thing it exists to preserve, which is the alternative you rejected.

---

## 6. Where an Invariant Lives

The question Weeks 1 and 2 kept deferring. **It has an answer, and the answer annoys people.**

**The candidates**, for *"a resource has at most one confirmed booking per slot"*:

| Where | Does it hold? |
|---|---|
| **The user interface** — grey out taken slots | **No.** It is a convenience. `curl` ignores it |
| **The API layer** — validate the request | **No.** It cannot see concurrent requests |
| **The domain layer** — `confirm()` checks for conflicts | **No.** Two processes both check, both pass, both insert. **This is exactly `confirm_booking`** |
| **A lock** — application-level mutex | **Only within one process.** With four workers, no. With a distributed lock, yes — and now you own a distributed lock |
| **The database** — partial unique index | **Yes.** Across processes, across machines, against direct writes, against a migration script, forever |

**The answer is the database, and this is not a defeat for your architecture.**

The objection people raise — *"business rules should not be in the database"* — conflates two different things. **The rule is stated in the domain; it is enforced by the only component that can enforce it.** Your `confirm()` still catches the `IntegrityError` and turns it into a domain-level `AlreadyBooked`, and the API turns that into a 409. **The domain owns the rule. The database owns the guarantee.**

```python
# domain
def confirm(hold_id: UUID, repo: BookingRepo) -> Booking:
    try:
        return repo.confirm(hold_id)
    except UniqueViolation:            # infra translates the DB error
        raise AlreadyBooked(hold_id)   # domain vocabulary
```

> **The general rule, and it is worth more than the example:** **an invariant must be enforced at
> the narrowest point every path must pass through.** For uniqueness under concurrency, that is
> the database. For a state transition that no concurrent process can race, the domain layer is
> narrow enough. **For anything the user interface enforces, the answer is nowhere.**

**Two of `slot`'s five invariants belong in the database and three in the domain**, and A 3 asks you to work out which and defend it.

---

## 7. Conway's Law, and Why It Is Not a Joke

Melvin Conway, 1968 — the same year as Garmisch:

> *"Organizations which design systems… are constrained to produce designs which are copies of the
> communication structures of these organizations."*

**It has held up.** The mechanism is not mysterious: an interface between two modules requires an agreement between the people who own them, and agreements are expensive in proportion to organisational distance. **So the cheap interfaces are the ones inside a team, and modules drift to match teams.**

**Two consequences you will actually experience:**

1. **Your five-person team will produce a design with five-person-shaped seams.** If two of you own "the API" and two own "the database", you will end up with an API-shaped layer and a database-shaped layer, and the domain will be nobody's. **Watch for it. The domain being nobody's is the failure mode.**
2. **The *inverse* manoeuvre is the actionable one.** If you want a particular architecture, organise so that its boundaries are where your communication is cheapest. For a term project: **rotate ownership by feature slice, not by layer.** A person who owns "bookings end to end this fortnight" produces vertical, deliverable work; a person who owns "the database" produces a layer split (W1 L05 §2's forbidden split) wearing a job title.

---

## 8. Summary

- **Architecture is the set of decisions that are expensive to reverse**, and the test is: *what would changing this cost in March?* Most of what teams argue about fails the test.
- **You have an architecture whether or not you decide one**, and the undecided one is always the same: logic in the handlers, SQL wherever convenient, rules everywhere. **That is `roomsvc`, and it was nobody's choice.**
- **Architecture trades between quality attributes**, and they conflict. **Rank yours before choosing a shape**; for `slot` the honest order starts with testability and ends with scalability.
- **ADRs are the highest-value process artefact in this course**: immutable, negatives included, alternatives with why they lost, in git. **Write them as you decide.**
- **An invariant must be enforced at the narrowest point every path must pass through.** For uniqueness under concurrency that is the database — **the domain owns the rule, the database owns the guarantee**, and the UI enforces nothing.
- **Conway's law holds.** Your team's shape will become your system's shape; **rotate ownership by feature slice rather than by layer**, or the domain will belong to nobody.

**Next:** L11 — layered, hexagonal and MVC, with the layering violations that every real system has and the honest question of how much ceremony a five-person project should carry.

---

*CS 212 · Week 3 · L10 · © CSE Department*
