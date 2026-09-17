# CS 212 · Software Engineering
## Week 7: Code Review

**Credits:** 3 · **Prerequisites:** PROG 102, CS 101
**Assessment for this course (overall):** Team Project 40%, Individual Assignments 30%, Midterm 15%, Final 15%
**This week's deliverables:** A 6 due Friday 17:00 · **A 7 released Wednesday** · **📊 Quiz 7 Tuesday** (covers Week 6) · **a reviewable pull request open by Friday**

> **⚠️ Spring Break follows this week** — Monday 16 March, no classes. **Week 8 opens Monday 23 March.**
> A 7 therefore gets sixteen days rather than nine, and **the extra time is spent waiting for other
> people**: you need a classmate's pull request to exist, and they need yours. **A 7's pairings are
> posted Wednesday; your PR must be open by Friday 13 March.**

---

### Why This Week Exists

Because the number everyone quotes about code review is a number about something you have never done.

**"Review finds 60% of defects"** comes from Fagan inspection at IBM in the 1970s: three to six people, hours of individual preparation, a reader paraphrasing the code aloud while the author stays silent, **150 lines per hour**, defects logged rather than solved, and a separate follow-up stage. **Now compare a pull request** — one reviewer, no preparation, five minutes, several hundred lines. Same name, different activity.

**And when someone measured the modern version, the answer was more interesting than the slogan.** Bacchelli & Bird classified 570 review comments at Microsoft: developers rank **defect finding first** among what they expect from review, and it accounts for about **14%** of what actually happens — behind code improvements at **29%**. The real value is knowledge transfer, team awareness and readability, **and nobody lists those when asked.**

**So the reframe is the week's point.** Review is not a bug filter with a 60% pass rate. **It is how a codebase acquires more than one reader** — and `roomsvc`'s bus factor on `bookings.py` is 1, with 78% of the surviving lines written by someone who left in 2023. The four-month fix was not four months of engineering. **It was four months of nobody being willing to touch a file they had never read.**

---

### Learning Objectives

By the end of Week 7, you should be able to:

1. Describe **Fagan inspection** as specified, and say why its 60% figure does not transfer to a pull request.
2. State what **Bacchelli & Bird** found about the gap between what review is expected to do and what it does.
3. Give **four reasons for review that survive the evidence**, only one of which is defect detection.
4. Cite the **size evidence** — Cisco's 200-line and 60-minute thresholds, Google's ~24-line median — and give **three mechanisms** by which large reviews fail.
5. Count review's **costs**, including latency, and say why **PRs awaiting review are work in progress.**
6. State the **standard for approval**, and why *"is this how I would have written it?"* is not it — while still **pushing back hard on design.**
7. Work the **five-pass checklist in order**, and say why the order is the content.
8. Name **four things never to comment on**, and the principle behind all four.
9. **Label comment severity** — `blocking:` / `question:` / `nit:` / `praise:` — and say what happens without labels.
10. Be reviewed well: small changes, a description saying what you are **unsure about**, self-review, respond to everything, **and disagree when you disagree.**
11. Handle the **three hard cases**: "rewrite this", "I don't understand this", and a recurring mistake.
12. Build the **five automation layers**, say which may block and which must only advise, and **name what no tool can check.**

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L22 What Review Is For and What the Evidence Says]] | **Fagan inspection as specified, against a pull request**; **Bacchelli & Bird's 570 comments** and the expectation gap; four reasons that survive — starting with `roomsvc`'s bus factor of 1; **the size evidence from Cisco and Google**, and why big reviews fail; the costs, including latency — **and why A 7 exists in a course with no TA** |
| [[L23 A Checklist With Teeth]] | **The standard: definitely improves code health, even if imperfect**; the five passes **in order**, because reviewers left alone never reach design; **the single best question — is there a test that fails without this change?**; four things never to comment on; **five rules for writing a comment, including the four-character severity labels**; being reviewed; three hard cases |
| [[L24 Automated Review and Its Limits]] | **Automation as a budget reallocation**, not rigour; the five layers cheapest-first, **with custom rules as the one nobody does and the highest-value**; what type checking buys, and why the 15% figure is about JavaScript; where scanners earn and where they waste; **seven things no tool can check — including the race that passes all five layers**; **never block on a probabilistic check** |
| [[CS212 Week7/resources/REVIEW CHECKLIST\|REVIEW CHECKLIST]] | **Print it.** The five passes, the never-comment list, the labels, the author's half, and the three hard cases, on one page |
| [[CS212 Week7/assignments/QUIZ 7 Week 7 Tuesday\|QUIZ 7]] | Seven questions on Week 6, ten minutes, with its own answer key |
| [[CS212 Week7/assignments/A 7 Review a Classmates Pull Request\|A 7]] | **The review is marked on GitHub.** Five questions, 100 points, due **Friday 27 March**. Two automatic caps |
| [[CS212 Week7/resources/Reading Guide Week 7\|Reading Guide Week 7]] | **Read Fagan's method section before you quote anyone**; and an honest note on how weak this week's evidence is |
| `solutions_instructor/` | Instructor only — marking procedure, since every student reviews a different artefact |

---

### The One Thing to Take From This Week

**If a machine can check it, a human must not.**

A reviewer has under an hour of useful attention, and perhaps forty productive minutes of it. **Every minute spent on an import order, a line break or a naming preference is a minute not spent asking "can two of these run at once?"** — and that question is the one that took `roomsvc` four months.

**This is not a claim that humans are bad at the mechanical checks.** It is a claim about what the scarce resource is. Formatting, linting, type checking, dependency audits and your own custom architecture rules are all free, tireless, consistent and — the part that is under-rated — **socially neutral**. A linter rejecting an unused import is not a colleague implying you are careless, which is why *"they keep making the same mistake"* is answered by a config file rather than a conversation.

**And the payoff is at the other end.** The seven things in L24 §5 that no tool can check — whether the requirement is right, whether the responsibility is placed right, whether an abstraction has a second case, **whether the code is comprehensible to someone who did not write it** — are exactly the things this course has been about since Week 0. **Automation does not replace the reviewer. It is what makes the reviewer affordable.**

---

### Assessment Reminder

**Quizzes carry no weight. The project carries 40%.** Quiz *N* covers Week *N−1*, ten minutes at the start of **Tuesday's** lecture in Weeks 1–11, with its own key printed. Tracked in [[_CS 212 Quiz Record]].

**Assignments** released Wednesday 17:00, due Friday 17:00 of the week after; **lowest of thirteen dropped.** A 6 is due this Friday. **A 7 is released Wednesday and is due Friday 27 March**, after the break.

> **A 7 has a hard deadline before the deadline.** Pairings are posted Wednesday 17:00; **each of you
> must have a reviewable pull request open — 80–400 lines, green in CI, with a description — by
> Friday 13 March.** If your partner has not opened one by Monday 23 March, **tell the instructor that
> day.** A pair that fails is re-paired; a pair that reports on 27 March cannot be.

**The review is marked from GitHub, not from your PDF**, and the mark is for the review you give. **A terse approval caps the paper at 45.**

---

### Connections

**Back:** **Week 6's survivors are what a reviewer should be looking for** — Google's practice of surfacing mutants on changed lines as review comments (W6 L21 §5) is L24 §7's model. **W5 L16 §4's structure-coupled test** is now a checklist item: *do the tests assert the result or the route?* **W3 L11 §1's architecture test** turns out to be the layer-5 custom rule that nobody writes and everybody should, and you already wrote one in A 3.

**Sideways:** **CS 202's Week 7 is file systems**, and its Project 1 lands this week — which is worth knowing when you schedule your pull request, because both courses want your attention on the same Friday. **PROG 202's Project 1 is due Friday 13 March**, the same day your A 7 pull request must be open.

**Forward:** **Week 8 turns the five layers from a local convention into a property of the repository**, and answers Knight Capital's eighth server. **Week 9's refactorings are exactly the changes that most need a second reader**, because they touch code nobody understands. **Week 11** asks what your review history shows — and the final report is marked partly on it. **Week 12's retrospective** asks what your review practice changed, which is why A 7 Q5(b) demands a change to the practice rather than a resolution to try harder.

---

*CS 212 · Week 7 · © CSE Department*
