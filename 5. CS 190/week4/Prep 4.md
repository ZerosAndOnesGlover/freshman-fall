---
assessment: Prep 4
course: CS 190
component: Seminar Prep
possible: 100
score: 100
status: graded
started: 2026-10-22
submitted: 2026-10-22
graded: 2026-10-22
source: "Prep Assignment.md"
---

# CS 190 · Prep 4
## Algorithmic Bias — Case Studies in Hiring, Lending, and Facial Recognition

**Assessment:** `Prep Assignment.md` (Week 4)
**Due:** Wednesday 21 October 2026, 12:00 — before the 13:00 seminar
**Grading:** Participation component — credit/no-credit (completion and evident engagement)

> Written under the prep sheet's headings, after the Week 4 lecture notes and the Reading Guide
> (Buolamwini & Gebru 2018; Dastin 2018; Kleinberg, Mullainathan & Raghavan 2016).

---

### Part A — Mechanism Diagnosis

1. **Amazon's resume screening tool.** Primarily **biased training data**: the model was trained on ten
   years of actual hiring decisions, so the historical predominance of men in technical roles became the
   signal it learned — the gendered terms it penalised were symptoms of that biased label, not the root
   cause.

2. **Algorithmic lending discrimination via ZIP code.** Primarily **proxy variables**: ZIP code is a
   facially neutral geographic feature, but residential segregation means it reconstructs much of race's
   predictive power without race ever appearing as an input.

3. **Gender Shades' facial analysis disparities.** Primarily **non-representative sampling**: the
   benchmark datasets were heavily skewed toward lighter-skinned male faces, so the systems had less data
   to learn from for darker-skinned women and their error rates were far higher.

---

### Part B — Construct Your Own Proxy Variable

**Domain:** Healthcare.

**Protected attribute:** Race.

**Proxy feature:** Prior-year healthcare spending, used as the label for "how sick is this patient" or
"how much care does this patient need."

**Mechanism:** At any given level of illness, Black patients historically generate lower healthcare
spending, because of reduced access, lower insurance coverage, and less trust in and contact with the
system — so spending is a biased measurement of need. A model trained to predict cost therefore learns
that Black patients are "cheaper" and, at the same risk score, under-refers them to the care-management
programmes the model is meant to target. Removing race from the inputs does nothing, because the proxy
carries the signal: the disparity is in the label, not the feature list.

---

### Part C — The Impossibility Result, In Your Own Numbers

Take two groups of 100 applicants each, and suppose the underlying ("true") repayment rates genuinely
differ:

- **Group A:** 60 would repay, 40 would default (base rate 60%).
- **Group B:** 30 would repay, 70 would default (base rate 30%).

Assume for simplicity that the score ranks applicants perfectly within each group, so a threshold
approves the most creditworthy applicants first. (Noise makes the arithmetic messier but does not remove
the tension.)

**Enforcing demographic parity — approve the same share of each group.** Approve the top 40% of each
group:

| Group | Approved | Of whom repay | Of whom default | Approval rate | PPV |
|---|---|---|---|---|---|
| A | 40 | 40 | 0 | 40% | **100%** |
| B | 40 | 30 | 10 | 40% | **75%** |

Approval rates are equal, but the model's positive predictions mean different things in the two groups:
a "approve" signal is right 100% of the time for Group A and 75% of the time for Group B. **Predictive
parity (calibration) is violated.**

**Enforcing predictive parity — make the signal mean the same thing in both groups.** If we require the
same PPV of 100%, we approve only applicants who will repay:

| Group | Approved | Of whom repay | Approval rate | PPV |
|---|---|---|---|---|
| A | 60 | 60 | **60%** | 100% |
| B | 30 | 30 | **30%** | 100% |

Now the signal is calibrated identically, but Group B's applicants are approved at half the rate.
**Demographic parity is violated.** The same happens at any intermediate target: aiming for a common PPV
of 75% in Group A requires approving some applicants who will default, pushing A's approval rate above
B's.

**What the example shows.** With unequal base rates, moving toward equal approval rates forces the
groups' positive predictions to have unequal reliability, and moving toward equal reliability forces
unequal approval rates. These are not bugs in a particular model; they follow from the arithmetic of
different base rates, and the impossibility result proves that no classifier can satisfy demographic
parity, equalized odds, and predictive parity simultaneously in this situation. Something has to give,
and deciding what gives — equal treatment of applicants, or equal meaning of the score — is an ethical
and political choice about what fairness means here. It should be made explicitly and documented, not
inherited by accident from whichever threshold the engineering team happened to tune.

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-22 |

| Part | Marks |
|---|---|
| A — Mechanism diagnosis (three cases) | Credit |
| B — Proxy variable construction | Credit |
| C — Numerical impossibility example | Credit |
| **Total** | **Credit (100 / 100)** |

**Feedback:** Full participation credit. Part A identifies the *primary* mechanism in each case and
distinguishes the root cause from its symptom — notably separating Amazon's biased training signal from
the proxy-variable behaviour it produced. Part B's healthcare example is well chosen: the cost-of-care
label is a genuinely biased measurement of need, and the explanation correctly locates the problem in the
label rather than in the exclusion of race from the features. Part C does the arithmetic honestly in both
directions, showing that equal approval rates break calibration and equal calibration breaks equal
approval rates, and it correctly draws the normative conclusion that the choice of metric is a value
judgment rather than a technical default.
