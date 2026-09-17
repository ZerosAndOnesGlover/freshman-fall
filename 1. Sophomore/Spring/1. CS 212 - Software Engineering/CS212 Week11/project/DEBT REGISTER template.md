# `slot` · Technical Debt Register
## Copy to `docs/debt.md`. Ordered by interest, highest first.

---

> **Why this file exists.** A debt item that is not written down is not debt — it is a feeling. This
> register is required by the project brief's report section, it is written in A 11, and **the final
> report is marked on its honesty rather than on its shortness.** A team with eight well-reasoned
> items scores above a team claiming none, because the second team either has not looked or is not
> saying.
>
> **Ordered by interest, not by severity.** Interest = how bad × how often you touch it (L34 §3), and
> the second factor is in your `git log`. **Terrible code nobody touches costs nothing.**

---

## How to fill this in

**Quadrant** (L34 §2) — and it determines the response:

|  | **Reckless** | **Prudent** |
|---|---|---|
| **Deliberate** | Not debt. It is choosing a mess while knowing better | ✅ **Cunningham's.** Needs a trigger and an estimate |
| **Inadvertent** | An education problem. Fix the review practice, not the code | ✅ **The most common and most honest.** Prioritise by interest |

**Trigger, not a date** (L34 §5). *"Fix by April"* does not survive contact with April. A **condition**
fires when the cost is actually being paid, which is when repayment is cheapest and the argument
strongest.

**Not only code** (L34 §7). At least three of your items should be **test, documentation, API,
process, dependency, data or knowledge** debt. A register of eight code smells is a smell list.

---

## D-01 · <short title>

**Quadrant:** prudent / deliberate
**Recorded:** YYYY-MM-DD · **Owner:** <role, not a name — roles survive>
**Issue:** #NN

**What.** *Specific enough that a stranger could find it. Name the file, the function, the endpoint.*

**Why we took it on.** *Without this, a later reader assumes incompetence. This sentence is what
distinguishes debt from mess.*

**Interest.** *Evidence, not adjectives. How many places must remember this? How many times has
someone forgotten? What did it cost last time?*

**Trigger to repay.** *A condition.*

**Estimated repayment.** *So the trade is arithmetic.*

---

## D-02 · <short title>

**Quadrant:** prudent / inadvertent
**Recorded:** · **Owner:** · **Issue:**

**What.**

**Why we took it on.** *For an inadvertent item this becomes "what we did not know then" — which is
not an apology. You could not have known in Week 1 what you knew in Week 9.*

**Interest.**

**Trigger to repay.**

**Estimated repayment.**

---

## Items we are deliberately NOT repaying

*L34 §6. Four reasons, and A 11 Q3 asks for one of each. Recording a decision not to act is worth as
much as recording one to act.*

| # | Item | Why not | Would change if |
|---|---|---|---|
| D-.. | | **Nothing touches it** — *touch count:* | |
| D-.. | | **Repayment riskier than the debt** — *we would repay ___ first* | |
| D-.. | | **We are about to ship** | |

---

## Non-code debt — at least three

*The debt that sinks projects is rarely in the code.*

| Kind | Prompt |
|---|---|
| **Test debt** | A suite that passes and would not notice a regression. **Your mutation score is the measurement** |
| **Documentation debt** | The invariant nobody wrote down. The `README` step that is not in the `README` |
| **API debt** | A field you cannot remove because you do not know who reads it |
| **Process debt** | **Something only one person can do.** A deploy, a migration, a release |
| **Dependency debt** | **The only kind that accrues while you sleep**, and whose cost grows super-linearly |
| **Data debt** | A column meaning two things; rows in a state the code no longer produces |
| **Knowledge debt** | **One person understands X.** A bus factor of 1 |

---

## Trend

*L35 §5. A score invites a target; a trend implies an action.*

| | Week 6 | Week 8 | Week 11 | Direction |
|---|---|---|---|---|
| Items open | | | | |
| Items closed since | — | | | |
| **Net** | | | | **Are you accruing faster than you repay?** |

---

*`slot` · debt register · required by the project brief · written in A 11*
