# CS 212 · Assignment 1
## Requirements: User Stories, Use Cases, a Domain Model

---

**Released:** Week 1, Wednesday 17:00 · **Due:** Week 2, Friday 17:00
**Total: 100 points** · Submit one PDF, `A1_{LastName}_{StudentID}.pdf`

> **This is an individual assignment about your team's project.** You will produce work that
> overlaps your team's — that is intended. **Write your own, and where you disagree with what your
> team decided, say so and argue for your version.** Q5 is entirely about that, and a paper whose
> author agreed with everything scores below one that did not.
>
> **The `roomsvc` parts require the repository.** Clone the tag `cs212-reference`; see
> [[CS212 Week0/resources/roomsvc metrics|roomsvc metrics]].
>
> Collaboration: discuss freely, write alone. State at the top who you discussed what with.

---

### Q1: Find the Unwritten Requirement (20 points)

`roomsvc` double-booked VNC 101 on 14 October 2024 (W0 L01 §6).

**(a) [5]** State the violated invariant as a single sentence, in the form L04 §2 requires. Then say **which of the four requirement categories it belongs to, and why it appears in no user story.**

**(b) [8]** **Find three more invariants in `roomsvc`'s behaviour that are nowhere written down.** Read the code — `models.py` and `bookings.py` — and look for rules the code *enforces* that no comment, docstring, issue or test states. For each: the sentence, the line number that enforces it, and **one way it could be violated today** (a code path, an admin action, a direct database write).

**(c) [7]** For each of your three, say **where it should be enforced** — database constraint, domain layer, API layer, or not at all — and why. **At least one of your three should be "not at all", and you should say what should happen instead.** Not every rule the code currently enforces deserves to be an invariant, and identifying an accidental one is worth more than finding a real one.

---

### Q2: Stories, With Criteria That Bite (20 points)

**(a) [8]** Write **four user stories** for `slot` in the Card/Conversation/Confirmation sense: the card, and **acceptance criteria in Given/When/Then**. They must cover: one booking action, one cancellation action, one thing an **admin** can do, and one thing a **student** can do.

**Every story needs at least one failure scenario.** A story with only a happy path scores at most half.

**(b) [6]** Take your **booking** story and **split it three different ways**, by three different strategies from L05 §2. For each split, give the resulting slices and say **which slice you would build first and why**.

**(c) [6]** **Pick one of your four stories and argue that it should not be built this term.** Use the beneficiary test and L02 §5's feature-usage data. **This question is marked on the honesty of the argument** — picking your most obviously frivolous story and knocking it down earns less than making the real case against something you want to build.

---

### Q3: A Use Case, With Its Failures (20 points)

**(a) [12]** Write a full use case, in L06 §1's format, for **cancelling a booking** in `slot`. Primary actor, precondition, guarantee, main success scenario, **and at least five extensions**.

**Your extensions must include** at least one of each:
- A case where the actor is not permitted
- A case where the state has changed since the actor last looked
- **A case where something downstream of the cancellation fails after the cancellation has succeeded**

**(b) [4]** For the third case, state **what must not happen**, and name the property you are relying on. *(L06 §1's extension 6a is the same shape. `roomsvc` gets it wrong; the line number is findable.)*

**(c) [4]** L06 §1 says use cases are worth writing only where the difficulty is in the failure paths. **Name one `slot` interaction for which a use case would be a waste of an hour, and justify it.** Then name the property that distinguishes the two.

---

### Q4: The Domain Model (25 points)

**(a) [10]** Produce a domain model for `slot`: entities with their identities, value objects, relationships, and **an Invariants section with at least four invariants and where each is enforced.**

**This must be your own model.** If it is identical to L06 §3's, say why you accepted it; if it differs, say where and why. **Both are fine; silence is not.**

**(b) [8]** **The `Slot` decision.** L06 §3 argues that fixed-duration slots make the invariant an equality enforceable by a unique index, while arbitrary intervals make it an overlap that no unique index expresses.

- **[4]** State the trade honestly: **what does the fixed-duration model give up?** Name a real requirement it cannot express.
- **[4]** PostgreSQL *can* enforce non-overlap, with an exclusion constraint over a `tstzrange`. **Look it up, write the DDL**, and say what it costs relative to a unique index — in what the constraint requires, and in what a developer has to know to maintain it.

**(c) [7]** `roomsvc` has **five words for one concept** (L06 §2) and **issue #31 has been open since August 2020** because `Recurrence` is not a concept in its model.

- **[4]** Reproduce the `grep` from L06 §2 and pick **one other concept in `roomsvc` with more than one name.** Show the counts.
- **[3]** *"Cancel one occurrence of a recurring booking"* touches nine files. **Name the missing concept and say what the model should have been**, in two sentences.

---

### Q5: Disagree With Your Team (15 points)

**Pick one decision your team made this week** — the domain model, the vocabulary, the stories on the board, the WIP limit, the Definition of Done, the Slot representation, anything in the charter.

**(a) [6]** State the decision, and the **strongest** case for it. Steel-manning is the marked part: state it better than its advocate did.

**(b) [6]** State your alternative and the case for it. **Say what evidence would settle it**, and whether that evidence is obtainable before Week 6.

**(c) [3]** Say what you will actually do — including *"nothing, they are right"* or *"nothing, it is not worth the argument"*, both of which are legitimate and both of which need a reason.

> **This question is not a trap and there is no penalty for loyalty.** Every team of five makes at
> least one decision that at least one member doubts. **The failure this course cares about is the
> doubt going unstated until April**, and this question exists to make stating it routine.

---

## Marking

| Band | |
|---|---|
| **90–100** | Q1(b) finds real undocumented invariants with line numbers, and Q1(c) correctly identifies one that should not be an invariant at all. Acceptance criteria include concurrency. Q4(b) writes working DDL and states the cost honestly. Q5 is a genuine disagreement, well made |
| **75–89** | Everything correct and specific. Failure paths present throughout. Q4's model is coherent and its invariants are placed sensibly. Q5 picks a real but low-stakes decision |
| **60–74** | Stories and use case correct but happy-path-heavy. Invariants listed without saying where they are enforced. Q1(b) reads the docs rather than the code. Q5 is pro-forma |
| **45–59** | Stories restate the template with no criteria. No failure paths. Domain model is an ER diagram with no invariants section |
| **< 45** | No engagement with `roomsvc`. Invariants absent or confused with features |

**The single most common way to lose marks on this paper** is writing only happy paths. L06 §1 counts six extensions against one success path in a use case you were handed. **If your answer to Q3 has three extensions, you have not finished.**

---

*CS 212 · Week 1 · Assignment 1 · 100 points · due Friday of Week 2, 17:00*
