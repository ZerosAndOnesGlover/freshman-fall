# CS 212 · Quiz 1
## Administered: Tuesday, Week 1 (first 10 minutes of lecture)

**Name:** _________________________________ **Team:** ___________ **Date:** ___________

**Covers Week 0** — software engineering as a discipline, the software crisis, process models, and the Agile Manifesto.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room — the point
> is to find out what has not landed while there is still a term left to fix it.
>
> Do not look at the key first. It costs you the only thing the exercise is for.

---

**Q1.** Where and when was the phrase "software engineering" coined, and why did its authors say they chose it?

&nbsp;

&nbsp;

---

**Q2.** Roughly what share of a system's lifetime cost falls after its first release, and roughly what share of *that* is fixing bugs?

&nbsp;

&nbsp;

---

**Q3.** What does Royce's 1970 paper say about the model in its own Figure 2?

&nbsp;

&nbsp;

---

**Q4.** L02 gives an argument for short cycles that does **not** depend on Boehm's cost-of-change curve. State it.

&nbsp;

&nbsp;

---

**Q5.** Quote, as closely as you can, the last sentence of the Agile Manifesto's four values — and say why it matters.

&nbsp;

&nbsp;

---

**Q6.** Knight Capital is used against which of the four Agile value statements, and what is the argument?

&nbsp;

&nbsp;

---

**Q7.** `roomsvc` has 61% line coverage and a 31% mutation score. What are these two numbers measuring, and why are they different?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** The **NATO Science Committee conference at Garmisch-Partenkirchen, October 1968**. The report says the phrase was **"deliberately chosen as being provocative"** — it asserted the *need* for theoretical foundations and practical disciplines like those of established engineering, which software did not then have.

*Half marks for "NATO, 1968" without the provocation. The provocation is the point.*

---

**Q2.** About **60%** of lifetime cost falls after first release. Of that, only about **21% is corrective** — fixing bugs. The rest is **perfective** (~50%, new and changed requirements) and **adaptive** (~25%, the world changed).

*Which is why you are optimising for **changeability**, not for correctness.*

---

**Q3.** He **rejects it**: *"I believe in this concept, but the implementation described above is risky and invites failure"* (p. 329). The rest of the paper proposes five fixes — including **"do it twice"** (build a pilot and throw it away) and **formal customer involvement** — which together describe iterative development.

---

**Q4.** **Roughly two-thirds of delivered features are rarely or never used** — 45% never, 19% rarely, in Standish's 2002 feature data. **No amount of up-front analysis identifies which third matters**, because users cannot reliably predict their own behaviour. The only way to find out is to ship and watch.

*It is a stronger argument than the cost curve because it does not depend on Boehm's numbers being right.*

---

**Q5.** **"That is, while there is value in the items on the right, we value the items on the left more."**

It matters because **every misuse of the document consists of deleting it.** Read without it, the four lines are commandments; read with it, they are trade-offs, and an engineer's job is knowing which side a situation falls on.

---

**Q6.** **"Individuals and interactions over processes and tools."** A deployment was performed by a person, who updated **seven of eight servers**; the eighth ran code in which a repurposed feature flag re-enabled an eight-year-old routine. **$440M in 45 minutes.**

The argument: **the more a task punishes a lapse of attention, the more it belongs to a tool.** Design needs individuals; deployment needs a robot.

*Full credit also for the rebuttal — that the manifesto is about organising a team, not about which tasks to automate, and that its closing sentence already grants the point.*

---

**Q7.** **Line coverage** — the share of lines executed while the tests run: **61%**. **Mutation score** — the share of deliberately introduced bugs that cause at least one test to fail: **31%**.

They differ because **a line can be executed by a test that never asserts anything about what it did.** Coverage measures what was *reached*; mutation measures what was *checked*. **The second is the one that tells you whether the suite would notice a regression.**

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L01 §1–2, §4 |
| **Q3** | **L02 §2** — and actually open the paper; A 0 Q1 requires it |
| Q4 | L02 §5 |
| **Q5, Q6** | **L03 §1–2** — this is the core of the midterm's essay question |
| **Q7** | **L01 §5** — and note it now; **Week 6 is entirely this distinction** |

**Q5 and Q7 are the two that recur.** Q5 is the reading skill the whole course is graded on; Q7 is a fact about your own project you will be marked on in May, where a 30% mutation score at 95% coverage scores below 75% at 70%.

---

*CS 212 · Week 1 · Quiz 1 · covers Week 0 · ungraded*
