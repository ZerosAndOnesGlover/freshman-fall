# CS 212 · Software Engineering
## Week 7 · Lecture 2 of 3
### A Checklist With Teeth

---

**Sat:** Wednesday of Week 7, 10:00–10:50, TH 200 · **Reading:** *Google Engineering Practices* — "The Standard of Code Review" and "What to Look For" · **Next:** L24, automated review
**A 7 is released after this lecture**, Wednesday 17:00.

---

## 1. The Standard: What Approval Means

Before the checklist, the question it serves. **Google's formulation is the best one available and it is one sentence:**

> **Approve when the change definitely improves the overall code health of the system, even if it is
> not perfect.**

**Three things follow, and all three are counter-intuitive:**

1. **"Better" beats "ideal".** A reviewer who blocks a change that improves things because it could improve them more is making the codebase worse, because the change does not land.
2. **There is no "perfect" to reach.** The standard is a direction, not a threshold.
3. **It is not "is this how I would have written it?"** If the author's approach is reasonable and yours is also reasonable, **the author's wins.** You may say you would have done it differently; you may not block on it.

**The one exception, and it matters:** **design is the place to push back hard.** A structural decision is expensive to reverse (W3 L10 §1), so a reviewer who lets a bad design through to avoid friction has deferred a cheap argument into an expensive one. **Pushing back on design, not on style, is what a good reviewer does.**

---

## 2. The Checklist, In Order

**The order is the content.** Reviewers left to themselves start at line 1 and comment on naming, because naming is easy to see. **By the time attention runs out — under an hour, L22 §4 — the design has not been looked at.**

### Pass 1 — Should this exist? *(2 minutes, and often ends the review)*

- [ ] **Is the problem it solves real, and stated?** If the PR description does not say why, ask before reading further
- [ ] **Is it the right size?** Over ~400 lines, ask for a split. **This is a kindness, not an obstruction** — the evidence says you will find nothing in it
- [ ] **Does it do one thing?** A refactoring mixed with a feature cannot be reviewed; each hides the other

### Pass 2 — Design *(the expensive half; spend the most time here)*

- [ ] **Does it fit the architecture we agreed?** Does the domain import infrastructure? *(If your architecture test runs in CI, this one is free — W3 L11 §1)*
- [ ] **Is the responsibility in the right place?** Is a rule leaking into a route handler, or persistence into the domain?
- [ ] **Does it duplicate knowledge, or duplicate code that looks alike?** W2 L09 §1's test, applied
- [ ] **Does it introduce an abstraction with one implementation?** Ask for the second case
- [ ] **Is anything expensive to reverse?** Schema, API shape, a dependency, a public interface. **If yes, ask for an ADR**

### Pass 3 — Correctness

- [ ] **The failure paths.** Every one. What happens when the database is down, the external call times out, the input is empty, the list has one element?
- [ ] **Concurrency.** Can two of these run at once? **If it reads then writes, say so out loud**
- [ ] **Invariants.** Can this code put the system into a state the domain model forbids?
- [ ] **Boundaries.** Empty, one, many, maximum, negative, zero, `None`
- [ ] **Time and timezones.** DST, midnight, month ends. *(Issue #31 is what happens when nobody asks — W6 L20 §4)*

### Pass 4 — Tests

- [ ] **Is there a test that fails without this change?** The single best question in the whole checklist
- [ ] **Do the tests assert the result, or the route?** `mock.assert_called_with` gets a comment
- [ ] **Are the failure paths tested, or only the happy one?**
- [ ] **Would the test still pass if the code were subtly wrong?** *(You can check: flip one comparison in your head)*

### Pass 5 — Readability and the small stuff

- [ ] Names say what the thing is
- [ ] The PR description will make sense in two years
- [ ] Comments explain **why**, not what
- [ ] No debug output, no commented-out code, no stray `TODO` without an issue number

> **Two rules about pass 5.** First, **do it last** — every minute spent on naming in pass 5 is a
> minute not spent on pass 2, and one of those is expensive to reverse. Second, **most of pass 5
> should not be a human's job at all**, and L24 is about moving it to a machine.

---

## 3. The Four Things Never to Comment On

Each of these wastes review capacity and — worse — teaches people that reviews are about trivia.

| Never | Why | Instead |
|---|---|---|
| **Formatting** | A machine does it better and without argument | `ruff format` / `black`, enforced in CI. **The argument is settled once, in a config file** |
| **Anything a linter catches** | Unused imports, shadowed names, mutable defaults | `ruff`, in CI |
| **Style preferences with no rationale** | *"I'd use a comprehension here"* costs the author time and buys nothing | Say nothing. If you genuinely believe it is clearer, say it once, prefixed **nit:**, and approve anyway |
| **The person** | *"You always forget this"* | Comment on the code. **§4** |

**The general rule: if a rule can be checked by a machine, a human must not check it.** Not because humans are bad at it — because human attention is the scarce resource in review, and every unit spent on an import order is a unit not spent on the concurrency question.

**This is how you make review cheap enough to happen.** A team that automates passes 5 and most of 4 can review a 24-line change in ten minutes, which means reviews happen the same day, which means changes are small, which is the whole virtuous cycle.

---

## 4. How to Write a Comment

Review is the only part of this course that is mostly about writing to another person. **Five rules, and they are not manners — they change outcomes.**

### 1. Ask, do not assert

> ❌ *"This is wrong, it'll break under concurrency."*
> ✅ *"What happens if two requests hit this at the same time? I think the read and the write can interleave here — am I reading it right?"*

**The question form is better even when you are certain**, for two reasons: you are sometimes wrong, and the author knows things you do not; and **a question invites reasoning while an assertion invites defence.**

### 2. Label the severity

The single highest-value convention in review, and it costs four characters:

| Prefix | Meaning |
|---|---|
| **`blocking:`** | I will not approve until this changes |
| **`question:`** | I do not understand; explain and I may approve unchanged |
| **`nit:`** | Take it or leave it. **I approve either way** |
| **`praise:`** | This is good. Say so |

**Without the labels, every comment reads as blocking**, and a review with fifteen unlabelled comments feels like a rejection even if fourteen are nits. **With them, an author can triage in thirty seconds.**

### 3. Explain why, once

*"Extract this"* → *"This is the third place that computes the slot grid; when the library extended to 21:00 last year, one of the three was missed. Worth extracting?"*

**The second version teaches something. The first is an instruction.**

### 4. Praise deliberately

**Not politeness — calibration.** A review stream that is 100% criticism gives an author no signal about what to do more of, and it makes review feel like an ordeal. **One `praise:` per review, on something specific.**

### 5. Talk, when the thread gets long

**Three round trips on one comment means the medium is wrong.** Go and talk to them, then post the outcome as a comment so the decision is on the record. **This one rule removes most of the interpersonal cost of review.**

---

## 5. Being Reviewed

Half the skill, and nobody teaches it.

- **Make the change small.** You control this, and it is the largest determinant of the review you get.
- **Write the description.** What, why, what to look at first, **and what you are unsure about.** The last item is the highest-value sentence in a PR and it is worth marks in every assignment in this course.
- **Review your own diff before you request a review.** You will find things. **Cisco's data says self-annotation before review finds real defects.**
- **Separate the mechanical commits.** A formatter run is its own commit, or the diff is unreadable.
- **Respond to everything**, even if only with `done` or `disagreed, because…`. **An unanswered comment is a reviewer who will not bother next time.**
- **Disagree when you disagree.** A reviewer is not automatically right and the standard is *"is it reasonable?"*, not *"is it what the reviewer would have written?"* **State your reason and ask them to decide.**

---

## 6. What to Do When the Review Is Hard

Three cases that your team will hit before May.

**"This should be rewritten."** Do not say it in a review. **A review is the wrong medium for a design disagreement that large**, and saying it after someone has written 400 lines is the worst possible timing. Talk; if the design was not discussed before the work, **that is a process failure and the retrospective should say so.**

**"I don't understand any of this."** This is a finding, not a gap in you. *"I have read this twice and I cannot follow the flow — can you walk me through it, and can we put that explanation in the code?"* **Incomprehensibility to a competent colleague is a defect** in exactly the sense W0 L01 §6 means.

**"They keep making the same mistake."** Review is the wrong tool for a recurring problem. **Anything that recurs belongs in the Definition of Done, the linter or the CI pipeline** — which is Week 8. Fixing it once in a config file beats mentioning it eleven times, and it removes the interpersonal dimension entirely.

---

## 7. Summary

- **The standard is: approve when the change definitely improves code health, even if imperfect.** Not "ideal", and **not "how I would have written it"** — but **push back hard on design**, because that is what is expensive to reverse.
- **The checklist's order is its content**: should this exist → **design** → correctness → tests → readability. Reviewers left alone start at line 1 and never reach design, because attention runs out in under an hour.
- **The single best question in the checklist: is there a test that fails without this change?**
- **Never comment on formatting, anything a linter catches, unjustified style preferences, or the person.** **If a machine can check it, a human must not** — attention is the scarce resource.
- **Five rules for comments:** ask rather than assert; **label severity — `blocking:` / `question:` / `nit:` / `praise:`**, which costs four characters and stops fourteen nits reading as a rejection; explain why once; praise deliberately; **talk after three round trips.**
- **Being reviewed is half the skill**: small changes, a description that says what you are unsure about, **self-review first**, respond to everything, and **disagree when you disagree.**
- **Three hard cases:** "rewrite this" is a process failure, not a review comment; **"I don't understand this" is a finding**; and **anything recurring belongs in CI, not in a comment.**

**Next:** L24 — automated review. What `ruff`, `mypy` and the scanners can and cannot do, and how to stop a human checking what a machine already checked.

---

*CS 212 · Week 7 · L23 · © CSE Department*
