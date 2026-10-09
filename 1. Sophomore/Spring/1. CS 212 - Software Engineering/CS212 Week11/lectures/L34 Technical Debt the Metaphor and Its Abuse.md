# CS 212 · Software Engineering
## Week 11 · Lecture 1 of 3
### Technical Debt — the Metaphor, and Its Abuse

*“Shipping first time code is like going into debt. A little debt speeds development so long as it is paid back promptly with a rewrite.”* — Ward Cunningham, "The WyCash Portfolio Management System", OOPSLA (1992)

---

**Sat:** Tuesday of Week 11, 10:00–10:50, TH 200 · **⚠️ Quiz 11 in the first ten minutes** — covers Week 10. **This is the last quiz.** · **Reading:** Cunningham (1992); Fowler, *"TechnicalDebtQuadrant"* · **Next:** L35, metrics

**Coursework:** 📊 **Quiz 11** today · 📝 **Assignment 11** released Wed this week 17:00, due Fri of Week 12 17:00 · 📝 **Assignment 10** due Fri this week 17:00

---

## 1. What Cunningham Actually Said

**Ward Cunningham, OOPSLA 1992**, in a report about a financial system written in Smalltalk. The passage is short and it is nothing like what the phrase now means:

> *"Shipping first-time code is like going into debt. A little debt speeds development so long as it
> is paid back promptly with a rewrite… The danger occurs when the debt is not repaid. Every minute
> spent on not-quite-right code counts as interest on that debt."*

**Three things in that passage are routinely lost:**

1. **The debt is taken on *deliberately*, to ship sooner.** It is a financing decision, not an accident.
2. **The thing owed is *understanding*.** Cunningham's later clarification is explicit: the debt is that **the code does not yet reflect what you now know about the domain.** It is not "bad code".
3. **The interest is real and continuous** — every minute spent working around the not-quite-right code.

**Cunningham himself, in 2009, on what the phrase became:**

> *"I'm never in favour of writing code poorly, but I am in favour of writing code to reflect your
> current understanding of a problem even if that understanding is partial."*

> **So the original metaphor describes a *good* practice done deliberately.** What the industry now
> calls technical debt is mostly **just mess** — and calling mess "debt" is how it gets excused, because
> debt sounds like a decision.

---

## 2. Fowler's Quadrant, Which Fixes the Confusion

**The single most useful tool for talking about this**, because it separates two axes people conflate.

|  | **Reckless** | **Prudent** |
|---|---|---|
| **Deliberate** | *"We don't have time for design"* | *"We must ship now and deal with the consequences"* |
| **Inadvertent** | *"What's layering?"* | *"Now we know how we should have done it"* |

**Read the quadrants in order of how you should respond:**

- **Prudent/deliberate** — **this is Cunningham's.** A recorded decision with a known cost. **Legitimate, and it needs a register entry and a date.**
- **Prudent/inadvertent** — **the most common and the most honest.** You could not have known in Week 1 what you know in Week 9. **`slot`'s domain model was wrong and you found out; that is not a failure, it is how the work goes.**
- **Reckless/inadvertent** — **an education problem, not a debt problem.** The answer is review and pairing, not a register entry.
- **Reckless/deliberate** — **not debt.** It is choosing to make a mess while knowing better, and dignifying it with a financial metaphor is the abuse the word suffers.

**The practical use, and A 11 requires it:** **put every item in your debt register in a quadrant.** The quadrant determines what you do — prudent/deliberate items get a repayment date, prudent/inadvertent items get prioritised by interest, reckless/inadvertent items get a review-practice change, and reckless/deliberate items should not have happened.

---

## 3. Interest Is the Only Thing That Matters

**The principal — how bad the code is — is almost irrelevant. What matters is the interest: how much it costs you, per unit time, to work around it.**

**Which means a piece of terrible code that nobody touches costs nothing.**

| `roomsvc` module | How bad | Touches / 2 years | Verdict |
|---|---|---|---|
| `bookings.py` | complexity 94, 31.8% branch coverage | **891** | **Crippling.** Maximum interest |
| `calendar_sync.py` | 19.4% coverage, message chains | 46 | Moderate |
| `roomsvc/legacy_import.py` | genuinely awful, 400 lines, no tests | **2** | **Costs essentially nothing.** Leave it |

**`legacy_import.py` is the important row.** It is worse code than `calendar_sync.py` by every static measure, and **paying it down would be a waste of a day**, because the loan is not accruing.

> **The rule that follows, and it is the whole of prioritisation:**
> **Interest = (how bad) × (how often you touch it).** The second factor is in your `git log`, it
> requires no judgement, and **most teams optimise the first factor because it is the one they can
> see by reading.**

**This is why L35's hotspot analysis is the useful metric and cyclomatic complexity alone is not.**

---

## 4. The Register

**A debt item that is not written down is not debt — it is a feeling.** The register is one markdown file in the repository, and Phase 1's rubric and the final report both ask for it.

```markdown
## D-07 · Holds never expire

**Quadrant:** prudent / deliberate
**Recorded:** 2026-03-18 · **Owner:** the release manager of the fortnight

**What:** `state='HELD'` rows are ignored after 15 minutes by a `WHERE` clause
in three queries, but nothing deletes or expires them. The rule lives in query
predicates rather than in the data.

**Why we took it on:** the expiry job needs a scheduler we did not have in
Week 4, and the query predicate was twenty minutes' work.

**Interest:** every new query that touches bookings must remember the predicate.
Three queries today; we have added one since February. One person has already
forgotten it once (PR #61, caught in review).

**Trigger to repay:** when a fourth query needs it, OR when we add the
background worker for notifications — whichever comes first.

**Estimated repayment:** half a day.
**Issue:** #44
```

**Six fields, and each earns its place:**

| Field | Why |
|---|---|
| **Quadrant** | Determines the response (§2) |
| **What** | Specific enough that somebody else can find it |
| **Why we took it on** | **Without this, a later reader assumes incompetence** — and this is what distinguishes debt from mess |
| **Interest** | **The prioritisation input.** With evidence, not adjectives |
| **Trigger to repay** | **A condition, not a date.** §5 |
| **Estimated repayment** | So the trade is arithmetic |

---

## 5. A Trigger Beats a Date

**"We'll fix it in Q3" does not survive contact with Q3.** A *condition* does, because it fires when the cost is actually being paid:

| Bad | Good |
|---|---|
| *"Fix by April"* | *"When a fourth query needs the predicate"* |
| *"Refactor soon"* | *"When we next add a booking kind"* |
| *"Improve coverage"* | *"When a mutant survives in this module again"* |
| *"Add the scheduler"* | *"When anything else needs a background job"* |

**Why triggers work, mechanically:** a date is a promise about *the future*, made by someone who cannot see their future workload. **A trigger is a rule about *the present*, and when it fires the cost of the debt is being paid right then** — which is exactly the moment when repaying it is cheapest and the argument for it is strongest.

**This is also W9's preparatory refactoring** in another form: *make the change easy, then make the easy change*. **The trigger fires when you are already in that code.**

---

## 6. When Not to Repay

**Four cases, and a team that cannot name them will waste its last fortnight.**

| Case | |
|---|---|
| **The code is not touched** | §3's `legacy_import.py`. Zero interest, zero urgency |
| **The component is being replaced** | Do not refactor what you are about to delete. `roomsvc` is being replaced by `slot`; **fixing `roomsvc`'s plugin system would be absurd** |
| **The repayment is riskier than the debt** | `confirm_booking` with eleven tests: **you cannot safely restructure it until you can pin it** (W9 L28 §2). Repay the *test* debt first |
| **You are about to ship** | **The last fortnight of a project is the worst time to repay debt.** Record it and hand it over |

**The fourth is the one that applies to you right now.** Week 11 of 13. **Your final demo is on 28 April and your report is due 1 May.** A team that spends the last fortnight refactoring will arrive with a cleaner codebase and fewer working features, **and the report marks honesty about debt far more than its absence.**

> **The report asks: "what do you know is wrong, and why did you leave it?"** A team with a
> well-reasoned register of eight items scores **above** a team claiming no debt — because the second
> team either has not looked or is not saying.

---

## 7. Debt You Cannot See From the Code

**The register should not be only about code**, and these are the entries teams never think to make.

| Kind | `slot` example |
|---|---|
| **Test debt** | A suite that passes and would not notice a regression. **Your mutation score is the measurement** (W6) |
| **Documentation debt** | The undocumented invariant. **`roomsvc`'s `slot.is_provisional` check, whose reason left in 2023** |
| **API debt** | A field you cannot remove because you do not know who uses it (**W10 L33 §1 — seventeen of them**) |
| **Process debt** | A deployment nobody but one person can perform. **A bus factor of 1 is debt** |
| **Dependency debt** | Three major versions behind, so the upgrade is now a project rather than a chore |
| **Data debt** | A column that means two things; rows from 2021 in a state the code no longer produces |
| **Knowledge debt** | **One person understands the migration strategy.** `roomsvc`'s is 78% of `bookings.py` written by someone who left |

**Dependency debt has a property worth naming: it accrues whether or not you touch the code.** Everything else on this list is dormant until you go near it. **A dependency three versions behind gets worse while you sleep**, and the upgrade cost grows super-linearly — which is why `pip-audit` sits in the nightly sweep (W8 L25 §5) and why that is a deliberate choice rather than a filler.

---

## 8. Summary

- **Cunningham's 1992 metaphor describes a deliberate financing decision**, where the thing owed is **understanding** — code that does not yet reflect what you have learned. **What the industry calls technical debt is mostly mess**, and the word is how mess gets excused.
- **Fowler's quadrant separates deliberate from inadvertent and reckless from prudent.** Prudent/deliberate is Cunningham's and needs a register entry; **prudent/inadvertent is the most common and the most honest**; reckless/inadvertent is an education problem; **reckless/deliberate is not debt at all.**
- **Interest, not principal, is what matters** — and **interest = badness × touch frequency**, the second factor being in your `git log` and requiring no judgement. **Terrible code nobody touches costs nothing**: `legacy_import.py` is worse than `calendar_sync.py` and not worth a day.
- **A register entry needs six fields**, and *"why we took it on"* is what distinguishes debt from mess, while *"interest"* is what lets you prioritise.
- **A trigger beats a date**, because a trigger fires when the cost is actually being paid — which is when repayment is cheapest and the argument is strongest. **It is W9's preparatory refactoring in another form.**
- **Four times not to repay**: untouched code, a component being replaced, a repayment riskier than the debt, **and the last fortnight of a project** — which is now.
- **Debt is not only code**: test, documentation, API, process, dependency, data and knowledge debt all belong on the register, **and dependency debt is the one that accrues while you sleep.**

**Next:** L35 — the metrics. Which ones mislead, which ones help, and the one analysis that is worth more than all the static measures put together.

---

*CS 212 · Week 11 · L34 · © CSE Department*
