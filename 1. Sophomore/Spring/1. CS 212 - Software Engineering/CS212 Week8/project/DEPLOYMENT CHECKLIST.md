# CS 212 · Deployment Checklist
## For `slot`, and for the Demo on 28 April

---

> **Two uses.** In the next fortnight it is A 8's specification. On **Tuesday 28 April** it is what
> stands between you and a demo that does not work — **and Demo Day is the one day of the term when a
> broken deploy is watched by forty people.**

---

## Before the first deploy — once

- [ ] **`/health` returns its own SHA**, baked in at image build. *(4 marks in A 8, and the thing that makes everything below checkable)*
- [ ] **Base image pinned** to a patch version or a digest. `FROM python:3.12` is not a version
- [ ] **`--platform linux/amd64`** in the build, if anyone on the team has an Apple Silicon machine
- [ ] **Multi-stage**, non-root, no config baked in
- [ ] **Migrations run as their own step**, never on application startup
- [ ] **A rollback target exists** — the previous SHA is still in the registry and you have tried deploying it
- [ ] **A secret is a secret**: nothing real in `docker-compose.yml`, nothing real in the repository. `detect-secrets` in pre-commit

## Every deploy — automated, not remembered

- [ ] Gate green on the commit
- [ ] Image built **once**, tagged with the SHA, pushed
- [ ] Tests ran **against that image**, not a fresh build
- [ ] Migrations applied, as a separate step, **before** the new code
- [ ] Deploy the tag
- [ ] **Verify: every target reports that SHA.** ← *the Knight Capital step*
- [ ] **Smoke test: book one slot against the deployed instance and read it back**
- [ ] If any of the last three fail: **stop, and roll back to the previous SHA**

## The question to answer before every deploy

> **If this is wrong, how do we get back, and how long does it take?**

**If the answer involves restoring a database, the change was not deployable.** Split it: add the
column, deploy; write both, deploy; backfill; read the new, deploy; drop the old, deploy. **Five
deploys, each reversible.**

---

## The week before Demo Day

- [ ] **Deploy on Monday 27 April**, not on the morning. A deploy on the day is a decision to debug in front of an audience
- [ ] **Rehearse the demo against the deployed instance**, twice, on the machine you will use
- [ ] **Rehearse the rejection**, not just the success. *"Book it, then try to book it again and be refused"* is 8 of the 30 presentation marks and it is the thing the whole course is about
- [ ] **Know your rollback command by heart**, and have it in a terminal that is already open
- [ ] **Have a recording.** Two minutes of the demo working, made on Monday. **If the network fails at 10:00 on Tuesday you show the recording and carry on** — and nobody will mind, because you thought about it
- [ ] **Seed data that exists.** A demo against an empty database is a demo of an empty database
- [ ] **Check the room.** TH 200 has a projector; know which cable, and test it

---

## What goes wrong on the day, and what to do

| | |
|---|---|
| **The network** | The recording. Say what you are showing and why |
| **The deploy drifted** | You checked the SHA on Monday. Check it again at 09:00 |
| **The database is empty** | A seed script, committed, run as part of the deploy |
| **Someone else's booking is in your slot** | Use a distinct resource and a date in the future. Do not demo on `TH200` at `10:00` on the day you are standing in TH 200 at 10:00 |
| **A migration failed halfway** | This is why you tried the rollback in advance |

> **And the one that is not technical.** Something will go slightly wrong, in front of everybody.
> **Handling it calmly costs you nothing and is visible engineering judgement** — the rubric gives
> marks for the demo, not for the demo being flawless. The teams that lose marks are the ones that
> had no plan, not the ones whose plan was needed.

---

*CS 212 · Week 8 · deployment checklist · use it in A 8, and again on 27 April*
