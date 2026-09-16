# CS 212 · Midterm — Solutions and Mark Scheme
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy.** The paper's header promises that a **defended disagreement scores full
marks**, and that promise must be honoured or the course's whole stance collapses. Four questions
have genuinely contested positions — B2, C1, C2 and C3 — and a student arguing against the lecture
with evidence should reliably out-score one reciting it.

**Where a question says "with a number" or "with evidence", cap an answer without one at half.** The
formula sheet supplies every figure, so there is no excuse.

**Time check:** 100 marks in 75 minutes is 45 seconds per mark. Section C at 30 marks is ~22 minutes
for 500–700 words, which is tight. **Mark the essays on argument, not completeness** — an essay that
makes two points well beats one that lists six.

**Calibration:** median 62–66. Section A should be high (most students 24+); B3 and C are where the
spread is.

---

## Section A — Short Answers (30)

**A1 [4].** 2: **architecture is the set of decisions that are expensive to reverse.** 2: the test —
**what would changing this cost in March?** Hours → a detail, stop arguing; weeks → architecture,
write an ADR. *Accept Fowler/Booch phrasing.*

**A2 [4].** 2: **cohesion.** A cohesive module is touched when its one concern changes; `bookings.py`
is touched when any of **eight** change. 2: **it requires no judgement because it is a count from
`git log`**, not an opinion about the code.

**A3 [5].** 2: functional, non-functional/quality, constraint, **invariant**. 1: the double-booking
violated the **invariant**. 2: **an invariant is not something a user wants** — it is something the
system *is* — and it never occurs to anyone that it could be false, so nobody writes a story for it.

**A4 [4].** 1 each for any four of: **missing code** (the `else` never written); **wrong values**;
**concurrency** (the VNC 101 race was in covered code); **missing assertions**; **wrong
specification**; **integration**; **data-dependent paths**. **Deduct nothing for good alternatives.**

**A5 [5].** 1 each, plus 1 for the framing:

- **Adapter** — different interface; make an incompatible thing fit.
- **Facade** — new, simpler interface over several things; hide complexity.
- **Decorator** — same interface; add behaviour transparently.
- **Proxy** — same interface; control access (cache, defer, authorise, remote).

**The 5th mark** is for noting that **Decorator and Proxy are structurally identical and differ only
in intent** — which is the demonstration that a pattern is named for its problem.

**A6 [5].** 2: *"Every piece of **knowledge** must have a single, unambiguous, authoritative
representation within a system"* — **knowledge, not code** (1 of the 2 is for that word). 3: the
test — **would a single change to the world require both to change, always, in the same way?** If
you can imagine a change affecting one and not the other, they are different knowledge that looks
alike.

**A7 [4].** 2: **independent deployability by separate teams.** 1 each for two of: the lost
transaction; partial failure; seven logs; eight containers; refactoring becomes a migration.

---

## Section B — Applied Judgement (40)

### B1. Where the invariant lives [14]

**(a) [6]**

| | |
|---|---|
| 2 | Named: **check-then-act**, a race with no mutual exclusion / TOCTOU |
| **4** | **The interleaving, described** |

The interleaving: worker A runs `confirmed_exists` → false. Worker B runs `confirmed_exists` → still
false, because A has not written anything (or has written uncommitted). A calls `mark_confirmed`;
B calls `mark_confirmed`. **Two confirmed bookings.** The window is between the read and the write,
and in `confirm_booking` it is 200 lines and two network calls wide.

**Deduct 2** for "it has a race condition" with no interleaving. **The interleaving is the answer.**

**Full credit for a student who notes it can also fail under a single worker** if the repo is async
and yields between the two calls — **that is correct and better than the expected answer.**

**(b) [4]**

2: **the database**, as a partial unique index on `(resource_id, slot) WHERE state='CONFIRMED'`.
2: **an invariant must be enforced at the narrowest point every path must pass through.**

**Accept an advisory lock or `SELECT … FOR UPDATE`** for the first 2 **only** if the student says the
guarantee still comes from the database. **Full 4 for a student who notes that the constraint version
has no "every write path must remember to take the lock" obligation and the lock version does** —
that asymmetry is better than the lecture stated it.

**(c) [4]**

2: **the answer** — the domain owns the *rule*; the database owns the *guarantee*. `confirm()` still
catches the integrity error and raises `AlreadyBooked`; the API still returns 409. The rule is stated
in the domain and enforced where enforcement is possible.

2: **what is right about the objection.** This is the mark that separates. Accept any of:

- Rules in the database are **invisible to a reader of the domain code** unless documented.
- They are **written in a different language**, versioned by a different mechanism (migrations), and
  often understood by fewer people on the team.
- **Complex** rules genuinely should not be there — a trigger encoding a permission policy is worse
  than the same policy in Python.
- The general form: **the objection is right about complex, changeable, readable rules and wrong
  about atomicity guarantees under concurrency** — which no application code can provide.

**Deduct all 2** for "the objection is simply wrong."

### B2. The abstraction question [14]

**(a) [5]**

**Expected answer: no.** 3 for the principle — **open/closed applies only against a demonstrated
axis of change**; with two kinds and one site there is no evidence, and abstracting is **speculative
generality**. **Rule of three.** 2 for *what would have to be true*: a known plan to add kinds, or an
existing requirement naming them.

**A defended "yes" can score 5** — the argument being that the registry is *smaller* than the `if`
and costs nothing, so the asymmetry Metz describes does not apply. **Accept it if they engage with
the fact that the abstraction's shape would have been guessed from two examples.**

**(b) [5]**

**Expected: yes.** 3 for the evidence — six kinds, four sites, five additions in six years, and
commit `7b1e4f2` missing a site for eight months. 2: **what changed is the evidence, not the
principle**, and **a developer finds it in `git log`.**

**Deduct 3** if the two answers differ but the student cannot say what changed. **That is the whole
question.**

**(c) [4]**

The asymmetry, and this is the hardest 4 on the paper:

- **Duplication costs a known, local, linear edit.** Three copies means three edits, and each one is
  visible at the site, by someone who can see the context.
- **A wrong abstraction costs a parameter, then a flag, then a branch** — and the cost is paid by
  someone who **does not know why the abstraction exists**, who must now understand all N cases to
  change one, and who will add a flag rather than undo it because undoing it means touching N
  callers.
- **Crucially: duplication is easy to remove later; a wrong abstraction that six modules depend on is
  not.** The operations are not symmetric in cost.

| | |
|---|---|
| 2 | The cost of the wrong abstraction is non-local and compounds |
| 2 | **The asymmetry of reversal** — extracting is routine, un-extracting is not |

### B3. Reading a test [12]

**(a) [6]** — 2 per defect, and **each needs the "would fail although nothing broke" or "would not
detect" clause.** Available defects:

| Defect | The clause |
|---|---|
| **Asserts the message text** | Reword the email → fails, nothing broke |
| **Asserts the call shape** | Refactor `notify(user, msg)` → `notify(Notification(...))` → fails, nothing broke |
| **Does not assert a notification was sent** | Wire `notify` to nothing in production → still passes |
| **`repo.confirm.assert_called_once_with` asserts the route** | `confirm` could discard the result entirely → still passes |
| **`Mock()` accepts any attribute** | `assert_called_once_wiht` → silently passes |
| **No assertion on the returned booking at all** | `confirm` could return `None` → still passes |

**Any three, 2 each.**

**(b) [3]** 2 for a rewrite using a fake repo and a fake notifier, asserting **the returned
booking's state** and **who was notified rather than what was said**. 1 for what it adds — *"it
asserts that confirming produced a confirmed booking, which the original never checks."*

**(c) [3]**

2: **No — the test still passes.** `repo.confirm` is still called once with `"h1"`, which is all the
first assertion checks; the second assertion is on `notify`, and if the message is built from
arguments rather than from `booking`, it is unaffected.

1: **what it tells you.** The line is **covered** and the mutant **survives** — which is exactly the
gap between coverage and mutation score. **Full 3 for a student who says this is survivor type 2
from L21 §3.**

*(If a student argues the test would fail because `notify` is called with data derived from
`booking`, and `booking` is now `None` → `AttributeError`: **that is correct reasoning about a
plausible implementation and scores full marks.** The point of the question is the analysis.)*

---

## Section C — Essay (30)

**Mark on argument.** Rough allocation for all three: **10 for the claim being engaged rather than
described; 12 for evidence used correctly; 8 for the complication or objection being real.**

| Band | |
|---|---|
| **27–30** | Takes a position, supports it with specific evidence from the course, and **handles the strongest objection to its own position.** May disagree with the lectures throughout |
| **22–26** | Clear position, correct evidence, objection acknowledged but not fully answered |
| **17–21** | Describes the debate accurately without taking a position; evidence present but general |
| **12–16** | Summarises lectures; evidence asserted without sources; no objection |
| **< 12** | Off-topic, or contradicts itself |

### C1 — the feedback-loop claim

**The strong answer *attacks* the claim's second half.** "Nothing else about them is common" is
overstated: all of them also assume **the ability to deliver** (a team that cannot deploy gets
nothing from a two-week sprint, W0 L03 §4), and most assume a **stable team**. A student who finds a
second commonality has done the work.

**Evidence expected:** Royce's five fixes as iterative development; the spiral's risk quadrant as a
*different* axis (risk, not latency — **a good student notes this is the counter-example to the
claim's exclusivity**); Kanban's WIP limit and Little's Law; CI as latency reduced to minutes.

**The asymmetry [required]:** mechanical practices have strong evidence (DORA, CI), cultural ones
weak (TDD ordering, pair programming, story points). **Implications a strong essay draws:** the
claim is best supported precisely where the evidence is best; and advice about *how people should
feel* should be discounted relative to advice about *what machines should do*.

### C2 — coverage and mutation

**Must state the controls correctly:**

- **Inozemtseva & Holmes** controlled for **suite size**. The correlation between coverage and
  effectiveness **largely disappears**. 31,000 suites, 5 large Java projects.
- **Just et al.** controlled for **coverage**, using **357 real faults**. Mutant kill rate still
  predicts real-fault detection.

**Deduct heavily for getting the controls backwards** — it is the single most common error and it
inverts the argument.

**The harder question — why is mutation testing not universal?** Expected: **cost** (mutants ×
suite time; `roomsvc` is 31 hours naively); **equivalent mutants** are undecidable and produce noise;
**tooling maturity** varies by language; **it needs a fast, deterministic suite** as a precondition,
which most codebases lack; **and it is a second-order measure**, which is a harder sell to management
than a percentage.

**Which are solvable:** cost (mutate the diff — Google), tooling (improving), suite speed (a choice).
**Not solvable:** equivalence, which is undecidable. **A student who separates these scores at the
top.**

### C3 — `confirm_booking` and length

**Part 1 [defend]:** the nine-four-line-functions test. Every problem survives: VAT in a booking
file, email untestable without SMTP, LDAP outage takes bookings down, calendar POST inside the
transaction, the `INSERT` still 200 lines after the `SELECT`. **The disease is cohesion and
coupling.**

**Part 2 [complicate] — this is where the marks are.** The best answers:

- **Length is a *proxy*, and proxies fail exactly where they are applied as rules.** Long functions
  correlate with low cohesion because a function accumulates length by accumulating concerns — **the
  correlation is real and the causation runs through cohesion.**
- **Length matters directly at the edge**: a function that does not fit on a screen cannot be held
  in working memory, and there is (weak) cognitive-load literature for this. **A student who cites
  the mechanism rather than asserting it scores high.**
- **The verdict on rules of thumb:** a rule wrong about the mechanism can still be useful, because
  it is **cheap to apply and correlated with the thing you want** — *provided* it is applied as a
  smell (look here) rather than as a target (make this number smaller). **Which is exactly the
  coverage argument from Week 6, and a student who connects them has written the best essay
  available on this paper.**

**Award 30 to any essay that reaches that last connection**, whatever its position.

---

## After the Paper

**Return with the cohort-level note**, not just individual marks: which of A1–A7 was weakest, and
which essay was chosen most. **The four contested questions were flagged in advance and in the
reading guide** — report how many students actually disagreed with a lecture, because that number is
the best single measure of whether the course's stance is landing.

---

*CS 212 · Midterm · Solutions and Mark Scheme · INSTRUCTOR ONLY*
