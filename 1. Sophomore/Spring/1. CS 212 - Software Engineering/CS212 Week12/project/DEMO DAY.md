# CS 212 · Demo Day
## Tuesday 28 April, TH 200 · 15 minutes per team plus 5 for questions

---

**Code and report due Friday 1 May, 17:00.** Demo Day is the presentation; the marks for the system,
the engineering and the report are assessed from the repository in the days after.

| Component | Marks |
|---|---|
| **The system** | 40 — works, meets the stories you committed to, handles the failures you identified |
| **Engineering quality** | 30 — tests and what they are worth, review history, pipeline, the state of the design |
| **The report** | 20 — 3,000–4,000 words |
| **The demo** | **10** |

> **The demo is 10 of 100.** Worth doing well because a failure damages the other 90 by association —
> **not** because the stage is where the marks are. **Do not spend the weekend on slides.**

---

## The Running Order

**Posted Thursday of Week 12.** Two teams per half-hour, 10:00–12:00. **Be in the room for the team
before you** — watching one other team is the cheapest improvement available to your own.

---

## Fifteen Minutes

| Time | | |
|---|---|---|
| **0:00** | **One sentence: what it is and who for.** No slides | If a stranger cannot repeat it afterwards, the rest was noise |
| **1:00** | **The live demo.** Book a slot. **Then try again and be refused** | ↓ |
| **5:00** | **One diagram** — where the rules live, **where the invariant is enforced** | Label it |
| **8:00** | **What your tests are worth.** Mutation score with the line count. **Then break something live** | ↓ |
| **10:00** | **One decision defended** — an ADR, with the rejected alternative | |
| **12:00** | **What you got wrong**, and what it cost | Four marks, and the most credible two minutes available |
| **14:00** | What next, one slide | |

**Everyone speaks.** Not equally.

---

## The Two Things That Matter Most

### 1. Show the refusal

```
POST /v1/bookings  TH200, 2026-05-12 14:00   → 201 Created
POST /v1/bookings  TH200, 2026-05-12 14:00   → 409 Conflict
```

**Then one sentence on where the guarantee lives:** *"a partial unique index on
`(resource_id, slot) WHERE state='CONFIRMED'`, so it holds under concurrency and against anything that
bypasses our API."*

**That is the incident this course opened with, refused, in ninety seconds.** If you have the nerve,
run the concurrency test instead — two clients, `[201, 409]`, one row.

### 2. Break something, live

```python
-  if (booking.state, to) not in LEGAL:
+  if (booking.state, to) in LEGAL:
```

```
FAILED test_only_legal_transitions_are_permitted[CONFIRMED-HELD]
```

**Ten seconds, and it answers the viva question — *"if someone broke your main rule, which test would
fail?"* — by doing it rather than claiming it.**

---

## Monday, Not Tuesday

**The deployment checklist is [[CS212 Week8/project/DEPLOYMENT CHECKLIST|DEPLOYMENT CHECKLIST]].** The
short version:

- [ ] **Deploy on Monday 27 April.** A deploy on the day is a decision to debug in front of forty people
- [ ] **Verify the SHA** on Monday evening **and again at 09:00 Tuesday**
- [ ] **Seed data that exists.** A demo against an empty database is a demo of an empty database
- [ ] **Rehearse twice, against the deployed instance, on the machine you will use**
- [ ] **Rehearse the refusal**, not just the success
- [ ] **Record two minutes of the demo working, on Monday.** If the network fails you show it and carry on
- [ ] **Rollback command in an already-open terminal**
- [ ] **A future date and a resource that is not TH 200** — you will be standing in TH 200

---

## The Viva

**Five minutes. Two questions are guaranteed and have been published since Week 6:**

> **1. What shape did you choose, and what did it buy — for whom?**
>
> *"Modular monolith; we ranked testability first; ADR 0003 has the alternative"* is full marks.
> *"Microservices, because it's better architecture"* is poor. **"We didn't really decide, it accreted,
> and here is the ADR we wrote late" is worth more than a retro-fitted justification.**

> **2. If someone broke your main rule, which test would fail?**
>
> **Name it.** Then break it, if asked.

**Likely follow-ups**, so you are not surprised:

- *What is on your debt register that you chose not to fix, and why?*
- *What would the first week of a Week 14 be?*
- *Which ADR would you now reverse?*
- *Who on the team cannot deploy, and what happens if the person who can is ill?*

**One person may answer each, and it need not be the same person.** A team where the same person
answers everything answers the fourth question by accident.

---

## What Loses Marks Reliably

| | |
|---|---|
| **Slides of screenshots instead of a live demo** | Something breaking live costs you almost nothing; not trying costs you the marks |
| **A feature tour** | Nobody has ever wanted more of one. Cut it first |
| **A coverage number with no mutation score** | **It invites the question you least want**, given the marking rule |
| **"Everything went well"** | Four marks, and it is the least credible two minutes you could choose |
| **One person presenting** | Visible, and it tells the room something you cannot unsay |
| **A number with no command or date** | Every figure comes with what produced it and when |
| **Overrunning** | You will be stopped at 15:00, mid-sentence, and the *"what we got wrong"* section is what you will lose |

---

## After

| | |
|---|---|
| **Friday 1 May, 17:00** | **Code frozen and report submitted.** `docs/report.md` plus a PDF |
| | **Peer assessment**, submitted with it. It affects individual marks |
| **Friday 8 May, 09:00–11:30** | **Final exam.** Comprehensive; **Weeks 11 and 12 appear only here** |

**And L39's last instruction, which is genuinely the best use of an hour before you write the report:**
**read your own `git log` from Week 1.** Thirteen weeks, in order, in the words you used at the time.
**It will remind you of three things you have forgotten, and it is what the report's process section is
actually about.**

---

*CS 212 · Week 12 · Demo Day · 28 April · TH 200*
