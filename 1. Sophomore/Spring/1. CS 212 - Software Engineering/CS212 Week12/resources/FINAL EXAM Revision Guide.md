# CS 212 · Final Exam Revision Guide
## Friday 8 May, 09:00–11:30 · 150 minutes · 100 marks

---

**Comprehensive: Weeks 0–12.** **Weeks 11 and 12 appear here and nowhere else** — there was no Quiz 12,
and the midterm stopped at Week 5.

**One A4 sheet of your own handwritten notes, both sides.** **Preparing it is the single best revision
exercise available**, and you keep it.

---

## 1. How to Revise This Course in Six Hours

**Not by rereading thirty-nine lectures.** In this order:

| # | | Time |
|---|---|---|
| 1 | **The eleven quiz answer keys.** They cover Weeks 0–10 and are the most compact material in the course | 90 min |
| 2 | **The "what to reread" table at the end of each quiz.** List every section you were sent to **more than once** — those are the load-bearing sections | 20 min |
| 3 | **The thirteen `summary.md` files.** One paragraph per week, and they are written to be read in sequence | 60 min |
| 4 | **Weeks 11 and 12's lectures properly**, since nothing else has examined them | 60 min |
| 5 | **Build the A4 sheet** — §4 | 90 min |
| 6 | **Write one essay plan** for each of the three Section C options, in bullets | 40 min |

**Step 2 is the highest-value twenty minutes.** The sections you were sent back to repeatedly are the
ones the exam's essays are built on.

---

## 2. What the Paper Looks Like

| Section | Marks | Shape |
|---|---|---|
| **A** | 30 | **Ten short answers, 3 marks each.** Two or three sentences. Definitions, rules, and one formula |
| **B** | 40 | **Three applied questions.** One cross-week synthesis, one code review, one set of numbers to interpret |
| **C** | 30 | **One essay of three**, 700–900 words |

**Six questions in the paper are contested positions**, and the paper says so. **A defended
disagreement scores full marks.**

**Where a question says "with a number" or "with evidence", an answer without one is capped at half.**
**Every figure you might need is on the paper's *Given facts* table** — so nothing depends on
memorising `roomsvc`'s line count.

---

## 3. The Ten Things Section A Will Ask About

**Not a leak — these are simply the course's definitional core, and there are only about ten.**

| # | | Week |
|---|---|---|
| 1 | **The refactoring test**: if a test had to change, it was not a refactoring | W9 |
| 2 | **Where an invariant is enforced**: the narrowest point every path must pass through | W3 |
| 3 | **Hyrum's law**, and the `roomsvc` ordering instance | W10 |
| 4 | **CI's two load-bearing words**, and the two-command test | W8 |
| 5 | **Coverage against mutation score**, and which controlled for which | W6 |
| 6 | **SRP's "one actor" form**, and why it beats "one thing" | W2 |
| 7 | **Characterisation tests**, and the mandatory comment | W9 |
| 8 | **Interest = badness × touch frequency** | W11 |
| 9 | **The four severity labels** | W7 |
| 10 | **Why documentation rots structurally** | W11 |

**Learn these ten as sentences you can write in twenty seconds each.** That is 30 marks.

---

## 4. Building the A4 Sheet

**You cannot fit the course on it, so the exercise is choosing.** What actually helps:

| Put on it | Leave off |
|---|---|
| **The Liskov compatibility table** — allowed against forbidden API changes | Anything on the *Given facts* table |
| **Fowler's debt quadrant**, 2×2 | Long prose you will not have time to read |
| **The five kinds of coverage**, and the six REST constraints | Lists you already know cold |
| **Cohesion and coupling ladders**, worst to best | `roomsvc`'s numbers — they are provided |
| **The five Goodhart appearances** | |
| **The six-step branch-by-abstraction sequence** | |
| **Knight Capital's five failures** | |
| **Bacchelli & Bird's four percentages**, and Cisco's two thresholds | |
| **Your three essay plans, in six bullets each** | |

**The essay plans are the best use of the space.** Section C is 30 marks and the difference between a
planned and an unplanned essay is larger than anything else on the sheet.

---

## 5. Section B: What Each Question Rewards

**B1 — one mechanism, three literatures.** The mechanism is **batch size**. You need what each of the
three found *and* **why the mechanism produces the result differently in each** — small reviews fit in
working memory; small TDD steps localise the cause of a red test; small deploys give one suspect
instead of two hundred. **Then a confound all three might share**: all three are observational, and all
three plausibly measure *teams that are already disciplined*.

**B2 — the code review.** Act on **size, title and description before reading code** (W7 L23 §2, pass 1).
Then the diff: **moving `notify` out of the transaction is a behaviour change, not a refactoring**, and
**the passing tests are not evidence because nothing tested the rollback path.** The reconciliation in
(c): **the change is right and the process is wrong** — it belonged in its own commit, with a test for
the new behaviour, not inside a 640-line PR titled *"refactor + fix"*. **The two hats** (W9 L28 §4).

**B3 — the numbers.** The one that is **not** a problem is the 1,400-line domain package. **91% against
38%** means assertionless tests and route-asserting tests — **survivor types 1 and 2** (W6 L21 §3). And
the wrong plan: **you do not raise a mutation score as a target** (Goodhart), and **the eleven-day
branch and the eleven-minute pipeline are more urgent** than either number.

---

## 6. Section C: What Each Essay Needs

**All three want: a position, evidence used precisely, and the strongest objection to your own position
addressed.** An essay making two points well beats one listing six.

**C1 — the evidence is weaker than the confidence.** Four of: the TDD replication (no effect of
test-*first*), Inozemtseva & Holmes (**controlled for suite size**), Just et al. (**357 real faults,
controlled for coverage**), the Fagan-to-PR transfer, DORA (self-reported, correlational), Project
Aristotle (one organisation), the maintainability index (**1991 weights, unactionable**). **Then the
four disowned originators** — and the answer wanted is about the *transmission mechanism*: the
memorable name travels and the caveats do not, so a practitioner's job is to **read the primary source
and ask what population it studied.**

**C2 — Goodhart.** Four of the five appearances. **The objection that makes it hard is real**: two
thousand engineers cannot manage by reading individual findings. **The strongest answer distinguishes
*aggregate for allocation* from *target for reward***, and reaches for the **ratchet** — *this may not
get worse* — plus Google's diff-scoped approach, where the aggregate is never the thing anyone is
measured on.

**C3 — twelve lines, four months.** Account for the four months without invoking incompetence: 487
lines, eleven tests, 94 paths, an author who left in 2023, **and nobody able to convince themselves the
change was safe.** Then the interesting half: **which week would have made no difference?** Defensible
answers include W4 (patterns), W10 (versioning — it is an internal function), W12 — **and the best
answers argue that W6's mutation testing would have *diagnosed* it and W9's characterisation tests would
have *fixed* it, while several weeks were irrelevant to this particular failure.** Then the cost
question: **a defensible "sometimes not worth it" scores as highly as "always"**, and the conditions are
short-lived code, a single author who stays, and a system nobody else depends on.

---

## 7. Cross-Week Connections the Paper Rewards

**Section B and C both reward noticing that the course has a small number of ideas appearing repeatedly.**

| The idea | Where |
|---|---|
| **Batch size** | Review size (W7), TDD's small steps (W5), deployment frequency (W8), small commits (W9) |
| **Goodhart's law** | Coverage (W6), review (W7), deploys (W8), deprecations (W10), everything (W11) |
| **A signal generated and never read** | Flaky tests (W5), dismissed lint rules (W7), an unread sweep (W8), 17 deprecations (W10) |
| **What changes together?** | Cohesion (W2), SRP's actor (W2), Parnas (W2), separation of concerns (W2), change coupling (W11) |
| **Liskov** | SOLID's L (W2), API compatibility (W10) |
| **Expand and contract** | A database column (W8), a component (W9), an API field (W10) |
| **A cheap fallible signal, not a verdict** | Coverage (W6), lint findings (W7), smells (W9), all metrics (W11) |
| **Originators disowning their ideas** | Agile (W0), Fagan (W7), Fielding (W10), Cunningham (W11) |
| **Make the check and the act indivisible** | The invariant (W3), and CS 202's Week 3 |

**Any Section C essay improves substantially by using two rows of that table.**

---

## 8. Practicalities

| | |
|---|---|
| **When** | Friday 8 May, **09:00–11:30**. Arrive 08:45 |
| **Where** | Posted on the portal in the last week of term |
| **Bring** | Pens, and **your one A4 sheet, handwritten, both sides** |
| **Timing** | ~75 seconds per mark. **Section A in 35 minutes, B in 55, C in 45**, 15 to read and check |
| **Do not** | Spend 50 minutes on Section A. It is 30 marks of two-sentence answers |

**One instruction worth following:** **read Section C first, decide which essay, then do A and B.** Your
essay choice will sit in the back of your mind while you answer the short questions, and two of the
Section B questions supply material for it.

---

*CS 212 · Final Exam Revision Guide · 8 May*
