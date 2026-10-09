# CS 212 · Software Engineering
## Week 7 · Lecture 1 of 3
### What Review Is For, and What the Evidence Actually Says

*“Given enough eyeballs, all bugs are shallow.”* — Eric S. Raymond, *The Cathedral and the Bazaar* (1997), naming it "Linus's Law"

---

**Sat:** Tuesday of Week 7, 10:00–10:50, TH 200 · **⚠️ Quiz 7 in the first ten minutes** — covers Week 6 · **Reading:** Bacchelli & Bird (2013) · **Next:** L23, the checklist

**Coursework:** 📊 **Quiz 7** today · 📝 **Assignment 7** released Wed this week 17:00, due Fri of Week 8 17:00 · 📝 **Assignment 6** due Fri this week 17:00

---

## 1. The Slogan, and Where It Came From

You will be told that **code review finds 60% of defects**. It is quoted constantly and it is quoted wrongly.

**The number comes from Michael Fagan's work at IBM in the 1970s**, published as *"Design and Code Inspections to Reduce Errors in Program Development"* (IBM Systems Journal, 1976). The figures are real and the studies are good. **They are studies of something you have never done.**

**Fagan inspection**, as specified:

| | |
|---|---|
| **Participants** | 3–6, in a room, with defined roles: moderator, reader, author, tester |
| **Preparation** | Each participant reads the material **alone, beforehand**, for hours |
| **The meeting** | 2 hours maximum. **A reader paraphrases the code aloud, line by line**; the author does not speak first |
| **Rate** | **~150 lines per hour.** Slower for critical code |
| **Output** | A logged defect list, and a **rework** stage, and a **follow-up** to verify |
| **Rule** | **Defects are logged, not solved, in the meeting** |

**Now compare a GitHub pull request.** One reviewer, asynchronous, no preparation stage, no paraphrase, no moderator, often skimmed in five minutes, at a rate of thousands of lines per hour. **These are different activities with the same name**, and transferring Fagan's numbers to the second is the field's most common evidential error.

> **This is not a reason to dismiss modern review.** It is a reason to look at what the evidence for
> *modern* review actually says — which is more interesting than the slogan, and points at a
> different purpose.

---

## 2. What Modern Review Actually Achieves

**The key study is Bacchelli & Bird, *"Expectations, Outcomes, and Challenges of Modern Code Review"* (ICSE 2013)** — Microsoft, observations, interviews, surveys, and a classification of **570 review comments**.

**What managers and developers *expected* review to do:**

| Expectation | Rank |
|---|---|
| Finding defects | **1st** |
| Code improvement | 2nd |
| Alternative solutions | 3rd |
| Knowledge transfer | 4th |
| Team awareness | 5th |

**What the 570 comments actually were:**

| What reviewers actually commented on | Share |
|---|---|
| **Code improvements** — readability, naming, structure, conventions | **~29%** |
| **Defects** | **~14%** |
| Knowledge transfer | ~9% |
| Alternative solutions | ~7% |
| Everything else — praise, questions, process | ~41% |

**Defect finding is fourth or fifth in practice and first in expectation.** And the defects found are mostly *low-level* — a missed null check, an off-by-one — rather than the design-level problems reviewers believe they are catching.

**The paper's conclusion is the sentence worth memorising:**

> **The main value of modern code review is not defect detection. It is knowledge transfer, team
> awareness, and improved code readability — and those are exactly the things nobody lists when
> asked what review is for.**

---

## 3. So Why Do It?

**Four reasons that survive the evidence**, in the order they matter for your team.

### 1. More than one person has read it

**`roomsvc`'s bus factor on `bookings.py` is 1.** One author, who left in 2023, wrote **78% of the surviving lines**. The four-month fix was not four months of engineering — it was four months of nobody being willing to touch a file they had never read.

**Review is the mechanism that stops that happening**, and it is the only one that scales. Documentation decays; pairing does not cover everything; **a reviewed pull request means at least two people have read every line, at the time it was written, when the author could still explain it.**

### 2. It transfers what the codebase knows

A reviewer saying *"we already have a helper for this"* or *"the registrar asked for the opposite last term"* is transferring something that exists nowhere else. **This is the largest real effect in the Bacchelli data and it is invisible in any defect count.**

### 3. It makes code readable by making it read

**Nothing else forces the question.** An author cannot tell whether their code is readable, because they have the context. A reviewer who has to ask *"what is `s` here?"* has produced evidence that no amount of self-review can.

### 4. It is a choke point where a check can be applied

Not the human part — the *position*. **A review is the one moment when every change passes through a gate**, which is where you put the architecture test, the coverage-of-diff check, the mutation survivors (W6 L21 §5), and the security scan. **Week 8 automates all of them**, and the reason they can be automated is that review created the checkpoint.

> **The reframe worth carrying:** **review is not a bug filter with a 60% pass rate. It is how a
> codebase acquires more than one reader, and how a team's knowledge gets into more than one head.**
> Judge your team's reviews by that standard and they will look different.

---

## 4. What the Evidence Says About How to Do It

**This part is better evidenced than the "why", and it is mostly one variable: size.**

**The SmartBear/Cisco study** (Cohen et al., 2006), 2,500 reviews of 3.2 million lines at Cisco, is the largest dataset on modern-style review:

| Finding | Number |
|---|---|
| **Defect density falls sharply above ~200 lines** under review | Below 200 LOC, ~10–15 defects found per 1,000 lines; above 400, **almost none** |
| **Effectiveness collapses beyond 60 minutes** of reviewing | Attention, not code |
| **Review rate should be under ~500 lines/hour** | Faster finds nothing |
| **Authors who annotate their own diff find more defects** — *before anyone else looks* | The "checklist effect" of having to explain |

**Google's internal data** (Sadowski et al., *"Modern Code Review: A Case Study at Google"*, ICSE-SEIP 2018), over ~9 million reviewed changes:

| | |
|---|---|
| **Median change size** | **~24 lines** |
| Changes with **one** reviewer | ~80% |
| Median time to first response | **under an hour** |
| Median time to approval | **under 4 hours** |

**The lesson from both is identical and it is not about people:**

> **Small changes, reviewed quickly, by one person.** A 24-line change reviewed in an hour is worth
> more than a 900-line change reviewed by three people over four days — and the 900-line review will
> find fewer defects **in absolute terms**, not just per line.

**Why big reviews fail** is worth spelling out, because you will be tempted to submit one:

1. **Attention is the binding constraint**, and it is exhausted in under an hour.
2. **A large diff cannot be held in working memory**, so a reviewer checks local properties — naming, style — and cannot check whether it is *right*.
3. **Social pressure rises with size.** Rejecting 40 lines is a suggestion; rejecting 900 lines is telling someone their week was wasted. **Reviewers approve big changes.**

---

## 5. The Cost, Which Is Rarely Counted

**Review is not free** and a team that pretends otherwise ends up resenting it.

| Cost | |
|---|---|
| **Reviewer time** | Roughly 10–15% of engineering time in organisations that do it properly |
| **Latency** | A change waiting for review is a change not integrated. **This is where WIP limits and Little's Law bite** (W0 L02 §7) — a team with four PRs open and nobody reviewing has four times the cycle time |
| **Context switching** | Both ways. The reviewer interrupts their work; the author has moved on by the time comments arrive |
| **Interpersonal** | §L24. The cheapest cost to reduce and the least-managed |

**The latency cost is the one that damages student teams most**, and it has a specific shape: everybody writes, nobody reviews, four branches drift for a fortnight, and the integration crisis arrives in April. **Your charter's WIP limit should count PRs awaiting review as work in progress**, because they are.

> **The rule that fixes it, and it costs nothing: review before you write.** When you sit down to
> work, look first at whether anything is waiting for you. **A team of four where everybody does
> this has a median review latency of a few hours; a team where nobody does has a median of days.**

---

## 6. What This Means for A 7

**A 7 is a peer review of a classmate's pull request, against the checklist in L23.** It is worth restating why the assignment exists in this form.

**This course has no TA** (syllabus §9). Nobody reviews your pull requests but your own team — who share your assumptions, your vocabulary and your blind spots. **A 7 is the one point in the term where someone outside your team reads your code**, which is both the week's topic and the answer to the staffing gap.

**It is also the closest thing to the real test.** W0 L01 §4: you are optimising for code that can be changed by someone who did not write it. **A classmate from another team, reading your pull request cold, is exactly that person** — and their questions are data about your code, not about them.

> **Which means the mark for A 7 is on the review you give, not the code you wrote.** A thoughtful
> review of a weak PR scores highly. A terse "LGTM" on a good one does not.

---

## 7. Summary

- **"Review finds 60% of defects" comes from Fagan inspection at IBM in the 1970s** — 3–6 people, hours of solo preparation, a paraphrasing reader, **150 lines per hour**, logged defects and a follow-up stage. **You have never done this.**
- **Bacchelli & Bird (ICSE 2013), 570 comments:** defect finding is expected first and delivers ~14%, behind **code improvements at ~29%.** The real value is **knowledge transfer, team awareness and readability** — none of which anyone lists when asked.
- **Four reasons that survive:** more than one person has read it (`roomsvc`'s bus factor is 1, and 78% of `bookings.py` belongs to someone who left in 2023); knowledge transfer; readability made observable; **and a choke point where checks can be applied** — which is what Week 8 automates.
- **How to do it is better evidenced than why**, and it is one variable: **size.** Cisco: defect density collapses above 200 lines and effectiveness collapses after 60 minutes. Google: **median change ~24 lines, one reviewer, first response under an hour.**
- **Big reviews fail** because attention is exhausted, a large diff exceeds working memory, and **social pressure means reviewers approve them.**
- **The cost is real**: 10–15% of engineering time, plus latency — **and PRs awaiting review are work in progress.** The fix is free: **review before you write.**
- **A 7 exists because this course has no TA**, and a classmate reading your code cold is exactly the reader you are optimising for. **The mark is on the review you give.**

**Next:** L23 — the checklist. What to look for, in what order, and the four things never to comment on.

---

*CS 212 · Week 7 · L22 · © CSE Department*
