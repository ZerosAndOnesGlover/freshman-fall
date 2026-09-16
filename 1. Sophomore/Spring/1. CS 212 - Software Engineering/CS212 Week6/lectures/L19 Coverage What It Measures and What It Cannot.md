# CS 212 · Software Engineering
## Week 6 · Lecture 1 of 3
### Coverage: What It Measures, and What It Cannot

---

**Sat:** Tuesday of Week 6, 10:00–10:50, TH 200 · **⚠️ Quiz 6 in the first ten minutes** — covers Week 5 · **Reading:** coverage.py docs, "Branch coverage" · **Next:** L20, property-based testing
**⚠️ Phase 1 presentations follow this lecture. Midterm is tomorrow, Wednesday 4 March, 18:00–19:15, Weeks 0–5.**

---

## 1. The Test Suite With 100% Coverage and No Assertions

Start with the demonstration, because it settles the argument faster than any amount of explanation.

```python
# slot/domain/pricing.py
def price(kind: str, hours: float) -> Decimal:
    if kind in ("lecture", "seminar", "exam"):
        return Decimal(0)
    if kind == "external_charity":
        return RATE * Decimal(hours) * Decimal("0.5") * VAT
    return RATE * Decimal(hours) * VAT
```

```python
# tests/test_pricing.py
def test_pricing():
    price("lecture", 1.0)
    price("external_charity", 2.0)
    price("external", 3.0)
```

```console
$ coverage run -m pytest -q && coverage report --show-missing
1 passed in 0.02s
Name                      Stmts   Miss  Cover   Missing
---------------------------------------------------------
slot/domain/pricing.py        6      0   100%
```

**100%. Every line, every branch. Zero assertions.**

Change `0.5` to `5.0`, invert the `if`, return `None` — **the suite stays green.** It will stay green for every mutation you can make to that function, because it never looked at a result.

> **Coverage measures what your tests *executed*. It says nothing about what they *checked*.**
> That sentence is the whole lecture, and it is why `roomsvc`'s 61% coverage sits beside a 31%
> mutation score.

---

## 2. The Kinds of Coverage, and Which One to Use

| Kind | Asks | Catches |
|---|---|---|
| **Statement / line** | Was this line executed? | The default, and the weakest useful measure |
| **Branch** | Was each branch taken both ways? | **The one to enable.** `if x:` with no else has two branches; line coverage sees one |
| **Condition** | Was each sub-condition true and false? | `if a and b` has four combinations; branch coverage tests two |
| **Path** | Was each path through the function taken? | **Combinatorially impossible.** `confirm_booking` has 94 independent paths and vastly more actual paths |
| **MC/DC** | Modified condition/decision — each condition independently affects the outcome | **Required by DO-178C Level A** for avionics. Expensive, and it exists because the alternative is people dying |

**Turn on branch coverage. It costs one line and it is strictly more informative:**

```toml
# pyproject.toml
[tool.coverage.run]
branch = true
source = ["src/slot"]

[tool.coverage.report]
show_missing = true
skip_covered = true
```

**The difference is not academic.** Here is `roomsvc` measured both ways:

```console
$ coverage report --precision=1 | tail -1          # line coverage
TOTAL                        11438   4461   61.0%

$ coverage report --precision=1 | tail -1          # with branch = true
TOTAL                        11438   5912   48.3%
```

**Thirteen points lower**, and the gap is concentrated exactly where you would expect: error branches, `else` clauses that do not exist, and the `except` blocks nobody exercises. **`bookings.py` drops from 47.1% to 31.8%.**

---

## 3. What Coverage Is Actually For

It is not a goal. **It is a diagnostic, and it answers exactly one question well:**

> **Which code has no test at all?**

That is a genuinely useful question, and it is the one use of coverage that survives every criticism. **Zero coverage on a module is a fact about your test suite, not an opinion.** `notify.py` at **3.9%** is not a subtle finding — 588 of 612 lines have never been executed by a test, and if any of them is wrong, nothing will tell you.

**Three legitimate uses, in descending order of value:**

1. **Find the untested regions.** Sort by coverage ascending, look at the top of the list, and ask whether those files matter. **This is the whole of the good use.**
2. **Coverage of the *diff*.** *"Does this pull request test the lines it added?"* is a much better question than *"is the project above 80%?"*, because it is actionable by the person being asked. `diff-cover` does this; Week 7 puts it in a review checklist and Week 8 puts it in the pipeline.
3. **A ratchet, not a target.** *"Coverage may not decrease"* is a defensible CI rule. *"Coverage must be ≥ 80%"* is not, for the reason in §4.

---

## 4. Why a Coverage Target Is Harmful

**Goodhart's law:** *when a measure becomes a target, it ceases to be a good measure.* Coverage is the textbook case and the mechanism is specific.

**A team required to hit 80% will hit 80%**, and here is how, in ascending order of dishonesty:

| Move | Effect on coverage | Effect on quality |
|---|---|---|
| Test the easy modules — `models.py`, value objects, DTOs | Large gain | **Zero.** These have no logic |
| Delete hard-to-test code paths instead of testing them | Gain | **Negative** |
| Write tests with no assertions (§1) | Gain | **Zero** |
| `# pragma: no cover` on anything awkward | Gain | **Negative** — the pragma marks precisely the code that most needs a test |
| Test the framework's behaviour rather than yours | Gain | Zero, plus maintenance |

**Every one of those is rational under the target**, which is what makes Goodhart's law a law rather than an accusation.

**And the target does not even correlate with what you want.** The research is thin but consistent in direction:

| Finding | Source |
|---|---|
| Coverage and defect density correlate weakly, and the relationship is dominated by module size | Inozemtseva & Holmes, *"Coverage Is Not Strongly Correlated with Test Suite Effectiveness"* (ICSE 2014) — 31,000 suites over 5 large Java projects |
| The correlation that exists largely disappears when suite **size** is controlled for | *ibid.* |
| **Mutation score correlates much better** with real fault detection | Papadakis et al. (2018), and it is the basis of L21 |

**Inozemtseva & Holmes is the paper to know**, and its result is precise: **coverage is correlated with effectiveness, but the correlation is explained by the fact that bigger suites both cover more and find more.** Coverage adds almost nothing once you know how many tests there are.

> **What this course requires**, and it is in the project brief: **no coverage target.** You report
> coverage as a diagnostic and you are marked on your **mutation score** and on whether your tests
> assert anything. **A project at 95% coverage and 30% mutation score scores below one at 70% and
> 75%**, and L21 explains exactly why.

---

## 5. Reading a Coverage Report Properly

Not the total. **The total is the least informative number in the file.**

```console
$ coverage report --sort=cover --precision=1 | head -12
Name                          Stmts   Miss Branch BrPart  Cover
-----------------------------------------------------------------
roomsvc/notify.py               612    588    104      2    3.9%
roomsvc/calendar_sync.py        377    301     88      6   19.4%
roomsvc/admin.py                355    214     71     11   38.2%
roomsvc/bookings.py            2814   1489    702    198   31.8%
roomsvc/reports.py              401    183     66     14   52.1%
roomsvc/auth.py                 488    102     92     18   77.3%
roomsvc/models.py               986     41     22      3   95.6%
```

**Read it in this order:**

1. **The bottom.** `models.py` at 95.6% is not good news — it is a file of column definitions with almost no logic, and its high coverage is a side effect of everything else importing it. **High coverage on a low-logic file inflates the total and means nothing.**
2. **The top, cross-referenced with change frequency.** `notify.py` at 3.9% is bad; whether it is *urgent* depends on whether it changes. It has 122 touches in two years, so yes.
3. **`BrPart`** — partially-covered branches. `bookings.py` has **198**: branches taken one way and never the other. **These are the highest-value coverage findings in any report**, because the code is reachable, exercised, and half-checked.
4. **The intersection with complexity.** `bookings.py`: 2,814 statements, 702 branches, 31.8% covered, complexity 94 in one function. **That intersection is Week 11's hotspot** and is the one actionable line in the file.

**The total — 61%, or 48.3% with branches — appears nowhere in that analysis.**

---

## 6. What Coverage Cannot See, Even at 100%

A list worth keeping, because each item is a real class of bug that a 100%-covered suite ships.

| Invisible to coverage | Example in `slot` |
|---|---|
| **Missing code** | The `else` you never wrote. Coverage measures lines that exist |
| **Wrong values** | Every line executed, `0.5` should be `0.8` |
| **Concurrency** | Both branches covered; the race is in the interleaving. **This is the VNC 101 bug, and it had coverage** |
| **Missing assertions** | §1 |
| **Wrong specification** | The code does exactly what you asked and you asked wrong |
| **Integration** | Every unit covered, the wiring broken. `roomsvc`'s `external_partner` bug (W2 L08 §2) was in covered code |
| **Data-dependent paths** | `if len(items) > 100` covered by a test with 101 items and never by one with 0 |

> **The line that puts coverage in its place:** **coverage tells you where you have definitely not
> looked. It tells you nothing about where you have.**

---

## 7. What to Do This Week

Before Phase 1 — and most of it takes minutes.

1. **Turn on branch coverage.** One line in `pyproject.toml`. **Your number will drop. Report the lower one**; the Phase 1 rubric prefers honesty and A 6 asks for both.
2. **Sort ascending and look at the top three files.** For each: does it matter, and does it change? That is your list.
3. **Look at `BrPart`.** Find one half-covered branch in code that matters and write the missing case. **It is almost always an error path** — which is W1 L06 §1's six extensions arriving again.
4. **Do not chase the total.** Do not add tests to `models.py`. **Do not add a `# pragma: no cover` this week**, and if you already have some, list them for A 6.
5. **Report the number with its date and command** in Phase 1, not as a claim.

---

## 8. Summary

- **A suite with 100% line and branch coverage and no assertions is trivial to construct**, and it stays green under every mutation. **Coverage measures execution, not checking.**
- **Enable branch coverage**; it costs one line. `roomsvc` goes from 61.0% to **48.3%**, and `bookings.py` from 47.1% to **31.8%** — the gap is all error paths.
- **Coverage answers one question well: which code has no test at all.** Use it to find untested regions, to gate the **diff**, and as a **ratchet** — never as a target.
- **A target is Goodhart's law in its textbook form**, and every way of hitting it is rational and useless: test the trivial modules, delete the awkward paths, write assertionless tests, `# pragma: no cover`.
- **Inozemtseva & Holmes (ICSE 2014):** over 31,000 suites, coverage correlates with effectiveness **only through suite size.** Control for size and it adds almost nothing.
- **Read the report bottom-first, then top against change frequency, then `BrPart`** — `bookings.py` has 198 half-covered branches — **and never the total.**
- **Even at 100%, coverage cannot see** missing code, wrong values, concurrency, missing assertions, a wrong specification, integration, or data-dependent paths. **The VNC 101 bug was in covered code.**
- **Coverage tells you where you have definitely not looked, and nothing about where you have.**

**Next:** L20 — property-based testing, where you stop writing examples and start writing the rule, and where Hypothesis finds the case you would never have thought of.

---

*CS 212 · Week 6 · L19 · © CSE Department*
