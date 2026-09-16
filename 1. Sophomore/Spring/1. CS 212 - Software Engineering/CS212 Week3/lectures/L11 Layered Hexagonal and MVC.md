# CS 212 · Software Engineering
## Week 3 · Lecture 2 of 3
### Layered, Hexagonal, and MVC

---

**Sat:** Wednesday of Week 3, 10:00–10:50, TH 200 · **Reading:** Cockburn, *"Hexagonal Architecture"* (2005) — 6 pages · **Next:** L12, microservices and event-driven
**A 3 is released after this lecture**, Wednesday 17:00.

---

## 1. Layered Architecture, and the Rule Nobody States

The default, and it is the default for good reasons.

```
┌─────────────────────────────────────┐
│  Presentation   HTTP routes, HTML   │
├─────────────────────────────────────┤
│  Application    orchestration       │
├─────────────────────────────────────┤
│  Domain         rules, invariants   │
├─────────────────────────────────────┤
│  Infrastructure SQL, SMTP, HTTP out │
└─────────────────────────────────────┘
```

**The rule everyone states:** a layer may call the layer below.
**The rule nobody states, and it is the one that matters:** *a layer may not know the layer above exists.*

The second rule is what makes the first worth anything. Without it you get "layers" that are labels on a directory structure, with the domain importing the web framework's exception type because it was convenient, and at that point you have the diagram and none of the property.

**Test it mechanically.** This should be in your CI by Week 8 and you can add it in ten minutes now:

```python
# tests/test_architecture.py
import ast, pathlib

FORBIDDEN = {"fastapi", "sqlalchemy", "starlette", "smtplib", "httpx", "psycopg"}

def test_domain_imports_nothing_external():
    for path in pathlib.Path("src/slot/domain").rglob("*.py"):
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            mods = ([a.name for a in node.names] if isinstance(node, ast.Import)
                    else [node.module or ""] if isinstance(node, ast.ImportFrom) else [])
            for m in mods:
                assert m.split(".")[0] not in FORBIDDEN, f"{path}: imports {m}"
```

**A rule a machine checks is a rule. A rule in a diagram is a hope.** This is the single cheapest architectural control available to you and almost no team adds it before Week 8.

### The strict/relaxed question

**Strict layering:** presentation may call only application. **Relaxed:** presentation may call anything below it.

**Relaxed is more honest and almost everyone uses it** — a read-only "list my bookings" going straight from the route to a query is fine, and forcing it through a one-line application function is the ceremony that gives layering a bad name.

> **The compromise worth adopting, and it is what your marks will reward:** **reads may skip
> layers; writes may not.** A query has no invariants to protect; a mutation does. It is one
> sentence, it is enforceable by review, and it removes about 80% of the arguments.

### Where layering leaks

Three leaks appear in every layered system. Know them so you recognise yours.

| Leak | What it looks like | What to do |
|---|---|---|
| **Transactions** | The application layer must open one, but the ORM that owns it is infrastructure | Accept it. The application layer owns the **unit of work**; make it explicit rather than pretending |
| **N+1 queries** | The domain loops over bookings asking each for its resource; infrastructure issues 300 queries | The domain cannot see it. **Measure it** (W11) and fix it at the repository with an explicit eager-loading method |
| **Validation** | The same rule checked at three layers, drifting apart | **Decide which layer owns each rule and write it in an ADR.** Presentation validates *shape*; domain validates *rules* |

---

## 2. Hexagonal — Ports and Adapters

Cockburn, 2005. **The same idea as dependency inversion (W2 L08 §5), taken to its conclusion and given a picture.**

```
                    ┌──────────────────┐
     HTTP adapter ─▶│                  │◀─ Postgres adapter
      CLI adapter ─▶│   DOMAIN + APP   │◀─ SMTP adapter
     test adapter ─▶│   (knows nothing │◀─ fake repo (tests)
                    │    of the outside)│
                    └──────────────────┘
        driving side                    driven side
```

**The two ideas:**

1. **A port is an interface defined *by the inside*.** `BookingRepo` is declared in the domain, in the domain's vocabulary, for the domain's needs. It is *not* a thin wrapper over SQLAlchemy's API, and that distinction is the whole of hexagonal architecture.
2. **An adapter implements a port using outside technology.** `PostgresBookingRepo` implements `BookingRepo`. So does `FakeBookingRepo` in your tests — **and the fake is not a second-class citizen, it is a first-class adapter**, which is the answer to W2 L08 §7's "name the second implementation".

**The asymmetry is the subtle part.** Driving adapters (HTTP, CLI, a test) *call in*. Driven adapters (database, SMTP) *are called*. **Only the driven side needs dependency inversion**, because that is the side where control flow and dependency direction disagree. A lot of over-built hexagonal code comes from inverting the driving side too, which buys nothing.

**What it actually buys, measured:**

| Claim | Honest assessment |
|---|---|
| **Fast tests** | **True and it is the main one.** Domain tests with a fake repo: ~1 ms. With a Postgres container: ~1.2 s per module, 9 s to start. At 200 tests this is the difference between a 2-second and a 4-minute feedback loop |
| **The domain is readable alone** | **True**, and under-rated. *"What are the booking rules?"* becomes a question with a one-file answer |
| **You can swap the database** | **Technically true, practically irrelevant.** You will not. Do not use this as the justification in your ADR — it is the one that makes reviewers stop believing you |
| **You can drive it from a CLI or a queue** | **Sometimes genuinely useful.** `slot` plausibly wants a bulk timetable importer, and that is a second driving adapter with no HTTP |

**What it costs**, honestly, and Phase 1 expects you to have counted it:

- **A mapping layer.** ORM row → domain object and back. For `slot` that is about 40 lines and it is tedious, and it is a real place for bugs.
- **Two hops to answer a question.** *"What SQL runs when we confirm?"* needs the port and the adapter.
- **A genuine temptation to leak.** The moment you need a query the port does not express, the easy move is to add `def raw_query(sql)` to the port, and then it is over.

> **Is it right for `slot`?** **Defensible, and not obligatory.** A five-person, twelve-week project
> with one database and one delivery mechanism can reasonably conclude that a **modular monolith
> with one enforced rule — the domain imports nothing external** — gets 90% of the benefit for 20%
> of the ceremony. **That conclusion is worth full marks if it is written as an ADR with the
> alternative considered.** What is not worth marks is arriving at it by accident.

---

## 3. MVC, and Why It Is Almost Always Misused

**Trygve Reenskaug, Xerox PARC, 1979.** The original is about **a user interface in a single address space**:

| | Original meaning |
|---|---|
| **Model** | The domain data **and its rules**, which notifies observers when it changes |
| **View** | An observer that renders the model, and **updates itself when notified** |
| **Controller** | Handles *input events* — mouse, keyboard — and translates them into model operations |

**The observer relationship is the core, and it is exactly what web MVC does not have.** HTTP is request/response; the server cannot notify a browser that a model changed. So "MVC" on the server means something different, and mostly means:

| | What web frameworks call it |
|---|---|
| **Model** | An ORM class — **data with no rules**, which is the Anemic Domain Model that Fowler named in 2003 |
| **View** | A template |
| **Controller** | A route handler, which in practice holds the business logic |

**The consequence is `roomsvc`.** `views.py` is 743 lines, `models.py` is 986 lines of columns with almost no behaviour, and the rules are in a 2,814-line file that belongs to neither. **"We use MVC" was true and told nobody anything about where the invariant lived.**

> **What to take from this.** MVC is a **user-interface** pattern and it is a good one in its place —
> a desktop application, a component in a browser framework. **It is not a system architecture**,
> and saying "we used MVC" in your Phase 1 presentation answers no question that was asked. Name
> where the rules live instead.

**And the Anemic Domain Model is worth naming**, because your project will grow one by Week 6 unless someone says the word. Its shape: classes with fields and getters, all behaviour in "service" functions that manipulate them from outside. **It is not a crime** — it is a reasonable style if the services are cohesive, and a great deal of working software is built this way. **It becomes a problem when the invariants have nowhere to live**, and then you get `Booking._state = 'CONFIRMED'` in `admin.py`.

---

## 4. The Modular Monolith, Which Is Probably Your Answer

**One deployable unit; strong module boundaries inside it.** This is the shape most of the industry has settled back on after the microservices decade, and it is almost certainly right for `slot`.

```
src/slot/
├── domain/          # rules, invariants, ports. Imports nothing external.
├── app/             # use cases, transactions, orchestration
├── infra/           # sqlalchemy models, repo impls, smtp, http clients
└── web/             # fastapi routes, request/response models, templates
```

**What makes it modular rather than just a directory tree:**

1. **The dependency rule is enforced by a test** (§1).
2. **Each module has an explicit public surface.** In Python, a module's `__init__.py` re-exports what is public, and the review rule is *"do not import from inside another module's package"*. It is weaker than a compiler would give you, and it is enough.
3. **The boundaries are where you would cut if you ever split.** Which you will not. **But designing as though you might is what keeps them real** — this is the one legitimate form of speculative design, because the cost is zero.

**Why this over microservices for a term project**, stated so you can say it in a viva: **a monolith gives you one deployment, one database transaction spanning everything, one log, one stack trace, and no network between your own functions.** Every one of those becomes a problem the moment you split, and none of them is currently a problem. **L12 does the arithmetic.**

---

## 5. Choosing, For Real

A decision procedure you can actually run this week.

**1. Rank your quality attributes** (L10 §3). Write them down; three lines.

**2. Ask what has to be true in twelve weeks.** For `slot`: ~200 tests that run in under a minute, four people changing code simultaneously without constant conflicts, a demo that works live, and a report that can state where the rules live.

**3. Pick the least structure that delivers it.** For most `slot` teams that is the modular monolith of §4 **with one enforced rule**: the domain imports nothing external. That single rule buys you the fast tests, the readable domain and the honest answer about the invariant — **which is most of what hexagonal promises.**

**4. Write the ADR, with the alternative you rejected and why.**

**5. Add the import test to CI now**, while the violation count is zero. Adding it in Week 9 means fixing 30 violations first, which means it never gets added.

> **The failure mode to avoid is not under-engineering.** A team that starts simple and discovers in
> Week 7 that it needs a seam adds one, in an afternoon, with the tests they now have.
> **A team that starts with eleven interfaces and one implementation each spends every week paying
> for a flexibility it never uses**, and — worse — cannot tell which of its abstractions are real,
> because none of them has ever been exercised by a second case.

---

## 6. Summary

- **Layered's stated rule is "a layer calls the one below". The unstated rule is "a layer does not know the layer above exists"**, and it is the one that carries the value. **Enforce it with a test**; twelve lines of `ast`, and it turns a hope into a rule.
- **Reads may skip layers; writes may not.** One sentence, removes most of the arguments.
- **Layering always leaks** in three places: transactions, N+1 queries and validation. Own the leaks explicitly.
- **Hexagonal: a port is an interface defined by the inside, in the inside's vocabulary**; an adapter implements it. **Only the driven side needs inversion.** It buys fast tests and a readable domain; **it does not buy database portability, and citing that makes reviewers stop believing you.**
- **MVC is a 1979 user-interface pattern whose core is the observer relationship** — which HTTP does not have. On the server it usually means an anemic model, a template and a fat controller, **and saying "we use MVC" tells nobody where the invariant lives.**
- **The modular monolith is probably your answer**: one deployable, enforced internal boundaries, and boundaries drawn where you *would* cut if you ever split — the one legitimate speculative design, because it costs nothing.
- **Pick the least structure that delivers what must be true in twelve weeks**, write the ADR with the rejected alternative, and **add the import test while the violation count is still zero.**

**Next:** L12 — microservices and event-driven architecture: what they buy, the arithmetic of what they cost, and the two questions to ask anyone who proposes either.

---

*CS 212 · Week 3 · L11 · © CSE Department*
