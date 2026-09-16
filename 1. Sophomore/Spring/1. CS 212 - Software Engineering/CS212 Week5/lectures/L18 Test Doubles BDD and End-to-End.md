# CS 212 · Software Engineering
## Week 5 · Lecture 3 of 3
### Test Doubles, BDD, and End-to-End

---

**Sat:** Thursday of Week 5, 10:00–10:50, TH 200 · **Reading:** Fowler, *"Mocks Aren't Stubs"* (2007) · **Next:** Week 6 — coverage, property-based and mutation testing · **⚠️ Week 6 holds Phase 1 (Tue) and the midterm (Wed)**

---

## 1. The Five Doubles, and Why the Names Matter

Meszaros' taxonomy, via Fowler. **People say "mock" for all five and it causes real confusion.**

| Double | What it does | Use it when |
|---|---|---|
| **Dummy** | Passed to satisfy a signature; never used | A parameter irrelevant to this test |
| **Stub** | Returns canned answers | You need the collaborator to *provide* something |
| **Spy** | A stub that records how it was called | The **call itself** is the behaviour under test |
| **Mock** | **Pre-programmed with expectations**; fails the test if they are not met | Rarely. §2 |
| **Fake** | A **working** implementation, simplified | **Most of the time.** An in-memory repository |

**The distinction that matters is the last column of Fowler's article:**

> **Stubs, fakes and dummies verify *state*. Mocks verify *interactions*.**

**State verification asks: after this, is the world right?** Interaction verification asks: **did it make the calls I expected?** The second couples your test to the implementation's route, which L16 §4 already said is how you get a test that passes when the behaviour breaks.

---

## 2. Why Mocks Are Mostly a Trap

```python
def test_confirm_notifies_owner():
    notify = Mock()
    confirm("h1", FakeRepo(...), notify)
    notify.assert_called_once_with(owner_id, "Confirmed: TH200 at 10:00")
```

**Four problems, and every one of them will happen to you:**

1. **It asserts the message text.** Change the wording and the test fails, though nothing broke.
2. **It asserts the call shape.** Refactor `notify(user, msg)` into `notify(Notification(...))` and the test fails, though nothing broke.
3. **It does not assert that a notification was *sent*.** If `notify` is wired to nothing in production, this test still passes.
4. **`Mock()` accepts everything.** `notify.assert_called_once_wiht(...)` — note the typo — **passes silently**, because `Mock` invents the attribute. This has cost real teams real incidents. `autospec=True` fixes it; almost nobody uses it.

**The fake version:**

```python
class FakeNotifier:
    def __init__(self): self.sent: list[tuple[UUID, str]] = []
    def __call__(self, user_id, message): self.sent.append((user_id, message))

def test_confirm_notifies_owner():
    notify = FakeNotifier()
    confirm("h1", FakeRepo(...), notify)
    assert [u for u, _ in notify.sent] == [owner_id]     # who, not what
```

**Survives a wording change, survives a signature refactor, fails when the notification stops happening, and cannot silently pass on a typo.**

**When a mock *is* right:** when the interaction is the entire observable behaviour and there is no state to check — an audit log write, a payment charge, an idempotency key sent to a third party. **"Did we call the payment provider exactly once?" is the requirement**, and a spy or a mock is the only way to say it.

> **The rule: prefer fakes; use spies when the call is the behaviour; use mocks when you need the
> test to fail on a missing call.** And **write your fakes once, in `tests/fakes.py`** — a fake reused
> across forty tests is maintained; a `Mock` configured inline in forty tests is forty maintenance
> sites.

**One warning about fakes, which is real:** a fake can drift from the thing it fakes. `FakeBookingRepo` has no unique index, so it can never reproduce the invariant violation. **That is not an argument against fakes — it is the argument for L16 §5's integration test**, and the division of labour is exactly right: fakes for the rules, real Postgres for the guarantees.

---

## 3. BDD: Two Different Things Under One Name

**BDD is (a) a way of phrasing tests and (b) a tool ecosystem, and they are worth very different amounts.**

### (a) The phrasing — worth a lot, costs nothing

```python
def test_confirming_a_slot_that_is_already_taken_is_rejected():
    # Given
    existing = a_confirmed_booking(resource="TH200", slot=TEN_AM)
    # When
    result = confirm_request(resource="TH200", slot=TEN_AM, owner=other_user)
    # Then
    assert result.status == 409
```

**Two habits, and they are the whole of the useful part:**

- **Name the test after the behaviour, in a sentence.** `test_confirming_a_slot_that_is_already_taken_is_rejected` tells you what broke from the failure line alone. `test_confirm_2` does not. **You read test names far more often when they fail than when you write them.**
- **Given / When / Then structure.** Setup, one action, assertions. **One *When* per test** — a test with three actions is three tests, and when it fails you do not know which.

### (b) The tooling — worth much less than it claims

Cucumber, `behave`, `pytest-bdd`: feature files in Gherkin, mapped to step definitions by regular expression.

```gherkin
Scenario: the slot is taken
  Given TH 200 has a confirmed booking at 10:00
  When I request TH 200 for that slot
  Then the request is rejected with 409
```

**The pitch:** non-technical stakeholders write and read these, so requirements and tests are the same artefact.

**What happens in practice:**

| | |
|---|---|
| **Stakeholders do not write them.** Developers do, in a constrained syntax, for an audience that does not read them | The main premise fails |
| **Step definitions become a second codebase** with its own duplication, and are matched by regex, so a reworded step silently matches the wrong one | Real maintenance cost |
| **Refactoring is worse** — no type checking or IDE navigation across the feature/step boundary | |
| **It is slow** | Most Gherkin suites are E2E, so you get the pyramid's top band by default |

**When it genuinely pays:** a regulated domain where an auditor or domain expert really does read the scenarios, or a product where acceptance criteria are negotiated with a non-technical customer who will engage. **Neither describes `slot`.**

> **This course's recommendation: adopt the phrasing, skip the tooling.** Sentence-shaped test
> names and Given/When/Then comments cost nothing and improve every test you write. **A Gherkin
> layer in a five-person term project costs a week and buys a vocabulary you already share.**

---

## 4. Contract Tests, Briefly

**The gap the pyramid leaves.** If `slot` calls the university calendar API, you stub it in your tests — so **your suite passes when the real API changes.**

**A contract test records what you believe about the other side and checks it against reality, separately:**

```python
@pytest.mark.contract          # deselected by default; runs nightly
def test_calendar_api_still_returns_the_fields_we_map():
    resp = real_client.get_event(KNOWN_EVENT_ID)
    assert {"uid", "dtstart", "summary"} <= resp.keys()
```

**Two properties make this work:** it is **not** in the fast suite (it needs the network and it will fail for reasons outside your control), and **it asserts only what you actually depend on** — not the whole response.

**Where the adapter pays again** (W4 L14 §5): the contract test asserts exactly the fields your adapter maps, which is a short, honest list. **Without an adapter, you cannot write this test, because you do not know what you depend on.**

---

## 5. What Makes a Test Suite Trustworthy

Six properties. **A suite with all six gets used; a suite missing one of the first three gets ignored, and an ignored suite is worse than none.**

| | |
|---|---|
| **Fast enough to run constantly** | Under 60 s in CI, under 2 s for one file |
| **Deterministic** | **Zero flaky tests. Not "few".** One tolerated flake teaches everyone that red might mean nothing |
| **Failures are diagnosable** | The name says what broke; the assertion says what was expected |
| **Independent of order** | `pytest -p randomly` should pass. Run it this week; it will not |
| **Tests behaviour, not structure** | Survives refactoring; fails on regression (L16 §4) |
| **Actually detects regressions** | **Week 6 measures this**, and it is the only one of the six you cannot assess by reading |

**On flakiness, the operational rule:** a flaky test is **quarantined the day it is noticed** — marked, excluded from the gate, and given an issue with a deadline. **Not re-run.** The moment "just re-run it" becomes normal, your suite has stopped being evidence and has become a ritual.

---

## 6. Before Week 6

**Week 6 is Phase 1 on Tuesday and the midterm on Wednesday.** What you do this week decides both.

**Make sure you have, by Friday:**

- [ ] **The concurrency test** — two clients, one slot, `[201, 409]`, exactly one confirmed booking. **This is the single most valuable artefact in Phase 1**
- [ ] **The parametrised transition test** — nine cases, invariant I3 discharged
- [ ] `tests/factories.py`
- [ ] **At least one test per failure extension** in your cancellation use case
- [ ] **`pytest -p randomly` passing** — if it does not, you have shared state, and you want to know now
- [ ] A suite-time budget in the charter, and the current number

**And read Beck's *TDD by Example*, Part I, in one sitting.** It is about 100 small pages and it is the only way the rhythm transmits. **This week, not in April.**

---

## 7. Summary

- **Five doubles:** dummy, stub, spy, mock, fake. **Stubs, fakes and dummies verify state; mocks verify interactions**, and interaction verification couples the test to the route.
- **Mocks are mostly a trap**: they assert wording and call shape, they do not assert the thing happened, and **`Mock()` passes silently on a typo'd `assert_called_once_wiht`.** Use `autospec=True` if you must.
- **Prefer fakes, written once in `tests/fakes.py`.** Use a spy when the call *is* the behaviour; a mock when the test must fail on a missing call.
- **A fake can drift** — `FakeBookingRepo` has no unique index — **which is the argument for the real-Postgres integration test**, not against fakes. Fakes for the rules; Postgres for the guarantees.
- **BDD's phrasing is free and valuable**: sentence-shaped test names, Given/When/Then, **one *When* per test.** **BDD's tooling mostly is not** — stakeholders do not write the features, steps are a second codebase matched by regex, and the suites are E2E by default.
- **Contract tests fill the gap your stubs create**: outside the fast suite, asserting only what your adapter maps.
- **Six properties of a trustworthy suite**, and **zero flaky tests, not few** — quarantine on the day, never re-run.

**Next:** Week 6 — coverage, property-based testing and mutation testing. Where you find out what your tests are actually worth, on a number, and where 61% and 31% finally get explained.

---

*CS 212 · Week 5 · L18 · © CSE Department*
