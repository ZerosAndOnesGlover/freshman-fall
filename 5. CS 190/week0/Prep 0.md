---
assessment: Prep 0
course: CS 190
component: Seminar Preparation
possible: 10
score: 10
status: graded
started: 2026-09-27
submitted: 2026-09-28
graded: 2026-09-28
source: "Prep Assignment.md"
---

# CS 190 · Prep 0

## Answer Sheet

**Assessment:** `Prep Assignment.md`
**Points available:** 10

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Answer

**Your answer:**

#### Part A: Reading Notes

_1–2 sentences per line._

##### 1. Dijkstra — "On the Cruelty of Really Teaching Computing Science" (EWD1036, 1988)\*\*

- **Central claim:** Computer science education should teach students rigorous ways of thinking rather than primarily teaching programming languages or practical techniques.

- **Strongest supporting evidence/reasoning:** Dijkstra argues that programming is intellectually demanding because students must learn to reason precisely about abstractions, correctness, and complexity; therefore, education should cultivate mathematical and disciplined thinking.

- **Strongest counterargument:** An excessive emphasis on formal reasoning may leave students underprepared for the practical skills—tools, languages, teamwork, and software-development practices—that professional computing requires.

- **My position:** I agree with Dijkstra because of what use is the attractiveness of a field if students are not prepared for its intellectual demands? A strong foundation in rigorous thinking prepares students to face the difficult realities of the field rather than simply learning the easier, more immediately practical aspects and encountering the deeper challenges later. Practical skills can be acquired over time, but the ability to reason rigorously provides a foundation for learning and adapting to those skills.

##### 2. ACM/IEEE Computing Curricula — "Computer Science as a Profession" (excerpt)

- **Central claim:** Computer science is a broad professional discipline encompassing foundational knowledge, theory, practice, and professional responsibilities; not merely programming.

- **Strongest supporting evidence/reasoning:** The Computing Curricula framework organizes CS around areas such as algorithms, programming, architecture, operating systems, networking, databases, and mathematics, demonstrating that programming is only one component of the discipline.

- **Strongest counterargument:** Because software development is a major practical application of CS, some may argue that curricula should devote substantially more time to directly employable programming and development skills.

- **My position:** I agree with the ACM's position because focusing too heavily on development skills can cause students to overlook the foundational principles that make those skills adaptable and sustainable. Once students understand the underlying concepts, they can more easily learn new languages, frameworks, and technologies because they are learning how the technology works rather than merely learning how to use it.

##### 3. Russell & Norvig, _AI: A Modern Approach_, 4th ed., §1.1 "What is AI?"

- **Central claim:** AI is a broad field concerned with creating agents that perceive their environment and act to achieve goals, with several competing definitions based on human-like behavior, rational behavior, thought, and action.

- **Strongest supporting evidence/reasoning:** The authors show that these different definitions capture genuinely different research traditions, explaining why AI cannot be reduced to simply "making computers think like humans."

- **Strongest counterargument:** Defining AI primarily through rational agents can underemphasize human intelligence, cognition, creativity, and other characteristics that many researchers consider central to intelligence.

- **My position:** I believe human intelligence involves more than rational decision-making because it is shaped by consciousness and the complexity of human experience. Humans can make judgments that appear counterintuitive because their decisions can be influenced by experiences, emotions, context, and knowledge that may seem unrelated to the immediate problem. Because humans are multifaceted and conscious beings, this suggests that rational action alone may not fully capture what we mean by human intelligence.

#### Part B: Discussion Question

_Pick one of Q3–Q10 (not the warm-ups 1–2). Write 4–6 sentences you'd be willing to say out loud._

**Question chosen:** Question 4: The lecture argues the boundaries between CS/SE/CE are "porous in practice." Can you think of a real engineering decision where getting the _category_ wrong — treating an SE problem as if it were a pure CS problem, or vice versa — would lead to a bad outcome?

**My answer:** Yes. A good example is designing a banking system's transaction-processing service.

If you treat it as a pure CS problem, you might focus on algorithms, data structures, concurrency, and correctness. For example, finding an efficient way to process millions of transactions concurrently. But you might overlook SE concerns such as requirements, maintainability, failure recovery, deployment, monitoring, security, and how the system will actually be operated by a bank.

Conversely, if you treat it purely as an SE problem, you might focus on requirements, architecture, testing, and deployment while choosing an inefficient concurrency algorithm or misunderstanding database consistency. The system could be well-engineered operationally but still perform incorrectly or become unusably slow at scale.

So the category error is assuming that one discipline's tools are sufficient. CS provides fundamental computational knowledge, while SE applies that knowledge to building and maintaining reliable systems in the real world.

#### Part C: My Question for the Class

_Clarifying, devil's-advocate, or genuine confusion — something the readings or lecture left unresolved._

**Question:** Why is Computer Science, Software Engineering, and Computer Engineering separate fields that seems not to lay the same foundations?

**What prompted it:** I see many CS students lack basic CE knowledge and many SE students lack basic CS foundations. At least, for the Year 1 and Year 2 (fall semester at least), everyone should have a common learning curriculum before branching out to the CS, SE, or CE specializations.

---

_Marks: 10 / 10_

---

## Grading Summary

_Filled in by the grader._

|             |             |
| ----------- | ----------- |
| **Score**   | **10 / 10** |
| **Percent** | 100%        |
| **Graded**  | 2026-09-28  |

**Feedback:**

_Grading basis: `assignments/Prep Assignment.md` — "Graded credit/no-credit on completion and
evident effort, not on 'correctness' (there isn't one)."_ No deduction below is charged against the
score; the critiques are recorded for the position papers, where written argument quality is the
thing actually marked.

**All three parts are complete, and the work is well past the threshold this assignment sets.**
Part A carries the full four-question structure for all three required readings — no reading is
skipped and no prompt is left blank. Part B picks Q4, which is a genuine non-warm-up question from
Part 2 of the Discussion Questions, and actually attempts it. Part C supplies both the question and
the prompting observation, which is what the prompt asks for and which several sheets omit. The
assignment sets one page at "low-friction… a thinking tool, not a polished deliverable"; this is
roughly three pages of substantive prose, so the effort is evident on any reading.

**Part B is the strongest thing on the page and the part most worth keeping.** The question asks
for a case where miscategorising the problem leads to a bad outcome, and the answer runs the error
in _both_ directions — treating an SE problem as pure CS, and then treating a CS problem as pure SE
— which is the harder half of the ask and the one most often skipped. The banking
transaction-processing example is concrete, the failure modes named on each side are the right ones
(concurrency and database consistency on the CS side; requirements, monitoring, and operations on
the SE side), and it is genuinely sayable aloud as required. The closing line — that the category
error is assuming one discipline's tools are sufficient — is an abstraction rather than a
restatement, which is what separates a usable answer from a competent one.

**The three counterarguments in Part A are genuine steelmen, not dismissals, and the Russell &
Norvig one is the sharpest** — that defining AI through rational agents underweights human
intelligence, cognition and creativity is a real objection that the reading's own framing invites,
and it is stated as a position someone could actually hold. All three "My position" entries take a
stand and give a reason for it rather than splitting the difference.
