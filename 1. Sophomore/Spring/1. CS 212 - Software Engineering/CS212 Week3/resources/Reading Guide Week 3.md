# CS 212 · Reading Guide · Week 3

---

## Required

| # | What | Length | Why |
|---|---|---|---|
| 1 | **Cockburn, *"Hexagonal Architecture"*** (2005, alistair.cockburn.us) | **6 pages** | The original, and much more modest than its reputation. Note how little ceremony he actually prescribes |
| 2 | **Nygard, *"Documenting Architecture Decisions"*** (2011, cognitect.com) | **2 pages** | A 3 Q2 is this, applied. Read it before you write the first ADR, not after |
| 3 | **Sommerville Ch. 6 §6.1–6.2** | ~18 pages | Architectural design and views. The 4+1 view model is here if you want it |
| 4 | **Fowler & Lewis, *"Microservices"*** (2014, martinfowler.com) | ~20 min | The definitional article. Read it **with** #5, not without |
| 5 | **Fowler, *"MicroservicePremium"*** (2015) | **5 min** | The correction to #4, by one of its authors. *"Don't even consider microservices unless…"* |

**About two hours.** Read #5 immediately after #4; the pair is the point.

---

## Recommended

| What | Why |
|---|---|
| **Fowler, *"MonolithFirst"*** (2015) | Three pages; the practical form of the same argument |
| **Fowler, *"AnemicDomainModel"*** (2003) | Two pages, and L11 §3 assumes it. Your project will grow one by Week 6 unless someone names it |
| **Conway, *"How Do Committees Invent?"*** (Datamation, 1968) | The original of Conway's law. Same year as Garmisch, and it reads as freshly |
| **Ford, Parsons & Kua, *Building Evolutionary Architectures*** (2017), Ch. 2 | Where the *fitness function* idea comes from — which is what L11 §1's import test is |
| **Newman, *Building Microservices*, 2nd ed.**, Ch. 1 and 3 | If you are seriously considering splitting. Ch. 3 is honest about the costs |

---

## On Reading Cockburn Before the Textbooks

**Read the six-page original before anything that summarises it**, because the summaries have drifted a long way. Cockburn's paper does not prescribe a mapping layer, does not require one class per port, does not mention dependency injection frameworks, and is almost entirely about one idea: **the application should be drivable equally by a user, a test, or a batch script, and should be equally happy talking to a database or a fake.**

Much of what is now taught as "hexagonal architecture" is an accretion on top of that, and **the accretion is where the ceremony students resent comes from.** Reading the original is the cheapest way to tell which parts are load-bearing.

---

## A Warning About Architecture Reading in General

More than any other week, the writing here is **assertive, aesthetic and largely unevidenced.** There are very few controlled studies of architectural style, for the obvious reason that you cannot run a system two ways for three years.

**What that means for how you read it:**

- **Treat every claim as a hypothesis about cost**, and ask what would falsify it. A 3 Q5(b) makes you do exactly this with your own choice.
- **Notice who is selling something.** A large share of the microservices literature was produced by vendors of the surrounding tooling, and the correction (#5 above) came from someone who was not.
- **Prefer the writers who publish their own retractions.** Fowler's *MicroservicePremium* and *MonolithFirst* are both corrections to his own earlier enthusiasm. **That is what makes him worth reading**, and it is the same property that makes a good ADR — the record of having changed your mind.

---

*CS 212 · Week 3 · Reading Guide*
