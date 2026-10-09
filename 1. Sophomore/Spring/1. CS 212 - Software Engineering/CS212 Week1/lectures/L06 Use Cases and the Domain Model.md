# CS 212 · Software Engineering
## Week 1 · Lecture 3 of 3
### Use Cases, and the Domain Model

*“A use case is a complete course of events in the system, seen from a user's perspective.”* — Ivar Jacobson, *Object-Oriented Software Engineering* (1992)

---

**Sat:** Thursday of Week 1, 10:00–10:50, TH 200 · **Reading:** Evans, *Domain-Driven Design*, Ch. 2 (or Sommerville §5.1–5.2) · **Next:** Week 2, design principles

**Coursework:** 📋 **Walking skeleton** due Fri this week 17:00 · 📝 **Assignment 0** due Fri this week 17:00 · 📊 **Quiz 2** Tue of Week 2 · 📝 **Assignment 2** released Wed of Week 2 17:00, due Fri of Week 3 17:00

---

## 1. What a Use Case Has That a Story Does Not

A user story is a *promise to have a conversation about a capability*. A **use case** is *the conversation, written down, as a sequence, including everything that can go wrong.*

The difference is the failure paths, and it is not a small difference.

```
Use Case: Book a resource
Primary actor:  Lecturer
Precondition:   Actor is authenticated
Guarantee:      Either exactly one confirmed booking exists for (resource, slot),
                or nothing has changed

Main success scenario
  1. Lecturer selects a resource and a slot
  2. System verifies the slot is within opening hours
  3. System verifies the actor may book this resource
  4. System places a hold on (resource, slot)
  5. System confirms the hold
  6. System notifies the actor

Extensions
  2a. Slot is outside opening hours
        2a1. System rejects with an explanation. Use case ends
  3a. Actor may not book this resource
        3a1. System rejects. Use case ends
  4a. A confirmed booking already exists
        4a1. System offers the next three free slots for that resource
  4b. Another hold exists and has not expired
        4b1. System reports the slot as temporarily unavailable, with the expiry time
  5a. The hold expired between step 4 and step 5
        5a1. System retries step 4 once, then reports failure
  6a. Notification fails
        6a1. The booking remains confirmed. The failure is logged and retried.
             ⚠️ The notification must not be able to undo the booking
```

**Count them: one success path and six extensions.** The extensions are 70% of the code you will write and 90% of the bugs you will have, and **none of them appear in the user story.**

> **Extension 6a is the one to stare at.** `roomsvc` gets this wrong: `confirm_booking` sends the
> email *inside* the transaction, so an SMTP timeout rolls back a booking the user was told about.
> **You will meet this again in Week 3** — it is an architecture question about which layer owns
> which failure — and in Week 4, where the pattern that fixes it has a name.

**Use them selectively.** Writing a full use case for every story is 1990s heaviness and you should not. **Write one for each interaction where the failure paths are where the difficulty is** — for `slot` that is booking, cancelling, and the recurring-booking expansion. Three use cases, and they will take an hour each, and they will be the hour that saves March.

---

## 2. The Domain Model Is a Vocabulary, Not a Schema

A domain model is the set of concepts your system is about, their relationships, and the rules that hold over them. **It is not a database diagram** — a database diagram is one possible encoding of it, arrived at later, with different concerns (Week 3).

Its first job is **the vocabulary**, and this is undersold. Evans calls it the *ubiquitous language*: one word per concept, used identically in conversation, in the code, in the tests, in the issue tracker, and by the users.

**`roomsvc` does not have one**, and it is measurable:

```console
$ grep -rohE '\b(booking|reservation|appointment|slot_booking|entry)\b' roomsvc/*.py \
    | sort | uniq -c | sort -rn
    891 booking
    212 reservation
     88 entry
     41 appointment
     19 slot_booking
```

**Five words for one concept.** And they are not synonyms in the code: `Reservation` in `models.py` has a `confirmed` boolean, `Booking` in `bookings.py` has a `state` string, and `_entry` in `calendar_sync.py` is a dict. **Three representations, silently converted between, in a 487-line function.** A rule applied to one is not applied to the others, which is a large part of why the invariant was violable.

> **This costs more than it looks like it costs.** Every conversation about a "reservation" requires
> a translation step in someone's head. Every translation is a place to be wrong. **The cheapest
> thing your team will do this term is agree, on Friday, on one word per concept — and the second
> cheapest is to `grep` for the others in Week 6.**

---

## 3. Modelling `slot`

Here is a domain model for the project, at the level of detail Phase 1 requires. **Yours should differ** — this is one defensible model, not the answer.

```
Resource ──< Booking >── User
   │             │
   │             └── state: HELD | CONFIRMED | CANCELLED
   │             └── slot: Slot
   │
   └── kind: ROOM | EQUIPMENT
   └── capacity: int | null
```

**Entities** — things with an identity that persists through change:

| Entity | Identity | Notes |
|---|---|---|
| `Resource` | Its code — `TH200`, `PROJ-03` | Rooms and equipment are one concept with a kind, **not two tables**. The booking rules are identical and duplicating them is how they diverge |
| `User` | University ID | |
| `Booking` | A generated id | **Not** `(resource, slot)` — that pair is unique only among *confirmed* bookings, which is the whole subtlety |

**Value objects** — things with no identity, equal when their contents are equal, and immutable:

| Value object | Why it is a value, not an entity |
|---|---|
| `Slot` | `2026-03-04T10:00` *is* the slot. Two slots with the same start are the same slot; there is nothing to update |

**The `Slot` decision is worth more than it looks.** Making it a value object with a fixed 50-minute duration means the invariant is an **equality** on `(resource, slot_start)` — which a unique index enforces. Making a booking hold arbitrary `start` and `end` timestamps makes the invariant an **overlap** — which no unique index expresses, and which lands you back in `confirm_booking`'s check-then-act (W0 L01 §6). **The domain decision and the enforceability of the invariant are the same decision**, which is why this lecture and Week 3's are connected.

*(For the record: PostgreSQL can express non-overlap, with an exclusion constraint over a `tstzrange` and a GiST index. It is the right tool if you genuinely need arbitrary intervals. **You do not** — the department books in 50-minute teaching slots — and choosing the general model because it is more general is the mistake W0 L02 §5 is about.)*

---

## 4. Invariants, Written Down

The section of `docs/domain-model.md` that Phase 1 marks most heavily. For `slot`:

| # | Invariant | Where it will be enforced |
|---|---|---|
| **I1** | **A resource has at most one `CONFIRMED` booking per slot** | **Database**: partial unique index on `(resource_id, slot)` where `state='CONFIRMED'` |
| **I2** | A `HELD` booking has an expiry; a `CONFIRMED` one does not | Schema: `CHECK`, plus the type system |
| **I3** | State transitions are `HELD → CONFIRMED`, `HELD → CANCELLED`, `CONFIRMED → CANCELLED`. **Nothing returns to `HELD`** | Domain layer, one function, tested exhaustively |
| **I4** | A booking's slot lies within the resource's opening hours | Domain layer at creation. *Note:* opening hours can change afterwards, so this is an invariant at creation, not for all time — **say so, or it is wrong** |
| **I5** | A cancelled booking is never deleted | Never issue `DELETE`; the registrar will eventually need the audit trail |

**Three things to notice, because they generalise.**

1. **I1 is enforced by the database, and that is not a cop-out — it is the only place it can be enforced.** Application code cannot make check-then-act atomic across two processes; that is a distributed mutual-exclusion problem, and the database has already solved it with a B-tree and a lock. **Your Python still catches the `IntegrityError` and turns it into a 409.** The code is not absolved of handling it; it is absolved of *deciding* it.
2. **I4 is qualified.** An invariant that is only true at a moment is not an invariant for all time, and writing it unqualified guarantees an argument in Week 8 when someone changes the opening hours. **The qualification is the content.**
3. **I5 is not a technical rule.** It is the registrar's, and you will only find it by asking. It is exactly the tacit requirement from L04 §3.

---

## 5. What the Model Is Not For

Three warnings, each of which costs a team two weeks when ignored.

**It is not a class diagram of your code.** The temptation is to make one Python class per box. Sometimes right; often not. `Slot` is a `NamedTuple`. `I3`'s state machine might be a dict of allowed transitions rather than five classes. **Model the domain; then decide, separately, how to represent it.** Week 3.

**It is not permanent.** Your model will be wrong. The interesting question is how you find out, and the answer is: **when a change that sounds simple turns out to require touching six files.** That is the model telling you a concept is missing. In `roomsvc`, *"cancel one occurrence of a recurring booking"* touches nine files, because **`Recurrence` is not a concept in the model** — recurring bookings are N rows with a shared string tag. **Issue #31, open since August 2020.**

**It is not a UML deliverable.** Draw it however you like. `docs/domain-model.md` with a code fence and a list of invariants is worth more than a beautiful diagram in a tool nobody else has installed, because **the text file is diffable and the diagram is not.** Week 11 is about exactly this property.

---

## 6. Friday

By 17:00 Friday, in your repository:

- [ ] `docs/charter.md` — filled in, including the WIP limit and the Definition of Done
- [ ] `docs/domain-model.md` — entities, value objects, **and an Invariants section**
- [ ] **The walking skeleton** — `POST /bookings` → database → `GET /bookings/{id}`, in Docker, tested by CI
- [ ] Your first stories on the board, ordered, each with acceptance criteria
- [ ] One commit per person, minimum. **Not one person committing everything**

**None of this is marked this week.** All of it is 70% of Phase 1 in Week 6 and the whole thing is an hour's work per person if you do it now.

---

## 7. Summary

- **A use case is a story with its failure paths written down.** Booking a resource has one success path and **six extensions**, and the extensions are most of the code and nearly all of the bugs. Write use cases only where the difficulty is in the failures — for `slot`, three of them.
- **Extension 6a — notification failure must not undo a confirmed booking** — is a bug `roomsvc` actually has, and it is an architecture question (W3) with a pattern name (W4).
- **A domain model is a vocabulary before it is a structure.** `roomsvc` uses **five words for one concept** and three incompatible representations, which is a large part of why its invariant was violable.
- **`Slot` as a fixed-duration value object makes the invariant an equality, which a unique index enforces.** Arbitrary intervals make it an overlap, which no unique index expresses. **The domain decision and the enforceability decision are the same decision.**
- **Write the invariants down, with where each is enforced.** I1 belongs in the database because application code cannot make check-then-act atomic across processes. I4 must be qualified or it is false. I5 exists only because someone asked the registrar.
- **The model is not your class diagram, is not permanent, and is not UML.** You find out it is wrong when a simple-sounding change touches six files — as *"cancel one occurrence"* touches nine in `roomsvc`, because `Recurrence` is not a concept there.

**Next:** Week 2 — design principles. Why `confirm_booking` is bad for reasons that have nothing to do with its length, and what coupling and cohesion actually mean when you try to measure them.

---

*CS 212 · Week 1 · L06 · © CSE Department*
