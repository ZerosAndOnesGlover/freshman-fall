# CS 212 · Final Examination — Solutions and Mark Scheme
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy.** The paper promises that **a defended disagreement scores full marks**, and names
six contested positions. **That promise must be honoured or the course's entire stance collapses** — the
whole term has asked students to treat every practice as a claim about cost in a context with evidence,
including the course's own.

**The six contested positions, for the avoidance of doubt:** the TDD evidence (W5 L17 §3); the SOLID
scoreboard (W2 L08 §6); whether microservices are ever right at small scale (W3 L12 §3); whether
function length is ever the problem (W2 L07 §1); whether a coverage target is ever defensible (W6
L19 §4); and whether the course's own process apparatus was worth its cost (W12 L39 §4).

**Where a question says "with a number" or "with evidence", cap an answer without one at half.** The
*Given facts* table supplies every figure, so there is no excuse.

**Timing:** 100 marks in 150 minutes. **Section A should be quick** — ten two-sentence answers. Watch for
scripts that spend an hour on it; mark generously there and let Section C carry the discrimination.

**Calibration:** median 64–68. Section A high (most 22+), Section B is the spread, Section C separates
the top decile.

---

## Section A — Short Answers (30)

**3 marks each. Two or three sentences. Do not reward length.**

**A1.** **If a test had to change, it was not a refactoring.** (2) Tests encode observable behaviour, so a
change requiring a test edit has changed what the system does. (1)

**A2.** **At the narrowest point every path must pass through.** (2) The domain layer is not enough for
uniqueness because **two processes both check, both pass, both insert** — check-then-act cannot be made
atomic in application code across workers. (1)

**A3.** *"With enough users, it does not matter what you promise in the contract: all observable
behaviours will be depended on by somebody."* (2) **`roomsvc`'s `GET /bookings` returned insertion order
because nothing said otherwise; the timetable generator depended on it; an index broke it in 2023.** (1)

**A4.** ***Integrate*** **and** ***daily***. (2) `git log --oneline main --since='7 days ago' | wc -l`, and
**the age of the oldest open branch.** (1)

**A5.** **Coverage measures what was executed; mutation score measures whether the suite would notice a
change.** (2) **Just et al. — mutant kill rate predicted real-fault detection after controlling for
coverage**; Inozemtseva & Holmes found coverage's correlation largely vanishes after controlling for
suite size. (1)

**A6.** *"A module should be responsible to one, and only one, **actor**"* (2) — better because **"one
thing" has no stopping rule** and *"which actor asks for this to change?"* is answerable. (1)

**A7.** Because **a characterisation test looks exactly like a normal test, and will be read as a
specification** by the next person, who will then defend the bug. (2) **The comment must say it records
behaviour rather than endorsing it.** (1)

**A8.** **Interest = badness × touch frequency.** (2) **Touch frequency requires no judgement** — it is a
count from `git log`. (1)

**A9.** **`blocking:` / `question:` / `nit:` / `praise:`** (2). Without them **every comment reads as
blocking**, so fifteen comments feel like a rejection even when fourteen are nits. (1)

**A10.** **Code is executed, so it cannot silently become false. Prose is not, so it does** (2) — **and a
stale README looks identical to a fresh one**, whereas a stale test fails. (1)

---

## Section B — Applied Judgement (40)

### B1. One mechanism, three literatures [12]

**(a) [4]** 1 for **batch size**; 1 each for the three findings: **Cisco/Google** — defect density
collapses above ~200 LOC, median change ~24 lines; **Fucci et al.** — no significant effect of
test-*first*, benefit tracks granularity and uniformity of the cycle; **DORA** — deployment frequency and
lead time move *with* low change-failure rate and fast restore.

**(b) [4]** **The three explanations must differ.** 1 each, plus 1 for them genuinely differing:

| | |
|---|---|
| **Review** | A large diff **exceeds working memory**, so a reviewer checks local properties and cannot check correctness. **Plus the social mechanism**: rejecting 900 lines tells someone their week was wasted, so reviewers approve big changes |
| **TDD** | Small steps **localise the cause**: when a test goes red, only one thing changed, so the diagnosis is immediate rather than a bisection |
| **Deployment** | A deploy of one commit that breaks gives **one suspect**; a release of 200 gives 200. **Diagnosis and reversal both scale with batch size** |

**Cap at 2** if the three explanations are the same sentence three times — that is the question.

**(c) [4]** 2 for **why convergence is stronger**: three independent methods, populations and outcome
measures agreeing is much harder to explain by a single methodological artefact than any one result is.
**2 for a shared confound**, and accept:

- **All three are observational**, and all three plausibly measure **teams that are already disciplined** — the small-batch practice may be a *symptom* of a well-run team rather than a cause.
- **All three are self-selected**: organisations that measure deployment frequency, developers who volunteer for TDD studies, companies that publish review data.
- **Reverse causation**: a codebase that *permits* small changes is a well-structured codebase, and the structure may be doing the work.

**Full marks and a note for the reverse-causation answer** — it is the sharpest and about one in ten
finds it.

### B2. A code review [14]

**(a) [5]** 2 for **acting before reading code**; 1 each for three of:

- **640 lines — ask for a split.** Above ~400 the evidence says you will find nothing.
- **The title says "refactor + fix"** — two things. **A refactoring mixed with a behaviour change cannot be reviewed; each hides the other.**
- **Empty description** — ask why, and what to look at first, before reading further.
- **"Tests pass" is not information** about a change that includes a refactoring (see (b)).

**Deduct 2** for a script that starts reading the diff. **Pass 1 is two minutes and often ends the
review**, and that is the question.

**(b) [5]**

**3 for a comment that is question-shaped, labelled, and explains why.** Model:

> **`blocking:`** *This moves `notify` outside the transaction. I think that changes behaviour rather
> than structure — before, a notification failure rolled back the confirmation; now the booking stands
> and the notification is lost. Is that the intent? If so it needs its own commit and a test for the new
> behaviour.*

**1: it is not a refactoring** — **observable behaviour changed**, in the failure case.

**1: the passing tests are not evidence** because **nothing tested the rollback path.** The tests cover
the happy path, where both orderings are indistinguishable. **Full marks for a script that adds that the
absence of a failing test is itself the finding.**

**Award the full 5 to a well-argued "this is an improvement and still not a refactoring"** — that is the
correct reading and (c) depends on it.

**(c) [4]**

2 for the reconciliation: **the change is right and the process is wrong.** Being correct about the
destination does not make a change a refactoring, and it does not make it reviewable inside a 640-line
PR titled *"refactor + fix"*.

2 for what should have happened: **a separate commit, declared as a behaviour change, with a test that
fails before and passes after** — plus, ideally, **the two hats** named (W9 L28 §4) and a note that the
right place for *"you told me last week"* is an ADR rather than a memory.

**Full marks and a note** for a script that observes the author has done something genuinely good and is
being told off for the packaging — **and that a reviewer should say so explicitly**, because this is
exactly where psychological safety is won or lost (W12 L38 §2).

### B3. A number that is not what it looks like [14]

**(a) [6]**

3 for a defensible ranking, 2 for justification, **1 for identifying the non-problem.**

**The non-problem is the 1,400-line domain package.** It is a size, not a defect; nothing in it is
actionable. **Accept "branch coverage 91%" as the non-problem only if argued** — it is not a problem in
itself, but in combination with 38% it is a finding, so this is weaker.

**The expected ranking, and accept variations with reasons:**

1. **Four open branches, oldest eleven days** — **they are not doing CI**, and this is the finding that damages everything else. It is also the cheapest to act on.
2. **The 38% mutation score** — the suite would ship a regression.
3. **Eleven-minute pipeline** — at that length people stop waiting, which causes (1).

**Full marks for a script that argues 3 causes 1** — the pipeline length produces batched pushes, which
produces long-lived branches (W8 L25 §4). **That is the correct causal reading and it should be
rewarded.**

**(b) [4]**

2 for the explanation: **the suite executes nearly everything and checks almost nothing.**

2 for the two survivor types, 1 each with an example:

- **No assertion** — a test that calls a function and asserts nothing. *`test_pricing()` calling three cases and asserting none.*
- **Asserting the route, not the result** — `mock.assert_called_once_with(...)`, true whatever the function does with the value. *`booking = repo.confirm(hold_id)` mutated to `= None` survives.*

**Accept "branch covered one way only" as a third**, but the question asks which two would *dominate* at
91% branch coverage — **and at that coverage level the first two must dominate**, because the branches
are being taken. A script that reasons this out explicitly earns full marks.

**(c) [4]**

2 each for two reasons:

- **Goodhart.** The moment 80% is a target, the cheap ways to reach it are to test the trivial modules, delete awkward paths and add assertionless tests. **The number would rise and nothing would improve.**
- **Equivalent mutants make 80% possibly unreachable**, and chasing the last stretch is chasing undecidable non-bugs.
- **It is the wrong priority** — the eleven-day branch and the eleven-minute pipeline are more urgent.
- **Two weeks before a demo is the worst time** to be changing test structure (W11 L34 §6).

**And what to do instead**, which is required for full marks: **read twenty survivors, fix the real gaps,
record the rest on the register, and set a ratchet — *this may not get worse*.**

---

## Section C — Essay (30)

**Mark on argument.** Allocation for all three: **10 for engaging the claim rather than describing it;
12 for evidence used correctly and precisely; 8 for the strongest objection to their own position being
addressed.**

| Band | |
|---|---|
| **27–30** | A position, precise evidence, **and the strongest objection to their own position answered.** May disagree with the lectures throughout. Uses at least two cross-week connections |
| **22–26** | Clear position, correct evidence, objection acknowledged but not answered |
| **17–21** | Describes the debate accurately without taking a position |
| **12–16** | Summarises lectures; evidence asserted without provenance |
| **< 12** | Off-topic or self-contradictory |

### C1 — the evidence is weaker than the confidence

**Must use four, and must use them precisely.** The common failures are stating the controls backwards
(**Inozemtseva & Holmes controlled for *suite size*; Just et al. controlled for *coverage***) and
treating DORA as experimental.

**The strongest essays attack the claim rather than agreeing**, and the best available attack is:
**the claim is true of the *cultural* practices and false of the *mechanical* ones.** Version control,
CI, automated testing and type checking have effects so large and so mechanically explicable that
demanding RCT evidence is a category error. **A script that separates the two and says the confidence is
*correctly* calibrated for half the course scores 27–30.**

**On the four disowned originators**, the answer wanted is about the **transmission mechanism**: a
memorable name is quotable and travels; a caveat is not and does not. **Practitioner's response: read the
primary source, and ask what population it studied.** Accept also: prefer authors who publish their own
retractions (Fowler's *MicroservicePremium*, Cunningham's 2009 clarification) — **which is itself a
selection heuristic and a good one.**

### C2 — Goodhart and targets

**Must use four of the five appearances.**

**The objection is the essay.** A 2,000-engineer organisation cannot read individual findings, so
"never set a target" appears to be small-scale advice. **The best answers distinguish:**

| Legitimate | Illegitimate |
|---|---|
| **Aggregate for allocation** — *"this area has the most incidents, put two engineers there"* | **Target for reward** — *"reach 80% or it affects your review"* |
| **A ratchet** — *this may not get worse*. No prize for exceeding it | A threshold with a bonus |
| **Diff-scoped** — Google's mutation practice: a few survivors surfaced in review, reviewers may dismiss them, and **dismissals prune the rule set** | A dashboard nobody can act on |

**A script that reaches the aggregate/target distinction scores 25+; one that also names the ratchet and
the diff-scoping scores 27–30.**

**Accept a defended "targets are sometimes necessary"**: in regulated contexts (DO-178C requires MC/DC
coverage **as a target**, and people's lives are the reason), a target is the right instrument and the
gaming is controlled by audit. **That is a strong essay and should score at the top** — it is the honest
boundary of the course's position.

### C3 — twelve lines, four months

**Part 1 — account for the four months without incompetence.** 487 lines, complexity 94, eleven tests
against ninety-four paths, 31.8% branch coverage, 78% of surviving lines by an author who left in 2023,
**and no mechanism by which anyone could establish that a change was safe.** **A script that blames the
team caps at 16.**

**Part 2 — the interesting half, and where the marks are.**

*Which week would have shortened it most?* Defensible: **W6** (the mutant *is* the bug — it would have
been found before it shipped); **W5** (the concurrency test); **W9** (characterisation tests made the
change safe); **W3** (the placement would have prevented it entirely). **Any of these, argued.**

*Which would have made no difference?* **This is the harder claim and it should be marked as the
discriminator.** Defensible:

- **W4 (patterns)** — no pattern in the catalogue addresses a check-then-act race.
- **W10 (versioning)** — `confirm_booking` is internal; no API compatibility question arises.
- **W12** — presentations and career paths are not causally connected to the bug.
- **W1** — *arguable both ways*, and the best essays notice the tension: the invariant *was* known to everybody, so writing it down might have changed nothing, **or** writing it down with *where it is enforced* is exactly what was missing. **A script that argues both sides of W1 and picks one scores at the top.**

**Part 3 — was it worth it?** **A defensible "sometimes not" must score as highly as "always"**, and the
paper says so. The conditions under which it was not: **short-lived code; a single author who stays; a
system nothing else depends on; a domain where being wrong is cheap.** **A script that notes that
`roomsvc` satisfied none of those — six years, five authors, the department's timetable depending on it
— has answered the question properly.**

---

## After the Paper

**Return with a cohort-level note**, and include two figures:

1. **How many scripts disagreed with a lecture position**, across the whole paper. The six contested
   positions were published in the reading guide and in the paper's own header. **That number is the
   single best measure of whether the course's stance landed**, and it should be reported to the
   department alongside the marks.
2. **The Section C distribution.** If C3 is chosen by most of the cohort, the concrete question is doing
   the work the abstract ones should; if C1 is chosen by almost nobody, the evidence thread has not
   landed and next year's Week 0 should be adjusted.

**And one marking note for whoever inherits this paper:** **the two hardest marks in it are B1(c)'s
shared confound and C3's "which week made no difference".** Both ask a student to argue against material
they have just been taught to value. **They are deliberately the discriminators, and they should not be
softened.**

---

*CS 212 · Final Examination · Solutions and Mark Scheme · INSTRUCTOR ONLY*
