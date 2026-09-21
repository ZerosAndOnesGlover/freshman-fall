# MATH 141 · Calculus I
## Course Overview & Week-by-Week Road-map

---

**Course:** MATH 141: Calculus I: Limits, Derivatives, and Integrals  
**Credits:** 4  
**Semester:** Fall, Year 1  
**Meeting:** 3 lectures per week (50 min each) + weekly lab (2 hr)  
**Prerequisites:** Precalculus / High School Calculus  

---

## Instructor Note to the Student

Calculus is the first mathematical discipline in your education where you will encounter ideas that took humanity thousands of years to formalize. The ancient Greeks approximated areas with polygons; Archimedes came close to integration. But it took Newton and Leibniz, independently, in the `1660s–1680s`, to develop the unified language: limits, derivatives, integrals; that we use today.

The reason you are learning it is not tradition. It is that calculus is the mathematical machinery underlying:

- Every machine learning algorithm (gradient descent is applied calculus)
- Computer graphics (curves, surfaces, ray tracing)
- Signal processing (Fourier analysis, audio, video, wireless)
- Physics simulation (differential equations everywhere)
- Numerical methods (algorithms that approximate continuous mathematics)
- Algorithm analysis (continuous approximation of discrete sums)

When your CS 331 (AI) course tells you to "take the gradient of the loss function," you will know exactly what that means — because of this course.

---

## Assessment

| Component | Weight | Notes |
|-----------|--------|-------|
| Weekly Problem Sets (12) | **30%** | PS 0–11, released Wednesday, due the following Wednesday at the start of class. Lowest 1 dropped. **Exception: PS 0** is released Monday of Week 0 and due **Friday 25 September 2026, 17:00** — Week 0 is compressed so the course can begin Week 1 on schedule. Week 12's Problem Set 12 is an **ungraded** self-diagnostic and carries no weight. |
| Midterm Exam 1 (Week 6) | **15%** | Thursday 5 November 2026, 18:00–19:15. 75 minutes. Covers Weeks 0–5. 1 cheat sheet (handwritten, 1 side). |
| Midterm Exam 2 (Week 10) | **15%** | Wednesday 2 December 2026, 18:00–19:15. 75 minutes. Covers Weeks 6–9. Same rules. |
| Final Exam (exam period) | **20%** | Wednesday 23 December 2026, 09:00–11:30. 150 minutes. Comprehensive. 2-page cheat sheet. |
| Lab Sections (13 labs) | **10%** | Weekly 2-hr lab, Fridays 15:00–16:50 (Lab 00 on Friday 25 September 2026). Graded on completion + correctness. |
| Weekly Quizzes (12) | **10%** | 15 minutes at the start of Monday's lecture (11:00–11:15), Weeks 1–12 (28 September – 14 December 2026). Quiz *N* covers Week *N−1*. Lowest 1 dropped. |

> **A note on these weights.** The Year 1 curriculum document specifies this course's topics,
> textbooks and credit hours, but **not its assessment breakdown**. The division above is set by the
> department and is the one the Academic Registry gradebook implements. If the curriculum document
> is later revised to specify weights, that revision governs.

**Grading Scale:** this course uses the **university-wide 13-band scale** defined in
[[UNIVERSITY POLICIES]] (Academic Registry) — A+ 97–100, A 93–96, A− 90–92, B+ 87–89, B 83–86,
B− 80–82, C+ 77–79, C 73–76, C− 70–72, D+ 67–69, D 63–66, D− 60–62, F below 60. The registry copy
governs if the two ever differ.

**Credit hours:** 4

---

## Required Textbooks

1. **Stewart, J.** — *Calculus: Early Transcendentals*, 9th ed. (Cengage, 2020)  
   *Primary text. Every problem set and exam draws from this book's exercises. Own it.*

2. **Spivak, M.** — *Calculus*, 4th ed. (Publish or Perish, 2008)  
   *Rigorous, proof-based. Optional but exceptional for understanding WHY calculus works. Read when you want depth.*

**Strongly Recommended:**
- **`3Blue1Brown` — Essence of Calculus** (YouTube, free): Visual intuition for every major concept
- **Paul's Online Math Notes** (tutorial.math.lamar.edu): Free, excellent worked examples
- **MIT `OpenCourseWare` 18.01** (Single Variable Calculus, free): Lectures by David Jerison

---

## Complete Week-by-Week Roadmap

| Week | Topic | Key Concept | Assessment |
|------|-------|-------------|------------|
| **0** | Functions, Algebra, Trig Review | The language calculus speaks | PS 0, Lab 0, Diagnostic Quiz |
| **1** | Limits: Intuition, ε-δ, Limits at Infinity | The ε-δ definition | PS 1, Lab 1, **Quiz 01** |
| **2** | Continuity, Discontinuity, the IVT | Continuity is three conditions | PS 2, Lab 2, Quiz 02 |
| **3** | The Derivative: Definition | Tangent line as a limit | PS 3, Lab 3, Quiz 03 |
| **4** | Differentiation Rules | Power, product, quotient, chain | PS 4, Lab 4, Quiz 04 |
| **5** | Implicit Differentiation & Related Rates | Differentiating both sides | PS 5, Lab 5, Quiz 05 |
| **6** | Extrema, Rolle, MVT, L'Hôpital | Derivatives tell us everything | PS 6, Lab 6, Quiz 06, **MIDTERM 1** |
| **7** | Curve Sketching & Optimization | Shape from derivatives | PS 7, Lab 7, Quiz 07 |
| **8** | The Definite Integral: Riemann Sums | Area as a limit | PS 8, Lab 8, Quiz 08 |
| **9** | Fundamental Theorem of Calculus | Integration = antidifferentiation | PS 9, Lab 9, Quiz 09 |
| **10** | Integration Techniques | Substitution, parts | PS 10, Lab 10, Quiz 10, **MIDTERM 2** |
| **11** | Applications of Integration | Area, volume, accumulation | PS 11, Lab 11, Quiz 11 |
| **12** | Review & Taylor Polynomials Preview | The path forward | PS 12 *(ungraded)*, Lab 12, Quiz 12, **FINAL** |

---

## The Conceptual Arc of the Course

```
WEEK 0:  Review ──────────────────────────────────────────┐
                                                          │ Foundation
WEEK 1:  Limits (intuition)                               │
WEEK 2:  Limits (formal) + Continuity ────────────────────┤
                                                          │ The Language
WEEK 3:  Derivative (definition) ─────────────────────────┤
WEEK 4:  Differentiation Rules                            │ Differential
WEEK 5:  Implicit + Related Rates                         │ Calculus
WEEK 6:  Applications (Extrema, MVT) ─────────────────────┤
WEEK 7:  Optimization ────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WEEK 8:  The Integral (Riemann Sums) ─────────────────────┐
WEEK 9:  Fundamental Theorem ← THE CLIMAX ────────────────┤ Integral
WEEK 10: Integration Techniques                           │ Calculus
WEEK 11: Applications of Integration ─────────────────────┤
WEEK 12: Taylor Polynomials Preview ──────────────────────┘
```

The **Fundamental Theorem of Calculus** (Week 9) is the single most important theorem in the course. It reveals that differentiation and integration — which appear to be completely different operations — are inverse processes. Everything in Weeks 1–8 builds toward this moment.

---

## How to Succeed in This Course

### Weekly Workflow (Proven Method)

**Before lecture (30 min):**
- Read the assigned textbook section
- Note what you don't understand, bring questions

**During lecture (50 min):**
- Do not just copy, understand. If you don't follow a step, put a ❓ in the margin and ask immediately after class
- Rework examples yourself as the instructor does them

**Same day as lecture (60 min):**
- Redo lecture examples from scratch without looking at notes
- This is when learning actually happens, not during the lecture

**Problem set (spread over the week, not the night before):**
- Try each problem alone first. Struggle is the mechanism of learning.
- After 20 minutes stuck: read the relevant section, try again
- After another 20 minutes: look at a worked example, then return to the problem
- Then get help: office hours, study groups

**Before exam:**
- Rework problem sets from scratch
- Do textbook chapter review problems
- Time yourself on old exams

### The Most Important Rule

> **Never skip the algebra steps.**  
> Write every step, even the trivial ones. Most lost points come from errors in algebra that a written intermediate step would have caught. Speed comes from deep understanding, not from skipping steps.

---

## Office Hours & Resources

- **Instructor Office Hours:** TBD — posted on course portal
- **TA Office Hours:** Daily coverage — schedule on portal
- **Math Help Center:** Open 8am–8pm weekdays, no appointment needed
- **Online:** Course discussion board (post within 24 hours of getting stuck)
- **Peer Tutoring:** Available through Academic Success office

---

## Calculator Policy

A scientific calculator is permitted for labs and homework. **Calculators are NOT permitted on quizzes or exams.** Every exam problem is designed to have clean, exact answers if you know the algebra and trig. If you need a calculator for the homework, you need to review your algebra, not rely on the calculator more.

---

## Academic Integrity

Homework: Discussion of approach is allowed. All written work must be independently completed. Copying is plagiarism.

Exams/Quizzes: Closed book, closed neighbor, closed device. The cheat sheet allowance is generous, use it.

---

*Welcome to Calculus I. This is where mathematics becomes a tool for understanding the physical world.*
