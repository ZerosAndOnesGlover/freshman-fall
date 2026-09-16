# CS 212 · Reading Guide · Week 6

---

> **Week 6 holds Phase 1 on Tuesday and the midterm on Wednesday.** The required reading below is
> deliberately short, and the two papers are the two you should actually read — they are the
> evidence for the one marking rule in this course that surprises people.

---

## Required

| # | What | Length | Why |
|---|---|---|---|
| 1 | **coverage.py documentation** — "Branch coverage measurement" | 10 min | One configuration line, thirteen points of difference on `roomsvc`. A 6 Q1 requires it |
| 2 | **Hypothesis docs** — "Quick start" and "What you can generate" | 30 min | Enough to write A 6 Q3's three properties |
| 3 | **Inozemtseva & Holmes**, *"Coverage Is Not Strongly Correlated With Test Suite Effectiveness"* (ICSE 2014) | ~12 pages | **Read the methodology section.** A 6 Q4(a) asks what they controlled for, and the answer is the paper's whole contribution |
| 4 | **Just et al.**, *"Are Mutants a Valid Substitute for Real Faults?"* (FSE 2014) | ~11 pages | **The paper that justifies marking your project on mutation score.** 357 real faults; read §4 |

**Papers 3 and 4 are the pair.** Read them together; the second is the answer to the gap the first opens. **Midterm essay C2 is exactly this pair**, so an hour here is an hour of revision.

---

## Recommended

| What | Why |
|---|---|
| **Petrović & Ivanković**, *"State of Mutation Testing at Google"* (ICSE-SEIP 2018) | How mutation testing is made usable at scale: mutate the diff, surface a few survivors in review, let reviewers mark them useless. **This is the shape your project should aim at** |
| **Wlaschin**, *"Choosing properties for property-based testing"* (fsharpforfunandprofit.com) | Where L20 §3's five patterns come from. Ignore the F#; the taxonomy is language-independent |
| **Hypothesis docs** — "Stateful testing" | Needed for A 6 Q3(c), and the best part of the library |
| **Marick**, *"How to Misuse Code Coverage"* (1997) | Nearly thirty years old and still the clearest statement of the Goodhart problem. Four pages |

---

## How to Read the Two Papers Quickly

You have a midterm tomorrow. **Twenty minutes each, done like this:**

**Inozemtseva & Holmes.** Abstract → then find the sentence about **controlling for suite size** → then the correlation figures before and after that control. **The whole result is: coverage correlates with effectiveness, and the correlation is explained by bigger suites both covering more and finding more.** Everything else is how they established it over 31,000 suites.

**Just et al.** Abstract → §2 for how they got **357 real faults** (from version-control history, with the fixing commit identified) → §4 for the result. **The claim: mutant kill rate predicts real-fault detection after controlling for coverage.** Note the words *after controlling for coverage* — that is the control the first paper showed coverage itself fails.

**Why "real faults" matters, and A 6 Q4(b) asks it:** most mutation research validates mutants against *seeded* faults, which is circular — you are checking that artificial bugs resemble artificial bugs. **Using faults that actually shipped and were actually fixed removes the circularity**, and that is why this paper carries weight that its predecessors do not.

---

## A Note Before the Midterm

**The paper has four questions where the lecture's own position is contested**, and it says so at the top. Those are, for the avoidance of doubt: **the evidence for TDD** (W5 L17 §3), **the SOLID scoreboard** (W2 L08 §6), **whether microservices are ever right for a small team** (W3 L12 §3), and **whether function length is ever the problem** (essay C3).

**A defended disagreement scores full marks on all four.** The revision that helps most is not re-reading the lectures — it is **deciding what you actually think about those four, and what evidence you would cite.**

---

*CS 212 · Week 6 · Reading Guide*
