# CS 212 · Software Engineering
## Week 4 · Lecture 1 of 3
### Patterns as a Vocabulary

---

**Sat:** Tuesday of Week 4, 10:00–10:50, TH 200 · **⚠️ Quiz 4 in the first ten minutes** — covers Week 3 · **Reading:** Gamma et al., *Design Patterns*, Ch. 1 · **Next:** L14, creational and structural
**A 2 was due Friday. A 3 is due Friday of this week.**

---

## 1. Where Patterns Came From, and Why It Matters

**Christopher Alexander was an architect** — of buildings. *A Pattern Language* (1977) catalogues 253 patterns for towns, buildings and rooms: *Light on Two Sides of Every Room*, *Six-Foot Balcony*, *Window Place*.

**His definition is still the best one:**

> *"Each pattern describes a problem which occurs over and over again in our environment, and then
> describes the core of the solution to that problem, in such a way that you can use this solution
> a million times over, without ever doing it the same way twice."*

**Three clauses, and all three are load-bearing:**

| Clause | What it rules out |
|---|---|
| *"a problem which occurs over and over"* | **A pattern is named for its problem, not its structure.** If you cannot state the problem, you do not have a pattern |
| *"the core of the solution"* | **Not the code.** A pattern is not a class diagram you copy |
| *"without ever doing it the same way twice"* | **Every instance differs.** A pattern that looks identical everywhere is a library function you failed to write |

**Alexander's own verdict on what happened next is worth knowing.** Invited to address OOPSLA in 1996, he told a room of software people that he was not sure they had taken the important part — which for him was that patterns exist to make things *better for the people who live in them*, and that a pattern language needs a **moral** component. Software's patterns movement kept the catalogue and dropped that. **You may think this is a soft point. It is the reason the field's patterns became a checklist within a decade.**

---

## 2. The Gang of Four, In Context

**Gamma, Helm, Johnson and Vlissides, 1994.** Twenty-three patterns, C++ and Smalltalk, and one of the best-selling technical books ever written.

**What it got right, and it is a lot:**

1. **A shared vocabulary.** *"Let's make this a strategy"* conveys in four words what takes two minutes to draw. **This is the durable contribution and it is why the book still matters.**
2. **It documented what good designers were already doing.** The patterns were *mined*, not invented — the book's introduction is explicit that a pattern had to appear in at least three real systems.
3. **It made design discussable** at a level above the class and below the architecture, which had no vocabulary before.

**What it got wrong, or what time did to it:**

| | |
|---|---|
| **The catalogue became a checklist** | Students learned twenty-three patterns and applied them, rather than recognising problems. **Peter Norvig's observation (1996) is the sharp form: 16 of the 23 patterns are "invisible or simpler" in a dynamic language** |
| **C++ is in the patterns** | Several exist to work around C++'s type system and object model. In Python, some are one line |
| **"Patterns are good" became the reading** | The book says repeatedly that patterns add indirection and should be applied to a demonstrated problem. Nobody quotes those paragraphs |
| **It aged where the languages moved** | First-class functions, closures, generators, `with`, decorators, `@dataclass` and structural typing each absorbed a pattern or three |

> **The honest summary:** *Design Patterns* is a **vocabulary**, plus a set of **case studies in
> trade-offs**, plus about six patterns that are still genuine engineering in Python. It is not a
> catalogue of things to add to your project.

---

## 3. Norvig's Point, Demonstrated

Norvig's 1996 claim, checked in Python:

**Strategy** — GoF: an interface, N implementing classes, a context that holds one.

```python
# GoF, in Python
class PricingStrategy(Protocol):
    def price(self, booking) -> Decimal: ...

class ExternalPricing:
    def price(self, booking): return RATE * booking.hours * 1.2

class Booker:
    def __init__(self, strategy: PricingStrategy): self._s = strategy
    def total(self, b): return self._s.price(b)

# Python
def total(booking, price):          # price is any callable
    return price(booking)
```

**The pattern has not disappeared** — you still have "a replaceable algorithm passed in from outside", which is the *idea*. **What disappeared is the ceremony**: the interface declaration, the classes, the field, the constructor.

**Same for these:**

| Pattern | What it becomes in Python |
|---|---|
| **Strategy** | A function argument |
| **Command** | A closure, or `functools.partial` |
| **Template Method** | A function taking a callable for the varying step |
| **Iterator** | `__iter__`, generators, `yield` — **built into the language** |
| **Singleton** | A module-level object. Modules are already singletons |
| **Factory Method** | A function |
| **Abstract Factory** | A module, or a dict of constructors |
| **Decorator** (structural) | `@decorator` syntax for the function case, though the object case is still real |
| **Visitor** | `functools.singledispatch`, or `match` |
| **Prototype** | `copy.deepcopy` |

**This is not a reason to skip the week.** It is the reason to learn the patterns **as problems** rather than as structures — because the problems are still there and the structures are not.

> **Concretely:** when someone says *"use the Strategy pattern"*, they mean *"the way this varies
> should be passed in, not branched on"*. That instruction is exactly as useful in Python as in Java.
> The five classes are not.

---

## 4. What a Pattern Description Should Contain

The GoF template, reduced to the four parts that matter. **A 4 requires you to produce this for the pattern you apply.**

| Part | Why |
|---|---|
| **Problem / when to use it** | The only part that helps you *recognise* an occasion. **If a colleague cannot state this, they are pattern-matching on shape** |
| **Solution, structurally** | The core, in your language, with the ceremony your language does not need removed |
| **Consequences** | **What it costs.** Every pattern adds indirection; several add allocation; some make debugging worse. **The book has this section and nobody reads it** |
| **Known uses** | Have you seen it work? In what? If the only known use is the textbook example, be careful |

**The consequences section is what separates knowing a pattern from being able to use one.** Every pattern is a trade, and a team that can only name the benefit will apply it everywhere.

---

## 5. The Failure Mode: Pattern-Oriented Programming

The characteristic disease, and you will see it in one team's project this term:

```
AbstractBookingFactoryProvider
  → BookingFactoryProvider
    → ConcreteBookingFactory
      → BookingBuilder
        → BookingBuilderDirector
          → Booking
```

**Six classes to construct an object with three fields.** Every one of them is a real pattern, correctly implemented, and the whole is unreadable.

**The failure is not in any one decision.** It is that each was made without asking *what problem does this solve here?* — and the answer, in all six cases, was "none yet".

**Three tests, apply them to your own project this week:**

1. **Name the problem.** Not the pattern — the problem. *"We have three pricing rules and the `if` tree is switched on in four places"* is a problem. *"We should use Strategy"* is not.
2. **Name the second case.** (W2 L08 §7 again, and it keeps coming back because it keeps being the right question.) A Strategy with one strategy is a function with extra steps.
3. **Count the files a reader must open** to answer one question about behaviour. Before and after. **If the number went up and nothing else got better, revert it.**

> **Fowler's rule, and it is the shortest form:** *patterns are a destination, not a starting point.*
> **You refactor towards a pattern when the code tells you it wants one** — which is Week 9's
> material, and which is why A 4 is phrased as *"refactor toward a pattern; document the smell it
> removes"* rather than *"add a pattern"*.

---

## 6. The Ones Still Worth Their Names in Python

Not the full twenty-three. **The ones that survive Norvig's test** — where the pattern still buys you something a language feature does not.

| Pattern | Why it survives | Where in `slot` |
|---|---|---|
| **Adapter** | Making an incompatible interface fit is real work, not ceremony | Wrapping the university SSO's response into your `User` |
| **Facade** | A simple front over a complicated subsystem is genuinely valuable | Your application layer over four repositories |
| **Observer** | The **relationship** is the content, and it is not a language feature | An in-process event bus — **if you have three subscribers** (W3 L12 §4) |
| **State** | When transitions are complex, a table or classes beat an `if` tree | `HELD → CONFIRMED → CANCELLED`, if it grows |
| **Repository** | Not GoF (Fowler, *PoEAA*) — **and the most useful one in this course** | `BookingRepo`; W3 L11 §2 |
| **Unit of Work** | Not GoF either. Transaction boundary as an object | Your `with uow:` block |
| **Null Object** | Cheap, removes a whole class of `if x is not None` | A `NullNotifier` in tests |
| **Circuit Breaker** | Not GoF (Nygard, *Release It!*). Real distributed-systems engineering | Only if you call the calendar API |

**Notice that three of the eight are not in the Gang of Four book at all.** The useful vocabulary has kept growing, and the most useful patterns for a web service in 2026 come from Fowler's *Patterns of Enterprise Application Architecture* (2002) and Nygard's *Release It!* (2007). **The GoF book is a foundation, not the field.**

---

## 7. Summary

- **Alexander's definition has three load-bearing clauses**: a recurring problem, the *core* of a solution, and never the same twice. A pattern is **named for its problem**.
- **The Gang of Four's durable contribution is the vocabulary**, and the patterns were mined from real systems, not invented. **Its own caveats about indirection are in the book and are never quoted.**
- **Norvig, 1996: 16 of the 23 are invisible or simpler in a dynamic language.** Strategy is a function argument; Command is a closure; Iterator is `yield`; Singleton is a module.
- **The problems survive; the structures do not.** Learn patterns as problems, and *"use Strategy"* means *"pass the varying thing in rather than branching on it"*.
- **A pattern description needs its consequences**, and that is the section nobody reads and the one that stops you applying it everywhere.
- **Pattern-oriented programming is the failure mode**: six classes for three fields, each correct, the whole unreadable. **Name the problem; name the second case; count the files a reader must open.**
- **Patterns are a destination, not a starting point.** You refactor *towards* one.
- **Eight survive for `slot`, and three of the eight are not in the GoF book** — Repository, Unit of Work and Circuit Breaker come from Fowler and Nygard.

**Next:** L14 — the creational and structural patterns, in production code, including the two that are still genuine engineering and the one that is almost always a mistake.

---

*CS 212 · Week 4 · L13 · © CSE Department*
