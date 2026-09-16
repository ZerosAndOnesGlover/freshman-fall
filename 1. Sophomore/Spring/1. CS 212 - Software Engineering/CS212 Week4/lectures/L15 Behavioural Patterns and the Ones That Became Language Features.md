# CS 212 · Software Engineering
## Week 4 · Lecture 3 of 3
### Behavioural Patterns, and the Ones That Became Language Features

---

**Sat:** Thursday of Week 4, 10:00–10:50, TH 200 · **Reading:** GoF Ch. 5, selectively; Norvig, *"Design Patterns in Dynamic Languages"* (1996) · **Next:** Week 5, testing

---

## 1. Strategy, Command, Template Method: One Idea, Three Names

**All three answer the same question** — *how do I vary one step of an algorithm without editing it?* — and in a language with first-class functions, **all three are "pass a function".**

| Pattern | GoF framing | Python |
|---|---|---|
| **Strategy** | Encapsulate a family of algorithms; make them interchangeable | A callable parameter |
| **Command** | Encapsulate a request as an object, so it can be queued, logged, undone | A closure, or `functools.partial` |
| **Template Method** | A base class defines the skeleton and defers steps to subclasses | A function taking callables for the varying steps |

**The distinction is not worthless, though.** Each carries a different *hint* about what you intend:

- **Strategy** says *"this will be chosen at runtime from several"*.
- **Command** says *"this will be stored, passed around, and executed later — possibly undone"*.
- **Template Method** says *"the skeleton is fixed and must not be overridden; only these holes vary"*.

**Where Command still earns a class**: when you need the *reification*. A command object can be serialised into a queue, logged for audit, retried, and inverted. **`slot`'s `outbox` table is Command** — each row is a request-to-notify, stored, retried, and discardable (W3 L12 §4).

**Where Template Method still earns inheritance**: almost nowhere in Python, and `roomsvc` has the counter-example. `reports.py` defines `BaseReport.generate()` calling four abstract hooks; the five subclasses override between one and four of them; **two override `generate()` itself**, which defeats the pattern entirely and is invisible until you read all five.

> **The general lesson, and it is the week's sharpest:** **inheritance is a very strong form of
> coupling** — connascence of *execution order* across a class boundary (W2 L07 §6). A subclass
> depends on the order in which the base class calls its hooks, which is not in any signature.
> **Composition — passing the varying step in — makes the dependency visible in the type.**

---

## 2. Observer: the One Whose Relationship Is the Point

**The problem:** one object changes, and an unknown number of others must react — and it must not know who they are.

**This does not reduce to a language feature**, because the content is the *many-to-one registration*, not the callback.

```python
class EventBus:
    def __init__(self): self._subs: dict[type, list[Callable]] = defaultdict(list)
    def subscribe(self, event_type, handler): self._subs[event_type].append(handler)
    def publish(self, event):
        for h in self._subs[type(event)]:
            h(event)          # <- see the warnings below
```

**Four things that will bite you, and they bite every team that adopts this:**

1. **A raising handler kills the rest.** The loop above stops at the first exception, so a failing audit write silently prevents the email. **Decide, deliberately, whether handlers are isolated — and if so, what happens to the failure.**
2. **Order is not guaranteed and will be relied on anyway.** Someone will write a handler that assumes another ran first. **Then it becomes connascence of execution across files, which is the worst kind.**
3. **You cannot answer *"what happens when a booking is confirmed?"* by reading.** You must search for subscribers (W3 L12 §4). In a 4,000-line project this is a real loss.
4. **Publishing inside a transaction re-creates the original bug.** If a handler sends an email and the transaction later rolls back, you have emailed about a booking that does not exist — **which is `roomsvc`'s `bookings.py:398` with the arrow reversed.** Publish after commit, or use the outbox.

> **When Observer is right for `slot`: three or more subscribers to one event.** Below that, call
> the function. **The ADR must name the third subscriber** (W3 L12 §5), and if you cannot, you have
> a function call wearing a costume.

---

## 3. State: When the `if` Tree Has Outgrown Itself

**The problem:** an object's behaviour depends on its state, and the transitions are numerous enough that scattered `if`s stop being trustworthy.

**`slot` has exactly three states and four legal transitions**, which is well inside `if`-tree territory — **and the honest version is a table, not a class hierarchy:**

```python
TRANSITIONS: dict[tuple[State, State], None] = {
    (State.HELD,      State.CONFIRMED): None,
    (State.HELD,      State.CANCELLED): None,
    (State.CONFIRMED, State.CANCELLED): None,
}

def transition(b: Booking, to: State) -> Booking:
    if (b.state, to) not in TRANSITIONS:
        raise IllegalTransition(b.state, to)
    return replace(b, state=to)
```

**Why the table beats both the `if` tree and the State pattern here:**

- **The whole rule is visible in four lines**, so a reviewer can check it against the domain model.
- **It is exhaustively testable** — iterate over `State × State` and assert the complement raises. **Nine cases, one loop.** W1 L06 §4's invariant I3 becomes a test rather than a hope.
- **Adding a state makes you look at the table**, which is the open/closed benefit without the classes.

**When the State pattern's classes earn their place:** when each state has substantially *different behaviour* across several operations, not just different legal transitions. A `Booking` that prices differently, notifies differently and renders differently per state would qualify. **`slot`'s does not**, and A 4 will reward a student who says so.

---

## 4. The Ones That Became Syntax

Worth naming, because you use all of them daily and may not know they had names.

| Pattern | Language feature | Since |
|---|---|---|
| **Iterator** | `__iter__` / `yield` / generators | Python 2.2 (2001) |
| **Decorator** (function case) | `@decorator` | Python 2.4 (2004) |
| **Template Method** (simple case) | Default arguments that are callables | Always |
| **Visitor** | `functools.singledispatch`; `match` statements | 3.4 (2014) / 3.10 (2021) |
| **Prototype** | `copy.deepcopy` | Always |
| **Memento** | `pickle`, `dataclasses.replace` | Always |
| **Chain of Responsibility** | Middleware lists; exception propagation | Always |
| **Flyweight** | String interning; `@lru_cache`; `__slots__` | Always |

**Why this table is worth ten minutes.** Not to be able to recite it — **to see the process.** A pattern is a workaround for something the language cannot say. **When enough people write the workaround, the language grows a way to say it**, and the pattern stops being a pattern and becomes syntax.

**Which tells you what to do with any pattern you are about to apply:** ask whether your language already says this. **In Python, for behavioural patterns, the answer is usually yes.**

**And it tells you something about the field.** `async`/`await` absorbed a decade of callback patterns. Context managers absorbed acquire/release protocols. Structural typing absorbed much of Interface Segregation. **The patterns catalogue is a list of things languages had not yet learned to say in 1994**, and a quarter of it has since been said.

---

## 5. Visitor, Because It Is the Interesting Failure

**The problem:** you have a fixed set of types and a growing set of operations over them, and you do not want to add a method to every type for every operation.

**GoF Visitor** requires every type to have `accept(visitor)`, and every visitor to have `visit_X` per type. **It is a lot of machinery, and it exists because C++ and Java lack multiple dispatch.**

```python
@singledispatch
def to_ical(event): raise NotImplementedError(type(event))

@to_ical.register
def _(e: BookingConfirmed): return f"BEGIN:VEVENT\nUID:{e.booking_id}\n..."

@to_ical.register
def _(e: BookingCancelled): return f"BEGIN:VEVENT\nUID:{e.booking_id}\nSTATUS:CANCELLED\n..."
```

**Same capability, no `accept` methods, and the types do not know the operation exists** — which is better than GoF Visitor, because in GoF the types must be modified once to add `accept`.

**The remaining reason Visitor is interesting is the *expression problem***, which you will meet properly in CS 311: it is hard for a language to make *both* adding a type *and* adding an operation easy. **Object-orientation makes adding a type easy and adding an operation invasive; functional dispatch makes adding an operation easy and adding a type invasive.** Visitor is object-orientation buying the functional trade at the cost of ceremony.

**Knowing that this is a real, named, unsolved tension** is worth more than knowing the pattern.

---

## 6. What to Actually Do This Week

A 4 asks you to *refactor toward* a pattern and **document the smell it removes**. So find the smell first.

**Look for these four, in this order:**

| Smell | What it usually wants |
|---|---|
| **The same `switch`/`if` on a type or kind, in more than two places** | Polymorphism or a dispatch table. **This is A 2's pricing case, and `slot` will have its own by now** |
| **A function whose parameters include a boolean that changes what it does** | Two functions, or a passed-in callable (Strategy) |
| **Construction of an infrastructure object inside domain logic** | Pass it in. Anything else is a Singleton in disguise |
| **A test that constructs six fields to assert one** | A test data builder. `tests/factories.py` |

**And two things not to do:**

- **Do not add a pattern to a place that has no smell.** A 4 is marked on the smell removed, not on the pattern applied, and a pattern applied to healthy code is a defect you have introduced.
- **Do not refactor the pricing case again.** That was A 2. **Find a new one in your own project.**

---

## 7. Summary

- **Strategy, Command and Template Method answer one question** — how to vary a step — and in Python all three are "pass a function". **The distinction survives as a hint about intent**: chosen at runtime, stored and replayable, or a fixed skeleton with holes.
- **Command earns a class when you need reification** — `slot`'s `outbox` table is Command.
- **Template Method's inheritance is very strong coupling**: connascence of execution order across a class boundary, invisible in any signature. `roomsvc`'s `BaseReport` has two subclasses that override the template itself. **Composition makes the dependency visible in the type.**
- **Observer's content is the many-to-one registration**, and four things bite: a raising handler kills the rest, order gets relied on, you lose the ability to read the control flow, **and publishing inside a transaction re-creates the original bug.**
- **State: for three states and four transitions, a table beats both the `if` tree and the pattern** — visible in four lines, exhaustively testable in nine cases, and it turns invariant I3 into a test.
- **Eight patterns became syntax**, and the process is the lesson: **a pattern is a workaround for something the language cannot say, and languages learn.**
- **`singledispatch` is a better Visitor than Visitor**, and the residue — the **expression problem** — is a real, named, unsolved tension rather than a gap in your knowledge.
- **A 4 is marked on the smell removed.** Find the smell first; a pattern applied to healthy code is a defect.

**Next:** Week 5 — testing. Where the acceptance criterion from Week 1 finally becomes a test that runs, including the concurrent one that `roomsvc` never had.

---

*CS 212 · Week 4 · L15 · © CSE Department*
