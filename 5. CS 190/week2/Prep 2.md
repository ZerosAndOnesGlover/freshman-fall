---
assessment: Prep 2
course: CS 190
component: Seminar Prep
possible: 10
score: 10
status: graded
started: 2026-10-05
submitted: 2026-10-07
graded: 2026-10-08
source: "Prep Assignment.md"
---

# CS 190 · Prep 2
## How Software Gets Built — Agile, Open Source, and Research Labs

**Assessment:** `Prep Assignment.md` (Week 2)
**Due:** Wednesday 7 October 2026, 12:00 — before the 13:00 seminar
**Grading:** Participation component — credit/no-credit (completion and evident engagement)

> Written under the prep sheet's headings, after the lecture notes and the three required readings.

---

### Part A — Raymond vs. Eghbal

Eghbal *updates* Raymond rather than contradicting him, and the update is empirical: Raymond's bazaar
assumes that a crowd of contributors reviews the code, but Eghbal's contributor-to-user ratios show
that almost every widely used project is maintained by a very small number of people and consumed by
a vast, passive majority. "Given enough eyeballs, all bugs are shallow" therefore fails as a
description of open source, because the eyeballs are on the *user* side of the project, not the
*contributor* side. That matters for Raymond's reliability argument, because reliability in the
modern ecosystem comes not from distributed peer review but from a thin, often unpaid maintenance
layer — a different and far more fragile mechanism than the one he described. The two essays also ask
different questions: Raymond asks how open source gets *built*, Eghbal asks who keeps it *standing*,
and recent history answers the second one badly. Heartbleed and the xz Utils backdoor are not
anomalies under Eghbal's frame but predictable outcomes of it — critical code with a handful of
maintainers and no funding. Where Raymond needs revision, then, is in substituting "many users" for
"many reviewers": the crowd contributes bug reports and demand, not patches, and the sustainability
question he never poses is the one that decides whether the software survives.

*Credit: awarded*

---

### Part B — A License Question

**1. Copyleft or permissive?** I would start with a **permissive** license (Apache 2.0), because the
value of a signal-processing library is in wide adoption and the permissive licence removes nearly all
legal friction for the people who might build on it. I am not trying to protect a competing business
here, so the enclosure that copyleft guards against is not the threat I am most worried about. Apache
2.0 over MIT specifically because its explicit patent grant is worth having for anything a company
might embed.

**2. Three major streaming companies will incorporate it without contributing back.** This changes my
answer: that scenario is exactly the enclosure copyleft exists to prevent, and it converts "wide
adoption" from a good into free-riding on eight months of unpaid work. Note that plain GPL would not
reach this case, because server-side use is not distribution — which is why the answer is
specifically **AGPL-3.0**: it extends the source-provision obligation to network use, so those
companies either contribute their improvements back or do not use the library.

**3. University music-cognition researchers are the primary users.** Now my answer changes *back*
toward permissive. Academic groups already operate under norms of publication and citation that make
them disposed to share derived work, and copyleft adds licence-compatibility and legal-review friction
to a community that does not need the obligation to motivate it. The enclosure risk I was guarding
against is largely absent here, so permissive serves both parties better — which shows that the
licence is a means to an end, chosen by who I want to build on the code and what I want to protect.

*Credit: awarded*

---

### Part C — Process Observation

On a PROG 101 group project we were graded on a small C program, and the process was implicit rather
than chosen: three of us split the required functions, committed to a shared Git repository, and
integrated roughly once a week with no sprints, backlog, or retrospectives. If it resembled anything
from the lecture, it was continuous-flow **Kanban** rather than Scrum — work simply moved through
"not started / in progress / merged", with an informal review step when someone else read the diff.
What we did not have was any explicit treatment of the two problems the lecture names: our
requirements did not really change, so the waterfall-style planning was fine, but our coordination
complexity showed up as merge conflicts and duplicated helper functions, which is exactly the cost
methodologies exist to manage. In a larger or longer project I would want a sprint cadence and a
retrospective, not because the rituals are inherently good but because we had no feedback loop at all.

*Credit: awarded*

---

## Grading Summary

| | |
|---|---|
| **Score** | 10 / 10 |
| **Percent** | 100% |
| **Graded** | 2026-10-08 |

| Part | Marks |
|---|---|
| A — Raymond vs. Eghbal | Credit |
| B — Licence question | Credit |
| C — Process observation | Credit |
| **Total** | **Credit (10 / 10)** |

**Feedback:** Full participation credit. Part A synthesises rather than summarises, which is what the
prompt asked for: the key move — that Raymond asked how open source gets built while Eghbal asked who
keeps it standing — is a real reconciliation, and substituting "many users" for "many reviewers"
correctly identifies *where* Raymond's premise breaks. Part B is the strongest part: it does not treat
the licence choice as an identity but as a means, and it changes its answer for good reasons in both
directions. The GPL-versus-AGPL distinction in part 2 is exactly right and is the technical point most
answers miss — server-side use is not distribution, which is the entire reason AGPL exists. Part C
honestly reports an ad-hoc process and, more usefully, diagnoses it against the lecture's own
framework (changing requirements versus coordination complexity) instead of just naming a method it
resembled.

---
*CS 190 · Week 2 · Prep 2 · Adebayo Glover*
