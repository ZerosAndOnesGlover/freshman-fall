# CS 212 · Assignment 11 — Marking Guidance
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for A 11.** **This paper is marked on honesty.** It asks students to produce an
unflattering document about their own project and then defend not fixing most of it — **and the mark
scheme must reward the unflattering version, or the incentive inverts and you get eight cosmetic
items and a claim of no debt.**

**Say so in feedback, every time:** a register of eight well-reasoned items scores above a register of
three, and *"we gamed our coverage number and here is how"* scores above *"we did not"*.

**Mark `docs/debt.md` from the repository first.** Then the PDF.

**The three discriminators:**

1. **Are there non-code items?** At least three required, and it is a cap. A register of eight code
   smells is a smell list — **and the debt that sinks projects is process, knowledge and dependency.**
2. **Triggers or dates?** A date is the default and it is wrong. Count them.
3. **Q4(b) — the Goodhart confession.** An honest yes is worth 3 of 6, and about a third of the cohort
   will give one. The rest will say "no" without evidence.

**Two automatic caps, both stated:** `docs/debt.md` not committed → 55; no non-code items → 75.

**Calibration:** median 70–74.

---

## Q1: The Hotspot Analysis (20)

### (a) [8]

| | |
|---|---|
| 5 | One table: touches, worst-function complexity, branch coverage per file |
| 3 | **The hotspot named as the intersection**, with why not the worst single column |

**Spot-check the touch counts** by re-running the command. Numbers are occasionally invented.

**Expected shape for a `slot` at Week 11:** the hotspot is almost always `src/slot/app/` or the module
holding the booking service — the domain has the complexity, the app layer has the churn. **A student
whose hotspot is their test file has misread the command** (it does not exclude `tests/`); deduct 1 and
explain, since it is a real analysis error.

**The 3 marks require the reasoning.** *"`models.py` has 40 touches and complexity 3 — it changes often
and trivially, so it is not a hotspot; `booking_service.py` has 28 touches and complexity 19, which is
the intersection"* → full marks.

### (b) [6]

| | |
|---|---|
| 2 | The most-coupled pair, with a count |
| **4** | **The interpretation, and a proposed boundary** |

**The interpretation wanted:** if neither imports the other, **the coupling is in the domain**, and the
boundary is misplaced — the shared concept should be extracted, or one of the two should own it.

**Most common real finding in `slot`:** the route module and the schema module change together, because
adding a field touches both. **That is expected coupling across a legitimate boundary, and a student
who says so scores full marks** — recognising a coupling as *benign* is as good as proposing a fix.

**Second most common, and the interesting one:** `domain/booking.py` and `infra/repository.py` change
together, **because the repository is leaking domain knowledge.** A student who spots that has found
something real.

**Deduct 4** for a pair reported with no interpretation.

### (c) [6]

| | |
|---|---|
| 3 | `git blame` percentages for the hotspot |
| 3 | **An honest answer to the illness question** |

**Nearly every four-person team has a bus factor of 1 somewhere**, and the honest answer is the mark.
Full marks for *"Priya wrote 81% of the migration and deployment code. If she is ill on 28 April we
cannot deploy, and nobody else has run `alembic upgrade` against staging."* **Then check whether that
appears on their register as a process-debt item** — if it does, note it approvingly in Q2.

**2 of 3** for percentages with *"we would manage"*. **0** for a claim of even distribution that the
numbers contradict.

---

## Q2: The Register (30)

**Mark from `docs/debt.md`. Check `git log docs/debt.md`** — a register committed in one push the
night before is worth noting in feedback though not penalising.

### Per item [2 × 8 = 16]

0.5 each for quadrant, specificity, interest-with-evidence, and a trigger.

**The two half-marks most often lost:**

**Interest as adjectives.** *"This makes the code hard to maintain"* → 0. *"Three queries must remember
the predicate; we have added one since February and someone forgot it once, caught in PR #61"* → 0.5.

**A date instead of a trigger.** *"Fix by 25 April"* → 0. *"When a fourth query needs the predicate, or
when we add the notification worker, whichever is first"* → 0.5.

**Quadrant errors to watch for**, because they are systematic:

- Everything marked **prudent/deliberate**, including things they plainly did not decide. **Prudent/inadvertent is the honest label for most of a student project** — you could not have known in Week 1 what you knew in Week 9 — and a register with no inadvertent items is a register that is posturing.
- **Reckless/deliberate used as self-flagellation.** It has a precise meaning — knowing better and choosing the mess — and *"we wrote it badly because we were tired"* is closer to reckless/inadvertent. **Accept either with a reason.**

### The register as a whole [14]

| | |
|---|---|
| **5** | **Three or more non-code items** |
| 4 | Items in three different quadrants, with a reckless/deliberate one declared if present |
| 3 | Ordered by interest, ordering defended in a sentence |
| 2 | Issue numbers that exist |

**The 5 marks for non-code items are the cap's mechanism** — check them against L34 §7's list. **Common
good ones:**

| Item | Kind |
|---|---|
| *"Our mutation score on the app layer is 34%; the suite would ship a regression there"* | **Test debt** — and it is the best available answer |
| *"Only one of us has deployed to staging"* | **Process debt** |
| *"The hold-expiry rule is documented nowhere; three of us learned it verbally"* | **Documentation / knowledge debt** |
| *"We are on SQLAlchemy 2.0.4; 2.0.31 is current and the upgrade is now untested"* | **Dependency debt** — and full credit for noting it accrues while they sleep |
| *"Bookings created before our Week 6 migration have `NULL` in `expires_at` regardless of state"* | **Data debt** — the rarest and most impressive find |

**Apply the 75 cap** if fewer than three are non-code.

---

## Q3: Four Things You Will Not Repay (20)

**4 + 4 + 4 + 5 + 3.**

| | |
|---|---|
| 4 | **Nothing touches it** — **with the touch count.** No count → 1 |
| 4 | **Repayment riskier than the debt** — **and what they would repay first** |
| 4 | **About to ship** — with what they would do in a nonexistent Week 14 |
| 5 | **One they *will* repay, with the arithmetic** |
| 3 | A change-of-mind condition for one of the first three |

**The second category's model answer**, and it is W9's argument returning: *"we will not restructure
`confirm()` — it has 6 tests and 41% branch coverage, so we cannot tell if we broke it. **We will
repay the test debt first**, then reconsider."* **That is exactly right and should score 4 with a
note.**

**The fourth category [5] needs real arithmetic:** cost to fix in hours, cost of not fixing before the
demo, and why it wins. *"Two hours to add the seed script; without it the demo runs against an empty
database, which is 8 of the 30 presentation marks"* → 5. *"We will fix the naming because it bothers
us"* → 1.

**The change-of-mind condition [3]** is the falsifiability mark, and it is the same habit A 3 Q5(b)
rewarded. **0 for "if we had more time".**

---

## Q4: Metrics, Read Honestly (20)

### (a) [8]

**2 per metric, and a single value scores 1.**

| Metric | Expected shape |
|---|---|
| Mutation score (domain) | Should have risen since Week 6 — A 6 fixed three gaps |
| Pipeline time | Often **risen** since Week 8 as tests were added. **A rise honestly reported and diagnosed is worth full marks** |
| Cycle time | Usually much longer than they expect |
| Their choice | Anything, with two points in time |

**Award the full 2 for a metric that got worse and is explained.** The paper asks for direction, not for
good news, and a team reporting *"pipeline 90 s → 4 min, because the integration suite tripled and we
have not parallelised"* has done better work than one reporting a flat number.

### (b) [6]

| | |
|---|---|
| 3 | A measure identified that they optimised |
| **3** | **An honest yes, with the specific thing they did** |

**Honest confessions seen in previous cohorts, and all should score 3:**

- *"We added four tests to `schemas.py` in Week 6 to get coverage over 70%. They assert that Pydantic works."*
- *"We closed cards at the end of the fortnight by splitting one card into three."*
- *"Two of us made small commits to make the contribution graph look even."*
- *"We put `# pragma: no cover` on the error branch in `confirm` because it was awkward to trigger."* **The best one — it is L19 §4's exact prediction.**

**A "no" scores 3 only with evidence of having checked**: a number they let get worse, a pragma they
refused to add, a card they left open. **A bare "no" scores 0**, and the feedback should say why —
everyone optimises what is measured, and claiming otherwise means they have not looked.

### (c) [6]

| | |
|---|---|
| 2 | The MI value reported |
| 2 | **The argument against it, using L35 §2's three objections** |
| 2 | **What goes on the register instead** |

**The three objections:** arbitrary weights fitted to 1991 C code; Halstead volume barely meaningful
for modern languages; **and the decisive one — a single composite number cannot be acted on.** There is
no such thing as fixing the maintainability index.

**The replacement [2]** must be actionable about that module: *"instead of 'MI 14', the register says
'`booking_service.confirm` has complexity 19, 6 tests and 41% branch coverage on the module our
`git log` says we touch most' — which names three actions."* → 2.

---

## Q5: Documentation, Tested (10)

### (a) [6]

| | |
|---|---|
| 3 | An ordered list of sticking points **with elapsed times** |
| **3** | **Which of them they already believed were documented** |

**The gap is the mark.** *"They spent 6 minutes on the `.env` file. I would have said that was
documented — it is in the README, on line 40, below the API examples."* → 3. **That is a real finding
about where documentation *is* versus where it is *read*.**

**Deduct 3** for a test with no times, or run on a teammate. **The instrument is a stranger**; a
teammate shares the blind spots, which is the whole point of W7's pairing.

**Typical results worth recognising:** 8–20 minutes to a running system for a well-documented project;
**over 30 minutes or a failure means the README is wrong**, which is 12 marks of the Phase 1 rubric and
will be again on Demo Day.

### (b) [4]

4 for a machine-checked documentation artefact with a green run. **The README quickstart in CI is worth
the most** and is the expected answer.

**2** for a doctest or a tested example that does not cover the quickstart. **Accept an OpenAPI
regeneration check, a link checker, or a test asserting the ADR directory has no numbering gaps** — the
last is unusual and shows they understood the principle rather than copying the example.

---

## Overall Bands

| Band | |
|---|---|
| **90–100** | Hotspot correctly identified as the intersection. A change coupling interpreted, benign or otherwise. A bus factor named and its 1 May consequence faced — **and appearing on the register as process debt.** Eight-plus items, three-plus non-code including a data- or dependency-debt find, real interest evidence, triggers not dates, ordered and defended. Four honest non-repayment cases with arithmetic and a change-of-mind condition. Four trends including one that got worse. **An honest Goodhart confession.** An onboarding test with times and the believed-documented gap |
| **75–89** | Analysis run and interpreted. Register complete, correctly formatted, with non-code items. Non-repayment reasoned. Trends reported. Onboarding test done properly |
| **60–74** | Numbers without the intersection. Register is code smells with dates (capped at 75). Non-repayment is "no time". Values not trends. Goodhart "no" without evidence |
| **45–59** | Register under eight or uncommitted (capped at 55). No hotspot analysis. Onboarding test on a teammate |
| **< 45** | No `docs/debt.md` |

**Feedback note for every paper:** name the one register item you think they have under-priced, and
say why. **The final report's debt section is marked again in May**, and a student who has had one
priority challenged writes a much better version.

**Cohort note after marking:** publish, anonymised, the **count of honest Goodhart confessions** and
two or three examples. **It is the single most effective thing you can do for next year's cohort** —
students believe that gaming a metric is unusual until they learn that a third of the room did it.

---

*CS 212 · Week 11 · A 11 marking guidance · INSTRUCTOR ONLY*
