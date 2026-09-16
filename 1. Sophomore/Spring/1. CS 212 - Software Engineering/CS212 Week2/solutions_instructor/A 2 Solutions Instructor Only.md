# CS 212 · Assignment 2 — Solutions and Mark Scheme
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for A 2.** The first paper with a diff in it. **Mark the argument, not the
elegance.** A student whose `PricingPolicy` registry is slightly clumsy but who correctly names the
axis of change, the axis they refused, and the cost to a reader has done the thing the week teaches.
A student with a beautiful abstract factory who cannot say what evidence justifies it has done the
thing the week warns about.

**Two automatic caps, and apply them.** Tests failing → 50. One commit, no description → 65. Both
are stated in the paper, both are about reviewability, and reviewability is the course's actual
subject.

**Calibration:** median 66–70. Q4 is where the top decile separates; Q3(a) is where the bottom
quartile reveals itself, because a student who deletes nothing has usually not looked.

---

## Q1: Find the Actors (15)

### (a) [8]

**The seven concerns in `bookings.py`**, with the two not in L08 §1 marked:

| Concern | Lines | Actor |
|---|---|---|
| Permission rules | 291–334 | Registrar |
| Conflict detection and insert | 335–352, 522–544 | Registrar (the booking rules themselves) |
| Price and VAT | 353–418, 1103–1148 | Finance office |
| Email rendering | 419–486 | Communications |
| LDAP department lookup | 487–521 | IT services |
| Audit log (second database) | 545–589 | **Registrar / internal audit** — ⭐ not in the lecture |
| Calendar sync | 590–664 | IT services (different schedule) |
| Cache invalidation by file deletion | 665–698 | **Nobody** — ⭐ not in the lecture, and no actor asks for it |
| Exam special cases | 699–778 | Examinations office |

| | |
|---|---|
| 5 | Seven or more concerns with line ranges |
| 3 | Actors attached, and **at least one concern beyond the lecture's five** |

**The cache-invalidation row is the interesting find** and deserves a comment in feedback: a concern
with **no actor** is either dead or it belongs to infrastructure and has leaked upward. Here it is
the latter. A student who spots that "nobody asks for this to change" is a diagnostic in its own
right has understood §1 better than the lecture stated it.

### (b) [4]

Distribution in the reference snapshot, last 60 subjects on `bookings.py`:

| Actor | Commits |
|---|---|
| Registrar (booking rules, permissions) | 21 |
| Finance (price, VAT, invoicing) | 14 |
| Communications (email wording, templates) | 11 |
| IT services (LDAP, calendar, caching) | 9 |
| Examinations | 3 |
| Unclassifiable ("fix", "update", "wip") | 2 |

| | |
|---|---|
| 2 | Counts, roughly matching |
| 2 | **What the distribution adds over the static reading** |

**The answer being looked for:** the static reading says *five actors share a file*; the commit
history says **they share it at comparable rates**, so this is not one owner with four occasional
guests — it is genuinely contended, and **every one of those 14 finance commits was an edit to the
file containing the booking invariant.** Accept also: the 2 unclassifiable subjects are the
traceability gap made concrete.

### (c) [3]

The three sentences should contain: `notify.py` exposes **five methods**, so any test of a caller
must construct a five-method double; nobody does; therefore the callers' notification paths are
untested and the module sits at **3.9%**. **The property is interface width** — the cost is paid in
the tests, not in recompilation, which is the L08 §4 restatement.

**Full marks also for** a student who notes the more direct cause — `notify.send()` does real SMTP
with no seam at all, so the interface width is not even the binding constraint. **That is a better
answer than the lecture's** and should be said so.

---

## Q2: The Open/Closed Case, With Evidence (20)

### (a) [6]

| Kind | Added | Commit | Files touched |
|---|---|---|---|
| `lecture`, `seminar` | 2020-02 | initial | — |
| `external` | 2020-06 | `e4d2a19` | 3 |
| `exam` | 2021-11 | `1f8c003` | 4 |
| `external_charity` | 2023-09 | `4b21c7d` | 4 |
| `external_partner` | 2024-03 | `7b1e4f2` | **3** |

| | |
|---|---|
| 4 | The table, from `git log`, dates and commits roughly right |
| 2 | The observation that the count is **3, not 4**, for the last one — this is the evidence (b) needs |

**Deduct 2** for a table assembled from the comments in `pricing_before.py` without touching
`git log`. The comments give two of the five dates; the rest require the tool.

### (b) [4]

| | |
|---|---|
| 2 | **`reports.py:212` is the missed site**, shown from the diff |
| 2 | The consequence in plain language |

**The consequence, in finance-officer terms:** *"For eight months, partner bookings were reported as
income at the full rate rather than at 80%, so the room-income figure in the monthly report was
overstated for every partner booking."* Accept any statement that identifies **the report, not the
invoice**, as wrong — the invoice was correct, which is why nobody noticed. **A student who spots
that the invoice was right and only the report was wrong has read the code properly; say so.**

### (c) [10]

**First part [4] — the implementation.** Any shape that satisfies: adding a kind adds a file or a
registry entry and **edits no existing branch**. Accept a dict of callables, a `Protocol` with
subclasses, `functools.singledispatch`, or a table-driven approach. **Do not require classes** — a
dict of `kind -> (multiplier, vatable)` is arguably the best answer here and should get full marks,
because the six cases differ only in a multiplier and the elaborate version is itself speculative
generality.

**Award the full 4 to the dict-of-multipliers answer and note it in feedback.** It is the answer
Week 9's "duplication is cheaper than the wrong abstraction" points at, and about one student in ten
finds it.

**Deduct 2** if the equipment override at the bottom of `price_for` is silently dropped — it is a
real rule, undocumented, and losing it is a behaviour change.

**Second part [3] — the axis.** *"Booking kind"*, with (a)'s evidence: five additions in six years,
each touching three to four files.

**Third part [3] — the axis refused.** The good answers:

- **Not** abstracting the VAT calculation behind a `TaxPolicy`. VAT has changed **once** in six years
  and in one place; a `TaxPolicy` interface is speculative generality.
- **Not** abstracting `RATE_PER_HOUR` per resource. There is no evidence of per-resource rates ever
  being requested.
- **Not** generalising to a rules engine. Named in three previous cohorts and always worth full marks.

**Fourth part [3] — the cost.** Requires a number: *"answering 'what does an external booking cost?'
now requires opening the registry and one policy file — two files instead of one, and the branch
condition is no longer visible at the call site."* **Deduct 2** for "adds a little indirection" with
no count.

---

## Q3: Your Own Project, Audited (25)

### (a) [8]

| | |
|---|---|
| 4 | A complete list, with the second-implementation column filled in honestly |
| 4 | **Something deleted**, with the diff — or a per-abstraction justification for keeping each |

**In a four-week-old project the honest answer is often "we have three abstractions and all are
justified".** Accept it **only** if each row has a named circumstance. A row reading "might need it
later" is not a named circumstance and costs a mark.

**Watch for the two abstractions almost every team has by now**, and which are the interesting cases:

- **A repository wrapper around SQLAlchemy.** Second implementation: almost never. **But** the
  justification that survives is *testing*, not portability — and a student who says so has got
  L08 §5 right.
- **A `Notifier` protocol with one implementation.** Justified, and the named circumstance is real:
  the fake used in tests **is** the second implementation. **Full marks for spotting that a test
  double counts.** It is the correct answer and it is under-appreciated.

### (b) [7]

| | |
|---|---|
| 3 | The import graph, produced |
| 4 | Either a violation found **and fixed in a diff**, or the near-misses named with what keeps them honest |

**The common real violation:** `service.py` importing `HTTPException` from `fastapi` to raise a 409.
**It is the single most frequent boundary leak in this project, every year.** The fix is a domain
exception translated at the edge. Full marks for finding and fixing it; 2 of 4 for finding and not
fixing it.

Second most common: a Pydantic request model used as the domain type, which is stamp coupling
(L07 §4) wearing a type annotation.

### (c) [10]

| | |
|---|---|
| 3 | A real duplication, merged, with the diff |
| **4** | The false one, **left alone**, with L09 §1's test applied explicitly |
| 3 | If done in `roomsvc` instead, same standard |

**The 4 marks are for the divergence scenario**, and it must be specific. *"They might change
differently"* earns 1. *"If the importer has to accept a missing slot and infer it from the previous
row — which the registrar has already asked for in issue #77 — the web form must still reject it,
because a user typing into a form has no previous row"* earns 4.

**Deduct 3** for merging the false duplication. It is the error the question is built to catch and a
surprising number of students do it anyway, because merging feels like progress.

**Other false-duplication pairs in `roomsvc`**, for markers checking the "roomsvc instead" route:
`views.py:412` / `reports.py:88` (the two `range(8,20)` loops **are** real duplication — do not
accept these as false); `notify.py`'s two `render` functions for email and portal (**false** — one
is HTML with a footer required by policy, one is plain text); `auth.py`'s two permission checks for
rooms and equipment (**false**, and this is the good one — they are identical today precisely
because of the Liskov violation in L08 §3, and merging them cements it).

---

## Q4: Disagree With the Scoreboard (25)

### (a) [10]

| | |
|---|---|
| 4 | A clear claim: which letter, which direction, what the correct verdict is |
| 4 | **Concrete code**, cited and real |
| 2 | The argument actually follows from the code |

**The strongest available attacks, for calibration:**

- **I is under-rated.** `typing.Protocol` (PEP 544) plus mypy gives structural typing checked
  statically, so interface width *does* have a mechanical cost in Python now — a wide Protocol makes
  every double fail type-checking. **This is correct and the lecture's verdict is slightly dated.**
  A student who makes it with a mypy error message in the paper should score 9–10.
- **D is over-rated.** Testcontainers makes a real Postgres cheap, so "fast tests" is worth less than
  claimed; and the readable-domain benefit is obtainable by discipline without the inversion. **This
  is a good argument and the honest rebuttal is about test *speed at scale*** — a student who
  anticipates the rebuttal and answers it should score 9–10.
- **L is over-rated for Python.** Weaker than it sounds: the lecture already grants that it applies
  beyond inheritance, and the duck-typed cases are still Liskov violations. **A student making this
  attack should be pushed on Week 10.** Cap at 7 unless they engage with the API-versioning reading.
- **O is not a principle.** Defensible, and the lecture half-concedes it. Needs the student to say
  what a principle would have to do that this does not — i.e. tell you *which* extension. Full marks
  if they get there.

**Deduct 4** for an attack with no code. Deduct all 10 for agreeing with the lecture — the question
says "attack", and this is stated.

### (b) [8]

**Mark this hardest.** The steel-man must include **evidence the lecture did not give**. Examples of
what that looks like:

- Attacking D, the steel-man should cite that `roomsvc`'s test suite takes **94 seconds for 212
  tests** — 0.44 s/test — and extrapolate what an inverted domain layer would do to that at 2,000
  tests. **The lecture never gives that number in this context.**
- Attacking I, the steel-man should note that Python's own stdlib abandoned wide ABCs in favour of
  Protocols precisely because the wide ones were unusable.

A steel-man that merely restates L08's paragraph earns 3 of 8. **A steel-man that makes the lecture's
case better than the lecture did earns 8**, and should be quoted back to the cohort, anonymised.

### (c) [7]

| | |
|---|---|
| 4 | A specific, obtainable observation |
| 3 | If nothing would settle it, **what that implies** |

**The best answers are about their own project by May:** *"if by Week 11 we have swapped no
implementation and our test suite is still under 20 seconds with a real database, D bought us
nothing here and I will say so in the report."* **That is a falsifiable commitment about a real
codebase and it is exactly right.** Score 7.

**The "nothing would settle it" route is fully creditable** and is the more sophisticated answer for
some letters: if no observation could distinguish a codebase that follows S from one that does not,
then S is **advice about how to talk about code rather than a claim about code**, which is not
worthless but is a different kind of thing. **A student who gets there scores 7 and should be told
they have made the lecture's strongest point for it.**

---

## Q5: The Pull Request (15)

**Mark from GitHub, not the PDF.**

| | | |
|---|---|---|
| **5** | Commits | 5: three or more commits, each one change, messages giving the why. 3: separated but messages describe the what. 0: one commit, or messages like "fix", "wip", "A2" |
| **4** | Description | 4 includes **what the student is unsure about**. Without that, cap at 2 however complete the rest |
| **3** | Reviewability | 0 if a formatter run is mixed into a logic commit |
| **3** | Evidence | Test output present; behaviour changes declared |

**The "unsure about" line is worth two of fifteen and is the highest-leverage habit in the course.**
Students who write it get better reviews in Week 7 and better feedback here. **Say so on every paper
that omits it.**

---

## Overall Bands

| Band | |
|---|---|
| **90–100** | Q1(a) finds the actorless concern. Q2(c) gives a file count for the reader's cost and names a refused axis. Q3(a) deletes something or defends every row with a named circumstance. Q3(c)'s divergence scenario is specific. Q4 steel-mans with evidence the lecture omitted. PR is reviewable and says what worries them |
| **75–89** | Refactoring correct and justified, tests green, audit honest, Q4 disagrees with code. Commits separated |
| **60–74** | Fix works; justification restates L08 §2. Audit lists and keeps everything. Q4 paraphrases a suggested bullet. Description thin |
| **45–59** | Code changed without argument or argued without changing. `git log` untouched. One commit |
| **< 45** | Tests broken; or the false duplication merged; or Q4 agrees with the lecture |

**Feedback note for every paper:** name the one abstraction in their `slot` you would delete, and
say what evidence would make you keep it. **Week 3 asks them to defend their architecture**, and
arriving with one concrete challenge already on the table makes that week land much harder.

---

*CS 212 · Week 2 · A 2 Solutions · INSTRUCTOR ONLY*
