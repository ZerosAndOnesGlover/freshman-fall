# CS 212 · Assignment 0 — Solutions and Mark Scheme
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for A 0.** This is a reading-and-judgement paper and it is the only one of the
term with no code. **Mark the sourcing and the position-taking.** A student who reaches a conclusion
the lecture disagrees with, from sources they demonstrably read, gets full marks; a student who
agrees with everything and cites nothing does not.

**The one automatic failure** is a quotation that does not appear in the source. This is common with
Royce and with the Manifesto, and it is checkable in thirty seconds. Treat a fabricated quotation as
an integrity matter, not a marking one.

**Calibration from previous cohorts:** the median lands at 68–72. Q3(b) and Q4 are where the top
decile separates, and Q2(a) column 4 is where the bottom quartile collapses.

---

## Q1: Read the Primary Source (20)

### (a) [6]

**The sentence, Royce (1970) p. 329, beside Figure 2:**

> "I believe in this concept, but the implementation described above is risky and invites failure."

**What he recommends instead:** iterate. Specifically — do the program design before the requirements
are frozen; build a pilot version and throw it away ("do it twice"); document the design; plan and
control the testing rather than treating it as a final phase; and involve the customer formally at
several defined points.

| | |
|---|---|
| 3 | The exact sentence, with page number |
| 3 | The recommendation, in the student's own words, ≤ 4 sentences |

**Deduct 2** for a paraphrase presented as a quotation. **Deduct all 3** of the first part for
"Royce proposed the waterfall model" with no engagement with p. 329 — this is the misreading the
question exists to catch.

### (b) [8]

4 marks each for any two. Accept these mappings; accept others with a defended mechanism.

| Royce | Descendant | What the modern version adds |
|---|---|---|
| "Do it twice" | Prototype / walking skeleton / spike | Royce throws away one pilot **once**; modern practice iterates continuously, and the automated test suite is what makes the second, third and fortieth iteration cheap rather than only the second |
| "Involve the customer" | Sprint review; continuous delivery to real users | Royce's is **three scheduled reviews of documents**; modern practice puts working software in front of users, which surfaces behaviour rather than opinions (L02 §5) |
| "Document the design" | ADRs | ADRs record the **decision, the alternatives and the consequences**, are versioned with the code, and are immutable-plus-superseded rather than edited |
| "Plan, control, monitor testing" | Test strategy + CI | Automation: the plan runs on every push rather than being executed by people at the end |
| "Program design comes first" | Architecture spike; risk-first iteration (Boehm) | Made explicit as **risk reduction**, and time-boxed |

**Full marks require the "what it adds" column.** Naming the descendant alone is 2 of 4. The most
common thin answer is "do it twice = Agile", which earns 1.

### (c) [6]

**Both positions are creditable.** Mark the argument.

*Defending the misreading:* a procurement organisation buying from an external supplier needs
**auditable, contractible artefacts**. A phase gate with a signed deliverable is enforceable in a way
that "we iterate with the customer" is not; public money requires an account of what was bought;
and a fixed price cannot be quoted against an unfixed scope. **This is a real constraint, not
stupidity** — and DO-178C still works this way for good reasons.

*Attacking it:* it optimises for the accountability of the *process* over the usefulness of the
*product*. It creates the incentive to produce documents that pass review rather than software that
works, and it puts the first honest integration at the end (FBI VCF).

| | |
|---|---|
| 3 | A real reason a procurement body prefers it, that a competent person would hold |
| 3 | A position taken, with an argument, either way |

**Award the full 6 to a student who argues that the reason is good *and* that the outcome is bad**,
and distinguishes the two. That is the correct answer and few students find it. **Deduct 3** for
"because they were bureaucrats" — an explanation that explains nothing.

---

## Q2: The Manifesto as Four Trade-Offs (30)

### (a) [12]

3 per row. 2 for the two situations, 1 for the deciding property — **and the fourth column must
differ across the four rows**, which is where most of the marks are lost.

**Model answers for column 4** (accept any well-argued property):

| Value | Deciding property |
|---|---|
| Individuals over processes | **The cost of a lapse of attention.** Where forgetting a step is catastrophic and the step is invariant, it belongs to a tool |
| Working software over comprehensive documentation | **The expected lifetime of the knowledge relative to the author's tenure.** If the reader will be someone else in two years, write it down |
| Customer collaboration over contract negotiation | **Whether the parties' interests are aligned, and whether there is one party.** Adversarial or many-headed → the contract is doing real work |
| Responding to change over following a plan | **The cost of reversing the decision.** Cheap-to-reverse → respond; expensive-to-reverse (schema, security model, data migration) → plan |

**Mark 0 for column 4 if two rows give the same property**, however well written. The instruction is
explicit in the paper and the exercise is exactly that discrimination.

Common good answers not in the table: "how observable the outcome is"; "whether the work is
judgement or vigilance"; "how many people must stay in agreement".

### (b) [10]

**Route 1 — extend.** A second class where the right-hand side wins. Best answers: **security
review**; **incident response** (a runbook beats improvisation at 3 a.m.); **data migration**;
**regulatory sign-off**; **on-call handover**. **The common property**, which carries 4 of the 10:
these are tasks where the *work is vigilance rather than judgement*, the correct sequence is known
in advance, and the cost of an omission is disproportionate to its size. **Knight Capital's eighth
server is exactly this.**

**Route 2 — rebut.** A strong rebuttal exists and should be rewarded at least as highly. It runs:
the manifesto's line is about **how to organise a team**, not about **which tasks to automate**; the
Knight Capital deployment was not "individuals over processes", it was a *bad process executed by
individuals*, and the manifesto explicitly grants that the right-hand items have value. **A student
who quotes the closing sentence in support of this gets full marks** — it is the correct reading and
it is the sentence the course keeps insisting on.

| | |
|---|---|
| 4 | The second class, or the rebuttal's central claim |
| 4 | The common property, or the reading of the manifesto that supports the rebuttal |
| 2 | Concrete, not generic |

### (c) [8]

The hardest principles in a university team, roughly in order of how often students pick them:

| Principle | Why genuinely hard here | Best substitute | What it loses |
|---|---|---|---|
| *"Business people and developers must work together **daily**"* | **There is no customer.** The instructor is a proxy, and a proxy who is also the assessor distorts every question asked | A named external stakeholder — a department administrator, a lecturer who books rooms — interviewed twice | You get **opinions, not behaviour**; and twice is not daily, so you cannot course-correct within an iteration |
| *"Deliver working software frequently"* | Nobody uses it, so "delivered" has no meaning | Deploy to a staging environment on every merge; demo to another team in Week 7 | No usage data. You never learn which of your features is in the 45% (L02 §5) |
| *"Sustainable pace… indefinitely"* | Five other courses, and two midterms in the same three days as this one | Plan the light iteration around Week 6 deliberately | It is a schedule, not a pace — the crunch is imposed from outside and cannot be smoothed |
| *"The most efficient… conveying information is face-to-face"* | Timetables do not overlap | One fixed 90-minute weekly slot, protected | Everything between slots is asynchronous, so decisions are slower and quieter |

| | |
|---|---|
| 3 | A principle named, with a **specific** structural reason — not "we are busy" |
| 3 | A substitute that could actually be done this term |
| 2 | **What the substitute loses.** This is the mark most often missed |

---

## Q3: A Failure, Reconstructed (30)

### (a) [10]

| | |
|---|---|
| 4 | What happened, accurately, within 300 words |
| 3 | The immediate technical cause, correctly |
| 3 | A primary source — inquiry, post-mortem, regulator's filing, peer-reviewed paper |

**Deduct 3** for Wikipedia as the source rather than the route. **Deduct 2** for exceeding 300 words
by more than 20% — concision is a marked skill here and this is the cheapest place to teach it.

**Reference answers for the common picks:**

- **Therac-25** — a one-byte counter overflowing to zero every 256 increments, plus a race between
  the operator's edits and the setup routine reachable only by fast typing. Source: Leveson &
  Turner (1993). **Watch for students who stop at "a software bug"** — the Therac-25's interest is
  that hardware interlocks were *removed* because the software was trusted.
- **Knight Capital** — deployment to 7 of 8 servers; a repurposed flag re-enabled the eight-year-old
  "Power Peg" routine. $460M gross / $440M net in 45 minutes. Source: SEC Admin. Proc. 3-15570 (2013).
- **Horizon** — the interesting failure is not a single defect but the **presumption that the system
  was reliable**, which was legally load-bearing in prosecutions. Source: the Post Office Horizon
  IT Inquiry, or Bates v Post Office [2019] EWHC 3408 (QB).
- **Heartbleed** — a missing bounds check on a length field in an OpenSSL heartbeat; consequential
  because of the monoculture and the absence of funded review. Source: CVE-2014-0160 and the
  Codenomicon disclosure.

### (b) [12]

**4 per decision.** The marks are in the third part.

| | |
|---|---|
| 1 | The decision is a real, identifiable decision, not a restatement of the failure |
| 1 | Who was placed to make it |
| **2** | **What would have had to be true for it to be right** |

**This is the question that separates the top decile.** Worked example, Knight Capital:

> **Decision:** reuse the dormant `Power Peg` flag for the new order-router feature, rather than
> introducing a new one.
> **Who:** the engineer implementing it, with whatever review the team ran.
> **Right if:** the old code path is genuinely unreachable — i.e. it has been deleted, or no server
> can be running a build containing it. **Neither was verified**, and the flag's old meaning had
> lived in the codebase for eight years. **The decision was right in a world with automated
> deployment verification and dead-code removal, and Knight had neither.**

**Deduct heavily for blame.** "The developer was careless" is not a decision and earns 0 for that
row. Every decision in every one of these cases looked reasonable to a competent person at the time,
and reconstructing that is the entire exercise.

### (c) [8]

| | |
|---|---|
| 4 | A practice that plausibly catches it, **with a mechanism** |
| 4 | A practice that plausibly would **not**, with a reason |

**"Better testing" earns 0.** The answer must name the level, the assertion and the path. Good
examples:

- *Therac-25*: a **property-based test** (W6) over interleavings of operator input, asserting that
  delivered dose ≤ prescribed dose on every path. **Would not have helped:** unit tests of the dose
  calculation, which was correct; nor code review of the diff, since the defect is an emergent
  property of concurrency and is invisible in a diff.
- *Knight*: **automated deployment verification** (W8) — the pipeline asserts that all eight hosts
  report the deployed SHA. **Would not have helped:** any amount of unit testing; the deployed code
  was correct on the seven servers that had it.
- *Heartbleed*: **fuzzing / memory-safety analysis** in CI. **Would not have helped:** code review —
  it was reviewed, by competent people, and the bug is a missing check rather than a present error.

**Award full marks for a well-argued "none of them would have caught this"** where the student shows
why — several of these are organisational failures. Horizon in particular is not a testing problem.

---

## Q4: The Evidence Question (20)

### (a) [8]

| | |
|---|---|
| 2 | Two genuinely conflicting studies, cited properly |
| 3 | What each measured, on whom, how many, how long |
| 3 | **A specific methodological difference** that explains the conflict |

**The TDD literature is the easiest route and the richest.** A good pairing:

- **George & Williams (2003)** — 24 professional developers, pairs, one short task. TDD group
  produced code passing ~18% more black-box tests, took ~16% longer.
- **Fucci et al. (2016)**, external replication, 39 professionals — **no significant difference** in
  external quality or productivity attributable to test-*first*. What predicted the outcome was
  **granularity and uniformity of the development cycle**, independent of ordering.

**The methodological difference that matters:** the early studies compare *TDD* against
*unstructured development with testing at the end*, confounding "test first" with "test often and in
small steps". Fucci separates the two and the effect goes with the second. **A student who identifies
this confound gets the full 3 even if the citations are different ones.**

Other acceptable pairings: pair programming (Williams et al. 2000 vs. Arisholm et al. 2007 —
experience level is the moderator); code review (Fagan-style inspection vs. modern PR studies —
the *treatment is not the same treatment*).

**Deduct 2** for two studies that agree, presented as disagreeing.

### (b) [6]

**Jørgensen & Moløkken's objections, the two strongest:**

1. **The sample is not described and appears to be self-selected.** The 1994 report gives no
   sampling frame; respondents were solicited in a way that plausibly over-represents troubled
   projects, and the authors note that Standish has declined to release the methodology.
2. **"Failure" is defined so broadly that it is uninformative.** A project delivered late or over
   budget by any margin is "challenged"; the reported ~189% average cost overrun is inconsistent
   with every other overrun study of the period (which cluster near 30–40%), and cannot be
   reconciled with the reported figures internally.

| | |
|---|---|
| 4 | The two objections, in the student's own words, from having read the paper |
| 2 | A defended position on the final question |

**The answer that earns the 2** is some version of: *they are measuring something real — projects do
overrun — but not the thing they claim, and the precision of the percentages is unwarranted by the
method.* Accept "worthless" if it is argued from the undisclosed sampling frame. **Do not accept a
position with no argument.**

### (c) [6]

| | |
|---|---|
| 3 | A coherent design: population, intervention, control, outcome, duration |
| 2 | **A confound named that cannot be eliminated** |
| 1 | Why it has not been run |

**The good answer's shape:** professional developers (not students — the external validity problem
sinks most of the existing literature), randomised to test-first or test-after **with cycle length
held constant** (this is the control that makes it a study of TDD rather than of small steps), on a
**real project over 6–12 months** (short tasks measure the wrong thing), with the outcome measured as
**defects found after release and cost of change at month 9**, not as tests passed.

**The confound that cannot be eliminated: blinding.** A developer knows which arm they are in, and
motivation, Hawthorne effects and self-selection into a preferred practice cannot be removed.
Accept also: developer skill variance swamping the effect size, which would demand a sample far
beyond what anyone funds.

**Why it has never been run:** a randomised trial over nine months with enough professionals for
power costs millions, must be paid by someone with no commercial interest in either result, and
would answer a question whose answer — as the student should notice — **is probably
context-dependent anyway**. Award the mark for any of these.

---

## Overall Bands

| Band | |
|---|---|
| **90–100** | Royce quoted correctly with the page. Q2(a) column 4 has four distinct properties. Q3(b) reconstructs reasoning with no blame. Q4(a) names the confound. **At least one defended disagreement with the lectures** |
| **75–89** | Sources real and read. Positions taken. Q3(b) gets 2 of 3 decisions right. Q4 competent but thin on methodology |
| **60–74** | Accurate, sourced, and entirely downstream of the lectures. Q2(a) column 4 collapses to two distinct properties. Q3(b) describes causes rather than decisions |
| **45–59** | Secondary sources only. Q1(a) hedged because the paper was not opened. Q3 is a narrative with no decisions. Q4 asserts the evidence is weak without reading anything |
| **< 45** | Royce credited with endorsing Figure 2. The four values as commandments. No citations, or citations that do not say what is claimed |

**Feedback note to write on every paper, whatever the mark:** name the one place the student was most
nearly right and pushed least. A 0 exists to establish that this course rewards pushing.

---

*CS 212 · Week 0 · A 0 Solutions · INSTRUCTOR ONLY*
