# PROG 102 · Lecture 22
## What Patterns Are

**Week 7 · Monday · 50 minutes**
**Reading:** Gang of Four, Ch. 1 · **Reference:** Meyers Items 32–36 (inheritance design)
**Assumes:** Week 4 (inheritance, abstract classes), Week 6 (you have implemented one already)

---

## 1. The Claim

> **A design pattern is a named, reusable solution to a recurring problem in software design.**

Four words matter in that sentence.

**Named.** The main deliverable is vocabulary. "Wrap it in a decorator" communicates a structure in
three words to anyone who knows the term; without it you draw a diagram.

**Reusable.** It is a shape, not code. There is no `std::factory` to include — you write the classes,
and the pattern tells you how to arrange them.

**Recurring.** The Gang of Four did not invent these. **They read a great deal of working code, noticed
the same structures appearing, and wrote them down.** Patterns are field observations.

**Design.** Not algorithms. An algorithm tells you how to compute; a pattern tells you how to arrange
classes so the computation can change later.

---

## 2. You Have Already Implemented One

Week 6's iterator is the **Iterator pattern**: *provide a way to access the elements of an aggregate
sequentially without exposing its underlying representation.*

You did not apply a pattern. **You solved a problem, and the solution turned out to have a name.**

That is the strongest available argument that patterns are descriptive rather than prescriptive, and it
is worth holding onto for §6, where the failure mode is the opposite.

Two others you have met:

- **Adapter** — `std::stack` (L11 §7) wraps a `deque` and exposes a different interface.
- **Template Method** — `std::sort` defines the algorithm's skeleton and takes the comparison as a
  parameter. *(Week 8 names this one.)*

---

## 3. The Two Principles

The Gang of Four's catalogue is 23 patterns. **Its two design principles are worth more than the
catalogue**, and they are the actual content of the book.

### 3.1 Favour Object Composition Over Class Inheritance

```cpp
class Buffered : public FileSource { ... };            // inheritance
class Buffered : public DataSource {                   // composition
    std::unique_ptr<DataSource> inner;
};
```

**Inheritance is the tightest coupling C++ offers** (L13 §2). The derived class depends on the base's
interface, its `protected` members, its invariants, and its construction order — and that dependency
is fixed **at compile time**.

Composition depends only on a public interface, and the thing composed can be **chosen at run time**.
Lecture 24 §3 measures what that is worth: $2^n$ classes become $n$.

> **This is not "inheritance is bad".** Week 4 exists because runtime polymorphism is genuinely useful
> and requires it. The principle is about *reuse*: **inherit to be substitutable, compose to reuse
> behaviour.** If you are inheriting because the base has a function you want, you wanted a member.

### 3.2 Program to Interfaces, Not Implementations

```cpp
void render(const Shape& s);                  // any shape, including ones I have never seen
void render(const Circle& c);                 // only circles
```

You have been doing this since Week 4. **Week 6 is the sharpest example**: `std::accumulate` is
programmed against the *iterator protocol*, which is why it worked on a container written decades after
it.

The practical test: **can I add a new implementation without editing existing code?** If yes, you
programmed to an interface. If you must find and edit a `switch` or an `if`-chain, you did not — and
L15 §4.4's `dynamic_cast` chain is what that looks like.

---

## 4. What a Pattern Description Contains

The Gang of Four give each pattern a fixed structure, and it is worth knowing because it is how the
book is usable as a reference:

| Section | What it tells you |
| --- | --- |
| **Intent** | One sentence. Read this first, and often only this |
| **Motivation** | A concrete problem |
| **Applicability** | **When to use it — and the "use it when" list is a checklist you should fail sometimes** |
| Structure | The class diagram |
| Consequences | **The trade-offs.** The most under-read section |
| Implementation | Language-specific notes |
| Known uses | Where it appears in real systems |

**Read Intent, Applicability and Consequences. Skim the rest.** A pattern you cannot state the intent
of in one sentence is one you should not be using.

---

## 5. The Three Categories

| Category | Concerned with | This course |
| --- | --- | --- |
| **Creational** | How objects get made | **L23** |
| **Structural** | How objects are composed | **L24** |
| **Behavioural** | How objects interact and share responsibility | **Week 8** |

The split is a filing convenience, not a deep truth. Some patterns sit awkwardly in it — Iterator is
filed behavioural and is arguably structural.

---

## 6. When Not to Use a Pattern

The most valuable thing in this week, and the hardest to assess, so it is worth being blunt.

**Patterns solve the problem of things changing.** A Factory exists because the concrete type may need
to vary. A Strategy exists because the algorithm may need to vary. **If it is not going to vary, the
pattern is pure cost:** more classes, more indirection, more files to open to follow one call.

### 6.1 The Symptoms of Over-Patterning

- **An interface with one implementation, ever.** You have added a virtual call and a file to
  achieve nothing.
- **A factory that returns one type.** That is a constructor with extra steps.
- **Class names that are pattern names.** `RequestHandlerFactoryStrategyImpl` describes the mechanism
  and not the job. **A class should be named for what it does.**
- **Following a call requires four files.** Indirection has a readability cost and it is not small.

### 6.2 The Test

> **Ask what specific change this pattern makes easy, and whether that change is actually coming.**

If you can name it — "we will need a second theme when the client asks for dark mode" — the pattern is
buying something. If the answer is "it might be useful one day", **you are paying now for an option
that expires unexercised.**

The honest form of the advice, which the Gang of Four themselves give in Chapter 1 and almost nobody
quotes:

> **Write the simple thing. When it needs to change, the pattern will be obvious — and you will know
> which one, because you will have the actual requirement rather than a guess.**

Refactoring *into* a pattern is easy, well-understood work. **Refactoring out of a pattern nobody
needed is harder**, because by then there are five files and a test suite shaped around it.

### 6.3 And Some of Them Are Just Bad

Not all 23 have aged well. **Singleton in particular** is widely regarded as an anti-pattern — Lecture
23 §2 presents it, shows the correct C++ implementation, and then explains why you should usually not.

**A pattern being in the book is not an endorsement.** It means it was observed, in 1994, in C++ and
Smalltalk codebases, before templates were standardised and before lambdas existed. Week 8 §L27 shows
two patterns that C++11 made nearly obsolete.

---

## 7. Summary

| Idea | The point |
| --- | --- |
| A pattern is a **named** solution shape | The vocabulary is the main deliverable |
| Descriptive, not prescriptive | Observed in working code, not invented |
| You built Iterator in Week 6 | Without knowing it was a pattern |
| **Composition over inheritance** | Inheritance is compile-time and tightly coupled |
| **Program to interfaces** | Test: can you add an implementation without editing anything? |
| Read Intent, Applicability, Consequences | Skim the rest |
| Three categories | Creational, structural, behavioural — a filing convenience |
| Patterns solve **change** | No change coming, no pattern needed |
| The test | Name the change it makes easy. Is it coming? |
| Some have aged badly | Singleton; and C++11 obsoleted others |

---

## 8. Exercises

**1.** Write the **Intent** sentence, from memory, for the Iterator pattern. Then compare it with the
Gang of Four's. **How close were you, having implemented it?**

**2.** Find three patterns in the C++ standard library that were not named in this lecture. For each,
give the class and one sentence on what varies.

**3.** Take a class hierarchy from your PS 4 or PS 6 code. **Identify one place where you used
inheritance to reuse behaviour rather than to be substitutable**, and rewrite it with composition. If
there is no such place, say so and show why.

**4.** Someone proposes an `IShapeFactory` interface for a program with exactly one shape type that
has never changed. **Write the three-sentence objection**, then write the three-sentence case *for*
it — the strongest version you can.

**5.** Find a real codebase (or a large open-source project) and locate one class whose name contains a
pattern name. **Is the name earning its keep?** Argue either way.

**6.** The Gang of Four say "program to interfaces, not implementations". `std::sort` takes a
*template parameter*, not a base-class pointer. **Is that programming to an interface?** Answer in
three sentences.

**7.** Name a change that a Factory Method makes easy and a change it makes *harder*. The second half
is the point.

---

## 9. Next

**Lecture 23** is the creational patterns — the four ways of controlling how objects come into
existence, including the one you should mostly avoid and the one that will quietly improve every
constructor you write with more than four parameters.

---

*PROG 102 · Week 7 · Lecture 22 · © CSE Department*
