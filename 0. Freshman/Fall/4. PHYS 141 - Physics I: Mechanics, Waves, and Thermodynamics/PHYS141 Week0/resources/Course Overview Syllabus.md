# PHYS 141 · Course Overview & Syllabus
## Physics I: Mechanics, Waves & Thermodynamics

---

## Course Information

| | |
|---|---|
| **Credits** | 4 |
| **Meetings** | Mon/Tue/Fri, 50 minutes each |
| **Lab** | Thursday 14:00–17:00 (Lab 0: 24 September 2026; Lab 12: 17 December 2026) |
| **Semester** | Fall, Year 1 |
| **Prerequisites** | None (concurrent: MATH 141 strongly recommended) |

---

## Course Description

Physics I grounds the CSE student in the physical world that computation inhabits. Electrical
signals, electromagnetic waves, energy dissipation, and mechanical systems all obey the laws studied
here.

The course covers classical mechanics from kinematics through rotation, then oscillations and waves,
then thermodynamics. Those look like three subjects. They are one method applied three times:
**identify what is conserved, identify what causes change, and write the relationship between them.**

**Relevance to CSE:** electronics, energy, robotics, signal processing. More concretely — ECE 110's
RLC circuits obey the same differential equation as this course's damped oscillator; signal
processing is built on the wave superposition of Weeks 9–10; every thermal-design decision in
computing hardware uses Week 11's heat-transfer relations; and the entropy of Week 12 has the same
functional form as Shannon's information entropy.

---

## Required Textbooks

**1. Halliday, R., Resnick, R. & Krane, K. — Physics, 5th ed.** *(Wiley, 2001)*
"HRK" — rigorous, mathematically demanding, the physicist's reference. Chapter references throughout
the weekly resource sheets are to this text.

**2. Serway, R. & Jewett, J. — Physics for Scientists and Engineers, 10th ed.** *(Cengage, 2018)*
A more accessible alternative with an excellent problem set. Either text is sufficient; students who
find HRK terse should work from Serway and consult HRK for depth.

---

## Assessment Breakdown

| Component | Weight | Details |
|-----------|--------|---------|
| **Problem Sets (13)** | 30% | PS 0–12, released Friday 15:00, due the following Friday at 17:00 (PS 12: Wednesday 23 December 2026, 17:00). Each worth 100 points: 10 problems × 10. **Lowest 1 dropped.** |
| **Laboratory (13)** | 25% | Lab 0–12, Thursdays 14:00–17:00. Each scored out of the total printed on it (100, or 75–85 for Labs 5, 6, 8 and 10, whose Friday-lecture parts were removed), assessed on the written report. **No lab grade is dropped.** |
| **Weekly Quizzes (13)** | 10% | Quiz 0–12, 20 minutes at 14:00, administered the Monday after the material is covered (28 September – 21 December 2026). Each worth 25 points. **Lowest 2 dropped.** |
| **Midterm Exam** (after Week 6) | 15% | 90 minutes, covering Weeks 0–6. *Date not yet set in the registry calendar.* |
| **Final Exam** (Finals week, 21–25 December 2026) | 20% | Comprehensive, 3 hours. *Date not yet set in the registry calendar.* Formula sheet provided; one double-sided A4 sheet of handwritten notes permitted. |

**Total:** 100%

> **A note on these weights.** The Year 1 curriculum document specifies this course's topics,
> textbooks, credit hours, and the weekly 3-hour lab, but **not its assessment breakdown**. The
> division above is set by the department and is what the Academic Registry gradebook implements. If
> the curriculum document is later revised to specify weights, that revision governs.

> **The laboratory weight is deliberately high.** A quarter of the grade rests on experimental work
> because measuring something, estimating its uncertainty, and explaining a discrepancy are skills
> that cannot be acquired from problem sets. Several labs are designed so that the "wrong" answer is
> the informative one — Lab 10's inverse-square law fails indoors because of reflections, and
> explaining that failure earns more marks than a clean result would.

**Grading scale:** this course uses the **university-wide 13-band scale** defined in
[[UNIVERSITY POLICIES]] (Academic Registry) — A+ 97–100, A 93–96, A− 90–92, B+ 87–89, B 83–86,
B− 80–82, C+ 77–79, C 73–76, C− 70–72, D+ 67–69, D 63–66, D− 60–62, F below 60. The registry copy
governs if the two ever differ.

**Credit hours:** 4

---

## Weekly Schedule

| Week | Topic | Lectures | Assessments |
|------|-------|----------|-------------|
| 0 | Measurement, units, coordinate systems, vectors | L01–L03 | PS 0, Lab 0, Quiz 0 |
| 1 | Kinematics in 1D — displacement, velocity, acceleration | L04–L06 | PS 1, Lab 1, Quiz 1 |
| 2 | Kinematics in 2D — projectile and circular motion | L07–L09 | PS 2, Lab 2, Quiz 2 |
| 3 | Newton's three laws of motion | L10–L12 | PS 3, Lab 3, Quiz 3 |
| 4 | Work, energy, and conservation of energy | L13–L15 | PS 4, Lab 4, Quiz 4 |
| 5 | Momentum, impulse, collisions, centre of mass | L16–L18 | PS 5, Lab 5, Quiz 5 |
| 6 | Rotational kinematics and dynamics | L19–L21 | PS 6, Lab 6, Quiz 6, **Midterm** |
| 7 | Angular momentum and static equilibrium | L22–L24 | PS 7, Lab 7, Quiz 7 |
| 8 | Simple harmonic motion and oscillators | L25–L27 | PS 8, Lab 8, Quiz 8 |
| 9 | Waves — properties, superposition, standing waves | L28–L30 | PS 9, Lab 9, Quiz 9 |
| 10 | Sound — Doppler effect, resonance, decibels | L31–L33 | PS 10, Lab 10, Quiz 10 |
| 11 | Thermodynamics I — temperature, heat, thermal expansion | L34–L36 | PS 11, Lab 11, Quiz 11 |
| 12 | Thermodynamics II — laws, entropy, heat engines | L37–L39 | PS 12, Lab 12, Quiz 12, **Final** |

**Lecture numbering.** Lectures run continuously **L01–L39**, three per week: Week *N* owns
`L(3N+1)` through `L(3N+3)`.

**A note on Weeks 6 and 7.** The curriculum document lists Week 6 as "Rotational Kinematics and
Dynamics" and Week 7 as "Torque, Angular Momentum, Moment of Inertia". This course teaches torque and
moment of inertia in Week 6 — rotational *dynamics* is not teachable without them — and devotes Week 7
to angular momentum, its conservation, and static equilibrium. The union of the two weeks covers the
union of the two listed topics, with static equilibrium added.

---

## Problem Set Policy

- **Released:** Friday end of day
- **Due:** The following Friday at 17:00
- **Late policy:** 20% per day, nothing accepted after 3 days
- **Lowest grade dropped**
- **Format:** a single PDF; handwritten is fine if legible. Show working — a bare numerical answer
  earns at most half marks.

## Laboratory Policy

Labs meet Thursday for 3 hours. **Pre-lab questions must be completed before you arrive** and are
checked at the door; students without them may be turned away, since the pre-lab is what makes the
session productive.

Work in pairs, but each student submits an individual report. Reports are due one week after the
session.

**Every lab requires uncertainty analysis.** A measurement without an uncertainty is not a
measurement, and reports that omit it cannot score above half marks regardless of how good the data
are.

---

## Collaboration Policy

**Problem sets:** discuss approaches freely; all written work must be your own.

**Labs:** collaborate on the measurements; write your own analysis.

**Exams:** no collaboration.

**AI tools:** using AI to generate submitted work is academic dishonesty. You may use it to explain a
concept. Note that physics problems are exactly where current AI systems produce confident, wrong,
plausible-looking answers — a habit of checking against the physics is worth more than the time it
saves.

---

## Why This Course Is Designed This Way

You will notice that this course computes things. Every worked example carries real numbers, and the
labs ask you to measure quantities you have just calculated.

That is deliberate. A formula you cannot evaluate is a formula you do not understand, and a
calculation you cannot sanity-check is one you cannot trust. When Week 12 asks whether an engine can
be 55% efficient between 700 K and 350 K, the answer is not a matter of opinion — it is 50%, and the
claim is impossible.

**The most valuable habit this course can give you is the reflex to check.** Does the magnitude make
sense? Do the units work? Did the Doppler shift move in the direction it should? Is the efficiency
below the Carnot limit? Every one of those checks costs seconds and catches errors that would
otherwise propagate silently — through a problem set, through a design, through a career.

---

*PHYS 141 · Course Overview & Syllabus · © CSE Department*
