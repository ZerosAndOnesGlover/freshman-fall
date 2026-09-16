# CS 212 · Assignment 5
## Write the Test Suite First — a TDD Kata, Committed Step by Step

---

**Released:** Week 5, Wednesday 17:00 · **Due:** Week 6, Friday 17:00
**Total: 100 points** · Submit **a pull request against your team repository** plus a PDF, `A5_{LastName}_{StudentID}.pdf`

> **This assignment is marked from your commit history.** Not from the final state of the code —
> from the **sequence**. A perfect implementation delivered in one commit scores under half.
>
> **Week 6 holds Phase 1 on Tuesday 3 March and the midterm on Wednesday 4 March.** This assignment
> is due Friday 13 March, so you have the week after both. **Q1 and Q2 should be done before the
> presentation anyway**, because Q2 is a Phase 1 artefact.
>
> Collaboration: the code is your team's; the paper is yours. State who you paired with, if anyone —
> **pairing is permitted and encouraged on Q1**, and costs nothing if declared.

---

### Q1: The Concurrency Test (20 points)

**The test `roomsvc` did not have.** This is the single highest-value artefact in Phase 1 and it is worth doing first.

**(a) [12]** Write an integration test that starts **two concurrent requests** for the same resource and slot against a **real** Postgres, and asserts:

- exactly one receives a success status and one a conflict status;
- **exactly one confirmed booking exists afterwards.**

**It must genuinely be concurrent.** Two sequential calls score 4 of 12. Show the test, and show it passing.

**(b) [5]** **Demonstrate it can fail.** Remove the constraint (or the guard), run the test, and paste the output. Then restore it. **A test never observed failing is not known to test anything** (L17 §1).

**(c) [3]** L16 §5 says the transaction-rollback fixture cannot be used for this test. **Say why**, in two sentences, and say what you used instead.

---

### Q2: Discharge an Invariant Exhaustively (15 points)

**(a) [8]** Take your state-transition invariant (W1 L06 §4's I3, or your equivalent) and test it **exhaustively** with one parametrised test over the full product of states — legal pairs succeed, illegal pairs raise.

**(b) [4]** **Count the cases**, and say what happens to the count when you add a fourth state. Then say why that property is worth more than the test passing today.

**(c) [3]** **Pick one other invariant from your domain model and say honestly whether it can be tested this way.** At least one of yours cannot — say which, why, and where it is enforced instead.

---

### Q3: The Kata, Committed Step by Step (30 points)

**Pick one genuinely new piece of behaviour** in `slot` — not something you have already written. Candidates: hold expiry, the cancellation permission rule, recurring-booking expansion, the "next three free slots" suggestion from W1 L06 §1's extension 4a.

**Do it test-first, properly, and commit every step.**

| | |
|---|---|
| **[12]** | **The commit sequence shows the loop.** Alternating test-then-implementation commits, each small. **Minimum six commits.** A commit message convention that marks which is which — `test:` / `feat:` / `refactor:` — is expected |
| **[6]** | **At least one commit is a deliberate over-simplification** later forced open by the next test. **"Fake it till you make it" is examinable here**, and the PDF must point at the commit and say what forced it |
| **[6]** | **At least one `refactor:` commit with no behaviour change**, tests green before and after |
| **[6]** | The resulting tests are behavioural, not structural (L16 §4): no assertion of the form `mock.assert_called_with` unless the call genuinely *is* the behaviour, argued in the PDF |

**In the PDF [included in the above]:** a table of your commits — SHA, message, and **what you learned from that step.** Three or four rows will say "nothing, it went as expected". **At least one should not**, and that row is what the question is for.

---

### Q4: Doubles, Chosen Deliberately (20 points)

**(a) [8]** Find the places in your existing test suite where you use a test double. **Classify each** as dummy, stub, spy, mock or fake (L18 §1). A table: file, line, kind, what it stands in for.

**If you have none, you have an integration-only suite — say so, and say what that costs you** in speed and in diagnostic precision.

**(b) [8]** **Replace one `Mock` with a fake**, or — if you have no mocks — **convert one inline stub into a reusable fake in `tests/fakes.py`.** Show the diff, and state which of L18 §2's four problems the change removes.

**(c) [4]** **`Mock()` passes silently on `assert_called_once_wiht`.** Demonstrate it: write the typo'd assertion, show the test passing, then show `autospec=True` catching it. Three lines of output.

---

### Q5: Is Your Suite Trustworthy? (15 points)

L18 §5 gives six properties. **Audit yours against the first five** — the sixth is Week 6's.

| | |
|---|---|
| **[3]** | **Fast.** The number, from CI. And your budget, from the charter |
| **[4]** | **Deterministic.** Run `pytest -p randomly` **five times** and report. **If anything fails, that is the interesting result** — diagnose it and say what shared state caused it |
| **[3]** | **Diagnosable.** Pick your worst test name and rewrite it as a sentence. Show both |
| **[3]** | **Order-independent.** Covered by the randomly runs; say explicitly whether you pass |
| **[2]** | **Behaviour, not structure.** Find one test that would break under a pure rename, and either fix it or justify it |

> **A suite that fails `-p randomly` is the expected outcome and is not a bad mark.** It is worth
> more, here, than one that passes — because you found the shared state in Week 5 rather than in
> April. **Report honestly; the marks are for the diagnosis.**

---

## Marking

| Band | |
|---|---|
| **90–100** | The concurrency test is genuinely concurrent and shown failing without the constraint. The kata's commits alternate and one is a fake-it step with the forcing test named. A mock becomes a fake with the problem named. `-p randomly` run five times with an honest diagnosis |
| **75–89** | All parts complete and correct. Commits show the loop but coarsely. Doubles classified correctly. Suite audited with numbers |
| **60–74** | Concurrency test sequential or without the failure demo. Kata delivered in three commits. Q4 classification confused between stub and mock. Q5 run once |
| **45–59** | Tests written after the code and committed as one. No failure demonstration anywhere |
| **< 45** | No concurrency test; or a suite that does not run |

**Automatic caps:** a kata delivered in **fewer than four commits caps at 55**; a concurrency test that is **two sequential requests caps at 70**.

---

*CS 212 · Week 5 · Assignment 5 · 100 points · due Friday of Week 6, 17:00*
