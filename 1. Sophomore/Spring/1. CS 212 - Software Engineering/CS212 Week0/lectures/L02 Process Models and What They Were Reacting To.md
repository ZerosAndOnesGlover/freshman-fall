# CS 212 · Software Engineering
## Week 0 · Lecture 2 of 3
### Process Models, and What They Were Reacting To

*“The management question, therefore, is not whether to build a pilot system and throw it away. You will do that. [...] Hence plan to throw one away; you will, anyhow.”* — Fred Brooks, *The Mythical Man-Month* (1975), ch. 11

---

**Sat:** first Thursday of Week 0, 10:00–10:50, TH 200 · **Reading:** Sommerville Ch. 2 · **Next:** L03, the Agile Manifesto read critically

**Coursework:** 📝 **Assignment 0** released Wed this week 17:00, due Fri of Week 1 17:00 · 📋 **Team formation workshop** Thu this week 10:00–10:50

---

## 1. A Process Model Is an Answer to "When Do We Find Out?"

Every software process — waterfall, spiral, Scrum, whatever your first employer calls theirs — is an answer to one question:

> **How long are we willing to go before we find out we were wrong?**

That is the only variable. Requirements are wrong, designs are wrong, estimates are wrong; this is not a failure of professionalism, it is the ordinary condition. **A process does not prevent being wrong. It decides how much you will have built by the time you notice.**

Hold that question through the next four sections. Each model below is a different bet on it, and each bet is right under conditions you can state.

---

## 2. The Waterfall Paper Argues Against the Waterfall

**Winston Royce, 1970**, *"Managing the Development of Large Software Systems"*, Proceedings of IEEE WESCON. This is the paper every textbook cites as the origin of the waterfall model. It contains the familiar diagram — requirements, analysis, design, coding, testing, operations, each flowing into the next.

**It appears on page 2, as Figure 2, and the text beside it reads:**

> "I believe in this concept, but the implementation described above is risky and invites failure."
> — Royce, 1970, p. 329

The remaining seven pages describe **five modifications** to fix it, and they are, in modern vocabulary:

| Royce's fix (1970) | What we call it now |
|---|---|
| "Program design comes first" | Architecture spike before committing to requirements |
| "Document the design" | ADRs, design docs, the thing Week 11 is about |
| **"Do it twice"** — build a pilot version and throw it away | **Prototyping; the walking skeleton; your Phase 1** |
| "Plan, control and monitor testing" | Test strategy, the pyramid, Week 5 |
| **"Involve the customer"** — formally, at three separate points | **The whole of the Agile Manifesto's third value** |

**The single most influential diagram in software engineering is a figure its own author labelled as inviting failure**, and the paper's actual recommendation — build it twice, show the customer early — is iterative development. The misreading happened because the diagram is memorable and the caption is not, and because the US Department of Defense standard **DOD-STD-2167 (1985)** wrote the single-pass version into contracts, where it stayed for a decade.

> **Two lessons, and the second is the one people skip.** First: pure single-pass waterfall was
> never seriously proposed by the person credited with it. Second: **a diagram will outrun its
> caveats.** You will draw architecture diagrams in Week 3 and they will be quoted back at you
> without the paragraph that qualified them. Write the caveat *into* the diagram.

---

## 3. The Sequential Model, Stated Fairly

It is fashionable to sneer at waterfall. Do not; it is the right model for some work and you should be able to say which.

**The model.** Complete each phase, review it, sign it off, proceed. Changes to a signed-off phase go through a formal change-control process.

**What it buys:**
- **A fixed price and a fixed date are possible**, because the scope is fixed first. No agile process can promise both; this one can.
- **Traceability.** Every line of code traces to a design element, which traces to a requirement. This is not bureaucracy when the regulator is the FAA or the FDA — **DO-178C** for airborne software requires exactly this, and the Therac-25 is the argument for it.
- **It works when requirements genuinely do not move**: a payroll system implementing a published tax code; a device whose specification is a physical standard; a re-implementation of something that already exists.

**What it costs**, and the number is the memorable part. Boehm's data from TRW and IBM in the 1970s–80s, reproduced in *Software Engineering Economics* (1981):

| Defect introduced in | Found in | Relative cost to fix |
|---|---|---|
| Requirements | Requirements | **1×** |
| Requirements | Design | ~5× |
| Requirements | Coding | ~10× |
| Requirements | Testing | ~20× |
| Requirements | **Production** | **~100×** (and up to 1,000× for large systems) |

**This curve is why late feedback is expensive**, and it is the whole argument for every process invented after 1970. It is also **contested**: Beck argued in *Extreme Programming Explained* (1999) that the curve is not a law of nature but a consequence of the practices around it, and that with automated tests, continuous integration and small releases it flattens dramatically. **He is substantially right, and the flattening is the thing you build in Weeks 5–8.**

Both claims can be true: change is expensive *if you have no way to know what your change broke*, and the cost of finding out is what your CI pipeline buys you. **Week 8 measures that price on your own project.**

---

## 4. Iterative and Incremental, and the Spiral

Between the sequential model and Agile sit two ideas that matter on their own.

**Incremental** — deliver working subsets, in order of value. Release 1 books a room; release 2 adds recurring bookings; release 3 adds equipment. Each release is usable.

**Iterative** — go through the same subset repeatedly, improving it. Version 1 books a room crudely; version 2 books it correctly; version 3 books it under load.

**They are different and most real processes do both.** Your project is incremental across the term and iterative within each week.

**Boehm's spiral model (1988)** adds the variable the others leave implicit: **risk**. Each loop of the spiral does four things — determine objectives, **evaluate alternatives and identify risks**, develop and verify, plan the next loop — and the second quadrant is the contribution. **You spend the next iteration on whatever would hurt most if you were wrong about it.**

That is a genuinely useful instruction and you should apply it in Week 1:

> **Ask your team: what is the thing we believe that, if false, costs us the most?**
> For most `slot` teams it will be one of: "we can model recurring bookings in the schema we drew",
> "the auth library we picked works with FastAPI", or "we can all run the project on our own
> laptops". **Do that first, this week, badly.** A walking skeleton in Week 1 is worth more than a
> perfect domain model in Week 5.

---

## 5. Why Sequential Delivery Fails in Practice: One Number

The Chaos-report figures are unreliable (L01 §8), so here is a claim with better provenance.

**Standish's own 2002 data, reported by Jim Johnson**, on features delivered in custom software:

| Feature usage in delivered systems | Share |
|---|---|
| Always used | 7% |
| Often used | 13% |
| Sometimes used | 16% |
| Rarely used | 19% |
| **Never used** | **45%** |

**Around two-thirds of delivered features are rarely or never used.** Even discounting heavily for the methodology, the direction is not in dispute and has been replicated in smaller studies since.

**The implication is not "build less".** It is: **you cannot tell in advance which third matters, and no amount of requirements analysis will tell you, because users cannot reliably predict their own behaviour.** The only reliable way to find out is to ship something and watch. That is the argument for short cycles, and it is a stronger argument than the cost-of-change curve because it does not depend on Boehm's numbers being right.

**This is YAGNI's evidential basis** (Week 2), and it is why Week 1's user stories are required to carry an *acceptance criterion you could observe*, not a description of a feature.

---

## 6. The Process Models, Side by Side

| Model | Bets that | Finds out you were wrong after | Use it when |
|---|---|---|---|
| **Sequential (waterfall)** | Requirements are knowable up front | **The whole project** | Requirements are fixed by law, physics or a published standard; a regulator requires traceability; fixed price and fixed date are contractual |
| **V-model** | Same, plus: every spec level has a matching test level | The whole project, but with a test plan written early | Safety-critical work — DO-178C, IEC 62304 |
| **Incremental** | Value can be ordered and delivered in slices | **One release** | You can split the system into independently useful pieces |
| **Spiral** | The biggest risk should be attacked first | **One loop** | Large, novel, expensive-to-be-wrong systems |
| **Scrum** | A cross-functional team can plan two weeks at a time | **One sprint** | Requirements move; the customer is reachable; the team is stable |
| **Kanban** | Work should flow, and limiting work-in-progress beats estimating | **One work item** | Unpredictable arrival of work: support, platform, ops |
| **XP** | Technical practices are what make change cheap | **One test run, minutes** | You control the codebase and can adopt TDD, pairing and CI wholesale |

**Read the third column down.** That column is the entire history of the field: from a project, to a release, to a loop, to a sprint, to an item, to minutes. **Every process innovation since 1968 has shortened the feedback loop, and nothing else about them is common.**

> **The course in one sentence, again.** Weeks 5–8 — testing, coverage, review, CI — are the
> machinery that makes the loop short enough to be worth shortening. Without them, "we do
> two-week sprints" is a calendar, not a process.

---

## 7. What Scrum and Kanban Actually Prescribe

You will be asked in interviews. Know the mechanics, and know which parts are load-bearing.

**Scrum** (Schwaber & Sutherland; the *Scrum Guide*, current edition 2020) is small:

| Element | What it is | Load-bearing? |
|---|---|---|
| **Sprint** | A fixed-length box, 1–4 weeks, whose scope does not change once started | **Yes** — the fixed box is the entire mechanism |
| **Product Backlog** | An ordered list of everything wanted, owned by one person | **Yes** — "ordered" and "one person" both |
| **Sprint Review** | Show working software to stakeholders at the end | **Yes** — this is the feedback loop closing |
| **Retrospective** | The team changes its own process | **Yes** — and it is the first thing teams drop |
| Daily Scrum | 15 minutes, team-facing, to re-plan the day | Often degenerates into status reporting to a manager, at which point it is worthless |
| Story points, velocity | Relative estimation and a measured rate | **No** — not in the Scrum Guide as a requirement; frequently abused as a productivity metric (Week 11) |

**Kanban** (Anderson, 2010) is smaller still: **visualise the work, limit work-in-progress, measure flow.** The WIP limit is the whole idea. Little's Law gives it teeth:

$$L = \lambda W \quad\Longrightarrow\quad W = \frac{L}{\lambda}$$

where $L$ is items in progress, $\lambda$ is throughput, $W$ is the average time an item takes. **If throughput is roughly fixed by the team's capacity, halving the number of things in flight halves how long each takes.** Starting more work does not finish more work; it just makes everything late simultaneously.

**Your project runs two-week iterations** — Weeks 1–2, 3–4, 5–6 (Phase 1), 7–8, 9–10, 11–12 — with a WIP limit you set yourselves and record. **A 12 asks what your WIP limit was and whether you kept it.**

---

## 8. The Honest Assessment of the Evidence

How much of §7 is *known* to work, as opposed to widely believed?

| Claim | Evidence |
|---|---|
| Shorter feedback loops reduce rework | **Strong**, and consistent across studies, though effect sizes vary widely |
| Continuous integration reduces integration failure | **Strong** — the DORA programme (Forsgren, Humble & Kim, *Accelerate*, 2018) links deployment frequency and lead time to organisational performance across ~2,000 organisations |
| Code review finds defects | **Moderate** — good evidence for formal inspection, weaker and messier for modern pull requests (Week 7) |
| TDD improves quality | **Weak and mixed.** Multiple controlled studies; results contradict each other. The most careful (Fucci et al., 2016) found the benefit attributable to **short cycles and frequent testing**, not to writing the test first |
| Pair programming is worth the cost | **Mixed.** Roughly 15% more total effort for fewer defects; whether that trades well depends entirely on the cost of a defect |
| Story points predict delivery dates | **Essentially none.** Counting stories works about as well |

**Notice the pattern.** The practices with the best evidence are the **mechanical** ones — automation, version control, integration frequency. The practices with the weakest evidence are the ones about **how humans should feel about their work**. That asymmetry should shape which battles you pick on a real team.

**It should also make you suspicious of this lecture.** Every table here is a summary of contested literature, and the summariser had a point to make.

---

## 9. Summary

- **A process model is a bet on how long you go before finding out you were wrong.** That is the only axis on which they differ.
- **Royce's 1970 paper argues against single-pass waterfall on its second page** and recommends prototyping and customer involvement. The misreading was locked in by DOD-STD-2167 in 1985.
- **Sequential development is correct** for fixed, regulated or already-known requirements, and its cost is Boehm's ~100× curve — which Beck argued, largely correctly, is flattened by automated testing and CI rather than being a law.
- **~2/3 of delivered features are rarely or never used**, and no amount of up-front analysis identifies which third matters. **This is a better argument for short cycles than the cost curve is.**
- **Every process innovation since 1968 has shortened the feedback loop**: project → release → loop → sprint → item → minutes.
- **Scrum's load-bearing parts** are the fixed box, the single ordered backlog, the review and the retrospective. **Kanban's is the WIP limit**, and Little's Law is why.
- **The evidence is strongest for mechanical practices and weakest for cultural ones.**

**Next:** L03 — the Agile Manifesto, all 68 words of it, read as four trade-offs rather than four slogans; what its authors have said about what happened to it; and how your project actually runs.

---

*CS 212 · Week 0 · L02 · © CSE Department*
