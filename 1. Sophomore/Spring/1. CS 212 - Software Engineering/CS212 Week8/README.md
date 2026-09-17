# CS 212 · Software Engineering
## Week 8: Continuous Integration and Deployment

**Credits:** 3 · **Prerequisites:** PROG 102, CS 101
**Assessment for this course (overall):** Team Project 40%, Individual Assignments 30%, Midterm 15%, Final 15%
**This week's deliverables:** **A 7 due Friday 27 March** · **A 8 released Wednesday** · **📊 Quiz 8 Tuesday** (covers Week 7)

> **First week back from Spring Break.** Week 8 opens Monday 23 March. **A 7 is due Friday 27 March** —
> if your review partner has not opened a pull request, **tell the instructor on Monday**, not on the
> deadline. A pair that fails can be re-paired; a pair that reports on the 27th cannot.
>
> CS 202 holds its Midterm 2 this Monday evening. Nothing in this week's work is due before Friday.

---

### Why This Week Exists

Because Knight Capital lost **$440 million in 45 minutes** to a deployment that reached seven servers out of eight.

**Not a coding error.** The new order router was correct. It was deployed by a person, over a week, to eight production hosts, and **one of them did not get it.** That host still ran code in which a **repurposed feature flag** now switched on a routine called Power Peg — dead for eight years, never deleted — which sent orders without counting fills. **Alerts fired at 08:01, ninety-seven minutes before the market opened**, saying "Power Peg disabled", and nobody knew what that meant.

**Five failures, and the answer to two of them is nine lines of YAML:** assert that every deployment target reports the commit SHA you just built. **That is the whole of L27 §4**, and its absence is the most expensive missing pipeline step on record.

**The week's other half is the practice, not the tooling.** Continuous integration is *integrating daily* — the build is only the verification. **A team with a green badge and four branches that have not merged for a fortnight does not have CI**, and the test takes ten seconds: `git log --oneline main --since='7 days ago' | wc -l`, and how old is your oldest open branch.

---

### Learning Objectives

By the end of Week 8, you should be able to:

1. State Fowler's definition of CI and identify the **two load-bearing words** — and run the ten-second test on your own team.
2. Name the **five of Fowler's ten practices** that do the work, and say why *"fix a broken build immediately"* is the cultural one that matters most.
3. Explain why long-lived branches cost **semantic drift** rather than merge conflicts, and **merge unfinished work three ways.**
4. Give the two feature-flag rules that Knight Capital violated.
5. Explain why **build speed decides everything**, and what a team does at each of the four time bands — including why over 30 minutes the pipeline becomes the obstacle to the practice it exists for.
6. Design a **two-speed pipeline**, and say which checks may block and which must only advise.
7. State **DORA's four metrics**, the counter-intuitive finding, **the batch-size mechanism that explains it**, and two honest caveats.
8. Say what a container **is** — namespaces, cgroups, a union filesystem — and four things it does **not** buy.
9. Name the **five reasons "works on my machine" survives Docker**, and fix each.
10. Write a Dockerfile with the **five decisions**: layer order, multi-stage, non-root, no baked config, healthcheck.
11. Explain **build once, tag with the SHA, promote that image** — and why rebuilding for production is dangerous.
12. Run migrations safely: **a separate step, backward-compatible with running code — five deploys to rename a column — and reversed at least once.**

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L25 Continuous Integration the Practice and the Server]] | **CI is a practice, not a server** — with the ten-second test; the five practices that do the work; **semantic drift and three ways to merge unfinished work**; **why build speed decides everything**, with `roomsvc`'s 94 s of tests inside a 6:40 pipeline; **the two-speed pipeline**; **DORA's four metrics and the batch-size mechanism**, with two caveats |
| [[L26 Docker and the Image You Ship]] | What a container **is**, and four things it does not buy; **five reasons "works on my machine" survives** — including the volume mount that means you have been testing local files; **a Dockerfile worth copying, with all five decisions annotated**; Compose's three load-bearing lines; **build once, promote that image**; **migrations, which are the hard part — five deploys to rename a column** |
| [[L27 Deployment and How to Fail Safely]] | Delivery against deployment; **Knight Capital in full, five failures with five cheap answers**; environments, and why staging cannot be made faithful; **deployment verification — nine lines of YAML for the eighth server**; strategies, and why **reversal time** is what matters; observability added **before** the incident; **an alert must say what to do** |
| [[CS212 Week8/project/DEPLOYMENT CHECKLIST\|DEPLOYMENT CHECKLIST]] | A 8's specification now, **and what stands between you and a working demo on 28 April** — including having a recording |
| [[CS212 Week8/assignments/QUIZ 8 Week 8 Tuesday\|QUIZ 8]] | Seven questions on Week 7, ten minutes, with its own answer key |
| [[CS212 Week8/assignments/A 8 Build a CI Pipeline\|A 8]] | **Almost every mark is for something that runs.** Five questions, 100 points, due Friday 3 April. Two automatic caps |
| [[CS212 Week8/resources/Reading Guide Week 8\|Reading Guide Week 8]] | **Read the SEC filing** — twelve pages, forty minutes, and the best value in the week; plus an honest note on why this week's evidence is unusually good |
| `resources/ci-gate.yml`, `resources/ci-sweep.yml` | The two workflows, fully commented, with every non-obvious line explained |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Deployment is vigilance, not judgement — and vigilance belongs to a machine.**

W0 L03 §2 said *"individuals and interactions over processes and tools"* is the wrong instruction for deployment, and this is the week that shows why in detail. Every one of Knight Capital's five failures is a failure of **attention** rather than of skill: a step missed on the eighth host, dead code nobody's job removed, a flag name reused, no check that the hosts agreed, an alert nobody could act on. **Competent people, a normal process, and $440M.**

**A machine does not skip the eighth host.** It does not get tired at 17:40 on a Friday, does not assume the last one is the same as the first seven, and does not need to be reminded. **Nine lines of YAML asserting that every target reports the SHA you just built is not a sophisticated engineering artefact** — it is the cheapest thing in this week, and its absence ended a firm.

**And notice that the same disease has now appeared four times in eight weeks.** Flaky tests that get re-run (W5). Linter rules everyone dismisses (W7). A nightly sweep nobody reads (W8). An alert that fires and means nothing (W8). **Every one is a signal that stopped carrying information, and every one was tolerated because tolerating it was cheaper than fixing it that day.** That is the mechanism by which engineering discipline decays, and it is worth recognising by name.

---

### Assessment Reminder

**Quizzes carry no weight. The project carries 40%.** Quiz *N* covers Week *N−1*, ten minutes at the start of **Tuesday's** lecture in Weeks 1–11, with its own key printed. Tracked in [[_CS 212 Quiz Record]].

**Assignments** released Wednesday 17:00, due Friday 17:00 of the week after; **lowest of thirteen dropped.** **A 7 is due this Friday, 27 March.** A 8 is released Wednesday and is due Friday 3 April.

> **A 8's two caps are both about the same thing.** **No linked green gate run caps the paper at 50** —
> this assignment is about things that run, and a described pipeline is not one. **A sweep that blocks
> merges caps at 75**, because it inverts L25 §5's principle and will be disabled within a fortnight,
> which is the exact failure the split exists to prevent.

---

### Connections

**Back:** **Week 7's five automation layers become a property of the repository this week** — L24 §7's *"never block on a probabilistic check"* is L25 §5's gate/sweep split, in a pipeline. **W3's architecture test** and **W6's mutation run** each get a home: one in the gate, one in the sweep. **W5's session-scoped Postgres** is why the gate can afford real integration tests at all, and **W1's walking skeleton** is the post-deployment smoke test.

**Sideways:** **CS 202's Week 10 is virtualization** and its **Week 12 covers `seccomp`** — namespaces and cgroups are kernel features, and a container is a configuration of them rather than a new kind of thing. **The two courses are describing the same mechanism from opposite ends**, and reading L26 §1 next to CS 202's hypervisor lecture is worth the twenty minutes.

**Forward:** **Week 9's refactoring depends entirely on a pipeline people are willing to wait for** — a team at eight minutes will stop running it during exactly the work that most needs it. **Week 10's API versioning is L26 §7's expand-and-contract applied to a public interface** instead of a schema. **Week 11** reads the pipeline's history as data. **And the demo on 28 April is a deployment**, which is why the checklist in `project/` has a section about the week before.

---

*CS 212 · Week 8 · © CSE Department*
