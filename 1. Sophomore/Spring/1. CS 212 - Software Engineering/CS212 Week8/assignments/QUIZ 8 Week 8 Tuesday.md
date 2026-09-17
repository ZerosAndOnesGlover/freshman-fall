# CS 212 · Quiz 8
## Administered: Tuesday, Week 8 (first 10 minutes of lecture)

**Name:** _________________________________ **Team:** ___________ **Date:** ___________

**Covers Week 7** — code review, the checklist, automated review.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.
>
> **First week back from Spring Break.** A 7 is due Friday 27 March — if your partner has not opened
> a pull request, tell the instructor **today**.

---

**Q1.** Where does "code review finds 60% of defects" come from, and why does it not apply to a pull request?

&nbsp;

&nbsp;

---

**Q2.** Bacchelli & Bird classified 570 review comments. What was expected first, and what actually dominated?

&nbsp;

&nbsp;

---

**Q3.** Give the standard for approving a change, and the one thing it is explicitly *not*.

&nbsp;

&nbsp;

---

**Q4.** The checklist has five passes. Name them in order, and say why the order matters.

&nbsp;

&nbsp;

---

**Q5.** Name the four severity labels, and say what happens to a review without them.

&nbsp;

&nbsp;

---

**Q6.** A teammate keeps making the same mistake. Why is review the wrong tool, and what is the right one?

&nbsp;

&nbsp;

---

**Q7.** Which of the five automation layers may block a merge, and which must only advise? Why?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **Fagan inspection**, IBM, 1976. Three to six people with defined roles; **hours of individual preparation**; a **reader paraphrasing the code aloud** while the author stays quiet; **~150 lines per hour**; defects **logged, not solved**; a separate rework stage and a follow-up.

**A pull request is one reviewer, asynchronous, no preparation, no paraphrase, often five minutes, at thousands of lines per hour.** Different activities with the same name.

---

**Q2.** **Expected first: finding defects.** **Actually: code improvements at ~29%** — readability, naming, structure — with **defects at ~14%**, knowledge transfer ~9%, alternatives ~7%.

**The real value is knowledge transfer, team awareness and readability**, which nobody lists when asked what review is for.

---

**Q3.** **Approve when the change definitely improves the overall code health of the system, even if it is not perfect.**

**It is not *"is this how I would have written it?"*** If the author's approach is reasonable and yours is also reasonable, the author's wins.

*The exception: push back hard on **design**, because that is what is expensive to reverse.*

---

**Q4.** **1. Should this exist? 2. Design. 3. Correctness. 4. Tests. 5. Readability.**

**The order is the content**: a reviewer who starts at line 1 comments on naming, because naming is easy to see, and **attention is exhausted in under an hour** — so the design, which is the expensive-to-reverse half, never gets looked at.

---

**Q5.** **`blocking:` / `question:` / `nit:` / `praise:`**

**Without them, every comment reads as blocking**, and a review with fifteen comments feels like a rejection even if fourteen are nits. With them, an author triages in thirty seconds. **Four characters.**

---

**Q6.** Review is the wrong tool because **it addresses the instance, not the pattern** — you will mention it eleven times — and it carries an interpersonal cost every time.

**The right tool: the Definition of Done, the linter, or the CI pipeline.** Fixing it once in a config file beats mentioning it eleven times **and removes the interpersonal dimension entirely** — a linter is not a colleague implying you are careless.

---

**Q7.** **May block: 1 formatting, 2 linting, 3 type checking, 5 custom rules** — all deterministic, all right essentially always.

**Must only advise: 4, security and pattern scanning** — because its false-positive rate is moderate to high.

**Why:** **a gate that is wrong two times in five will be disabled**, and then you have neither the gate nor the advice.

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L22 §1–2 |
| **Q3, Q4** | **L23 §1–2** — and print [[CS212 Week7/resources/REVIEW CHECKLIST\|REVIEW CHECKLIST]] before you start A 7 |
| **Q5** | **L23 §4** — A 7 awards 8 marks for labels and **caps the paper at 65 without them** |
| Q6 | L23 §6 — and A 7 Q4 is this, done three times |
| Q7 | L24 §7 |

**Q5 is the one that costs marks this fortnight.** It is the cheapest habit in the week and the one every cohort forgets while actually reviewing.

---

*CS 212 · Week 8 · Quiz 8 · covers Week 7 · ungraded*
