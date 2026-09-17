# CS 212 · The Final Report
## `docs/report.md` plus a PDF · Friday 1 May, 17:00 · 20 of the project's 100 marks

---

**3,000–4,000 words**, excluding tables, code and appendices. **Six sections, specified in the project
brief.** This file says what each one is marked on and what the common failures are.

> **The report is read more carefully than the demo**, at a desk, with your repository open beside it.
> **Every claim in it is checkable, and it will be checked.** A number without its command is worth
> less than no number.
>
> **It is marked on honesty as much as on outcome.** The brief says so: *a team that says "our domain
> model was wrong and we found out in Week 8; here is what it cost and here is the migration" scores
> above a team that implies it was right all along.* **Every engineer marking it has been wrong in
> exactly that way, and can tell.**

---

## 1. What You Built — and What You Did Not *(~600 words)*

**Equal weight to both halves**, and the second is where reports differentiate.

| | |
|---|---|
| ✅ | Scope, in terms of the stories you committed to and delivered |
| ✅ | **Three or more things you deliberately did not build, with the reason for each** |
| ✅ | The charter's *"what we are deliberately not doing"* table, revisited: were you right? |
| ❌ | A feature list |

**Why the second half carries the marks:** **~2/3 of delivered features are rarely or never used**
(W0 L02 §5). **Choosing what not to build is engineering**, and a scope section that only lists what
exists has not shown any.

**And revisit the charter's three.** If you built one of them anyway, say so and say why — **that is a
requirements finding, not an embarrassment.**

---

## 2. Requirements *(~500 words)*

| | |
|---|---|
| ✅ | The stories, where they came from, **and which ones changed** |
| ✅ | **At least one invariant, and where it is enforced** |
| ✅ | A requirement you got wrong, and how you found out |
| ❌ | Your elicitation process, described at length |

> **The brief's sharpest line, and it is marked:** ***a requirement that never changed all term is a
> requirement you never tested against a user.*** A report in which nothing moved is a report about a
> team that never left the room.

---

## 3. Architecture *(~700 words)*

| | |
|---|---|
| ✅ | The shape, and the quality attributes you ranked — **with the sacrifice named** |
| ✅ | **At least one ADR you would now make differently**, and why |
| ✅ | **Where the no-double-booking invariant is enforced, and why the four wider options fail** |
| ✅ | One diagram. **Label where the invariant is enforced** |
| ❌ | "We used MVC" (W3 L11 §3 — it answers no question that was asked) |
| ❌ | A justification retro-fitted to what accreted |

**On the reversed ADR**, which is explicitly required: it is **not a confession.** It is evidence that
you can evaluate your own decisions, which is the capacity this course exists to build. **A team with
no such ADR has either decided nothing or not looked back** — and the second is the more likely.

**"We did not decide; it accreted; here is the ADR we wrote in Week 11 to record what we have"** is
worth more than a retro-fitted justification. W3 L12 §6 says so and the marking follows it.

---

## 4. Quality *(~700 words)*

**Numbers with the command that produced them and the date. As trends, not scores** (W11 L35 §5).

| Metric | Report it as |
|---|---|
| **Mutation score, domain package** | With the **line count** and the trend. *"71%, from 51% in Week 6"* |
| Branch coverage | The **branch** figure, not line. **No target — it is a diagnostic** |
| Survivors | **How many you read, and what they were**: real gaps, equivalents, deliberate |
| Review history | PRs, reviewers, median time to first response |
| Pipeline | Gate time, and the trend |
| **The invariant** | **The DDL, and the concurrency test.** This is the most important artefact in the project |

> **The marking rule, restated because it surprises people:** **95% coverage with a 30% mutation score
> scores below 70% with 75%.** Just et al. and Inozemtseva & Holmes are why (W6 L21 §5), and a report
> that leads with coverage invites the question it least wants.

**And include what your numbers cannot see** (W11 L35 §6). **The strongest quality sections end by
naming a defect the project could ship today that no metric they report would reveal.**

---

## 5. Debt *(~500 words)*

**W11's method, applied to your own code. `docs/debt.md` is the artefact; this section is the argument.**

| | |
|---|---|
| ✅ | The register, summarised — **ordered by interest, not severity** |
| ✅ | **Three or more non-code items**: test, documentation, API, process, dependency, data, knowledge |
| ✅ | **What you are deliberately not repaying, and why** — including the last-fortnight case |
| ✅ | **A bus factor, if you have one**, and what happens if that person is ill |
| ❌ | A list of code smells |
| ❌ | A claim of no debt |

> **A register of eight well-reasoned items scores above a register of three, and above a claim of
> none.** A team claiming none has either not looked or is not saying.

---

## 6. Process *(~600 words)*

**Largely A 12, compressed — and written from the documents rather than from memory.**

| | |
|---|---|
| ✅ | **What each of the six retrospectives changed**, and whether it stuck |
| ✅ | **Your actual cycle time**, as a range, from your board |
| ✅ | **What the process cost**, in hours, with your working — **and one item that was not worth it** |
| ✅ | The charter commitment that turned out to be most wrong |
| ❌ | "Communication could have been better" |
| ❌ | A claim that every commitment was kept |

**A team whose process never changed did not retrospect**, and the rubric has said so since Week 6.

---

## Before You Submit

- [ ] **Every number has its command and its date**
- [ ] **Every claim about the repository is true of the repository** — it will be opened
- [ ] **The reversed ADR exists, is numbered, and is in `docs/adr/`**
- [ ] `docs/debt.md`, `docs/charter.md`, six retros, the generated OpenAPI — **all committed**
- [ ] **The README quickstart works from a clean clone**, tested on a machine that has never run it
- [ ] **Peer assessment submitted** — it affects individual marks
- [ ] **Word count inside 3,000–4,000**
- [ ] **Read your own `git log` from Week 1 first.** Thirteen weeks in the words you used at the time; it will remind you of three things you have forgotten

---

## The Two Sentences Worth Writing

**Somewhere in this report there should be a sentence like:**

> *"Our domain model had a booking belonging to a course rather than a person. We found out in Week 8;
> it cost a migration and six hours; ADR 0009 supersedes ADR 0004; and if we had spoken to the
> registrar in Week 1 instead of Week 7 we would have known."*

**And one like:**

> *"Our mutation score on the app layer is 34%. The suite would ship a regression there. It is item
> D-03, we are not fixing it before 1 May, and here is why that is the right call."*

**Those two sentences — a mistake with its cost, and a weakness with a reasoned decision to keep it —
are what distinguishes a report in the 80s from one in the 60s**, and neither requires the project to
have gone well.

---

*CS 212 · Week 12 · final report guide · due Friday 1 May, 17:00*
