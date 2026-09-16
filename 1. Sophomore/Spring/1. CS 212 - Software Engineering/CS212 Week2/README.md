# CS 212 · Software Engineering
## Week 2: Design Principles

**Credits:** 3 · **Prerequisites:** PROG 102, CS 101
**Assessment for this course (overall):** Team Project 40%, Individual Assignments 30%, Midterm 15%, Final 15%
**This week's deliverables:** A 1 due Friday 17:00 · **A 2 released Wednesday** · **📊 Quiz 2 Tuesday** (covers Week 1)

---

### Why This Week Exists

Because the obvious diagnosis of `confirm_booking` is wrong, and acting on it would make things worse.

**487 lines, complexity 94.** The reflex — extract until every function is four lines — is what *Clean Code* trains and what the syllabus explicitly rejects (§7.1). **Split it into nine four-line functions and every actual problem survives:** the VAT rate still lives in a file about booking rules, the email still cannot be tested without an SMTP server, the LDAP outage still takes bookings down, and the calendar POST is still inside the transaction, so a slow external service still rolls back a confirmed booking.

**Length was a symptom.** The disease has two fifty-year-old names — **cohesion** and **coupling** — and this week is those two ideas, then SOLID rated honestly against them, then the three slogans that get quoted most and understood least.

**And the week has one measurement that needs no judgement at all.** `bookings.py` absorbs **891 of 2,173 file-touches in two years — 41%**. A cohesive module is touched when its one concern changes; this one is touched when any of **eight** concerns change. That is what low cohesion looks like in a `git log`, and it is the diagnostic the rest of the course keeps returning to.

---

### Learning Objectives

By the end of Week 2, you should be able to:

1. **Explain why splitting `confirm_booking` by length fixes nothing**, naming at least four problems that survive the split.
2. Define **cohesion and coupling** in terms of what a single change should require you to touch and to read.
3. **Read low cohesion out of a `git log`** — and say why 41% of file-touches landing on one file is a design fact rather than an accident.
4. Rank cohesion and coupling on Constantine's scales, and apply the **name test** for functional cohesion.
5. Say why **stamp coupling** makes a function untestable, unscriptable and unreusable, and why **content coupling** dissolves another module's invariants.
6. State **Parnas's criterion** — decompose by what is likely to change — and **name a decision in `slot` that cannot be hidden**, and what follows from that.
7. Use **connascence** as an actionable scale: the nine forms, the two axes, and the rule that stronger connascence may span shorter distances.
8. Give the **real** statement of each SOLID letter, and rate it: S in the *one actor* form, O only against a demonstrated axis, **L as the only one with formal content**, I as weak in Python as stated, **D as the most valuable — for fast tests, not portability**.
9. **Apply the second-implementation test** to your own repository, and delete what fails it.
10. State DRY as being about **knowledge**, and apply the divergence test that separates real duplication from lookalikes.
11. Give **YAGNI's four costs**, and name five things it does **not** apply to because they cannot be retrofitted proportionally.
12. **Resolve two principles in conflict using evidence rather than imagination**, and say where the evidence lives.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L07 Coupling and Cohesion]] | Why the nine-four-line-functions fix fails; Constantine's two scales; **41% of file-touches as a measurement of cohesion**; stamp and content coupling, with `admin.py:271` breaking an invariant from outside; **Parnas (1972) and the decision that cannot be hidden**; connascence, nine forms with their standard weakenings; **what decoupling costs and when not to pay** |
| [[L08 SOLID One Letter at a Time]] | Each letter in its author's words, applied to code that exists: **five actors in one file**, the pricing `if` tree switched on in **four places with one missed for eight months**, `Equipment.book` violating Liskov in production, `notify.py` at **3.9% coverage** because its interface has five methods, and dependency inversion **valued for test speed rather than portability**; the scoreboard; **"duplication is far cheaper than the wrong abstraction"** |
| [[L09 DRY YAGNI and When Each Is Wrong]] | DRY as **knowledge, not code** — `range(8, 20)` in four places with three updated, against two lookalike validators whose 2022 merge caused a 2025 incident; the rule of three; **YAGNI's four costs and the plugin system with 31 commits and zero plugins**; **the five things YAGNI does not apply to**; separation of concerns made operational; **four principle conflicts you will actually hit** |
| [[CS212 Week2/assignments/QUIZ 2 Week 2 Tuesday\|QUIZ 2]] | Seven questions on Week 1, ten minutes, with its own answer key |
| [[CS212 Week2/assignments/A 2 Apply SOLID to a Provided Codebase\|A 2]] | **A pull request plus an argument.** Five questions, 100 points, due Friday of Week 3. **Two automatic caps** |
| [[CS212 Week2/resources/Reading Guide Week 2\|Reading Guide Week 2]] | **Parnas first — four pages, the best value on the course**; how to read Martin critically; and `git log` as evidence |
| `resources/pricing_before.py` | The open/closed case, extracted, so A 2 Q2 can start without a clone |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Week 2 is one idea with four names.**

Cohesion asks what belongs together. Single responsibility asks which actor asks for the change. Separation of concerns asks what changes for different reasons at different times. Parnas asks what is likely to change and demands you hide it. **These are four vocabularies for one question — *what changes together?* — and the reason there are four is that the field kept rediscovering it rather than that there are four things to know.**

**The question has an empirical answer and you are not it.** Your intuition about what will change is about as good as your intuition about which features will be used, which W0 L02 §5 says is roughly chance. **The evidence is in the `git log`**: `roomsvc`'s pricing abstraction is right in 2024 and would have been wrong in 2020, and nothing changed except six years of commits saying which axis moved.

**So the discipline is not "apply the principles". It is: find out what has actually been changing, and design for that.** Everything else is guessing with better vocabulary.

---

### Assessment Reminder

**Quizzes carry no weight. The project carries 40%.** Quiz *N* covers Week *N−1*, ten minutes at the start of **Tuesday's** lecture in Weeks 1–11, with its own key printed. Tracked in [[_CS 212 Quiz Record]].

**Assignments** are released Wednesday 17:00, due Friday 17:00 of the week after; **lowest of thirteen dropped.** A 1 is due this Friday; A 2 is released Wednesday.

> **A 2 is the first assignment marked as a pull request**, and it carries two automatic caps: a
> submission whose tests fail caps at 50, and one that is a single undescribed commit caps at 65.
> **Both are about reviewability, which is the property whose absence turned a fourteen-line fix
> into four months.**

---

### Connections

**Back:** **Week 1 left an invariant needing a home**, and this week explains why `confirm_booking` is not one — it serves five actors and reaches into five external systems. **W1 L06 §1's extension 6a** — the notification that must not roll back a booking — is now diagnosable as a separation-of-concerns failure, not an oversight.

**Sideways:** **CS 202's Week 2 is scheduling policy against mechanism**, which is L07 §5's Parnas criterion in a kernel: the mechanism is compiled in and the policy is a replaceable knob, because one was expected to change and the other was not. **PROG 202's higher-order functions** are dependency inversion with the ceremony removed — passing `notify` as a callable is the same move as injecting a `Notifier`, and Haskell makes it cheaper.

**Forward:** **Week 3 turns the three concerns into layers and makes you defend the boundaries** — and asks where an invariant lives, which is the question Weeks 1 and 2 have both deferred. **Week 4** names the patterns that resolve several of this week's conflicts, and shows which became language features. **Week 9** is this week applied to code that already exists, with Fowler's catalogue and a name for every smell. **Week 11** measures *change coupling* on your own project, which is L07 §7's heuristic made into a number.

---

*CS 212 · Week 2 · © CSE Department*
