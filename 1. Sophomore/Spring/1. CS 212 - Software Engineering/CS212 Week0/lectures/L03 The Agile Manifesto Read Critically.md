# CS 212 · Software Engineering
## Week 0 · Lecture 3 of 3
### The Agile Manifesto, Read Critically

*“The business changes. The technology changes. The team changes. The team members change. The problem isn't change, per se, because change is going to happen; the problem, rather, is the inability to cope with change when it comes.”* — Kent Beck, *Extreme Programming Explained* (2000)

---

**Sat:** second Tuesday of Week 0, 10:00–10:50, TH 200 · **Reading:** agilemanifesto.org (both pages — it takes four minutes) · **Next:** Week 1, requirements

**Coursework:** 📝 **Assignment 0** released Wed this week 17:00, due Fri of Week 1 17:00 · 📋 **Team formation workshop** Thu this week 10:00–10:50
**A 0 is released after this lecture**, Wednesday 17:00.

---

## 1. The Document, In Full

**11–13 February 2001. Snowbird ski resort, Utah. Seventeen people**, all men, all consultants or practitioners from lightweight-methodology communities — Extreme Programming, Scrum, DSDM, Crystal, Feature-Driven Development, Pragmatic Programming, Adaptive Software Development. They had no agenda beyond finding common ground. They produced **68 words**:

> **Manifesto for Agile Software Development**
>
> We are uncovering better ways of developing software by doing it and helping others do it.
> Through this work we have come to value:
>
> - **Individuals and interactions** over processes and tools
> - **Working software** over comprehensive documentation
> - **Customer collaboration** over contract negotiation
> - **Responding to change** over following a plan
>
> That is, while there is value in the items on the right, we value the items on the left more.

**The last sentence is the most-skipped sentence in the industry.** It says the right-hand items have value. Every misuse of this document in the next twenty-five years consists of deleting that sentence.

There are also **twelve principles** on the second page, which almost nobody quotes and which are considerably more specific. Several are genuinely demanding — *"Deliver working software frequently, from a couple of weeks to a couple of months"*, *"Business people and developers must work together daily"*, *"Continuous attention to technical excellence and good design enhances agility"*. **A 0 requires you to read them.**

---

## 2. Each Line Is a Trade-Off, and Each Has a Failure Mode

Read as absolutes, all four are wrong. Read as trade-offs with a stated context, all four are defensible. Here is each one with the context it needs and the way it actually fails.

### "Individuals and interactions over processes and tools"

**What it was reacting to:** 1990s heavyweight methodologies in which a process defined roles so tightly that competent people could not act. The prescription came before the problem.

**Where it is right:** a good team with a bad process outperforms a bad team with a good process, reliably.

**How it fails:** it becomes an argument against *any* process, including ones that exist because a human will otherwise forget. **Knight Capital lost $440M because a deployment was done by a person rather than a tool**, and the person missed the eighth server. *"Individuals over processes"* is precisely the wrong instruction for deployment.

> **The rule that survives contact:** the more a task punishes a lapse of attention, the more it
> belongs to a tool. **Design needs individuals. Deployment needs a robot.** Week 8.

### "Working software over comprehensive documentation"

**What it was reacting to:** deliverable documents that existed to satisfy a contract, were written before the code, contradicted it within a month, and were never read.

**Where it is right:** a 200-page design document describing a system nobody has built is a work of fiction, and its page count is not evidence.

**How it fails:** `roomsvc`. Four of its six authors have left. **Nobody can say why `confirm_booking` checks `slot.is_provisional` twice**, because the reason lived in someone's head and the head left in 2023. The undocumented invariant is exactly what Week 11 has to reconstruct, expensively.

**Note the adjective.** The line does not say *over documentation*. It says over **comprehensive** documentation. The manifesto's own authors documented heavily — Beck's book, Cockburn's books, the Scrum Guide. **Week 11 is about documentation that survives, which is mostly documentation that lives next to the code and is checked by a machine.**

### "Customer collaboration over contract negotiation"

**What it was reacting to:** fixed-price, fixed-scope contracts in which both sides spend the project arguing about whether a change is in scope, and the software is a by-product of the argument.

**Where it is right:** when the customer is reachable and wants the software to be good, weekly conversation beats quarterly change-control.

**How it fails:** **there is often no single customer.** Who is `slot`'s customer — the registrar, the lecturer who books the room, the student who reads the timetable, or the facilities team who unlock the doors? Their interests conflict; the registrar wants control and the lecturer wants speed. *"Collaborate with the customer"* is not an instruction when there are four of them, and **Week 1 is largely about what to do when it is not.**

It also fails when the relationship is adversarial, when the money is public and must be accounted for, or when the supplier is genuinely trying to bill for the same work twice. **Contracts exist for a reason and the reason is not going away.**

### "Responding to change over following a plan"

**What it was reacting to:** plans treated as commitments to a guess made when least was known.

**Where it is right:** the plan encodes what you believed in January. In March you know more, and following the January plan is choosing to act on worse information.

**How it fails:** the two ways are opposite and both common.
- **No plan at all** — "we're agile" as a reason not to think past the sprint. Databases get migrated, security models get retrofitted, and someone has to decide about them before the sprint they bite in.
- **A plan that is changed so often it stops being information.** If the date moves every two weeks, nobody downstream can do anything with it, and the honest statement — *"we don't know"* — is more useful.

**Eisenhower's line is the correct reading, and the manifesto's authors quote it:** *"plans are worthless, but planning is indispensable."*

---

## 3. What the Authors Say Happened

Unusually for a founding document, several signatories have publicly repudiated what became of it.

- **Dave Thomas, 2014**, *"Agile is Dead (Long Live Agility)"*: "The word 'agile' has been subverted to the point where it is effectively meaningless… what passes for agile is often just a travesty." He proposes dropping the noun and keeping the adjective.
- **Andy Hunt, 2015**, *"The Failure of Agile"*: teams adopted the practices without the judgement, because practices are teachable and judgement is not. His term is **"Fragile"**.
- **Martin Fowler, 2018**, *"The State of Agile Software in 2018"*, on what he named the **Agile Industrial Complex**: processes imposed on teams by people who do not do the work, which contradicts the first line of the document being imposed.
- **Ron Jeffries, 2018**: *"Developers Should Abandon Agile"* — arguing that developers should keep the technical practices (testing, refactoring, small steps) and walk away from the branded processes entirely.

**The common diagnosis:** a document about **judgement** was turned into a **certification**. You can buy a two-day Scrum Master certificate; you cannot buy the ability to tell which of §2's four trade-offs applies to the argument in front of you.

> **This is not a reason to dismiss agility.** It is a reason to be specific. *"We should be more
> agile"* is not an engineering proposal. *"We should cut our release cycle from six weeks to one,
> which requires the integration test suite to run in under ten minutes, which it currently does
> not"* is.

---

## 4. Where Agile Genuinely Does Not Apply

Know these, because the strongest signal of understanding a method is naming its boundary.

| Context | Why short iterations fail | What is used instead |
|---|---|---|
| **Safety-critical, certified** — avionics, medical devices, nuclear | Certification evidence must be produced against a frozen specification. DO-178C requires bidirectional traceability from requirement to test | V-model with iterative development *inside* each phase |
| **Hardware-coupled** | You cannot iterate a fabricated silicon mask on a two-week cycle; the feedback loop is set by manufacturing | Long cycles, heavy simulation, formal methods |
| **Fixed-price public procurement** | The contract fixes scope before work starts, by law in many jurisdictions | Sequential, with change control — or restructure the procurement, which is the real fix |
| **Very large systems of systems** | Dozens of teams, hard interface contracts; per-team agility with no architectural control produces an unintegrable mess | Architecture-led development; scaled frameworks (SAFe, LeSS) with all their compromises |
| **Genuinely stable domains** | A payroll engine for a published tax code has requirements that arrive as legislation, not as discoveries | Sequential, and it is fine |

**And one context where it fails that nobody puts in the table: a team that cannot deploy.** If releasing takes three days of manual work, two-week sprints produce software that is *finished* every two weeks and *delivered* never. **The technical practices are the precondition, not the reward.** This is the single most common reason "agile transformations" produce nothing, and it is why Weeks 5–8 of this course exist before Week 12 talks about management.

---

## 5. What Is Left When You Strip the Branding

Take away Scrum's ceremonies and the certifications, and a defensible core remains. Every item below has evidence behind it (L02 §8) and none requires a consultant.

1. **Work in small increments.** Every increment is releasable, whether or not you release it.
2. **Integrate continuously.** Every push is built and tested by a machine you did not have to remember to ask.
3. **Automate the repetitive.** Build, test, lint, deploy. Humans do judgement; machines do vigilance.
4. **Get real feedback, from real users, early.** Not a review meeting — someone using it.
5. **Keep the code changeable.** Refactor continuously; changeability is a capability you spend and must replenish.
6. **Reflect and adjust the process** — the retrospective is the only part of Scrum that changes Scrum.

**That is this course's syllabus, in order.** Weeks 1–4 are (5) before the fact; Weeks 5–7 are (3) and (6); Week 8 is (2) and (3); Weeks 9–11 are (5) after the fact; Week 12 is (4) and (6).

---

## 6. How Your Project Actually Runs

Concrete, so nobody has to guess. Full detail in [[CS212 Week0/project/PROJECT BRIEF slot|PROJECT BRIEF slot]] and [[CS212 Week0/project/TEAM CHARTER template|TEAM CHARTER template]].

| | |
|---|---|
| **Teams** | 4–5, formed Thursday, fixed. Changes need the instructor and a reason |
| **Iterations** | Two weeks: W1–2, W3–4, **W5–6 (Phase 1)**, W7–8, W9–10, W11–12 |
| **Backlog** | GitHub Projects, one board per team, **ordered**, one person responsible for the order — rotate that role each iteration |
| **WIP limit** | You choose it in the charter, you record it, and **A 12 asks whether you kept it** |
| **Definition of Done** | You write it in the charter in Week 0 and it does not change. It must include: reviewed by a teammate, tests pass in CI, no `TODO` left in the diff |
| **Retrospective** | Fifteen minutes at the end of each iteration, **written up in `docs/retro-N.md` and committed.** Six files by the end of term; A 12 is built on them |
| **Evidence** | The git history. Commits spread through the term, small, with messages that say why |

> **The most common way this project fails, from every previous cohort:** four people work in
> parallel for ten weeks on four branches and integrate in the last fortnight. It does not
> integrate. **The counter-measure is in Week 1 and it is not negotiable: a walking skeleton — one
> booking, end to end, through every layer, deployed by CI — before any feature is built.**
> Thin and ugly is fine. It must be *whole*.

---

## 7. What to Take From Week 0

Three things, in the order they will matter to you.

1. **The discipline was named because software was failing, and the failures were mostly not coding errors.** Process, review, testing and deployment are where the famous disasters live.
2. **Every process innovation since 1968 shortens the feedback loop.** Judge any practice — including any this course teaches — by asking what it lets you find out, and how much sooner.
3. **The Agile Manifesto is four trade-offs, not four commandments**, and its final sentence says so. **An engineer's skill is knowing which side of a trade-off the situation is on**, and that is what A 0 is marked on.

**Next week: requirements.** Where the double-booking of VNC 101 turns out to have been a requirement nobody wrote down — and where you find out how hard it is to write down the ones you do know.

---

## 8. Summary

- **68 words, 17 people, Snowbird, February 2001**, and a closing sentence — *"there is value in the items on the right"* — which is the one people delete.
- **Each of the four lines is a trade-off with a real failure mode**: individuals-over-process is wrong for deployment; working-software-over-documentation is why nobody knows what `confirm_booking` does; customer-collaboration assumes a single customer and `slot` has four; responding-to-change fails both by having no plan and by having one that changes too often to inform anyone.
- **Four signatories have publicly repudiated what the word became** — Thomas, Hunt, Fowler, Jeffries — with one diagnosis: a document about judgement became a certification.
- **It genuinely does not apply** to certified safety-critical work, hardware-coupled cycles, fixed-price procurement, large systems-of-systems — **and to any team that cannot deploy**, which is the common case.
- **What survives the branding is six practices**, and they are this course in order.
- **Your project: 4–5 people, six two-week iterations, an ordered backlog, a written Definition of Done, six committed retrospectives, and a walking skeleton in Week 1.**

---

*CS 212 · Week 0 · L03 · © CSE Department*
