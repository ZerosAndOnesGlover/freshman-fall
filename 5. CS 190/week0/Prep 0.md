---
assessment: Prep 0
course: CS 190
component: Seminar Prep
possible: 10
score: 10
status: graded
started: 2026-09-21
submitted: 2026-09-23
graded: 2026-09-24
source: "Prep Assignment.md"
---

# CS 190 · Prep 0
## What is Computer Science? Careers in CS, Software, and Hardware Engineering

**Assessment:** `Prep Assignment.md` (Week 0)
**Due:** Wednesday 23 September 2026, 12:00 — before the 13:00 seminar
**Grading:** Participation component — credit/no-credit (completion and evident effort; there is no
"correct" answer)

> Written under the prep sheet's headings, after the lecture notes and the three required readings.

---

### Part A — Reading Notes

For each required reading: central claim, strongest support, strongest counterargument, my position.

#### 1. Dijkstra, "On the Cruelty of Really Teaching Computing Science" (EWD1036)

| | |
|---|---|
| **Central claim** | Computer science is a branch of mathematics, not a craft. Teaching it as vocational programming rather than applied mathematics is a category error that keeps the field professionally immature. |
| **Strongest support** | The subject matter — correctness, termination, complexity — is genuinely formal, and the evidence is historical: Turing did the foundational work a decade before a working stored-program computer existed, so the mathematics was never downstream of the hardware. |
| **Strongest counterargument** | The formal core is real but partial. It says almost nothing about the coordination, changing requirements and legacy-code problems that dominate building actual systems, so "mathematics" names the field's purest subfield and mistakes it for the whole. |
| **My position** | The corrective is useful and the rhetoric is too broad. Formal habits have already changed how I reason (CS 101 proofs, loop invariants), but defining the discipline by its least-empirical part quietly excludes software engineering, which has its own standards of rigour. |

#### 2. ACM, "Computer Science as a Profession" (Computing Curricula excerpt)

| | |
|---|---|
| **Central claim** | Computing is a profession — a shared body of knowledge with curricular standards and, therefore, responsibilities — and should be understood and taught in those terms rather than as a trade. |
| **Strongest support** | Professions are defined institutionally: a consensus curriculum, a code of conduct, and a public expectation that practitioners can be relied on. The ACM/IEEE curricula reports and the Code exist to supply exactly those, the way accreditation does in other fields. |
| **Strongest counterargument** | Calling a field a profession does not make it one. Law, medicine and civil engineering enforce entry through licensure and personal liability; computing has neither, so the framing can read as aspiration dressed up as description. |
| **My position** | It converges with Dijkstra that the field is more than tooling, but diverges on what the core is — institutional consensus rather than pure mathematics. The professional framing is the more useful one to me, because it ties competence to responsibility, which is the point of this seminar. |

#### 3. Russell & Norvig, *AIMA* 4th ed., §1.1 ("What is AI?")

| | |
|---|---|
| **Central claim** | "AI" is best defined by crossing two axes — thinking versus acting, and humanly versus rationally — and the "rational agent" quadrant is the most productive working definition. |
| **Strongest support** | The taxonomy is genuinely clarifying. Separating "humanly" from "rationally" escapes the trap of treating human behaviour as the gold standard, when humans are routinely the least rational reference available. |
| **Strongest counterargument** | "Acting rationally" still leaves the objective unspecified — rational with respect to whose goal? The definition brackets the value question instead of answering it, and that is exactly where the contested ethics of AI actually live. |
| **My position** | It is this week's method applied to a subfield: define the field by its central question. It also quietly undercuts the neutrality myth, since choosing "rational agent" as the frame is a value-laden decision about what matters, made before any system gets built. |

*Credit: awarded*

---

### Part B — Discussion Question (Q9: Civil vs. software ethics)

I think software engineering ethics has to look *different* from civil engineering ethics, not merely
newer, and the difference is visibility and blame-assignment. A bridge collapse has a moment, an
identifiable victim, and a causal chain short enough to trace, which is what makes licensure and
personal liability work: you can stamp a drawing and hold the person who signed it responsible. A
biased hiring algorithm has no single moment of failure, no individual who is identifiable in the
aggregate, and a causal chain distributed across data collection, proxy choice, and deployment
decisions. The civil-engineering mechanism — a licensed seal of approval before the fact — does not
transfer, because you cannot stamp a data pipeline the way you stamp a structural calculation. What
does transfer is the underlying habit of externalising safety as a checkable artifact *before* harm,
which in software looks more like code review, staged rollout and audit than like a licence. So
software's version of professional ethics is likely to be continuous and process-based where civil
engineering's is gate-based and terminal.

*Credit: awarded*

---

### Part C — One Question for the Class

The reading guide asks whether machine learning — where systems exhibit behaviour hard to describe
except in quasi-anthropomorphic terms — has broken Dijkstra's argument against anthropomorphic
language. I would push it further, as a devil's advocate: if it has, does that mean Dijkstra's
"CS is mathematics" thesis was merely incomplete, or that it was *wrong about the future* — that the
mathematics-only view was a claim about the field's past that the field's present has quietly
overtaken?

*Credit: awarded*

---

## Grading Summary

| | |
|---|---|
| **Score** | 10 / 10 |
| **Percent** | 100% |
| **Graded** | 2026-09-24 |

| Part | Marks |
|---|---|
| A — Reading notes (3 readings × 4 questions) | Credit |
| B — Discussion question answer | Credit |
| C — Question for the class | Credit |
| **Total** | **Credit (10 / 10)** |

**Feedback:** Full participation credit. All three readings are covered with the required four
questions each, and the notes distinguish the authors' claims rather than summarising the topic.
Two strengths worth naming, because they are what the credit is for: Part A separates Dijkstra's
*claim* from his *rhetoric* (useful corrective, overbroad conclusion) rather than accepting or
rejecting him wholesale, and it notices on the Russell & Norvig excerpt that the choice of frame is
itself value-laden — the neutrality-is-a-myth argument arriving from a direction the lecture did not
take. Part B answers the question it was asked (does software ethics differ in kind, not just in age)
and justifies "different" with a mechanism — visibility and blame-assignment — instead of asserting
it. Part C offers a genuine challenge rather than a clarifying question: is the mathematics thesis
falsified by ML, or only outrun. Credit awarded; bring Part C to the seminar, it is worth spending
time on.

---
*CS 190 · Week 0 · Prep 0 · Adebayo Glover*
