# CS 212 · Software Engineering
## Course Overview and Syllabus · Year 2, Spring

---

**Credits:** 3 · **Prerequisites:** PROG 102, CS 101
**Lectures:** Tuesday, Wednesday, Thursday, 10:00–10:50, **TH 200**
**No laboratory section.** The practical work of this course is the team project.
**Assessment:** Team Project 40%, Individual Assignments 30%, Midterm 15%, Final 15%

> **Read this file in full during Week 0.** It is the only place several things are written down:
> why there is no lab, what the project actually demands and when, why quizzes are unmarked, which
> tool versions the lectures' numbers came from, and where this course deviates from its textbooks.

---

## 1. What This Course Is

**CS 212 is the first course in this degree about software that outlives the person who wrote it.**

Everything before it has been about making a program correct. This one is about the other 60% of the cost — the part that arrives after the first release, when the requirements have moved, the original authors have left, and the code has to be changed by someone reading it cold (L01 §4).

The method is concrete throughout. **The course has a reference codebase, `roomsvc`**, which is the department's real room-booking service: 11,438 lines, six years old, four of its six authors gone. Every principle is applied to it and measured. **And you build its replacement, `slot`, in a team of 4–5, across the whole term.**

**You will write less code than in PROG 201. It will be read much more.**

---

## 2. Assessment

| Component | Weight | Rule |
|---|---|---|
| **Individual Assignments** (A 0 – A 12) | **30%** | Thirteen; **lowest one dropped** |
| **Team Project — Phase 1** | **10%** | Week 6 presentation, Tue 3 March |
| **Team Project — Final** | **30%** | Demo Tue 28 April; code and report Fri 1 May 17:00 |
| **Midterm** | **15%** | Wed 4 March, 18:00–19:15, Weeks 0–5 |
| **Final** | **15%** | Fri 8 May, 09:00–11:30, comprehensive |
| **Total** | **100%** | |

**Quizzes carry no weight.** Eleven of them, Weeks 1–11, ten minutes at the start of **Tuesday's** lecture, closed book, **and each prints its own answer key below the questions.** Sit it, then mark it yourself before you leave. The point is to find out what has not landed while there is a term left to fix it; adding a number would subtract nothing from the misunderstanding. Tracked in [[_CS 212 Quiz Record]].

> **⚠️ Read this sentence twice, because CS 212 differs from every other Year 2 course here.**
> In CS 201, CS 202, PROG 201 and PROG 202 the practical work — the lab — is **unmarked**.
> **In CS 212 the practical work is the project, and it is 40% of the course**: the largest single
> component in any course you take this year. A student who treats it the way a lab is treated
> will fail it.

**Assignments** are released **Wednesday 17:00** and due **Friday 17:00 of the following week**, via the portal. Late penalty begins at 17:01 and follows [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]]. **A 11 and A 12 are both due Friday 24 April**; A 12 is deliberately short.

---

## 3. The Weeks

| W | Topic | Assignment | Project |
|---|---|---|---|
| **0** | Software engineering as a discipline; the software crisis; Agile | A 0 — critical reading | Teams formed; brief issued |
| **1** | Requirements: user stories, use cases, domain models | A 1 | **Charter + walking skeleton** |
| **2** | Design principles: SOLID, DRY, YAGNI, separation of concerns | A 2 | |
| **3** | Architectural patterns: MVC, layered, microservices, event-driven | A 3 | **ADRs** |
| **4** | Design patterns in depth | A 4 | |
| **5** | Testing: unit, TDD, BDD, integration, end-to-end | A 5 | |
| **6** | Coverage, property-based testing, mutation testing | A 6 | **📣 Phase 1 · 📘 Midterm** |
| **7** | Code review; automated review tools | A 7 — peer review | |
| **8** | CI/CD: GitHub Actions, Docker | A 8 | **Pipeline complete** |
| **9** | Refactoring: code smells, Fowler's catalogue | A 9 | |
| **10** | API design: REST, GraphQL, gRPC; versioning | A 10 | |
| **11** | Technical debt; metrics; maintainability; documentation | A 11 | **Debt register** |
| **12** | Presentations; engineering management; career paths | A 12 | **Dress rehearsal** |
| — | *Completion period* | | **🎤 Demo Day Tue 28 Apr · Final due Fri 1 May** |
| — | *Finals* | | **📕 Final exam Fri 8 May** |

---

## 4. Books

**Four, and you need two of them.**

| Book | Status | How to use it |
|---|---|---|
| **Fowler, *Refactoring*, 2nd ed. (2018)** | **Required** | The catalogue of smells and their cures. **Week 9 is this book.** The 2nd edition's examples are JavaScript; the catalogue is language-independent and that is the part you need |
| **Beck, *Test-Driven Development by Example* (2002)** | **Required** | 200 small pages, two worked examples. **Read it in Week 5, in one sitting.** Its value is the *rhythm*, which no summary conveys |
| **Sommerville, *Software Engineering*, 10th ed. (2015)** | Reference | Comprehensive and even-handed on process and requirements — Chapters 1–4 and 9. Weaker on modern practice; its CI chapter predates most of what Week 8 does |
| **Martin, *Clean Code* (2008)** | **Read critically** | Influential and widely disagreed with. **Several of its recommendations are actively bad** — see §7. Read it to know what your colleagues have read |

**Free and worth more than any of them for one week each:** Cockburn's *"Hexagonal Architecture"* (2005), Fowler's bliki, Nygard's *"Documenting Architecture Decisions"* (2011), the *Google Engineering Practices* code review guide (free, google.github.io/eng-practices), and the Twelve-Factor App.

---

## 5. Tools, With Versions

Every number printed in a lecture came from this configuration. **Versions are given because three of these tools changed defaults in a minor release**, and if your coverage figure differs by two points you should be able to find out why rather than assume you did something wrong.

| Tool | Version | Used from |
|---|---|---|
| Machine | Intel i5-8250U, Ubuntu 24.04.4, kernel 7.0 | — |
| Python | **3.12.3** | W1 |
| pytest | **8.2.0** | W5 |
| coverage.py | **7.5.1** | W6 |
| hypothesis | **6.100.1** | W6 |
| mutmut | **2.5.0** | W6 |
| ruff | **0.4.4** | W2 |
| mypy | **1.10.0** | W2 |
| radon | 6.0.1 | W11 |
| Docker | **26.1.3** | W8 |
| git | 2.43.0 | W0 |
| FastAPI / SQLAlchemy / PostgreSQL | 0.111 / 2.0 / 16 | W1 |

**The stack is not a free choice.** Thirteen assignments and a peer-review exercise assume one toolchain; a team on a different one cannot have its pull request reviewed by a classmate in Week 7. If you have a serious reason to deviate, ask in Week 1, not Week 5.

---

## 6. What the Course Assumes, and What It Does Not Teach

**Assumed from PROG 102 and CS 101:** Python to the level of classes, exceptions and modules; basic data structures; the ability to read code you did not write. **Assumed from any course:** that you can use git for your own work — commit, branch, push.

**Not assumed, and taught here:** git *in a team* — branches that other people also touch, merge conflicts on shared files, rebasing, pull requests. **Week 1 spends twenty minutes on this and it is the highest-value twenty minutes in the term for about a third of every cohort.**

**Not taught here, and you will want it:** front-end development. `slot` needs a user interface and the course does not teach you to build one. **Keep it minimal** — server-rendered HTML is entirely acceptable and no marks are given for CSS. A team that spends March on a single-page application has spent March on the one part of the project this course does not assess.

---

## 7. Deviations — Where This Course Disagrees With Its Books

Recorded here because you will notice, and because noticing is the skill.

1. **On *Clean Code*'s function length.** Martin argues functions should be 2–4 lines and "do one thing". **This course does not.** Taken seriously it produces code with a hundred tiny methods whose control flow can only be understood by holding all hundred in your head; the empirical support is absent, and the practice has been criticised at length (see Dan North's *"CUPID"*, 2021). **What this course asks for is the rule Fowler actually gives: extract a function when the extracted part needs a name.** `confirm_booking` is bad at 487 lines for reasons of cohesion, not for reasons of line count.

2. **On comments.** *Clean Code* treats a comment as a failure to make the code clear. **This course treats a comment explaining *why* as a first-class artefact**, because the why is not recoverable from the code and is the first thing lost when authors leave. `roomsvc` is the argument (L01 §6).

3. **On TDD.** Beck's book is required reading and the evidence for test-first over test-soon is **weak and mixed** (L02 §8). **Week 5 teaches the rhythm and states the evidence honestly.** You are assessed on having tests that are worth something, measured in Week 6 — not on the order in which you typed them.

4. **On "100% coverage".** Several tools' defaults and a great deal of industry practice treat coverage as a target. **Week 6 demonstrates a test suite with 100% line coverage and no assertions.** Coverage is a floor and a diagnostic, never a goal.

5. **On microservices.** Much of the industry literature presents them as a maturity level. **Week 3 presents them as a trade that buys independent deployability with distributed-systems problems**, most of which a five-person team does not have and none of which `slot` has. **A team that microservices `slot` will be asked, in the viva, what it bought.**

---

## 8. Academic Integrity

The general rule is [[UNIVERSITY POLICIES]]'s. Two things specific to this course:

**Assignments** are individual. Discuss approaches freely; the writing and the code are yours. Say at the top of every paper who you discussed what with — this has never cost anyone a mark and its absence has.

**Generated code is permitted, and must be disclosed** in the commit message, with the tool named. Disclosed, it costs you nothing — using a tool well is engineering. Undisclosed, it is an integrity matter. **And you own every line you merge, whoever wrote it.** In Week 7 a classmate will review your pull request and ask why a line is there. *"The tool wrote it"* is not an answer here and is not an answer in industry.

---

## 9. Staff

**Spring staff are not yet listed in** [[Year2 - Sophomore/OFFICE HOURS|OFFICE HOURS]], which currently covers Fall only. Until they are: the **Engineering Help Desk, BH 120**, keeps the hours given in that file, and course questions go through the portal.

**This course has no TA**, which has one consequence you should plan around: **nobody reviews your pull requests but your own team, until Week 7 when you review each other's across teams.** Reviewing badly from Week 1 is how you get to review well by Week 7.

---

## 10. How to Pass, and How to Do Well

**To pass:** do the assignments, sit the exams, and contribute visibly to the project. Contribution is measured from `git shortlog`, the pull request history and your teammates' peer assessment. **A student with no commits after Week 4 does not receive the team's mark.**

**To do well:** three things, in order of how much they matter.

1. **Build the walking skeleton in Week 1.** Not Week 3. Every previous cohort's retrospectives say the same sentence.
2. **Make your git history evidence.** Small commits, messages that say *why*, spread across thirteen weeks. It is read at Phase 1 and read again in May, and it is the most honest document your team produces.
3. **Argue with the material.** This course states contested things, marks papers on the quality of disagreement, and puts at least four claims in front of you in Week 0 alone that the literature does not settle. **A 0 is worth 8 marks for finding one.**

---

*CS 212 · Course Overview and Syllabus · Year 2 Spring · © CSE Department*
