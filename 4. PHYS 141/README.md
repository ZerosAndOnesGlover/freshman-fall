# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics

**Course:** PHYS 141 — Physics I: Mechanics, Waves, and Thermodynamics
**Programme:** B.Sc. Computer Science and Engineering, Year 1 (Freshman)
**Semester:** Fall 2026: Monday 21 September to Friday 18 December 2026 (finals 21–25 December)
**Source materials:** `4. PHYS 141 - Physics I: Mechanics, Waves, and Thermodynamics`

PHYS 141 is the first physics course: mechanics, oscillations, waves and thermodynamics.
Assessment is by problem set, lab and quiz. Problem sets and quizzes are written work; labs are
reports built from measurements recorded in data tables. The course is non-coding.

---

## Topics

| Week | Topic |
|---|---|
| 0 | Measurement, units, coordinate systems and vectors |
| 1 | Kinematics in one dimension |
| 2 | Kinematics in two dimensions: projectiles and circular motion |
| 3 | Newton's three laws of motion |
| 4 | Work, energy and conservation of energy |
| 5 | Momentum, impulse, collisions and centre of mass |
| 6 | Rotational kinematics and dynamics |
| 7 | Angular momentum and static equilibrium |
| 8 | Simple harmonic motion and oscillators |
| 9 | Waves, superposition and standing waves |
| 10 | Sound, the Doppler effect, resonance and decibels |
| 11 | Temperature, heat and thermal expansion |
| 12 | The laws of thermodynamics, entropy and heat engines |

Each course folder has `week0/` … `week12/`, one per teaching week, and each `weekN/` also has a
`practice/` folder for classwork, test code and experiments that is never submitted.

---

## Assessment

| Component | Points | Naming |
|---|---|---|
| Problem Sets | 100 | `weekN/PS N.md` |
| Labs | 100 | `weekN/Lab N.md` |
| Quizzes | 25 | `weekN/Quiz N.md` |

Labs run as three-hour Thursday sessions and are graded on method, so a report carries its own
representative measurements in tables; a plot is described where one is required (labels, fitted
line, R²). Quizzes are filed in the week of their *material* (Quiz N in `weekN/`).

---

## How each assessment is submitted

1. The answer is written under each heading of the answer sheet; a lab report includes its data
   tables and analysis directly in the sheet.
2. The sheet's frontmatter is set to `status: submitted`.
3. The work is committed and pushed.
4. After grading, the sheet's `score:` is filled in and its status set to `graded`.

---

## What is ignored

- `.gitignore` at the repo root applies to every course: OS files, editor files, Python bytecode
  and Obsidian workspace state.
- The final rule, `practice/`, ignores every week's practice folder, so classwork, test code and
  experiments stay local. Anything meant for grading goes in `weekN/` itself.

---
