# CS 212 · Quiz 2
## Administered: Tuesday, Week 2 (first 10 minutes of lecture)

**Name:** _________________________________ **Team:** ___________ **Date:** ___________

**Covers Week 1** — requirements, user stories, acceptance criteria, use cases, and the domain model.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.

---

**Q1.** Name the four requirement categories from L04, and say which one the VNC 101 double-booking belonged to.

&nbsp;

&nbsp;

---

**Q2.** What is wrong with the requirement *"the week view shall be fast"*, and what is the minimum needed to fix it?

&nbsp;

&nbsp;

---

**Q3.** L04 says vagueness in a requirement is usually a symptom. Of what? Give the seven-word example.

&nbsp;

&nbsp;

---

**Q4.** Name three ways to split a user story, and the one way you must not.

&nbsp;

&nbsp;

---

**Q5.** Write the third acceptance scenario for *"book a room"* — the one that is the whole difference between `slot` and `roomsvc`.

&nbsp;

&nbsp;

---

**Q6.** Why does a notification failure have to be outside the transaction that confirms a booking?

&nbsp;

&nbsp;

---

**Q7.** Fixed 50-minute slots versus arbitrary start/end times: which makes the no-double-booking invariant enforceable by a unique index, and why?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **Functional, non-functional (quality), constraint, and invariant.** The double-booking violated an **invariant** — *"a resource has at most one confirmed booking per slot"*.

*An invariant is not something the system does; it is something the system is. That is why it appeared in no user story.*

---

**Q2.** It is **unfalsifiable** — you cannot write a test for it. **A non-functional requirement needs a number, a percentile and a load**: *"the week view renders in under 300 ms at p95 with 500 bookings loaded"*.

---

**Q3.** **Unresolved conflict between two stakeholders.** The example: **"Admins should be able to cancel bookings"** (`roomsvc` issue #812) — seven words hiding at least five questions, vague because the registrar wants control and the lecturer wants not to be overridden, and nobody settled it.

---

**Q4.** Any three of: **workflow step**, **business rule**, **happy path first**, **data variation**, **effort in the interface**.

**Never split by layer** — *"build the schema / the API / the UI"* — because nothing is deliverable until all three are done. That is the waterfall rebuilt inside the sprint.

---

**Q5.**

```gherkin
  Scenario: two requests arrive at once
    Given TH 200 has no confirmed booking at that slot
    When two clients request that slot simultaneously
    Then exactly one is confirmed and the other receives 409
    And exactly one confirmed booking exists
```

*It was in nobody's story in 2020, and it is the scenario that describes 14 October 2024.*

---

**Q6.** Because **a notification failure must not undo a booking the user has already been told about**. The cancellation or confirmation is committed first; the side effect is attempted after, and is retriable and idempotent.

*`roomsvc` gets this wrong at `bookings.py:398` — `notify.send()` inside the `with db.begin()` block, so an SMTP timeout rolls back a confirmed booking.*

---

**Q7.** **Fixed 50-minute slots.** They make the invariant an **equality** on `(resource_id, slot)`, which a partial unique index enforces across processes and against direct writes. Arbitrary start/end times make it an **overlap**, which no unique index expresses — so the check goes back into application code, which is exactly where `confirm_booking` was standing.

*Postgres can do it, with an exclusion constraint over a `tstzrange` and `btree_gist`. Knowing the escape hatch is part of knowing the trade.*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L04 §2 |
| Q3 | L04 §5 |
| Q4 | L05 §2 |
| **Q5** | **L05 §3** — and check whether it is in your team's board |
| **Q6** | **L06 §1**, extension 6a — Week 4 names the pattern that fixes it |
| **Q7** | **L06 §3** — this is the midterm's most likely design question |

**Q5 and Q7 are the ones that recur.** Q5 becomes an actual running test in Week 5 and a surviving mutant in Week 6. Q7 is the decision your Phase 1 domain model is marked on.

---

*CS 212 · Week 2 · Quiz 2 · covers Week 1 · ungraded*
