# CS 212 · Final Examination
## Friday 8 May, 09:00–11:30 · 150 minutes · 100 marks · 15% of the course

**Name:** _________________________________ **Student ID:** ___________ **Team:** ___________

---

**Comprehensive: Weeks 0–12.** **Weeks 11 and 12 are examined here and nowhere else** — there was no Quiz 12.

**Closed book.** **One A4 sheet of your own handwritten notes is permitted**, both sides. Bring it; preparing it is the best revision available and you may keep it.

**Answer all of Sections A and B, and ONE essay from Section C.** Marks are shown. **Budget roughly 75 seconds per mark**, which leaves fifteen minutes to read and check.

> **How this paper is marked.** Every question asks for a judgement.
> **A defended position that disagrees with the lectures scores full marks**, and the paper contains
> **six** places where the lecture's own position is contested. Where a question says *"with a number"*
> or *"with evidence"*, an answer without one is capped at half.
>
> **Section C is marked on argument, not on agreement or length.**

---

## Section A — Short Answers (30 marks)

*Two or three sentences each. Do not write paragraphs.*

**A1. [3]** State the operational test for whether a change was a refactoring.

**A2. [3]** An invariant must be enforced where? State the general rule, and why the domain layer is not enough for uniqueness.

**A3. [3]** State Hyrum's law, and give the `roomsvc` instance.

**A4. [3]** Name the load-bearing words in Fowler's definition of continuous integration, and the two-command test for whether a team is doing it.

**A5. [3]** What is the difference between coverage and mutation score, and which one predicted real-fault detection after controlling for the other?

**A6. [3]** Give the *"one actor"* form of the Single Responsibility Principle, and say why it is better than *"one thing"*.

**A7. [3]** Why does a characterisation test need a comment, and what must the comment say?

**A8. [3]** Define technical debt's **interest** as a formula, and say which factor requires no judgement.

**A9. [3]** Name the four severity labels for review comments, and what happens to a review without them.

**A10. [3]** Why does documentation rot for a structural reason rather than a human one?

---

## Section B — Applied Judgement (40 marks)

**B1. One mechanism, three literatures [12]**

Three practices in this course are supported by evidence that points at the same underlying mechanism: **review size** (Cisco, Google), **TDD's small steps** (Fucci et al.), and **deployment frequency** (DORA).

**(a) [4]** Name the mechanism, and state what each of the three literatures found.

**(b) [4]** **Explain why the mechanism produces the result in each case.** The explanation must differ across the three, because the three activities are different.

**(c) [4]** **Why is three independent literatures agreeing stronger evidence than any one of them?** And **give one reason it could still be wrong** — a confound that all three might share.

---

**B2. A code review [14]**

A teammate opens a pull request. It is **640 lines**, titled `"refactor booking service + fix cancel bug"`, with an empty description. The tests pass. You have thirty minutes.

**(a) [5]** **What do you do first, and why?** Name three things about this pull request that you can act on before reading any code.

**(b) [5]** The diff contains this, and the existing tests pass:

```python
-    with uow:
-        booking = repo.confirm(hold_id)
-        notify(booking.owner_id, message_for(booking))
+    with uow:
+        booking = repo.confirm(hold_id)
+    notify(booking.owner_id, message_for(booking))
```

**Write the review comment.** Then say **whether this is a refactoring**, and **why the passing tests are not evidence either way.**

**(c) [4]** The author replies: *"I moved it because you told me last week that notifications shouldn't be in the transaction."* **They are right, and the change is still not a refactoring. Reconcile those two facts**, and say what should have happened instead.

---

**B3. A number that is not what it looks like [14]**

A team reports: **branch coverage 91%, mutation score 38%, pipeline time 11 minutes, 1,400 lines in the domain package, four open branches, oldest eleven days.**

**(a) [6]** **Rank these findings by what you would act on first**, and justify the ranking. **At least one of the numbers is not a problem** — say which and why.

**(b) [4]** **What is the most likely explanation of 91% against 38%?** Name the two survivor types you would expect to dominate, with an example of each.

**(c) [4]** The team says: *"we will raise the mutation score to 80% before the demo."* **Give two reasons that is the wrong plan**, and say what you would do instead.

---

## Section C — Essay (30 marks)

**Answer ONE. About 700–900 words.** Marked on the argument: a position, evidence used correctly, and the strongest objection to your own position addressed.

---

**C1. "Every practice in this course is a claim about cost, in a context, with evidence — and the evidence is much weaker than the confidence with which it is taught."**

**Defend or attack.** You must use at least **four** of: the TDD replication, Inozemtseva & Holmes, Just et al., the Fagan-to-pull-request transfer, DORA's methodology, Project Aristotle, the maintainability index.

**Then the harder part:** four originators — Fagan's inspection figure, Fielding's REST, the Agile Manifesto's authors, Cunningham's debt — publicly disowned what their ideas became. **What does that pattern tell you about how this field transmits knowledge, and what should a practitioner do about it?**

---

**C2. "Goodhart's law is the central problem of software engineering measurement, and the only defensible response is to refuse targets entirely."**

**Defend or attack.** Use at least **four** of the five appearances: coverage, review thoroughness, deployment frequency, deprecation counts, velocity.

**Then answer the objection that makes this hard:** an organisation of two thousand engineers **cannot** manage by reading individual findings — it needs aggregate numbers to allocate anything. **So is "never set a target" advice that only works at small scale?** Take a position, and say what a large organisation should do instead.

---

**C3. "The fix was twelve lines and it took four months."**

**Use the VNC 101 incident to argue what software engineering is actually about.**

Account for the four months without invoking incompetence. Then: **which of this course's thirteen weeks would have shortened it most, and which would have made no difference at all?** Defend both choices — **the second is the harder and more interesting claim.**

**Finally, the complication:** a team that had done everything this course teaches would have spent considerable effort to make that afternoon possible. **Was it worth it? Under what conditions would it not have been?** A defensible "sometimes not" scores as highly as a defensible "always".

---

## Given facts

*Provided so that no mark depends on memorising a figure.*

| | |
|---|---|
| **`roomsvc`** | 11,438 lines; 2,847 commits; 5 human authors, 1 remaining; **14% of commits reference an issue**; 143 open issues, median age 291 days; **17 deprecated endpoints, oldest March 2021** |
| **`bookings.py`** | 2,814 lines; **891 of 2,173 file-touches in 2 years (41%)**; maintainability index 11.4; **78% of surviving lines by an author who left in 2023** |
| **`confirm_booking`** | 487 lines; cyclomatic complexity 94; **11 tests**; changes together with `notify.py` in 112 commits, neither importing the other |
| **Tests** | 212 tests, 94 s; **61.0% line / 48.3% branch coverage**; **31.1% mutation score** (1,204 mutants, 374 killed) |
| **The incident** | VNC 101 double-booked 14 Oct 2024; **23 days to diagnose; 4 months to ship**; fix = 12 insertions, 1 of them DDL |
| **Lifetime cost** | ~60% post-release; of maintenance: ~50% perfective, ~25% adaptive, **~21% corrective**, ~4% preventive |
| **Feature usage** | 45% never used, 19% rarely (Standish, 2002) |
| **Review size** | Cisco: defect density falls sharply above ~200 LOC; effectiveness collapses after ~60 min. Google: **median change ~24 lines**, ~80% one reviewer |
| **Modern review** | Bacchelli & Bird, 570 comments: code improvements ~29%, **defects ~14%**, knowledge transfer ~9% |
| **Brooks / Little** | $n(n-1)/2$ communication paths; $L = \lambda W$ |
| **Test timings** | domain test with a fake ≈ 1 ms; integration test, session container ≈ 5–20 ms; container startup ≈ 9 s |

---

*CS 212 · Final Examination · Weeks 0–12 · 100 marks · 15% of the course*
