# CS 212 · Assignment 3 — Solutions and Mark Scheme
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for A 3.** There is no correct architecture, so **every mark here is for
reasoning, evidence and honesty.** A modular monolith defended with numbers beats a hexagonal
architecture asserted; a hexagonal architecture defended with a measured container startup time
beats both.

**The three things that actually discriminate**, and they recur in every band:

1. **Negatives in the ADRs.** Present and concrete, or absent. This is the single best predictor of
   the rest of the paper.
2. **Whether the architecture test was made to fail.** Q3(a) asks for the failing output. A student
   who only shows it passing has not checked that it checks anything.
3. **Q5(b)'s falsifiable observation with a week number.** It separates students who have understood
   that these are cost hypotheses from students reciting a preference.

**Automatic cap: ADRs not in the repository → 60.** Check the repo, not the PDF. Every year several
students paste the ADRs into the paper only, and the whole point is that they live next to the code.

**Calibration:** median 70–74. This paper marks higher than A 2 because there is no code to break.

---

## Q1: Rank, Then Choose (20)

### (a) [6]

| | |
|---|---|
| 3 | A complete ranking of all seven |
| 3 | **Top three each tied to a requirement or a measurement**, 1 each |

**The defensible ranking for `slot`** is roughly testability → modifiability → deployability →
security → performance → availability → scalability. **Do not require this order.** Accept any order
with reasons; a team that ranks security second because they are handling university SSO has argued
it, and that is the mark.

**Deduct 1 per top-three item** justified by a general preference — *"testability, because tests are
important"*. The standard in the paper is a number or a named constraint.

**What a full-marks (a) looks like:**

> 1. **Testability** — we measured a Postgres-backed test module at 1.2 s and container startup at
>    9 s on the CI runner; at the ~200 tests the brief implies, a container-per-module suite is a
>    4-minute loop and we will stop running it.
> 2. **Modifiability** — the requirements in our backlog have already changed twice in three weeks
>    (issues #7 and #19 were both rewritten after we spoke to the departmental administrator).
> 3. **Deployability** — Phase 1 and the final are both live demos, and our charter's Definition of
>    Done requires CI green, so a deploy we cannot do in a minute blocks every merge.

### (b) [6]

| | |
|---|---|
| 3 | An attribute ranked low **with what is given up stated concretely** |
| 3 | What would have to change for it to move |

**Scalability is the expected answer and is correct.** Full marks require the sacrifice named:
*"we will not handle a load test; if the department ever opened booking to all 4,000 students at
registration we would have a thundering-herd problem on one Postgres instance."*

**Availability is the more interesting low-ranked answer** and should be praised: *"we accept that
a single container restart drops in-flight requests; a booking system used by 40 staff can be down
for two minutes."*

**Deduct 3** for a ranking with no sacrifice — *"we ranked them all highly"*. The paper says
explicitly that this is not a ranking.

### (c) [8]

| | |
|---|---|
| 4 | The architecture described clearly enough for an outside reader |
| 4 | **Each of the top three mapped to a structural feature**, not to an intention |

**The mapping is the mark.** *"Testability → the domain package imports nothing external, enforced
by `tests/test_architecture.py`, so domain tests run with a fake repo in ~1 ms"* is a structural
feature. *"Testability → we will write lots of tests"* is an intention and earns 0 for that row.

---

## Q2: Four ADRs (25)

**Mark from the repository.** Check `git log docs/adr/` — ADRs all committed in one push the night
before are worth noting in feedback even though the paper does not penalise it.

### Per ADR [5 × 4]

| | |
|---|---|
| 1 | Context with a number or an observation |
| 1 | Decision specific enough to be violated |
| **2** | **Two or more concrete negatives** |
| 1 | Alternatives with why each lost |

**Expected content, ADR 1 — the `Slot` representation:**

The **fixed-duration** decision is the expected one and the negatives are well known: cannot express
a 150-minute exam (**which is in the registry's own calendar** — a student who cites it is doing the
right thing); cannot express setup time; a multi-slot booking becomes N rows that must be
created and cancelled atomically. **Alternatives:** `tstzrange` + exclusion constraint, rejected with
its cost (btree_gist, a constraint nobody on the team can read, GiST rather than B-tree).

**A team choosing intervals can get full marks**, and the negatives they must state are: the
invariant is no longer a unique index; the exclusion constraint is now load-bearing and understood
by one person; and query plans change. **If they choose intervals and do not mention the exclusion
constraint, they have not understood W1 L06 §3** — cap that ADR at 2.

**Expected content, ADR 2 — where the invariant is enforced:**

Database, partial unique index. **The four rejected candidates must be rejected for the right
reasons** (L10 §6): the UI is bypassable by `curl`; the API layer cannot see concurrent requests;
the domain layer is exactly `confirm_booking`'s check-then-act; an in-process lock does not span
workers.

**A team that puts it in the domain layer with an advisory lock** — `SELECT … FOR UPDATE` on the
resource row, or `pg_advisory_xact_lock` — **is not wrong and should score well**, provided they say
that the guarantee still comes from the database and that they have chosen a lock over a constraint.
The negatives they owe: serialisation on the resource row, and a rule that every write path must
remember to take the lock. **The constraint version has no such rule, and a team that notices this
asymmetry has understood the lecture better than it stated.**

**Expected content, ADR 3 — the shape:** anything, defended.

**ADR 4:** anything they actually argued about. Good ones seen in previous cohorts: whether
cancellation is a state change or a delete; whether to use Alembic from the start; whether the hold
expiry is a scheduled job or a query predicate (**the last is `roomsvc`'s bug and is a very good
sign**).

### The set [5]

| | |
|---|---|
| 2 | Mutually consistent — ADR 2's placement is possible given ADR 1's representation |
| 2 | **At least one cross-reference by number** |
| 1 | Numbering, dates, statuses all present and sane |

**The consistency check is real and catches people.** A team that chooses intervals in ADR 1 and a
unique index in ADR 2 has contradicted itself, and the whole set caps at 2 of 5.

**Bonus worth mentioning in feedback, not marks:** a team that already has a `superseded` ADR in
Week 3 is doing something right and should be told.

---

## Q3: Enforce One Boundary (15)

### (a) [8]

| | |
|---|---|
| 4 | A working test that inspects imports |
| **4** | **Output of it failing on a deliberate violation** |

**The failing output is half the marks and it is the half people skip.** A test that has never failed
has not been shown to test anything. Accept a screenshot, a pasted `pytest` failure, or a commit that
adds and removes the violation.

**Accept any mechanism**: the `ast` walk from L11 §1, `import-linter` (a real tool; a student using
it and configuring it properly should be praised), a `grep`-based check in CI, or `ruff`'s
`flake8-tidy-imports` banned-api rules. **The tool is not the point; the enforcement is.**

**Common defect:** a test that only checks `src/slot/domain/*.py` and not `rglob`, so a violation in
a subpackage passes. Deduct 1 and say so — it is exactly the kind of gap that makes a control
decorative.

### (b) [4]

4 for a linked green run that includes the test. 2 if the test exists but CI does not run it —
**and say in feedback that a check which does not run on every push is a convention, not a control.**

### (c) [3]

| | |
|---|---|
| 2 | A real unchecked rule |
| 1 | How it could be checked, or why it cannot |

**Good answers:** *"reads may skip layers, writes may not"* — checkable in principle by inspecting
which functions are called from routes, painful in practice. *"Every mutating endpoint is
idempotent"* — not statically checkable; needs a test per endpoint. *"No module imports from inside
another module's package"* — **checkable, and a student who then adds it has done more than asked.**

---

## Q4: Where the Invariants Live (20)

### (a) [10]

2.5 per invariant × 4.

| | |
|---|---|
| 1 | Correct placement |
| 1.5 | **Why narrower and wider are both wrong** |

**Reference placements for the `slot` invariants** (W1 L06 §4):

| Invariant | Correct home | Why not narrower | Why not wider |
|---|---|---|---|
| I1 one confirmed booking per (resource, slot) | **Database** | Domain cannot make check-then-act atomic across workers | Nothing is wider |
| I2 held has expiry, confirmed does not | **Database `CHECK`** | The domain can be bypassed by a migration or a fix-up script | — |
| I3 state transitions | **Domain**, one function | The database *can* do it with a trigger, but the rule is complex and belongs where it is readable | The API layer would let a second caller bypass it |
| I4 slot within opening hours at creation | **Domain** | Database cannot see the resource's calendar cheaply; and the rule is time-qualified | — |
| I5 cancelled bookings are never deleted | **Database permissions / no DELETE path**, plus review | Domain code can always be written to delete | — |

**I5 is the interesting one and should be credited generously.** The honest answer is that it is
enforced *by convention and code review*, not by a mechanism — and a student who says so and
proposes revoking `DELETE` from the application role has given the right answer.

**Deduct 2** if all four are placed in the database. **Deduct 3** if all four are in the domain
layer — that is `confirm_booking`.

### (b) [6]

```sql
CREATE UNIQUE INDEX one_confirmed_per_slot
  ON bookings (resource_id, slot)
  WHERE state = 'CONFIRMED';
```

| | |
|---|---|
| 2 | Correct DDL, **including the partial `WHERE`** |
| 4 | **A real two-session transcript** showing one blocking and failing |

**The `WHERE` clause is load-bearing and half of students omit it**, which makes cancelled and held
bookings collide. Deduct 2 and explain: without it, you can never cancel and rebook a slot.

**The transcript must show the block.** Session B's `INSERT` blocks until A commits, then raises
`duplicate key value violates unique constraint`. A transcript showing two sequential inserts with
no concurrency earns 1 of 4 — **it demonstrates the constraint, not the property the constraint was
chosen for.**

### (c) [4]

| | |
|---|---|
| 2 | Two excerpts: infra translating `UniqueViolation` → `AlreadyBooked`; web translating `AlreadyBooked` → 409 |
| 2 | Why the domain must not raise `HTTPException` |

**The reason:** the domain would then be unusable from the bulk importer, the CLI and the tests — it
would be stamp-coupled to the web framework (W2 L07 §4) — **and the import test from Q3 would fail**,
which is the pleasing part: a student who notices that Q3 and Q4(c) are the same rule seen twice has
understood the week.

---

## Q5: The Case Against Your Own Architecture (20)

### (a) [8]

| | |
|---|---|
| 5 | The strongest case, made properly |
| 3 | Specific to **their** project, not a general argument |

**Cap at 4** for a token caveat — *"hexagonal has a bit more boilerplate"*. The question asks for the
sceptical reviewer's case.

**Full-marks examples:**

- Against a modular monolith: *"our domain currently has 40 lines of rules and 300 lines of
  SQLAlchemy models; the boundary we claim to be enforcing is protecting almost nothing, and the
  import test passes trivially. We may be claiming a property we have not paid for."* **Excellent —
  it attacks the substance rather than the style.**
- Against hexagonal: *"we have one adapter per port and the second implementation in every case is
  the test fake, which means our ports are shaped by our tests rather than by the domain. That is the
  tail wagging the dog, and W2 L08 §7's test is arguably failed."*

### (b) [6]

| | |
|---|---|
| 3 | An **observable** |
| 3 | **A week number**, before the final report |

**Deduct 3** for an unfalsifiable answer — *"if it feels wrong"*. The paper says it must be
checkable.

**Model answers:** *"If by Week 9 our domain tests still require a database container, the import
rule bought us nothing and I will say so in the report."* *"If by Week 10 we have never added a
second adapter to any port, the ports are ceremony."* *"If we ever need to change the mapping layer
for a reason other than a schema change, the mapping is doing work we did not intend."*

### (c) [6]

| | |
|---|---|
| 3 | *What are you buying and who is the customer?* — answered for their own shape |
| 3 | *What does being wrong about the boundary cost?* — with a unit of time |

**Full marks for an honest "nobody".** The paper says so and it must be honoured: *"Our ports buy
testability, and the customer is us, on every push. Nobody outside the team benefits, and we should
stop claiming otherwise in the presentation."* — 6.

**Also full marks for:** *"We did not decide; the shape accreted from the walking skeleton and we
are writing ADR 0003 retrospectively to record what we have rather than what we chose."* **L12 §6
rates this above a retro-fitted justification and the mark scheme must agree**, or the incentive is
to lie.

---

## Overall Bands

| Band | |
|---|---|
| **90–100** | Ranking with a named sacrifice. ADRs with concrete negatives, cross-referenced, consistent. The architecture test shown failing. A real two-session transcript. Q5(b) commits to an observable and a week |
| **75–89** | Sound throughout. ADRs have negatives but thin ones. Test in CI, passing only. DDL correct with the partial index. Q5 makes a real case without a falsifier |
| **60–74** | Ranking is preference. ADRs lack alternatives or negatives. Invariants placed correctly but undefended. Q5 is a caveat |
| **45–59** | ADRs are decisions with no context. No test, or a test that cannot fail. DDL missing the `WHERE`. Q4(b) is two sequential inserts |
| **< 45** | ADRs not committed (capped at 60 anyway). Architecture asserted. Q5 agrees with the team |

**Feedback note for every paper:** quote back their single best negative consequence from Q2 and
say whether you agree it is a cost. **Week 6's Phase 1 viva asks about exactly this**, and a student
who has already had one negative taken seriously will write better ones for the final report.

---

*CS 212 · Week 3 · A 3 Solutions · INSTRUCTOR ONLY*
