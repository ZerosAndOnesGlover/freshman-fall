# CS 212 · Quiz 6
## Administered: Tuesday, Week 6 (first 10 minutes of lecture)

**Name:** _________________________________ **Team:** ___________ **Date:** ___________

**Covers Week 5** — the test pyramid, TDD, test doubles, BDD, end-to-end.

**Instructions:** Closed notes. 10 minutes.

> **Phase 1 presentations follow this lecture, and the midterm is tomorrow evening.** This quiz is
> ten minutes and it is unmarked; sit it, mark it against the key below, and use the table at the
> end as tonight's revision list.

---

**Q1.** What is a test *for*? Answer in one sentence, and say where the value lies.

&nbsp;

&nbsp;

---

**Q2.** The pyramid's proportions follow from three facts. Name them. Which one is the one that kills projects?

&nbsp;

&nbsp;

---

**Q3.** Why can the transaction-rollback fixture not be used for the concurrency test?

&nbsp;

&nbsp;

---

**Q4.** What does the careful replication (Fucci et al., 2016) find that the benefit of TDD actually tracks?

&nbsp;

&nbsp;

---

**Q5.** Name the five test doubles. Which two verify state, and which verifies interactions?

&nbsp;

&nbsp;

---

**Q6.** `notify.assert_called_once_wiht(...)` — note the typo. What happens, and what fixes it?

&nbsp;

&nbsp;

---

**Q7.** What is the ten-second habit from L17 §5, and what is it a manual version of?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **A test is a claim about behaviour, written so that a machine can tell you when the claim stops being true.**

**The value is in the *stops*.** You write the code once and change it four hundred times; the suite is what lets you change code you do not fully understand.

---

**Q2.** **Cost scales up** the pyramid (E2E is 1,000–10,000× a unit test). **Diagnostic precision scales down** (a failing unit test names the function; a failing E2E test names your system). **Brittleness scales up.**

**The third kills projects.** Once "just re-run it" becomes normal, **every real failure is also probably flaky**, and the suite has stopped being evidence.

---

**Q3.** The rollback fixture runs the whole test **inside one uncommitted transaction on one connection.** Two concurrent clients need **two connections**, and an uncommitted row is invisible to the other one — so the unique index is never contended and the test passes regardless.

*Use truncation, a dedicated schema, or a separate database for those few tests.*

---

**Q4.** **Small, uniform steps with frequent test execution** — **not** writing the test first. 39 professionals; no significant effect of test-*first* on external quality or productivity, and what predicted outcomes was the granularity and uniformity of the cycle.

*Good news, not a debunking: the discipline is real, and TDD is an unusually effective way to enforce it.*

---

**Q5.** **Dummy, stub, spy, mock, fake.**

**Stubs, fakes (and dummies) verify state. Mocks verify interactions** — and interaction verification couples the test to the implementation's route rather than its result.

---

**Q6.** **It passes.** `Mock()` invents any attribute you touch, so the typo'd assertion is a no-op that silently succeeds.

**`autospec=True`** (or `create_autospec` / `spec_set=`) fixes it — the double then only has the attributes the real object has, and the typo raises `AttributeError`.

---

**Q7.** **Break the code and check the test notices** — comment out a line, flip a comparison, change a constant — then run the test that covers it. **If it still passes, the test is decorative.**

**It is mutation testing done by hand**, which is today's third lecture.

---

### What to Do With Your Score — and Tonight

There is no score. **Use this as the midterm revision list**:

| If you missed | Reread before tomorrow |
|---|---|
| Q1, Q2 | L16 §1–2 |
| **Q3** | **L16 §5** — and A 5 Q1(c) asks it directly |
| **Q4** | **L17 §3** — essay C1 leans on how the evidence in this field is distributed |
| Q5, Q6 | L18 §1–2 — **midterm B3 is a test with exactly these defects in it** |
| **Q7** | **L17 §5** — and it is this afternoon's L21 |

**B3 on tomorrow's paper is a `Mock`-based test with three defects.** If Q5 or Q6 was shaky, that section is thirty minutes of revision that is worth twelve marks.

---

*CS 212 · Week 6 · Quiz 6 · covers Week 5 · ungraded*
