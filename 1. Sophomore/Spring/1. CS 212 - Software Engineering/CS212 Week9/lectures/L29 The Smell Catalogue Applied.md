# CS 212 · Software Engineering
## Week 9 · Lecture 2 of 3
### The Smell Catalogue, Applied — and the Fix

*“There is a programming smell here… which is kind of like the smell in your refrigerator, you know. There's a sign that there's something wrong, but you can't quite put your finger on it. But you know if you leave it there, its only going to get worse.”* — Ward Cunningham, Geek Noise podcast (2004)

---

**Sat:** Wednesday of Week 9, 10:00–10:50, TH 200 · **Reading:** Fowler, *Refactoring*, 2nd ed., Ch. 3 (the smells) · **Next:** L30, large refactorings

**Coursework:** 📝 **Assignment 9** released today 17:00, due Fri of Week 10 17:00 · 📝 **Assignment 8** due Fri this week 17:00 · 📊 **Quiz 10** Tue of Week 10
**A 9 is released after this lecture**, Wednesday 17:00.

---

## 1. A Smell Is a Hint, Not a Verdict

**Kent Beck's word, and Fowler's framing:**

> *"A smell is a surface indication that usually corresponds to a deeper problem in the system…
> **The nose is a metaphor for something quick and easy to notice.** Smells don't always indicate a
> problem."*

**The "usually" and "don't always" are the important parts.** A smell is a **cheap, fallible signal that says look here** — which is exactly what W6 said coverage is, and exactly what W7 said linter findings are. **Three weeks, three instances of the same epistemic shape**, and the failure mode in all three is treating a signal as a verdict.

**So the procedure for any smell is three steps, and the third is the one people skip:**

1. **Notice it** — the smell's whole value is that this is cheap.
2. **Ask what problem it indicates**, in this code, for a change you are actually making.
3. **Decide whether it is worth fixing now.** Sometimes the answer is no, and **A 9 awards marks for a smell deliberately left** — as A 4 did.

---

## 2. The Smells That Matter, in `roomsvc`

Fowler lists twenty-four. **These nine account for essentially everything wrong with the reference codebase**, and each is given with the refactoring that addresses it.

| Smell | Where in `roomsvc` | The refactoring |
|---|---|---|
| **Long Function** | `confirm_booking`, 487 lines | Extract Function — **but see §3; this is not the real problem** |
| **Divergent Change** | `bookings.py`: **five actors, 891 file-touches in two years** | Split Phase; Move Function. **The most important smell in the file** |
| **Shotgun Surgery** | Adding a booking kind touches **four** files; a 2024 commit missed one for eight months | Move Function; Combine Functions into Class |
| **Duplicated Code** | `range(8, 20)` in **four** places; three updated in 2023 | Extract Function — **but apply W2 L09 §1's test first** |
| **Primitive Obsession** | `state` as a bare `String(20)`, `slot` as a naked `datetime` | Replace Primitive with Object; Replace Type Code with Subclasses |
| **Mysterious Name** | `_entry`, `s`, `do_it`, `process2` | Rename — **the cheapest refactoring, and the most under-used** |
| **Feature Envy** | `reports.py` reaching into `Booking`'s fields to compute what `Booking` should know | Move Function |
| **Message Chains** | `booking.resource.building.campus.timezone` | Hide Delegate; Extract Function |
| **Speculative Generality** | `roomsvc/plugins/`: **380 lines, 31 commits, zero plugins** | **Remove Dead Code.** Delete it |

**Two of these deserve a moment because students consistently mis-rank them.**

**Divergent Change is the most serious and the least visible.** A file with five reasons to change is not ugly to look at; it looks like a big file. **Its damage is measurable only in the `git log`**, and it is the reason a VAT change shipped a permission regression (W2 L08 §1). **It is also the only smell on the list that a linter can never detect.**

**Speculative Generality is the easiest to fix and the hardest to agree to.** Deleting 380 lines that took someone a week feels like waste. **It is not: the waste already happened, and keeping it means paying for it forever** — 31 commits of maintenance, a dependency in every graph, two days lost to entry-point loading on a Python upgrade. **Deletion is a refactoring, and it is the one nobody chooses** (A 4's bonus note said so).

---

## 3. Long Function Is a Symptom, Not the Disease

**W2 L07 §1 argued this and this is where it is settled.**

`confirm_booking` is 487 lines. **Extract nine functions from it and every real problem survives:** the VAT rate still lives in a file about booking rules, the email still cannot be tested without SMTP, the calendar POST is still inside the transaction.

**So what is the right first refactoring?** **Split Phase** — separate the function into stages that pass data forward, then move each stage where it belongs:

```python
# Stage 1: decide.  Pure, testable in microseconds, no I/O.
def plan_confirmation(hold, existing, actor, policy) -> ConfirmationPlan:
    if not policy.may_confirm(actor, hold):    raise NotPermitted(actor, hold)
    if existing is not None:                   raise AlreadyBooked(hold.resource, hold.slot)
    return ConfirmationPlan(hold_id=hold.id,
                            price=policy.price(hold),
                            notify=hold.owner_id)

# Stage 2: act.  One transaction, one invariant, nothing else.
def apply_confirmation(plan, repo) -> Booking:
    try:
        return repo.confirm(plan.hold_id, price=plan.price)
    except UniqueViolation:
        raise AlreadyBooked(...)              # the constraint had the last word

# Stage 3: consequences.  AFTER the commit, retriable, cannot undo it.
def announce(booking, plan, outbox) -> None:
    outbox.enqueue(BookingConfirmed(booking.id, plan.notify, booking.slot))
```

**What that bought, item by item:**

| | |
|---|---|
| Stage 1 is **pure** | Testable with no database, no SMTP, no LDAP. Ninety-four paths become tractable |
| Stage 2 is **one transaction** | The invariant is enforced by the constraint, and nothing else is in the critical section |
| Stage 3 is **after the commit** | **W1 L06 §1's extension 6a is now structurally impossible** — a notification failure cannot roll back a confirmed booking |
| Each stage has **one actor** | Permissions and pricing are in stage 1's policy object, email in stage 3's outbox. **Divergent Change is addressed** |

**Note what did *not* happen.** Nobody counted lines. **The function was split along the axis of *what changes for whom*, which is Week 2's question, and the line count fell out as a consequence.**

---

## 4. The Fix

**Nine weeks ago this course opened with a bug. Here it is, removed.**

```sql
-- migrations/0042_unique_confirmed_booking.sql
CREATE UNIQUE INDEX one_confirmed_per_slot
  ON bookings (room, slot)
  WHERE state = 'confirmed';
```

```python
# roomsvc/bookings.py -- inside apply_confirmation, after Split Phase
    try:
        db.execute("INSERT INTO bookings (room, slot, owner, state) "
                   "VALUES (?,?,?,'confirmed')", room, slot, owner)
        db.commit()
    except UniqueViolation:
        raise RoomUnavailable(room, slot)
```

```console
$ git show 9a2f1c4 --stat
 migrations/0042_unique_confirmed_booking.sql | 3 +
 roomsvc/bookings.py                          | 11 ++++++----
 2 files changed, 12 insertions(+), 4 deletions(-)
```

**Twelve insertions. One of them is DDL.**

**And the timeline, which is the point:**

| | |
|---|---|
| Detected | 2024-10-14, by two lecturers, standing in VNC 101 |
| Diagnosed | 2024-11-06 — **23 days** |
| Shipped | 2025-03-11 — **four months** |
| Engineering work, once someone was confident | **An afternoon** |

> **The four months were not engineering.** They were 487 lines, eleven tests, 94 independent paths,
> and an author who left in 2023. **Nobody could convince themselves that touching the function was
> safe** — and every week of this course has been one answer to that sentence.

**What the course has built, in order, is the thing that makes the afternoon possible:**

| Week | What it supplies |
|---|---|
| **W1** | The invariant, *written down* — so there is something to enforce |
| **W2** | Cohesion, so the rule is not tangled with email and VAT |
| **W3** | The placement: the narrowest point every path passes through |
| **W5** | The concurrency test, which fails before the fix and passes after |
| **W6** | The mutant that proves the old suite would have shipped it |
| **W7** | A second reader, so the author is not alone with it |
| **W8** | A pipeline that runs the migration as its own step, and verifies |
| **W9** | Characterisation tests and Split Phase, so the change is safe |

**Eight weeks to make an afternoon possible.** That ratio is not a failure of the course; **it is the actual economics of the field** — W0 L01 §4's 60% of lifetime cost, arriving as a bill.

---

## 5. Automated Refactorings, and Where They Stop

**Use the tool for anything it will do**, because a machine-performed rename is *certain* and a hand-performed one is *probably* fine.

| Reliable in tooling | Not reliable |
|---|---|
| **Rename** (symbol-aware, via LSP) | Anything involving a string — a name in a template, a column, a JSON key, a `getattr` |
| **Extract Function / Variable** | Split Phase — a judgement about *what the stages are* |
| **Inline** | Replace Conditional with Polymorphism |
| **Change Signature** | Move Function across a module boundary |
| **Organise imports** | Anything that requires knowing what the code is *for* |

**Python's weak spot is the dynamic one**, and it matters here: `getattr(obj, name)`, a Django-style string-keyed lookup, a column name in a migration, a field name in a template. **A symbol-aware rename misses all of them.** So: **rename with the tool, then `grep` for the old name as a string.** Every time.

**And the layer that makes all of this safe** — a fast green pipeline (W8 L25 §4). **A team at eight minutes will stop running the suite during a refactoring**, which is precisely the work that most needs it. That is not a hypothetical; it is the commonest way a refactoring introduces a bug.

---

## 6. Summary

- **A smell is a cheap, fallible signal that says *look here*** — the same epistemic shape as coverage (W6) and linter findings (W7), and the same failure mode: treating a signal as a verdict. **Notice, ask what it indicates, decide whether to fix it now.**
- **Nine smells account for `roomsvc`**, and two are consistently mis-ranked: **Divergent Change is the most serious and is visible only in the `git log`** — no linter can detect it — and **Speculative Generality is the easiest to fix and the hardest to agree to**, because the waste already happened and keeping it means paying forever.
- **Long Function is a symptom.** The right first move is **Split Phase**: decide (pure), act (one transaction), announce (after the commit) — which makes the notification-rollback bug **structurally impossible** and addresses Divergent Change. **Nobody counted lines; the count fell out.**
- **The fix is twelve insertions, one of them DDL.** 23 days to diagnose, **four months to ship, an afternoon of engineering** — and the four months were 487 lines, eleven tests and a departed author.
- **Eight weeks of this course are what make the afternoon possible**, and that ratio is the field's actual economics rather than a failure of the course.
- **Automate the refactorings a tool does reliably** — rename, extract, inline, change signature — **and `grep` for the old name as a string afterwards**, because Python's dynamic lookups are invisible to symbol-aware tools.

**Next:** L30 — large refactorings: branch by abstraction and the strangler fig, which are how you restructure something too big to change in one commit.

---

*CS 212 · Week 9 · L29 · © CSE Department*
