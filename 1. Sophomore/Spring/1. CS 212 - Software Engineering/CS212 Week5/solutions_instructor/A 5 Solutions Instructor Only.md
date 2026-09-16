# CS 212 · Assignment 5 — Solutions and Mark Scheme
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for A 5.** **This paper is marked from `git log`, not from the working tree.**
A correct implementation delivered in one commit has failed the assignment, and the caps enforce it.
Read the commit sequence first, before opening any file.

**The three discriminators:**

1. **Is the concurrency test actually concurrent?** Two `requests.post` calls in sequence pass
   trivially and prove nothing. Look for threads, processes, or two open connections.
2. **The fake-it step.** Q3 asks for a deliberate over-simplification forced open by a later test.
   About a third of the cohort will not do it, because it feels like cheating. **It is the whole
   mechanism** and should be marked as such.
3. **Q5's honesty.** A student reporting five clean `-p randomly` runs on a suite with a
   session-scoped database and no rollback fixture is almost certainly not telling the truth or
   not running what they think. **Check the fixture scope.**

**Automatic caps, both stated:** kata in fewer than four commits → 55; sequential "concurrency" test
→ 70.

**Calibration:** median 70–74. This paper marks slightly high because the work is well specified;
the spread is in Q3 and Q5.

---

## Q1: The Concurrency Test (20)

### (a) [12]

| | |
|---|---|
| 5 | **Genuine concurrency** — `ThreadPoolExecutor`, `multiprocessing`, or two explicitly-managed connections |
| 4 | Both assertions: `[201, 409]` **and** exactly one confirmed row |
| 3 | Runs against real Postgres, shown passing |

**4 of 12 for two sequential requests**, per the paper, and the cap applies.

**The mistake to look for, and it is common and subtle:** a "concurrent" test using two SQLAlchemy
sessions bound to **the same connection**, or run inside the rollback fixture. Both serialise, so
the second insert sees the first's uncommitted row within the same transaction and the test passes
for the wrong reason. **Check which fixture it uses.** If it uses `session`, deduct 5 — this is
exactly what (c) is asking about and they have not noticed.

**Acceptable status pairs:** `[201, 409]` is the expected design. Accept `[201, 500]` **only** if
the student flags it as a defect and has an issue for it — an unhandled `IntegrityError` reaching
the client is a real bug and noticing it is worth more than hiding it.

**A model answer, for reference:**

```python
def test_two_concurrent_confirms_yield_exactly_one_booking(committed_db, client):
    resource, slot = "TH200", "2026-03-04T10:00:00Z"
    h1, h2 = make_hold(resource, slot), make_hold(resource, slot)

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(client.post, f"/holds/{h}/confirm") for h in (h1, h2)]
        statuses = sorted(f.result().status_code for f in futures)

    assert statuses == [201, 409]
    assert count_confirmed(resource, slot) == 1
```

### (b) [5]

| | |
|---|---|
| 3 | The constraint or guard removed and the test shown failing |
| 2 | The failure output is the **right** failure — two 201s, or a count of 2 |

**Deduct 3** for a test shown failing with an error (import failure, fixture error) rather than an
assertion failure. **A test that errors has not been shown to detect the behaviour.**

### (c) [3]

**The answer:** the rollback fixture runs the whole test inside **one uncommitted transaction on one
connection**. Two concurrent clients need **two connections**, and an uncommitted row in one is
invisible to the other, so the unique index is never contended — nothing conflicts, and the test
passes regardless. Also: the rollback fixture cannot roll back work that another connection
committed.

| | |
|---|---|
| 2 | Either correct reason |
| 1 | What they used instead — truncation, a dedicated schema, or a separate database |

---

## Q2: Discharge an Invariant Exhaustively (15)

### (a) [8]

| | |
|---|---|
| 5 | A parametrised test over the **full product**, with legal and illegal branches |
| 3 | It actually passes, and the legal set matches the domain model |

**Deduct 3** for a test that enumerates only the three legal transitions — that is three tests with a
loop, not an exhaustive discharge, and it cannot fail when an illegal transition is wrongly allowed.
**This is the whole point of the question** and about a quarter of students miss it.

**Watch for a subtle correct-looking error:** `product(State, State)` includes the identity pairs
`(HELD, HELD)` etc. Whether those are legal is a real design question — most models say no, and a
student who notices and decides explicitly should be credited in feedback.

### (b) [4]

| | |
|---|---|
| 2 | **Nine now; sixteen with a fourth state** |
| 2 | Why the property matters |

**The answer wanted:** adding a state **automatically extends the test** to every new pair, so the
new state's illegal transitions are checked without anyone remembering to check them. **That is
open/closed applied to a test** (W2 L08 §2) and a student who names it should be told so.

### (c) [3]

| | |
|---|---|
| 2 | An invariant correctly identified as not exhaustively testable |
| 1 | Where it is enforced instead |

**The expected answer is I1** — the uniqueness invariant cannot be exhaustively tested because the
state space is unbounded and the interesting failures are concurrent. **Enforced in the database**
(W3 L10 §6), and demonstrated by Q1's test rather than discharged by enumeration.

**Also creditable:** I4 (opening hours) — the space is large, and the real reason it is not
exhaustive is that the rule is time-qualified. **I5** — enforced by convention and the absence of a
`DELETE` path, which cannot be tested by enumeration at all.

---

## Q3: The Kata, Committed Step by Step (30)

**Read `git log --oneline` first. The mark is largely decided there.**

### [12] The commit sequence

| | |
|---|---|
| 12 | Six or more commits, alternating test and implementation, each small, prefixed |
| 9 | Six or more but clumped — three tests then three implementations |
| 6 | Four or five commits |
| 0 | Fewer than four → **cap the paper at 55** |

**Check the timestamps.** Six commits within four minutes of each other, all pushed at once, is a
history reconstructed by `git rebase` after the fact. **This is not automatically a failure** — say
so in feedback and ask — but combined with a missing fake-it step it usually means the work was done
first and the history staged afterwards.

**Check that each `test:` commit actually fails.** A student can be asked to demonstrate
`git stash`-ing the implementation. In practice, look for whether the test commit precedes the
implementation commit that makes it pass, and whether the test is *specific* enough to have failed.

### [6] The fake-it step

| | |
|---|---|
| 6 | A commit containing a deliberate over-simplification, **and the PDF names the later test that forced it open** |
| 3 | An over-simplification present but not identified in the PDF |
| 0 | Every implementation commit is the general solution |

**This is the question's core.** The model is L17 §2's step 2: a special case on `CANCELLED` that
step 3 makes untenable. **Look for the same shape** — a hard-coded return, a single-case `if`, a
constant where a computation belongs.

**Full marks also for a student who reports that they tried to fake it and the next test did not
force it open**, and analyses why. **That is a real and instructive outcome** — it usually means
their second test was too similar to the first — and should score 6 with a note.

### [6] The refactor commit

6 for a commit that changes structure with tests green before and after, and **no behaviour change**.
Check the diff: if a `refactor:` commit changes an assertion or adds a branch, it is not one.
**Deduct 3** and say so; W9 makes this precise and it is worth establishing now.

### [6] Behavioural not structural

| | |
|---|---|
| 6 | Assertions are on results; any interaction assertion is argued |
| 3 | One or two `assert_called_with` assertions, unargued |
| 0 | The suite is mostly interaction assertions |

**The argued case is real and must be honoured:** *"the notification going out **is** the behaviour
here; there is no state to observe, so a spy is correct"* — full marks.

---

## Q4: Doubles, Chosen Deliberately (20)

### (a) [8]

| | |
|---|---|
| 5 | A complete table with correct classification |
| 3 | Locations accurate (spot-check two) |

**The classification error to expect:** calling everything a mock, and in particular calling a
hand-written fake a "stub". **The distinguishing question is whether it has working behaviour**: a
stub returns canned answers, a fake has an implementation. `FakeBookingRepo` with a dict inside is a
fake; `Mock(return_value=booking)` is a stub.

**"We have no doubles" is a legitimate answer** and is true for teams with integration-only suites.
Award the full 8 if they then state the cost honestly — **suite time and diagnostic precision**: a
failure tells them something in the stack is wrong, not which function.

### (b) [8]

| | |
|---|---|
| 5 | The diff: a real replacement or extraction into `tests/fakes.py` |
| 3 | **Which of L18 §2's four problems it removes**, named specifically |

The four: asserts wording; asserts call shape; does not assert the thing happened; silent pass on a
typo. **A student who says "it's cleaner" scores 0 of the 3.**

### (c) [4]

| | |
|---|---|
| 2 | The typo'd assertion shown passing |
| 2 | `autospec=True` shown catching it |

Expected output:

```
>>> notify = Mock()
>>> notify(1, "x")
>>> notify.assert_called_once_wiht(1, "x")     # typo -- passes
>>> notify = create_autospec(send_notification)
>>> notify(1, "x")
>>> notify.assert_called_once_wiht(1, "x")
AttributeError: Mock object has no attribute 'assert_called_once_wiht'
```

**Accept `spec_set=` or `create_autospec` equally.** A student who also notes that pytest's
`--strict-markers` and `mock.patch(autospec=True)` are the same class of fix has read around.

---

## Q5: Is Your Suite Trustworthy? (15)

| | |
|---|---|
| 3 | Suite time from CI, plus the charter's budget |
| **4** | **Five `-p randomly` runs, reported honestly** |
| 3 | A test renamed to a sentence, before and after |
| 3 | Explicit order-independence verdict |
| 2 | One structure-coupled test found, fixed or justified |

**The 4 marks are for honesty and diagnosis, not for passing.** The paper says so. Marking guidance:

- **Five clean runs, with a session-scoped DB and a rollback fixture:** plausible. 4.
- **Failures reported, with the shared state named** — a module-level list, a session-scoped fixture
  mutated by a test, a `datetime.now()` boundary, an autoincrement id assumed: **4, and praise it.**
- **Failures reported with no diagnosis:** 2.
- **Five clean runs claimed on a suite with obvious shared state:** 1, and ask them to run it in the
  Phase 1 viva.

**The rename [3]:** look for a name that states the behaviour and the expectation.
`test_confirm_2` → `test_confirming_a_slot_that_is_already_taken_is_rejected`. **Deduct 1** for a
rename that is merely longer without being a sentence about behaviour.

---

## Overall Bands

| Band | |
|---|---|
| **90–100** | Genuinely concurrent test, shown failing with the right failure. Exhaustive product test. Six-plus alternating commits with an identified fake-it step and a clean refactor commit. A mock replaced by a fake with the problem named. `-p randomly` run five times with a real diagnosis |
| **75–89** | All parts present and correct. Commits show the loop coarsely. Doubles classified right. Suite audited with numbers |
| **60–74** | Concurrency test lacks the failure demo, or uses the rollback fixture. Kata in four commits, no fake-it step. Q4(a) confuses stub and mock. Q5 run once |
| **45–59** | Tests written after and committed as one (capped at 55). No failure demonstrated anywhere. Q2 enumerates only legal transitions |
| **< 45** | No concurrency test, or a suite that does not run |

**Feedback note for every paper:** tell them their suite's current runtime and whether it is on
track for the budget. **Week 6 adds mutation testing, which multiplies suite time by roughly the
number of mutants**, and a team at 90 seconds now will find `mutmut` unusable. **Better they hear it
this week.**

---

*CS 212 · Week 5 · A 5 Solutions · INSTRUCTOR ONLY*
