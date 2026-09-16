# CS 212 · Team Charter — Template
## Copy to `docs/charter.md` in your repository, fill in, commit before Friday of Week 1

---

> **Why this exists.** Every disagreement your team will have in April is a disagreement you could
> have had cheaply in January. This document is where you have them cheaply.
>
> **It is not marked on its own.** It is 5 of Phase 1's 100 marks, and it is referenced by A 12,
> which asks what in it turned out to be wrong. **A charter that was never wrong about anything was
> not specific enough to be wrong.**

---

## 1. Team

| Name | GitHub handle | What you are most confident doing | What you want to get better at this term |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

**The fourth column is the point of the table.** A team that assigns every task to whoever is already best at it produces a good project and four people who learned nothing. **Assign at least one thing per person from column 4.**

---

## 2. Definition of Done

A change is **done** when — *complete this list, and do not change it after Week 1:*

- [ ] It is on a branch, in a pull request
- [ ] **Reviewed and approved by a teammate who did not write it**
- [ ] All tests pass in CI, not just locally
- [ ] Lint and type-check pass
- [ ] No `TODO`, no commented-out code, no debug print in the diff
- [ ] *(your additions:)*
- [ ]
- [ ]

**The three unchecked lines are the ones that make this yours.** Candidates: a test that fails before the change and passes after; documentation updated in the same PR; a migration that has been run backwards at least once.

---

## 3. Work in Progress

**Our WIP limit is: ______ items in "In Progress" at once.**

Little's Law says $W = L/\lambda$: with throughput roughly fixed, the number of things in flight sets how long each one takes (L02 §7). A five-person team that starts five things finishes them all at the end. **Pick a number below your team size and justify it in one sentence:**

> *Because:*

---

## 4. Roles, and How They Rotate

| Role | What it means | Iteration 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| **Backlog owner** | Decides the order of the board. **One person, not a committee** | | | | | | |
| **Release manager** | Owns the pipeline that fortnight; fixes it when it breaks | | | | | | |
| **Scribe** | Runs and writes the retrospective | | | | | | |

**Everybody writes code every iteration**, including the backlog owner. These are duties, not job titles.

---

## 5. How We Communicate

| Question | Our answer |
|---|---|
| Where do decisions get made? | |
| Where do they get **written down**? | |
| How long before an unanswered message gets escalated? | |
| When do we meet, and for how long? | |
| **What happens when someone goes quiet for a week?** | |

**The last row is the one that matters** and it is the one every team leaves vague. Write the actual sequence: who contacts them, after how long, and at what point the instructor is told. **Deciding this in Week 0 costs nothing. Deciding it in Week 9, about a specific person, costs the team.**

---

## 6. How We Disagree

Two technical disagreements per term is normal and healthy; the failure mode is not having them, and the second failure mode is having the same one four times.

**Our rule:**

> *When we cannot agree on a technical decision after ______ minutes of discussion, we:*
> *(examples: the backlog owner decides; we timebox a spike and let the result decide; we write both
> options as an ADR and pick the one with the cheaper reversal)*

**Whatever you choose, the outcome gets written as an ADR** (Week 3), including the option you rejected. The rejected option is the part that is worth something in eight weeks when someone asks why.

---

## 7. What We Are Deliberately Not Doing

List three things a booking system could have that **you are choosing not to build**, with a reason for each.

| Not building | Because |
|---|---|
| | |
| | |
| | |

**This is the hardest section and it is worth writing carefully.** Two-thirds of delivered features are rarely or never used (L02 §5). The skill is deciding which third yours is in, before you build it rather than after.

---

*CS 212 · Team Charter template · commit as `docs/charter.md` before Friday of Week 1*
