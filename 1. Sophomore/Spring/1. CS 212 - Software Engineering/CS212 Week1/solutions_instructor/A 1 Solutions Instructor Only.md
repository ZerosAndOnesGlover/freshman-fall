# CS 212 · Assignment 1 — Solutions and Mark Scheme
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for A 1.** This is the first paper requiring the student to read a codebase
they did not write. **Expect it to go badly for about a third of the cohort**, and mark the method
rather than the yield: a student who documents how they searched and found two real invariants
scores above one who found four by reading the issue tracker.

**The single discriminator on this paper is failure paths.** Q2, Q3 and Q4 all reward them and the
mark scheme is built so that a happy-path-only submission caps around 55.

---

## Q1: Find the Unwritten Requirement (20)

### (a) [5]

**The invariant:** *"A resource has at most one confirmed booking per slot."*

| | |
|---|---|
| 2 | The sentence, stated as a thing that must never be false — not as a feature |
| 1 | Category: **invariant** (accept "non-functional" only if the student argues it and notes the distinction) |
| 2 | **Why no story:** it is not something a user *wants*; it never occurs to anyone that it could be false. Stories describe capabilities; this describes the absence of a possibility |

**Deduct 2** for *"as a user I want no double-bookings"* — the point of (a) is that this is not a story.

### (b) [8]

Open-ended by design. **Award marks for evidence of having read code**, not for matching this list.

**Real ones in the reference snapshot**, for the marker's own use:

| Invariant the code enforces | Where | How it can be violated today |
|---|---|---|
| A booking's `owner_id` must exist in `users` | `models.py` ForeignKey, line 214 | It cannot at the DB level — **this is a good answer for (c)'s "correctly enforced" case** |
| A `HELD` booking older than 15 minutes is treated as absent | `bookings.py:355`, an implicit `WHERE created > now() - interval` | **Nothing expires it.** The rows accumulate; a `state='HELD'` row from 2021 is still in the table. The rule exists in *queries*, not in the data |
| `state` is one of four strings | Nowhere — it is a plain `String(20)` column, `models.py:198` | **Any typo.** `git log -S"'Confirmed'"` finds commit `c81ae40`, which wrote a capitalised variant for three weeks in 2022 |
| A recurring group's members share `recur_tag` | `bookings.py:2103` `apply_recurrence` | Direct update; also partial failure mid-expansion, which is not transactional |
| `cancelled_at` is set iff `state='CANCELLED'` | Implicit in two functions, contradicted in a third | `admin.py:271` sets `state` without `cancelled_at` |
| A resource's `capacity` is positive | Nowhere | A negative capacity is accepted and renders as a negative number in `reports.py` |

| | |
|---|---|
| 2 per invariant × 3 | 1 for the sentence + line number; 1 for a **concrete** violation path |
| 2 | Method — evidence of having grepped, read tests, or used `git log -S` |

**Award full marks for invariants not on this list** if the line number checks out. **Deduct** for anything sourced from a docstring — the question asks for rules that are *not* written down.

### (c) [7]

| | |
|---|---|
| 2 per invariant × 3 | Placement with a reason |
| 1 | **The "not at all" case**, correctly identified |

**Correct placements**, broadly:

- **Database** for anything that must hold across concurrent processes or against direct writes: uniqueness, foreign keys, `CHECK` on an enum, `capacity > 0`.
- **Domain layer** for anything requiring several entities or a decision: state transitions, permission rules.
- **API layer** for nothing, really — validation at the edge is good practice but is not *enforcement*, and a student who says so has understood the lecture.

**The "not at all" answer.** The best is the 15-minute hold expiry: **it should not be an invariant, it should be a scheduled job plus an expiry column**, because an invariant enforced only in query predicates is not enforced. Accept also the `recur_tag` grouping — the right answer there is that `Recurrence` should be an entity (Q4c), at which point the invariant dissolves.

**A student who says all three belong in the database has not thought about it.** Cap (c) at 4.

---

## Q2: Stories, With Criteria That Bite (20)

### (a) [8]

2 per story. **1 for the card** (role, capability, **non-circular benefit**), **1 for the criteria including at least one failure scenario.**

**Deduct 1 per story** with a circular *"so that"*. **Deduct 1 per story** whose criteria are not observable from outside — "the booking is saved correctly" is the canonical bad one.

**Award a bonus mark within the section** (up to the cap) for any student who writes a **concurrency scenario** unprompted. It is in L05 §3 and about a fifth of the cohort will carry it across.

Watch for the **admin** story reproducing `roomsvc` issue #812's ambiguity — *"admins can cancel bookings"*. **That is not a failure**; it is a good opportunity in feedback to ask which two stakeholders are disagreeing.

### (b) [6]

| | |
|---|---|
| 1 per split × 3 | Three genuinely **different strategies** from L05 §2 |
| 3 | Which slice first, with a reason, for each |

**Deduct all 3 of the first part** for any split by layer — *"build the schema / the API / the UI"*. It is explicitly the wrong answer in the lecture and it is the most common submission.

**The best answers order by risk**, not by ease: *"reject a taken slot first, because it is the invariant and everything else is decoration"*. Give full marks and say so in feedback.

### (c) [6]

| | |
|---|---|
| 3 | The beneficiary test applied honestly |
| 3 | The feature-usage argument, applied to **this** story rather than quoted |

**The marking judgement:** a student who argues against a story they clearly want to build — a calendar UI, a notification system, a mobile app — gets 6. A student who knocks down an obvious straw story gets 3. **Say which in the feedback**, because Q5 depends on the same skill and it is worth 15.

---

## Q3: A Use Case, With Its Failures (20)

### (a) [12]

| | |
|---|---|
| 3 | Actor, precondition, **guarantee** (the guarantee is the part usually missing) |
| 3 | A coherent main success scenario, numbered, in the right grain |
| **6** | **Five extensions, correctly numbered against their steps, including the three required kinds** |

**The three required kinds, with model answers:**

| Required | Model |
|---|---|
| Not permitted | *"3a. Actor does not own the booking and is not an admin → reject, 403, use case ends"* |
| State changed since last look | *"4a. Booking is already `CANCELLED` → report success idempotently"* or *"4b. The slot has already started → reject or require an admin"* — **both are excellent, and the second surfaces a real requirement** |
| Downstream failure after success | *"6a. Notifying the facilities team fails → the cancellation stands; the notification is retried; the failure must not roll back the cancellation"* |

**Deduct 2** for extensions written as a flat list unattached to step numbers — the numbering is what makes a use case more than a list.

### (b) [4]

| | |
|---|---|
| 2 | **What must not happen: the cancellation must not be undone by the notification failing** |
| 2 | The property: the notification is **outside the transaction**; the cancellation is committed before the side effect is attempted; the side effect is retriable and idempotent |

**Full marks also for** a student who names the general problem — you cannot atomically commit a database change and an external call — and gestures at the outbox pattern. It is Week 4's material and finding it now is worth noting.

**`roomsvc`'s version:** `bookings.py:398`, `notify.send()` inside the `with db.begin()` block. A student who cites the line gets the 4 regardless of vocabulary.

### (c) [4]

| | |
|---|---|
| 2 | A defensible interaction — *"list my bookings"*, *"view the week grid"*, *"look up a resource"* |
| 2 | **The distinguishing property** |

**The property:** a use case earns its hour when the interaction **changes state**, **has more than one actor or system involved**, and **can fail partway with something left behind**. A read-only query with one failure mode ("not found") has nothing to write down. Accept any formulation containing *changes state* or *can fail partway*.

---

## Q4: The Domain Model (25)

### (a) [10]

| | |
|---|---|
| 3 | Entities with **stated identities** (not just names) |
| 2 | At least one value object, correctly justified as having no identity |
| **4** | **Four invariants, each with a placement** |
| 1 | An explicit statement of agreement or disagreement with L06 §3 |

**Deduct 2** for a model that is an ER diagram with no invariants section. **Deduct 2** for making `Room` and `Equipment` separate entities without arguing for it — L06 §3 gives the reason against, and a student may argue back, but not silently.

**Award full marks for a materially different model that hangs together.** The best alternative seen in previous cohorts makes `Booking` an event log with `state` derived; it is defensible, it makes I5 free, and it makes I1 much harder. **A student who notices that trade should be told they have done something good.**

### (b) [8]

**(b) first part [4]:**

**What fixed-duration slots give up**, and a real requirement they cannot express — accept any of:
- A three-hour exam booking (the department holds 150-minute finals — **it is in the registry's own calendar**, and a student who notices this gets all 4)
- Setup or turnaround time between bookings
- Equipment loaned overnight or for a week
- Anything for an external event outside the teaching grid

**The workaround** — N consecutive slots for one logical booking — **is the right answer and should be credited**, along with its cost: cancelling a three-hour exam is now three operations that must succeed or fail together, which is the `Recurrence` problem in miniature.

**(b) second part [4]:**

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

ALTER TABLE bookings ADD CONSTRAINT no_overlap
  EXCLUDE USING gist (
    resource_id WITH =,
    tstzrange(starts_at, ends_at, '[)') WITH &&
  ) WHERE (state = 'CONFIRMED');
```

| | |
|---|---|
| 2 | Working DDL — `EXCLUDE USING gist`, `&&`, the `WHERE` for the partial constraint |
| 1 | `btree_gist` required for the `=` on a scalar column. **Most students miss this and it is the part that fails in practice** |
| 1 | The cost: an extension to install, a GiST index rather than a B-tree, a constraint most developers cannot read, and `'[)')` bounds semantics that are load-bearing and invisible |

**Give the full 4** to a student who ran it. **Give 3** for correct DDL without `btree_gist`, noting it in feedback — it is exactly the kind of thing that works on the marker's machine and fails on the student's.

### (c) [7]

**First part [4]:** the `grep`, reproduced, plus one more multiply-named concept. Real ones:

```console
$ grep -rohE '\b(user|account|person|owner|requester)\b' roomsvc/*.py | sort | uniq -c | sort -rn
    604 user
    233 owner
    112 account
     58 requester
     14 person
$ grep -rohE '\b(resource|room|space|venue|asset)\b' roomsvc/*.py | sort | uniq -c | sort -rn
    712 room
    301 resource
     97 asset
     44 venue
     12 space
```

The `room`/`resource` split is the richest: **`room` predates equipment support**, which was added in 2022 and named `resource`, and the two vocabularies never merged. 2 for counts, 2 for any observation about *why* the split exists.

**Second part [3]:** **the missing concept is `Recurrence`** (or `RecurringSeries`, `BookingSeries` — any name). The model should have a `Recurrence` entity owning a rule and a set of `Booking`s, so that cancelling one occurrence is a state change on one child, and changing the series is one operation. 2 for the concept, 1 for a two-sentence statement of what follows.

---

## Q5: Disagree With Your Team (15)

| | |
|---|---|
| **6** | **(a) Steel-manning.** The strongest case for the decision, stated better than its advocate stated it |
| 6 | (b) The alternative, with **what evidence would settle it** and whether it is obtainable |
| 3 | (c) An actual intention, with a reason |

**Mark (a) hardest.** A weak statement of the opposing case caps the question at 8 however good (b) is — the skill being taught is that you cannot argue against a position you cannot state.

**Full marks for "nothing, they are right"** in (c) if (a) and (b) are real. Full marks also for *"nothing — I think I am right and it is not worth the two hours of team time before Phase 1"*, **which is the most professionally mature answer available and should be praised explicitly.**

**Award nothing** for a manufactured disagreement about something trivial (tabs, file names). If a student genuinely cannot find a decision they doubt, the honest answer — *"we have not made a decision anyone could doubt yet, which is itself a problem, and here is why"* — is worth up to 10 and should be encouraged in feedback.

---

## Overall Bands

| Band | |
|---|---|
| **90–100** | Q1(b) has line numbers and a violation path for each; Q1(c) identifies a rule that should not be an invariant. Concurrency appears in the acceptance criteria unprompted. Q3 has five properly-numbered extensions. Q4(b) DDL runs, with `btree_gist`. Q5 steel-mans genuinely |
| **75–89** | Specific and correct throughout. Failure paths present. Model coherent with placements. Q4(b) DDL nearly right. Q5 real but safe |
| **60–74** | Happy-path-heavy. Invariants listed without placement. Q1(b) from documentation rather than code. Q2(b) contains a layer split |
| **45–59** | Stories without criteria; use case with three extensions; ER diagram for a domain model; Q5 pro-forma |
| **< 45** | No contact with `roomsvc`. Invariants confused with features throughout |

**Feedback note for every paper:** name the best of their invariants and say where it should be enforced if they got the placement wrong. **Placement is Week 3's entire subject**, and a student who arrives at Week 3 having already been told they put an invariant in the wrong layer gets much more out of it.

---

*CS 212 · Week 1 · A 1 Solutions · INSTRUCTOR ONLY*
