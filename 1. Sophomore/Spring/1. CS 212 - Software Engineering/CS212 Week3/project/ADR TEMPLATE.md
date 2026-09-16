# NNNN. <Short title, a statement not a question>

Date: YYYY-MM-DD
Status: proposed | accepted | superseded by [NNNN](NNNN-....md) | deprecated

## Context

*The forces. What situation are we in, and why does a decision have to be made now?*

**Put a number or an observation in here.** "Our tests are slow" is a feeling; "our suite takes 94 s
and we expect to triple the test count by May" is a context. A future reader needs to know whether
the pressure that produced this decision still exists.

## Decision

*What we will do. Present tense, active voice: "We will…", "The domain layer does not…".*

**Specific enough to be violated.** If nobody could tell whether the codebase obeys this, it is not a
decision, it is a sentiment.

## Consequences

*What becomes true, good and bad.*

**At least two negatives, and they must be concrete.**

+
+
−
−

## Alternatives considered

*What else we could have done, and why each lost.*

**This is the section that answers the question someone asks in March**, and it is the section
everyone omits. The alternative that lost is often the one a later reader is about to propose again.

- **<Alternative>.** <Why it lost — and if it lost narrowly, say so.>
- **<Alternative>.**

---

> **Rules for this directory**
>
> 1. **Numbered sequentially, never renumbered.** `0001`, `0002`, …
> 2. **Never edit an accepted ADR.** To change your mind, write a new one that supersedes it and
>    set the old one's Status to `superseded by NNNN`. **The record of having changed your mind is
>    the most valuable thing in here**, and the final report asks for one.
> 3. **Write it when you decide, not later.** An ADR reconstructed from memory keeps the decision
>    and loses the alternative, which is the part worth keeping.
> 4. **One page.** If it needs more, the decision is more than one decision.
