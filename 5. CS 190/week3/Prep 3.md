---
assessment: Prep 3
course: CS 190
component: Seminar Prep
possible: 100
score: 100
status: graded
started: 2026-10-12
submitted: 2026-10-14
graded: 2026-10-15
source: "Prep Assignment.md"
---

# CS 190 · Prep 3
## Ethics in Computing — The ACM Code of Ethics and Professional Responsibility

**Assessment:** `Prep Assignment.md` (Week 3)
**Due:** Wednesday 14 October 2026, 12:00 — before the 13:00 seminar
**Grading:** Participation component — credit/no-credit (completion and evident engagement)

> Written under the prep sheet's headings, after the lecture notes, the ACM Code (all four sections),
> Gotterbarn et al., and Vallor Ch. 1.

---

### Part A — Code Mapping

**Scenario A (facial recognition; 34% error rate for dark-skinned women, 1% for light-skinned men).**

| Principle | Why it applies |
|---|---|
| **1.4** Be fair and take action not to discriminate | The measured error disparity across a protected characteristic is the paradigm case this principle names; that the system is "accurate" in aggregate is irrelevant when the error is distributed by skin colour and sex. |
| **1.2** Avoid harm | The harm is *foreseeable* — the company has already measured it — and "unnecessary," since shipping in two weeks is a business deadline, not a technical necessity. |
| **1.1** Contribute to society; all people are stakeholders | The people misidentified as criminal suspects are stakeholders who never agreed to be in the system and bear the consequences of its errors. |
| **2.1** Strive for high quality in products | Knowingly shipping a system whose error rate is known to be 34% for a sub-population is a quality failure with ethical weight, not merely a scheduling compromise. |

**Scenario B (hospital legacy system; vulnerability exposing patient records, fix needs an unfunded six-month refactor).**

| Principle | Why it applies |
|---|---|
| **1.2** Avoid harm; report suspected harm to a responsible party | Patient records exposed to unauthorized access is exactly the harm this principle obliges the professional to report, and it names a positive duty to escalate rather than a mere duty to avoid. |
| **1.6** Respect privacy | Medical records are the clearest case of data whose collection and protection the code governs, and the vulnerability defeats that protection. |
| **1.7** Honor confidentiality (with its limit) | Confidentiality to the employer is real, but the carve-out applies: the code removes the duty when secrecy would endanger health or safety, which is what concealing the vulnerability does. |
| **2.5** Give comprehensive and thorough evaluations of systems and their impacts | The engineer has effectively performed that evaluation and discovered a risk; the principle frames the discovery as the *start* of an obligation, not the end of one. |

*Credit: awarded*

---

### Part B — Preparing for Your Position Paper

My provisional position: an engineer who holds credible evidence that a system poses a serious,
foreseeable risk of public harm is obligated to press the concern through the internal channels that
actually exist, and once those routes are genuinely closed — not merely inconvenient — external
disclosure becomes permitted, and in serious enough cases obligatory. The obligation is **graduated**
rather than absolute: it scales with the severity and imminence of the harm and with how completely
internal remedies were exhausted, so a minor and speculative risk obliges nothing beyond a
documented email, while a serious and imminent one can oblige disclosure to a regulator. The
principles doing the most work are **1.2** (avoid and report harm), **1.7** (confidentiality does not
extend to concealing danger), and **1.1** (all people are stakeholders), with **2.3** establishing
that legality is a floor rather than a ceiling. My real uncertainty is the *threshold*: how certain
and how serious must the evidence be before the obligation to go external attaches, and who gets to
be the judge of that — because a threshold set too low licenses reckless disclosure, and one set too
high makes the obligation vanish in practice.

*Credit: awarded*

---

### Part C — One Strong Objection

The claim proves too much and too little at once, because it makes *procedure* rather than *harm* the
measure of the violation. An engineer can tick every box — file the ticket, escalate to the manager,
copy the director, document diligently — and still ship a system she believes will hurt people; on the
claim as written she has satisfied her obligations, even though nothing was prevented. Meanwhile the
engineer whose employer quietly dissolved the internal channels (access revoked, escalation path
reported to a line manager with an interest in silence, concerns logged into a system no one reads)
has done everything that was *available* and is still condemned for not having done more. If the
obligation is really about preventing harm, its measure cannot be an unbounded list of internal
gestures; the honest version of the claim would be that an engineer violates her obligations when she
fails to take *reasonable and proportionate* steps, having weighed the seriousness of the risk against
the realistic effectiveness of the channels open to her — which is a much weaker, and more defensible,
claim than the one printed above.

*Credit: awarded*

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-15 |

| Part | Marks |
|---|---|
| A — Code mapping (Scenarios A and B) | Credit |
| B — Position-paper sketch | Credit |
| C — Strongest objection | Credit |
| **Total** | **Credit (100 / 100)** |

**Feedback:** Full participation credit. Part A maps principles to scenarios rather than merely
listing them, and the annotations distinguish the *reason* each principle bites (1.2's
"unnecessary"/"foreseeable" qualifiers, 1.7's carve-out, 2.1's quality-as-ethics). Part B is a real
position with a structure — graduated obligation, severity and exhaustion as the two dials — rather
than a restatement of the prompt, and it names its own uncertainty (the threshold) instead of
pretending to have resolved it; that uncertainty is likely the hardest part of the paper, so fronting
it now is the right instinct. Part C attacks the claim at its weakest structural point — it measures
process rather than harm — and proposes the repair, which is stronger work than arguing that
disclosure is simply risky. One caution for the paper itself: do not let the graduated framing
collapse into hedging; commit to what the threshold *is* when you write Paper #1, even if provisionally.

---
*CS 190 · Week 3 · Prep 3 · Adebayo Glover*
