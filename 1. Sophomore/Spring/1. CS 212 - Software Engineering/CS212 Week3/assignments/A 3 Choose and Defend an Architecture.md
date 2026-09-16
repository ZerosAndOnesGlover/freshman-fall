# CS 212 · Assignment 3
## Choose and Defend an Architecture for the Team Project

---

**Released:** Week 3, Wednesday 17:00 · **Due:** Week 4, Friday 17:00
**Total: 100 points** · Submit a PDF, `A3_{LastName}_{StudentID}.pdf`, **plus ADRs committed to your team repository**

> **Individual paper, team subject.** Your team makes one architecture decision; you each write your
> own defence of it — **or your own argument against it.** Q5 exists for the second case and there
> is no penalty for taking it.
>
> **Two deliverables are in the repository, not the PDF**: the ADRs (Q2) and the import test (Q3).
> Both are also Phase 1 artefacts, so this assignment is three weeks of Phase 1 work done early.

---

### Q1: Rank, Then Choose (20 points)

**(a) [6]** Rank the seven quality attributes from L10 §3 for `slot`, most important first. **For each of the top three, name the requirement or constraint that puts it there** — not a general preference. *"Testability, because we expect ~200 tests by May and a container-backed suite measured 1.2 s per module in our spike"* is the standard.

**(b) [6]** **Name one attribute you are deliberately ranking low, and what you are giving up.** Say what would have to change about `slot` for it to move up. **A ranking with no sacrifice in it is not a ranking.**

**(c) [8]** State the architecture your team has chosen, in one paragraph a reader outside the team could follow, and **map it back to (a)**: for each of your top three attributes, name the specific structural feature that serves it.

---

### Q2: Four ADRs (25 points)

**Write four Architecture Decision Records** in Nygard's format (L10 §5) and **commit them to `docs/adr/` in your team repository.** Numbered, dated, with Status, Context, Decision, Consequences and Alternatives Considered.

**They must cover, at minimum:**

| # | Subject |
|---|---|
| 1 | **The `Slot` representation** — fixed duration or interval. W1 L06 §3 is the argument; this is where you settle it |
| 2 | **Where the no-double-booking invariant is enforced**, and why the other four candidates from L10 §6 fail |
| 3 | **The overall shape** — layered, hexagonal, modular monolith, or otherwise |
| 4 | **Your choice** — one your team actually argued about |

**Marked as follows, per ADR [5 each], plus 5 for the set:**

| | |
|---|---|
| 1 | Context states a real situation, with a number or an observation in it |
| 1 | Decision is specific enough to be violated |
| **2** | **Consequences include negatives** — at least two per ADR, concrete |
| 1 | Alternatives considered, **with why each lost** |
| +5 | **The set:** they are consistent with each other, and at least one references another by number |

> **The negatives carry the marks.** An ADR with only upsides is marketing and scores 3 of 5 at
> best. The minus lines are what makes the file useful in March, and they are the first thing every
> team leaves out.

---

### Q3: Enforce One Boundary (15 points)

**(a) [8]** **Add the architecture test to your repository** (L11 §1) — or an equivalent that a machine runs. It must fail if a forbidden import appears in the layer you have protected. **Show the test, show it passing, and show it failing** (add a deliberate violation, capture the output, remove it).

**(b) [4]** **Wire it into CI** so it runs on every push. Link the green run.

**(c) [3]** Name **one other architectural rule your team has that no machine checks**, and say either how you would check it or why you cannot. *(Candidates: "reads may skip layers, writes may not"; "no module imports from inside another module's package"; "every mutating endpoint is idempotent".)*

---

### Q4: Where the Invariants Live (20 points)

**(a) [10]** Take your domain model's invariants — at least four (W1 L06 §4). For each: **where it is enforced, and why the narrower and wider options are wrong.** Use L10 §6's table shape.

**At least one must be in the database and at least one must not.** If your model genuinely has none of the second kind, say so and explain what that tells you.

**(b) [6]** **Write the DDL** for the database-enforced ones, and **demonstrate that it works**: two concurrent transactions, one of which fails. Show the session transcript.

```
-- Session A                         -- Session B
BEGIN;                               BEGIN;
INSERT ... ;                         INSERT ... ;   -- blocks, then fails
```

**(c) [4]** **Show the translation.** Where does the database error become a domain concept, and where does the domain concept become a 409? Two code excerpts, and one sentence on why the domain layer must not raise `HTTPException`.

---

### Q5: The Case Against Your Own Architecture (20 points)

**(a) [8]** **Make the strongest case against the shape your team chose.** Not a token caveat — the argument a sceptical reviewer would make. If you chose a modular monolith, the case for hexagonal; if hexagonal, the case that you have bought ceremony for a benefit you will not use; if anything else, the case for the modular monolith.

**(b) [6]** **What would show that you were wrong, and when?** Name the observable and the week. *"If by Week 9 our domain tests still need a database, the import rule bought us nothing"* is the standard. **It must be checkable before the final report**, because the report asks.

**(c) [6]** L12 §5 gives two questions to ask anyone proposing microservices. **Answer them honestly for your own chosen architecture** — whatever it is. *What are you buying, and who is the customer? What does being wrong about the boundary cost?*

**If the honest answer to the first is "nobody" or "it felt right", say so.** L12 §6 rates *"we didn't really decide"* above a retro-fitted justification, and this question is marked the same way.

---

## Marking

| Band | |
|---|---|
| **90–100** | Q1(b) names a real sacrifice. ADRs have specific negatives and cross-reference each other. Q3 shows the test failing. Q4(b) has a real concurrent transcript. Q5(b) commits to a falsifiable observation with a week number |
| **75–89** | Ranking justified, four sound ADRs, test in CI, invariants correctly placed with DDL. Q5 makes a real case |
| **60–74** | Ranking is preference, not evidence. ADRs have thin or absent negatives. Invariant placement right but undefended. Q5 is a caveat |
| **45–59** | ADRs are a decision with no context and no alternatives. No test. Invariants listed without placement |
| **< 45** | No ADRs in the repository. Architecture asserted, not chosen. Q5 absent or agreeing |

**One automatic cap: ADRs not committed to the repository cap the paper at 60.** They are a Phase 1 artefact, they are worth nothing in a PDF, and the point of them is that they live next to the code.

---

*CS 212 · Week 3 · Assignment 3 · 100 points · due Friday of Week 4, 17:00*
