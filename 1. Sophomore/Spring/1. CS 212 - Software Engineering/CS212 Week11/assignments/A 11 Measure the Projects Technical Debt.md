# CS 212 · Assignment 11
## Measure the Team Project's Technical Debt, and Write It Up

---

**Released:** Week 11, Wednesday 17:00 · **Due:** Week 12, Friday 24 April, 17:00
**Total: 100 points** · Submit a PDF, `A11_{LastName}_{StudentID}.pdf`, plus **`docs/debt.md` committed to your team repository**

> **⚠️ A 11 and A 12 are both due Friday 24 April**, the last teaching day, along with Problem Sets 11
> and 12 in every other course and CS 290's Position Paper 3. **A 12 is deliberately short. A 11 is
> not — start it this week.**
>
> **This assignment produces something the final report is marked on.** `docs/debt.md` is required by
> the project brief's report section, and A 11 is where you write it. **Nothing here is duplicated
> work.**

---

### Q1: The Hotspot Analysis (20 points)

**(a) [8]** Run the analysis on **your own project** (L35 §3):

```bash
git log --since='10 weeks ago' --name-only --format='' | grep '\.py$' | sort | uniq -c | sort -rn | head -10
radon cc -s -a src/
coverage report --precision=1 --sort=cover
```

**Produce one table** with, per file: touches, worst-function complexity, branch coverage. **Then name your hotspot** — the intersection — and say why it is the intersection rather than the worst on any single column.

**(b) [6]** **Change coupling.** Find the two files in your project that change together most often, and **say whether either imports the other.**

**[4 of the 6]** are for the interpretation: if they are coupled and neither imports the other, **the coupling is in the domain and a boundary is in the wrong place.** Say where you think it should be.

**(c) [6]** **Knowledge distribution.** `git blame` your hotspot by author and report the percentages. Then answer honestly:

- **Does any file have a bus factor of 1?**
- **What happens to your team on 1 May if that person is ill for a week?**

> `roomsvc`'s answer: **78% of `bookings.py`'s surviving lines were written by someone who left in
> 2023**, on the file that absorbs 41% of all change. **It is the most alarming number in the
> reference codebase and no static analyser will ever produce it.**

---

### Q2: The Register (30 points)

**Write `docs/debt.md` and commit it.** At least **eight** items, in L34 §4's format.

**Marked per item [2 each, 16 total]:**

| | |
|---|---|
| 0.5 | **Quadrant**, correctly assigned |
| 0.5 | **What** — specific enough that a stranger could find it |
| 0.5 | **Interest**, with evidence rather than adjectives |
| 0.5 | **A trigger**, not a date |

**Plus, for the register as a whole [14]:**

| | |
|---|---|
| **5** | **It is not only about code.** At least three of your eight must be from L34 §7's list — test, documentation, API, process, dependency, data or knowledge debt. **A register of eight code smells is a smell list, not a debt register** |
| **4** | **At least one item in each of three different quadrants**, and **if you have a reckless/deliberate item, say so** — it is the honest answer and it is marked as such |
| **3** | **Ordered by interest**, and the ordering is defended in a sentence |
| **2** | Each item has an issue number, and the issues exist |

---

### Q3: Four Things You Will Not Repay (20 points)

L34 §6 gives four reasons not to repay. **Find one item of yours for each.**

| | |
|---|---|
| **[4]** | One you will not repay because **nothing touches it** — with the touch count |
| **[4]** | One you will not repay because **the repayment is riskier than the debt** — say what you would repay first instead |
| **[4]** | One you will not repay because **you are about to ship.** State what you would do in the first week of a Week 14 that does not exist |
| **[5]** | One you **will** repay before 1 May, with the arithmetic: cost to fix, cost of not fixing before the demo, and why it wins |
| **[3]** | **Say what you would need to see to change your mind about any one of the first three** |

> **The fourth category is the important one and it is the last fortnight.** A team that spends it
> refactoring arrives with a cleaner codebase and fewer working features. **The report marks honesty
> about debt far above its absence** — and this question is the rehearsal for that section.

---

### Q4: Metrics, Read Honestly (20 points)

**(a) [8]** **Four numbers, as trends** (L35 §4–5): mutation score on the domain, pipeline time, cycle time, and one of your choosing. **For each: the value now, the value at an earlier point, and what the direction tells you.**

**A single value scores half.** The trend is the point.

**(b) [6]** **Goodhart, applied to yourselves.** L35 §1 lists five appearances of Goodhart's law in this course. **Pick one measure your team has actually optimised** — coverage, green builds, closed cards, commit count — **and say honestly whether you gamed it.** Describe the specific thing you did.

**[3 of the 6]** are for an honest yes. **A "no" is acceptable only with evidence that you checked** — a number you deliberately let get worse, a card you did not close, a `# pragma: no cover` you refused to add.

**(c) [6]** **The maintainability index of your worst module**, reported — and then **an argument for why it should not be on your register**, using L35 §2's three objections. Then say **what you would put on the register instead**, about the same module.

---

### Q5: Documentation, Tested (10 points)

**(a) [6]** **The onboarding test** (L36 §5). Hand your repository to somebody from another team. **Do not help.** Write down, in order, everywhere they got stuck, with the elapsed time.

**Then: which of those did you already believe was documented?** **That gap is the answer** and it carries 3 of the 6.

**(b) [4]** **Make one piece of your documentation machine-checked** (L36 §3). The README quickstart in CI is the obvious one and is worth the most. Show the diff and a green run.

---

## Marking

| Band | |
|---|---|
| **90–100** | Hotspot is the genuine intersection. A change coupling found with neither file importing the other, and a boundary proposed. A bus factor named and its consequence faced. Eight-plus items with real interest evidence and triggers, at least three non-code, ordered and defended. Four honest non-repayment cases with a change-of-mind condition. Four trends, not values. **An honest Goodhart confession.** An onboarding test with the believed-documented gap named |
| **75–89** | Analysis run and interpreted. Register complete and correctly formatted. Non-repayment reasoned. Trends reported. Onboarding test done |
| **60–74** | Numbers reported without the intersection. Register is eight code smells with dates instead of triggers. Non-repayment is "no time". Values rather than trends. Goodhart answered "no" with no evidence |
| **45–59** | Register under eight items or not committed. No hotspot analysis. No onboarding test |
| **< 45** | No `docs/debt.md` in the repository |

**Two automatic caps.** **`docs/debt.md` not committed → 55**: it is a report artefact and it is worth nothing in a PDF. **A register with no non-code items → 75**, because that is a smell list, and the debt that sinks projects is process, knowledge and dependency debt.

---

*CS 212 · Week 11 · Assignment 11 · 100 points · due Friday 24 April, 17:00*
