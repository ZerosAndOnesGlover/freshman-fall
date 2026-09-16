# CS 212 · Software Engineering
## Week 4: Design Patterns in Depth

**Credits:** 3 · **Prerequisites:** PROG 102, CS 101
**Assessment for this course (overall):** Team Project 40%, Individual Assignments 30%, Midterm 15%, Final 15%
**This week's deliverables:** A 3 due Friday 17:00 · **A 4 released Wednesday** · **📊 Quiz 4 Tuesday** (covers Week 3)

---

### Why This Week Exists

Because you already know the twenty-three names, and the names are the least useful part.

**Peter Norvig checked, in 1996, and found that 16 of the 23 Gang of Four patterns are "invisible or simpler" in a dynamic language.** Strategy is a function argument. Command is a closure. Iterator is `yield`. Singleton is a module. **The structures dissolve, and the problems do not** — which is the whole content of the week.

**So the week teaches patterns as problems.** *"Use Strategy"* is not an instruction; *"the way this varies should be passed in rather than branched on"* is, and it is exactly as useful in Python as in Java. **A pattern is named for its problem** — which is why Decorator and Proxy have identical structure and are two different patterns, distinguished only by what you were worried about.

**And the week is honest about the catalogue's limits.** Three of the eight patterns still worth their names for `slot` — **Repository, Unit of Work and Circuit Breaker** — are not in the Gang of Four book at all. The vocabulary kept growing; the reputation did not.

**A 4 asks you to refactor toward a pattern and document the smell it removes**, in that order, and it is written so that *"the right answer was a dict"* is a full-marks answer.

---

### Learning Objectives

By the end of Week 4, you should be able to:

1. State **Alexander's definition** and say what each of its three clauses rules out.
2. Say what the Gang of Four got right — **a shared vocabulary, mined from real systems** — and what time did to it.
3. **Demonstrate Norvig's claim** on at least three patterns, and in each case say **what survives** when the structure dissolves.
4. Produce a **four-part pattern description**, and explain why the Consequences section is the one that stops you applying a pattern everywhere.
5. Recognise **pattern-oriented programming**, and apply the three tests: name the problem, name the second case, **count the files a reader must open.**
6. Say why **creational patterns exist** — construction is a decision that changes for different reasons than use — and find the eleven places `roomsvc` gets it wrong.
7. Use a **test data builder**, and say why a test that states six facts to assert one is a test you will eventually delete.
8. Explain why **Singleton is a global variable with a nicer name**, and give the alternative in three characters at the call site.
9. Distinguish **Adapter, Facade, Decorator and Proxy** — identical shapes, different intents — and say why `employeeType == 'E'` in four files locked research staff out for five months.
10. Name the **four things that bite** every team that adopts an event bus, including the one that re-creates `roomsvc`'s original bug with the arrow reversed.
11. Say why a **transition table beats both the `if` tree and the State pattern** for three states, and how it turns invariant I3 into nine test cases.
12. Explain **why inheritance is very strong coupling** — connascence of execution order, invisible in any signature — with `roomsvc`'s `BaseReport` as the evidence.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L13 Patterns as a Vocabulary]] | Alexander's three load-bearing clauses, and his own 1996 verdict on what software did with them; what GoF got right and what time did to it; **Norvig's 16 of 23, demonstrated**; the four-part description; **pattern-oriented programming and the three tests**; the eight still worth their names — **three of which are not in the book** |
| [[L14 Creational and Structural Patterns]] | Why construction is a decision, and the `SMTPMailer` built inside `confirm_booking` in **eleven places**; factories as functions and dicts; **the test data builder, which is the week's highest-value pattern**; Singleton as a global with a nicer name; **Adapter as genuine engineering**, and the four files that locked out research staff; Facade, Decorator, Proxy — **and the table that separates four identical shapes by intent** |
| [[L15 Behavioural Patterns and the Ones That Became Language Features]] | Strategy, Command and Template Method as one idea with three hints; **where Command still earns a class**; **inheritance as connascence of execution order**, with `BaseReport`'s two subclasses that override the template; **Observer's four bites**; the transition table that beats the pattern; **eight patterns that became syntax, and why that is the lesson**; `singledispatch` as a better Visitor, and the expression problem |
| [[CS212 Week4/assignments/QUIZ 4 Week 4 Tuesday\|QUIZ 4]] | Seven questions on Week 3, ten minutes, with its own answer key |
| [[CS212 Week4/assignments/A 4 Refactor Toward a Pattern\|A 4]] | Five questions, 100 points, due Friday of Week 5. **A non-pattern answer can score full marks; deletion scores highest** |
| [[CS212 Week4/resources/Reading Guide Week 4\|Reading Guide Week 4]] | **How to read GoF without being damaged by it** — Intent, Motivation, Consequences, then stop; and the three pattern families the book does not contain |
| `resources/report_template_before.py` | `BaseReport`, extracted, so L15 §1's claim about the two overriding subclasses is checkable |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A pattern is a workaround for something the language cannot yet say.**

Iterator became `yield` in 2001. Decorator became `@` in 2004. Acquire-release became `with` in 2005. Visitor became `singledispatch` in 2014 and `match` in 2021. Interface Segregation was largely absorbed by `Protocol` in 2019. **Eight of the twenty-three are now syntax, and the process that did that is still running.**

**Which tells you what to do with any pattern you are about to apply: ask whether your language already says this.** For behavioural patterns in Python the answer is usually yes, and reaching for the 1994 structure anyway adds five classes and removes nothing.

**And it tells you what patterns are *for*.** Not a catalogue of good things to include. **A record of the problems that recurred often enough that people built vocabulary around them** — and, read that way, the list is most valuable for the patterns that have *not* dissolved. Adapter has not dissolved, because translating between two systems you do not control is irreducible work. Observer has not, because a many-to-one registration is a relationship rather than a call. **Those are where the engineering still is.**

---

### Assessment Reminder

**Quizzes carry no weight. The project carries 40%.** Quiz *N* covers Week *N−1*, ten minutes at the start of **Tuesday's** lecture in Weeks 1–11, with its own key printed. Tracked in [[_CS 212 Quiz Record]].

**Assignments** released Wednesday 17:00, due Friday 17:00 of the week after; **lowest of thirteen dropped.** A 3 is due this Friday; A 4 is released Wednesday.

> **Week 6 is two weeks away and it holds three things in three days**: Quiz 6 and the Phase 1
> presentation on Tuesday 3 March, and the midterm on Wednesday 4 March, 18:00–19:15, covering
> Weeks 0–5. **Look at [[CS212 Week3/project/PHASE 1 CHECKPOINT|PHASE 1 CHECKPOINT]] this week if
> you have not.** 70 of Phase 1's 100 marks are for artefacts that exist in the repository before
> you present, and most of them are already assigned work.

---

### Connections

**Back:** **Week 2's "duplication is cheaper than the wrong abstraction"** is L13 §5's three tests in another form, and **W2 L08 §7's second-implementation test** is quoted directly because it keeps being the right question. **W3 L12 §4's transactional outbox** turns out to be Command reified, and **W3 L11 §2's ports** turn out to be Adapter under another name.

**Sideways:** **PROG 202 is doing higher-order functions and type classes**, which is this week's central claim from the other side — Haskell has never needed Strategy, because passing a function is the ordinary way to write anything. **CS 202's Week 4 is deadlock**, and its four Coffman conditions are a pattern description in the L13 §4 sense: a problem, its core, its consequences, its known uses.

**Forward:** **Week 5 is testing**, where the test data builder from L14 §3 pays immediately, and where Week 1's concurrency acceptance criterion finally becomes a test that runs. **Week 9 is refactoring done formally** — A 4 is a rehearsal for it, which is why the assignment is phrased as *refactor toward*. **Week 11** measures the indirection this week's patterns add, and asks whether it bought anything.

---

*CS 212 · Week 4 · © CSE Department*
