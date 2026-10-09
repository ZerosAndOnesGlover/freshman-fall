# CS 212 · Software Engineering
## Week 11 · Lecture 3 of 3
### Documentation That Survives

*“When you feel the need to write a comment, first try to refactor the code so that any comment becomes superfluous.”* — Martin Fowler, *Refactoring* (1999)

---

**Sat:** Thursday of Week 11, 10:00–10:50, TH 200 · **Reading:** Procida, *Diátaxis*; Nygard on ADRs (re-read) · **Next:** Week 12, presentations, management and career paths

**Coursework:** 📝 **Assignment 10** due Fri this week 17:00 · 📝 **Assignment 12** released Wed of Week 12 17:00, due Fri of Week 12 17:00

---

## 1. Why Documentation Rots

**Not laziness. Structural.**

> **Code is executed, so it cannot silently become false. Prose is not executed, so it silently
> becomes false and looks identical either way.**

**That asymmetry is the whole subject**, and it produces the observed pattern: documentation is accurate on the day it is written, decays continuously, and — crucially — **gives no signal while decaying.** A stale test fails. A stale README looks exactly like a fresh one.

**Which yields the only reliable design rule available:**

> **Documentation survives in proportion to how close it lives to the code, and how much of it a
> machine checks.**

**`roomsvc`'s `docs/` directory is the demonstration:**

```console
$ ls roomsvc/docs/
architecture.md  api.md  deployment.md  onboarding.md
$ git log -1 --format=%cd --date=short roomsvc/docs/architecture.md
2021-06-14
$ git log -1 --format=%cd --date=short roomsvc/                    # the code
2025-12-15
```

**The architecture document describes a system that has been changed 1,800 times since it was written.** It is not merely stale; **it is actively misleading**, because a new developer will trust it, and it is worse than nothing.

---

## 2. Four Kinds, With Different Half-Lives

**The Diátaxis framework** (Daniele Procida) separates four things that get mixed into one `docs/` folder and are then all wrong together.

| Kind | Answers | Reader | Half-life |
|---|---|---|---|
| **Tutorial** | *"Get me started"* | A newcomer, learning | **Short** — every step breaks |
| **How-to guide** | *"How do I do X?"* | A practitioner, working | **Short** |
| **Reference** | *"What are the parameters?"* | Someone who knows what they want | **Long, if generated** |
| **Explanation** | *"Why is it like this?"* | Someone deciding something | **Longest — it is about reasons, and reasons do not change when code does** |

**Two conclusions follow, and they are the practical content of this lecture:**

1. **Generate reference. Never write it by hand.** Your OpenAPI document (W10) is generated from annotations, so it cannot lie. A hand-written API table is stale within a fortnight.
2. **Explanation is the highest-value thing you write**, because it is the only kind that does not rot — and **it is the only kind that cannot be recovered from the code.** You can reconstruct *what* by reading; you can never reconstruct *why*.

> **`roomsvc`'s canonical loss:** `confirm_booking` checks `slot.is_provisional` **twice**. `git log -S`
> finds the commit; the message is `"fix"`. Nobody knows why. **The what is in the code and the why
> left the department in 2023** — and this is what the `docs/` directory should have contained and
> did not.

---

## 3. Documentation a Machine Checks

**The only documentation that stays true.** In descending order of value per minute spent.

**1. Types.** A signature is documentation that cannot drift:

```python
def confirm(hold_id: UUID, repo: BookingRepo, clock: Clock) -> Booking: ...
```

**Tells you what it needs, what it returns, and — by omission — that it does not touch HTTP or SMTP.** `mypy` checks it on every push.

**2. Tests as specification.** A well-named test is an executable claim:

```python
def test_a_confirmed_booking_cannot_return_to_held(): ...
```

**Nine parametrised cases document invariant I3 exactly, and fail if the documentation becomes false.** This is why W5 L18 §3 recommended BDD's phrasing — a sentence-shaped test name is documentation with a build step.

**3. Executable examples.** `doctest`, or a tested README snippet:

```python
>>> Slot.from_iso("2026-03-04T10:00:00Z").end
datetime.datetime(2026, 3, 4, 10, 50, tzinfo=datetime.timezone.utc)
```

**4. The architecture test** (W3 L11 §1). Twelve lines of `ast` asserting that the domain imports nothing external. **It is a statement about your architecture that fails when it stops being true** — which is more than any diagram has ever done.

**5. Generated reference.** OpenAPI from annotations; `--help` from the argument parser.

**6. A tested README.** Put the quickstart in CI:

```yaml
- run: docker compose up -d --wait
- run: curl -fsS -X POST localhost:8000/v1/bookings -d @docs/example.json | jq -e '.state=="HELD"'
```

**Now "how to run this" cannot rot**, and it is the one document read by a stranger under time pressure — at Phase 1, on Demo Day, and by next year's team.

---

## 4. What Must Be Prose, and How to Keep It

**Four things a machine cannot check, and they are exactly the four worth writing.**

| | Where it lives | Why it survives |
|---|---|---|
| **Why a decision was made** | `docs/adr/` | **Immutable and dated.** A superseded ADR is still true about the day it was written |
| **What the domain means** | `docs/domain-model.md` | Changes only when the domain does |
| **What you know is wrong** | `docs/debt.md` | L34 §4 |
| **Why this line is strange** | A comment, at the line | **Right next to the thing it explains, so it moves when that moves** |

**On comments, and the course disagrees with two of its own books here** (syllabus §7.2):

```python
# Two checks, deliberately. The second catches the case where the hold was
# provisionalised by the bulk importer between our read and the transaction
# (registrar's requirement, issue #219). Removing either reintroduces #219.
if not slot.is_provisional: ...
```

**That comment is the most valuable thing in the file**, and it is exactly what `roomsvc` lacks. *Clean Code* would call it a failure to make the code clear. **It is not: no arrangement of code expresses "the registrar asked for this in 2021 and here is the issue".**

> **The rule: a comment explaining *what* is a naming failure. A comment explaining *why* is an
> artefact, and it is the first thing lost when authors leave.**

**And the ADR property people forget:** an ADR is **immutable and superseded, never edited** (W3 L10 §5). **A stale ADR is not wrong** — it is a correct record of what was decided and why, on a date. **This is the only kind of prose documentation that is immune to rot by construction**, and it is why the final report asks for one you would now decide differently.

---

## 5. The Onboarding Test

**The one empirical test of documentation, and it is cheap.**

> **Hand your repository to somebody who has never seen it. Watch. Do not help. Write down where
> they get stuck.**

**That list is your documentation backlog, and it is evidence rather than opinion.** You did this in Week 3's checkpoint; **do it again this fortnight**, because the codebase has doubled since.

**What it reliably finds, every cohort:**

- **The quickstart is wrong.** A step was added and not written down; an environment variable is assumed.
- **A vocabulary assumption.** They do not know what "hold" means, and your README never says.
- **An undocumented prerequisite.** Docker version, a Python version, a `.env` file that is gitignored and mandatory.
- **A tool nobody wrote down.** `uv`, `alembic`, `just` — obvious to you, invisible to them.

**And it doubles as W7's shared-blind-spot exercise**, which is why A 7 Q3(c) was worth six marks: **an outside reader is the only instrument you have for finding what your team assumes.**

---

## 6. What to Have by 1 May

**The final report is marked partly on these, and every one is already required by an earlier week.**

| Document | Required since |
|---|---|
| `README.md`, **with a quickstart tested in CI** | Week 1 |
| `docs/domain-model.md`, with the Invariants section | Week 1 |
| `docs/charter.md` | Week 1 |
| `docs/adr/` — **including at least one superseded** | Week 3 |
| `docs/retro-*.md` × 6 | Weeks 2, 4, 6, 8, 10, 12 |
| **`docs/debt.md`** | **This week** |
| Generated OpenAPI, committed | Week 10 |

**Nothing on that list is new work.** What Week 11 adds is `docs/debt.md`, and **what it asks of the rest is that you check they are still true** — which is fifteen minutes with the onboarding test and a look at the ADR dates.

---

## 7. Summary

- **Documentation rots for a structural reason: code is executed and cannot silently become false; prose is not and does.** A stale test fails; **a stale README looks exactly like a fresh one.** `roomsvc`'s architecture document describes a system changed 1,800 times since, and is **worse than nothing** because a newcomer trusts it.
- **Documentation survives in proportion to how close it lives to the code and how much a machine checks.**
- **Four kinds with different half-lives.** **Generate reference; never hand-write it.** **Explanation is the highest-value thing you write**, because reasons do not change when code does — **and *why* is the only thing that cannot be recovered by reading.**
- **Six kinds a machine checks**: types, **tests as specification**, executable examples, **the architecture test** — a statement about your design that fails when it stops being true — generated reference, and **a README quickstart run in CI.**
- **Four things must be prose**: why a decision was made, what the domain means, what you know is wrong, and why a strange line is strange. **A comment explaining *what* is a naming failure; a comment explaining *why* is an artefact** — and `roomsvc`'s double `is_provisional` check is what its absence costs.
- **An ADR is immutable and superseded, never edited**, which makes it **the only prose documentation immune to rot by construction.**
- **The onboarding test is the one empirical measure**: hand it to a stranger, do not help, write down where they stick. **That list is evidence.**

**Next:** Week 12 — presenting engineering work, engineering management, and what to do after this course. Plus the dress rehearsal for Demo Day on 28 April.

---

*CS 212 · Week 11 · L36 · © CSE Department*
