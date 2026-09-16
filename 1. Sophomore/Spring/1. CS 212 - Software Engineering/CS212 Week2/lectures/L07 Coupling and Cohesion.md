# CS 212 · Software Engineering
## Week 2 · Lecture 1 of 3
### Coupling and Cohesion — the Two Ideas the Rest Are About

---

**Sat:** Tuesday of Week 2, 10:00–10:50, TH 200 · **⚠️ Quiz 2 in the first ten minutes** — covers Week 1 · **Reading:** Sommerville §7.1; Parnas (1972) · **Next:** L08, SOLID in `roomsvc`

---

## 1. Why `confirm_booking` Is Bad, and It Is Not the Line Count

Week 0 gave you the numbers: **487 lines, cyclomatic complexity 94, eleven tests.** It is easy to conclude that the problem is length, and the *Clean Code* reflex — extract until every function is four lines — follows immediately.

**That reflex is wrong, and the syllabus says so** (§7.1). Here is the actual structure of the function, compressed:

```python
def confirm_booking(room, slot, owner, opts):
    # 1. permission check, reading a global settings dict       (lines 291–334)
    # 2. conflict SELECT                                         (335–352)
    # 3. price calculation, including a VAT rate hard-coded      (353–418)
    # 4. email rendering, with HTML in triple-quoted strings     (419–486)
    # 5. LDAP lookup of the owner's department                   (487–521)
    # 6. INSERT                                                  (522–544)
    # 7. audit log write, to a different database                (545–589)
    # 8. calendar sync, an HTTP POST to an external service      (590–664)
    # 9. cache invalidation, by deleting files from disk         (665–698)
    # ... 80 more lines of special cases for exam bookings       (699–778)
```

**Now split it into nine four-line functions.** Every problem in the list below survives:

- The VAT rate still changes annually, in a file about bookings.
- The email still cannot be tested without an SMTP server.
- The LDAP outage still takes bookings down.
- The calendar POST is still inside the transaction, so a slow external service still rolls back a confirmed booking.
- The `INSERT` is still 200 lines and two network calls after the `SELECT` that justified it.

**Length was never the problem.** The problem has two names, and they are the oldest two ideas in software design.

---

## 2. The Two Definitions

From Stevens, Myers & Constantine (1974), *"Structured Design"*, IBM Systems Journal — a fifty-year-old paper whose vocabulary has not been improved on.

> **Cohesion** — how strongly the things *inside* one module belong together.
> **Coupling** — how much one module depends on the *internals* of another.

**The goal is high cohesion and low coupling**, and the reason is a single sentence about change:

> **A change to one thing should require touching one module, and reading only that module to be
> sure you are right.**

`confirm_booking` fails both. **Cohesion:** it contains permissions, pricing, email, directory lookup, persistence, audit, calendar and caching — eight unrelated reasons to change one function. **Coupling:** it reaches into a global settings dict, a second database, an LDAP server, an HTTP service and the filesystem, and it knows the internal shape of all five.

**And this is measurable.** Week 0's change data:

```console
$ git log --since='2 years ago' --name-only --format='' | grep '\.py$' \
    | sort | uniq -c | sort -rn | head -3
    891 roomsvc/bookings.py
    204 roomsvc/views.py
    186 roomsvc/models.py
```

**891 touches in two years, 41% of all file changes.** A cohesive module is touched when its one concern changes. `bookings.py` is touched when *any of eight* concerns change — when VAT changes, when the email template changes, when LDAP moves, when the calendar API versions. **That is what low cohesion looks like in a `git log`**, and it is the most useful diagnostic in this course because it requires no judgement.

---

## 3. Cohesion, Ranked

Constantine's scale, worst to best. **Learn the top and the bottom; the middle is for recognising things.**

| Level | The module's parts are together because… | Example |
|---|---|---|
| **Coincidental** (worst) | …no reason. Someone had to put them somewhere | `utils.py`. Every codebase has one; `roomsvc`'s is 340 lines and imports six unrelated libraries |
| **Logical** | …they are the same *kind* of thing, selected by a flag | `handle_event(kind, payload)` with an eight-branch `if` |
| **Temporal** | …they happen at the same time | `on_startup()` that opens a database, loads a config and warms a cache |
| **Procedural** | …they happen in sequence | |
| **Communicational** | …they operate on the same data | |
| **Sequential** | …one's output is the next's input | |
| **Functional** (best) | …**together they do exactly one thing, and all of them are needed to do it** | `confirm(hold_id) -> Booking` |

**The test for functional cohesion is the name.** If you can name the module with a single verb phrase and no "and", it is probably cohesive. `confirm_booking` would have to be called `check_permission_and_price_and_email_and_look_up_department_and_insert_and_audit_and_sync_and_invalidate`, which is the diagnosis.

> **`utils.py` deserves a moment.** It is the canonical coincidental module and it is *always* the
> hardest file to delete, because everything imports it. **Your `slot` will grow one by Week 5.**
> When it does, the fix is not to organise it better — it is to move each function next to the
> thing it is about, and discover that most of them are about something.

---

## 4. Coupling, Ranked

Same paper, same shape. **The bottom three of this table are where `roomsvc`'s damage is.**

| Level | | Example |
|---|---|---|
| **Data** (best) | Modules communicate by passing simple values | `confirm(hold_id: UUID) -> Booking` |
| **Stamp** | A whole record is passed where a field would do | `confirm(request)` where `request` is the entire HTTP request object |
| **Control** | One module passes a flag telling another *how* to behave | `save(booking, send_email=True, skip_audit=False)` |
| **External** | Several modules share a dependency on an outside format or device | Four modules all know the LDAP attribute names |
| **Common** | Several modules read and write shared global state | `roomsvc`'s `SETTINGS` dict, mutated in three places |
| **Content** (worst) | One module reaches into another's internals | `booking._state = 'CONFIRMED'` from `admin.py` |

**Stamp coupling is the one students under-rate**, because it looks harmless and it is the default. A function that takes the HTTP request object:

```python
def confirm_booking(request):          # stamp-coupled to the web framework
    room = request.form['room']
    ...
```

**cannot be tested without constructing an HTTP request, cannot be called from a command-line script, and cannot be reused by the batch job that imports the timetable.** All three of those are things `roomsvc` needs and cannot do. The fix is four characters of thinking:

```python
def confirm_booking(room: str, slot: Slot, owner_id: UUID) -> Booking:
```

**This function has no idea the web exists.** That is the property Week 3 builds an architecture around, and it starts here.

**Content coupling is rarer and worse.** `roomsvc` has it: `admin.py:271` sets `state` directly without `cancelled_at`, which is how invariant I5 gets violated (W1 L06 §4). **When one module can reach past another's front door, the second module's invariants are not invariants.**

---

## 5. Parnas, 1972: What a Module Should Hide

Fifteen years before object-orientation went mainstream, David Parnas published *"On the Criteria To Be Used in Decomposing Systems into Modules"*, and got the answer right in four pages.

**The question he asked:** given a program, there are many ways to split it into modules. Which split is better, and why?

**The wrong criterion** — and the obvious one — is to split by **step in the processing**: read input, process, format output. **The right criterion** is to split by **what is likely to change**, and to put each likely change **inside** one module, behind an interface that does not mention it.

> *"We propose instead that one begins with a list of difficult design decisions or design
> decisions which are likely to change. Each module is then designed to hide such a decision from
> the others."* — Parnas, 1972

**His worked example** — a KWIC index — shows the two decompositions side by side. The step-based one requires changes to four modules when the storage format changes; the information-hiding one requires changes to one. **That is the entire argument for encapsulation, made before the word existed.**

**Applied to `slot`, this is the most useful design question you can ask this term:**

| What is likely to change in `slot`? | Which module should hide it? |
|---|---|
| The booking window (how far ahead you may book) | A policy module. **Not sprinkled as a constant in six places** |
| Whether notification is email, or a message on the portal | A `Notifier` interface; nothing else knows |
| The database — Postgres now, something else if the department's IT insists | A repository layer. **This one is genuinely arguable** — see W3 |
| Opening hours, which differ per resource and change per term | A `Resource` method. Not a global |
| **The slot duration** | **Nothing can hide this.** It is in the domain model, the schema, the index and every query |

**The last row is the honest one and it is why the table is worth drawing.** Some decisions cannot be hidden, and knowing *which* is the difference between a design and a hope. **A decision you cannot hide is a decision you must get right**, which is exactly why W1 L06 §3 spent a lecture on it.

---

## 6. Connascence: a Sharper Tool

Coupling is a six-level scale invented for 1974's programs, and it does not discriminate well among modern code. **Connascence** (Page-Jones, 1992) is the same idea made precise: **two pieces of code are connascent if changing one requires changing the other.**

Its value is that it is **ordered and has two independent axes.** The forms, weakest to strongest:

| Form | Two things must agree on… | Example |
|---|---|---|
| **Name** | A name | The caller and the function agree on `confirm_booking` |
| **Type** | A type | |
| **Meaning** | The meaning of a value | `state = 2` means confirmed. **Fix with an enum** |
| **Position** | The order of arguments | `book(room, slot, owner)` — swap two strings and it compiles |
| **Algorithm** | The same algorithm | Two modules that both hash the same way |
| **Execution** | The order of execution | `open()` must be called before `read()` |
| **Timing** | Timing | **The 15-minute hold expiry, known by three separate queries** |
| **Value** | Several values changing together | `start < end` across two columns |
| **Identity** | Referring to the same instance | Two modules sharing one mutable cache object |

**And two axes:**

- **Degree** — how many places are involved. Connascence of name across two functions is nothing; across two hundred it is a refactoring project.
- **Locality** — **how far apart they are.** Connascence of position inside one function is fine. Across a module boundary it is a bug waiting.

> **The rule that makes this practical:** *the stronger the connascence, the shorter the distance
> it may span.* Connascence of meaning inside one class is acceptable; the same connascence between
> `bookings.py` and `calendar_sync.py`, 2,000 lines apart, is how `roomsvc` ended up with
> `state = 'Confirmed'` in one file and `'CONFIRMED'` in another for three weeks in 2022
> (`git log -S"'Confirmed'"`, commit `c81ae40`).

**Why this beats the 1974 scale in practice:** it tells you *what to do*. Connascence of meaning → introduce an enum. Connascence of position → use keyword arguments. Connascence of execution → make the ordering impossible to get wrong by construction. **Each form has a standard weakening**, and A 2 asks you to apply three of them.

---

## 7. What This Costs, and When Not to Pay It

Every decoupling has a price, and it is **indirection**. A `Notifier` interface with one implementation means that reading the code requires two hops instead of one, and a stack trace is longer.

**When the price is worth paying:**

- The decision genuinely might change, and you can name the alternative. *"We might switch database"* — name which one. If you cannot, you are guessing.
- **It is already changing.** The best evidence is a `git log` showing the thing has changed three times.
- The coupling crosses a testing boundary — an abstraction that lets you test without an SMTP server pays for itself in Week 5, immediately and measurably.

**When it is not:**

- One implementation, no named alternative, no change history. This is the speculative generality smell (Week 9) and it is the most common over-engineering in student projects.
- **Inside a module.** Decoupling is about boundaries. Two functions in one file that know about each other are supposed to.

**The honest heuristic**, and it is Fowler's: **couple to things that change together, decouple things that change apart** — and you find out which from the `git log`, not from your intuition. Week 11 measures exactly this, on your own project, and calls it *change coupling*.

---

## 8. Summary

- **`confirm_booking` is not bad because it is 487 lines.** Split into nine four-line functions, every one of its actual problems survives. Length is a symptom.
- **Cohesion is how well the things inside a module belong together; coupling is how much one module depends on another's internals.** The goal is one module touched per change, and only that module read to be sure.
- **Low cohesion is visible in `git log`:** `bookings.py` takes 41% of all file-touches because eight unrelated concerns live in it.
- **Functional cohesion passes the name test** — one verb phrase, no "and".
- **Stamp coupling is under-rated**: a function taking the HTTP request cannot be tested, scripted or reused. **Content coupling is worse** — `admin.py:271` reaches past `Booking`'s front door and breaks its invariant.
- **Parnas (1972): decompose by what is likely to change, not by processing step**, and hide each likely change inside one module. **Some decisions cannot be hidden** — the slot duration is one — and knowing which is the point of the exercise.
- **Connascence is coupling made precise and actionable**: nine ordered forms, each with a standard weakening, and the rule *the stronger the connascence, the shorter the distance it may span*.
- **Decoupling costs indirection.** Pay when the alternative is nameable, the history shows change, or it crosses a testing boundary. **Otherwise it is speculative generality.**

**Next:** L08 — SOLID, one letter at a time, applied to code that exists. Two of the five are worth what they claim; one is almost always misquoted.

---

*CS 212 · Week 2 · L07 · © CSE Department*
