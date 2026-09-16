# CS 212 · Software Engineering
## Week 2 · Lecture 3 of 3
### DRY, YAGNI, Separation of Concerns — and When Each Is Wrong

---

**Sat:** Thursday of Week 2, 10:00–10:50, TH 200 · **Reading:** Hunt & Thomas, *The Pragmatic Programmer*, §7 · **Next:** Week 3, architectural patterns

---

## 1. DRY Is Not About Duplicate Code

**The actual statement**, from Hunt & Thomas (1999):

> *"Every piece of **knowledge** must have a single, unambiguous, authoritative representation
> within a system."*

**The word is knowledge, not code**, and the substitution is where most DRY damage comes from.

**Two pieces of code that look identical but encode different knowledge are not duplication**, and merging them creates a coupling between two things that have no reason to change together. When they later diverge — and they will, because they were always different — you get a function with a boolean parameter, then two, then the `if` tree from L08 §2.

**`roomsvc` has both errors, one of each kind.**

### Real duplication (merge it)

The 50-minute slot grid is computed in four places:

```console
$ grep -rn 'range(8, 20)' roomsvc/
roomsvc/views.py:412:      for hour in range(8, 20):
roomsvc/reports.py:88:     hours = list(range(8, 20))
roomsvc/bookings.py:1502:  if slot.hour not in range(8, 20):
roomsvc/calendar_sync.py:203: for h in range(8, 20):
```

**One piece of knowledge — *the department books 08:00 to 19:00* — in four representations.** When the library extended to 21:00 in 2023, three of the four were updated. `calendar_sync.py` was not, and library bookings after 19:00 have been invisible in exported calendars ever since. **Issue #1044, open.**

### False duplication (do not merge it)

```python
def validate_booking_request(data):        # views.py:88
    if not data.get('resource'): raise ValidationError(...)
    if not data.get('slot'):     raise ValidationError(...)

def validate_import_row(row):              # importer.py:40
    if not row.get('resource'): raise ImportError(...)
    if not row.get('slot'):     raise ImportError(...)
```

**These look identical. They are not the same knowledge.** One is *"what a web form must contain"*; the other is *"what a row of the registrar's spreadsheet must contain"*. They coincide today. In 2025 the importer needed to accept a missing slot and infer it from the row above — and because someone had merged them in 2022 into `validate(data, mode='web'|'import')`, that change landed in the web path too. **`git show 3d91e0a` is the merge; `git show a72bc14` is the incident three years later.**

> **The test that distinguishes them, and it is the only test worth memorising:**
> **would a single change to the world require both to change, always, in the same way?**
> If yes, one piece of knowledge — merge. If you have to imagine a scenario where one changes and
> not the other, **they are different knowledge that happens to look alike.** Leave them.

**Sandi Metz's rule from L08 §7 is the same rule seen from the other side:** *duplication is far cheaper than the wrong abstraction.* Duplication costs you an edit in two places. The wrong abstraction costs you a parameter, then a flag, then a branch, then a rewrite — and it costs it to somebody who does not know why the abstraction exists.

---

## 2. Rule of Three

The practical heuristic, from Roberts via Fowler's *Refactoring*:

> **The first time, write it. The second time, wince and duplicate it. The third time, refactor.**

**Why three and not two?** Because two occurrences give you one axis of variation, and you will guess the abstraction from it — and guess wrong about half the time. **Three occurrences show you what actually varies.**

**This is the same argument as L08 §2's "demonstrated axis of change"**, and it generalises: you cannot design an abstraction from one example, you can barely do it from two, and three is where the shape becomes visible. **`roomsvc`'s pricing `if` tree has six cases, and the right abstraction is obvious from the sixth in a way it was not from the second.**

---

## 3. YAGNI

**"You Aren't Gonna Need It."** From Extreme Programming; Ron Jeffries' formulation: *always implement things when you actually need them, never when you just foresee that you need them.*

**The evidential basis is W0 L02 §5**: 45% of delivered features are never used, 19% rarely. **You are systematically wrong about what will be needed, and so is everyone else.**

**The cost of building something speculatively is four costs, not one**, and only the first is obvious:

| Cost | |
|---|---|
| **Building it** | The obvious one, and the smallest |
| **Carrying it** | It is in every code review, every refactoring, every dependency upgrade, forever |
| **Repairing it** | It breaks, and it breaks in code nobody uses, so it is found late and by a user |
| **Blocking** | **The worst one.** A wrong abstraction built for an imagined need makes the real need harder to satisfy, because six modules now depend on it |

**`roomsvc`'s example is worth the thirty seconds.** In 2021, someone added a plugin system — `roomsvc/plugins/`, 380 lines, a registry, an entry-point loader, documented hooks. **Six years later there are zero plugins.** It is imported by `main.py`, it appears in every dependency graph, and when the project moved to Python 3.11 someone spent two days fixing the entry-point loading for a mechanism nothing uses. **`git log --oneline roomsvc/plugins/` has 31 commits and not one of them adds a plugin.**

### Where YAGNI is wrong

**YAGNI applies to features and abstractions. It does not apply to things that are expensive to retrofit**, and the distinction is the difference between a good engineer and a cargo-culting one.

| Do not defer | Why it cannot be retrofitted cheaply |
|---|---|
| **The security model** | Retrofitting authorisation means auditing every endpoint written without it. `slot` should decide who may do what **before** Week 5 |
| **Database migrations** | The second migration is easy. The first one, applied to a database with data in it and no tooling, is a weekend |
| **The audit trail** | You cannot reconstruct who cancelled what in March if you did not record it in February. **Invariant I5 exists for exactly this reason** |
| **Observability** | Logs and request IDs you did not add are not available during the incident |
| **Anything with a legal or contractual deadline** | Accessibility, data retention, GDPR deletion |

**The distinguishing property:** *can this be added later at a cost proportional to the new work, or does adding it later require revisiting everything already written?* **The second kind is not YAGNI-able**, whatever it feels like.

> **Say this in your ADRs.** *"We are deferring X under YAGNI; it is cheap to add later because
> only the new endpoints will need it"* is an engineering judgement. *"We'll do auth later"* is a
> hope, and it is the single most common Phase 1 deficiency.

---

## 4. Separation of Concerns

Dijkstra, 1974 — and it is the oldest and vaguest of the four:

> *"It is what I sometimes have called 'the separation of concerns'… focusing one's attention upon
> some aspect: it does not mean ignoring the other aspects, it is just that from this aspect's
> point of view, the other is irrelevant."*

**The vagueness is in "concern", and it is doing a lot of work.** A usable operational version, and the one this course uses:

> **Two things are separate concerns if they change for different reasons, at different times, at
> the request of different people.**

**Which is L08 §1's "one actor" test, again** — a third route to the same place, and by now you should be noticing that Week 2's material is one idea with four names.

**The three concerns every web application must separate**, and the ones `slot` will be marked on:

| Concern | Changes when | Must not know about |
|---|---|---|
| **The domain** — booking rules, invariants, state transitions | The registrar changes a rule | HTTP, SQL, email, JSON |
| **The application** — orchestration, transactions, "confirm then notify" | A workflow changes | HTTP; and it knows the domain but not the framework |
| **The infrastructure** — HTTP routing, SQL, SMTP, the calendar API | A library or a vendor changes | Anything about booking rules |

**`confirm_booking` mixes all three in one function**, which is why it cannot be tested without a database, an SMTP server, an LDAP server and an HTTP service — and therefore is not tested, at 47% coverage with eleven tests against ninety-four paths.

**In your walking skeleton this separation is already marked**: `main.py` is infrastructure, `service.py` is application, and the domain is the thing that has not been written yet because the skeleton has no rules. **Week 3 is where you build it and defend the boundaries.**

---

## 5. The Principles Against Each Other

Real design is the conflicts, not the principles. **Four you will actually hit in `slot`:**

### DRY vs. decoupling

Two modules share a helper. DRY says extract it; decoupling says now they change together. **Resolution:** ask whose knowledge it is. If it belongs to neither, it belongs to a third module both depend on — and if you cannot name that third module, it is not shared knowledge and should be duplicated.

### YAGNI vs. open/closed

Open/closed says abstract the extension point; YAGNI says you do not need it yet. **Resolution:** YAGNI wins until the `git log` disagrees. **Rule of three.** L08 §2's pricing case is the worked example: right in 2024, wrong in 2020, and the only thing that changed is the evidence.

### Single responsibility vs. the cost of indirection

Split by actor and you get many small modules; reading a request now touches six files. **Resolution:** split at boundaries that a *change* crosses, not at every conceptual seam. **If two "responsibilities" have never changed independently, they are one responsibility with two names.**

### Separation of concerns vs. getting anything done in a five-person term project

A full hexagonal architecture with ports, adapters and a mapping layer is defensible for a system with twelve developers. **For `slot` it is probably over-built, and Week 3 says so.** **Resolution:** separate the domain from the infrastructure — that boundary pays for itself in test speed by Week 5. **Do not separate further until something hurts.**

> **The general resolution, and the one thing to take from the week:** every principle here is a
> statement about **the cost of future change**. When two principles conflict, ask which change is
> more likely, using evidence rather than imagination — and the evidence is in the `git log`,
> which Week 11 teaches you to read systematically.

---

## 6. What to Do on Monday

Concrete, because A 2 asks for it and Phase 1 marks it.

1. **`grep` your own project for a constant that appears twice.** There is one — the slot duration, the opening hours, or the hold expiry. **Give it one home.** That is real DRY, and it takes ten minutes.
2. **List every abstraction you have and name the second implementation.** Delete the ones you cannot name (L08 §7).
3. **Find one function that takes a flag** — `send_email=True`, `strict=False`. It is probably two functions. Split it and see whether the call sites read better.
4. **Write down the three concerns and check `service.py`.** If it imports `fastapi`, you have a boundary violation in a 40-line project, and it is much cheaper to fix now than in a 4,000-line one.
5. **Add one line to an ADR:** what you are deferring under YAGNI, and why it is cheap to add later. **If you cannot write the second half, do not defer it.**

---

## 7. Summary

- **DRY is about knowledge, not code.** Two identical fragments encoding different knowledge are not duplication, and merging them couples things that will diverge. **The test: would one change to the world require both to change, always, in the same way?**
- **`roomsvc` has both errors**: `range(8, 20)` in four places, three updated in 2023 — and a 2022 merge of two lookalike validators that caused an incident in 2025.
- **Rule of three.** Two occurrences give one axis of variation and you will guess wrong; three show you what actually varies.
- **YAGNI's cost model has four terms**, and *blocking* is the worst: a wrong abstraction makes the real need harder. `roomsvc`'s plugin system is 380 lines, 31 commits and **zero plugins**.
- **YAGNI does not apply to what cannot be retrofitted proportionally**: the security model, migrations, the audit trail, observability, legal deadlines. **Say which kind you are deferring, in the ADR.**
- **Separation of concerns, operationally: things that change for different reasons, at different times, at different people's request.** Domain, application, infrastructure — and `confirm_booking` mixes all three, which is why it is untestable and therefore untested.
- **Week 2 is one idea with four names.** Cohesion, single responsibility, separation of concerns and Parnas's information hiding are the same question asked four ways: *what changes together?*
- **The conflicts are the design.** Resolve them with evidence from the `git log`, not with imagination.

**Next:** Week 3 — architecture. Where the three concerns become three layers, where an invariant gets a home, and where "microservices" gets asked what it bought.

---

*CS 212 · Week 2 · L09 · © CSE Department*
