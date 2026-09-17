# CS 212 · Quiz 10
## Administered: Tuesday, Week 10 (first 10 minutes of lecture)

**Name:** _________________________________ **Team:** ___________ **Date:** ___________

**Covers Week 9** — refactoring, the smell catalogue, large refactorings.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.

---

**Q1.** Give the operational test for whether a change was a refactoring.

&nbsp;

&nbsp;

---

**Q2.** Why can `confirm_booking` not be refactored safely, and what is the way out?

&nbsp;

&nbsp;

---

**Q3.** Describe the characterisation-test procedure in three steps, and say what the mandatory comment must say.

&nbsp;

&nbsp;

---

**Q4.** What are the two hats, and what does wearing one at a time buy you when a test goes red?

&nbsp;

&nbsp;

---

**Q5.** Why is Long Function a symptom rather than the disease? Name the refactoring that addresses the real problem, and its three stages.

&nbsp;

&nbsp;

---

**Q6.** Which smell is the most serious in `roomsvc`, and why can no linter detect it?

&nbsp;

&nbsp;

---

**Q7.** In branch by abstraction, which step is the only creative one, which is where teams stall, and which does everybody forget?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **If a test had to change, it was not a refactoring.**

Tests encode observable behaviour, so a change requiring a test edit has changed what the system does — and needs the argument and care a behaviour change needs.

---

**Q2.** Because **refactoring is safe only because tests tell you when you broke something**, and `confirm_booking` has **eleven tests against ninety-four independent paths** at 31.8% branch coverage. Nothing will tell you.

**The way out: characterisation tests** — which break the deadlock that tests need seams, seams need refactoring.

---

**Q3.** **1.** Write a test asserting something obviously wrong. **2.** Run it and read the failure — the failure contains the real value. **3.** Put the real value in.

**The comment must say the test records behaviour rather than endorsing it.** Otherwise the next reader treats it as a specification and defends the bug.

---

**Q4.** **Adding functionality**, or **refactoring** — never both, though you may swap often.

**When a test goes red while refactoring, you know it was your restructuring**, because nothing else changed. The diagnosis is immediate. Mixing hats means every red test has two possible causes and you bisect by hand.

---

**Q5.** Because **extracting nine functions from `confirm_booking` leaves every real problem standing** — VAT in a file about booking rules, email untestable without SMTP, the calendar POST inside the transaction.

**Split Phase**: **decide** (pure, no I/O, testable in microseconds); **act** (one transaction, one invariant); **announce** (after the commit, retriable, cannot undo the booking).

*The split is along what changes for whom. Nobody counts lines; the count falls out.*

---

**Q6.** **Divergent Change** — `bookings.py` changes for five actors' reasons and took 891 of 2,173 file-touches in two years.

**No linter can detect it because the evidence is not in the code — it is in the `git log`.** A file with five reasons to change does not look ugly; it looks big.

---

**Q7.** **Step 1 — introduce the abstraction — is the only creative step.** Steps 2–5 are mechanical, revertable and parallelisable.

**Step 2 — migrating the callers — is where teams stall**, because it is boring and delivers nothing visible. Put a visible denominator on the board: *"12 of 31 call sites migrated."*

**Step 6 — deciding whether to keep the abstraction — is the one everybody forgets**, and it may now fail the second-implementation test.

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q4 | L28 §1, §4 |
| **Q2, Q3** | **L28 §2–3** — A 9 Q2 is worth 25 marks and is exactly this procedure |
| **Q5** | **L29 §3** — the most likely final-exam design question |
| Q6 | L29 §2 |
| Q7 | L30 §2 — A 9 Q4 plans one of these |

**Q3 and Q5 are the ones that recur.** Q3 is 25 of A 9's marks and four of them require showing the procedure rather than claiming it. Q5 is the argument that started in Week 2 and finished in Week 9, which makes it exam-shaped.

---

*CS 212 · Week 10 · Quiz 10 · covers Week 9 · ungraded*
