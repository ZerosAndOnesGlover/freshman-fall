# CS 212 · Software Engineering
## Week 2 · Lecture 2 of 3
### SOLID, One Letter at a Time, in Code That Exists

*“Data abstractions provide the same benefits as procedures, but for data. Recall that the main idea is to separate what an abstraction is from how it is implemented so that implementations of the same abstraction can be substituted freely.”* — Barbara Liskov, keynote address, OOPSLA (1987)

---

**Sat:** Wednesday of Week 2, 10:00–10:50, TH 200 · **Reading:** Martin, *Clean Architecture*, Ch. 7–11 — **critically** · **Next:** L09, DRY, YAGNI, and when each is wrong

**Coursework:** 📝 **Assignment 2** released today 17:00, due Fri of Week 3 17:00 · 📝 **Assignment 1** due Fri this week 17:00 · 📊 **Quiz 3** Tue of Week 3
**A 2 is released after this lecture**, Wednesday 17:00.

---

## 0. Before the Five Letters

SOLID is an acronym assembled by Michael Feathers around 2004 from five principles Robert Martin had written about separately. **It is a mnemonic, not a theory.** The five are of very different value, they overlap heavily with Week 0's coupling and cohesion, and **two of them are routinely quoted in a form their author did not write.**

This lecture takes them one at a time, states each in its author's words, applies it to `roomsvc`, and says what it is worth. **You are expected to leave disagreeing with at least one of the verdicts**, and A 2 Q4 is where you do it.

---

## 1. S — Single Responsibility

**The misquotation:** *"a class should do one thing."*

**What Martin actually wrote:** *"A module should have one, and only one, reason to change."* And later, more precisely: *"A module should be responsible to one, and only one, actor."*

**The second form is the useful one**, and the difference is not pedantry. "One thing" is undefinable — is `confirm_booking` one thing (confirming a booking) or eight? **"One actor" is answerable**, because actors are people with budgets who ask for changes.

**`roomsvc`'s `bookings.py`, by actor:**

| Concern in the file | Who asks for changes to it |
|---|---|
| Permission rules | The **registrar** |
| Price calculation and VAT | The **finance office** |
| Email content and wording | The **communications team** |
| LDAP department lookup | **IT services** |
| Calendar sync | **IT services**, on a different schedule |
| The booking rules themselves | The **registrar**, again |

**Five actors, one file.** When finance changes the VAT rate, someone edits the file that contains the booking invariant — and in a 2,814-line file, with 47% test coverage, **that edit is not obviously safe.** That is the mechanism by which unrelated changes become risky, and it is exactly `roomsvc`'s history: the VAT change of April 2023 (`git log --grep VAT`) shipped alongside a permission regression.

> **Verdict: genuinely useful, in the "one actor" form.** It is Week 0's cohesion with a practical
> test attached. **Applied as "one thing", it produces the hundred-tiny-methods problem** the
> syllabus warns about (§7.1), because "one thing" can always be subdivided and there is no stopping
> rule. *"Which actor asks for this to change?"* has a stopping rule.

---

## 2. O — Open/Closed

**Meyer's original (1988):** *a module should be open for extension and closed for modification* — by which he meant **inheritance**: you extend a class by subclassing it, without editing it, because editing it breaks the already-compiled clients.

**Martin's reformulation (1996)** is about **polymorphic dependency**: depend on an abstraction, and add new behaviour by adding a new implementation rather than by editing a `switch`.

**In `roomsvc`:**

```python
# roomsvc/bookings.py:1103 — the price calculation
if booking.kind == 'lecture':
    price = 0
elif booking.kind == 'seminar':
    price = 0
elif booking.kind == 'external':
    price = rate * hours * (1 + VAT)
elif booking.kind == 'exam':
    price = 0
elif booking.kind == 'external_charity':      # added 2023
    price = rate * hours * 0.5 * (1 + VAT)
elif booking.kind == 'external_partner':      # added 2024
    price = rate * hours * 0.8 * (1 + VAT)
```

**Each new booking kind edits this function.** And `kind` is also switched on in `notify.py:88`, `reports.py:212` and `views.py:341` — **four places, and adding a kind means finding all four.** Commit `7b1e4f2` (2024-03) added `external_partner` and missed `reports.py`, so partner bookings were reported at full price for eight months.

**The open/closed fix:** a `PricingPolicy` per kind, looked up in a registry. Adding a kind adds a file.

**And here is the honest part.** That fix is right *here*, because the change history proves the axis of change: **six kinds added over six years, in four places each.** The same fix applied speculatively — before any kind was added — would be **speculative generality**, and would have been the wrong call in 2020.

> **Verdict: useful, but only against a demonstrated axis of change.** The principle as stated gives
> you no way to know *which* extensions to be open to, and you cannot be open to all of them — every
> abstraction closes some doors. **The `git log` tells you; the principle does not.** This is the
> single most important caveat in the lecture, and A 2 Q2 is built on it.

---

## 3. L — Liskov Substitution

**Liskov & Wing's formulation (1994):** *if `S` is a subtype of `T`, then objects of type `T` may be replaced with objects of type `S` without altering any of the desirable properties of the program.*

**This is the only one of the five that is a theorem rather than advice**, and it has precise content: a subtype may **weaken preconditions** and **strengthen postconditions**, never the reverse, and must preserve the supertype's invariants.

**The classic violation is square/rectangle**, and it is a real example rather than a contrived one: `Square` inheriting from `Rectangle` breaks any client that does `r.width = 5; r.height = 4; assert r.area() == 20`.

**`roomsvc`'s version is better, because it is in production:**

```python
class Resource:
    def book(self, slot, owner) -> Booking: ...

class Room(Resource): ...

class Equipment(Resource):
    def book(self, slot, owner) -> Booking:
        if not owner.is_staff:
            raise PermissionError("equipment is staff-only")   # <- strengthened precondition
        ...
```

**`Equipment` demands more of its caller than `Resource` promises.** Every piece of code written against `Resource` — the bulk booking importer, the timetable generator, the API — is now wrong for one subtype, and it fails at runtime with a `PermissionError` nobody catches, in `reports.py`'s nightly job.

**The fix is not to make `Equipment` looser.** The rule is real and should be enforced. The fix is that **permission is not a property of the resource type** — it is a policy, and it belongs in one place that all callers go through. Which is §1's answer, arrived at from a different direction.

> **Verdict: genuinely important, and it applies far beyond inheritance.** The same reasoning
> governs any implementation of an interface, any duck-typed substitution, and any API version
> claiming backward compatibility — **which is Week 10's entire subject.** If you learn one letter
> properly, learn this one.

---

## 4. I — Interface Segregation

**Martin's statement:** *no client should be forced to depend on methods it does not use.*

**In a statically-typed, compiled language this has teeth**: a client that imports a fat interface recompiles when any part of it changes, and in a large C++ or Java codebase that is a real cost.

**In Python it is much weaker.** Duck typing means a client that calls two methods depends on two methods, whatever the class declares. **The principle survives as a design smell rather than a mechanical cost:**

```python
class Notifier:
    def send_email(self, to, subject, body): ...
    def send_sms(self, to, body): ...
    def send_push(self, device_token, body): ...
    def render_template(self, name, ctx): ...
    def queue_digest(self, user, items): ...
```

**`bookings.py` calls exactly one of these**, and `notify.py` is 612 lines with **3.9% test coverage** (W0 resources). To test `confirm_booking` you must construct something that satisfies all five methods, so nobody does, so it is not tested.

**The mechanical consequence in Python is in the tests**, which is where interface segregation actually pays:

```python
# with the fat interface — a five-method fake nobody writes
# with a segregated one:
def confirm(hold_id, notify: Callable[[UserId, str], None]): ...
# test:  confirm(h, notify=lambda u, m: sent.append((u, m)))
```

> **Verdict: weak as stated in a dynamic language; strong when restated as "the smallest interface
> you can test against".** In Python the relevant unit is usually a **function**, not a class, and
> the smallest useful interface is very often a single callable. Week 5 comes back to this, because
> the size of your interfaces determines whether your tests need mocks.

---

## 5. D — Dependency Inversion

**Martin's statement**, in two parts:

> *A. High-level modules should not depend on low-level modules. Both should depend on abstractions.*
> *B. Abstractions should not depend on details. Details should depend on abstractions.*

**This is the most valuable letter and the most mangled.** It is **not** "use a dependency injection framework". It is a statement about **which direction source-code dependencies point**, and the word *inversion* refers to inverting them relative to the flow of control.

**Concretely.** Control flows: booking logic → sends an email. **Naively, the source dependency points the same way** — `bookings.py` imports `smtp_client`. Dependency inversion points it the other way: the booking logic declares what it needs, and the SMTP code implements it.

```python
# domain layer — knows nothing about email, HTTP, or SQL
def confirm(hold_id: UUID, repo: BookingRepo, notify: Notifier) -> Booking:
    booking = repo.confirm(hold_id)      # may raise AlreadyBooked
    notify(booking.owner_id, f"Confirmed: {booking.resource} at {booking.slot}")
    return booking
```

**`confirm` imports nothing from the database or the mail server.** Both of those import *it*, or rather import the protocol it declares. And the payoff is not architectural purity — it is three concrete things:

| | |
|---|---|
| **Testable** | `confirm(h, FakeRepo(), lambda *a: None)` runs in microseconds, with no database and no SMTP |
| **The domain is readable alone** | You can answer *"what are the booking rules?"* by reading one file |
| **The details are replaceable** | Which matters less often than people claim, and is the reason usually given |

**The third is the weakest justification and the one always cited.** You will probably never change database. **You will run the tests ten thousand times**, and that is where the principle pays.

> **Verdict: the most valuable of the five, for a reason that is not the one usually given.**
> It buys fast tests and a readable domain, not portability. **Week 3 turns it into an
> architecture** — this is the seam that `service.py` marks in your walking skeleton.

---

## 6. The Scoreboard

| Letter | Worth what it claims? | The real content |
|---|---|---|
| **S** | **Yes**, in the "one actor" form | Cohesion, with an answerable test |
| **O** | **Only against a demonstrated axis of change** | Read the `git log` before abstracting |
| **L** | **Yes — and it is the one with actual formal content** | Substitutability, which is also API compatibility (W10) |
| **I** | **Weak in Python as stated** | Restate as: the smallest interface you can test against |
| **D** | **Yes, and it is the most valuable** | Fast tests and a readable domain; portability is the least of it |

**Notice what the table reduces to.** S is cohesion. I and D are coupling. O is Parnas's "hide what changes". **L is the only one that is not a restatement of Week 2's first lecture**, and it is the only one with a proof attached.

**That is not a criticism.** A mnemonic that makes five people in a code review reach for the same vocabulary has value even when it is not new. **But it means that a team that has understood coupling and cohesion has most of SOLID already**, and a team that recites SOLID without them has none of it.

---

## 7. The Failure Mode: SOLID as a Checklist

The characteristic over-application, seen in every cohort:

```
slot/
├── interfaces/
│   ├── IBookingRepository.py          # one implementation
│   ├── IBookingService.py             # one implementation
│   ├── INotificationStrategy.py       # one implementation
│   └── IBookingValidatorFactory.py    # no implementations yet
├── factories/
│   └── BookingServiceFactory.py
└── impl/
    └── PostgresBookingRepositoryImpl.py
```

**Eleven files to insert one row.** Every abstraction has exactly one implementation, every interface was written for a change that has not happened, and **the cost is paid every time anyone reads it.**

> **The test to apply, and A 2 Q3 asks you to apply it to your own repository:** for each
> abstraction in your project, **name the second implementation.** If it does not exist and you
> cannot name a specific circumstance that would create it, delete the abstraction and inline it.
> **You can always extract it later; that is what Week 9 is for.** Extracting an abstraction from
> concrete code is a routine refactoring. Removing a wrong abstraction that six modules now depend
> on is not.

**Sandi Metz's formulation is the one to remember:** *"duplication is far cheaper than the wrong abstraction."* It is the single most useful sentence in this week and it contradicts most people's instinct.

---

## 8. Summary

- **SOLID is a mnemonic assembled in 2004, not a theory**, and two of the five are usually quoted in a form their author did not write.
- **S: "one reason to change" is vague; "one actor" is answerable.** `bookings.py` serves five actors, which is why a VAT change shipped a permission regression.
- **O: only abstract against a demonstrated axis of change.** `roomsvc`'s six booking kinds are switched on in four places, and a 2024 commit missed one for eight months — **but the same abstraction built in 2020 would have been speculative generality.**
- **L is the only letter with formal content** — weaken preconditions, strengthen postconditions, preserve invariants — and `Equipment.book` violates it in production. **It is also Week 10's API compatibility rule.**
- **I is weak in Python as stated**; restate it as *the smallest interface you can test against*, and note that `notify.py` has 3.9% coverage because its interface has five methods.
- **D is the most valuable, for the wrong reason.** It buys fast tests and a readable domain; database portability is the least of it.
- **Four of the five reduce to coupling and cohesion.** A team that understands L07 has most of SOLID; a team that recites SOLID without it has none.
- **"Duplication is far cheaper than the wrong abstraction."** For every abstraction in your project, name the second implementation — or delete it.

**Next:** L09 — DRY, YAGNI, separation of concerns, and the cases where each of them is straightforwardly wrong.

---

*CS 212 · Week 2 · L08 · © CSE Department*
