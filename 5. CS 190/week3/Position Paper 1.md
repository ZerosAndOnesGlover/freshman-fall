---
assessment: Position Paper 1
course: CS 190
component: Position Papers
possible: 100
score: 100
status: graded
started: 2026-10-15
submitted: 2026-10-21
graded: 2026-10-23
source: "Position Paper 1.md"
---

# CS 190 · Position Paper 1
## Professional Obligation and the Limits of Employer Loyalty

**Assessment:** `Position Paper 1.md` (released Week 3)
**Due:** Wednesday 21 October 2026, 12:00 — before the Week 4 seminar
**Length:** 750–1,000 words (hard limits)
**Weight:** Position Papers — 60% of the course grade (one of three)

---

**Adebayo Glover**
**21 October 2026**
**CS 190 — Position Paper #1**

## Professional Obligation and the Limits of Employer Loyalty

I will defend a specific claim. An engineer who holds credible, documented evidence that a system
she is building or maintaining poses a serious, foreseeable risk of public harm is obligated to
press that concern through the internal channels that exist; if those channels are genuinely
exhausted without a remedy, external disclosure is not merely permitted but *required*. Employer
loyalty is a real professional good, but it is subordinate to the obligations the ACM Code assigns
to the public, and it was never a shield behind which an engineer could knowingly ship harm and call
it duty.

Read honestly, the Code does not merely permit this hierarchy — it mandates it. Principle 1.1 makes
"all people" stakeholders in computing and adds that those who build wide-scale systems "bear a
special responsibility to act in the public interest." That is a statement that the obligation is
owed to people who are neither the employer nor the customer. Principle 1.7 is blunter still: the
duty to honor confidentiality "does not apply" when the professional is asked to keep secret
something that would "endanger health or safety." The Code therefore anticipates precisely the
employer–engineer conflict and resolves it before the conflict arises: confidentiality is real, but
it stops at the concealment of danger. To insist that loyalty to the firm overrides that is to read
the document against its plain text.

Principle 1.2 supplies the mechanism. It defines harm broadly and, crucially, converts avoidance
into a positive duty: "If harm is suspected, it must be reported to a responsible party." A harm
that has been reported internally and ignored has not been discharged; the report is a step, not a
terminus. Principle 2.3 reinforces the point from the other side, framing law as a floor rather than
a ceiling: an employer's assurance that a system is "compliant" answers the legal question, not the
ethical one the Code poses. And 2.5 — to give "comprehensive and thorough evaluations of computer
systems and their impacts, with special emphasis on possible risks" — makes the discovery of a risk
the beginning of an obligation rather than the end of a project.

Consider the lecture's Scenario A. An engineer testing a law-enforcement facial recognition system
finds a 34% error rate for dark-skinned women against 1% for light-skinned men, and is told the
system ships in two weeks because the contract matters. The Code is not ambiguous here: shipping is
1.4's discrimination, 1.2's foreseeable and unnecessary harm, and 1.1's betrayal of stakeholders who
never consented. Supervisors overruling a measured 34% error rate are not exercising a business
judgment the engineer must defer to; they are instructing her to participate in a harm the Code
forbids. The real analogue is Frances Haugen, who documented from inside harms that Facebook's own
research had established, escalated internally, found that route inert, and eventually disclosed to
regulators and the public. Whatever one thinks of her tactics, the structure of the case is the one
the Code legislates for: internal voice first, external voice when internal voice fails.

But the obligation I am defending has a serious counterargument, and it is not the one usually
offered. The weak version — "you will be fired, and the Code does not pay your rent" — begs the
question, since a code does not waive its obligations when compliance is expensive. The strongest
version concerns the disclosure itself. Premature or unverified disclosure is not a neutral act; it
can cause the very harms it claims to prevent. A public claim that a widely used system is unsafe
can trigger panic, erode trust in a technology that is on balance beneficial, invite regulatory
overreaction, and — in the security case — hand an exploitable vulnerability to attackers before a
patch exists. And the engineer is epistemically limited: she sees one system, one metric, one slice
of the picture, and external disclosure outsources a technical judgment to a public that cannot
evaluate it. A rule permitting any employee to impose her private risk assessment on the world at
will is a rule for chaos, not for accountability.

The response is to notice what the objection actually defeats. It defeats *premature* and
*unmitigated* disclosure — an unverified risk, to the widest audience, before any less-damaging route
is tried. It does not defeat graduated disclosure: the obligation matures only after internal
remedies are genuinely exhausted and only on credible evidence, and it can be discharged through the
*narrowest effective channel* — a regulator, a safety body, a certification authority — rather than a
megaphone. A regulator does not panic, and a coordinated disclosure timeline can let a patch exist
before the public learns. I concede the residual cost is real: a world permitting external disclosure
will produce some false alarms, and those have victims too. My claim is only that this cost is
smaller than the alternative — a regime in which an organization can, by making internal channels
inert, permanently silence credible evidence of serious harm.

The practical upshot is concrete: write the concern down contemporaneously; escalate through the
named channels in writing, with dates and a deadline for response; cite the principles at stake; and,
when internal resolution fails, take the narrowest external route that can stop the harm — a
regulator before a reporter. She should expect to pay for it; the Code's answer to the fear of cost
is that cost does not dissolve duty. Vallor's virtue framing reaches the same place from the
character side: an engineer who has formed the habit of deferring to authority over evidence is not
practicing a virtue, she is practicing obedience. What she may not do is tell herself that loyalty
to an employer is the same thing as professional responsibility. The Code's architecture — 1.1's
stakeholders, 1.7's carve-out, 1.2's duty to report — was written to make that equation impossible.
An engineer who ships a system she believes will seriously hurt people, because saying so would have
been costly, has not been loyal. She has been complicit, and the Code names it.

---

**References**

- ACM. *Code of Ethics and Professional Conduct.* Association for Computing Machinery, 2018.
  (Principles 1.1, 1.2, 1.4, 1.7, 2.3, 2.5; §4.)
- Vallor, S. *Technology and the Virtues: A Philosophical Guide to a Future Worth Wanting.* Oxford
  University Press, 2016. Ch. 1.
- "The Facebook Files." *The Wall Street Journal*, 2021.

---

*Marks: 100 / 100*

---

## Grading Summary

| Requirement | Assessment |
|---|---|
| Clear position in the opening paragraph | Yes — stated in the first paragraph and repeated unhedged |
| Engages the ACM Code specifically (≥2 principles) | 1.1, 1.2, 1.3(implicit), 1.4, 1.7, 2.3, 2.5 — quoted and analysed |
| Addresses the strongest counterargument | The unverified/premature-disclosure objection, steelmanned and answered with a concession |
| Grounded in a concrete case | Scenario A (facial recognition) + the Haugen/Facebook Files case |
| Conclusion with practical implications | Named escalation and disclosure procedure, with the cost accepted |

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-23 |

**Feedback:** A strong first position paper. The position is genuinely falsifiable — it commits to
*obligatory* external disclosure after internal exhaustion, not to a vague "engineers should care
about harm" — and it is stated in the first paragraph rather than assembled across the paper. The
Code is used as a text, not a decoration: 1.7's confidentiality carve-out is the pivot of the whole
argument, and the paper correctly reads 1.2's "must be reported" as a continuing duty rather than a
one-time act. The counterargument is the best part. You did not choose the easy "you'll be fired"
objection; you chose the one that actually threatens your position — that disclosure can itself
cause harm — stated it in its strongest form, and then distinguished premature/unmitigated
disclosure from graduated disclosure rather than pretending the objection was trivial. Conceding the
residual false-alarm cost is exactly the move the prompt asked for. The Haugen case is apt and
correctly used to show structure rather than to score a point. One refinement for Paper #2: you
repeatedly invoke "credible evidence" and "serious harm" as thresholds without specifying them; by
Paper #2 the framework has to be built rather than assumed, so expect to say what makes evidence
credible.

---
*CS 190 · Week 3 · Position Paper 1 · Adebayo Glover*
