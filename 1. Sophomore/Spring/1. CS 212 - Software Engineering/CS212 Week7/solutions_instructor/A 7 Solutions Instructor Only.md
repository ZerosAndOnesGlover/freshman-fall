# CS 212 · Assignment 7 — Marking Guidance
## **INSTRUCTOR ONLY** · Do not distribute

---

**This paper has no model answers**, because the artefact under review is a different piece of code
for every student. What follows is a marking procedure and a calibration set.

**Marking philosophy.** The paper's own sentence is the rule: **the mark is for the review you give,
not the code you wrote.** A thoughtful review of a weak pull request scores highly; a terse approval
of an excellent one does not. Students find this counter-intuitive and it should be said again in
feedback.

**Mark Q1 from GitHub before opening the PDF.** The PDF reports on the review; the review is the
evidence. Reading the PDF first primes you to accept its account.

**The three discriminators:**

1. **Does the review reach pass 2 or pass 3?** This is the single split in the cohort. Roughly half
   of every cohort produces a review that is entirely pass 5 with labels bolted on.
2. **Q3(c) — the shared blind spot.** The question that only this assignment can answer, and the one
   students most often answer vaguely. A specific finding here is a strong signal.
3. **Q4(b)'s arithmetic.** *"It was annoying"* against *"41 firings, 41 dismissals, three seconds
   each of the forty minutes a reviewer has."*

**Automatic caps, both stated:** no severity labels → 65; approval with no substantive comment → 45.

**Calibration:** median 66–70. Lower than A 6 because Q1 is marked on somebody else's artefact and
half the cohort under-reaches.

---

## Administration, Before Marking

**Check the pairing held.** Some pairs fail — a partner drops the course, or never opens a PR. **A
student whose partner defaulted must not be penalised.** If they reported it by Monday 23 March as
the paper instructs:

- **Re-pair them** if the report came early enough, and extend by one week.
- **If too late to re-pair**, mark Q1 from a review of any pull request from another team (arrange
  one), and mark Q3 from their own team's reviews, noting that Q3(c) is weakened. **Scale Q3 to 14
  and rebase the paper.**

**Check the PR sizes.** A nominated PR under 80 or over 400 lines is out of spec. **Do not penalise
the reviewer for it** — penalise the author, at Q1's size checklist item, only if they were the one
out of spec, and note in feedback that L22 §4 predicted the outcome.

---

## Q1: The Review (35) — marked on GitHub

### [10] Checklist coverage

| | |
|---|---|
| 10 | At least one substantive **pass 2 (design)** comment **and** one **pass 3 (correctness)** comment, both genuine |
| 7 | One of the two, plus good pass 4 coverage |
| 4 | Pass 4 only — tests discussed, design and correctness not |
| **2** | **Entirely pass 5**, however many comments. The paper states this cap |

**What counts as a genuine pass 2 comment** — calibration, because students and markers both
inflate this:

| Genuine | Not |
|---|---|
| *"This rule is in the route handler; the domain package is where the other three live — is there a reason?"* | *"Maybe move this function up?"* |
| *"`PricingPolicy` has one implementation here. What's the second?"* | *"Nice abstraction."* |
| *"This adds a column, which is expensive to reverse. Is there an ADR?"* | *"Should this be a dataclass?"* |

**What counts as a genuine pass 3 comment:**

| Genuine | Not |
|---|---|
| *"This reads then writes. Can two requests interleave between lines 14 and 22?"* | *"Add error handling."* |
| *"What happens when `holds` is empty — `max()` raises, doesn't it?"* | *"Check for edge cases."* |
| *"`slot.replace(hour=...)` on 29 March — does this survive the DST boundary?"* | *"Watch out for timezones."* |

**The distinction in both tables is specificity to the code in front of them.** A generic instruction
is a pass-5 comment about diligence, not a pass-2 or pass-3 finding.

### [8] Severity labels

| | |
|---|---|
| 8 | Every comment labelled, and the labels are **used correctly** — nits are actually nits |
| 5 | Most labelled; one or two missing |
| 2 | A few labelled |
| **0** | None → **cap the paper at 65** |

**Check for label inflation**, which is the interesting failure: a student who labels a naming
preference `blocking:` has not understood the convention, and it does real harm — it is how a review
becomes an ordeal. **Deduct 3** and explain.

**Also check for the opposite**, which is rarer and worth praising: a student who labels a genuine
design concern `question:` because they are not certain, and says so. **That is exactly right.**

### [7] Question form

| | |
|---|---|
| 7 | Questions where the author may know more; assertions reserved for certainty on things that matter |
| 4 | Mostly questions but phrased as rhetorical ones — *"why would you do this?"* is an assertion wearing a question mark |
| 2 | Assertions throughout, though polite |
| 0 | Assertions about design choices, stated as facts |

**The rhetorical-question failure is worth naming in feedback.** *"Did you consider that this
breaks under concurrency?"* is not the question form; *"I think the read and write can interleave
here — am I reading it right?"* is. **The difference is whether the reviewer has left themselves room
to be wrong.**

### [6] The why, once

6 for every substantive comment carrying a reason; 3 for about half; 0 for instructions throughout.

**Deduct 2 for over-explaining** — a paragraph of rationale on a nit is its own failure, and it
consumes the author's attention as surely as an unlabelled comment.

### [4] The verdict

4 requires a stated verdict **against the standard**. Look for evidence they applied *"definitely
improves code health"* rather than *"is it how I would have written it"*.

**Full marks for an approval with unresolved nits**, explicitly reasoned: *"approving — the two nits
are preferences and the change is clearly better than what's there."* **That is the standard applied
correctly and about a third of the cohort cannot bring themselves to do it.**

**Also full marks for a request-changes on a genuine design or correctness concern.** What loses the
mark is request-changes over pass 5 items.

---

## Q2: What You Found, and What It Cost (20)

### (a) [8]

| | |
|---|---|
| 5 | A complete table: comment, pass, label, acted-upon |
| 3 | Counts by pass, correct |

**Cross-check two rows against GitHub.** Students misclassify their own comments upward — a naming
comment recorded as pass 2. **Deduct 2** for systematic inflation and say which rows.

### (b) [6]

| | |
|---|---|
| 3 | The comparison made, with the lecture's figures |
| 3 | **A reason for the difference that is about the artefact or about them** |

**Expected distributions**, and both are fine:

- **Defect-heavy** (more than Bacchelli's ~14%): usually a date-arithmetic, pricing or state-machine
  change. **A correct reason: the artefact was logic-dense and small.**
- **Pass-5-heavy**: the honest reason is usually attention or unfamiliarity. **Award full marks for
  *"almost all mine were pass 5, because I could not hold their layering in my head and defaulted to
  what I could see"*** — that is a true and useful observation about the mechanism, and it is L22 §4
  from the inside.

**Deduct 3** for a reason that is about their partner's code quality only (*"their code was bad"*) —
the question asks about the *distribution*, which is a fact about the reviewer as much as the code.

### (c) [6]

| | |
|---|---|
| 2 | Time and line count |
| 2 | **Lines per hour, computed** |
| 2 | An honest account of attention |

**Typical honest figures:** 90–250 lines in 30–50 minutes, i.e. **150–400 lines/hour** — at or below
Cisco's ceiling, which is the expected result and should be noted approvingly.

**A student reporting 1,200 lines/hour** has skimmed, and **the mark is for saying so.** Full 6 for
*"I reviewed 300 lines in 15 minutes, which is 1,200/hour, four times Cisco's ceiling — and looking
back, my last four comments are all naming, which is what running out of attention looks like."*
**That is a better answer than a comfortable one.**

**Deduct 2** for no arithmetic.

---

## Q3: Being Reviewed (20)

### (a) [8]

| | |
|---|---|
| 4 | Every received comment, with the disposition |
| **4** | **At least one argued back, with a reason** |

**The 4 marks for arguing back are the point of the question** and must be awarded honestly. Accept:

- A defended disagreement on a design choice, citing the *"is it reasonable"* standard.
- **A disagreement the student lost** — *"I argued, they showed me the case I'd missed, I changed it"*
  — which is fully creditable and often the better answer.
- **"They were right about all of them"** → 2 of 4, **unless** the student says what they checked
  before conceding. A student who verifies rather than defers has done the right thing and should get
  4 with a note.

**Award 0 of the 4** for a paper where every comment was accepted with no engagement recorded. That
is compliance, not review.

### (b) [6]

| | |
|---|---|
| 4 | A specific comment, and what it revealed |
| 2 | Why it was informative rather than merely severe |

**The expected best answer, and it should be recognised as such:** a `question:` that revealed the
code was not saying what the author thought. *"They asked what `pending` meant — and we have
`pending` in the API and `HELD` in the domain for the same state, which nobody on my team had
noticed."* **That is W1 L06 §2's five-words-for-one-concept happening live**, and it should be
praised explicitly.

### (c) [6]

| | |
|---|---|
| 4 | **A specific shared blind spot**, named |
| 2 | What they changed, or a reasoned decision not to |

**This is the question the assignment exists for.** Calibration:

| 6 marks | 2 marks |
|---|---|
| *"They could not tell what `r` was. We use `r` for `resource` in eleven places because the first person to write it did, and all four of us learned it from them."* | *"They found some of our names confusing."* |
| *"They asked why `confirm` takes a `clock`. Nobody outside the team knows we inject it for the expiry tests, and it's documented nowhere."* | *"They asked a question about our design."* |
| *"They assumed a booking belonged to a course. It belongs to a person. Every one of us has assumed the same thing at some point, and our domain model says it in one line that is easy to miss."* | *"They misunderstood our model."* |

**"Nothing — they understood everything" is almost never true** and should be pushed back on in
feedback rather than penalised: cap at 3 and ask what questions they were asked, since questions are
the evidence.

---

## Q4: Move Three Things to a Machine (15)

### (a) [9]

**3 each, and the mark requires the change to exist.** Check the repository: a config diff, a hook, a
test. **A description of a change scores 1 of 3.**

| | |
|---|---|
| 1 | The comment identified, and the layer correctly named |
| 2 | **The change, committed** |

**At least one must be layer 5 (custom).** If all three are `ruff` rules, cap (a) at 6. Good
layer-5 rules from previous cohorts:

- An `ast` check that no `datetime.now()` appears in `src/slot/domain` (the injectable-clock rule).
- A test asserting every route function's return type is annotated.
- A check that every file in `migrations/` has a matching `down` operation.
- A test asserting `docs/adr/` numbering has no gaps and no duplicates.
- **A check that no test file contains `assert_called` without `autospec`** — which is W5 L18 §2
  turned into a rule, and is the best one seen.

### (b) [6]

| | |
|---|---|
| 3 | A rule turned off, with the count of firings |
| 3 | **The attention-budget argument, with arithmetic** |

**The paper's own calibration is the standard:** *"it fired 41 times, we dismissed 41, three seconds
each of the forty minutes a reviewer has"* → 3. *"It was annoying"* → 0.

**A student who discovers they had `select = ["ALL"]` and prunes it to a chosen list** has done the
best version of this and should get the full 6 — **L24 §6 predicts exactly this finding.**

**Accept "we have nothing to prune"** only with evidence: a short `select` list, a pre-commit config
with three hooks, and a statement that every rule has fired usefully. **2 of 6**, because the
exercise is the pruning.

---

## Q5: The Limit (10)

### (a) [6]

3 each, and they must be **about their own code**.

**Strong answers seen:**

- *"Our cancellation endpoint reads the booking, checks ownership, then writes. Two admin requests
  cancelling the same booking both succeed and both write an audit row, so the audit log shows two
  cancellations of one booking. Nothing in our review or our tooling looks at that, because the
  outcome is not wrong — the log is."* **Excellent: a concurrency defect that is not an invariant
  violation.**
- *"We assumed an admin may cancel any booking. If the registrar meant 'in their own department',
  every one of our tests passes on the wrong rule, and no reviewer from another team could know."*
  **The wrong-requirement case, correctly instantiated.**

**Deduct 3** for the list restated.

### (b) [4]

| | |
|---|---|
| 4 | A **practice** change: a PR-template question, a required description section, a rotation, a checklist item answered in words |
| 2 | A tooling change *(the question asks for practice; it is the wrong answer, but a real one)* |
| 0 | *"Be more careful"*, *"review more thoroughly"* |

**The best answers are mechanical and small.** From previous cohorts, and worth circulating:

- A PR template with one required line: **"Can two of these run at once? Answer in words."**
- A rule that any PR touching `domain/` requires the author to name the invariant it could break.
- Rotating the reviewer so no pair reviews each other twice running.

---

## Overall Bands

| Band | |
|---|---|
| **90–100** | The review reaches design *and* correctness with specific findings, every comment labelled and correctly graded, whys given once. Real lines-per-hour with an honest attention account. A blocking comment argued. A specific shared blind spot. Three committed automations including a custom rule, and a pruning with arithmetic |
| **75–89** | Solid labelled review with at least one design comment. Distribution compared with a reason. Received comments engaged. Two or three real automations |
| **60–74** | Review mostly pass 5 with labels. Counts without analysis. Comments accepted without judgement. Automations described, not committed |
| **45–59** | Terse or unlabelled review (capped at 65 / 45). No design or correctness comment. Nothing moved to a machine |
| **< 45** | No review posted |

**Feedback note for every paper:** quote back their single best comment and say which pass it was in.
**Students systematically over-rate their pass-5 comments and under-rate their questions**, and one
concrete correction here changes how they review for the rest of the term — including on their own
team, where the effect compounds.

**Cohort-level note to publish after marking:** the distribution by pass, aggregated and anonymised,
against Bacchelli's figures. **Every cohort is more pass-5-heavy than Microsoft's professionals**, and
seeing that as a group is more persuasive than being told it individually.

---

*CS 212 · Week 7 · A 7 marking guidance · INSTRUCTOR ONLY*
