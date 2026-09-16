# CS 212 · Reading Guide · Week 4

---

## Required

| # | What | Length | Why |
|---|---|---|---|
| 1 | **Gamma et al., *Design Patterns*, Ch. 1** | ~30 pages | The introduction, which contains all the caveats the rest of the industry forgot. §1.6 *"How to Select a Design Pattern"* and §1.8 are the parts to read twice |
| 2 | **Norvig, *"Design Patterns in Dynamic Languages"*** (1996 slides, norvig.com) | ~20 min | The 16-of-23 claim, with the demonstrations. **Read it before L15** |
| 3 | **GoF Ch. 3–5, selectively** | — | **Do not read cover to cover.** Read the *Intent*, *Motivation* and *Consequences* of: Adapter, Facade, Decorator, Observer, Strategy, State. Skip the sample code; it is C++ |

**About ninety minutes if you obey the "selectively".**

---

## Recommended

| What | Why |
|---|---|
| **Alexander, *A Pattern Language* (1977)** — any ten pages | Read ten patterns about buildings. It will change how you read the software ones, because you will see immediately that they are **arguments about how people live**, not structures |
| **Alexander's OOPSLA 1996 keynote** (transcript online) | Twenty minutes. The originator telling the software community what he thinks they missed |
| **Fowler, *Patterns of Enterprise Application Architecture*** (2002) | **More useful for `slot` than GoF.** Repository, Unit of Work, Data Mapper, Service Layer, Identity Map — read those five entries |
| **Nygard, *Release It!*, 2nd ed.** (2018), Ch. 5 | Circuit Breaker, Bulkhead, Timeout. The patterns that come from operating systems rather than designing them |
| **Meszaros, *xUnit Test Patterns*** (2007) — Object Mother, Test Data Builder | L14 §3's pattern. Twenty pages, and it will improve every test you write from Week 5 on |

---

## How to Read GoF Without Being Damaged By It

**The book's structure works against you.** Twenty-three chapters of equal length imply twenty-three patterns of equal value, and the sample code — C++ from 1994 — implies that the structure is the pattern.

**A reading order that works:**

1. **Chapter 1 in full.** It is the only part that tells you when *not* to use these.
2. **For any pattern: read Intent, then Motivation, then Consequences. Stop.** Those three sections are the pattern. Structure, Participants, Collaborations and Sample Code are an implementation in a language you are not using.
3. **Then write the Python yourself**, before looking at anything. Norvig's point will be obvious from doing it once.
4. **Read *Related Patterns* at the end of each entry.** It is where the book is most honest about overlap — Decorator and Proxy, Strategy and State, Adapter and Facade.

**The sentence to carry out of Chapter 1**, and it is in the book:

> *"Design patterns should not be applied indiscriminately. Often they achieve flexibility and
> variability by introducing additional levels of indirection, and that can complicate a design
> and/or cost you some performance."* — GoF, §1.8

---

## On the Pattern Catalogue Being Incomplete

**GoF is 1994 and is about object-oriented desktop and framework code.** Three whole families of pattern that your project needs are not in it:

| Family | Where | Examples |
|---|---|---|
| **Enterprise / persistence** | Fowler, *PoEAA* (2002) | Repository, Unit of Work, Data Mapper, Identity Map, Service Layer |
| **Stability / distributed** | Nygard, *Release It!* (2007) | Circuit Breaker, Bulkhead, Timeout, Fail Fast, Steady State |
| **Integration / messaging** | Hohpe & Woolf (2003) | Transactional Outbox, Idempotent Receiver, Dead Letter Channel |

**Two of the three most useful patterns in this course — Repository and Transactional Outbox — are in the second and third rows**, and neither is in the book everyone means when they say "design patterns". **The vocabulary has kept growing; the reputation has not.**

---

*CS 212 · Week 4 · Reading Guide*
