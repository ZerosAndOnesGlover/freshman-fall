# CS 212 · Assignment 6 — Solutions and Mark Scheme
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for A 6.** This is the lightest assignment of the term by design — released the
evening of the midterm, the day after Phase 1. **Almost all the marks are for reading output
carefully rather than for writing code.** Mark the specificity of the reading.

**The three discriminators:**

1. **Q2(b)'s "what it means" column.** Ten rows. A row saying *"we need more tests here"* is 0; a
   row saying *"this is the notification path — if the mutant flipped `if notify:` to `if not
   notify:` and nothing failed, we never test that notification is attempted at all"* is 2.
2. **Whether a proven equivalent is actually proven.** Students classify anything they cannot kill
   as equivalent. A proof is one sentence of reasoning about behaviour, not a shrug.
3. **Q4's controls.** Same as the midterm's C2, and the same error — getting the two papers'
   controls backwards. **This is worth checking against their midterm script.**

**Automatic cap: line coverage only → 70.**

**Calibration:** median 72–76. This paper marks high because the work is mechanical; the spread is
entirely in Q2(b) and Q4.

---

## Q1: Two Numbers, Honestly (15)

### (a) [5]

| | |
|---|---|
| 2 | Both numbers, with command and date |
| 1 | **The branch number reported as the headline** |
| 2 | The biggest-gap file identified, and the kind of code in it |

**The expected finding**, and it should be true of nearly every team: the biggest gap is in whichever
module has the most error handling — typically the web layer or the repository, where `except`
blocks and early returns are half-covered. **A student who notes that the gap is concentrated in
error paths has drawn the right conclusion** (L19 §2) and should be credited even if their
arithmetic is approximate.

**Deduct 1** for reporting line coverage as the headline with branch coverage in a footnote. The
paper says which is the headline.

### (b) [5]

| | |
|---|---|
| 2 | High coverage that means nothing, with **why** |
| 1 | Low coverage that does not matter, with why |
| 2 | Low coverage that does, **with a change count from `git log`** |

**Expected first answer:** their SQLAlchemy models, Pydantic schemas or value objects — **high
coverage as a side effect of everything importing them, with almost no logic to be wrong.**

**Expected second:** a CLI entry point, a `conftest` helper, a migration, `__main__.py`.

**The third requires the `git log` count.** Without a number, cap that part at 1. It is the whole
point of the question — **coverage is only actionable when crossed with change frequency.**

### (c) [5]

| | |
|---|---|
| 3 | A complete list with a reason each |
| 2 | An honest verdict on whether each should be there |

**Most teams will have none**, and the paper anticipates it. **Full marks require checking
`exclude_lines` too** — coverage.py excludes `if TYPE_CHECKING:`, `raise NotImplementedError` and
`if __name__ == "__main__"` by default in many templates, and a student who finds that their config
already excludes `except ImportError` has found a real hidden exclusion.

**Award the full 5 to a team with none who checked both places and said so.**

---

## Q2: Ten Survivors (30)

### (a) [5]

5 for all five figures plus command and date. **Deduct 2** if the run covers the whole package
including web and infra — L21 §6 says mutate the domain and app, and mutating route declarations
produces noise that inflates the survivor count and the runtime.

**Sanity check the numbers.** A team reporting 1,500 mutants on a domain package of 200 lines has
mutated everything. A team reporting 12 mutants has mutated one file.

### (b) [20]

**2 per row, and the mark is in the last column.**

| | |
|---|---|
| 0 | Generic — "needs a test", "not covered" |
| 1 | Correct classification, thin explanation |
| 2 | **Specific**: names the behaviour that would ship broken, or proves the equivalence |

**Calibration for "real gap" rows.** The most common genuine survivors in `slot` at this stage, for
the marker's reference:

| Mutation | Why it survives | Classification |
|---|---|---|
| `if (frm, to) not in LEGAL:` → `in` | If they only test legal transitions | **Real gap** — and it means every illegal transition is permitted |
| `EXPIRY_MINUTES = 15` → `16` | Nothing tests the boundary | **Real gap**, usually |
| `state == CONFIRMED` → `state != CONFIRMED` in a query filter | Fake repo returns everything anyway | **Real gap**, and it reveals fake drift (W5 L18 §2) |
| `return round(price, 2)` → `return price` | No test with a fractional result | Real gap, low severity |
| `x = compute(); return x` → `return compute()` | No behaviour change | **Equivalent** — and the proof is one sentence |
| `list[:n]` → `list[:n+0]` | | **Equivalent**, trivially |
| `if len(items) > 0:` → `!= 0` | Equivalent for a list, **not** for something that can be negative | **Equivalent, with the caveat** — a student who states the caveat gets 2 |
| A mutation in a logging call | Nothing asserts logs | **Deliberate**, if it is in their debt register — otherwise it is a real gap they are choosing to ignore, which is fine **if declared** |

**The "equivalent" proof standard:** one sentence of behavioural reasoning. *"`[:n]` and `[:n+0]`
compute the same slice for all n"* is a proof. *"We couldn't kill it"* is not, and scores 1.

**Deduct across the section** if more than six of ten are classified equivalent — that is well above
the empirical 5–20% and almost always means the student gave up on killing them. **Say so in
feedback and ask them to look again.**

### (c) [5]

| | |
|---|---|
| 3 | Three tests written, shown |
| 2 | The mutants shown killed afterwards |

**The "fewer than three real gaps" escape is legitimate and rare.** If claimed, check their ten rows:
if seven are honestly-proven equivalents, award the full 5 for taking another ten and reporting. **If
they claim it without taking another ten, 2.**

---

## Q3: Three Properties (25)

### (a) [8]

| | |
|---|---|
| 5 | A genuine round-trip property, passing, with the example count |
| 3 | **A first-run failure with the shrunk counterexample reported** |

**The 3 bonus marks should be awarded generously.** Round-trip properties on datetime-bearing objects
fail on the first run most of the time — timezone normalisation, microsecond truncation, ISO format
variants, `Z` versus `+00:00`. **A student reporting a shrunk failure has done the exercise
properly.**

**A student whose round-trip passes first time on 200 examples:** award 5, and check the strategy —
if it generates naive datetimes only, the property is weaker than it looks and that is worth saying.

### (b) [8]

| | |
|---|---|
| 5 | The property, correctly shaped: refuses, **or** produces something satisfying the invariant |
| 3 | It runs and is not trivially true |

**Deduct 4** for a "does not crash" property. L20 §5 names this as the characteristic failure and the
paper repeats it.

**Check that the `except` branch does not swallow everything.** `except Exception: return` makes the
property vacuous, and about one student in six writes it.

### (c) [9]

| | |
|---|---|
| 6 | A `RuleBasedStateMachine` with three or more rules and one `@invariant`, running |
| 3 | **What it cannot find, and why** |

**The 3 marks:** it runs **against the fake, in one process**, so it explores **logic orderings, not
interleavings** — it cannot find the concurrency race, because the fake has no unique index and there
is no second connection. **The answers to that remain the database constraint (W3) and A 5 Q1's
concurrent test.**

**Full marks for a student who adds that the state machine could find an *ordering* bug the
concurrency test never would** — e.g. cancel-then-confirm — **and that the two are complementary
rather than one being better.** That is the right reading and about one in ten finds it.

---

## Q4: The Two Papers (20)

### (a) [8]

| | |
|---|---|
| 4 | **Controlled for suite size** |
| 2 | The correlation largely disappears when they do |
| 2 | Why the uncontrolled version is quoted |

**The last 2:** because the uncontrolled correlation is real, simple, and says something people want
to hear — that a cheap, automatable number measures quality. **Accept any version that identifies
the incentive rather than dishonesty.**

**Deduct 4** for the control stated backwards.

### (b) [8]

| | |
|---|---|
| 3 | 357 real faults; what they measured — which suites detected which faults, against mutant kill rate and coverage |
| 2 | The finding: **mutant kill rate predicts real-fault detection after controlling for coverage** |
| 3 | **Why "real" rather than "seeded" matters** |

**The 3 marks for "real":** validating mutants against seeded faults is **circular** — you are
checking that artificial bugs resemble artificial bugs, and the resemblance is guaranteed by
construction. Real faults, identified from version history by their fixing commits, remove the
circularity. **This is the question's point** and it is worth pressing in feedback if missed.

### (c) [4]

| | |
|---|---|
| 2 | The three-sentence argument |
| 2 | **One honest objection to the marking rule** |

**The argument:** coverage measures execution and its apparent correlation with effectiveness is an
artefact of suite size; mutation score measures whether the suite would notice a change and predicts
real-fault detection independently of coverage; **therefore a high-coverage low-mutation suite is a
large suite that checks little, and the rule ranks them correctly.**

**Acceptable objections, and the marker should be generous here:**

- **Mutation score is gameable too.** Delete hard-to-kill code; mutate only easy packages; **Goodhart
  applies to any measure, including this one** — and the course applies Goodhart to coverage while
  exempting mutation score, which is inconsistent. **This is the best objection and should score 2.**
- **It penalises breadth.** A team testing many modules shallowly may be better positioned than one
  testing a small domain deeply, depending on where the risk is.
- **Neither number sees the things in L21 §7**, so ranking on either is ranking on a partial measure.
- **Small domains score high easily** — which Q5(b) makes them confront about their own project.

---

## Q5: What Your Numbers Do Not Say (10)

### (a) [6]

3 per item, and they must be **concrete about `slot`**, not restatements of the list.

**Strong answers:**

- **Wrong specification** — *"our cancellation permission rule is that an admin may cancel any
  booking. If the registrar actually meant 'any booking in their own department', our suite tests the
  wrong rule perfectly and scores 100% on it."*
- **Concurrency** — *"the state machine and the mutation run both use the fake; the only thing
  standing between us and the VNC 101 bug is one line of DDL and one test, and neither number would
  tell us if the migration had not been applied in production."* **That is an excellent answer.**
- **Missing features** — *"there is no mutant for the hold-expiry job we never wrote, so nothing in
  these numbers reflects that holds currently never expire."*

**Deduct 3** for restating L21 §7 without applying it.

### (b) [4]

| | |
|---|---|
| 2 | Line count reported alongside the score |
| 2 | An honest verdict |

**The honest verdict most teams owe:** *"our domain package is 180 lines, mostly value objects and a
transition table; 80% on that is not comparable to 80% on `roomsvc`'s 2,814-line `bookings.py`."*

**Award the full 4 for a student who says their score is not impressive.** The question is a test of
whether they will state an unflattering fact about their own project, and the final report asks the
same thing at greater length.

---

## Overall Bands

| Band | |
|---|---|
| **90–100** | Branch headline. Coverage read against change frequency with counts. Ten specific survivors with proven equivalents. A shrunk round-trip failure. The state machine's limitation connected to A 5. Both controls correct. An honest objection to the marking rule. An unflattering verdict in Q5(b) |
| **75–89** | Everything run and reported with commands and dates. Survivors classified correctly if thinly. Three working properties. Papers correct |
| **60–74** | Totals reported without distribution. Generic survivor meanings. One trivial property. Papers paraphrased from the lecture |
| **45–59** | Line coverage only (capped at 70 anyway). Mutation run but unread. Q4 from the lecture slides |
| **< 45** | Tools not run, or run against `roomsvc` |

**Feedback note for every paper:** name the single most alarming survivor they found and ask what it
would look like in production. **Week 7's review checklist asks reviewers to look for exactly this
class of gap**, and a student who has already had one named for them reviews better.

---

*CS 212 · Week 6 · A 6 Solutions · INSTRUCTOR ONLY*
