# CS 212 · Software Engineering
## Week 5 · Lecture 2 of 3
### TDD: Red, Green, Refactor — Done for Real

*“I'm not a great programmer; I'm just a good programmer with great habits.”* — Kent Beck, as quoted in Martin Fowler et al., *Refactoring* (1999)

---

**Sat:** Wednesday of Week 5, 10:00–10:50, TH 200 · **Reading:** Beck, *TDD by Example*, Part I, in one sitting · **Next:** L18, test doubles and BDD

**Coursework:** 📝 **Assignment 5** released today 17:00, due Fri of Week 6 17:00 · 📝 **Assignment 4** due Fri this week 17:00 · 📊 **Quiz 6** Tue of Week 6 · 📋 **Phase 1 presentation** Tue of Week 6 · 📘 **Midterm** Wed of Week 6 18:00–19:15
**A 5 is released after this lecture**, Wednesday 17:00.

---

## 1. The Loop

```
   ┌──────────────────────────────────────┐
   │  RED     write a failing test        │
   │  GREEN   make it pass, any way       │
   │  REFACTOR  clean up, tests still green│
   └──────────────────────────────────────┘
           seconds to a couple of minutes
```

**Three rules people skip, each of which is the point:**

1. **Run the test and watch it fail, for the right reason.** A test that passes before you write the code is testing nothing — and this happens constantly, from a typo in the test name, a wrong import, or asserting something already true. **The red is the only evidence the test can fail.**
2. **Make it pass the simplest way, including a hard-coded return.** This feels absurd and it is the mechanism: it forces the *next* test to be the one that makes the hard-code untenable. **Beck calls it "fake it till you make it".**
3. **Refactor with the tests green**, and never at the same time as changing behaviour. This is Week 9's rule arriving early.

**The cycle length is the whole thing.** Seconds to minutes. If you have been red for twenty minutes, **revert and take a smaller step** — this is the single hardest habit in the practice and the one that distinguishes people who have done it from people who have read about it.

---

## 2. A Kata, Live

`slot`'s state transitions (W4 L15 §3). **Watch the steps, including the bad-looking ones.**

**Step 1 — Red.**

```python
def test_a_held_booking_can_be_confirmed():
    b = Booking(state=State.HELD)
    assert transition(b, State.CONFIRMED).state is State.CONFIRMED
```
```
E   NameError: name 'transition' is not defined
```

**Green, shamelessly:**
```python
def transition(b, to): return replace(b, state=to)
```

**Step 2 — Red.** The first rule:

```python
def test_a_cancelled_booking_cannot_be_confirmed():
    b = Booking(state=State.CANCELLED)
    with pytest.raises(IllegalTransition):
        transition(b, State.CONFIRMED)
```
```
E   Failed: DID NOT RAISE <class 'IllegalTransition'>
```

**Green — and this is the step students refuse to take:**
```python
def transition(b, to):
    if b.state is State.CANCELLED:
        raise IllegalTransition(b.state, to)
    return replace(b, state=to)
```

**That is wrong.** It is deliberately, visibly wrong — a cancelled booking cannot go to `HELD` either, and neither can a confirmed one. **Write it anyway**, because the next test is what tells you the shape of the right answer.

**Step 3 — Red.**
```python
def test_a_confirmed_booking_cannot_return_to_held():
    with pytest.raises(IllegalTransition):
        transition(Booking(state=State.CONFIRMED), State.HELD)
```

**Now the special-casing is untenable**, and the table falls out on its own:

```python
LEGAL = {(State.HELD, State.CONFIRMED),
         (State.HELD, State.CANCELLED),
         (State.CONFIRMED, State.CANCELLED)}

def transition(b, to):
    if (b.state, to) not in LEGAL:
        raise IllegalTransition(b.state, to)
    return replace(b, state=to)
```

**Step 4 — Refactor, green throughout.** Replace the three tests with one that covers all nine pairs:

```python
@pytest.mark.parametrize("frm,to", list(product(State, State)))
def test_only_legal_transitions_are_permitted(frm, to):
    b = Booking(state=frm)
    if (frm, to) in LEGAL:
        assert transition(b, to).state is to
    else:
        with pytest.raises(IllegalTransition):
            transition(b, to)
```

**Invariant I3 is now exhaustively tested** (W1 L06 §4), in nine cases, and adding a fourth state makes the parametrisation cover sixteen automatically.

> **Notice what happened, because this is the actual claim of TDD.** The table was not designed; it
> **emerged from the third test**, at the moment the special-casing stopped paying. The tests drove
> the design — and that, rather than the test coverage, is what its advocates mean.

---

## 3. What the Evidence Actually Says

**Stated honestly, because W0 L02 §8 rated it weak and mixed and you deserve the detail.**

| Study | Setup | Result |
|---|---|---|
| **George & Williams (2003)** | 24 professionals, pairs, one short task | TDD passed ~18% more black-box tests; took ~16% longer |
| **Erdogmus et al. (2005)** | 24 students | More tests written; **quality difference not significant** |
| **Nagappan et al. (2008)**, Microsoft/IBM case studies | Four industrial teams | 40–90% fewer defects; **15–35% more development time.** No control for team quality |
| **Fucci et al. (2016)**, external replication | 39 professionals | **No significant effect of test-*first* on external quality or productivity.** What predicted outcomes was **granularity and uniformity of the cycle** |
| **Santos et al. (2021)**, meta-analysis | Pooled | Small, inconsistent effects; **high heterogeneity** |

**The convergent reading, and it is the one to carry:**

> **The benefit attributed to TDD appears to come from working in small, uniform steps with
> frequent test execution — not from writing the test first.**

**This is good news, not a debunking.** The small-steps discipline is real, it is learnable, and TDD is an unusually effective way to *enforce* it, because the loop makes a large step physically awkward. **What is not supported is the strong claim** that the ordering itself is the active ingredient.

> **This course's position, and it is in the syllabus §7.3:** you are assessed in Week 6 on whether
> **your tests are worth something**, measured by mutation score. **Not on the order in which you
> typed them.** Learn the rhythm because it is the most reliable way to get there.

---

## 4. Where TDD Is Genuinely Hard

Its advocates under-report these. Know them so that failing at them does not read as failing at TDD.

| Situation | Why it is hard | What to do instead |
|---|---|---|
| **You do not know the design yet** | TDD assumes you can name the next behaviour. Exploring an unfamiliar API, you cannot | **Spike**: throw-away code to learn the shape. **Then delete it and TDD the real thing.** Beck's own advice |
| **Algorithmic work** | Tests for a scheduling heuristic do not drive you toward it; you need the algorithm first | Write it, then test it thoroughly. **Property-based testing (W6) is the better tool here** |
| **Concurrency** | You cannot write a failing unit test for a race. **It fails one time in ten thousand** | Design it away (W3 L10 §6) and **verify with a stress test**, not a unit test |
| **UI** | Test-first on layout is rarely worth it | Test the logic behind it; look at the UI with your eyes |
| **Legacy code** | There is no seam to write a test against, which is why `confirm_booking` has eleven tests | **Characterisation tests first** (Feathers, and Week 9), then refactor |

**The last row is the one this course keeps returning to**, because it is the situation most of your career is in. **Michael Feathers' definition — *"legacy code is code without tests"* — is deliberately unkind and it is operationally right:** what makes code legacy is not its age but that you cannot change it safely.

---

## 5. Test-After, Done Properly

Most of your code will be written test-after. **That is fine, and it can be done well or badly.**

**Badly:** write the code, run it by hand, then write tests that pass. **The tests are shaped by the implementation you already have** — they walk the paths you happen to have written, assert what the code happens to do, and are exactly as wrong as the code. This is `roomsvc`'s suite, and it is how you get 61% coverage and a 31% mutation score.

**Well — three habits that recover most of the benefit:**

1. **Write the test from the acceptance criteria, not from the code.** Close the implementation. If you cannot write the test without re-reading the function, you are documenting rather than testing.
2. **Break it deliberately.** Comment out a line, flip a comparison, change a constant. **If the suite still passes, the test is decorative.** This is mutation testing done by hand, it takes ten seconds, and Week 6 automates it.
3. **Write the failure cases first.** Left to last, they are never written — which is why W1 L06 §1's six extensions have no tests in `roomsvc` and the one success path has eleven.

> **Habit 2 is the one to adopt this week and it costs nothing.** Every time you write a test,
> break the code once and check the test notices. **A student who does this for the whole term will
> have a better mutation score in Week 6 than one who wrote twice as many tests.**

---

## 6. What to Do on Your Project

**This fortnight, in this order:**

1. **Write the concurrency test** (L16 §5). It is the highest-value test in the project and Phase 1 marks it.
2. **Parametrise the transition table test.** Nine cases, one loop, invariant I3 discharged.
3. **Add `tests/factories.py`** (W4 L14 §3). Every test you write after it is shorter and clearer.
4. **Write one test for each failure extension in your cancellation use case** (A 1 Q3). There are at least five and you probably have zero.
5. **Pick one new feature this fortnight and do it test-first, properly** — small steps, red first, fake it till you make it. **A 5 requires the commit history to show it.**

**And set the budget now** (L16 §3): *the suite runs in under 60 seconds in CI.* Put it in the charter. **It is much easier to hold a budget from 40 tests than to recover one from 300.**

---

## 7. Summary

- **Red, green, refactor**, in seconds to minutes. **Watch the test fail for the right reason** — the red is the only evidence it can fail. **Fake it till you make it.** If you have been red twenty minutes, revert and take a smaller step.
- **The kata shows the actual claim:** the transition table was not designed, it **emerged at the third test**, when special-casing stopped paying.
- **The evidence: test-first is not the active ingredient.** Five studies, and the careful replication (Fucci 2016) attributes the benefit to **small, uniform steps with frequent test runs.** That is good news — the discipline is real and TDD enforces it well.
- **This course assesses whether your tests are worth something (W6), not the order you typed them.**
- **TDD is genuinely hard** for unknown designs (spike, then delete), algorithms (property-based testing), concurrency (**design it away and stress-test**), UI, and legacy code (**characterisation tests first**).
- ***"Legacy code is code without tests"*** — unkind, and operationally right: what makes code legacy is that you cannot change it safely.
- **Test-after can be done well:** write from the acceptance criteria with the implementation closed; **break the code deliberately and check the test notices**; write the failure cases first.
- **Set a suite-time budget now**, at 40 tests, not at 300.

**Next:** L18 — test doubles, the five kinds and which two you should mostly avoid; BDD; and what an end-to-end test is actually for.

---

*CS 212 · Week 5 · L17 · © CSE Department*
