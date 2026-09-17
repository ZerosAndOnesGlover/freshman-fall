# CS 212 · Software Engineering
## Week 12: Presentations, Engineering Management, Career Paths

**Credits:** 3 · **Prerequisites:** PROG 102, CS 101
**Assessment for this course (overall):** Team Project 40%, Individual Assignments 30%, Midterm 15%, Final 15%
**This week's deliverables:** **A 11 and A 12 both due Friday 24 April 17:00** · **No quiz — Quiz 11 was the last**

> ## The last teaching week.
>
> **Friday 24 April is the heaviest day of the term**: A 11 and A 12 here, **Problem Sets 11 and 12 in
> every other course**, and **CS 290's Position Paper 3**. None of it can move. **A 12 is deliberately
> short and should take an evening; A 11 is not — it should have been started last week.**
>
> **Then:** 🎤 **Demo Day Tuesday 28 April** · 📄 **code and report Friday 1 May 17:00** ·
> 📕 **Final exam Friday 8 May, 09:00–11:30.**

---

### Why This Week Exists

Because you are about to present thirteen weeks of work to a room, and then write about it, and then be examined on it — and **none of those three is a test of whether the project went well.**

**The demo is 10 marks of 100.** The system is 40, engineering quality is 30, the report is 20. **The stage is worth doing well because a failed demo damages the other 90 by association**, not because that is where the marks are. So this week's first lecture is about the ninety seconds that actually matter — **book a slot, be refused, and say where the guarantee lives** — and about the two minutes that are the most credible you can spend, which are the ones where you say what you got wrong.

**The second lecture is the evidence about teams**, and it lands somewhere uncomfortable: **Google studied 180 of its own teams and found that individual ability did not predict performance. Psychological safety did, by a wide margin.** Which is not a soft coda — **it is what makes a code review possible.** A reviewer who cannot say *"I have read this twice and cannot follow it"* approves it; an author who cannot say *"I do not know if this is right"* does not write it in the description. **Thirteen weeks of assignments awarding marks for that sentence were this finding, applied.**

**And the third is what the course was for**, which comes down to one thing: **you are not optimising for a program that is correct.**

---

### Learning Objectives

By the end of Week 12, you should be able to:

1. Structure a technical presentation for **three audiences who want different things**, in the right order.
2. **Demo the refusal** — and say in one sentence where the guarantee lives.
3. **Show that your tests are worth something**: a mutation score with its line count, the survivors you read, **and a live break that a test catches.**
4. Say what you got wrong, **specifically enough that it is a finding rather than a formula.**
5. State **Brooks's arithmetic** — four people is 6 pairs, five is 10 — and name the mechanism that three separate literatures agree on.
6. State **Project Aristotle's finding** with its caveats, and explain why psychological safety is a precondition for code review rather than a nicety.
7. Explain why **estimation fails structurally**, and give four things that work better.
8. Run a **blameless post-mortem** in five sections, and explain why **human error is a symptom rather than a cause.**
9. Rank which of this course's practices are **unilateral** and which need organisational permission — and **bring evidence rather than principles** for the second kind.
10. Describe the **two senior tracks**, and the feedback-loop difference that makes each hard.
11. Say what the **first two years of a job actually ask for**, and ask the one interview question that reveals an engineering culture.
12. State **the four things this course was for**, and the one sentence.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L37 Presenting Engineering Work]] | **Three audiences, and the demo is 10 of 100**; a fifteen-minute structure with timings; **show the refusal** — thirteen weeks in ninety seconds; **show that your tests are worth something, then break something live**; **why the part where you were wrong is the strongest part**; five slides; and why the report is read more carefully than the demo |
| [[L38 Engineering Management]] | **Brooks measured**; **batch size as the most robust result in the course**, from three literatures; **Project Aristotle — individual ability did not predict, psychological safety did** — and why that is what makes review possible; **why estimation fails structurally**, and four things that work; **blameless post-mortems in five sections**; **which practices are unilateral**; and whether to become a manager |
| [[L39 Career Paths and What This Course Was For]] | **The two tracks and the feedback-loop difference**; what the first two years actually ask for; **the one interview question**; where to go next; **the four things this course was for**; **four originators who disowned their own ideas**; and **the one sentence** |
| [[CS212 Week12/project/DEMO DAY\|DEMO DAY]] | **Tuesday 28 April.** The running order, the two things that matter most, **Monday not Tuesday**, the two published viva questions and their likely follow-ups, and what loses marks reliably |
| [[CS212 Week12/project/FINAL REPORT GUIDE\|FINAL REPORT GUIDE]] | Six sections, what each is marked on, the common failures — **and the two sentences worth writing** |
| [[CS212 Week12/assignments/A 12 Retrospective\|A 12]] | Five questions, 100 points, **1,200–1,600 words**, due Friday 24 April. Two caps, both about honesty |
| [[CS212 Week12/assignments/FINAL EXAM\|FINAL EXAM]] | **Friday 8 May, 09:00–11:30.** Comprehensive, 100 marks, one A4 sheet permitted, **six contested positions** |
| [[CS212 Week12/resources/FINAL EXAM Revision Guide\|FINAL EXAM Revision Guide]] | **How to revise this course in six hours**, what the paper looks like, the ten things Section A asks about, **how to build the A4 sheet**, and the cross-week connections the paper rewards |
| [[CS212 Week12/resources/Reading Guide Week 12\|Reading Guide Week 12]] | Forty minutes this week; **three books for after 1 May**; what not to read for a year; and the habit that compounds |
| `solutions_instructor/` | Instructor only — final exam mark scheme and A 12 |

---

### The One Thing to Take From This Week — and From the Course

> **You are not optimising for a program that is correct. You are optimising for a program that can be
> changed by someone who did not write it, years after you have left — and every technique in this
> course is a way of buying that.**

**`roomsvc` is what it costs when nobody buys it.** `confirm_booking` was correct for most inputs. It was 487 lines, complexity 94, eleven tests against ninety-four paths, with 78% of its surviving lines written by somebody who left in 2023. **When it turned out to be wrong, the fix was twelve lines and it took four months** — not because the fix was hard, but because **nobody could convince themselves that touching it was safe.**

**Two lectures in one room, on 14 October 2024.**

Everything in thirteen weeks has been an answer to that sentence: the invariant written down, cohesion, the placement at the narrowest point every path must pass through, tests whose passing is evidence, a second reader, a pipeline that verifies, characterisation tests before you touch anything. **Eight weeks of apparatus to make an afternoon possible** — which is the bill for **60% of lifetime cost falling after first release**, and only about a fifth of that being bug-fixing.

---

### Assessment Reminder

**There is no Quiz 12.** Quiz 11 was the last, and **Weeks 11 and 12 are examined only on the final.**

| | |
|---|---|
| **A 11 + A 12** | **Friday 24 April, 17:00.** The lowest of the thirteen assignments is dropped |
| 🎤 **Demo Day** | **Tuesday 28 April**, TH 200. 15 min + 5 for questions. **Deploy on Monday** |
| 📄 **Code and report** | **Friday 1 May, 17:00.** 3,000–4,000 words, plus peer assessment |
| 📕 **Final exam** | **Friday 8 May, 09:00–11:30.** One A4 sheet of your own handwritten notes |

> **The two viva questions have been published since Week 6**: *what shape did you choose and what did
> it buy, for whom?* and *if someone broke your main rule, which test would fail?* **Preparing for them
> is most of what the project was trying to make you do.**

---

### Connections

**Back:** **the whole course.** L39 §4 collects it: code you cannot change safely is worthless however correct; every practice is a claim about cost, in a context, with evidence; instrument what you intend to act on, and act on it; and the hard part is other people, and it is mostly mechanical. **W12 L38 §2's psychological safety is the reason A 2 through A 10 each awarded marks for saying what you were unsure about** — that was not a formatting requirement.

**Sideways:** **CS 202's Week 12 is security and synthesis**, and its course closes the same week. **CS 290's Position Paper 3 is due the same Friday as A 11 and A 12.** **PROG 202's Project 2 is due 1 May**, alongside your report and CS 202's Project 2 — **that Friday is the heaviest of the year and none of it moves.**

**Forward:** **CS 311 is the best place in the degree to practise reading unfamiliar code**; **CS 321/331 is where W3 L12's distributed-systems bill is paid in full**; and **the capstone is where this course's apparatus is either used or missed, at four times the scale.** After that: Feathers in your first fortnight, Ousterhout when you have opinions to test, *Software Engineering at Google* when you have been somewhere long enough to be irritated by something — **and a decision log of your own, read a year later.**

---

*CS 212 · Week 12 · the last teaching week · © CSE Department*
