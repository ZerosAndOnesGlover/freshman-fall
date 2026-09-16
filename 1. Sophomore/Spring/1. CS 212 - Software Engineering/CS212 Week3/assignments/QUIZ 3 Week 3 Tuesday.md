# CS 212 · Quiz 3
## Administered: Tuesday, Week 3 (first 10 minutes of lecture)

**Name:** _________________________________ **Team:** ___________ **Date:** ___________

**Covers Week 2** — cohesion and coupling, SOLID, DRY, YAGNI, separation of concerns.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.

---

**Q1.** Split `confirm_booking` into nine four-line functions. Name two problems that survive.

&nbsp;

&nbsp;

---

**Q2.** `bookings.py` took 891 of 2,173 file-touches in two years. What does that measure, and why does it need no judgement?

&nbsp;

&nbsp;

---

**Q3.** State Parnas's criterion for decomposing a system into modules. What is it *not*?

&nbsp;

&nbsp;

---

**Q4.** What is the "one actor" form of the Single Responsibility Principle, and why is it better than "one thing"?

&nbsp;

&nbsp;

---

**Q5.** L08 rates dependency inversion the most valuable letter — but says the usual justification for it is the weakest. What is the usual justification, and what is the real one?

&nbsp;

&nbsp;

---

**Q6.** DRY says *"every piece of ___ must have a single, unambiguous, authoritative representation"*. Fill in the blank, and give the test that distinguishes real from false duplication.

&nbsp;

&nbsp;

---

**Q7.** Name three things YAGNI does **not** apply to, and the property they share.

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** Any two of: the VAT rate still lives in a file about booking rules; the email still cannot be tested without an SMTP server; the LDAP outage still takes bookings down; **the calendar POST is still inside the transaction, so a slow external service still rolls back a confirmed booking**; the `INSERT` is still 200 lines and two network calls after the `SELECT`.

*Length was a symptom. The disease is low cohesion and high coupling.*

---

**Q2.** **Cohesion.** A cohesive module is touched when its one concern changes; `bookings.py` is touched when **any of eight** concerns change — VAT, email wording, LDAP, the calendar API, permissions, exam rules, caching, the booking rules themselves.

It needs no judgement because **it is a count from `git log`**, not an opinion about the code.

---

**Q3.** *"Begin with a list of difficult design decisions or design decisions which are likely to change. Each module is then designed to hide such a decision from the others."*

**It is not** decomposition by **step in the processing** — read input, process, format output — which is the obvious criterion and the wrong one.

---

**Q4.** *"A module should be responsible to one, and only one, **actor**"* — an actor being a person or group who asks for changes.

Better because **"one thing" has no stopping rule** — anything can be subdivided — whereas *"which actor asks for this to change?"* is answerable. `bookings.py` serves five actors, which is how a VAT change shipped a permission regression.

---

**Q5.** **Usual justification: you can swap the database.** You will not, and it is the claim that makes reviewers stop believing you.

**The real one: fast tests and a readable domain.** You will never change database; you will run the tests ten thousand times. And *"what are the booking rules?"* becomes a question with a one-file answer.

---

**Q6.** **Knowledge.** Not code.

**The test:** *would a single change to the world require both to change, always, in the same way?* If yes, one piece of knowledge — merge. If you can imagine a change that affects one and not the other, **they are different knowledge that happens to look alike.** Leave them.

---

**Q7.** Any three of: **the security model, database migrations, the audit trail, observability, anything with a legal or contractual deadline.**

**The shared property:** they cannot be added later at a cost proportional to the new work — adding them later requires revisiting everything already written.

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L07 §1–2 |
| **Q3** | **L07 §5** — and read Parnas; it is four pages and A 3 is easier after it |
| Q4, Q5 | L08 §1, §5 |
| **Q6** | **L09 §1** — A 2 Q3(c) is marked on exactly this test |
| Q7 | L09 §3 |

**Q3 and Q6 are the ones that recur.** Parnas's criterion is this week's architecture question in its original form, and the DRY test is what stops your Week 9 refactoring from making things worse.

---

*CS 212 · Week 3 · Quiz 3 · covers Week 2 · ungraded*
