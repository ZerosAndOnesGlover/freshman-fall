# CS 212 · Software Engineering
## Week 1 · Lecture 2 of 3
### User Stories, and What Makes One Worth Writing

*“The business of software building isn't really high-tech at all. It's most of all a business of talking to each other and writing things down.”* — Tom DeMarco, *Why Does Software Cost So Much?* (1995)

---

**Sat:** Wednesday of Week 1, 10:00–10:50, TH 200 · **Reading:** Cohn, *User Stories Applied*, Ch. 1–2 (or Sommerville §4.4) · **Next:** L06, use cases and the domain model

**Coursework:** 📝 **Assignment 1** released today 17:00, due Fri of Week 2 17:00 · 📋 **Walking skeleton** due Fri this week 17:00 · 📝 **Assignment 0** due Fri this week 17:00 · 📊 **Quiz 2** Tue of Week 2
**A 1 is released after this lecture**, Wednesday 17:00.

---

## 1. The Format Is the Least Important Part

```
As a <role>, I want <capability>, so that <benefit>.
```

**This template is not the technique.** Ron Jeffries, who invented the surrounding practice, described a story as **three Cs**:

| | |
|---|---|
| **Card** | A short written reminder — the template above, or anything else |
| **Conversation** | **The discussion the card triggers.** This is where the requirement actually gets specified |
| **Confirmation** | The acceptance criteria: how we will agree it is done |

**The card exists to schedule the conversation.** A team that writes forty perfectly-formatted cards and never has a conversation has produced forty perfectly-formatted nothings — which is the single most common failure of "doing agile" in a student project, because the cards are visible and the conversations are not.

**That said, the template does one useful thing**, and it is the third clause. *"So that…"* forces you to state the benefit, and **a story whose benefit clause is empty or circular is a story you should not build.**

> *"As a user, I want a settings page, so that I can change my settings."* — **Delete it.** There is
> no benefit here, which means nobody knows why it is on the board, which means it is in the 45%
> (W0 L02 §5).

---

## 2. INVEST, With the Two That Matter

Bill Wake's checklist. Six letters; two of them do real work.

| Letter | | |
|---|---|---|
| **I** | Independent | Can be built without waiting for another story. Rarely fully true; aim for *orderable* |
| **N** | Negotiable | The card is not a contract. If it reads like a specification, the conversation has been skipped |
| **V** | **Valuable** | **To someone nameable.** If you cannot name who is worse off without it, it is not a story |
| **E** | Estimable | You know enough to guess the size. If you cannot, the story is really a research question — make it a spike |
| **S** | **Small** | **Finishable in a few days by one or two people** |
| **T** | Testable | You can say what would prove it done. §3 |

### Why **Small** is the one that matters most

A story that takes three weeks is a story whose progress you cannot see. It is 80% done for a fortnight, and the last 20% contains all the surprises. **Small stories are how you find out you were wrong while it is still cheap** — which is the same thing every process model since 1968 has been trying to buy (W0 L02 §6).

**Splitting is a learnable skill.** The bad way is by layer:

> ❌ *"Build the database schema"* → *"Build the API"* → *"Build the UI"*

**Nothing is deliverable until all three are done**, so you get no feedback until the end — you have rebuilt the waterfall inside your sprint, which is exactly what the sprint was for.

**The good ways**, in rough order of usefulness:

| Split by | Example on `slot` |
|---|---|
| **Workflow step** | *"Create a hold"* → *"Confirm a hold"* → *"Expire a hold"* |
| **Business rule** | *"Book a free slot"* → *"Reject a taken slot"* → *"Reject a slot outside opening hours"* |
| **Happy path first** | *"Book a room"* now; *"Book a room when the network drops mid-request"* later |
| **Data variation** | *"Book a room"* → *"Book equipment"* → *"Book a room and its projector together"* |
| **Effort in the interface** | *"Pick a slot from a list"* now; *"pick it from a calendar grid"* later |

**Every one of those slices is independently demonstrable.** That is the test.

### Why **Valuable** is the second

*"Valuable to a nameable person"* is the filter that stops a backlog from filling with work that exists because a developer found it interesting. **Your `slot` backlog will contain at least one story about caching, one about a nicer admin interface, and one about a plugin architecture, and none of them will have a nameable beneficiary.** They are not wrong to want. They are wrong to be in the same list as the work.

---

## 3. Acceptance Criteria Are the Actual Requirement

The card is a placeholder. **The acceptance criteria are the thing you can be wrong about**, and they are what the test is written from.

**Given/When/Then** (from BDD; Week 5 does it properly with executable tests):

```gherkin
Story: As a lecturer, I want to book a room for a slot,
       so that I know I have somewhere to teach.

  Scenario: the slot is free
    Given TH 200 has no confirmed booking at 2026-03-04 10:00
    When I request TH 200 for that slot
    Then the booking is confirmed
    And it appears in my bookings list

  Scenario: the slot is taken
    Given TH 200 has a confirmed booking at 2026-03-04 10:00
    When I request TH 200 for that slot
    Then the request is rejected with 409 Conflict
    And no second booking exists

  Scenario: two requests arrive at once          # <- the interesting one
    Given TH 200 has no confirmed booking at 2026-03-04 10:00
    When two clients request that slot simultaneously
    Then exactly one is confirmed and the other receives 409
    And exactly one confirmed booking exists
```

**The third scenario is the whole difference between your system and `roomsvc`.** It is the VNC 101 incident written as an acceptance criterion, and it was in nobody's story in 2020.

**Three properties of a good criterion:**

1. **Observable from outside.** *"The booking is saved correctly"* is not observable; *"a GET of the booking returns 200 with state `confirmed`"* is.
2. **Includes the failure cases.** A story with only a happy path is a story someone will implement with no error handling, correctly, because that is what you asked for.
3. **Numeric where it is about quality.** *"Fast"*, no. *"Under 300 ms at p95 with 500 bookings"*, yes.

> **A working rule for your team's Definition of Done:** if you cannot write the Then, you have not
> finished specifying the story. **Do not start it.**

---

## 4. Where Stories Are the Wrong Tool

Stories are good at user-visible capability. They are bad at four things you will need anyway.

| What | Why a story fits badly | What to use instead |
|---|---|---|
| **Invariants** | Not something a user wants; something that must never be false | A stated invariant in `docs/domain-model.md`, plus a test |
| **Cross-cutting quality** — security, accessibility, performance | *"As a user I want the site not to be hacked"* is absurd, and putting it on the board means it gets prioritised against features and loses | The **Definition of Done**. Every story is done only if it meets them |
| **Research** — *"can SQLAlchemy express this constraint?"* | It has no user and no acceptance criterion | A **spike**: timeboxed, and the deliverable is an answer, usually an ADR |
| **Debt and maintenance** | The beneficiary is a future developer, so it always loses on value | A named share of each iteration, agreed in the charter. Week 11 |

**The second row is where student teams lose the most marks.** Security and accessibility go on the board as stories, sit at the bottom of the order for eleven weeks, and are never built. **Put them in the Definition of Done and they get done fifty times.**

---

## 5. Estimation, Briefly and Sceptically

You will be asked to estimate. Here is what is known.

- **Relative estimation beats absolute.** People are poor at "how many hours" and better at "bigger or smaller than that one". This is why story points exist.
- **Story points are not in the Scrum Guide** and are not required by anything. Counting stories, once they are consistently small, **predicts about as well as pointing them** — a result that has been replicated and that surprises people.
- **Velocity is a planning aid and a terrible management metric.** The moment it is used to compare teams or judge performance, it inflates, because points are made up. Week 11 has the general form of this failure (Goodhart's law).
- **The most useful number in a student project is not an estimate at all.** It is **cycle time**: how long a card actually takes from "In Progress" to "Done". Measure it from your board. **It will be much longer than you think, and the reason will be that you started too many things at once** (Little's Law, W0 L02 §7).

> **What your team should actually do:** make stories small enough that estimation stops mattering.
> **A story you can finish in two days does not need an estimate; it needs starting.** If you find
> yourselves arguing about whether something is a 3 or a 5, the argument is a signal that the story
> is not understood — **split it, do not point it.**

---

## 6. The Walking Skeleton Is Due Friday

Not a story. The precondition for having stories mean anything.

**Alistair Cockburn's definition:** *a tiny implementation of the system that performs a small end-to-end function. It need not use the final architecture, but it should link together the main architectural components.*

**For `slot`, concretely:**

```
POST /bookings  {resource: "TH200", slot: "2026-03-04T10:00"}
    → FastAPI route
    → service function
    → SQLAlchemy insert into a real PostgreSQL
    → 201 with an id
GET /bookings/{id}
    → 200 {resource, slot, state: "confirmed"}
```

Plus: **`docker compose up` works on every team member's laptop**, and **a GitHub Actions workflow runs the one test on every push.**

**That is the whole deliverable.** No authentication. No user interface. No validation. One resource hard-coded is fine. **It must be whole, not good.**

> **Why this is the highest-value thing you do all term.** Everything that is going to be hard
> about integrating your work is hard *now*, when there is nothing to integrate: the database
> connection string, the container networking, the migration tool, the test database, the four
> laptops with three Python versions. **Teams that defer the skeleton meet all of it in April,
> simultaneously, along with everything else.** Every previous cohort's retrospective says this
> sentence, and every cohort contains teams that do it anyway.

---

## 7. Summary

- **The template is not the technique.** A story is **Card, Conversation, Confirmation**, and the card exists only to schedule the conversation. A story with an empty *"so that"* should be deleted.
- **INVEST's load-bearing letters are Small and Valuable.** Small is how you find out you were wrong cheaply; Valuable-to-a-nameable-person is what keeps the interesting-but-pointless off the board.
- **Never split by layer.** Split by workflow step, business rule, happy path, data variation, or interface effort — each slice independently demonstrable.
- **The acceptance criteria are the requirement.** Observable from outside, failure cases included, numeric where they concern quality. **If you cannot write the Then, do not start the story.**
- **The concurrent-request scenario is the difference between your system and `roomsvc`.**
- **Stories are the wrong tool for invariants, cross-cutting quality, research and debt.** Quality belongs in the **Definition of Done**, where it is satisfied fifty times instead of losing fifty prioritisation arguments.
- **Story points are optional and abusable; cycle time is the number worth measuring.** Make stories small enough that estimation stops mattering.
- **The walking skeleton is due Friday.** Thin, ugly, whole, containerised, and built by CI.

**Next:** L06 — use cases, where the failure paths live; and the domain model, where the invariants live.

---

*CS 212 · Week 1 · L05 · © CSE Department*
