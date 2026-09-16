# CS 212 · Team Project — Phase 1
## Rubric · Tuesday 3 March, TH 200, 10 minutes per team · 10% of the course

---

> **70 of the 100 marks are for artefacts that exist in your repository before you present.**
>
> This is deliberate and it is stated in the brief. **Ten minutes of stage time cannot be worth 10%
> of a course**, and making the repository carry the mark is what lets you rehearse for twenty
> minutes instead of an evening. It also means **a team that has done the work cannot lose the mark
> to a projector failure**, which has happened.

---

## The Repository — 70 marks

**Assessed from a clone taken at 09:00 on Tuesday 3 March.** Everything below is work already
required by A 1, A 3 and A 5; none of it is additional.

### 1. The walking skeleton, grown up — 15

| | |
|---|---|
| **8** | **One booking, created and read back through every layer**, against a real database, in Docker. Works from a clean clone by following your `README.md` |
| **4** | **`docker compose up` works on a machine that has never run it.** Marked by doing it |
| **3** | **CI green on `main`**, running the tests on every push |

**A team whose project cannot be started from its own README loses 12 of these 15**, whatever the demo shows. It is the single most common Phase 1 failure and it is entirely avoidable — hand the README to another team and watch (W3 checkpoint, question 1).

### 2. The invariant, enforced — 15

| | |
|---|---|
| **6** | The constraint exists in a **migration**, not applied by hand. Show the DDL |
| **6** | **The concurrency test** (A 5 Q1): two concurrent requests, `[201, 409]`, exactly one confirmed row |
| **3** | The database error is **translated** — infra to domain concept to HTTP status. The domain does not raise `HTTPException` |

**This is the artefact that most distinguishes a strong Phase 1 from a weak one**, and it is the direct answer to the incident the course opened with.

### 3. Requirements and the domain model — 12

| | |
|---|---|
| **4** | `docs/domain-model.md`: entities with identities, value objects, relationships |
| **5** | **An Invariants section, with where each is enforced.** At least four, at least one in the database and at least one not |
| **3** | An ordered board with acceptance criteria, **including at least one failure scenario per story** |

### 4. Architecture decisions — 12

| | |
|---|---|
| **8** | **Four ADRs** in `docs/adr/`, in Nygard's format. **2 each, and the negatives carry the marks** — an ADR with only upsides scores 1 |
| **2** | They are mutually consistent and at least one cross-references another |
| **2** | **The architecture test exists and runs in CI** (A 3 Q3) |

### 5. Tests that are worth something — 10

| | |
|---|---|
| **4** | The suite runs in CI and within the budget in your charter. **Report the number** |
| **3** | **Branch coverage reported**, with the command and date. **No target; the number is a diagnostic** |
| **3** | **A mutation score for the domain package**, with mutants generated and killed. **A 6 is due after this, so a preliminary run is fine** — what is marked is that you have looked |

**Reminder, from the brief:** **95% coverage with a 30% mutation score scores below 70% with 75%.**

### 6. Process evidence — 6

| | |
|---|---|
| **2** | `docs/charter.md`, with the Definition of Done and the WIP limit |
| **3** | **Three retrospectives**, `docs/retro-1.md` … `retro-3.md`, **each naming something that changed** |
| **1** | Every member has commits spread across the weeks, not clustered |

> **On the retrospectives.** A retro that says *"went well: we merged things; improve: communicate
> more"* scores 0 of its mark. **A retro must name something the team changed as a result** — a
> rule, a rotation, a tool, a rhythm. **A team whose process never changed did not retrospect**,
> and the final report asks about this again.

---

## The Presentation — 30 marks

**Ten minutes, plus five for questions. TH 200 has a projector and a whiteboard.**

| | |
|---|---|
| **8** | **A live demo of one booking, including a rejection.** Not slides of screenshots. **Book a slot, then try to book it again and be refused** |
| **8** | **The architecture, in one diagram**, explained in two minutes: where the rules are, where the invariant is enforced, what the layers are |
| **6** | **One decision, defended** — an ADR, with the alternative you rejected and why |
| **4** | **One thing you got wrong and changed.** Any team that has not got something wrong by Week 6 has not built anything |
| **4** | **The viva.** Two questions, answered honestly. §Q below |

**Everyone speaks.** Not equally, but everyone. A team where one person presents and four stand silent loses 4 marks across the presentation and gains nothing.

### The two viva questions

**Every team gets these two.** They are published so that you can prepare, which is the point — **preparing for them is most of what Phase 1 is trying to make you do.**

> **1. What shape did you choose, and what did it buy you — for whom?**
>
> W3 L12 §6 gives the mark scheme. *"Modular monolith; we ranked testability first; ADR 0003 has
> the alternative"* is full marks. *"Microservices, because it's better architecture"* is poor.
> **"We didn't really decide, it accreted, and here is the ADR we are writing now" is worth more
> than a retro-fitted justification** and is marked accordingly.

> **2. If someone broke your main rule, which test would fail?**
>
> **Name the test.** Then, if asked, break it in front of us and show the failure. A team that
> cannot name the test has the same problem `roomsvc` had with 212 green ticks.

---

## What Loses Marks Reliably

Collected from previous cohorts. **Every one of these is avoidable in the week before.**

| | |
|---|---|
| **A README that does not work** | 12 marks, immediately. Test it on a foreign laptop |
| **Slides of screenshots instead of a live demo** | 8 marks. Something breaking live costs you nothing; handling it badly costs a little |
| **ADRs written the night before** | Visible in `git log`, and the alternatives are always missing — which is the part worth marks |
| **Retros with no change in them** | 3 marks, and it recurs in the final report |
| **A beautiful user interface and no invariant** | **No marks are given for CSS.** 15 are given for the constraint |
| **One person presenting** | 4 marks, and it is the clearest signal of a team problem the instructor can see |
| **Claiming a number without the command** | Every number you present should come with what produced it and when |

---

## If You Are Behind on Monday Morning

**In this order. Do not do the second before the first.**

1. **Make the README work from a clean clone.** Thirty minutes, 12 marks.
2. **Apply the constraint as a migration and write the concurrency test.** Two hours, 12 marks, and it is the artefact the course is about.
3. **Write the four ADRs**, honestly, with the alternatives — **dated today, marked `accepted`, and say in the presentation that you wrote them late.** Honest and late beats fabricated and backdated, and `git log` shows the difference anyway.
4. **Run `coverage` and `mutmut` once and report whatever they say.** 3 marks for having looked.
5. Rehearse the demo **twice**, on the machine you will use.

**Do not spend Monday on slides.** Eight of the thirty presentation marks are a live demo and eight are one diagram; the rest is talking.

---

*CS 212 · Week 6 · Phase 1 rubric · 10% of the course*
