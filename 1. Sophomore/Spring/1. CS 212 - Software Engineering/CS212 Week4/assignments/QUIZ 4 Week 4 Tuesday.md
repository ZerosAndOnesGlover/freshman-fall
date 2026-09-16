# CS 212 · Quiz 4
## Administered: Tuesday, Week 4 (first 10 minutes of lecture)

**Name:** _________________________________ **Team:** ___________ **Date:** ___________

**Covers Week 3** — architecture, layered and hexagonal, MVC, microservices, event-driven.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.

---

**Q1.** Give the operational definition of architecture, and the test it yields.

&nbsp;

&nbsp;

---

**Q2.** Where is the no-double-booking invariant enforced, and why does each of the other four candidates fail?

&nbsp;

&nbsp;

---

**Q3.** Layering's stated rule is "a layer may call the layer below". What is the unstated rule, and why does it matter more?

&nbsp;

&nbsp;

---

**Q4.** Name the two things hexagonal architecture actually buys, and the one benefit you should *not* cite.

&nbsp;

&nbsp;

---

**Q5.** What is the one thing microservices buy? Name three items on the bill.

&nbsp;

&nbsp;

---

**Q6.** An ADR has five sections. Which one carries the marks, and which one answers the question someone asks in March?

&nbsp;

&nbsp;

---

**Q7.** State Conway's law, and the counter-measure for a five-person team.

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **Architecture is the set of decisions that are expensive to reverse.** The test: **what would changing this cost in March?** Hours → a detail; stop arguing and write it. Weeks → architecture, and it deserves an ADR.

---

**Q2.** **The database**, as a partial unique index on `(resource_id, slot) WHERE state='CONFIRMED'`.

| Candidate | Why it fails |
|---|---|
| The UI | Bypassable — `curl` ignores it |
| The API layer | Cannot see concurrent requests |
| The domain layer | Two processes both check, both pass, both insert — **this is `confirm_booking`** |
| An in-process lock | Does not span four workers |

**The domain owns the rule; the database owns the guarantee.** General form: **an invariant must be enforced at the narrowest point every path must pass through.**

---

**Q3.** **Unstated: a layer may not know the layer above exists.**

It matters more because without it you have layers that are labels on directories — a domain importing the web framework's exception type because it was convenient. **And it is the one a machine can check**, in about twelve lines of `ast`.

---

**Q4.** **Fast tests** (measured: ~1 ms with a fake repo against ~1.2 s per module with a container) **and a readable domain** — *"what are the booking rules?"* becomes a one-file question.

**Do not cite database portability.** You will never swap the database, and citing it is what makes reviewers stop believing the rest of your ADR.

---

**Q5.** **Independent deployability by separate teams.** That is all; everything else is a consequence of it or obtainable without it.

Three from the bill: **you lose the transaction** (sagas, and compensation is not undo); **partial failure** (retries, idempotency, timeouts, circuit breakers, correlation IDs); **debugging becomes seven logs**; local development becomes eight containers; **refactoring across a boundary becomes a migration**.

---

**Q6.** **Consequences carries the marks** — specifically the *negatives*. An ADR with only upsides is marketing.

**Alternatives Considered answers the March question**, because the alternative that lost is usually the one someone is about to propose again.

---

**Q7.** *"Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations."*

**Counter-measure: rotate ownership by feature slice, not by layer.** If two of you own "the API" and two own "the database", **the domain belongs to nobody** — which is how you build `roomsvc`.

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1 | L10 §1 |
| **Q2** | **L10 §6** — A 3 Q4 is this, with the DDL and a concurrent transcript |
| **Q3** | **L11 §1** — and add the test this week, while the violation count is zero |
| Q4 | L11 §2 |
| Q5 | L12 §1–2 |
| **Q6** | **L10 §5** — A 3 Q2 is marked on exactly this |
| Q7 | L10 §7 |

**Q2 and Q6 are the ones that recur.** Q2 is the midterm's most likely long question and is the thing your Phase 1 is most distinguished by; Q6 is how your ADRs get marked twice — in A 3, and again in the final report.

---

*CS 212 · Week 4 · Quiz 4 · covers Week 3 · ungraded*
