# CS 212 · Software Engineering
## Week 12 · Lecture 1 of 3
### Presenting Engineering Work

---

**Sat:** Tuesday of Week 12, 10:00–10:50, TH 200 · **No quiz — Quiz 11 was the last.** · **Reading:** none. Rehearse instead. · **Next:** L38, engineering management

---

## 1. Who You Are Talking To

**The commonest failure in a technical presentation is answering a question nobody asked.**

Demo Day has three audiences in the room, and they want different things:

| Audience | Wants | Bored by |
|---|---|---|
| **The instructor** | *Did you do the engineering?* Where the invariant lives, what your tests are worth, what you got wrong | Feature tours |
| **Other teams** | *How did you solve the problem I am stuck on?* | Your requirements process |
| **A hypothetical stakeholder** | *Does it work, and can I trust it?* | Your architecture diagram |

**You cannot serve all three for fifteen minutes**, so the order matters: **show that it works, then show why it is trustworthy, then say what you got wrong.** That sequence satisfies the third audience in two minutes, the first in ten, and the second throughout.

**And the structural fact worth knowing: you are marked on the repository more than on the stage.** Phase 1 put 70 of 100 marks in the repository; the final puts **40 on the system, 30 on engineering quality, 20 on the report and 10 on the demo.** **The demo is 10.** It is worth doing well because a failed demo damages the other 90 by association — not because the stage is where the marks are.

---

## 2. The Fifteen Minutes

**A structure that works, with timings. Deviate deliberately, not by accident.**

| Time | What | Why |
|---|---|---|
| **0:00–1:00** | **What it is, in one sentence, and who for.** No slides | If a stranger cannot repeat your one sentence afterwards, the rest was noise |
| **1:00–5:00** | **The live demo.** Book a slot. **Then try to book it again and be refused** | §3 |
| **5:00–8:00** | **One diagram**: where the rules live, where the invariant is enforced, what the layers are | The engineering question, answered before it is asked |
| **8:00–10:00** | **What your tests are worth.** Mutation score with the line count. **Then break something live and show a test catch it** | §4 |
| **10:00–12:00** | **One decision, defended** — an ADR, with the alternative you rejected | W3 L10 §5's payoff |
| **12:00–14:00** | **What you got wrong.** A model that changed, a decision you would reverse, a debt item you chose to keep | §5 |
| **14:00–15:00** | What you would do next, in one slide | Shows you know what "done" would mean |

**Everyone speaks.** Not equally. A team where one person presents and four stand silent loses marks and — more importantly — **tells the room that one person did the work**, which may not be true and cannot be unsaid.

**Two things to cut first when you overrun:** the requirements process, and the feature tour. **Nobody has ever wanted more of either.**

---

## 3. The Demo: Show the Refusal

**The single highest-value ninety seconds available to you.**

```
Book TH 200 at 10:00 on 4 March.        → 201 Created
Book TH 200 at 10:00 on 4 March again.  → 409 Conflict
```

**Then say what just happened, in one sentence:** *"That refusal is a partial unique index on `(resource_id, slot) WHERE state='CONFIRMED'`, so it holds even if two requests arrive simultaneously and even if someone bypasses our API entirely."*

**Why this beats everything else you could show.** It is the exact failure this course opened with — **two lectures in VNC 101 on 14 October 2024** — and demonstrating that your system refuses it, **and being able to say where the guarantee lives**, is the whole thesis of thirteen weeks in ninety seconds.

**If you have the nerve, show the concurrency test instead:** two clients, one slot, `[201, 409]`, exactly one row. **It is the more impressive artefact** and it is A 5 Q1, which you already have.

**Rules for a live demo:**

| | |
|---|---|
| **Use the deployed instance**, not your laptop | Deployed on Monday, verified at 09:00 Tuesday (W8 checklist) |
| **Seed data that exists** | A demo against an empty database is a demo of an empty database |
| **Distinct resource and a future date** | **Do not demo `TH200` at `10:00` while standing in TH 200 at 10:00** |
| **Have a recording** | Two minutes, made Monday. If the network fails, you show it and carry on |
| **Know your rollback command**, in an already-open terminal | |

> **Something will go slightly wrong in front of everybody. Handling it calmly costs nothing** — the
> rubric marks the demo, not its flawlessness. **The teams that lose marks are the ones with no plan,
> not the ones whose plan was needed.**

---

## 4. Show That Your Tests Are Worth Something

**Everybody claims tests. Almost nobody shows evidence.** Two minutes, and it is the part that distinguishes a strong final presentation.

**What not to say:** *"we have 94% coverage."* **The examiners' own marking rule is that 95% coverage with a 30% mutation score scores below 70% with 75%**, so a coverage number alone invites the question you least want.

**What to say instead:**

> *"Domain package, 340 lines. Branch coverage 74%. **Mutation score 71%** — 312 mutants, 221 killed.
> We read twenty survivors in Week 6: three were real gaps, now tested; eleven were equivalent;
> six are in code we decided not to test, and they are items D-04 and D-09 on our debt register."*

**Then break something.** Live, in ten seconds:

```python
-  if (booking.state, to) not in LEGAL:
+  if (booking.state, to) in LEGAL:
```

```
FAILED tests/unit/test_transitions.py::test_only_legal_transitions_are_permitted[CONFIRMED-HELD]
```

**That is the demonstration.** It answers *"if someone broke your main rule, which test would fail?"* — **which is one of the two viva questions, published since Week 6** — by doing it rather than claiming it.

---

## 5. Say What You Got Wrong

**Counter-intuitive and worth four marks in Phase 1 and more in the final: the strongest part of an engineering presentation is the part where you were wrong.**

**Three reasons it works:**

1. **Every engineer in the room has been wrong the same way**, and can tell when somebody is pretending otherwise. **The pretence is more visible than the mistake.**
2. **It is the only evidence that you learned anything.** A team that was right from Week 1 either built something trivial or is not telling you.
3. **It pre-empts the question.** An examiner who was going to ask *"why is the domain model like this?"* now hears you explain that it changed in Week 8 and what it cost — **which is a much better answer than a defence.**

**What good looks like, and it is specific:**

> *"Our domain model had a booking belonging to a course rather than a person. We found out in Week 8
> when the registrar's actual rule turned out to be that a person owns a booking and may act for a
> course. **It cost a migration and six hours**, and ADR 0009 supersedes ADR 0004. If we had
> interviewed anyone in Week 1 instead of Week 7, we would have known."*

**What bad looks like:** *"we could have managed our time better"*, *"communication could have been improved"*. **These are not findings; they are the things people say instead of a finding.**

---

## 6. Slides, Briefly

**You need about five, and most teams make twenty.**

| Slide | |
|---|---|
| 1 | **The one sentence.** What it is, who for |
| 2 | **The architecture diagram.** One. Boxes, arrows, and **where the invariant is enforced, labelled** |
| 3 | **The numbers**, with their commands and dates |
| 4 | **What we got wrong**, and what it cost |
| 5 | What next |

**The demo is not a slide.** Neither is a code listing — **nobody can read code on a projector**, and if you must show a diff, show three lines at 24pt.

**On the diagram**, since it is worth eight marks in Phase 1 and is the thing that recurs: **label where the invariant is enforced.** W3 L10 §7's warning applies — a diagram outruns its caveats and gets quoted back at you without the paragraph that qualified it — **so write the caveat into the diagram.**

---

## 7. The Report Is Read More Carefully Than the Demo

**Fifteen minutes on stage; 3,000–4,000 words read at a desk with your repository open.** The report carries twice the demo's marks and is the document that survives.

**The two sections that distinguish reports, from the brief:**

**"What you deliberately did not build, and why."** With equal weight to what you did. **Two-thirds of delivered features are rarely or never used** (W0 L02 §5), so choosing not to build something is engineering, and a scope section that is only a feature list has missed the point.

**"At least one ADR you would now make differently."** Not a confession — **evidence that you can evaluate your own decisions**, which is the capacity the whole course is trying to build. **A team with no such ADR has either not decided anything or not looked back.**

> **And the sentence from the brief worth re-reading before you write:** *a team that says "our domain
> model was wrong and we found out in Week 8; here is what it cost and here is the migration" scores
> above a team that implies it was right all along.* **Every engineer marking it has been wrong in
> exactly that way, and can tell.**

---

## 8. Summary

- **Three audiences want different things**; serve them in order — **show it works, show it is trustworthy, say what you got wrong.** And note that **the demo is 10 of 100**: worth doing well because a failure damages the other 90 by association.
- **Fifteen minutes, structured**, with the first minute a single sentence and no slides. **Everyone speaks.** Cut the requirements process and the feature tour first.
- **Show the refusal.** Book it, then be refused, **then say where the guarantee lives.** That is thirteen weeks in ninety seconds. **Use the deployed instance, seed real data, pick a resource that is not the room you are standing in, and have a recording made on Monday.**
- **Show that your tests are worth something**: mutation score **with the line count**, the survivors you read and what they were — **then break something live and let a test catch it.** That answers the published viva question by doing it.
- **The strongest part of the presentation is where you were wrong**, because everyone in the room has been wrong the same way and can see the pretence. *"We could have managed our time better"* is what people say instead of a finding.
- **Five slides.** The demo is not a slide and neither is code. **Label where the invariant is enforced on the diagram**, because a diagram outruns its caveats.
- **The report carries twice the demo's marks.** Its distinguishing sections are **what you chose not to build** and **an ADR you would now reverse.**

**Next:** L38 — engineering management: what the evidence says about teams, estimation and incidents, and which of this course's practices survive contact with an organisation.

---

*CS 212 · Week 12 · L37 · © CSE Department*
