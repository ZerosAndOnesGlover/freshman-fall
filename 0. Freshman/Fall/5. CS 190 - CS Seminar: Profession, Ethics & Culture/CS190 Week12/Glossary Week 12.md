# Glossary — Week 12: Course-Wide Review

Not new terms. **The twelve concepts that recurred**, restated in the form the course finally arrived
at. If you retain nothing else from CS 190, retain these — and note that most of them are correctives
to a comfortable idea rather than the comfortable idea itself.

---

**ACM Code of Ethics** *(Week 3)* — The profession's statement of obligations. **A floor, not a
ceiling**, and not self-applying: it tells you which considerations are relevant, not how to weigh
them when they conflict. Position Paper #1 applied it; Paper #2 removed it deliberately.

**Algorithmic bias** *(Week 4)* — Systematic disparity in a system's outputs across groups. **Rarely
requires biased intent and usually survives removing the protected attribute**, because correlated
features reconstruct it. The impossibility results mean you must choose which fairness criterion to
satisfy; you cannot satisfy them all.

**Base rate** *(Week 4)* — The underlying prevalence in a population. The reason a highly accurate
classifier for a rare condition still produces mostly false positives, and the single most common
place that confident quantitative claims about screening systems go wrong.

**Complicity** *(Weeks 3, 9, 10)* — Responsibility arising from participation in a harm one did not
cause and could not prevent alone. **The concept most position papers eventually needed**, because
agent-centred frameworks handle structural harm badly.

**Dual use** *(Weeks 6, 8)* — The property of a technology that serves both protective and harmful
purposes with no technical distinction between them. Encryption, penetration tools, and generative
models are all dual use; **this is a permanent condition, not a design flaw awaiting a fix**.

**Informed consent** *(Week 5)* — Agreement given with understanding of what is being agreed to. The
concept that clickwrap terms **fail to satisfy** — and the reason regulators moved toward purpose
limitation and data minimisation, which do not depend on anyone having read anything.

**Purpose limitation** *(Week 5)* — The principle that data collected for one purpose may not be
repurposed for another without fresh justification. **More protective than consent** in practice,
because it constrains the collector rather than relying on the subject's attention.

**Responsible disclosure** *(Week 8)* — The practice of reporting a vulnerability privately with a
deadline before publication. A **negotiated compromise** between the harm of the vulnerability and
the harm of publicising it, not a moral absolute — which is why the deadline is the contested part.

**Structural harm** *(Weeks 9, 10)* — Harm produced by the aggregate of many uncoordinated decisions
rather than by any identifiable choice. **The hardest case for every framework in this course**, and
the subject of Position Paper #3.

**Supererogatory** *(Week 9)* — Praiseworthy but not required. **The distinction that Paper #3 turned
on**: arguing that conduct is admirable is easy, and arguing that failing to perform it is a wrong is
the actual task.

**Task-based analysis** *(Week 10)* — Decomposing jobs into tasks rather than treating occupations as
atomic. Yields ~9% rather than ~47% high-risk employment from comparable data. **The course's
clearest lesson in how a methodological choice, not dishonesty, produces a fivefold disagreement.**

**Whistleblowing** *(Week 8)* — Disclosure of wrongdoing outside the normal channels. **Legally
protected in narrow circumstances and personally costly in nearly all of them**; a functioning
internal process is what makes it unnecessary, which is why Week 9's material on speaking up is not
a separate topic.

---

### The One-Sentence Version

Every framework in this course was built to evaluate **actions by agents**, and the hardest problems
in computing — bias without a biased decision, harm without a decider, obligation without leverage —
**are not shaped like that**. Noticing where your tools run out is not a failure to have learned
them. It is what having learned them looks like.
