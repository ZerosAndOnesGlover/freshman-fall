# CS 212 · Code Review Checklist
## Print this. Use it for A 7, and keep using it.

---

> **The order is the content.** A reviewer who starts at line 1 comments on naming — because naming is
> easy to see — and runs out of attention before reaching the design. **Attention is exhausted in
> under an hour** (L22 §4), and the design is the expensive-to-reverse half.

**The standard for approval:** *the change definitely improves the overall code health of the system,
even if it is not perfect.* **Not "ideal". Not "how I would have written it."**

---

## Pass 1 — Should this exist? *(2 minutes; often ends the review)*

- [ ] The PR description says **why**. If not, ask before reading further
- [ ] **Size.** Over ~400 lines → ask for a split. This is a kindness: the evidence says you will find nothing in it
- [ ] **One thing.** A refactoring mixed with a feature cannot be reviewed; each hides the other

## Pass 2 — Design *(spend the most time here)*

- [ ] Fits the agreed architecture. Does the domain import infrastructure?
- [ ] **Responsibility in the right place** — a rule in a route handler, persistence in the domain?
- [ ] Duplicates **knowledge**, or duplicates code that merely looks alike? *(Would one change to the world require both to change, always, the same way?)*
- [ ] A new abstraction with **one** implementation? → **ask for the second case**
- [ ] **Anything expensive to reverse** — schema, API shape, a dependency, a public interface? → **ask for an ADR**

## Pass 3 — Correctness

- [ ] **Every failure path.** Database down, external call times out, input empty, list of one
- [ ] **Concurrency.** *Can two of these run at once?* **If it reads then writes, say so out loud**
- [ ] **Invariants.** Can this put the system in a state the domain model forbids?
- [ ] **Boundaries.** Empty, one, many, maximum, negative, zero, `None`
- [ ] **Time.** DST, midnight, month ends, timezones

## Pass 4 — Tests

- [ ] **Is there a test that fails without this change?** ← *the single best question here*
- [ ] Do the tests assert the **result** or the **route**? `mock.assert_called_with` gets a comment
- [ ] Are the **failure paths** tested, or only the happy one?
- [ ] Would the test still pass if the code were subtly wrong? *(flip one comparison in your head)*

## Pass 5 — Readability *(last, and mostly a machine's job)*

- [ ] Names say what the thing is
- [ ] The description will make sense in two years
- [ ] Comments explain **why**, not what
- [ ] No debug output, no commented-out code, no `TODO` without an issue number

---

## Never comment on

| | Instead |
|---|---|
| **Formatting** | `ruff format` in CI. The argument is settled once, in a config file |
| **Anything a linter catches** | `ruff check` in CI |
| **Style preferences with no rationale** | Say nothing — or once, prefixed `nit:`, and **approve anyway** |
| **The person** | Comment on the code |

**If a machine can check it, a human must not.** Attention is the scarce resource.

---

## Labels — four characters, and the whole week turns on them

| Prefix | Meaning |
|---|---|
| **`blocking:`** | I will not approve until this changes |
| **`question:`** | I do not understand; explain and I may approve unchanged |
| **`nit:`** | Take it or leave it — **I approve either way** |
| **`praise:`** | This is good, specifically |

**Without labels every comment reads as blocking**, and fifteen comments feel like a rejection even
if fourteen are nits. **With them an author triages in thirty seconds.**

---

## Writing the comment

1. **Ask, do not assert** — even when you are certain. A question invites reasoning; an assertion invites defence
2. **Label the severity**
3. **Explain why, once.** *"Extract this"* teaches nothing
4. **One `praise:` per review**, on something specific. Not politeness — calibration
5. **After three round trips on one thread, go and talk**, then post the outcome

---

## When you are the author

- [ ] **Make it small.** You control this, and it determines the review you get
- [ ] Description: what, why, **what to look at first, and what you are unsure about**
- [ ] **Review your own diff first.** You will find things
- [ ] Formatter runs are their own commit
- [ ] **Respond to everything**, even `done`
- [ ] **Disagree when you disagree**, with a reason

---

## Three hard cases

| Situation | What to do |
|---|---|
| *"This should be rewritten"* | **Not a review comment.** Talk. If the design was never discussed before the work, that is a process failure and the retro should say so |
| *"I don't understand any of this"* | **A finding, not a gap in you.** Ask for a walkthrough, and ask for the explanation to go in the code |
| *"They keep making the same mistake"* | **Review is the wrong tool.** It belongs in the Definition of Done, the linter or CI. Fixing it once in a config file beats mentioning it eleven times |

---

*CS 212 · Week 7 · review checklist · print and keep*
