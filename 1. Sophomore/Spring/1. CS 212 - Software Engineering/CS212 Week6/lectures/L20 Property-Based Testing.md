# CS 212 · Software Engineering
## Week 6 · Lecture 2 of 3
### Property-Based Testing

---

**Sat:** Wednesday of Week 6, 10:00–10:50, TH 200 · **Reading:** Hypothesis docs, "Quick start" and "What you can generate" · **Next:** L21, mutation testing
**A 6 is released after this lecture**, Wednesday 17:00. **⚠️ Midterm this evening, 18:00–19:15, Weeks 0–5.**

---

## 1. The Problem With Examples

Every test you have written this term is an **example**: *given this input, expect that output.*

Examples have a defect that is easy to state and hard to feel until it bites: **you choose them, and you choose them from the same mental model that produced the code.** The cases you did not think of when writing the function are exactly the cases you do not think of when writing its tests.

**`roomsvc`'s hold expiry is the demonstration.** Eleven tests, all of them with durations like 5, 10, 15 and 20 minutes. **None with zero. None with a negative. None spanning a DST boundary.** Issue #31 — *"recurring bookings drop the last occurrence in DST weeks"* — has been open since **August 2020**, and it is a test-selection failure rather than a coding one.

> **Property-based testing inverts the exercise.** You do not supply inputs. You state a **property
> that should hold for all inputs**, and the library generates them — including the ones you would
> never choose, and then **shrinks any failure to the smallest example that still fails.**

---

## 2. A First Property

```python
from hypothesis import given, strategies as st

@given(st.sampled_from(State), st.sampled_from(State))
def test_transition_either_succeeds_or_raises_and_never_corrupts(frm, to):
    booking = BookingBuilder().with_state(frm).build()
    try:
        result = transition(booking, to)
    except IllegalTransition:
        return                                   # rejecting is always acceptable
    assert result.state is to                    # if it succeeded, it did what it said
    assert result.id == booking.id               # and changed nothing else
```

**This is weaker than W5's exhaustive parametrised test and it is complementary**, not a replacement: the parametrised version checks *which* transitions are legal, and this one checks that **whatever the answer, the function never half-does it.**

**The general shape:** *for all inputs, either it refuses, or it produces something satisfying the invariant.* **That shape applies to almost every domain function you will write**, and it is the cheapest property to add.

---

## 3. The Five Property Patterns

From Scott Wlaschin's taxonomy. **Learn these five and you can find a property for most functions.**

### 1. Invariants — something that never changes

```python
@given(st.lists(booking_strategy()))
def test_week_view_never_shows_two_confirmed_bookings_in_one_cell(bookings):
    grid = render_week(bookings)
    for cell in grid.cells:
        assert sum(1 for b in cell if b.state is State.CONFIRMED) <= 1
```

### 2. Round-trip — encode then decode

```python
@given(slot_strategy())
def test_slot_survives_serialisation(slot):
    assert Slot.from_iso(slot.to_iso()) == slot
```

**Round-trip properties find more bugs per line than anything else in this lecture.** Every serialisation boundary in your project — JSON, the database, iCal export, a URL parameter — has one available, and **DST, timezones, microsecond truncation and integer overflow all surface here first.**

### 3. Two implementations agree — the oracle

```python
@given(st.lists(booking_strategy()))
def test_fast_conflict_check_agrees_with_the_obvious_one(bookings):
    assert indexed_conflicts(bookings) == sorted(naive_conflicts(bookings))
```

**This is how you optimise safely.** Keep the slow obvious implementation as the oracle; the property says the fast one agrees. **Week 11 uses exactly this when you make something faster.**

### 4. Test the inverse — easier to verify than to compute

```python
@given(recurrence_strategy())
def test_every_expanded_occurrence_matches_the_rule(rule):
    for occurrence in expand(rule):
        assert rule.matches(occurrence)          # checking is easy; generating is not
```

### 5. Some things never change — idempotence, commutativity, ordering

```python
@given(booking_strategy())
def test_cancelling_twice_is_the_same_as_cancelling_once(booking):
    assert cancel(cancel(booking)) == cancel(booking)
```

**Idempotence is not an academic property for you** — it is a requirement of every retried operation (W3 L12 §2), and **A 5's concurrency work already depends on it.**

---

## 4. Shrinking Is the Feature

Generation is the obvious part. **Shrinking is what makes the tool usable.**

When Hypothesis finds a failure, it does not report the random input that broke — it **searches for the smallest input that still fails**, deleting list elements, reducing integers toward zero, simplifying strings.

```console
$ pytest tests/test_recurrence.py
Falsifying example: test_expand_preserves_count(
    rule=Recurrence(
        start=datetime(2026, 3, 29, 1, 30, tzinfo=Europe/London),
        count=2,
        freq='DAILY',
    ),
)
E   assert 1 == 2
```

**Not a 40-field random object. A two-occurrence rule starting at 01:30 on 29 March 2026** — which is the morning the UK clocks go forward, and 01:30 does not exist that day.

**That is `roomsvc` issue #31**, open since August 2020, found in under a second by a tool that knew nothing about calendars. **Nobody would have written that example. Hypothesis does not know it is interesting; it knows it is small.**

> **Shrinking is why this is worth learning.** A random-input tester that reports the raw failing
> case gives you a debugging session. One that shrinks gives you a **minimal reproduction**, which
> is most of a diagnosis.

---

## 5. Where It Fits, and Where It Does Not

**Excellent for:**

| | |
|---|---|
| **Pure functions with structure** | Parsers, formatters, date arithmetic, pricing, recurrence expansion |
| **Anything with a round-trip** | Serialisation, encoding, the database boundary |
| **Optimisations** | Against the obvious implementation as an oracle |
| **State machines** | Hypothesis's `RuleBasedStateMachine` generates *sequences* of operations and checks invariants after each — **and this is the right tool for `slot`'s booking lifecycle** |

**Poor for:**

| | |
|---|---|
| **Specific business rules** | *"External charity bookings cost half"* is one example and should stay one example |
| **Anything slow** | 100 examples × a database round trip is 100× the cost. Use `@settings(max_examples=20)` and a fake |
| **Finding the property when there isn't one** | If you cannot state a property, do not invent a weak one. **A property that says "it does not crash" is worth almost nothing** |

**The honest failure mode:** teams write one trivial property (`does not raise`), feel they have adopted property-based testing, and get nothing. **One good round-trip property is worth twenty of those.**

---

## 6. The State Machine, Because It Is the Right Tool Here

`slot` is a state machine, and Hypothesis will drive it for you:

```python
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant

class BookingLifecycle(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.repo = FakeBookingRepo()

    @rule(resource=resources(), slot=slots())
    def hold(self, resource, slot):
        try: self.repo.hold(resource, slot)
        except SlotUnavailable: pass

    @rule(data=st.data())
    def confirm(self, data):
        if not self.repo.held_ids(): return
        hid = data.draw(st.sampled_from(self.repo.held_ids()))
        try: self.repo.confirm(hid)
        except AlreadyBooked: pass

    @rule(data=st.data())
    def cancel(self, data):
        ...

    @invariant()
    def never_two_confirmed_in_one_slot(self):
        seen = Counter((b.resource, b.slot)
                       for b in self.repo.all() if b.state is State.CONFIRMED)
        assert all(n <= 1 for n in seen.values())

TestBookingLifecycle = BookingLifecycle.TestCase
```

**Hypothesis generates sequences** — hold, hold, confirm, cancel, confirm, hold, confirm — **and checks the invariant after every step.** It will find orderings you would never enumerate, and it shrinks the failing sequence to the shortest one that breaks it.

**One honest limitation, and it is important:** this runs against your **fake**, in one process, so **it cannot find the concurrency bug** (W5 L18 §2's drift warning). It finds *logic* orderings, not *interleavings*. **The database constraint and A 5's concurrent test remain the answer to the race**; this is the answer to *"is the state machine right?"*

---

## 7. Adopting It Without Wasting a Week

**Three properties, this fortnight, in this order:**

1. **A round-trip.** Your `Slot` or your booking JSON. **Ten minutes, and it will find something** — a timezone, a microsecond, or an ISO format edge.
2. **The either-refuses-or-is-correct property** from §2 on your main domain function. Five minutes.
3. **The state machine** from §6, with one invariant. An hour, and it is the one that finds real bugs.

**And two settings you want immediately:**

```python
# conftest.py
from hypothesis import settings, Phase
settings.register_profile("ci",  max_examples=200, deadline=None)
settings.register_profile("dev", max_examples=20,  deadline=200)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "dev"))
```

**Twenty examples locally, two hundred in CI.** The local suite stays inside L16 §3's budget; CI does the searching.

> **And record the failures.** Hypothesis writes its failing examples to `.hypothesis/examples`
> and replays them first on subsequent runs, so a bug once found stays found. **Do not gitignore
> that directory** — or, better, when it finds something, **write the shrunk example as an ordinary
> `@example` decorator or a plain test**, so the regression is explicit and survives a cache clear.

---

## 8. Summary

- **Examples are chosen from the same mental model that produced the code**, so the cases you missed writing it are the cases you miss testing it. `roomsvc`'s eleven expiry tests use 5, 10, 15 and 20 minutes and none spans a DST boundary — **issue #31, open since 2020.**
- **A property is a claim over all inputs**, and the library generates them and **shrinks the failure to the smallest failing case.**
- **Five patterns:** invariants, **round-trip** (best value per line), **an oracle** (how you optimise safely), testing the inverse, and **idempotence** (which you need anyway for retries).
- **Shrinking is the feature.** A two-occurrence rule starting 01:30 on 29 March 2026 — the hour the clocks go forward — found in under a second by a tool that knows nothing about calendars, only about *small*.
- **Excellent for pure structured functions, round-trips, optimisations and state machines. Poor for specific business rules and for anything slow**, and **a property that says "does not crash" is worth almost nothing.**
- **`RuleBasedStateMachine` is the right tool for `slot`'s lifecycle** — it generates operation sequences and checks the invariant after each — **but it runs against your fake and cannot find the race.** The constraint and the concurrent test remain the answer to that.
- **Adopt three properties this fortnight**: a round-trip, the refuses-or-correct property, and a state machine. **20 examples locally, 200 in CI**, and **write shrunk failures back as explicit tests.**

**Next:** L21 — mutation testing, where 61% and 31% are finally reconciled, and where your test suite gets the only score in this course that measures whether it would notice a regression.

---

*CS 212 · Week 6 · L20 · © CSE Department*
