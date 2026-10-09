# CS 212 · Software Engineering
## Week 5 · Lecture 1 of 3
### The Test Pyramid, and What Each Level Buys

*“"How to test?" is a question that cannot be answered in general. "When to test?" however, does have a general answer: as early and as often as possible.”* — Bjarne Stroustrup, *The C++ Programming Language*

---

**Sat:** Tuesday of Week 5, 10:00–10:50, TH 200 · **⚠️ Quiz 5 in the first ten minutes** — covers Week 4 · **Reading:** Beck, *TDD by Example*, Part I — **read it in one sitting this week** · **Next:** L17, TDD

**Coursework:** 📊 **Quiz 5** today · 📝 **Assignment 5** released Wed this week 17:00, due Fri of Week 6 17:00 · 📝 **Assignment 4** due Fri this week 17:00 · 📘 **Midterm** Wed of Week 6 18:00–19:15

---

## 1. What a Test Is For

Not "to find bugs". A test that finds a bug has already failed at its main job, which is:

> **A test is a claim about behaviour, written so that a machine can tell you when the claim stops
> being true.**

**The value is in the *stops*.** You write the code once and change it four hundred times, and every one of those changes is a chance to break something you are not looking at. **The test suite is the thing that lets you change code you do not fully understand**, which — given that 60% of lifetime cost is post-release change by people who did not write it (W0 L01 §4) — is the whole point.

**`roomsvc` is what the absence looks like.** 212 tests, 61% coverage, **31% mutation score**, and a fourteen-line fix that took four months because *nobody could convince themselves that touching `confirm_booking` was safe.* **The tests existed. They were not evidence.**

> **The question to ask of any test you write, all term:** *if someone broke this behaviour, would
> this test fail?* Week 6 answers it with a tool. This week you should ask it by hand, every time.

---

## 2. The Pyramid

Mike Cohn, 2009. **Three levels, and the shape is an assertion about proportions.**

```
        ╱ E2E ╲          few, slow, brittle, high confidence
      ╱─────────╲
    ╱ Integration ╲      some, medium
  ╱─────────────────╲
╱       Unit         ╲   many, fast, precise
```

| Level | What it exercises | Speed | What a failure tells you |
|---|---|---|---|
| **Unit** | One function or class, no I/O | **< 1 ms** | **Exactly which function is wrong** |
| **Integration** | Several components, with real infrastructure — a real database | 10–500 ms | Something in this interaction is wrong |
| **End-to-end** | The whole system through its real interface | 1–30 s | **Something, somewhere, is wrong** |

**The proportions are a *consequence*, not a rule.** They follow from three facts:

1. **Cost scales up the pyramid.** An E2E test is 1,000–10,000× slower than a unit test. A suite of 200 E2E tests takes an hour and nobody runs it.
2. **Diagnostic precision scales down.** A failing unit test names the function. A failing E2E test names your entire system.
3. **Brittleness scales up.** E2E tests fail for reasons unrelated to your change — a slow container, a race in the fixture, a stale session. **A suite that fails randomly gets ignored, and an ignored suite is worse than none**, because it costs time and buys nothing.

**That third point is the one that kills projects.** Once a team starts re-running the build "because it's probably flaky", every real failure is also probably flaky. **Flakiness is not an annoyance; it is the mechanism by which a test suite stops being evidence.**

---

## 3. The Honest Criticisms of the Pyramid

The pyramid is a useful default and it is not a law. **Three real objections you should know:**

**1. "Unit" is undefined.** Is a unit a function, a class, a module, or "a behaviour"? Kent Beck's own usage is closer to *"a test that runs in isolation from other tests"* than *"a test of one class"*. **The class-per-test-file convention is a convention, and following it mechanically produces tests coupled to structure** — so every refactoring breaks tests that were testing nothing that changed.

**2. The shape depends on your architecture.** A system whose complexity is in its *rules* (a tax engine, a scheduler) has a real base of unit tests. A system whose complexity is in its *integrations* (a service that mostly moves data between four APIs) has almost no logic to unit-test, and a pyramid-shaped suite there tests mocks rather than behaviour. **`slot` is closer to the first; a lot of industrial code is the second.**

**3. Fast integration tests change the arithmetic.** The pyramid's proportions assume integration tests are expensive. With a containerised Postgres reused across the whole session, an integration test against a real database can run in **5–20 ms** — a hundred times slower than a unit test and a hundred times faster than E2E. **The "testing trophy"** (Kent C. Dodds) argues for pushing weight into that middle band, and for `slot` it is a defensible position.

> **What to do with this:** do not defend a shape. **Defend a budget.** *"The whole suite runs in
> under 60 seconds on CI, and a single test file runs in under 2 seconds locally"* is an
> engineering constraint; it forces the pyramid's proportions wherever they are actually needed and
> permits the trophy where they are not.

---

## 4. Unit Tests: the Properties That Matter

**FIRST** (Beck, via Martin) is the usual mnemonic. Three of the five do real work.

| | | |
|---|---|---|
| **F** | Fast | **Load-bearing.** A suite you will not run during a refactoring is not a safety net |
| **I** | **Isolated** | **Load-bearing.** No shared state, no order dependence. `roomsvc`'s suite fails if you run it with `-p no:randomly` in a different order — try it |
| **R** | Repeatable | **Load-bearing.** `datetime.now()` and `random` in a test are defects |
| **S** | Self-validating | Passes or fails; no human reads output |
| **T** | Timely | Written near the code. This is the TDD claim and L17 is sceptical about the strong form |

**The failure mode you will actually hit** is not slowness — it is **tests coupled to structure instead of behaviour.**

```python
# coupled to structure: breaks when you rename or inline, tells you nothing
def test_confirm_calls_repo_confirm():
    repo = Mock()
    confirm("h1", repo, noop)
    repo.confirm.assert_called_once_with("h1")

# coupled to behaviour: survives refactoring, fails when the rule breaks
def test_confirming_a_held_booking_makes_it_confirmed():
    repo = FakeRepo(bookings=[BookingBuilder().held().with_id("h1").build()])
    booking = confirm("h1", repo, noop)
    assert booking.state is State.CONFIRMED
```

**The first test passes if `confirm` does nothing else at all.** It asserts an implementation detail, it will break the day you rename the method, and **it will not fail when the behaviour breaks** — which is the definition of a worthless test, and which Week 6 will demonstrate with a mutant.

> **The rule: assert on the result, not on the route.** If a test's assertion is
> `mock.assert_called_with(...)`, ask what observable behaviour you meant, and assert that instead.
> Sometimes the call genuinely *is* the behaviour — sending the email is the point — and then a
> spy is right. Usually it is not.

---

## 5. Integration Tests: Test the Thing, Not a Picture of It

**An integration test that mocks the database has tested your mock.**

This matters more than it sounds because **the database is where your invariant lives** (W3 L10 §6). A unit test with a fake repo can never fail on a unique-index violation, because the fake has no index. **The only test that can demonstrate your invariant holds is one that runs against real Postgres.**

```python
# tests/integration/test_invariant.py
def test_two_concurrent_confirms_yield_exactly_one_booking(pg):
    slot, resource = Slot("2026-03-04T10:00"), "TH200"
    a, b = make_hold(resource, slot), make_hold(resource, slot)

    with ThreadPoolExecutor(2) as pool:
        results = [f for f in as_completed([pool.submit(confirm_via_api, a),
                                            pool.submit(confirm_via_api, b)])]
    statuses = sorted(r.result().status_code for r in results)

    assert statuses == [201, 409]
    assert count_confirmed(resource, slot) == 1
```

**That is the test `roomsvc` did not have**, and it is the acceptance criterion from W1 L05 §3 made executable. **It is the single highest-value test in your project** and Phase 1 gives marks for it directly.

**Use a real Postgres, in a container, reused for the session:**

```python
@pytest.fixture(scope="session")
def pg():                       # testcontainers, or a compose service in CI
    ...                         # start once: ~9 s
@pytest.fixture(autouse=True)
def rollback(pg):               # per test: wrap in a transaction, roll back
    ...                         # ~2 ms, and perfect isolation
```

**The transaction-rollback trick is the one to learn.** Each test runs inside a transaction that is rolled back at the end: perfect isolation, no truncation, ~2 ms per test. It has one limitation and you must know it — **it cannot test anything that itself commits**, which includes the concurrency test above. Those few tests get their own schema or their own database.

---

## 6. End-to-End: Few, and Chosen

**E2E tests are expensive, brittle and slow, and you still want some**, because they are the only tests that exercise the wiring — your routing, your serialisation, your middleware, your migrations having actually run.

**The rule: E2E tests cover *journeys*, not *cases*.** One test per thing a user actually does end to end; every variation lives at a lower level.

**For `slot`, three or four is right:**

1. A lecturer books a free slot and sees it in their list.
2. A lecturer tries a taken slot and is told no.
3. An admin cancels someone's booking and the owner is notified.
4. *(if you build it)* A recurring booking is created and one occurrence is cancelled.

**What makes them brittle, and what to do:**

| Cause | Fix |
|---|---|
| **Timing** — asserting before an async thing finished | Wait for a **condition**, never `sleep`. `sleep` is how a suite becomes both slow and flaky |
| **Shared state between tests** | Fresh data per test, distinct resource ids. **Never depend on test order** |
| **Selectors on a UI** | Test the API, not the browser, wherever you can. **No marks in this course require a browser test** |
| **Real external services** | Stub at your boundary — the adapter from W4 L14 §5 is the seam you already built |

---

## 7. What Not to Test

A short list, and every item on it costs a team a day at some point.

| Do not test | Why |
|---|---|
| **The framework or the library** | FastAPI's routing works. SQLAlchemy's `INSERT` works. Testing them tests other people's code and breaks on their upgrades |
| **Getters, setters, `@dataclass` fields** | A test with no logic in the subject asserts that Python works |
| **Private functions, directly** | Test through the public surface. A test on a private function **prevents the refactoring the privacy existed to permit** |
| **Exact log or error message strings** | Unless the message is a contract — an API error code is; a log line is not |
| **Randomly generated everything, without control** | Non-repeatable failures. **Property-based testing is the disciplined version and it is Week 6** |

> **And the inverse, which is where the marks are: things teams do not test and should.**
> The **failure paths** (W1 L06 §1 counted six extensions to one success path), the **invariant
> under concurrency**, the **state transitions that should be illegal**, and **what happens when
> the notification fails.** Every one of these is in your acceptance criteria already, and every one
> is the sort of thing `roomsvc`'s 212 tests do not cover.

---

## 8. Summary

- **A test is a claim about behaviour that a machine can tell you has stopped being true**, and its value is in the *stops*. `roomsvc` had 212 tests that were not evidence.
- **The pyramid's proportions are a consequence** of cost scaling up, diagnostic precision scaling down and **brittleness scaling up** — and flakiness is the mechanism by which a suite stops being believed.
- **Three honest objections:** "unit" is undefined; the right shape depends on where your complexity is; **fast containerised integration tests change the arithmetic.** So **defend a budget, not a shape** — under 60 s for the suite, under 2 s for a file.
- **FIRST's load-bearing letters are Fast, Isolated and Repeatable.** `datetime.now()` in a test is a defect.
- **Assert on the result, not the route.** A test whose assertion is `mock.assert_called_with` usually passes when the behaviour breaks — which Week 6 demonstrates with a mutant.
- **An integration test that mocks the database has tested your mock**, and **the only test that can demonstrate your invariant is one against real Postgres.** The concurrent-confirm test is the highest-value test in your project.
- **Learn the transaction-rollback fixture** — ~2 ms and perfect isolation — and know its one limit: it cannot test code that commits.
- **E2E tests cover journeys, not cases.** Three or four for `slot`. **Wait for conditions, never `sleep`.**
- **Do not test the framework, accessors, private functions or log strings.** **Do** test the failure paths, the invariant under concurrency, and the illegal transitions.

**Next:** L17 — TDD, done for real on a kata, with an honest account of what the evidence for it does and does not say.

---

*CS 212 · Week 5 · L16 · © CSE Department*
