# MATH 141 · Calculus I
## Week 0: Review of Functions, Algebra & Trigonometry
### Package README

---

```
MATH141_Week0/
│
├── README.md                          ← You are here
│
├── lectures/
│   ├── Lecture 00 The Language of Mathematics.md (Lecture 0 of 4 — read first)
│   ├── Lecture 01 Functions.md                   (Lecture 1 of 4)
│   ├── Lecture 02 Algebra Review.md              (Lecture 2 of 4)
│   └── Lecture 03 Exponentials Logarithms Bridge.md  (Lecture 3 of 4)
│
├── assignments/
│   └── Problem Set 0.md              (100 pts + bonus — due Friday Week 0)
│
├── lab/
│   └── LAB 00 Graphical Exploration.md           (2-hr Saturday lab)
│
├── quiz/
│   └── QUIZ 00 Diagnostic.md         (Ungraded self-assessment — do it honestly)
│
├── resources/
│   ├── Formula Sheet Week 0.md        (Print this — keep it)
│   └── Course Overview Syllabus.md   (Full course roadmap, grading, policies)
│
└── solutions_instructor/
    ├── Problem Set 0 Solutions Instructor Only.md  ⚠️ NOT FOR STUDENTS
    └── LAB 00 Solutions.md                        ⚠️ NOT FOR STUDENTS
```

---

## Week 0 at a Glance

| Item                             | Status                 | Points          | Notes                                                 |
| -------------------------------- | ---------------------- | --------------- | ----------------------------------------------------- |
| Lecture 0: Language of Math      | Read first             | —               | Sets, set-builder, intervals, ∪/∩, ⇒/⟺, ∀/∃           |
| Lecture 1: Functions             | Read before Mon        | —               | Domain, range, transformations, composition, inverses |
| Lecture 2: Algebra Review        | Read before Tue        | —               | Equations, inequalities, coordinate geometry          |
| Lecture 3: Exponentials & Bridge | Read before Wed        | —               | Exp/log, growth models, preview of calculus           |
| Diagnostic Quiz                  | Complete by Tue        | 0 (ungraded)    | Brutal honesty, find your gaps NOW                    |
| Problem Set 0                    | Due Friday 11:59 PM    | 100             | First real graded assignment                          |
| Lab 00                           | Saturday session       | 0 (orientation) | Not graded, but do it anyway                          |

---

## Learning Objectives for Week 0

By the end of this week, you will be able to:

1. **Read aloud** any statement written in set-builder, interval, or quantifier notation, and translate fluently between all three
2. **State** the formal definition of a function and apply the uniqueness requirement correctly
3. **Determine** the natural domain of any function involving polynomials, rationals, radicals, logarithms, and inverse trig functions
4. **Find** composite functions and inverse functions algebraically
5. **Solve** polynomial, rational, radical, exponential, and logarithmic equations exactly
6. **Solve** linear, polynomial, rational, and absolute value inequalities using sign charts
7. **Apply** all logarithm and exponent laws fluently
8. **Construct** exponential growth and decay models
9. **Recall** exact trigonometric values for all standard angles
10. **Prove** trigonometric identities
11. **Compute** average rates of change and interpret them geometrically as secant slopes
12. **Identify** the central questions of calculus and describe what limits, derivatives, and integrals are (conceptually)

---

## Core Concept of the Week

> **The function is the fundamental object of calculus.**  
> Every theorem in this course is a statement about a function. The domain tells you where the function lives. The rule tells you what it does. The limit (next week) tells you what it approaches. The derivative (Week 3) tells you how fast it changes. The integral (Week 8) tells you its accumulated total. Learn to think in functions, and calculus becomes a single coherent story.

---

## Connections to the CSE Curriculum

| MATH 141 Concept | Where It Reappears in CS/Engineering |
|-----------------|--------------------------------------|
| Logarithms | Binary search $O(\log n)$, information entropy, hash tables |
| Exponentials | Time complexity of brute-force algorithms, signal decay, Big-O classes |
| Rate of change (secant) | Finite difference methods in numerical computing |
| Function composition | Compiler optimization, function pipelines, category theory |
| Inverse functions | Cryptography (one-way functions), data compression |
| Trig functions | Computer graphics (rotation matrices), signal processing (Fourier), physics simulation |
| Absolute value / distance | Loss functions in ML (L1 norm), nearest-neighbor search |
| Domain analysis | Type checking (valid inputs), static analysis, precondition verification |

---

## Recommended Reading Schedule

| Day               | Activity                                                       | Time   |
| ----------------- | -------------------------------------------------------------- | ------ |
| Sunday / Monday AM | Read Lecture 0; do all six Checks **aloud**; Stewart Appendix A | 60 min |
| Monday            | Read Lecture 1; Stewart §1.1–1.2                                | 90 min |
| Monday evening    | Attempt Problems 1–3 of PS0                                     | 60 min |
| Tuesday           | Complete Diagnostic Quiz honestly; review any missed topics     | 60 min |
| Tuesday           | Read Lecture 2 §1–6 (algebra); Stewart §1.3–1.4                 | 90 min |
| Tuesday evening   | Attempt Problems 4–6 of PS0                                     | 60 min |
| Wednesday         | Read Lecture 2 §7 (trigonometry deep dive)                      | 90 min |
| Wednesday evening | Complete PS0 — trigonometry section (Problems 10–12)            | 60 min |
| Thursday          | Read Lecture 3; Stewart §1.5–1.6                                | 90 min |
| Thursday evening  | Attempt Problems 7–9 of PS0                                     | 60 min |
| Friday            | Final review, polish, submit PS0 by 11:59 PM                    | 45 min |
| Saturday          | Lab 00 session — graphical exploration                          | 2 hr   |

**Total: ≈ 12.5 hours.** Budget accordingly — this is a full week of work, not a warm-up.

Two notes on the schedule:

- **Lecture 2 is split across two days on purpose.** It is by far the densest item in the package (intervals, absolute value, five equation types, four inequality types, coordinate geometry, four calculus-specific manipulation techniques, *and* a full trigonometry review). Ninety minutes was never realistic for all of it. §1–6 is the algebra; §7 is trigonometry and stands alone.
- **Every problem set section now follows its lecture.** PS0 was previously due Wednesday, which put Problems 7–9 (exponentials and logarithms, Lecture 3 material) ahead of the lecture that teaches them. The deadline is now **Friday 11:59 PM**, so the order is: read the lecture, then attempt the problems, then do a final pass. Nothing on the sheet is answerable before it has been taught.
- **PS0 is a documented exception to the standard cadence.** Every other problem set is released Wednesday and due the *following* Wednesday — a full seven days (see the syllabus). PS0 is released Monday of Week 0 and due that Friday, which is five. Week 0 is compressed by design so the course can start Week 1 on schedule.

---

## What Week 1 Will Require from This Week

Week 1 opens with the $\varepsilon$-$\delta$ definition of a limit. You will need:

- Fluency reading $\forall$, $\exists$, $\implies$ and "such that" — the ε-δ definition is one long
  sentence in exactly that notation, and Lecture 0 §7.2 decodes it fragment by fragment
- Absolute value inequalities ($|x - a| < \delta$ means $x$ is within $\delta$ of $a$)
- Algebraic manipulation to simplify $\dfrac{f(x) - L}{x - a}$ expressions
- Factoring to cancel $(x - a)$ from numerator and denominator
- Trigonometric identities for computing $\displaystyle\lim_{x\to 0}\frac{\sin x}{x}$

If any of these feel shaky after this week: visit the Math Help Center before Monday.

---

## Note to Instructor

**Week 0 pedagogical intent:** This week is not remediation — it is recalibration. Students arriving from high school calculus will recognize the material but encounter a higher standard of precision (formal domain analysis, sign charts for inequalities, exact trig values under time pressure). Students without prior calculus exposure need this week to build the precalculus foundation.

**On Lecture 0.** It teaches no mathematical content — only the notation the other three lectures assume: set-builder, interval notation, $\cup$/$\cap$, $\Rightarrow$/$\iff$, and the quantifiers. It exists because notation was previously introduced *after* first use (Lecture 1 used interval and set-builder notation in §1 and §3; interval notation was not defined until Lecture 2 §1, and set-builder never was). Students who cannot decode a statement spend their attention decoding instead of learning, which is the most common cause of avoidable failure in a first calculus course. Lecture 0 is short and should not be skipped by confident students — the ε-δ decoding table in §7.2 is what Week 1 depends on.

The diagnostic quiz (ungraded) is critical for early identification of at-risk students. Encourage TAs to flag students scoring below 25/50 for early office hour outreach.

The lab (ungraded) establishes the Python/Desmos toolchain that will be used in graded labs from Week 1 onward. Students who skip Lab 00 typically struggle with Lab 1's submission format.

The Problem Set is deliberately broad — 100 points across all precalculus topics — to surface any weaknesses before the semester's graded content begins in earnest (Week 1 PS is where performance counts toward the final grade in a way that reflects Week 0 preparation).

---

*MATH 141 — Week 0 of 12 | Fall Semester, Year 1*  
*Next: Week 1 — Limits: Intuition and the Formal ε-δ Definition*
