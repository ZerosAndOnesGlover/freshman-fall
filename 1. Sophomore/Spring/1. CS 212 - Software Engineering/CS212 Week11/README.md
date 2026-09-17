# CS 212 · Software Engineering
## Week 11: Technical Debt, Metrics, Maintainability, Documentation

**Credits:** 3 · **Prerequisites:** PROG 102, CS 101
**Assessment for this course (overall):** Team Project 40%, Individual Assignments 30%, Midterm 15%, Final 15%
**This week's deliverables:** A 10 due Friday 17 April 17:00 · **A 11 released Wednesday** · **📊 Quiz 11 Tuesday — the last quiz**

> **A heavy Friday.** A 10 is due 17 April alongside **CS 202's Project 1**, **Problem Set 10 in every
> course** and **CS 290's Position Paper 2**.
>
> **And then Week 12 is heavier:** **A 11 and A 12 are both due Friday 24 April**, the last teaching
> day. **A 12 is deliberately short. A 11 is not — start it this week.**

---

### Why This Week Exists

Because you are eleven weeks in, your project has debts, and the final report asks you to be honest about them rather than to have none.

**The word has drifted almost beyond use.** Ward Cunningham's 1992 metaphor is two pages long and describes **a deliberate financing decision** in which the thing owed is **understanding** — code that does not yet reflect what you have since learned about the domain. His own clarification is explicit: *"I'm never in favour of writing code poorly, but I am in favour of writing code to reflect your current understanding of a problem even if that understanding is partial."*

**What the industry now calls technical debt is mostly just mess** — and calling mess "debt" is how it gets excused, because debt sounds like a decision somebody made on purpose.

**The week's most useful correction is that the principal barely matters.** What matters is the **interest**: how much it costs you per unit time to work around the thing. **Which means terrible code nobody touches costs nothing.** `roomsvc/legacy_import.py` is worse by every static measure than `calendar_sync.py`, and it is touched twice in two years, so paying it down would waste a day. **Interest = badness × touch frequency**, the second factor is in your `git log`, it requires no judgement — and most teams optimise the first because it is the one you can see by reading.

---

### Learning Objectives

By the end of Week 11, you should be able to:

1. State **what Cunningham actually said**, and say why calling mess "debt" excuses it.
2. Place an item in **Fowler's quadrant**, and say what each quadrant implies you should *do*.
3. Explain why **interest, not principal, decides priority** — and why untouched bad code costs nothing.
4. Write a **register entry** with all six fields, and say why *"why we took it on"* is what distinguishes debt from mess.
5. Explain why **a trigger beats a date**, and connect it to preparatory refactoring.
6. Name the **four times not to repay**, including the one that applies to you right now.
7. Name **seven kinds of non-code debt**, and say which one accrues while you sleep.
8. Give **five appearances of Goodhart's law** in this course, and the mechanism common to all of them.
9. Say what **cyclomatic complexity and the maintainability index** are good for and what they are not — and why the MI cannot be acted on.
10. Run a **hotspot analysis**, and explain why it beats every static measure.
11. Use **change coupling** to find a coupling in nobody's import graph, and **`git blame`** to find a bus factor of 1.
12. Say why **documentation rots structurally**, name the **six kinds a machine checks**, and run the **onboarding test.**

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L34 Technical Debt the Metaphor and Its Abuse]] | **What Cunningham actually said**, and what the phrase became; **Fowler's quadrant and what each implies**; **interest, not principal** — with the module that is worse and cheaper to ignore; **the six-field register entry**; **why a trigger beats a date**; **four times not to repay, including the last fortnight**; **seven kinds of non-code debt, and the one that accrues while you sleep** |
| [[L35 Metrics That Mislead and Metrics That Help]] | **Goodhart's law for the fifth time**, all five tabulated, with the mechanism that is never dishonesty; LOC, complexity, the maintainability index and velocity, rated; **hotspots — the one analysis worth more than the rest**; **change coupling, which finds what no import graph shows**; **the bus factor of 1 on the file absorbing 41% of change**; **trends rather than scores**; and what metrics cannot see |
| [[L36 Documentation That Survives]] | **Why documentation rots structurally** — a stale test fails, a stale README looks fresh; **four kinds with different half-lives**; **six kinds a machine checks**, including the architecture test as a statement that fails when it stops being true; **the four things that must be prose**, and the comment `roomsvc` needed and lacks; **the onboarding test** |
| [[CS212 Week11/project/DEBT REGISTER template\|DEBT REGISTER template]] | Copy to `docs/debt.md`. The quadrant table, the trigger rule, the non-code prompts, and a trend table |
| [[CS212 Week11/assignments/QUIZ 11 Week 11 Tuesday\|QUIZ 11]] | **The last quiz.** Seven questions on Week 10 — and a note on how to use all eleven for the final |
| [[CS212 Week11/assignments/A 11 Measure the Projects Technical Debt\|A 11]] | Five questions, 100 points, due Friday 24 April. **Produces `docs/debt.md`, which the final report is marked on.** Two automatic caps |
| [[CS212 Week11/resources/Reading Guide Week 11\|Reading Guide Week 11]] | **Cunningham's two pages first**; why Tornhill Ch. 4 is the valuable one; and an honest table of what this week is evidence *for* |
| `resources/metrics.sh` | Every metric in the week as one script — hotspots, change coupling, bus factor, traceability, deprecations |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A metric is a proxy, and optimising a proxy diverges from the goal exactly where the proxy is weakest.**

**Goodhart's law has now appeared five times in eleven weeks.** Coverage, gamed by testing the trivial modules and pragma-ing the hard ones. Review thoroughness, gamed by commenting on naming. Deployment frequency, gamed by splitting one change into six. Endpoints deprecated, gamed by marking seventeen things deprecated and removing none. And any metric on this week's list, gamed the moment somebody is rewarded for it.

**The mechanism is never dishonesty.** People find the divergence **because they are competent** — they are optimising exactly what you asked for, and what you asked for was the proxy.

**Which gives you the only defensible posture toward every number this course has produced: measure it, read it, act on individual findings, and never set a target on it.** Read ten mutation survivors, not the score. Read the top of the coverage report, not the total. Read the hotspot table, not the maintainability index. **The one legitimate target-shaped use is a ratchet — *this may not get worse* — which cannot be gamed because there is no prize for exceeding it.**

**And then the honest closing note, which is L35 §6.** Eleven weeks of measurement, and the single most important property of your system — **that it cannot double-book a room** — is verified by one integration test and one line of DDL, **neither of which appears in any metric you will report.**

---

### Assessment Reminder

**Quizzes carry no weight, and this is the last one.** **There is no Quiz 12.** Nothing covers Weeks 11 or 12 — they are examined only on the **final, Friday 8 May, 09:00–11:30**. Tracked in [[_CS 212 Quiz Record]].

**Assignments** released Wednesday 17:00, due Friday 17:00 of the week after; **lowest of thirteen dropped.** A 10 is due this Friday. **A 11 and A 12 are both due Friday 24 April.**

> **A 11's two caps.** **`docs/debt.md` not committed → 55**, because it is a report artefact and worth
> nothing in a PDF. **A register with no non-code items → 75**, because that is a smell list — and the
> debt that sinks projects is **process, knowledge and dependency debt**, not code smells.

**And the thing to internalise before the report:** **a register of eight well-reasoned items scores above a register of three, and above a claim of no debt.** A team claiming none has either not looked or is not saying.

---

### Connections

**Back:** **W6's coverage and mutation numbers become trends this week rather than scores**, and W6 L19 §4's Goodhart argument is generalised. **W9's interest rate** — *badness × touch frequency* — is L34 §3's formalisation of why A 9 asked students to choose a target by looking at the `git log`. **W2 L07 §7's "couple what changes together"** finally gets its measurement in change coupling. **W10's seventeen deprecations** are API debt, and the register is where they should have lived.

**Sideways:** **CS 202's Week 11 is distributed systems** — and its treatment of failure detection is the same epistemic problem as this week's metrics: **you are reasoning about a system from partial, delayed signals.** **MATH 251's Week 11** is hypothesis testing, which is the formal machinery behind "is this trend real or noise?"

**Forward:** **Week 12 is the last teaching week** — presenting engineering work, engineering management, career paths, and the dress rehearsal. **A 12 is the retrospective**, and it is built on the six `docs/retro-*.md` files and on this week's register. **Demo Day is Tuesday 28 April; the report and code are due Friday 1 May**, and its Debt section is A 11 expanded. **The final is Friday 8 May**, and Weeks 11 and 12 appear there and nowhere else.

---

*CS 212 · Week 11 · © CSE Department*
