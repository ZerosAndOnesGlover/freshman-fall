# CS 212 · Software Engineering
## Week 12 · Lecture 2 of 3
### Engineering Management

---

**Sat:** Wednesday of Week 12, 10:00–10:50, TH 200 · **Reading:** *Accelerate*, Ch. 2 and 11; Rozovsky on Project Aristotle · **Next:** L39, career paths
**A 12 is released after this lecture**, Wednesday 17:00. **A 11 and A 12 are both due Friday 24 April.**

---

## 1. Brooks, Measured

W0 L01 §2 gave you the slogan — *adding manpower to a late software project makes it later* — and the mechanism: **communication paths grow as $n(n-1)/2$.**

**Your own term is the demonstration.** Four people is 6 pairs; five is 10. **Going from four to five adds 25% more labour and 67% more pairs who must stay in agreement**, and every team that grew mid-term discovered the second number.

**What the evidence adds to the slogan:**

| Finding | Source |
|---|---|
| **The optimum team size for software is small** — commonly cited as 5–9, and smaller for tightly-coupled work | Consistent across studies; effect sizes vary widely |
| **Adding people to a late project costs *more* than nothing**, because existing members stop producing to onboard them | Brooks (1975); replicated in practice, never in a controlled trial |
| **The best predictor of a team's performance is not its members' individual ability** | Google's **Project Aristotle** (2015) — §2 |

**And the finding that survives best, because it is mechanical rather than psychological: batch size.** You have met it three times — **review size** (W7), **TDD's small steps** (W5), **deployment frequency** (W8). **Three literatures, one mechanism**, and it is the most robust result in this course.

---

## 2. What Actually Predicts Team Performance

**Google's Project Aristotle** studied 180 of its own teams, looking for what distinguished the effective ones. **The individual ability of the members did not predict it.** Nor did tenure, seniority, colocation or personality mix.

**What did, in descending order:**

| Factor | |
|---|---|
| **1. Psychological safety** | **By a wide margin the strongest.** Can a member say *"I don't understand this"* or *"I think this is wrong"* without cost? |
| 2. Dependability | Work gets done when it was said it would |
| 3. Structure and clarity | Clear goals, roles and plans |
| 4. Meaning | The work matters to the individual |
| 5. Impact | The work matters to somebody else |

**Two honest caveats.** It is one organisation, self-reported, and the construct — psychological safety, from Amy Edmondson's 1999 work — is measured by survey. **And the direction of causation is not established**: safe teams may perform well, or performing well may make a team feel safe.

**What makes it worth taking seriously anyway is that the mechanism is visible and testable in your own team**, and it is exactly the thing this course has been optimising without naming:

> **Psychological safety is what makes a code review possible.** A reviewer who cannot say *"I have
> read this twice and cannot follow it"* will approve it. An author who cannot say *"I do not know if
> this is right"* will not write it in the description — **which is why A 2 through A 10 each awarded
> marks for that sentence.** Thirteen weeks of asking for *"what you are unsure about"* was this
> finding, applied.

**And it is why W7 L23 §4's severity labels matter more than they look.** Four characters — `nit:` — that remove the implication that a comment is an accusation. **The convention exists to make the safety cheap.**

---

## 3. Estimation, and Why It Fails

**You were sceptical about story points in Week 0. Here is why it is worse than that.**

**The reference-class problem.** Estimating a task by imagining it takes you through the steps you can foresee, and **the variance is entirely in the steps you cannot.** So estimates are systematically optimistic, and the error is not symmetric: a task can take ten times as long and cannot take a tenth.

| Phenomenon | |
|---|---|
| **The planning fallacy** | Kahneman & Tversky. **People estimate from the best-case path even when they have historical data showing they should not** |
| **Overrun distributions are long-tailed** | Which is why the *average* overrun is much larger than the *median*, and why an average is the wrong summary |
| **Estimates become commitments** | The moment a number is repeated to someone else, it stops being a forecast |

**What works better, in order of how much better:**

1. **Make the thing small enough that the estimate does not matter.** A two-day task does not need an estimate; it needs starting. **This is the only reliable answer** and it is W5 and W7's batch-size mechanism again.
2. **Count, do not estimate.** *"We finished 9, 11 and 8 cards in the last three fortnights"* forecasts better than adding up points, and it cannot be inflated by redefinition.
3. **Measure cycle time and give a range.** *"Cards take 2–6 days at the 80th percentile"* is honest and actionable. **A single-point estimate is a claim about a distribution, stated as a fact.**
4. **Forecast probabilistically if you must forecast.** A Monte Carlo over historical cycle times beats expert judgement in most published comparisons — and you already have the data in your board.

> **The professional skill is not estimating accurately. It is communicating uncertainty without
> being useless.** *"I don't know"* is useless; *"two to six days, and here is what would make it
> six"* is not. **A 12 asks for your team's actual cycle-time range**, which is the cheapest version
> of this you can practise.

---

## 4. Incidents, and Blameless Post-Mortems

**The most transferable management practice in this lecture, and it is procedural rather than cultural.**

**The rule:** a post-mortem asks *what about the system allowed this?* — never *who did this?*

**Not because blame is unkind. Because blame destroys the information.** If naming a cause costs somebody, the cause stops being named, and **you lose the only data you had.** Knight Capital's alerts fired at 08:01 and nobody acted; **the interesting question is what made those alerts ignorable**, and you will never learn it in a meeting where somebody is at fault for ignoring them.

**A post-mortem that works has five sections**, and the fourth is where it usually fails:

| | |
|---|---|
| **Timeline** | What happened, in order, with times. **Facts only** |
| **Impact** | Who was affected, how, for how long |
| **Contributing factors** | *Plural.* **There is never one cause** — Knight Capital had five |
| **What made it hard to detect or fix** | ← **the section that produces the valuable actions** |
| **Actions** | Each with an owner and a date. **Actions that are not scheduled work do not happen** (W10 L33 §5) |

**Human error is not a contributing factor; it is a symptom of one.** *"The engineer deployed to seven of eight servers"* is not a root cause — **"deployment was manual and unverified"** is, and only the second has an action attached.

> **And the sentence worth carrying into your career:** **the question is never "who broke it?" but
> "what allowed one person's ordinary mistake to break it?"** Every failure in this course's canon —
> Therac-25, Ariane 5, Knight Capital, the 737 MAX — was a competent person inside a system that gave
> their mistake too much leverage.

---

## 5. Which of This Course's Practices Survive an Organisation

**You will arrive somewhere that does some of this and not the rest. Rank your battles.**

| Practice | Adoptability | Why |
|---|---|---|
| **Small changes** | **Easy, unilateral** | You can do it today, alone, and the effects are visible |
| **Tests for what you change** | **Easy, unilateral** | Nobody stops you |
| **Writing down decisions** | **Easy** | An ADR in a repository needs no permission |
| **Characterisation tests before refactoring** | **Easy** | Purely personal discipline |
| Review that reaches design | **Medium** | Needs one other person to agree |
| A fast pipeline | **Medium** | Usually a resourcing argument, and **DORA's data is the argument** |
| **Trunk-based development** | **Hard** | Requires the team to change |
| **Deleting things** | **Hard** | Requires organisational permission and confidence |
| **Not setting a coverage target** | **Very hard** | Somebody's dashboard depends on it |

**Note the pattern: everything in the top half is something you can do alone**, and most of the value of this course is in the top half. **Do not wait for a mandate to write a test.**

**And on the bottom half**, the professional advice is to **bring evidence rather than principles.** *"We should not have a coverage target"* loses; *"our coverage is 82% and our mutation score is 34%, so the target is not measuring what we think"* wins, sometimes. **W6's two papers exist for this conversation.**

---

## 6. Should You Become a Manager?

**Briefly, because it is the question the next lecture is really about.**

**Management is a different job, not a promotion.** The skills barely overlap: your output stops being code and becomes other people's effectiveness, and **your feedback loop lengthens from minutes to months** — which, after a term of arguing that short feedback loops are the whole of engineering progress, should tell you what the difficulty is.

**Two things worth knowing now:**

1. **The move is usually reversible early and usually not later.** Two years of management erodes hands-on skill; five years makes returning genuinely hard. **Most people who intend to try it for a year do not go back.**
2. **A good engineer is not automatically a good manager, and the failure mode is specific:** continuing to do the engineering, because it is what you are good at and the feedback is immediate. **The team then has no manager and one frustrated senior engineer.**

**The alternative is real.** The **staff/principal engineer** track exists at most serious employers precisely because organisations need technical judgement at the same level as managerial judgement. **L39 is about that choice.**

---

## 7. Summary

- **Brooks's $n(n-1)/2$**: four people is 6 pairs, five is 10 — **25% more labour, 67% more pairs**. Adding people to a late project costs more than nothing.
- **The most robust result in this course is batch size**, arriving from three separate literatures — review size, TDD's small steps, deployment frequency.
- **Project Aristotle: individual ability did not predict team performance. Psychological safety did, by a wide margin** — one organisation, self-reported, causation unestablished. **And it is what makes code review possible**, which is why thirteen weeks of assignments asked for *"what you are unsure about"*, and why **severity labels make the safety cheap.**
- **Estimation fails structurally**: the variance is in the steps you cannot foresee, overruns are long-tailed, and an estimate becomes a commitment when repeated. **Make things small, count rather than estimate, give cycle-time ranges, forecast probabilistically.** **The skill is communicating uncertainty without being useless.**
- **A blameless post-mortem protects the information, not the feelings.** Five sections, and *"what made it hard to detect or fix"* produces the valuable actions. **Human error is a symptom, not a cause** — *"deployment was manual and unverified"* is the cause, and only it has an action.
- **The question is never "who broke it?" but "what allowed one person's ordinary mistake to break it?"**
- **Everything in the top half of §5's table is unilateral.** Do not wait for a mandate to write a test. **For the bottom half, bring evidence rather than principles.**
- **Management is a different job with a much longer feedback loop**, usually reversible early and rarely later — and the **staff engineer track exists because organisations need technical judgement too.**

**Next:** L39 — career paths, what this course was actually for, and the four things worth taking from it.

---

*CS 212 · Week 12 · L38 · © CSE Department*
