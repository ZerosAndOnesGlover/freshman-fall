# CS 212 · Team Project
## `slot` — A Room and Equipment Booking Service

---

**Teams:** 4–5, formed in the Week 0 workshop, fixed for the term
**Weight:** 40% of the course — **Phase 1 10%** (Week 6), **Final 30%** (Fri 1 May, 17:00)
**Stack:** Python 3.12 · FastAPI · PostgreSQL · pytest · Docker · GitHub Actions

---

## 1. The Problem

The department books rooms and equipment with `roomsvc`, which has been in production since February 2020, is 11,438 lines of Python, was written by six people of whom four have left, and **double-booked VNC 101 on 14 October 2024** (L01 §6).

**You are building its replacement.** Not a prototype — a system another team could pick up in Week 7 and work on, which is the actual test and which Week 7 actually applies.

**You are not expected to match `roomsvc`'s feature set.** It has six years of accreted features and roughly two-thirds of them are never used (L02 §5). **Choosing what not to build is part of the assessment**, and Week 1 is where you justify the choice.

---

## 2. The Domain, As Given

This much is fixed, so that every team is solving the same problem and A 7's peer review is possible across teams. **Everything else is yours to decide.**

| Concept | What it is |
|---|---|
| **Resource** | A bookable thing. Rooms (TH 200, VNC 101, BH 210) and equipment (projector cart, the department's two portable PA kits) |
| **Slot** | A bookable interval. The department books in **50-minute teaching slots** on the hour, 08:00–20:00, Monday to Friday |
| **Booking** | A request by a named user for one resource in one slot |
| **Hold** | A booking that is not yet confirmed. Holds expire |
| **User** | Staff, student, or admin. What each may do is one of the requirements you must pin down |

**The invariant that the old system broke:**

> **A resource has at most one confirmed booking per slot.**

**It must be impossible to violate this in your system**, and "impossible" is assessed. A test that passes is not evidence; a test that passes while two clients POST simultaneously is. Week 5's assignment asks you to write that test, and Week 6's Phase 1 rubric awards marks for the mechanism, not the intention.

---

## 3. What Phase 1 Must Contain (Week 6, 10%)

**Presented Tuesday 3 March, 10 minutes per team, in TH 200.** Rubric in [[CS212 Week6/project/PHASE 1 RUBRIC|PHASE 1 RUBRIC]].

**70 of the 100 marks are for artefacts that are in the repository before you present.** The presentation is 30. This is deliberate: ten minutes of stage time cannot be worth 10% of a course, and the repository is where the engineering is.

| Artefact | Where it lives | Week it was taught |
|---|---|---|
| **User stories with acceptance criteria**, ordered, on the board | GitHub Projects | W1 |
| **A domain model** — entities, relationships, invariants | `docs/domain-model.md` | W1 |
| **Architecture Decision Records**, at least four | `docs/adr/NNNN-*.md` | W3 |
| **A walking skeleton**: one booking created, confirmed and read back, through every layer | the code | **W1** |
| **A green pipeline**: tests, lint and type-check on every push | `.github/workflows/` | W8 (start it in W1 anyway) |
| **A team charter**: Definition of Done, WIP limit, role rotation | `docs/charter.md` | W0 |
| **Three retrospectives** | `docs/retro-1.md` … `retro-3.md` | W0 |

**The walking skeleton is due in Week 1, not Week 6.** It is thin, ugly, and whole — HTTP in, database write, HTTP out, deployed by CI. It exists so that the integration you would otherwise discover in April happens in January instead. **This is the single highest-value thing in the brief and the one most teams defer.**

---

## 4. What the Final Must Contain (Fri 1 May, 30%)

**Demo Day is Tuesday 28 April**, in the completion period. **Code and report are due 17:00 on Friday 1 May.**

| Component | Marks | |
|---|---|---|
| **The system** | 40 | Works, meets the stories you committed to, handles the failure cases you identified |
| **Engineering quality** | 30 | Tests and what they are worth (W5–6), review history (W7), pipeline (W8), the state of the design (W2, W3, W9) |
| **The report** | 20 | 3,000–4,000 words. See §6 |
| **The demo** | 10 | 15 minutes. Live. Something will break; how you handle that is part of it |

**Engineering quality is assessed from the repository, not from claims about it.** Specifically: `git log`, the pull request history, the CI run history, the coverage trend and the mutation score. **A project with 95% coverage and a 30% mutation score scores below one with 70% coverage and a 75% mutation score**, and Week 6 explains why in enough detail that this should not surprise anyone.

---

## 5. Rules

1. **Everything in git, on GitHub, from Week 1.** One repository per team in the course organisation. Private; the instructor has access.
2. **No commit goes to `main` without a reviewed pull request.** From Week 1, before you have been taught review. You will do it badly until Week 7; do it anyway.
3. **Your own code.** Libraries and frameworks are expected — that is engineering. Generated code is permitted **and must be marked as such in the commit message**, with the tool named. Undisclosed generated code is an academic integrity matter under [[UNIVERSITY POLICIES]]; disclosed generated code costs you nothing. **You are responsible for every line you merge, whoever or whatever wrote it**, and "the tool wrote it" is not a defence in a code review, here or anywhere else.
4. **Contribution is tracked and it affects individual marks.** `git shortlog -sn`, the PR history, and the peer assessment submitted with the final report. **A team member with no commits after Week 4 does not receive the team's mark.**
5. **Teams are fixed.** A team in real difficulty should talk to the instructor in Week 3 or 4, not in Week 11.

---

## 6. The Report

3,000–4,000 words, `docs/report.md` in the repository, PDF submitted. Six sections:

| Section | What it must contain |
|---|---|
| **What you built** | Scope, and — with equal weight — **what you deliberately did not build, and why** |
| **Requirements** | The stories, where they came from, and the ones that changed. **A requirement that never changed all term is a requirement you never tested against a user** |
| **Architecture** | The decisions, as ADRs, including **at least one you would now make differently** |
| **Quality** | Coverage, mutation score, review statistics, pipeline timings. Numbers with the command that produced them |
| **Debt** | What you know is wrong and chose to leave. Week 11's method, applied to your own code |
| **Process** | What the six retrospectives changed. **A team whose process never changed did not retrospect** |

**The report is marked on honesty as much as on outcome.** A team that says *"our domain model was wrong and we found out in Week 8; here is what it cost us and here is the migration"* scores above a team that implies it was right all along. Every engineer reading your report has been wrong in exactly this way, and can tell.

---

## 7. Advice From Previous Cohorts

- **The walking skeleton. In Week 1.** Every team that deferred it said the same thing in their retrospective.
- **Decide how you run the thing on day one.** `docker compose up` should work on four laptops by the end of Week 1. Teams lose more time to "it works on mine" than to any design problem.
- **Rotate the backlog owner.** A team where one person decides the order all term learns one person's judgement.
- **Write the retro even in the week where nothing happened.** *Especially* then. Two of the six most useful retrospectives in last year's cohort were about why a fortnight produced nothing.
- **The invariant is the interesting part.** Teams that treat "no double-booking" as an `if` statement discover in Week 5 that it is not. Teams that treat it as a constraint the *database* enforces are done in Week 1 and spend the term on things that are actually hard.

---

*CS 212 · Team Project Brief · 40% of the course · © CSE Department*
