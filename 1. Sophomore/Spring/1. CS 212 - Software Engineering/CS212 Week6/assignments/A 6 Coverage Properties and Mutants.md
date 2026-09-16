# CS 212 · Assignment 6
## Raise Coverage, Then Break It With Mutation Testing

---

**Released:** Week 6, Wednesday 17:00 · **Due:** Week 7, Friday 17:00
**Total: 100 points** · Submit a PDF, `A6_{LastName}_{StudentID}.pdf`, plus **tests committed to your team repository**

> **This is the lightest assignment of the term, deliberately.** It is released on the evening of the
> midterm and the day after Phase 1. **Most of it is running three tools on code you already have
> and reading the output carefully.**
>
> **The reading is the work.** Q2 and Q3 are worth 55 of the 100 marks and neither requires you to
> write much code — they require you to look at ten survivors and say, honestly, what each one means.

---

### Q1: Two Numbers, Honestly (15 points)

**(a) [5]** Turn on **branch coverage** and report both numbers for your project — line and branch — with the command and the date. **Report the lower one as your headline.** Then name the file with the biggest gap between the two, and say what kind of code lives there.

**(b) [5]** Run `coverage report --sort=cover`. **Read it the way L19 §5 says**: the bottom first, then the top against change frequency, then `BrPart`.

- Name one file with **high** coverage that this tells you nothing about, and why.
- Name one file with **low** coverage that does not matter, and why.
- Name one file with low coverage that **does**, with its change count from `git log`.

**(c) [5]** List every `# pragma: no cover` in your repository. For each: why it is there, and whether it should be. **If you have none, say so** — and check `.coveragerc` / `pyproject.toml` for `exclude_lines`, which is the same thing wearing a different hat.

---

### Q2: Ten Survivors (30 points)

**Run mutation testing on your domain and application packages.** Configuration in L21 §6; expect it to take a while, so start it before you write anything else.

**(a) [5]** Report: mutants generated, killed, survived, timed out, and the score. Command and date.

**(b) [20]** **Take ten survivors in code that matters** and classify each:

| Survivor | File:line | Mutation | Classification | What it means |
|---|---|---|---|---|

**Classifications:** **real gap** (a bug your suite would ship), **equivalent** (behaviour unchanged — *prove it, in a sentence*), or **deliberate** (untested on purpose — say why, and it must be in your debt register).

**2 marks each.** A row scores 2 only if the *"what it means"* column says something specific. *"We need more tests here"* scores 0.

**(c) [5]** **Fix three of the real gaps.** Show the tests, show the mutants now killed. **If you found fewer than three real gaps in ten survivors, say so and take ten more** — and if your sample really is mostly equivalents, that is an interesting result and you should say what it suggests about your suite.

---

### Q3: Three Properties (25 points)

**(a) [8]** Write a **round-trip property** for something in your project — a `Slot`, your booking JSON, an iCal export, a URL parameter. Show the property, show it passing, and say how many examples it ran.

**[+3 within this mark]** if it **fails** the first time and you report the shrunk counterexample. **This happens more often than not**, and a failure found here is worth more than a passing test.

**(b) [8]** Write the **refuses-or-is-correct** property (L20 §2) for your main domain function.

**(c) [9]** Write a **`RuleBasedStateMachine`** for your booking lifecycle, with at least three rules and **one `@invariant`**.

- **[6]** It runs and the invariant holds.
- **[3]** **State what it cannot find**, and why — L20 §6 says it directly, and the answer connects to A 5 Q1.

---

### Q4: The Two Papers (20 points)

**(a) [8]** **Inozemtseva & Holmes (2014)** found coverage correlates with test-suite effectiveness. **State precisely what they controlled for, and what happened to the correlation when they did.** Then say why the uncontrolled version is the one everybody quotes.

**(b) [8]** **Just et al. (2014)** used **357 real faults.** State what they measured and what they found about mutants versus coverage as a predictor. **Say specifically why "real faults" rather than "seeded faults" matters to the strength of the claim.**

**(c) [4]** **The two results together justify this course's marking rule** — that 95% coverage with a 30% mutation score scores below 70% with 75%. **State the argument in three sentences.** Then give **one honest objection** to the rule.

---

### Q5: What Your Numbers Do Not Say (10 points)

**(a) [6]** L21 §7 lists five things mutation testing cannot see. **Pick the two most relevant to `slot`** and say, concretely, what defect your project could currently ship that neither your coverage nor your mutation score would reveal.

**(b) [4]** L21 §7 also notes that a high score on a small trivial domain is easy. **Report your domain package's line count alongside your score**, and say honestly whether the score is impressive for that size.

---

## Marking

| Band | |
|---|---|
| **90–100** | Branch coverage on and the lower number reported as the headline. Ten survivors with specific meanings, including proven equivalents. A round-trip property that failed and was shrunk. The state machine's limitation correctly connected to A 5. Q4 states what each paper controlled for |
| **75–89** | All tools run and reported with commands and dates. Survivors classified correctly, three gaps fixed. Three properties working. Papers summarised accurately |
| **60–74** | Numbers reported without reading the distribution. Survivors listed with generic meanings. Properties present but one is a "does not crash". Papers paraphrased from the lecture |
| **45–59** | Coverage reported as a total only. Mutation run but not read. One property. Papers not opened |
| **< 45** | Tools not run, or run on `roomsvc` instead of your own project |

**One automatic cap: a paper reporting only line coverage caps at 70.** Branch coverage is one line of configuration, it is strictly more informative, and L19 §2 measures the difference at thirteen points.

---

*CS 212 · Week 6 · Assignment 6 · 100 points · due Friday of Week 7, 17:00*
