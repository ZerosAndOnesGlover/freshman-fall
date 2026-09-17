# CS 212 · Assignment 12
## Retrospective: What the Process Cost, and What It Bought

---

**Released:** Week 12, Wednesday 17:00 · **Due:** Week 12, **Friday 24 April, 17:00** — the same day as A 11
**Total: 100 points** · Submit a PDF, `A12_{LastName}_{StudentID}.pdf`. **1,200–1,600 words**, excluding tables.

> **This is deliberately short**, because A 11 is not and both are due on the last teaching day,
> alongside Problem Sets 11 and 12 in every other course. **It should take an evening.**
>
> **It is built on documents you already have**: `docs/charter.md`, six `docs/retro-*.md` files,
> `docs/adr/`, `docs/debt.md`, and your `git log`. **Read those before you write anything** — L39 §6's
> last instruction is that your commit history is the most honest document your team produced.
>
> **It is not a group document.** Your teammates will disagree with parts of it, and that is expected.
> Nothing here is marked on loyalty, and Q4 is marked on the opposite.

---

### Q1: What the Charter Got Wrong (20 points)

In Week 0 you wrote `docs/charter.md`: a Definition of Done, a WIP limit, role rotations, a communication rule, a disagreement rule, and three things you were deliberately not building.

**(a) [8]** **Go through it line by line and mark each commitment: kept, quietly abandoned, or renegotiated.** A table. **Be specific about *when* each one stopped being true**, with evidence — a week, a commit, a retro.

**(b) [6]** **Pick the commitment that turned out to be most wrong**, and say why it was wrong when you wrote it — **not "we were optimistic", but what you did not know in Week 0 that you know now.**

**(c) [6]** **Your WIP limit.** What was it, did you keep it, and what was your actual cycle time? **Give a range**, from your board, at roughly the 80th percentile (L38 §3).

**If you never measured it, say so** — and estimate it from your board's timestamps now, which takes ten minutes. **An honest reconstruction scores more than a remembered number.**

> **The charter template said it directly:** *"a charter that was never wrong about anything was not
> specific enough to be wrong."* **A paper claiming every commitment was kept scores in the 50s**, and
> the reason is stated: if nothing was violated, nothing in it was demanding.

---

### Q2: The Six Retrospectives (20 points)

**(a) [10]** For each of your six retros: **what change did it produce?** A table: week, the change, and whether it stuck.

**A retro that produced no change scores 0 for its row.** The rubric said so since Week 6: *"a retro must name something the team changed as a result."*

**(b) [5]** **Which single change produced the most value, and how do you know?** Evidence, not impression — a cycle-time shift, a pipeline time, a review latency, a count of merge conflicts, a number of PRs that sat unreviewed.

**(c) [5]** **Which retro was the most useful, and was it the one where the most had happened?** L39's brief and the project brief both suggest the answer is no — *"two of the six most useful retrospectives in last year's cohort were about why a fortnight produced nothing."* **Say whether that held for you.**

---

### Q3: What the Process Cost (25 points)

**The assignment's actual question. Be quantitative.**

**(a) [10]** **Estimate the hours your team spent on process rather than on the product**, broken down. Reviews, retros, ADRs, the debt register, CI maintenance, meetings, writing the charter. **Show your working** — you have timestamps, PR histories and Actions runs.

**A range is fine; an unjustified number is not.**

**(b) [9]** **For each of the three largest items, say what it bought, with evidence.** And for at least one, **say honestly that it bought less than it cost.**

| Cost | What it bought | Evidence | Worth it? |
|---|---|---|---|

**[3 of the 9]** are for the honest negative. **Something in your process was not worth its cost** — and naming it is the mark.

**(c) [6]** **The counterfactual.** If you had done **none** of it — no reviews, no ADRs, no retros, no pipeline, no register — **what would be different on 1 May?** Be concrete: about the code, about the demo, and about what four people would know.

**Both answers are creditable.** *"We would have shipped more features and could not have demonstrated the invariant holds"* is an answer. *"For a thirteen-week project with one client, most of it would have made little difference and the pipeline would have"* is **also** an answer, and a braver one — **and W3 L12 §6's marking principle applies: an honest assessment scores above a loyal one.**

---

### Q4: Your Own Part (20 points)

**(a) [6]** **What did you do?** Your commits, your reviews, your part of the pipeline, the sections of the report and the ADRs you wrote. **Specific, and checkable — `git shortlog -sn` and the PR history will be read.**

**(b) [7]** **What did you do badly?** Not a modesty formula — a specific thing, with what it cost the team.

**Full marks require a cost.** *"I should have communicated more"* scores 0. *"I held PR #41 for nine days because I did not want to admit the approach was wrong, which blocked two people for a week"* scores 7.

**(c) [7]** **The disagreement you did not have.** A 1 Q5 asked you to disagree with a team decision in Week 1. **Name one you kept to yourself all term** — and say what it would have cost to raise, what it cost not to, and which was more.

> **This question is about psychological safety measured from the inside** (L38 §2). **Every team of
> four or five has at least one of these.** A paper claiming none scores 2 of 7, and the feedback will
> ask what the team's charter §6 rule was and whether anyone ever used it.

---

### Q5: The One Thing (15 points)

**(a) [8]** **What will you do differently on your next project, because of this one?** One thing. **Specific enough to be checked** — a practice, a habit, a rule, a question you will ask.

**Not a value.** *"I will care more about testing"* scores 0. *"I will write the characterisation test before I touch anything I did not write, because in A 9 I broke `render_week` twice before I pinned it"* scores 8.

**(b) [7]** **What did this course get wrong?** A practice it over-sold, an argument it did not make, a week that was not worth its place, a claim you now doubt.

**This is marked on the quality of the argument, and there is no penalty of any kind.** The course spent thirteen weeks asking you to treat every practice as a claim about cost in a context with evidence, **including its own** — six questions on the final exam are contested positions and say so.

**A paper that finds nothing to criticise scores 2 of 7.**

---

## Marking

| Band | |
|---|---|
| **90–100** | Charter commitments dated with evidence, and the most-wrong one explained by what they did not know. Cycle-time range from real timestamps. Six retros with changes and one evidenced as most valuable. Process hours with working, and an honest negative. A concrete counterfactual. A specific self-criticism with a cost. **The disagreement they did not have.** One checkable change, and a real criticism of the course |
| **75–89** | All questions answered specifically, with evidence. Process cost estimated. Self-assessment honest. Criticism of the course present |
| **60–74** | Charter reviewed generally. Retros listed without changes. Process cost asserted. Q4(b) is a modesty formula. Q5 is a value rather than a practice |
| **45–59** | Claims every commitment was kept. No numbers. No self-criticism. Nothing wrong with the course |
| **< 45** | Generic reflection with no reference to their own documents |

**Two things that cap this paper.** **Claiming every charter commitment was kept → 55.** **Claiming no suppressed disagreement and no criticism of the course → 60** — not as a punishment, but because both are evidence that the paper was not written honestly, and honesty is the only thing this assignment can measure.

---

*CS 212 · Week 12 · Assignment 12 · 100 points · due Friday 24 April, 17:00*
