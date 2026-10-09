# CS 212 · Software Engineering
## Week 6 · Lecture 3 of 3
### Mutation Testing — Testing the Tests

*“There are two ways to write error-free programs; only the third one works.”* — Alan Perlis, "Epigrams on Programming" (1982), #40

---

**Sat:** Thursday of Week 6, 10:00–10:50, TH 200 · **Reading:** Papadakis et al., *"Mutation Testing Advances"* (2019), §1–3 · **Next:** Week 7, code review

**Coursework:** 📝 **Assignment 5** due Fri this week 17:00 · 📊 **Quiz 7** Tue of Week 7 · 📝 **Assignment 7** released Wed of Week 7 17:00, due Fri of Week 8 17:00

---

## 1. The Idea, in One Paragraph

**Change the code so that it is wrong. Run the tests. Did any fail?**

If yes, the change was **killed** — your suite noticed. If no, the change **survived** — your suite would ship that bug.

**The mutation score is the share killed**, and it is the only number in this course that directly answers W5's question: *if someone broke this behaviour, would a test fail?*

**This is the ten-second habit from W5 L17 §5, automated and run thousands of times.**

---

## 2. What a Mutant Looks Like

Mutation operators are small, single, syntactic changes:

| Operator | Original | Mutant |
|---|---|---|
| Relational | `if hours > 0:` | `if hours >= 0:` |
| Arithmetic | `total = rate * hours` | `total = rate / hours` |
| Constant | `EXPIRY_MINUTES = 15` | `EXPIRY_MINUTES = 16` |
| Boolean | `if a and b:` | `if a or b:` |
| Return | `return price` | `return None` |
| Statement deletion | `self.audit(booking)` | *(removed)* |
| Negation | `if not permitted:` | `if permitted:` |

**Each mutant is a separate program, and each is run against the whole suite.** Which is why it is slow: 1,204 mutants against `roomsvc`'s 94-second suite is, naively, **31 hours**. §6 is about making that tractable.

---

## 3. Reconciling 61% and 31%

The two numbers you have been carrying since Week 0.

```console
$ coverage report --precision=1 | tail -1
TOTAL                        11438   4461   61.0%
$ mutmut results | tail -1
1204 mutants generated, 374 killed (31.1%), 802 survived, 28 timeout
```

**61% of lines are executed. 31% of introduced bugs are caught.** The gap is made of three things, and every one of them is visible in an individual survivor.

**Survivor 1 — no assertion.**

```python
# mutant in slot/domain/pricing.py:14
-     return RATE * Decimal(hours) * Decimal("0.5") * VAT
+     return RATE * Decimal(hours) * Decimal("5.0") * VAT
# SURVIVED
```

The line is covered by `test_pricing` (L19 §1), which calls it and asserts nothing.

**Survivor 2 — asserted the route, not the result.**

```python
# mutant in slot/app/confirm.py:22
-     booking = repo.confirm(hold_id)
+     booking = None
# SURVIVED
```

Covered by `test_confirm_calls_repo_confirm`, which asserts `repo.confirm.assert_called_once_with("h1")` — **true whatever `confirm` does with the result** (W5 L16 §4, exactly as predicted).

**Survivor 3 — the branch is covered one way only.**

```python
# mutant in roomsvc/bookings.py:349
-     if existing:
+     if not existing:
# SURVIVED
```

Every test books into a free slot. **The conflict path is executed by no test at all** — and this mutant is *the VNC 101 bug*, introduced deliberately, and nothing noticed.

> **Read that last one again.** A mutation tool, in 2026, generated the 2024 incident as a mutant,
> ran 212 tests against it, and **all 212 passed.** That is the most direct statement available of
> what "61% coverage" was worth.

---

## 4. Equivalent Mutants, and Why the Score Is Not 100

**Some surviving mutants are not bugs.** An *equivalent mutant* changes the source without changing behaviour, so no test can possibly kill it.

```python
-  for booking in bookings[:limit]:
+  for booking in bookings[:limit + 0]:        # trivially equivalent

-  if len(items) > 0:
+  if len(items) != 0:                          # equivalent for a list

-  x = compute()
-  return x
+  return compute()                             # equivalent
```

**Detecting equivalence is undecidable in general** — it reduces to program equivalence — so no tool can filter them for you. **Empirically they are 5–20% of survivors**, depending on the code and the operator set.

**The practical consequences, and they matter for how you read your own score:**

1. **A 100% mutation score is not a target**; it is usually not attainable and chasing the last few is chasing equivalents.
2. **The absolute number is less useful than the trend and the distribution.** 31% is bad; whether good is 75% or 85% depends on your code.
3. **Read individual survivors, do not optimise the aggregate.** This is the opposite instruction to coverage, and it is the right one: **each survivor is a specific, checkable claim that your suite would ship a specific bug.**

> **The workflow that works: `mutmut results`, pick ten survivors in code that matters, and for each
> ask "is this a real bug the suite would miss?"** Most of the time the answer is yes and you learn
> something specific. **A 6 makes you do exactly this for ten of them.**

---

## 5. What the Evidence Says

**Better than for most things in this course**, which is why this is the number the project is marked on.

| Finding | Source |
|---|---|
| **Mutants are a valid substitute for real faults** — suites that kill more mutants detect more real faults | Just et al., *"Are Mutants a Valid Substitute for Real Faults?"* (FSE 2014), 357 real faults across 5 projects |
| The mutant-detection/real-fault correlation **holds after controlling for coverage** | *ibid.* — this is the crucial control, and the one Inozemtseva & Holmes showed coverage fails |
| Coverage's correlation with effectiveness **disappears when suite size is controlled** | Inozemtseva & Holmes (ICSE 2014) |
| Mutation testing is usable at industrial scale **if you mutate only the diff** | Petrović & Ivanković, *"State of Mutation Testing at Google"* (ICSE-SEIP 2018) |

**Just et al. (2014) is the paper that justifies this lecture.** It took 357 *real* faults, checked which test suites caught them, and found **mutant kill rate predicts real-fault detection and coverage does not, once size is controlled.** That is as close to a settled empirical result as this field offers.

**Google's practice is the model for how to use it**, because 31 hours per run is not a workflow. They mutate **only the lines changed in a review**, surface a handful of survivors as review comments, and let reviewers mark them useless — which trains the operator selection. **That is Week 7 and Week 8's shape, and it is what your project should aim at by May.**

---

## 6. Making It Tractable

Naive mutation testing is unusable. Four techniques, in order of how much they buy you.

**1. Mutate only what changed.**

```console
$ mutmut run --paths-to-mutate src/slot/domain/pricing.py
```

Or against a diff. **This is the single biggest win** and it is what makes the practice viable.

**2. Only run the tests that cover the mutated line.** `mutmut` and `cosmic-ray` use coverage data to do this automatically; it typically cuts the cost by an order of magnitude.

**3. Keep the suite fast.** Mutation time ≈ *mutants × suite time*. **A 90-second suite is unusable for this and a 5-second one is fine** — which is why L16 §3's budget matters and why W5's feedback note warned about it.

**4. Mutate the domain, not everything.** Your domain package holds the rules and is fast to test. Mutating `main.py`'s route declarations produces noise.

**A realistic configuration for `slot`:**

```toml
# setup.cfg
[mutmut]
paths_to_mutate = src/slot/domain/,src/slot/app/
runner = python -m pytest -x -q --no-header -p no:randomly
```

**Nightly in CI, not on every push** (Week 8), with the result posted somewhere the team sees it.

---

## 7. What Mutation Testing Cannot Tell You

Balance, so you do not over-trust the one good number in the lecture.

| Cannot see | |
|---|---|
| **Missing features** | It mutates code that exists. The `else` you never wrote has no mutant |
| **Wrong specifications** | A perfectly-tested implementation of the wrong rule scores 100% |
| **Concurrency** | Operators are syntactic and single. **The VNC 101 race is only visible as the `if existing:` mutant because the guard exists at all** |
| **Performance, security, usability** | Not behaviour a unit test asserts |
| **Whether the tests are readable** | A suite of unreadable tests can score 90% and still be unmaintainable |

**And one thing it can mislead you about:** a high score on a small, trivial domain layer is easy. **A 75% score on 200 lines of value objects is not the same achievement as 75% on 2,000 lines of rules**, and the final report should give the score *with the line count and the package*.

---

## 8. What This Means for Your Marks

**Stated plainly, because it is unusual and the brief says it:**

> **A project at 95% coverage and a 30% mutation score scores below one at 70% coverage and a 75%
> mutation score.**

**The reason is now fully visible.** Coverage says lines ran. Mutation says the suite would notice. **Just et al. is the evidence that the second predicts real-fault detection and the first does not.** A 95/30 project has a large suite that executes everything and checks little — which is `roomsvc` at a smaller scale, and `roomsvc` is what this course is a reaction to.

**What to report in Phase 1 and in the final:**

```
Coverage (branch):  72.4%   coverage run -m pytest && coverage report   2026-03-02
Mutation score:     68%     mutmut run --paths-to-mutate src/slot/domain 2026-03-02
                            (312 mutants, 212 killed, 84 survived, 16 timeout)
Survivors reviewed: 20, of which 3 were real gaps (now tested), 11 equivalent,
                    6 in code we decided not to test (see docs/debt.md)
```

**The last line is worth more than the numbers above it**, and it is the line that distinguishes a team that ran a tool from a team that used one.

---

## 9. Summary

- **Change the code so it is wrong; run the tests; did any fail?** The mutation score is the share killed, and it is the only number that answers *would a test fail if this broke?*
- **`roomsvc`'s 61% and 31% are reconciled by three survivor types**: no assertion, asserting the route rather than the result, and a branch covered one way only. **The third survivor *is* the VNC 101 bug — generated as a mutant, and all 212 tests passed.**
- **Equivalent mutants are undecidable to detect and are 5–20% of survivors**, so **100% is not a target.** Read individual survivors; do not optimise the aggregate.
- **The evidence is unusually good.** Just et al. (FSE 2014), on 357 real faults: **mutant kill rate predicts real-fault detection after controlling for coverage; coverage's correlation disappears after controlling for suite size.**
- **Make it tractable**: mutate only the diff, run only covering tests, **keep the suite fast** (mutation time ≈ mutants × suite time), and mutate the domain rather than everything. **Nightly, not per push.**
- **It cannot see missing features, wrong specifications, concurrency, performance, or unreadable tests** — and a high score on a trivial domain is easy, so **report the score with the line count.**
- **95/30 scores below 70/75**, and by now you can say exactly why.

**Next:** Week 7 — code review: what the evidence for it actually is, which is both weaker and more interesting than the slogan; and a checklist with teeth.

---

*CS 212 · Week 6 · L21 · © CSE Department*
