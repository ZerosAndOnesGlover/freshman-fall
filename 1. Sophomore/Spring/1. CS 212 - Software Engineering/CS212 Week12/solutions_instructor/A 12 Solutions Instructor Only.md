# CS 212 · Assignment 12 — Marking Guidance
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for A 12.** **This paper can only measure honesty**, and the mark scheme must
reward the unflattering version or the incentive inverts and you receive thirteen identical papers
saying the team worked well and the course was excellent.

**Two caps exist for that reason and are stated in the paper:** claiming every charter commitment was
kept → 55; claiming no suppressed disagreement **and** no criticism of the course → 60. **Both are
evidence that the paper was not written honestly**, not moral failings, and the feedback should say so
in those terms.

**Read a team's four or five papers together.** Q1 and Q2 are about shared documents, so they should
broadly agree — **and where they disagree sharply, that disagreement is itself the most interesting
thing in the set** and is worth a note in the team's final-report feedback.

**The three discriminators:**

1. **Q3(b)'s honest negative.** Something in their process was not worth its cost. About a third will
   name one.
2. **Q4(c) — the disagreement they did not have.** Nearly every team has one; a paper claiming none
   caps that question at 2.
3. **Q5(b) — a real criticism of the course.** The strongest signal in the paper, and it should be
   collected across the cohort (see the closing note).

**Calibration:** median 70–74. This marks higher than A 11 because the work is reflective rather than
analytical, and the spread is entirely in Q3(b), Q4(b–c) and Q5(b).

---

## Q1: What the Charter Got Wrong (20)

### (a) [8]

| | |
|---|---|
| 5 | Every commitment marked kept / abandoned / renegotiated |
| 3 | **Dated, with evidence** — a week, a commit, a retro |

**Cross-check two rows against the repository.** The Definition of Done is the easiest: if it said
*"reviewed by a teammate who did not write it"*, check the PR history for self-merges. **A paper claiming
it was kept where `git log` shows twelve self-merged PRs is not being marked down for the self-merges —
it is being marked down for the claim.**

**Expected honest findings**, and these recur every cohort:

- The **WIP limit** was set in Week 0 and never referred to again.
- **Role rotation** stopped after iteration two, usually because the backlog owner was good at it.
- The **"what happens when someone goes quiet"** rule was never used, including in the fortnight when somebody went quiet.
- The **Definition of Done's** review requirement survived until the week before Phase 1.

**Apply the 55 cap** for a paper claiming everything was kept.

### (b) [6]

| | |
|---|---|
| 3 | The most-wrong commitment identified |
| **3** | **What they did not know in Week 0** |

**The 3 marks are for the epistemic answer, not the apology.** *"We were optimistic"* → 0. *"We set a WIP
limit of 3 assuming our cards were the same size. They were not — our median card was 2 days and our
longest was 11, so the limit constrained nothing and we never noticed"* → 3.

### (c) [6]

| | |
|---|---|
| 2 | The WIP limit, and whether it was kept |
| 4 | **A cycle-time range from real timestamps** |

**A reconstruction done now scores full marks** — the paper says so explicitly, and reconstructing it
from board timestamps is the honest version of the exercise.

**Expected figures:** medians of 3–7 days and 80th percentiles of 8–15. **A team reporting a median
under two days either has very small cards (good — say so) or is measuring from "started coding" rather
than from "In Progress".**

**Deduct 3** for a remembered number with no source.

---

## Q2: The Six Retrospectives (20)

### (a) [10]

**Roughly 1.5 per retro, plus 1 for the table being complete.** **A retro that produced no change scores
0 for its row** — the paper and the Phase 1 rubric have both said so since Week 6.

**Check against `docs/retro-*.md`.** Papers reconstruct changes that are not in the files.

**Common genuine changes worth recognising:** moving to smaller PRs; adding the dependency cache; a
fixed weekly 90-minute slot; rotating who owns the pipeline; **adding the `-p randomly` run after it
failed**; deciding to stop using a tool.

**"It stuck" is the more interesting column.** Full credit for honest reporting that a change lasted two
weeks and lapsed — **and a note that this is itself a retrospective finding.**

### (b) [5]

| | |
|---|---|
| 2 | A change identified |
| **3** | **Evidence, not impression** |

**Acceptable evidence:** a cycle-time shift, pipeline time, median time-to-first-review, a count of merge
conflicts, PRs open at a given moment. **"It felt better" scores 0 of the 3.**

### (c) [5]

| | |
|---|---|
| 3 | A judgement about which retro was most useful |
| 2 | Whether the quiet-fortnight claim held for them |

**Full marks for either answer**, provided it is argued. **The claim — that the most useful retros are
often the ones where least happened — is the course's, and a student who tests it against their own six
and finds it false has done exactly the right thing.**

---

## Q3: What the Process Cost (25)

### (a) [10]

| | |
|---|---|
| 5 | A breakdown by activity |
| 5 | **Working shown** — from PR timestamps, Actions runs, meeting counts |

**A range is fine.** An unjustified total is not: **deduct 5** for a single number with no derivation.

**Expected totals for a five-person team over thirteen weeks: 60–150 person-hours on process.** A paper
reporting 15 has not counted reviews; one reporting 400 has counted development. **Neither is penalised
if the working is shown** — the working is the mark, and an anomalous total with visible arithmetic is
more useful than a plausible one without.

### (b) [9]

| | |
|---|---|
| 6 | Three largest items, each with what it bought **and evidence** |
| **3** | **At least one honest "bought less than it cost"** |

**The 3 marks are the point of the question.** Honest negatives seen in previous cohorts, all of which
should score 3:

- *"The ADRs. We wrote eleven; we referred back to two. The nine others took four hours and were read once, by the marker."*
- *"Our six retros cost about nine hours. Four produced a change; two were fifteen minutes of agreeing that things were fine."*
- *"The debt register was written in Week 11 for A 11. It has not changed a single decision, because by then every decision was made."* **The sharpest one, and it is a fair criticism of the course's own sequencing.**

**A paper in which everything was worth it scores 3 of 9**, and the feedback should say why: **a process
where every element paid off has not been examined.**

### (c) [6]

| | |
|---|---|
| 3 | A concrete counterfactual — code, demo, and what four people would know |
| 3 | It is argued rather than asserted |

**Both directions score full marks**, and the paper says so. **The braver answer — *"for a thirteen-week
project with one client, most of it would have made little difference; the pipeline and the constraint
would have"* — should be marked at the top if it is argued**, and it is closer to the truth than most
students expect to be allowed to say.

**What distinguishes 6 from 3** is the third element: **what four people would know.** The strongest
answers notice that without review, only one person would understand each part — **which is `roomsvc`'s
bus factor arriving in their own team**, and it is the counterfactual's most defensible claim.

---

## Q4: Your Own Part (20)

### (a) [6]

| | |
|---|---|
| 4 | Specific and checkable |
| 2 | It matches the record |

**Check `git shortlog -sn` and the PR history.** **A claim that materially overstates their part is a
serious matter** — flag it, discuss it with the student, and weigh it against the team's peer
assessment before adjusting. **Understating is common and should be corrected upward in feedback**, not
penalised.

### (b) [7]

| | |
|---|---|
| 3 | A specific thing done badly |
| **4** | **With what it cost the team** |

**The paper's own calibration is the standard.** *"I should have communicated more"* → 0. *"I held PR #41
for nine days because I did not want to admit the approach was wrong, which blocked two people for a
week"* → 7.

**Watch for the humblebrag** — *"I took on too much"*, *"I cared too much about quality"*. **Score 2 and
name it in feedback**; it is the most common evasion in this question.

### (c) [7]

| | |
|---|---|
| 3 | A real suppressed disagreement, named |
| 4 | **The cost both ways, and which was more** |

**A paper claiming none scores 2 of 7**, and the feedback asks what the charter's §6 disagreement rule
was and whether anyone ever invoked it. **That is not a rhetorical question** — in most teams the answer
is that the rule was written in Week 0 and never used, which is a finding about psychological safety
worth putting in front of them.

**Excellent answers seen:**

- *"I thought our `Slot` decision was wrong in Week 2. I said nothing because the person who proposed it had just spent an evening on the walking skeleton and I did not want to undo it. It was right, and I only know that because of A 3, not because we discussed it."* **Full marks — the disagreement was wrong and the suppression was still the problem.**
- *"Two of us thought the UI work was wasted. Raising it would have meant telling one person their four weeks were low-value. We did not, and they spent four more."*

### Note on Q4 overall

**This question is where a team problem becomes visible**, and sometimes seriously. **If a paper
discloses something that needs a conversation — sustained exclusion, a member who was carrying
everyone, a disagreement suppressed by pressure — handle it as a pastoral matter and not only as a
mark.** The paper asked them to be honest; the response should be proportionate to that.

---

## Q5: The One Thing (15)

### (a) [8]

| | |
|---|---|
| 4 | One thing, **not a value** |
| 4 | **Specific enough to be checked** |

*"I will care more about testing"* → 0. *"I will write the characterisation test before I touch anything
I did not write, because in A 9 I broke `render_week` twice before I pinned it"* → 8.

**The test for the second 4: could a friend tell in six months whether they did it?**

### (b) [7]

| | |
|---|---|
| 4 | A real criticism |
| 3 | Argued |

**A paper finding nothing to criticise scores 2**, and this is stated. **Contribute to the 60 cap** if
combined with a claim of no suppressed disagreement.

**Criticisms that have been made and are fair — do not mark these down for being uncomfortable:**

| Criticism | Assessment |
|---|---|
| *"The debt register in Week 11 is too late to change anything. It should be Week 4."* | **Correct, and the strongest available.** Score 7 |
| *"`roomsvc` is a constructed example and we all know it. Its numbers are too neat."* | Fair. The best version notes that a real legacy codebase would have been messier and less pedagogically clean, **and that the tidiness is a cost** |
| *"The course says every practice needs evidence and then teaches ten practices with no evidence — especially Week 3."* | **Fair and the course half-concedes it** (W3's reading guide). Score 7 |
| *"A 7's cross-team review is a good idea that arrives too late to change our own habits."* | Fair |
| *"Thirteen weeks of being told the evidence is weak is demoralising and does not tell us what to do."* | **A real criticism and should score well** if argued — it is the honest cost of the course's stance |
| *"The project is 40% and we were never taught front-end, so a chunk of our time went into something unassessed."* | Fair; the syllabus warns but does not solve it |

**Score 3–4** for a criticism that is really a request for more marks or fewer deadlines.

---

## Overall Bands

| Band | |
|---|---|
| **90–100** | Charter commitments dated against evidence; the most-wrong one explained epistemically. A real cycle-time range. Six retros with changes and one evidenced. Process hours with working and an honest negative. A concrete counterfactual including what four people would know. A self-criticism with a cost. **The suppressed disagreement, with both costs.** A checkable change and a real criticism of the course |
| **75–89** | Specific throughout, with evidence. Process cost estimated. Honest self-assessment. A criticism present |
| **60–74** | Charter reviewed generally. Retros listed without changes. Process cost asserted. Q4(b) is a modesty formula. Q5(a) is a value |
| **45–59** | Every commitment kept (capped at 55). No numbers. No suppressed disagreement and no criticism (capped at 60) |
| **< 45** | Generic reflection with no reference to their own documents |

---

## After Marking — and This Matters More Than the Marks

**Collect Q5(b) across the cohort, anonymised, and act on it.** It is the only systematic feedback the
course receives from people who have just completed it, **and the course's entire stance obliges it to
be taken seriously** — thirteen weeks of *"every practice is a claim about cost, in a context, with
evidence"* applies to the syllabus.

**Two specific things to look for:**

1. **If more than a third say the debt register arrives too late**, move it. It is a real defect in the
   sequencing and the students are right.
2. **If a substantial number say the evidence-scepticism is demoralising**, that is a finding about
   *delivery*, not about the position — and Week 0 should say earlier and more clearly that the answer
   to weak evidence is **judgement**, not paralysis.

**Also publish, anonymised, to next year's cohort in Week 0:** two or three Q3(b) honest negatives and
two or three Q4(c) suppressed disagreements. **Students do not believe these are normal until they see
that a third of the previous room reported one**, and seeing it is what makes them willing to write
their own.

---

*CS 212 · Week 12 · A 12 marking guidance · INSTRUCTOR ONLY*
