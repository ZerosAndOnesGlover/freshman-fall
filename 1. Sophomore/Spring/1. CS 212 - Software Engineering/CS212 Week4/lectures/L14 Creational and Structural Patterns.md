# CS 212 · Software Engineering
## Week 4 · Lecture 2 of 3
### Creational and Structural Patterns, in Production Code

*“The definition I use for a pattern is an idea that has been useful in one practical context and will probably be useful in others”* — Martin Fowler, *Analysis Patterns* (1997)

---

**Sat:** Wednesday of Week 4, 10:00–10:50, TH 200 · **Reading:** GoF Ch. 3–4, selectively · **Next:** L15, behavioural patterns

**Coursework:** 📝 **Assignment 4** released today 17:00, due Fri of Week 5 17:00 · 📝 **Assignment 3** due Fri this week 17:00 · 📊 **Quiz 5** Tue of Week 5
**A 4 is released after this lecture**, Wednesday 17:00.

---

## 1. Creational Patterns Exist Because Construction Is a Decision

**The insight underneath all five:** the code that *uses* an object and the code that *decides which* object to make have different reasons to change. Mixing them couples every user to every choice.

**In `roomsvc`, every one of them is mixed:**

```python
# roomsvc/bookings.py:294 — inside confirm_booking
mailer = SMTPMailer(host=SETTINGS['smtp_host'], port=587, tls=True)
```

**Constructed in-line, in a function about booking rules.** Which means: you cannot test `confirm_booking` without an SMTP server; the settings dict is read at call time from a global; and changing the mail transport means finding every construction site. **There are eleven.**

---

## 2. Factory Method and Abstract Factory — Mostly a Function

**Factory Method** — a method that decides which class to instantiate.
**Abstract Factory** — an object that creates *families* of related objects.

**In Python both are usually a function or a dict.** The `PricingPolicy` registry from A 2 is the honest version:

```python
POLICIES = {
    'lecture':          FreePolicy(),
    'seminar':          FreePolicy(),
    'exam':             FreePolicy(),
    'external':         RatePolicy(multiplier=1.0),
    'external_charity': RatePolicy(multiplier=0.5),
    'external_partner': RatePolicy(multiplier=0.8),
}

def policy_for(kind: str) -> PricingPolicy:
    try:
        return POLICIES[kind]
    except KeyError:
        raise UnknownBookingKind(kind)
```

**That is Abstract Factory with the ceremony removed**, and it is better than the class version here, because the six policies differ only in a multiplier.

**When the class hierarchy is worth it:** when the created objects genuinely have different *behaviour*, not just different data. Two of `slot`'s six pricing rules differ only in a number — **those should be one class with a parameter, and noticing that is worth more than knowing the pattern.**

> **The rule to take:** *"a factory"* in Python usually means **a callable that returns a
> constructed thing**. Reach for a class only when the factory itself has state or needs
> substituting — which for `slot` means: almost never, except in your tests.

---

## 3. Builder — the One That Earns Its Keep in Tests

**The problem:** an object with many optional fields, where a constructor with eleven parameters is unreadable and eleven overloads are worse.

**In Python, keyword arguments and `@dataclass` solve most of it**, and this is one of Norvig's cases:

```python
@dataclass(frozen=True)
class Booking:
    resource_id: str
    slot: Slot
    owner_id: UUID
    state: State = State.HELD
    expires_at: datetime | None = None
    note: str = ""
```

**But Builder survives in one place, and it is the place you will actually want it: test data.**

```python
# tests/factories.py
class BookingBuilder:
    def __init__(self):
        self._kw = dict(resource_id="TH200", slot=Slot("2026-03-04T10:00"),
                        owner_id=uuid4(), state=State.HELD)
    def confirmed(self):   self._kw["state"] = State.CONFIRMED; return self
    def for_resource(self, r): self._kw["resource_id"] = r; return self
    def at(self, s):       self._kw["slot"] = Slot(s); return self
    def build(self):       return Booking(**self._kw)

# in a test:
booking = BookingBuilder().confirmed().for_resource("VNC101").build()
```

**Why this matters more than it looks.** A test that constructs a `Booking` with all six fields states six facts, of which **one** is relevant to the test. A reader cannot tell which. **The builder makes the test say only what it means** — and Week 5 will show you that a test's readability is most of its value, because a failing test you cannot understand is a test you delete.

**This is the *Object Mother* / *Test Data Builder* pattern** (Meszaros, *xUnit Test Patterns*, 2007), and **it is the highest-value pattern in this lecture for your project.** Add `tests/factories.py` this week.

---

## 4. Singleton — Usually a Mistake

**The problem it claims to solve:** exactly one instance, globally reachable.

**What it actually is: a global variable with a nicer name**, plus a hidden dependency in every user.

| Cost | |
|---|---|
| **Untestable** | Tests share state and pass or fail depending on order. **Every "flaky test" story has one of these in it** |
| **Hidden dependency** | `Config.instance()` inside a function means the signature lies about what the function needs |
| **Lifetime is wrong** | "One per process" is the wrong scope for almost everything. One per request, one per transaction, one per tenant |
| **Concurrency** | Lazy initialisation needs a lock. `roomsvc`'s `SETTINGS` is mutated in three places from four workers |

**In Python it is also unnecessary**, because a module is already a singleton: `import config; config.SMTP_HOST` gives you one instance without a pattern.

**When it is defensible:** a genuinely process-wide, immutable resource — a connection pool, a metrics registry, a logger. **Note that all three are infrastructure, none holds business state, and all three should still be *passed in* to anything you want to test.**

> **What to do instead, and it is the whole of dependency injection without the framework:**
> **pass it as an argument.** `def confirm(hold_id, repo, notify)`. Three extra characters at the
> call site, and the function now states its dependencies truthfully and can be tested in
> microseconds.

---

## 5. Adapter — Genuine Engineering

**The problem:** you have a class with the behaviour you need and the wrong interface, and you cannot change it — it is a library, a vendor API, or the university's SSO.

**This one does not reduce to a language feature**, because the work is the translation, not the indirection.

```python
# slot/infra/sso.py
class UniversitySSOAdapter:
    """Adapts the university IdP's response to slot's User."""
    def __init__(self, client: OIDCClient): self._c = client

    def authenticate(self, token: str) -> User:
        claims = self._c.introspect(token)
        return User(
            id=UUID(claims["sub"]),
            # the IdP calls staff "employeeType=E"; slot has a role enum
            role=Role.STAFF if claims.get("employeeType") == "E" else Role.STUDENT,
            # 'eduPersonPrimaryAffiliation' is absent for emeritus staff (!)
            department=claims.get("eduPersonPrimaryAffiliation", "UNKNOWN"),
        )
```

**Every line of that mapping is knowledge** — about a system you do not control, discovered painfully. **The value of the adapter is that the knowledge is in one file**, with a comment per surprise, rather than distributed across every call site.

**`roomsvc` has no adapter**, and the consequence is exact: `employeeType == 'E'` appears in **four files**, and when the IdP added `employeeType=R` for research staff in 2023, research staff could not book equipment for five months.

> **Adapter is the pattern to reach for at every boundary with something you do not own.**
> That is the SSO, the calendar API, the email provider, and — arguably — the ORM.

---

## 6. Facade, Decorator, Proxy — Briefly

**Facade** — one simple interface over a complicated subsystem.

**Your application layer is a facade** over repositories, the event bus and the notifier. That is not a coincidence and it is worth naming: a good facade is *task-shaped*, offering `confirm_booking(hold_id)` rather than exposing the five things that happen inside.

**The failure mode:** a facade that grows a method per call site, ending up as wide as the thing it was hiding. **`views.py` is a facade that lost.**

**Decorator** (the structural pattern, not `@syntax`) — wrap an object in another with the same interface, adding behaviour.

**Python's `@` decorators cover the function case entirely.** The object case is still real and still useful:

```python
class LoggingBookingRepo:                       # same interface as BookingRepo
    def __init__(self, inner, log): self._i, self._log = inner, log
    def confirm(self, hold_id):
        t = time.perf_counter()
        try: return self._i.confirm(hold_id)
        finally: self._log.info("confirm %s took %.1fms", hold_id,
                                (time.perf_counter()-t)*1000)
```

**Adds timing to every repository call without touching the repository or its callers.** This is a genuinely good use and it costs nothing; it is also how you get the Week 11 numbers.

**Proxy** — same interface, controls access. Caching, lazy loading, remote calls.

**Under-rated caution:** SQLAlchemy's lazy-loading relationships are proxies, and **they are where your N+1 queries come from** (W3 L11 §1). The pattern works by making an expensive thing look free, and that is exactly its danger. **Week 11 measures it.**

---

## 7. The Distinction Worth Keeping

**Adapter, Facade, Decorator and Proxy all have the same shape** — an object wrapping another object — and students confuse them constantly. **They differ entirely in intent:**

| Pattern | Interface of the wrapper | Intent |
|---|---|---|
| **Adapter** | **Different** from the wrapped | Make an incompatible thing fit |
| **Facade** | **New and simpler**, over several things | Hide complexity |
| **Decorator** | **Same** as the wrapped | Add behaviour, transparently |
| **Proxy** | **Same** as the wrapped | Control access — cache, defer, authorise, go remote |

**Decorator and Proxy have identical structure and are distinguished only by why you did it.** That is not a flaw in the taxonomy; it is the point of L13 §1 — **a pattern is named for its problem.** Two identical structures with different problems are two patterns, and a reader who knows which one you meant knows what you were worried about.

---

## 8. Summary

- **Creational patterns exist because "which object to make" changes for different reasons than "what to do with it".** `roomsvc` constructs an `SMTPMailer` inside `confirm_booking`, in eleven places.
- **Factory Method and Abstract Factory are usually a function or a dict in Python.** Reach for classes when the created objects differ in *behaviour*, not in a number.
- **Builder survives where it matters most: test data.** A test that states six facts to test one is unreadable. `tests/factories.py`, this week — it is the highest-value pattern in the lecture.
- **Singleton is a global variable with a nicer name**: untestable, a hidden dependency, almost always the wrong lifetime, and unnecessary in Python because modules are singletons. **Pass it as an argument instead.**
- **Adapter is genuine engineering**, because the work is the translation. `roomsvc` has none, and `employeeType == 'E'` in four files locked research staff out for five months.
- **Facade, Decorator and Proxy are all "wrap an object"**, and a `LoggingBookingRepo` is a free win. **Lazy-loading proxies are where your N+1 queries come from.**
- **Adapter, Facade, Decorator and Proxy share a shape and differ only in intent** — which is the clearest demonstration in the course that **a pattern is named for its problem.**

**Next:** L15 — behavioural patterns, the ones that became language features, and the three that are still worth their names.

---

*CS 212 · Week 4 · L14 · © CSE Department*
