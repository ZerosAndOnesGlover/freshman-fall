# CS 212 · Software Engineering
## Week 1: Requirements Engineering

**Credits:** 3 · **Prerequisites:** PROG 102, CS 101
**Assessment for this course (overall):** Team Project 40%, Individual Assignments 30%, Midterm 15%, Final 15%
**This week's deliverables:** A 0 due Friday 17:00 · **A 1 released Wednesday** · **📊 Quiz 1 Tuesday** (covers Week 0) · **the walking skeleton, Friday**

> **Graded work begins this week.** Week 1 opens Monday Jan 26. CS 212 meets **Tue/Wed/Thu
> 10:00–10:50 in TH 200**, and **Quiz 1 runs in the first ten minutes of Tuesday's lecture** — ten
> minutes, closed book, unmarked, with its own key printed below the questions.

---

### Why This Week Exists

Because the bug that put two lectures in VNC 101 was a requirement nobody wrote down.

**Not a missing feature — a missing sentence.** *"A resource has at most one confirmed booking per slot"* is an **invariant**: not something the system does, but something the system is. It appears in no user story, because it never occurs to anyone that it could be false, and it sat in `roomsvc`'s issue tracker as exactly zero issues until 14 October 2024.

**This week is the three artefacts that would have caught it**, in increasing order of how much they cost you: a **user story** whose acceptance criteria include the concurrent case; a **use case** whose six extensions are the 70% of the code the success path does not mention; and a **domain model** with an *Invariants* section that says, for each one, **where it is enforced.**

**And the last of those is the week's real argument.** Whether your invariant is enforceable at all is decided by a modelling choice you make before you write a line: fixed-duration slots make it an equality that a unique index enforces; arbitrary start-and-end times make it an overlap that no unique index expresses. **The domain decision and the enforceability decision are the same decision.**

**The walking skeleton is due Friday.** Thin, ugly, whole.

---

### Learning Objectives

By the end of Week 1, you should be able to:

1. Distinguish **functional, non-functional, constraint and invariant** requirements, and say why only the fourth killed `roomsvc`.
2. **Find your own invariants** by asking which sentence, if it became false, would mean the system had lied — and write them down with a placement.
3. Say why **a non-functional requirement without a number, a percentile and a load is a mood**, and rewrite one that is.
4. Give **four reasons requirements are discovered rather than gathered**, and name what each of the four elicitation techniques is blind to.
5. Ask the two highest-yield interview questions, and say why *"tell me about the last time this went wrong"* outperforms twenty minutes of "what would you like".
6. **Treat vagueness as unresolved conflict**: name `slot`'s four stakeholders and a requirement on which two of them disagree.
7. State a story as **Card, Conversation, Confirmation**, and delete one whose *"so that"* is circular.
8. **Split a story five ways that are not by layer**, and say which slice you would build first and why.
9. Write acceptance criteria that are **observable from outside, include the failure cases, and are numeric where they concern quality** — including the concurrent-request scenario.
10. Say what stories are the **wrong** tool for, and why cross-cutting quality belongs in the Definition of Done rather than on the board.
11. Write a **use case with its extensions**, and explain why a notification failure must not roll back a confirmed booking.
12. **Build a domain model that is a vocabulary before it is a structure**, and explain what five words for one concept cost `roomsvc`.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L04 What a Requirement Is and Why Yours Are Wrong]] | The four categories and **the invariant that is in none of the textbooks**; requirements as discovered, not gathered; four elicitation techniques and their blind spots; **vagueness as unresolved conflict**, with `roomsvc` issue #812 taken apart; cheap traceability — **and the 14% of `roomsvc` commits that have it**; the four expensive-to-reverse decisions in `slot` |
| [[L05 User Stories and Acceptance Criteria]] | Card, Conversation, Confirmation; **INVEST's two load-bearing letters**; five ways to split a story and the one way not to; **acceptance criteria including the concurrency scenario that is the whole difference from `roomsvc`**; what stories are the wrong tool for; estimation, sceptically; the walking skeleton |
| [[L06 Use Cases and the Domain Model]] | **One success path, six extensions**; the notification that must not roll back a booking; the domain model as vocabulary — **five words for one concept, measured**; entities, value objects, and **why the `Slot` decision is the invariant decision**; five invariants with placements; **the missing `Recurrence` that has kept issue #31 open since 2020** |
| [[CS212 Week1/project/WALKING SKELETON\|WALKING SKELETON]] | **Due Friday.** What it is, what it deliberately lacks, **the five failure modes you want to meet now**, a layout, and how four people split an evening |
| [[CS212 Week1/assignments/QUIZ 1 Week 1 Tuesday\|QUIZ 1]] | Seven questions on Week 0, ten minutes, **with its own answer key** |
| [[CS212 Week1/assignments/A 1 Requirements User Stories Use Cases Domain Model\|A 1]] | Five questions, 100 points, due **Friday of Week 2**. Requires reading `roomsvc` |
| [[CS212 Week1/resources/Reading Guide Week 1\|Reading Guide Week 1]] | Ninety minutes required; **a warning about over-applying Evans**; and a five-step method for reading a codebase cold |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Whether you can enforce your invariant is decided before you write any code.**

Fixed 50-minute slots make *"at most one confirmed booking per resource per slot"* an **equality** on `(resource_id, slot)`, and a partial unique index enforces it absolutely — across processes, against direct database writes, forever, with no application code involved in the decision. Arbitrary start and end times make the same rule an **overlap**, which a unique index cannot express, which pushes the check back into application code, which is exactly where `confirm_booking` was standing on 14 October 2024.

**The more general model is the weaker one.** That sentence is counter-intuitive and it is the week's lesson: generality is not free, it is paid for in enforceability, and *"arbitrary intervals"* sounds like better engineering right up to the point where you have to make it true. **Choosing the constrained model, deliberately, having named what it gives up — that is the engineering.**

*(And when you genuinely do need intervals, Postgres has an exclusion constraint over a `tstzrange`. A 1 Q4(b) makes you write it, because knowing the escape hatch is part of knowing the trade.)*

---

### Assessment Reminder

**Quizzes carry no weight. The project carries 40%.**

> **⚠️ CS 212 differs from every other Year 2 course on exactly this point.** In CS 201, CS 202,
> PROG 201 and PROG 202 the practical work is the lab, and the lab is unmarked. **CS 212 has no
> lab. Its practical work is the team project.**

**Quiz *N* covers Week *N−1***, runs ten minutes at the start of **Tuesday's** lecture in Weeks 1–11, and prints its own answer key. Tracked in [[_CS 212 Quiz Record]].

**Assignments** are released Wednesday 17:00 and due Friday 17:00 of the week after; **the lowest of the thirteen is dropped.** A 0 is due this Friday; A 1 is released Wednesday.

**Nothing due Friday in the repository is marked this week.** The charter, the domain model and the walking skeleton are **70% of Phase 1** in Week 6, and the skeleton in particular is the thing every previous cohort wished they had done now.

---

### Connections

**Back:** **Week 0's invariant is this week's vocabulary.** The VNC 101 double-booking (W0 L01 §6) is now a named requirement category, and the reason it appeared in no story is a fact about stories rather than about that team. **W0 L02 §5's feature-usage data** is what A 1 Q2(c) makes you apply to your own backlog.

**Sideways:** **CS 202's Week 1 is the process** — what the kernel saves when it takes the CPU away. The concurrency in this week's third acceptance scenario is the same phenomenon at a different scale: two workers interleaved between a check and an act. **CS 202 solves it with a lock in one address space; you solve it with a constraint in a shared database**, and both are the same idea — make the check and the act indivisible.

**Forward:** **Week 2 asks why `confirm_booking` is bad for reasons that have nothing to do with its length.** **Week 3 is the placement question this week keeps deferring** — which layer owns an invariant, and why "the database" is an answer people resist. **Week 4** names the pattern that fixes the notification-inside-the-transaction bug. **Week 5** writes the concurrency scenario as a test that actually runs two clients.

---

*CS 212 · Week 1 · © CSE Department*
