# CS 212 · Quiz 7
## Administered: Tuesday, Week 7 (first 10 minutes of lecture)

**Name:** _________________________________ **Team:** ___________ **Date:** ___________

**Covers Week 6** — coverage, property-based testing, mutation testing.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.

---

**Q1.** Describe a test suite with 100% line and branch coverage that would not catch a single bug.

&nbsp;

&nbsp;

---

**Q2.** Turning on branch coverage takes `roomsvc` from 61.0% to 48.3%. Where does the missing thirteen points live?

&nbsp;

&nbsp;

---

**Q3.** What did Inozemtseva & Holmes control for, and what happened to the correlation?

&nbsp;

&nbsp;

---

**Q4.** Name the three survivor types that explain the gap between 61% coverage and a 31% mutation score. Which one is the VNC 101 bug?

&nbsp;

&nbsp;

---

**Q5.** Why is a 100% mutation score not a target?

&nbsp;

&nbsp;

---

**Q6.** What makes "real faults" rather than "seeded faults" the important word in Just et al. (2014)?

&nbsp;

&nbsp;

---

**Q7.** A `RuleBasedStateMachine` for `slot`'s booking lifecycle cannot find one important class of bug. Which, and why?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **A suite with no assertions.** Call every function, assert nothing:

```python
def test_pricing():
    price("lecture", 1.0)
    price("external_charity", 2.0)
    price("external", 3.0)
```

Every line and branch executes; the suite is green under every possible mutation. **Coverage measures what your tests executed, not what they checked.**

---

**Q2.** **Error paths.** `else` clauses that do not exist, `except` blocks nobody exercises, early returns, guard branches taken one way only. `bookings.py` drops from 47.1% to **31.8%** and has **198 partially-covered branches**.

*`BrPart` is the most valuable column in a coverage report for exactly this reason: reachable, exercised, and half-checked.*

---

**Q3.** **Suite size.** Over ~31,000 suites from five large Java projects, coverage does correlate with test-suite effectiveness — **and the correlation largely disappears once you control for how many tests there are.** Bigger suites both cover more and find more; coverage adds almost nothing once size is known.

---

**Q4.** **1.** No assertion — the line ran and nothing was checked. **2.** Asserted the route, not the result — `mock.assert_called_once_with` is true whatever the function does with the value. **3.** **A branch covered one way only.**

**The third is the VNC 101 bug:** `if existing:` → `if not existing:` in `confirm_booking` **survived all 212 tests**, because every test books into a free slot and the conflict path is exercised by nothing.

---

**Q5.** **Equivalent mutants** — changes to the source that do not change behaviour, so **no test can possibly kill them.** Detecting equivalence is undecidable in general, and empirically they are **5–20% of survivors.**

So: **read individual survivors, do not optimise the aggregate.** Chasing the last few per cent is chasing equivalents.

---

**Q6.** Validating mutants against **seeded** faults is **circular** — you are checking that artificial bugs resemble artificial bugs, and the resemblance is guaranteed by how you made them.

Just et al. used **357 faults that actually shipped**, identified from version history by their fixing commits. That removes the circularity, **which is why the paper carries weight its predecessors do not.**

---

**Q7.** **The concurrency race.** It runs **against your fake, in one process**, so it explores *logic orderings* — hold, confirm, cancel, confirm — **not interleavings**. The fake has no unique index and there is no second connection, so nothing can conflict.

**The answers to the race remain the database constraint and A 5's concurrent test.** The two are complementary: the state machine finds orderings the concurrency test never would.

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L19 §1–2 |
| **Q3, Q6** | **L19 §4 and L21 §5** — A 6 Q4 is these two papers, and getting the controls backwards inverts the argument |
| **Q4** | **L21 §3** — the three survivors are A 6 Q2's classification scheme |
| Q5 | L21 §4 |
| **Q7** | **L20 §6** — and A 6 Q3(c) awards 3 marks for exactly this answer |

**Q3 and Q6 are the ones that recur.** They are the whole justification for the rule that 95% coverage with a 30% mutation score scores below 70% with 75% — which is how your project is marked in May, and which appeared on last week's midterm as essay C2.

---

*CS 212 · Week 7 · Quiz 7 · covers Week 6 · ungraded*
