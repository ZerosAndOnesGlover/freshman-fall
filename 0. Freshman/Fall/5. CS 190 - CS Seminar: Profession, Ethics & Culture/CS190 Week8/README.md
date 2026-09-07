# CS 190 · CS Seminar: Profession, Ethics & Culture
## Week 8: Cybersecurity Ethics — Responsible Disclosure and Hacktivism

**Format:** Weekly 1-hour seminar + readings
**Assessment for this course (overall):** Participation 40%, Position Papers 60%
**This week's deliverable:** Discussion preparation notes (participation-graded)

---

### Why This Week Exists

Almost every other week of this seminar asks what you should *build*. This week asks what you should
do when you find that something is **broken**.

That turns out to be harder, because the decision is genuinely forced. A researcher who finds a
serious flaw has no option that harms nobody: publishing arms attackers, silence leaves users
exposed, and reporting privately hands the timeline to a party with its own interests. There is no
neutral choice, only a choice about who bears the risk and for how long.

This is also the week where **ethics and law come apart most sharply**. A researcher may act with
complete integrity and still face prosecution; another may act within the law while leaving users
exposed for commercial convenience. Learning to reason about the two separately — and to notice when
you are substituting one for the other — is the practical skill this week teaches.

### Learning Objectives

By the end of Week 8, you should be able to:

1. Describe the vulnerability lifecycle and explain why the discovery-to-deployment window is where disclosure policy operates.
2. State the case for and against full, coordinated, and non-disclosure, without caricaturing any of them.
3. Explain what bug bounties, CVE, safe-harbour policies and CERT/CC each contribute, and what they do not solve.
4. Summarise what *Van Buren* changed about the CFAA and what remains legally uncertain for researchers.
5. Distinguish the legal question from the ethical one in a disclosure scenario, and reason about each on its own terms.
6. Set out the strongest case for hacktivism and the three standard objections to it — accountability, proportionality, and epistemic humility.
7. Distinguish whistleblowing from intrusion, and identify cases where the distinction is genuinely difficult.
8. Apply the ACM Code to a disclosure decision and recognise where its principles conflict rather than resolve.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[Lecture Week 8]] | The disclosure dilemma, the three models, the legal overlay, hacktivism, and the ACM Code applied |
| [[CS190 Week8/Reading Guide\|Reading Guide]] | *Van Buren*, ISO/IEC 29147, and Project Zero's disclosure policy, with guiding questions |
| [[CS190 Week8/Discussion Questions\|Discussion Questions]] | Twelve questions across disclosure, law, and hacktivism |
| [[CS190 Week8/Prep Assignment\|Prep Assignment]] | Write a disclosure policy; identify the line you would not cross |
| [[Glossary Week 8]] | Terms introduced this week, defined precisely |

### Connections

**Back:** Week 3's ACM Code supplies the framework, and this week is the first where its principles
visibly conflict with one another. Week 7's DMCA § 1201 discussion is the direct legal antecedent —
the anti-circumvention rule that makes lawful research conditional on a renewable exemption.

**Forward:** Week 9 turns to the culture of the industry that employs you, including the conditions
under which people feel able to raise concerns at all. A disclosure policy is worth little in an
organisation where nobody dares invoke it.

### A Note on Scope

This is a seminar on **professional ethics and policy**, not a technical security course. We are
concerned with how the profession decides what to do about vulnerabilities, what the law permits, and
how to reason when the two disagree. Techniques belong to CS 340 and to your own later study.

The distinction matters practically as well as pedagogically: the interesting questions in this field
are almost never technical. They are questions about incentives, accountability, and who bears risk on
whose behalf.
