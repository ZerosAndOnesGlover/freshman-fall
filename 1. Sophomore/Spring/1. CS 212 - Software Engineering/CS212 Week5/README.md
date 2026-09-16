# CS 212 · Software Engineering
## Week 5: Testing

**Credits:** 3 · **Prerequisites:** PROG 102, CS 101
**Assessment for this course (overall):** Team Project 40%, Individual Assignments 30%, Midterm 15%, Final 15%
**This week's deliverables:** A 4 due Friday 17:00 · **A 5 released Wednesday** · **📊 Quiz 5 Tuesday** (covers Week 4)

> **⚠️ Next week is the heaviest of the term.** **Quiz 6 and the Phase 1 presentation on Tuesday
> 3 March**, and the **midterm on Wednesday 4 March, 18:00–19:15, covering Weeks 0–5.** Everything
> this week's lectures ask for is also a Phase 1 artefact, so the work is not additional.

---

### Why This Week Exists

Because `roomsvc` had 212 tests and they were not evidence.

**61% line coverage. 31% mutation score.** 94 seconds of green ticks, and a fourteen-line fix that took four months, because nobody could convince themselves that touching `confirm_booking` was safe. **The tests existed and did not do the thing tests are for.**

**So the question this week trains is one question, asked of every test you write:** *if someone broke this behaviour, would this test fail?* Week 6 answers it with a tool. This week you answer it by hand, and the answer is uncomfortable more often than you expect — a test asserting `mock.assert_called_once_with(...)` usually passes when the behaviour breaks, because it asserts the route rather than the result.

**And the week has one test in it that is worth more than the other forty.** Two clients, one slot, simultaneously: exactly one 201, exactly one 409, exactly one confirmed row. **It is the acceptance criterion from Week 1 made executable, the invariant from Week 3 made observable, and the incident from Week 0 made impossible.** `roomsvc` never had it. Phase 1 gives marks for it directly.

---

### Learning Objectives

By the end of Week 5, you should be able to:

1. Say what a test is for — **a claim a machine can tell you has stopped being true** — and why the value is in the *stops*.
2. Explain the pyramid's proportions as **consequences** of cost, diagnostic precision and brittleness, rather than as a rule.
3. Give **three honest objections** to the pyramid, and **defend a budget rather than a shape**.
4. Say why **flakiness is not an annoyance but the mechanism** by which a suite stops being believed — and give the operational rule.
5. Distinguish tests coupled to **structure** from tests coupled to **behaviour**, and rewrite one as the other.
6. **Write the concurrency test**, against real Postgres, and say why the transaction-rollback fixture cannot be used for it.
7. Use the **rollback fixture** for everything else, and state its one limitation exactly.
8. Run the **red-green-refactor loop** properly, including watching the red, **faking it till you make it**, and reverting when you have been red twenty minutes.
9. State **what the TDD evidence actually says** — that the benefit tracks small uniform steps rather than ordering — and why that is good news.
10. Name the **five situations where TDD is genuinely hard**, and what to do in each.
11. Choose among the **five test doubles**, explain why mocks are mostly a trap, and demonstrate `Mock()` passing on a typo'd assertion.
12. Adopt **BDD's phrasing and skip its tooling**, and say why the tooling's central premise fails in practice.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L16 The Test Pyramid and What Each Level Buys]] | What a test is for; the pyramid's proportions as consequences; **three honest objections and the budget that replaces the shape**; FIRST's three load-bearing letters; **structure-coupled versus behaviour-coupled tests**; **the concurrency test, and the rollback fixture with its one limitation**; E2E as journeys not cases; **what not to test — and the inverse, which is where the marks are** |
| [[L17 TDD Red Green Refactor Done For Real]] | The loop and the three rules people skip; **a kata in four steps where the transition table emerges at the third test**; **five studies, honestly tabulated, and what the replication actually attributes the benefit to**; five situations where TDD is genuinely hard; **test-after done properly — and the ten-second habit that beats writing twice as many tests** |
| [[L18 Test Doubles BDD and End-to-End]] | The five doubles and state-versus-interaction; **four problems with mocks, including `assert_called_once_wiht` passing silently**; fakes written once, and the drift that argues for the integration test; **BDD's phrasing is free, BDD's tooling mostly is not**; contract tests; **six properties of a trustworthy suite, and zero flaky tests, not few** |
| [[CS212 Week5/assignments/QUIZ 5 Week 5 Tuesday\|QUIZ 5]] | Seven questions on Week 4, ten minutes, with its own answer key |
| [[CS212 Week5/assignments/A 5 Write the Test Suite First\|A 5]] | **Marked from the commit history.** Five questions, 100 points, due Friday of Week 6. Two automatic caps |
| [[CS212 Week5/resources/Reading Guide Week 5\|Reading Guide Week 5]] | **Beck in one sitting, with a terminal open** — the only assigned reading that must be *done*; and what not to read this week |
| `resources/conftest_reference.py` | The session Postgres, the rollback fixture with its limitation spelled out, a frozen clock, and the `-p randomly` settings |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Break the code and check the test notices.**

It takes ten seconds. Comment out a line, flip a `<` to `<=`, change a constant, delete a `raise` — then run the test that is supposed to cover it. **If it still passes, the test is decorative**, and you have just learned that at a cost of ten seconds rather than at the cost of a production incident.

**This is the entire content of Week 6, done by hand.** `mutmut` automates it — 1,204 mutants against `roomsvc`, of which the suite noticed 374 — but the habit does not need the tool, and a student who does it all term will arrive at Week 6 with a better score than one who wrote twice as many tests.

**It also reframes what you are doing when you write a test.** You are not covering a line. **You are making a claim, and then checking that the claim has teeth.** 61% of `roomsvc`'s lines are executed by its suite; 31% of deliberately introduced bugs are caught by it. **The gap between those two numbers is the gap between a test that ran and a test that checked**, and every test you write this term falls on one side of it.

---

### Assessment Reminder

**Quizzes carry no weight. The project carries 40%.** Quiz *N* covers Week *N−1*, ten minutes at the start of **Tuesday's** lecture in Weeks 1–11, with its own key printed. Tracked in [[_CS 212 Quiz Record]].

**Assignments** released Wednesday 17:00, due Friday 17:00 of the week after; **lowest of thirteen dropped.** A 4 is due this Friday; A 5 is released Wednesday and is **marked from your commit history**, not from the final state of the code.

> **Before Tuesday of Week 6 you want**: the concurrency test, the parametrised transition test,
> `tests/factories.py`, a test per failure extension, **and `pytest -p randomly` passing.**
> All five are Phase 1 artefacts. The last one will fail the first time you run it, and finding out
> in Week 5 rather than in April is the point.

---

### Connections

**Back:** **Week 1's third acceptance scenario becomes an executable test this week** — it has been waiting four weeks. **Week 3's placement of the invariant in the database** is what makes that test pass, and **W3 L11 §2's measured 1 ms against 1.2 s per module** is the arithmetic behind L16 §3's budget. **W4 L14 §3's test data builder** pays off immediately in every test you write.

**Sideways:** **CS 202's Week 5 is address spaces and the memory hierarchy**, and its lab measures things the same way this week does — by breaking an assumption and watching what notices. **MATH 251's Weeks 4–5 are random variables and expectation**, which is the machinery Week 6 needs to say what a mutation score is a measurement *of*.

**Forward:** **Week 6 is the measurement**: coverage, property-based testing and mutation testing, where 61% and 31% are finally explained and where your own suite gets a number. **Week 7's peer review** uses your tests as evidence — a reviewer's first question about a pull request is what test would have caught this. **Week 9's refactoring depends entirely on this week**, because refactoring without tests is rewriting. **The final report marks a 70%-coverage, 75%-mutation project above a 95%/30% one**, and this is the week that decides which one you have.

---

*CS 212 · Week 5 · © CSE Department*
