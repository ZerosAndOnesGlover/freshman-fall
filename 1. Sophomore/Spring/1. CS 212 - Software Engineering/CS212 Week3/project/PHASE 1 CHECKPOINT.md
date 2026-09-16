# CS 212 · Phase 1 Checkpoint
## Three weeks out — Week 3 of 6

---

**Phase 1 is presented Tuesday 3 March, Week 6.** You are at the halfway point. This file exists so
that a team can find out *now* that it is behind, rather than in the last fortnight.

**Full requirements:** [[CS212 Week0/project/PROJECT BRIEF slot|PROJECT BRIEF slot]] §3.
**Rubric:** [[CS212 Week6/project/PHASE 1 RUBRIC|PHASE 1 RUBRIC]].

---

## Where You Should Be

| Artefact | Due by | Status you should have now |
|---|---|---|
| `docs/charter.md` | Week 1 | **Done.** If not, it is twenty minutes and it is blocking Q5-type conversations |
| **Walking skeleton** | Week 1 | **Done, and deployed by CI.** If not, **stop reading and fix this** |
| `docs/domain-model.md` with invariants | Week 1–2 | Done, with an Invariants section naming where each is enforced |
| Stories on an ordered board | Week 1 | Ordered by someone, with acceptance criteria |
| `docs/adr/` — four ADRs | **Week 3–4** | **This week.** A 3 Q2 makes you write them |
| Architecture test in CI | **Week 3** | **This week.** A 3 Q3 makes you add it |
| `docs/retro-1.md`, `retro-2.md` | Weeks 2, 4 | One written, one due |
| **One booking end to end, with the invariant enforced** | Week 5 | Not yet — but the DDL should exist by Friday |
| `docs/retro-3.md` | Week 6 | |

---

## The Three Questions to Ask at This Week's Meeting

**1. Can a person who has never seen our repository run it?**

Not *"can we run it"*. Take fifteen minutes, hand your `README.md` to someone from another team, and watch. **Do not help them.** Write down where they get stuck. That list is real, it is short, and it is the difference between a demo that works and a demo that does not.

**2. Which of us has not committed in the last seven days?**

Ask it out loud, in the room, without accusation. The charter has a rule for this (§5, *"what happens when someone goes quiet"*), and **the rule exists so that asking is routine rather than confrontational.**

If the answer is someone: the failure is almost never unwillingness. It is usually that they cannot run the project, or do not know what to pick up, or picked up something too big three weeks ago and cannot admit it is stuck. **All three are fixable this week and none of them is fixable in April.**

**3. What have we built that nobody asked for?**

Go through the board. **For every card in progress or done, name who is worse off without it.** W0 L02 §5: ~2/3 of delivered features are rarely or never used. Your version of that statistic is being created right now, and this is the last cheap moment to look at it.

---

## The Two Most Common Week 3 Failures

**Parallel branches.** Four people, four long-lived branches, no merge for a fortnight. It feels productive and it is the integration crisis of April being pre-paid at interest. **Counter-measure: merge to `main` at least every two days, behind a flag if it is not finished.** If a branch has been open a week, it is too big.

**The domain belongs to nobody.** Conway's law (L10 §7): if two of you own "the API" and two own "the database", the rules end up in whichever layer needed them first, and you have built `roomsvc`. **Counter-measure: rotate ownership by feature slice, not by layer.** One person owns "cancellation, end to end" this fortnight.

---

## If You Are Behind

**In order. Do not do the second before the first.**

1. **The walking skeleton.** Everything else is worthless without it. An evening, four people, §6 of [[CS212 Week1/project/WALKING SKELETON|WALKING SKELETON]] has the split.
2. **One booking with the invariant enforced by the database.** This is the single artefact that most distinguishes a good Phase 1 from a bad one, and it is one migration and a caught exception.
3. **The four ADRs.** A 3 requires them anyway, so this is not extra work.
4. **The architecture test.** Twelve lines.
5. Everything else.

**Do not spend this week on the user interface.** No marks are given for CSS, it is the most visible work, and it is therefore the most tempting way to feel productive while the invariant is still unenforced.

---

*CS 212 · Week 3 · Phase 1 checkpoint · unmarked*
