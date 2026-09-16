# CS 212 · Software Engineering
## Week 6: Coverage, Property-Based Testing, Mutation Testing

**Credits:** 3 · **Prerequisites:** PROG 102, CS 101
**Assessment for this course (overall):** Team Project 40%, Individual Assignments 30%, Midterm 15%, Final 15%
**This week's deliverables:** **🎤 Phase 1 Tuesday 3 March (10%)** · **📘 Midterm Wednesday 4 March, 18:00–19:15 (15%)** · A 5 due Friday 17:00 · **A 6 released Wednesday** · **📊 Quiz 6 Tuesday**

> ## The heaviest week of the term.
>
> **Tuesday 3 March:** Quiz 6 at 10:00, then **Phase 1 presentations** in TH 200.
> **Wednesday 4 March:** lecture at 10:00, **A 6 released at 17:00**, **midterm at 18:00–19:15**
> covering Weeks 0–5. ECE 211's Midterm 1 is the same evening at 20:00.
> **Friday 6 March:** A 5 due, along with Problem Set 5 in every other course.
>
> **None of it can move** — every date is in the registry. **A 6 is the lightest assignment of the
> term for this reason**, and the Phase 1 rubric puts 70 of its 100 marks on artefacts that are
> already in your repository.

---

### Why This Week Exists

Because you have been carrying two numbers since Week 0, and this is where they are reconciled.

**61% line coverage. 31% mutation score.** The gap between them is the gap between a test that *ran* and a test that *checked*, and it is made of exactly three things: tests with no assertions, tests that assert the route instead of the result, and branches covered one way only.

**And the third one has a name you already know.** Run mutation testing on `roomsvc` and one of the 802 survivors is this:

```python
- if existing:
+ if not existing:
# SURVIVED
```

**That is the VNC 101 bug, generated automatically as a mutant, run against all 212 tests — and every one of them passed.** A tool that knows nothing about rooms or calendars reproduced the 2024 incident in a fraction of a second and demonstrated that the suite would ship it. **That is the most direct statement available of what "61% coverage" was worth.**

**The week's third tool finds the bug you would never have written a test for.** Hypothesis, given `slot`'s recurrence rule and no domain knowledge at all, shrinks its way to a two-occurrence rule starting **01:30 on 29 March 2026** — the morning the clocks go forward, when 01:30 does not exist. **That is `roomsvc` issue #31, open since August 2020.**

---

### Learning Objectives

By the end of Week 6, you should be able to:

1. **Construct a suite with 100% line and branch coverage and no assertions**, and say what that proves.
2. Enable **branch coverage**, and say why it takes `roomsvc` from 61.0% to 48.3% and where the difference lives.
3. Name the **one question coverage answers well**, and the three legitimate uses — untested regions, **diff coverage**, and a **ratchet**.
4. Explain why a coverage **target** is Goodhart's law in textbook form, and name four rational ways to hit one that improve nothing.
5. State what **Inozemtseva & Holmes (2014)** controlled for and what happened to the correlation.
6. **Read a coverage report bottom-first**, cross-referenced with change frequency, and say why `BrPart` is the most valuable column and the total the least.
7. List **seven things coverage cannot see at 100%** — including the concurrency bug that *was* in covered code.
8. Write properties in the **five patterns**, and say why **round-trip** gives the most bugs per line.
9. Explain **why shrinking is the feature**, with the DST example.
10. Build a **`RuleBasedStateMachine`** for a booking lifecycle — **and state precisely what it cannot find.**
11. Define the **mutation score**, classify a survivor as a real gap, an equivalent or a deliberate omission, and **prove an equivalence.**
12. State what **Just et al. (2014)** established with 357 **real** faults, why "real" matters, and **why 95/30 scores below 70/75.**

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L19 Coverage What It Measures and What It Cannot]] | **The 100%-covered suite with no assertions**; five kinds of coverage and which to enable; **61.0% → 48.3%**; coverage as diagnostic, diff gate and ratchet; **Goodhart, with the four rational cheats**; **Inozemtseva & Holmes and the suite-size control**; how to read a report bottom-first; **seven things invisible at 100%** |
| [[L20 Property-Based Testing]] | Why examples come from the model that wrote the code; **the five property patterns**; **shrinking, and the 01:30 on 29 March counterexample that is issue #31**; where it fits and where it does not; **the state machine for `slot`'s lifecycle, and the one thing it cannot find**; adopting three properties without losing a week |
| [[L21 Mutation Testing]] | **61% and 31% reconciled, with three survivors** — and **the third is the VNC 101 bug, surviving 212 tests**; equivalent mutants and why 100% is not a target; **Just et al. on 357 real faults**; making it tractable; **five things it cannot see**; why 95/30 scores below 70/75 |
| [[CS212 Week6/project/PHASE 1 RUBRIC\|PHASE 1 RUBRIC]] | **70 marks in the repository, 30 on stage.** The two viva questions, published in advance; what loses marks reliably; and what to do first if you are behind on Monday |
| [[CS212 Week6/assignments/MIDTERM\|MIDTERM]] | **Wednesday 18:00–19:15, 100 marks, Weeks 0–5.** Three sections, one A4 sheet permitted, **four questions where disagreeing with the lectures scores full marks** |
| [[CS212 Week6/assignments/QUIZ 6 Week 6 Tuesday\|QUIZ 6]] | Seven questions on Week 5 — **and its answer-key table doubles as tonight's revision list** |
| [[CS212 Week6/assignments/A 6 Coverage Properties and Mutants\|A 6]] | **The lightest assignment of the term.** Five questions, 100 points, due Friday of Week 7 |
| [[CS212 Week6/resources/Reading Guide Week 6\|Reading Guide Week 6]] | Short, and **the two papers that justify the marking rule** — with a twenty-minute method for each, the night before the midterm |
| `solutions_instructor/` | Instructor only — midterm mark scheme and A 6 |

---

### The One Thing to Take From This Week

**A mutation tool generated the VNC 101 bug, ran 212 tests against it, and all 212 passed.**

Not a simulation of the bug. The mutation `if existing:` → `if not existing:` in `confirm_booking` is, precisely, the guard that failed on 14 October 2024 — and the test suite that was green on that day is green on the mutant too.

**Everything in this week follows from that one observation.** Coverage said 61% and was measuring something real and useless. The tests were executed and did not check. **And the tool that revealed it costs one command and a nightly CI job.**

**So the rule this course marks on is not arbitrary.** *95% coverage with a 30% mutation score scores below 70% coverage with a 75% mutation score*, because Just et al. took 357 faults that actually shipped and found that mutant kill rate predicts detecting them **after controlling for coverage**, while Inozemtseva & Holmes found coverage's own correlation vanishes once you control for how many tests there are.

**One number tells you a line ran. The other tells you somebody would notice.**

---

### Assessment Reminder

**Quizzes carry no weight. Phase 1 is 10% and the midterm is 15%** — a quarter of the course, in two days.

**Quiz 6** runs at 10:00 Tuesday, ten minutes, before the presentations, with its own key printed; **its "what to reread" table is built as the midterm revision list.**

**Phase 1:** Tuesday 3 March, TH 200, ten minutes per team plus five for questions. **70 of 100 marks are assessed from a clone taken at 09:00** — see the rubric. The **two viva questions are published**: what shape did you choose and what did it buy, *for whom*; and **if someone broke your main rule, which test would fail?**

**Midterm:** Wednesday 4 March, 18:00–19:15, 75 minutes, 100 marks, Weeks 0–5. **One A4 sheet of your own handwritten notes is permitted.** Section C is one essay of three.

**A 5** is due Friday and is marked from your commit history. **A 6** is released Wednesday 17:00 and is deliberately light.

---

### Connections

**Back:** **Week 0 §5's two numbers are settled here** — they have been sitting in `roomsvc metrics.md` for six weeks waiting for L21. **W5 L17 §5's ten-second habit** — break the code, check the test notices — **is this week's third lecture, automated.** **W5 L16 §4's structure-coupled test** appears again as survivor type 2, exactly as predicted. **W1 L06 §5's missing `Recurrence`** is what Hypothesis finds in under a second.

**Sideways:** **MATH 251's Weeks 4–5 are random variables and expectation**, which is what a mutation score is a statistic *of* — and its treatment of sampling is why "ten survivors" is a sample rather than a census. **CS 202's Week 6 is page replacement**, where the same lesson recurs: a hit rate is a measurement, not a goal, and optimising it directly produces LRU-shaped cheating.

**Forward:** **Week 7's review checklist** asks reviewers to look for exactly the gaps a survivor reveals, and Google's practice — mutate the diff, surface survivors as review comments — is the model. **Week 8** puts the mutation run in a nightly pipeline. **Week 9's refactoring is only safe because of the tests this week measured.** **Week 11** measures the trend rather than the number. **The final report is marked on these figures**, with the line count beside them.

---

*CS 212 · Week 6 · © CSE Department*
